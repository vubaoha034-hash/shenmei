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
PLAN=ROOT/'evidence/vpd/p1_typography_repair_v4/WORDMARK_V3_HUMAN_DIRECTIONAL_FAIL_AND_V4_PLAN_20260914.json'
EVID=ROOT/'evidence/vpd/p1_typography_repair_v4/STRUCTURAL_WORDMARK_V4_EXECUTION_20260914.json'
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
    if '"P1_WAIT_HUMAN_STRUCTURAL_WORDMARK_V4_DIRECTION_VERDICT",' not in text:
        needle='    "P1_EXECUTE_STRUCTURAL_WORDMARK_V4",\n}'
        if needle not in text: raise SystemExit('ACTIONS insertion point missing')
        text=text.replace(needle,'    "P1_EXECUTE_STRUCTURAL_WORDMARK_V4",\n    "P1_WAIT_HUMAN_STRUCTURAL_WORDMARK_V4_DIRECTION_VERDICT",\n}')
    if 'elif action == "P1_WAIT_HUMAN_STRUCTURAL_WORDMARK_V4_DIRECTION_VERDICT":' not in text:
        needle='    require(not set(cp["completed"]) & set(cp["incomplete"]), "COMPLETED_AND_INCOMPLETE")'
        if needle not in text: raise SystemExit('validator branch insertion point missing')
        branch='''    elif action == "P1_WAIT_HUMAN_STRUCTURAL_WORDMARK_V4_DIRECTION_VERDICT":
        tr = lock["typography_repair"]
        require(tr["status"] == "STRUCTURAL_WORDMARK_V4_EXECUTED_WAITING_HUMAN_DIRECTION_VERDICT", "WORDMARK_V4_EXECUTION_STATE")
        require(tr["phase"] == "STRUCTURAL_WORDMARK_V4", "WORDMARK_V4_PHASE")
        require(tr["wordmark_v4_render_allowed"] is False, "WORDMARK_V4_SHOULD_BE_FROZEN")
        require(tr["wordmark_v4_direction_budget"] == {"豆坊":3,"茶作":3}, "WORDMARK_V4_BUDGET")
        require(tr["wordmark_v4_visible_directions_generated"] == {"豆坊":3,"茶作":3}, "WORDMARK_V4_VISIBLE_COUNT")
        require(tr["wordmark_v4_hidden_variants"] == 0 and tr["wordmark_v4_preselection_polish_passes"] == 0, "WORDMARK_V4_HIDDEN_WORK")
        require(tr["wordmark_v4_selected_direction"] == {"豆坊":None,"茶作":None}, "WORDMARK_V4_PREMATURE_SELECTION")
        require(tr["support_typography_bench_allowed"] is False and tr["poster_reintegration_allowed"] is False, "WORDMARK_V4_PREMATURE_ADVANCE")
        require(tr["wordmark_v3_human_verdict"] == {"豆坊":"IMPROVED_NOT_PASS","茶作":"IMPROVED_NOT_PASS","overall":"FAIL_FAR_FROM_SHANYEJI_CONTINUE_TYPOGRAPHY_ONLY"}, "WORDMARK_V3_VERDICT_DRIFT")
        check_ref(root, tr["wordmark_v3_human_fail_and_v4_plan"])
        check_ref(root, tr["wordmark_v4_execution"])

'''
        text=text.replace(needle,branch+needle)
    VALIDATOR.write_text(text,encoding='utf-8')

def main():
    lock=load(LOCK); cp=load(CP); adapter=load(ADAPTER)
    if lock.get('revision')!=42: raise SystemExit('unexpected source revision')
    if lock.get('next_required_action')!='P1_EXECUTE_STRUCTURAL_WORDMARK_V4': raise SystemExit('unexpected source action')
    tr=lock['typography_repair']
    if tr.get('status')!='WORDMARK_V3_DIRECTIONAL_IMPROVEMENT_V4_READY': raise SystemExit('unexpected typography state')
    plan=load(PLAN)
    if plan.get('next_required_action')!='P1_EXECUTE_STRUCTURAL_WORDMARK_V4': raise SystemExit('V4 plan not executable')
    recorded=now(); old_blob=blob('continuity/vpd/CURRENT_TASK_LOCK.json')
    evidence={
      'schema_version':'vpd-structural-wordmark-v4-execution/v1',
      'recorded_at':recorded,
      'status':'EXECUTED_FROZEN_WAITING_HUMAN_DIRECTION_VERDICT',
      'strategy':'STRUCTURAL_WORDMARK_RECONSTRUCTION_V4',
      'authority_plan':ref(PLAN),
      'figma':{
        'file_key':'uyDxOoN1iNDPpEHTKSUWg1',
        'page_id':'69:2',
        'page_name':'P1 Structural Wordmark V4',
        'v3_source_frames':{'豆坊':'66:3','茶作':'66:16'},
        'directions':{
          '豆坊':{'A_MASS_BLOCK':'69:3','B_NEGATIVE_CHANNEL':'69:20','C_ANCHOR_DOMINANT':'69:38'},
          '茶作':{'A_MASS_BLOCK':'69:55','B_NEGATIVE_CHANNEL':'69:71','C_ANCHOR_DOMINANT':'69:88'}
        }
      },
      'execution':{
        'visible_directions_generated':{'豆坊':3,'茶作':3},
        'hidden_variants':0,
        'preselection_polish_passes':0,
        'selection_before_generation':False,
        'direction_definitions':{
          'A_MASS_BLOCK':'denser shared silhouette / common mass and baseline logic',
          'B_NEGATIVE_CHANNEL':'coordinated negative channel crossing both characters',
          'C_ANCHOR_DOMINANT':'semantic anchor receives dominant mass while secondary glyph nests/supports'
        }
      },
      'preservation':{
        'photography_modified':False,
        'photo_bases_regenerated':False,
        'P6_modified':False,
        'candidate1_baselines_modified':False,
        'V2_final_vectors_modified':False,
        'V3_final_groups_modified':False,
        'V3_legibility_coherence_and_connected_wordmark_gains_used_as_starting_point':True,
        'overall_visual_direction_gains_preserved':True
      },
      'drive_review':{
        'presentation_id':'1YjnZKpLUhoQVClPu06ojvhF7iudkWdLXuSP8EeQkOwM',
        'title':'T1_V4_结构方向复判_20260914',
        'folder_id':'1TaQJeK5BGskE7gVXUL5yEfEDVNSSvCG9',
        'url':'https://docs.google.com/presentation/d/1YjnZKpLUhoQVClPu06ojvhF7iudkWdLXuSP8EeQkOwM/edit',
        'slides':[
          '豆坊: V3 -> A_MASS_BLOCK -> B_NEGATIVE_CHANNEL -> C_ANCHOR_DOMINANT',
          '茶作: V3 -> A_MASS_BLOCK -> B_NEGATIVE_CHANNEL -> C_ANCHOR_DOMINANT'
        ],
        'image_elements_readback_verified':8,
        'readback_verified':True
      },
      'human_direction_selection':{'豆坊':None,'茶作':None},
      'review_instruction':'Select A, B, C or NONE independently for each title. These are structural prototypes, not polished finals.',
      'T2_allowed':False,
      'P6_reintegration_allowed':False,
      'next_required_action':'P1_WAIT_HUMAN_STRUCTURAL_WORDMARK_V4_DIRECTION_VERDICT'
    }
    dump(EVID,evidence); evid_ref=ref(EVID)
    lock['revision']=43
    lock['preserved_prior_revision']={'revision':42,'git_blob_sha':old_blob,'note':'Revision 42 recorded V3 directional improvement but fail and authorized 3x2 V4 structural exploration.'}
    lock['current_stage']='Structural Wordmark V4 has generated exactly three visible, unpolished whole-word directions for 豆坊 and three for 茶作, all forked from preserved V3. No hidden variants or preselection polishing were used. The six directions are frozen for human structure selection; photography/P3/P4/P6 and prior typography evidence remain unchanged.'
    lock['status']='VPD_P1_STRUCTURAL_WORDMARK_V4_EXECUTED_WAITING_HUMAN_DIRECTION_VERDICT'
    lock['next_required_action']='P1_WAIT_HUMAN_STRUCTURAL_WORDMARK_V4_DIRECTION_VERDICT'
    lock['completed_this_revision']=[
      'generated exactly three visible whole-word V4 structure directions for 豆坊 and three for 茶作',
      'used zero hidden variants and zero preselection polish passes',
      'preserved V3 source frames and all photography/P3/P4/P6 state',
      'created and independently read back a two-slide Drive review deck with V3 plus A/B/C for each title',
      'froze V4 outputs pending human direction selection'
    ]
    lock['blockers']=[
      'V4 structural prototypes are frozen pending human A/B/C/NONE selection; no polishing is authorized before selection.',
      'T2 support typography remains blocked until selected V4 structures are subsequently refined and pass.',
      'P6 reintegration and photo regeneration remain blocked; prior image gains are preserved.',
      'Candidate promotion, Commercial, Golden and Scale remain blocked.'
    ]
    tr={**tr,
        'status':'STRUCTURAL_WORDMARK_V4_EXECUTED_WAITING_HUMAN_DIRECTION_VERDICT',
        'phase':'STRUCTURAL_WORDMARK_V4',
        'wordmark_v4_render_allowed':False,
        'wordmark_v4_visible_directions_generated':{'豆坊':3,'茶作':3},
        'wordmark_v4_hidden_variants':0,
        'wordmark_v4_preselection_polish_passes':0,
        'wordmark_v4_selected_direction':{'豆坊':None,'茶作':None},
        'wordmark_v4_execution':evid_ref,
        'drive_wordmark_v4_review':evidence['drive_review'],
        'support_typography_bench_allowed':False,
        'poster_reintegration_allowed':False,
        'next_required_action':'P1_WAIT_HUMAN_STRUCTURAL_WORDMARK_V4_DIRECTION_VERDICT'}
    lock['typography_repair']=tr
    lock['wordmark_v4_execution_evidence']=evid_ref
    lock['updated_at']=recorded
    dump(LOCK,lock); lock_sha=sha(LOCK)

    prev=None
    for line in LEDGER.read_text(encoding='utf-8').splitlines():
        o=json.loads(line); prev={'event_id':o['event_id'],'event_hash':o['event_hash']}
    event={'schema_version':'upcp-state-ledger-event/v1','stream_id':'commercial_design_pipeline','event_id':'EVT-VPD-P1-STRUCTURAL-WORDMARK-V4-EXECUTED-20260914-001','event_type':'STRUCTURAL_WORDMARK_V4_EXECUTED_WAITING_HUMAN_DIRECTION_VERDICT','task_id':lock['parent_active_task_id'],'project_id':lock['project_id'],'recorded_at':recorded,'material':True,'previous_event_id':prev['event_id'] if prev else None,'previous_event_hash':prev['event_hash'] if prev else None,'lock_sha256':lock_sha,'before':{'state':'WORDMARK_V3_DIRECTIONAL_IMPROVEMENT_V4_READY','next_action':'P1_EXECUTE_STRUCTURAL_WORDMARK_V4'},'after':{'state':lock['status'],'next_action':lock['next_required_action']},'evidence':[ref(PLAN)['path'],evid_ref['path']],'reason':'V4 executes the predeclared 3x2 structure exploration without hidden variants or polishing, preserving all previously accepted image and typography gains until human direction selection.','remote_authority':{'repository':lock['repository'],'branch':lock['branch']}}
    event['event_hash']=eh(event)
    with LEDGER.open('a',encoding='utf-8',newline='\n') as f: f.write(json.dumps(event,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n')

    cp['sequence']=65; cp['recorded_at']=recorded; cp['current_focus']=lock['current_stage']
    if 'p1_structural_wordmark_v4_execution' not in cp['completed']: cp['completed'].append('p1_structural_wordmark_v4_execution')
    cp['incomplete']=['p1_structural_wordmark_v4_direction_selection','p1_typography_support_hierarchy_bench','p6_reintegration_after_typography_repair','candidate_promotion','second_style_family_validation','golden','scale']
    cp['blocked']=list(lock['blockers']); cp['next_required_action']=lock['next_required_action']; cp['status']=lock['status']; cp['task_lock']={'path':'continuity/vpd/CURRENT_TASK_LOCK.json','sha256':lock_sha}; cp['ledger_tails']={'commercial_design_pipeline':{'event_id':event['event_id'],'event_hash':event['event_hash']}}
    cp['typography_repair']={'status':tr['status'],'phase':tr['phase'],'wordmark_v4_execution':evid_ref,'drive_review':evidence['drive_review'],'selected_direction':tr['wordmark_v4_selected_direction'],'T2_allowed':False,'P6_reintegration_allowed':False,'next_required_action':lock['next_required_action']}
    dump(CP,cp)

    adapter['vpd_system_goal_authority']['checkpoint']=lock['status']; adapter['vpd_system_goal_authority']['next_required_action']=lock['next_required_action']; adapter['vpd_system_goal_authority']['render_allowed']=False
    adapter['task_lock']['revision']=43; adapter['task_lock']['sha256']=lock_sha
    adapter['forward_commercial_pipeline']['status']='PAUSED_FOR_P1_STRUCTURAL_WORDMARK_V4_HUMAN_DIRECTION_SELECTION'; adapter['forward_commercial_pipeline']['next_required_action']=lock['next_required_action']
    adapter['change_authorities'].insert(0,{**evid_ref,'priority':0,'purpose':'Current V4 3x2 structural wordmark execution; six visible unpolished directions frozen for human selection with all prior gains preserved.'})
    dump(ADAPTER,adapter)
    patch_validator()
    print(json.dumps({'status':lock['status'],'revision':43,'checkpoint_sequence':65,'next_required_action':lock['next_required_action'],'evidence':evid_ref,'lock_sha256':lock_sha},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
