# LIU VISUAL SYSTEM — PHASE 3 MINIMUM DATA CONTRACT

Status: `PHASE_3 / DESIGN_COMPLETE`

Date: `2026-08-12`

Branch: `phase-3-min-data-contract-20260812`

Scope: define the **minimum durable data contract** required to preserve personal visual evidence without prematurely building Skills, schemas, scripts, storage infrastructure, embeddings, trained preference models, or a final architecture.

This phase is intentionally narrow.

---

# 0. Executive decision

The V0.1 data layer should preserve only the information that would be expensive or impossible to reconstruct later.

The minimum durable model is:

```text
logical visual sample
        ↓
exact asset blob(s)
        ↓
raw user evidence events
        ↓
comparison / revision relations when they actually occur
        ↓
minimal generation history for generated outputs
        ↓
rebuildable derived profiles / exemplars / candidate rules
```

The contract therefore has **four durable raw record families**:

1. `SampleRecord`
2. `AssetRecord`
3. `EvidenceEvent`
4. `GenerationRecord`

Everything else is either:

- a derived projection;
- an evaluation artifact built later;
- an existing `skill-refiner` concern;
- or explicitly deferred.

The core anti-rework invariant is:

> **A future implementation may replace every derived profile, retrieval method, prompt compiler, critic, renderer adapter, taxonomy, or Skill without requiring the user to manually relabel the original visual samples and historical decisions.**

---

# 1. Contract boundaries

## 1.1 Raw truth

Raw records may contain only facts that came directly from one of these sources:

- the visual asset itself;
- user-provided source/provenance information;
- a direct user action or utterance;
- a concrete generation execution;
- deterministic ingestion metadata such as SHA-256.

Raw records must **not** contain LLM-inferred taste rules such as:

```text
"User prefers cinematic darkness"
"User dislikes warm palettes"
"This revision improved because grain was reduced"
```

unless the user explicitly stated that claim and the record preserves the original wording.

## 1.2 Derived truth

The following are always rebuildable derived outputs:

- visual profiles;
- inferred taste summaries;
- candidate global preferences;
- semantic tags not explicitly supplied by the user;
- embeddings;
- clusters;
- exemplar rankings;
- retrieval indexes;
- aesthetic scores;
- candidate rules;
- prompt/compiler advice.

A derived artifact may point **to** raw IDs.

A raw record must never depend on a derived artifact for its meaning.

## 1.3 Skill evolution is a separate authority

The existing `skill-refiner` remains the authority for:

```text
observation
→ candidate
→ evaluation
→ promotion
→ archive
```

The visual data contract does not recreate candidate/active/deprecated rule state.

A future `skill-refiner` observation may cite one or more visual `event_id` values as evidence, but the raw visual ledger remains independent.

---

# 2. Stable ID policy

All durable records use opaque generated IDs.

Recommended form:

```text
smp_<uuid>
ast_<uuid>
ev_<uuid>
gen_<uuid>
```

The UUID implementation is deliberately not frozen in PHASE 3. UUIDv4, UUIDv7, or another collision-safe generator may be selected during implementation.

Hard rules:

1. IDs are assigned once.
2. File paths are never IDs.
3. URLs are never IDs.
4. SHA-256 is not a logical sample ID.
5. Taxonomy labels are never embedded in IDs.
6. Moving, renaming, or re-hosting an asset must not change `sample_id`.

---

# 3. SampleRecord

A `SampleRecord` represents one logical visual item that may accumulate preference history.

Examples:

- one collected poster reference;
- one photography reference;
- one generated image;
- one revised generated image;
- one rejected visual candidate.

It is **not** the binary file itself.

## 3.1 Minimum fields

```json
{
  "schema_version": "1",
  "sample_id": "smp_<uuid>",
  "created_at": "2026-08-12T05:00:00Z",
  "sample_kind": "reference",
  "primary_asset_id": "ast_<uuid>",
  "dataset_role": "discovery",
  "provenance": {
    "source_type": "web",
    "source_ref": "opaque source locator",
    "creator": null,
    "license": null
  },
  "user_tags": []
}
```

## 3.2 Required fields

- `schema_version`
- `sample_id`
- `created_at`
- `sample_kind`
- `primary_asset_id`
- `dataset_role`
- `provenance.source_type`

## 3.3 Allowed `sample_kind` in V0.1

```text
reference
generated
imported
```

Do not create a large type system.

## 3.4 Dataset role

V0.1 uses only:

```text
discovery
blind_eval_reserved
production
unassigned
```

Semantics:

- `discovery`: may contribute to preference derivation.
- `blind_eval_reserved`: must not contribute to preference derivation before the blind evaluation using it is completed.
- `production`: generated/used during real work; may later supply regression evidence.
- `unassigned`: not yet authorized for either discovery or reserved blind evaluation.

Important:

`regression` is **not** a dataset partition. A known production failure can later become a regression case without pretending it was held out.

## 3.5 Provenance

`provenance` must remain minimal and may contain unknown values.

Allowed `source_type` examples:

```text
user_upload
web
repo
generated
unknown
```

`source_ref` is optional and opaque. It may be a URL, repository path, conversation attachment reference, or another stable locator available at ingestion time.

`creator` and `license` are optional because forcing the user to fill them would create excessive labeling burden.

Unknown provenance must be represented as unknown, not invented.

## 3.6 Tags

`user_tags` are optional free-form strings explicitly supplied or confirmed by the user.

LLM-generated tags do not belong here; they belong in derived artifacts.

There is no fixed visual taxonomy in V0.1.

---

# 4. AssetRecord

An `AssetRecord` represents one exact binary blob.

A visual `SampleRecord` and an `AssetRecord` are deliberately different entities.

This prevents a moved, recompressed, resized, or replaced file from silently becoming a new preference entity.

## 4.1 Minimum fields

```json
{
  "schema_version": "1",
  "asset_id": "ast_<uuid>",
  "sample_id": "smp_<uuid>",
  "created_at": "2026-08-12T05:00:00Z",
  "sha256": "sha256:<64-hex>",
  "locator_kind": "local_file",
  "locator": "references/example.jpg",
  "asset_relation": "primary",
  "derived_from_asset_id": null,
  "media_type": "image/jpeg"
}
```

## 4.2 Required fields

- `schema_version`
- `asset_id`
- `sample_id`
- `created_at`
- `sha256`
- `locator_kind`
- `locator`
- `asset_relation`

## 4.3 Locator policy

V0.1 supports only broad locator classes:

```text
repo_relative
local_file
remote_url
opaque
```

Do **not** build dedicated `s3://`, `r2://`, `gs://`, or object-store resolver logic in V0.1.

The locator is mutable infrastructure metadata; the logical identity is not.

If an asset moves, implementation may update the current asset locator or append an asset-location change record later. The sample identity must remain stable.

## 4.4 Exact duplicate semantics

SHA-256 provides only byte-exact duplicate detection.

The contract explicitly does **not** claim that SHA-256 identifies:

- resized copies;
- recompressed copies;
- crops;
- watermarked copies;
- screenshots;
- color-adjusted derivatives.

Perceptual deduplication remains deferred.

## 4.5 Multiple assets for one sample

V0.1 permits more than one `AssetRecord` to share one `sample_id`.

Allowed `asset_relation` values:

```text
primary
alternate
derivative
```

When `asset_relation = derivative`, `derived_from_asset_id` should be populated when known.

No automatic claim is made that two derivatives are visually equivalent for evaluation purposes.

---

# 5. EvidenceEvent

`EvidenceEvent` is the most important record family.

It preserves what the user actually said or explicitly chose before any LLM interpretation.

Raw events are append-oriented.

Corrections do not silently rewrite old evidence.

## 5.1 Shared envelope

```json
{
  "schema_version": "1",
  "event_id": "ev_<uuid>",
  "occurred_at": "2026-08-12T05:10:00Z",
  "event_type": "feedback",
  "source_kind": "user",
  "source_ref": null,
  "scope": {
    "level": "task",
    "domain": null
  },
  "raw_text": "这个深黑不是我要的，这个看起来特别脏。",
  "target_sample_ids": ["smp_<uuid>"],
  "target_generation_ids": [],
  "payload": {}
}
```

## 5.2 Required envelope fields

- `schema_version`
- `event_id`
- `occurred_at`
- `event_type`
- `source_kind`
- `scope.level`
- `raw_text`
- `target_sample_ids`
- `target_generation_ids`
- `payload`

`raw_text` may be an empty string only when the evidence is a direct structured action such as an explicit A/B click whose raw action is captured in `payload`.

## 5.3 Source policy

V0.1 allows:

```text
user
system
import
```

Only `source_kind = user` may directly establish personal preference evidence.

System/critic output can be stored as technical evidence later, but must not be silently converted into user taste.

## 5.4 Scope policy

Raw scope values:

```text
task
domain
global_explicit
unspecified
```

Definitions:

- `task`: applies only to the current concrete task/output.
- `domain`: the user explicitly or contextually constrained a visual domain; `scope.domain` must contain a free-form domain label.
- `global_explicit`: use only when the user explicitly states a durable cross-domain preference.
- `unspecified`: the user expressed preference, but the durable scope is not safely known.

Important:

`global_candidate` is **not** a raw scope. It is a derived hypothesis that may emerge from repeated evidence.

This avoids turning one comment into a universal rule.

## 5.5 Event types

V0.1 supports only five event types:

```text
feedback
comparison
revision
correction
tombstone
```

Do not add more types without evidence from the pilot.

---

# 6. Feedback event

A normal reaction to one or more visual samples.

Example:

```json
{
  "event_type": "feedback",
  "raw_text": "这个好很多，但是撕开的范围还是太大。",
  "target_sample_ids": ["smp_after"],
  "payload": {
    "explicit_verdict": null
  }
}
```

`explicit_verdict` may be:

```text
approved
rejected
neutral
null
```

It is populated only when the verdict is explicit enough to preserve without semantic invention.

If the user says something ambiguous, keep it `null` and allow the derived interpretation layer to reason later.

---

# 7. Comparison event

A pairwise preference relation.

```json
{
  "event_type": "comparison",
  "raw_text": "A更好，B太脏。",
  "target_sample_ids": ["smp_A", "smp_B"],
  "payload": {
    "left_sample_id": "smp_A",
    "right_sample_id": "smp_B",
    "winner": "left",
    "comparison_kind": "natural"
  }
}
```

Allowed winner values:

```text
left
right
tie
unclear
```

Allowed `comparison_kind`:

```text
natural
controlled
```

V0.1 primarily records naturally occurring comparisons.

Controlled-pair experiment generation remains deferred.

A comparison event records **ordering**, not causality.

The statement:

```text
A > B
```

does not prove why A won when several variables differ.

---

# 8. Revision event

A relation between a before-state and after-state.

```json
{
  "event_type": "revision",
  "raw_text": "把灰尘感去掉，保留黑色层次和轮廓。",
  "target_sample_ids": ["smp_before", "smp_after"],
  "payload": {
    "before_sample_id": "smp_before",
    "after_sample_id": "smp_after",
    "requested_change_text": "把灰尘感去掉，保留黑色层次和轮廓。",
    "result_feedback_event_id": null,
    "causal_attribution": "unknown"
  }
}
```

Allowed `causal_attribution` in raw V0.1:

```text
user_stated
controlled
unknown
```

Do not store `llm_inferred` causal attribution in the raw ledger.

If several things changed and the user only says “好多了”, causal attribution stays `unknown`.

---

# 9. Correction event

Historical evidence must be auditable without forcing known-wrong feedback to remain active.

```json
{
  "event_type": "correction",
  "raw_text": "刚刚那句我说错了，我不是不喜欢红色，只是不喜欢这里这么大面积。",
  "target_sample_ids": [],
  "payload": {
    "target_event_ids": ["ev_old"],
    "effect": "supersede"
  }
}
```

Allowed effects:

```text
supersede
retract
clarify
```

Current effective preference must be computed from the event history; it must not treat a retracted event as active truth.

Recency by itself is not enough to supersede old evidence.

Explicit correction is stronger than time decay.

---

# 10. Tombstone / deletion semantics

Append-only auditability must not become physical undeletability.

A `tombstone` event may mark raw records or assets as unavailable for future use:

```json
{
  "event_type": "tombstone",
  "raw_text": "",
  "target_sample_ids": ["smp_x"],
  "payload": {
    "target_record_ids": ["smp_x", "ast_x"],
    "reason": "deletion_request"
  }
}
```

Hard rules:

1. Tombstoned records are excluded from retrieval, profile derivation, training/discovery, and evaluation.
2. A future implementation may physically purge sensitive payloads while preserving a non-sensitive tombstone/ID where legally and operationally appropriate.
3. The contract does not require irreversible storage.

Physical purge tooling is deferred.

---

# 11. GenerationRecord

A `GenerationRecord` preserves enough execution context to distinguish preference drift from renderer/model behavior changes.

It is execution metadata, not preference truth.

## 11.1 Minimum fields

```json
{
  "schema_version": "1",
  "generation_id": "gen_<uuid>",
  "created_at": "2026-08-12T05:20:00Z",
  "renderer": "openai-imagegen",
  "model": "opaque-model-name",
  "model_version": null,
  "task_ref": null,
  "reference_sample_ids": ["smp_ref_1"],
  "parent_generation_id": null,
  "output_sample_ids": ["smp_output_1"],
  "prompt_text": null,
  "parameters": {}
}
```

## 11.2 Required fields

- `schema_version`
- `generation_id`
- `created_at`
- `renderer`
- `model`
- `reference_sample_ids`
- `output_sample_ids`
- `parameters`

## 11.3 Prompt policy

`prompt_text` may be stored as optional execution metadata.

It must never be treated as raw personal preference evidence because prompts may contain:

- assistant guesses;
- renderer-specific syntax;
- temporary workarounds;
- negative prompts;
- inherited upstream Skill instructions.

A future renderer change may invalidate prompt syntax while leaving visible-outcome preferences valid.

## 11.4 Renderer policy

PHASE 3 records renderer/model/version metadata but does **not** define a renderer adapter framework.

That seam is sufficient for V0.1.

---

# 12. Derived artifact minimum envelope

PHASE 3 does not design profile schemas, embeddings, rule files, or retrieval indexes.

It only defines one minimum rebuildability rule:

Any durable derived artifact must identify its source raw records.

Recommended generic envelope:

```json
{
  "artifact_id": "derived_<opaque>",
  "artifact_type": "preference_profile",
  "built_at": "2026-08-12T06:00:00Z",
  "builder_version": "opaque",
  "source_record_ids": ["ev_1", "ev_2", "smp_1"],
  "content": {}
}
```

Derived artifacts may be deleted wholesale and rebuilt.

The raw contract must remain sufficient to do so.

---

# 13. Existing calibration compatibility

The current repository has `calibration/anchors.json` and currently reports `PERSONAL_CALIBRATION_PENDING` with no anchors.

PHASE 3 decision:

> `calibration/anchors.json` should not become a second independent source of raw personal truth.

When implementation begins, choose one of these compatibility strategies:

1. materialize `anchors.json` as a derived compatibility projection from `SampleRecord + EvidenceEvent`; or
2. migrate its future writes into the raw ledger and keep the file as a read-only compatibility view.

Do not maintain two manually edited preference sources of truth.

The exact migration mechanism is deferred until implementation because the file is currently empty.

---

# 14. Evaluation contamination protection

PHASE 3 protects evaluation separation with only one raw mechanism: `SampleRecord.dataset_role`.

Hard invariant:

```text
blind_eval_reserved
```

samples must not be used in derived preference profiles, exemplar selection, rule discovery, or prompt/profile tuning before their reserved blind evaluation is completed.

A future evaluation layer may create:

- fixed regression cases;
- rotating blind cases;
- production-failure cases.

Those structures are not part of this minimum raw contract.

---

# 15. Runtime precedence invariant

This is not a field; it is a mandatory interpretation rule:

```text
current explicit user instruction
>
explicit task-scoped evidence
>
explicit domain-scoped evidence
>
confirmed durable/global evidence
>
derived historical inference
```

No stored profile may override the user's current explicit request.

If the user says:

> “这次我要暖色。”

an old derived preference for cooler palettes must not block the current task.

---

# 16. Human-effort invariant

The user must not be required to fill a metadata form for every image.

Minimum human actions remain natural:

```text
喜欢
不喜欢
A 更好
这个太脏
这版好多了
刚刚那句说错了
```

The system may automatically generate:

- IDs;
- timestamps;
- hashes;
- file metadata;
- generation IDs;
- links between generated outputs.

It may derive interpretations later, but those interpretations must stay outside raw truth.

---

# 17. What is intentionally NOT in the Data Contract

The following are deliberately excluded from PHASE 3:

- final JSON Schema files;
- `schemas/` directory;
- database choice;
- SQL tables;
- vector database;
- embeddings;
- automatic clustering;
- perceptual duplicate detection;
- fixed taxonomy;
- universal `LIU VISUAL DNA` schema;
- personal preference weights;
- AI taste score as ground truth;
- automatic rule promotion;
- new `visual-distill` Skill;
- Router + multiple new visual Skills;
- final Skill topology;
- full renderer adapter interface;
- object storage integration;
- migration framework;
- multi-user support;
- multi-agent concurrent writes;
- large benchmark;
- production ingestion CLI;
- validators;
- scaffold directories.

These exclusions are intentional, not missing work.

---

# 18. Contract invariants

A future implementation must enforce all of these:

```text
DC-01 Stable logical sample ID is independent of file path.
DC-02 SHA-256 identifies exact blob equality only.
DC-03 Asset identity and sample identity are separate.
DC-04 Raw user wording is preserved verbatim when available.
DC-05 LLM interpretation never overwrites raw user evidence.
DC-06 Corrections/retractions supersede effective meaning without erasing history by default.
DC-07 Physical deletion remains possible.
DC-08 Scope is explicit or marked unspecified; one-off evidence cannot silently become global.
DC-09 Raw and derived data are separate.
DC-10 Derived artifacts point back to raw record IDs.
DC-11 Derived artifacts can be deleted and rebuilt.
DC-12 Pairwise evidence records preference ordering, not assumed causality.
DC-13 Before→After records relation, not assumed causal attribution.
DC-14 Current explicit instruction outranks historical inference.
DC-15 Blind-eval-reserved samples cannot leak into discovery.
DC-16 Renderer/model/version metadata is preserved for generated outputs.
DC-17 Prompt syntax is execution metadata, not personal taste truth.
DC-18 Existing skill-refiner remains the promotion authority for durable Skill changes.
DC-19 GitHub is not the bulk image warehouse by architectural assumption.
DC-20 The user is never required to manually fill a large metadata form.
```

---

# 19. Minimum example lifecycle

A reference image is added:

```text
AssetRecord ast_1
↓
SampleRecord smp_1
```

The user says:

```text
“喜欢这个黑色，但它很干净，不脏。”
```

Store:

```text
EvidenceEvent ev_1
raw_text preserved
scope = unspecified or domain if context is clear
```

Later another generated image appears:

```text
GenerationRecord gen_1
↓
SampleRecord smp_2
```

The user says:

```text
“参考图更好，这个太脏。”
```

Store:

```text
comparison event ev_2
smp_1 > smp_2
```

The image is revised:

```text
GenerationRecord gen_2
↓
SampleRecord smp_3
revision event ev_3
before = smp_2
after = smp_3
```

The user says:

```text
“这个好多了。”
```

Store a feedback event.

Do **not** immediately write:

```text
GLOBAL RULE: reduce grain by 40%
```

A derived profile may later hypothesize a preference for clean dark rendering. If repeated evidence becomes stable enough to change a Skill, `skill-refiner` handles that separate promotion process.

---

# 20. Catastrophic-migration test

Before implementation, apply this thought experiment:

> Assume every derived algorithm is deleted in 2027.

Delete:

- inferred profiles;
- embeddings;
- clusters;
- prompt compilers;
- retrieval indexes;
- critic weighting;
- Visual DNA summaries;
- renderer-specific compilation logic.

If the surviving records still preserve:

- every logical sample;
- exact assets and current locations;
- original user feedback;
- A/B decisions;
- Before→After relations;
- corrections/retractions;
- generation model context;
- provenance;
- blind-eval reservation;

then the Data Contract passes its primary purpose.

---

# 21. PHASE 3 exit gate

PHASE 3 is PASS only if all are true:

```text
[ ] Sample identity is independent from asset/path/hash.
[ ] Exact asset integrity has SHA-256.
[ ] Raw user feedback is preserved verbatim.
[ ] Corrections/retractions are representable.
[ ] Pairwise preference is representable without causal overclaim.
[ ] Before→After is representable without causal overclaim.
[ ] Evidence scope is representable without fixed taxonomy.
[ ] Raw and derived data are explicitly separated.
[ ] Generated outputs retain renderer/model context.
[ ] Blind evaluation reservation cannot silently leak into discovery.
[ ] Existing calibration can be migrated without creating two authorities.
[ ] Existing skill-refiner is not duplicated.
[ ] The user does not need a heavy metadata workflow.
[ ] No Skill was created.
[ ] No scaffold was created.
[ ] No production schema/validator/script was created.
[ ] No images were imported.
[ ] No architecture freeze was performed.
```

If all pass, PHASE 3 may be marked `PASS / DESIGN ONLY` and must stop before PHASE 4.

---

# 22. Final PHASE 3 decision

The smallest durable source of truth is not a Visual DNA file and not a Skill.

It is:

```text
Samples
+
Assets
+
Raw Evidence Events
+
Generation History
```

with comparison, revision, correction, and deletion semantics carried as event types.

Everything intelligent above that layer is intentionally replaceable.

That is the contract boundary PHASE 3 recommends freezing conceptually before implementation, while leaving actual file formats, JSON Schema mechanics, storage engine, and Skill topology for later phases.
