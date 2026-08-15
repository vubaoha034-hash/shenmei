# VPD V2 — CODEX MASTER TASK

Status: `FROZEN_EXECUTION_TASK`

## Repository

`vubaoha034-hash/shenmei`

## Required branch

`visual-program-distillation-v2-photography-design-20260814`

## Anchor commit at task creation

`8e749b43cfa230ebd23f3c372da414cc9eb2a03a`

Use the connected repository and work only on the required branch.

This is an idempotent gated master task. It may be run again later. Do not skip gates based on assumption or prior chat text; use repository receipts.

---

# OBJECTIVE

Build and validate a professional personal visual-distillation system whose purpose is not to accumulate rules or imitate one frozen reference.

The system must learn how a strong image/design is constructed at photography, retouching, typography, layout, semantic, material, and photo-design-integration levels; reduce that deep analysis to a small high-impact renderer payload; and let the strongest available visual model perform creative synthesis.

Core principle:

`MODEL CREATES / SYSTEM DISTILLS AND DIRECTS / PRODUCTION TOOLS FINISH / HUMAN JUDGES`

Never use Figma, SVG path editing, or Codex geometry as the zero-to-one visual artist.

---

# PHASE 0 — VERIFY AND READ

Before doing any work:

1. Verify the current branch is exactly:
   `visual-program-distillation-v2-photography-design-20260814`
2. Record current HEAD.
3. Verify working tree is clean before execution.
4. Read completely:
   - `VPD_V2_DESIGN_SPEC_DRAFT.md`
   - `VISUAL_DISTILLATION_COMPILER_CONTRACT_V2.md`
   - `VPD_V2_MEASUREMENT_AND_CAUSAL_SPEC.md`
   - `schemas/visual-program.v2.schema.json`
   - `VPD_V2_ACCEPTANCE_PROTOCOL.md`
   - `VPD_V2_SELF_REVIEW_CHECKLIST.md`
   - `VPD_V2_EXTERNAL_SKILL_AUDIT.md`
   - `VPD_V2_PROFESSIONAL_REVIEW_RESULT.md`
   - `VPD_V2_RUNNER.md`
   - `VPD_V2_LIBRARY_SCALING_POLICY.md`
   - `VPD_V2_LIBRARY_SCALE_ACCEPTANCE.md`
   - `AESTHETIC_SKILL_DESIGN_CHARTER.md`

Do not continue R1E, R1E-2, or R1F.
Do not reintroduce typography-node repair as the primary task.
Do not bulk-import thousands of images during this phase.
Do not add new aesthetic rules unless required to fix a deterministic architecture defect discovered by validation.

---

# PHASE 1 — PRE-RENDER PROFESSIONAL DISTILLATION

Use exactly two materially different absolutely-usable reference styles:

- Style A: `R1C-APPROVED-05`
- Style B: `R1C-APPROVED-13`

Use their raw canonical pixels, never contact sheets or text summaries as substitutes.

Use the SAME V2 compiler architecture for A and B.
Do not modify the compiler between A and B.

For each style create exactly one V2 Style Capsule.

## Photography Engine must analyze, when material:

- camera/view geometry;
- perspective and focal-length feel without fabricating EXIF;
- subject scale, crop, occupancy and dominant mass;
- focus target and depth-of-field/blur gradient;
- bokeh/optical character where visible;
- key/fill/negative-fill/rim/back-light architecture;
- shadow direction, density and edge hardness;
- specular width/intensity and highlight rolloff;
- exposure placement, black floor, highlight shoulder, shadow toe;
- regional local contrast;
- white-balance feel and regional warm/cool map;
- hue relationships and saturation distribution;
- material realism and color plausibility;
- microcontrast, clarity, sharpening and edge behavior;
- grain/halation/bloom/scan character where relevant;
- subject styling/plating/props/environmental authenticity;
- moisture/oil/steam/condensation/action cues where relevant;
- global and local post-processing/retouch behavior.

## Graphic Design Engine must analyze, when material:

- semantic/communication intent;
- exact visible copy where readable and its role;
- first/second/third read;
- visual entry point and scan path;
- grid, axes, margins, alignment and optical offsets;
- title/subtitle/body/caption scale relationships;
- type category only when inferable;
- type width/weight/stroke modulation;
- tracking, line height and baseline behavior;
- stock vs modified vs custom lettering;
- glyph irregularity, terminal/cut behavior and word silhouette;
- text-image overlap/interlock/avoidance;
- whitespace map and function;
- background/text/accent/image color roles and proportions;
- graphics/motifs and whether they are structural or decorative;
- motif semantic source;
- z-order, masks, bleed, crop and frame-edge behavior;
- material/printing/substrate behavior;
- sequence/campaign behavior if present.

## Integration Engine must analyze:

- photo vs type dominance;
- whether photography creates usable type space;
- how crop and copy placement co-depend;
- how lighting supports hierarchy;
- shared color logic between image and graphics;
- semantic binding between subject/process and motifs;
- how realism survives graphic treatment;
- thumbnail read and second-read surprise.

## Evidence requirements

For critical/important variables record separately:

- `DIRECT_VISIBLE / METADATA / INFERENCE`;
- confidence;
- source region;
- measured/normalized evidence where appropriate;
- causal-quality hypothesis;
- counterfactual;
- interaction with other variables;
- validation test.

Never fabricate exact lens, aperture, light size, camera body, colorimetry or production settings from pixels without evidence.

With a single reference, proposed invariants remain `INVARIANT_HYPOTHESIS` until controlled output tests support them.

## Pre-render fail-closed conditions

Return `VPD_V2_DISTILLATION_NOT_READY` and STOP if any critical subsystem contains only adjectives such as:

- premium;
- cinematic;
- clean;
- high-end;
- soft light;
- big type;
- lots of whitespace;

without observable/measured evidence and causal explanation.

Also fail closed on:

- unsupported precision;
- missing typography analysis where typography is material;
- missing photography/design integration;
- missing raw-pixel reference binding;
- renderer prompt bloat.

---

# PHASE 2 — COMPILE THIN RENDERER PAYLOADS

Deep analysis may contain many fields.
The renderer must NOT receive the whole analysis.

For each condition compile only:

- task/content facts;
- actual raw reference pixels;
- actual real source/content pixels;
- mode;
- 4–10 highest-impact controls selected by causal priority;
- explicit freedoms;
- at most 6 relevant hard avoids.

The payload must behave like professional art direction, not governance documentation.

---

# PHASE 3 — CONTROLLED VISUAL BENCHMARK

Use the strongest available visual generation/editing model as creative renderer.

Use real, non-generated content assets from the private Asset Vault.

For each style resolve:

- CONTENT-1: reconstruction/source content;
- CONTENT-2: genuinely different real content for content-swap;
- CONTENT-3: real content suitable for composition/aspect variation if needed.

If sufficiently different real content is not available, return:

`VPD_V2_BLOCKED_INPUTS`

and STOP.

Do NOT manufacture transfer evidence by using a tiny crop change of the same image.

Generate EXACTLY 8 primary outputs:

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

Rules:

- same underlying strong visual model across comparable conditions;
- A0/B0 = raw reference + content + short human-like instruction only;
- no V2 variables in direct baseline;
- no best-of-N;
- no hidden extra batch;
- no cosmetic retry because output is ugly;
- deterministic integrity/tool failure retry is allowed only if failed artifact is quarantined and retry is logged;
- no Figma/Codex/SVG zero-to-one visual construction.

---

# PHASE 4 — PACKAGE FOR BLIND HUMAN REVIEW

Upload the 8 primary outputs to Drive using neutral/blind labels.

Keep condition mapping private.

Save:

- both capsule JSON files;
- schema validation receipts;
- measured evidence sheets;
- causal-priority sheets;
- renderer payload receipts;
- raw-reference/content hashes;
- generation receipts;
- retry/quarantine receipts if any;
- machine-integrity report;
- private blind mapping.

Codex may check technical integrity only.
Codex MUST NOT judge which output is aesthetically best.
Codex MUST NOT declare VPD V2 visually successful.

The required human review later must inspect actual pixels at:

- thumbnail scale;
- normal scale;
- detail scale;

and separately judge:

- photography;
- graphic design;
- photo/design integration;
- material realism;
- typography quality;
- absolute `USABLE / UNUSABLE`.

---

# PHASE 5 — HUMAN REVIEW GATE

After packaging, check for an explicit repository receipt created only after independent human review:

`VPD_V2_HUMAN_REVIEW_RESULT.json`

If it does NOT exist, or does not explicitly contain an allowed PASS status, STOP.

Do not infer PASS from chat logs, technical success, image existence, or Codex self-judgment.

On the first execution of this MASTER TASK, the expected stopping state is normally:

`WAITING_FOR_INDEPENDENT_PIXEL_REVIEW`

Do not continue to Library Scale Gate before this receipt exists.

---

# PHASE 6 — LIBRARY SCALE GATE

Execute this phase ONLY on a later rerun after explicit human-reviewed visual PASS exists.

Purpose:

Prove that a library growing to hundreds/thousands of liked restaurant images does NOT cause rule growth, style averaging, retrieval contamination or generation-quality regression.

Follow exactly:

- `VPD_V2_LIBRARY_SCALING_POLICY.md`
- `VPD_V2_LIBRARY_SCALE_ACCEPTANCE.md`

## Required architecture behavior

Raw evidence may grow without a matching increase in active generation complexity.

Every incoming image must be classified into exactly one primary evidence action:

- `DUPLICATE_OR_NEAR_DUPLICATE`
- `REINFORCE_EXISTING_FAMILY`
- `REFINE_EXISTING_FAMILY`
- `NEW_FAMILY_CANDIDATE`
- `CONTRADICTION_EVIDENCE`

Do not automatically create a new rule or capsule per image.

Whole-image approval must not imply every component is approved.
Where evidence supports it, keep component-level judgments separate for:

- photography;
- lighting;
- color;
- composition;
- retouching;
- typography;
- lettering;
- layout;
- copy;
- graphics;
- material/print;
- photo/design integration.

Do not allow repeated frames from one campaign/brand/photographer to create fake preference voting weight.

Conflicting liked families must remain distinct rather than averaged into a middle style.

## Scale invariants

As library size grows:

- raw evidence count MAY grow;
- number of visual families MAY grow when justified;
- confidence in an existing family MAY improve;
- active references per generation must remain bounded;
- active capsules per generation must remain bounded;
- renderer prompt budget must remain bounded;
- hard-avoid count must remain bounded;
- global preference rules must not grow linearly with image count.

If 1,000 additional images cause the default renderer prompt, active rule count or active reference count to expand roughly in proportion to library size, the scale architecture FAILS.

## Scale acceptance tests

At minimum test:

1. duplicate amplification resistance;
2. campaign/creator overrepresentation resistance;
3. component-level approval isolation;
4. contradictory-liked-family separation;
5. new-family onboarding without old-family contamination;
6. bounded active context as library grows;
7. fixed benchmark quality before/after simulated/actual library expansion;
8. no degradation versus the frozen pre-scale benchmark.

Do NOT bulk-import thousands of private images merely to satisfy a numeric target if a controlled stratified scale simulation can test the architecture first.

If the scale gate fails, identify the failure class before changing architecture:

- clustering/family error;
- duplicate weighting error;
- component-label contamination;
- global-prior contamination;
- retrieval/context-budget failure;
- prompt-growth failure;
- quality-regression failure.

Do not respond to a scale failure by simply adding more rules.

---

# FINAL OUTPUT CONTRACT

On first run, return exactly one of:

- `VPD_V2_BENCHMARK_READY_FOR_HUMAN_REVIEW`
- `VPD_V2_BLOCKED_INPUTS`
- `VPD_V2_DISTILLATION_NOT_READY`
- `VPD_V2_TECHNICAL_FAILURE`

If benchmark is ready, include:

## 已完成什么

## 未完成什么

## 需要人工验收什么

Then STOP.

On a later rerun with explicit human PASS receipt, after completing the Scale Gate, return exactly one of:

- `VPD_V2_SCALE_GATE_PASS`
- `VPD_V2_SCALE_GATE_FAIL`
- `VPD_V2_SCALE_GATE_BLOCKED`

and include:

## 已完成什么

## 未完成什么

## Scale Gate 证据

## 是否允许扩大图库

Never declare production promotion unless both visual benchmark and scale gate have passed independent acceptance.
