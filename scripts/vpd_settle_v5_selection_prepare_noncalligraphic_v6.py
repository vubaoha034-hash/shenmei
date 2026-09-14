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
V5_EXEC=ROOT/'evidence/vpd/p1_typography_repair_v5/GENERATIVE_CUSTOM_WORDMARK_V5_EXECUTION_20260914.json'
EVID=ROOT/'evidence/vpd/p1_typography_repair_v6/V5_HUMAN_SELECTION_AND_NONCALLIGRAPHIC_V6_PLAN_20260914.json'
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
    action='    "P1_EXECUTE_NONCALLIGRAPHIC_SEMANTIC_WORDMARK_V6",\n'
    if action not in text:
        needle='    "P1_WAIT_HUMAN_GENERATIVE_CUSTOM_WORDMARK_V5_DIRECTION_VERDICT",\n}'
        if needle not in text: raise SystemExit('ACTIONS insertion point missing')
        text=text.replace(needle,'    "P1_WAIT_HUMAN_GENERATIVE_CUSTOM_WORDMARK_V5_DIRECTION_VERDICT",\n'+action+'}')
    branch='''    elif action == "P1_EXECUTE_NONCALLIGRAPHIC_SEMANTIC_WORDMARK_V6":
        tr = lock["typography_repair"]
        require(tr["status"] == "GENERATIVE_V5_HUMAN_SELECTION_NONCALLIGRAPHIC_V6_READY", "WORDMARK_V6_READY_STATE")
        require(tr["phase"] == "NONCALLIGRAPHIC_SEMANTIC_WORDMARK_V6", "WORDMARK_V6_PHASE")
        require(tr["wordmark_v6_generation_allowed"] is True, "WORDMARK_V6_GENERATION_NOT_OPEN")
        require(tr["wordmark_v5_selected_direction"] == {"豆坊":"B","茶作":"D"}, "WORDMARK_V5_SELECTION_DRIFT")
        require(tr["wordmark_v5_selection_status"] == "SELECTED_AS_SEEDS_NOT_PASS", "WORDMARK_V5_FALSE_PASS")
        require(tr["support_typography_bench_allowed"] is False and tr["poster_reintegration_allowed"] is False, "WORDMARK_V6_PREMATURE_ADVANCE")
        check_ref(root, tr["wordmark_v5_execution"])
        check_ref(root, tr["wordmark_v5_human_selection_and_v6_plan"])

'''
    if 'elif action == "P1_EXECUTE_NONCALLIGRAPHIC_SEMANTIC_WORDMARK_V6":' not in text:
        needle='    require(not set(cp["completed"]) & set(cp["incomplete"]), "COMPLETED_AND_INCOMPLETE")'
        if needle not in text: raise SystemExit('validator branch insertion point missing')
        text=text.replace(needle,branch+needle)
    VALIDATOR.write_text(text,encoding='utf-8')

def main():
    lock=load(LOCK); cp=load(CP); adapter=load(ADAPTER)
    if lock.get('revision')!=45: raise SystemExit('unexpected source revision')
    if lock.get('next_required_action')!='P1_WAIT_HUMAN_GENERATIVE_CUSTOM_WORDMARK_V5_DIRECTION_VERDICT': raise SystemExit('unexpected source action')
    tr=lock['typography_repair']
    if tr.get('status')!='GENERATIVE_CUSTOM_WORDMARK_V5_EXECUTED_WAITING_HUMAN_DIRECTION_VERDICT': raise SystemExit('unexpected typography state')
    v5=load(V5_EXEC)
    if v5.get('status')!='EXECUTED_FROZEN_WAITING_HUMAN_DIRECTION_VERDICT': raise SystemExit('V5 not frozen')
    recorded=now(); old_blob=blob('continuity/vpd/CURRENT_TASK_LOCK.json')
    evidence={
      'schema_version':'vpd-v5-human-selection-noncalligraphic-v6-plan/v1',
      'recorded_at':recorded,
      'human_authority':'CURRENT_USER',
      'human_feedback_exact':'豆坊选择 B，因为豆这个文字更符合豆的感觉；茶作 D 也可以。但是这个跟山野集还是差很多。',
      'selection':{'豆坊':'B','茶作':'D','status':'SELECTED_AS_SEEDS_NOT_PASS'},
      'selection_rationale':{
        '豆坊':'B is preferred because the 豆 glyph carries a more convincing bean-like semantic feeling.',
        '茶作':'D is acceptable as the strongest seed because the two-character relation is more coherent.'
      },
      'quality_verdict':'NOT_PASS_FAR_BELOW_SHANYEJI',
      'preserve':[
        'all photography and photo directional gains','P6 image state','V5 B bean-semantic cue','V5 D word-level continuity lesson'
      ],
      'method_change':{
        'why':'V5 improved over Figma-derived geometry but collapsed toward brush/calligraphic lettering; the next experiment must redesign glyph skeletons rather than beautify handwriting.',
        'figma_role':'Figma remains required later for vector reconstruction, optical correction, support typography, image-text composition and editable final delivery; it is not the primary glyph ideation medium in V6.'
      },
      'v6':{
        'id':'NONCALLIGRAPHIC_SEMANTIC_WORDMARK_V6',
        'goal':'Create genuinely authored Chinese wordmarks by reconstructing glyph skeletons while preserving immediate readability.',
        'seed_lessons':{'豆坊':'retain B bean/rounded semantic cue only, not its brush style','茶作':'retain D whole-word continuity only, not its brush style'},
        'high_leverage_variables':['semantic glyph reconstruction','non-uniform but shared stroke DNA','whole-word silhouette','cross-glyph negative-space topology','controlled asymmetric mass'],
        'hard_bans':['calligraphy','brush lettering','handwriting aesthetic as the solution','off-the-shelf font feeling','same brush treatment applied to both characters','texture used to fake design authorship','photo or poster decoration'],
        'budget':{'visible_concepts_per_title':6,'hidden_variants':0,'figma_glyph_ideation':False},
        'gate':['immediately readable','clearly not ordinary handwriting or a font swap','both characters belong to one system','semantic reconstruction is structural rather than decorative','materially closer to Shanyeji maturity without copying literal Shanyeji glyph shapes']
      },
      'T2_allowed':False,'P6_reintegration_allowed':False,
      'next_required_action':'P1_EXECUTE_NONCALLIGRAPHIC_SEMANTIC_WORDMARK_V6'
    }
    dump(EVID,evidence); er=ref(EVID)
    lock['revision']=46
    lock['preserved_prior_revision']={'revision':45,'git_blob_sha':old_blob,'note':'Revision 45 executed and froze V5 generative board pending human selection.'}
    lock['current_stage']='Human selects V5 豆坊 B and 茶作 D only as promising seeds, explicitly not as passes and still far below Shanyeji. Preserve all image gains. Typography advances to non-calligraphic semantic wordmark V6; Figma is reserved for later vector reconstruction and composition, not glyph ideation.'
    lock['status']='VPD_P1_GENERATIVE_V5_HUMAN_SELECTION_NONCALLIGRAPHIC_V6_READY'
    lock['next_required_action']='P1_EXECUTE_NONCALLIGRAPHIC_SEMANTIC_WORDMARK_V6'
    lock['completed_this_revision']=['recorded V5 human direction selection 豆坊 B / 茶作 D as seeds only','recorded explicit NOT PASS and far-below-Shanyeji verdict','preserved photography/P3/P4/P6 and prior typography evidence','changed only the typography ideation method from calligraphic generative exploration to non-calligraphic glyph reconstruction','kept Figma in the downstream vector/composition role']
    lock['blockers']=['V5 B/D are selected seeds, not approved wordmarks.','T2 remains blocked until V6 title review passes.','P6 reintegration and photo regeneration remain blocked; prior image gains are preserved.','Candidate promotion, Commercial, Golden and Scale remain blocked.']
    tr={**tr,'status':'GENERATIVE_V5_HUMAN_SELECTION_NONCALLIGRAPHIC_V6_READY','phase':'NONCALLIGRAPHIC_SEMANTIC_WORDMARK_V6','wordmark_v5_selected_direction':{'豆坊':'B','茶作':'D'},'wordmark_v5_selection_status':'SELECTED_AS_SEEDS_NOT_PASS','wordmark_v5_human_selection_and_v6_plan':er,'wordmark_v6_generation_allowed':True,'wordmark_v6_visible_concept_budget':{'豆坊':6,'茶作':6},'wordmark_v6_hidden_variants':0,'support_typography_bench_allowed':False,'poster_reintegration_allowed':False,'next_required_action':'P1_EXECUTE_NONCALLIGRAPHIC_SEMANTIC_WORDMARK_V6'}
    lock['typography_repair']=tr; lock['updated_at']=recorded
    dump(LOCK,lock); lock_sha=sha(LOCK)
    prev=None
    for line in LEDGER.read_text(encoding='utf-8').splitlines():
        o=json.loads(line); prev={'event_id':o['event_id'],'event_hash':o['event_hash']}
    event={'schema_version':'upcp-state-ledger-event/v1','stream_id':'commercial_design_pipeline','event_id':'EVT-VPD-P1-V5-HUMAN-SELECTION-V6-READY-20260914-001','event_type':'V5_HUMAN_SELECTION_NONCALLIGRAPHIC_V6_READY','task_id':lock['parent_active_task_id'],'project_id':lock['project_id'],'recorded_at':recorded,'material':True,'previous_event_id':prev['event_id'] if prev else None,'previous_event_hash':prev['event_hash'] if prev else None,'lock_sha256':lock_sha,'authorization':{'source':'current controlling ChatGPT conversation','authority':'user human verdict','exact_feedback':evidence['human_feedback_exact']},'before':{'state':'GENERATIVE_CUSTOM_WORDMARK_V5_EXECUTED_WAITING_HUMAN_DIRECTION_VERDICT','next_action':'P1_WAIT_HUMAN_GENERATIVE_CUSTOM_WORDMARK_V5_DIRECTION_VERDICT'},'after':{'state':lock['status'],'next_action':lock['next_required_action']},'evidence':[ref(V5_EXEC)['path'],er['path']],'reason':'User selects B/D only as seeds and explicitly says the work remains far below Shanyeji; switch typography ideation from brush/calligraphy to non-calligraphic structural reconstruction without touching photography.','remote_authority':{'repository':lock['repository'],'branch':lock['branch']}}
    event['event_hash']=eh(event)
    with LEDGER.open('a',encoding='utf-8',newline='\n') as f: f.write(json.dumps(event,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n')
    cp['sequence']=68; cp['recorded_at']=recorded; cp['current_focus']=lock['current_stage']
    if 'p1_generative_custom_wordmark_v5_direction_selection' not in cp['completed']: cp['completed'].append('p1_generative_custom_wordmark_v5_direction_selection')
    cp['incomplete']=['p1_noncalligraphic_semantic_wordmark_v6_execution','p1_noncalligraphic_semantic_wordmark_v6_direction_selection','p1_typography_support_hierarchy_bench','p6_reintegration_after_typography_repair','candidate_promotion','second_style_family_validation','golden','scale']
    cp['blocked']=list(lock['blockers']); cp['next_required_action']=lock['next_required_action']; cp['status']=lock['status']; cp['task_lock']={'path':'continuity/vpd/CURRENT_TASK_LOCK.json','sha256':lock_sha}; cp['ledger_tails']={'commercial_design_pipeline':{'event_id':event['event_id'],'event_hash':event['event_hash']}}
    cp['typography_repair']={'status':tr['status'],'phase':tr['phase'],'wordmark_v5_execution':ref(V5_EXEC),'wordmark_v5_human_selection_and_v6_plan':er,'selected_direction':tr['wordmark_v5_selected_direction'],'selection_status':tr['wordmark_v5_selection_status'],'T2_allowed':False,'P6_reintegration_allowed':False,'next_required_action':lock['next_required_action']}
    dump(CP,cp)
    adapter['vpd_system_goal_authority']['checkpoint']=lock['status']; adapter['vpd_system_goal_authority']['next_required_action']=lock['next_required_action']; adapter['vpd_system_goal_authority']['render_allowed']=False
    adapter['task_lock']['revision']=46; adapter['task_lock']['sha256']=lock_sha
    adapter['forward_commercial_pipeline']['status']='PAUSED_FOR_P1_NONCALLIGRAPHIC_SEMANTIC_WORDMARK_V6'; adapter['forward_commercial_pipeline']['next_required_action']=lock['next_required_action']
    adapter['change_authorities'].insert(0,{**er,'priority':0,'purpose':'Human V5 B/D seed selection, explicit far-below-Shanyeji non-pass verdict, and V6 non-calligraphic structural reconstruction plan.'})
    dump(ADAPTER,adapter)
    patch_validator()
    print(json.dumps({'status':lock['status'],'revision':46,'checkpoint_sequence':68,'next_required_action':lock['next_required_action'],'evidence':er,'lock_sha256':lock_sha},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
