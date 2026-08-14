# VPD V1 — Static Architecture Acceptance

Status: `PASS_STATIC / VISUAL_BENCHMARK_PENDING`
Date: 2026-08-14

## Scope

This acceptance checks architecture and contracts only.

It does **not** claim that the visual system already produces high-quality images.

## User requirement restated

The target is not merely:

`automatically choose one Mother Reference`

The target is:

`distill an excellent visual work into a reusable design program so future work can reuse the underlying method without literal copying; when a new style arrives, the same distillation system can create a new program without forgetting how to work.`

## Static gates

### G1 — Not retrieval-only

PASS.

The architecture defines a reusable `VisualProgram`, not only reference selection.

### G2 — Raw visual information is preserved

PASS.

A capsule must retain real visual anchors, including the canonical full-reference pixels.

This prevents language-only compression from becoming the sole representation.

### G3 — Design logic is explicit

PASS.

The program separates:

- observed evidence;
- inferred generative mechanism;
- fixed invariants;
- degrees of freedom;
- source-specific do-not-transfer elements;
- failure boundaries.

### G4 — Non-copy reuse is structurally supported

PASS.

The schema and compiler require explicit degrees of freedom plus transformation operators.

The system therefore has a formal representation of `what may change while the family remains recognisable`.

### G5 — Style transfer is structurally supported

PASS.

`FAMILY` and `TRANSFER` are distinct modes.

The acceptance protocol separately tests same-family reuse and higher-level transfer.

### G6 — New style does not require rewriting the system

PASS BY CONTRACT / PENDING EMPIRICAL TEST.

The compiler is fixed and Style Capsules are local.

The first benchmark explicitly requires a second materially different style capsule created with the same compiler and no global rule change.

### G7 — Strong visual model remains the creative renderer

PASS.

The architecture restores creative visual synthesis to the strongest available image model.

Codex/Figma are downstream production tools, not the zero-to-one artist.

### G8 — Prompt/rule bloat is controlled

PASS.

Renderer instructions are capped at 5–8 high-leverage variables and 1–6 relevant hard avoids.

The full evidence database is forbidden from serialization into the renderer prompt.

### G9 — Personal taste is not collapsed into one style

PASS.

The architecture separates:

- local Style Capsules;
- cross-style personal priors.

A single capsule cannot promote a global taste rule.

### G10 — Rejected evidence has a safe role

PASS.

Rejected images are failure/evaluator anchors and must not be attached as ordinary positive visual references without an explicit negative-image conditioning mechanism.

### G11 — Relative-only approval contamination is blocked

PASS.

`RELATIVE_ONLY` is represented explicitly and cannot be used as a positive capsule source.

### G12 — Direct simple workflow remains the control

PASS.

`reference pixels + content + short instruction -> same visual model` is a permanent B0 baseline.

The complex system must earn its existence.

### G13 — First real benchmark tests two styles

PASS.

The frozen run plan requires:

- Capsule A from Reference 05;
- Capsule B from materially different Reference 13;
- B0/B1/B2/B3 conditions for each.

This prevents false success from one-style overfitting.

### G14 — Transfer requires genuinely different content

PASS.

The run requires three content identities and blocks if the Asset Vault lacks honest transfer assets.

### G15 — Visual promotion cannot be inferred from static correctness

PASS.

Final state remains:

`VISUAL_BENCHMARK_PENDING`

## Static acceptance result

`PASS_STATIC / VISUAL_BENCHMARK_PENDING`

## What has been completed

- corrected project goal;
- Visual Program architecture;
- machine-readable capsule schema;
- frozen distillation compiler contract;
- acceptance protocol;
- first two-style benchmark plan;
- stop rules and promotion boundary.

## What has not been completed

- actual Capsule A distillation;
- actual Capsule B distillation;
- B0/B1/B2/B3 image generation;
- independent pixel review of eight benchmark outputs;
- user absolute quality judgment;
- production promotion.

## Next allowed step

Execute `VPD_V1_FIRST_RUN_PLAN.md` exactly.

If honest CONTENT-2 / CONTENT-3 real assets are unavailable, stop with:

`BLOCKED_NEEDS_TRANSFER_CONTENT_ASSETS`

Do not weaken the benchmark to avoid the blocker.
