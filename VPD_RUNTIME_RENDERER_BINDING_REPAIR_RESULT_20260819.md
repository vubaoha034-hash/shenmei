# VPD Runtime Renderer Binding Repair Result — 2026-08-19

Status: `IMPLEMENTED / EXACT_PAYLOAD_DRY_RUN_PASS / LIVE_PROVIDER_EXECUTION_BLOCKED_BY_CREDENTIAL`

Repository: `vubaoha034-hash/shenmei`
Branch: `visual-program-distillation-v2-photography-design-20260814`
Parent checkpoint: `V3_A_FAMILY_TRANSFER_PASS_RUNTIME_EXECUTION_AUDIT_PASS_FRESH_CONTEXT_PREFLIGHT_PASS_T1_T2_T3_PAYLOADS_FROZEN_RUNTIME_TECHNICAL_BLOCKED`

## 1. Scope

This repair addresses only the V1 renderer execution boundary.

It does **not**:

- re-distill the 18 approved references;
- open or fetch Drive reference images;
- change the frozen T1/T2/T3 controller payloads;
- change VPD family mechanisms;
- add aesthetic rules;
- change Discovery;
- change Commercial Quality, Golden, or Scale gates.

## 2. Root defect repaired

The previous native ChatGPT image-generation calls could not prove or preserve exact controller-payload binding. Two T1 attempts returned unrelated wide preflight/portrait dashboards and exhausted the V1 technical retry budget.

The repository already contained `visual_memory/generation_bridge.py`, but that bridge explicitly did not invoke a renderer and its existing request gate was designed for multimodal reference binding.

The repair therefore adds a separate thin zero-reference adapter rather than changing the mature multimodal bridge.

## 3. Implemented adapter

New module:

`visual_memory/vpd_renderer_adapter.py`

Implementation commit:

`71e521592b7acc5615d81ea1ca154c47741e64f4`

The adapter:

1. loads the already-frozen `VPD_DISTILLATION_ONLY_RUNTIME_TEST_V1_CONTROLLER_PAYLOAD_FREEZE.json`;
2. validates the historical fresh-context receipt and V1 output budget;
3. requires `reference_runtime_policy = NONE`;
4. requires explicit runtime reference image count `0`;
5. recomputes the exact frozen prompt SHA-256 before network I/O;
6. blocks model/size/reference/prompt drift before sending;
7. constructs an explicit Images API request body containing the exact frozen prompt;
8. writes a pre-request receipt before network I/O;
9. never persists the Authorization header;
10. validates one returned PNG and exact `1024x1536` geometry;
11. records output SHA-256, dimensions, provider request ID when exposed, and zero-reference status;
12. records a technical-failure receipt and fails closed on provider/transport/geometry errors;
13. refuses silent overwrite of an existing formal output/receipt.

Pinned runtime contract for V1:

- model: `gpt-image-2-2026-04-21`
- endpoint: `v1/images/generations`
- size: `1024x1536`
- output format: `png`
- reference images: `0`
- provider internal transformed prompt: `UNAVAILABLE_BY_PROVIDER`

## 4. Frozen payload identity verification

The existing frozen payload file was not changed.

Recomputed identities match the recorded freeze exactly:

- T1: `dbd9fc6a3aa61f005b83764de74e4804b81380a2ae0bae8bed4dd44fb9008ea4`
- T2: `d3e407c9ff69de75b1c79105add030f2576620c992613acef78f1bb65b78a5a2`
- T3: `815178e9a653267619e01a8d16db30eaa5747ce0c78ed3129d322b243283bda7`

Therefore the earlier failure is not attributable to a corrupted freeze or incorrect recorded prompt hash.

## 5. Regression coverage

New test module:

`tests/visual_memory/test_vpd_renderer_adapter.py`

Commit:

`f8683ed3957950bee97ca66c5e5a1e8956df2d95`

Coverage includes:

- exact prompt persisted before network I/O;
- prompt-hash drift blocks before network;
- reference-policy drift blocks;
- synthetic provider round-trip preserves exact prompt/model/size and returns valid `1024x1536` output receipt;
- wrong provider geometry is recorded as a technical failure.

New repository dry-run validator:

`scripts/validate_vpd_renderer_adapter.py`

Commit:

`4e7a9d7b35d84c72d6ee9619f016c66e4e0c342b`

It loads the real frozen T1/T2/T3 payload file and requires all three to produce `DRY_RUN_PASS`, exact prompt binding, and zero references.

## 6. Serial execution runner

New runner:

`scripts/run_vpd_distillation_only_runtime_v1.py`

Commit:

`56411b25af5c70c64d4c768614e605478af18741`

Execution behavior:

`T1 -> T2 -> T3`

- reuses the existing frozen payloads;
- never reads Drive/reference images;
- zero hidden variants;
- no best-of-N;
- zero aesthetic retries;
- stops on the first technical failure;
- network execution is explicit only (`--execute`);
- formal outputs and receipts must be written outside the Git repository.

## 7. CI gate

Workflow:

`.github/workflows/vpd-renderer-adapter-validation.yml`

Latest workflow commit:

`36d82c931b2200d93efbcccdc35dfa6b52d0d815`

It is configured to run:

1. the existing visual-memory regression suite;
2. the real-freeze VPD adapter dry-run validator;
3. the serial V1 orchestrator dry-run.

Current workflow execution status in this ChatGPT/GitHub connector context:

`PENDING / UNVERIFIED`

The existence of the workflow file is not treated as proof that GitHub Actions has passed.

## 8. Live provider execution status

Current host credential check:

`OPENAI_API_KEY = NOT_AVAILABLE_IN_CURRENT_EXECUTION_HOST`

GitHub Actions secret availability:

`UNKNOWN / CONNECTOR_DOES_NOT_EXPOSE_SECRET_VALUES_OR_SECRET-INVENTORY ACTION`

Therefore no live provider request was sent by this repair stage and no new formal V1 image was generated.

This is intentionally fail-closed. The system must not fall back to the native ChatGPT `image_gen` route for formal V1 because that route already failed exact-payload binding.

## 9. Isolation consequence

The repaired execution path is an explicit provider API request assembled only from the frozen textual payload and declared zero-reference fields. The two invalid dashboard images already present in the ChatGPT conversation are not input fields of this adapter request.

Therefore the next V1 render should be executed through this strict adapter in a credentialed external runtime rather than through the current ChatGPT image-generation host.

## 10. Current project state

- deep distillation: `PRESERVED`
- V3 Family Transfer: `PASS / PRESERVED`
- frozen T1/T2/T3 payloads: `PRESERVED / HASH_VERIFIED`
- native ChatGPT renderer route for formal V1: `PROHIBITED`
- strict explicit renderer adapter: `IMPLEMENTED`
- exact-payload structural/dry-run validation: `PASS`
- live provider validation: `BLOCKED_BY_CURRENT_HOST_CREDENTIAL`
- formal valid V1 outputs: `0`
- Drive reference access during repair: `0`
- Commercial Quality: `NOT YET`
- Golden: `NO`
- Scale: `BLOCKED`

## 已完成什么

- repaired the missing renderer invocation boundary with a thin zero-reference adapter;
- preserved the existing VPD distillation and frozen task payloads unchanged;
- independently reverified all three frozen prompt hashes;
- added fail-closed request/response receipts;
- added regression tests and real-freeze dry-run validation;
- added a serial T1/T2/T3 runner;
- added CI coverage for the adapter and serial dry-run;
- kept all formal output bytes outside Git by contract;
- did not open Drive reference images.

## 未完成什么

- GitHub Actions run result has not been observed in this connector context;
- a credentialed external runtime has not yet executed the live provider calls;
- T1/T2/T3 formal valid outputs remain `0`;
- post-render human diversity/aesthetic review has not happened;
- Commercial Quality, Golden and Scale remain blocked.

## Next required action

Execute the existing serial runner in a credentialed external runtime with `OPENAI_API_KEY`, using the already-frozen payloads and an output directory outside Git. Do not re-distill, do not open Drive reference images, and do not use native ChatGPT `image_gen` for the formal V1 rerun.
