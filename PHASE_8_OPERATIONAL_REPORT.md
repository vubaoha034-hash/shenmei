# LIU VISUAL SYSTEM — PHASE 8 OPERATIONAL PRIVATE ROOT REPORT

Status: `TOOLING_PASS / REAL_HOST_GATE_OPEN`
Date: `2026-08-12`
Branch: `phase-8-operational-private-root-20260812`
Base: PHASE 7 final HEAD `9edfb5f4c6d05aec86fcd28ad38d99da1273858c`

## Purpose

PHASE 8 closes the software-side pre-Pilot operational gates created by the frozen V0.1 architecture without pretending that an ephemeral cloud/chat runtime is the user's durable private writer host.

No real personal visual references, user preference history, or private calibration anchors are imported in this phase.

---

## Implemented operational tooling

### Private operational configuration

Added `visual_memory/operational.py` with:

- explicit private `data_root`;
- separate private `backup_dir`;
- stable `writer_id`;
- optional future private calibration overlay path;
- validation that private paths remain outside the public `shenmei` repository;
- validation that data and backup roots do not contain one another;
- persistent private-root marker that refuses a silent writer identity change.

### Single-writer lease

Added a cross-platform `WriterLease` using atomic exclusive lock-file creation.

Properties:

- a second writer fails closed;
- stale locks are not broken automatically;
- lock ownership includes writer ID, PID, host, and random token;
- release checks the token before deleting the lock.

This implements the V0.1 single-writer policy without a database or distributed lock service.

### Backup / restore hardening

Updated `visual_memory/backup.py` so that:

- backup archives cannot be created inside the data root;
- existing archives are not overwritten silently;
- restore still requires an empty destination.

### Tombstone-gated physical purge

Added `visual_memory/purge.py` and `scripts/visual_memory_purge.py`.

Physical purge requires a prior Tombstone covering every explicitly purged ID.

The minimal purge path:

- removes controlled Asset Vault bytes;
- never deletes arbitrary external source files;
- scrubs sample provenance/source metadata and user tags;
- replaces asset locators with opaque purged locators;
- scrubs prompt/task/parameter execution metadata from affected generations;
- physically removes explicitly tombstoned EvidenceEvents;
- clears rebuildable derived artifacts;
- keeps non-sensitive stable identity skeletons where appropriate.

A dry-run plan is supported.

### Public-Git guardrail

Added `.gitignore` entries for common accidental private-runtime directory/file names.

This is only a secondary guard. Canonical personal data is still required to live outside the public repository.

### Actual-host preflight command

Added `scripts/visual_memory_operational_preflight.py`.

On the eventual durable writer host it will:

1. verify private/backup path separation;
2. initialize the private-root marker;
3. acquire the exclusive WriterLease;
4. rerun the PHASE 7 synthetic verification suite in that host environment;
5. create only synthetic, non-sensitive operational records;
6. perform backup → restore and verify stable IDs/assets/integrity;
7. perform Tombstone-gated physical purge verification;
8. verify the public `calibration/anchors.json` hash did not change;
9. write a private receipt to `<DATA_ROOT>/operations/phase8_preflight.json`.

The receipt may authorize the small Personal Pilot on that writer host only when it records `status=PASS` and `pilot_authorized_on_this_writer_host=true`.

Formal private `personal_fit` remains disabled until a privacy-safe calibration overlay is actually integrated with the existing critic.

---

## Verification performed in this phase

New PHASE 8 operational logic was tested in an isolated non-sensitive temporary environment.

Result:

```text
6 tests run
6 passed
0 failed
```

Covered behavior:

1. private/public/overlapping path guards;
2. exclusive/releasable WriterLease;
3. private-root marker prevents silent writer-ID change;
4. backup rejects archive placement inside the data root;
5. backup rejects silent overwrite of an existing archive;
6. physical purge requires a Tombstone and then scrubs/deletes controlled private payload while preserving valid record structure.

All new PHASE 8 Python files also passed Python bytecode compilation in the isolated verification environment.

---

## Important limitation — real durable host is not this cloud turn

This conversation/runtime is not a trustworthy long-lived private storage host.

Therefore PHASE 8 does **not** claim that the user's actual durable:

- Private Data Root;
- Asset Vault;
- Backup location;
- single writer host;
- backup/restore receipt;
- physical purge receipt;

already exists.

Creating a temporary directory in an ephemeral sandbox and calling it the permanent private memory would be a false PASS.

The real host gate must be closed by running `PHASE_8_LOCAL_RUNBOOK.md` in the durable private environment that will own the first Pilot.

---

## Personal Pilot status

```text
Operational tooling: PASS
Isolated new-logic verification: PASS
Durable private writer-host preflight: PENDING
Real personal data imported: NO
Personal Pilot authorized: NO
Formal private personal_fit authorized: NO
```

PHASE 8 therefore has a deliberately split verdict:

```text
PHASE 8 SOFTWARE/TOOLING = PASS
PHASE 8 REAL HOST GATE = OPEN
PERSONAL PILOT = BLOCKED
```

The next executable action is not to ingest the user's visual archive. It is to run the local/private preflight on the actual durable writer host and retain its private PASS receipt.
