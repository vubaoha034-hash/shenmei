# V25 实际作品与复用入口

先从权威分支最新 `START_HERE.md` → `CURRENT_TASK_LOCK.json` / `LATEST_CHECKPOINT.json` → `continuity/vpd/codex_takeover_20261003/WORKER_CURRENT_REUSE.md` 恢复。本文只定位V25，不能覆盖当前任务锁。正式审美结果以本版 `pixel_review/PIXEL_REVIEW.json` 为准，未取得前为PENDING；AI_PASS也仅允许进入刘先生审核。

完整[海报原件](https://drive.google.com/file/d/1IXXnS6o4OOUus-tEVY0qLZp6UMnQf1wH/view)：1536×1024 RGB，1798351B，SHA256 `e2f1f5d432fd74c9f705a976f41ab61cfe7fff3ac5a768844f765a5f1f1fe6da`。[主句SVG](https://drive.google.com/file/d/19PlORUWR0KYgA-UCnnytNhSvg1BYU2V2/view)：7823B，SHA256 `a9b15003c81650271f022b51985e86b63928d794e1674e1565b1f05fd39c2129`。已有[茶作字标](https://drive.google.com/file/d/1hgIzKY63zIpxVJgYA590aPfi2mnixhhO/view)七条曲线、SHA256 `dd8e9e899393dc36eb3f5b1652bdbb740787d41a108ea6aa1eae05cb1368b1ff`及285,198/宽205原位保留。

真实可编辑[Figma源](https://www.figma.com/design/uyDxOoN1iNDPpEHTKSUWg1/?node-id=388-2)：page251:2，frame388:2；摄影388:3，编排388:4；品牌frame388:5/组388:6/矢量388:7–13；主句frame388:23/组388:31/矢量388:24–30。21节点、14VECTOR、0TEXT、0mask、0BOOLEAN；曲线和位置可编辑，不能当原生文本换字/自动重排。V24 frame384:2保留。[Figma原生PNG](https://drive.google.com/file/d/1-K9AyPkA-qACmQja7glmxBJHSwOPOHGn/view)：2045083B，SHA256 `738e79d3fd45bcec03166bfe351e97cb08b6c2c868f25c7dcf1416c283f9daaa`。它与登记合成PNG有7917像素/最大41RGB差，均保存，不能称同一文件或推定感知色彩完全等价。

摄影为真人认可的局部无字背景重建源：[S原件](https://drive.google.com/file/d/1ZU-jfc_3JZqNlKn56PSpMyBLjwYnqIIA/view)，1735549B，SHA256 `7fd7777fed21100cb6b47bc305701476054263565e73246ac469d065aa080618`，Figma IMAGE `074a11ff4345752bae19150e799d9cae49518b8b`。没有恢复隐藏原件，也没有恢复原摄影prompt/seed/生图后端；单张底图及确定性重合成不能证明重复生成摄影规则。原始摄影及真人认可范围未扩大。

本版只调整主句读序、行间和收笔：提高“一”的位置，缩短杯木竖及下/来的长脚，拉开茶与慢的行间，以原杯/叶/盘像素作边界。仍是同一个设计方向；是否真正建立产品与文字关系由实际像素冷审判断。V24唯一真实[透明生成素材](https://drive.google.com/file/d/1SRpCiG8Mu59ZP5UFtY4hxg3ynLTPF2U3/view)1774×887 RGBA、383223B、SHA256 `34b9b720d7d39b85c48d36220d2d53e4261d4ee88a5c27056fa796a52c39f774`与完整17路径/21轮廓trace复用；V25没有新生图、生产描摹或摄影生成。实际旧调用和prompt仍在V24，内置image_gen后端模型为NOT_EXPOSED。

制作依据是逐原轮廓before绑定的有限JSON编辑，40个作者闭合轮廓，经未改skia-pathops的原生曲线union/difference成为7个复合主句路径。不是普通字体旁贴叶子，也不是保留原生成轮廓的无损转换；不使用字体文件轮廓或R参考字形。真实程序、字形数据及局部慢忄留白修正在 `make_glyph_program.py`、`build_headline_asset.py`、`V25_GLYPH_EDIT_MANIFEST.json`、`SOURCE_REAUTHORING_NOTES.json`、`MAKER_PIXEL_INSPECTION.json` 和 `geometry-corrections`，前版失败不删除。源路径、制作与运行身份见 `ASSET_PROVENANCE.json`、`CREATION_RUNTIME_EVIDENCE.json`、`FINAL_FREEZE_RECEIPT.json`。

只读重算：仓库根目录中，以实际可用Python执行 `python -X utf8 -B evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v25/build_headline_asset.py --verify-only`。需要固定的原件/私有依赖时，先按Drive和封存许可恢复并校验SHA，不能把下载说成已启用。Python3.12.14/Pillow12.3.0、Node24.19.0/Sharp0.35.4/librsvg2.62.91、FontTools4.63.0、VTracer0.6.15 MIT、skia-pathops0.9.2 BSD3；固定上游、wheel、实际调用和许可见 `../../audit/SKIA_PATHOPS_0_9_2_DEPENDENCY_EVIDENCE.json`。数学库不是审美技能。

登记复用同一原生机制：`visual_memory.vpd_registered_type_composite.edited_lineage(root,25)`、`register(root,25,headline_ref,lineage)`、`replay`、`compare_pixels`。旧V24 kernel不改，V25最小适配仅为其固定有限编辑器映射版本，原25profile和输出身份保持。注册与全幅/alpha0/固定162052核心检查分别在 `REGISTERED_TYPE_COMPOSITE.json` / `REGISTERED_TYPE_COMPOSITE_CHECK.json`。核心78字层覆盖+161974未覆盖均参与0RGB核验，不作核心贴回、遮罩、背景补丁。

实际源结构、摄影原字节、7+7条曲线和原生导出绑定在 `FIGMA_NATIVE_CAPTURE.json`、`FIGMA_ACTUAL_BINDING.json`、`FIGMA_BINDING_RUNTIME_EVIDENCE.json`、`REGISTERED_TYPE_FIGMA_BINDING_CHECK.json`。入口仍是 `visual_memory.vpd_registered_type_figma_binding.verify_actual_binding(root,registration_ref,runtime_ref,download_ref)`；精确RGB/alpha零容差及4operand ULP不放松。26等未封存未来版本拒绝。跨设备缺少原宿主runtime时只读封存证据，不能谎称在新设备已复跑宿主绑定。

成熟审核方法沿用Apache-2.0官方Anthropic design-critique，固定提交 `d3ee81913e5e179273313345847a2a4f42449bd2`：[原始SKILL](https://github.com/anthropics/knowledge-work-plugins/blob/d3ee81913e5e179273313345847a2a4f42449bd2/design/skills/design-critique/SKILL.md)。已核验实际发现和读取；上游核心不重写，仅适配静态海报。项目 `skills/chazuo-independent-art-review/SKILL.md` 是薄适配，不是另建状态系统，也不是中文字体专家技能或真人资格。Glyphs Drawing good paths与Figma官方矢量教程的闭合曲线/节点/字腔方法实际用于制作，固定来源见现有 `continuous_typography_20261004/tutorials/TUTORIAL_METHODS.md`。本轮不重复无缺口的全面技能搜索。

正式审稿另建项目外Sol/Max任务，只收到中立要求和P→N→R→S→T五原图，分五次各实际看一张，不传创作者自评分/历史AI判决/T真人判决。P/N有限校准与匿名检验分开，不宣称准确率。移除两条Root附加且此前产生错误事实的数值位置要求，保留原始像素、标准与技术核验；完整修改依据在 `REVIEW_BRIEF_EVIDENCE_BOUNDARY_REPAIR.json`。独立专业技术与代码报告另见 `../audit/PROFESSIONAL_V25_TECHNICAL.json`、`../../audit/REGISTERED_TYPE_GUARD_FRESH_REVIEW_V25.json`，不能替代项目外审美冷审。

三新Drive原件均存既有项目文件夹，metadata/parent/revision已核，HTTP200全字节与本地相同，见 `DRIVE_ARCHIVE_READBACK.json`、`ASSET_DRIVE_ARCHIVE.json`。品牌和生成素材沿用历史归档，未声称本版重新网络读取。连接账户可访问、metadata shared=false，不宣称匿名公开。源文件、封存字层与实际运行可编辑性/流程收益分别报告；视觉改善、真人认可及整个蒸馏系统迁移验证另行判断。只按最新任务锁的唯一下一动作继续。
