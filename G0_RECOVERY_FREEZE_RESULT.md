# G0 — RECOVERY FREEZE RESULT

Status: `PASS / FROZEN_FOR_VALUE_FIRST_RESTART`
Date: `2026-08-13`

## Purpose

Establish one canonical recovery point before any new generation work.

## Preserved as reusable infrastructure

The following remain valid and reusable:

- Architecture V0.1 raw/derived authority boundaries;
- SampleRecord / AssetRecord / EvidenceEvent / GenerationRecord contract;
- stable logical IDs and SHA-256 exact-blob identity;
- private Raw Store and Asset Vault;
- real-host single-writer setup;
- backup/restore workflow;
- append-oriented Evidence history and correction semantics;
- blind-eval quarantine;
- purge/doctor/integrity mechanisms;
- current PHASE 9 restaurant Discovery data and its explicit user evidence.

These are frozen for reuse, not expanded.

## Experiments permanently invalid / quarantined

### PHASE 10 Attempt 1

Status: `PERMANENTLY INVALID_BLIND_CONTAMINATION`

Reason:
- P10-01 output and `baseline` condition label were exposed before user voting.

Rules:
- do not repair in place;
- do not regenerate P10-01 inside Attempt 1;
- do not score Attempt 1;
- do not move its outputs/reactions into Discovery;
- keep all related artifacts in blind/evaluation quarantine.

## Experiments paused

### PHASE 10 Attempt 2

Status: `PAUSED_FOR_GENERATION_CHAIN_AUDIT`

Reason:
- absolute visual quality floor has not been demonstrated;
- actual reference-pixel binding into the renderer is not yet proven;
- continuing a 20-pair replication would risk measuring relative preference among unusable outputs.

Attempt 2 cannot resume until G4 absolute quality floor passes.

## Frozen personal evidence state

Restaurant Discovery remains at the current PHASE 9 frozen state:

```text
approved = 18
rejected = 12
domain = 餐饮
positive context max = 4
negative context max = 2
```

No new approved/rejected images or Discovery feedback may be added before G4 unless a data-integrity correction is required; such a correction must be documented and may require re-freezing the relevant experiment.

## Disallowed work during G0–G4

- bulk image ingestion;
- embeddings/vector DB;
- new visual domains;
- large blind replication;
- new mega visual Skill;
- broad aesthetic-rule expansion;
- automated Skill promotion from taste feedback;
- infrastructure work not required to prove the generation chain.

## Known critical state at freeze

```text
Raw evidence persistence = PROVEN
Asset identity / backup / restore = PROVEN
Blind quarantine = PROVEN
Restaurant domain retrieval = PROVEN_BUT_COARSE
Reference pixels → renderer = UNPROVEN
Correct route selection = UNPROVEN
Prompt compiler preservation = UNPROVEN
Quality gate execution = UNPROVEN
Renderer production capability = UNPROVEN
Relative personalization benefit = WEAK_EVIDENCE
Absolute production quality = FAILED
```

## Exit gate

G0 passes because:
- one value-first control branch exists;
- current reusable infrastructure is explicitly preserved;
- invalid and paused experiments are explicitly separated;
- Discovery state is frozen;
- scale/automation work is blocked;
- the next work item is the highest-risk unproven chain assumption, not additional infrastructure.

## Next stage

`G1 — End-to-End Generation Trace Proof`

No new design image should be generated merely to start G1.