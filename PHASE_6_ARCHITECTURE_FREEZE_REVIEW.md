# LIU VISUAL SYSTEM — PHASE 6 ARCHITECTURE FREEZE REVIEW

Status: `PASS_WITH_FREEZE_CLARIFICATIONS`
Date: `2026-08-12`
Branch: `phase-6-architecture-freeze-review-20260812`
Base: PHASE 5 HEAD `a620f3baefbcde68a8981a1db2c8f7457101bc88`

Purpose: perform the final pre-freeze attack across PHASE 3 Data Contract, PHASE 4 Architecture Proposal, and PHASE 5 accepted ADRs. This review is allowed to freeze architecture only if no unresolved structural blocker would force later relabeling, duplicate preference authority, privacy leakage, evaluation contamination, or a redesign of the four raw record families.

This phase does **not** create production code, schemas, validators, a data store, asset storage, Skills, embeddings, a benchmark implementation, or a Pilot dataset.

---

# 1. Inputs under review

Authoritative inputs reviewed together:

```text
PHASE_3_MIN_DATA_CONTRACT.md
PHASE_3_FIELD_MATRIX.md
PHASE_3_CONTRACT_REVIEW.md

PHASE_4_ARCHITECTURE_PROPOSAL.md
PHASE_4_AUTHORITY_BOUNDARY_MATRIX.md
PHASE_4_ARCHITECTURE_REVIEW.md

PHASE_5_ADR_INDEX.md
PHASE_5_ADR_REVIEW.md

docs/adr/ADR-001 ... ADR-008
```

The review also checked current repository behavior relevant to the freeze:

- `AESTHETIC_SKILL_DESIGN_CHARTER.md`;
- `skills/personal-aesthetic-critic/SKILL.md`;
- `calibration/README.md` and current empty `anchors.json`;
- `skills/skill-refiner/SKILL.md` and its integration policy.

---

# 2. Freeze question

The architecture is eligible to freeze only if both are true:

> If every derived algorithm is replaced later, the user does not need to relabel the visual history.

and

> The V0.1 architecture does not secretly require infrastructure that has been deferred.

Result: **both conditions pass**, subject to the freeze clarifications in this review.

---

# 3. Structural attack results

## F6-01 — Four raw record families remain sufficient

Attack:

Could runtime, calibration, evaluation, or Skill evolution require a fifth raw source-of-truth family?

Reviewed candidate additions:

```text
VisualDNARecord
ProfileRecord
CriticRecord
RuleRecord
CalibrationAnchorRecord
EvalRecord
```

Decision:

None belongs in raw personal preference truth.

The frozen raw families remain:

```text
SampleRecord
AssetRecord
EvidenceEvent
GenerationRecord
```

Profiles/calibration/evals/rules remain derived or external workflow state.

Verdict: `PASS`.

---

## F6-02 — Source-of-truth graph has no unresolved dual authority

Attack:

Check whether `anchors.json`, critic output, Skill rules, prompt history, or derived profiles can compete with EvidenceEvent.

Decision:

No dual authority is allowed.

Frozen authority chain:

```text
Direct user evidence
    ↓
Raw EvidenceEvent
    ↓
Derived effective/projection views
    ↓
Runtime context / compatibility calibration / evaluation
```

Durable Skill changes use a separate authority:

```text
selected evidence IDs
    ↓
skill-refiner
    ↓
evaluation + Git review
```

Verdict: `PASS`.

---

## F6-03 — Imported historical evidence needs a stricter fidelity boundary

Attack:

ADR-008 allows "faithfully imported historical user evidence with traceable origin". Without a freeze clarification, a summary from assistant memory could be imported as if it were direct user wording.

Freeze clarification:

`imported_user_evidence` may enter the raw preference ledger only when the importer can preserve either:

1. the original user wording; or
2. an original structured user action such as an explicit A/B selection,

and retain a traceable source reference when available.

The following must **not** enter as raw imported user evidence:

- assistant-created memories/summaries;
- inferred preference descriptions;
- paraphrased profile notes whose original user evidence is unavailable;
- AI-written labels reconstructed from historical behavior.

Those may be derived notes only.

Verdict: `PASS WITH FREEZE CLARIFICATION`.

---

## F6-04 — Evidence scope can itself become a hidden inference channel

Attack:

A direct user sentence may be raw, but assigning it an overly broad `domain` or `global_explicit` scope could still contaminate preference memory.

Freeze clarification:

- `global_explicit` requires explicit durable/global wording from the user;
- `domain` may be assigned when the current task/domain context is objectively clear;
- if scope is ambiguous, record `unspecified`;
- an LLM may later infer broader scope only in the derived layer.

Verdict: `PASS WITH FREEZE CLARIFICATION`.

---

## F6-05 — "Current explicit user instruction wins" must not override non-preference invariants

Attack:

ADR-005 places current explicit user instruction at the top of runtime preference precedence. Read literally, this could conflict with privacy, data integrity, safety, evaluation isolation, or correctness constraints.

Freeze clarification:

The precedence:

```text
current explicit instruction
>
current task constraints
>
historical preference
```

applies **inside the personalization/aesthetic preference layer only**.

It does not bypass:

- system/safety requirements;
- privacy/deletion policy;
- raw-data integrity rules;
- blind-eval isolation;
- deterministic correctness requirements;
- repository security/governance constraints.

Verdict: `PASS WITH FREEZE CLARIFICATION`.

---

## F6-06 — Blind-eval isolation must be transitive, not sample-only

Attack:

`dataset_role = blind_eval_reserved` exists on SampleRecord. Leakage could still occur indirectly if an EvidenceEvent, GenerationRecord, or derived artifact based on a reserved sample enters discovery or Skill refinement.

Freeze clarification:

For V0.1, the contamination barrier is **transitive across the evaluation case**.

Before and after the designated blind evaluation, do not use for discovery/tuning:

- the reserved SampleRecord;
- direct preference EvidenceEvents whose comparison/feedback targets depend on the reserved case;
- generated outputs designated as part of that blind case;
- derived summaries or exemplar roles produced from that blind case;
- those event IDs as `skill-refiner` evidence.

When a generated candidate is part of a designated blind evaluation case, it must inherit evaluation reservation for the purposes of that case even if it would otherwise be a production sample.

This does not require a new raw record family. It is an Eval Isolation Guard rule using existing IDs and dataset roles/eval manifests.

Verdict: `PASS WITH FREEZE CLARIFICATION`.

---

## F6-07 — Public `calibration/anchors.json` creates a privacy trap if materialized naively

Attack:

ADR-004 makes calibration a derived compatibility view, while ADR-001 keeps canonical personal evidence private. The repository is public. A future implementation that writes private personal anchors/reasons/paths into the tracked public `calibration/anchors.json` would leak personal data.

Freeze clarification:

The tracked public calibration file must remain only a non-sensitive template/example/default unless its contents are explicitly safe for publication.

Private personal calibration projections must be materialized through a **private runtime/workspace overlay or another private resolved input**, never committed to the public repository by default.

Until the existing critic can consume such a privacy-safe projection, formal private `personal_fit` must remain `null` rather than copying private anchors into public Git.

Any change to the critic's calibration input path is an implementation/integration change and must preserve ADR-004 authority semantics.

Verdict: `PASS WITH HARD FREEZE CLARIFICATION`.

---

## F6-08 — Cross-runtime access is not solved by the private local store

Attack:

The project goal eventually includes Codex + ChatGPT cooperation. A private local file root is not automatically visible to every runtime.

Decision:

This is a real V0.1 limitation, but not a Data Contract blocker.

Freeze boundary:

- canonical raw identity is independent of host;
- runtimes must expose truthful `resolvable / actually_inspected` state;
- a host that cannot access private memory falls back to current explicit input/current-task references;
- no public-Git workaround is allowed merely to obtain cross-runtime access;
- cross-runtime synchronization/bridge is a future deployment capability, not a reason to redesign the raw model.

Pilot may initially operate through one authoritative writer/runtime path.

A claim of "ChatGPT + Codex shared persistent visual memory" is not allowed until an actual private bridge/synchronization path exists.

Verdict: `ACCEPTED V0.1 LIMITATION / NOT FREEZE BLOCKER`.

---

## F6-09 — Raw-store durability/backup was under-specified

Attack:

The project says raw user evidence is irreplaceable, yet ADR-001 can be implemented as one local directory with no recovery copy.

Freeze clarification:

Before ingesting **non-disposable real personal evidence at Pilot scale**, the implementation must provide a recoverable backup/export path for:

```text
raw structured records
+
Asset Vault bytes required by those records
```

The exact technology is intentionally not frozen. Acceptable examples may include a second durable local copy, encrypted private sync, private archive/export, or later database/object-store backup.

The architecture freezes the durability requirement, not a vendor.

Verdict: `PASS WITH PRE-PILOT GATE`.

---

## F6-10 — Deletion semantics cannot stop at a tombstone when real private data exists

Attack:

PHASE 3 allows tombstone events and defers physical purge tooling. A tombstone alone is not a complete response when the user actually requires data removal.

Freeze clarification:

The Pilot implementation does not need a sophisticated deletion service, but it must have a documented deterministic way to:

1. mark affected IDs unavailable immediately;
2. physically remove requested raw sensitive payloads/assets when required;
3. rebuild/delete derived artifacts that contain those records;
4. retain only non-sensitive tombstone/audit metadata when appropriate.

Verdict: `PASS WITH PRE-PILOT GATE`.

---

## F6-11 — Persistence failure must not be reported as successful learning

Attack:

The current task can still use an explicit correction even if the raw store write fails.

Freeze clarification:

If Feedback Capture fails to persist an EvidenceEvent:

- the current response/task may still use the user's explicit instruction;
- the system must not claim that the preference was saved/learned persistently;
- no derived profile or Skill-refiner bridge may treat the failed write as durable evidence.

Verdict: `PASS`.

---

## F6-12 — Asset durability vs source URL

Attack:

A provenance URL can disappear. If the system stores only a web URL, the exemplar may be lost even though the preference event survives.

Freeze clarification:

A sample intended to become a durable visual exemplar should have inspectable bytes preserved in the Asset Vault when legally/operationally appropriate, with SHA-256 recorded. A source URL alone is provenance, not a durable asset guarantee.

If bytes cannot be preserved, the system may retain historical evidence but must treat future visual resolvability as uncertain.

Verdict: `PASS`.

---

## F6-13 — Existing critic must not become a mandatory architecture choke point

Attack:

The critic currently supports a limited category set.

Decision:

The critic remains optional/reusable by supported task. Unsupported domains may use direct user comparison and task-specific evaluation.

No fake category assignment merely to produce a formal score.

Verdict: `PASS`.

---

## F6-14 — Derived profile edits cannot become an informal bypass around ADR-006

Attack:

A human/LLM could hand-edit a derived profile and effectively create a durable rule without Skill Refiner.

Decision:

Derived profiles remain cache. Manual edits can affect only a temporary/derived artifact and are erased on rebuild. If the edit reflects a real user correction, the evidence must be captured in the raw ledger. If it reflects a production Skill procedure change, it must go through `skill-refiner`.

Verdict: `PASS`.

---

## F6-15 — Architecture component names must remain logical boundaries

Attack:

PHASE 4 names many logical components. An implementer could create a class/service/agent for each and recreate over-engineering.

Freeze clarification:

V0.1 implementation must prefer a small modular package / deterministic scripts. Component names describe authority boundaries only.

No microservices, queues, agent fleet, workflow engine, or vector infrastructure is implied by the freeze.

Verdict: `PASS`.

---

# 4. Contradiction resolution / document precedence

Several earlier documents contain superseded wording. Freeze must avoid ambiguity.

The controlling order for V0.1 architecture is:

```text
1. ARCHITECTURE_V0.1_FROZEN.md
2. accepted ADRs, as narrowed by PHASE_6 freeze clarifications
3. PHASE_6_ARCHITECTURE_FREEZE_REVIEW.md
4. PHASE_3_CONTRACT_REVIEW.md for PHASE 3 ambiguities
5. PHASE_4_ARCHITECTURE_REVIEW.md for PHASE 4 ambiguities
6. earlier proposal/design narrative
```

Historical documents are not rewritten to hide earlier decisions.

Specific resolved conflict:

- PHASE 3 early draft allowed `source_kind = user/system/import`.
- PHASE 3 self-review + ADR-008 narrowed raw preference evidence to direct user / faithful imported-user evidence.
- V0.1 freeze adopts the narrowed rule.

---

# 5. Freeze-blocker test

A finding is a blocker if fixing it would require one of:

- a fifth raw record family;
- changing stable identity semantics;
- making derived intelligence canonical;
- creating another preference authority;
- abandoning existing routing/critic/refiner boundaries;
- migrating user labels before Pilot;
- selecting major infrastructure solely to make the architecture coherent.

No finding requires any of those.

Therefore no structural freeze blocker remains.

---

# 6. Catastrophic migration simulation

Assume after the Pilot the following all change:

```text
flat files → database
local vault → private cloud/object store
simple metadata retrieval → embeddings
current critic → new evaluator
current renderer → future renderer
host integration → plugin/tool/native memory
profile builder → new algorithm
VisualContextPack shape → new format
```

Required work:

```text
preserve/copy stable raw IDs and fields
move asset bytes and rewrite locators
rebuild derived artifacts
rebuild calibration compatibility view
rebuild retrieval/eval indexes
adapt host integration
```

Not required:

```text
relabel user likes/dislikes
repeat A/B decisions
reconstruct original rejection wording
reconstruct revision history
reconstruct corrections/retractions
rename logical sample identity because storage changed
```

Result: `PASS`.

---

# 7. Over-engineering regression test

Frozen architecture does **not** require:

```text
new mega visual Skill
new router family
new critic
new rule lifecycle
trained Preference Model
embedding database
object-store vendor
microservices
message queue
multi-agent write merge
fixed taxonomy
universal Visual DNA
large benchmark
```

Result: `PASS`.

---

# 8. Privacy / evidence-quality test

Required protections after freeze:

```text
private raw store
private bulk asset storage by default
explicit user evidence only
no assistant-memory summaries as imported raw truth
public anchors cannot receive private calibration by default
physical deletion path before real Pilot data scales
backup/recovery path before real Pilot data scales
```

Result: `PASS WITH IMPLEMENTATION GATES`.

---

# 9. Evaluation-validity test

Required protections after freeze:

```text
sticky V0.1 blind-eval reservation
transitive quarantine of associated evidence/output/derived artifacts
no reuse for skill-refiner evidence
production regression cases kept conceptually separate from blind holdout
critic diagnostics separate from personal preference
```

Result: `PASS`.

---

# 10. PHASE 6 verdict

Final verdict:

```text
PHASE 6 — PASS WITH FREEZE CLARIFICATIONS
```

The architecture may now be frozen as V0.1 because remaining limitations are operational/reversible and do not require redesigning the durable personal-evidence model.

Freeze is valid only together with the pre-implementation gates documented separately.

---

# 11. What this PASS does not authorize

PHASE 6 PASS authorizes creation of the **freeze record only**.

It does not in this phase authorize:

- production scaffold implementation;
- JSON schemas;
- validators;
- private data-root creation;
- image ingestion;
- Pilot data collection;
- modifications to existing visual Skills;
- embeddings/vector DB;
- preference-model training.

Those begin only in the next implementation phase after the freeze record is committed and verified.
