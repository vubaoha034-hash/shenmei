# 高级感 P｜当前进度与端到端制作流程（2026-10-11）

## 2026-10-11 17:29 核验：地图以外 A/B 双原始 PNG 已保存，待真人盲评（最新）

- 已执行两条独立新 ChatGPT 会话，各携带同一实际参考图，严格按冻结双路文本输入各生成一张原始 PNG（X、Y）。原旧图 R1–R5 没有作为新一轮输入。
- 旧 V2_STAGE1_AB_INPUTS_FROZEN.json 只是预先冻结的输入，不能再单凭它把最新状态说成『尚未出图』。本轮最新实证：evidence/vpd/dituyiwai_photo_20261011/V2_STAGE1_AB_GENERATION_AND_LIBRARY_READBACK_20261011.json。
- X：ChatGPT 资料库 libfile_f472048b87b481919c6dd35785fb26b5，原文件 2060330 字节，941×1672 RGB PNG；SHA256 b0958ce70e0e55b08642d7671e8f5fe8dc2d3c4cefc104912e202c7918609268；实际生成会话 https://chatgpt.com/c/6acb42fc-0fac-83ec-af2c-132ab60ded2e。
- Y：ChatGPT 资料库 libfile_1afa56c01ed08191be566b92b17cbbca，原文件 1934752 字节，941×1672 RGB PNG；SHA256 e24c7d286cf622613abec7c48b81010724858de6b7dd19b9ebef15b231ec9e42；实际生成会话 https://chatgpt.com/c/6acb43f1-df0c-83ec-a0d6-8d627fa4ed6d。
- 已从 ChatGPT 资料库实际 materialize 两张原始 PNG 并读取真实原始字节、尺寸和哈希；不是截图。两张目前未成功归档 Google Drive。
- 两张尺寸 941×1672 接近但不等于数学上严格 9:16；这一硬技术验收不能标 PASS。工具内部精确参考图调用元数据未暴露，不能声称确定性条件绑定或蒸馏有效。
- 目前人审绝对可用性 / 匿名偏好 / V2 相对收益 / Figma 完整海报仍全部 PENDING。让刘先生先看两张实际像素各自判断是否可用，再比较偏好，最后才解开 X/Y 对 A/B 的映射，防止盲评污染。不得为了这次评估追加盲重试。
- 本轮仅新增旁路执行回执及这份进度快照；原生任务锁仍 revision355、checkpoint377，原任务 S7 等人审，不覆盖任何历史或已完成文字。

---

## 2026-10-11 实际 A/B 浏览器预检（未正式出图）

本次依据最新HEAD `f677646cf046fd9bfb1e2101778c2611ea8858b2` 复核 V2 双路输入，确认A/B仍是未执行。已在连接的ChatGPT网页中实际检索到Google Drive原参考，并曾成功把图片上传到新聊天输入框；随后正式发送前发现共享Opera浏览器标签被其他任务导航/关闭。同时另一新聊天虽已输入A路冻结原文，却无法保证与参考图片在同一隔离请求里稳定绑定。**A未发送、B未开始、Image生成次数=0、没有新的A/B正式图片。** 已恢复操作前浏览器中存在的未发送草稿，不改变他人的正式会话。记录：[隔离执行预检与并发阻断回执](../../evidence/vpd/dituyiwai_photo_20261011/V2_STAGE1_AB_ISOLATION_BROWSER_PREFLIGHT_20261011.json)。不再把受污染的同聊天生成冒充正式比较。下一动作维持：在稳定、独立的两个新ChatGPT会话中分别携带**同一参考原图**与已冻结的A/B原文生成各一张后，保留实际像素及验收；不能满足隔离条件就不消耗预算。原生锁355/检查点377保持不变。

---

## 2026-10-11：现有 V2 蒸馏编译合同首次用于《地图以外》摄影输入冻结（**还未正式出图**）

- **实际恢复**：独立读取当时 GitHub HEAD `705120a1be99dc50736760cc6271938c0a630390` 下 `START_HERE.md`、`AGENTS.md`、`PROJECT_CONTROL_ADAPTER.json`、`VPD_PROJECT_ROADMAP.md`、`CURRENT_TASK_LOCK.json`、`LATEST_CHECKPOINT.json`、`VISUAL_DISTILLATION_COMPILER_CONTRACT_V2.md`、`VISUAL_PROGRAM_DISTILLATION_V1.md`、`AESTHETIC_SKILL_DESIGN_CHARTER.md` 和真实 R5 记录。原任务锁仍 revision=355、checkpoint=377、S7 等真人审核，**没有改变**。
- **找到根因**：实际读取 GitHub 当时完整约4795树项，V2 是 `FROZEN_FOR_IMPLEMENTATION` 的规范合同+JSON Schema+已存个别 Style Capsule；未找到可直接运行并调用 ChatGPT Images 的通用 `visual-distillation-compiler-v2` 可执行程序。现有 `visual_memory/generation_bridge.py` 自述不调用 renderer。因此“已经自动运行现有 V2 编译器”不成立。当前成果明确是**人工按照原 V2 合同，从实际像素做一次结构化编译**，不是部署新 Skill、训练模型或自动调用插件。
- **源图验证**：实际下载、读取参考A：709×1064 RGB PNG；SHA256 `fc5b2302cc829d4a864e850c6f59c53fe3be1009946da9db0a5bb000246ee016`；仅此一张作为正参考。并实读 R5 原件 941×1672，SHA256 `f2d797ebaf377518afc6a8c5e3d0b5c151116f2b2f54561c5ebf87ce05fe242d`，用失败对比确定原图不同机制（左下小路/极小车辆/大片乳白雾/浅桃远山/无太阳/低对比留白）。
- **实际产物1**：[《地图以外》摄影 V2 VisualProgram 草案](../../evidence/vpd/dituyiwai_photo_20261011/V2_PHOTO_VISUAL_PROGRAM_DRAFT.json)。包括真实来源血统、摄影B1-B8、无文字设计和图文融合说明、8条按优先级排序的高杠杆视觉机制、同一参考家族可变项与不复制边界、迁移算子和质量检查。**已加载仓库现存 `schemas/visual-program.v2.schema.json`，使用当前运行中 JSON Schema 核验逻辑校验所有 required/type/enum/const/refs/arrays/props，结果 PASS；状态只为 DRAFT，真人尚未批准**。
- **实际产物2**：[冻结 A/B 双路输入](../../evidence/vpd/dituyiwai_photo_20261011/V2_STAGE1_AB_INPUTS_FROZEN.json)。A=实际单图直参+共同内容条件；B=同单图+完全相同内容条件+冻结8个V2高杠杆机制。均限定9:16、单张无字摄影、每路n=1、不重试、不隐藏变体、禁止 Figma 写入；两路文本已落盘，防止现场微改提示词。
- **目前仅 PREPARED，不是成功实测**：这次没有任何新 Image 生成，没有证据声称 B 比 A 好。按照 2026-09-21 已存 `CHATGPT_IMAGES_NATIVE_CONTROL_MAPPING_20260921.md` 原协议，A/B 须各用**独立干净生成聊天**，只载入同一原始参考、不得载入R1-R5或对方输出，在一致条件生成后由真人盲评。当前会话已经含有旧图，不能将本聊天内连续生成视为合法正式 A/B。
- **下一唯一实验动作**：把现有已冻结 A/B 输入分别投送至两个真实独立新生成上下文，核对运行者、参考实际像素与文本身份/比例/输出，且生成后每路只归档一个原始作品。若平台不能公开完整 Image 参数/附件绑定凭证，标注观察限制，不将相似外观冒充可审计因果证明。此工作属当前《地图以外》摄影独立试验，不能擅自重写S7原生业务任务锁，也不能晋升Golden或Scale。

---

## 2026-10-11 新纠偏：Image可以直接参考已有图片，无须更换Adobe

用户正确指出：**Image 本身具备以真实图片为参考生成新图片的能力**。此前把“生成返回没有可机读参考绑定凭证”解释为“Image不能参考，需要Adobe Firefly”，属于执行者错误推论。二者须区分：参考图实际在聊天可见/上传，Image可以利用；工具是否公开独立绑定清单是另一层可观测性问题。以后**默认在 Image 内继续参考创作，不再因缺少绑定日志而强制换工具，也不把生成 metadata 的 `edit_op=null`、`parent_gen_id=null` 当成未使用参考的证明**。

本轮已从 Drive 重新实际读入参考A像素709×1064，Image执行一次新摄影创作，`gen_id=5f19abff-3a7e-4718-9f20-95413b352a74`。原始941×1672图的SHA256 `f2d797ebaf377518afc6a8c5e3d0b5c151116f2b2f54561c5ebf87ce05fe242d`，[Drive原件](https://drive.google.com/file/d/1XC4rfo1o5_k6uWQ-RD9FCu9y90vBUCBz/view)，真实上传后回读字节一致。另从原文件无色彩修改地居中裁切出严格936×1664（9:16）文件，SHA256 `eddebaf7a2b19453ad0001564b6784c705a83bddfebbe3f71fdbaa8cf976a3ff`，仅在本轮工作区生成，未声称已归档Drive。

独立视觉冷筛：新图部分恢复柔和桃色与层峦云雾及小车，但道路仍在右下而非原参考左下，缺少参考的静谧低反差。天空上35%平均饱和度约53.3，参考约24.4（HSV S 0—255），比R4的约70.6更接近，但**不可据此宣称审美通过**。R5仍是候选，**未完成真人验收、未进入Figma**。详细源身份、审稿和保留边界见[`R5_IMAGE_REFERENCE_DIRECT_USE_RECEIPT.json`](../../evidence/vpd/dituyiwai_photo_20261011/R5_IMAGE_REFERENCE_DIRECT_USE_RECEIPT.json)。

后续唯一当前摄影范围：用户先看R5真实原图给出维度范围明确的意见；不再退回文字任务，不再无依据地迁移生成工具，不改原生任务锁355/检查点377。已完成文字仍复用，只有摄影通过后才进入整图设计。

---

## 2026-10-11 摄影 R4 冷判定：停止无绑定证明的重复生成

- 新聊天续接前已实读 HEAD `73166dd7db72b049decf0f6231db10eb652b2731` 的根入口、适配器、项目路线、原生锁 355、检查点 377、R3 失败回执；`shenmei` 原生 S7 锁未动，当前用户工作重点明确为《地图以外》摄影 R1 来源纠错后的独立新候选。
- 已打开真实参考 `06_确认参考A_暖色山谷山路_截图裁取_非生成.png`（709×1064，SHA256 `fc5b2302cc829d4a864e850c6f59c53fe3be1009946da9db0a5bb000246ee016`）；图上不存在显著发光太阳，天空/云层低饱和，山谷浅桃灰，左下小弯道上仅小车。
- 一次 `image_gen.text2im` 生成 R4，`gen_id=d97a367a-53e9-426e-93ce-23ec2a71c578`；回传没有可机读参考绑定证明，`parent_gen_id=null` 且 `edit_op=null`，不由此推断源图必定参与了条件生成。生成图片 `941×1671`，SHA256 `ea408a7f6ea5d45e23cf6b68e540331cd2c04805f66151ba91c5528c4fe4901d`，上传 Drive `1kOisnRqiVBxs2137ECTzB5fGDNKMnFyD`，下载回读原始字节一致：[R4 原件，仅失败留档](https://drive.google.com/file/d/1kOisnRqiVBxs2137ECTzB5fGDNKMnFyD/view)。
- 视觉/像素冷审：R4 仍出现直接太阳、高对比金黄色，失去参考的雾化低反差与左下道路关系；参考顶端35% ROI 的 HSV 平均饱和度24.4，R4为70.6（0—255尺度），说明预期色彩机制明显失配。这是局部量化辅助，不代替整体审美。**R4=FAIL_CLOSED；禁止晋升、禁止基于它修 Figma、禁止再盲重试同样的生图路线**。
- 唯一进一步处理方向：**先解决显式参考绑定和原样回执**。已实际发现 Adobe Firefly 的 `image_generate` 有显式 `referenceImage` URL 参数，可使输入路径在调用中有证据；**但该插件会消耗 Firefly credits，且 referenceImage 不可与尺寸/比例参数同时指定**。在获得用户对额度消耗及比例裁切方案的许可之前，本记录不启动 Firefly 生成、不再生成 R5。
- 详细回执：[R4_IMAGE_REFERENCE_BINDING_AND_AESTHETIC_FAIL_RECEIPT.json](../../evidence/vpd/dituyiwai_photo_20261011/R4_IMAGE_REFERENCE_BINDING_AND_AESTHETIC_FAIL_RECEIPT.json)；只增加旁路证据，不覆盖原生任务锁、R1-R3、第三方参考和已完成的旧《地图以外》文字母版。
 
---

## 2026-10-11 后续摄影尝试 R3（未通过，严禁视为视觉改进）

- 已真实打开 Drive 参考 A 的原始709×1064 PNG，并与已存旧 R1、R2 的实际像素比较：参考为**无可见太阳的浅桃灰远山、连续白色云海、下方左侧的山路与很小一辆车、低反差雾化空间**，不是耀眼金色日出。
- 本轮 `image_gen.text2im` 实际只调用一次，`gen_id=29ecd090-8c04-402f-934a-2ccc91459dfd`。关键执行问题：调用**没有显式传入指定的原参考 file ID**，工具回传也无参考图绑定清单；不能因为执行者在生成前看过参考图片，就假称模型已条件化绑定到真实像素。返回图仍走高饱和强日出方向，因此本轮 **FAIL_CLOSED**。
- R3 未改动旧 R1 / R2 / 已认可文字母版 / Figma；无自行补图、无第二候选、无晋升。真实输出 `941×1672` RGB PNG（非精确9:16），SHA256 `5830fd77e2d496d9296977b3042f2e5271bf767070b0108944b7844efde6b152`。 [Drive原始图，失败留档](https://drive.google.com/file/d/1od6ki1gKdJJNd9sFd1fFu1b3eqtp5HOX/view)，已实测下载回读 SHA256 一致。
- 详细可追溯记录：[`R3_REFERENCE_BINDING_UNVERIFIED_FAIL_RECEIPT.json`](../../evidence/vpd/dituyiwai_photo_20261011/R3_REFERENCE_BINDING_UNVERIFIED_FAIL_RECEIPT.json)。**唯一真正有效的下一项**不是盲目第三次重投生成，而是先使用能实际附带/可观察参考像素输入的图像生成通道，验证绑定与生成边界，然后再用一张受限候选做实际图像对照；如绑定证明仍缺失，不能报告“参考学习成功”。原生任务锁仍维持旧S7状态，此记录不擅自替换它。

---

## 当天追加：地图以外摄影 R2（2026-10-11）

原生锁 `355/377` 保持不动；用户本轮“下一步”之后已经从 Google Drive 实际取回并查看参考 A 和旧绿色 R1 的两个原始像素文件，完成 SHA256/尺寸核对；**一次** `image_gen.text2im` 生成了新的竖图原始候选，已经归档并实际原字节回读；另外产生精确 9:16 的仅裁切派生文件。

- 原始 R2：941×1672，SHA256 `76a6acce2d5dc67845e2fce1a1d47b587e80e371620cc318a709ed505188c5c5`，[Drive 原件](https://drive.google.com/file/d/154R3cgHtjVnHhU14AuxERilXSW6rrg5t/view)。
- 严格 9:16 裁切派生：936×1664，SHA256 `634b5515b27b3ae562a7258f4782fc084f8537d835f8aa9208502f62f77297b6`，[Drive 文件](https://drive.google.com/file/d/1MbCut8ZZR2tonrXCR4wLdU1448scv8-s/view)。
- **内部摄影审美/内容筛查未通过**：相对参考，缺少应有的小车叙事锚点，日出暖金偏强，构图偏向通用云海日落图。不能把这张称为已验收新底图，不进入 Figma 整图、不覆盖旧 R1、不重做已完成的透明文字任务。
- **重大来源限制**：参考图本轮确已被执行者实际查看，但图像生成工具未提供参考像素绑定的可核验证据，不能声称“模型确实看到了原参考图”；下一次改进必须首先解决这一点而不是盲目复述画面。没有新的自动出图授权。
- 独立实证回执（当前状态唯一新增参考）：[`evidence/vpd/dituyiwai_photo_20261011/R2_ORIGINAL_PHOTOGRAPHY_CANDIDATE_RECEIPT.json`](../../evidence/vpd/dituyiwai_photo_20261011/R2_ORIGINAL_PHOTOGRAPHY_CANDIDATE_RECEIPT.json)。


**同日后续接口预检：** Adobe Firefly 确有支持显式 `referenceImage` 的图片生成工具定义，但在当前聊天实际调用 `adobe_mandatory_init` 得到 `The tool failed internally.`，因此 Adobe 路线 **连接前置失败，不得声称已接通、已绑定或可以立即生成**，没有调用其生成接口、没有使用 Firefly 点数。需要先解决可用参考图接口（或连接器故障）和额度授权才进入下一张生产，绝不重播 R1—R4 失败。

**此图片证据仍是旁路工作记录，不改变原生 S7 真人 PENDING 与既有 P7 主线结果**。下一次新聊天应在读完原生状态后阅读本段新增 R2 回执，先处理摄影真实参考绑定和新候选，不倒回已完成文字。

---

## 2026-10-11 用户纠错｜当前交互的视觉创作重点为《地图以外》摄影 R1（优先阅读）

**最高优先级解释：** 本文件下文“唯一下一动作=审 S7”只是 `shenmei` 原生 `CURRENT_TASK_LOCK.json` 至今未改写的既有业务锁记录，**不是用户在最近聊天里要继续执行的最新创作目标**。2026-10-11 用户纠正了上一轮接管错把原生 S7 当作《地图以外》最新任务的错误。现阶段用户讨论的是《地图以外》摄影方向与图源识别，而非重启文字制作。本次记录不偷偷改变原生锁，未来若正式转移原生任务须另行按授权与单作者接续。

**R1 身份分离（依据用户本次提供的上轮实际纠错说明和最近会话，不把它冒充本轮 Drive 图片像素回读）：**
- 暖色山路云海图片：网上摄影参考，**非 ChatGPT 生成的新成品**；摄影师/拍摄时间/授权未独立确认，不得冒认来源，不可把该图片交作原创成果。
- 绿色草坡、道路没入灰色雾中的图片：此前被归档称为旧 `R1` 的真实候选；在暖色参考的色彩、山谷层次、云海和空间构图方面存在明显差距。
- 历史真人表述“R1保留，我觉得不错”：用户当时眼前图片与实际文件可能错配，**不能自动绑定成绿色 R1 的明确审美通过**。上轮助手宣称已向旧 R1 Drive 记录追加纠错；本次尚未直接读回该 Drive 修订原件，不冒称再次核验。
- 当前期望方向：以暖色山路云海参考为**质量与空间叙事锚点**，创作真正新的 **9:16 原创摄影底图**；不能拿网上参考冒充 AI 出图；新的高质量原创底图截至本次复核仍**未有确认交付**。本次只是对齐和保存状态，不授权立即生成。

**《地图以外》文字资产已经完成，不应回退返工：** 本次已实调已连接的私有插件 `get_typography_delivery`，task_id=`typo_f904cbe7-12ef-4ce1-a6ac-37e16d7c009c`，revision=`14`，`status=COMPLETE`，`next_required_action=NONE_COMPLETE`；透明文字母版 SHA-256 `5b438be548d6db51e16f328416aaa293e814c4868b42f094eb8cc5326480f2e4`，670×946 RGBA。**真实制作链是图片生成的 RGB 文字素材 + 程序化颜色遮罩形成透明 alpha + 用户已认可文字的准确重新排版，随后 Figma 重建 37 个原生可编辑矢量，零贴图文字节点，分区像素审核**。既不是一次无修复的 Image 输出，也不是 Figma 单独创意设计。37个矢量可编辑轮廓不等于37个可直接替换字符串的 TEXT。文案、母版和已通过的 Figma 制作可以直接复用，不必重启文字流程。

**下轮边界：** 用户当前追问的是摄影 R1 及制作来源，应先修正“参考/生成图/已验收范围”的证据对应，再在真实创作授权范围内推进摄影主视觉；**不按旧 S7 文字审核任务强行切换主题，不重新修改已完成的《地图以外》文字，也不擅自恢复其他任务**。不同任务流必须分开登记，原生锁和插件任务不是同一个数据库状态权威。

---

> 性质：**接管核对与工作流保存快照**；不是新任务锁，不批准出图、改 Figma、扩预算、启动自动化、修改主线或晋升作品。若本文件与最新原生状态发生冲突，以当次实际读取的 `CURRENT_TASK_LOCK.json`、`LATEST_CHECKPOINT.json` 及用户新明确指令为准。不可把本文件的“下一步”当成第二个任务系统。

## 一、权威入口与读序

- 仓库：`vubaoha034-hash/shenmei`；分支：`visual-program-distillation-v2-photography-design-20260814`。
- 本次读取时基线 HEAD：`0afdd2ae1b4d30d8f001d9b3d203ecfb27a44428`，2026-10-08 的“v0.3.0 包发布”提交。本文件写入后 HEAD 必然更新，不能将此基线误作未来 HEAD。
- 根入口：`START_HERE.md` → `AGENTS.md` → `PROJECT_CONTROL_ADAPTER.json` → `VPD_PROJECT_ROADMAP.md` → `continuity/vpd/CURRENT_TASK_LOCK.json` → `continuity/vpd/LATEST_CHECKPOINT.json` → 当步真实规则与资产／回执。
- 最新业务状态的**核对时**锁修订 `355`，检查点序号 `377`；两者都记录至 **2026-10-06 19:20:26（北京时间）**。当前任务 `VPD-CHAZUO-CODEX-COMPLETE-POSTER-20261003-01`；状态 `VPD_CODEX_CHAZUO_CORRECT_SOURCE_REFERENCE_STUDY_DELIVERED`；唯一原生下一动作 `LIU_REVIEW_LIUXIANSHENG_CONTENT_TRANSFER`；没有从本快照触发该动作。
- 核对时 checkpoint 指向当前锁的 SHA-256 为 `4eee3b6aec2ee8979bc96f3e1193636caa986b16d779bd8bdd15263e1652428f`。本次经连接器直接读取文件，**未运行**本地 `python scripts/verify_visual_memory.py --vpd-state --status-card`，不能把该命令标成已通过。下一实际写业务状态前须在有效执行环境核验远端 SHA、锁/检查点/账本，并按单作者流程推进。
- 权限：Root 是业务状态唯一写入者；独立执行者可产出图片、设计源与证据，**不得自己覆盖任务锁**。任何并发 HEAD 冲突先查明，不强推。

## 二、已完成、局部通过、失败、未完成

| 项目 | 实际结果 | 严格边界 |
|---|---|---|
| 冻结参考、历史方法与旧候选 | 资料和不可变证据保留，`MAINLINE_LOCK_20261001.md` 已固定目标 | 不因后续失败重写原认可、不清零历史 |
| 主线 P3 茶作、P4 换内容/画幅、P5 第二风格、P7 交付 | **P7 有界实验交付 CLOSED/COMPLETED**，有效候选和失败证据已留存 | 画幅精确生产验证仍不足；P7 不是完整系统商业验收，`system_validation_complete=false`、`global_production_promotion_allowed=false`；真人整图设计否决保留 |
| 茶作摄影 | 用户认可的局部去字重建摄影 SHA-256 `7fd7777fed21100cb6b47bc305701476054263565e73246ac469d065aa080618`，Drive `1ZU-jfc_3JZqNlKn56PSpMyBLjwYnqIIA`、Figma 节点 `283:5` | **摄影单项受保护**；不代表文字或海报整体通过；这不是找回“隐藏无字原图” |
| 茶作文字/完整海报 | 同一正确摄影曾串行做到 **V29，28 次修订**；V29 AI_PASS 的历史评估存在 | **真人文字 REJECTED；整体未完成正式认可**。不要把 AI_PASS 当真人通过；不得擅自产生 V30 |
| 山野集参考文字学习 | S1、S2 等真实文字研究和可编辑 Figma 已归档 | 局部形态复建不证明可以换字泛化；研究的人审仍有 PENDING |
| 山野集文字机制→“刘先生”迁移 | **S7 已交付**，960×1280、Figma `453:10`、主字标 `453:37`；12 个原生可编辑 TEXT，主标 9 个 VECTOR；两图独立审稿 `CONTENT_TRANSFER_PASS_WITH_LIMITATIONS` | **真人 PENDING**。字标矢量可调曲线，不能直接输入新字；完整摄影、商业成品、跨风格迁移与可重复高审美均未证实 |
| 工作流插件 | 已有私有插件连接/只读调用历史证据；站点原地更新到至少 v0.1.5 的工程部署记录；仓库已有 v0.3.0 完整源码包 | `CURRENT_RELEASE.json` 仍写旧 0.1.1；**v0.3.0 包在仓库 ≠ 线上运行 v0.3.0**。未取得 v0.3.0 真实部署/原样回读证明；控制器测试 ≠ 作品验收 |
| 蘑菇摄影 Golden | 已认可的真实像素真实性基准，应长期保存为绝对明显 AI 感回退的审稿锚点 | 不是当前新作品或默认加入生成上下文的第二参考；不可用文字描述代替原始像素 |
| “地图以外”近几日聊天推进 | 有关于参考、透明文字母版、Figma 可编辑还原的进一步讨论和局部成果回报；指定 9:16、情侣车中驶向“地图以外”的画面方向 | 此分支的原生锁**尚未**以实际回执登记为完成。最近聊天说明原创 9:16 摄影底图尚未产出；**未授权本次直接生成**；不能凭聊天口头总结冒充锁更新 |

实际 S7 原件：[Drive 完整 PNG](https://drive.google.com/file/d/1svX-5kyxGBA-hEKg6iq_xMaxcwYU0Ubt/view)；[Figma 可编辑源](https://www.figma.com/design/uyDxOoN1iNDPpEHTKSUWg1/?node-id=453-10)；[字标 SVG](https://drive.google.com/file/d/15COp7aWZ7sKWKDinV3KasEQ38lVzt0e5/view)。回执：
`evidence/vpd/codex_takeover_20261003/liuxiansheng_content_transfer_20261005/DELIVERY_MANIFEST_S7.json`；
`.../s7_final_verified_review/PIXEL_REVIEW.json`；
`continuity/vpd/codex_takeover_20261003/WORKER_CURRENT_REUSE.md`。

## 三、端到端总流程（唯一长期目标）

**目标不是做出一张顺眼海报，而是从用户认可的真实参考像素提炼可迁移的视觉方法，稳定产出包含摄影、文字及图文关系的完整优秀作品，并验证换文案、换画幅、换风格而不是套模板。**

1. **任务与真实来源锁定**：读本次参考和批准范围的实际像素，登记素材身份、SHA-256、画幅、文案、产品事实及来源；划分哪些是已通过部分、哪些是待改善部分。不能用历史形容词或错误参考替代真实图。
2. **精确蒸馏**：拆解注意力结构、主体尺度/位置、留白、材质/光线、色彩机制、标题形体、辅助信息、负形及图文相互作用；得到 5—8 个高杠杆可成像变量，分稳定骨架与合理变化轴。不要写长篇审美提示词或机械复制原品牌轮廓。
3. **完整画面策划**：设计先于生成，明确新的主体、空间、叙事、光影、字形占位与各自关系。不能先生成一张无关照片，再硬贴文字和叶子。规划需以真实参考独有视觉关系为依据，而非“高级”“艺术”泛词。
4. **主视觉摄影分支**：如本任务明确允许出图，制作无烘焙文字的照片/主视觉；绝对检查真实性、物体结构、整体构图与比例，而不只看局部质感。蘑菇 Golden 只用于真实感冷审比较；不因文字修改而重做已获认可的照片。存在已认可底图时只可在打开的局部范围修复。
5. **独立文字资产分支**：特殊主字标用实际图稿先把整体字形创作好，再在 Figma 还原成原生可编辑 TEXT/VECTOR；普通辅助字遵循来源/授权。严格防止“套现成字体＋装饰叶子”的伪设计。文字正确和文字美观分别判断。
6. **Figma 原生合成**：在获批准的照片和文字资产上做有设计因果的排布：标题与主体互相借位、负形相互解释、色彩作用一致、视线动线清晰；检查移动/缩放后的空间关系。保留照片、字标、辅助信息、蒙版各自独立图层，不以扁平贴图代替可编辑设计。
7. **真实导出与双层审核**：实际原始 PNG、Figma 源和所有引用素材可回读；硬事实审计检查文字、尺寸、保护区和原始像素/哈希；另做独立像素审美冷评，在缩略图、正常观看、原尺寸看真实作品，重点评照片、文字、融合、品牌辨识、新意、AI 感与图像完整性。**技术 PASS 不代表审美 PASS，独立 AI PASS 不等于真人 PASS**。
8. **真人验收与有界局部修复**：真人认定哪一维过、哪一维不过；冻结已获认可部分，仅改变一个明确失败维度，提交一张可见候选并和受保护最佳版比较；若退化回滚。不能把“有点好”升级成“整图通过”，也不能借字形失败推翻摄影成功。
9. **原始证据与发布**：保存真实照片、透明文字母版、Figma 可编辑源、最终 PNG、源参考、提示词与可观察生成参数、导出 SHA、审核意见、局部失败样例与真实执行成本；通过 Drive/Figma/GitHub 原生链接指向，实际回读后更新任务锁、检查点和原账本。未经最后人审，不晋升 Golden 或商业生产母版。
10. **迁移/价值验证**：在同一参考家族换内容、换画幅，再以明显不同的已批准家族复测；保留直接参考与蒸馏方式的公平对照。没有整体可用作品就不宣称“系统成熟”；测试没有收益就删去冗余规则，保留失败边界，不靠增加审核层数冒充质量进步。

其中 P0–P7 的原生历史阶段身份和已有结果继续遵从 `VPD_PROJECT_ROADMAP.md`；此处是方便未来实际生产的**执行视图**，不是重启已交付 P7 或修改已冻结历史。对当前正式作品，先让真正图文合成优秀，再谈更大规模迁移。

## 四、独立透明文字链｜v0.3.0 源码合同（**尚未核实线上全面运行**）

当前仓库最新包 `plugins/visual-aesthetic-workflow/v0.3.0/` 所定义的五步顺序：

1. `REFERENCE_TEXT_EXTRACTION`：实际读参考像素；逐个标注所有可见文字区域、角色、位置和保留/替换决策；新任务明确 5 类目标文字：主字标、顶部标、英文、竖向文字、底部文字。
2. `AI_COMPLETE_TRANSPARENT_TYPOGRAPHY_MASTER`：调用图像工具生成**真正完整透明 RGBA PNG 文字母版**。不允许用 SVG 导引、整张海报、聊天里的提示词或无像素凭证代替。
3. `FIGMA_EXACT_EDITABLE_REBUILD`：母版是 Figma 视觉形态的唯一真值；原生 TEXT/VECTOR 重建所有区域，交付时不得有作为文字替代的 IMAGE 节点；主标若是矢量，改文案需重新设计，不能假装可直接改字。
4. `INDEPENDENT_MASTER_FIGMA_PIXEL_AUDIT`：由实际可读两张 PNG 字节的执行器独立测量透明母版和 Figma 原生导出图（不是与整张参考照片比较）；按总区域及分区域核对字形、色彩、尺寸、位置，文本逐字另查。源码指标包括 alpha IoU ≥ 0.97、单区 ≥ 0.95，归一化 RGBA 平均误差 ≤ 0.04、单区 ≤ 0.065，边界框误差 ≤ 2 像素。这些阈值只检验制作一致性，不证明审美高级。
5. `ISOLATED_TYPOGRAPHY_DELIVERY`：交付母版、原生可编辑 Figma、分区审计、原件位置、版本与回执，完整可重新读取。**插件服务端只校验外部证据声明，不自己读取图片字节**；需外部审计脚本真实运行才可能称像素通过。

源码 `v0.3.0/server/typography-task.mjs` 将旧隔离任务升级定义为显式 `upgrade_typography_contract`；需要原任务 task_id、revision 并保留旧历史和 native_snapshot。**未实际调用不能说旧任务已升级。** 新合同和旧主线锁是不同范围；不能拿 0.3.0 包覆盖 S7 的真人 PENDING。

## 五、常见失败与禁止项

- **摄影通过 / 文字失败**：只修文字与图文关系；除非真人明确重新开放摄影，不重生摄影。
- **Figma 制作精确 / 原图形态一般**：回到创作图稿，不能靠 Figma 精修产生原本不存在的设计张力。
- **文字高质量 / 整图没有关系**：回到图文共同构图，不用叶子、线条、渐变色块伪造联系。
- **参考像素缺失**：停止对“是否学会风格”的证明；源位置和形容词不等于实际读图。
- **模型审核通过 / 真人否定**：以真人对该维度的实际意见为准，旧 AI PASS 保留但不得晋升。
- **源代码、CI/单测、插件返回 PASS**：仅证明对应工程事实，不代表作品专业、审美提高或线上版本已切换。
- **已用/失败生成**：按原任务规定计数与保存，不隐藏变体、不重试博概率、不改历史记录。
- **任何新规则/Skill 改动**：先读 `AESTHETIC_SKILL_DESIGN_CHARTER.md`，优先少而准确、删掉无效规则；不要为每个“丑”新增一个工程门。
- **私人源、密钥、素材**：只存受控 Drive/Figma 原件和不泄露的来源描述/哈希；不得提交明文密钥、私有原始图片或临时签名 URL。

## 六、恢复命令与唯一下一动作

新聊天可直接使用：
> 接管高级感P最新视觉任务。实际读取 `vubaoha034-hash/shenmei` 的 `visual-program-distillation-v2-photography-design-20260814` 最新 HEAD；按 START_HERE、PROJECT_CONTROL_ADAPTER、ROADMAP、CURRENT_TASK_LOCK、LATEST_CHECKPOINT、当前证据及 `continuity/vpd/PROGRESS_AND_END_TO_END_FLOW_20261011.md` 恢复。只信当次真实权威状态，不重做旧成果，不因整理记录改变任务；汇报已完成、未完成、唯一下一步。

**截至本次快照：**原生下一动作是将已存 S7 真实作品交刘先生审核：`LIU_REVIEW_LIUXIANSHENG_CONTENT_TRANSFER`。当前的“地图以外”完整作品创作方向与蘑菇真实性 Golden 应分别保留为近期讨论/质量基准；如有新的明确创作授权，先登记相应实际参考和目标，不擅自覆盖原任务锁。

保存说明：本文件仅登记已核实的状态、证据边界和可复用程序。没有运行状态校验脚本，没有出图，没有操作 Figma，没有更新业务任务锁/检查点/账本，没有把聊天里未回读的交付晋升为仓库权威。

## 七、2026-10-11 追加：从**已连接的线上插件**实际只读回读的现状

此附录晚于本文件前面的 GitHub 代码核验。已实际调用同一私有插件的 `get_current_workflow`、`get_typography_delivery`、`get_image_first_workflow`、`get_photo_composition_workflow`。返回 `plugin_version=0.5.0`，应优先作为**当前线上插件运行版本**的证据；`plugins/visual-aesthetic-workflow/v0.3.0/` 是仓库中历史源码包，`CURRENT_RELEASE.json` 的 0.1.1 为旧历史登记，不能冒充当前运行版本。

- 原生项目状态：`get_current_workflow` 在本文件首次写入后回读 commit `f877e30c4a81cacc6e5d31354878545b7b51305f`；原生锁 SHA-256 `4eee3b6aec2ee8979bc96f3e1193636caa986b16d779bd8bdd15263e1652428f`、revision `355`、checkpoint sequence `377`；原生唯一下一动作依然 `LIU_REVIEW_LIUXIANSHENG_CONTENT_TRANSFER`。这是插件的只读原生快照，不是新业务状态提交。
- **《地图以外》旧参考文字任务（确实完成）**：`typo_f904cbe7-12ef-4ce1-a6ac-37e16d7c009c`；任务修订 `14`；`status=COMPLETE`，`next_required_action=NONE_COMPLETE`，`completion_claim_allowed=true`。生成透明文字母版 `dituyiwai_master_rgba_670x946.png`，SHA-256 `5b438be548d6db51e16f328416aaa293e814c4868b42f094eb8cc5326480f2e4`；已取得真人对母版的明确批准。**母版的透明效果有后处理/校正文案成分，不是一次直接输出完整 RGBA 的证明。** 原 Figma 文件 `Ul7UeikXjD9uE7qHluRfky` 节点 `14:2`，实际回读 **37 个可编辑 VECTOR、0 个原生 TEXT、0 个 IMAGE**：轮廓可编辑，但不能把矢量字说成键盘一改就行。原生导出有独立实际双 PNG 字节审计通过，**不是零像素差、不是无损完全相同**；记录 146062 个变化像素，母版与导出 SHA 不同。Figma 源：https://www.figma.com/design/Ul7UeikXjD9uE7qHluRfky?node-id=14-2。这一局部**文字交付**完成不代表摄影/完整海报完成。
- **《地图以外》新参考文字任务（未完成）**：`typo_6fad2cc2-cbea-4457-830d-ed63f339779a`，新参考名 `1000031655.jpg`，真实参考像素已检查并登记 SHA-256 `bd37054c151b1fe62d39879fbb247483da605213105eb09ffe59e06ac39dc6f4`（1149×1536）；任务修订 `1`，`status=IN_PROGRESS`，`stage=IMAGE_MASTER_REQUIRED`，唯一插件内下一动作 `RECORD_IMAGE`；未有已批准的新透明母版、没有该新参考的 Figma 成品和独立像素审核。**不得用旧任务完成状态冒充新任务完成**。
- 线上通用文字流程的实际合同版本为 `reference-image-first-typography/v1`、`workflow_version=0.4.0`：用户上传并核验**真实参考像素** → 图片工具创作**纯文字、无摄影背景、透明 PNG** → 明确真人审查/批准 → 原 Figma 中以 TEXT/可编辑 VECTOR 复刻（不允许用整张扁平图片冒充）→ 实际读取两 PNG 进行独立分区域像素差审计和交付；原任务可按需在原 ID 原地续办，禁止重建第二个相同任务。
- **可选摄影/完整海报合成流程**已经由同一线上插件 `0.5.0` 的只读合同实际返回，其工作流版本 `0.5.0`、schema `approved-lettering-photo-composition/v1`；它属于**完成并批准文字父任务之后的独立子任务**，不是文字任务自动延展，也不是已实际制作作品的证据。流程：确认已完成获批文字父任务/其同一 Figma 文件 → 实读用户照片原字节、真实 MIME、尺寸与哈希 → 规划构图并冻结人物/摄影保护区 → 同一 Figma 文件新建独立 frame，**一个原照片 image fill + 可编辑的文字矢量/普通 TEXT** → 实际导出 PNG/节点回读，独立检查照片保真和层次关系 → 真人批准整张海报 → 交付真实 PNG + 原生 Figma 源。这条路明确 **不得重生成用户提供的摄影原件**；插件服务端只核验提交的外部证据字段，本身不能解码原图或自主操控 Figma，不得无工具调用声称完成。只读调用 `get_photo_composition` 未给出任务 ID，返回 `COMPOSITION_ID_OR_REQUEST_KEY_REQUIRED`，**没有证据表明有摄影合成子任务完成**。
- 线上插件的阶段与 GitHub 原生锁各管不同范围：`get_typography_delivery` 状态可以说明其 D1 隔离文字任务是否完成，但**不能覆盖**原生茶作/S7 的锁、评价、真人门、推广资格或阶段。当前核对**没有运行**真正的新作品生成、Figma 写入、母版回读或摄影合成。
- **接管结论**：原生 S7 等真人审稿；《地图以外》旧透明字形支线已经完成；新参考字形支线等待 Image 生成新母版并经真人审核；9:16 真实摄影与成品合成还需另核对实际照片、执行与子任务证据，不把待办推断为完成。下一对话先读最新原生锁，再按明确要继续的具体 task_id 查插件，**不要重做已完成旧任务**。

