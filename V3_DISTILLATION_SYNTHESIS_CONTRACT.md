# V3 Distillation Synthesis Contract

Status: `ACTIVE / R2`

## Pipeline

```text
FROZEN RAW EVIDENCE + CANONICAL PIXELS
→ DEEP EVIDENCE
→ EVIDENCE-BACKED DISTILLATION HYPOTHESIS
→ HUMAN DISTILLATION REVIEW
→ PROVISIONAL VISUAL PROGRAM
→ TRANSFER VALIDATION + HUMAN PIXEL REVIEW
→ VALIDATED VISUAL PROGRAM / HOLD / REWORK
```

Deep evidence may be rich. Runtime payloads must stay bounded. Raw evidence is
never rewritten by a derived conclusion.

## Deterministic support utilities

Deterministic code may validate schemas and hashes, preserve lineage, rank
confidence, deduplicate redundant claims, surface candidate mechanisms, and
enforce package limits. It must not decide a visual philosophy, convert one
liked image into component approval, or declare an aesthetic invariant.

`rank_candidate_evidence` ranks support, not taste. A lower-ranked claim is not
less beautiful; it merely has weaker or less direct evidence.

## Hypothesis-producing synthesis

A synthesizer may propose a philosophy, grammar, variations, compatibility,
and contradictions. Every proposal carries evidence IDs, confidence, and
uncertainty. Every grammar item remains `INVARIANT_HYPOTHESIS` and the artifact
remains `HUMAN_DISTILLATION_REVIEW_PENDING` until explicit human acceptance.

The default 4–8 stable-grammar target is a runtime compression target, not an
aesthetic correctness test. A reviewed program may use a bounded exception
with a written justification.

## Component mechanism support

Whole-image approval supports the family candidate only. A component mechanism
may become supported only through direct component feedback, repeated evidence,
or transfer validation. Conflicting liked styles stay in separate families;
family merge is prohibited without explicit human approval.

### Typography and component-separated intake

When a user explicitly likes a new work, the derived V3 intake must preserve
three independent evidence channels:

- `whole_image_evidence`: the user approved the work as a whole;
- `typography_evidence`: only direct statements or pixel observations about
  title, copy hierarchy, script relations, glyph behavior, layout coupling and
  production constraints;
- `component_evidence`: direct feedback about a specific title, English
  system, layout, seal, line, lockup or other named component.

The channels never imply one another. A whole-image like does not confirm the
typography, a typography like does not approve every glyph or copy role, and a
user may explicitly like the image while rejecting its type, or like only the
title, English system, layout, seal, line or lockup. Each supported component
must carry direct user feedback, repeated independent evidence or transfer
validation before its `component_approval_status` can move beyond
`UNCONFIRMED`.

Canonical pixels are mandatory before creating typography deep evidence. A
chat description, filename, contact sheet or remembered visual is not a
canonical source. Missing canonical pixels returns
`TYPOGRAPHY_REFERENCE_SOURCE_NOT_CANONICALIZED` and blocks the candidate rather
than fabricating a distillation.

Typography follows the same review chain as other V3 modules:

```text
CANONICAL PIXELS
→ TYPOGRAPHY DEEP EVIDENCE
→ TYPOGRAPHY DISTILLATION HYPOTHESIS
→ HUMAN TYPOGRAPHY REVIEW
→ PROVISIONAL PROGRAM COMPONENT
→ TYPOGRAPHY TRANSFER VALIDATION
```

Figma is the deterministic production layer for exact live copy, alignment,
spacing, components, variables, approved lettering-asset placement and export.
It is not the default zero-to-one art director for expert Chinese display
lettering. The renderer/Figma responsibility split and every unresolved font,
copy or asset dependency must be carried into the bounded runtime package and
fail closed at production time.

## Anchor dependence

Every transfer records one of:

- `HIGH_REFERENCE_CONDITIONED`
- `MODERATE_REFERENCE_ASSISTED`
- `LOW_PROGRAM_DRIVEN`
- `UNKNOWN`

Reference-conditioned success does not prove low-anchor program capability.

## Runtime boundary

The downstream builder accepts only reviewed provisional or validated programs.
It emits at most two golden exemplars, at most eight active mechanisms, at most
three shortcut blockers, exact current content/copy/brand constraints, a
semantic identity contract, explicit freedoms, and renderer provenance
requirements. It never embeds the deep-evidence object.

## Validation and promotion

Technical correctness and human aesthetic judgment are separate receipts.
Relative improvement below the absolute quality floor is recorded as
`RELATIVE_GAIN / ABSOLUTE_FAIL`.

Durable promotion remains owned by `skill-refiner`. A handoff is eligible only
with transfer evidence, passing human pixel review, explicit user approval,
complete provenance, and no unresolved contradiction. Packaging is not
promotion; Git/evaluation/review gates still apply.
