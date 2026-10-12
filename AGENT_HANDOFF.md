# AGENT_HANDOFF · LabPulse / EEG 双空间项目交接文档

> 写给下一个接手本项目的 AI agent。
> **本文件 2026-10-12 23:0x 全量重写**（旧版 `f0281a7`，10-06 12:21 生成，内容核对至 10-04）。
> 旧版有四处**会直接误导你**：路径写 `C:\Users\wshix\WorkBuddy\`（早已不在那）、写「Streamlit 已装」（其实没装）、
> 交付物按「7 文件 8 节」模型（那批稿子已被取代并删除）、git 写「只有 4 次提交」（现在 17 次）。
> **阅读顺序**：① `.workbuddy\memory\MEMORY.md`（设计意图与规矩的唯一真相源）→ ② 本文（磁盘 / 环境 / 内核 / 同采 / 待办）→ ③ `AI使用日志.md` 最后几行。

---

## 0. 一分钟总览

用户是**大一学生王释贤**（BCI 方向，无编程专业背景），Windows 11。两个空间已从 WorkBuddy 迁到 D 盘：

| 空间 | 路径 | 干什么 | 状态 |
|---|---|---|---|
| **LabPulse** | `D:\Notes\EEG\LabPulse\` | 课程 44511105 Projects 模块（**期末 40%**）唯一计分项目 | Stage 1 已于 10-12 提交；**Stage 2（可运行 MVP）10-27 截止** |
| **EEG** | `D:\Notes\EEG\EEG\` | 纯科研：董航实验室（AI4S³）EEG 设备验收、pilot、课题论证 | 活跃，**工作区有大量他人未提交改动**（见 §3.2） |

两空间**唯一共享资产**是算法内核 `acceptance_check.py`，主本只在 EEG，LabPulse 只有指针 + 三个自定位 `.bat`（契约见 §5）。

**你现在最该做的事**：Stage 2 要交**可运行 MVP**（10-27）。LabPulse 侧现在 **0 个 `.py`**，应用一行都还没写——`MVP规格_LabPulse.md` 已经把要写什么定死了，从那里开工。

---

## 1. 用户与协作规则（违反这些会被打断）

1. **动手改之前先商量**（2026-09-17 明确规则）：带主观判断的活（UI 打磨、文档结构、方案选型）先讲判断、给可选方向，等点头再落地。纯执行类（跑命令、修明确 bug）不受此限。
2. **通俗化讲解**（2026-09-28 长期规则）：用户是初学者，必须解释专业术语（是什么 / 为什么 / 像什么），不假定任何先修知识。
3. **判断权在用户**：评分相关取舍（范围、删节、口径）由用户拍板。真例：10-04 迁移时 agent 建议「16 号企业项目归档」，用户否掉并要求彻底删除——照做。
4. **不伪造过程证据**：AI 合规日志只记真实发生的事，**包括翻车和返工**。LabPulse 空间 2026-10-04 才建 Git，此前无提交痕迹这件事必须在 Stage 文档里如实说明。
5. **不要用 `rm` 批量删文件**（触发安全拦截），改用 `mv`；个人文件删除走回收站或自管回收站。

## 2. 项目是什么（一句话，细节看 MEMORY.md）

用一台已验收的 16 通道设备采脑电（主）+ 表面肌电（辅），把实验操作按 **SOP 步骤表**排成时间线；
用**被试本人的安静基线**判定「这一步偏离了你的常态」（偏离 > X 个标准差且持续 ≥ Y 秒）；
人在回看时自己看、自己判。**定位是镜子，不是判官**——系统不替人下结论。

- 主指标：**theta / alpha 功率比**，双侧判定；其余频段分别报告；**绝不融合成单一分数**
- 两个阳性对照：**白噪声**（人为开关负荷 → 验脑电）· **session 前半 vs 后半**（时间疲劳 → 验肌电）
- 3 名被试各固定 1 个任务（A 称量 / B 用户本人 稀释 / C 采样），**互不交叉**；12 次 session ≈ 18 小时 ≈ 2000 个 30s 窗口
- 次级目标（异常 ↔ 错误的关系）**只是探索性观察**，不写成结论——因为已决定不做诱导错误实验

## 3. 磁盘地图（实况，非旧文档抄录）

### 3.1 LabPulse（本文件所在）

```
LabPulse\
├── AGENT_HANDOFF.md                  ← 本文件（10-12 重写）
├── AI使用日志.md                      ← AI Compliance 10% 主证据，每次实质改动补一行（现 10 行）
├── .gitattributes (149B)  .gitignore (87B)
├── deliverables\course-project\
│   ├── Stage1_Proposal_LabPulse.md   ← 20.2KB，中文，9 节，**10-12 提交，用户已自行改完并冻结，不要再动**
│   └── MVP规格_LabPulse.md            ← 17.6KB，中文，10 节，Stage 2 的施工图
├── scripts\
│   ├── README.md                     ← 指针：算法主本在哪、怎么找
│   └── run_demo.bat / run_file.bat / run_lsl.bat   ← 自定位副本（%~dp0 找主本，找不到打人话报错）
└── .workbuddy\memory\MEMORY.md        ← 本空间长期笔记（9956B，154 行，**内容是最新的**）
```

- **0 个 `.py`、无 `app\`、无 `requirements.txt`** → MVP 完全没开工
- **已不存在**（旧文档还在提）：`迁移执行报告_2026-10-04.md`、日报 `2026-10-03.md` / `2026-10-04.md`、以及 `deliverables\course-project\` 里那 7 份旧稿（`Proposal_EEG_Workbench.md/.docx`、`MVP_PRD.md/.docx`、`中文版_*`、`解读_Proposal与PRD.md`）
- `.gitignore` 现内容：`__pycache__/` `*.pyc` `*.pyo` `.venv/` `venv/` `node_modules/` `.DS_Store` `Thumbs.db` `*.log` `backups/` ⚠️ **尚未忽略 `sessions/`（真实数据目录）——建目录时务必先加**
- `.gitattributes`：`* text=auto eol=crlf`、`*.bat`/`*.cmd` eol=crlf、`*.sh` eol=lf、`*.docx`/`*.doc`/`*.pdf`/`*.png`/`*.jpg` binary

### 3.2 EEG（科研侧）

```
EEG\
├── SHARED_DEPS.md                     ← ★ 跨空间共享依赖契约（改接口前必读）
├── scripts\  acceptance_check.py (13178B, 261 行, canonical)  eeg_bootstrap.py (1858B)
│             run_demo/run_file/run_lsl.bat ×3   + 两张 PSD 样图
├── deliverables\equipment\            ← 设备选型/验收（18 文件，含两份 EEG-EMG 同采分析：**§6 的来源**）
├── deliverables\product-strategy\      ← 课题论证（8 文件）
├── deliverables\course-project\       ← ✅ 已清空（10-12 把 7 份旧副本移入回收站，见 §11）
├── .tmp\                              ← 未全量核对；现至少有 ads1299*.pdf/txt、manual.pdf/txt（未跟踪）
└── .workbuddy\memory\                 ← 科研侧长期笔记
```

⚠️ **EEG 仓库工作区本来就很脏**（不是本次会话造成的），已核实：
- 已修改（`M`）：`.workbuddy/memory/MEMORY.md`、`deliverables/equipment/acceptance-guide-2026-10-03.md`、`deliverables/equipment/lab-assets-map-2026-09-28.md`
- 已删除（`D`，我方造成 7 条 + 他人 5 条）：`deliverables/course-project/*` 7 份（我方）；根目录 `两份方案解读笔记.docx/.md`、`会话摘要_2026-09-21至24.md`、`方案B六问详解_含疑点举例.md`、`项目进展纪要_2026-09-22.md`（他人）
- 未跟踪（`??`）：`.tmp/ads1299*.txt`、`.tmp/manual.pdf/txt`、`.workbuddy/memory/2026-10-08.md`、`deliverables/equipment/` 6 份（含两份同采文档、`验收执行包_2026-10-07.md`、`接线映射表_16ch_单端EEG.md`、`厂商资产勘察_2026-10-07.md`、`说明书导读_2026-10-11.md`）、`deliverables/product-strategy/展示策略_2026-10-08.md`

**按 §1 规矩 + MEMORY.md §七.5：不要把这些裹进你自己的提交。** 要提交就按路径精确 `git add <具体文件>`。

### 3.3 外部引用（勿动）

- `D:\Project-Based_CST_AI_Foundations\`：课程学习路径。`Vibe Coding\` 是同课程另一模块（有独立 Git，根目录是否补了 Git **待核**）
- `D:\董航BCI项目\EEG files\`：设备购买方（第三方机构）资产，**勿表述为我方资产**
- `D:\_EEG_migration_backup\`：迁移备份 + 回收站，**勿清理**

## 4. 环境信息（Windows 11）

### 4.1 两个解释器，别选错（实测）

| 解释器 | 有什么 | 缺什么 |
|---|---|---|
| `C:\Users\wshix\.workbuddy\binaries\python\envs\default\Scripts\python.exe`（Python 3.13.12）**← 唯一运行时** | **mne 1.13.2**、numpy 2.5.3、scipy 1.18.1、matplotlib 3.11.2 | **pandas、streamlit、pylsl 全都没装** |
| `C:\Users\wshix\anaconda3\python.exe`（Python 3.13.9） | pandas 2.3.3、**streamlit 1.51.0**、sklearn 1.7.2、numpy 2.3.5、scipy 1.16.3、matplotlib 3.10.6 | **mne 完全没有**（`find_spec` 返回 None） |

→ **用 .workbuddy 那个 venv**（mne 只在那；在 anaconda 里装 mne 等于给自己挖坑）。开工第一步：
`pip install "pandas>=2.2" "streamlit>=1.40"`，然后生成 `requirements.txt` 并提交。

### 4.2 ★ MNE 的 `~/.mne` 地雷（会复发，记牢）

受限沙箱下 `import mne` 抛 `PermissionError`，**不是没装**，是它要往 `C:\Users\wshix\.mne` 写而那里在沙箱外。
绕行：把 `_MNE_FAKE_HOME_DIR` 指到工作区内目录，并预置配置。

```
环境变量：_MNE_FAKE_HOME_DIR = D:\Notes\EEG\LabPulse\.tmp\mne_home
（需在其下存在 .mne\mne-python.json）→ import mne 即 OK 1.13.2
```

### 4.3 Git：TLS 与沙箱推送（已排过一次，会复发）

- git = `C:\Program Files\Git\cmd\git.exe`，version 2.55.0.windows.5
- **本机 schannel 坏了**（系统 gitconfig `http.sslbackend=schannel`）。症状：`schannel: AcquireCredentialsHandle failed: SEC_E_NO_CREDENTIALS (0x8009030e)`；连 PowerShell `Invoke-WebRequest https://github.com` 也「基础连接已经关闭」。**不是网络坏、不是认证坏。**
  修复：`git config http.sslBackend openssl`（**已写在 LabPulse 仓库级配置里**，别的仓库要另设；要一劳永逸就 `--global`）
- **推送要提权**：沙箱禁止命名管道 → `C:\Program Files\Git\usr\bin\sh.exe: *** fatal error - couldn't create signal pipe, Win32 error 5` → `could not read Username`。本会话内每次 push 都需放宽一次权限；否则**让用户自己在他的终端 push**
- 凭据：`credential.helper = manager`，GCM 在 `C:\Program Files\Git\mingw64\bin\git-credential-manager.exe`；已存 `LegacyGeneric:target=git:https://github.com`（User `TaiVerdus`）
- Git 对中文文件名显示成八进制转义（`\344\270...`），**正常显示问题**，文件没事

### 4.4 其他机器事实

- pandoc = `C:\Users\wshix\anaconda3\Library\bin\pandoc.exe`（可用）；**soffice 未安装**
- Node（备用）：`C:\Users\wshix\.workbuddy\binaries\node\versions\22.22.2-2\node.exe`
- 无 ffmpeg（用 imageio-ffmpeg）；RTX 5070 8GB；下模型走 ModelScope 不走 HF
- `robocopy` 通配符参数必须加引号；写 `D:\` 根文件用 PowerShell + UTF8Encoding($false)
- **禁止从 Bash 或 PowerShell 调 cmd.exe**（安全策略拦截）。`.bat` 冒烟测试的替代法：python 跑等价命令 + 静态三查（BOM / CRLF / 路径解析）

## 5. 跨空间契约与内核真实接口

### 5.1 SHARED_DEPS.md 要点（改接口前读原文）

1. `acceptance_check.py` **主本只在 `EEG\scripts\`**，禁止在 LabPulse 放任何副本（两份必然漂移，而 MVP 拿它当「模块化复用」举证，漂移会毁掉举证）
2. LabPulse 引用用相对路径 `..\..\EEG\scripts\acceptance_check.py`（现在两空间是 `D:\Notes\EEG\` 下的兄弟目录）
3. canonical 的任何修改**只在 EEG 侧做**，改完在 SHARED_DEPS.md 第 5 节追加一行变更记录
4. 文档引用只写文件名/相对路径，不写死绝对路径
5. `.tmp\` 唯一副本不复制、不迁移

### 5.2 内核真实接口（读源码得出，`EEG\scripts\acceptance_check.py`）

- 常量：`NOISE_PASS_UV = 7.0`、`NOISE_WARN_UV = 15.0`、`FLAT_UV = 0.5`、`LINE_RATIO = 3.0`、`SPIKE_Z = 8.0`、`SR_TOL = 0.01`
- 纯函数（**返回 numpy 数组**）：`noise_floor(raw)`、`line_noise_ratios(raw)`、`spike_counts(raw, win_s=20.0)`、`band_power(raw, lo, hi)`、`tr(y, x, axis=1)`、`psd_plot(raw, out_png)`
- `verdict(name, ok, note="")` 返回 bool；⚠️ **`run_battery(raw, label, device_check=True)` 只 print、返回 None** → 不能整块当库用
- 三种模式：`demo()`（读 `C:\Users\wshix\mne_data\MNE-eegbci-data\files\eegmmidb\1.0.0\S001\S001R03.edf`）、`file_mode(path)`（EDF/BDF/FIF）、`lsl_mode()`（需 pylsl）
- CLI：`python acceptance_check.py demo | file <路径> | lsl`（手写 `sys.argv` 分派，无 argparse）

→ MVP 复用它走两条路，**都不复制代码**：按路径 importlib 载入 → 调 `noise_floor` / `band_power` 取数字；`subprocess` 调 CLI 取给人看的报告。

## 6. ★ 必须先知道的技术前提：EEG / EMG 能否同采

Stage 1 §7 曾把这条写成**阻断性**前置条件（「要对厂商说明书核实」）。**这个说法已被推翻**，来源：
`EEG\deliverables\equipment\EEG-EMG同采可行性_2026-10-11.md`（技术版）+ `EEG-EMG同采_通俗版_2026-10-12.md`（大白话版，103 行）。

- **结论「能」**：同一次 session、同一台放大器可混搭。依据是芯片手册第 20 页 + `CHnSET` 里的 **SRB2 位是「每通道一位」** → 想共用参照线的通道打开它，要自己两根线的通道关掉它
- **必须避开 SRB1**：那是**全局**开关，一按下去全部 16 通道跟着变，混搭就做不成。厂商给的接法正好用 SRB2 绕开
- **通道账是零和的**：设备共 **16 通道**；头皮脑电 1 个位置 = **1 路**；手臂肌电 1 条 = **2 路**。16 导脑电帽 + 1 条肌电 → 只剩 **14** 个分析位置；两条肌电 → 只剩 **12**。Fp2 还要留给眼电处理。**定蒙太奇时一次算清**
- **仍未验证的部分**：设备是**两块板叠起来**做的，SRB2 要跨两块板共享，厂商说明**没写**混搭模式是否成立
- **需约 10 分钟真机实测**：4 个通道分两组（2 路按脑电方式接头皮电极、2 路按肌电方式接前臂电极对），手指快速刷前臂。**判据：肌电有反应 且 脑电基线不劣化/不漂移**。坏结果 → 退回只做脑电（主目标不变，Stage 1 §7 的退路 c）
- **该测试尚未执行**，也**尚未写进** `EEG\deliverables\equipment\验收执行包_2026-10-07.md` 的 Step 4。来源文档 §7 的后续：① 把测试写进验收执行包 Step 4；② 定蒙太奇时算通道账

## 7. 证据与痕迹

- **git 共 17 次提交**：`629a42d` 2026-10-04 01:06（初始化仓库骨架）→ `5392b49` 2026-10-12 22:07
  - 建库晚是**真实缺口**，Stage 文档里已如实说明，不要美化
  - `c6c2f17` 10-07 00:55 课程空间迁至 D 盘；`f0281a7` 10-06 12:21 是旧 AGENT_HANDOFF
- 远端 `origin` = https://github.com/TaiVerdus/LabPulse，分支 `master`，与本地一致于 `5392b49`
- ⚠️ **仓库当前是公开的**（python urllib 抓取返回 HTTP **200**；私有仓库对未登录请求会 404）→ **待用户改成 private**。里面对外可读的有 `AGENT_HANDOFF.md`、`AI使用日志.md`、`.workbuddy/memory/MEMORY.md`
- ⚠️ **旧稿仍在远端 git 历史里**：`37a3711` 删掉了 5 份旧交付物（`Proposal_EEG_Workbench.md`、`MVP_PRD.md`、`中文版_Proposal.md`、`中文版_MVP_PRD.md`、`解读_Proposal与PRD.md`），但它们存在于**已推送**的父提交 `b6bf95a` 的树里 → 从历史仍可取回。要彻底移除须改写历史或另建仓库；**转 private 后风险大降**
- `AI使用日志.md` 列口径：时间取 git 提交时间；状态 ✅ 已验证 / 🟡 待用户填判断栏。**目前行 6–10 的判断栏是 🟡，需用户本人用自己的话复核**
- 密钥扫描（`ghp_` / `github_pat_` / `AKIA` / `PRIVATE KEY` / `password=` / `api_key=` / `secret=` / `token=`）：无命中

## 8. ★ 已知过期表述清单（防止下一个 agent 重蹈）

这份项目最大的坑不是技术，是**过期文档被当成事实**。以下表述**全部已过期，不要再引用**：

| 过期说法 | 现在的事实 | 哪儿还残留 |
|---|---|---|
| 「同采能否成立要对厂商说明书核实」「同采是阻断项」 | 芯片层已解决，只剩两块板叠加的 10 分钟实测（§6） | LabPulse `MEMORY.md` §四（带 ⚠️ 标注）、`MVP规格_LabPulse.md` §10 风险行 |
| 「主通道是肌电 EMG」 | **主通道是脑电 EEG**（10-12 第二次修订改回） | git 历史 `e63af56` 的文档里（正常，它是历史） |
| 「Streamlit 已装」 | venv 里**没装**，要 `pip install` | 旧 AGENT_HANDOFF（已作废） |
| 「仓库私有」「在 `C:\Users\wshix\WorkBuddy\`」 | 公开 + 在 `D:\Notes\EEG\` | 旧 AGENT_HANDOFF、`SHARED_DEPS.md` 里的绝对路径示例 |
| 「新版 PRD 待写」 | 已写成 `MVP规格_LabPulse.md` | LabPulse `MEMORY.md` §五 |

> 一句话：**引用任何跨空间事实，只写「路径 + 摘要 + 最后核对日期」；发现过期就顺手改，别只在嘴上说。**

## 9. 待办清单

| # | 事项 | 截止 | 在哪做 |
|---|---|---|---|
| 1 | **Stage 2 = 可运行 MVP**：按 `MVP规格_LabPulse.md` 写模块 1–5，在已录 session 上端到端跑通 | **10-27** | LabPulse（新建 `app/`） |
| 2 | `pip install "pandas>=2.2" "streamlit>=1.40"` + 生成 `requirements.txt` | 开工第一步 | LabPulse |
| 3 | `.gitignore` 补 `sessions/`（真实数据不能进仓库） | 建目录前 | LabPulse |
| 4 | ✅ **已办（10-13）**：两份规格里「同采待核实」的表述已更正为「芯片层已确认可行，只剩约 10 分钟两板叠加实测」；肌电整体推迟到 Stage 4（汇总见 `EEG\SHARED_DEPS.md` §6） | 已办 | LabPulse |
| 5 | 仓库改回 **private** | 尽快 | GitHub 网页（用户操作） |
| 6 | AI 日志行 6–10 判断栏由用户本人复核 | 下次评审前 | 需用户参与 |
| 7 | 把「同采 10 分钟实测」写进 `验收执行包_2026-10-07.md` Step 4 | 基线采集前 | EEG |
| 8 | 定蒙太奇时算清通道账（16 通道 - 肌电 2 路 - 眼电…） | 基线采集前 | EEG |
| 9 | EEG 仓库那批未提交改动（含我方 7 条删除）如何处置 | 待用户裁决 | EEG（**别整仓 `git add -A`**） |
| 10 | ⚠️ **设备 48h 验收（10-03~10-05）结论——查到的文件里没有结论记录**；课程轨 **10-13 起就要采基线**，而验收结论是 P1 的上游闸门。另：`Vibe Coding` 补 Git | **基线采集前** | EEG / 范围外 |

## 10. 记忆体系与开工第一步

| 层级 | 文件 | 读法 |
|---|---|---|
| 用户级 | `C:\Users\wshix\.workbuddy\MEMORY.md` | 跨项目习惯与规则（含大学发展策略：GPA>科研>竞赛、项目 4-6h/周、期中断崖线） |
| LabPulse 项目级 | `.workbuddy\memory\MEMORY.md` | **先读这个**（设计、协议、规矩五条、明确不做八条都在里面） |
| EEG 项目级 | `EEG\.workbuddy\memory\MEMORY.md` | 涉及科研侧时读 |
| 日报 | 两空间各自 `YYYY-MM-DD.md` | 做完实质工作后追加，勿覆盖（LabPulse 侧当前**没有**日报文件） |

**开工第一步（建议）**：
1. 读 `.workbuddy\memory\MEMORY.md` + `deliverables\course-project\MVP规格_LabPulse.md`
2. 跑 §4.1 的 `pip install`，并确认 `_MNE_FAKE_HOME_DIR` 绕行有效（`import mne` 不报 `PermissionError`）
3. 从 MVP 规格里的验收自检 **T1/T2/T5/T6** 入手——**它们不需要设备、不需要真实数据**，能在拿到任何 session 之前先跑通
4. 每次实质改动后：**先 `git status`**（这仓库可能被别的会话同时改）→ 精确 `git add <文件>` → commit → 在 `AI使用日志.md` 补一行

## 11. 备份与回滚

```
D:\_EEG_migration_backup\
├── EEG_20261004_004541.tar.gz      51 文件（解包 md5 反向比对已验证可恢复）
├── EEG_baseline_20261004_004541.md5
├── S_20261004_004541.tar.gz        3 文件（16 号，已取消项目）
├── S_baseline_20261004_004541.md5
├── _回收站_20261004_*\              16 号 3 文件的第二份保险
└── _回收站_2026-10-12_EEG课程旧副本\  7 份旧稿（10-12 从 EEG\deliverables\course-project\ 移入）
```
三个原件 `.bat` 的基线 md5：`8477768f…` / `77414491…` / `d0e54325…`（在 EEG_baseline 文件里）。

---

*文档结束。如与本文件有出入，**以磁盘实际状态 + `git log` 为准**，并顺手修正本文件。*
