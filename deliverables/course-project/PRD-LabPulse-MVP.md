# Product Requirements Document: LabPulse MVP

> 生成依据：`vibe-coding-prompt-template` Part 2（PRD / MVP Generator），In-Between 路径。
> 项目级适配：本文只描述 **Stage 2（MVP，2026-10-27）** 的范围；研究问题与协议见同目录 `Stage1_Proposal_LabPulse.md`。
> **Research status: not provided** —— 本 PRD 未附 `research-LabPulse.md`。因此凡属"现有哪些做法不够用"的判断，一律标注为**本团队判断（未附文献出处）**，不冒充调研结论。

---

## Overview

**Product Name:** LabPulse
**Problem Statement:** 湿实验的质量保障完全是事后发现——稀释倍数算错、离心管标错，通常要到下游才暴露，几小时之后或者永远不暴露；等失效显形时，哪一步出的问题已经不可恢复。同时，操作者本人的状态在真实实验室里**没有任何东西在记录**：自陈不准、一打断就毁掉手上的活，录像回看准但没人会为找五秒钟的失误去回看两小时素材。
**MVP Goal:** 在**已经录好的 session** 上把模块 1–5 端到端跑通一次——给定一段录好的脑电和一张 SOP 步骤表，系统能把信号变成一句可解释的结论：**"稀释 SOP 第 3 步偏离了"**。
**Target Launch:** 2026-10-27（Stage 2 里程碑）。此后 11-10 Stage 3、12-01 Stage 4、12-08 Stage 5 Demo Day。

**一句定位：它是镜子，不是判官。** 系统不判断操作者还能不能继续干，只把操作者自己的信号对着他自己的基线摆出来，判断权在操作者手里。

---

## Target Users

### Primary User Profile

**Who:** 湿实验的真实操作者。本项目共 3 人，各自绑定一项固定任务、不交叉：

| 代号 | 任务 |
|---|---|
| A | 称量 |
| B（作者本人） | 稀释 |
| C | 采样 |

**Problem:** 手上活没停，但不知道自己的状态正在往哪走；出了错也不知道错在哪一步。
**Current Solution:** 没有。现有的只有"事后靠人回忆"和"整段录像"。
**Why They'll Switch:** 它不是又一个要人填表的工具——**全程无文本框输入**（稀释时双手都占着，需要打字的交互事实上不会发生），输出是一句定位到 SOP 步骤的话，而不是一段要人自己解释的曲线。

### User Persona: 操作者 B（稀释）

- **Demographics:** 本科一年级，理工科实验室，个人项目（solo），每周有固定的实验排班
- **Tech Level:** Intermediate（能读懂技术文档与数据格式，代码实现依赖 AI 辅助）
- **Goals:** 在不打断手上操作的前提下，事后能回头看清"哪一步、哪个指标、往哪个方向偏了"
- **Frustrations:** 事后复盘拿不出证据；自陈量表会破坏作业节奏；录像回看的成本高到不会真的去做

---

## User Journey

### The Story

1. 操作者 B 按每周排班进实验室，走真实稀释流程（本就存在的任务，不额外造 session）。
2. 开机、连设备、起 LabPulse（本地跑，不上云、不要账号）。
3. 事先选定任务步骤表（稀释一份 JSON 配置），**该次 session 冻结一份步骤表副本**进会话目录，保证日后能追溯"当时用的是哪一版"。
4. 作业过程中用键盘打点：`空格` = 本步完成、`F1` = 发现失误、`1`–`9` = 自由标签。**不看屏幕也能打。**
5. 信号与打点落在同一条时间轴上（错位必须 < 1 秒）。
6. 作业结束，系统算出每个 30 秒窗口的 theta/alpha 比值与 z 分数，标出**相对 B 本人基线**持续偏离的区段，并归因到具体的 SOP 步骤。
7. B 打开回看页：SOP 步骤色块条 × 生理曲线同图；点任一报警点或标记，图跳到对应信号区间；导出结构化 CSV。

### Key Touchpoints

1. **Discovery:** 不存在"发现"环节——使用者就是 3 位团队成员本人，没有获客路径，**因此本 PRD 不含增长、注册、留存类指标**（不适用，见下方 Success Metrics）。
2. **First Contact:** 双击 `scripts\run_app.bat` 启动本地应用。
3. **Onboarding:** 选择任务 → 选择/导入该 session 的脑电文件 → 确认通道映射与 t0。
4. **Core Loop:** 打点 → 打点 → 打点（每步一次，没有别的交互）。
5. **Retention:** 由课程里程碑与每周真实排班驱动（Stage 3/4/5 各要看一次结果），不是产品化留存。

---

## MVP Features

### Core Features (Must Have)

#### 1. 采集 · 离线导入（Collection）

- **Description:** 读入已录制的脑电文件（`.edf` / `.bdf` / `.fif`），统一到 μV 与统一采样率元信息，建立通道映射与墙钟起点 `t0`。
- **User Value:** 没有统一时钟与通道映射，后面的信号与 SOP 根本对不上。
- **Success Criteria:**
  - 导入同一个文件两次，得到的 `t0`、通道数、采样率**完全一致**
  - `session.json` 如实写入 `t0_source`（`edf_header` / `manual` / `device_clock`）——**手动对表就说手动对表**，不许伪装成设备时钟
  - **不写 EMG 字段**，界面与导出不出现肌电占位
- **Priority:** Critical

#### 2. SOP 时间线（SOP Timeline）

- **Description:** 按任务步骤表配置文件 `sop/<task>.json`（称量 `weighing` / 稀释 `dilution` / 采样 `sampling`）驱动一个步骤状态机，记录每一步起止时刻。
- **User Value:** 这张表是**整个系统的骨架**——它把一段连续信号变成"有位置的结果"，输出才能是"第 3 步偏离"而不是"某处异常"。
- **Success Criteria:**
  - 同一套代码服务三个任务，**任务差异全部在配置里**，不写 if-else 分支；改一份 `sop/*.json` 就能换任务，代码零改动
  - 每次 session 冻结一份步骤表副本进 `sop.json`
  - 允许跳步、允许回退、允许中途新增步骤——真实作业不会按剧本走
- **Priority:** Critical

#### 3. 事件标记（Event Marking）

- **Description:** 键盘一键打标，追加一行到 `events.csv`。
- **User Value:** 稀释时双手占着，这是唯一可行的交互形式。
- **Success Criteria:**
  - **全程无文本框**；单手按 `空格` 十次 → `events.csv` 十行、时刻单调递增
  - 每个标记同时记录 **ISO8601 墙钟时刻**与**相对 t0 的秒数**（一个给人看，一个给机器用）
  - 撤销是软删除（追加 `void` 标记），不真删行
- **Priority:** Critical

#### 4. 状态异常检测（Anomaly Detection · 核心）

- **Description:** 算脑电 **theta / alpha 功率比**，与该操作者本人基线比较，按冻结的 X / Y 规则标记持续偏离，并归因到具体 SOP 步骤。
- **User Value:** 这是"镜子"真正照出来的东西；也是整个课题唯一要回答的问题。
- **Success Criteria:**
  - 判定规则：`|z| > X` **且持续 ≥ Y 秒**才报警；`z` 相对**该操作者自己的基线**（不是绝对阈值，不是别人）
  - **双侧判定**：白噪声段与 session 后段会把 theta/alpha 推向**相反方向**——所以输出是"往哪偏"，不是"累"
  - 窗口：指标窗 30 秒、步进 5 秒；持续判定按 5 秒步进累计（Y 精确到 5 秒，不被 30 秒窗粗糙化）
  - delta / alpha / beta 相对本人基线的偏离**分别报告**（只报不报警），**不合成复合指数**
  - 报警前先过质量闸门：`quality_ok == false` 的窗口只报"不判定"，不算异常也不算正常
  - **合成数据自检必须通过**（见 MVP Completion Checklist T1）
- **Priority:** Critical

#### 5. 同步回看与导出（Playback & Export）

- **Description:** SOP 步骤时间线 × 生理曲线同图；点任一标记或报警点跳到对应信号区间；导出结构化 CSV。
- **User Value:** 这是 3 分钟现场演示（Demo Day）唯一要给人看的东西。
- **Success Criteria:**
  - 一次 session 的导出文件能被 `pandas` 直接读回，行列数与界面一致
  - 导出**不含个人标识**（只有 A / B / C 代号）
- **Priority:** Critical

### Nice to Have (If Time Allows)

- **步骤耗时提示**：`expected_s` 只用于界面提示"这一步比平时慢了"，**不参与报警判定**（否则就变成拿别人/上次的节奏给人定罪）。
- **一次 session 的"跑通记录"导出版**：截图 + 导出 CSV + git 时间戳，作为交付证据。

---

## Out of Scope (Not in MVP)

| Feature | Why Wait | Planned For |
|---|---|---|
| 实时 LSL 采集、设备握手、阻抗检测 | Stage 2 的判定口径只要求"在**已录好的** session 上跑通"，接实时设备会把工期卡在与主目标无关的工程步骤上 | Stage 4 前后 |
| 表面肌电 EMG 辅通道（MDF + RMS） | 主通道的验证**不依赖它**；同采已从关键路径移出。在它真正跑通前，本项目**不声称有两条通道** | Stage 4 前后，且只按探索性报告 |
| 自动决策 / 判断"该停" / 拦作业 | 产品定位是镜子不是判官 | 不做 |
| 把偏离翻译成命名状态（"疲劳""过载"） | 主指标双侧，它本来就不是一把"累"的刻度 | 不做 |
| 把两条通道融合成单一"状态分" | 时间常数与证据强度都不同 | 不做 |
| 跨操作者 / 跨任务比较 | 人与任务在设计上完全混淆 | 不做 |
| 诱导失误 | 真实物料属于另一个在研项目 | 不做 |
| 医学 / 诊断声明 | 超出研究范围 | 不做 |
| 多用户账号、云部署、移动端 | 本地单人使用，无此需求 | 不做 |

*Why we're waiting: 课程在 4 周内只有一个硬里程碑（10-27），范围必须收敛到"离线链路端到端跑通"这一件事上。*

---

## Success Metrics

> 本产品的"成功"分两层，**两层不许混写**。
> 软件层是**硬判据**（过 Stage 2 的唯一依据）；科学层只报**可行性**，且**阴性不阻塞软件交付物**。

### Primary Metrics

**1. 软件层（硬判据）——模块 1–5 端到端跑通，且 T1–T6 全绿**
- **Target:** 2026-10-27 前完成；其中 T1/T2/T5/T6 为脚本自检，**不需要设备、不需要真实数据**
- How to measure: MVP Completion Checklist 的 T1–T6 逐条执行，记录命令与输出
- Why it matters: **这是唯一与硬件到货、与真实数据是否录成无关的判据**

**2. 科学层（可行性，允许阴性）——主通道在两个方向上可分**
- **Target:** 白噪声段相对该操作者安静基线出现可检出偏移（3/3 人）；同 session 前 30 分钟 vs 后 30 分钟 theta/alpha 出现可检出变化（12/12 次 session 算出，≥2/3 人）。**这两项目标在 Stage 3（11-10）才到期，不是 Stage 2 的判据。**
- How to measure: 阈值冻结后的检测输出 + 人工复核
- Why it matters: 若两个对照都对不上，则主目标不成立，**如实报阴性；不许拿肌电结果充数**

### Secondary Metrics

- SOP 标记与信号时间线对齐错位 **< 1 秒**（第 1 周内验证）
- 一次完整 session（采集 → 打标 → 回看 → 导出）**无需他人协助**跑通（1 位操作者独立完成）
- Demo Day 现场端到端演示 **< 3 分钟**通过

### 不适用的指标类别

**Acquisition / Activation / Retention / Revenue / Referral 一律不适用**：使用者是 3 位团队成员本人，无账号、无注册、无付费、无分发路径。**不设 MRR、DAU、留存率一类的目标。**

---

## UI/UX Direction

**Design Feel:** 安静、可读、不打扰——**作业中几乎不需要看它**，事后一眼能看出"哪一步"。

**Inspiration:** 时间轴型回看工具（视频剪辑时间轴 × 生理信号浏览器的组合）。*（本团队判断，未附调研出处。）*

### Key Screens

1. **Session 概览 / 导入**
   - Purpose: 选任务、导入脑电文件、确认通道映射与 t0
   - Key Elements: 任务下拉、文件选择、通道映射表、`t0_source` 如实显示
   - User Actions: 导入、核对、开始
2. **打标页（作业中）**
   - Purpose: 极简打点
   - Key Elements: 当前步骤名 + 大号提示、毫秒级常显时钟（用于人工对表）、快捷键说明
   - User Actions: `空格` / `F1` / `1`–`9` / `Backspace`
3. **回看页**
   - Purpose: 同图叠画 SOP 步骤色块 × theta/alpha 曲线，标出报警区段
   - Key Elements: 双层时间轴、报警标记、质量闸门标记（区分"不判定"与"正常"）
   - User Actions: 点击跳转、缩放、导出 CSV
4. **基线 / 阈值页**
   - Purpose: 展示 `baselines/<operator>.json` 与 `config/thresholds.json` 的冻结状态
   - Key Elements: 基线 mean/sd、X / Y、`frozen` 与 `frozen_commit`
   - User Actions: 查看（**冻结后在此页不可改**）

### Design Principles

- **无文本框优先（Keyboard-only）:** 打标路径上不许出现任何需要打字的控件。双手可能都占着。
- **不判定"不判定"之外的东西:** 界面文案不许出现"疲劳""过载""建议停止"；只有"第几步、哪个指标、往哪偏"。
- **质量状态可见:** 坏段必须显式标成"不判定"，不能悄悄按"正常"处理——那等于伪造正常。

---

## Technical Considerations

**Platform:** 桌面 Web 应用（Python + Streamlit），**本地运行，不上云，不要账号**。

**Responsive:** No（固定桌面使用，不做移动适配）。

**唯一运行时（只有一个解释器，不要换）:**

```
C:\Users\wshix\.workbuddy\binaries\python\envs\default\Scripts\python.exe   （Python 3.13.12）
```

`mne 1.13.2` **只装在这个 venv 里**，而跨空间复用的算法内核 `acceptance_check.py` 本身就 import mne → 两条轨必须共用同一个解释器，否则就是第二份环境漂移。anaconda 没有 mne，**不要**往 anaconda 装 mne。

**Performance Goals:** 本产品无并发、无网络、无在线服务。唯一的时间要求是**打标响应**——按键到落盘必须是即时的（人感觉不到延迟），因为它发生在操作者手上正在干活的时候。

**Security/Privacy:**
- 真实 session 的原始生理数据**不进仓库**（`.gitignore`），只留本机
- 仓库里只放合成样例与导出样例；对外一律以 A / B / C 指代
- 任何被试可随时退出并要求删除记录，无需理由
- 敏感原始数据、未发表结果、凭据**一律不喂 AI 工具**

**Scalability:** Not applicable —— 单机、单人、12 次 session，不涉及多用户或数据增长。

---

## AI / Automation Scope

**AI Surface:** **None**（产品内不含任何 AI 功能，v1 不引入，也不需要）。

- **Allowed Data:** 不适用——产品不调用任何模型。数据不出本机。
- **Provider / Retention:** Not applicable（无模型调用、无外部服务、无遥测）。
- **Output Contract:** Not applicable。
- **Confirmation Rules:** Not applicable。
- **Verification Prompts:** Not applicable。

**AI 仅用于开发协助（构建期）**，并且这是课程明确计分项：
- 每一次产生改动的 AI 交互都记入仓库根目录 `AI使用日志.md`，**时间戳一律取 git 提交时间**（任何人可复现）
- 研究问题、范围取舍与结果解释**由作者本人决定**，AI 只给方案与风险

---

## Constraints & Requirements

### Budget

- 开发工具：**0** —— 全部使用本机已装或免费开源工具（Python / MNE / Streamlit / pandas）
- 托管 / 基础设施：**0** —— 本地运行，不上云
- 第三方服务：**0**
- **Total: 0 / 月**（硬件成本属科研轨的设备验收，不计入本 PRD）

### Timeline

| 日期 | 目标状态 |
|---|---|
| 10-13 ~ 10-26 | 基线 6 次 session 录完；阈值 X / Y 定下并**冻结** |
| **10-27** | **模块 1–5 在已录 session 上端到端跑通；T1–T6 全绿** |
| 10-27 ~ 11-09 | 白噪声段 6 次 session（验主通道） |
| 11-10 | Stage 3：3/3 人**脑电**检测结果 + 下一轮决策 |
| 12-01 | Stage 4：条件允许则引入肌电辅通道；否则保持单模态并如实声明 |
| 12-08 | Stage 5：Demo Day 现场演示 < 3 分钟 |

### Technical Constraints

- **唯一运行时**（见上），`requirements.txt` 必须进仓库，保证 venv 被重建后能一键恢复
- **MNE 的 `~/.mne` 地雷**：MNE 一 import 就会去碰用户目录 `~/.mne`，**在受限沙箱里会直接 `PermissionError`，在用户双击的终端里不会**。所有自检脚本第一行先设可写的假 home（`os.environ.setdefault("_MNE_FAKE_HOME_DIR", r"D:\Notes\EEG\LabPulse\.tmp\mne_home")`），否则在沙箱里测不了。
- **算法内核复用，不许复制**：canonical 在 `D:\Notes\EEG\EEG\scripts\acceptance_check.py`（契约全文 `D:\Notes\EEG\EEG\SHARED_DEPS.md`）。本空间**不放任何副本**，canonical **只在科研空间改**。
  - 要数字（质量闸门、theta/alpha）：按路径 `importlib.util.spec_from_file_location` 载入 canonical，调 `noise_floor` / `band_power` 这些纯函数
  - 要给人看的完整体检报告：`subprocess` 调 canonical 的 CLI，**原样显示它的 stdout**
  - 排错提示：该文件里 `MNE_IMPORT_ERR` 是模块级变量；import 拿到它说明 **mne 没装**，不要去猜数据坏了
- **`run_file.bat` 的已知坑**：文档称支持 CSV，**实际只认 EDF / BDF / FIF** → 录数据优先 BDF

---

## Open Questions & Assumptions

### Open Questions

1. **X / Y 的数值未定。** 规则已定死（`|z| > X` 且持续 ≥ Y 秒），但 X / Y 要等**头两次基线 session 分析后**才能按通道冻结。这是 Stage 2 之前必须关掉的问题。
2. **上游闸门：设备 48h 验收结论未见记录**（窗口 10-03~10-05 已过期）。基线采集 10-13 起就要用设备 → **验收结论是 10-27 的上游依赖**，目前状态为 TBD。
3. **到 10-27 能否录到真实 session。** 兜底已就位：T1/T2/T5/T6 全部不依赖真实数据（合成数据即可交付软件证据）；演示可改用动作构成相同的替代练习任务，并在日志里标注"替代"。
4. **`t0` 的来源未定**（`edf_header` / `manual` / `device_clock`）。`session.json` 要求如实记录，但用哪一种还没定。
5. **BDF 采样率未定论。** 实测 BDF 每记录 2000 采样点：记录时长 1 秒 → 2000 Hz，8 秒 → 250 Hz；`duration` 字段未读到（该文件已被删除）。GUI 面板高亮 250 Hz。→ **采完先打印 `raw.info['sfreq']`。**
6. **BDF 第 20 路 `BDF Annotations` 单位为空**，`mne.io.read_raw_bdf` 可能报错；拟用 `units='uV'` 绕过，**尚未实测**。该通道正是 OpenBCI Marker 写事件的地方，直接关系到"事件对齐"，所以必须解决。
7. **步骤表与视频流规格尚未向实验室索取**（影响步骤 id 与动作边界）。

### Assumptions

- **假设 1:** 3 位操作者的每周真实排班保持不变 → 不需要额外造 session（否则改用替代练习任务并标注）。
- **假设 2:** 脑电在真实湿实验中的伪迹虽重，但**同一 session 内的相对对比**（伪迹对安静段与噪声段同等，差分后存活）足以让大效应显形。
- **假设 3:** 现有做法（自陈量表、录像回看、电子实验记录本）不足以在作业当下发现问题——此判断属**本团队判断，未附文献出处**。
- **假设 4:** 跨空间共用一个解释器与一份算法内核是可持续的（由 `SHARED_DEPS.md` 契约保证）。

### Dependencies

- **外部:** 设备 48h 验收结论（科研轨出具）；实验室每周真实排班；三位操作者的知情同意（B、C 已签署）。
- **内部:** 跨空间算法内核 `acceptance_check.py`；唯一运行时 venv。

---

## Quality Standards

**Code Quality:**
- 用得上类型标注的地方就用；错误要显式处理，不许吞掉
- 交付前把重要路径测一遍（T1–T6 就是这件事的落地形式）
- **阈值冻结之后不许为了凑结果临时改阈值** —— 由 `scripts/check_thresholds_frozen.py` 挡住

**Data Quality:**
- 坏段必须显式标成"不判定"，不许静默按"正常"处理
- 导出不含个人标识
- 真实原始数据不进仓库

**What This Project Will NOT Accept:**
- 占位内容（假数据、假截图）出现在交付物里
- 半成品功能——要么做完，要么明确砍掉
- 在约定的目标平台上跳过测试
- **伪造过程证据**（时间戳、提交记录、验收结论）

---

## Risk Mitigation

| Risk | Impact | Mitigation Strategy |
|---|---|---|
| 到 10-27 一次真实 session 都没录成 | Med | T1/T2/T5/T6 **全部不依赖真实数据**，用合成数据交付软件证据；演示改用替代练习任务并标注 |
| 设备 48h 验收结论始终没出 | High | 标为上游闸门与 TBD，先推进不依赖设备的软件链路；同时向科研轨催结论 |
| `pip install pandas streamlit` 装不上 / venv 被重建 | Low | `requirements.txt` + 一条重建命令写进 `scripts/README.md`（venv 是 harness 托管的，重建是可能的） |
| 真实湿实验伪迹太大，安静段与噪声段分不开 | High | 先用质量闸门剔除坏段；再用同一 session 内的相对对比。仍不可分 → 按提案第五节声明主目标未成立，**如实报阴性** |
| 阈值被临时调整去凑结果 | High | 冻结提交 + T6 脚本。**这是最需要防的一条** |
| 采样率 / BDF 解析结论出错导致后续全部返工 | Med | 采完立刻打印 `raw.info['sfreq']` 并记录；解析结论写明依据（EDF+/BDF 规范 offsets） |

---

## MVP Completion Checklist

> **T1 / T2 / T5 / T6 是脚本，不需要设备、不需要真实数据。** 这是本项目最重要的一条工程保障：即使到 10-27 一次真实 session 都没录成，Stage 2 也能拿出可运行的证据。

### Verification Suite（验收清单）

| # | 检查 | 命令 | 通过标准 |
|---|---|---|---|
| T1 | 检测器合成数据自检 | `python scripts/selftest_detector.py` | 构造"前 60s 正常 + 后 60s 注入已知 theta/alpha 偏移"的合成信号，检测器必须在注入段给出 `flag_ta=1` 并归因到正确步骤；正常段无报警。**这是唯一能证明检测器真的在算东西的测试** |
| T2 | 对齐自检 | `python scripts/selftest_alignment.py` | 注入标记读回误差 < 1 个采样间隔 |
| T3 | 真实 session 端到端 | 双击 `scripts\run_app.bat` → 导入 → 走 SOP → 打标 → 检测 → 回看 → 导出 | 全程无他人协助，导出 `export.csv` 能被 pandas 读回 |
| T4 | **无肌电输入**（默认情形） | 同 T3，用不含任何肌电字段的输入 | 全链路跑通；`windows.csv` 与导出**不出现肌电列**、界面不出现肌电占位 |
| T5 | 复用无漂移 | `python scripts/check_reuse.py` | 同一文件，走内核 CLI 与走 app 质量闸门，**逐通道噪声底一致**（证明没偷偷复制一份算法） |
| T6 | 阈值冻结 | `python scripts/check_thresholds_frozen.py` | 基线分析完后 `frozen=true`；若为 false 则检测器**拒绝出报警**（只出 z 分数） |

### Development Complete

- [ ] 模块 1–5 全部按上述 Success Criteria 实现
- [ ] 基础错误处理到位（导入失败、通道不匹配、缺基线文件都有明确提示）
- [ ] `requirements.txt` 已生成并进仓库

### Quality Checks

- [ ] **T1–T6 全绿**（T3 / T4 若因真实数据缺失无法执行，必须写明原因并给出替代证据）
- [ ] `windows.csv` / `export.csv` 能被 pandas 读回，且与界面显示一致
- [ ] 无个人标识出现在任何导出物中
- [ ] `AI使用日志.md` 已补齐本次全部实质改动

### Release Ready

- [ ] 一次 session 的"跑通记录"已归档（截图 / 导出 CSV / git 时间戳）
- [ ] Demo Day 的 3 分钟演示流程已走通一遍

---

## Next Steps

1. **Immediate:** 复核并确认本 PRD 的范围、Must-Have 清单与 Out of Scope 清单
2. **Next:** 用 `vibe-coding-prompt-template` Part 3 生成 `docs/TechDesign-LabPulse-MVP.md`（技术设计）
3. **Then:** 用 Part 4 生成 `AGENTS.md` / `MEMORY.md` / `REVIEW-CHECKLIST.md` 等 Agent 说明文件
4. **Build:** 按 T1 → T2 → T5 → T6 → 模块 1/2/3 → 模块 4 → 模块 5 的顺序实现（**先做不依赖真实数据的部分**）
5. **Test:** T1–T6 逐条跑；有真实 session 时补 T3 / T4
6. **Milestone:** 10-27 交 Stage 2

---
*Created: 2026-10-14*
*Status: Ready for Technical Design*

---
## Handoff Context
<!-- Machine-readable summary for the next workflow step. Do not delete; the next prompt in the workflow reads this block. -->
- Stage: prd
- App name: LabPulse
- User level: C  (A = vibe coder, B = developer, C = in-between)
- Target platform: Desktop local web app (Python + Streamlit, no cloud, no accounts)
- Budget: 0 (free/open-source only; hardware cost belongs to the research track)
- Timeline: Stage 2 MVP due 2026-10-27; Stage 3 11-10; Stage 4 12-01; Demo Day 12-08
- AI in product scope: no (no model calls inside the product; AI used for development assistance only, logged in AI使用日志.md)
- Research status: not provided — no research-LabPulse.md; all "existing solutions fall short" statements are labeled as team judgement without citations
- Constraints: single runtime venv (Python 3.13.12 at C:\Users\wshix\.workbuddy\binaries\python\envs\default, mne 1.13.2); EEG only (no EMG in MVP); reuse canonical acceptance_check.py by path, never copy; real session data never committed; alignment error < 1 s; thresholds X/Y frozen before white-noise sessions
- Decisions: 5 modules (collection / SOP timeline / event marking / anomaly detection / playback+export); theta-alpha ratio with two-sided |z|>X for >=Y s; 30 s window, 5 s step; per-channel independent reporting, never fused; mirror-not-judge (no automatic decisions, no named states); T1–T6 acceptance suite, T1/T2/T5/T6 hardware-free
- Open questions: X/Y values not yet fixed; device 48 h acceptance result missing (upstream gate); whether any real session can be recorded by 10-27; t0_source choice; BDF sampling rate unresolved (2000 vs 250 Hz); BDF `BDF Annotations` channel has empty unit, mne read workaround untested; SOP/video-stream spec not yet obtained
- Source files: none → docs/PRD-LabPulse-MVP.md
---

```json
{
  "schemaVersion": 1,
  "documentType": "prd",
  "appName": "LabPulse",
  "oneLiner": "A local desktop app that puts the wet-lab SOP timeline on the same axis as the operator's own EEG, and flags sustained deviations from that operator's own baseline at a named SOP step — a mirror, not a judge.",
  "targetUsers": "Wet-lab operators running bench protocols by hand (three operators A/B/C, each bound to one task: weighing / dilution / sampling)",
  "phase": "Foundation",
  "mustHave": [
    "Offline EEG import with channel mapping and wall-clock t0",
    "SOP step timeline driven by per-task JSON config",
    "Keyboard-only event marking (no text input)",
    "Theta/alpha anomaly detection against the operator's own baseline, attributed to a SOP step",
    "Synchronised playback and CSV export"
  ],
  "niceToHave": [
    "Per-step duration hint versus expected_s",
    "Archived run-through evidence pack (screenshots, exported CSV, git timestamp)"
  ],
  "notInMvp": [
    "Realtime LSL acquisition, device handshake, impedance check",
    "EMG auxiliary channel (MDF / RMS)",
    "Automatic decisions or stopping the operator",
    "Named states such as fatigue or overload",
    "Fused single state score across channels",
    "Cross-operator or cross-task comparison",
    "Induced errors",
    "Medical or diagnostic claims",
    "Accounts, cloud deployment, mobile client"
  ],
  "successMetrics": [
    "Modules 1-5 run end to end on recorded sessions; T1-T6 all green by 2026-10-27",
    "T1/T2/T5/T6 pass with synthetic data only, with no device and no real session data",
    "SOP-to-signal alignment error below 1 second",
    "A full session (capture, mark, review, export) completed unaided by one operator",
    "Feasibility only for the science layer: white-noise versus quiet segment separable (3/3 operators) and first-vs-last 30 min change detectable (>=2/3 operators) by Stage 3 — a negative result does not block the software deliverable"
  ]
}
```
