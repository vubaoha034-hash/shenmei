# Promotion Policy

This policy prevents continual learning from degenerating into continual prompt growth.

## Evidence classes

Strong evidence:

- failing/passing automated test;
- reproducible deterministic defect;
- CI result with identified cause;
- direct source-code invariant;
- repeated authoritative user correction with concrete examples;
- repeated accepted result with the same reusable tactic.

Weak evidence:

- one model guess about why an output failed;
- one-off preference with unclear scope;
- transient tool/network failure;
- an unverified causal story;
- a single example that conflicts with established successful cases.

Weak evidence may be recorded but should not drive promotion alone.

## Default promotion threshold

A normal candidate needs:

- at least 3 independent case IDs linked as evidence;
- no unresolved contradictory evidence;
- at least one passing evaluation;
- zero regressions on must-pass cases;
- a reviewable Git diff.

A deterministic bug may bypass the 3-case threshold only when:

- the defect is directly demonstrated;
- the proposed fix is narrowly scoped;
- relevant regression evaluation passes.

## Core instruction budget

Agent Skills use progressive disclosure. Treat `SKILL.md` as the core activation payload, not as the long-term database.

Rules:

1. Hard stop: never promote a change that would push `SKILL.md` beyond 500 lines.
2. Soft ceiling: above 250 lines, positive core growth requires an explicit reason; prefer net-neutral replacement/merging.
3. For any core addition, first attempt: replace -> merge -> reference -> script -> add.
4. A candidate with positive `core_line_delta` and no explicit evidence-backed reason returns `REWORK` when the target is already above the soft ceiling.
5. Moving detail from core to a focused reference counts as improvement when behavior is preserved.

## Regression policy

The candidate evaluation should contain both:

- target cases: cases that motivated the change;
- preservation cases: older accepted behavior that must not degrade.

Promotion is blocked when `regressions > 0` unless the regression is explicitly judged to be correction of previously wrong behavior and that judgment is documented.

## Conflict policy

When evidence conflicts:

- narrow the rule scope;
- split contexts if they are genuinely different;
- preserve explicit user constraints over inferred preferences;
- prefer conditional rules over contradictory universal rules;
- do not promote until the contradiction is resolved.

## Forgetting / compaction

Active learning state should stay small.

- Unlinked evidence older than the configured retention window may be archived.
- Promoted candidate evidence stays referenced by ID and Git history.
- Rejected candidates remain in state for audit but should not be injected into ordinary task context.
- Archive is for regression investigation, not routine loading.
