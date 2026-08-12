# ADR-006 — `skill-refiner` Is the Only Durable Skill-Promotion Authority

Status: `ACCEPTED_FOR_V0.1`
Date: `2026-08-12`

## Context

PHASE 2 found that the repository already has an evidence-gated `skill-refiner` workflow and has previously suffered from rule-bloat in visual Skills. A new visual distillation subsystem with its own candidate/active/deprecated lifecycle would duplicate authority and create drift.

## Decision

The existing `skill-refiner` remains the **single authority for durable production Skill changes** derived from repeated visual evidence.

Rules:

1. raw user feedback is never a direct Skill edit;
2. derived preference projections may influence current runtime context but may not modify production Skills;
3. repeated stable evidence may be handed to `skill-refiner` by citing raw visual `event_id` values;
4. candidate formation follows existing evidence thresholds/gates;
5. promotion requires relevant baseline/regression evaluation and reviewable Git change;
6. no automatic LLM promotion is allowed;
7. no parallel `visual-distill` promotion ledger is created;
8. if a lesson only improves retrieval/profile behavior and does not belong in a Skill, it stays in the derived layer rather than being promoted merely because it is stable.

## Alternatives Considered

### A. Create a dedicated visual rule lifecycle

Rejected. It would create two candidate/promotion authorities.

### B. Automatically rewrite Skills after strong user feedback

Rejected. One-off or misinterpreted feedback could self-amplify into permanent behavior.

### C. Never modify Skills from personal evidence

Rejected as too rigid. Some repeated failures may reveal real reusable procedure defects, but they must pass the existing promotion workflow.

## Consequences

Positive:

- one reviewable evolution mechanism;
- existing anti-bloat policy remains effective;
- personal evidence and production procedure remain separated;
- failed candidates cannot corrupt raw preference history.

Negative:

- durable Skill improvement is slower than automatic self-modification;
- bridge logic must translate relevant visual evidence IDs into `skill-refiner` observations without losing provenance.

## Migration Impact

Future replacement of `skill-refiner` requires an explicit ADR because it changes production-rule authority. Raw visual evidence remains independent and must survive such a replacement.

## Revisit Trigger

Revisit only if `skill-refiner` can no longer express required validation/promotion workflows or becomes deprecated by a demonstrably better repository-wide authority.
