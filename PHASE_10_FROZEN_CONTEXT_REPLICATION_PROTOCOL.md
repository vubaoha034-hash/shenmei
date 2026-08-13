# LIU VISUAL SYSTEM — PHASE 10 FROZEN-CONTEXT REPLICATION

Status: `PRE_REGISTERED / NOT_STARTED`
Date: `2026-08-13`
Base: PHASE 9 code HEAD `0a9785ee0336b6697a9e9250af8e3751697a6e0e`

## 0. Purpose

PHASE 9 passed only at the minimum expansion threshold. PHASE 10 exists to test whether that direction replicates on a larger set of new restaurant-design tasks **without changing the personal evidence, retrieval behavior, visual Skills, critic, or prompt strategy after seeing results**.

This phase is deliberately a replication study, not an expansion phase.

The null hypothesis is that Personalized does not beat Baseline more often than chance among non-tie blind choices.

---

## 1. Frozen independent variable

The only allowed condition difference remains:

```text
Baseline
= current task
+ existing router / visual Skill / renderer settings
+ current-task explicit references, if any
+ NO historical Personal Context

Personalized
= the exact same task
+ the exact same router / visual Skill / renderer settings
+ the exact same current-task explicit references, if any
+ bounded restaurant-domain VisualContextPack
```

Everything else must remain matched as closely as the renderer permits.

---

## 2. Frozen personal-context state

Before generating any PHASE 10 output, the real writer host must create a **private replication snapshot** from the canonical store.

The snapshot must record at minimum:

- current discovery sample IDs;
- current effective discovery EvidenceEvent IDs;
- current restaurant-domain ContextPack;
- selected positive exemplar IDs;
- selected negative exemplar IDs;
- `positive_max = 4`;
- `negative_max = 2`;
- a canonical SHA-256 state hash;
- creation timestamp;
- source PHASE 9 final backup reference/hash if available.

The snapshot is private and must not be committed to public Git.

After the snapshot is locked, the following are forbidden until PHASE 10 is scored:

- importing new discovery images;
- adding new approved/rejected feedback;
- changing any existing EvidenceEvent meaning;
- changing sample dataset roles except PHASE 10 blind outputs;
- changing ContextPack selection limits;
- changing retrieval ranking/selection logic;
- changing Router/Skill/Critic/prompt strategy to improve Personalized;
- using PHASE 10 blind results as discovery evidence.

A correction required for data integrity may invalidate the current replication and require a fresh pre-registration rather than an in-place repair.

---

## 3. Task pre-registration

Exactly 20 task briefs are pre-registered in:

`PHASE_10_REPLICATION_TASKS.json`

Rules:

1. all 20 tasks are restaurant-domain tasks;
2. they must be new relative to PHASE 9 blind tasks;
3. task text is frozen before generation;
4. tasks may not be deleted because one condition produced an inconvenient result;
5. if a task is genuinely non-executable, mark it invalid with a concrete reason before user voting; do not replace it after seeing which condition appears better;
6. if fewer than 20 valid pairs remain, PHASE 10 cannot pass and is `INCONCLUSIVE` unless the whole study is invalid.

---

## 4. Pair-generation lock

For each task:

1. resolve the existing repository route/visual Skill exactly once;
2. record renderer/model/aspect ratio/parameters;
3. compile Baseline and Personalized from the same task contract;
4. Personalized may receive only the frozen bounded ContextPack as the additional input;
5. generate each condition exactly once unless the renderer itself returns a technical failure/no image;
6. no manual repair, retouch, regeneration, or selective retry after seeing visual quality;
7. store both outputs as `blind_eval_reserved`;
8. store GenerationRecords and pair lineage privately;
9. lock the pair before presentation.

A technical failure may invalidate one task, but it may not trigger a creative regeneration chosen because the first result was weak.

---

## 5. Anonymous A/B protocol

For every valid pair:

- randomize Baseline/Personalized into presentation A/B;
- keep mapping private;
- filenames/UI must not reveal condition;
- user sees only task brief + image A + image B;
- accepted votes: `A`, `B`, or `tie`;
- vote is locked before unblinding;
- optional user note is preserved verbatim if volunteered;
- blind-case outputs and votes remain excluded from discovery and Skill refinement.

Do not reveal interim aggregate scores before all 20 votes are locked.

---

## 6. Primary replication statistic

PHASE 10 does **not** reuse the weak PHASE 9 `60% / +2` threshold as sufficient proof.

The primary analysis combines the locked PHASE 9 blind result with PHASE 10 non-tie results and calculates a one-sided exact binomial probability under:

```text
H0: P(Personalized win) = 0.5
H1: P(Personalized win) > 0.5
```

PHASE 9 locked result entering the combined analysis:

```text
Personalized wins = 6
Baseline wins = 4
Ties = 0
```

The exact binomial calculation must be implemented using the standard library and recorded in the private result receipt.

---

## 7. Decision rules — pre-registered before PHASE 10 outputs

Possible final results:

```text
REPLICATION_PASS
INCONCLUSIVE
NOT_REPLICATED
INVALID
```

### `INVALID`

If any occurs:

- blind contamination;
- private Git leakage;
- current user instruction overridden by historical memory;
- cross-domain contamination;
- frozen discovery/context state changed after pre-registration without invalidating/restarting;
- condition mapping leaked before votes lock;
- selective creative regeneration/repair breaks pair symmetry.

### `INCONCLUSIVE`

If:

- fewer than 20 valid PHASE 10 pairs; or
- PHASE 10 direction favors Personalized but combined one-sided exact binomial `p > 0.05`; or
- ties/non-ties leave insufficient evidence without reversing direction.

### `NOT_REPLICATED`

If all safety conditions are valid but:

```text
PHASE 10 Personalized wins <= PHASE 10 Baseline wins
```

The original PHASE 9 6:4 result is then not treated as replicated.

### `REPLICATION_PASS`

All must hold:

1. exactly 20 valid PHASE 10 pairs;
2. PHASE 10 Personalized wins > Baseline wins;
3. combined PHASE 9 + PHASE 10 non-tie exact one-sided binomial `p <= 0.05`;
4. no blind contamination;
5. no current-instruction override failure;
6. no cross-domain contamination;
7. no private Git leakage;
8. frozen context snapshot hash unchanged through scoring.

This gate intentionally requires stronger evidence than PHASE 9.

---

## 8. Secondary diagnostics

After all votes are locked and the primary result is computed, report:

- PHASE 10 Personalized/Baseline/tie counts;
- PHASE 10 non-tie Personalized win rate;
- combined PHASE 9 + PHASE 10 counts;
- combined one-sided exact binomial p-value;
- outcome by task category;
- whether any category consistently favors Baseline;
- failure notes for Personalized losses;
- retrieval/context selected for each task;
- any renderer technical failures.

These are diagnostic. Do not rewrite the primary decision threshold after viewing them.

---

## 9. Failure analysis boundary

PHASE 9 Baseline winners (`P9-01`, `P9-06`, `P9-07`, `P9-09`) and any PHASE 10 Baseline winners may be analyzed **only after PHASE 10 scoring is locked**.

Allowed post-hoc hypotheses include:

- exemplar mismatch;
- ContextPack too dominant;
- negative exemplar interference;
- existing Skill already better matched to the task;
- renderer stochastic variance;
- genuine preference mismatch.

Do not convert a post-hoc hypothesis into a production rule automatically.

Any durable Skill change still belongs to the existing `skill-refiner` workflow.

---

## 10. No-expansion rule

Until PHASE 10 final decision is known:

```text
real discovery library size = frozen
restaurant feedback set = frozen
retrieval algorithm = frozen
ContextPack limits = frozen
```

Do not add hundreds of images merely because PHASE 9 passed.

---

## 11. Exit meaning

`REPLICATION_PASS` means the current small restaurant evidence/context system has reproduced a measurable user-preference advantage strongly enough to justify **controlled** expansion.

It does not authorize:

- bulk archive ingestion;
- embeddings/vector DB;
- a trained preference model;
- automatic Skill mutation;
- making every visual domain use restaurant evidence;
- enabling private `personal_fit` without its separate privacy-safe calibration path.

`INCONCLUSIVE` means keep the current data safe and investigate experiment power/task variance before expansion.

`NOT_REPLICATED` means do not expand the evidence library; analyze why the PHASE 9 advantage failed to repeat.
