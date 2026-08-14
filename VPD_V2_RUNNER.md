# VPD V2 Controlled Benchmark Runner

Status: `FROZEN_FOR_FIRST_VISUAL_BENCHMARK`

## 1. Objective

Test whether professional photography/design distillation creates practical visual value beyond direct raw-reference prompting.

Do not treat this benchmark as a production workflow.

## 2. Required inputs

Read only the VPD V2 architecture files and the specific benchmark assets/metadata required by this runner.

Required architecture:

- `VPD_V2_DESIGN_SPEC_DRAFT.md`
- `VISUAL_DISTILLATION_COMPILER_CONTRACT_V2.md`
- `VPD_V2_MEASUREMENT_AND_CAUSAL_SPEC.md`
- `schemas/visual-program.v2.schema.json`
- `VPD_V2_ACCEPTANCE_PROTOCOL.md`
- `VPD_V2_SELF_REVIEW_CHECKLIST.md`
- `VPD_V2_EXTERNAL_SKILL_AUDIT.md`
- `AESTHETIC_SKILL_DESIGN_CHARTER.md`

## 3. Styles

Use two materially different absolutely-usable reference styles:

- Style A: R1C-APPROVED-05
- Style B: R1C-APPROVED-13

Use raw canonical pixels, not contact sheets or text summaries.

Do not edit the V2 compiler architecture between A and B.

## 4. Content assets

Use real non-generated content assets from the private Asset Vault.

For each style identify:

- CONTENT-1: source/reconstruction content;
- CONTENT-2: genuinely different content for content-swap;
- CONTENT-3: content suitable for composition/aspect variation if needed.

If sufficiently different real content assets cannot be resolved, stop:

`VPD_V2_BLOCKED_INPUTS`

Do not fabricate transfer evidence with tiny crop changes of the same image.

## 5. Capsule authoring

Create exactly two V2 capsules, one per style.

Each capsule must:

- validate against `visual-program.v2.schema.json`;
- contain measured/direct evidence;
- separate inference;
- contain causal quality hypotheses;
- contain causal priority map;
- identify style/content/brand/production binding;
- preserve raw pixel anchors;
- compile a thin renderer payload.

If a critical subsystem is irrelevant, explicitly mark it not material in the authored analysis rather than inventing detail.

## 6. Pre-render review

Before generation, run the photographer/designer/art-director checklist.

Fail closed on:

- vague adjective-only critical fields;
- unsupported exact camera settings;
- generic typography description when custom type matters;
- missing photo/design integration;
- renderer prompt bloat;
- missing raw pixel anchor binding.

## 7. Renderer

Use the strongest available visual generation/editing model as the creative renderer.

The renderer receives:

- actual reference pixels;
- actual source/content asset;
- compact V2 art direction;
- explicit freedoms;
- short relevant avoid list.

Do not use Figma/Codex/SVG path construction as the zero-to-one creative renderer.

## 8. Required primary outputs

Exactly 8 primary outputs.

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

No best-of-N.
No hidden extra batch.
No cosmetic retry because the result is ugly.

A deterministic integrity/tool failure may be retried only if the failed output is quarantined and the retry is logged.

## 9. Direct baseline

`A0_DIRECT` and `B0_DIRECT` must use:

- the same underlying strong visual model;
- raw reference pixels;
- corresponding content asset;
- short human-like instruction only.

Do not add V2 distilled variables to direct baseline.

This preserves the workflow that historically performs well when a reference is simply attached.

## 10. Drive review package

Upload the 8 primary outputs with neutral/blind labels to one review folder.

Save the mapping privately.

Also save:

- capsule JSONs;
- schema validation receipts;
- compiled renderer payload receipts;
- source/reference hashes;
- generation receipts;
- machine integrity report.

Do not expose condition names on the images during user review.

## 11. Independent pixel review

Codex may check machine integrity but may not judge aesthetic PASS.

Final review must inspect actual pixels at:

- thumbnail scale;
- normal view;
- detail view.

Review photography, design and integration separately.

User absolute `USABLE / UNUSABLE` is required.

## 12. Acceptance

Use `VPD_V2_ACCEPTANCE_PROTOCOL.md` exactly.

V2 fails if complexity consistently produces worse images than direct baseline.

Do not respond to failure by adding rules immediately.

First identify whether failure came from:

- wrong observation;
- wrong causal priority;
- bad transfer classification;
- prompt compilation interference;
- renderer capability;
- source/reference mismatch.

## 13. Final status

Return one of:

- `VPD_V2_BENCHMARK_READY_FOR_HUMAN_REVIEW`
- `VPD_V2_BLOCKED_INPUTS`
- `VPD_V2_DISTILLATION_NOT_READY`
- `VPD_V2_TECHNICAL_FAILURE`

Do not declare `VPD_V2_PASS_TO_CANDIDATE` before independent human review.
