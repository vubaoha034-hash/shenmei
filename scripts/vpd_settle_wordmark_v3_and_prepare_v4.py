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
V3_EXEC=ROOT/'evidence/vpd/p1_typography_repair_v3/SEMANTIC_ANCHOR_WORDMARK_V3_EXECUTION_20260914.json'
EVID=ROOT/'evidence/vpd/p1_typography_repair_v4/WORDMARK_V3_HUMAN_DIRECTIONAL_FAIL_AND_V4_PLAN_20260914.json'
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
    if '"P1_EXECUTE_STRUCTURAL_WORDMARK_V4",' not in text:
        needle='    "P1_WAIT_HUMAN_SEMANTIC_ANCHOR_WORDMARK_V3_VERDICT",\n}'
        if needle not in text: raise SystemExit('ACTIONS insertion point missing')
        text=text.replace(needle,'    "P1_WAIT_HUMAN_SEMANTIC_ANCHOR_WORDMARK_V3_VERDICT",\n    "P1_EXECUTE_STRUCTURAL_WORDMARK_V4",\n}')
    if 'elif action == "P1_EXECUTE_STRUCTURAL_WORDMARK_V4":' not in text:
        needle='    require(not set(cp["completed"]) & set(cp["incomplete"]), "COMPLETED_AND_INCOMPLETE")'
        if needle not in text: raise SystemExit('validator branch insertion point missing')
        branch='''    elif action == "P1_EXECUTE_STRUCTURAL_WORDMARK_V4":
        tr = lock["typography_repair"]
        require(tr["status"] == "WORDMARK_V3_DIRECTIONAL_IMPROVEMENT_V4_READY", "WORDMARK_V4_READY_STATE")
        require(tr["phase"] == "STRUCTURAL_WORDMARK_V4", "WORDMARK_V4_PHASE")
        require(tr["wordmark_v4_render_allowed"] is True, "WORDMARK_V4_RENDER_NOT_OPEN")
        require(tr["wordmark_v4_direction_budget"] == {"豆坊":3,"茶作":3}, "WORDMARK_V4_BUDGET")
        require(tr["wordmark_v3_human_verdict"] == {"豆坊":"IMPROVED_NOT_PASS","茶作":"IMPROVED_NOT_PASS","overall":"FAIL_FAR_FROM_SHANYEJI_CONTINUE_TYPOGRAPHY_ONLY"}, "WORDMARK_V3_HUMAN_VERDICT_DRIFT")
        require(tr["support_typography_bench_allowed"] is False and tr["poster_reintegration_allowed"] is False, "WORDMARK_V4_PREMATURE_ADVANCE")
        check_ref(root, tr["wordmark_v3_execution"])
        check_ref(root, tr["wordmark_v3_human_fail_and_v4_plan"])

'''
        text=text.replace(needle,branch+needle)
    VALIDATOR.write_text(text,encoding='utf-8')

def main():
    lock=load(LOCK); cp=load(CP); adapter=load(ADAPTER)
    if lock.get('revision')!=41: raise SystemExit('unexpected source revision')
    if lock.get('next_required_action')!='P1_WAIT_HUMAN_SEMANTIC_ANCHOR_WORDMARK_V3_VERDICT': raise SystemExit('unexpected source action')
    tr=lock['typography_repair']
    if tr.get('status')!='SEMANTIC_ANCHOR_WORDMARK_V3_EXECUTED_WAITING_HUMAN_REVIEW': raise SystemExit('unexpected typography state')
    v3=load(V3_EXEC)
    if v3.get('status')!='EXECUTED_FROZEN_WAITING_HUMAN_REVIEW': raise SystemExit('wordmark v3 execution not frozen')
    recorded=now(); old_blob=blob('continuity/vpd/CURRENT_TASK_LOCK.json')
    evidence={
      'schema_version':'vpd-wordmark-v3-human-directional-fail-v4-plan/v1',
      'recorded_at':recorded,
      'human_authority':'CURRENT_USER',
      'human_feedback_exact':'V3 确实 两个确实好一些     但是 离山野集   差很多。',
      'wordmark_v3_human_verdict':{
        '豆坊':'IMPROVED_NOT_PASS',
        '茶作':'IMPROVED_NOT_PASS',
        'overall':'FAIL_FAR_FROM_SHANYEJI_CONTINUE_TYPOGRAPHY_ONLY'
      },
      'v3_assessment':{
        'improvements_to_preserve':[
          'both V3 titles are visibly better than V2',
          'V3 keeps V2 readability and broad wordmark coherence',
          'V3 begins to read as one connected graphic object rather than two unrelated characters'
        ],
        'blocking_failure':'authored maturity remains far below the approved Shanyeji mother reference; the structural identity is still too constructed and not inevitable/natural enough',
        'formal_verdict':'DIRECTIONAL_IMPROVEMENT_ONLY_NOT_PASS'
      },
      'anti_rollback':{
        'preserve_photography_and_photo_directional_gains':True,
        'preserve_current_overall_visual_direction_improvements':True,
        'preserve_V2_legibility_and_coherence':True,
        'preserve_V3_connected_wordmark_gain':True,
        'do_not_modify_P6':True,
        'do_not_regenerate_photo_bases':True,
        'do_not_restart_from_candidate1_baseline':True,
        'do_not_treat_local_typography_feedback_as_total_project_rejection':True
      },
      'wordmark_v4':{
        'id':'STRUCTURAL_WORDMARK_RECONSTRUCTION_V4',
        'strategy':'fork the frozen V3 final wordmarks and explore three whole-word structures per title before any polish; select structure first, polish second',
        'fork_from':'SEMANTIC_ANCHOR_WORDMARK_V3_FINAL_GROUPS',
        'five_high_leverage_variables':[
          'whole-word silhouette before local glyph decoration',
          'shared stroke DNA inherited from V3',
          'controlled asymmetric mass between anchor and secondary glyph',
          'coordinated negative-space topology crossing the word boundary',
          'one semantic abstraction expressed at word level rather than added as decoration'
        ],
        'directions':{
          'A_MASS_BLOCK':'dense integrated silhouette; shared canopy/baseline mass; strongest single-object reading',
          'B_NEGATIVE_CHANNEL':'a coordinated negative-space channel cuts across both characters and creates the identity',
          'C_ANCHOR_DOMINANT':'semantic anchor carries larger mass and secondary glyph nests/interlocks as support'
        },
        'title_semantics':{
          '豆坊':'bean/tofu workshop; compression/mold/block; warm handcraft solidity',
          '茶作':'tea craft; leaf/tray/layer; lifted vertical rhythm and processing layers'
        },
        'budget':{'directions_per_title':3,'total_visible_directions':6,'hidden_variants':0,'preselection_polish_passes':0},
        'forbidden':[
          'photo regeneration','P6 edits','restart from Candidate 1','font swap as primary move','independent per-glyph style invention','texture used to hide weak structure','support typography before structural selection'
        ],
        'selection_gate':[
          'immediately readable','one coherent authored system','materially stronger structural identity than V3','meaningfully closer to Shanyeji maturity without copying literal glyph shapes'
        ]
      },
      'T2_allowed':False,
      'P6_reintegration_allowed':False,
      'next_required_action':'P1_EXECUTE_STRUCTURAL_WORDMARK_V4'
    }
    dump(EVID,evidence); evid_ref=ref(EVID)
    lock['revision']=42
    lock['preserved_prior_revision']={'revision':41,'git_blob_sha':old_blob,'note':'Revision 41 executed and froze semantic-anchor V3 pending human review.'}
    lock['current_stage']='Human review says both V3 titles are genuinely better than V2 but still far from the approved Shanyeji maturity level. V3 gains are preserved. Photography/P3/P4/P6 gains remain frozen. Typography alone advances to a bounded V4 structural exploration with three visible whole-word directions per title, all forked from V3 rather than restarted.'
    lock['status']='VPD_P1_WORDMARK_V3_DIRECTIONAL_IMPROVEMENT_V4_STRUCTURAL_EXPLORATION_READY'
    lock['next_required_action']='P1_EXECUTE_STRUCTURAL_WORDMARK_V4'
    lock['completed_this_revision']=[
      'recorded the user human verdict that both V3 titles improved but still fail against the Shanyeji maturity target',
      'preserved V2 readability/coherence and V3 connected-wordmark gains',
      'preserved all photography, P3/P4 directional gains and P6 image state',
      'isolated the remaining gap to whole-word authored structural maturity',
      'prepared a V4 three-direction structural exploration per title with zero preselection polish'
    ]
    lock['blockers']=[
      'V3 outputs are human-rated as improved but not passed; freeze them as progress evidence.',
      'T2 support typography remains blocked until a V4 structure is selected and subsequently passes.',
      'P6 reintegration and photo regeneration remain blocked; prior image gains are preserved.',
      'Candidate promotion, Commercial, Golden and Scale remain blocked.'
    ]
    tr={**tr,
        'status':'WORDMARK_V3_DIRECTIONAL_IMPROVEMENT_V4_READY',
        'phase':'STRUCTURAL_WORDMARK_V4',
        'wordmark_v3_human_verdict':evidence['wordmark_v3_human_verdict'],
        'wordmark_v3_human_fail_and_v4_plan':evid_ref,
        'wordmark_v4_render_allowed':True,
        'wordmark_v4_direction_budget':{'豆坊':3,'茶作':3},
        'wordmark_v4_selected_direction':{'豆坊':None,'茶作':None},
        'support_typography_bench_allowed':False,
        'poster_reintegration_allowed':False,
        'next_required_action':'P1_EXECUTE_STRUCTURAL_WORDMARK_V4'}
    lock['typography_repair']=tr
    lock['wordmark_v3_human_fail_and_v4_plan_evidence']=evid_ref
    lock['updated_at']=recorded
    dump(LOCK,lock); lock_sha=sha(LOCK)

    prev=None
    for line in LEDGER.read_text(encoding='utf-8').splitlines():
        o=json.loads(line); prev={'event_id':o['event_id'],'event_hash':o['event_hash']}
    event={'schema_version':'upcp-state-ledger-event/v1','stream_id':'commercial_design_pipeline','event_id':'EVT-VPD-P1-WORDMARK-V3-DIRECTIONAL-FAIL-V4-READY-20260914-001','event_type':'WORDMARK_V3_DIRECTIONAL_IMPROVEMENT_V4_READY','task_id':lock['parent_active_task_id'],'project_id':lock['project_id'],'recorded_at':recorded,'material':True,'previous_event_id':prev['event_id'] if prev else None,'previous_event_hash':prev['event_hash'] if prev else None,'lock_sha256':lock_sha,'authorization':{'source':'current controlling ChatGPT conversation','authority':'user human verdict','exact_feedback':evidence['human_feedback_exact']},'before':{'state':'SEMANTIC_ANCHOR_WORDMARK_V3_EXECUTED_WAITING_HUMAN_REVIEW','next_action':'P1_WAIT_HUMAN_SEMANTIC_ANCHOR_WORDMARK_V3_VERDICT'},'after':{'state':lock['status'],'next_action':lock['next_required_action']},'evidence':[ref(V3_EXEC)['path'],evid_ref['path']],'reason':'Human review confirms directional improvement in both V3 titles but a large remaining gap to Shanyeji. Preserve the gains and explore whole-word structure rather than restarting or polishing a single path.','remote_authority':{'repository':lock['repository'],'branch':lock['branch']}}
    event['event_hash']=eh(event)
    with LEDGER.open('a',encoding='utf-8',newline='\n') as f: f.write(json.dumps(event,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n')

    cp['sequence']=64; cp['recorded_at']=recorded; cp['current_focus']=lock['current_stage']
    if 'p1_semantic_anchor_wordmark_v3_human_verdict' not in cp['completed']: cp['completed'].append('p1_semantic_anchor_wordmark_v3_human_verdict')
    cp['incomplete']=['p1_structural_wordmark_v4_execution','p1_structural_wordmark_v4_direction_selection','p1_typography_support_hierarchy_bench','p6_reintegration_after_typography_repair','candidate_promotion','second_style_family_validation','golden','scale']
    cp['blocked']=list(lock['blockers']); cp['next_required_action']=lock['next_required_action']; cp['status']=lock['status']; cp['task_lock']={'path':'continuity/vpd/CURRENT_TASK_LOCK.json','sha256':lock_sha}; cp['ledger_tails']={'commercial_design_pipeline':{'event_id':event['event_id'],'event_hash':event['event_hash']}}
    cp['typography_repair']={'status':tr['status'],'phase':tr['phase'],'wordmark_v3_execution':ref(V3_EXEC),'wordmark_v3_human_fail_and_v4_plan':evid_ref,'T2_allowed':False,'P6_reintegration_allowed':False,'next_required_action':lock['next_required_action']}
    dump(CP,cp)

    adapter['vpd_system_goal_authority']['checkpoint']=lock['status']; adapter['vpd_system_goal_authority']['next_required_action']=lock['next_required_action']; adapter['vpd_system_goal_authority']['render_allowed']=False
    adapter['task_lock']['revision']=42; adapter['task_lock']['sha256']=lock_sha
    adapter['forward_commercial_pipeline']['status']='PAUSED_FOR_P1_STRUCTURAL_WORDMARK_V4'; adapter['forward_commercial_pipeline']['next_required_action']=lock['next_required_action']
    adapter['change_authorities'].insert(0,{**evid_ref,'priority':0,'purpose':'Current human V3 directional-improvement-but-fail verdict and V4 structural exploration plan. Preserves image and typography gains while changing only whole-word structure.'})
    dump(ADAPTER,adapter)
    patch_validator()
    print(json.dumps({'status':lock['status'],'revision':42,'checkpoint_sequence':64,'next_required_action':lock['next_required_action'],'evidence':evid_ref,'lock_sha256':lock_sha},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
