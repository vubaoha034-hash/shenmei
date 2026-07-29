# START HERE — 强制执行入口

版本：`4.0.0`
状态：`MANDATORY`

## 1. 最高优先级路由

任何执行者先判断任务类型。当前仓库包含五条路线：

1. 每日或单次完整餐饮品牌案例；
2. 单张餐饮海报与独立视觉素材；
3. 明确要求可编辑 Figma 源文件的正式品牌系统；
4. 私人审美评分与校准；
5. 餐饮经营总控。

同一任务涉及多条路线时分别通过相关硬门槛。根入口的路由优先级高于旧子目录入口。

## A. 每日或单次完整餐饮品牌案例｜V4 主流程

适用：

- 每天 09:00 自动品牌案例；
- 系统自主确定品牌；
- 一套十张品牌案例；
- 品牌空间、门头、Logo、超级符号、故事、产品、海报、包装和运营触点；
- 小红书品牌设计案例；
- 用户要求参考案例图采用多模块整版排版。

必须读取：

1. `DAILY_AUTOBRAND_SYSTEM_V4.md`；
2. `rules/DAILY_CASE_10_IMAGE_STRUCTURE_V4.md`；
3. `rules/BOARD_LAYOUT_PRESENTATION_RULES_V4.md`；
4. `rules/BRAND_WORDMARK_AND_TYPOGRAPHY_RULES_V4.md`；
5. `rules/DAILY_CASE_QUALITY_GATE_V4.md`；
6. 每日任务另读 `schedules/DAILY_0900_BRAND_CASE_V4.md`。

强制结果：

```text
1 个完整餐饮品牌
→ 定制变形中文品牌字标
→ 10 张独立完整案例展示页
→ 每张允许 2—6 个有秩序的展示模块
→ 空间、字标、故事、产品、海报、包装、应用和总结全部覆盖
→ 逐张审查
→ READY
```

核心边界：

- Figma 不是依赖、前置条件或验收条件；
- 允许图像生成系统直接生成完整品牌案例展示页；
- 品牌 Logo 必须是设计过的定制字标，不能直接套用现成字体；
- 十张必须是十个独立图片文件；
- 禁止用一张十页总览合板、十宫格或长图代替十张；
- 禁止要求用户自行拼版；
- 参考图用于学习多模块呈现、尺寸和信息层级，不得复制品牌、字标、水印、署名或完整商业外观。

默认尺寸为统一竖版 `4:5`，推荐 `2160 × 2700 px`。用户指定比例时以用户要求为准。

## B. 单张餐饮海报与独立视觉素材

适用：单张海报、单个产品主视觉、独立海报备选或品牌项目中的单素材。

读取：

1. `skills/restaurant-poster-art-director/SKILL.md`；
2. `generation/RESTAURANT_POSTER_IMAGE_RULES_V1.md`；
3. `config/restaurant-poster-generation.v1.json`；
4. calibration 文件。

独立海报的多风格配额不得套用到 V4 十张品牌案例内部。`READY_TO_POST` 必须通过产品、文字、实际尺寸与 100% 检查。

## C. 可编辑 Figma 正式品牌系统｜仅明确请求时使用

只有用户明确要求以下内容时，才读取旧 Figma-first 路线：

- 可编辑 Figma 文件；
- 组件库、变量和 node ID；
- 生产级设计协作文件；
- 明确要求 Figma 三页验证或十页 Frame。

读取：

1. `restaurant_design_system/START_HERE.md`；
2. `restaurant_design_system/FIGMA_FIRST_NO_ADOBE_PIPELINE_V1.md`；
3. 该路线要求的 Skill、配置与 validator。

不得把该路线强加给每日品牌案例、直接整版生成或用户明确说“不用 Figma”的任务。

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

没有真实基线只能诊断；食品安全、负贡献或高峰不可执行是 `BLOCKER`；没有试点 PASS 不得 `ROLLOUT_READY`。

## 混合任务

经营结论和视觉交付分别通过独立闸门。漂亮设计不能覆盖亏损、食安或执行问题；经营逻辑也不能覆盖错字、产品错误、结构错误和弱品牌逻辑。

## 隐私

仓库为 public 时，不上传逐笔流水、员工个人信息、供应合同、私人照片、账号或其他敏感数据。只提交脱敏模板、聚合证据和稳定的非敏感设计记录。