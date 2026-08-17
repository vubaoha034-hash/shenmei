# V3 PRODUCTION REARCHITECTURE — CODEX MASTER TASK

Status: `READY_FOR_IMPLEMENTATION`

Repository: `vubaoha034-hash/shenmei`
Required branch: `v3-exemplar-first-production-rearchitecture-20260817`

Anchor commit containing the architecture plan:

`a36851278f066c74dbad9630f773426113ef6c16`

## Mission

Implement the production rearchitecture defined in:

`V3_PRODUCTION_REARCHITECTURE_MASTER_PLAN.md`

The purpose is NOT to generate another poster.

The purpose is to convert the repository into a durable system where:

- production and experiment workflows are separated;
- official built-in `image_gen` is the explicit normal raster renderer;
- Codex orchestrates instead of acting as visual author;
- active runtime context is small and exemplar-first;
- source/product semantics are resolved before generation;
- human pixel review determines taste acceptance;
- research evidence remains available without contaminating ordinary production;
- runtime rules do not grow linearly with the reference library.

Do not summarize the architecture. Implement it.

---

# 0. Mandatory pre-read

Read in this order:

1. `START_HERE.md`
2. `AESTHETIC_SKILL_DESIGN_CHARTER.md`
3. `VPD_V3_TOP_SKILL_REFERENCE_AUDIT.md`
4. `V3_PRODUCTION_REARCHITECTURE_MASTER_PLAN.md`
5. existing relevant visual Skills / production runners only as needed to wire routing correctly
6. existing `skill-refiner` durable-promotion authority and its contract

Do not load the entire reference library.
Do not inspect unrelated business/operations systems.

---

# PHASE 1 — Inventory and legacy classification

Create:

`V3_PRODUCTION_LEGACY_INVENTORY.md`

Inventory existing components relevant to image production and classify each as:

- `PRODUCTION_KEEP`
- `PRODUCTION_ADAPT`
- `RESEARCH_ONLY`
- `DEPRECATED_PRODUCTION_PATH`
- `EVIDENCE_ONLY`

At minimum classify:

- VPD V2 analysis/compiler artifacts;
- blind review / ablation machinery;
- role-anchor and contrastive-signature experiments;
- Figma-first creative path;
- restaurant poster production Skill;
- image/material director Skills;
- personal aesthetic critic / brand aesthetic gates;
- evidence ledger / provenance / raw feedback systems;
- asset vault / private semantic metadata paths;
- skill-refiner.

Hard rule:

Do not delete evidence.
Do not rewrite experiment history.
Do not promote research artifacts into production simply because they exist.

---

# PHASE 2 — Explicit Production / Experiment routing

Implement repository-level routing so ordinary image creation chooses one of:

- `PRODUCTION_FAST_FAMILY`
- `PRODUCTION_NEW_STYLE_DISCOVERY`
- `PRODUCTION_DIRECT_CREATIVE`
- `EXPERIMENT_VISUAL_CAUSAL`

Create a machine-readable routing contract, for example:

`config/visual-production-routing.v3.json`

and a human-readable contract:

`V3_VISUAL_PRODUCTION_ROUTING.md`

Update `START_HERE.md` minimally so future executors can discover the V3 production route.

Do NOT replace existing canonical routes until V3 is validated; label V3 as the new production candidate route and preserve existing stable paths.

Routing requirements:

### PRODUCTION_FAST_FAMILY
Use when a validated family capsule exists.
No deep distillation rerun by default.

### PRODUCTION_NEW_STYLE_DISCOVERY
Use when a new liked visual is not represented by a validated family.
Deep analysis once, then immediately test through finished artifacts.

### PRODUCTION_DIRECT_CREATIVE
Use when the user wants the best result and does not require family continuity.
Do not force an existing family.

### EXPERIMENT_VISUAL_CAUSAL
Use only for ablations/blind tests/causal research.
Experiment restrictions must never silently leak into production.

---

# PHASE 3 — Renderer provenance contract

Create:

`schemas/visual-production-manifest.v3.schema.json`

Required fields include:

```text
mode
imagegen_skill_used
renderer_mode
built_in_image_gen_used
cli_fallback_used
imagegen_call_count
edit_or_generate
input_visual_ids
input_visual_hashes
mother_reference_id
golden_exemplar_ids
content_asset_ids
semantic_contract_ids
attachment_count
runtime_control_count
output_filename
output_sha256
output_dimensions
technical_retries
aesthetic_refinement_calls
human_review_status
final_status
```

Normal raster production contract:

- official OpenAI imagegen Skill;
- built-in `image_gen` default;
- CLI fallback only if user explicitly requests it;
- vague values such as `strongest renderer` are invalid provenance.

Implement a validator that fails if formal raster production lacks explicit renderer provenance.

Do not call image generation in this phase.

---

# PHASE 4 — Asset Semantic Identity Registry

Implement a semantic sidecar/registry for production-critical visual assets.

Create schema:

`schemas/visual-asset-semantic.v1.schema.json`

Restaurant fields must support:

```text
asset_id
asset_sha256
canonical_dish_name
aliases
primary_ingredient_or_protein
cooking_method
required_visible_identity_cues
forbidden_substitutions
hero_suitability
source_truth_mode
user_label_source
confidence
evidence_links
```

Hero suitability:

- `PASS`
- `CONDITIONAL`
- `FAIL`

Implement a semantic gate script/check:

- if product identity matters and authoritative semantics are absent -> `NEEDS_HUMAN_INPUT`;
- never infer authoritative dish identity from ambiguous pixels alone;
- source `FAIL` does not mean delete the asset; it remains evidence/grounding where appropriate.

## Seed the known lemon tenderloin evidence

For asset:

`ast_63aa377b-5287-400d-b0a3-a6282313b38c`

preserve the user's authoritative semantic input:

- canonical dish name: `柠檬叶怪味里脊`
- alias: `柠檬怪味里脊`
- primary ingredient/protein: `猪里脊肉`
- process:
  1. pork tenderloin strips are fried to set;
  2. oil temperature is raised and strips are re-fried about 30 seconds for a crisp shell;
  3. garlic and chili are aromatized, dark guaiwei sauce is simmered until thick/sticky;
  4. fried tenderloin strips are rapidly tossed over high heat until evenly coated.
- required identity cues should include:
  - pork tenderloin strip form;
  - fried/crisp outer shell evidence;
  - individually separable strips;
  - deep glossy guaiwei sauce coating;
  - not a formless black mass.
- forbidden substitutions should include at least:
  - beef;
  - chicken;
  - ribs / bone-in meat;
  - generic irregular chunks that erase tenderloin-strip identity.

The user later explicitly rejected this specific source/artifact direction as visually unappetizing for hero use and asked to change the dish.

Therefore set the current source asset's `hero_suitability` to `FAIL` for hero-KV use, while retaining it as truthful historical evidence.

Do not reinterpret the user's rejection as rejection of the real dish itself; it is rejection of this asset/direction as a hero visual.

---

# PHASE 5 — Style Capsule V3

Create schema:

`schemas/style-capsule.v3.schema.json`

Required concepts:

- family_id
- state
- visual_philosophy
- mother_reference
- golden_exemplars
- discriminative_signature
- content_compatibility
- display_typography_role
- functional_typography_role
- generic_shortcut_blockers
- freedoms
- production_finish_policy
- human_evidence_links

Enforce bounds:

- visual philosophy remains compact;
- discriminative signature default max 7;
- generic shortcut blockers max 3;
- golden exemplars scarce;
- no requirement that every stored reference becomes active runtime context.

Create state rules:

- `PROVISIONAL`
- `STRUCTURALLY_VALIDATED`
- `PRODUCTION_VALIDATED`
- `GOLDEN`
- `DEPRECATED`

Promotion to `GOLDEN` requires explicit human approval evidence and immutable artifact identity/hash.

Do not automatically convert V3-A experimental artifacts into Golden Exemplars.

---

# PHASE 6 — Runtime Package Builder

Implement deterministic package-building logic, preferably as a small script/library rather than a large new rule system.

Suggested output:

`scripts/build_visual_runtime_package_v3.py`

The package builder should accept:

- route/mode;
- task facts;
- exact copy;
- product semantic contract;
- optional family capsule;
- mother reference;
- optional golden exemplar;
- primary content asset.

It should output a compact manifest/prompt input package.

Default limits:

- active visual attachments target: 2–4;
- one mother reference;
- zero or one golden exemplar by default;
- one primary content asset by default;
- second content/exemplar only if non-duplicate and necessary;
- runtime discriminative controls 4–7 when a family is used;
- generic shortcut blockers <=3.

Implement role deduplication:

If two images provide materially duplicate role information, do not attach both by default.

The builder must NOT load the full reference library.

The builder must NOT dump the full VPD schema into the image prompt.

---

# PHASE 7 — New production Skill, without contaminating stable Skills

Because this is a major execution-model change, create a new experimental production Skill rather than rewriting a currently stable canonical Skill.

Create:

`skills/visual-production-director-v3/SKILL.md`

Its role:

- route production mode;
- resolve semantics;
- select small exemplar package;
- instruct Codex to use official imagegen Skill / built-in `image_gen`;
- hand off actual pixels to human review;
- permit one targeted refinement in production;
- route deterministic finishing only after visual direction is accepted.

Keep it thin.
Do NOT embed the VPD V2 analysis schema.
Do NOT embed blind-review protocols.
Do NOT embed dozens of aesthetic failure codes.

Create a thin restaurant adapter only if necessary:

`skills/restaurant-visual-production-v3/SKILL.md`

The adapter may add restaurant-specific semantic/food hierarchy but must not fork the base visual production logic.

---

# PHASE 8 — Human/Codex responsibility enforcement

Create:

`V3_HUMAN_CODEX_RESPONSIBILITY_MATRIX.md`

and encode these invariants in relevant docs/tests:

## Codex may decide

- exact file identities;
- metadata completeness;
- renderer availability;
- manifest validity;
- semantic gate status;
- file integrity;
- whether a deterministic production step completed technically.

## Codex may NOT decide as final truth

- aesthetically beautiful;
- premium;
- top-tier;
- Golden Exemplar;
- final user taste fit.

## ChatGPT/human review decides

- visual authorship;
- appetite;
- product legibility in actual pixels;
- generic-template collapse;
- hierarchy quality;
- typography quality as design;
- `ACCEPT / TARGETED_REFINE / REJECT`.

## User final signal

Explicit user artifact feedback overrides inferred aesthetic preference.
Preserve raw wording.

---

# PHASE 9 — Production iteration policy

Implement production policy:

- initial complete artifact;
- human pixel inspection;
- one targeted aesthetic refinement allowed by default;
- additional refinements require explicit human continuation;
- no hidden parallel candidates unless exploration is explicitly requested;
- production may reject the first artifact and try again if the direction is wrong; it is not bound by causal-experiment purity.

At the same time, preserve a separate experiment policy that remains strict for causal tests.

Create tests proving production and experiment policies cannot be confused by routing.

---

# PHASE 10 — Legacy runtime decoupling

Do not delete old VPD/research material.

But remove it from default V3 production loading.

Create a clear mapping showing:

```text
VPD V2 schemas -> research/evidence
blind mapping -> experiment only
ablation tasks -> experiment only
role anchors -> optional research evidence, not default production attachments
contrastive selector -> research result, not default runtime requirement
Figma-first art creation -> only explicit editable-production route
raw user evidence -> retained and authoritative
provenance -> retained
asset vault -> retained
skill-refiner -> retained promotion authority
```

The V3 production Skill must not import experiment protocols by default.

---

# PHASE 11 — Automated checks

Add tests/validators for at least:

1. Production raster manifest cannot omit explicit built-in imagegen provenance.
2. CLI fallback cannot be silently selected.
3. Runtime package does not exceed configured visual attachment budget without an explicit exception.
4. Style Capsule blockers <=3.
5. Style Capsule discriminative signature within configured bound.
6. Hero semantic gate blocks missing product identity when identity is required.
7. `hero_suitability=FAIL` blocks that asset from hero-source role by default.
8. Production mode allows targeted refinement; experiment mode can still enforce one-shot purity.
9. Technical PASS cannot automatically assign aesthetic/Golden status.
10. Full VPD analysis schema is not imported into normal Fast Family runtime.

Run the repository's existing relevant doctor/tests plus new tests.

---

# PHASE 12 — Documentation convergence

Update discovery docs minimally so future chats/Codex contexts know:

- where production V3 starts;
- production vs experiment split;
- when to use Fast Family / New Style / Direct Creative;
- built-in imagegen default;
- semantic identity requirement;
- human review requirement;
- Scale Gate remains blocked until visual validation.

Do not rewrite unrelated docs.

---

# PHASE 13 — No-image dry run

Before any real image generation, execute at least three dry-run package builds:

1. `FAST_FAMILY` with a mock/fixture validated family capsule;
2. `NEW_STYLE_DISCOVERY` with one new-reference fixture;
3. `DIRECT_CREATIVE` without a family.

Dry runs must prove:

- small active context;
- correct renderer provenance contract;
- no research-protocol leakage;
- semantic gate works;
- manifests validate.

Do NOT call image generation during these dry runs.

---

# PHASE 14 — Stop before visual pilot

After implementation and dry-run PASS, STOP.

Do not generate a new visual automatically.

The next visual pilot must be chosen with the supervising ChatGPT/user so the test uses a product/source with authoritative semantics and suitable hero material.

Final status should be:

`V3_PRODUCTION_REARCHITECTURE_READY_FOR_VISUAL_PILOT`

not `PRODUCTION_VALIDATED`.

---

# Required final report

Return exactly:

# V3 PRODUCTION REARCHITECTURE READY FOR VISUAL PILOT

Branch:
HEAD:
Production/Experiment split:
Renderer provenance contract:
Semantic asset registry:
Style Capsule V3:
Runtime package builder:
New production Skill:
Restaurant adapter:
Human/Codex responsibility matrix:
Legacy runtime decoupled:
New tests:
Existing relevant tests:
Dry runs:
Image generation executed: NO
Scale Gate executed: NO
Git working tree:

## 已完成什么

## 未完成什么

## 下一步人工选择什么

Then STOP.
