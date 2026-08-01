# Repository instructions for Codex

版本：`4.3.0`
状态：`MANDATORY`

## 1. 每次设计任务的读取顺序

先读取：

1. `START_HERE.md`；
2. `skills/restaurant-design-growth-director/SKILL.md`；
3. `rules/CONCEPT_FIRST_DESIGN_AND_AI_GENERATION_V1.md`；
4. `rules/XIAOHONGSHU_DESIGN_CONTENT_SYSTEM_V1.md`；
5. `rules/DESIGN_GROWTH_QUALITY_GATE_V1.md`；
6. `config/restaurant-design-growth.v1.json`。

再按 `START_HERE.md` 进入完整品牌案例、单张海报、Figma、私人审美或餐饮经营路线。

不得因为旧文件仍存在，就让旧规则覆盖 V4.3。

## 2. V4.3 优先级

以下规则高于旧文件中的冲突内容：

- 先做品牌与经营 Brief，再生成图片；
- 重要参考图必须拆解视觉 DNA；
- 至少提出三个真正不同的创意方向；
- 换颜色、换字体、换样机不算新方向；
- AI 只负责无文字主视觉、场景、背景、插画、纹理和探索素材；
- 最终 Logo、中文、英文、拼音、价格、菜单、二维码和版式必须人工控制；
- 真实门店产品优先使用真实摄影；
- AI 不得发明门店无法提供的菜品、分量、配料、器皿和经营承诺；
- 入选方向必须通过门头、菜单、包装、海报和手机封面五触点延展；
- 准备发布时必须声明收藏、评论、转化或不发布；
- 生成完成不等于设计完成。

旧 V4.2 中不冲突的结构、色彩、食品、空间、包装、字标、文字密度和物料去重规则继续执行。

## 3. 完整品牌案例

读取：

- `DAILY_AUTOBRAND_SYSTEM_V4_3.md`；
- `DAILY_AUTOBRAND_SYSTEM_V4.md`；
- `rules/DAILY_CASE_10_IMAGE_STRUCTURE_V4.md`；
- `rules/BOARD_LAYOUT_PRESENTATION_RULES_V4.md`；
- `rules/BRAND_WORDMARK_AND_TYPOGRAPHY_RULES_V4.md`；
- `rules/DAILY_CASE_QUALITY_GATE_V4.md`；
- 每日任务另读 `schedules/DAILY_0900_BRAND_CASE_V4.md`。

强制结果：

```text
1 个完整餐饮品牌
→ 完整概念与视觉机制
→ 3 个真正不同的方向
→ 选择与淘汰理由
→ 5 触点延展预演
→ 真实摄影与 AI 素材计划
→ 人工完成最终字标和排版
→ 10 张独立 3:2 横版案例页
→ V4 与 V4.3 双重质量闸门
→ READY_BRAND_CASE / READY_TO_POST
```

### 完整品牌案例硬规则

1. 正好 10 张独立图片，不得用十宫格、总览合板或长图代替。
2. 默认 `3:2` 横版，推荐 `2400 × 1600 px`，PNG；用户指定尺寸时以用户要求为准。
3. 页面内不得显示 `01`、`02` 等页码、章节号和提案式编号。
4. 主 Logo 必须是可控的定制字标，不得直接套现成字体冒充。
5. 十张品牌名、字标和核心超级符号必须一致。
6. 全套仅允许 1—2 张中等文字密度页面，其余页面少字。
7. 配角物料原则上只重点展示一次；主角跨页也不得机械复用同一图片和裁切。
8. 至少使用四种版式骨架、三类背景家族和清楚的冷暖深浅节奏。
9. 暖米、奶油和黄棕纸张底不得成为默认审美答案，继续执行 V4.2 数量约束。
10. 食品、空间、包装和运营物料必须经得起结构、材质、光影和透视检查。
11. 最终中文、价格和关键承诺必须逐字核对。
12. 参考图只学习机制，不复制品牌资产与完整商业外观。
13. AI 完整页面只可作为构图参考或素材草案，不得直接成为最终页面。

## 4. 单张海报与独立视觉素材

读取：

- `skills/restaurant-poster-art-director/SKILL.md`；
- `generation/RESTAURANT_POSTER_IMAGE_RULES_V1.md`；
- `config/restaurant-poster-generation.v1.json`；
- calibration 文件。

单张海报同样执行概念、视觉 DNA、三方向、AI 边界、真实产品、五触点预演和发布目标规则。

只有用户明确要求多个独立海报备选时，才执行多风格配额。不得把该配额强加到同一品牌十张案例中。

## 5. 小红书发布

每篇内容声明一个主目标：

```text
COLLECTION  收藏型
DISCUSSION  评论型
CONVERSION  转化型
NOT_FOR_PUBLICATION  不发布
```

推荐账号结构：

```text
收藏型 50%
评论型 30%
转化型 20%
```

这是运营分配，不是平台官方算法权重。

### 收藏型

必须有明确对象、可带走内容、准确搜索词和具有保存价值的首图。

### 评论型

必须有具体判断、两份可见证据和一个窄选择题。不得使用“大家觉得怎么样”。

### 转化型

必须有真实经营问题、设计取舍、实际结果或可验证后果。原则上使用 A 或 B 级证据。

首图优先真实门头、真实菜单、前后对比、材料细节、高质量四宫格和完整案例页。标准样机和抽象品牌故事不得长期作为主力。

冲突标题不是必选项。模板钩子没有强视觉证据时直接淘汰。

## 6. Figma 路线

只有用户明确要求可编辑 Figma 文件、组件、变量、node ID 或团队协作源文件时，才读取：

- `restaurant_design_system/START_HERE.md`；
- `restaurant_design_system/FIGMA_FIRST_NO_ADOBE_PIPELINE_V1.md`；
- 对应 Skill、配置和 validator。

不得把 Figma 设为日常品牌案例或单张海报的前置条件。

## 7. 私人审美与经营路线

私人审美：读取相应 personal aesthetic Skill、rubric、penalties、schema 与 calibration。锚点不足时不得伪造个人偏好分数。

餐饮经营：读取 `restaurant_operations_system/START_HERE.md` 和 `skills/restaurant-operations-master/`。经营结论与视觉交付分别过闸门，不能互相覆盖失败。

## 8. 直接淘汰

- 伪中文、错字、乱码、假 Logo；
- 塑料食物、假热气、胶水酱汁；
- 光影、反射、透视和接触错误；
- 无理由印章、水墨、烟雾、飞溅、颗粒和假旧；
- 机械对称、元素克隆、脏灰、过度锐化；
- 通用“中式高级感”，没有品牌专属记忆；
- 三个方向只有颜色差异；
- AI 全页成图直接交付；
- 只有一张漂亮图，无法延展；
- 模板钩子替代视觉证据；
- 宽泛评论问题；
- 灵感合集冒充自己的商业案例；
- 把搜索样本或经验比例冒充平台官方算法。

## 9. 必填记录

```text
route:
content_objective:
product_fact:
consumer_scene:
business_problem:
brand_point_of_view:
core_concept:
visual_mechanism:
reference_visual_dna:
creative_directions:
selected_direction:
selection_reason:
real_photography_plan:
ai_asset_plan:
human_typesetting_plan:
extension_touchpoints:
first_image_logic:
primary_search_phrase:
evidence_level:
rejections_and_reasons:
final_status:
```

缺失关键字段，不得开始正式生成或声称完成。

## 10. 最终状态

允许：

- `CONCEPT_REVIEW`；
- `ASSET_DRAFT`；
- `LAYOUT_DRAFT`；
- `READY_FOR_QA`；
- `READY_BRAND_CASE`；
- `READY_TO_POST`；
- `REJECTED`。

任何硬门槛未通过，不得标记 READY。