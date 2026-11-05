# LabPulse：ExpandableEEG 离线联调笔记

资料核对：2026-11-05｜对应 FR-01、FR-02｜实机尚未验证

用户提供了以下四条 B 站直链。本次访问未能读取视频正文或字幕，公开信息接口返回 HTTP 412。下表中的关注点按标题和项目需求整理；后面的操作步骤来自设备说明书和 OpenBCI 官方文档。

| 视频 | 后续重点核对 |
|---|---|
| [教程 1：OpenBCI GUI 使用简介](https://www.bilibili.com/video/BV1zNoRBoEce/) | 设备选项、会话启动和录制文件位置 |
| [教程 2：OpenBCI GUI 控件介绍、专注度检测](https://www.bilibili.com/video/BV1mKo9BMEGC/) | Networking、Marker、Packet Loss 是否出现及其设置；专注度指标不用于 ErrP |
| [教程 5：湿电极使用指导及 SSVEP 实验](https://www.bilibili.com/video/BV1n89DBVEuC/) | 湿电极佩戴与接触质量；SSVEP 范式不用于 ErrP |
| [一个脑机接口设备三种通信方式](https://www.bilibili.com/video/BV17u9iBhEAs/) | 核对通信模式、是否保留外网、16 通道实际输出率；模式名称和配置以说明书与实机为准 |

| 核对项 | 资料支持 | 现场如何检查 |
|---|---|---|
| 实时脑电 | 随机说明书第 6、9 页给出 Networking → LSL；标准 OpenBCI GUI 文档提供 Python 接收示例 | 用已能采集的设备配置启动会话；若 Networking 可选 LSL，输出 Time Series，并记下流名称、类型及显示的采样率。开启输出不等于 Python 已收到 |
| 手动标记 | 随机说明书第 6 页称测试版有 Marker；标准 OpenBCI GUI 文档说明其 CSV 可保存 Marker Channel | 在同一会话点几次 Marker，记录点击顺序和数值；停止后检查本机导出的 CSV/BDF 是否包含相应标记。界面出现竖线不等于文件保存成功 |
| 程序标记 | 标准 OpenBCI GUI 支持 Marker 的 UDP 输入，尚未确认探脑科技修改版也支持 | 若界面有 Receive IP/Port，记下选项；没有就记录版本，不升级固件、不照其他板卡说明接线 |
| 采样率与同步 | 厂商官网列 Wi-Fi 下支持 250/500/1000 Hz；没有给出本机 EEG 与物理事件的对齐误差 | 记录配置、观测采样率与丢包；同步误差留待独立参考测量。手动打标只验证记录链路 |

现场最小证据：GUI 版本、Networking 与 Marker 截图、一段原始导出、标记顺序、失败时的完整报错。GitHub 已有 `scripts/run_lsl.bat`，但它是启动器，依赖仓库外的科研空间脚本和本机 Python；请在断网前确认这两项存在。若依赖尚未就绪，先完成 GUI 检查。原始 EEG 留本地；公开归档仅放经检查的脱敏记录。

资料入口：[B 站教程索引](https://search.bilibili.com/all?keyword=Yicb) · [探脑科技官网](https://www.seekbci.com/) · [OpenBCI Networking](https://docs.openbci.com/Software/OpenBCISoftware/GUIWidgets/#networking) · [OpenBCI Marker](https://docs.openbci.com/Software/OpenBCISoftware/GUIWidgets/#marker)。设备侧优先核对用户提供的《ExpandableEEG 使用说明书》和当前 GUI。
