# VPD 新聊天图像生成 → Google Drive 回传合同 V1

日期：2026-09-22
状态：MANDATORY_FOR_FUTURE_GENERATOR_CHATS

## 目的

以后所有 VPD 新聊天只负责隔离生成。生成结束后必须立刻把原始图上传到 Google Drive，并把 Drive 链接返回给用户。用户把该 Drive 链接发回主聊天，主聊天通过 Google Drive 读取同一原文件并完成评审/接续。

这样不再依赖：
- 用户手动重新上传图片；
- 截图；
- 临时 sandbox 路径；
- 文件名猜测；
- 生成聊天里的视觉上下文继续累积。

## 生成聊天必须执行

1. 读取最新项目入口、任务锁、对应 RUN 文件。
2. 只加载 RUN 文件允许的视觉参考。
3. 只生成 RUN 文件授权的数量；默认 n=1。
4. 生成后不在同一聊天继续审美修改或重试。
5. 记录 gen_id、runtime file id、requested aspect、actual dimensions。
6. 计算或取得原始 PNG 的 SHA-256。
7. **把原始 PNG 上传到 Google Drive。**
8. 上传后读取 Drive metadata，取得：
   - Drive file ID
   - browser/display URL
   - 文件名
   - mime type
   - size
9. 将这些字段写入对应 provenance。
10. 生成聊天最后只返回一个极简回传块，不展开评价：

```
已生成并归档。
DRIVE_URL: <Google Drive browser URL>
DRIVE_FILE_ID: <file id>
SHA256: <sha256>
DIMENSIONS: <width>x<height>
请把 DRIVE_URL 发回主聊天。
```

## 隐私/分享

- 默认不把文件改成公开互联网可访问。
- 同一用户账号下的 Drive 链接足够让主聊天通过 Google Drive connector 读取。
- 不调用“anyone with link”之类公开分享，除非用户明确要求。
- 不把 OAuth token、Drive credential、下载签名 URL 写进 GitHub。
- provenance 只保存稳定的 Drive file ID/browser URL，不保存短期 signed download URL。

## 主聊天收到 Drive URL 后

1. 直接用 Google Drive 读取该 URL。
2. 核对 Drive file ID 与仓库 provenance。
3. 核对 SHA-256 / dimensions（如 provenance 已保存）。
4. 只基于 Drive 原始文件评审，不要求用户再次上传。
5. 评审完成后再决定是否解锁下一路。

## 失败处理

- 如果图片生成成功但 Drive 上传失败：停止，不生成第二张；保留 runtime file id，报告上传失败点。
- 如果 Drive 上传成功但无法取得 browser URL：用 file ID 再读取 metadata；仍失败则停止。
- 如果 Drive 原图与 provenance SHA 不一致：停止，不继续下一路。
- 不因为“只差一个链接”就重新生成图片。

## 当前 Stage 1 特殊规则

Route A 已经归档：
- Drive file ID: 1mOt0T4vS7KaJeR0PP0pCg5dq6dG5DdHm
- URL: https://drive.google.com/file/d/1mOt0T4vS7KaJeR0PP0pCg5dq6dG5DdHm/view

Route A 因主体任务错误而技术失败，因此 Route B 暂不执行。剩余 Route B 授权额度不消耗，直到主聊天修复新的 fresh-chat handoff 后再决定。
