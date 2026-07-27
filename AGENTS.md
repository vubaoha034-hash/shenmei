# Repository instructions for Codex

This repository implements three strict systems:

1. a domestic Chinese restaurant brand-case generation system;
2. a mandatory restaurant poster generation and delivery system;
3. an auditable personal aesthetic scoring system.

## Mandatory routing

- Read `START_HERE.md` before evaluating, generating, revising, upscaling or preparing any image.
- For a new domestic restaurant brand concept or ten-image case set, read all files in the order defined by `restaurant_design_system/START_HERE.md`.
- The current authoritative brand files are `BRAND_CREATIVE_DIRECTOR_RULES_V2.md`, `OUTPUT_STRUCTURE_10_IMAGES_V2.md`, `DAILY_WORKFLOW_V2.md` and `GLOBAL_FEEDBACK_RULES_V1.md`.
- For restaurant poster work, also read `skills/restaurant-poster-art-director/SKILL.md`, `generation/RESTAURANT_POSTER_IMAGE_RULES_V1.md` and `config/restaurant-poster-generation.v1.json`.
- For aesthetic scoring, read the personal aesthetic critic skill, category rubric and penalty configuration before assigning numbers.
- Mixed planning, generation and evaluation tasks must execute all relevant workflows.

## Creative-director behavior

- The task is to design one brand system, not to generate ten attractive but unrelated images.
- Before generation, create a brand strategy card and a seven-part visual DNA card.
- Validate the wordmark, the primary poster and the storefront or wall visual before producing the full ten-image set.
- Reference images are for extracting strategy, visual grammar, material logic and system depth. Never copy names, slogans, typography, characters, layouts or trade dress.
- Every image must include a `brand_evidence` explanation showing why it belongs to the brand beyond displaying the logo.
- Proactively provide at least three directions, recommend one, explain risks and suggest improvements. Do not wait for the user to identify every problem.
- Stop batch generation when the strategy, visual DNA or three key touchpoints do not form a coherent brand.

## Domestic restaurant brand-case behavior

- Keep the project grounded in Chinese restaurant categories, customers, menu logic, price tiers, service flow and commercial context unless the user explicitly requests a foreign restaurant project.
- Do not interpret “different styles” as “convert the project into a foreign food brand.” International graphic design language is allowed; foreign restaurant context is not the default.
- Do not interpret “domestic restaurant” as “always use traditional Chinese aesthetics.” Ink wash, calligraphy, red seals, cream backgrounds, wooden interiors and light Eastern minimalism are optional style families only.
- Choose a category, brand persona, style family, target customer, price tier, service scene, specific brand promise and product-driven motif before generation.
- Read recent project records and avoid repeating the previous category, persona, palette, layout, storefront, packaging or style family.
- A new concept must visibly change at least four major dimensions from the latest projects, and at least two of main style, primary palette or brand persona.
- Follow `GLOBAL_FEEDBACK_RULES_V1.md`, including the default rejection of the black-red stainless-steel neon wok template unless explicitly requested.
- “Tian Xiao Gou type” means an original, warm, personality-led or light-IP neighborhood restaurant concept. Never copy an existing brand name, character, slogan, typography or trade dress.
- Every standard case contains exactly ten independent image tasks as defined in `OUTPUT_STRUCTURE_10_IMAGES_V2.md`.
- Do not substitute one collage board for ten independent deliverables.

## Ten-image output

1. primary brand poster;
2. shop-name poster / logo / wordmark;
3. brand theme poster;
4. signature product poster;
5. in-store wall poster series;
6. storefront / shop-name spatial application;
7. fast-food takeaway box;
8. paper bag and utensil packaging system;
9. menu or tabletop operational touchpoint;
10. brand visual overview.

## Restaurant poster generation behavior

- Do not default every design to Chinese ink, calligraphy, red seals, black backgrounds or gold typography.
- For batches, allocate style families before generation and enforce diversity quotas.
- The product must generate design logic. Do not paste food into a generic template.
- Reject any food with invalid anatomy, duplicate parts, plastic texture, copied ingredients, glue-like sauce, incorrect container perspective or physically implausible steam.
- Water, smoke and fire must follow physical and conceptual logic. They may not dominate the product or conceal defects.
- AI-generated Chinese typography is concept-only. Final Chinese titles, wordmarks, prices and key information require real fonts or vector paths.
- AI is suitable for food-photo assets, lighting exploration and spatial concept images. Figma, Adobe or vector tools must handle logos, typography, menus, packaging dielines, signage and final 4K layout.
- Packaging must be structurally manufacturable; menus must be readable and orderable; signage must use coherent arrows, wording and spatial logic.
- Do not mark a design `READY_TO_POST` until actual 4K pixel dimensions and 100% zoom inspection are verified.
- Default Xiaohongshu master size is `2160 × 3840 px` PNG unless the user specifies another format or ratio.
- If native 4K output is unavailable, use a controlled generation → super-resolution → local correction → output sharpening workflow.
- Report rejected images honestly. Completion of generation is not evidence of quality.

## AI-signature rejection behavior

Reject or downgrade outputs that show:

- fake Chinese or fabricated prices;
- a foreign restaurant concept without user instruction;
- repeated light-Eastern, cream-olive-wood community, black-gold, black-red industrial-neon or generic branding templates;
- plastic food, repeated ingredients or impossible food anatomy;
- inconsistent logos across applications;
- unusable menus, impossible packaging or incorrect spatial scale;
- over-perfect render scenes with identical materials and lighting;
- decorative smoke, water or fire used to hide defects;
- low-resolution files presented as 4K;
- an image that cannot prove brand ownership beyond the logo.

## Aesthetic scoring behavior

- Never output an `OFFICIAL` score until the JSON record passes `scripts/validate_evaluation.py`.
- When evaluating the same image twice, run `scripts/compare_evaluations.py` and reject unstable results.
- Never score `personal_fit` without valid same-category anchors from `calibration/anchors.json`.
- Never infer the user's private preference from demographic information or generic popularity.
- Never upload private photos or personal calibration samples while repository visibility is public.
- Do not silently change weights, score bands, penalties, caps, confidence logic, anchor rules, category libraries, diversity quotas or generation gates. Increase the relevant version and explain the migration.

## Standard commands

```bash
python scripts/validate_evaluation.py evaluations/example.json
python scripts/compare_evaluations.py evaluations/run-1.json evaluations/run-2.json
```

## Evaluation status

- `OFFICIAL`: validator PASS.
- `DRAFT`: incomplete or unvalidated.
- `NO_SCORE`: input quality or required evidence is insufficient.

## Generation status

- `PLANNED`: brand strategy and visual DNA are defined.
- `CONCEPT`: direction exploration only.
- `DRAFT`: typography, validation, brand evidence or 4K verification incomplete.
- `READY_TO_POST`: one image passes realism, design, typography and actual 4K checks.
- `READY_TO_POST_SET`: all ten independent images pass.
- `REJECTED`: product realism, brand logic, anti-repetition, AI signature or application logic failed.

## Editing priorities

Preserve in this order:

1. brand strategy specificity;
2. visual-system coherence;
3. repeatability;
4. evidence traceability;
5. domestic market correctness;
6. product realism;
7. style diversity;
8. AI-signature rejection;
9. generation rule enforcement;
10. personal calibration integrity.

A more complex formula or prompt is not automatically better. Prefer explicit, testable rules over vague sophistication.
