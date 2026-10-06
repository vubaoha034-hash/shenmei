# 刘先生·视觉设计工作流：实际安装验收

2026-10-06已在用户当前ChatGPT账户完成安装和OAuth连接。真实详情页显示“已安装”“已连接”和“在聊天中试用”，见ACTUAL_UI_INSTALLATION.json。安装前的HTTP401及资料授权拦截作为历史保留；用户明确回复“授权，”后才选择账户并允许向本人插件分享基本资料。

已核验至少一次真实get_current_workflow：调用消息和author.role=tool原始结果前缀来自既有ChatGPT对话的HTTP200响应，不以助手自述代替调用证据。它读取c19970b76cb2e30b037c55016ceb5f54b29a887c，原生锁353、检查点375，阶段LIUXIANSHENG_REFERENCE_TYPOGRAPHY_CONTENT_TRANSFER_EXPERIMENT，唯一下一动作LIU_REVIEW_LIUXIANSHENG_CONTENT_TRANSFER。见ACTUAL_TOOL_PROOF.json及独立补充审查。网络检查器截断了长响应，因此只证明实际保存的调用和结果字段；第二次调用自述不计入验证。

实际入口：[插件详情](https://chatgpt.com/plugins/plugin_asdk_app_sites_e3827109d9348191a163f8f785ef2b4c?directoryTab=personal)，名称“刘先生·视觉设计工作流”。打开“在聊天中试用”，或在新ChatGPT聊天用@选中此插件，请它调用get_current_workflow。然后以同提交原生锁为准恢复工作；不能从旧聊天的下一动作推进。实际只读验收聊天：[插件验收核验](https://chatgpt.com/c/6ac4c047-1148-83ea-b408-5f39d5d50ab7)。

源码发布0.1.1、Site发布3、插件UI显示1.0.0是不同版本维度。CURRENT_RELEASE.json保留发布时“连接未验证”的原始历史；最新连接证据由CONNECTION_VERIFICATION.json及当前原生回执绑定。没有重写上游稳定实现、重新创建插件、伪造已安装Skill或把ZIP当安装成功。

本次只读验收实际ChatGPT配置gpt-5-6-thinking / max（存储调用metadata），没有声称切换为Sol。Root本机配置gpt-6.1-sol / xhigh；子代理实际配置看其运行证据。插件四个工具尚未在当前Codex Root/旧子代理工具目录出现，这不否定已核验的ChatGPT运行，亦不声称它能在当前Codex会话直接调用。

本轮未生成图片、未写Figma或Drive、未新建正式作品，未生产写入反馈。save_human_feedback/get_human_feedback的生产写入回读仍未验证。已认可摄影、S7交付身份、全部失败、计数、审核载体和主线不变。插件提供现有工作流入口与反馈接收，独立实际像素审核仍通过原生载体执行；不宣称安装使审美自动提升。

原生入口START_HERE.md → CURRENT_TASK_LOCK.json → 当前receipt → S7_FINAL_REUSE.md。唯一业务下一动作仍是刘先生审核S7文字迁移；正向评价是原话观察记录，正式真人验收状态不擅自改判。

S7_FINAL_REUSE.md为原生迁移证据中的冻结入口，保留原字节和当时连接未验证的历史文字。最新安装状态从START_HERE.md及当前原生receipt的current_plugin_connection_verification读取，旧S7说明不覆盖后续实际连接证据。
