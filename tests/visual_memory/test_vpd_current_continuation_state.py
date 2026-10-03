"""Real native metadata plus isolated mutations; fixtures are never runtime evidence."""
import copy
import hashlib
import io
import json
import shutil
import subprocess
import tarfile
from pathlib import Path

import pytest

from visual_memory.vpd_task_lock import (
    LOCK_PATH, CHECKPOINT_PATH, TaskLockError, digest, validate_state, validate_request, status_card,
)
from visual_memory.vpd_locked_mainline_state import HUMAN_FINAL_TASK, TAKEOVER_TASK

ROOT = Path(__file__).resolve().parents[2]
SOURCE = '003cfdfaa6481f8ac41cc46f56539bb4782ec34b'
BASE = 'continuity/vpd/codex_takeover_20261003/'
LEDGER = 'continuity/vpd/state_ledger/commercial_design_pipeline.jsonl'


def load(root, name):
    return json.loads((root / name).read_text(encoding='utf-8'))


def save(root, name, data):
    p = root / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return {'path': name, 'sha256': digest(p)}


def event_hash(event):
    data = dict(event)
    data.pop('event_hash', None)
    return hashlib.sha256(json.dumps(data, ensure_ascii=False, sort_keys=True,
        separators=(',', ':')).encode()).hexdigest()


def reseal(root, lock):
    """Reseal temporary projections so failures prove semantics beyond stale hashes."""
    lr = save(root, LOCK_PATH, lock)
    cp, adapter = load(root, CHECKPOINT_PATH), load(root, 'PROJECT_CONTROL_ADAPTER.json')
    take = lock.get('codex_takeover')
    task = take['task_id'] if take else HUMAN_FINAL_TASK
    cp.update(status=lock['status'], next_required_action=lock['next_required_action'],
              task_lock=dict(lr, revision=lock['revision']), active_task_ids=[task],
              mainline_progress=copy.deepcopy(lock['mainline_progress']),
              candidate88_human_final_review=copy.deepcopy(lock['candidate88_human_final_review']),
              candidate88_external_review_r4=copy.deepcopy(lock['candidate88_external_review_r4']),
              latest_evidence=lock['latest_evidence'])
    current = adapter['current_mainline']
    current.update(task_id=task, status=lock['status'], next_required_action=lock['next_required_action'])
    current['evidence'] = {'human_verdict': {k: lock['candidate88_human_final_review'][k]
                                          for k in ['path', 'sha256']}}
    adapter['task_lock'].update(**lr, revision=lock['revision'])
    ledger = root / LEDGER
    lines = ledger.read_bytes().splitlines(keepends=True)
    event = json.loads(lines[-1])
    event.update(task_id=task, lock_sha256=lr['sha256'])
    if take:
        cp['codex_takeover'] = copy.deepcopy(take)
        current['codex_takeover'] = copy.deepcopy(take)
        current['evidence']['execution'] = take['receipt']
        event.update(authorization=take['authorization'], evidence=[take['receipt'], take['photo_protection']],
                     after={'revision': lock['revision'], 'checkpoint': cp['sequence'],
                            'status': lock['status'], 'next_required_action': lock['next_required_action'],
                            'budget': take['budget']})
    else:
        cp.pop('codex_takeover', None)
        current.pop('codex_takeover', None)
        event['after'] = {'state': lock['status'], 'next_action': lock['next_required_action']}
    event['event_hash'] = event_hash(event)
    lines[-1] = (json.dumps(event, ensure_ascii=False) + '\n').encode()
    ledger.write_bytes(b''.join(lines))
    tail = {'commercial_design_pipeline': {k: event[k] for k in ['event_id', 'event_hash']}}
    cp['ledger_tails'] = copy.deepcopy(tail)
    adapter['ledger_tails'] = copy.deepcopy(tail)
    save(root, CHECKPOINT_PATH, cp)
    save(root, 'PROJECT_CONTROL_ADAPTER.json', adapter)


@pytest.fixture(scope='module')
def native_snapshot(tmp_path_factory):
    root = tmp_path_factory.mktemp('native-current-snapshot') / 'repo'
    root.mkdir()
    archive = subprocess.check_output(['git', '-c', 'core.autocrlf=false', '-C', str(ROOT),
                                       'archive', '--format=tar', SOURCE])
    with tarfile.open(fileobj=io.BytesIO(archive)) as source:
        source.extractall(root, filter='data')
    for name in ['visual_memory/vpd_locked_mainline_state.py', 'visual_memory/vpd_task_lock.py']:
        shutil.copyfile(ROOT / name, root / name)
    # Fix only the two proven projection defects in the isolated fixture.
    # Actual repository mutations are exclusively the root executor's work.
    lock = load(root, LOCK_PATH)
    ref = lock['candidate88_external_review_r4']['revision']
    ref['output_sha256'] = ref['sha256']
    ref['sha256'] = digest(root / ref['path'])
    reseal(root, lock)
    return root


@pytest.fixture
def native(native_snapshot, tmp_path):
    root = tmp_path / 'repo'
    shutil.copytree(native_snapshot, root)
    return root


@pytest.fixture
def takeover(native):
    lock = load(native, LOCK_PATH)
    for name in ['EXECUTION_AUTHORIZATION.json', 'PHOTO_PROTECTION.json']:
        save(native, BASE + name, load(ROOT, BASE + name))
    ref = lambda name: {'path': BASE + name, 'sha256': digest(native / (BASE + name))}
    take = {'task_id': TAKEOVER_TASK, 'status': 'VPD_CODEX_CHAZUO_AUTHORIZED_SOURCE_PROTECTED',
            'next_required_action': 'CREATE_ONE_EDITABLE_CHAZUO_POSTER_VERSION_1',
            'authorization': ref('EXECUTION_AUTHORIZATION.json'),
            'photo_protection': ref('PHOTO_PROTECTION.json'),
            'receipt': ref('EXECUTION_AUTHORIZATION.json'),
            'budget': {'formal_versions_max': 3, 'formal_versions_used': 0, 'revisions_max': 2,
                       'revisions_used': 0, 'photo_generations': 0, 'paid_compute_usd': 0,
                       'training': 0, 'automations': 0, 'second_style': 0},
            'human_verdict': 'PENDING', 'candidate_promoted': False,
            'state_writer': 'ROOT_EXECUTOR_ONLY'}
    lock.update(codex_takeover=take, current_task_id=TAKEOVER_TASK, status=take['status'],
                next_required_action=take['next_required_action'], latest_evidence=take['receipt'])
    lock['execution_boundary'].update(current_figma_canvas_authorization=3,
        current_image_generation_authorization_scope=TAKEOVER_TASK, successor_execution_authorized=True,
        bounded_typography_design_versions_authorization=take['authorization'])
    reseal(native, lock)
    return native


def test_real_252_274_current_route_and_p7_history_are_both_checked(native):
    lock, cp = validate_state(native)
    assert (lock['revision'], cp['sequence']) == (252, 274)
    assert cp['active_task_ids'] == [HUMAN_FINAL_TASK]
    assert lock['mainline_progress']['status'] == 'COMPLETED'
    assert lock['next_required_action'] != 'MAINLINE_DELIVERY_COMPLETE_STOP'
    card = status_card(lock, cp)
    assert card['真人结论'] == 'HUMAN_FAIL_DESIGN_SYSTEM_NOT_READY'
    assert card['当前任务'] == HUMAN_FINAL_TASK
    assert card['当前出图授权'] == card['当前Figma授权'] == 0


def test_original_checkpoint_drift_is_rejected(native):
    original = subprocess.check_output(['git', '-C', str(ROOT), 'cat-file', 'blob',
                                       SOURCE + ':' + CHECKPOINT_PATH])
    cp = load(native, CHECKPOINT_PATH)
    cp['mainline_progress'] = json.loads(original)['mainline_progress']
    save(native, CHECKPOINT_PATH, cp)
    with pytest.raises(TaskLockError, match='PROGRESS_MIRROR_CONFLICT'):
        validate_state(native)


def test_original_image_hash_in_json_reference_is_rejected(native):
    lock = load(native, LOCK_PATH)
    ref = lock['candidate88_external_review_r4']['revision']
    ref['sha256'] = ref['output_sha256']
    reseal(native, lock)
    with pytest.raises(TaskLockError, match='EVIDENCE_HASH_MISMATCH'):
        validate_state(native)


@pytest.mark.parametrize('case,reason', [
    ('task', 'CURRENT_TASK_CHANGED'),
    ('checkpoint_task', 'CURRENT_TASK_CHANGED'),
    ('old_next', 'HUMAN_FINAL_ROUTE_CONFLICT'),
    ('photo_flag', 'HUMAN_FINAL_SCOPE_CHANGED'),
    ('photo_mutation', 'PHOTO_PROTECTION_CHANGED'),
    ('images', 'RENDER_NOT_AUTHORIZED'),
    ('figma', 'RENDER_NOT_AUTHORIZED'),
    ('reference', 'EVIDENCE_HASH_MISMATCH'),
    ('historical_stage', 'HISTORICAL_DELIVERY_CHANGED'),
])
def test_current_human_route_rejects_real_semantic_drift(native, case, reason):
    lock = load(native, LOCK_PATH)
    if case == 'task':
        adapter = load(native, 'PROJECT_CONTROL_ADAPTER.json')
        adapter['current_mainline']['task_id'] = 'UNRELATED_TASK'
        save(native, 'PROJECT_CONTROL_ADAPTER.json', adapter)
    elif case == 'checkpoint_task':
        cp = load(native, CHECKPOINT_PATH)
        cp['active_task_ids'] = [lock['parent_active_task_id']]
        save(native, CHECKPOINT_PATH, cp)
    else:
        if case == 'old_next':
            lock['next_required_action'] = 'MAINLINE_DELIVERY_COMPLETE_STOP'
        elif case == 'photo_flag':
            lock['candidate88_human_final_review']['photo_protected'] = False
        elif case == 'photo_mutation':
            lock['execution_boundary']['modify_accepted_repair03_photo'] = True
        elif case == 'images':
            lock['execution_boundary']['current_image_generation_authorization'] = 1
        elif case == 'figma':
            lock['execution_boundary']['current_figma_canvas_authorization'] = 1
        elif case == 'reference':
            lock['candidate88_human_final_review']['sha256'] = '0' * 64
        elif case == 'historical_stage':
            lock['mainline_progress']['stage_id'] = 'P4_CONTENT'
        reseal(native, lock)
    with pytest.raises(TaskLockError, match=reason):
        validate_state(native)


def test_new_user_receipt_authorizes_three_versions_without_reopening_p7(takeover):
    lock, cp = validate_state(takeover)
    assert cp['active_task_ids'] == [TAKEOVER_TASK]
    assert lock['mainline_progress']['planned_attempts_max'] == 0
    assert lock['mainline_progress']['status'] == 'COMPLETED'
    assert not lock['render_allowed']
    card = status_card(lock, cp)
    assert card['正式设计版本'] == '0/3'
    assert card['真人结论'] == 'PENDING'
    assert card['当前Figma授权'] == 3
    action = {'action': lock['next_required_action'], 'lock_sha256': digest(takeover / LOCK_PATH),
              'task_id': TAKEOVER_TASK, 'figma_write': True, 'formal_version': 1,
              'authorization': lock['codex_takeover']['authorization'],
              'photo_protection': lock['codex_takeover']['photo_protection']}
    assert validate_request(takeover, action) == lock
    with pytest.raises(TaskLockError, match='REQUEST_BUDGET_EXCEEDED'):
        validate_request(takeover, dict(action, formal_version=4))
    with pytest.raises(TaskLockError, match='RENDER_NOT_AUTHORIZED'):
        validate_request(takeover, {'action': lock['next_required_action'],
                                   'lock_sha256': digest(takeover / LOCK_PATH), 'render': True})


@pytest.mark.parametrize('case,reason', [
    ('task', 'CONTINUATION_MIRROR_CONFLICT'),
    ('max', 'BUDGET_CHANGED'),
    ('extra_version', 'BUDGET_CHANGED'),
    ('photo_budget', 'BUDGET_CHANGED'),
    ('paid', 'BUDGET_CHANGED'),
    ('authorization_hash', 'EVIDENCE_HASH_MISMATCH'),
    ('authority_scope', 'CONTINUATION_SCOPE_CHANGED'),
    ('source', 'PHOTO_PROTECTION_CHANGED'),
    ('overlay', 'PHOTO_PROTECTION_CHANGED'),
    ('source_overwrite', 'PHOTO_PROTECTION_CHANGED'),
    ('next', 'CONTINUATION_ACTION_CONFLICT'),
    ('human_pass', 'CONTINUATION_SCOPE_CHANGED'),
    ('projection', 'CONTINUATION_MIRROR_CONFLICT'),
])
def test_takeover_rejects_scope_budget_protection_and_reference_drift(takeover, case, reason):
    lock = load(takeover, LOCK_PATH)
    take = lock['codex_takeover']
    if case == 'task':
        take['task_id'] = 'UNRELATED_SUCCESSOR'
    elif case == 'max':
        take['budget']['formal_versions_max'] = 4
    elif case == 'extra_version':
        take['budget']['formal_versions_used'] = 4
    elif case == 'photo_budget':
        take['budget']['photo_generations'] = 1
    elif case == 'paid':
        take['budget']['paid_compute_usd'] = 1
    elif case == 'authorization_hash':
        take['authorization']['sha256'] = '0' * 64
    elif case == 'authority_scope':
        data = load(takeover, take['authorization']['path'])
        data['authorized_scope']['new_global_task_system'] = True
        take['authorization'] = save(takeover, take['authorization']['path'], data)
        take['receipt'] = lock['latest_evidence'] = take['authorization']
        lock['execution_boundary']['bounded_typography_design_versions_authorization'] = take['authorization']
    elif case in ['source', 'overlay', 'source_overwrite']:
        data = load(takeover, take['photo_protection']['path'])
        if case == 'source':
            data['source']['sha256'] = '0' * 64
        elif case == 'overlay':
            data['visible_design_overlay_envelopes'][0][0] = 0
        else:
            data['source_file_overwrite_allowed'] = True
        take['photo_protection'] = save(takeover, take['photo_protection']['path'], data)
    elif case == 'next':
        lock['next_required_action'] = take['next_required_action'] = 'RUN_SECOND_STYLE'
    elif case == 'human_pass':
        take['human_verdict'] = 'PASSED'
    if case == 'projection':
        adapter = load(takeover, 'PROJECT_CONTROL_ADAPTER.json')
        adapter['current_mainline']['codex_takeover']['budget']['formal_versions_max'] = 4
        save(takeover, 'PROJECT_CONTROL_ADAPTER.json', adapter)
    else:
        reseal(takeover, lock)
    with pytest.raises(TaskLockError, match=reason):
        validate_state(takeover)


def test_rewritten_current_ledger_hash_is_rejected(takeover):
    ledger = takeover / LEDGER
    lines = ledger.read_bytes().splitlines(keepends=True)
    event = json.loads(lines[-1])
    event['after']['budget']['formal_versions_max'] = 4
    lines[-1] = (json.dumps(event, ensure_ascii=False) + '\n').encode()
    ledger.write_bytes(b''.join(lines))
    with pytest.raises(TaskLockError, match='LEDGER_HASH_MISMATCH'):
        validate_state(takeover)


def test_append_only_budget_cannot_roll_back(takeover):
    ledger = takeover / LEDGER
    lines = ledger.read_bytes().splitlines(keepends=True)
    event = json.loads(lines[-1])
    prior = copy.deepcopy(event)
    prior['event_id'] = 'SYNTHETIC_PRIOR_VERSION_NOT_RUNTIME_EVIDENCE'
    prior['after']['budget']['formal_versions_used'] = 1
    prior['event_hash'] = event_hash(prior)
    event.update(previous_event_id=prior['event_id'], previous_event_hash=prior['event_hash'])
    event['event_hash'] = event_hash(event)
    lines[-1:] = [(json.dumps(v, ensure_ascii=False) + '\n').encode() for v in [prior, event]]
    ledger.write_bytes(b''.join(lines))
    tail = {k: event[k] for k in ['event_id', 'event_hash']}
    for name in [CHECKPOINT_PATH, 'PROJECT_CONTROL_ADAPTER.json']:
        data = load(takeover, name)
        data['ledger_tails']['commercial_design_pipeline'] = tail
        save(takeover, name, data)
    with pytest.raises(TaskLockError, match='CONTINUATION_BUDGET_ROLLBACK_OR_SKIP'):
        validate_state(takeover)


def test_executed_version_cannot_be_only_assertions(takeover):
    lock = load(takeover, LOCK_PATH)
    take = lock['codex_takeover']
    take['status'] = lock['status'] = 'VPD_CODEX_CHAZUO_AWAITING_PIXEL_REVIEW'
    take['next_required_action'] = lock['next_required_action'] = 'REVIEW_CURRENT_CHAZUO_POSTER_ACTUAL_PIXELS'
    take['budget']['formal_versions_used'] = 1
    lock['execution_boundary']['current_figma_canvas_authorization'] = 2
    assertion = {'task_id': TAKEOVER_TASK, 'status': take['status'],
                 'next_required_action': take['next_required_action'],
                 'budget': {'formal_versions_used': 1, 'revisions_used': 0},
                 'exported': True, 'pixels_passed': True}
    take['receipt'] = lock['latest_evidence'] = save(takeover, BASE + 'SYNTHETIC_ASSERTION_ONLY.json', assertion)
    reseal(takeover, lock)
    with pytest.raises(TaskLockError, match='CONTINUATION_ARTIFACT_REQUIRED'):
        validate_state(takeover)
