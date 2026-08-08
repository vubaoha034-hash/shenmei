# Continual Learning Trigger Rule

版本：`1.0.0`
状态：`MANDATORY`

本规则负责把 `skills/skill-refiner/` 接到仓库级 Agent / Codex 工作流中，使 Skill、Agent 行为和仓库编码经验能够长期积累，但不得把每次任务都变成元学习任务。

## 1. 触发时机

在一次用户任务接近结束时，只做一次轻量检查。仅当本次任务出现以下任一**证据事件**时，必须读取并调用：

- `skills/skill-refiner/SKILL.md`

证据事件包括：

1. 用户明确否定、纠正或指出一个可能复用的失败模式；
2. 同类失败再次出现；
3. 测试、CI、validator、运行结果证明存在稳定 defect / regression；
4. 某个新 tactic 明显提高结果，并且具有复用价值；
5. 代码、工具、数据源或仓库结构证明了稳定 invariant；
6. 已晋升的旧规则被证据证明有害、过时或过宽；
7. Agent 的路由、委派、工具使用出现可复用的稳定成功或失败模式。

普通成功、一次性偏好、临时网络错误、偶发工具失败、未经验证的原因猜测，不触发长期学习。

## 2. 默认只记录，不自动改正式规则

第一次出现的新问题，默认只执行 `observe`。

不得因为一次差评、一次失败或一次用户情绪强烈，就直接修改：

- 目标 `SKILL.md`；
- `AGENTS.md`；
- repository rules；
- validator；
- production code；
- 全局 Agent policy。

只有 `skill-refiner` 的 Promotion Gate 达到要求并完成 baseline-vs-candidate 验证后，才允许进入正式修改流程。

## 3. 必须先分类学习层

每次记录前，先选择最窄层级：

- `skill`：只属于某一个 Skill 的程序、审美、领域或调用经验；
- `repo`：只属于当前仓库的代码、CI、测试、架构、数据源、发布或调试经验；
- `agent`：跨 Skill / 跨仓库仍稳定成立的路由、委派和工具策略。

不得把局部经验误升格为全局 Agent 规则。

## 4. 自动触发的成本上限

为了避免 Agent 因“学习”而越来越慢：

1. 每个用户任务最多执行一次 refinement evidence review；
2. 没有证据事件时不得调用 `skill-refiner`；
3. 自动触发默认只记录必要证据，不自动做大规模历史回放；
4. 不得为了形成候选规则而制造额外任务或虚构独立案例；
5. candidate / evaluation / promotion 只在阈值自然达到、用户明确要求升级、或确定性 defect 已验证时继续；
6. archive 默认不加载，只有 regression / rollback 调查时才读取。

## 5. 审美任务额外约束

视觉、审美、海报、图片 Skill 必须继续服从 `AESTHETIC_SKILL_DESIGN_CHARTER.md`。

特别注意：

- “不好看”本身不是 correctness defect；
- 单次审美差评只记录 scoped evidence；
- 不得自动把 subjective taste 变成硬 blocker；
- 当规则变多导致表现更僵，优先候选动作是合并、删除、回退或移入 `references/`，不是继续追加规则；
- 成熟 upstream Skill 的本地 wrapper 不得因少量失败重新膨胀成复杂本地视觉系统。

## 6. Coding / Repo 长期提升

对代码与仓库工作，优先记录以下 durable knowledge：

- 必跑测试与 validator；
- 反复出现的 CI 根因；
- fragile module / architecture invariant；
- 数据源真实限制；
- 已验证的 debugging tactic；
- release / deployment / migration 顺序；
- 哪些修改容易造成 regression；
- 哪些自动化检查能取代重复人工判断。

优先把验证后的 repo lesson 晋升为测试、脚本、CI 或 scoped developer docs；能用可执行检查表达的，不要只增加 prose rule。

## 7. 持久化要求

证据默认写入：

```text
.skill-evolution/<target>/state.json
```

若当前环境不能持久化该文件，不得声称“已经长期记住”。应明确把本次证据视为未持久化，并在具备持久仓库写入能力时补录。

正式晋升必须通过 Git branch / diff / PR，并记录 candidate ID、evidence IDs、evaluation 和最终 Git ref。

## 8. 触发后的用户体验

`skill-refiner` 是后台治理步骤，不应抢占正常任务输出。

除非：

- 用户明确询问学习/升级情况；
- 本次触发形成了需要用户知道的候选变更；
- 发现现有正式规则正在造成持续性 regression；

否则无需在最终答复中展开完整 refinement 日志。

核心目标：**持续变强，但核心规则保持紧凑；持续学习，但不让正常工作越来越慢。**
