# V3 PRODUCTION REARCHITECTURE MASTER PLAN

Status: `ARCHITECTURE_FREEZE_CANDIDATE`
Branch: `v3-exemplar-first-production-rearchitecture-20260817`

## 0. Why this rearchitecture exists

The visual system accumulated strong evidence, provenance, blind-review and causal-analysis capability, but production quality repeatedly lagged behind direct high-quality image generation.

The central failure was not a lack of effort or analysis. It was a responsibility and runtime-design error:

- research/benchmark constraints leaked into production;
- taste problems were treated like correctness problems;
- too many intermediate abstractions sat between visible reference pixels and the renderer;
- runtime prompts became heavier while visual freedom decreased;
- renderer provenance was not always explicit;
- source assets lacked semantic identity and hero-suitability metadata;
- Codex was allowed to behave too much like the visual author instead of the production orchestrator;
- the strongest visual renderer did not always receive the smallest, highest-value visual package.

The repository's own `AESTHETIC_SKILL_DESIGN_CHARTER.md` already defines the correct governance principle:

> compact high-leverage prompt compiler, thin wrappers, correctness separated from taste, and delete rules when more rules make results stiffer.

V3 production must return to that principle.

---

# 1. Non-negotiable architecture split

The system SHALL have two independent operating planes.

## A. PRODUCTION PLANE

Purpose:

> create the best possible finished visual quickly.

Characteristics:

- exemplar-first;
- built-in OpenAI `image_gen` as the default raster creative/edit renderer;
- small active context;
- one complete artifact first;
- inspect actual pixels;
- at most one targeted aesthetic refinement by default;
- human taste review controls acceptance;
- deterministic post-production only where it is genuinely superior;
- no blind-evaluation ceremony during ordinary production;
- no causal-ablation constraints during ordinary production;
- no requirement to keep an ugly first valid output simply for experimental purity.

## B. EXPERIMENT PLANE

Purpose:

> learn whether a specific system change causes measurable improvement.

Characteristics:

- isolated branches / experiments;
- frozen inputs;
- one-variable ablations when appropriate;
- blind review when needed;
- no best-of-N when it would contaminate causal inference;
- mapping integrity, receipts and experiment validity gates;
- outputs do NOT become production standards merely because an experiment technically passes.

### Hard rule

`EXPERIMENT_PROTOCOL != PRODUCTION_WORKFLOW`

No experiment-only restriction may enter the production runtime unless it has a direct production benefit.

---

# 2. Production responsibility model

## 2.1 Strong visual model = ARTIST

The visual renderer owns:

- zero-to-one visual composition;
- integrated photography / food rendering / atmosphere;
- display lettering when it is part of the visual artwork;
- image-text integration at concept/art-direction level;
- stylistic interpretation;
- selective image editing when pixel-level visual correction is required.

Default raster path:

`OpenAI official imagegen Skill -> built-in image_gen`

The runtime MUST record this explicitly.

## 2.2 ChatGPT visual director = ART DIRECTOR + HUMAN-LOOP CONTROLLER

The supervising ChatGPT context owns:

- reading real pixels;
- interpreting the user's live visual feedback;
- choosing the active visual family / mother reference / golden exemplar;
- deciding what is essential vs optional;
- producing the short art-direction payload;
- deciding `ACCEPT / TARGETED_REFINE / REJECT / CHANGE_SOURCE / CHANGE_FAMILY`;
- comparing final pixels against the user's actual quality bar;
- deciding whether a durable lesson is worthy of promotion.

This layer must NOT delegate taste judgment to a validator.

## 2.3 Codex = ORCHESTRATOR + ENGINEER + RECORDER

Codex owns:

- resolving exact files and identities;
- retrieving authoritative metadata;
- building the small runtime package;
- calling the required renderer through the official imagegen Skill;
- preserving user-required facts and correctness constraints;
- saving outputs and manifests;
- recording renderer provenance;
- maintaining tests, schemas, branches and storage;
- deterministic typesetting/production cleanup when explicitly routed there;
- reporting what changed and what did not.

Codex MUST NOT:

- self-award aesthetic PASS;
- replace the visual renderer with Figma/vector work for zero-to-one visual design;
- turn human taste complaints into growing validator rule sets by default;
- infer missing food/product identity from ambiguous pixels when authoritative semantics are absent.

## 2.4 User = FINAL TASTE AUTHORITY

The user owns the final preference signal.

Raw user statements such as:

- `喜欢`
- `非常丑`
- `这个菜看起来炒糊了`
- `看不懂这是什么`
- `这个可以`

are first-class raw evidence.

They must be preserved verbatim with artifact identity and timestamp/context lineage.

The system may interpret them, but may not overwrite them.

---

# 3. Production runtime: minimal active package

For one ordinary generation, load only what changes the pixels.

Default active package:

1. **Task facts**
   - exact deliverable;
   - exact visible copy;
   - required aspect/format where supported;
   - brand/product facts.

2. **One Mother Reference**
   - canonical pixels;
   - exact identity/hash.

3. **Zero or one Golden Exemplar by default**
   - only if a user-approved family exemplar exists;
   - use a second only when it contributes non-duplicate information.

4. **Current real content source(s)**
   - usually 1 primary content asset;
   - secondary only if semantically necessary.

5. **Compact Family Capsule**
   - `VISUAL_PHILOSOPHY`: 3–6 sentences;
   - `DISCRIMINATIVE_SIGNATURE`: 4–7 mechanisms;
   - `GENERIC_SHORTCUT_BLOCKERS`: <=3;
   - `FREEDOMS`: concise.

6. **Correctness constraints**
   - exact spelling;
   - identity/product facts;
   - prohibited factual substitutions.

### Attachment budget

Default target: `2–4 visual attachments`.

The runtime builder must deduplicate roles. If Mother Reference already contains the process cue, do not automatically attach a redundant process crop.

More stored references do NOT mean more active attachments.

---

# 4. Style Capsule V3

A validated family capsule contains:

```text
family_id
status
VISUAL_PHILOSOPHY
MOTHER_REFERENCE
GOLDEN_EXEMPLARS[]
DISCRIMINATIVE_SIGNATURE[]
CONTENT_COMPATIBILITY
DISPLAY_TYPOGRAPHY_ROLE
FUNCTIONAL_TYPOGRAPHY_ROLE
GENERIC_SHORTCUT_BLOCKERS[]
FREEDOMS[]
PRODUCTION_FINISH_POLICY
human_evidence_links[]
```

## Rules

- no giant runtime schema dump;
- no linear growth as the library grows;
- conflicting liked styles remain separate families;
- a whole-image `LIKE` does not imply every component is globally preferred;
- family promotion requires finished visual evidence, not prose completeness;
- a family can be useful before it is `GOLDEN`.

### Family states

- `PROVISIONAL`
- `STRUCTURALLY_VALIDATED`
- `PRODUCTION_VALIDATED`
- `GOLDEN`
- `DEPRECATED`

Only explicit high-quality human acceptance can promote to `GOLDEN`.

---

# 5. Asset Semantic Contract

Visual source files cannot be treated as anonymous pixels when product identity matters.

For restaurant hero assets, the registry must support:

```text
asset_id
canonical_dish_name
primary_ingredient_or_protein
cooking_method
visible_identity_cues[]
forbidden_substitutions[]
hero_suitability
source_truth_mode
user_label_source
```

## hero_suitability

- `PASS`: strong hero source;
- `CONDITIONAL`: usable as grounding, but renderer may improve plating/clarity while preserving identity;
- `FAIL`: not suitable as hero visual; use another source or semantic reconstruction.

### Hard rule

If exact product semantics matter and authoritative identity is missing:

> ASK / RESOLVE SEMANTICS BEFORE HERO PRODUCTION.

Do not spend repeated image-edit calls trying to infer a missing product identity.

---

# 6. Food production hierarchy

For restaurant imagery, production priority is:

1. **PRODUCT LEGIBILITY** — what is it?
2. **APPETITE** — do I want to eat it?
3. **PRODUCT TRUTH** — is it still the actual dish/product?
4. **COMMERCIAL HIERARCHY** — what am I supposed to notice first?
5. **FAMILY IDENTITY** — does it belong to the intended visual family?
6. **TYPOGRAPHY / MICRO-POLISH**

Any lower priority must yield when it damages a higher priority.

Examples:

- family style may not make the dish unrecognizable;
- `wok hei` may not turn food into a black burnt mass;
- extra bowls may not be kept merely to make the layout look fuller;
- typography may not overpower the product.

---

# 7. Production routing

## 7.1 FAST FAMILY MODE

Use when a validated family exists.

Flow:

```text
resolve task facts
-> resolve product semantics
-> choose Mother + approved exemplar
-> build compact runtime package
-> built-in image_gen
-> inspect real pixels
-> ACCEPT or one TARGETED_REFINE
-> optional deterministic finish
-> human final decision
-> archive lineage
```

No deep distillation rerun by default.

## 7.2 NEW STYLE DISCOVERY MODE

Use when the user provides a genuinely new liked visual direction.

Flow:

```text
inspect reference pixels
-> deep distillation once
-> provisional compact capsule
-> generate complete artifact(s)
-> user judges actual finished outputs
-> revise capsule from visual feedback
-> repeat only as needed
-> promote after repeated success
```

Learning occurs through finished artifacts, not schema completion.

## 7.3 DIRECT CREATIVE MODE

Use when the user asks simply for a good result and does not require family continuity.

Flow:

```text
short brief + real content
-> built-in image_gen directly
-> human pixel review
-> targeted refinement if useful
```

The system must not force an existing family onto the task merely because a family is available.

---

# 8. Iteration policy

Production default:

- Call 1: complete artifact;
- inspect actual pixels;
- Call 2: allowed only as a targeted refinement of the most important remaining visual defect;
- additional aesthetic iterations require explicit human decision that the direction remains worth refining.

This is deliberately different from benchmark purity rules.

### Single-change refinement principle

After a selected artifact exists:

> prefer `change only X; keep Y unchanged` over rewriting the whole prompt.

If the base direction is wrong, reject the direction instead of accumulating local patches.

---

# 9. Visual review and acceptance

Codex technical checks:

- file integrity;
- dimensions/format;
- obvious correctness failures;
- exact text/identity facts where deterministically verifiable;
- renderer provenance;
- attachment identities;
- output persistence.

ChatGPT/human visual review:

- thumbnail impact;
- product legibility;
- appetite/material credibility;
- visual authorship;
- hierarchy;
- typography as visual design;
- family fidelity where relevant;
- generic-template collapse;
- absolute final quality.

### Acceptance vocabulary

- `TECHNICALLY_VALID`
- `DIRECTION_PROMISING`
- `TARGETED_REFINE`
- `REJECT_VISUAL`
- `PRODUCTION_USABLE`
- `GOLDEN_CANDIDATE`
- `GOLDEN_EXEMPLAR`

Technical validity must never automatically imply `PRODUCTION_USABLE`.

---

# 10. Golden Exemplar promotion

A candidate may become `GOLDEN_EXEMPLAR` only when:

1. user explicitly approves the actual artifact at a high bar;
2. artifact identity/hash is frozen;
3. family identity is known;
4. product/scene semantics are known;
5. no major unresolved correctness issue remains;
6. the artifact is useful as a positive future target rather than merely a historical experiment result.

Promotion authority remains the system's durable promotion mechanism (`skill-refiner` or equivalent canonical authority already defined by repository governance).

Golden exemplars are scarce. Do not promote merely because one artifact is the best seen so far.

---

# 11. Renderer provenance hard requirement

Every formal production manifest must record:

```text
imagegen_skill_used
renderer_mode
built_in_image_gen_used
cli_fallback_used
imagegen_call_count
edit_or_generate
input_visual_ids[]
final_output_sha256
```

For normal raster visual creation/editing:

- official OpenAI imagegen Skill;
- built-in `image_gen` is the default;
- CLI fallback only when explicitly requested by the user;
- `strongest renderer` is not a sufficient provenance string.

---

# 12. What becomes legacy / research-only

The following are NOT deleted, because they contain evidence and lessons.

But they are removed from ordinary production runtime:

- VPD V2 full analysis schema;
- blind-review machinery;
- ablation protocols;
- one-shot aesthetic purity constraints;
- role-anchor experiment machinery;
- contrastive-signature experiment machinery;
- large hard-avoid warehouses;
- Figma-first creative reconstruction;
- large multi-stage prompt reconstruction chains.

They remain:

> `EVIDENCE / RESEARCH / DIAGNOSTICS`

not:

> `DEFAULT PRODUCTION PATH`.

---

# 13. System simplification rule

Before adding any new production rule, ask:

1. Does this fix a correctness error or a taste complaint?
2. Does it directly change pixels in a useful way?
3. Could the same improvement come from a better reference/exemplar or one clearer art-direction sentence?
4. Does it increase runtime context size?
5. Does it reduce visual freedom?
6. Can it be stored as evidence rather than loaded every run?

If a new taste rule is not clearly high leverage:

> do not add it to runtime.

---

# 14. Success definition for this rearchitecture

The rearchitecture is not complete when documents exist.

It is complete only after the new production path proves all of the following:

1. renderer provenance is explicit and uses built-in image_gen by default;
2. runtime visual package remains small;
3. known family can produce a coherent artifact without deep re-analysis;
4. product semantics are resolved before hero generation;
5. a complete artifact can be generated quickly without research-protocol ceremony;
6. one targeted refinement can improve the selected artifact without broad drift;
7. human review, not Codex self-scoring, determines visual acceptance;
8. production output quality is at least competitive with direct ChatGPT image generation;
9. research plane remains available without contaminating production.

---

# 15. Current migration decision

Current V2/V3 experimental artifacts remain evidence.

Immediate production migration should:

- create the Production/Experiment split;
- implement renderer provenance;
- implement semantic asset contract;
- implement compact Style Capsule V3;
- implement Fast Family / New Style / Direct Creative routing;
- implement small runtime package builder;
- implement human-review handoff;
- explicitly retire experiment-only rules from default production routing;
- retain all raw user evidence and provenance.

No library-scale expansion is allowed until the new production path is visually validated.

---

# 16. Core operating formula

```text
RAW HUMAN EVIDENCE
+ AUTHORITATIVE PRODUCT SEMANTICS
+ MOTHER REFERENCE
+ SCARCE GOLDEN EXEMPLARS
+ COMPACT FAMILY CAPSULE
        ↓
OFFICIAL BUILT-IN IMAGE_GEN
        ↓
HUMAN PIXEL REVIEW
        ↓
ONE TARGETED REFINEMENT WHEN USEFUL
        ↓
DETERMINISTIC FINISH ONLY WHERE SUPERIOR
        ↓
FINAL HUMAN ACCEPT / REJECT
        ↓
DURABLE LEARNING PROMOTION
```

The system is the art director, memory and production discipline.
The image model is the artist.
Codex is the orchestrator and engineer.
The user remains the final taste authority.
