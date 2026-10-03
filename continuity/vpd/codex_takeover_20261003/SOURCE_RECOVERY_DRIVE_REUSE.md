# 茶作摄影修补：Drive 原图调用入口

先从最新分支 START_HERE.md 和原生任务锁恢复，再用本入口。当前完整品牌海报仍未完成；原三版已否决。本次修补候选仅通过独立 AI 摄影审核，真人仍 PENDING。唯一下一动作是刘先生验收局部背景重建能否作为冻结摄影输入。没有新的海报额度或生成授权。

刘先生明确要求图片存入 Drive。现在 Drive 是图片主存储，Figma 保留可编辑源及原字节备用档案。归档目录为 [视觉审美操作系统_茶作_原件与版本归档_20261003](https://drive.google.com/drive/folders/1wV_R9VcJQ9z4sOynHtHczkSP9z3KpK9O)。现有连接账户、该目录与历史茶作项目图片均已核对为同一所有者；没有改共享权限。

| 实际文件 | Drive ID | SHA256 前缀 | 用途 |
| --- | --- | --- | --- |
| 最终局部背景重建候选，1536×1024 | 1ZU-jfc_3JZqNlKn56PSpMyBLjwYnqIIA | 7fd7777f | 当前送摄影真人验收 |
| 确认的第一张含旧字原件 | 1a4vS6o7yXaCS-EPU18nGvXsUelc3bnwn | e7af9c9e | 摄影对照及保护输入 |
| 透明修补层 | 1dMcZn4qws47UuxRsAJDLxYY1RO0HdKZF | 74899b51 | 原件上独立栅格层 |
| 唯一工具生成的去字素材 | 14eZPr5_u_brLLZzMv0u3VPg0fOMtJO4A | 01faebaa | 整图改变主体，只可按已存蒙版取背景素材 |
| 窄笔画蒙版失败预览 | 1TLIWNC3E5H7apD_Er7uVvjhWGctl6nqL | 9d473dbd | 残字/暗影失败记录 |
| 旧正式 V1 | 1sYdyYYpIDfoINLbMELi3ODdpqfLwCMUE | 5845727b | AI_FAIL / 真人否决 / R4 源绑定错误 |
| 旧正式 V2 | 1RZMu9PerLQM8H1mVPZzM4sTYxY1AMLN4 | deb61c60 | 同上，不能作新基准 |
| 旧正式 V3 | 1jBx1Gf5fVhHIq2g0PSMrXjNAeBWiuQwg | 078ec5ae | 同上，不能作新基准 |

完整 SHA、实际 provider revision ID、文件大小、MIME、创建/修改时间、逐个 HTTP200 原字节回读结果在 `evidence/vpd/codex_takeover_20261003/source_recovery/DRIVE_ARCHIVE_MANIFEST.json`。八份文件均与本地保存的原字节完全一致；版本失败没有被覆盖。

ChatGPT 真实读取步骤：加载 google-drive skill；先按 Drive ID 调 `get_file_metadata`，使用返回的真实 Drive URL。PNG 是存储文件，调用 `fetch(url=该URL, download_raw_file=true, include_base64=false)`，取得本次认证的 `file_uri` 或 `workspace_path`。按返回的临时下载引用取原字节到私有目录，核对清单完整 SHA、大小与1536×1024，再用可用看图工具查看像素。不要用原生文档 export、缩略图、文件名或过期下载 URL 代替原件；不要公开保存认证下载 URL。每次调用重新取得临时引用。读取失败时标记无法评测，不判通过。

本机可用 bundled Python urllib/Pillow 读取下载原件，或复用仓库已有的受身份绑定下载脚本；另一宿主必须先发现其实际运行环境。Figma 的 283:5 仍是精确最终 PNG，278:2 是原件，283:2 是锁定原件283:3＋透明层283:4。实际方法、成熟审核 skill 版本、蒙版、保护检查、失败边界和独立评测继续读 `SOURCE_RECOVERY_REUSE.md`；后者是先前 Figma 归档快照，当前主存储以本 Drive 入口和原生锁为准。

保护结论仍仅为文字邻域外1,259,404个RGB像素完全相同；约19.93%邻域涉及局部背景重建。不是找回原字后隐藏摄影，也不是新海报或真人认可。原第一张的生成模型、seed与完整生成配方仍未确认。不要把本次去字请求当作成功摄影生成规则。

后续已授权任务产生或修改实际图片时，沿用此归档方式：新版本另存，写 Drive ID / revision ID / SHA / 原图、作品和审核对应关系，下载回读；再由唯一主执行者写同一原生任务锁、检查点与账本。没有触发任务时不会自动运行，不恢复定时任务。
