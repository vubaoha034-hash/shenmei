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
VALIDATOR=ROOT/'visual_memory/vpd_p6_composition_state.py'
PLAN=ROOT/'evidence/vpd/p1_typography_research_sandbox_v1/TYPOGRAPHY_METHOD_SANDBOX_PLAN_V1.json'
EVID=ROOT/'evidence/vpd/p1_typography_research_sandbox_v1/TYPOGRAPHY_METHOD_SANDBOX_TEST01_FAIL_20260916.json'

def load(p): return json.loads(p.read_text(encoding='utf-8'))
def dump(p,o): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p): return {'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)}
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def blob(path): return subprocess.check_output(['git','rev-parse',f'HEAD:{path}'],cwd=ROOT,text=True).strip()
def eh(o): return hashlib.sha256(json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def patch_validator():
    s=VALIDATOR.read_text(encoding='utf-8')
    if 'P1_EXECUTE_TYPOGRAPHY_METHOD_SANDBOX_TEST_02' not in s:
        marker='    "P1_EXECUTE_TYPOGRAPHY_METHOD_SANDBOX_TEST_01",\n'
        if marker not in s: raise SystemExit('test01 action marker missing')
        s=s.replace(marker,marker+'    "P1_EXECUTE_TYPOGRAPHY_METHOD_SANDBOX_TEST_02",\n',1)
    tail='    require(not set(cp["completed"]) & set(cp["incomplete"]), "COMPLETED_AND_INCOMPLETE")\n'
    if 'TYPOGRAPHY_SANDBOX_TEST02_NOT_READY' not in s:
        block='''    if action == "P1_EXECUTE_TYPOGRAPHY_METHOD_SANDBOX_TEST_02":\n        tr = lock["typography_repair"]\n        require(lock["status"] == "VPD_P1_TYPOGRAPHY_METHOD_SANDBOX_TEST01_FAIL", "TYPOGRAPHY_SANDBOX_TEST02_NOT_READY")\n        require(tr.get("status") == "TYPOGRAPHY_METHOD_SANDBOX_TEST01_FAIL", "TYPOGRAPHY_SANDBOX_TEST01_FAIL_STATE")\n        require(tr.get("sandbox_test01_verdict") == "FAIL_NOT_READABLE_AS_CHA", "TYPOGRAPHY_SANDBOX_TEST01_VERDICT")\n        require(tr.get("sandbox_rule_promotion_allowed") is False, "TYPOGRAPHY_SANDBOX_PREMATURE_RULE_PROMOTION")\n        require(tr.get("sandbox_next_test") == "TYP-M02", "TYPOGRAPHY_SANDBOX_TEST02_DRIFT")\n        check_ref(root, tr["typography_method_sandbox_plan"])\n        check_ref(root, tr["sandbox_test01_evidence"])\n        require(tr.get("T2_allowed") is False and tr.get("P6_reintegration_allowed") is False, "TYPOGRAPHY_SANDBOX_PREMATURE_ADVANCE")\n\n'''
        if tail not in s: raise SystemExit('validator tail missing')
        s=s.replace(tail,block+tail,1)
    VALIDATOR.write_text(s,encoding='utf-8')

def main():
    lock=load(LOCK); cp=load(CP); adapter=load(ADAPTER); plan=load(PLAN)
    if lock.get('revision')!=53 or lock.get('next_required_action')!='P1_EXECUTE_TYPOGRAPHY_METHOD_SANDBOX_TEST_01':
        raise SystemExit('unexpected source state')
    if plan.get('first_test')!='TYP-M01': raise SystemExit('plan drift')
    patch_validator(); recorded=now(); old_blob=blob('continuity/vpd/CURRENT_TASK_LOCK.json')
    evidence={
      'schema_version':'vpd-typography-method-sandbox-test/v1',
      'recorded_at':recorded,
      'test_id':'TYP-M01',
      'method':'CENTERLINE_VARIABLE_WIDTH_STROKE_RECONSTRUCTION',
      'status':'FAIL_ARCHIVED_NEGATIVE_EVIDENCE_NOT_RULE',
      'scope':{'target':'茶 only','visible_outputs':1,'hidden_variants':0,'pre_review_polish_retries':0,'leaves':False,'texture':False,'gradient':False,'shadow':False},
      'figma':{'file_key':'uyDxOoN1iNDPpEHTKSUWg1','page_id':'70:2','sandbox_frame_id':'120:2','stroke_node_ids':['120:3','120:4','120:5','120:6','120:7','120:8','120:9','120:10','120:11'],'formal_nodes_overwritten':False,'variable_width_api_readback':'PASS_CUSTOM_PROFILES_ON_ALL_9_STROKES'},
      'technical_observation':{
        'glyph_readability':'FAIL',
        'observed_shape':'first read collapses into a broad umbrella/mushroom-like mass rather than an immediately recognizable 茶 character',
        'edge_noise_problem':'AVOIDED_BUT_NOT_SUFFICIENT',
        'method_value_observed':'centerline/variable-width removes dense bitten-edge tracing, but this first construction does not preserve Chinese component structure or mother lettering character'
      },
      'verdict':'FAIL_NOT_READABLE_AS_CHA',
      'human_verdict':None,
      'why_no_human_pass_needed':'The candidate fails a prior correctness requirement: immediate character recognition. Aesthetics cannot promote an unreadable glyph.',
      'rule_admission':{'allowed':False,'action':'ARCHIVE_NEGATIVE_EVIDENCE_DO_NOT_ADD_TO_RULES'},
      'next_test':'TYP-M02_FAITHFUL_LETTERING_VECTORIZATION'
    }
    dump(EVID,evidence); er=ref(EVID); pr=ref(PLAN)

    lock['revision']=54
    lock['preserved_prior_revision']={'revision':53,'git_blob_sha':old_blob,'note':'Revision 53 opened exactly one TYP-M01 sandbox output with no rule promotion.'}
    lock['current_stage']='Typography sandbox Test 01 (TYP-M01 centerline + variable-width stroke reconstruction) executed exactly once on 茶. The method avoided dense trace-edge noise but failed prior glyph correctness: the result does not immediately read as 茶 and collapses into an umbrella/mushroom-like mass. TYP-M01 is archived as negative evidence and is forbidden from rule promotion. Open TYP-M02 faithful lettering vectorization next; formal nodes, Doufang, photography, T2 and P6 remain frozen.'
    lock['status']='VPD_P1_TYPOGRAPHY_METHOD_SANDBOX_TEST01_FAIL'
    lock['next_required_action']='P1_EXECUTE_TYPOGRAPHY_METHOD_SANDBOX_TEST_02'
    lock['p6_allowed']=False
    lock['completed_this_revision']=[
      'executed exactly one visible TYP-M01 centerline plus variable-width stroke sandbox output on 茶',
      'confirmed all nine Figma stroke nodes used custom variable-width profiles',
      'recorded correctness failure because the output is not immediately readable as 茶',
      'archived TYP-M01 as negative evidence and explicitly prohibited rule promotion',
      'opened only TYP-M02 faithful lettering vectorization as the next sandbox test',
      'kept formal Chazuo nodes, Doufang, photography, T2 and P6 frozen'
    ]
    lock['blockers']=[
      'TYP-M01 failed and is not eligible for rule promotion.',
      'No typography research method is an approved VPD rule until a controlled actual-pixel test passes human review and the user explicitly approves promotion.',
      'T2 remains blocked until a title route achieves human visual acceptance.',
      'P6 reintegration and photo regeneration remain blocked; prior image gains are preserved.',
      'Candidate promotion, Commercial, Golden and Scale remain blocked.'
    ]
    tr=lock['typography_repair']
    tr={**tr,'status':'TYPOGRAPHY_METHOD_SANDBOX_TEST01_FAIL','phase':'TYPOGRAPHY_METHOD_SANDBOX','sandbox_test01_evidence':er,'sandbox_test01_verdict':'FAIL_NOT_READABLE_AS_CHA','sandbox_rule_promotion_allowed':False,'sandbox_next_test':'TYP-M02','T2_allowed':False,'P6_reintegration_allowed':False,'next_required_action':'P1_EXECUTE_TYPOGRAPHY_METHOD_SANDBOX_TEST_02'}
    lock['typography_repair']=tr; lock['updated_at']=recorded
    dump(LOCK,lock); lock_sha=sha(LOCK)

    prev=None
    for line in LEDGER.read_text(encoding='utf-8').splitlines():
        o=json.loads(line); prev={'event_id':o['event_id'],'event_hash':o['event_hash']}
    event={'schema_version':'upcp-state-ledger-event/v1','stream_id':'commercial_design_pipeline','event_id':'EVT-VPD-P1-TYPOGRAPHY-METHOD-SANDBOX-TEST01-FAIL-20260916-001','event_type':'TYPOGRAPHY_METHOD_SANDBOX_TEST01_FAIL','task_id':lock['parent_active_task_id'],'project_id':lock['project_id'],'recorded_at':recorded,'material':True,'previous_event_id':prev['event_id'] if prev else None,'previous_event_hash':prev['event_hash'] if prev else None,'lock_sha256':lock_sha,'authorization':{'source':'current controlling ChatGPT conversation','authority':'user sandbox rule plus current test execution','instruction':'Test researched methods first; failed methods must not enter rules.'},'before':{'state':'VPD_P1_TYPOGRAPHY_METHOD_SANDBOX_READY','next_action':'P1_EXECUTE_TYPOGRAPHY_METHOD_SANDBOX_TEST_01'},'after':{'state':lock['status'],'next_action':lock['next_required_action']},'evidence':[er['path'],pr['path']],'reason':'The single TYP-M01 output fails immediate Chinese glyph recognition. The method is archived as negative evidence and cannot enter production rules.','remote_authority':{'repository':lock['repository'],'branch':lock['branch']}}
    event['event_hash']=eh(event)
    with LEDGER.open('a',encoding='utf-8',newline='\n') as f:f.write(json.dumps(event,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n')

    cp['sequence']=max(int(cp.get('sequence',0))+1,76); cp['recorded_at']=recorded; cp['current_focus']=lock['current_stage']
    if 'p1_typography_method_sandbox_test01_fail' not in cp['completed']: cp['completed'].append('p1_typography_method_sandbox_test01_fail')
    cp['incomplete']=['p1_typography_method_sandbox_test_02','p1_typography_support_hierarchy_bench','p6_reintegration_after_typography_repair','candidate_promotion','second_style_family_validation','golden','scale']
    cp['blocked']=list(lock['blockers']); cp['next_required_action']=lock['next_required_action']; cp['status']=lock['status']; cp['task_lock']={'path':'continuity/vpd/CURRENT_TASK_LOCK.json','sha256':lock_sha}; cp['ledger_tails']={'commercial_design_pipeline':{'event_id':event['event_id'],'event_hash':event['event_hash']}}
    cp['typography_repair']={**cp.get('typography_repair',{}),'status':tr['status'],'phase':tr['phase'],'sandbox_test01_evidence':er,'sandbox_test01_verdict':'FAIL_NOT_READABLE_AS_CHA','sandbox_rule_promotion_allowed':False,'sandbox_next_test':'TYP-M02','T2_allowed':False,'P6_reintegration_allowed':False,'next_required_action':lock['next_required_action']}
    dump(CP,cp)

    adapter['task_lock']['revision']=54; adapter['task_lock']['sha256']=lock_sha; adapter['vpd_system_goal_authority']['checkpoint']=lock['status']; adapter['vpd_system_goal_authority']['next_required_action']=lock['next_required_action']; adapter['vpd_system_goal_authority']['render_allowed']=False; adapter['forward_commercial_pipeline']['status']='PAUSED_FOR_P1_TYPOGRAPHY_METHOD_SANDBOX_TEST_02'; adapter['forward_commercial_pipeline']['next_required_action']=lock['next_required_action']; adapter['change_authorities'].insert(0,{**er,'priority':0,'purpose':'Sandbox Test 01 negative evidence: TYP-M01 failed glyph recognition and is not eligible for rule promotion.'}); dump(ADAPTER,adapter)
    print(json.dumps({'status':lock['status'],'revision':54,'checkpoint_sequence':cp['sequence'],'next_required_action':lock['next_required_action'],'evidence':er,'lock_sha256':lock_sha},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
