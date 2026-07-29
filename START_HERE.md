# START HERE — 强制执行入口

本仓库包含四套严格工作流：

1. 国内餐饮品牌案例系统；
2. 餐饮海报图片生成与发布；
3. 私人审美评分与校准；
4. 餐饮经营、单店模型、试点和多店复制。

任何执行者先判断任务路由；混合任务同时执行相关规则。

## A. 餐饮品牌案例

读取 `restaurant_design_system/START_HERE.md` 及其规定的全局反馈、分阶段交付、作品集呈现、创意总监、方向库、十页结构、每日工作流、海报规则、配置与锚点。

品牌案例任务的强制原则：

- 任务是一个品牌系统，不是十张无关图片；
- 每日默认状态为 `CONCEPT_SET`；
- 十张必须是十张独立的品牌作品集提案页面，不是十张孤立广告；
- 每页只讲一个章节，但可展示同章节的主图、细节和应用；
- 十页必须共享原创页码、页眉或页脚、安全边距、字体层级和图片规则；
- 一套至少使用四种版式原型；
- 禁止一张总拼贴替代十页；
- 禁止复制参考案例的公司署名、水印、二维码、电话、地址和页面壳；
- 参考图只学习策略、视觉语法、作品集章节和材料空间统一方法。

状态边界为 `CONCEPT_SET`、`DESIGN_DEVELOPMENT` 和 `PRODUCTION_READY`。不得把概念图描述为生产终稿。

## B. 餐饮海报

读取 `skills/restaurant-poster-art-director/SKILL.md`、`generation/RESTAURANT_POSTER_IMAGE_RULES_V1.md`、`config/restaurant-poster-generation.v1.json` 和校准文件。`READY_TO_POST` 仍要求产品、结构、文字、实际 4K 和 100% 检查通过。

## C. 私人审美评分

读取 `skills/personal-aesthetic-critic/SKILL.md`、rubric、penalties、schema 和 calibration。两轮独立评分、必要仲裁和 validator PASS 后才可 `OFFICIAL`。

## D. 餐饮经营总控

凡涉及菜单、价格、活动、会员、供应商、厨房流程、排班、损耗、食品安全、门店经营、试点或多店推广，必须读取：

1. `restaurant_operations_system/START_HERE.md`
2. `skills/restaurant-operations-master/SKILL.md`
3. `skills/restaurant-operations-master/workflows/RESTAURANT_OPERATIONS_PIPELINE_V1.md`
4. `skills/restaurant-operations-master/config/restaurant-operations-gates.v1.json`
5. 当前阶段模块与真实经营数据

经营系统核心：基线 → 单店经济 → 菜单/产能 → 顾客价值 → 供应与食安 → 六席独立审查 → 小试点 → 分批推广 → 因果复盘。

没有真实基线只能诊断；食品安全、负贡献或高峰不可执行是 `BLOCKER`；没有试点 PASS 不得 `ROLLOUT_READY`。

## 混合任务

例如会员活动海报：先通过经营契约、经济、顾客和试点设计，再通过海报视觉、文字和 4K 闸门。漂亮设计不能覆盖亏损或执行风险；盈利方案不能覆盖虚假文字、食安或品牌问题。

## 隐私

本仓库为 public 时，不上传真实门店逐笔流水、员工个人信息、供应合同、私人照片、账号或其他敏感经营数据。只提交脱敏模板和聚合证据。