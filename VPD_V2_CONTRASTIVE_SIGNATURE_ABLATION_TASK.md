# VPD V2 — Contrastive Signature Selection Ablation

Status: `FROZEN_NEXT_EXPERIMENT`

Repository: `vubaoha034-hash/shenmei`
Required branch: `visual-program-distillation-v2-photography-design-20260814`

## Why this experiment exists

The frozen Role-Specific Visual Anchor Ablation produced only partial support:

- Reference 05 improved slightly when role-specific crops were added, but remained `UNUSABLE` and still heavily collapsed into the generic `large brush title + food plate` pattern.
- Reference 13 became worse when role-specific crops were added.
- Therefore the project must not keep adding more image anchors as the default fix.

The next primary hypothesis is:

`DISCRIMINATIVE_FEATURE_SELECTION_FAILURE`

The current compiler tends to select visually salient / high-impact controls, but it does not explicitly prefer controls that distinguish the target reference family from a generic Chinese restaurant-poster prior.

A feature can be high-impact yet non-discriminative.

Examples of non-discriminative/common-mode features:

- Chinese brush-like title;
- food hero image;
- red/black heat cues;
- warm beige background;
- generic restaurant mood.

These features are easy for the renderer to realize and can dominate more distinctive structural mechanisms.

## Experimental question

Does replacing `high-impact-only` control selection with `contrastive discriminative signature` selection materially reduce template collapse and reference distance, while preserving technical correctness and food/material realism?

## Frozen inputs

Use exactly the same canonical references, reconstruction content assets, target headline, aspect ratio, output size, strongest available visual model, one-attempt policy, and technical integrity policy as the existing VPD V2 RECONSTRUCT benchmark.

Style A reference:
`R1C-APPROVED-05.jpg`

Style B reference:
`R1C-APPROVED-13.jpg`

Do not use role-specific crops in this experiment. Use full canonical reference pixels only for both Control and Treatment so the only changed variable is control selection/compilation.

## Conditions

Generate exactly 4 valid primary outputs:

1. `A_CONTROL_CURRENT_COMPILER`
2. `A_TREATMENT_CONTRASTIVE_SIGNATURE`
3. `B_CONTROL_CURRENT_COMPILER`
4. `B_TREATMENT_CONTRASTIVE_SIGNATURE`

No hidden outputs.
No best-of-N.
No cosmetic retry.
A deterministic invalid-byte/tool failure may be replaced only with quarantine + receipt.

## Control conditions

Control uses the current frozen V2 RECONSTRUCT renderer payload exactly as already defined for each family.

Do not improve, reinterpret, or clean it up.

## Treatment compiler layer

Do NOT rewrite the global compiler yet.

For this experiment only, add one experimental post-analysis selection layer:

`CONTRASTIVE_SIGNATURE_SELECTOR_V0`

It receives the existing measured evidence / causal hypotheses and selects renderer controls by two axes:

1. causal importance to the reference family's visual quality;
2. discriminative value versus a generic Chinese restaurant-poster prior.

A candidate control should be down-ranked if it is common across many generic restaurant outputs and does not materially distinguish the reference family.

The final treatment payload must still remain thin:

- 4–8 positive structural controls;
- max 3 generic-shortcut suppressions;
- same task/content facts;
- same full raw reference pixels;
- same explicit freedoms;
- no role crops;
- no new aesthetic database rules.

## Required family-specific discriminative structures

The selector must derive controls from actual source evidence, but the treatment must preserve the following structural classes because they are visibly material to each reference and are not equivalent to generic brush-title food posters.

### Reference 05 family

Treatment must prioritize structural mechanisms equivalent to:

- `PROCESS_SCENE_HIERARCHY`: cooking/action/process imagery must materially participate in the visual identity, rather than reducing the design to a plated-dish hero shot.
- `MULTI_TIER_INFORMATION_SYSTEM`: visual identity includes clear secondary/tertiary information modules, not only one oversized headline.
- `CAMPAIGN_MODULE_LOGIC`: supporting ingredient/origin/process modules or equivalent structured storytelling must exist as part of the composition, adapted to a single-poster output rather than copied as a board.
- `SEMANTIC_GRAPHIC_DERIVATION`: graphic marks must derive from cooking/ingredient/origin semantics, not generic decorative brush strokes.

Generic shortcut suppressions should include the equivalent of:

- do not reduce the entire design to `oversized brush title + one plated dish + red/black field`;
- do not use red brush blocks as a substitute for the source's information architecture.

### Reference 13 family

Treatment must prioritize structural mechanisms equivalent to:

- `ASYMMETRIC_TITLE_FIELD`: title is a spatial object with non-uniform character scale, position, rhythm and negative-space tension; not a single horizontal headline row.
- `VESSEL_INGREDIENT_STILL_LIFE`: the photographic/illustrative anchor is a vessel/ingredient still-life relationship or a semantically adapted equivalent, not merely a finished plated dish under a headline.
- `EDITORIAL_INFORMATION_RHYTHM`: vertical-side information, lower information band, caption/body relationships, or an adapted equivalent must create editorial hierarchy beyond the hero title.
- `ACTIVE_WHITESPACE_GEOMETRY`: empty space must be shaped by the title, still-life and information system, not left as passive beige background.

Generic shortcut suppressions should include the equivalent of:

- do not reduce the design to `beige background + brush title + centered plated dish`;
- do not treat brush-calligraphy appearance itself as the style signature.

## Absolute aesthetic review

Blind review must use the calibrated dual-axis rubric:

### Technical Correctness

- file/image integrity;
- catastrophic text errors;
- catastrophic structural artifacts;
- baseline material plausibility.

### Absolute Aesthetic Quality

Score independently:

- photography/art direction;
- graphic-design authorship;
- typography/lettering;
- photo-design integration;
- semantic hierarchy;
- reference-family structural fidelity;
- generic-template collapse;
- reference distance;
- `USABLE / UNUSABLE`;
- `TOP_TIER true/false`.

Technical correctness MUST NOT elevate aesthetic scores.

The corresponding reference is the 10/10 family benchmark.

## Pass criteria

`SUPPORTED` only if BOTH Treatment outputs, before unblinding:

- improve `reference_family_structural_fidelity` by at least +2.0 versus paired Control;
- reduce `generic_template_collapse` by at least 2.0;
- reduce `reference_distance` by at least 1.5;
- improve both `graphic_design_authorship` and `semantic_hierarchy` by at least +1.5;
- do not reduce technical correctness or food/material realism by more than 0.5;
- visibly retain at least two family-specific structural mechanisms that are absent or materially weaker in Control;
- are not judged as the same `large brush title + food plate` template with cosmetic variation.

Additionally, at least one Treatment must reach `USABLE` under the project's strict final-work definition.

`PARTIAL_SUPPORT` if both families show material structural improvement but the strict `SUPPORTED` threshold is not fully met, or if one family passes the structural thresholds while the other is neutral (not materially worse).

`HYPOTHESIS_REJECTED` if neither family materially improves, or if either Treatment materially worsens template collapse/reference distance while the other fails to meet the structural thresholds.

## Stop rule

After exactly 4 valid outputs are blind-reviewed, frozen, and unblinded, STOP.

Do not:

- modify the global compiler;
- add more reference images;
- change the content assets;
- add rules to the production Skill;
- enter Library Scale Gate;
- bulk-import the library.

The result determines whether contrastive/discriminative feature selection deserves replication or whether the next bottleneck is renderer capability / layout-text production separation.
