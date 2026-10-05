"""Select actual tool/model/final evidence only; never extract reasoning text."""
import json,pathlib,hashlib,sys,re,urllib.parse,argparse
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('child_runtime',type=pathlib.Path)
parser.add_argument('output',type=pathlib.Path)
parser.add_argument('--parent-runtime',required=True,type=pathlib.Path)
cli=parser.parse_args()
root=pathlib.Path.cwd();child=cli.child_runtime;out=root/cli.output
if out.exists():raise RuntimeError('OUTPUT_DIRECTORY_EXISTS')
out.mkdir(parents=True,exist_ok=False)
contexts=[];calls=[];views=0;final=None;meta=None;image_reads=[]
for line in child.open(encoding='utf-8'):
    row=json.loads(line);kind=row.get('type');p=row.get('payload',{})
    if kind=='session_meta':meta={k:p.get(k) for k in ['id','source','cwd','model_provider']}
    if kind=='turn_context':contexts.append({k:p.get(k) for k in ['model','effort','reasoning_effort']})
    if kind=='response_item' and p.get('type') in ['function_call','custom_tool_call']:
        name=p.get('name');args=p.get('input',p.get('arguments',''))
        calls.append({'name':name,'call_id':p.get('call_id'),'arguments':args})
    if kind=='event_msg' and p.get('type')=='item_completed' and p.get('item',{}).get('type')=='ImageView':
        path=urllib.parse.unquote(p['item']['path'].removeprefix('file:///')).replace('\\','/')
        image_reads.append({'path':path,'sha256':hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()})
    if kind=='response_item' and p.get('type')=='message':
        blocks=p.get('content',[])
        if p.get('role')=='assistant':
            for b in blocks:
                if b.get('type') in ['output_text','text']:
                    s=b.get('text','').strip()
                    if s.startswith('{'):
                        try:
                            value=json.loads(s)
                            if value.get('schema')=='vpd-reference-typography-pixel-review/v1':final=value
                        except ValueError:pass
        if p.get('role')=='tool':views+=sum(b.get('type')=='image' for b in blocks)
    if kind=='event_msg' and p.get('type')=='agent_message':
        s=p.get('message','').strip()
        try:
            value=json.loads(s)
            if value.get('schema')=='vpd-reference-typography-pixel-review/v1':final=value
        except ValueError:pass
if final is None:raise RuntimeError('ACTUAL_FINAL_REVIEW_REQUIRED')
# Bounded allowlist: these exact two real wrappers were read in full by Root.
# Unknown future wrappers fail closed; regex below is not a JavaScript sandbox.
REVIEWED_VIEW_WRAPPERS = {'ec5ed0bd96013535a7f692229ac55998cab6cd854b9ac7c6f21c76b049d44f52', '2bf13a520b0bb136b06a87213cbff19b0aaa0d9289d6bdff0fbbec19c1dec130'}
allowed=True
for c in calls:
    code=c['arguments'];names=re.findall(r'\btools\.([A-Za-z0-9_]+)\s*\(',code)
    residual=re.sub(r'\btools\.view_image(?=\s*\()','',code)
    if (c['name']!='exec' or set(names)!={'view_image'}
            or re.search(r'\b(?:eval|Function|import|require|fetch|globalThis|Reflect|tools)\b',residual)
            or re.search(r'\\(?:u|x)',code)
            or hashlib.sha256(code.encode()).hexdigest() not in REVIEWED_VIEW_WRAPPERS):
        allowed=False
bound={i['sha256'] for i in image_reads}=={final['reference_sha256'],final['study_export_sha256']}
actual_effort=contexts[0].get('effort') or contexts[0].get('reasoning_effort')
parent_file=cli.parent_runtime
spawn_source=meta['source'].get('subagent',{}).get('thread_spawn',{})
with parent_file.open('rb') as handle:
    root_meta=json.loads(handle.readline())['payload']
    handle.seek(max(0,parent_file.stat().st_size-32*1024*1024))
    if handle.tell():handle.readline()
    spawns=[]
    for line in handle:
        if b'spawn_agent' not in line:continue
        try:row=json.loads(line)
        except ValueError:continue
        p=row.get('payload',{})
        if row.get('type')=='response_item' and p.get('type')=='function_call' and p.get('name')=='spawn_agent':
            q=json.loads(p.get('arguments','{}'))
            if q.get('task_name')==spawn_source.get('agent_path','').rsplit('/',1)[-1]:
                spawns.append({'call_id':p['call_id'],'fork_turns':q.get('fork_turns'),'model':q.get('model'),'reasoning_effort':q.get('reasoning_effort')})
spawn_verified=len(spawns)==1 and spawns[0]['fork_turns']=='none' and root_meta['id']==spawn_source.get('parent_thread_id')
audit={'schema':'vpd-study-review-runtime-audit/v1','scope':final['scope'],
    'verified':allowed and bound and len(contexts)==1 and len(image_reads)==2 and spawn_verified,
    'fork_turns':'none','history_inherited':False,'actual_model':contexts[0]['model'],
    'actual_reasoning_effort':actual_effort,'pixels_seen':sum(c['arguments'].count('tools.view_image(') for c in calls),
    'reviewer_thread_id':meta['id'],'reference_sha256':final['reference_sha256'],
    'study_export_sha256':final['study_export_sha256'],'tool_scope_violations':[] if allowed else ['UNEXPECTED_TOOL'],
    'actual_tool_calls':[{k:v for k,v in c.items() if k!='arguments'}|{'input_sha256':hashlib.sha256(c['arguments'].encode()).hexdigest()} for c in calls],
    'actual_image_reads':image_reads,'actual_turn_contexts':contexts,
    'actual_parent_spawn':spawns,'actual_child_spawn_source':spawn_source,'parent_spawn_verified':spawn_verified,
    'runtime_file_sha256':hashlib.sha256(child.read_bytes()).hexdigest(),
    'checked_utc':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),
    'reviewed_wrapper_sha256_allowlist':sorted(REVIEWED_VIEW_WRAPPERS),
    'limitations':['Parent logged prompt may be encrypted; fork-none and observed tool scope do not prove every provider-internal prompt token.',
        'Wrapper checks are a bounded reviewed-code allowlist, not a JavaScript security parser.',
        'Fork-none and image input scope bound to parent spawn and actual child trace; shared filesystem is not OS isolation.',
        'Actual ImageView transport markers and current input-file bytes are matched to both declared images.',
        'Prompt hash is not cryptographic proof of provider-internal execution.']}
final['reviewer_thread_id']=meta['id']
(out/'ISOLATION_AUDIT.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(out/'PIXEL_REVIEW.json').write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'reviewer':meta['id'],'actual_contexts':contexts,'tool_calls':len(calls),
    'declared_view_calls':audit['pixels_seen'],'message_image_blocks':views,'verdict':final['verdict'],'verified_before_transport_check':audit['verified']},ensure_ascii=False))
