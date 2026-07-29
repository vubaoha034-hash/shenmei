---
name: restaurant-poster-art-director
description: >
  Use for a single restaurant poster, food advertising key visual, product hero, or a batch
  of independent poster alternatives. Do not use this skill to control a ten-page brand
  portfolio; restaurant brand systems must route through the Figma-first pipeline.
---

# Restaurant Poster Art Director

## Scope boundary

This Skill applies to:

- one restaurant poster;
- one product hero visual;
- one food advertising key visual;
- several independent poster alternatives;
- product-realism inspection for brand-project visual assets.

It does **not** apply to:

- ten-page restaurant brand portfolios;
- brand strategy and naming;
- Logo and wordmark systems;
- Figma portfolio layout;
- multi-touchpoint brand continuity.

For those tasks, read and execute:

`restaurant_design_system/FIGMA_FIRST_NO_ADOBE_PIPELINE_V1.md`

## Mandatory files

For a single poster or independent poster batch, read:

1. `generation/RESTAURANT_POSTER_IMAGE_RULES_V1.md`;
2. `config/restaurant-poster-generation.v1.json`;
3. `calibration/README.md`;
4. `calibration/anchors.json`.

For brand-project assets, use only the product, food, material, smoke, water and text-realism sections. Do not import the independent-poster style quota into one brand's ten-page portfolio.

## Mission

Create commercially credible food visuals and single posters with realistic product structure, controlled composition and real final typography.

## Non-negotiable principles

- Product realism outranks decoration.
- Product structure must influence the visual logic.
- Pure black, smoke, ink, red seals and gold typography are not default shortcuts.
- AI-generated Chinese typography is draft-only.
- Final Chinese text must use real fonts or vector paths.
- Actual output dimensions must be verified.
- Generation completion is not a pass condition.

## Independent-poster batch rule

Only when the user explicitly requests several independent poster alternatives:

- define at least four style families for ten alternatives;
- no family exceeds 40%;
- restrained Eastern styles do not exceed 30% unless requested;
- dark-black designs do not exceed 20%.

This quota must never be applied inside one coherent brand portfolio.

## Product-driven concept

For each poster or asset, state:

> The visual structure is generated from a specific product shape, material, motion, vessel or preparation action, not from a generic layout.

## Product hero audit

Reject:

- malformed anatomy or product shape;
- copied ingredients;
- plastic, waxy, rubber or metallic food texture;
- glue-like sauce;
- floating product;
- impossible bowl, pan or packaging perspective;
- steam unrelated to heat;
- fake text embedded in a reusable visual asset.

## Composition

Use one primary focal point and a clear reading order:

1. key message or brand name;
2. product hero;
3. core claim;
4. minimal support.

Do not default to “headline + English subtitle + three round icons”.

For Figma-first brand projects, generate the product hero without text and leave intentional negative space. The final reading order is built in Figma.

## Typography

- AI text is placeholder only;
- final title, wordmark, price and key information require real typesetting;
- reject wrong characters, malformed strokes, fake seals and gibberish;
- an image-generator full-page layout cannot become `READY_TO_POST` merely by looking complete.

## Delivery

Default ready-to-post Xiaohongshu output:

- 2160 × 3840 px;
- PNG master;
- optional JPEG publishing copy;
- 100% zoom inspection.

Use statuses:

- `ASSET_DRAFT` for raw brand visual material;
- `CONCEPT` for single-poster direction exploration;
- `DRAFT` for incomplete typography or resolution;
- `READY_TO_POST` only after all checks;
- `REJECTED` for realism or design failure;
- `REJECTED_AI_FULL_PAGE` when a complete brand page was generated instead of laid out in Figma.

## Required report

Report:

- product-driven source;
- actual pixels;
- whether text is placeholder or real;
- structure and material audit;
- rejected outputs and exact reasons;
- final status.
