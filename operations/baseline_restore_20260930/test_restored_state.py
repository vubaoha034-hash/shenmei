"""Mutate the real repaired snapshot; test state/identity controls, not aesthetics."""
from pathlib import Path
import sys, json, hashlib
root=Path(sys.argv[1]).resolve();sys.path.insert(0,str(root))
from visual_memory.vpd_p6_composition_state import validate_p6_composition_state
L='continuity/vpd/CURRENT_TASK_LOCK.json';C='continuity/vpd/LATEST_CHECKPOINT.json';A='PROJECT_CONTROL_ADAPTER.json';G='continuity/vpd/VISUAL_MASTER_FREEZE_GUARD_V1.json'
R='evidence/vpd/p1_typography_research_sandbox_v1/CHAZUO_NEW_IMAGE_COMPOSITION01_EXECUTION_20260930.json'
H='evidence/vpd/p1_typography_research_sandbox_v1/CHAZUO_CONCEPT02_EDITABLE_RECONSTRUCTION_HUMAN_REVIEW_PHOTO_FAIL_20260921.json'
T='evidence/vpd/p1_typography_research_sandbox_v1/CHAZUO_NEW_IMAGE_COMPOSITION01_TASK_20260930.json'
J='continuity/vpd/state_ledger/commercial_design_pipeline.jsonl'
files=[L,C,A,G,R,H,J,T];original={p:(root/p).read_bytes() for p in files}
enc=lambda d:(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode()
sha=lambda b:hashlib.sha256(b).hexdigest()
def read(p):return json.loads((root/p).read_text())
def put(p,d):(root/p).write_bytes(enc(d))
def reset():
 for p,b in original.items():(root/p).write_bytes(b)
def rehash():
 g,l,c,a=map(read,[G,L,C,A]);g['current_comparison']['evidence']['sha256']=sha((root/R).read_bytes());put(G,g)
 t=read(T);t['human_verdict_ref']=g['current_comparison']['evidence'];put(T,t)
 ref={'path':G,'sha256':sha((root/G).read_bytes())}
 l['baseline_preservation']=ref;l['visual_master_freeze_guard']['sha256']=ref['sha256'];put(L,l)
 c['baseline_preservation']=a['baseline_preservation']=ref;c['task_lock']['sha256']=a['task_lock']['sha256']=sha((root/L).read_bytes());c['latest_evidence']=g['current_comparison']['evidence']
 lines=(root/J).read_text().splitlines();e=json.loads(lines[-1]);e['lock_sha256']=sha((root/L).read_bytes());e.pop('event_hash');e['event_hash']=sha(json.dumps(e,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode());lines[-1]=json.dumps(e,ensure_ascii=False,separators=(',',':'));(root/J).write_text('\n'.join(lines)+'\n')
 c['ledger_tails']=a['ledger_tails']={'commercial_design_pipeline':{'event_id':e['event_id'],'event_hash':e['event_hash']}};put(C,c);put(A,a)
def mutate(p,keys,value):
 d=read(p);t=d
 for k in keys[:-1]:t=t[k]
 t[keys[-1]]=value;put(p,d)
validate_p6_composition_state(root)
results=[{'test':'real_repaired_state','result':'PASS'}]
cases=[
 ('failed_image_used_as_reference',lambda:mutate(G,['current_comparison','baseline_frame_ids'],['227:2','201:2']),True,'WRONG_PROTECTED_REFERENCE'),
 ('photo_acceptance_invented',lambda:mutate(G,['current_comparison','photographic_realism_accepted'],True),True,'SCOPED_ACCEPTANCE_UPGRADED'),
 ('whole_poster_acceptance_invented',lambda:mutate(G,['current_comparison','whole_poster_accepted'],True),True,'SCOPED_ACCEPTANCE_UPGRADED'),
 ('negative_promoted',lambda:mutate(G,['current_comparison','rejected_candidate_is_baseline'],True),True,'WRONG_BASELINE_ROLE'),
 ('generation_budget_reopened',lambda:mutate(L,['execution_boundary','current_image_generation_authorization'],1),True,'UNAUTHORIZED_NEW_EXECUTION'),
 ('settled_trial_returned_to_pending',lambda:mutate(C,['chazuo_new_image_composition01','status'],'PENDING'),True,'CURRENT_CANDIDATE_MIRROR_DRIFT'),
 ('stale_candidate_task',lambda:mutate(T,['next_legal_action'],'WAIT_FOR_HUMAN_REVIEW'),True,'STALE_CANDIDATE_TASK'),
 ('stale_current_stage',lambda:mutate(C,['current_stage'],'AWAITING_HUMAN'),True,'CURRENT_STAGE_MIRROR_DRIFT'),
 ('claim_blind_evaluation',lambda:mutate(R,['coordinator_baseline_comparison','review_type'],'INDEPENDENT_BLIND'),True,'PIXEL_REVIEW_EVIDENCE_OR_ISOLATION_CLAIM'),
 ('stale_reference_hash',lambda:mutate(L,['baseline_preservation','sha256'],'0'*64),False,'ADAPTER_STALE_LOCK'),
 ('missing_human_scope_source',lambda:(root/H).unlink(),True,None),
]
try:
 for name,change,recompute,expected in cases:
  reset();change()
  if recompute:rehash()
  try:validate_p6_composition_state(root)
  except (ValueError,OSError,KeyError) as e:
   if expected and str(e)!=expected:raise AssertionError(name+': unexpected '+str(e))
   results.append({'test':name,'result':'BLOCKED_AS_EXPECTED','reason':str(e)})
  else:raise AssertionError(name+': failed to block')
finally:reset()
validate_p6_composition_state(root)
print(json.dumps({'checks':results,'count':len(results),'actual_reference_pixels_compared_by_machine_tests':False,'aesthetic_judgment_automated':False,'all_test_mutations_restored':True},ensure_ascii=False,indent=2))
