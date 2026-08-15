# VPD V2 — Contrastive Signature Selection Ablation — Replacement R1

Status: `FROZEN_REPLACEMENT_AFTER_TECHNICAL_INVALIDATION`

Repository: `vubaoha034-hash/shenmei`
Required branch: `visual-program-distillation-v2-photography-design-20260814`

## Purpose

Repeat the Contrastive Signature Selection Ablation after Attempt 1 was invalidated only for renderer geometry failure.

The causal hypothesis is unchanged:

`DISCRIMINATIVE_FEATURE_SELECTION_FAILURE`

Do not reinterpret or modify the hypothesis before this replacement completes.

## Mandatory reads

Read completely:

- `VPD_V2_CONTRASTIVE_SIGNATURE_ATTEMPT1_TECHNICAL_INVALIDATION.md`
- `VPD_V2_CONTRASTIVE_SIGNATURE_ABLATION_TASK.md`
- `VPD_V2_ROLE_ANCHOR_ABLATION_RESULT.json`
- `VPD_V2_CALIBRATED_ABSOLUTE_UNBLIND_RESULT.json`
- `VPD_V2_TEMPLATE_COLLAPSE_ROOT_CAUSE.md`
- `VPD_V2_EVALUATION_RUBRIC_CALIBRATION_V2.md`

## Phase 0 — quarantine Attempt 1

Treat all Attempt-1 outputs and receipts as technical-failure evidence only.

They must not be reviewed, ranked, reused, or mixed into Replacement R1.

Record their hashes/paths in a private quarantine receipt.

## Phase 1 — renderer geometry preflight

Before generating any Replacement-R1 benchmark output, establish what output geometry the current creative renderer can actually guarantee.

Priority order:

1. inspect the renderer/tool schema or documented capability metadata without image generation;
2. if a fixed supported portrait size/aspect is explicitly exposed, select one fixed portrait geometry for the whole replacement run;
3. if exact output dimensions are not contractually exposed, perform at most `2` technical geometry probes, both quarantined and never eligible for aesthetic review.

The preflight is not an aesthetic optimization and may not compare styles.

### Geometry contract requirements

Freeze exactly one `RENDERER_NATIVE_GEOMETRY_CONTRACT` before benchmark generation.

It must specify either:

- exact native width × height that the renderer contract guarantees; or
- one native portrait aspect class plus an explicit allowable aspect-ratio tolerance if exact pixel dimensions are not guaranteed.

Do not continue if the tool cannot establish a stable shared portrait geometry contract.
Return:

`VPD_V2_CONTRASTIVE_REPLACEMENT_BLOCKED_GEOMETRY`

and STOP.

### Critical correction

Do not keep demanding an arbitrary legacy 4:5 pixel size if the current renderer cannot guarantee it.

The experiment requires Control and Treatment comparability; it does not require a technically impossible size.

Any replacement geometry change must apply identically to all four conditions.

## Phase 2 — freeze all non-causal variables

After geometry preflight, freeze for all four conditions:

- same canonical Reference 05 / Reference 13 raw pixels as before;
- same reconstruction content assets as Attempt 1;
- same target headline;
- same strongest available creative visual model/tool;
- same one-attempt policy;
- same content facts;
- same reference-binding policy;
- no role-specific crops;
- no global compiler modification;
- same technical integrity rules;
- same newly frozen renderer-native geometry contract.

The ONLY experimental variable remains:

`CURRENT_COMPILER` vs `CONTRASTIVE_SIGNATURE_SELECTOR_V0`.

## Phase 3 — generate a complete fresh replacement

Generate exactly four fresh primary outputs:

1. `A_CONTROL_CURRENT_COMPILER_R1`
2. `A_TREATMENT_CONTRASTIVE_SIGNATURE_R1`
3. `B_CONTROL_CURRENT_COMPILER_R1`
4. `B_TREATMENT_CONTRASTIVE_SIGNATURE_R1`

Rules:

- no reuse of Attempt-1 images;
- hidden outputs = 0;
- best-of-N = 0;
- no cosmetic retry;
- no manual image repair;
- no Figma/vector cleanup;
- no post-generation crop that changes composition;
- no aesthetic post-processing.

A deterministic invalid-byte/tool transport failure may be retried once only if quarantined and logged.

A geometry-contract mismatch is NOT retryable. Stop immediately and report technical failure instead of repeating the same request.

## Phase 4 — integrity and blind package

All four outputs must satisfy the same frozen geometry contract.

Verify:

- image readable;
- expected MIME;
- no catastrophic truncation;
- geometry contract PASS;
- output hashes recorded;
- exactly four fresh primary outputs.

Then upload only the four valid Replacement-R1 primaries to a new Drive folder:

`LIU_VISUAL_REVIEW/VPD_V2_CONTRASTIVE_SIGNATURE_REPLACEMENT_R1`

Use new neutral random blind labels unrelated to A/B or Control/Treatment.

Keep mapping private.

Do not upload Attempt-1 images into this review folder.

## Phase 5 — stop for independent blind review

Do not judge aesthetic quality.
Do not unblind.
Do not claim success.
Do not modify the global compiler.
Do not run Library Scale Gate.
Do not change Discovery.

Final status only:

`VPD_V2_CONTRASTIVE_REPLACEMENT_R1_READY_FOR_BLIND_REVIEW`

or a strict technical blocker/failure.

## Final response

Return:

# VPD V2 CONTRASTIVE SIGNATURE REPLACEMENT R1 READY FOR BLIND REVIEW

Branch:
HEAD:
Attempt 1 quarantined:
Geometry preflight method:
Frozen native geometry contract:
Technical geometry probes:
Outputs generated:
Hidden outputs:
Technical retries:
Drive folder:
Blind labels:
Mapping private:
Global compiler changed:
Reference crops used:
Scale Gate executed:

## 已完成什么

## 未完成什么

## 需要人工验收什么

Then STOP.
