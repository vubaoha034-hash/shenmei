# 国内餐饮品牌 Figma-First 无 Adobe 全流程 V1.0

版本：`1.0.0`
状态：`MANDATORY`
优先级：`HIGHEST`
适用任务：每日餐饮品牌方案、手动新品牌、三页概念验证、十页品牌作品集、设计深化

## 1. 核心结论

本流程不依赖 Adobe。Adobe 不得作为任务开始、继续或完成的硬依赖。

标准工具分工：

1. **品牌概念**：文本推理与 `restaurant-brand-concept-director`；
2. **视觉素材**：`image_gen` 仅生成无文字菜品、食材、工艺、材料、包装空白模型和空间氛围素材；
3. **审美闸门**：`personal-aesthetic-critic` 与 `restaurant-brand-aesthetic-gate`；
4. **真实排版**：Figma `create_new_file`、`use_figma`、`upload_assets`、`download_assets`；
5. **记录与审计**：GitHub 项目文件、评分记录和交付清单。

最高原则：

> 图像模型不得直接承担品牌策略、中文 Logo、完整页面排版、十页一致性和最终文字。它只负责提供经过审计的视觉素材。

## 2. 强制工具边界

### 2.1 image_gen 可以做

- 无文字招牌产品摄影；
- 无文字食材与工艺摄影；
- 无文字空间氛围概念；
- 无文字包装空白模型或材质方向；
- 无文字产品局部、切面、动作与光影探索；
- 单独图形或插画概念草案。

### 2.2 image_gen 禁止做

- 直接生成完整品牌提案页；
- 直接生成十页作品集；
- 直接生成中文 Logo、价格、菜单或大段说明；
- 一张图同时生成页码、标题、正文、Mockup、门头、包装和空间；
- 用一张三联图、九宫格或总拼贴代替独立页面；
- 把 AI 生成文字当作真实排版；
- 把图像模型生成的完整页面标记为 `CONCEPT_SET`。

出现以上任一情况，图片状态必须是：

`REJECTED_AI_FULL_PAGE`

### 2.3 Figma 必须做

- 新建项目设计文件；
- 真实中文品牌名、页码、章节名、主文案和说明文字；
- Logo/字标方向的可编辑构造；
- 色彩、字体、间距、线条和圆角变量；
- 统一页面组件；
- 三页验证与十页作品集排版；
- 图片放置、裁切和章节级构图；
- 单页 PNG 导出；
- 记录真实 Figma 文件 URL、节点 ID 和导出尺寸。

若没有 Figma 文件 URL 和每页节点 ID，整套不得标记为 `CONCEPT_SET`。

## 3. 总流程与闸门

### Gate 0：输入与近期审计

开始前必须：

- 读取本文件及 `restaurant_design_system/START_HERE.md` 的全部强制文件；
- 读取最近 7 个项目；
- 列出最近母风格、品类、人格、主色、字体、母题、摄影、包装、空间和页面骨架；
- 明确本次至少 4 项变化；
- 主风格、主色或品牌人格至少变化 2 项；
- 列出至少 2 个必须避开的近期模板。

未完成则状态为 `BLOCKED_RECENT_AUDIT`。

### Gate 1：六个内部候选、三个对外方向

内部至少形成 6 个组合：

`品类 × 客群 × 价格带 × 品牌人格 × 产品事实 × 经营规则 × 品牌观点 × 视觉机制`

向用户输出至少 3 个方向并推荐 1 个。

禁止用“新鲜、手工、好吃、温暖、高级、年轻”单独构成品牌核心。

### Gate 2：品牌设计发动机

推荐方向必须形成四元组：

1. `product_fact`：可观察的产品事实；
2. `operating_rule`：真实或可执行的经营规则；
3. `brand_point_of_view`：品牌对该品类的具体观点；
4. `visual_mechanism`：能进入字体、图形、包装、菜单、空间和服务的视觉机制。

必须回答：

- 为什么该机制只能属于这个品牌；
- 它能生成哪些运营触点；
- 除去 Logo 后如何识别；
- 是否能支撑至少 8 个不同应用；
- 是否只是产品外形的直接描摹；
- 是否落入圆圈、红章、毛笔、三图标等通用模板。

失败则状态为 `REJECTED_WEAK_ENGINE`，不得生成素材。

### Gate 3：先建素材计划，不生成页面

建立 `ASSET_PLAN.md`，逐项写明：

- asset_id；
- 页面用途；
- 画面主体；
- 机位、光线、背景和材质；
- 必须保留的负空间；
- 禁止出现的文字和物体；
- 产品结构检查项；
- 对应 brand_evidence。

素材必须独立生成，不得把三页或十页合成在一次图像生成调用中。

### Gate 4：无文字素材生成与审计

每个核心素材必须检查：

- 产品数量、结构、形状、切面；
- 食材分布和容器接触；
- 光源、阴影、油光、汤汁和蒸汽；
- 包装结构和开启关系；
- 空间尺度、透视和入口关系；
- 是否存在复制配料、塑料感、错误手指、假烟雾或不合理高光；
- 是否包含伪文字、Logo、二维码、电话、价格或假标签。

含关键伪文字的素材直接淘汰，不允许后续“遮住继续用”。

### Gate 5：三页 Figma 概念验证

完整十页前，只制作 3 个独立 Figma 页面：

1. `01_BRAND_CONCEPT`：品牌概念与主视觉；
2. `02_WORDMARK_SYMBOL`：店名字标、Logo 与超级符号；
3. `03_HERO_APPLICATION`：主题海报、包装主应用或门头主视觉，按品牌最强触点选择。

三页必须：

- 使用真实字体；
- 使用同一色彩、字体、间距和组件变量；
- 使用至少 2 种不同版式原型；
- 每页只有一个核心结论；
- 主图信息权重 55%–75%；
- 说明文字不超过页面信息权重 15%；
- 不放虚构日期、联系方式、二维码和无意义英文；
- 不使用参考设计公司的页面壳、页脚或署名。

### Gate 6：三页审美闸门

三页完成后必须执行：

- 技术与形式盲评；
- 参考图匹配评估；
- 失败锚点距离评估；
- 品牌证据审计；
- AI 痕迹审计；
- 三页连续性审计。

最低通过条件：

- `poster_design` 技术总分不低于 78；
- 信息层级、字体、网格、图像质量、品牌一致性任一项不得低于 70；
- 不得触发伪中文、错误产品结构、模板重复、弱品牌证据等致命上限；
- 与正向参考的接近证据必须多于与失败锚点的接近证据；
- 若私人锚点不足，`personal_fit` 设为 `null`，但仍必须进行定性成对比较；
- 用户明确否定的方向不得自动通过。

失败则：

- 只修正品牌发动机、素材或三页；
- 禁止扩展十页；
- 状态为 `THREE_PAGE_PROOF_REJECTED`。

通过则状态为：

`THREE_PAGE_PROOF_PASS`

### Gate 7：十页故事板与 Figma 扩展

只有 `THREE_PAGE_PROOF_PASS` 后，才建立十页故事板并扩展到 10 页。

十页固定章节遵循 `PORTFOLIO_PRESENTATION_RULES_V1.md`。

Figma 中必须建立：

- 页面背景组件；
- 页码与章节组件；
- 品牌名与状态组件；
- 标题、正文、注释和数字文字样式；
- 颜色变量；
- 间距变量；
- 图像容器与裁切规则；
- 至少 4 种版式原型。

禁止把三页验证机械复制成十页。

### Gate 8：十页最终审计

逐页检查：

- 一个章节、一个核心结论；
- 主图、设计细节和应用证明关系；
- 真实文字；
- brand_evidence；
- 图片结构与材质；
- 无通用 Mockup 贴 Logo；
- 无伪价格和假经营数据。

整套检查：

- 同一本画册；
- 至少 4 种版式；
- 不连续重复同一骨架；
- 品牌资产一致而构图变化；
- 十个独立节点和十个独立导出文件；
- 实际尺寸已记录；
- Figma URL、节点 ID 和导出 URL/路径已记录。

全部通过后才允许标记：

`CONCEPT_SET`

## 4. 每日自动任务规则

每日自动任务的目标是高质量 `CONCEPT_SET`，但不得为了完成十页而跳过三页闸门。

自动任务必须按以下逻辑执行：

1. 完成 Gate 0–4；
2. 创建三页 Figma 验证；
3. 执行 Gate 6；
4. 通过则继续十页；
5. 不通过则停止，交付三页、失败原因和重做计划；
6. 不得用 image_gen 直接整页结果补足数量；
7. “生成完成”不等于“质量通过”。

自动任务不能访问 Figma 时：

- 状态必须为 `BLOCKED_FIGMA_ACCESS`；
- 可以交付品牌策略和无文字素材；
- 不得交付 AI 完整页面；
- 不得标记 `CONCEPT_SET`。

## 5. 项目文件契约

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

`FIGMA_MANIFEST.json` 必须包含：

- file_url；
- file_key；
- page_node_ids；
- frame_dimensions；
- fonts_used；
- variables_created；
- export_status；
- actual_export_dimensions。

## 6. 状态定义

- `PLANNED`：候选与策略初步建立；
- `CONCEPT_ENGINE_PASS`：品牌设计发动机通过；
- `ASSET_READY`：无文字核心素材通过；
- `THREE_PAGE_PROOF`：三页已排版，待审；
- `THREE_PAGE_PROOF_PASS`：三页通过，可以扩展；
- `THREE_PAGE_PROOF_REJECTED`：三页未通过，禁止扩展；
- `TEN_PAGE_LAYOUT`：十页 Figma 排版中；
- `CONCEPT_SET`：十页与全部审计通过；
- `DESIGN_DEVELOPMENT`：用户选中后深化；
- `READY_TO_POST_SET`：真实字体、实际尺寸与发布检查通过；
- `PRODUCTION_READY`：真实尺寸、刀版、菜单、材料和供应商条件齐全；
- `BLOCKED_FIGMA_ACCESS`：无法访问 Figma；
- `REJECTED_AI_FULL_PAGE`：错误使用图像模型生成完整页面；
- `REJECTED_WEAK_ENGINE`：品牌发动机不成立。

## 7. 绝对禁止

- 以 Adobe 授权失败为理由停止整个流程；
- 要求用户自己打开 Figma 排版才能继续；
- 直接用 image_gen 生成十张完整品牌页；
- 三页失败后仍扩展十页；
- 用数量代替质量；
- 用大段说明文字掩盖视觉不足；
- 用真实字体缺失作为概念阶段生成伪中文字的理由；
- 宣称未经过 Figma 和审美闸门的图片是完整新流程结果；
- 将 `CONCEPT TEST`、`THREE_PAGE_PROOF` 或图像模型整页结果冒充 `CONCEPT_SET`。
