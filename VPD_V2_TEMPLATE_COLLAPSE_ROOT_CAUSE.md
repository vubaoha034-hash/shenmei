# VPD V2 Template Collapse Root-Cause Diagnosis

Status: `ABSOLUTE_QUALITY_FAIL / ROOT_CAUSE_IDENTIFIED_ENOUGH_FOR_TARGETED_EXPERIMENT`

## 1. Calibrated premise

The replacement blind review showed technical correctness but used a commercial-acceptability rubric that was too lenient for the project goal. The user's absolute calibration is materially stricter: food/material realism is only around 6/10, while design, typography, integration and overall aesthetic quality are around 1–2/10. No benchmark output is accepted as final-quality usable, and none is top-tier.

Therefore the benchmark must be interpreted as `RELATIVE_METHOD_SIGNAL / ABSOLUTE_AESTHETIC_FAIL`.

## 2. Correct unblind mapping

- R01 = A0_DIRECT
- R02 = B0_DIRECT
- R03 = B1_V2_RECONSTRUCT
- R04 = B3_V2_COMPOSITION_OR_ASPECT_VARIATION
- R05 = B2_V2_CONTENT_SWAP
- R06 = A2_V2_CONTENT_SWAP
- R07 = A3_V2_COMPOSITION_OR_ASPECT_VARIATION
- R08 = A1_V2_RECONSTRUCT

The mapping itself is retained from the original frozen benchmark ledger; the earlier human score binding was invalid, not the benchmark mapping.

## 3. What the pixels prove under the calibrated rubric

Across all eight outputs, two materially different source references collapse into two surface variants of the same generic restaurant-poster template:

- Style A outputs: black/red field + oversized white brush/calligraphic headline + plated food;
- Style B outputs: warm mineral/beige field + olive/dark brush/calligraphic headline + plated food.

The persistent shared skeleton is:

`large brush headline + one or more plated dishes + simple background field`.

This is much simpler than either approved source reference.

## 4. Why this is not faithful distillation of Reference 05

Reference 05 is not merely `black/red + white brush type + spicy food`.

Its high-value design system includes:

- an active cooking-process hero image: chef hands, wok, flame, steam, ingredient action;
- a compact brand mark and secondary copy hierarchy rather than one oversized generic headline;
- semantic chili/fire/ingredient iconography;
- multiple editorial/campaign panels with differentiated image roles;
- place/ingredient/process storytelling;
- red used as a system carrier across a campaign, not merely a background splash;
- multiple levels of copy, icons and image modules.

The benchmark Style A outputs retain mostly the lowest-dimensional surface cues:

- black;
- red;
- white;
- rough calligraphic lettering;
- food;
- heat/fire ambience in some outputs.

They discard the campaign-system grammar, process narrative, information hierarchy and semantic graphic system.

### Additional reference-granularity problem

Reference 05 is itself a multi-panel brand/campaign board rather than one single target poster. Using the full board as a monolithic renderer anchor encourages the model to compress it into its most salient common motifs instead of preserving the role of individual sub-layouts. Full-board pixels are useful as system evidence, but are insufficient as the sole visual anchor for a single-output reconstruction.

## 5. Why this is not faithful distillation of Reference 13

Reference 13 is not merely `beige + green brush headline + food vessel`.

Its high-value design system includes:

- a deliberately irregular multi-glyph headline field, with large spatial variation across characters;
- strong asymmetrical title composition rather than one horizontal line of type;
- a dark clay pot/ingredient still-life occupying the lower center;
- a vertical right-side information rail;
- a lower four-part hashtag/information rhythm;
- supporting body copy;
- active negative space whose shape is defined by the headline, pot and information system together;
- muted photographic still-life styling, not a generic plated-dish hero.

The benchmark Style B outputs retain mostly:

- warm mineral/beige field;
- olive/dark calligraphic title;
- food;
- sparse composition.

They discard the distinctive title geometry, vertical side rail, lower information architecture, pot/ingredient still-life archetype and carefully engineered negative-space relationships.

## 6. Root causes

### RC1 — STYLE-DISCRIMINATIVE FEATURE LOSS
Confidence: `HIGH`
Layer: `compiler / payload selection`

V2 selects a small number of high-impact variables, but the current selection logic does not guarantee that the selected variables are the ones that distinguish one style family from another.

Both source references contain food and expressive Chinese lettering. Those shared, easy-to-verbalize cues survive compilation; the discriminative grammar is dropped.

Critical distinction:

`quality-important` is not the same as `style-discriminative`.

A future payload must preserve both.

### RC2 — COMMON-MODE SEMANTIC PRIOR
Confidence: `HIGH`
Layer: `renderer/task framing`

All conditions share:

- restaurant/food domain;
- the exact phrase `今日现烧`;
- plated-food source assets in several conditions;
- the same underlying visual model.

That common semantic bundle strongly activates a generic Chinese restaurant-ad prior: large brush calligraphy plus food plate. The raw references are not strong enough, in the current payload form, to overcome that prior consistently.

DIRECT outputs also collapse, proving this is not solely a V2 compiler defect. V2 failed to overcome the model prior rather than creating it from nothing.

### RC3 — CONTENT / SCENE-ARCHETYPE MISMATCH
Confidence: `HIGH`
Layer: `input routing / transfer model`

Reference 05's strongest hero logic is cooking action/process. Reference 13's strongest photographic logic is clay-pot/ingredient still life. The benchmark repeatedly asks these systems to absorb already-plated dish sources.

The system currently treats `food content swap` as sufficient compatibility. It needs a `scene-archetype compatibility gate`.

When target content is incompatible with the source family, the system should either:

- synthesize a new compatible scene while preserving factual product identity; or
- refuse to claim faithful family transfer.

It should not simply place the new plate into a generic poster shell.

### RC4 — TYPOGRAPHY REBINDING COLLAPSE
Confidence: `HIGH`
Layer: `compiler + renderer capability`

The sources use typography differently:

- Reference 05: compact brand/identity hierarchy integrated with imagery and supporting copy;
- Reference 13: large custom irregular character composition forming the spatial architecture.

The outputs reduce both to `large brush headline`.

The measurement layer already has typography boxes and behavior fields, but the renderer payload does not preserve enough of:

- glyph-group geometry;
- relative character scale;
- title silhouette;
- baseline irregularity;
- vertical vs horizontal information rails;
- relation between headline and secondary copy.

This is not solved by saying `custom brush lettering` more strongly.

### RC5 — OVERCOMPRESSION OF A COMPLEX STYLE SYSTEM
Confidence: `HIGH`
Layer: `renderer interface`

The anti-bloat principle is correct, but the implementation over-compresses style information into prose controls. A deep analysis may contain dozens of useful fields, while only 4–10 controls reach the renderer.

The solution is not to dump all fields into the prompt.

The solution is to preserve high-dimensional information through direct visual anchors:

- full system reference;
- role-specific source crops for typography;
- role-specific source crops for composition/scene;
- role-specific source crops for information hierarchy or graphic language.

Prompt stays thin; visual conditioning becomes richer.

### RC6 — REFERENCE GRANULARITY BUG FOR MULTI-PANEL REFERENCES
Confidence: `HIGH` for Style A
Layer: `reference binding`

A multi-panel brand board and a single target poster are not the same visual object. The current system lacks an explicit `reference object type` distinction:

- single poster;
- campaign board;
- editorial spread;
- packaging system;
- photo-only reference;
- typography-only reference.

A campaign board must first be decomposed into role-bearing regions before single-image generation.

### RC7 — ABSOLUTE QUALITY RUBRIC FAILURE
Confidence: `CONFIRMED`
Layer: `evaluation`

Previous evaluation rewarded legibility, clean files, basic composition and plausible food as if they implied high aesthetic quality. That is false for this project.

Technical correctness and aesthetic quality are now separate axes. Reference distance is a hard gate.

## 7. Why 'add more rules' is the wrong response

The collapse is not caused by a shortage of adjectives or constraints. Adding rules such as:

- more premium;
- less generic;
- more reference-like;
- more custom typography;

would increase prompt interference without restoring lost visual information.

The needed repair is structural:

1. preserve style-discriminative evidence;
2. decompose reference objects by role;
3. bind role-specific raw-pixel crops directly;
4. add scene-archetype compatibility;
5. compile a thin prompt from discriminative + quality-critical variables, not generic shared cues.

## 8. Calibrated conclusion

VPD V2 currently demonstrates that structured distillation can change outputs, but it has not demonstrated production-worthy aesthetics.

All eight benchmark outputs remain `ABSOLUTE_FAIL` under the user's calibrated quality target.

The important finding is not which condition is relatively better. The important finding is that two distinct approved references converge toward one generic restaurant prior.

This is a `STYLE_SIGNATURE_COMPRESSION_COLLAPSE`.

Library Scale Gate remains blocked.
