# VPD V2 — Library Scaling Policy

Status: `MANDATORY_FOR_SCALE`
Date: 2026-08-15

## 1. Problem

A visual preference library may grow from dozens to thousands of restaurant images. Growth is useful only if the system converts additional images into better evidence, broader style-family coverage, and better confidence. Raw item count must not cause prompt/context growth, rule growth, or indiscriminate style averaging.

The architecture therefore separates **evidence scale** from **active decision scale**.

Principle:

> Raw evidence may grow without practical limit; active visual programs and per-task renderer context remain bounded.

More images are valuable when they add independent information. Near-duplicates should strengthen confidence, not create duplicate rules.

## 2. Four memory layers

### L0 — Raw Evidence Vault

Append-only source of truth for every imported image and tied user judgment.

Contains:
- original pixels;
- provenance/hash;
- timestamp/source metadata when available;
- user judgment (`LIKED`, `DISLIKED`, `USABLE`, `UNUSABLE`, `RELATIVE_ONLY`);
- exact comments and revision lineage.

L0 is not loaded wholesale into the renderer.

### L1 — Image Evidence Sheets

Each image may receive a structured photography/design analysis under VPD V2.

Important: a whole-image `LIKED` label does not imply every component is liked.

Where evidence exists, component judgments are separated:
- photography / realism;
- color grade;
- lighting;
- composition;
- typography / lettering;
- copy / semantics;
- grid / layout;
- graphic language;
- material / texture;
- photo-design integration.

This prevents a liked photograph with mediocre typography from teaching the typography system that the mediocre type was desirable.

### L2 — Visual Families

Images are organized into coherent visual families rather than merged into one global restaurant style.

A family is defined by recurring, causally relevant image-making/design mechanisms, not by superficial tags alone.

Examples of family boundaries may include:
- bright editorial real-food photography;
- high-impact fire/chili campaign design;
- restrained monochrome menu editorial;
- tactile print/collage packaging;
- clean modern product still life.

One image may carry secondary memberships, but one family must not silently absorb contradictory mechanisms.

### L3 — Active Style Capsules

A family is represented at generation time by a bounded Style Capsule:
- a small canonical exemplar set;
- validated style signatures;
- measured ranges/tolerances;
- causal priorities;
- degrees of freedom;
- transformation operators;
- failure boundaries;
- renderer compilation policy.

Generation uses the capsule, not the entire library.

## 3. Ingestion decision: every new image must do exactly one primary job

When a new image enters the library, classify its marginal information contribution as one of:

1. `DUPLICATE`
   - exact or near-duplicate visual evidence;
   - retain provenance but do not create new rules.

2. `REINFORCE_EXISTING`
   - substantially supports an already-known family mechanism;
   - raises confidence or narrows/clarifies tolerances.

3. `REFINE_EXISTING`
   - belongs to an existing family but expands a valid range or exposes a missing interaction.

4. `NEW_FAMILY_CANDIDATE`
   - materially different mechanism set; create a candidate family rather than contaminating the old one.

5. `CONTRADICTION_EVIDENCE`
   - conflicts with a current style hypothesis or personal prior;
   - do not average away the contradiction; trigger review of family split, scope, or prior validity.

A new image must not automatically become a new permanent rule.

## 4. Redundancy control

Thousands of similar images can create false certainty through repetition.

Therefore:
- exact duplicates count once for visual evidence;
- near-duplicates are grouped into one redundancy group;
- repeated screenshots/crops/exports of the same underlying work cannot vote independently;
- repeated work from the same campaign/photographer/brand is not treated as fully independent evidence when estimating cross-style personal priors;
- confidence must consider source diversity, not raw file count.

Implementation may use perceptual hash, image embeddings, metadata, and human review. The policy does not depend on one specific embedding model.

## 5. Canonical exemplar policy

A Style Capsule does not need every family member as a renderer reference.

Maintain a small exemplar set selected for complementary evidence roles, such as:
- strongest overall family representative;
- clearest photography/lighting representative;
- clearest typography/layout representative;
- useful boundary/variation representative.

The number is intentionally bounded. Increasing the raw family from 20 to 2,000 images must not make the renderer receive 2,000 references.

Additional images update confidence, ranges, and candidate exemplars in the background.

## 6. Family-level distillation instead of image-level rule accumulation

The pipeline is:

`many images -> individual evidence sheets -> family synthesis -> one bounded capsule`

Do not use:

`many images -> many rules -> one giant prompt`

For each family, synthesize:
- recurrent photographic mechanisms;
- recurrent graphic-design mechanisms;
- allowed variation envelope;
- component interactions;
- causal confidence;
- disagreement/uncertainty.

A mechanism becomes family-level only if supported by sufficiently independent evidence or by controlled output validation.

## 7. Personal taste is learned above, not inside, style families

Cross-style personal priors are promoted only when the same preference recurs across independent visual families.

Examples:
- material realism;
- avoiding dirty yellow casts;
- avoiding plastic AI food;
- preference for purposeful rather than arbitrary decoration.

Do not globally promote:
- a specific palette;
- one font family;
- one layout density;
- one camera angle;
- one type of whitespace;

merely because many images from one family contain it.

Family frequency must not masquerade as personal universality.

## 8. Task-conditioned routing

At generation time, the system first identifies the task and target visual family or family combination.

Relevant distinctions include:
- food photography;
- restaurant hero poster;
- menu/editorial;
- packaging;
- brand identity;
- space/storefront;
- social content.

Only relevant capsules and component priors enter the decision.

The full restaurant library never enters one generation context.

## 9. Controlled style fusion

Combining families is allowed only as an explicit operation.

A fusion must specify which subsystem comes from which family, for example:
- photography grammar from Family A;
- typography hierarchy from Family B;
- material/print language from Family C.

Do not average entire capsules.

If mechanisms conflict, the fusion must identify the conflict and choose a dominant system rather than blending by default.

## 10. Bounded active complexity

The following quantities must remain bounded as the library grows:
- renderer reference attachments;
- high-impact renderer controls;
- hard avoids;
- active Style Capsules per task;
- global personal priors loaded per task.

The exact corpus size must not directly increase prompt length.

Desired scaling behavior:
- storage/evidence grows with image count;
- number of active capsules grows mainly with genuinely distinct visual families;
- per-task renderer context remains approximately constant.

This is a hard architectural requirement.

## 11. Quality-weighted evidence, not popularity-weighted evidence

A family with 500 mediocre liked images must not overpower a family with 20 absolutely excellent, explicitly `USABLE` references merely because the first has more files.

Evidence weighting must prioritize:
- absolute-quality judgment;
- direct user feedback strength;
- independence/diversity of evidence;
- transfer validation;
- consistency of component-level approval.

Raw frequency is secondary.

## 12. Required anti-contamination checks

Before updating a capsule or prior, ask:
- Is this a new mechanism or a duplicate?
- Is approval whole-image or component-specific?
- Is the source independent evidence?
- Does this belong to an existing family or require a new family?
- Does it contradict an existing rule?
- Is the proposed update style-local or truly cross-style?
- Would accepting this update increase active prompt/context size?

If the last answer is YES, prefer compression/replacement/family split over additive rule growth.

## 13. Scale acceptance tests

The system is not considered scalable until it passes all of the following.

### A. Library Growth Invariance

Adding large numbers of redundant images must not materially increase renderer prompt size or reference count.

### B. Family Separation

Adding a materially different restaurant style must create/suggest a new family rather than deforming an unrelated established capsule.

### C. Duplicate Robustness

Duplicating one style/campaign many times must not cause it to dominate unrelated tasks solely by count.

### D. Component Approval Integrity

A whole-image like must not automatically promote every photographic, typography, color, and layout property as positive evidence.

### E. Retrieval/Compilation Stability

Per-task active context remains bounded when the raw vault grows by orders of magnitude.

### F. Quality Non-Regression

More evidence is beneficial only if benchmark output quality is maintained or improved. If the larger library produces worse outputs than an earlier snapshot under the same benchmark, diagnose routing/family/promotion contamination before adding more data.

## 14. Practical end state

A library containing thousands of restaurant references should behave conceptually like:

- thousands of immutable raw evidence items;
- many evidence sheets;
- a manageable number of coherent visual families;
- a small set of validated active capsules relevant to the current task;
- one compact renderer payload.

The system should become **better informed**, not more verbose.

Success is not `more images -> more rules`.

Success is:

> `more independent high-quality evidence -> better family boundaries, better confidence, better transfer, same small generation interface`.
