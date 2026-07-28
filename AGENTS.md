# Repository instructions for Codex

This repository implements three strict systems:

1. a domestic Chinese restaurant brand-case generation system;
2. a mandatory restaurant poster generation and delivery system;
3. an auditable personal aesthetic scoring system.

## Mandatory routing

- Read `START_HERE.md` before evaluating, generating, revising, upscaling or preparing any image.
- For a new domestic restaurant brand concept or ten-image case set, read all files in the order defined by `restaurant_design_system/START_HERE.md`.
- The current authoritative brand files are `PHASED_DELIVERY_RULES_V1.md`, `BRAND_CREATIVE_DIRECTOR_RULES_V2.md`, `OUTPUT_STRUCTURE_10_IMAGES_V2.md`, `DAILY_WORKFLOW_V2.md` and `GLOBAL_FEEDBACK_RULES_V1.md`.
- For restaurant poster work, also read `skills/restaurant-poster-art-director/SKILL.md`, `generation/RESTAURANT_POSTER_IMAGE_RULES_V1.md` and `config/restaurant-poster-generation.v1.json`.
- For aesthetic scoring, read the personal aesthetic critic skill, category rubric and penalty configuration before assigning numbers.
- Mixed planning, generation and evaluation tasks must execute all relevant workflows.

## Phased delivery behavior

- Default daily brand work to `CONCEPT_SET` unless the user has selected a concept or supplied real production data.
- `CONCEPT_SET` may use a stable wordmark direction, explicit poster-grid specification, unmeasured storefront concept, plausible packaging concept and audited AI food visuals.
- Do not require final SVG wordmarks, true 1:20 construction drawings, supplier dielines or real food photography before generating a daily concept set.
- Do not describe concept images as construction drawings, print-ready files or production deliverables.
- Enter `DESIGN_DEVELOPMENT` only after the user selects a concept and requests refinement.
- Enter `PRODUCTION_READY` only with real storefront measurements, menu data, dielines, material and process requirements, supplier constraints and applicable real food assets.
- Always disclose actual image dimensions, whether typography is real or generated, whether food is AI or photographed, and whether measurements or dielines are real.

## Creative-director behavior

- The task is to design one brand system, not to generate ten attractive but unrelated images.
- Before generation, create a brand strategy card and a seven-part visual DNA card.
- Validate the wordmark direction, primary-poster direction and storefront or wall-visual direction at concept level before producing the full ten-image set.
- Concept validation means defining the type skeleton, proportions, grid, hierarchy, materials and recognition logic. It does not require final vector, Figma or construction files.
- Reference images are for extracting strategy, visual grammar, material logic and system depth. Never copy names, slogans, typography, characters, layouts or trade dress.
- Every image must include a `brand_evidence` explanation showing why it belongs to the brand beyond displaying the logo.
- Proactively provide at least three directions, recommend one, explain risks and suggest improvements. Do not wait for the user to identify every problem.
- Stop batch generation when the strategy, visual DNA or three concept touchpoints do not form a coherent brand.

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
2. shop-name poster / logo / wordmark direction;
3. brand theme poster;
4. signature product poster;
5. in-store wall poster series;
6. storefront / shop-name spatial concept;
7. fast-food takeaway-box concept;
8. paper-bag and utensil-packaging system;
9. menu or tabletop operational touchpoint;
10. brand visual overview.

## Restaurant poster generation behavior

- Do not default every design to Chinese ink, calligraphy, red seals, black backgrounds or gold typography.
- For batches, allocate style families before generation and enforce diversity quotas.
- The product must generate design logic. Do not paste food into a generic template.
- Reject any food with invalid anatomy, duplicate parts, plastic texture, copied ingredients, glue-like sauce, incorrect container perspective or physically implausible steam.
- Water, smoke and fire must follow physical and conceptual logic. They may not dominate the product or conceal defects.
- At `CONCEPT_SET`, AI-generated typography or food may be used only as clearly labeled concept material and must remain readable and internally consistent.
- At `DESIGN_DEVELOPMENT`, real fonts or vector paths must handle logos, Chinese typography, menus and final layouts.
- At `PRODUCTION_READY`, packaging dielines, measurements, menu data and material specifications must come from real project inputs.
- Packaging concepts must be structurally plausible; menu concepts must have coherent categories and reading hierarchy; signage concepts must use coherent arrows, wording and spatial logic.
- Do not mark a design `READY_TO_POST` until actual 4K pixel dimensions and 100% zoom inspection are verified.
- Default Xiaohongshu master size is `2160 × 3840 px` PNG unless the user specifies another format or ratio.
- If native 4K output is unavailable, use a controlled generation → super-resolution → local correction → output sharpening workflow during design development.
- Report rejected images honestly. Completion of generation is not evidence of quality.

## AI-signature rejection behavior

Reject or downgrade outputs that show:

- fake or unreadable Chinese, fabricated confirmed prices or incorrect English;
- a foreign restaurant concept without user instruction;
- repeated light-Eastern, cream-olive-wood community, black-gold, black-red industrial-neon or generic branding templates;
- plastic food, repeated ingredients or impossible food anatomy;
- inconsistent logos across applications;
- implausible packaging concepts, incoherent menu concepts or incorrect spatial scale;
- over-perfect render scenes with identical materials and lighting;
- decorative smoke, water or fire used to hide defects;
- low-resolution files presented as 4K;
- an image that cannot prove brand ownership beyond the logo;
- a concept image falsely presented as construction, print-ready or production-ready work.

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
- `CONCEPT`: one direction or touchpoint exploration.
- `CONCEPT_SET`: all ten concept images and concept audits are complete.
- `DESIGN_DEVELOPMENT`: the selected concept is being refined with real typography, vectors, grids and target output sizes.
- `DRAFT`: development work remains incomplete or unverified.
- `READY_TO_POST`: one image passes realism, design, typography and actual 4K checks.
- `READY_TO_POST_SET`: all ten independent images pass release checks.
- `PRODUCTION_READY`: real measurements, dielines, menu data, materials and supplier requirements are satisfied.
- `REJECTED`: product realism, brand logic, anti-repetition, AI signature or application logic failed.

## Editing priorities

Preserve in this order:

1. brand strategy specificity;
2. visual-system coherence;
3. honest phase labeling;
4. repeatability;
5. evidence traceability;
6. domestic market correctness;
7. product realism;
8. style diversity;
9. AI-signature rejection;
10. personal calibration integrity.

A more complex formula or prompt is not automatically better. Prefer explicit, testable rules over vague sophistication.