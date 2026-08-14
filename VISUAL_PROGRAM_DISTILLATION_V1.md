# Visual Program Distillation V1

Status: `EXPERIMENTAL / NOT_PRODUCTION`
Date: 2026-08-14
Principle: `MODEL_CREATES / SYSTEM_DISTILLS_AND_DIRECTS / HUMAN_JUDGES`

## 1. Problem definition

The system must not reduce the user's goal to `find one liked reference and imitate it`.

The target capability is:

> Take an excellent visual work, distill the generative logic that made it work, preserve enough visual evidence to avoid language-only information loss, and produce a reusable Visual Program that can create new works in the same design family without literal copying. When a new style is introduced, the same distillation compiler must create a new program without rewriting global rules.

This is different from:

- image retrieval;
- a style-name classifier;
- a long prompt summary;
- one global personal style;
- manually rebuilding visual output in Figma;
- training model weights.

## 2. Corrected architecture

The system is split into five responsibilities.

### 2.1 Human evidence memory

Preserve raw approved/rejected images, user comments, A/B choices, revision history, and `USABLE / UNUSABLE` judgments.

This layer answers:

- what the user actually saw;
- what the user actually said;
- which outputs were absolutely usable;
- which were merely less bad.

It does not draw.

### 2.2 Visual Distillation Compiler

Input:

- one source reference work or a tightly related reference set;
- its raw pixels;
- optional user explanation;
- task/domain context.

Output:

- one `VisualProgram` Style Capsule.

The compiler must separate:

1. **Observed visual evidence** — directly visible in pixels;
2. **Generative mechanism** — the design relationship that appears to create the effect;
3. **Fixed invariants** — elements that define the family;
4. **Degrees of freedom** — elements that should vary across outputs;
5. **Transfer operators** — how the program changes when subject/content/aspect ratio changes;
6. **Failure boundaries** — what collapses the family into a generic template;
7. **Visual anchors** — actual image evidence retained from the source.

The compiler is a meta-skill. It must work for a new visual style without changing its own code or global taste rules.

### 2.3 Strong visual model

The image model is the creative renderer.

It receives:

- source/content asset;
- Style Capsule visual anchors;
- a compact compiled direction;
- task-specific factual constraints.

It is allowed to synthesize visual composition, light, material, illustration, atmosphere, visual lettering exploration, and image-world coherence.

The system must not replace this capability with manual low-level Figma node construction during creative exploration.

### 2.4 Production tools

Codex / Figma / vector/layout tools are downstream production tools.

They are used after a visual direction passes quality review for:

- exact copy;
- real editable text;
- layout measurement;
- vector cleanup;
- logos;
- menus;
- packaging dielines;
- exports and production specifications.

They are not the default zero-to-one art director or painter.

### 2.5 Human quality authority

Final aesthetic judgment remains human.

A machine may verify:

- files;
- hashes;
- prompt/reference binding;
- text correctness;
- dimensions;
- prohibited defects.

It may not convert technical correctness into aesthetic PASS.

## 3. The Visual Program is not a prompt

A valid Visual Program must contain four layers.

### Layer A — Visual anchors

Preserve actual source pixels.

Minimum:

- canonical full reference;
- 1–4 optional diagnostic crops/regions if they materially encode typography, texture, composition, or material behavior.

These are not merely thumbnails for a human viewer. They are first-class multimodal conditioning assets.

Why:

Language cannot faithfully preserve optical spacing, stroke energy, micro-contrast, edge behavior, texture, density, and many other high-dimensional visual relationships.

### Layer B — Design grammar

Describe relationships, not adjectives.

Examples:

- hierarchy geometry;
- subject-to-canvas mass relationships;
- negative-space behavior;
- tension between image and type;
- dominant/subordinate element logic;
- color-role logic;
- material/light behavior;
- typography behavior;
- motif derivation rules;
- texture/printing behavior;
- asymmetry and rhythm.

Bad grammar:

- premium;
- artistic;
- clean;
- high-end;
- oriental.

Good grammar:

- primary image mass occupies the lower visual field while display type invades the breathing zone;
- one dominant accent color is repeated only through semantically related elements;
- visual marks derive from the product/process rather than generic geometry.

### Layer C — Degrees of freedom

A reusable visual family must explicitly state what may change.

Examples:

- subject identity;
- crop;
- aspect ratio;
- accent color family;
- wording;
- motif source;
- image count;
- spatial arrangement.

Without this layer, the system only knows how to imitate one frozen image.

### Layer D — Transformation operators

Operators describe how to produce related but non-identical work.

Required operator classes:

- `CONTENT_SWAP`: change subject/content while preserving hierarchy and tension;
- `ASPECT_ADAPT`: adapt composition to a new canvas without merely stretching;
- `PALETTE_SHIFT`: change palette while preserving role relationships;
- `DENSITY_SHIFT`: make a quieter or denser member of the same family;
- `MOTIF_REBIND`: derive supporting graphics from the new subject rather than copying old motifs;
- `TYPOGRAPHY_REBIND`: preserve typographic role/energy while changing literal wording/type construction;
- `MATERIAL_SHIFT`: transfer the family into another material/printing/photographic treatment without copying surface texture blindly.

## 4. Personal taste is not one style

The system must not learn `the user's style = one visual formula`.

It must maintain two different things:

### 4.1 Style Capsules

Local programs distilled from specific successful visual families.

Examples:

- editorial food photography capsule;
- high-impact fire/chili restaurant campaign capsule;
- minimal travel-zine capsule;
- cyber-wuxia concept-art capsule.

These can be very different from each other.

### 4.2 Cross-style personal priors

Only stable preferences supported across independent styles are promoted globally.

Examples may include:

- strong material realism;
- avoidance of dirty yellow casts;
- avoidance of generic AI plastic texture;
- dislike of empty decoration unrelated to the subject;
- preference for clean black hierarchy.

A preference from one style must not automatically become a global rule.

## 5. Approved and rejected evidence have different roles

### Approved evidence

Used to:

- form Style Capsules;
- identify successful design mechanisms;
- validate transfer.

An approved image must be absolutely usable or clearly marked as `RELATIVE_ONLY`.

`RELATIVE_ONLY` examples must never become positive visual anchors.

### Rejected evidence

Used primarily as:

- failure anchors;
- post-generation anti-pattern checks;
- negative retrieval evidence;
- contradiction detection.

Rejected images should not be attached to the renderer as ordinary positive image references unless the renderer has an explicit, auditable negative-image conditioning mechanism.

## 6. Distillation modes

Every Style Capsule supports three modes.

### `RECONSTRUCT`

Purpose: validate whether the distillation captured the source logic.

The output may remain close to the reference family, but must not copy brand identity or protected content.

This mode is a diagnostic test, not the normal production mode.

### `FAMILY`

Purpose: produce a new member of the same visual family with changed subject/content/crop/wording.

This is the normal reuse mode.

The output should be recognizably related in design grammar but not a clone.

### `TRANSFER`

Purpose: preserve only higher-level design mechanisms while changing domain/style surface.

Example:

- keep asymmetrical editorial hierarchy and semantic motif derivation, but move from spicy wok food to a cold dessert campaign.

This mode proves that the system learned design logic rather than memorized one picture.

## 7. New-style onboarding

When the user introduces a genuinely different style, the system must not edit the existing capsule until it fits.

Instead:

1. ingest the new reference pixels;
2. create a new capsule using the same Visual Distillation Compiler;
3. run the same validation gates;
4. only after independent evidence, update cross-style personal priors if appropriate.

The compiler is stable; capsules change.

This is the mechanism that prevents `new style = system no longer knows what to do`.

## 8. Prompt compiler role

The prompt compiler must remain thin.

It converts a Visual Program into a compact renderer instruction that emphasizes approximately 5–8 high-leverage variables.

It must not serialize the whole evidence database or a long rule encyclopedia.

Required renderer payload classes:

- task/content facts;
- visual anchors;
- current mode (`RECONSTRUCT / FAMILY / TRANSFER`);
- fixed invariants;
- selected degrees of freedom;
- 3–6 hard avoids relevant to this specific task.

If the compiled prompt becomes a long generic design manifesto, compilation has failed.

## 9. Direct visual baseline is permanent

Every major architecture revision must retain a direct baseline:

`reference pixels + source/content + short human instruction -> same visual model`

This baseline is not primitive or embarrassing. It represents the strong model used directly.

A more complex system must not be promoted if it consistently performs worse than this baseline.

## 10. Failure taxonomy

### `DISTILLATION_LOSS`

The capsule cannot reconstruct the source family's core visual mechanism.

### `OVERFIT_COPY`

The capsule can only produce near-copies and breaks when content changes.

### `TRANSFER_COLLAPSE`

The capsule works for the source subject but becomes generic when content/domain changes.

### `RULE_INTERFERENCE`

Adding structured constraints makes output worse than direct reference baseline.

### `GLOBAL_TASTE_CONTAMINATION`

A preference from one style harms a different style.

### `CAPABILITY_MISMATCH`

A downstream tool is asked to create visual quality outside its demonstrated ability.

### `RELATIVE_APPROVAL_CONTAMINATION`

A merely less-bad output was treated as a positive style anchor.

## 11. Promotion boundary

V1 remains experimental until the acceptance protocol passes.

Do not:

- replace current production routes;
- bulk re-distill all approved images;
- add embeddings merely because the schema exists;
- promote generated style rules into global taste;
- expand domains.

First prove one capsule, then prove a second unseen style capsule using the same compiler.

## 12. End state

A successful system should be able to answer:

> `How do I make another work like this without copying this exact work?`

with a reusable program consisting of:

- preserved visual evidence;
- design grammar;
- fixed invariants;
- controlled degrees of freedom;
- transformation operators;
- compact generator instructions;
- failure anchors;
- provenance and user quality evidence.

That is the object being learned.
