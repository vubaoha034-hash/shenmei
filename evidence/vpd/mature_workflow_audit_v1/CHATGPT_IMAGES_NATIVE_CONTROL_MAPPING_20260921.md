# 成熟视觉控制逻辑 → ChatGPT Images 原生工作流映射卡

日期：2026-09-21
项目：visual-aesthetic-vpd
状态：MAPPING_COMPLETE_NO_GENERATION_EXECUTED
主渲染器：ChatGPT Images
目的：吸收 InstantStyle / IP-Adapter / StyleAligned / ControlNet / LoRA 等成熟方案的控制思想，但不虚构 ChatGPT Images 不具备的底层参数，也不替换现有主渲染器。

## 1. 当前官方能力依据

本卡实际核对的 OpenAI 官方资料：

1. ChatGPT Images Help Center  
   https://help.openai.com/en/articles/11084440  
   - 可以创建新图并编辑已有图；
   - 可上传现有图片并描述修改；
   - 可使用选择工具进行局部编辑，也可直接描述区域修改；
   - 支持任意宽高比，并可用宽高比选择器调整；
   - 支持透明背景、文字和细节修改。

2. OpenAI Academy: Creating images with ChatGPT  
   https://openai.com/academy/image-generation/  
   - 图像提示不需要很长，通常 1–3 句清楚说明即可；
   - 支持多个上传图片作为生成/编辑参考；
   - 官方示例明确允许将“图1”作为内容/布局来源，“图2”作为风格参考，并在提示中说明角色；
   - 推荐分步骤修改，而不是一次性堆积大量改动。

3. ChatGPT Images 2.5 发布说明  
   https://openai.com/index/introducing-chatgpt-images-2-5/  
   - 改进参考照片主体保留；
   - 改进自然光、纹理；
   - 改进多轮编辑的一致性；
   - 更擅长只改指定元素而保留主体、构图和品牌处理。

4. 当前 ChatGPT 图像执行工具合同（本会话实际可用能力）
   - 可新生成或编辑当前会话中的具体图片；
   - 可明确要求 style transfer；
   - 可指定输出 size / aspect；
   - 可指定 n，正式实验固定 n=1；
   - 对已有图片的修复应优先走 edit，而不是重绘整图；
   - 图像输入由当前会话中的实际图片目标进行绑定，正式实验需用隔离聊天避免歧义。

## 2. 成熟方法逐项映射

| 成熟方法机制 | ChatGPT Images 原生对应 | 映射等级 | 当前项目用法 |
|---|---|---|---|
| IP-Adapter：参考图直接进入生成条件 | 上传/附加真实参考图参与生成 | **直接可用** | 母参考真实像素继续直接输入，不先压缩成纯文字 |
| 多参考图角色分工 | 官方支持多上传图，并可按“图1内容、图2风格”说明角色 | **直接可用** | 仅在确实需要“内容源 + 风格源”时使用；首轮家族迁移仍优先单一母参考 |
| InstantStyle：减少 content leakage | 明确参考只提供风格/关系，不复制主体、品牌、文案、表面 token | **部分映射** | 通过输入角色 + anti-copy 指令 + 独立泄漏评审实现 |
| InstantStyle：只注入 style block | ChatGPT 不暴露 transformer block 控制 | **不可直接实现** | 不伪造数值权重；用简洁角色约束近似，不宣称等价 |
| IP-Adapter scale 数值权重 | ChatGPT 产品没有公开 reference-strength 数值旋钮 | **不可直接实现** | 不编造 0.6/0.8 等强度；通过提示角色和独立 A/B 观察实际效果 |
| StyleAligned：共享注意力保持系列一致 | ChatGPT 不暴露 shared-attention 机制；Images 2.5 改进多轮/reference consistency | **部分映射** | 每张使用同一批准母参考与同一 compact mechanism capsule，不用上一张生成图串联漂移 |
| ControlNet depth / edge / pose | 没有公开可控的 depth/edge map 权重接口 | **不可直接等价** | 需要粗结构时可使用参考图/草图/编辑；不能称为 ControlNet 级约束 |
| 草图结构条件 | ChatGPT 移动端支持 Sketch → image | **直接但场景有限** | 仅在需要人为粗构图时作为开发工具；不作为首轮正式验证依赖 |
| Inpainting / 局部编辑 | 选择区域后编辑，或直接描述局部修改 | **直接可用** | 已通过母版只修失败维度；这是“局部修复优先”的主要路线 |
| Outpainting / 改画幅 | 编辑器可改 aspect ratio 并重新生成扩展画面 | **直接可用但需复核** | 画幅变化必须检查是否真正 reflow，而不是简单填边/重构失真 |
| LoRA / DreamBooth 权重个性化 | ChatGPT Images 无用户可训练视觉权重接口 | **当前不可用** | 不用 prompt 冒充 LoRA；只有未来证明参考图原生能力不足时才考虑外部 baseline |
| 固定 seed / 完全确定性 | ChatGPT Images 当前产品不提供用户可控 seed | **不可用** | 不宣称像素级复现；通过固定输入、单次输出、全部留存实现实验可审计 |
| negative prompt 独立通道 | ChatGPT Images 没有独立公开 negative-prompt 参数 | **不可用** | 将关键禁止项写进同一简洁任务说明，但不能宣称等价 |
| 精确中文字生产 | ChatGPT 可生成文字，但本项目还要求可编辑与逐字精确 | **不作为最终生产层** | 主视觉阶段尽量无最终文字；Figma 继续完成正式中文字标与排版 |

## 3. 核心架构改成三层，而不是一张 prompt 包办全部

### Layer A：真实像素锚点
输入批准参考图本身。

职责：
- 风格气质；
- 材质与光影感觉；
- 图文/主体对重关系；
- 区域密度和留白关系。

禁止：
- 把参考图全部转写成几十条 prompt，再丢掉真实像素；
- 默认复制参考图品牌名、主体、具体文案、山/茶壶/印章等 surface token。

### Layer B：Compact VPD Mechanism Capsule
只保留 5–8 个当前任务真正有用的高杠杆机制。

首轮候选最多包含：
1. 主次阅读关系；
2. title/photo counter-mass；
3. type-safe tonal space；
4. regional density；
5. truthful depth/material realism；
6. role-based color behavior；
7. semantic-role binding；
8. aspect-dependent reflow（仅画幅任务）。

不再把 VPD 当规则百科。

### Layer C：Production
当视觉方向通过后：
- ChatGPT Images 的局部 edit 负责摄影/对象局部修复；
- Figma 负责精确中文字标、辅助信息、网格、字距、光学对齐与可编辑交付。

已通过层冻结；只修失败层。

## 4. 两种生成模式必须分开

### Mode 1：新内容家族迁移
适用：从批准参考生成新的内容任务。

必须：
- 新鲜隔离聊天；
- 只放该任务允许的参考图；
- A/B 都使用同一 ChatGPT Images renderer；
- n=1；
- 相同 aspect；
- 相同主体事实；
- 相同输出阶段（均为主视觉，或均为完整视觉，不混用）；
- 不在生成前看另一组输出再调整 prompt。

### Mode 2：已通过资产局部修复
适用：茶作摄影、背景、单个物体等局部问题。

必须：
- 以实际已通过图片作为 edit source；
- 不从文字重新生成整张；
- 母版保留，候选 sibling；
- 一次只打开一个失败维度；
- 若 candidate 让已通过维度退化，直接 reject/rollback。

## 5. 首轮同一 renderer A/B 结构

目的：回答一个问题——**VPD compact mechanism controls 在“真实参考图已经直接输入”的前提下，是否仍提供额外价值。**

### A 路：Reference Native Baseline
输入：
- 同一批准参考图；
- 同一新内容任务；
- 必要 correctness 约束；
- 1–3 句自然语言；
- 不加入 VPD mechanism capsule。

### B 路：Reference + Compact VPD
输入：
- 与 A 完全同一批准参考图；
- 与 A 完全同一新内容任务；
- 与 A 完全相同 correctness 约束；
- 额外加入冻结的 5–8 个 distilled mechanism controls。

共同条件：
- renderer = ChatGPT Images；
- 每路 1 张；
- 同一 aspect；
- 禁止 hidden variants / best-of-N；
- 每路用独立 fresh chat，避免后生成一路看到前一路像素；
- 所有原始输出留存；
- 技术无输出不计审美失败，但可见错误输出计入实验结果；
- 不在 A/B 之间使用不同编辑预算。

## 6. 为什么首轮不用多参考图

OpenAI 官方支持多个参考图，但首轮不使用，原因不是能力不足，而是**实验归因**。

首轮只允许一个 canonical family reference：
- 更容易证明实际参考身份；
- 减少图1/图2角色混淆；
- 减少上下文污染；
- 能直接回答“真实母参考 + VPD 机制”是否优于“真实母参考本身”。

如果未来需要“产品真实照片 + 风格参考”，再开启双参考实验，并把两张图角色写死。

## 7. 画幅控制

ChatGPT Images 产品支持任意宽高比；正式任务必须把 aspect 当成调用级条件，不只埋在长 prompt 中。

执行时记录：
- requested_aspect；
- 实际输出 dimensions；
- orientation；
- 是否发生 editor aspect regeneration。

如果实际尺寸/方向与冻结任务不符：
- 该输出技术不合格；
- 不靠裁切/Figma 伪装成原生合格；
- 不立即隐性重试。

## 8. 如何避免 Attempt 2/3 那种上下文污染

正式每一路必须：
1. 新聊天；
2. 只读取项目规则文字，不读取任何旧生成图片；
3. 在生成前只附加当前唯一允许的 reference；
4. 不附加茶作、蘑菇、Attempt 旧图、Figma screenshot；
5. 生成后立即记录 provenance 并停止 generator chat；
6. 下一路换新聊天。

注意：
项目规则文字可以读取；**旧视觉像素不能进入 generator conversation**。

## 9. Provenance 最低字段

每张正式输出记录：
- task_id / experiment_id；
- renderer = ChatGPT Images；
- generation vs edit；
- source/reference file ID；
- reference SHA-256；
- reference count；
- exact task prompt / compiled mechanism text SHA-256；
- requested aspect / size；
- requested output count = 1；
- gen_id；
- parent_gen_id（若为 edit）；
- raw output file ID；
- raw output SHA-256；
- actual dimensions；
- generation attempt count；
- hidden variants = false；
- pre-review retry = false；
- human verdict = pending / actual wording。

没有这些字段不能进入正式对照。

## 10. 首轮预算提案

当前仍然：
- 新图片：0（映射阶段）
- 外部 GPU：0
- 训练：0
- Figma 写入：0

下一阶段只提案，不在本卡自动授权：

### Stage 1
一个新内容任务：
- A 路 1 张；
- B 路 1 张；
总计 2 张。

如果其中任何一路发生任务身份/画幅/参考绑定错误，先结算技术问题，不直接扩展第二任务。

### Stage 2
只有 Stage 1 两路均技术有效，才增加第二个新内容任务：
- A 路 1 张；
- B 路 1 张；
总计再 2 张。

**整个首轮最多 4 张新图。**

不额外生成“看看效果”的图；不先出 10 张挑最好。

## 11. 评审顺序

第一层：correctness
- 内容是否正确；
- 单图还是拼板；
- aspect；
- reference identity；
- 是否出现被禁止的源品牌/文案/主体泄漏。

第二层：匿名实际像素
- A/B 隐藏标签；
- 用户看实际图，不看方法名；
- 判断可用性和偏好。

第三层：reference-aware
- 家族关系；
- material newness；
- literal copy risk；
- surface-token dependence。

第四层：mechanism
- B 的额外控制是否真的解释可见提升；
- 如果 A 已经同样好，则 VPD 复杂度没有证明必要价值。

## 12. 停止条件

以下任一成立就停止扩大实验：
- Stage 1 任一路技术身份不成立；
- B 明显不如 A；
- A/B 接近，无法证明 VPD 新增价值；
- B 的优势只能靠更多人工修改得到；
- 输出开始复制参考品牌/主体/文案；
- 为了救结果需要不断追加规则；
- 第二任务仍不能重复第一任务的优势。

失败时保留旧成果，不修改用户已通过资产。

## 13. 当前明确做不到的事情

不能因为 ChatGPT Images 很强就虚构以下能力：
- 精确 numeric style strength；
- transformer-block injection；
- ControlNet depth/edge weight；
- LoRA weight training；
- deterministic seed；
- pixel-identical rerun。

这些如果未来成为项目必需能力，再单独论证外部工具；目前不是默认前置。

## 14. 当前结论

**ChatGPT Images 足以承担下一轮 VPD 的主渲染与局部编辑验证。**

目前没有证据要求我们为了参考图风格迁移去自建 SDXL。

成熟方案真正给我们的价值是：
- image-first；
- style/content separation；
- local-edit-first；
- isolate one variable；
- same-renderer A/B；
- compact high-leverage controls；
- explicit failure boundaries。

唯一下一步：
**冻结 Stage 1 的一个新内容任务、A/B 两路输入和匿名评审顺序；仍不生成，先完成执行包。**
