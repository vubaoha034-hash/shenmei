# LIU VISUAL SYSTEM — PHASE 3 CONTRACT SELF-REVIEW

Status: `PASS / DESIGN_ONLY`

Date: `2026-08-12`

Authority: this review is part of the PHASE 3 contract package. Where a clarification below conflicts with an earlier sentence in `PHASE_3_MIN_DATA_CONTRACT.md` or `PHASE_3_FIELD_MATRIX.md`, **this review controls** until the later implementation phase converts the design into formal schemas.

No Skill, schema file, script, scaffold, image import, database, vector index, renderer adapter, or architecture freeze is created by this phase.

---

# 1. Self-review purpose

After the first Data Contract draft was written, the contract itself was red-teamed against the PHASE 2 risks.

Four ambiguities were found. None requires changing the four-family model, but all should be resolved before implementation.

---

# 2. Clarification C-01 — production feedback is valid discovery evidence

Earlier wording described `dataset_role = production` mainly as a future regression source.

That is too narrow.

Authoritative semantics:

```text
discovery
    reference/sample may be used to derive preference knowledge

blind_eval_reserved
    sample is isolated from discovery before/during its reserved blind evaluation

production
    sample was created or used in real work;
    direct user feedback on it MAY contribute to preference discovery;
    it may also later become a regression case

unassigned
    no discovery/evaluation authorization has been decided yet
```

This is important because the user's real corrections during normal visual work are expected to be some of the highest-value preference evidence.

`production` therefore does not mean “excluded from learning”.

---

# 3. Clarification C-02 — the raw EvidenceEvent ledger is for direct user evidence, not AI critic output

The first draft allowed `source_kind = system` while warning that system output must not become personal preference truth.

That is an unnecessary contamination surface.

Authoritative V0.1 rule:

Allowed raw visual preference evidence sources are only:

```text
user
imported_user_evidence
```

Definitions:

- `user`: direct current user utterance/action.
- `imported_user_evidence`: faithfully imported historical user evidence whose origin can be traced.

Do not put the following into the raw personal EvidenceEvent ledger:

- AI critic judgments;
- generic aesthetic scores;
- LLM summaries;
- system-generated taste interpretations;
- candidate rules;
- automated cluster labels.

Those belong in derived/evaluation systems or the existing `skill-refiner` workflow as appropriate.

This directly protects PHASE 2 risks `R-005`, `R-027`, `R-029`, and `R-046`.

---

# 4. Clarification C-03 — Revision EvidenceEvent is user-directed; automated lineage belongs in GenerationRecord

The V0.1 `revision` event should only be created when there is direct user revision evidence, for example:

```text
“把灰尘感去掉，保留黑色层次。”
```

Therefore, for a raw `revision` EvidenceEvent:

```text
requested_change_text
```

remains required and must preserve the user's actual request.

If an assistant/renderer creates another version without a direct user revision instruction, do **not** invent a user revision event.

Instead record lineage through:

```text
GenerationRecord.parent_generation_id
GenerationRecord.output_sample_ids
```

If the user later says:

```text
“这个好多了。”
```

store that as a separate user `feedback` event against the new sample.

This prevents assistant-generated edit plans from being mistaken for user taste evidence.

---

# 5. Clarification C-04 — asset identity is immutable; locator is operationally mutable

The contract separates logical identity from physical storage.

Authoritative rule:

The following AssetRecord identity facts are stable once accepted:

```text
asset_id
sample_id
sha256
asset_relation
created_at
```

The following is operational storage metadata and may change when a file moves:

```text
locator_kind
locator
```

Changing only the locator does not create a new logical sample and does not change the exact blob identity if SHA-256 is unchanged.

If the bytes change, create a new `AssetRecord` with a new `asset_id` and new SHA-256.

This protects against path-as-identity while avoiding an unnecessary asset-location event subsystem in V0.1.

---

# 6. Append-only boundary clarification

“Append-only” applies strictly to the user's personal evidence history:

```text
EvidenceEvent
```

User feedback should not be silently rewritten.

Corrections are new events with:

```text
supersede
retract
clarify
```

`SampleRecord` and `AssetRecord` contain identity/provenance/infrastructure facts and may require deterministic metadata correction during implementation. Such correction must preserve stable IDs and must never rewrite the user's original EvidenceEvent text.

This avoids turning the entire storage system into an event-sourcing framework merely for architectural purity.

---

# 7. Blind evaluation rule clarification

`blind_eval_reserved` is a contamination barrier, not ML training vocabulary.

Minimum V0.1 rule:

> A sample reserved for blind evaluation must not be used to construct preference profiles, exemplar retrieval sets, candidate global preferences, or prompt/profile tuning before the relevant blind evaluation is locked.

PHASE 3 does not define the later benchmark/eval case file format.

That belongs to a later phase.

---

# 8. Compatibility conclusion

## `calibration/anchors.json`

Current repository state has no personal anchors.

Decision remains:

```text
future compatibility projection
NOT second manual raw source of truth
```

Because it is currently empty, there is no expensive migration burden yet.

## `skill-refiner`

Decision remains:

```text
visual raw evidence IDs
→ may be cited by skill-refiner
→ candidate/evaluation/promotion happens there
```

The dependency must never be reversed.

Raw visual evidence must remain intelligible even if `.skill-evolution/` is deleted or rebuilt.

---

# 9. PHASE 3 contract package

The complete PHASE 3 design consists of:

```text
PHASE_3_MIN_DATA_CONTRACT.md
PHASE_3_FIELD_MATRIX.md
PHASE_3_CONTRACT_REVIEW.md
```

The first document defines the minimum model.

The second prevents unnecessary field growth.

This review resolves post-draft ambiguities and records the final phase gate.

---

# 10. Final record-family decision

PHASE 3 still concludes that only four durable raw record families are necessary:

```text
SampleRecord
AssetRecord
EvidenceEvent
GenerationRecord
```

There is no fifth raw “Visual DNA”, “Profile”, “Rule”, “Score”, “Embedding”, or “Critic” record family.

Those remain derived or external workflow state.

---

# 11. PHASE 3 exit-gate verification

| Gate | Result |
|---|---|
| sample identity independent of file path/hash | PASS |
| sample vs asset identity separated | PASS |
| exact blob SHA-256 represented | PASS |
| verbatim direct user evidence preserved | PASS |
| AI interpretation excluded from raw preference truth | PASS |
| corrections/retractions represented | PASS |
| A/B ordering represented without causal overclaim | PASS |
| Before→After represented without causal overclaim | PASS |
| automated revision lineage does not impersonate user evidence | PASS |
| scope does not require fixed taxonomy | PASS |
| raw and derived layers separated | PASS |
| renderer/model execution context represented | PASS |
| prompt syntax not treated as preference truth | PASS |
| blind-eval contamination barrier represented | PASS |
| existing calibration does not become duplicate authority | PASS |
| existing skill-refiner is not duplicated | PASS |
| heavy user metadata forms avoided | PASS |
| no Skill created | PASS |
| no scaffold created | PASS |
| no formal schemas/validators/scripts created | PASS |
| no images imported | PASS |
| no architecture freeze performed | PASS |

PHASE 3 verdict:

```text
PASS / DESIGN ONLY
```

Stop here.

Do not begin PHASE 4 in this phase.
