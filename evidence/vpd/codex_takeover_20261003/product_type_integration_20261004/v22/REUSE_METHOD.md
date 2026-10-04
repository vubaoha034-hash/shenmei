# V22 实际源文件、原件和注册字层复用

先从仓库 `START_HERE.md` 读取原生任务锁与 `continuity/vpd/codex_takeover_20261003/WORKER_CURRENT_REUSE.md`。本文描述已经实际制作的 V22；不代替任务锁，不将技术正确或文件上传当成审美通过。旧版本及失败均保留。

真实完整海报：Drive `1ggyCK9T6CZPjFsSAoTa-zYtAbAQ0GTFc`，1536×1024，SHA-256 `062a525304f75f7642132ba9a08e22344aa12c31de36dc0c4a2f7eed0d173b4e`。可查看：<https://drive.google.com/file/d/1ggyCK9T6CZPjFsSAoTa-zYtAbAQ0GTFc/view>。

实际 Figma 源：<https://www.figma.com/design/uyDxOoN1iNDPpEHTKSUWg1/?node-id=366-2>；page251:2，frame366:2，摄影366:3，透明编排366:4，茶作字标366:5，完整主句366:33。24个可编辑矢量：字标7、主句17；0原生TEXT、0mask。可编辑曲线和位置，不支持原生文本自动重排。

主句SVG：`headline.svg`，Drive `1QsEOw6aww-zy8qP1NUwL_tXKqGf4gHdJ`，SHA `e9feab432466d4f1a7188fdeff746ab6773a538ff59d1f2c3fa477aa3de6d14d`。字标`brand.svg`保留V9已认可字形dd8e9e89…，位置285,198，等比宽205。冻结文案仍为“茶作”“一杯茶，慢下来”。

制作依据：仅一次内置 `image_gen.imagegen` 生成透明主句字层，后台模型名称没有对执行者暴露。思源宋体2.003旧主句图只作拼写/汉字结构输入，R的上半广告只作图文关系参考；新主句不是思源字体原始轮廓。实际原始RGBA字层在Drive `1tfu-QgcH_79hsXxm0lBqon7G8LG491ZD`，SHA `fcb4b5097ae1610dfd84ba6eb49fef7853d254d0c405c5e47600f35095064d2c`。

保留上游VTracer0.6.15核心，MIT许可、wheel/二进制/源码许可SHA及固定参数见`LETTERING_PROVENANCE.json`。只做项目所需的alpha≥128输入和整体等比定位；17条非空上游路径全部保留，路径d/translate逐项对账。阈值去掉原始辉光和柔边，样条近似不等于逐像素无损矢量化。源代码/依赖版本/实际调用见`build_headline_asset.py`、`CREATION_RUNTIME_EVIDENCE.json`及`MAKER_RUNTIME_EVIDENCE.json`。

摄影原件：Drive `1ZU-jfc_3JZqNlKn56PSpMyBLjwYnqIIA`，SHA `7fd7777fed21100cb6b47bc305701476054263565e73246ac469d065aa080618`；已获真人认可的局部背景重建图，不能声称找回隐藏无字原件。本版不生成、不调色、不回填摄影。先通过Drive官方metadata、原件stream与全部字节对账后，恢复到注册记录中的本地源路径。

V22保护检查修正只针对Root此前增加的“成品所有产品核心RGB必须等于底图”约束。当前要求源摄影不变，并且全幅成品严格等于冻结摄影加独立注册字层的source-over结果。字层覆盖的10283产品核心像素仍参与预期合成核验，未覆盖的151769核心像素严格等于摄影。不是跳过产品保护；遮挡是否合适仍由独立审美审核判断。旧V1–21保护与判断不改。

实际PNG导出边界：Figma原生导出SHA `fd15ce8e198607404be7747cad7f359b84b8b98f8cd238acbbc990ef540ddde3`与交付PNG是两个渲染器，实际8431像素有差异，最大通道差34。交付原件由相同源摄影和注册SVG在固定Sharp/Pillow存储色彩合成；全幅预期差0，字层alpha0范围原照片差0。没有声称原生导出字节等于交付PNG。所有真实原件、比较和身份见`PHOTO_SAFE_EXPORT.json`、`REGISTERED_TYPE_COMPOSITE_CHECK.json`、`FIGMA_ACTUAL_BINDING.json`、`DRIVE_ARCHIVE_READBACK.json`。

最小本地调用入口：Python3.12.14/Pillow12.3.0，Node24.19.0/Sharp0.35.4/librsvg2.62.91，VTracer0.6.15，FontTools4.63.0，实际缓存路径在模块和provenance中。使用`visual_memory.vpd_registered_type_composite.register/replay/compare_pixels`按已冻结注册复算；实际Figma检查使用`visual_memory.vpd_registered_type_figma_binding.verify_actual_binding(root, registration_ref, runtime_evidence_ref, download_readback_ref)`。`REGISTERED_TYPE_FIGMA_BINDING_CHECK.json`提供本版实际参数。资产builder可`--verify-only`复用，具体参数从脚本入口读取，不猜参数。

正确性检查读取实际源像素、字体/轮廓字节、Figma全树属性/隐藏层/全部曲线、真实调用日志和官方导出，禁止只拿五个布尔声明通过。实际本地宿主日志、私有原件缓存与绑定调用均须可读；只有Git文字记录的其他运行环境不能冒充已重新验证。可以读取已封存证据及Drive/Figma成果；缺少原件、依赖、宿主日志或live工具时精确报告缺项。当前实现仅接受已核验V22调用，未来版本的真实collector须有界登记和检查，不能沿用旧审稿结论。

独立审美使用`WORKER_PROMPT.txt`与`REVIEW_PACKET_BINDINGS.json`限定P/N校准、R上半参考、S冻结摄影、T本版真实原件；不带作者自评分、此前审稿结论或T真人结果。必须实际看五图。项目外新任务冷审原路线保留，技术专业角色与冷审角色不同，只有Root写业务状态。真人验收仍由刘先生最终决定。

读取当前原生锁确认审稿状态及唯一下一动作；本方法、可运行代码、可编辑性和保存证据都不能证明视觉提升或整个蒸馏系统完成。
