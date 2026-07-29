# 每日国内餐饮品牌方案工作流 V3.0

版本：`3.0.0`
状态：`MANDATORY`

## 1. 每日目标

每日目标仍是一个全新的中国餐饮品牌 `CONCEPT_SET`，但必须通过“品牌发动机 → 无文字素材 → 三页 Figma 验证 → 审美闸门 → 十页 Figma 扩展”的完整流程。

不得为了每天凑齐十张而跳过质量闸门。三页未通过时，当日应停止并交付失败原因与重做方案，而不是继续生产低质量十页。

Adobe 不参与强制流程。

## 2. 强制读取

每日任务必须完整读取：

1. `restaurant_design_system/START_HERE.md`；
2. `restaurant_design_system/FIGMA_FIRST_NO_ADOBE_PIPELINE_V1.md`；
3. `restaurant_design_system/GLOBAL_FEEDBACK_RULES_V1.md`；
4. `restaurant_design_system/PHASED_DELIVERY_RULES_V1.md`；
5. `restaurant_design_system/PORTFOLIO_PRESENTATION_RULES_V1.md`；
6. `restaurant_design_system/BRAND_CREATIVE_DIRECTOR_RULES_V2.md`；
7. `restaurant_design_system/DOMESTIC_RESTAURANT_DIRECTION_LIBRARY_V1.md`；
8. `restaurant_design_system/STYLE_PERSONA_MATRIX_V1.md`；
9. `restaurant_design_system/OUTPUT_STRUCTURE_10_IMAGES_V2.md`；
10. `calibration/README.md` 与 `calibration/anchors.json`；
11. 四个专用 Skill 与 `personal-aesthetic-critic`。

任何一项缺失，状态为 `BLOCKED_RULES_NOT_READ`。

## 3. Step 1：读取最近 7 个项目

必须检查：

- 品类；
- 品牌名；
- 品牌人格；
- 主张；
- 主风格与辅助风格；
- 主色和明暗关系；
- 字体气质；
- 图形母题；
- 摄影方式；
- 包装结构；
- 门头和空间结构；
- 页面骨架和版式原型；
- 用户喜欢、一般和拒绝的方向；
- AI 味与失败原因。

必须输出：

- 最近母风格列表；
- 至少两个本次禁用模板；
- 至少四项明确变化；
- 主风格、主色或人格中至少两项变化；
- 为什么不是旧模板改名版。

## 4. Step 2：候选方向

内部形成至少 6 个候选：

`品类 + 客群 + 价格带 + 产品事实 + 经营规则 + 品牌观点 + 视觉机制 + 作品集叙事`

对用户输出至少 3 个方向，说明优劣并推荐 1 个。

评估维度：

- 近期差异；
- 品牌发动机专属性；
- 国内商业真实性；
- 视觉延展能力；
- 运营触点能力；
- 食品与空间素材潜力；
- 参考图级作品集潜力；
- 去 AI 味可执行性。

## 5. Step 3：品牌设计发动机

推荐方向必须形成：

```text
product_fact
operating_rule
brand_point_of_view
visual_mechanism
```

并完成独占性测试：

- 改名后是否还能给任何竞品使用；
- 是否只是直接描摹产品外形；
- 是否依赖圆圈、毛笔、印章、三图标等通用符号；
- 是否能进入至少 8 个触点；
- 是否形成顾客可见的经营动作；
- 除 Logo 外能否识别。

失败：`REJECTED_WEAK_ENGINE`。

通过：`CONCEPT_ENGINE_PASS`。

## 6. Step 4：策略卡与视觉 DNA

必须完成：

- 中文品牌名；
- 辅助英文名；
- 品类和核心产品；
- 客群和价格带；
- 消费场景；
- 具体主张；
- 品牌故事；
- 经营差异；
- Logo/字标逻辑；
- 字体规则；
- 色彩系统；
- 图形母题；
- 摄影规则；
- 材料规则；
- 品牌口吻；
- 禁止模板。

## 7. Step 5：素材计划

在任何图像生成前写 `ASSET_PLAN.md`。

每个素材必须记录：

- asset_id；
- 用途；
- 对应页面；
- 主体；
- 机位与裁切；
- 光线；
- 背景和材料；
- 负空间；
- 禁止文字；
- 产品结构检查项；
- brand_evidence；
- reject_conditions。

## 8. Step 6：只生成无文字素材

使用 `restaurant-image-material-director`。

允许：

- 菜品、食材、工艺；
- 材料；
- 空白包装结构；
- 空白空间概念；
- 插画与图形草案。

禁止：

- 完整页面；
- 中文 Logo；
- 标题、菜单、价格；
- 三联页、九宫格和总拼贴；
- 页面页码、页脚和状态。

任何 AI 完整页面标记 `REJECTED_AI_FULL_PAGE`。

素材通过结构、材质、文字和透视审计后，状态为 `ASSET_READY`。

## 9. Step 7：创建 Figma 文件

使用 `restaurant-brand-portfolio-layout`。

没有文件时：

1. 调用 Figma `whoami`；
2. 选择可用 plan；
3. 调用 `create_new_file`，类型为 `design`；
4. 创建 tokens、proof、portfolio、export、archive 页面；
5. 记录 URL 和 file_key。

无法访问 Figma 时：

- 状态 `BLOCKED_FIGMA_ACCESS`；
- 只交付策略和无文字素材；
- 禁止用 image_gen 整页替代；
- 禁止标记 `CONCEPT_SET`。

## 10. Step 8：三页 Figma 验证

先制作：

1. 品牌概念与主视觉；
2. 店名字标与超级符号；
3. 最强应用触点。

硬规则：

- 真实可编辑中文；
- 同一变量和组件系统；
- 至少两种版式；
- 一页一个核心结论；
- 主图权重 55%–75%；
- 说明文字权重不超过 15%；
- 不放假日期、假电话、假二维码和无意义英文；
- 不复制参考图页面壳；
- 记录三个 Frame node_id。

状态：`THREE_PAGE_PROOF`。

## 11. Step 9：三页审美闸门

使用 `restaurant-brand-aesthetic-gate` 与 `personal-aesthetic-critic`。

最低通过条件：

- 技术总分 ≥ 78；
- 信息层级、字体、网格、图像质量、品牌一致性均 ≥ 70；
- 无致命 AI、文字或品牌逻辑问题；
- 正向参考接近证据多于失败锚点接近证据；
- 品牌发动机在三页中均可见；
- Figma manifest 完整。

失败：

`THREE_PAGE_PROOF_REJECTED`

必须停止十页扩展。

通过：

`THREE_PAGE_PROOF_PASS`

## 12. Step 10：十页故事板与扩展

只有三页通过后才执行。

固定章节：

1. 品牌概念与主视觉；
2. 店名 / Logo / 字标 / 超级符号；
3. 视觉 DNA；
4. 招牌产品；
5. 包装系统；
6. 主题海报与墙面海报；
7. 食材 / 工艺 / 地域 / 故事；
8. 门头与空间；
9. 菜单、员工服与运营触点；
10. 品牌视觉总览。

每页故事板记录：

- chapter；
- page_goal；
- single_conclusion；
- hero_visual；
- supporting_details；
- application_proof；
- brand_evidence；
- layout_archetype；
- asset_ids；
- real_text_fields。

十页至少使用 4 种版式原型，同一版式不得连续超过 2 页。

## 13. Step 11：十页 Figma 排版

必须：

- 十个独立 Frame；
- 真实文字；
- 共享颜色、字体、间距和组件；
- 不拉伸图片；
- 不用文字遮盖 AI 缺陷；
- 每页一个章节；
- 每页有可验证 brand_evidence；
- 不用通用 Mockup 贴 Logo 作为设计证明。

状态：`TEN_PAGE_LAYOUT`。

## 14. Step 12：最终审计

执行：

1. 反重复审计；
2. AI 痕迹审计；
3. 品牌证据审计；
4. 作品集呈现审计；
5. Figma 真实排版审计；
6. 审美评分与锚点对比；
7. 实际尺寸和导出审计。

通过条件：

- 十页全部可读；
- 无 `REJECTED` 页面；
- 平均分 ≥ 80；
- 关键页 01、02、04、05、08、10 均 ≥ 75；
- 十个 node_id 和导出记录齐全；
- 至少四种版式；
- 所有 brand_evidence 有效；
- 没有 AI 完整页面。

全部通过才标记：`CONCEPT_SET`。

## 15. 每日最终交付

通过时输出：

- 三个候选方向；
- 推荐理由；
- 近期反重复审计；
- 品牌发动机；
- 策略卡；
- 视觉 DNA；
- 素材清单；
- 三页审美结果；
- 十页故事板；
- 十张独立导出；
- Figma URL 和节点记录；
- 每页 brand_evidence；
- 全部审计；
- 实际尺寸；
- 未完成依赖和风险。

三页失败时输出：

- 三页验证图；
- 失败评分；
- 更接近哪些失败锚点；
- 精确修改顺序；
- 下一轮重做计划；
- 明确说明未扩展十页。

## 16. 不得声称

- 无 Figma 文件时不得声称完整流程完成；
- 无真实文字时不得声称正式排版完成；
- 无审美闸门时不得声称达到参考图水平；
- 无十页导出时不得声称 `CONCEPT_SET`；
- Adobe 不可用不得作为失败理由。
