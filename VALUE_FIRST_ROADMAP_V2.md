# LIU VISUAL SYSTEM — VALUE-FIRST ROADMAP V2

Status: `CONTROLLED_RESTART / VALUE_FIRST`
Date: `2026-08-13`
Base: PHASE 10A repository audit head `a96ac48689e6b98e0439a391aa85d74f8f72e2e3`

## 0. Why this roadmap exists

The project has proven several infrastructure capabilities, but the latest visual outputs exposed a more important failure: the generated images can still fall below the user's real production-quality threshold even when storage, evidence, backup, retrieval and blind-evaluation mechanics are functioning.

Therefore the project is reordered around one governing principle:

> **VALUE BEFORE INFRASTRUCTURE.**

No new scale, automation, evidence expansion or statistical replication is allowed until the shortest real generation chain produces outputs that the user independently considers usable.

This roadmap does not discard the previous Data Contract, private store, backup/restore, evidence ledger or blind quarantine. Those remain reusable infrastructure. It changes the order in which new investment is allowed.

---

# NEW MAINLINE

## G0 — Recovery Freeze

Purpose: stop sunk-cost escalation and establish one canonical recovery point.

Do:
- keep Architecture V0.1, Data Contract, Raw Store, Asset Vault, Backup/Restore and Blind Quarantine;
- keep PHASE 10 Attempt 1 permanently INVALID;
- keep PHASE 10 Attempt 2 PAUSED;
- freeze Discovery at the current PHASE 9 restaurant set;
- record the current critical assumptions.

Do not:
- ingest more images;
- add embeddings/vector DB;
- expand domains;
- modify production visual Skills;
- resume 20-pair blind testing.

Exit gate:
- canonical state documented;
- no hidden expansion work in progress;
- assumption register exists.

---

## G1 — End-to-End Generation Trace Proof

Purpose: prove what actually reaches the renderer.

For at least three existing executions, reconstruct:

```text
Task
→ Router
→ Skill files actually read
→ Compiler output
→ ContextPack
→ selected exemplar IDs
→ resolved asset files + SHA-256
→ final renderer prompt
→ actual image attachments sent to renderer
→ renderer/model/version/parameters
→ output asset
→ quality gate execution
```

Reference binding must be classified exactly as one of:
- `MULTIMODAL_BOUND`
- `PARTIAL_MULTIMODAL_BOUND`
- `TEXT_ONLY_PERSONALIZATION`
- `UNPROVEN_BINDING`

Hard stop:
- anything except `MULTIMODAL_BOUND` blocks personalized quality experiments.

No-generation rule:
- G1 produces no new design images unless required for a minimal trace probe that cannot be obtained from existing receipts.

---

## G2 — Minimal Bridge / Observability Repair

Conditional stage. Execute only if G1 finds a chain defect.

Possible defects:
- reference pixels not attached;
- final prompt not captured;
- route/Skill execution cannot be proven;
- renderer identity/parameters cannot be proven;
- quality gate exists only in documentation but not execution.

Allowed work:
- minimum renderer bridge needed to attach exact reference files;
- generation trace receipt;
- deterministic attachment/asset hash evidence;
- execution status for mandatory hard gates.

Forbidden:
- aesthetic rule expansion;
- new mega Skill;
- new database;
- new retrieval algorithm unless required to fix a proven chain defect.

Exit gate:
- G1 rerun passes with complete traceability and `MULTIMODAL_BOUND` for personalized condition.

---

## G3 — 3×3 Capability Diagnostic

Purpose: identify the actual bottleneck before further investment.

Use exactly three representative restaurant tasks:
1. food/product realism;
2. brand key visual;
3. packaging/layout.

For each task generate once under three conditions:
- **A — Baseline:** current normal chain, no personal context;
- **B — Personalized:** same chain + proven multimodal-bound personal references;
- **C — Expert Direct:** same renderer, but bypass the current restaurant Prompt Compiler; use a pre-locked direct prompt with only 5–8 high-leverage imageable variables and no personal context.

Total: 9 images.

For each image the user must independently mark:
- `USABLE`
- `UNUSABLE`

Then rank the three conditions per task.

Interpretation:
- `C >>> B > A` → Prompt Compiler / Skill execution bottleneck likely;
- `B ≈ C >>> A` → personalization transmission likely working;
- `A ≈ B ≈ C`, mostly unusable → renderer/model bottleneck likely;
- `C usable, A/B unusable` → current Skill/Prompt Compiler chain blocks quality;
- B worse than A despite valid binding → retrieval/reference-conditioning problem likely.

Hard stop:
- do not proceed to broad blind testing if all three conditions remain below the absolute quality floor.

---

## G4 — Absolute Quality Floor Confirmation

Purpose: prove the chosen generation chain can repeatedly produce work worth continuing to invest in.

Prerequisite:
- G3 identifies a plausible working chain and any required minimal repair is complete.

Run a small representative set of new restaurant tasks using the chosen chain.

Primary metric:
- user-independent `USABLE / UNUSABLE` judgment for each output.

Recommended initial confirmation set:
- 8 tasks across food realism, key visual, promotion, packaging and store/social.

Pre-registered pass suggestion:
- at least 6/8 outputs `USABLE`;
- zero systemic fake-food failure;
- zero repeated generic-template collapse;
- zero reference-binding failure;
- no current-task instruction overridden by history.

If this gate fails:
- stop and diagnose the generation chain again;
- do not compensate by importing more preference images.

---

## G5 — Relative Personalization Proof

Purpose: only after absolute quality exists, test whether personal memory adds value.

Design:
- matched Baseline vs Personalized pairs;
- both conditions must use the already quality-capable chain;
- record pairwise A/B/tie and absolute `USABLE / UNUSABLE` separately.

Important:
- a Personalized pairwise win where both images are `UNUSABLE` is not product success.

Pass requires both:
1. relative preference advantage;
2. acceptable absolute usable rate.

Do not use pairwise win rate alone as a success claim.

---

## G6 — Replication

Purpose: verify that G5 was not a small-sample accident.

Only now run a larger frozen-context replication.

Requirements:
- new tasks;
- frozen evidence/context;
- pre-registered statistics;
- blind-safe generation path;
- absolute quality labels retained alongside relative votes.

Replication cannot rescue a failed G4 absolute-quality gate.

---

## G7 — Controlled Evidence Expansion

Purpose: expand only after the system has demonstrated usable outputs and reproducible personalization value.

Allowed:
- small batches of new approved/rejected references;
- only explicit user evidence;
- domain/subtask coverage gaps identified from real failures.

Do not bulk ingest hundreds or thousands of images.

Every expansion batch must answer:
- what specific missing capability does this evidence add?
- how will we know it improved the system?

---

## G8 — Task-Aware Retrieval / Derived Intelligence

Conditional stage. Build only if controlled evidence shows domain-only retrieval is too coarse.

Possible task classes:
- food photography;
- brand key visual;
- promotion poster;
- menu/packaging;
- storefront/social system.

Raw evidence remains unchanged. Task-aware labels/rankings are derived and rebuildable.

Do not introduce embeddings/vector DB unless metadata/task-aware retrieval is measurably insufficient.

---

## G9 — Scale and Automation

Only after G4–G6 pass.

Possible later work:
- larger evidence library;
- embeddings/vector DB if justified;
- automation;
- new domains;
- performance optimization;
- richer calibration projection.

No infrastructure is authorized merely because it is technically interesting.

---

# PERMANENT PROJECT RULES

## Rule 1 — Absolute quality outranks relative improvement

`Personalized > Baseline` does not mean success if both are unusable.

## Rule 2 — Unobservable chain = unproven chain

If we cannot prove what reached the renderer, we cannot use that execution as evidence that personalization worked.

## Rule 3 — Core value before scale

No database, vector search, bulk ingestion or large benchmark before the generation chain itself passes the quality floor.

## Rule 4 — Existing rule ≠ executed rule

Hard gates must record `DEFINED / EXECUTED / RESULT`.

## Rule 5 — Do not solve taste failure by rule bloat

If outputs become generic/template-like, inspect route, compiler, reference binding and renderer first. Do not automatically add more aesthetic prohibitions.

## Rule 6 — Sunk cost gives no permission to continue

Any core assumption may stop the roadmap regardless of phase number or previous effort.

## Rule 7 — Every stage must reduce a critical uncertainty

If a stage does not increase real user value or reduce a high-risk unknown, do not build it.

---

# CURRENT ORDER OF EXECUTION

The next executable sequence is now:

```text
G0 Recovery Freeze
→ G1 Generation Trace Proof
→ if needed G2 Minimal Bridge Repair
→ G3 3×3 Capability Diagnostic
→ G4 Absolute Quality Floor Confirmation
→ G5 Relative Personalization Proof
→ G6 Replication
→ G7 Controlled Expansion
→ G8 Task-Aware Retrieval (only if justified)
→ G9 Scale / Automation
```

No later gate may be pulled forward for convenience.