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
V2_EXEC=ROOT/'evidence/vpd/p1_typography_repair_v2/WORDMARK_V2_EXECUTION_20260914.json'
EVID=ROOT/'evidence/vpd/p1_typography_repair_v3/WORDMARK_V2_HUMAN_FAIL_AND_V3_PLAN_20260914.json'
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
    if '"P1_EXECUTE_SEMANTIC_ANCHOR_WORDMARK_V3",' not in text:
        needle='    "P1_WAIT_HUMAN_WORDMARK_V2_VERDICT",\n}'
        if needle not in text: raise SystemExit('ACTIONS insertion point missing')
        text=text.replace(needle,'    "P1_WAIT_HUMAN_WORDMARK_V2_VERDICT",\n    "P1_EXECUTE_SEMANTIC_ANCHOR_WORDMARK_V3",\n}')
    if 'elif action == "P1_EXECUTE_SEMANTIC_ANCHOR_WORDMARK_V3":' not in text:
        needle='    require(not set(cp["completed"]) & set(cp["incomplete"]), "COMPLETED_AND_INCOMPLETE")'
        if needle not in text: raise SystemExit('validator branch insertion point missing')
        branch='''    elif action == "P1_EXECUTE_SEMANTIC_ANCHOR_WORDMARK_V3":
        tr = lock["typography_repair"]
        require(tr["status"] == "WORDMARK_V2_HUMAN_FAIL_SEMANTIC_ANCHOR_V3_READY", "WORDMARK_V3_READY_STATE")
        require(tr["phase"] == "SEMANTIC_ANCHOR_WORDMARK_V3", "WORDMARK_V3_PHASE")
        require(tr["wordmark_v3_render_allowed"] is True, "WORDMARK_V3_RENDER_NOT_OPEN")
        require(tr["support_typography_bench_allowed"] is False and tr["poster_reintegration_allowed"] is False, "WORDMARK_V3_PREMATURE_ADVANCE")
        require(tr["wordmark_v2_human_verdict"] == {"豆坊":"FAIL","茶作":"FAIL","overall":"FAIL_CONTINUE_TYPOGRAPHY_ONLY"}, "WORDMARK_V2_HUMAN_VERDICT_DRIFT")
        check_ref(root, tr["wordmark_v2_execution"])
        check_ref(root, tr["wordmark_v2_human_fail_and_v3_plan"])

'''
        text=text.replace(needle,branch+needle)
    VALIDATOR.write_text(text,encoding='utf-8')

def main():
    lock=load(LOCK); cp=load(CP); adapter=load(ADAPTER)
    if lock.get('revision')!=39: raise SystemExit('unexpected source revision')
    if lock.get('next_required_action')!='P1_WAIT_HUMAN_WORDMARK_V2_VERDICT': raise SystemExit('unexpected source action')
    tr=lock['typography_repair']
    if tr.get('status')!='WORDMARK_V2_EXECUTED_WAITING_HUMAN_REVIEW': raise SystemExit('unexpected typography state')
    v2=load(V2_EXEC)
    if v2.get('status')!='EXECUTED_FROZEN_WAITING_HUMAN_REVIEW': raise SystemExit('wordmark v2 execution not frozen')
    recorded=now(); old_blob=blob('continuity/vpd/CURRENT_TASK_LOCK.json')
    evidence={
      'schema_version':'vpd-wordmark-v2-human-fail-v3-plan/v1',
      'recorded_at':recorded,
      'human_authority':'CURRENT_USER',
      'human_feedback_exact':'豆坊不通过，茶作不通过，继续。',
      'wordmark_v2_human_verdict':{'豆坊':'FAIL','茶作':'FAIL','overall':'FAIL_CONTINUE_TYPOGRAPHY_ONLY'},
      'v2_assessment':{
        'improvements_to_preserve':[
          'legibility is materially better than the failed T1 technical retry',
          'both characters now share one broad typographic language instead of looking like two unrelated styles',
          'word-level spacing and mass are more coherent than the per-glyph compiler'
        ],
        'blocking_failures':[
          'authored quality remains too close to a selected display font plus proportion edits',
          'semantic graphic transformation is insufficient relative to the approved Shanyeji mother reference',
          'negative-space topology and wordmark silhouette are not distinctive enough',
          'the result is improved but still far from completion and cannot open T2'
        ],
        'formal_verdict':'FAIL_WORDMARK_V2_AUTHORED_QUALITY_NOT_ENOUGH'
      },
      'anti_rollback':{
        'preserve_photography_and_photo_directional_gains':True,
        'preserve_current_overall_visual_direction_improvements':True,
        'preserve_wordmark_v2_legibility_and_coherence_lessons':True,
        'do_not_modify_P6':True,
        'do_not_regenerate_photo_bases':True,
        'do_not_restart_from_candidate1_baseline':True,
        'feedback_scope_rule':'A local typography failure changes only the typography experiment unless the user explicitly rejects another layer.'
      },
      'wordmark_v3':{
        'id':'SEMANTIC_ANCHOR_WORDMARK_V3',
        'strategy':'fork V2 wordmark coherence, then add authored semantic transformation at the whole-word level',
        'fork_from':'WORDMARK_V2_FINAL_VECTORS',
        'titles':{
          '豆坊':{'semantic_anchor_glyph':'豆','secondary_glyph':'坊','semantic_domain':'bean/tofu workshop, press/mold/block process'},
          '茶作':{'semantic_anchor_glyph':'茶','secondary_glyph':'作','semantic_domain':'tea craft, leaf/tray/layered processing'}
        },
        'five_high_leverage_variables':[
          'shared stroke DNA preserved across both characters',
          'one semantic anchor glyph receives a strong but still readable graphic transformation',
          'the entire two-character silhouette is composed as one graphic mass',
          'negative spaces are authored as a coordinated system rather than accidental font counters',
          'controlled asymmetry and interlock create identity without independently redesigning each character'
        ],
        'forbidden':[
          'photo regeneration',
          'P6 edits',
          'starting over from Candidate 1',
          'independent per-glyph style invention',
          'font swap as the primary design move',
          'texture used to hide weak structure',
          'T2 support typography before both titles pass'
        ],
        'budget':{'primary_build_per_title':1,'aesthetic_correction_max_per_title':1,'hidden_variants':0},
        'pass_gate':[
          'both words are immediately readable',
          'both characters clearly belong to one system',
          'Candidate 2 has materially stronger authored identity than the frozen strong baseline',
          'the result is meaningfully closer to the approved Shanyeji mother-reference level without copying its literal glyph shapes',
          'no preserved photography or P6 state is changed'
        ]
      },
      'T2_allowed':False,
      'P6_reintegration_allowed':False,
      'next_required_action':'P1_EXECUTE_SEMANTIC_ANCHOR_WORDMARK_V3'
    }
    dump(EVID,evidence); evid_ref=ref(EVID)
    lock['revision']=40
    lock['preserved_prior_revision']={'revision':39,'git_blob_sha':old_blob,'note':'Revision 39 executed and froze wordmark-first V2 pending human review.'}
    lock['current_stage']='Human review rejects both wordmark V2 titles. The V2 coherence/legibility improvement is preserved, but authored identity remains too font-like and far below the approved Shanyeji reference. Photography and existing image-direction gains remain frozen. Typography alone advances to semantic-anchor wordmark V3, forked from the V2 final wordmarks rather than restarting from baseline.'
    lock['status']='VPD_P1_WORDMARK_V2_HUMAN_FAIL_SEMANTIC_ANCHOR_V3_READY'
    lock['next_required_action']='P1_EXECUTE_SEMANTIC_ANCHOR_WORDMARK_V3'
    lock['completed_this_revision']=[
      'recorded the user human verdict that both V2 titles fail',
      'preserved V2 legibility and wordmark coherence as positive evidence instead of resetting typography to baseline',
      'preserved all current photography, P3/P4 directional gains and overall visual-direction improvements',
      'isolated the remaining failure to insufficient authored wordmark identity and semantic graphic transformation',
      'prepared a semantic-anchor V3 experiment that forks from V2 and changes only typography'
    ]
    lock['blockers']=[
      'V2 outputs are human-rejected and frozen as intermediate positive/negative evidence; do not polish them in place.',
      'T2 support typography remains blocked until both semantic-anchor V3 titles pass.',
      'P6 reintegration and photo regeneration remain blocked; prior image gains are preserved.',
      'Candidate promotion, Commercial, Golden and Scale remain blocked.'
    ]
    tr={**tr,
        'status':'WORDMARK_V2_HUMAN_FAIL_SEMANTIC_ANCHOR_V3_READY',
        'phase':'SEMANTIC_ANCHOR_WORDMARK_V3',
        'wordmark_v2_human_verdict':evidence['wordmark_v2_human_verdict'],
        'wordmark_v2_human_fail_and_v3_plan':evid_ref,
        'wordmark_v3_render_allowed':True,
        'wordmark_v3_correction_passes_used':{'豆坊':0,'茶作':0},
        'support_typography_bench_allowed':False,
        'poster_reintegration_allowed':False,
        'next_required_action':'P1_EXECUTE_SEMANTIC_ANCHOR_WORDMARK_V3'}
    lock['typography_repair']=tr
    lock['wordmark_v2_human_fail_and_v3_plan_evidence']=evid_ref
    lock['updated_at']=recorded
    dump(LOCK,lock); lock_sha=sha(LOCK)

    prev=None
    for line in LEDGER.read_text(encoding='utf-8').splitlines():
        o=json.loads(line); prev={'event_id':o['event_id'],'event_hash':o['event_hash']}
    event={'schema_version':'upcp-state-ledger-event/v1','stream_id':'commercial_design_pipeline','event_id':'EVT-VPD-P1-WORDMARK-V2-HUMAN-FAIL-V3-READY-20260914-001','event_type':'WORDMARK_V2_HUMAN_FAIL_SEMANTIC_ANCHOR_V3_READY','task_id':lock['parent_active_task_id'],'project_id':lock['project_id'],'recorded_at':recorded,'material':True,'previous_event_id':prev['event_id'] if prev else None,'previous_event_hash':prev['event_hash'] if prev else None,'lock_sha256':lock_sha,'authorization':{'source':'current controlling ChatGPT conversation','authority':'user human verdict','exact_feedback':evidence['human_feedback_exact']},'before':{'state':'WORDMARK_V2_EXECUTED_WAITING_HUMAN_REVIEW','next_action':'P1_WAIT_HUMAN_WORDMARK_V2_VERDICT'},'after':{'state':lock['status'],'next_action':lock['next_required_action']},'evidence':[ref(V2_EXEC)['path'],evid_ref['path']],'reason':'Both V2 titles are human-rejected. Improvements in legibility/coherence remain preserved; only the insufficient authored typography layer advances to a bounded semantic-anchor V3 without touching photography or P6.','remote_authority':{'repository':lock['repository'],'branch':lock['branch']}}
    event['event_hash']=eh(event)
    with LEDGER.open('a',encoding='utf-8',newline='\n') as f: f.write(json.dumps(event,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n')

    cp['sequence']=62; cp['recorded_at']=recorded; cp['current_focus']=lock['current_stage']
    if 'p1_wordmark_system_repair_v2_human_verdict' not in cp['completed']: cp['completed'].append('p1_wordmark_system_repair_v2_human_verdict')
    cp['incomplete']=['p1_semantic_anchor_wordmark_v3_execution','p1_typography_support_hierarchy_bench','p6_reintegration_after_typography_repair','candidate_promotion','second_style_family_validation','golden','scale']
    cp['blocked']=list(lock['blockers']); cp['next_required_action']=lock['next_required_action']; cp['status']=lock['status']; cp['task_lock']={'path':'continuity/vpd/CURRENT_TASK_LOCK.json','sha256':lock_sha}; cp['ledger_tails']={'commercial_design_pipeline':{'event_id':event['event_id'],'event_hash':event['event_hash']}}
    cp['typography_repair']={'status':tr['status'],'phase':tr['phase'],'wordmark_v2_execution':ref(V2_EXEC),'wordmark_v2_human_fail_and_v3_plan':evid_ref,'T2_allowed':False,'P6_reintegration_allowed':False,'next_required_action':lock['next_required_action']}
    dump(CP,cp)

    adapter['vpd_system_goal_authority']['checkpoint']=lock['status']; adapter['vpd_system_goal_authority']['next_required_action']=lock['next_required_action']; adapter['vpd_system_goal_authority']['render_allowed']=False
    adapter['task_lock']['revision']=40; adapter['task_lock']['sha256']=lock_sha
    adapter['forward_commercial_pipeline']['status']='PAUSED_FOR_P1_SEMANTIC_ANCHOR_WORDMARK_V3'; adapter['forward_commercial_pipeline']['next_required_action']=lock['next_required_action']
    adapter['change_authorities'].insert(0,{**evid_ref,'priority':0,'purpose':'Current human V2 FAIL and semantic-anchor V3 preparation. Preserves photography and V2 coherence gains while changing only the typography layer.'})
    dump(ADAPTER,adapter)
    patch_validator()
    print(json.dumps({'status':lock['status'],'revision':40,'checkpoint_sequence':62,'next_required_action':lock['next_required_action'],'evidence':evid_ref,'lock_sha256':lock_sha},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
