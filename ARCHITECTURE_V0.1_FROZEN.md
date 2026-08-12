# LIU VISUAL SYSTEM — ARCHITECTURE V0.1

Status: `FROZEN`
Freeze date: `2026-08-12`
Freeze branch: `phase-6-architecture-freeze-review-20260812`

This file is the compact controlling architecture record for LIU VISUAL SYSTEM V0.1.

It freezes only the decisions whose change would create significant data migration, preference-authority conflict, privacy risk, evaluation contamination, or user relabeling cost.

It intentionally does **not** freeze implementation details that are cheap to change.

---

# 1. System purpose

LIU VISUAL SYSTEM is a personal visual evidence and context layer that improves existing visual-generation workflows over time by preserving direct user preference evidence and retrieving relevant exemplars.

It is not:

- a trained foundation model;
- a universal aesthetic scoring oracle;
- a giant visual Skill;
- a new Skill router family;
- a permanent Visual DNA document;
- an automatic self-modifying agent.

Its long-term promise is narrower and testable:

> **The user should be able to change models, retrieval methods, renderers, Skills, profile algorithms, and storage technology without having to manually recreate the original visual preference history.**

---

# 2. Frozen architecture style

V0.1 is a:

```text
DATA-FIRST MODULAR MONOLITH
```

Logical components describe responsibility and authority boundaries.

They do not imply separate services, processes, agents, queues, or classes.

V0.1 should remain implementable as a small local/private package plus existing repository workflows.

---

# 3. Frozen raw source of truth

There are exactly four durable raw record families in V0.1:

```text
SampleRecord
AssetRecord
EvidenceEvent
GenerationRecord
```

No fifth raw family for Visual DNA, profile, rule, critic score, embedding, cluster, or calibration anchor is part of V0.1 source truth.

---

# 4. Frozen identity semantics

## Sample identity

`sample_id` identifies one logical visual sample.

It is independent of:

```text
file path
URL
filename
SHA-256
storage provider
domain taxonomy
```

## Asset identity

`asset_id + sha256` identifies one exact binary blob.

Changing bytes creates a new AssetRecord.

Moving unchanged bytes changes locator metadata only.

## Evidence identity

`event_id` identifies one direct user-evidence event.

## Generation identity

`generation_id` identifies one concrete generation execution.

Stable IDs must survive storage migration.

---

# 5. Frozen persistence authority

Canonical structured personal raw data is stored in a **private data root outside the public `shenmei` repository by default**.

V0.1 is single-writer.

The exact storage engine is not permanent.

Initial file-based persistence may later migrate to SQLite, Postgres, or another private store through a superseding ADR while preserving stable IDs and semantics.

The public repository may contain code, schemas, validators, non-sensitive fixtures, ADRs, and documentation, but not the canonical private preference ledger by default.

---

# 6. Frozen asset policy

Bulk visual bytes live behind a private `Asset Vault` boundary outside public Git by default.

The storage vendor/location is not frozen.

Runtime must distinguish:

```text
known
selected
resolvable
actually inspected
```

A runtime may make visual claims about a stored exemplar only when it actually resolved and inspected the asset bytes in that run.

Failure to resolve an asset does not invalidate historical preference evidence.

A source URL is provenance; it is not by itself a durability guarantee.

---

# 7. Frozen personal evidence admission policy

Raw personal preference truth accepts only:

```text
direct current user evidence
or
faithfully imported historical user evidence with traceable origin
```

Faithful historical import requires original user wording or an original structured user action when available.

The following do not become raw personal preference truth automatically:

```text
image upload alone
silence
routine task completion
AI critic output
assistant memory summary
LLM paraphrase
prompt text
professional aesthetic rule
derived profile
retrieval result
renderer behavior
```

When evidence meaning/scope is ambiguous, preserve the original user evidence and keep structured interpretation unknown/unspecified rather than inventing certainty.

---

# 8. Frozen evidence-history semantics

User EvidenceEvents are append-oriented.

Original user wording is not silently rewritten.

Corrections are new events using:

```text
supersede
retract
clarify
```

Current effective preference is a derived replay/projection of raw history.

A failed EvidenceEvent persistence write may affect the current task ephemerally, but the system must not claim persistent learning occurred.

---

# 9. Frozen evidence scope semantics

V0.1 raw scope supports:

```text
task
domain
global_explicit
unspecified
```

Rules:

- `global_explicit` requires explicit durable/global user intent;
- `domain` requires objectively clear task/domain context;
- ambiguity defaults to `unspecified`;
- broader generalization belongs in the derived layer.

One-off evidence never silently becomes global truth.

---

# 10. Frozen raw vs derived boundary

All intelligence inferred from raw evidence is replaceable derived state.

Examples:

```text
EffectiveEvidenceView
ConfirmedGlobalCore
DomainPreferenceSnapshot
AntiPatternSummary
Exemplar rankings
Visual DNA presentation summary
embeddings
clusters
retrieval indexes
calibration compatibility views
```

Derived artifacts:

- may be deleted wholesale;
- must not overwrite raw evidence;
- must preserve source-record provenance when durable;
- must be rebuildable without asking the user to relabel historical samples.

A derived profile is cache, not a second brain/source of truth.

---

# 11. Frozen calibration authority

`calibration/anchors.json` is a compatibility representation for the existing critic, not an independent personal-preference authority.

Personal calibration must originate from eligible raw user evidence + inspectable samples.

Because the repository is public:

- tracked public calibration content must remain non-sensitive by default;
- private personal calibration must be supplied through a private runtime/workspace overlay or another privacy-safe input mechanism;
- private personal anchor content must not be committed into public Git by default;
- until a safe integration exists, `personal_fit` remains `null` rather than leaking private calibration data.

Critic category mapping is derived and may fail safely.

Raw evidence is never rewritten merely to fit critic categories.

---

# 12. Frozen runtime-context architecture

Personal context is assembled at the host/runtime orchestration layer before the selected existing visual Skill executes.

A dedicated top-level personal visual Skill is not required by V0.1.

The ephemeral `VisualContextPack` is:

```text
small
bounded
task-specific
evidence-cited
replaceable
```

It may contain:

```text
small scoped preference summary
positive/reference exemplars
negative/rejected exemplars
relevant anti-patterns
asset resolution status
source evidence IDs
```

It must not reproduce the entire evidence archive or an alternate full visual grammar.

---

# 13. Frozen personalization precedence

Inside the personalization/aesthetic layer:

```text
current explicit user instruction
>
current task-specific constraints
>
explicit scoped historical evidence
>
confirmed durable/global evidence
>
derived historical inference
```

This precedence does not bypass:

- system/safety policy;
- privacy/deletion requirements;
- raw-data integrity;
- evaluation isolation;
- deterministic correctness constraints;
- repository security/governance.

Historical preference assists the current task; it does not overrule the user.

---

# 14. Frozen existing-system reuse

V0.1 reuses existing repository capabilities.

## Routing

Use existing `START_HERE.md` / `AGENTS.md` routing.

Do not create a new Router family solely for visual memory.

## Visual execution

Use existing appropriate visual Skills / prompt compilers.

Personal context is additive and bounded; it does not duplicate the Skill grammar.

## Critic

Reuse `personal-aesthetic-critic` where the task legitimately fits its supported categories.

The critic is a professional/technical/task evaluator, not personal truth.

Unsupported domains are not forced into fake critic categories.

## Skill evolution

Existing `skill-refiner` is the single durable production Skill-promotion authority.

No parallel visual rule-lifecycle system is permitted in V0.1.

---

# 15. Frozen Skill-promotion boundary

Raw feedback never edits a production Skill directly.

Runtime preference projections may affect current context only.

A repeated stable lesson may become a Skill candidate only through:

```text
selected raw evidence IDs
→ skill-refiner observation/candidate
→ relevant baseline/regression evaluation
→ reviewable Git change
→ promotion
```

No automatic LLM Skill promotion is allowed.

If a stable preference belongs only in retrieval/profile context, it stays there instead of being promoted into a Skill unnecessarily.

---

# 16. Frozen blind-evaluation isolation

V0.1 `blind_eval_reserved` is sticky for the lifetime of the V0.1 evaluation pool.

The contamination barrier is transitive across the designated blind case.

Do not use for preference discovery/tuning/Skill refinement:

```text
reserved samples
blind-case generated outputs
preference events dependent on the blind case
derived summaries/exemplar roles produced from the blind case
those blind-case evidence IDs as skill-refiner evidence
```

Production failures may become regression cases, but they are not retroactively called blind holdout.

Releasing a V0.1 reserved sample requires a future superseding ADR with auditable release history.

---

# 17. Frozen generation provenance

Generated outputs preserve at minimum:

```text
generation_id
timestamp
renderer
model
reference_sample_ids
output_sample_ids
parameters
```

Prompt text may be stored as private execution metadata when useful but is never personal preference truth.

Renderer/model/version metadata exists to prevent model behavior changes from being mistaken for preference drift.

No renderer adapter framework is frozen in V0.1.

---

# 18. Frozen deletion principle

Append-oriented evidence does not mean physically undeletable personal data.

V0.1 must support:

```text
logical tombstone / immediate exclusion
+
physical purge path when required
+
derived rebuild/removal
```

The exact purge implementation is not frozen.

---

# 19. Frozen durability principle

Before non-disposable real personal Pilot evidence accumulates, both must have a recoverable backup/export path:

```text
canonical structured raw records
Asset Vault bytes required by those records
```

Backup technology/vendor is not frozen.

The architecture is not considered operationally ready for real Pilot data without recoverability.

---

# 20. Frozen fallback behavior

Failure of derived intelligence must degrade personalization, not corrupt truth.

Examples:

## Profile/retrieval failure

Fallback to:

```text
current user task
+ current explicit references
+ directly confirmed available evidence when safe
```

## Asset unavailable

Do not claim inspection.

## Critic failure/disagreement

Critic remains diagnostic. Explicit user preference controls personal taste.

## Skill-refiner candidate failure

No production Skill change.

## Raw evidence write failure

Do not claim persistent learning.

---

# 21. Frozen privacy boundary for public repository

Personal raw evidence, private source locators, private prompt history, personal calibration, and bulk private reference assets do not enter public Git by default.

The public repository may contain synthetic/non-sensitive fixtures for tests.

Any future proposal to make personal visual memory public requires an explicit user decision and separate review; it is not an architecture default.

---

# 22. Frozen architecture change policy

These frozen invariants are not silently edited in place.

To reverse one:

1. write a new ADR;
2. identify the frozen invariant being superseded;
3. state migration and privacy/evaluation impact;
4. preserve stable raw identities/evidence where possible;
5. rerun Architecture Freeze Review before implementation uses the new decision.

Historical ADRs/reviews remain in Git.

---

# 23. Intentionally NOT frozen

V0.1 deliberately leaves these reversible:

```text
UUIDv4 vs UUIDv7
exact private directory names
JSON vs JSONL file partition details beyond contract semantics
future database vendor
object storage vendor
backup vendor
VisualContextPack serialization
number of exemplars retrieved
free-form domain labels
future taxonomy
embedding model
vector database
perceptual-hash algorithm
retrieval scoring formula
profile prose format
cluster algorithm
renderer adapter interface
prompt syntax
critic numeric weights
future thin entry Skill name
```

Do not turn these into invariants without measured need.

---

# 24. V0.1 architecture snapshot

```text
CURRENT USER REQUEST
        │
        ▼
EXISTING REPO ROUTER
        │
        ▼
HOST RUNTIME CONTEXT ASSEMBLY
        │
        ├── current intent
        ├── effective raw evidence projection
        ├── small scoped preference projection
        ├── positive/negative exemplars
        └── asset resolution truth
        │
        ▼
BOUNDED VisualContextPack
        │
        ▼
EXISTING VISUAL SKILL / PROMPT COMPILER
        │
        ▼
RENDERER
        │
        ▼
GenerationRecord + output Sample/Asset
        │
        ├──────────────► existing critic (diagnostic/eval only)
        │
        ▼
DIRECT USER REACTION
        │
        ▼
EvidenceEvent raw ledger
        │
        ▼
rebuildable derived projections
        │
        └── repeated stable procedure defect only
                ▼
           skill-refiner
                ▼
        eval + Git-reviewed Skill change
```

---

# 25. Freeze result

```text
ARCHITECTURE V0.1 = FROZEN
```

This freeze authorizes the next phase to build a **minimal implementation scaffold** that conforms to these invariants.

It does not authorize the next phase to import the full visual archive immediately.

A small disposable/synthetic verification should precede the real Pilot, followed by a deliberately small personal Pilot only after the implementation gates pass.
