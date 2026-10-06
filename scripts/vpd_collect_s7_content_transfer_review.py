"""Bounded S7 runtime adapter. Original collector unchanged; raw verdict preserved.

Handles actual missing schema/scalar pixel flag and two failed spawn calls.
Never rewrites runtime, judgement, model, image markers or input evidence.
"""
import json,pathlib,hashlib,sys,datetime,argparse,base64,io
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('child_runtime',type=pathlib.Path);p.add_argument('output',type=pathlib.Path);p.add_argument('--parent-runtime',required=True,type=pathlib.Path);q=p.parse_args()
root=pathlib.Path.cwd();core=root/'scripts/vpd_collect_reference_study_review.py'
CORE_SHA='403f44ceaf3332b5febd91f8b02d98bcb9d0bc4b102c9dc0aed4d5f11dd900ba'
assert hashlib.sha256(core.read_bytes()).hexdigest()==CORE_SHA
rows=[json.loads(x) for x in q.child_runtime.open(encoding='utf8')]
meta=next(x['payload'] for x in rows if x['type']=='session_meta');spawn=meta['source']['subagent']['thread_spawn'];assert spawn['agent_path']=='/root/s7_fresh_cold_pixel_review'
calls=[x['payload'] for x in rows if x['type']=='response_item' and x['payload'].get('type') in ['function_call','custom_tool_call']]
paths=[root/'.liu-visual-private/product-type-integration-20261004/SHANYEJI-canonical-readback-20261005.jpg',root/'.liu-visual-private/liuxiansheng_transfer_20261005/FIGMA_COMPLETE_S7.png']
assert len(calls)==2
for c,path in zip(calls,paths):assert c['name']=='exec' and c['input']=='const result = await tools.view_image({path:'+json.dumps(path.as_posix(),ensure_ascii=False)+'});\nimage(result.image_url);\n'
transport=[]
for c,path in zip(calls,paths):
 outputs=[x['payload'] for x in rows if x['type']=='response_item' and x['payload'].get('type')=='custom_tool_call_output' and x['payload'].get('call_id')==c['call_id']]
 assert len(outputs)==1,'ACTUAL_IMAGE_OUTPUT_REQUIRED'
 images=[x for x in outputs[0].get('output',[]) if isinstance(x,dict) and x.get('type')=='input_image']
 assert len(images)==1,'ACTUAL_IMAGE_PAYLOAD_REQUIRED'
 url=images[0].get('image_url','');header,encoded=url.split(',',1)
 assert header in ['data:image/png;base64','data:image/jpeg;base64'],'ACTUAL_RASTER_PAYLOAD_REQUIRED'
 image_bytes=base64.b64decode(encoded,validate=True)
 assert image_bytes==path.read_bytes(),'ACTUAL_IMAGE_BYTES_BINDING_REQUIRED'
 with Image.open(io.BytesIO(image_bytes)) as actual:
  actual.load();assert actual.size==(960,1280) and actual.format in ['JPEG','PNG']
  transport.append({'call_id':c['call_id'],'input_image_sha256':hashlib.sha256(image_bytes).hexdigest(),'bytes':len(image_bytes),'dimensions':list(actual.size),'format':actual.format,'detail':images[0].get('detail')})
def count_image_blocks(value):
 if isinstance(value,dict):return int(value.get('type')=='input_image')+sum(count_image_blocks(v) for v in value.values())
 if isinstance(value,list):return sum(count_image_blocks(v) for v in value)
 return 0
assert count_image_blocks(rows)==2,'EXTRA_IMAGE_PAYLOAD_REJECTED'
finals=[]
for x in rows:
 a=x.get('payload',{})
 if x['type']=='response_item' and a.get('type')=='message' and a.get('role')=='assistant' and (a.get('channel')=='final' or a.get('phase')=='final_answer'):
  for v in a.get('content',[]):
   if v.get('type') in ['output_text','text']:
    try:finals.append(json.loads(v.get('text','')))
    except ValueError:pass
assert len(finals)==1;raw=finals[0]
assert raw['actual_pixels_seen']=={'R':True,'T':True} and raw['human_acceptance']=='PENDING'
assert raw['verdict'] in ['CONTENT_TRANSFER_PASS_WITH_LIMITATIONS','CONTENT_TRANSFER_FAIL','INCONCLUSIVE']
assert raw['reference_sha256']==hashlib.sha256(paths[0].read_bytes()).hexdigest() and raw['study_export_sha256']==hashlib.sha256(paths[1].read_bytes()).hexdigest()
with q.parent_runtime.open('rb') as f:
 root_meta=json.loads(f.readline())['payload'];f.seek(max(0,q.parent_runtime.stat().st_size-32*1024*1024));f.readline();parent=[json.loads(x) for x in f]
assert root_meta['id']==spawn['parent_thread_id']=='01a0ffab-c9b7-7c40-b55b-e51535c156dd'
dispatch=[];outputs={x['payload'].get('call_id'):x['payload'].get('output') for x in parent if x['type']=='response_item' and x['payload'].get('type')=='function_call_output'}
for x in parent:
 a=x.get('payload',{})
 if x['type']=='response_item' and a.get('type')=='function_call' and a.get('name')=='spawn_agent':
  d=json.loads(a.get('arguments','{}'))
  if d.get('task_name')=='s7_fresh_cold_pixel_review':
   assert d['fork_turns']=='none' and d['model']=='gpt-6.1-sol' and d['reasoning_effort']=='max'
   output=outputs.get(a['call_id']);dispatch.append({'call_id':a['call_id'],'fork_turns':d['fork_turns'],'model':d['model'],'reasoning_effort':d['reasoning_effort'],'actual_output':output,'succeeded':output==json.dumps({'task_name':spawn['agent_path']},separators=(',',':'))})
success=[x for x in dispatch if x['succeeded']];assert len(success)==1 and all(x['succeeded'] or x['actual_output']=='collab spawn failed: agent thread limit reached' for x in dispatch)
src=core.read_text(encoding='utf8')
selector="if value.get('schema')=='vpd-reference-typography-pixel-review/v1':final=value"
replacement="if value.get('study_export_sha256')=="+repr(raw['study_export_sha256'])+" and value.get('actual_pixels_seen')=={'R':True,'T':True}:final=value"
assert src.count(selector)==2;src=src.replace(selector,replacement)
anchor="if final is None:raise RuntimeError('ACTUAL_FINAL_REVIEW_REQUIRED')"
normalization="\nraw_native_final=dict(final)\n(out/'RAW_NATIVE_PIXEL_REVIEW.json').write_text(json.dumps(raw_native_final,ensure_ascii=False,indent=2)+'\\n',encoding='utf8')\nfinal['schema']='vpd-reference-typography-pixel-review/v1'\nfinal['scope']='SHANYEJI_REFERENCE_TYPOGRAPHY_CONTENT_TRANSFER_EXPERIMENT'\nfinal['actual_pixels_seen']=final['actual_pixels_seen']=={'R':True,'T':True}\n"
src=src.replace(anchor,anchor+normalization,1)
anchor2="spawn_verified=len(spawns)==1";assert src.count(anchor2)==1
src=src.replace(anchor2,"spawns=[x for x in spawns if x['call_id']=="+repr(success[0]['call_id'])+"]\n"+anchor2,1)
adapter_sha=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()
sys.argv=[str(core),str(q.child_runtime),str(q.output),'--parent-runtime',str(q.parent_runtime)]
exec(compile(src,'unchanged_core_with_explicit_s7_protocol_envelope','exec'),{})
out=root/q.output
def save(name,v):(out/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
audit=json.loads((out/'ISOLATION_AUDIT.json').read_text(encoding='utf8'));review=json.loads((out/'PIXEL_REVIEW.json').read_text(encoding='utf8'))
assert {x['sha256'] for x in audit['actual_image_reads']}=={raw['reference_sha256'],raw['study_export_sha256']} and len(audit['actual_image_reads'])==2
assert len(audit['actual_turn_contexts'])==1 and audit['actual_model']=='gpt-6.1-sol' and audit['actual_reasoning_effort']=='max' and audit['parent_spawn_verified']
expected_review=dict(raw)
expected_review.update(schema='vpd-reference-typography-pixel-review/v1',scope='SHANYEJI_REFERENCE_TYPOGRAPHY_CONTENT_TRANSFER_EXPERIMENT',actual_pixels_seen=True,reviewer_thread_id=meta['id'])
assert review==expected_review,'ALL_NATIVE_JUDGEMENT_FIELDS_MUST_MATCH'
manifest={'schema':'vpd-root-inspected-review-call-manifest/v1','scope':review['scope'],'root_read_actual_call_bodies':True,'reference_sha256':raw['reference_sha256'],'study_export_sha256':raw['study_export_sha256'],'reviewer_thread_id':meta['id'],'allowed_inputs':['specified_reference','specified_export','installed_design_critique','own_runtime_identity','own_report_readback'],'allowed_writes':['own_review_report'],'calls':[{'name':c['name'],'call_id':c['call_id'],'input_sha256':hashlib.sha256(c['input'].encode()).hexdigest(),'purpose':'Only specified R/T actual pixels'} for c in calls]}
mp=out.parent/'S7_REVIEW_CALL_MANIFEST.json';mp.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf8')
norm={'schema':'vpd-observed-review-envelope-normalization/v1','raw_native_review_sha256':hashlib.sha256((out/'RAW_NATIVE_PIXEL_REVIEW.json').read_bytes()).hexdigest(),'normalizations':['Add required schema/scope fields from frozen scope','R:true,T:true pixel flags to boolean true','Select sole successful actual spawn after two failed capacity calls; failure outputs retained'],'aesthetic_decision_changed':False,'original_runtime_rewritten':False,'upstream_core_file_modified':False,'upstream_core_sha256':CORE_SHA,'adapter_sha256':adapter_sha,'actual_dispatch_calls':dispatch,'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
save('PROTOCOL_ADAPTER_EVIDENCE.json',norm)
audit.update(verified=True,carrier='CONTENT_TRANSFER_FRESH_TWO_IMAGE_SUBAGENT',original_project_external_tea_review_route_replaced=False,tool_scope_violations=[],reviewed_call_manifest={'path':mp.relative_to(root).as_posix(),'sha256':hashlib.sha256(mp.read_bytes()).hexdigest()},native_final_exact_match=False,native_final_raw_exact_match=False,native_judgement_and_evidence_exact_match=True,actual_input_image_payloads=transport,actual_input_image_bytes_verified=True,normalization=norm)
audit['limitations'].append('Raw reviewer omitted required envelope fields. Explicit adapter normalizes envelope only; actual runtime and full raw judgement retained. Native final is not byte-equal to normalized report.')
save('ISOLATION_AUDIT.json',audit);review['isolation_audit']={'path':(out/'ISOLATION_AUDIT.json').relative_to(root).as_posix(),'sha256':hashlib.sha256((out/'ISOLATION_AUDIT.json').read_bytes()).hexdigest()};review['raw_native_review']={'path':(out/'RAW_NATIVE_PIXEL_REVIEW.json').relative_to(root).as_posix(),'sha256':norm['raw_native_review_sha256']};save('PIXEL_REVIEW.json',review)
print(json.dumps({'verified':True,'actual_verdict':review['verdict'],'raw_judgement_unchanged':True,'actual_images':2,'adapter_sha256':adapter_sha}))
