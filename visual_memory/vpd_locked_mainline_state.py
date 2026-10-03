"""State compatibility for the locked mainline; never certifies visual quality.

Uses the existing lock/checkpoint/ledger. Historical defects stay disclosed and
byte-preserved. Repository checks constrain cooperating executors, not the host.
"""
import hashlib
import json
import zlib

from .vpd_task_lock import (
    LOCK_PATH, CHECKPOINT_PATH, PROJECT, PARENT, read, path, require,
    check_ref, digest, evidence_bytes,
)

PROFILE = 'vpd-locked-mainline/v1'
STAGES = ['P3_STAGE1', 'P4_CONTENT', 'P4_ASPECT', 'P5_SECOND_STYLE', 'P7_DELIVERY']
HUMAN_FINAL_TASK = 'VPD-CANDIDATE-88-HUMAN-FINAL-AESTHETIC-REVIEW-20261003-01'
HUMAN_FAIL_STATUS = (
    'VPD_CANDIDATE_88_HUMAN_FINAL_FAIL_PHOTO_PROTECTED_TYPOGRAPHY_WORDMARK_REDESIGN_REQUIRED'
)
TAKEOVER_TASK = 'VPD-CHAZUO-CODEX-COMPLETE-POSTER-20261003-01'
OVERLAY_ENVELOPES = [[920, 94, 1536, 409], [32, 28, 224, 142]]
TAKEOVER_BUDGET = {'formal_versions_max': 3, 'revisions_max': 2, 'photo_generations': 0,
                   'paid_compute_usd': 0, 'training': 0, 'automations': 0, 'second_style': 0}


def validate_locked_mainline(root):
    lock, cp = read(root, LOCK_PATH), read(root, CHECKPOINT_PATH)
    adapter = read(root, 'PROJECT_CONTROL_ADAPTER.json')
    post_delivery = bool(lock.get('candidate88_human_final_review'))
    current_task = (lock['codex_takeover']['task_id'] if lock.get('codex_takeover')
                    else HUMAN_FINAL_TASK if post_delivery else PARENT)
    require(lock['state_profile'] == PROFILE, 'LOCK_SCHEMA')
    require(lock['schema_version'] == 'vpd-current-task-lock/v1', 'LOCK_SCHEMA')
    require(lock['project_id'] == cp['project_id'] == adapter['project_id'] == PROJECT,
            'PROJECT_ID_MISMATCH')
    require(lock['parent_active_task_id'] == PARENT,
            'PARENT_TASK_CHANGED')
    require(cp['active_task_ids'] == [current_task] and
            adapter['current_mainline']['task_id'] == current_task, 'CURRENT_TASK_CHANGED')
    require(lock['repository'] == adapter['repository'] == 'vubaoha034-hash/shenmei',
            'REPOSITORY_DRIFT')
    require(lock['branch'] == adapter['canonical_branch'] ==
            'visual-program-distillation-v2-photography-design-20260814', 'BRANCH_DRIFT')
    require(adapter['task_registry_path'] == adapter['task_lock']['path'] == LOCK_PATH,
            'COMPETING_TASK_INDEX')
    check_ref(root, adapter['task_lock'])
    require(adapter['task_lock']['revision'] == lock['revision'], 'STALE_LOCK_REVISION')
    check_ref(root, cp['task_lock'])
    require(cp['task_lock']['path'] == LOCK_PATH and
            cp['task_lock']['sha256'] == digest(path(root, LOCK_PATH)) and
            cp['task_lock'].get('revision', lock['revision']) == lock['revision'],
            'STALE_CHECKPOINT_LOCK')
    require(cp['status'] == lock['status'] == adapter['current_mainline']['status'],
            'STATE_STATUS_CONFLICT')
    require(lock['next_required_action'] == cp['next_required_action'] ==
            adapter['current_mainline']['next_required_action'], 'NEXT_ACTION_DRIFT')
    parent_projection = adapter['vpd_system_goal_authority']
    if post_delivery:
        require(parent_projection['legacy_holdout_fields_scope'] ==
                'HISTORICAL_NOT_CURRENT_EXECUTION_AUTHORITY' and
                parent_projection['active_task_id'] == PARENT and
                parent_projection['current_state_path'] == LOCK_PATH and
                parent_projection['checkpoint'] ==
                'VPD_MAINLINE_BOUNDED_DELIVERY_COMPLETE_WITH_KNOWN_LIMITATIONS' and
                parent_projection['next_required_action'] == 'MAINLINE_DELIVERY_COMPLETE_STOP' and
                parent_projection['render_allowed'] is False,
                'HISTORICAL_PARENT_PROJECTION_CONFLICT')
    else:
        require(parent_projection['checkpoint'] == lock['status'] and
                parent_projection['next_required_action'] == lock['next_required_action'],
                'STATE_STATUS_CONFLICT')
    require(cp['mainline_lock'] == adapter['mainline_lock'] == lock['mainline_lock'],
            'MAINLINE_MIRROR_CONFLICT')
    require(cp['mainline_progress'] == lock['mainline_progress'], 'PROGRESS_MIRROR_CONFLICT')
    main = lock['mainline_lock']
    require(main['locked'] is True, 'MAINLINE_UNLOCKED')
    require(lock['mainline_plan'] == cp['mainline_plan'] == adapter['mainline_plan'] ==
            main['plan'] and lock['latest_evidence'] == cp['latest_evidence'],
            'MAINLINE_MIRROR_CONFLICT')
    check_ref(root, lock['latest_evidence'])
    if not post_delivery:
        require(lock['latest_evidence'] == main['authority'], 'MAINLINE_MIRROR_CONFLICT')
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
    require(main['id'] == contract['id'] and
            parent_projection.get('current_mainline_contract') == main['contract'],
            'MAINLINE_MIRROR_CONFLICT')
    if not post_delivery:
        require(adapter['current_mainline']['plan'] == main['plan'] and
                adapter['current_mainline']['subtask_id'] == lock['mainline_progress']['task_id'],
                'MAINLINE_MIRROR_CONFLICT')
    else:
        current = adapter['current_mainline']
        require(current.get('plan', main['plan']) == main['plan'] and
                current.get('subtask_id', current_task) == current_task,
                'MAINLINE_MIRROR_CONFLICT')
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
    _validate_progress(root, lock, adapter, contract, historical=post_delivery)
    if post_delivery:
        _validate_human_final(root, lock, cp, adapter)
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
    _validate_append_only_ledger(root, lock, cp, preserve, current_task)
    require(adapter['ledger_tails']['commercial_design_pipeline'] ==
            cp['ledger_tails']['commercial_design_pipeline'], 'LEDGER_TAIL_MISMATCH')
    return lock, cp


def _ref_only(ref):
    return {k: ref[k] for k in ['path', 'sha256']}


def _validate_human_final(root, lock, cp, adapter):
    """The actual human rejection governs the current route after bounded P7."""
    ref = lock['candidate88_human_final_review']
    verdict = _receipt(root, ref)
    require(cp.get('candidate88_human_final_review') == ref and
            verdict.get('schema_version') == 'vpd-human-aesthetic-verdict/v1' and
            verdict.get('project_id') == PROJECT and
            verdict.get('authority') == 'LIU_XIANSHENG_HUMAN_FINAL_AESTHETIC_REVIEW' and
            verdict.get('recorded_at') and verdict.get('user_feedback_verbatim'),
            'HUMAN_FINAL_EVIDENCE_REQUIRED')
    require(ref.get('verdict') == verdict.get('normalized_verdict', {}).get('overall') ==
            'HUMAN_FAIL_DESIGN_SYSTEM_NOT_READY' and ref.get('design_failed') is True and
            ref.get('photo_protected') is True and
            verdict['normalized_verdict'].get('first_image_photo') ==
            'HUMAN_POSITIVE_PROTECT_FREEZE_PHOTO' and
            verdict.get('supersedes_external_deliverable_as_final_quality_judgment') is True and
            verdict.get('external_pass_remains_technical_evidence_only') is True,
            'HUMAN_FINAL_SCOPE_CHANGED')
    review = lock['mainline_progress'].get('post_p7_human_review', {})
    require(review.get('status') == ref['verdict'] and review.get('current_route') is True and
            review.get('human_personal_acceptance') is False and
            review.get('photo_protected') is True and
            review.get('next_required_action') == ref.get('next_legal_action') ==
            verdict.get('next_legal_action'), 'HUMAN_FINAL_ROUTE_CONFLICT')
    for key in ['visual_master_freeze_guard', 'baseline_preservation']:
        require(lock[key] == cp[key], 'PHOTO_PROTECTION_MIRROR_CONFLICT')
        check_ref(root, lock[key])
    boundary = lock['execution_boundary']
    require(boundary.get('modify_accepted_repair03_photo') is False and
            boundary.get('photo_repair_loop_closed') is True and
            boundary.get('repair04_allowed') is False, 'PHOTO_PROTECTION_CHANGED')
    r4 = lock['candidate88_external_review_r4']
    require(r4 == cp['candidate88_external_review_r4'], 'CURRENT_EVIDENCE_MIRROR_CONFLICT')
    for key in ['prior_r3_review', 'revision', 'review', 'callback_receipt']:
        check_ref(root, r4[key])
    revision = read(root, r4['revision']['path'])
    require(revision['revision_scope'].get('full_photo_regeneration_allowed') is False and
            r4['revision']['drive_file_id'] == revision['output']['drive_file_id'] and
            r4['revision']['dimensions'] == revision['output']['dimensions'],
            'PHOTO_PROTECTION_CHANGED')
    if lock.get('codex_takeover'):
        _validate_codex_takeover(root, lock, cp, adapter)
    else:
        require(lock['status'] == HUMAN_FAIL_STATUS and
                lock['next_required_action'] == verdict['next_legal_action'],
                'HUMAN_FINAL_ROUTE_CONFLICT')
        require(adapter['current_mainline'].get('evidence', {}).get('human_verdict') ==
                _ref_only(ref), 'CURRENT_EVIDENCE_MIRROR_CONFLICT')
        require(lock['render_allowed'] is False and
                boundary['current_image_generation_authorization'] ==
                boundary['current_image_generation_count_max'] ==
                boundary['current_figma_canvas_authorization'] == 0,
                'RENDER_NOT_AUTHORIZED')
        require(lock['latest_evidence'] in [lock['mainline_lock']['authority'], _ref_only(ref)],
                'CURRENT_EVIDENCE_MIRROR_CONFLICT')


def _takeover_budget(budget):
    require(isinstance(budget, dict) and all(type(budget.get(k)) is int and budget[k] == v
            for k, v in TAKEOVER_BUDGET.items()), 'BUDGET_CHANGED')
    versions, revisions = budget.get('formal_versions_used'), budget.get('revisions_used')
    require(type(versions) is int and type(revisions) is int and 0 <= versions <= 3 and
            revisions == max(0, versions - 1), 'BUDGET_CHANGED')
    return versions, revisions


def _validate_codex_takeover(root, lock, cp, adapter):
    """Bounded successor in the existing lock; a receipt is never a second task index."""
    take = lock['codex_takeover']
    require(take == cp.get('codex_takeover') == adapter['current_mainline'].get('codex_takeover')
            and take.get('task_id') == lock.get('current_task_id') == TAKEOVER_TASK and
            take.get('status') == lock['status'] and
            take.get('next_required_action') == lock['next_required_action'],
            'CONTINUATION_MIRROR_CONFLICT')
    feedback_settled = take.get('status') == 'VPD_CODEX_CHAZUO_REJECTED_SOURCE_MISMATCH'
    require(take.get('state_writer') == 'ROOT_EXECUTOR_ONLY' and
            take.get('candidate_promoted') is False and take.get('human_verdict') ==
            ('REJECTED' if feedback_settled else 'PENDING'),
            'CONTINUATION_SCOPE_CHANGED')
    authority = _receipt(root, take.get('authorization'))
    require(authority.get('schema_version') == 'vpd-codex-bounded-design-authorization/v1' and
            authority.get('authority_class') == 'EXPLICIT_USER_CODEX_COMPLETE_POSTER_AUTHORIZATION'
            and authority.get('project_id') == PROJECT and authority.get('task_id') == TAKEOVER_TASK
            and authority.get('source', {}).get('kind') == 'CURRENT_HUMAN_USER_MESSAGE'
            and authority['source'].get('verbatim'), 'CONTINUATION_AUTHORITY_REQUIRED')
    require(authority.get('budget') == dict(TAKEOVER_BUDGET, parallel_alternatives=0,
            hidden_variants=0), 'BUDGET_CHANGED')
    scope = authority.get('authorized_scope', {})
    require(scope.get('editable_figma_design_and_exports') is True and
            scope.get('necessary_wordmark_image_tools') is True and
            scope.get('single_business_state_writer') == 'ROOT_EXECUTOR_ONLY' and
            scope.get('new_global_task_system') is False,
            'CONTINUATION_SCOPE_CHANGED')
    protection = _receipt(root, take.get('photo_protection'))
    r4 = read(root, lock['candidate88_external_review_r4']['revision']['path'])['output']
    source = protection.get('source', {})
    require(protection.get('schema_version') == 'vpd-scoped-photo-protection/v1' and
            protection.get('project_id') == PROJECT and
            protection.get('task_id') == TAKEOVER_TASK and
            protection.get('human_verdict_ref') == _ref_only(lock['candidate88_human_final_review'])
            and source.get('candidate_id') == '88-R4' and
            all(source.get(k) == r4[k] for k in ['drive_file_id', 'sha256', 'dimensions']) and
            source.get('pixels_inspected') is True and source.get('download_sha256_verified') is True,
            'PHOTO_PROTECTION_CHANGED')
    require(protection.get('visible_design_overlay_envelopes') == OVERLAY_ENVELOPES and
            protection.get('original_failed_design_regions') == [[920, 94, 1536, 409], [40, 49, 194, 80]]
            and protection.get('protected_visible_pixels') ==
            'ALL_PIXELS_OUTSIDE_DECLARED_DESIGN_OVERLAY_ENVELOPES' and
            protection.get('hidden_background_recovery') == 'UNKNOWN_NOT_CLAIMED' and
            all(protection.get(k) is False for k in ['original_assets_modified',
                'photo_regeneration_allowed', 'source_file_overwrite_allowed',
                'historical_figma_protected_nodes_modified']), 'PHOTO_PROTECTION_CHANGED')
    versions, revisions = _takeover_budget(take.get('budget'))
    boundary = lock['execution_boundary']
    require(lock['render_allowed'] is False and
            boundary['current_image_generation_authorization'] ==
            boundary['current_image_generation_count_max'] == 0 and
            type(boundary['current_figma_canvas_authorization']) is int and
            boundary['current_figma_canvas_authorization'] == 3 - versions and
            boundary['current_image_generation_authorization_scope'] == TAKEOVER_TASK and
            boundary.get('bounded_typography_design_versions_authorization') == take['authorization']
            and boundary.get('successor_execution_authorized') is True,
            'CONTINUATION_AUTHORIZATION_MIRROR_CONFLICT')
    ref = take.get('receipt')
    receipt = _receipt(root, ref)
    require(lock['latest_evidence'] == ref and
            adapter['current_mainline'].get('evidence', {}).get('execution') == ref and
            adapter['current_mainline']['evidence'].get('human_verdict') in
            [lock['candidate88_human_final_review'], _ref_only(lock['candidate88_human_final_review'])],
            'CURRENT_EVIDENCE_MIRROR_CONFLICT')
    state = take['status'].removeprefix('VPD_CODEX_CHAZUO_')
    if state == 'AUTHORIZED_SOURCE_PROTECTED':
        require(ref == take['authorization'] and versions == revisions == 0 and
                take['next_required_action'] == 'CREATE_ONE_EDITABLE_CHAZUO_POSTER_VERSION_1',
                'CONTINUATION_ACTION_CONFLICT')
        return
    require(state in ['AWAITING_PIXEL_REVIEW', 'REVISION_REQUIRED',
                     'DELIVERED_AI_PASS_HUMAN_PENDING', 'DELIVERED_AI_FAIL_HUMAN_PENDING',
                     'REJECTED_SOURCE_MISMATCH'],
            'UNKNOWN_CONTINUATION_STATE')
    require(receipt.get('task_id') == TAKEOVER_TASK and receipt.get('status') == take['status'] and
            receipt.get('next_required_action') == take['next_required_action'] and
            receipt.get('budget') == {'formal_versions_used': versions, 'revisions_used': revisions}
            and versions > 0, 'CONTINUATION_RECEIPT_CONFLICT')
    require(receipt.get('artifact_refs'), 'CONTINUATION_ARTIFACT_REQUIRED')
    for artifact in receipt['artifact_refs']:
        check_ref(root, artifact)
    technical = _validate_takeover_technical(root, receipt.get('technical_check'), versions, protection)
    if state == 'AWAITING_PIXEL_REVIEW':
        require(take['next_required_action'] == 'REVIEW_CURRENT_CHAZUO_POSTER_ACTUAL_PIXELS',
                'CONTINUATION_ACTION_CONFLICT')
        return
    review = _validate_isolated_pixel_review(root, receipt.get('pixel_review'), versions,
                                            technical['export'])
    if state == 'REJECTED_SOURCE_MISMATCH':
        feedback = _receipt(root, take.get('human_feedback'))
        correction = _receipt(root, take.get('source_identity_correction'))
        recovery = take.get('source_recovery')
        recovery_action = 'RECOVER_TEXT_FREE_SOURCE_OF_CONFIRMED_FIRST_IMAGE'
        if recovery:
            authority_recovery = _receipt(root, recovery.get('authorization'))
            require(authority_recovery.get('schema_version') == 'vpd-source-recovery-continuation-authorization/v1'
                    and authority_recovery.get('source', {}).get('kind') == 'CURRENT_HUMAN_USER_MESSAGE'
                    and authority_recovery['source'].get('verbatim')
                    and authority_recovery.get('task_id') == TAKEOVER_TASK
                    and authority_recovery.get('scope', {}).get('formal_poster_budget_reset') is False
                    and authority_recovery['scope'].get('source_photo_regeneration') is False,
                    'SOURCE_RECOVERY_AUTHORITY_REQUIRED')
            require(recovery == receipt.get('source_recovery') == boundary.get('source_recovery_tool_trial')
                    and recovery.get('source_sha256') == 'e7af9c9e88ff9dd38357a570305c4b5d40e98678d14c174957d4bdf2e7bdfd29'
                    and recovery.get('imagegen_edit_calls_max') == 1
                    and type(recovery.get('imagegen_edit_calls_used')) is int
                    and 0 <= recovery['imagegen_edit_calls_used'] <= 1
                    and recovery.get('formal_poster_versions_added') == 0
                    and recovery.get('is_recovered_hidden_original') is False,
                    'SOURCE_RECOVERY_SCOPE_CONFLICT')
            if recovery.get('phase') == 'HUMAN_REVIEW_REQUIRED':
                recovery_action = 'LIU_XIANSHENG_REVIEW_LOCAL_BACKGROUND_RECONSTRUCTION'
                delivered = _receipt(root, recovery.get('delivery_manifest'))
                source_review = _receipt(root, recovery.get('pixel_review'))
                source_audit = _receipt(root, source_review.get('isolation_audit'))
                protection_recovery = _receipt(root, delivered.get('pixel_protection'))
                require(delivered.get('kind') == 'LOCAL_BACKGROUND_RECONSTRUCTION_NOT_TEXTLESS_ORIGINAL'
                        and delivered.get('hidden_original_recovered') is False
                        and delivered.get('formal_poster_versions_added') == 0
                        and delivered.get('source', {}).get('sha256') == recovery['source_sha256']
                        and delivered.get('output', {}).get('dimensions') == [1536, 1024]
                        and source_review.get('review_unit') == 'SOURCE_RECONSTRUCTION_ONLY'
                        and source_review.get('verdict') in ['AI_PASS', 'AI_FAIL']
                        and source_review.get('version') == 0
                        and source_review.get('export', {}).get('sha256') == delivered['output']['sha256']
                        and source_audit.get('verified') is True
                        and source_audit.get('attachments_verified') == ['P', 'N', 'R', 'S', 'T']
                        and source_audit.get('actual_model') == 'gpt-6.1-sol'
                        and source_audit.get('actual_reasoning_effort') == 'max'
                        and source_audit.get('tool_scope_violations') == []
                        and protection_recovery.get('protected_pixels_changed') == 0
                        and protection_recovery.get('protected_max_channel_difference') == 0,
                        'SOURCE_RECOVERY_ACTUAL_DELIVERY_REQUIRED')
                require(recovery.get('human_verdict') == 'PENDING', 'SOURCE_RECOVERY_HUMAN_ACCEPTANCE_REQUIRED')
            else:
                require(recovery.get('phase') in ['PREPARING', 'EDIT_IN_PROGRESS', 'TOOL_BLOCKED'],
                        'SOURCE_RECOVERY_PHASE_UNKNOWN')
        require(versions == 3 and revisions == 2 and review['verdict'] == 'AI_FAIL' and
                take['next_required_action'] == recovery_action
                and receipt.get('human_verdict') == 'REJECTED'
                and receipt.get('human_feedback') == take['human_feedback']
                and receipt.get('source_identity_correction') == take['source_identity_correction'],
                'HUMAN_FEEDBACK_STATE_CONFLICT')
        require(feedback.get('source_kind') == 'CURRENT_HUMAN_USER_MESSAGE' and
                feedback.get('verbatim') and feedback.get('human_verdict') == 'REJECTED' and
                feedback.get('target_sha256') == technical['export']['sha256'],
                'HUMAN_FEEDBACK_TARGET_CONFLICT')
        comparison = correction.get('pixel_comparison', {})
        require(correction.get('prior_r4_human_photo_binding') == 'REVOKED' and
                correction.get('new_design_created') is False and
                correction.get('clean_photography_source') == 'NOT_YET_LOCATED' and
                correction.get('generated_first_image', {}).get('sha256') ==
                'e7af9c9e88ff9dd38357a570305c4b5d40e98678d14c174957d4bdf2e7bdfd29' and
                correction.get('user_uploaded_image', {}).get('sha256') ==
                'a579e846b41be42faf92d0c9e6322dd67da25a1ff0c67a1bc9e9c4d194aaf590' and
                comparison.get('gallery_vs_upload', {}).get('rgb_pixels_changed') == 0 and
                comparison.get('gallery_vs_upload', {}).get('pixels_compared') == 1572864 and
                comparison.get('gallery_vs_r4', {}).get('rgb_pixels_changed', 0) > 0,
                'SOURCE_IDENTITY_CORRECTION_REQUIRED')
        return
    if state == 'REVISION_REQUIRED':
        require(review['verdict'] == 'AI_FAIL' and versions < 3 and
                take['next_required_action'] == 'REVISE_CURRENT_CHAZUO_TYPOGRAPHY_FROM_PIXEL_EVIDENCE',
                'CONTINUATION_ACTION_CONFLICT')
    else:
        expected = 'AI_PASS' if state == 'DELIVERED_AI_PASS_HUMAN_PENDING' else 'AI_FAIL'
        action = ('LIU_XIANSHENG_REVIEW_FINAL_CHAZUO_POSTER' if expected == 'AI_PASS' else
                  'LIU_XIANSHENG_REVIEW_FINAL_CHAZUO_POSTER_AND_FAILED_REVIEW')
        require(review['verdict'] == expected and take['next_required_action'] == action,
                'CONTINUATION_ACTION_CONFLICT')


def _validate_isolated_pixel_review(root, ref, version, exported):
    """A settled AI verdict needs actual attachment reads and audited isolation."""
    review = _receipt(root, ref)
    ids = ['P', 'N', 'R', 'T']
    bindings = review.get('input_bindings', [])
    observations = review.get('observations', [])
    require(review.get('task_id') == TAKEOVER_TASK and type(review.get('version')) is int and
            review['version'] == version and review.get('export') == exported and
            review.get('reviewer') and review.get('verdict') in ['AI_PASS', 'AI_FAIL'] and
            review.get('human_verdict') == 'HIDDEN_PENDING' and
            'personal_fit' in review and review['personal_fit'] is None and
            review.get('pixels_seen') == ids and len(bindings) == 4 and
            [b.get('neutral_id') for b in bindings] == ids and
            all(_sha256_value(b.get('sha256')) for b in bindings) and
            len({b['sha256'] for b in bindings}) == 4 and bindings[-1]['sha256'] == exported['sha256']
            and isinstance(observations, list) and len(observations) >= 5 and
            all(isinstance(o, dict) and o.get('region') and o.get('evidence') for o in observations),
            'PIXEL_REVIEW_EVIDENCE_REQUIRED')
    check_ref(root, exported)
    audit = _receipt(root, review.get('isolation_audit'))
    require(audit.get('schema_version') == 'vpd-isolated-pixel-review-audit/v1' and
            audit.get('verified') is True and audit.get('actual_model') == 'gpt-6.1-sol' and
            audit.get('actual_reasoning_effort') == 'max' and
            audit.get('attachments_verified') == ids and audit.get('tool_scope_violations') == [],
            'REVIEW_ISOLATION_EVIDENCE_REQUIRED')
    carrier = audit.get('carrier')
    if carrier == 'FRESH_EXTERNAL_CODEX_EXEC':
        require(audit.get('fresh_process') is True and audit.get('outside_project_directory') is True
                and audit.get('ignore_user_config') is True and
                audit.get('resumed_or_forked') is False and type(audit.get('exit_code')) is int and
                audit['exit_code'] == 0, 'REVIEW_ISOLATION_EVIDENCE_REQUIRED')
    else:
        require(carrier == 'FRESH_FORK_NONE_PIXEL_AGENT' and audit.get('fork_turns') == 'none' and
                audit.get('history_inherited') is False and
                audit.get('resumed_or_history_forked') is False and
                audit.get('source_project_context_read') is False and
                audit.get('fresh_agent') is True and audit.get('completed') is True,
                'REVIEW_ISOLATION_EVIDENCE_REQUIRED')
        amendment = _receipt(root, audit.get('carrier_amendment'))
        require(amendment.get('task_id') == TAKEOVER_TASK and
                amendment.get('from_carrier') == 'FRESH_EXTERNAL_CODEX_EXEC' and
                amendment.get('to_carrier') == carrier and
                amendment.get('prior_failures_preserved') is True and
                amendment.get('source', {}).get('kind') == 'CURRENT_HUMAN_USER_MESSAGE',
                'REVIEW_CARRIER_AMENDMENT_REQUIRED')
        check_ref(root, amendment.get('failure_evidence'))
    evidence = _receipt(root, audit.get('evidence'))
    reads = evidence.get('tool_reads', [])
    require(evidence.get('thread_id') and
            evidence.get('turn_context') == {'model': audit['actual_model'],
                'reasoning_effort': audit['actual_reasoning_effort']} and
            _sha256_value(evidence.get('initial_prompt_sha256')) and
            evidence['initial_prompt_sha256'] == audit.get('initial_prompt_sha256') and
            len(reads) == 4 and {r.get('neutral_id') for r in reads} == set(ids) and
            {r.get('neutral_id'): r.get('sha256') for r in reads} ==
                {b['neutral_id']: b['sha256'] for b in bindings} and
            all(r.get('tool') == 'view_image' and r.get('path') for r in reads) and
            len({r['path'] for r in reads}) == 4, 'REVIEW_ACTUAL_TOOL_READS_REQUIRED')
    raw_audit = _receipt(root, evidence.get('raw_tool_read_audit'))
    require(raw_audit.get('thread_id') == evidence['thread_id'] and
            raw_audit.get('tool_reads') == reads and raw_audit.get('extra_tool_reads') == [] and
            raw_audit.get('source_project_context_reads') == [] and
            _sha256_value(raw_audit.get('raw_rollout_sha256')),
            'REVIEW_ACTUAL_TOOL_READS_REQUIRED')
    if carrier == 'FRESH_FORK_NONE_PIXEL_AGENT':
        spawn = _receipt(root, evidence.get('spawn_receipt'))
        require(spawn.get('thread_id') == evidence['thread_id'] and spawn.get('fork_turns') == 'none'
                and spawn.get('history_inherited') is False and
                spawn.get('initial_prompt_sha256') == evidence['initial_prompt_sha256'] and
                spawn.get('actual_model') == audit['actual_model'] and
                spawn.get('actual_reasoning_effort') == audit['actual_reasoning_effort'],
                'REVIEW_SPAWN_EVIDENCE_REQUIRED')
    return review


def _sha256_value(value):
    return isinstance(value, str) and len(value) == 64 and all(c in '0123456789abcdef' for c in value)


def _validate_takeover_technical(root, ref, version, protection):
    technical = _receipt(root, ref)
    require(technical.get('task_id') == TAKEOVER_TASK and technical.get('version') == version and
            technical.get('source_sha256') == protection['source']['sha256'] and
            technical.get('dimensions') == protection['source']['dimensions'] == [1536, 1024] and
            technical.get('overlay_envelopes') == OVERLAY_ENVELOPES and
            technical.get('source_layer_unchanged') is True and
            technical.get('protected_pixels_changed') == 0 and
            technical.get('protected_pixels_compared') == 1356936,
            'PHOTO_PROTECTION_TECHNICAL_EVIDENCE_REQUIRED')
    for key in ['source', 'export', 'figma_readback', 'trace']:
        check_ref(root, technical.get(key))
    require(technical['source']['sha256'] == protection['source']['sha256'],
            'PHOTO_SOURCE_IDENTITY_CHANGED')
    for key in ['source', 'export']:
        raw = evidence_bytes(path(root, technical[key]['path']))
        require(raw[:8] == b'\x89PNG\r\n\x1a\n' and raw[12:16] == b'IHDR' and
                [int.from_bytes(raw[16:20], 'big'), int.from_bytes(raw[20:24], 'big')] == [1536, 1024],
                'PIXEL_EVIDENCE_REQUIRED')
    compared, changed = _protected_pixel_comparison(root, technical['source'], technical['export'])
    require(compared == technical['protected_pixels_compared'] and
            changed == technical['protected_pixels_changed'] == 0, 'PROTECTED_PHOTO_PIXELS_CHANGED')
    figma = technical.get('figma', {})
    require(figma.get('file_key') and figma.get('node_id') and figma.get('url') and
            figma['file_key'] in figma['url'] and
            ('node-id=' + figma['node_id'].replace(':', '-')) in figma['url'],
            'FIGMA_SOURCE_EVIDENCE_REQUIRED')
    readback = read(root, technical['figma_readback']['path'])
    require(readback.get('file_key') == figma['file_key'] and
            readback.get('node_id') == figma['node_id'] and readback.get('source_layer') ==
            {'source_sha256': protection['source']['sha256'], 'x': 0, 'y': 0,
             'width': 1536, 'height': 1024, 'rotation': 0, 'locked': True},
            'FIGMA_SOURCE_EVIDENCE_REQUIRED')
    return technical


def _png_rgb_rows(root, ref):
    """Decode the bounded RGB/RGBA PNG evidence; no visual or taste judgment."""
    raw = evidence_bytes(path(root, ref['path']))
    require(raw[:8] == b'\x89PNG\r\n\x1a\n', 'PIXEL_EVIDENCE_REQUIRED')
    offset, packed, header = 8, bytearray(), None
    while offset + 12 <= len(raw):
        length = int.from_bytes(raw[offset:offset + 4], 'big')
        tag = raw[offset + 4:offset + 8]
        payload = raw[offset + 8:offset + 8 + length]
        require(len(payload) == length and offset + length + 12 <= len(raw),
                'PIXEL_EVIDENCE_REQUIRED')
        if tag == b'IHDR':
            header = payload
        elif tag == b'IDAT':
            packed.extend(payload)
        offset += length + 12
        if tag == b'IEND':
            break
    require(header and len(header) == 13 and header[8] == 8 and header[9] in [2, 6]
            and header[10:] == b'\0\0\0' and
            [int.from_bytes(header[:4], 'big'), int.from_bytes(header[4:8], 'big')] == [1536, 1024],
            'UNSUPPORTED_PIXEL_EVIDENCE_ENCODING')
    channels = 3 if header[9] == 2 else 4
    stride, expected = 1536 * channels, (1536 * channels + 1) * 1024
    decoder = zlib.decompressobj()
    try:
        decoded = decoder.decompress(bytes(packed), expected + 1)
    except zlib.error:
        require(False, 'PIXEL_EVIDENCE_REQUIRED')
    require(len(decoded) == expected and decoder.eof and not decoder.unconsumed_tail,
            'PIXEL_EVIDENCE_REQUIRED')
    previous = bytearray(stride)
    for y in range(1024):
        start = y * (stride + 1)
        kind = decoded[start]
        row = bytearray(decoded[start + 1:start + stride + 1])
        require(kind in range(5), 'PIXEL_EVIDENCE_REQUIRED')
        if kind:
            for x in range(stride):
                left = row[x - channels] if x >= channels else 0
                up = previous[x]
                upper_left = previous[x - channels] if x >= channels else 0
                if kind == 1:
                    predictor = left
                elif kind == 2:
                    predictor = up
                elif kind == 3:
                    predictor = (left + up) // 2
                else:
                    p = left + up - upper_left
                    a, b, c = abs(p - left), abs(p - up), abs(p - upper_left)
                    predictor = left if a <= b and a <= c else up if b <= c else upper_left
                row[x] = (row[x] + predictor) & 255
        previous = row
        if channels == 4:
            require(all(alpha == 255 for alpha in row[3::4]), 'TRANSPARENT_PHOTO_EVIDENCE')
            yield b''.join(row[x:x + 3] for x in range(0, stride, 4))
        else:
            yield bytes(row)


def _protected_pixel_comparison(root, source, exported):
    compared, changed = 0, 0
    for y, (a, b) in enumerate(zip(_png_rgb_rows(root, source), _png_rgb_rows(root, exported))):
        omitted = sorted((x1, x2) for x1, y1, x2, y2 in OVERLAY_ENVELOPES if y1 <= y < y2)
        start, intervals = 0, []
        for x1, x2 in omitted:
            intervals.append((start, x1))
            start = x2
        intervals.append((start, 1536))
        for x1, x2 in intervals:
            left, right = a[x1 * 3:x2 * 3], b[x1 * 3:x2 * 3]
            compared += x2 - x1
            if left != right:
                changed += sum(left[x:x + 3] != right[x:x + 3] for x in range(0, len(left), 3))
    return compared, changed


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


def _scoped_format_failure_continuation(root, progress, prior, result_ref, result):
    """Admit an authorized exploratory successor while retaining the failed result."""
    require(prior == 'P4_ASPECT' and progress['stage_id'] in ['P5_SECOND_STYLE', 'P7_DELIVERY']
            and result['outcome'] == 'TEST_FAILED_OR_NO_GAIN'
            and result.get('exact_aspect_passed') is False
            and result.get('visual_set_ready') is True, 'PRIOR_WHOLE_ACCEPTANCE_REQUIRED')
    amendment = _receipt(root, progress.get('scoped_progression_amendment'))
    authority = _receipt(root, amendment.get('source_scope'))
    require(amendment.get('authority_class') == 'USER_SCOPED_EXPLORATORY_CONTINUATION'
            and amendment.get('trigger') == 'OBSERVED_TECHNICAL_FAILURE'
            and amendment.get('prior_result') == result_ref
            and amendment.get('prior_stage_passed') is False
            and amendment.get('promotion_allowed') is False
            and amendment.get('source_scope') == progress.get('continuation_authority'),
            'SCOPED_CONTINUATION_REQUIRED')
    require(authority.get('authority_class') == 'USER_REQUESTED_MAINLINE_COMPLETION'
            and authority.get('project_id') == PROJECT and authority.get('source')
            and authority.get('total_new_images_max') == 10
            and any(s.get('stage_id') == progress['stage_id'] for s in authority.get('stages', [])),
            'SCOPED_CONTINUATION_REQUIRED')
    execution = _receipt(root, result['execution_receipt'])
    require(execution.get('attempts_consumed') == 2
            and any(e.get('code') == 'OUTPUT_FORMAT_MISMATCH' for e in execution.get('errors', [])),
            'OBSERVED_EXECUTION_ERROR_REQUIRED')


def _validate_progress(root, lock, adapter, contract, historical=False):
    progress = lock['mainline_progress']
    stage_id, state = progress['stage_id'], progress['status']
    require(stage_id in STAGES, 'UNKNOWN_MAINLINE_STAGE')
    stage = next(s for s in contract['stages'] if s['id'] == stage_id)
    actions = dict(stage['actions'])
    if state == 'AWAITING_INDEPENDENT_REVIEW':
        _delegated_review_authority(root, progress.get('review_delegation'),
                                    stage_id, progress['task_id'])
        actions[state] = 'WAIT_FOR_INDEPENDENT_REVIEWER_CALLBACK'
    require(state in actions, 'STAGE_ACTION_CONFLICT')
    if historical:
        require(stage_id == 'P7_DELIVERY' and state == 'COMPLETED',
                'HISTORICAL_DELIVERY_CHANGED')
    else:
        require(lock['next_required_action'] == actions[state], 'STAGE_ACTION_CONFLICT')
    receipts = progress['completed_stage_receipts']
    require(len(receipts) == STAGES.index(stage_id), 'PRIOR_STAGE_EVIDENCE_REQUIRED')
    for prior, ref in zip(STAGES, receipts):
        result = _tested_result(root, ref, prior)
        if result['outcome'] != 'PASSED':
            _scoped_format_failure_continuation(root, progress, prior, ref, result)
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
    if not historical:
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
        if historical:
            require(delivery.get('next_action') == actions[state] and
                    delivery.get('stage_id') == stage_id and
                    delivery.get('source_stage_receipts') == receipts and
                    delivery.get('authority') == auth.get('receipt') and
                    delivery.get('frozen_inputs') == frozen_inputs and
                    delivery.get('delivery_complete') is True and
                    delivery.get('system_validation_complete') is False and
                    delivery.get('human_personal_acceptance') is False and
                    delivery.get('global_method_promotion') is False and
                    progress.get('system_validation_complete') is False and
                    progress.get('global_production_promotion_allowed') is False,
                    'HISTORICAL_DELIVERY_CHANGED')
        for ref in delivery['artifact_refs']:
            check_ref(root, ref)


def _validate_append_only_ledger(root, lock, cp, preserve, current_task):
    ledger = preserve['ledger_prefix']
    lines = evidence_bytes(path(root, ledger['path'])).splitlines(keepends=True)
    count = ledger['event_count']
    require(hashlib.sha256(b''.join(lines[:count])).hexdigest() == ledger['sha256'],
            'HISTORICAL_LEDGER_REWRITTEN')
    require(len(lines) > count, 'MAINLINE_LEDGER_EVENT_REQUIRED')
    previous = json.loads(lines[count - 1])
    prior_versions, prior_revisions = 0, 0
    for raw in lines[count:]:
        event = json.loads(raw)
        claimed = event.pop('event_hash')
        actual = hashlib.sha256(json.dumps(event, ensure_ascii=False, sort_keys=True,
            separators=(',', ':')).encode()).hexdigest()
        require(claimed == actual, 'LEDGER_HASH_MISMATCH')
        require(event['previous_event_id'] == previous['event_id'] and
                event['previous_event_hash'] == previous['event_hash'], 'LEDGER_PARENT_MISMATCH')
        if event.get('task_id') == TAKEOVER_TASK:
            versions, revisions = _takeover_budget(event.get('after', {}).get('budget'))
            require(prior_versions <= versions <= prior_versions + 1 and
                    prior_revisions <= revisions <= prior_revisions + 1,
                    'CONTINUATION_BUDGET_ROLLBACK_OR_SKIP')
            prior_versions, prior_revisions = versions, revisions
            take = lock.get('codex_takeover', {})
            require(event.get('authorization') == take.get('authorization') and
                    event.get('evidence', [None, None])[-1] == take.get('photo_protection'),
                    'CONTINUATION_LEDGER_SCOPE_CHANGED')
            check_ref(root, event['authorization'])
            for ref in event['evidence']:
                check_ref(root, ref)
        previous = dict(event, event_hash=claimed)
    tail = {k: previous[k] for k in ['event_id', 'event_hash']}
    require(cp['ledger_tails']['commercial_design_pipeline'] == tail, 'LEDGER_TAIL_MISMATCH')
    require(previous['lock_sha256'] == digest(path(root, LOCK_PATH)), 'LEDGER_STALE_LOCK')
    after = previous.get('after', {})
    if current_task == TAKEOVER_TASK:
        require(after == {'revision': lock['revision'], 'checkpoint': cp['sequence'],
                'status': lock['status'], 'next_required_action': lock['next_required_action'],
                'budget': lock['codex_takeover']['budget']} and
                previous.get('evidence', [None])[0] == lock['codex_takeover']['receipt'],
                'LEDGER_CURRENT_STATE_CONFLICT')
    else:
        require(after == {'state': lock['status'], 'next_action': lock['next_required_action']},
                'LEDGER_CURRENT_STATE_CONFLICT')
    require(previous.get('task_id') == current_task and previous.get('project_id') == PROJECT,
            'LEDGER_CURRENT_STATE_CONFLICT')


def validate_locked_request(root, request, lock):
    require(request.get('lock_sha256') == digest(path(root, LOCK_PATH)), 'REQUEST_STALE_LOCK')
    require(request.get('action') == lock['next_required_action'], 'ACTION_NOT_AUTHORIZED_OR_REPLAY')
    require(not any(request.get(k) for k in ['accepted', 'promoted', 'binding_pass',
                'output', 'export', 'changes']), 'EXECUTION_OR_TEST_EVIDENCE_REQUIRED')
    if lock.get('codex_takeover'):
        take = lock['codex_takeover']
        require(not any(request.get(k) for k in ['render', 'photo_generation', 'training',
                'paid_compute_usd', 'automations', 'second_style', 'hidden_variants']),
                'RENDER_NOT_AUTHORIZED')
        if request.get('figma_write') or request.get('wordmark_image_tool'):
            require(take['status'] in ['VPD_CODEX_CHAZUO_AUTHORIZED_SOURCE_PROTECTED',
                    'VPD_CODEX_CHAZUO_REVISION_REQUIRED'] and
                    request.get('task_id') == take['task_id'] and
                    request.get('authorization') == take['authorization'] and
                    request.get('photo_protection') == take['photo_protection'],
                    'CONTINUATION_ACTION_CONFLICT')
            require(type(request.get('formal_version')) is int and
                    request['formal_version'] == take['budget']['formal_versions_used'] + 1 <= 3,
                    'REQUEST_BUDGET_EXCEEDED')
        return lock
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
