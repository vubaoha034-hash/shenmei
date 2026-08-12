# ADR-003 — Derived Artifacts Are Rebuildable Cache, Not Source Truth

Status: `ACCEPTED_FOR_V0.1`
Date: `2026-08-12`

## Context

PHASE 3 and PHASE 4 deliberately separate irreplaceable raw user evidence from inferred preference intelligence. Future implementations may change retrieval algorithms, embeddings, domain grouping, profile summaries, critic logic, or VisualContextPack construction.

If derived outputs become manually maintained source truth, later algorithm changes would force expensive reconciliation and could permanently preserve old LLM mistakes.

## Decision

All derived preference intelligence is treated as **replaceable, rebuildable cache/projection**.

This includes, when they exist:

```text
EffectiveEvidenceView
ConfirmedGlobalCore
DomainPreferenceSnapshot
AntiPatternSummary
Exemplar rankings/sets
embeddings
clusters
retrieval indexes
calibration compatibility views
Visual DNA presentation summaries
```

Every durable derived artifact must include at least:

```text
artifact_id
artifact_type
built_at
builder_version
source_record_ids
```

Rules:

1. derived artifacts never overwrite raw records;
2. derived artifacts may be deleted wholesale;
3. a full rebuild from raw Sample/Asset/Evidence/Generation records must not require new user labeling;
4. derived summaries must cite source raw IDs;
5. contradictions in raw evidence cannot be silently removed merely to make a clean profile;
6. manual edits to a derived profile do not become personal preference truth; if a human correction reflects real user preference, capture the underlying user evidence instead;
7. no derived artifact is required to exist for basic generation to continue; fallback is current user instruction plus explicitly confirmed/resolvable examples.

## Alternatives Considered

### A. Maintain one authoritative `LIU_VISUAL_DNA.md`

Rejected. It would become a second source of truth and likely accumulate stale or over-generalized rules.

### B. Treat embeddings/vector DB as canonical memory

Rejected. Embeddings are model-dependent derived indexes and must be replaceable.

### C. Manually curate domain profiles as the primary long-term record

Rejected. Manual curation would collapse raw user evidence and interpretation into one irreversible layer.

## Consequences

Positive:

- profile algorithms can be replaced without relabeling;
- bad distillation can be discarded safely;
- model upgrades do not rewrite history;
- auditability is preserved through source IDs.

Negative:

- rebuilding may cost compute later;
- applications must tolerate stale/missing projections;
- profile outputs cannot be casually hand-edited as if they were canonical truth.

## Migration Impact

Any future derived-storage redesign is low-risk if raw IDs and builder provenance are preserved. A derived schema may change completely without raw migration.

## Revisit Trigger

Revisit only if a future derived artifact contains genuinely irreplaceable human work that cannot be represented as raw user evidence. Such a case requires a new ADR rather than silently promoting the artifact to source truth.
