# LabPulse —— MVP 规格（Stage 2）

**课程 44511105 Project-Based CST&AI Foundations · Projects 模块 · 个人项目**
**作者：王释贤 ｜ 里程碑：Stage 2（10-27）｜ 依据：`Stage1_Proposal_LabPulse.md` 定稿**

> 本规格是 **Stage 1 定稿的技术展开**，不是新方向。凡是与 Stage 1 冲突的地方，以 Stage 1 为准。
> 通道主辅分工已按定稿：**脑电 EEG 为主通道，表面肌电 EMG 为辅通道**。

---

## 1. 这个 MVP 要证明什么

Stage 2 的判定口径（Stage 1 第八节）只有一句：

> **模块 1–5 在「已经录好的 session」上端到端跑通一次。**

所以 MVP **不接实时设备**，不需要设备到货，不需要 LSL。它证明的是**软件链路成立**：给定一段录好的脑电（+ 可选肌电）和一张 SOP 步骤表，系统能把信号变成一句「稀释 SOP 第 3 步偏离了」。

**MVP 要证明的三件事**

| # | 命题 | 靠什么证明 |
|---|---|---|
| P1 | 时间对齐成立：人打的 SOP 标记与连续信号对得上 | 错位 < 1 秒（第 6 节，可跑的自检） |
| P2 | 检测器真的在算东西：能识别出「相对本人基线的持续偏离」，并归因到某一步 | 合成数据自检 + 一次真实 session（第 8 节 T1/T3） |
| P3 | 检测不依赖肌电：只剩脑电时全链路照样跑通 | 单通道降级自检（第 8 节 T4） |

**明确不做**（继承 Stage 1 第六节）

- ❌ 不做自动决策、不判断「该停」、不拦作业 → 它是镜子，不是判官
- ❌ 不把 theta/alpha 或 MDF 翻译成命名状态（「疲劳」「过载」）→ 输出只有「第几步、哪个指标、往哪偏」
- ❌ 不把两条通道融合成单一「状态分」
- ❌ 不做实时 LSL 采集、不做医学声明、不做账号 / 云部署 / 移动端
- ❌ 不诱导失误、不碰真实物料

---

## 2. 运行环境（唯一运行时，先读这段再动手）

### 2.1 解释器只有一个

```
C:\Users\wshix\.workbuddy\binaries\python\envs\default\Scripts\python.exe   （Python 3.13.12）
```

**为什么是它而不是 anaconda**：`mne 1.13.2` **只装在这个 venv 里**，anaconda（3.13.9）完全没有 mne。而验收内核 `acceptance_check.py` 本身就 import mne，两空间共用同一个内核 → 必须共用同一个解释器，否则就是第二份环境漂移。

| 解释器 | 已有 | 缺 |
|---|---|---|
| **`.workbuddy` venv ← 本项目用它** | **mne 1.13.2**、numpy 2.5.3、scipy 1.18.1、matplotlib 3.11.2 | pandas、streamlit |
| anaconda 3.13.9（**不用**） | pandas 2.3.3、streamlit 1.51.0、sklearn | mne 完全没有 |

**开工第一步（唯一的环境动作）**

```powershell
& "C:\Users\wshix\.workbuddy\binaries\python\envs\default\Scripts\python.exe" -m pip install "pandas>=2.2" "streamlit>=1.40"
& "C:\Users\wshix\.workbuddy\binaries\python\envs\default\Scripts\python.exe" -m pip freeze > requirements.txt
```

`requirements.txt` 进仓库（第 8 节 T5）。**不要**往 anaconda 装 mne——那是给另一个环境挖坑。

### 2.2 MNE 的 `~/.mne` 地雷

MNE 一 import 就会去碰用户目录 `~/.mne`。**在受限沙箱里跑会直接 `PermissionError`，在用户自己双击的终端里不会**。这不是 bug，是访问边界。

- 正常使用（用户双击 / 普通终端）：**什么都不用做**。
- 受限环境（AI agent、沙箱、CI）跑测试：设一个可写的假 home 再把包导入。

```python
# labpulse/env_guard.py —— 全文就这么点东西
import os
os.environ.setdefault("_MNE_FAKE_HOME_DIR", r"D:\Notes\EEG\LabPulse\.tmp\mne_home")
```

所有自检脚本（第 8 节）**第一行就 import 它**，否则在沙箱里测不了。

### 2.3 启动方式

```powershell
# 双击 scripts\run_app.bat 也可以（第 9 节会加这个启动器）
& <venv>\Scripts\python.exe -m streamlit run app\main.py
```

---

## 3. 五个模块的规格

### 模块 1 · 采集（MVP 范围 = 离线导入）

| 项 | 规格 |
|---|---|
| 输入 | 脑电：`.edf` / `.bdf` / `.fif`；肌电：`.csv`（时间列 + 通道列）或与脑电同文件 |
| 输出 | 内存中的 `Raw`（统一到 μV + 统一采样率元信息）+ `session.json` 里的通道映射与起始时刻 |
| 必须做到 | ① 读取通道数与采样率并与标称值核对；② 建立**墙钟 t0**（该段第一个采样点对应的真实时刻）；③ 通道映射（哪一路是哪个电极位）写成显式配置，不靠猜；④ 肌电缺失时**不报错**，标记 `emg: absent` 后继续 |
| 不做 | 实时 LSL 接收、设备握手、阻抗检测（都属扩展模块） |
| 验收 | 导入同一个文件两次，得到的 `t0` 与通道数完全一致 |

### 模块 2 · SOP 时间线（整个系统的骨架）

| 项 | 规格 |
|---|---|
| 输入 | 任务步骤表配置文件 `sop/<task>.json`（称量 `weighing` / 稀释 `dilution` / 采样 `sampling`） |
| 输出 | 当前步骤状态机 + 每一步的起止时刻（写入 `events.csv`） |
| 必须做到 | ① 同一套代码服务三个任务，**任务差异全部在配置里**，不写 if-else 分支；② 每次 session **冻结一份步骤表副本**进 `sop.json`（步骤表改了也能追溯当时用的是哪版）；③ 允许跳步、允许回退、允许中途新增步骤——真实作业不会按剧本走 |
| 验收 | 改一份 `sop/*.json` 就能换任务，代码零改动 |

### 模块 3 · 事件标记（打标）

| 项 | 规格 |
|---|---|
| 输入 | 键盘：`空格` = 本步完成 / 下一步；`F1` = 发现失误；`1`–`9` = 自由标签；`Backspace` = 撤销上一个标记 |
| 输出 | `events.csv` 追加一行 |
| 必须做到 | ① **全程无文本框**——稀释时双手都占着，需要打字的交互事实上不会发生；② 每个标记同时记录 **ISO8601 墙钟时刻**和 **相对 t0 的秒数**，两个都存（一个给人看，一个给机器用）；③ 撤销是软删除（打 `void` 标记），不真删行 |
| 验收 | 单手按 `空格` 十次，`events.csv` 十行、时刻单调递增 |

### 模块 4 · 状态异常检测（核心）

| 项 | 规格 |
|---|---|
| 输入 | 模块 1 的信号 + 模块 2 的步骤时间线 + 该操作者的基线文件 |
| 输出 | `windows.csv`：每个窗口一行，含指标值、z 分数、是否报警、归因的 **步骤 id** |
| 主通道（脑电） | **theta / alpha 功率比**为主指标，**双侧**判定；delta / alpha / beta 相对本人基线的偏离**分别报告**（只报不报警） |
| 辅通道（肌电） | **MDF**（中值频率）与 **RMS**；MDF 单侧判定（下降为异常方向），RMS 只报告 |
| 判定规则 | `|z| > X` 且**持续 ≥ Y 秒**才报警；`z` 相对**该操作者自己的基线**（不是绝对阈值，不是别人） |
| 窗口 | 指标窗 30 秒、步进 5 秒（滑动窗）。持续判定按 5 秒步进累计 → Y 能精确到 5 秒，不被 30 秒窗粗糙化 |
| 两条通道 | **各自独立判定、分别报告，绝不融合成一个分数**；不做自动决策，不命名状态 |
| 阈值 | X / Y **按通道**存在 `config/thresholds.json`，前两次基线 session 分析后定下并**冻结**（见第 5 节） |
| 质量闸门 | 报警前先过质量：`quality_ok == false` 的窗口只报「不判定」，不算异常也不算正常 |

### 模块 5 · 同步回看与导出

| 项 | 规格 |
|---|---|
| 输入 | `windows.csv` + `events.csv` + 质量结果 |
| 输出 | ① 同图叠画：SOP 步骤色块条 × 脑电 theta/alpha 曲线（+ 肌电 MDF 第二条）；② 结构化导出 `export.csv` |
| 必须做到 | 点任一事件标记或任一报警点，**图跳到对应信号区间**；导出**不含个人标识**（只有 A / B / C 代号） |
| 验收 | 一次 session 的导出文件能被 pandas 直接读回、行列数与界面一致 |

---

## 4. 数据契约（谁在写文件、写成什么样）

### 4.1 目录结构

```
sessions/
  2026-10-15_B_dilution_01/
    raw/            eeg_*.edf | emg_*.csv
    session.json    元数据（操作者、任务、t0、通道映射、采样率）
    sop.json        该次实际使用的步骤表副本（冻结）
    events.csv      打标事件
    windows.csv     检测输出
    quality.json    质量闸门结果
baselines/
  B.json            操作者 B 的基线（mean / sd，按通道分）
config/
  thresholds.json   X / Y，按通道，冻结后不许再改
sop/
  weighing.json  dilution.json  sampling.json
```

### 4.2 `session.json`（关键字段）

```json
{
  "session_id": "2026-10-15_B_dilution_01",
  "operator": "B",
  "task": "dilution",
  "t0_iso": "2026-10-15T14:03:11+08:00",
  "t0_source": "edf_header | manual | device_clock",
  "eeg": { "file": "raw/eeg_01.edf", "sfreq": 250, "channels": ["Fz","Cz","Pz","..."] },
  "emg": { "file": "raw/emg_01.csv", "sfreq": 1000, "channels": ["FDS","EDC"] },
  "notes": ""
}
```

`t0_source` 必须如实填——**手动对表就说手动对表**，不许伪装成设备时钟。

### 4.3 `events.csv`

```
t_iso,t_rel_s,kind,step_id,label
2026-10-15T14:04:32+08:00,81.2,step_done,dilute.s1,
2026-10-15T14:07:10+08:00,239.0,mistake,dilute.s3,吸头碰壁
```

`kind ∈ {step_start, step_done, mistake, free, void}`

### 4.4 `windows.csv`

```
t_start_s,t_end_s,step_id,eeg_ta,z_ta,flag_ta,emg_mdf,emg_rms,z_mdf,flag_mdf,quality_ok
15.0,45.0,dilute.s1,1.42,0.31,0,,,,1
120.0,150.0,dilute.s2,2.87,2.41,1,88.2,41.0,-1.9,0,1
```

`flag_*` 已是「持续 ≥ Y 秒」之后的最终结论，不是单窗原始判定；单窗原始判定另存 `z_*`，便于事后复核。

### 4.5 `sop/<task>.json`

```json
{
  "task": "dilution", "task_label": "稀释", "version": 1,
  "steps": [
    { "id": "dilute.s1", "label": "取原液",      "expected_s": 60 },
    { "id": "dilute.s2", "label": "加入缓冲液",  "expected_s": 90 },
    { "id": "dilute.s3", "label": "混匀",        "expected_s": 30 }
  ]
}
```

`expected_s` 只用于界面提示「这一步比平时慢了」，**不参与报警判定**（否则就变成拿别人/上次的节奏给人定罪）。

---

## 5. 基线与阈值（这条决定结果能不能被评判）

1. **基线 = 该操作者本人的安静作业 session**（每人 2 次，Stage 1 第四节）。基线算 mean / sd，写入 `baselines/<operator>.json`。
2. 阈值 X / Y 在**前两次基线 session 分析后**定下，写入 `config/thresholds.json`：

```json
{
  "frozen": true,
  "frozen_at": "2026-10-26T21:00:00+08:00",
  "frozen_commit": "<git hash>",
  "channels": {
    "eeg_theta_alpha": { "X": 2.0, "Y": 30, "direction": "both" },
    "emg_mdf":         { "X": 2.0, "Y": 30, "direction": "down" }
  }
}
```

3. **冻结的含义**：`frozen: true` 之后，改阈值必须显式提 `frozen: false` 并且**在 git 里留下一条单独的提交**。当场改阈值来「凑出」好结果，是最容易发生也最没品的一种作弊——脚本 `scripts/check_thresholds_frozen.py` 会把这条挡住（第 8 节）。
4. 主指标**双侧**的理由（Stage 1 第二节）：白噪声段与 session 后段会把 theta/alpha 推向**相反**方向。所以同一个比值朝两头偏 → 它本来就不是「累」的刻度，输出也不许叫「累」。

---

## 6. 时间对齐（P1，错位 < 1 秒）

| 项 | 做法 |
|---|---|
| 统一时钟 | 一切时刻都归到 **t0**；`t_rel_s = (t_press − t0)`，由打标那一刻算出并落盘，**不在事后重新推算** |
| 两个都存 | 墙钟 ISO8601（给人看、能对照墙上的表） + 相对秒数（给机器用） |
| 怎么验证 | ① **合成数据自检**：在已知采样点注入一个标记，读回后相对误差必须 < 1 个采样间隔；② **人工对表自检**：打标界面上常显毫秒级时钟，打标时与外部秒表对一次，误差记进 `session.json` |
| 已知误差源 | 键盘响应延迟（几十毫秒级） + 人按下时的判断延迟（几百毫秒级）。**后者是人的，不是软件的**——所以 1 秒是合理线，往 100 毫秒较真是浪费 |

---

## 7. 复用验收内核：契约怎么落地

**canonical 位置**：`D:\Notes\EEG\EEG\scripts\acceptance_check.py`（契约全文 `D:\Notes\EEG\EEG\SHARED_DEPS.md`）
**铁律**：课程空间**不放任何副本**，canonical **只在科研空间改**。

内核的真实形状（读过源码，不是猜）：

- `noise_floor(raw) -> np.ndarray`（逐通道 1–40Hz RMS μV）
- `line_noise_ratios(raw) -> (r50, r60)`（工频比值数组）
- `spike_counts(raw, win_s=20.0) -> np.ndarray`
- `band_power(raw, lo, hi)`（频段功率——**theta/alpha 主指标直接用这个**）
- `run_battery(raw, label, device_check=True)` → **只 print，不返回**（人看的报告）
- CLI：`python acceptance_check.py demo | file <路径> | lsl`（`sys.argv` 手写分派）

**因此分两条路用它，都不复制代码：**

| 用途 | 怎么调 | 为什么这么选 |
|---|---|---|
| 要**数字**（质量闸门、theta/alpha） | 按路径 import 那几个纯函数：`importlib.util.spec_from_file_location` 载入 canonical → 调 `noise_floor` / `band_power` | 它们返回 numpy 数组，能直接用在检测链路里；canonical 一行都不用改 |
| 要**给人看的完整体检报告** | `subprocess` 调 canonical 的 CLI，**原样显示它的 stdout** | 报告是给人读的散文，硬解析成结构体是自找的脆弱 |

**推荐诊断（背下来）**：这个文件里 `MNE_IMPORT_ERR` 是模块级变量。如果 `import` 拿到的是 `MNE_IMPORT_ERR`，说明 mne 没装——**报这个错，不要去猜是数据坏了**。

---

## 8. 「MVP 算完成」的验收清单（每条都能跑）

| # | 检查 | 命令 | 通过标准 |
|---|---|---|---|
| T1 | 检测器合成数据自检 | `python scripts/selftest_detector.py` | 构造一段「前 60s 正常 + 后 60s 注入已知 theta/alpha 偏移」的合成信号，检测器必须在注入段给出 `flag_ta=1` 且归因到正确步骤；正常段无报警。**这是唯一能证明检测器真的在算东西的测试** |
| T2 | 对齐自检 | `python scripts/selftest_alignment.py` | 注入标记读回误差 < 1 个采样间隔 |
| T3 | 真实 session 端到端 | 双击 `scripts\run_app.bat` → 导入 → 走 SOP → 打标 → 检测 → 回看 → 导出 | 全程无他人协助，导出 `export.csv` 能被 pandas 读回 |
| T4 | **单通道降级**（肌电缺席） | 同 T3，但 `emg: absent` | 主目标链路完整跑通；界面明确显示「肌电通道缺失，仅脑电」 |
| T5 | 复用无漂移 | `python scripts/check_reuse.py` | 同一文件，走内核 CLI 与走 app 质量闸门，**逐通道噪声底一致**（证明没偷偷复制一份算法） |
| T6 | 阈值冻结 | `python scripts/check_thresholds_frozen.py` | 基线 session 分析完后 `frozen=true`；若为 false 则检测器拒绝出报警（只出 z 分数） |

**T1/T2/T5/T6 是脚本，不需要设备、不需要真实数据**——所以**即使到 10-27 一次真实 session 都没录成，Stage 2 也能拿出可运行的证据**。这是本项目最重要的一条工程保障（Stage 1 第二节的「核心承诺永不依赖硬件」的延续）。

---

## 9. 交付物与里程碑（10-27）

| 交付物 | 内容 |
|---|---|
| `app/` | 模块 1–5 的 Streamlit 应用（本地运行，不上云，不要账号） |
| `scripts/` | `run_app.bat`（新）+ 四个自检脚本 + `selftest_*.py` |
| `sop/`、`config/`、`baselines/` | 三份任务步骤表、阈值文件、基线文件各一份**样例**（真实数据进 `.gitignore`） |
| `requirements.txt` | 唯一运行时的依赖清单（第 2.1 节生成） |
| `docs/` 或交付物目录 | 本规格 + 一份「跑通记录」（截图 / 导出 CSV / git 时间戳） |

**数据边界**：真实 session 的原始生理数据**不进仓库**（`.gitignore`）。仓库里只放合成样例与导出样例。参与者以 A / B / C 指代。

| 日期 | 目标状态 |
|---|---|
| 10-13 ~ 10-26 | 基线 6 次 session 录完，阈值 X / Y 定下并冻结（第 5 节） |
| **10-27** | **模块 1–5 在已录 session 上端到端跑通；T1–T6 全绿** |
| 10-27 ~ 11-09 | 白噪声段 6 次 session（验主通道） |
| 11-10 | Stage 3：3/3 人检测结果 + 下一轮决策 |

---

## 10. 风险与降级（对应 Stage 1 第八节）

| 风险 | 降级方案 |
|---|---|
| 肌电与脑电无法同采（**阻断性**，Stage 1 第七节） | **主目标不受影响**：模块 1 与 T4 从第一天就按「只有脑电」设计。砍掉辅通道必须明确声明为降级，**不许包装成两条通道都跑了** |
| `pip install pandas streamlit` 装不上 / venv 被重建 | `requirements.txt` + 一条重建命令写进 `scripts/README.md`；venv 是 harness 托管的，重建是有可能的，所以要能一键恢复 |
| 到 10-27 一次真实 session 都没录成 | T1/T2/T5/T6 **全部不依赖真实数据**，用合成数据交付软件证据；演示改用动作构成相同的替代练习任务，并在日志里标注「替代」 |
| 真实湿实验伪迹太大，安静段与噪声段分不开 | 先用质量闸门剔除坏段；再用**同一 session 内的相对对比**（伪迹对两段同等，差分后存活）。仍不可分则按 Stage 1 第五节声明主目标未成立，**如实报阴性** |
| 阈值被临时调整去凑结果 | T6 脚本 + 冻结提交（第 5 节）。**这是最需要防的一条** |

---

*规格版本 v1 —— 2026-10-12。继承 `Stage1_Proposal_LabPulse.md`（EEG 主 / EMG 辅）；本文件只展开实现，不改方向。*
