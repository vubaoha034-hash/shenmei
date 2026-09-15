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
EVID=ROOT/'evidence/vpd/p1_typography_repair_v6/V6_FIGMA_CONTOUR_CLEANUP_20260915.json'

def load(p): return json.loads(p.read_text(encoding='utf-8'))
def dump(p,o): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p): return {'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)}
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def blob(path): return subprocess.check_output(['git','rev-parse',f'HEAD:{path}'],cwd=ROOT,text=True).strip()
def eh(o): return hashlib.sha256(json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def main():
    lock=load(LOCK); cp=load(CP); adapter=load(ADAPTER)
    if lock.get('revision')!=49 or lock.get('next_required_action')!='P1_WAIT_HUMAN_V6_FIGMA_VECTOR_REVIEW':
        raise SystemExit('unexpected source state')
    tr=lock['typography_repair']; recorded=now(); old_blob=blob('continuity/vpd/CURRENT_TASK_LOCK.json')
    evidence={
      'schema_version':'vpd-v6-figma-contour-cleanup/v1',
      'recorded_at':recorded,
      'status':'FIGMA_CONTOUR_CLEANUP_EXECUTED_WAITING_HUMAN_REVIEW',
      'human_feedback_before_cleanup':{
        '豆坊':'CONTINUE; endpoint improved but lower edge still reads cut',
        '茶作':'CONTINUE',
        'shared_edge_issue':'high-frequency bitten/jagged contour is visually uncomfortable and does not resemble controlled lettering',
        'feedback_exact':['豆坊端头：解决了一些，但是还是下面有很明显的切割感。','两个标题：都可以继续','很少有文字会这种凹凸不平的边缘。感觉就是很不舒服的感觉。就算是毛笔字，也不会边缘这样像咬了一样的感觉。']
      },
      'non_authoritative_generation_correction':{
        'status':'EXCLUDED_FROM_FORMAL_PROGRESS',
        'note':'Two directly generated clean-edge draft images from the prior assistant turn were not Figma edits, dropped the green tea-leaf design information, and are explicitly not formal V6 evidence or replacements.'
      },
      'diagnosis':{
        'doufang_bottom_hard_cut':{'segment_index':178,'start_vertex':178,'end_vertex':179,'length_px':126,'both_y':498,'at_vector_max_y':True},
        'edge_noise_source':'dense raster-trace-like polygon vertices and short segments; macro silhouette is directionally useful but micro contour is over-jagged',
        'principle':'preserve macro irregularity and semantic structure; remove only high-frequency micro jitter'
      },
      'figma_cleanup':{
        'file_key':'uyDxOoN1iNDPpEHTKSUWg1',
        'page_id':'70:2',
        'review_frames':{'豆坊':'70:3','茶作':'70:4'},
        'formal_vectors':{'豆坊':'75:2','茶作白字':'70:8','茶作绿色叶片':'70:10'},
        'hidden_backups_created':['DOUFANG_PRE_EDGE_CLEANUP_BACKUP','CHAZUO_GLYPH_PRE_EDGE_CLEANUP_BACKUP','CHAZUO_LEAF_PRE_EDGE_CLEANUP_BACKUP'],
        'doufang_bottom_fix':'replaced the 126px flat bottom cut with a controlled upward Bezier arc on segment 178',
        'micro_cleanup_method':'local perpendicular projection smoothing on short low-deviation contour vertices; topology and loop structure preserved',
        'cleanup_operations':{'豆坊':272,'茶作白字':297,'茶作绿色叶片':13},
        'green_leaf_layer_preserved':True,
        'green_leaf_position_count_structure_preserved':True,
        'glyph_reideation_performed':False,
        'photography_modified':False,
        'P6_modified':False,
        'image_generation_used_for_formal_cleanup':False
      },
      'drive_review':{
        'presentation_id':'1-YtSzv7O5KiXQPncc-GBktPrhb2IJ2t6cZMUd6viLhY',
        'title':'T1_V6_Figma矢量重建复判_20260915',
        'both_slides_replaced_with_current_figma_renders':True,
        'url':'https://docs.google.com/presentation/d/1-YtSzv7O5KiXQPncc-GBktPrhb2IJ2t6cZMUd6viLhY/edit'
      },
      'gate':{
        'title_passed':False,
        'T2_allowed':False,
        'P6_reintegration_allowed':False,
        'next_required_action':'P1_WAIT_HUMAN_V6_FIGMA_VECTOR_REVIEW'
      }
    }
    dump(EVID,evidence); er=ref(EVID)

    lock['revision']=50
    lock['preserved_prior_revision']={'revision':49,'git_blob_sha':old_blob,'note':'Revision 49 recorded the localized Doufang endpoint fix and kept human review open.'}
    lock['current_stage']='Both V6 wordmarks remain viable. Formal work stayed in Figma: Doufang bottom hard-cut geometry and high-frequency bitten edges were cleaned; Chazuo white glyph edges were cleaned while the separate green tea-leaf vector layer was preserved. Prior direct-generation cleanup drafts are excluded from formal progress. Await human re-review before T2 or poster reintegration.'
    lock['completed_this_revision']=[
      'excluded the prior direct-generation cleanup drafts from formal V6 progress',
      'confirmed and repaired the remaining 126px Doufang bottom hard-cut segment in Figma',
      'cleaned high-frequency micro contour jitter on Doufang and Chazuo editable vectors',
      'preserved the Chazuo green tea-leaf vector layer and semantic color accents',
      'created hidden pre-cleanup Figma backups for rollback safety',
      'updated both stable Drive review slides from the current Figma renders'
    ]
    lock['blockers']=[
      'V6 contour-cleaned Doufang and Chazuo remain waiting for human title re-review and are not approved.',
      'T2 remains blocked until this human review passes.',
      'P6 reintegration and photo regeneration remain blocked; prior image gains are preserved.',
      'Candidate promotion, Commercial, Golden and Scale remain blocked.'
    ]
    tr={**tr,
        'v6_figma_contour_cleanup':er,
        'v6_human_review_before_contour_cleanup':evidence['human_feedback_before_cleanup'],
        'T2_allowed':False,
        'P6_reintegration_allowed':False,
        'next_required_action':'P1_WAIT_HUMAN_V6_FIGMA_VECTOR_REVIEW'}
    lock['typography_repair']=tr; lock['updated_at']=recorded
    dump(LOCK,lock); lock_sha=sha(LOCK)

    prev=None
    for line in LEDGER.read_text(encoding='utf-8').splitlines():
        o=json.loads(line); prev={'event_id':o['event_id'],'event_hash':o['event_hash']}
    event={'schema_version':'upcp-state-ledger-event/v1','stream_id':'commercial_design_pipeline','event_id':'EVT-VPD-P1-V6-FIGMA-CONTOUR-CLEANUP-20260915-001','event_type':'V6_FIGMA_CONTOUR_CLEANUP_WAITING_HUMAN_REVIEW','task_id':lock['parent_active_task_id'],'project_id':lock['project_id'],'recorded_at':recorded,'material':True,'previous_event_id':prev['event_id'] if prev else None,'previous_event_hash':prev['event_hash'] if prev else None,'lock_sha256':lock_sha,'authorization':{'source':'current controlling ChatGPT conversation','authority':'user feedback','feedback':['豆坊端头仍有下边切割感','两个标题都可以继续','边缘像被咬一样不舒服','指出上一轮误用生图并丢失茶叶颜色设计']},'before':{'state':lock['status'],'next_action':'P1_WAIT_HUMAN_V6_FIGMA_VECTOR_REVIEW'},'after':{'state':lock['status'],'next_action':lock['next_required_action']},'evidence':[er['path']],'reason':'Preserve the accepted V6 direction and repair only formal Figma vector contour defects. Green tea-leaf design information is preserved; direct-generation cleanup drafts are non-authoritative. Human re-review remains mandatory.','remote_authority':{'repository':lock['repository'],'branch':lock['branch']}}
    event['event_hash']=eh(event)
    with LEDGER.open('a',encoding='utf-8',newline='\n') as f: f.write(json.dumps(event,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n')

    cp['sequence']=72; cp['recorded_at']=recorded; cp['current_focus']=lock['current_stage']
    if 'p1_v6_figma_contour_cleanup' not in cp['completed']: cp['completed'].append('p1_v6_figma_contour_cleanup')
    cp['incomplete']=['p1_v6_post_vector_human_review','p1_typography_support_hierarchy_bench','p6_reintegration_after_typography_repair','candidate_promotion','second_style_family_validation','golden','scale']
    cp['blocked']=list(lock['blockers']); cp['next_required_action']=lock['next_required_action']; cp['status']=lock['status']; cp['task_lock']={'path':'continuity/vpd/CURRENT_TASK_LOCK.json','sha256':lock_sha}; cp['ledger_tails']={'commercial_design_pipeline':{'event_id':event['event_id'],'event_hash':event['event_hash']}}
    cp['typography_repair']={**cp.get('typography_repair',{}),'v6_figma_contour_cleanup':er,'T2_allowed':False,'P6_reintegration_allowed':False,'next_required_action':lock['next_required_action']}
    dump(CP,cp)

    adapter['task_lock']['revision']=50; adapter['task_lock']['sha256']=lock_sha
    adapter['vpd_system_goal_authority']['checkpoint']=lock['status']; adapter['vpd_system_goal_authority']['next_required_action']=lock['next_required_action']; adapter['vpd_system_goal_authority']['render_allowed']=False
    adapter['forward_commercial_pipeline']['status']='PAUSED_FOR_P1_V6_CONTOUR_CLEANUP_HUMAN_REVIEW'; adapter['forward_commercial_pipeline']['next_required_action']=lock['next_required_action']
    adapter['change_authorities'].insert(0,{**er,'priority':0,'purpose':'Current V6 Figma contour-cleanup evidence; green tea-leaf design is preserved and human title re-review remains mandatory.'})
    dump(ADAPTER,adapter)

    print(json.dumps({'status':lock['status'],'revision':50,'checkpoint_sequence':72,'next_required_action':lock['next_required_action'],'evidence':er,'lock_sha256':lock_sha},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
