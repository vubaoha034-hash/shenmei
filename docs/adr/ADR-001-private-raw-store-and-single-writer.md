# ADR-001 — Private Raw Store and Single-Writer Policy

Status: `ACCEPTED_FOR_V0.1`
Date: `2026-08-12`

## Context

PHASE 3 established four durable raw record families: `SampleRecord`, `AssetRecord`, `EvidenceEvent`, and `GenerationRecord`. The `shenmei` repository is public, while raw personal preference evidence may contain private user feedback, source locations, and visual-history metadata. The system also needs low-friction inspection and future migration without introducing a database before the pilot.

## Decision

V0.1 will use a **private data root outside the public `shenmei` repository** as the canonical raw store.

The logical persistence pattern is:

```text
<private-data-root>/
  samples/       one JSON document per SampleRecord
  assets/        one JSON document per AssetRecord
  generations/   one JSON document per GenerationRecord
  evidence/      append-oriented JSONL EvidenceEvent ledger(s)
```

This ADR decides the persistence *shape*, not the final directory spelling.

Additional rules:

1. every durable record carries `schema_version`;
2. stable IDs from PHASE 3 are independent of storage path;
3. direct user `EvidenceEvent` history is append-oriented and is never silently rewritten;
4. Sample/Asset/Generation metadata may receive deterministic corrections while preserving stable IDs;
5. V0.1 uses **one logical writer at a time** for the raw store;
6. no multi-agent merge protocol, distributed transaction layer, or event bus is introduced;
7. the public repository may contain schemas, fixtures, documentation, and non-sensitive examples later, but not the canonical personal evidence ledger by default;
8. when the first real schema change occurs, add an explicit versioned migration for that change. Do not build a general migration framework in advance.

## Alternatives Considered

### A. Put all raw JSON in the public `shenmei` repository

Rejected. It creates unnecessary privacy exposure and couples personal data retention to public code history.

### B. SQLite as the canonical V0.1 store

Deferred. SQLite would provide atomic querying, but it introduces a binary operational store before the pilot proves a need and makes review/diff of individual evidence less transparent.

### C. Full event sourcing for all four record families

Rejected. Only direct user evidence needs strict append-oriented history. Turning Sample/Asset/Generation metadata into a complete event-sourced model adds complexity without equivalent user value.

### D. Cloud database/object service immediately

Rejected for V0.1. It adds infrastructure before the access pattern and scale are known.

## Consequences

Positive:

- protects private preference history from accidental public Git publication;
- keeps records human-inspectable and portable;
- avoids database lock-in;
- preserves a cheap path to later SQLite/Postgres/object-backed migration because logical IDs remain stable;
- keeps the pilot single-writer and debuggable.

Negative:

- cross-device synchronization is not solved by V0.1;
- concurrent writers are intentionally unsupported;
- later scale may justify consolidating records into a database.

## Migration Impact

A future store migration must preserve:

```text
sample_id
asset_id
event_id
generation_id
schema_version
raw_text
cross-record references
```

Changing from flat files to a database is acceptable and should not require user relabeling.

The catastrophic migration to avoid is changing logical identities or losing raw user evidence.

## Revisit Trigger

Revisit only when at least one is true:

- the pilot requires reliable multi-device synchronization;
- query/update performance becomes a measured bottleneck;
- more than one writer is genuinely required;
- operational durability requirements exceed simple private-file storage.
