# LIU VISUAL SYSTEM — G3 3×3 CAPABILITY DIAGNOSTIC

Status: `PRE_REGISTERED / NOT_STARTED`
Date: `2026-08-13`
Base G2 PASS commit: `d2ecc48c4d0fd3fa80b57f9ae7309123a751a3b8`

## Purpose

G3 identifies the dominant quality bottleneck **before** any larger personalization or replication study.

This is a capability diagnostic, not a benchmark and not a scale stage.

Exactly three restaurant tasks are tested under exactly three generation conditions:

- `A — Baseline`
- `B — Personalized`
- `C — Expert Direct`

Total planned outputs: **9**.

No output may be regenerated merely because it is ugly or below the quality floor.

---

## 1. Preconditions

G3 may start only if all are true:

- G2 = `G2_PASS`;
- remote base commit is exactly `d2ecc48c4d0fd3fa80b57f9ae7309123a751a3b8`;
- Discovery remains frozen at approved 18 / rejected 12;
- Personal Context remains restaurant domain, positive max 4 / negative max 2;
- Personalized reference binding is `MULTIMODAL_BOUND`;
- positive references are direct independent attachments;
- rejected references are not silently used as positive image conditioning;
- prompt preservation gate is active;
- renderer receipt contract is active;
- independent Google Drive pixel-review path is available;
- PHASE 10 Attempt 2 remains paused.

Any failed precondition blocks G3.

---

## 2. Frozen tasks

Use exactly `G3_DIAGNOSTIC_TASKS.json`.

There are three diagnostic axes:

1. food/product realism;
2. brand key visual design;
3. packaging/graphic-system design.

Task wording must not be changed after the first prompt/request hash is locked.

---

## 3. Conditions

### A — Baseline

Use:

- current task;
- current correct route;
- current existing restaurant Skill / Prompt Compiler;
- G2 prompt-preservation invariants;
- same renderer boundary and comparable exposed parameters;
- **no historical Personal Context**.

### B — Personalized

Identical to A except:

- add the frozen bounded restaurant Personal Context;
- positive exemplars are direct independent multimodal attachments;
- rejected exemplars stay upstream-only / negative-constraint evidence unless the provider explicitly supports negative image conditioning.

No additional manual beautification is allowed.

### C — Expert Direct

Use:

- the same task;
- the same renderer boundary and comparable exposed parameters;
- **no Personal Context**;
- bypass the current restaurant Prompt Compiler;
- create a concise direct image prompt using only 5–8 high-leverage, imageable variables plus mandatory correctness/realism constraints.

The Expert Direct prompt must not default to generic terms such as `Chinese ink`, `brush stroke`, `red seal`, `Zen`, or `traditional premium` unless the task itself requires them.

Expert Direct exists only for diagnosis. It is not a new production Skill.

---

## 4. Pre-render lock

Before rendering the first G3 image:

For all 3 tasks and all 3 conditions:

- compile/finalize request inputs;
- record prompt SHA-256;
- record reference attachment identities;
- record route and Skill blob SHA where applicable;
- record exposed renderer/tool parameters;
- create a private random mapping from conditions to presentation labels `X/Y/Z` for each task;
- create a private randomized render order.

No prompt, reference set, mapping, or task text may change after any output is seen.

---

## 5. One-shot symmetry

Each of the 9 conditions is rendered exactly once.

Forbidden:

- best-of-N;
- selective retry;
- selective repair;
- manual retouch;
- re-prompting because the result is ugly;
- generating more alternatives for one condition;
- weakening Baseline;
- adding hidden creative help only to Personalized.

A true renderer failure means no usable image bytes were returned. Record it as technical failure; do not treat bad visual quality as technical failure.

---

## 6. Quality-gate behavior

Every output must run through:

1. Machine Integrity Gate;
2. Independent Real Pixel Visual Gate.

The independent reviewer must inspect the actual Drive image bytes, not a text description.

Pixel-review result:

- `PASS_FOR_USER_REVIEW`
- `REJECTED_BELOW_FLOOR`

A rejected image is **not regenerated**. It remains a diagnostic failure sample and may still be included anonymously for user judgment.

The independent review result must remain hidden from the user until the user's X/Y/Z judgments are locked, so it cannot bias ranking.

---

## 7. User judgment

For each anonymous task trio, the user sees only:

- Task ID and brief;
- Image X;
- Image Y;
- Image Z.

No condition labels, prompts, reference roles, or running scores are shown.

For every image, the user records:

- `USABLE`
- `UNUSABLE`

Definition of `USABLE`:

> The core visual concept is good enough that it could plausibly enter a real project without redesigning the concept from scratch. Minor production cleanup is allowed; fundamental composition, food realism, material language or design-system replacement is not.

Then the user ranks the three images:

- 1st
- 2nd
- 3rd

All judgments lock before unblinding.

---

## 8. Unblinding and interpretation

After all user judgments are locked, reveal X/Y/Z mapping and combine with the independent Pixel Gate.

Primary diagnostic patterns:

- `C >>> B > A` → Prompt Compiler / Skill execution bottleneck likely;
- `B ≈ C >>> A` → Personal Context transmission likely working;
- `A ≈ B ≈ C`, mostly unusable → renderer/model bottleneck likely;
- `C usable, A/B unusable` → current Skill / Prompt Compiler chain likely blocks quality;
- `B worse than A` despite valid direct binding → reference selection / conditioning likely harmful;
- task-specific divergence → likely multiple bottlenecks.

G3 does not estimate statistical significance.

---

## 9. G3 decisions

Allowed final decisions:

- `G3_PROMPT_COMPILER_BOTTLENECK`
- `G3_RENDERER_BOTTLENECK`
- `G3_PERSONALIZATION_BINDING_WORKS`
- `G3_REFERENCE_CONDITIONING_HARMFUL`
- `G3_MULTIPLE_BOTTLENECKS`
- `G3_INCONCLUSIVE`
- `G3_CAPABILITY_PATH_IDENTIFIED`

`G3_CAPABILITY_PATH_IDENTIFIED` means at least one chain shows credible absolute quality worth taking to G4; it does not mean the whole system is production-ready.

---

## 10. Stop rule

After G3 scoring:

- stop;
- do not resume PHASE 10 Attempt 2;
- do not bulk-ingest images;
- do not start embeddings/vector DB;
- do not automatically modify Skills;
- do not start G4 until the G3 result is independently reviewed.
