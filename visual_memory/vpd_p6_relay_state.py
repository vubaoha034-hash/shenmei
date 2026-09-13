"""P6 transport-only state profile. Does not grant rendering or visual acceptance."""
import hashlib
import json

from .vpd_task_lock import (LOCK_PATH, CHECKPOINT_PATH, PROJECT, PARENT,
                           read, path, require, check_ref, digest, evidence_bytes)

PROFILE = 'p6-figma-relay/v1'
FILE_KEY = 'uyDxOoN1iNDPpEHTKSUWg1'
TARGETS = [('12:3', 'DOUFANG_A_BASELINE', '12:4'),
           ('12:11', 'DOUFANG_B_DISTILLED', '12:12'),
           ('12:19', 'CHAZUO_A_BASELINE', '12:20'),
           ('12:27', 'CHAZUO_B_DISTILLED', '12:28')]
ACTIONS = {'RUN_LIVE_DOUFANG_B_RELAY', 'RUN_LIVE_CHAZUO_A_RELAY',
           'RUN_LIVE_CHAZUO_B_RELAY', 'P6_RELAY_BINDINGS_COMPLETE_STOP'}


def validate_p6_ledger(root, lock, cp, repair):
    """Preserve the explicitly audited legacy prefix, validate every new event.

    Three pre-existing invalid event hashes are disclosed, not rehashed or
    silently certified. The prefix is pinned as evidence at the repair commit.
    """
    raw = evidence_bytes(path(root, 'continuity/vpd/state_ledger/system_validation.jsonl'))
    lines = raw.splitlines(keepends=True)
    count = repair['legacy_ledger']['event_count']
    require(hashlib.sha256(b''.join(lines[:count])).hexdigest() == repair['legacy_ledger']['sha256'],
            'HISTORICAL_LEDGER_REWRITTEN')
    previous = json.loads(lines[count - 1])
    require(len(lines) > count, 'P6_LEDGER_EVENT_REQUIRED')
    for line in lines[count:]:
        event = json.loads(line)
        claimed = event.pop('event_hash')
        actual = hashlib.sha256(json.dumps(event, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        require(claimed == actual, 'LEDGER_HASH_MISMATCH')
        require(event['previous_event_id'] == previous['event_id'] and event['previous_event_hash'] == previous['event_hash'], 'LEDGER_PARENT_MISMATCH')
        previous = dict(event, event_hash=claimed)
    require(cp['ledger_tails']['system_validation'] == {k:previous[k] for k in ('event_id','event_hash')}, 'LEDGER_TAIL_MISMATCH')
    require(previous['lock_sha256'] == digest(path(root, LOCK_PATH)), 'LEDGER_STALE_LOCK')


def validate_p6_state(root):
    lock, cp = read(root, LOCK_PATH), read(root, CHECKPOINT_PATH)
    adapter = read(root, 'PROJECT_CONTROL_ADAPTER.json')
    require(lock['schema_version'] == 'vpd-current-task-lock/v1' and lock['state_profile'] == PROFILE, 'LOCK_SCHEMA')
    require(lock['project_id'] == cp['project_id'] == adapter['project_id'] == PROJECT, 'PROJECT_ID_MISMATCH')
    require(lock['parent_active_task_id'] == PARENT and cp['active_task_ids'] == [PARENT], 'PARENT_TASK_CHANGED')
    require(lock['repository'] == adapter['repository'] == 'vubaoha034-hash/shenmei', 'REPOSITORY_DRIFT')
    require(lock['branch'] == adapter['canonical_branch'] == 'visual-program-distillation-v2-photography-design-20260814', 'BRANCH_DRIFT')
    dispatch = adapter['task_lock']
    require(dispatch['path'] == adapter['task_registry_path'] == LOCK_PATH, 'COMPETING_TASK_INDEX')
    check_ref(root, dispatch)
    require(dispatch['revision'] == lock['revision'] >= 25 and cp['sequence'] >= 47, 'STALE_LOCK_REVISION')
    require(cp['task_lock'] == {'path':LOCK_PATH, 'sha256':digest(path(root, LOCK_PATH))}, 'STALE_CHECKPOINT_LOCK')
    require(cp['status'] == lock['status'] == adapter['vpd_system_goal_authority']['checkpoint'], 'STATE_STATUS_CONFLICT')
    action = lock['next_required_action']
    require(action in ACTIONS and action == cp['next_required_action'] == adapter['vpd_system_goal_authority']['next_required_action'], 'NEXT_ACTION_DRIFT')
    require(lock['render_allowed'] is False and adapter['vpd_system_goal_authority']['render_allowed'] is False, 'RENDER_NOT_AUTHORIZED')
    require(not set(cp['completed']) & set(cp['incomplete']), 'COMPLETED_AND_INCOMPLETE')
    repair_ref = lock['authority_repair']['record']
    check_ref(root, repair_ref)
    repair = read(root, repair_ref['path'])
    require(repair['scope'] == 'AUTHORITY_COMPATIBILITY_AND_P6_RELAY_ONLY', 'REPAIR_SCOPE_CHANGED')
    require(lock['authority_repair']['historical_ledger_status'] == 'PRESERVED_WITH_PREEXISTING_HASH_DEFECTS_NOT_RECERTIFIED', 'HISTORY_RECERTIFICATION')
    for ref in repair['preserved_state'].values():
        check_ref(root, ref)
    old = read(root, repair['preserved_state']['lock']['path'])
    require(lock['objective'] == old['objective'] and lock['family'] == old['family'], 'OBJECTIVE_DRIFT')
    require(lock['mechanism_transfer_verdict'] == old['mechanism_transfer_verdict'], 'UNSUPPORTED_PROMOTION')
    require(lock['capsule'] == old['capsule'] and not lock['capsule']['promoted'], 'CAPSULE_IDENTITY_DRIFT')
    require(lock['execution_boundary'] == old['execution_boundary'], 'P6_BOUNDARY_WEAKENED')
    check_ref(root, repair['immutable_baseline'])
    for name, expected in read(root, repair['immutable_baseline']['path'])['files'].items():
        require(digest(path(root, name)) == expected, 'FROZEN_BYTES_CHANGED:' + name)
    for ref in repair['p6_input_evidence'].values():
        check_ref(root, ref)
    wf = lock['workflow']['document']
    check_ref(root, wf)
    require(cp['workflow'] == wf == {k:adapter['workflow'][k] for k in ('path','sha256')}, 'WORKFLOW_REFERENCE_CONFLICT')
    require(lock['workflow']['focus_stage'] == 'P6' and lock['workflow']['status_authority'] == LOCK_PATH, 'WORKFLOW_STAGE_DRIFT')
    for name in ('START_HERE.md', 'AGENTS.md'):
        entry = path(root, name).read_text(encoding='utf-8')
        require(entry.count('<!-- VPD_TASK_LOCK_ENTRY_V1 -->') == 1 and LOCK_PATH in entry and wf['path'] in entry, 'ENTRYPOINT_NOT_UNIQUE')
    p6 = lock['p6_integrated_design']
    require([(f['id'], f['name'], f['photo']) for f in p6['frames']] == TARGETS, 'P6_TARGET_DRIFT')
    require(p6['frame_size'] == [2400,3200] and p6['figma_file_key'] == FILE_KEY, 'P6_GEOMETRY_DRIFT')
    require(all(f['locked'] is False for f in p6['frames']), 'PHOTO_RELOCK_FORBIDDEN')
    require(p6['equal_budget'] == old['p6_integrated_design']['equal_budget'], 'P6_BUDGET_DRIFT')
    require(p6['semantic_raw_asset_identity_locked'] is True and p6['figma_photo_node_locked_required'] is False, 'ASSET_LOCK_DRIFT')
    require(p6['final_pixel_validation_allowed'] is False and cp['p6']['final_pixel_validation_allowed'] is False, 'PIXEL_ACCEPTANCE_NOT_AUTHORIZED')
    frames = p6['frames']
    count = sum(f['bound'] is True for f in frames)
    require([f['bound'] for f in frames] == [True]*count + [False]*(4-count), 'RELAY_ORDER_VIOLATION')
    require(count == p6['bound_count'] == cp['p6']['real_images_bound_count'], 'P6_COUNT_CONFLICT')
    require(p6['remaining_bindings'] == [f['photo'] for f in frames if not f['bound']], 'P6_REMAINING_CONFLICT')
    require(cp['p6']['photo_nodes'] == {f['photo']:{'bound':f['bound'],'locked':False} for f in frames}, 'P6_MIRROR_CONFLICT')
    require(action == ['RUN_LIVE_DOUFANG_B_RELAY','RUN_LIVE_CHAZUO_A_RELAY','RUN_LIVE_CHAZUO_B_RELAY','P6_RELAY_BINDINGS_COMPLETE_STOP'][count-1], 'RELAY_ORDER_VIOLATION')
    relay = lock['figma_upload_relay']
    require(relay['secret_present_verified'] is True and relay['required_secret'] == 'VPD_FIGMA_RELAY_PRIVATE_KEY_B64', 'SECRET_NOT_VERIFIED')
    check_ref(root, relay['secret_metadata_receipt'])
    require(relay['public_certificate_sha256'] == digest(path(root, relay['public_certificate'])), 'RELAY_CERT_CHANGED')
    require(relay['private_key_committed'] is False, 'PRIVATE_KEY_EXPOSURE')
    for f in frames[1:count]:
        binding = lock['relay_bindings'][f['photo']]
        check_ref(root, binding['receipt']); check_ref(root, binding['readback'])
        receipt, readback = read(root, binding['receipt']['path']), read(root, binding['readback']['path'])
        require(receipt['status'] == 'UPLOAD_PASS' and receipt['node_id'] == f['photo'], 'RELAY_RECEIPT_REQUIRED')
        require(receipt['source_sha256'] == repair['frozen_source_sha256'][f['photo']], 'RELAY_SOURCE_HASH_MISMATCH')
        require(readback['node_id'] == f['photo'] and readback['locked'] is False and readback['scaleMode'] == 'FILL' and readback['fills_type'] == 'IMAGE', 'FIGMA_READBACK_FAILED')
        require(readback['imageHash'] == receipt['response']['imageHash'] and readback['imageHash'], 'FIGMA_IMAGE_HASH_MISMATCH')
        require(readback['non_photo_nodes_unchanged'] is True and readback['screenshot_verified'] is True and len(readback['screenshot_sha256']) == 64, 'FIGMA_VERIFICATION_REQUIRED')
    require(set(lock['relay_bindings']) == {f['photo'] for f in frames[1:count]}, 'UNVERIFIED_BINDING_CLAIM')
    validate_p6_ledger(root, lock, cp, repair)
    return lock, cp
