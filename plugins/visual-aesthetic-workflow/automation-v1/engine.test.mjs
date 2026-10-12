import test from "node:test";
import assert from "node:assert/strict";
import {createPipeline,advancePipeline,compilePrompt,nextAutomaticAction} from "./engine.mjs";
import {inspectImage,sha256,putImmutable,readImmutable,assertAdapterReady} from "./openai-image-adapter.mjs";

const digest="a".repeat(64),output="b".repeat(64),poster="c".repeat(64);
const ref={role:"THIRD_PARTY_REFERENCE",sha256:digest,asset_id:"ref-001",mime:"image/png",width:709,height:1064,rights:"UNKNOWN"};
const clock="2026-10-12T00:00:00Z";
const ctx=(who="executor")=>({actor_id:"user-private",actor_type:who,now:clock});
const job=()=>createPipeline({request_key:"test_automated_vpd",goal:"new photograph",max_generation_calls:1,reference:ref},{actor_id:"user-private",job_id:"job-unique-0001",now:clock});
const ev=(j,type,evidence,who="executor",id="")=>advancePipeline(j,{id:id||"action_"+j.revision+"_"+type,expected_revision:j.revision,type,evidence},ctx(who));
const program={reference_sha256:digest,actual_reference_pixels_inspected:true,inspector:"real-pixel-reader",main_subject:"A tiny car on a road above fog",high_impact_variables:["a quiet pale sky","left-turning narrow road","mist filling the valley"],avoid:["golden sunburst"]};
const sourceEvidence={checked_actual_bytes:true,actual_sha256:digest,actual_mime:"image/png",width:709,height:1064};
const paid={explicit_user_approval:true,approved_max_calls:1,approved_vision_calls:1,vision_model:"vision-approved",provider:"OpenAI API",model:"image-approved",provider_budget_type:"SEPARATE_PAID_API"};
function beforeRender(){let j=job();j=ev(j,"SOURCE_VERIFIED",sourceEvidence);j=ev(j,"COST_AUTHORIZED",paid,"human");j=ev(j,"ANALYSIS_RESERVED",{reference_sha256:digest,attempt_id:"vision001",model:"vision-approved"});j=ev(j,"PROGRAM_COMPILED",{analysis_attempt_id:"vision001",source_input_sha256:digest,provider_response_id:"visionresp",program});return j}
function beforePhoto(){let j=beforeRender();j=ev(j,"RENDER_RESERVED",{attempt_id:"render001",reference_sha256:digest,prompt:j.prompt.text});j=ev(j,"RENDER_COMPLETED",{attempt_id:"render001",actual_output_bytes_verified:true,output_sha256:output,output_asset_id:"privateimg001",request_reference_sha256:digest,provider_response_id:"provider_req_1",width:941,height:1672,output_bytes:1934752});j=ev(j,"TECH_AUDIT",{image_sha256:output,independent_bytes_read:true,actual_dimensions_checked:true,no_unrecorded_derivative:true,hard_fail:false,exact_native_ratio:false});return j}
test("source identity is required and no web URL can substitute for bytes",()=>{
 assert.throws(()=>createPipeline({request_key:"q",goal:"photo",max_generation_calls:1,reference:{...ref,sha256:"WRONG"}},{actor_id:"user-private",job_id:"id",now:clock}),/REFERENCE_SHA256_REQUIRED/);
 assert.throws(()=>ev(job(),"PROGRAM_COMPILED",{program}),/STAGE_ORDER_VIOLATION/);
 assert.throws(()=>ev(job(),"SOURCE_VERIFIED",{...sourceEvidence,actual_sha256:output}),/SOURCE_BYTES_UNVERIFIED/);
});
test("cost is explicitly approved before even the paid vision call",()=>{
 let j=ev(job(),"SOURCE_VERIFIED",sourceEvidence);
 assert.equal(nextAutomaticAction(j).automatic,false);
 assert.throws(()=>ev(j,"ANALYSIS_RESERVED",{reference_sha256:digest,attempt_id:"one",model:"vision-approved"}),/STAGE_ORDER_VIOLATION/);
 assert.throws(()=>ev(j,"COST_AUTHORIZED",{...paid,approved_vision_calls:0},"human"),/COST_APPROVAL_REQUIRED/);
 assert.throws(()=>ev(j,"COST_AUTHORIZED",paid,"executor"),/EVENT_ACTOR_TYPE_FORBIDDEN/);
 j=ev(j,"COST_AUTHORIZED",paid,"human");assert.equal(j.phase,"AWAIT_VISUAL_PROGRAM");
});
test("vision call reservation prevents silent duplicate analysis",()=>{
 let j=ev(ev(job(),"SOURCE_VERIFIED",sourceEvidence),"COST_AUTHORIZED",paid,"human");
 j=ev(j,"ANALYSIS_RESERVED",{reference_sha256:digest,attempt_id:"vision001",model:"vision-approved"});
 assert.equal(j.phase,"ANALYSIS_IN_FLIGHT");
 assert.throws(()=>ev(j,"ANALYSIS_RESERVED",{reference_sha256:digest,attempt_id:"vision002",model:"vision-approved"}),/STAGE_ORDER_VIOLATION/);
 assert.throws(()=>ev(j,"PROGRAM_COMPILED",{analysis_attempt_id:"wrong",source_input_sha256:digest,provider_response_id:"abc",program}),/VISION_PROVIDER_RECEIPT_REQUIRED/);
 j=ev(j,"PROGRAM_COMPILED",{analysis_attempt_id:"vision001",source_input_sha256:digest,provider_response_id:"visionresp",program});
 assert.equal(j.phase,"RENDER_READY");
 assert.ok(j.prompt.text.includes("left-turning narrow road"));
});
test("same event id is idempotent, same id with different content is rejected",()=>{
 const original=job(),e={id:"same_action",type:"SOURCE_VERIFIED",expected_revision:1,evidence:sourceEvidence};
 let once=advancePipeline(original,e,ctx());
 let twice=advancePipeline(once,e,ctx());
 assert.equal(twice.idempotent,true);assert.equal(twice.revision,once.revision);
 assert.throws(()=>advancePipeline(once,{...e,evidence:{...sourceEvidence,width:800}},ctx()),/IDEMPOTENCY_KEY_REUSED/);
});
test("render attempt reserves quota before calling provider and no reroll follows uncertainty",()=>{
 let j=beforeRender();j=ev(j,"RENDER_RESERVED",{attempt_id:"render001",reference_sha256:digest,prompt:j.prompt.text});
 assert.equal(j.used_generation_calls,1);
 assert.throws(()=>ev(j,"RENDER_RESERVED",{attempt_id:"render002",reference_sha256:digest,prompt:j.prompt.text}),/STAGE_ORDER_VIOLATION/);
 j=ev(j,"RECONCILE",{attempt_id:"render001",outcome:"UNKNOWN"});
 assert.equal(j.phase,"RECONCILE_REQUIRED");
 assert.equal(nextAutomaticAction(j).automatic,false);
 assert.throws(()=>ev(j,"RENDER_RESERVED",{attempt_id:"another",reference_sha256:digest,prompt:j.prompt.text}),/STAGE_ORDER_VIOLATION/);
 j=ev(j,"RENDER_COMPLETED",{attempt_id:"render001",actual_output_bytes_verified:true,output_sha256:output,output_asset_id:"same-old-result",request_reference_sha256:digest,provider_response_id:"confirmed-after-reconcile",width:941,height:1672});
 assert.equal(j.phase,"AWAIT_TECH_AUDIT");
});
test("no auto approval: both photographic and final poster human evidence are mandatory",()=>{
 let j=beforePhoto();assert.equal(j.phase,"AWAIT_PHOTO_HUMAN");
 assert.equal(nextAutomaticAction(j).automatic,false);
 assert.throws(()=>ev(j,"PHOTO_HUMAN_REVIEW",{image_sha256:output,verdict:"APPROVE"}),/EVENT_ACTOR_TYPE_FORBIDDEN/);
 assert.throws(()=>ev(j,"PHOTO_HUMAN_REVIEW",{image_sha256:digest,verdict:"APPROVE"},"human"),/HUMAN_PHOTO_ASSET_OR_VERDICT_INVALID/);
 j=ev(j,"PHOTO_HUMAN_REVIEW",{image_sha256:output,verdict:"APPROVE"},"human");assert.equal(j.phase,"AWAIT_FIGMA");
 assert.throws(()=>ev(j,"FIGMA_COMPOSITE",{source_image_sha256:output,native_layers_verified:false}),/FIGMA_NATIVE_EVIDENCE_MISSING/);
 j=ev(j,"FIGMA_COMPOSITE",{source_image_sha256:output,native_layers_verified:true,photo_background_original:true,approved_lettering_reused:true,file_key:"existingFigmaFile",frame_id:"55:2",export_sha256:poster});
 assert.equal(j.phase,"AWAIT_POSTER_AUDIT");
 assert.throws(()=>ev(j,"POSTER_AUDIT",{export_sha256:poster,independent_export_bytes_read:false}),/INDEPENDENT_POSTER_PIXEL_AUDIT_REQUIRED/);
 j=ev(j,"POSTER_AUDIT",{export_sha256:poster,independent_export_bytes_read:true,photo_fidelity_pass:true,native_editable_layers_pass:true,copy_correct:true});
 assert.equal(j.phase,"AWAIT_POSTER_HUMAN");
 j=ev(j,"POSTER_HUMAN_REVIEW",{export_sha256:poster,verdict:"APPROVE"},"human");
 assert.equal(j.phase,"COMPLETE");assert.equal(j.status,"COMPLETE");
});
test("a user correction supersedes review and stops unsafe downstream progress",()=>{
 let j=beforePhoto();j=ev(j,"PHOTO_HUMAN_REVIEW",{image_sha256:output,verdict:"APPROVE"},"human","approval_old");
 j=ev(j,"CORRECT_HUMAN_REVIEW",{supersedes_event_id:"approval_old",corrected_asset_sha256:output,corrected_verdict:"REJECT",reason:"I mistook download order for X/Y"},"human");
 assert.equal(j.phase,"REJECTED");assert.equal(j.photo_review.verdict,"REJECT");assert.equal(j.events.some(x=>x.id==="approval_old"),true);
});
test("a blocker forbids progress until explicit evidence-backed RESUME",()=>{
 let j=job();j=ev(j,"BLOCK",{reason:"connector egress denied"});assert.equal(nextAutomaticAction(j).automatic,false);
 assert.throws(()=>ev(j,"SOURCE_VERIFIED",sourceEvidence),/BLOCKER_MUST_BE_RESOLVED/);
 assert.throws(()=>ev(j,"RESUME",{proof_of_resolution:false,resolution_receipt:"still broken"}),/BLOCKER_RESOLUTION_EVIDENCE_REQUIRED/);
 j=ev(j,"RESUME",{proof_of_resolution:true,resolution_receipt:"stable source connector readback"});
 assert.equal(j.blocker,null);
 j=ev(j,"SOURCE_VERIFIED",sourceEvidence);assert.equal(j.phase,"AWAIT_COST_APPROVAL");
});
test("do not make an inflexible one-to-three sentence or short prompt universal rule",()=>{
 let j=job(),many={...program,high_impact_variables:["a","b","c","d","e","f","g","h"]};
 assert.ok(compilePrompt(many,j).controls===8);
 assert.throws(()=>compilePrompt({...many,high_impact_variables:[...many.high_impact_variables,"i"]},j),/HIGH_IMPACT_VARIABLE_COUNT/);
 assert.throws(()=>compilePrompt({...many,reference_sha256:output},j),/PROGRAM_SOURCE_MISMATCH/);
});
test("private storage requires explicit R2 binding and raw readback digest",async()=>{
 const p=new Uint8Array(33);p.set([137,80,78,71,13,10,26,10]);p[18]=1;p[22]=1;const sha=await sha256(p);const s=new Map();
 const store={async put(k,v){s.set(k,new Uint8Array(v))},async get(k){const v=s.get(k);return v?{arrayBuffer:async()=>v.buffer.slice(v.byteOffset,v.byteOffset+v.byteLength)}:null}};
 assert.deepEqual(inspectImage(p),{mime:"image/png",width:256,height:256,bytes:33});
 const saved=await putImmutable(store,"safeuser001","safejob001",p,sha);
 assert.equal(saved.readback_verified,true);
 const re=await readImmutable(store,"safeuser001",saved.asset_id,sha);
 assert.equal(re.sha256,sha);assert.equal(re.bytes.length,p.length);
 await assert.rejects(readImmutable(store,"wrongowner",saved.asset_id,sha),/ASSET_ACCESS_INVALID/);
 assert.throws(()=>assertAdapterReady({}),/OPENAI_KEY_NOT_CONFIGURED/);
});

