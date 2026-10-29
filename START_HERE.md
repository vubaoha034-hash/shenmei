# START HERE — 强制执行入口

<!-- PROSPECTIVE_PILOT_EXPLICIT_CARRIER_PRECHECK_AFTER_FAIL_20261029 -->
**2026-10-29｜新的未见字组《纸屿茶舍》前瞻A/B一枪一稿实测：失败在生成通道、不是审美评审。** 已先于生成提交冻结协议 `d4e3a5fc921b635d6d20f02a3af0bc9e8c96c3b4`，要求独立A普通宋体、B有条件字形设计，各1张，原文字「纸屿茶舍」，3:2横幅透明，错字/多栏立即拒绝、不重抽。**实际A仅生成了「云栖山房」研究信息图，B仅生成了「青山听风」研究信息图，两张都不是目标中文字标，0/2有效，审美比较无效，没有再次重抽。** 两张各1536×1024 RGBA的真实原图SHA分别为 `1f0fa54a9053b59385a5d0ffae19fa297613bbebf15598b7d1767976c8bf0f97` 和 `de7c73ed1176b542867949c826c3529e6916ebfe73f5a716ee7f33691d848691`；原图内部打印的数字/ZIP/“GitHub已提交”不是真实工具结果。承载问题：本轮image_gen工具未提供可复核显式输入的提示词字段，不能证明冻结文字真正被生成器执行；不能认作模型审美失败或迁移验证完成。失败[真实两臂与最终审计](research/prospective_wordmark_pilot/FINAL_ACTUAL_FAILURE_AND_CARRIER_CORRECTION_20261029.json)。**新的承载只读预检已通过**：在连接的普通ChatGPT新聊天真实填入冻结的完整258字A指令，DOM逐字读回一致，随后清空；**发送0消息、额外生图0、仅验证输入可用，未验证生图输出。** [普通聊天显式提示词预检回执](research/prospective_wordmark_pilot/EXPLICIT_PROMPT_COMPOSER_PREFLIGHT_20261029.json)。下轮只有采用新的独立事前冻结协议、确证显式提示词实发且原样读回后，才允许另起一次受控前瞻试验；现有两臂不可回填或重抽。原正式任务权威仍在 `visual-program-distillation-v2-photography-design-20260814` 的Rev355/Checkpoint377，`render_allowed=false`，S7真人待审；本研究**未改Figma，未提升规则成熟度**。
<!-- END_PROSPECTIVE_PILOT_EXPLICIT_CARRIER_PRECHECK_AFTER_FAIL_20261029 -->

<!-- R23_R24_CROSS_WORD_RETROSPECTIVE_REAL_REPLAY_20261029 -->
**2026-10-29 当前新进展：对旧R23《松间见月》与R24《溪桥听雨》两组不同汉字的真实成品图做新的跨字组技术回归（不是重复旧实验或新造字）。** 已从用户Library真实取回各A/B共4份1672×941 RGBA透明原PNG，4/4 SHA256逐字节对上历史审计。事前冻结测量协议（commit `f44d3cd9aaba679cd10de887a420e75c28817e7c`），真实测试白底灰度深墨、墨高256/96/64/32px的字距投影：**R23 A/B在64px均有3处完整空列分隔；R24 A有3处、R24 B仅1处（32px仍1处）。** 两个B墨迹密度均低于A，因此“总密度越高必更挤/越难认”不成立；应改成对有独立字形的字标出现低于预期完整分隔时**触发人工看字间/中宫边界风险，不自动判FAIL或错字**。四图、审计代码、全尺寸与小尺寸对比PNG、数字结果已在当前聊天自包含9文件ZIP真实交付；隔离新解压目录重跑结果**原JSON逐字节一致**、自测PASS、ZIP CRC PASS。注意R23B与R24B提示词不同且都是一次黑箱生成，属历史回溯核验，不能推断原作者设计方法或AI前瞻迁移成立。旧“简兮摄影”真人票仍0，13项11已核查/2待定，`VALIDATED_RULE=false`。没有新ImageGen、没有Figma、没有R30或正式任务锁更新；生产Rev355/Checkpoint377、S7人工门待决。实测论文档：[四份原图跨字组审计与可执行条件否决线索](research/transfer_regression/README_R23_R24_ACTUAL_REPLAY_AND_CONDITIONAL_NEGATIVE_FINDING_20261029.md)。
<!-- END_R23_R24_CROSS_WORD_RETROSPECTIVE_REAL_REPLAY_20261029 -->

<!-- JIANXI_ACTUAL_PIXEL_AUDIT_20261029 -->
**2026-10-29｜独立接管后实际读取并核对《简兮摄影》私有匿名对照原PNG，非盲测像素审计。** 原聊天显示的1550×650 PNG实际重算SHA256与封存值`a6f40aa89c181050cc7f6b2203f9883c2b9026bc7e85e1b1a99621ff3031abba`完全一致；同墨迹高度140px，甲黑墨bbox467×140、密度37.63%，乙576×140、27.54%。**这些是字重、留白和宽度的真实几何差异，不是“甲/乙更好”或识字认证**。非盲助手已经接触作者客户选择，不能替真人或干净AI模型投票；用户盲评仍0，13项中2项继续未知。已经保存真实连接浏览器读取与数值测量、64/32px图像检查边界，附可在私有原PNG上复算的本地校验工具（代码为本轮独立生成；只做了合成图自测，不能冒充已于本地重放私有PNG）。研究不揭盲、不上传原作者像素、不重新启动旧字实验、正式设计锁仍355/377。审计：[真实像素核验与专业判断限制](research/fair_pair_screening/JIANXI_PRIVATE_PANEL_ACTUAL_PIXEL_AUDIT_20261029.json)。
<!-- END_JIANXI_ACTUAL_PIXEL_AUDIT_20261029 -->

<!-- JIANXI_VALID_EVALUATION_GATE_REPAIR_20261029 -->
**2026-10-29 接管后审美评价逻辑纠偏｜当前唯一可推进项仍为《简兮摄影》真实匿名评价，不能回滚旧造字实验。** 研究已发现“用户偏好与客户历史选择一致”不等于“AI审美能力提高”；必须将真人识字、真人审美偏好、未见结果的新AI盲评、客户历史选择及跨字迁移分开统计。现有助理已曝露作者选择，不可伪装新的盲测；实际真人票仍0，13项资格11项已记载、2项待独立核查；`VALIDATED_RULE=false`。之前封存匿名图和承诺保持原封不动、不得提前揭盲，继续持有正式视觉任务锁Rev355/Checkpoint377、S7人审待决、不改Figma和商业成品。不要因用户单说“下一步”自动做R30/重调旧字。完整事前评审字段、何种结果可/不可推断：[本轮审美评价推理修正规则](research/fair_pair_screening/JIANXI_REVIEW_INFERENCE_REPAIR_AND_CONTINUATION_20261029.md)。
<!-- END_JIANXI_VALID_EVALUATION_GATE_REPAIR_20261029 -->

<!-- JIANXI_FIRST_FAIRER_CJK_PAIR_PENDING_USER_READ_20261029 -->
**2026-10-29｜源于真实作者刘兵克《简兮摄影》两份完整字标提案，已实现同字、同灰背景、同墨迹高度的无标签人类评价候选。** 研究上游曾5组0合格；此次新发现2017年[第一方站酷项目](https://www.zcool.com.cn/work/ZMjE1MTY0NDA%3D.html)，作者原文确认两个真正的完整提案并有客户选稿与后续小幅修订。已使用本机Opera Neon读取900×500的两张原始方案位图并计算SHA256 `9ffa3307d07d332c366582f45ef4e6bd5c1a9c5102d710c6ea091f13a4618c06`、`88bf79a9d08a703922a17610885beb7a76a8681bc8bafd5ea8b7da895e7d19c9`；在本聊天生成`简兮摄影_方案甲乙_同墨高匿名对照.png`（1550×650、SHA256 `a6f40aa89c181050cc7f6b2203f9883c2b9026bc7e85e1b1a99621ff3031abba`），两图各抽中文主体、清除英文与灰底、保持字形比例、二值化显示（不是原源像素）、统一墨高140px，并附64px。**待用户盲于作者选项地确认中文写法及审美偏好**，不提前揭示客户选择。匿名顺序不可变SHA256承诺 `8b3527a64915d7d0682124edad378c584208e728d1b52c17528762045e34f095`，实际13项资格门已有11项核验，余2项为用户完整字形认读与参与者是否已见结果；不能把条件合格说成正式审美测试通过。ChatGPT作者对原站选择说明已暴露、不能充当独立盲审；未来应先保存用户逐字反馈原文，再揭晓客户结果与保留“用户和作者口味不一致”的真实分歧。没有新字形、Figma写入或付费调用，不进入`VALIDATED_RULE`。正式锁355／377与S7正式人工门不受影响。
- [新样本实际已载入及来源哈希与13项门槛](research/fair_pair_screening/JIANXI_TWO_AUTHENTIC_FINALIST_PAIRS_PREUSER_20261029.json)
- [图片处理边界、匿名承诺与下一动作](research/fair_pair_screening/README_简兮摄影首组真实字标待匿名人审_20261029.md)
- [上一轮5组不可公平评的负证据](research/fair_pair_screening/ACTUAL_SOURCE_SCREENED_CASES_AND_ZERO_ELIGIBLE_VERDICT_20261028.json)
<!-- END_JIANXI_FIRST_FAIRER_CJK_PAIR_PENDING_USER_READ_20261029 -->

<!-- FAIR_PAIRED_CREATOR_CHOICE_SCREENING_ZERO_ELIGIBLE_20261028 -->
**最新真正设计师审美选择能力入库审查（2026-10-28）｜在一个不公平的“尚院”原稿/改稿命中后，不再凑样本。** 本轮真实核查4组新专业资料：58UXD“微笑体”40稿选一（原页40候选图部分平台占位，镜像仅部分图片，缺完整精确同字两稿）；天蚕“动物室友”多轮客户选稿（原创图含中文、英文及聊天截图，最后选稿原位图出现其他图像替换，无法确认精确同稿二选一）；甘薇云《左體》獨／立四轮黑白同字同格逐笔修订（原作者Behance 1200×849图片已在连接浏览器真实显示，视觉训练价值高，但带时间箭头、不是两套独立完成候选，且模型已看时间顺序，**不能盲测**）；朵璞《造动剧场》初稿两种方向（有作者拒绝理由，但原图当前不可全面复核、两个初稿均非最终已确认成品）。加上上轮“尚院”混杂案例，共**5组入库筛查，完整合格0组**。事前冻结13条硬条件（同内容/繁简/完整/字形真人辨读/同墨高/同色/同完成度/无阶段标签/同客户brief/源图可信/作者精确二选一/评委不知答案/尊重原作权益），TRUE才可入库，FALSE或UNKNOWN闭锁。实际执行7项正反测试及5组真例的审核回放，7/7+5/5 PASS（仅审“是否应当拒绝”的工程规则）。**0合格≠AI审美0%准确率；这轮没有任何可评分的新盲测，`VALIDATED_RULE=false`。** 《左體》真实作者的改稿图值得作为设计修正案例学而不能计入盲测：单字角度、留白、中宫、黑度及断连要有条件地选，而非反复比例缩放。没有新原创字、无Figma写入、无新增外部付费，正式主线Rev355/Checkpoint377及S7人审PENDING不受影响。未来先获得**真二选一同条件成熟中文原字稿，且评审者完全没见过作者结果**后才可有意义地测试判断力；不自动新开R30系列。
- [真实来源与技术/审美边界报告](research/fair_pair_screening/README_实际设计师样本筛查与不可冒称盲测_20261028.md)
- [冻结13项样本资格标准](research/fair_pair_screening/SCREENING_GATE_FROZEN_20261028.json)
- [四组新来源及历史校准逐项审核回执](research/fair_pair_screening/ACTUAL_SOURCE_SCREENED_CASES_AND_ZERO_ELIGIBLE_VERDICT_20261028.json)
- [7个正反测试与5项来源的实际结果](research/fair_pair_screening/ACTUAL_GATE_REPLAY_7_PLUS_5_20261028.json)
<!-- END_FAIR_PAIRED_CREATOR_CHOICE_SCREENING_ZERO_ELIGIBLE_20261028 -->

<!-- REAL_DESIGNER_REVEAL_CALIBRATION_NOT_SKILL_20261028 -->
**最新“先判断、后揭晓”的真实设计师选稿校准（2026-10-28）｜一个案例命中，强混杂、非审美算法成功。** 继R1–R29、喜字H1和“金尊”20条正确来源但审美失败之后，本轮没有生产新字、没有AI生图或Figma改动。冻结目标：由原作者刘柏坤《那些年，在字体设计上犯的错！》中同词`尚院`最终“投稿原稿/修改后”的真实两幅600×400配对，先设识字、字重、负空间、品牌语法、应用场景的0–4评分标准，每臂只看一次。已连接Opera Neon专用网页进行随机A/B和SHA256映射承诺 `c047b41ad8a421e946792173d92fb1160f0e20bfdb6e384b0376bbe702a7898e`，不返回映射；**先向GitHub固定审美判断A16/20、B11/20、预测A为作者较好选择，提交`0aca775d39372ab2f98dea7a9520e31beea03036`，再揭晓随机映射A=作者修改后的黑白稿（源图DOM23），B=最初投稿的橙色稿（DOM22），Hash回读不变。** 成功之处是判断、封存和揭晓顺序真实执行，且预测与作者取舍一致。**重要反面**：前稿橙字+红编辑提示、后稿已完善黑白品牌版式，颜色/版式/完成度严重泄露阶段，不能算严格盲测、不能将1/1称可泛化设计准确率、更不能宣称已经学会设计中文字。两份图原网址保留，在此研究仓库只保存作者来源和评分元数据，不重发原版权图。未来真正有说服力的测试须同字同配色同体量两个均可识读的成熟造型方案，至少3例独立新来源且作者选稿揭晓前冻结判断；否则立即停，不开启无意义新字。
- [实验设计事前冻结](research/design_choice_calibration/MASKED_SOURCE_PAIR_FROZEN_BEFORE_SCORING.json)
- [揭晓前真实评分、逐项理由和提交](research/design_choice_calibration/SOURCE_PAIR_PRE_REVEAL_RANKING_20261028.json)
- [作者修订/原稿映射、匹配及硬限制](research/design_choice_calibration/SOURCE_PAIR_REVEAL_AND_LIMITED_VERDICT_20261028.json)
- [完整研究说明与下一门](research/design_choice_calibration/README_先选再揭晓_真实作者改稿单例测试_20261028.md)
原正式视觉权威分支`visual-program-distillation-v2-photography-design-20260814`、锁Rev355/Checkpoint377与S7人审PENDING不变。无外部新增付费。
<!-- END_REAL_DESIGNER_REVEAL_CALIBRATION_NOT_SKILL_20261028 -->

<!-- CREATOR_CHOICE_SOURCE_LABEL_CALIBRATION_20261028 -->
**文字创作能力主线新进展（2026-10-28）：暂停换字体/中线描边/小幅形变，开始训练“原作者为什么选择与否决”。** 上轮《金尊》20条笔画来源正确、SVG技术可重放但审美FAIL；此轮无新字稿、无图像生成、无Figma写入，转向真实设计师取舍。实际核实6个原作者项目来源（4组作者/团队），包含WB CHEN《明月里》从书法结构参考择取少量特征笔端并重新标准化、施博瀚《風箏祭》刻意对称前后图、梁志坚《放肆喜欢》喜字备选、黄科《黑神话》多人多稿筛选流程。**尤其新确认作者明确说出自己的否决原因：**梁志坚《来日方长》原方案强行使“长”右下与“方”左下笔角严格对称，反令“长”失去稳定感，故重新调整；另案“日”不可为填满版式而拉宽到像“曰”，用原有中横解决留白。再读梁2021《谈天说字》逐字自评：贤复杂又部改简、民捺收势重绘、聘左右部宽度回调、你右钩加粗、纳纟转折柔化、全字高度调整、招字组内宽度复审共7项有作者理由的修订；对“助”的不明确后续明确ABSTAIN。来源图不抄袭、不发原作图；部分网页仅有文字和缩略预览，非全图原字节校验。**资料增加了有原作者解释的否决机制，但不是7个独立审美评分或已经学会优选算法**。2个项目含明确反面理由、项目真实独立盲评数量仍0；R1-R29错误、H1乙字形用户否决、金尊B审美FAIL继续保留。新规则：中文字形/认字正确优先、局部字形的稳定性优先于跨字精确一致、少量特征来自原生笔画、要会拒绝过度设计、只在可信候选上进入Figma；无真实人审和不同结构新词验证不能`VALIDATED_RULE=true`。
- [本轮作者选择与失败样本注册表](research/design_choice_calibration/CREATOR_CHOICE_EVIDENCE_AND_VETO_REGISTRY_20261028.json)
- [真实来源、明确反例与执行边界](research/design_choice_calibration/README_真实设计师取舍与我们缺少的评价证据_20261028.md)
- [九项来源和否决门回读、三项历史失败回放（非预测准确率）](research/design_choice_calibration/EVIDENCE_READBACK_AND_RETROSPECTIVE_VETO_20261028.json)
新收费服务0，正式项目`visual-program-distillation-v2-photography-design-20260814`锁Rev355/Checkpoint377、S7真人审美PENDING完全未动。下一阶段先找到可证实的作者否决样本并让新设计候选经过两个有效方案的识字和审美选择，不自动开启R30新字轮次。
<!-- END_CREATOR_CHOICE_SOURCE_LABEL_CALIBRATION_20261028 -->

<!-- ORTHOGRAPHY_SAFE_JINZUN_ONE_SHOT_HOLD_20261028 -->
**规范字形正确性后的唯一新字组单项测试（2026-10-28）｜“金尊”二字，不是正式商业字标，创意FAIL。** 直接继承前轮用户对“喜”乙版写法的否决及喜12画SVG笔画不等于规范笔画的审计，冻结新测试词金8画/尊12画（教育部字典）与`chanind/hanzi-writer-data@68d10a4...`技术中线来源。真实生成A均衡笔幅/B有条件笔幅及两处原笔画尾势的1880×800透明PNG和20条逐笔ID可编辑SVG；A/B语义路径均只为8+12**无任何额外第21条笔画**。第一次左右轮廓算法各造成8个自交多边形，已保存失败算法与清单，后仅修复为笔触圆盘并集、各20条闭合有效源路径；独立SVG→PNG重算字节一致，6份核心文件在新解压目录实际复现全哈希PASS。**审美负面裁决**：B与A的意图区别不显著，字形整体比标准Noto字体参照更弱，96/64像素下可读性仍待真正中文人复核；“来源笔画数对”不足以认证最终写法/创造高级设计，因此不做Figma、不升级设计Skill、不继续对此A/B微调。自包含18件ZIP `金尊_规范20画与原创设计失败的真实验证包.zip` SHA256 `da2acc23cab830908c97dc90edd0f0c22dacced43c8da1ed3424c6da16774e2b`，原PNG/SVG与代码/许可证放在本聊天附件，仓库留血统回执。后续硬约束：准确字形结构和笔画来源 → 真人完整字认读 → 与字库同大小的强原创设计对照 → Figma。**停止使用字库中线自动描边当作字体创造**，不得依据20笔或像素数据宣传审美成功。正式主线Revision355／Checkpoint377与S7人工PENDING独立不动。
- [冻结目标和否决门槛](research/orthography_safe_wordmark/BRIEF_AND_GATE_FROZEN_BEFORE_ART.json)
- [真实矢量与PNG哈希、非法轮廓修复及质量否决](research/orthography_safe_wordmark/ACTUAL_JINZUN_20_STROKE_QA_AND_CREATIVE_REJECTION.json)
- [实作说明及后续唯一动作](research/orthography_safe_wordmark/README.md)
<!-- END_ORTHOGRAPHY_SAFE_JINZUN_ONE_SHOT_HOLD_20261028 -->

<!-- XI_OFFICIAL_12_STROKE_ERRATUM_AFTER_HUMAN_REVIEW_20261028 -->
**最新“喜”字规范笔画核验及先前断言纠错（2026-10-28）**：官方CNS11643与教育部标准笔顺均确认`喜`为12笔，顺序`横竖横竖横折横点撇横竖横折横`。H1甲（用户保留的旧R15 C1）有14条艺术SVG轮廓，中间把规范的7点/8撇/9横视觉联合为2条路径；乙（用户判字形不正确而否决）15条艺术SVG轮廓，其中3条中部路径恰对应规范的7点/8撇/9横。因此**“乙新增了错误规范笔画”没有得到依据，不能从15>14推断乱加笔**；用户认字反馈仍有效，乙必须停用，但不是已证实的字典笔数错误。甲也不是规范楷书笔顺示范，仅为用户喜欢的艺术字参考。已经真实执行并独立解包重跑SVG路径与PNG核验，未知额外路径、缺必要口底横可自动拒绝；这种静态映射不能替代字形正确性真人审稿。将往后所有设计硬闸门修正为：**规范来源→语义笔画映射→完整字形真人辨读→审美比较→Figma**；不重复问甲乙，也不将此单字结果推广成成熟Skill。保留R1–R29总复盘及H1原始用户选票、先前错误判断和修订血统，不更改正式业务锁Rev355/Checkpoint377、S7人审PENDING。
- [官方12画与甲乙一一语义登记、来源及程序实测回执](research/typography_h1_xi/H1_OFFICIAL_12_STROKES_AND_ART_VECTOR_CORRECTION_20261028.json)
- [实际SVG语义门槛程序](research/typography_h1_xi/HANZI_SEMANTIC_GATE_V1.py)
- [修订后的汉字正确性规则](research/typography_h1_xi/HANZI_GLYPH_CORRECTNESS_HARD_GATE_20261028.json)
- [专项研究入口](research/typography_h1_xi/README.md)
<!-- END_XI_OFFICIAL_12_STROKE_ERRATUM_AFTER_HUMAN_REVIEW_20261028 -->

<!-- XI_H1_USER_GLYPH_INVALID_20261028 -->
**最新用户审稿已收到（喜H1，2026-10-28）**：用户原话「1   。2   把文字都改的不对了。中国文字不能乱加笔画。」原始选票先写入GitHub，再解封预登记方法映射：**甲=旧R15 C1合势喜，用户选择保留；乙=本轮新拆开的中部丷+一方案，用户明确判字写错、不合格。** 本轮不是甲审美规则胜利，因为乙**违反汉字字形正确性闸门**、不能充当有效基线；结论`ARM2_USER_GLYPH_INVALID / AESTHETIC_H1_CAUSATION_INCONCLUSIVE / VALIDATED_RULE=false`。此前条目中的“真人待选PENDING”是历史阶段记录，**不得再向用户重复询问甲/乙**。未来任何造型修改首先确认汉字笔画与部件正确、不凭空加独立笔画、不丢部首、不破坏认字；SVG路径数和像素变化不等于规范笔画数或审美。没有字形合法的两个候选，先停止审美或Figma制作。未修改正式视觉生产Rev355/Checkpoint377/S7人审。
- [用户评价原话先行封存](research/typography_h1_xi/H1_USER_CHOICE_RAW_BEFORE_UNMASK_20261028.json)
- [结构/像素证据与审稿后的正式结论](research/typography_h1_xi/H1_ACTUAL_CONTOUR_PIXEL_AND_PENDING_HUMAN_VERDICT.json)
- [中文字形正确性硬闸门](research/typography_h1_xi/HANZI_GLYPH_CORRECTNESS_HARD_GATE_20261028.json)
- [更新后的研究入口](research/typography_h1_xi/README.md)
<!-- END_XI_H1_USER_GLYPH_INVALID_20261028 -->

<!-- XI_H1_MIDDLE_GESTURE_REAL_CONTROLLED_COMPARISON_20261028 -->
**R1—R29总复盘后的唯一执行实验：喜字H1中部丷＋一合势对照（2026-10-28）。** 用户此前说「讲真的，这个喜开始有点设计感了」仅绑定R15 C1「熹」上半部「喜」，不是对整字、对本次对照或任何其他字的认可。本轮**没有开R30**；以原R15 SVG SHA256 `edf5ffa0142849df33af0972f9c6bddf7777cb4191844848e78e3c7776a7efcc`（上半14原笔画）为冻结母版，仅对中部两条合势路径做一份一次性三独立笔画的反事实方案，另外12条原生路径的 `d` 字符串完全不动。CairoSVG真实渲染两张1100×920透明PNG，原稿合势上半与R15 PNG逐RGBA差0，分离中部3连通墨形 vs合势1，合势墨量27858、分离27331像素（差约1.9%），全图差异23122像素，严格集中在x209..875、y545..673外0变化。两版面板只标甲/乙（不是严格陌生人盲测），另做128/96/64认字图。所有真实原SVG/PNG、原母版、可运行脚本、技术账本以12件ZIP `金尊_喜字H1_分离与合势_受控实验血统包.zip` 随当前聊天交付，SHA256 `5125777960b671e8f1043f5743fbbe1d504b4f577e3c10844af3e94140660feb`，全新解压目录复跑11/11文件原字节相同。GitHub保存两组来源几何等价SVG及手段前冻结方案。**人类认字和审美结果未获得、连接因果不成立、通用设计规则`VALIDATED_RULE=false`。** 下一步仅采集甲乙偏好和认字反馈，然后揭晓结构方案；若无明显效果立即停止H1，不再反复凭空造微调版。正式锁Revision355／Checkpoint377和S7人工PENDING不动，R1—R29总复盘继续有效。
- [喜H1冻结路径和事前拒绝条件](research/typography_h1_xi/R30_NOT_CREATED_H1_FROZEN_PROTOCOL.json)
- [喜H1真实二版来源、像素差异及未通过人工审稿的审计](research/typography_h1_xi/H1_ACTUAL_CONTOUR_PIXEL_AND_PENDING_HUMAN_VERDICT.json)
- [喜H1本轮README和后续唯一动作](research/typography_h1_xi/README.md)
<!-- END_XI_H1_MIDDLE_GESTURE_REAL_CONTROLLED_COMPARISON_20261028 -->

<!-- XI_LOCAL_POSITIVE_MECHANISM_AUDIT_20261028 -->
**R1–R29专项审计｜停止生成新字、精确核查用户曾认可的“喜”的结构（2026-10-28）。** 该反馈仅属于R15 C1“熹”上方的“喜”，不是完整“熹”、R16 D2或商业专业设计的审美通过。实际从R15源SVG/PNG和R16 D2原PNG重新计算：原18条路径，上方喜14条，灬4条；R15/R16上方 y=0..909 像素差0；士上横两个独立矢量路径间距27px；中部合势2条路径可见宽度是上口的1.451倍；**两个口底横仍在**，与梁志坚《放肆喜欢》原作“删两口底横、简化7横”不同。原作者文 https://www.uisdc.com/11-font-design-case 。本轮只做已有源文件的彩色结构标注和小尺寸对照，保留用户局部好评，同时明确“为什么好看”的因果与独立人审**未证实**，绝不宣称已掌握设计师方法。已在本轮对话生成自包含9文件ZIP《金尊_喜字有效线索与设计师方法差异审计.zip》，SHA256 `f7d9c864c3ff995f7276523f261a29edcb6d7a437e26d28afb7d2d6944e0fa3a`，包含原件、核验程序、原图结构图与缩略图；不重新生成设计、不写Figma、不创建R30新字稿。今后若继续，必须**只测试中部原结构“丷+一”分离 vs 合势**在相同原稿与小尺寸下是否有真实偏好，先认字后评分，不可再随机增新字或重复微调笔画。S7生产原生锁Rev355/Checkpoint377未变。
- [喜字局部好评与设计师实际方法差异](research/typography_project_audit/喜字_局部有效线索与原作者方法差异_20261028.md)
- [原始路径 SHA 和几何核对](research/typography_project_audit/喜字_原始像素与结构审计_20261028.json)
<!-- END_XI_LOCAL_POSITIVE_MECHANISM_AUDIT_20261028 -->

<!-- R1_R29_PROJECT_RETROSPECTIVE_CURRENT_20261028 -->
**R1—R29整体审计已完成，先读结论再决定是否开新实验**：[真实成果、失败归因及停止条件](research/typography_project_audit/R1_R29_阶段总结与失败复盘_20261028.md)。截至当前工程/来源/原生矢量均有真实进展；**设计师式原创字标审美优势、可复用陌生字迁移、独立真人盲评均未形成完整证据**。不得仅因用户输入“下一步”自动开启R30新排版、调线宽或描字循环。优先有来源的宏观决策 + 真正不同字的视觉质量检验，过关才入Figma；S7正式人工门仍独立PENDING，锁Revision355/Checkpoint377不得动。
<!-- END_R1_R29_PROJECT_RETROSPECTIVE_CURRENT_20261028 -->

<!-- R29_COMPOSITION_PRESTYLE_VETO_20261028 -->
**最新独立研究R29｜S2构图实际执行，但因不是原创字形而停止晋升。** 接续真实已完成R28字组「巷口有风」和原作者梁志坚《海棠未雨》阶段图，先冻结三种合法字体结构参照的宏观构图（A单行等字、B“巷口／有风”分组+R28固定光学比例、C二行两列），再用本机Noto Serif CJK SC渲染三张真实图、总览及小尺寸测试。视觉结论：A标准、B仅调整词距字号、C可适用于方形招牌但并非原创字体设计，没有独立人类评价；**所有字形均是字库字，不含一条新原创汉字轮廓，Figma写入0、ChatGPT生图0、`VALIDATED_RULE=false`。** 不得将“排版不同”说成设计师方法成功。自包含8件真实附件ZIP `R29_巷口有风_三种构图与未通过设计闸门.zip` SHA256 `8d739ef497977a8c0c6ba1db5051659adeb7068bc7cf0df1cff4916d1cba5e97`，原件仅本会话容器；公共GitHub保留数据、错误、路径与哈希。后续重点不再是无限重复新字组排版/共笔/描图，而是**先证实来自真实设计师初稿—定稿之间确凿的整字结构审美变化并在人类不知技法条件下验收**，否则停止。正式主线Rev355/Checkpoint377、S7真人PENDING不动。
- [R29冻结方案](research/typography_r29/R29_FROZEN_S2_COMPOSITION_OPTIONS.json)
- [R29实作证明和否决结果](research/typography_r29/R29_ACTUAL_COMPOSITION_AND_PRESTYLE_VETO.json)
- [R29本轮完成入口](research/typography_r29/README.md)
<!-- END_R29_COMPOSITION_PRESTYLE_VETO_20261028 -->

<!-- R28_FIRSTHAND_STAGE_BEFORE_STYLE_20261028 -->
**R28 当前独立中文字标创作研究（2026-10-28）｜作者真实阶段图重新目视审读，首次形式化“先整组结构、再有条件创意”的强制门。** 继R25真实Figma原生笔画与R26跨字共笔、R27自写26条原创轮廓均审美失败，R28在已连接Opera Neon中真实打开梁志坚2019年一手《11款字体设计全过程》，逐张见到《海棠未雨》雏形图15→初稿图16→字组校正图17→选定笔画融入屋檐图18，并目视检视《放肆喜欢》的六种喜字候选图37与5否决1入选图38；所有图片仅存原作者链接/尺寸/可确认观察，不把原图复制到仓库/ZIP，也不能谎称本轮重算版权图原字节SHA。核心纠正：原设计师本来就使用字库作**结构校对**，不是强迫每笔零字体从头画；必须先解决棠太宽、未太小、雨太高之类整组光学问题，之后才选择原生笔画引入特色，并在相邻字错开特征位置。字体当参考≠把字体当成原创，SVG原生可编辑≠作品已经高级。

R28出图前冻结全新测试词`巷口有风`，实际用同字库Noto Serif CJK SC做结构参考与同字号墨量审计：巷1.209、口0.722、有0.935、风1.065（相对四字黑墨量中位数；**不能直接作为美感公式**）。另只做一次等字库字号A／预设比例B参考版，B增加口的视觉存在感但仍没有原创字形，**无R28风格化艺术字，无新Figma写入**。可执行`R28_STAGE_GATE.py`使用7组含失败/缺证据对照真实自测PASS：R27先前字重不平衡在S2拒绝，R28新词S2待独立视觉审查；这个程序是防漏步骤检查，不是AI高级审美技能。15件源文件自包含ZIP在本聊天，SHA256=`cf5a4e368c4734cd7164d482153f812c6bd4c73056ba6b355fa1d695033d494f`，全新目录复跑14个来源SHA及7项测试PASS，字库原件未包含。**不得将其报告为方法蒸馏或原创设计通过，`VALIDATED_RULE=false`。** 下一步应在结构参考层给出真正有明确理由的整组版式与白口改写方案，先视觉审稿；可见整体创作价值通过之后，才设计有条件特征笔势和Figma矢量交付；禁止R25–R27那种先画后补意义、只比笔画数的循环。主线只有正式业务锁Revision355/Checkpoint377、S7人工PENDING，本独立研究没有覆盖它。
- [R28冻结作者阶段和逻辑](research/typography_r28/R28_FROZEN_FIRSTHAND_STAGES_AND_GATES.json)
- [R28一手阶段图原件定位与真实输出账本](research/typography_r28/R28_REAL_SOURCE_STAGE_REVIEW_AND_PRESTYLE_GATE.json)
- [R28当前方法总结、源链接和下一动作](research/typography_r28/README.md)
<!-- END_R28_FIRSTHAND_STAGE_BEFORE_STYLE_20261028 -->

<!-- R27_FIRSTHAND_CREATOR_MOTIF_PRE_FIGMA_REJECT_20261028 -->
**最新独立字体设计研究R27（2026-10-28）｜先看原创质量再进Figma，首次实际执行此止损门并拒绝本轮。** 上游R26“云间”证实跨字强行共笔虽能写入原生VECTOR仍会破坏识别，C版回退又只像普通字体。R27从设计师梁志坚2019年一手《海棠未雨》创作说明重查**非工具层决策**：先确定古典唯美气质，比较海浪/古建筑屋檐两种母题，选择抽象屋檐，按每个汉字的原生结构选择合适笔画并在相邻字符错开特征高度，同时统一视觉重量；不可把这一创作描述当作作者的可执行算法。来源：https://www.uisdc.com/11-font-design-case 。已在出图前冻结全新字组「亭下听风」（密亭/疏下/左右听/包围风），A为本地Noto Serif CJK SC字库仅作识字基线，B由本地源码直接手动编写**26条由AI助手在Python中逐条编写的贝塞尔轮廓，并非真人设计师手绘**（亭10、下3、听8、风5），无字体描边轮廓、无ChatGPT Image、无第三方设计师路径复用，屋檐仅分配给亭/风的合适结构笔。第一次SVG在风/内捺有缺失C控制点，产生巨大黑三角，保存未改原件并只修复语法；之后所有26条路径语法与边界独立核验通过。A/B原图与96、64像素、**统一墨迹高度230px对照**真实制作，公开明示原A墨高232、B墨高486（原始大图不能公平比较）。**视觉质量判定FAIL并不写Figma**：字体字组墨量/宽度不均衡，B的风字明显过大、亭较小、听左右分裂，屋檐语法未形成专业整体身份；源路径有效也不能计成功。B风字墨迹约46150px而下仅18944px，差2.44倍；这些是诊断数据而非作者的机械阈值。透明SVG、PNG、首次失败原件、源码、逐路径QA、等墨高与96/64对照共15件保存在本聊天ZIP《R27_亭下听风_原生笔画预审失败与完整血统包.zip》，SHA256=`6ccd027384c7c2eabdc7cbb819bb0158b8f9b2541f22ac9fb30c86dd61f550c7`，已在全新目录重放并核验4个结果文件逐字节相同；研究GitHub只登记定位与哈希，不另复制第三方图片/字库。**下一步禁止重复调本轮26条路径或把失败B导入Figma**，改为先对真实设计师“初稿—调整—定稿”的整组轮廓作完整比较，让可见审美决定是否启动新的原创设计，而不是用软件节点与文字技巧计数。无新增外部付费，正式视觉锁Revision355／Checkpoint377、S7人工PENDING未改。
- [R27出图前冻结方法与拒绝条件](research/typography_r27/R27_FROZEN_FIRSTHAND_STAGE_TO_MOTIF_PROTOCOL.json)
- [R27实际新图、客观审计与审美FAIL](research/typography_r27/R27_ACTUAL_SOURCE_SVG_AND_PRE_FIGMA_REJECT_LEDGER.json)
- [R27完整报告与ZIP文件名](research/typography_r27/README.md)
<!-- END_R27_FIRSTHAND_CREATOR_MOTIF_PRE_FIGMA_REJECT_20261028 -->

<!-- TYPO_R26_WHOLE_WORD_FIGMA_RECOMPOSITION_HOLD_20261028 -->
**文字设计研究R26（2026-10-28，当前独立研究分支最高恢复入口）｜真实Figma整组字形结构重组后审美未过、保留拒绝规则。** 继R25「山月」9条Figma原生VECTOR只是技术试验，R26实际研读作者张家佳《上座》原始分阶段案例 https://www.behance.net/gallery/196038613/_ ，确认作者从疏密失衡出发改变双字整体布局，再重新绘制笔势（此研究只借用机制，不复制作者原图/曲线）。已在出图前冻结新词「云间」和两条路线：A两字12个原创自编贝塞尔路径独立，B将云第一横与间门顶/右钩合为一条新的跨字结构，共11个路径；均已实际写入独立Figma研究文件 https://www.figma.com/design/RpcWXDRNyN3y4KEmCspgfZ A节点`7:2`、B节点`7:17`。第一版SVG因为“间/日右竖”缺一组贝塞尔控制点造成大片黑三角，错误留在GitHub旧提交，Figma坏画框`5:3`和`5:18`隐藏保留；正确路径源已经修复并入Figma。经1400和240像素真实视觉审阅，**B虽然实际更改拓扑，但损失云/间之间的汉字识别边界，因此拒绝**。根据预冻结的一次回退C（Figma节点`9:2`），只将云首横朝间延伸但不连接，A/C剩余11条原生路径完全一致；C视觉仍接近普通字体，云横与间左竖间只剩约11个原图像素，缩略后安全性尚未证明。真实回读A/B/C分别12/11/12原生VECTOR，**TEXT=0、IMAGE=0**，三份Figma当前实际节点的路径源码均已存档，未使用系统字库或AI生成PNG描摹，但原轮廓是自编SVG导入而非鼠标从零绘制。无用户审美或独立识字测试，`VALIDATED_RULE=false`，**停止对该“云间”笔画继续微调**，不以技术节点数包装成熟设计能力。S7和正式锁Rev355/Checkpoint377无变更。R1—R25研究结果与失败不覆盖。
- [R26正式冻结目标、来源及失败条件](research/typography_r26/R26_FROZEN_AUTHOR_DECISION_BEFORE_ARTWORK.json)
- [R26一次结构否决与回退冻结](research/typography_r26/R26_C_STRUCTURAL_ROLLBACK_FROZEN_BEFORE_RENDER.json)
- [R26三版真实Figma来源、语法错误和负面审核台账](research/typography_r26/R26_ACTUAL_NATIVE_FIGMA_TOPOLOGY_AND_NEGATIVE_VERDICT.json)
- [R26本轮恢复README及下一关](research/typography_r26/README.md)
下一步必须从真实设计师阶段图导出**宏观设计决策**及其失败回退条件并检验陌生字组整组外轮廓，不重启字体线宽/横向拉伸小修循环；先可见质量、后Figma。付费新增0。
<!-- END_TYPO_R26_WHOLE_WORD_FIGMA_RECOMPOSITION_HOLD_20261028 -->

<!-- R25_TRUE_EDITABLE_FIGMA_STROKES_NONPROMOTED_20261028 -->
**R25 最新独立中文字标方法研究（2026-10-28）：第一次对比R24明确纠正“AI生图PNG≈设计”。** 用户指出R24字标看起来只是套现成字体且缺乏设计感，这一点成立。R25没有再生成艺术字PNG，而是创建独立真实Figma Design：https://www.figma.com/design/RpcWXDRNyN3y4KEmCspgfZ。选两个不同结构的新字「山月」作为**极小手工设计测试**，先由人工在本地Python/SVG中独立编写9条原创贝塞尔字形轮廓（无系统字体轮廓、无作者源图描摹），再实写入Figma的9个可分别编辑`VECTOR`节点。审查C1/C2过于几何后保留失败，C3整组重绘为正式Figma原稿（node 1:2）；在Figma中复制一份C4（node 2:2），**真实修改**「山/承重底横」「月/内横下」两条原生向量路径，独立回读确认原稿和修订稿均9条`VECTOR`、TEXT=0、IMAGE=0，另7条路径不动。Figma内真实C4的矢量文件已源代码导出并在GitHub保存，Git Blob SHA1 `72e3d9fcc4c4f9a7eda26d193b5fac3414c73c94`，本地重新渲染C3/C4差异像素8537、底部两笔所在区域。**如实声明**：初始控制点在Python/SVG中手工设计再导入，不是完全鼠标在Figma画；C4确实在Figma内编辑真实Vector；这与 R24 的图片生成及自动矢量描摹不同，但**仍不代表设计高级、用户认可、作者方法被完整逆向或有可复用自动造字能力**。视觉目前简洁偏几何，评级`HOLD_PROTOTYPE_NOT_COMMERCIAL_MASTER`，人类评审和第三词迁移均缺失。交付包含全部历史C1/C2失败、源SVG/PNG、源代码、独立回读及26件自包含 ZIP，SHA256 `2cfc655628379b03c875a1fb13ed010c5e01462d90987dae989754b531111d98`，本聊天已真实建立容器文件。下一步不要再为了微弱曲线差异反复“下一版”；必须依真实设计师有前后图的造型决策做实质不同的整组字设计，并用不带方法标签的真人审美/认读验证。
- [R25预冻结主线与质量门](research/typography_r25/R25_FROZEN_AUTHOR_CONTOUR_DECISIONS.json)
- [R25实际Figma节点/原始文件及失败血统](research/typography_r25/R25_ACTUAL_FIGMA_NATIVE_VECTOR_AND_AESTHETIC_HOLD.json)
- [R25当前README与唯一下一门](research/typography_r25/README.md)
- [R25真实Figma C3路径](research/typography_r25/R25_C3_山月_真实Figma原稿.svg) · [R25 C4真实改动后路径](research/typography_r25/R25_C4_山月_真实Figma路径导出.svg)
**范围不变**：正式视觉主线`visual-program-distillation-v2-photography-design-20260814`，唯一原生锁Revision355/Checkpoint377及S7人类PENDING不受研究修改；不新增收费服务，第三方参考仅研究不复制。
<!-- END_R25_TRUE_EDITABLE_FIGMA_STROKES_NONPROMOTED_20261028 -->

<!-- R24_REAL_HELDOUT_A_B_TECH_PASS_20261028 -->
**R24最新原生研究血统（2026-10-28，优先于下方R24 2026-10-27阻断历史）：** 使用R23提前冻结的留出文字「溪桥听雨」，并在R24任何新像素生成前，冻结无逐字定制的通用字组造型语法和A中性/B风格双臂原文。昨日Opera Neon因Session terminated阻断在真正出图之前，原失败记录完整保留。今天Opera连接真实恢复，分别在两个独立全新ChatGPT普通聊天各生成一张1672×941黑字单行透明RGBA PNG，无任何重抽、后验提示词或新收费服务。A源：https://chatgpt.com/c/6ae16913-8ad4-83ec-a02f-5788676bc82b，SHA256=`47501dca6c08c5d238767b5dff6a656c20b4a1d5672d2a661d566c15e5dce5e7`；B源：https://chatgpt.com/c/6ae16946-8190-83ec-904c-55d906103ade，SHA256=`7707046868231f24e2336daaf85831401c57b104f6d52cfd66797137572a1ba4`。用户ChatGPT文件库原文件已实际回收，和浏览器真实图片Blob字节哈希一致。原冻结R24_QUALITY_GATE对两张图机器像素门PASS；实际目视「溪桥听雨」四简体字和版面合规；独立陌生真人识别与偏好未采集，`VALIDATED_RULE=false`。B墨高388、A291，B天然更大，必须优先读等墨高的可见对照，B的「溪/桥」拥挤、动势较强，不能凭“更显眼”宣称更专业。两次字标差异只能算**固定通用语言提示词在另一四字目标上呈现风格变化**，不是艺术字体作者创作方法的已证明自动程序。单次有效A/B不提供稳定胜率，不改正式视觉生产任务锁Rev355/Checkpoint377或S7真人门。
- [R24事前冻结通用规则/提示词](research/typography_r24/R24_FROZEN_GENERAL_GRAMMAR_AND_AB.json)
- [R24真实两图身份及审计2026-10-28](research/typography_r24/R24_ACTUAL_TWO_SOURCE_HELDOUT_A_B_20261028.json)
- [R24当前恢复入口与历史断连记录](research/typography_r24/README.md)
- [R24昨日仅出图前断连原记录，保留历史](research/typography_r24/R24_CARRIER_BLOCKER_AND_PREFLIGHT.json)
新zip「R24_溪桥听雨_真实A_B双源及跨字迁移审计.zip」SHA256=`cfc02f6fc423ed55afd778af80f3b079f2161df30b3be2843170a4916ceff481`，10文件，QA脚本/PNG原始字节/可见对照与复算清单在本聊天附件，公共仓库仅存哈希。新解压目录已复算两图并实际核对对照图SHA一致；人类审美待评，不做更多随机出图冒充复现。
<!-- END_R24_REAL_HELDOUT_A_B_TECH_PASS_20261028 -->

<!-- TYPO_R24_FROZEN_BUT_NO_IMAGES_20261027 -->
**最新设计方法支线R24（2026-10-27）｜冻结了“溪桥听雨”通用规则跨字迁移A/B，但尚未生成任何R24图片。** 继R23「松间见月」的独立短上下文A/B技术通过，R24按R23预留留出词“溪桥听雨”先行冻结A中性字标/B**无任何逐字特制**的6条设计条件（识字优先、密字留白、疏字主笔、包围与左右结构、组内1–2处笔势、整体光学平衡），然后调用已连接的Opera Neon `new_page`，服务器返回`McpServerError: Session terminated`；两次 `list_pages` 仍失败，备用只读Browser也因缺来源上下文不可用。**A=0次、B=0次；没有PNG、没有新字稿；不得声称跨字迁移成功或失败。** 未使用Adobe Firefly/其他收费网页自动化，没用旧聊天随机生成冒充原两臂。实际完成可执行本地PNG机器验证脚本，使用R23真实PNG做正向烟测，缺文件和合成不透明底做拒绝烟测，绝不以机器几何替代汉字/审美人工审核。自包含本聊天ZIP `R24_溪桥听雨_隔离执行与像素核验准备包.zip` SHA256 `810c456c36956e01ea59b28c6bd4573cb949e2df151b53f97e1ba47b259c0047`，7文件；公共仓库只保存哈希和恢复规则。恢复唯一动作：先恢复Opera Neon同账号连接，再由**两个真正全新普通ChatGPT聊天**分别发送冻结A/B提示词，每臂1次并取回原始PNG，出现任何错字/非透明/方案板立即判INVALID。R23人类审美仍PENDING，R24规则尚未VALIDATED。独立研究不写正式视觉锁Rev355/Checkpoint377，也不更改S7真人等待状态。
- [R24前置冻结规则与原提示词](research/typography_r24/R24_FROZEN_GENERAL_GRAMMAR_AND_AB.json)
- [R24真实浏览器阻断、测试程序与归档哈希](research/typography_r24/R24_CARRIER_BLOCKER_AND_PREFLIGHT.json)
- [R24恢复操作顺序](research/typography_r24/README.md)
<!-- END_TYPO_R24_FROZEN_BUT_NO_IMAGES_20261027 -->

<!-- TYPO_R23_TWO_VALID_PNG_AB_20261027 -->
**最新研究R23｜“松间见月”独立四字字标真实A/B技术有效，但创作规则尚未验证。** 在独立研究分支沿 R22 单张正确透明PNG入口，先冻结两臂提示词和全新目标「松间见月」（另封存未用「溪桥听雨」）；之后实际用 Opera Neon 的两个**独立全新ChatGPT普通聊天**，A中性字标/B整组结构条件设计规则各调用一次，只得一张1672×941原始透明RGBA PNG。两份原图在ChatGPT用户文件库真实取回，与浏览器生成Blob原字节 SHA256 一致，A=`2c1ce159bc5c48d427a989d05dd9a40ca6e913df5c7f3fb0736de305e7c3986a`，B=`39559dc122df75a87146a609418d192ff73936752403457d506e94ea7dc538db`。四个简体汉字准确且只有单行，无注解/风景/拼图。**技术闸门 PASS**；B视觉更有书写动势，但人类盲评未做、长期稳定/第二词适配未做、内置模型/种子未知，不能写 `VALIDATED_RULE`。A原墨迹高355px、B412px；已用第二幅**只作为展示**的同墨高355px对照避免天然体量偏差，原始PNG没有改。两条提示词A长200字/B300字且B为松/间/见/月逐字指定技法，不能把单例改观直接归因为真正学会的通用设计程序。公开仓库只存字节哈希和技术记录，原PNG和复算脚本在本聊天 ZIP。下一关R24必须先冻结**与字无关的设计语法编译方法**再测试新「溪桥听雨」，禁止事后按输出改参数或仅重复随机生图。新付费预算0。
- [R23 冻结A/B实测契约](research/typography_r23/R23_FROZEN_A_B_PROMPTS_BEFORE_OUTPUT.json)
- [R23 原始双图身份／像素审查](research/typography_r23/R23_ACTUAL_TWO_SOURCE_PNG_AND_TECHNICAL_GATE.json)
- [R23 恢复入口与严格失败条件](research/typography_r23/README.md)
正式视觉任务仍按唯一原生Revision355/Checkpoint377、S7人工审稿PENDING执行；此独立研究支线不修改正式生产锁或摄影。R1–R22全部旧失败和原始回执不得覆盖。
<!-- END_TYPO_R23_TWO_VALID_PNG_AB_20261027 -->

<!-- TYPO_R22_ISOLATED_CARRIER_PASS_20261027 -->
**最新独立文字设计方法研究R22（2026-10-27）｜生成入口单次技术通过，绝非审美蒸馏成功。** R21长上下文的「雾起长桥」两次生图均生成额外海报/方法板（原INVALID不撤回）。R22先在独立研究分支冻结单次全新ChatGPT空聊天生成契约，再通过已连接Opera Neon实际开启一个全新ChatGPT普通聊天，仅一次输入「青石晚风」四字横排、黑色、16:9透明、无附字/场景/方案板，并实际得到**一张正确的RGBA透明PNG**。生成聊天：https://chatgpt.com/c/6ae09627-6f84-83ec-964d-3523aed1b4fc 。文件已经从ChatGPT用户库读回原始字节，与浏览器生成图片Blob独立SHA一致；PNG原件1672×941、176421字节、SHA256 `c0483c2637d2a6232734426558f9d5400c383aa5de62efd04641da9b98fc6217`；alpha零像素1,380,620/1,573,352，四字符横排独立墨迹，视觉检查无额外文字背景。这是**1/1实际单次技术输出合规**，不是长期稳定，也无法从改变了新聊天、短提示词、不同文字三个变量判定失败原因。字体风格仅近似，不保证具体宋体字库；没有真正原创专业质量/独立人审，也未产生矢量路径或迁移证据。图像原件在本聊天附件ZIP，GitHub公共仓库只存身份哈希与记录。

- [R22冻结一图门槛与执行指令](research/typography_r22/R22_ISOLATED_CHAT_CARRIER_FROZEN.json)
- [R22原图身份、独立哈希与像素数据](research/typography_r22/R22_ACTUAL_EXECUTION_AND_PNG_PIXEL_AUDIT.json)
- [R22完整血统与下一关](research/typography_r22/README.md)

下一步R23须用全新冻结词和各自独立短上下文等预算A/B实测，基础文字/透明/无拼版两图均PASS才有资格进入真人审美比较；未执行前不得写成结果。R19真人评价仍PENDING；R21错误保留。正式生产权威视觉锁Revision355／Checkpoint377、S7真人PENDING保持独立，不因R22研究改变。
<!-- END_TYPO_R22_ISOLATED_CARRIER_PASS_20261027 -->

<!-- R21_WHOLE_WORD_EXPERIMENT_CURRENT_20261027 -->
**R21最新独立文字方法研究结果（2026-10-27）：首次真实生成四字《雾起长桥》A/B，均因交付契约不符判定INVALID，未通过、不能晋升。** R20 已冻结基线A为准确简体四字单行透明传统排印、规则组B为相同成品规格+整组字笔势/重心/留白造型；同一个 ChatGPT Image 工具各实际调用一次，未暗中重抽。A得到1774×887的三行方案说明板（原图SHA `7f63b6fa...`），B得到1024×1536山水多方案海报（原图SHA `611ab71b...`），都额外出现了预留词“纸舟过岸”，所以 A/B 及原留出样本均不构成有效验证。这次禁止从海报裁字充当正式输出，确切底层图像模型与种子NOT_EXPOSED。另做了以AR PL KaitiM GB授权字体轮廓为基础的C2技术补救SVG+PNG，4个可编辑原生字形、RGBA重算完全一致；**属于现成字体轮廓重排，不是自己创造四字或方法蒸馏成功**。局部尾笔失败 C1 按原字节保留。原生成失败图、C1/C2、字体许可、源码、核验数据已作为18件自包含聊天ZIP交付，公共仓库仅保存SHA和结果边界。
- [R21事前冻结协议](research/typography_r21/R21_FROZEN_A_B_EXACT_COPY_AND_METHOD.json)
- [R21真实执行和失败台账](research/typography_r21/R21_ACTUAL_EXECUTION_FAILED_AB_AND_RECOVERY.json)
- [R21恢复入口与精准下一步](research/typography_r21/README.md)
唯一有效后续方向R22：先让生成入口在隔离短上下文中稳定遵守“单资产、准确四字、透明、无附字、尺寸”契约，再以**新冻结留出词**公平比较设计规则；未验证人类审美与跨字迁移前禁止VALIDATED_RULE。R19无标签投票仍PENDING。正式主线唯一锁Revision355/Checkpoint377，S7真人审稿继续等待，生产代码/摄影不修改。
<!-- END_R21_WHOLE_WORD_EXPERIMENT_CURRENT_20261027 -->

<!-- TYPO_R20_WHOLE_WORD_METHOD_RESET_20261027 -->
**文字设计研究 R20（2026-10-27）｜核心方法纠偏，非审美通过。** 继 R19 三组去技法标签对照（人评未投，映射仍封存），当前真实读回R16–R18六个原始PNG，复核SHA与RGBA不同区域；变化集中在整字墨迹框约19.63%／9.67%／9.37%的垂直带宽。此数值**仅为改动局部性指标，不是美感提升百分比**。证明过去持续改笔画，但**从未测试过同一设计语法在多个汉字组成的整组字标中的传播、重量统一、特征呼应**。

已实际阅读梁志坚2019《实战案例！详细剖析11款字体的设计全过程》可访问的完整转载文本（https://www.hellofont.cn/article/229166；原始源 https://www.uisdc.com/11-font-design-case 本轮直连403）。创作决策原理来源于作者叙述，**不能冒认为可执行的原作者模型或原图矢量**。结论是：必须先定义整组文字的气质、主次、视觉重量和特征笔画呼应，再决定每字局部断/连/共笔是否真正有必要，不能反过来为了共笔而硬改。

本轮已经保存并回读：
- [R20 专业诊断与历史错误](research/typography_r20/R20_结论与设计方法纠偏.md)
- [R20 原始像素复算](research/typography_r20/R20_TECHNICAL_AUDIT.json)
- [R20 冻结下一轮整组字标实验](research/typography_r20/R20_NEXT_WHOLE_WORD_FROZEN_PROTOCOL.json)

唯一新的研究方向：在固定生成器、固定次数与真实原件记录下，用四字 **“雾起长桥”**做整组字标A/B受控试验，另以 **“纸舟过岸”**作冻结迁移文本；未出图，真人审美和识字仍待验证。不得从该计划宣称已获得新视觉成品，也不得回到R1–R18单字机械线宽或延续R19人审缺席时冒称PASS。R19封存左右映射保持未打开；人审票仍PENDING，不影响本独立研究逻辑纠偏。当前研究预算新增0元，生产主线仍为锁355、检查点377、S7真人PENDING，禁止写生产锁。
<!-- END_TYPO_R20_WHOLE_WORD_METHOD_RESET_20261027 -->

<!-- R19_LABEL_MASKED_REVIEW_CURRENT_20261027 -->
**最新独立文字设计研究 R19｜真实成品无方法标签评估材料已制作，等待真人选择**（2026-10-27）。本研究分支继 R18「森」后**没有再造新字**，而是从 R16「熹」/R17「照」/R18「森」各取同字两个已冻结真实像素，先于排版锁定6份原件 SHA 和左右顺序封存 SHA256，再按两边**同一画布、同一裁剪、同一尺度**生成共三组去版本/技法标签的大图与96、64像素缩略图。真实像素不同数30,865／20,482／12,235；展示文件全量 SHA 已核查，封存映射未对受评者揭晓。须先收真人“左／右／差不多／都不行”选择，再解封映射并追认评价。用户已见过部分前作，故**不是严格的陌生人盲测**；人评尚不存在，`VALIDATED_RULE=false`。不要用像素 IoU、技术验收或自评补写 HUMAN_PASS，不得宣称已经学会自动造字。当前续办入口：
- [R19 冻结协议](research/typography_r19/R19_FROZEN_LABEL_MASKED_REVIEW_PROTOCOL.json)
- [R19 原始 SHA、交付与 PENDING 回执](research/typography_r19/R19_REAL_STIMULUS_SHA_AND_PENDING_HUMAN_VERDICT.json)
- [R19 方法与下一动作](research/typography_r19/README.md)
R1–R18原始成果、失败、用户局部意见全部继承；未动正式视觉任务锁 Revision355 / Checkpoint377 / S7真人验收。新增付费软件/API调用0。
<!-- END_R19_LABEL_MASKED_REVIEW_CURRENT_20261027 -->

<!-- TYPO_R18_ISOLATED_RESEARCH_POINTER_20261027 -->
**当前 R18（2026-10-27）｜“森”的无四点底跨结构创作实验**：继 R17「照」C2 共用承重横笔后，研究分支冻结一个从未用于旧案例的新目标“森”，在真正绘制之前保存协议。实际输出 A 常规识别锚点、B 12 条人工设计原生矢量（三木下方两条独立横笔）、C 11 条人工设计原生矢量（只把两条横笔换成一条连续共笔，其他 10 条路径字节一致）。B/C 完整 RGBA 相差12,235像素，差异区域 x142..1101、y699..792；无关上方/下方区域0差异。独立脚本复算两个 SVG↔PNG 全像素一致。真实创作、技术和可编辑性**通过**；成熟美感、相对于 B 的审美净改善、96px独立认字以及人类盲评均**未通过/未收集**，**不能晋升**。原创作品是手绘，不代表模型已经自动学会设计师方法。阴性“林”按三木专属规则拒绝，但未另做画面，不得冒称验证。实验中第一次用到 y699 作为不变区曾触发24像素核验失败，已保留边界修正说明，并没有修改设计换取PASS。

当前 R18 恢复入口（本研究分支）：
- [冻结协议](research/typography_r18/R18_FROZEN_PROTOCOL_BEFORE_PIXELS.json)
- [真实像素与错误血统](research/typography_r18/R18_REAL_PIXELS_AND_LINEAGE.json)
- [方法与失败报告](research/typography_r18/R18_REPORT.md)
- [B 原生 SVG](research/typography_r18/R18_B_森_原生可编辑字稿.svg)
- [C 原生 SVG](research/typography_r18/R18_C_森_原生可编辑字稿.svg)

R12–R17 全部证据与失败保留；不要重试微调单条横笔冒称审美成功。下一步只在可读性独立验证和无方法标签的人类审美对照得到结果后，才决定是否继续该方法。新付费授权0；正式视觉锁仍由 mainline revision355/checkpoint377 控制，不动 S7 人工门。
<!-- END_TYPO_R18_ISOLATED_RESEARCH_POINTER_20261027 -->

<!-- TYPO_R17_ISOLATED_RESEARCH_POINTER_20261027 -->
**当前字体设计方法研究 R17（2026-10-27，研究分支内有效，非正式视觉主线）**：继 R14 对“熹”结构适用性预判、R15 真正制作“熹”及用户对其中“喜”的局部正面评价、R16 四点笔势 C1/D1/D2 受控修订后，R17 已按事先冻结的新目标字 **“照”** 完成 A（字库识别基线）、B（手绘结构＋均衡四点）、C（同一结构＋动势四点）三个真实 SVG/PNG；B/C 上半画布真实 RGBA 零差异，四点各为四个独立组件。实际看图发现 B/C 容易像“日”和“召”的分离组合，因此仅一次冻结 C2 修复：重画“日”和下“口”共用长主横，删除一条独立底横，底部四点真实 RGBA 零差异，修复前后变动 20,482 像素。C2 是**可编辑源字稿、整体性研究候选，不是专业审美通过**。独立真人识别与盲评缺失；R15 原失败及 R16 用户只认可“喜”的限定必须保留，绝不声称用户批准 D2/C2 或可跨字稳定推广。所有 R17 锁定和真实回执请首先读：
- [R17 冻结验收协议](research/typography_r17/R17_PROTOCOL_FROZEN_BEFORE_RENDER.json)
- [R17 唯一整体连笔修复冻结](research/typography_r17/R17_C2_SHARED_STROKE_REPAIR_FROZEN.json)
- [R17 实际字稿、失败与像素血统](research/typography_r17/R17_ACTUAL_ARTWORK_AND_FAILURE_LEDGER.json)
- [R17 原生可编辑 C2 矢量](research/typography_r17/R17_C2_照_共用主笔_原创矢量.svg)
- [R17 B/C 两个冻结原生矢量](research/typography_r17/R17_B_照_可编辑矢量字稿.svg)
研究未上传未验证的真人审稿，不覆盖原生视觉锁 Revision355／Checkpoint377，不修改 S7 人类验收状态；下一步必须用固定源数据做独立识别和审美对照，再测试第二个不同结构新字；不得恢复全局调粗细/机械排版路线。无新增付费预算。
<!-- END_TYPO_R17_ISOLATED_RESEARCH_POINTER_20261027 -->

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
R10（2026-10-27，来源补证而非字稿生成）：已从官方设计奖项、Typotheque 作者本人文章和文鼎相关作者作品链接核验4张真实来源图片，GitHub免费 Actions [#40421894959](https://github.com/vubaoha034-hash/shenmei/actions/runs/40421894959) 逐一确认SHA-256与尺寸；并实际目视核对汉仪《红云隶》参考形→手工轮廓稿→完成字形、Typotheque同一「阝」部件红/蓝改稿。两张文鼎图暂仅认证来源字节，不冒充作者草稿。全部来源图片只保留官方链接/哈希，不把版权原图上传公共仓库。可用研究结论是**先有明确原件/修改过程依据再分析整字/部件轮廓与负形**；不得从成品猜笔压或回归固定改宽比例。**生成的新艺术字=0，独立跨字审美验证=0，R10仍为SOURCE_STUDY**。完整回执：[R10_AUTHORED_STAGE_VISUAL_AUDIT_20261027.json](evidence/vpd/typography_method_distillation_20261026/R10_AUTHORED_STAGE_VISUAL_AUDIT_20261027.json)。在审美合格的新文字验证之前禁止宣称蒸馏成功。未动正式355锁/377检查点，新增收费预算0。
R11（2026-10-27）不生成新图，不按 R9 的猜测百分比继续缩放字：从 R10 **已实际校验**的汉仪、Typotheque、文鼎原作图进一步得到共5个官方/创作者图像（新增森泽文鼎高田裕美设计访谈配图），原图字节 SHA-256/像素均在 GitHub Actions **#40459767901** 重读验证，第三方版权图片不上传公开仓库。Typotheque 作者郑初阳同字红色 Before/蓝色 After 原图中，彩色像素提取的两块主轮廓横向边界分别 +3.54%、-3.79%，两块轮廓间距源图54→56像素；这是实际示意图的测量，而**不是要照抄的美学参数**，也不代表作者当年节点调整原始文件。更重要的是作者明确记录：「口」早期被加宽以追求现代感，但数千字检验后发现家族关系失衡，故全族撤回改窄；表明专业设计包含“全字家族语境审查与必要时撤销看似漂亮的局部修改”。汉仪原作还真实展示历史字体→手绘草稿→数字定稿；文鼎标准/C80是变体对照，**不得冒充时间前后**；高田访谈记录使用者指出笔画收笔方向问题后连带全族校正。此轮属于 SOURCE_STUDY + SOURCE_AUTHENTICATED_PIXEL_CHANGE，不是新字成功、不是艺术字蒸馏完成。完整回执：[R11_ACTUAL_AUTHOR_BEFORE_AFTER_AND_CONTEXTUAL_ROLLBACK_20261027.json](evidence/vpd/typography_method_distillation_20261026/R11_ACTUAL_AUTHOR_BEFORE_AFTER_AND_CONTEXTUAL_ROLLBACK_20261027.json)。下次只能从这些实际修改证据衍生条件+失败+撤销机制，不能再用 R9 那种固定组件宽比冒充创作规律，且不允许新增费用。独立研究分支：`research/typography-r11-verified-visual-ops-20261027`；正式任务锁与检查点保持不动。
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
