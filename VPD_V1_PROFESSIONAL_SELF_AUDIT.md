# VPD V1 Professional Self-Audit

Status: `FAIL_ARCHITECTURE_DEPTH / DO_NOT_RUN_VISUAL_BENCHMARK`
Date: 2026-08-14

## Verdict

VPD V1 is conceptually directionally correct but too coarse to be accepted as a professional photography/design distillation system.

The failure is not that it lacks more aesthetic adjectives. The failure is that its typed decomposition does not reach the resolution at which photographers, retouchers, art directors, typographers, and graphic designers actually control a final image.

Do not run the previously planned VPD V1 visual benchmark as the next step. First upgrade the distillation contract.

## What V1 got right

- separates raw visual anchors from text summaries;
- separates fixed invariants from degrees of freedom;
- keeps the strong visual model as creative renderer;
- distinguishes creative rendering from downstream production tooling;
- preserves direct-reference baseline;
- supports family/transfer rather than literal cloning;
- keeps rejected evidence primarily as failure evidence.

These remain.

## What V1 got wrong / under-specified

### 1. Photography was collapsed into broad labels

V1 records `material/light behavior`, color distribution, composition, crop, contrast and texture, but this is insufficient.

A professional image can change materially while preserving all of those broad labels if any of the following differ:

- camera height / view angle / perspective;
- focal-length feel and subject-camera distance;
- focus plane;
- depth-of-field gradient;
- bokeh character;
- motion blur or subject blur;
- key/fill/rim relationship;
- light-source apparent size and softness;
- shadow edge hardness and density;
- specular width and rolloff;
- exposure placement;
- highlight shoulder / black floor / midtone compression;
- white balance and local color temperature split;
- global vs local saturation;
- microcontrast / clarity;
- sharpening behavior;
- local dodge-and-burn;
- grain / halation / bloom;
- material-specific response;
- styling / prop / surface / imperfection decisions.

V1 cannot reliably distinguish or reconstruct these.

### 2. Graphic design was also collapsed into broad labels

V1 records hierarchy, typography behavior, geometry and motif logic, but does not explicitly model:

- message/semantic intent;
- copy hierarchy and meaning;
- grid / alignment / baseline structure;
- type category vs custom lettering;
- size ratios, width ratios, tracking, line height;
- glyph-level transformation behavior;
- image/type overlap geometry;
- optical rather than mathematical spacing;
- information density by region;
- edge/crop interactions;
- repetition/rhythm;
- layer order and occlusion;
- production/print behavior;
- multi-page continuity where relevant.

V1 therefore risks producing generic `large type + image + whitespace` summaries that are technically true but visually weak.

### 3. V1 mixes observation and latent production inference too loosely

Some properties are directly visible; some are inferred.

Example:

- `soft shadow edge` is visible evidence;
- `large softbox at camera-left` is an inference;
- `85mm lens` is usually not safely inferable from pixels alone.

V2 must retain confidence/provenance and prohibit invented camera settings from becoming facts.

### 4. V1 does not model causal importance

Not every visible property contributes equally to quality.

V2 needs an `impact_weight` / `sensitivity` layer:

- which variables are quality-critical;
- which are secondary;
- which can vary freely;
- which variables interact nonlinearly.

Without this, thin prompt compilation may preserve the wrong 5–8 variables.

### 5. V1 lacks perceptual-scale acceptance

A design can look acceptable at full screen and fail at thumbnail scale, or vice versa.

V2 acceptance must include:

- thumbnail read;
- normal viewing read;
- detail/microtexture read;
- subject/material realism read;
- typography legibility read where text matters.

### 6. V1 lacks component-level reconstruction tests

Before full-image transfer, a capsule must be able to reproduce critical subsystems independently when needed:

- photography grade/lighting;
- typography treatment;
- composition skeleton;
- material/texture behavior.

This does not mean rebuilding them manually in Figma. It means testing whether the renderer understands each subsystem.

## Required V2 direction

Build a two-engine distillation model:

1. `PHOTOGRAPHY_ENGINE`
   - capture geometry;
   - light;
   - exposure/tonality;
   - color science/grade;
   - focus/optics;
   - texture/sharpness/noise;
   - material realism;
   - styling/scene;
   - post-processing.

2. `GRAPHIC_DESIGN_ENGINE`
   - semantic intent;
   - hierarchy;
   - grid/alignment;
   - typography/lettering;
   - image-type relationship;
   - whitespace;
   - color roles;
   - motif/illustration;
   - rhythm/repetition;
   - layer/crop/edge behavior;
   - print/material treatment;
   - information density.

Then add:

3. `INTEGRATION_ENGINE`
   - how photography and design interact;
   - what the eye reads first/second/third;
   - how type shares space with image;
   - how palette is shared;
   - how subject semantics drive motifs and typography.

4. `CAUSAL_PRIORITY_MAP`
   - high-impact variables;
   - variable interactions;
   - confidence;
   - tolerances.

5. `TRANSFER_MODEL`
   - what remains;
   - what rebinds to new content;
   - what must never be copied literally.

## Acceptance consequence

VPD V1 static acceptance is superseded by this audit.

Current state:

`VPD_V1 = ARCHITECTURE_NOT_DEEP_ENOUGH`

Next permitted action:

Create VPD V2 and statically validate its schema and compiler before any expensive image-generation benchmark.
