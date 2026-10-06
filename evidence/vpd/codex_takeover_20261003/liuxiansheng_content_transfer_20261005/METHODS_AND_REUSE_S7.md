# 刘先生：参考文字迁移与 ChatGPT 工作流入口

仅用于当前山野集文字→刘先生实验。先读 START_HERE.md 与原生 CURRENT_TASK_LOCK/LATEST_CHECKPOINT/PROJECT_CONTROL_ADAPTER，再读 DELIVERY_MANIFEST_S7.json。历史下一动作不覆盖当前锁。原茶作主线、受保护摄影与真人否决均保留；本轮没有生成摄影、图稿或新茶作版本。

实际工作流：读真实参考与冻结文案 → Image 图稿（本轮复用 G4，未新增调用）→ Figma 曲线及12个原生辅助文字 → 新隔离两图像素审核 → 有限必要修复/重新导出 → Drive 原件回读 → Root 原生保存 → 真人审核。审稿 worker 无业务状态写权和主线变更权。AI通过只是允许送交刘先生。

S7实际源位于 Figma uyDxOoN1iNDPpEHTKSUWg1 / page412:2 / frame453:10 / wordmark453:37。成品960×1280，PNG SHA ed03ba67ca82da6920e49ab44f42f73f112d8c9bc25b841cb47ebcfc7a583762。Drive PNG 1svX-5kyxGBA-hEKg6iq_xMaxcwYU0Ubt，SVG15COp7aWZ7sKWKDinV3KasEQ38lVzt0e5，原字节回读一致。参考R9a29fbdc…、G4图稿9ef09dd1…、SVG b721b2a7…各自用途不同，不能用图稿替代最终原件。

字标由图稿恢复的14个正形笔画继续作局部塑形；S7只修订5个指定轮廓，其余9条与S6同字节，橙色4条路径保留穿插。参考真实8×8供体264个，固定映射到5档浅/深磨损；JPEG亮度转为设计透明度，不声称恢复未知原始印刷版或原字体。主标9个VECTOR（5层奶白+4橙）可编辑曲线，不能直接改字为另一个名字；12个TEXT可直接编辑，文字更改仍需重排与新评测。

试验保留成熟 VTracer0.6.15、skia-pathops0.9.2、sharp 上游，未改其核心。详见 guide-adapter-s7/SOURCE.json、DEPENDENCIES.json、REUSE_METHOD.json 及许可。VTracer polygon 把单像素成分输出为零面积路径，五次真实失败保留于 technical-failures/polygon-refuted。最终用固定精确像素网格替代这一次转换步骤，没有重新阈值搜索或增加图稿。实际内部38827像素透明度匹配，12个外曲边抗锯齿偏差记录；几何/字节证据不等于审美质量。

Figma单次脚本超过50000字符被拒绝，未写画布；实际以7个隐藏临时TEXT传输同一SVG，复合长度/FNV核对后完成唯一正式导入，再删除全部临时节点。guide-adapter-s7/figma-transport 保留源码与回执。原七个研究/迁移版本属性指纹一致、V29摄影属性一致，S6→S7字标区域以外像素差为0。属性子集指纹不是所有Figma内部元数据的证明。

新的隔离Sol/Max审核实际读R/T像素，CONTENT_TRANSFER_PASS_WITH_LIMITATIONS，P1为空；保留P2：部分长直边/橙线较规整、均匀撒点感、辅助手写句节奏及参考差距。S5/S6独立FAIL不删除。唯一有效S7评测是 s7_final_verified_review；s7_verified_review、s7_verified_review_transport_bound 为被反证否定的保存适配基线，不能用于送审判定。Root初次调度漏了严格JSON信封字段，且两次spawn实际失败：S7专用适配明确补充schema/scope、R/T布尔转换并只认成功spawn，不改判词和证据，原runtime/core不变，不能声称规范化报告逐字等于原审稿。当前适配核对actual input_image原字节、全部载体恰2图、完整原审稿字段一致；失败源码和反证在 s7_review_adapter_failed_baseline。脚本 scripts/vpd_collect_s7_content_transfer_review.py；这项协议适配须以实际专业反证报告为准。

跨上下文重建所需11个冻结输入（含6个二进制掩模）另存为Drive原件包 1QPaUkMUZZ8VJOs1ab8A3RqG89KBW8THq，SHA535cae9b6f7367ed3faf328c040a1d856b1bdb75962db6992890eba040f28861，51692字节。DRIVE_REBUILD_INPUTS_S7.json记录原件回读。先用 guide-adapter-s7/restore-source-inputs.py --root <checkout> --archive <原件zip> --destination <checkout>/.liu-visual-private/<新目录> 校验并恢复11个输入，再按REUSE_METHOD.json用明确--root/--output-dir重建。不得运行旧失败polygon代码；PNG输入不进Git，不能只克隆仓库便声称已恢复二进制依赖。已有SVG可直接从Drive恢复和Figma编辑；诊断脚本中的旧私有绝对路径不具跨机器可用性。

ChatGPT插件“刘先生·视觉设计工作流”已私有发布：[查看](https://liu-visual-workflow-20261006.deemoliul.chatgpt.site)，MCP路径 /mcp。官方Sites0.1.75工作流及身份机制未改；项目薄适配0.1.0为实验版本，不冒充成熟中文品牌技能。根入口 plugins/visual-aesthetic-workflow/SKILL.md、README.md；实际生产源码镜像315e945f…，plugin_evidence/SOURCE_PROVENANCE.json/ACTUAL_PUBLICATION_RECEIPT.json 绑定版本。

安装后首先调用 get_current_workflow 读取最新原生提交；compile_transfer_plan 只生成调用草案；save_human_feedback 仅保存绑定作品/提交的追加反馈，必须返回persisted:true，再用 get_human_feedback核对。反馈不是第二权威状态系统，只有Root合并到原生账本。插件不自带生图/Figma/Drive/独立评测工具，不会自行后台训练、定时运行或修改主线。

安装建议卡已提供，连接未核验。当前4个生产HTTP探测均被平台401拦截，不是成功MCP握手或真实D1反馈写入。保持自有私有权限；在ChatGPT Plugins → Personal → Created by you安装连接，随后用只读get_current_workflow验证。未连接不能宣称已启用。仅本地34项工程测试/独立源码审查通过不证明生产反馈落库或视觉普适收益。

可验证收益：保存/回读、辅助文字可编辑、独立审稿流程、保留失败并修复转换丢失；S7内部送审门槛通过。时间节省、整个视觉蒸馏系统、第二风格、成熟品牌设计和真人最终认可尚未验证。后续按实际新缺口研究，不每轮重查全部技能。

最终原生交付通过后唯一业务下一动作：LIU_REVIEW_LIUXIANSHENG_CONTENT_TRANSFER。等待刘先生评价S7，不因AI通过恢复茶作、继续新版本或擅自改主线。原生最终写入失败时以实际锁为准，不读本说明推断完成。
