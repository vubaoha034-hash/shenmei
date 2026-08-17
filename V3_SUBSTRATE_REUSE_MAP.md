# V3 Frozen Substrate Reuse Map

Status: `FROZEN_SUBSTRATE_REUSE`

V3 is a rebuildable derived layer above the PHASE 1–8 substrate. It creates no
parallel raw store and requires no re-import, relabel, or re-approval of raw
visual evidence.

| Capability | Existing authority | V3 decision |
|---|---|---|
| Raw evidence storage | `VisualMemoryStore`; Sample, Asset, Evidence, Generation JSON records | `FROZEN_SUBSTRATE_REUSE` |
| Asset Vault and exact-blob identity | `visual_memory/store.py`; SHA-256 resolution against `vault/` | `FROZEN_SUBSTRATE_REUSE` |
| Evidence ledger and correction replay | `raw/evidence/events.jsonl`; `visual_memory/replay.py` | `FROZEN_SUBSTRATE_REUSE` |
| Provenance and generation lineage | Asset/Sample provenance and GenerationRecord parent/reference/output links | `FROZEN_SUBSTRATE_REUSE` |
| Backup and restore | `visual_memory/backup.py` with restore integrity checks | `FROZEN_SUBSTRATE_REUSE` |
| Privacy boundary | Explicit private data root outside public Git; `assert_outside_public_repo` | `FROZEN_SUBSTRATE_REUSE` |
| Deletion | tombstone replay plus `visual_memory/purge.py` physical purge gate | `FROZEN_SUBSTRATE_REUSE` |
| Single writer and host integrity | `WriterLease`, operational configuration, `VisualMemoryStore.doctor()` | `FROZEN_SUBSTRATE_REUSE` |
| Blind isolation | sticky `blind_eval_reserved` role and discovery exclusion | `FROZEN_SUBSTRATE_REUSE` |
| Durable Skill promotion | `skill-refiner` evidence/evaluation/Git gate; ADR-006 | `FROZEN_SUBSTRATE_REUSE` |

## V3 ownership boundary

V3 may write only derived, rebuildable artifacts whose lineage points back to
raw IDs. It may validate and rank evidence support, package hypotheses for
human review, maintain family/mechanism registries, and build bounded runtime
packages from reviewed programs.

V3 must not mutate raw wording, replace canonical assets, create a fifth raw
truth family, turn inferred analysis into raw evidence, or create a second
promotion authority.

## Verified private instances used by the initial hypotheses

The private PHASE 9 store resolved and SHA-verified both canonical assets:

- Reference 05: `smp_c8e1c9c1-1c3a-414a-b54e-ee2a5069f733` →
  `ast_415897bc-faae-4f55-bfeb-a9fde4acdddf`, SHA-256
  `eedd32a428f7483fefc53b1f5107dc9a790b76db2e408b29917607c3fb030e38`,
  1080×1440 JPEG.
- Reference 13: `smp_07d29426-97f3-4d2f-9233-d0b196b6e6e7` →
  `ast_147f0ca3-83dd-47ed-9d74-ebbd19001532`, SHA-256
  `3f8cd4b9bf99be512c7b543a931c8c505877e4692b777751fd30a3ad6f3b29d7`,
  1080×1440 JPEG.

Their shared direct approval event is whole-image, domain-scoped evidence. It
does not approve every component mechanism.
