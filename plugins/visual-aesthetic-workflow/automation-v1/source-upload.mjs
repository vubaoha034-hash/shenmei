// One-use upload capability for the SAME Site. Never logs original private bytes.
import {advancePipeline} from "./engine.mjs";
import {sha256,inspectImage,putImmutable} from "./openai-image-adapter.mjs";
const must=(x,s)=>{if(!x)throw new Error(s)};
const json=(o,status=200)=>new Response(JSON.stringify(o),{status,headers:{"cache-control":"private, no-store","content-type":"application/json"}});
const ownerKey=async(actor,cryptoApi)=>"user_"+(await sha256(new TextEncoder().encode(actor),cryptoApi)).slice(0,40);
export async function ensureTickets(db){
 must(db?.prepare,"D1_STORAGE_NOT_CONFIGURED");
 await db.prepare("CREATE TABLE IF NOT EXISTS visual_auto_upload_tickets_v1(token_hash TEXT PRIMARY KEY,actor_id TEXT NOT NULL,job_id TEXT NOT NULL,expires_at INTEGER NOT NULL,used INTEGER NOT NULL DEFAULT 0)").run();
}
export async function issueTicket(db,job,{clock=()=>Date.now(),cryptoApi=globalThis.crypto}={}){
 must(job?.phase==="AWAIT_SOURCE","UPLOAD_NOT_REQUIRED_FOR_CURRENT_STAGE");
 must(cryptoApi?.randomUUID,"CRYPTO_RANDOM_UNAVAILABLE");
 await ensureTickets(db);
 const token=cryptoApi.randomUUID()+"-"+cryptoApi.randomUUID();
 const token_hash=await sha256(new TextEncoder().encode(token),cryptoApi);
 const expires_at=Math.floor(clock()/1000)+600;
 await db.prepare("INSERT INTO visual_auto_upload_tickets_v1(token_hash,actor_id,job_id,expires_at,used) VALUES(?,?,?,?,0)").bind(token_hash,job.owner_id,job.job_id,expires_at).run();
 return {token,expires_at,job_id:job.job_id,single_use:true};
}
async function findTicket(db,token,cryptoApi){
 must(typeof token==="string"&&/^[a-z0-9-]{65,120}$/i.test(token),"UPLOAD_TOKEN_FORMAT_INVALID");
 await ensureTickets(db);
 const h=await sha256(new TextEncoder().encode(token),cryptoApi);
 const ticket=await db.prepare("SELECT token_hash,actor_id,job_id,expires_at,used FROM visual_auto_upload_tickets_v1 WHERE token_hash=?").bind(h).first();
 return ticket;
}
export async function getUploadPage(db,token,{clock=()=>Date.now(),cryptoApi=globalThis.crypto}={}){
 const t=await findTicket(db,token,cryptoApi);
 must(t&&t.used===0&&t.expires_at>=Math.floor(clock()/1000),"UPLOAD_TICKET_NOT_VALID");
 const html='<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>视觉工作流：上传参考原图</title><main><h1>上传原始参考图片</h1><p>仅接收 PNG / JPEG / WebP 原始文件。不会当作已经生成的作品。</p><form method="POST" enctype="multipart/form-data"><label>选择原件：<input type="file" name="image" accept=".png,.jpg,.jpeg,.webp,image/*" required></label><button type="submit">上传并核验原始字节</button></form></main></html>';
 return new Response(html,{headers:{"content-type":"text/html; charset=utf-8","cache-control":"no-store","content-security-policy":"default-src 'none'; style-src 'none'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'; img-src 'none'","x-content-type-options":"nosniff"}});
}
export async function receiveUpload({request,token,env,clock=()=>Date.now(),cryptoApi=globalThis.crypto}){
 must(env?.DB?.prepare&&env?.VISUAL_ASSETS?.put&&env?.VISUAL_ASSETS?.get,"UPLOAD_STORAGE_BINDINGS_MISSING");
 const db=env.DB,t=await findTicket(db,token,cryptoApi);
 must(t&&t.used===0&&t.expires_at>=Math.floor(clock()/1000),"UPLOAD_TICKET_EXPIRED_OR_USED");
 const reported=Number(request.headers.get("content-length")||0);
 must(!reported||reported<=22*1024*1024,"UPLOAD_TOO_LARGE");
 const form=await request.formData();
 const file=form.get("image");
 must(file&&typeof file.arrayBuffer==="function","IMAGE_FILE_REQUIRED");
 must(file.size>32&&file.size<=20*1024*1024,"IMAGE_FILE_SIZE_INVALID");
 const bytes=new Uint8Array(await file.arrayBuffer());
 const meta=inspectImage(bytes);
 const actual_sha256=await sha256(bytes,cryptoApi);
 const row=await db.prepare("SELECT payload FROM visual_image_automation_v1 WHERE actor_id=? AND job_id=?").bind(t.actor_id,t.job_id).first();
 const job=row?.payload?JSON.parse(row.payload):null;
 must(job&&job.phase==="AWAIT_SOURCE","UPLOAD_JOB_NOT_IN_SOURCE_STAGE");
 must(actual_sha256===job.reference.sha256&&meta.mime===job.reference.mime&&meta.width===job.reference.width&&meta.height===job.reference.height,"REFERENCE_ORIGINAL_BYTES_DO_NOT_MATCH_MANIFEST");
 // Consume capability atomically so a double-submit cannot create two jobs or overwrite assets.
 const consumed=await db.prepare("UPDATE visual_auto_upload_tickets_v1 SET used=1 WHERE token_hash=? AND used=0 AND expires_at>=?").bind(t.token_hash,Math.floor(clock()/1000)).run();
 must(consumed?.meta?.changes===1,"UPLOAD_ALREADY_USED");
 const stored=await putImmutable(env.VISUAL_ASSETS,await ownerKey(t.actor_id,cryptoApi),job.job_id,bytes,actual_sha256,cryptoApi);
 const next=advancePipeline(job,{id:"asset_upload_"+t.token_hash.slice(0,24),type:"SOURCE_VERIFIED",expected_revision:job.revision,evidence:{checked_actual_bytes:true,actual_sha256,actual_mime:meta.mime,width:meta.width,height:meta.height,asset_id:stored.asset_id}},{actor_id:t.actor_id,actor_type:"executor",now:new Date(clock()).toISOString()});
 const updated=await db.prepare("UPDATE visual_image_automation_v1 SET revision=?,payload=?,updated_at=? WHERE actor_id=? AND job_id=? AND revision=?").bind(next.revision,JSON.stringify(next),next.updated_at,t.actor_id,t.job_id,job.revision).run();
 must(updated?.meta?.changes===1,"CONCURRENT_JOB_REVISION_AFTER_ASSET_UPLOAD");
 return json({ok:true,job_id:job.job_id,phase:next.phase,source_sha256:stored.sha256,private_asset_id:stored.asset_id,readback_verified:true});
}

