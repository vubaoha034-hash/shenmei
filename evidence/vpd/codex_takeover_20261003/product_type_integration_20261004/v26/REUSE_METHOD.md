# V26 实际作品与调用入口

从权威分支最新START_HERE.md，依次读取CURRENT_TASK_LOCK.json、LATEST_CHECKPOINT.json及continuity/vpd/codex_takeover_20261003/WORKER_CURRENT_REUSE.md。本页定位V26，不覆盖任务锁。正式审美以本版pixel_review/PIXEL_REVIEW.json为准；不存在时为PENDING，AI_PASS只允许进入刘先生审核。

完整[海报原件](https://drive.google.com/file/d/1mF0kYK5Ya22nbzsIY0ElgebMG-n0X4sx/view?usp=drivesdk)：1536×1024 RGB、1801270B、SHA256 `2019e4a1e413b169d72bc4e15826d6af2be2780663745125b4fa5afa9faf23c9`。[主句SVG](https://drive.google.com/file/d/1czeeLvDi4vFEHXbRaeKMIQLqHqDYFHfH/view?usp=drivesdk)：29127B、SHA256 `5ea079d14a0b7bcbfe74d467e913d1f17e1ef1962a9522b97cce72b3552ad08c`。三份新Drive原件已实际HTTP200下载、全字节核对，见DRIVE_ARCHIVE_READBACK.json。连接账户可访问，shared=false，不声称匿名公开。

真实[Figma源](https://www.figma.com/design/uyDxOoN1iNDPpEHTKSUWg1/?node-id=391-2)：page251:2/frame391:2；摄影391:3、编排391:4；品牌frame391:5/组391:6/矢量391:7–13；主句frame391:23/组391:31/矢量391:24–30。21节点、14VECTOR、0TEXT/遮罩/布尔节点；曲线及位置可编辑，不支持原生文本换字或自动重排。V25 frame388:2保留。[Figma原生PNG](https://drive.google.com/file/d/1iZM3lXkkLXIIajG2398uVgtwH_I6dFgR/view?usp=drivesdk)：2048197B、SHA256 `317e5e1ce631e4d01d10f6fb6abf3dd10a372fdb7c14588e2d5cd16d7f3d24a0`。它与登记成品有7666像素/最大42RGB差，两者各自保存，不能混称同一文件。

摄影仍为真人认可的局部无字背景重建源[S原件](https://drive.google.com/file/d/1ZU-jfc_3JZqNlKn56PSpMyBLjwYnqIIA/view)，1735549B、SHA256 `7fd7777fed21100cb6b47bc305701476054263565e73246ac469d065aa080618`；Figma原图IMAGE074a11ff4345752bae19150e799d9cae49518b8b、全部调色0。没有恢复隐藏摄影原件、原prompt/seed/后端；单张好底图和确定性重合成不能证明重复生成摄影规则。已改善的[V9茶作字标](https://drive.google.com/file/d/1hgIzKY63zIpxVJgYA590aPfi2mnixhhO/view)、dd8e9e899393dc36eb3f5b1652bdbb740787d41a108ea6aa1eae05cb1368b1ff、x285/y198/宽205保留。

本版主要变化是恢复原生成素材已有的自然书写粗细与转折，再在杯、叶、盘上方的暗部组织一条主句。此前手工重画造成匀细直线，故不继续重写有效源曲线。V24唯一[透明生成原件](https://drive.google.com/file/d/1SRpCiG8Mu59ZP5UFtY4hxg3ynLTPF2U3/view)、34b9b720d7d39b85c48d36220d2d53e4261d4ee88a5c27056fa796a52c39f774，与17路径/21轮廓alpha128描摹复用；26没有新生图、生产描摹或摄影生成。内置image_gen实际旧调用及prompt保留在V24，后端模型NOT_EXPOSED。

制作依据及可运行程序：make_glyph_program.py、V26_GLYPH_EDIT_MANIFEST.json、build_headline_asset.py、SOURCE_REAUTHORING_NOTES.json。21原始轮廓逐一before绑定，删除462个冗余曲线指令，有限调整字腔/收笔，组成7个主句复合路径；不是40个另造匀细轮廓，也不声称原生成边缘无损。品牌七路径原样保留，不使用字体文件或临摹R字形。两次技术接口失败、真实修复、最终零写验证在technical-interface-history、FINAL_FREEZE_RECEIPT.json及MAKER_ACTUAL_VERIFY_READBACK.json；不能把作者保存的输出当宿主实际运行证明。

只读调用：仓库根目录执行 `python -X utf8 -B evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v26/build_headline_asset.py --verify-only`。登记沿用原生机制：`visual_memory.vpd_registered_type_composite.edited_lineage(root,26)` → `register(root,26,headline_ref,lineage)` → `replay` / `compare_pixels`。旧V24有限编辑器不变，仅在内存映射版本，原保存manifest及所有作品身份仍为26。REGISTERED_TYPE_COMPOSITE_CHECK.json核对全幅、透明区域及全部162052核心；本版核心字层覆盖0、未覆盖162052，均0RGB差，不回贴/遮罩/重生摄影。

真实原生曲线、摄影原字节、导出与宿主调用分别绑定在FIGMA_NATIVE_CAPTURE.json、FIGMA_ACTUAL_BINDING.json、FIGMA_BINDING_RUNTIME_EVIDENCE.json、REGISTERED_TYPE_FIGMA_BINDING_CHECK.json。固定入口 `visual_memory.vpd_registered_type_figma_binding.verify_actual_binding(root,registration_ref,runtime_ref,download_ref)`；0RGB/0alpha及4operand ULP不放松。未封存27拒绝；缺少原宿主runtime时只能读封存证据，不能宣称新设备已重跑宿主绑定。

依赖为Python3.12.14/Pillow12.3.0、Node24.19.0/Sharp0.35.4/librsvg2.62.91、FontTools4.63.0 MIT、VTracer0.6.15 MIT、skia-pathops0.9.2 BSD3。上游及wheel固定来源、许可、实际原生运算见../../audit/SKIA_PATHOPS_0_9_2_DEPENDENCY_EVIDENCE.json。需要本地原件与私有依赖时按Drive/许可证恢复并核验SHA；下载不等于启用，数学库不等于审美技能。

成熟评审框架继续采用官方Anthropic [design-critique](https://github.com/anthropics/knowledge-work-plugins/blob/d3ee81913e5e179273313345847a2a4f42449bd2/design/skills/design-critique/SKILL.md)，固定d3ee81913e5e179273313345847a2a4f42449bd2、Apache2。上游核心不重写，项目skills/chazuo-independent-art-review/SKILL.md薄适配静态海报。它不是中文字形专家技能或真人资格。Glyphs Drawing good paths及Figma官方矢量教程的方法出处和实际读取边界见continuous_typography_20261004/tutorials/TUTORIAL_METHODS.md；YouTube只有描述读取，不声称看过视频。

正式审美另建项目外Sol/Max任务，只给中立要求及P→N→R→S→T五原图；分别实际看图，不给创作者自评分/历史AI结论/T真人结论。独立技术和代码挑战另见../audit/PROFESSIONAL_V26_TECHNICAL.json、../../audit/REGISTERED_TYPE_GUARD_FRESH_REVIEW_V26.json，技术通过不能替代冷审。有限校准只报告真实一致/分歧；旧版本错误品牌位置判断仍保存，不移动已冻结品牌去迎合错误意见，也不宣称数值提示已解决审稿可靠性。

流程、可编辑性、视觉收益、时间收益和真人认可分别判断。仅最新固定仓库入口的新读取上下文实际使用已保存资产，才证明本版复用；历史V9证明及Root文件回读不能代替此项。整个视觉蒸馏系统、跨家族迁移、第二风格均未因本版完成而通过。唯一下一动作始终取当前任务锁。
