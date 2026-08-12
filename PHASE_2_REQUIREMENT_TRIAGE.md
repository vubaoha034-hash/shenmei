# LIU VISUAL SYSTEM — PHASE 2 REQUIREMENT TRIAGE

Status: `COMPLETE`

Date: `2026-08-12`

Purpose: decide which proposed requirements are genuinely needed in V0.1, which should be deferred, and which should be rejected before PHASE 3 Data Contract work.

Verdict values:

- `MUST` — necessary to protect user value / avoid catastrophic migration.
- `SHOULD` — valuable in V0.1, but implementation should stay minimal.
- `DEFER` — preserve a seam if cheap, but do not build the feature now.
- `REJECT` — do not implement as proposed in V0.1.
- `UNKNOWN` — evidence insufficient; do not freeze.

---

| Requirement | User Value | Evidence / Current State | Needed in V0.1? | Cost | Migration Cost if Deferred | Risk if Implemented Early | Risk if Deferred | Verdict | Reason |
|---|---|---|---|---|---|---|---|---|---|
| Stable logical sample identity | Prevents relabeling/relinking all history | Current calibration has no durable visual anchors yet; future evidence needs stable references | Yes | Low | Catastrophic if paths become identity | Low | High | MUST | Human feedback must attach to something stable independent of filename/location |
| Exact content hash | Detect exact duplicate blobs and integrity changes | Existing repo already uses hashes/SHA patterns in governance | Yes | Low | Moderate | Very low | Medium | MUST | Cheap now; useful for dedupe and integrity |
| Separate asset identity from sample identity | Prevents resized/recompressed copies becoming accidental new preference entities | SHA alone cannot model derivatives | Yes conceptually | Low | High | Low | High | MUST | Contract must not equate “file” and “logical sample” |
| Verbatim raw user feedback | Preserves irreplaceable preference evidence | Existing `skill-refiner` already distinguishes evidence from promoted rules | Yes | Low | Catastrophic | Very low | Critical | MUST | Summaries can be regenerated; original user statement cannot |
| Append-only evidence history | Auditability and rollback | Existing `skill-refiner` records observations before promotion | Yes, with correction semantics | Low | High | Medium if interpreted literally | High | MUST | Preserve history, but do not confuse history with current truth |
| Supersession/correction/retraction semantics | Handles “I said that wrong” and scope corrections | Not adequately represented by literal immutable-only proposal | Yes | Low | High | Low | High | MUST | Avoid stale wrong preference continuing to act |
| Privacy/deletion path | Allows raw evidence/assets to be removed when required | Literal immutability conflicts with deletion needs | Minimal path | Medium | High | Low | Medium/High | SHOULD | Do not design irreversible storage |
| Provenance for durable samples | Copyright traceability and source confidence | Reference library may contain third-party work | Yes | Low/Medium | High | Low | High | MUST | Source and author/platform should survive transformations when known |
| Raw vs derived physical/logical separation | Allows complete re-distillation | Core project goal | Yes | Low | Catastrophic | Low | Critical | MUST | This is the main anti-rework invariant |
| Schema version on durable records | Enables future migrations | Current repo already versions configs and rules | Yes | Low | High | Very low | High | MUST | Cheap and foundational |
| Full migration framework | Automates arbitrary future upgrades | No visual dataset exists yet | No | Medium/High | Low/Medium for small pilot | High complexity | Low | DEFER | Add migrations when first real schema change happens; do not invent a framework now |
| Minimal migration convention | Prevents ad-hoc manual rewrites | Schema will evolve | Yes | Low | Medium | Low | Medium | SHOULD | Define where migration scripts live and require idempotent/versioned upgrades later |
| Pairwise preference records | Captures relative preference better than scores in many cases | Current critic already uses blind pairwise ranking | When pairwise feedback occurs | Low | Medium | Low | Medium | SHOULD | Store naturally occurring A/B evidence, do not force every task into A/B |
| Controlled-pair experiment mode | Better causal inference | Natural pairs are confounded | No | Medium/high generation cost | Low | High workflow burden | Low | DEFER | Use only when a specific ambiguity justifies it |
| Before→After revision relation | Captures successful/failed edits | Current critic already has before/after protocol | When revisions occur | Low | Medium/High | Low | Medium | SHOULD | High-value evidence with minimal storage burden |
| Causal attribution from revisions | Explains why improvement happened | Often confounded | No automatic inference | Medium | Low | High false-learning risk | Low | REJECT | Store relation and attribution source/confidence; do not auto-causalize |
| Scope on preference evidence | Prevents sci-fi feedback contaminating food/design work | User works across heterogeneous visual domains | Yes, minimal | Low | High | Medium if taxonomy too deep | High | MUST | Need at least task/domain/global-candidate separation |
| Fixed visual taxonomy | Organizes profiles | Categories likely to evolve | No | Low/Medium | Low | High lock-in risk | Low | DEFER | Use configurable/free tags first; do not hard-code ontology into schema |
| Universal `LIU VISUAL DNA` document as source of truth | Easy mental model | Cross-domain consistency not proven | No | Low | Low | High oversimplification risk | Low | REJECT | Allow a small cross-domain core to emerge later as derived output |
| Domain/profile documents | Efficient context loading | Stitch/DESIGN.md pattern supports durable profile separate from task prompt | Minimal derived form | Low | Low | Medium if treated as truth | Medium | SHOULD | Useful as rebuildable projections, never raw truth |
| Exemplar retrieval | Grounds taste in actual cases | Current personal calibration is empty; examples are the immediate need | Yes, simple | Low/Medium | Medium | Low | High | MUST | Start with metadata/manual retrieval; sophistication can grow later |
| Embeddings/vector database | Scales semantic retrieval | No evidence yet that pilot needs it | No | Medium/high | Low | High infrastructure complexity | Low | DEFER | Add only after ordinary retrieval fails at scale |
| Automatic clustering | Discovers latent styles | No dataset yet | No | Medium | Low | High false-structure risk | Low | DEFER | Clusters may be useful later but should not shape V0.1 schema |
| Dedicated new `visual-distill` Skill | Encapsulates distillation | Existing `skill-refiner` already provides evidence→candidate→eval→promotion | No | Medium | Low | High duplicate-authority risk | Low | REJECT | Reuse/extend existing refiner and keep visual profile derivation separate |
| Rule lifecycle | Prevents one-off feedback becoming permanent | Existing `skill-refiner` already implements candidate/evaluation/promotion | Yes as capability | Low if reused | High if omitted entirely | High if duplicated | Medium | SHOULD | Reuse existing lifecycle; do not create another engine |
| Automatic rule promotion | Reduces manual review | LLM causal errors can self-amplify | No | Medium | Low | Critical | Low | REJECT | Candidate creation can be automated; promotion must remain evidence-gated/reviewable |
| Rule evidence/provenance | Makes derived statements auditable | Existing refiner already links evidence IDs | Yes for promoted preferences/rules | Low | Medium | Low | Medium | SHOULD | Every durable inferred rule should point to evidence |
| Rule compaction/anti-bloat | Prevents Skill growth | Existing charter and refiner already encode this | Yes by reuse | Low | Medium | Low | High | MUST | Repository has already experienced rule-bloat failure |
| Router + 5 new visual Skills | Clear responsibility separation | OpenAI Product Design uses router pattern, but repo already has many routes | No | Medium/high | Low | High routing/maintenance risk | Low | DEFER | Do not copy official topology without equivalent workflow complexity |
| One giant `liu-visual-director` Skill | Single entry point | Conflicts with compact-Skill charter | No | Medium | Low | High bloat/context risk | Low | REJECT | If a later entry Skill exists, keep it thin |
| Tiny always-loaded preference core | Avoids retrieval miss of truly global constraints | Progressive disclosure can miss critical context | Maybe | Low | Low | Medium if prematurely filled | Medium | SHOULD | Keep only confirmed cross-domain invariants; can initially be nearly empty |
| Fully dynamic preference retrieval | Minimizes context | Retrieval misses can omit critical constraints | No as exclusive strategy | Medium | Low | High omission risk | Low | REJECT | Use hybrid tiny core + selective retrieval |
| Professional aesthetic critic | Improves diagnosis | Existing `personal-aesthetic-critic` already strong | Yes by reuse | None/new | High if rewritten | Medium | Low | MUST | Reuse current critic; do not create duplicate critic in V0.1 |
| AI personal-taste score as ground truth | Easy automation | Current anchors are empty and `PERSONAL_CALIBRATION_PENDING` | No | Low | None | Critical false-confidence risk | Low | REJECT | Personal fit must remain unknown/null until evidence exists |
| Fixed personal aesthetic weights | Repeatable scoring | Current rubric has fixed weights but they are professional choices, not user utility | No as ground truth | None/new | None | High metric gaming risk | Low | REJECT | Keep only as diagnostic rubric if useful |
| Hard Gates for correctness | Prevents wrong text/identity/aspect/etc. | Existing charter explicitly separates correctness from taste | Yes | Low | Medium | Low | High | MUST | Appropriate place for deterministic blockers |
| Hard Gates for taste | Attempts to guarantee “high-end” | Charter explicitly warns against it | No | Low | None | Critical template/rigidity risk | Low | REJECT | Taste should not be disguised as correctness |
| Eval separation from discovery data | Prevents self-congratulating benchmark | Core validity requirement | Yes | Low | High | Low | High | MUST | Preserve principle even if not called train/dev/holdout |
| ML-style `TRAIN/DEV/HOLDOUT` naming | Familiar evaluation vocabulary | Current system is not training a model | No | Low | None | Medium conceptual confusion | Low | REJECT | Prefer role semantics such as discovery/regression/blind_eval |
| Small fixed regression set | Detects known failures | Existing refiner requires preservation cases | Yes | Low/Medium | Medium | Low | Medium | SHOULD | Start small and grow from real failures |
| Rotating blind evaluation cases | Reduces static-suite overfit | Anthropic supports blind comparator pattern | Useful after pilot | Medium | Low | Low | Medium | SHOULD | Small rotating set is enough; no giant suite |
| Large benchmark from day one | Looks rigorous | No real sample/history yet | No | High | Low | High maintenance/overfit | Low | REJECT | Let benchmark grow from production failures |
| Renderer/model metadata in generation records | Helps explain changes across model versions | Models will change | Yes | Low | High | Low | Medium | MUST | Record renderer/model/version without building adapter layer |
| Full renderer adapter framework | Makes swapping models elegant | Only one main renderer in V0.1 | No | Medium | Low | High abstraction tax | Low | DEFER | Preserve a generation contract seam instead |
| Renderer-neutral Visual DNA | Prevents model-specific preference lock-in | Valuable principle | Yes as constraint | Low | Medium | Low | Medium | SHOULD | Keep preference evidence about visible outcomes, not prompt syntax |
| Asset location abstraction field | Decouples storage path | Storage may move later | Minimal | Low | Medium | Low | Medium | SHOULD | Store logical asset reference/location separately from sample ID |
| Multi-scheme URI (`file://`, `s3://`, `r2://`, `gs://`) | Future storage portability | Pilot is local/small | No | Low/Medium | Low | Medium complexity | Low | DEFER | Relative path + optional origin is sufficient now |
| Bulk Git image storage | Easy versioning | Git binary bloat risk; images are not code | No | Low immediate | High later | High repository cost | Low | REJECT | Git stores metadata and small canonical fixtures only |
| External/object storage | Scales images | Not needed for pilot | No | Medium | Low | High infra overhead | Low | DEFER | Introduce only when local asset management stops scaling |
| Exact duplicate detection | Prevents repeated blobs | Cheap with hash | Yes | Low | Medium | Low | Medium | SHOULD | Implement alongside content hash |
| Perceptual/near-duplicate detection | Finds resized/cropped copies | Valuable at scale | No | Medium/high | Low | High tuning/compute cost | Low | DEFER | Leave seam; do not block pilot |
| Generation record/history | Connects inputs, model, output, user reaction | Needed for revision learning and regression | Yes, minimal | Low | High | Low | High | MUST | Preserve reproducibility context without storing every prompt essay as preference truth |
| Full prompt history as preference evidence | Easy to collect | Prompt may contain model artifacts and assistant guesses | No | Low | None | High contamination | Low | REJECT | Prompt is execution metadata, not user taste truth |
| User feedback event-triggered capture | Low-friction learning | Existing refiner integration already recommends event-driven evidence capture | Yes | Low | Medium | Low | Medium | SHOULD | Do not record routine success unless evidence-worthy |
| Mandatory metadata form for every image | Rich records | High human burden | No | High human cost | Low | Critical adoption risk | Low | REJECT | User interaction must stay minimal |
| Multi-user support | General product potential | Actual system is single-user | No | High | Low | Very high complexity | None | REJECT | Out of scope |
| Multi-agent concurrent evidence merge | Future agent scale | Existing refiner documents possible merge semantics | No | Medium | Low | High concurrency bugs | Low | DEFER | Single-writer workflow is enough now |
| Third-party Skill architecture research | Avoid reinventing good patterns | PHASE 1 already did this | Yes as research | Low | None | Low | Low | SHOULD | Continue selectively, but do not auto-install |
| Third-party Skill auto-install/execute | Convenience | Supply-chain/prompt-injection risk | No | Low | None | Critical | Low | REJECT | Reference first; audit before code adoption |
| License tracking for copied code/assets | Legal/provenance hygiene | Upstream skills/assets may have different licenses | Yes when reused | Low | High | Low | High | SHOULD | Architecture ideas and code copying are different operations |
| 10,000-sample scalability requirement | Future-proofing | Current dataset not yet built | No | High | Usually manageable later if raw contract is sound | Critical overengineering | Low | REJECT | Design raw contracts to migrate; do not optimize runtime for hypothetical scale |

---

# Summary by verdict

## MUST

The V0.1 Data Contract should prioritize:

- stable logical sample identity;
- exact content hash;
- asset/sample identity separation;
- verbatim raw feedback;
- append-only history with correction semantics;
- provenance;
- raw/derived separation;
- schema versioning;
- scoped preference evidence;
- exemplar retrieval;
- anti-bloat / reuse of existing governance;
- reuse of current critic;
- correctness hard gates;
- evaluation separation;
- renderer/model metadata;
- minimal generation history.

## SHOULD

Implement minimally where cheap:

- deletion path;
- migration convention;
- pairwise relations;
- Before→After relations;
- derived profile documents;
- existing rule lifecycle reuse;
- rule evidence links;
- tiny confirmed global core;
- small regression set;
- rotating blind cases;
- renderer-neutral visible-outcome preference representation;
- asset location field;
- exact duplicate detection;
- event-driven feedback capture;
- license tracking when reuse occurs.

## DEFER

Do not build before evidence:

- full migration framework;
- controlled-pair lab mode;
- fixed taxonomy;
- embeddings/vector DB;
- automatic clustering;
- router + five new visual Skills;
- full renderer adapters;
- multi-scheme URI abstraction;
- object storage;
- near-duplicate service;
- multi-agent merge.

## REJECT for V0.1

- universal Visual DNA as mandatory truth;
- separate `visual-distill` promotion engine;
- automatic rule promotion;
- giant all-in-one visual Skill;
- fully dynamic retrieval with no stable core;
- AI personal-fit score as truth;
- fixed personal weights as truth;
- taste hard gates;
- ML TRAIN/DEV/HOLDOUT naming as architecture;
- large benchmark from day one;
- bulk Git image storage;
- prompt history as preference truth;
- mandatory heavy metadata forms;
- multi-user support;
- third-party Skill auto-install;
- 10k runtime optimization as V0.1 requirement.

---

# Gate for PHASE 3

PHASE 3 should only design fields for `MUST` and the minimal subset of `SHOULD` requirements needed to preserve data fidelity.

A `DEFER` item must not silently enter the Data Contract unless omitting a small seam would create a demonstrably expensive migration.

A `REJECT` item must not be reintroduced merely because an upstream project uses it.
