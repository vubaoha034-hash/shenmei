# LIU VISUAL SYSTEM — PHASE 5 ADR SELF-REVIEW

Status: `PASS / ADR_ONLY`
Date: `2026-08-12`
Branch: `phase-5-adr-20260812`

Scope: review the accepted ADR set for contradictions, accidental over-engineering, migration traps, authority duplication, and PHASE 2/3/4 regressions.

PHASE 5 does not freeze the whole architecture and does not implement production code.

---

# 1. Review question

The ADR set was tested against two questions:

> If one of these decisions is wrong in two years, can we migrate without asking the user to relabel their visual history?

and:

> Did PHASE 5 accidentally freeze implementation details that PHASE 2 explicitly told us to defer?

---

# 2. ADR set under review

```text
ADR-001 private raw store and single writer
ADR-002 asset vault and resolution policy
ADR-003 derived artifacts are rebuildable cache
ADR-004 calibration is a derived compatibility view
ADR-005 runtime context is host-level and bounded
ADR-006 skill-refiner is the only promotion authority
ADR-007 blind-eval reservations are sticky in V0.1
ADR-008 only explicit user evidence enters raw preference ledger
```

---

# 3. Cross-check X-01 — Raw Store vs Asset Vault

Potential conflict:

ADR-001 places raw record metadata in a private data root, while ADR-002 says bulk image bytes live behind a separate Asset Vault boundary.

Decision:

No conflict.

Authoritative interpretation:

```text
private raw store
    = canonical structured metadata/evidence

asset vault
    = durable binary visual bytes
```

They may physically share one private parent directory during the pilot, but they remain logically separate so future image-storage migration does not move/rename preference identities.

Verdict: `PASS`.

---

# 4. Cross-check X-02 — File-based V0.1 persistence is not a permanent database ban

Risk:

ADR-001 could be misread as “flat files forever”.

Clarification:

The accepted decision is:

> V0.1 starts with a private inspectable file-based canonical store and stable logical IDs.

A later SQLite/Postgres/other store is explicitly allowed through a superseding ADR/migration if real operational need appears.

What is long-lived is the record identity/meaning, not the storage engine.

Verdict: `PASS WITH CLARIFICATION`.

---

# 5. Cross-check X-03 — Evidence append-orientation does not turn all data into event sourcing

ADR-001 and PHASE 3 agree:

```text
EvidenceEvent
```

is append-oriented.

Sample/Asset/Generation records do not require a complete event-sourcing framework.

Stable IDs and raw user wording remain protected while deterministic operational metadata can be corrected.

Verdict: `PASS`.

---

# 6. Cross-check X-04 — Explicit evidence policy vs existing calibration

Potential conflict:

The old calibration approach allows manually recorded anchors; ADR-008 admits only explicit user evidence to raw preference truth, and ADR-004 makes calibration derived.

Decision:

This is intentional.

Future formal anchors must originate from explicit user-confirmed evidence and an inspectable/resolvable sample. `anchors.json` cannot invent approval by itself.

This narrows, rather than contradicts, the repository's current rule that a reference is not automatically approved.

Verdict: `PASS`.

---

# 7. Cross-check X-05 — Runtime context vs existing visual Skill authority

Risk:

A host-level VisualContextPack could become an alternate giant design grammar and override the selected visual Skill.

ADR-005 explicitly forbids this.

Context should carry only small task-relevant personal evidence/exemplars/anti-patterns. The existing visual Skill continues to own its visual grammar and prompt compiler.

Current user instruction remains above both.

Verdict: `PASS`.

---

# 8. Cross-check X-06 — Runtime preference projection vs Skill promotion authority

Potential conflict:

A derived profile may influence current generation while `skill-refiner` owns persistent Skill changes.

Decision:

These are separate time horizons:

```text
runtime projection
    = advisory context for this task

skill-refiner promotion
    = durable production procedure change
```

A runtime projection cannot write production Skill files.

Stable repeated evidence may be cited to `skill-refiner`, which then performs its own candidate/evaluation/Git process.

Verdict: `PASS`.

---

# 9. Cross-check X-07 — Blind-eval policy vs learning speed

ADR-007 permanently reserves the V0.1 blind pool rather than releasing it after one evaluation.

Cost:

Some useful examples cannot become discovery data.

Benefit:

No release-state/mutation/audit subsystem is required, and future re-evaluation remains clean.

For a small pilot this is the lower-complexity and lower-contamination choice.

Verdict: `PASS`, with an explicit future revisit trigger rather than premature release machinery.

---

# 10. Cross-check X-08 — Private raw store vs ChatGPT/Codex accessibility

Risk:

A private local raw store may not be reachable by every runtime.

This is not solved by pretending a public repository is a memory database.

ADR-002 requires truthful resolution status. Architecture may operate in degraded mode when raw assets are not resolvable in the current runtime.

A later private synchronized store may supersede local-only persistence without changing IDs.

Verdict: `ACCEPTED LIMITATION`.

---

# 11. Cross-check X-09 — No renderer ADR

PHASE 4 listed renderer behavior as important, but PHASE 5 does not create a renderer-adapter ADR.

Reason:

PHASE 3 already preserves `renderer/model/version` metadata in `GenerationRecord`. Building or selecting an adapter interface now is reversible and low migration cost.

Therefore it does not justify ADR status yet.

Verdict: `CORRECTLY DEFERRED`.

---

# 12. Cross-check X-10 — No taxonomy ADR

No fixed visual-domain taxonomy is accepted.

Reason:

Raw evidence uses free/scoped labels and the existing critic category vocabulary is handled through a derived compatibility mapping.

Taxonomy changes therefore remain cheap.

Verdict: `CORRECTLY DEFERRED`.

---

# 13. Cross-check X-11 — No embedding/vector database ADR

No vector database or embedding model is selected.

Reason:

Simple metadata/exemplar retrieval must fail measurably before semantic infrastructure becomes justified.

Raw IDs and derived-rebuild policy keep this future change cheap.

Verdict: `CORRECTLY DEFERRED`.

---

# 14. Cross-check X-12 — No universal Visual DNA ADR

The ADR set intentionally contains no universal `LIU_VISUAL_DNA` source of truth.

A small global preference core may emerge as a derived artifact and may remain empty.

Verdict: `PASS`.

---

# 15. Migration simulation

Assume V0.1 launches with:

```text
private flat-file metadata
local asset directory
simple exemplar retrieval
existing critic
existing visual Skills
```

Then assume V2 changes to:

```text
private database
cloud object storage
embedding retrieval
new critic categories
new renderer
new host/plugin integration
```

Required migration:

```text
copy structured records preserving stable IDs
move binary assets and rewrite locators
rebuild derived artifacts
rebuild calibration compatibility view
rebuild retrieval indexes
```

Not required:

```text
user relabels images
user repeats A/B decisions
user re-explains old rejections
user reconstructs Before→After history
user recreates correction/retraction history
```

This is the desired migration boundary.

Verdict: `PASS`.

---

# 16. Decisions most expensive to reverse

Ranked roughly by migration/data-cleanup risk:

1. `ADR-008` evidence admission semantics — contaminated raw truth is costly to clean.
2. `ADR-001` raw identity/persistence authority — wrong source-of-truth placement can force relinking.
3. `ADR-004` calibration authority — dual preference truth causes reconciliation debt.
4. `ADR-006` Skill promotion authority — competing lifecycles cause behavioral drift.
5. `ADR-007` evaluation contamination policy — invalid blind evidence cannot be repaired retroactively.
6. `ADR-002` asset/sample separation — path/blob identity mistakes break history during moves.
7. `ADR-005` runtime authority precedence — historical memory overriding current intent harms every task.
8. `ADR-003` derived rebuild policy — making inference canonical creates algorithm lock-in.

All eight are therefore justified as ADR-level decisions.

---

# 17. PHASE 5 exit gate

```text
[PASS] ADR candidates were triaged instead of mechanically copied.
[PASS] Only high migration/authority/data-quality decisions were accepted.
[PASS] Raw personal data is not assigned to the public repository by default.
[PASS] Asset bytes remain decoupled from logical sample identity.
[PASS] Derived intelligence remains rebuildable.
[PASS] Existing calibration cannot become a second manual truth source.
[PASS] Existing visual Skills and router remain reusable.
[PASS] Existing skill-refiner remains sole durable Skill-promotion authority.
[PASS] Blind-eval lifecycle ambiguity has a simple V0.1 decision.
[PASS] Only explicit/traceable user evidence enters raw preference truth.
[PASS] Renderer/taxonomy/embedding details remain deferred.
[PASS] No Skill was created or modified.
[PASS] No production schema/validator/script/scaffold was created.
[PASS] No images were imported.
[PASS] No Architecture Freeze was performed.
```

PHASE 5 verdict:

```text
PASS / ADR ONLY
```

Stop here.

The next phase may use PHASE 3 + PHASE 4 + these ADRs to perform an Architecture Freeze review, but PHASE 5 itself does not freeze or implement the system.
