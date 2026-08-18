# V3-A R3A External Render Handoff Task

Status: `ACTIVE_RENDER_HANDOFF`

Repository: `vubaoha034-hash/shenmei`
Branch: `visual-program-distillation-v2-photography-design-20260814`
Anchor HEAD before handoff: `28bf804a9c64d1d2f06fdcc8cf05de166833398c`

## Why this task exists

The current long-running ChatGPT project context repeatedly failed to bind the clean-base image as an image-edit source. The image model produced unrelated project-status infographics instead of editing the poster. Those generations are INVALID and must never be treated as R3A outputs.

This handoff allows the visual edit to occur in a minimal, isolated render context while preserving complete engineering continuity through repository settlement.

This does NOT return ownership of the whole project to Codex.

## Current frozen project state

- Family Transfer: `PASS`
- Production Layer Pilot R2: `PASS`
- R3A Art Realism Hardening: `NOT YET`
- R3B Brand Authorship: `NOT STARTED`
- Commercial Quality Gate: `NOT YET`
- Golden Exemplar: `NO`
- Route B: `SOURCE_MISMATCH_FOR_ROUTE_B`
- Scale Gate: `BLOCKED`

## Render input

External render filename:

`V3-A_R3A_CLEAN_BASE_LOCAL.png`

Dimensions:

`1024x1536`

File-level SHA-256 of the locally materialized handoff PNG:

`15ecb2901de7588771905663a8eedbe48979819b87b952cb418f075f97a54612`

Provenance:

- materialized from Figma clean-base frame `3:8`
- Figma file key: `XZPhanfxH1JWUPsOoxt0zp`
- frame name: `V3-A_R3A_CLEAN_BASE_MATERIALIZED__EDIT_THIS_ONLY`
- created by cloning validated R2 frame and removing only the five live functional-text nodes
- original production frame `1:2` remains untouched

Important identity note:

The R2 manifest previously recorded a clean-base PNG SHA-256 of:

`f0d67df33bf1d185c73c7770a3e3a9adb20e9a76fd956e3093483148c979f36a`

The externally materialized handoff PNG currently has a different file-level SHA because it was re-exported/materialized. Do NOT claim byte identity between these two PNG files unless a later pixel-level comparison proves equivalent decoded pixels. Treat the external handoff SHA above as the exact input identity for the isolated render experiment.

## R3A render instruction

Edit ONLY the supplied image. Do not create a new poster concept and do not produce an infographic, workflow diagram, dashboard, or project-status image.

Preserve exactly:

- macro composition
- left black identity rail
- raster display identity `现烧`
- people and hand positions
- wok / utensils
- plate position, size, perspective, and table relationship
- overall camera viewpoint and perspective
- lighting direction
- general dark / warm restaurant atmosphere
- visual curve / spatial rhythm

Change ONLY the food-and-process realism defects:

1. reduce repetitive food-piece geometry;
2. reduce plastic / uniformly glossy highlights;
3. create believable variation in piece size, edge shape, sauce thickness, moisture, oil-film reflection, sear and焦边;
4. reduce repetitive scallion / garnish placement;
5. reduce excessive suspended particles, droplets and debris;
6. reduce over-cinematic smoke/fire density while retaining wok energy;
7. preserve appetite and red-brown / sauce-red / amber separation;
8. avoid over-sharpening, over-contrast and synthetic orange saturation;
9. make the result read as real high-end restaurant commercial photography rather than an AI advertising render.

Do not add text. Do not remove or redraw `现烧`.

## Output contract

Generate exactly ONE formal candidate.

Preferred filename:

`V3-A_R3A_ART_REALISM_CANDIDATE_01.png`

No hidden variants.
No aesthetic retry inside the isolated render context.

The isolated render context has NO authority to declare:

- R3A PASS
- Commercial Quality PASS
- Golden Exemplar
- Scale readiness

It only creates the candidate.

## Return-to-main-project settlement

After the candidate is generated, return it to the main project context.

The main project controller must then:

1. verify dimensions / MIME / output identity;
2. compute SHA-256 of the returned candidate;
3. compare actual pixels against the exact external render input;
4. check all frozen structures for regression;
5. evaluate food realism, appetite, particle restraint and photographic coherence;
6. record `R3A_PASS` or `R3A_FAIL` in a human-validation result;
7. if PASS, create a formal manifest tying exact input SHA to exact output SHA;
8. commit the validation / manifest to this same branch;
9. only then create / activate R3B;
10. keep Commercial Quality / Golden / Scale gates blocked until their own evidence exists.

This repository settlement is what preserves continuity for future Codex contexts.

## Codex policy

`CODEX_REQUIRED_NOW = NO`

The isolated image render is not a software-engineering task.

Codex becomes admissible only if the direct isolated image-edit route still cannot accept the exact PNG and an engineering bridge must be implemented to move:

`exact input file -> image editing API/runtime -> exact output file -> hash/dimension verification`.

If that happens, Codex scope must be limited to that bridge and technical verification. It must not own aesthetic judgment, R3B, Commercial Quality promotion, Golden promotion or Scale Gate.

## 已完成什么

- current R3A failure mode isolated as image-edit binding/context contamination rather than project-design failure;
- exact external render PNG materialized;
- exact local file SHA-256 recorded;
- provenance to Figma frame `3:8` recorded;
- isolated render instruction frozen;
- repository settlement contract frozen;
- Codex admission boundary frozen.

## 未完成什么

- no valid content-aware R3A candidate exists yet;
- R3A human validation not yet executed;
- R3B not started;
- Commercial Quality Gate not passed;
- Golden Exemplar not promoted;
- Scale Gate not executed.
