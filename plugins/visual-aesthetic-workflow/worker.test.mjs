import {test} from 'node:test';
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {DatabaseSync} from 'node:sqlite';
import {mkdirSync,readFileSync} from 'node:fs';
import {createWorker,saveIntake} from './worker.mjs';

test('MCP request ID accepts strings and integers, rejects fractions before any storage',async()=>{
  const worker=createWorker({adapters:{resolveHead:async()=>{throw Error('Unexpected repository read');},readFile:async()=>{throw Error('Unexpected repository read');}}});
  for(const id of [1.5,[],{},null])assert.equal((await worker.fetch(req({jsonrpc:'2.0',id,method:'ping'}),{})).status,400);
  for(const id of ['',0,'request-1'])assert.equal((await worker.fetch(req({jsonrpc:'2.0',id,method:'ping'}),{})).status,200);
});
// Immutable real S4 test fixture; no production HEAD is replaced.
const commit=execFileSync('git',['rev-parse','4d128f7b44dc43163f021b5717f5e003ca70a323^{commit}'],{encoding:'utf8'}).trim();
const repo={resolveHead:async()=>commit,readFile:async({commit,path})=>new Uint8Array(execFileSync('git',['show',commit+':'+path]))};
const wrap=db=>({
  prepare(sql) {
    return {bind(...args) {
      return {
        run:async()=>db.prepare(sql).run(...args),
        first:async()=>db.prepare(sql).get(...args),
        all:async()=>({results:db.prepare(sql).all(...args)}),
      };
    }};
  },
});
function req(rpc,{user=null,origin=null,protocol=null}={}){const headers={'Content-Type':'application/json'};if(user)headers['oai-authenticated-user-id']=user;if(origin)headers.origin=origin;if(protocol!==null)headers['MCP-Protocol-Version']=protocol;return new Request('https://local.test/mcp',{method:'POST',headers,body:JSON.stringify(rpc)});}
const call=(name,args={})=>({jsonrpc:'2.0',id:1,method:'tools/call',params:{name,arguments:args}});
test('HTTP discovery accurately marks durable feedback as a write',async()=>{const r=await createWorker({adapters:repo}).fetch(req({jsonrpc:'2.0',id:1,method:'tools/list'}),{});const b=await r.json();assert.equal(b.result.tools.find(t=>t.name==='save_human_feedback').annotations.readOnlyHint,false);assert.ok(b.result.tools.some(t=>t.name==='get_human_feedback'));});
test('body/query identity cannot substitute trusted hosting identity',async()=>{const r=await createWorker({adapters:repo}).fetch(req(call('get_current_workflow',{userId:'owner'})),{});assert.equal(r.status,401);});
test('cross-origin browser requests are denied',async()=>{const r=await createWorker({adapters:repo}).fetch(req(call('get_current_workflow'),{origin:'https://unrelated.test'}),{});assert.equal(r.status,403);});
test('real committed native files traverse HTTP adapter; no generated acceptance',async()=>{const r=await createWorker({adapters:repo}).fetch(req(call('get_current_workflow'),{user:'local-fixture'}),{});const b=await r.json();assert.equal(r.status,200);assert.equal(b.result.structuredContent.source.commit,commit);assert.equal(b.result.structuredContent.acceptance.promotion_allowed,false);assert.equal(b.result.structuredContent.capabilities.independent_reviewer,false);});
test('durable local SQLite replay persists, conflicts do not overwrite, actors are scoped',async()=>{
  mkdirSync('.liu-visual-private/plugin_http_tests',{recursive:true});
  const path='.liu-visual-private/plugin_http_tests/'+crypto.randomUUID()+'.sqlite';
  const db=new DatabaseSync(path);db.exec('CREATE TABLE feedback_intakes(actor_id TEXT NOT NULL,idempotency_key TEXT NOT NULL,content_sha256 TEXT NOT NULL,payload TEXT NOT NULL,recorded_at TEXT NOT NULL,PRIMARY KEY(actor_id,idempotency_key))');
  const worker=createWorker({adapters:repo,clock:()=> '2026-10-06T00:00:00Z'});
  const args={expected_commit:commit,artwork_sha256:'ddb621ebf7e230279a1358b1b93ab9fcd55705b7e6ca99af8649aa3295ab1ca4',idempotency_key:'local_test_key',verdict:'COMMENT',comment:'TEST ONLY, not a human evaluation or design result'};
  const first=await (await worker.fetch(req(call('save_human_feedback',args),{user:'local-fixture'}),{DB:wrap(db)})).json();assert.equal(first.result.structuredContent.persisted,true);
  const second=await (await worker.fetch(req(call('save_human_feedback',args),{user:'local-fixture'}),{DB:wrap(db)})).json();assert.deepEqual(second.result.structuredContent.durable_receipt,first.result.structuredContent.durable_receipt);
  const conflict=await worker.fetch(req(call('save_human_feedback',{...args,comment:'different'}),{user:'local-fixture'}),{DB:wrap(db)});assert.equal(conflict.status,409);
  db.close();const reopened=new DatabaseSync(path);const other=await (await worker.fetch(req(call('get_human_feedback'),{user:'another-fixture'}),{DB:wrap(reopened)})).json();assert.equal(other.result.structuredContent.intakes.length,0);
  const restored=await (await worker.fetch(req(call('get_human_feedback'),{user:'local-fixture'}),{DB:wrap(reopened)})).json();assert.equal(restored.result.structuredContent.intakes.length,1);assert.equal(restored.result.structuredContent.intakes[0].payload.authority,'NON_AUTHORITATIVE_INTAKE');reopened.close();
});
test('missing durable store cannot return saved',async()=>{await assert.rejects(()=>saveIntake(null,{},repo.resolveHead),/not saved/);});
test('new HEAD before persistence is rejected without database mutation',async()=>{await assert.rejects(()=>saveIntake({}, {validated_intake:{source:{commit},actor_id:'fixture'}},async()=> '0'.repeat(40)),/HEAD_CHANGED/);});
test('all HTTP dispatch paths validate JSON-RPC, argument objects and request ids before any storage access',async()=>{
  const worker=createWorker({adapters:repo});let touched=0;
  const DB={prepare(){touched++;throw new Error('Invalid input must not access storage');}};
  const requests=[{jsonrpc:'wrong',id:1,method:'tools/list'}, {...call('get_human_feedback'),jsonrpc:'wrong'},call('get_human_feedback',0),call('save_human_feedback',0),{jsonrpc:'2.0',method:'tools/call',params:{name:'save_human_feedback',arguments:{}}}, {...call('get_human_feedback'),id:null}, {...call('get_human_feedback'),id:true}, {...call('get_human_feedback'),params:[]}, {jsonrpc:'2.0',id:1,method:'tools/call',params:{name:'get_human_feedback',arguments:null}}];
  for(const rpc of requests)assert.equal((await worker.fetch(req(rpc,{user:'TESTONLY_PROTOCOL'}),{DB})).status,400,JSON.stringify(rpc));
  const notification=await worker.fetch(req({jsonrpc:'2.0',method:'notifications/initialized'}),{DB});assert.equal(notification.status,202);assert.equal(await notification.text(),'');
  assert.equal(touched,0);
});
test('only four advertised public tools are callable; internal prepare cannot bypass durable save',async()=>{
  const worker=createWorker({adapters:repo});
  const list=await (await worker.fetch(req({jsonrpc:'2.0',id:1,method:'tools/list'}),{})).json();
  assert.deepEqual(list.result.tools.map(x=>x.name),['get_current_workflow','compile_transfer_plan','save_human_feedback','get_human_feedback']);
  assert.equal((await worker.fetch(req(call('prepare_human_feedback'),{user:'TESTONLY_PROTOCOL'}),{})).status,400);
});
test('protocol header rejects invalid/unsupported versions and matches initialize negotiation',async()=>{
  const worker=createWorker({adapters:repo});
  for(const protocol of ['wrong','2030-01-01',''])assert.equal((await worker.fetch(req({jsonrpc:'2.0',id:1,method:'tools/list'},{protocol}),{})).status,400);
  const init={jsonrpc:'2.0',id:1,method:'initialize',params:{protocolVersion:'2025-06-18'}};
  const response=await worker.fetch(req(init,{protocol:'2025-06-18'}),{});assert.equal(response.status,200);assert.equal(response.headers.get('MCP-Protocol-Version'),'2025-06-18');assert.equal((await response.json()).result.protocolVersion,'2025-06-18');
  assert.equal((await worker.fetch(req(init,{protocol:'2025-03-26'}),{})).status,400);
  const negotiated=await worker.fetch(req({...init,params:{protocolVersion:'unknown-future'}},{protocol:'2025-06-18'}),{});assert.equal((await negotiated.json()).result.protocolVersion,'2025-06-18');
  assert.equal((await worker.fetch(req({jsonrpc:'2.0',id:1,method:'tools/list'}),{})).status,200);
});
test('51 pending intakes remain recoverable by tied-timestamp cursor and exact key with actor isolation',async()=>{
  const db=new DatabaseSync(':memory:');db.exec('CREATE TABLE feedback_intakes(actor_id TEXT NOT NULL,idempotency_key TEXT NOT NULL,content_sha256 TEXT NOT NULL,payload TEXT NOT NULL,recorded_at TEXT NOT NULL,PRIMARY KEY(actor_id,idempotency_key))');
  const insert=db.prepare('INSERT INTO feedback_intakes VALUES (?,?,?,?,?)');
  for(let i=0;i<51;i++){const key='TESTONLY_'+String(i).padStart(4,'0');insert.run('TESTONLY_OWNER',key,'f'.repeat(64),JSON.stringify({idempotency_key:key,scope:'SYNTHETIC_ONLY'}),'2026-10-06T00:00:00.000Z');}
  insert.run('TESTONLY_OTHER','TESTONLY_OTHER_KEY','e'.repeat(64),JSON.stringify({scope:'OTHER_ACTOR_SYNTHETIC_ONLY'}),'2026-10-06T00:00:00.000Z');
  const worker=createWorker({adapters:repo});
  const read=async(args={},user='TESTONLY_OWNER')=>{const response=await worker.fetch(req(call('get_human_feedback',args),{user}),{DB:wrap(db)});assert.equal(response.status,200);return (await response.json()).result.structuredContent;};
  const first=await read();assert.equal(first.intakes.length,50);assert.ok(first.next_cursor);assert.equal(first.intakes[0].idempotency_key,'TESTONLY_0050');
  const last=await read({cursor:first.next_cursor});assert.equal(last.intakes.length,1);assert.equal(last.intakes[0].idempotency_key,'TESTONLY_0000');assert.equal(last.next_cursor,null);
  assert.equal(new Set([...first.intakes,...last.intakes].map(x=>x.idempotency_key)).size,51);
  const exact=await read({idempotency_key:'TESTONLY_0000'});assert.equal(exact.intakes.length,1);assert.equal(exact.next_cursor,null);
  assert.equal((await read({idempotency_key:'TESTONLY_0000'},'TESTONLY_OTHER')).intakes.length,0);
  assert.equal((await read({cursor:first.next_cursor},'TESTONLY_OTHER')).intakes.length,0);
  assert.equal((await read({},'TESTONLY_OTHER')).intakes.length,1);
  for(const args of [{cursor:'garbage'},{limit:0},{limit:51},{idempotency_key:'TESTONLY_0000',cursor:first.next_cursor},{idempotency_key:'TESTONLY_0000',limit:1},{cursor:JSON.stringify(['bad-date','TESTONLY_0000'])}])assert.equal((await worker.fetch(req(call('get_human_feedback',args),{user:'TESTONLY_OWNER'}),{DB:wrap(db)})).status,400);
  assert.equal(db.prepare('SELECT count(*) n FROM feedback_intakes').get().n,52);db.close();
});
