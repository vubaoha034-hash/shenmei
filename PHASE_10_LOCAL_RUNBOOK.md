# LIU VISUAL SYSTEM — PHASE 10 LOCAL REPLICATION RUNBOOK

Status: `READY_TO_RUN_ON_VERIFIED_WRITER_HOST`
Date: `2026-08-13`

This runbook executes PHASE 10 on the already verified private Windows writer host. It does not authorize evidence expansion.

## 1. Checkout and ancestry

Use the existing local `shenmei` checkout.

Fetch the remote branch and switch to:

```text
phase-10-frozen-context-replication-20260813
```

Requirements:

- working tree clean;
- branch contains PHASE 9 code HEAD `0a9785ee0336b6697a9e9250af8e3751697a6e0e` as ancestor;
- PHASE 8 real-host receipt still says PASS for `local-codex-primary`;
- `VisualMemoryStore.doctor()` returns `[]` before replication starts.

Do not modify `main`.

---

## 2. Run all tests before touching the replication state

Run:

```powershell
python scripts/verify_visual_memory.py
```

Requirements:

- all existing PHASE 7/8/9 tests PASS;
- `tests/visual_memory/test_replication.py` is actually discovered;
- all 10 PHASE 10 replication tests PASS;
- Python compile check PASS.

If any test fails, stop before creating blind outputs.

---

## 3. Verify the PHASE 9 canonical state

Before freezing PHASE 10:

- real discovery library must still be the PHASE 9 final library;
- do not import new approved/rejected images;
- do not append new discovery feedback;
- no PHASE 9/10 blind case may appear in discovery evidence;
- public `calibration/anchors.json` must remain unchanged;
- no private data may appear in Git status.

If the canonical discovery state has already changed since PHASE 9, stop and report `BLOCKED_STATE_DRIFT`; do not silently redefine the replication baseline.

---

## 4. Create the private frozen replication snapshot

Using the canonical private store and:

```python
from visual_memory.replication import build_replication_snapshot
```

build:

```text
domain = 餐饮
max_positive = 4
max_negative = 2
```

Write the resulting JSON only inside the private PHASE 10 runtime area, for example:

```text
<PRIVATE_DATA_ROOT>/pilot/phase10/pre_registration.json
```

The private file must contain:

- discovery sample IDs;
- discovery EvidenceEvent IDs;
- frozen ContextPack;
- positive/negative exemplar IDs;
- `state_sha256`.

Record the hash in the private experiment report.

Do not commit the snapshot to Git.

Immediately verify:

```python
verify_replication_snapshot(store, snapshot) == True
```

---

## 5. Lock the 20 pre-registered tasks

Read exactly:

`PHASE_10_REPLICATION_TASKS.json`

Requirements:

- 20 tasks are present;
- task IDs are `P10-01` through `P10-20`;
- no task text is edited after this point;
- compare against the private PHASE 9 blind-task manifest and verify none is an exact reused task;
- if an exact reused task is found, stop before generation and report it; do not invent a replacement after seeing any PHASE 10 output.

Create a private task-lock receipt containing the SHA-256 of the public task JSON and the 20 task IDs.

---

## 6. Pre-generate the hidden A/B mapping

Before any PHASE 10 images are generated:

- create a cryptographically random A/B assignment for all 20 task IDs;
- exactly one condition is Baseline and the other Personalized per task;
- store mapping only in the private blind ledger;
- user-visible files must never reveal the mapping;
- do not modify mappings after outputs are seen.

This prevents presentation assignment from being influenced by image quality.

---

## 7. Generate 20 matched pairs

For each `P10-01` … `P10-20`:

### Baseline

```text
pre-registered task brief
+ existing repository route / selected visual Skill
+ same renderer/model/ratio/parameters
+ no historical Personal Context
```

### Personalized

```text
same pre-registered task brief
+ same repository route / selected visual Skill
+ same renderer/model/ratio/parameters
+ frozen bounded restaurant ContextPack only
```

Hard rules:

- same current-task inputs for both conditions;
- do not add extra creative guidance to Personalized;
- do not weaken Baseline;
- each condition generated once;
- no manual retouch/repair/regeneration after visual inspection;
- genuine renderer failure may invalidate a task but cannot trigger selective creative retry;
- every PHASE 10 output SampleRecord is `blind_eval_reserved`;
- GenerationRecords preserve condition lineage privately;
- PHASE 10 blind outputs/events never enter discovery or `skill-refiner` evidence.

After each pair is created, lock it before moving to the next task.

---

## 8. Verify frozen state before user voting

After all output generation and before presenting A/B:

```python
verify_replication_snapshot(store, snapshot)
```

must still return `True`.

If False:

```text
PHASE 10 = INVALID_STATE_DRIFT
```

Stop. Do not repair state in place and continue voting.

---

## 9. Prepare blind review

For each pair show only:

```text
Task ID
brief
Image A
Image B
```

Do not show:

- Baseline/Personalized labels;
- ContextPack;
- prompt differences;
- hidden file names;
- interim win totals.

Accepted user vote only:

```text
A
B
tie
```

Optional user note may be preserved verbatim.

All 20 votes must be locked before unblinding.

Do not reveal the running score after the first few votes.

---

## 10. Unblind only after all votes are locked

Use the hidden mapping and existing PHASE 9 helper:

```python
blind_pair_result(...)
```

Produce exactly 20 locked condition results if all tasks are valid.

Then use:

```python
from visual_memory.replication import summarize_replication
```

PHASE 9 locked prior is already pre-registered as:

```text
Personalized = 6
Baseline = 4
Tie = 0
```

Provide:

```text
safety_ok = True only if every safety audit is PASS
frozen_state_unchanged = result of snapshot re-verification
```

Do not manually compute a more favorable threshold.

---

## 11. Safety audit before final decision

All must be zero/clean:

- blind contamination;
- current task overridden by historical context;
- cross-domain evidence contamination;
- private Git leakage;
- public calibration mutation;
- discovery/context state drift;
- hidden mapping leak before votes lock;
- selective creative regeneration asymmetry.

Any failure makes the replication `INVALID`.

---

## 12. Final output

Return:

```text
# PHASE 10 FROZEN-CONTEXT REPLICATION RESULT

Branch:
HEAD:
Tests:
Pre-registration snapshot hash:
Frozen state unchanged:
Task count:
Valid pairs:
Phase10 Personalized wins:
Phase10 Baseline wins:
Phase10 ties:
Phase10 Personalized non-tie win rate:
Combined P9+P10 Personalized wins:
Combined P9+P10 Baseline wins:
Combined ties:
Combined Personalized non-tie win rate:
One-sided exact binomial p:
Safety audit:
Backup/restore checkpoint:
Git privacy:
Decision:
```

Decision must be exactly one of:

```text
REPLICATION_PASS
INCONCLUSIVE
NOT_REPLICATED
INVALID
```

Do not call `INCONCLUSIVE` a pass.

---

## 13. Stop rule

After the PHASE 10 result is locked:

- stop;
- do not import more images;
- do not edit retrieval;
- do not modify Skills;
- do not automatically start failure remediation;
- do not begin controlled expansion.

Return the result for independent review first.
