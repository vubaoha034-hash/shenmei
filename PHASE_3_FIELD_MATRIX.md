# LIU VISUAL SYSTEM — PHASE 3 FIELD MATRIX

Status: `DESIGN_COMPLETE`

Date: `2026-08-12`

Purpose: prevent schema theater by requiring every proposed durable field to have a concrete writer, reader, and migration justification.

This file is a companion to `PHASE_3_MIN_DATA_CONTRACT.md`.

---

# 1. Admission rule

A field belongs in the V0.1 durable contract only if at least one of the following is true:

1. it preserves user evidence that cannot be reconstructed later;
2. it prevents catastrophic relabeling/relinking migration;
3. it is cheap deterministic provenance/integrity metadata;
4. it is necessary to prevent evaluation contamination;
5. it is necessary to distinguish renderer behavior from preference evidence.

Fields that only make future analytics more convenient should remain derived or deferred.

---

# 2. SampleRecord fields

| Field | Required | Writer | Primary reader | Why durable | Decision |
|---|---:|---|---|---|---|
| `schema_version` | Yes | ingestion | migration/validator | enables future schema evolution | KEEP |
| `sample_id` | Yes | ingestion | all relations | stable logical identity independent of asset/path | KEEP |
| `created_at` | Yes | ingestion | audit/drift analysis | historical ordering cannot always be reconstructed later | KEEP |
| `sample_kind` | Yes | ingestion | retrieval/evaluation | distinguishes reference/generated/imported without fixed taxonomy | KEEP |
| `primary_asset_id` | Yes | ingestion | asset resolver | minimum direct link to a usable visual asset | KEEP |
| `dataset_role` | Yes | ingestion/eval governance | discovery/eval pipeline | protects blind-eval reservation from leakage | KEEP |
| `provenance.source_type` | Yes | ingestion | governance/retrieval | preserves origin class even if file moves | KEEP |
| `provenance.source_ref` | No | ingestion | governance | source may be unavailable; preserve when known | KEEP OPTIONAL |
| `provenance.creator` | No | ingestion/user | copyright/governance | useful when known; must not burden user | KEEP OPTIONAL |
| `provenance.license` | No | ingestion/user | reuse/governance | important for copied assets/code where known | KEEP OPTIONAL |
| `user_tags` | No | user/ingestion | simple retrieval | explicit user labels are durable evidence; inferred tags are not | KEEP OPTIONAL |

## Rejected from raw SampleRecord

| Candidate field | Reason rejected/deferred |
|---|---|
| `aesthetic_score` | AI/professional score is derived, not raw preference truth |
| `style_cluster` | automatic clustering is deferred and unstable |
| `visual_dna` | universal DNA is not established |
| `domain_id` hard enum | fixed taxonomy would create lock-in |
| `embedding` | infrastructure/derived artifact |
| `dominant_color` | deterministic/vision-derived metadata can be rebuilt later |
| `composition_type` | interpretation, not irreplaceable raw fact |
| `personal_fit` | must remain derived/null until evidence exists |

---

# 3. AssetRecord fields

| Field | Required | Writer | Primary reader | Why durable | Decision |
|---|---:|---|---|---|---|
| `schema_version` | Yes | ingestion | migration/validator | versioned durable record | KEEP |
| `asset_id` | Yes | ingestion | sample/asset relations | exact blob identity independent of path | KEEP |
| `sample_id` | Yes | ingestion | resolver/audit | binds blob to logical visual sample | KEEP |
| `created_at` | Yes | ingestion | audit | distinguishes asset versions and history | KEEP |
| `sha256` | Yes | deterministic ingestion | dedupe/integrity | cheap exact duplicate and integrity check | KEEP |
| `locator_kind` | Yes | ingestion | resolver | minimum interpretation of locator without object-store framework | KEEP |
| `locator` | Yes | ingestion/storage update | resolver | tells implementation where current blob can be found | KEEP |
| `asset_relation` | Yes | ingestion | resolver/revision analysis | supports primary/alternate/derivative without conflating blobs | KEEP |
| `derived_from_asset_id` | No | ingestion | lineage/audit | useful only when derivative relation is known | KEEP OPTIONAL |
| `media_type` | No | deterministic ingestion | renderer/viewer | cheap objective metadata | KEEP OPTIONAL |

## Rejected from raw AssetRecord

| Candidate field | Reason rejected/deferred |
|---|---|
| `perceptual_hash` | near-duplicate system deferred |
| `s3_bucket`, `r2_bucket`, `gcs_bucket` | storage-specific abstraction premature |
| `vector_embedding` | derived/infrastructure |
| `quality_score` | derived judgment |
| `style_tags` | derived interpretation |

---

# 4. EvidenceEvent envelope fields

| Field | Required | Writer | Primary reader | Why durable | Decision |
|---|---:|---|---|---|---|
| `schema_version` | Yes | event recorder | migration/validator | versioning | KEEP |
| `event_id` | Yes | event recorder | all evidence consumers | stable evidence identity | KEEP |
| `occurred_at` | Yes | event recorder | chronology/correction/drift | original sequence matters | KEEP |
| `event_type` | Yes | event recorder | event replay | distinguishes minimal semantics | KEEP |
| `source_kind` | Yes | event recorder | preference derivation | prevents critic/system claims becoming user truth | KEEP |
| `source_ref` | No | event recorder | audit | allows trace back to conversation/case when available | KEEP OPTIONAL |
| `scope.level` | Yes | recorder/user-context resolver | context retrieval | prevents one-off feedback becoming global by default | KEEP |
| `scope.domain` | Conditional | recorder | domain retrieval | only required when `scope.level=domain` | KEEP CONDITIONAL |
| `raw_text` | Yes* | recorder | human audit/derivation | irreplaceable original wording | KEEP |
| `target_sample_ids` | Yes | recorder | retrieval/relations | binds evidence to visuals | KEEP |
| `target_generation_ids` | Yes | recorder | execution audit | links feedback to generation run when relevant | KEEP |
| `payload` | Yes | typed event recorder | event-specific reader | keeps event family count low without losing typed semantics | KEEP |

`raw_text` may be empty only for a direct structured user action whose exact action is fully represented in the typed payload.

## Rejected from raw EvidenceEvent envelope

| Candidate field | Reason rejected/deferred |
|---|---|
| `llm_summary` | derived; may be wrong and can be rebuilt |
| `inferred_preference_rule` | derived/candidate rule; belongs outside raw truth |
| `confidence` for user statement | risks pretending model confidence is source truth; interpretation confidence belongs derived |
| `sentiment_score` | derived |
| `global_weight` | fixed preference weighting rejected |

---

# 5. Feedback payload

| Field | Required | Writer | Reader | Decision |
|---|---:|---|---|---|
| `explicit_verdict` | No | recorder only when explicit | preference derivation | KEEP OPTIONAL |

Allowed: `approved / rejected / neutral / null`.

Do not infer a verdict merely to fill the field.

---

# 6. Comparison payload

| Field | Required | Writer | Reader | Why | Decision |
|---|---:|---|---|---|---|
| `left_sample_id` | Yes | recorder | pairwise analysis | stable pair identity | KEEP |
| `right_sample_id` | Yes | recorder | pairwise analysis | stable pair identity | KEEP |
| `winner` | Yes | recorder | preference analysis | preserves direct ordering | KEEP |
| `comparison_kind` | Yes | recorder | causal-safety logic | distinguishes natural pair from controlled experiment | KEEP |

Allowed winner: `left / right / tie / unclear`.

Allowed comparison kind: `natural / controlled`.

Rejected: automatic “winning dimensions” in raw payload. That is derived interpretation.

---

# 7. Revision payload

| Field | Required | Writer | Reader | Why | Decision |
|---|---:|---|---|---|---|
| `before_sample_id` | Yes | recorder | revision analysis | preserves lineage | KEEP |
| `after_sample_id` | Yes | recorder | revision analysis | preserves lineage | KEEP |
| `requested_change_text` | Yes | recorder | human/derived analysis | preserves what was actually requested | KEEP |
| `result_feedback_event_id` | No | recorder after reaction | revision analysis | links explicit outcome evidence when available | KEEP OPTIONAL |
| `causal_attribution` | Yes | recorder | causal-safety logic | prevents relation being mistaken for proof of cause | KEEP |

Allowed causal attribution: `user_stated / controlled / unknown`.

Rejected: `llm_inferred` in raw data.

---

# 8. Correction payload

| Field | Required | Writer | Reader | Why | Decision |
|---|---:|---|---|---|---|
| `target_event_ids` | Yes | recorder | effective-state projection | identifies corrected evidence | KEEP |
| `effect` | Yes | recorder | effective-state projection | defines supersede/retract/clarify semantics | KEEP |

Allowed effect: `supersede / retract / clarify`.

No raw record is silently rewritten to represent the new interpretation.

---

# 9. Tombstone payload

| Field | Required | Writer | Reader | Why | Decision |
|---|---:|---|---|---|---|
| `target_record_ids` | Yes | deletion/governance path | every consumer | ensures deleted material is excluded everywhere | KEEP |
| `reason` | Yes | deletion/governance path | audit | distinguishes deletion from corruption/other removal | KEEP |

Physical purge implementation is deferred.

---

# 10. GenerationRecord fields

| Field | Required | Writer | Primary reader | Why durable | Decision |
|---|---:|---|---|---|---|
| `schema_version` | Yes | generation runtime | migration/validator | versioning | KEEP |
| `generation_id` | Yes | generation runtime | events/revisions/audit | stable run identity | KEEP |
| `created_at` | Yes | runtime | chronology/model-change analysis | distinguishes preference change from system change | KEEP |
| `renderer` | Yes | runtime | audit | renderer behavior may change independently of taste | KEEP |
| `model` | Yes | runtime | audit | model identity materially affects output | KEEP |
| `model_version` | No | runtime | audit | store when available; do not invent | KEEP OPTIONAL |
| `task_ref` | No | runtime | traceability | useful when durable task/case ID exists | KEEP OPTIONAL |
| `reference_sample_ids` | Yes | runtime | reproduction/retrieval audit | records which exemplars affected execution | KEEP |
| `parent_generation_id` | No | runtime | revision lineage | useful for iterative generation | KEEP OPTIONAL |
| `output_sample_ids` | Yes | runtime | event linkage | connects run to visual outputs | KEEP |
| `prompt_text` | No | runtime | execution debugging | useful but explicitly not preference truth | KEEP OPTIONAL |
| `parameters` | Yes | runtime | execution debugging | preserves available renderer settings without freezing schema | KEEP |

## Rejected from raw GenerationRecord

| Candidate field | Reason rejected/deferred |
|---|---|
| `personal_fit_score` | derived and uncalibrated |
| `aesthetic_score` | derived diagnostic |
| `winning_prompt_formula` | derived inference |
| `style_cluster` | derived |
| adapter-specific normalized mega-schema | renderer adapter framework deferred |

---

# 11. Derived artifact envelope

Only a generic provenance envelope is admitted now.

| Field | Required | Why |
|---|---:|---|
| `artifact_id` | Yes | identity |
| `artifact_type` | Yes | identifies projection type |
| `built_at` | Yes | staleness/audit |
| `builder_version` | Yes | reproducibility/debugging |
| `source_record_ids` | Yes | rebuildability and provenance |
| `content` | Yes | derived payload |

No specific Visual DNA/profile schema is frozen in PHASE 3.

---

# 12. Field-count sanity check

The durable raw model intentionally remains small:

- `SampleRecord`: 7 required fields + small provenance object;
- `AssetRecord`: 8 required fields;
- `EvidenceEvent`: 10 required envelope fields with small typed payloads;
- `GenerationRecord`: 8 required fields.

The user does not manually fill these fields. Most are machine-generated.

The only high-value human information is still the natural visual decision itself.

---

# 13. Migration-cost classification

## Catastrophic if omitted now

- stable `sample_id`;
- asset/sample separation;
- verbatim `raw_text`;
- correction/retraction links;
- source scope;
- raw/derived separation;
- provenance source;
- renderer/model on generation records;
- blind-eval reservation.

## Moderate if omitted now

- exact `sha256`;
- derivative asset lineage;
- pairwise typed payload;
- revision typed payload;
- optional prompt execution metadata.

## Cheap to add later

- embeddings;
- perceptual hashes;
- detailed visual taxonomy;
- vector DB locators;
- object-store fields;
- richer renderer adapter fields;
- aesthetic dimensions;
- automated clusters.

This is why they remain out of the V0.1 contract.

---

# 14. Compatibility decisions

## Existing `calibration/anchors.json`

Decision: future compatibility projection, not parallel raw truth.

Reason: maintaining both anchors and a new evidence ledger as manually edited personal-preference authorities would create drift.

## Existing `.skill-evolution/<target>/state.json`

Decision: remain separate.

Reason: it stores promotion/evolution workflow state, not the primary personal visual evidence archive.

Future integration direction:

```text
visual EvidenceEvent IDs
        ↓ cited as evidence
skill-refiner observation/candidate
        ↓ evaluated
reviewable Skill change
```

Never reverse this dependency so that raw taste records require Skill Refiner state to be interpreted.

---

# 15. PHASE 3 field gate

A field proposed after PHASE 3 must answer all five questions before entering the durable raw contract:

```text
1. Who writes it?
2. Who reads it?
3. Is it raw fact or derived interpretation?
4. What user value is lost if it is absent?
5. Is later migration materially more expensive than adding it now?
```

If these questions cannot be answered, the default verdict is:

```text
DEFER
```

not `KEEP`.
