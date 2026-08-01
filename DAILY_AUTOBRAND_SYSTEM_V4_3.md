# Shenmei V4.3｜概念优先品牌案例总控覆盖层

版本：`4.3.0`
状态：`MANDATORY`

## 1. 定位与优先级

本文件是 `DAILY_AUTOBRAND_SYSTEM_V4.md` 的 V4.3 覆盖层。

旧 V4 文件继续提供十张独立案例结构、页面角色、色彩人格、反默认暖色、文字密度、配角物料去重、字标一致性以及食品、空间、包装检查。

本文件新增并优先执行：

- 概念优先；
- 参考图视觉 DNA；
- 三个真正不同的创意方向；
- AI 只承担素材与探索；
- 最终文字、字标、价格和版式必须人工控制；
- 真实产品优先；
- 五触点延展测试；
- 小红书收藏、评论、转化目标；
- 新设计增长质量闸门。

发生冲突时，本文件及 V4.3 规则优先。

## 2. 强制读取顺序

1. `START_HERE.md`
2. `skills/restaurant-design-growth-director/SKILL.md`
3. `rules/CONCEPT_FIRST_DESIGN_AND_AI_GENERATION_V1.md`
4. `rules/XIAOHONGSHU_DESIGN_CONTENT_SYSTEM_V1.md`
5. `rules/DESIGN_GROWTH_QUALITY_GATE_V1.md`
6. `config/restaurant-design-growth.v1.json`
7. `DAILY_AUTOBRAND_SYSTEM_V4.md`
8. `rules/DAILY_CASE_10_IMAGE_STRUCTURE_V4.md`
9. `rules/BOARD_LAYOUT_PRESENTATION_RULES_V4.md`
10. `rules/BRAND_WORDMARK_AND_TYPOGRAPHY_RULES_V4.md`
11. `rules/DAILY_CASE_QUALITY_GATE_V4.md`
12. 每日任务另读 `schedules/DAILY_0900_BRAND_CASE_V4.md`

## 3. 新执行流程

```text
最近项目审计
→ 品牌与经营 Brief
→ 参考图视觉 DNA 拆解
→ 三个真正不同的创意方向
→ 方向比较与选择
→ 五触点延展预演
→ 真实摄影与 AI 素材计划
→ 生成无文字素材
→ 人工控制字标、中文、价格和版式
→ 完成十张独立案例页
→ V4 结构与真实性闸门
→ V4.3 概念、AI、延展与内容闸门
→ READY_BRAND_CASE / READY_TO_POST
```

任何步骤不得跳过。

## 4. 品牌 Brief

正式生成前必须记录：

```text
brand_name:
category:
product_fact:
consumer_scene:
business_problem:
brand_point_of_view:
core_concept:
visual_mechanism:
why_this_mechanism_belongs_to_this_brand:
brand_color_personality:
```

禁止只确定品牌名、颜色和空洞口号。

## 5. 三方向阶段

至少三个方向。每个方向必须说明概念、视觉机制、摄影、构图、字体、材质、色彩人格、五触点表现和风险。

任意两个方向必须在至少四项关键维度上不同。换颜色、换字体或换样机不算新方向。

入选方向必须说明选择理由和另外两个方向的淘汰理由。

## 6. AI 素材阶段

允许生成：

- 无文字产品图；
- 无文字场景；
- 背景；
- 插画；
- 纹理；
- 光影、镜头和构图测试；
- 独立物料素材。

AI 不得直接承担最终中文、Logo、价格、菜单、二维码和完整最终页面。

AI 输出的完整页面只能作为构图参考或 `ASSET_DRAFT`。正式稿必须重建文字、字标、层级和版式。

## 7. 真实产品计划

真实门店、真实菜品或真实价格存在时，必须优先使用真实证据。

记录：

```text
real_product_source:
real_space_source:
real_packaging_source:
verified_price_and_claims:
ai_extension_scope:
forbidden_inventions:
```

不得让 AI 发明门店无法提供的菜、配料、分量、器皿或经营承诺。

## 8. 五触点预演

十张正式展开前，先证明入选方向可以进入：

1. 门头；
2. 菜单；
3. 包装；
4. 海报；
5. 手机封面或小红书首图。

若其中三项无法成立，方向不得入选。

## 9. 十张正式制作

继续执行旧 V4 的十张结构、页面角色、色彩节奏和物料去重。

新增要求：

- 最终文字必须可控；
- 品牌字标必须来自同一可复用源文件或可控矢量结构；
- 产品页优先使用真实产品证据；
- 海报页不得展示未通过文字和价格校验的 AI 全页图；
- 总结页展示品牌机制，不重复所有样机；
- 小红书首图在小尺寸下仍能看清类别与案例价值。

## 10. 发布目标

案例完成后必须声明：

- `COLLECTION`：提供可保存的结构、方法、材料、尺寸、对比或拆解；
- `DISCUSSION`：提供具体判断、两份证据和一个窄问题；
- `CONVERSION`：提供真实经营问题、设计取舍和可验证结果或后果；
- `NOT_FOR_PUBLICATION`：本次不发布。

不允许默认使用冲突标题。

## 11. 新增执行凭证

```text
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
```

## 12. 状态

- 素材生成完成：`ASSET_DRAFT`
- 页面排版未完成最终校验：`LAYOUT_DRAFT`
- 等待最终检查：`READY_FOR_QA`
- 十张与设计闸门通过：`READY_BRAND_CASE`
- 同时通过发布闸门：`READY_TO_POST`
- 任一硬门槛失败：`REJECTED`

不得继续使用“生成完成等于 READY”的旧逻辑。