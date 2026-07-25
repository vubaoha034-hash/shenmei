# Repository instructions for Codex

This repository implements a strict, auditable personal aesthetic scoring system.

## Mandatory behavior

- Read `START_HERE.md` before evaluating any image or changing scoring logic.
- Read the category rubric and penalty configuration before assigning numbers.
- Never output an `OFFICIAL` score until the JSON record passes `scripts/validate_evaluation.py`.
- When evaluating the same image twice, run `scripts/compare_evaluations.py` and reject unstable results.
- Never score `personal_fit` without valid same-category anchors from `calibration/anchors.json`.
- Never infer the user's private preference from demographic information or generic popularity.
- Never upload private photos or personal calibration samples while repository visibility is public.
- Do not silently change weights, score bands, penalties, caps, confidence logic, or anchor rules. Increase the relevant version and explain the migration.

## Standard commands

```bash
python scripts/validate_evaluation.py evaluations/example.json
python scripts/compare_evaluations.py evaluations/run-1.json evaluations/run-2.json
```

## Evaluation status

- `OFFICIAL`: validator PASS.
- `DRAFT`: incomplete or unvalidated.
- `NO_SCORE`: input quality or required evidence is insufficient.

## Editing priorities

When improving this repository, preserve in this order:

1. repeatability;
2. evidence traceability;
3. task-specific category rules;
4. personal calibration integrity;
5. ease of use.

A more complex scoring formula is not automatically better. Prefer explicit, testable rules over vague sophistication.
