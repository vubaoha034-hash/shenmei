本目录保存 2026-10-06 的真实插件连接验证及原生状态修复证据。它是证据目录，不是第二套任务状态。

从仓库 `START_HERE.md` 进入，读取当前 `continuity/vpd/CURRENT_TASK_LOCK.json` 及其 `codex_takeover.receipt`。本轮恢复后的锁版本为 353、检查点为 375；业务阶段和下一动作按原生文件执行。作品与复用入口继续由 `continuity/vpd/codex_takeover_20261003/S7_FINAL_REUSE.md` 和当前 receipt 定位。

- [实际连接结果](VERIFICATION_RESULT.json)：初始化请求真实返回 HTTP 401；未成功调用线上工作流、保存反馈或读取反馈。发布状态不能替代连接成功。
- [真实用户反馈](HUMAN_S7_POSITIVE_FEEDBACK.json)：保存“我觉得很不错，而后现在验证”的原话及 S7 作品绑定；这是仓库观察记录，尚未写入插件线上反馈库。
- [独立远端回读](STAGE_CORRECTION_PUBLICATION_READBACK.json)：审核提交 `7979533e66f29bba23bd33dd9a9a38ead6762ef7`，限定元数据、五份远端原字节和 Git 对象比较的保存验证通过；不是新的像素评测或插件连接通过。原字节 SHA256：`df2896c31afbf1126b879cde5ea095afce703f6e6f2451158fe7d28cbbb8f679`。
- [阶段标签修复](STAGE_METADATA_CORRECTION.json)与[保留的失败回读](PUBLICATION_READBACK_1c09621_STAGE_DIFFERENCE.json)：主执行者误用状态卡显示标签，独立回读发现后恢复实际原生字段；旧失败记录未改写。

连接验证的下一操作：用户在 ChatGPT 的 Plugins → Personal → Created by you 安装并连接“刘先生·视觉设计工作流”后，先实际调用只读工作流，再将这条真实反馈保存并按作品与版本回读。缺少连接时保留阻塞，不能降低身份校验、伪造调用或把本地测试冒充生产验证。这项操作不改变业务主线，也不授权新增风格、出图、付费资源或自动任务。
