# LabPulse：ExpandableEEG 离线联调笔记

资料核对：2026-11-05｜对应 FR-01、FR-02｜实机尚未验证

复查已从四条 B 站原页面读到标题、简介和时长。现已检查用户提供的教程 2 和通信方式本地片段，只看画面与画内字幕，未分析音频。下文时间以本地片段为准。

| 视频 | 页面已核实 | 后续重点核对 |
|---|---|---|
| [教程 1：OpenBCI GUI 使用简介](https://www.bilibili.com/video/BV1zNoRBoEce/) | 1:53；ExpandableBCI 搭配干电极，介绍基本 GUI 操作 | 设备选项、会话启动和录制文件位置 |
| [教程 2：OpenBCI GUI 控件介绍、专注度检测](https://www.bilibili.com/video/BV1mKo9BMEGC/) | 9:34；简介明确列出控件说明与数据传输 | Networking、Marker、Packet Loss 是否出现及其设置；专注度指标不用于 ErrP |
| [教程 5：湿电极使用指导及 SSVEP 实验](https://www.bilibili.com/video/BV1n89DBVEuC/) | 8:12；简介确认使用 ExpandableBCI | 湿电极佩戴与接触质量；SSVEP 范式不用于 ErrP |
| [一个脑机接口设备三种通信方式](https://www.bilibili.com/video/BV17u9iBhEAs/) | 5:11；简介未列出模式名称或配置 | 核对通信模式、是否保留外网、16 通道实际输出率；模式名称和配置以说明书与实机为准 |

## 视频核对结果

- 通信片段 **00:10–00:33、00:46–00:52**：蓝牙、Wi-Fi AP、Wi-Fi Client 三种模式。默认 AP 由板卡提供热点，电脑连接；GUI 的设备 IP 示例为 `192.168.4.1`。1000 Hz 字幕出现在 8 通道语境，不能作为本机 16 通道实测证据。
- 通信片段 **00:36–00:44、00:54–01:10**：通过 USB Type-C 数据线和 ExpandableEEG 配置工具连接板卡。Client 示例让板卡加入路由器，再打开配置工具查看板卡 IP。日后如需同时使用外网，可在允许使用的局域网测试 Client，验证电脑和板卡能否互通，以及电脑能否同时联网。首次联调可沿用已能采集的 AP。
- 通信片段 **01:20–01:46**：蓝牙配对后，在 Windows 的更多蓝牙设置找传出 COM 口，GUI 用 Serial → Manual 选择本机端口。视频的 COM5 是示例。
- 教程 2 **约 00:44–00:56、02:16–02:20**：Networking 面板显示 LSL、Data Type、Name、Type 和 Start LSL Stream；菜单可见 TimeSeriesRaw。本机有同名选项时，可用它测试原始时序输出。视频未验证 Python 接收 16 通道。
- 教程 2 **约 02:31–02:44**：控件菜单可见 Packet Loss 和 Marker；Marker 面板有 Insert 1–8、Receive IP/Port，示例接收 IP 为 `127.0.0.1`，与板卡 IP 不同。视频未验证外部发送格式、实际导出是否保留标记，或 LSL 脑电流是否携带标记。

| 核对项 | 资料支持 | 现场如何检查 |
|---|---|---|
| 实时脑电 | 随机说明书第 6、9 页给出 Networking → LSL；标准 OpenBCI GUI 文档提供 Python 接收示例 | 用已能采集的设备配置启动会话；若 Networking 可选 LSL，输出 Time Series，并记下流名称、类型及显示的采样率。开启输出不等于 Python 已收到 |
| 手动标记 | 随机说明书第 6 页称测试版有 Marker；标准 OpenBCI GUI 文档说明其 CSV 可保存 Marker Channel | 在同一会话点几次 Marker，记录点击顺序和数值；停止后检查本机导出的 CSV/BDF 是否包含相应标记。界面出现竖线不等于文件保存成功 |
| 程序标记 | 标准 OpenBCI GUI 支持 Marker 的 UDP 输入，尚未确认探脑科技修改版也支持 | 若界面有 Receive IP/Port，记下选项；没有就记录版本，不升级固件、不照其他板卡说明接线 |
| 采样率与同步 | 厂商官网列 Wi-Fi 下支持 250/500/1000 Hz；没有给出本机 EEG 与物理事件的对齐误差 | 记录配置、观测采样率与丢包；同步误差留待独立参考测量。手动打标只验证记录链路 |

现场最小证据：GUI 版本、Networking 与 Marker 截图、一段原始导出、标记顺序、失败时的完整报错。GitHub 已有 `scripts/run_lsl.bat`，但它是启动器，依赖仓库外的科研空间脚本和本机 Python；请在断网前确认这两项存在。若依赖尚未就绪，先完成 GUI 检查。原始 EEG 留本地；公开归档仅放经检查的脱敏记录。

资料入口：[B 站教程索引](https://search.bilibili.com/all?keyword=Yicb) · [探脑科技官网](https://www.seekbci.com/) · [OpenBCI Networking](https://docs.openbci.com/Software/OpenBCISoftware/GUIWidgets/#networking) · [OpenBCI Marker](https://docs.openbci.com/Software/OpenBCISoftware/GUIWidgets/#marker)。设备侧优先核对用户提供的《ExpandableEEG 使用说明书》和当前 GUI。
