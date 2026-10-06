# Independent corrected-source review — 2026-10-06

Verdict: PASS for the bounded implementation corrections in the root plugin source identified below. The initial published c6f8e614a7056ccbd0358945ff4bfafc6a34bc31 FAIL remains preserved in INITIAL_REVIEW.md. This source review does not upgrade that old deployment. Production OAuth connection, authenticated MCP execution and real D1 persistence remain INCONCLUSIVE.

## Exact reviewed source

Source directory: plugins/visual-aesthetic-workflow in shenmei-vpd-resume-20261006. Native committed baseline used by the tests: 4d128f7b44dc43163f021b5717f5e003ca70a323. The plugin is still untracked in that repository at review time; these file hashes and final-snapshot/ identify the corrected artifact independently of the old repository HEAD.

| File | SHA256 |
| --- | --- |
| core.mjs | dd82b4527282a2e9baa5c2be8614b2d56cd680357c40758aee6408dcad03ede8 |
| worker.mjs | 8aeab739d994c0675e32f49e7ea279a9f21f0a050573dd82337dcbc4a6d33710 |
| core.test.mjs | 9b7107d4562cf5b625946ecc7fdc25c011a5f5dad3c9e99b28d141112b5b8297 |
| worker.test.mjs | 71ec9b38ab91c68f347bc8fd98c3b0bb09b5f0e8566ac86eca1f87c98402b2c8 |
| README.md | 05828dc71ec5ff7a380c7fd5978d5940f7350ab5866c4207c2f8749800634a0d |
| SKILL.md | 1639a6c556697044cacc76632720a97fca2dc5d0a2c92f58d6e9ba126ffad86f |

Full snapshot manifest: final-source-manifest.json. build.mjs and schema implementation are unchanged from initial review. Actual source diffs were inspected against the initial isolated-build copy and the intermediate revised-snapshot; the final protocol change replaces finite numeric IDs with integer IDs and accepts string IDs, including the empty string.

## Closure of initial findings

1. **Feedback workflow mismatch — CLOSED.** Skill step 7 and README now specify published save_human_feedback, require persisted:true plus durable_receipt, and require get_human_feedback readback. worker rejects the internal prepare_human_feedback name with HTTP 400 before database access. Independent replay confirms valid save returns a receipt and exact-key readback returns the saved synthetic comment.

2. **Envelope/transport validation bypass — CLOSED for the reproduced cases.** validateRpcRequest runs before every HTTP dispatch. Independent replay confirms wrong JSON-RPC discovery/read, scalar arguments, null ID and an id-less save all return 400, without touching storage. Unsupported MCP-Protocol-Version returns 400. Initialized notification returns 202 with an empty body. Final independent ID probe confirms 1.5 returns 400 while integer and string IDs, including empty string, return 200. An intermediate fractional-ID tolerance was independently found, retained in revised-id-probe-results.txt, then corrected; this report binds the corrected final hash.

3. **Older pending records hidden by LIMIT 50 — CLOSED.** Worker now supports actor-scoped exact-key lookup and descending (recorded_at,idempotency_key) cursor pagination. Independent replay used 51 records with identical timestamps, page limit 7 and 8 actual database queries: 51 unique records returned with no duplication or omission. A second actor with the same key receives only their own payload and cannot fetch the owner's other keys. Missing identity returns 401. This replay used actual in-memory SQLite SQL execution, not a mocked row list.

## Cold-evidence validation and mainline checks

The new cold-evidence changes require verified:true, the expected model/effort, exactly two image records, two distinct call IDs with valid hashes, consistent turn/spawn fields, and a hash-bound reviewed-call manifest whose call IDs/names/input hashes match the audit.

I executed all eight new negative mutations: verified=false; wrong model; wrong effort; inconsistent turn-context effort; inherited spawn; an extra image read; a removed tool call; and a changed call-input hash. Each returned MISSING_OR_INVALID_NO_PASS while preserving promotion_allowed:false. These are synthetic hash-rebound protocol fixtures based on the committed old S4 evidence. They prove these validation branches work; they do not prove a new real cold review or provider-internal isolation.

Diff inspection found no change to the canonical repository/branch, pinned mainline policy hashes, native task/stage/action checks, artwork/reference bindings, before/after HEAD guards, scope controls, or separate AI/human acceptance. New permissions are not added. The final independent replay confirms image_generation, drive_pixels, figma_edit, independent_reviewer and business_state_write all remain false, and promotion_allowed remains false. Feedback persists only as non-authoritative intake pending Root reconciliation. No second business authority or automatic human acceptance appears in this diff.

## Actual execution evidence

- final-suite-results.txt: 33/33 original-plus-new tests executed, exit 0, using bundled Node v24.19.0. This includes local file-backed SQLite reopening, idempotency conflict handling, all eight cold-record negative mutations and tied-timestamp pagination/actor isolation.
- final-independent-replay-results.txt: reviewer-written replay independently re-runs the initial attack inputs, legal save/readback, 8-page tied-timestamp retrieval, same-key actor isolation, identity rejection and capability boundaries against the frozen final snapshot.
- final-id-probe-results.txt: final fractional/integer/empty-string/string request-ID checks.
- Initial failed reproduction and initial/intermediate results remain intact. No failure history or acceptance criteria were rewritten.

Reviewer actions were confined to read-only root-source inspection and audit-local test files/databases. No source, business state, Site deployment, external feedback store or pixel-reviewer directory was modified or accessed. This remains an independent implementation review, not a design review.

## Unchanged production boundary

Owner-private Sites access and old-version deployment provenance were independently read during initial review. Worker still depends on the documented Sites trusted-header boundary and its owner-only audience; local synthetic identities are not production authentication evidence. No header bypass or OAuth workaround was attempted.

This turn did not install a plugin, publish the correction, run an authenticated production MCP call or write/read production D1. The initial local real-GitHub transport attempt failed because api.github.com did not resolve in this environment; that result remains a local networking limitation, not evidence that the cloud runtime fails.

The source is ready for the Root's already-authorized same-Site publication and subsequent immutable-source/hash readback. Claim only source fixes verified until the corrected deployment is actually observed; claim connected and durable in production only after actual authorized OAuth tool-call and D1 readback evidence. A full image→Figma→independent review→Drive→native Git workflow still requires the external tools and Root route disclosed by this plugin.
