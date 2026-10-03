# scripts（课程空间 LabPulse）

> **本目录不含脚本主本。** 验收算法内核 `acceptance_check.py` 的 canonical 在科研空间：
> 相对路径 `..\EEG\scripts\acceptance_check.py`
> 绝对路径 `C:\Users\wshix\WorkBuddy\EEG\scripts\acceptance_check.py`
>
> 契约全文见 `C:\Users\wshix\WorkBuddy\EEG\SHARED_DEPS.md`。

## 这里的三个 .bat 是什么

它们是**启动器副本**，不是脚本本体。双击后会自动定位到科研空间的脚本主本并执行，
所以你不需要关心文件在哪台目录里——只要科研空间还在 `C:\Users\wshix\WorkBuddy\EEG`，
双击就能跑。

| 文件 | 作用 | 什么时候用 |
|---|---|---|
| `run_demo.bat` | 用公开脑电数据跑一遍验收流程（练习/对照） | 学工具、看正常输出长什么样 |
| `run_file.bat` | 分析一个录好的数据文件（把文件**拖到它图标上**即可） | 设备录完一段后做体检 |
| `run_lsl.bat` | 收实时数据流，测采样率与丢样 | GUI 已连机并打开 LSL 后 |

## 使用注意

- 双击即可，不需要懂命令行
- 如果看到「找不到验收脚本主本」的提示：说明科研空间被移动了，
  用记事本打开对应的 `.bat`，改第 6 行 `set "CANON=..."` 指向新的 scripts 目录
- **不要**往这里复制 `acceptance_check.py`，也不要在这里改算法——
  算法只有一个主本，在科研空间
