"""Metadata regression tests. Synthetic receipts are never runtime evidence."""
import json
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from visual_memory.vpd_task_lock import (
    LOCK_PATH, CHECKPOINT_PATH, TaskLockError, digest, validate_state, validate_request,
)

ROOT = Path(__file__).resolve().parents[2]


def load(root, name):
    return json.loads((root / name).read_text(encoding='utf-8'))


def save(root, name, value):
    dest = root / name
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return {'path': name, 'sha256': digest(dest)}


@pytest.fixture(scope='module')
def snapshot(tmp_path_factory):
    target = tmp_path_factory.mktemp('locked-mainline-snapshot') / 'repo'
    shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns('.git', '__pycache__', '.pytest_cache'))
    # Fixed R1 preparation scenario, independent of later legitimate progress.
    # Only this temporary fixture is normalized; live state is checked by CLI/CI.
    lock = load(target, LOCK_PATH)
    contract = load(target, lock['mainline_lock']['contract']['path'])
    lock['mainline_progress'] = {
        'stage_id': 'P3_STAGE1', 'status': 'READY_WAITING_EXECUTION_REQUEST',
        'task_id': contract['stage1']['task_id'], 'attempts_consumed': 0,
        'outputs': [], 'human_verdict': 'NOT_REVIEWED', 'completed_stage_receipts': [],
        'execution_authorization': {'status': 'NOT_REQUESTED', 'images': 0,
                                    'figma_writes': 0, 'external_compute_usd': 0},
        'planned_attempts_max': 2,
    }
    lock.update(render_allowed=False, next_required_action='WAIT_FOR_STAGE1_EXECUTION_REQUEST')
    lock['execution_boundary']['current_image_generation_authorization'] = 0
    reseal(target, lock)
    return target


@pytest.fixture
def isolated(snapshot, tmp_path):
    target = tmp_path / 'repo'
    shutil.copytree(snapshot, target)
    return target


def reseal(root, lock):
    """Rebind state/ledger so tests exercise semantics beyond stale hashes."""
    save(root, LOCK_PATH, lock)
    cp = load(root, CHECKPOINT_PATH)
    cp.update(task_lock={'path': LOCK_PATH, 'sha256': digest(root / LOCK_PATH)},
              mainline_progress=lock['mainline_progress'], mainline_lock=lock['mainline_lock'],
              status=lock['status'], next_required_action=lock['next_required_action'])
    adapter = load(root, 'PROJECT_CONTROL_ADAPTER.json')
    adapter['task_lock'].update(sha256=digest(root / LOCK_PATH), revision=lock['revision'])
    adapter['mainline_lock'] = lock['mainline_lock']
    adapter['vpd_system_goal_authority'].update(checkpoint=lock['status'],
        next_required_action=lock['next_required_action'], render_allowed=lock['render_allowed'])
    adapter['current_mainline'].update(status=lock['status'],
        subtask_id=lock['mainline_progress']['task_id'],
        next_required_action=lock['next_required_action'],
        current_generation_authorization=lock['mainline_progress']['execution_authorization']['images'],
        current_chat_render_eligible=lock['render_allowed'])
    ledger = root / 'continuity/vpd/state_ledger/commercial_design_pipeline.jsonl'
    lines = ledger.read_bytes().splitlines(keepends=True)
    event = json.loads(lines[-1])
    event['lock_sha256'] = digest(root / LOCK_PATH)
    event.pop('event_hash')
    event['event_hash'] = hashlib.sha256(json.dumps(event, ensure_ascii=False, sort_keys=True,
        separators=(',', ':')).encode()).hexdigest()
    lines[-1] = (json.dumps(event, ensure_ascii=False) + '\n').encode()
    ledger.write_bytes(b''.join(lines))
    tail = {k: event[k] for k in ['event_id', 'event_hash']}
    cp['ledger_tails']['commercial_design_pipeline'] = tail
    adapter['ledger_tails']['commercial_design_pipeline'] = tail
    save(root, CHECKPOINT_PATH, cp)
    save(root, 'PROJECT_CONTROL_ADAPTER.json', adapter)


def request(root, **extra):
    return dict(action=load(root, LOCK_PATH)['next_required_action'],
                lock_sha256=digest(root / LOCK_PATH), **extra)


def authorize_synthetic(root):
    lock = load(root, LOCK_PATH)
    p = lock['mainline_progress']
    ref = save(root, 'synthetic/authorization.json', {
        'authority_class': 'EXPLICIT_USER_STAGE_EXECUTION', 'task_id': p['task_id'],
        'source': 'SYNTHETIC_TEST_NOT_RUNTIME_EVIDENCE',
        'recorded_at': 'SYNTHETIC_TEST_NOT_RUNTIME_EVIDENCE', 'attempts_max': 2,
    })
    p['status'] = 'AUTHORIZED'
    p['execution_authorization'].update(status='EXPLICIT_USER_AUTHORIZED', images=2, receipt=ref)
    lock.update(render_allowed=True, next_required_action='EXECUTE_STAGE1_FROZEN_TASK')
    lock['execution_boundary']['current_image_generation_authorization'] = 2
    reseal(root, lock)
    return lock


def test_prepared_state_and_actual_cli_pass(isolated):
    lock, cp = validate_state(isolated)
    assert cp['sequence'] > 209 and lock['revision'] > 187
    assert lock['mainline_progress']['attempts_consumed'] == 0
    assert not lock['render_allowed']
    assert validate_request(isolated, request(isolated)) == lock
    result = subprocess.run([sys.executable, str(isolated / 'scripts/verify_visual_memory.py'),
        '--vpd-state', '--status-card'], capture_output=True, text=True, encoding='utf-8')
    assert result.returncode == 0, result.stdout
    assert json.loads(result.stdout)['真人结论'] == 'NOT_REVIEWED'


@pytest.mark.parametrize('case,reason', [
    ('goal', 'OBJECTIVE_DRIFT'),
    ('unlocked', 'MAINLINE_UNLOCKED'),
    ('old_acceptance', 'HISTORICAL_ACCEPTANCE_CHANGED'),
    ('old_candidate', 'PRESERVED_RESULT_CHANGED'),
    ('stage_jump', 'PRIOR_STAGE_EVIDENCE_REQUIRED'),
    ('self_pass', 'UNSUPPORTED_TEST_OR_ACCEPTANCE_CLAIM'),
    ('unauthorized_budget', 'RENDER_NOT_AUTHORIZED'),
    ('hidden_variants', 'BUDGET_CHANGED'),
    ('extra_attempt', 'BUDGET_CHANGED'),
    ('unproved_amendment', 'MISSING_EVIDENCE_REFERENCE'),
])
def test_semantic_drift_even_after_resealing(isolated, case, reason):
    lock = load(isolated, LOCK_PATH)
    p = lock['mainline_progress']
    if case == 'goal':
        lock['objective']['text'] = '只修一张茶作海报'
    elif case == 'unlocked':
        lock['mainline_lock']['locked'] = False
    elif case == 'old_acceptance':
        cp = load(isolated, CHECKPOINT_PATH)
        cp['highest_accepted_checkpoint'] = '未经真人验收的新结果'
        save(isolated, CHECKPOINT_PATH, cp)
    elif case == 'old_candidate':
        lock['chazuo_new_reference_lock_and_one_proof_candidate01']['reference_sha256'] = '0' * 64
    elif case == 'stage_jump':
        p.update(stage_id='P4_CONTENT', status='NEEDS_INPUT_FREEZE')
        lock['next_required_action'] = 'PREPARE_P4_CONTENT_INPUTS'
    elif case == 'self_pass':
        p.update(status='PASSED', human_verdict='PASSED')
        lock['next_required_action'] = 'PREPARE_NEXT_STAGE_AFTER_STAGE1'
    elif case == 'unauthorized_budget':
        p['execution_authorization']['images'] = 2
    elif case == 'hidden_variants':
        lock['execution_boundary']['current_image_generation_hidden_variants'] = 1
    elif case == 'extra_attempt':
        p['attempts_consumed'] = 3
    elif case == 'unproved_amendment':
        p['task_id'] = 'UNPROVED-R2'
    reseal(isolated, lock)
    with pytest.raises(TaskLockError, match=reason):
        validate_state(isolated)


def test_stale_projection_is_rejected(isolated):
    adapter = load(isolated, 'PROJECT_CONTROL_ADAPTER.json')
    adapter['task_lock']['revision'] = 180
    save(isolated, 'PROJECT_CONTROL_ADAPTER.json', adapter)
    with pytest.raises(TaskLockError, match='STALE_LOCK_REVISION'):
        validate_state(isolated)


@pytest.mark.parametrize('which', ['contract', 'prompt', 'historical_output', 'ledger_prefix'])
def test_frozen_input_or_history_change_fails(isolated, which):
    lock = load(isolated, LOCK_PATH)
    if which == 'contract':
        p = isolated / lock['mainline_lock']['contract']['path']
    elif which == 'prompt':
        p = isolated / 'continuity/vpd/stage1/DISTILLED_DELTA.txt'
    elif which == 'historical_output':
        preserve = load(isolated, lock['mainline_lock']['preservation']['path'])
        p = isolated / next(iter(preserve['immutable_files']))
    else:
        p = isolated / 'continuity/vpd/state_ledger/commercial_design_pipeline.jsonl'
        p.write_bytes(b' ' + p.read_bytes())
        with pytest.raises(TaskLockError, match='HISTORICAL_LEDGER_REWRITTEN'):
            validate_state(isolated)
        return
    p.write_bytes(p.read_bytes() + b' ')
    with pytest.raises(TaskLockError, match='EVIDENCE_HASH_MISMATCH|FROZEN_BYTES_CHANGED'):
        validate_state(isolated)


@pytest.mark.parametrize('flag', ['accepted', 'promoted', 'binding_pass', 'render'])
def test_preparation_cannot_claim_results_or_render(isolated, flag):
    with pytest.raises(TaskLockError, match='EXECUTION_OR_TEST_EVIDENCE_REQUIRED|RENDER_NOT_AUTHORIZED'):
        validate_request(isolated, request(isolated, **{flag: True}))


def test_explicit_bounded_authorization_is_supported_without_code_changes(isolated):
    lock = authorize_synthetic(isolated)
    assert validate_state(isolated)[0] == lock
    assert validate_request(isolated, request(isolated, render=True, attempts=2,
        frozen_inputs=lock['mainline_lock']['contract'])) == lock
    with pytest.raises(TaskLockError, match='REQUEST_BUDGET_EXCEEDED'):
        validate_request(isolated, request(isolated, render=True, attempts=3))


def test_boolean_authorization_without_user_receipt_fails(isolated):
    lock = authorize_synthetic(isolated)
    del lock['mainline_progress']['execution_authorization']['receipt']
    reseal(isolated, lock)
    with pytest.raises(TaskLockError, match='MISSING_EVIDENCE_REFERENCE'):
        validate_state(isolated)


def reviewed_synthetic(root, scope='WHOLE_POSTER', authority='HUMAN_USER_FEEDBACK'):
    lock = authorize_synthetic(root)
    p = lock['mainline_progress']
    trace = save(root, 'synthetic/call_trace.json', {
        'source': 'SYNTHETIC_TEST_NOT_RUNTIME_EVIDENCE', 'calls': ['SYNTHETIC_A', 'SYNTHETIC_B']})
    outputs = [{'asset_pointer': 'SYNTHETIC_A'}, {'asset_pointer': 'SYNTHETIC_B'}]
    execution = save(root, 'synthetic/execution.json', {
        'stage_id': 'P3_STAGE1', 'task_id': p['task_id'], 'attempts_consumed': 2,
        'outputs': outputs, 'trace': trace, 'frozen_inputs': lock['mainline_lock']['contract']})
    feedback = save(root, 'synthetic/feedback.json', {
        'authority_class': authority, 'task_id': p['task_id'], 'outcome': 'PASSED',
        'scope': scope, 'whole_poster_accepted': scope == 'WHOLE_POSTER',
        'source': 'SYNTHETIC_TEST_NOT_RUNTIME_EVIDENCE',
        'recorded_at': 'SYNTHETIC_TEST_NOT_RUNTIME_EVIDENCE'})
    review = save(root, 'synthetic/review.json', {
        'stage_id': 'P3_STAGE1', 'outcome': 'PASSED', 'scope': scope,
        'execution_receipt': execution, 'human_feedback': feedback})
    p.update(status='PASSED', attempts_consumed=2, outputs=outputs, human_verdict='PASSED',
             execution_receipt=execution, review_receipt=review)
    p['execution_authorization']['images'] = 0
    lock.update(render_allowed=False, next_required_action='PREPARE_NEXT_STAGE_AFTER_STAGE1')
    lock['execution_boundary']['current_image_generation_authorization'] = 0
    reseal(root, lock)
    return lock, review


@pytest.mark.parametrize('scope,authority,reason', [
    ('LOCAL_PHOTOGRAPHY', 'HUMAN_USER_FEEDBACK', 'WHOLE_HUMAN_ACCEPTANCE_REQUIRED'),
    ('WHOLE_POSTER', 'ASSISTANT_SELF_SCORE', 'HUMAN_FEEDBACK_REQUIRED'),
])
def test_local_or_machine_feedback_cannot_pass_whole_stage(isolated, scope, authority, reason):
    reviewed_synthetic(isolated, scope, authority)
    with pytest.raises(TaskLockError, match=reason):
        validate_state(isolated)


def test_whole_review_receipt_supports_next_stage_without_unlocking(isolated):
    lock, review = reviewed_synthetic(isolated)
    assert validate_state(isolated)[0] == lock
    lock['mainline_progress'] = {
        'stage_id': 'P4_CONTENT', 'status': 'NEEDS_INPUT_FREEZE', 'task_id': 'SYNTHETIC_P4',
        'attempts_consumed': 0, 'outputs': [], 'human_verdict': 'NOT_REVIEWED',
        'completed_stage_receipts': [review], 'planned_attempts_max': 4,
        'execution_authorization': {'status': 'NOT_REQUESTED', 'images': 0,
                                    'figma_writes': 0, 'external_compute_usd': 0},
    }
    lock['next_required_action'] = 'PREPARE_P4_CONTENT_INPUTS'
    reseal(isolated, lock)
    validated, _ = validate_state(isolated)
    assert validated['mainline_lock']['locked'] is True
    assert not validated['render_allowed']
