import { readFileSync, writeFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { pathToFileURL } from 'node:url';
import { resolve, join } from 'node:path';
import assert from 'node:assert/strict';

const repo = resolve(process.cwd(), '../..');
const newDir = join(repo, 'plugins/visual-aesthetic-workflow/v0.1.1');
const oldDir = join(repo, 'plugins/visual-aesthetic-workflow');
const { createCore, PATHS, SOURCE } = await import(pathToFileURL(join(newDir, 'core.mjs')));
const { createCore: oldCore } = await import(pathToFileURL(join(oldDir, 'core.mjs')));
const { createCore: builtCore } = await import(pathToFileURL(resolve('build_copy/dist/server/core.mjs')));
const { createWorker: builtWorker, githubAdapters } = await import(pathToFileURL(resolve('build_copy/dist/server/index.js')));
const CURRENT = '3e6a5638c2af2bedcfd66d23fabf6aa7d35c957d';
const LEGACY = '4d128f7b44dc43163f021b5717f5e003ca70a323';
const ENTRY = 'continuity/vpd/codex_takeover_20261003/S7_FINAL_REUSE.md';
const identity = { userId: 'INDEPENDENT_LOCAL_TEST_IDENTITY_NO_PRODUCTION_AUTH' };
const hash = bytes => createHash('sha256').update(bytes).digest('hex');
const encode = value => Buffer.from(JSON.stringify(value));
const originals = new Map();
function gitBytes(commit, path) {
  const key = commit + ':' + path;
  if (!originals.has(key)) originals.set(key, execFileSync('git', ['show', key], { cwd: repo, maxBuffer: 2500000 }));
  return originals.get(key);
}
const native = () => Object.fromEntries(Object.entries({ lock: PATHS.lock, checkpoint: PATHS.checkpoint, adapter: PATHS.adapter }).map(([key, path]) => [key, JSON.parse(gitBytes(CURRENT, path))]));
function modified(transform) {
  const states = native();
  const extra = new Map();
  transform(states, extra);
  const lockBytes = encode(states.lock);
  for (const state of [states.checkpoint, states.adapter]) state.task_lock.sha256 = hash(lockBytes);
  return new Map([[PATHS.lock, lockBytes], [PATHS.checkpoint, encode(states.checkpoint)], [PATHS.adapter, encode(states.adapter)], ...extra]);
}
function fixture({ factory=createCore, commit=CURRENT, overrides=new Map(), heads=null, authorized=true }={}) {
  let headCalls=0;
  const reads=[];
  const adapters={
    resolveHead: async source => { assert.deepEqual(source, SOURCE); return heads ? heads[Math.min(headCalls++,heads.length-1)] : commit; },
    readFile: async input => { assert.equal(input.commit,commit); assert.equal(input.repository,SOURCE.repository); reads.push(input); return overrides.get(input.path) ?? gitBytes(input.commit,input.path); }
  };
  const core=factory({ ...adapters, authorize:async who=>authorized && who.userId===identity.userId });
  return { core, reads, adapters };
}
const request = (name='get_current_workflow', args={}) => ({jsonrpc:'2.0',id:1,method:'tools/call',params:{name,arguments:args}});
const cases=[];
const observations={};
async function check(name, operation) {
  try { const evidence=await operation(); cases.push({name,pass:true,...evidence}); }
  catch(error){cases.push({name,pass:false,error:error.message,stack:error.stack});}
}
async function rejection(options, status, pattern, who=identity, rpc=request()) {
  const f=fixture(options);const result=await f.core.handle(rpc,who);
  assert.equal(result.status,status,JSON.stringify(result));
  if(pattern)assert.match(result.body.error.message,pattern);
  return {status:result.status,error:result.body.error.message,read_count:f.reads.length};
}
function projection(value) {
  return {source:value.source,task_id:value.task_id,stage:value.stage,next_required_action:value.next_required_action,entry_path:value.entry.path,entry_text_sha256:hash(value.entry.text),artwork_sha256:value.artwork.sha256,acceptance:value.acceptance,capabilities:value.capabilities,evidence:value.evidence};
}
let current;
await check('original 0.1.0 rejects actual current native 350/372',()=>rejection({factory:oldCore},409,/Current reuse entry mismatch/));
await check('0.1.1 reads actual native three-file bound S7 entry',async()=>{
  const f=fixture();const r=await f.core.handle(request(),identity);assert.equal(r.status,200,JSON.stringify(r));current=r.body.result.structuredContent;
  const states=native();assert.equal(current.source.lock_revision,350);assert.equal(current.source.checkpoint_sequence,372);
  assert.equal(current.source.commit,CURRENT);assert.equal(current.entry.path,states.lock.codex_takeover.reuse_entry.path);
  assert.deepEqual(states.lock.codex_takeover.reuse_entry,states.adapter.workflow.current_bounded_delivery_entry);
  assert.equal(current.entry.path,ENTRY);assert.equal(current.entry.text,gitBytes(CURRENT,ENTRY).toString('utf8'));
  assert.equal(hash(gitBytes(CURRENT,ENTRY)),states.lock.codex_takeover.reuse_entry.sha256);
  assert.equal(current.source.native_lock_sha256,hash(gitBytes(CURRENT,PATHS.lock)));
  assert.equal(current.next_required_action,states.lock.next_required_action);assert.equal(current.next_required_action,'LIU_REVIEW_LIUXIANSHENG_CONTENT_TRANSFER');
  assert.equal(current.artwork.sha256,'ed03ba67ca82da6920e49ab44f42f73f112d8c9bc25b841cb47ebcfc7a583762');
  assert.equal(current.acceptance.human,'PENDING');assert.equal(current.acceptance.promotion_allowed,false);assert.equal(current.acceptance.whole_visual_system_complete,false);
  for(const key of ['image_generation','drive_pixels','figma_edit','independent_reviewer','business_state_write','training','scheduling'])assert.equal(current.capabilities[key],false);
  observations.current=projection(current);return{status:r.status,read_count:f.reads.length,all_reads_fixed_commit:f.reads.every(x=>x.commit===CURRENT)};
});
await check('0.1.1 retains actual legacy S4 344/366 fixed blobs',async()=>{
  const f=fixture({commit:LEGACY});const r=await f.core.handle(request(),identity);assert.equal(r.status,200,JSON.stringify(r));const v=r.body.result.structuredContent;
  assert.equal(v.entry.path,PATHS.entry);assert.equal(v.source.lock_revision,344);assert.equal(v.source.checkpoint_sequence,366);
  assert.equal(v.artwork.sha256,'ddb621ebf7e230279a1358b1b93ab9fcd55705b7e6ca99af8649aa3295ab1ca4');assert.equal(v.acceptance.promotion_allowed,false);
  observations.legacy=projection(v);return{status:r.status,read_count:f.reads.length};
});
await check('S7 entry altered bytes retain old SHA and are rejected',()=>rejection({overrides:new Map([[ENTRY,Buffer.concat([gitBytes(CURRENT,ENTRY),Buffer.from('\nTEST_ONLY_TAMPER')])]])},409,/EVIDENCE_HASH_MISMATCH/));
await check('coherent unknown entry with correct own SHA is rejected',()=>rejection({overrides:modified((s,x)=>{
  const path='continuity/vpd/TEST_ONLY_UNAUTHORIZED_ENTRY.md';const bytes=Buffer.from('TEST_ONLY_UNKNOWN');const ref={path,sha256:hash(bytes)};
  s.lock.codex_takeover.reuse_entry=ref;s.adapter.workflow.current_bounded_delivery_entry=ref;x.set(path,bytes);
})},409,/Current reuse entry mismatch/));
await check('allowed paths with mismatched native entry projections are rejected',()=>rejection({overrides:modified(s=>{s.adapter.workflow.current_bounded_delivery_entry={...s.lock.codex_takeover.reuse_entry,path:PATHS.entry};})},409,/Current reuse entry mismatch/));
await check('all mainline mirrors and lock hashes coherent but changed policy are rejected',()=>rejection({overrides:modified(s=>{for(const state of Object.values(s))state.mainline_lock.contract.sha256='b'.repeat(64);})},409,/MAINLINE_TAMPER/));
await check('coherent authority path traversal is rejected before external read',()=>rejection({overrides:modified(s=>{for(const state of Object.values(s))state.mainline_lock.authority.path='../TEST_ONLY_OUTSIDE.json';})},409,/Invalid repository evidence path/));
for(const [name,path] of [['checkpoint',PATHS.checkpoint],['adapter',PATHS.adapter]]){
  const value=JSON.parse(gitBytes(CURRENT,path));value.task_lock.sha256='c'.repeat(64);
  await check(name+' native lock hash mismatch is rejected',()=>rejection({overrides:new Map([[path,encode(value)]])},409,/STATE_BINDING_MISMATCH/));
}
await check('native project identity mismatch is rejected',()=>rejection({overrides:modified(s=>{s.checkpoint.project_id='TEST_ONLY_WRONG_PROJECT';})},409,/Native task identity mismatch/));
await check('native task identity mismatch is rejected',()=>rejection({overrides:modified(s=>{s.adapter.current_mainline.task_id='TEST_ONLY_WRONG_TASK';})},409,/Native stage\/status mismatch/));
await check('native next action mismatch is rejected',()=>rejection({overrides:modified(s=>{s.checkpoint.next_required_action='TEST_ONLY_START_ANOTHER_VERSION';})},409,/Native next-action mismatch/));
await check('HEAD drift after exact fixed snapshot is rejected',()=>rejection({heads:[CURRENT,LEGACY]},409,/HEAD_CHANGED_DURING_READ/));
await check('missing identity is rejected before reading native data',async()=>{const r=await rejection({},401,/Authenticated user identity required/,null);assert.equal(r.read_count,0);return r;});
await check('unauthorized identity is rejected before reading native data',async()=>{const r=await rejection({authorized:false},403,/User is not authorized/);assert.equal(r.read_count,0);return r;});
await check('body identity cannot override authorization',()=>rejection({},400,/Unsupported argument/,identity,request('get_current_workflow',{identity})));
await check('wrong expected commit is rejected before evidence reads',async()=>{const r=await rejection({},409,/HEAD_CHANGED/,identity,request('compile_transfer_plan',{expected_commit:LEGACY,reference_sha256:current.artwork.reference_sha256}));assert.equal(r.read_count,0);return r;});
await check('current transfer plan is non-authorizing and cannot promote acceptance',async()=>{
  const r=await fixture().core.handle(request('compile_transfer_plan',{expected_commit:CURRENT,reference_sha256:current.artwork.reference_sha256}),identity);assert.equal(r.status,200,JSON.stringify(r));const v=r.body.result.structuredContent;
  assert.equal(v.execution_authorized,false);assert.equal(v.status,'DRAFT_ROOT_SCOPE_CHECK_REQUIRED');assert.equal(v.gates.ai_is_not_human,true);assert.equal(v.gates.engineering_is_not_taste,true);
  return{status:r.status,execution_authorized:v.execution_authorized,status_value:v.status};
});
await check('built core is source byte-identical and actually reads S7',async()=>{
  assert.equal(hash(readFileSync(resolve('build_copy/dist/server/core.mjs'))),hash(readFileSync(join(newDir,'core.mjs'))));
  assert.equal(hash(readFileSync(resolve('build_copy/dist/server/index.js'))),hash(readFileSync(join(newDir,'worker.mjs'))));
  const r=await fixture({factory:builtCore}).core.handle(request(),identity);assert.equal(r.status,200,JSON.stringify(r));const v=r.body.result.structuredContent;assert.equal(v.entry.path,ENTRY);assert.equal(v.source.lock_revision,350);
  return{status:r.status,core_sha256:hash(readFileSync(resolve('build_copy/dist/server/core.mjs'))),worker_sha256:hash(readFileSync(resolve('build_copy/dist/server/index.js')))};
});
await check('built HTTP worker imports new core with initialization and homepage 0.1.1',async()=>{
  const f=fixture();const worker=builtWorker({adapters:f.adapters});
  const http=(rpc,auth=true)=>new Request('https://local-test.invalid/mcp',{method:'POST',headers:{'content-type':'application/json',...(auth?{'oai-authenticated-user-id':identity.userId}:{})},body:JSON.stringify(rpc)});
  const init=await worker.fetch(http({jsonrpc:'2.0',id:1,method:'initialize',params:{protocolVersion:'2025-06-18'}},false),{});assert.equal(init.status,200);assert.equal((await init.json()).result.serverInfo.version,'0.1.1');
  const home=await worker.fetch(new Request('https://local-test.invalid/'),{});assert.equal((await home.json()).version,'0.1.1');
  const r=await worker.fetch(http(request()),{});assert.equal(r.status,200);const body=await r.json();assert.equal(body.result.structuredContent.entry.path,ENTRY);assert.equal(body.result.structuredContent.source.checkpoint_sequence,372);
  assert.equal((await worker.fetch(http(request(),false),{})).status,401);
  return{status:r.status,initialize_version:'0.1.1',homepage_version:'0.1.1',scope:'LOCAL_TEST_HEADER_AND_ADAPTERS_ONLY_NOT_HOSTED_AUTH'};
});
await check('built github adapter preserves immutable raw URL and reports 0.1.1 User-Agent',async()=>{
  const calls=[];const adapter=githubAdapters(async(url,options)=>{calls.push({url,headers:options.headers,cache:options.cache});return new Response(gitBytes(CURRENT,ENTRY));});
  const bytes=await adapter.readFile({...SOURCE,commit:CURRENT,path:ENTRY});assert.equal(hash(bytes),hash(gitBytes(CURRENT,ENTRY)));
  assert.equal(calls[0].url,'https://raw.githubusercontent.com/'+SOURCE.repository+'/'+CURRENT+'/'+ENTRY);
  assert.equal(calls[0].headers['User-Agent'],'liu-visual-workflow/0.1.1');assert.equal(calls[0].cache,'no-store');return{scope:'MOCK_TRANSPORT_REAL_FIXED_BLOB_NO_NETWORK',calls};
});

const result={schema:'vpd-plugin-v011-independent-engineering-cases/v1',actual_context:'Retained prior S4 publication context; not an aesthetic cold review',current_commit:CURRENT,legacy_commit:LEGACY,total:cases.length,passed:cases.filter(x=>x.pass).length,failed:cases.filter(x=>!x.pass).length,cases,observations};
writeFileSync('INDEPENDENT_CASE_RESULTS.json',JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({total:result.total,passed:result.passed,failed:result.failed,current:observations.current,failures:cases.filter(x=>!x.pass)},null,2));
if(result.failed)process.exitCode=1;
