# VPD 当前状态权威对齐（2026-09-29）

- 基线：分支 `visual-program-distillation-v2-photography-design-20260814`，提交 `d635badb850f790004925efddba2b484ca2fecf0`。
- 当前任务锁原为 revision 172，检查点原为 sequence 194；两者共同指向 Figma `227:2` 的唯一候选，等待刘先生实际像素评审，生成与 Figma 新写入额度均为零。
- 原适配器仍指向 revision 161 / RF4，检查点锁哈希过期，商业设计账本尾也只到 RF4；因此入口校验返回 `PARENT_TASK_CHANGED`。这是索引与校验程序的漂移，不代表候选获得人类审美通过。
- 已有冻结文件 `evidence/vpd/p6_authority_repair_v1/COMMERCIAL_LEDGER_PREEXISTING_HASH_DEFECT_FREEZE_20260923.json` 逐条绑定商业设计账本第 62–83 行共 22 个旧哈希缺陷。原始 118 行不修改；校验只允许冻结所列的原始字节及宣称/重算哈希组合，其余行严格校验。
- 修复把适配器、检查点、任务锁、账本尾对齐为同一当前状态；新增一条 **聚合纠偏记录**，明确 revision 162–172 的离散事件没有在这条账本中逐条补齐。不能从这条记录反推未记载的聊天、授权或质量结论。
- 旧任务锁和检查点中的长串阶段性 blocker 原样归档在 `HISTORICAL_BLOCKERS_20260929.json`；当前 blocker 只保留 `227:2` 人工像素评审和零执行额度，旧禁令不会被当作新的待执行任务。
- 只恢复状态读取和防跑偏验证。Figma `227:2` 是否通过、能否继续设计仍取决于刘先生的实际像素评审；此修复不授权生成、改图、第二候选或下游推广。
