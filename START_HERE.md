# START HERE — 强制执行入口

本仓库包含四套严格工作流：

1. 国内餐饮品牌案例系统；
2. 餐饮海报图片生成与发布；
3. 私人审美评分与校准；
4. 餐饮经营、单店模型、试点和多店复制。

任何执行者先判断任务路由；混合任务同时执行相关规则。

## A. 餐饮品牌案例

读取 `restaurant_design_system/START_HERE.md` 及其规定的策略、分阶段交付、创意总监、方向库、十图结构、反馈、海报规则、配置与锚点。状态边界仍为CONCEPT_SET、DESIGN_DEVELOPMENT和PRODUCTION_READY。任务是一个品牌系统，不是十张无关图片；参考只学习策略和视觉语法。

## B. 餐饮海报

读取 `skills/restaurant-poster-art-director/SKILL.md`、`generation/RESTAURANT_POSTER_IMAGE_RULES_V1.md`、`config/restaurant-poster-generation.v1.json`和校准文件。READY_TO_POST仍要求产品/结构/文字/实际4K/100%检查通过。

## C. 私人审美评分

读取 `skills/personal-aesthetic-critic/SKILL.md`、rubric、penalties、schema和calibration。两轮独立评分、必要仲裁和validator PASS后才可OFFICIAL。

## D. 餐饮经营总控

凡涉及菜单、价格、活动、会员、供应商、厨房流程、排班、损耗、食品安全、门店经营、试点或多店推广，必须读取：

1. `restaurant_operations_system/START_HERE.md`
2. `skills/restaurant-operations-master/SKILL.md`
3. `skills/restaurant-operations-master/workflows/RESTAURANT_OPERATIONS_PIPELINE_V1.md`
4. `skills/restaurant-operations-master/config/restaurant-operations-gates.v1.json`
5. 当前阶段模块与真实经营数据

经营系统核心：基线→单店经济→菜单/产能→顾客价值→供应与食安→六席独立审查→小试点→分批推广→因果复盘。

没有真实基线只能诊断；食品安全、负贡献或高峰不可执行是BLOCKER；没有试点PASS不得ROLLOUT_READY。

## 混合任务

例如会员活动海报：先通过经营契约、经济、顾客和试点设计，再通过海报视觉/文字/4K闸门。漂亮设计不能覆盖亏损或执行风险；盈利方案不能覆盖虚假文字、食安或品牌问题。

## 隐私

本仓库为public时，不上传真实门店逐笔流水、员工个人信息、供应合同、私人照片、账号或其他敏感经营数据。只提交脱敏模板和聚合证据。