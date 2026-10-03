#!/usr/bin/env python3
"""One writer, existing VPD lock/checkpoint/ledger; never an aesthetic oracle."""
import argparse, copy, datetime, hashlib, json, pathlib, subprocess, os
ROOT = pathlib.Path(__file__).resolve().parents[1]
LOCK = 'continuity/vpd/CURRENT_TASK_LOCK.json'
CP = 'continuity/vpd/LATEST_CHECKPOINT.json'
ADAPTER = 'PROJECT_CONTROL_ADAPTER.json'
BASE = 'continuity/vpd/codex_takeover_20261003/'
TASK = 'VPD-CHAZUO-CODEX-COMPLETE-POSTER-20261003-01'
BRANCH = 'visual-program-distillation-v2-photography-design-20260814'

def dump(rel, value):
    p=ROOT/rel; p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')

def ref(rel):
    from visual_memory.vpd_task_lock import digest
    return {'path':rel,'sha256':digest(ROOT/rel)}

def read(rel): return json.loads((ROOT/rel).read_text(encoding='utf-8'))

def remote_head():
    try:
        return subprocess.check_output(['gh','api','repos/vubaoha034-hash/shenmei/git/ref/heads/'+BRANCH,'--jq','.object.sha'],cwd=ROOT,text=True).strip()
    except subprocess.CalledProcessError:
        # A different transport, with TLS verification retained; one bounded fallback.
        raw=subprocess.check_output(['git','-c','http.sslBackend=openssl','ls-remote','https://github.com/vubaoha034-hash/shenmei.git','refs/heads/'+BRANCH],cwd=ROOT,text=True).split()
        if len(raw)!=2 or raw[1]!='refs/heads/'+BRANCH:raise ValueError('REMOTE_REF_UNVERIFIED')
        return raw[0]

def encoded(value):
    return (json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf-8')

def write_transaction(updates):
    originals={p:p.read_bytes() for p in updates}
    staged={}
    try:
        for p,content in updates.items():
            tmp=p.with_name(p.name+'.codex-staged')
            tmp.write_bytes(content);staged[p]=tmp
        for p,tmp in staged.items():os.replace(tmp,p)
    except BaseException:
        for p,content in originals.items():p.write_bytes(content)
        raise
    finally:
        for tmp in staged.values():
            if tmp.exists():tmp.unlink()

def main():
    a=argparse.ArgumentParser(); a.add_argument('--receipt',required=True); a.add_argument('--status',required=True); a.add_argument('--next',required=True); a.add_argument('--focus',required=True); a.add_argument('--versions',type=int,default=0); a.add_argument('--revisions',type=int,default=0); args=a.parse_args()
    if not 0<=args.versions<=3 or not 0<=args.revisions<=2: raise ValueError('BUDGET_EXCEEDED')
    current_branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()
    if current_branch!=BRANCH: raise ValueError('BRANCH_DRIFT')
    remote=remote_head()
    local=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    if remote!=local: raise ValueError('REMOTE_ADVANCED_RECONCILE_BEFORE_WRITE')
    lock,cp,adapter=read(LOCK),read(CP),read(ADAPTER)
    from visual_memory.vpd_task_lock import evidence_bytes
    ledger='continuity/vpd/state_ledger/commercial_design_pipeline.jsonl'
    originals={ROOT/rel:(ROOT/rel).read_bytes() for rel in [LOCK,CP,ADAPTER,ledger]}
    ledger_bytes=originals[ROOT/ledger].replace(b'\r\n',b'\n')
    head_ledger=subprocess.check_output(['git','show','HEAD:'+ledger],cwd=ROOT)
    if not ledger_bytes.startswith(head_ledger):raise ValueError('HISTORICAL_LEDGER_PREFIX_CHANGED')
    last=json.loads(ledger_bytes.decode('utf-8').splitlines()[-1])
    receipt=read(args.receipt)
    if receipt.get('task_id')!=TASK or receipt.get('status')!=args.status or receipt.get('next_required_action')!=args.next:raise ValueError('RECEIPT_STATE_MISMATCH')
    if receipt.get('budget')!={'formal_versions_used':args.versions,'revisions_used':args.revisions}:raise ValueError('RECEIPT_BUDGET_MISMATCH')
    prior=lock.get('codex_takeover')
    if prior and (args.versions<prior['budget']['formal_versions_used'] or args.revisions<prior['budget']['revisions_used']): raise ValueError('BUDGET_ROLLBACK')
    if prior and args.versions>prior['budget']['formal_versions_used']+1: raise ValueError('NON_SERIAL_VERSION')
    now=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat()
    take={**(prior or {}),'task_id':TASK,'status':args.status,'next_required_action':args.next,'authorization':ref(BASE+'EXECUTION_AUTHORIZATION.json'),'photo_protection':ref(BASE+'PHOTO_PROTECTION.json'),'receipt':ref(args.receipt),'budget':{'formal_versions_max':3,'formal_versions_used':args.versions,'revisions_max':2,'revisions_used':args.revisions,'photo_generations':0,'paid_compute_usd':0,'training':0,'automations':0,'second_style':0},'human_verdict':'PENDING','candidate_promoted':False,'state_writer':'ROOT_EXECUTOR_ONLY'}
    entry='REUSE_FINAL.md' if (ROOT/BASE/'REUSE_FINAL.md').exists() else 'REUSE.md'
    if (ROOT/BASE/entry).exists():
        take['reuse_entry']=ref(BASE+entry)
    lock['revision']+=1; lock['codex_takeover']=take; lock['current_task_id']=TASK; lock['status']=args.status; lock['next_required_action']=args.next; lock['current_stage']=args.focus; lock['updated_at']=now; lock['latest_evidence']=ref(args.receipt); lock['completed_this_revision']=receipt.get('completed_this_revision') or ['本次授权范围内真实制作与证据按回执保存；历史已认可范围保留']
    lock['execution_boundary']['current_image_generation_authorization']=0
    lock['execution_boundary']['current_figma_canvas_authorization']=3-args.versions
    lock['execution_boundary']['current_image_generation_authorization_scope']=TASK
    lock['execution_boundary']['successor_execution_authorized']=True
    lock['execution_boundary']['bounded_typography_design_versions_authorization']=take['authorization']
    lock['execution_boundary']['legacy_zero_figma_budget_scope']='SUPERSEDED_FOR_THIS_EXPLICIT_USER_BOUNDED_TASK_ONLY'
    lock['execution_boundary']['photo_repair_loop_closed']=True
    lock['render_allowed']=False
    # Correct a current projection that accidentally used image SHA as JSON-receipt SHA.
    for d in [lock,cp]:
        rr=d['candidate88_external_review_r4']['revision']
        rr['output_sha256']='7d84d35523afcb2d7599c438fc946801608e85c5489a5cde08d55f13eea4c9ed'
        rr.update(ref('evidence/vpd/candidate88_external_review_20261002/r4/REVISION_EXECUTION_RECEIPT.json'))
        rr.pop('receipt',None)
    lr={'path':LOCK,'sha256':hashlib.sha256(encoded(lock)).hexdigest()}
    event={'schema_version':'upcp-state-ledger-event/v1','stream_id':'commercial_design_pipeline','event_id':'EVT-VPD-CODEX-CHAZUO-'+str(lock['revision'])+'-20261003','event_type':'CODEX_BOUNDED_DESIGN_NATIVE_STATE_UPDATE','project_id':lock['project_id'],'task_id':TASK,'recorded_at':now,'previous_event_id':last['event_id'],'previous_event_hash':last['event_hash'],'lock_sha256':lr['sha256'],'material':True,'authorization':take['authorization'],'evidence':[take['receipt'],take['photo_protection']],'before':{'revision':lock['revision']-1,'checkpoint':cp['sequence']},'after':{'revision':lock['revision'],'checkpoint':cp['sequence']+1,'status':args.status,'next_required_action':args.next,'budget':take['budget']},'reason':'Explicit complete-poster takeover; preserve old human verdict and mainline history. Technical state is not aesthetic acceptance.'}
    event['event_hash']=hashlib.sha256(json.dumps(event,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    new_ledger=ledger_bytes+(json.dumps(event,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode('utf-8')
    tail={'commercial_design_pipeline':{k:event[k] for k in ['event_id','event_hash']}}
    cp.update(sequence=cp['sequence']+1,recorded_at=now,updated_at=now,current_focus=args.focus,current_stage=args.focus,active_task_ids=[TASK],status=args.status,next_required_action=args.next,task_lock={**lr,'revision':lock['revision']},codex_takeover=copy.deepcopy(take),latest_evidence=lock['latest_evidence'],ledger_tails=tail,mainline_progress=copy.deepcopy(lock['mainline_progress']))
    cp['incomplete']=['本轮设计未通过内部审美审核，等待刘先生验收失败成品','长期视觉蒸馏及迁移收益未验证'] if args.status.endswith('DELIVERED_AI_FAIL_HUMAN_PENDING') else ['最终成品刘先生真人验收','长期视觉蒸馏及迁移收益未验证']
    adapter['task_lock']={**adapter['task_lock'],**lr,'revision':lock['revision']}; adapter['ledger_tails']=tail
    adapter['current_mainline']={'task_id':TASK,'status':args.status,'current_visual_unit':'FROZEN_R4_PHOTO_NEW_WORDMARK_TYPOGRAPHY','evidence':{'execution':take['receipt'],'human_verdict':lock['candidate88_human_final_review']},'next_required_action':args.next,'codex_takeover':copy.deepcopy(take)}
    if take.get('reuse_entry'):
        adapter['workflow']['current_bounded_delivery_entry']=take['reuse_entry']
    fresh_remote=remote_head()
    if fresh_remote!=remote:raise ValueError('REMOTE_ADVANCED_DURING_PREPARATION')
    if any(p.read_bytes()!=v for p,v in originals.items()):raise ValueError('LOCAL_CONCURRENT_STATE_WRITE')
    for rel in [LOCK,CP,ADAPTER]:
        p=ROOT/BASE/'history'/('revision_'+str(lock['revision']-1))/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(evidence_bytes(ROOT/rel))
    write_transaction({ROOT/LOCK:encoded(lock),ROOT/CP:encoded(cp),ROOT/ADAPTER:encoded(adapter),ROOT/ledger:new_ledger})
    print(json.dumps({'revision':lock['revision'],'checkpoint':cp['sequence'],'next':args.next,'remote_parent':remote},ensure_ascii=False))

if __name__=='__main__':
    import sys
    sys.path.insert(0,str(ROOT))
    main()
