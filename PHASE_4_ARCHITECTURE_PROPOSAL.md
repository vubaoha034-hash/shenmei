# LIU VISUAL SYSTEM — PHASE 4 ARCHITECTURE PROPOSAL

Status: `PROPOSED / NOT_FROZEN`

Date: `2026-08-12`

Branch: `phase-4-architecture-proposal-20260812`

Base: PHASE 3 `PASS / DESIGN ONLY`

Scope: define the **overall logical architecture** that sits above the PHASE 3 minimum Data Contract while preserving the PHASE 2 anti-overengineering decisions.

This phase proposes boundaries and flows. It does **not** create Skills, production schemas, scripts, scaffold directories, a database, asset storage infrastructure, embeddings, a trained preference model, or an architecture freeze.

---

# 0. Executive decision

The recommended architecture is a **data-first modular monolith**, not a microservice system and not a new family of visual Skills.

“Component” in this document means a **responsibility boundary**, not a separate server/process.

The architecture has five logical planes:

```text
1. RAW EVIDENCE PLANE
   SampleRecord / AssetRecord / EvidenceEvent / GenerationRecord

2. DERIVED INTELLIGENCE PLANE
   effective evidence view / preference projections / exemplar selection

3. RUNTIME CONTEXT PLANE
   current task + retrieved evidence → bounded VisualContextPack

4. EXECUTION & EVALUATION PLANE
   existing visual route / renderer / existing personal-aesthetic-critic

5. LEARNING & GOVERNANCE PLANE
   existing skill-refiner / blind-eval isolation / Git-reviewed promotion
```

The central design principle is:

> **The architecture may get smarter above the raw layer without acquiring the authority to rewrite what the user actually said, liked, rejected, compared, revised, or corrected.**

The architecture deliberately reuses existing repository assets:

- root routing in `START_HERE.md` / `AGENTS.md`;
- existing visual Skills;
- `personal-aesthetic-critic` for technical/professional/task evaluation;
- `calibration/anchors.json` only as a future compatibility projection;
- `skill-refiner` as the single promotion authority for durable Skill changes.

It does **not** create:

- a new mega `$liu-visual-director` Skill;
- Router + five new visual Skills;
- a second visual rule-lifecycle engine;
- a universal Visual DNA truth file;
- automatic preference-model training.

---

# 1. Architecture goals

The architecture must optimize for the following outcomes.

## G-01 — Preserve irreplaceable personal evidence

The user's original visual judgments must survive changes in:

- model;
- renderer;
- prompt language;
- taxonomy;
- Skill topology;
- retrieval strategy;
- scoring system;
- profile-building algorithm.

## G-02 — Make derived intelligence replaceable

A future implementation must be free to rebuild or delete:

- profiles;
- summaries;
- embeddings;
- clusters;
- exemplar rankings;
- Visual DNA hypotheses;
- context-pack compilation logic.

## G-03 — Keep current user intent sovereign

Historical preference exists to assist the current task, not to override it.

## G-04 — Learn from real work with low human burden

The system should learn primarily from natural user behavior:

```text
喜欢 / 不喜欢
A 更好
这里太脏
这版好多了
刚才我说错了
```

not from mandatory metadata forms.

## G-05 — Reuse existing repository capabilities

New architecture must not duplicate mature repository functions merely to make LIU VISUAL SYSTEM look self-contained.

## G-06 — Fail safely

A failure in profile derivation, retrieval, critic scoring, or Skill refinement must not corrupt raw evidence or silently rewrite preference truth.

---

# 2. Non-goals

PHASE 4 explicitly does not optimize for:

- 10,000+ sample runtime performance;
- multi-user productization;
- real-time distributed systems;
- multi-agent concurrent ledger merging;
- automatic model training;
- autonomous Skill mutation;
- universal object-store support;
- mathematically perfect preference inference;
- full causal inference from natural Before→After revisions.

Those are not required to make the first useful system correct.

---

# 3. Architecture overview

```text
                         CURRENT USER REQUEST
                                │
                                ▼
                    ┌────────────────────────┐
                    │ Existing Repo Routing  │
                    │ START_HERE / AGENTS    │
                    └────────────┬───────────┘
                                 │
                                 │ current explicit constraints
                                 ▼
                    ┌────────────────────────┐
                    │ Context Orchestrator   │
                    │      (logical)         │
                    └───────┬───────┬────────┘
                            │       │
                 derived ctx│       │task intent
                            │       │
                            ▼       ▼
                ┌──────────────────────────────┐
                │       VisualContextPack      │
                │ bounded, ephemeral, cited    │
                └──────────────┬───────────────┘
                               │
                               ▼
                 ┌───────────────────────────┐
                 │ Existing Visual Skill /   │
                 │ Prompt Compiler / Route   │
                 └─────────────┬─────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Generation Gateway   │
                    │ renderer + metadata  │
                    └──────────┬───────────┘
                               │
                  records gen  │  outputs
                               ▼
                    ┌──────────────────────┐
                    │  Sample + Asset      │
                    │ GenerationRecord     │
                    └──────────┬───────────┘
                               │
             ┌─────────────────┴─────────────────┐
             │                                   │
             ▼                                   ▼
┌────────────────────────┐           ┌─────────────────────────┐
│ personal-aesthetic-    │           │ Direct User Feedback    │
│ critic (diagnostic)    │           │ / A-B / Revision        │
└────────────┬───────────┘           └────────────┬────────────┘
             │ derived/eval                       │ raw truth
             ▼                                    ▼
      evaluation artifacts               ┌──────────────────────┐
                                         │ EvidenceEvent Ledger │
                                         └──────────┬───────────┘
                                                    │
                                                    ▼
                                          ┌─────────────────────┐
                                          │ Effective Evidence  │
                                          │     Projector       │
                                          └─────────┬───────────┘
                                                    │
                                      ┌─────────────┴──────────────┐
                                      │                            │
                                      ▼                            ▼
                             Preference Projections       Exemplar Selector
                                      │                            │
                                      └────────────┬───────────────┘
                                                   │
                                                   ▼
                                           next VisualContextPack

Repeated stable evidence only:

EvidenceEvent IDs
      │
      ▼
existing skill-refiner
      │
 candidate → eval → Git review
      │
      ▼
existing Skill / repo rule update
```

---

# 4. Plane A — Raw Evidence Plane

PHASE 3 is authoritative here.

The raw plane contains only:

```text
SampleRecord
AssetRecord
EvidenceEvent
GenerationRecord
```

## Responsibilities

- preserve stable logical sample identity;
- preserve exact asset identity and current location;
- preserve direct user evidence verbatim;
- preserve A/B relations;
- preserve user-directed Before→After relations;
- preserve correction/retraction semantics;
- preserve generated-output renderer/model lineage;
- preserve blind-eval reservation.

## Must not do

The raw plane must not:

- infer personal taste;
- compute visual scores;
- create global rules;
- write Skill instructions;
- classify style families automatically;
- decide what the user “really meant” beyond direct structured facts.

---

# 5. Plane B — Derived Intelligence Plane

This plane converts raw evidence into rebuildable assistance.

It contains four logical components.

## B1 — Effective Evidence Projector

Purpose:

> Convert append-oriented user EvidenceEvents into a current effective view without rewriting history.

Responsibilities:

- apply `supersede`, `retract`, and `clarify` semantics;
- exclude tombstoned evidence;
- expose event chronology;
- separate task/domain/global-explicit/unspecified scope;
- preserve direct references to original event IDs;
- enforce blind-eval exclusion where relevant.

Output:

```text
EffectiveEvidenceView
```

This is derived and may be rebuilt at any time.

It is **not** a fifth raw record family.

## B2 — Preference Projection Builder

Purpose:

> Build small, scoped, evidence-backed summaries that help runtime generation without pretending to be a universal personal model.

Possible outputs:

```text
ConfirmedGlobalCore
DomainPreferenceSnapshot
TaskRelevantPreferenceSummary
AntiPatternSummary
```

Rules:

1. every statement must cite source `event_id` values;
2. explicit user evidence outranks inferred summaries;
3. one-off task feedback must not become global automatically;
4. contradictions must be preserved, not averaged away silently;
5. unknown/insufficient evidence is a valid state;
6. the projection is replaceable and versioned as a derived artifact.

The term `Visual DNA` may be used later as a presentation label, but it is not an architectural source of truth.

## B3 — Exemplar Selector

Purpose:

> Return a small number of relevant visual examples rather than injecting the entire archive into context.

V0.1 strategy:

```text
transparent metadata
+ explicit user tags
+ scope/domain compatibility
+ approved/rejected relations
+ recency where useful
```

Do not require embeddings or a vector database initially.

Recommended runtime result:

```text
2–6 positive / reference exemplars
0–3 negative / rejected exemplars
```

Exact counts are tuning parameters, not architecture invariants.

The selector must return:

- `sample_id`;
- why it was selected;
- the raw evidence IDs supporting its preference role;
- whether the asset is currently resolvable.

## B4 — Calibration Projection Adapter

Purpose:

> Preserve compatibility with the current `personal-aesthetic-critic` without creating a second preference authority.

The current repository's `calibration/anchors.json` becomes, after implementation, a compatibility projection generated from eligible SampleRecords and explicit user EvidenceEvents.

It must not become a manually maintained parallel truth source once the new ledger is active.

The existing critic can continue reading its expected anchor format while the underlying authority becomes the raw visual ledger.

---

# 6. Plane C — Runtime Context Plane

The Runtime Context Plane is the bridge between durable preference memory and an actual visual task.

It contains two logical components.

## C1 — Task Intent Resolver

The current user request is the highest authority.

The resolver identifies only what is necessary for retrieval and execution:

- task type;
- explicit current constraints;
- likely visual domain;
- referenced images/samples;
- whether this is generation, edit, comparison, or critique;
- whether personal preference context is relevant.

The resolver must not promote temporary task instructions into durable preferences.

## C2 — Visual Context Assembler

Purpose:

> Build a bounded, inspectable, ephemeral context packet for one task.

Proposed logical shape:

```text
VisualContextPack
├── current_explicit_constraints
├── confirmed_global_core
├── scoped_preference_summary
├── positive_exemplars[]
├── negative_exemplars[]
├── known_conflicts_or_uncertainty
└── source_evidence_ids[]
```

The pack is **not durable preference truth**.

It may be logged for debugging, but must not be treated as user evidence.

## Context precedence

Mandatory order:

```text
1. current explicit user instruction
2. explicit task-scoped evidence relevant to this task
3. explicit domain-scoped evidence
4. confirmed global-explicit evidence
5. derived historical inference
6. generic professional aesthetic defaults
```

If any historical layer conflicts with the current explicit instruction, the current instruction wins.

## Context budget

The system must prefer a small, high-signal context over exhaustive loading.

Architecture target:

- tiny confirmed cross-domain core, possibly empty;
- relevant profile summary only;
- a handful of visual exemplars;
- clear negative examples when materially useful.

This follows the repository's anti-bloat charter: preserve high-leverage variables and avoid rule encyclopedias.

---

# 7. Plane D — Execution & Evaluation Plane

This plane uses existing generation routes and separates execution from evaluation.

## D1 — Existing Repository Router

PHASE 4 does not add a new visual Router Skill.

The repository already routes visual work through `START_HERE.md` and `AGENTS.md` to existing domain Skills.

Therefore:

```text
LIU VISUAL SYSTEM supplies context
Existing repo routing chooses workflow
Existing visual Skill compiles execution
```

This minimizes trigger collisions and avoids duplicating repository topology.

A dedicated thin visual-memory entry Skill may be considered later only if real workflows prove that host integration cannot reliably request context without one.

## D2 — Existing Visual Skill / Prompt Compiler

The visual memory system must not rewrite mature visual Skills merely to inject personal preference.

Preferred integration:

```text
base Skill behavior
+
small VisualContextPack
+
current explicit task
```

The Skill remains responsible for its own domain execution grammar.

Personal memory should modify high-leverage choices, not append hundreds of new rules.

## D3 — Generation Gateway

Purpose:

> Execute the chosen renderer while recording enough metadata to explain model-dependent changes.

Responsibilities:

- receive final execution request;
- call the currently selected renderer;
- create `GenerationRecord`;
- register output `SampleRecord` + `AssetRecord`;
- connect iterative generations using `parent_generation_id`;
- record reference sample IDs actually used.

It is a logical seam, not a full multi-renderer adapter framework.

## D4 — Personal Aesthetic Critic

The existing `personal-aesthetic-critic` remains the diagnostic/evaluation mechanism.

Architecture rule:

```text
critic output != raw user preference evidence
```

The critic may produce:

- technical evaluation;
- professional aesthetic evaluation;
- task compliance;
- calibrated personal-fit when enough user anchors exist;
- pairwise comparison;
- before/after diagnosis.

But only the user's direct reaction becomes raw EvidenceEvent preference truth.

## D5 — Correctness Gates

Hard gates remain appropriate only for objectively testable failures:

- wrong text;
- wrong identity;
- missing required output;
- wrong dimensions/aspect ratio;
- broken file;
- prohibited leakage into blind eval;
- schema/integrity failure once schemas exist.

Taste remains advisory/evidence-driven, not converted into hard deterministic gates.

---

# 8. Plane E — Learning & Governance Plane

## E1 — Evidence-Worthy Feedback Capture

The architecture should capture raw evidence only when a meaningful user event occurs.

Capture examples:

- explicit approval/rejection;
- A/B choice;
- concrete revision request;
- correction/retraction;
- stable user-confirmed reference.

Do not automatically capture as personal preference:

- every successful generation;
- critic scores;
- assistant summaries;
- prompt text;
- generic model judgments.

## E2 — Existing Skill Refiner Bridge

When repeated evidence suggests a stable change to a Skill or repository workflow:

```text
raw visual event IDs
      ↓
skill-refiner observation
      ↓
candidate
      ↓
baseline vs candidate evaluation
      ↓
gate
      ↓
Git review / promotion
```

There is only one durable promotion authority.

LIU VISUAL SYSTEM must not automatically edit production Skills from raw feedback.

## E3 — Evaluation Isolation Guard

Purpose:

> Prevent self-congratulatory evaluation by ensuring reserved blind samples cannot influence discovery before evaluation is locked.

Minimum responsibilities:

- block `blind_eval_reserved` from preference-profile building;
- block it from exemplar retrieval;
- block it from prompt/profile tuning;
- record when a blind case is released after evaluation;
- allow production failures to become regression cases later without pretending they were previously held out.

The final evaluation file format is deferred.

## E4 — Derived Artifact Provenance

Every durable derived profile/snapshot must identify:

- builder version;
- build time;
- source raw record IDs;
- source-evidence range/snapshot;
- known conflicts/uncertainty where relevant.

This makes stale or wrong derived intelligence removable without losing user truth.

---

# 9. Authority model

The architecture has deliberately separate authorities.

## Authority A — Current Task Truth

Owner:

```text
current user instruction
```

Highest runtime priority.

## Authority B — Personal Evidence Truth

Owner:

```text
raw EvidenceEvent ledger
```

Only direct user / faithfully imported user evidence.

## Authority C — Visual Asset Identity

Owner:

```text
SampleRecord + AssetRecord
```

## Authority D — Derived Preference Interpretation

Owner:

```text
rebuildable derived artifacts
```

Advisory, never source truth.

## Authority E — Professional/Technical Evaluation

Owner:

```text
personal-aesthetic-critic + deterministic gates
```

Diagnostic, not personal truth.

## Authority F — Production Skill Changes

Owner:

```text
Git + existing skill-refiner promotion workflow
```

No other subsystem may silently promote raw feedback into permanent Skill changes.

---

# 10. Write-permission architecture

A major failure mode is allowing every intelligent component to write everywhere.

PHASE 4 proposes strict logical write boundaries.

## Raw Ingestor may write

```text
SampleRecord
AssetRecord
```

It may not write inferred preference.

## Generation Gateway may write

```text
GenerationRecord
output SampleRecord
output AssetRecord
```

It may not write user EvidenceEvent unless the user separately supplied direct evidence.

## Feedback Capture may write

```text
EvidenceEvent
```

Only direct/fidelity-preserved user evidence.

## Effective Evidence / Profile Builder may write

```text
derived artifacts only
```

Never raw.

## Critic may write

```text
evaluation artifacts only
```

Never raw preference events.

## Skill Refiner may write

```text
.skill-evolution state
candidate patches
Git-reviewed production changes
```

It does not own the raw personal evidence archive.

---

# 11. Core runtime workflows

## Workflow W1 — Import a liked reference

```text
user supplies image
→ ingest binary
→ create AssetRecord
→ create SampleRecord
→ no preference assumption yet
→ user explicitly says liked/reference/rejected
→ create EvidenceEvent
→ derived projection may update later
```

Critical rule:

Uploading an image is not automatically an approval signal.

## Workflow W2 — Generate from personal context

```text
current user task
→ existing repo route
→ Task Intent Resolver
→ Effective Evidence View
→ scoped Preference Projection
→ Exemplar Selector
→ VisualContextPack
→ existing visual Skill / prompt compiler
→ Generation Gateway
→ GenerationRecord + output Sample/Asset
→ optional critic evaluation
→ wait for user reaction
```

## Workflow W3 — User rejects output

```text
user: “太脏了”
→ raw Feedback EvidenceEvent
→ no automatic Skill edit
→ current task uses explicit correction immediately
→ next derived build may update scoped summary
→ repeated stable evidence may later feed skill-refiner
```

## Workflow W4 — A/B preference

```text
A and B exist as SampleRecords
→ user picks A
→ Comparison EvidenceEvent
→ pairwise ordering preserved
→ derived layer may analyze likely dimensions
→ raw layer does not claim causality
```

## Workflow W5 — Revision

```text
user requests concrete change
→ Revision EvidenceEvent
→ new generation
→ GenerationRecord parent link
→ after SampleRecord
→ user reaction stored separately as FeedbackEvent
```

## Workflow W6 — User corrects old preference

```text
user: “刚才说错了”
→ Correction EvidenceEvent
→ Effective Evidence View recomputed
→ derived profiles become stale
→ rebuild derived projections
→ raw historical wording remains auditable
```

## Workflow W7 — Stable pattern becomes Skill candidate

```text
multiple evidence IDs support recurring issue
→ skill-refiner observe
→ candidate formation only if threshold/authority condition met
→ evaluate against baseline/regression
→ Git-reviewed promotion
```

---

# 12. Derived profile strategy

PHASE 4 rejects a single mandatory universal Visual DNA file.

Instead, the architecture allows multiple projections.

## 12.1 ConfirmedGlobalCore

Extremely small.

Contains only cross-domain preferences with strong explicit/repeated evidence.

May initially be empty.

Examples of things that might eventually qualify:

- current explicit instruction always wins;
- user dislikes dirty/grungy texture when the request is clean-dark, if repeatedly confirmed across domains.

The content itself is not frozen here.

## 12.2 DomainPreferenceSnapshot

Scope-limited projection for domains such as:

```text
food
photography
sci-fi
travel/editorial
branding
```

But domain names are not fixed schema enums.

A future taxonomy can reorganize them without rewriting raw evidence.

## 12.3 AntiPatternSummary

Derived summary of repeatedly rejected visual mechanisms.

Must cite raw evidence.

Must stay short and scoped.

## 12.4 Exemplar Sets

Prefer actual visual examples over converting every preference into prose rules.

This architecture intentionally favors:

```text
small rule/profile summary
+
actual positive/negative exemplars
```

over hundreds of explicit aesthetic rules.

---

# 13. Asset architecture

The architecture separates **asset authority** from Git repository metadata.

## V0.1 rule

Git is suitable for:

- code;
- contracts;
- metadata;
- small canonical fixtures;
- derived review artifacts.

Git is not assumed to be the bulk visual warehouse.

## Asset Vault abstraction

“Asset Vault” is a conceptual boundary only.

It may initially be:

- local durable files;
- a stable user file store;
- another reachable durable location.

PHASE 4 does not select object storage.

The Asset Resolver must eventually answer:

```text
Given asset_id, can the current runtime obtain inspectable bytes?
```

If not, the architecture must report the reference as unavailable rather than pretending it was inspected.

This is important because Codex/local runtime, ChatGPT, and GitHub may not all share the same filesystem.

---

# 14. Runtime environment boundary

The architecture must not assume every host can access every asset locator.

Therefore VisualContextPack distinguishes:

```text
selected exemplar
vs
resolvable exemplar
```

If a selected sample is not resolvable in the current runtime:

- do not claim visual inspection;
- either select another resolvable exemplar;
- or proceed with evidence-backed text context only while clearly marking the limitation;
- never delete or downgrade the underlying sample merely because one runtime cannot fetch it.

This prevents host-specific availability from contaminating preference truth.

---

# 15. Evaluation architecture

Evaluation has three separate questions.

## 15.1 Correctness

Can be deterministic or hard-gated where observable.

## 15.2 Professional visual quality

Handled by existing critic / human review.

## 15.3 Personal preference match

Must be evidence-backed and may remain unknown.

The architecture must never collapse these three into one misleading score.

## Evaluation loop

```text
baseline architecture/profile version
vs
candidate architecture/profile version
→ same task constraints
→ blind or anonymized comparison where practical
→ user preference / critic diagnostics separated
→ known regression cases checked
```

A fixed regression suite protects known failures.

Rotating blind cases protect against suite overfitting.

Production failures feed future regression cases.

The detailed benchmark format belongs to a later phase.

---

# 16. Failure isolation and fallback behavior

## F-01 — Derived profile build fails

Fallback:

```text
current explicit task
+ explicit confirmed examples only
```

Generation may continue without inferred profile.

Raw evidence remains untouched.

## F-02 — Retrieval returns irrelevant examples

Fallback:

- discard retrieved set;
- use current explicit references;
- optionally use small confirmed core;
- record retrieval failure as technical/evaluation evidence, not user preference.

## F-03 — Asset cannot be resolved

Fallback:

- mark unavailable;
- never pretend it was visually inspected;
- substitute another evidence-backed exemplar if possible.

## F-04 — Critic fails or disagrees with user

User preference wins for personal taste.

Critic output remains diagnostic only.

## F-05 — Derived profile conflicts with current instruction

Current instruction wins immediately.

No manual profile edit is required for the current task.

If conflict reveals an outdated durable assumption, user correction may create a new EvidenceEvent.

## F-06 — Skill Refiner candidate fails validation

No production Skill change.

Raw visual evidence remains useful independently.

## F-07 — Blind-eval contamination detected

Evaluation result is invalidated/flagged.

Do not repair validity by retroactively relabeling evidence.

## F-08 — Renderer model changes

GenerationRecord provides renderer/model context.

Do not infer preference drift solely from output behavior changing after a model update.

---

# 17. Consistency model

PHASE 4 recommends a simple consistency model.

## Raw evidence

Strong consistency for one writer path:

- write succeeds or does not exist;
- stable IDs;
- user EvidenceEvents are append-oriented.

## Derived projections

Eventually consistent:

- may lag behind newest raw event;
- must expose build timestamp/version/source IDs;
- can be rebuilt on demand.

## Runtime task

The current explicit instruction is applied immediately even if derived projections have not rebuilt yet.

This avoids requiring synchronous full re-distillation after every user comment.

---

# 18. Rebuild model

The architecture must support this operation conceptually:

```text
DELETE ALL DERIVED ARTIFACTS
        ↓
read raw Sample / Asset / Evidence / Generation records
        ↓
recompute effective evidence
        ↓
rebuild preference projections
        ↓
rebuild exemplar sets / indexes
        ↓
rebuild calibration compatibility view
```

No user relabeling should be required.

The existing `.skill-evolution` state is not required to reconstruct raw preference memory.

Promoted Skill history remains separately recoverable through Git.

---

# 19. Proposed deployment sequence

This is an architecture sequence, not implementation work performed in PHASE 4.

## Step A — Minimal persistence implementation

Implement PHASE 3 record families and integrity rules.

## Step B — Small pilot ingestion

20–50 positive/reference samples plus selected rejected examples and real feedback.

## Step C — Effective evidence projection

Add correction/retraction/tombstone replay.

## Step D — Simple metadata exemplar retrieval

No embeddings initially.

## Step E — Derived scoped preference snapshots

Small, cited, rebuildable.

## Step F — Compatibility adapter to existing critic calibration

Avoid manual dual truth.

## Step G — Runtime VisualContextPack integration

Inject context into existing visual routes without rewriting those Skills.

## Step H — Generation logging and feedback capture

Complete the closed loop.

## Step I — Small regression + rotating blind evaluation

Prove whether the system actually reduces revision rounds and increases user preference.

## Step J — Scale only when measured bottlenecks appear

Possible later additions:

- embeddings;
- perceptual dedupe;
- object storage;
- a thin visual-memory entry Skill;
- richer preference models.

---

# 20. Metrics architecture

The system should not optimize for “more rules” or “higher critic score”.

Useful future metrics include:

```text
first-generation user acceptance
pairwise win rate of context-enabled vs baseline
revision rounds per accepted output
user override/conflict rate
retrieval relevance rate
known-regression recurrence rate
personal-fit unknown rate as calibration grows
```

These are evaluation metrics, not raw user preference fields.

No numeric success threshold is frozen in PHASE 4.

---

# 21. Complexity budget

PHASE 4 deliberately limits V0.1 complexity.

## Required logical components

```text
Raw Record Store
Asset Resolver boundary
Effective Evidence Projector
Preference Projection Builder
Exemplar Selector
Visual Context Assembler
Generation Gateway
Feedback Capture
Evaluation Isolation Guard
Skill Refiner Bridge
Calibration Compatibility Adapter
```

Important:

These do not need to be 11 services/classes/processes.

A V0.1 implementation may combine several responsibilities in a small set of files/scripts as long as authority boundaries are preserved.

## Deferred infrastructure

```text
vector database
embedding service
object storage adapter fleet
microservices
message queue
workflow engine
multi-agent merge coordinator
trained reward/preference model
```

---

# 22. Alternatives considered

## Alternative A — One giant visual Skill

Rejected.

Why:

- repeats repository rule-bloat failure;
- mixes memory, generation, evaluation, and governance;
- hard to rebuild independently;
- historical taste becomes prompt bloat.

## Alternative B — Router + many new visual Skills

Deferred/rejected for V0.1.

Why:

- repository already has routing;
- adds trigger collisions;
- data layer is the actual missing capability;
- workflow divergence has not yet justified new Skills.

## Alternative C — Full event-sourced service architecture

Rejected for V0.1.

Why:

- only EvidenceEvent truly requires append-oriented history;
- would create infrastructure complexity without user value;
- Sample/Asset operational metadata needs simple corrections.

## Alternative D — Train a preference model immediately

Rejected for V0.1.

Why:

- no calibrated dataset yet;
- high false-confidence risk;
- case-based exemplars + explicit scoped evidence are more inspectable.

## Alternative E — Data-first modular monolith with existing Skills

Recommended.

Why:

- protects raw evidence;
- minimizes new topology;
- supports incremental sophistication;
- allows complete derived-layer replacement;
- aligns with current repository anti-bloat governance.

---

# 23. Decisions intentionally left open for PHASE 5 ADR

PHASE 4 is a proposal, not a freeze.

The following decisions should receive explicit ADR treatment next:

```text
ADR candidate 1 — raw storage format and repository placement
ADR candidate 2 — asset vault / locator operational policy
ADR candidate 3 — derived artifact storage and rebuild policy
ADR candidate 4 — calibration compatibility strategy
ADR candidate 5 — runtime VisualContextPack integration point
ADR candidate 6 — existing Skill integration without prompt bloat
ADR candidate 7 — blind-eval contamination control
ADR candidate 8 — skill-refiner bridge semantics
ADR candidate 9 — user evidence capture trigger policy
ADR candidate 10 — single-writer and migration policy
```

PHASE 5 may merge or reject ADR candidates after review.

---

# 24. PHASE 4 hard invariants

The architecture proposal is acceptable only if all of these remain true:

```text
AR-01 Current explicit user instruction is highest runtime authority.
AR-02 Direct user EvidenceEvent is the personal preference source of truth.
AR-03 Critic/LLM output cannot enter raw preference truth automatically.
AR-04 Raw records never depend on a derived profile for meaning.
AR-05 Derived profiles are cited, versioned, and rebuildable.
AR-06 Existing skill-refiner is the only durable Skill-promotion authority.
AR-07 Existing personal-aesthetic-critic is reused, not duplicated.
AR-08 Existing repository routing is reused in V0.1.
AR-09 No universal Visual DNA is assumed.
AR-10 Actual exemplars remain first-class preference evidence.
AR-11 Blind-eval-reserved samples cannot leak into discovery.
AR-12 Renderer-specific prompt syntax is not personal preference truth.
AR-13 Git is not assumed to be the bulk image warehouse.
AR-14 Runtime cannot claim it inspected an unavailable asset.
AR-15 Taste is not converted into deterministic correctness gates.
AR-16 User correction can change effective meaning without rewriting history.
AR-17 Failure of any derived component cannot corrupt raw evidence.
AR-18 V0.1 remains implementable without embeddings, microservices, or model training.
```

---

# 25. PHASE 4 exit gate

PHASE 4 may pass if:

```text
[ ] Architecture is based on PHASE 3 four-family Data Contract.
[ ] Component boundaries do not create duplicate sources of truth.
[ ] Existing repo router is reused.
[ ] Existing critic is reused.
[ ] Existing skill-refiner is reused.
[ ] Calibration compatibility avoids dual manual authority.
[ ] Runtime context precedence is explicit.
[ ] Raw/derived write permissions are explicit.
[ ] Asset availability across runtimes is addressed.
[ ] Blind-eval contamination path is addressed.
[ ] Failure fallback behavior is specified.
[ ] Derived rebuild path is specified.
[ ] At least four alternative architectures were considered.
[ ] Deferred infrastructure remains deferred.
[ ] ADR candidates are identified but not written yet.
[ ] No Skill was created or modified.
[ ] No schema/validator/script/scaffold was created.
[ ] No images were imported.
[ ] No Architecture Freeze was performed.
```

If all pass, status is:

```text
PHASE 4 — PASS / PROPOSAL ONLY
```

Then stop before PHASE 5.

---

# 26. Final recommendation

The architecture should not be understood as “building a new giant system next to the existing aesthetic repository.”

It should be understood as adding a **personal visual evidence and context layer underneath the existing visual workflows**.

The durable core is:

```text
user visual evidence
        ↓
rebuildable scoped interpretation
        ↓
small context pack
        ↓
existing visual workflow
        ↓
generation
        ↓
diagnostic critic
        ↓
real user feedback
        ↓
user evidence
```

Only when evidence repeatedly proves a production Skill itself is wrong should `skill-refiner` attempt a reviewed Skill change.

This keeps the system capable of becoming increasingly personalized without recreating the exact failure mode the repository has already experienced: more rules, more validators, more complexity, and worse visual output.
