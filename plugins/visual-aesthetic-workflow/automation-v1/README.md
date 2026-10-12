# 刘先生·视觉设计工作流｜图片生成自动化扩展 V1（候选）

> **当前身份：已实现的可测试源码扩展 / 尚未部署到现有 Site / 不等于线上完全自动化。**  
> 属于同一私有插件「刘先生·视觉设计工作流」的增量模块。**禁止新建 Site、第二插件、第二 Figma 文件、覆盖旧 0.5.0 部署，或修改原生任务锁。**

## 1. 目标和边界

一张真实参考图 + 一次目标描述 → 自动读取私有原始字节和 SHA256 → 付费额度经真人签名授权 → 真实多模态分析 → 将分析压成可生成 Prompt → 明确绑定同一参考图调用 Image API → 原始 PNG 私有归档和回读 → 原图硬技术检查 → **等待真人判断摄影是否认可** → 通过已连接 Figma 执行器复用独立摄影层及已批准文字母版 → 真正导出并由独立像素审计器检查 → **等待真人确认完整海报** → 交付。任何未完成的外部环节返回真实 BLOCKED，不能冒充 PASS。

**两次审美人审不能自动化代替用户**。API 付费不自动授权，商业版权不自动认证，正式发布也不能自动发生。若用户选择使用现有 ChatGPT Image 而非独立付费 API，站点本身没有调用聊天工具的权限，只能由 ChatGPT/Work 在实际对话中执行并回传可核验的原始输出；不能把聊天额度当 API 额度。

## 2. 已审查并实质修复的旧流程漏洞

| 曾经的问题 | 这个扩展的处理 |
|---|---|
| 参考照片被误当我们生成的图 | reference.role / 原件 SHA256 / 输出 SHA256 分开且不可互换；上传真字节后再次校验 |
| 有血统却未传进生成器 | OpenAI Images edits 请求直接发送真实原图二进制；记录 source hash + provider response |
| 蒸馏报告直接复制成冗长提示词 | 从真正观看参考像素得到的视觉程序压缩成可成像的主体 + 2–8 项高杠杆变量 + 最多4项必要避项；**不规定越短越好** |
| X/Y 与下载次序混淆 | 记录每个输出原件字节 SHA256、job_id、prompt 和引用；更正人审时只追加并 supersede 原事件 |
| 生成成功但归档失败后自动重生 | 分析和生成先以持久 revision 预留唯一尝试，再发出付费请求；不确定时只允许对原尝试对账，不自动再扣费用 |
| 技术检查当审美通过 | 分开像素身份/格式检查、摄影真人验收、成品独立像素审计、完整海报真人验收 |
| 拼接把已认可摄影与字稿毁掉 | 必须由现有 Figma 执行器使用原图独立 IMAGE fill + 克隆已批准 TEXT/VECTOR；原件不变 |
| 插件与 Figma 进度脱节 | 每个外部动作要求执行回执、原生 file_key/frame_id、导出 PNG SHA256，使用同一个 D1 job ID/修订号防并发 |
| 固定9:16实际上只有近似比例 | 对原生宽高执行 16*w===9*h 判断；未满足时不得谎称准确9:16，后续衍生裁切必须另记真实操作 |
| 参考图许可不明 | 来源 rights 明示 UNKNOWN / PERMISSIONED / USER_OWNED；不自动发布，更不把网络参考当自有素材 |
| 出现单张胜出就修改全局 Skill | 只输出 scoped evidence；跨多个独立案例与回归测试通过后才允许审核晋升，不自动改全局规则 |

## 3. 当前源码

- engine.mjs：持久阶段合同、严禁跳步骤、人审纠错、付费预留、不会无意识重试、原始文件与生成图分层
- openai-image-adapter.mjs：实际含参考图的 OpenAI Vision/Images 请求、原始图格式与字节 SHA256、私有 R2 资产回读（使用单独 API 帐单）
- source-upload.mjs：一次性10分钟私有上传票据、网页上传参考原件、SHA256/尺寸验证、单用户 D1 绑定
- mcp-overlay.mjs：在**已运行的现有 v0.5 Worker**外增加 MCP 操作、同一 D1 新表、revision compare-and-swap、签名人审入口、Figma/审核执行器注入点
- engine.test.mjs / source-upload.test.mjs：无付费调用的回归测试
- package.json：Node.js 22 环境下 npm run check 和 npm test
- .github/workflows/visual-automation-addon-ci.yml：只跑本扩展的源码检查与无网络回归测试，不改 VPD 审美规则

## 4. 生命周期与真正自动化的暂停点

AWAIT_SOURCE → AWAIT_COST_APPROVAL → AWAIT_VISUAL_PROGRAM → ANALYSIS_IN_FLIGHT → RENDER_READY → RENDER_IN_FLIGHT → AWAIT_TECH_AUDIT → **AWAIT_PHOTO_HUMAN** → AWAIT_FIGMA → AWAIT_POSTER_AUDIT → **AWAIT_POSTER_HUMAN** → COMPLETE。

- 参考首次上传：用户选择一次原始文件；机器人不能暗自猜测本地路径。
- 人审：必须来自现有 Site 的受信任签名点击回执；MCP 模型自行传入“用户已批准”不允许。
- 预算：分析与生图是各自**付费** API 请求；必须先通过真人额度许可，否则 WAIT。
- 独立图像审核只能自动提供辅助判断。美学偏好与最终录用由用户决定。
- 单轮生成默认1张；A/B 仅在用户明确要求的情况下分两个绑定同一参考图的独立任务，每路1张、匿名展示、按原件 SHA256 解盲。不能把“先后下载”当 XY。
- 不允许异常自动重试已经预留的付费分析或生图；首先核对对应 provider request id / 存档。

## 5. 在原有 Site 上安装，而不是新建站点

现有 Site/project：
- 名称：刘先生·视觉设计工作流
- project_id：appgprj_6ac469271bac81919273f01e8e73ba35
- URL：https://liu-visual-workflow-20261006.deemoliul.chatgpt.site/
- 通过已连接 MCP 工具实读运行版本：0.5.0
- 仓库历史完整部署源：最后公开源码包是 v0.3.0，**不能拿它替换 v0.5.0 的代码和数据。**

完整上线必须先从现有 Site 的真实 v0.5.0 工作区导出并核验当前源及数据库结构，在同一个 Worker 入口外套用：

    import {extendExistingVisualWorker} from "./automation-v1/mcp-overlay.mjs";
    import deployedV050Worker from "./PRESERVED_ACTUAL_V050_ENTRY.mjs";  // 示例：不可凭此虚构文件
    export default extendExistingVisualWorker(deployedV050Worker, {
      verifyHumanApproval: existingSiteSignedApprovalVerifier,
      external: {compose: existingFigmaMcpExecutor, auditPoster: independentRealPixelAuditor}
    });

以上是**接入合同，不是已部署的工作文件**；涉及三个 callback 必须由现场真正存在的服务实现，不得写布尔占位充当通过。

还需要在**同一 Site** 安全绑定：
- D1：沿用现有 DB，新增两个以 visual_ 开头的表，不清空旧表或重建项目；
- 私有原图存储 R2：VISUAL_ASSETS（当前 hosting.json 的 r2 仍为 null，尚未开通）；
- 后台密钥：OPENAI_API_KEY、OPENAI_VISION_MODEL、OPENAI_IMAGE_MODEL；**只存在托管密钥库，不写 GitHub、不要求在聊天直接提供密码**；
- 接口信任：现有的 oai-authenticated-user-id 由可信宿主验证；同源上传票据10分钟/单次消费；Site 真实签名用户确认 UI；
- 与本账号现有 Figma 工具的稳定授权、独立截图/导出原始字节读取能力；
- 长耗时任务后台运行器或队列（现有 host 未核实，不得声称无人值守持续运行）。

未满足上述任一项，系统返回 capability BLOCKED，不创建伪造图片、不宣称 Site 已升级。

## 6. 用户操作（上线后）

首次：上传参考原图、说明创作目标、确认分配的付费调用上限。  
此后：插件按状态自动运行直到**摄影图片的真人审核**；确认后自动请求 Figma 合成并进行独立原生导出审核；再让用户确认完整成品。中途异常自动停在具体 stage，可依据原 job_id 继续，不重新生成已成功的图片。

## 7. 本轮验收与不允许夸大的结论

- 已完成：独立仓库内扩展源码、状态机、真实参考图 API 适配、私有存储回读逻辑、一次性上传与 MCP 操作、自动回归测试。
- 尚未完成：线上 v0.5.0 **原地部署**，私有 R2 绑定、API secret、签名人审 UI、实际 Figma 执行适配器、真实独立像素审计与最终作品真人通过。
- 任何“自动生成/自动合成”都必须以实际工具请求、输入原始字节、输出原始字节和回读证明，不靠工具名称或 README 猜测。
- 当前原生任务锁 revision355 / checkpoint377 不属于这次附加模块可写范围，且《地图以外》Y/R1、S7、旧插件身份和数据不得被重置。
