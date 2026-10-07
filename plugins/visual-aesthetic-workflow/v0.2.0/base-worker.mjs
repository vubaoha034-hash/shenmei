import { createCore, SOURCE, TOOLS, sha256, validateRpcRequest, PROTOCOL_VERSIONS, negotiatedProtocol } from './core.mjs';

const headers = { 'Cache-Control': 'private, no-store', 'Content-Type': 'application/json; charset=utf-8' };
const json = (body, status=200) => new Response(body === null ? null : JSON.stringify(body), {status, headers});
const encodePath = path => path.split('/').map(encodeURIComponent).join('/');
export function githubAdapters(fetcher=fetch) {
  async function checked(url, limit=1500000) {
    const response = await fetcher(url, {headers:{Accept:'application/vnd.github+json','User-Agent':'liu-visual-workflow/0.1.5'}, cache:'no-store', signal:AbortSignal.timeout(15000)});
    if (!response.ok) throw new Error(`GitHub read unavailable (${response.status}); no authoritative state changed`);
    if (Number(response.headers.get('content-length') || 0)>limit) throw new Error('Repository response exceeds bounded limit');
    const bytes = new Uint8Array(await response.arrayBuffer());
    if (bytes.length>limit) throw new Error('Repository response exceeds bounded limit');
    return bytes;
  }
  return {
    resolveHead: async()=>JSON.parse(new TextDecoder().decode(await checked(`https://api.github.com/repos/${SOURCE.repository}/git/ref/heads/${encodeURIComponent(SOURCE.branch)}`))).object.sha,
    readFile: async({commit,path})=>checked(`https://raw.githubusercontent.com/${SOURCE.repository}/${commit}/${encodePath(path)}`),
  };
}
export async function saveIntake(db, validated, resolveHead) {
  if (!db) throw new Error('Durable feedback storage unavailable; feedback was not saved');
  const p=validated.validated_intake;
  if (await resolveHead()!==p.source.commit) throw new Error('HEAD_CHANGED_BEFORE_SAVE: reload the native workflow');
  await db.prepare('INSERT OR IGNORE INTO feedback_intakes (actor_id,idempotency_key,content_sha256,payload,recorded_at) VALUES (?,?,?,?,?)').bind(p.actor_id,p.idempotency_key,validated.content_sha256,JSON.stringify(p),p.recorded_at).run();
  const row=await db.prepare('SELECT content_sha256,payload,recorded_at FROM feedback_intakes WHERE actor_id=? AND idempotency_key=?').bind(p.actor_id,p.idempotency_key).first();
  if (!row || row.content_sha256!==validated.content_sha256) throw new Error('IDEMPOTENCY_CONFLICT: saved feedback differs; no existing record overwritten');
  return {...validated,validated_intake:JSON.parse(row.payload),persisted:true,durable_receipt:{idempotency_key:p.idempotency_key,content_sha256:row.content_sha256,recorded_at:row.recorded_at,authority:'NON_AUTHORITATIVE_PENDING_ROOT_RECONCILIATION'}};
}
const feedbackReadSchema={type:'object',properties:{idempotency_key:{type:'string',pattern:'^[A-Za-z0-9_-]{8,128}$'},cursor:{type:'string',maxLength:512},limit:{type:'integer',minimum:1,maximum:50}},additionalProperties:false};
function feedbackReadArgs(args) {
  if(Object.keys(args).some(key=>!Object.hasOwn(feedbackReadSchema.properties,key)))throw new Error('Unsupported feedback read argument');
  if(args.idempotency_key!==undefined && (typeof args.idempotency_key!=='string'|| !/^[A-Za-z0-9_-]{8,128}$/.test(args.idempotency_key)))throw new Error('Invalid idempotency key');
  if(args.limit!==undefined && (!Number.isInteger(args.limit)||args.limit<1||args.limit>50))throw new Error('Invalid page limit');
  if(args.idempotency_key!==undefined && (args.cursor!==undefined||args.limit!==undefined))throw new Error('Exact key lookup cannot include pagination arguments');
  let boundary=null;
  if(args.cursor!==undefined) {
    if(typeof args.cursor!=='string'||args.cursor.length>512)throw new Error('Invalid feedback cursor');
    try { boundary=JSON.parse(args.cursor); }catch{throw new Error('Invalid feedback cursor');}
    if(!Array.isArray(boundary)||boundary.length!==2||typeof boundary[0]!=='string'||boundary[0].length>64||!Number.isFinite(Date.parse(boundary[0]))||typeof boundary[1]!=='string'||!/^[A-Za-z0-9_-]{8,128}$/.test(boundary[1]))throw new Error('Invalid feedback cursor');
  }
  return {key:args.idempotency_key,boundary,limit:args.limit??50};
}
async function readIntakes(db, actor, options) {
  const columns='idempotency_key,payload,content_sha256,recorded_at';
  let rows;
  if(options.key!==undefined) {
    const row=await db.prepare(`SELECT ${columns} FROM feedback_intakes WHERE actor_id=? AND idempotency_key=?`).bind(actor,options.key).first();
    rows=row?[row]:[];
  }else if(options.boundary) {
    const [timestamp,key]=options.boundary;
    rows=(await db.prepare(`SELECT ${columns} FROM feedback_intakes WHERE actor_id=? AND (recorded_at < ? OR (recorded_at = ? AND idempotency_key < ?)) ORDER BY recorded_at DESC,idempotency_key DESC LIMIT ?`).bind(actor,timestamp,timestamp,key,options.limit+1).all()).results||[];
  }else {
    rows=(await db.prepare(`SELECT ${columns} FROM feedback_intakes WHERE actor_id=? ORDER BY recorded_at DESC,idempotency_key DESC LIMIT ?`).bind(actor,options.limit+1).all()).results||[];
  }
  const more=options.key===undefined && rows.length>options.limit;
  const page=more?rows.slice(0,options.limit):rows;
  const last=page.at(-1);
  return {intakes:page.map(r=>({idempotency_key:r.idempotency_key,payload:JSON.parse(r.payload),content_sha256:r.content_sha256,recorded_at:r.recorded_at})),next_cursor:more?JSON.stringify([last.recorded_at,last.idempotency_key]):null,authority:'NON_AUTHORITATIVE_PENDING_ROOT_RECONCILIATION',business_state_changed:false};
}
export function createWorker({fetcher=fetch, adapters=null, clock=()=>new Date().toISOString()}={}) {
  return { async fetch(request,env) {
    const url=new URL(request.url);
    if (url.pathname==='/' && request.method==='GET') return json({name:'刘先生·视觉设计工作流',version:'0.1.5',connection:'ChatGPT插件连接后调用；原生任务保持绑定，新参考使用user_request请求级草稿。'});
    if (url.pathname!=='/mcp') return json({error:'Not found'},404);
    if (request.method!=='POST') return new Response(null,{status:405,headers:{...headers,Allow:'POST'}});
    const protocolHeader=request.headers.get('MCP-Protocol-Version');
    if(protocolHeader!==null && !PROTOCOL_VERSIONS.includes(protocolHeader))return json({error:'Invalid or unsupported MCP-Protocol-Version'},400);
    if (request.headers.get('origin') && request.headers.get('origin')!==url.origin) return json({error:'Cross-origin browser request denied'},403);
    if (!request.headers.get('content-type')?.toLowerCase().startsWith('application/json')) return json({error:'JSON request required'},415);
    if (Number(request.headers.get('content-length') || 0)>65536) return json({error:'Request too large'},413);
    let rpc;
    try { const body=await request.text(); if(new TextEncoder().encode(body).length>65536)return json({error:'Request too large'},413); rpc=JSON.parse(body); }
    catch {return json({error:'Invalid JSON'},400);}
    const envelopeError=validateRpcRequest(rpc);
    if(envelopeError)return json({jsonrpc:'2.0',id:null,error:{code:-32600,message:envelopeError}},400);
    if(rpc.method==='initialize' && protocolHeader!==null && protocolHeader!==negotiatedProtocol(rpc.params?.protocolVersion))return json({jsonrpc:'2.0',id:rpc.id,error:{code:-32602,message:'Protocol header differs from initialization negotiation'}},400);
    // Only initialized notification is accepted without an id; it never accesses data.
    if(rpc.method==='notifications/initialized')return new Response(null,{status:202,headers});
    // Sites strips/provides these trusted headers and enforces the owner-private audience.
    // Identity is never accepted from JSON, query parameters or browser storage.
    const userId=request.headers.get('oai-authenticated-user-id');
    const identity=userId?.trim()?{userId}:null;
    const repo=adapters || githubAdapters(fetcher);
    const core=createCore({...repo,hash:sha256,authorize:async()=>!!identity,now:clock});
    if(rpc?.method==='tools/list') {
      const tools=TOOLS.map(t=>t.name==='prepare_human_feedback'?{...t,name:'save_human_feedback',description:'Save artwork-bound human feedback as append-only durable intake for Root reconciliation. Does not change the native task, review verdict or acceptance.',annotations:{...t.annotations,readOnlyHint:false,destructiveHint:false,idempotentHint:true}}:t);
      tools.push({name:'get_human_feedback',description:'Read this authenticated user\u2019s non-authoritative feedback by exact idempotency key or stable cursor pages. These are not business state.',inputSchema:feedbackReadSchema,annotations:{readOnlyHint:true,openWorldHint:false}});
      return json({jsonrpc:'2.0',id:rpc.id??null,result:{tools}});
    }
    if (rpc?.method==='tools/call' && rpc.params?.name==='get_human_feedback') {
      if(!identity)return json({jsonrpc:'2.0',id:rpc.id??null,error:{code:-32001,message:'Authenticated user required'}},401);
      let options;
      try{options=feedbackReadArgs(rpc.params.arguments??{});}catch(error){return json({jsonrpc:'2.0',id:rpc.id,error:{code:-32602,message:error.message}},400);}
      if(!env?.DB)return json({error:'Feedback storage unavailable'},503);
      try {
        const value=await readIntakes(env.DB,identity.userId,options);
        return json({jsonrpc:'2.0',id:rpc.id??null,result:{content:[{type:'text',text:JSON.stringify(value)}],structuredContent:value,isError:false}});
      }catch{return json({error:'Feedback read failed; no business state changed'},503);}
    }
    if(rpc.method==='tools/call' && !['get_current_workflow','compile_transfer_plan','validate_user_request_delivery','save_human_feedback'].includes(rpc.params.name))return json({jsonrpc:'2.0',id:rpc.id,error:{code:-32602,message:'Unknown public tool'}},400);
    const persist=rpc?.method==='tools/call' && rpc.params?.name==='save_human_feedback';
    if(persist)rpc={...rpc,params:{...rpc.params,name:'prepare_human_feedback'}};
    const response=await core.handle(rpc,identity);
    if(persist && response.body?.result?.structuredContent) {
      try {
        const value=await saveIntake(env?.DB,response.body.result.structuredContent,repo.resolveHead);
        response.body.result.structuredContent=value;
        response.body.result.content=[{type:'text',text:JSON.stringify(value)}];
      }catch(error){return json({jsonrpc:'2.0',id:rpc.id??null,error:{code:-32020,message:error.message}},409);}
    }
    const output=json(response.body,response.status);
    if(response.body?.result?.protocolVersion)output.headers.set('MCP-Protocol-Version',response.body.result.protocolVersion);
    return output;
  }};
}
export default createWorker();
