---
name: restaurant-poster-art-director
description: >
  Use this skill whenever the user asks to generate, design, revise, evaluate, batch-produce,
  upscale or prepare Xiaohongshu restaurant posters, restaurant brand concept posters,
  food advertising key visuals, or any “刘先生 + 餐饮品类” design case. This skill enforces
  product realism, style diversity, product-driven design, restrained use of water and smoke,
  real typography for final Chinese text, and verified 4K delivery.
---

# Restaurant Poster Art Director

## Mandatory files

Before any restaurant poster generation or revision, read in this order:

1. `generation/RESTAURANT_POSTER_IMAGE_RULES_V1.md`
2. `config/restaurant-poster-generation.v1.json`
3. `calibration/README.md`
4. `calibration/anchors.json`

If the task also asks for aesthetic scoring, additionally follow `START_HERE.md` and the personal aesthetic scoring system.

## Mission

Create high-end, young, clean, commercially credible restaurant design cases for Xiaohongshu client acquisition. The result must look like professional design work, not a generic AI poster or template.

## Non-negotiable principles

- Real product texture outranks decorative complexity.
- Product structure must generate the visual logic; the product cannot be pasted into a generic layout.
- A batch must contain genuinely different design families, not color variants of one template.
- Modern and international directions are required; restrained Eastern design is only one optional family.
- Pure black, smoke, ink painting, red seals and gold typography cannot be default shortcuts.
- AI-generated Chinese typography is draft-only. Final Chinese text must use real fonts or vector paths.
- Final delivery must have verified actual pixel dimensions, not a “4K” claim in the prompt.

## Required workflow

### 1. Resolve the brief

Record:

- brand name and category;
- platform and aspect ratio;
- number of images;
- intended customer type;
- required style diversity;
- product-specific visual source;
- whether this is a concept or ready-to-post final;
- target pixel dimensions.

### 2. Allocate style quota

For 10 images, define at least 4 style families before generating. No single style may exceed 40%. Restrained Eastern styles may not exceed 30% unless explicitly requested. Dark-black designs may not exceed 20%.

### 3. Define product-driven concept

For each poster state one sentence:

> “The layout is generated from [specific product structure/material/motion], not from a generic template.”

For grilled fish, valid sources include fish-body curvature, scoring rhythm, pan ratio, grilled texture, ingredient rhythm, sauce flow and heat-zone steam.

### 4. Generate/select product hero first

The food hero must pass anatomy, material, ingredient, pan perspective and contact-shadow inspection before any final layout work.

Immediately reject:

- multiple heads or eyes;
- fused fins or malformed tail;
- plastic, waxy or metallic fish skin;
- copied ingredients;
- glue-like sauce;
- floating product;
- impossible pan perspective;
- steam unrelated to the heat source.

### 5. Build composition

Use one primary focal point and a clear reading order:

1. brand name;
2. product hero;
3. core claim;
4. minimal supporting information.

Do not default to “headline + English subtitle + three round icons”. Do not fill the page with decorative details.

### 6. Integrate water and smoke

Water must express freshness, source or flow with restrained ripples or thin lines. Smoke must originate from the hot product or pan. Neither may dominate the product or hide defects.

### 7. Typography

Use AI-rendered text only as a composition placeholder. Before marking `READY_TO_POST`, replace all Chinese titles, wordmarks, prices and key information with real typesetting or vector paths. Reject any wrong character, fake seal, malformed stroke or gibberish.

### 8. 4K delivery

Default Xiaohongshu final:

- 2160 × 3840 px;
- PNG master;
- optional compressed JPEG publishing copy.

If native 4K is unavailable, use a two-stage process: high-quality generation → controlled super-resolution → local correction → output sharpening. Inspect at 100% zoom.

### 9. Status gate

Only mark `READY_TO_POST` when all requirements in `config/restaurant-poster-generation.v1.json` pass.

Otherwise use:

- `CONCEPT`: direction exploration only;
- `DRAFT`: typography, 4K or validation incomplete;
- `REJECTED`: product realism or design logic failed.

## Required response after a batch

Report:

- style family assigned to each image;
- product-driven design source for each image;
- actual output pixels;
- whether typography is final or placeholder;
- rejected images and exact reasons;
- which images are `READY_TO_POST`, `DRAFT`, `CONCEPT` or `REJECTED`.

Never claim all images are successful merely because generation completed.
