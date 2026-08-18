# V3-A R3A Figma Fallback Validation Result

Status: `TONAL_RESTRAINT_PARTIAL_PASS / FULL_R3A_NOT_YET`

Repository: `vubaoha034-hash/shenmei`
Branch: `visual-program-distillation-v2-photography-design-20260814`
Codex used: `NO`
ImageGen valid edit produced: `NO`
Figma deterministic fallback executed: `YES`
Commercial Quality Gate: `NOT YET`
Golden Exemplar: `NO`
Scale Gate: `BLOCKED`

## Why this fallback was executed

The current ImageGen path repeatedly failed to treat the Figma clean-base poster as the edit target and instead generated unrelated project-status/infographic images. Those outputs are invalid and are not formal R3A artifacts.

Adobe fallback was unavailable because the connected Adobe account could not be used in the current session. Figma / Weave fallback was also unavailable because the authenticated Figma account is not linked to Weave.

Therefore a deterministic, non-generative Figma raster-filter experiment was run to measure how much of R3A can be solved without a content-aware image editor.

## Frozen clean base

Figma clean-base frame:

`3:8` — `V3-A_R3A_CLEAN_BASE_MATERIALIZED__EDIT_THIS_ONLY`

Dimensions:

`1024x1536`

The clean base remains untouched.

Its raster fill supports native filters:

- exposure
- contrast
- saturation
- temperature
- tint
- highlights
- shadows

## D1 — Tonal restraint

Frame:

`4:2` — `V3-A_R3A_FALLBACK_D1_TONAL_RESTRAINT`

Filters:

- exposure: `0.01`
- contrast: `-0.08`
- saturation: `-0.05`
- temperature: `0`
- tint: `0`
- highlights: `-0.14`
- shadows: `0.07`

Human finding:

`VALID BUT TOO LIGHT`

D1 slightly reduces harsh highlight behavior and overall synthetic punch, but the effect is too subtle to materially change the dominant R3A defects.

## D2 — Stronger tonal restraint

Frame:

`5:2` — `V3-A_R3A_FALLBACK_D2_TONAL_RESTRAINT`

Filters:

- exposure: `0.015`
- contrast: `-0.12`
- saturation: `-0.08`
- temperature: `0`
- tint: `0`
- highlights: `-0.22`
- shadows: `0.10`

Human finding:

`BEST DETERMINISTIC TONAL FALLBACK / STILL NOT FULL R3A`

D2 is the better of the two fallback variants.

Improvements vs the clean base:

- slightly more mature commercial restraint;
- less aggressively glossy highlight behavior;
- lower synthetic local-contrast pressure;
- slightly less over-saturated sauce / fire response;
- shadow information remains usable rather than becoming crushed.

Remaining unchanged structural AI/composite cues:

- repetitive food-piece geometry;
- repetitive garnish / scallion behavior;
- excessive particle / droplet distribution;
- hyper-dramatized process-scene density;
- generated-looking local micro-detail;
- lack of natural material irregularity between food pieces.

## Core conclusion

Figma native raster filters can solve only the tonal-restraint subset of R3A.

They cannot solve the structural content defects that require content-aware image editing.

Therefore:

- D2 may be retained as the preferred tonal fallback reference;
- D2 must NOT be promoted to `R3A_PASS`;
- D2 must NOT be treated as a Commercial Quality artifact;
- R3B must not begin yet;
- Golden Exemplar and Scale Gate remain blocked.

## Renderer/tooling conclusion

Current valid content-aware edit routes tested:

1. Native ImageGen edit route: `ROUTING_FAIL` — generated unrelated infographic/status imagery instead of editing the target poster.
2. Adobe Firefly edit route: `UNAVAILABLE_CURRENT_ACCOUNT_CONNECTION`.
3. Figma / Weave route: `UNAVAILABLE_NOT_LINKED`.
4. Figma deterministic image filters: `AVAILABLE / PARTIAL_ONLY`.

This is a renderer/tool-availability blocker, not a Codex problem.

Do not invoke Codex to compensate for a missing content-aware image editor.

## Next valid action

Obtain one functioning image-to-image editor that can accept the exact clean-base raster as input while preserving composition.

Preferred recovery order:

1. restore/enable a true edit-capable image route in the current environment;
2. if available, connect Adobe and run one bounded `image_instruct_edit` pass;
3. or link Figma to Weave and use an image-edit workflow whose input contract explicitly accepts an existing image;
4. only after a valid content-aware R3A output exists, perform human visual validation against clean base and D2.

## 已完成什么

- clean base materialized in Figma;
- original production frame preserved;
- ImageGen routing failure reproduced and isolated;
- Adobe availability checked;
- Figma / Weave availability checked;
- Figma image-filter capability inspected;
- D1 and D2 deterministic tonal fallback variants created;
- D2 identified as the best deterministic tonal reference;
- Codex kept out of the task correctly.

## 未完成什么

- no valid content-aware R3A image edit exists yet;
- structural AI cues remain unresolved;
- R3A human PASS not reached;
- R3B not started;
- Commercial Quality Gate not passed;
- Golden Exemplar not promoted;
- Scale Gate not executed.
