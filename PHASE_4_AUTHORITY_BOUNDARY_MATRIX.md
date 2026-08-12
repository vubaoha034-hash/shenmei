# LIU VISUAL SYSTEM — PHASE 4 AUTHORITY & BOUNDARY MATRIX

Status: `PROPOSED / NOT_FROZEN`

Date: `2026-08-12`

Purpose: make ownership, read/write boundaries, and prohibited authority transfers explicit before any implementation exists.

This document is a companion to `PHASE_4_ARCHITECTURE_PROPOSAL.md`.

---

# 1. Authority map

| Concern | Authoritative source | Derived/secondary source | Must never become authority |
|---|---|---|---|
| current task intent | current explicit user instruction | task parser/context pack | historical profile |
| personal visual preference evidence | direct/imported-user `EvidenceEvent` | effective evidence view / preference projection | AI critic output, prompt text, LLM summary |
| logical sample identity | `SampleRecord.sample_id` | indexes/views | file path, URL, SHA-256 |
| exact binary identity | `AssetRecord.asset_id + sha256` | locator/index | filename |
| asset availability | current asset locator/resolution status | cache | sample preference status |
| generation provenance | `GenerationRecord` | debugging views | assistant memory alone |
| personal-fit calibration view | raw evidence projected into compatibility anchors | `calibration/anchors.json` view | independently hand-maintained parallel truth |
| technical/professional visual evaluation | existing critic + deterministic correctness checks | evaluation artifacts | raw personal evidence |
| durable Skill changes | Git-reviewed existing `skill-refiner` flow | candidate/eval ledgers | raw feedback directly editing Skill |
| evaluation isolation | raw dataset role + eval governance | eval manifests | derived profile builder |

---

# 2. Component boundary matrix

| Component | Reads | Writes | Must not write | Failure effect |
|---|---|---|---|---|
| Raw Ingestor | asset bytes, explicit source metadata | SampleRecord, AssetRecord | EvidenceEvent inference, profile | import fails; no preference corruption |
| Feedback Capture | direct user utterance/action | EvidenceEvent | inferred rule, critic score | evidence not recorded; existing raw data intact |
| Generation Gateway | task execution request, refs | GenerationRecord, output Sample/Asset | personal EvidenceEvent | generation/logging failure isolated |
| Effective Evidence Projector | EvidenceEvents | derived effective view | raw evidence | stale/absent profile only |
| Preference Projection Builder | effective evidence, Samples | derived scoped profiles | raw evidence, Skill | personalization degrades gracefully |
| Exemplar Selector | Samples, derived roles, resolvability | ephemeral selection / optional derived index | sample label truth | fallback to explicit refs/manual selection |
| Calibration Adapter | eligible raw evidence / samples | derived anchors compatibility view | raw evidence | critic personal_fit may remain null |
| Task Intent Resolver | current task | ephemeral task intent | durable preference | current task still available manually |
| Visual Context Assembler | task intent, derived profile, exemplars | ephemeral VisualContextPack | raw preference | generation can run with explicit task only |
| Existing Repo Router | user task, repository routing docs | route choice | preference ledger | ordinary routing fallback |
| Existing Visual Skill | route input + context pack | prompt/execution intent | raw evidence, promoted memory | output quality issue only |
| Personal Aesthetic Critic | image, brief, calibration view | evaluation artifact | raw personal evidence | no raw learning consequence |
| Eval Isolation Guard | dataset roles / eval state | allow/block decision | rewrite dataset history | eval invalidated/blocked |
| Skill Refiner Bridge | selected evidence IDs | skill-refiner observation/candidate state | raw visual ledger | no Skill improvement, raw evidence preserved |

---

# 3. Read-path rules

## 3.1 Runtime generation may read

```text
current task
confirmed effective evidence
relevant derived profiles
small exemplar set
existing visual Skill
```

It should not read the entire raw evidence archive by default.

## 3.2 Derived builders may read

```text
raw SampleRecords
raw EvidenceEvents
GenerationRecords where relevant
asset metadata
```

They must honor:

- tombstones;
- corrections/retractions;
- dataset-role isolation;
- evidence scope;
- source kind.

## 3.3 Critic may read

```text
actual inspectable image
brief/current task
professional rubric
calibration compatibility projection
```

It should not automatically use unconfirmed derived preference hypotheses as official personal-fit anchors.

## 3.4 Skill Refiner may read

Only evidence intentionally bridged for a specific learning claim.

It should not scan every personal EvidenceEvent and autonomously promote rules.

---

# 4. Write-path rules

## 4.1 Direct user evidence path

Only the feedback-capture path can create raw preference EvidenceEvents.

Faithful historical imports are permitted but must retain provenance and be distinguishable as imported user evidence.

## 4.2 AI interpretation path

AI may write only derived/evaluation outputs.

Examples:

```text
"likely preference: clean dark texture"
"possible domain: sci-fi"
"retrieval relevance: high"
```

These cannot overwrite or mutate direct user evidence.

## 4.3 Skill mutation path

No component can write permanent Skill changes except through the existing evidence-gated `skill-refiner` + Git review path.

## 4.4 Asset path change

Asset locator may change operationally while asset identity remains stable if bytes/hash are unchanged.

A binary change creates a new AssetRecord.

---

# 5. Preference-scope boundary

The runtime must preserve at least these semantic layers:

```text
current task instruction
explicit task evidence
explicit domain evidence
explicit durable/global evidence
derived inference
```

A domain label may be free-form/configurable.

No fixed ontology is required by the architecture.

A derived system may later map multiple labels to a taxonomy, but raw events remain unchanged.

---

# 6. Evidence-confidence boundary

Raw direct user evidence does not need an AI-generated confidence score.

Confidence belongs to derived interpretation.

Examples:

```text
Raw:
用户：“这个红色太多了。”

Derived interpretation A:
possible preference = lower red area
confidence = medium
scope = task/domain hypothesis

Derived interpretation B:
user dislikes red globally
confidence = low / unsupported
```

The architecture must allow interpretation B to be discarded without modifying the raw event.

---

# 7. Causality boundary

## Pairwise

Raw:

```text
A > B
```

Allowed.

Derived:

```text
A may win because of cleaner texture
```

Possible hypothesis only.

## Revision

Raw:

```text
user requested changes X/Y/Z
before → after
user later approves after
```

Allowed.

Derived:

```text
Y caused the improvement
```

Not justified unless user-stated or controlled.

---

# 8. Calibration boundary

The current critic expects stable approved/neutral/rejected/reference anchors.

Architecture proposal:

```text
raw Sample + direct Evidence
        ↓
eligibility/projection
        ↓
calibration compatibility view
        ↓
existing critic
```

This avoids:

```text
raw new ledger
+
manual anchors.json
```

becoming two divergent personal-preference authorities.

The exact projection rules are a PHASE 5/implementation decision.

---

# 9. Retrieval boundary

Exemplar retrieval chooses what to show the model; it does not decide what the user likes.

Therefore a retrieved sample can be:

```text
relevant but not approved
approved but not relevant
rejected but useful as negative exemplar
unavailable in current host
```

Retrieval ranking is derived and replaceable.

A retrieval error must not change raw labels/evidence.

---

# 10. Runtime accessibility boundary

Asset authority and host accessibility are separate.

A sample may remain valid evidence even when:

- ChatGPT cannot access the local file;
- Codex cloud cannot resolve a desktop path;
- a remote URL is temporarily unavailable.

The runtime must report availability truthfully.

No component may infer:

```text
not resolvable == no longer preferred
```

---

# 11. Evaluation boundary

Professional aesthetic score and personal preference are independent signals.

Four valid outcomes include:

```text
professional high / user likes
professional high / user dislikes
professional low / user likes
professional low / user dislikes
```

The architecture must preserve this possibility.

A critic score cannot be silently converted into a preference event.

---

# 12. Error-severity boundary

## Catastrophic errors

These require hard architectural prevention:

- rewriting raw user feedback;
- path-as-sample identity;
- blind-eval leakage;
- critic becoming personal truth;
- current user instruction overridden by history;
- derived profile written back as raw evidence;
- automatic Skill promotion from one-off feedback.

## Recoverable errors

These should not justify heavy infrastructure:

- retrieval miss;
- stale derived profile;
- unavailable exemplar;
- imperfect domain label;
- no embedding index;
- missing personal-fit score;
- delayed profile rebuild.

---

# 13. Implementation topology constraint

The logical boundaries in this document do not imply separate services.

Acceptable initial implementation examples:

```text
one repository package
+ a few deterministic scripts
+ raw/derived folders
+ existing Skills
```

or another small local architecture.

Unacceptable justification:

> “There are 11 logical components, therefore we need 11 services/classes/agents.”

The purpose of the boundary matrix is authority safety, not topology inflation.

---

# 14. Boundary gate

Before PHASE 5, verify:

```text
[ ] every durable truth has one authority
[ ] AI components cannot write direct-user preference truth
[ ] critic cannot promote itself into preference authority
[ ] raw ledger is independent of skill-refiner state
[ ] skill-refiner remains one promotion authority
[ ] current instruction precedence is explicit
[ ] retrieval is advisory
[ ] calibration is a projection, not duplicate truth
[ ] runtime availability does not alter preference truth
[ ] logical components do not imply microservices
```

If any fails, Architecture Proposal requires rework before ADRs.
