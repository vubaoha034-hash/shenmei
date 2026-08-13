# LIU VISUAL SYSTEM — PHASE 10A GENERATION CHAIN AUDIT

Status: `AUDIT_IN_PROGRESS / ATTEMPT_2_PAUSED`
Date: `2026-08-13`
Branch: `phase-10a-generation-chain-audit-20260813`
Base: PHASE 10 Attempt 2 HEAD `59f60adff1dc47e73f861cef5c1c294f6fbab059`

## 0. Why PHASE 10A exists

PHASE 10 Attempt 2 is paused before execution because the user inspected recent restaurant generations and reported an absolute-quality failure: food looks visibly synthetic and the design language is far below the approved references.

The immediate question is no longer whether Personalized beats Baseline relatively. The question is whether the generation chain can faithfully transmit approved visual evidence and existing restaurant-generation rules into the renderer at all.

This phase audits the chain before any further replication run.

## 1. Hard boundaries

PHASE 10A does **not**:

- add new approved/rejected Discovery samples;
- append new Discovery preference Evidence from PHASE 10 blind outputs;
- modify Router, existing visual Skills, critic, or frozen architecture;
- start PHASE 10 Attempt 2 generation;
- import embeddings/vector DB/model training;
- treat the user's reaction to contaminated/blind outputs as Discovery truth.

Attempt 1 and Attempt 2 remain quarantined/evaluation-only while this audit runs.

## 2. Initial repository findings

### F10A-01 — ContextPack resolves assets but discards the visual payload

`visual_memory/pilot.py::build_context_pack()` verifies that an exemplar asset resolves, but the returned item contains only:

```text
sample_id
asset_id
evidence_ids
raw_text
resolvable
```

It does **not** include:

```text
resolved asset path
image bytes / connector file reference
pixel dimensions
visual feature representation
renderer-ready reference binding
```

Therefore `build_context_pack()` by itself cannot prove that the renderer ever receives the approved image pixels.

Verdict: `HIGH-RISK GAP / MUST TRACE ON REAL HOST`.

### F10A-02 — No repository-owned renderer bridge is present

The public `scripts/` and `visual_memory/` packages contain persistence, evidence replay, operational safeguards and pilot helpers, but no deterministic program that maps:

```text
Task
+ selected Skill
+ VisualContextPack
+ resolved exemplar bytes
→ renderer invocation payload
```

Generation appears to depend on host/Codex orchestration outside the audited repository code.

Consequences:

- it is currently impossible from Git alone to prove which Skill instructions reached the renderer;
- it is impossible from Git alone to prove whether approved images were passed as multimodal references;
- it is impossible from Git alone to reproduce the exact final prompt/payload used for one generated image.

Verdict: `CRITICAL OBSERVABILITY GAP`.

### F10A-03 — Output failures contradict existing mandatory restaurant rules

Existing restaurant generation rules already reject or discourage the same mechanisms visible in failed outputs:

- plastic/waxy/rubber food texture;
- fake or overly uniform gloss;
- default ink/brush/Eastern clichés;
- decorative smoke detached from product logic;
- template reuse;
- food/background appearing as separate layers;
- excessive HDR/plastic highlights.

`restaurant-poster-art-director` explicitly states that generation completion is not a pass condition and that product realism outranks decoration.

The observed outputs nevertheless repeatedly show generic brush fields, large decorative empty areas and synthetic food rendering.

Possible explanations to distinguish:

1. mandatory Skill/rule files were not actually read for that task;
2. they were read but not compiled into high-leverage renderer instructions;
3. the final prompt became too generic/verbose/conflicted and collapsed to common restaurant clichés;
4. the renderer received the prompt but not approved image references;
5. the renderer received references but they were too weakly bound;
6. outputs that should have been rejected were accepted into the experiment without an absolute-quality gate.

Verdict: `CHAIN EXECUTION / QUALITY-GATE FAILURE LIKELY`.

### F10A-04 — Domain-only retrieval is too coarse for the test task mix

Current retrieval matches the broad domain `餐饮` plus explicit global evidence. It does not rank exemplars by task type such as:

```text
brand key visual
food photography
promotion poster
menu / packaging
store / social system
```

A packaging task can therefore receive the same 4 positive / 2 negative exemplars as a food-photography task.

This is not a Raw Data defect. It is a Derived Retrieval limitation.

Verdict: `CONFIRMED LIMITATION / DO NOT FIX UNTIL CHAIN AUDIT COMPLETES`.

### F10A-05 — Route mismatch is plausible and must be traced

`START_HERE.md` distinguishes restaurant routes:

- complete restaurant brand case;
- single poster / product visual;
- editable Figma brand system.

PHASE 10 task families include brand key visuals, promotion posters, food-product visuals, menu/packaging and store/social work. A single generic route across all of them would be incorrect.

The public repo contains no deterministic per-task route receipt for the prior generations.

Verdict: `MUST TRACE ON REAL HOST`.

## 3. Audit questions that must be answered with evidence

For at least three representative prior/diagnostic tasks, capture the exact chain:

```text
1. user/task brief
2. route selected
3. exact Skill files read
4. prompt-compiler output before personalization
5. ContextPack selected exemplar IDs
6. actual resolved exemplar files
7. whether those image bytes/file references were attached to renderer call
8. negative/rejected exemplar handling
9. final renderer prompt/payload
10. renderer/model/version/ratio/parameters
11. raw output
12. pre-delivery quality-gate result
```

Every claim must be backed by a private trace artifact on the writer host. "The model had access" is not enough.

## 4. Critical gate — actual-reference proof

For a Personalized condition to count as genuinely multimodal personalization, the audit must prove:

```text
selected approved sample
→ resolved exact AssetRecord bytes
→ explicit renderer input attachment/reference
→ renderer invocation receipt or local trace proving the attachment
```

If the chain stops at `sample_id`, `asset_id`, `raw_text`, prose summary, or filename text, classify the current Personalized implementation as:

```text
TEXT_ONLY_PERSONALIZATION
```

and stop PHASE 10 replication until the renderer bridge is corrected.

## 5. Absolute quality diagnostic

After the no-generation trace audit is complete, and only if a renderer path can be instrumented, run exactly three representative restaurant tasks through three conditions:

```text
A — current Baseline
B — current Personalized
C — Expert Direct Prompt (bypasses current restaurant prompt compiler, does not use Personal Context)
```

Total: 9 images.

The purpose is diagnostic, not a blind superiority test.

For each image record two independent judgments:

```text
relative preference within the three-condition set
absolute production floor: USABLE / UNUSABLE
```

Interpretation:

- `C >>> B > A`: Prompt Compiler / Skill execution is the likely bottleneck.
- `B ≈ C >>> A`: Personal Context transmission is working.
- `A ≈ B ≈ C` and all unusable: renderer/model is the likely bottleneck.
- `C` usable while `A/B` unusable: current Skill/Prompt Compiler chain is blocking quality.

No result from these 9 images enters Discovery Evidence automatically.

## 6. Absolute-quality floor

Pairwise wins are no longer sufficient evidence of system success.

Every future replication pair must additionally distinguish:

```text
winner = A/B/tie
A absolute quality = USABLE/UNUSABLE
B absolute quality = USABLE/UNUSABLE
```

A Personalized pairwise win where both outputs are `UNUSABLE` is recorded as:

```text
RELATIVE_WIN / BELOW_PRODUCTION_FLOOR
```

It must not be used to claim production readiness.

## 7. PHASE 10A exit conditions

PHASE 10A cannot pass until all are answered:

```text
[ ] Exact route per diagnostic task is known.
[ ] Exact Skill files actually read are known.
[ ] Exact compiled prompt before renderer is captured.
[ ] Selected positive/negative exemplar IDs are captured.
[ ] Actual resolved positive reference image bytes are accounted for.
[ ] Renderer invocation proves whether images were attached.
[ ] Renderer/model/version/settings are captured.
[ ] Existing mandatory restaurant rules are checked against final prompt.
[ ] Pre-delivery reject logic is inspected.
[ ] Three-condition 9-image diagnostic is run only after traceability exists.
[ ] Absolute USABLE/UNUSABLE judgments are collected.
```

Possible verdicts:

```text
RENDERER_REFERENCE_BRIDGE_MISSING
PROMPT_COMPILER_BOTTLENECK
ROUTING_BOTTLENECK
QUALITY_GATE_BOTTLENECK
RENDERER_BOTTLENECK
MULTIPLE_BOTTLENECKS
CHAIN_AUDIT_PASS
```

Do not resume PHASE 10 Attempt 2 merely because one small fix appears plausible.
