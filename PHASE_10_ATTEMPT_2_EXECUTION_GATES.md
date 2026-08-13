# PHASE 10 ATTEMPT 2 — EXECUTION GATES

Status: `REQUIRED_BEFORE_GENERATION`

## Gate A — Attempt 1 quarantine

Verify Attempt 1 remains permanently invalid and isolated:

- contaminated P10-01 output remains `blind_eval_reserved`;
- Attempt 1 blind ledger/mapping is not reused;
- the user's reaction to the leaked baseline is not Discovery Evidence;
- no Attempt 1 artifact enters ContextPack or skill-refiner.

## Gate B — Frozen Discovery state

Before Attempt 2 generation:

- Discovery approved remains 18;
- Discovery rejected remains 12;
- effective Discovery feedback remains the PHASE 9 frozen set;
- `doctor() == []`;
- fresh Attempt 2 replication snapshot verifies true;
- ContextPack remains domain `餐饮`, positive max 4, negative max 2.

Any drift blocks the run.

## Gate C — New Attempt 2 task lock

Read exactly `PHASE_10_ATTEMPT_2_TASKS.json`.

- exactly 20 tasks;
- IDs P10A2-01..P10A2-20;
- 4 tasks in each frozen category;
- no exact task reuse from Phase 9 or Attempt 1;
- task file SHA recorded before generation.

## Gate D — New independent mapping

Create a new cryptographically random A/B mapping for Attempt 2.

- do not read Attempt 1 mapping when producing it;
- store only in a new private Attempt 2 blind ledger;
- lock before the first output is generated.

## Gate E — No user-visible generation path

Before rendering the first image, prove the selected rendering path does not expose to the voting user:

- condition label;
- prompt text;
- ContextPack;
- individual output during generation;
- condition-bearing filename/metadata.

If this cannot be guaranteed, stop with `ATTEMPT_2_BLOCKED_NO_BLIND_RENDER_PATH`.

## Gate F — Opaque generation package

Private orchestration may refer to the two conditions only through opaque tokens at the renderer boundary. The Baseline/Personalized mapping stays in the private ledger.

The user sees nothing until the full blind package is ready.

## Gate G — Pair symmetry

For all 20 tasks:

- same frozen task brief;
- same route/Skill;
- same renderer/model/ratio/parameters;
- exactly one generation per condition unless technical no-image failure;
- no visual-quality retry/repair;
- all outputs `blind_eval_reserved`.

## Gate H — Post-generation frozen-state check

After all Attempt 2 outputs are generated and before presentation:

`verify_replication_snapshot(...) == True`

Otherwise Attempt 2 is invalid.

## Gate I — Leak audit before first presentation

Scan the user-visible review package, filenames, captions and metadata.

It must not reveal:

- baseline/personalized;
- hidden mapping;
- condition prompt;
- ContextPack or personal exemplar role;
- private source IDs that reveal condition.

Only after this audit passes may the first A/B pair be shown to the user.

## Gate J — Voting and scoring

- user votes only A/B/tie;
- all votes lock before unblinding;
- no interim scores;
- use existing pre-registered `summarize_replication` threshold;
- final report must disclose `prior_condition_exposure=true`.
