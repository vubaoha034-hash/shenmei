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
V4_EXEC=ROOT/'evidence/vpd/p1_typography_repair_v4/STRUCTURAL_WORDMARK_V4_EXECUTION_20260914.json'
EVID=ROOT/'evidence/vpd/p1_typography_repair_v5/WORDMARK_V4_HUMAN_NONE_AND_GENERATIVE_V5_PLAN_20260914.json'
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
    if '"P1_EXECUTE_GENERATIVE_CUSTOM_WORDMARK_EXPLORATION_V5",' not in text:
        needle='    "P1_WAIT_HUMAN_STRUCTURAL_WORDMARK_V4_DIRECTION_VERDICT",\n}'
        if needle not in text: raise SystemExit('ACTIONS insertion point missing')
        text=text.replace(needle,'    "P1_WAIT_HUMAN_STRUCTURAL_WORDMARK_V4_DIRECTION_VERDICT",\n    "P1_EXECUTE_GENERATIVE_CUSTOM_WORDMARK_EXPLORATION_V5",\n}')
    if 'elif action == "P1_EXECUTE_GENERATIVE_CUSTOM_WORDMARK_EXPLORATION_V5":' not in text:
        needle='    require(not set(cp["completed"]) & set(cp["incomplete"]), "COMPLETED_AND_INCOMPLETE")'
        if needle not in text: raise SystemExit('validator branch insertion point missing')
        branch='''    elif action == "P1_EXECUTE_GENERATIVE_CUSTOM_WORDMARK_EXPLORATION_V5":
        tr = lock["typography_repair"]
        require(tr["status"] == "WORDMARK_V4_HUMAN_NONE_GENERATIVE_V5_READY", "WORDMARK_V5_READY_STATE")
        require(tr["phase"] == "GENERATIVE_CUSTOM_WORDMARK_V5", "WORDMARK_V5_PHASE")
        require(tr["wordmark_v5_generation_allowed"] is True, "WORDMARK_V5_GENERATION_NOT_OPEN")
        require(tr["wordmark_v4_human_direction_verdict"] == {"豆坊":"NONE","茶作":"NONE","overall":"FAIL_ALL_V4_STRUCTURES_NO_DESIGN_SENSE"}, "WORDMARK_V4_HUMAN_VERDICT_DRIFT")
        require(tr["support_typography_bench_allowed"] is False and tr["poster_reintegration_allowed"] is False, "WORDMARK_V5_PREMATURE_ADVANCE")
        check_ref(root, tr["wordmark_v4_execution"])
        check_ref(root, tr["wordmark_v4_human_none_and_v5_plan"])

'''
        text=text.replace(needle,branch+needle)
    VALIDATOR.write_text(text,encoding='utf-8')

def main():
    lock=load(LOCK); cp=load(CP); adapter=load(ADAPTER)
    if lock.get('revision')!=43: raise SystemExit('unexpected source revision')
    if lock.get('next_required_action')!='P1_WAIT_HUMAN_STRUCTURAL_WORDMARK_V4_DIRECTION_VERDICT': raise SystemExit('unexpected source action')
    tr=lock['typography_repair']
    if tr.get('status')!='STRUCTURAL_WORDMARK_V4_EXECUTED_WAITING_HUMAN_DIRECTION_VERDICT': raise SystemExit('unexpected typography state')
    v4=load(V4_EXEC)
    if v4.get('status')!='EXECUTED_FROZEN_WAITING_HUMAN_DIRECTION_VERDICT': raise SystemExit('wordmark v4 execution not frozen')
    recorded=now(); old_blob=blob('continuity/vpd/CURRENT_TASK_LOCK.json')
    evidence={
      'schema_version':'vpd-wordmark-v4-human-none-generative-v5-plan/v1',
      'recorded_at':recorded,
      'human_authority':'CURRENT_USER',
      'human_feedback_exact':'都不行，这看起来虽然比以前好点，但是依旧完全没有任何设计感。我不知道为什么',
      'wordmark_v4_human_direction_verdict':{'豆坊':'NONE','茶作':'NONE','overall':'FAIL_ALL_V4_STRUCTURES_NO_DESIGN_SENSE'},
      'diagnosis':{
        'positive_to_preserve':['V3/V4 are somewhat better than the earliest typography attempts','readability is no longer the main failure','the whole-word coherence direction is conceptually useful'],
        'blocking_failure':'the Figma-derived path is still manipulating a pre-existing glyph skeleton with added bars/cuts/bridges rather than authoring the glyph forms themselves; complexity increased without convincing design authorship',
        'formal_verdict':'FAIL_FIGMA_DERIVED_GEOMETRIC_MODULATION_AESTHETIC_CEILING'
      },
      'anti_rollback':{
        'preserve_photography_and_photo_directional_gains':True,
        'preserve_current_overall_visual_direction_improvements':True,
        'preserve_V2_readability_and_V3_word_coherence_lessons':True,
        'preserve_V4_as_negative_evidence':True,
        'do_not_modify_P6':True,
        'do_not_regenerate_photo_bases':True,
        'do_not_treat_typography_failure_as_project_reset':True
      },
      'wordmark_v5':{
        'id':'GENERATIVE_CUSTOM_WORDMARK_EXPLORATION_V5',
        'strategy':'move ideation out of Figma: generate whole custom Chinese wordmarks as visual objects first; Figma returns only after a visually convincing direction is selected',
        'reference_authority':'approved Shanyeji mother-reference mechanism and distilled family evidence only; feedback images are not promoted to mother reference',
        'five_high_leverage_variables':['whole-word silhouette authored from scratch','shared stroke DNA across both glyphs','controlled asymmetric mass','coordinated negative-space rhythm','one semantic abstraction embedded in glyph structure rather than added as decoration'],
        'titles':{
          '豆坊':{'semantic_domain':'豆腐/豆坊手作；凝聚、压制、模具、温润厚实','visible_concepts':6},
          '茶作':{'semantic_domain':'制茶手作；叶、竹匾、层次、提气、清透但有骨性','visible_concepts':6}
        },
        'presentation':'pure wordmark studies on simple dark/light field; no photography, no English support text, no badges, no poster decoration',
        'correctness_hard_gate':['exact text must read 豆坊 or 茶作 at first glance','no wrong radicals or invented substitute characters'],
        'taste_goal':'materially closer to the authored maturity and inevitability of the approved Shanyeji reference, without copying its literal glyph shapes',
        'forbidden':['photo regeneration','P6 edits','Figma-first glyph authoring','adding geometric bars as a substitute for glyph design','texture used to hide weak structure','promoting a feedback image to reference authority','T2 before title pass'],
        'selection_rule':'show all visible concepts; user may select one, several, or NONE; no hidden best-of filtering'
      },
      'T2_allowed':False,
      'P6_reintegration_allowed':False,
      'next_required_action':'P1_EXECUTE_GENERATIVE_CUSTOM_WORDMARK_EXPLORATION_V5'
    }
    dump(EVID,evidence); evid_ref=ref(EVID)
    lock['revision']=44
    lock['preserved_prior_revision']={'revision':43,'git_blob_sha':old_blob,'note':'Revision 43 executed and froze three V4 Figma-derived structural directions per title pending human selection.'}
    lock['current_stage']='Human review rejects all six V4 structural directions. They are somewhat better than early attempts but still lack convincing design authorship. Preserve every image-direction gain and typography learning, stop Figma as the primary glyph ideation medium, and advance typography only to a bounded generative custom-wordmark V5 exploration. Figma is reserved for later vector reconstruction/refinement after a human-selected visual direction.'
    lock['status']='VPD_P1_WORDMARK_V4_HUMAN_NONE_GENERATIVE_V5_READY'
    lock['next_required_action']='P1_EXECUTE_GENERATIVE_CUSTOM_WORDMARK_EXPLORATION_V5'
    lock['completed_this_revision']=[
      'recorded human NONE selection for all V4 豆坊 and 茶作 structures',
      'preserved the fact that V4 is somewhat better than early attempts without misclassifying it as acceptable design',
      'preserved photography, P3/P4 directional gains, P6 image state and prior typography progress',
      'diagnosed the current aesthetic ceiling as Figma-derived geometric modulation of an inherited glyph skeleton',
      'prepared a bounded generative custom-wordmark V5 exploration before any return to Figma'
    ]
    lock['blockers']=[
      'V4 outputs are human-rejected and frozen as negative/diagnostic evidence; do not polish them in place.',
      'T2 support typography remains blocked until a V5 title direction is selected and subsequently passes.',
      'P6 reintegration and photo regeneration remain blocked; prior image gains are preserved.',
      'Candidate promotion, Commercial, Golden and Scale remain blocked.'
    ]
    tr={**tr,
        'status':'WORDMARK_V4_HUMAN_NONE_GENERATIVE_V5_READY',
        'phase':'GENERATIVE_CUSTOM_WORDMARK_V5',
        'wordmark_v4_human_direction_verdict':evidence['wordmark_v4_human_direction_verdict'],
        'wordmark_v4_human_none_and_v5_plan':evid_ref,
        'wordmark_v5_generation_allowed':True,
        'wordmark_v5_visible_concept_budget':{'豆坊':6,'茶作':6},
        'wordmark_v5_selected_direction':{'豆坊':None,'茶作':None},
        'support_typography_bench_allowed':False,
        'poster_reintegration_allowed':False,
        'next_required_action':'P1_EXECUTE_GENERATIVE_CUSTOM_WORDMARK_EXPLORATION_V5'}
    lock['typography_repair']=tr
    lock['wordmark_v4_human_none_and_v5_plan_evidence']=evid_ref
    lock['updated_at']=recorded
    dump(LOCK,lock); lock_sha=sha(LOCK)

    prev=None
    for line in LEDGER.read_text(encoding='utf-8').splitlines():
        o=json.loads(line); prev={'event_id':o['event_id'],'event_hash':o['event_hash']}
    event={'schema_version':'upcp-state-ledger-event/v1','stream_id':'commercial_design_pipeline','event_id':'EVT-VPD-P1-WORDMARK-V4-HUMAN-NONE-V5-READY-20260914-001','event_type':'WORDMARK_V4_HUMAN_NONE_GENERATIVE_V5_READY','task_id':lock['parent_active_task_id'],'project_id':lock['project_id'],'recorded_at':recorded,'material':True,'previous_event_id':prev['event_id'] if prev else None,'previous_event_hash':prev['event_hash'] if prev else None,'lock_sha256':lock_sha,'authorization':{'source':'current controlling ChatGPT conversation','authority':'user human verdict','exact_feedback':evidence['human_feedback_exact']},'before':{'state':'STRUCTURAL_WORDMARK_V4_EXECUTED_WAITING_HUMAN_DIRECTION_VERDICT','next_action':'P1_WAIT_HUMAN_STRUCTURAL_WORDMARK_V4_DIRECTION_VERDICT'},'after':{'state':lock['status'],'next_action':lock['next_required_action']},'evidence':[ref(V4_EXEC)['path'],evid_ref['path']],'reason':'Human rejects all V4 structures. Preserve image and typography progress but stop Figma-derived glyph ideation and move only the title layer to generative custom-wordmark exploration.','remote_authority':{'repository':lock['repository'],'branch':lock['branch']}}
    event['event_hash']=eh(event)
    with LEDGER.open('a',encoding='utf-8',newline='\n') as f: f.write(json.dumps(event,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n')

    cp['sequence']=66; cp['recorded_at']=recorded; cp['current_focus']=lock['current_stage']
    if 'p1_structural_wordmark_v4_direction_selection' not in cp['completed']: cp['completed'].append('p1_structural_wordmark_v4_direction_selection')
    cp['incomplete']=['p1_generative_custom_wordmark_v5_execution','p1_generative_custom_wordmark_v5_direction_selection','p1_typography_support_hierarchy_bench','p6_reintegration_after_typography_repair','candidate_promotion','second_style_family_validation','golden','scale']
    cp['blocked']=list(lock['blockers']); cp['next_required_action']=lock['next_required_action']; cp['status']=lock['status']; cp['task_lock']={'path':'continuity/vpd/CURRENT_TASK_LOCK.json','sha256':lock_sha}; cp['ledger_tails']={'commercial_design_pipeline':{'event_id':event['event_id'],'event_hash':event['event_hash']}}
    cp['typography_repair']={'status':tr['status'],'phase':tr['phase'],'wordmark_v4_execution':ref(V4_EXEC),'wordmark_v4_human_none_and_v5_plan':evid_ref,'T2_allowed':False,'P6_reintegration_allowed':False,'next_required_action':lock['next_required_action']}
    dump(CP,cp)

    adapter['vpd_system_goal_authority']['checkpoint']=lock['status']; adapter['vpd_system_goal_authority']['next_required_action']=lock['next_required_action']; adapter['vpd_system_goal_authority']['render_allowed']=False
    adapter['task_lock']['revision']=44; adapter['task_lock']['sha256']=lock_sha
    adapter['forward_commercial_pipeline']['status']='PAUSED_FOR_P1_GENERATIVE_CUSTOM_WORDMARK_V5'; adapter['forward_commercial_pipeline']['next_required_action']=lock['next_required_action']
    adapter['change_authorities'].insert(0,{**evid_ref,'priority':0,'purpose':'Current human V4 NONE verdict and bounded V5 generative custom-wordmark plan. Preserves all image-direction gains while changing only title ideation medium.'})
    dump(ADAPTER,adapter)
    patch_validator()
    print(json.dumps({'status':lock['status'],'revision':44,'checkpoint_sequence':66,'next_required_action':lock['next_required_action'],'evidence':evid_ref,'lock_sha256':lock_sha},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
