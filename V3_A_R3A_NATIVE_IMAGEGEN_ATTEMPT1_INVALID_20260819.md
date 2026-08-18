# V3-A R3A — Native ImageGen Attempt 1 — INVALID

Status: `TECHNICAL_INVALID / WHOLE_IMAGE_REGENERATION / WRONG_GEOMETRY`

Repository: `vubaoha034-hash/shenmei`
Branch: `vpd-v3-cinema-dna-integration-audit-20260818`
Date: `2026-08-19`
Codex used: `NO`
Image generation executed: `YES`
Formal outputs accepted: `0`
Hidden variants: `0`
Aesthetic retries: `0`
Technical retries: `0`

## Intended input

Figma clean-base source:

- file key: `XZPhanfxH1JWUPsOoxt0zp`
- node: `3:8`
- displayed/rendered dimensions: `1024x1536`
- target role: selective R3A art-realism edit only

The source image was successfully surfaced inline from Figma immediately before the image-generation call.

## Intended edit contract

Use the bounded patch in:

`V3_A_R3A_CINEMA_DNA_BOUNDED_PATCH_V1.md`

Frozen preservation requirements included:

- preserve macro composition;
- preserve left black identity rail;
- preserve raster `现烧` identity;
- preserve chef/person/hand placement;
- preserve wok, utensils and plate placement;
- preserve camera viewpoint/perspective and light direction;
- change only food/process realism defects;
- exactly one candidate;
- no whole-image redesign.

## Actual output

Local generated file:

`a_dramatic_food_photography_scene_in_a_dark_moody.png`

Generated output SHA-256:

`70150645f37143f897af0eeb9c07f91788a76dbf932359569cbccd7f09e2b109`

Generated dimensions:

`1536x1024`

Generation id:

`6a031685-7604-4b75-9fa2-7d85304aa400`

## Invalidation reasons

The output is formally invalid before aesthetic scoring because it violates hard frozen identity and geometry constraints:

1. source aspect/orientation was `1024x1536`, but output became `1536x1024`;
2. the macro composition was replaced by a new scene rather than selectively edited;
3. left identity rail geometry was changed materially;
4. the raster `现烧` identity was redrawn/changed rather than preserved;
5. person/hand/wok/plate positions and scene structure were replaced;
6. the output therefore cannot be treated as an R3A candidate, regardless of local food realism quality.

This is classified as a renderer/source-binding/edit-operation failure, not an aesthetic failure of the six-control patch.

## Consequence

Do not run an aesthetic retry from this invalid output.
Do not promote any recipe from this attempt.
Do not modify the six-control patch based on pixels from this invalid whole-image regeneration.

The next admissible action must use an image-edit runtime that demonstrably preserves the exact input image structure, or a narrowly scoped engineering bridge that can guarantee:

`exact input bytes -> edit operation -> exact output file -> dimension/hash verification`.

## Gates

- R3A Art Realism: `NOT YET`
- R3B Brand Authorship: `NOT STARTED`
- Commercial Quality Gate: `NOT YET`
- Golden Exemplar: `NO`
- Scale Gate: `BLOCKED`

## 已完成什么

- exact clean-base frame was surfaced as an inline visual target;
- one native ImageGen attempt was executed under the bounded-patch intent;
- output file hash and dimensions were computed;
- the result was rejected as technically invalid instead of being miscounted as progress;
- invalidation cause was narrowed to whole-image regeneration / source-binding failure.

## 未完成什么

- no valid selective R3A edited candidate exists;
- no aesthetic R3A comparison has been performed;
- no human R3A PASS exists;
- no production compiler change has been authorized;
- R3B, Commercial Quality, Golden and Scale remain blocked.
