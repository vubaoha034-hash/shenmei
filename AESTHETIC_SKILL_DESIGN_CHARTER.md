# AESTHETIC SKILL DESIGN CHARTER

版本：`1.1.0`
状态：`MANDATORY`

## 0. 适用范围

凡涉及以下任一任务，必须先读取本文件：

- 新建视觉 / 审美 / 海报 / 品牌 / 图片生成 Skill；
- 修改现有视觉 Skill；
- 从一个成熟视觉 Skill 派生新 Skill；
- 为图像生成增加 Prompt Compiler、Variation Engine、Color Engine、Quality Gate 或审美规则；
- 因“结果不好看”准备继续增加视觉规则、阈值、分类或失败码；
- 用户明确点名某个 Skill 并要求直接使用 / 生成。

本文件约束的是**如何设计和执行审美 Skill**，不是某一种具体视觉风格。

用户明确点名 Skill 时，同时必须读取：

`rules/DIRECT_SKILL_INVOCATION_RULE.md`

---

## 1. 第一原则：审美 Skill 首先是 Prompt Compiler

视觉 Skill 的核心职责是：

> 把用户意图压缩成少量、具体、可成像、真正会变成像素的高杠杆变量。

默认目标不是写一篇“风格说明书”，而是生成一段清晰、决定性、可成像的 Prompt。

长期原则：

> **Prefer a concrete, imageable prompt over a long style essay.**

最终 Prompt 中优先保留：

- canvas / ratio；
- attention geometry；
- main image anchor；
- anchor material treatment；
- typography behavior；
- one clear color logic；
- reproduction texture；
- emotional temperature；
- hard avoids。

不要默认塞入：

- 长篇审美解释；
- 执行过程；
- checklist 原文；
- 失败码；
- 分析字段；
- README / source path / metadata；
- 为了“显得专业”而增加的术语。

---

## 2. 高杠杆变量原则：先找 5—8 个，再停止

设计一个视觉 Skill 时，先回答：

**真正决定这套视觉气质的 5—8 个变量是什么？**

例如可能是：

- 留白比例；
- 主体尺度；
- 主体位置；
- 单一色彩锚点；
- 字体尺度与行为；
- 纸张 / 印刷材质；
- 一个稳定的反向约束；
- 一个变化轴。

当核心变量已经足够决定视觉身份时，默认停止加规则。

**可以写 100 条，不代表应该写 100 条。**

---

## 3. 稳定骨架与可变表达必须分开

优秀视觉 Skill 通常包含两层：

### Stable Grammar｜稳定骨架

决定“这是同一种视觉语言”的少量规则，例如：

- 留白；
- 主体尺度；
- 色彩数量；
- 字体气质；
- 材料 / 印刷语言；
- 商业感 / 3D / 模板感等反向约束。

### Variation Axes｜可变表达

决定“每次不是同一个模板”的变量，例如：

- layout；
- image anchor；
- typography mode；
- texture mode；
- mood；
- accent hue。

规则：

- 稳定骨架应少而强；
- 变化轴应给模型真实选择空间；
- 不得把 variation 写成一堆强制模板家族，然后要求模型机械选一个。

---

## 4. 先判断：这是 Correctness Problem 还是 Taste Problem

视觉系统中的问题分两类。

### Correctness Problem｜适合硬锁

例如：

- 错字；
- 品牌名错误；
- 假坐标 / 假日期 / 假电话；
- 产品结构错误；
- 人物身份漂移；
- 比例不符合用户明确要求；
- 多图被错误混成一张。

这类问题可以使用：

- validator；
- schema；
- blocker；
- 明确阈值；
- failure code。

### Taste Problem｜禁止用工程验证替代审美

例如：

- 构图是否高级；
- 留白是否舒服；
- 画面是否有呼吸；
- 意象是否有诗意；
- 是否模板化；
- 是否“土”；
- 是否真正有艺术张力。

这类问题不能通过不断增加阈值、失败码和 checklist 自动变好。

**工程验证保证“不能错”；它不能证明“很好看”。**

---

## 5. 成熟上游 Skill 默认采用 Thin Wrapper

如果一个成熟 Skill 已经被证明视觉结果优秀，派生时默认策略是：

> **Upstream 100% + thin wrapper**

优先只修改真正必要的接口差异，例如：

- aspect ratio；
- 输入素材类型；
- 用户明确提供的事实文字；
- 批量交付方式。

在修改成熟上游 Skill 前必须回答：

> **我是在适配它，还是已经在重新设计它？**

如果已经开始改变：

- Prompt Compiler；
- Variation Engine；
- Color Engine；
- Typography System；
- Texture System；
- Quality Gate；
- 主构图逻辑；

则默认应**新建实验 Skill**，而不是继续污染稳定 Skill。

对 vendored / mirrored upstream，能做 SHA 校验时应保留原版镜像并验证一致性。

---

## 6. 不要因为失败就自动加规则

视觉结果失败后，按以下顺序诊断：

1. 是否真正执行了原 Skill 的 Prompt Compiler？
2. 最终 Prompt 是否具体、可成像？
3. 是否把大量解释性语言塞进了 Prompt？
4. 是否错误地把调用名 / 风格昵称当成视觉词？
5. 是否给模型留下了足够的 composition / anchor / texture 自由度？
6. 是否把 correctness 规则误用于 taste 问题？
7. 是否已有规则互相竞争，迫使模型选择安全平庸解？

只有确认缺少一个真正高杠杆视觉变量后，才新增规则。

### Stop Rule

如果出现以下趋势：

> 规则越来越多，输出越来越安全、越来越僵、越来越模板化

默认动作是：

> **删规则 / 回退到更简单版本，而不是继续补规则。**

---

## 7. 视觉数字必须直接对应“眼睛看到的结果”

可以使用数字，但数字应描述视觉结果，例如：

- 70%—90% 留白；
- 主视觉簇占 8%—25%；
- 一个高饱和色占画布约 1%—3%；
- 字体明显弱于主视觉。

谨慎使用只描述管理流程的视觉阈值，例如：

- 为了通过 validator 而设定的任意照片占比；
- “至少完成两种转译”之类过程计数；
- 并不直接改善视觉结果的结构检查。

问自己：

> **这个数字改变的是画面，还是只改变了检查表？**

---

## 8. 反向约束优先定义“不要成为什么”

与其堆叠：

- 高级；
- 艺术；
- 专业；
- 有设计感；
- 有电影感；

更有效的是清楚排除：

- commercial ad；
- generic template；
- glossy mockup；
- dense scrapbook；
- stock-photo realism；
- 3D / neon / cyberpunk；
- long clean body copy；
- too many colors / stickers / objects。

反向约束应少而明确，不应变成另一个长规则系统。

---

## 9. 参考图的作用：学习机制，不复制资产

参考图应优先帮助识别：

- attention geometry；
- 主体与留白关系；
- 视觉簇尺度；
- 抽象程度；
- 色彩锚点；
- 印刷 / 材料机制；
- 字体行为；
- 稳定骨架与变化轴。

不要机械复制：

- 品牌名；
- 水印；
- 账号；
- 精确装饰文字；
- 完整商业外观；
- 无事实依据的 metadata。

如果已有优秀成熟 Skill 可以实现相同视觉机制，优先复用其生成逻辑，而不是把参考图重新解释成几十条本地规则。

---

## 10. Prompt 长度不是专业度

设计视觉 Skill 时必须区分：

### Skill 文档可以相对完整
用于说明系统和变化轴。

### 最终图像 Prompt 必须压缩
只保留会影响最终像素的内容。

默认推荐结构：

1. canvas + attention geometry；
2. image anchor + treatment；
3. typography + accent color + print defects；
4. flat-scan / material mood + hard avoids。

最终 Prompt 如果变成“风格论文”，应主动压缩。

---

## 11. 反例：Over-engineered Aesthetic Skill

已验证失败模式：

1. 一个成熟原版 Skill 简洁有效；
2. 派生后不断加入视觉家族、阈值、验证、失败码、字段表；
3. validator 越来越严格；
4. 模型为同时满足所有规则，选择最安全的公共解；
5. 输出变成“所有规则都对，但很土”的模板。

典型症状：

- 每张都像同一种模板；
- 装饰元素越来越可预测；
- 抽象能力下降；
- 图像不敢做大胆取舍；
- 结果很“完整”，但没有张力。

修复策略：

> 回到成熟原版，恢复生成自由度，只保留必要适配。

---

## 12. 新建 / 修改审美 Skill 的强制自问

在提交审美 Skill 改动前，回答：

```text
1. 这个 Skill 的 5—8 个高杠杆视觉变量是什么？
2. 哪些是 stable grammar，哪些是 variation axes？
3. 我加的是 correctness rule 还是 taste rule？
4. 这个新增规则是否真的会改变像素结果？
5. 最终 Prompt 能否保持具体、可成像、紧凑？
6. 是否存在成熟上游 Skill，可以 thin-wrapper 而不是重写？
7. 我是不是因为一次失败就在堆规则？
8. 删除一半规则，视觉身份是否仍然成立？如果成立，应优先删除。
```

缺少这些判断，不得把“规则更多”解释为“Skill 更成熟”。

---

## 13. 与业务硬规则的关系

本 Charter 不削弱事实正确性、安全、品牌一致性、文字正确性等硬约束。

优先级：

1. 用户明确要求；
2. 事实 / 安全 / 身份 / 品牌 correctness；
3. 本 Charter 的审美 Skill 设计原则；
4. 具体视觉 Skill 的风格规则。

当业务 validator 与视觉创造发生冲突时：

- correctness 问题继续硬锁；
- taste 问题不得伪装成 correctness blocker。

---

## 14. 核心记忆

以后设计任何审美 Skill，优先记住四句话：

> **少而准，比多而全重要。**
>
> **工程验证能防错，不能制造审美。**
>
> **成熟优秀 Skill，默认 thin wrapper，不要重写。**
>
> **规则越多结果越僵时，先删规则。**

---

## 15. 用户点名 Skill 时：执行优先于再设计

当用户明确说“直接用 Skill”“使用这个 Skill”“按 `$skill-name` 生成”时，执行纪律高于助手的自由发挥。

必须：

1. 读取并执行用户点名的 Skill；
2. 若 Skill 有 Prompt Compiler，最终 Prompt 必须由该 Compiler 产生；
3. 只填写 Skill 允许的变量 / 适配，不得另写一套艺术指导取代它；
4. 用户没有要求改 Skill 时，不得擅自改 Skill；
5. 输出不满意时，先查执行链，不先改审美规则；
6. 不得自动退回“我重新给你写一个 Prompt”的模式。

完整执行规则见：

`rules/DIRECT_SKILL_INVOCATION_RULE.md`

核心原则：

> **用户点名 Skill = 执行 Skill，不是借 Skill 名义自由发挥。**
