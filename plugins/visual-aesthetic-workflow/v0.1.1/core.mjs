// Stateless, runtime-neutral MCP core. No storage, rendering, or business-state writes.
export const SOURCE = Object.freeze({ repository: 'vubaoha034-hash/shenmei', branch: 'visual-program-distillation-v2-photography-design-20260814' });
export const PATHS = Object.freeze({ lock: 'continuity/vpd/CURRENT_TASK_LOCK.json', checkpoint: 'continuity/vpd/LATEST_CHECKPOINT.json', adapter: 'PROJECT_CONTROL_ADAPTER.json', entry: 'continuity/vpd/codex_takeover_20261003/WORKER_CURRENT_REUSE.md' });
const MAINLINE = Object.freeze({ id: 'VPD-FULL-POSTER-REFERENCE-DISTILLATION-MAINLINE-20261001', plan: '7c3e375279f08efd53900e9fb5434bfa1fdbb8e356ec80f74014e21340c68aed', contract: '6e7249fc74c93e82c5fd3d3bf9f0cf23ef4e5282ce611af674a648f8c3d764e9' });
const HEX64 = /^[a-f0-9]{64}$/;
const HEX40 = /^[a-f0-9]{40}$/;
export const PROTOCOL_VERSIONS = Object.freeze(['2024-11-05', '2025-03-26', '2025-06-18']);
export const negotiatedProtocol = requested => PROTOCOL_VERSIONS.includes(requested) ? requested : '2025-06-18';
export function validateRpcRequest(request) {
  if (!request || typeof request !== 'object' || Array.isArray(request) || request.jsonrpc !== '2.0' || typeof request.method !== 'string' || !request.method.length) return 'Invalid JSON-RPC request';
  if (request.params !== undefined && (!request.params || typeof request.params !== 'object' || Array.isArray(request.params))) return 'JSON-RPC params must be an object';
  if (request.method === 'notifications/initialized') { if (Object.hasOwn(request, 'id')) return 'Initialized notification cannot have an id'; return null; }
  if (!Object.hasOwn(request, 'id') || !((typeof request.id === 'string') || (typeof request.id === 'number' && Number.isInteger(request.id)))) return 'JSON-RPC request id must be a string or integer';
  if (request.method === 'tools/call') {
    if (typeof request.params?.name !== 'string' || !request.params.name.length) return 'Tool name required';
    const args = request.params.arguments;
    if (args !== undefined && (!args || typeof args !== 'object' || Array.isArray(args))) return 'Tool arguments must be an object';
  }
  return null;
}
const objectSchema = (properties = {}, required = []) => ({ type: 'object', properties, required, additionalProperties: false });
const string = { type: 'string', minLength: 1 };
export const TOOLS = Object.freeze([
  { name: 'get_current_workflow', description: 'Read the actual latest authoritative GitHub commit, bound native state and current artwork locations. Does not retrieve pixels or manufacture acceptance.', inputSchema: objectSchema(), annotations: { readOnlyHint: true, openWorldHint: true } },
  { name: 'compile_transfer_plan', description: 'Prepare a compact reference → copy → image → Figma → isolated pixel review → repair → Drive/native handoff. Planning only; current native authorization still controls execution.', inputSchema: objectSchema({ expected_commit: string, reference_sha256: string, new_copy: { type: 'object', additionalProperties: { type: 'string' } }, variables: { type: 'object', additionalProperties: { type: 'string' } } }, ['expected_commit', 'reference_sha256']), annotations: { readOnlyHint: true, openWorldHint: true } },
  { name: 'prepare_human_feedback', description: 'Validate an artwork-bound human feedback intake for host append-only persistence and Root reconciliation. Never changes mainline, verdicts or production rules.', inputSchema: objectSchema({ expected_commit: string, artwork_sha256: string, idempotency_key: string, verdict: { type: 'string', enum: ['APPROVE', 'REJECT', 'COMMENT'] }, comment: { type: 'string', minLength: 1, maxLength: 8000 } }, ['expected_commit', 'artwork_sha256', 'idempotency_key', 'verdict', 'comment']), annotations: { readOnlyHint: true, openWorldHint: true } }
]);
class CoreError extends Error { constructor(message, code = -32010, status = 409) { super(message); this.code = code; this.status = status; } }
const requireThat = (test, message, code, status) => { if (!test) throw new CoreError(message, code, status); };
const canonical = value => JSON.stringify(value, (_k, v) => v && typeof v === 'object' && !Array.isArray(v) ? Object.fromEntries(Object.entries(v).sort(([a], [b]) => a.localeCompare(b))) : v);
export async function sha256(bytes) {
  const input = typeof bytes === 'string' ? new TextEncoder().encode(bytes) : bytes;
  return [...new Uint8Array(await globalThis.crypto.subtle.digest('SHA-256', input))].map(b => b.toString(16).padStart(2, '0')).join('');
}
function safePath(path) { requireThat(typeof path === 'string' && !path.startsWith('/') && !path.includes('\\') && !path.split('/').some(x => x === '..' || x === '.' || !x) && !path.includes(':'), 'Invalid repository evidence path'); return path; }
function strictArgs(args, tool) {
  requireThat(args && typeof args === 'object' && !Array.isArray(args), 'Arguments must be an object', -32602, 400);
  const schema = tool.inputSchema;
  for (const key of Object.keys(args)) requireThat(Object.hasOwn(schema.properties, key), `Unsupported argument: ${key}`, -32602, 400);
  for (const key of schema.required) requireThat(Object.hasOwn(args, key), `Missing argument: ${key}`, -32602, 400);
  for (const [key, value] of Object.entries(args)) {
    const field = schema.properties[key];
    requireThat(typeof value === field.type && value !== null && !Array.isArray(value), `Invalid argument: ${key}`, -32602, 400);
    if (field.type === 'string') requireThat(value.length >= (field.minLength ?? 0) && value.length <= (field.maxLength ?? 1000) && (!field.enum || field.enum.includes(value)), `Invalid argument: ${key}`, -32602, 400);
  }
}
function recordedColdEvidence(review, audit, delivery, manifest) {
  const reads = audit?.actual_image_reads;
  const expected = [delivery.reference_sha256, delivery.export.sha256];
  return Boolean(review?.reviewer_thread_id && review.reviewer_thread_id === audit?.reviewer_thread_id && audit.verified === true && audit.actual_model === 'gpt-6.1-sol' && audit.actual_reasoning_effort === 'max' && audit.fork_turns === 'none' && audit.history_inherited === false && audit.parent_spawn_verified === true && audit.tool_scope_violations?.length === 0 && HEX64.test(audit.runtime_file_sha256) && audit.pixels_seen === 2 && reads?.length === 2 && expected.every(hash => reads.some(x => x.sha256 === hash)) && audit.actual_tool_calls?.length === 2 && audit.actual_tool_calls.every(x => typeof x.call_id === 'string' && HEX64.test(x.input_sha256)) && new Set(audit.actual_tool_calls.map(x => x.call_id)).size === 2 && audit.actual_turn_contexts?.length > 0 && audit.actual_turn_contexts.every(x => x.model === 'gpt-6.1-sol' && (x.effort ?? x.reasoning_effort) === 'max') && audit.actual_parent_spawn?.length > 0 && audit.actual_parent_spawn.every(x => x.fork_turns === 'none' && x.model === 'gpt-6.1-sol' && x.reasoning_effort === 'max') && audit.reference_sha256 === expected[0] && audit.study_export_sha256 === expected[1] && manifest?.root_read_actual_call_bodies === true && manifest.reference_sha256 === expected[0] && manifest.study_export_sha256 === expected[1] && manifest.reviewer_thread_id === audit.reviewer_thread_id && manifest.calls?.length === 2 && audit.actual_tool_calls.every(call => manifest.calls.some(x => x.call_id === call.call_id && x.name === call.name && x.input_sha256 === call.input_sha256)));
}
export function createCore({ resolveHead, readFile, authorize = async () => false, hash = sha256, now = () => new Date().toISOString() }) {
  requireThat(typeof resolveHead === 'function' && typeof readFile === 'function', 'Missing repository adapters', -32603, 500);
  async function head() { const commit = await resolveHead(SOURCE); requireThat(HEX40.test(commit), 'Repository adapter did not return an actual Git commit SHA'); return commit; }
  async function snapshot(expectedCommit) {
    const commit = await head();
    if (expectedCommit !== undefined) requireThat(expectedCommit === commit, 'HEAD_CHANGED: reload current workflow');
    const cache = new Map();
    async function raw(path) { safePath(path); if (!cache.has(path)) cache.set(path, Promise.resolve(readFile({ ...SOURCE, commit, path }))); const bytes = await cache.get(path); requireThat(typeof bytes === 'string' || bytes instanceof Uint8Array, 'Repository adapter must return exact UTF-8 bytes'); return bytes; }
    async function json(path) { return JSON.parse(typeof await raw(path) === 'string' ? await raw(path) : new TextDecoder('utf-8', { fatal: true }).decode(await raw(path))); }
    async function bound(ref, parse = true) { requireThat(ref && HEX64.test(ref.sha256), 'Missing bound evidence hash'); requireThat(await hash(await raw(ref.path)) === ref.sha256, `EVIDENCE_HASH_MISMATCH: ${ref.path}`); return parse ? json(ref.path) : (typeof await raw(ref.path) === 'string' ? await raw(ref.path) : new TextDecoder().decode(await raw(ref.path))); }
    const [lock, checkpoint, adapter] = await Promise.all([json(PATHS.lock), json(PATHS.checkpoint), json(PATHS.adapter)]);
    const lockHash = await hash(await raw(PATHS.lock));
    for (const state of [checkpoint, adapter]) requireThat(state.task_lock?.path === PATHS.lock && state.task_lock.sha256 === lockHash && state.task_lock.revision === lock.revision, 'STATE_BINDING_MISMATCH: native lock hash/revision');
    requireThat(lock.repository === SOURCE.repository && lock.branch === SOURCE.branch && adapter.repository === SOURCE.repository && adapter.canonical_branch === SOURCE.branch, 'Repository identity mismatch');
    requireThat(lock.project_id === checkpoint.project_id && lock.project_id === adapter.project_id && checkpoint.active_task_ids?.includes(lock.current_task_id) && lock.codex_takeover?.task_id === lock.current_task_id, 'Native task identity mismatch');
    requireThat(checkpoint.current_stage === lock.current_stage && adapter.current_mainline?.task_id === lock.current_task_id && adapter.current_mainline.current_visual_unit === lock.current_stage && checkpoint.status === lock.status && adapter.current_mainline.status === lock.status, 'Native stage/status mismatch');
    requireThat(checkpoint.next_required_action === lock.next_required_action && lock.codex_takeover.next_required_action === lock.next_required_action, 'Native next-action mismatch');
    requireThat(canonical(lock.mainline_lock) === canonical(checkpoint.mainline_lock) && canonical(lock.mainline_lock) === canonical(adapter.mainline_lock), 'MAINLINE_TAMPER: three-file mainline mismatch');
    const mainline = lock.mainline_lock;
    requireThat(mainline?.locked === true && mainline.id === MAINLINE.id && mainline.plan?.sha256 === MAINLINE.plan && mainline.contract?.sha256 === MAINLINE.contract, 'MAINLINE_TAMPER: locked policy changed; requires explicit implementation revision');
    await Promise.all([bound(mainline.plan, false), bound(mainline.contract), bound(mainline.authority)]);
    requireThat(canonical(lock.workflow?.document) === canonical(checkpoint.workflow) && adapter.workflow?.path === checkpoint.workflow?.path && adapter.workflow?.sha256 === checkpoint.workflow?.sha256, 'Native roadmap binding mismatch');
    await bound(checkpoint.workflow, false);
    const entryRef = adapter.workflow?.current_bounded_delivery_entry;
    requireThat([PATHS.entry, 'continuity/vpd/codex_takeover_20261003/S7_FINAL_REUSE.md'].includes(entryRef?.path) && canonical(entryRef) === canonical(lock.codex_takeover.reuse_entry), 'Current reuse entry mismatch');
    const entry = await bound(entryRef, false);
    const transfer = lock.codex_takeover.worker_continuation?.content_transfer_experiment;
    requireThat(transfer?.delivery && transfer.copy_manifest && transfer.review, 'Unsupported current stage: no native content-transfer delivery');
    const [delivery, copy, review, referenceIdentity] = await Promise.all([bound(transfer.delivery), bound(transfer.copy_manifest), bound(transfer.review), bound(lock.codex_takeover.worker_continuation.reference_identity_clarification)]);
    requireThat(HEX64.test(delivery.export?.sha256) && HEX64.test(delivery.reference_sha256) && canonical(delivery.copy_manifest) === canonical(transfer.copy_manifest) && canonical(delivery.independent_review) === canonical(transfer.review), 'Artwork/copy/review binding mismatch');
    requireThat(transfer.attempts?.some(x => x.export?.sha256 === delivery.export.sha256), 'Artwork not bound to native attempt history');
    requireThat(referenceIdentity.correct_reference?.sha256 === delivery.reference_sha256, 'Current reference identity mismatch');
    const audit = review.isolation_audit ? await bound(review.isolation_audit) : null;
    const callManifest = audit?.reviewed_call_manifest ? await bound(audit.reviewed_call_manifest) : null;
    const cold = recordedColdEvidence(review, audit, delivery, callManifest);
    let latestHumanFeedback = null;
    if (transfer.human_local_repair_allocation) {
      const allocation = await bound(transfer.human_local_repair_allocation);
      requireThat((allocation.schema_version ?? allocation.schema) === 'vpd-content-transfer-human-local-repair-allocation/v1', 'Unsupported human local-repair allocation schema');
      const feedback = await bound(allocation.feedback);
      requireThat(feedback.scope === 'S4_OUTLINE_AND_XIAN_CONTINUITY_ONLY' && HEX64.test(feedback.target_export?.sha256) && allocation.target_export?.sha256 === feedback.target_export.sha256 && transfer.attempts?.some(a => a.export?.sha256 === feedback.target_export.sha256), 'HUMAN_FEEDBACK_ARTWORK_OR_SCOPE_MISMATCH');
      requireThat((feedback.source_kind ?? feedback.source?.kind) === 'CURRENT_HUMAN_USER_MESSAGE' && feedback.verdict === 'LOCAL_REPAIR_REQUESTED', 'Human local-repair feedback identity mismatch');
      const verbatim = feedback.user_literal ?? feedback.verbatim ?? feedback.source?.verbatim;
      requireThat(typeof verbatim === 'string' && verbatim.trim().length > 0, 'Human feedback original wording missing');
      latestHumanFeedback = { allocation: transfer.human_local_repair_allocation, feedback: allocation.feedback, user_literal: verbatim, verbatim, artwork_sha256: feedback.target_export.sha256, applies_to_export_sha256: feedback.target_export.sha256, current_artwork_assessed_by_this_feedback: feedback.target_export.sha256 === delivery.export.sha256, scope: feedback.scope, verdict: feedback.verdict, source_kind: 'CURRENT_HUMAN_USER_MESSAGE', final_human_acceptance: 'PENDING', historical_ai_pass_is_not_human_acceptance: true, independent_review_input: false, original_record: feedback };
    }
    return { commit, lockHash, lock, checkpoint, adapter, entryRef, entry, transfer, delivery, copy, review, latestHumanFeedback, reference: referenceIdentity.correct_reference, audit, cold, bound, stable: async () => requireThat(await head() === commit, 'HEAD_CHANGED_DURING_READ: retry on latest commit') };
  }
  function baseCurrent(s) {
    return { source: { ...SOURCE, commit: s.commit, native_lock_sha256: s.lockHash, lock_revision: s.lock.revision, checkpoint_sequence: s.checkpoint.sequence }, task_id: s.lock.current_task_id, stage: s.lock.current_stage, next_required_action: s.lock.next_required_action, entry: { path: s.entryRef.path, text: s.entry }, reference: s.reference, artwork: { ...s.delivery.export, drive: s.delivery.drive, figma: s.delivery.figma, reference_sha256: s.delivery.reference_sha256, copy: s.copy }, acceptance: { recorded_ai_verdict: s.delivery.review_verdict, cold_pixel_evidence: s.cold ? 'RECORDED_BOUND_RUNTIME_EVIDENCE_NOT_REEXECUTED' : 'MISSING_OR_INVALID_NO_PASS', human: s.transfer.human_acceptance, whole_visual_system_complete: false, promotion_allowed: false }, evidence: { delivery: s.transfer.delivery, review: s.transfer.review, isolation: s.review.isolation_audit ?? null }, limits: s.delivery.limits ?? [], pixel_requirements: ['Retrieve reference and current complete artwork original bytes from connected Drive; recompute SHA256 before viewing.', 'View full-resolution reference and artwork in an independent context without creator history or human verdict leakage.', 'A repository record, URL, thumbnail, code check, or current plugin conversation is not a new independent pixel review.', 'Use the existing native review carrier and runtime collector; without that route stop at NEEDS_INDEPENDENT_PIXEL_REVIEW.'], capabilities: { github_state_read: true, image_generation: false, drive_pixels: false, figma_edit: false, independent_reviewer: false, business_state_write: false, training: false, scheduling: false } };
  }
  function current(s) {
    const value = baseCurrent(s);
    return s.latestHumanFeedback ? { ...value, latest_human_feedback: s.latestHumanFeedback, acceptance: { ...value.acceptance, historical_ai_pass_is_not_human_acceptance: true } } : value;
  }
  async function basePlan(s, args) {
    requireThat(args.reference_sha256 === s.delivery.reference_sha256, 'Reference SHA is not the currently bound reference');
    const defaults = { canvas: `${s.copy.dimensions?.join(' × ') ?? 'use native dimensions'}`, attention_geometry: 'Central custom wordmark with subordinate edge information; derive proportions from actual reference pixels.', image_anchor: 'Actual Shanyeji reference pixels; typography-only transfer, photography remains paused.', material_treatment: 'Retain deliberate glyph edges and source-like print character without copying source assets.', typography_behavior: 'Custom original wordmark contours; supporting copy native editable TEXT, exact factual characters.', color_logic: 'Forest green ground, cream main wordmark, orange curve/statement and subordinate gold copy.', variation_axis: 'Adapt wordmark negative spaces and curve responses to new characters; preserve reading hierarchy.' };
    const overrides = args.variables ?? {};
    requireThat(Object.keys(overrides).length <= 7 && Object.entries(overrides).every(([key, value]) => Object.hasOwn(defaults, key) && typeof value === 'string' && value.length > 0 && value.length <= 600), 'Variables must use the seven declared high-leverage axes', -32602, 400);
    const newCopy = args.new_copy ?? Object.fromEntries(Object.entries(s.copy.copy ?? {}).map(([key, value]) => [key, Array.isArray(value) ? value.join('\n\n') : value]));
    requireThat(newCopy && Object.keys(newCopy).length > 0 && Object.keys(newCopy).length <= 20 && Object.values(newCopy).every(x => typeof x === 'string' && x.length > 0 && x.length <= 1000), 'Invalid proposed copy', -32602, 400);
    const variables = { ...defaults, ...overrides };
    return { source: current(s).source, status: 'DRAFT_ROOT_SCOPE_CHECK_REQUIRED', task_id: s.lock.current_task_id, next_required_action: s.lock.next_required_action, execution_authorized: false, reference_sha256: s.delivery.reference_sha256, proposed_copy: newCopy, variables, prompt: Object.values(variables).join(' ') + ` Exact proposed copy: ${Object.values(newCopy).join(' / ')}. Do not copy reference brand, watermark or invented facts.`, workflow: [
      { step: 'reference', action: 'Retrieve/hash/view real reference pixels; record source, license/use boundary and seven variables.' },
      { step: 'copy', action: 'Freeze exact new copy and native scoped authorization with Root; retain historical input contracts.' },
      { step: 'image', action: 'Use existing ChatGPT image tool only within actual native allocation; record prompt, calls, failures and actual exposed model. Guide is not a final accepted work.' },
      { step: 'Figma', action: 'Use connected Figma tools to rebuild original editable contours and native supporting text; verify actual nodes, export, source protection and source identities.' },
      { step: 'independent_review', action: 'Existing independent context/carrier retrieves and views original reference/current artwork; bind actual model, image bytes, runtime and isolation. Missing cold evidence prohibits PASS.' },
      { step: 'repair', action: 'Apply only evidence-backed scoped changes allowed by current lock. Preserve failures; when awaiting human review do not start another version.' },
      { step: 'save', action: 'Root saves Drive original bytes and editable Figma; verifies readback then updates the same native lock/checkpoint/adapter/ledger and reads published state independently.' }
    ], experience: { recognized: { recorded_verdict: s.delivery.review_verdict, scope: s.delivery.scope, benefits: s.delivery.benefits, limits: s.delivery.limits }, rejected: { typography: s.lock.codex_takeover.worker_continuation.reference_typography_study?.typography_human_verdict ?? 'UNKNOWN', historical_human: s.lock.codex_takeover.human_verdict, attempts: s.delivery.formal_version_correspondence ?? [], review_issues: s.review.priority_issues ?? [] }, learning_policy: 'Read scoped evidence; one rating is observe-only. Do not automatically append aesthetic rules or promote this experiment to a universal skill.' }, gates: { engineering_is_not_taste: true, ai_is_not_human: true, no_training_or_paid_or_scheduled_actions: true, actual_external_tools_required: true } };
  }
  async function plan(s, args) {
    const value = await basePlan(s, args);
    return s.latestHumanFeedback ? { ...value, latest_human_feedback: s.latestHumanFeedback, review_handoff_policy: 'Use human feedback only for scoped creator repair. Never attach this feedback, human verdicts or creator history to the cold independent-review packet. Historical AI_PASS is not human final acceptance.' } : value;
  }
  async function feedback(s, args, identity) {
    requireThat(args.artwork_sha256 === s.delivery.export.sha256, 'FEEDBACK_ARTWORK_MISMATCH: feedback must bind current delivered artwork');
    requireThat(/^[A-Za-z0-9_-]{8,128}$/.test(args.idempotency_key), 'Invalid idempotency key', -32602, 400);
    const payload = { schema: 'vpd-plugin-human-feedback-intake/v1', source: { ...SOURCE, commit: s.commit, native_lock_sha256: s.lockHash }, task_id: s.lock.current_task_id, artwork_sha256: args.artwork_sha256, reference_sha256: s.delivery.reference_sha256, delivery: s.transfer.delivery, actor_id: identity.userId, idempotency_key: args.idempotency_key, human_feedback: { verdict: args.verdict, comment: args.comment }, disposition: 'PENDING_ROOT_RECONCILIATION', authority: 'NON_AUTHORITATIVE_INTAKE', append_only: true, mainline_write: false, acceptance_write: false, recorded_at: now() };
    const contentHash = await hash(canonical({ ...payload, recorded_at: undefined }));
    return { validated_intake: payload, content_sha256: contentHash, persisted: false, persistence_requirement: 'Host must append durably by actor/idempotency key, reject conflicting payload reuse, and recheck expected HEAD immediately before persistence. Root reconciles against native artwork identity; intake never changes AI/human verdicts or mainline.' };
  }
  async function handle(request, identity = null) {
    const id = request?.id ?? null;
    try {
      const envelopeError = validateRpcRequest(request);
      requireThat(!envelopeError, envelopeError, -32600, 400);
      const result = value => ({ status: 200, body: { jsonrpc: '2.0', id, result: value } });
      if (request.method === 'initialize') { requireThat(typeof request.params?.protocolVersion === 'string', 'Missing MCP protocol version', -32602, 400); return result({ protocolVersion: negotiatedProtocol(request.params.protocolVersion), capabilities: { tools: {} }, serverInfo: { name: 'visual-aesthetic-workflow', version: '0.1.1' }, instructions: 'Native GitHub state controls this workflow. External image/Figma/Drive and independent pixel review tools remain required. Feedback preparation does not save or approve artwork.' }); }
      if (request.method === 'notifications/initialized') return { status: 202, body: null };
      if (request.method === 'ping') return result({});
      if (request.method === 'tools/list') return result({ tools: TOOLS });
      requireThat(request.method === 'tools/call', 'Method not found', -32601, 400);
      requireThat(identity && typeof identity.userId === 'string' && identity.userId.trim().length > 0, 'Authenticated user identity required', -32001, 401);
      requireThat(await authorize(identity), 'User is not authorized for this workflow', -32003, 403);
      const tool = TOOLS.find(x => x.name === request.params?.name);
      requireThat(tool, 'Unknown tool', -32602, 400);
      const args = request.params.arguments ?? {};
      strictArgs(args, tool);
      const s = await snapshot(args.expected_commit);
      const value = tool.name === 'get_current_workflow' ? current(s) : tool.name === 'compile_transfer_plan' ? await plan(s, args) : await feedback(s, args, identity);
      await s.stable();
      return result({ content: [{ type: 'text', text: JSON.stringify(value) }], structuredContent: value, isError: false });
    } catch (error) {
      const known = error instanceof CoreError;
      return { status: known ? error.status : 502, body: { jsonrpc: '2.0', id, error: { code: known ? error.code : -32603, message: known ? error.message : 'Authoritative repository read failed; no state or acceptance was changed' } } };
    }
  }
  return Object.freeze({ handle });
}
