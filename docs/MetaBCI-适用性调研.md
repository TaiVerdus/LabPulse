# LabPulse：MetaBCI 适用性调研

2026-11-05｜资料及源码核对，未安装或实机测试｜涉及 FR-01～03、NFR-01

**建议：把 MetaBCI 用作参考框架，暂不纳入第一次硬件联调的必装依赖。** 先沿用 ExpandableEEG → OpenBCI GUI → LSL → 本机接收程序，留存原始时间戳；再用外部 ErrP 数据跑离线流程。只有需要复用在线缓冲和事件切窗时，再单独试用 MetaBCI。

| 模块 | 官方示例/用法 | 对 LabPulse 的用途与边界 |
|---|---|---|
| brainda | P300 示例加载 Cattan_P300，注册预处理钩子，取出 X、y、meta 后训练及验证 | 学习事件切窗、数据与标签组织；示例的拼写任务标签、双向滤波和指标不直接移植到实时 ErrP |
| brainflow | LSLapps 通过 pylsl 接数据流与标记流；还有针对若干厂商设备的采集接口 | 可参考数据缓冲与标记映射；未见 ExpandableEEG 专用驱动。MetaBCI 的同名子模块与独立 BrainFlow 库不是一回事 |
| brainstim | PsychoPy 实验界面及范式组织 | 可用于未来屏幕模拟场景；真实机械臂事件起点仍要由 LabPulse 记录并独立校准 |

## 接入和同步

源码中 LSLapps 接收规则包含规则采样数值流，以及名为 Markers 类型的独立标记流（期望非规则采样、字符串格式，值能转换为整数）。源码用事件时间在一批 EEG 样本中找位置，输出时以标记列替换时间戳列。初次联调只开一条明确命名的 TimeSeriesRaw 输出，检查真实通道数、观测采样率、连续性及丢包。本机 GUI 的 Marker 按钮、UDP 输入、导出标记和独立 LSL Markers 流应分别验证，不能假定互通。

保留 EEG 和事件的原始时间戳、时钟域及校正记录。软件把事件放到某个样本上不等于已经测出相对物理事件的误差；不能以标称 1000 Hz、LSL 时钟校正或匹配到采样点作为 NFR-01 通过证据。

## 数据和实施顺序

MetaBCI 是统一数据加载、解码、实验和在线处理的 Python 平台。核对官方公开数据加载目录和 demos，未发现现成 ErrP 加载器或演示，不排除另有独立或未公开资源。P300/SSVEP 可用于学习框架，不能当作错误感知标签。候选外部数据首选 Ehrlich 与 Cheng 的 ErrP-HRI（机器人与光标观察条件），另有 BNCI 2015-013（观察自主光标）。先读数据说明和使用条件，仅下载所需样例。离线验证读取、切窗、标签及基线，按块或会话划分，记录拒判与误报；外部数据成绩不证明本机或湿实验识别性能。

1. 现有 AP 模式下做同机 LSL 与 Marker 验收。断网前确认接收程序、Python 依赖能启动，录制文件保留本地。
2. 用外部 ErrP 样例单独测试事件切窗、模型及本地提示；证据标记为回放。
3. 获得本人受控数据后，再验证对齐误差和独立试次分类；如确需 MetaBCI，参照发行说明在独立环境仅安装所用模块，例如 `metabci[brainflow]`。尚未执行安装或验证。Jarvis 继续使用单独的消息接口。

来源：[天津大学平台发布](https://www.tju.edu.cn/info/1026/6938.htm) · [使用文档](https://metabci.readthedocs.io/en/latest/) · [安装与版本说明](https://github.com/TBC-TJU/MetaBCI/releases) · [数据加载器目录](https://github.com/TBC-TJU/MetaBCI/tree/master/metabci/brainda/datasets) · [示例目录](https://github.com/TBC-TJU/MetaBCI/tree/master/demos) · [P300 示例](https://github.com/TBC-TJU/MetaBCI/blob/master/demos/P300_demo.py) · [LSL 源码](https://github.com/TBC-TJU/MetaBCI/blob/master/metabci/brainflow/amplifiers.py#L798-L965) · [Brainstim API](https://metabci.readthedocs.io/en/latest/python_apis/metabci.brainstim.html) · [ErrP-HRI](https://github.com/stefan-ehrlich/dataset-ErrP-HRI) · [BNCI 2015-013](https://nemar.org/dataset/nm000168?v=v1.0.2)。
