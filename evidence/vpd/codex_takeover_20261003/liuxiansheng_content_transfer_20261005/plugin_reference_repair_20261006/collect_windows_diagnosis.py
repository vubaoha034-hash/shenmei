import json,hashlib
from pathlib import Path
base=Path(__file__).resolve().parent
found=[]
for p in Path('C:/Users/Administrator/.codex/sessions/2026/10/06').glob('*.jsonl'):
 with p.open(encoding='utf-8') as f:
  m=json.loads(f.readline()).get('payload',{})
 if m.get('agent_path')=='/root/site_windows_packaging_diagnosis': found.append((p,m))
if len(found)!=1: raise ValueError(('exact scoped agent sessions',len(found)))
p,m=found[0]; raw=p.read_bytes(); events=[json.loads(x) for x in raw.decode().splitlines()]
items=[e['payload'] for e in events if e['type']=='response_item']
final=next(x for x in reversed(items) if x.get('type')=='message' and x.get('role')=='assistant' and x.get('phase')=='final_answer')
text='\n'.join(x.get('text','') for x in final.get('content',[]) if x.get('type')=='output_text')
(base/'windows_diagnosis_RAW_FINAL.md').write_text(text+'\n',encoding='utf-8',newline='\n')
contexts=[{k:e['payload'].get(k) for k in ['model','effort','reasoning_effort']} for e in events if e['type']=='turn_context']
calls={x.get('call_id'):x for x in items if x.get('type') in ['custom_tool_call','function_call']}
scoped=[]
for x in items:
 c=calls.get(x.get('call_id'),{})
 if x.get('type') in ['custom_tool_call_output','function_call_output'] and c.get('name')=='exec':
  inp=c.get('input',c.get('arguments',''))
  scoped.append({'call_id':x.get('call_id'),'name':'exec','input':inp,'input_sha256':hashlib.sha256(inp.encode()).hexdigest(),'output':x.get('output')})
out={'schema':'vpd-scoped-native-agent-execution-evidence/v1','thread_id':m['id'],'agent_path':m['agent_path'],'agent_role':m.get('agent_role'),'actual_turn_contexts':contexts,'native_runtime_sha256':hashlib.sha256(raw).hexdigest(),'execution_events':scoped,'final_output':'windows_diagnosis_RAW_FINAL.md','limits':'Read-only environment diagnosis and packaging plan. Agent did not verify Root-produced archive or final deployment. Root actual archive verification separately labelled independent_agent:false.'}
(base/'windows_diagnosis_EXECUTION_EVIDENCE.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'agent':m['agent_path'],'contexts':contexts,'scoped_calls':len(scoped)},ensure_ascii=False))
