# LIU VISUAL SYSTEM — PHASE 7 MINIMAL SCAFFOLD REPORT

Status: `IMPLEMENTED / SYNTHETIC_VERIFICATION_PASS`
Date: `2026-08-12`
Branch: `phase-7-minimal-scaffold-20260812`
Base: Architecture V0.1 frozen at `04dc98ccd772c6de3fbe2a3baf1c2b3c5093d1bf`

## Scope implemented

PHASE 7 implements only the minimum frozen raw-evidence scaffold:

- public, non-sensitive JSON Schema documents for the four raw record families;
- standard-library runtime validation with strict raw-field allowlists;
- explicit private-root file persistence;
- stable opaque IDs;
- SHA-256 exact-blob identity;
- Sample/Asset identity separation;
- local Asset Vault bytes and truthful asset resolution;
- append-oriented direct-user EvidenceEvent ledger;
- correction / supersede / retract replay;
- tombstone exclusion;
- pairwise and user-directed revision events;
- GenerationRecord lineage;
- transitive blind-eval discovery quarantine;
- derived artifact write/delete/rebuild proof;
- backup and restore helpers;
- basic cross-record integrity doctor;
- synthetic/non-sensitive verification suite.

## Deliberately not implemented

- real personal image/reference ingestion;
- personal Pilot dataset;
- VisualContextPack host integration;
- calibration projection adapter;
- preference profiles beyond a synthetic rebuild artifact;
- embeddings/vector database;
- perceptual duplicate detection;
- object-store vendor integration;
- trained preference/reward model;
- new Router, visual Skill, critic, or Skill-promotion engine;
- automatic Skill changes;
- multi-user or multi-writer support;
- physical purge tooling for real personal data.

## Synthetic verification

Command:

```bash
python scripts/verify_visual_memory.py
```

Result:

```text
12 tests run
12 passed
0 failed
0 errors
```

Verified behaviors:

1. stable ID prefixes and SHA-256 exact-blob behavior;
2. asset locator move preserves sample/asset identity;
3. private-root guard rejects a root inside a declared public repository;
4. direct user raw_text survives persistence round trip;
5. imported historical evidence requires a traceable source reference;
6. raw records reject inferred/unknown fields such as aesthetic scores or LLM summaries;
7. A/B, revision, generation parent lineage, and correction/retraction replay;
8. tombstone removes targets from effective/runtime discovery;
9. blind-reserved references require blind-reserved outputs;
10. blind-case evidence quarantine is transitive through corrections;
11. unavailable remote assets return unresolved rather than fabricated inspection;
12. derived state can be deleted/rebuilt and backup→restore preserves IDs, links, hashes, and resolvability.

The same source tree also passed Python bytecode compilation.

## Code-level Red Team corrections made before commit

The first local scaffold was not accepted immediately. Two design violations were found and fixed:

### RT-01 — unknown raw fields could contaminate source truth

Initial validation allowed additional keys. That could permit derived fields such as:

```text
aesthetic_score
llm_summary
inferred_preference
```

inside raw records.

Fix:

- runtime validation now uses strict field allowlists;
- published raw JSON Schemas use `additionalProperties: false` at the raw record boundary;
- synthetic tests prove contaminated fields are rejected.

### RT-02 — blind-reference output could accidentally be production data

Initial generation logging did not prevent a generation using a `blind_eval_reserved` reference from writing ordinary `production` output samples.

Fix:

- when any GenerationRecord reference is `blind_eval_reserved`, its output samples must also be `blind_eval_reserved`;
- synthetic test proves violation is rejected;
- discovery replay also quarantines direct and correction evidence that depends on reserved samples/generations.

## Remaining gates before a real personal Pilot

PHASE 7 does **not** authorize real private image ingestion yet.

Still required before the first non-disposable personal Pilot:

- choose/configure an actual private root outside public Git;
- choose/configure a durable Asset Vault location;
- perform backup/export and restore against that real private root;
- document and verify physical purge for requested sensitive data/assets;
- verify Git ignore / operational workflow cannot accidentally commit private paths/data;
- decide the actual single-writer execution host for the first Pilot;
- run the synthetic suite from the final operational environment;
- keep public calibration from becoming a private anchor sink.

## Verdict

```text
PHASE 7 MINIMAL SCAFFOLD = PASS
SYNTHETIC VERIFICATION = PASS
REAL PERSONAL PILOT = NOT STARTED / NOT YET AUTHORIZED
```
