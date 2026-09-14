#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
LOCK=ROOT/'continuity/vpd/CURRENT_TASK_LOCK.json'
CP=ROOT/'continuity/vpd/LATEST_CHECKPOINT.json'
ADAPTER=ROOT/'PROJECT_CONTROL_ADAPTER.json'
LEDGER=ROOT/'continuity/vpd/state_ledger/commercial_design_pipeline.jsonl'
PLAN=ROOT/'evidence/vpd/p1_typography_repair_v3/WORDMARK_V2_HUMAN_FAIL_AND_V3_PLAN_20260914.json'
EVID=ROOT/'evidence/vpd/p1_typography_repair_v3/SEMANTIC_ANCHOR_WORDMARK_V3_EXECUTION_20260914.json'
VALIDATOR=ROOT/'visual_memory/vpd_p6_composition_state.py'

def load(p): return json.loads(p.read_text(encoding='utf-8'))
def dump(p,o): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p): return {'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)}
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def blob(path): return subprocess.check_output(['git','rev-parse',f'HEAD:{path}'],cwd=ROOT,text=True).strip()
def eh(o): return hashlib.sha256(json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def patch_validator():
    text=VALIDATOR.read_text(encoding='utf-8')
    if '"P1_WAIT_HUMAN_SEMANTIC_ANCHOR_WORDMARK_V3_VERDICT",' not in text:
        needle='    "P1_EXECUTE_SEMANTIC_ANCHOR_WORDMARK_V3",\n}'
        if needle not in text: raise SystemExit('validator action insertion point missing')
        text=text.replace(needle,'    "P1_EXECUTE_SEMANTIC_ANCHOR_WORDMARK_V3",\n    "P1_WAIT_HUMAN_SEMANTIC_ANCHOR_WORDMARK_V3_VERDICT",\n}')
    if 'elif action == "P1_WAIT_HUMAN_SEMANTIC_ANCHOR_WORDMARK_V3_VERDICT":' not in text:
        needle='    require(not set(cp["completed"]) & set(cp["incomplete"]), "COMPLETED_AND_INCOMPLETE")'
        if needle not in text: raise SystemExit('validator branch insertion point missing')
        branch='''    elif action == "P1_WAIT_HUMAN_SEMANTIC_ANCHOR_WORDMARK_V3_VERDICT":
        tr = lock["typography_repair"]
        require(tr["status"] == "SEMANTIC_ANCHOR_WORDMARK_V3_EXECUTED_WAITING_HUMAN_REVIEW", "WORDMARK_V3_EXECUTION_STATE")
        require(tr["phase"] == "SEMANTIC_ANCHOR_WORDMARK_V3", "WORDMARK_V3_PHASE")
        require(tr["wordmark_v3_render_allowed"] is False, "WORDMARK_V3_SHOULD_BE_FROZEN")
        require(tr["wordmark_v3_correction_passes_used"] == {"豆坊":1,"茶作":1}, "WORDMARK_V3_CORRECTION_BUDGET")
        require(tr["wordmark_v3_human_verdict"] is None, "WORDMARK_V3_PREMATURE_VERDICT")
        require(tr["support_typography_bench_allowed"] is False and tr["poster_reintegration_allowed"] is False, "WORDMARK_V3_PREMATURE_ADVANCE")
        require(tr["wordmark_v2_human_verdict"] == {"豆坊":"FAIL","茶作":"FAIL","overall":"FAIL_CONTINUE_TYPOGRAPHY_ONLY"}, "WORDMARK_V2_VERDICT_DRIFT")
        check_ref(root, tr["wordmark_v2_human_fail_and_v3_plan"])
        check_ref(root, tr["wordmark_v3_execution"])

'''
        text=text.replace(needle,branch+needle)
    VALIDATOR.write_text(text,encoding='utf-8')

def main():
    lock=load(LOCK); cp=load(CP); adapter=load(ADAPTER); plan=load(PLAN)
    if lock.get('revision')!=40: raise SystemExit('unexpected source revision')
    if lock.get('next_required_action')!='P1_EXECUTE_SEMANTIC_ANCHOR_WORDMARK_V3': raise SystemExit('unexpected source action')
    tr=lock['typography_repair']
    if tr.get('status')!='WORDMARK_V2_HUMAN_FAIL_SEMANTIC_ANCHOR_V3_READY': raise SystemExit('unexpected typography state')
    if tr.get('wordmark_v3_render_allowed') is not True: raise SystemExit('V3 render not authorized')
    if tr.get('wordmark_v3_correction_passes_used')!={'豆坊':0,'茶作':0}: raise SystemExit('V3 correction budget not fresh')
    recorded=now(); old_blob=blob('continuity/vpd/CURRENT_TASK_LOCK.json')
    evidence={
      'schema_version':'vpd-semantic-anchor-wordmark-v3-execution/v1',
      'recorded_at':recorded,
      'status':'EXECUTED_FROZEN_WAITING_HUMAN_REVIEW',
      'strategy':'SEMANTIC_ANCHOR_WORDMARK_V3',
      'authority_plan':ref(PLAN),
      'figma':{
        'file_key':'uyDxOoN1iNDPpEHTKSUWg1',
        'page_id':'66:2',
        'page_name':'P1 Semantic Anchor Wordmark V3',
        'frames':{'豆坊':'66:3','茶作':'66:16'},
        'final_groups':{'豆坊':'67:2','茶作':'67:17'},
        'v2_source_vectors':{'豆坊':'64:9','茶作':'64:14'}
      },
      'budget':{
        'primary_builds_used':{'豆坊':1,'茶作':1},
        'aesthetic_corrections_used':{'豆坊':1,'茶作':1},
        'aesthetic_corrections_remaining':0,
        'hidden_variants':0
      },
      'execution':{
        'primary_build_review':'Both first V3 primary builds visibly improved semantic anchoring but were internally rejected as insufficiently integrated whole-word graphic masses.',
        'single_correction':'The only allowed correction strengthened whole-word silhouette, shared baseline/sweep mass, coordinated negative cuts and inter-character binding while preserving V2 readability/coherence.',
        '豆坊':'Forked V2; 豆 is the semantic anchor. The corrected V3 introduces a press/mold-like counter, denser bean/workshop mass, a shared lower sweep/base, and coordinated cuts while retaining readable 豆坊.',
        '茶作':'Forked V2; 茶 is the semantic anchor. The corrected V3 introduces a broad leaf/tray canopy, stronger shared lower sweep and connector rhythm, and coordinated cuts while retaining readable 茶作.'
      },
      'preservation':{
        'photography_modified':False,
        'photo_bases_regenerated':False,
        'P6_modified':False,
        'candidate1_baselines_modified':False,
        'V2_final_vectors_modified':False,
        'V2_legibility_and_coherence_used_as_starting_point':True,
        'overall_visual_direction_gains_preserved':True
      },
      'drive_review':{
        'presentation_id':'12BWCYEZD6Oy3ef4ZhS8MuTm7gcgdIuIrYNgYCFdw8SQ',
        'title':'T1_V3_语义锚点字标复判_20260914',
        'folder_id':'1TaQJeK5BGskE7gVXUL5yEfEDVNSSvCG9',
        'url':'https://docs.google.com/presentation/d/12BWCYEZD6Oy3ef4ZhS8MuTm7gcgdIuIrYNgYCFdw8SQ/edit',
        'structure':['豆坊: frozen strong baseline -> V2 coherence stage -> V3 semantic anchor','茶作: frozen strong baseline -> V2 coherence stage -> V3 semantic anchor'],
        'readback_verified':True
      },
      'human_review_gate':{
        'questions':[
          'is each word immediately readable',
          'do both characters clearly belong to one authored system',
          'does V3 preserve V2 coherence while becoming materially more designed',
          'is V3 meaningfully closer to the approved Shanyeji maturity level without literal copying'
        ],
        'human_verdict':None
      },
      'T2_allowed':False,
      'P6_reintegration_allowed':False,
      'next_required_action':'P1_WAIT_HUMAN_SEMANTIC_ANCHOR_WORDMARK_V3_VERDICT'
    }
    dump(EVID,evidence); evid_ref=ref(EVID)
    lock['revision']=41
    lock['preserved_prior_revision']={'revision':40,'git_blob_sha':old_blob,'note':'Revision 40 recorded V2 human fail, preserved all prior gains and authorized semantic-anchor V3.'}
    lock['current_stage']='Semantic-anchor wordmark V3 has been executed for 豆坊 and 茶作 by forking frozen V2 final wordmarks. Each title used one primary build and exactly one aesthetic correction. V3 outputs are now frozen for human review. Photography, P6, Candidate 1 and V2 final vectors remain unchanged.'
    lock['status']='VPD_P1_SEMANTIC_ANCHOR_WORDMARK_V3_EXECUTED_WAITING_HUMAN_REVIEW'
    lock['next_required_action']='P1_WAIT_HUMAN_SEMANTIC_ANCHOR_WORDMARK_V3_VERDICT'
    lock['completed_this_revision']=[
      'executed semantic-anchor V3 for both 豆坊 and 茶作 by forking V2 final wordmarks',
      'internally rejected the first V3 primary builds as not integrated enough rather than presenting them as progress',
      'used exactly one allowed V3 aesthetic correction per title',
      'froze final V3 outputs with no photography, P6, Candidate 1 or V2 mutation',
      'created and independently read back a Drive three-stage review deck: baseline -> V2 -> V3'
    ]
    lock['blockers']=[
      'V3 outputs are frozen pending human review; no additional V3 aesthetic correction is authorized before the verdict.',
      'T2 support typography remains blocked until both V3 titles pass.',
      'P6 reintegration and photo regeneration remain blocked; prior image gains are preserved.',
      'Candidate promotion, Commercial, Golden and Scale remain blocked.'
    ]
    tr={**tr,
        'status':'SEMANTIC_ANCHOR_WORDMARK_V3_EXECUTED_WAITING_HUMAN_REVIEW',
        'phase':'SEMANTIC_ANCHOR_WORDMARK_V3',
        'wordmark_v3_render_allowed':False,
        'wordmark_v3_correction_passes_used':{'豆坊':1,'茶作':1},
        'wordmark_v3_human_verdict':None,
        'wordmark_v3_execution':evid_ref,
        'drive_v3_review':evidence['drive_review'],
        'support_typography_bench_allowed':False,
        'poster_reintegration_allowed':False,
        'next_required_action':'P1_WAIT_HUMAN_SEMANTIC_ANCHOR_WORDMARK_V3_VERDICT'}
    lock['typography_repair']=tr
    lock['semantic_anchor_wordmark_v3_execution_evidence']=evid_ref
    lock['updated_at']=recorded
    dump(LOCK,lock); lock_sha=sha(LOCK)

    prev=None
    for line in LEDGER.read_text(encoding='utf-8').splitlines():
        o=json.loads(line); prev={'event_id':o['event_id'],'event_hash':o['event_hash']}
    event={'schema_version':'upcp-state-ledger-event/v1','stream_id':'commercial_design_pipeline','event_id':'EVT-VPD-P1-SEMANTIC-ANCHOR-WORDMARK-V3-EXECUTED-20260914-001','event_type':'SEMANTIC_ANCHOR_WORDMARK_V3_EXECUTED_WAITING_HUMAN_REVIEW','task_id':lock['parent_active_task_id'],'project_id':lock['project_id'],'recorded_at':recorded,'material':True,'previous_event_id':prev['event_id'] if prev else None,'previous_event_hash':prev['event_hash'] if prev else None,'lock_sha256':lock_sha,'authorization':{'source':'revision-40 semantic-anchor V3 plan','authority':'current task lock'},'before':{'state':'WORDMARK_V2_HUMAN_FAIL_SEMANTIC_ANCHOR_V3_READY','next_action':'P1_EXECUTE_SEMANTIC_ANCHOR_WORDMARK_V3'},'after':{'state':lock['status'],'next_action':lock['next_required_action']},'evidence':[ref(PLAN)['path'],evid_ref['path']],'reason':'V3 was executed strictly as an incremental typography-only fork from V2, consumed the symmetric one-correction budget, preserved all photo/P6 gains and is frozen for human review.','remote_authority':{'repository':lock['repository'],'branch':lock['branch']}}
    event['event_hash']=eh(event)
    with LEDGER.open('a',encoding='utf-8',newline='\n') as f: f.write(json.dumps(event,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n')

    cp['sequence']=63; cp['recorded_at']=recorded; cp['current_focus']=lock['current_stage']
    if 'p1_semantic_anchor_wordmark_v3_execution' not in cp['completed']: cp['completed'].append('p1_semantic_anchor_wordmark_v3_execution')
    cp['incomplete']=['p1_semantic_anchor_wordmark_v3_human_verdict','p1_typography_support_hierarchy_bench','p6_reintegration_after_typography_repair','candidate_promotion','second_style_family_validation','golden','scale']
    cp['blocked']=list(lock['blockers']); cp['next_required_action']=lock['next_required_action']; cp['status']=lock['status']; cp['task_lock']={'path':'continuity/vpd/CURRENT_TASK_LOCK.json','sha256':lock_sha}; cp['ledger_tails']={'commercial_design_pipeline':{'event_id':event['event_id'],'event_hash':event['event_hash']}}
    cp['typography_repair']={'status':tr['status'],'phase':tr['phase'],'wordmark_v3_execution':evid_ref,'drive_v3_review':evidence['drive_review'],'T2_allowed':False,'P6_reintegration_allowed':False,'next_required_action':lock['next_required_action']}
    dump(CP,cp)

    adapter['vpd_system_goal_authority']['checkpoint']=lock['status']; adapter['vpd_system_goal_authority']['next_required_action']=lock['next_required_action']; adapter['vpd_system_goal_authority']['render_allowed']=False
    adapter['task_lock']['revision']=41; adapter['task_lock']['sha256']=lock_sha
    adapter['forward_commercial_pipeline']['status']='PAUSED_FOR_P1_SEMANTIC_ANCHOR_WORDMARK_V3_HUMAN_REVIEW'; adapter['forward_commercial_pipeline']['next_required_action']=lock['next_required_action']
    adapter['change_authorities'].insert(0,{**evid_ref,'priority':0,'purpose':'Current semantic-anchor Wordmark V3 execution; outputs frozen for human review with photography/P6 preserved.'})
    dump(ADAPTER,adapter)
    patch_validator()
    print(json.dumps({'status':lock['status'],'revision':41,'checkpoint_sequence':63,'next_required_action':lock['next_required_action'],'evidence':evid_ref,'drive_review':evidence['drive_review'],'lock_sha256':lock_sha},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
