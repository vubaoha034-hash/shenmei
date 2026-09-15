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
EVID=ROOT/'evidence/vpd/p1_typography_repair_v6/NONCALLIGRAPHIC_SEMANTIC_WORDMARK_V6_EXECUTION_20260915.json'
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
    if '"P1_VECTOR_RECONSTRUCT_V6_IN_FIGMA",' not in text:
        text=text.replace('    "P1_EXECUTE_NONCALLIGRAPHIC_SEMANTIC_WORDMARK_V6",\n}', '    "P1_EXECUTE_NONCALLIGRAPHIC_SEMANTIC_WORDMARK_V6",\n    "P1_VECTOR_RECONSTRUCT_V6_IN_FIGMA",\n}')
    if 'elif action == "P1_VECTOR_RECONSTRUCT_V6_IN_FIGMA":' not in text:
        needle='    require(not set(cp["completed"]) & set(cp["incomplete"]), "COMPLETED_AND_INCOMPLETE")'
        branch='''    elif action == "P1_VECTOR_RECONSTRUCT_V6_IN_FIGMA":\n        tr = lock["typography_repair"]\n        require(tr["status"] == "V6_DIRECTIONAL_POSITIVE_FIGMA_VECTOR_RECONSTRUCTION_READY", "V6_VECTOR_READY_STATE")\n        require(tr["phase"] == "V6_FIGMA_VECTOR_RECONSTRUCTION", "V6_VECTOR_PHASE")\n        require(tr["figma_vector_reconstruction_allowed"] is True, "V6_VECTOR_NOT_OPEN")\n        require(tr["selected_direction"] == {"豆坊":"B","茶作":"D"}, "V6_SEED_SELECTION_DRIFT")\n        require(tr["T2_allowed"] is False and tr["P6_reintegration_allowed"] is False, "V6_PREMATURE_ADVANCE")\n        check_ref(root, tr["v6_execution"])\n\n'''
        if needle not in text: raise SystemExit('validator insertion point missing')
        text=text.replace(needle,branch+needle)
    VALIDATOR.write_text(text,encoding='utf-8')

def main():
    lock=load(LOCK); cp=load(CP); adapter=load(ADAPTER)
    if lock.get('revision')!=46 or lock.get('next_required_action')!='P1_EXECUTE_NONCALLIGRAPHIC_SEMANTIC_WORDMARK_V6':
        raise SystemExit('unexpected source state')
    tr=lock['typography_repair']
    recorded=now(); old_blob=blob('continuity/vpd/CURRENT_TASK_LOCK.json')
    evidence={
      'schema_version':'vpd-noncalligraphic-semantic-wordmark-v6-execution/v1',
      'recorded_at':recorded,
      'status':'EXECUTED_DIRECTIONAL_POSITIVE_NOT_PASS',
      'selected_v5_seeds':{'豆坊':'B','茶作':'D'},
      'generation':{
        'tool':'OpenAI image generation',
        'gen_id':'c75e53e9-711b-42fd-b238-719c447b24ce',
        'board_dimensions':[1536,1024],
        'board_sha256':'4cda6a754fc87c5146a3c989b57281bb9723fc9b1ec0cbe4dd72758dd174943f',
        'board_bytes':1990594,
        'method':'non-calligraphic semantic glyph reconstruction; generated concept first, Figma reserved for downstream vector reconstruction'
      },
      'human_feedback':{
        'positive_exact':'这个设计好很多了。',
        'quality_boundary_exact':'这个跟山野集还是差很多。',
        'formal_interpretation':'DIRECTIONAL_POSITIVE_NOT_PASS'
      },
      'drive_review':{
        'presentation_id':'16bPswZ8cSebDuPsf5uRxRMNm55fdFfZ0lxc0KHShuwA',
        'title':'T1_V6_非书法语义字标候选_20260915',
        'folder_id':'1TaQJeK5BGskE7gVXUL5yEfEDVNSSvCG9',
        'url':'https://docs.google.com/presentation/d/16bPswZ8cSebDuPsf5uRxRMNm55fdFfZ0lxc0KHShuwA/edit'
      },
      'figma_role':{
        'glyph_ideation':False,
        'vector_reconstruction':True,
        'optical_refinement':True,
        'support_typography':False,
        'poster_composition':False,
        'note':'V6 must be reconstructed from the selected visual concept; Figma must not invent a new wordmark style.'
      },
      'preservation':{'photography_modified':False,'P6_modified':False,'V3_V4_V5_evidence_modified':False},
      'T2_allowed':False,
      'P6_reintegration_allowed':False,
      'next_required_action':'P1_VECTOR_RECONSTRUCT_V6_IN_FIGMA'
    }
    dump(EVID,evidence); er=ref(EVID)
    lock['revision']=47
    lock['preserved_prior_revision']={'revision':46,'git_blob_sha':old_blob,'note':'Revision 46 selected V5 B/D as seeds and authorized non-calligraphic V6.'}
    lock['current_stage']='V6 non-calligraphic semantic wordmark generation is directionally much better but remains explicitly far below Shanyeji and is not passed. Preserve all image gains. Move only the selected V6 wordmarks into Figma for faithful editable vector reconstruction and optical refinement; Figma must not re-ideate the glyph style.'
    lock['status']='VPD_P1_V6_DIRECTIONAL_POSITIVE_FIGMA_VECTOR_RECONSTRUCTION_READY'
    lock['next_required_action']='P1_VECTOR_RECONSTRUCT_V6_IN_FIGMA'
    lock['completed_this_revision']=[
      'executed V6 non-calligraphic semantic wordmark concept generation from selected V5 B/D seeds',
      'recorded human directional-positive but not-pass feedback and the remaining large gap to Shanyeji',
      'stored V6 concept board in Drive',
      'preserved photography/P3/P4/P6 and all prior typography evidence',
      'assigned Figma only the downstream editable vector reconstruction and optical-refinement role'
    ]
    lock['blockers']=[
      'V6 concept is directionally positive but not an approved final wordmark.',
      'T2 remains blocked until post-vector human title review passes.',
      'P6 reintegration and photo regeneration remain blocked; prior image gains are preserved.',
      'Candidate promotion, Commercial, Golden and Scale remain blocked.'
    ]
    tr={**tr,
        'status':'V6_DIRECTIONAL_POSITIVE_FIGMA_VECTOR_RECONSTRUCTION_READY',
        'phase':'V6_FIGMA_VECTOR_RECONSTRUCTION',
        'v6_execution':er,
        'v6_human_feedback':evidence['human_feedback'],
        'figma_vector_reconstruction_allowed':True,
        'figma_reideation_allowed':False,
        'T2_allowed':False,
        'P6_reintegration_allowed':False,
        'next_required_action':'P1_VECTOR_RECONSTRUCT_V6_IN_FIGMA'}
    lock['typography_repair']=tr
    lock['updated_at']=recorded
    dump(LOCK,lock); lock_sha=sha(LOCK)

    prev=None
    for line in LEDGER.read_text(encoding='utf-8').splitlines():
        o=json.loads(line); prev={'event_id':o['event_id'],'event_hash':o['event_hash']}
    event={'schema_version':'upcp-state-ledger-event/v1','stream_id':'commercial_design_pipeline','event_id':'EVT-VPD-P1-V6-DIRECTIONAL-POSITIVE-FIGMA-VECTOR-READY-20260915-001','event_type':'V6_DIRECTIONAL_POSITIVE_FIGMA_VECTOR_RECONSTRUCTION_READY','task_id':lock['parent_active_task_id'],'project_id':lock['project_id'],'recorded_at':recorded,'material':True,'previous_event_id':prev['event_id'] if prev else None,'previous_event_hash':prev['event_hash'] if prev else None,'lock_sha256':lock_sha,'authorization':{'source':'current controlling ChatGPT conversation','authority':'user feedback','feedback':['这个设计好很多了。','这个跟山野集还是差很多。']},'before':{'state':'GENERATIVE_V5_HUMAN_SELECTION_NONCALLIGRAPHIC_V6_READY','next_action':'P1_EXECUTE_NONCALLIGRAPHIC_SEMANTIC_WORDMARK_V6'},'after':{'state':lock['status'],'next_action':lock['next_required_action']},'evidence':[er['path']],'reason':'V6 materially improves design direction but is not accepted as finished. Continue by faithfully reconstructing the selected concept as editable vectors in Figma without restarting glyph ideation.','remote_authority':{'repository':lock['repository'],'branch':lock['branch']}}
    event['event_hash']=eh(event)
    with LEDGER.open('a',encoding='utf-8',newline='\n') as f: f.write(json.dumps(event,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n')

    cp['sequence']=69; cp['recorded_at']=recorded; cp['current_focus']=lock['current_stage']
    if 'p1_noncalligraphic_semantic_wordmark_v6_execution' not in cp['completed']: cp['completed'].append('p1_noncalligraphic_semantic_wordmark_v6_execution')
    cp['incomplete']=['p1_v6_figma_vector_reconstruction','p1_v6_post_vector_human_review','p1_typography_support_hierarchy_bench','p6_reintegration_after_typography_repair','candidate_promotion','second_style_family_validation','golden','scale']
    cp['blocked']=list(lock['blockers']); cp['next_required_action']=lock['next_required_action']; cp['status']=lock['status']; cp['task_lock']={'path':'continuity/vpd/CURRENT_TASK_LOCK.json','sha256':lock_sha}; cp['ledger_tails']={'commercial_design_pipeline':{'event_id':event['event_id'],'event_hash':event['event_hash']}}
    cp['typography_repair']={'status':tr['status'],'phase':tr['phase'],'v6_execution':er,'selected_direction':tr['selected_direction'],'T2_allowed':False,'P6_reintegration_allowed':False,'next_required_action':lock['next_required_action']}
    dump(CP,cp)

    adapter['vpd_system_goal_authority']['checkpoint']=lock['status']; adapter['vpd_system_goal_authority']['next_required_action']=lock['next_required_action']; adapter['vpd_system_goal_authority']['render_allowed']=False
    adapter['task_lock']['revision']=47; adapter['task_lock']['sha256']=lock_sha
    adapter['forward_commercial_pipeline']['status']='PAUSED_FOR_P1_V6_FIGMA_VECTOR_RECONSTRUCTION'; adapter['forward_commercial_pipeline']['next_required_action']=lock['next_required_action']
    adapter['change_authorities'].insert(0,{**er,'priority':0,'purpose':'Current V6 directional-positive execution and Figma downstream vector reconstruction authority; photography and P6 remain frozen.'})
    dump(ADAPTER,adapter)
    patch_validator()
    print(json.dumps({'status':lock['status'],'revision':47,'checkpoint_sequence':69,'next_required_action':lock['next_required_action'],'evidence':er,'lock_sha256':lock_sha},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
