# VPD V2 Role-Anchor Ablation — Unblind Mapping Only

Status: `FROZEN_MAPPING_DISCLOSURE_TASK`

Repository: `vubaoha034-hash/shenmei`

Required branch: `visual-program-distillation-v2-photography-design-20260814`

## Purpose

Reveal only the private Control/Treatment mapping for the four already-generated anonymous Role-Specific Visual Anchor Ablation outputs.

This task MUST NOT perform aesthetic evaluation, causal diagnosis, prompt changes, renderer changes, new generation, or Library Scale Gate work.

The human blind review is already frozen in a separate independent context. The frozen facts available to the project are:

- `VPD2-RA-2F55A7` belongs to Reference 05 family.
- `VPD2-RA-4435C4` belongs to Reference 05 family.
- `VPD2-RA-8AAB9A` belongs to Reference 13 family.
- `VPD2-RA-971CB0` belongs to Reference 13 family.
- all four were judged `UNUSABLE` on the project's absolute aesthetic scale.
- all four were judged `top_tier = false`.
- `BLIND_REVIEW_FROZEN = YES`.

Do not alter those human judgments.

## Required mapping targets

The exact four frozen experimental conditions are:

- `A_CONTROL_FULL_REFERENCE_ONLY`
- `A_TREATMENT_FULL_PLUS_ROLE_ANCHORS`
- `B_CONTROL_FULL_REFERENCE_ONLY`
- `B_TREATMENT_FULL_PLUS_ROLE_ANCHORS`

Resolve each to exactly one of:

- `VPD2-RA-2F55A7`
- `VPD2-RA-4435C4`
- `VPD2-RA-8AAB9A`
- `VPD2-RA-971CB0`

Use the private mapping ledger / generation receipts created during the frozen Role-Specific Visual Anchor Ablation run. Do not infer from image appearance.

## Integrity checks

Before disclosure verify:

- exactly four valid primary outputs existed;
- hidden outputs = 0;
- best-of-N = 0;
- technical retries = 0;
- compiler changed = NO;
- Scale Gate executed = NO;
- each anonymous output appears exactly once in the private mapping;
- each experimental condition appears exactly once.

If any integrity condition fails, return `VPD_V2_ROLE_ANCHOR_MAPPING_INTEGRITY_FAILURE` and STOP.

## Prohibited actions

Do NOT:

- generate or edit images;
- score the images;
- reinterpret the frozen blind review;
- compare which output looks better;
- diagnose why a condition succeeded or failed;
- modify the compiler, capsule, prompt, reference crops, or hard avoids;
- create a next experiment;
- execute Library Scale Gate;
- change Discovery.

## Output

Create exactly one repository file:

`VPD_V2_ROLE_ANCHOR_UNBLIND_MAPPING.json`

with this structure:

```json
{
  "experiment": "ROLE_SPECIFIC_VISUAL_ANCHOR_ABLATION",
  "mapping_integrity": "PASS",
  "conditions": {
    "A_CONTROL_FULL_REFERENCE_ONLY": "...",
    "A_TREATMENT_FULL_PLUS_ROLE_ANCHORS": "...",
    "B_CONTROL_FULL_REFERENCE_ONLY": "...",
    "B_TREATMENT_FULL_PLUS_ROLE_ANCHORS": "..."
  },
  "hidden_outputs": 0,
  "best_of_n": 0,
  "technical_retries": 0,
  "compiler_changed": false,
  "scale_gate_executed": false
}
```

Then commit and push it on the required branch.

## Final response

Return only:

# VPD V2 ROLE-ANCHOR MAPPING DISCLOSED

Branch:
HEAD:
Mapping integrity:
A_CONTROL:
A_TREATMENT:
B_CONTROL:
B_TREATMENT:
Human scores changed: NO
New images generated: NO
Compiler changed: NO
Scale Gate executed: NO

Then STOP.
