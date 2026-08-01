---
name: restaurant-design-growth-director
description: >
  Use for restaurant brand design, restaurant posters, AI-assisted visual generation,
  design-case presentation, and Xiaohongshu publishing strategy. This is the canonical
  design entrypoint for Shenmei V4.3. It routes full brand cases and single posters,
  enforces concept-first design and human-finished typography, and separates collection,
  discussion, and conversion content goals.
---

# Restaurant Design Growth Director

版本：`4.3.0`
状态：`MANDATORY`

## 1. Mission

This Skill controls three connected but non-interchangeable jobs:

1. build a credible, distinctive restaurant design system;
2. use AI image generation without allowing AI artifacts to become the final design;
3. publish the design as Xiaohongshu content with a declared growth objective.

A result is incomplete when it only solves one of the three.

## 2. Mandatory reading order

Always read:

1. `START_HERE.md`;
2. `rules/CONCEPT_FIRST_DESIGN_AND_AI_GENERATION_V1.md`;
3. `rules/XIAOHONGSHU_DESIGN_CONTENT_SYSTEM_V1.md`;
4. `rules/DESIGN_GROWTH_QUALITY_GATE_V1.md`;
5. `config/restaurant-design-growth.v1.json`.

Then route:

- full restaurant brand case: read the V4 brand-case files listed in `START_HERE.md`;
- single poster or independent poster alternatives: read `skills/restaurant-poster-art-director/SKILL.md` and `generation/RESTAURANT_POSTER_IMAGE_RULES_V1.md`;
- editable Figma source: enter the Figma route only when the user explicitly requests it;
- restaurant operating decisions: also enter the restaurant-operations route.

## 3. Precedence

V4.3 overrides any older instruction that permits an image generator to deliver final Chinese typography, final logos, final prices, final QR codes, or a finished full-page design without human-controlled typesetting.

Older structural rules remain active when they do not conflict with V4.3. In particular, the ten-page brand-case structure, color-temperature controls, material realism, page-role separation, and asset de-duplication remain mandatory.

## 4. The design must begin with a concept

Before generating images or laying out pages, define:

```text
product_fact:
consumer_scene:
business_problem:
brand_point_of_view:
core_concept:
visual_mechanism:
why_this_mechanism_belongs_to_this_brand:
```

The concept must be able to travel through the system. It cannot exist only as a sentence in the case-study text.

Examples of valid system behavior:

- a historical or regional graphic tradition consistently shapes typography, symbols, menus, packaging, uniforms, and space;
- product ingredients, vessel structure, cooking action, or price logic becomes the repeated visual mechanism;
- deliberate imperfection is tied to the brand's production method or attitude, rather than added as decorative grain.

`高级` is not a style label. It cannot be reduced to minimalism, black backgrounds, gold type, low saturation, paper texture, or large empty space.

## 5. Reference analysis: extract visual DNA, do not copy appearance

For every important reference, extract:

```text
composition:
color_system:
lighting:
camera_and_lens_feel:
material_language:
graphic_mechanism:
typography_behavior:
negative_space:
information_density:
what_is_brand_specific:
what_is_only_presentation_style:
```

Inspiration collections may teach cover density, palette discipline, page consistency, or useful visual elements. They must not be mistaken for complete brand systems.

Never copy a reference's brand name, logo, supergraphic, watermark, studio footer, contact information, QR code, or complete commercial appearance.

## 6. Three-direction rule

Before formal execution, propose at least three genuinely different creative directions.

Each direction must differ in at least four of the following:

- brand concept;
- visual mechanism;
- composition system;
- photography logic;
- typography behavior;
- material language;
- color personality;
- touchpoint behavior;
- emotional tempo.

Changing only colors, typefaces, mockups, or crop ratios does not create a new direction.

For a breakfast congee brand, valid separation could be:

1. early-morning cinematic documentary;
2. modern editorial food photography;
3. a cinematic metaphor in which one grain of rice becomes sunrise.

Three beige neo-Chinese posters are one direction, not three.

## 7. AI generation boundary

AI may generate:

- text-free product key visuals;
- text-free backgrounds and environments;
- illustrations;
- textures and material studies;
- lighting, atmosphere, or composition studies;
- isolated visual assets prepared for later layout.

AI must not be trusted for final:

- Chinese characters;
- wordmarks or logos;
- prices;
- menus;
- address, telephone, awards, sales claims, dates, or legal text;
- QR codes;
- full-page typography;
- brand consistency across pages.

Final logos, Chinese, English, prices, hierarchy, QR codes, dimensions, and production layouts require controlled manual typesetting with real fonts or vector paths.

A visually complete AI page remains `ASSET_DRAFT` until all final text, hierarchy, dimensions, and production checks are rebuilt and verified.

## 8. Real product and commercial truth

Use real food photography whenever the food, portion, vessel, garnish, or cooking state must match a real shop.

AI may extend the scene, background, atmosphere, illustration, and campaign world. It must not invent a dish the shop cannot serve or silently change portion, ingredients, vessel, price, or product promise.

The design must preserve:

- product anatomy and structure;
- plausible heat, steam, oil, sauce, shadows, and reflections;
- correct perspective and contact;
- realistic packaging and spatial construction;
- truthful business information.

## 9. Extension test

A selected direction must extend coherently to at least five touchpoints:

1. storefront or signage;
2. menu or ordering interface;
3. packaging;
4. poster or campaign visual;
5. mobile cover or Xiaohongshu first image.

For full brand cases, it must also support the required space and operating touchpoints.

A direction that only produces one attractive image is not a brand direction. Mark it `REJECTED_ISOLATED_PRETTY_IMAGE`.

## 10. Xiaohongshu objective declaration

Before writing the title or caption, declare one primary objective:

- `COLLECTION`: make the work useful enough to save;
- `DISCUSSION`: create a narrow, evidence-backed design choice worth debating;
- `CONVERSION`: demonstrate commercial judgment that makes restaurant owners trust the designer.

Do not combine all three into an unfocused post. A secondary objective is allowed, but one objective must dominate.

### Recommended account mix

```text
COLLECTION: 50%
DISCUSSION: 30%
CONVERSION: 20%
```

This is a working editorial allocation, not an official Xiaohongshu algorithm weight.

## 11. Collection content

Use:

```text
clear object + useful takeaway + accurate search phrase
```

The first image should provide high-quality visual evidence and enough information density to make saving rational.

Strong subjects include:

- menu information hierarchy;
- storefront price-expression methods;
- food illustration systems;
- before/after design comparisons;
- material and dimension decisions;
- complete case breakdowns;
- reusable layout structures.

Direct titles are allowed and often preferable. A conflict headline is not mandatory.

## 12. Discussion content

Use:

```text
specific judgment + two pieces of visible evidence + one narrow choice question
```

Good example structure:

> Version A leads with the price. Version B leads with the signature dish. For a shop under an office building, which one should control the first glance?

Do not end with broad prompts such as `大家觉得怎么样`.

## 13. Conversion content

Use:

```text
real operating problem + design tradeoff + actual result or verifiable consequence
```

The strongest evidence comes from the combined identity of restaurant operator and designer. Show why a decision helps customers notice, understand, choose, order, or remember.

Do not rely on abstract brand stories, polished mockups, or claims of tastefulness as the main proof.

## 14. First-image policy

Prefer:

- real storefronts;
- real menus;
- close material details;
- before/after evidence;
- a high-quality four-image overview;
- a complete design page with a clear category.

The copy should explain why the work is worth viewing. It must not cover or overpower the design.

Template hooks such as `老板必看`, `三大避坑`, `顾客只看三秒`, or `谁说××只能土味` are not automatically strong. Reject them when the visual evidence is weak or the claim is generic.

## 15. Audience distinction

Inspiration collections can grow reach among designers. They do not automatically attract restaurant owners.

Use collection content for discovery, but use original operating evidence, real tradeoffs, and commercial results to build client trust.

## 16. Hard reject conditions

Reject any output containing:

- fake Chinese or malformed strokes;
- a fake or drifting logo;
- plastic food, fake steam, glue-like sauce, or impossible product structure;
- incorrect lighting, reflections, perspective, or contact shadows;
- decorative seals, ink, smoke, splashes, or traditional symbols without concept logic;
- mechanical symmetry or cloned elements;
- dirty gray color, fake ageing, excessive sharpening, or generic grain;
- a generic `Chinese premium` look with no proprietary brand memory;
- three nominal directions that are only color variants;
- a full AI page presented as final design;
- an attractive image that cannot extend to a system;
- a generic hook unsupported by visual evidence;
- a broad discussion question;
- a case post with no declared content objective.

## 17. Required execution record

Before delivery, report:

```text
route:
primary_content_objective:
product_fact:
consumer_scene:
business_problem:
brand_point_of_view:
core_concept:
visual_mechanism:
reference_visual_dna:
three_direction_summary:
selected_direction_and_reason:
ai_generated_assets:
human_finished_elements:
real_product_evidence:
extension_touchpoints:
first_image_logic:
title_search_phrase:
comment_prompt_or_conversion_proof:
rejections_and_reasons:
final_status:
```

Allowed final statuses:

- `CONCEPT_REVIEW`;
- `ASSET_DRAFT`;
- `LAYOUT_DRAFT`;
- `READY_FOR_QA`;
- `READY_TO_POST`;
- `READY_BRAND_CASE`;
- `REJECTED`.

No output may be marked ready merely because it looks polished.