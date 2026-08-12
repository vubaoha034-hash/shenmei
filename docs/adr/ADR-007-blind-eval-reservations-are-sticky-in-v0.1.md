# ADR-007 — Blind-Eval Reservations Are Sticky in V0.1

Status: `ACCEPTED_FOR_V0.1`
Date: `2026-08-12`

## Context

PHASE 3 introduced `dataset_role = blind_eval_reserved` as a contamination barrier, but PHASE 4 intentionally left open whether a reserved sample could later be released into preference discovery.

A reversible release mechanism would require additional state/history semantics. V0.1 has a small single-user dataset, so permanent reservation of a small blind set is cheaper than risking ambiguous contamination history.

## Decision

For V0.1, once a sample is assigned:

```text
blind_eval_reserved
```

it remains reserved for the lifetime of that V0.1 evaluation pool.

Rules:

1. reserved samples may be used for their designated blind evaluation;
2. before and after evaluation, they do not enter preference-profile derivation, exemplar discovery, candidate global preferences, prompt/profile tuning, or Skill refinement evidence unless a future ADR explicitly changes the policy;
3. do not casually mutate `dataset_role` from `blind_eval_reserved` to `discovery`;
4. production failures may become regression cases without pretending they were blind-held-out cases;
5. when more evaluation capacity is needed, add new reserved samples instead of recycling old ones;
6. if sample scarcity later becomes a real constraint, design an auditable release manifest/history mechanism in a new ADR.

## Alternatives Considered

### A. Release reserved samples immediately after one blind evaluation

Rejected for V0.1. It makes future re-evaluation and contamination auditing harder and requires release-history semantics not yet present in the minimum contract.

### B. Never use blind evaluation at all

Rejected. Without a contamination barrier the system can easily congratulate itself on examples it already used to derive preferences.

### C. Full TRAIN/DEV/HOLDOUT lifecycle

Rejected. The project is not currently training a model and does not need ML vocabulary or split machinery.

## Consequences

Positive:

- contamination rule is simple and auditable;
- no additional release-event schema is needed;
- future benchmark comparisons retain a clean reserved pool.

Negative:

- reserved images are unavailable for preference discovery;
- the blind pool must grow rather than recycle if new cases are needed.

For V0.1 this cost is intentionally accepted.

## Migration Impact

Changing this policy later requires an explicit ADR and an auditable release mechanism. Historical knowledge that a sample was once reserved must not be erased.

## Revisit Trigger

Revisit only when the reserved pool materially constrains useful learning or a later evaluation design requires rotating release/reassignment with preserved history.
