# VPD V2 Next Experiment — Role-Specific Visual Anchor Ablation

Experiment ID: `ROLE_SPECIFIC_VISUAL_ANCHOR_ABLATION`
Status: `AUTHORIZED_NEXT_EXPERIMENT_ONLY`

## Question

Did both style families collapse into `brush headline + plated food` primarily because the renderer received each complex reference as an overly compressed whole-image anchor, losing role-specific visual information before/while the thin prompt was applied?

## Hypothesis

Keeping the exact current V2 reconstruction prompt and all task facts unchanged, but adding source-derived role-specific raw-pixel crops should reduce template collapse and improve reference-distance scores.

This experiment tests visual-anchor granularity only.

It does NOT change:

- compiler code;
- capsule text;
- causal priorities;
- renderer prompt wording;
- headline wording;
- source/content asset;
- model;
- output aspect ratio;
- hard avoids.

## Styles

Style A reference: `R1C-APPROVED-05`

Style B reference: `R1C-APPROVED-13`

## Style A diagnostic anchors

The full Reference 05 remains attached.

Add source-derived crops that preserve the roles lost in generic Style A outputs:

1. `A_HERO_PROCESS_ANCHOR`
   - top hero panel containing chef hands, wok, flame, steam and active cooking process;
2. `A_IDENTITY_HIERARCHY_ANCHOR`
   - compact brand mark + supporting copy region, preserving that typography is not simply one giant generic headline;
3. `A_CAMPAIGN_SYSTEM_ANCHOR`
   - representative mid-board panel region showing image module + semantic icon + small-copy hierarchy.

No synthetic crop may be created. Crops must be exact rectangular pixel regions from the canonical reference and hash/provenance traceable.

## Style B diagnostic anchors

The full Reference 13 remains attached.

Add source-derived crops:

1. `B_TITLE_GEOMETRY_ANCHOR`
   - main irregular multi-glyph title field plus right-side vertical information rail where possible;
2. `B_STILL_LIFE_ANCHOR`
   - dark clay pot and ingredient arrangement;
3. `B_INFORMATION_RHYTHM_ANCHOR`
   - lower hashtag/information row plus body-copy region.

Again: exact source pixels only; no synthetic restyling.

## Conditions

Exactly four valid primary outputs in one run:

- `A_CONTROL_FULL_REFERENCE_ONLY`
- `A_TREATMENT_FULL_PLUS_ROLE_ANCHORS`
- `B_CONTROL_FULL_REFERENCE_ONLY`
- `B_TREATMENT_FULL_PLUS_ROLE_ANCHORS`

For each style, control and treatment must use the same current V2 RECONSTRUCT renderer payload, same content bytes, same headline, same dimensions and same underlying visual model.

The ONLY intended difference is the additional role-specific raw-pixel anchors in treatment.

## No hidden sampling

- exactly 4 valid primary outputs;
- no best-of-N;
- no cosmetic retries;
- deterministic invalid-file retry only with quarantine/logging;
- no extra exploratory image.

## Blind review

Package four outputs with neutral labels.

The reviewer must not know control/treatment or Style A/B condition names.

Review must use the calibrated dual-axis rubric:

### Technical correctness
- text correctness;
- gross image defects;
- material plausibility;
- structural integrity.

### Aesthetic quality / reference distance
- photography/art-direction quality;
- graphic-design quality;
- typography/lettering quality;
- photo-design integration;
- authored distinctiveness;
- reference-family structural fidelity;
- generic restaurant-template collapse;
- absolute `USABLE / UNUSABLE`;
- `TOP_TIER true/false`.

Technical correctness must not inflate aesthetic scores.

## Pass rule

The experiment supports the anchor-granularity hypothesis only if BOTH treatments:

1. visibly preserve at least two reference-family structures missing from their matched controls;
2. reduce `brush headline + plated food` generic-template collapse;
3. improve reference-distance judgment materially;
4. do not reduce material realism;
5. show improvement in independent human review before condition disclosure.

A prettier color grade alone is not a pass.

If only one style improves, result is `PARTIAL_SUPPORT` and anchor decomposition is not sufficient as a universal fix.

If neither improves, reject anchor granularity as the primary bottleneck and next investigate compiler/prompt discriminative-feature selection.

## Hard stop

After the four outputs are generated, packaged and blind-reviewed, STOP.

Do not:

- modify the compiler;
- add aesthetic rules;
- run content swap;
- run typography repair;
- run Library Scale Gate;
- bulk-distill the library.
