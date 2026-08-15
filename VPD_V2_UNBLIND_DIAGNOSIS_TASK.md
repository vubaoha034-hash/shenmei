# VPD V2 — Unblind Diagnosis Task

Status: `FROZEN_POST_BLIND_TASK`

## Repository / branch

Repository: `vubaoha034-hash/shenmei`

Branch: `visual-program-distillation-v2-photography-design-20260814`

The human blind review was frozen in:

`VPD_V2_HUMAN_BLIND_REVIEW_FREEZE.json`

Freeze commit:

`e875553581994e2519ba806a025192ede72ac63d`

Do not modify, reinterpret, rescore, or replace the frozen blind review after reading the mapping.

---

# OBJECTIVE

Unblind the completed 8-output VPD V2 benchmark only after the human blind judgments have been frozen, then determine whether V2 professional distillation added practical visual value over the DIRECT baseline, where it helped, where it harmed, and what the minimum next experiment should be.

This is a diagnosis task, not a generation task.

Do not generate any new images.
Do not alter the V2 compiler.
Do not add aesthetic rules.
Do not enter Library Scale Gate.
Do not reopen R1E/R1F typography experiments.

---

# PHASE 0 — VERIFY FREEZE

Before reading the private blind mapping:

1. Verify current branch is exactly `visual-program-distillation-v2-photography-design-20260814`.
2. Record current HEAD.
3. Read `VPD_V2_HUMAN_BLIND_REVIEW_FREEZE.json` completely.
4. Verify:
   - `human_review_frozen_before_unblind = true`
   - 8 blind IDs exist exactly once: `VPD2-R01` through `VPD2-R08`
   - `usable_count = 4`
   - `unusable_count = 4`
   - `top_tier_count = 0`
   - `scale_gate_status = NOT_READY_FOR_SCALE`
5. Compute and record the SHA-256 of the frozen review file.
6. Do not read the mapping before steps 1–5 are complete.

If the freeze file is missing, inconsistent, or modified after mapping disclosure, return:

`VPD_V2_UNBLIND_BLOCKED_REVIEW_FREEZE`

and STOP.

---

# PHASE 1 — READ ONLY REQUIRED BENCHMARK EVIDENCE

After freeze verification, read the minimum benchmark evidence required to diagnose conditions:

- private blind mapping created by the benchmark run;
- capsule JSON for Style A and Style B;
- measured evidence sheets;
- causal-priority sheets;
- compiled renderer payload receipts;
- reference/content hashes;
- generation receipts;
- machine-integrity report;
- retry/quarantine receipts if any;
- `VPD_V2_RUNNER.md`;
- `VPD_V2_ACCEPTANCE_PROTOCOL.md`;
- `VPD_V2_HUMAN_BLIND_REVIEW_FREEZE.json`.

Do not read unrelated historical outputs to improve the interpretation.
Do not change any benchmark artifact.

Private file paths/assets must not be copied into public Git beyond the minimum non-sensitive condition mapping and derived diagnosis.

---

# PHASE 2 — UNBLIND EXACTLY ONCE

Resolve each blind ID to exactly one frozen condition:

Style A:
- `A0_DIRECT`
- `A1_V2_RECONSTRUCT`
- `A2_V2_CONTENT_SWAP`
- `A3_V2_COMPOSITION_OR_ASPECT_VARIATION`

Style B:
- `B0_DIRECT`
- `B1_V2_RECONSTRUCT`
- `B2_V2_CONTENT_SWAP`
- `B3_V2_COMPOSITION_OR_ASPECT_VARIATION`

Create an internal mapping table:

`blind_id -> condition -> style -> content asset role -> human blind scores/status`

Do not alter human scores after mapping.

---

# PHASE 3 — DIRECT VS V2 DIAGNOSIS

For each style separately answer:

## 3.1 DIRECT baseline quality

What was the human outcome for A0/B0?

Classify:

- `STRONG_USABLE`
- `USABLE`
- `UNUSABLE`

Do not invent a numerical composite if not needed.

## 3.2 RECONSTRUCT value

Compare A1 vs A0 and B1 vs B0 using the frozen human scores.

Determine whether professional distillation caused:

- `CLEAR_GAIN`
- `SMALL_GAIN`
- `PARITY`
- `SMALL_REGRESSION`
- `CLEAR_REGRESSION`

Explain the change dimension-by-dimension:

- photography;
- graphic design;
- integration;
- material realism;
- typography.

## 3.3 CONTENT_SWAP robustness

Judge A2 and B2 against the corresponding style's quality floor and direct baseline context.

Determine whether the style survived content change without collapsing into:

- generic restaurant-poster tropes;
- literal copying;
- typography degradation;
- photo/design separation;
- material-realism loss.

## 3.4 COMPOSITION / ASPECT robustness

Judge A3 and B3 for whether composition/aspect variation preserved the actual style logic rather than merely changing crop or rearranging generic elements.

---

# PHASE 4 — ROOT-CAUSE ATTRIBUTION

For every meaningful V2 regression, attribute it to one or more of the following ONLY when supported by receipts and visible human-score pattern:

1. `OBSERVATION_ERROR`
   - source visual evidence was described incorrectly or incompletely.

2. `CAUSAL_PRIORITY_ERROR`
   - the analysis captured many true details but selected the wrong high-impact variables for the renderer.

3. `STYLE_CONTENT_BINDING_ERROR`
   - a source/content-specific property was incorrectly promoted as style, or a style property was incorrectly treated as free.

4. `PROMPT_COMPILATION_INTERFERENCE`
   - the distilled payload constrained the strong model in a way that reduced visual quality compared with DIRECT.

5. `REFERENCE_BINDING_ERROR`
   - raw reference or required source pixels were not actually available to the renderer as intended.

6. `RENDERER_CAPABILITY_LIMIT`
   - the renderer itself failed a difficult task despite correct/compact direction.

7. `TYPOGRAPHY_CAPABILITY_LIMIT`
   - image synthesis produced insufficient Chinese display-type quality even when the broader visual direction worked.

8. `PHOTO_DESIGN_INTEGRATION_FAILURE`
   - photography and graphic design were each plausible but did not behave as one composition.

9. `STYLE_FAMILY_EASINESS_BIAS`
   - one style is intrinsically easier for the renderer because strong contrast/tropes can hide weak typography or layout, while a minimal style exposes those weaknesses.

Do not use generic labels such as `needs more polish`.

For each root cause record:

- evidence;
- affected conditions;
- confidence: `HIGH / MEDIUM / LOW`;
- whether it is architectural, compiler-level, renderer-level, or task-level.

---

# PHASE 5 — TEST THE CENTRAL HYPOTHESIS

The benchmark exists to answer:

> Does VPD V2 improve or preserve image quality relative to simply giving the strong visual model the raw reference and a short instruction, while also enabling controlled variation/transfer?

Return exactly one overall verdict:

- `V2_CLEAR_ADVANTAGE`
- `V2_PARTIAL_ADVANTAGE`
- `V2_PARITY_WITH_TRANSFER_VALUE`
- `DIRECT_BASELINE_ADVANTAGE`
- `MIXED_INCONCLUSIVE`

The verdict must be derived from frozen blind judgments after unblinding, not from architecture sophistication.

If DIRECT wins materially on both styles, say so explicitly.
If V2 wins only on the visually easier family, do not generalize that as V2 success.
If V2 reconstructs well but transfer collapses, classify transfer failure honestly.

---

# PHASE 6 — SCALE GATE DECISION

The frozen human review already states:

`NOT_READY_FOR_SCALE`

Therefore this task MUST NOT execute Library Scale Gate.

After diagnosis, set:

`allow_library_scale_gate = false`

unless a new independent human review explicitly supersedes the frozen result in a later task.

Do not reinterpret 4/8 usable as approval to scale.

---

# PHASE 7 — MINIMUM NEXT EXPERIMENT

Do not propose a large redesign.

Based on unblind evidence, define exactly ONE minimum next experiment.

Requirements:

- targets the highest-confidence bottleneck;
- uses the same strong visual model;
- keeps DIRECT baseline;
- generates the smallest number of outputs necessary to falsify the proposed fix;
- does not change multiple architecture layers simultaneously;
- does not bulk-import more reference images;
- does not enter Scale Gate;
- does not revive manual Figma lettering as zero-to-one creation.

Examples of legitimate next-experiment forms, only if supported by the unblind result:

- `PROMPT_COMPILER_ABLATION`: same raw references, compare DIRECT vs current V2 vs V2 with one suspected interfering control removed/reweighted;
- `MINIMAL_STYLE_DIAGNOSTIC`: isolate why the light/minimal family collapses while dark/high-contrast survives;
- `TYPOGRAPHY_RENDERER_BOUNDARY_TEST`: keep photography fixed and test whether typography should be synthesized separately then production-cleaned;
- `CAUSAL_PRIORITY_REWEIGHT_TEST`: retain the same capsule evidence but alter only which 4–10 variables enter the renderer payload.

Do not choose the experiment before reading the mapping.

---

# REQUIRED PUBLIC OUTPUT FILES

Create exactly:

## 1. `VPD_V2_HUMAN_REVIEW_RESULT.json`

Must contain at minimum:

- benchmark id;
- frozen review SHA-256;
- `human_review_frozen_before_unblind: true`;
- blind-to-condition mapping after freeze;
- all eight frozen blind judgments unchanged;
- top-tier / usable / unusable counts;
- per-style DIRECT vs V2 outcome;
- overall verdict;
- `scale_gate_status: NOT_READY_FOR_SCALE`;
- `allow_library_scale_gate: false`;
- diagnosis status.

This file is a human-review receipt, not an aesthetic PASS receipt.
It MUST NOT use an allowed Scale-Gate PASS status.

## 2. `VPD_V2_UNBLIND_DIAGNOSIS.md`

Must include:

- mapping table;
- Style A comparison;
- Style B comparison;
- DIRECT vs V2 conclusion;
- content-swap conclusion;
- composition/aspect conclusion;
- root-cause table with confidence;
- what V2 actually proved;
- what V2 did NOT prove;
- why Scale Gate remains blocked.

## 3. `VPD_V2_NEXT_EXPERIMENT.md`

Exactly one next experiment with:

- hypothesis;
- changed variable(s);
- frozen variables;
- baseline;
- exact output count;
- pass/fail rule;
- stop rule.

No generation in this task.

---

# VALIDATION

Before final response verify:

- frozen blind review file unchanged;
- every blind ID mapped exactly once;
- all 8 human judgments unchanged;
- no new images generated;
- no V2 compiler edits;
- no Scale Gate execution;
- no Discovery changes;
- no private asset leakage into Git;
- working tree clean after committed public diagnosis files;
- `doctor() == []` if available for this project.

---

# FINAL RESPONSE

Return exactly:

# VPD V2 UNBLIND DIAGNOSIS COMPLETE

Branch:
HEAD:
Frozen review SHA:
Mapping resolved:
Human scores changed:
New images generated:
Compiler changed:
Overall verdict:
Scale Gate allowed:
Next experiment:

## 已完成什么

## 未完成什么

## 解盲后最关键结论

## 下一步唯一实验

Then STOP.
