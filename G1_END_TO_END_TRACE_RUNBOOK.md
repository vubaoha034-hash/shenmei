# G1 — END-TO-END GENERATION TRACE RUNBOOK

Status: `READY_FOR_REAL_HOST_AUDIT / NO_NEW_DESIGN_GENERATION`
Date: `2026-08-13`

## Goal

Prove what actually happened in the generation chain before spending any more image-generation budget.

G1 is not a visual-style improvement stage. It is an observability and truth stage.

---

## 1. Preconditions

Use the value-first control branch:

```text
value-first-roadmap-v2-20260813
```

Required state:

```text
G0 = PASS
PHASE 10 Attempt 1 = permanently INVALID
PHASE 10 Attempt 2 = PAUSED
restaurant Discovery = frozen at PHASE 9 state
Google Drive single-image pixel review bridge = PASS
```

No new Discovery evidence may be added.

No new diagnostic images may be generated during the primary G1 audit.

---

## 2. Existing traces to reconstruct

Reconstruct at least three existing executions from private receipts/artifacts when available:

1. PHASE 10 Attempt 1 contaminated `P10-01` execution;
2. one PHASE 9 Personalized winner;
3. one PHASE 9 Baseline winner.

If exact artifacts for an execution do not exist, mark fields `UNKNOWN` rather than inventing them.

---

## 3. Required trace fields

For each execution record:

```text
run_id
task_id
task_brief
route_selected
route_reason
skill_files_actually_read
skill_blob_sha
mandatory_rule_files_actually_read
compiler_input
compiler_output
context_pack
positive_exemplar_ids
negative_exemplar_ids
resolved_reference_files
canonical_reference_sha256
final_renderer_prompt
renderer_tool
renderer_model
renderer_model_version
aspect_ratio
parameters
actual_renderer_attachments
attachment_identity_or_sha
output_sample_id
output_asset_id
output_sha256
quality_gates_defined
quality_gates_executed
quality_gate_results
```

Every field must be supported by an actual artifact/receipt/log or be `UNKNOWN`.

---

## 4. Reference binding proof

For each Personalized execution and every selected positive exemplar, verify all of:

```text
ContextPack selected asset
→ canonical AssetRecord exists
→ asset resolves to exact file
→ canonical SHA-256 known
→ renderer invocation includes actual image/file attachment
→ attachment identity can be matched to canonical asset
```

Classify the execution exactly:

```text
MULTIMODAL_BOUND
PARTIAL_MULTIMODAL_BOUND
TEXT_ONLY_PERSONALIZATION
UNPROVEN_BINDING
```

Only `MULTIMODAL_BOUND` passes the reference-binding gate.

A sample ID, asset ID, filename, text description, or resolvable path alone does not prove multimodal binding.

---

## 5. Routing audit

Compare the actual execution with `START_HERE.md` and relevant scope boundaries.

Check whether heterogeneous restaurant tasks were routed appropriately, especially:

- food/product realism;
- single key visual/poster;
- packaging/layout;
- store/social visual.

Record:

```text
ROUTE_CORRECT
ROUTE_INCORRECT
ROUTE_UNPROVEN
```

Do not change routing during G1.

---

## 6. Prompt compiler audit

Preserve separately:

```text
Task brief
Compiler output
Final renderer prompt
```

Check whether the final prompt preserved the highest-value constraints actually required by the selected Skill, including when applicable:

- product realism outranks decoration;
- no plastic/waxy/rubber food texture;
- controlled oil gloss;
- natural ingredient distribution;
- physically plausible contact/shadow;
- heat-related steam;
- product-driven visual logic;
- no default ink/brush/red-seal shortcut;
- no template/color-swap repetition.

Also detect whether host orchestration inserted unsupported generic cliché terms.

Record:

```text
PROMPT_PRESERVED
PROMPT_LOSS_DETECTED
PROMPT_UNPROVEN
```

Do not repair the prompt during G1.

---

## 7. Quality-gate execution audit

For each hard correctness/realism gate, record independently:

```text
DEFINED
EXECUTED
RESULT
```

A Markdown rule existing in the repository does not count as executed.

For obviously weak historical outputs, determine whether:

- gate executed and incorrectly passed;
- gate executed and failed but output still advanced;
- gate never executed;
- execution cannot be proven.

Record one of:

```text
QUALITY_GATE_EXECUTED_CORRECTLY
QUALITY_GATE_FALSE_PASS
QUALITY_GATE_BYPASSED
QUALITY_GATE_UNPROVEN
```

---

## 8. Renderer identity audit

Capture actual:

- renderer/tool;
- model;
- model version when available;
- ratio;
- generation parameters;
- reference attachment list.

If the renderer identity or final invocation cannot be reconstructed, G1 cannot pass.

---

## 9. External pixel-review bridge

Do not use Drive to generate or modify images.

Google Drive is only an approved transport for independent pixel review.

Known proof:

```text
LIU_VISUAL_REVIEW/G1/
LIU_G1_DRIVE_PROBE_001.png
```

The single-image review path passed.

Future assets must preserve real MIME/extension consistency; do not store HEIF bytes under `.png` names.

---

## 10. G1 exit decision

Possible G1 results:

```text
G1_PASS
G1_BLOCKED_REFERENCE_BINDING
G1_BLOCKED_ROUTING
G1_BLOCKED_PROMPT_TRACE
G1_BLOCKED_RENDERER_TRACE
G1_BLOCKED_QUALITY_GATE
G1_MULTIPLE_BLOCKERS
```

`G1_PASS` requires all of:

- at least three historical traces reconstructed sufficiently;
- route known for each trace;
- Skill/rule reads known;
- compiler output captured;
- final renderer prompt captured;
- renderer identity captured;
- Personalized reference binding = `MULTIMODAL_BOUND`;
- quality-gate execution state known;
- no fabricated/assumed trace fields.

If any critical requirement is unknown, do not call G1 PASS.

---

## 11. What G1 does NOT prove

Even `G1_PASS` does not prove:

- images are beautiful;
- renderer is good enough;
- Personalized is better;
- current Prompt Compiler is optimal;
- G4 production floor passes.

It only proves we can trust the execution trace enough to run the next smallest experiment.

---

## 12. Next-stage rule

If G1 finds a proven bridge/trace defect:

```text
→ G2 Minimal Bridge / Observability Repair
```

If G1 passes without requiring repair:

```text
→ G3 3×3 Capability Diagnostic
```

Do not skip directly to G4/G5/G6.

---

## Required report

Every G1 result must report:

### 已完成什么
### 未完成什么
### Three trace IDs
### Reference binding classification
### Routing result
### Prompt compiler result
### Renderer trace result
### Quality-gate result
### New design images generated
### Drive review bridge state
### G1 decision
### Why the next step is justified
### What remains reusable if the next step fails
