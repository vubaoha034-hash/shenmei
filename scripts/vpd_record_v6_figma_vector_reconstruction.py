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
EVID=ROOT/'evidence/vpd/p1_typography_repair_v6/V6_FIGMA_VECTOR_RECONSTRUCTION_20260915.json'
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
    if '"P1_WAIT_HUMAN_V6_FIGMA_VECTOR_REVIEW",' not in text:
        text=text.replace('    "P1_VECTOR_RECONSTRUCT_V6_IN_FIGMA",\n}', '    "P1_VECTOR_RECONSTRUCT_V6_IN_FIGMA",\n    "P1_WAIT_HUMAN_V6_FIGMA_VECTOR_REVIEW",\n}')
    if 'elif action == "P1_WAIT_HUMAN_V6_FIGMA_VECTOR_REVIEW":' not in text:
        needle='    require(not set(cp["completed"]) & set(cp["incomplete"]), "COMPLETED_AND_INCOMPLETE")'
        branch='''    elif action == "P1_WAIT_HUMAN_V6_FIGMA_VECTOR_REVIEW":\n        tr = lock["typography_repair"]\n        require(tr["status"] == "V6_FIGMA_VECTOR_RECONSTRUCTED_WAITING_HUMAN_REVIEW", "V6_VECTOR_REVIEW_STATE")\n        require(tr["phase"] == "V6_FIGMA_VECTOR_REVIEW", "V6_VECTOR_REVIEW_PHASE")\n        require(tr["figma_vector_reconstruction_allowed"] is False, "V6_VECTOR_RECONSTRUCTION_STILL_OPEN")\n        require(tr["T2_allowed"] is False and tr["P6_reintegration_allowed"] is False, "V6_VECTOR_PREMATURE_ADVANCE")\n        check_ref(root, tr["v6_execution"])\n        check_ref(root, tr["v6_vector_reconstruction"])\n        rec = read(root, tr["v6_vector_reconstruction"]["path"])\n        require(rec["status"] == "EDITABLE_VECTOR_RECONSTRUCTION_COMPLETE_WAITING_HUMAN_REVIEW", "V6_VECTOR_RECORD_STATUS")\n        require(rec["figma"]["page_id"] == "70:2", "V6_VECTOR_PAGE_DRIFT")\n        require(rec["figma"]["editable_nodes"] == {"豆坊":"70:5","茶作字形":"70:7","茶作叶形":"70:9"}, "V6_VECTOR_NODE_DRIFT")\n        require(rec["editability_readback_verified"] is True, "V6_VECTOR_EDITABILITY_UNVERIFIED")\n\n'''
        if needle not in text: raise SystemExit('validator insertion point missing')
        text=text.replace(needle,branch+needle)
    VALIDATOR.write_text(text,encoding='utf-8')

def main():
    lock=load(LOCK); cp=load(CP); adapter=load(ADAPTER)
    if lock.get('revision')!=47 or lock.get('next_required_action')!='P1_VECTOR_RECONSTRUCT_V6_IN_FIGMA':
        raise SystemExit('unexpected source state')
    tr=lock['typography_repair']; recorded=now(); old_blob=blob('continuity/vpd/CURRENT_TASK_LOCK.json')
    evidence={
      'schema_version':'vpd-v6-figma-vector-reconstruction/v1',
      'recorded_at':recorded,
      'status':'EDITABLE_VECTOR_RECONSTRUCTION_COMPLETE_WAITING_HUMAN_REVIEW',
      'source_v6_execution':tr['v6_execution'],
      'figma':{
        'file_key':'uyDxOoN1iNDPpEHTKSUWg1',
        'page_id':'70:2',
        'page_name':'P1 V6 Vector Reconstruction',
        'review_frames':{'豆坊':'70:3','茶作':'70:4'},
        'editable_nodes':{'豆坊':'70:5','茶作字形':'70:7','茶作叶形':'70:9'},
        'leaf_vector_separate_editable_layer':True,
        'raster_wordmark_used':False,
        'glyph_reideation_performed':False
      },
      'editability_readback_verified':True,
      'metadata_readback':{
        '豆坊':'70:5 FRAME -> 70:6 VECTOR',
        '茶作字形':'70:7 FRAME -> 70:8 VECTOR',
        '茶作叶形':'70:9 FRAME -> 70:10 VECTOR'
      },
      'drive_review':{
        'presentation_id':'1-YtSzv7O5KiXQPncc-GBktPrhb2IJ2t6cZMUd6viLhY',
        'title':'T1_V6_Figma矢量重建复判_20260915',
        'folder_id':'1TaQJeK5BGskE7gVXUL5yEfEDVNSSvCG9',
        'url':'https://docs.google.com/presentation/d/1-YtSzv7O5KiXQPncc-GBktPrhb2IJ2t6cZMUd6viLhY/edit'
      },
      'preservation':{'P6_modified':False,'photography_modified':False,'V6_concept_geometry_used_as_source':True},
      'review_boundary':'This is faithful editable reconstruction only. Human review decides whether the design direction remains worth continuing; T2 and P6 remain blocked.',
      'next_required_action':'P1_WAIT_HUMAN_V6_FIGMA_VECTOR_REVIEW'
    }
    dump(EVID,evidence); er=ref(EVID)
    lock['revision']=48
    lock['preserved_prior_revision']={'revision':47,'git_blob_sha':old_blob,'note':'Revision 47 authorized faithful editable Figma vector reconstruction of V6 only.'}
    lock['current_stage']='V6 selected wordmarks have been faithfully reconstructed in Figma as editable vectors, with tea leaf graphics on a separate editable vector layer. No glyph re-ideation, photography change or P6 mutation occurred. Await human review of the Figma vector result before any support typography or poster reintegration.'
    lock['status']='VPD_P1_V6_FIGMA_VECTOR_RECONSTRUCTED_WAITING_HUMAN_REVIEW'
    lock['next_required_action']='P1_WAIT_HUMAN_V6_FIGMA_VECTOR_REVIEW'
    lock['completed_this_revision']=[
      'reconstructed V6 豆坊 as an editable Figma vector tree',
      'reconstructed V6 茶作 glyph and leaf graphics as separate editable Figma vector layers',
      'verified vector node structure by Figma metadata readback',
      'created a stable two-slide Drive review file from Figma renders',
      'preserved P6 photography and all prior experiment evidence unchanged'
    ]
    lock['blockers']=[
      'V6 Figma vector result is waiting for human title review and is not approved.',
      'T2 remains blocked until this human review passes.',
      'P6 reintegration and photo regeneration remain blocked; prior image gains are preserved.',
      'Candidate promotion, Commercial, Golden and Scale remain blocked.'
    ]
    tr={**tr,
        'status':'V6_FIGMA_VECTOR_RECONSTRUCTED_WAITING_HUMAN_REVIEW',
        'phase':'V6_FIGMA_VECTOR_REVIEW',
        'v6_vector_reconstruction':er,
        'figma_vector_reconstruction_allowed':False,
        'T2_allowed':False,
        'P6_reintegration_allowed':False,
        'next_required_action':'P1_WAIT_HUMAN_V6_FIGMA_VECTOR_REVIEW'}
    lock['typography_repair']=tr; lock['updated_at']=recorded
    dump(LOCK,lock); lock_sha=sha(LOCK)

    prev=None
    for line in LEDGER.read_text(encoding='utf-8').splitlines():
        o=json.loads(line); prev={'event_id':o['event_id'],'event_hash':o['event_hash']}
    event={'schema_version':'upcp-state-ledger-event/v1','stream_id':'commercial_design_pipeline','event_id':'EVT-VPD-P1-V6-FIGMA-VECTOR-RECONSTRUCTED-20260915-001','event_type':'V6_FIGMA_VECTOR_RECONSTRUCTED_WAITING_HUMAN_REVIEW','task_id':lock['parent_active_task_id'],'project_id':lock['project_id'],'recorded_at':recorded,'material':True,'previous_event_id':prev['event_id'] if prev else None,'previous_event_hash':prev['event_hash'] if prev else None,'lock_sha256':lock_sha,'before':{'state':'V6_DIRECTIONAL_POSITIVE_FIGMA_VECTOR_RECONSTRUCTION_READY','next_action':'P1_VECTOR_RECONSTRUCT_V6_IN_FIGMA'},'after':{'state':lock['status'],'next_action':lock['next_required_action']},'evidence':[er['path']],'reason':'Figma now contains editable vector reconstructions of the selected V6 concept without re-ideating the wordmark. Human review must decide whether to continue before T2 or poster reintegration.','remote_authority':{'repository':lock['repository'],'branch':lock['branch']}}
    event['event_hash']=eh(event)
    with LEDGER.open('a',encoding='utf-8',newline='\n') as f: f.write(json.dumps(event,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n')

    cp['sequence']=70; cp['recorded_at']=recorded; cp['current_focus']=lock['current_stage']
    if 'p1_v6_figma_vector_reconstruction' not in cp['completed']: cp['completed'].append('p1_v6_figma_vector_reconstruction')
    cp['incomplete']=['p1_v6_post_vector_human_review','p1_typography_support_hierarchy_bench','p6_reintegration_after_typography_repair','candidate_promotion','second_style_family_validation','golden','scale']
    cp['blocked']=list(lock['blockers']); cp['next_required_action']=lock['next_required_action']; cp['status']=lock['status']; cp['task_lock']={'path':'continuity/vpd/CURRENT_TASK_LOCK.json','sha256':lock_sha}; cp['ledger_tails']={'commercial_design_pipeline':{'event_id':event['event_id'],'event_hash':event['event_hash']}}
    cp['typography_repair']={'status':tr['status'],'phase':tr['phase'],'v6_execution':tr['v6_execution'],'v6_vector_reconstruction':er,'selected_direction':tr['selected_direction'],'T2_allowed':False,'P6_reintegration_allowed':False,'next_required_action':lock['next_required_action']}
    dump(CP,cp)

    adapter['vpd_system_goal_authority']['checkpoint']=lock['status']; adapter['vpd_system_goal_authority']['next_required_action']=lock['next_required_action']; adapter['vpd_system_goal_authority']['render_allowed']=False
    adapter['task_lock']['revision']=48; adapter['task_lock']['sha256']=lock_sha
    adapter['forward_commercial_pipeline']['status']='PAUSED_FOR_P1_V6_FIGMA_VECTOR_HUMAN_REVIEW'; adapter['forward_commercial_pipeline']['next_required_action']=lock['next_required_action']
    adapter['change_authorities'].insert(0,{**er,'priority':0,'purpose':'Current V6 editable Figma vector reconstruction evidence; human title review remains mandatory before T2 or P6.'})
    dump(ADAPTER,adapter)
    patch_validator()
    print(json.dumps({'status':lock['status'],'revision':48,'checkpoint_sequence':70,'next_required_action':lock['next_required_action'],'evidence':er,'lock_sha256':lock_sha},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
