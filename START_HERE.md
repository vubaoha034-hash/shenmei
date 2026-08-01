# START HERE — 强制执行入口

版本：`4.3.0`
状态：`MANDATORY`

## 1. 最高优先级规则

任何设计任务先读取：

1. `skills/restaurant-design-growth-director/SKILL.md`；
2. `rules/CONCEPT_FIRST_DESIGN_AND_AI_GENERATION_V1.md`；
3. `rules/XIAOHONGSHU_DESIGN_CONTENT_SYSTEM_V1.md`；
4. `rules/DESIGN_GROWTH_QUALITY_GATE_V1.md`；
5. `config/restaurant-design-growth.v1.json`。

然后按任务类型读取对应路线。

V4.3 的优先级高于旧文件中与其冲突的内容。尤其是：

- AI 不再允许直接承担最终中文、Logo、价格、二维码和完整最终版式；
- 生成完成不等于设计完成；
- 正式设计必须先有概念、视觉机制、三个不同方向和多触点延展；
- 小红书发布必须声明收藏、评论或转化目标。

旧 V4.2 中不冲突的十张结构、反默认暖色、字标、空间、食品、包装、文字密度和物料去重规则继续有效。

## 2. 路由

当前仓库包含五条路线：

1. 每日或单次完整餐饮品牌案例；
2. 单张餐饮海报与独立视觉素材；
3. 明确要求可编辑 Figma 源文件的正式品牌系统；
4. 私人审美评分与校准；
5. 餐饮经营总控。

同一任务涉及多条路线时，分别通过相关硬门槛。根入口优先于旧子目录入口。

## A. 每日或单次完整餐饮品牌案例｜V4.3 主流程

适用：

- 每天 09:00 自动生成品牌案例；
- 系统自主确定品牌与品类；
- 一套十张独立品牌案例；
- 空间、门头、定制字标、故事、产品、海报、包装和运营触点的完整展示；
- 小红书品牌设计案例；
- 用户要求参考案例图采用多模块整版呈现；
- 用户明确说不用 Figma。

必须读取：

1. `DAILY_AUTOBRAND_SYSTEM_V4_3.md`；
2. `DAILY_AUTOBRAND_SYSTEM_V4.md`；
3. `rules/DAILY_CASE_10_IMAGE_STRUCTURE_V4.md`；
4. `rules/BOARD_LAYOUT_PRESENTATION_RULES_V4.md`；
5. `rules/BRAND_WORDMARK_AND_TYPOGRAPHY_RULES_V4.md`；
6. `rules/DAILY_CASE_QUALITY_GATE_V4.md`；
7. 每日任务另读 `schedules/DAILY_0900_BRAND_CASE_V4.md`。

强制流程：

```text
最近项目审计
→ 产品与经营 Brief
→ 参考图视觉 DNA
→ 至少三个真正不同的创意方向
→ 选择并说明淘汰理由
→ 门头、菜单、包装、海报、手机封面延展预演
→ 真实摄影与 AI 素材计划
→ 生成无文字素材
→ 人工完成字标、中文、价格和版式
→ 十张独立案例页
→ V4 结构与真实性闸门
→ V4.3 概念、AI、延展与发布闸门
→ READY_BRAND_CASE / READY_TO_POST
```

### V4.3 最高优先级硬规则

1. 必须先建立 `产品事实 + 消费场景 + 经营问题 + 品牌观点 + 核心概念 + 视觉机制`。
2. 重要参考图必须拆解构图、色彩、光线、镜头、材质、图形、字体、留白和信息密度。
3. 至少提出三个真正不同的方向；换颜色、换字体、换样机不算新方向。
4. AI 只生成无文字主视觉、背景、场景、插画、纹理和独立素材。
5. 最终 Logo、中文、英文、拼音、价格、菜单、二维码、尺寸和版式必须人工控制。
6. 真实门店产品优先使用真实摄影；AI 不得发明门店无法提供的菜品和经营承诺。
7. 入选方向必须通过门头、菜单、包装、海报和手机封面五触点延展。
8. 十张必须是十个独立文件，不得用十宫格、长图或总览合板代替。
9. 默认单页为 `3:2` 横版，推荐 `2400 × 1600 px`，PNG；用户指定尺寸时以用户要求为准。
10. 页面内不得出现 `01`、`02` 等可见页码和提案式编号。
11. 品牌 Logo 必须是可控的定制字标，不得直接套现成字体冒充。
12. 全套仅允许 1—2 张中等文字密度页面，其余页面以图像、比例、材质和留白表达。
13. 配角物料原则上只重点展示一次；主角跨页也不得机械复用相同图片和裁切。
14. 必须先定义品牌色彩人格，再安排背景家族、色温、明度和对比。
15. 暖米色、奶油色和黄棕纸张底不得成为默认答案；数量约束继续执行 V4.2。
16. 不得复制参考案例的名称、Logo、超级符号、水印、设计公司页脚、二维码或完整商业外观。
17. 生成完成不等于质量通过；AI 全页图不得直接标记为最终设计。

### 必填设计凭证

```text
product_fact:
consumer_scene:
business_problem:
brand_point_of_view:
core_concept:
visual_mechanism:
reference_visual_dna:
creative_directions:
selected_direction:
selection_reason:
real_photography_plan:
ai_asset_plan:
human_typesetting_plan:
extension_touchpoints:
brand_color_personality:
primary_palette:
background_families:
temperature_map:
contrast_plan:
```

没有这些字段，不得开始十张正式扩展。

## B. 单张餐饮海报与独立视觉素材

适用：单张海报、产品主视觉、独立海报备选或品牌项目中的单素材。

必须读取：

1. `skills/restaurant-poster-art-director/SKILL.md`；
2. `generation/RESTAURANT_POSTER_IMAGE_RULES_V1.md`；
3. `config/restaurant-poster-generation.v1.json`；
4. calibration 文件。

独立海报同样必须执行概念、视觉 DNA、三方向、AI 边界、真实产品和发布目标规则。

只有用户明确要求多个独立备选时，才执行独立海报的多风格配额。该配额不得套用到同一品牌十张案例中。

## C. 可编辑 Figma 正式品牌系统｜仅明确请求时使用

只有用户明确要求以下内容时，才进入 Figma 专项路线：

- 可编辑 Figma 文件；
- 组件库、变量和 node ID；
- 生产级设计协作文件；
- 明确要求 Figma 页面或 Frame。

读取：

1. `restaurant_design_system/START_HERE.md`；
2. `restaurant_design_system/FIGMA_FIRST_NO_ADOBE_PIPELINE_V1.md`；
3. 该路线要求的 Skill、配置与 validator。

Figma 不得被强加给每日品牌案例、单张海报或用户明确说“不用 Figma”的任务。

## D. 私人审美评分

读取：

- `skills/personal-aesthetic-critic/SKILL.md`；
- 品牌项目需要正式量化时读取 `skills/restaurant-brand-aesthetic-gate/SKILL.md`；
- rubric、penalties、schema 与 calibration。

快速视觉判断不必伪装成正式评分。锚点不足时 `personal_fit` 必须为 `null`，未验证结果不得标记 `OFFICIAL`。

## E. 餐饮经营总控

凡涉及菜单、价格、活动、会员、供应商、厨房、前厅、排班、损耗、食安、试点或多店推广，读取：

1. `restaurant_operations_system/START_HERE.md`；
2. `skills/restaurant-operations-master/SKILL.md`；
3. 当前阶段工作流、配置、真实经营数据与当前有效法规证据。

经营结论和视觉交付分别通过独立闸门。漂亮设计不能覆盖亏损、食品安全或执行问题；经营逻辑也不能覆盖错字、产品错误、空间错误和弱品牌逻辑。

## 3. 小红书发布路由

任何准备发布的设计内容必须声明：

- `COLLECTION`：可保存的结构、方法、材料、尺寸、对比或完整拆解；
- `DISCUSSION`：具体判断、两份证据和一个窄问题；
- `CONVERSION`：真实经营问题、设计取舍和可验证结果或后果；
- `NOT_FOR_PUBLICATION`：本次不发布。

推荐内容结构：

```text
收藏型 50%
评论型 30%
转化型 20%
```

这是运营分配，不是平台官方算法权重。

首图优先真实门头、真实菜单、前后对比、材料细节、高质量四宫格和完整案例页。标准样机与抽象品牌故事不得长期作为主力。

冲突标题不是必选项。标题、首图和正文必须围绕同一搜索对象。

## 4. 直接淘汰

以下任一问题直接淘汰：

- 伪中文、错字、乱码、假 Logo；
- 塑料食物、假热气、胶水酱汁；
- 光影、反射、透视和接触错误；
- 无理由印章、水墨、烟雾、飞溅和做旧；
- 机械对称和元素克隆；
- 脏灰、过度锐化和通用滤镜；
- 只有“中式高级感”，没有品牌专属记忆；
- 三个方向只是配色变化；
- AI 完整页面直接交付；
- 只有一张漂亮图，无法延展；
- 用模板钩子替代视觉证据；
- 评论问题宽泛；
- 灵感合集冒充自己的商业案例；
- 把经验样本冒充平台官方规则。

## 5. 状态

允许状态：

- `CONCEPT_REVIEW`；
- `ASSET_DRAFT`；
- `LAYOUT_DRAFT`；
- `READY_FOR_QA`；
- `READY_BRAND_CASE`；
- `READY_TO_POST`；
- `REJECTED`。

任何硬门槛未通过，不得声称任务完成。

## 6. 隐私

仓库为 public 时，不上传逐笔流水、员工个人信息、供应合同、私人照片、账号或其他敏感数据。只提交脱敏模板、聚合证据和稳定的非敏感设计记录。