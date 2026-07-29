# Repository instructions for Codex

版本：`4.0.0`
状态：`MANDATORY`

先读取根 `START_HERE.md`，再按任务类型选择路线。不得因为旧文件仍存在，就让旧 Figma-first 规则覆盖 V4 每日品牌案例。

## 1. 每日或单次完整品牌案例｜默认主路线

凡涉及以下任一需求，必须执行 V4：

- 每天 09:00 自动生成品牌案例；
- 系统自主确定餐饮品牌；
- 一套十张品牌设计案例；
- 参考案例图的多模块整版呈现；
- 空间、门头、品牌字标、海报、包装和应用的完整展示；
- 用户明确说不用 Figma。

必须读取：

- `DAILY_AUTOBRAND_SYSTEM_V4.md`；
- `rules/DAILY_CASE_10_IMAGE_STRUCTURE_V4.md`；
- `rules/BOARD_LAYOUT_PRESENTATION_RULES_V4.md`；
- `rules/BRAND_WORDMARK_AND_TYPOGRAPHY_RULES_V4.md`；
- `rules/DAILY_CASE_QUALITY_GATE_V4.md`；
- 每日任务读取 `schedules/DAILY_0900_BRAND_CASE_V4.md`。

### 强制行为

1. 读取最近 7 个有效项目的轻量记录；
2. 自主确定一个有差异的餐饮品类和品牌；
3. 建立 `产品事实 + 消费场景 + 品牌观点 + 视觉机制`；
4. 主 Logo 必须进行定制字形设计，不能直接套现成字体；
5. 建立固定十页内容清单；
6. 每页生成一张独立的完整案例展示图；
7. 每页允许 2—6 个有秩序的模块；
8. 十张共同覆盖空间、门头、字标、超级符号、故事、产品、食材、海报、包装、运营触点和总结；
9. 逐张检查中文、品牌名、字标一致性、空间、食品、包装与物料结构；
10. 只有 10 个独立文件全部通过，才使用 `READY`。

### 绝对禁止

- 以一张十页合板、十宫格、长图或总览图代替 10 张独立图片；
- 要求用户自行拼版；
- 将 Figma 设为依赖、前置条件或验收条件；
- 因没有 Figma URL、file_key 或 node_id 阻塞任务；
- 直接使用黑体、宋体、圆体、书法体或其他现成字体冒充最终 Logo；
- 十张中的品牌名字形发生漂移；
- 用错字、乱码、无意义英文、假电话、假二维码、假地址或假奖项制造专业感；
- 复制参考案例的品牌名、字标、超级符号、水印、设计公司页脚或完整商业外观；
- 只生成单素材而没有整版案例展示；
- 十页复制同一版式模板。

### 默认输出

- 数量：10 张独立图片；
- 比例：统一 `4:5`；
- 推荐像素：`2160 × 2700 px`；
- 格式：PNG；
- 用户指定尺寸时，以用户要求为准。

## 2. Figma 专项路线｜仅明确要求时使用

只有用户明确要求可编辑 Figma 文件、组件库、变量、node ID 或设计团队协作源文件时，才读取：

- `restaurant_design_system/START_HERE.md`；
- `restaurant_design_system/FIGMA_FIRST_NO_ADOBE_PIPELINE_V1.md`；
- 该路线指定的 Skill、配置与 validator。

旧 Figma validator 仅约束 Figma 专项路线，不约束 V4 每日品牌案例。

## 3. 单张餐饮海报与视觉素材

读取 `skills/restaurant-poster-art-director/SKILL.md`、`generation/RESTAURANT_POSTER_IMAGE_RULES_V1.md` 和相关配置。

独立海报多风格配额只适用于独立备选，不得强加到同一品牌十页中。

## 4. 私人审美

正式评分读取：

- `skills/personal-aesthetic-critic/SKILL.md`；
- 品牌正式量化时读取 `skills/restaurant-brand-aesthetic-gate/SKILL.md`；
- rubric、penalties、schema 和 calibration。

快速视觉诊断不必生成正式 JSON。不得伪造个人偏好分数。

## 5. 餐饮经营

读取 `restaurant_operations_system/START_HERE.md` 和 `skills/restaurant-operations-master/`。

- 收入不能替代贡献毛利；
- 食品安全 `BLOCKER` 不能被评分覆盖；
- 总部方案必须通过普通员工和高峰压力测试；
- 没有预注册试点不得全店推广；
- public 仓库不得提交敏感经营信息。

## 6. V4 最终检查

每日或单次完整品牌案例在交付前必须确认：

```text
[ ] 正好10张独立图片
[ ] 不是一张总览合板
[ ] 第03页存在定制字标系统
[ ] 十张品牌名和字标完全一致
[ ] 十页功能完整
[ ] 中文和拼音可读
[ ] 食品、空间、包装和物料无明显结构错误
[ ] 至少四种版式骨架
[ ] 没有复制参考项目的水印、署名或商业外观
[ ] 最终状态为READY
```

任何一项未通过，不得声称任务完成。