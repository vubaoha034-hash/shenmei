# LIU VISUAL SYSTEM — PHASE 2 RED TEAM

Status: `PHASE_2 / RED_TEAM_COMPLETE`

Date: `2026-08-12`

Scope: attack the current LIU VISUAL SYSTEM proposal before Data Contract work. This phase does **not** create a final Skill, scaffold, production schema, asset migration, or architecture freeze.

---

## 0. Evidence boundary

This audit uses three evidence classes and keeps them separate.

### A. Repository facts verified on `vubaoha034-hash/shenmei@main`

Primary evidence inspected:

- `AGENTS.md`
- `START_HERE.md`
- `AESTHETIC_SKILL_DESIGN_CHARTER.md`
- `skills/skill-refiner/SKILL.md`
- `skills/skill-refiner/references/PROMOTION_POLICY.md`
- `skills/skill-refiner/references/INTEGRATION.md`
- `skills/skill-refiner/scripts/evolve.py`
- `skills/personal-aesthetic-critic/SKILL.md`
- `config/rubric.v1.json`
- `calibration/anchors.json`
- `skills/gc-travel-zine-poster-v1/SKILL.md`
- commit `0cc46237f34b5676f581ddfcea2c641fd0b6c303`

### B. PHASE 1 facts reported by the user

Reported but not independently available in the current `main` tree during this audit:

- `PHASE_1_REFERENCE_AUDIT.md`
- `PHASE_1_EVIDENCE_LEDGER.md`
- 16 reviewed systems / official Skills
- 18 fields per system
- 32 unique source links

These claims are treated as **reported PHASE 1 results**, not as files this audit pretends to have read.

### C. External source re-verification

Selective high-load-bearing PHASE 1 claims were rechecked against current upstream material:

- OpenAI Product Design router: `openai/role-specific-plugins/plugins/product-design/skills/index/SKILL.md`
- OpenAI Product Design QA separation: `.../design-qa/SKILL.md`
- Anthropic Skill Creator: `anthropics/skills/skills/skill-creator/SKILL.md`
- Anthropic Blind Comparator: `.../agents/comparator.md`
- Vercel DS Skills Pipeline: `vercel-labs/design-systems-to-agent-skills`
- Google Labs Stitch / DESIGN.md: `google-labs-code/stitch-skills` and `google-labs-code/design.md`

---

# 1. Executive verdict

## Verdict

The original LIU VISUAL SYSTEM direction is **valid**, but the proposed V0.1 is materially over-engineered if implemented literally.

The largest error is not any single component. It is the assumption that because a future mature system may eventually need event history, profiles, retrieval, evaluation, renderer abstraction, rule lifecycle, multiple Skills, large asset storage, migration tooling, and preference modeling, **all of those abstractions should exist in V0.1**.

That assumption fails the YAGNI test.

The repository already contains direct evidence of the same failure pattern: a visual Skill became too large and rule-heavy, then was deliberately reverted to a thin wrapper. Commit `0cc46237f34b5676f581ddfcea2c641fd0b6c303` changed `skills/gc-travel-zine-poster-v1/SKILL.md` from 442 lines to 115 lines, deleting 395 lines while restoring upstream-first behavior. The current charter explicitly records this class of failure as an anti-pattern.

Therefore PHASE 2 recommends:

1. **Freeze raw evidence semantics early, not Skill topology.**
2. **Reuse the existing `skill-refiner` evidence/candidate/evaluation machinery instead of building a second rule-lifecycle subsystem.**
3. **Treat examples and user decisions as the primary long-term asset; treat derived rules as replaceable projections.**
4. **Keep personal preference modeling case-based at first. Do not build a trained Preference Model in V0.1.**
5. **Do not create Router + five new visual Skills in V0.1.** Existing repository routing is already substantial.
6. **Do not build a full renderer adapter framework, object-store URI abstraction, near-duplicate service, embedding infrastructure, or ML-style train/dev/holdout pipeline in V0.1.** Preserve seams, not implementations.
7. **Keep evaluation separated from discovery, but use domain-neutral names such as `discovery`, `regression`, and `blind_eval` unless actual model training begins.**
8. **Retire fixed personal-aesthetic score weights as a source of truth.** They can remain diagnostic until real calibration evidence exists.

The simplest viable architecture is not “a new visual operating system made of many Skills.” It is:

> **stable sample identity + raw feedback events + comparison/revision relations + derived profiles + selective exemplar retrieval + existing critic + existing evidence-gated refiner.**

---

# 2. PHASE 1 evidence problems and attribution corrections

## 2.1 Completeness is not validity

A report with 16 × 18 populated fields demonstrates process completeness. It does not by itself establish:

- independence of sources;
- correctness of implementation interpretation;
- applicability to a single-user visual preference system;
- necessity of every proposed requirement;
- absence of copied assumptions between projects;
- currentness of every upstream implementation.

PHASE 2 therefore rejects “all fields complete” as an architecture gate.

## 2.2 Anthropic held-out attribution needs narrowing

Current Anthropic Skill Creator does support:

- baseline vs with-Skill runs;
- blind A/B comparison through a separate comparator;
- post-hoc analysis;
- human review loops.

It also uses a 60/40 train/held-out split in **description trigger optimization**.

However, that does **not** establish a general HOLDOUT protocol for visual output-quality evaluation across the entire Skill Creator workflow.

Correct attribution:

> Anthropic provides blind comparison and baseline evaluation broadly, and a held-out split specifically for trigger-description optimization. A general visual `blind_eval` partition for LIU VISUAL SYSTEM is our engineering adaptation, not something to attribute wholesale to Anthropic.

## 2.3 OpenAI Product Design router claim is valid but not automatically transferable

OpenAI Product Design currently has an explicit router-only index and focused workflows such as user-context, ideate, audit, and design-qa. It also instructs focused workflows to inspect only the saved references needed for the current task.

That validates the **pattern**, not the necessity of reproducing the same number of Skills here.

OpenAI Product Design has several distinct production workflows. LIU VISUAL SYSTEM V0.1 initially has one user and one core objective: improve visual generation by preserving and retrieving preference evidence. The routing complexity is not equivalent.

## 2.4 Vercel pipeline claim is strong but domain-limited

Vercel's design-system-to-agent-skills project persists source-derived artifacts and extracts verified facts from actual design-system source code. This is a strong precedent for:

- source truth vs derived artifacts;
- deterministic extraction;
- persisted intermediate artifacts;
- validation against a source of truth.

But a source-code design system is more deterministic than human aesthetic preference. The pattern transfers; the confidence level does not.

## 2.5 Stitch / DESIGN.md claim is useful with a boundary

Google Labs' DESIGN.md / Stitch ecosystem supports persistent design-system representation separate from individual generation requests. This strongly supports separating a durable design profile from a task prompt.

It does not prove that one universal personal `VISUAL_DNA.md` is the correct representation for heterogeneous personal taste.

---

# 3. Repository evidence that changes the design

## 3.1 The repository already has an evidence lifecycle

`skills/skill-refiner/` already implements:

```text
observation
→ candidate
→ evaluation
→ gate decision
→ Git promotion
→ compaction/archive
```

The state is kept outside the target Skill under `.skill-evolution/<target>/state.json`.

This directly overlaps the proposed new `visual-distill` rule lifecycle.

### Red-team conclusion

Creating another independent:

```text
candidate rule
→ evidence
→ active rule
→ deprecated rule
```

system would create duplicate authorities and drift.

**Default decision: reuse or extend `skill-refiner`; do not create a parallel rule-promotion engine in V0.1.**

## 3.2 The repository already has pairwise and before/after logic

`skills/personal-aesthetic-critic/SKILL.md` already includes:

- anonymized A/B ranking;
- pairwise comparison;
- before/after evaluation;
- personal calibration anchors;
- separate technical, task, and personal-fit reasoning.

Therefore the new system should primarily improve **persistence and provenance** of those events rather than inventing new evaluation concepts.

## 3.3 Personal calibration is currently not established

`calibration/anchors.json` currently has:

```text
status: PERSONAL_CALIBRATION_PENDING
anchors: []
```

This is a critical fact.

The system currently has sophisticated personal-fit logic but no actual stored personal visual anchors in the calibration file.

### Red-team conclusion

The immediate bottleneck is not a more advanced preference model. It is collecting trustworthy anchors and feedback events.

## 3.4 Fixed score weights already exist before calibration

`config/rubric.v1.json` contains fixed per-category weights such as composition, typography, color, story, originality, personal fit, etc.

Those weights may be useful as a professional diagnostic rubric, but they are not evidence that they represent the user's personal utility function.

### Risk

If these weights are allowed to become the optimization target, the system may optimize for a professionally tidy score while missing the user's actual preference.

### Decision

Keep weighted scoring as **diagnostic**, not as ground truth for personal taste.

## 3.5 The repository has already experienced rule-bloat failure

The current `AESTHETIC_SKILL_DESIGN_CHARTER.md` explicitly warns:

- keep visual Skills compact;
- find 5–8 high-leverage variables;
- distinguish correctness from taste;
- prefer thin wrappers around mature upstream Skills;
- delete rules when outputs become rigid or template-like.

Commit `0cc462...` is concrete evidence that this was not hypothetical. A large local travel-zine Skill was reduced dramatically and restored to upstream-first execution.

### Red-team conclusion

Any LIU VISUAL SYSTEM architecture that starts by creating many new rules, validators, failure codes, or sub-Skills is contradicting the repository's strongest learned lesson.

---

# 4. Logical leaps in the original proposal

## L01 — “No existing system has every feature” ⇒ “we need every feature”

Invalid.

A missing feature may indicate either:

- an unmet requirement; or
- an unnecessary abstraction.

Every requirement must be justified by user value and deferral cost.

## L02 — “Personal taste is learnable” ⇒ “there is one stable Visual DNA”

Not established.

The user can simultaneously prefer:

- clean dark sci-fi;
- bright food imagery;
- editorial travel zines;
- restrained branding;
- expressive collage.

A small cross-domain core may exist, but it must emerge from evidence. It must not be assumed.

## L03 — “A/B is better than scores” ⇒ “A/B identifies causality”

False when several variables change at once.

Natural pairs capture preference ordering, not necessarily why.

## L04 — “Before/After is high-value” ⇒ “the change explains improvement”

False when multiple variables change in the same revision.

Before/After preserves historical evidence; causal attribution requires confidence and sometimes controlled variants.

## L05 — “Future renderers may change” ⇒ “build renderer adapters now”

Premature.

A stable generation record containing renderer/model/version/input/output is enough to preserve a future extraction seam.

## L06 — “Future storage may change” ⇒ “support file://, s3://, r2://, gs:// now”

Premature.

Relative path + content hash + source metadata is enough for the pilot.

## L07 — “ML systems use TRAIN/DEV/HOLDOUT” ⇒ “this system should use those exact partitions”

Potentially misleading.

V0.1 is primarily a preference evidence/retrieval system, not a trained ML model.

The principle to preserve is **evaluation separation**, not ML vocabulary.

## L08 — “Progressive disclosure works” ⇒ “everything should be dynamically retrieved”

Unsafe.

A retrieval miss can omit a critical user constraint. A tiny always-loaded core plus task-specific retrieval is safer.

## L09 — “AI Critic can score work” ⇒ “AI Critic can stand in for personal taste”

Unproven.

Generic aesthetic judgment and personal preference prediction are different tasks.

## L10 — “Benchmarks protect regressions” ⇒ “a fixed benchmark proves long-term improvement”

False.

A static suite can overfit. Production failures and rotating blind cases are required.

## L11 — “Immutable events are auditable” ⇒ “events can never be corrected”

Incorrect.

Historical events should be append-only, but their effective status must support supersession, retraction, privacy deletion, and corrected interpretation.

## L12 — “Rules are explainable” ⇒ “rules should be the dominant preference representation”

Not established.

Visual taste may be better represented by:

- a small stable rule set;
- retrieved exemplars;
- pairwise history;
- domain profiles;
- recent task context.

Case-based reasoning is likely more faithful than hundreds of explicit rules.

---

# 5. Requirements that are actually necessary

The detailed verdict is in `PHASE_2_REQUIREMENT_TRIAGE.md`.

The minimum requirements that survive Red Team are:

1. stable sample identity;
2. content hash for exact-duplicate detection;
3. raw user feedback preserved verbatim;
4. correction / supersession semantics;
5. provenance;
6. comparison relation when A/B feedback occurs;
7. revision relation when Before/After occurs;
8. raw vs derived separation;
9. schema version on durable records;
10. derived artifacts rebuildable from raw records;
11. evaluation evidence separated from the evidence used to derive preferences;
12. current explicit user instruction outranks inferred historical preference;
13. scope separation so domain-specific feedback does not silently become global;
14. minimal retrieval of relevant exemplars;
15. a path for evidence-gated promotion using the existing `skill-refiner` rather than automatic self-modification.

---

# 6. Requirements that are premature

The following are plausible later features but should not be implemented in V0.1 unless the pilot proves need:

- full Router + five new visual Skills;
- dedicated `visual-distill` promotion engine;
- trained Preference Model;
- embeddings/vector DB;
- full renderer adapter interface;
- object storage abstraction layer;
- universal asset URI scheme;
- near-duplicate image service;
- automatic clustering pipeline;
- fixed domain taxonomy hierarchy;
- large static benchmark;
- automatic rule promotion;
- multi-user support;
- distributed/multi-agent ledger merging;
- 10,000-sample optimizations.

---

# 7. Requirements that should be rejected in V0.1

## 7.1 Fixed personal-aesthetic weights as ground truth

Reject.

They can remain diagnostic but must not define the user's preference function.

## 7.2 Universal `LIU VISUAL DNA` as a mandatory single ontology

Reject as an assumption.

Allow evidence to determine whether a small cross-domain core emerges.

## 7.3 Automatic LLM rule promotion

Reject.

LLM hypotheses may be recorded as candidates. Promotion remains evidence-gated and reviewable.

## 7.4 GitHub as the primary bulk image store

Reject.

Git should store code, metadata, small canonical fixtures, and reviewable derived artifacts. Bulk image storage must remain separable.

---

# 8. Overengineering risks

## 8.1 Duplicate authority

A new visual rule lifecycle would overlap `skill-refiner`.

Result:

```text
visual rule state
!=
skill-refiner state
```

No clear source of truth.

## 8.2 Router explosion

The repository already has substantial root routing in `AGENTS.md` and `START_HERE.md` plus multiple visual Skills.

Adding six more narrow visual Skills before the data layer exists can increase:

- trigger collisions;
- missed routes;
- cross-Skill state ambiguity;
- maintenance burden;
- debugging surface.

## 8.3 Schema theater

Adding fields merely because they may be useful later creates false maturity. Every V0.1 field must have a writer, reader, and reason.

## 8.4 Infrastructure before evidence

The current personal calibration store is empty. Building vector retrieval, model training, object storage, and large eval suites before collecting anchors would optimize infrastructure around missing data.

---

# 9. Data-model risks

## 9.1 Sample identity vs asset identity

A file is not automatically a sample.

Need to distinguish at least conceptually:

- exact asset blob;
- logical visual sample;
- derived/cropped/recompressed variant.

Do not solve every derivative relationship in V0.1, but do not collapse them into one ID.

## 9.2 SHA256 is exact duplicate detection only

It will not detect resized, recompressed, cropped, watermarked, or color-adjusted copies.

V0.1 should support exact duplicate detection and leave a clean seam for later perceptual dedupe.

## 9.3 Raw feedback needs retraction semantics

Example:

```text
Event 1: “I like the red accent.”
Event 2: “I meant only in this sci-fi image, not generally.”
```

Event 1 remains historical evidence but must no longer project into a global preference.

A superseding/corrective event is sufficient; hard mutation is not required.

## 9.4 Scope must be explicit enough to stop leakage

Minimum useful scopes:

- task-only;
- domain/profile;
- global candidate;

Do not create a deep ontology yet.

---

# 10. Pairwise preference risks

Pairwise preference is useful, but two modes must be distinguished conceptually.

## Natural pair

Two naturally produced versions differ in many variables.

Value:

- strong ordering evidence;
- weak causal evidence.

## Controlled pair

One intended variable changes while others are held approximately stable.

Value:

- stronger causal evidence;
- higher generation/labeling cost.

V0.1 does not need separate storage systems for the two. It needs an optional `comparison_context` / `changed_dimensions` / confidence field or equivalent.

---

# 11. Before→After risks

Before/After should be stored because it is valuable historical evidence.

But the system must not automatically infer:

```text
changed X
→ user liked after
→ X caused improvement
```

Attribution should be expressed as one of:

- user-stated;
- controlled enough to infer;
- model hypothesis;
- unknown.

Unknown is a valid result.

---

# 12. Preference drift

Historical evidence and active preference are different layers.

A robust system must allow:

```text
historical truth: preserved
current projection: changed
```

Recency can be a signal, but it must not automatically erase old evidence. A newer explicit correction is stronger than passive recency.

---

# 13. Context leakage

A sci-fi correction such as:

> “Keep one red operational accent.”

must not automatically become a food-poster rule.

The initial precedence should be treated as a hypothesis for PHASE 3, not frozen here:

```text
current explicit instruction
> current task context
> same-domain confirmed preference
> cross-domain stable preference
> weak historical inference
```

The key invariant is simpler:

> **Current explicit instruction always beats inferred history.**

---

# 14. Critic risks

The current critic is useful but has four distinct jobs that must remain conceptually separated:

1. technical QA;
2. explicit requirement compliance;
3. professional aesthetic critique;
4. personal taste prediction.

Only the first two are strong candidates for deterministic blockers.

Professional aesthetic quality and personal taste should remain advisory until calibrated.

The system should never report an AI-generated `personal_fit` as if it were user truth without anchor evidence.

---

# 15. Benchmark risks

A single fixed benchmark can fail through:

- contamination;
- prompt leakage;
- test memorization;
- judge bias;
- renderer randomness;
- overrepresentation of one domain;
- regression suite ossification.

Recommended evaluation structure for the pilot:

```text
small fixed regression cases
+
small blind/rotating cases
+
real production failures added over time
```

Do not create a large numbered benchmark before real failures exist.

---

# 16. Cost attack

## Small: 50–100 samples

Likely dominant cost:

- human selection;
- user feedback;
- image inspection;
- metadata cleanup.

Infrastructure should be trivial.

## Medium: 500–1,000 samples

Likely new costs:

- duplicate management;
- retrieval quality;
- profile drift;
- re-analysis cost;
- maintaining useful evaluation cases.

Embeddings may become justified here, but only if ordinary metadata + exemplar retrieval is failing.

## Large: 10,000 samples

Potential needs:

- object storage;
- perceptual dedupe;
- vector search;
- batched derived rebuilds;
- data-quality jobs;
- stronger migration tooling.

These are not valid reasons to burden the 50-image pilot.

---

# 17. Human-effort budget

A successful system cannot require the user to label 20 fields per image.

Preferred user actions:

```text
喜欢
不喜欢
A 比 B 好
这个地方太脏
这个版本比上一版好
只适用于科幻，不是全局
```

The system may derive metadata, but raw user text remains the authoritative source event.

The most expensive long-term resource is likely not token cost. It is sustained, high-quality human preference feedback.

---

# 18. Security and third-party Skill risk

GitHub Skill research is valuable, but third-party Skills are executable instruction/code surfaces.

Default policy:

```text
REFERENCE FIRST
NOT AUTO-INSTALL
NOT AUTO-EXECUTE
```

Before code reuse:

- inspect license;
- inspect scripts;
- inspect network/file/credential behavior;
- pin source revision where practical;
- separate architecture ideas from copied implementation.

---

# 19. Alternative architecture challenge

## Architecture A — Full Event Platform

```text
Asset Registry
+ Event Store
+ Derived Profiles
+ Vector Retrieval
+ Rule Lifecycle
+ Router
+ Context Skill
+ Director Skill
+ Critic Skill
+ Eval Skill
+ Renderer Adapters
```

### Strengths

- maximally explicit;
- scalable;
- highly auditable.

### Weaknesses

- very high V0.1 complexity;
- duplicates existing repo mechanisms;
- large maintenance surface;
- high probability of building abstractions before evidence.

### Verdict

`DEFER` as a future architecture, not V0.1.

---

## Architecture B — Evidence Core + Case Retrieval

```text
Sample Registry
+ Raw Feedback Events
+ Pair/Revision Relations
+ Derived Preference Profiles
+ Exemplar Retrieval
+ existing personal-aesthetic-critic
+ existing skill-refiner
```

### Strengths

- preserves irreplaceable evidence;
- reuses current repository capabilities;
- few new moving parts;
- easily rebuildable;
- supports later embeddings/modeling without migration of human labels.

### Weaknesses

- less automation initially;
- manual/LLM retrieval may be enough only for small/medium scale;
- requires discipline in raw-vs-derived separation.

### Verdict

`RECOMMENDED SVA`.

---

## Architecture C — Profile Document First

```text
small reference library
→ curated DESIGN/PROFILE.md
→ task prompt
→ image generation
→ critic
```

### Strengths

- extremely simple;
- fast to pilot;
- easy for agents to consume.

### Weaknesses

- weak provenance;
- preference corrections may overwrite history;
- harder to rebuild when summaries are wrong;
- limited support for A/B and revision evidence.

### Verdict

Useful as a derived output format, insufficient as the only durable system.

---

## Architecture D — Learned Preference Model

```text
labeled dataset
→ embeddings/features
→ ranking/reward model
→ generator selection
```

### Strengths

- potentially powerful at scale.

### Weaknesses

- needs substantial clean data;
- opaque failure modes;
- much harder evaluation;
- model/version dependency;
- premature with zero persisted anchors in the current calibration store.

### Verdict

`REJECT V0.1 / REVISIT ONLY AFTER DATA`.

---

# 20. Simplest Viable Architecture (SVA)

This is a PHASE 2 recommendation, **not an architecture freeze**.

```text
                 ┌───────────────────┐
                 │  visual assets     │
                 │  local / external  │
                 └─────────┬─────────┘
                           │
                  stable sample record
                           │
                ┌──────────▼──────────┐
                │ raw evidence events │
                │ feedback / compare  │
                │ revision / correction│
                └──────────┬──────────┘
                           │
                    rebuildable derive
                           │
             ┌─────────────▼─────────────┐
             │ preference/profile views  │
             │ + exemplar retrieval      │
             └─────────────┬─────────────┘
                           │
             ┌─────────────▼─────────────┐
             │ task design context       │
             └─────────────┬─────────────┘
                           │
                    generation / edit
                           │
             ┌─────────────▼─────────────┐
             │ existing visual critic    │
             └─────────────┬─────────────┘
                           │
                  user accepts/rejects
                           │
                           └─────→ raw event

Repeated stable evidence
        │
        └────→ existing skill-refiner → reviewable candidate change
```

### What is intentionally missing

- no new multi-Skill router;
- no vector DB;
- no trained preference model;
- no full renderer framework;
- no object-store abstraction;
- no automatic rule promotion;
- no large taxonomy;
- no large benchmark.

This is intentional, not incomplete engineering.

---

# 21. Pre-mortem — assume the project failed after one year

| # | Failure mode | Likely cause | Early signal |
|---|---|---|---|
| 1 | Rules become an encyclopedia | every rejection becomes a rule | Skill/docs grow every week |
| 2 | Output becomes safe and generic | conflicting taste constraints | fewer bold variations |
| 3 | Old sci-fi rules leak into food work | bad scoping | irrelevant accents recur |
| 4 | User stops labeling | metadata burden | unlabeled backlog grows |
| 5 | LLM invents causal explanations | confounded A/B or revisions | explanations disagree with user |
| 6 | Critic rewards generic polish | generic-aesthetic bias | high scores on user-rejected work |
| 7 | Fixed weights become the target | rubric treated as truth | score rises, acceptance does not |
| 8 | Benchmark is gamed | static suite | benchmark improves, live tasks do not |
| 9 | Holdout is contaminated | same examples used in derivation | suspiciously perfect evals |
| 10 | Asset store becomes messy | identity rules unclear | duplicate/cropped samples proliferate |
| 11 | Git repo bloats | raw images committed directly | clone/pull slows |
| 12 | Derived profile becomes stale | no rebuild/version signal | profile contradicts recent feedback |
| 13 | Preference drift is ignored | old evidence always active | user repeatedly corrects old taste |
| 14 | One-off feedback becomes global | weak promotion gate | bizarre universal rules appear |
| 15 | New visual system duplicates refiner | separate lifecycle stores | conflicting active rules |
| 16 | Router misroutes | too many narrow Skills | same prompt produces inconsistent routes |
| 17 | Retrieval misses critical context | all context is dynamic | explicit stable preference omitted |
| 18 | Context becomes huge | “just in case” retrieval | prompt length grows without quality gain |
| 19 | Renderer upgrade breaks behavior | prompts overfit one model | quality changes after model update |
| 20 | Third-party Skill compromises workflow | unreviewed code/instructions | unexpected file/network access |
| 21 | License provenance is lost | copied assets/instructions | unclear reuse rights |
| 22 | Before/After falsely teaches cause | many simultaneous edits | repeated wrong “lessons” |
| 23 | Pairwise labels are noisy | candidates differ too much | preference dimensions unstable |
| 24 | Automatic distillation self-reinforces errors | LLM candidate promoted too quickly | same bad assumption spreads |
| 25 | Architecture absorbs all attention | infra before sample collection | months pass with few real anchors |
| 26 | Multi-agent merge corrupts state | premature concurrency | duplicate/conflicting evidence IDs |
| 27 | User correction cannot invalidate old projection | no supersession semantics | wrong preference keeps resurfacing |
| 28 | Deletion/privacy request is impossible | literal immutability | raw data cannot be removed safely |
| 29 | Taxonomy locks the user into old categories | categories embedded in code | new style requires schema rewrite |
| 30 | “Visual DNA” becomes mythology | summary overclaims consistency | cross-domain rules have many exceptions |

---

# 22. Migration pre-mortem

| Future change | If designed badly | Target impact |
|---|---|---|
| schema v1→v2 | manual edit of thousands of records | catastrophic |
| asset storage local→object store | IDs tied to file path | catastrophic |
| taxonomy changes | domain names embedded in primary keys | moderate/catastrophic |
| renderer change | preferences encoded as model-specific prompt text | moderate |
| embedding model change | raw evidence discarded after indexing | catastrophic |
| rule representation changes | raw feedback replaced by summaries | catastrophic |
| Skill topology changes | data lives inside Skill directories | catastrophic |
| scoring rubric changes | only final scores were stored | moderate |
| user preference changes | history overwritten | loss of auditability |

### Primary mitigation

Protect:

- raw user text;
- stable sample identity;
- relations between samples;
- provenance;
- schema version.

Everything derived from those may be replaced.

---

# 23. What should be frozen early

Candidate `FREEZE EARLY` contracts for PHASE 3 review:

- raw evidence vs derived data boundary;
- stable logical sample identity semantics;
- verbatim feedback preservation;
- correction/supersession mechanism;
- provenance fields required for durable records;
- schema version on durable records;
- relation semantics for comparison and revision;
- ability to rebuild derived state;
- current explicit instruction outranks inferred history.

---

# 24. What should stabilize later

- profile structure;
- scope vocabulary;
- retrieval algorithm;
- rule representation;
- regression suite shape;
- critic rubric;
- taxonomy;
- storage backend;
- generation record details.

---

# 25. What should never be treated as permanently frozen

- image model;
- prompt format;
- score weights;
- embedding model;
- visual taxonomy;
- Skill count;
- router topology;
- named style families;
- inferred “Visual DNA” statements.

---

# 26. Recommended corrections before PHASE 3

PHASE 3 should design a Data Contract around the SVA rather than around the original maximal architecture.

Mandatory corrections:

1. Replace literal immutable-event language with **append-only history + supersession/retraction projection semantics**.
2. Keep raw feedback verbatim and separate from model interpretation.
3. Separate logical sample identity from binary asset identity.
4. Do not use domain taxonomy in immutable IDs.
5. Store pairwise and revision relations without claiming causality.
6. Include attribution confidence/source for derived causal interpretations.
7. Add a small scope concept sufficient to prevent domain leakage.
8. Define an eval-role field without locking into ML `TRAIN/DEV/HOLDOUT` vocabulary.
9. Reuse existing `skill-refiner` lifecycle rather than create a duplicate rule engine.
10. Keep renderer/model metadata in generation records but defer a renderer adapter framework.
11. Keep asset location simple for pilot; no multi-scheme URI abstraction yet.
12. Treat weighted aesthetic scores as diagnostics, not personal truth.
13. Design the contract so current `personal-aesthetic-critic` can consume anchors later without forcing its current rubric into the data model.

---

# 27. PHASE 2 exit gate

- [x] Selectively rechecked PHASE 1 high-load-bearing upstream claims
- [x] Identified attribution boundary on Anthropic held-out behavior
- [x] Challenged original architecture with at least three alternatives
- [x] Triaged core requirements in a separate document
- [x] Found more than 10 material design risks
- [x] Completed 20+ failure-mode pre-mortem
- [x] Completed migration pre-mortem
- [x] Defined a Simplest Viable Architecture
- [x] Identified features that should be deferred/rejected
- [x] Did not create a final Skill
- [x] Did not create scaffold
- [x] Did not import images
- [x] Did not freeze architecture

## PHASE 2 verdict

`PASS — READY TO DESIGN PHASE 3 DATA CONTRACT, WITH CORRECTIONS`

This PASS does **not** mean the original architecture passed unchanged. It means Red Team found sufficient evidence to simplify it before the next phase.

---

# 28. One-sentence design rule carried into PHASE 3

> Preserve what the user actually saw and said; make every interpretation, profile, rule, score, router, renderer binding, and Skill replaceable.
