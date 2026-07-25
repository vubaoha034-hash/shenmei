# Repository instructions for Codex

This repository implements two strict systems:

1. an auditable personal aesthetic scoring system;
2. a mandatory restaurant poster generation and delivery system.

## Mandatory routing

- Read `START_HERE.md` before evaluating, generating, revising, upscaling or preparing any image.
- For restaurant poster work, read `skills/restaurant-poster-art-director/SKILL.md`, `generation/RESTAURANT_POSTER_IMAGE_RULES_V1.md` and `config/restaurant-poster-generation.v1.json` before taking action.
- For aesthetic scoring, read the personal aesthetic critic skill, category rubric and penalty configuration before assigning numbers.
- Mixed generation-and-evaluation tasks must execute both workflows.

## Restaurant poster generation behavior

- Do not default every design to Chinese ink, calligraphy, red seals, black backgrounds or gold typography.
- For batches, allocate style families before generation and enforce the configured diversity quotas.
- The product must generate the design logic. Do not paste food into a generic template.
- Reject any fish with invalid anatomy, duplicate heads or eyes, fused fins, plastic skin, copied ingredients, glue-like sauce, incorrect pan perspective or physically implausible steam.
- Water and smoke must follow physical and conceptual logic. They may not dominate the product or conceal defects.
- AI-generated Chinese typography is concept-only. Final Chinese titles, wordmarks, prices and key information require real fonts or vector paths.
- Do not mark a design `READY_TO_POST` until actual 4K pixel dimensions and 100% zoom inspection are verified.
- Default Xiaohongshu master size is `2160 × 3840 px` PNG unless the user specifies another format or ratio.
- If native 4K output is unavailable, use a controlled generation → super-resolution → local correction → output sharpening workflow.
- Report rejected images honestly and give the exact failure reason. Completion of generation is not evidence of quality.

## Aesthetic scoring behavior

- Never output an `OFFICIAL` score until the JSON record passes `scripts/validate_evaluation.py`.
- When evaluating the same image twice, run `scripts/compare_evaluations.py` and reject unstable results.
- Never score `personal_fit` without valid same-category anchors from `calibration/anchors.json`.
- Never infer the user's private preference from demographic information or generic popularity.
- Never upload private photos or personal calibration samples while repository visibility is public.
- Do not silently change weights, score bands, penalties, caps, confidence logic, anchor rules or generation gates. Increase the relevant version and explain the migration.

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

- `READY_TO_POST`: realism, design, typography and actual 4K checks pass.
- `CONCEPT`: direction exploration only.
- `DRAFT`: typography, validation or 4K verification incomplete.
- `REJECTED`: product realism, anatomy or design logic failed.

## Editing priorities

When improving this repository, preserve in this order:

1. repeatability;
2. evidence traceability;
3. product realism;
4. generation rule enforcement;
5. task-specific category rules;
6. personal calibration integrity;
7. ease of use.

A more complex formula or prompt is not automatically better. Prefer explicit, testable rules over vague sophistication.
