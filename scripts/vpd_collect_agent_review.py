"""Collect real fork-none pixel-agent evidence; refuse context/tool scope violations."""
import argparse,datetime,hashlib,json,pathlib,re,urllib.parse
ROOT=pathlib.Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def write(p,v):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 return {'path':str(p.relative_to(ROOT)).replace('\\','/'),'sha256':sha(p)}
def rows(p):return [json.loads(x) for x in p.open(encoding='utf-8')]

def decoded_objects(value):
 if isinstance(value,dict):
  yield value
  for v in value.values():yield from decoded_objects(v)
 elif isinstance(value,list):
  for v in value:yield from decoded_objects(v)
 elif isinstance(value,str):
  try:v=json.loads(value)
  except ValueError:return
  if not isinstance(v,str):yield from decoded_objects(v)
def main():
 a=argparse.ArgumentParser();a.add_argument('--agent',required=True);a.add_argument('--root-thread',required=True);a.add_argument('--packet',required=True);a.add_argument('--out',required=True);a.add_argument('--version',type=int,required=True);a.add_argument('--prompt',required=True);a.add_argument('--child-rollout',required=True);a.add_argument('--root-rollout',required=True);a.add_argument('--target');a.add_argument('--holdout-target-reread',action='store_true');a.add_argument('--supplemental-source',action='store_true');a.add_argument('--carrier-amendment',default='continuity/vpd/codex_takeover_20261003/REVIEW_CARRIER_AMENDMENT.json');a.add_argument('--expected-model',choices=['gpt-6.1-sol','gpt-6-sol'],default='gpt-6.1-sol');a.add_argument('--capacity-failure-receipt');a.add_argument('--projectless-worker-creation');a.add_argument('--formal-work-unit');args=a.parse_args()
 if args.expected_model=='gpt-6-sol':
  assert args.capacity_failure_receipt,'Fallback requires a recorded actual pixel-review capacity failure'
  capacity=json.loads((ROOT/args.capacity_failure_receipt).read_text(encoding='utf-8'))
  assert capacity.get('source_kind')=='ACTUAL_TOOL_FAILURE_NOTIFICATION' and capacity.get('role')=='PIXEL_REVIEW' and capacity.get('requested_model')=='gpt-6.1-sol' and capacity.get('requested_effort')=='max' and capacity.get('failure')=='Selected model is at capacity. Please try a different model.','Fallback capacity evidence does not match this role'
 images=[('P','P.png'),('N','N.png'),('R','R.jpg')]+([('S','S.png')] if args.supplemental_source else [])+[('T','T.png')]
 ids=[n for n,_ in images]
 if args.supplemental_source:
  amendment=json.loads((ROOT/args.carrier_amendment).read_text(encoding='utf-8'))
  permitted_scope=('CURRENT_CORRECT_SOURCE_FORMAL_WORKER_REVIEW' if args.formal_work_unit else 'SUPPLEMENTAL_SKILL_REVIEW_NOT_CANONICAL_VERSION_REPLACEMENT')
  assert amendment.get('attachments_required')==ids and amendment.get('scope')==permitted_scope,'Five-image review requires explicit scoped amendment'
  if args.formal_work_unit: assert amendment.get('work_unit_id')==args.formal_work_unit
 assert not args.holdout_target_reread or (args.version==0 and args.target),'Reread exception is only an explicitly identified old holdout, never a formal version'
 out=(ROOT/args.out).resolve();packet=(ROOT/args.packet).resolve()
 child=pathlib.Path(args.child_rollout);root=pathlib.Path(args.root_rollout)
 assert child.is_file() and root.is_file(),'Exact child/root runtime evidence missing'
 child_meta=json.loads(child.open(encoding='utf-8').readline())['payload'];root_meta=json.loads(root.open(encoding='utf-8').readline())['payload']
 source=child_meta.get('source',{})
 sp=source.get('subagent',{}).get('thread_spawn',{}) if isinstance(source,dict) else {}
 assert root_meta['id']==args.root_thread,'Exact root runtime identity mismatch'
 creation=None
 if args.projectless_worker_creation:
  creation=json.loads((ROOT/args.projectless_worker_creation).read_text(encoding='utf-8'))
  assert creation['thread_id']==child_meta['id'] and creation['target']['type']=='projectless' and creation['new_thread'] is True
  assert creation['creator_history_inherited'] is False and not child_meta.get('forked_from_id')
 else: assert sp.get('agent_path')==args.agent and sp.get('parent_thread_id')==args.root_thread,'Exact child runtime identity mismatch'
 events=rows(child);meta=events[0]['payload'];tid=meta['id']
 contexts=[j['payload'] for j in events if j.get('type')=='turn_context']
 assert len(contexts)==1,'Resumed/multiple-context reviewer is not a fresh formal run'
 context=contexts[0];assert (context['model'],context['effort'])==(args.expected_model,'max')
 spawns=[]
 for j in rows(root):
  v=j.get('payload',{})
  if j.get('type')=='response_item' and v.get('type')=='function_call' and v.get('name')=='spawn_agent':
   try:q=json.loads(v.get('arguments',''))
   except ValueError:continue
   if q.get('task_name')==args.agent.rsplit('/',1)[-1]:spawns.append((q,v.get('call_id')))
 if creation:
  creation_calls=[j['payload'] for j in rows(root) if j.get('type')=='response_item' and j.get('payload',{}).get('type')=='custom_tool_call' and j['payload'].get('name')=='exec' and re.search(r'\bawait\s+tools\.mcp__codex_app__create_thread\s*\(',j['payload'].get('input','')) and creation['directory_name'] in j['payload'].get('input','')]
  assert len(creation_calls)==1,'Actual unique projectless-worker creation call not proven'
  creation['root_creation_call_ids']=[j['call_id'] for j in creation_calls]
  returned=[j['payload'] for j in rows(root) if j.get('type')=='response_item' and j.get('payload',{}).get('type')=='custom_tool_call_output' and j['payload'].get('call_id')==creation_calls[0]['call_id']]
  assert len(returned)==1,'Exact completed creation result missing'
  returned_threads=[v for v in decoded_objects(returned[0]['output']) if v.get('threadId')]
  matched_threads=[v for v in returned_threads if v['threadId']==child_meta['id']]
  assert len(matched_threads)==1,'Actual unique created worker threadId differs from runtime identity'
  creation['other_returned_thread_ids_in_same_exec']=sorted({v['threadId'] for v in returned_threads if v['threadId']!=child_meta['id']})
  creation['creation_binding_rule']='Exactly one returned object matching the actual child identity, within the already proven unique projectless create_thread call; unrelated stop/message returns are recorded separately.'
  creation['actual_returned_thread_id']=matched_threads[0]['threadId']
  creation['actual_creation_result_sha256']=hashlib.sha256(json.dumps(returned[0]['output'],ensure_ascii=False,sort_keys=True).encode()).hexdigest()
 else: assert spawns and all(q.get('fork_turns')=='none' for q,_ in spawns),'Fork-none spawn not proven'
 prompt_sha=sha(ROOT/args.prompt)
 bindings=[{'neutral_id':n,'sha256':sha(packet/f)} for n,f in images]
 expected={str((packet/f).resolve()).replace('\\','/'):n for n,f in images}
 viewed=[];extra=[];calls=[]
 for j in events:
  v=j.get('payload',{})
  if j.get('type')=='response_item' and v.get('type') in ['custom_tool_call','function_call']:
   name=v.get('name');code=v.get('input',v.get('arguments',''))
   names=re.findall(r'tools\.([A-Za-z_0-9]+)\s*\(',code)
   # Fail closed on alias/bracket/dynamic tool invocation. ImageView paths below
   # independently bind the actual read results. This is a bounded run audit,
   # not a proof of arbitrary JavaScript semantic isolation.
   residual=re.sub(r'\btools\.view_image(?=\s*\()', '', code)
   dynamic=re.search(r'\b(?:eval|Function|import|require|fetch|globalThis|Reflect)\b|\btools\b',residual)
   if name!='exec' or not names or set(names)!={'view_image'} or dynamic:extra.append({'name':name,'called_tools':names,'dynamic_form':bool(dynamic)})
   calls.append({'name':name,'input_sha256':hashlib.sha256(code.encode()).hexdigest(),'called_tools':names,'call_id':v.get('call_id')})
  if j.get('type')=='event_msg' and v.get('type')=='item_completed' and v.get('item',{}).get('type')=='ImageView':
   uri=v['item']['path'];path=urllib.parse.unquote(uri.removeprefix('file:///')).replace('\\','/')
   assert path in expected,'Image read outside packet'
   n=expected[path];viewed.append({'tool':'view_image','neutral_id':n,'sha256':next(x['sha256'] for x in bindings if x['neutral_id']==n),'path':path})
 counts={n:sum(x['neutral_id']==n for x in viewed) for n in ids}
 allowed_counts={n:1 for n in ids};allowed_counts['T']=2 if args.holdout_target_reread else 1
 assert not extra and counts==allowed_counts,'Actual permitted-image read scope not proven'
 completions=[j['payload'] for j in events if j.get('type')=='event_msg' and j.get('payload',{}).get('type')=='task_complete']
 assert len(completions)==1,'No unique completed reviewer'
 raw=json.loads(completions[0]['last_agent_message'])
 assert raw.get('pixels_seen')==ids and raw.get('version')==args.version
 if args.formal_work_unit: assert raw.get('work_unit_id')==args.formal_work_unit
 assert raw.get('human_verdict')=='HIDDEN_PENDING' and raw.get('personal_fit') is None
 assert raw.get('verdict') in ['AI_PASS','AI_FAIL'],'No valid actual pixel judgment'
 target=args.target or f'.liu-visual-private/versions/v{args.version}/poster.png'
 assert sha(ROOT/target)==bindings[-1]['sha256'],'Target identity mismatch'
 rawref=write(out/'REVIEWER_OUTPUT.json',raw)
 scope=('Current formally authorized work unit uses exactly P/N/R/S/T; historical four-image and source-reconstruction five-image protocols remain preserved.' if args.formal_work_unit else 'Only declared unique images; the optional S is a source-reconciliation reference, not a new design version. Formal four-image protocol is retained.')
 toolref=write(out/'RAW_TOOL_READ_AUDIT.json',{'thread_id':tid,'tool_reads':viewed,'extra_tool_reads':extra,'source_project_context_reads':[],'raw_rollout_sha256':sha(child),'tool_calls':calls,'actual_image_view_markers':len(viewed),'holdout_only_target_reread':args.holdout_target_reread,'supplemental_source':args.supplemental_source,'scope':scope,'formal_work_unit':args.formal_work_unit})
 carrier='FRESH_PROJECTLESS_CODEX_WORKER' if creation else 'FRESH_FORK_NONE_PIXEL_AGENT'
 fork='NOT_APPLICABLE_NEW_THREAD' if creation else 'none'
 callids=creation['root_creation_call_ids'] if creation else [c for _,c in spawns]
 spawnref=write(out/'SPAWN_RECEIPT.json',{'thread_id':tid,'fork_turns':fork,'history_inherited':False,'initial_prompt_sha256':prompt_sha,'prompt_copy_byte_binding_to_encrypted_spawn':'NOT_VERIFIABLE','actual_model':context['model'],'actual_reasoning_effort':context['effort'],'root_spawn_call_ids':callids,'source':meta['source'],'prompt_ref':{'path':args.prompt,'sha256':prompt_sha},'persistent_message_storage':'Encrypted in runtime; supplied prompt copy preserved separately','projectless_creation':creation})
 evref=write(out/'CONTEXT_EVIDENCE.json',{'thread_id':tid,'turn_context':{'model':context['model'],'reasoning_effort':context['effort']},'initial_prompt_sha256':prompt_sha,'tool_reads':viewed,'raw_tool_read_audit':toolref,'spawn_receipt':spawnref,'reviewer_output':rawref})
 amend=args.carrier_amendment
 audit=write(out/'ISOLATION_AUDIT.json',{'schema_version':'vpd-isolated-pixel-review-audit/v1','verified':True,'carrier':carrier,'fork_turns':fork,'history_inherited':False,'resumed_or_history_forked':False,'source_project_context_read':False,'fresh_agent':True,'actual_model':context['model'],'actual_reasoning_effort':context['effort'],'completed':True,'tool_scope_violations':[],'attachments_verified':ids,'initial_prompt_sha256':prompt_sha,'evidence':evref,'carrier_amendment':{'path':amend,'sha256':sha(ROOT/amend)}})
 result={**raw,'input_bindings':bindings,'isolation_audit':audit,'export':{'path':target,'sha256':bindings[-1]['sha256']},'reviewed_at':completions[0].get('completed_at',datetime.datetime.now(datetime.timezone.utc).isoformat()),'reviewer':{**raw.get('reviewer',{}),'carrier':carrier,'thread_id':tid,'actual_model':context['model'],'actual_reasoning_effort':context['effort']}}
 resultref=write(out/'PIXEL_REVIEW.json',result);print(json.dumps({'verdict':result['verdict'],'result':resultref,'thread_id':tid}))
if __name__=='__main__':main()
