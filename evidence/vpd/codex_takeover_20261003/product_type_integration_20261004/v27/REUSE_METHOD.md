# V27 实际作品与调用入口

先从权威分支最新START_HERE.md读取CURRENT_TASK_LOCK.json、LATEST_CHECKPOINT.json及continuity/vpd/codex_takeover_20261003/WORKER_CURRENT_REUSE.md。本页仅定位27，不覆盖任务锁。审美以本版pixel_review/PIXEL_REVIEW.json为准；尚无文件时为PENDING，AI_PASS只允许进入刘先生验收。

完整[海报PNG](https://drive.google.com/file/d/1jN8ow06WVOP42wM_e3me7RdLZV159EXS/view)：1536×1024 RGB，1800565B，SHA256 `2a1d3077b0133fb383a957bbbf7bec3b84d9d2a4240b12fd9065db01b7a3f98d`。[主句SVG](https://drive.google.com/file/d/1KJn8KgvLXP0_piG9UPB9W1syCJ0vu1-f/view)：28889B，SHA256 `b8c0a6a0dbd31225c164535789eeee66042ee7bc8ccfa003df18083fd64b28a4`。三份原件均实际HTTP200下载并全字节核验，见DRIVE_ARCHIVE_READBACK.json；连接账户可访问，shared=false，不声称匿名公开。

实际[Figma源](https://www.figma.com/design/uyDxOoN1iNDPpEHTKSUWg1/?node-id=395-2)：page251:2/frame395:2，摄影395:3、编排395:4；品牌frame395:5/组395:6/矢量395:7–13；主句frame395:23/组395:31/矢量395:24–30。21节点14VECTOR，0TEXT/遮罩/布尔；曲线和位置可编辑，不支持原生文字换字或自动重排。旧26 frame391:2保留。[原生PNG](https://drive.google.com/file/d/1-MVwPZeEpN5R1JUQphrKgr_-Fx3QS9Pt/view)：2045956B，SHA256 `e3ba0f70d9710f9be4727875206d439e50a549848bd45b49da4ed8290d2e0dc2`。原生与登记成品有8463像素/最大33RGB渲染差，各自保存，不混称同一原件。

摄影仍是刘先生认可的局部无字背景重建[S原件](https://drive.google.com/file/d/1ZU-jfc_3JZqNlKn56PSpMyBLjwYnqIIA/view)，1735549B，SHA256 `7fd7777fed21100cb6b47bc305701476054263565e73246ac469d065aa080618`。FigmaIMAGE074a11ff4345752bae19150e799d9cae49518b8b，全部调色0。隐藏摄影原件及原prompt/seed/后端未恢复；单张好图与确定性重合成不能证明摄影可重复生成规则。已改善[V9品牌](https://drive.google.com/file/d/1hgIzKY63zIpxVJgYA590aPfi2mnixhhO/view) dd8e、x285/y198/宽205保留。

本版只改同一方向的字形与产品空间关系：复用24唯一[透明生成素材](https://drive.google.com/file/d/1SRpCiG8Mu59ZP5UFtY4hxg3ynLTPF2U3/view)34b9及17路径21轮廓描摹，保留自然书写粗细；“一”采用朝向杯口的弧线，“茶”一个完整部件局部重作落笔；一杯茶与慢下来分成杯/盘两组。全部21原轮廓before绑定，最终7完整复合路径。不是原生成边缘无损，不临摹参考字形、不调用字体文件。27无新生图/摄影/生产描摹；旧24内置image_gen真实调用及prompt见V24/IMAGEGEN_EXECUTION.json，后端NOT_EXPOSED。

实际制作程序为make_glyph_program.py、V27_GLYPH_EDIT_MANIFEST.json、build_headline_asset.py，依据及局部编辑在SOURCE_REAUTHORING_NOTES.json。接口失败、首稿保留、唯一茶字收笔修正和mtime纳秒JSON精度修复见technical-interface-history、geometry-corrections、MAKER_EXECUTION_RECEIPT.json及FINAL_FREEZE_RECEIPT.json。原宿主两次零写运行与Root另两次实际运行见MAKER_ACTUAL_VERIFY_READBACK.json；作者保存的文字不能代替实际运行记录。

只读复用：在仓库根运行 `python -X utf8 -B evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v27/build_headline_asset.py --verify-only`。用原生 `visual_memory.vpd_registered_type_composite.edited_lineage(root,27)` → `register(root,27,headline_ref,lineage)` → `replay` / `compare_pixels`。24有限编辑器核心未改，只在内存映射版本；保存的manifest和作品仍为27。全部1572864像素与登记结果0RGB差。固定162052产品核心中1374被正常字层覆盖、160678未覆盖：覆盖区与登记合成一致，未覆盖区与源一致；不能声称整个核心均与源相同。没有回贴、遮罩、补摄影或调色。

真实宿主调用、完整原生曲线、原摄影字节及原生导出绑定于FIGMA_NATIVE_CAPTURE.json、FIGMA_ACTUAL_BINDING.json、FIGMA_BINDING_RUNTIME_EVIDENCE.json、REGISTERED_TYPE_FIGMA_BINDING_CHECK.json。只读 `visual_memory.vpd_registered_type_figma_binding.verify_actual_binding(root,registration_ref,runtime_ref,download_ref)` 的第三参数必须是HTTP原件读回列表，不是官方工具结果字典。RGB/alpha零容差和4operand ULP不放松；28尚未封存时拒绝。缺宿主原始事件只能读封存证据，不能宣称在新设备重跑了宿主绑定。

依赖Python3.12.14/Pillow12.3.0、Node24.19.0/Sharp0.35.4/librsvg2.62.91、FontTools4.63.0 MIT、VTracer0.6.15 MIT、skia-pathops0.9.2 BSD3。固定wheel/来源/许可见../../audit/SKIA_PATHOPS_0_9_2_DEPENDENCY_EVIDENCE.json。按Drive及许可恢复私有素材并核验SHA后实际运行；下载不等于技能启用。

审美框架继续复用官方Anthropic [design-critique](https://github.com/anthropics/knowledge-work-plugins/blob/d3ee81913e5e179273313345847a2a4f42449bd2/design/skills/design-critique/SKILL.md)，固定d3ee81913e5e179273313345847a2a4f42449bd2、Apache2；上游核心不重写，skills/chazuo-independent-art-review/SKILL.md为薄适配，不是中文品牌专家技能或真人资格。27实际阅读的Adobe/Tiago海报与产品字形组织、Adobe编排、ChanaMesser字形资料及许可边界见PROFESSIONAL_METHOD_READBACK.md；示范图和视频未能读取，不声称观看、复现或复制素材。Glyphs/Figma官方曲线方法及实际观看边界见continuous_typography_20261004/tutorials/TUTORIAL_METHODS.md。未发现适用的成熟中文产品品牌制作SKILL，不能拿网页美化技能替代。

独立技术见../audit/PROFESSIONAL_V27_TECHNICAL.json、../../audit/REGISTERED_TYPE_GUARD_FRESH_REVIEW_V27.json；正式审美是另建项目外Sol/Max任务，只给中立要求及P→N→R→S→T五原图，不给创作者自评分、历史审稿结论或T真人结论。技术通过不能替代实际像素冷审，有限校准只报告真实一致和分歧。原评论即使错误仍保留，不移动冻结品牌迎合误判。

流程、可编辑性、视觉收益、时间收益、真人认可分开报告。仅最新固定仓库入口的新上下文实际使用保存资产才证明本版复用，旧V9证明和Root文件回读不能替代。整个视觉蒸馏、迁移及第二风格未因单张完成而通过。唯一下一动作取当前任务锁。
