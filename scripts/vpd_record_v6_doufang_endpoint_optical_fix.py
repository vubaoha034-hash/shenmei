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
EVID=ROOT/'evidence/vpd/p1_typography_repair_v6/V6_DOUFANG_ENDPOINT_OPTICAL_FIX_20260915.json'

def load(p): return json.loads(p.read_text(encoding='utf-8'))
def dump(p,o): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p): return {'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)}
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def blob(path): return subprocess.check_output(['git','rev-parse',f'HEAD:{path}'],cwd=ROOT,text=True).strip()
def eh(o): return hashlib.sha256(json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def main():
    lock=load(LOCK); cp=load(CP); adapter=load(ADAPTER)
    if lock.get('revision')!=48 or lock.get('next_required_action')!='P1_WAIT_HUMAN_V6_FIGMA_VECTOR_REVIEW':
        raise SystemExit('unexpected source state')
    tr=lock['typography_repair']; recorded=now(); old_blob=blob('continuity/vpd/CURRENT_TASK_LOCK.json')
    evidence={
      'schema_version':'vpd-v6-doufang-endpoint-optical-fix/v1',
      'recorded_at':recorded,
      'status':'FIX_EXECUTED_WAITING_HUMAN_REVIEW',
      'human_review_before_fix':{
        '豆坊':'CONTINUE_WITH_ENDPOINT_FIX_REQUIRED',
        '茶作':'CONTINUE_UNCHANGED',
        'feedback_exact':'两个都可以继续。但是有个很严重的问题，豆坊 明显的感觉左边和右边被截取去除了的感觉。'
      },
      'diagnosis':{
        'cause':'DOUFANG_VECTOR_BOUNDARY_HARD_CUT',
        'measured_boundary_vertices':{
          'left':[{'x':0,'y':356},{'x':0,'y':498}],
          'right':[{'x':824,'y':304},{'x':824,'y':284}]
        },
        'container_clip_only':False,
        'visual_issue':'left and right terminals read as cropped/removed rather than intentionally finished'
      },
      'figma_fix':{
        'file_key':'uyDxOoN1iNDPpEHTKSUWg1',
        'page_id':'70:2',
        'review_frame_id':'70:3',
        'wrapper_id':'70:5',
        'formal_fixed_vector_id':'75:2',
        'formal_fixed_vector_name':'DOUFANG_V6_EDITABLE_VECTOR_ENDPOINT_FIXED',
        'method':'direct boundary-vertex and Bezier-tangent optical correction; no external patch nodes retained',
        'left_terminal':'rounded/tapered natural start, replacing hard vertical cut',
        'right_terminal':'reduced subtle natural finish, replacing hard vertical cut',
        'tea_modified':False,
        'photography_modified':False,
        'P6_modified':False,
        'glyph_style_reideated':False
      },
      'drive_review':{
        'presentation_id':'1-YtSzv7O5KiXQPncc-GBktPrhb2IJ2t6cZMUd6viLhY',
        'title':'T1_V6_Figma矢量重建复判_20260915',
        'first_slide_replaced_with_endpoint_fixed_doufang':True,
        'tea_slide_unchanged':True,
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

    lock['revision']=49
    lock['preserved_prior_revision']={'revision':48,'git_blob_sha':old_blob,'note':'Revision 48 recorded editable V6 Figma reconstruction waiting for human review.'}
    lock['current_stage']='Human says both V6 Figma wordmarks may continue, but identifies a serious Doufang left/right cropped-terminal defect. Tea remains unchanged. Doufang received only a local endpoint optical correction by directly editing boundary vertices/Bezier tangents; no glyph re-ideation, photography or P6 mutation occurred. Await human re-review before T2 or poster reintegration.'
    lock['completed_this_revision']=[
      'recorded human continue verdict for both V6 Figma wordmarks without promoting them to pass',
      'diagnosed Doufang left/right hard-cut boundary geometry from exact vector vertices',
      'corrected only Doufang terminal geometry using direct editable-vector endpoint/tangent refinement',
      'kept Chazuo, photography and P6 unchanged',
      'updated the stable Drive review first slide with the endpoint-fixed Doufang result'
    ]
    lock['blockers']=[
      'V6 endpoint-fixed Doufang and unchanged Chazuo remain waiting for human title re-review and are not approved.',
      'T2 remains blocked until this human review passes.',
      'P6 reintegration and photo regeneration remain blocked; prior image gains are preserved.',
      'Candidate promotion, Commercial, Golden and Scale remain blocked.'
    ]
    tr={**tr,
        'v6_doufang_endpoint_optical_fix':er,
        'v6_human_review_before_endpoint_fix':evidence['human_review_before_fix'],
        'T2_allowed':False,
        'P6_reintegration_allowed':False,
        'next_required_action':'P1_WAIT_HUMAN_V6_FIGMA_VECTOR_REVIEW'}
    lock['typography_repair']=tr; lock['updated_at']=recorded
    dump(LOCK,lock); lock_sha=sha(LOCK)

    prev=None
    for line in LEDGER.read_text(encoding='utf-8').splitlines():
        o=json.loads(line); prev={'event_id':o['event_id'],'event_hash':o['event_hash']}
    event={'schema_version':'upcp-state-ledger-event/v1','stream_id':'commercial_design_pipeline','event_id':'EVT-VPD-P1-V6-DOUFANG-ENDPOINT-OPTICAL-FIX-20260915-001','event_type':'V6_DOUFANG_ENDPOINT_OPTICAL_FIX_WAITING_HUMAN_REVIEW','task_id':lock['parent_active_task_id'],'project_id':lock['project_id'],'recorded_at':recorded,'material':True,'previous_event_id':prev['event_id'] if prev else None,'previous_event_hash':prev['event_hash'] if prev else None,'lock_sha256':lock_sha,'authorization':{'source':'current controlling ChatGPT conversation','authority':'user feedback','feedback':'两个都可以继续。但是有个很严重的问题，豆坊 明显的感觉左边和右边被截取去除了的感觉。'},'before':{'state':'VPD_P1_V6_FIGMA_VECTOR_RECONSTRUCTED_WAITING_HUMAN_REVIEW','next_action':'P1_WAIT_HUMAN_V6_FIGMA_VECTOR_REVIEW'},'after':{'state':lock['status'],'next_action':lock['next_required_action']},'evidence':[er['path']],'reason':'Both directions remain viable; only the exact Doufang endpoint-cropping defect was locally corrected in editable vector geometry. Human re-review remains mandatory.','remote_authority':{'repository':lock['repository'],'branch':lock['branch']}}
    event['event_hash']=eh(event)
    with LEDGER.open('a',encoding='utf-8',newline='\n') as f: f.write(json.dumps(event,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n')

    cp['sequence']=71; cp['recorded_at']=recorded; cp['current_focus']=lock['current_stage']
    if 'p1_v6_doufang_endpoint_optical_fix' not in cp['completed']: cp['completed'].append('p1_v6_doufang_endpoint_optical_fix')
    cp['incomplete']=['p1_v6_post_vector_human_review','p1_typography_support_hierarchy_bench','p6_reintegration_after_typography_repair','candidate_promotion','second_style_family_validation','golden','scale']
    cp['blocked']=list(lock['blockers']); cp['next_required_action']=lock['next_required_action']; cp['status']=lock['status']; cp['task_lock']={'path':'continuity/vpd/CURRENT_TASK_LOCK.json','sha256':lock_sha}; cp['ledger_tails']={'commercial_design_pipeline':{'event_id':event['event_id'],'event_hash':event['event_hash']}}
    cp['typography_repair']={**cp.get('typography_repair',{}),'v6_doufang_endpoint_optical_fix':er,'T2_allowed':False,'P6_reintegration_allowed':False,'next_required_action':lock['next_required_action']}
    dump(CP,cp)

    adapter['task_lock']['revision']=49; adapter['task_lock']['sha256']=lock_sha
    adapter['vpd_system_goal_authority']['checkpoint']=lock['status']; adapter['vpd_system_goal_authority']['next_required_action']=lock['next_required_action']; adapter['vpd_system_goal_authority']['render_allowed']=False
    adapter['forward_commercial_pipeline']['status']='PAUSED_FOR_P1_V6_ENDPOINT_FIXED_HUMAN_REVIEW'; adapter['forward_commercial_pipeline']['next_required_action']=lock['next_required_action']
    adapter['change_authorities'].insert(0,{**er,'priority':0,'purpose':'Current V6 Doufang endpoint optical-fix evidence; both titles still require human re-review before T2 or P6.'})
    dump(ADAPTER,adapter)

    print(json.dumps({'status':lock['status'],'revision':49,'checkpoint_sequence':71,'next_required_action':lock['next_required_action'],'evidence':er,'lock_sha256':lock_sha},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
