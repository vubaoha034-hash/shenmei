# V3 Distillation-First — Correction Audit

Status: `BINDING_CORRECTION_BEFORE_EXECUTION`

## Conclusion

The current V3 Distillation-First direction is substantially aligned with the user's original long-term goal, but it still contains several risks that could recreate the V2 failure mode if executed unchanged.

The project goal remains:

> turn genuinely approved visual works into durable, reusable, transferable visual capability that can guide future AI work across projects, brands, styles, and media — without literal copying and without losing raw human evidence.

The following corrections are mandatory before Codex executes the V3 build.

## Correction 1 — Do not rebuild the already-completed substrate

PHASE 1–8 infrastructure is already completed and must be treated as frozen substrate where still valid:

- raw human evidence store;
- Asset Vault;
- evidence ledger;
- provenance / lineage;
- backup / restore;
- privacy / deletion boundaries;
- writer identity and integrity controls.

V3 must extend this substrate, not recreate a parallel evidence system.

Required classification:
- reuse existing substrate by reference;
- migrate only missing schema/semantic layers;
- never require the user to relabel or re-import the same originals because an upper algorithm changed.

## Correction 2 — Distillation synthesis is not a deterministic taste compiler

The existing Master Task says to implement a deterministic compiler:

`DEEP_EVIDENCE -> PROVISIONAL_VISUAL_PROGRAM`

That is too strong and risks repeating the V2 compression failure.

Correct model:

`DEEP_EVIDENCE -> EVIDENCE-BACKED PROGRAM HYPOTHESES -> HUMAN DISTILLATION REVIEW -> PROVISIONAL VISUAL PROGRAM`

Deterministic code may:
- validate schemas;
- preserve boundedness;
- rank evidence confidence;
- detect duplication/redundancy;
- package runtime controls;
- preserve provenance.

Deterministic code may NOT be the final aesthetic authority selecting what the style "really is".

The high-value stable grammar must remain an evidence-backed hypothesis until human distillation review confirms that it captures the mechanism rather than merely salient surface traits.

## Correction 3 — Add component-level mechanism memory

A whole-image like does not mean every component was liked.

The system needs a `VISUAL_MECHANISM_LIBRARY` in addition to full Visual Programs / families.

Mechanism evidence may cover components such as:
- lighting;
- color grading;
- capture geometry;
- depth / blur;
- material treatment;
- composition;
- whitespace;
- typography / lettering behavior;
- grid / layout;
- graphic language;
- photo/type integration;
- retouch / finishing.

A mechanism may be:
- family-local;
- cross-family candidate;
- content-bound;
- brand-bound;
- unverified.

No component preference may be promoted merely because the whole image was liked. It requires direct user feedback, repeated evidence, or transfer validation that supports that component.

This is required for the original goal of a visual aesthetic operating system that can learn across different brands, projects, and media — not only retrieve whole style families.

## Correction 4 — Numeric counts are defaults, not aesthetic correctness gates

`stable_grammar target 4–8` is a useful compression target, but it must NOT become a hard validator that claims aesthetic validity.

Correct rule:
- default target: 4–8 high-leverage mechanisms;
- may be fewer or slightly more when evidence requires it;
- any exception must remain bounded and justified;
- validator checks boundedness and structure, not taste quality.

Likewise, rule counts must never be interpreted as proof that a style has been understood.

`generic_shortcut_blockers <= 3` can remain a hard runtime boundedness rule because it directly prevents negative-prompt inflation.

## Correction 5 — Keep the core domain-neutral; restaurant semantics are an adapter

The long-term system is intended to apply across brands, projects, and media.

Therefore:
- core Visual Program V3 remains domain-neutral;
- core semantic identity contract is generic/extensible;
- restaurant dish semantics are implemented as a restaurant-domain adapter/extension;
- future photography, travel, packaging, architecture, portrait, etc. may add their own semantic adapters without changing the core Visual Program schema.

Do not couple V3 core architecture to food-only concepts.

## Correction 6 — Measure reference-anchor dependence

The user explicitly rejected a retrieval-only system.

A Mother Reference may remain a useful visual anchor, but the system must record how dependent a program is on the exact reference pixels.

Add `anchor_dependence`:
- `HIGH_REFERENCE_CONDITIONED`
- `MODERATE_REFERENCE_ASSISTED`
- `LOW_PROGRAM_DRIVEN`
- `UNKNOWN`

Transfer validation should record whether family identity survives:
- macro-composition change;
- content change;
- reduced or changed exemplar support when technically meaningful.

This does not require eliminating reference pixels. It prevents falsely claiming that reference imitation equals fully distilled capability.

## Corrected architecture

The durable architecture is:

`EXISTING RAW HUMAN EVIDENCE SUBSTRATE`
→ `DEEP PROFESSIONAL DISTILLATION`
→ `PROGRAM + MECHANISM HYPOTHESES`
→ `HUMAN DISTILLATION REVIEW`
→ `PROVISIONAL VISUAL PROGRAM`
→ `TRANSFER VALIDATION`
→ `HUMAN PIXEL REVIEW`
→ `USER APPROVAL`
→ `SKILL-REFINER DURABLE PROMOTION`
→ `LONG-TERM REUSE`

The Visual Program is the integrated family-level capability.
The Visual Mechanism Library stores component-level reusable evidence without forcing incompatible styles to merge.

## Execution rule

Do not execute the original `V3_DISTILLATION_FIRST_CODEX_MASTER_TASK.md` by itself.

Use the R2 master task that incorporates this correction audit.