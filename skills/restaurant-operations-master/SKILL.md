---
name: restaurant-operations-master
description: "Master orchestrator for Chinese restaurant operations and small-chain growth. It turns an operating question into evidence-locked unit economics, menu engineering, kitchen and service capacity, customer value, supplier and food-safety review, independent operating panels, bounded pilots, rollout gates and causal postmortems. It is separate from restaurant brand design and poster generation."
metadata:
  version: "1.0.0"
  scope: "restaurant_operations_multi_store_pilot_and_rollout"
---

# Restaurant Operations Master

本 Skill 服务真实餐饮经营，不是生成品牌图片。它适用于单店优化、菜单/价格、活动、会员、供应商、厨房流程、门店扩张、集中采购、区域管理和多店复制。

核心原则：先建立真实经营基线，再提出假设；先小范围试点，再扩大；结果必须同时看顾客、门店、财务、食品安全和长期品牌，不以营业额单一指标判定成功。

## 与现有系统的关系

- 餐饮品牌概念与视觉：继续走 `restaurant_design_system/`；
- 餐饮海报生成：继续走 `skills/restaurant-poster-art-director/`；
- 审美评分：继续走 `skills/personal-aesthetic-critic/`；
- 经营决策：走本 Skill。

混合任务必须分别通过相关闸门。例如促销活动既要通过经营模型，也要通过海报发布级审核。

## 总流程

```text
Phase 0  经营问题契约
Phase 1  门店/商品/时段/渠道真实基线
Phase 2  单店经济与菜单工程
Phase 3  厨房、前厅、人员和服务产能
Phase 4  顾客价值、品牌承诺和需求验证
Phase 5  供应商、食品安全和合规
Phase 6  六个独立经营面板
Phase 7  小规模试点、指标和停止规则
Phase 8  多店推广、例外管理和培训
Phase 9  因果复盘与经营知识库
```

详细读取 `workflows/RESTAURANT_OPERATIONS_PIPELINE_V1.md`。

## Phase 0：经营契约

先明确：

```text
problem:
decision_owner:
stores_in_scope:
customer_segment:
daypart:
channel:
time_window:
financial_objective:
customer_objective:
operational_guardrails:
food_safety_guardrails:
brand_guardrails:
maximum_pilot_loss:
rollout_decision_date:
```

“提高营业额”“做会员活动”“谈供应商”过于模糊。必须明确通过什么机制、在哪些门店/时段、允许牺牲什么、不能牺牲什么。

## Phase 1：真实基线

读取 `modules/BASELINE_AND_DECISION_CONTRACT.md`。统一POS、收银、采购、库存、排班、损耗、外卖、评价和人工口径；按店、日、时段、渠道、菜品拆分。缺少基线时只允许 `DIAGNOSIS_ONLY`，不能承诺收益。

## Phase 2：单店经济与菜单

读取 `modules/UNIT_ECONOMICS_AND_MENU_ENGINEERING.md`。至少计算：实际售价、食材、包装、平台/支付费、可变人工、损耗、贡献毛利、订单/顾客、客单、复购、折扣侵蚀、桌时或产能占用。菜单工程同时看受欢迎度和贡献毛利，并加入出餐复杂度、共享原料、食品安全和品牌作用。

## Phase 3：产能与服务

读取 `modules/CAPACITY_SERVICE_AND_LABOR.md`。把流程拆为点单、备菜、烹饪、称重/装盘、结账、取餐、清台、外卖打包。用峰值到达率、处理时间、在制品、瓶颈和服务等待判断方案能否执行。总部想法若高峰期无法稳定执行，直接否决或重做。

## Phase 4：顾客价值

读取 `modules/CUSTOMER_VALUE_AND_BRAND_PROMISE.md`。独立检验顾客是否理解、是否在意、是否愿意改变行为、是否只是薅补贴。活动不能只增加交易量而损害菜品、等待、信任和品牌承诺。

## Phase 5：供应与安全

读取 `modules/SUPPLIER_FOOD_SAFETY_AND_COMPLIANCE.md`。供应商决策用总成本，不只看单价：质量波动、交付、退换、账期、起订、冷链、检测、追溯、缺货和门店操作负担。食品安全是硬闸门；任何销量或毛利不能覆盖高风险缺口。

## Phase 6：独立经营面板

读取 `modules/INDEPENDENT_OPERATING_PANEL.md`。默认六席：顾客、店长/前厅、厨师长/后厨、财务、品牌/产品、食品安全/风险。每席先锁定，再汇总。总部观点不是第七票裁决全部。

## Phase 7：试点

读取 `modules/PILOT_EXPERIMENT_AND_ROLLOUT.md`。优先选1—2家有代表性且风险可控门店，预注册假设、对照/基线、主指标、护栏、周期、最大损失和停止规则。一次试点尽量只改变少数核心变量。

## Phase 8：推广

只有试点通过财务、顾客、执行和安全闸门，才进入扩店。建立SOP、培训、材料、权限、异常升级、门店例外和分批推广；不能要求所有店无条件复制。

## Phase 9：复盘

读取 `modules/MULTI_STORE_GOVERNANCE_AND_POSTMORTEM.md`。区分方案机制、执行质量、门店差异、季节/天气、竞争、外部流量和随机性。营业额上涨但贡献毛利、等待、投诉、损耗或复购恶化，不判定成功。

## 质量闸门

读取 `config/restaurant-operations-gates.v1.json`。

状态：

```text
DATA_INCOMPLETE
DIAGNOSIS_ONLY
HYPOTHESIS_READY
PILOT_READY
PILOT_RUNNING
PILOT_PASS
PILOT_FAIL
ROLLOUT_READY
ROLLOUT_RUNNING
STANDARDIZED
```

一个总分不能覆盖食品安全、单店经济或高峰执行 BLOCKER。

## 输出要求

完整经营方案必须包含：

- 契约和基线；
- 单店经济；
- 菜单/商品角色；
- 产能与服务瓶颈；
- 顾客价值；
- 供应商/食品安全；
- 六席独立报告；
- 试点设计；
- 推广/停止条件；
- 复盘和仍存在风险。

## 方法来源

读取 `references/METHODOLOGY_SOURCES.md`。法规和行业资料需按当前日期核验；本 Skill 不替代持证财务、法律或食品安全专业人员。