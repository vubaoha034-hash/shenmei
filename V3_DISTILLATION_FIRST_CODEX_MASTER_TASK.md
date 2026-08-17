# V3 Distillation-First Long-Term System — Codex Master Task

Status: `EXECUTE_SYSTEM_BUILD_AND_INITIAL_DISTILLATION / STOP_BEFORE_VISUAL_TRANSFER`

Repository: `vubaoha034-hash/shenmei`

Required branch: `v3-distillation-first-long-term-system-20260817`

## 0. Primary objective

Build the durable distillation system whose central job is:

> turn user-approved high-quality visual works into reusable Visual Programs that can be used long-term across future content without literal copying.

This task is NOT a production-first migration and is NOT a request to generate a new poster.

No new image generation is allowed in this master task.

## 1. Mandatory reads

Read first:

1. `START_HERE.md`
2. `AESTHETIC_SKILL_DESIGN_CHARTER.md`
3. `VPD_V3_TOP_SKILL_REFERENCE_AUDIT.md`
4. `V3_DISTILLATION_FIRST_SYSTEM_CHARTER.md`
5. current VPD V2 schema / compiler / evidence / scaling files only as needed for migration
6. current `skill-refiner` durable-promotion contract

Historical V2/V3 experiment evidence may be used to avoid repeating proven failures, but must not be treated as user-approved style evidence unless explicitly approved.

## 2. Preserve / supersede policy

Do not delete:
- raw references;
- user feedback;
- VPD V1/V2 experiment records;
- blind-review incidents;
- invalidation records;
- benchmark outputs;
- lineage / provenance.

Classify existing components as:
- `KEEP_AS_EVIDENCE`
- `MIGRATE_TO_V3`
- `KEEP_EXPERIMENT_ONLY`
- `SUPERSEDED_RUNTIME`

Create:
`V3_LEGACY_COMPONENT_CLASSIFICATION.md`

## 3. V3 state model

Implement a durable state machine:

- `RAW_REFERENCE`
- `DISTILLATION_CANDIDATE`
- `PROVISIONAL_VISUAL_PROGRAM`
- `TRANSFER_VALIDATION_PENDING`
- `TRANSFER_VALIDATED`
- `HUMAN_APPROVED`
- `DURABLE_PROMOTED`
- `RETIRED_OR_SPLIT`

No single-reference family may jump directly from raw reference to durable promoted.

## 4. Deep distillation evidence schema

Create a V3 deep evidence schema that preserves professional analysis but clearly separates evidence from runtime controls.

Required evidence domains:

### Photography
- capture geometry;
- focus / optics;
- lighting;
- exposure / tonality;
- color science / grade;
- texture / sharpness / microcontrast;
- subject styling / scene;
- post-processing / retouch.

### Graphic design
- semantic / communication intent;
- reading hierarchy;
- grid / geometry;
- typography / lettering;
- copy meaning / tone;
- whitespace / density;
- color roles;
- graphic language;
- layering / crop / edge;
- material / print;
- sequence / system behavior.

### Integration
- photo/type dominance;
- shared color logic;
- image-provided type space;
- overlap / avoidance;
- crop/copy co-dependence;
- lighting/hierarchy interaction;
- semantic motif binding;
- realism protection;
- thumbnail and second-read behavior.

Every high-value observation must support:
- evidence class: `DIRECT_VISIBLE | METADATA | INFERENCE`;
- confidence;
- source region / evidence pointer;
- uncertainty note;
- optional measured evidence;
- `STYLE_SIGNATURE | CONTENT_BOUND | BRAND_BOUND | PRODUCTION_BOUND | OPTIONAL_VARIATION` classification.

Create:
- `schemas/distillation-evidence.v3.schema.json`
- validator/tests.

## 5. Visual Program V3 schema

Create:
`schemas/visual-program.v3.schema.json`

Required durable fields:

- program_id
- family_id
- status
- visual_philosophy
- mother_reference
- golden_exemplars
- stable_grammar
- variation_axes
- content_compatibility
- content_bound_features
- brand_bound_features
- typography_role
- color_light_material_signature
- integration_rules
- generic_shortcut_blockers (max 3)
- freedoms
- transfer_operators
- validation_evidence
- renderer_provenance_requirements
- promotion_history
- evidence_lineage

Constraints:
- stable_grammar target 4–8 items;
- generic_shortcut_blockers max 3;
- program must not embed the entire deep evidence object;
- program must retain pointers back to deep evidence and raw pixels;
- program must explicitly distinguish invariant hypotheses from validated invariants.

## 6. Distillation compiler V3

Implement a deterministic compiler layer:

`DEEP_EVIDENCE -> PROVISIONAL_VISUAL_PROGRAM`

It must prioritize:
1. discriminative mechanisms;
2. causal importance;
3. cross-content reusability;
4. evidence confidence;
5. avoiding common-mode generic restaurant-poster priors.

It must down-rank:
- visually salient but generic features;
- content-specific objects mistaken for style;
- brand-specific marks without transfer rights;
- weak-confidence inferences;
- redundant controls.

It must emit an audit explaining why each stable-grammar item was selected.

Create tests proving the compiler stays bounded as deep evidence grows.

## 7. Family registry

Create a durable family registry that prevents averaging conflicting liked styles.

Each family record must track:
- family_id
- canonical mother reference
- provisional / validated exemplars
- approved domains / content archetypes
- contradictions
- near-duplicate reinforcement count
- split history
- merge prohibition unless human-approved
- current Visual Program version

Create:
- `schemas/visual-family.v3.schema.json`
- registry seed file
- validator/tests.

## 8. Evidence action on new liked work

Implement one primary action per newly liked work:

- `DUPLICATE_OR_NEAR_DUPLICATE`
- `REINFORCE_EXISTING_FAMILY`
- `REFINE_EXISTING_FAMILY`
- `NEW_FAMILY_CANDIDATE`
- `CONTRADICTION_EVIDENCE`

Do not automatically convert every liked image into new global rules.

## 9. Transfer operators

Define reusable transfer operators:

- `RECONSTRUCT`
- `CONTENT_SWAP`
- `COMPOSITION_OR_ASPECT_TRANSFER`
- optional `SCENE_ARCHETYPE_TRANSFER`
- optional `BRAND_CONTEXT_TRANSFER`
- optional `TYPOGRAPHY_ROLE_TRANSFER`
- optional `MATERIAL_OR_MEDIUM_TRANSFER`

Each operator must declare:
- preconditions;
- which stable grammar must survive;
- which fields may vary;
- content compatibility requirements;
- semantic identity requirements;
- failure conditions.

Create a transfer-plan schema and tests.

## 10. Validation harness

Create a harness for future visual validation.

It must separate:

### Technical correctness
- file integrity;
- text correctness;
- catastrophic artifacts;
- semantic substitutions;
- renderer provenance.

### Absolute aesthetic quality
Human-only final judgment of:
- photography / art direction;
- graphic-design authorship;
- typography / lettering;
- photo-design integration;
- semantic hierarchy;
- reference-family structural fidelity;
- generic-template collapse;
- reference distance;
- appetite / product legibility when relevant;
- `USABLE / UNUSABLE`;
- `TOP_TIER`.

Codex may package evidence but cannot self-promote an aesthetic PASS.

## 11. Semantic asset registry

Implement a semantic asset registry for content correctness.

For restaurant hero assets, support:
- canonical dish name;
- aliases;
- primary ingredient / protein;
- cooking method;
- required visible identity cues;
- forbidden substitutions;
- hero suitability;
- evidence source / user authority;
- confidence.

Seed current authoritative user data:

Asset:
`ast_63aa377b-5287-400d-b0a3-a6282313b38c`

Canonical dish name:
`柠檬叶怪味里脊`

Alias:
`柠檬怪味里脊`

Primary ingredient:
`猪里脊肉`

Cooking process:
- cut pork tenderloin into strips;
- fry to set shape;
- raise oil temperature and refry about 30 seconds for crisp shell;
- sauté garlic and chili fragments;
- simmer the strange-flavor sauce until thick and sticky;
- rapidly toss the fried tenderloin over high heat until every strip is evenly coated in the dark sauce.

Required visible identity cues:
- pork tenderloin strip geometry;
- crisp-fried exterior evidence;
- individual strips remain distinguishable;
- dark strange-flavor sauce coats the strips rather than obscuring shape;
- not a shapeless black meat pile.

Forbidden substitutions:
- beef;
- chicken;
- ribs / bone-in meat;
- irregular chunks that erase strip identity.

Current source hero suitability:
`FAIL`

Reason:
User judged this specific source visually unappealing / unsuitable as hero material. Preserve it as real evidence; do not interpret this as rejection of the real dish itself.

## 12. Renderer provenance

For every future visual validation call record:
- imagegen skill used;
- renderer mode;
- built-in vs fallback;
- number of generation/edit calls;
- model/tool version when available;
- attachment identities and roles;
- output SHA/dimensions.

Normal raster validation should default to official OpenAI imagegen Skill / built-in `image_gen`.

## 13. Runtime compiler for long-term reuse

Create a separate bounded runtime compiler:

`VALIDATED_VISUAL_PROGRAM + CURRENT_CONTENT -> SMALL_RENDERER_PACKAGE`

The package should contain only what the renderer needs now, typically:
- one mother reference when useful;
- 0–1 golden exemplar by default;
- primary content asset(s);
- concise visual philosophy;
- 4–7 active structural controls;
- max 3 shortcut blockers;
- content semantic contract;
- exact copy/brand constraints;
- explicit freedoms.

This runtime compiler is a consumer of the durable distillation system.
It must not replace the deep distillation layer.

## 14. Promotion path

Create a promotion package that can be consumed by `skill-refiner`.

Promotion requires:
- validated transfer evidence;
- human pixel review;
- explicit user approval for durable preference/style promotion;
- no unresolved contradiction;
- provenance complete.

No automatic promotion from Codex aesthetic scores.

## 15. Initial long-term distillation: Reference 05 and Reference 13

Use the canonical approved source images already established in the project:
- `R1C-APPROVED-05.jpg`
- `R1C-APPROVED-13.jpg`

Do NOT generate images in this task.

For each reference:
1. verify exact canonical identity;
2. create a deep V3 evidence object;
3. create a provisional Visual Program V3;
4. explicitly separate style-signature vs content-bound vs brand-bound;
5. define content compatibility hypotheses;
6. define 3 future transfer tests: reconstruct, content swap, composition/aspect transfer;
7. create a human-review sheet summarizing what the program believes is essential;
8. mark status `PROVISIONAL_VISUAL_PROGRAM / HUMAN_DISTILLATION_REVIEW_PENDING`.

Do not average 05 and 13.
They are separate families.

## 16. Human distillation review package

Create:
- `V3_REFERENCE_05_DISTILLATION_REVIEW.md`
- `V3_REFERENCE_13_DISTILLATION_REVIEW.md`

Each must show:
- concise visual philosophy;
- stable grammar hypotheses;
- variation axes;
- content-bound exclusions;
- brand-bound exclusions;
- typography role;
- color/light/material signature;
- integration rules;
- transfer hypotheses;
- evidence pointers;
- unresolved uncertainty.

The human reviewer must be able to answer:

> Did the system actually learn why this work is good, or merely summarize visible surface traits?

## 17. Automated tests

Add tests for:
- schema validity;
- bounded stable grammar;
- max shortcut blockers;
- no deep-evidence dump into runtime package;
- family separation;
- state transitions;
- evidence lineage;
- renderer provenance completeness;
- semantic identity requirements;
- transfer preconditions;
- promotion cannot occur without human/user approval.

Run all relevant existing tests and new V3 tests.

## 18. Documentation convergence

Update only the minimum routing/docs needed to expose Distillation-First V3 as the active experimental long-term direction.

Do not delete or rewrite stable production Skills.
Do not make the new V3 program canonical until human distillation review and visual transfer validation pass.

## 19. Hard prohibitions

This master task must NOT:
- generate any new image;
- run Library Scale Gate;
- bulk-import the library;
- promote any family to durable approved;
- call Figma as zero-to-one designer;
- modify raw user evidence;
- merge Reference 05 and 13;
- infer a user preference from one liked whole image beyond supported evidence;
- replace long-term distillation with production-only routing.

## 20. Final output

Return only:

# V3 DISTILLATION-FIRST SYSTEM READY FOR HUMAN DISTILLATION REVIEW

Branch:
HEAD:
Legacy classification:
Deep evidence schema:
Visual Program V3 schema:
Family registry:
Distillation compiler:
Transfer operators:
Validation harness:
Semantic asset registry:
Runtime compiler:
Promotion package:
Reference 05 provisional program:
Reference 13 provisional program:
New tests:
Existing relevant tests:
Image generation executed: NO
Scale Gate executed: NO
Git working tree:

## 已完成什么

## 未完成什么

## 需要人工审核什么

Then STOP.
