# 国内餐饮品牌案例系统 — 强制入口

版本：`1.0.0`
状态：`MANDATORY`

本项目用于持续生产面向中国餐饮市场的小红书品牌设计案例。目标不是长期生成单一中式审美，也不是默认把项目改造成国外餐饮品牌，而是在真实国内餐饮品类与经营语境中建立多风格、低 AI 味、可落地的设计案例库。

## 强制读取顺序

任何 AI、Codex 或人工执行者在生成新的国内餐饮品牌方案前，必须依次读取：

1. `restaurant_design_system/DOMESTIC_RESTAURANT_DIRECTION_LIBRARY_V1.md`
2. `restaurant_design_system/STYLE_PERSONA_MATRIX_V1.md`
3. `restaurant_design_system/OUTPUT_STRUCTURE_10_IMAGES_V1.md`
4. `restaurant_design_system/DAILY_WORKFLOW_V1.md`
5. `restaurant_design_system/config/domestic-restaurant-directions.v1.json`
6. `generation/RESTAURANT_POSTER_IMAGE_RULES_V1.md`
7. `calibration/anchors.json`

## 每个新项目必须先确定六项

1. 国内餐饮品类；
2. 品牌人格；
3. 主视觉风格；
4. 目标客群与价格带；
5. 产品驱动的设计母题；
6. 与最近项目的差异点。

缺少任一项，不得开始批量生成。

## 三条最高优先级硬规则

### 1. 国内餐饮语境

- 品类、消费场景、菜单结构、门店运营和顾客认知必须适合中国市场；
- 可以使用国际化、现代、编辑、潮流或工业设计语言；
- 但不得因为“不要中式”就直接变成国外餐饮品牌、国外菜单或不符合国内经营逻辑的项目；
- 除非用户明确要求，品牌中文名必须是主要识别名称。

### 2. 风格多样性

- 中式、轻东方、水墨、书法只是风格池的一部分，不是默认答案；
- 同一批或连续项目不得反复使用米白底、黑色中式字标、红印章、木色空间、烟雾水波等固定组合；
- 新项目必须与最近一次项目在品类或主风格上形成明确差异；
- “田小狗类型”指原创、亲切、人格化、IP 感的小馆品牌，不得复制现有品牌的名称、角色或商业外观。

### 3. 去除 AI 味

- 产品结构、材质、空间、包装和文字必须真实；
- 禁止伪中文、假价格、重复食材、塑料食物、错误透视、统一模板感；
- 生成图只可作为概念素材，正式标题、Logo、价格和关键文字应使用真实字体或矢量路径；
- 未达到实际 4K 像素与 100% 放大检查要求，不得标记为 `READY_TO_POST`。

## 标准输出

每个品牌方案固定输出 10 张独立图片，一张完成一个任务。不得用一张拼贴图替代十张独立设计。具体结构见：

`restaurant_design_system/OUTPUT_STRUCTURE_10_IMAGES_V1.md`

## 项目状态

- `PLANNED`：完成六项定义，尚未生成；
- `CONCEPT`：方向探索，文字或产品仍未验证；
- `DRAFT`：已成套，但存在排版、真实感或 4K 问题；
- `READY_TO_POST`：十图系统、真实感、文字和实际 4K 全部通过；
- `REJECTED`：产品、品牌逻辑、风格差异或 AI 痕迹不合格。
