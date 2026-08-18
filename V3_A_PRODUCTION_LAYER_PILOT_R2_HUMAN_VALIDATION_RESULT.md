# V3 A Production Layer Pilot R2 — Human Validation Result

Status: `PRODUCTION_LAYER_PASS / COMMERCIAL_QUALITY_NOT_YET`

Repository: `vubaoha034-hash/shenmei`
Branch: `visual-program-distillation-v2-photography-design-20260814`
Submitted HEAD: `0b506625ab48917cc81f5e120f4ea45cbc5596e4`

## Evidence reviewed

Human visual review compared actual pixels from:

1. `V3-A_FOOD_APPETITE_CORRECTED_R1.png` — before
2. `V3-A_PRODUCTION_LAYER_PILOT_R2.png` — after
3. `R1C-APPROVED-05.jpg` — Mother Reference

Submitted after SHA-256:
`964671205099d7f7e08d8fe8a5279bdc5cc6505f88e970da24466c54e82acb67`

Dimensions:
`1024x1536`

## Pixel-stability verification

A direct before/after pixel comparison found:

- total changed pixels: `8841` (`0.5621%` of image pixels)
- changed pixels in the left production/typography rail: `8709`
- changed pixels outside the left production rail: `132`
- maximum channel delta for all 132 outside-rail pixels: `1`

Therefore the reported Art Layer stability is visually and numerically consistent with export-rounding-only differences outside the typography production zones.

The following remain materially unchanged:

- plated food
- wok / process scene
- hands / people / dining context
- flames / steam
- macro composition
- semantic curve system
- global lighting / grade
- raster display identity `现烧`

## Human findings

### 1. Functional typography professionalism

Verdict: `PASS — MATERIAL BUT LIMITED IMPROVEMENT`

The deterministic typography is cleaner and more controlled than the baked generated text.

Most visible improvement:

- `今日` is now correctly subordinate to `现烧` instead of competing with it;
- glyph rendering is cleaner;
- Chinese functional typography is more stable;
- English micro-labels have consistent tracking / baseline behavior;
- the left rail now reads as an intentional production layer instead of unstable generated lettering.

However this is not yet a proprietary typography system.

`Noto Serif SC + Inter` is technically competent but still reads as a generic professional pairing rather than a brand-owned typographic voice.

### 2. Left-rail hierarchy and spacing

Verdict: `PASS`

Hierarchy is clearer:

1. `现烧` remains the display identity leader;
2. `今日` is secondary;
3. `锅气入味` works as tertiary Chinese support;
4. English labels sit in the lowest information tier.

Spacing and baseline control are more disciplined than before.

Remaining weakness:

- the vertical `锅气入味` treatment is clean but slightly generic / passive;
- the repeated separator-rail + English-label grammar still resembles an editorial/UI information component more than a distinctive restaurant brand language;
- the English labels remain semantically generic (`WOK HEAT`, `CHILI AROMA`, `DINING ALIVE`) and can still read as art-direction filler rather than campaign-specific copy.

### 3. Display identity `现烧`

Verdict: `PASS`

`现烧` remains the first identity layer and was not visually degraded by the production-layer work.

The new smaller `今日` materially improves its dominance.

### 4. Food and Art Layer stability

Verdict: `PASS`

Human pixel comparison shows no meaningful food or Art Layer regression.

The submitted claim that food/art remained frozen is consistent with the actual before/after imagery.

### 5. Less AI-template-like?

Verdict: `PARTIAL PASS`

The typography itself is materially less AI-generated because the functional text now behaves like real typesetting.

But the whole artifact still carries noticeable AI/composite cues, especially in:

- hyper-glossy repetitive food surfaces;
- over-dense particles / droplets / debris;
- highly dramatized wok scene;
- synthetic-looking garnish repetition;
- excessive micro-detail and local contrast in the food / process layer;
- a polished but still generic editorial label system.

Therefore the Production Layer solved one important AI cue, but did not solve the entire commercial-readiness problem.

### 6. Commercial production readiness

Verdict: `CLOSER, BUT NOT YET`

This is a real improvement toward a commercial production artifact.

It is not yet at the user's required commercial standard.

The dominant remaining gap is no longer basic functional typography. It has moved to:

1. food / photography realism and restraint;
2. authored brand-specific visual language rather than generic premium-editorial language;
3. proprietary relationship between display identity and supporting typography;
4. campaign-specific copy / information semantics instead of generic English filler;
5. reduction of synthetic particle/detail density;
6. final micro-art-direction and production restraint.

### 7. Is the remaining gap now mainly display-identity / renderer rather than functional typography?

Verdict: `YES WITH QUALIFICATION`

Functional typography is no longer the primary blocker.

However the remaining blocker is broader than display lettering alone. It includes renderer/art-layer realism, food styling, photographic coherence, brand authorship, copy semantics, and overall commercial restraint.

## Final verdict

- Production Layer Pilot R2: `PASS`
- Functional typography materially improved: `YES`
- Hierarchy / spacing materially improved: `YES`
- `现烧` identity preserved: `YES`
- Food layer stable: `YES`
- Art layer stable: `YES`
- Whole-image regeneration: `NO`
- Commercial Quality Gate: `NOT YET`
- Golden Exemplar: `NO`
- Route B: `SOURCE_MISMATCH_FOR_ROUTE_B`
- Library Scale Gate: `BLOCKED`

## Dependency update

Do not repeat another typography-only retrofit as the next major experiment.

The next Commercial Hardening step should target the dominant remaining commercial defects while preserving the validated macro composition and production-layer gains:

- reduce synthetic food / particle artifacts;
- improve food photographic realism and material variation;
- increase brand-specific authorship in the left rail without redrawing `现烧` blindly;
- replace generic English filler with campaign-meaningful microcopy or remove it if unnecessary;
- preserve deterministic live typography and exact micro-alignment;
- keep Scale Gate blocked until a human Commercial Quality Gate passes.
