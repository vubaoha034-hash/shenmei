# 茶作 V29：完整成品与复用

权威状态是 `continuity/vpd/CURRENT_TASK_LOCK.json`；从 `START_HERE.md` 固定最新提交并读取入口要求，不依赖本聊天。当前唯一下一步在锁中：刘先生审核 V29 完整海报。AI_PASS 只允许进入交付，真人结果 PENDING。不得自行启动 V30、第二风格或恢复自动任务。

完整 PNG：[Drive 原件](https://drive.google.com/file/d/1HOlv9dQhBLWery2pDFIok_QLAblLsypt/view?usp=drivesdk)，1536×1024，1808415 bytes，SHA-256 `9ef3fb9bcdbf2b6188e95b90d4abe9e6b12ab2c237acf544e73b9c8ab65b7fe4`。本机路径由本版 TECHNICAL_CHECK/DRIVE_ARCHIVE 指定，属于 Git 忽略的私有图像缓存，克隆没有 PNG 时先从 Drive 恢复原字节再核对 SHA。

实际 Figma：[402:2](https://www.figma.com/design/uyDxOoN1iNDPpEHTKSUWg1/?node-id=402-2)，page 251:2，photo 402:3，overlay 402:4，brand 402:23，文字系统 403:2。实际 42 VECTOR（7品牌+35字体）、0 TEXT、0 mask；矢量可编辑，但不能宣称原生文字重排。读取权限及原件已用连接账号核验，不代表匿名公开访问。完整节点来源用 FIGMA_SOURCE_READBACK/FIGMA_NATIVE_CAPTURE/REGISTERED_TYPE_FIGMA_BINDING_CHECK；两次成功导入属于一个正式版本。首次单段调用超过工具字符上限、下载/守卫失败及薄适配都保留，没有追加成品候选。

品牌资产：[SVG](https://drive.google.com/file/d/1PUyFMjJssY5Fkw8QpORb6HGIQLwcqqY-/view)；文字系统：[SVG](https://drive.google.com/file/d/1zr78voQRuJzfK1uLhj-dLuMae7GgE1xS/view)。Git 保存本版 brand.svg/headline.svg，SHA 分别 e9338ca1f4bb1016e24d524c21113481e405a3be1f4d6de0cb46e9d6833b3054、91fd53825b9bf8cacd48aa69753dedab6c13d90676d3f8096e1e83545a0b6a31。品牌沿用历史原创书写字标7个路径，属性和曲线不改，仅整组等比位置改变；源图像工具后台模型未暴露。辅助文字采用 Adobe Source Han Serif SC Regular 2.003 未修改完整字形，通过 FontTools 4.63.0 提取。品牌路径来源、30个唯一glyph/38实例/35可见轮廓、布局及许可见 ACTUAL_FONT_LAYOUT_LINEAGE、font-layout-production/glyph-evidence、manifest、font-license-OFL1.1.txt。

准确文案分三行：

> 一杯茶，慢下来
>
> 煮水、沏茶，把一刻留给自己。
>
> TEA FOR SLOW DAYS

前瞻授权依据 COPY_LAYOUT_AUTHORIZATION_AMENDMENT_20261005、REFERENCE_IDENTITY_CLARIFICATION_SHANYEJI_20261005 和本版 ROOT_FROZEN_INPUT_CONTRACT。指定参考是山野集，Drive 1fG2OQ7IphZfGnH1csu1qZKYCsyAMDOAZ，SHA 9a29fbdc7dd908017924bed270e8dfe18351519eed3fa7bc7001789f2a383414；仓库 CANONICAL_VISUAL_ANCHOR_MANIFEST 已有对应原件，不是参考缺失。历史 V1–V28 与默认旧参考/文案保持原样。

冻结摄影是已获真人摄影范围认可的局部去字重建：[Drive](https://drive.google.com/file/d/1ZU-jfc_3JZqNlKn56PSpMyBLjwYnqIIA/view)，SHA 7fd7777fed21100cb6b47bc305701476054263565e73246ac469d065aa080618。不是隐藏无字原件。完整生成提示/seed/后台模型不足，尚不能复现好底图的生成规则。V29 不生成摄影，不调色、不改构图；字标及文字用登记 alpha source-over。实际全幅重算 RGB 差0，框外1437534及产品核心162052像素差0。原生 Figma PNG另存 Drive 1V2jJ7hXq7abOLo7ngEZ7PMnEt2fM0U53；它与登记完整成品10018像素/max33RGB不同，两个渲染器差异如实保存，不称同一原件。

恢复现有作品只需 Drive 原件和 Git SVG/Figma 节点，不需要重新生图。完整原生状态检查会核验历史版本，因此新克隆若缺旧PNG，按 `scripts/vpd_restore_correct_source_exports.py` 与 WORKER_CURRENT_REUSE.md 的既有恢复机制先逐ID原字节取回并验SHA，不能用缩略图、截图或占位图代替。无凭据就报告原件不可获取，不判全状态通过。

重新运行制作配方使用 `scripts/vpd_prepare_v29_font_recipe.py`，先准备固定配方，已有目标图时 --run 拒绝覆盖。其准备入口已实际执行；新机器独立重跑制作尚未验证。只在新的制作授权与原生状态允许时调用 --run，当前 AI_PASS 后停止制作。配方位于 font-layout-production/build_v29.py、render_svg.cjs、finalize_receipt.py，成熟上游核心保留。实际依赖 Python3.12.14/Pillow12.3.0/FontTools4.63.0/Node24.19.0/sharp0.35.4；FontTools 来自现有 Hermes venv，bundled Python/Node/Sharp 用 load_workspace_dependencies 查实际路径，不承诺跨机器自动安装。字体固定提交7889f11bf31170b5d092a083b357c8c8130f89e0，完整OTF SHA78aa7a328fd974df2d688c8a9fd74a33d8334dfa84ab24d9d11efb2ffc464117，OFL1.1；FontTools MIT。保留预先生产原配方和实际调用证据，不把 --prepare 当重新制图。

正式评测复用 `scripts/vpd_collect_agent_review.py` 与原生 INDEPENDENT_WORKER_CONTRACT_V2 / WORKER_FORMAL_REVIEW_CARRIER_AMENDMENT。每次改图重新冻结包、新建项目外隔离审核；不能沿用本版结果。V29 实际全新 projectless 任务01a10ad0-d94f-7293-820e-3905c9188c09，Sol/Max，只看P/N/R/S/T五张原图，295839ms。完整原话与模型/读取/原字节传输证据在 pixel_review/ 和 ACTUAL_COLD_PIXEL_TRANSPORT_READBACK。加密初始prompt的逐字节绑定在日志中 NOT_VERIFIABLE，其余新任务/未继承上下文/工具读取范围/五原图身份已实查；不夸大隔离证明。

审美结果 AI_PASS：可读字标、层级、杯盘动线成立；作字内白、小字对比、品牌专属性和与参考的整体差距仍存在。专业技术 TECHNICAL_PASS_WITH_LIMITATIONS 在 ../audit/PROFESSIONAL_V29_TECHNICAL.json；29.0类型绕过的真实初审失败、修复、负例与原结果全保存。技术正确不等于审美通过。校准P只认可文字，摄影否决；N整图否决。T真人结论隐藏且待定，历史误放行未删除，样本有限不报准确率。

补充 blind_comparison/ 实际隐藏A/B版本号对照支持品牌识别、阅读秩序和产品空间改善；字图关系、接近山野集为MIXED。两turn含一次B路径失败恢复，非项目外冷审替代。A“贴顶”观察与实际y198不符，明确排除这条收益依据。不能推断节时、迁移或真人认可。

成熟 [Anthropic design-critique](https://github.com/anthropics/knowledge-work-plugins/blob/d3ee81913e5e179273313345847a2a4f42449bd2/design/skills/design-critique/SKILL.md) 固定d3ee81913e5e179273313345847a2a4f42449bd2、Apache2，核心不改，仅静态海报中立审稿适配；实际brief调用已保存，不是中文创作skill。FontTools/Adobe字体是专业工具与素材；未找到可据实宣称成熟适用的中文品牌生成skill。最新教程证据在 tutorial-learning/：站酷编号正文实际读，B站/抖音仅目录/索引，视频观看0；V29早于本次教程阅读，不把改善归因新课程。此前一次透明四字图像资产/一次VTracer描摹 NOT_USED，Drive1WyVZYPUGKmNNw4uDTQhUtOBi3d8V1e8e，失败边界保留；最终字体布局0生图/0生产描摹不等于整个本轮0生图。

流程与可编辑性已验证；这对作品局部视觉改善有独立像素对照，整体高级感/系统迁移收益与节时未验证。新读取上下文的仓库恢复结果以实际发布后回执为准，当前准备文档不等于恢复通过。唯一下一步：刘先生审核这张完整原件，并将反馈绑定V29 SHA后由主执行者更新原生锁。
