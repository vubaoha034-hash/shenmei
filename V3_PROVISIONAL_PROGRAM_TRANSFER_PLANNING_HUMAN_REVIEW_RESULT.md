# V3 Provisional Programs — Human Transfer-Planning Review

Status: `PROGRAMS_APPROVED_FOR_CONTROLLED_TRANSFER_VALIDATION / PLAN_FIXES_REQUIRED_BEFORE_EXECUTION`

Reviewed HEAD: `320eb2924a4bc10aca678aebcf99b44f5dda701d`

Reviewed artifacts:
- `V3_VISUAL_PROGRAM_REFERENCE_05_PROVISIONAL.json`
- `V3_VISUAL_PROGRAM_REFERENCE_13_PROVISIONAL.json`
- the three planned transfer operators for each program at HEAD `320eb292...`
- `V3_VISUAL_MECHANISM_LIBRARY.json`
- canonical Reference 05 / 13 pixels and prior human distillation reviews.

## 1. Overall decision

Both provisional programs are now materially aligned with the human distillation reviews and may proceed to **controlled transfer validation**.

This is NOT durable approval. All stable-grammar items remain hypotheses until transfer outputs pass human pixel review.

Reference 05: `PASS_FOR_CONTROLLED_TRANSFER_VALIDATION`
Reference 13: `PASS_FOR_CONTROLLED_TRANSFER_VALIDATION`

The mechanism library correctly remains `UNCONFIRMED / UNPROMOTED` at component level.

## 2. Reference 05 program review

Accepted as provisional:
- process/action narrative engine;
- multi-tier information roles;
- semantic campaign sequencing instead of fixed cards;
- semantic graphic derivation principle while exact marks remain brand-bound;
- broader world/context layer;
- low-key heat / tonal-color orchestration;
- display lettering as structural mass;
- semantic-role compatibility instead of literal asset-category locking;
- structural family naming and preserved alias/history;
- `HIGH_REFERENCE_CONDITIONED` anchor dependence.

Important unresolved proof questions:
1. Can the family survive a materially different macro composition?
2. Does the family survive changed content without collapsing to black/red + brush title?
3. Can product/process legibility remain high under low-key heat treatment?
4. How much of success is still caused by direct Mother Reference pixels?

## 3. Reference 13 program review

Accepted as provisional:
- asymmetric expressive title field;
- active whitespace;
- low tactile object/raw-material still-life anchor;
- editorial information rhythm;
- cross-element optical geometry;
- organic display-lettering behavior;
- matte-mineral / muted / soft-light materiality;
- exact objects remain content-bound;
- exact paper grain remains production-bound;
- literal vessel is no longer required;
- finished product remains high-risk rather than universally forbidden;
- structural family naming and preserved alias/history;
- `HIGH_REFERENCE_CONDITIONED` anchor dependence.

Important unresolved proof questions:
1. Can the family survive new objects/materials without becoming beige minimalism?
2. Can title lettering remain authored instead of generic brush calligraphy?
3. Can active whitespace remain structural rather than empty?
4. Can the still-life mechanism survive beyond the original vessel/ingredient constellation?

## 4. Mandatory transfer-plan fixes before any image call

### FIX A — remove ambiguous `original` wording

Some `allowed_variation` entries use wording such as:
- `original macro composition`
- `original glyph forms`
- `original object constellation`

At execution time this may be read as permission to reuse/copy the Mother Reference.

Replace with explicit semantics such as:
- `newly authored macro composition that is not copied from the Mother Reference`;
- `new glyph forms authored for the current content; never copy source glyph shapes`;
- `new object constellation grounded in the current content; never reuse source object inventory merely for resemblance`.

### FIX B — no vague content placeholders at execution

Before an image call, every route must bind exact asset identities and semantic roles.

Execution may NOT use unresolved placeholders such as:
- `ONLY_VERIFIED_CURRENT_CONTENT`
- `DIRECT_CANONICAL_ATTACHMENTS`
- `SAME_AS_APPROVED_RECONSTRUCT_OR_DECLARED_NEW_SET`

Those are acceptable planning placeholders only.

Each actual transfer execution must record:
- exact asset ID;
- SHA-256;
- semantic role;
- content authority/identity;
- suitability for that role.

If the required role package cannot be assembled, fail closed for that route.

## 5. Route readiness decisions

### Reference 05 — RECONSTRUCT
`CONDITIONALLY_APPROVED`

May execute after exact content-role package is bound and renderer invocation is frozen.

### Reference 05 — CONTENT_SWAP
`SOURCE_PACKAGE_REQUIRED`

Do not use `ast_63aa377b-5287-400d-b0a3-a6282313b38c` as the hero product source because its current recorded hero suitability is `FAIL_FOR_HERO_SOURCE`.

The route requires a genuinely different, semantically grounded package covering the reviewed roles:
- process/action or equivalent live-making evidence;
- product/proof/detail evidence;
- credible world/context evidence.

### Reference 05 — COMPOSITION_OR_ASPECT_TRANSFER
`WAIT_FOR_RECONSTRUCT_HUMAN_PASS`

Do not spend a composition-transfer call until the reconstruction establishes that the program can at least produce an absolutely usable family result.

### Reference 13 — RECONSTRUCT
`CONDITIONALLY_APPROVED`

May execute only if a semantically grounded tactile object/raw-material content package and meaningful copy hierarchy can be bound without copying the original vessel/object inventory.

### Reference 13 — CONTENT_SWAP
`CURRENTLY_BLOCKED_UNLESS_NEW_COMPATIBLE_SOURCE_IS_FOUND`

Prior Route B work already demonstrated a source mismatch when only plated/served-food content was available. A plan existing on paper does not resolve that mismatch.

Suitable new content should support a quiet tactile object/raw-material anchor. If no such source exists in the private vault, fail closed rather than inventing one for validation.

### Reference 13 — COMPOSITION_OR_ASPECT_TRANSFER
`WAIT_FOR_RECONSTRUCT_HUMAN_PASS`

Same sequencing rule as Reference 05.

## 6. Controlled validation sequence

Do NOT execute all six planned transfers at once.

Correct sequence:

1. `SOURCE_READINESS_PREFLIGHT`
   - resolve exact current assets for both reconstruction routes;
   - fix ambiguous plan wording;
   - compile bounded runtime packages;
   - no image generation if a route lacks adequate sources.

2. `RECONSTRUCT_VALIDATION_R1`
   - maximum one formal output per family whose source preflight passes;
   - official OpenAI imagegen Skill;
   - built-in `image_gen`;
   - no hidden variants / no best-of-N;
   - technical retry only if no valid image bytes are returned;
   - record full renderer provenance.

3. `HUMAN_PIXEL_REVIEW`
   - show actual outputs to the user;
   - judge absolute quality, family mechanism survival, template collapse, product/content legibility, typography and anchor dependence.

4. Only a family with a human reconstruction PASS may proceed to `COMPOSITION_OR_ASPECT_TRANSFER`.

5. `CONTENT_SWAP` executes only after an exact compatible new-source package is bound.

This ordering avoids spending calls on a program that cannot clear the first absolute-quality gate.

## 7. Human review status

No component mechanism is promoted by this review.
No family is durable-promoted.
No Scale Gate is authorized.
No Discovery expansion is authorized.

Next authorized action:
`SOURCE_READINESS_PREFLIGHT + CONDITIONAL RECONSTRUCT VALIDATION ONLY`.