# 刘先生·视觉设计工作流 v0.2.0

本版修复“图像编辑约束存在，但最终交付与执行顺序没有被强制”的根因。0.1.5 及其结构锁/整张海报回归能力保留为兼容工具，但不再能替代请求级独立文字交付。

唯一可完成的独立文字主线固定为：

1. REFERENCE_TEXT_EXTRACTION — 参考文字提取
2. LOCAL_LETTERING_ASSET — 局部字稿
3. FIGMA_EDITABLE_REBUILD — Figma 可编辑文字重建
4. ACTUAL_INDEPENDENT_TYPOGRAPHY_REVIEW — 实际独立像素审核
5. ISOLATED_TYPOGRAPHY_DELIVERY — 独立可编辑文字交付

新增三个公开工具：
- start_typography_delivery
- get_typography_delivery
- record_typography_stage

任务持久化到现有 Site D1，以 authenticated user + task_id/request_key 隔离；每次写入使用 revision 乐观锁。任一步没有真实产物就不能前进。整张海报、结构锁回归、聊天计划、只把透明图贴进 Figma、未审核候选稿都不能满足阶段关卡。独立审核 FAIL 会回到 Figma 重建阶段，而不是继续交付。

Figma 阶段明确要求：
- isolated_typography_only=true
- contains_full_poster=false
- flattened_image_only=false
- image_node_count=0
- native_text_node_count + editable_vector_node_count >= 1
- 实际 readback 与 export SHA 证据

最终交付明确要求独立文字范围、可编辑源、Figma 实际回读、通过审核的 export 绑定；只有任务 status=COMPLETE 时才允许宣称工作流完成。

请求级任务只保存原生工作流的只读快照；native_state_write=false、native_task_lock_unchanged=true、s7_state_unchanged=true。不会把“地图以外”等临时请求写回原生 S7 任务，也不会改变原生真人 PENDING。

旧 compile_transfer_plan / validate_user_request_delivery 仍可用于历史海报/结构锁诊断，但工具说明会明确标记：不能完成 v0.2.0 独立文字任务。
