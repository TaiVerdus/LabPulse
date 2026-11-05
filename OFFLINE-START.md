# LabPulse：无设备工具入口

2026-11-05 新增。机械臂和 Jarvis 按用户要求后放。

- 双击 `scripts/run_offline.bat`：公开 ErrP 数据训练、独立评价、回放提示。
- 打开 `reports/offline/report.html`：无需服务器或网络，查看结果并逐条播放预测。
- 双击 `scripts/check_offline.bat`：依赖、逻辑测试、本机合成 LSL 流检查。
- 双击 `scripts/practice_screen.bat`：无 EEG 的屏幕练习；GUI 体验待人工检查。
- 详细步骤：[无设备阶段操作手册](docs/无设备阶段操作手册.md)。
- 结果：[验证结果](reports/offline/验证结果.md)；局限和失败记录：[决策记录](docs/无设备阶段决策记录.md)。

本机数据与依赖已缓存，但 GitHub 不含这些原始数据和安装包。重新克隆时，先按照操作手册准备环境及数据。`reports/offline/data_manifest.json` 和 `wheel_manifest.json` 提供来源/文件哈希；安装命令见 `requirements-offline.txt` 和手册。训练模型 `baseline.joblib` 是本机生成物，可重跑生成，勿加载不可信 joblib。

公开数据回放、合成流联调、本人设备实验是三类不同证据。目前前两项已执行；本人实时 EEG、物理同步、个人模型及真实 Jarvis 均未验证。屏幕练习不作为 ErrP 正式范式。保留课程已提交文档；旧课程材料中不同研究范围不在本轮静默改写。
