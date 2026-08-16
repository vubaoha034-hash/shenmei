# V3 A — Food Appetite Correction R1

Status: `FROZEN_SINGLE_ARTIFACT_CORRECTION_TASK`

Repository: `vubaoha034-hash/shenmei`
Required branch: `visual-program-distillation-v2-photography-design-20260814`

## Why this task exists

Human review identified a blocking visual defect in the selected artifact:

> the primary dish looks overcooked / burnt / visually blackened ("炒糊了，乌漆麻黑").

This invalidates the assumption that the current Art Layer is ready to freeze for production typography work.

Therefore:

- `V3_A_PRODUCTION_LAYER_SEPARATION_PILOT.md` is PAUSED;
- do not execute production-layer typography work yet;
- first correct food appetite quality while preserving the already-validated family-transfer composition.

Read first:

- `V3_A_FOOD_APPETITE_CORRECTION_RULE_V1.md`
- `V3_A_REFINED_R1_HUMAN_VALIDATION_RESULT.md`
- current selected artifact identity/provenance for `V3-A_FAMILY_TRANSFER_REFINED_R1.png`

## Exact selected artifact

Input artifact:
`V3-A_FAMILY_TRANSFER_REFINED_R1.png`

Expected SHA-256:
`95151c9d234cbfde1c2765c737602ccf224f10c68fd8172847b6db940a6bb788`

Expected dimensions:
`1024x1536`

If identity does not match, return:
`V3_A_FOOD_CORRECTION_ARTIFACT_IDENTITY_FAILURE`
and STOP.

## Source food grounding

Resolve the exact real main-dish source asset from the existing V3 Route A generation provenance / receipt. The known abbreviated identity in the prior Route A report is:
`ast_63aa…b38c.jpg`

Do not guess a replacement asset and do not browse unrelated food assets.

If the exact canonical source cannot be resolved and verified, return:
`V3_A_FOOD_CORRECTION_SOURCE_ASSET_MISSING`
and STOP.

## Formal attachment budget

Use only what is necessary:

1. current selected artifact — REQUIRED
2. exact verified real main-dish source — REQUIRED
3. Mother Reference 05 — OPTIONAL only if needed to preserve family lighting/context, not for layout redesign

Formal visual attachments <= 3.

Do not attach role crops, old benchmark outputs, or redundant exemplars.

## Correction scope

This is a selective appetite correction, not a new design.

Preserve:

- macro composition
- process/wok scene
- people / dining context
- identity rail
- semantic line system
- typography/layout positions
- background lighting system
- all non-food narrative structures

Correct the primary plated dish only, plus any immediately dependent local light/shadow interaction required to make the dish sit naturally in the existing scene.

Do not redraw the whole poster.

## Desired food target

The dish must read as:

- freshly cooked
- red-brown / sauce-red / amber-brown, not black-dominant
- moist and sauce-glossy, not hard-black glossy
- richly coated but with visible meat/ingredient texture
- selective browned/seared edges only
- dimensional tonal separation across pieces
- warm, appetizing, aromatic
- high-heat cooked, but not scorched

Priority order:

1. appetizing red-brown color separation
2. moist sauce gloss
3. believable meat/ingredient texture
4. selective seared edges
5. wok-heat cues
6. fire intensity

If heat/fire cues damage 1–4, reduce heat intensity instead of darkening the food.

## Hard avoids

Do not produce:

- whole-dish dark-brown/black dominance
- large-area carbonized surfaces
- burnt/scorched appearance
- black crust hiding texture
- crushed food shadows
- dry leathery meat
- soot-like color
- neon garnish
- global poster brightening that destroys the validated mood
- recoloring the whole poster just to fix the dish

## Execution method

Prefer a true image-edit / selective-edit workflow using the current artifact as the edit target and the verified real dish as grounding.

Do not reconstruct the poster from text memory.

If the available tool cannot reliably edit the current artifact while preserving non-food regions, FAIL CLOSED with:
`V3_A_SELECTIVE_EDIT_CAPABILITY_BLOCKED`

Do not fall back to whole-image regeneration.

## Formal output

Exactly 1 formal output:

`V3-A_FOOD_APPETITE_CORRECTED_R1.png`

No alternatives.
No best-of-N.
No hidden variants.
No aesthetic retries.

A deterministic transport/invalid-byte failure may be retried once with a receipt; an aesthetically unsatisfactory result may not be regenerated inside this task.

## Human validation package

Upload exact comparison set to a new Drive folder:

1. `V3-A_FAMILY_TRANSFER_REFINED_R1.png` — before
2. `V3-A_FOOD_APPETITE_CORRECTED_R1.png` — after
3. exact verified real main-dish source asset

Optionally include `R1C-APPROVED-05.jpg` only if it was actually used as a visual attachment.

Create:
`V3_A_FOOD_APPETITE_CORRECTION_R1_MANIFEST.json`

Record:

- before artifact SHA
- after artifact SHA
- dimensions
- real food source asset identity/SHA
- formal attachment count
- edited_region = primary plated dish
- whole_image_regenerated = false
- hidden_outputs = 0
- aesthetic_retries = 0
- production_layer_pilot_status = PAUSED_PENDING_FOOD_PASS

## Human pass gate

Codex must NOT self-declare visual success.

Human review must verify:

- dish no longer reads burnt/blackened;
- red-brown / sauce-red separation is visible;
- food remains realistic and appetizing;
- sauce gloss is moist rather than black-plastic;
- texture remains believable;
- family identity and macro composition are preserved;
- no meaningful regression outside the corrected dish region.

Only after human `FOOD_APPETITE_PASS` may the Production Layer Separation Pilot resume.

## Prohibited

Do NOT:

- modify global compiler
- modify Discovery
- run Library Scale Gate
- generate Route B
- redesign macro composition
- replace typography
- add new labels/icons
- make a new concept
- promote a new global aesthetic rule beyond the thin appetite gate already recorded

## Final response

Return only:

# V3 A FOOD APPETITE CORRECTION R1 READY FOR HUMAN VALIDATION

Branch:
HEAD:
Selected artifact SHA verified:
Real food source verified:
Formal outputs:
Hidden outputs:
Aesthetic retries:
Technical retries:
Output filename:
Output SHA-256:
Dimensions:
Drive folder:
Formal attachment count:
Whole image regenerated:
Global compiler changed:
Production Layer Pilot status:
Route B status:
Scale Gate executed:

## 已完成什么

## 未完成什么

## 需要人工验收什么

Then STOP.
