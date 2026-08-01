# 每日 09:00 品牌案例任务契约 V4.3

版本：`4.3.0`
状态：`MANDATORY`
时区：`Asia/Shanghai`
执行时间：每天 `09:00`

## 1. 每次运行任务

执行一次完整的 Shenmei V4.3 每日品牌案例流程：

1. 读取最近 7 个有效项目，审计品类、品牌语义、概念、视觉机制、字标、色彩、背景、摄影和页面骨架；
2. 自主选择一个差异明确的餐饮品类与品牌方向；
3. 建立产品事实、消费场景、经营问题、品牌观点、核心概念和视觉机制；
4. 拆解重要参考图的视觉 DNA；
5. 提出至少三个真正不同的创意方向；
6. 比较方向，记录选择理由和淘汰理由；
7. 预演门头、菜单、包装、海报和手机封面五触点；
8. 制定真实摄影、AI 素材和人工排版计划；
9. AI 只生成无文字主视觉、场景、背景、插画、纹理和独立素材；
10. 使用可控工具完成最终字标、中文、英文、拼音、价格和版式；
11. 按固定十页结构完成 10 张独立品牌案例展示图；
12. 执行 V4 结构、色彩、食品、空间、包装和物料闸门；
13. 执行 V4.3 概念、AI 边界、真实性、延展和发布闸门；
14. 为小红书发布声明收藏、评论、转化或不发布；
15. 只在全部通过时标记 `READY_BRAND_CASE` 或 `READY_TO_POST`。

## 2. 必须读取

- `/START_HERE.md`
- `/skills/restaurant-design-growth-director/SKILL.md`
- `/rules/CONCEPT_FIRST_DESIGN_AND_AI_GENERATION_V1.md`
- `/rules/XIAOHONGSHU_DESIGN_CONTENT_SYSTEM_V1.md`
- `/rules/DESIGN_GROWTH_QUALITY_GATE_V1.md`
- `/config/restaurant-design-growth.v1.json`
- `/DAILY_AUTOBRAND_SYSTEM_V4_3.md`
- `/DAILY_AUTOBRAND_SYSTEM_V4.md`
- `/rules/DAILY_CASE_10_IMAGE_STRUCTURE_V4.md`
- `/rules/BOARD_LAYOUT_PRESENTATION_RULES_V4.md`
- `/rules/BRAND_WORDMARK_AND_TYPOGRAPHY_RULES_V4.md`
- `/rules/DAILY_CASE_QUALITY_GATE_V4.md`

## 3. 强制结果

- 1 个完整品牌；
- 1 份完整品牌与经营 Brief；
- 1 份参考图视觉 DNA；
- 至少 3 个真正不同的创意方向；
- 1 份方向选择与淘汰记录；
- 1 份五触点延展预演；
- 1 份真实摄影、AI 素材和人工排版责任表；
- 10 张独立图片；
- 每张是完整品牌案例展示页；
- 定制且可控的中文品牌字标；
- 空间、门头、故事、产品、食材、海报、包装、运营触点和总结全部覆盖；
- 不依赖 Figma；
- 不让用户自行拼版；
- 不把 AI 全页图直接当作最终设计。

## 4. 默认交付

```text
数量：10 张独立图片
比例：3:2 横版
推荐尺寸：2400 × 1600 px
格式：PNG
页面内无可见序列号
```

用户指定尺寸时，以用户要求为准。

## 5. 发布目标

每次运行必须声明：

- `COLLECTION`；
- `DISCUSSION`；
- `CONVERSION`；
- `NOT_FOR_PUBLICATION`。

收藏型必须提供可保存内容；评论型必须有具体判断、两份证据和窄问题；转化型必须有真实经营问题、设计取舍和可验证结果或后果。

冲突标题不是默认要求。

## 6. 失败处理

当工具额度、连接、图片生成或排版条件导致无法完成时：

- 不得把未完成结果标记为 READY；
- 明确报告已完成阶段、图片数量和失败原因；
- 保留同一品牌方向；
- 下一次优先补齐缺失步骤或页面，不得无理由重新生成新品牌；
- AI 素材完成但最终排版未完成时标记 `ASSET_DRAFT` 或 `LAYOUT_DRAFT`；
- 概念、三方向、延展或真实性闸门失败时标记 `REJECTED`。

## 7. 去重记录

每次运行至少记录：

- 日期；
- 品牌名；
- 品类；
- 产品事实；
- 经营问题；
- 核心概念；
- 视觉机制；
- 品牌人格；
- 主色与整体色温；
- 字标机制；
- 摄影逻辑；
- 主要版式骨架；
- 发布目标；
- 证据等级；
- 最终文件数量；
- 最终状态。

近 7 个有效项目不得出现明显相同的品类、品牌名语义、核心概念、视觉机制、主色、字标、摄影和页面骨架组合。

## 8. 最终状态

允许：

- `CONCEPT_REVIEW`
- `ASSET_DRAFT`
- `LAYOUT_DRAFT`
- `READY_FOR_QA`
- `READY_BRAND_CASE`
- `READY_TO_POST`
- `REJECTED`

生成完成不得自动升级为 READY。