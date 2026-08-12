# LIU VISUAL SYSTEM — PHASE 4 ARCHITECTURE SELF-REVIEW

Status: `PASS / PROPOSAL_ONLY`

Date: `2026-08-12`

Authority: this self-review is the final controlling clarification for PHASE 4. Where a clarification below narrows an earlier sentence in `PHASE_4_ARCHITECTURE_PROPOSAL.md` or `PHASE_4_AUTHORITY_BOUNDARY_MATRIX.md`, this review controls until PHASE 5 ADRs make the relevant decisions explicit.

PHASE 4 remains a proposal. It is **not** an architecture freeze.

---

# 1. Review method

The proposal was attacked against:

- PHASE 2 highest-priority risks;
- PHASE 3 Data Contract invariants;
- current repository routing;
- existing `personal-aesthetic-critic` limitations;
- existing calibration behavior;
- existing `skill-refiner` authority;
- the repository's documented visual rule-bloat failure mode.

The review specifically asked:

> Does the proposed architecture accidentally recreate complexity that PHASE 2 already rejected?

and:

> If the upper intelligence layer is wrong and rewritten later, does the user have to relabel visual history?

---

# 2. Finding R4-01 — logical components must not become implementation units by default

The proposal names several components:

```text
Effective Evidence Projector
Preference Projection Builder
Exemplar Selector
Calibration Adapter
Task Intent Resolver
Visual Context Assembler
Generation Gateway
Feedback Capture
Eval Isolation Guard
Skill Refiner Bridge
```

Risk:

An implementer could interpret this as a mandate for ten services/classes/agents.

Final clarification:

> These names define authority and failure boundaries only.

For the pilot, several may be implemented together in one small package or deterministic script set.

No microservices, queues, workflow engine, or agent fleet are justified by PHASE 4.

Verdict: `PASS WITH CLARIFICATION`.

---

# 3. Finding R4-02 — existing personal-aesthetic-critic is reusable but not universal

The current critic supports four primary categories:

```text
portrait_editorial
food_photography
poster_design
cinematic_photo
```

LIU VISUAL SYSTEM is broader than those categories.

Risk:

If the architecture treats the critic as a mandatory universal evaluation bottleneck, unsupported work may be forced into incorrect categories merely to obtain a score.

Final clarification:

1. Reuse `personal-aesthetic-critic` when the current work legitimately maps to its supported categories.
2. Do not force every future visual domain into one of its four categories.
3. Unsupported domains may use direct pairwise/user evidence and task-specific evaluation without an official critic score.
4. If critic coverage later needs expansion, that is a separate evidence-gated Skill evolution task.

Therefore:

```text
existing critic = reusable evaluator
NOT universal architectural dependency
```

Verdict: `PASS WITH CLARIFICATION`.

---

# 4. Finding R4-03 — calibration projection must map critic categories without rewriting raw domains

The existing calibration system expects same-category anchors.

The new raw contract deliberately avoids a fixed domain taxonomy.

Risk:

A compatibility adapter might hard-code critic categories back into raw Sample/Evidence records, recreating taxonomy lock-in.

Final clarification:

```text
raw scope/domain label
        ↓
derived compatibility mapping
        ↓
critic category if legitimately compatible
```

The mapping is derived and replaceable.

Raw evidence does not change simply because the critic uses a different category vocabulary.

If no safe mapping exists, `personal_fit` remains unavailable/null rather than forcing a category.

Verdict: `PASS`.

---

# 5. Finding R4-04 — ConfirmedGlobalCore can become a disguised universal Visual DNA

Risk:

Even a “tiny global core” can gradually grow into the same large global rule dump that PHASE 2 rejected.

Final clarification:

`ConfirmedGlobalCore` is optional and derived.

It may remain empty indefinitely.

A statement belongs there only when evidence supports cross-domain durability. Domain-specific rules must not be promoted merely because they recur inside one domain.

No component may require a non-empty global core.

Verdict: `PASS WITH HARD LIMIT`.

---

# 6. Finding R4-05 — profile rebuild must not block immediate corrections

Risk:

If every user correction synchronously triggers full profile rebuild, routine image iteration becomes slow and infrastructure-heavy.

Final clarification:

Current explicit feedback affects the current task immediately.

Derived projections may rebuild asynchronously in the architectural sense of “later invocation/eventual consistency”, but the system must not promise background execution unless the host actually provides it.

Operationally:

```text
current task uses direct new correction now
future context builds include rebuilt projection when available
```

No synchronous full-distillation requirement exists.

Verdict: `PASS`.

---

# 7. Finding R4-06 — dataset-role release lifecycle is not yet fully decided

PHASE 3 defines:

```text
blind_eval_reserved
```

but does not fully specify whether a reserved sample can later become discovery evidence and how that history is preserved.

Risk:

Mutating the role without audit could erase evidence that a supposedly blind case had once been protected; never releasing it may reduce reuse flexibility.

Final PHASE 4 decision:

This remains **OPEN FOR ADR**.

Safest V0.1 default until PHASE 5 resolves it:

> Keep blind-eval-reserved samples isolated for the life of the initial evaluation set rather than mutating them casually.

A later evaluation manifest/release policy may authorize reuse while preserving the historical contamination barrier.

Verdict: `OPEN / NOT A PHASE-4 BLOCKER`.

---

# 8. Finding R4-07 — Asset Vault cannot be hand-waved because host accessibility differs

The user intends ChatGPT/Codex/GitHub-assisted workflows, but these runtimes do not necessarily share a filesystem.

Risk:

The architecture could store excellent local references that a cloud runtime cannot inspect, then silently continue as if the images were available.

Final clarification:

Every runtime context selection must distinguish:

```text
known sample
selected sample
resolvable sample
actually inspected sample
```

Only actually resolved visual bytes may support visual claims in that run.

Unavailability does not invalidate the user's historical preference evidence.

Asset-storage technology remains deferred, but **availability truthfulness is not deferred**.

Verdict: `PASS`.

---

# 9. Finding R4-08 — Preference Projection Builder must not become an autonomous rule engine

Risk:

A profile builder could slowly become a hidden `visual-distill` subsystem, creating global rules without `skill-refiner` review.

Final clarification:

Preference projections may influence one task's context.

They may not directly modify:

- `SKILL.md`;
- repository routing;
- promoted design rules;
- calibration raw truth.

A persistent behavior change to a production Skill must still go through `skill-refiner` + evaluation + Git review.

Verdict: `PASS`.

---

# 10. Finding R4-09 — Exemplar selection should remain inspectable before becoming semantic infrastructure

Risk:

Embedding search could be introduced because it appears architecturally elegant before simple metadata retrieval has failed.

Final clarification:

V0.1 retrieval must be explainable enough to answer:

```text
why was this sample selected?
what user evidence supports its role?
is its asset resolvable?
```

Embeddings are a future implementation option, not part of the current architecture requirement.

Verdict: `PASS`.

---

# 11. Finding R4-10 — “user acceptance” metrics cannot infer preference from silence

Risk:

A generation that receives no complaint might be counted as accepted and pollute evaluation metrics.

Final clarification:

Preference metrics must use explicit or reliably observable acceptance events.

Silence alone is not a positive personal-preference label.

Metrics are derived/evaluation data and never raw preference truth.

Verdict: `PASS`.

---

# 12. Finding R4-11 — existing route and memory context must not compete for prompt authority

Risk:

The selected visual Skill may already contain a strong visual grammar. Injecting an oversized personal context pack could override the Skill and recreate rule competition.

Final clarification:

VisualContextPack should primarily influence high-leverage choices such as:

- relevant positive/negative exemplars;
- current known user rejection patterns;
- small scoped preferences;
- explicitly confirmed cross-domain constraints.

It should not reproduce the entire visual Skill or append an alternate full design grammar.

The final renderer prompt should remain compact in line with `AESTHETIC_SKILL_DESIGN_CHARTER.md`.

Verdict: `PASS`.

---

# 13. Finding R4-12 — architecture must not require a permanent “LIU VISUAL SYSTEM Skill”

Risk:

The project name itself may create pressure to package everything into a named Skill.

Final clarification:

LIU VISUAL SYSTEM is an architecture/system label.

A dedicated Skill is optional later.

The architecture is valid if the host uses:

```text
repository policy / runtime integration
+
small data/retrieval layer
+
existing visual Skills
```

without any new top-level personal visual Skill.

Verdict: `PASS`.

---

# 14. Catastrophic migration simulation

Assume in 2027 all of the following are replaced:

```text
profile builder
retrieval algorithm
critic version
prompt compilers
renderer
VisualContextPack format
domain taxonomy
calibration mapping
```

Expected impact:

## Must survive unchanged in meaning

```text
Sample IDs
Asset identities/hashes
raw user EvidenceEvents
A/B decisions
user revision requests
corrections/retractions
GenerationRecords
provenance
```

## May be rebuilt

```text
effective evidence view
profiles
anti-pattern summaries
exemplar ranks
calibration compatibility view
evaluation indexes
```

## May require code migration

```text
storage serialization
runtime interfaces
prompt integration
asset locator implementation
```

Conclusion:

The proposal protects the irreplaceable human work even when substantial upper-layer code is rewritten.

This satisfies the project's actual “avoid future big rework” goal more realistically than trying to prevent all refactoring.

---

# 15. Architecture simplicity check

Question:

> If forced to implement only 30% of the proposal, what remains essential?

Answer:

```text
1. PHASE 3 raw records
2. simple effective-evidence replay
3. simple exemplar selection
4. bounded context pack
5. existing visual route
6. generation logging
7. direct feedback capture
```

Everything else can be added later.

This confirms the architecture has a viable thin slice and is not all-or-nothing.

---

# 16. PHASE 5 ADR candidates after self-review

Recommended ADR topics are now narrowed to:

```text
ADR-01 Raw record serialization/storage location
ADR-02 Asset Vault and runtime resolution policy
ADR-03 Derived artifact placement/rebuild/version policy
ADR-04 Calibration compatibility projection
ADR-05 VisualContextPack runtime integration and size budget
ADR-06 Blind-eval reservation/release policy
ADR-07 Evidence capture trigger and faithful historical import policy
ADR-08 Skill-refiner bridge and non-automatic promotion boundary
ADR-09 Single-writer/migration/versioning implementation policy
```

A separate ADR for microservices is unnecessary because microservices are rejected for the pilot.

A separate ADR for embeddings is unnecessary until evidence shows they are needed.

---

# 17. PHASE 4 exit-gate result

| Gate | Result |
|---|---|
| based on four-family PHASE 3 Data Contract | PASS |
| no duplicate raw preference authority | PASS |
| existing repo routing reused | PASS |
| existing critic reused without forcing universal coverage | PASS |
| existing skill-refiner remains sole Skill promotion authority | PASS |
| calibration dual-authority risk addressed | PASS |
| current task precedence explicit | PASS |
| raw/derived write permissions explicit | PASS |
| asset accessibility across runtimes addressed | PASS |
| blind-eval contamination addressed | PASS, lifecycle ADR remains open |
| failure fallback behavior specified | PASS |
| derived rebuild path specified | PASS |
| alternative architectures considered | PASS |
| logical components do not imply services | PASS |
| embedding/vector/object-store infrastructure remains deferred | PASS |
| no new Skill created or modified | PASS |
| no schema/validator/script/scaffold created | PASS |
| no images imported | PASS |
| no architecture freeze performed | PASS |

Final verdict:

```text
PHASE 4 — PASS / PROPOSAL ONLY
```

Stop here.

Do not begin PHASE 5 ADR creation in this phase.
