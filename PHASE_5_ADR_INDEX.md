# LIU VISUAL SYSTEM — PHASE 5 ADR INDEX

Status: `ADR_SET_COMPLETE / NOT_ARCHITECTURE_FROZEN`
Date: `2026-08-12`
Branch: `phase-5-adr-20260812`

Purpose: record only architecture decisions whose wrong choice would create meaningful long-term migration cost, duplicate authority, privacy risk, evaluation contamination, or irreversible preference-data pollution.

---

# 1. Accepted V0.1 ADRs

| ADR | Decision | Why it deserves ADR status |
|---|---|---|
| `ADR-001-private-raw-store-and-single-writer.md` | Canonical raw personal data lives in a private file-based data root; EvidenceEvent is append-oriented; V0.1 is single-writer | Privacy, identity, persistence and future DB migration |
| `ADR-002-asset-vault-and-resolution-policy.md` | Bulk images stay outside public Git by default; logical sample identity is independent of asset location; runtimes must resolve before claiming inspection | Moving image storage later must not break preference history |
| `ADR-003-derived-artifacts-are-rebuildable-cache.md` | Profiles, summaries, embeddings, clusters, indexes and Visual DNA-like artifacts are replaceable derived projections | Prevents inference errors from becoming irreversible source truth |
| `ADR-004-calibration-is-a-derived-compatibility-view.md` | `calibration/anchors.json` becomes a compatibility projection from raw evidence, not a second preference authority | Avoids dual sources of personal truth and critic-taxonomy lock-in |
| `ADR-005-runtime-context-is-host-level-and-bounded.md` | Personal context is assembled at host/runtime before existing visual Skills; current explicit intent is highest authority; no mandatory new mega Skill | Prevents prompt/routing bloat while keeping integration replaceable |
| `ADR-006-skill-refiner-is-the-only-promotion-authority.md` | Existing `skill-refiner` is the sole durable production Skill-promotion mechanism | Prevents duplicate rule lifecycles and uncontrolled self-modification |
| `ADR-007-blind-eval-reservations-are-sticky-in-v0.1.md` | V0.1 blind-eval-reserved samples remain reserved for that evaluation pool | Avoids ambiguous contamination/release history before such machinery exists |
| `ADR-008-only-explicit-user-evidence-enters-raw-preference-ledger.md` | Only direct or traceably imported user evidence enters raw preference truth; silence/upload/critic output do not | Prevents irreversible preference-data contamination |

---

# 2. PHASE 4 candidates intentionally merged

PHASE 4 listed ten candidate ADR topics. PHASE 5 did not create ten documents mechanically.

## Raw storage format + single writer + migration policy

Merged into ADR-001 because these decisions are tightly coupled in V0.1. A second migration-policy ADR would add paperwork without a separate authority boundary.

## Asset vault + locator policy

Merged into ADR-002.

## Derived storage + rebuild policy

Merged into ADR-003.

## Calibration compatibility

ADR-004.

## Runtime VisualContextPack integration + existing Skill integration without prompt bloat

The runtime authority/precedence decision is ADR-005. Durable Skill changes remain separately governed by ADR-006.

## Blind-eval contamination control

ADR-007 resolves the previously open V0.1 lifecycle choice.

## Skill-refiner bridge semantics

ADR-006.

## User evidence capture trigger policy

ADR-008.

---

# 3. Decisions deliberately NOT promoted to ADR

The following remain implementation/tuning choices because changing them later should be cheap if the accepted ADR boundaries hold:

```text
UUIDv4 vs UUIDv7
exact private data-root directory name
number of exemplars retrieved per task
VisualContextPack serialization format
exact domain labels
embedding model
vector database choice
perceptual-hash algorithm
object storage vendor
renderer adapter classes
prompt compiler syntax
critic score weights
profile prose format
cluster algorithm
future thin entry Skill name
```

Do not freeze them merely to make the architecture appear complete.

---

# 4. Decisions still deferred

These are explicitly not V0.1 ADR requirements:

- trained preference/reward model;
- embeddings/vector DB;
- object-storage service selection;
- near-duplicate service;
- multi-user support;
- multi-agent concurrent raw writes;
- microservices/queues/workflow engine;
- universal Visual DNA ontology;
- automatic Skill promotion;
- giant benchmark;
- full renderer adapter framework.

---

# 5. ADR change policy

An accepted ADR may be superseded, but not silently edited into the opposite decision.

If a future phase needs to reverse an accepted decision:

1. create a new ADR;
2. mark the old ADR `SUPERSEDED_BY ADR-xxx`;
3. state migration impact;
4. preserve compatibility with existing stable raw IDs/evidence wherever possible;
5. do not rewrite history to pretend the earlier decision never existed.

---

# 6. What PHASE 5 does not mean

`ACCEPTED_FOR_V0.1` means these are the current decisions to carry into the implementation/freeze review.

It does **not** mean:

- the full architecture is frozen;
- production code exists;
- JSON Schemas exist;
- private storage exists;
- assets were imported;
- runtime context integration exists;
- Skills were changed;
- main was modified.

PHASE 5 remains an architecture-decision phase only.
