import { createWorker as createBaseWorker } from './base-worker.mjs';
import {
  VERSION, TASK_CONTRACT, TASK_TOOLS,
  validateStartArgs, validateGetArgs, validateRecordArgs,
  createTask, applyStage
} from './typography-task.mjs';

const headers = {'Cache-Control':'private, no-store','Content-Type':'application/json; charset=utf-8'};
const json = (body,status=200) => new Response(JSON.stringify(body),{status,headers});
const toolResult = (id,value) => json({jsonrpc:'2.0',id,result:{content:[{type:'text',text:JSON.stringify(value)}],structuredContent:value,isError:false}});
const toolError = (id,message,status=409,code=-32030) => json({jsonrpc:'2.0',id,error:{code,message}},status);
const rowTask = row => row ? JSON.parse(row.payload) : null;

async function ensureTasks(db) {
  if (!db) throw new Error('REQUEST_TASK_STORAGE_UNAVAILABLE');
  await db.prepare(`CREATE TABLE IF NOT EXISTS typography_delivery_tasks (
    actor_id TEXT NOT NULL,
    task_id TEXT NOT NULL,
    request_key TEXT NOT NULL,
    revision INTEGER NOT NULL,
    stage TEXT NOT NULL,
    status TEXT NOT NULL,
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    PRIMARY KEY(actor_id,task_id),
    UNIQUE(actor_id,request_key)
  )`).run();
}

const canonical = value => JSON.stringify(value, (_k,v) => v && typeof v === 'object' && !Array.isArray(v) ? Object.fromEntries(Object.entries(v).sort(([a],[b])=>a.localeCompare(b))) : v);

function publicTask(task) {
  return {
    plugin_version: VERSION,
    task_contract: TASK_CONTRACT,
    task,
    completion_claim_allowed: task?.status === 'COMPLETE',
    native_state_write: false,
    native_task_lock_unchanged: true,
    s7_state_unchanged: true
  };
}

function internalRequest(request,rpc) {
  const h = new Headers(request.headers);
  h.delete('content-length');
  return new Request(request.url,{method:'POST',headers:h,body:JSON.stringify(rpc)});
}

async function readNative(base,request,env,id) {
  const rpc={jsonrpc:'2.0',id:'v020-native-'+String(id),method:'tools/call',params:{name:'get_current_workflow',arguments:{}}};
  const response=await base.fetch(internalRequest(request,rpc),env);
  let body;
  try{body=await response.json();}catch{throw new Error('NATIVE_WORKFLOW_READ_FAILED');}
  if(!response.ok || !body?.result?.structuredContent) {
    const e=new Error(body?.error?.message || 'NATIVE_WORKFLOW_READ_FAILED');
    e.status=response.status;
    throw e;
  }
  return body.result.structuredContent;
}

async function getByKey(db,actor,key) {
  return db.prepare('SELECT payload FROM typography_delivery_tasks WHERE actor_id=? AND request_key=?').bind(actor,key).first();
}
async function getById(db,actor,id) {
  return db.prepare('SELECT payload FROM typography_delivery_tasks WHERE actor_id=? AND task_id=?').bind(actor,id).first();
}
async function getLatest(db,actor) {
  return db.prepare('SELECT payload FROM typography_delivery_tasks WHERE actor_id=? ORDER BY updated_at DESC,task_id DESC LIMIT 1').bind(actor).first();
}

async function startTask({db,actor,args,native,now}) {
  await ensureTasks(db);
  const existing=rowTask(await getByKey(db,actor,args.request_key));
  if(existing) {
    const identical = existing.reference_source===args.reference_source &&
      canonical(existing.requested_copy)===canonical(args.requested_copy) &&
      existing.request_title===(args.request_title || '独立文字设计');
    if(!identical) throw new Error('REQUEST_KEY_CONFLICT_DIFFERENT_TASK');
    return {...publicTask(existing),idempotent_replay:true};
  }
  const nativeSnapshot={
    source:native.source,
    task_id:native.task_id,
    stage:native.stage,
    next_required_action:native.next_required_action,
    human_acceptance:native.acceptance?.human ?? 'UNKNOWN',
    snapshot_only:true
  };
  if(native.source?.commit !== args.expected_commit) throw new Error('HEAD_CHANGED_RELOAD_CURRENT_WORKFLOW');
  const task=createTask(args,nativeSnapshot,now,'typo_'+crypto.randomUUID());
  await db.prepare('INSERT INTO typography_delivery_tasks(actor_id,task_id,request_key,revision,stage,status,payload,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?)')
    .bind(actor,task.task_id,task.request_key,task.revision,task.stage,task.status,JSON.stringify(task),task.created_at,task.updated_at).run();
  const stored=rowTask(await getById(db,actor,task.task_id));
  if(!stored) throw new Error('REQUEST_TASK_PERSISTENCE_FAILED');
  return {...publicTask(stored),idempotent_replay:false};
}

async function recordStage({db,actor,args,now}) {
  await ensureTasks(db);
  const task=rowTask(await getById(db,actor,args.task_id));
  if(!task) throw new Error('TYPOGRAPHY_TASK_NOT_FOUND');
  if(task.revision!==args.expected_revision) throw new Error('REVISION_CONFLICT_RELOAD_TASK');
  const updated=applyStage(task,args.stage,args.artifact,now);
  await db.prepare('UPDATE typography_delivery_tasks SET revision=?,stage=?,status=?,payload=?,updated_at=? WHERE actor_id=? AND task_id=? AND revision=?')
    .bind(updated.revision,updated.stage,updated.status,JSON.stringify(updated),updated.updated_at,actor,args.task_id,args.expected_revision).run();
  const stored=rowTask(await getById(db,actor,args.task_id));
  if(!stored || stored.revision!==updated.revision) throw new Error('REVISION_CONFLICT_RELOAD_TASK');
  return publicTask(stored);
}

export function createWorker(options={}) {
  const base=createBaseWorker(options);
  const clock=options.clock || (()=>new Date().toISOString());
  return {async fetch(request,env){
    const url=new URL(request.url);
    if(url.pathname==='/' && request.method==='GET') return json({
      name:'刘先生·视觉设计工作流',
      version:VERSION,
      workflow:'参考文字提取 → 局部字稿 → Figma可编辑文字重建 → 实际独立审核 → 独立可编辑文字交付',
      target_delivery:TASK_CONTRACT.target_delivery,
      full_poster_substitution:false,
      native_state_write:false,
      s7_state_unchanged:true
    });

    if(url.pathname!=='/mcp' || request.method!=='POST') return base.fetch(request,env);
    if(Number(request.headers.get('content-length')||0)>65536) return json({error:'Request too large'},413);
    if(request.headers.get('origin') && request.headers.get('origin')!==url.origin) return json({error:'Cross-origin browser request denied'},403);
    if(!request.headers.get('content-type')?.toLowerCase().startsWith('application/json')) return base.fetch(request,env);

    let rpc;
    try{
      const raw=await request.clone().text();
      if(new TextEncoder().encode(raw).length>65536) return json({error:'Request too large'},413);
      rpc=JSON.parse(raw);
    }catch{return base.fetch(request,env);}

    if(rpc?.method==='initialize') {
      const response=await base.fetch(request,env);
      const body=await response.json();
      if(body?.result?.serverInfo) body.result.serverInfo.version=VERSION;
      return new Response(JSON.stringify(body),{status:response.status,headers:response.headers});
    }

    if(rpc?.method==='tools/list') {
      const response=await base.fetch(request,env);
      const body=await response.json();
      if(!response.ok || !body?.result?.tools) return new Response(JSON.stringify(body),{status:response.status,headers:response.headers});
      const tools=body.result.tools.map(t=>{
        if(t.name==='compile_transfer_plan') return {...t,description:t.description+' Legacy planner/structure-lock diagnostic only: it can never complete an isolated editable typography request. For that goal use start_typography_delivery.'};
        if(t.name==='validate_user_request_delivery') return {...t,description:t.description+' This remains a legacy full-poster/structure-edit receipt gate and cannot substitute for the v0.2.0 isolated typography task.'};
        if(t.name==='get_current_workflow') return {...t,description:t.description+' Native workflow context only; v0.2.0 request tasks are separate and must be read with get_typography_delivery.'};
        return t;
      });
      tools.push(...TASK_TOOLS);
      body.result.tools=tools;
      return new Response(JSON.stringify(body),{status:response.status,headers:response.headers});
    }

    const name=rpc?.method==='tools/call' ? rpc?.params?.name : null;
    if(!TASK_TOOLS.some(t=>t.name===name)) return base.fetch(request,env);

    if(rpc.jsonrpc!=='2.0' || !Object.hasOwn(rpc,'id') || !['string','number'].includes(typeof rpc.id) || (typeof rpc.id==='number' && !Number.isInteger(rpc.id))) return toolError(null,'Invalid JSON-RPC request',400,-32600);
    if(!rpc.params || typeof rpc.params!=='object' || Array.isArray(rpc.params) || !rpc.params.arguments || typeof rpc.params.arguments!=='object' || Array.isArray(rpc.params.arguments)) return toolError(rpc.id,'Invalid tool arguments',400,-32602);
    const actor=request.headers.get('oai-authenticated-user-id')?.trim();
    if(!actor) return toolError(rpc.id,'Authenticated user required',401,-32001);

    try{
      if(name==='start_typography_delivery') {
        const args=validateStartArgs(rpc.params.arguments);
        const native=await readNative(base,request,env,rpc.id);
        const value=await startTask({db:env?.DB,actor,args,native,now:clock()});
        return toolResult(rpc.id,value);
      }
      if(name==='get_typography_delivery') {
        const args=validateGetArgs(rpc.params.arguments);
        await ensureTasks(env?.DB);
        const task=rowTask(args.task_id ? await getById(env.DB,actor,args.task_id) : await getLatest(env.DB,actor));
        if(!task) return toolError(rpc.id,'TYPOGRAPHY_TASK_NOT_FOUND',404,-32004);
        return toolResult(rpc.id,publicTask(task));
      }
      if(name==='record_typography_stage') {
        const args=validateRecordArgs(rpc.params.arguments);
        const value=await recordStage({db:env?.DB,actor,args,now:clock()});
        return toolResult(rpc.id,value);
      }
    }catch(error){
      const invalid=/^(ARGUMENT|UNSUPPORTED|EXPECTED_COMMIT|REQUEST_KEY|REFERENCE_SOURCE_REQUIRED|REQUESTED_COPY|REQUEST_TITLE|TASK_ID_INVALID|EXPECTED_REVISION_INVALID|STAGE_INVALID|ARTIFACT_REQUIRED)/.test(error.message);
      const missing=error.message==='TYPOGRAPHY_TASK_NOT_FOUND';
      return toolError(rpc.id,error.message,invalid?400:(missing?404:(error.status||409)),invalid?-32602:-32030);
    }
  }};
}

export default createWorker();
