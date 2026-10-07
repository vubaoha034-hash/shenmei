import test from 'node:test';
import assert from 'node:assert/strict';
import {createWorker} from './worker.mjs';

const req=(rpc,user=null)=>{
  const h={'Content-Type':'application/json'};
  if(user)h['oai-authenticated-user-id']=user;
  return new Request('https://local.test/mcp',{method:'POST',headers:h,body:JSON.stringify(rpc)});
};

test('root and initialize expose v0.2.0',async()=>{
  const w=createWorker({adapters:{resolveHead:async()=>{throw Error('no read')},readFile:async()=>{throw Error('no read')}}});
  assert.equal((await (await w.fetch(new Request('https://local.test/'),{})).json()).version,'0.2.0');
  const r=await w.fetch(req({jsonrpc:'2.0',id:1,method:'initialize',params:{protocolVersion:'2025-06-18'}}),{});
  assert.equal((await r.json()).result.serverInfo.version,'0.2.0');
});

test('tool discovery keeps legacy tools and adds hard-gated typography tools',async()=>{
  const w=createWorker({adapters:{resolveHead:async()=>{throw Error('no read')},readFile:async()=>{throw Error('no read')}}});
  const r=await w.fetch(req({jsonrpc:'2.0',id:1,method:'tools/list'}),{});
  const b=await r.json();
  const names=b.result.tools.map(x=>x.name);
  for(const n of ['get_current_workflow','compile_transfer_plan','validate_user_request_delivery','save_human_feedback','get_human_feedback','start_typography_delivery','get_typography_delivery','record_typography_stage']) assert.ok(names.includes(n),n);
  assert.match(b.result.tools.find(x=>x.name==='compile_transfer_plan').description,/cannot complete an isolated editable typography request/);
});

test('new write tools require authenticated hosting identity',async()=>{
  const w=createWorker({adapters:{resolveHead:async()=>{throw Error('must not read')},readFile:async()=>{throw Error('must not read')}}});
  const rpc={jsonrpc:'2.0',id:1,method:'tools/call',params:{name:'start_typography_delivery',arguments:{expected_commit:'a'.repeat(40),request_key:'request_001',reference_source:'attachment://ref',requested_copy:{title:'地图以外'}}}};
  const r=await w.fetch(req(rpc),{});
  assert.equal(r.status,401);
});


const emptyTaskDB={
  prepare(sql){
    const ops={
      run:async()=>({success:true}),
      first:async()=>null,
      all:async()=>({results:[]})
    };
    return {
      ...ops,
      bind(..._args){ return ops; }
    };
  }
};

test('missing typography task is an MCP tool-level error over HTTP 200, not transport 404',async()=>{
  const w=createWorker({adapters:{resolveHead:async()=>{throw Error('no repository read expected')},readFile:async()=>{throw Error('no repository read expected')}}});
  const rpc={jsonrpc:'2.0',id:11,method:'tools/call',params:{name:'get_typography_delivery',arguments:{}}};
  const r=await w.fetch(req(rpc,'owner-test'),{DB:emptyTaskDB});
  assert.equal(r.status,200);
  const b=await r.json();
  assert.equal(b.result.isError,true);
  assert.equal(b.result.content[0].text,'TYPOGRAPHY_TASK_NOT_FOUND');
  assert.equal(b.error,undefined);
});

test('recording against a missing typography task also stays inside MCP tool result',async()=>{
  const w=createWorker({adapters:{resolveHead:async()=>{throw Error('no repository read expected')},readFile:async()=>{throw Error('no repository read expected')}}});
  const rpc={jsonrpc:'2.0',id:12,method:'tools/call',params:{name:'record_typography_stage',arguments:{
    task_id:'typo_00000000-0000-4000-8000-000000000000',
    expected_revision:1,
    stage:'REFERENCE_TEXT_EXTRACTION',
    artifact:{artifact_type:'REFERENCE_TEXT_EXTRACTION'}
  }}};
  const r=await w.fetch(req(rpc,'owner-test'),{DB:emptyTaskDB});
  assert.equal(r.status,200);
  const b=await r.json();
  assert.equal(b.result.isError,true);
  assert.equal(b.result.content[0].text,'TYPOGRAPHY_TASK_NOT_FOUND');
});
