# VPD V2 Acceptance Protocol

Status: `FROZEN_FOR_FIRST_BENCHMARK`

## 1. Purpose

Determine whether VPD V2 actually improves visual-program distillation rather than merely increasing schema detail.

The benchmark must prove three things independently:

1. `DECOMPOSITION_VALIDITY` — the distilled description captures the image-making factors that matter;
2. `GENERATION_VALUE` — using the distilled program with the same strong visual model does not degrade quality versus direct reference use;
3. `TRANSFER_VALUE` — the program can make a new work in the same family without literal copying.

## 2. Benchmark references

Use two materially different, absolutely usable references.

For the first benchmark:

- Style A: commercial high-impact restaurant reference (Reference 05);
- Style B: editorial restrained restaurant reference (Reference 13).

The same compiler architecture must be used for both.

No compiler rule may be changed after seeing Style A results and before Style B distillation.

## 3. Controlled conditions

For each style, use the same underlying strong visual model.

Required outputs:

### B0 DIRECT

`raw reference pixels + source/content asset + short human instruction -> strong visual model`

This is the permanent direct-reference baseline.

### V2-R RECONSTRUCT

`V2 anchors + compiled V2 high-impact controls -> strong visual model`

Purpose: verify the capsule understands the source family.

### V2-C CONTENT_SWAP

Use a genuinely different content asset while preserving family logic.

### V2-A ASPECT_OR_COMPOSITION_TRANSFER

Use either a materially different aspect ratio or composition arrangement, chosen before generation.

Total primary outputs: exactly 4 per style, 8 total.

No best-of-N or hidden retries.

One targeted regeneration is allowed only for deterministic integrity failure or renderer instruction violation, and must be logged as invalidating the first attempt rather than silently replacing it.

## 4. Decomposition audit

Before generation, independently inspect each capsule.

### Photography audit

Confirm it contains evidence-backed coverage of:

- capture geometry;
- focus/optics;
- lighting;
- exposure/tonality;
- color grade;
- texture/sharpness;
- subject styling;
- post-processing.

Fields irrelevant to the source may be explicitly marked `NOT_MATERIAL` rather than filled with invented detail.

### Design audit

Confirm evidence-backed coverage of:

- semantic intent;
- attention hierarchy;
- grid/geometry;
- typography/lettering;
- copy meaning;
- whitespace/density;
- color system;
- graphic language;
- layer/crop/edge;
- material/print;
- sequence/system when applicable.

### Integration audit

Confirm the capsule explains how photography and design interact.

Any missing critical subsystem -> `DISTILLATION_DEPTH_FAIL` before generation.

## 5. Visual evaluation

Every primary output receives independent human review at three scales.

### Thumbnail review

Judge:

- immediate hierarchy;
- dominant mass;
- color rhythm;
- family recognition;
- template/generic collapse.

### Normal-view review

Judge photography:

- framing/perspective;
- light quality;
- tonal structure;
- color relationship;
- focus/DOF;
- subject/material realism;
- styling.

Judge design:

- message;
- hierarchy;
- grid/optical balance;
- typography quality;
- copy-image relationship;
- whitespace function;
- graphic-language coherence.

### Detail review

Judge:

- microtexture;
- specular behavior;
- edges;
- sharpening/clarity;
- cloned/repeated detail;
- local retouch artifacts;
- glyph/lettering quality;
- print/material cues.

## 6. Absolute quality

Every output receives:

- `USABLE`
- `UNUSABLE`

No pairwise win can override `UNUSABLE`.

Relative improvement is recorded separately.

## 7. Direct-baseline gate

For each style compare B0 DIRECT against the V2 outputs.

V2 does not need to beat B0 on every dimension.

But promotion fails if:

- V2 outputs are consistently less usable than B0;
- V2 adds generic/template artifacts not present in B0;
- V2 destroys photographic realism;
- V2 typography/design becomes weaker due to overconstraint.

Failure code:

`RULE_INTERFERENCE_V2`

## 8. Family/non-copy gate

V2-C and V2-A must satisfy both:

1. recognizable family relationship;
2. no literal copying of brand identity, exact layout coordinates, unique illustrations, or source-specific motifs.

Failures:

- `OVERFIT_COPY_V2`
- `FAMILY_COLLAPSE_V2`

## 9. Second-style gate

Style B must be distilled without editing the V2 compiler.

If V2 only works after adding Style-B-specific global rules:

`COMPILER_NOT_STYLE_GENERAL`

## 10. Photography-specific hard failures

For real-food/product tests, any of the following is a major failure:

- waxy/plastic uniform surface;
- cloned ingredient/features;
- impossible contact/shadow;
- fake smoke/steam structure;
- over-sharpened halos;
- crushed or synthetic tonal rolloff;
- inaccurate material response;
- color grade that damages food/material plausibility.

## 11. Design-specific hard failures

Any of the following is a major failure:

- stock-font look when source quality depends on custom lettering;
- image plus unrelated decorative geometry;
- empty whitespace with no hierarchy function;
- generic center-poster template;
- copied source brand/identity;
- mechanically literal interpretation of abstract grammar;
- type and image behaving as unrelated layers;
- decoration added only to fill space.

## 12. Promotion criteria

VPD V2 may move from `EXPERIMENTAL` to `CANDIDATE` only if:

- both style capsules pass decomposition-depth audit;
- at least one non-direct V2 output per style is `USABLE`;
- each style demonstrates one usable changed-content/composition result;
- no direct-baseline systematic regression is observed;
- no literal-copy failure;
- Style B required no compiler rewrite;
- user confirms at least one V2 output in each style family is genuinely worth continuing.

This is deliberately strict.

## 13. Outcome states

- `VPD_V2_PASS_TO_CANDIDATE`
- `VPD_V2_FAIL_DECOMPOSITION_DEPTH`
- `VPD_V2_FAIL_RULE_INTERFERENCE`
- `VPD_V2_FAIL_RENDERER_CAPABILITY`
- `VPD_V2_FAIL_OVERFIT_COPY`
- `VPD_V2_FAIL_STYLE_GENERALIZATION`
- `VPD_V2_BLOCKED_INPUTS`

## 14. Boundary

Do not bulk-distill the approved library before this benchmark passes.

Do not use benchmark success to claim model-weight learning.

Do not merge V2 into production solely because the schema validates.
