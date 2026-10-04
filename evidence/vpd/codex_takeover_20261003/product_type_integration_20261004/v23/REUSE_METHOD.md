# V23 实际作品与恢复方法

先读权威分支最新 `START_HERE.md`，再读原生 `CURRENT_TASK_LOCK.json`、`LATEST_CHECKPOINT.json` 和 `continuity/vpd/codex_takeover_20261003/WORKER_CURRENT_REUSE.md`。本文只定位实际 V23，不覆盖唯一下一动作。审美、真人认可和整个蒸馏系统完成情况，以当前任务锁及独立原始评测为准。

完整 PNG：[Drive 原件](https://drive.google.com/file/d/1lizdEuUcCxePGS6uUly7pzmpxiFdhuK4/view)，1536×1024，1788655B，SHA256 `9a2b30f2220357dd7a345e7e503b122a8eb21cdc01f7009084ee85e9e40cb0aa`。主句 [SVG](https://drive.google.com/file/d/1A2hdphLvMLLLE3gDuBs6mbu1pAqZjFwZ/view)，37499B，SHA256 `75e6b9a03b35afeeb577d7d9232efb2dbdb35de5f1cf5a5f999eaf09a5791a10`。`DRIVE_ARCHIVE_READBACK.json` 记录两次实际 HTTP200 原字节读取、当前 revision 及连接账户可访问边界；没有宣称匿名公开。

真实 [Figma 源](https://www.figma.com/design/uyDxOoN1iNDPpEHTKSUWg1/?node-id=373-2)：page251:2，frame373:2，摄影373:3，透明编排373:4，茶作字标373:5，主句373:33，主句组373:34，17主句矢量373:35–51。完整31节点、24VECTOR（7品牌＋17主句），0TEXT、0mask。可编辑曲线和位置，不支持原生文本换字或自动重排。

摄影仍为真人仅认可的局部无字背景重建图，Drive `1ZU-jfc_3JZqNlKn56PSpMyBLjwYnqIIA`，SHA256 `7fd7777fed21100cb6b47bc305701476054263565e73246ac469d065aa080618`。这不是找回隐藏原件，也不证明原生成提示词或底图生成规律已恢复。摄影文件、材质、颜色与Figma图片身份不变，本版0摄影生成、0调色。

品牌保留V9已有7条字形及285,198/宽205的定位。主句复用V22一次内置透明字层工具生成的17条轮廓；该工具后端模型名没有暴露。V23只整组等比缩放与平移，没有新生成、没有新描摹或删路径。最终矩阵：`matrix(0.3488013255394301 0 0 0.3488013255394301 524.3160869265243 431.0762262905397)`；alpha bbox `[610,514,990,720]`。初定位超出既有区域1px，正式登记前只上移1px；原资产、预览、Figma读取和原生导出完整保留在 `pre-envelope-correction` 及对应私有目录。不是隐藏失败或新增审美候选。

沿用未改上游 VTracer0.6.15（MIT）的已保存描摹结果；alpha≥128与样条近似不等于原RGBA无损复制。V22思源宋体2.003只作拼写和结构参考，新主句不能标成思源原始轮廓。源码、来源固定版本、许可、全部路径逐项对账和真实builder调用在 `LETTERING_PROVENANCE.json`、`BUILD_EVIDENCE.json`、`build_headline_asset.py`；制作观察在 `MAKER_INSPECTION.json`，不能冒充独立评测。

实际依赖复用Python3.12.14/Pillow12.3.0、Node24.19.0/Sharp0.35.4/librsvg2.62.91、FontTools4.63.0和已固定VTracer0.6.15。`build_headline_asset.py --verify-only`只读重算，不重新生成或写已有作品。完整制作脚本需读取原入口参数和实际环境路径，不猜测已安装。Figma初次组装 `FIGMA_ASSEMBLY.js` 是修正前真实调用；最终场景还包含 `FIGMA_ENVELOPE_CORRECTION_READBACK.json` 记录的一像素组移动，不能把初次组装单独称为最终版本。

实际技术调用复用现有 `visual_memory.vpd_registered_type_composite.register/replay/compare_pixels`；具体注册为 `REGISTERED_TYPE_COMPOSITE.json`。Figma绑定用现有 `visual_memory.vpd_registered_type_figma_binding.verify_actual_binding(root, registration_ref, runtime_evidence_ref, download_readback_ref)`，实参见本版 `REGISTERED_TYPE_FIGMA_BINDING_CHECK.json`（登记前若尚未保存则不可称已通过）。必须读取真实摄影、SVG、完整节点、官方导出与授权宿主实际runtime，不能用声明或文件路径替代。

成品严格等于固定摄影＋已注册字层的source-over，五项全幅/alpha0/字层正覆盖/核心检查均差0；固定162052核心中8328文字覆盖、153724未覆盖都参与核验。Figma原生PNG `9621d562c3b1dea74cc6075f9bdeedcbac64af55daf31b285993740d9484cc00` 与固定合成 PNG 使用不同渲染器：7275像素、最大39RGB差异，原生导出单独保留，不宣称两者相同。摄影不贴回核心，也不从成品减底图来推算字层。

独立审美沿用 `chazuo-independent-art-review` 和已固定 Apache-2.0 的官方 `anthropics/knowledge-work-plugins` design-critique 静态海报部分。该框架不是中文字体专业能力或真人资质。本版五张真实P/N校准、R上半参考、S摄影、匿名T由新项目外任务按P→N→R→S→T分五次各看一次，作者自评分、历史结论及T真人结论均不传入；具体输入与实际执行证据由 `REVIEW_PACKET_BINDINGS.json`、`WORKER_PROMPT.txt`、独立 `pixel_review` 保存，未运行不能判通过。

仓库文字和SVG可跨聊天读取；其他设备须从Drive恢复原件、核实依赖，Figma需要连接账户权限。缺少原宿主runtime的环境只能读取封存证据，不能声称已经重新执行当前绑定守卫。此前V22某些私有Drive缓存当前只剩1B，旧已核验记录仅支持其当时读取；本版实际新下载原件完整，历史Drive仍为恢复来源。真人认可、视觉改善和省时收益都需各自证据，不能从流程跑通推定。
