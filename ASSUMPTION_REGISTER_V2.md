# LIU VISUAL SYSTEM — CRITICAL ASSUMPTION REGISTER V2

Status: `ACTIVE_CONTROL_DOCUMENT`
Date: `2026-08-13`

This register determines execution priority. Work must attack the highest-risk `FAILED` or `UNPROVEN` assumption before expanding already-proven infrastructure.

## Status vocabulary

- `PROVEN` — supported by direct execution evidence.
- `WEAK_EVIDENCE` — positive signal exists but is not robust enough for scale.
- `UNPROVEN` — plausible, but current evidence does not establish it.
- `FAILED` — current evidence contradicts the assumption.
- `NOT_NEEDED_YET` — intentionally deferred until upstream value is proven.

---

## A01 — Raw user evidence can be preserved without silent reinterpretation

Status: `PROVEN`

Evidence:
- append-oriented EvidenceEvent ledger exists;
- correction/supersede behavior was exercised after Windows encoding contamination;
- original incorrect events remained auditable rather than silently rewritten.

Next action: none unless regression appears.

---

## A02 — Logical sample identity survives file movement/storage change

Status: `PROVEN`

Evidence:
- Sample/Asset separation implemented;
- locator movement and stable IDs covered by synthetic tests;
- backup/restore preserved IDs and links.

Next action: none unless regression appears.

---

## A03 — Private raw store / backup / restore are operationally reliable on the real Windows host

Status: `PROVEN`

Evidence:
- Phase 8 Real Host PASS;
- independent data and backup disks;
- backup/restore, writer lock, purge and doctor checks passed on real host.

Next action: maintain, do not expand.

---

## A04 — Blind-eval evidence can be quarantined from Discovery

Status: `PROVEN`

Evidence:
- blind-reserved role exists;
- transitive quarantine implemented/tested;
- Attempt 1 contamination was stopped rather than repaired into the live study.

Caveat:
- blind-safe presentation path still requires execution discipline.

---

## A05 — Domain-level restaurant retrieval finds in-domain approved/rejected references

Status: `PROVEN_BUT_COARSE`

Evidence:
- restaurant Retrieval Sanity Check returned only restaurant-domain references;
- no unresolved/cross-domain sample in that check.

Limitation:
- current `build_context_pack()` is not task-aware; food photography, packaging, key visual and other restaurant subtasks may receive the same bounded exemplar pool.

Priority: medium, but do not fix until G3/G4 show retrieval is a real bottleneck.

---

## A06 — Actual approved reference image pixels are transmitted into the renderer for Personalized generation

Status: `UNPROVEN`

Current evidence:
- ContextPack contains sample/asset IDs and raw evidence;
- assets are resolvable in the private store;
- repository-side code does not yet prove renderer attachment identity/hash for those exemplars.

Risk if false:
- Personalized may be text-only while being mislabeled as multimodal personalization;
- previous A/B conclusions become weaker than assumed.

Priority: `CRITICAL / NEXT`.

Required proof:
- per-reference renderer attachment evidence matching canonical asset identity/SHA.

---

## A07 — Router selects the correct visual execution path for heterogeneous restaurant tasks

Status: `UNPROVEN`

Concern:
- food product, full key visual, packaging and store/social tasks have different intended routes/skills;
- current private generation traces have not yet been fully reconstructed.

Risk if false:
- packaging or food-photo tasks collapse into one generic restaurant-poster solution.

Priority: high after A06 trace reconstruction.

---

## A08 — Current restaurant Prompt Compiler preserves the highest-value visual constraints in the final renderer prompt

Status: `UNPROVEN / HIGH_RISK`

Observation:
- existing rules prohibit many defects seen in recent outputs: waxy/plastic food, default ink/brush shortcuts, template repetition and decorative smoke masking structure;
- recent outputs nevertheless exhibited these patterns.

Possible explanations:
1. rules were not actually read;
2. compiler dropped them;
3. host added generic cliche guidance;
4. renderer ignored them;
5. quality gate failed to reject output.

Priority: critical after A06/A07.

---

## A09 — Mandatory visual quality gates are actually executed before an output enters evaluation

Status: `UNPROVEN / HIGH_RISK`

Observation:
- repository documents say generation completion is not a pass;
- visibly weak/fake-food images still reached experimental comparison.

Required proof:
- execution receipt records gate `DEFINED / EXECUTED / RESULT`.

Priority: critical.

---

## A10 — Current renderer/model can produce restaurant visuals that meet the user's real production floor under a strong prompt

Status: `UNPROVEN`

Important:
- recent poor outputs do not isolate renderer quality because prompt/reference transmission is not yet proven.

Required experiment:
- G3 Expert Direct condition after renderer trace is observable.

Priority: critical, but only after G1 trace proof.

---

## A11 — Personalized context improves relative preference

Status: `WEAK_EVIDENCE`

Evidence:
- Phase 9 blind result: Personalized 6 vs Baseline 4.

Why weak:
- only 10 pairs;
- user later reported both sides were often visually poor;
- absolute quality was not measured;
- true multimodal reference binding was not proven.

Action:
- do not use this as scale authorization.

---

## A12 — Personalized generation reaches an acceptable absolute production-quality floor

Status: `FAILED`

Evidence:
- user reports that the generated restaurant images were broadly unusable and only relatively less bad choices were selected;
- recent outputs show repeated template/cliche patterns and implausible food material.

Consequence:
- PHASE 10 replication is paused;
- G4 absolute quality must pass before future scale/replication.

Priority: critical.

---

## A13 — More preference images will solve the current quality problem

Status: `UNPROVEN / CURRENTLY_DISALLOWED ASSUMPTION`

Reason:
- no evidence yet that data quantity is the bottleneck;
- reference pixels may not even be reaching the renderer correctly;
- prompt/compiler/quality-gate/renderer issues remain unresolved.

Action:
- do not expand the library until G4 passes.

---

## A14 — Embeddings/vector DB are required for the next quality improvement

Status: `NOT_NEEDED_YET`

Reason:
- upstream generation-chain failures are more likely and more consequential;
- task-aware metadata retrieval has not yet been tested as insufficient.

Action:
- defer.

---

## A15 — More aesthetic rules will solve the current quality problem

Status: `DISFAVORED HYPOTHESIS`

Reason:
- many relevant rules already exist;
- output still violated them;
- project charter explicitly warns against rule bloat for taste problems.

Preferred action:
- audit execution/transmission first.

---

# Current execution priority

```text
1. A06 — Reference pixels → Renderer
2. A07 — Correct routing
3. A08 — Prompt/compiler preservation
4. A09 — Quality gate execution
5. A10 — Renderer capability under Expert Direct
6. A12 — Absolute usable quality recovery
7. Only then revisit A11 personalization strength
```

Anything lower-priority must not displace this order without new evidence.