# LIU Visual Memory V0.1 — Minimal Scaffold

This package is the PHASE 7 implementation of `ARCHITECTURE_V0.1_FROZEN.md`.

It intentionally implements only the frozen raw-data and integrity loop:

- four raw record families: Sample / Asset / Evidence / Generation;
- explicit private-root boundary;
- exact SHA-256 blob identity;
- append-oriented direct-user evidence;
- correction/retraction replay;
- tombstone exclusion;
- blind-eval discovery quarantine;
- minimal generation lineage;
- asset resolution truthfulness;
- rebuildable derived test artifacts;
- backup/restore verification;
- integrity doctor.

It intentionally does **not** implement:

- image embeddings or vector DB;
- preference/reward model;
- automatic clustering;
- object-store provider integration;
- perceptual duplicate detection;
- runtime VisualContextPack integration;
- calibration adapter;
- new visual Skill/router/critic;
- automatic Skill promotion;
- real personal reference ingestion.

## Private root

Real personal data must use an explicit private path outside the public repository, for example through:

```bash
export LIU_VISUAL_DATA_ROOT=/private/path/liu-visual-memory
```

The package never defaults the personal data root into the repository.

## Synthetic verification

```bash
python scripts/verify_visual_memory.py
```

The test suite uses temporary, synthetic/non-sensitive files only.
