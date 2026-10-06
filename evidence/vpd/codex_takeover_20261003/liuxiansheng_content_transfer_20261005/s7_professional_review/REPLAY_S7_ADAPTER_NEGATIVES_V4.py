import pathlib,json,hashlib,subprocess,sys,copy
r=pathlib.Path.cwd();out=r/'.liu-visual-private/s7_professional_delivery_audit/protocol_replay_v4';out.mkdir(exist_ok=True)
child=pathlib.Path('C:/Users/Administrator/.codex/sessions/2026/10/06/rollout-2026-10-06T12-51-14-01a10f8d-32a6-7df3-b75b-3f9ec325f3f8.jsonl')
parent=pathlib.Path('C:/Users/Administrator/.codex/sessions/2026/10/04/rollout-2026-10-04T11-12-31-01a0ffab-c9b7-7c40-b55b-e51535c156dd_01a104e6-1b34-70a3-b5fa-04cac3947c09.jsonl')
rows=[]
for x in map(json.loads,child.read_text(encoding='utf8').splitlines()):
 a=x.get('payload',{})
 if x['type'] in ['session_meta','turn_context'] or (x['type']=='response_item' and a.get('type') in ['function_call','custom_tool_call','custom_tool_call_output','function_call_output']) or (x['type']=='response_item' and a.get('type')=='message' and a.get('role')=='assistant' and a.get('phase')=='final_answer') or (x['type']=='event_msg' and (a.get('type')=='agent_message' or a.get('item',{}).get('type')=='ImageView')):rows.append(x)
pr=[];ids=set();outputs=[]
with parent.open(encoding='utf8') as f:
 pr=[json.loads(next(f)),{'type':'fixture_padding','payload':{}}]
 for line in f:
  if 's7_fresh_cold_pixel_review' not in line and 'function_call_output' not in line:continue
  x=json.loads(line);a=x.get('payload',{})
  if x['type']=='response_item' and a.get('type')=='function_call' and a.get('name')=='spawn_agent' and json.loads(a['arguments']).get('task_name')=='s7_fresh_cold_pixel_review':pr.append(x);ids.add(a['call_id'])
  elif x['type']=='response_item' and a.get('type')=='function_call_output':outputs.append(x)
pr += [x for x in outputs if x['payload'].get('call_id') in ids]
def save(p,v):p.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in v),encoding='utf8')
results=[]
for name in ['actual_selected_evidence_control','no_pixel_payloads_with_markers_retained','replace_pixel_payload','extra_output_pixel_payload','extra_message_pixel_payload','human_acceptance_divergence']:
 d=out/name;d.mkdir();cr=copy.deepcopy(rows);pa=copy.deepcopy(pr)
 if name=='no_pixel_payloads_with_markers_retained':
  for x in cr:
   a=x.get('payload',{})
   if a.get('type')=='custom_tool_call_output':a['output']=[z for z in a['output'] if z.get('type')!='input_image']
 if name in ['replace_pixel_payload','extra_output_pixel_payload','extra_message_pixel_payload']:
  toolouts=[x['payload'] for x in cr if x.get('payload',{}).get('type')=='custom_tool_call_output']
  image=copy.deepcopy(next(z for z in toolouts[0]['output'] if z.get('type')=='input_image'))
  if name=='replace_pixel_payload':toolouts[1]['output']=[image if z.get('type')=='input_image' else z for z in toolouts[1]['output']]
  elif name=='extra_output_pixel_payload':toolouts[1]['output'].append(image)
  else:cr.append({'type':'response_item','payload':{'type':'message','role':'user','content':[image]}})
 if name=='human_acceptance_divergence':
  raw=json.loads((r/'evidence/vpd/codex_takeover_20261003/liuxiansheng_content_transfer_20261005/s7_verified_review/RAW_NATIVE_PIXEL_REVIEW.json').read_text(encoding='utf8'));raw['human_acceptance']='ACCEPTED';cr.append({'type':'event_msg','payload':{'type':'agent_message','message':json.dumps(raw,ensure_ascii=False)}})
 if name=='no_image_markers':cr=[x for x in cr if x.get('payload',{}).get('item',{}).get('type')!='ImageView']
 if name=='extra_tool':cr.append({'type':'response_item','payload':{'type':'custom_tool_call','name':'exec','call_id':'TEST_ONLY_EXTRA','input':'await tools.exec_command({cmd:"TEST_ONLY"});'}})
 if name=='no_successful_spawn':
  for x in pa:
   if x.get('payload',{}).get('type')=='function_call_output':x['payload']['output']='collab spawn failed: agent thread limit reached'
 if name=='judgement_divergence':
  raw=json.loads((r/'evidence/vpd/codex_takeover_20261003/liuxiansheng_content_transfer_20261005/s7_verified_review/RAW_NATIVE_PIXEL_REVIEW.json').read_text(encoding='utf8'));raw['verdict']='CONTENT_TRANSFER_FAIL';cr.append({'type':'event_msg','payload':{'type':'agent_message','message':json.dumps(raw,ensure_ascii=False)}})
 save(d/'child.TEST_ONLY.jsonl',cr);save(d/'parent.TEST_ONLY.jsonl',pa)
 run=subprocess.run([sys.executable,str(r/'scripts/vpd_collect_s7_content_transfer_review.py'),str(d/'child.TEST_ONLY.jsonl'),str(d/'result'),'--parent-runtime',str(d/'parent.TEST_ONLY.jsonl')],cwd=r,capture_output=True,text=True,encoding='utf8')
 item={'case':name,'returncode':run.returncode,'stdout':run.stdout,'stderr':run.stderr,'fixture_only':True}
 if (d/'result/ISOLATION_AUDIT.json').exists():item['output_verified']=json.loads((d/'result/ISOLATION_AUDIT.json').read_text(encoding='utf8'))['verified']
 results.append(item)
report={'adapter_sha256':hashlib.sha256((r/'scripts/vpd_collect_s7_content_transfer_review.py').read_bytes()).hexdigest(),'source_child_sha256':hashlib.sha256(child.read_bytes()).hexdigest(),'business_state_modified':False,'cases':results}
(out.parent/'ADAPTER_NEGATIVE_REPLAY_V4.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps(report,ensure_ascii=False))
