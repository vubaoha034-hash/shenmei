# 新参考入口修复

用户在“修改地图文字”聊天上传 `1000031560.jpg`（最长的旅途），要求主标题“地图以外”，英文“for liuxiansheng”。0.1.1仅支持原生山野集参考，错误地把一次新参考请求也挡在原生参考哈希门外；实际原图为金色摄影与大书法标题，不能套山野集的绿底文字模板。

0.1.2增加 `compile_transfer_plan(reference_scope:"user_request", reference_source:本次附件定位, new_copy:准确新文案)`。SHA未知可以不传；不得编造。SHA即使提供，也只是调用者声明，插件标记 `NOT_PERFORMED`，不声称看过像素。原生模式默认不变，仍需原生参考SHA；新请求不会改原生参考、摄影、任务锁或配额。插件自身不生成图，也不把草稿或工程测试当成审美通过。

ChatGPT先读 `plugins/visual-aesthetic-workflow/REQUEST_REFERENCE_RUNTIME.json` 的真实发布/运行证据和 `v0.1.2/SKILL.md`。旧 `CURRENT_RELEASE.json`、S7入口及0.1.1保留原字节，属于历史。后续实际制作仍按用户当前授权调用图片工具，真实看图，独立审稿、Figma重建与Drive原件保存；本次只修插件，不生成“地图以外”海报。

证据：`REQUEST_AND_DIAGNOSIS.json`保存实际聊天、附件身份与源代码原因；`BASELINE_REPRODUCTION.json`实际复现旧版409（本地工程运行）；新源码与冻结清单在 `plugins/visual-aesthetic-workflow/v0.1.2/`。真实部署、ChatGPT调用、独立工程审查及原生回执在本目录后续文件中，以实际保存结果为准。工程审查不是视觉冷审。

原项目唯一下一动作继续为 `LIU_REVIEW_LIUXIANSHENG_CONTENT_TRANSFER`。本次插件修复未替换原生审稿载体，未改变S7真人PENDING、茶作29/28或认可摄影7fd7777f。

实际结果：同一Site第4版发布成功，源码535a61558e3154b644f60b7b643566a94f1ea86f；ChatGPT管理→刷新工具返回新schema，原生重新连接完成。新聊天 https://chatgpt.com/c/6ac4d667-64d0-83ea-a6a6-782cf1719f03 的实际api_tool.call_tool输入与原始工具响应前缀已核对，DRAFT_USER_REQUEST、准确主标与英文、NOT_PERFORMED、native_reference_rebound:false已验证；网络结果截断，完整尾部及全输出哈希未验证。生产同时间POST /mcp为200。原“修改地图文字”仍三次报告内部错误，未恢复；不能借用新聊天通过冒充旧聊天通过，后续使用已验证新入口。新聊天只有参考locator，原附件像素读取及附件迁移未验证，出图前必须解决。

独立工程审查实际只读55项及13探针通过；实现者56项本地测试通过。两者不作托管连接、审美或真人认可；真实ChatGPT调用由Root另行取证。Windows原生打包采用官方prepare-site-build不改写的薄适配，实际6文件归档哈希核验由Root执行，独立归档审核因agent thread limit reached未运行，不称独立通过。官方WSL/Git Bash两次真实失败保留，未无限重试。未测试生产反馈落库，不启动自动化；本轮没有制作新作品或证明视觉改善。
