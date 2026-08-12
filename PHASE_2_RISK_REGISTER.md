# LIU VISUAL SYSTEM — PHASE 2 RISK REGISTER

Status: `COMPLETE`

Date: `2026-08-12`

Scale:

- Likelihood: `LOW / MEDIUM / HIGH / CRITICAL`
- Impact: `LOW / MEDIUM / HIGH / CRITICAL`

The register avoids pseudo-precise probabilities. Residual risk is the remaining risk after the proposed mitigation.

---

| Risk ID | Risk | Cause | Likelihood | Impact | Detection | Mitigation | Residual Risk | Affected Layer |
|---|---|---|---|---|---|---|---|---|
| R-001 | PHASE 1 evidence cannot be independently replayed from current `main` | Reported PHASE 1 artifacts are not present in the visible main tree | HIGH | MEDIUM | File/tree audit | Treat reported claims as reported; reverify load-bearing upstream claims; require future phase artifacts to be committed/pinned | LOW | Governance |
| R-002 | Upstream attribution is overstated | A pattern from one sub-workflow is generalized to an entire upstream system | MEDIUM | MEDIUM | Claim→source review | Record exact file/path and scope of each borrowed pattern; label inference separately | LOW | Research |
| R-003 | Anthropic held-out behavior is mischaracterized | Held-out split in trigger-description optimization is described as general output-quality holdout | MEDIUM | MEDIUM | Source audit | Narrow attribution; treat LIU blind evaluation split as our own adaptation | LOW | Evaluation |
| R-004 | Existing `skill-refiner` is duplicated by a new visual lifecycle | New `visual-distill` builds candidate/active/deprecated logic independently | HIGH | HIGH | Two ledgers or conflicting rule status | Reuse/extend existing evidence-gated refiner; one promotion authority | LOW | Skill evolution |
| R-005 | Raw feedback is overwritten by a summary | Convenience-driven normalization replaces verbatim user text | MEDIUM | CRITICAL | Compare event record to source interaction | Store raw text separately; derived interpretation is replaceable/versioned | LOW | Data |
| R-006 | Literal immutability preserves known-wrong feedback as active truth | No supersession/retraction state | HIGH | HIGH | User correction still affects later context | Append corrective/superseding event; compute current projection separately | LOW | Data |
| R-007 | Privacy/deletion request conflicts with append-only history | “Immutable” is implemented as physically undeletable | LOW/MEDIUM | HIGH | Deletion request cannot be fulfilled | Distinguish audit semantics from physical deletion; support tombstone/purge policy | LOW | Data/Governance |
| R-008 | Sample identity is tied to file path | Filename/move/storage migration changes identity | HIGH | CRITICAL | Broken feedback references after move | Stable logical sample ID independent of location; location stored separately | LOW | Data/Assets |
| R-009 | Binary asset and logical sample are conflated | One JPEG = one sample assumption | HIGH | HIGH | Resized/recompressed copies get separate histories | Separate asset/blob identity from logical sample identity | MEDIUM | Data/Assets |
| R-010 | SHA256 is mistaken for visual dedupe | Exact hash only catches byte-identical files | HIGH | MEDIUM | Resized/cropped copies appear as “new” | Document exact-dedupe limitation; defer perceptual dedupe until needed | MEDIUM | Assets |
| R-011 | Perceptual dedupe is built too early | Future-scale anxiety | MEDIUM | MEDIUM | Large image-processing subsystem before pilot | Defer; define only a future seam | LOW | Assets/Infrastructure |
| R-012 | Natural A/B comparisons are treated as causal experiments | Multiple visual variables differ at once | HIGH | HIGH | Inferred “reason” changes across similar pairs | Store preference ordering; track changed dimensions/source/confidence; allow unknown cause | MEDIUM | Preference |
| R-013 | Before→After is treated as proof of which edit worked | Several edits occur simultaneously | HIGH | HIGH | System promotes one arbitrary edit as rule | Preserve revision relation; causal attribution must be user-stated/controlled/hypothesis/unknown | MEDIUM | Preference |
| R-014 | One-off feedback becomes a global preference | LLM overgeneralizes isolated comment | HIGH | CRITICAL | Irrelevant rule appears in unrelated domain | Scope evidence; use candidate state; require repeated/authoritative evidence for global promotion | LOW/MEDIUM | Preference |
| R-015 | Domain-specific taste leaks into other domains | No scope boundary | HIGH | HIGH | Sci-fi/food/travel constraints cross-contaminate | Minimal task/domain/global-candidate scopes; current instruction overrides history | LOW | Context |
| R-016 | User preference drift is ignored | Old evidence has permanent equal force | HIGH | HIGH | Repeated user corrections of “old taste” | Preserve history but allow newer explicit correction/supersession and profile versioning | MEDIUM | Preference |
| R-017 | Recency blindly overwrites stable preference | Time decay is used as sole truth mechanism | MEDIUM | MEDIUM | Stable long-term preference disappears despite no correction | Explicit correction > recency; recency only a signal | LOW | Preference |
| R-018 | Universal Visual DNA invents consistency that is not real | Branding metaphor precedes evidence | HIGH | HIGH | Cross-domain core accumulates exceptions | Treat global core as derived hypothesis; permit multiple independent profiles | LOW/MEDIUM | Preference/Profile |
| R-019 | Fixed taxonomy becomes schema lock-in | Category names embedded in IDs or required fields | MEDIUM | HIGH | New visual family requires migration | Free/configurable tags; taxonomy versioned/derived, never in immutable identity | LOW | Data/Profile |
| R-020 | Too many narrow Skills cause routing collisions | OpenAI Product Design topology copied without equivalent need | MEDIUM/HIGH | HIGH | Same prompt triggers different routes; instructions compete | Defer new router topology; reuse current routes; add Skill only after workflow divergence is proven | LOW/MEDIUM | Skills/Routing |
| R-021 | One giant visual Skill becomes a rule dump | “Single source of truth” interpreted as one huge SKILL.md | HIGH | HIGH | Skill size grows; context becomes generic | Follow charter; thin entry + references only if needed; prefer data/profile layer | LOW | Skills |
| R-022 | Progressive disclosure omits critical preference | Everything is dynamically retrieved | MEDIUM | HIGH | User has to repeat stable hard preference | Tiny confirmed always-loaded core + selective retrieval | LOW/MEDIUM | Context/Retrieval |
| R-023 | Retrieval loads too much | “Just in case” context expansion | HIGH | MEDIUM/HIGH | Token cost rises; output becomes averaged/generic | Retrieval budget; top relevant exemplars; keep raw archive out of ordinary context | LOW | Retrieval |
| R-024 | Retrieval loads the wrong examples | Weak metadata or immature semantic index | MEDIUM/HIGH | HIGH | Visual direction contradicts requested domain | Start with transparent metadata/profile retrieval; inspect retrieved set; later benchmark retrieval relevance | MEDIUM | Retrieval |
| R-025 | Embeddings infrastructure becomes a premature dependency | Assumption that 10k samples are imminent | MEDIUM | MEDIUM | Vector DB exists before enough samples | Defer until metadata/manual retrieval fails measurably | LOW | Infrastructure |
| R-026 | Automatic clustering creates false style families | Small/noisy dataset | MEDIUM | HIGH | Clusters are unstable between reruns | Treat clusters as derived exploratory output; never source truth | MEDIUM | Derived/Profile |
| R-027 | LLM distillation errors self-amplify | Candidate interpretation automatically promoted | HIGH | CRITICAL | Same wrong rule influences future outputs, producing confirming data | No automatic promotion; evidence-gated candidate state; independent/user review | LOW/MEDIUM | Distillation |
| R-028 | AI critic and generator share the same blind spot | Same model family/rubric reinforces generic aesthetics | HIGH | HIGH | High critic scores on user-rejected images | Separate technical/requirement QA from taste; user preference is final signal; use blind human A/B where important | MEDIUM | Evaluation |
| R-029 | Professional rubric is mistaken for personal preference | Existing weights look objective because numeric | HIGH | HIGH | Scores improve while user acceptance does not | Keep weights diagnostic; personal-fit remains null until anchors; monitor acceptance/revision metrics | LOW/MEDIUM | Evaluation |
| R-030 | Taste is converted into hard correctness gates | Desire for deterministic quality control | HIGH | CRITICAL | Outputs satisfy rules but become rigid/template-like | Charter rule: hard-lock correctness, not taste; use advisory critique for taste | LOW | Evaluation/Skills |
| R-031 | Benchmark contamination | Same cases used to derive profiles and evaluate them | HIGH | HIGH | Unrealistically strong eval performance | Explicit eval-role separation; provenance; blind/rotating cases | LOW/MEDIUM | Evaluation |
| R-032 | Static benchmark overfits | Fixed cases become optimization target | MEDIUM/HIGH | HIGH | Benchmark rises; live acceptance flat | Fixed regression + rotating blind cases + production failures | MEDIUM | Evaluation |
| R-033 | Renderer randomness masks changes | Single run per condition | HIGH | MEDIUM/HIGH | Candidate appears better/worse due to sampling | Use pairwise repeated/controlled checks for high-stakes changes; avoid overreading one run | MEDIUM | Evaluation/Renderer |
| R-034 | Renderer/model upgrade is interpreted as preference drift | Generation behavior changes independently of user taste | MEDIUM | HIGH | Same prompt/profile yields different output after model change | Record renderer/model/version in generation history | LOW/MEDIUM | Generation |
| R-035 | Full renderer adapter framework becomes dead code | Only one actual renderer in V0.1 | MEDIUM | MEDIUM | Interfaces with one implementation, no real portability tests | Record generation contract seam; defer adapter classes | LOW | Architecture |
| R-036 | Prompt syntax is stored as Visual DNA | Model-specific execution details contaminate preference knowledge | HIGH | HIGH | New renderer cannot use profile cleanly | Store visible-outcome preference separately from renderer prompt/compiler | LOW | Preference/Generation |
| R-037 | Asset URI abstraction is overbuilt | Supporting hypothetical S3/R2/GCS simultaneously | MEDIUM | MEDIUM | Many unused schemes and resolver bugs | V0.1 uses stable logical ID + simple location field; add schemes on migration | LOW | Assets |
| R-038 | Git repository bloats with reference images | Git used as image warehouse | MEDIUM/HIGH | HIGH | Slow clone/pull, large history | Git stores metadata/small fixtures; bulk assets external/local | LOW | Assets/Git |
| R-039 | Asset provenance is lost during copying | Download/re-export strips source metadata | HIGH | HIGH | Cannot trace author/source/license later | Persist provenance in sample record independent of file metadata | LOW/MEDIUM | Assets/Governance |
| R-040 | Third-party Skill contains malicious instructions/scripts | GitHub Skill installed without review | MEDIUM | CRITICAL | Unexpected network/file/credential activity | Reference-first policy; inspect code/license; pin version; never auto-execute research Skills | LOW/MEDIUM | Security |
| R-041 | License-incompatible code/assets are copied | Architecture study turns into implementation copying | MEDIUM | HIGH | Unknown reuse terms | Track license per adopted code/asset; prefer idea-level adaptation | LOW | Governance |
| R-042 | Human labeling workload kills the project | Heavy form/schema requirements | HIGH | CRITICAL | Unlabeled backlog; user stops giving feedback | User actions stay minimal; derive metadata automatically; never require 20-field forms | LOW/MEDIUM | Human workflow |
| R-043 | System spends months on infrastructure before learning taste | Architecture perfectionism | HIGH | CRITICAL | Few real anchors despite large codebase | Pilot immediately after minimal Data Contract; measure real feedback volume | LOW | Program |
| R-044 | Existing calibration remains empty while new layers are added | Data collection is not prioritized | HIGH | HIGH | `anchors: []` persists | Make initial anchor collection the first post-contract milestone | LOW | Program/Preference |
| R-045 | Derived profiles become stale | No rebuild/version provenance | MEDIUM/HIGH | HIGH | Profile contradicts recent raw events | Derived version includes source event set/version; rebuild command/check | LOW/MEDIUM | Derived |
| R-046 | Raw and derived data are accidentally mixed | Convenience files contain both user truth and LLM inference | HIGH | CRITICAL | Cannot rebuild without preserving old inference | Separate namespaces/directories/contracts; validators reject derived fields in raw records | LOW | Data |
| R-047 | Data migration rewrites thousands of records manually | No schema version/migration convention | MEDIUM | CRITICAL | One schema change becomes a manual project | Schema version now; migration scripts when first change happens; raw backup | LOW | Data |
| R-048 | Multi-agent state writes race | Concurrency added prematurely | LOW now | HIGH | Duplicate/conflicting evidence/candidate IDs | Single-writer V0.1; defer merge protocol; Git review for promotions | LOW | Concurrency |
| R-049 | User explicit instruction loses to historical profile | Retrieval/profile has too much authority | MEDIUM/HIGH | CRITICAL | “I asked for X but system keeps doing Y” | Invariant: current explicit user instruction outranks inferred history | LOW | Runtime |
| R-050 | Repository instructions themselves become too large/contradictory | Continuous additions to AGENTS/START_HERE | HIGH | HIGH | Route conflicts, repeated warnings, outdated rules | Apply same anti-bloat policy to routing docs; consolidate and retire obsolete rules | MEDIUM | Governance/Routing |

---

# Highest-priority risks

The following risks deserve explicit PHASE 3 protection because their failure would create the most expensive rework:

1. `R-005` raw feedback overwritten;
2. `R-008` identity tied to path;
3. `R-014` one-off feedback promoted globally;
4. `R-027` auto-distillation self-amplification;
5. `R-030` taste converted into hard gates;
6. `R-031` benchmark contamination;
7. `R-036` renderer syntax stored as preference truth;
8. `R-042` human labeling burden;
9. `R-046` raw/derived mixing;
10. `R-049` historical profile overrides current explicit instruction.

---

# Risks intentionally accepted in V0.1

A minimal system should consciously accept several non-catastrophic limitations rather than solve them early:

- resized/cropped near duplicates may not be detected automatically;
- retrieval may initially rely on transparent metadata/manual selection rather than embeddings;
- domain profiles may be coarse;
- causal attribution from natural revisions may remain `unknown`;
- only one main renderer may be supported operationally;
- evaluation sets may initially be small;
- concurrent agent writes may be unsupported.

These limitations are acceptable because the raw evidence contract can preserve the data needed to solve them later.

---

# Risk posture for PHASE 3

PHASE 3 should optimize for **catastrophic-migration avoidance**, not abstraction completeness.

A future code rewrite is acceptable.

A future requirement to manually relabel hundreds or thousands of images and user decisions is not.
