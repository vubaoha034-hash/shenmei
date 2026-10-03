# 本轮保存与冷进入补充

仍先读根 START_HERE.md 和最新任务锁，再读 REUSE_FINAL.md。本页只补充该入口，不建立第二状态系统，也不授权第四版。

首次远端 51baee3 的新克隆真实恢复失败：Git 把本轮尚未跟踪的 CRLF 证据转换成 LF，原生 SHA 核验正确拒绝。失败原报告在 `evidence/vpd/codex_takeover_20261003/FRESH_ENTRY_RECOVERY_FAILED_51.json`，没有删去。

限定 `.gitattributes` 对本轮 continuity/evidence 两个目录使用 `-text`，保留已封存原字节及原判词；62个现有文件只有换行编码差异。旧真人证据、主任务锁、检查点、适配器、商业账本与校验代码未因该修复改动。修复不允许跳过 SHA 检查。证据见 `EVIDENCE_BYTE_PRESERVATION_FIX.json`、`PERSISTED_EVIDENCE_SCOPE_CHECK.json`、`SECOND_REMOTE_READBACK.json`。

第二个全新上下文在远端 51cc7557 的空克隆中，仅凭入口恢复原始R4和当前V3、核验两个精确SHA、实际查看两个像素原件，再运行既有状态检查，真实退出0。保护区1,356,936像素变化0。实际报告和模型/上下文/ImageView取证见 `FRESH_ENTRY_RECOVERY_VERIFIED.json`。这证明入口与当前成果恢复可行，不证明审美通过。检验仅恢复这两张图；未冒称所有历史版、审稿包或公开匿名访问已核验。

## Figma 源结构与字体条件

源259:2是FRAME；摄影259:3也是FRAME，锁定、1:1原图fill。字标259:46是FRAME，内部GROUP259:47及16个闭合VECTOR；文案259:64是FRAME，内部TEXT259:65/66。不要预设摄影必为RECTANGLE。新读取代理实际错误 `UNEXPECTED_SOURCE_TYPES` 与一次只读结构诊断均保留在上述恢复报告。

制作时和主执行者最后核验的Noto Serif SC Medium为可用，独立审查另一次冷读取曾出现 `hasMissingFont=true`。该差异不得被旧false快照覆盖，也不能据此认定永久字体缺失。实际目录列出了相同字体/字重；主执行者在同一次调用里按官方技能发现目录、读取现有getStyledTextSegments的fontName（包括variationSettings.wght=500）、await loadFontAsync，随后两TEXT无缺失标记，文字、字体、字号、xy、宽高完全相同，未创建/修改节点，未重新导出作品。实测见 `COLD_FONT_READINESS.json`。

以后每次冷进入要先发现可用字体，再加载节点实际当前字体后才做已授权的文字编辑；不得猜字体、改用替代字体、将文本转曲或凭旧快照保证所有账号无缺字体。加载失败应记录具体字体/环境阻塞。本轮无新增文字编辑或第四版授权。

## 本轮结论与复用边界

执行及必要流程已实际跑通；最终V3纠正校准后的冷审仍AI_FAIL，刘先生真人反馈PENDING。专业审查原报告及保存补充分别在 `PROFESSIONAL_AUDIT.json`、`PROFESSIONAL_AUDIT_PERSISTENCE_SUPPLEMENT.json`，最终引用以最新原生receipt为准。流程改善已验证，视觉收益未验证；时间节省、系统迁移与第二风格没有证据。

唯一下一动作仍是把真实第三版和失败意见交刘先生验收。三版/两修订已经用尽，不自动开始第四版或恢复定时任务。
