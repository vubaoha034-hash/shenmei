"""P6 scope guard regression tests; synthetic fixtures are not upload evidence."""
import hashlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import tarfile

import pytest
from visual_memory.vpd_task_lock import validate_state, TaskLockError, digest

ROOT = Path(__file__).resolve().parents[2]
LOCK = 'continuity/vpd/CURRENT_TASK_LOCK.json'


@pytest.fixture(scope='module')
def base(tmp_path_factory):
    dest = tmp_path_factory.mktemp('p6-state-base')
    archive = subprocess.check_output(['git','-C',str(ROOT),'-c','core.autocrlf=false','archive','HEAD'])
    with tarfile.open(fileobj=io.BytesIO(archive)) as tf:
        tf.extractall(dest, filter='data')
    for name in [LOCK, 'continuity/vpd/LATEST_CHECKPOINT.json', 'PROJECT_CONTROL_ADAPTER.json',
                 'continuity/vpd/state_ledger/system_validation.jsonl']:
        (dest/name).write_bytes((ROOT/name).read_bytes())
    shutil.copytree(ROOT/'evidence/vpd/p6_authority_repair_v1', dest/'evidence/vpd/p6_authority_repair_v1', dirs_exist_ok=True)
    return dest


@pytest.fixture
def repo(base,tmp_path):
    shutil.copytree(base, tmp_path/'repo')
    return tmp_path/'repo'


def read(repo,p):
    return json.loads((repo/p).read_text(encoding='utf-8'))


def write(repo,p,obj):
    (repo/p).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')


def reseal(repo, lock):
    write(repo,LOCK,lock)
    sha=digest(repo/LOCK)
    adapter=read(repo,'PROJECT_CONTROL_ADAPTER.json');adapter['task_lock']['sha256']=sha
    write(repo,'PROJECT_CONTROL_ADAPTER.json',adapter)
    cp=read(repo,'continuity/vpd/LATEST_CHECKPOINT.json');cp['task_lock']['sha256']=sha
    write(repo,'continuity/vpd/LATEST_CHECKPOINT.json',cp)


def test_p6_state_passes_without_promoting_history(repo):
    lock,cp=validate_state(repo)
    assert lock['authority_repair']['historical_ledger_status'].startswith('PRESERVED_WITH_PREEXISTING')
    assert not lock['render_allowed'] and not lock['capsule']['promoted']


@pytest.mark.parametrize('case,reason',[
    ('relock','PHOTO_RELOCK_FORBIDDEN'), ('wrong_node','P6_TARGET_DRIFT'),
    ('render','RENDER_NOT_AUTHORIZED'), ('promote','CAPSULE_IDENTITY_DRIFT'),
    ('objective','OBJECTIVE_DRIFT'), ('no_receipt','P6_COUNT_CONFLICT'),
    ('boundary','P6_BOUNDARY_WEAKENED')])
def test_p6_semantic_drift_fails_even_with_resealed_hash(repo,case,reason):
    lock=read(repo,LOCK)
    if case=='relock':lock['p6_integrated_design']['frames'][1]['locked']=True
    elif case=='wrong_node':lock['p6_integrated_design']['frames'][1]['photo']='12:20'
    elif case=='render':lock['render_allowed']=True
    elif case=='promote':lock['capsule']['promoted']=True
    elif case=='objective':lock['objective']['text']='optimize one poster'
    elif case=='no_receipt':lock['p6_integrated_design']['frames'][1]['bound']=True
    elif case=='boundary':lock['execution_boundary']['do_not_relock_photo_nodes']=False
    reseal(repo,lock)
    with pytest.raises(TaskLockError,match=reason):validate_state(repo)


def test_frozen_bytes_still_guarded(repo):
    p=repo/'evidence/vpd/shanyeji/system_level_holdout_validation_v1/H1_CONTROLLER_PAYLOAD.json'
    p.write_bytes(p.read_bytes()+b' ')
    with pytest.raises(TaskLockError,match='FROZEN_BYTES_CHANGED'):validate_state(repo)


def test_historical_ledger_cannot_be_rehashed(repo):
    p=repo/'continuity/vpd/state_ledger/system_validation.jsonl'
    p.write_bytes(p.read_bytes().replace(b'EVT-',b'OLD-',1))
    with pytest.raises(TaskLockError,match='HISTORICAL_LEDGER_REWRITTEN'):validate_state(repo)


def test_stale_adapter_fails(repo):
    a=read(repo,'PROJECT_CONTROL_ADAPTER.json');a['task_lock']['sha256']='0'*64
    write(repo,'PROJECT_CONTROL_ADAPTER.json',a)
    with pytest.raises(TaskLockError,match='EVIDENCE_HASH_MISMATCH'):validate_state(repo)


def test_git_eol_compatibility_does_not_hide_changes(tmp_path):
    subprocess.run(['git','init','-q',str(tmp_path)],check=True)
    subprocess.run(['git','-C',str(tmp_path),'config','core.autocrlf','true'],check=True)
    p=tmp_path/'frozen.txt';p.write_bytes(b'one\n')
    subprocess.run(['git','-C',str(tmp_path),'add','frozen.txt'],check=True)
    p.write_bytes(b'one\r\n')
    assert digest(p)==hashlib.sha256(b'one\n').hexdigest()
    p.write_bytes(b'two\r\n')
    assert digest(p)!=hashlib.sha256(b'one\n').hexdigest()
    subprocess.run(['git','-C',str(tmp_path),'add','frozen.txt'],check=True)
    assert digest(p)!=hashlib.sha256(b'one\n').hexdigest()
