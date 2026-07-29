# shenmei｜餐饮品牌案例、海报、经营与私人审美系统

当前主版本：`4.0.0`

## 当前主流程

本仓库的默认视觉路线已经调整为：

> 每天北京时间 09:00，自主确定 1 个餐饮品牌，直接生成 10 张独立的完整品牌案例展示图。

每张图是一页多模块整版案例，不是单素材，也不是等待用户去 Figma 拼版的半成品。

十张固定覆盖：

1. 品牌总览；
2. 门头与空间；
3. 定制字标、超级符号与色彩；
4. 品牌故事；
5. 产品与食材；
6. 海报系统；
7. 包装系统；
8. 运营触点；
9. 系统组合；
10. 总结收尾。

## 最重要的硬规则

- 必须交付 10 张独立图片；
- 禁止以一张十页总览合板、十宫格或长图代替；
- 品牌 Logo 必须进行定制字形设计，不能直接套用现成字体；
- 每张图可以包含 2—6 个有秩序的展示模块；
- 不要求用户自行拼版；
- Figma 不再是每日品牌案例的依赖、前置条件或验收条件；
- 只有用户明确要求可编辑 Figma 源文件时，才进入旧 Figma 专项路线。

## 唯一入口

```text
START_HERE.md
```

## V4 核心规则

```text
DAILY_AUTOBRAND_SYSTEM_V4.md
rules/DAILY_CASE_10_IMAGE_STRUCTURE_V4.md
rules/BOARD_LAYOUT_PRESENTATION_RULES_V4.md
rules/BRAND_WORDMARK_AND_TYPOGRAPHY_RULES_V4.md
rules/DAILY_CASE_QUALITY_GATE_V4.md
schedules/DAILY_0900_BRAND_CASE_V4.md
```

## 默认尺寸

```text
2160 × 2700 px
4:5
PNG
10个独立文件
```

参考图比例不同时可以调整，但同一套十张必须统一。用户指定尺寸时，以用户要求为准。

## 其他路线

### 单张餐饮海报与视觉素材

```text
skills/restaurant-poster-art-director/SKILL.md
generation/RESTAURANT_POSTER_IMAGE_RULES_V1.md
```

### 可编辑 Figma 正式品牌系统

仅在用户明确要求可编辑 Figma 文件、组件、变量或 node ID 时使用：

```text
restaurant_design_system/START_HERE.md
restaurant_design_system/FIGMA_FIRST_NO_ADOBE_PIPELINE_V1.md
```

### 餐饮经营系统

```text
restaurant_operations_system/START_HERE.md
skills/restaurant-operations-master/SKILL.md
skills/restaurant-operations-master/workflows/RESTAURANT_OPERATIONS_PIPELINE_V1.md
skills/restaurant-operations-master/config/restaurant-operations-gates.v1.json
```

餐饮经营与视觉交付分开审查。漂亮设计不能覆盖亏损、食品安全或执行问题；经营逻辑也不能覆盖错字、产品错误、空间错误或弱品牌逻辑。

## 隐私

仓库公开时只保存框架、脱敏模板和聚合证据，不上传真实流水、员工信息、合同、供应价格、账号或私人校准照片。