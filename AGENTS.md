# Repository instructions for Codex

This repository implements three strict systems:

1. a domestic Chinese restaurant brand-case generation system;
2. a mandatory restaurant poster generation and delivery system;
3. an auditable personal aesthetic scoring system.

## Mandatory routing

- Read `START_HERE.md` before evaluating, generating, revising, upscaling or preparing any image.
- For a new domestic restaurant brand concept or a ten-image case set, read all files under `restaurant_design_system/` in the order defined by `restaurant_design_system/START_HERE.md`.
- For restaurant poster work, also read `skills/restaurant-poster-art-director/SKILL.md`, `generation/RESTAURANT_POSTER_IMAGE_RULES_V1.md` and `config/restaurant-poster-generation.v1.json` before taking action.
- For aesthetic scoring, read the personal aesthetic critic skill, category rubric and penalty configuration before assigning numbers.
- Mixed planning, generation and evaluation tasks must execute all relevant workflows.

## Domestic restaurant brand-case behavior

- Keep the project grounded in Chinese restaurant categories, customers, menu logic, price tiers, service flow and commercial context unless the user explicitly requests a foreign restaurant project.
- Do not interpret “different styles” as “convert the project into a foreign food brand.” International graphic design language is allowed; foreign restaurant context is not the default.
- Do not interpret “domestic restaurant” as “always use traditional Chinese aesthetics.” Ink wash, calligraphy, red seals, cream backgrounds, wooden interiors and light Eastern minimalism are optional style families only.
- Choose a category, brand persona, style family, target customer, price tier, service scene and product-driven motif before generation.
- Read recent project records and avoid repeating the previous category or style family.
- Follow the diversity quotas in `restaurant_design_system/config/domestic-restaurant-directions.v1.json`.
- “Tian Xiao Gou type” means an original, warm, personality-led or light-IP neighborhood restaurant concept. Never copy an existing brand name, character, slogan, typography or trade dress.
- Every standard case contains exactly ten independent image tasks as defined in `restaurant_design_system/OUTPUT_STRUCTURE_10_IMAGES_V1.md`.
- Do not substitute one collage board for ten independent deliverables.

## Restaurant poster generation behavior

- Do not default every design to Chinese ink, calligraphy, red seals, black backgrounds or gold typography.
- For batches, allocate style families before generation and enforce the configured diversity quotas.
- The product must generate the design logic. Do not paste food into a generic template.
- Reject any food with invalid anatomy, duplicate parts, plastic texture, copied ingredients, glue-like sauce, incorrect container perspective or physically implausible steam.
- Water, smoke and fire must follow physical and conceptual logic. They may not dominate the product or conceal defects.
- AI-generated Chinese typography is concept-only. Final Chinese titles, wordmarks, prices and key information require real fonts or vector paths.
- Packaging must be structurally manufacturable; menus must be readable and orderable; signage must use coherent arrows, wording and spatial logic.
- Do not mark a design `READY_TO_POST` until actual 4K pixel dimensions and 100% zoom inspection are verified.
- Default Xiaohongshu master size is `2160 × 3840 px` PNG unless the user specifies another format or ratio.
- If native 4K output is unavailable, use a controlled generation → super-resolution → local correction → output sharpening workflow.
- Report rejected images honestly and give the exact failure reason. Completion of generation is not evidence of quality.

## AI-signature rejection behavior

Reject or downgrade any output that shows:

- fake Chinese or fabricated prices;
- a foreign restaurant concept without user instruction;
- repeated light-Eastern, black-gold, cream-paper or generic branding templates;
- plastic food, repeated ingredients or impossible food anatomy;
- inconsistent logos across applications;
- unusable menus, impossible packaging or incorrect spatial scale;
- over-perfect render scenes with identical materials and lighting;
- decorative smoke, water or fire used to hide defects;
- low-resolution files presented as 4K.

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

- `PLANNED`: project brief and direction are defined.
- `READY_TO_POST_SET`: all ten independent images pass.
- `READY_TO_POST`: one image passes realism, design, typography and actual 4K checks.
- `CONCEPT`: direction exploration only.
- `DRAFT`: typography, validation or 4K verification incomplete.
- `REJECTED`: product realism, anatomy, brand logic, diversity or design logic failed.

## Editing priorities

When improving this repository, preserve in this order:

1. repeatability;
2. evidence traceability;
3. domestic market correctness;
4. product realism;
5. style diversity;
6. AI-signature rejection;
7. generation rule enforcement;
8. task-specific category rules;
9. personal calibration integrity;
10. ease of use.

A more complex formula or prompt is not automatically better. Prefer explicit, testable rules over vague sophistication.
