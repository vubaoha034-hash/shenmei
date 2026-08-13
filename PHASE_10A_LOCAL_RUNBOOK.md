# PHASE 10A — WINDOWS GENERATION CHAIN AUDIT RUNBOOK

Status: `READY_FOR_VERIFIED_WRITER_HOST`
Date: `2026-08-13`

This runbook pauses PHASE 10 Attempt 2 and audits the real generation chain on the verified Windows writer host.

The first half is **no-generation**. Do not generate diagnostic images until the traceability gates pass.

## 1. Checkout

Use the verified local `shenmei` checkout and switch to:

```text
phase-10a-generation-chain-audit-20260813
```

Requirements:

- working tree clean;
- ancestry includes Attempt 2 HEAD `59f60adff1dc47e73f861cef5c1c294f6fbab059`;
- PHASE 8 receipt still PASS for `local-codex-primary`;
- `doctor() == []`;
- Discovery remains PHASE 9 frozen state: 18 approved / 12 rejected and no new Discovery Evidence from blind outputs.

Do not modify `main`.

## 2. Run full tests

Run:

```powershell
python scripts/verify_visual_memory.py
```

Confirm `tests/visual_memory/test_generation_audit.py` is discovered and all tests pass.

If any test fails, stop before further audit work.

## 3. Preserve current pause

Record privately:

```text
PHASE 10 Attempt 1 = INVALID_BLIND_CONTAMINATION
PHASE 10 Attempt 2 = PAUSED_FOR_GENERATION_CHAIN_AUDIT
```

Do not generate any Attempt 2 output during PHASE 10A.

## 4. No-generation audit A — reconstruct prior chain

Inspect the private PHASE 9 / PHASE 10 runtime artifacts and the canonical GenerationRecords.

For at least:

- contaminated P10-01 if its private artifacts still exist;
- one PHASE 9 Personalized winner;
- one PHASE 9 Baseline winner;

reconstruct as much of the exact chain as evidence allows:

```text
task brief
route selected
Skill files read
mandatory rule/config files read
compiler output
ContextPack IDs
resolved exemplar assets
final renderer prompt
renderer/tool/model/ratio/parameters
attached reference images/files
output sample/asset/hash
quality check performed before acceptance
```

Do not fill missing information from memory or inference. Use `UNKNOWN` when evidence is absent.

Write private traces under:

```text
<DATA_ROOT>/pilot/phase10a/traces/
```

Do not commit them.

## 5. No-generation audit B — prove or reject renderer reference binding

For the prior Personalized trace(s), answer each selected positive exemplar separately:

```text
Context selected asset_id?
Canonical AssetRecord SHA known?
Asset resolves now?
Actual bytes/file reference attached to renderer call?
Attachment identity/hash provable?
```

Use `visual_memory.generation_audit.classify_reference_binding()`.

Allowed result:

```text
MULTIMODAL_BOUND
PARTIAL_MULTIMODAL_BOUND
TEXT_ONLY_PERSONALIZATION
UNPROVEN_BINDING
```

### Hard stop

If the best evidence is:

```text
TEXT_ONLY_PERSONALIZATION
```

or

```text
UNPROVEN_BINDING
```

for the Personalized chain, stop the 9-image diagnostic and report:

```text
PHASE 10A = RENDERER_REFERENCE_BRIDGE_MISSING
```

Do not compensate by adding more prose about the reference images.

If only partial binding is proven, report:

```text
PHASE 10A = PARTIAL_RENDERER_REFERENCE_BRIDGE
```

and stop until the binding path is deliberately fixed in a separate implementation step.

## 6. No-generation audit C — route and Skill execution

For each prior trace, verify the selected route against `START_HERE.md`.

Record exact Git blob SHA for every Skill/rule file actually read.

Important checks:

- product/food visual should not silently use a full-brand route;
- packaging/brand-system tasks should not all be collapsed into one generic poster route;
- if a Skill was claimed but there is no evidence it was read, mark it `UNPROVEN`.

If route mismatch is systematic, report:

```text
ROUTING_BOTTLENECK
```

## 7. No-generation audit D — prompt-loss analysis

Capture separately:

```text
Task brief
Compiler output
Final renderer prompt
```

Compare the final renderer prompt against mandatory restaurant rules.

Specifically check whether it preserved or lost:

```text
product realism outranks decoration
no plastic/waxy/rubber food
controlled oil gloss
natural ingredient distribution
physical contact/shadow
steam related to heat source
no default ink/brush/seal shortcut
no template repetition
product-driven visual concept
```

Also flag generic injected clichés that were not required by task/rules, e.g.:

```text
Chinese ink
brush stroke
oriental paper
red seal
premium traditional
Zen leaves
```

If the compiler/final prompt consistently reduces the task into those public clichés, report:

```text
PROMPT_COMPILER_BOTTLENECK
```

## 8. No-generation audit E — quality-gate execution

Existing rules say generation completion is not a pass condition.

For the inspected prior outputs, determine whether product realism/design validation was actually performed before the output became an experimental pair.

If obviously invalid food/template outputs were admitted without a reject step, report:

```text
QUALITY_GATE_BOTTLENECK
```

Do not retroactively regenerate them.

## 9. Pre-diagnostic decision

Before generating the 9 diagnostic images, create a private no-generation audit receipt with:

```text
route_traceable: true/false
skills_traceable: true/false
compiler_output_captured: true/false
final_renderer_prompt_captured: true/false
reference_binding_classification: ...
renderer_identity_captured: true/false
quality_gate_execution_known: true/false
```

### Block diagnostic if

Any of these are false:

```text
route_traceable
skills_traceable
compiler_output_captured
final_renderer_prompt_captured
renderer_identity_captured
```

or if reference binding is `TEXT_ONLY_PERSONALIZATION` / `UNPROVEN_BINDING` / `PARTIAL_MULTIMODAL_BOUND`.

Fix observability/bridge first; do not generate more diagnostic pictures on an unknown chain.

## 10. Only after audit gates pass — lock diagnostic tasks

Read exactly:

`PHASE_10A_DIAGNOSTIC_TASKS.json`

There are exactly three tasks:

```text
P10A-D01 food realism
P10A-D02 brand key visual
P10A-D03 packaging design
```

Do not replace tasks after generation begins.

## 11. Compile three conditions before seeing outputs

For each task prepare and lock all three conditions before any of the three outputs are viewed:

### A — Baseline

Current normal route + current normal Skill/Prompt Compiler, no historical Personal Context.

### B — Personalized

Same normal route + same normal Skill/Prompt Compiler + current bounded restaurant ContextPack.

Personalized must be `MULTIMODAL_BOUND`; actual positive exemplar image attachments must be proven in the trace.

### C — Expert Direct Prompt

Bypass the current restaurant Prompt Compiler for this diagnostic only.

Do not use Personal Context.

Build a compact expert prompt directly from:

- the exact task brief;
- Aesthetic Skill Design Charter high-leverage variables;
- mandatory restaurant product-realism constraints relevant to the task;
- no generic Chinese/ink/brush/Zen cliché unless the task itself demands it.

The Expert Direct prompt must be written and hash-locked before any output for that task is viewed.

It is diagnostic only and does not become a production Skill automatically.

## 12. Matched renderer conditions

For A/B/C within one task keep:

```text
same renderer
same model/version
same ratio
same comparable generation parameters
one output per condition
```

Condition C differs in compiler path by design.

No selective retry, retouch, repair or best-of-N.

A genuine technical renderer failure may invalidate the task; "ugly" is not a technical failure.

## 13. Private generation / blind presentation

Generate all 9 outputs through a non-user-visible boundary.

For each task randomize the three conditions to opaque labels:

```text
X
Y
Z
```

The user sees only:

```text
Task brief
Image X
Image Y
Image Z
```

No condition/prompt/reference information before judgments lock.

## 14. User judgment

For every image independently require:

```text
USABLE
or
UNUSABLE
```

Definition:

- `USABLE`: could plausibly be used in a real project without redesigning the core visual concept.
- `UNUSABLE`: below production floor even if relatively better than another output.

Then ask the user to rank the three outputs for that task:

```text
1st / 2nd / 3rd
```

Do not reveal conditions until all 9 absolute judgments and all three rankings are locked.

## 15. Interpret diagnostic

After unblinding, summarize:

```text
A Baseline usable count
B Personalized usable count
C Expert Direct usable count
rank wins by condition
reference binding classification
route findings
prompt-loss findings
quality-gate findings
```

Interpret cautiously:

- `C >>> B > A` → Prompt Compiler / Skill execution likely bottleneck.
- `B ≈ C >>> A` → Personal Context transmission likely works.
- `A ≈ B ≈ C`, mostly unusable → Renderer/model likely bottleneck.
- `C` usable while A/B unusable → current Skill/Prompt Compiler chain likely blocking quality.

## 16. Stop

After PHASE 10A diagnostic result:

- stop;
- do not resume Attempt 2;
- do not modify production Skills automatically;
- do not expand Discovery;
- do not treat diagnostic outputs/judgments as Discovery preference evidence;
- return the result for architecture/implementation decision.
