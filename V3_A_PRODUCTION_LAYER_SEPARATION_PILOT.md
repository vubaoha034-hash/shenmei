# V3 A — Production Layer Separation Pilot

Status: `FROZEN_NEXT_TASK`

## Objective

Test whether the remaining quality gap in `V3-A_FAMILY_TRANSFER_REFINED_R1.png` is primarily a production-layer typography/alignment problem rather than a macro visual-program problem.

This is **not** a new concept generation task.

The current refined artifact is the selected visual direction and must remain the visual target.

## Frozen evidence

Human validation status:

`REFINEMENT_PASS / GOLDEN_EXEMPLAR_NOT_YET`

The macro visual system is now considered structurally successful enough for this pilot:

- family identity is present;
- generic `large brush title + plated dish` collapse is absent;
- process cooking, multi-tier information, semantic cues and dining-world context are integrated;
- macro composition does not need another redesign pass.

Remaining dominant weakness:

- display identity ownership;
- exact functional typography;
- optical spacing;
- baseline rhythm;
- small-label consistency;
- repeatable brand production precision.

## Principle

Use the strongest visual model for the **art layer**.

Use deterministic production tooling for **functional typography and alignment**.

Do NOT ask Figma/Codex to hand-draw Chinese display lettering.

Do NOT regenerate the whole poster.

## Input

Primary selected artifact:

`V3-A_FAMILY_TRANSFER_REFINED_R1.png`

Mother reference:

`R1C-APPROVED-05.jpg`

The primary artifact must be verified by its existing SHA and dimensions before work begins.

## Production split

### Layer 1 — Art layer

Freeze all of the following pixels unless a minimal mask is required solely to cover text being replaced:

- wok/process scene;
- flames;
- steam;
- food;
- dining scene;
- tableware;
- ingredient cues;
- background lighting;
- global color grade;
- macro composition;
- curved semantic line system.

No generative redesign of these regions.

### Layer 2 — Display identity

The large `现烧` display lettering may remain as the current raster visual asset if it survives validation.

Do not redraw it in Figma as low-level vector paths.

If exact isolation is possible without generative invention, preserve it as a raster/alpha visual asset.

If exact isolation is not possible, keep the existing display lettering pixels and do not attempt replacement in this pilot.

### Layer 3 — Functional typography

Deterministically typeset the functional information layer using real installed/project-accessible fonts:

- `今日`
- `锅气入味`
- `WOK HEAT`
- `CHILI AROMA`
- `DINING ALIVE`
- any small explanatory labels that remain necessary

Do not invent additional copy merely to fill space.

The functional type should:

- use at most two compatible font families;
- use a disciplined type scale;
- have exact baseline rhythm;
- have optical alignment to the left identity rail;
- use intentional tracking and line spacing;
- be quieter than the display identity;
- avoid stock-template icon/label styling.

### Layer 4 — Micro alignment

Allow deterministic adjustment only for:

- left rail margins;
- label spacing;
- baseline positions;
- small separators;
- semantic line endpoint alignment;
- safe-area consistency.

No change to the macro composition.

## Required output

Create exactly one production pilot:

`V3-A_PRODUCTION_LAYER_PILOT_R1.png`

and one editable production source if available through the chosen deterministic tool (for example Figma frame/source).

No alternative designs.
No best-of-N.
No hidden variants.
No whole-image ImageGen retry.

## Comparison package

Upload exactly:

1. `R1C-APPROVED-05.jpg`
2. `V3-A_FAMILY_TRANSFER_REFINED_R1.png`
3. `V3-A_PRODUCTION_LAYER_PILOT_R1.png`

The new output must be evaluated by human pixels before any Golden Exemplar promotion.

## Acceptance questions

Human validation must answer:

1. Does functional typography look materially more professional and intentional?
2. Is the main display identity preserved without degradation?
3. Are spacing and alignment visibly more controlled?
4. Does the work feel less AI-generated / templated at normal and detail view?
5. Is the overall artifact now worthy of `GOLDEN_EXEMPLAR`?

## Fail-closed conditions

Fail if:

- the art layer is materially changed;
- the current display lettering is damaged by masking/compositing;
- Figma/Codex attempts to redraw the Chinese display lettering from scratch;
- the production overlay looks detached from the image;
- additional labels/icons are added only to fill space;
- macro composition is changed;
- the output cannot be traced back to the exact selected artifact.

## Route B

Remain `SOURCE_MISMATCH_FOR_ROUTE_B`.

Do not generate Route B.

## Scale Gate

Blocked.
