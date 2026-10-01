"""State compatibility for the locked mainline; never certifies visual quality.

Uses the existing lock/checkpoint/ledger. Historical defects stay disclosed and
byte-preserved. Repository checks constrain cooperating executors, not the host.
"""
import hashlib
import json

from .vpd_task_lock import (
    LOCK_PATH, CHECKPOINT_PATH, PROJECT, PARENT, read, path, require,
    check_ref, digest, evidence_bytes,
)

PROFILE = 'vpd-locked-mainline/v1'
STAGES = ['P3_STAGE1', 'P4_CONTENT', 'P4_ASPECT', 'P5_SECOND_STYLE', 'P7_DELIVERY']


def validate_locked_mainline(root):
    lock, cp = read(root, LOCK_PATH), read(root, CHECKPOINT_PATH)
    adapter = read(root, 'PROJECT_CONTROL_ADAPTER.json')
    require(lock['state_profile'] == PROFILE, 'LOCK_SCHEMA')
    require(lock['schema_version'] == 'vpd-current-task-lock/v1', 'LOCK_SCHEMA')
    require(lock['project_id'] == cp['project_id'] == adapter['project_id'] == PROJECT,
            'PROJECT_ID_MISMATCH')
    require(lock['parent_active_task_id'] == PARENT and cp['active_task_ids'] == [PARENT],
            'PARENT_TASK_CHANGED')
    require(lock['repository'] == adapter['repository'] == 'vubaoha034-hash/shenmei',
            'REPOSITORY_DRIFT')
    require(lock['branch'] == adapter['canonical_branch'] ==
            'visual-program-distillation-v2-photography-design-20260814', 'BRANCH_DRIFT')
    require(adapter['task_registry_path'] == adapter['task_lock']['path'] == LOCK_PATH,
            'COMPETING_TASK_INDEX')
    check_ref(root, adapter['task_lock'])
    require(adapter['task_lock']['revision'] == lock['revision'], 'STALE_LOCK_REVISION')
    require(cp['task_lock'] == {'path': LOCK_PATH, 'sha256': digest(path(root, LOCK_PATH))},
            'STALE_CHECKPOINT_LOCK')
    require(cp['status'] == lock['status'] == adapter['vpd_system_goal_authority']['checkpoint'] ==
            adapter['current_mainline']['status'],
            'STATE_STATUS_CONFLICT')
    require(lock['next_required_action'] == cp['next_required_action'] ==
            adapter['vpd_system_goal_authority']['next_required_action'] ==
            adapter['current_mainline']['next_required_action'], 'NEXT_ACTION_DRIFT')
    require(cp['mainline_lock'] == adapter['mainline_lock'] == lock['mainline_lock'],
            'MAINLINE_MIRROR_CONFLICT')
    require(cp['mainline_progress'] == lock['mainline_progress'], 'PROGRESS_MIRROR_CONFLICT')
    main = lock['mainline_lock']
    require(main['locked'] is True, 'MAINLINE_UNLOCKED')
    require(lock['mainline_plan'] == cp['mainline_plan'] == adapter['mainline_plan'] ==
            main['plan'] and lock['latest_evidence'] == cp['latest_evidence'] ==
            main['authority'], 'MAINLINE_MIRROR_CONFLICT')
    for name in ['plan', 'contract', 'authority', 'preservation']:
        check_ref(root, main[name])
    authority = read(root, main['authority']['path'])
    require(authority['authority_class'] == 'EXPLICIT_USER_MAINLINE_SAVE_AND_LOCK',
            'MAINLINE_AUTHORITY_MISSING')
    require(authority['authorized_scope']['generation_now'] is False,
            'SAVE_AUTHORITY_IS_NOT_RENDER_AUTHORITY')
    require(main['plan'] == authority['frozen_plan'] and
            main['contract'] == authority['frozen_contract'], 'MAINLINE_CHANGED_WITHOUT_TEST_AMENDMENT')
    contract = read(root, main['contract']['path'])
    require(adapter['current_mainline']['plan'] == main['plan'] and
            adapter['current_mainline']['task_id'] == PARENT and
            adapter['current_mainline']['subtask_id'] == lock['mainline_progress']['task_id'] and
            main['id'] == contract['id'], 'MAINLINE_MIRROR_CONFLICT')
    preserve = read(root, main['preservation']['path'])
    for ref in preserve['snapshots'].values():
        check_ref(root, ref)
    old = read(root, preserve['snapshots']['lock']['path'])
    old_cp = read(root, preserve['snapshots']['checkpoint']['path'])
    require(lock['revision'] > old['revision'] and cp['sequence'] > old_cp['sequence'],
            'STATE_REVISION_ROLLBACK')
    require(lock['objective'] == contract['fixed_goal'] == old['objective'], 'OBJECTIVE_DRIFT')
    require(cp['highest_accepted_checkpoint'] == old_cp['highest_accepted_checkpoint'] and
            cp['highest_accepted_checkpoint_scope'] == old_cp['highest_accepted_checkpoint_scope'],
            'HISTORICAL_ACCEPTANCE_CHANGED')
    for name in ['capsule', 'mechanism_transfer_verdict', 'concept02',
                 'chazuo_concept02_photo_repair03', 'latest_human_review',
                 'chazuo_new_reference_lock_and_one_proof_candidate01']:
        require(lock.get(name) == old.get(name), 'PRESERVED_RESULT_CHANGED:' + name)
    for name, expected in preserve['immutable_files'].items():
        require(digest(path(root, name)) == expected, 'FROZEN_BYTES_CHANGED:' + name)
    require([s['id'] for s in contract['stages']] == STAGES, 'MAINLINE_STAGE_ORDER_CHANGED')
    require(contract['primary_renderer'] == 'CHATGPT_IMAGES', 'RENDERER_CHANGED')
    stage1 = contract['stage1']
    require(stage1['same_reference_in_both_arms'] is True and
            stage1['only_variable'] == 'ADDED_DISTILLED_VISUAL_RELATIONS', 'COMPARISON_CHANGED')
    require(stage1['budget'] == {'attempts_max': 2, 'per_arm': 1, 'retries': 0,
                                'hidden_variants': 0, 'best_of_n': False}, 'BUDGET_CHANGED')
    for ref in stage1['prompt_files'].values():
        check_ref(root, ref)
    require(stage1['reference']['sha256'] ==
            old['chazuo_new_reference_lock_and_one_proof_candidate01']['reference_sha256'],
            'REFERENCE_CHANGED')
    _validate_progress(root, lock, adapter, contract)
    require(not set(cp['completed']) & set(cp['incomplete']), 'COMPLETED_AND_INCOMPLETE')
    require(cp['workflow'] == lock['workflow']['document'] ==
            {k: adapter['workflow'][k] for k in ['path', 'sha256']},
            'WORKFLOW_REFERENCE_CONFLICT')
    check_ref(root, cp['workflow'])
    require(adapter['workflow']['current_progress_path'] == lock['workflow']['status_authority'] ==
            LOCK_PATH, 'COMPETING_TASK_INDEX')
    for name in ['START_HERE.md', 'AGENTS.md']:
        text = path(root, name).read_text(encoding='utf-8')
        require(text.count('<!-- VPD_TASK_LOCK_ENTRY_V1 -->') == 1 and
                main['plan']['path'] in text and LOCK_PATH in text, 'ENTRYPOINT_MAINLINE_MISSING')
    _validate_append_only_ledger(root, lock, cp, preserve)
    require(adapter['ledger_tails']['commercial_design_pipeline'] ==
            cp['ledger_tails']['commercial_design_pipeline'], 'LEDGER_TAIL_MISMATCH')
    return lock, cp


def _receipt(root, ref):
    check_ref(root, ref)
    return read(root, ref['path'])


def _delegated_review_authority(root, ref, stage_id, task_id):
    authority = _receipt(root, ref)
    require(authority.get('authority_class') == 'EXPLICIT_USER_DELEGATED_INDEPENDENT_REVIEW'
            and authority.get('project_id') == PROJECT and authority.get('source')
            and authority.get('recorded_at'), 'DELEGATED_REVIEW_AUTHORITY_REQUIRED')
    require(isinstance(task_id, str) and stage_id in authority.get('stage_ids', []) and
            task_id.startswith(authority.get('task_prefix') or '\0'),
            'DELEGATED_REVIEW_SCOPE_MISMATCH')
    require(authority.get('reviewer_url') and authority.get('callback_url') and
            authority.get('round_by_round_user_review_required') is False,
            'DELEGATED_REVIEW_ROUTE_REQUIRED')
    return authority


def _tested_result(root, ref, stage_id):
    """Check recorded provenance, never infer a verdict from the rendered pixels."""
    result = _receipt(root, ref)
    require(result.get('stage_id') == stage_id, 'TEST_STAGE_ID_MISMATCH')
    execution = _receipt(root, result.get('execution_receipt'))
    require(execution.get('stage_id') == stage_id and execution.get('attempts_consumed', 0) > 0,
            'ACTUAL_TEST_REQUIRED')
    _receipt(root, execution.get('trace'))
    delegated = result.get('delegated_review')
    feedback = _receipt(root, delegated or result.get('human_feedback'))
    if delegated:
        authority = _delegated_review_authority(root, feedback.get('delegation_authority'),
                                               stage_id, execution.get('task_id', ''))
        require(feedback.get('authority_class') == 'USER_DELEGATED_INDEPENDENT_REVIEW' and
                feedback.get('reviewer_url') == authority['reviewer_url'],
                'DELEGATED_REVIEWER_IDENTITY_MISMATCH')
        _receipt(root, feedback.get('callback_receipt'))
    else:
        require(feedback.get('authority_class') == 'HUMAN_USER_FEEDBACK',
                'HUMAN_FEEDBACK_REQUIRED')
    require(
            feedback.get('task_id') == execution.get('task_id') and
            feedback.get('source') and feedback.get('recorded_at'), 'HUMAN_FEEDBACK_REQUIRED')
    require(result.get('outcome') == feedback.get('outcome') and
            result.get('scope') == feedback.get('scope'), 'TEST_VERDICT_SCOPE_CONFLICT')
    if result.get('outcome') == 'PASSED':
        require(result.get('scope') == 'WHOLE_POSTER' and
                feedback.get('whole_poster_accepted') is True and execution.get('outputs'),
                'WHOLE_HUMAN_ACCEPTANCE_REQUIRED')
    return result


def _validate_progress(root, lock, adapter, contract):
    progress = lock['mainline_progress']
    stage_id, state = progress['stage_id'], progress['status']
    require(stage_id in STAGES, 'UNKNOWN_MAINLINE_STAGE')
    stage = next(s for s in contract['stages'] if s['id'] == stage_id)
    actions = dict(stage['actions'])
    if state == 'AWAITING_INDEPENDENT_REVIEW':
        _delegated_review_authority(root, progress.get('review_delegation'),
                                    stage_id, progress['task_id'])
        actions[state] = 'WAIT_FOR_INDEPENDENT_REVIEWER_CALLBACK'
    require(state in actions and lock['next_required_action'] == actions[state],
            'STAGE_ACTION_CONFLICT')
    receipts = progress['completed_stage_receipts']
    require(len(receipts) == STAGES.index(stage_id), 'PRIOR_STAGE_EVIDENCE_REQUIRED')
    for prior, ref in zip(STAGES, receipts):
        require(_tested_result(root, ref, prior)['outcome'] == 'PASSED',
                'PRIOR_WHOLE_ACCEPTANCE_REQUIRED')
    attempts, ceiling = progress['attempts_consumed'], stage['images_max']
    require(type(attempts) is int and 0 <= attempts <= ceiling and
            progress['planned_attempts_max'] == ceiling, 'BUDGET_CHANGED')
    if stage_id == 'P3_STAGE1' and progress['task_id'] == contract['stage1']['task_id']:
        frozen_inputs = lock['mainline_lock']['contract']
    else:
        frozen_inputs = progress.get('input_freeze')
        if state != 'NEEDS_INPUT_FREEZE':
            inputs = _receipt(root, frozen_inputs)
            require(inputs.get('stage_id') == stage_id and
                    inputs.get('task_id') == progress['task_id'], 'INPUT_FREEZE_IDENTITY_MISMATCH')
            require(inputs.get('input_refs'), 'INPUT_FREEZE_REQUIRED')
            for ref in inputs.get('input_refs', []):
                check_ref(root, ref)
    if stage_id == 'P3_STAGE1' and progress['task_id'] != contract['stage1']['task_id']:
        amendment = _receipt(root, progress.get('amendment_receipt'))
        require(amendment.get('trigger') in contract['amendment_policy']['allowed_triggers'] and
                all(amendment.get(k) for k in contract['amendment_policy']['required_evidence']),
                'EVIDENCE_BASED_AMENDMENT_REQUIRED')
        require(amendment.get('new_task_id') == progress['task_id'], 'AMENDMENT_TASK_MISMATCH')
        check_ref(root, amendment['actual_input_and_output_or_error_receipts'])
    auth = progress['execution_authorization']
    require(type(auth['images']) is int and 0 <= auth['images'] <= ceiling - attempts and
            auth['figma_writes'] == auth['external_compute_usd'] == 0, 'BUDGET_CHANGED')
    if auth['status'] != 'NOT_REQUESTED':
        receipt = _receipt(root, auth.get('receipt'))
        require(receipt.get('authority_class') == 'EXPLICIT_USER_STAGE_EXECUTION' and
                receipt.get('task_id') == progress['task_id'] and receipt.get('source') and
                receipt.get('recorded_at') and receipt.get('attempts_max') == ceiling,
                'EXPLICIT_EXECUTION_REQUEST_REQUIRED')
    else:
        require(auth['images'] == attempts == 0, 'RENDER_NOT_AUTHORIZED')
    eligible = state == 'AUTHORIZED' and auth['images'] > 0
    require(lock['render_allowed'] is eligible and
            adapter['vpd_system_goal_authority']['render_allowed'] is eligible and
            adapter['current_mainline']['current_chat_render_eligible'] is eligible and
            adapter['current_mainline']['current_generation_authorization'] == auth['images'] and
            lock['execution_boundary']['current_image_generation_authorization'] == auth['images'] and
            lock['execution_boundary']['current_figma_canvas_authorization'] == 0,
            'RENDER_AUTHORIZATION_MIRROR_CONFLICT')
    boundary = lock['execution_boundary']
    require(boundary['current_image_generation_hidden_variants'] ==
            boundary['current_image_generation_reroll'] ==
            boundary['current_image_generation_automatic_retry'] == 0 and
            boundary['current_image_generation_best_of_n'] is False, 'BUDGET_CHANGED')
    if state != 'AUTHORIZED':
        require(auth['images'] == 0, 'RENDER_NOT_AUTHORIZED')
    if attempts or progress['outputs']:
        execution = _receipt(root, progress.get('execution_receipt'))
        require(execution.get('stage_id') == stage_id and
                execution.get('task_id') == progress['task_id'] and
                execution.get('attempts_consumed') == attempts and
                execution.get('outputs') == progress['outputs'] and
                execution.get('frozen_inputs') == frozen_inputs, 'EXECUTION_RECEIPT_CONFLICT')
        _receipt(root, execution.get('trace'))
    else:
        require(progress['human_verdict'] == 'NOT_REVIEWED', 'UNSUPPORTED_TEST_OR_ACCEPTANCE_CLAIM')
    if state in ['PASSED', 'TEST_FAILED_OR_NO_GAIN', 'PARTIAL_OR_UNKNOWN']:
        result = _tested_result(root, progress.get('review_receipt'), stage_id)
        if result.get('delegated_review'):
            require(progress['human_verdict'] == 'NOT_REVIEWED' and
                    result['outcome'] == state == progress.get('review_verdict'),
                    'TEST_VERDICT_SCOPE_CONFLICT')
        else:
            require(result['outcome'] == state == progress['human_verdict'],
                    'TEST_VERDICT_SCOPE_CONFLICT')
        require(result['execution_receipt'] == progress.get('execution_receipt'),
                'REVIEW_EXECUTION_MISMATCH')
    else:
        require(progress['human_verdict'] == 'NOT_REVIEWED', 'UNSUPPORTED_TEST_OR_ACCEPTANCE_CLAIM')
    if state in ['NEEDS_INPUT_FREEZE', 'READY_WAITING_EXECUTION_REQUEST']:
        require(attempts == 0 and progress['outputs'] == [], 'EXECUTION_RECEIPT_CONFLICT')
    if state in ['AWAITING_HUMAN_REVIEW', 'AWAITING_INDEPENDENT_REVIEW']:
        require(attempts > 0, 'ACTUAL_TEST_REQUIRED')
    if state == 'TECHNICAL_BLOCKED':
        require(attempts > 0 and execution.get('errors'), 'OBSERVED_EXECUTION_ERROR_REQUIRED')
    if state == 'COMPLETED':
        require(stage_id == 'P7_DELIVERY', 'PREMATURE_MAINLINE_COMPLETION')
        delivery = _receipt(root, progress.get('delivery_receipt'))
        require(delivery.get('task_id') == progress['task_id'] and delivery.get('artifact_refs'),
                'DELIVERY_RECEIPT_REQUIRED')
        for ref in delivery['artifact_refs']:
            check_ref(root, ref)


def _validate_append_only_ledger(root, lock, cp, preserve):
    ledger = preserve['ledger_prefix']
    lines = evidence_bytes(path(root, ledger['path'])).splitlines(keepends=True)
    count = ledger['event_count']
    require(hashlib.sha256(b''.join(lines[:count])).hexdigest() == ledger['sha256'],
            'HISTORICAL_LEDGER_REWRITTEN')
    require(len(lines) > count, 'MAINLINE_LEDGER_EVENT_REQUIRED')
    previous = json.loads(lines[count - 1])
    for raw in lines[count:]:
        event = json.loads(raw)
        claimed = event.pop('event_hash')
        actual = hashlib.sha256(json.dumps(event, ensure_ascii=False, sort_keys=True,
            separators=(',', ':')).encode()).hexdigest()
        require(claimed == actual, 'LEDGER_HASH_MISMATCH')
        require(event['previous_event_id'] == previous['event_id'] and
                event['previous_event_hash'] == previous['event_hash'], 'LEDGER_PARENT_MISMATCH')
        previous = dict(event, event_hash=claimed)
    tail = {k: previous[k] for k in ['event_id', 'event_hash']}
    require(cp['ledger_tails']['commercial_design_pipeline'] == tail, 'LEDGER_TAIL_MISMATCH')
    require(previous['lock_sha256'] == digest(path(root, LOCK_PATH)), 'LEDGER_STALE_LOCK')


def validate_locked_request(root, request, lock):
    require(request.get('lock_sha256') == digest(path(root, LOCK_PATH)), 'REQUEST_STALE_LOCK')
    require(request.get('action') == lock['next_required_action'], 'ACTION_NOT_AUTHORIZED_OR_REPLAY')
    require(not any(request.get(k) for k in ['accepted', 'promoted', 'binding_pass',
                'output', 'export', 'changes']), 'EXECUTION_OR_TEST_EVIDENCE_REQUIRED')
    if request.get('render'):
        progress = lock['mainline_progress']
        require(lock['render_allowed'] and progress['status'] == 'AUTHORIZED', 'RENDER_NOT_AUTHORIZED')
        require(type(request.get('attempts')) is int and
                0 < request['attempts'] <= progress['execution_authorization']['images'],
                'REQUEST_BUDGET_EXCEEDED')
        require(request.get('frozen_inputs') ==
                (lock['mainline_lock']['contract'] if progress['task_id'] ==
                 'VPD-FULL-POSTER-STAGE1-CHAZUO-20261001-R1' else progress.get('input_freeze')),
                'RENDER_INPUT_FREEZE_REQUIRED')
    return lock
