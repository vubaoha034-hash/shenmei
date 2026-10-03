# 茶作当前成果与独立 worker 调用入口

当前说明优先于下方历史过程，实际状态仍只由原生任务锁决定。2026-10-04刘先生已否定V3文字与完整设计，V3真人结论REJECTED；已撤回“请真人验收失败成品”的请求。正确摄影上本次一初版、两修订均真实制作与冷审，三版都AI_FAIL，预算3/3、修订2/2。V1/V2未虚构单独真人结论；旧三版否决另行保留。摄影认可继续有效。唯一下一动作是明确同一任务新增正式版本范围（CONFIRM_ADDITIONAL_SAME_TASK_DESIGN_VERSION_SCOPE），不重新验收V3、不清零计数、不自动继续第四版或迁移。

本次批评的逐字记录、V3冷审与真人失败对账在 `evidence/vpd/codex_takeover_20261003/lettering_correction_20261004/HUMAN_REJECTION.json`；实际官方案例像素核查、根因与同一方向纠偏依据在该目录 `ROOT_DIAGNOSIS.md`、`PROFESSIONAL_CASE_METHODS.md`、`CASE_PIXEL_READS.json`。这是专业方法研究与失败处置，没有新增作品，也没有视觉改善可宣称。FontTools与design-critique的工具能力不能冒充中文品牌字标制作能力。

| 版本 | Drive完整原件 | Figma同文件：frame / photo / vector | 完整PNG SHA-256 | 冷审 |
|---|---|---|---|---|
| V1 | [原件](https://drive.google.com/file/d/1CoBStVipE6iysm2eeg9aa-wF8Eg8VPzE/view) | 286:2 / 286:3 / 286:4 | a3f2dac976dbd99fc5a0867df625ffe1548f46f75655eb6dc6ed2c78b9cc3e96 | AI_FAIL |
| V2 | [原件](https://drive.google.com/file/d/1dsAgR4S_TENd5FTdo6QNeIylaFR9PfLZ/view) | 287:2 / 287:3 / 287:4 | c92aa90e87c867503a3a53ab869dc079bbec9de44f7a31a07103bb692f26cae4 | AI_FAIL |
| V3失败归档 | [完整PNG](https://drive.google.com/file/d/1j249tXSd8KFJKFonBdFsng4aUJpg_xZ-/view) | [290:2](https://www.figma.com/design/uyDxOoN1iNDPpEHTKSUWg1/?node-id=290-2) / 290:3 / 290:4 | 0d2dbf6421f505f95b4ed9aaafd7648b28bbbefb9a01bfd85a856a57d9bd8826 | AI_FAIL / 真人REJECTED |

V3 [字标SVG](https://drive.google.com/file/d/1ceZuyHDkMTzeW5qw0-j-qtfaZlD6PvZn/view)，SHA f83a8b20b2b97c2e53bd40b85124023d53fea0c397ad8ac90dae7382eaeb823e。Figma file key uyDxOoN1iNDPpEHTKSUWg1，page251:2，V3有9个可编辑VECTOR（2字标+7标题），0原生TEXT，不能宣称可直接打字。Unicode标题源、轮廓加工脚本、许可、来源及修改依据在 `evidence/vpd/codex_takeover_20261003/correct_source_typography/assets_v1/`、`assets_v2/`、`assets_v3/`。每版像素审稿与隔离证据在同目录 `v1/pixel_review/`、`v2/pixel_review/`、`v3/pixel_review/`，技术/Drive/专业审查也分别保留。

V3冷审认为字标仍接近常规宋体、独特结构弱；标题气质与自然摄影不协调；品牌、标题、产品重心分散。刘先生此次否定与此前AI_FAIL一致，只报告这个实际对账，不虚构准确率。工程检查不改写审美结论。视觉收益未验证，节时收益未测量，整图已被否定，整体蒸馏及迁移能力尚未验证。

实际采用的成熟方法：

- [Anthropic官方design-critique](https://github.com/anthropics/knowledge-work-plugins/blob/d3ee81913e5e179273313345847a2a4f42449bd2/design/skills/design-critique/SKILL.md)，提交d3ee81913e5e179273313345847a2a4f42449bd2，Apache-2.0。上游 `skills/design-critique/upstream/` 与项目thin wrapper `skills/chazuo-independent-art-review/SKILL.md`。实际三次brief调用第一印象、层级、间距、区域证据和优先问题，排除网页UX项；不能冒充中文品牌字标技能。
- [FontTools](https://github.com/fonttools/fonttools/tree/978d9edccb60ea0e5fbad7015cb11817c3532328)4.63.0，提交978d9edccb60ea0e5fbad7015cb11817c3532328，MIT；[Adobe Source Han Serif](https://github.com/adobe-fonts/source-han-serif/tree/7889f11bf31170b5d092a083b357c8c8130f89e0)2.003，提交7889f11bf31170b5d092a083b357c8c8130f89e0，OFL1.1。V3基于许可轮廓作局部Bézier加工，字体软件未改写，字标不是100%原创。没有找到经本项目验证有效的自动中文品牌字标技能；这些是专业工具与实验方法。
- 实际 Python3.12.14 / FontTools4.63.0 / Node24.19.0 / sharp0.35.4，模块位置、SHA及真实执行见各版provenance。用load_workspace_dependencies查询bundled runtime；本机FontTools来自已有hermes venv site-packages，新环境先检测。许可字体原件位于 `evidence/vpd/codex_takeover_20261003/skill_research/fonttools_bounded_probe_v1/upstream/adobe-fonts/source-han-serif/OTF/SimplifiedChinese/SourceHanSerifSC-Regular.otf`，SHA78aa7a328fd974df2d688c8a9fd74a33d8334dfa84ab24d9d11efb2ffc464117。
- 本次矢量制作没有调用生图；此前一次局部摄影修补用内置image_gen编辑，底层模型名未暴露。没有重生摄影、训练、付费算力或定时任务。好底图的完整原始生成输入仍不足，不能从单一样本虚构可重现生图规则。`.skill-evolution/vpd-correct-source-worker/`仅一次工程观察，无审美规则晋升或权重训练。
- 稳定 `scripts/vpd_export_photo_safe.py` 保真导出：raw Figma保护区有1152像素最大1级RGB舍入差；正式PNG保留既定文字区域的raw像素，其他1,204,672像素复制冻结源，实测差0。不能声称raw Figma本来零差。

### 全新克隆恢复真实像素

字体二进制被Git忽略，不随克隆分发。重新制作文字时，从 `evidence/vpd/codex_takeover_20261003/skill_research/fonttools_bounded_probe_v1/FONTTOOLS_FONT_SOURCE_MANIFEST.json` 的OTF条目获取固定提交raw URL，下载并核验24,543,332 bytes及上述78aa…完整SHA，再放回其声明的字体缓存路径；许可随仓库保留。全新读取worker已仅凭该清单实际下载HTTP200并核验原字节，未安装软件、未修改tracked文件。使用现有SVG/Figma矢量不需要字体安装；重跑制作脚本需要该许可原件和实际FontTools依赖。具体证据见最新回执中的fresh_entry_recovery结果，不把本机字体缓存冒充Git交付。

Drive是图片主存储，私有项目目录1wV_R9VcJQ9z4sOynHtHczkSP9z3KpK9O。用连接Drive的fetch(url=原件地址,download_raw_file=true,include_base64=true)获取真实b64_string。signed download_url曾403，不盲目重试；实际raw base64回读均字节匹配。每版DRIVE_ARCHIVE.json含ID、revision、SHA与元数据，字标在WORDMARK_DRIVE_ARCHIVE.json。不得提交签名URL/base64。

将已认可摄影（ID1ZU-jfc_3JZqNlKn56PSpMyBLjwYnqIIA）及V1–V3实际fetch结果写入私有bundle：`{"entries":[{"drive_id":"实际ID","raw_base64":"实际fetch的b64_string"}]}`。运行 `python -B scripts/vpd_restore_correct_source_exports.py --bundle .liu-visual-private/drive-restore-bundle.json`，再运行 `python -B scripts/verify_visual_memory.py --vpd-state --status-card`。脚本从原生锁/Drive回执绑定路径和SHA，先验证所有输入及私有路径，再恢复缺失PNG并读回；业务状态写入0、新增版本0。冲突报错。专业审查发现的路径逃逸已修复并留前后证据；不宣称OS沙盒隔离。

校准P/N真实Drive归档在CALIBRATION_DRIVE_ARCHIVE.json：P 1QPZuDYcha0RGI-tGAnZSFvaQiHdFSBtu（仅文字认可，摄影否决），N 1tAA78AyYpjiaKKYiG1uJyjt3TOZw0jwO（整体否决）。参考R 11HpNmepnqlyZNs4uzUTjjEbP8LWwPutC，SHA87a28f5cd4b5d15b01e6536206127c357043a904b3c0dab3bfa0c50080782167，只用上半广告。S为7fd摄影，T本版成品，审稿当时T真人/旧AI结论隐藏。P/N不是最高水平标准。历史一例隐去真人否决的检验与当前V3各有实际失败对账；保留原盲审，不把后来的真人反馈填回旧审稿或虚构总体准确率。

新的读取上下文恢复结果以最新原生receipt引用为准，不能用本机缓存成功冒充全新恢复。以下保留调用协议与过程，V1描述是历史定位而非当前唯一动作。

先固定分支最新提交，读取 START_HERE.md、原生 CURRENT_TASK_LOCK.json、LATEST_CHECKPOINT.json、PROJECT_CONTROL_ADAPTER.json。唯一权威仍是原生任务锁；本文件只解释如何调用成果。

刘先生已认可局部背景重建摄影（7fd7777f…）：Drive 1ZU-jfc_3JZqNlKn56PSpMyBLjwYnqIIA；Figma uyDxOoN1iNDPpEHTKSUWg1 / 283:5。完整原字节、透明层和原第一张仍按 SOURCE_RECOVERY_DRIVE_REUSE.md 恢复。不是无字隐藏原件恢复。

最新用户授权：独立 worker 审核，不通过就在同方向修复复审；通过后保存、内部验收并推进已授权下一项。worker 不能改主线，除非刘先生明确同意。当前调用 INDEPENDENT_WORKER_CONTRACT_V2.json 及 WORKER_FORMAL_REVIEW_CARRIER_AMENDMENT.json；旧合同和审核路线保留为历史。主执行者是唯一状态写作者。审稿只看 P/N/R/S/T 五图：P认可文字但否决摄影、N否决设计、R指定参考上半广告、S已认可7fd摄影、T本版成品。target真人及旧AI结论隐藏。

当前真实载体为新建的项目外 Codex task（projectless），没有继承创作聊天或仓库上下文。不能称它为 fork-none 子代理；其 fork_turns 为 NOT_APPLICABLE_NEW_THREAD。子代理线程数量已达上限、旧CLI TLS失败均有实际记录。保存 WORKER_CREATION.json 后调用 scripts/vpd_collect_agent_review.py，加 --supplemental-source --formal-work-unit CHAZUO_APPROVED_SOURCE_TYPOGRAPHY_20261003_R1 --carrier-amendment continuity/vpd/codex_takeover_20261003/WORKER_FORMAL_REVIEW_CARRIER_AMENDMENT.json --projectless-worker-creation 对应本版文件，并指定实际新task运行文件。collector核验实际create_thread调用及返回threadId、单一真实model/effort、五次view_image结果、无额外工具读取和本版SHA。缺看图或隔离证据不能通过。现有子代理只作独立实现审查，不能冒充本版冷审。

当前 work_unit 是原茶作未完成字标与文字编排在已认可正确摄影上的续办。旧三版/两修订仍为用尽、AI_FAIL、真人 REJECTED，不清零。本次同方向最多一初版加两修订为主执行者自限；不新增品类、画幅或第二风格，不再生成摄影。精确文案“一杯茶，慢下来”，1536×1024。当前版本及唯一动作只从 worker_continuation 与顶层任务锁读取。审核意见不是新授权。

AI_PASS 只允许内部交付，整张海报真人结论须单独记录。达到最终成品真人审查门或真实阻塞才停；不要求用户每步重复继续。图片存原 Drive 项目目录并逐次回读，Figma保留可编辑来源，Git保存代码/证据/原生状态。执行环境实际模型从 turn_context 核验，不凭提示名称。

V1当前实际成品：Drive 1CoBStVipE6iysm2eeg9aa-wF8Eg8VPzE，SHA a3f2dac976dbd99fc5a0867df625ffe1548f46f75655eb6dc6ed2c78b9cc3e96；Figma同文件286:2 / 照片286:3 / 矢量286:4。独立worker 01a101e6-416a-7590-bac0-f9cf39f9efa7 实际判AI_FAIL，证据在 evidence/vpd/codex_takeover_20261003/correct_source_typography/v1/pixel_review/；修订在同一方向进行，准确最新版以原生锁的versions为准。

本轮writer还核验实际CODEX_THREAD_ID，仅本root有业务写入权。以后换主执行上下文，先依照当前锁登记主执行者交接、核实新的实际root身份并更新writer授权绑定，不能把子worker升级为状态写作者。读取、素材下载、复用SVG无需业务写入权。没有新真人指令不得变更主线。
