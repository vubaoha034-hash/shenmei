# PHASE 10A — REPOSITORY-SIDE AUDIT RESULT

Status: `REPO_AUDIT_COMPLETE / REAL_HOST_TRACE_REQUIRED`
Date: `2026-08-13`

## Completed

Repository-side inspection covered:

- frozen architecture and visual-Skill governance;
- `visual_memory/pilot.py` ContextPack construction;
- public `scripts/` and `visual_memory/` generation-related topology;
- root restaurant routing;
- `restaurant-poster-art-director`;
- `restaurant-image-material-director`;
- mandatory restaurant image-generation rules/config;
- PHASE 10 Attempt 2 protocol and execution gates.

PHASE 10 Attempt 2 remains paused.

## Confirmed findings

### 1. Context selection is not renderer binding

Current ContextPack proves that selected assets are resolvable, but it returns IDs/evidence metadata rather than renderer-ready image attachments.

Therefore the current repository implementation cannot, by itself, prove that an approved reference image's pixels are supplied to the renderer.

### 2. Renderer bridge is not repository-owned/auditable

No deterministic renderer orchestration module exists in the public `scripts/` or `visual_memory/` implementation that records the exact mapping from ContextPack + Skill compiler output to a concrete renderer invocation.

The real host/Codex execution layer must be traced directly.

### 3. Existing rules already reject the observed failures

Existing mandatory restaurant rules already reject:

- plastic/waxy/rubber food texture;
- uncontrolled oil/plastic highlights;
- default ink/brush/Eastern cliché shortcuts;
- food/background layer separation;
- template repetition;
- physically implausible steam/contact/material behavior.

Therefore adding more aesthetic rules before tracing execution would violate repository governance.

### 4. Current retrieval is domain-level, not task-aware

The same restaurant ContextPack can be reused across food photography, brand key visual, packaging and store/social tasks. This is confirmed as a Derived Retrieval limitation, but it is not yet authorized for remediation because the renderer bridge and prompt chain have not been proven.

### 5. Prior experiment gate did not prove actual multimodal reference use

Attempt 2 requires matched conditions and a bounded ContextPack, but it did not require per-reference renderer attachment/hash proof. PHASE 10A adds that requirement for diagnosis.

## Repository-side preliminary verdict

```text
GENERATION_CHAIN_OBSERVABILITY = INSUFFICIENT
REFERENCE_PIXEL_TRANSMISSION = UNPROVEN
EXISTING_RULE_COVERAGE = ALREADY_SUFFICIENT_TO_REJECT OBSERVED FAILURES
ATTEMPT_2 = PAUSED
```

This is not yet a final claim that the renderer bridge is absent. A host-level orchestration step may have attached images outside repository code. The real writer-host trace must determine whether the correct classification is:

```text
MULTIMODAL_BOUND
PARTIAL_MULTIMODAL_BOUND
TEXT_ONLY_PERSONALIZATION
UNPROVEN_BINDING
```

## Verification of new audit helper

The new binding-classification/trace semantics were independently exercised with eight synthetic checks covering:

- no attachment → text-only;
- complete exact-hash attachment → multimodal bound;
- partial attachment;
- mismatched hash → unproven;
- missing compiler output rejection;
- missing Skill evidence rejection;
- valid trace acceptance;
- stable SHA-256 trace hashing.

Result: `8 / 8 PASS`.

Full repository test execution remains required on `local-codex-primary` because the current cloud execution sandbox cannot reach GitHub to clone the branch.

## Next required action

Run `PHASE_10A_LOCAL_RUNBOOK.md` on the verified Windows writer host.

The run must stop **before new image generation** if actual renderer binding, route, prompt or renderer identity cannot be reconstructed/proven.

Only after all no-generation trace gates pass may the 3-task × 3-condition absolute-quality diagnostic run.
