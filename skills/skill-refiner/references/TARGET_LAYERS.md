# Target Layers

Choose the narrowest layer that can own the lesson safely.

## `skill`

Use for knowledge/procedures specific to one Agent Skill.

Examples:

- an image Skill's composition rule;
- a finance Skill's validation sequence;
- a document Skill's formatting invariant;
- a domain-specific tool call pattern.

Preferred destinations: the target Skill's `SKILL.md`, `references/`, `scripts/`, tests, or assets.

## `agent`

Use for stable cross-task agent operating behavior.

Examples:

- when to delegate to a subagent;
- when a factual claim requires verification;
- stable tool-routing lessons;
- a durable user operating preference that truly applies across tasks.

Do not put domain-specific details here merely because they happened more than once.

## `repo`

Use for repository/project intelligence.

Examples:

- mandatory validators before recommendation/merge;
- recurring CI root causes;
- fragile modules and invariants;
- required release steps;
- data-source limitations;
- repository-specific debugging tactics.

Preferred destinations: repo-level agent instructions, developer docs, tests, validation scripts, CI, or scoped project references.

## Cross-layer promotion

A lesson may move upward only with broader evidence.

`skill -> agent` requires proof that the behavior is useful across materially different tasks/skills.

`repo -> agent` requires proof that it is not merely a quirk of one repository.

When uncertain, keep the lesson at the narrower layer.
