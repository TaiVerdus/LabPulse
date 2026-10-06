# AGENT_HANDOFF · LabPulse / EEG 双空间项目交接文档

> 写给下一个接手本项目的 AI agent。**本文件自包含**，读完后即可直接干活。
> 生成时间：2026-10-06 12:20（内容核对至 2026-10-04 01:25 的磁盘状态，此后无新提交）

---

## 0. 一分钟总览

用户是**大一学生王释贤**（BCI 方向，无编程专业背景），一台 Windows 11 机器上跑着**两个 WorkBuddy 工作空间**，10-04 刚从"混在一个空间"拆出来：

| 空间 | 路径 | 干什么 | 状态 |
|---|---|---|---|
| **LabPulse** | `C:\Users\wshix\WorkBuddy\LabPulse\` | 课程 44511105 Projects 模块（**期末 40%**）唯一计分项目：湿实验操作状态记录与可视化的 Streamlit 桌面网页应用 | **活跃开发中，Stage 1 截止 10-13** |
| **EEG** | `C:\Users\wshix\WorkBuddy\EEG\` | 纯科研：董航实验室（AI4S³）的 EEG 设备验收、pilot、课题论证 | 活跃（设备 48h 验收窗口 10-03~10-05） |

两个空间**唯一的共享资产**是算法内核 `acceptance_check.py`，主本在 EEG，LabPulse 只有指针和三个自定位 `.bat` 副本（契约见第 5 节）。

**你现在最该做的事**：LabPulse 的 Stage 1（Proposal + PRD + AI 合规 + Git 提交）10-13 截止，文档主体已就位（见第 4.2 节），但有几件收尾事（第 6 节）。

---

## 1. 用户与协作规则（违反这些会被打断）

1. **动手改之前先商量**（用户 2026-09-17 明确规则）：凡是带主观判断的活（UI 打磨、文档结构、方案选型），先讲判断、给可选方向，等点头再落地。纯执行类（跑命令、修明确 bug）不受此限。
2. **通俗化讲解**（2026-09-28 长期规则）：用户是初学者，必须解释专业术语（是什么/为什么/像什么），不要假定任何先修知识。
3. **判断权在用户**：评分相关取舍（范围、删节、口径）由用户拍板。真实例子：10-04 迁移时，agent 建议"16 号企业项目保留归档"，用户否掉并要求彻底删除——照做了。
4. **不伪造过程证据**：AI 合规日志只记真实发生的事，包括翻车和返工；LabPulse 空间 10-04 才建 Git，此前无提交记录这件事要在 Stage 文档里**如实说明**，不能编。
5. 不要用 `rm` 批量删文件（触发安全拦截），改用 `mv`；个人文件删除走回收站或自管回收站。

## 2. 项目背景（课程）

- 课程：**44511105《Project-Based CST&AI Foundations》**，天津大学—香港理工大学深圳未来技术学院，英文授课
- Projects 模块占期末 **40%**；另有贯穿全课的 **AI Compliance 10%**（五项标准各 2 分：带时间戳的 AI 交互日志 / 质疑验证 AI / 能解释 AI 生成内容 / 署名与边界 / 伦理隐私）
- 大纲原文允许两种项目来源："topics come from **enterprise partners or student proposals**"。用户 10-02 曾建 16 号企业项目（翔宇医疗，4 人团队任队长），**10-04 已整体取消**，痕迹移入 `D:\_EEG_migration_backup\_回收站_*`，不建独立空间。现在唯一计分项目 = LabPulse
- **LabPulse 是什么**：Python + Streamlit + MNE 的桌面网页应用。功能：导入脑电记录→自动质量检查→干活时一键打标→操作时间线与 EEG 频段能量曲线同步回放→导出结构化会话日志→管理历史会话；最终形态经 LSL 接收用户自购 16 通道设备的实时数据
- **核心承诺（写进 Proposal，不能违背）**：核心产品永不依赖硬件是否到货——演示基线用 PhysioNet EEGBCI 公开数据集；设备接入与 LSL 实时模式是扩展模块，各有降级路径
- **模块化复用卖点（评分举证）**：信号质量模块复用 `acceptance_check.py`——用户在设备验收阶段已写好并验证过的分析内核

## 3. 磁盘地图

### 3.1 LabPulse 空间（本文件所在）

```
LabPulse\
├── AGENT_HANDOFF.md                  ← 本文件
├── 迁移执行报告_2026-10-04.md         ← 拆分迁移的方案+执行记录+校验结果（背景细节看这里）
├── AI使用日志.md                      ← AI Compliance 10% 的主证据，每次改动后补一行
├── deliverables\course-project\      ← 课程交付物（7 个文件）
│   ├── Proposal_EEG_Workbench.md/.docx    英文 Proposal（8 节，Stage 1 主交付）
│   ├── 中文版_Proposal.md                 中文版（同样 8 节）
│   ├── MVP_PRD.md/.docx / 中文版_MVP_PRD.md
│   └── 解读_Proposal与PRD.md              面向用户的讲解稿（18 个标题，含子节）
├── scripts\
│   ├── README.md                      ← 指针：算法主本在哪、怎么找
│   └── run_demo.bat / run_file.bat / run_lsl.bat   ← 自定位副本（%~dp0 找主本，找不到打人话报错）
└── .workbuddy\memory\
    ├── MEMORY.md                      ← 本空间长期笔记（新会话先读）
    ├── 2026-10-03.md                  ← 课程块（从 EEG 切分而来）
    └── 2026-10-04.md                  ← 迁移完成记录
```

### 3.2 EEG 空间（科研侧）

```
EEG\
├── SHARED_DEPS.md                     ← ★ 跨空间共享依赖契约（改接口前必读）
├── scripts\
│   ├── acceptance_check.py            ← ★ canonical：信号质量算法内核（261 行）
│   ├── eeg_bootstrap.py               纯科研启动脚本
│   └── run_*.bat ×3                   原件（md5 已入基线，勿改）
├── deliverables\equipment\            设备选型/验收（9 文件）
├── deliverables\product-strategy\     课题论证（6 文件）
├── deliverables\course-project\       ⚠️ LabPulse 的旧副本，**10-13 提交后删除**
├── .tmp\                              三个唯一副本：PlanB_full.txt（导师方案书全文）、
│                                       ExpandableEEG_manual.txt、naolichuang_16ch.txt
│                                       + 中立工具 extract2.py / md2docx.py
├── 项目方案书_v0.1.md 等 5 份科研文档
└── .workbuddy\memory\                 9 份日志 + MEMORY.md（科研侧长期笔记）
```

### 3.3 外部引用（勿动）

- `D:\Project-Based_CST_AI_Foundations\`：课程学习路径。`Vibe Coding\` 是同课程另一模块（10-09 截止，有独立 Git + 234 KB AI 日志，根目录缺 Git 待补）
- `D:\董航BCI项目\EEG files\`：设备购买方（第三方机构）资产，勿表述为我方资产
- `D:\_EEG_migration_backup\`：迁移备份 + 16 号回收站，**勿清理**

## 4. LabPulse 当前状态

### 4.1 Git（刚建立，历史很短）

```
d87f97e 10-04 01:23 docs: 迁移执行报告
c2780b1 10-04 01:21 docs: 补 10-04 迁移日志
dc00d89 10-04 01:19 feat: 课程项目空间建立
629a42d 10-04 01:06 chore: 初始化仓库骨架
```
`.gitattributes`：全文本 CRLF、`.bat` 强锁 CRLF、`.docx/.pdf/图片` binary。
`.gitignore`：**不忽略 `.tmp/`**（那里有唯一副本，必须进版本保护）。
EEG 空间同样有 Git（3 次提交）。git 身份已配全局：`Verdus / wshixian2026@163.com`。

### 4.2 交付物状态

| 交付物 | 状态 | 备注 |
|---|---|---|
| 英文 Proposal | ✅ 8 节完整 | 10-04 补回过被误删的三节：利益相关者沟通（=第 5 节，Stage 1 评分点）、交付路径与风险控制（7）、伦理数据与 AI 合规（8）；产品范围退回第 6 节。Word 已重生成（9 标题 4 表） |
| 中文 Proposal | ✅ 8 节完整 | 同上 |
| MVP_PRD 中英文 | ✅ | 引用 `acceptance_check.py` 属语义引用，路径变化不影响 |
| 解读稿 | ✅ 与正文对齐 | 曾按 8 节讲解而正文只剩 5 节，补回后已对齐 |
| AI 使用日志 | 🟡 骨架已建 | 格式对齐 Vibe Coding 那本（五项标准 + git 时间戳表格）；第 2–5 行"我的判断"栏**需用户本人用自己的话复核** |
| Git 提交痕迹 | 🟡 只有 4 次 | 空间 10-04 才建库，此前无证据——需在 Stage 文档如实说明 |

### 4.3 已验证过的运行链路

`python acceptance_check.py demo` 完整跑通（MNE EEGBCI 数据已缓存本机，输出验收电池报告 + PSD 图，退出码 0）。LabPulse 侧 `.bat` 自定位逻辑已测：无 BOM、全 CRLF、CANON 路径解析 OK。

## 5. 跨空间契约（SHARED_DEPS.md 摘要，改接口前必读原文）

1. `acceptance_check.py` **主本只在 `EEG\scripts\`**，禁止在 LabPulse 放任何副本（两份必然漂移，且 PRD 拿它当"模块化复用"举证，漂移会毁掉举证）
2. LabPulse 引用它：相对路径 `..\EEG\scripts\acceptance_check.py`（前提：两空间同为 `C:\Users\wshix\WorkBuddy\` 直接子目录）
3. canonical 的任何修改**只在 EEG 侧进行**，改完在 SHARED_DEPS.md 第 5 节追加一行变更记录
4. 文档引用只写文件名/相对路径，不写死绝对路径
5. `.tmp\` 三个唯一副本不复制、不迁移

## 6. 待办清单（按优先级）

| # | 事项 | 截止 | 在哪做 |
|---|---|---|---|
| 1 | LabPulse **应用本体开发**：Streamlit 骨架（导入/质检/打标/回放/导出/历史会话六模块），先跑通公开数据集 demo | 10-13 前 | LabPulse（新建 `app/` 或同级，技术栈 Python+Streamlit+MNE） |
| 2 | Stage 1 提交材料整合 + 提交 | **10-13** | LabPulse |
| 3 | AI 日志第 2–5 行"我的判断"栏请用户复核 | 10-13 前 | 需用户参与 |
| 4 | Stage 文档说明"10-04 才建 Git"的证据缺口 | 10-13 前 | LabPulse |
| 5 | 清掉 `EEG\deliverables\course-project\` 旧副本 | **10-13 之后**（现在是心理安全垫） | EEG |
| 6 | Vibe Coding 根目录补 Git | 10-09 前 | 本次范围外，单独排 |
| 7 | 设备 48h 验收窗口（10-03~10-05）结果跟进 | 已过窗口，向用户确认结果 | EEG |
| 8 | 科研侧：周三取样/稀释模块时长确认、SOP 与视频流规格、错误分类学 v1、方案书 v0.2、文献清单 | 滚动 | EEG（详见 EEG memory） |

## 7. 环境信息（Windows 11）

- Python：`C:\Users\wshix\.workbuddy\binaries\python\envs\default\Scripts\python.exe`（venv，MNE/Streamlit 等已装，跑通过 demo）
- Node（备用）：`C:\Users\wshix\.workbuddy\binaries\node\versions\22.22.2-2\node.exe`
- Git Bash 可用；**禁止从 Bash 或 PowerShell 调 cmd.exe**（被安全策略拦截）。bat 冒烟测试的替代法：用 python 直接跑等价命令 + 静态三查（BOM/CRLF/路径解析）
- Bash 工具 PATH 可能损坏，命令前加 `export PATH="/usr/bin:/bin:$PATH"`（若报错）
- 本机无 ffmpeg（用 imageio-ffmpeg）；有 RTX 5070 8GB；下模型走 ModelScope 不走 HF
- `robocopy` 通配符参数必须加引号；写 `D:\` 根文件用 PowerShell + UTF8Encoding($false)
- Git 对中文文件名显示为转义八进制（`\344\270...`），属正常显示问题，文件本身没事

## 8. 备份与回滚

```
D:\_EEG_migration_backup\
├── EEG_20261004_004541.tar.gz      51 文件（解包 md5 反向比对已验证可恢复）
├── EEG_baseline_20261004_004541.md5
├── S_20261004_004541.tar.gz        3 文件（16 号，已取消项目）
├── S_baseline_20261004_004541.md5
└── _回收站_20261004_*\              16 号 3 文件的第二份保险
```
三个原件 `.bat` 的基线 md5：`8477768f…` / `77414491…` / `d0e54325…`（在 EEG_baseline 文件里）。

## 9. 记忆体系（新 agent 的接续指引）

| 层级 | 文件 | 读法 |
|---|---|---|
| 用户级 | `C:\Users\wshix\.workbuddy\MEMORY.md` | 跨项目习惯与规则（含大学发展策略：GPA>科研>竞赛、项目 4-6h/周、期中断崖线） |
| LabPulse 项目级 | `.workbuddy\memory\MEMORY.md`（本空间） | **先读这个**，再读最近的日报 |
| EEG 项目级 | `EEG\.workbuddy\memory\MEMORY.md` | 涉及科研侧时读；其中「空间边界」一节记了拆分契约摘要 |
| 日报 | 两空间各自的 `YYYY-MM-DD.md` | 做完实质工作后追加，勿覆盖 |
| 迁移细节 | 本空间 `迁移执行报告_2026-10-04.md` | 为什么要拆、怎么拆的、校验了什么 |

**跨空间引用规矩**：只写「路径 + 摘要 + 最后核对日期」三件套，不复制正文。

## 10. 新 agent 的开工第一步（建议）

1. 读本空间 `.workbuddy\memory\MEMORY.md` 和 `2026-10-04.md` 日报
2. 向用户确认三件事：设备验收结果如何（#7）；Stage 1 除文档外是否还要可运行 demo（影响 #1 的范围）；本周项目投入时间（用户铁律 4-6h/周，期中临近需防过载）
3. 得到答复后，从待办 #1 动手：Streamlit 六模块骨架，第一版只跑公开数据集，不接硬件
4. 每次实质性改动后：`git add -A && git commit`，并在 `AI使用日志.md` 补一行

---

*文档结束。如与本文件有出入，以磁盘实际状态 + git log 为准，并顺手修正本文件。*
