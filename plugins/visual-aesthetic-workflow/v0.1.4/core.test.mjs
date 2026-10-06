import test from 'node:test';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';
import { createCore, SOURCE, PATHS, TOOLS, sha256 } from './core.mjs';
import { createCore as stableCore } from './baseline-core-v0.1.1.mjs';

const cwd = process.env.SHENMEI_TEST_REPOSITORY ?? fileURLToPath(new URL('../../', import.meta.url));
// Immutable real S4 baseline; production adapters still resolve actual live HEAD.
const commit = execFileSync('git', ['rev-parse', '4d128f7b44dc43163f021b5717f5e003ca70a323^{commit}'], { cwd, encoding: 'utf8' }).trim();
const hash = async value => createHash('sha256').update(value).digest('hex');
const originals = new Map();
function gitBytes(path) {
  if (!originals.has(path)) originals.set(path, execFileSync('git', ['show', `${commit}:${path}`], { cwd }));
  return originals.get(path);
}
const identity = { userId: 'test-owner' };
const call = (name, args = {}) => ({ jsonrpc: '2.0', id: 1, method: 'tools/call', params: { name, arguments: args } });
function fixture({ transform, heads, authorized = true, factory = createCore } = {}) {
  let headCalls = 0;
  const reads = [];
  const overrides = new Map();
  const json = path => JSON.parse(overrides.get(path) ?? gitBytes(path).toString('utf8'));
  const put = (path, value) => overrides.set(path, Buffer.from(JSON.stringify(value)));
  if (transform) transform({ json, put, overrides });
  const core = factory({
    resolveHead: async source => { assert.deepEqual(source, SOURCE); return heads ? heads[Math.min(headCalls++, heads.length - 1)] : commit; },
    readFile: async input => { assert.equal(input.commit, commit); assert.equal(input.repository, SOURCE.repository); reads.push(input); return overrides.get(input.path) ?? gitBytes(input.path); },
    authorize: async who => authorized && who.userId === identity.userId,
    hash,
    now: () => '2026-10-06T00:00:00.000Z'
  });
  return { core, reads };
}
function data(response) { assert.equal(response.status, 200, JSON.stringify(response.body)); return response.body.result.structuredContent; }
function rebindLock({ json, put, overrides }) {
  const digest = createHash('sha256').update(overrides.get(PATHS.lock)).digest('hex');
  for (const path of [PATHS.checkpoint, PATHS.adapter]) { const state = json(path); state.task_lock.sha256 = digest; put(path, state); }
}

test('MCP initialize, stateless discovery, ping and initialized notification expose no private state', async () => {
  const { core, reads } = fixture();
  const init = await core.handle({ jsonrpc: '2.0', id: 1, method: 'initialize', params: { protocolVersion: '2025-06-18' } });
  assert.equal(init.body.result.protocolVersion, '2025-06-18');
  assert.equal(init.body.result.serverInfo.version, '0.1.4');
  const list = await core.handle({ jsonrpc: '2.0', id: 2, method: 'tools/list' });
  assert.equal(list.body.result.tools.length, 3);
  assert.deepEqual(list.body.result.tools.map(x => x.name), TOOLS.map(x => x.name));
  assert.equal((await core.handle({ jsonrpc: '2.0', method: 'notifications/initialized' })).status, 202);
  assert.equal((await core.handle({ jsonrpc: '2.0', id: 3, method: 'ping' })).status, 200);
  assert.equal(reads.length, 0);
});
test('no identity, unauthorized identity and caller-provided identity arguments cannot read project data', async () => {
  const { core, reads } = fixture();
  assert.equal((await core.handle(call('get_current_workflow'))).status, 401);
  assert.equal((await core.handle(call('get_current_workflow'), { userId: 'outsider' })).status, 403);
  assert.equal((await core.handle(call('get_current_workflow', { identity }), identity)).status, 400);
  assert.equal(reads.length, 0);
});
test('actual pinned Git blobs satisfy native bindings and expose real S4 locations with scoped recorded evidence', async () => {
  const { core, reads } = fixture();
  const value = data(await core.handle(call('get_current_workflow'), identity));
  assert.equal(value.source.commit, commit);
  assert.equal(value.next_required_action, 'LIU_REVIEW_LIUXIANSHENG_CONTENT_TRANSFER');
  assert.equal(value.artwork.sha256, 'ddb621ebf7e230279a1358b1b93ab9fcd55705b7e6ca99af8649aa3295ab1ca4');
  assert.equal(value.artwork.figma.node_id, '442:2');
  assert.equal(value.artwork.drive.file_id, '1V_7Vlv4wJj_LZz6nGXlMxZ2hCxhXX5kD');
  assert.equal(value.reference.drive_file_id, '1fG2OQ7IphZfGnH1csu1qZKYCsyAMDOAZ');
  assert.equal(value.acceptance.human, 'PENDING');
  assert.equal(value.acceptance.promotion_allowed, false);
  assert.equal(value.acceptance.cold_pixel_evidence, 'RECORDED_BOUND_RUNTIME_EVIDENCE_NOT_REEXECUTED');
  assert.ok(reads.length >= 10);
  assert.ok(reads.every(x => x.commit === commit));
});
test('concurrent HEAD advancement rejects even a coherent pinned snapshot', async () => {
  const { core } = fixture({ heads: [commit, 'f'.repeat(40)] });
  const response = await core.handle(call('get_current_workflow'), identity);
  assert.equal(response.status, 409);
  assert.match(response.body.error.message, /HEAD_CHANGED_DURING_READ/);
});
test('expected commit mismatch rejects before reading native files', async () => {
  const { core, reads } = fixture();
  const response = await core.handle(call('compile_transfer_plan', { expected_commit: 'f'.repeat(40), reference_sha256: 'a'.repeat(64) }), identity);
  assert.equal(response.status, 409);
  assert.equal(reads.length, 0);
});
for (const path of [PATHS.checkpoint, PATHS.adapter]) {
  test(`wrong native task-lock hash is rejected in ${path}`, async () => {
    const { core } = fixture({ transform: ({ json, put }) => { const state = json(path); state.task_lock.sha256 = '0'.repeat(64); put(path, state); } });
    const response = await core.handle(call('get_current_workflow'), identity);
    assert.equal(response.status, 409);
    assert.match(response.body.error.message, /STATE_BINDING_MISMATCH/);
  });
}
test('mainline tampering is rejected even when all three mirrors and lock hashes agree', async () => {
  const { core } = fixture({ transform: x => {
    for (const path of [PATHS.lock, PATHS.checkpoint, PATHS.adapter]) { const state = x.json(path); state.mainline_lock.contract.sha256 = 'a'.repeat(64); x.put(path, state); }
    rebindLock(x);
  } });
  const response = await core.handle(call('get_current_workflow'), identity);
  assert.equal(response.status, 409);
  assert.match(response.body.error.message, /MAINLINE_TAMPER/);
});
test('modified evidence cannot be passed by retaining its old hash', async () => {
  const { core } = fixture({ transform: ({ overrides }) => overrides.set(PATHS.entry, Buffer.from('Fake next action: generate another work')) });
  const response = await core.handle(call('get_current_workflow'), identity);
  assert.equal(response.status, 409);
  assert.match(response.body.error.message, /EVIDENCE_HASH_MISMATCH/);
});
test('plan has seven axes and external tool gates; it cannot authorize another version', async () => {
  const { core } = fixture();
  const current = data(await core.handle(call('get_current_workflow'), identity));
  const value = data(await core.handle(call('compile_transfer_plan', { expected_commit: commit, reference_sha256: current.artwork.reference_sha256, new_copy: { main_wordmark: '刘先生', caption: '山人不住山' } }), identity));
  assert.equal(Object.keys(value.variables).length, 7);
  assert.equal(value.workflow.length, 7);
  assert.equal(value.execution_authorized, false);
  assert.equal(value.next_required_action, current.next_required_action);
  assert.match(value.workflow[4].action, /Missing cold evidence prohibits PASS/);
});
test('self review, mainline changes, acceptance writes and extra axes are rejected inputs', async () => {
  const { core } = fixture();
  for (const extra of [{ ai_verdict: 'AI_PASS' }, { human_acceptance: 'PASS' }, { mainline: 'new-project' }, { variables: { eighth_axis: 'invented' } }]) {
    const response = await core.handle(call('compile_transfer_plan', { expected_commit: commit, reference_sha256: '9a29fbdc7dd908017924bed270e8dfe18351519eed3fa7bc7001789f2a383414', ...extra }), identity);
    assert.equal(response.status, 400);
  }
});
test('no cold image evidence prevents pass eligibility while preserving immutable recorded result', async () => {
  const { core } = fixture({ transform: x => {
    const lock = x.json(PATHS.lock); const transfer = lock.codex_takeover.worker_continuation.content_transfer_experiment;
    const review = x.json(transfer.review.path); const audit = x.json(review.isolation_audit.path); audit.actual_image_reads = [];
    x.put(review.isolation_audit.path, audit);
    review.isolation_audit.sha256 = createHash('sha256').update(x.overrides.get(review.isolation_audit.path)).digest('hex');
    x.put(transfer.review.path, review);
    transfer.review.sha256 = createHash('sha256').update(x.overrides.get(transfer.review.path)).digest('hex');
    const delivery = x.json(transfer.delivery.path); delivery.independent_review = transfer.review;
    x.put(transfer.delivery.path, delivery); transfer.delivery.sha256 = createHash('sha256').update(x.overrides.get(transfer.delivery.path)).digest('hex');
    x.put(PATHS.lock, lock); rebindLock(x);
  } });
  const value = data(await core.handle(call('get_current_workflow'), identity));
  assert.equal(value.acceptance.cold_pixel_evidence, 'MISSING_OR_INVALID_NO_PASS');
  assert.equal(value.acceptance.recorded_ai_verdict, 'CONTENT_TRANSFER_PASS_WITH_LIMITATIONS');
  assert.equal(value.acceptance.promotion_allowed, false);
});
const feedbackArgs = { expected_commit: commit, artwork_sha256: 'ddb621ebf7e230279a1358b1b93ab9fcd55705b7e6ca99af8649aa3295ab1ca4', idempotency_key: 'test-feedback-001', verdict: 'APPROVE', comment: '认可这张文字迁移稿，后续仍需核对范围。' };
test('human feedback binds actual artwork, reference, commit and actor, without persistence or promotion', async () => {
  const { core } = fixture();
  const first = data(await core.handle(call('prepare_human_feedback', feedbackArgs), identity));
  const second = data(await core.handle(call('prepare_human_feedback', feedbackArgs), identity));
  assert.equal(first.persisted, false);
  assert.equal(first.validated_intake.actor_id, identity.userId);
  assert.equal(first.validated_intake.disposition, 'PENDING_ROOT_RECONCILIATION');
  assert.equal(first.validated_intake.acceptance_write, false);
  assert.equal(first.validated_intake.mainline_write, false);
  assert.equal(first.content_sha256, second.content_sha256);
  assert.equal(data(await core.handle(call('get_current_workflow'), identity)).acceptance.human, 'PENDING');
});
test('feedback for another artwork, invalid verdict and automatic promotion request are rejected', async () => {
  const { core } = fixture();
  for (const extra of [{ artwork_sha256: 'f'.repeat(64) }, { verdict: 'PASS' }, { acceptance_write: true }, { mainline: 'new-goal' }]) {
    const response = await core.handle(call('prepare_human_feedback', { ...feedbackArgs, ...extra }), identity);
    assert.notEqual(response.status, 200);
  }
});
test('invalid JSON-RPC, missing protocol and unknown tools fail cleanly', async () => {
  const { core } = fixture();
  assert.equal((await core.handle([])).status, 400);
  assert.equal((await core.handle({ jsonrpc: '2.0', id: 1, method: 'initialize' })).status, 400);
  assert.equal((await core.handle(call('promote_self_review'), identity)).status, 400);
});
test('runtime-neutral WebCrypto hashes original UTF-8 bytes identically to Node crypto', async () => {
  const input = '刘先生\r\n山野集\n';
  assert.equal(await sha256(input), await hash(input));
  assert.equal(await sha256(new TextEncoder().encode(input)), await hash(input));
});
test('default authorization fails closed without an explicit owner ACL', async () => {
  const core = createCore({ resolveHead: async () => commit, readFile: async () => { throw new Error('Must not read'); } });
  assert.equal((await core.handle(call('get_current_workflow'), identity)).status, 403);
});
test('state stage mismatch prevents dispatching a competing task', async () => {
  const { core } = fixture({ transform: ({ json, put }) => { const cp = json(PATHS.checkpoint); cp.current_stage = 'ANOTHER_STYLE'; put(PATHS.checkpoint, cp); } });
  const response = await core.handle(call('get_current_workflow'), identity);
  assert.equal(response.status, 409);
  assert.match(response.body.error.message, /stage\/status mismatch/);
});
function scopedHumanFixture({ wrongArtwork = false, wrongHash = false, newerArtwork = false, wrongAllocationTarget = false } = {}) {
  return fixture({ transform: x => {
    const feedbackPath = 'evidence/vpd/codex_takeover_20261003/liuxiansheng_content_transfer_20261005/HUMAN_S4_FEEDBACK_20261006.json';
    const allocationPath = 'evidence/vpd/codex_takeover_20261003/liuxiansheng_content_transfer_20261005/TEST_HUMAN_LOCAL_REPAIR_ALLOCATION.json';
    // Synthetic protocol fixture, never a statement attributed to the real human.
    x.put(feedbackPath, { source_kind: 'CURRENT_HUMAN_USER_MESSAGE', user_literal: '合成测试反馈：仅修轮廓和先字连续性。', scope: 'S4_OUTLINE_AND_XIAN_CONTINUITY_ONLY', target_export: { sha256: wrongArtwork ? 'f'.repeat(64) : feedbackArgs.artwork_sha256 }, verdict: 'LOCAL_REPAIR_REQUESTED' });
    const feedbackHash = createHash('sha256').update(x.overrides.get(feedbackPath)).digest('hex');
    x.put(allocationPath, { schema_version: 'vpd-content-transfer-human-local-repair-allocation/v1', target_export: { sha256: wrongAllocationTarget ? 'b'.repeat(64) : (wrongArtwork ? 'f'.repeat(64) : feedbackArgs.artwork_sha256) }, feedback: { path: feedbackPath, sha256: wrongHash ? '0'.repeat(64) : feedbackHash } });
    const lock = x.json(PATHS.lock);
    lock.codex_takeover.worker_continuation.content_transfer_experiment.human_local_repair_allocation = { path: allocationPath, sha256: createHash('sha256').update(x.overrides.get(allocationPath)).digest('hex') };
    if (newerArtwork) {
      const transfer = lock.codex_takeover.worker_continuation.content_transfer_experiment;
      const delivery = x.json(transfer.delivery.path);
      delivery.export = { ...delivery.export, sha256: 'a'.repeat(64) };
      delivery.review_verdict = 'CONTENT_TRANSFER_FAIL';
      transfer.attempts.push({ export: delivery.export });
      x.put(transfer.delivery.path, delivery);
      transfer.delivery.sha256 = createHash('sha256').update(x.overrides.get(transfer.delivery.path)).digest('hex');
    }
    x.put(PATHS.lock, lock); rebindLock(x);
  } });
}
test('bound scoped human repair wording is exposed for creation but excluded from cold reviewer handoff', async () => {
  const { core } = scopedHumanFixture();
  const current = data(await core.handle(call('get_current_workflow'), identity));
  assert.equal(current.latest_human_feedback.verbatim, '合成测试反馈：仅修轮廓和先字连续性。');
  assert.equal(current.latest_human_feedback.artwork_sha256, feedbackArgs.artwork_sha256);
  assert.equal(current.latest_human_feedback.final_human_acceptance, 'PENDING');
  assert.equal(current.latest_human_feedback.independent_review_input, false);
  assert.equal(current.acceptance.historical_ai_pass_is_not_human_acceptance, true);
  const plan = data(await core.handle(call('compile_transfer_plan', { expected_commit: commit, reference_sha256: current.artwork.reference_sha256 }), identity));
  assert.deepEqual(plan.latest_human_feedback, current.latest_human_feedback);
  assert.match(plan.review_handoff_policy, /Never attach this feedback/);
  assert.ok(!plan.prompt.includes(current.latest_human_feedback.verbatim));
  assert.equal(plan.execution_authorized, false);
});
test('scoped human feedback rejects incorrect evidence hash and artwork binding', async () => {
  for (const config of [{ wrongHash: true }, { wrongArtwork: true }, { wrongAllocationTarget: true }]) {
    const { core } = scopedHumanFixture(config);
    const response = await core.handle(call('get_current_workflow'), identity);
    assert.equal(response.status, 409);
    assert.match(response.body.error.message, /EVIDENCE_HASH_MISMATCH|HUMAN_FEEDBACK_ARTWORK_OR_SCOPE_MISMATCH/);
  }
});

test('historical human wording remains bound to S4 and cannot assess a newer artwork', async () => {
  const { core } = scopedHumanFixture({ newerArtwork: true });
  const current = data(await core.handle(call('get_current_workflow'), identity));
  assert.equal(current.artwork.sha256, 'a'.repeat(64));
  assert.equal(current.latest_human_feedback.applies_to_export_sha256, feedbackArgs.artwork_sha256);
  assert.equal(current.latest_human_feedback.current_artwork_assessed_by_this_feedback, false);
  assert.equal(current.acceptance.human, 'PENDING');
  assert.equal(current.acceptance.promotion_allowed, false);
  assert.equal(current.acceptance.cold_pixel_evidence, 'MISSING_OR_INVALID_NO_PASS');
});
test('cold record rejects unverified, wrong model/effort, altered image count and unmatched exact call hashes', async () => {
  const mutations = [
    audit => { audit.verified = false; },
    audit => { audit.actual_model = 'gpt-6-astra'; },
    audit => { audit.actual_reasoning_effort = 'high'; },
    audit => { audit.actual_turn_contexts[0].effort = 'low'; },
    audit => { audit.actual_parent_spawn[0].fork_turns = 'all'; },
    audit => { audit.actual_image_reads.push({ sha256: 'f'.repeat(64) }); },
    audit => { audit.actual_tool_calls.pop(); },
    audit => { audit.actual_tool_calls[0].input_sha256 = 'e'.repeat(64); }
  ];
  for (const mutate of mutations) {
    const { core } = fixture({ transform: x => {
      const lock = x.json(PATHS.lock); const transfer = lock.codex_takeover.worker_continuation.content_transfer_experiment;
      const review = x.json(transfer.review.path); const audit = x.json(review.isolation_audit.path);
      mutate(audit); x.put(review.isolation_audit.path, audit);
      review.isolation_audit.sha256 = createHash('sha256').update(x.overrides.get(review.isolation_audit.path)).digest('hex');
      x.put(transfer.review.path, review); transfer.review.sha256 = createHash('sha256').update(x.overrides.get(transfer.review.path)).digest('hex');
      const delivery = x.json(transfer.delivery.path); delivery.independent_review = transfer.review;
      x.put(transfer.delivery.path, delivery); transfer.delivery.sha256 = createHash('sha256').update(x.overrides.get(transfer.delivery.path)).digest('hex');
      x.put(PATHS.lock, lock); rebindLock(x);
    } });
    const value = data(await core.handle(call('get_current_workflow'), identity));
    assert.equal(value.acceptance.cold_pixel_evidence, 'MISSING_OR_INVALID_NO_PASS');
    assert.equal(value.acceptance.promotion_allowed, false);
  }
});

const requestArgs = { expected_commit: commit, reference_scope: 'user_request', reference_source: 'attachment://current-chat/最长的旅途.png', new_copy: { title: '最长的旅途', subtitle: '写给仍在路上的人' } };

test('compile schema advertises explicit scopes with an optional SHA and required expected commit', () => {
  const schema = TOOLS.find(tool => tool.name === 'compile_transfer_plan').inputSchema;
  assert.deepEqual(schema.properties.reference_scope.enum, ['native_task', 'user_request']);
  assert.equal(schema.properties.reference_scope.default, 'native_task');
  assert.deepEqual(schema.required, ['expected_commit']);
  assert.equal(schema.properties.reference_source.maxLength, 2048);
});

test('valid native calls preserve complete v0.1.1 output and default reference scope', async () => {
  const { core } = fixture();
  const previous = fixture({ factory: stableCore }).core;
  const current = data(await core.handle(call('get_current_workflow'), identity));
  const nativeArgs = { expected_commit: commit, reference_sha256: current.artwork.reference_sha256 };
  for (const rpc of [call('get_current_workflow'), call('compile_transfer_plan', nativeArgs), call('prepare_human_feedback', feedbackArgs)]) {
    assert.deepEqual(await core.handle(rpc, identity), await previous.handle(rpc, identity));
  }
  assert.deepEqual(await core.handle(call('compile_transfer_plan', { ...nativeArgs, reference_scope: 'native_task' }), identity), await core.handle(call('compile_transfer_plan', nativeArgs), identity));
});

test('native scope still rejects a different well-formed reference SHA', async () => {
  const { core } = fixture();
  for (const extra of [{}, { reference_scope: 'native_task' }]) {
    const response = await core.handle(call('compile_transfer_plan', { expected_commit: commit, reference_sha256: 'f'.repeat(64), ...extra }), identity);
    assert.equal(response.status, 409);
    assert.match(response.body.error.message, /Reference SHA is not the currently bound reference/);
  }
});

test('native scope requires a canonical 64-hex reference SHA', async () => {
  const { core, reads } = fixture();
  for (const extra of [{}, { reference_sha256: 'UNKNOWN' }, { reference_sha256: 'g'.repeat(64) }, { reference_sha256: 'a'.repeat(63) }, { reference_sha256: 'a'.repeat(65) }]) {
    const response = await core.handle(call('compile_transfer_plan', { expected_commit: commit, ...extra }), identity);
    assert.equal(response.status, 400);
    assert.match(response.body.error.message, /reference_sha256/);
  }
  assert.equal(reads.length, 0);
});

test('user-request reference accepts a different SHA as caller-provided and unverified', async () => {
  const { core } = fixture();
  const current = data(await core.handle(call('get_current_workflow'), identity));
  const value = data(await core.handle(call('compile_transfer_plan', { ...requestArgs, reference_sha256: 'f'.repeat(64) }), identity));
  assert.notEqual(value.reference_sha256, current.artwork.reference_sha256);
  assert.equal(value.status, 'DRAFT_USER_REQUEST');
  assert.equal(value.reference_scope, 'user_request');
  assert.equal(value.reference_source, requestArgs.reference_source);
  assert.equal(value.reference_sha256, 'f'.repeat(64));
  assert.deepEqual(value.reference_verification, { status: 'NOT_PERFORMED', sha256: 'f'.repeat(64), sha256_provenance: 'CALLER_PROVIDED_NOT_VERIFIED', pixels_viewed: false });
  assert.deepEqual(value.proposed_copy, requestArgs.new_copy);
  assert.deepEqual(value.native_context.source, current.source);
  assert.equal(value.native_context.next_required_action, current.next_required_action);
  assert.equal(value.native_context.mainline_locked, true);
  assert.equal(value.native_context.native_reference_rebound, false);
  assert.equal(value.mainline_write, false);
  assert.equal(value.business_state_write, false);
  assert.equal(value.execution_authorized, false);
  assert.equal(value.artwork_generated, false);
  assert.equal(value.independent_review_performed, false);
  assert.match(value.execution_authority, /existing user authorization/);
  assert.match(value.execution_authority, /do not ask for repeated approval solely/);
});

test('user-request reference can omit SHA without inheriting native identity or visual defaults', async () => {
  const { core } = fixture();
  const value = data(await core.handle(call('compile_transfer_plan', requestArgs), identity));
  assert.equal(value.reference_sha256, 'UNKNOWN');
  assert.deepEqual(value.reference_verification, { status: 'NOT_PERFORMED', sha256: 'UNKNOWN', sha256_provenance: 'UNKNOWN', pixels_viewed: false });
  assert.equal(value.prompt_status, 'DRAFT_PENDING_REFERENCE_PIXELS');
  assert.equal(Object.keys(value.variables).length, 7);
  assert.equal(value.workflow.length, 7);
  assert.ok(Object.values(value.variables).every(value => /actual user-request reference pixels/.test(value)));
  assert.doesNotMatch(value.prompt, /Shanyeji|山野集|forest green|cream main|orange curve|960|1280|central custom wordmark|photography remains paused/i);
  assert.match(value.workflow[0].action, /recompute SHA256 and view actual pixels/);
  assert.match(value.workflow[4].action, /Missing cold evidence prohibits PASS/);
});

test('user-request accepts only the seven bounded explicit axes', async () => {
  const { core } = fixture();
  const variables = { canvas: 'Use the explicit user dimensions 1200 × 900 after reference verification.', color_logic: 'Inspect the attached image before choosing colors.' };
  const value = data(await core.handle(call('compile_transfer_plan', { ...requestArgs, variables }), identity));
  assert.equal(value.variables.canvas, variables.canvas);
  assert.equal(value.variables.color_logic, variables.color_logic);
  for (const variables of [{ eighth_axis: 'extra' }, { canvas: 'x'.repeat(601) }, { canvas: ' ' }, { canvas: [] }, { canvas: {} }]) {
    assert.equal((await core.handle(call('compile_transfer_plan', { ...requestArgs, variables }), identity)).status, 400);
  }
});

test('user-request requires a bounded source locator and explicit valid proposed copy', async () => {
  const { core, reads } = fixture();
  const bad = [
    { ...requestArgs, reference_source: undefined }, { ...requestArgs, reference_source: '' }, { ...requestArgs, reference_source: ' ' },
    { ...requestArgs, reference_source: 'x'.repeat(2049) }, { ...requestArgs, reference_source: 'attachment://line\nother' },
    { ...requestArgs, new_copy: undefined }, { ...requestArgs, new_copy: {} }, { ...requestArgs, new_copy: { title: '' } },
    { ...requestArgs, new_copy: { title: ' ' } }, { ...requestArgs, new_copy: { title: 'x'.repeat(1001) } },
    { ...requestArgs, new_copy: Object.fromEntries(Array.from({ length: 21 }, (_, i) => [`copy_${i}`, 'value'])) }
  ];
  for (const args of bad) {
    // Serialize the RPC as a real transport does, so undefined fields are absent.
    assert.equal((await core.handle(JSON.parse(JSON.stringify(call('compile_transfer_plan', args))), identity)).status, 400, JSON.stringify(args));
  }
  assert.equal(reads.length, 0);
});

test('user-request rejects malformed SHA, scopes and object/array substitutions before reads', async () => {
  const { core, reads } = fixture();
  const bad = [
    { ...requestArgs, reference_sha256: 'UNKNOWN' }, { ...requestArgs, reference_sha256: 'z'.repeat(64) },
    { ...requestArgs, reference_sha256: 'a'.repeat(63) }, { ...requestArgs, reference_sha256: 'a'.repeat(65) },
    { ...requestArgs, reference_sha256: null }, { ...requestArgs, reference_scope: 'replace_native' },
    { ...requestArgs, reference_source: [] }, { ...requestArgs, reference_source: {} },
    { ...requestArgs, new_copy: [] }, { ...requestArgs, new_copy: null }, { ...requestArgs, new_copy: { title: [] } },
    { ...requestArgs, new_copy: { title: {} } }, { ...requestArgs, variables: [] }, { ...requestArgs, variables: null },
    [], null
  ];
  for (const args of bad) assert.equal((await core.handle(call('compile_transfer_plan', args), identity)).status, 400, JSON.stringify(args));
  assert.equal(reads.length, 0);
});

test('user-request never returns native artwork feedback, copy, review results or historical experience', async () => {
  const { core } = scopedHumanFixture();
  const before = data(await core.handle(call('get_current_workflow'), identity));
  const value = data(await core.handle(call('compile_transfer_plan', requestArgs), identity));
  for (const key of ['latest_human_feedback', 'experience', 'acceptance', 'artwork', 'entry', 'evidence']) assert.equal(Object.hasOwn(value, key), false);
  const serialized = JSON.stringify(value);
  assert.ok(!serialized.includes(before.latest_human_feedback.verbatim));
  assert.ok(!serialized.includes(before.artwork.sha256));
  assert.ok(!serialized.includes(before.artwork.reference_sha256));
  assert.ok(!serialized.includes(before.acceptance.recorded_ai_verdict));
  assert.doesNotMatch(serialized, /合成测试反馈|山人不住山|刘先生|CONTENT_TRANSFER_PASS_WITH_LIMITATIONS/);
  assert.match(value.review_handoff_policy, /Do not attach native_context/);
  assert.deepEqual(data(await core.handle(call('get_current_workflow'), identity)), before);
});

test('user-request still requires identity and owner ACL before native reads', async () => {
  const { core, reads } = fixture();
  assert.equal((await core.handle(call('compile_transfer_plan', requestArgs))).status, 401);
  assert.equal((await core.handle(call('compile_transfer_plan', requestArgs), { userId: 'outsider' })).status, 403);
  assert.equal((await core.handle(call('compile_transfer_plan', { ...requestArgs, identity }), identity)).status, 400);
  assert.equal(reads.length, 0);
});

test('user-request rejects stale expected HEAD before reads and advancement before response', async () => {
  const stale = fixture();
  const response = await stale.core.handle(call('compile_transfer_plan', { ...requestArgs, expected_commit: 'f'.repeat(40) }), identity);
  assert.equal(response.status, 409);
  assert.match(response.body.error.message, /HEAD_CHANGED/);
  assert.equal(stale.reads.length, 0);
  const advancing = fixture({ heads: [commit, 'f'.repeat(40)] });
  const changed = await advancing.core.handle(call('compile_transfer_plan', requestArgs), identity);
  assert.equal(changed.status, 409);
  assert.match(changed.body.error.message, /HEAD_CHANGED_DURING_READ/);
  assert.equal(Object.hasOwn(changed.body, 'result'), false);
});

test('user-request cannot bypass native mirror or bound-evidence integrity checks', async () => {
  for (const transform of [
    ({ json, put }) => { const cp = json(PATHS.checkpoint); cp.task_lock.sha256 = '0'.repeat(64); put(PATHS.checkpoint, cp); },
    ({ overrides }) => overrides.set(PATHS.entry, Buffer.from('Synthetic altered entry')),
    x => { for (const path of [PATHS.lock, PATHS.checkpoint, PATHS.adapter]) { const state = x.json(path); state.mainline_lock.contract.sha256 = 'a'.repeat(64); x.put(path, state); } rebindLock(x); }
  ]) {
    const { core } = fixture({ transform });
    const response = await core.handle(call('compile_transfer_plan', requestArgs), identity);
    assert.equal(response.status, 409);
    assert.match(response.body.error.message, /STATE_BINDING_MISMATCH|EVIDENCE_HASH_MISMATCH|MAINLINE_TAMPER/);
  }
});

const lockedArgs={...requestArgs,operation_mode:'structure_locked_edit',reference_source:'sediment://file_real_locator',new_copy:{main_wordmark:'地图以外',english:'for liuxiansheng',vertical_copy:'不是所有远方，都写在地图上',footer_copy:'离开既定路线，去看未知远方'},editable_regions:[{id:'title',role:'main_title_text',x:1,y:1,width:2,height:2,mask_source:'synthetic-mask',mask_sha256:'c'.repeat(64)}]};
const binding={context_id:'synthetic-current-context',attachment_id:'synthetic-attachment',reference_source:lockedArgs.reference_source,sha256:'a'.repeat(64),edit_target:'/synthetic/reference.png',width:4,height:4,pixels_readable:true,pixels_viewed:true,attached_in_current_context:true};
test('A locator only structure lock is BLOCKED STOP without any generation prompt',async()=>{
 const {core}=fixture();const v=data(await core.handle(call('compile_transfer_plan',lockedArgs),identity));
 assert.equal(v.status,'BLOCKED');assert.equal(v.action,'STOP');assert.equal(Object.hasOwn(v,'prompt'),false);
 for(const k of ['reference_pixels_required','current_context_reference_required'])assert.equal(v.execution_contract[k],true);
 for(const k of ['text_to_image_allowed','fallback_allowed','reconstruct_reference_from_description_allowed'])assert.equal(v.execution_contract[k],false);
 for(const k of ['on_reference_unavailable','on_reference_not_bound'])assert.equal(v.execution_contract[k],'STOP');
 assert.equal(v.execution_contract.image_operation,'EDIT_EXISTING_IMAGE_ONLY');assert.equal(v.hard_preserve.length,12);assert.ok(v.blocked_until.length);
});
test('B valid caller pixel binding yields edit-only contract but cannot manufacture server pixel verification',async()=>{
 const {core}=fixture();const v=data(await core.handle(call('compile_transfer_plan',{...lockedArgs,current_reference_binding:binding}),identity));
 assert.equal(v.action,'VERIFY_BINDING_THEN_MASKED_EDIT_AND_COMPOSITE');assert.equal(v.execution_contract.image_operation,'EDIT_EXISTING_IMAGE_ONLY');
 assert.equal(v.execution_contract.binding_verified_by_server,false);assert.ok(v.blocked_until.length);assert.equal(Object.hasOwn(v,'prompt'),false);
 assert.deepEqual(v.edit_directives.replace_text_only,lockedArgs.new_copy);
});
test('false, incomplete, extra, unread, other locator and hash-mismatched bindings STOP',async()=>{
 const {core}=fixture();for(const b of [{},{...binding,pixels_readable:false},{...binding,pixels_viewed:false},{...binding,attached_in_current_context:false},{...binding,reference_source:'other'},{...binding,sha256:'invalid'},{...binding,extra:true},{...binding,context_id:''}]){
  const v=data(await core.handle(call('compile_transfer_plan',{...lockedArgs,current_reference_binding:b}),identity));assert.equal(v.action,'STOP');assert.equal(Object.hasOwn(v,'prompt'),false);
 }
 const v=data(await core.handle(call('compile_transfer_plan',{...lockedArgs,reference_sha256:'b'.repeat(64),current_reference_binding:binding}),identity));assert.equal(v.action,'STOP');
});
test('structure preservation intent forces routing even when creative mode was requested',async()=>{
 const {core}=fixture();for(const user_intent of ['不改变结构','只改文字','保留原图','严格参考原结构','别改变结构']){
 const v=data(await core.handle(call('compile_transfer_plan',{...requestArgs,operation_mode:'creative_transfer',user_intent}),identity));assert.equal(v.operation_mode,'structure_locked_edit');assert.equal(v.action,'STOP');}
 const v=data(await core.handle(call('compile_transfer_plan',{...requestArgs,variables:{attention_geometry:'严格保持原始版式，只改文字'}}),identity));assert.equal(v.action,'STOP');
});
test('C native read plan and feedback remain byte equivalent to preserved 0.1.2',async()=>{
 const {createCore:baseline}=await import('./baseline-core-v0.1.2.mjs');const {core}=fixture();const old=fixture({factory:baseline}).core;
 const v=data(await core.handle(call('get_current_workflow'),identity));
 for(const rpc of [call('get_current_workflow'),call('compile_transfer_plan',{expected_commit:commit,reference_sha256:v.artwork.reference_sha256}),call('prepare_human_feedback',feedbackArgs)])assert.deepEqual(await core.handle(rpc,identity),await old.handle(rpc,identity));
});
test('D creative request keeps baseline creative draft and seven-axis prompt',async()=>{
 const {createCore:baseline}=await import('./baseline-core-v0.1.2.mjs');const {core}=fixture();const old=fixture({factory:baseline}).core;
 const args={...requestArgs,user_intent:'参考风格创作一张新的旅行海报，构图自由'};const v=data(await core.handle(call('compile_transfer_plan',args),identity));
 assert.equal(v.status,'DRAFT_USER_REQUEST');assert.ok(v.prompt);assert.equal(Object.hasOwn(v,'execution_contract'),false);
 assert.deepEqual(v,data(await old.handle(call('compile_transfer_plan',requestArgs),identity)));
});
test('actual cooperating image invocation requires same byte hash context and target; no fallback on editor failure',async()=>{
 const {executeStructureLockedEdit}=await import('./execution-gate.mjs');const {core}=fixture();const bytes=new TextEncoder().encode('SYNTHETIC_BYTES_NOT_REAL_PIXEL_ACCEPTANCE');
 const b={...binding,sha256:await sha256(bytes)};const plan=data(await core.handle(call('compile_transfer_plan',{...lockedArgs,current_reference_binding:b}),identity));
 const context={...b};let calls=0;const invokeEdit=async input=>{calls++;assert.equal(input.image_operation,'EDIT_EXISTING_IMAGE_ONLY');assert.equal(input.edit_target,b.edit_target);assert.equal(input.text_to_image_allowed,false);return 'synthetic-editor-result';};
 for(const bad of [{referenceBytes:null,context},{referenceBytes:bytes,context:{...context,context_id:'other'}},{referenceBytes:bytes,context:{...context,edit_target:'other'}},{referenceBytes:new Uint8Array([0]),context},{referenceBytes:bytes,context:{...context,pixels_viewed:false}}])await assert.rejects(()=>executeStructureLockedEdit({plan,...bad,invokeEdit}),/STOP/);
 assert.equal(calls,0);const guide=await executeStructureLockedEdit({plan,referenceBytes:bytes,context,invokeEdit});assert.equal(guide.role,'GUIDE_ONLY');assert.equal(guide.material,'synthetic-editor-result');assert.equal(guide.final_eligible,false);assert.equal(calls,1);
 await assert.rejects(()=>executeStructureLockedEdit({plan,referenceBytes:bytes,context,invokeEdit:async()=>{calls++;throw Error('synthetic editor failure');}}),/synthetic editor failure/);assert.equal(calls,2);
});

test('0.1.4 exact finalization contract is hard, masks are explicit and whole-canvas generation cannot be final',async()=>{
 const {core}=fixture();const v=data(await core.handle(call('compile_transfer_plan',{...lockedArgs,current_reference_binding:binding}),identity));const c=v.execution_contract;
 assert.equal(c.final_canvas_policy,'EXACT_REFERENCE_DIMENSIONS');assert.equal(c.finalization_mode,'MASKED_LOCAL_EDIT_OR_DETERMINISTIC_COMPOSITE');
 assert.equal(c.whole_canvas_generative_edit_as_final,false);assert.equal(c.outside_edit_regions_policy,'BIT_IDENTICAL');assert.equal(c.generative_output_role,'GUIDE_ONLY');
 assert.equal(c.on_exact_composite_unavailable,'STOP');assert.equal(c.exact_composite_requirement,'DETERMINISTIC_COMPOSITE_REQUIRED');
 assert.deepEqual(c.reference_dimensions,{width:4,height:4});assert.deepEqual(c.editable_regions,lockedArgs.editable_regions);assert.equal(c.postconditions.outside_edit_masks_changed_pixels,0);
 assert.equal(Object.hasOwn(v,'prompt'),false);
});
test('binding alone cannot bypass missing exact dimensions or missing edit masks',async()=>{
 const {core}=fixture();const noDims={...binding};delete noDims.width;delete noDims.height;
 for(const extra of [{current_reference_binding:noDims},{current_reference_binding:binding,editable_regions:undefined},{current_reference_binding:binding,editable_regions:[]}]){
 const args={...lockedArgs,...extra};if(args.editable_regions===undefined)delete args.editable_regions;
 const v=data(await core.handle(call('compile_transfer_plan',args),identity));assert.equal(v.action,'STOP');assert.equal(v.status,'BLOCKED');assert.ok(v.blocked_until.length);
 }
});
test('whole-canvas arbitrary-role out-of-bounds and unbound cleanup mask declarations STOP',async()=>{
 const {core}=fixture();const region=lockedArgs.editable_regions[0];
 for(const r of [{...region,x:0,y:0,width:4,height:4},{...region,role:'photo'},{...region,x:3,width:2},{...region,mask_sha256:'fake'},{...region,role:'minimal_text_cleanup'},{...region,x:1.5}]){
 const v=data(await core.handle(call('compile_transfer_plan',{...lockedArgs,current_reference_binding:binding,editable_regions:[r]}),identity));assert.equal(v.action,'STOP');
 }
});
test('0.1.3 native and creative byte output and feedback persistence contract remain unchanged',async()=>{
 const {createCore:baseline}=await import('./baseline-core-v0.1.3.mjs');const {core}=fixture();const old=fixture({factory:baseline}).core;
 const v=data(await core.handle(call('get_current_workflow'),identity));
 for(const rpc of [call('get_current_workflow'),call('compile_transfer_plan',{expected_commit:commit,reference_sha256:v.artwork.reference_sha256}),call('prepare_human_feedback',feedbackArgs),call('compile_transfer_plan',requestArgs)])assert.deepEqual(await core.handle(rpc,identity),await old.handle(rpc,identity));
});
