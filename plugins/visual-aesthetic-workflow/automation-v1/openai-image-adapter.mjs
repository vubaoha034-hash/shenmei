// Optional paid adapter. Same existing plugin; NOT a ChatGPT subscription Image call.
const must=(x,code)=>{if(!x)throw new Error(code)};
const hex=a=>Array.from(a,x=>x.toString(16).padStart(2,"0")).join("");
const arr=b=>b instanceof Uint8Array?b:new Uint8Array(b);
export async function sha256(b,cryptoApi=globalThis.crypto){
 must(cryptoApi?.subtle,"WEBCRYPTO_UNAVAILABLE");
 return hex(new Uint8Array(await cryptoApi.subtle.digest("SHA-256",arr(b))));
}
export function inspectImage(b){
 const a=arr(b),n=a.length;must(n>=24,"IMAGE_TOO_SHORT");
 const dv=new DataView(a.buffer,a.byteOffset,n);
 if([137,80,78,71,13,10,26,10].every((v,i)=>a[i]===v)){
  const width=dv.getUint32(16,false),height=dv.getUint32(20,false);
  must(width>0&&height>0&&width<=25000&&height<=25000,"PNG_DIMENSION_INVALID");
  return {mime:"image/png",width,height,bytes:n};
 }
 if(a[0]===255&&a[1]===216&&a[2]===255){
  let o=2;while(o+9<n){if(a[o]!==255){o++;continue}
   const tag=a[o+1],len=dv.getUint16(o+2,false);
   must(len>=2,"JPEG_MARKER_INVALID");
   if([192,193,194,195,198,199,201,202].includes(tag)){const height=dv.getUint16(o+5,false),width=dv.getUint16(o+7,false);must(width&&height,"JPEG_DIMENSION_INVALID");return {mime:"image/jpeg",width,height,bytes:n}}
   o+=2+len;
  }throw new Error("JPEG_SOF_MISSING");
 }
 const ascii=(i,n)=>String.fromCharCode(...a.slice(i,i+n));
 if(n>30&&ascii(0,4)==="RIFF"&&ascii(8,4)==="WEBP"){
  const kind=ascii(12,4);let width,height;
  if(kind==="VP8X"){width=1+a[24]+(a[25]<<8)+(a[26]<<16);height=1+a[27]+(a[28]<<8)+(a[29]<<16)}
  else if(kind==="VP8 "){width=dv.getUint16(26,true)&0x3fff;height=dv.getUint16(28,true)&0x3fff}
  else if(kind==="VP8L"){width=1+a[21]+((a[22]&63)<<8);height=1+((a[22]>>6)&3)+(a[23]<<2)+((a[24]&15)<<10)}
  else throw new Error("WEBP_LAYOUT_UNSUPPORTED");
  must(width>0&&height>0,"WEBP_DIMENSIONS_INVALID");return {mime:"image/webp",width,height,bytes:n};
 }
 throw new Error("UNSUPPORTED_IMAGE_MAGIC");
}
export function assertAdapterReady(env){
 must(env?.OPENAI_API_KEY?.length>10,"OPENAI_KEY_NOT_CONFIGURED");
 must(env?.OPENAI_VISION_MODEL,"VISION_MODEL_NOT_CONFIGURED");
 must(env?.OPENAI_IMAGE_MODEL,"IMAGE_MODEL_NOT_CONFIGURED");
 must(env?.VISUAL_ASSETS?.get&&env?.VISUAL_ASSETS?.put,"PRIVATE_R2_STORAGE_NOT_CONFIGURED");
 return {ready:true,uses:"SEPARATELY_BILLED_OPENAI_API",asset_store:"VISUAL_ASSETS"};
}
export async function putImmutable(bucket,ownerKey,jobId,bytes,expectedHash,cryptoApi=globalThis.crypto){
 must(bucket?.put&&bucket?.get,"STORAGE_NOT_CONFIGURED");
 must(/^[a-z0-9_-]{8,128}$/i.test(ownerKey||"")&&/^[a-z0-9_-]{8,128}$/i.test(jobId||""),"INVALID_OWNER_OR_JOB");
 const info=inspectImage(bytes);must(info.bytes<=20*1024*1024,"ASSET_TOO_LARGE");
 const digest=await sha256(bytes,cryptoApi);must(!expectedHash||expectedHash===digest,"ASSET_HASH_MISMATCH");
 const suffix=info.mime==="image/png"?"png":info.mime==="image/jpeg"?"jpg":"webp";
 const id=ownerKey+"/"+jobId+"/"+digest+"."+suffix;
 await bucket.put(id,arr(bytes),{httpMetadata:{contentType:info.mime}});
 const obj=await bucket.get(id);must(obj,"STORED_ASSET_MISSING");
 const after=new Uint8Array(await obj.arrayBuffer());
 must(await sha256(after,cryptoApi)===digest,"READBACK_MISMATCH");
 return {asset_id:id,sha256:digest,...info,readback_verified:true};
}
export async function readImmutable(bucket,ownerKey,assetId,expectedHash,cryptoApi=globalThis.crypto){
 must(bucket?.get&&assetId?.startsWith(ownerKey+"/")&&/^[a-f0-9]{64}$/.test(expectedHash||""),"ASSET_ACCESS_INVALID");
 const obj=await bucket.get(assetId);must(obj,"ASSET_NOT_FOUND");
 const bytes=new Uint8Array(await obj.arrayBuffer());
 const digest=await sha256(bytes,cryptoApi);must(digest===expectedHash,"SOURCE_HASH_CHANGED");
 return {...inspectImage(bytes),bytes_count:bytes.length,bytes,sha256:digest};
}
const b64Encode=bytes=>{let s="",u=arr(bytes);for(let i=0;i<u.length;i+=16384)s+=String.fromCharCode(...u.subarray(i,i+16384));return btoa(s)};
const b64Decode=s=>{must(typeof s==="string"&&s.length>0,"BASE64_OUTPUT_MISSING");let v=atob(s),u=new Uint8Array(v.length);for(let i=0;i<v.length;i++)u[i]=v.charCodeAt(i);return u};
export function createOpenAIAdapter(env,{fetchImpl=globalThis.fetch,cryptoApi=globalThis.crypto}={}){
 assertAdapterReady(env);
 must(typeof fetchImpl==="function","FETCH_UNAVAILABLE");
 const auth={Authorization:"Bearer "+env.OPENAI_API_KEY};
 async function responseToJSON(r){
  let j;try{j=await r.json()}catch{throw new Error("API_RESPONSE_NOT_JSON")}
  if(!r.ok)throw new Error("OPENAI_API_HTTP_"+r.status);
  return j;
 }
 async function analyze({referenceBytes,referenceSha256,goal}){
  const m=inspectImage(referenceBytes),sha=await sha256(referenceBytes,cryptoApi);
  must(sha===referenceSha256,"VISION_REFERENCE_BYTES_CHANGED");
  const ask="Analyze the attached actual reference as a professional art director. Do not copy exact geography or copyrighted layouts. Provide valid JSON ONLY: main_subject (string), high_impact_variables (2-8 concrete visible relations), avoid (0-4). Avoid hype. Goal: "+goal;
  const q={model:env.OPENAI_VISION_MODEL,input:[{role:"user",content:[{type:"input_text",text:ask},{type:"input_image",image_url:"data:"+m.mime+";base64,"+b64Encode(referenceBytes)}]}],max_output_tokens:1100};
  const res=await fetchImpl("https://api.openai.com/v1/responses",{method:"POST",headers:{...auth,"Content-Type":"application/json"},body:JSON.stringify(q)});
  const data=await responseToJSON(res);
  let txt=data.output_text||data.output?.flatMap(o=>o.content||[]).filter(c=>c.type==="output_text").map(c=>c.text).join("\n");
  must(typeof txt==="string"&&txt.trim(),"VISION_ANALYSIS_EMPTY");
  let parsed;try{parsed=JSON.parse(txt.replace(/^[^{]*/,"").replace(/[^}]*$/,""))}catch{throw new Error("VISION_JSON_NOT_PARSABLE")}
  must(typeof parsed.main_subject==="string"&&Array.isArray(parsed.high_impact_variables),"VISION_FIELDS_MISSING");
  return {program:{reference_sha256:sha,actual_reference_pixels_inspected:true,inspector:"OpenAI Responses "+env.OPENAI_VISION_MODEL,main_subject:parsed.main_subject,high_impact_variables:parsed.high_impact_variables,avoid:parsed.avoid||[]},reference_sha256:sha,request_id:res.headers.get("x-request-id")||data.id||"REQUEST_ID_NOT_EXPOSED"};
 }
 async function render({referenceBytes,referenceSha256,prompt,size="1024x1536",quality="high"}){
  const m=inspectImage(referenceBytes),sha=await sha256(referenceBytes,cryptoApi);
  must(sha===referenceSha256,"RENDER_REFERENCE_BYTES_CHANGED");
  must(typeof prompt==="string"&&prompt.length>5&&prompt.length<=16000,"RENDER_PROMPT_INVALID");
  const form=new FormData();form.append("model",env.OPENAI_IMAGE_MODEL);form.append("prompt",prompt);form.append("image",new Blob([arr(referenceBytes)],{type:m.mime}),"reference."+(m.mime==="image/jpeg"?"jpg":m.mime==="image/webp"?"webp":"png"));form.append("n","1");form.append("quality",quality);form.append("size",size);form.append("output_format","png");
  const res=await fetchImpl("https://api.openai.com/v1/images/edits",{method:"POST",headers:auth,body:form});
  const data=await responseToJSON(res);
  must(data.data?.length===1,"IMAGE_VARIANT_COUNT_WRONG");
  const bytes=b64Decode(data.data[0].b64_json),out=inspectImage(bytes),imageSha=await sha256(bytes,cryptoApi);
  return {bytes,source_sha256:sha,output_sha256:imageSha,output_mime:out.mime,width:out.width,height:out.height,provider_response_id:res.headers.get("x-request-id")||data.id||"REQUEST_ID_NOT_EXPOSED",model:env.OPENAI_IMAGE_MODEL,n:1};
 }
 return {analyze,render};
}

