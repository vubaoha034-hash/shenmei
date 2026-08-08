# Host Integration

`skill-refiner` provides the learning workflow and gate. It does **not** alter model weights, and a portable Agent Skill cannot guarantee that the host runtime will invoke it after every task.

For real continual improvement, the host agent/router should add a lightweight end-of-task review trigger.

## Recommended trigger policy

Activate `skill-refiner` after a task only when at least one evidence-worthy event occurred:

- the user explicitly rejected/corrected an output in a way that may generalize;
- the same failure pattern appeared again;
- a regression test or CI check exposed a stable defect;
- a reusable tactic materially improved the outcome;
- a stable repository/tool invariant was demonstrated;
- an older promoted rule was shown to be wrong or harmful.

Do **not** activate it merely because a task completed. Routine successful tasks should not generate learning records unless they reveal a reusable tactic.

## Recommended host policy text

A host-level agent policy can use the following semantics:

> At the end of a task, check whether there is concrete evidence of a repeated failure, authoritative correction, reusable success tactic, regression, or stable tool/repository invariant. If yes, invoke `skill-refiner` once to record evidence. Do not edit production Skills from raw evidence. Promotion must pass the Skill Refiner gate and Git review workflow.

Adapt the wording to the host product; do not copy this into every domain Skill.

## Persistence

The default ledger path is `.skill-evolution/<target>/state.json` in the repository working tree.

For long-term learning it must survive the session. Use one of these persistence patterns:

1. persistent local/remote workspace: keep the repo checkout durable;
2. Git-backed: include the relevant ledger state with promotion/maintenance commits so it can be recovered on another machine;
3. external durable store: mirror the JSON state into the host's persistent memory/database and materialize it before running the tool.

Do not assume an ephemeral sandbox provides long-term memory.

## Multi-agent use

When several agents can learn at once:

- each agent may record evidence locally;
- merge ledgers by evidence ID/fingerprint rather than concatenating blindly;
- only one promotion PR should own a given candidate at a time;
- Git is the authority for promoted production changes;
- unresolved contradictory evidence blocks promotion.

## Suggested cadence

- evidence review: event-driven, not every turn;
- candidate formation: when thresholds are met;
- compaction: periodically or when active evidence becomes noisy;
- promotion: only after evaluation.

This keeps continual learning cheap enough to leave enabled without turning every task into a meta-analysis task.
