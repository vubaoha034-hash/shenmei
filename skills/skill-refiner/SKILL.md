---
name: skill-refiner
description: Evidence-driven continual improvement for Agent Skills, agent operating rules, and repository coding workflows. Use after repeated failures, authoritative corrections, successful reusable tactics, regressions, or stable tool/repository lessons. Records experience first, promotes only validated improvements, limits SKILL.md growth, and requires a reviewable Git diff/PR instead of silently rewriting production skills.
metadata:
  version: "1.0.0"
  evolution-policy: "evidence-gated"
---

# Skill Refiner

Use this skill to make another Skill, an agent harness, or a repository workflow improve over time **without turning its core instructions into an ever-growing rule dump**.

## Non-negotiable principles

1. **Evidence first.** A new observation is not a new rule.
2. **Core stays small.** Prefer replacing, merging, deleting, or moving detail to `references/` over appending to `SKILL.md`.
3. **No silent self-modification.** This skill may prepare a candidate diff, but permanent changes must be reviewable in Git and should go through a branch/PR.
4. **Validation before promotion.** A candidate must beat or preserve the baseline on relevant regression cases.
5. **Separate learning layers.** Skill-specific knowledge, agent behavior, and repository/coding knowledge must not be mixed unless the evidence is genuinely cross-cutting.
6. **Reversible evolution.** Every promoted change must retain evidence IDs, evaluation results, and a Git commit/PR reference so it can be rolled back.
7. **Compaction is part of learning.** Successful evolution may reduce the number of core rules.

## Storage model

Runtime learning state lives outside the target Skill by default:

```text
<repo>/.skill-evolution/<target>/
├── state.json
└── archive.jsonl
```

This prevents raw observations from bloating the target Skill. The state file is machine-readable and is managed by `scripts/evolve.py`.

## Decide the target layer first

Use one of these layers:

- `skill`: procedure/domain knowledge belonging to one Skill.
- `agent`: cross-task behavior, routing, delegation, tool-use policy, or stable user operating preferences.
- `repo`: repository-specific coding, CI, test, architecture, data-source, or release knowledge.

Read [references/TARGET_LAYERS.md](references/TARGET_LAYERS.md) when the correct layer is ambiguous.

For durable/automatic use, read [references/INTEGRATION.md](references/INTEGRATION.md). A Skill cannot guarantee self-activation unless the host agent/router invokes it on evidence-worthy events.

## Workflow

### 1. Record evidence, do not edit the Skill yet

For a failure, success, correction, regression, or reusable tactic:

```bash
python skills/skill-refiner/scripts/evolve.py observe \
  --repo-root . \
  --target gc-travel-zine-poster-v1 \
  --layer skill \
  --kind failure \
  --source user \
  --case-id travel-2026-08-08-01 \
  --confidence high \
  --severity high \
  --summary "Vintage was interpreted as dirty yellow grunge" \
  --detail "User rejected yellow/dirty treatment; desired clean editorial vintage."
```

Good evidence contains a concrete case, what happened, and why the outcome was accepted or rejected. Avoid unsupported causal claims.

### 2. Form a candidate only when there is a stable pattern

Create a candidate when at least one of these is true:

- the same failure/tactic appears in **3 independent cases**;
- an authoritative correction is repeated and stable;
- a deterministic rule/code defect is verified directly;
- a repository/tool invariant is demonstrated by tests, CI, source code, or repeated operation.

```bash
python skills/skill-refiner/scripts/evolve.py candidate \
  --repo-root . \
  --target gc-travel-zine-poster-v1 \
  --layer skill \
  --scope reference \
  --target-file references/style-failures.md \
  --title "Separate vintage from dirty/yellow styling" \
  --proposal "Define clean vintage as editorial print texture without mandatory yellow cast or grime." \
  --rationale "Repeated user rejections show the old mapping is not stable." \
  --evidence-ids ev_...
```

For a proven deterministic defect, add `--deterministic-bug`.

### 3. Prefer compression over accumulation

Before writing a patch, ask in order:

1. Can this candidate **replace** a weaker existing rule?
2. Can several old rules be **merged** into one stronger principle?
3. Is this detail only needed sometimes? Move it to `references/`.
4. Can deterministic logic become a script instead of prose?
5. Only then consider a new core rule.

When the patch touches `SKILL.md`, report the estimated net line delta in the candidate with `--core-line-delta`.

The core budget rules are in [references/PROMOTION_POLICY.md](references/PROMOTION_POLICY.md).

### 4. Build a reviewable candidate patch

Inspect the target's current `SKILL.md`, relevant references/scripts, and the evidence attached to the candidate. Make the **smallest** patch that expresses the lesson.

Do not rewrite unrelated sections. Do not weaken explicit user constraints. Do not promote a one-off stylistic preference as a universal rule unless it is clearly scoped.

### 5. Evaluate baseline vs candidate

Use the target's existing tests/evals when available. Otherwise create a small regression set from historical accepted and rejected cases.

Record every evaluation:

```bash
python skills/skill-refiner/scripts/evolve.py evaluate \
  --repo-root . \
  --target gc-travel-zine-poster-v1 \
  --candidate-id cand_... \
  --suite regression \
  --result pass \
  --baseline-score 0.78 \
  --candidate-score 0.91 \
  --regressions 0 \
  --notes "7 historical cases; all must-pass constraints preserved."
```

A qualitative task may use human/agent scoring, but the evaluator must state what was compared and must include old successful cases, not only the new failure.

### 6. Ask the gate for a decision

```bash
python skills/skill-refiner/scripts/evolve.py decision \
  --repo-root . \
  --target gc-travel-zine-poster-v1 \
  --candidate-id cand_...
```

Interpret the result strictly:

- `PROMOTE`: eligible to move into a Git branch/PR.
- `HOLD`: more evidence or evaluation is required.
- `REWORK`: regression, contradiction, or core-bloat issue exists.
- `REJECT`: candidate is contradicted or failed validation.

The script is a gate, not an oracle. If evidence is misclassified, fix the evidence/candidate instead of overriding the result casually.

### 7. Promote through Git

When the decision is `PROMOTE`:

1. create a focused branch;
2. apply only the candidate patch;
3. run relevant tests and Agent Skill format validation where available;
4. inspect the diff for unrelated changes;
5. open a PR containing candidate ID, evidence IDs, baseline/candidate evaluation, and rollback path;
6. merge only after the PR is acceptable.

After merge:

```bash
python skills/skill-refiner/scripts/evolve.py promote \
  --repo-root . \
  --target gc-travel-zine-poster-v1 \
  --candidate-id cand_... \
  --git-ref "PR#123 / abcdef1"
```

### 8. Compact stale learning state

Raw evidence should not stay in the active context forever. Archive old, unlinked observations instead of deleting history:

```bash
python skills/skill-refiner/scripts/evolve.py compact \
  --repo-root . \
  --target gc-travel-zine-poster-v1 \
  --older-than-days 180
```

Archived evidence remains auditable in `archive.jsonl` but is not loaded in normal status/decision work.

## Hard anti-bloat rules

- Never append a core rule solely because a single output was bad.
- Never put raw conversation logs into `SKILL.md`.
- Never copy the evidence ledger into a reference file verbatim.
- Never create a new core rule when an existing rule can be clarified or replaced.
- If `SKILL.md` is already large, core growth must be net-neutral or shrinking unless there is a verified exceptional reason.
- Keep detailed domain cases in focused `references/` files and deterministic operations in `scripts/`.
- Do not load archive history unless investigating a regression or rollback.

## Improving coding agents and repositories

For coding work, record durable repository facts under `layer=repo`: recurring CI failure causes, required validators, fragile modules, invariants, release steps, data-source behavior, or reliable debugging tactics. Promote these into the repository's existing agent instructions, developer docs, tests, or scripts—not into an unrelated domain Skill.

For general agent behavior, use `layer=agent`: routing rules, delegation patterns, stable tool-use policies, and cross-repository operating lessons.

See [references/TARGET_LAYERS.md](references/TARGET_LAYERS.md).

## Required output after a refinement cycle

Report:

- target and layer;
- evidence IDs used;
- candidate ID;
- what was changed or proposed;
- baseline vs candidate validation;
- core size delta;
- gate decision;
- Git PR/commit if promoted;
- what remains unproven.

Do not claim that the underlying model weights improved. The improvement is in persistent procedures, knowledge, tools, tests, routing, and repository intelligence.
