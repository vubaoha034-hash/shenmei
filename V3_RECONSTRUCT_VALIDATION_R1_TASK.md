# V3 Distillation-First — Controlled Reconstruct Validation R1

Status: `AUTHORIZED_AFTER_HUMAN_TRANSFER_PLANNING_REVIEW`

Repository: `vubaoha034-hash/shenmei`
Branch: `v3-distillation-first-long-term-system-20260817`
Required starting HEAD containing human review: `65ce8917f4d7c207c4c4d416872bfde388a15e8c`

## 0. Purpose

Run the first actual visual validation of the two human-reviewed Provisional Visual Programs.

This task is NOT content-swap validation and NOT durable promotion.

The only authorized visual operators are:
- Reference 05 `RECONSTRUCT`;
- Reference 13 `RECONSTRUCT`.

Maximum formal visual outputs: `2` total, at most one per family.

## 1. Mandatory preflight

Before any image generation:

1. verify branch and starting HEAD ancestry;
2. read:
   - `V3_PROVISIONAL_PROGRAM_TRANSFER_PLANNING_HUMAN_REVIEW_RESULT.md`;
   - both Provisional Visual Programs;
   - the two reconstruction transfer plans;
   - current mechanism library;
   - semantic identity / renderer provenance contracts;
3. confirm neither family has been durable-promoted;
4. confirm Scale Gate is still disabled;
5. confirm official OpenAI imagegen Skill and built-in `image_gen` are available.

If built-in `image_gen` is unavailable, return:
`V3_RECONSTRUCT_BUILTIN_IMAGEGEN_UNAVAILABLE`
and STOP. Do not switch to CLI fallback.

## 2. Mandatory plan wording repair

Before invocation, repair ambiguous planning language where `original` could mean copied from the Mother Reference.

Execution semantics must say explicitly:
- `newly authored macro composition; do not copy Mother Reference geometry`;
- `new glyph forms authored for the current reconstruction; do not copy source glyph shapes`;
- `newly authored object constellation where variation is permitted; do not reproduce source inventory merely for resemblance`.

Persist the repaired transfer-plan wording before rendering.

## 3. Source readiness preflight

For each family independently, construct an exact execution package.

Every attachment must record:
- role;
- exact asset/sample ID where applicable;
- SHA-256;
- whether it is Mother Reference, semantic/content grounding, or execution target;
- semantic authority where required.

Do not use unresolved placeholders at invocation time.

### Reference 05 reconstruction

The canonical Mother Reference is required.

The reconstruction is allowed to use the Mother Reference as the semantic/reference baseline because this operator is explicitly establishing a `HIGH_REFERENCE_CONDITIONED` reconstruction baseline.

Do not attach Reference 13 or any Reference 13-derived material.
Do not attach prior V2/V3 generated outputs as Golden Exemplars.

If additional content grounding is used, it must be exact and role-bound.
Do not use the rejected `ast_63aa377b-5287-400d-b0a3-a6282313b38c` as hero product grounding.

### Reference 13 reconstruction

The canonical Mother Reference is required.

The reconstruction may use the Mother Reference as the semantic/reference baseline for this first `HIGH_REFERENCE_CONDITIONED` baseline.

Do not attach Reference 05 or any Reference 05-derived material.
Do not attach plated-food sources merely to satisfy an object slot.
Do not attach prior V2/V3 generated outputs as Golden Exemplars.

If the renderer cannot construct a valid reconstruction package without literal source-object copying, mark this route:
`RECONSTRUCT_SOURCE_PACKAGE_INADEQUATE`
and do not generate it.

## 4. Runtime package rules

For each route, compile a small renderer package from only that family's program.

Runtime package must include:
- one canonical Mother Reference;
- no Golden Exemplar in R1;
- concise visual philosophy;
- the reviewed active stable grammar;
- max 3 shortcut blockers;
- required copy/semantic constraints for the reconstruction;
- explicit freedoms;
- explicit instruction that exact source layout/glyph/object assets are not to be copied.

Do NOT dump deep evidence into the image prompt.
Do NOT mention the other family in a family's prompt.

## 5. Renderer hard lock

Use official OpenAI imagegen Skill.
Use built-in `image_gen`.

For each family:
- exactly one formal imagegen call if preflight passes;
- no hidden variants;
- no best-of-N;
- no aesthetic retry;
- a technical retry is allowed only when no valid image bytes are returned.

Record:
- `imagegen_skill_used`;
- `renderer_mode = BUILT_IN_IMAGE_GEN`;
- `cli_fallback_used = NO`;
- imagegen call count;
- actual attachments with hashes;
- final invocation evidence;
- output SHA-256 and dimensions.

## 6. Visual intent — Reference 05

Test whether the reviewed program produces a newly authored member of the same family while preserving:
- process/action narrative credibility;
- multiple information roles;
- semantic sequencing rather than equal cards;
- world/context depth;
- semantic graphics derived from real brand/process evidence;
- low-key heat / tonal orchestration with retained detail;
- expressive display lettering as structural mass;
- integrated first/second/third read.

Hard avoid:
- exact three-band reproduction;
- exact card count/geometry;
- exact source glyphs or marks;
- generic black/red + brush title + food plate collapse.

## 7. Visual intent — Reference 13

Test whether the reviewed program produces a newly authored member of the same family while preserving:
- asymmetric expressive title field;
- active whitespace;
- quiet tactile object/raw-material anchor;
- editorial information rhythm;
- cross-element optical geometry;
- organic handmade display-lettering behavior;
- matte-mineral, muted, soft-light materiality.

Hard avoid:
- exact vessel/ingredient inventory;
- exact source glyphs;
- exact four-label rhythm;
- beige background + giant brush title + centered dish collapse;
- glossy promotional rendering.

## 8. Output filenames

If Reference 05 passes preflight:
`V3-R05_RECONSTRUCT_VALIDATION_R1.png`

If Reference 13 passes preflight:
`V3-R13_RECONSTRUCT_VALIDATION_R1.png`

Do not create additional formal visual variants.

## 9. Human validation package

Create one Drive folder containing for each executed route:
- canonical Mother Reference;
- reconstruction output;
- renderer/runtime receipt.

The human reviewer must see the actual pixels.

Do not self-score aesthetic success.
Do not mark transfer validated.
Do not modify mechanism promotion status.

## 10. Stop conditions

This task must NOT execute:
- CONTENT_SWAP;
- COMPOSITION_OR_ASPECT_TRANSFER;
- durable promotion;
- Library Scale Gate;
- Discovery expansion;
- bulk import;
- production typography retrofit;
- global compiler changes unrelated to execution correctness.

## Final response

Return only:

# V3 RECONSTRUCT VALIDATION R1 READY FOR HUMAN PIXEL REVIEW

Branch:
HEAD:
Starting HEAD verified:
Transfer-plan wording repaired:
Reference 05 preflight:
Reference 13 preflight:
Reference 05 output:
Reference 13 output:
Imagegen skill used:
Renderer mode:
CLI fallback used:
Total formal outputs:
Hidden variants:
Technical retries:
Drive folder:
Reference 05 attachment receipt:
Reference 13 attachment receipt:
Transfer validated: NO
Content Swap executed: NO
Composition/Aspect Transfer executed: NO
Scale Gate executed: NO
Durable promotion executed: NO
Git working tree:

## 已完成什么

## 未完成什么

## 需要人工验收什么

Then STOP.