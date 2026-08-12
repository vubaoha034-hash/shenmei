# LIU VISUAL SYSTEM — PHASE 9 SMALL PERSONAL PILOT

Status: `READY_FOR_REAL_PILOT / NOT_STARTED`
Date: `2026-08-12`
Base: verified Windows PHASE 8 HEAD `b74117f678a4ad9cfc3e664ae44606a6b10e0b29`

## 0. Purpose

PHASE 9 is the first stage allowed to ingest real personal visual evidence.

The goal is **not** to build a large taste library. The goal is to test whether a small amount of explicit personal evidence produces measurably better visual outcomes than the existing system without personal memory.

The Pilot must answer:

1. Does bounded personal context beat the existing baseline in blind A/B preference?
2. Does it reduce revision rounds?
3. Does exemplar retrieval return references the user agrees are relevant?
4. Does it avoid known rejected mechanisms without overriding the current task?
5. Can incorrect derived interpretation be deleted/rebuilt without damaging raw evidence?

If these are not demonstrated, do not scale the library.

---

## 1. Hard boundaries

PHASE 9 must continue to obey `ARCHITECTURE_V0.1_FROZEN.md`.

Forbidden during the Pilot:

- bulk ingest of the full visual archive;
- embeddings/vector database;
- trained preference/reward model;
- automatic clustering as authority;
- new visual Router;
- new mega personal visual Skill;
- modification of `personal-aesthetic-critic` merely to make the Pilot pass;
- automatic Skill promotion;
- public Git storage of private evidence/assets;
- using silence/upload alone as a preference label;
- using blind-eval outputs/evidence for discovery.

---

## 2. Pilot dataset size

Keep the first real set deliberately small.

Recommended discovery pool:

```text
20–40 explicitly liked/reference samples
10–20 explicitly rejected samples
optional small neutral set
```

Do not exceed roughly 60 discovery samples in the first Pilot unless there is a concrete reason.

The Pilot should cover at least 2–3 real visual domains/tasks that the user actually uses, so cross-domain leakage can be observed.

Do not force equal counts per domain.

---

## 3. Explicit evidence requirement

An image becomes preference evidence only with an explicit user statement or explicit structured action.

Good batch evidence examples:

```text
“这批我都喜欢，可以作为餐饮品牌参考。”
“这 12 张我明确不喜欢，主要作为反例。”
“这几张只是参考，不代表整体喜欢。”
```

A single exact user statement may target multiple SampleRecords when it truthfully applies to the whole selected batch.

Do not manufacture one sentence per image if the user did not say it.

Uploading a directory alone is not approval.

---

## 4. Discovery vs blind evaluation

### Discovery samples

May be used for:

- effective evidence replay;
- scoped preference projection;
- exemplar selection;
- runtime VisualContextPack.

### Blind-eval material

Must be isolated before any derived preference process can see it.

For V0.1:

- blind generation outputs are `blind_eval_reserved`;
- user A/B judgments on those outputs are quarantined;
- their EvidenceEvent IDs do not feed profiles, retrieval or `skill-refiner`;
- they remain sticky reserved under ADR-007.

---

## 5. Minimal personal context strategy

The first Pilot does **not** use embeddings.

Context selection must be transparent and inspectable.

V0.1 Pilot inputs may use:

- explicit verdict (`approved` / `rejected` / `reference` semantics from user evidence);
- evidence scope;
- free-form user tags where explicitly supplied;
- current task/domain match;
- current asset resolvability;
- small recency tie-break where useful.

The system must be able to explain:

```text
why this exemplar was selected
which user EvidenceEvent supports its role
whether the asset was actually resolvable/inspected
```

---

## 6. VisualContextPack Pilot shape

The first Pilot context pack is ephemeral and private.

Recommended shape:

```json
{
  "domain": "<free-form or null>",
  "positive_exemplars": [
    {"sample_id": "...", "evidence_ids": ["..."], "raw_text": "...", "resolvable": true}
  ],
  "negative_exemplars": [],
  "explicit_scoped_preferences": [],
  "source_event_ids": []
}
```

Guidance:

- normally 2–5 positive/reference exemplars;
- normally 0–3 negative exemplars;
- include only evidence relevant to the current domain/task;
- do not reproduce the entire archive;
- do not turn the pack into an alternate visual Skill grammar.

Counts are tuning guidance, not frozen architecture.

---

## 7. Primary experiment — blind Baseline vs Personal Context

Use the same task brief for both conditions.

### Baseline

```text
current explicit user task
+ current explicit references supplied for that task
+ existing repository route / existing visual Skill
```

No historical personal-memory context.

### Personalized

Exactly the same current task and existing route, plus the bounded `VisualContextPack` produced only from discovery evidence.

Do not change unrelated prompt language just to help one condition.

### Renderer control

Use the same renderer/model/version and as-close-as-practical settings for both conditions.

Renderer stochasticity is accepted; do not infer too much from a single pair.

### Blind presentation

Before the user evaluates:

- hide condition identity;
- randomize left/right or A/B placement;
- do not expose filenames such as `baseline` or `personalized`;
- user chooses A / B / tie based on the visible result.

Only after the choice is locked may condition mapping be revealed for scoring.

---

## 8. Minimum evaluation volume

First decision point requires at least:

```text
10 valid blind A/B pairs
```

Prefer coverage across multiple real task/domain families rather than ten near-identical prompts.

If renderer randomness appears large, add repeat pairs rather than pretending one generation is decisive.

---

## 9. Pilot decision rule

This is an experimental gate, not a permanent architecture invariant.

### PASS_TO_EXPAND

All hard safety/authority gates pass, and:

- personalized wins at least 60% of non-tie valid blind pairs;
- personalized has at least 2 more wins than baseline;
- no observed case where historical memory overrides a current explicit instruction;
- no blind-eval contamination;
- no private-data Git leakage.

### INCONCLUSIVE

Examples:

- fewer than 10 valid pairs;
- results near even;
- too many ties;
- renderer variance obscures the effect;
- retrieval relevance is inconsistent.

Action: repeat/fix the smallest failing layer. Do not scale data yet.

### FAIL / REWORK

Any of:

- baseline wins as often or more often than personalized after sufficient valid pairs;
- systematic cross-domain preference leakage;
- repeated irrelevant exemplar retrieval;
- current explicit instruction loses to historical memory;
- derived interpretation cannot be deleted/rebuilt safely;
- evaluation contamination/privacy breach.

Action: identify the failing layer. Do not add more Skills/rules by default.

---

## 10. Secondary metrics

Record but do not turn into personal truth:

```text
revision rounds until accepted
first-generation explicit acceptance
retrieved exemplar relevance
known-rejection recurrence
user override/conflict count
context assembly failures
asset-resolution failures
```

Silence is not acceptance.

---

## 11. Pilot sequence

### P9-A — real sample ingestion

1. verify PHASE 8 private PASS receipt;
2. acquire `local-codex-primary` WriterLease;
3. ingest only the selected small sample set;
4. copy durable visual bytes into the private Asset Vault where appropriate;
5. add explicit batch/single user EvidenceEvents;
6. run `doctor()`;
7. backup the private root after the first real ingestion checkpoint.

### P9-B — build first derived context

1. replay effective evidence;
2. exclude tombstoned / blind material;
3. build a small scoped projection;
4. select transparent exemplars;
5. verify selected assets are actually resolvable;
6. write derived context artifacts only under the private derived root.

### P9-C — retrieval sanity review

Before generation experiment, show the selected exemplar set for several representative tasks.

The user should be able to say whether the retrieved references are actually relevant.

If retrieval is obviously wrong, fix retrieval before spending generation runs.

### P9-D — blind A/B generation

Run at least 10 valid baseline vs personalized pairs.

All blind outputs and dependent feedback remain quarantined from discovery.

### P9-E — score and decide

Lock pair decisions first, then reveal condition mapping and calculate win/tie/loss.

Apply the decision rule in section 9.

### P9-F — backup / audit

At the Pilot checkpoint:

- run `doctor()`;
- create backup;
- restore/audit a copy if the raw model changed materially;
- verify Git privacy;
- verify blind quarantine;
- verify public `calibration/anchors.json` is still not a private data sink.

---

## 12. What a successful PHASE 9 means

A successful Pilot does **not** prove a universal Preference Model exists.

It only proves that:

> a small, explicit, private personal evidence set + bounded exemplar context improves this user's real visual work enough to justify expanding the dataset and runtime integration.

If PASS_TO_EXPAND, the next phase may expand the library gradually and harden host-level context integration.

Do not jump directly from 40 samples to thousands.
