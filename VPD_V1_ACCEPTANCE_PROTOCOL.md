# Visual Program Distillation V1 — Acceptance Protocol

Status: `MANDATORY_FOR_PROMOTION`

## 1. Purpose

VPD V1 is not accepted because the schema is elegant or because one output looks better than an earlier failed output.

It is accepted only if it demonstrates all of the following:

1. a visual work can be distilled into a reusable program;
2. the program can recreate the source family's logic without literal copying;
3. the program can produce a different member of the same family;
4. the program can transfer higher-level design logic to a changed subject/domain;
5. the same compiler can distill a second, clearly different style without code/rule changes;
6. the more complex system does not consistently underperform direct reference generation;
7. global personal priors do not flatten distinct styles into one look.

## 2. Permanent baseline

For every benchmark task include:

### B0 — Direct Reference Baseline

Input:

- source/content asset;
- raw reference pixels;
- short human instruction;
- same visual renderer used by VPD.

No Visual Program, no ContextPack, no long rule stack.

B0 is a mandatory control condition.

## 3. Capsule conditions

### B1 — Capsule + Raw Visual Anchors

Input:

- same source/content;
- Visual Program;
- its visual anchors;
- compact compiled direction.

Purpose:

Prove that distillation plus compact direction does not degrade the strong direct path.

### B2 — Capsule Reuse / Family

Input:

- new content asset not used to create the capsule;
- same Visual Program;
- same visual anchors;
- `FAMILY` mode.

Purpose:

Prove the system learned a reusable family rather than a one-image prompt.

### B3 — Capsule Transfer

Input:

- changed content/domain or materially different product;
- same Visual Program;
- `TRANSFER` mode;
- only high-level invariants retained.

Purpose:

Prove the program contains generative logic rather than frozen composition.

## 4. Second-style generalization condition

A second reference style must be materially different from the first.

The same compiler version must create Capsule B.

Forbidden between Capsule A and Capsule B:

- changing global design rules to fit Style B;
- adding a Style-B-specific exception to the compiler;
- copying Style A surface features into Style B;
- changing the acceptance standard.

This is the key test for the user's requirement: `new style does not make the system forget how to work`.

## 5. Evaluation dimensions

Each output receives two independent gate classes.

### 5.1 Absolute quality gate

User / independent reviewer:

- `USABLE`
- `UNUSABLE`

Definition of `USABLE`:

The core visual idea could plausibly enter a real project without redesign from scratch. Minor production cleanup is allowed.

Relative improvement does not count.

### 5.2 Distillation fidelity gate

Reviewer answers:

- Does this preserve the source family's hierarchy logic?
- Does it preserve geometry/tension logic?
- Does it preserve color-role relationships?
- Does it preserve material/light behavior where relevant?
- Does it preserve typography role/energy without copying literal glyphs?
- Does it preserve motif derivation behavior?

Result:

- `FIDELITY_PASS`
- `FIDELITY_FAIL`

### 5.3 Non-copy gate

Result:

- `NONCOPY_PASS`
- `OVERFIT_COPY`

Automatic failure if the output merely reproduces distinctive source composition, branding, wording, or exact motifs without task justification.

### 5.4 Transfer gate

For B2/B3:

- `TRANSFER_PASS`
- `TRANSFER_COLLAPSE`

A changed subject must still look like a valid family member while containing subject-derived decisions appropriate to the new content.

## 6. Direct-baseline comparison

For each task compare B0 vs B1 blind where possible.

Acceptable outcomes:

- B1 clearly better;
- B1 equivalent in quality while adding proven reuse/transfer value;
- mixed result with no systematic degradation, if B2/B3 strongly validate reuse.

Promotion blocker:

`RULE_INTERFERENCE` if B1 is repeatedly worse than B0 because the distilled program or compiled constraints suppress visual quality.

Complexity must earn its existence.

## 7. Required first benchmark matrix

Use exactly two style capsules before any production promotion.

### Capsule A — Existing restaurant reference family

Use one existing absolutely liked restaurant reference as source.

Tests:

- A0: B0 direct baseline;
- A1: B1 capsule + anchors;
- A2: B2 new restaurant content;
- A3: B3 materially different food/product transfer.

### Capsule B — Clearly different visual style

Use another approved style with visibly different typography/color/composition/material logic.

Tests:

- B0: direct baseline;
- B1: capsule + anchors;
- B2: new content in family;
- B3: transfer.

Total: 8 primary outputs if one render per condition.

Do not expand to larger batches until the 8-output matrix is reviewed.

## 8. Promotion criteria

All must hold:

1. both capsules validate against schema;
2. visual anchors are raw-pixel bound and hash-traceable;
3. both capsules achieve at least one `USABLE` B1/B2 result;
4. neither capsule is limited to exact near-copy behavior;
5. both B2 conditions pass family reuse;
6. at least one B3 passes transfer, and the other must not show catastrophic collapse;
7. Capsule B is produced with the same compiler without global rule edits;
8. B1 does not show systematic quality degradation versus B0;
9. rejected/relative-only evidence is not used as a positive anchor;
10. no new global personal preference is promoted from a single capsule.

Failure of any hard condition means:

`VPD_V1_NOT_PROMOTED`

## 9. Stop rules

Stop and diagnose before generating more images if any of the following occur:

- `DISTILLATION_LOSS` in A1 or B1;
- `OVERFIT_COPY` in two or more family outputs;
- B1 is visibly worse than B0 in both styles;
- Style B requires code/rule modification to work;
- outputs converge to the same look across distinct capsules;
- any relative-only historical output is discovered as a positive anchor.

Do not respond by adding many more rules.

Diagnose in this order:

1. visual-anchor binding;
2. capsule extraction quality;
3. prompt/compiler compression;
4. renderer capability;
5. only then consider grammar changes.

## 10. Production boundary

Until VPD V1 is promoted:

- existing raw evidence remains frozen;
- no bulk capsule creation;
- no global router switch;
- no deprecation of existing working direct-reference workflows;
- no claim that the system has learned the user's full aesthetic.

The benchmark must prove value first.
