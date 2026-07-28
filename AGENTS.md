# Repository instructions for Codex

本仓库有四套路由：餐饮品牌设计、餐饮海报、私人审美评分、餐饮经营总控。先读根 `START_HERE.md`。

## 品牌/海报/审美

原有分阶段交付、十图系统、参考抽象、产品真实感、4K、两轮审美评分、校准和validator规则全部保留。不得把概念图描述为生产终稿。

## 餐饮经营

读取 `restaurant_operations_system/START_HERE.md` 和 `skills/restaurant-operations-master/`。

- 经营基线、经济、产能、顾客、供应/食安、独立面板、试点和推广是独立阶段；
- 收入不能替代贡献毛利，毛利不能替代净利润；
- 食品安全BLOCKER不能被销售或评分覆盖；
- 总部方案必须通过普通员工和高峰压力测试；
- 没有预注册试点不得全店铺开；
- 单店成功不自动升级为标准SOP；
- 不在public仓库提交逐笔经营、员工、合同或账户敏感信息。

## 混合任务

经营活动与视觉物料同时通过两套闸门。不要让视觉系统决定经营结论，也不要让经营结论跳过图片质量和真实文字。

## Checks

```text
python -m py_compile skills/restaurant-operations-master/scripts/validate_master_record.py
python skills/restaurant-operations-master/scripts/validate_master_record.py <fixture.json>
```

现有审美评分命令和图片规则继续有效。