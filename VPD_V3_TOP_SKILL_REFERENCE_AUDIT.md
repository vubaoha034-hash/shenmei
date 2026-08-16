# VPD V3 — Top Visual Skill Reference Audit

Status: `ARCHITECTURE_REVIEW_ONLY / NO_PRODUCTION_CHANGE`

Purpose: audit VPD V3 against current high-signal visual Skill patterns before any V3 implementation. This file must not change the active production compiler or current CSR1 experiment.

## 1. Problem being corrected

The draft V3 direction risked turning photography, typography, layout, brand semantics, and anti-collapse logic into a large rule warehouse. That would repeat the failure mode already seen in VPD V2: rich analysis upstream, then brittle compression or generic interpretation downstream.

The target is not a larger ruleset. The target is a thin art-direction system that keeps proven visual artifacts visible and lets the strongest visual model do the creative work.

## 2. Reference Skill patterns reviewed

### A. OpenAI Product Design / ideate
Adopt:
- inspect actual visual references directly, never infer from filenames;
- attach screenshots/reference images/brand assets to Image Gen rather than relying on text summaries;
- inspect only the context needed for the current task, not the whole saved library;
- generate distinct complete visual options with meaningfully different hierarchy/layout strategies;
- after user feedback, regenerate/refine from the selected visual rather than drifting into abstract planning.

Implication for VPD V3:
- active visual context must remain tiny and directly visible;
- a style family should carry selected approved exemplar images, not only distilled text;
- the selected visual result becomes the next refinement target.

### B. OpenAI Product Design / image-to-code
Adopt:
- a selected image/screenshot/mockup is a stronger execution target than a written brief;
- do not proceed from a written brief alone when fidelity to a visual target is required;
- resolve exact target identity before execution.

Implication for VPD V3:
- approved visual artifacts must be first-class canonical evidence;
- exact exemplar identity must be bound by file/hash, never attachment order.

### C. OpenAI Build Web Apps / frontend-app-builder
Adopt:
- concept first, implementation second;
- one clear visual point of view;
- fewer, stronger visual elements rather than filling space;
- preserve design as a system across the surface;
- keep improving against the accepted visual target rather than declaring success from technical correctness.

Implication for VPD V3:
- avoid feature/checklist accumulation;
- visual coherence outranks field coverage;
- QA must compare the rendered artifact to the accepted family exemplars.

### D. Anthropic / canvas-design
Adopt:
- generate a compact visual philosophy/aesthetic worldview rather than a template dump;
- communicate through form, space, color, composition, imagery, rhythm and hierarchy;
- leave creative room for the renderer;
- refine the existing composition on the second pass instead of reflexively adding more elements.

Adapt:
- VPD V3 should not copy the philosophy-writing format literally; restaurant design needs stronger grounding in real food, brand semantics, typography and commercial hierarchy.

Implication for VPD V3:
- each style family needs a compact `VISUAL_PHILOSOPHY` plus a small set of structural signatures;
- the philosophy guides interpretation; exemplars ground the actual visual distribution.

### E. Anthropic / frontend-design
Adopt:
- anti-generic design must be explicit;
- make opinionated, context-specific choices instead of defaulting to common AI aesthetics;
- typography, palette and layout should express one coherent point of view.

Implication for VPD V3:
- generic shortcut detection stays, but as a small targeted blocker, not a growing negative-prompt warehouse.

### F. Skill-creator patterns
Adopt:
- concrete validated examples are required to define an effective Skill;
- keep core Skill compact and move detail into supporting references/scripts when needed;
- evaluate behavior against examples/benchmarks rather than assuming prose correctness.

Implication for VPD V3:
- V3 must be validated on approved real visual examples before promotion;
- large field schemas may remain in evidence storage, but must not all load into the runtime prompt.

## 3. Core architecture correction

VPD V3 must be `EXEMPLAR_FIRST`, not `RULE_FIRST`.

### Runtime package for one generation
Maximum active visual context:
1. one canonical mother/reference image;
2. one or two approved family exemplars when available;
3. current real content asset(s);
4. one compact visual philosophy;
5. 4–7 discriminative structural controls;
6. at most 3 generic-shortcut blockers;
7. exact required copy/brand constraints.

Everything else remains evidence/archive and is not loaded by default.

## 4. Style Capsule V3

A validated family capsule should contain:

- `VISUAL_PHILOSOPHY`: 3–6 concise sentences, not a rules dump;
- `GOLDEN_EXEMPLARS`: 1–3 approved finished outputs or approved references with hashes;
- `DISCRIMINATIVE_SIGNATURE`: 4–7 mechanisms that separate this family from generic restaurant design;
- `CONTENT_COMPATIBILITY`: what scene archetypes this family can transfer to without breaking;
- `TYPOGRAPHY_ROLE`: display lettering vs functional copy behavior;
- `GENERIC_SHORTCUT_BLOCKERS`: <=3;
- `FREEDOMS`: what the renderer may reinterpret;
- `PRODUCTION_FINISH`: deterministic typesetting/cleanup only when required, never as zero-to-one art direction.

## 5. Two rendering modes

### FAST FAMILY MODE
Use when a validated family exists.

Input:
- user brief/content;
- mother reference;
- golden exemplar(s);
- compact capsule.

Action:
- generate immediately with the strongest visual model;
- default one candidate when the user asks for direct execution;
- use 2–3 independent candidates only when exploration is explicitly useful.

Goal:
- seconds/minutes to a useful visual, not another analysis phase.

### NEW STYLE DISCOVERY MODE
Use when the user gives a new liked image/style not represented by a validated family.

Action:
- analyze deeply once;
- produce a provisional compact capsule;
- generate a small number of complete artifacts immediately;
- user judges the artifacts;
- revise capsule from artifact feedback;
- only after repeated success can the family become validated.

Goal:
- learn through finished visual evidence, not through schema completion alone.

## 6. Typography correction

Do not make Figma/Codex vector drawing the default Chinese display-lettering generator.

Two-track typography:
- `DISPLAY_LETTERING`: strongest visual model or an approved reusable lettering asset/style exemplar;
- `FUNCTIONAL_TEXT`: deterministic professional typesetting after the visual direction is accepted when exact wording/readability matters.

Display lettering is judged as part of visual authorship, not merely correctness.

## 7. QA correction

Every candidate must be judged against visible golden exemplars, not only abstract rubric scores.

Required QA views:
- candidate alone;
- side-by-side with the relevant mother reference / golden exemplar;
- thumbnail view;
- normal view;
- detail view.

The system must separately report:
- technical correctness;
- absolute aesthetic quality;
- reference-family structural fidelity;
- generic-template collapse.

Technical correctness cannot promote an aesthetically weak artifact.

## 8. What V3 must NOT do

- no linear growth of runtime rules as the library grows;
- no averaging multiple conflicting liked styles into one family;
- no loading hundreds of stored references into one generation;
- no full-schema dump into Image Gen prompts;
- no automatic conversion of every liked whole image into global rules;
- no Figma/vector reconstruction as default creative path;
- no declaring success because output is readable, realistic, or technically intact;
- no promotion without finished visual evidence.

## 9. Adoption gate

Do not implement V3 production changes until the current CSR1 contrastive-signature experiment is completed and frozen.

After CSR1:
- if contrastive feature selection materially improves both families, incorporate it as part of `DISCRIMINATIVE_SIGNATURE`;
- if it fails, do not keep expanding compiler rules; prioritize exemplar-first rendering and investigate renderer capability / integrated-layout limits.

## 10. Final architectural principle

`RAW HUMAN EVIDENCE + APPROVED FINISHED VISUALS -> COMPACT FAMILY CAPSULE -> STRONGEST VISUAL MODEL -> HUMAN PIXEL REVIEW -> REFINEMENT`

The Skill is the art director and memory system. The visual model is the artist. Approved finished work is the strongest guardrail against drift.
