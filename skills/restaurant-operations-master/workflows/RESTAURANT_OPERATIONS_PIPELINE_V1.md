# 餐饮经营总控流程 V1

## 读取顺序

1. 根 `START_HERE.md`；
2. `restaurant_operations_system/START_HERE.md`；
3. `skills/restaurant-operations-master/SKILL.md`；
4. gate、当前模块和模板；
5. 涉及设计/海报/审美时同时读取对应系统。

## 项目目录

```text
operations/{project_id}/
├── contract.md
├── baseline/
├── unit_economics.json
├── menu_engineering.md
├── capacity_map.md
├── customer_evidence.md
├── supplier_safety.md
├── panels/
├── pilot_plan.json
├── rollout_plan.md
└── postmortem.md
```

## Gates

- G0经营契约；
- G1数据和基线；
- G2单店经济；
- G3菜单/产能/服务；
- G4顾客价值和品牌；
- G5供应商和食品安全；
- G6独立面板；
- G7试点设计；
- G8推广治理；
- G9因果复盘和知识升级。

食品安全、负贡献或高峰不可执行是BLOCKER，不能靠销售总分覆盖。