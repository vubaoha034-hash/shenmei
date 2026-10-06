"""Extract only scoped agent execution evidence; never publish full session metadata."""
import hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
SESSION=Path('C:/Users/Administrator/.codex/sessions/2026/10/06')
SPECS={
 'implementation':'rollout-2026-10-06T18-28-33-01a110c2-070c-7a22-b5c3-797334a26564.jsonl',
 'independent_review':'rollout-2026-10-06T18-39-33-01a110cc-17a0-7133-8dec-86ed93c03198.jsonl'
}
EXECUTION_CALL_IDS={
 'implementation':{'call_9tnX8jK1LGvGSCrOSdvE7vDy','call_6FC0hMQao7J3qXksWLoH63xt'},
 'independent_review':{'call_EcHRF4CvH4GfEdyBl63Jzwne','call_8dZbFSpb8PBzl7X8ZVPNFHyZ'}
}
def write(name,obj):
 p=ROOT/name;p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');return {'path':name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
for role,filename in SPECS.items():
 path=SESSION/filename;data=path.read_bytes();events=[json.loads(x) for x in data.decode('utf-8').splitlines()]
 meta=events[0]['payload'];items=[e['payload'] for e in events if e['type']=='response_item']
 contexts=[{k:e['payload'].get(k) for k in ['model','effort','reasoning_effort']} for e in events if e['type']=='turn_context']
 calls={x['call_id']:x for x in items if x.get('type') in ['custom_tool_call','function_call']}
 selected=[]
 for item in items:
  if item.get('type') not in ['custom_tool_call_output','function_call_output']:continue
  call=calls.get(item.get('call_id'),{});code=call.get('input',call.get('arguments',''))
  if item.get('call_id') not in EXECUTION_CALL_IDS[role] or call.get('name')!='exec':continue
  selected.append({'call_id':item.get('call_id'),'name':call.get('name'),'input':code,'input_sha256':hashlib.sha256(code.encode()).hexdigest(),'output':item.get('output')})
 final=next(x for x in reversed(items) if x.get('type')=='message' and x.get('role')=='assistant' and x.get('phase')=='final_answer')
 text='\n'.join(x.get('text','') for x in final.get('content',[]) if x.get('type')=='output_text')
 (ROOT/(role+'_RAW_FINAL.md')).write_text(text+'\n',encoding='utf-8',newline='\n')
 proof=write(role+'_EXECUTION_EVIDENCE.json',{'schema':'vpd-scoped-native-agent-execution-evidence/v1','role':role,'thread_id':meta['id'],'parent_thread_id':meta.get('parent_thread_id'),'agent_path':meta.get('agent_path'),'agent_role':meta.get('agent_role'),'native_runtime_sha256':hashlib.sha256(data).hexdigest(),'actual_turn_contexts':contexts,'execution_events':selected,'final_output':role+'_RAW_FINAL.md','full_runtime_published':False,'proof_limits':'Native event excerpts confirm actual model and local execution. Not hosted, pixel, aesthetic or human acceptance evidence. Full runtime remains private.'})
 print(json.dumps({'role':role,'actual_contexts':contexts,'actual_scoped_events':len(selected),'proof':proof},ensure_ascii=False))
