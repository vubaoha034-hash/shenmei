# LIU VISUAL SYSTEM — PHASE 8 LOCAL PRIVATE ROOT RUNBOOK

Status: `READY_TO_RUN_ON_DURABLE_PRIVATE_HOST`
Date: `2026-08-12`

This runbook closes the part of PHASE 8 that cannot be executed truthfully from an ephemeral cloud chat runtime: creating and verifying the actual durable private writer environment.

## Preconditions

Choose two durable private locations:

1. `DATA_ROOT` — canonical personal visual-memory data + Asset Vault.
2. `BACKUP_DIR` — a separate private backup location.

They must:

- be outside the public `shenmei` repository;
- not contain one another;
- be durable across restarts;
- not be a temporary ChatGPT/Codex sandbox directory.

V0.1 uses one logical writer. Choose one stable writer label such as:

```text
local-codex-primary
```

The label is operational identity, not a user preference field.

## Windows example

From a local checkout of this PHASE 8 branch:

```powershell
python scripts/visual_memory_operational_preflight.py `
  --data-root "<PRIVATE_DATA_ROOT>" `
  --backup-dir "<SEPARATE_PRIVATE_BACKUP_DIR>" `
  --writer-id "local-codex-primary"
```

Do not use the repository directory itself as either private path.

## macOS / Linux example

```bash
python scripts/visual_memory_operational_preflight.py \
  --data-root "<PRIVATE_DATA_ROOT>" \
  --backup-dir "<SEPARATE_PRIVATE_BACKUP_DIR>" \
  --writer-id "local-codex-primary"
```

## Environment-variable alternative

```text
LIU_VISUAL_DATA_ROOT
LIU_VISUAL_BACKUP_DIR
LIU_VISUAL_WRITER_ID
LIU_VISUAL_CALIBRATION_OVERLAY   # optional, not yet required
```

Then run:

```bash
python scripts/visual_memory_operational_preflight.py
```

## What the preflight actually verifies

The command uses synthetic/non-sensitive records only and verifies:

- private root is outside public Git;
- backup location is outside public Git and separate from the data root;
- single-writer lock can be acquired exclusively;
- PHASE 7 synthetic suite still passes on this host;
- synthetic records can be backed up and restored with stable IDs and assets;
- Tombstone-gated physical purge removes targeted bytes/evidence and clears derived cache;
- public `calibration/anchors.json` is unchanged;
- no real personal visual data is imported.

On PASS it writes a private receipt:

```text
<DATA_ROOT>/operations/phase8_preflight.json
```

That receipt is not committed to Git.

## Formal personal_fit

PHASE 8 does not enable private `personal_fit` automatically.

Until a privacy-safe calibration overlay is integrated with the existing critic:

```text
personal_fit = null
```

is the correct behavior.

## Physical purge

Physical purge requires a prior explicit Tombstone event for every ID being physically purged.

Dry-run:

```bash
python scripts/visual_memory_purge.py --dry-run <record_id> [<record_id> ...]
```

Execute:

```bash
python scripts/visual_memory_purge.py <record_id> [<record_id> ...]
```

The purge tool never deletes arbitrary external source files. It deletes controlled Asset Vault bytes, scrubs stored locators/private metadata, removes explicitly tombstoned evidence records, scrubs related generation prompt/task metadata, and clears rebuildable derived cache.

## PHASE 8 exit condition

PHASE 8 is fully closed only when the actual durable writer host produces:

```json
{
  "status": "PASS",
  "pilot_authorized_on_this_writer_host": true,
  "real_personal_data_imported": false
}
```

in the private preflight receipt.

Only then may the small Personal Pilot begin.
