# LIU VISUAL SYSTEM V3 — Distillation-First Long-Term System Charter

Status: `PRIMARY_DIRECTION`

## 0. Primary mission

The primary mission of LIU VISUAL SYSTEM is NOT to generate one attractive image quickly.

The primary mission is:

> Take visual works the user truly approves, preserve the raw evidence, distill why they work into durable reusable visual programs, validate that those programs transfer beyond the original image, and make the validated capability available for long-term future use.

Fast image generation is a downstream consumer of the distilled capability.

## 1. Core architecture

The durable system is:

`RAW VISUAL EVIDENCE`
→ `DEEP PROFESSIONAL DISTILLATION`
→ `PROVISIONAL VISUAL PROGRAM`
→ `TRANSFER VALIDATION`
→ `HUMAN PIXEL REVIEW`
→ `DURABLE PROMOTION`
→ `LONG-TERM REUSABLE STYLE / SKILL`
→ `FUTURE PRODUCTION USE`

The system must never collapse this into simple reference retrieval or literal imitation.

## 2. Raw evidence survives forever

For every important source or output, preserve:

- exact original pixels;
- SHA / identity;
- source metadata;
- user feedback in the wording given at the time;
- before/after lineage;
- whether the user judged the revision better, worse, or rejected;
- approved outputs and rejected outputs.

Upper algorithms may be rewritten. Raw human evidence must survive.

## 3. Distillation has two layers

### 3.1 Deep evidence layer

This can be rich and professional.

Photography evidence may cover:
- framing / perspective / focal-distance feel;
- subject occupancy and spatial layers;
- focus plane / depth / blur / motion;
- key/fill/rim/environment lighting;
- falloff / speculars / highlight rolloff;
- exposure and tonal hierarchy;
- color temperature / hue relations / saturation distribution;
- material realism / microcontrast / sharpening / grain / bloom;
- plating / props / scene authenticity;
- retouch / dodge-burn / local cleanup.

Graphic-design evidence may cover:
- semantic intent;
- first/second/third read;
- grid / margins / axes / modular geometry;
- typography / lettering geometry / optical spacing;
- copy hierarchy and meaning;
- whitespace / density;
- color roles;
- graphic marks / motifs / illustration / collage;
- layering / edge / crop behavior;
- material / print language;
- system / sequence behavior.

Integration evidence may cover:
- photo/type dominance;
- color continuity;
- crop/copy co-dependence;
- overlap / avoidance;
- lighting-hierarchy interaction;
- semantic motif binding;
- realism protection;
- thumbnail and second-read behavior.

Evidence fields must distinguish:
- direct visible evidence;
- metadata;
- inference;
- uncertainty / confidence.

### 3.2 Reusable visual-program layer

The durable program must be compact enough to use repeatedly.

A validated Visual Program V3 contains:

- `VISUAL_PHILOSOPHY` — concise worldview / aesthetic intent;
- `MOTHER_REFERENCE` — canonical visual anchor when relevant;
- `GOLDEN_EXEMPLARS` — very small approved set;
- `STABLE_GRAMMAR` — 4–8 mechanisms that define family identity;
- `VARIATION_AXES` — what may change without losing identity;
- `CONTENT_COMPATIBILITY` — scene/content archetypes this program can accept;
- `CONTENT_BOUND_FEATURES` — features tied to the original subject and not reusable;
- `BRAND_BOUND_FEATURES` — features that cannot transfer across brands without evidence;
- `TYPOGRAPHY_ROLE` — display lettering vs functional text behavior;
- `COLOR_LIGHT_MATERIAL_SIGNATURE` — compact perceptual controls;
- `INTEGRATION_RULES` — how photo, type, layout and semantics interact;
- `GENERIC_SHORTCUT_BLOCKERS` — at most three high-value anti-collapse warnings;
- `FREEDOMS` — explicit creative room for the renderer;
- `TRANSFER_OPERATORS` — supported transformations such as content swap, composition shift, aspect-ratio shift, medium/scene adaptation;
- `VALIDATION_EVIDENCE` — outputs and human judgments that prove transferability;
- `PROMOTION_STATUS`.

Deep analysis may be large. Runtime program must stay small.

## 4. Long-term learning is not retrieval-only

The system must not reduce to:

> find the closest old image and imitate it.

Instead:

> infer the reusable mechanism, preserve the approved visual distribution with exemplars, and allow controlled transfer to new content.

A Mother Reference helps anchor the program, but is not the program itself.

## 5. New-style learning

When the user gives a new liked image not represented by an existing family:

1. preserve the raw image;
2. deep-distill it once;
3. create a provisional Visual Program;
4. identify what is likely style-signature vs content-bound;
5. immediately run transfer tests;
6. let the user judge actual outputs;
7. revise the program from pixel evidence;
8. promote only after repeated proof.

A single image can create a provisional hypothesis, not a fully validated invariant.

## 6. Transfer validation is mandatory for durable promotion

A reusable program must prove that it survives controlled change.

Minimum validation families:

- `RECONSTRUCT` — can the program reproduce the family logic without copying assets literally?
- `CONTENT_SWAP` — can it survive a genuinely different compatible subject/content input?
- `COMPOSITION_OR_ASPECT_TRANSFER` — can it survive a different macro composition or aspect ratio?

Optional when relevant:
- `SCENE_ARCHETYPE_TRANSFER`;
- `BRAND_CONTEXT_TRANSFER`;
- `TYPOGRAPHY_ROLE_TRANSFER`;
- `MATERIAL_OR_MEDIUM_TRANSFER`.

A result that merely improves relatively but remains aesthetically poor is `RELATIVE_GAIN / ABSOLUTE_FAIL` and cannot be promoted.

## 7. Human approval remains the durable promotion authority

Codex may analyze, structure, compare and run technical validation.

Codex may NOT declare:
- top-tier;
- beautiful;
- Golden Exemplar;
- user-approved;
- durable aesthetic success.

Those require human pixel review and, for durable user preference promotion, explicit user approval.

The existing `skill-refiner` remains the durable promotion authority for accepted long-term rules/programs.

## 8. Renderer role

The strongest visual model is the artist.

The distillation system is the art director and long-term memory.

Production tools are finishers.

Normal raster validation/production should use the official OpenAI imagegen Skill with built-in `image_gen` unless a task explicitly requires another validated path.

Renderer provenance must be recorded so future evaluation can distinguish program quality from renderer changes.

## 9. Product / content semantics are part of distillation correctness

For restaurant work, a visual program cannot safely transfer if the content asset itself is semantically ambiguous.

Each hero content asset should carry authoritative semantic identity when available:
- canonical dish name;
- main ingredient / protein;
- cooking method;
- visible identity cues;
- forbidden substitutions;
- hero suitability.

This is correctness/context grounding, not taste-rule inflation.

## 10. Style-family scaling

As the approved library grows:

- raw evidence may grow without a hard aesthetic cap;
- active runtime context remains bounded;
- near-duplicates reinforce rather than create new global rules;
- conflicting liked styles remain separate families;
- repeated campaign frames do not vote multiple times globally;
- one liked whole image does not imply every component is liked;
- family programs are revised from evidence, not linearly accumulated rules.

## 11. Codex primary role

Codex's primary work in V3 is to build and maintain the distillation machinery:

- raw-evidence identity and lineage;
- professional evidence extraction;
- Visual Program schemas and compiler;
- family registry;
- semantic asset registry;
- compatibility logic;
- transfer operators;
- validation harness;
- renderer provenance;
- promotion packages;
- tests and anti-regression;
- long-term reuse interfaces.

Codex is not primarily a fast-image operator.

## 12. ChatGPT / human visual-director role

The visual director:

- inspects actual pixels;
- chooses which works are worth distilling;
- checks whether the distillation captured the real mechanism;
- interprets user feedback into high-value hypotheses;
- judges transfer outputs;
- separates technical correctness from aesthetic quality;
- decides whether a program needs refinement, rejection, or new-family split;
- recommends promotion only from visual evidence.

## 13. Production use is a consumer of validated programs

Once a program is validated, future use should be fast:

`user content`
+ `validated Visual Program`
+ `minimal active exemplars`
→ `built-in image_gen`
→ `human pixel check`
→ optional targeted refinement.

The speed comes from prior distillation work being reusable, not from abandoning distillation.

## 14. What must be stopped

Do not make these the center of V3:

- reference retrieval without mechanism distillation;
- production-first architecture that bypasses long-term learning;
- giant runtime schemas;
- rule accumulation after every taste failure;
- Figma/vector reconstruction as zero-to-one art direction;
- blind/ablation protocols as ordinary production workflow;
- technical correctness presented as aesthetic success.

## 15. Final principle

> The system exists to turn approved visual works into durable visual capability.
>
> Every good work should teach the system something reusable.
>
> Every durable rule must be backed by pixels and human judgment.
>
> Every validated capability should become faster to use in the future.
