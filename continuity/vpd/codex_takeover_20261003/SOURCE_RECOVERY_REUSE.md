# 茶作第一张摄影恢复：真人验收入口

只从最新分支的 START_HERE.md → PROJECT_CONTROL_ADAPTER.json → CURRENT_TASK_LOCK.json / LATEST_CHECKPOINT.json 恢复。当前唯一动作是验收局部背景重建，原三版海报仍已被刘先生否决，未重新开海报预算。

本次只调用一次内置 image_gen 做去字素材；没有新摄影、第二风格、付费算力或自动任务。整张工具输出改变了茶碗等像素，不能作冻结底图。实际交付仅取文字所在的五个背景邻域，与原摄影合成，20px 内侧过渡，约19.93%像素在声明的修补范围内；其他1,259,404个RGB像素与认可第一张完全相同。茶碗、茶盘、苔石和中央溪流的检查区域不在蒙版内。

这叫“局部背景重建”，不是找回无字原件。文字遮住的隐藏内容未知，周围少量可见背景也参与过渡，需要刘先生验收其氛围与痕迹。原件 SHA256 为 e7af9c9e88ff9dd38357a570305c4b5d40e98678d14c174957d4bdf2e7bdfd29；最终修补候选为 7fd7777fed21100cb6b47bc305701476054263565e73246ac469d065aa080618，1536×1024。

实际查看与恢复：

- [原件](https://www.figma.com/design/uyDxOoN1iNDPpEHTKSUWg1?node-id=278-2)：原字与摄影同时保留。
- [最终摄影修补候选](https://www.figma.com/design/uyDxOoN1iNDPpEHTKSUWg1?node-id=283-5)：精确PNG原字节档案。
- [可编辑原图＋透明修补层](https://www.figma.com/design/uyDxOoN1iNDPpEHTKSUWg1?node-id=283-2)：底层283:3锁定，透明修补层283:4。
- [失败笔画蒙版预览](https://www.figma.com/design/uyDxOoN1iNDPpEHTKSUWg1?node-id=283-6)：暗字影及残字，不作为交付。

在 ChatGPT 中读取图像：加载 figma-use，再调用官方 figma_download_assets(fileKey=uyDxOoN1iNDPpEHTKSUWg1,nodeId=283:5)。下载 rawImages 原PNG并核对上述SHA；不要把 export 重渲染当作相同文件字节。原件同法读取278:2，可编辑图的 rawImages 应返回原件与透明修补层。当前已完成调用与HTTP200身份回读证据见 evidence/vpd/codex_takeover_20261003/source_recovery/。

运行方法：已有一次生成请求在 IMAGEGEN_REQUEST.json，真实返回及整图越界比较在 IMAGEGEN_EXECUTION.json。不要自动重放生图。scripts/vpd_compose_local_repair.cjs 只对该固定原件和该唯一素材做声明蒙版的透明合成，不补造内容、不重采样、不调色；依赖 Node 与 MIT pngjs 7.0.0。MASK_DEFINITION.json / FAILED_GLYPH_MASK_FIDELITY.json 保留窄笔画方案失败，CONTEXT_MASK_DEFINITION.json / FINAL_PIXEL_PROTECTION.json 为最终范围与数值检查。透明层原文件SHA为74899b51caf9d15ba4055572d30b89479d3209e2baa748130a20bdd1309f8fad。

本机已实际使用 Codex bundled runtime，默认PATH里的node/Python不是这次依赖来源。先调用load_workspace_dependencies获取当前宿主路径。当前Windows宿主在仓库根目录的真实调用如下；其他宿主改为工具返回路径，勿凭该固定Windows地址宣称依赖可用。

```powershell
$env:NODE_PATH='C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules'
& 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe' scripts/vpd_compose_local_repair.cjs --source .liu-visual-private/browser_reconcile_20261003/CHATGPT_GENERATED_IMAGE_1_e7af9c9e.png --material .liu-visual-private/source_recovery_20261003/imagegen-cleanup-material.png --out .liu-visual-private/source_recovery_20261003/photography-local-reconstruction-final.png --overlay .liu-visual-private/source_recovery_20261003/local-repair-overlay.png --mask evidence/vpd/codex_takeover_20261003/source_recovery/CONTEXT_MASK_DEFINITION.json --receipt evidence/vpd/codex_takeover_20261003/source_recovery/FINAL_PIXEL_PROTECTION.json
```

上述输入原件和素材可以分别从Figma278:2与278:3的rawImages恢复，必须核对e7af9c9e…和01faebaa… SHA。若没有bundled pngjs，可在私有工作目录用npm install --prefix .liu-visual-private/node-runtime pngjs@7.0.0，然后将NODE_PATH设为该目录的node_modules；本次未执行此安装路径，不能宣称另一个宿主已安装。Pillow仅用于读取像素并建立早期矢量mask；不是最终成品修图工具，也不是最终合成必需依赖。

独立审核复用成熟 Anthropic design-critique 固定提交 d3ee81913e5e179273313345847a2a4f42449bd2 的整体印象、具体画面证据、优先问题方法，仍为实验适配，不证明中文字标能力。专职审稿AI以fork_turns=none读P/N/R/S/T实际像素；不会继承创作者过程，也不冒充项目外物理目录或真人专家。原四图海报审核协议保留，SOURCE_REVIEW_CARRIER_AMENDMENT.json只用于本次摄影输入补充检查。

本次真实审核结果：source_recovery/pixel_review/PIXEL_REVIEW.json为AI_PASS，仅针对摄影背景重建候选。已核验一个新turn_context、实际gpt-6.1-sol/Max、5次成功view_image、无其他工具读取；范围及原始审稿结论不可扩成字标或海报通过。P/N/S为有限校准，T为未给真人结论的检验样本，其真人结论仍待审，当前不能报告该新样本的人机一致率。

当前未完成：摄影修补真人验收、重做茶作字标及完整文字海报、长期视觉生成规则与迁移收益。AI审核仅决定可否送摄影验收，不能把无字图当最终品牌海报。新的原始摄影生成配方、旧第一张的模型/seed仍未确认；本次保存的清理提示词不冒充旧成功摄影配方。

唯一下一动作：刘先生对283:5与278:2实际像素对照，确认局部背景重建是否可作为冻结摄影输入。在这个反馈到来前停止进一步设计或生成。
