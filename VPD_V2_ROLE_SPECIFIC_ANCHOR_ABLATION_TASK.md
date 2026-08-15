# VPD V2 — Role-Specific Visual Anchor Ablation Task

Status: `FROZEN_EXECUTION_TASK`

## Repository

`vubaoha034-hash/shenmei`

## Required branch

`visual-program-distillation-v2-photography-design-20260814`

## Required reads

Read completely before execution:

1. `VPD_V2_CALIBRATED_ABSOLUTE_UNBLIND_RESULT.json`
2. `VPD_V2_TEMPLATE_COLLAPSE_ROOT_CAUSE.md`
3. `VPD_V2_NEXT_EXPERIMENT_ROLE_SPECIFIC_ANCHOR_ABLATION.md`
4. `VPD_V2_EVALUATION_RUBRIC_CALIBRATION_V2.md`
5. `VPD_V2_DESIGN_SPEC_DRAFT.md`
6. `VISUAL_DISTILLATION_COMPILER_CONTRACT_V2.md`
7. `VPD_V2_MEASUREMENT_AND_CAUSAL_SPEC.md`

Do not use the invalid old 8–9 point blind review as an aesthetic success signal.

## Objective

Test exactly one hypothesis:

`STYLE_SIGNATURE_COMPRESSION_COLLAPSE` may be materially caused by treating a complex reference as one monolithic image anchor, causing the renderer to retain only generic cross-style cues.

Do not repair the compiler yet.
Do not add rules.
Do not modify the headline.
Do not change content.

## Reference A

`R1C-APPROVED-05.jpg`

This is a multi-panel campaign/brand board.

Control:
- current full-reference-only V2 RECONSTRUCT binding.

Treatment:
- same full reference;
- plus exact source-derived pixel crops defined by the experiment spec:
  - A_HERO_PROCESS_ANCHOR;
  - A_IDENTITY_HIERARCHY_ANCHOR;
  - A_CAMPAIGN_SYSTEM_ANCHOR.

All crops must be literal rectangles from the source pixels and hash traceable.

## Reference B

`R1C-APPROVED-13.jpg`

Control:
- current full-reference-only V2 RECONSTRUCT binding.

Treatment:
- same full reference;
- plus exact source-derived crops:
  - B_TITLE_GEOMETRY_ANCHOR;
  - B_STILL_LIFE_ANCHOR;
  - B_INFORMATION_RHYTHM_ANCHOR.

## Frozen variables

For each matched pair keep exactly the same:

- source/content image bytes;
- target aspect ratio;
- exact headline wording;
- current V2 RECONSTRUCT renderer payload text;
- hard avoids;
- strongest available visual model;
- model/tool configuration where controllable;
- output size;
- one-attempt policy.

The ONLY intentional independent variable is additional role-specific raw-pixel anchors in treatment.

## Outputs

Generate exactly four valid primary outputs:

- `A_CONTROL_FULL_REFERENCE_ONLY`
- `A_TREATMENT_FULL_PLUS_ROLE_ANCHORS`
- `B_CONTROL_FULL_REFERENCE_ONLY`
- `B_TREATMENT_FULL_PLUS_ROLE_ANCHORS`

No other image generation is allowed.

No best-of-N.
No hidden retries for aesthetics.
A deterministic invalid-file retry is permitted only with quarantine and receipt.

## Packaging

Upload four outputs to a fresh Drive folder using random neutral labels.

Do not expose:

- A/B;
- control/treatment;
- reference identity;
- condition names.

Save private mapping and generation receipts.

## Review rubric

Blind review must use two separate axes.

### Technical correctness

- image integrity;
- text correctness;
- catastrophic visual defects;
- material plausibility.

### Absolute aesthetic quality

Judge against the project's approved-reference level, not ordinary restaurant-ad acceptability:

- photography/art direction;
- design authorship;
- typography/lettering;
- photo-design integration;
- semantic hierarchy;
- structural reference-family fidelity;
- generic-template collapse;
- reference distance;
- `USABLE / UNUSABLE` under the user's final-quality standard;
- `TOP_TIER true/false`.

Technical correctness must not raise aesthetic score.

## Pass rule

Support the role-anchor hypothesis only if BOTH treatment outputs, before unblinding:

1. materially improve reference-family structural fidelity over matched control;
2. visibly preserve at least two source-family structures absent from control;
3. reduce the common `brush headline + plated food` template;
4. improve reference-distance judgment;
5. preserve or improve material realism.

If only one style improves: `PARTIAL_SUPPORT`.

If neither improves: `HYPOTHESIS_REJECTED`; the next investigation must move to compiler discriminative-feature selection / common-mode semantic prior, not add more anchors.

## Prohibited

Do not:

- modify V2 compiler code;
- rewrite capsule causal priorities;
- add new aesthetic rules;
- change the headline;
- change content assets;
- run content-swap tests;
- do Figma lettering repair;
- run Library Scale Gate;
- bulk-import library images;
- declare production readiness.

## Final return

Return exactly:

# VPD V2 ROLE-ANCHOR ABLATION READY FOR BLIND REVIEW

Branch:
HEAD:
Reference A crops:
Reference B crops:
Outputs generated:
Hidden outputs:
Technical retries:
Drive folder:
Blind labels:
Mapping private:
Compiler changed:
Scale Gate executed:

## 已完成什么

## 未完成什么

## 需要人工验收什么

Then STOP.
