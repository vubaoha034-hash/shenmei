# V3 — Food Semantic Identity Gate

Status: `FROZEN_NEXT_TASK`

Repository: `vubaoha034-hash/shenmei`
Required branch: `visual-program-distillation-v2-photography-design-20260814`

## Purpose

Resolve the exact semantic identity of the current Route A real food source before any more hero-image work.

Current source:

`ast_63aa377b-5287-400d-b0a3-a6282313b38c.jpg`

Do NOT infer the dish name from image pixels alone.

## Allowed evidence

Read only existing private provenance / asset metadata / import receipts / source filename mappings that directly refer to this exact asset UUID.

You may inspect:

- exact asset registry row for this asset;
- original source filename/path metadata;
- user-provided label captured at import;
- exact generation/provenance receipts that cite this asset;
- exact private metadata sidecars for this asset.

Do not browse unrelated food assets.
Do not search the public web.
Do not guess from visual appearance.

## Required contract

If authoritative metadata is sufficient, create a private `FOOD_SEMANTIC_IDENTITY_CONTRACT` for this exact asset with:

- `asset_id`
- `canonical_dish_name`
- `primary_ingredient_or_protein`
- `cooking_method`
- `required_visible_identity_cues` (2–5)
- `forbidden_substitutions`
- `source_asset_hero_adequacy`: `PASS | CONDITIONAL | FAIL`
- `evidence_sources`
- `confidence`

Do not invent fields whose values are not supported.

## Hero adequacy rule

`PASS` only if the source itself contains enough visible information to ground a recognizable hero dish while preserving the real dish identity.

`CONDITIONAL` if semantic metadata is known but the source is visually weak/ambiguous and would require careful imagegen reconstruction to become legible.

`FAIL` if the source cannot safely support a hero representation without materially hallucinating what the dish should look like.

## Fail-closed rule

If authoritative metadata cannot resolve the exact dish name and primary ingredient, return:

`V3_FOOD_SEMANTIC_IDENTITY_NEEDS_HUMAN_INPUT`

and list only the missing fields that must be supplied by the user.

Do not generate or edit any image.
Do not resume Production Layer Separation.
Do not modify the global compiler.
Do not change Discovery.
Do not run Library Scale Gate.

## Output

If resolved, create:

`V3_ROUTE_A_FOOD_SEMANTIC_IDENTITY_CONTRACT.json`

If unresolved, create:

`V3_ROUTE_A_FOOD_SEMANTIC_IDENTITY_BLOCKER.json`

with the exact missing fields and evidence inspected.

## Final response

Return exactly one of:

### Resolved

# V3 FOOD SEMANTIC IDENTITY RESOLVED

Branch:
HEAD:
Asset:
Canonical dish name:
Primary ingredient/protein:
Cooking method:
Hero adequacy:
Confidence:
Image generated: NO
Production Layer Pilot resumed: NO
Scale Gate executed: NO

## 已完成什么

## 未完成什么

## 下一步需要什么

### Unresolved

# V3 FOOD SEMANTIC IDENTITY NEEDS HUMAN INPUT

Branch:
HEAD:
Asset:
Authoritative metadata found:
Missing fields:
Image generated: NO
Production Layer Pilot resumed: NO
Scale Gate executed: NO

## 已完成什么

## 未完成什么

## 需要用户提供什么

Then STOP.
