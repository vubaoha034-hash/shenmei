// Mount this as an additive wrapper around the CURRENT deployed v0.5 worker,
// after retrieving its real source. DO NOT replace existing v0.5 with old v0.3 code.
// No new Site/project, no native VPD lock mutations, no paid calls without consent.
import {createPipeline,advancePipeline,nextAutomaticAction} from "./engine.mjs";
import {assertAdapterReady,createOpenAIAdapter,readImmutable,putImmutable} from "./openai-image-adapter.mjs";

const toJSON=(o,status=200)=>new Response(JSON.stringify(o),{status,headers:{"content-type":"application/json; charset=utf-8","cache-control":"private, no-store"}});
const rpcResult=(id,v)=>toJSON({jsonrpc:"2.0",id,result:{content:[{type:"text",text:JSON.stringify(v)}],structuredContent:v,isError:false}});
const rpcError=(id,msg)=>toJSON({jsonrpc:"2.0",id,result:{content:[{type:"text",text:msg}],isError:true}});
const schema=(props={},required=[])=>({type:"object",properties:props,required,additionalProperties:false});
export const AUTO_TOOLS=Object.freeze([
{name:"get_visual_automation_contract",description:"Read add-on automation contract and whether SAME Site has paid API and private bytes store. Read-only; does not create images.",inputSchema:schema(),annotations:{readOnlyHint:true}},
{name:"start_visual_automation",description:"Create/recover one image workflow child using actual reference asset lineage. No generation, no native lock write.",inputSchema:schema({request_key:{type:"string"},goal:{type:"string"},reference:{type:"object"},max_generation_calls:{type:"integer",minimum:1,maximum:4}},["request_key","goal","reference","max_generation_calls"])},
{name:"get_visual_automation",description:"Read real job state, source hash, next action, generation budget and user approvals.",inputSchema:schema({job_id:{type:"string"}},["job_id"]),annotations:{readOnlyHint:true}},
{name:"run_visual_automation_once",description:"Execute at most one evidence-checked automatic stage. No blind retry or payment without separate authorization.",inputSchema:schema({job_id:{type:"string"},expected_revision:{type:"integer",minimum:1}},["job_id","expected_revision"])}
]);
const assert=(x,msg)=>{if(!x)throw new Error(msg)};
async function ensure(db){
 assert(db?.prepare,"D1_NOT_CONFIGURED");
 await db.prepare("CREATE TABLE IF NOT EXISTS visual_image_automation_v1(actor_id TEXT NOT NULL, job_id TEXT NOT NULL, request_key TEXT NOT NULL, revision INTEGER NOT NULL, payload TEXT NOT NULL, updated_at TEXT NOT NULL, PRIMARY KEY(actor_id,job_id), UNIQUE(actor_id,request_key))").run();
}
const row=r=>r?.payload?JSON.parse(r.payload):null;
const getJob=async(db,actor,id)=>row(await db.prepare("SELECT payload FROM visual_image_automation_v1 WHERE actor_id=? AND job_id=?").bind(actor,id).first());
const byKey=async(db,actor,key)=>row(await db.prepare("SELECT payload FROM visual_image_automation_v1 WHERE actor_id=? AND request_key=?").bind(actor,key).first());
async function saveCAS(db,actor,old,updated){
 const r=await db.prepare("UPDATE visual_image_automation_v1 SET revision=?,payload=?,updated_at=? WHERE actor_id=? AND job_id=? AND revision=?").bind(updated.revision,JSON.stringify(updated),updated.updated_at,actor,old.job_id,old.revision).run();
 assert(r?.meta?.changes===1,"CONCURRENT_REVISION_CONFLICT_RELOAD");return updated;
}
const ownerKey=(actor)=>{let s=actor.replace(/[^a-zA-Z0-9_-]/g,"_");return ("user_"+s).slice(0,128)};
const asContext=(actor,now)=>({actor_id:actor,actor_type:"executor",now});
const ev=(j,type,e,now)=>advancePipeline(j,{id:"auto_"+j.job_id+"_"+j.revision+"_"+type,expected_revision:j.revision,type,evidence:e},asContext(j.owner_id,now));
function adapterStatus(env){
 try{return {...assertAdapterReady(env),status:"READY_FOR_PAID_PROVIDER_AFTER_USER_APPROVAL",figma_executor:"EXTERNAL_CONNECTED_TOOL_REQUIRED",human_approval:"NON_AUTOMATABLE"}}catch(e){return {status:"BLOCKED_MISSING_CAPABILITY",reason:e.message,online_deployed:false}};
}
async function runStage({job,env,db,actor,now}){
 const action=nextAutomaticAction(job);if(!action.automatic)return {job,next:action,ran:false};
 const config=adapterStatus(env);if(config.status==="BLOCKED_MISSING_CAPABILITY")return {job,next:action,ran:false,blocked:config.reason};
 const provider=createOpenAIAdapter(env);
 const owner=ownerKey(actor);
 if(job.phase==="AWAIT_SOURCE"){
  const v=await readImmutable(env.VISUAL_ASSETS,owner,job.reference.asset_id,job.reference.sha256);
  const updated=ev(job,"SOURCE_VERIFIED",{checked_actual_bytes:true,actual_sha256:v.sha256,actual_mime:v.mime,width:v.width,height:v.height},now);
  return {job:await saveCAS(db,actor,job,updated),next:nextAutomaticAction(updated),ran:true};
 }
 if(job.phase==="AWAIT_VISUAL_PROGRAM"){
  const source=await readImmutable(env.VISUAL_ASSETS,owner,job.reference.asset_id,job.reference.sha256);
  // Reserve the paid analysis before network egress. Uncertain outcomes are never retried automatically.
  let reserved=ev(job,"ANALYSIS_RESERVED",{attempt_id:"vision_"+job.job_id,reference_sha256:job.reference.sha256,model:job.cost_authorization.vision_model},now);
  await saveCAS(db,actor,job,reserved);
  try{
   const out=await provider.analyze({referenceBytes:source.bytes,referenceSha256:job.reference.sha256,goal:job.goal});
   const fresh=await getJob(db,actor,job.job_id);assert(fresh.revision===reserved.revision,"CONCURRENT_VISION_STATE_CHANGED");
   const updated=ev(fresh,"PROGRAM_COMPILED",{analysis_attempt_id:reserved.analysis.attempt_id,source_input_sha256:source.sha256,provider_response_id:out.request_id,program:out.program},now);
   return {job:await saveCAS(db,actor,fresh,updated),next:nextAutomaticAction(updated),ran:true};
  }catch(e){return {job:reserved,next:nextAutomaticAction(reserved),ran:true,blocked:"VISION_PROVIDER_OUTCOME_UNCERTAIN_NO_AUTOMATIC_REPEAT"}}
 }
 if(job.phase==="RENDER_READY"){
  const source=await readImmutable(env.VISUAL_ASSETS,owner,job.reference.asset_id,job.reference.sha256);
  let reserved=ev(job,"RENDER_RESERVED",{attempt_id:"render_"+job.job_id,reference_sha256:source.sha256,prompt:job.prompt.text},now);
  await saveCAS(db,actor,job,reserved);
  try{
   const out=await provider.render({referenceBytes:source.bytes,referenceSha256:source.sha256,prompt:job.prompt.text});
   const stored=await putImmutable(env.VISUAL_ASSETS,owner,job.job_id,out.bytes,out.output_sha256);
   const fresh=await getJob(db,actor,job.job_id);assert(fresh.revision===reserved.revision,"CONCURRENT_RENDER_STATE_CHANGED");
   const updated=ev(fresh,"RENDER_COMPLETED",{attempt_id:reserved.render.attempt_id,actual_output_bytes_verified:true,output_sha256:out.output_sha256,output_asset_id:stored.asset_id,request_reference_sha256:source.sha256,provider_response_id:out.provider_response_id,width:stored.width,height:stored.height,output_bytes:stored.bytes},now);
   return {job:await saveCAS(db,actor,fresh,updated),next:nextAutomaticAction(updated),ran:true};
  }catch(e){return {job:reserved,next:nextAutomaticAction(reserved),ran:true,blocked:"RENDER_PROVIDER_OR_ARCHIVE_OUTCOME_UNCERTAIN_NO_REROLL"}}
 }
 if(job.phase==="AWAIT_TECH_AUDIT"){
  const check=await readImmutable(env.VISUAL_ASSETS,owner,job.render.output_asset_id,job.render.output_sha256);
  const exact=(check.width*16===check.height*9),strict=job.pixel_policy==="STRICT_NATIVE_9_16";
  const updated=ev(job,"TECH_AUDIT",{image_sha256:check.sha256,independent_bytes_read:true,actual_dimensions_checked:true,exact_native_ratio:exact,no_unrecorded_derivative:true,hard_fail:strict&&!exact},now);
  return {job:await saveCAS(db,actor,job,updated),next:nextAutomaticAction(updated),ran:true};
 }
 return {job,next:action,ran:false,blocked:"EXTERNAL_FIGMA_EXECUTOR_OR_INDEPENDENT_AUDITOR_NOT_CONNECTED"};
}
export function extendExistingVisualWorker(existingWorker,{clock=()=>new Date().toISOString()}={}){
 assert(existingWorker&&typeof existingWorker.fetch==="function","EXISTING_WORKER_REQUIRED");
 return {async fetch(request,env,ctx){
  const url=new URL(request.url);
  if(url.pathname!=="/mcp"||request.method!=="POST")return existingWorker.fetch(request,env,ctx);
  const contentType=request.headers.get("content-type")||"";
  if(!contentType.startsWith("application/json"))return existingWorker.fetch(request,env,ctx);
  let rpc;try{const raw=await request.clone().text();if(raw.length>64000)return toJSON({error:"RPC_TOO_LARGE"},413);rpc=JSON.parse(raw)}catch{return existingWorker.fetch(request,env,ctx)}
  if(rpc.method==="tools/list"){
   const orig=await existingWorker.fetch(request,env,ctx);const body=await orig.json();
   if(!orig.ok||!Array.isArray(body?.result?.tools))return toJSON(body,orig.status);
   body.result.tools=[...body.result.tools.filter(t=>!AUTO_TOOLS.some(u=>u.name===t.name)),...AUTO_TOOLS];
   return toJSON(body);
  }
  if(rpc.method!=="tools/call"||!AUTO_TOOLS.some(t=>t.name===rpc?.params?.name))return existingWorker.fetch(request,env,ctx);
  const name=rpc.params.name,args=rpc.params.arguments||{},actor=request.headers.get("oai-authenticated-user-id")?.trim();
  if(!actor)return rpcError(rpc.id,"AUTHENTICATED_USER_REQUIRED");
  try{
   if(name==="get_visual_automation_contract")return rpcResult(rpc.id,{automation_version:"1.0.0",site_identity:"PRESERVE_EXISTING_SITE_AND_D1",capabilities:adapterStatus(env),automatic_stages:["source_bytes","paid_vision_after_consent","image_api_after_consent","private_archive","technical_png_check"],human_stages:["paid_api_consent","photo_aesthetic_review","poster_aesthetic_review"],external_stages:["figma_editable_composite","independent_export_pixels"],native_task_lock_write:false,background_unattended_guarantee:false});
   await ensure(env.DB);
   if(name==="start_visual_automation"){
    const prev=await byKey(env.DB,actor,args.request_key);
    if(prev){assert(prev.goal===args.goal&&prev.reference?.sha256===args.reference?.sha256,"REQUEST_KEY_ALREADY_USED_FOR_DIFFERENT_SOURCE");return rpcResult(rpc.id,{job:prev,next:nextAutomaticAction(prev),replayed:true})}
    const now=clock(),job=createPipeline(args,{actor_id:actor,job_id:"visual_"+crypto.randomUUID().replace(/-/g,""),now});
    await env.DB.prepare("INSERT INTO visual_image_automation_v1(actor_id,job_id,request_key,revision,payload,updated_at) VALUES(?,?,?,?,?,?)").bind(actor,job.job_id,job.request_key,job.revision,JSON.stringify(job),now).run();
    return rpcResult(rpc.id,{job,next:nextAutomaticAction(job),replayed:false});
   }
   assert(typeof args.job_id==="string","JOB_ID_REQUIRED");
   const job=await getJob(env.DB,actor,args.job_id);assert(job,"JOB_NOT_FOUND");
   if(name==="get_visual_automation")return rpcResult(rpc.id,{job,next:nextAutomaticAction(job)});
   if(name==="run_visual_automation_once"){
    assert(args.expected_revision===job.revision,"REVISION_CONFLICT");
    return rpcResult(rpc.id,await runStage({job,env,db:env.DB,actor,now:clock()}));
   }
  }catch(e){return rpcError(rpc.id,e?.message||"AUTOMATION_ERROR")}
  return rpcError(rpc.id,"UNKNOWN_AUTO_TOOL");
 }};
}

