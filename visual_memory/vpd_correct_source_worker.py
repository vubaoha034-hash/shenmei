"""Current work-unit checks inside the one existing VPD state authority.

The worker supplies evidence, never business state or authorization. This is
repository consistency, not an operating-system capability sandbox or taste oracle.
"""
from .vpd_task_lock import read, require, check_ref
import copy

SOURCE = '7fd7777fed21100cb6b47bc305701476054263565e73246ac469d065aa080618'
UNIT = 'CHAZUO_APPROVED_SOURCE_TYPOGRAPHY_20261003_R1'
TASK = 'VPD-CHAZUO-CODEX-COMPLETE-POSTER-20261003-01'
ENVELOPES = [[64,56,504,304],[800,72,1504,440]]
CONTINUOUS_TYPE_AREAS = [[64,56,504,304],[832,72,1504,624]]
HUMAN_BACKGROUND_TYPE_AREA = [300,380,1350,550]
# Root implementation of the authorized full poster refinement: text may
# intersect the product foreground, while the immutable photo layer is kept.
# This is a bounded production choice, not a coordinate instruction from Liu.
PRODUCT_INTERLEAVED_TYPE_AREA = [288,400,1328,720]
PRODUCT_CORE_MAP = {
    'path': 'evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/audit/FIXED_PRODUCT_CORE_MAP.json',
    'sha256': '6f17681f217db23c0ccbb2a30ac01878581d1ee867800169156cb66b60b3092f',
}
V28_LAYOUT_AMENDMENT = {
    'path': 'continuity/vpd/codex_takeover_20261003/COPY_LAYOUT_AUTHORIZATION_AMENDMENT_20261005.json',
    'sha256': '2f78640ae85343fc89c0835a75be7a78564ed9c5e94d679b35aa3326414f0738',
}
V28_AUTHORIZED_OVERLAY_ENVELOPES = [[285,198,490,298],[380,354,1349,663]]
V29_AUTHORIZED_OVERLAY_ENVELOPES = [[140,100,530,447]]

def version_input_contract(root, version, number):
    """Only29 may override copy/reference; historical unit fields remain intact."""
    require(type(number) is int and 1 <= number <= 29, 'INSPECTED_FORMAL_VERSION_REQUIRED')
    if number != 29:
        return None
    from .vpd_registered_type_composite import font_layout_kernel
    kernel = font_layout_kernel(root)
    require(type(version.get('number')) is int and version.get('number') == 29
            and version.get('input_contract') == kernel['ROOT_INPUT'],
            'V29_ROOT_FROZEN_INPUT_REQUIRED')
    contract = kernel['contract'](root)
    require(version.get('copy') == contract['copy'], 'V29_PROSPECTIVE_COPY_REQUIRED')
    return contract

def review_inputs_for_version(root, version, number, fallback):
    contract = version_input_contract(root, version, number)
    if contract is None:
        return fallback
    reference = version.get('review_inputs')
    require(isinstance(reference, dict) and reference.get('path') and reference.get('sha256'),
            'REQUIRED_ACTUAL_DATA:V29_REVIEW_INPUTS')
    new, old = load(root, reference), load(root, fallback)
    bindings = {item['neutral_id']: item['sha256'] for item in new['input_bindings']}
    prior = {item['neutral_id']: item['sha256'] for item in old['input_bindings']}
    require(set(bindings) == {'P','N','R','S'} and bindings == dict(prior, R=contract['reference']['sha256']),
            'V29_PROSPECTIVE_REVIEW_INPUTS_REQUIRED')
    return reference

def available_canvas_slots(unit):
    if unit['phase'] in ['REFERENCE_STUDY_ACTIVE', 'REFERENCE_STUDY_DELIVERED', 'REFERENCE_STUDY_ARCHIVE_BLOCKED']:
        return int(unit['phase'] == 'REFERENCE_STUDY_ACTIVE')
    if unit.get('repair_authorization'):
        return int(unit['phase'] in ['AUTHORIZED','REVISION_REQUIRED'])
    return unit['budget']['formal_versions_max'] - unit['budget']['formal_versions_used']

def load(root, ref):
    check_ref(root, ref)
    return read(root, ref['path'])

def validate_human_revision_requests(root, unit):
    """Bind each human resumption to one preserved AI-pass export."""
    refs = unit.get('human_revision_requests', [])
    require(isinstance(refs, list), 'HUMAN_REVISION_REQUEST_LIST_REQUIRED')
    requests = {}
    for ref in refs:
        request = load(root, ref)
        require(isinstance(request, dict) and unit['unit_id'] == UNIT
                and request.get('task_id') == TASK and request.get('unit_id') == UNIT
                and request.get('source_kind') == 'CURRENT_HUMAN_USER_MESSAGE'
                and isinstance(request.get('verbatim'), str) and request['verbatim'].strip()
                and request.get('scope') == 'SAME_DIRECTION_PRODUCT_TYPE_RELATIONSHIP_REFINEMENT'
                and all(request.get(k) is False for k in ['final_acceptance',
                    'photo_acceptance_retracted', 'mainline_change_authorized', 'old_budget_reset'])
                and isinstance(request.get('permitted_background_type_area'), list)
                and all(type(v) is int for v in request['permitted_background_type_area'])
                and request['permitted_background_type_area'] == HUMAN_BACKGROUND_TYPE_AREA,
                'ACTUAL_SCOPED_HUMAN_REVISION_REQUIRED')
        number = request.get('target_version')
        require(type(number) is int and 1 <= number <= len(unit['versions'])
                and number not in requests, 'HUMAN_REVISION_TARGET_VERSION_INVALID')
        version = unit['versions'][number-1]
        require(version['number'] == number and version.get('verdict') == 'AI_PASS'
                and request.get('target_export') == version['export'],
                'HUMAN_REVISION_TARGET_EXPORT_MISMATCH')
        requests[number] = request
    if unit.get('current_scoped_human_feedback'):
        require(bool(refs) and unit['current_scoped_human_feedback'] == refs[-1],
                'CURRENT_SCOPED_HUMAN_FEEDBACK_REFERENCE_CONFLICT')
    return requests

def has_scoped_human_revision_request(root, unit, number):
    return number in validate_human_revision_requests(root, unit)

def review_allows_revision(verdict, number, human_requests):
    return verdict == 'AI_FAIL' or (verdict == 'AI_PASS' and number in human_requests)

def validate_serial_transition(root, old_unit, unit):
    """Writer preflight; shared human evidence checks also run in the validator."""
    require(old_unit['unit_id'] == unit['unit_id'], 'WORKER_CANNOT_CHANGE_UNIT')
    old_used = old_unit['budget']['formal_versions_used']
    used = unit['budget']['formal_versions_used']
    require(type(used) is int and old_used <= used <= min(old_used+1, 29)
            and unit['budget']['revisions_used'] == max(0, used-1)
            and len(old_unit['versions']) == old_used and len(unit['versions']) == used,
            'CONTINUATION_BUDGET_ROLLBACK_OR_SKIP')
    completing_current_review = (used == old_used and old_used > 0
        and old_unit['phase'] == 'AWAITING_PIXEL_REVIEW'
        and old_unit['versions'][-1].get('verdict') == 'PENDING')
    preserved_count = old_used - 1 if completing_current_review else old_used
    require(unit['versions'][:preserved_count] == old_unit['versions'][:preserved_count],
            'HISTORICAL_VERSION_EVIDENCE_REWRITTEN')
    if completing_current_review:
        review_fields = {'verdict', 'pixel_review', 'drive_archive',
            'asset_drive_archive', 'professional_technical_review'}
        prior_version, current_version = old_unit['versions'][-1], unit['versions'][-1]
        require({k:v for k,v in prior_version.items() if k not in review_fields}
                == {k:v for k,v in current_version.items() if k not in review_fields}
                and current_version.get('verdict') in ['PENDING','AI_PASS','AI_FAIL']
                and all(current_version.get(k) == v for k,v in prior_version.items()
                    if k in review_fields and k != 'verdict'),
                'HISTORICAL_VERSION_EVIDENCE_REWRITTEN')
    old_refs = old_unit.get('human_revision_requests', [])
    new_refs = unit.get('human_revision_requests', [])
    require(isinstance(old_refs, list) and isinstance(new_refs, list)
            and new_refs[:len(old_refs)] == old_refs,
            'HISTORICAL_HUMAN_REVISION_REQUEST_REWRITTEN')
    requests = validate_human_revision_requests(root, unit)
    from .vpd_reference_typography_study import PHASES, validate_study
    if unit['phase'] in PHASES:
        require(used == old_used == 29 and old_unit['phase'] in
                ['DELIVERED_AI_PASS', 'REFERENCE_STUDY_ACTIVE', 'REFERENCE_STUDY_DELIVERED', 'REFERENCE_STUDY_ARCHIVE_BLOCKED'],
                'REFERENCE_STUDY_NOT_POSTER_RESUMPTION')
        validate_study(root, unit)
    elif old_unit['phase'] in PHASES:
        require(False, 'REFERENCE_STUDY_CANNOT_RESUME_POSTER_WITHOUT_NEW_AUTHORIZATION')
    active = unit['phase'] in ['AUTHORIZED','REVISION_REQUIRED','AWAITING_PIXEL_REVIEW']
    if old_used and used == old_used and active and old_unit['versions'][-1].get('verdict') == 'AI_PASS':
        require(unit['phase'] == 'REVISION_REQUIRED' and old_used in requests
                and unit['poster_human_verdict'] == 'PENDING', 'AI_PASS_STOPS_SERIAL_REPAIR')
    if used > old_used:
        require(old_unit['phase'] in ['AUTHORIZED','REVISION_REQUIRED'],
                'PRIOR_PIXEL_REVIEW_REQUIRED_BEFORE_NEXT_VERSION')
        if old_used:
            version = old_unit['versions'][-1]
            require(version.get('pixel_review'), 'PRIOR_PIXEL_REVIEW_REQUIRED_BEFORE_NEXT_VERSION')
            reviewed = load(root, version['pixel_review'])
            require(reviewed.get('task_id') == TASK and reviewed.get('work_unit_id') == UNIT
                    and reviewed.get('version') == old_used and reviewed.get('export') == version['export']
                    and reviewed.get('verdict') == version.get('verdict'),
                    'VERSION_REVIEW_VERDICT_CONFLICT')
            require(review_allows_revision(reviewed['verdict'], old_used, requests),
                    'AI_PASS_STOPS_SERIAL_REPAIR')
            if reviewed['verdict'] == 'AI_PASS':
                require(unit['poster_human_verdict'] == 'PENDING',
                        'HUMAN_REVISION_IS_NOT_POSTER_REJECTION')
    return requests

def validate_overlay_envelopes(number, envelopes, human_requests, v28_layout_authorized=False, v29_contract=None):
    # V13 splits the already authorized headline into two phrase blocks.
    # Keep each block bounded separately; permitted photography areas stay fixed.
    require(type(number) is int and 1 <= number <= 29, 'INSPECTED_FORMAL_VERSION_REQUIRED')
    if number == 29:
        require(v29_contract is not None and v29_contract['formal_version'] == 29
                and [v29_contract['typography_alpha_bbox']] == V29_AUTHORIZED_OVERLAY_ENVELOPES
                and envelopes == V29_AUTHORIZED_OVERLAY_ENVELOPES,
                'V29_REGISTERED_ENVELOPE_CHANGED')
        return
    limit = 3 if number >= 13 and any(target < number for target in human_requests) else 2
    require(isinstance(envelopes, list) and 1 <= len(envelopes) <= limit
            and all(isinstance(r, list) and len(r)==4 and all(type(v) is int for v in r)
                and 0<=r[0]<r[2]<=1536 and 0<=r[1]<r[3]<=1024 for r in envelopes),
            'DECLARED_OVERLAY_BOUNDS_REQUIRED')
    if type(number) is int and number == 28 and v28_layout_authorized is True:
        require(envelopes == V28_AUTHORIZED_OVERLAY_ENVELOPES,
                'V28_REGISTERED_ENVELOPE_CHANGED')
        return
    areas = CONTINUOUS_TYPE_AREAS
    if any(target < number for target in human_requests):
        areas = areas + [HUMAN_BACKGROUND_TYPE_AREA]
        if number >= 14:
            areas = areas + [PRODUCT_INTERLEAVED_TYPE_AREA]
    require(all(any(a[0]<=r[0]<r[2]<=a[2] and a[1]<=r[1]<r[3]<=a[3]
                    for a in areas) for r in envelopes),
            'PHOTOGRAPHY_PROTECTION_CANNOT_BE_ERASED_BY_ENVELOPE')

def validate_v28_layout_amendment(root, unit):
    reference = unit.get('copy_layout_authorization_amendment')
    if reference is None:
        return False
    require(reference == V28_LAYOUT_AMENDMENT, 'V28_EXACT_LAYOUT_AUTHORIZATION_REQUIRED')
    amendment = load(root, reference)
    scope = amendment['scope']; preservation = amendment['preservation']
    require(amendment['schema'] == 'vpd-scoped-human-typography-amendment/v1'
            and amendment['task_id'] == TASK and amendment['unit_id'] == UNIT
            and amendment['source']['kind'] == 'CURRENT_HUMAN_USER_MESSAGE'
            and amendment['source']['verbatim']
            and scope['copy_layout_change'] is True and scope['brand'] == '茶作'
            and scope['source_photography_sha256'] == SOURCE
            and scope['dimensions'] == [1536,1024]
            and scope['business_state_writer'] == 'ROOT_ONLY'
            and scope['independent_worker_may_change_mainline'] is False
            and preservation['historical_copy_and_versions_not_rewritten'] is True
            and preservation['v28_already_sealed_copy'] == '一杯茶，慢下来'
            and preservation['v28_already_sealed_files_not_changed'] is True,
            'V28_EXACT_LAYOUT_AUTHORIZATION_REQUIRED')
    return True

def validate_continuation(root, lock, cp, adapter, receipt):
    take = lock['codex_takeover']; unit = take['worker_continuation']
    require(unit == receipt.get('worker_continuation') and unit['unit_id'] == UNIT,
            'WORKER_UNIT_CHANGED')
    require(take['human_verdict'] == receipt['human_verdict'] == 'REJECTED' and
            take['budget']['formal_versions_used'] == 3 and take['budget']['revisions_used'] == 2,
            'OLD_FAILED_CYCLE_REWRITTEN')
    prior = load(root, unit['prior_failed_cycle_receipt'])
    require(prior['human_verdict'] == 'REJECTED' and prior['budget'] ==
            {'formal_versions_used':3,'revisions_used':2}, 'OLD_FAILED_CYCLE_REWRITTEN')
    authorization = load(root, unit['authorization'])
    continuous = bool(unit.get('repair_authorization'))
    if continuous:
        repair = load(root, unit['repair_authorization'])
        require(repair['task_id'] == TASK and repair['unit_id'] == UNIT
                and repair['source']['kind'] == 'CURRENT_HUMAN_USER_MESSAGE'
                and repair['source']['verbatim']
                and repair['scope'] == 'SAME_DIRECTION_SERIAL_TYPOGRAPHY_UNTIL_INDEPENDENT_AI_PASS'
                and repair['preserved_mainline'] == lock['mainline_lock']
                and repair['frozen_source_sha256'] == SOURCE
                and repair['brand'] == '茶作' and repair['copy'] == '一杯茶，慢下来'
                and repair['dimensions'] == [1536,1024]
                and repair['mainline_change'] is False and repair['photo_generation'] is False
                and repair['paid_compute'] is False and repair['training'] is False
                and repair['automations'] is False and repair['second_style'] is False
                and repair['old_budget_reset'] is False,
                'CONTINUOUS_REPAIR_EXPLICIT_AUTHORIZATION_REQUIRED')
    worker = load(root, unit['worker_contract'])
    require(authorization['task_id'] == TASK and authorization['unit_id'] == UNIT and
            authorization['source']['kind'] == 'CURRENT_HUMAN_USER_MESSAGE' and
            authorization['source']['verbatim'] and authorization['scope']['mainline_change'] is False
            and authorization['scope']['old_formal_budget_reset'] is False,
            'EXPLICIT_SAME_TASK_CONTINUATION_REQUIRED')
    require(worker['task_id'] == TASK and worker['roles']['business_state_writer'] == 'ROOT_ONLY'
            and worker['roles']['reviewer'] == 'FRESH_READ_ONLY_PIXEL_WORKER'
            and worker['worker_permissions'] == {
                'read_declared_review_images':True, 'write_business_state':False,
                'change_mainline':False, 'change_goal':False, 'change_reference':False,
                'change_copy_or_aspect':False, 'expand_budget':False,
                'generate_or_edit_artwork':False, 'give_human_acceptance':False}
            and worker['mainline_change_requires'] == 'EXPLICIT_HUMAN_USER_CONSENT'
            and lock['execution_boundary']['independent_worker_contract'] == unit['worker_contract'],
            'WORKER_AUTHORITY_EXPANSION')
    require(authorization['preserved_mainline'] == worker['preserved_mainline'] == lock['mainline_lock']
            and authorization['brand'] == unit['brand'] == '茶作'
            and authorization['copy'] == unit['copy'] == '一杯茶，慢下来'
            and unit['dimensions'] == [1536,1024], 'WORKER_MAINLINE_DRIFT')
    approval = load(root, unit['source_approval'])
    require(approval['source_kind'] == 'CURRENT_HUMAN_USER_MESSAGE' and approval['verbatim']
            and approval['target_sha256'] == SOURCE and approval['human_verdict'] == 'ACCEPTED'
            and approval['scope'] == 'LOCAL_BACKGROUND_RECONSTRUCTION_PHOTOGRAPHY_ONLY'
            and unit['frozen_source']['sha256'] == SOURCE,
            'SCOPED_HUMAN_APPROVAL_REQUIRED')
    require(unit['poster_human_verdict'] in ['PENDING','REJECTED'],
            'POSTER_HUMAN_VERDICT_UNSUPPORTED')
    if unit['poster_human_verdict'] == 'REJECTED':
        feedback = load(root, unit['poster_human_feedback'])
        require(unit['phase'] == 'HUMAN_REJECTED' or
                (continuous and unit['phase']=='REVISION_REQUIRED'),
                'POSTER_REJECTION_ACTION_CONFLICT')
        require(feedback['task_id'] == TASK and feedback['work_unit_id'] == UNIT
                and feedback['source_kind'] == 'CURRENT_HUMAN_USER_MESSAGE'
                and feedback['verbatim'] and feedback['human_verdict'] == 'REJECTED'
                and feedback['scope'] == 'CURRENT_COMPLETE_POSTER_TYPOGRAPHY_AND_DESIGN'
                and feedback['version'] == len(unit['versions']) == 3
                and feedback['target_export'] == unit['versions'][-1]['export']
                and feedback['photography_approval_retracted'] is False
                and feedback['budget_expansion_authorized'] is False
                and feedback['mainline_change_authorized'] is False
                and feedback['prior_blind_ai_review_unchanged'] is True
                and unit['human_review_request_withdrawn'] is True,
                'ACTUAL_SCOPED_POSTER_REJECTION_REQUIRED')
    else:
        require(unit['phase'] != 'HUMAN_REJECTED', 'POSTER_HUMAN_VERDICT_CONFLICT')
    recovery = take['source_recovery']
    require(recovery == receipt['source_recovery'] == lock['execution_boundary']['source_recovery_tool_trial']
            and recovery['phase'] == 'APPROVED_FROZEN' and recovery['human_verdict'] == 'ACCEPTED'
            and recovery['human_approval'] == unit['source_approval']
            and recovery['imagegen_edit_calls_used'] == 1
            and recovery['is_recovered_hidden_original'] is False, 'SOURCE_RECOVERY_SCOPE_CONFLICT')
    delivered = load(root, recovery['delivery_manifest'])
    require(delivered['output']['sha256'] == SOURCE and delivered['hidden_original_recovered'] is False,
            'APPROVED_SOURCE_IDENTITY_CHANGED')
    budget = unit['budget']; used = budget['formal_versions_used']
    require(type(used) is int and 0 <= used <= 29 and budget['revisions_used'] == max(0,used-1)
            and ((continuous and budget['formal_versions_max'] is None and
                  budget['revisions_max'] is None and budget['stop_condition']=='INDEPENDENT_AI_PASS')
                 or (not continuous and used<=3 and budget['formal_versions_max']==3
                     and budget['revisions_max']==2))
            and all(budget[k] == 0 for k in ['photo_generations','paid_compute_usd','training',
                'automations','second_style','parallel_alternatives','hidden_variants'])
            and authorization['operational_ceiling']['formal_versions_max'] == 3
            and authorization['operational_ceiling']['revisions_max'] == 2,
            'CONTINUATION_BUDGET_EXCEEDED')
    require(receipt['budget'] == {'formal_versions_used':3,'revisions_used':2}
            and receipt['task_id'] == TASK and receipt['status'] == take['status']
            and receipt['next_required_action'] == take['next_required_action'], 'CONTINUATION_RECEIPT_CONFLICT')
    require(receipt.get('artifact_refs'), 'CONTINUATION_ARTIFACT_REQUIRED')
    for ref in receipt['artifact_refs']: check_ref(root, ref)
    v28_layout_authorized = validate_v28_layout_amendment(root, unit)
    human_requests = validate_human_revision_requests(root, unit)
    actions = {'AUTHORIZED':'CREATE_CORRECT_SOURCE_CHAZUO_POSTER_VERSION_1',
        'AWAITING_PIXEL_REVIEW':'REVIEW_CORRECT_SOURCE_CHAZUO_POSTER_PIXELS',
        'REVISION_REQUIRED':'REVISE_CORRECT_SOURCE_CHAZUO_TYPOGRAPHY_FROM_WORKER_EVIDENCE',
        'DELIVERED_AI_PASS':'LIU_XIANSHENG_REVIEW_CORRECT_SOURCE_COMPLETE_POSTER',
        'DELIVERED_AI_FAIL':'LIU_XIANSHENG_REVIEW_CORRECT_SOURCE_POSTER_AND_FAILED_REVIEW',
        'HUMAN_REJECTED':'CONFIRM_ADDITIONAL_SAME_TASK_DESIGN_VERSION_SCOPE',
        'TECHNICAL_BLOCKED':'REPAIR_OBSERVED_CORRECT_SOURCE_TECHNICAL_BLOCKER'}
    from .vpd_reference_typography_study import PHASES, validate_study
    actions.update(REFERENCE_STUDY_ACTIVE='RECONSTRUCT_SHANYEJI_WHOLE_TYPOGRAPHY_IN_FIGMA',
                   REFERENCE_STUDY_DELIVERED='LIU_REVIEW_SHANYEJI_TYPOGRAPHY_REFERENCE_STUDY',
                   REFERENCE_STUDY_ARCHIVE_BLOCKED='AUTHORIZE_SHANYEJI_STUDY_DRIVE_DESTINATION')
    if unit['phase'] in PHASES:
        validate_study(root, unit)
    require(unit['phase'] in actions and take['next_required_action'] == actions[unit['phase']]
            and take['status'] == 'VPD_CODEX_CHAZUO_CORRECT_SOURCE_'+unit['phase'],
            'WORKER_CONTINUATION_ACTION_CONFLICT')
    if unit['phase'] in ['AUTHORIZED','TECHNICAL_BLOCKED']: return
    require(used > 0 and len(unit['versions']) == used, 'SERIAL_VERSION_EVIDENCE_REQUIRED')
    for number, version in enumerate(unit['versions'],1):
        require(version['number'] == number, 'SERIAL_VERSION_EVIDENCE_REQUIRED')
        input_contract = version_input_contract(root, version, number)
        technical = load(root, version['technical_check'])
        if input_contract is not None:
            require(technical.get('input_contract') == version['input_contract'], 'V29_TECHNICAL_INPUT_CONTRACT_REQUIRED')
        envelopes = ENVELOPES
        if number > 3:
            protection = load(root, version['photo_protection'])
            require(continuous and protection['source']['sha256'] == SOURCE
                    and protection['photo_regeneration_allowed'] is False
                    and protection['source_file_overwrite_allowed'] is False,
                    'SERIAL_PHOTO_PROTECTION_REQUIRED')
            envelopes = protection['visible_design_overlay_envelopes']
            validate_overlay_envelopes(number, envelopes, human_requests,
                                       v28_layout_authorized=v28_layout_authorized, v29_contract=input_contract)
        require(technical['frozen_source']['sha256'] == SOURCE and technical['dimensions'] == [1536,1024]
                and technical['export'] == version['export'] and technical['overlay_envelopes'] == envelopes
                and technical['protected_pixels_changed'] == 0
                and technical['protected_max_channel_difference'] == 0
                and technical['source_layer_unchanged'] is True,
                'ACCEPTED_PHOTOGRAPHY_CHANGED')
        if number >= 14:
            require(technical.get('product_foreground_core'), 'PRODUCT_CORE_CHECK_REQUIRED')
        if number >= 22:
            require(technical.get('formal_version') == number
                    and technical.get('protection_mode') == 'REGISTERED_TYPE_SOURCE_COMPOSITE_V1'
                    and technical.get('registered_type_composite')
                    and technical.get('registered_type_binding_audit')
                    and technical.get('registered_type_figma_binding'),
                    'V22_REGISTERED_TYPE_SOURCE_COMPOSITE_REQUIRED')
        else:
            require(not technical.get('protection_mode')
                    and not technical.get('registered_type_composite'),
                    'HISTORICAL_PHOTO_PROTECTION_MODE_CHANGED')
        compare_pixels(root,technical,envelopes)
        if number < used or unit['phase'] != 'AWAITING_PIXEL_REVIEW':
            require(version.get('pixel_review'), 'PRIOR_PIXEL_REVIEW_REQUIRED')
        if version.get('pixel_review'):
            reviewed = validate_review(root, version, number,
                review_inputs_for_version(root, version, number, unit['review_inputs']))
            require(version.get('verdict') == reviewed['verdict'], 'VERSION_REVIEW_VERDICT_CONFLICT')
            if number < used:
                require(review_allows_revision(reviewed['verdict'], number, human_requests),
                        'AI_PASS_STOPS_SERIAL_REPAIR')
    current = unit['versions'][-1]
    if unit['phase'] == 'AWAITING_PIXEL_REVIEW': return
    verdict = validate_review(root, current, used,
        review_inputs_for_version(root, current, used, unit['review_inputs']))['verdict']
    require((unit['phase']=='REVISION_REQUIRED' and (continuous or used<3)
             and review_allows_revision(verdict, used, human_requests))
            or (unit['phase']=='DELIVERED_AI_FAIL' and verdict=='AI_FAIL')
            or (unit['phase']=='HUMAN_REJECTED' and verdict=='AI_FAIL' and used==3)
            or (unit['phase']=='DELIVERED_AI_PASS' and verdict=='AI_PASS')
            or (unit['phase'] in PHASES and verdict=='AI_PASS'), 'WORKER_VERDICT_ACTION_CONFLICT')
    if unit['phase'].startswith('DELIVERED_') or unit['phase']=='HUMAN_REJECTED':
        archive=load(root,current['drive_archive'])
        require(archive['readback_result']=='PASS' and archive['poster_sha256']==current['export']['sha256']
                and archive['raw_bytes_equal_local'] is True, 'DRIVE_RAW_READBACK_REQUIRED')

def compare_pixels(root,technical,envelopes=ENVELOPES):
    if technical.get('protection_mode') == 'REGISTERED_TYPE_SOURCE_COMPOSITE_V1':
        require(type(technical.get('formal_version')) is int
                and 22 <= technical['formal_version'] <= 29, 'PROSPECTIVE_V22_REQUIRED')
        from .vpd_registered_type_composite import compare_pixels as compare_composite, replay
        from PIL import Image, ImageChops
        report = load(root, technical['registered_type_composite'])
        require(technical.get('registered_type_figma_binding'),
                'ACTUAL_FIGMA_RUNTIME_BOUND_REPORT_REQUIRED')
        from .vpd_registered_type_figma_binding import verify_actual_binding
        figma_report = load(root, technical['registered_type_figma_binding'])
        actual_figma = verify_actual_binding(root, report['registration'],
                                            figma_report['runtime_evidence'],
                                            figma_report['download_readback'])
        require(actual_figma == figma_report
                and actual_figma['formal_version'] == technical['formal_version']
                and actual_figma['source'] == technical['frozen_source']
                and actual_figma['raw_figma_export'] == technical['raw_figma_export'],
                'ACTUAL_FIGMA_REGISTERED_TYPE_BINDING_CONFLICT')
        binding = load(root, technical['registered_type_binding_audit'])
        require(binding.get('result') == 'TECHNICAL_PASS_WITH_LIMITATIONS'
                and binding.get('version') == technical['formal_version']
                and binding.get('registered_type_composite_check') == technical['registered_type_composite']
                and binding.get('registered_type_figma_binding') == technical['registered_type_figma_binding']
                and binding.get('actual_figma_registered_vectors_verified') is True
                and binding.get('actual_original_photo_verified') is True,
                'ACTUAL_FIGMA_REGISTERED_TYPE_AUDIT_REQUIRED')
        actual = compare_composite(root, report['registration'], technical['export'],
                                   technical['raw_figma_export'])
        require(actual == report and actual['formal_version'] == technical['formal_version']
                and actual['source'] == technical['frozen_source'],
                'REGISTERED_TYPE_COMPOSITE_REPORT_CONFLICT')
        _, overlay, registration = replay(root, report['registration'])
        if technical['formal_version'] == 29:
            require(technical.get('input_contract') == registration['input_contract'], 'V29_REGISTERED_INPUT_CONTRACT_CONFLICT')
        outside = Image.new('L', (1536,1024), 255)
        for x0,y0,x1,y1 in envelopes:
            outside.paste(0, (x0,y0,x1,y1))
        require(ImageChops.darker(overlay.getchannel('A'), outside).getbbox() is None
                and sum(outside.histogram()[1:]) == technical['protected_pixels_compared'],
                'REGISTERED_TYPE_OUTSIDE_DECLARED_BOUNDS')
        # Core report stays mandatory and hash-bound. Full-frame recomposition
        # includes all 162052 core pixels; it does not omit text-covered pixels.
        core_report = load(root, technical['product_foreground_core'])
        require(core_report.get('protection_mode') == technical['protection_mode']
                and core_report.get('registration') == report['registration']
                and core_report.get('source_sha256') == SOURCE
                and core_report.get('final_png_sha256') == technical['export']['sha256']
                and core_report.get('product_core_pixels_compared') == 162052
                and core_report.get('product_core_expected_composite_differences_final') == 0,
                'REGISTERED_PRODUCT_CORE_IDENTITY_CONFLICT')
        return
    from .vpd_locked_mainline_state import _png_rgb_rows
    source=technical['frozen_source']; export=technical['export']
    check_ref(root,source); check_ref(root,export)
    core_rows = {}
    if technical.get('product_foreground_core'):
        report = load(root, technical['product_foreground_core'])
        core = load(root, PRODUCT_CORE_MAP)
        check_ref(root, core['mask_asset'])
        require(core['source_sha256'] == source['sha256'] == SOURCE
                and core['dimensions'] == [1536,1024] and core['pixels'] == 162052
                and report['mask_asset_sha256'] == core['mask_asset']['sha256']
                and report['final_png_sha256'] == export['sha256']
                and report['source_sha256'] == SOURCE
                and report['product_core_pixels_compared'] == core['pixels']
                and report['product_core_rgb_differences_final'] == 0,
                'PRODUCT_CORE_IDENTITY_CONFLICT')
        core_rows = dict(core['rows'])
    changed=0; compared=0; maximum=0
    core_changed=0; core_compared=0
    for y,(a,b) in enumerate(zip(_png_rgb_rows(root,source),_png_rgb_rows(root,export))):
        omitted=sorted((x0,x1) for x0,y0,x1,y1 in envelopes if y0<=y<y1)
        start=0; intervals=[]
        for x0,x1 in omitted:
            if start < x0: intervals.append((start,x0))
            start=max(start,x1)
        intervals.append((start,1536))
        for x0,x1 in intervals:
            aa,bb=a[x0*3:x1*3],b[x0*3:x1*3]; compared+=x1-x0
            if aa!=bb:
                changed+=sum(aa[p:p+3]!=bb[p:p+3] for p in range(0,len(aa),3))
                maximum=max(maximum,max(abs(x-z) for x,z in zip(aa,bb)))
        for x0,x1 in core_rows.get(y, []):
            aa,bb=a[x0*3:x1*3],b[x0*3:x1*3]
            core_compared+=x1-x0
            core_changed+=sum(aa[p:p+3]!=bb[p:p+3] for p in range(0,len(aa),3))
    require(changed==0 and maximum==0 and compared==technical['protected_pixels_compared'],
            'APPROVED_PHOTO_ACTUAL_PIXELS_CHANGED')
    if core_rows:
        require(core_changed == 0 and core_compared == 162052,
                'APPROVED_PRODUCT_CORE_ACTUAL_PIXELS_CHANGED')

def validate_review(root, version, number, expected_inputs):
    contract = version_input_contract(root, version, number)
    if contract is not None:
        require(expected_inputs == version.get('review_inputs'), 'V29_PROSPECTIVE_REVIEW_INPUTS_REQUIRED')
    review=load(root,version['pixel_review']); ids=['P','N','R','S','T']
    require(review['task_id']==TASK and review['work_unit_id']==UNIT and review['version']==number
            and review['human_verdict']=='HIDDEN_PENDING' and review['personal_fit'] is None
            and review['verdict'] in ['AI_PASS','AI_FAIL'] and review['pixels_seen']==ids
            and review['export']==version['export'] and len(review['observations'])>=5
            and all(o.get('region') and o.get('evidence') for o in review['observations']),
            'ACTUAL_WORKER_PIXEL_REVIEW_REQUIRED')
    audit=load(root,review['isolation_audit']); evidence=load(root,audit['evidence'])
    raw=load(root,evidence['raw_tool_read_audit']); spawn=load(root,evidence['spawn_receipt'])
    bindings={b['neutral_id']:b['sha256'] for b in review['input_bindings']}
    inputs=load(root,expected_inputs)
    expected={b['neutral_id']:b['sha256'] for b in inputs['input_bindings']}
    reference_sha = (contract['reference']['sha256'] if contract is not None else
                     '87a28f5cd4b5d15b01e6536206127c357043a904b3c0dab3bfa0c50080782167')
    require(bindings==dict(expected,T=version['export']['sha256']) and expected['S']==SOURCE
            and expected['R']==reference_sha,
            'WORKER_REFERENCE_BINDING_CHANGED')
    carrier=audit['carrier']; fork=('NOT_APPLICABLE_NEW_THREAD' if carrier=='FRESH_PROJECTLESS_CODEX_WORKER' else 'none')
    require(audit['verified'] is True and audit['fork_turns']==fork and audit['history_inherited'] is False
            and audit['source_project_context_read'] is False and audit['fresh_agent'] is True
            and audit['completed'] is True and audit['tool_scope_violations']==[]
            and audit['attachments_verified']==ids and audit['actual_model']=='gpt-6.1-sol'
            and audit['actual_reasoning_effort']=='max' and len(bindings)==5
            and bindings['T']==version['export']['sha256']
            and evidence['turn_context']=={'model':'gpt-6.1-sol','reasoning_effort':'max'}
            and len(evidence['tool_reads'])==5
            and {r['neutral_id']:r['sha256'] for r in evidence['tool_reads']}==bindings
            and all(r['tool']=='view_image' for r in evidence['tool_reads'])
            and raw['tool_reads']==evidence['tool_reads'] and raw['extra_tool_reads']==[]
            and raw['source_project_context_reads']==[]
            and raw['actual_image_view_markers']==5 and len(raw['tool_calls'])>0
            and all(c['name']=='exec' and c['called_tools'] and set(c['called_tools'])=={'view_image'}
                    for c in raw['tool_calls'])
            and carrier in ['FRESH_FORK_NONE_PIXEL_AGENT','FRESH_PROJECTLESS_CODEX_WORKER']
            and spawn['thread_id']==evidence['thread_id']==raw['thread_id']
            and spawn['fork_turns']==fork and spawn['history_inherited'] is False
            and spawn['actual_model']=='gpt-6.1-sol' and spawn['actual_reasoning_effort']=='max'
            and spawn['root_spawn_call_ids']
            and spawn['initial_prompt_sha256']==audit['initial_prompt_sha256']==evidence['initial_prompt_sha256'],
            'WORKER_EXECUTION_OR_ISOLATION_UNVERIFIED')
    amendment=load(root,audit['carrier_amendment']); load(root,evidence['reviewer_output'])
    require(amendment['scope']=='CURRENT_CORRECT_SOURCE_FORMAL_WORKER_REVIEW'
            and amendment['work_unit_id']==UNIT and amendment['attachments_required']==ids,
            'WORKER_CARRIER_AMENDMENT_REQUIRED')
    if carrier=='FRESH_PROJECTLESS_CODEX_WORKER':
        creation=spawn.get('projectless_creation')
        require(creation and creation['new_thread'] is True and creation['creator_history_inherited'] is False
                and creation['target']['type']=='projectless' and creation['thread_id']==spawn['thread_id']
                and creation['actual_returned_thread_id']==spawn['thread_id']
                and creation['actual_creation_result_sha256']
                and creation['root_creation_call_ids']==spawn['root_spawn_call_ids'],
                'WORKER_CREATION_EVIDENCE_REQUIRED')
    return review
