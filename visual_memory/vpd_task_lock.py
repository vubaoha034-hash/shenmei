"""Bounded VPD identity/state guard. Evidence checks, never a visual-quality oracle."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

LOCK_PATH = 'continuity/vpd/CURRENT_TASK_LOCK.json'
CHECKPOINT_PATH = 'continuity/vpd/LATEST_CHECKPOINT.json'
NEXT_ACTION = 'RECONCILE_FORMAL_RENDER_ATTEMPT2_EVIDENCE'
PROJECT = 'visual-aesthetic-vpd'
PARENT = 'VPD-SYSTEM-LEVEL-HOLDOUT-TRANSFER-VALIDATION-V1'

class TaskLockError(ValueError):
    pass

def require(condition, code):
    if not condition:
        raise TaskLockError(code)

def path(root, value):
    require(isinstance(value, str), 'INVALID_PATH')
    root = Path(root).resolve()
    p = (root / value).resolve()
    require(p.is_relative_to(root), 'PATH_ESCAPE')
    return p

def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def unique_object(pairs):
    out = {}
    for k, v in pairs:
        require(k not in out, 'DUPLICATE_STATE_KEY')
        out[k] = v
    return out

def read(root, name):
    return json.loads(path(root, name).read_text(encoding='utf-8'), object_pairs_hook=unique_object)

def check_ref(root, ref):
    require(isinstance(ref, dict) and {'path', 'sha256'} <= ref.keys(), 'MISSING_EVIDENCE_REFERENCE')
    require(digest(path(root, ref['path'])) == ref['sha256'], 'EVIDENCE_HASH_MISMATCH:' + ref['path'])

def validate_ledger(root, checkpoint):
    for stream, tail in checkpoint['ledger_tails'].items():
        p = path(root, f'continuity/vpd/state_ledger/{stream}.jsonl')
        previous = None
        for line in p.read_text(encoding='utf-8').splitlines():
            event = json.loads(line, object_pairs_hook=unique_object)
            claimed = event.pop('event_hash')
            actual = hashlib.sha256(json.dumps(event, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
            require(claimed == actual, 'LEDGER_HASH_MISMATCH')
            require(event['previous_event_id'] == (previous['event_id'] if previous else None), 'LEDGER_PARENT_ID')
            require(event['previous_event_hash'] == (previous['event_hash'] if previous else None), 'LEDGER_PARENT_HASH')
            previous = {'event_id': event['event_id'], 'event_hash': claimed}
        require(previous == tail, 'LEDGER_TAIL_MISMATCH')

def validate_state(root):
    adapter = read(root, 'PROJECT_CONTROL_ADAPTER.json')
    dispatch = adapter['task_lock']
    require(dispatch['path'] == LOCK_PATH, 'WRONG_TASK_LOCK_PATH')
    require(adapter.get('task_registry_path') == LOCK_PATH, 'COMPETING_TASK_INDEX')
    check_ref(root, dispatch)
    lock = read(root, LOCK_PATH)
    cp = read(root, CHECKPOINT_PATH)
    require(lock['schema_version'] == 'vpd-current-task-lock/v1', 'LOCK_SCHEMA')
    require(lock['project_id'] == PROJECT == cp['project_id'], 'PROJECT_ID_MISMATCH')
    require(lock['parent_active_task_id'] == PARENT and cp['active_task_ids'] == [PARENT], 'PARENT_TASK_CHANGED')
    require(lock['revision'] == dispatch['revision'], 'STALE_LOCK_REVISION')
    require(cp['task_lock'] == {'path': LOCK_PATH, 'sha256': digest(path(root, LOCK_PATH))}, 'STALE_CHECKPOINT_LOCK')
    require(cp['sequence'] > 22, 'STALE_CURRENT_CHECKPOINT')
    require(cp['status'] == lock['status'] == adapter['vpd_system_goal_authority']['checkpoint'], 'STATE_STATUS_CONFLICT')
    require(cp['next_required_action'] == lock['next_required_action'] == adapter['vpd_system_goal_authority']['next_required_action'] == NEXT_ACTION, 'NEXT_ACTION_DRIFT')
    require(not lock['render_allowed'] and not adapter['vpd_system_goal_authority']['render_allowed'], 'RENDER_NOT_AUTHORIZED')
    workflow = lock['workflow']['document']
    check_ref(root, workflow)
    require(cp['workflow'] == workflow and {k: adapter['workflow'][k] for k in ['path', 'sha256']} == workflow, 'WORKFLOW_REFERENCE_CONFLICT')
    require(adapter['workflow']['current_progress_path'] == LOCK_PATH and lock['workflow']['status_authority'] == LOCK_PATH, 'COMPETING_TASK_INDEX')
    review = lock['requirements'].get('task_lock_state_readback_review', {})
    require(review.get('status') == 'DONE', 'REVIEW_REQUIRED_BEFORE_RECONCILIATION')
    check_ref(root, review['evidence'])
    decision = read(root, review['evidence']['path'])
    require(decision['completed_action'] == 'CHATGPT_REVIEW_TASK_LOCK_AND_STATE_READBACK' and decision['review_result'] == 'PASS' and decision['next_required_action'] == NEXT_ACTION, 'REVIEW_DECISION_CONFLICT')
    for ref in lock['history']['previous_current_state'].values():
        check_ref(root, ref)
    for name in ['START_HERE.md', 'AGENTS.md']:
        text = path(root, name).read_text(encoding='utf-8')
        require(text.count('<!-- VPD_TASK_LOCK_ENTRY_V1 -->') == 1, 'ENTRYPOINT_NOT_UNIQUE')
        entry = text.split('<!-- VPD_TASK_LOCK_ENTRY_V1 -->')[1].split('<!-- END_VPD_TASK_LOCK_ENTRY_V1 -->')[0]
        require(LOCK_PATH in entry and 'python scripts/verify_visual_memory.py --vpd-state --status-card' in entry, 'ENTRYPOINT_LOCK_OR_VALIDATOR_MISSING')
        require(workflow['path'] in entry, 'ENTRYPOINT_WORKFLOW_MISSING')
    for ref in [lock['changes_authority'], lock['immutable_baseline'], lock['anomaly_evidence'], lock['objective']['authority'], lock['source_library']['locator_receipt']]:
        check_ref(root, ref)
    baseline = read(root, lock['immutable_baseline']['path'])
    require(baseline['input_commit'] == lock['input_commit'], 'BASELINE_COMMIT_CONFLICT')
    for name, expected in baseline['files'].items():
        require(digest(path(root, name)) == expected, 'FROZEN_BYTES_CHANGED:' + name)
    for ref in lock['history']['snapshots'].values():
        check_ref(root, ref)
    require(cp['history_snapshot'] == lock['history']['snapshots'][CHECKPOINT_PATH], 'HISTORY_SCOPE_CONFLICT')
    historic_cp = read(root, cp['history_snapshot']['path'])
    require(cp['highest_accepted_checkpoint'] == historic_cp['highest_accepted_checkpoint'], 'HISTORICAL_ACCEPTANCE_CHANGED')
    old_ledger = lock['history']['snapshots']['continuity/vpd/state_ledger/system_validation.jsonl']
    require(path(root, 'continuity/vpd/state_ledger/system_validation.jsonl').read_bytes().startswith(path(root, old_ledger['path']).read_bytes()), 'HISTORICAL_LEDGER_REWRITTEN')
    require(not set(cp['completed']) & set(cp['incomplete']), 'COMPLETED_AND_INCOMPLETE')
    require(cp['requirements'] == lock['requirements'], 'REQUIREMENT_MIRROR_CONFLICT')
    for name, value in lock['requirements'].items():
        require(not (value['status'] == 'DONE' and name in cp['incomplete']), 'DONE_REQUIREMENT_PENDING')
        require(not (value['status'] != 'DONE' and name in cp['completed']), 'PENDING_REQUIREMENT_DONE')
        if value['status'] == 'DONE':
            require(name in cp['completed'], 'DONE_REQUIREMENT_MISSING')
            check_ref(root, value['evidence'])
    located = read(root, lock['source_library']['locator_receipt']['path'])
    require(located['folder_id'] == lock['source_library']['folder_id'], 'SOURCE_LIBRARY_CHANGED')
    require(located['entries'] == lock['source_library']['entries'], 'SOURCE_ROLE_OR_ID_CHANGED')
    for source in located['entries']:
        require(source['role'] == 'APPROVED_LIBRARY_ENTRY', 'FEEDBACK_AS_SOURCE')
        check_ref(root, source['approval_evidence'])
    require(lock['objective']['single_poster_optimization'] is False, 'OBJECTIVE_DRIFT')
    require(lock['objective']['text'] == '从用户原先批准的海报真实像素蒸馏可复用视觉程序，用新作品验证视觉逻辑、迁移能力和质量；不同家族共用同一个蒸馏器。', 'OBJECTIVE_DRIFT')
    candidate = read(root, 'evidence/vpd/shanyeji/style_capsule_v1_1_candidate/CAPSULE_V1_1_CANDIDATE_IDENTITY.json')
    require(lock['capsule']['id'] == candidate['candidate_id'] and lock['family'] == candidate['family_scope'], 'CAPSULE_IDENTITY_DRIFT')
    require(lock['capsule']['sha256'] == candidate['candidate_artifact']['sha256'], 'CAPSULE_HASH_DRIFT')
    experiment = lock['experiment']
    identity = read(root, 'evidence/vpd/shanyeji/system_level_holdout_validation_v1/FORMAL_RENDER_ATTEMPT2_IDENTITY_V1.json')
    require(experiment['renderer_attempt'] == identity['identity_id'] and experiment['task_id'] == PARENT, 'RENDERER_ATTEMPT_IDENTITY_DRIFT')
    anchor = experiment['runtime_anchor']
    check_ref(root, anchor['manifest']); check_ref(root, anchor['authorization']); check_ref(root, anchor['source_approval'])
    manifest = read(root, anchor['manifest']['path'])
    canonical = manifest['positive_runtime_anchors'][0]
    require(experiment['reference_count'] == manifest['reference_image_count'] == 1, 'HISTORICAL_ZERO_REFERENCE_LEAK')
    require(anchor['role'] == 'EXPERIMENT_RUNTIME_ANCHOR' and anchor['scope'] == ['H1', 'H2', 'H3', 'H4'], 'RUNTIME_ROLE_SCOPE_CHANGED')
    require(anchor['drive_file_id'] == canonical['drive_file_id'] and anchor['sha256'] == canonical['sha256'], 'FEEDBACK_AS_RUNTIME_ANCHOR')
    require(set(experiment['payloads']) == {'H1', 'H2', 'H3', 'H4'}, 'CHALLENGE_SET_CHANGED')
    for challenge, ref in experiment['payloads'].items():
        check_ref(root, ref)
        payload = read(root, ref['path'])
        require(payload['challenge_id'] == challenge, 'PAYLOAD_IDENTITY_CROSSOVER')
        require(payload['runtime_visual_anchor']['sha256'] == anchor['sha256'], 'PAYLOAD_ANCHOR_CONFLICT')
    check_ref(root, experiment['freeze_receipt']); check_ref(root, experiment['handoff']); check_ref(root, lock['capsule'])
    require(experiment['handoff']['consumption'] == 'EXTERNAL_EXECUTION_REPORTED_UNRECONCILED' and experiment['handoff']['automatic_replay'] is False, 'HANDOFF_REPLAY_NOT_AUTHORIZED')
    require(cp['execution'] == lock['execution'], 'EXECUTION_MIRROR_CONFLICT')
    execution = lock['execution']
    require(execution['bound_anchor'] == execution['bound_payloads'] == execution['calls'] == 'UNKNOWN', 'SELF_ASSERTED_BINDING_OR_CALL_PASS')
    require(execution['verified_outputs'] is None, 'OUTPUT_VERIFICATION_WITHOUT_EVIDENCE')
    require(not lock['capsule']['promoted'] and execution['human_acceptance'] == 'NOT_ACCEPTED', 'MISSING_HUMAN_ACCEPTANCE')
    for ref in cp['source_state_refs']:
        check_ref(root, ref)
    validate_ledger(root, cp)
    return lock, cp

def validate_request(root, request):
    """Validate a proposed dispatch/claim before accepting it; does not perform actions."""
    lock, cp = validate_state(root)
    require(request.get('lock_sha256') == digest(path(root, LOCK_PATH)), 'REQUEST_STALE_LOCK')
    action = request.get('action')
    # This evidence-reconciliation scope grants no rendering or domain mutations.
    require(not request.get('changes'), 'SCOPED_CHANGE_AUTHORITY_REQUIRED')
    require(action == NEXT_ACTION, 'ACTION_NOT_AUTHORIZED_OR_REPLAY')
    if request.get('source_role_change'):
        raise TaskLockError('SOURCE_ROLE_CHANGE_NOT_AUTHORIZED')
    if request.get('binding_pass'):
        raise TaskLockError('SELF_ASSERTED_BINDING_PASS')
    if request.get('accepted') or request.get('promoted'):
        raise TaskLockError('MISSING_HUMAN_ACCEPTANCE')
    output = request.get('output')
    if output:
        challenge = output.get('challenge_id')
        require(challenge in lock['experiment']['payloads'], 'UNKNOWN_OUTPUT_CHALLENGE')
        payload = read(root, lock['experiment']['payloads'][challenge]['path'])
        require(output.get('experiment_id') == payload['experiment_id'], 'OUTPUT_IDENTITY_CROSSOVER')
        require(output.get('payload_sha256') == lock['experiment']['payloads'][challenge]['sha256'], 'OUTPUT_PAYLOAD_HASH_MISMATCH')
        require(not output.get('verified'), 'UNRECONCILED_OUTPUT_CANNOT_BE_VERIFIED_BY_FILENAME')
    export = request.get('export')
    if export and export.get('formal'):
        raise TaskLockError('FORMAL_EXPORT_NOT_AUTHORIZED_OR_PROXY')
    if request.get('remote_verified'):
        evidence = request.get('remote_readback') or {}
        require(evidence.get('kind') == 'GITHUB_CONNECTOR_INDEPENDENT_READBACK', 'LOCAL_OR_CACHED_REF_NOT_REMOTE_PROOF')
        require(evidence.get('repository') == lock['repository'] and evidence.get('branch') == lock['branch'], 'REMOTE_IDENTITY_MISMATCH')
        commit = evidence.get('commit', '')
        require(len(commit) == 40 and all(c in '0123456789abcdef' for c in commit), 'REMOTE_COMMIT_MISSING')
        require(evidence.get('live_ref_commit') == commit and evidence.get('observed_at'), 'REMOTE_REF_NOT_READ')
        observed = evidence.get('file_sha256', {})
        for p in [LOCK_PATH, CHECKPOINT_PATH, 'PROJECT_CONTROL_ADAPTER.json']:
            require(observed.get(p) == digest(path(root, p)), 'REMOTE_FILE_NOT_READ_BACK')
    return lock

def status_card(lock, cp):
    return {'主目标':lock['objective']['text'], '完整流程':lock['workflow']['document']['path'], '当前母参考/源库':'原 approved_refs 18 条登记及独立批准的山野集；山野集仅为当前家族', '当前阶段':lock['current_stage'], '本轮实际完成':lock['completed_this_revision'], '未完成/阻塞':lock['blockers'], '唯一下一动作':lock['next_required_action'], '证据/远端版本':{'起始远端提交':lock['input_commit'],'当前锁修订':lock['revision'],'当前检查点':cp['sequence'],'远端发布回读':'须单独提供真实工具回读，不从本地文件推定'}}
