---
name: restaurant-brand-portfolio-layout
description: >
  Use to create the editable Figma three-page proof and ten-page restaurant brand portfolio.
  It owns real typography, variables, components, grids, image placement, page variation,
  node tracking and export. It replaces image-generator full-page layouts.
---

# Restaurant Brand Portfolio Layout

## Mandatory reads

1. `restaurant_design_system/FIGMA_FIRST_NO_ADOBE_PIPELINE_V1.md`;
2. `restaurant_design_system/PORTFOLIO_PRESENTATION_RULES_V1.md`;
3. current `BRAND_STRATEGY.md`;
4. current `VISUAL_DNA.md`;
5. current `ASSET_MANIFEST.json`;
6. current `THREE_PAGE_PROOF.md` or `TEN_PAGE_STORYBOARD.md`;
7. Figma `figma-create-new-file` and `figma-use` skill guidance before tool calls.

## Mission

Build a real, editable brand presentation in Figma. Do not ask the user to manually lay out pages.

## Figma file creation

If no project Figma file exists:

1. call Figma `whoami`;
2. select the only available plan, or ask the user only when multiple plans exist;
3. call `create_new_file` with editor type `design`;
4. record file key and URL immediately.

If a file exists, reuse it.

## Required Figma structure

Create pages or sections:

```text
00_TOKENS_COMPONENTS
01_THREE_PAGE_PROOF
02_TEN_PAGE_PORTFOLIO
03_EXPORT_CHECK
99_REJECTED_ARCHIVE
```

Create variables or reusable constants for:

- primary, accent, neutral and background colors;
- safe margin;
- header/footer height;
- spacing scale;
- border and line weights;
- image corner rule;
- text hierarchy.

Create text styles for:

- Chinese brand wordmark direction;
- chapter number;
- chapter title;
- main claim;
- supporting heading;
- body copy;
- caption and audit note;
- English support text.

Create components for:

- page header/footer;
- chapter number;
- status label;
- brand signature;
- image frame;
- annotation/caption;
- palette chip;
- material chip.

## Three-page proof

First build only:

1. brand concept and hero visual;
2. wordmark and super symbol;
3. strongest application.

Requirements:

- frames use actual intended dimensions;
- all key text is real editable text;
- at least two layout archetypes;
- one visual conclusion per page;
- no fake dates, phone numbers, addresses or QR codes;
- no generic footer fields added only to appear professional;
- no reference-company logo, watermark or page shell;
- no screenshot of an AI-generated full page.

Record every frame node ID in `FIGMA_MANIFEST.json`.

## Ten-page expansion

Only after `THREE_PAGE_PROOF_PASS`:

- create ten separate frames;
- use at least four layout archetypes;
- do not use the same archetype more than twice consecutively;
- keep shared tokens and components;
- vary image scale, crop and narrative role;
- preserve one chapter per page;
- each page must show a result, a method/detail and an application proof when relevant;
- no page may become a miniature overview of all touchpoints.

## Image placement

Use selected assets from `ASSET_MANIFEST.json` only.

- upload assets to Figma;
- preserve product anatomy and intended crop;
- do not stretch images;
- do not hide AI defects with text or overlays;
- avoid using one hero asset on more than three pages unless the repetition is intentional and documented;
- label AI concept imagery in a real-text caption when needed.

## Export

Each final frame must have export settings.

Record:

- node ID;
- natural frame size;
- exported size;
- format;
- export URL or local path;
- export verification status.

Concept pages may be below 4K only when actual dimensions are disclosed. `READY_TO_POST_SET` requires verified 2160 × 3840 or user-specified dimensions.

## Figma manifest schema

`FIGMA_MANIFEST.json` must contain:

```json
{
  "file_url": "",
  "file_key": "",
  "editor_type": "design",
  "tokens_page_node_id": "",
  "three_page_proof": [],
  "ten_page_portfolio": [],
  "fonts_used": [],
  "variables_created": [],
  "components_created": [],
  "export_status": "",
  "actual_export_dimensions": {}
}
```

## Hard rules

- No Figma file and node IDs means no `CONCEPT_SET`.
- Do not use image-generation models for page typography.
- Do not import a generated full-page board and call it editable layout.
- Do not ask the user to complete layout work manually.
- Do not continue to ten pages after the proof fails.
- Every visible Chinese character must be real editable text or a deliberate vector wordmark direction.

## Status

- `FIGMA_FILE_READY`;
- `THREE_PAGE_PROOF`;
- `TEN_PAGE_LAYOUT`;
- `EXPORT_PENDING`;
- `EXPORT_VERIFIED`;
- `BLOCKED_FIGMA_ACCESS`.
