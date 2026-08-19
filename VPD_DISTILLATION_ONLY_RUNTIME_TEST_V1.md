# VPD Distillation-Only Runtime Test V1

Status: `FROZEN_NEXT_DIAGNOSTIC / PREFLIGHT_REQUIRED / NO_RENDER_UNTIL_ISOLATION_PROVEN`

Repository: `vubaoha034-hash/shenmei`
Branch: `visual-program-distillation-v2-photography-design-20260814`
Parent audit: `VPD_RUNTIME_EXECUTION_AUDIT_20260819.md`
Purpose: validate runtime transmission of the **already-distilled visual program**, not re-distill references and not test direct reference imitation.

## 1. Narrow question

Can the already-distilled VPD program generate materially different visual types while preserving high-level design judgment **without runtime reference-image conditioning**?

This diagnostic separates:

- `DISTILLATION_TRANSFER_DIVERSITY` — can different task types avoid one-template collapse?;
- `ABSOLUTE_AESTHETIC_QUALITY` — are the outputs actually good enough?;
- `RUNTIME_INTEGRITY` — did the renderer demonstrably receive the compiled distilled program rather than an ad-hoc conversational summary?

Passing one axis does not imply passing the others.

## 2. Scope boundary

This is an experimental ablation mode only.

It does **not** replace V3 `EXEMPLAR_FIRST` production architecture.
It does **not** change Discovery.
It does **not** change approved references.
It does **not** promote a new Style Capsule.
It does **not** create a new global aesthetic rule warehouse.

The purpose is to determine whether distilled causal controls survive the runtime boundary when direct visual anchors are intentionally absent.

## 3. Fresh-context requirement

The renderer session used for this test must be fresh/isolated.

Before rendering, prove all:

- no approved `R1C-APPROVED-*` pixels are loaded in the renderer conversation/session;
- no Mother Reference, Golden Exemplar, contact sheet, Drive preview, or derivative reference image is attached;
- no previous generated VPD output is attached as an image reference;
- renderer invocation uses `reference_runtime_policy = NONE`;
- the host can identify the exact textual/program payload sent to the renderer.

If any condition cannot be proven, STOP with:

`DISTILLATION_ONLY_RUNTIME_UNPROVEN_CONTEXT_CONTAMINATION`

Do not generate and then argue about contamination afterward.

## 4. Frozen source knowledge

Use existing repository distillation evidence only.

For the primary Reference-05-derived family test, use the already-established higher-level mechanisms:

1. `PROCESS_SCENE_HIERARCHY`
2. `MULTI_TIER_INFORMATION_SYSTEM`
3. `CAMPAIGN_MODULE_LOGIC`
4. `SEMANTIC_GRAPHIC_DERIVATION`
5. `DINING_WORLD_CONTEXT`

These are the candidate family mechanisms already used by V3 Family Transfer validation.

Do not substitute surface proxies such as:

- black/red;
- beige/green;
- brush calligraphy;
- paper texture;
- red seals;
- generic mountains;
- generic “东方” atmosphere.

Surface choices may vary by task and should be treated as freedoms unless a specific compiled task justifies them.

## 5. Runtime compiler contract

Each test task must produce a pre-render receipt containing:

```text
test_id:
task_type:
task_brief:
route_selected:
source_family_id:
family_mechanisms_selected:
primary_visual_cause:
attention_flow:
4_to_8_high_leverage_controls:
variation_freedoms:
generic_shortcut_suppressions_max_3:
reference_runtime_policy: NONE
production_role_of_imagegen:
compiler_output:
final_renderer_payload:
final_renderer_payload_sha256:
renderer_tool:
renderer_model_if_exposed:
renderer_settings_if_exposed:
context_isolation_proven: YES/NO
render_allowed: YES/NO
```

If `context_isolation_proven != YES`, render is forbidden.

If the final renderer payload is merely a list of color/font/material style tokens with no causal/structural mechanisms, fail preflight with:

`DISTILLATION_PAYLOAD_SURFACE_COLLAPSE`

## 6. Three task types

Generate exactly three outputs **only after all three preflights pass**.

The three tasks must be materially different in communication job, content organization and composition pressure.

### T1 — Brand Key Visual

Purpose:
- test whether the family can create a strong single campaign image without reducing itself to `big title + food plate`.

Required transfer:
- process/action participates in identity;
- at least three information levels exist conceptually;
- semantic marks derive from the actual food/process proposition;
- one clear primary visual cause;
- composition is free to be dense, sparse, light, dark, modern or rustic as justified.

### T2 — Ingredient / Origin Narrative

Purpose:
- test whether family logic can move away from a conventional restaurant promotion poster.

Required transfer:
- origin/ingredient/process storytelling becomes the dominant content structure;
- supporting modules are unequal and meaning-bearing, not decorative cards;
- dining/restaurant world may be secondary or absent if the origin narrative already establishes the world;
- surface language must not default to mountains + paper + seals simply because the task says origin.

### T3 — Minimal Editorial Campaign

Purpose:
- test whether the same high-level judgment survives severe density reduction.

Required transfer:
- at least one family mechanism must be expressed through **absence/spacing/hierarchy**, not by adding more objects;
- process or ingredient evidence may be a small photographic/graphic anchor;
- information hierarchy remains multi-tier even if the amount of visible copy is low;
- no default “new Chinese minimal” formula of beige paper + green calligraphy + red seal.

## 7. Diversity gate

The three outputs fail `DISTILLATION_TRANSFER_DIVERSITY` if they are recognizably the same template with changes limited to:

- color;
- background texture;
- headline placement;
- photo crop;
- decorative seal/icon;
- density alone.

Before aesthetic scoring, compare the three at grayscale thumbnail scale.

PASS requires materially different:

- dominant mass structure;
- image/type relationship;
- negative-space geometry;
- attention path;
- module architecture;
- scene/content emphasis.

The family relationship should come from design decisions and hierarchy, not repeated props or surface tokens.

## 8. Image-generation role boundary

This diagnostic may use one-pass ImageGen to test zero-to-one art-direction capability, but **must not interpret generated typography as production typography**.

For every output record:

`PRODUCTION_TYPOGRAPHY = NOT_EVALUATED`

unless a later separate Figma/layout stage is explicitly run.

Do not declare a full commercial brand artifact PASS solely from this test.

If the test proves art direction but typography is weak, that is compatible with the existing G3R production separation doctrine.

## 9. Output budget

- formal outputs: exactly `3`
- one per task type
- hidden variants: `0`
- best-of-N: `NO`
- aesthetic retries: `0`
- technical retry: at most `1` per task for deterministic transport/tool failure only

Any invalid technical output must be recorded and cannot be silently replaced.

## 10. Post-render receipts

For each output record:

```text
output_filename:
output_sha256:
dimensions:
renderer_generation_id_if_exposed:
reference_images_attached: 0
technical_validity:
family_mechanisms_visibly_present:
generic_template_collapse_0_to_10:
absolute_art_direction_0_to_10:
photo_material_realism_0_to_10_if_applicable:
photo_design_integration_0_to_10:
semantic_hierarchy_0_to_10:
production_typography: NOT_EVALUATED
user_absolute_verdict: PENDING
```

No self-score can substitute for the user's human absolute verdict.

## 11. Pass logic

### Runtime Integrity PASS

Requires:

- fresh context proven;
- zero runtime reference images;
- exact compiler output captured;
- exact final payload/hash captured;
- actual renderer identity/settings captured to provider limits;
- exact outputs captured.

### Distillation Transfer Diversity PASS

Requires all three outputs to have materially different macro structures and no shared surface-template collapse.

### Aesthetic Signal PASS

Requires:

- at least two of three outputs judged by the user as a material aesthetic advance over the recent ad-hoc R4.2 set;
- none relies primarily on a generic cultural shortcut;
- at least one output demonstrates a visual type not already represented by the recent R4.2 template family.

This is a diagnostic signal, not Commercial Quality PASS.

## 12. Verdicts

Use exactly one primary test verdict:

- `DISTILLATION_ONLY_RUNTIME_PASS`
- `DISTILLATION_ONLY_RUNTIME_PARTIAL_SUPPORT`
- `DISTILLATION_ONLY_RUNTIME_SURFACE_COLLAPSE`
- `DISTILLATION_ONLY_RUNTIME_UNPROVEN_CONTEXT_CONTAMINATION`
- `DISTILLATION_ONLY_RUNTIME_TECHNICAL_BLOCKED`

Commercial Quality, Golden and Scale remain separate gates regardless of verdict.

## 13. Stop rule

After exactly three valid outputs and human review, STOP.

Do not immediately:

- add rules;
- add references;
- re-distill;
- scale the library;
- change V3 architecture.

First attribute any failure to one of:

- runtime payload selection;
- prompt compilation;
- renderer capability;
- task/content compatibility;
- one-pass art-direction limitation;
- typography/production-stage limitation.

## 已完成什么

- strict no-reference runtime diagnostic defined;
- clean-context gate defined before rendering;
- three materially different task types defined;
- surface-template failure criteria defined;
- production typography explicitly separated from ImageGen art-direction testing;
- exact receipt requirements defined.

## 未完成什么

- fresh renderer context has not yet been established;
- no preflight receipt exists yet;
- no formal outputs have been generated;
- no human verdict exists;
- Commercial Quality, Golden and Scale remain blocked.
