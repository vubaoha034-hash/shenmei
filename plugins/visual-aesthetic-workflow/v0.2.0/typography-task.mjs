export const VERSION = '0.2.0';

export const STAGES = Object.freeze([
  'REFERENCE_TEXT_EXTRACTION',
  'LOCAL_LETTERING_ASSET',
  'FIGMA_EDITABLE_REBUILD',
  'ACTUAL_INDEPENDENT_TYPOGRAPHY_REVIEW',
  'ISOLATED_TYPOGRAPHY_DELIVERY'
]);

export const TASK_CONTRACT = Object.freeze({
  schema: 'isolated-typography-delivery/v2',
  target_delivery: 'FIGMA_EDITABLE_ISOLATED_TYPOGRAPHY',
  order_locked: true,
  stages: STAGES,
  completion_rule: 'ALL_FIVE_STAGES_REQUIRE_BOUND_REAL_ARTIFACTS',
  forbidden_substitutes: [
    'FULL_POSTER',
    'STRUCTURE_LOCK_REGRESSION',
    'FLATTENED_IMAGE_IN_FIGMA',
    'UNREVIEWED_FIGMA_CANDIDATE',
    'CHAT_SUMMARY_OR_PLAN'
  ],
  poster_work_role: 'DIAGNOSTIC_ONLY_NEVER_COMPLETES_TYPOGRAPHY_TASK',
  native_state_policy: 'READ_ONLY_SNAPSHOT_NEVER_WRITE',
  s7_policy: 'UNCHANGED',
  fail_closed: true
});

const HEX40 = /^[a-f0-9]{40}$/;
const HEX64 = /^[a-f0-9]{64}$/;
const KEY = /^[A-Za-z0-9_-]{8,128}$/;
const TASK = /^typo_[0-9a-f-]{36}$/;
const obj = x => x && typeof x === 'object' && !Array.isArray(x);
const text = (x,max=2048) => typeof x === 'string' && x.trim().length > 0 && x.length <= max;
const integer = x => Number.isInteger(x) && x >= 0;
const same = (a,b) => JSON.stringify(a, Object.keys(a || {}).sort()) === JSON.stringify(b, Object.keys(b || {}).sort());
const fail = code => { const e = new Error(code); e.code = code; throw e; };
const only = (o, keys) => {
  if (!obj(o)) fail('ARGUMENT_OBJECT_REQUIRED');
  for (const k of Object.keys(o)) if (!keys.includes(k)) fail('UNSUPPORTED_ARGUMENT_' + k);
};

export function validateStartArgs(args) {
  only(args, ['expected_commit','request_key','reference_source','requested_copy','request_title']);
  if (!HEX40.test(args.expected_commit || '')) fail('EXPECTED_COMMIT_REQUIRED');
  if (!KEY.test(args.request_key || '')) fail('REQUEST_KEY_INVALID');
  if (!text(args.reference_source,2048)) fail('REFERENCE_SOURCE_REQUIRED');
  if (!obj(args.requested_copy) || Object.keys(args.requested_copy).length < 1 || Object.keys(args.requested_copy).length > 20) fail('REQUESTED_COPY_REQUIRED');
  for (const [k,v] of Object.entries(args.requested_copy)) {
    if (!text(k,128) || !text(v,1000)) fail('REQUESTED_COPY_INVALID');
  }
  if (args.request_title !== undefined && !text(args.request_title,200)) fail('REQUEST_TITLE_INVALID');
  return args;
}

export function validateGetArgs(args) {
  only(args || {}, ['task_id']);
  if (args?.task_id !== undefined && !TASK.test(args.task_id)) fail('TASK_ID_INVALID');
  return args || {};
}

export function validateRecordArgs(args) {
  only(args, ['task_id','expected_revision','stage','artifact']);
  if (!TASK.test(args.task_id || '')) fail('TASK_ID_INVALID');
  if (!Number.isInteger(args.expected_revision) || args.expected_revision < 1) fail('EXPECTED_REVISION_INVALID');
  if (!STAGES.includes(args.stage)) fail('STAGE_INVALID');
  if (!obj(args.artifact)) fail('ARTIFACT_REQUIRED');
  return args;
}

function commonIsolated(a) {
  if (a.contains_full_poster !== false) fail('FULL_POSTER_CANNOT_SATISFY_TYPOGRAPHY_STAGE');
  if (a.structure_lock_test === true || a.regression_test === true) fail('REGRESSION_EVIDENCE_CANNOT_SATISFY_TYPOGRAPHY_STAGE');
}

export function validateStageArtifact(stage, a, task) {
  const latest = task.latest_artifacts || {};
  if (stage === 'REFERENCE_TEXT_EXTRACTION') {
    if (a.artifact_type !== 'REFERENCE_TEXT_EXTRACTION') fail('REFERENCE_TEXT_EXTRACTION_ARTIFACT_REQUIRED');
    if (a.reference_source !== task.reference_source) fail('REFERENCE_SOURCE_MISMATCH');
    if (!HEX64.test(a.reference_sha256 || '')) fail('REFERENCE_SHA256_REQUIRED');
    if (a.actual_reference_pixels_viewed !== true) fail('ACTUAL_REFERENCE_PIXELS_MUST_BE_VIEWED');
    if (!obj(a.extracted_reference_text) || Object.keys(a.extracted_reference_text).length < 1) fail('EXTRACTED_REFERENCE_TEXT_REQUIRED');
    if (!text(a.typography_observations,6000) || !text(a.geometry_evidence,2048)) fail('REFERENCE_TYPOGRAPHY_EVIDENCE_REQUIRED');
    if (a.contains_full_poster === true) fail('FULL_POSTER_CANNOT_BE_STAGE_ARTIFACT');
    return {advance:true};
  }
  commonIsolated(a);
  const ref = latest.REFERENCE_TEXT_EXTRACTION;
  if (!ref) fail('REFERENCE_STAGE_ARTIFACT_MISSING');
  if (a.reference_sha256 !== ref.reference_sha256) fail('REFERENCE_SHA256_MISMATCH');

  if (stage === 'LOCAL_LETTERING_ASSET') {
    if (a.artifact_type !== 'LOCAL_LETTERING_ASSET') fail('LOCAL_LETTERING_ARTIFACT_REQUIRED');
    if (!HEX64.test(a.asset_sha256 || '') || !text(a.asset_locator,2048)) fail('LOCAL_LETTERING_ASSET_IDENTITY_REQUIRED');
    if (a.transparent_background !== true || a.isolated_typography_only !== true || a.copy_confirmed !== true) fail('LOCAL_LETTERING_SCOPE_INVALID');
    if (!obj(a.target_copy) || !same(a.target_copy, task.requested_copy)) fail('TARGET_COPY_MISMATCH');
    return {advance:true};
  }

  if (stage === 'FIGMA_EDITABLE_REBUILD') {
    const local = latest.LOCAL_LETTERING_ASSET;
    if (!local) fail('LOCAL_LETTERING_STAGE_ARTIFACT_MISSING');
    if (a.artifact_type !== 'FIGMA_EDITABLE_TYPOGRAPHY_REBUILD') fail('FIGMA_EDITABLE_REBUILD_ARTIFACT_REQUIRED');
    if (a.source_asset_sha256 !== local.asset_sha256) fail('FIGMA_SOURCE_ASSET_MISMATCH');
    for (const k of ['file_key','page_id','node_id','figma_url','readback_evidence','export_locator']) if (!text(a[k],2048)) fail('FIGMA_' + k.toUpperCase() + '_REQUIRED');
    if (!HEX64.test(a.export_sha256 || '')) fail('FIGMA_EXPORT_SHA256_REQUIRED');
    if (a.actual_readback_verified !== true || a.isolated_typography_only !== true || a.flattened_image_only !== false) fail('FIGMA_READBACK_OR_SCOPE_INVALID');
    if (!integer(a.native_text_node_count) || !integer(a.editable_vector_node_count) || !integer(a.image_node_count)) fail('FIGMA_NODE_COUNTS_REQUIRED');
    if ((a.native_text_node_count + a.editable_vector_node_count) < 1) fail('FIGMA_EDITABLE_NODES_REQUIRED');
    if (a.image_node_count !== 0) fail('FIGMA_IMAGE_NODE_CANNOT_BE_FINAL_EDITABLE_TYPOGRAPHY');
    return {advance:true};
  }

  if (stage === 'ACTUAL_INDEPENDENT_TYPOGRAPHY_REVIEW') {
    const figma = latest.FIGMA_EDITABLE_REBUILD;
    if (!figma) fail('FIGMA_STAGE_ARTIFACT_MISSING');
    if (a.artifact_type !== 'ACTUAL_INDEPENDENT_TYPOGRAPHY_REVIEW') fail('ACTUAL_INDEPENDENT_REVIEW_ARTIFACT_REQUIRED');
    if (a.reviewed_export_sha256 !== figma.export_sha256) fail('REVIEW_EXPORT_MISMATCH');
    if (!['PASS','PASS_WITH_LIMITATIONS','FAIL'].includes(a.verdict)) fail('REVIEW_VERDICT_INVALID');
    if (a.actual_pixels_viewed !== true || a.reference_pixels_viewed !== true || a.output_pixels_viewed !== true || a.independent_context !== true || a.creator_history_inherited !== false || a.human_verdict_leaked !== false || a.typography_only_scope !== true) fail('INDEPENDENT_ACTUAL_PIXEL_REVIEW_EVIDENCE_REQUIRED');
    if (!text(a.carrier_evidence,2048) || !text(a.pixel_transport_evidence,2048) || !text(a.review_notes,6000)) fail('REVIEW_EVIDENCE_REQUIRED');
    return a.verdict === 'FAIL' ? {advance:false,repair:true} : {advance:true};
  }

  if (stage === 'ISOLATED_TYPOGRAPHY_DELIVERY') {
    const figma = latest.FIGMA_EDITABLE_REBUILD;
    const review = latest.ACTUAL_INDEPENDENT_TYPOGRAPHY_REVIEW;
    if (!figma || !review || review.verdict === 'FAIL') fail('PASSING_REVIEW_REQUIRED_BEFORE_DELIVERY');
    if (a.artifact_type !== 'ISOLATED_EDITABLE_TYPOGRAPHY_DELIVERY') fail('ISOLATED_TYPOGRAPHY_DELIVERY_ARTIFACT_REQUIRED');
    if (a.file_key !== figma.file_key || a.page_id !== figma.page_id || a.node_id !== figma.node_id) fail('DELIVERY_FIGMA_IDENTITY_MISMATCH');
    if (a.reviewed_export_sha256 !== review.reviewed_export_sha256) fail('DELIVERY_REVIEW_BINDING_MISMATCH');
    if (a.review_verdict !== review.verdict) fail('DELIVERY_REVIEW_VERDICT_MISMATCH');
    if (a.delivery_scope !== 'ISOLATED_EDITABLE_TYPOGRAPHY_ONLY') fail('DELIVERY_SCOPE_INVALID');
    if (a.actual_figma_readback_verified !== true || a.includes_editable_source !== true || a.flattened_image_only !== false) fail('EDITABLE_FIGMA_DELIVERY_REQUIRED');
    if (!text(a.share_url,2048) || !text(a.delivery_evidence,2048)) fail('DELIVERY_EVIDENCE_REQUIRED');
    return {advance:true,complete:true};
  }
  fail('UNKNOWN_STAGE');
}

export function createTask(args, nativeSnapshot, now, taskId) {
  return {
    schema: TASK_CONTRACT.schema,
    task_id: taskId,
    request_key: args.request_key,
    request_title: args.request_title || '独立文字设计',
    revision: 1,
    status: 'IN_PROGRESS',
    stage: STAGES[0],
    next_required_action: STAGES[0],
    reference_source: args.reference_source,
    requested_copy: args.requested_copy,
    native_snapshot: nativeSnapshot,
    native_state_write: false,
    native_task_lock_unchanged: true,
    s7_state_unchanged: true,
    target_delivery: TASK_CONTRACT.target_delivery,
    repair_cycle: 0,
    latest_artifacts: {},
    artifact_history: [],
    created_at: now,
    updated_at: now
  };
}

export function applyStage(task, stage, artifact, now) {
  if (task.status === 'COMPLETE') fail('TASK_ALREADY_COMPLETE');
  if (task.stage !== stage) fail('STAGE_ORDER_VIOLATION_EXPECTED_' + task.stage);
  const decision = validateStageArtifact(stage, artifact, task);
  const history = [...(task.artifact_history || []), {stage, artifact, recorded_at: now, revision: task.revision + 1}];
  const latest = {...(task.latest_artifacts || {}), [stage]: artifact};
  let nextStage = stage, status = 'IN_PROGRESS', next = stage, repair = task.repair_cycle || 0;
  if (decision.repair) {
    nextStage = 'FIGMA_EDITABLE_REBUILD';
    next = 'FIGMA_EDITABLE_REBUILD';
    status = 'NEEDS_REPAIR';
    repair += 1;
  } else if (decision.complete) {
    nextStage = 'ISOLATED_TYPOGRAPHY_DELIVERY';
    next = 'NONE_COMPLETE';
    status = 'COMPLETE';
  } else {
    const i = STAGES.indexOf(stage);
    nextStage = STAGES[i + 1];
    next = nextStage;
  }
  return {...task, revision: task.revision + 1, status, stage: nextStage, next_required_action: next, repair_cycle: repair, latest_artifacts: latest, artifact_history: history, updated_at: now};
}

const objectSchema = (properties={},required=[]) => ({type:'object',properties,required,additionalProperties:false});
const string = {type:'string',minLength:1};
export const TASK_TOOLS = Object.freeze([
  {
    name:'start_typography_delivery',
    description:'Start or idempotently recover a persistent request-level isolated typography task. Hard-locks the only completion path to reference text extraction → local lettering asset → editable Figma typography rebuild → actual independent pixel review → isolated editable typography delivery. Full posters, structure-lock regressions, flattened Figma images and plans cannot satisfy any later stage. Reads authoritative native workflow first and stores only a read-only snapshot; never writes native task lock or S7.',
    inputSchema:objectSchema({
      expected_commit:{type:'string',pattern:'^[a-f0-9]{40}$'},
      request_key:{type:'string',pattern:'^[A-Za-z0-9_-]{8,128}$'},
      reference_source:{type:'string',minLength:1,maxLength:2048},
      requested_copy:{type:'object',minProperties:1,maxProperties:20,additionalProperties:{type:'string',minLength:1,maxLength:1000}},
      request_title:{type:'string',minLength:1,maxLength:200}
    },['expected_commit','request_key','reference_source','requested_copy']),
    annotations:{readOnlyHint:false,destructiveHint:false,idempotentHint:true,openWorldHint:true}
  },
  {
    name:'get_typography_delivery',
    description:'Read the authenticated user’s persistent isolated-typography task, including exact current gate, revision, bound artifacts and the immutable delivery contract. Omit task_id to read the most recently updated request task. This is separate from native S7/business state.',
    inputSchema:objectSchema({task_id:{type:'string',pattern:'^typo_[0-9a-f-]{36}$'}}),
    annotations:{readOnlyHint:true,openWorldHint:false}
  },
  {
    name:'record_typography_stage',
    description:'Record one real stage artifact and advance exactly one gate with optimistic revision control. The server rejects stage skipping and rejects full-poster/regression/flattened-image substitutes. A FAIL independent review returns the task to FIGMA_EDITABLE_REBUILD for repair; only a passing bound review can reach isolated editable typography delivery. This receipt does not change native task lock, S7, AI verdict or human acceptance.',
    inputSchema:objectSchema({
      task_id:{type:'string',pattern:'^typo_[0-9a-f-]{36}$'},
      expected_revision:{type:'integer',minimum:1},
      stage:{type:'string',enum:STAGES},
      artifact:{type:'object',minProperties:1,additionalProperties:true}
    },['task_id','expected_revision','stage','artifact']),
    annotations:{readOnlyHint:false,destructiveHint:false,idempotentHint:false,openWorldHint:true}
  }
]);
