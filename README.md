# shenmei｜餐饮品牌设计、AI 图片生成与小红书内容系统

当前主版本：`4.3.0`

## 核心变化

V4.3 不再把“生成一张看似高级的 AI 图”当成设计完成。

默认流程改为：

```text
产品与经营问题
→ 品牌概念
→ 参考图视觉 DNA
→ 三个真正不同的创意方向
→ 五触点延展预演
→ AI 生成无文字素材
→ 人工完成字标、中文、价格和版式
→ 设计质量闸门
→ 小红书收藏 / 评论 / 转化发布闸门
```

## 唯一入口

```text
START_HERE.md
```

## 设计总控 Skill

```text
skills/restaurant-design-growth-director/SKILL.md
```

任何餐饮品牌设计、海报、AI 图片生成或小红书设计内容任务，先读取该 Skill。

## V4.3 强制规则

```text
rules/CONCEPT_FIRST_DESIGN_AND_AI_GENERATION_V1.md
rules/XIAOHONGSHU_DESIGN_CONTENT_SYSTEM_V1.md
rules/DESIGN_GROWTH_QUALITY_GATE_V1.md
config/restaurant-design-growth.v1.json
```

## 完整品牌案例

```text
DAILY_AUTOBRAND_SYSTEM_V4_3.md
DAILY_AUTOBRAND_SYSTEM_V4.md
rules/DAILY_CASE_10_IMAGE_STRUCTURE_V4.md
rules/BOARD_LAYOUT_PRESENTATION_RULES_V4.md
rules/BRAND_WORDMARK_AND_TYPOGRAPHY_RULES_V4.md
rules/DAILY_CASE_QUALITY_GATE_V4.md
schedules/DAILY_0900_BRAND_CASE_V4.md
```

旧 V4 文件继续提供十张结构、色彩人格、反默认暖色、字标、食品、空间、包装和物料去重规则；V4.3 覆盖旧文件中允许 AI 直接承担最终中文和完整最终页面的部分。

默认完整案例交付：

```text
1 个完整餐饮品牌
10 张独立图片
3:2 横版
推荐 2400 × 1600 px
PNG
```

用户指定尺寸时，以用户要求为准。

## 单张餐饮海报与视觉素材

```text
skills/restaurant-poster-art-director/SKILL.md
generation/RESTAURANT_POSTER_IMAGE_RULES_V1.md
config/restaurant-poster-generation.v1.json
```

单张海报也必须先做概念、视觉 DNA、三方向、AI 边界、真实产品和延展测试。

## 小红书内容目标

每篇内容必须声明一个主目标：

```text
COLLECTION  收藏型
DISCUSSION  评论型
CONVERSION  转化型
NOT_FOR_PUBLICATION  不发布
```

推荐账号结构：

```text
收藏型 50%
评论型 30%
转化型 20%
```

这是运营分配，不是平台官方算法权重。

- 收藏型：靠可带走的设计证据与搜索价值；
- 评论型：靠具体判断、两份证据和窄问题；
- 转化型：靠真实经营问题、设计取舍和商业结果。

冲突标题不是必选项。标准样机和抽象品牌故事不得长期作为主力。

## AI 边界

AI 可以生成无文字主视觉、背景、场景、插画、纹理和探索素材。

最终 Logo、中文、英文、拼音、价格、菜单、二维码、尺寸和版式必须人工控制。AI 全页成图只能是 `ASSET_DRAFT`，不能直接标记为最终设计。

## 其他路线

### 可编辑 Figma 正式品牌系统

仅在用户明确要求可编辑 Figma 文件、组件、变量或 node ID 时使用：

```text
restaurant_design_system/START_HERE.md
restaurant_design_system/FIGMA_FIRST_NO_ADOBE_PIPELINE_V1.md
```

### 私人审美评分

```text
skills/personal-aesthetic-critic/SKILL.md
skills/restaurant-brand-aesthetic-gate/SKILL.md
```

### 餐饮经营系统

```text
restaurant_operations_system/START_HERE.md
skills/restaurant-operations-master/SKILL.md
```

餐饮经营与视觉交付分开审查。漂亮设计不能覆盖亏损、食品安全或执行问题；经营逻辑也不能覆盖错字、产品错误、空间错误和弱品牌逻辑。

## 隐私

仓库公开时只保存框架、脱敏模板和聚合证据，不上传真实流水、员工信息、合同、供应价格、账号或私人校准照片。