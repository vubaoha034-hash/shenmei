---
name: restaurant-image-material-director
description: >
  Use after a restaurant brand concept engine passes to generate and inspect no-text food,
  ingredient, craft, material, packaging-model and space assets. It forbids complete page
  generation and prepares clean visual material for Figma layout.
---

# Restaurant Image Material Director

## Mandatory reads

1. `restaurant_design_system/FIGMA_FIRST_NO_ADOBE_PIPELINE_V1.md`;
2. current `CONCEPT_ENGINE.md`;
3. current `VISUAL_DNA.md`;
4. current `ASSET_PLAN.md`;
5. `generation/RESTAURANT_POSTER_IMAGE_RULES_V1.md` only for product-realism checks;
6. relevant calibration anchors.

## Mission

Generate usable visual assets, not finished brand pages. Every output must be suitable for later placement, crop and real-text composition in Figma.

## Allowed asset families

- product hero photography;
- product detail and cut-section photography;
- ingredient photography;
- craft/process photography;
- material close-ups;
- blank packaging structure concepts;
- blank storefront and space concepts;
- restrained illustration or graphic-motif studies.

## Forbidden content

Every generation prompt must forbid:

- Chinese or English text;
- logos and wordmarks;
- prices;
- QR codes;
- phone numbers and addresses;
- page numbers and portfolio headers;
- full posters, moodboards, brand boards or presentation layouts;
- multi-page triptychs and nine-grid compositions;
- fake labels and decorative seals.

If a generated asset contains critical fake text, reject it. Do not crop or cover it for reuse.

## Asset-plan contract

Before generation, each asset must define:

- `asset_id`;
- intended page and role;
- subject;
- composition and required negative space;
- camera position and crop flexibility;
- light direction and hardness;
- palette and background;
- physical material rules;
- must-preserve details;
- reject conditions;
- brand evidence source.

## Product audit

Check at 100% when resolution permits:

- correct number and shape;
- anatomy and cut section;
- ingredient variety without copied repetition;
- contact with bowl, plate, tray or wrapper;
- realistic oil, sauce, moisture and steam;
- believable edge, shadow and depth;
- no plastic, waxy, metallic or rubber texture;
- no impossible utensil, hand or packaging interaction.

## Packaging and space audit

Packaging:

- structure can open and close;
- lid and body align;
- seal location is plausible;
- materials match the food and transport need;
- no fake production dieline claims.

Space:

- storefront, entry and circulation are legible;
- scale and perspective are plausible;
- signage areas remain blank or neutral for Figma placement;
- lighting is physically coherent;
- no generic restaurant scene with a fake logo applied.

## Output manifest

Write `ASSET_MANIFEST.json` with:

- asset_id;
- source tool;
- actual dimensions;
- AI-generated boolean;
- text_present boolean;
- audit result;
- reject reason;
- intended Figma page;
- final selected boolean.

## Status

- `ASSET_DRAFT`;
- `ASSET_READY`;
- `REJECTED_FAKE_TEXT`;
- `REJECTED_PRODUCT_STRUCTURE`;
- `REJECTED_PACKAGING_LOGIC`;
- `REJECTED_SPACE_LOGIC`.

## Hard stop

This skill must never output or approve a complete brand proposal page. Any full-page image-generator result is `REJECTED_AI_FULL_PAGE`.
