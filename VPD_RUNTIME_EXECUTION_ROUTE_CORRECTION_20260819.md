# VPD Runtime Execution Route Correction — 2026-08-19

Status: `STATE_CORRECTED / ACTIONS_WIF_OPTIONAL / LIVE_RUNTIME_NOT_YET_SELECTED`

Repository: `vubaoha034-hash/shenmei`
Branch: `visual-program-distillation-v2-photography-design-20260814`

## Why this correction exists

The prior state incorrectly promoted GitHub Actions + OpenAI Workload Identity Federation (WIF) from one possible execution/authentication implementation into a mandatory VPD gate.

That was an execution-infrastructure choice, not a requirement of `VPD_DISTILLATION_ONLY_RUNTIME_TEST_V1.md`.

The frozen V1 protocol requires:

- fresh/isolated renderer execution;
- zero runtime reference images;
- exact compiled payload and SHA-256 captured;
- actual renderer identity/settings captured to provider limits;
- exact outputs captured;
- exactly three formal outputs, one per T1/T2/T3, with fail-closed technical handling.

It does **not** require GitHub Actions, WIF, OIDC, a service account, or any particular cloud executor.

## Preserved work

The following remain valid and must not be rolled back:

- deep VPD distillation is preserved; do not re-distill the same approved references;
- `V3_A_FAMILY_TRANSFER` remains PASS as transferable-family evidence;
- `VPD_DISTILLATION_ONLY_RUNTIME_TEST_V1_CONTROLLER_PAYLOAD_FREEZE.json` remains unchanged;
- T1/T2/T3 prompt SHA-256 identities remain unchanged;
- `reference_runtime_policy = NONE` and runtime reference image count `0` remain hard requirements;
- `visual_memory/vpd_renderer_adapter.py` remains the strict exact-payload bridge;
- `scripts/run_vpd_distillation_only_runtime_v1.py` remains the serial fail-closed runner;
- native ChatGPT `image_gen` remains disallowed for **formal V1** because two prior T1 calls failed exact-payload binding;
- Commercial Quality, Golden and Scale gates are unchanged.

## Correct execution model

The execution environment is now deliberately neutral:

`frozen VPD payload -> strict adapter -> explicit renderer request -> output + receipt`

Any private/credentialed runtime may be used if it can execute the existing strict adapter without changing the frozen payload or zero-reference contract.

Examples include a local machine, private VM/container, private notebook/runtime, or GitHub Actions. These are implementation choices, not VPD acceptance gates.

GitHub Actions is therefore:

`OPTIONAL_EXECUTION_ENVIRONMENT_NOT_VPD_GATE`

OpenAI WIF is therefore:

`OPTIONAL_AUTH_METHOD_NOT_VPD_GATE`

The existing WIF probe/setup files remain historical/optional infrastructure evidence only. They do not block another valid private execution environment.

## Why not silently switch to another currently-connected image renderer

A renderer substitution would change the runtime under test and must not be hidden.

The current native ChatGPT image-generation route already failed exact prompt binding and cannot be used for formal V1.

A currently connected explicit-prompt image provider would also need to accept the **exact** frozen payload unchanged and support the frozen geometry/output contract. If it cannot, compressing or rewriting the payload would invalidate this exact-runtime test.

Therefore the shortest valid path is not to rewrite prompts or add infrastructure. It is to execute the already-built strict adapter in the first available private runtime that can send the exact request.

## Current state

- renderer binding repair: `IMPLEMENTED_NOT_LIVE_PROVIDER_VALIDATED`
- exact-payload dry-run: `PASS`
- frozen T1/T2/T3 payloads: `PRESERVED / HASH_VERIFIED`
- live execution environment: `NOT_YET_SELECTED`
- GitHub Actions: `OPTIONAL`
- WIF: `OPTIONAL`
- formal valid V1 outputs: `0`
- reference images attached: `0`
- Drive approved-reference images opened during this correction: `0`
- Commercial Quality: `NOT YET`
- Golden: `NO`
- Scale: `BLOCKED`

## 已完成什么

- corrected the false premise that GitHub Actions/WIF is a mandatory VPD gate;
- preserved the strict renderer adapter and frozen payloads;
- restored execution-environment neutrality;
- retained WIF tooling only as optional infrastructure;
- kept formal V1 output budget untouched at 0/3.

## 未完成什么

- select or obtain one private runtime that can execute the strict adapter with provider credentials/network access;
- execute T1 -> T2 -> T3 live without changing the frozen payloads;
- capture three technically valid outputs and live receipts;
- perform human diversity/aesthetic review;
- Commercial Quality, Golden and Scale remain pending.

## Next required action

Run the existing strict adapter/serial runner in **any** private credentialed runtime that can reach the pinned renderer API. Do not treat GitHub Actions or WIF as prerequisites. Do not re-distill, rewrite T1/T2/T3, open Drive reference images, or fall back to native ChatGPT `image_gen` for formal V1.