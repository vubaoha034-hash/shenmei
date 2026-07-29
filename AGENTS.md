# Repository instructions for Codex

本仓库有四套路由：餐饮品牌设计、餐饮海报、私人审美评分、餐饮经营总控。先读根 `START_HERE.md`。

## 餐饮品牌设计

凡涉及新餐饮品牌、每日方案或十图案例，必须完整读取 `restaurant_design_system/START_HERE.md` 指定的文件，特别包括：

- `GLOBAL_FEEDBACK_RULES_V1.md`；
- `PHASED_DELIVERY_RULES_V1.md`；
- `PORTFOLIO_PRESENTATION_RULES_V1.md`；
- `BRAND_CREATIVE_DIRECTOR_RULES_V2.md`；
- `OUTPUT_STRUCTURE_10_IMAGES_V2.md`；
- `DAILY_WORKFLOW_V2.md`。

强制行为：

- 先完成品牌策略卡、视觉 DNA、三个关键触点和十页作品集故事板；
- 十张必须是十张独立品牌提案页面，不是十张孤立广告，也不是一张总拼贴；
- 每页只讲一个章节，但可展示同章节的主图、细节和应用；
- 十页共享原创页码、页眉或页脚、安全边距、字体层级、图片和材质规则；
- 一套至少使用四种版式原型；
- 页面中的页码、章节名、项目名、主文案和状态必须使用真实字体排版；
- 禁止复制参考案例的设计公司署名、水印、二维码、电话、地址、页面壳或商业外观；
- 每页记录 `brand_evidence`；
- 完成反重复、AI 痕迹、品牌证据和作品集呈现四项审计；
- 每日默认交付 `CONCEPT_SET`，不得把概念图描述为施工、印刷或生产终稿。

## 餐饮海报与审美

原有产品真实感、文字、4K、两轮审美评分、校准和 validator 规则全部保留。

## 餐饮经营

读取 `restaurant_operations_system/START_HERE.md` 和 `skills/restaurant-operations-master/`。

- 经营基线、经济、产能、顾客、供应/食安、独立面板、试点和推广是独立阶段；
- 收入不能替代贡献毛利，毛利不能替代净利润；
- 食品安全 `BLOCKER` 不能被销售或评分覆盖；
- 总部方案必须通过普通员工和高峰压力测试；
- 没有预注册试点不得全店铺开；
- 单店成功不自动升级为标准 SOP；
- 不在 public 仓库提交逐笔经营、员工、合同或账户敏感信息。

## 混合任务

经营活动与视觉物料同时通过两套闸门。不要让视觉系统决定经营结论，也不要让经营结论跳过图片质量和真实文字。

## Checks

```text
python -m py_compile skills/restaurant-operations-master/scripts/validate_master_record.py
python skills/restaurant-operations-master/scripts/validate_master_record.py <fixture.json>
```

现有审美评分命令和图片规则继续有效。