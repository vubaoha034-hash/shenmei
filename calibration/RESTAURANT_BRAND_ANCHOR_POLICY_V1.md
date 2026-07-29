# 餐饮品牌审美锚点策略 V1.0

版本：`1.0.0`
状态：`MANDATORY`

## 1. 目的

本文件用于三页验证和十页作品集的私人审美校准。它不替代公共设计标准，而是回答：新方案更接近用户认可的参考，还是更接近已被否定的失败方案。

## 2. 锚点组

至少建立四组：

- `reference_brand_portfolio`：行业参考；
- `approved_brand_portfolio`：用户明确喜欢；
- `neutral_brand_portfolio`：可用但不满意；
- `rejected_brand_portfolio`：明确不喜欢。

每组必须使用稳定 GitHub 图片路径、Figma node URL 或稳定公共 URL。

## 3. 参考图拆解字段

每个参考锚点记录：

- page rhythm；
- negative space；
- focal hierarchy；
- typography contrast；
- image crop language；
- material realism；
- brand-engine visibility；
- application depth；
- what may be learned；
- what must not be copied。

## 4. 失败锚点字段

每个 rejected 锚点记录：

- generic-template evidence；
- weak brand-engine evidence；
- AI text or material failure；
- repeated layout；
- excessive explanation；
- fake professional metadata；
- product realism issue；
- why user rejected it。

## 5. 三页验证比较

每轮三页必须逐页回答：

1. 更接近哪个 reference/approved 锚点；
2. 更接近哪个 rejected 锚点；
3. 接近来自哪些可见设计决定；
4. 哪些差距可以通过排版修正；
5. 哪些差距来自品牌发动机，需要重做概念；
6. 是否不解释也能成立。

若与失败锚点的接近证据不少于正向参考，三页不得通过。

## 6. 防止表面模仿

接近参考图不等于复制：

- 绿色、米白、山野、云南等表面组合不得作为接近依据；
- 参考品牌名、Logo、字体、口号和包装轮廓不得复用；
- 页面壳、设计公司署名、水印、二维码、地址和虚构项目日期不得复用；
- 允许学习的是视觉哲学、章节组织、信息权重、留白、裁切和系统延展。

## 7. 锚点不足

稳定视觉锚点不足时：

- `personal_fit = null`；
- 仍执行公共专业评分；
- 仍可使用用户当前提供的参考做定性比较；
- 自动任务必须披露锚点不足；
- 不得声称系统已完整学习用户审美。

## 8. 自动任务闸门

自动任务不得因为锚点不足而伪造分数，也不得因为参考图不可访问而自动放行。

在没有稳定 reference 和 rejected 锚点时：

- 三页只能标记 `THREE_PAGE_PROOF`；
- 若当前任务没有用户实时提供参考，则必须使用公共专业评分并标记 `PERSONAL_CALIBRATION_PENDING`；
- 只有公共评分通过且没有已知拒绝模板时，才可继续，但最终报告必须披露私人校准未完成。
