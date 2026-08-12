# ADR-004 — Calibration Is a Derived Compatibility View

Status: `ACCEPTED_FOR_V0.1`
Date: `2026-08-12`

## Context

The repository already contains `calibration/anchors.json` and `personal-aesthetic-critic`, but the current calibration file is still `PERSONAL_CALIBRATION_PENDING` with no anchors. PHASE 3 established a new raw evidence contract that can represent explicit approvals, rejections, comparisons, revisions, and corrections more faithfully than a second manually edited anchor ledger.

Maintaining both systems as independent preference authorities would create drift.

## Decision

`calibration/anchors.json` will become a **derived compatibility projection** from raw visual evidence, not an independent manually maintained source of personal truth.

Rules:

1. raw `SampleRecord + EvidenceEvent` are authoritative for personal preference history;
2. future anchor entries must be materialized from explicit user-confirmed evidence and resolvable visual samples;
3. category mapping required by `personal-aesthetic-critic` is derived and may fail safely;
4. if a raw domain cannot be safely mapped to one of the critic's supported categories, do not force a category; `personal_fit` remains unavailable/null;
5. changing critic categories later must not require rewriting raw evidence;
6. direct manual editing of generated anchors is not the normal learning path;
7. if an anchor must be corrected, capture the underlying user correction in raw evidence and rebuild the compatibility view.

## Alternatives Considered

### A. Keep anchors.json as a second manually curated source of truth

Rejected. Two authorities would eventually disagree.

### B. Delete the existing calibration system and rewrite the critic immediately

Rejected. Existing critic behavior is useful and does not need to be replaced to build personal memory.

### C. Hard-code critic categories into the new raw schema

Rejected. It would reintroduce taxonomy lock-in and make future critic evolution expensive.

## Consequences

Positive:

- existing critic remains usable;
- one authoritative personal evidence source is preserved;
- critic taxonomy can evolve independently;
- corrected user evidence propagates by rebuild instead of manual dual edits.

Negative:

- a projection step is required before formal personal-fit scoring;
- some visual domains may have no official personal-fit score until critic coverage expands.

## Migration Impact

Because current `anchors.json` has no active anchors, the migration cost is currently low. Once implementation begins, new authoritative preference writes must flow into the raw evidence store first.

## Revisit Trigger

Revisit if the critic is replaced entirely or if a future calibration artifact contains human-authored information not already representable in the raw evidence contract.
