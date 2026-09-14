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
EVID=ROOT/'evidence/vpd/p1_typography_repair_v2/WORDMARK_V2_EXECUTION_20260914.json'
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
    if '"P1_WAIT_HUMAN_WORDMARK_V2_VERDICT",' not in text:
        needle='    "P1_EXECUTE_WORDMARK_SYSTEM_REPAIR_V2",\n}'
        if needle not in text: raise SystemExit('ACTIONS insertion point missing')
        text=text.replace(needle,'    "P1_EXECUTE_WORDMARK_SYSTEM_REPAIR_V2",\n    "P1_WAIT_HUMAN_WORDMARK_V2_VERDICT",\n}')
    if 'elif action == "P1_WAIT_HUMAN_WORDMARK_V2_VERDICT":' not in text:
        needle='    require(not set(cp["completed"]) & set(cp["incomplete"]), "COMPLETED_AND_INCOMPLETE")'
        if needle not in text: raise SystemExit('branch insertion point missing')
        branch='''    elif action == "P1_WAIT_HUMAN_WORDMARK_V2_VERDICT":
        tr = lock["typography_repair"]
        require(tr["status"] == "WORDMARK_V2_EXECUTED_WAITING_HUMAN_REVIEW", "WORDMARK_V2_WAIT_STATE")
        require(tr["wordmark_v2_render_allowed"] is False, "WORDMARK_V2_SHOULD_BE_FROZEN")
        require(tr["wordmark_v2_correction_passes_used"] == {"豆坊": 1, "茶作": 1}, "WORDMARK_V2_BUDGET")
        require(tr["wordmark_v2_human_verdict"] is None, "WORDMARK_V2_PREMATURE_VERDICT")
        require(tr["support_typography_bench_allowed"] is False and tr["poster_reintegration_allowed"] is False, "WORDMARK_V2_PREMATURE_ADVANCE")
        for name in ("final_t1_settlement", "wordmark_v2_plan", "wordmark_v2_execution"):
            check_ref(root, tr[name])

'''
        text=text.replace(needle,branch+needle)
    VALIDATOR.write_text(text,encoding='utf-8')

def main():
    lock=load(LOCK); cp=load(CP); adapter=load(ADAPTER)
    if lock.get('revision')!=38: raise SystemExit('unexpected source revision')
    if lock.get('next_required_action')!='P1_EXECUTE_WORDMARK_SYSTEM_REPAIR_V2': raise SystemExit('unexpected source action')
    tr=lock['typography_repair']
    recorded=now(); old_blob=blob('continuity/vpd/CURRENT_TASK_LOCK.json')
    evidence={
      'schema_version':'vpd-wordmark-v2-execution/v1',
      'recorded_at':recorded,
      'status':'EXECUTED_FROZEN_WAITING_HUMAN_REVIEW',
      'scope':'P1_WORDMARK_SYSTEM_REPAIR_V2_TITLE_ONLY',
      'figma':{
        'file_key':'uyDxOoN1iNDPpEHTKSUWg1',
        'page_id':'63:2',
        'page_name':'P1 Wordmark System Repair V2',
        'doufang_frame':'63:3',
        'chazuo_frame':'63:9',
        'doufang_final_vector':'64:9',
        'chazuo_final_vector':'64:14'
      },
      'preservation':{
        'photos_modified':False,
        'P6_modified':False,
        'candidate1_baselines_modified':False,
        'prior_negative_evidence_modified':False,
        'overall_visual_direction_reset':False
      },
      'execution':{
        'primary_build':{
          'scaffold':'LXGW Marker Gothic Regular',
          'assistant_pixel_verdict':'REJECTED_BEFORE_USER_REVIEW_TOO_FONTLIKE_AND_TOO_FAR_FROM_MOTHER_REFERENCE'
        },
        'single_aesthetic_correction':{
          'used':True,
          'scaffold':'Noto Serif SC Black',
          'method':'word-level single text object -> outline -> unequal character mass -> tight wordmark spacing -> restrained shared terminal cuts',
          'doufang_used':1,
          'chazuo_used':1
        },
        'additional_hidden_corrections':0
      },
      'drive_review':{
        'folder_id':'1TaQJeK5BGskE7gVXUL5yEfEDVNSSvCG9',
        'presentation_id':'1HGpfLCzBad8aqgzBCqJwSiXQo-uOJY5EsUb_dINrojE',
        'title':'T1_V2_字标复判_20260914',
        'contains':['豆坊 frozen Candidate 1 vs V2 Candidate 2','茶作 frozen Candidate 1 vs V2 Candidate 2']
      },
      'human_review_required':True,
      'human_questions':[
        'Can the title be read immediately and unambiguously?',
        'Do both characters belong to one wordmark system?',
        'Is Candidate 2 materially more designed than the frozen Candidate 1 baseline?',
        'Is the authored quality meaningfully closer to the approved Shanyeji mother-reference level?'
      ],
      'wordmark_v2_human_verdict':None,
      'T2_allowed':False,
      'P6_reintegration_allowed':False,
      'next_required_action':'P1_WAIT_HUMAN_WORDMARK_V2_VERDICT'
    }
    dump(EVID,evidence); evid_ref=ref(EVID)
    lock['revision']=39
    lock['preserved_prior_revision']={'revision':38,'git_blob_sha':old_blob,'note':'Revision 38 stopped the failed T1 compiler, preserved image gains and opened wordmark-first V2.'}
    lock['current_stage']='Wordmark-first V2 has been executed for 豆坊 and 茶作 with frozen Candidate 1 baselines. The first V2 build was rejected internally as too font-like; exactly one aesthetic correction per title was then used. Final V2 Candidate 2 frames are frozen and awaiting human review. Photography/P6 remain untouched.'
    lock['status']='VPD_P1_WORDMARK_V2_EXECUTED_WAITING_HUMAN_REVIEW'
    lock['next_required_action']='P1_WAIT_HUMAN_WORDMARK_V2_VERDICT'
    lock['completed_this_revision']=[
      'executed wordmark-first V2 on a new isolated Figma page',
      'rejected the first primary build internally instead of presenting a known weak draft as progress',
      'used exactly one allowed V2 aesthetic correction for 豆坊 and one for 茶作',
      'froze the corrected V2 candidates with no photography/P6/baseline mutation',
      'created and moved a two-slide Drive review deck comparing frozen baselines to V2 candidates'
    ]
    lock['blockers']=[
      'V2 candidates are frozen pending human review; no additional aesthetic correction is authorized before the verdict.',
      'T2 support typography remains blocked until both V2 titles pass.',
      'P6 reintegration and photo regeneration remain blocked.',
      'Candidate promotion, Commercial, Golden and Scale remain blocked.'
    ]
    tr={**tr,
        'status':'WORDMARK_V2_EXECUTED_WAITING_HUMAN_REVIEW',
        'wordmark_v2_render_allowed':False,
        'wordmark_v2_correction_passes_used':{'豆坊':1,'茶作':1},
        'wordmark_v2_human_verdict':None,
        'wordmark_v2_execution':evid_ref,
        'drive_wordmark_v2_review':evidence['drive_review'],
        'next_required_action':'P1_WAIT_HUMAN_WORDMARK_V2_VERDICT'}
    lock['typography_repair']=tr
    lock['wordmark_v2_execution_evidence']=evid_ref
    lock['updated_at']=recorded
    dump(LOCK,lock); lock_sha=sha(LOCK)
    prev=None
    for line in LEDGER.read_text(encoding='utf-8').splitlines():
        o=json.loads(line); prev={'event_id':o['event_id'],'event_hash':o['event_hash']}
    event={'schema_version':'upcp-state-ledger-event/v1','stream_id':'commercial_design_pipeline','event_id':'EVT-VPD-P1-WORDMARK-V2-EXECUTED-20260914-001','event_type':'WORDMARK_V2_EXECUTED_WAITING_HUMAN_REVIEW','task_id':lock['parent_active_task_id'],'project_id':lock['project_id'],'recorded_at':recorded,'material':True,'previous_event_id':prev['event_id'] if prev else None,'previous_event_hash':prev['event_hash'] if prev else None,'lock_sha256':lock_sha,'before':{'state':'WORDMARK_V2_READY','next_action':'P1_EXECUTE_WORDMARK_SYSTEM_REPAIR_V2'},'after':{'state':lock['status'],'next_action':lock['next_required_action']},'evidence':[evid_ref['path'],tr['wordmark_v2_plan']['path']],'reason':'Wordmark-first V2 was executed under the bounded budget without touching retained photographic gains. Final candidates are frozen for human evaluation.','remote_authority':{'repository':lock['repository'],'branch':lock['branch']}}
    event['event_hash']=eh(event)
    with LEDGER.open('a',encoding='utf-8',newline='\n') as f: f.write(json.dumps(event,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n')
    cp['sequence']=61; cp['recorded_at']=recorded; cp['current_focus']=lock['current_stage']
    if 'p1_wordmark_system_repair_v2_execution' not in cp['completed']: cp['completed'].append('p1_wordmark_system_repair_v2_execution')
    cp['incomplete']=['p1_wordmark_system_repair_v2_human_verdict','p1_typography_support_hierarchy_bench','p6_reintegration_after_typography_repair','candidate_promotion','second_style_family_validation','golden','scale']
    cp['blocked']=list(lock['blockers']); cp['next_required_action']=lock['next_required_action']; cp['status']=lock['status']; cp['task_lock']={'path':'continuity/vpd/CURRENT_TASK_LOCK.json','sha256':lock_sha}; cp['ledger_tails']={'commercial_design_pipeline':{'event_id':event['event_id'],'event_hash':event['event_hash']}}
    cp['typography_repair']={'status':tr['status'],'phase':'WORDMARK_SYSTEM_REPAIR_V2','wordmark_v2_execution':evid_ref,'drive_review':evidence['drive_review'],'T2_allowed':False,'P6_reintegration_allowed':False,'next_required_action':lock['next_required_action']}
    dump(CP,cp)
    adapter['vpd_system_goal_authority']['checkpoint']=lock['status']; adapter['vpd_system_goal_authority']['next_required_action']=lock['next_required_action']; adapter['vpd_system_goal_authority']['render_allowed']=False
    adapter['task_lock']['revision']=39; adapter['task_lock']['sha256']=lock_sha
    adapter['forward_commercial_pipeline']['status']='PAUSED_FOR_P1_WORDMARK_V2_HUMAN_REVIEW'; adapter['forward_commercial_pipeline']['next_required_action']=lock['next_required_action']
    adapter['change_authorities'].insert(0,{**evid_ref,'priority':0,'purpose':'Current wordmark-first V2 execution receipt; candidates frozen for human review with prior image improvements preserved.'})
    dump(ADAPTER,adapter)
    patch_validator()
    print(json.dumps({'status':lock['status'],'revision':39,'checkpoint_sequence':61,'next_required_action':lock['next_required_action'],'execution':evid_ref,'lock_sha256':lock_sha},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
