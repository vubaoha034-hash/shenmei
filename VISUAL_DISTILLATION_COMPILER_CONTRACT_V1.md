# Visual Distillation Compiler Contract V1

Status: `FROZEN_FOR_VPD_V1_BENCHMARK`
Compiler id: `visual-distillation-compiler-v1`

## 1. Input contract

The compiler accepts:

- one canonical visual reference, or a deliberately coherent reference set of at most 3 images;
- raw pixels for every reference;
- provenance/hash metadata;
- domain/task context;
- optional explicit user feedback tied to the reference;
- optional cross-style personal priors already supported by independent evidence.

The compiler must reject:

- references marked `RELATIVE_ONLY` as positive source anchors;
- mixed unrelated styles silently combined into one capsule;
- references whose raw pixels cannot be resolved;
- source sets where the compiler cannot explain why the images belong to one visual family.

## 2. Step 1 — Observe pixels before interpretation

Produce an `Observed Evidence` worksheet.

Only record directly visible properties:

- frame/aspect ratio;
- subject scale and position;
- dominant masses;
- negative-space regions;
- hierarchy order;
- edge/crop behavior;
- color distribution and role;
- contrast structure;
- material/lighting behavior;
- typography location, scale, weight, irregularity and interaction with imagery;
- motif/icon/illustration placement;
- texture/printing/photographic treatment.

Do not write style adjectives at this stage.

Forbidden examples:

- premium;
- artistic;
- young;
- oriental;
- emotional.

## 3. Step 2 — Infer generative relationships

Convert observed evidence into relationships that could create a new work.

Every inferred mechanism must cite one or more observed evidence items.

Examples:

Observed:

`display title overlaps the upper edge of the product mass`

Mechanism:

`type and product are composed as interacting masses, not separate header and image blocks`

Observed:

`small red marks appear only near heat/ingredient zones`

Mechanism:

`accent marks are semantically bound to the product process rather than decorative`

If a mechanism cannot be traced back to visible evidence, mark it `INFERENCE_LOW_CONFIDENCE` and do not make it a fixed invariant.

## 4. Step 3 — Split invariant vs freedom

For every major mechanism decide:

- `FIXED_INVARIANT`
- `DEGREE_OF_FREEDOM`
- `SOURCE_SPECIFIC_DO_NOT_TRANSFER`

### Fixed invariant

A relationship required for family identity.

Examples:

- image/type interlock;
- asymmetrical visual mass;
- semantic motif derivation;
- high material realism.

### Degree of freedom

A variable that can change while preserving family identity.

Examples:

- accent hue;
- product identity;
- crop direction;
- copy wording;
- motif source derived from new product.

### Source-specific do-not-transfer

Elements belonging only to the original work.

Examples:

- original logo;
- exact slogan;
- exact illustration character;
- exact chili shape;
- exact paper tear;
- exact layout coordinates.

This classification is mandatory. Without it the capsule is either vague or a cloning recipe.

## 5. Step 4 — Build transformation operators

Every capsule must define at least:

- `CONTENT_SWAP`
- `ASPECT_ADAPT`
- `MOTIF_REBIND`
- `TYPOGRAPHY_REBIND`

and at least two of:

- `PALETTE_SHIFT`
- `DENSITY_SHIFT`
- `MATERIAL_SHIFT`

Each operator must contain:

- what may change;
- what must remain;
- what would break the family.

Operators must be executable instructions, not descriptive prose.

Bad:

`keep it high-end while changing the product`

Good:

`replace the main product while retaining the lower-field dominant mass and image/type interlock; derive supporting marks from the new product/process; do not preserve the source ingredient silhouettes`

## 6. Step 5 — Preserve visual anchors

The capsule must retain actual visual evidence.

Required:

- full canonical reference anchor.

Optional:

- typography crop;
- composition crop;
- material/texture crop;
- color/lighting crop.

Diagnostic crops must be source-derived and hash/provenance traceable.

The compiler must not create synthetic anchor images during distillation.

## 7. Step 6 — Build failure boundaries

Use three evidence sources:

1. obvious generic collapses for this visual family;
2. user's rejected examples relevant to this mechanism;
3. prior generated failures from the same task family.

Failure boundaries must be specific enough to evaluate after generation.

Bad:

`avoid ugly AI look`

Good:

`reject if the real food surface becomes uniformly glossy/waxy or if repeated ingredient shapes appear cloned`

Bad:

`avoid generic design`

Good:

`reject if title, image and supporting marks become three isolated rectangular blocks with no optical interaction`

## 8. Step 7 — Cross-style personal priors

Apply only personal priors supported by multiple independent style families.

The compiler must record every global prior applied.

If a prior conflicts with source style evidence, the source style wins unless the prior is a hard user boundary.

Example:

A global dislike of dirty yellow cast may constrain grading.

A global preference for minimalism must not erase a deliberately dense maximalist source family unless independently established as a hard boundary.

## 9. Step 8 — Compile renderer payload

The renderer payload is deliberately thin.

It must include:

### Task facts

What must be depicted / preserved.

### Mode

`RECONSTRUCT / FAMILY / TRANSFER`

### Visual anchors

Actual raw-pixel attachments.

### High-leverage variables

Maximum 8.

Choose only the variables most responsible for the current output.

### Hard avoids

Maximum 6.

Only task-relevant failure boundaries.

### Freedom instruction

Explicitly tell the renderer what it is free to change so the result does not become literal imitation.

## 10. Prompt anti-bloat rule

Compilation fails if the final renderer instruction:

- serializes the entire evidence database;
- includes unrelated global rules;
- repeats the same concept in multiple forms;
- explains internal system architecture to the renderer;
- contains more instructions than necessary to reproduce the program.

The image model should receive art direction, not governance documentation.

## 11. Renderer/production separation

Creative renderer responsibilities:

- visual synthesis;
- composition;
- lighting;
- image-world coherence;
- illustrative/material exploration;
- visual lettering exploration where appropriate.

Production tool responsibilities after quality PASS:

- exact copy;
- exact real text;
- editable layout;
- vector cleanup;
- print/packaging specifications;
- final exports.

Do not move creative responsibilities downstream merely because production tools are deterministic.

## 12. Distillation self-check

Before a capsule is eligible for rendering, answer YES to all:

1. Are raw pixels resolvable?
2. Is source evidence absolutely usable rather than relative-only?
3. Is observed evidence separated from inference?
4. Can every fixed invariant be traced to visual evidence?
5. Are degrees of freedom explicit?
6. Are source-specific elements marked do-not-transfer?
7. Are at least four transform operators executable?
8. Are actual visual anchors preserved?
9. Are failure boundaries concrete?
10. Is the renderer payload expected to stay within the thin prompt budget?

Any NO -> `DISTILLATION_NOT_READY`.

## 13. What the compiler learns over time

The compiler itself should change rarely.

New evidence should primarily create or improve:

- Style Capsules;
- task-conditioned preference priors;
- failure anchors;
- operator quality.

Do not rewrite the compiler for every new aesthetic style.

A compiler modification requires evidence that the same distillation failure occurs across multiple unrelated style capsules.
