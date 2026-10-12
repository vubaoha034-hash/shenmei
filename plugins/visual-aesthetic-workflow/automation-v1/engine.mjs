// Additive pipeline engine for the EXISTING Liu visual workflow plugin.
// Does not call providers and cannot claim human approval. No native VPD lock writes.
export const ENGINE_VERSION = "automation-v1.0.0";
const HEX=/^[0-9a-f]{64}$/;
const OBJ=x=>x!==null&&typeof x==="object"&&!Array.isArray(x);
const TXT=(x,max=4000)=>typeof x==="string"&&x.trim().length>0&&x.length<=max;
export class PipelineError extends Error { constructor(code){super(code);this.code=code;} }
const req=(pass,code)=>{if(!pass)throw new PipelineError(code);};
export const STAGES=Object.freeze([
 "AWAIT_SOURCE","AWAIT_COST_APPROVAL","AWAIT_VISUAL_PROGRAM","ANALYSIS_IN_FLIGHT","RENDER_READY",
 "RENDER_IN_FLIGHT","AWAIT_TECH_AUDIT","AWAIT_PHOTO_HUMAN",
 "AWAIT_FIGMA","AWAIT_POSTER_AUDIT","AWAIT_POSTER_HUMAN",
 "COMPLETE","REJECTED","RECONCILE_REQUIRED"
]);
const copy=x=>JSON.parse(JSON.stringify(x));
const canon=x=>JSON.stringify(x,(_k,v)=>OBJ(v)?Object.fromEntries(Object.entries(v).sort(([a],[b])=>a.localeCompare(b))):v);
export function validateReference(r) {
 req(OBJ(r),"REFERENCE_REQUIRED");
 req(["THIRD_PARTY_REFERENCE","USER_OWNED_REFERENCE"].includes(r.role),"REFERENCE_ROLE_INVALID");
 req(HEX.test(r.sha256||""),"REFERENCE_SHA256_REQUIRED");
 req(TXT(r.asset_id,256),"REFERENCE_ASSET_ID_REQUIRED");
 req(["image/png","image/jpeg","image/webp"].includes(r.mime),"REFERENCE_MIME_INVALID");
 req(Number.isInteger(r.width)&&r.width>0&&Number.isInteger(r.height)&&r.height>0,"REFERENCE_DIMENSIONS_INVALID");
 req(["UNKNOWN","PERMISSIONED","USER_OWNED"].includes(r.rights),"REFERENCE_RIGHTS_STATUS_REQUIRED");
 return copy(r);
}
export function createPipeline(input,context) {
 req(OBJ(input)&&TXT(input.request_key,128),"REQUEST_KEY_REQUIRED");
 req(TXT(input.goal,1024),"GOAL_REQUIRED");
 req(OBJ(context)&&TXT(context.actor_id,256)&&TXT(context.job_id,128)&&TXT(context.now,64),"TRUSTED_CONTEXT_REQUIRED");
 req(Number.isInteger(input.max_generation_calls)&&input.max_generation_calls>=1&&input.max_generation_calls<=4,"GENERATION_BUDGET_INVALID");
 const ref=validateReference(input.reference);
 return {
  schema:"visual-image-automation/v1",engine_version:ENGINE_VERSION,
  job_id:context.job_id,owner_id:context.actor_id,request_key:input.request_key,
  reference:ref,goal:input.goal,ratio:input.ratio||"9:16",
  variant:input.variant||"IMAGE_PHOTOGRAPHY",pixel_policy:input.pixel_policy||"ALLOW_AUDITED_DERIVATIVE",
  max_generation_calls:input.max_generation_calls,used_generation_calls:0,
  revision:1,phase:"AWAIT_SOURCE",status:"IN_PROGRESS",events:[],
  prompt:null,program:null,render:null,photo_review:null,
  figma:null,poster_audit:null,poster_review:null,blocker:null,
  cost_authorization:null,created_at:context.now,updated_at:context.now
 };
}
export function compilePrompt(program,job) {
 req(OBJ(program)&&program.reference_sha256===job.reference.sha256,"PROGRAM_SOURCE_MISMATCH");
 req(program.actual_reference_pixels_inspected===true&&TXT(program.inspector,256),"PIXEL_INSPECTION_EVIDENCE_REQUIRED");
 const main=program.main_subject;
 req(TXT(main,1000),"MAIN_SUBJECT_REQUIRED");
 const variables=program.high_impact_variables;
 req(Array.isArray(variables)&&variables.length>=2&&variables.length<=8,"HIGH_IMPACT_VARIABLE_COUNT");
 variables.forEach(x=>req(TXT(x,300),"IMAGEABLE_VARIABLE_INVALID"));
 const avoids=program.avoid||[];
 req(Array.isArray(avoids)&&avoids.length<=4&&avoids.every(x=>TXT(x,250)),"AVOIDS_INVALID");
 const unique=xs=>Array.from(new Set(xs.map(s=>s.trim())));
 req(unique(variables).length===variables.length,"DUPLICATE_VISUAL_VARIABLE");
 const start="Create one original "+(job.variant==="IMAGE_PHOTOGRAPHY"?"photoreal photograph":"visual image")+" in "+job.ratio+". "+main.trim()+".";
 const line=unique(variables).join("; ")+".";
 const no=avoids.length?" Avoid: "+unique(avoids).join("; ")+".":"";
 const suffix=" Use the attached reference for visual structure, not as the output file. Do not imitate a photographer credit or watermark.";
 return {text:start+" "+line+no+suffix,source_sha256:job.reference.sha256,controls:variables.length,avoids:avoids.length,version:"vpd-compiler-compact-v1"};
}
const ACTOR={SOURCE_VERIFIED:"executor",ANALYSIS_RESERVED:"executor",PROGRAM_COMPILED:"executor",COST_AUTHORIZED:"human",RENDER_RESERVED:"executor",RENDER_COMPLETED:"executor",TECH_AUDIT:"executor",PHOTO_HUMAN_REVIEW:"human",FIGMA_COMPOSITE:"executor",POSTER_AUDIT:"executor",POSTER_HUMAN_REVIEW:"human",BLOCK:"executor",RESUME:"executor",RECONCILE:"executor",CORRECT_HUMAN_REVIEW:"human"};
const PHASE={SOURCE_VERIFIED:"AWAIT_SOURCE",ANALYSIS_RESERVED:"AWAIT_VISUAL_PROGRAM",PROGRAM_COMPILED:"ANALYSIS_IN_FLIGHT",COST_AUTHORIZED:"AWAIT_COST_APPROVAL",RENDER_RESERVED:"RENDER_READY",RENDER_COMPLETED:"RENDER_IN_FLIGHT",TECH_AUDIT:"AWAIT_TECH_AUDIT",PHOTO_HUMAN_REVIEW:"AWAIT_PHOTO_HUMAN",FIGMA_COMPOSITE:"AWAIT_FIGMA",POSTER_AUDIT:"AWAIT_POSTER_AUDIT",POSTER_HUMAN_REVIEW:"AWAIT_POSTER_HUMAN"};
export function advancePipeline(input,evt,ctx) {
 req(OBJ(input)&&input.schema==="visual-image-automation/v1","JOB_SCHEMA_INVALID");
 req(OBJ(evt)&&TXT(evt.id,128)&&TXT(evt.type,64)&&OBJ(evt.evidence),"EVENT_INVALID");
 req(OBJ(ctx)&&ctx.actor_id===input.owner_id&&TXT(ctx.now,64)&&["executor","human"].includes(ctx.actor_type),"UNAUTHORIZED_ACTOR");
 req(Object.hasOwn(ACTOR,evt.type),"UNKNOWN_ACTION");
 req(ACTOR[evt.type]===ctx.actor_type,"EVENT_ACTOR_TYPE_FORBIDDEN");
 req(Number.isInteger(evt.expected_revision)&&evt.expected_revision>=1,"REVISION_REQUIRED");
 const old=input.events.find(x=>x.id===evt.id);
 if(old){req(old.type===evt.type&&canon(old.evidence)===canon(evt.evidence),"IDEMPOTENCY_KEY_REUSED_WITH_DIFFERENT_PAYLOAD");return {...copy(input),idempotent:true};}
 req(evt.expected_revision===input.revision,"REVISION_CONFLICT");
 if(input.blocker&&!["BLOCK","RESUME"].includes(evt.type))req(false,"BLOCKER_MUST_BE_RESOLVED_EXPLICITLY");
 const j=copy(input),e=evt.evidence;
 if(!["BLOCK","RESUME","RECONCILE","CORRECT_HUMAN_REVIEW"].includes(evt.type))req(j.phase===PHASE[evt.type]||(["RENDER_COMPLETED","PROGRAM_COMPILED"].includes(evt.type)&&j.phase==="RECONCILE_REQUIRED"),"STAGE_ORDER_VIOLATION_EXPECTED_"+j.phase);
 switch(evt.type){
 case "SOURCE_VERIFIED":
   req(e.checked_actual_bytes===true&&e.actual_sha256===j.reference.sha256,"SOURCE_BYTES_UNVERIFIED");
   req(e.actual_mime===j.reference.mime&&e.width===j.reference.width&&e.height===j.reference.height,"SOURCE_FORMAT_MISMATCH");
   if(e.asset_id!==undefined){req(TXT(e.asset_id,256),"SOURCE_PRIVATE_ASSET_ID_INVALID");j.reference.asset_id=e.asset_id;}
   j.phase="AWAIT_COST_APPROVAL";break;
 case "ANALYSIS_RESERVED":
   req(e.reference_sha256===j.reference.sha256&&TXT(e.attempt_id,128)&&TXT(e.model,128),"ANALYSIS_BINDING_MISSING");
   req(e.model===j.cost_authorization?.vision_model,"UNAUTHORIZED_VISION_MODEL");
   j.analysis={attempt_id:e.attempt_id,source_sha256:e.reference_sha256,status:"IN_FLIGHT_UNCERTAIN",reserved_at:ctx.now};
   j.phase="ANALYSIS_IN_FLIGHT";break;
 case "PROGRAM_COMPILED":
   req(j.analysis?.attempt_id===e.analysis_attempt_id&&e.source_input_sha256===j.reference.sha256&&TXT(e.provider_response_id,256),"VISION_PROVIDER_RECEIPT_REQUIRED");
   j.prompt=compilePrompt(e.program,j);j.program=copy(e.program);j.analysis={...j.analysis,status:"COMPLETE",provider_response_id:e.provider_response_id};j.phase="RENDER_READY";j.status="IN_PROGRESS";break;
 case "COST_AUTHORIZED":
   req(e.explicit_user_approval===true&&e.approved_max_calls>=1&&e.approved_max_calls<=j.max_generation_calls&&e.approved_vision_calls===1&&TXT(e.vision_model,128),"COST_APPROVAL_REQUIRED");
   req(TXT(e.provider,128)&&TXT(e.model,128)&&e.provider_budget_type==="SEPARATE_PAID_API","BILLING_SCOPE_MUST_BE_EXPLICIT");
   j.cost_authorization={provider:e.provider,model:e.model,vision_model:e.vision_model,max_calls:e.approved_max_calls,approved_vision_calls:1,approved_at:ctx.now};
   j.phase="AWAIT_VISUAL_PROGRAM";break;
 case "RENDER_RESERVED":
   req(j.cost_authorization&&j.used_generation_calls<j.cost_authorization.max_calls,"GENERATION_QUOTA_EXHAUSTED");
   req(TXT(e.attempt_id,128)&&e.reference_sha256===j.reference.sha256&&e.prompt===j.prompt.text,"REQUEST_REFERENCE_OR_PROMPT_CHANGED");
   j.used_generation_calls++;
   j.render={attempt_id:e.attempt_id,prompt:e.prompt,source_sha256:e.reference_sha256,status:"IN_FLIGHT_UNCERTAIN",reserved_at:ctx.now};
   j.phase="RENDER_IN_FLIGHT";break;
 case "RENDER_COMPLETED":
   req(j.render?.attempt_id===e.attempt_id,"RENDER_ATTEMPT_MISMATCH");
   req(e.actual_output_bytes_verified===true&&HEX.test(e.output_sha256||"")&&TXT(e.output_asset_id,256),"RENDER_OUTPUT_UNVERIFIED");
   req(e.request_reference_sha256===j.reference.sha256&&TXT(e.provider_response_id,256),"REFERENCE_BINDING_RECEIPT_MISSING");
   req(Number.isInteger(e.width)&&e.width>0&&Number.isInteger(e.height)&&e.height>0,"GENERATED_DIMENSIONS_INVALID");
   j.render={...j.render,status:"COMPLETED",provider_response_id:e.provider_response_id,output_sha256:e.output_sha256,output_asset_id:e.output_asset_id,output_bytes:e.output_bytes,width:e.width,height:e.height,completed_at:ctx.now};
   j.phase="AWAIT_TECH_AUDIT";j.status="IN_PROGRESS";break;
 case "TECH_AUDIT":
   req(j.render?.status==="COMPLETED"&&e.image_sha256===j.render.output_sha256&&e.independent_bytes_read===true,"TECH_AUDIT_SOURCE_MISSING");
   req(e.actual_dimensions_checked===true&&e.no_unrecorded_derivative===true,"TECH_AUDIT_INCOMPLETE");
   j.technical_audit=copy(e);
   if(e.hard_fail===true){j.phase="REJECTED";j.status="FAILED_TECH_AUDIT";}
   else {j.phase="AWAIT_PHOTO_HUMAN";}break;
 case "PHOTO_HUMAN_REVIEW":
   req(e.image_sha256===j.render?.output_sha256&&["APPROVE","REJECT"].includes(e.verdict),"HUMAN_PHOTO_ASSET_OR_VERDICT_INVALID");
   j.photo_review={...copy(e),recorded_at:ctx.now};
   j.phase=e.verdict==="APPROVE"?"AWAIT_FIGMA":"REJECTED";
   if(e.verdict==="REJECT")j.status="REJECTED_BY_USER";
   break;
 case "FIGMA_COMPOSITE":
   req(j.photo_review?.verdict==="APPROVE"&&e.source_image_sha256===j.render.output_sha256,"PHOTO_APPROVAL_REQUIRED");
   req(e.native_layers_verified===true&&e.photo_background_original===true&&e.approved_lettering_reused===true,"FIGMA_NATIVE_EVIDENCE_MISSING");
   req(TXT(e.file_key,128)&&TXT(e.frame_id,128)&&HEX.test(e.export_sha256||""),"FIGMA_EXPORT_IDENTIFIERS_REQUIRED");
   j.figma=copy(e);j.phase="AWAIT_POSTER_AUDIT";break;
 case "POSTER_AUDIT":
   req(e.export_sha256===j.figma?.export_sha256&&e.independent_export_bytes_read===true,"INDEPENDENT_POSTER_PIXEL_AUDIT_REQUIRED");
   req(e.photo_fidelity_pass===true&&e.native_editable_layers_pass===true&&e.copy_correct===true,"POSTER_AUDIT_FAIL");
   j.poster_audit=copy(e);j.phase="AWAIT_POSTER_HUMAN";break;
 case "POSTER_HUMAN_REVIEW":
   req(e.export_sha256===j.figma?.export_sha256&&["APPROVE","REJECT"].includes(e.verdict),"POSTER_HUMAN_ASSET_OR_VERDICT_INVALID");
   j.poster_review={...copy(e),recorded_at:ctx.now};
   j.phase=e.verdict==="APPROVE"?"COMPLETE":"REJECTED";
   j.status=e.verdict==="APPROVE"?"COMPLETE":"REJECTED_BY_USER";break;
 case "BLOCK":
   req(TXT(e.reason,512),"BLOCK_REASON_REQUIRED");j.blocker={reason:e.reason,phase:j.phase,at:ctx.now};break;
 case "RESUME":
   req(j.blocker&&e.proof_of_resolution===true&&TXT(e.resolution_receipt,512),"BLOCKER_RESOLUTION_EVIDENCE_REQUIRED");
   j.blocker=null;break;
 case "RECONCILE":
   req((j.phase==="RENDER_IN_FLIGHT"&&j.render?.status==="IN_FLIGHT_UNCERTAIN")||(j.phase==="ANALYSIS_IN_FLIGHT"&&j.analysis?.status==="IN_FLIGHT_UNCERTAIN"),"RECONCILE_ONLY_IN_FLIGHT");
   req(e.attempt_id===(j.phase==="RENDER_IN_FLIGHT"?j.render.attempt_id:j.analysis.attempt_id),"RECONCILE_ATTEMPT_MISMATCH");
   if(e.outcome==="UNKNOWN"){j.phase="RECONCILE_REQUIRED";j.status="NO_AUTOMATIC_REROLL";}
   else req(false,"RECONCILE_WITH_REAL_PROVIDER_RECEIPT_REQUIRED");break;
 case "CORRECT_HUMAN_REVIEW":
   req(TXT(e.supersedes_event_id,128)&&TXT(e.reason,512)&&e.corrected_asset_sha256===j.render?.output_sha256,"CORRECTION_IDENTITY_INVALID");
   req(j.events.some(x=>x.id===e.supersedes_event_id&&x.type==="PHOTO_HUMAN_REVIEW"),"OLD_HUMAN_REVIEW_NOT_FOUND");
   req(["APPROVE","REJECT"].includes(e.corrected_verdict),"CORRECTED_VERDICT_INVALID");
   j.photo_review={verdict:e.corrected_verdict,corrects:e.supersedes_event_id,recorded_at:ctx.now,image_sha256:e.corrected_asset_sha256};
   j.phase=j.figma?"RECONCILE_REQUIRED":(e.corrected_verdict==="APPROVE"?"AWAIT_FIGMA":"REJECTED");
   j.status="REVIEW_CORRECTED";break;
 }
 j.events.push({id:evt.id,type:evt.type,evidence:copy(evt.evidence),recorded_at:ctx.now,revision:j.revision+1});
 j.revision++;j.updated_at=ctx.now;return j;
}
export function nextAutomaticAction(job) {
 const map={AWAIT_SOURCE:"READ_SOURCE_BYTES_AND_VERIFY_SHA256",AWAIT_COST_APPROVAL:"WAIT_USER_BILLING_APPROVAL_BEFORE_PAID_VISION_OR_IMAGE",AWAIT_VISUAL_PROGRAM:"RESERVE_VISION_CALL_ONCE_AND_ANALYZE",ANALYSIS_IN_FLIGHT:"RECONCILE_EXISTING_VISION_CALL_ONLY",RENDER_READY:"RESERVE_AND_CALL_GENERATOR_ONCE",RENDER_IN_FLIGHT:"RECONCILE_EXISTING_PROVIDER_ATTEMPT_ONLY",AWAIT_TECH_AUDIT:"READ_GENERATED_BYTES_AND_CHECK",AWAIT_PHOTO_HUMAN:"WAIT_HUMAN_PHOTO_VERDICT",AWAIT_FIGMA:"COMPOSE_FIGMA_WITH_LOCKED_PHOTO",AWAIT_POSTER_AUDIT:"INDEPENDENT_EXPORT_AND_PIXEL_AUDIT",AWAIT_POSTER_HUMAN:"WAIT_HUMAN_POSTER_VERDICT",COMPLETE:"NONE_COMPLETE",REJECTED:"STOP_AND_PRESERVE_EVIDENCE",RECONCILE_REQUIRED:"STOP_UNTIL_EXISTING_ATTEMPT_RECONCILED"};
 return {action:job.blocker?"BLOCKED_UNTIL_RESUME":(map[job.phase]||"UNKNOWN"),phase:job.phase,automatic:!job.blocker&&!["AWAIT_COST_APPROVAL","AWAIT_PHOTO_HUMAN","AWAIT_POSTER_HUMAN","REJECTED","COMPLETE","RECONCILE_REQUIRED"].includes(job.phase),blocker:job.blocker};
}
