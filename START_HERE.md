# START HERE — 强制执行入口

本仓库包含三套强制工作流：

1. **国内餐饮品牌案例系统**；
2. **餐饮海报图片生成与发布工作流**；
3. **私人审美评分与校准工作流**。

任何 AI、Codex 或人工执行者必须先判断任务属于哪一种；混合任务必须同时执行相关规则。

---

# A. 国内餐饮品牌案例系统

凡用户提出“设计一个新方案”“每天生成一套餐饮设计”“做一个全新国内餐饮品牌”“输出整套十张图”等任务，必须先读取：

1. `restaurant_design_system/START_HERE.md`
2. `restaurant_design_system/GLOBAL_FEEDBACK_RULES_V1.md`
3. `restaurant_design_system/PHASED_DELIVERY_RULES_V1.md`
4. `restaurant_design_system/BRAND_CREATIVE_DIRECTOR_RULES_V2.md`
5. `restaurant_design_system/DOMESTIC_RESTAURANT_DIRECTION_LIBRARY_V1.md`
6. `restaurant_design_system/STYLE_PERSONA_MATRIX_V1.md`
7. `restaurant_design_system/OUTPUT_STRUCTURE_10_IMAGES_V2.md`
8. `restaurant_design_system/DAILY_WORKFLOW_V2.md`
9. `restaurant_design_system/config/domestic-restaurant-directions.v1.json`
10. `generation/RESTAURANT_POSTER_IMAGE_RULES_V1.md`
11. `calibration/anchors.json`

## 阶段路由

- 默认每日任务与无真实客户资料的任务：`CONCEPT_SET`；
- 用户选中方案并要求精修：`DESIGN_DEVELOPMENT`；
- 获得真实门店尺寸、包装刀版、菜单数据、材料工艺和实际菜品资料：`PRODUCTION_READY`。

不得把真实矢量字标、1:20 施工图、包装厂刀版或真实菜品摄影设为每日概念方案的前置硬门槛。不得把概念效果图描述为施工图、印刷稿或生产终稿。

## 新方案概念阶段硬门槛

以下任一项缺失，不得开始十图概念生成：

- 未完成品牌策略卡；
- 未完成视觉 DNA 卡；
- 未完成店名字标方向、品牌主视觉方向、门头或墙面方向的概念级验证；
- 未读取最近五至七个项目和全局反馈；
- 未说明与最近项目至少四项明确差异；
- 品牌主张只有“新鲜、现炒、锅气、家常、用心、好吃不贵”等行业空话；
- 因“不要中式”直接改成国外餐饮品牌；
- 继续重复米白轻东方、橄榄绿木色社区、黑红金属霓虹或其他近期模板；
- 计划输出不是固定十张独立任务图；
- 产品、文字、空间、包装或应用仍有明显 AI 结构错误。

概念阶段允许：

- 可进一步矢量化的字标方向；
- 明确但尚未建立正式 Figma 文件的版式网格；
- 无实测尺寸的门头立面概念；
- 尚未取得真实刀版的合理包装概念；
- 通过结构和材质审计的 AI 产品概念视觉。

## 核心原则

- 任务是设计一个品牌，而不是生成十张好看图片；
- 十张图必须成为同一品牌的十个证据；
- 每张图都必须记录除 Logo 外的 `brand_evidence`；
- 参考图只学习策略、视觉语法、材料和空间统一方法，不复制表面风格；
- 同一母风格只能低频间隔使用，不能连续或习惯性延续；
- 执行者必须主动提供方向、判断、审计与改进建议，不得只等用户纠错。

## 固定输出

每套固定十张：

1. 品牌主视觉海报；
2. 店名海报 / Logo / 字标；
3. 品牌主题海报；
4. 招牌产品海报；
5. 墙面海报系列；
6. 门头 / 店名空间应用；
7. 快餐打包盒；
8. 纸袋与餐具包装系统；
9. 菜单 / 桌面运营触点；
10. 品牌视觉总览。

每日完成十张概念图并通过审计后，状态为 `CONCEPT_SET`。低于 4K 的概念预览必须披露实际尺寸，但不因未达到正式 4K 而阻止概念阶段完成。

---

# B. 餐饮海报图片生成强制入口

凡涉及生成、设计、修改、批量生产、放大、排版、交付或发布餐饮海报，必须读取：

1. `skills/restaurant-poster-art-director/SKILL.md`
2. `generation/RESTAURANT_POSTER_IMAGE_RULES_V1.md`
3. `config/restaurant-poster-generation.v1.json`
4. `calibration/README.md`
5. `calibration/anchors.json`

## 图片状态边界

- `CONCEPT` / `CONCEPT_SET`：方向和概念探索，允许未完成正式字体、矢量和 4K；
- `DRAFT`：已进入深化但尚未通过正式审计；
- `READY_TO_POST`：单图产品、设计、文字、实际 4K 和 100% 放大检查全部通过；
- `READY_TO_POST_SET`：十张全部达到发布级标准；
- `PRODUCTION_READY`：真实尺寸、刀版、菜单数据、材料和供应商要求全部满足；
- `REJECTED`：产品真实感、结构、品牌逻辑或设计逻辑失败。

## READY_TO_POST 硬门槛

以下任一条件不满足，不得标记为 `READY_TO_POST`：

- 产品没有参与设计逻辑，只是贴进模板；
- 产品、配料、器皿、烟雾或水存在明显 AI 结构错误；
- 中文标题、Logo、价格或关键信息仍是 AI 伪文字；
- 水、烟、火或产品状态缺乏物理逻辑；
- 使用重复模板，仅更换颜色或角度；
- 实际文件未达到目标 4K 像素；
- 未完成 100% 放大检查；
- 存在塑料感、蜡质感、过度 HDR、假油光或复制配料。

---

# C. 私人审美评分强制入口

正式评分前必须读取：

1. `skills/personal-aesthetic-critic/SKILL.md`
2. `config/rubric.v1.json`
3. `config/penalties.v1.json`
4. `schemas/evaluation.schema.json`
5. `calibration/README.md`

## 正式评分硬门槛

以下任一条件不满足，只能标记 `DRAFT` 或 `NO_SCORE`：

- 没有明确作品类别；
- 没有逐项画面证据；
- 没有两轮独立评分；
- 两轮总分差大于 4 分但没有仲裁；
- 任一维度分差大于 10 分但没有仲裁；
- 使用未登记扣分项；
- 没有有效同类别锚点却评分 `personal_fit`；
- 最终 JSON 未通过 `scripts/validate_evaluation.py`；
- 图片质量不足却输出精确分数；
- 没有参考图却评价参考吻合度。

保存评分 JSON 后运行：

```bash
python scripts/validate_evaluation.py evaluation.json
```

只有输出 `PASS` 才能交付 `OFFICIAL` 评分。