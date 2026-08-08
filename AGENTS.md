# Repository instructions for Codex

版本：`4.2.1`
状态：`MANDATORY`

先读取根 `START_HERE.md`，再按任务类型选择路线。不得因为旧文件仍存在，就让旧 Figma-first 规则覆盖 V4.2 每日品牌案例。

## 0. 审美 Skill 设计治理｜强制前置

任何涉及**新建、修改、派生视觉 / 审美 / 海报 / 品牌 / 图片生成 Skill** 的任务，在读取具体 Skill 之前必须先读取：

`AESTHETIC_SKILL_DESIGN_CHARTER.md`

特别是出现以下行为时必须触发：

- 修改 Prompt Compiler / Variation Engine / Color Engine / Typography / Texture / Quality Gate；
- 因“结果不好看”准备新增视觉规则、阈值、分类、validator、failure code；
- 从一个已经成熟、已有优秀结果的视觉 Skill 派生本地版本。

强制原则：

1. 审美 Skill 优先是紧凑 Prompt Compiler；
2. 先找 5—8 个高杠杆视觉变量，再停止；
3. `correctness` 可以硬锁，`taste` 不得伪装成 correctness blocker；
4. 成熟上游视觉 Skill 默认 `upstream 100% + thin wrapper`；
5. 规则越多、结果越僵时，优先删规则或回退；
6. 大幅改变成熟 Skill 的视觉机制时，应新建实验 Skill，不得继续污染稳定版本。

## 1. 每日或单次完整品牌案例｜默认主路线

凡涉及以下任一需求，必须执行 V4.2：

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
2. 避开近期重复的品类、品牌名核心字、视觉隐喻、品牌人格、主色、背景家族和整体色温；
3. 自主确定一个差异明确的品牌，形成 `产品事实 + 消费场景 + 品牌观点 + 视觉机制`；
4. 主 Logo 必须进行定制字形设计，不能直接套现成字体；
5. 先建立十张页面角色清单、文字密度表、物料出现表与色彩温度表；
6. 每页生成一张独立的完整横版案例展示图；
7. 默认比例 `3:2`，推荐 `2400 × 1600 px`，PNG；
8. 每页只设一个第一视觉中心，通常使用 1 个主模块和 0—3 个辅助模块；
9. 全套仅允许 1—2 张中等文字密度页面，其余页面必须少字；
10. 配角物料分配到唯一专属页面，完整展示后不得跨页重复作为主内容；
11. 页面内不得显示 `01`、`02`、`03` 等序列号、页码或提案式章节编号；
12. 先确定品牌色彩人格，再分配十张页面的背景家族、色温、明度与对比；
13. 暖米色、奶油色、黄棕纸张底默认不得超过 3 张；
14. 至少 4 张不得使用暖米或奶油底；至少 2 张采用冷色或中性底；至少 1 张采用深色、低明度或强对比背景。例外必须在 manifest 中说明；
15. 同一页不得让主图、背景、文字和强调色全部同时偏暖；
16. 十张共同覆盖空间、门头、字标、超级符号、故事、产品、食材、海报、包装、运营触点、产品组合和总结；
17. 逐张检查中文、品牌名、字标一致性、空间、食品、包装、物料结构、文字密度、配角重复、色温惯性与背景重复；
18. 只有 10 个独立文件全部通过，才使用 `READY`。

### 色彩策略凭证

生成前必须记录：

```text
brand_color_personality:
primary_palette:
background_families:
temperature_map:
warm_dominant_board_count:
contrast_plan:
recent_color_repetition_check:
color_exception_reason: null
```

若缺失上述字段，禁止开始十张正式生成。

### 色彩和背景执行政策

- 不得默认使用暖米色、奶油色或黄棕色纸张底；
- 不得把“温暖、自然、手作”自动翻译为整套暖黄光和暖米底；
- 色彩必须来自品牌事实、品类、消费时间、空间材料和品牌人格；
- 十张至少使用三类背景家族；
- 冷白、灰白、雾蓝灰、浅灰绿、矿物灰、深灰、炭黑、品牌色实底均为常规选项；
- 暖色可以使用，但只能是有理由的局部节奏；
- 最近两套若均为暖调，下一套优先采用冷、中性或深色主导；
- 不得只通过降低饱和度，把暖米色伪装成中性色；
- 不得十张全部使用相同纸张纹理、相同木色和相同日落光；
- 文字必须与背景形成清楚对比，不能全部使用暖棕或金色弱对比字。

### 主角与配角

允许适度跨页重复的品牌主角：

- 定制中文主字标；
- 核心超级符号；
- 主产品；
- 核心空间气质。

原则上只重点出现一次的配角：

- 手提袋、打包盒、杯、碗和餐具包；
- 围裙、员工服；
- 桌牌、取餐牌、菜单牌；
- 小票、会员卡、吊牌、贴纸、封签；
- 其他运营应用物料。

主角重复时也不得机械复用同一张图片、同一裁切和同一模块比例。

### 文字密度

- 中等文字密度页面最多 2 张，通常为品牌元素页和品牌故事页；
- 其余页面不得出现正文段落；
- 低文字页面只保留品牌名、必要标题、短句和少量标签；
- 海报页中的海报文案属于设计对象，但页面外围不得再堆说明文字；
- 不得用微型中文、无意义英文、细线和编号填满留白。

### 绝对禁止

- 以一张十页合板、十宫格、长图或总览图代替 10 张独立图片；
- 默认使用 4:5 竖版；
- 要求用户自行拼版；
- 将 Figma 设为依赖、前置条件或验收条件；
- 因没有 Figma URL、file_key 或 node_id 阻塞任务；
- 直接使用黑体、宋体、圆体、书法体或其他现成字体冒充最终 Logo；
- 十张中的品牌名字形发生漂移；
- 页面显示序列号或页码；
- 每页都写大段说明；
- 袋子、围裙、杯子、菜单牌、小票等配角跨页反复出现；
- 十张全部使用暖米、奶油或黄棕底色；
- 主图、背景、文字和强调色在多数页面全部同时偏暖；
- 连续项目复用相同暖色模板、木质空间和金黄日光；
- 用错字、乱码、无意义英文、假电话、假二维码、假地址或假奖项制造专业感；
- 复制参考案例的品牌名、字标、超级符号、水印、设计公司页脚或完整商业外观；
- 只生成单素材而没有整版案例展示；
- 十页复制同一版式模板；
- 连续项目只替换“灶、山野、火、院子”等相似语义而没有真正改变方向。

### 默认输出

- 数量：10 张独立图片；
- 比例：统一 `3:2` 横版；
- 推荐像素：`2400 × 1600 px`；
- 格式：PNG；
- 页面内无序列号；
- 文件顺序由 `CASE_MANIFEST.json` 管理，文件名优先使用语义角色名；
- 用户指定尺寸时，以用户要求为准。

## 2. Figma 专项路线｜仅明确要求时使用

只有用户明确要求可编辑 Figma 文件、组件库、变量、node ID 或设计团队协作源文件时，才读取：

- `restaurant_design_system/START_HERE.md`；
- `restaurant_design_system/FIGMA_FIRST_NO_ADOBE_PIPELINE_V1.md`；
- 该路线指定的 Skill、配置与 validator。

旧 Figma validator 仅约束 Figma 专项路线，不约束 V4.2 每日品牌案例。

## 3. 单张餐饮海报与视觉素材

读取 `AESTHETIC_SKILL_DESIGN_CHARTER.md` 后，再读取 `skills/restaurant-poster-art-director/SKILL.md`、`generation/RESTAURANT_POSTER_IMAGE_RULES_V1.md` 和相关配置。

独立海报多风格配额只适用于独立备选，不得强加到同一品牌十张案例中。

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

## 6. 旅行视频 / 照片极简 Zine

凡涉及旅行视频帧、旅行照片、`gc-minimal-zine-poster` 旅行适配、`撕纸效果` 或 `$tear-paper`，先读取：

1. `AESTHETIC_SKILL_DESIGN_CHARTER.md`；
2. `skills/gc-travel-zine-poster-v1/SKILL.md`；
3. 该 Skill 要求读取的 `UPSTREAM_SKILL.md`。

核心原则：

- 本地路线是上游 `gc-minimal-zine-poster-v0-1` 的 **thin wrapper**；
- 不得再恢复本地视觉家族、55% 照片阈值、结构转译最低要求、`REJECTED_*` 审美失败码或 cheapness detector；
- 只允许在必要时适配画幅、真实照片素材保真、用户明确提供的地点文字和多图独立交付；
- 上游 Prompt Compiler、Variation Engine、Color Engine、Negative Constraints、Workflow、Quality Gate 保持原样；
- `撕纸效果` / `$tear-paper` 只是路由别名，不是最终图像 Prompt 的视觉词。

旧调用名存在时只作为兼容入口，不得覆盖 canonical thin wrapper。

## 7. V4.2 最终检查

每日或单次完整品牌案例在交付前必须确认：

```text
[ ] 正好10张独立图片
[ ] 全套统一3:2横版，或符合用户明确指定尺寸
[ ] 页面内没有01、02、03等可见序列号
[ ] 不是一张总览合板
[ ] 存在可解释的定制字标系统
[ ] 十张品牌名和字标完全一致
[ ] 只有1—2张中等文字密度页面
[ ] 其余页面没有正文段落
[ ] 配角物料没有跨页重复作为主要内容
[ ] 已记录brand_color_personality与temperature_map
[ ] 暖米/奶油/黄棕底默认不超过3张
[ ] 至少4张不是暖米或奶油底
[ ] 至少2张采用冷色或中性底
[ ] 至少1张采用深色、低明度或强对比背景，或记录合理例外
[ ] 同一页面没有主图、背景、文字、强调色全部偏暖
[ ] 至少使用三类背景家族和四种版式骨架
[ ] 中文和拼音可读
[ ] 食品、空间、包装和物料无明显结构错误
[ ] 没有复制参考项目的水印、署名或商业外观
[ ] 最终状态为READY
```

任何一项未通过，不得声称任务完成。