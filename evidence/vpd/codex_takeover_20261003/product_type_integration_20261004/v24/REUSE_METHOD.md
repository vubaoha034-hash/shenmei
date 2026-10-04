# V24 实际作品与恢复方法

从权威分支最新 `START_HERE.md` 读取原生 `CURRENT_TASK_LOCK.json`、`LATEST_CHECKPOINT.json`、`continuity/vpd/codex_takeover_20261003/WORKER_CURRENT_REUSE.md`。本文只定位V24，不覆盖任务锁。正式审美结果读本版原始 `pixel_review/PIXEL_REVIEW.json`；该文件未取得前为PENDING，不能用制作记录、技术检查或本文推断通过。

完整海报：[Drive原件](https://drive.google.com/file/d/1nYivrRDZU3aZySfapBbeHLiX8RWLFomd/view?usp=drivesdk)，1536×1024 RGB，1797487B，SHA256 `c677444525f6e677661a981e873bd2f1fd87d1a3a16817d5030b2f4af6f53fee`。主句 [SVG](https://drive.google.com/file/d/18uO1wSX5_V69T6rlgWGmGLeZg2IavGQ3/view?usp=drivesdk)，8447B，SHA256 `58a8f9813e5f0f313fc58c30f47b893c13661c5f0ebd061a6cd064a7defd02dd`。一次真实生成的 [透明素材原件](https://drive.google.com/file/d/1SRpCiG8Mu59ZP5UFtY4hxg3ynLTPF2U3/view?usp=drivesdk)，1774×887 RGBA，383223B，SHA256 `34b9b720d7d39b85c48d36220d2d53e4261d4ee88a5c27056fa796a52c39f774`。这张生成素材不是成品；原件、实际prompt和结果见 `IMAGEGEN_EXECUTION.json`、`IMAGEGEN_PROMPT.txt`。

真实 [Figma源](https://www.figma.com/design/uyDxOoN1iNDPpEHTKSUWg1/?node-id=384-2)：page251:2，frame384:2，摄影384:3，编排384:4，品牌384:5/组384:6/矢量384:7–13；主句384:33/组384:41/矢量384:34–40。共21节点、14VECTOR（7品牌＋7主句复合路径），0TEXT、0mask、0BOOLEAN。实际创建、完整节点曲线、原始摄影字节和原生PNG读取分别在 `FIGMA_SOURCE_READBACK.json`、`FIGMA_NATIVE_CAPTURE.json`、`FIGMA_BINDING_RUNTIME_EVIDENCE.json`。原V23节点373:2保留，可编辑曲线/位置，但不能当原生文本直接换字或自动重排。

[Figma原生完整PNG](https://drive.google.com/file/d/11q6W1UEKcibcA0UljwhGIy5HaZk-g1E_/view?usp=drivesdk) 2044264B，SHA256 `1eca44ae11df066cdcac70fbddc780ed093d8100e4ccbdaddd1c16ce9a7e9e23`。原生PNG与严格登记合成使用不同渲染器：8234像素、最大42RGB差异，两个原件分别保留，不能称为同一个文件。主交付采用固定摄影＋品牌＋登记字层的精确source-over合成，没有核心贴回、遮罩或背景补丁。

摄影保留真人仅认可的局部无字背景重建图，Drive `1ZU-jfc_3JZqNlKn56PSpMyBLjwYnqIIA`，SHA256 `7fd7777fed21100cb6b47bc305701476054263565e73246ac469d065aa080618`，Figma IMAGE `074a11ff4345752bae19150e799d9cae49518b8b`。它不是找回隐藏无字原件；原始底图prompt、seed、后端模型并未恢复，单张结果不能证明可重复生成底图规则。品牌保留V9已有七条字形，285,198/宽205与SHA `dd8e9e899393dc36eb3f5b1652bdbb740787d41a108ea6aa1eae05cb1368b1ff` 不变。底图和品牌的历史认可范围没有扩大。

本版主变化是实际重画主句骨架：一次内置 `image_gen.imagegen` 透明素材→未改VTracer0.6.15完整原始trace→逐原路径/轮廓before哈希绑定的有限JSON编辑→40个闭合作者轮廓→未改skia-pathops0.9.2原生曲线union/difference→七个复合字形。原17路径/21原轮廓完整对账，最终轮廓是作者重释，不能称为保留生成轮廓。源字形/编辑数据在 `SOURCE_TRACE.json`、`TRACE_COMMANDS.json`、`V24_GLYPH_EDIT_MANIFEST.json`；真实制作程序在 `trace_source_once.py`、`make_glyph_program.py`、`build_headline_asset.py`。不使用字体库轮廓或参考R字形。原生成素材比prompt要求更重、更噪；未重新抽取候选掩盖失败。

杯木竖与慢忄/又实际经过同一资产的局部可读性修正；杯沿和叶片附近留白由真实作者轮廓改变完成，摄影没有重生成。初稿、两次修正、最终kernel元数据刷新前记录都保留，定位见 `MAKER_PIXEL_INSPECTION.json`、`SOURCE_REAUTHORING_NOTES.json`、`geometry-corrections`、`technical-interface-history`。修正PNG在私有目录，公开代码/JSON/SVG留Git。没有把这些制作自查当独立AI_PASS。

依赖为实际Python3.12.14/Pillow12.3.0、Node24.19.0/Sharp0.35.4/librsvg2.62.91、FontTools4.63.0、VTracer0.6.15 MIT、skia-pathops0.9.2 BSD3。新依赖固定上游commit、wheel/许可/已安装二进制与真实示例调用在 `../../audit/SKIA_PATHOPS_0_9_2_DEPENDENCY_EVIDENCE.json`（该相对路径从本目录回到codex_takeover_20261003/audit）。几何库是技术能力，不能当中文审美技能或视觉收益证明。实际内置生图后端模型名未暴露；Root实际Sol/xhigh，制作Sol/Max，专业技术审查与独立审美配置各自读真实runtime。

只读复算：从仓库根目录，以实际已核实Python环境运行 `python -X utf8 -B evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v24/build_headline_asset.py --verify-only`。缺少原件/依赖则先按Drive和固定源码恢复，不能宣称下载即安装。生产描摹只执行一次；技术审计重描摹/重算不另记正式设计版本。

登记与核验复用原机制：`visual_memory.vpd_registered_type_composite.edited_lineage(root)`、`register(root,24,headline_ref,lineage)`、`replay`、`compare_pixels`，具体注册在 `REGISTERED_TYPE_COMPOSITE.json`。Figma绑定用 `visual_memory.vpd_registered_type_figma_binding.verify_actual_binding(root, registration_ref, runtime_evidence_ref, download_readback_ref)`；必须存在本版实际绑定检查后才可声明技术通过。全幅登记合成/alpha0/固定162052核心全部参与核验，1061字层覆盖与160991未覆盖均为0RGB差；摄影源与注册字层不能偷换。

独立审美使用已固定Apache-2.0官方 `anthropics/knowledge-work-plugins` 的design-critique静态海报部分及项目 `chazuo-independent-art-review` 协议。上游核心保留，只移除不适用网页交互项。它是审核框架，不是中文字体专门技能或真人资格。实际P/N校准、R上半参考、S摄影、匿名T由新的项目外任务按P→N→R→S→T分五次各读一张；不传制作自评分、历史AI结论或T真人结论。有限校准与检验分开，只报告实际一致/分歧，不能从样本推准确率。

四个新Drive文件均直接存既有归档文件夹，metadata确认parents，原件HTTP200且全字节回读相同，revision见 `DRIVE_ARCHIVE_READBACK.json`、`ASSET_DRIVE_ARCHIVE.json`。连接账户可读，当前metadata显示shared=false，不宣称匿名公开。跨设备从Drive恢复并校验完整SHA；Figma需要连接账户权限。原宿主runtime缺失时只能读取封存证据，不能宣称在新设备已运行宿主绑定守卫。 V23保存过当时V22私有缓存仅1B的观察；本轮Root只读检查be859f已核实三个缓存恢复为完整旧SHA。恢复原因和执行者未知，未宣称本轮重新网络下载或Root修复；历史观察保留。

流程、可编辑性、摄影保护、视觉改善与真人验收分别报告。内部AI通过只允许进入刘先生交付审核，不能推定整个视觉蒸馏系统、迁移能力或第二风格通过。当前唯一动作始终读取原生锁。
