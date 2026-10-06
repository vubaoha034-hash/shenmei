"""Scoped reference study inside the existing task; never a poster release gate."""
from .vpd_task_lock import require, check_ref, read

REFERENCE = '9a29fbdc7dd908017924bed270e8dfe18351519eed3fa7bc7001789f2a383414'
PHASES = {'REFERENCE_STUDY_ACTIVE', 'REFERENCE_STUDY_DELIVERED', 'REFERENCE_STUDY_ARCHIVE_BLOCKED'}
TRANSFER_AUTH = 'evidence/vpd/codex_takeover_20261003/liuxiansheng_content_transfer_20261005/HUMAN_SCOPE_AUTHORIZATION.json'
FINAL_ALLOCATION_AUTH = 'evidence/vpd/codex_takeover_20261003/liuxiansheng_content_transfer_20261005/FINAL_REPAIR_ALLOCATION_AUTHORIZATION.json'
SUPPLEMENTAL_ALLOCATION_AUTH = 'evidence/vpd/codex_takeover_20261003/liuxiansheng_content_transfer_20261005/CONTINUOUS_METHOD_REPAIR_ALLOCATION.json'
CONTINUOUS_AUTH = {'path':'continuity/vpd/codex_takeover_20261003/CONTINUOUS_REPAIR_AUTHORIZATION_20261004.json', 'sha256':'73a521078dbea5b6b819bc4b8640d42e268d5621dbecbb9af2949b6a1aabe848'}
TRANSFER_SCOPE = 'SHANYEJI_REFERENCE_TYPOGRAPHY_CONTENT_TRANSFER_EXPERIMENT'
HUMAN_FEEDBACK_AUTH = 'evidence/vpd/codex_takeover_20261003/liuxiansheng_content_transfer_20261005/HUMAN_S4_FEEDBACK_20261006.json'
HUMAN_LOCAL_ALLOCATION_AUTH = 'evidence/vpd/codex_takeover_20261003/liuxiansheng_content_transfer_20261005/HUMAN_S4_LOCAL_REPAIR_ALLOCATION_20261006.json'
HUMAN_LOCAL_FOLLOWUP_ALLOCATION_AUTH = 'evidence/vpd/codex_takeover_20261003/liuxiansheng_content_transfer_20261005/CONTINUOUS_S5_FAILED_METHOD_REPAIR_ALLOCATION_20261006.json'
S5_FAILED_REVIEW = 'evidence/vpd/codex_takeover_20261003/liuxiansheng_content_transfer_20261005/s5_verified_review/PIXEL_REVIEW.json'
REFERENCE_GRAIN_ALLOCATION_AUTH = 'evidence/vpd/codex_takeover_20261003/liuxiansheng_content_transfer_20261005/CONTINUOUS_S6_FAILED_REFERENCE_METHOD_ALLOCATION_20261006.json'
S6_FAILED_REVIEW = 'evidence/vpd/codex_takeover_20261003/liuxiansheng_content_transfer_20261005/s6_verified_review/PIXEL_REVIEW.json'
S5_REVIEW_PARENT_THREAD_ID = '01a0ffab-c9b7-7c40-b55b-e51535c156dd'
HUMAN_LOCAL_SCOPE = 'S4_OUTLINE_AND_XIAN_CONTINUITY_ONLY'
HUMAN_LOCAL_LITERAL = '有些不对的。但是整体好了很多很多。一  边缘很像是刀切了一样。二  先字还被断了一下。而后。我现在希望这个做成一个插件，并在chatgpt里面持续改善。流程就按现在这种。明白我的额意思吗。'
S4_EXPORT_SHA = 'ddb621ebf7e230279a1358b1b93ab9fcd55705b7e6ca99af8649aa3295ab1ca4'
S4_GUIDE_SHA = '9ef09dd1814343a938445227ce9a8906f0eb1ae4531a857baaba0720606aa558'
PROTECTED_PHOTO_SHA = '7fd7777fed21100cb6b47bc305701476054263565e73246ac469d065aa080618'
HUMAN_LOCAL_LIMITS = dict.fromkeys(['image_guide_calls', 'new_tea_versions', 'mainline_changes',
    'second_styles', 'photo_changes', 'photo_generations', 'paid_compute', 'model_training',
    'automations', 'budget_resets'], 0)
TRANSFER_ACTIONS = {
    'REFERENCE_STUDY_ACTIVE': 'EXECUTE_LIUXIANSHENG_CONTENT_TRANSFER',
    'REFERENCE_STUDY_DELIVERED': 'LIU_REVIEW_LIUXIANSHENG_CONTENT_TRANSFER',
    'REFERENCE_STUDY_ARCHIVE_BLOCKED': 'REPAIR_LIUXIANSHENG_CONTENT_TRANSFER_ARCHIVE',
}


def study_actions(unit):
    if 'content_transfer_experiment' in unit:
        require(unit['phase'] in PHASES, 'CONTENT_TRANSFER_NOT_POSTER_RESUMPTION')
        return TRANSFER_ACTIONS
    return {
        'REFERENCE_STUDY_ACTIVE': 'RECONSTRUCT_SHANYEJI_WHOLE_TYPOGRAPHY_IN_FIGMA',
        'REFERENCE_STUDY_DELIVERED': 'LIU_REVIEW_SHANYEJI_TYPOGRAPHY_REFERENCE_STUDY',
        'REFERENCE_STUDY_ARCHIVE_BLOCKED': 'AUTHORIZE_SHANYEJI_STUDY_DRIVE_DESTINATION',
    }


def validate_transfer_transition(old, new):
    require(isinstance(new, dict), 'CONTENT_TRANSFER_CANNOT_BE_REMOVED')
    if old is None:
        return
    require(all(new.get(k) == old.get(k) for k in ['authorization', 'copy_manifest', 'human_acceptance'])
            and new.get('attempts', [])[:len(old.get('attempts', []))] == old.get('attempts', [])
            and new.get('artifacts', [])[:len(old.get('artifacts', []))] == old.get('artifacts', []),
            'CONTENT_TRANSFER_HISTORY_REWRITTEN')
    if 'final_repair_allocation' in old:
        require(new.get('final_repair_allocation') == old['final_repair_allocation'],
                'CONTENT_TRANSFER_FINAL_ALLOCATION_REWRITTEN')
    if 'supplemental_repair_allocation' in old:
        require(new.get('supplemental_repair_allocation') == old['supplemental_repair_allocation'],
                'CONTENT_TRANSFER_SUPPLEMENTAL_ALLOCATION_REWRITTEN')
    if 'human_local_repair_allocation' in old:
        require(new.get('human_local_repair_allocation') == old['human_local_repair_allocation'],
                'CONTENT_TRANSFER_HUMAN_LOCAL_ALLOCATION_REWRITTEN')
    if 'human_local_followup_allocation' in old:
        require(new.get('human_local_followup_allocation') == old['human_local_followup_allocation'],
                'CONTENT_TRANSFER_HUMAN_LOCAL_FOLLOWUP_ALLOCATION_REWRITTEN')
    if 'reference_grain_method_allocation' in old:
        require(new.get('reference_grain_method_allocation') == old['reference_grain_method_allocation'],
                'CONTENT_TRANSFER_REFERENCE_METHOD_ALLOCATION_REWRITTEN')
    for field in ['image_guide', 'supplemental_image_guide']:
        if field not in old:
            continue
        prior, guide = old[field], new.get(field)
        require(isinstance(guide, dict) and guide.get('authorization') == prior.get('authorization')
                and type(guide.get('calls_used')) is int
                and prior['calls_used'] <= guide['calls_used'] <= 1
                and all(guide.get(k) == prior[k] for k in ['export', 'error'] if k in prior),
                'CONTENT_TRANSFER_GUIDE_HISTORY_REWRITTEN')
        if prior['calls_used'] == 1:
            require(all(guide.get(k) == prior.get(k) for k in ['phase', 'export', 'error']),
                    'CONTENT_TRANSFER_GUIDE_TERMINAL_STATE_REWRITTEN')


def _load(root, ref):
    check_ref(root, ref)
    return read(root, ref['path'])


def _final_allocation(transfer, root):
    if 'final_repair_allocation' not in transfer:
        return None
    require(root is not None, 'CONTENT_TRANSFER_FINAL_ALLOCATION_ROOT_REQUIRED')
    ref = transfer['final_repair_allocation']
    grant = _load(root, ref)
    require(ref['path'] == FINAL_ALLOCATION_AUTH
            and grant['schema_version'] == 'vpd-content-transfer-final-repair-allocation/v1'
            and grant['scope'] == TRANSFER_SCOPE
            and grant['task_id'] == 'VPD-CHAZUO-CODEX-COMPLETE-POSTER-20261003-01'
            and grant['work_unit_id'] == 'CHAZUO_APPROVED_SOURCE_TYPOGRAPHY_20261003_R1'
            and grant['authorization'] == transfer['authorization']
            and grant['copy_manifest'] == transfer['copy_manifest']
            and grant['attempt_budget'] == {'primary_max':1, 'targeted_repairs_max':2, 'total_max':3}
            and all(type(v) is int for v in grant['attempt_budget'].values())
            and grant['real_current_task_actor'] == 'ROOT_ONLY'
            and grant['human_acceptance'] == 'PENDING'
            and all(grant[k] is False for k in ['new_tea_version', 'mainline_change', 'second_style',
                'photo_change', 'paid_compute', 'model_training', 'automation', 'budget_reset']),
            'CONTENT_TRANSFER_FINAL_ALLOCATION_SCOPE_CONFLICT')
    if 'guide_generation' in grant:
        require(grant['guide_generation'] == {'tool':'image_gen.imagegen', 'max_calls':1,
                    'typography_only':True, 'transparent_background':True, 'photo_generation':False}
                and type(grant['guide_generation']['max_calls']) is int
                and bool(grant['user_method_literal']) and grant['reference_sha256'] == REFERENCE,
                'CONTENT_TRANSFER_GUIDE_AUTHORIZATION_CONFLICT')
    return grant


def transfer_attempt_limit(transfer, root=None):
    grant = _final_allocation(transfer, root)
    if _reference_grain_method_allocation(transfer, root):
        return 7
    if _human_local_followup_allocation(transfer, root):
        return 6
    if _human_local_allocation(transfer, root):
        return 5
    if _supplemental_allocation(transfer, root):
        return 4
    return grant['attempt_budget']['total_max'] if grant else 2


def _supplemental_allocation(transfer, root):
    if 'supplemental_repair_allocation' not in transfer:
        return None
    grant = _load(root, transfer['supplemental_repair_allocation'])
    base = _final_allocation(transfer, root)
    continuous = _load(root, grant['continuous_repair_authorization'])
    require(transfer['supplemental_repair_allocation']['path'] == SUPPLEMENTAL_ALLOCATION_AUTH
            and grant['schema_version'] == 'vpd-content-transfer-continuous-method-repair-allocation/v1'
            and grant['scope'] == TRANSFER_SCOPE
            and grant['task_id'] == continuous['task_id'] == 'VPD-CHAZUO-CODEX-COMPLETE-POSTER-20261003-01'
            and grant['work_unit_id'] == continuous['unit_id'] == 'CHAZUO_APPROVED_SOURCE_TYPOGRAPHY_20261003_R1'
            and grant['authorization'] == transfer['authorization']
            and grant['copy_manifest'] == transfer['copy_manifest']
            and grant['final_repair_allocation'] == transfer['final_repair_allocation']
            and grant['continuous_repair_authorization'] == CONTINUOUS_AUTH
            and continuous['scope'] == 'SAME_DIRECTION_SERIAL_TYPOGRAPHY_UNTIL_INDEPENDENT_AI_PASS'
            and continuous['stop_condition'] == 'INDEPENDENT_AI_PASS_THEN_HUMAN_REVIEW'
            and grant['reference_sha256'] == REFERENCE
            and grant['attempt_budget'] == {'base_attempts':3, 'total_max':4}
            and all(type(v) is int for v in grant['attempt_budget'].values())
            and grant['guide_generation'] == {'tool':'image_gen.imagegen', 'base_guide_calls':1,
                'max_calls':1, 'guide_total_max':2, 'typography_only':True,
                'transparent_background':True, 'photo_generation':False}
            and all(type(grant['guide_generation'][k]) is int for k in ['base_guide_calls','max_calls','guide_total_max'])
            and base is not None and 'guide_generation' in base
            and len(transfer.get('attempts', [])) >= 3
            and transfer.get('image_guide', {}).get('calls_used') == 1
            and grant['real_current_task_actor'] == 'ROOT_ONLY' and grant['human_acceptance'] == 'PENDING'
            and all(grant[k] is False for k in ['new_tea_version', 'mainline_change', 'second_style',
                'photo_change', 'paid_compute', 'model_training', 'automation', 'budget_reset']),
            'CONTENT_TRANSFER_SUPPLEMENTAL_ALLOCATION_SCOPE_CONFLICT')
    return grant


def _human_feedback(root, ref, prior_export):
    basis = _load(root, ref)
    require(ref['path'] == HUMAN_FEEDBACK_AUTH
            and basis.get('schema_version') == 'vpd-content-transfer-human-local-feedback/v1'
            and basis.get('source_kind') == 'CURRENT_HUMAN_USER_MESSAGE'
            and basis.get('task_id') == 'VPD-CHAZUO-CODEX-COMPLETE-POSTER-20261003-01'
            and basis.get('work_unit_id') == 'CHAZUO_APPROVED_SOURCE_TYPOGRAPHY_20261003_R1'
            and basis.get('user_literal') == HUMAN_LOCAL_LITERAL
            and basis.get('scope') == HUMAN_LOCAL_SCOPE
            and basis.get('target_export') == prior_export
            and prior_export.get('sha256') == S4_EXPORT_SHA
            and basis.get('verdict') == 'LOCAL_REPAIR_REQUESTED'
            and basis.get('human_acceptance') == 'PENDING'
            and all(basis.get(k) is False for k in ['final_acceptance', 'mainline_change',
                'second_style', 'photo_change', 'photo_generation', 'guide_generation']),
            'CONTENT_TRANSFER_CURRENT_HUMAN_LOCAL_FEEDBACK_REQUIRED')
    return basis


def _human_local_allocation(transfer, root):
    if 'human_local_repair_allocation' not in transfer:
        return None
    ref = transfer['human_local_repair_allocation']
    grant = _load(root, ref)
    supplemental = _supplemental_allocation(transfer, root)
    attempts = transfer.get('attempts', [])
    require(ref['path'] == HUMAN_LOCAL_ALLOCATION_AUTH
            and grant.get('schema_version') == 'vpd-content-transfer-human-local-repair-allocation/v1'
            and grant.get('scope') == TRANSFER_SCOPE
            and grant.get('task_id') == 'VPD-CHAZUO-CODEX-COMPLETE-POSTER-20261003-01'
            and grant.get('work_unit_id') == 'CHAZUO_APPROVED_SOURCE_TYPOGRAPHY_20261003_R1'
            and grant.get('authorization') == transfer['authorization']
            and grant.get('copy_manifest') == transfer['copy_manifest']
            and grant.get('continuous_repair_authorization') == CONTINUOUS_AUTH
            and supplemental is not None and len(attempts) >= 4
            and grant.get('target_export') == attempts[3]['export']
            and attempts[3]['export'].get('sha256') == S4_EXPORT_SHA
            and grant.get('protected_photo_sha256') == PROTECTED_PHOTO_SHA
            and grant.get('image_guide') == transfer.get('supplemental_image_guide', {}).get('export')
            and grant.get('image_guide', {}).get('sha256') == S4_GUIDE_SHA
            and grant.get('attempt_budget') == {'base_attempts':4, 'total_max':5, 'local_repairs_max':1}
            and all(type(v) is int for v in grant['attempt_budget'].values())
            and grant.get('limits') == HUMAN_LOCAL_LIMITS
            and all(type(v) is int for v in grant['limits'].values())
            and grant.get('real_current_task_actor') == 'ROOT_ONLY'
            and grant.get('human_acceptance') == transfer.get('human_acceptance') == 'PENDING',
            'CONTENT_TRANSFER_HUMAN_LOCAL_ALLOCATION_SCOPE_CONFLICT')
    _human_feedback(root, grant['feedback'], attempts[3]['export'])
    guide = _image_guide(transfer, root)
    require(guide['calls_used'] == 1 and guide['phase'] == 'GENERATED',
            'CONTENT_TRANSFER_HUMAN_LOCAL_GUIDE_FROZEN')
    return grant


def _human_local_followup_allocation(transfer, root):
    """One Root allocation after S5 FAIL; the continuous human grant remains live."""
    if 'human_local_followup_allocation' not in transfer:
        return None
    ref = transfer['human_local_followup_allocation']
    grant = _load(root, ref)
    base = _human_local_allocation(transfer, root)
    attempts = transfer.get('attempts', [])
    require(ref['path'] == HUMAN_LOCAL_FOLLOWUP_ALLOCATION_AUTH
            and grant.get('schema_version') == 'vpd-content-transfer-failed-local-method-followup/v1'
            and grant.get('scope') == TRANSFER_SCOPE
            and grant.get('task_id') == 'VPD-CHAZUO-CODEX-COMPLETE-POSTER-20261003-01'
            and grant.get('work_unit_id') == 'CHAZUO_APPROVED_SOURCE_TYPOGRAPHY_20261003_R1'
            and grant.get('authorization') == transfer['authorization']
            and grant.get('copy_manifest') == transfer['copy_manifest']
            and grant.get('continuous_repair_authorization') == CONTINUOUS_AUTH
            and base is not None and len(attempts) >= 5
            and grant.get('base_allocation') == transfer['human_local_repair_allocation']
            and grant.get('human_feedback') == base['feedback']
            and grant.get('prior_failed_export') == attempts[4]['export']
            and isinstance(grant.get('prior_failed_review'), dict)
            and grant['prior_failed_review'].get('path') == S5_FAILED_REVIEW
            and grant.get('protected_photo_sha256') == PROTECTED_PHOTO_SHA
            and grant.get('image_guide') == base['image_guide']
            and grant.get('attempt_budget') == {'base_attempts':5, 'total_max':6, 'method_repairs_max':1}
            and all(type(v) is int for v in grant['attempt_budget'].values())
            and grant.get('limits') == HUMAN_LOCAL_LIMITS
            and all(type(v) is int for v in grant['limits'].values())
            and grant.get('real_current_task_actor') == 'ROOT_ONLY'
            and grant.get('human_acceptance') == transfer.get('human_acceptance') == 'PENDING'
            and grant.get('allocation_is_not_human_stop_condition') is True
            and isinstance(grant.get('method_change_reason'), str)
            and bool(grant['method_change_reason'].strip()),
            'CONTENT_TRANSFER_HUMAN_LOCAL_FOLLOWUP_SCOPE_CONFLICT')
    _validate_failed_local_followup_review(root, grant['prior_failed_review'], attempts[4]['export'])
    return grant


def _reference_grain_method_allocation(transfer, root):
    """One S7 repair of the actual failed S6, under the existing continuous grant."""
    if 'reference_grain_method_allocation' not in transfer:
        return None
    ref = transfer['reference_grain_method_allocation']
    grant = _load(root, ref)
    base = _human_local_followup_allocation(transfer, root)
    attempts = transfer.get('attempts', [])
    require(ref['path'] == REFERENCE_GRAIN_ALLOCATION_AUTH
            and grant.get('schema_version') == 'vpd-content-transfer-failed-reference-method-followup/v1'
            and grant.get('scope') == TRANSFER_SCOPE
            and grant.get('task_id') == 'VPD-CHAZUO-CODEX-COMPLETE-POSTER-20261003-01'
            and grant.get('work_unit_id') == 'CHAZUO_APPROVED_SOURCE_TYPOGRAPHY_20261003_R1'
            and grant.get('authorization') == transfer['authorization']
            and grant.get('copy_manifest') == transfer['copy_manifest']
            and grant.get('continuous_repair_authorization') == CONTINUOUS_AUTH
            and base is not None and len(attempts) >= 6
            and grant.get('parent_allocation') == transfer['human_local_followup_allocation']
            and grant.get('prior_failed_export') == attempts[5]['export']
            and isinstance(grant.get('prior_failed_review'), dict)
            and grant['prior_failed_review'].get('path') == S6_FAILED_REVIEW
            and grant.get('protected_photo_sha256') == PROTECTED_PHOTO_SHA
            and grant.get('image_guide') == base['image_guide']
            and grant.get('attempt_budget') == {'base_attempts':6, 'total_max':7, 'method_repairs_max':1}
            and all(type(v) is int for v in grant['attempt_budget'].values())
            and grant.get('limits') == HUMAN_LOCAL_LIMITS
            and all(type(v) is int for v in grant['limits'].values())
            and grant.get('real_current_task_actor') == 'ROOT_ONLY'
            and grant.get('human_acceptance') == transfer.get('human_acceptance') == 'PENDING'
            and grant.get('allocation_is_not_human_stop_condition') is True
            and isinstance(grant.get('method_change_reason'), str)
            and bool(grant['method_change_reason'].strip())
            and isinstance(grant.get('expert_spec_refs'), list) and bool(grant['expert_spec_refs']),
            'CONTENT_TRANSFER_REFERENCE_METHOD_SCOPE_CONFLICT')
    for spec_ref in grant['expert_spec_refs']:
        check_ref(root, spec_ref)
    _validate_failed_local_followup_review(root, grant['prior_failed_review'], attempts[5]['export'],
                                         expected_agent_path='/root/s6_fresh_cold_pixel_review')
    return grant


def _validate_failed_local_followup_review(root, ref, prior_export,
                                         expected_agent_path='/root/s5_fresh_cold_pixel_review'):
    require(expected_agent_path in ['/root/s5_fresh_cold_pixel_review', '/root/s6_fresh_cold_pixel_review'],
            'CONTENT_TRANSFER_FAILED_LOCAL_REVIEW_CARRIER_REQUIRED')
    _validate_repair_basis(root, ref, prior_export)
    basis = _load(root, ref)
    audit = _load(root, basis.get('isolation_audit'))
    calls = audit.get('actual_tool_calls', [])
    reads = audit.get('actual_image_reads', [])
    spawns = audit.get('actual_parent_spawn', [])
    child = audit.get('actual_child_spawn_source', {})
    require(audit.get('schema') == 'vpd-study-review-runtime-audit/v1'
            and audit.get('scope') == TRANSFER_SCOPE
            and audit.get('verified') is True and audit.get('history_inherited') is False
            and audit.get('fork_turns') == 'none' and audit.get('pixels_seen') == 2
            and audit.get('actual_model') == 'gpt-6.1-sol'
            and audit.get('actual_reasoning_effort') == 'max'
            and audit.get('reference_sha256') == REFERENCE
            and audit.get('study_export_sha256') == prior_export['sha256']
            and bool(basis.get('reviewer_thread_id'))
            and audit.get('reviewer_thread_id') == basis['reviewer_thread_id']
            and audit.get('tool_scope_violations') == []
            and isinstance(reads, list) and len(reads) == 2
            and all(isinstance(item, dict) for item in reads)
            and {item.get('sha256') for item in reads} == {REFERENCE, prior_export['sha256']}
            and isinstance(calls, list) and len(calls) == 2
            and all(isinstance(call, dict) and call.get('name') == 'exec'
                    and isinstance(call.get('call_id'), str) and bool(call['call_id'])
                    and isinstance(call.get('input_sha256'), str) and len(call['input_sha256']) == 64
                    and all(c in '0123456789abcdef' for c in call['input_sha256']) for call in calls)
            and len({call['call_id'] for call in calls}) == 2
            and audit.get('parent_spawn_verified') is True
            and isinstance(spawns, list) and len(spawns) == 1
            and isinstance(spawns[0], dict) and bool(spawns[0].get('call_id'))
            and spawns[0].get('fork_turns') == 'none'
            and spawns[0].get('model') == 'gpt-6.1-sol'
            and spawns[0].get('reasoning_effort') == 'max'
            and isinstance(child, dict) and child.get('parent_thread_id') == S5_REVIEW_PARENT_THREAD_ID
            and child['parent_thread_id'] != basis['reviewer_thread_id']
            and child.get('depth') == 1
            and child.get('agent_path') == expected_agent_path,
            'CONTENT_TRANSFER_FAILED_LOCAL_REVIEW_ISOLATION_REQUIRED')
    manifest = _load(root, audit.get('reviewed_call_manifest'))
    require(manifest.get('schema') == 'vpd-root-inspected-review-call-manifest/v1'
            and manifest.get('scope') == TRANSFER_SCOPE
            and manifest.get('root_read_actual_call_bodies') is True
            and manifest.get('reference_sha256') == REFERENCE
            and manifest.get('study_export_sha256') == prior_export['sha256']
            and manifest.get('reviewer_thread_id') == basis['reviewer_thread_id']
            and isinstance(manifest.get('calls'), list)
            and [{k:call.get(k) for k in ['name','call_id','input_sha256']}
                 for call in manifest['calls']] == calls,
            'CONTENT_TRANSFER_FAILED_LOCAL_REVIEW_CALL_BINDING_REQUIRED')


def _guide_state(root, guide, authorization):
    require(isinstance(guide, dict) and guide['authorization'] == authorization
            and type(guide['calls_used']) is int and guide['calls_used'] in [0,1],
            'CONTENT_TRANSFER_GUIDE_STATE_CONFLICT')
    if guide['calls_used'] == 0:
        require(guide['phase'] == 'AUTHORIZED' and not guide.get('export') and not guide.get('error'),
                'CONTENT_TRANSFER_GUIDE_STATE_CONFLICT')
    elif guide['phase'] == 'GENERATED':
        require(not guide.get('error'), 'CONTENT_TRANSFER_GUIDE_STATE_CONFLICT')
        check_ref(root, guide['export'])
        from PIL import Image
        with Image.open(root / guide['export']['path']) as actual:
            alpha_min, alpha_max = actual.convert('RGBA').getchannel('A').getextrema()
            require(actual.format == 'PNG' and alpha_min < 255 and alpha_max > 0,
                    'CONTENT_TRANSFER_TRANSPARENT_GUIDE_PNG_REQUIRED')
    else:
        require(guide['phase'] == 'FAILED' and not guide.get('export'), 'CONTENT_TRANSFER_GUIDE_STATE_CONFLICT')
        check_ref(root, guide['error'])
    return guide


def _image_guide(transfer, root):
    grant = _final_allocation(transfer, root)
    if not grant or 'guide_generation' not in grant:
        require(transfer.get('image_guide') is None and transfer.get('supplemental_image_guide') is None
                and 'supplemental_repair_allocation' not in transfer,
                'CONTENT_TRANSFER_GUIDE_AUTHORIZATION_REQUIRED')
        return None
    guide = _guide_state(root, transfer.get('image_guide'), transfer['final_repair_allocation'])
    supplemental = _supplemental_allocation(transfer, root)
    if supplemental:
        return _guide_state(root, transfer.get('supplemental_image_guide'), transfer['supplemental_repair_allocation'])
    require(transfer.get('supplemental_image_guide') is None, 'CONTENT_TRANSFER_GUIDE_AUTHORIZATION_REQUIRED')
    return guide


def available_guide_calls(unit, root):
    if 'content_transfer_experiment' not in unit:
        return 0
    guide = _image_guide(unit['content_transfer_experiment'], root)
    return 1 - guide['calls_used'] if guide else 0


def transfer_attempts(transfer, root=None):
    attempts = transfer.get('attempts', [])
    require(isinstance(attempts, list) and len(attempts) <= transfer_attempt_limit(transfer, root)
            and all(isinstance(attempt, dict)
                    and attempt.get('kind') == ('PRIMARY' if i == 0 else 'TARGETED_REPAIR')
                    for i, attempt in enumerate(attempts)),
            'CONTENT_TRANSFER_ATTEMPT_BUDGET_EXCEEDED')
    return attempts


def _validate_repair_basis(root, ref, prior_export):
    basis = _load(root, ref)
    require(basis.get('schema') == 'vpd-reference-typography-pixel-review/v1'
            and basis.get('scope') == TRANSFER_SCOPE and basis.get('actual_pixels_seen') is True
            and basis.get('reference_sha256') == REFERENCE
            and basis.get('study_export_sha256') == prior_export['sha256']
            and basis.get('verdict') == 'CONTENT_TRANSFER_FAIL'
            and basis.get('human_acceptance') == 'PENDING'
            and basis.get('evidence_class') != 'SYNTHETIC_NOT_RUNTIME_EVIDENCE',
            'CONTENT_TRANSFER_ACTUAL_REPAIR_BASIS_REQUIRED')


def validate_transfer_write(root, transfer, request):
    attempts = transfer_attempts(transfer, root)
    count = len(attempts)
    require(count < transfer_attempt_limit(transfer, root), 'CONTENT_TRANSFER_ATTEMPT_BUDGET_EXHAUSTED')
    require(type(request.get('attempt_count')) is int and request['attempt_count'] == count,
            'CONTENT_TRANSFER_ATTEMPT_STATE_MISMATCH')
    require(request.get('intent') == ('PRIMARY' if count == 0 else 'TARGETED_REPAIR'),
            'CONTENT_TRANSFER_WRITE_INTENT_CONFLICT')
    if count == 0:
        require('repair_basis' not in request, 'CONTENT_TRANSFER_PRIMARY_CANNOT_BE_REPAIR')
    else:
        require(isinstance(request.get('repair_basis'), dict),
                'CONTENT_TRANSFER_ACTUAL_REPAIR_BASIS_REQUIRED')
        if count == 4:
            local = _human_local_allocation(transfer, root)
            require(local is not None and request['repair_basis'] == local['feedback'],
                    'CONTENT_TRANSFER_CURRENT_HUMAN_LOCAL_FEEDBACK_REQUIRED')
            _human_feedback(root, request['repair_basis'], attempts[-1]['export'])
            require(request.get('figma_write') is True
                    and request.get('protected_photo_sha256') == PROTECTED_PHOTO_SHA
                    and not any(request.get(k) for k in ['wordmark_image_tool', 'typography_guide',
                        'render', 'photo_generation', 'photo_change', 'guide_generation',
                        'paid_compute_usd', 'paid_compute', 'training', 'model_training',
                        'automations', 'automation', 'second_style', 'hidden_variants',
                        'new_tea_version', 'new_tea_poster', 'tea_verdict', 'final_acceptance',
                        'budget_reset', 'mainline_change'])
                    and 'formal_version' not in request,
                    'CONTENT_TRANSFER_HUMAN_LOCAL_WRITE_SCOPE_CONFLICT')
        elif count in [5, 6]:
            followup = (_human_local_followup_allocation(transfer, root) if count == 5
                        else _reference_grain_method_allocation(transfer, root))
            require(followup is not None and request['repair_basis'] == followup['prior_failed_review'],
                    'CONTENT_TRANSFER_FAILED_LOCAL_REVIEW_REQUIRED')
            if count == 6:
                require(request.get('method_authorization') == transfer['reference_grain_method_allocation'],
                        'CONTENT_TRANSFER_REFERENCE_METHOD_AUTHORIZATION_REQUIRED')
            require(request.get('figma_write') is True
                    and request.get('actor') == 'ROOT_EXECUTOR'
                    and request.get('task_id') == followup['task_id']
                    and request.get('work_unit_id') == followup['work_unit_id']
                    and request.get('authorization') == transfer['authorization']
                    and request.get('copy_manifest') == transfer['copy_manifest']
                    and request.get('protected_photo_sha256') == PROTECTED_PHOTO_SHA
                    and not any(request.get(k) for k in HUMAN_LOCAL_LIMITS)
                    and not any(request.get(k) for k in ['wordmark_image_tool', 'typography_guide',
                        'render', 'photo_generation', 'photo_change', 'guide_generation',
                        'paid_compute_usd', 'paid_compute', 'training', 'model_training',
                        'automations', 'automation', 'second_style', 'hidden_variants',
                        'new_tea_version', 'new_tea_poster', 'tea_verdict', 'final_acceptance',
                        'budget_reset', 'mainline_change'])
                    and 'formal_version' not in request,
                    'CONTENT_TRANSFER_FAILED_LOCAL_WRITE_SCOPE_CONFLICT')
        else:
            _validate_repair_basis(root, request['repair_basis'], attempts[-1]['export'])
    grant = _final_allocation(transfer, root)
    if request.get('figma_write') and ((count == 2 and grant and 'guide_generation' in grant)
                                     or count == 3):
        guide = _image_guide(transfer, root)
        require(guide['calls_used'] == 1 and guide['phase'] == 'GENERATED',
                'CONTENT_TRANSFER_GUIDE_REQUIRED_BEFORE_FINAL_FIGMA')


def validate_typography_guide_write(root, unit, transfer, request):
    guide = _image_guide(transfer, root)
    supplemental = 'supplemental_repair_allocation' in transfer
    require(guide is not None and guide['calls_used'] == 0 and guide['phase'] == 'AUTHORIZED'
            and request.get('wordmark_image_tool') is True and request.get('figma_write') is False
            and request.get('typography_guide') is True and request.get('transparent_background') is True
            and request.get('authorization') == transfer['authorization']
            and request.get('method_authorization') == transfer['supplemental_repair_allocation' if supplemental else 'final_repair_allocation']
            and request.get('copy_manifest') == transfer['copy_manifest']
            and request.get('reference_sha256') == REFERENCE
            and request.get('task_id') == 'VPD-CHAZUO-CODEX-COMPLETE-POSTER-20261003-01'
            and request.get('study_only') is True and request.get('intent') == 'TARGETED_REPAIR'
            and request.get('attempt_count') == (3 if supplemental else 2)
            and request.get('protected_poster_node') == '402:2'
            and request.get('protected_photo_sha256') == unit['frozen_source']['sha256']
            and not any(request.get(k) for k in ['render', 'photo_generation', 'photo_change',
                'paid_compute_usd', 'paid_compute', 'training', 'model_training', 'automations',
                'automation', 'second_style', 'hidden_variants', 'node_id', 'node_ids',
                'new_tea_version', 'tea_verdict', 'final_acceptance'])
            and 'formal_version' not in request,
            'CONTENT_TRANSFER_GUIDE_WRITE_SCOPE_CONFLICT')
    inputs = request.get('input_refs')
    require(isinstance(inputs, list) and len(inputs) == 1 and inputs[0].get('sha256') == REFERENCE,
            'CONTENT_TRANSFER_GUIDE_REFERENCE_ONLY')
    check_ref(root, inputs[0])
    validate_transfer_write(root, transfer, request)


def _copy_texts(manifest):
    copy = manifest.get('copy')
    require(isinstance(copy, dict) and copy.get('main_wordmark') == '刘先生',
            'CONTENT_TRANSFER_FULL_COPY_REQUIRED')
    texts = []
    for key, value in copy.items():
        values = value if isinstance(value, list) else [value]
        require(bool(values) and all(isinstance(text, str) and text.strip() for text in values),
                'CONTENT_TRANSFER_FULL_COPY_REQUIRED')
        require(not any(old in text for text in values for old in ['山野集', '茶作']),
                'CONTENT_TRANSFER_OLD_COPY_FORBIDDEN')
        if key != 'main_wordmark':
            texts.extend(values)
    require(all(anchor in '\n'.join(texts) for anchor in ['疯疯癫癫', '山人不住山']),
            'CONTENT_TRANSFER_COPY_ANCHORS_REQUIRED')
    return texts


def _validate_transfer(root, unit):
    transfer = unit['content_transfer_experiment']
    require(isinstance(transfer, dict) and unit['phase'] in PHASES,
            'CONTENT_TRANSFER_REQUIRED')
    auth = _load(root, transfer['authorization'])
    manifest = _load(root, transfer['copy_manifest'])
    baseline = _load(root, unit['reference_typography_study']['delivery'])
    require(transfer['authorization']['path'] == TRANSFER_AUTH
            and auth['schema_version'] == 'vpd-human-reference-typography-content-transfer/v1'
            and auth['scope'] == TRANSFER_SCOPE
            and auth['task_id'] == 'VPD-CHAZUO-CODEX-COMPLETE-POSTER-20261003-01'
            and auth['work_unit_id'] == unit['unit_id'] and bool(auth['user_literal'])
            and auth['reference']['sha256'] == REFERENCE
            and auth['reference']['dimensions'] == [960,1280]
            and auth['target_v29_export_sha256'] == unit['versions'][28]['export']['sha256']
            and auth['baseline_s2_export_sha256'] == baseline['export']['sha256']
            and auth['copy_manifest'] == transfer['copy_manifest']
            and auth['brand'] == manifest['brand'] == '刘先生'
            and manifest['schema_version'] == 'vpd-typography-transfer-copy/v1'
            and auth['required_copy_anchors'] == manifest['required_copy_anchors'] == ['疯疯癫癫', '山人不住山']
            and manifest['dimensions'] == [960,1280]
            and auth['attempt_budget'] == {'primary_max':1, 'targeted_repairs_max':1}
            and auth['human_acceptance'] == transfer['human_acceptance'] == 'PENDING'
            and all(auth[k] is False for k in ['mainline_change', 'photo_change',
                'retract_prior_human_feedback', 'new_tea_version', 'budget_reset',
                'paid_compute', 'model_training', 'automation', 'second_style'])
            and unit['budget']['formal_versions_used'] == 29
            and unit['budget']['revisions_used'] == 28 and len(unit['versions']) == 29,
            'CONTENT_TRANSFER_SCOPE_CONFLICT')
    page = auth['allowed_figma_page']
    require(page['file_key'] == 'uyDxOoN1iNDPpEHTKSUWg1'
            and page['page_id'] not in ['', '402:2', '402:3', '416:2']
            and isinstance(page['page_name'], str) and page['page_name'],
            'CONTENT_TRANSFER_PAGE_REQUIRED')
    texts = _copy_texts(manifest)
    for ref in transfer.get('artifacts', []):
        check_ref(root, ref)
    attempts = transfer_attempts(transfer, root)
    for index, attempt in enumerate(attempts):
        check_ref(root, attempt['export'])
        if attempt['kind'] == 'TARGETED_REPAIR':
            if index == 4:
                local = _human_local_allocation(transfer, root)
                require(local is not None and attempt['repair_basis'] == local['feedback'],
                        'CONTENT_TRANSFER_CURRENT_HUMAN_LOCAL_FEEDBACK_REQUIRED')
                _human_feedback(root, attempt['repair_basis'], attempts[index-1]['export'])
            elif index == 5:
                followup = _human_local_followup_allocation(transfer, root)
                require(followup is not None and attempt['repair_basis'] == followup['prior_failed_review'],
                        'CONTENT_TRANSFER_FAILED_LOCAL_REVIEW_REQUIRED')
                _validate_failed_local_followup_review(root, attempt['repair_basis'], attempts[index-1]['export'])
            else:
                _validate_repair_basis(root, attempt['repair_basis'], attempts[index-1]['export'])
    guide = _image_guide(transfer, root)
    if len(attempts) >= 3 and guide is not None:
        prior_guide = transfer['image_guide'] if len(attempts) == 3 else guide
        require(prior_guide['calls_used'] == 1 and prior_guide['phase'] == 'GENERATED',
                'CONTENT_TRANSFER_GUIDE_REQUIRED_BEFORE_FINAL_FIGMA')
    if unit['phase'] == 'REFERENCE_STUDY_ACTIVE':
        return transfer
    require(bool(attempts) and transfer.get('delivery') and transfer.get('review'),
            'CONTENT_TRANSFER_DELIVERY_EVIDENCE_REQUIRED')
    delivery = _load(root, transfer['delivery'])
    review = _load(root, transfer['review'])
    check_ref(root, delivery['export'])
    figma = _load(root, delivery['figma_readback'])
    audit = _load(root, review['isolation_audit'])
    from PIL import Image
    with Image.open(root / delivery['export']['path']) as actual:
        require(actual.format == 'PNG' and actual.size == (960,1280), 'CONTENT_TRANSFER_ACTUAL_PNG_REQUIRED')
    mode = delivery['rendering_mode']
    require(mode in ['ORIGINAL_VECTOR_WORDMARK_AND_NATIVE_EDITABLE_TEXT',
                     'IMAGE_GUIDE_VECTOR_RECONSTRUCTION_AND_NATIVE_EDITABLE_TEXT'],
            'CONTENT_TRANSFER_RENDERING_MODE_CONFLICT')
    if len(attempts) >= 3 and guide is not None:
        require(mode == 'IMAGE_GUIDE_VECTOR_RECONSTRUCTION_AND_NATIVE_EDITABLE_TEXT',
                'CONTENT_TRANSFER_FINAL_GUIDE_RENDERING_MODE_REQUIRED')
    if mode == 'IMAGE_GUIDE_VECTOR_RECONSTRUCTION_AND_NATIVE_EDITABLE_TEXT':
        require(guide is not None and guide['phase'] == 'GENERATED' and guide['calls_used'] == 1
                and delivery.get('image_guide') == guide['export']
                and figma.get('reconstruction_source_sha256') == guide['export']['sha256'],
                'CONTENT_TRANSFER_GUIDE_RECONSTRUCTION_BINDING_CONFLICT')
    require(attempts[-1]['export'] == delivery['export']
            and delivery['scope'] == review['scope'] == audit['scope'] == TRANSFER_SCOPE
            and delivery['reference_sha256'] == review['reference_sha256'] == audit['reference_sha256'] == REFERENCE
            and delivery['copy_manifest'] == figma['copy_manifest'] == transfer['copy_manifest']
            and delivery['new_tea_version'] is False and delivery['human_acceptance'] == 'PENDING'
            and delivery['figma']['file_key'] == figma['file_key'] == page['file_key']
            and delivery['figma']['page_id'] == figma['page_id'] == page['page_id']
            and figma['page_name'] == page['page_name']
            and delivery['figma']['node_id'] == figma['study_frame_id']
            and figma['study_frame_id'] not in ['', '402:2', '402:3', '416:2']
            and figma['frame_name'].startswith('LIUXIANSHENG_CONTENT_TRANSFER')
            and figma['wordmark_vector_count'] > 0 and figma['vector_count'] > 0
            and figma['all_wordmark_curves_custom'] is True
            and figma['text_count'] > 0 and sorted(figma['candidate_texts']) == sorted(texts)
            and figma['type_frame_image_paints'] == 0
            and figma['protected_v29_unchanged'] is True and figma['protected_s2_unchanged'] is True
            and figma['export_sha256'] == review['study_export_sha256'] == audit['study_export_sha256'] == delivery['export']['sha256']
            and review['actual_pixels_seen'] is True and review['human_acceptance'] == 'PENDING'
            and not any(k in review for k in ['tea_verdict', 'final_acceptance', 'formal_version'])
            and review['verdict'] in ['CONTENT_TRANSFER_PASS_WITH_LIMITATIONS', 'CONTENT_TRANSFER_FAIL']
            and audit['verified'] is True and audit['history_inherited'] is False
            and audit['fork_turns'] == 'none' and audit['pixels_seen'] == 2
            and audit['actual_model'] == 'gpt-6.1-sol' and audit['actual_reasoning_effort'] == 'max'
            and audit['reviewer_thread_id'] == review['reviewer_thread_id']
            and audit['reviewer_thread_id'] != _load(root, unit['reference_typography_study']['review'])['reviewer_thread_id']
            and audit['tool_scope_violations'] == []
            and len(audit['actual_image_reads']) == 2
            and {item['sha256'] for item in audit['actual_image_reads']} == {REFERENCE, delivery['export']['sha256']},
            'CONTENT_TRANSFER_REVIEW_BINDING_CONFLICT')
    if unit['phase'] == 'REFERENCE_STUDY_DELIVERED':
        drive = _load(root, delivery['drive_readback'])
        check_ref(root, drive['restored_file'])
        require(drive['file_id'] == delivery['drive']['file_id']
                and drive['restored_file']['sha256'] == delivery['export']['sha256']
                and drive['raw_bytes_equal_local'] is True, 'CONTENT_TRANSFER_DRIVE_BYTES_REQUIRED')
    else:
        blocker = _load(root, delivery['drive']['blocker'])
        require(delivery['drive']['status'] in ['BLOCKED_AUTO_REVIEW', 'TECHNICAL_BLOCKED']
                and delivery['drive']['file_id'] is None and blocker['no_bypass'] is True
                and (bool(blocker.get('actual_error')) or
                     type(blocker.get('actual_rejections')) is int and blocker['actual_rejections'] > 0),
                'CONTENT_TRANSFER_ACTUAL_ARCHIVE_BLOCKER_REQUIRED')
    return transfer


def validate_study(root, unit):
    if 'content_transfer_experiment' in unit:
        # The completed reconstruction stays independently verifiable while the
        # sibling transfer uses the same native phase and formal Tea counters.
        _validate_reconstruction(root, dict(unit, phase='REFERENCE_STUDY_DELIVERED'))
        return _validate_transfer(root, unit)
    return _validate_reconstruction(root, unit)


def _validate_reconstruction(root, unit):
    study = unit.get('reference_typography_study')
    require(isinstance(study, dict), 'REFERENCE_STUDY_REQUIRED')
    check_ref(root, study['authorization'])
    auth = read(root, study['authorization']['path'])
    require(auth['schema'] == 'vpd-human-reference-typography-study/v1'
            and auth['source_kind'] == 'CURRENT_HUMAN_USER_MESSAGE'
            and bool(auth['verbatim'])
            and auth['task_id'] == 'VPD-CHAZUO-CODEX-COMPLETE-POSTER-20261003-01'
            and auth['unit_id'] == unit['unit_id']
            and auth['reference']['sha256'] == REFERENCE
            and auth['reference']['dimensions'] == [960, 1280]
            and auth['scope'] == 'SHANYEJI_WHOLE_TYPOGRAPHY_REFERENCE_RECONSTRUCTION_ONLY'
            and auth['target_version'] == 29
            and auth['target_export'] == unit['versions'][28]['export']
            and auth['typography_human_verdict'] == 'REJECTED'
            and all(auth[k] is False for k in ['mainline_change', 'photo_change',
                'photo_approval_retracted', 'new_tea_poster', 'budget_reset',
                'paid_compute', 'training', 'automations', 'second_style'])
            and unit['budget']['formal_versions_used'] == 29
            and len(unit['versions']) == 29
            and unit['versions'][28]['verdict'] == 'AI_PASS'
            and unit['poster_human_verdict'] == 'PENDING'
            and study['typography_human_verdict'] == 'REJECTED'
            and study['human_acceptance'] == 'PENDING', 'REFERENCE_STUDY_SCOPE_CONFLICT')
    for ref in study.get('artifacts', []):
        check_ref(root, ref)
    if unit['phase'] != 'REFERENCE_STUDY_ACTIVE':
        require(bool(study.get('delivery')) and bool(study.get('review')),
                'REFERENCE_STUDY_DELIVERY_EVIDENCE_REQUIRED')
        for key in ['delivery', 'review']:
            check_ref(root, study[key])
        delivery = read(root, study['delivery']['path'])
        review = read(root, study['review']['path'])
        check_ref(root, delivery['export'])
        check_ref(root, delivery['figma_readback'])
        figma = read(root, delivery['figma_readback']['path'])
        if unit['phase'] == 'REFERENCE_STUDY_DELIVERED':
            check_ref(root, delivery['drive_readback'])
            drive = read(root, delivery['drive_readback']['path'])
            check_ref(root, drive['restored_file'])
            require(drive['file_id'] == delivery['drive']['file_id']
                    and drive['restored_file']['sha256'] == delivery['export']['sha256']
                    and drive['raw_bytes_equal_local'] is True,
                    'REFERENCE_STUDY_DRIVE_BYTES_REQUIRED')
        else:
            check_ref(root, delivery['drive']['blocker'])
            blocker = read(root, delivery['drive']['blocker']['path'])
            require(delivery['drive']['status'] == 'BLOCKED_AUTO_REVIEW'
                    and delivery['drive']['file_id'] is None
                    and blocker['actual_rejections'] == 2
                    and blocker['explicit_destination_approval'] == 'PENDING'
                    and blocker['no_bypass'] is True,
                    'REFERENCE_STUDY_ACTUAL_ARCHIVE_BLOCKER_REQUIRED')
        check_ref(root, review['isolation_audit'])
        audit = read(root, review['isolation_audit']['path'])
        from PIL import Image
        with Image.open(root / delivery['export']['path']) as actual:
            require(actual.format == 'PNG' and actual.size == (960,1280),
                    'REFERENCE_STUDY_ACTUAL_PNG_REQUIRED')
        require(delivery['reference_sha256'] == REFERENCE
                and delivery['scope'] == auth['scope']
                and delivery['new_tea_poster'] is False
                and delivery['figma']['file_key'] == 'uyDxOoN1iNDPpEHTKSUWg1'
                and delivery['figma']['node_id'] not in ['', '402:2', '402:3']
                and figma['file_key'] == delivery['figma']['file_key']
                and figma['study_frame_id'] == delivery['figma']['node_id']
                and figma['page_name'] == 'SHANYEJI Whole Typography Study 20261005'
                and figma['vector_count'] > 0
                and ((delivery['rendering_mode'] == 'EDITABLE_VECTOR_CONTOURS'
                      and figma['type_frame_image_paints'] == 0)
                     or (delivery['rendering_mode'] == 'EDITABLE_VECTORS_WITH_EXPLICIT_APPROXIMATE_RASTER_INK'
                         and figma['type_frame_image_paints'] == 1))
                and figma['protected_v29_unchanged'] is True
                and delivery['exact_original_font_recovered'] is False
                and delivery['original_alpha_recovered'] is False
                and review['scope'] == auth['scope']
                and 'tea_verdict' not in review and 'final_acceptance' not in review
                and review['actual_pixels_seen'] is True
                and audit['verified'] is True and audit['history_inherited'] is False
                and audit['fork_turns'] == 'none' and audit['pixels_seen'] >= 2
                and audit['scope'] == auth['scope']
                and audit['reference_sha256'] == REFERENCE
                and audit['study_export_sha256'] == delivery['export']['sha256']
                and audit['reviewer_thread_id'] == review['reviewer_thread_id']
                and audit['tool_scope_violations'] == []
                and figma['export_sha256'] == delivery['export']['sha256']
                and audit['actual_model'] and audit['actual_reasoning_effort']
                and review['reference_sha256'] == REFERENCE
                and review['study_export_sha256'] == delivery['export']['sha256']
                and review['human_acceptance'] == 'PENDING'
                and review['verdict'] in ['REFERENCE_FIDELITY_PASS_WITH_LIMITATIONS',
                    'REFERENCE_FIDELITY_FAIL'], 'REFERENCE_STUDY_REVIEW_BINDING_CONFLICT')
    return study
