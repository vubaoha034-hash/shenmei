import test from "node:test";
import assert from "node:assert/strict";
import {createOpenAIAdapter,sha256} from "./openai-image-adapter.mjs";
const image=()=>{let b=new Uint8Array(33);b.set([137,80,78,71,13,10,26,10]);b[18]=1;b[22]=1;return b;};
function setup(fetchImpl){return createOpenAIAdapter({OPENAI_API_KEY:"test-secret-must-never-be-logged",OPENAI_VISION_MODEL:"fake-vision",OPENAI_IMAGE_MODEL:"fake-image",VISUAL_ASSETS:{get:async()=>{},put:async()=>{}}},{fetchImpl})}
test("paid vision model receives actual image bytes as an input_image, not merely a URL or filename",async()=>{
 const bytes=image(),digest=await sha256(bytes),calls=[];
 const p=setup(async(url,opt)=>{calls.push({url,opt});const body=JSON.parse(opt.body);
  assert.equal(body.model,"fake-vision");assert.equal(body.input[0].content[1].type,"input_image");
  const embedded=body.input[0].content[1].image_url;
  assert.ok(embedded.startsWith("data:image/png;base64,"));
  const bytesSeen=Buffer.from(embedded.split(",")[1],"base64");
  assert.equal(await sha256(bytesSeen),digest);
  return new Response(JSON.stringify({id:"vision-response-id",output_text:JSON.stringify({main_subject:"one small car above cloud valley",high_impact_variables:["pale sky","left road","fog bank"],avoid:["sunburst"]})}),{status:200,headers:{"x-request-id":"vision-request-id","content-type":"application/json"}});
 });
 const result=await p.analyze({referenceBytes:bytes,referenceSha256:digest,goal:"map outside"});
 assert.equal(result.program.reference_sha256,digest);
 assert.equal(result.program.actual_reference_pixels_inspected,true);
 assert.equal(result.request_id,"vision-request-id");
 assert.equal(calls.length,1);
});
test("Image API edit request embeds exactly one original reference binary and does not create hidden variants",async()=>{
 const bytes=image(),sha=await sha256(bytes);
 let called=0;
 const p=setup(async(url,opt)=>{
  called++;
  assert.equal(url,"https://api.openai.com/v1/images/edits");
  assert.equal(opt.method,"POST");
  const f=opt.body;
  assert.equal(f.get("n"),"1");
  assert.equal(f.get("prompt"),"An original mountain road with low fog");
  const original=Buffer.from(await f.get("image").arrayBuffer());
  assert.equal(await sha256(original),sha);
  assert.equal(f.get("model"),"fake-image");
  return new Response(JSON.stringify({data:[{b64_json:Buffer.from(bytes).toString("base64")}] }),{status:200,headers:{"x-request-id":"render-id"}});
 });
 const res=await p.render({referenceBytes:bytes,referenceSha256:sha,prompt:"An original mountain road with low fog"});
 assert.equal(called,1);assert.equal(res.source_sha256,sha);assert.equal(res.output_sha256,sha);
 assert.equal(res.output_mime,"image/png");assert.equal(res.width,256);assert.equal(res.height,256);
 assert.equal(res.provider_response_id,"render-id");assert.equal(res.n,1);
});
test("wrong source digest and provider errors fail closed without claiming completion",async()=>{
 const bytes=image(),digest=await sha256(bytes);
 const p=setup(async()=>{throw new Error("SHOULD_NOT_CALL_PROVIDER")});
 await assert.rejects(p.render({referenceBytes:bytes,referenceSha256:"a".repeat(64),prompt:"valid prompt"}),/RENDER_REFERENCE_BYTES_CHANGED/);
 await assert.rejects(p.analyze({referenceBytes:bytes,referenceSha256:"b".repeat(64),goal:"test"}),/VISION_REFERENCE_BYTES_CHANGED/);
 const q=setup(async()=>new Response(JSON.stringify({error:{message:"Provider failed"}}),{status:503}));
 await assert.rejects(q.render({referenceBytes:bytes,referenceSha256:digest,prompt:"valid prompt"}),/OPENAI_API_HTTP_503/);
});

