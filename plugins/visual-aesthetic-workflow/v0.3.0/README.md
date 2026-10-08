# 刘先生·视觉设计工作流 v0.3.0

现有 Site 原地发布，部署文件逐字节来自用户指定 liu-visual-workflow-v0.3.0-site.zip；full-source-audit 与 source-tests 的相同文件已核对一致。

入口 worker.mjs 转发至 server/index.js；build.mjs 只复制原有 6 个部署模块与 hosting.json，不改业务逻辑。

唯一流程：参考真实像素全文分区 → AI 实际生成完整透明 RGBA PNG 母版 → Figma 仅按母版重建可编辑文字 → 独立读取两份 PNG 并按区域测量/视觉审核 → 母版、可编辑 Figma、审计三项交付。

upgrade_typography_contract 是显式旧合同升级入口；按 task_id 和 revision 原地迁移，保留历史、旧证据及 native snapshot，重置至 REFERENCE_TEXT_EXTRACTION。旧数据不得视为新合同通过。

边界：Site 校验外部执行器的证据字段及数值阈值，并不独立读取图片或验证生成事件/节点树。visual_v030_pixel_auditor.py 实际读取 PNG、计算 SHA 和逐区域差分；文字语义准确性仍要求审查方实际看图。不得将控制器测试通过当作真实作品审核通过。

部署包 SHA256：592dad6098a5766bc609840a8193a344baa066aad282542533ff116f7d139f7a。
