// v0.3.0: exact AI-master-first isolated typography contract.
// A receipt is a gate, not proof that the server independently inspected pixels.
export const VERSION = '0.3.0';
export const STAGES = Object.freeze([
  'REFERENCE_TEXT_EXTRACTION',
  'AI_COMPLETE_TRANSPARENT_TYPOGRAPHY_MASTER',
  'FIGMA_EXACT_EDITABLE_REBUILD',
  'INDEPENDENT_MASTER_FIGMA_PIXEL_AUDIT',
  'ISOLATED_TYPOGRAPHY_DELIVERY'
]);
export const LEGACY_SCHEMA='isolated-typography-delivery/v2';
export const REQUIRED_COPY_ROLES = Object.freeze(['main_wordmark','top_wordmark','english','vertical_copy','footer_copy']);
export const TASK_CONTRACT = Object.freeze({
  schema:'isolated-typography-delivery/v3',
  target_delivery:'AI_TRANSPARENT_MASTER_PLUS_FIGMA_EDITABLE_EXACT_REPLICA_PLUS_PIXEL_AUDIT',
  order_locked:true, stages:STAGES,
  exact_copy_roles:REQUIRED_COPY_ROLES,
  stage_authority:'AI_MASTER_IS_THE_ONLY_FIGMA_VISUAL_TRUTH_REFERENCE_PHOTO_IS_STYLE_SOURCE_ONLY',
  mandatory_master:'ACTUAL_AI_GENERATED_RGBA_PNG_NOT_SVG_GUIDE',
  all_source_regions:'INVENTORY_EVERY_VISIBLE_TEXT_ELEMENT_EACH_MAPPED_TO_KEEP_OR_REPLACE',
  final_node_set:'NATIVE_EDITABLE_TEXT_OR_VECTOR_ONLY_IMAGE_NODE_COUNT_ZERO',
  comparison:'AI_MASTER_RGBA_VS_FIGMA_EXPORTED_RGBA_NOT_REFERENCE_PHOTO',
  pixel_verification:'ACTUAL_BOTH_IMAGE_BYTES_READ_AND_MEASURED_BY_INDEPENDENT_EXECUTOR; SERVER_ONLY_ENFORCES_EVIDENCE_AND_THRESHOLDS',
  pass_metric_thresholds:{alpha_iou_min:0.97, per_region_alpha_iou_min:0.95, normalized_rgba_mae_max:0.04, per_region_rgba_mae_max:0.065, bbox_max_error_px:2},
  exactness_disclaimer:'HIGH_FIDELITY_QUANTIFIED_VISUAL_EQUIVALENCE_NOT_FALSE_ZERO_RASTER_DIFFERENCE',
  completion_rule:'ALL_FIVE_CURRENT_CONTRACT_STAGES_WITH_REAL_BOUND_ARTIFACTS',
  forbidden_substitutes:['LEGACY_V2_TASK','SVG_GUIDE_AS_AI_MASTER','FULL_POSTER','STRUCTURE_LOCK_REGRESSION','FLATTENED_IMAGE_IN_FIGMA','SAME_TEXT_ONLY','FIGMA_NODE_COUNTS_ONLY','RECEIPT_ONLY_NO_PIXEL_MEASUREMENT','REFERENCE_PHOTO_AS_FIGMA_COMPARE_TARGET','UNREVIEWED_FIGMA_CANDIDATE','CHAT_SUMMARY_OR_PLAN'],
  native_state_policy:'READ_ONLY_SNAPSHOT_NEVER_WRITE',s7_policy:'UNCHANGED', fail_closed:true
});
const HEX40=/^[a-f0-9]{40}$/; const HEX64=/^[a-f0-9]{64}$/; const KEY=/^[A-Za-z0-9_-]{8,128}$/; const TASK=/^typo_[0-9a-f-]{36}$/;
const obj=x=>!!x&&typeof x==='object'&&!Array.isArray(x);
const text=(x,max=2048)=>typeof x==='string'&&x.trim().length>0&&x.length<=max;
const uint=x=>Number.isInteger(x)&&x>=0;
const pos=x=>Number.isInteger(x)&&x>0;
const fail=code=>{const e=new Error(code);e.code=code;throw e;};
const only=(o,keys)=>{if(!obj(o))fail('ARGUMENT_OBJECT_REQUIRED');for(const k of Object.keys(o))if(!keys.includes(k))fail('UNSUPPORTED_ARGUMENT_'+k);};
const canonical=value=>JSON.stringify(value,(_k,v)=>obj(v)?Object.fromEntries(Object.entries(v).sort(([a],[b])=>a.localeCompare(b))):v);
const eq=(a,b)=>canonical(a)===canonical(b);
const mustText=(x,code,max=2048)=>{if(!text(x,max))fail(code);};
const mustHash=(x,code)=>{if(!HEX64.test(x||''))fail(code);};
const mustTrue=(x,code)=>{if(x!==true)fail(code);};
const mustFalse=(x,code)=>{if(x!==false)fail(code);};
const mustPositive=(x,code)=>{if(!pos(x))fail(code);};
const mustRef=(a,task)=>{const ref=task.latest_artifacts?.REFERENCE_TEXT_EXTRACTION;if(!ref)fail('REFERENCE_STAGE_ARTIFACT_MISSING');if(a.reference_sha256!==ref.reference_sha256)fail('REFERENCE_SHA256_MISMATCH');return ref;};
const assertCurrent=task=>{if(task?.schema!==TASK_CONTRACT.schema)fail('CONTRACT_UPGRADE_REQUIRED');};
const bbox=(b,w,h)=>obj(b)&&[b.x,b.y,b.width,b.height].every(uint)&&b.width>0&&b.height>0&&b.x+b.width<=w&&b.y+b.height<=h;
const byRegion=(items,regions,code,verify)=>{
  if(!Array.isArray(items)||items.length!==regions.length)fail(code+'_COUNT');
  const want=new Map(regions.map(r=>[r.region_id,r])); const found=new Set();
  for(const e of items){if(!obj(e)||!text(e.region_id,128)||!want.has(e.region_id)||found.has(e.region_id))fail(code+'_REGION_ID');found.add(e.region_id);const ref=want.get(e.region_id);if(e.target_text!==ref.target_text)fail(code+'_TARGET_TEXT');if(verify)verify(e,ref);}
  return true;
};
export function validateStartArgs(args){
  only(args,['expected_commit','request_key','reference_source','requested_copy','request_title']);
  if(!HEX40.test(args.expected_commit||''))fail('EXPECTED_COMMIT_REQUIRED');
  if(!KEY.test(args.request_key||''))fail('REQUEST_KEY_INVALID');
  mustText(args.reference_source,'REFERENCE_SOURCE_REQUIRED');
  if(!obj(args.requested_copy)||Object.keys(args.requested_copy).length<5||Object.keys(args.requested_copy).length>20)fail('REQUESTED_COPY_REQUIRED');
  for(const role of REQUIRED_COPY_ROLES)mustText(args.requested_copy[role],'REQUESTED_COPY_ROLE_MISSING_'+role,1000);
  for(const [k,v] of Object.entries(args.requested_copy)){mustText(k,'COPY_KEY_INVALID',128);mustText(v,'REQUESTED_COPY_INVALID',1000);}
  if(args.request_title!==undefined)mustText(args.request_title,'REQUEST_TITLE_INVALID',200);
  return args;
}
export function validateGetArgs(args){only(args||{},['task_id']);if(args?.task_id!==undefined&&!TASK.test(args.task_id))fail('TASK_ID_INVALID');return args||{};}
export function validateRecordArgs(args){only(args,['task_id','expected_revision','stage','artifact']);if(!TASK.test(args.task_id||''))fail('TASK_ID_INVALID');if(!pos(args.expected_revision))fail('EXPECTED_REVISION_INVALID');if(!STAGES.includes(args.stage))fail('STAGE_INVALID');if(!obj(args.artifact))fail('ARTIFACT_REQUIRED');return args;}
export function validateUpgradeArgs(args){only(args,['task_id','expected_revision','migration_reason']);if(!TASK.test(args.task_id||''))fail('TASK_ID_INVALID');if(!pos(args.expected_revision))fail('EXPECTED_REVISION_INVALID');mustText(args.migration_reason,'MIGRATION_REASON_REQUIRED',2000);return args;}
export function upgradeLegacyTask(task,now,reason){
  if(task.schema!==LEGACY_SCHEMA)fail(task.schema===TASK_CONTRACT.schema?'ALREADY_UPGRADED':'UNSUPPORTED_TASK_SCHEMA');
  if(task.status==='COMPLETE')fail('LEGACY_COMPLETION_REQUIRES_MANUAL_RECONCILIATION');
  const prior={schema:task.schema,stage:task.stage,status:task.status,revision:task.revision,latest_artifacts:task.latest_artifacts};
  const history=[...(task.artifact_history||[]),{stage:'CONTRACT_MIGRATION_V2_TO_V3',recorded_at:now,revision:task.revision+1,reason,previous_state:prior}];
  return {...task,schema:TASK_CONTRACT.schema,revision:task.revision+1,status:'NEEDS_REBUILD',stage:STAGES[0],next_required_action:STAGES[0],target_delivery:TASK_CONTRACT.target_delivery,
    latest_artifacts:{},legacy_artifacts:task.latest_artifacts,artifact_history:history,
    native_snapshot:task.native_snapshot,native_state_write:false,native_task_lock_unchanged:true,s7_state_unchanged:true,
    migrated_from_version:'0.2.0',contract_migrated_at:now,updated_at:now};
}
function validateInventory(regions,task,w,h){
  if(!Array.isArray(regions)||regions.length<REQUIRED_COPY_ROLES.length||regions.length>60)fail('FULL_REFERENCE_TEXT_INVENTORY_REQUIRED');
  const seen=new Set(),roles=new Set();
  for(const r of regions){
    if(!obj(r)||!text(r.region_id,128)||seen.has(r.region_id))fail('DUPLICATE_OR_INVALID_REFERENCE_TEXT_REGION');
    seen.add(r.region_id);mustText(r.source_text,'SOURCE_TEXT_REQUIRED_FOR_EVERY_REGION',1000);mustText(r.target_text,'TARGET_TEXT_REQUIRED_FOR_EVERY_REGION',1000);
    if(!bbox(r.bbox,w,h))fail('REFERENCE_TEXT_BBOX_INVALID');
    if(!['REPLACE','PRESERVE'].includes(r.mode))fail('REGION_CHANGE_MODE_INVALID');
    if(!obj(r.visual_spec)||!text(r.visual_spec.description,2000)||!text(r.visual_spec.color,128))fail('REGION_FONT_APPEARANCE_EVIDENCE_REQUIRED');
    if(r.role!==undefined){
      if(!REQUIRED_COPY_ROLES.includes(r.role)||roles.has(r.role)||r.mode!=='REPLACE'||r.target_text!==task.requested_copy[r.role])fail('FROZEN_COPY_ROLE_MISMATCH');
      roles.add(r.role);
    }else if(r.mode==='PRESERVE'&&r.target_text!==r.source_text)fail('PRESERVED_REGION_TEXT_CHANGED');
  }
  if(REQUIRED_COPY_ROLES.some(k=>!roles.has(k)))fail('FIVE_DISTINCT_COPY_REGIONS_REQUIRED');
  return true;
}
const isolated=a=>{mustFalse(a.contains_full_poster,'FULL_POSTER_FORBIDDEN');mustFalse(a.contains_photo,'PHOTO_FORBIDDEN');if(a.structure_lock_test===true||a.regression_test===true)fail('REGRESSION_ARTIFACT_FORBIDDEN');};
export function validateStageArtifact(stage,a,task){
  assertCurrent(task);const latest=task.latest_artifacts||{};
  if(stage==='REFERENCE_TEXT_EXTRACTION'){
    if(a.artifact_type!=='REFERENCE_TEXT_EXTRACTION')fail('REFERENCE_TEXT_EXTRACTION_ARTIFACT_REQUIRED');
    if(a.reference_source!==task.reference_source)fail('REFERENCE_SOURCE_MISMATCH');
    mustHash(a.reference_sha256,'REFERENCE_SHA256_REQUIRED');
    mustPositive(a.poster_crop_width,'POSTER_CROP_WIDTH_REQUIRED');mustPositive(a.poster_crop_height,'POSTER_CROP_HEIGHT_REQUIRED');
    mustTrue(a.actual_reference_pixels_viewed,'REAL_REFERENCE_PIXELS_NOT_READ');
    mustText(a.pixel_read_evidence,'REFERENCE_FILE_BYTE_EVIDENCE_REQUIRED');
    mustTrue(a.full_reference_text_coverage_verified,'UNINVENTORIED_SOURCE_TEXT');
    if(a.inventoried_region_count!==a.text_regions?.length)fail('REFERENCE_REGION_COUNT_MISMATCH');
    validateInventory(a.text_regions,task,a.poster_crop_width,a.poster_crop_height);
    isolated(a);return {advance:true};
  }
  const ref=mustRef(a,task);
  if(stage==='AI_COMPLETE_TRANSPARENT_TYPOGRAPHY_MASTER'){
    if(a.artifact_type!=='AI_COMPLETE_TRANSPARENT_TYPOGRAPHY_MASTER')fail('REAL_AI_MASTER_REQUIRED');
    if(a.generation_mode!=='AI_IMAGE_GENERATION_OR_EDIT' || a.generated_for_this_task!==true || a.is_svg_guide!==false)fail('SVG_GUIDE_NOT_AI_MASTER');
    mustHash(a.master_sha256,'AI_MASTER_SHA256_REQUIRED');mustText(a.master_png_locator,'AI_MASTER_PNG_LOCATOR_REQUIRED');
    mustText(a.image_generator_evidence,'ACTUAL_AI_GENERATION_EVIDENCE_REQUIRED');mustText(a.generator_result_id,'AI_GENERATION_RESULT_ID_REQUIRED');
    mustTrue(a.actual_master_png_bytes_read,'AI_MASTER_PNG_BYTES_NOT_READ');mustText(a.pixel_digest_evidence,'AI_MASTER_BYTE_HASH_EVIDENCE_REQUIRED');
    if(a.mime_type!=='image/png'||a.png_mode!=='RGBA'||a.master_width!==ref.poster_crop_width||a.master_height!==ref.poster_crop_height)fail('AI_MASTER_RGBA_CROP_DIMENSIONS_INVALID');
    mustTrue(a.alpha_channel_verified,'AI_MASTER_ALPHA_NOT_VERIFIED');
    if(!uint(a.alpha_zero_pixel_count)||a.alpha_zero_pixel_count<1||!pos(a.alpha_nonzero_pixel_count))fail('MASTER_TRANSPARENCY_PIXEL_COUNTS_REQUIRED');
    mustTrue(a.all_copy_pixel_review_pass,'AI_MASTER_ALL_TEXT_NOT_VERIFIED');mustTrue(a.reference_region_coverage_verified,'AI_MASTER_REGION_COVERAGE_NOT_VERIFIED');
    byRegion(a.text_regions,ref.text_regions,'AI_MASTER',e=>{if(e.visible_in_master!==true||!bbox(e.bbox,a.master_width,a.master_height))fail('AI_MASTER_REGION_NOT_VISIBLE');});
    isolated(a);mustTrue(a.frozen_as_only_figma_visual_truth,'AI_MASTER_NOT_FROZEN');return {advance:true};
  }
  if(stage==='FIGMA_EXACT_EDITABLE_REBUILD'){
    const master=latest.AI_COMPLETE_TRANSPARENT_TYPOGRAPHY_MASTER;
    if(!master)fail('APPROVED_AI_MASTER_REQUIRED_BEFORE_FIGMA');
    if(a.artifact_type!=='FIGMA_EXACT_EDITABLE_REBUILD')fail('FIGMA_EXACT_REBUILD_RECEIPT_REQUIRED');
    if(a.ai_master_sha256!==master.master_sha256||a.reference_sha256!==master.reference_sha256)fail('FIGMA_AI_MASTER_HASH_MISMATCH');
    if(a.visual_reference!=='AI_MASTER_ONLY'||a.reinterpreted_or_redisigned!==false)fail('FIGMA_REDESIGN_FORBIDDEN');
    for(const k of ['file_key','page_id','node_id','figma_url','node_tree_readback','export_png_locator','export_readback_evidence'])mustText(a[k],'FIGMA_'+k+'_REQUIRED');
    mustHash(a.export_sha256,'ACTUAL_FIGMA_EXPORT_HASH_REQUIRED');mustTrue(a.export_png_bytes_read,'FIGMA_EXPORT_PNG_NOT_READ');
    if(a.export_width!==master.master_width||a.export_height!==master.master_height||a.export_mime!=='image/png'||a.export_mode!=='RGBA')fail('FIGMA_EXPORT_CANVAS_OR_RGBA_MISMATCH');
    if(!uint(a.text_node_count)||!uint(a.vector_node_count)||(a.text_node_count+a.vector_node_count)<1||a.image_node_count!==0||a.flattened_image_only!==false)fail('FIGMA_NATIVE_EDITABILITY_REQUIRED_NO_IMAGE');
    byRegion(a.region_nodes,master.text_regions,'FIGMA_REGION',e=>{if(!Array.isArray(e.native_node_ids)||e.native_node_ids.length<1||!e.native_node_ids.every(x=>text(x,128)))fail('FIGMA_REGION_NOT_NATIVE_EDITABLE');});
    isolated(a);return {advance:true};
  }
  if(stage==='INDEPENDENT_MASTER_FIGMA_PIXEL_AUDIT'){
    const master=latest.AI_COMPLETE_TRANSPARENT_TYPOGRAPHY_MASTER,figma=latest.FIGMA_EXACT_EDITABLE_REBUILD;
    if(!master||!figma)fail('MASTER_AND_FIGMA_REQUIRED_FOR_AUDIT');
    if(a.artifact_type!=='INDEPENDENT_MASTER_FIGMA_PIXEL_AUDIT')fail('ACTUAL_PIXEL_AUDIT_REQUIRED');
    if(a.master_sha256!==master.master_sha256||a.figma_export_sha256!==figma.export_sha256)fail('AUDIT_ARTIFACT_HASH_MISMATCH');
    if(a.comparison_type!=='AI_MASTER_VS_FIGMA_EXPORT'||a.reference_photo_as_comparison_target!==false)fail('WRONG_AUDIT_COMPARISON_SOURCE');
    mustTrue(a.independent_context,'INDEPENDENT_AUDITOR_REQUIRED');
    mustTrue(a.actual_ai_master_pixels_read,'AI_MASTER_ACTUAL_PIXELS_NOT_READ');mustTrue(a.actual_figma_export_pixels_read,'FIGMA_ACTUAL_PIXELS_NOT_READ');
    mustText(a.master_pixel_read_evidence,'MASTER_READ_EVIDENCE_REQUIRED');mustText(a.figma_pixel_read_evidence,'FIGMA_READ_EVIDENCE_REQUIRED');
    mustText(a.audit_script_or_tool,'REPRODUCIBLE_AUDIT_EXECUTOR_REQUIRED');mustText(a.metrics_artifact_locator,'PIXEL_METRICS_ARTIFACT_REQUIRED');
    if(a.verdict!=='PASS'&&a.verdict!=='FAIL')fail('STRICT_PASS_OR_FAIL_REQUIRED');
    const m=a.metrics;
    if(!obj(m)||m.dimensions_match!==true||m.registration_aligned!==true||m.text_accuracy_100_percent!==true||m.transparent_background_verified!==true)fail('AUDIT_DIMENSIONS_ALIGNMENT_OR_COPY_FAILED');
    for(const k of ['alpha_iou','normalized_rgba_mae','bbox_max_error_px'])if(!Number.isFinite(m[k]))fail('AUDIT_NUMERIC_PIXEL_METRIC_REQUIRED');
    const th=TASK_CONTRACT.pass_metric_thresholds;
    byRegion(m.region_metrics,master.text_regions,'AUDIT_REGION',e=>{if(!Number.isFinite(e.alpha_iou)||!Number.isFinite(e.normalized_rgba_mae)||!Number.isFinite(e.bbox_error_px))fail('AUDIT_REGION_NUMERIC_METRICS_REQUIRED');});
    const pass=m.alpha_iou>=th.alpha_iou_min&&m.normalized_rgba_mae<=th.normalized_rgba_mae_max&&m.bbox_max_error_px<=th.bbox_max_error_px&&m.region_metrics.every(e=>e.alpha_iou>=th.per_region_alpha_iou_min&&e.normalized_rgba_mae<=th.per_region_rgba_mae_max&&e.bbox_error_px<=th.bbox_max_error_px);
    if(a.verdict==='PASS'&&!pass)fail('LOOSE_THRESHOLDS_CANNOT_CLAIM_EXACT_REPLICA');
    if(a.verdict==='FAIL'||!pass)return {advance:false,repair:true};
    return {advance:true};
  }
  if(stage==='ISOLATED_TYPOGRAPHY_DELIVERY'){
    const master=latest.AI_COMPLETE_TRANSPARENT_TYPOGRAPHY_MASTER,figma=latest.FIGMA_EXACT_EDITABLE_REBUILD,audit=latest.INDEPENDENT_MASTER_FIGMA_PIXEL_AUDIT;
    if(!master||!figma||!audit||audit.verdict!=='PASS')fail('INDEPENDENT_PIXEL_AUDIT_PASS_REQUIRED');
    if(a.artifact_type!=='ISOLATED_EDITABLE_TYPOGRAPHY_DELIVERY')fail('TYPOGRAPHY_DELIVERY_RECEIPT_REQUIRED');
    if(a.master_sha256!==master.master_sha256||a.figma_export_sha256!==figma.export_sha256||a.audit_metrics_artifact_locator!==audit.metrics_artifact_locator)fail('FINAL_THREE_ARTIFACT_CHAIN_BROKEN');
    if(a.figma_url!==figma.figma_url||a.master_png_locator!==master.master_png_locator)fail('DELIVERY_ARTIFACT_MISMATCH');
    mustText(a.delivery_review_evidence,'ACTUAL_DELIVERY_REVIEW_REQUIRED');mustTrue(a.editable_figma_verified,'FINAL_EDITABLE_SOURCE_REQUIRED');
    if(a.delivery_scope!=='AI_MASTER_PLUS_EDITABLE_FIGMA_PLUS_PIXEL_AUDIT')fail('ALL_THREE_DELIVERABLES_REQUIRED');
    isolated(a);return {advance:true,complete:true};
  }
  fail('UNKNOWN_STAGE');
}
export function createTask(args,nativeSnapshot,now,taskId){return {schema:TASK_CONTRACT.schema,task_id:taskId,request_key:args.request_key,request_title:args.request_title||'独立可编辑文字设计',revision:1,status:'IN_PROGRESS',stage:STAGES[0],next_required_action:STAGES[0],reference_source:args.reference_source,requested_copy:args.requested_copy,native_snapshot:nativeSnapshot,native_state_write:false,native_task_lock_unchanged:true,s7_state_unchanged:true,target_delivery:TASK_CONTRACT.target_delivery,repair_cycle:0,latest_artifacts:{},artifact_history:[],created_at:now,updated_at:now};}
export function applyStage(task,stage,artifact,now){
  assertCurrent(task);if(task.status==='COMPLETE')fail('TASK_ALREADY_COMPLETE');if(task.stage!==stage)fail('STAGE_ORDER_VIOLATION_EXPECTED_'+task.stage);
  const result=validateStageArtifact(stage,artifact,task);
  const history=[...(task.artifact_history||[]),{stage,artifact,recorded_at:now,revision:task.revision+1}];
  const latest={...(task.latest_artifacts||{}),[stage]:artifact};
  const next=result.complete?'ISOLATED_TYPOGRAPHY_DELIVERY':result.repair?'FIGMA_EXACT_EDITABLE_REBUILD':STAGES[STAGES.indexOf(stage)+1];
  return {...task,revision:task.revision+1,status:result.complete?'COMPLETE':result.repair?'NEEDS_REPAIR':'IN_PROGRESS',stage:next,next_required_action:result.complete?'NONE_COMPLETE':next,repair_cycle:(task.repair_cycle||0)+(result.repair?1:0),latest_artifacts:latest,artifact_history:history,updated_at:now};
}
const schema=(properties={},required=[])=>({type:'object',properties,required,additionalProperties:false});
export const TASK_TOOLS=Object.freeze([
 {name:'start_typography_delivery',description:'Start or idempotently recover single isolated typography task, enforcing reference full text inventory → actual AI RGBA master → Figma native exact rebuild → independent master-vs-export pixel audit → all-three-artifact delivery. Existing legacy task must be explicitly upgraded, never replaced. Native S7 remains read-only.',inputSchema:schema({expected_commit:{type:'string',pattern:'^[a-f0-9]{40}$'},request_key:{type:'string',pattern:'^[A-Za-z0-9_-]{8,128}$'},reference_source:{type:'string',minLength:1},requested_copy:{type:'object',minProperties:5,additionalProperties:{type:'string',minLength:1}},request_title:{type:'string'}},['expected_commit','request_key','reference_source','requested_copy']),annotations:{readOnlyHint:false,destructiveHint:false,idempotentHint:true,openWorldHint:true}},
 {name:'get_typography_delivery',description:'Read persistent isolated typography task and v3 contract; v2 data remains untrusted for v3, upgrade must be explicit. Returns task stage, history, artifact lineage, migration status. No native task writes.',inputSchema:schema({task_id:{type:'string',pattern:'^typo_[0-9a-f-]{36}$'}}),annotations:{readOnlyHint:true,openWorldHint:false}},
 {name:'upgrade_typography_contract',description:'Explicitly migrate one existing v2 request task to v3 IN PLACE using task_id and optimistic revision: keep same task_id, key, full v2 history, legacy artifacts, and native snapshot. Reset to new full-reference text-inventory gate; v2 artifacts are NOT v3 acceptance. No new task or D1 reset.',inputSchema:schema({task_id:{type:'string',pattern:'^typo_[0-9a-f-]{36}$'},expected_revision:{type:'integer',minimum:1},migration_reason:{type:'string',minLength:1,maxLength:2000}},['task_id','expected_revision','migration_reason']),annotations:{readOnlyHint:false,destructiveHint:false,idempotentHint:false,openWorldHint:false}},
 {name:'record_typography_stage',description:'Record exactly one v3 stage with real artifact identity, full text region coverage, actual AI generated transparent PNG evidence, Figma exact editable source and exported PNG, independent real-pixel AI-master-vs-Figma comparison with strict per-region metrics, and three-artifact delivery. Server enforces receipt consistency, not independent pixel inspection. FAIL returns to Figma, never completes.',inputSchema:schema({task_id:{type:'string',pattern:'^typo_[0-9a-f-]{36}$'},expected_revision:{type:'integer',minimum:1},stage:{type:'string',enum:STAGES},artifact:{type:'object',minProperties:1}},['task_id','expected_revision','stage','artifact']),annotations:{readOnlyHint:false,destructiveHint:false,idempotentHint:false,openWorldHint:true}}
]);
