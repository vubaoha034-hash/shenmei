import test from "node:test";
import assert from "node:assert/strict";
import {createPipeline} from "./engine.mjs";
import {sha256,inspectImage} from "./openai-image-adapter.mjs";
import {issueTicket,getUploadPage,receiveUpload} from "./source-upload.mjs";
import {extendExistingVisualWorker} from "./mcp-overlay.mjs";
class TestDB {
 constructor(){this.jobs=new Map();this.tickets=new Map()}
 prepare(sql){const db=this;return {async run(){if(sql.startsWith("CREATE TABLE"))return {meta:{changes:0}};throw new Error("BIND_REQUIRED")},bind(...a){
   return {
    async first(){
     if(sql.includes("FROM visual_auto_upload_tickets_v1"))return db.tickets.get(a[0])||null;
     if(sql.includes("FROM visual_image_automation_v1")&&sql.includes("request_key")){for(let j of db.jobs.values())if(j.actor_id===a[0]&&j.request_key===a[1])return {payload:j.payload};return null}
     if(sql.includes("FROM visual_image_automation_v1")){let j=db.jobs.get(a[1]);return j&&j.actor_id===a[0]?{payload:j.payload}:null}
     return null;
    },
    async run(){
     if(sql.startsWith("CREATE TABLE"))return {meta:{changes:0}};
     if(sql.startsWith("INSERT INTO visual_auto_upload_tickets_v1")){db.tickets.set(a[0],{token_hash:a[0],actor_id:a[1],job_id:a[2],expires_at:a[3],used:0});return {meta:{changes:1}}}
     if(sql.startsWith("INSERT INTO visual_image_automation_v1")){db.jobs.set(a[1],{actor_id:a[0],job_id:a[1],request_key:a[2],revision:a[3],payload:a[4],updated_at:a[5]});return {meta:{changes:1}}}
     if(sql.startsWith("UPDATE visual_auto_upload_tickets_v1")){let t=db.tickets.get(a[0]);if(t&&t.used===0&&t.expires_at>=a[1]){t.used=1;return {meta:{changes:1}}}return {meta:{changes:0}}}
     if(sql.startsWith("UPDATE visual_image_automation_v1")){let j=db.jobs.get(a[4]);if(j&&j.actor_id===a[3]&&j.revision===a[5]){j.revision=a[0];j.payload=a[1];j.updated_at=a[2];return {meta:{changes:1}}}return {meta:{changes:0}}}
     throw new Error("UNKNOWN_TEST_SQL_"+sql.slice(0,70));
    }
   }
 }}}
}
function privateBucket(){const m=new Map();return {async put(k,b){m.set(k,new Uint8Array(b))},async get(k){let a=m.get(k);return a?{arrayBuffer:async()=>a.buffer.slice(a.byteOffset,a.byteOffset+a.byteLength)}:null}}}
function makeImage(){let u=new Uint8Array(33);u.set([137,80,78,71,13,10,26,10]);u[18]=1;u[22]=1;return u}
const owner="user_private_test";
test("source ticket is single-use, expires, and binds real bytes to one actor and private job",async()=>{
 const db=new TestDB(),bucket=privateBucket(),bytes=makeImage(),sha=await sha256(bytes);
 const job=createPipeline({request_key:"ticket_test_001",goal:"create original image",max_generation_calls:1,reference:{role:"THIRD_PARTY_REFERENCE",sha256:sha,asset_id:"UPLOAD_PENDING",mime:"image/png",width:256,height:256,rights:"UNKNOWN"}},{actor_id:owner,job_id:"visual_testjob0001",now:"2026-10-12T00:00:00Z"});
 db.jobs.set(job.job_id,{actor_id:owner,job_id:job.job_id,request_key:job.request_key,revision:job.revision,payload:JSON.stringify(job)});
 const timestamp=Date.parse("2026-10-12T00:00:00Z"),time=()=>timestamp;
 const issued=await issueTicket(db,job,{clock:time});assert.ok(issued.token.length>64);
 const response=await getUploadPage(db,issued.token,{clock:time});
 assert.equal(response.status,200);assert.match(await response.text(),/上传原始参考图片/);
 const form=new FormData();form.append("image",new Blob([bytes],{type:"image/png"}),"example.png");
 const request=new Request("https://existing.site/visual-automation/upload/"+issued.token,{method:"POST",body:form});
 const done=await receiveUpload({request,token:issued.token,env:{DB:db,VISUAL_ASSETS:bucket},clock:time});
 const final=await done.json();assert.equal(final.ok,true);assert.equal(final.phase,"AWAIT_COST_APPROVAL");assert.equal(final.source_sha256,sha);
 const after=JSON.parse(db.jobs.get(job.job_id).payload);
 assert.ok(after.reference.asset_id.startsWith("user_"));assert.notEqual(after.reference.asset_id,"UPLOAD_PENDING");
 await assert.rejects(getUploadPage(db,issued.token,{clock:time}),/UPLOAD_TICKET_NOT_VALID/);
 await assert.rejects(receiveUpload({request,token:issued.token,env:{DB:db,VISUAL_ASSETS:bucket},clock:time}),/UPLOAD_TICKET_EXPIRED_OR_USED/);
});
test("wrong hash is rejected before ticket is consumed",async()=>{
 const db=new TestDB(),bucket=privateBucket(),bytes=makeImage(),sha=await sha256(bytes);
 const job=createPipeline({request_key:"ticket_wrong_001",goal:"new photo",max_generation_calls:1,reference:{role:"THIRD_PARTY_REFERENCE",sha256:"f".repeat(64),asset_id:"UPLOAD_PENDING",mime:"image/png",width:256,height:256,rights:"UNKNOWN"}},{actor_id:owner,job_id:"visual_testjob0002",now:"2026-10-12T00:00:00Z"});
 db.jobs.set(job.job_id,{actor_id:owner,job_id:job.job_id,request_key:job.request_key,revision:job.revision,payload:JSON.stringify(job)});
 const timestamp=Date.parse("2026-10-12T00:00:00Z"),time=()=>timestamp;
 const issued=await issueTicket(db,job,{clock:time});
 const form=new FormData();form.append("image",new Blob([bytes],{type:"image/png"}),"wrong.png");
 const request=new Request("https://site/upload",{method:"POST",body:form});
 await assert.rejects(receiveUpload({request,token:issued.token,env:{DB:db,VISUAL_ASSETS:bucket},clock:time}),/REFERENCE_ORIGINAL_BYTES_DO_NOT_MATCH_MANIFEST/);
 const page=await getUploadPage(db,issued.token,{clock:time});assert.equal(page.status,200);
 await assert.rejects(getUploadPage(db,issued.token,{clock:()=>timestamp+601000}),/UPLOAD_TICKET_NOT_VALID/);
});
test("additive MCP overlay preserves existing tools and refuses approval without trusted verifier",async()=>{
 const db=new TestDB();
 const base={async fetch(req){const q=await req.json();if(q.method==="tools/list")return new Response(JSON.stringify({jsonrpc:"2.0",id:q.id,result:{tools:[{name:"get_photo_composition_workflow"}]}}),{headers:{"content-type":"application/json"}});return new Response(JSON.stringify({jsonrpc:"2.0",id:q.id,result:{content:[]}}))}};
 const overlay=extendExistingVisualWorker(base);
 const req=(id,name,args={})=>new Request("https://existing.site/mcp",{method:"POST",headers:{"content-type":"application/json","oai-authenticated-user-id":owner},body:JSON.stringify({jsonrpc:"2.0",id,method:"tools/call",params:{name,arguments:args}})});
 const toolsRes=await overlay.fetch(new Request("https://existing.site/mcp",{method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify({jsonrpc:"2.0",id:1,method:"tools/list",params:{}})}),{DB:db});
 const tools=(await toolsRes.json()).result.tools.map(x=>x.name);
 assert.ok(tools.includes("get_photo_composition_workflow"));assert.ok(tools.includes("start_visual_automation"));assert.ok(tools.includes("get_visual_upload_ticket"));
 const started=await overlay.fetch(req(2,"start_visual_automation",{request_key:"overlaytest1",goal:"new picture",max_generation_calls:1,reference:{role:"THIRD_PARTY_REFERENCE",sha256:"a".repeat(64),asset_id:"UPLOAD_PENDING",mime:"image/png",width:256,height:256,rights:"UNKNOWN"}}),{DB:db});
 const job=(await started.json()).result.structuredContent.job;
 assert.equal(job.phase,"AWAIT_SOURCE");
 const decision=await overlay.fetch(req(3,"record_verified_visual_user_decision",{job_id:job.job_id,expected_revision:1,action:"COST_AUTHORIZED",event_id:"human_test1",evidence:{explicit_user_approval:true},consent_token:"NOT_A_REAL_SIGNED_USER_TOKEN"}),{DB:db});
 assert.match(JSON.stringify(await decision.json()),/HUMAN_APPROVAL_UI_NOT_CONNECTED/);
 const contract=await overlay.fetch(req(4,"get_visual_automation_contract"),{DB:db});
 const status=(await contract.json()).result.structuredContent;
 assert.equal(status.capabilities.status,"BLOCKED_MISSING_CAPABILITY");
 assert.equal(status.native_task_lock_write,false);
});

