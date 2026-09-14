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
PLAN=ROOT/'evidence/vpd/p1_typography_repair_v5/WORDMARK_V4_HUMAN_NONE_AND_GENERATIVE_V5_PLAN_20260914.json'
EVID=ROOT/'evidence/vpd/p1_typography_repair_v5/GENERATIVE_CUSTOM_WORDMARK_V5_EXECUTION_20260914.json'
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
    if '"P1_WAIT_HUMAN_GENERATIVE_CUSTOM_WORDMARK_V5_DIRECTION_VERDICT",' not in text:
        needle='    "P1_EXECUTE_GENERATIVE_CUSTOM_WORDMARK_EXPLORATION_V5",\n}'
        if needle not in text: raise SystemExit('ACTIONS insertion point missing')
        text=text.replace(needle,'    "P1_EXECUTE_GENERATIVE_CUSTOM_WORDMARK_EXPLORATION_V5",\n    "P1_WAIT_HUMAN_GENERATIVE_CUSTOM_WORDMARK_V5_DIRECTION_VERDICT",\n}')
    if 'elif action == "P1_WAIT_HUMAN_GENERATIVE_CUSTOM_WORDMARK_V5_DIRECTION_VERDICT":' not in text:
        needle='    require(not set(cp["completed"]) & set(cp["incomplete"]), "COMPLETED_AND_INCOMPLETE")'
        if needle not in text: raise SystemExit('validator branch insertion point missing')
        branch='''    elif action == "P1_WAIT_HUMAN_GENERATIVE_CUSTOM_WORDMARK_V5_DIRECTION_VERDICT":
        tr = lock["typography_repair"]
        require(tr["status"] == "GENERATIVE_CUSTOM_WORDMARK_V5_EXECUTED_WAITING_HUMAN_DIRECTION_VERDICT", "WORDMARK_V5_WAIT_STATE")
        require(tr["phase"] == "GENERATIVE_CUSTOM_WORDMARK_V5", "WORDMARK_V5_PHASE")
        require(tr["wordmark_v5_generation_allowed"] is False, "WORDMARK_V5_SHOULD_BE_FROZEN")
        require(tr["wordmark_v5_visible_concept_budget"] == {"豆坊":6,"茶作":6}, "WORDMARK_V5_BUDGET")
        require(tr["wordmark_v5_selected_direction"] == {"豆坊":None,"茶作":None}, "WORDMARK_V5_PREMATURE_SELECTION")
        require(tr["support_typography_bench_allowed"] is False and tr["poster_reintegration_allowed"] is False, "WORDMARK_V5_PREMATURE_ADVANCE")
        check_ref(root, tr["wordmark_v4_human_none_and_v5_plan"])
        check_ref(root, tr["wordmark_v5_execution"])

'''
        text=text.replace(needle,branch+needle)
    VALIDATOR.write_text(text,encoding='utf-8')

def main():
    lock=load(LOCK); cp=load(CP); adapter=load(ADAPTER)
    if lock.get('revision')!=44: raise SystemExit('unexpected source revision')
    if lock.get('next_required_action')!='P1_EXECUTE_GENERATIVE_CUSTOM_WORDMARK_EXPLORATION_V5': raise SystemExit('unexpected source action')
    tr=lock['typography_repair']
    if tr.get('status')!='WORDMARK_V4_HUMAN_NONE_GENERATIVE_V5_READY': raise SystemExit('unexpected typography state')
    plan=load(PLAN)
    recorded=now(); old_blob=blob('continuity/vpd/CURRENT_TASK_LOCK.json')
    evidence={
      'schema_version':'vpd-generative-custom-wordmark-v5-execution/v1',
      'recorded_at':recorded,
      'status':'EXECUTED_FROZEN_WAITING_HUMAN_DIRECTION_VERDICT',
      'authority_plan':ref(PLAN),
      'generation':{
        'tool':'OpenAI image generation',
        'gen_id':'3d604246-83d0-4eff-81ac-dbd0ec362d91',
        'single_visible_board':True,
        'visible_concepts':{'豆坊':6,'茶作':6},
        'hidden_variants':0,
        'board_dimensions':[2160,728],
        'board_sha256':'c230fdbc00c870678fb41a4fea7a26e13fd9bcd4639d185ac97fbc8099a4d3ce',
        'board_bytes':1393641,
        'execution_note':'The model returned one visible board containing six 豆坊 and six 茶作 wordmark explorations in the same call. No Figma glyph construction was used.'
      },
      'drive_review':{
        'presentation_id':'1qj21-h8GT_K-J-rsnidsl7VcSw04qkWXq9OuSBzk9MQ',
        'title':'T1_V5_生成式定制字标探索_20260914',
        'folder_id':'1TaQJeK5BGskE7gVXUL5yEfEDVNSSvCG9',
        'url':'https://docs.google.com/presentation/d/1qj21-h8GT_K-J-rsnidsl7VcSw04qkWXq9OuSBzk9MQ/edit',
        'thumbnail_readback_verified':True
      },
      'preservation':{
        'photography_modified':False,
        'photo_bases_regenerated':False,
        'P6_modified':False,
        'V3_modified':False,
        'V4_modified':False,
        'Figma_used_for_glyph_ideation':False
      },
      'human_review_gate':{
        'questions':[
          'which 豆坊 concept, if any, has convincing authored design sense while remaining immediately readable',
          'which 茶作 concept, if any, has convincing authored design sense while remaining immediately readable',
          'is any concept materially closer to the approved Shanyeji maturity level than V4',
          'if none, return NONE without polishing or reintegration'
        ],
        'human_verdict':None
      },
      'T2_allowed':False,
      'P6_reintegration_allowed':False,
      'next_required_action':'P1_WAIT_HUMAN_GENERATIVE_CUSTOM_WORDMARK_V5_DIRECTION_VERDICT'
    }
    dump(EVID,evidence); evid_ref=ref(EVID)
    lock['revision']=45
    lock['preserved_prior_revision']={'revision':44,'git_blob_sha':old_blob,'note':'Revision 44 recorded V4 human NONE and authorized generative custom-wordmark V5.'}
    lock['current_stage']='Generative custom-wordmark V5 has executed one fully visible exploration board containing six 豆坊 and six 茶作 concepts. The board is stored in Drive and read back. No Figma glyph ideation, photography regeneration or P6 mutation occurred. V5 is frozen pending human direction selection.'
    lock['status']='VPD_P1_GENERATIVE_CUSTOM_WORDMARK_V5_EXECUTED_WAITING_HUMAN_DIRECTION_VERDICT'
    lock['next_required_action']='P1_WAIT_HUMAN_GENERATIVE_CUSTOM_WORDMARK_V5_DIRECTION_VERDICT'
    lock['completed_this_revision']=[
      'executed one visible V5 generative custom-wordmark board with 6 豆坊 and 6 茶作 concepts',
      'used zero hidden variants and no Figma glyph construction',
      'stored the generated board in Drive and independently read back its slide thumbnail',
      'preserved all photography, P3/P4/P6, V3 and V4 evidence unchanged',
      'froze V5 outputs pending human direction selection'
    ]
    lock['blockers']=[
      'V5 concepts are frozen pending human selection; do not polish or vectorize before selection.',
      'T2 support typography remains blocked until a V5 direction is selected and passes title review.',
      'P6 reintegration and photo regeneration remain blocked; prior image gains are preserved.',
      'Candidate promotion, Commercial, Golden and Scale remain blocked.'
    ]
    tr={**tr,
        'status':'GENERATIVE_CUSTOM_WORDMARK_V5_EXECUTED_WAITING_HUMAN_DIRECTION_VERDICT',
        'phase':'GENERATIVE_CUSTOM_WORDMARK_V5',
        'wordmark_v5_generation_allowed':False,
        'wordmark_v5_execution':evid_ref,
        'wordmark_v5_drive_review':evidence['drive_review'],
        'wordmark_v5_selected_direction':{'豆坊':None,'茶作':None},
        'support_typography_bench_allowed':False,
        'poster_reintegration_allowed':False,
        'next_required_action':'P1_WAIT_HUMAN_GENERATIVE_CUSTOM_WORDMARK_V5_DIRECTION_VERDICT'}
    lock['typography_repair']=tr
    lock['wordmark_v5_execution_evidence']=evid_ref
    lock['updated_at']=recorded
    dump(LOCK,lock); lock_sha=sha(LOCK)

    prev=None
    for line in LEDGER.read_text(encoding='utf-8').splitlines():
        o=json.loads(line); prev={'event_id':o['event_id'],'event_hash':o['event_hash']}
    event={'schema_version':'upcp-state-ledger-event/v1','stream_id':'commercial_design_pipeline','event_id':'EVT-VPD-P1-GENERATIVE-CUSTOM-WORDMARK-V5-EXECUTED-20260914-001','event_type':'GENERATIVE_CUSTOM_WORDMARK_V5_EXECUTED','task_id':lock['parent_active_task_id'],'project_id':lock['project_id'],'recorded_at':recorded,'material':True,'previous_event_id':prev['event_id'] if prev else None,'previous_event_hash':prev['event_hash'] if prev else None,'lock_sha256':lock_sha,'authorization':{'source':'current controlling ChatGPT conversation','authority':'current task lock revision 44'},'before':{'state':'WORDMARK_V4_HUMAN_NONE_GENERATIVE_V5_READY','next_action':'P1_EXECUTE_GENERATIVE_CUSTOM_WORDMARK_EXPLORATION_V5'},'after':{'state':lock['status'],'next_action':lock['next_required_action']},'evidence':[ref(PLAN)['path'],evid_ref['path']],'reason':'Execute the bounded generative wordmark exploration outside Figma, preserve all image-direction gains, and wait for human selection before any vectorization or reintegration.','remote_authority':{'repository':lock['repository'],'branch':lock['branch']}}
    event['event_hash']=eh(event)
    with LEDGER.open('a',encoding='utf-8',newline='\n') as f: f.write(json.dumps(event,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n')

    cp['sequence']=67; cp['recorded_at']=recorded; cp['current_focus']=lock['current_stage']
    if 'p1_generative_custom_wordmark_v5_execution' not in cp['completed']: cp['completed'].append('p1_generative_custom_wordmark_v5_execution')
    cp['incomplete']=['p1_generative_custom_wordmark_v5_direction_selection','p1_typography_support_hierarchy_bench','p6_reintegration_after_typography_repair','candidate_promotion','second_style_family_validation','golden','scale']
    cp['blocked']=list(lock['blockers']); cp['next_required_action']=lock['next_required_action']; cp['status']=lock['status']; cp['task_lock']={'path':'continuity/vpd/CURRENT_TASK_LOCK.json','sha256':lock_sha}; cp['ledger_tails']={'commercial_design_pipeline':{'event_id':event['event_id'],'event_hash':event['event_hash']}}
    cp['typography_repair']={'status':tr['status'],'phase':tr['phase'],'wordmark_v5_execution':evid_ref,'drive_review':evidence['drive_review'],'T2_allowed':False,'P6_reintegration_allowed':False,'next_required_action':lock['next_required_action']}
    dump(CP,cp)

    adapter['vpd_system_goal_authority']['checkpoint']=lock['status']; adapter['vpd_system_goal_authority']['next_required_action']=lock['next_required_action']; adapter['vpd_system_goal_authority']['render_allowed']=False
    adapter['task_lock']['revision']=45; adapter['task_lock']['sha256']=lock_sha
    adapter['forward_commercial_pipeline']['status']='PAUSED_FOR_P1_GENERATIVE_CUSTOM_WORDMARK_V5_HUMAN_REVIEW'; adapter['forward_commercial_pipeline']['next_required_action']=lock['next_required_action']
    adapter['change_authorities'].insert(0,{**evid_ref,'priority':0,'purpose':'Current V5 generative custom-wordmark execution evidence; typography only, no photography or P6 mutation.'})
    dump(ADAPTER,adapter)
    patch_validator()
    print(json.dumps({'status':lock['status'],'revision':45,'checkpoint_sequence':67,'next_required_action':lock['next_required_action'],'evidence':evid_ref,'lock_sha256':lock_sha},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
