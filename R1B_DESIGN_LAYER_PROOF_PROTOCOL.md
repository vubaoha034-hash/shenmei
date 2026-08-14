# R1B — DESIGN LAYER PROOF

Status: `PRE_REGISTERED / NOT_STARTED`
Date: `2026-08-14`

## Purpose

R1A established that a real-photo-first image-conditioned workflow can materially improve food realism, but the resulting candidate still failed as a commercial hero because the design layer was weak.

R1B tests only one question:

> Can a frozen, already-realistic food asset become a genuinely usable restaurant hero visual when image generation is removed from the design/layout step and the page is composed as editable graphic design?

This is not a new food-generation test.

---

## Frozen food asset

Use exactly the existing R1 candidate:

`R1_SINGLE_DISH_HERO_CANDIDATE.png`

Drive file id:

`1ptSMiN7b88DEvbmWdQ7l4Td_BTo-PWh8`

Rules:

- do not redraw the food;
- do not image-generate another dish;
- do not inpaint/replace food structure;
- allow only crop, scale, position and non-destructive tonal matching in the design layer;
- preserve food pixels as the source visual asset.

The asset is not declared production-perfect food photography. It is only frozen for this design-layer diagnostic.

---

## Design tool boundary

The final page must be built as editable layout/design, preferably Figma.

Image generation must not create the complete page.

Allowed design-layer operations:

- canvas and grid;
- crop and image placement;
- color fields;
- vector geometry;
- masks;
- spacing and alignment;
- real typography;
- hierarchy;
- intentional negative space;
- small vector accents if justified;
- background/tone fields that do not redraw the food.

Forbidden:

- another image-generation call for the food;
- generated Chinese text;
- fake seals;
- generic brush-stroke decoration;
- generic ink/watercolor decoration;
- AI-generated full-page poster;
- multiple alternatives;
- logo system expansion;
- packaging expansion;
- brand portfolio expansion.

---

## One-output rule

R1B produces exactly one editable hero design.

No variants.
No best-of-N.
No second layout after seeing the first.
No automatic retry for taste.

---

## Design brief

Build a mature restaurant single-dish hero visual around the frozen food asset.

The page should feel like real contemporary commercial graphic design rather than an AI poster template.

The design must solve:

1. attention geometry;
2. strong but controlled crop;
3. usable negative space;
4. clear typographic hierarchy;
5. one coherent color logic;
6. a distinctive but restrained graphic mechanism;
7. commercial legibility;
8. no generic East-Asian cliché shorthand.

The food remains the hero, but the page must also have a recognizable visual structure that could plausibly extend into a brand system.

---

## Text policy

Use real editable text only.

For this proof, keep text minimal.

Required text:

- main title: `今日现烧`
- supporting line: `锅气刚好，趁热吃`

Do not invent prices, addresses, QR codes, dates, English filler or brand claims.

If the exact font requested is unavailable, use a real installed Chinese sans/serif with clear fallback disclosure. Never generate text as pixels.

---

## Art-direction constraint

Do not solve the page by adding more decoration.

Prefer:

- strong crop;
- controlled scale contrast;
- one graphic device;
- real whitespace;
- restrained color fields;
- coherent typography.

Avoid:

- red brush strokes;
- ink wash;
- red seals;
- faux rice paper;
- generic leaves;
- generic frame boxes;
- excessive dark premium styling;
- symmetrical template composition;
- default beige + dark brown restaurant palette.

---

## Figma requirement

Use the existing Figma file created for this proof:

File key:
`IGJRXAlQLtlKXqC1ljNLGg`

File name:
`LIU_VISUAL_R1B_DESIGN_LAYER_PROOF`

The final proof must have:

- one 4:5 frame;
- editable real text;
- editable vector design elements;
- frozen food image as a placed raster asset;
- no second alternative frame;
- one export PNG for review.

---

## Quality review

After design is complete:

1. export exactly one PNG;
2. upload to `LIU_VISUAL_REVIEW/R1B/`;
3. stop;
4. ChatGPT independently reads the exported pixels;
5. user judges `USABLE / UNUSABLE`.

Codex may verify technical integrity but may not declare visual success.

---

## Pass meaning

R1B passes only if the user judges the design usable or close enough that the core design concept does not need to be rebuilt from scratch.

If the user says the page still looks generic, weak, templated or fundamentally needs redesign:

`R1B = FAIL / DESIGN_LAYER_BOTTLENECK`

Do not proceed to packaging or a larger brand system.

---

## Stop rule

After one output and review handoff:

STOP.

Do not start R2/R3.
Do not modify Discovery.
Do not generate new food.
Do not create extra alternatives.
