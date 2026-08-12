# LIU VISUAL SYSTEM — PHASE 9 LOCAL PILOT RUNBOOK

Status: `READY_FOR_CODEX_EXECUTION`
Date: `2026-08-12`
Writer host: Windows / `local-codex-primary`

This runbook starts the first real personal Pilot. It must not bulk-ingest the user's full visual archive.

## 1. Fixed operational environment

Verified PHASE 8 host:

```text
Repository checkout:
C:\Users\Administrator\source\repos\shenmei

Private DATA_ROOT:
E:\LIU_VISUAL_SYSTEM\private-data

BACKUP_DIR:
F:\LIU_VISUAL_SYSTEM_BACKUP

Writer:
local-codex-primary
```

Before any real ingestion, verify the PHASE 8 private receipt still says PASS and the worktree is clean.

PHASE 9 code baseline is the branch:

```text
phase-9-small-personal-pilot-20260812
```

which was created from verified Windows PHASE 8 HEAD:

```text
b74117f678a4ad9cfc3e664ae44606a6b10e0b29
```

---

## 2. Do not crawl the machine automatically

Do not recursively ingest Desktop/Pictures/drives or attempt to infer taste from the user's entire photo library.

The user must deliberately choose the small Pilot input set.

Codex may help list/copy candidate files from a directory the user explicitly selects, but it must not silently expand scope to unrelated folders.

---

## 3. First Pilot target

Discovery target:

```text
20–40 explicit approved/liked visual samples
10–20 explicit rejected visual samples
```

Optional neutral/reference-only samples may be stored, but they are not treated as positive preference unless explicitly approved.

Use at least 2–3 real task/domain families if available.

Do not exceed roughly 60 discovery samples for the first Pilot.

---

## 4. Evidence capture rule

The user does not need to describe every image separately.

A deliberate batch statement is allowed when it is true for the whole selected batch.

Examples:

```text
“这一批我都明确喜欢，作为这个视觉方向的正面参考。”
“这一批我明确不喜欢，作为这个视觉方向的反例。”
```

The exact wording the user gives must be preserved in `EvidenceEvent.raw_text`.

Do not replace it with an assistant summary.

For domain-scoped batches, record the domain as a free-form label only when the current task/domain is objectively clear.

If scope is uncertain, use `unspecified`; do not invent global preference.

---

## 5. Safe ingestion procedure

For every selected source file:

1. call `visual_memory.pilot.ingest_visual_file`;
2. confirm exact SHA-256 is not already present;
3. copy bytes into the private Asset Vault;
4. create SampleRecord + AssetRecord;
5. verify asset resolves from the private store;
6. do **not** create preference evidence from ingestion alone.

After a whole user-confirmed batch is ingested successfully:

- call `record_batch_feedback` once with the exact user statement;
- use `approved`, `rejected`, or `neutral` as explicitly appropriate;
- do not label blind material through this discovery path.

After each batch:

```text
doctor() == []
```

must hold.

---

## 6. First real checkpoint backup

After the first real discovery dataset is complete and `doctor()` passes:

1. create a new backup under `F:\LIU_VISUAL_SYSTEM_BACKUP`;
2. do not overwrite the PHASE 8 preflight backup;
3. restore into a separate audit directory;
4. open the restored store;
5. confirm IDs, hashes, evidence and asset resolution;
6. remove only the temporary restored audit copy after PASS.

The canonical real DATA_ROOT remains intact.

---

## 7. Build first ContextPack

Use `visual_memory.pilot.build_context_pack`.

No embeddings/vector DB.

For each representative domain/task:

- select max 4 positive exemplars;
- select max 2 negative exemplars;
- only use matching `domain` evidence + `global_explicit` evidence;
- ignore `unspecified` evidence for cross-task retrieval;
- skip any asset that cannot actually resolve.

Store generated ContextPack only as derived/private state.

Do not place private context in public Git.

---

## 8. Retrieval sanity gate

Before image-generation A/B tests, inspect several ContextPacks.

For each representative task ask:

```text
Are these selected positive examples actually relevant?
Are these selected negative examples useful as anti-examples?
Did anything from another domain leak in?
```

If retrieval is obviously wrong, stop and repair retrieval selection.

Do not compensate by adding more images.

---

## 9. Blind generation experiment

Minimum:

```text
10 valid Baseline vs Personalized pairs
```

Use multiple real visual task families.

For each pair:

### Baseline

Existing route/Skill + current explicit task only.

### Personalized

Same route/Skill + same current task + bounded ContextPack.

Keep renderer/model/settings as close as practical.

Before user judgment:

- randomize which condition is shown as A/B;
- hide condition identity;
- never use filenames that expose baseline/personalized;
- lock user choice before unblinding.

Choices:

```text
A
B
tie
```

After lock, use `blind_pair_result` to convert the decision into baseline/personalized/tie.

All blind outputs/evidence must stay quarantined from discovery under the frozen blind-eval policy.

---

## 10. Pilot score

Use `summarize_blind_results` after at least 10 valid pairs.

Possible results:

```text
PASS_TO_EXPAND
INCONCLUSIVE
FAIL_REWORK
```

`PASS_TO_EXPAND` requires:

- >= 10 valid pairs;
- personalized >= 60% of non-tie wins;
- personalized has at least 2 more wins than baseline;
- no current-instruction override;
- no cross-domain contamination;
- no blind-eval leakage;
- no private Git leakage.

The numeric rule is a Pilot decision gate, not a permanent architecture invariant.

---

## 11. Additional observations

Record separately as evaluation/telemetry, not raw personal truth:

- revision rounds;
- first-generation explicit acceptance;
- exemplar relevance;
- recurrence of known rejected mechanisms;
- asset-resolution failures;
- context assembly failures.

Silence is not acceptance.

---

## 12. End-of-Pilot audit

Before declaring PHASE 9 result:

```text
[ ] doctor PASS
[ ] real data backup PASS
[ ] Git worktree contains no private data
[ ] public calibration/anchors.json contains no private Pilot data
[ ] blind-eval quarantine PASS
[ ] no new visual Skill was created merely to improve the score
[ ] no critic/router modification was used to bias one condition
[ ] scorecard has >=10 locked valid blind pairs
```

Final result must be exactly one of:

```text
PHASE 9 = PASS_TO_EXPAND
PHASE 9 = INCONCLUSIVE
PHASE 9 = FAIL_REWORK
```

Do not bulk ingest more data automatically after PASS. Stop and report first.
