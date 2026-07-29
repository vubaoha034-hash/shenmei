# START HERE — 强制执行入口

版本：`3.0.0`
状态：`MANDATORY`

本仓库包含四套路由：

1. 国内餐饮品牌设计；
2. 单张餐饮海报与视觉素材；
3. 私人审美评分与校准；
4. 餐饮经营总控。

任何执行者先判断任务路由。混合任务必须同时通过相关规则。

## A. 国内餐饮品牌设计

凡涉及新餐饮品牌、每日方案、三页概念验证、十页作品集、品牌包装或空间系统，必须读取：

1. `restaurant_design_system/START_HERE.md`；
2. `restaurant_design_system/FIGMA_FIRST_NO_ADOBE_PIPELINE_V1.md`；
3. 该入口指定的全部规则与校准文件；
4. 四个专用品牌 Skill；
5. `skills/personal-aesthetic-critic/SKILL.md`。

强制流程：

```text
近期7项目审计
→ 至少6个内部候选
→ 对外3个方向并推荐1个
→ 产品事实+经营规则+品牌观点+视觉机制
→ 无文字素材计划与生成
→ Figma三页验证
→ 审美闸门
→ 通过后Figma十页扩展
→ 十页审计与独立导出
```

核心边界：

- Adobe 不是依赖；
- image_gen 只生成无文字素材；
- image_gen 不得直接生成完整品牌页面；
- 真实中文、Logo方向、组件、网格和十页必须由 Figma 完成；
- 三页验证失败时禁止扩展十页；
- 没有 Figma URL、node ID 和真实文字不得标记 `CONCEPT_SET`；
- 不要求用户自己完成 Figma 排版；
- 生成完成不等于质量通过。

## B. 单张餐饮海报与视觉素材

单张海报、单个主视觉或独立海报批次读取：

1. `skills/restaurant-poster-art-director/SKILL.md`；
2. `generation/RESTAURANT_POSTER_IMAGE_RULES_V1.md`；
3. `config/restaurant-poster-generation.v1.json`；
4. calibration 文件。

独立海报的多风格配额不得应用到一个品牌的十页作品集。

`READY_TO_POST` 必须通过产品、文字、实际尺寸和 100% 检查。

## C. 私人审美评分

读取：

- `skills/personal-aesthetic-critic/SKILL.md`；
- `skills/restaurant-brand-aesthetic-gate/SKILL.md`，品牌项目适用；
- rubric、penalties、schema；
- `calibration/README.md` 与 `calibration/anchors.json`。

少于足够锚点时 `personal_fit` 必须为 `null`，但仍要做定性成对比较。未验证结果不得标记 `OFFICIAL`。

## D. 餐饮经营总控

凡涉及菜单、价格、活动、会员、供应商、厨房流程、排班、损耗、食安、试点或多店推广，读取：

1. `restaurant_operations_system/START_HERE.md`；
2. `skills/restaurant-operations-master/SKILL.md`；
3. 当前阶段工作流、配置和真实经营数据。

没有真实基线只能诊断；食品安全、负贡献或高峰不可执行是 `BLOCKER`；没有试点 PASS 不得 `ROLLOUT_READY`。

## 混合任务

经营结论和视觉交付分别通过独立闸门。漂亮设计不能覆盖亏损、食安或执行问题；经营逻辑也不能覆盖伪文字、AI产品错误和品牌弱逻辑。

## 隐私

本仓库为 public 时，不上传逐笔流水、员工个人信息、供应合同、私人照片、账号或其他敏感经营数据。只提交脱敏模板、聚合证据和稳定的非敏感设计记录。
