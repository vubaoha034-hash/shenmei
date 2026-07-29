# 国内餐饮品牌案例系统 — 强制入口

版本：`3.0.0`
状态：`MANDATORY`

本系统用于生产面向中国餐饮市场的高质量品牌案例。核心目标不是生成十张好看的 AI 图片，而是建立一个有商业逻辑、专属品牌发动机、真实视觉素材、可编辑 Figma 排版、审美闸门和连续作品集叙事的品牌系统。

## 1. 最高优先级流程

任何新品牌、每日方案、三页验证或十页项目，必须首先读取：

1. `restaurant_design_system/FIGMA_FIRST_NO_ADOBE_PIPELINE_V1.md`；
2. `restaurant_design_system/GLOBAL_FEEDBACK_RULES_V1.md`；
3. `restaurant_design_system/PHASED_DELIVERY_RULES_V1.md`；
4. `restaurant_design_system/PORTFOLIO_PRESENTATION_RULES_V1.md`；
5. `restaurant_design_system/BRAND_CREATIVE_DIRECTOR_RULES_V2.md`；
6. `restaurant_design_system/DOMESTIC_RESTAURANT_DIRECTION_LIBRARY_V1.md`；
7. `restaurant_design_system/STYLE_PERSONA_MATRIX_V1.md`；
8. `restaurant_design_system/OUTPUT_STRUCTURE_10_IMAGES_V2.md`；
9. `restaurant_design_system/DAILY_WORKFLOW_V2.md`；
10. `restaurant_design_system/config/domestic-restaurant-directions.v1.json`；
11. `generation/RESTAURANT_POSTER_IMAGE_RULES_V1.md`，仅用于产品真实感与单张海报规则；
12. `calibration/README.md` 与 `calibration/anchors.json`。

并按顺序执行以下 Skill：

1. `skills/restaurant-brand-concept-director/SKILL.md`；
2. `skills/restaurant-image-material-director/SKILL.md`；
3. `skills/restaurant-brand-portfolio-layout/SKILL.md`；
4. `skills/restaurant-brand-aesthetic-gate/SKILL.md`；
5. `skills/personal-aesthetic-critic/SKILL.md`。

未读取 Figma-First 总控文件，禁止生成任何品牌页面。

## 2. 工具分工

### 品牌概念

由品牌概念 Skill 完成：近期审计、候选方向、品牌设计发动机、策略卡、视觉 DNA 和三页验证 brief。

### 图像生成

`image_gen` 只允许生成无文字素材：

- 菜品；
- 食材；
- 工艺；
- 材料；
- 空白包装概念；
- 空间氛围概念；
- 插画或图形草案。

禁止直接生成完整品牌页面、中文 Logo、十页作品集、菜单、价格和大段文字。

### Figma

Figma 必须负责：

- 真实中文排版；
- Logo/字标方向；
- 变量与组件；
- 三页概念验证；
- 十页作品集；
- 节点 ID 与导出尺寸记录。

无 Figma 文件 URL 和页面节点 ID，不得标记 `CONCEPT_SET`。

### Adobe

Adobe 不是依赖，也不是前置条件。Adobe 授权或服务失败不得阻塞本流程。

## 3. 强制阶段

### A. 近期审计

读取最近 7 个项目，至少比较：

- 品类；
- 品牌人格；
- 主风格；
- 主色；
- 字体气质；
- 图形母题；
- 摄影；
- 包装；
- 门头与空间；
- 作品集页面骨架。

新方案至少更换 4 项，且主风格、主色或人格至少更换 2 项。

### B. 品牌设计发动机

推荐方向必须形成：

`产品事实 + 经营规则 + 品牌观点 + 视觉机制`

只有名称、口号、产品轮廓和统一颜色的方案不合格。

### C. 无文字素材

先建立 `ASSET_PLAN.md`，再逐张生成和审计。含伪文字、错误产品结构、塑料食物、假蒸汽、错误包装或空间透视的素材直接淘汰。

### D. 三页 Figma 验证

完整十页前只做：

1. 品牌概念与主视觉；
2. 店名字标与超级符号；
3. 最强应用触点。

必须使用真实文字和至少两种版式原型。

### E. 三页审美闸门

三页必须通过：

- `poster_design` 技术总分不低于 78；
- 信息层级、字体、网格、图像质量和品牌一致性均不低于 70；
- 与正向参考更接近，而不是与失败锚点更接近；
- 无致命 AI 或品牌逻辑问题；
- Figma 节点记录完整。

失败时停止，不得扩展十页。

### F. 十页 Figma 扩展

只有状态为 `THREE_PAGE_PROOF_PASS` 才能建立十页故事板并扩展。

十页必须：

- 十个独立 Figma Frame；
- 十个独立导出文件；
- 至少四种版式原型；
- 每页一个章节和一个核心结论；
- 共享真实字体、颜色、间距和组件；
- 每页存在有效 `brand_evidence`。

## 4. 标准十页

1. 品牌概念与主视觉；
2. 店名海报 / Logo / 字标 / 超级符号；
3. 视觉 DNA：色彩、材质、图形与插画；
4. 招牌产品与产品视觉系统；
5. 快餐打包盒与包装系统；
6. 品牌主题海报与墙面海报系列；
7. 食材来源 / 工艺 / 地域 / 品牌故事；
8. 门头与空间应用；
9. 菜单、员工服与运营触点；
10. 品牌视觉总览与收尾。

## 5. 强制禁止

- image_gen 直接生成完整品牌页面；
- image_gen 一次生成三联页、九宫格或十页总拼贴；
- 三页失败后为了数量继续十页；
- 用伪中文或 AI Logo 代替真实排版；
- 把生成完成等同于质量通过；
- 要求用户自己完成 Figma 排版；
- 使用虚构日期、二维码、电话、地址和无意义英文伪造专业感；
- 复制参考品牌的名称、Logo、字体、页面壳、署名、水印和商业外观；
- 用同一个版式连续复制十页；
- 将 `CONCEPT TEST`、`THREE_PAGE_PROOF` 或 AI 整页冒充 `CONCEPT_SET`。

## 6. 项目文件

每个项目至少保存：

```text
BRIEF.md
RECENT_AUDIT.md
DIRECTION_OPTIONS.md
CONCEPT_ENGINE.md
BRAND_STRATEGY.md
VISUAL_DNA.md
ASSET_PLAN.md
ASSET_MANIFEST.json
THREE_PAGE_PROOF.md
FIGMA_MANIFEST.json
TEN_PAGE_STORYBOARD.md
AESTHETIC_EVALUATION.json
PROJECT_RECORD.json
delivery_manifest.json
feedback.md
```

## 7. 状态

- `PLANNED`；
- `CONCEPT_ENGINE_PASS`；
- `ASSET_READY`；
- `THREE_PAGE_PROOF`；
- `THREE_PAGE_PROOF_PASS`；
- `THREE_PAGE_PROOF_REJECTED`；
- `TEN_PAGE_LAYOUT`；
- `CONCEPT_SET`；
- `DESIGN_DEVELOPMENT`；
- `READY_TO_POST_SET`；
- `PRODUCTION_READY`；
- `BLOCKED_FIGMA_ACCESS`；
- `REJECTED_AI_FULL_PAGE`；
- `REJECTED_WEAK_ENGINE`。

`CONCEPT_SET` 仅在十页 Figma 页面、十页导出和全部审计通过后使用。
