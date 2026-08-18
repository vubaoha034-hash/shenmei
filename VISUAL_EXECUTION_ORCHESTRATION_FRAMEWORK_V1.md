# Visual Execution Orchestration Framework V1

Status: `ACTIVE`

Repository: `vubaoha034-hash/shenmei`
Primary operating principle: `CHATGPT_FIRST / SPECIALIST_TOOL_ONLY_WHEN_REQUIRED`

## Purpose

Prevent three recurring failures:

1. consuming Codex quota on work that does not require a software-engineering agent;
2. confusing professional difficulty with executor requirements;
3. losing project state when work moves between reasoning, image generation, production tooling, GitHub, Codex, and human review.

This framework governs executor selection and phase handoff. It does not replace project-specific visual-program contracts or quality gates.

---

# 1. Four-layer operating model

## Layer A — Control / reasoning

Default owner: `ChatGPT`

Responsibilities:

- recover and lock current project state;
- inspect assumptions and dependencies;
- research when necessary;
- design experiments and gates;
- define acceptance criteria;
- perform visual comparison and human-facing review;
- decide whether Codex is actually required;
- coordinate ImageGen / Figma / Adobe / GitHub;
- keep `已完成什么 / 未完成什么` explicit;
- prevent rollback, duplication, and premature promotion.

Professional complexity alone is never a reason to invoke Codex.

## Layer B — Creative / visual execution

Default owner by task:

- generative image creation or selective visual editing: `ImageGen`;
- deterministic layout, live typography, spacing, production source: `Figma` or equivalent production tool;
- local image finishing / bounded raster cleanup when appropriate: `Adobe` or equivalent image editor.

Codex must not be used as a substitute for a visual renderer or human aesthetic judgment.

## Layer C — Software-engineering execution

Owner: `Codex`, but only when one or more hard triggers apply.

Valid Codex triggers:

1. commands/scripts must actually run in an engineering environment;
2. tests/build/lint/doctor/validator must execute against real files;
3. multi-file code changes or non-trivial refactors are required;
4. a reproducible bug must be traced, fixed, and verified in code;
5. migration, dependency, CI, packaging, or repository automation work is required;
6. deterministic asset processing requires code that must be executed and validated;
7. a tested PR-grade implementation is the required deliverable.

If none of these triggers exists, Codex is not the default executor.

## Layer D — Validation / authority

Technical validation:

- exact file identity;
- SHA / dimensions / MIME where applicable;
- deterministic export checks;
- tests / doctor / validator when required;
- changed-region or regression verification.

Aesthetic authority:

- human visual review, supported by ChatGPT pixel comparison and structured critique;
- Codex may report technical facts but must not self-promote a visual artifact to Commercial Pass / Golden Exemplar.

---

# 2. Executor routing matrix

| Task type | Default executor | Codex? |
|---|---|---|
| Professional analysis / strategy / architecture | ChatGPT | NO |
| Research / comparison / diagnosis | ChatGPT + relevant sources | NO |
| Human visual review / commercial critique | ChatGPT + human | NO |
| Experiment/gate design | ChatGPT | NO |
| GitHub branch/status/file inspection | ChatGPT + GitHub connector | NO |
| Simple Markdown / JSON / state-record changes | ChatGPT + GitHub connector | NO |
| Single bounded image generation/edit | ImageGen | NO |
| Typography / spacing / editable layout | Figma | NO |
| Raster cleanup / finishing | Adobe or image editor | NO unless code required |
| Script execution / test / build / validator | Codex | YES |
| Multi-file implementation / refactor | Codex | YES |
| CI / packaging / migration | Codex | YES |
| Reproducible engineering bug fix | Codex | YES |
| Mixed creative + engineering workflow | ChatGPT orchestrates specialists | ONLY scoped engineering portion |

---

# 3. Codex admission gate

Before invoking Codex, the controlling context must be able to state all of:

- `CODEX_REQUIRED_REASON`
- exact engineering deliverable;
- exact repository / branch / anchor;
- allowed read/write scope;
- expected verification command(s) or technical evidence;
- explicit stop condition.

If `CODEX_REQUIRED_REASON` cannot be stated concretely, do not invoke Codex.

Invalid reasons:

- "the task is professional";
- "the task is important";
- "the project is complex";
- "Codex may do it better";
- "we want a second opinion";
- "write a document / analyze an image / judge aesthetics".

---

# 4. Codex quota-control rules

When Codex is admitted:

1. give it one bounded engineering task, not the whole project;
2. provide the minimum exact context required to execute safely;
3. do not ask it to rediscover project history already known by the controller;
4. do not ask it to perform aesthetic self-review;
5. do not duplicate research already completed by ChatGPT;
6. do not launch parallel Codex contexts unless independent replicates are explicitly required by the experiment;
7. do not browse large unrelated repository areas when exact paths/anchors are known;
8. stop after the requested implementation + verification + handoff;
9. return control to ChatGPT for interpretation, visual review, next-step selection, and project-state update.

---

# 5. Standard project execution sequence

## Step 0 — Recover state

Lock:

- repository;
- branch;
- current artifact / SHA if relevant;
- latest passed gate;
- current blocked gate;
- active next task;
- prohibited actions.

Never silently revert to an older phase because an older document still exists.

## Step 1 — Define the actual problem

Separate:

- technical failure;
- visual/aesthetic failure;
- commercial-readiness failure;
- missing information;
- tooling limitation.

Do not use a technical tool to solve an aesthetic problem unless the tool is actually the bottleneck.

## Step 2 — Classify executor

Choose the lowest-cost specialist capable of producing valid evidence:

`ChatGPT → connected tool / ImageGen / Figma / Adobe → Codex only if engineering trigger exists`.

## Step 3 — Freeze acceptance criteria before execution

Specify what counts as PASS / FAIL before generating or editing.

For visual work, define at least:

- what pixels / structures must remain frozen;
- what exact defects may change;
- what regression is forbidden;
- formal output count;
- whether retries are allowed;
- who has aesthetic authority.

## Step 4 — Execute one controlled change

Avoid changing typography, composition, food styling, copy, and color simultaneously unless the experiment explicitly tests a combined production pass.

## Step 5 — Technical validation

Validate identity, files, exports, changed regions, code/tests where applicable.

Technical PASS is not aesthetic PASS.

## Step 6 — Human/commercial review

Evaluate actual output pixels against the frozen target and reference standard.

Possible states:

- `TECHNICAL_FAIL`
- `VISUAL_FAIL`
- `EXPERIMENT_PASS / COMMERCIAL_NOT_YET`
- `COMMERCIAL_QUALITY_PASS`
- `GOLDEN_EXEMPLAR_CANDIDATE`

## Step 7 — Record state

Every phase report must state:

### 已完成什么

### 未完成什么

Also record:

- exact next gate;
- blocked operations;
- whether Codex was used and why;
- whether Scale Gate remains blocked.

## Step 8 — Promote only after gate evidence

Do not equate one successful improvement with system-level readiness.

`Family Transfer PASS != Commercial Quality PASS != Scale Gate PASS`.

## Step 9 — Scale only after commercial quality

Library/Scale expansion is allowed only when the target quality level is already demonstrated on controlled exemplars. Do not scale a stable 80-point system when the objective is a 90–95-point commercial system.

---

# 6. V3-A current mapping

Current frozen status:

- Family Transfer: `PASS`
- Production Layer Pilot R2: `PASS`
- Functional typography primary blocker: `RESOLVED_ENOUGH_FOR_NEXT_STAGE`
- Commercial Quality Gate: `NOT YET`
- Golden Exemplar: `NO`
- Route B: `SOURCE_MISMATCH_FOR_ROUTE_B`
- Scale Gate: `BLOCKED`

Dominant remaining defects:

1. food / photography realism;
2. synthetic particles and local-detail overload;
3. brand-specific authorship;
4. generic premium-editorial support language;
5. campaign copy / information semantics;
6. overall commercial restraint and art direction.

## V3-A executor decision

Next major stage: `COMMERCIAL HARDENING R3 — ART REALISM & BRAND AUTHORSHIP`

Default orchestration:

- diagnosis / target definition / acceptance criteria: `ChatGPT`;
- selective visual realism edit: `ImageGen`;
- live typography / exact production layout preservation: `Figma`;
- human commercial review: `ChatGPT + human`;
- GitHub state / manifests: `ChatGPT + GitHub connector`;
- Codex: `NOT REQUIRED BY DEFAULT`.

Codex may enter later only if R3 requires actual engineering automation, scripted layer extraction/compositing, batch validation, tests, or repository code changes that cannot be completed with the connected production tools.

---

# 7. Hard anti-regression rules

- Never invoke Codex merely because the user asks a professional question.
- Never let a Codex run replace human aesthetic authority.
- Never regenerate a validated macro composition unless the active task explicitly authorizes it.
- Never allow a newer task to erase an unfinished active gate.
- Never run Scale Gate while Commercial Quality Gate is `NOT YET`.
- Never ask the user for information that the system itself invented/generated unless the missing information is genuinely a user-owned fact required for a real-world claim.

---

# 8. Operating shorthand

Use this decision chain on every new task:

`What is the failure? → What evidence is needed? → Which specialist can produce that evidence most cheaply and reliably? → Is Codex engineering execution actually required? → Execute bounded change → Validate technically → Review visually → Record completed/uncompleted → Advance one gate.`
