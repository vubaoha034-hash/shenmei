"""Mutation tests use temporary copies; synthetic readback is never runtime evidence."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import pytest
from visual_memory.vpd_task_lock import (
    LOCK_PATH, CHECKPOINT_PATH, NEXT_ACTION, TaskLockError,
    validate_state, validate_request, status_card, digest,
)
ROOT = Path(__file__).resolve().parents[2]

def load(root, p):
    return json.loads((root / p).read_text())

def save(root, p, data):
    (root / p).write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')

@pytest.fixture
def isolated(tmp_path):
    shutil.copytree(ROOT, tmp_path / 'repo', ignore=shutil.ignore_patterns('.git', '__pycache__', '.pytest_cache'))
    return tmp_path / 'repo'

def reseal(root, lock):
    # Rebind mirrors so semantic tests cannot pass only because a checksum changed.
    save(root, LOCK_PATH, lock)
    adapter = load(root, 'PROJECT_CONTROL_ADAPTER.json')
    adapter['task_lock']['sha256'] = digest(root / LOCK_PATH)
    save(root, 'PROJECT_CONTROL_ADAPTER.json', adapter)
    cp = load(root, CHECKPOINT_PATH)
    cp['task_lock']['sha256'] = digest(root / LOCK_PATH)
    cp['requirements'] = lock['requirements']
    cp['execution'] = lock['execution']
    for r in cp['source_state_refs']:
        if r['path'] in [LOCK_PATH, 'PROJECT_CONTROL_ADAPTER.json']:
            r['sha256'] = digest(root / r['path'])
    save(root, CHECKPOINT_PATH, cp)

def request(root):
    return {'action':NEXT_ACTION, 'lock_sha256':digest(root / LOCK_PATH)}

def test_correct_state_and_real_entrypoint_pass(isolated):
    lock, cp = validate_state(isolated)
    assert cp['sequence'] > 22
    assert lock['requirements']['task_lock_state_readback_review']['status'] == 'DONE'
    assert lock['next_required_action'] == 'RECONCILE_FORMAL_RENDER_ATTEMPT2_EVIDENCE'
    assert lock['parent_active_task_id'] == 'VPD-SYSTEM-LEVEL-HOLDOUT-TRANSFER-VALIDATION-V1'
    assert validate_request(isolated, request(isolated)) == lock
    result = subprocess.run([sys.executable, str(isolated/'scripts/verify_visual_memory.py'), '--vpd-state', '--status-card'], capture_output=True, text=True)
    assert result.returncode == 0
    assert json.loads(result.stdout) == status_card(lock, cp)

@pytest.mark.parametrize('case,reason', [
 ('source', 'SOURCE_ROLE_OR_ID_CHANGED'),
 ('objective_state','OBJECTIVE_DRIFT'),
 ('capsule_state','CAPSULE_IDENTITY_DRIFT'),
 ('attempt_state','RENDERER_ATTEMPT_IDENTITY_DRIFT'),
 ('anchor', 'FEEDBACK_AS_RUNTIME_ANCHOR'),
 ('duplicate', 'COMPLETED_AND_INCOMPLETE'),
 ('zero_reference', 'HISTORICAL_ZERO_REFERENCE_LEAK'),
 ('goal', 'SCOPED_CHANGE_AUTHORITY_REQUIRED'),
 ('cached_remote', 'LOCAL_OR_CACHED_REF_NOT_REMOTE_PROOF'),
 ('unread_remote', 'REMOTE_FILE_NOT_READ_BACK'),
 ('replay', 'ACTION_NOT_AUTHORIZED_OR_REPLAY'),
 ('handoff_reset', 'HANDOFF_REPLAY_NOT_AUTHORIZED'),
 ('wrong_h2', 'OUTPUT_IDENTITY_CROSSOVER'),
 ('filename_only', 'UNRECONCILED_OUTPUT_CANNOT_BE_VERIFIED_BY_FILENAME'),
 ('proxy', 'FORMAL_EXPORT_NOT_AUTHORIZED_OR_PROXY'),
 ('accepted', 'MISSING_HUMAN_ACCEPTANCE'),
 ('promoted', 'MISSING_HUMAN_ACCEPTANCE'),
 ('wrong_entry', 'ENTRYPOINT_LOCK_OR_VALIDATOR_MISSING'),
 ('stale_state', 'STALE_CURRENT_CHECKPOINT'),
 ('binding_boolean', 'SELF_ASSERTED_BINDING_OR_CALL_PASS'),
 ('binding_claim', 'SELF_ASSERTED_BINDING_PASS'),
])
def test_drift_is_rejected(isolated, case, reason):
    root=isolated;lock=load(root,LOCK_PATH);cp=load(root,CHECKPOINT_PATH);r=request(root)
    if case=='source':lock['source_library']['entries'][0]['drive_file_id']='zaobianwei-output'
    elif case=='objective_state':lock['objective']['text']='重新优化灶边味海报'
    elif case=='capsule_state':lock['capsule']['id']='new-capsule'
    elif case=='attempt_state':lock['experiment']['renderer_attempt']='ATTEMPT3'
    elif case=='anchor':lock['experiment']['runtime_anchor']['drive_file_id']='zaobianwei-output'
    elif case=='duplicate':cp['incomplete'].append('runtime_authorization');save(root,CHECKPOINT_PATH,cp)
    elif case=='zero_reference':lock['experiment']['reference_count']=0
    elif case=='goal':r['changes']={'objective':'single poster'};r['user_text']='继续'
    elif case=='cached_remote':r.update(remote_verified=True,remote_readback={'kind':'CACHED_ORIGIN','commit':'a'*40})
    elif case=='unread_remote':r.update(remote_verified=True,remote_readback={'kind':'GITHUB_CONNECTOR_INDEPENDENT_READBACK','repository':lock['repository'],'branch':lock['branch'],'commit':'a'*40,'live_ref_commit':'a'*40,'observed_at':'test-only','file_sha256':{}})
    elif case=='replay':r['action']='RENDER_H1_H2_H3_H4'
    elif case=='handoff_reset':lock['experiment']['handoff']['consumption']='UNUSED'
    elif case in ('wrong_h2','filename_only'):
        payload=load(root,lock['experiment']['payloads']['H2']['path'])
        r['output']={'challenge_id':'H2','experiment_id':payload['experiment_id'] if case=='filename_only' else 'SHY-SYS-HOLDOUT-V1-H1','payload_sha256':lock['experiment']['payloads']['H2']['sha256'],'filename':'H2.png','verified':case=='filename_only'}
    elif case=='proxy':r['export']={'formal':True,'kind':'FIGMA_PROXY_PREVIEW'}
    elif case=='accepted':r['accepted']=True
    elif case=='promoted':r['promoted']=True
    elif case=='wrong_entry':
        p=root/'START_HERE.md';p.write_text(p.read_text().replace(LOCK_PATH,'continuity/vpd/WRONG_LOCK.json'))
    elif case=='stale_state':cp['sequence']=22;save(root,CHECKPOINT_PATH,cp)
    elif case=='binding_boolean':lock['execution']['bound_anchor']=True
    elif case=='binding_claim':r['binding_pass']=True
    if case in ['source','anchor','zero_reference','handoff_reset','binding_boolean','objective_state','capsule_state','attempt_state']:
        reseal(root,lock);r['lock_sha256']=digest(root/LOCK_PATH)
    with pytest.raises(TaskLockError,match=reason):validate_request(root,r)

@pytest.mark.parametrize('name',['H1_CONTROLLER_PAYLOAD.json','H4_CONTROLLER_PAYLOAD.json','RUNTIME_VISUAL_ANCHOR_BINDING_MANIFEST_V1.json','SYSTEM_LEVEL_HOLDOUT_PAYLOAD_FREEZE_RECEIPT_V1.json'])
def test_any_frozen_byte_change_fails(isolated,name):
    p=isolated/'evidence/vpd/shanyeji/system_level_holdout_validation_v1'/name
    p.write_bytes(p.read_bytes()+b' ')
    with pytest.raises(TaskLockError,match='FROZEN_BYTES_CHANGED'):validate_state(isolated)

def test_entrypoint_exits_nonzero_on_bad_state(isolated):
    cp=load(isolated,CHECKPOINT_PATH);cp['incomplete'].append('payload_freeze');save(isolated,CHECKPOINT_PATH,cp)
    result=subprocess.run([sys.executable,str(isolated/'scripts/verify_visual_memory.py'),'--vpd-state'],capture_output=True,text=True)
    assert result.returncode!=0
    assert json.loads(result.stdout)['status']=='VPD_STATE_BLOCKED'

def test_readback_receipt_shape_positive_synthetic_only(isolated):
    lock,_=validate_state(isolated);r=request(isolated)
    r.update(remote_verified=True,remote_readback={'kind':'GITHUB_CONNECTOR_INDEPENDENT_READBACK','repository':lock['repository'],'branch':lock['branch'],'commit':'a'*40,'live_ref_commit':'a'*40,'observed_at':'SYNTHETIC_TEST_NOT_RUNTIME_EVIDENCE','file_sha256':{p:digest(isolated/p) for p in [LOCK_PATH,CHECKPOINT_PATH,'PROJECT_CONTROL_ADAPTER.json']}})
    assert validate_request(isolated,r)==lock

def test_reconciliation_requires_completed_review(isolated):
    lock=load(isolated,LOCK_PATH)
    del lock['requirements']['task_lock_state_readback_review']
    reseal(isolated,lock)
    with pytest.raises(TaskLockError,match='REVIEW_REQUIRED_BEFORE_RECONCILIATION'):
        validate_state(isolated)

def test_new_chat_entry_requires_workflow(isolated):
    p=isolated/'START_HERE.md'
    p.write_text(p.read_text().replace('VPD_PROJECT_ROADMAP.md','WRONG_ROADMAP.md'))
    with pytest.raises(TaskLockError,match='ENTRYPOINT_WORKFLOW_MISSING'):
        validate_state(isolated)
