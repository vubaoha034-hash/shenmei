# START HERE — 强制执行入口

<!-- TYPO_METHOD_TRANSFER_GOAL_20261026 -->
**独立文字创作方法蒸馏任务（刘先生 2026-10-26 最新目标限定，非正式海报主线替代）**：
目标不是修好一张字、临摹优秀字标、描摹 Figma 矢量或学习新字体；必须从优秀设计师真实文字作品中提取可执行且可调整的创作机制，并在未经该方法调试的不同新汉字/词组上，以固定预算、相同生成器和盲评证明质量与可读性增益。
每次汇报严格分清 SOURCE_STUDY、METHOD_CANDIDATE、UNSEEN_TRANSFER_PIXELS、HUMAN_BLIND_REVIEW、VALIDATED_RULE。无跨字盲评数据不得宣称方法蒸馏成功。
已完成第一份参考矢量测量和假设候选（不是成功）：[REFERENCE_TO_METHOD_R1.json](evidence/vpd/typography_method_distillation_20261026/REFERENCE_TO_METHOD_R1.json)。
2026-10-26 已实际执行最小跨字技术诊断，四幅『潮 / 星光未眠』 A/C 真实可编辑Figma输出已存在，但不具备可证明的审美提升；ChatGPT Image 两次未按目标出单独字稿，Figma AI 当前文件不可用。**禁止把该诊断算作独立盲测或蒸馏成功；禁止简单字体变形循环**。读：[TRANSFER_PILOT_R1_RESULT_20261026.json](evidence/vpd/typography_method_distillation_20261026/TRANSFER_PILOT_R1_RESULT_20261026.json)
文字创作方法蒸馏 R2 实测（2026-10-26）：BCSS 两字共7条标注笔画 → 真实宽度响应测量 → 目标『云』『潮』A原轮廓/B均宽算法/C源测宽度算法三路Figma原生矢量实际输出；A/B/C截图已看，**源轮廓宽度迁移的审美增益未见，且不是《六島》原作者方法复原**。必须先解决同创作者样本、真实逐笔证据及部件/笔画角色匹配，不重跑纯宽度变形。详细证据：[R2_REAL_STROKE_PROFILE_ABLATION_20261026.json](evidence/vpd/typography_method_distillation_20261026/R2_REAL_STROKE_PROFILE_ABLATION_20261026.json)。该记录是独立研究支线，不动正式任务锁或任何生产额度。
，下一轮首先补齐真正笔势/墨迹和多样本创作过程依据。
范围保护：本段只管用户明确要求的**文字创作方法蒸馏支线**；不新增第二套任务锁，不变更 `continuity/vpd/CURRENT_TASK_LOCK.json`、正式主线下一步、生成预算、其他已停止任务及真人最终验收权限。
R3 外部方法可行性审核（2026-10-26）：[R3_INK_MORPHOLOGY_MODEL_FEASIBILITY_20261026.json](evidence/vpd/typography_method_distillation_20261026/R3_INK_MORPHOLOGY_MODEL_FEASIBILITY_20261026.json)。已检查公开代码：InkDiffuser 当前仓库缺推理脚本、训练依赖模块和预训练权重，许可证也未核实；不能直接使用。R2 的真实笔画宽度尝试和《六島》静态墨形代理均未证明审美改善。**下一次必须先满足同一作者/风格的合法多样本来源和按笔画角色的素材证据，不得再重复仅几何笔宽的 R2 实验。**
R3 同作者字标真实原件核验（2026-10-26 最新状态）：**此前 3 份 SVG 原件缺失已由独立的免费 GitHub Actions 云端实测解决**；3/3 源文件与 Wikimedia Commons 官方字节数和 SHA-1 完全一致，随后实际完成三件作品的静态墨形特征测量，原始SVG字节只在临时运行器中处理，公共仓库只保存衍生指标。核验报告：[R3_ROSANJIN_VERIFIED_SOURCE_METRICS_20261026.json](evidence/vpd/typography_method_distillation_20261026/R3_ROSANJIN_VERIFIED_SOURCE_METRICS_20261026.json)，唯一审计原始回执位于研究分支 [ROSANJIN_REMOTE_SOURCE_RECEIPT.json](https://github.com/vubaoha034-hash/shenmei/blob/research/typography-r3-rosanjin-source-20261026/research/typography_r3/ROSANJIN_REMOTE_SOURCE_RECEIPT.json)，运行[Actions #40269497024](https://github.com/vubaoha034-hash/shenmei/actions/runs/40269497024)。版权和跨地区商业再利用尚未独立核验。**这些文件是2025数字描摹，非1908—1909作者亲笔源工程；线宽、复杂度、连接片数不能当笔压或创作步骤。** 已确认三样本的静态宽度P90/P10范围3.19—4.85，仅为候选特征，不构成成功蒸馏；下一步应做同文本中性/书法字体基线与受控对照，筛除汉字普遍性质，再把可证据化的笔画角色操作应用到未见字并盲评。早期只有网页无原件的审计保留历史：[R3_ROSANJIN_SAME_AUTHOR_SOURCE_AUDIT_20261026.json](evidence/vpd/typography_method_distillation_20261026/R3_ROSANJIN_SAME_AUTHOR_SOURCE_AUDIT_20261026.json)。
R3 同字内容对照实测（2026-10-26，已完成）：相同繁体文字的 3 件鲁山人字标 × 3 种真实字体（Noto宋体、黑体、文鼎楷体）× 2 种尺寸匹配方式，共 18 组，另在独立 GitHub Actions 远端复算成功。三件原作的**静态粗细强弱反差和笔画相对重量**在该对照范围内均比基础字体显著，但**轮廓复杂度不稳定，排除“随机毛刺/飞白”作为设计规则**。这只是候选特征，不是原作者创作方法或新字审美成功。完整数据、方法、失败边界：[R3_SAME_TEXT_FONT_CONTROL_RESULT_20261026.json](evidence/vpd/typography_method_distillation_20261026/R3_SAME_TEXT_FONT_CONTROL_RESULT_20261026.json)；远端回执 [ROSANJIN_MATCHED_FONT_CONTROLS.json](https://github.com/vubaoha034-hash/shenmei/blob/research/typography-r3-rosanjin-source-20261026/research/typography_r3/ROSANJIN_MATCHED_FONT_CONTROLS.json)。**下一步必须按字形部件与真实笔画角色定位主辅墨形并对照其他高级书法设计，禁止重做R2那种按方向/长度改线宽的失败路线。**
R4 已执行（2026-10-26）：10款开源表达字体校验，6款完整覆盖三段繁体文字，36次配对实测；像素哈希去重后**仅4组真实独立字形**（Yuji Syuku、Yuji Boku、Yuji Mai 逐像素相同，禁止三算）。三件鲁山人字标在此对照内整体粗细反差与笔重更大，但复杂度不稳定，均非可迁移创作法。下一阶段强制转向**实际设计师创作流程**（已读叶天宇一席演讲全文：选真实参考→双钩拆每笔→数百字草稿→矢量→抽象横竖撇捺点/部首→未见字检验），不得重复R2笔宽变形。证据：[R4_EXPRESSIVE_FONT_AND_REAL_CREATOR_PROCESS_AUDIT_20261026.json](evidence/vpd/typography_method_distillation_20261026/R4_EXPRESSIVE_FONT_AND_REAL_CREATOR_PROCESS_AUDIT_20261026.json)。这是候选流程，不是 AI 创作能力通过。
R5 新字验证（2026-10-26，最新）：在独立研究分支 `research/typography-r5-role-primitives-20261026` 从 SIL OFL 的 Ma Shan Zheng 字体48个训练字提取294条近似端笔样本，训练/未见字完全隔离；**首次云端“绿灯却0样本”错误已留下失败记录并修复为CI硬失败**。随后使用冻结程序在 Figma 独立页 [R5 新字 A/B/C/D 四路实际对照](https://www.figma.com/design/uyDxOoN1iNDPpEHTKSUWg1/?node-id=538-3)，测试未见「泉」「清风入梦」；笔画几何和4组源真实可编辑，但 **C组视觉仍接近A/B基线，明显达不到D专业字形质感，设计方法尚未学会，禁止晋升**。真实回执：[R5_HELDOUT_FIGMA_A_B_C_D_NEGATIVE_20261026.json](evidence/vpd/typography_method_distillation_20261026/R5_HELDOUT_FIGMA_A_B_C_D_NEGATIVE_20261026.json)。**以后首先读取12项错误台账**：[TYPOGRAPHY_DISTILLATION_FAILURE_GATES_R0_R5_20261026.json](evidence/vpd/typography_method_distillation_20261026/TYPOGRAPHY_DISTILLATION_FAILURE_GATES_R0_R5_20261026.json)。不得重复仅笔粗、端点、曲线轻微修整的旧路线；下一步只有具备整笔书写路径、转折、偏旁部件和负形空间的可追溯真实依据，才继续R6方法实验。正式主线任务锁和检查点不变。
R6 字形创作决策模型实验（2026-10-26）：已从 Figma 真实《六島》参考建立**全新目标简体「归雁」**的双路冻结输入：A 仅文本直出，C 同样文本加入主笔／笔势／负形／字间节奏等创作决策，参考字轮廓不传入。真实接口试验结果：Adobe Firefly 两次调用均内部错误；原生 image_gen 输出无关多栏设计教程图（gen_id `e8f39797-6007-487a-b396-48043e8632c4`），**并非「归雁」字稿，A无效**。C 未执行，不能比较或宣称创作方法失败/成功；已停止在当前长对话内重复调用失控 image_gen。Figma 旧文件AI不可用，Weave 未绑定账户；备选 Runway 仅发现可连接，尚未安装或授权。研究分支：`research/typography-r6-visual-decision-20261026`。完整冻结提示词：[R6_VISUAL_DECISION_A_C_FROZEN.json](https://github.com/vubaoha034-hash/shenmei/blob/research/typography-r6-visual-decision-20261026/research/typography_r6/R6_VISUAL_DECISION_A_C_FROZEN.json)；错误收据：[R6_GENERATOR_CONNECTIVITY_AND_OUTPUT_VALIDATION_20261026.json](https://github.com/vubaoha034-hash/shenmei/blob/research/typography-r6-visual-decision-20261026/research/typography_r6/R6_GENERATOR_CONNECTIVITY_AND_OUTPUT_VALIDATION_20261026.json)。下一步仅在获得真正可控的文字图像生成入口及必要账号授权后执行固定 A/C；生成新作品并经过人工审美验证之前不晋升。**严禁重新用端笔统计或数值造字重复 R1–R5。**
R7（2026-10-26）：暂停Figma反复修字与无效生图，改从字由完整教程《海浪》的**共享三点水→各字结构先修→下点折转形成系列风格→右侧复杂度另审**得到可执行有条件规则。GitHub独立测试：在7组事先已知结构词的适用性判断上，永远套用基线3/7、条件规则7/7，未知资料1组拒绝；**测试词的适用标签人工标注，并非盲测，也未生成任何专业字稿，更未证明美感**。唯一研究回执：[R7_SOURCE_CONDITIONAL_DECISION_GATE_20261026.json](evidence/vpd/typography_method_distillation_20261026/R7_SOURCE_CONDITIONAL_DECISION_GATE_20261026.json)。下一步将不同类别的有来源条件决策加入后，必须用新字真实画面和真人审美复验；严禁将条件测试晋升为蒸馏成功。新增收费软件与API预算为零。
R8 真实创作决策补偿实验（2026-10-26）：已阅读字由《字体设计在变化之前，你得先做这一步》完整原文，其《反叛》示例的“**先强化位置对应的主笔→发现重心失衡→另一笔补偿并重新审查整体**”有文字来源，原GIF未成功下载，不冒充作者真实运笔资料。首先在「友」「龙」实验发现主笔放大1.18、上横1.24虽然把物理X重心偏差削减约89%—92%，但轮廓交并比仅0.75—0.81，**以破坏结构换取一项数字改善，已判失败**。因此先冻结较克制参数（主笔1.06/上横1.08、原墨形交并比≥0.90、偏移削减≥25%）再读取全新词「存在」：在未经后验调整的两字上，几何门分别得0.917/0.903交并比，偏移减少90.9%/97.5%。但A/B/C实际视觉差别微弱，**这仍是物理像素约束通过、不是设计审美蒸馏成功**。与R7冲突优先级（共享结构优先；证据缺失就拒绝）完成6组一致性自测，不称独立盲测。权威回执：[R8_CONDITIONAL_COMPENSATION_HOLDOUT_20261026.json](evidence/vpd/typography_method_distillation_20261026/R8_CONDITIONAL_COMPENSATION_HOLDOUT_20261026.json)；独立研究分支：`research/typography-r8-compensation-20261026`。旧错误台账保持，未来禁止再次拿提高单指标、补笔修字冒充创作能力。下一阶段需验证**整字骨架和部件负形决策**的真正跨字美感改善；新增付费预算仍为0。
R9（2026-10-26）真实部件重排/负空间测试，**实际输出但审美不通过**：从徐学成《稳、整、匀》与字由《字体设计在变化之前，你得先做这一步》的可访问正文提炼按结构密度调整左右部件，而不是统一粗细；在读取目标新字前冻结阈值与测试词「沙漠」「深浅」及否定控制「灯火」，随后将合法且 SHA 可追溯的 Hanzi Writer 逐笔轮廓绘成 12 个真实原生矢量，Figma 独立 [R9 三路视觉对照](https://www.figma.com/design/uyDxOoN1iNDPpEHTKSUWg1/?node-id=541-3)。真实截图已目视审计：C 仅改变左右部件的横向仿射比例，不足以形成任何明显高于基线的高级艺术字；没有用户盲评，**严禁把结构规则运行成功当成专业创作成功**。源研究分支 `research/typography-r9-space-decision-20261026`，完整版回执：[R9_STRUCTURAL_SPACE_UNSEEN_VISUAL_NEGATIVE_20261026.json](evidence/vpd/typography_method_distillation_20261026/R9_STRUCTURAL_SPACE_UNSEEN_VISUAL_NEGATIVE_20261026.json)。原专业教程中的阶段插图链接本轮无法稳定取回；没有作者实际草图/修改前后形态样本就不得宣称精确逆向作者操作。错误台账新增F12/F13；下一阶段先补强具有视觉变化的真实作者过程证据，再测实际新作品的跨字审美；停止对同类数字化部件比例继续无限调参。新增收费预算维持0；不得修改正式355锁/377检查点。
R10（2026-10-27，下一步真实材料突破）：**终于获取并校验原设计师/设计机构发表的真实草稿／字形修改前后图像**。在独立研究分支 `research/typography-r10-authored-stage-images-20261027` 冻结四个官方图源，GitHub Actions运行[#40421894959](https://github.com/vubaoha034-hash/shenmei/actions/runs/40421894959)，四张原始图片真实字节下载/解码/尺寸与SHA-256校验全部成功，覆盖汉仪红云隶（古典字形→手绘初稿→定稿）、Typotheque同字红蓝修改轮廓、文鼎方新书C80前后及内部空间处理，3个设计方；**没有复制任何版权图片到公共仓库**。全文实证审读：[R10_真实设计师前后图与实际方法审读_20261027.md](https://github.com/vubaoha034-hash/shenmei/blob/research/typography-r10-authored-stage-images-20261027/research/typography_r10/R10_%E7%9C%9F%E5%AE%9E%E8%AE%BE%E8%AE%A1%E5%B8%88%E5%89%8D%E5%90%8E%E5%9B%BE%E4%B8%8E%E5%AE%9E%E9%99%85%E6%96%B9%E6%B3%95%E5%AE%A1%E8%AF%BB_20261027.md)，原始证据:[R10_REAL_AUTHORED_STAGE_IMAGE_EVIDENCE_20261027.json](evidence/vpd/typography_method_distillation_20261026/R10_REAL_AUTHORED_STAGE_IMAGE_EVIDENCE_20261027.json)。真实证据产生三项**候选而非规则**：手稿中重新塑造整笔/整字墨形、因整套字灰度失衡主动撤回错误的部件变宽决定、字宽收窄时重算内部留白而非整字X缩放。**不得把“修改前后图”臆称为可逆作者笔压/源文件，也不得在未见字审美验证前宣称方法蒸馏成功。** R1–R9失败不删除；禁止继续只调笔宽/比例/重心。下一阶段仅从一张有明确前后图的同字案例冻结具体造型决策，再对不同结构新字开展等预算真实视觉对照/人工评审。预算新增0元，正式任务锁355/检查点377不变。
R10（2026-10-27）：R9之后的真实过程证据缺口已**部分补齐并实际验收原始图像字节**。独立研究分支 `research/typography-r10-authored-stage-images-20261027`，两次真实GitHub Actions先对4张官方/设计师本人发布的图片校验SHA-256、宽高、原始字节，再重复下载做实际内容与红/蓝改稿像素统计，4/4复算一致、CI实体门PASS：[来源哈希回执](https://github.com/vubaoha034-hash/shenmei/blob/research/typography-r10-authored-stage-images-20261027/research/typography_r10/R10_IMAGE_SOURCE_BYTE_AUDIT.json)、[实际修订图证据](https://github.com/vubaoha034-hash/shenmei/blob/research/typography-r10-authored-stage-images-20261027/research/typography_r10/R10_AUTHORED_STAGE_VISUAL_AUDIT.json)。3张有真实草稿/修订阶段（汉仪赤云隶参考字→手稿→成品；Typotheque同字阝红旧/蓝新，先修阶段，不与文字另述的“口”部回退混淆；文鼎方新书Before/After局部开口修正）；1张**仅标准字宽/C80并非时间先后**，排除训练对。底层图像属第三方版权，只存来源URL和衍生哈希/统计，不公开拷贝原像素。已提炼三个可证据化的候选决策（结构先于墨迹、同部件需多字情境审查、压缩字的负形须局部修正），并逐项写明无法证明的作者意图和反例。主线唯一权威记录：[R10_AUTHOR_VISUAL_PROCESSES_VERIFIED_AND_DECISION_CANDIDATES_20261027.json](evidence/vpd/typography_method_distillation_20261026/R10_AUTHOR_VISUAL_PROCESSES_VERIFIED_AND_DECISION_CANDIDATES_20261027.json)。**重要：只是SOURCE_STUDY视觉证据通过，没有实现新字风格转移、真人盲评或设计成功。** 下一步仅锁定其中一种来源/一种决策，进行等成本的真实新字创作对照，不得再重复Figma几何线宽试验；新增收费预算0元。
R10 下一步（2026-10-27，**首次实际看过专业设计师原始阶段图像**）：独立分支 `research/typography-r10-authored-stage-images-20261027` 经免费 GitHub Actions #40421894959 校验四幅设计原图的SHA256与尺寸，另在Opera浏览器对Typotheque的多字修改表逐字视觉检查并执行SHA256校验，共5张可追溯原作者/机构素材：① 汉仪《赤云隶》历史碑帖→灰色字形探索→手绘轮廓首稿→黑色定稿；② Typotheque同一「阝」部件红色Before与蓝色After轮廓叠图，以及一组真正Before/After字族表；③ 文鼎方新书《氣》笔画细节实拍Before/After；④文鼎「仁」「空」标准版/机械横向压缩/C80针对字形重新设计是**三种方案的对照，不是时间顺序的原始创作稿**。来源图片仅在浏览器和临时下载器读取，不将他人受版权保护的原图放进公共GitHub；任何原作者笔压、贝塞尔操作及商业复用权均未证实。最新证据：[R10_REAL_AUTHOR_STAGE_VISUAL_DECISION_AUDIT_20261027.json](evidence/vpd/typography_method_distillation_20261026/R10_REAL_AUTHOR_STAGE_VISUAL_DECISION_AUDIT_20261027.json)。结论：真正可学习的机制是**整体草稿先定形、局部白口按拥挤情况条件修正、同部件跨众字一致性反复审查及必要时撤销原设计**；当前仅完成 `SOURCE_STUDY` 与 `METHOD_CANDIDATE`，**仍没有未经训练新字上的专业审美提升与真人盲评，不许晋升规则**。之前R1–R9通过横向拉伸、端点加粗等几何手段的失败继续有效；错误台账新增F14，后续必须从真实作者阶段图出发，不能拿商业字库的局部编辑冒充艺术字造型整体方法。**新增费用0，正式355任务锁与377检查点不变**。
R10（2026-10-27，实际作者前后图核验，**不是新文字审美成功**）：独立研究分支 `research/typography-r10-authored-stage-images-20261027` 实际下载复核汉仪、Typotheque、文鼎共4张原始视觉过程图，4/4 SHA-256 与尺寸通过；其中2张确认同一字形的 BEFORE/AFTER（Typotheque '阝/那' 红蓝重叠、文鼎方新書局部内弯修正），1张汉仪是历史参考→构形草稿→成品的阶段说明，另1张文鼎标准/C80只是字宽版本，不得算真实修订。对Typotheque主要红蓝重叠区域，经最长边1600像素缩放后测得红边缘至蓝边缘中位14像素、90分位18像素——只是**实际改动证据，不是通用变形参数，更不是美感证明**。原文确认过度拓宽共用`口`部件导致数千字一致性问题最终返工，支持‘**跨字族审查→局部回改→必要时撤销**’的决策机制。R10权威数据回执：[R10_AUTHORED_BEFORE_AFTER_VISUAL_VERIFIED_20261027.json](evidence/vpd/typography_method_distillation_20261026/R10_AUTHORED_BEFORE_AFTER_VISUAL_VERIFIED_20261027.json)，创作决策分解：[R10_DESIGNER_EDIT_DECISIONS_FROM_OBSERVED_IMAGES_20261027.md](https://github.com/vubaoha034-hash/shenmei/blob/research/typography-r10-authored-stage-images-20261027/research/typography_r10/R10_DESIGNER_EDIT_DECISIONS_FROM_OBSERVED_IMAGES_20261027.md)。GitHub不存版权原图，只存原始来源URL、SHA和聚合统计。**没有真实新字高质量输出／用户盲评，尚未蒸馏成功**。下一步只研究真实作者‘同部件在不同字中的适应与回滚’，禁止用源像素14px作为普适变形量或另开付费软件。正式任务锁保持不变。
R11（2026-10-27）：从R10已完成的4份真实来源中纠正**成品展览≠同字修订**的误判，再核验 Typotheque 设计团队本人发表的红色「那」Before / 蓝色「那」After 与右「阝」部件修订，另取同页多字前后对照及真人红线复查照。R11 GitHub Actions `40441785892` **真实下载解码3/3张原图、核对SHA与尺寸**，版权原始图片未提交仓库。关键《那》原始图SHA256 `f4505122dd0c0386252096a757d861a4652fa570f44f304fc1fd86af3e256ef1`；检测到的前后彩色图形bbox约154×151与155×150、墨迹像素10563与10485、粗配准IoU≈0.8674；这些是有误差的颜色分割指标，**不能当成作者使用的数字/真实运笔记录/美感增益**。原作者文字解释：同偏旁需跨数百、数千字审查，他曾因「口」过宽而在后期回改；真正值得研究的是**多字系统复核→局部轮廓修正→保留整字稳定**，而不是继续按统一宽度拉伸。完整记录：[R11_REAL_AUTHOR_BEFORE_AFTER_AND_FAMILY_REVISION_20261027.json](evidence/vpd/typography_method_distillation_20261026/R11_REAL_AUTHOR_BEFORE_AFTER_AND_FAMILY_REVISION_20261027.json)，分支 `research/typography-r11-authored-delta-20261027`。**阶段仍是SOURCE_STUDY，未生成新字、未通过真人审美、未蒸馏成功**。字体系列改进与目标《六島》表现性书法风格不同，后续仍必须找到同字的表现性艺术书写草稿—中间稿—定稿实际对应图，再锁定新字验收。原有正式锁不动；新增软件/API预算0。
R12（2026-10-27）首次取得**真正表现性中文字标作者完整过程证据**，不再把正文字体细部修订冒充《六島》式字标：从梁志坚本人《放肆喜欢》2019设计长文，冻住原始9张/项电脑雏形→初稿→多版修改喜字→定稿→105帧过程动图，全部原始字节SHA256与尺寸解码真实通过；另从张家佳本人《上座》Behance提供的3幅字标设计过程图真实核验，合计**12/12个来源文件，属于2个项目，不是12个独立设计案例，105帧动图也不是105次独立创作**。免费 GitHub Actions 实跑[来源校验](https://github.com/vubaoha034-hash/shenmei/actions/runs/40442819225) PASS，证据分支 `research/typography-r12-expressive-author-stages-20261027`，来源原件均未上传至公共仓库，公开只存图像来源、SHA与聚合审计。两条作者确实执行过的高层创作操作候选：①对过密且重复的「喜」修改**笔画拓扑关系**（断开、合并、共用、删冗余横笔但保持识别），不是拉伸笔宽；②对笔画疏密悬殊的「上座」，**改变两字整体组合方式**并绘制连贯书写笔势，非给两字加同一套数值。权威回执：[R12_VERIFIED_REAL_ARTIST_LETTERING_STAGES_AND_NEW_DECISIONS_20261027.json](evidence/vpd/typography_method_distillation_20261026/R12_VERIFIED_REAL_ARTIST_LETTERING_STAGES_AND_NEW_DECISIONS_20261027.json)。**真实研究级别仅 SOURCE_STUDY + METHOD_CANDIDATE，无新字生成/真人盲评/蒸馏成功证明**。下个试验拟锁定「上座」的整体组合决策在完全未见的「山海」上检验，同时使用字势均衡的「风云」作防误用对照；不走R1–R9全局线宽、端部或横向仿射老路线，不重新生图再依赖Figma描摹。版权原图不作公开训练或商业转用，新付费费用0；正式视觉任务锁355/检查点377仍由原记录控制。
R11 补充来源审计（2026-10-27，**不覆盖更新的R12艺术字资料**）：从设计师甘薇云《左體》本人发布的多阶段「獨/立」造型图和 justfont《金萱》明确标前后差异的原图新增4个官方来源文件。Github Actions #40445493208 实际下载解码4/4，单张彩图两次下载视觉像素SHA一致；PNG透明黑底误计为墨色的首次错误已存证并改为透明层合成白底再统计。由真实一手资料形成4条情景触发/回退候选：意图先定书写语言、长文阅读可回退过强的弯钩、加粗字形先救负空间、跨字复核可撤回不适用的部件特征。**仅作者案例研究，不是可自动生成新字的已验证程序**。权威补充记录：[R11_REAL_DESIGNER_REVISION_AND_CONDITIONAL_DECISION_20261027.json](evidence/vpd/typography_method_distillation_20261026/R11_REAL_DESIGNER_REVISION_AND_CONDITIONAL_DECISION_20261027.json)；独立分支 `research/typography-r11-verified-creative-revisions-20261027`。
R13（2026-10-27，**已实际画面隔离测试但审美负面**）：依赖R12真实作者《上座》的整词上下组合思路，在读取视觉输出之前冻结「山海」（3对10笔）与否定控制「风云」（4对4笔），使用同一套合法自带楷体、同字同字号，不经Figma/收费接口，制作横向独立与上下组合四格真实PNG。首版居中程序把「风云」横向版画出界，**空白面板不可计入结果**；修复后四格均有真实笔画像素并逐格目视复核。最终：上下摆放并不生成原作者的整笔共势或高级艺术字，横向「山海」更自然；且「风云」竖排未必差，说明笔画疏密不能独立决定优秀布局。**不允许把普通字体堆叠冒充‘蒸馏成功’**。依据、SHA、实际视觉结论：[R13_REAL_WHOLE_WORD_LAYOUT_NEGATIVE_20261027.json](evidence/vpd/typography_method_distillation_20261026/R13_REAL_WHOLE_WORD_LAYOUT_NEGATIVE_20261027.json)；独立试验分支 `research/typography-r13-whole-word-composition-20261027`。后续只允许在作者真实阶段图证据下研究跨字连贯主笔/字形拓扑改写，不能再加几何换位新花样；新收费0，正式锁355/检查点377不动。
<!-- END_TYPO_METHOD_TRANSFER_GOAL_20261026 -->



<!-- LIU_VPD_IMAGE_GENERATION_GUIDE_20261012 -->
图片生成正式流程名称：**《刘先生 VPD 图片生成》**，操作说明与完整出图/审核/原件保存链：[docs/刘先生 VPD 图片生成.md](docs/%E5%88%98%E5%85%88%E7%94%9F%20VPD%20%E5%9B%BE%E7%89%87%E7%94%9F%E6%88%90.md)。新聊天在实读最新 HEAD、PROJECT_CONTROL_ADAPTER、VPD_PROJECT_ROADMAP、CURRENT_TASK_LOCK 与 LATEST_CHECKPOINT **之后**，按当次任务相关范围使用该文档。该文件不是第二个任务锁、已安装的第二 Skill 或已部署的自动化插件，不重做已完成成果。
历史《地图以外》X胜出表述已被用户正式纠正：**Y更好、X有AI味道**。参见 evidence/vpd/dituyiwai_photo_20261011/V2_AB_HUMAN_CORRECTION_Y_PREFERRED_20261011.json。2026-10-12 已另有 Figma R2 (71:2) 局部修订回执，**没有真人整体定稿**；旧聊天与过时快照不得覆盖它。
<!-- END_LIU_VPD_IMAGE_GENERATION_GUIDE_20261012 -->


<!-- LIU_PLUGIN_REQUEST_REFERENCE_RUNTIME_20261006 -->
插件新参考入口补充：先读最新原生锁，再读 `plugins/visual-aesthetic-workflow/REQUEST_REFERENCE_RUNTIME.json` 和 `plugins/visual-aesthetic-workflow/v0.1.2/SKILL.md`。同一私有插件运行0.1.2、Site第4版已发布，ChatGPT新聊天真实compile_transfer_plan已返回地图以外/for liuxiansheng请求草稿；管理页刷新工具目录已实测。旧“修改地图文字”聊天仍报告内部工具错误，未声称已恢复，失败记录保留；可用验收入口https://chatgpt.com/c/6ac4d667-64d0-83ea-a6a6-782cf1719f03。新参考用user_request及真实reference_source，不重绑山野集，不套用其绿底模板；SHA未知可省略，插件仍未看图，制作前须实际核对原件。此为调用修复，不改变主线、已认可摄影、S7真人PENDING、计数或唯一下一动作；旧CURRENT_RELEASE、连接证据与S7入口按原字节作历史保存，不覆盖此运行补充。完整证据目录见runtime pointer；工程及新聊天调用通过不作审美通过。
<!-- END_LIU_PLUGIN_REQUEST_REFERENCE_RUNTIME_20261006 -->

<!-- LIU_PLUGIN_ACTUALLY_CONNECTED_20261006 -->
刘先生·视觉设计工作流已在本ChatGPT账户实际安装并连接，至少一次真实get_current_workflow调用及原始tool结果绑定已通过独立核对。先读本分支最新原生锁和当前receipt，再读 plugins/visual-aesthetic-workflow/CONNECTION_VERIFICATION.json 与 evidence/vpd/codex_takeover_20261003/liuxiansheng_content_transfer_20261005/plugin_installation_20261006/README.md。旧S7_FINAL_REUSE.md、CURRENT_RELEASE.json及HTTP401记录按原哈希冻结，表示当时未验证，不覆盖本次已授权安装与真实运行。此连接记录不改变作品、主线、真人门、版本预算或唯一下一动作。实际入口https://chatgpt.com/plugins/plugin_asdk_app_sites_e3827109d9348191a163f8f785ef2b4c?directoryTab=personal，选择“在聊天中试用”或新聊天@选中插件后调用get_current_workflow；生产反馈写入/回读及当前Codex会话直接工具发现仍未验证。
<!-- END_LIU_PLUGIN_ACTUALLY_CONNECTED_20261006 -->

<!-- INDEPENDENT_WORKER_CURRENT_ENTRY_20261003 -->
最新授权与 worker 入口：先读原生任务锁，再读 `continuity/vpd/codex_takeover_20261003/WORKER_CURRENT_REUSE.md`。2026-10-04刘先生明确授权同一方向持续制作、独立审核和修复，直到内部审核通过；本次授权取代三版两修订停止上限，保留累计版本、全部失败、主线、摄影保护与真人最终验收。授权原话见 `continuity/vpd/codex_takeover_20261003/CONTINUOUS_REPAIR_AUTHORIZATION_20261004.json`。V3真人REJECTED及V1–V3真实AI_FAIL不改写；冻结7fd7777f摄影认可不撤回。worker不能改主线，根执行者唯一写业务状态。下方三版耗尽、等待追加范围或旧验收下一动作均为历史，不覆盖当前原生锁。
<!-- END_INDEPENDENT_WORKER_CURRENT_ENTRY_20261003 -->

<!-- CHAZUO_DRIVE_PRIMARY_ARCHIVE_ENTRY_20261003 -->
历史摄影归档阶段（2026-10-03）：`continuity/vpd/codex_takeover_20261003/SOURCE_RECOVERY_DRIVE_REUSE.md`保留原件、局部摄影修补、透明层、素材及旧三版的Drive文件ID、revision与SHA。摄影7fd7777f后来已获真人认可；不再等待这个历史摄影验收。当前成品、审核与唯一下一动作先从原生锁和WORKER_CURRENT_REUSE.md读取；Drive为图片主存储，Figma源文件保留。
<!-- END_CHAZUO_DRIVE_PRIMARY_ARCHIVE_ENTRY_20261003 -->

<!-- FIRST_PHOTO_LOCAL_RECOVERY_ENTRY_20261003 -->
历史摄影恢复阶段（2026-10-03）：`continuity/vpd/codex_takeover_20261003/SOURCE_RECOVERY_REUSE.md`记录第一张局部去字背景重建及一次修补工具操作；不是找回隐藏无字原件。摄影7fd7777f已获真人认可并冻结。旧三版海报否决保留；持续同方向文字制作权限已在当前授权覆盖，后续只从原生锁接续，不执行历史等待步骤。
<!-- END_FIRST_PHOTO_LOCAL_RECOVERY_ENTRY_20261003 -->

<!-- INDEPENDENT_REVIEW_SKILL_ENTRY_20261003 -->
多角色与实际审核skill入口：读取原生任务锁及下方原件纠偏后，读 `continuity/vpd/codex_takeover_20261003/REVIEW_FIRST_REUSE.md`。已实际完成独立五图像素审核及真人结论隐藏后的核对；官方design-critique固定版本与项目必要适配可复用，仍是实验方法。摄影成功与文字失败分别保留，当前作品仍为AI_FAIL/真人REJECTED，唯一下一动作及既有预算不扩大。
<!-- END_INDEPENDENT_REVIEW_SKILL_ENTRY_20261003 -->

<!-- CODEX_REFERENCE_FEEDBACK_CORRECTION_20261003 -->
最新纠偏先读 `continuity/vpd/codex_takeover_20261003/RECONCILE_REFERENCE_AND_FEEDBACK.md`。已通过网页实际原件和全幅像素对比确认：用户评价的第一张为网页生成图1（e7af9c9e…），与16:24上传图（a579e846…）像素相同；它不是R4。旧R4摄影认可绑定已撤回，三版保留为AI_FAIL和真人否定结果。不得只凭旧恢复回执重新认定认可底图，也不得自动增加第四版。
<!-- END_CODEX_REFERENCE_FEEDBACK_CORRECTION_20261003 -->

<!-- CODEX_BOUNDED_CHAZUO_DELIVERY_20261003 -->
本轮已明确授权Codex制作茶作成品及Figma写入，取代该任务旧零额度/Chat-only限制；历史限制仍保留原范围。按下文读取当前任务锁后，若 `codex_takeover.task_id` 为 `VPD-CHAZUO-CODEX-COMPLETE-POSTER-20261003-01`，继续读 `continuity/vpd/codex_takeover_20261003/REUSE_FINAL.md`：真实成品、源节点、精确PNG恢复、独立审稿、依赖和失败边界均在此。三版/两修订已用尽，当前动作以任务锁为准，不按历史下一步再出图。
保存与冷进入补充：接着读 `continuity/vpd/codex_takeover_20261003/ENTRY_RECOVERY_NOTES.md`。其中保留首次新克隆的真实哈希失败、限定字节保存修复、全新上下文的实际PNG恢复验证、源节点真实类型与冷环境字体加载条件；这些工程验证不把AI_FAIL改为通过。最终审查与恢复证据以最新原生receipt引用为准。
<!-- END_CODEX_BOUNDED_CHAZUO_DELIVERY_20261003 -->

<!-- UNIFIED_USER_INSTRUCTION_20261003 -->
## 最新用户执行偏好与总审核权限（2026-10-03）

- 本项目与统一指挥管理的其他项目一样，尽量使用 **GPT-6.1 Sol，Max 思考强度**。这项当前用户偏好优先于旧模型/思考强度默认值；实际模型与强度须从可观察的执行设置核对，无法使用时如实记录原因，不得只在提示词写名称就宣称已切换。
- 统一指挥负责审核、验收、调度和推进既有授权任务。**只有刘先生明确要求，才可改变项目主线目标或既定主线路线。** 测试失败、审稿意见、新资料、旧任务结束和审核者的个人判断，均不单独授权总审核者改主线；原协议内已经授权的有界修订继续按原范围执行。
- 这次只更新上述执行偏好与审核权限；当前任务、唯一下一动作、候选身份、已认可成果、预算、真人门和自动化暂停状态仍以本项目原生状态为准。模型偏好本身不要求切换 Chat/Work，也不启动或重跑业务。
- 本次指令与接续定位：`continuity/vpd/mainline_recovery_20261002/UNIFIED_COMMAND_USER_INSTRUCTION_20261003.json`。此回执不是第二个任务索引，也不宣称五个运行会话已经切换模型。
<!-- END_UNIFIED_USER_INSTRUCTION_20261003 -->

版本：`4.2.2`
状态：`MANDATORY`

<!-- VPD_TASK_LOCK_ENTRY_V1 -->
当前用户锁定主线：`continuity/vpd/MAINLINE_LOCK_20261001.md`；机器执行合同：`continuity/vpd/MAINLINE_CONTRACT_20261001.json`。在既有基础上按完整成品→内容→画幅→第二风格→交付推进。仅凭实际测试失败/无收益等证据，按合同作有界局部修订；不得因旧任务、教程或临时偏好改主线。历史结果保留，单一任务锁不变。

## VPD 视觉蒸馏任务专用入口

本段适用于视觉蒸馏系统的接管、继续、完整流程和状态修复；其他路线照其范围执行。
权威仓库为 `vubaoha034-hash/shenmei`，工作分支为
`visual-program-distillation-v2-photography-design-20260814`，新聊天先核对该分支最新提交。
先读 `PROJECT_CONTROL_ADAPTER.json` 的 `task_lock` 与 `workflow`，再读：

1. `VPD_PROJECT_ROADMAP.md`：完整步骤、交付物、通过条件、提速预算和新聊天接续方式；
2. `continuity/vpd/CURRENT_TASK_LOCK.json`：唯一当前任务、进展与下一动作；
3. `continuity/vpd/LATEST_CHECKPOINT.json`：最新检查点和本步骤所需证据。

```bash
python scripts/verify_visual_memory.py --vpd-state --status-card
```

检查失败即停止写入或出图。当前下一动作只从任务锁读取，不执行历史文件的旧下一步。
同一提交已核验信息复用，历史正文按当前任务需要读取；不要每轮重做全量接管。
写入前再次读取远端；并发前进先协调，禁止覆盖。发布后独立回读，未回读不声称同步。
完成一项就更新同一任务锁、检查点和既有账本；汇报已完成、未完成、下一步和保存版本。
反馈图不自动成为母参考，未知旧执行不自动重放；本地检查不证明模型绑定或审美通过。
<!-- END_VPD_TASK_LOCK_ENTRY_V1 -->

## 0. 审美 Skill 设计治理｜全仓强制前置

凡涉及以下任一任务，**在读取具体视觉 Skill 之前，必须先读取**：

`AESTHETIC_SKILL_DESIGN_CHARTER.md`

适用范围：

- 新建视觉 / 审美 / 海报 / 品牌 / 图片生成 Skill；
- 修改现有视觉 Skill；
- 从成熟视觉 Skill 派生新 Skill；
- 修改 Prompt Compiler、Variation Engine、Color Engine、Typography、Texture、Quality Gate；
- 因“结果不好看”准备继续增加视觉规则、阈值、分类、validator 或失败码。

核心治理要求：

1. 审美 Skill 优先设计成**紧凑 Prompt Compiler**，不是规则百科；
2. 先找 5—8 个高杠杆视觉变量，再停止加规则；
3. 必须区分 `correctness problem` 与 `taste problem`；工程验证可以防错，不能证明好看；
4. 已经优秀且成熟的上游视觉 Skill，默认采用 **upstream 100% + thin wrapper**，不得轻易重写；
5. 如果出现“规则越来越多，结果越来越僵 / 越来越模板化”，默认动作是删规则或回退，而不是继续补规则；
6. 若必须大幅改变成熟 Skill 的构图、色彩、字体、纹理、variation 或质量门槛，应新建实验 Skill，而不是污染稳定 Skill。

本节优先于各视觉路线内部的“为了更高级而加规则”类做法，但不覆盖事实正确性、安全、品牌名、人物身份、用户明确尺寸等 correctness 硬约束。

## 1. 最高优先级路由

任何执行者先判断任务类型。当前仓库包含六条路线：

1. 每日或单次完整餐饮品牌案例；
2. 单张餐饮海报与独立视觉素材；
3. 明确要求可编辑 Figma 源文件的正式品牌系统；
4. 私人审美评分与校准；
5. 餐饮经营总控；
6. 旅行视频 / 照片的极简 Zine 转换。

同一任务涉及多条路线时分别通过相关硬门槛。根入口优先于旧子目录入口。

## A. 每日或单次完整餐饮品牌案例｜V4.2 主流程

适用：

- 每天 09:00 自动生成品牌案例；
- 系统自主确定品牌与品类；
- 一套十张独立品牌案例；
- 空间、门头、定制字标、故事、产品、海报、包装和运营触点的完整展示；
- 小红书品牌设计案例；
- 用户要求参考品牌案例图采用多模块整版呈现；
- 用户明确说不用 Figma。

必须读取：

1. `DAILY_AUTOBRAND_SYSTEM_V4.md`；
2. `rules/DAILY_CASE_10_IMAGE_STRUCTURE_V4.md`；
3. `rules/BOARD_LAYOUT_PRESENTATION_RULES_V4.md`；
4. `rules/BRAND_WORDMARK_AND_TYPOGRAPHY_RULES_V4.md`；
5. `rules/DAILY_CASE_QUALITY_GATE_V4.md`；
6. 每日任务另读 `schedules/DAILY_0900_BRAND_CASE_V4.md`。

强制结果：

```text
1 个完整餐饮品牌
→ 定制变形中文品牌字标
→ 10 张独立 3:2 横版案例展示图
→ 每张 1 个主视觉中心 + 0—3 个辅助模块
→ 空间、字标、故事、产品、海报、包装、运营触点和总结全部覆盖
→ 配角物料跨页去重
→ 大多数页面极少文字
→ 无可见页码与序列号
→ 建立品牌专属色彩人格与十张色温节奏
→ 逐张审查
→ READY
```

### V4.2 最高优先级硬规则

1. **十张必须是十个独立图片文件。**禁止用一张十页合板、十宫格或长图代替。
2. **默认单页为 `3:2` 横版，推荐 `2400 × 1600 px`，PNG。**用户指定尺寸时以用户要求为准。
3. **页面内禁止出现 `01`、`02`、`03` 等页码、章节序列号或提案式编号。**内部 manifest 可以记录顺序，但不得把编号画进图片。
4. **品牌 Logo 必须是设计过的定制字标。**不得直接套用现成黑体、宋体、圆体、书法体或其他字体冒充 Logo。
5. **只有品牌主角允许适度跨页重复。**主角包括主字标、核心超级符号、主产品和核心空间气质。
6. **配角物料原则上只重点展示一次。**袋子、围裙、杯子、菜单牌、桌牌、小票、会员卡、吊牌、餐具包等一旦在专属页面完整展示，后续页面不得再次作为主要内容。
7. **全套仅允许 1—2 张中等文字密度页面。**其余页面以图像、比例和留白表达，禁止每页大段解释。
8. **统一不等于模板复制。**十张至少使用四种版式骨架，并形成满版、留白、产品主导、空间主导和系统主导之间的节奏变化。
9. **禁止连续复用近期项目的中心语义。**近 7 个有效项目中已使用的品类、品牌名核心字、视觉隐喻、品牌人格与主色逻辑必须主动避让。
10. **不得把暖色与暖米色底当作默认审美答案。**每个项目必须先定义品牌色彩人格，再确定页面底色、图像色温、文字对比和强调色。
11. **十张必须形成可见的色温与明度节奏。**除非有明确品牌证据，暖米色、奶油色、黄棕纸张底不得超过 3 张；至少 4 张不得使用暖米或奶油底；至少 2 张使用冷色或中性底；至少 1 张使用深色、低明度或强对比背景。例外必须写入 `CASE_MANIFEST.json`。
12. **同一页面不得让主图、背景、文字和强调色全部同时偏暖。**至少有一层承担冷、中性或深色对比。
13. **整套至少使用三类背景家族。**可从冷白、灰白、雾蓝灰、浅灰绿、矿物灰、深灰、炭黑、中性纸白、品牌色实底和局部暖底中选择。
14. **最近 7 个项目必须审计色温惯性。**若最近两套均为暖调，下一套必须优先采用冷、中性或深色主导方向，除非用户明确指定暖调。
15. **参考图只用于学习展示机制。**不得复制参考品牌名、字标、超级符号、水印、设计公司页脚、二维码、联系方式或完整商业外观。

### 色彩策略最低凭证

生成前必须在内部 brief 或 `CASE_MANIFEST.json` 中记录：

```text
brand_color_personality:
primary_palette:
background_families:
temperature_map:
warm_dominant_board_count:
contrast_plan:
recent_color_repetition_check:
color_exception_reason: null
```

没有这些字段，不得开始十张扩展。

### 工具边界

- Figma 不是依赖、前置条件或验收条件；
- 允许图像生成系统直接生成完整品牌案例展示页；
- Adobe、Photoshop、Illustrator 均为可选后期工具；
- 不得要求用户自行拼版；
- 生成完成不等于质量通过。

## B. 单张餐饮海报与独立视觉素材

适用：单张海报、单个产品主视觉、独立海报备选或品牌项目中的单素材。

读取：

1. `AESTHETIC_SKILL_DESIGN_CHARTER.md`；
2. `skills/restaurant-poster-art-director/SKILL.md`；
3. `generation/RESTAURANT_POSTER_IMAGE_RULES_V1.md`；
4. `config/restaurant-poster-generation.v1.json`；
5. calibration 文件。

独立海报的多风格配额不得套用到 V4.2 十张品牌案例内部。`READY_TO_POST` 必须通过产品、文字、实际尺寸与 100% 检查。

## C. 可编辑 Figma 正式品牌系统｜仅明确请求时使用

只有用户明确要求以下内容时，才进入旧 Figma-first 路线：

- 可编辑 Figma 文件；
- 组件库、变量和 node ID；
- 生产级设计协作文件；
- 明确要求 Figma 三页验证或十页 Frame。

读取：

1. `AESTHETIC_SKILL_DESIGN_CHARTER.md`；
2. `restaurant_design_system/START_HERE.md`；
3. `restaurant_design_system/FIGMA_FIRST_NO_ADOBE_PIPELINE_V1.md`；
4. 该路线要求的 Skill、配置与 validator。

不得把该路线强加给每日品牌案例、直接整版生成或用户明确说“不用 Figma”的任务。

## D. 私人审美评分

读取：

- `AESTHETIC_SKILL_DESIGN_CHARTER.md`（仅当任务涉及修改/新建审美 Skill 时强制；普通评分不必重复读取）；
- `skills/personal-aesthetic-critic/SKILL.md`；
- 品牌项目需要正式量化时读取 `skills/restaurant-brand-aesthetic-gate/SKILL.md`；
- rubric、penalties、schema 与 calibration。

快速视觉判断不必伪装成正式评分。锚点不足时 `personal_fit` 必须为 `null`，未验证结果不得标记 `OFFICIAL`。

## E. 餐饮经营总控

凡涉及菜单、价格、活动、会员、供应商、厨房、前厅、排班、损耗、食安、试点或多店推广，读取：

1. `restaurant_operations_system/START_HERE.md`；
2. `skills/restaurant-operations-master/SKILL.md`；
3. 当前阶段工作流、配置、真实经营数据与当前有效法规证据。

没有真实基线只能诊断；食品安全、负贡献或高峰不可执行是 `BLOCKER`；没有试点 PASS 不得 `ROLLOUT_READY`。

## F. 旅行视频 / 照片极简 Zine

适用：

- 旅行视频帧或旅行照片转视觉；
- 用户点名 `gc-minimal-zine-poster` 并要求旅行影像适配；
- 用户使用中性入口 `$zine`；
- 同一批照片要求每张独立生成；
- 用户明确指定 `16:9` 或其他比例。

必须读取：

1. `AESTHETIC_SKILL_DESIGN_CHARTER.md`；
2. `skills/zine/SKILL.md`；
3. `skills/gc-travel-zine-poster-v1/SKILL.md`；
4. 该 Skill 要求读取的 `skills/gc-travel-zine-poster-v1/UPSTREAM_SKILL.md`。

### 最高优先级原则

- 本地实现是上游 `gc-minimal-zine-poster-v0-1` 的 **thin wrapper**；
- 不得再恢复本地旅行视觉家族、55% 照片占比阈值、结构转译最低要求、`REJECTED_*` 审美失败码、cheapness detector 或大型 reference-conditioning 规则；
- 只允许必要适配：画幅、真实照片作为上游 Image Anchor 的素材来源、用户明确提供的事实地名、多图独立交付；
- 上游 Prompt Compiler、Variation Engine、Color Engine、Typography、Texture、Negative Constraints、Workflow、Quality Gate 保持原样；
- `$zine` 只负责中性路由，不得作为视觉风格词进入最终图像 Prompt；
- `$tear-paper` / “撕纸效果”已废弃为生产入口。收到旧调用时不得直接生成，只能提示切换到 `$zine`；
- 若未来需要大幅改变上游审美机制，新建实验 Skill，不得继续修改 canonical wrapper。

## 混合任务

经营结论和视觉交付分别通过独立闸门。漂亮设计不能覆盖亏损、食安或执行问题；经营逻辑也不能覆盖错字、产品错误、结构错误、色彩同质化和弱品牌逻辑。

## 隐私

仓库为 public 时，不上传逐笔流水、员工个人信息、供应合同、私人照片、账号或其他敏感数据。只提交脱敏模板、聚合证据和稳定的非敏感设计记录。
