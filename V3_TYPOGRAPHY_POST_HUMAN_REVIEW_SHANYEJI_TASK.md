# V3 Typography — Post Human Review + Shan Ye Ji Canonical Ingestion Task

Status: `EXECUTE / STOP_BEFORE_TYPOGRAPHY_TRANSFER`

Repository: `vubaoha034-hash/shenmei`
Branch: `v3-distillation-first-long-term-system-20260817`
Required human-review commit: `94cf3ef692e77e46c94ecc4072d16f9a8299831c`

## 0. Primary objective

Apply the human typography review corrections, formalize the missing display-lettering source pipeline, and canonicalize/distill the exact user-supplied “山野集” typography reference.

Do not execute typography transfer validation in this task.

## 1. Mandatory preflight

The active branch must contain:
- `ae7a24a5263b2bea00f8527d17e174ce240e507d`
- `94cf3ef692e77e46c94ecc4072d16f9a8299831c`

Read:
- `V3_TYPOGRAPHY_DISTILLATION_HUMAN_REVIEW_RESULT.md`
- 05/13 typography evidence, hypotheses and Figma contracts
- current Visual Mechanism Library
- current Visual Programs
- current Phase 1–8 raw evidence substrate contracts
- current skill-refiner promotion contract

## 2. Apply Reference 05 human review

Update the 05 typography hypothesis and linked mechanism records:

- keep as strong family hypotheses:
  - display lettering as structural mass;
  - multi-tier information hierarchy;
  - campaign claim/proposition bridge;
  - semantic module labelling;
  - text-image coupling;
  - distressed display / cleaner functional-copy contrast.

- reclassify `mech_05_dual_script_support_system` from stable invariant to:
  `OPTIONAL_VARIATION / SUPPORTING_MECHANISM`

Reason:
Chinese identity/narrative authority is supported; mandatory bilinguality is not yet proven.

Exact Latin presence, exact claim count and exact bilingual structure remain production/content bound.

## 3. Apply Reference 13 human review

Keep as strong family hypotheses:
- asymmetric title object;
- organic display-lettering behavior;
- active whitespace;
- restrained secondary/tertiary copy;
- shared optical geometry.

Reclassify:

`mech_13_editorial_side_rail`
→ `OPTIONAL_OR_EQUIVALENT_COUNTERWEIGHT`

The reusable mechanism is a restrained secondary counterweight participating in shared optical geometry, not a mandatory literal vertical rail.

`mech_13_dual_script_editorial_support`
→ `OPTIONAL_VARIATION / SUPPORTING_MECHANISM`

Mandatory English presence is not proven.

Keep exact four-tag count, exact rail coordinate, exact glyphs and exact copy production/brand bound.

## 4. Display Lettering Source Pipeline

Create a formal reusable schema/contract for producing a new approved display-lettering asset.

Create at least:
- `schemas/display-lettering-source-pipeline.v3.schema.json`
- `V3_DISPLAY_LETTERING_SOURCE_PIPELINE_CONTRACT.json`

Allowed routes:

### Route A — APPROVED_FONT_PLUS_CONTROLLED_DEFORMATION
Use only when a real installed font is an evidence-supported starting point.

Requirements:
- actual font identity recorded;
- deformation operations bounded and auditable;
- Figma may perform controlled deformation;
- human review required;
- fail if output becomes generic or loses family behavior.

### Route B — SPECIALIZED_VISUAL_SYNTHESIS_TO_APPROVED_ASSET
Use image generation / specialized lettering exploration only for candidate art.

Requirements:
- exact requested characters locked;
- candidate must be human-reviewed;
- no candidate becomes production copy automatically;
- selected result is cleaned/vectorized or retained as approved pixel lettering asset;
- Figma places/productionizes the approved asset;
- exact character correctness verified before production.

### Route C — HUMAN_OR_EXISTING_VECTOR_ASSET
Use a user/designer supplied SVG/outline/lettering asset.

Requirements:
- source/provenance captured;
- exact copy verified;
- Figma places and scales it without silently redrawing it.

Every route must record:
- source route;
- exact copy;
- source asset identity;
- family behavior target;
- font/vector/pixel source;
- transformations;
- correctness verification;
- human review status;
- final approved asset ID/hash;
- Figma placement contract;
- promotion status.

No route may durable-promote automatically.

## 5. Canonicalize the exact Shan Ye Ji reference

The user has explicitly supplied an image referred to as “山野集” and explicitly requires its typography portion to enter long-term distillation.

Required input attachment for this task:

`万策餐饮全案策划｜土菜馆逆袭宴请顶流🔥_1_万策餐饮全案设计_来自小红书网页版.jpg`

The task may use a different local attachment filename only if it is demonstrably the same exact user-supplied image bytes.

### If exact pixels are NOT available to Codex

Return:

`SHANYEJI_CANONICAL_INGEST_REQUIRES_IMAGE_ATTACHMENT`

and STOP before creating Shan Ye Ji evidence.

Do not infer from filename, chat summary or prose.

### If exact pixels ARE available

Canonicalize them through the existing PHASE 1–8 private substrate:
- compute SHA-256;
- create/reuse Asset Vault record;
- create sample/evidence lineage;
- do not write raw private pixels to public Git;
- preserve the original source filename/attachment metadata;
- record authority:
  `USER_EXPLICIT_TYPOGRAPHY_DISTILLATION_REQUEST`.

Important:
This authority means the typography portion is a requested distillation target.
It does NOT mean every component is individually approved.

## 6. Shan Ye Ji typography-only distillation

After canonicalization create:
- `V3_TYPOGRAPHY_EVIDENCE_SHANYEJI.json`
- `V3_TYPOGRAPHY_HYPOTHESIS_SHANYEJI.json`
- `V3_TYPOGRAPHY_SHANYEJI_HUMAN_REVIEW.md`

Scope must be explicitly:
`TYPOGRAPHY_ONLY_FAMILY_CANDIDATE / HUMAN_REVIEW_PENDING`

Do NOT create a durable whole-image family from this task.

The evidence should inspect, when actually visible:
- oversized central display lettering;
- irregular block/stone/mountain-like mass behavior;
- negative-space cuts / erosion / missing-stroke behavior;
- orange semantic thread/path integration;
- vertical orange badge/seal role;
- top repeated English claim rhythm;
- secondary English title support;
- restrained Chinese support line;
- handwritten orange slogan role;
- bottom brand lockup and footer balance;
- relationship between dark photographic background and high-contrast typography;
- text-image occupancy and first/second/third read.

Do not assume every listed mechanism is present; only record what exact pixels support.

Every observation must carry:
- DIRECT_VISIBLE / METADATA / INFERENCE;
- confidence;
- evidence region;
- uncertainty;
- STYLE_SIGNATURE / CONTENT_BOUND / BRAND_BOUND / PRODUCTION_BOUND / OPTIONAL_VARIATION.

## 7. Shan Ye Ji Figma producibility hypothesis

Create a provisional Figma producibility map, NOT a final production contract.

It must distinguish:
- exact functional live text;
- top English claim groups;
- badge/seal live text or approved vector asset;
- orange semantic line as vector path;
- handwritten slogan as live-font candidate vs approved lettering asset pending review;
- central display title as `DISPLAY_LETTERING_SOURCE_PIPELINE_REQUIRED` unless a credible real-font route is proven;
- bottom brand lockup as deterministic live text / supplied brand asset where appropriate.

No claim that Figma can perfectly reproduce the central display title is allowed until a source route is human-approved and technically validated.

## 8. Update long-term typography ingestion rules

The V3 ingestion contract must support component-scoped user evidence:

- WHOLE_IMAGE_APPROVED
- TYPOGRAPHY_DISTILLATION_REQUESTED
- TYPOGRAPHY_APPROVED
- TYPOGRAPHY_REJECTED
- DISPLAY_TITLE_APPROVED
- FUNCTIONAL_TYPE_APPROVED
- LAYOUT_APPROVED
- BILINGUAL_SYSTEM_APPROVED
- BADGE_OR_MARK_APPROVED
- COMPONENT_UNCONFIRMED

A whole-image approval may not populate the component states automatically.

## 9. Prepare typography transfer planning only

After 05/13 corrections and Shan Ye Ji hypothesis creation, prepare reviewable future typography transfer plans.

Do NOT execute them.

Plans should explicitly separate:
- display-lettering source creation/approval;
- Figma functional typography production;
- final compositing/export;
- human pixel review.

## 10. Tests

Add/update tests for:
- 05 bilingual mechanism downgraded from invariant;
- 13 side-rail no longer mandatory invariant;
- 13 bilingual support no longer mandatory invariant;
- display-lettering route schema validity;
- no route auto-promotes;
- exact copy required before approved display asset;
- Shan Ye Ji cannot distill without canonical pixels;
- typography-only family candidate does not create whole-image family approval;
- raw pixels remain private;
- component-scoped user evidence separation;
- Figma contract/runtime separation remains intact;
- Discovery remains unchanged.

Run all relevant existing tests.

## 11. Prohibitions

Do NOT:
- generate final poster images;
- execute typography transfer;
- execute Content Swap or Composition/Aspect Transfer;
- run Scale Gate;
- durable-promote typography mechanisms;
- alter Discovery approval counts;
- rewrite raw evidence;
- merge 05/13/Shan Ye Ji typography families;
- claim display-lettering creation is solved merely because Figma runtime works.

## 12. Final response

Return only:

# V3 TYPOGRAPHY POST-REVIEW + SHANYEJI INGESTION READY FOR HUMAN REVIEW

Branch:
HEAD:
Starting human-review commit verified:
Reference 05 mechanism corrections:
Reference 13 mechanism corrections:
Display Lettering Source Pipeline:
Shan Ye Ji image attachment available:
Shan Ye Ji canonical asset:
Shan Ye Ji typography evidence:
Shan Ye Ji typography hypothesis:
Shan Ye Ji Figma producibility map:
Component-scoped evidence rules:
Typography transfer plans:
New tests:
Relevant tests:
Image generation executed: NO
Typography transfer executed: NO
Scale Gate executed: NO
Durable promotion executed: NO
Discovery modified: NO
Raw private pixels committed to Git: NO
Git working tree:

## 已完成什么

## 未完成什么

## 需要人工审核什么

Then STOP.