# V3-A Commercial Hardening Plan V1

Status: `ACTIVE_NEXT_SEQUENCE`

Repository: `vubaoha034-hash/shenmei`
Branch: `visual-program-distillation-v2-photography-design-20260814`
Executor policy: `CHATGPT_FIRST / CODEX_NOT_REQUIRED_BY_DEFAULT`

## Frozen current state

- Family Transfer: `PASS`
- Production Layer Pilot R2: `PASS`
- Functional typography: materially improved and no longer the dominant blocker
- Commercial Quality Gate: `NOT YET`
- Golden Exemplar: `NO`
- Route B: `SOURCE_MISMATCH_FOR_ROUTE_B`
- Scale Gate: `BLOCKED`

Current formal artifact:

`V3-A_PRODUCTION_LAYER_PILOT_R2.png`

SHA-256:
`964671205099d7f7e08d8fe8a5279bdc5cc6505f88e970da24466c54e82acb67`

Dimensions:
`1024x1536`

Editable production source:

- Figma file key: `XZPhanfxH1JWUPsOoxt0zp`
- Frame: `1:2`
- Live typography: YES
- Functional fonts: `Noto Serif SC + Inter`

The R2 manifest also records a deterministic clean raster base:

`V3-A_PRODUCTION_LAYER_PILOT_R2_CLEAN_BASE.png`

SHA-256:
`f0d67df33bf1d185c73c7770a3e3a9adb20e9a76fd956e3093483148c979f36a`

This clean base is the preferred art-edit substrate because it removes the five baked functional-text groups while preserving protected art pixels.

---

# Objective

Raise the selected V3-A direction from:

`successful visual-program transfer + competent production typography`

to:

`credible commercial restaurant campaign artifact with controlled realism, brand authorship, meaningful information semantics, and production discipline`.

Do not redesign the validated macro composition unless a later human gate explicitly determines the composition itself is the remaining blocker.

---

# Execution sequence

## R3A — Art Realism Hardening

Owner:

- target definition / constraints: ChatGPT
- selective visual editing: ImageGen
- technical identity checks: ChatGPT + tools
- aesthetic authority: human review
- Codex: NO by default

Primary targets:

1. reduce synthetic food gloss repetition;
2. increase believable material variation between food pieces;
3. reduce repeated garnish patterns;
4. reduce excessive particle / droplet / debris density;
5. preserve appetizing red-brown / sauce-red separation;
6. preserve the validated wok/process/dining narrative;
7. retain the same macro composition and identity rail.

Output must remain a controlled refinement, not a new poster concept.

Human R3A Gate:

- food looks materially more photographic;
- fewer obvious generated/composite cues;
- appetite is not degraded;
- art-direction energy remains;
- macro composition and display identity remain stable.

If R3A fails, revise the realism strategy before touching brand/copy structure.

## R3B — Brand Authorship + Copy Semantics

Enter only after R3A human PASS.

Owner:

- brand-language decision: ChatGPT + human standard
- deterministic typography/layout: Figma
- image generation: NO unless a tiny supporting visual asset is explicitly approved
- Codex: NO by default

Primary targets:

1. preserve the raster `现烧` display identity;
2. keep functional text live/editable;
3. remove or replace generic premium-editorial filler;
4. make the left rail feel authored for this family rather than like a reusable UI component;
5. reduce unnecessary English if it carries no campaign meaning;
6. establish a more proprietary relationship between display identity, Chinese support type, separators, and semantic markers;
7. keep information density useful rather than decorative.

Current generic strings requiring review:

- `WOK HEAT`
- `CHILI AROMA`
- `DINING ALIVE`

They must not survive merely because they fill space.

Human R3B Gate:

- left rail reads as brand language, not template language;
- supporting copy carries real semantic value;
- `现烧` remains first identity layer;
- typography remains production-grade and editable;
- no regression in art realism.

## R3C — Full Commercial Quality Gate

Enter only after R3A + R3B PASS.

Review actual final pixels at full view and detail view.

Critical dimensions:

1. food / material realism;
2. photographic coherence;
3. brand authorship / non-genericness;
4. display + functional typography relationship;
5. copy / information semantics;
6. hierarchy and micro-layout precision;
7. AI/composite artifact risk;
8. commercial restraint / density control;
9. production editability and traceability.

Suggested internal 0–5 review scale:

- `5`: mature top commercial delivery quality;
- `4`: credible professional commercial quality with only minor non-blocking issues;
- `3`: strong concept / portfolio quality but still visibly unfinished;
- `2`: material visual or production defects;
- `1`: major failure;
- `0`: invalid / unusable.

Commercial Quality PASS requires:

- every critical dimension >= 4;
- no unresolved visual blocker;
- no major AI/composite cue at normal viewing distance;
- human reviewer explicitly answers YES to real-world deployment readiness.

The numeric rubric is a control aid, not a substitute for human judgment.

## R3D — Golden Exemplar Candidate

Only after Commercial Quality PASS.

A Commercial PASS artifact may become a Golden candidate, but promotion is a separate decision.

Promotion must verify that the artifact is:

- representative of the intended system ceiling;
- reusable as a quality anchor without forcing template collapse;
- traceable to exact inputs / process / production source;
- not dependent on accidental one-off artifacts.

## Scale Gate

Remain blocked until:

1. Commercial Quality PASS;
2. Golden Exemplar decision completed;
3. no open critical regression blocker remains.

Scale must test repeatability, not compensate for quality gaps.

---

# Codex usage for this sequence

Current decision:

`CODEX_REQUIRED = NO`

Reason:

R3A is a selective visual-edit problem; R3B is a deterministic Figma production problem; R3C is a human/commercial review problem.

Codex becomes admissible only if a later step requires actual code execution such as:

- scripted layer extraction/compositing;
- batch image metrics or deterministic validators not available through existing tools;
- repository automation;
- multi-file implementation;
- test/build/CI work.

Do not spend Codex quota on visual judgment, prompt drafting, GitHub state writing, or simple manifest work.

---

# Reporting contract

Every R3 substage report must include:

## 已完成什么

## 未完成什么

And explicitly state:

- Codex used: YES / NO
- if YES: `CODEX_REQUIRED_REASON`
- image generation executed: YES / NO
- live typography preserved: YES / NO
- Commercial Quality Gate: PASS / NOT YET
- Golden Exemplar: YES / NO
- Scale Gate executed: YES / NO
