# G3R — PRODUCTION PIPELINE REDESIGN

Status: `ACTIVE_AFTER_G3_VALUE_FLOOR_FAILURE`
Date: `2026-08-14`
Base: G3 absolute-quality failure (`0/9 USABLE`)

## 0. Why G3R exists

G3 proved that the current one-pass generation approach is not production-capable for the user's restaurant-design standard:

- all 9 outputs were judged `UNUSABLE`;
- food imagery remained obviously synthetic;
- packaging graphics remained generic;
- corrected multimodal binding and prompt-invariant preservation were not sufficient.

The next step is therefore NOT more blind testing and NOT more prompt rules.

The pipeline itself must be split by professional responsibility.

---

## 1. Core correction

Do not ask one image-generation call to simultaneously perform:

1. believable food photography;
2. brand art direction;
3. graphic layout / typography;
4. packaging production design.

These are separate production tasks and must use different tools/stages.

---

## 2. New production architecture

### Track A — Food / Product Realism

Preferred source hierarchy:

1. real user/restaurant photograph;
2. real photograph edited/enhanced with AI;
3. synthetic food generation only as a fallback experiment.

Rule:

> When realism is commercially important, preserve a real food source whenever possible.

Image generation may be used for:
- background replacement;
- environment extension;
- controlled lighting reinterpretation;
- steam/smoke enhancement;
- crop/negative-space creation;
- supporting ingredients/background props.

It must not casually replace a believable real dish with invented geometry/material.

### Track B — Brand Key Visual

Use a staged system:

1. real/approved food or product asset;
2. one visual concept / art-direction mechanism;
3. layout in a real design environment;
4. real typography/vector graphics;
5. final pixel review.

Image generation is an asset creator, not the final layout authority.

### Track C — Packaging / Graphic System

Use vector/layout-first production:

- Figma / equivalent real layout tool;
- real type;
- real grids/proportions;
- actual print area and dieline assumptions stated explicitly;
- image generation limited to illustration/material/motif exploration where justified.

Do not treat a rendered paper-bag mockup with generic geometry as a finished packaging-design proof.

---

## 3. Permanent role boundary for image generation

Allowed roles:

- image assets;
- photo edits;
- backgrounds;
- material studies;
- illustration/motif studies;
- visual-concept exploration.

Not sufficient by itself for final PASS:

- restaurant brand system;
- packaging graphic system;
- final typography;
- production layout;
- food realism when the generated food is visibly synthetic.

---

## 4. Next minimal proof — only 3 deliverables

Do NOT generate another 9/20-image batch.

Use exactly one representative deliverable per track:

### R1 — Real-food-first hero

Input prerequisite:
- one real restaurant dish photo that the user considers a legitimate source asset.

Process:
- preserve dish structure/material;
- use AI only for controlled enhancement/background/art direction;
- final review through Google Drive.

PASS criterion:
- user marks `USABLE`;
- independent pixel review finds no obvious synthetic-food failure.

### R2 — Brand KV composition

Input:
- the R1 food asset or another approved real asset.

Process:
- one art-direction concept;
- real layout/vector/typography environment;
- image generation only for supporting image assets if needed.

PASS criterion:
- user marks `USABLE` without requiring a new concept from scratch.

### R3 — Packaging graphic

Input:
- same brand concept;
- blank bag/packaging structure or production-realistic mockup.

Process:
- vector-first graphic system;
- real layout;
- no generic AI-generated pseudo-brand geometry accepted by default.

PASS criterion:
- user marks `USABLE` as a credible starting production design.

---

## 5. Kill gate

If R1 fails even when the dish itself is a real photograph preserved through the process:

- diagnose edit/art-direction chain;
- do not continue R2/R3.

If R1 passes but R2/R3 fail:

- food renderer is not the main problem;
- fix design/layout process rather than image realism.

If R1/R2/R3 all pass:

- only then return to a small G4 absolute-quality confirmation set.

---

## 6. What remains frozen

Until R1–R3 establish production capability:

- Discovery = 18 approved / 12 rejected;
- no evidence expansion;
- no embeddings/vector DB;
- no PHASE 10 restart;
- no large blind benchmark;
- no new aesthetic rule warehouse;
- no automated taste learning from failed G3 outputs.

G3 outputs remain evaluation-only and do not enter preference memory.

---

## 7. Current diagnosis

### Proven facts

- G2 technical bridge works.
- G3 absolute quality = 0/9 usable.
- food realism failed at user-visible level.
- packaging visual quality failed at user-visible level.

### Strong inference

The current one-pass image-generation workflow is the wrong production abstraction for the target quality level.

### Not yet proven

- whether a real-photo-first food pipeline meets the user's quality floor;
- whether vector/layout-first brand and packaging work meets the user's quality floor;
- whether the current image model is useful as a supporting asset generator once removed from final-layout responsibility.

---

## 8. Next required user input

Before R1, obtain exactly one real dish photograph suitable for a production-quality test.

Do not request a large batch.
