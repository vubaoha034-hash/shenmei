"""Scoped reference study inside the existing task; never a poster release gate."""
from .vpd_task_lock import require, check_ref, read

REFERENCE = '9a29fbdc7dd908017924bed270e8dfe18351519eed3fa7bc7001789f2a383414'
PHASES = {'REFERENCE_STUDY_ACTIVE', 'REFERENCE_STUDY_DELIVERED', 'REFERENCE_STUDY_ARCHIVE_BLOCKED'}


def validate_study(root, unit):
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
