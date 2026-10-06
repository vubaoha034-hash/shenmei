> 当前实际安装状态（2026-10-06）：**已安装、已连接、只读调用已核验**。以CONNECTION_VERIFICATION.json及当前原生回执绑定的安装证据为准；源码部署为0.1.1。下方保留原0.1.0基线说明，不能用其旧版限制覆盖新运行证据。实际调用方式及范围见 ../../evidence/vpd/codex_takeover_20261003/liuxiansheng_content_transfer_20261005/plugin_installation_20261006/README.md。

# Visual aesthetic workflow MCP core

Experimental version **0.1.0**. This package wraps the existing native Shanyeji → Liu typography experiment. It reads actual authoritative GitHub state, prepares a seven-variable production/review handoff, and validates human feedback for append-only intake. It does not generate an image, edit Figma, fetch Drive pixels, run an independent reviewer, train a model, schedule work or update business acceptance.

The S4 baseline records `CONTENT_TRANSFER_PASS_WITH_LIMITATIONS`, human `PENDING`; whole visual quality and time savings are unverified. Complete artwork SHA256 is `ddb621ebf7e230279a1358b1b93ab9fcd55705b7e6ca99af8649aa3295ab1ca4`, reference SHA256 `9a29fbdc7dd908017924bed270e8dfe18351519eed3fa7bc7001789f2a383414`. Real saved positions are Drive `1V_7Vlv4wJj_LZz6nGXlMxZ2hCxhXX5kD` and Figma file `uyDxOoN1iNDPpEHTKSUWg1`, node `442:2`; current responses resolve these from bound native records. Recorded Drive readback and cold review are existing evidence, not a new tool operation performed by the plugin.

## Host interface

The published Sites HTTP adapter exposes `get_current_workflow`, `compile_transfer_plan`, `save_human_feedback` and `get_human_feedback`. The `prepare_human_feedback` row below documents the internal dependency-neutral core, not a callable published workflow. Use `save_human_feedback`, require its durable receipt, and verify with `get_human_feedback`; the latter supports an exact `idempotency_key` or stable pagination (`limit` up to 50 and returned `next_cursor`). Feedback remains pending Root reconciliation with the native task.

`core.mjs` is a stateless ES module using WebCrypto by default. No dependencies or Node-specific imports are required in production. The host provides actual repository transport and owner authorization:

```js
import { createCore } from './core.mjs';
const core = createCore({
  resolveHead: async ({ repository, branch }) => /* latest GitHub 40-character SHA */,
  readFile: async ({ repository, branch, commit, path }) => /* exact UTF-8 Git blob bytes */,
  authorize: async ({ userId }) => /* trusted hosting identity owner ACL */,
  // Optional: hash(bytes) → lowercase SHA256; now() → ISO date string.
});
const { status, body } = await core.handle(jsonRpcRequest, trustedIdentity);
```

The comments above describe adapter contracts; they are not executable adapter implementations. `resolveHead` must resolve the live canonical branch without serving a stale fixture as latest. `readFile` must fetch **every** requested file at the given immutable commit, preserve original bytes/newlines, and fail on missing/inaccessible files. Core resolves HEAD before and after data-bearing calls, validates lock SHA/revision from checkpoint and adapter, matches task/stage/action, checks the pinned mainline policy and bound entry/roadmap/evidence files. It caches only within a single call.

The host exposes stateless HTTP `POST /mcp`, validates JSON/body limits, and translates core `{status, body}` to HTTP. Initialization, discovery, ping and initialized notification contain no private project data. Data-bearing `tools/call` requires trusted hosting identity and an explicit owner ACL; the default ACL denies everyone. Never construct identity from tool arguments or accept spoofed identity headers on an untrusted alternate endpoint. Sites handles authentication at its boundary; this core implements neither OAuth nor deployment.

| Tool | Output | External actions |
| --- | --- | --- |
| `get_current_workflow` | Same-commit bound native state, current entry, real reference/artwork locations and pixel requirements | GitHub reads only |
| `compile_transfer_plan` | Seven-variable prompt and reference/copy/image/Figma/independent-review/repair/save handoff, recognized/rejected evidence | Draft only; no execution authorization |
| `prepare_human_feedback` | `validated_intake`, stable `content_sha256`, `persisted: false` | Validation only; host performs persistence |

Feedback requires `expected_commit`, `artwork_sha256`, `idempotency_key`, `verdict`, and `comment`. The host must recheck actual HEAD immediately before append, persist in its configured durable store, enforce actor/idempotency uniqueness, return an existing identical record on replay, and reject conflicting content. Core's content hash excludes its recording timestamp for replay stability. Host must not report `persisted: true` until durable commit succeeds. Intake is separate from business authority: Root reconciles it against the exact native artwork and user scope, preserving historical evidence. It is not another task table. No caller-controlled acceptance, mainline or AI-review fields are accepted.

Core reports whether the pinned repository contains the existing bound cold-review audit structure; it does not rerun the native collector or independently prove provider-internal isolation. New production requires the original native independent-review route. Even a recorded passing result has `promotion_allowed: false` here. Independent review without actual original pixels cannot pass. Figma contours are editable vectors, not automatically type-to-replace text.

When the native transfer includes `human_local_repair_allocation`, core verifies that allocation's schema/hash and its feedback reference/hash, then binds feedback to the actual delivered artwork and `S4_OUTLINE_AND_XIAN_CONTINUITY_ONLY` scope. Current-workflow and transfer-plan responses expose the original human wording and artwork SHA as `latest_human_feedback`. Historical AI_PASS is explicitly not human final acceptance, which remains PENDING. Feedback helps the creator apply scoped repairs; it must be excluded from the cold review packet to avoid verdict leakage. Continuous improvement comes from actual human and independent-review evidence followed by authorized local changes, not background training or automatic rule accumulation.

## Checks and limits

Run from the repository checkout:

```sh
node --test plugins/visual-aesthetic-workflow/core.test.mjs
```

Tests read the immutable published S4 commit `4d128f7b44dc43163f021b5717f5e003ca70a323` as a regression baseline, then exercise authentication, MCP initialization/discovery, same-SHA reads, concurrent HEAD changes, lock hashes, evidence hashes, mainline tampering, missing cold-pixel evidence, self-review promotion rejection and artwork-bound feedback. The deployed runtime resolves the actual latest branch; it does not serve this test baseline as current. Separate repository-entry recovery verifies each new delivery. These are engineering tests, not a new artwork demonstration or aesthetic approval.

Not implemented by the core: HTTP hosting, GitHub HTTP adapters, request ACL configuration, durable feedback write/read APIs, plugin connection/installation, Drive/Figma/image execution, review context creation and native business-state reconciliation. Host-owned implementation files may supply transport and intake persistence; consult those actual files and deployment receipts before claiming they are live. Missing external capabilities remain explicit limits; no mock response may be described as real production.

Governance sources: repository `AGENTS.md`, `START_HERE.md`, `AESTHETIC_SKILL_DESIGN_CHARTER.md`, native state trio and `WORKER_CURRENT_REUSE.md`. Stateless transport guidance comes from the installed Sites MCP skill. Skill packaging follows the installed `skill-creator`; neither source changes the native mainline or acceptance criteria.
