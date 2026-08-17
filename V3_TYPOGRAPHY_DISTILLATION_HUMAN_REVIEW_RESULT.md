# V3 Typography Distillation + Figma Production Layer — Human Review Result

Status: `PASS_WITH_REQUIRED_REVISIONS / NO_TRANSFER_VALIDATION_YET`

Reviewed HEAD: `ae7a24a5263b2bea00f8527d17e174ce240e507d`

## 1. System-level decision

The Typography Distillation + Figma Production Layer is accepted as the correct architectural direction.

The Figma technical dry run is accepted as `FIGMA_RUNTIME_VERIFIED` for technical capability only: live Chinese text, live Latin text, variables, text style, component creation, export and readback were actually exercised. This does not establish aesthetic validity.

The Figma production contracts are materially executable and correctly fail closed on unresolved copy/font/lettering/runtime/export dependencies.

No durable promotion is authorized.

## 2. Reference 05 typography review

Decision: `ACCEPT_WITH_REQUIRED_REVISIONS`

### Accepted as strong family hypotheses

- expressive display lettering as structural visual mass;
- multi-tier information hierarchy;
- campaign claim / proposition bridging identity and process imagery;
- semantic module labelling tied to actual content roles;
- text-image coupling to semantic zones;
- distressed display identity paired with cleaner functional copy;
- deterministic functional text in Figma, with display lettering supplied as an approved asset rather than invented zero-to-one by Figma.

### Required revisions

1. `mech_05_dual_script_support_system` must NOT remain a stable invariant merely because Latin support is visible in the reference.
   - Reclassify as `OPTIONAL_VARIATION / SUPPORTING_MECHANISM` unless future transfer evidence proves it family-defining.
   - Chinese identity/narrative authority is stronger evidence than mandatory bilinguality.

2. Campaign claim rhythm may remain a family hypothesis, but exact claim count, exact wording and exact bilingual structure remain production/content bound.

3. The long-term reusable mechanism is the **behavior** of expressive display lettering; each brand-specific display title asset remains brand-bound and must be newly authored/approved.

4. Figma production may not silently substitute a generic CJK font for missing display lettering.

## 3. Reference 13 typography review

Decision: `ACCEPT_WITH_REQUIRED_REVISIONS`

### Accepted as strong family hypotheses

- asymmetric title-object behavior;
- organic handmade display-lettering behavior;
- active whitespace as structure;
- restrained secondary/tertiary editorial copy;
- shared optical geometry across title, still life and metadata;
- deterministic Figma production for functional labels/body/English support;
- approved display lettering asset placement rather than Figma zero-to-one invention.

### Required revisions

1. `mech_13_editorial_side_rail` is too strong as a stable invariant.
   - Reclassify to `OPTIONAL_OR_EQUIVALENT_COUNTERWEIGHT`.
   - A narrow vertical rail is evidenced, but the deeper mechanism is a restrained secondary counterweight participating in the shared optical geometry.

2. `mech_13_dual_script_editorial_support` must NOT remain a stable invariant.
   - Reclassify as `OPTIONAL_VARIATION / SUPPORTING_MECHANISM` unless future transfer evidence proves bilinguality itself is essential.

3. The family must preserve low-volume secondary/tertiary information rhythm, but not a fixed four-tag count, fixed side-rail coordinate, or mandatory English presence.

4. Exact source glyph outlines remain brand-bound; the reusable family mechanism is asymmetric mass, controlled handmade stroke behavior and optical counter-adjustment.

## 4. Figma capability boundary

Accepted:

- Figma owns exact live text, alignment, spacing, hierarchy, variables, components, vector support marks, deterministic export and placement of approved display-lettering assets.
- Figma runtime has been technically verified.

Not yet solved:

- producing a new high-quality display-lettering asset for a new brand/title.

Therefore the system must add a formal `DISPLAY_LETTERING_SOURCE_PIPELINE` with multiple allowed routes:

1. `APPROVED_FONT_PLUS_CONTROLLED_DEFORMATION`
   - only when a real installed font is a credible starting point;
   - Figma may perform limited evidence-backed deformation;
   - cannot be used when it collapses family identity.

2. `SPECIALIZED_VISUAL_SYNTHESIS_TO_APPROVED_ASSET`
   - image-generation / specialized lettering exploration may create candidate display lettering;
   - candidate must be human-reviewed;
   - selected asset is then cleaned/vectorized or stored as approved pixel art and placed in Figma.

3. `HUMAN_OR_EXISTING_VECTOR_ASSET`
   - user/designer-provided SVG/outline/lettering asset;
   - Figma places and productionizes it.

No route may auto-promote its output.

## 5. Shan Ye Ji / 山野集 reference

The user explicitly requires the typography portion of the supplied “山野集” reference to enter long-term distillation.

Current status remains:
`TYPOGRAPHY_REFERENCE_SOURCE_NOT_CANONICALIZED`

This is a real blocker, not a failure of the typography architecture.

Required next action:

- canonicalize the exact source pixels into the existing private Phase 1–8 evidence substrate;
- record the user instruction that the typography portion is a distillation target;
- do NOT infer that every typography component is individually approved;
- create Typography Deep Evidence and a Distillation Hypothesis only after exact pixels are canonicalized.

## 6. Next authorized work

Authorized:

- apply the 05/13 mechanism reclassifications above;
- add `DISPLAY_LETTERING_SOURCE_PIPELINE` schema/contract;
- canonicalize the exact 山野集 source pixels if available to Codex;
- create 山野集 typography deep evidence + hypothesis after canonicalization;
- prepare, but do not execute, typography transfer validation.

Not authorized:

- typography transfer generation;
- durable promotion;
- Scale Gate;
- family merge;
- Discovery mutation;
- raw evidence rewrite;
- claiming a final production font has been selected.

## 7. Human review summary

The architecture is now correctly separated:

`PIXEL / ART LAYER` -> image generation / photography / scene creation

`DISPLAY LETTERING SOURCE` -> approved asset pipeline

`FUNCTIONAL TYPOGRAPHY + DESIGN PRODUCTION` -> Figma

`LONG-TERM MEMORY` -> Typography Distillation + Visual Program + Mechanism Library

The next missing capability is not Figma runtime. It is the durable creation/approval pipeline for new display-lettering assets and the canonical ingestion of the 山野集 reference.