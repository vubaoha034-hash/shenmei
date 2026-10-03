# 独立审稿与技能复用入口

从根 START_HERE 读取最新原生任务锁，先读 [原件纠偏](RECONCILE_REFERENCE_AND_FEEDBACK.md)。正确第一图是 e7af9c9e…，不是 R4；摄影正向和文字否决分别保留。当前三版/两修订均已用尽，唯一业务下一动作仍是恢复正确第一图的无字摄影源。

本轮刘先生要求多角色介入、检查并采用审核 skill 后继续。授权原文在 `INDEPENDENT_REVIEW_USER_AUTHORIZATION.json`。三个角色分别负责执行与原生保存、独立技能研究、独立审美判断；审稿人没有继承创作历史，只有主执行者写业务状态。

实际采用 Anthropic 官方 `design-critique`，固定提交 `d3ee81913e5e179273313345847a2a4f42449bd2`，Apache-2.0。上游 SKILL、许可、CONNECTORS、README 的真实固定字节及SHA见 `skills/design-critique/upstream/` 与 `SOURCE_SNAPSHOT.json`。Codex安装版只移除不支持的 argument-hint 元数据、修复 CONNECTORS 相对链接，审核核心不变。安装目录为 `C:/Users/Administrator/.codex/skills/design-critique`：下一轮可发现，本轮已显式读取并将实际审核核心提供给独立审稿人。跨环境可读取仓库镜像，不依赖此电脑路径。

项目适配入口是 `skills/chazuo-independent-art-review/SKILL.md`。它复用既有 personal-aesthetic-critic 的快速视觉诊断，分开摄影/设计/正确性，不执行三页或十页品牌方案门槛。官方 skill 主要是UX评审；其中文字形专科能力未验证，当前仅作为实验性审核方法，不以官方身份宣称审美成熟或已提高成品质量。

真实审核见 `evidence/vpd/codex_takeover_20261003/skill_review_20261003/PIXEL_REVIEW.json`：新fork-none上下文、实际GPT-6.1 Sol/Max、五个成功ImageView、无其他文件工具读取。P是仅字标/构图认可、摄影否决的校准；N是完整设计否决校准；R只看指定参考上半广告；S是正确第一图，摄影正向而文字否决；T是真人结论及旧AI判决隐藏的第三版。结果AI_FAIL，判后与已保存真人否决核对，一份检验样本结论一致，未推算准确率。

三个优先问题：先恢复S摄影，随后解决硬色板与空横条造成的图文割裂，再统一茶作整组笔画语言。审稿确认T的叶形确实已进入笔画，是有限改进，仍不足以证明整张好设计。T摄影不同源于历史使用R4，不是本轮重新生成或改写S；本轮没有新增正式版本。

审稿中保存了S的具体摄影成功关系：暖茶汤与暗绿环境、可区分的杯/木/茶材质、虚前景—清主体—远溪流、可容纳文字的暗背景。它们是可见关系，不是已经验证的生成配方；这张图的完整实际生成输入和无字源仍待恢复。

审核后已实际继续源文件恢复：通过Opera Neon展开原聊天44m21s执行摘要、读取R1真实回执并检查第一图PNG元数据。旧回执记载两个生成式编辑越界，DISCARDED_NOT_SAVED_NOT_REVIEWED；界面没有完整工具输入，原件没有文本生成元数据。不能把这两次调用与e7af9c9e逐一绑定，也不能认定R1的“文字清除”真的产出了摄影不变的无字层。限定追查结果在 `SOURCE_RECOVERY_FOLLOWTHROUGH.json`，当前缺口精确保留。

重新审核：按适配 skill 建新的匿名像素包与中性brief，目标作品每次修改必须新审。复用 `scripts/vpd_collect_agent_review.py --help`；新增 `--supplemental-source` 只用于五图补充审核，原四图正式协议与旧结论保留。初次研究代理因GPT-6.1 Sol容量不足失败，研究用实际GPT-6 Sol/Max完成；像素审稿成功使用GPT-6.1 Sol/Max。

独立性证据、真实回复、读取范围、输入SHA、模型与时间均在该证据目录。提示副本不能解密绑定spawn消息，这是现有边界；同文件系统子代理也不冒称原项目外目录审核。AI通过只允许进入交付审核，真人接受仍另行记录。

收益：分工与实际像素审核调用已验证，发现了具体问题；时间节省未测量，新skill相对旧审核的因果收益未验证，视觉收益未验证，当前作品已被真人否定。不能用安装/测试数量或审核通过流程证明审美提升。
