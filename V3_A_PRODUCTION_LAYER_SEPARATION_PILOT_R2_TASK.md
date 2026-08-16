# V3 A — Production Layer Separation Pilot R2

Status: `READY_AFTER_FOOD_APPETITE_PASS`

Repository: `vubaoha034-hash/shenmei`
Required branch: `visual-program-distillation-v2-photography-design-20260814`

## Current state

Human validation has frozen:

- Family Transfer: `PASS`
- Single-artifact refinement: `PASS`
- Food Appetite Correction R1: `FOOD_APPETITE_PASS`
- Golden Exemplar: `NOT YET`
- Route B: `SOURCE_MISMATCH_FOR_ROUTE_B`
- Library Scale Gate: `BLOCKED`

The exact selected artifact for this pilot is now:

`V3-A_FOOD_APPETITE_CORRECTED_R1.png`

SHA-256:
`64c9a1370519f0cc3bc7a16046f4042712353b08b2729f10051a58ffc3c6803c`

Dimensions:
`1024x1536`

Do not use the older pre-food-correction artifact as the production target.

## Purpose

Test whether the remaining quality gap is primarily a production-precision problem in functional typography and micro-alignment rather than a failure of the visual program.

This is NOT a new concept generation.
This is NOT another whole-image refinement.
This is NOT a Chinese display-lettering drawing task.

## Critical production-layer insight

The selected artifact already contains functional text baked into pixels.

Therefore it is invalid to simply overlay new deterministic typography on top of existing generated text.

The pilot must either:

1. safely clear ONLY the functional-text production zones, preserving the underlying visual field and all art pixels outside those zones, then typeset deterministic typography; or
2. fail closed with:
   `V3_A_PRODUCTION_LAYER_RETROFIT_BLOCKED`

If clean local separation is not technically reliable, do not recreate the entire image from memory or regenerate the art layer.

## Frozen Art Layer

The following must remain visually unchanged except for unavoidable sub-pixel export/compositing differences:

- main corrected plated dish and its appetite correction;
- wok / process scene;
- flames;
- steam;
- people / dining context;
- tableware and supporting food cues;
- global lighting;
- global color grade;
- macro composition;
- major semantic curve/path system;
- large raster display identity `现烧`.

The corrected food appearance is now frozen.
Do not darken it again.
Do not recolor it.

## Display Identity

The large Chinese display identity `现烧` is a raster visual asset for this pilot.

Rules:

- preserve it;
- do not redraw it in Figma/Codex;
- do not replace it with a stock font;
- do not vector-trace it;
- do not ask a layout tool to invent a new high-end Chinese display wordmark.

This pilot is explicitly NOT a repeat of the failed R1E Chinese-lettering path.

## Functional Typography zones

The following generated functional text may be removed/replaced deterministically where present:

- `今日`
- `锅气入味`
- `WOK HEAT`
- `CHILI AROMA`
- `DINING ALIVE`

If additional small labels exist, retain them only if they carry real semantic value. Do not preserve filler text for density.

Use real font files already available in the production environment / project. Do not share font binaries externally.

Maximum 2 font families.

## Typography requirements

The deterministic layer must improve:

- hierarchy;
- optical alignment;
- tracking;
- line spacing;
- baseline rhythm;
- safe-area consistency;
- left identity-rail balance;
- relationship between Chinese functional text and English micro-labels.

Functional typography must stay subordinate to `现烧` and the main visual scene.

Avoid:

- fake luxury spacing;
- stock restaurant-template labels;
- decorative English for filler;
- excessive all caps;
- gratuitous icons;
- generic gold-on-black premium clichés.

## Local cleanup rules

If functional text is baked into a nearly flat/dark region, local deterministic cleanup is allowed only inside a tightly bounded production zone.

Allowed:

- local background reconstruction limited to text removal zones;
- re-drawing simple production separators / rails where they are part of typography alignment;
- sub-pixel alignment adjustments.

Not allowed:

- changing food;
- changing people;
- changing wok / flame / steam;
- changing scene lighting;
- changing macro composition;
- replacing semantic imagery;
- whole-image regeneration;
- generative redesign of the poster.

Keep a before/after zone manifest.

## Preferred tool split

Use deterministic layout/text tooling for the final typography layer.

A local image editor may be used only for tightly bounded text cleanup if necessary.

Do not use a generative visual model to redesign the poster.

If the available toolchain cannot isolate the text zones cleanly, fail closed instead of faking layer separation.

## Formal output

Exactly one formal output:

`V3-A_PRODUCTION_LAYER_PILOT_R2.png`

Also preserve one editable production source if supported by the deterministic production tool.

No alternative concepts.
No hidden variants.
No aesthetic retries.

A deterministic export failure may be retried once with a receipt.

## Comparison package

Upload exactly these human-review essentials:

1. `V3-A_FOOD_APPETITE_CORRECTED_R1.png` — selected before state
2. `V3-A_PRODUCTION_LAYER_PILOT_R2.png` — production-layer result
3. `R1C-APPROVED-05.jpg` — mother reference
4. editable production source only if it is useful for future production and supported by the tool
5. `V3_A_PRODUCTION_LAYER_PILOT_R2_MANIFEST.json`

The manifest must record:

- selected artifact SHA;
- output SHA;
- dimensions;
- exact zones cleaned;
- exact typography elements replaced;
- fonts/families used by name only;
- art-layer-changed boolean;
- food-layer-changed boolean;
- display-lettering-redrawn boolean;
- whole-image-regenerated boolean;
- editable source identity;
- technical retry count.

## Human validation questions

Do NOT self-approve aesthetics.

Human review must determine:

1. Did functional typography become materially more professional and less AI-template-like?
2. Did hierarchy and micro-alignment improve?
3. Is `现烧` still the visual identity leader?
4. Did the corrected food remain intact?
5. Did the art layer remain visually stable?
6. Did the poster move closer to a real production-ready brand artifact?
7. Is remaining quality gap now dominated by display-identity/renderer capability rather than functional typography?

## Stop conditions

Do not:

- run Route B;
- run Library Scale Gate;
- modify Discovery;
- modify the global compiler;
- expand the reference library;
- create a new poster concept.

After one formal output or one fail-closed retrofit blocker, STOP.
