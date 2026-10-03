"""Synthetic receipt tests; no synthetic verdict is runtime review evidence."""
import copy
import hashlib
import json

import pytest

from visual_memory.vpd_task_lock import TaskLockError, digest
from visual_memory.vpd_locked_mainline_state import TAKEOVER_TASK, _validate_isolated_pixel_review


def save(root, name, data):
    p = root / name
    p.write_text(json.dumps(data, ensure_ascii=False) + '\n', encoding='utf-8')
    return {'path': name, 'sha256': digest(p)}


@pytest.fixture
def records(tmp_path):
    out = tmp_path / 'SYNTHETIC_EXPORT_BYTES_NOT_RUNTIME.png'
    out.write_bytes(b'SYNTHETIC_BYTES_FOR_METADATA_BINDING_ONLY')
    exported = {'path': out.name, 'sha256': digest(out)}
    hashes = [hashlib.sha256(n.encode()).hexdigest() for n in ['SYNTHETIC_P', 'SYNTHETIC_N', 'SYNTHETIC_R']]
    hashes.append(exported['sha256'])
    ids = ['P', 'N', 'R', 'T']
    reads = [{'neutral_id': n, 'sha256': h, 'tool': 'view_image', 'path': '/SYNTHETIC/' + n + '.png'}
             for n, h in zip(ids, hashes)]
    prompt_sha = hashlib.sha256(b'SYNTHETIC_NEUTRAL_PROMPT').hexdigest()
    raw = {'thread_id': 'SYNTHETIC_THREAD_NOT_RUNTIME', 'tool_reads': reads, 'extra_tool_reads': [],
           'source_project_context_reads': [], 'raw_rollout_sha256': hashlib.sha256(b'SYNTHETIC_RAW').hexdigest()}
    spawn = {'thread_id': raw['thread_id'], 'fork_turns': 'none', 'history_inherited': False,
             'initial_prompt_sha256': prompt_sha, 'actual_model': 'gpt-6.1-sol',
             'actual_reasoning_effort': 'max'}
    evidence = {'thread_id': raw['thread_id'], 'turn_context': {'model': 'gpt-6.1-sol', 'reasoning_effort': 'max'},
                'initial_prompt_sha256': prompt_sha, 'tool_reads': reads}
    amendment = {'task_id': TAKEOVER_TASK, 'from_carrier': 'FRESH_EXTERNAL_CODEX_EXEC',
                 'to_carrier': 'FRESH_FORK_NONE_PIXEL_AGENT', 'prior_failures_preserved': True,
                 'source': {'kind': 'CURRENT_HUMAN_USER_MESSAGE'},
                 'failure_evidence': save(tmp_path, 'SYNTHETIC_FAILURES.json', {'failures': ['SYNTHETIC']})}
    audit = {'schema_version': 'vpd-isolated-pixel-review-audit/v1', 'verified': True,
             'carrier': 'FRESH_FORK_NONE_PIXEL_AGENT', 'fork_turns': 'none', 'history_inherited': False,
             'resumed_or_history_forked': False, 'source_project_context_read': False,
             'fresh_agent': True, 'completed': True, 'actual_model': 'gpt-6.1-sol',
             'actual_reasoning_effort': 'max', 'attachments_verified': ids,
             'tool_scope_violations': [], 'initial_prompt_sha256': prompt_sha}
    review = {'task_id': TAKEOVER_TASK, 'version': 1, 'export': exported, 'reviewer': raw['thread_id'],
              'verdict': 'AI_PASS', 'human_verdict': 'HIDDEN_PENDING', 'personal_fit': None,
              'pixels_seen': ids, 'input_bindings': [{'neutral_id': n, 'sha256': h} for n, h in zip(ids, hashes)],
              'observations': [{'region': 'SYNTHETIC_REGION_' + str(n), 'evidence': 'SYNTHETIC_OBSERVATION'}
                               for n in range(5)]}
    return tmp_path, exported, {'raw': raw, 'spawn': spawn, 'evidence': evidence,
                               'amendment': amendment, 'audit': audit, 'review': review}


def seal(root, data):
    data['evidence']['raw_tool_read_audit'] = save(root, 'SYNTHETIC_RAW_READ_AUDIT.json', data['raw'])
    data['evidence']['spawn_receipt'] = save(root, 'SYNTHETIC_SPAWN.json', data['spawn'])
    data['audit']['evidence'] = save(root, 'SYNTHETIC_EXECUTION_EVIDENCE.json', data['evidence'])
    data['audit']['carrier_amendment'] = save(root, 'SYNTHETIC_CARRIER_AMENDMENT.json', data['amendment'])
    data['review']['isolation_audit'] = save(root, 'SYNTHETIC_ISOLATION_AUDIT.json', data['audit'])
    return save(root, 'SYNTHETIC_REVIEW.json', data['review'])


def test_verified_fork_none_metadata_is_accepted_without_claiming_human_pass(records):
    root, exported, data = records
    ref = seal(root, data)
    assert _validate_isolated_pixel_review(root, ref, 1, exported) == data['review']
    assert data['review']['human_verdict'] == 'HIDDEN_PENDING'


def test_parallel_image_completion_order_preserves_exact_unique_bindings(records):
    root, exported, data = records
    reordered = [data['raw']['tool_reads'][i] for i in [2, 0, 3, 1]]
    data['raw']['tool_reads'] = reordered
    data['evidence']['tool_reads'] = reordered
    ref = seal(root, data)
    assert _validate_isolated_pixel_review(root, ref, 1, exported) == data['review']


def test_duplicate_image_cannot_replace_missing_peer_at_four_markers(records):
    root, exported, data = records
    duplicated = [data['raw']['tool_reads'][i] for i in [0, 0, 2, 3]]
    data['raw']['tool_reads'] = duplicated
    data['evidence']['tool_reads'] = duplicated
    ref = seal(root, data)
    with pytest.raises(TaskLockError, match='REVIEW_ACTUAL_TOOL_READS_REQUIRED'):
        _validate_isolated_pixel_review(root, ref, 1, exported)


@pytest.mark.parametrize('case,reason', [
    ('missing_image', 'PIXEL_REVIEW_EVIDENCE_REQUIRED'),
    ('wrong_export', 'PIXEL_REVIEW_EVIDENCE_REQUIRED'),
    ('duplicate_attachment', 'PIXEL_REVIEW_EVIDENCE_REQUIRED'),
    ('unknown_verdict', 'PIXEL_REVIEW_EVIDENCE_REQUIRED'),
    ('human_pass', 'PIXEL_REVIEW_EVIDENCE_REQUIRED'),
    ('observations', 'PIXEL_REVIEW_EVIDENCE_REQUIRED'),
    ('unverified', 'REVIEW_ISOLATION_EVIDENCE_REQUIRED'),
    ('unknown_model', 'REVIEW_ISOLATION_EVIDENCE_REQUIRED'),
    ('wrong_effort', 'REVIEW_ISOLATION_EVIDENCE_REQUIRED'),
    ('history', 'REVIEW_ISOLATION_EVIDENCE_REQUIRED'),
    ('project_read', 'REVIEW_ISOLATION_EVIDENCE_REQUIRED'),
    ('extra_tool', 'REVIEW_ACTUAL_TOOL_READS_REQUIRED'),
    ('wrong_tool_hash', 'REVIEW_ACTUAL_TOOL_READS_REQUIRED'),
    ('missing_spawn', 'REVIEW_SPAWN_EVIDENCE_REQUIRED'),
])
def test_review_claims_need_real_matching_evidence_after_resealing(records, case, reason):
    root, exported, data = records
    if case == 'missing_image':
        data['review']['pixels_seen'].pop()
    elif case == 'wrong_export':
        data['review']['input_bindings'][-1]['sha256'] = '0' * 64
    elif case == 'duplicate_attachment':
        data['review']['input_bindings'][1]['sha256'] = data['review']['input_bindings'][0]['sha256']
    elif case == 'unknown_verdict':
        data['review']['verdict'] = 'UNKNOWN_CANNOT_EVALUATE'
    elif case == 'human_pass':
        data['review']['human_verdict'] = 'PASSED'
    elif case == 'observations':
        data['review']['observations'] = ['looks good']
    elif case == 'unverified':
        data['audit']['verified'] = False
    elif case == 'unknown_model':
        data['audit']['actual_model'] = 'UNKNOWN'
    elif case == 'wrong_effort':
        data['audit']['actual_reasoning_effort'] = 'UNKNOWN'
    elif case == 'history':
        data['audit']['history_inherited'] = True
    elif case == 'project_read':
        data['audit']['source_project_context_read'] = True
    elif case == 'extra_tool':
        data['raw']['extra_tool_reads'] = [{'tool': 'exec_command', 'path': 'AGENTS.md'}]
    elif case == 'wrong_tool_hash':
        data['evidence']['tool_reads'] = copy.deepcopy(data['evidence']['tool_reads'])
        data['evidence']['tool_reads'][-1]['sha256'] = '0' * 64
    elif case == 'missing_spawn':
        data['spawn']['thread_id'] = 'DIFFERENT_SYNTHETIC_THREAD'
    ref = seal(root, data)
    with pytest.raises(TaskLockError, match=reason):
        _validate_isolated_pixel_review(root, ref, 1, exported)


def test_hashed_audit_cannot_be_modified_in_place(records):
    root, exported, data = records
    ref = seal(root, data)
    (root / data['review']['isolation_audit']['path']).write_bytes(b'{"verified":true}\n')
    with pytest.raises(TaskLockError, match='EVIDENCE_HASH_MISMATCH'):
        _validate_isolated_pixel_review(root, ref, 1, exported)
