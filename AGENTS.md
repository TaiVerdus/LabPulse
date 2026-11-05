# LabPulse 项目约定

- 项目名称：LabPulse。
- 权威 GitHub 仓库：https://github.com/TaiVerdus/LabPulse 。
- 用户要求所有项目产物归档到此仓库；文档、代码、配置模板、验证记录和演示材料应纳入版本管理。大文件按 GitHub 适用方式管理，并在仓库中提供索引。
- 提交前检查个人信息、原始脑电数据的公开授权、实验室保密材料与密钥；不默认公开这些内容。可提供脱敏数据、数据说明与获取方式。
- 课程 Project Documentation Guidelines 优先于参考网站模板。文档用中文 Markdown。
- 当前三份文档为未经完整阶段确认的初稿：01-Proposal.md、02-MVP-PRD.md、03-Technical-Design.md。沿用已有信息继续澄清，不把建议指标或未运行命令当作已验证事实。
- 后续修订统一使用 LabPulse 名称。需求、设计与验证证据保持关联；明确实时、回放、模拟以及真实 Jarvis 接入与本地测试桩的区别。
- 当前工作区尚无提交、尚未配置远程仓库（2026-10-22 检查）。上传前先检查目标仓库已有内容，避免覆盖远程历史；完成上传后核实远程状态再报告成功。
- 2026-11-05：用户要求机械臂后放、完成无设备任务。新增工具入口为 OFFLINE-START.md；不覆盖远程 deliverables 中已冻结课程稿。不修改 D 盘科研空间 acceptance_check.py。
- offline/pipeline.py 的公开数据回放、offline/stream.py 的合成 LSL 与本人实时设备数据必须分别记录。原始数据、wheelhouse、环境和模型留本地，提供来源、哈希及重建方法。BAT 使用 CRLF。
