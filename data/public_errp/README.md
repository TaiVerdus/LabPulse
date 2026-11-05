# 公开 ErrP 数据索引

用于本地软件研究，不是 LabPulse 自采 EEG。原始文件不进入本仓库。

来源：https://github.com/stefan-ehrlich/dataset-ErrP-HRI

固定版本：`4bc3e52469934aa0551a2261a6e4e899d156c28f`。

本地缓存：robot/s02_robot.set、s02_robot.fdt、s03_robot.set、s03_robot.fdt，以及作者数据说明 PDF。下载量约 119 MB。重建命令：`.venv\Scripts\python.exe -m offline.fetch`，联网一次，后续回放不联网。下载器记录 URL、文件长度和 SHA256；索引副本见 reports/offline/data_manifest.json。

出处：Ehrlich, S. K., & Cheng, G. (2019). A feasibility study for validating robot actions using EEG-based error-related potentials. International Journal of Social Robotics, 11(2), 271–283. DOI: https://doi.org/10.1007/s12369-018-0501-8 。数据说明修订于 2019-03-23。未确认独立数据再分发授权，因此只提供来源和下载脚本，不在 LabPulse 重发原始记录。

文件为连续 EEGLAB SET/FDT，256 Hz，30 个存储通道，其中 3 个为 EOG。外部 FDT 按小端 float32、逐采样通道顺序读取。EEGLAB 幅度按 µV 解释；设备自采数据需另外核对单位。排除 EOG 后 27 通道，不代表本人的16通道设备。

每个方向反馈 FB1/FB2/FB3 为取窗锚点，S4 正常、S5 人按错、S6 机器出错。按 S9 试次结束标记匹配反馈与条件，不能简单把“后一个标记”当真值：实测部分 S4/S6 比 FB 早不足一个采样间隔。排除 S5，真值不进入特征。机器人转头和颜色边框反馈可能构成混杂；本基线不能证明检测到了特异的 ErrP。
