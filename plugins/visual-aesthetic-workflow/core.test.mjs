import test from 'node:test';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';
import { createCore, SOURCE, PATHS, TOOLS, sha256 } from './core.mjs';

const cwd = fileURLToPath(new URL('../../', import.meta.url));
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
function fixture({ transform, heads, authorized = true } = {}) {
  let headCalls = 0;
  const reads = [];
  const overrides = new Map();
  const json = path => JSON.parse(overrides.get(path) ?? gitBytes(path).toString('utf8'));
  const put = (path, value) => overrides.set(path, Buffer.from(JSON.stringify(value)));
  if (transform) transform({ json, put, overrides });
  const core = createCore({
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
  assert.equal(init.body.result.serverInfo.version, '0.1.0');
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
