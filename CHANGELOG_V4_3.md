# Shenmei V4.3 Changelog

版本：`4.3.0`
日期：`2026-08-02`

## 升级目的

V4.3 修正了此前“完成十张或生成一张看似高级的 AI 图，就等于完成设计”的错误倾向，并把餐饮设计、AI 图片生成和小红书发布统一到一套可审计流程。

## 新增

- `skills/restaurant-design-growth-director/SKILL.md`
- `rules/CONCEPT_FIRST_DESIGN_AND_AI_GENERATION_V1.md`
- `rules/XIAOHONGSHU_DESIGN_CONTENT_SYSTEM_V1.md`
- `rules/DESIGN_GROWTH_QUALITY_GATE_V1.md`
- `config/restaurant-design-growth.v1.json`
- `DAILY_AUTOBRAND_SYSTEM_V4_3.md`

## 更新

- `START_HERE.md`
- `AGENTS.md`
- `README.md`
- `skills/restaurant-poster-art-director/SKILL.md`
- `schedules/DAILY_0900_BRAND_CASE_V4.md`

## 核心规则

1. 设计先建立产品事实、消费场景、经营问题、品牌观点、核心概念和视觉机制。
2. 重要参考图必须拆解构图、色彩、光线、镜头、材质、图形、字体、留白和信息密度。
3. 正式执行前至少比较三个真正不同的创意方向。
4. 换颜色、换字体、换样机和换裁切不算新方向。
5. AI 只生成无文字主视觉、场景、背景、插画、纹理和探索素材。
6. 最终 Logo、中文、英文、拼音、价格、菜单、二维码、尺寸和版式必须人工控制。
7. 真实门店产品优先使用真实摄影，AI 不得发明门店无法提供的菜品和经营承诺。
8. 入选方向必须通过门头、菜单、包装、海报和手机封面五触点延展。
9. 小红书发布必须声明收藏、评论、转化或不发布。
10. 收藏靠可带走的设计证据，评论靠具体判断与窄问题，转化靠真实经营问题、设计取舍和结果。
11. 冲突标题不是必选项；模板钩子不能替代视觉证据。
12. 灵感合集可以增长收藏，但不得冒充自己的完整商业案例。

## 与 V4.2 的关系

V4.2 的以下内容继续保留：

- 十张独立案例结构；
- 页面角色；
- 反默认暖色；
- 品牌色彩人格；
- 文字密度；
- 配角物料去重；
- 字标一致性；
- 食品、空间、包装与运营触点真实性。

V4.3 覆盖旧文件中允许 AI 直接生成最终中文、最终 Logo 或完整最终页面的部分。

## 新失败状态

- `REJECTED_UNDECLARED_ROUTE_OR_OBJECTIVE`
- `REJECTED_WEAK_OR_GENERIC_CONCEPT`
- `REJECTED_MISSING_VISUAL_DNA`
- `REJECTED_FALSE_CREATIVE_VARIETY`
- `REJECTED_AI_FULL_PAGE_AS_FINAL`
- `REJECTED_PRODUCT_OR_BUSINESS_FALSEHOOD`
- `REJECTED_ISOLATED_PRETTY_IMAGE`
- `REJECTED_NO_SAVE_VALUE`
- `REJECTED_BROAD_OR_EMPTY_DISCUSSION`
- `REJECTED_NO_COMMERCIAL_PROOF`
- `REJECTED_GENERIC_HOOK`
- `REJECTED_EVIDENCE_MISREPRESENTATION`

## 新最终状态

- `CONCEPT_REVIEW`
- `ASSET_DRAFT`
- `LAYOUT_DRAFT`
- `READY_FOR_QA`
- `READY_BRAND_CASE`
- `READY_TO_POST`
- `REJECTED`