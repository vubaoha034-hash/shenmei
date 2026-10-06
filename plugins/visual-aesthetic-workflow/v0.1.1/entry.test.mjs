import { test } from 'node:test';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { createCore, PATHS, sha256 } from './core.mjs';
import { createCore as oldCore } from './baseline-core-v0.1.0.mjs';
const currentCommit = '3e6a5638c2af2bedcfd66d23fabf6aa7d35c957d';
const oldCommit = '4d128f7b44dc43163f021b5717f5e003ca70a323';
const identity = { userId: 'LOCAL_TEST_ONLY_NOT_PRODUCTION_IDENTITY' };
const request = {jsonrpc:'2.0',id:1,method:'tools/call',params:{name:'get_current_workflow',arguments:{}}};
const bytes = (commit,path) => new Uint8Array(execFileSync('git',['show',commit+':'+path],{maxBuffer:2000000}));
const decode = b => JSON.parse(new TextDecoder().decode(b));
function instance(factory=createCore,commit=currentCommit,overrides=new Map(),heads=null){
  let calls=0;
  return factory({resolveHead:async()=>heads ? heads[Math.min(calls++,heads.length-1)] : commit,readFile:async({commit,path})=>overrides.get(path)??bytes(commit,path),authorize:async who=>who.userId===identity.userId});
}
test('actual published350/372 reproduces old fixed-path rejection',async()=>{
  const r=await instance(oldCore).handle(request,identity);
  assert.equal(r.status,409);assert.match(r.body.error.message,/Current reuse entry mismatch/);
});
test('actual published350/372 resolves final native entry and current S7',async()=>{
  const r=await instance().handle(request,identity);assert.equal(r.status,200);
  const v=r.body.result.structuredContent;
  assert.equal(v.source.commit,currentCommit);assert.equal(v.source.lock_revision,350);assert.equal(v.source.checkpoint_sequence,372);
  assert.equal(v.entry.path,'continuity/vpd/codex_takeover_20261003/S7_FINAL_REUSE.md');
  assert.match(v.entry.text,/DELIVERY_MANIFEST_S7_FINAL.json/);
  assert.equal(v.artwork.sha256,'ed03ba67ca82da6920e49ab44f42f73f112d8c9bc25b841cb47ebcfc7a583762');
  assert.equal(v.next_required_action,'LIU_REVIEW_LIUXIANSHENG_CONTENT_TRANSFER');
  assert.equal(v.acceptance.human,'PENDING');assert.equal(v.acceptance.promotion_allowed,false);
  assert.equal(v.acceptance.cold_pixel_evidence,'RECORDED_BOUND_RUNTIME_EVIDENCE_NOT_REEXECUTED');
});
test('actual legacy S4 commit remains supported',async()=>{
  const r=await instance(createCore,oldCommit).handle(request,identity);assert.equal(r.status,200);assert.equal(r.body.result.structuredContent.entry.path,PATHS.entry);
});
test('entry bytes still require actual pinned SHA',async()=>{
  const overrides=new Map([['continuity/vpd/codex_takeover_20261003/S7_FINAL_REUSE.md',new TextEncoder().encode('TEST_ONLY_TAMPER')]]);
  const r=await instance(createCore,currentCommit,overrides).handle(request,identity);assert.equal(r.status,409);assert.match(r.body.error.message,/EVIDENCE_HASH_MISMATCH/);
});
test('matching state projections cannot admit an unrelated entry path',async()=>{
  const lock=decode(bytes(currentCommit,PATHS.lock));const cp=decode(bytes(currentCommit,PATHS.checkpoint));const adapter=decode(bytes(currentCommit,PATHS.adapter));
  const bad={path:'unrelated/new-authority.md',sha256:'a'.repeat(64)};
  lock.codex_takeover.reuse_entry=bad;adapter.workflow.current_bounded_delivery_entry=bad;
  const encode=v=>new TextEncoder().encode(JSON.stringify(v));const lockBytes=encode(lock);
  for(const x of [cp,adapter])x.task_lock.sha256=await sha256(lockBytes);
  const overrides=new Map([[PATHS.lock,lockBytes],[PATHS.checkpoint,encode(cp)],[PATHS.adapter,encode(adapter)]]);
  const r=await instance(createCore,currentCommit,overrides).handle(request,identity);assert.equal(r.status,409);assert.match(r.body.error.message,/Current reuse entry mismatch/);
});
test('HEAD drift and missing identity still block data-bearing calls',async()=>{
  assert.equal((await instance().handle(request)).status,401);
  const r=await instance(createCore,currentCommit,new Map(),[currentCommit,oldCommit]).handle(request,identity);assert.equal(r.status,409);assert.match(r.body.error.message,/HEAD_CHANGED_DURING_READ/);
});
