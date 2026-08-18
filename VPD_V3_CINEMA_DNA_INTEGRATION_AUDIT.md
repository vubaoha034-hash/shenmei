# VPD V3 — Cinema DNA Integration Audit

Status: `ARCHITECTURE_REVIEW_ONLY / NO_PRODUCTION_CHANGE`

Repository: `vubaoha034-hash/shenmei`
Audit branch: `vpd-v3-cinema-dna-integration-audit-20260818`
Base production branch: `visual-program-distillation-v2-photography-design-20260814`
Base production HEAD: `40bf943d1e9b3f2e1d514a2d0b1d5c3b5d402368`
External source: `dacnay816y62-hub/cinema-dna-21x9x3`
External source HEAD: `4e3ec03b0a2ac5ebf5ceb9f4bfac12ec60f54ef1`
Codex required: `NO`
Production compiler modified: `NO`
Active R3A task modified: `NO`

## 1. Decision

Do **not** replace VPD V3 with Cinema DNA and do **not** copy its 21:9 triptych identity, film-director recipes, or cinematic surface style into the restaurant system.

VPD V3 already has the correct higher-level architecture correction: `EXEMPLAR_FIRST`, compact family capsules, 4–7 discriminative controls, visible golden exemplars, and human pixel review. The useful gap exposed by Cinema DNA is lower in the stack: it converts aesthetic intent into a small number of **pixel-causal execution decisions** more aggressively than our current V3 runtime language.

Therefore the correct move is:

`VPD V3 exemplar-first architecture` + `six adapted execution mechanisms` + `no rule-warehouse expansion`.

The six mechanisms below are the maximum allowed transplant set for this audit.

## 2. What Cinema DNA does better at execution time

Cinema DNA repeatedly forces a visual decision to answer a physical or perceptual question before it becomes prompt language:

- composition follows relation/pressure instead of a generic composition template;
- attention has an entry, obstruction/acceleration, decisive landing point, and residue/exit;
- image detail is budgeted instead of maximized;
- light and lens behavior require a physical reason;
- realism comes from selective imperfection rather than global dirt/sharpness;
- recurring failures are converted into validated recipes rather than endlessly adding adjectives.

This is compatible with the VPD V3 charter only if each mechanism remains compact and imageable.

## 3. Six-module delta matrix

### M1 — Visual Causal Chain

Cinema-DNA pattern:
- first determine relationship pressure and why the camera/view exists;
- only then select framing, scale, obstruction, focus and light.

Current VPD V3 gap:
- `DISCRIMINATIVE_SIGNATURE` tells the renderer what separates a family from generic work, but it does not always force an explicit causal reason for the dominant visual arrangement.

Decision: `ADAPT`.

VPD translation:
- add one compact runtime field, conceptually `PRIMARY_VISUAL_CAUSE`;
- it answers: **what visual/business relation makes this composition necessary?**
- for restaurant work this may be appetite-vs-process, product-vs-space, craft-vs-speed, freshness-vs-heat, not cinematic character conflict.

Guardrail:
- one sentence only;
- not a new schema forest;
- not a mandatory narrative story for every commercial image.

### M2 — Attention Flow

Cinema-DNA pattern:
- define where the eye enters;
- what changes its speed or blocks it;
- where it lands;
- what remains partially unresolved;
- where attention exits.

Current VPD V3 gap:
- existing exemplar comparison and hierarchy control are correct, but attention movement is often implicit.

Decision: `ADAPT`.

VPD translation:
- one runtime `ATTENTION_FLOW` sentence;
- commercial version: `entry -> primary appetite/brand landing -> secondary proof -> quiet exit`;
- not every layout needs four visually explicit objects; this is a perceptual flow, not a checklist.

Immediate value:
- useful for preventing equal-weight clutter and template-like left/right module filling.

### M3 — Prompt Density Budget

Cinema-DNA pattern:
- one primary clue, one secondary clue;
- only 2–3 concrete scene details per shot plus camera/light;
- allow mundane, dark, soft, occluded or empty regions.

Current VPD V3 gap:
- V3 correctly keeps runtime context small, but the final image prompt can still over-describe local texture and supporting events.

Decision: `ADOPT WITH DOMAIN TRANSLATION`.

VPD translation:
- one primary visual proof;
- one secondary visual proof;
- at most 2–3 concrete high-value detail cues per focal zone;
- support zones are explicitly allowed to be quieter, softer, simpler or partially occluded.

This is a **prompt-density limit**, not an object-count validator.

Immediate value:
- directly targets AI over-explanation, equal sharpness, decorative debris and synthetic richness.

### M4 — Physical Capture / Light Causality

Cinema-DNA pattern:
- choose a capture substrate;
- special optics/light must have a physical reason;
- restrained optical limits are preferred to generic “cinematic” effects.

Current VPD V3 gap:
- `PRODUCTION_FINISH` and material treatment exist, but capture behavior is not consistently stated as a causal imaging decision.

Decision: `ADAPT`, not literal film-stock copying.

VPD translation:
- use a compact `CAPTURE_BEHAVIOR` rather than a universal film-stock field;
- examples: high-end commercial food photography, documentary kitchen photography, direct-flash street food, soft large-source tabletop, long-lens restaurant observation;
- specify only the physically relevant behavior: highlight roll-off, microcontrast, focus falloff, sensor/lens restraint, practical light direction.

Guardrail:
- 35mm / VHS / MiniDV etc. are optional only when semantically justified;
- “film look” is not a global VPD identity.

### M5 — Controlled Imperfection

Cinema-DNA pattern:
- select one dominant imperfection family;
- do not combine every dirt/noise/smoke/glow mode;
- realism comes from selective limits.

Current VPD V3 gap:
- anti-generic blockers exist, but realism corrections can still accumulate several simultaneous texture effects.

Decision: `ADOPT WITH COMMERCIAL RESTRAINT`.

VPD translation:
- choose one dominant realism correction family per refinement pass;
- examples: food-surface heterogeneity, practical-light inconsistency, print/reproduction defect, lived-in material wear;
- do not simultaneously add grain + smoke + dirt + scratches + droplets + heavy contrast simply to signal “real”.

Immediate value:
- especially strong for R3A because the present blocker is synthetic food/process realism, not lack of drama.

### M6 — Failure-to-Recipe Promotion Loop

Cinema-DNA pattern:
- repeated output failures become validated domain recipes;
- recipes contain usable positive/negative behavior instead of vague “make it better” language.

Current VPD V3 gap:
- VPD already has evidence storage, skill-refiner, human review and continual-learning infrastructure, but recurring aesthetic defects are not yet consistently promoted into narrow, domain-scoped execution recipes.

Decision: `ADAPT`.

VPD translation:
- only repeated, human-confirmed defects may become a recipe;
- recipe scope must be local (e.g. food-gloss realism) rather than global taste law;
- a recipe must contain: observable symptom, likely rendering cause, compact correction, known regression risk, validated before/after evidence, domain scope;
- one-off dislikes remain feedback evidence and must not automatically create a permanent rule.

Guardrail:
- this loop must use the existing evidence/promotion authority;
- it must not bypass the Charter by turning every failure into a blocker.

## 4. Explicit rejects

The following Cinema-DNA mechanisms must **not** enter canonical VPD V3 by default:

1. `21:9 × 3` triptych as a universal output contract.
2. Shot-1 / Shot-2 / Shot-3 narrative progression for non-film commercial work.
3. Director-style or film-media imitation as a default taste engine.
4. Forced focal-length recipes for every visual category.
5. External triptych stitching rhythm as a generic composition method.
6. Mandatory “hidden plot” for product/brand work where no narrative event is needed.
7. Direct copying of its validated scene recipes as our restaurant visual identity.
8. Expansion of our runtime prompt into its full long-form spec.

Reason: these are domain-specific strengths of Cinema DNA. Copying them wholesale would recreate the exact over-engineering/template-collapse risk that VPD V3 is designed to avoid.

## 5. Relationship to current VPD V3 architecture

No architecture replacement is required.

Existing V3 capsule remains:

- `VISUAL_PHILOSOPHY`
- `GOLDEN_EXEMPLARS`
- `DISCRIMINATIVE_SIGNATURE`
- `CONTENT_COMPATIBILITY`
- `TYPOGRAPHY_ROLE`
- `GENERIC_SHORTCUT_BLOCKERS`
- `FREEDOMS`
- `PRODUCTION_FINISH`

The six adapted mechanisms should initially live as **runtime compiler behavior**, not eight new persistent schema fields.

Recommended runtime order:

1. bind canonical exemplar(s) and real content assets;
2. state one `PRIMARY_VISUAL_CAUSE`;
3. state one `ATTENTION_FLOW`;
4. choose one `CAPTURE_BEHAVIOR`;
5. choose one dominant realism/imperfection family when needed;
6. enforce prompt-density budget;
7. compile to 5–8 high-leverage imageable variables;
8. render;
9. human pixel review against visible exemplars;
10. repeated confirmed failure may enter recipe-promotion workflow.

## 6. Immediate application to V3-A R3A

R3A is the correct first bounded test because its current blocker matches the strongest Cinema-DNA anti-AI lesson: synthetic gloss repetition, equal-detail rendering, excessive particles/smoke, and over-dramatized commercial-CG cues.

Do **not** change R3A macro composition, typography, brand identity, or project route.

For the next valid R3A renderer call, adapt only these six controls:

1. `PRIMARY_VISUAL_CAUSE`: appetizing cooked-food material truth must dominate; wok/process energy is supporting proof, not spectacle.
2. `ATTENTION_FLOW`: eye enters at hero food texture, moves to credible wok/process evidence, then exits through quieter dining/context regions.
3. `PROMPT_DENSITY`: hero food gets only a few high-value microtexture differences; supporting process cues are sparse; no “detail everywhere”.
4. `CAPTURE_BEHAVIOR`: real high-end restaurant commercial photography, natural highlight roll-off, moderate microcontrast, non-uniform focus/texture, existing light direction preserved.
5. `CONTROLLED_IMPERFECTION`: only food/material heterogeneity is the dominant imperfection family in this pass.
6. `HARD AVOIDS <=3`:
   - repeated plastic gloss / repeated food geometry;
   - repeated garnish + suspended particles/sparks;
   - global over-sharpening / orange cinematic spectacle.

This should be tested as a **single-candidate R3A edit**, matching the already frozen output budget.

## 7. Promotion gate

This audit does not authorize a production change.

Promotion requires evidence that the compact R3A patch materially improves actual pixels without harming:

- appetite;
- macro composition;
- `现烧` identity;
- process/dining narrative;
- color family;
- later live-typography reintegration.

If the patch fails, do not respond by adding more Cinema-DNA rules. Diagnose whether the failure came from renderer binding/capability, prompt compression, or the chosen control itself.

## 8. Result

`CINEMA_DNA_WHOLESALE_IMPORT = REJECT`

`VPD_V3_ARCHITECTURE_REPLACEMENT = NO`

`SIX_EXECUTION_MECHANISMS = ADOPT/ADAPT`

`FIRST_BOUNDED_TEST = V3-A R3A`

`PRODUCTION_CHANGE = NOT AUTHORIZED BY THIS AUDIT`

`CODEX_REQUIRED = NO`

## 已完成什么

- pinned the current external Cinema DNA source HEAD;
- compared its execution grammar against current VPD V3 exemplar-first architecture;
- reduced the useful transplant surface to exactly six high-leverage mechanisms;
- explicitly rejected its domain-specific triptych/director machinery from canonical restaurant VPD;
- defined a bounded R3A application path without changing the active production task.

## 未完成什么

- no R3A image has been rendered under the compact patch;
- no human pixel validation exists for this integration;
- no canonical VPD V3 compiler/schema has been modified;
- no recipe has been promoted;
- R3B has not started;
- Commercial Quality Gate remains `NOT YET`;
- Golden Exemplar remains `NO`;
- Scale Gate remains blocked.
