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
EVID=ROOT/'evidence/vpd/p1_typography_repair_v6/V6_PER_CONTOUR_BEZIER_REFINEMENT_20260915.json'

def load(p): return json.loads(p.read_text(encoding='utf-8'))
def dump(p,o): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p): return {'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)}
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def blob(path): return subprocess.check_output(['git','rev-parse',f'HEAD:{path}'],cwd=ROOT,text=True).strip()
def eh(o): return hashlib.sha256(json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def main():
    lock=load(LOCK); cp=load(CP); adapter=load(ADAPTER)
    if lock.get('revision')!=50 or lock.get('next_required_action')!='P1_WAIT_HUMAN_V6_FIGMA_VECTOR_REVIEW':
        raise SystemExit('unexpected source state')
    tr=lock['typography_repair']; recorded=now(); old_blob=blob('continuity/vpd/CURRENT_TASK_LOCK.json')
    evidence={
      'schema_version':'vpd-v6-per-contour-bezier-refinement/v1',
      'recorded_at':recorded,
      'status':'PER_CONTOUR_BEZIER_REFINEMENT_EXECUTED_WAITING_HUMAN_REVIEW',
      'human_review_before_refinement':{
        'doufang_cropping':'PASS_NO_LONGER_READS_AS_CUT',
        'shared_edge_quality':'FAIL_UNACCEPTABLE',
        'chazuo_green_leaf':'PASS_PRESERVED',
        'feedback_exact':['1 没有被切掉','2 不可接受','3 茶叶保留了。']
      },
      'diagnosis':{
        'prior_cleanup_limit':'moving existing trace vertices reduced some jitter but left dense trace topology, so bitten/faceted edge quality remained',
        'formal_node_density_before_refinement':{'豆坊':321,'茶作白字':341,'茶作绿色叶片':118},
        'decision':'do not globally simplify or regenerate; rebuild edge continuity per closed contour with corner-preserving Bezier tangents'
      },
      'rejected_non_destructive_tests':[
        {'method':'aggressive contour reduction','result':'REJECTED','reason':'produced coarse faceted/cut lettering','formal_nodes_overwritten':False},
        {'method':'automatic reduced-point curve fit','result':'REJECTED','reason':'damaged internal 豆 structure','formal_nodes_overwritten':False}
      ],
      'figma_refinement':{
        'file_key':'uyDxOoN1iNDPpEHTKSUWg1',
        'page_id':'70:2',
        'review_frames':{'豆坊':'70:3','茶作':'70:4'},
        'formal_vectors':{'豆坊':'75:2','茶作白字':'70:8','茶作绿色叶片':'70:10'},
        'method':'per closed contour: preserve true corners, apply one low-strength local average only to non-corner micro-jitter points, then assign Catmull-Rom-derived cubic Bezier tangents with handle clamping',
        'doufang_verified_terminal_segments_preserved':[0,178],
        'chazuo_green_leaf_modified':False,
        'chazuo_green_leaf_preserved':True,
        'glyph_reideation_performed':False,
        'photography_modified':False,
        'P6_modified':False,
        'image_generation_used_for_formal_refinement':False,
        'test_frames_removed_after_promotion':True
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

    lock['revision']=51
    lock['preserved_prior_revision']={'revision':50,'git_blob_sha':old_blob,'note':'Revision 50 recorded Figma contour cleanup but human edge-quality review still failed.'}
    lock['current_stage']='Human confirms Doufang cropping is solved and the Chazuo green leaf layer is preserved, but rejects both wordmarks edge quality. Formal Figma glyph contours were therefore refined per closed contour with corner-preserving cubic Bezier continuity; no image generation, glyph re-ideation, leaf deletion, photography change or P6 mutation occurred. Await human re-review before T2 or poster reintegration.'
    lock['completed_this_revision']=[
      'recorded human verdict: Doufang cropping pass, shared edge quality fail, Chazuo green leaf preservation pass',
      'rejected and deleted two non-destructive automatic curve-fit tests before any formal overwrite',
      'refined formal Doufang and Chazuo glyph edge continuity per closed contour using cubic Bezier tangents',
      'preserved validated Doufang terminal/bottom geometry and the complete Chazuo green leaf layer',
      'updated both stable Drive review slides from the new formal Figma renders',
      'kept T2, P6 reintegration, photography and candidate promotion blocked pending human re-review'
    ]
    lock['blockers']=[
      'V6 per-contour-Bezier-refined Doufang and Chazuo remain waiting for human title re-review and are not approved.',
      'T2 remains blocked until this human review passes.',
      'P6 reintegration and photo regeneration remain blocked; prior image gains are preserved.',
      'Candidate promotion, Commercial, Golden and Scale remain blocked.'
    ]
    tr={**tr,
        'v6_per_contour_bezier_refinement':er,
        'v6_human_review_before_bezier_refinement':evidence['human_review_before_refinement'],
        'T2_allowed':False,
        'P6_reintegration_allowed':False,
        'next_required_action':'P1_WAIT_HUMAN_V6_FIGMA_VECTOR_REVIEW'}
    lock['typography_repair']=tr; lock['updated_at']=recorded
    dump(LOCK,lock); lock_sha=sha(LOCK)

    prev=None
    for line in LEDGER.read_text(encoding='utf-8').splitlines():
        o=json.loads(line); prev={'event_id':o['event_id'],'event_hash':o['event_hash']}
    event={'schema_version':'upcp-state-ledger-event/v1','stream_id':'commercial_design_pipeline','event_id':'EVT-VPD-P1-V6-PER-CONTOUR-BEZIER-REFINEMENT-20260915-001','event_type':'V6_PER_CONTOUR_BEZIER_REFINEMENT_WAITING_HUMAN_REVIEW','task_id':lock['parent_active_task_id'],'project_id':lock['project_id'],'recorded_at':recorded,'material':True,'previous_event_id':prev['event_id'] if prev else None,'previous_event_hash':prev['event_hash'] if prev else None,'lock_sha256':lock_sha,'authorization':{'source':'current controlling ChatGPT conversation','authority':'user feedback','feedback':['豆坊没有被切掉','两组边缘不可接受','茶叶保留了','继续下一步']},'before':{'state':lock['status'],'next_action':'P1_WAIT_HUMAN_V6_FIGMA_VECTOR_REVIEW'},'after':{'state':lock['status'],'next_action':lock['next_required_action']},'evidence':[er['path']],'reason':'The prior Figma contour cleanup did not solve edge taste quality. Formal glyphs were refined by per-contour Bezier continuity while preserving accepted structure, Doufang terminals and the Chazuo green leaf layer. Human re-review remains mandatory.','remote_authority':{'repository':lock['repository'],'branch':lock['branch']}}
    event['event_hash']=eh(event)
    with LEDGER.open('a',encoding='utf-8',newline='\n') as f: f.write(json.dumps(event,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n')

    cp['sequence']=73; cp['recorded_at']=recorded; cp['current_focus']=lock['current_stage']
    if 'p1_v6_per_contour_bezier_refinement' not in cp['completed']: cp['completed'].append('p1_v6_per_contour_bezier_refinement')
    cp['incomplete']=['p1_v6_post_vector_human_review','p1_typography_support_hierarchy_bench','p6_reintegration_after_typography_repair','candidate_promotion','second_style_family_validation','golden','scale']
    cp['blocked']=list(lock['blockers']); cp['next_required_action']=lock['next_required_action']; cp['status']=lock['status']; cp['task_lock']={'path':'continuity/vpd/CURRENT_TASK_LOCK.json','sha256':lock_sha}; cp['ledger_tails']={'commercial_design_pipeline':{'event_id':event['event_id'],'event_hash':event['event_hash']}}
    cp['typography_repair']={**cp.get('typography_repair',{}),'v6_per_contour_bezier_refinement':er,'T2_allowed':False,'P6_reintegration_allowed':False,'next_required_action':lock['next_required_action']}
    dump(CP,cp)

    adapter['task_lock']['revision']=51; adapter['task_lock']['sha256']=lock_sha
    adapter['vpd_system_goal_authority']['checkpoint']=lock['status']; adapter['vpd_system_goal_authority']['next_required_action']=lock['next_required_action']; adapter['vpd_system_goal_authority']['render_allowed']=False
    adapter['forward_commercial_pipeline']['status']='PAUSED_FOR_P1_V6_PER_CONTOUR_BEZIER_HUMAN_REVIEW'; adapter['forward_commercial_pipeline']['next_required_action']=lock['next_required_action']
    adapter['change_authorities'].insert(0,{**er,'priority':0,'purpose':'Current V6 per-contour Bezier edge-refinement evidence; human title re-review remains mandatory before T2 or P6.'})
    dump(ADAPTER,adapter)

    print(json.dumps({'status':lock['status'],'revision':51,'checkpoint_sequence':73,'next_required_action':lock['next_required_action'],'evidence':er,'lock_sha256':lock_sha},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
