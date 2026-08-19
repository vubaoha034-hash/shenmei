# VPD Codex Handoff — 2026-08-19

Status: `PAUSED_FOR_CODEX_CONTINUATION / NO_MORE_CHATGPT_RUNTIME_INFRASTRUCTURE_EXPANSION`

Repository: `vubaoha034-hash/shenmei`
Branch: `visual-program-distillation-v2-photography-design-20260814`

## Current accepted state

- Deep VPD distillation is already present. Do not re-distill the approved references.
- `V3_A_FAMILY_TRANSFER` remains PASS as preserved transferable-family evidence.
- `VPD_DISTILLATION_ONLY_RUNTIME_TEST_V1_CONTROLLER_PAYLOAD_FREEZE.json` is authoritative and must remain unchanged.
- T1/T2/T3 frozen prompt hashes are already reverified.
- `reference_runtime_policy = NONE`; runtime reference image count must remain `0`.
- `visual_memory/vpd_renderer_adapter.py` exists and its exact-payload dry-run passed.
- `scripts/run_vpd_distillation_only_runtime_v1.py` exists and serializes T1 -> T2 -> T3 with fail-closed behavior.
- Native ChatGPT `image_gen` is not allowed for formal V1 because two T1 invocations failed exact payload binding.
- GitHub Actions and OpenAI WIF are optional infrastructure only, not VPD acceptance gates.
- Formal valid V1 outputs remain `0/3`.
- Commercial Quality = `NOT YET`; Golden = `NO`; Scale = `BLOCKED`.

## Codex continuation scope

Codex should continue repository engineering and runtime completion from the current branch/checkpoint. The goal is to finish the Skill/runtime path with the minimum additional infrastructure.

Codex may:

1. inspect and validate the existing strict renderer adapter and serial runner;
2. simplify or harden implementation bugs that prevent already-canonical behavior, without changing VPD aesthetics or frozen payload semantics;
3. use the first available private credentialed renderer runtime if one exists in the Codex execution environment;
4. execute the existing formal V1 only if exact frozen payload binding, zero references, renderer identity/settings and output receipts can be demonstrated;
5. persist all material state changes through the existing continuity checkpoint/ledger rules.

## Hard prohibitions

Codex must NOT:

- re-distill the approved reference set;
- open Drive approved-reference pixels merely to continue this runtime test;
- rewrite, compress or paraphrase T1/T2/T3 frozen payloads;
- make GitHub Actions or WIF mandatory again;
- add more authentication/cloud infrastructure unless it is actually necessary for the selected execution environment;
- silently substitute another renderer/model and claim it is the same formal V1;
- use native ChatGPT `image_gen` as the formal V1 renderer;
- create hidden variants, best-of-N, or aesthetic retries;
- promote Commercial Quality, Golden or Scale without the required human/artifact evidence.

## Formal V1 execution contract

When a valid private runtime exists, run the existing serial path from the authoritative freeze:

`T1 -> T2 -> T3`

Requirements:

- exact frozen prompt/hash;
- one formal output per task;
- zero runtime reference images;
- `1024x1536` PNG under the currently pinned adapter contract unless an explicitly authorized protocol change is made;
- output and provider receipts captured outside the public Git repository;
- stop on the first deterministic technical failure according to the V1 protocol;
- after three valid outputs, hand them to human review for diversity and absolute aesthetic quality.

## Primary files to read first

1. `PROJECT_CONTROL_ADAPTER.json`
2. `continuity/vpd/LATEST_CHECKPOINT.json`
3. `VPD_RUNTIME_EXECUTION_ROUTE_CORRECTION_20260819.md`
4. `VPD_DISTILLATION_ONLY_RUNTIME_TEST_V1.md`
5. `VPD_DISTILLATION_ONLY_RUNTIME_TEST_V1_CONTROLLER_PAYLOAD_FREEZE.json`
6. `VPD_RUNTIME_RENDERER_BINDING_REPAIR_RESULT_20260819.md`
7. `visual_memory/vpd_renderer_adapter.py`
8. `scripts/run_vpd_distillation_only_runtime_v1.py`

## Next required action

Codex should first validate the existing adapter/runner in its own execution environment and determine whether it already has a usable private renderer credential/network path. If yes, execute formal V1 without changing the frozen payloads. If no, stop at a clearly documented external-runtime blocker; do not build additional infrastructure merely to avoid declaring the blocker.
