# V3 Distillation-First Long-Term System — Codex Master Task R2

Status: `CORRECTED_PRIMARY_EXECUTION_TASK`

Repository: `vubaoha034-hash/shenmei`
Branch: `v3-distillation-first-long-term-system-20260817`

## 0. Authority and scope

This R2 task supersedes the uncorrected execution semantics in `V3_DISTILLATION_FIRST_CODEX_MASTER_TASK.md` wherever they conflict.

Mandatory reads, in order:
1. `START_HERE.md`
2. `AESTHETIC_SKILL_DESIGN_CHARTER.md`
3. `VPD_V3_TOP_SKILL_REFERENCE_AUDIT.md`
4. `V3_DISTILLATION_FIRST_SYSTEM_CHARTER.md`
5. `V3_DISTILLATION_FIRST_CORRECTION_AUDIT.md`
6. `V3_DISTILLATION_FIRST_CODEX_MASTER_TASK.md` as historical/base specification
7. existing PHASE 1–8 substrate docs only as needed to reuse, not rebuild
8. current `skill-refiner` durable-promotion contract

No image generation in this task.

## 1. Preserve the existing substrate

Before creating anything, inventory which existing components already provide:
- raw evidence storage;
- Asset Vault;
- evidence ledger;
- provenance/lineage;
- backup/restore;
- privacy/deletion boundaries;
- writer/integrity controls.

Classify them as `FROZEN_SUBSTRATE_REUSE` where still valid.

Do NOT build parallel replacements for already-passed PHASE 1–8 capabilities.
Do NOT ask the user to re-import, relabel, or re-approve raw originals because V3 changes upper algorithms.

Create:
- `V3_SUBSTRATE_REUSE_MAP.md`

## 2. Deep distillation evidence V3

Create/extend the V3 evidence schema for professional analysis across photography, graphic design, and integration, preserving:
- `DIRECT_VISIBLE | METADATA | INFERENCE`;
- confidence;
- evidence pointer/region;
- uncertainty;
- optional measurements;
- `STYLE_SIGNATURE | CONTENT_BOUND | BRAND_BOUND | PRODUCTION_BOUND | OPTIONAL_VARIATION`.

Reuse V2 fields where sound instead of renaming equivalent concepts for cosmetic novelty.

Create migration mapping from V2 evidence fields to V3 only where a real semantic change exists.

## 3. Replace deterministic taste compilation with evidence-backed synthesis

Do NOT implement a deterministic aesthetic authority that decides the style from deep evidence.

Implement two layers:

### A. Evidence support utilities — deterministic
May:
- validate structure;
- rank confidence;
- detect duplication/redundancy;
- surface high-evidence candidate mechanisms;
- enforce bounded package size;
- preserve pointers and lineage.

### B. Distillation synthesizer — hypothesis producing
Produces:
- candidate visual philosophy;
- candidate stable grammar;
- candidate variation axes;
- candidate compatibility constraints;
- unresolved contradictions;
- confidence and evidence for each hypothesis.

Output status remains:
`HUMAN_DISTILLATION_REVIEW_PENDING`.

Human review is required before the candidate stable grammar becomes a Provisional Visual Program used for transfer validation.

Create:
- `schemas/distillation-evidence.v3.schema.json`
- `schemas/distillation-hypothesis.v3.schema.json`
- validators/tests
- `V3_DISTILLATION_SYNTHESIS_CONTRACT.md`

## 4. Visual Program V3

Create:
- `schemas/visual-program.v3.schema.json`

Required fields:
- program_id
- family_id
- status
- visual_philosophy
- mother_reference (optional/nullable where appropriate)
- golden_exemplars
- stable_grammar
- variation_axes
- content_compatibility
- content_bound_features
- brand_bound_features
- typography_role
- color_light_material_signature
- integration_rules
- generic_shortcut_blockers
- freedoms
- transfer_operators
- validation_evidence
- renderer_provenance_requirements
- anchor_dependence
- promotion_history
- evidence_lineage

Rules:
- stable grammar default target is 4–8 high-leverage mechanisms, NOT an aesthetic pass/fail count;
- bounded exceptions allowed with explicit justification;
- generic shortcut blockers hard max = 3;
- no deep-evidence dump into runtime program;
- distinguish invariant hypotheses from validated invariants.

## 5. Visual Mechanism Library

Create a component-level mechanism registry in addition to whole-family programs.

Mechanism domains may include:
- lighting
- color/grade
- capture geometry
- focus/depth/blur
- material treatment
- composition
- whitespace
- typography/lettering
- grid/layout
- graphic language
- photo/type integration
- retouch/finish

Each mechanism record tracks:
- mechanism_id
- domain
- description
- evidence pointers
- family scope
- transfer scope
- `FAMILY_LOCAL | CROSS_FAMILY_CANDIDATE | CONTENT_BOUND | BRAND_BOUND | UNVERIFIED`
- direct user-feedback support if any
- transfer validation support
- contradiction evidence
- promotion status

A whole-image like MUST NOT automatically mark every component as liked.

Create:
- `schemas/visual-mechanism.v3.schema.json`
- `V3_VISUAL_MECHANISM_LIBRARY.json`
- validator/tests.

## 6. Visual Family Registry

Create/extend family registry without averaging conflicting liked styles.

Each family tracks:
- canonical reference(s)
- provisional/validated exemplars
- program version
- contradictions
- near-duplicate reinforcement
- split history
- merge prohibition unless human-approved
- component mechanisms linked to the family
- anchor dependence status.

## 7. New liked work ingestion

A new liked work receives one primary whole-work action:
- `DUPLICATE_OR_NEAR_DUPLICATE`
- `REINFORCE_EXISTING_FAMILY`
- `REFINE_EXISTING_FAMILY`
- `NEW_FAMILY_CANDIDATE`
- `CONTRADICTION_EVIDENCE`

Separately, component-level mechanism evidence may be added only when supported by:
- direct user component feedback;
- repeated evidence;
- or transfer validation.

Do not infer component approval from whole-image approval alone.

## 8. Domain-neutral semantic identity core + restaurant adapter

Create a generic semantic identity contract in core.

Then create restaurant-domain extension supporting:
- canonical dish name
- aliases
- primary ingredient/protein
- cooking method/process
- required visible identity cues
- forbidden substitutions
- hero suitability
- evidence/user authority
- confidence.

Seed the user-provided authoritative identity for:
`ast_63aa377b-5287-400d-b0a3-a6282313b38c`

Canonical dish:
`柠檬叶怪味里脊`
Alias: `柠檬怪味里脊`
Primary ingredient: `猪里脊肉`
Process:
- tenderloin cut into strips;
- fry to set shape;
- higher-temperature refry about 30 seconds for crisp exterior;
- garlic and chili fragments sautéed;
- strange-flavor sauce simmered until thick/sticky;
- fried tenderloin rapidly tossed over high heat until evenly coated.
Required visible cues:
- pork tenderloin strip geometry;
- crisp-fried exterior evidence;
- strips individually readable;
- dark sauce coats rather than erases shape;
- not a shapeless black meat pile.
Forbidden substitutions:
- beef;
- chicken;
- ribs/bone-in meat;
- irregular chunks that erase strip identity.
Current source hero suitability:
`FAIL_FOR_HERO_SOURCE`
This records the suitability of this specific source image, not rejection of the real dish.

## 9. Transfer operators and anchor-dependence validation

Support at minimum:
- RECONSTRUCT
- CONTENT_SWAP
- COMPOSITION_OR_ASPECT_TRANSFER

Optional domain-relevant operators may be added.

Each transfer plan declares:
- preconditions;
- stable grammar that should survive;
- allowed variation;
- semantic identity requirements;
- content compatibility;
- reference/exemplar attachments used;
- expected anchor dependence test;
- failure criteria.

Record anchor dependence as:
- `HIGH_REFERENCE_CONDITIONED`
- `MODERATE_REFERENCE_ASSISTED`
- `LOW_PROGRAM_DRIVEN`
- `UNKNOWN`

Do not equate successful reference-conditioned imitation with fully distilled capability.

## 10. Validation harness

Keep technical correctness separate from human aesthetic judgment.

Codex may validate:
- file integrity;
- text correctness;
- semantic substitutions;
- catastrophic artifacts;
- provenance/renderer metadata;
- contract compliance.

Human pixel review judges:
- photography/art direction;
- graphic-design authorship;
- typography/lettering;
- integration;
- semantic hierarchy;
- family structural fidelity;
- template collapse;
- reference distance;
- appetite/product legibility where relevant;
- absolute usability/top-tier.

Relative gain with poor absolute quality remains:
`RELATIVE_GAIN / ABSOLUTE_FAIL`.

## 11. Runtime compiler is downstream only

Create a bounded runtime package builder only as a consumer of validated/provisional programs.

Typical active package:
- optional mother reference when useful;
- 0–1 golden exemplar by default;
- current content asset(s);
- concise visual philosophy;
- active high-leverage mechanisms;
- max 3 shortcut blockers;
- semantic contract;
- exact copy/brand constraints;
- explicit freedoms.

The runtime builder must never replace deep distillation or become the system center.

## 12. Durable promotion

Promotion package to `skill-refiner` requires:
- transfer evidence;
- human pixel review;
- explicit user approval for long-term aesthetic promotion;
- provenance complete;
- no unresolved contradiction.

No automatic aesthetic promotion by Codex.

## 13. Initial V3 distillation objects

Use canonical approved references:
- `R1C-APPROVED-05.jpg`
- `R1C-APPROVED-13.jpg`

Keep them as separate families.

For each:
1. verify exact identity;
2. create deep evidence object;
3. produce distillation hypothesis object, NOT yet a human-approved Provisional Visual Program;
4. separate style/content/brand/production-bound features;
5. propose component mechanisms with evidence but do not globally promote them;
6. propose compatibility hypotheses;
7. propose transfer operators;
8. record expected anchor dependence;
9. create human distillation review sheet.

Create:
- `V3_REFERENCE_05_DISTILLATION_REVIEW.md`
- `V3_REFERENCE_13_DISTILLATION_REVIEW.md`

Status must be:
`DISTILLATION_HYPOTHESIS / HUMAN_DISTILLATION_REVIEW_PENDING`

Do NOT mark them `PROVISIONAL_VISUAL_PROGRAM` until human review explicitly accepts the distilled mechanism.

## 14. Tests

Add tests for:
- schema validity;
- substrate reuse/no duplicate parallel store;
- deep-evidence/runtime separation;
- bounded runtime package;
- whole-image approval not auto-promoting components;
- family separation;
- state transitions;
- anchor dependence field;
- generic semantic core + restaurant adapter;
- renderer provenance completeness;
- transfer preconditions;
- promotion requires human/user approval.

Run all relevant existing tests.

## 15. Hard stop

This task MUST NOT:
- generate images;
- run Library Scale Gate;
- bulk import the library;
- durable-promote any family/mechanism;
- rewrite stable Phase 1–8 substrate;
- delete raw evidence or experiments;
- merge 05 and 13;
- make retrieval or production the system center.

## Final response

Return only:

# V3 DISTILLATION-FIRST R2 READY FOR HUMAN DISTILLATION REVIEW

Branch:
HEAD:
Frozen substrate reused:
Deep evidence schema:
Distillation hypothesis schema:
Visual Program V3 schema:
Visual Mechanism Library:
Family registry:
Semantic identity core:
Restaurant semantic adapter:
Transfer operators:
Anchor-dependence model:
Validation harness:
Runtime package builder:
Promotion package:
Reference 05 hypothesis:
Reference 13 hypothesis:
New tests:
Existing relevant tests:
Image generation executed: NO
Scale Gate executed: NO
Git working tree:

## 已完成什么

## 未完成什么

## 需要人工审核什么

Then STOP.