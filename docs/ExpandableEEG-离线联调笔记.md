# LabPulse：ExpandableEEG 离线联调笔记

资料核对：2026-11-05｜对应 FR-01、FR-02｜实机尚未验证

在 B 站检索到《脑机接口教程2：OpenBCI GUI使用-各个控件介绍、专注度检测》的索引，部分结果显示作者为探脑科技。未能读取视频正文或字幕，不能将以下步骤归为视频内容。也检索到同系列设备的《8-32通道可扩展脑电采集设备〈ExpandableBCI〉初步介绍》转载页面；未核实原视频。

| 核对项 | 资料支持 | 现场如何检查 |
|---|---|---|
| 实时脑电 | 随机说明书第 6、9 页给出 Networking → LSL；标准 OpenBCI GUI 文档提供 Python 接收示例 | 用已能采集的设备配置启动会话；若 Networking 可选 LSL，输出 Time Series，并记下流名称、类型及显示的采样率。开启输出不等于 Python 已收到 |
| 手动标记 | 随机说明书第 6 页称测试版有 Marker；标准 OpenBCI GUI 文档说明其 CSV 可保存 Marker Channel | 在同一会话点几次 Marker，记录点击顺序和数值；停止后检查本机导出的 CSV/BDF 是否包含相应标记。界面出现竖线不等于文件保存成功 |
| 程序标记 | 标准 OpenBCI GUI 支持 Marker 的 UDP 输入，尚未确认探脑科技修改版也支持 | 若界面有 Receive IP/Port，记下选项；没有就记录版本，不升级固件、不照其他板卡说明接线 |
| 采样率与同步 | 厂商官网列 Wi-Fi 下支持 250/500/1000 Hz；没有给出本机 EEG 与物理事件的对齐误差 | 记录配置、观测采样率与丢包；同步误差留待独立参考测量。手动打标只验证记录链路 |

现场最小证据：GUI 版本、Networking 与 Marker 截图、一段原始导出、标记顺序、失败时的完整报错。GitHub 已有 `scripts/run_lsl.bat`，但它是启动器，依赖仓库外的科研空间脚本和本机 Python；请在断网前确认这两项存在。若依赖尚未就绪，先完成 GUI 检查。原始 EEG 留本地；公开归档仅放经检查的脱敏记录。

资料入口：[B 站教程索引](https://search.bilibili.com/all?keyword=Yicb) · [探脑科技官网](https://www.seekbci.com/) · [OpenBCI Networking](https://docs.openbci.com/Software/OpenBCISoftware/GUIWidgets/#networking) · [OpenBCI Marker](https://docs.openbci.com/Software/OpenBCISoftware/GUIWidgets/#marker)。设备侧优先核对用户提供的《ExpandableEEG 使用说明书》和当前 GUI。
