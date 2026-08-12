# ADR-002 — Asset Vault and Resolution Policy

Status: `ACCEPTED_FOR_V0.1`
Date: `2026-08-12`

## Context

Visual preference evidence depends on actual images, but ChatGPT, Codex/local environments, GitHub, and future runtimes do not necessarily share one filesystem. PHASE 3 also separated logical `SampleRecord` identity from exact `AssetRecord` blobs.

## Decision

Bulk visual bytes are stored **outside the public Git repository by default** behind a conceptual `Asset Vault` boundary.

V0.1 does not select a universal cloud object store.

An `AssetRecord` preserves:

```text
asset_id
sample_id
sha256
locator_kind
locator
asset_relation
```

Operational rules:

1. `sample_id` never depends on asset location;
2. `asset_id` identifies one exact blob; if bytes change, create a new AssetRecord;
3. `locator_kind` / `locator` may change when the same exact blob moves;
4. SHA-256 verifies exact blob identity only;
5. Git may hold small canonical fixtures, never the default bulk warehouse;
6. each runtime must resolve selected assets before claiming to have visually inspected them;
7. runtime state distinguishes `known`, `selected`, `resolvable`, and `actually inspected` samples;
8. if an asset is unavailable, preserve the historical preference evidence and degrade honestly rather than fabricating inspection;
9. object-store-specific fields (`s3`, `r2`, `gcs`, etc.) are not part of the V0.1 contract.

## Alternatives Considered

### A. Store every image in Git/Git LFS

Rejected as the default. It couples a growing private visual archive to repository history and does not solve runtime accessibility uniformly.

### B. Choose S3/R2/GCS now

Deferred. No measured need justifies an object-storage dependency yet.

### C. Store only textual descriptions and discard images

Rejected. Actual exemplars are first-class personal preference evidence and cannot be reconstructed reliably from descriptions.

## Consequences

Positive:

- storage can change without changing logical sample identity;
- large binary growth does not bloat the code repository;
- host-specific access failures do not corrupt preference truth;
- future object storage remains possible.

Negative:

- some runtimes may not be able to inspect all references initially;
- the pilot needs explicit asset-resolution checks;
- portability requires preserving both metadata and actual asset bytes somewhere durable.

## Migration Impact

A storage migration may rewrite locators but must not rewrite `sample_id`, user EvidenceEvents, or preference relationships.

A copied/recompressed image with changed bytes becomes a new `asset_id`; whether it maps to the same logical `sample_id` remains a controlled ingestion decision.

## Revisit Trigger

Revisit when cross-runtime asset unavailability becomes a material blocker or when local/private storage no longer scales operationally.
