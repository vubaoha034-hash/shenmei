"""Bind already-viewed historical design references, close a rejected candidate.
No generation, no image-byte changes, no new aesthetic scores or validator family.
"""
from pathlib import Path
import json, hashlib, sys, copy
SOURCE='6c9a4f67206156443ec6320f6bbd1cc5bf9a543e'
TASK='VPD-BASELINE-RESTORE-AND-REGRESSION-01'
STATUS='VPD_CHAZUO_SCOPED_BASELINE_RESTORED_REJECTED_CANDIDATE_CLOSED'
NEXT='DEFINE_ONE_CHAZUO_DESIGN_SUCCESSOR_WITH_SCOPED_BASELINE'
L='continuity/vpd/CURRENT_TASK_LOCK.json'
C='continuity/vpd/LATEST_CHECKPOINT.json'
A='PROJECT_CONTROL_ADAPTER.json'
G='continuity/vpd/VISUAL_MASTER_FREEZE_GUARD_V1.json'
R='evidence/vpd/p1_typography_research_sandbox_v1/CHAZUO_NEW_IMAGE_COMPOSITION01_EXECUTION_20260930.json'
H='evidence/vpd/p1_typography_research_sandbox_v1/CHAZUO_CONCEPT02_EDITABLE_RECONSTRUCTION_HUMAN_REVIEW_PHOTO_FAIL_20260921.json'
J='continuity/vpd/state_ledger/commercial_design_pipeline.jsonl'
V='visual_memory/vpd_p6_composition_state.py'
T='evidence/vpd/p1_typography_research_sandbox_v1/CHAZUO_NEW_IMAGE_COMPOSITION01_TASK_20260930.json'

def encoded(d): return (json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode()
def sha(b): return hashlib.sha256(b).hexdigest()
def restore(root):
    load=lambda p:json.loads((root/p).read_text())
    write=lambda p,d:(root/p).write_bytes(encoded(d))
    lock,cp,ad,g,r,h=[load(p) for p in [L,C,A,G,R,H]]
    assert lock['revision']==178 and cp['sequence']==200, 'SOURCE_REVISION_CHANGED'
    assert r['status']=='HUMAN_REJECT_GENERIC_RETURN_TO_ORIGINAL'
    assert r['candidate']['sha256']=='0aeeb282ab767001abb99435dcebf2412680e996ef839becea9c763f89bcb715'
    assert h['human_review']['overall_design']=='PASS' and h['human_review']['wordmark']=='PASS'
    assert h['human_review']['photo_base']=='FAIL_NEEDS_REPAIR'
    original_guard=copy.deepcopy(g)
    comparison={
      'task_id':TASK,'source_head':SOURCE,
      'review_type':'COORDINATOR_KNOWN_LABEL_PIXEL_COMPARISON_NOT_BLIND',
      'actual_pixels_viewed':True,
      'baseline':{'file_key':'uyDxOoN1iNDPpEHTKSUWg1','reference_frame':'197:2','reference_raster':'197:3','design_frame':'201:2','wordmark_node':'203:2',
        'reference_dimensions':[1024,1536],'design_dimensions':[1024,1536],
        'source_sha256_historical':'b4b7fdd825baaa83c751409d84702275c60da810d9f1ee5db44aabe79ea9299f',
        'source_bytes_revalidated_this_task':False,
        'readback':'Figma native full-node screenshots of 197:2 and 201:2 actually viewed; not regenerated. Original source-byte download unavailable in coordinator runtime.',
        'human_scope_ref':{'path':H,'sha256':sha((root/H).read_bytes())},
        'accepted_dimensions':['composition_hierarchy','wordmark'],
        'not_accepted':['photographic_realism','final_whole_poster_quality','cross_family_transfer'],
        'role':'historical_internal_design_reference_not_universal_best_not_original_external_reference',
        'generation_anchor_required':False,'reuse_old_photo_required':False,'old_route_reopened':False},
      'candidate':{'task_id':r['task_id'],'gen_id':r['candidate']['gen_id'],'sha256':r['candidate']['sha256'],
        'dimensions':r['candidate']['dimensions'],'actual_file_hash_checked':True,'human_rejected':True,'baseline_promotion_allowed':False},
      'findings':[
        {'dimension':'wordmark','baseline_observation':'大尺度茶作字标成为主视觉，叶片笔画与茶语义相接；201:2是已认可的可编辑字标版本。','candidate_observation':'左上较小书写字标与产品静物分离，退回品牌标签式摆放。','judgment':'已认可的字标存在感与产品语义关系未保住。'},
        {'dimension':'composition_hierarchy','baseline_observation':'左侧大字、右侧深色竖向结构、下方近景茶器与远山纵深形成图文对重和阅读路径。','candidate_observation':'白墙承载左侧标题和文案，茶器静物集中右下，图与字主要依靠分区摆放。','judgment':'换了场景，但图文关系更通用；不构成设计能力进步。'},
        {'dimension':'scope_and_photography','baseline_observation':'旧回执只接受整体设计与字标，摄影明确AI味重。','candidate_observation':'新图可更平顺干净，但真人明确评价非常普通。','judgment':'不以干净或摄影顺眼抵消设计回退，也不把旧摄影改判通过。'}],
      'verdict':'REJECTED_CANDIDATE_MUST_NOT_REPLACE_SCOPED_BASELINE',
      'new_human_acceptance_inferred':False,'independent_evaluator_calibrated':False,
      'stable_quality_guaranteed':False,'new_generation_count':0,
      'next_action':'使用已恢复的设计参照制定一个新图文设计候选；基线用于对照质量，不强制复制旧图骨架。不得继续修已否决的新茶具图或227:2，不自动扩成新一轮审计。'}
    r['coordinator_baseline_comparison']=comparison
    r['human_gate']['next_legal_action']='CLOSED_NO_RESUBMISSION_BASELINE_COMPARISON_COMPLETE'
    write(R,r)
    task=load(T)
    task['status']='COMPLETED_HUMAN_REJECTED_CLOSED'
    task['next_legal_action']='CLOSED_NO_RESUBMISSION'
    task['human_verdict_ref']={'path':R,'sha256':sha((root/R).read_bytes())}
    write(T,task)
    g['current_comparison']={'task_id':TASK,'status':'SCOPED_BASELINE_RESTORED_NEGATIVE_CLOSED',
      'evidence':{'path':R,'sha256':sha((root/R).read_bytes())},
      'baseline_frame_ids':['197:2','201:2'],'accepted_dimensions':['composition_hierarchy','wordmark'],
      'photographic_realism_accepted':False,'whole_poster_accepted':False,
      'rejected_candidate_gen_id':r['candidate']['gen_id'],'rejected_candidate_sha256':r['candidate']['sha256'],
      'rejected_candidate_is_baseline':False,'current_generation_reference_mandatory':False,
      'historical_mandatory_next_loop_is_not_current_dispatch':True,
      'evaluation_reference_is_not_a_fixed_template':True}
    # Never rewrite the historical protected image, its accepted dimensions or invariant rules.
    for key in ['core_invariants','current_chazuo_freeze_map','mandatory_next_loop']:
      assert g[key]==original_guard[key]
    write(G,g)
    ref={'path':G,'sha256':sha((root/G).read_bytes())}
    lock['revision']+=1
    lock['status']=STATUS;lock['next_required_action']=NEXT
    lock['current_stage']='已恢复197:2与201:2真实像素对照，旧认可仅限设计/字标；最新普通茶作图继续否决关闭。下一步为一个有界的新图文设计候选，不是再审旧图。'
    lock['updated_at']='2026-09-30'
    lock['baseline_preservation']=ref
    lock['visual_master_freeze_guard']['sha256']=ref['sha256']
    lock['blockers']=[]
    lock['completed_this_revision']=['实际读取197:2和201:2完整图像','按原人审限定设计与摄影范围','最新失败候选不得替换历史设计参照','闭合本次人审状态镜像与哈希']
    n=lock['chazuo_new_image_composition01'];n['status']=r['status'];n['human_review_state']=r['human_gate']['status'];n['next_legal_action']='CLOSED_NO_RESUBMISSION';n['baseline_promotion_allowed']=False
    write(L,lock)
    raw=(root/J).read_bytes();prior=json.loads(raw.splitlines()[-1])
    event={'schema_version':'upcp-state-ledger-event/v1','stream_id':'commercial_design_pipeline',
      'event_id':'EVT-VPD-SCOPED-BASELINE-RESTORED-20260930-001','event_type':'SCOPED_BASELINE_RESTORED_AND_REJECTED_CANDIDATE_CLOSED','project_id':lock['project_id'],'task_id':TASK,
      'recorded_at':'2026-09-30','previous_event_id':prior['event_id'],'previous_event_hash':prior['event_hash'],
      'lock_sha256':sha((root/L).read_bytes()),'material':True,
      'before':{'lock_revision':178,'checkpoint_sequence':200},
      'after':{'lock_revision':lock['revision'],'checkpoint_sequence':201,'status':STATUS,'next':NEXT,'new_images':0,'baseline_frames':['197:2','201:2'],'photography_pass':False,'candidate_promoted':False},
      'evidence':[G,R,H],
      'reason':'恢复真实质量参照及其局部认可范围；不再让新失败候选与未结算的人审镜像覆盖已成立部分。'}
    event['event_hash']=sha(json.dumps(event,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
    (root/J).write_bytes(raw+(b'' if raw.endswith(b'\n') else b'\n')+json.dumps(event,ensure_ascii=False,separators=(',',':')).encode()+b'\n')
    cp['sequence']=201;cp['recorded_at']='2026-09-30';cp['status']=STATUS;cp['next_required_action']=NEXT;cp['current_focus']=lock['current_stage'];cp['current_stage']=lock['current_stage'];cp['updated_at']='2026-09-30'
    cp['active_task_ids']=[];cp['blocked']=[];cp['incomplete']=['下一项实际视觉候选尚未制作；本轮无新作品质量通过']
    cp['completed'] += ['scoped_design_baseline_actual_pixels_restored','latest_generic_candidate_human_rejection_settled']
    cp['task_lock']={'path':L,'sha256':sha((root/L).read_bytes())}
    cp['latest_evidence']={'path':R,'sha256':sha((root/R).read_bytes())}
    cp['baseline_preservation']=ref
    cp['chazuo_new_image_composition01']=copy.deepcopy(n)
    cp['ledger_tails']={'commercial_design_pipeline':{'event_id':event['event_id'],'event_hash':event['event_hash']}}
    write(C,cp)
    ad['task_lock']['revision']=lock['revision'];ad['task_lock']['sha256']=cp['task_lock']['sha256']
    ad['vpd_system_goal_authority']['checkpoint']=STATUS;ad['vpd_system_goal_authority']['next_required_action']=NEXT
    ad['ledger_tails']=cp['ledger_tails'];ad['baseline_preservation']=ref
    write(A,ad)
    text=(root/V).read_text()
    marker='def validate_p6_composition_state(root):'
    handler=(Path(__file__).with_name('handler.txt')).read_text()
    assert text.count(marker)==1 and '_validate_scoped_baseline_preservation' not in text
    text=text.replace(marker,handler+'\n\n'+marker)
    marker2='    if lock.get("next_required_action") == CHAZUO_REWORK_REVIEW_ACTION:'
    assert text.count(marker2)==1
    text=text.replace(marker2,'    if lock.get("status") == "VPD_CHAZUO_SCOPED_BASELINE_RESTORED_REJECTED_CANDIDATE_CLOSED":\n        _validate_scoped_baseline_preservation(root, lock, cp, adapter)\n        return lock, cp\n'+marker2)
    (root/V).write_text(text)
    return [L,C,A,G,R,T,J,V]

if __name__=='__main__':
    root=Path(sys.argv[1]);changed=restore(root)
    print(json.dumps({'source_head':SOURCE,'changed_files':changed,'generation_count':0,'new_human_quality_pass':False},ensure_ascii=False))
