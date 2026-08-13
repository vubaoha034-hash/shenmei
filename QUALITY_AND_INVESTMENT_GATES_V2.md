# LIU VISUAL SYSTEM — QUALITY & INVESTMENT GATES V2

Status: `MANDATORY_FOR_NEW_MAINLINE`
Date: `2026-08-13`

These gates exist to prevent the project from spending large effort on infrastructure, statistics or automation while the core visual output remains unusable.

---

## Gate Q0 — Absolute Quality Floor

Every generated output used as evidence must be independently labeled by the user:

- `USABLE`
- `UNUSABLE`

Definition of `USABLE`:

> The core visual concept is good enough that the image could plausibly enter a real project without redesigning the concept from scratch. Minor production cleanup is allowed; fundamental composition, product realism or visual language replacement is not.

Pairwise preference is recorded separately.

A relative winner can still be `UNUSABLE`.

Hard rule:
- pairwise win alone never authorizes scale.

---

## Gate Q1 — Reference Binding Proof

Before any claim that Personal Context affected a render, classify the run:

- `MULTIMODAL_BOUND`
- `PARTIAL_MULTIMODAL_BOUND`
- `TEXT_ONLY_PERSONALIZATION`
- `UNPROVEN_BINDING`

Only `MULTIMODAL_BOUND` may be used as evidence for multimodal personalization quality.

Required evidence:
- selected exemplar ID;
- canonical asset ID/SHA;
- resolved file identity;
- renderer attachment identity;
- evidence that the renderer invocation included that attachment.

---

## Gate Q2 — Generation Trace Completeness

The following must be known for any quality experiment:

- task brief;
- route;
- Skill/version or blob SHA;
- compiler output;
- final renderer prompt;
- reference attachments;
- renderer/model/version;
- aspect ratio/parameters;
- output asset/hash;
- quality gate execution result.

If a critical step is UNKNOWN, the chain is not considered proven.

---

## Gate Q3 — Hard Gate Execution Proof

For each mandatory correctness/realism gate record:

```text
DEFINED
EXECUTED
RESULT
```

Examples:
- product anatomy/structure;
- plastic/waxy texture rejection;
- physical contact/shadow;
- fake text rejection;
- current-task explicit requirement compliance.

A rule merely existing in a Markdown file does not count as executed.

---

## Gate Q4 — Early Value Kill Gate

Trigger `VALUE_FLOOR_FAILURE` when a small diagnostic batch shows systematic unusable quality.

When triggered, freeze:
- evidence expansion;
- blind replication;
- embeddings/vector DB;
- new domains;
- automation;
- new aesthetic rule accumulation.

Resume only after the responsible upstream bottleneck is isolated and repaired.

---

## Gate Q5 — Capability Proof Before Architecture Expansion

Before authorizing any new infrastructure layer, answer:

1. Which core user-visible capability has already been proven?
2. What critical uncertainty will this infrastructure reduce?
3. Can the same uncertainty be tested more cheaply with a vertical slice?
4. If the core hypothesis fails tomorrow, how much of this work remains reusable?

If answers are weak, defer the infrastructure.

---

## Gate Q6 — Small-Batch Investment Rule

Before G4 passes:
- no bulk image ingestion;
- no large blind benchmark;
- no new renderer abstraction framework;
- no vector DB;
- no multi-agent architecture;
- no automated Skill evolution from taste feedback.

The next batch must always be the smallest batch that can falsify the current hypothesis.

---

## Gate Q7 — Anti-Sunk-Cost Rule

Previous effort is not evidence that the next step should proceed.

If a critical assumption becomes `FAILED`:

```text
STOP
→ isolate bottleneck
→ repair/replace/retire
→ rerun smallest proof
```

Do not continue merely because the project is already at a high phase number.

---

## Gate Q8 — Rule-Bloat Stop Rule

When visual failures occur, diagnosis order is:

1. Was the correct route used?
2. Was the intended Skill actually read?
3. Did the compiler produce a concrete imageable prompt?
4. Did actual reference pixels reach the renderer?
5. Did host orchestration add generic cliche terms?
6. Did the renderer comply?
7. Did the quality gate execute?

Only after these are proven may a new aesthetic rule be proposed.

Do not default to adding more prohibitions such as more color/style bans.

---

## Gate Q9 — Relative Personalization Success

After G4 passes, a personalization experiment must report two independent metrics:

### Relative
- Baseline vs Personalized: A/B/tie.

### Absolute
- Baseline: USABLE/UNUSABLE.
- Personalized: USABLE/UNUSABLE.

Success cannot be claimed from relative wins if absolute usable quality remains poor.

---

## Gate Q10 — Replication Eligibility

Large replication is allowed only when:
- generation trace is complete;
- Personalized reference binding is `MULTIMODAL_BOUND`;
- G4 absolute quality floor has passed;
- G5 shows a positive personalization signal;
- blind presentation path is proven safe.

Otherwise replication is premature.

---

# Stage exit report format

Every stage must report exactly these questions:

## 已完成什么
What was actually demonstrated?

## 未完成什么
What remains unproven or blocked?

## 核心假设状态
Which assumptions changed status?

## Absolute Quality
Were outputs independently usable?

## 下一阶段为什么值得做
Which high-risk uncertainty will it reduce?

## 如果下一阶段失败，当前成果能保留什么
Explicit reuse / sunk-cost analysis.

A stage may not be marked PASS merely because code, documents or tests were produced.