# VPD 主渲染器路线纠正｜ChatGPT Images 优先

日期：2026-09-21
状态：ACTIVE_CORRECTION
用户纠正：项目已经具备 ChatGPT Images 作为强主渲染器，不应因为学习外部成熟风格迁移方法，就自动转向自建 SDXL/RunPod。

## 1. 纠正结论

当前 VPD 的主渲染器固定为 **ChatGPT Images**。

InstantStyle、IP-Adapter、StyleAligned、LoRA、ControlNet 等外部成熟方案当前角色改为：
- 学习成熟的参考图条件化逻辑；
- 学习风格/内容解耦、结构控制、少样本组织、评测和失败处理；
- 为 ChatGPT Images 工作流提供方法论参考；
- 必要时作为未来独立对照，不自动成为执行基础设施。

它们不是当前替换 ChatGPT Images 的默认路线。

## 2. 为什么纠正

外部方案的价值是解释“成熟团队怎么做”，不是证明“我们必须自己跑一个图像模型”。

此前 RunPod + SDXL + IP-Adapter 选择存在路线错误：
1. 增加新的模型、GPU、依赖、版本、费用与运维变量；
2. 没有先证明 ChatGPT Images 在当前目标上能力不足；
3. 会把项目重新带入基础设施建设，而不是视觉学习本身；
4. 与用户已经获得过较好 ChatGPT Images 结果的事实不一致；
5. 无法保证外部基座在绝对画质上优于当前主渲染器。

因此 RunPod 环境卡保留为研究/备选证据，不删除，但从当前主线退出。

## 3. 成熟方法如何转译到 ChatGPT Images

### 3.1 图像优先，不把参考图压缩成纯文字
成熟参考条件方法说明图像特征本身包含文字提示难以完整表达的信息。

在 ChatGPT Images 中对应：
- 真实参考图直接作为视觉输入；
- Prompt Capsule 只描述高杠杆机制和任务变化；
- 不用几十条文字规则重建参考图的全部视觉信息。

### 3.2 风格与内容分离
InstantStyle 的核心启示是减少 content leakage。

在 ChatGPT Images 中对应：
- 参考图负责风格/关系锚定；
- 新任务明确声明新的主体、过程、环境；
- 显式禁止参考图中的品牌身份、主体、文案和表面符号被复制；
- 评价时单独检查“风格迁移”和“内容泄漏”。

### 3.3 编辑优先于重新生成
已通过资产需要局部修复时：
- 优先使用 image edit / referenced-image edit；
- 不把已经通过的整张图重新总结成提示词再生成；
- 母版永不覆盖，候选作为 sibling。

### 3.4 结构变化单独测试
不要同时改风格、主体、画幅、字标和摄影。

每轮只打开一个主要变量：
- 内容变化；
- 画幅变化；
- 摄影修复；
- 字形/版式。

### 3.5 同一主渲染器做 A/B
最重要的比较优先保持同一个 ChatGPT Images renderer：
- A：参考图 + 简单任务说明；
- B：同一参考图 + 同一任务 + VPD distilled mechanism controls。

这样才能回答“我们的蒸馏有没有额外价值”，而不是比较两个不同基础模型。

## 4. 文字与生产层

ChatGPT Images 负责主视觉/视觉方向。
Figma 继续负责：
- 精确中文；
- 可编辑字标；
- 辅助信息；
- 网格、字距、光学对齐；
- 正式生产导出。

不要求图像模型一次同时解决所有精确文字生产问题。

## 5. RunPod / SDXL 状态

以下文件保留，不删除：
- evidence/vpd/mature_workflow_audit_v1/INSTANTSTYLE_IPADAPTER_REPRODUCIBILITY_CARD_20260921.md
- evidence/vpd/mature_workflow_audit_v1/RUNPOD_SECURE_A40_ENVIRONMENT_CARD_20260921.md

它们改分类为：
**RESEARCH_EVIDENCE / OPTIONAL_FUTURE_EXTERNAL_BASELINE / NOT_CURRENT_EXECUTION_ROUTE**

禁止：
- 因为环境卡已经写好就继续创建 Pod；
- 继续修 validator 只为了 RunPod；
- 启动任何付费 GPU；
- 将 SDXL 设为默认生产渲染器。

## 6. 当前新的唯一下一步

在不生成图片的情况下，完成：
**“成熟方案控制逻辑 → ChatGPT Images 原生工作流映射卡”**

必须明确：
- 哪些成熟机制 ChatGPT Images 已能直接实现；
- 哪些只能部分模拟；
- 哪些做不到；
- 对应的实际调用方式；
- A/B 实验怎样保持同一 renderer；
- 最多生成多少张；
- 如何避免上下文污染与多图拼板；
- 如何确保参考图绑定、单图、画幅、编辑对象与 provenance。

映射卡完成后，再决定是否恢复一个最多 4–6 张的有界 ChatGPT Images 对照实验。

## 7. 不变边界

不取消或重做：
- 用户认可的蘑菇系列；
- 山野集批准参考；
- 茶作 Concept 02 与已通过字标/整体设计；
- Style Capsule V1.1 Candidate；
- H1-H4 冻结输入与历史结算；
- Attempt 4 准备成果；
- Figma relay 与已验证生产工具；
- Visual Master Freeze Guard。

本次只纠正“外部模型成为当前执行主线”的错误，不清零此前任何有效成果。
