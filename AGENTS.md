# Repository instructions for Codex

版本：`3.0.0`
状态：`MANDATORY`

本仓库有四套路由：餐饮品牌设计、单张餐饮海报与视觉素材、私人审美评分、餐饮经营总控。先读根 `START_HERE.md`。

## 餐饮品牌设计

凡涉及新餐饮品牌、每日方案、三页验证或十页案例，必须完整读取：

- `restaurant_design_system/START_HERE.md`；
- `restaurant_design_system/FIGMA_FIRST_NO_ADOBE_PIPELINE_V1.md`；
- `restaurant_design_system/GLOBAL_FEEDBACK_RULES_V1.md`；
- `restaurant_design_system/PHASED_DELIVERY_RULES_V1.md`；
- `restaurant_design_system/PORTFOLIO_PRESENTATION_RULES_V1.md`；
- `restaurant_design_system/OUTPUT_STRUCTURE_10_IMAGES_V2.md`；
- `restaurant_design_system/DAILY_WORKFLOW_V2.md`；
- calibration 文件；
- 四个专用品牌 Skill；
- `skills/personal-aesthetic-critic/SKILL.md`。

强制行为：

1. 读取最近 7 个项目；
2. 建立至少 6 个内部候选，输出至少 3 个方向；
3. 推荐方向必须形成 `产品事实 + 经营规则 + 品牌观点 + 视觉机制`；
4. image_gen 只生成无文字素材；
5. 任何 AI 完整品牌页标记 `REJECTED_AI_FULL_PAGE`；
6. 先创建 Figma 三页验证；
7. 三页通过审美闸门后才扩展十页；
8. 十页必须是十个独立 Figma Frame 和十个独立导出；
9. 记录 Figma URL、file_key、node_id、字体、变量、组件和实际尺寸；
10. 每页记录 `brand_evidence`；
11. 完成反重复、AI、品牌证据、作品集、Figma和审美审计；
12. 只有全部通过才使用 `CONCEPT_SET`。

绝对禁止：

- 让图像模型直接生成完整品牌页面；
- 三页失败后继续十页；
- 用伪中文、假日期、假二维码、假电话和无意义英文制造专业感；
- 要求用户自己完成 Figma 排版；
- 以 Adobe 不可用为阻塞理由；
- 无 Figma node_id 却声称完整流程完成。

## 单张餐饮海报与视觉素材

读取 `skills/restaurant-poster-art-director/SKILL.md`。其多风格配额只适用于独立海报备选，不得用于一个品牌的十页作品集。

产品真实感、真实文字、实际尺寸和发布审计仍为硬门槛。

## 私人审美

品牌项目使用：

- `skills/restaurant-brand-aesthetic-gate/SKILL.md`；
- `skills/personal-aesthetic-critic/SKILL.md`；
- rubric、penalties 和 calibration。

锚点不足时不得伪造 `personal_fit`。必须明确区分公共专业标准、参考图接近度和用户私人偏好。

## 餐饮经营

读取 `restaurant_operations_system/START_HERE.md` 和 `skills/restaurant-operations-master/`。

- 收入不能替代贡献毛利；
- 食品安全 `BLOCKER` 不能被评分覆盖；
- 总部方案必须通过普通员工和高峰压力测试；
- 没有预注册试点不得全店推广；
- 不在 public 仓库提交敏感经营信息。

## Checks

现有 validator 和审美评分命令继续有效。品牌项目还必须检查项目文件是否包含 `CONCEPT_ENGINE.md`、`ASSET_MANIFEST.json`、`FIGMA_MANIFEST.json` 和 `AESTHETIC_EVALUATION.json`。
