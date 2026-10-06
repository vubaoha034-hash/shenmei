# Independent implementation review — 2026-10-06

Verdict: FAIL for published source commit c6f8e614a7056ccbd0358945ff4bfafc6a34bc31. Production authenticated connection and real D1 persistence remain INCONCLUSIVE. A local correction is not a deployed correction; a succeeding deployment is not an installed plugin.

Independent challenger; fresh task context; no implementation authorship, delegation, production writes, mainline edits, visual judgment, or access to this round's pixel-reviewer directory. I wrote only audit evidence/isolated test fixtures under this directory. Root reports fixes are in progress; those are not included in this verdict.

## Scope and identities

- Repository state tested: actual committed native Git blobs at 4d128f7b44dc43163f021b5717f5e003ca70a323. The repository has concurrent uncommitted business-state changes; tests deliberately read committed blobs and do not certify those changes.
- Reviewed core.mjs, worker.mjs, build.mjs, db/schema.ts, migration, both tests, README, SKILL, package metadata and deployed mirror.
- Core SHA256: bde48b58634d8784babf834bc343bc6801cab983a3d90b5d0d333db44dec6ebc.
- Worker SHA256: f51d4fccd6b80e1981113122797dbb75e27daabe3fb3e3307066719700a2ed9c.
- Build SHA256: 646859f26d7f45af525758079826e3743b2251981e238bcc1322bf800bad5f3f.
- Schema SHA256: fecb781110790048c7c45d4ef984740f764327df58619f55a2ebc0431227f90e.
- Initial SKILL SHA256: d2bd636913425b9162d04fc15422e695075907f550ea747581356fa36810d6da.
- Root plugin, Site source and built worker/core hashes matched at initial inspection. Frozen executable copies are in isolated-build/.
- Applied instructions: AGENTS.md, START_HERE and native lock/mainline/adapter/current-entry governance, charter, independent challenger restrictions. adaptive-orchestrator version check reported MAINTENANCE_REQUIRED; no routing or global configuration was modified.

## Blocking findings for the claimed usable release

1. **Published workflow instructs a non-persisting feedback call.** SKILL step 7 tells the user agent to call prepare_human_feedback; worker.mjs:47–49 only advertises save_human_feedback. The hidden prepare tool nevertheless remains callable through worker.mjs:64 and returns HTTP 200 with persisted:false; the database stays empty. A client following the shipped Skill cannot complete the promised durable feedback path. Reproduced against frozen published code, not inferred from documentation alone. Root says the local Skill is corrected; published c6 is still the artifact reviewed here.

2. **MCP envelope and transport validation is bypassed or incomplete.** worker.mjs:47–60 handles list/read before core validation. jsonrpc:'wrong' with tools/list returns 200/tool discovery; jsonrpc:'wrong' with get_human_feedback and arguments:0 returns 200/persisted intake data. core.mjs:121–125 does not validate request IDs: an id-less tools/call save_human_feedback performs an actual local SQLite insert and returns HTTP 200/id:null/persisted:true. worker.mjs ignores unsupported MCP-Protocol-Version headers; invalid-version + ping returns 200. These are real execution counterexamples on local synthetic data, not claims of a production exploit. Central validation must run before read/write dispatch, require valid IDs for requests, handle notifications appropriately, validate tool argument objects and reject unsupported protocol headers.

The official 2025-06-18 protocol requires valid JSON-RPC and string/integer non-null request IDs; accepted notifications return HTTP 202 without a body, and invalid/unsupported version headers require HTTP 400:
[base protocol](https://modelcontextprotocol.io/specification/2025-06-18/basic), [HTTP transport](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports).

## Non-blocking but material finding

3. **Older pending feedback becomes inaccessible through the plugin.** worker.mjs:57 uses LIMIT 50, and get_human_feedback accepts no filtering/paging argument. After 51 synthetic rows for one actor, only 50 return with no cursor/truncation indicator; there is no exposed by-key retrieval tool. Rows remain in storage, but Root cannot retrieve all pending records through the plugin. Continuous use needs pagination or equivalent exact-key retrieval, ideally with a stable ordering tie-breaker.

## Verified strengths and scope limits

- Mainline identity, three-file lock hash/revision, task/stage/status, next action, immutable commit reads, bound roadmap/entry/evidence and reference/artwork relationships are checked. HEAD changes fail closed before response and immediately before persistence; this is not an atomic Git/database transaction.
- Core and Skill explicitly disclose no image engine, Figma editor, Drive pixel transport or independent review engine. No newly executed visual review, training, business-state promotion or native Git write is claimed by the executable code. AI verdict and human acceptance remain separate. Existing recorded cold evidence is labeled as recorded, not re-executed.
- The cold-evidence helper checks structure and hashes of repository records; it does not rerun the native collector or establish provider-internal isolation. The code discloses this limitation. Local test fixtures for human wording are explicitly synthetic.
- saveIntake uses actor/key uniqueness and INSERT OR IGNORE, rejects conflicting replay, preserves the original timestamp on an identical retry, and fails when storage is missing. The schema matches the SQL migration. Local SQLite reopening genuinely verified local file durability; it is not a production D1 test.
- Worker relies on Sites' trusted user header and authorizes any authenticated header identity, rather than comparing an owner ID in worker code. Independent get_site returned custom access with exactly one owner, no external visitors, groups or editors. This matches the intended platform-enforced owner-only boundary. No direct header spoofing, OAuth bypass or alternate endpoint probe was attempted. Broader future Site sharing would broaden application access unless the implementation adds an owner ACL.
- Independent Sites API readback: deployment appgdep_6ac46cfd18ac8191ac7214711a53e752 succeeded, has_mcp:true, live URL https://liu-visual-workflow-20261006.deemoliul.chatgpt.site. Returned MCP/plugin connection metadata does not establish installation or a successful authenticated tool call.

## Executed verification

- Bundled Node v24.19.0 ran both original suites: 27/27 PASS (baseline-tests.txt). Worker test SQLite artifacts were redirected beneath this owned audit directory using the working directory and subprocess GIT_DIR; no business store was touched.
- supplemental-frozen.mjs reproduces findings 1–3 using original committed native blobs and an in-memory SQLite database. See supplemental-results-frozen.txt.
- protocol-header.mjs reproduces unsupported-version acceptance. See protocol-header-results.txt.
- Isolated build copied only reviewed source and nonsecret hosting config into this directory, ran build.mjs, imported dist/server/index.js and executed the health handler successfully. It did not publish or alter the live site.
- github-readonly.mjs attempted the real public GitHub adapter. It returned 502. Direct diagnostic isolated local network failure: getaddrinfo ENOTFOUND api.github.com. This does not establish a Cloudflare/runtime failure, but prevents this reviewer from claiming actual remote branch reads were verified. See github-readonly-results.txt and github-diagnostic-results.txt.
- Initial supplemental script had an incorrect relative import and failed before execution; supplemental-results.txt preserves that failure. Corrected execution and frozen replay both produced the stated findings.

## Missing evidence / release boundary

No reviewer-observed authenticated production initialize/tools/list/get_current_workflow call, no actual production D1 write/readback, no installed/connected plugin proof, and no verified end-to-end production image→Figma→independent review→Drive→native Git execution through this plugin. Core tests plus Sites deployment prove a bounded implementation and publication, not those capabilities. Resolve findings 1–2 and rerun adversarial cases on the corrected immutable source before upgrading the implementation verdict. Report production connection/D1 as pending until actual authorized evidence exists.
