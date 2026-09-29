# VPD 请求校验分发补丁（2026-09-29）

在状态对齐提交 `2ba4140fbb824aedaa87bb6354727ef5bda9f86e` 之后，复查发现 `scripts/verify_visual_memory.py --vpd-state --status-card` 走当前 `p6-composition/v1`，但附加 `--request` 时 `validate_request()` 二次调用的 `vpd_task_lock.validate_state()` 仍路由到 legacy 状态。症状是只读状态可读、请求前校验被旧入口误阻。

修正提交 `3da78492a1ffe6105a88376df0546a9a731ccc9a` 在既有状态分发增加 `p6-composition/v1` 分支，不改任务锁、检查点、图像、Figma 或人工 verdict。定向验证：同一当前锁下只读请求通过；带 `changes=['new_figma_canvas_write']` 的请求被 `SCOPED_CHANGE_AUTHORITY_REQUIRED` 拦截；状态卡仍为 `VPD_STATE_VALID_REVIEW_ONLY`，Figma 227:2 继续等待真人像素评审。
