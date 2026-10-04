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

def available_canvas_slots(unit):
    if unit.get('repair_authorization'):
        return int(unit['phase'] in ['AUTHORIZED','REVISION_REQUIRED'])
    return unit['budget']['formal_versions_max'] - unit['budget']['formal_versions_used']

def load(root, ref):
    check_ref(root, ref)
    return read(root, ref['path'])

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
    require(type(used) is int and used >= 0 and budget['revisions_used'] == max(0,used-1)
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
    actions = {'AUTHORIZED':'CREATE_CORRECT_SOURCE_CHAZUO_POSTER_VERSION_1',
        'AWAITING_PIXEL_REVIEW':'REVIEW_CORRECT_SOURCE_CHAZUO_POSTER_PIXELS',
        'REVISION_REQUIRED':'REVISE_CORRECT_SOURCE_CHAZUO_TYPOGRAPHY_FROM_WORKER_EVIDENCE',
        'DELIVERED_AI_PASS':'LIU_XIANSHENG_REVIEW_CORRECT_SOURCE_COMPLETE_POSTER',
        'DELIVERED_AI_FAIL':'LIU_XIANSHENG_REVIEW_CORRECT_SOURCE_POSTER_AND_FAILED_REVIEW',
        'HUMAN_REJECTED':'CONFIRM_ADDITIONAL_SAME_TASK_DESIGN_VERSION_SCOPE',
        'TECHNICAL_BLOCKED':'REPAIR_OBSERVED_CORRECT_SOURCE_TECHNICAL_BLOCKER'}
    require(unit['phase'] in actions and take['next_required_action'] == actions[unit['phase']]
            and take['status'] == 'VPD_CODEX_CHAZUO_CORRECT_SOURCE_'+unit['phase'],
            'WORKER_CONTINUATION_ACTION_CONFLICT')
    if unit['phase'] in ['AUTHORIZED','TECHNICAL_BLOCKED']: return
    require(used > 0 and len(unit['versions']) == used, 'SERIAL_VERSION_EVIDENCE_REQUIRED')
    for number, version in enumerate(unit['versions'],1):
        require(version['number'] == number, 'SERIAL_VERSION_EVIDENCE_REQUIRED')
        technical = load(root, version['technical_check'])
        envelopes = ENVELOPES
        if number > 3:
            protection = load(root, version['photo_protection'])
            require(continuous and protection['source']['sha256'] == SOURCE
                    and protection['photo_regeneration_allowed'] is False
                    and protection['source_file_overwrite_allowed'] is False,
                    'SERIAL_PHOTO_PROTECTION_REQUIRED')
            envelopes = protection['visible_design_overlay_envelopes']
            require(1<=len(envelopes)<=2 and all(len(r)==4 and all(type(v) is int for v in r)
                    and 0<=r[0]<r[2]<=1536 and 0<=r[1]<r[3]<=1024 for r in envelopes),
                    'DECLARED_OVERLAY_BOUNDS_REQUIRED')
            require(all(any(a[0]<=r[0]<r[2]<=a[2] and a[1]<=r[1]<r[3]<=a[3]
                            for a in CONTINUOUS_TYPE_AREAS) for r in envelopes),
                    'PHOTOGRAPHY_PROTECTION_CANNOT_BE_ERASED_BY_ENVELOPE')
        require(technical['frozen_source']['sha256'] == SOURCE and technical['dimensions'] == [1536,1024]
                and technical['export'] == version['export'] and technical['overlay_envelopes'] == envelopes
                and technical['protected_pixels_changed'] == 0
                and technical['protected_max_channel_difference'] == 0
                and technical['source_layer_unchanged'] is True,
                'ACCEPTED_PHOTOGRAPHY_CHANGED')
        compare_pixels(root,technical,envelopes)
        if number < used or unit['phase'] != 'AWAITING_PIXEL_REVIEW':
            require(version.get('pixel_review'), 'PRIOR_PIXEL_REVIEW_REQUIRED')
        if version.get('pixel_review'):
            reviewed = validate_review(root, version, number, unit['review_inputs'])
            require(version.get('verdict') == reviewed['verdict'], 'VERSION_REVIEW_VERDICT_CONFLICT')
            if number < used:
                require(reviewed['verdict']=='AI_FAIL', 'AI_PASS_STOPS_SERIAL_REPAIR')
    current = unit['versions'][-1]
    if unit['phase'] == 'AWAITING_PIXEL_REVIEW': return
    verdict = validate_review(root, current, used, unit['review_inputs'])['verdict']
    require((unit['phase']=='REVISION_REQUIRED' and verdict=='AI_FAIL' and (continuous or used<3))
            or (unit['phase']=='DELIVERED_AI_FAIL' and verdict=='AI_FAIL')
            or (unit['phase']=='HUMAN_REJECTED' and verdict=='AI_FAIL' and used==3)
            or (unit['phase']=='DELIVERED_AI_PASS' and verdict=='AI_PASS'), 'WORKER_VERDICT_ACTION_CONFLICT')
    if unit['phase'].startswith('DELIVERED_') or unit['phase']=='HUMAN_REJECTED':
        archive=load(root,current['drive_archive'])
        require(archive['readback_result']=='PASS' and archive['poster_sha256']==current['export']['sha256']
                and archive['raw_bytes_equal_local'] is True, 'DRIVE_RAW_READBACK_REQUIRED')

def compare_pixels(root,technical,envelopes=ENVELOPES):
    from .vpd_locked_mainline_state import _png_rgb_rows
    source=technical['frozen_source']; export=technical['export']
    check_ref(root,source); check_ref(root,export)
    changed=0; compared=0; maximum=0
    for y,(a,b) in enumerate(zip(_png_rgb_rows(root,source),_png_rgb_rows(root,export))):
        omitted=sorted((x0,x1) for x0,y0,x1,y1 in envelopes if y0<=y<y1)
        start=0; intervals=[]
        for x0,x1 in omitted: intervals.append((start,x0)); start=x1
        intervals.append((start,1536))
        for x0,x1 in intervals:
            aa,bb=a[x0*3:x1*3],b[x0*3:x1*3]; compared+=x1-x0
            if aa!=bb:
                changed+=sum(aa[p:p+3]!=bb[p:p+3] for p in range(0,len(aa),3))
                maximum=max(maximum,max(abs(x-z) for x,z in zip(aa,bb)))
    require(changed==0 and maximum==0 and compared==technical['protected_pixels_compared'],
            'APPROVED_PHOTO_ACTUAL_PIXELS_CHANGED')

def validate_review(root, version, number, expected_inputs):
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
    require(bindings==dict(expected,T=version['export']['sha256']) and expected['S']==SOURCE
            and expected['R']=='87a28f5cd4b5d15b01e6536206127c357043a904b3c0dab3bfa0c50080782167',
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
