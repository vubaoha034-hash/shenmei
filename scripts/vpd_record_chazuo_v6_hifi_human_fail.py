#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / 'continuity/vpd/CURRENT_TASK_LOCK.json'
CP = ROOT / 'continuity/vpd/LATEST_CHECKPOINT.json'
ADAPTER = ROOT / 'PROJECT_CONTROL_ADAPTER.json'
LEDGER = ROOT / 'continuity/vpd/state_ledger/commercial_design_pipeline.jsonl'
SOURCE = ROOT / 'evidence/vpd/p1_typography_repair_v7/CHAZUO_D_MOTHER_FAITHFUL_VECTOR_TEST_20260915.json'
EVID = ROOT / 'evidence/vpd/p1_typography_repair_v7/CHAZUO_V6_HIFI_HUMAN_REJECTION_20260916.json'


def load(p): return json.loads(p.read_text(encoding='utf-8'))
def dump(p, o): p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p): return {'path': p.relative_to(ROOT).as_posix(), 'sha256': sha(p)}
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')
def blob(path): return subprocess.check_output(['git', 'rev-parse', f'HEAD:{path}'], cwd=ROOT, text=True).strip()
def eh(o): return hashlib.sha256(json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def main():
    lock = load(LOCK); cp = load(CP); adapter = load(ADAPTER); source = load(SOURCE)
    if lock.get('revision') != 51 or lock.get('next_required_action') != 'P1_WAIT_HUMAN_V6_FIGMA_VECTOR_REVIEW':
        raise SystemExit('unexpected source task-lock state')
    if source.get('hifi_surface_test', {}).get('figma_test_frame_id') != '118:2':
        raise SystemExit('unexpected V7 high-fidelity source evidence')

    recorded = now(); old_blob = blob('continuity/vpd/CURRENT_TASK_LOCK.json')
    before_state = lock.get('status'); before_next = lock.get('next_required_action')

    evidence = {
      'schema_version': 'vpd-chazuo-v6-hifi-human-rejection/v1',
      'recorded_at': recorded,
      'status': 'HUMAN_FAIL_STOP_CURRENT_VECTOR_ONLY_SURFACE_ROUTE',
      'source_test': ref(SOURCE),
      'figma': {
        'file_key': 'uyDxOoN1iNDPpEHTKSUWg1',
        'test_frame_id': '118:2',
        'geometry_changed_by_test': False,
        'leaf_positions_changed_by_test': False,
        'leaf_scale_changed_by_test': False,
        'leaf_overlap_changed_by_test': False
      },
      'human_feedback_exact': [
        '叶子比以前好了一点点。',
        '右边的low还是没有。',
        '没达到不值得。'
      ],
      'human_settlement': {
        'leaf_visibility': 'SLIGHT_IMPROVEMENT_ONLY_NOT_ENOUGH',
        'premium_surface_quality': 'FAIL_LOW_FLAT_FEELING_PERSISTS',
        'worth_continuing_same_route': False,
        'title_gate': 'FAIL',
        'commercial_readiness': 'FAIL',
        'T2_allowed': False,
        'P6_reintegration_allowed': False
      },
      'route_decision': {
        'stop': 'Figma-vector-only microtexture, outline, shadow, gradient and leaf-strengthening refinements on frame 118:2',
        'preserve': 'V6 geometry and six-leaf placement/scale/overlap as research evidence only; do not treat as approved production wordmark',
        'do_not_do': [
          'do not keep stacking more vector effects or aesthetic rules onto the same failed route',
          'do not move or redesign the six leaves merely to compensate for surface-quality failure',
          'do not unlock T2 or P6 from a correctness-only or editability-only result'
        ],
        'next_required_action': 'P1_PREPARE_HYBRID_TEXTURE_FINISH_PROBE',
        'next_probe_scope': 'One bounded alternative route only: preserve the exact editable V6 vector geometry as underlay, create a separate pixel-faithful material/texture finish outside the Figma-vector-only effect stack, then reimport/overlay for final-pixel comparison against the mother. No structural redesign in this probe.'
      },
      'diagnosis': {
        'problem_type': 'TASTE_PROBLEM_NOT_CORRECTNESS_PROBLEM',
        'reason': 'The vector route now preserves the intended structure and improves leaf visibility slightly, but it still does not reproduce the mother image material richness or premium surface finish. Additional Figma-only effect tuning is therefore low-leverage and risks rule/effect stacking without solving the visible quality gap.',
        'charter_alignment': 'Stop adding aesthetic micro-rules after repeated taste failure; change the rendering route rather than keep engineering the same failed surface treatment.'
      }
    }
    dump(EVID, evidence); er = ref(EVID); sr = ref(SOURCE)

    lock['revision'] = 52
    lock['preserved_prior_revision'] = {
      'revision': 51,
      'git_blob_sha': old_blob,
      'note': 'Revision 51 preserved the formal V6 vector-review gate. A later non-formal Chazuo V6 high-fidelity surface test was recorded without promoting the task lock; this revision settles its human verdict as FAIL and stops that vector-only surface route.'
    }
    lock['current_stage'] = 'Human review of the Chazuo V6 geometry-frozen high-fidelity Figma surface test is FAIL: leaf visibility improved only slightly, while the right-side result still reads low/flat and is not worth continuing. Stop the current Figma-vector-only surface micro-refinement route. Preserve the exact V6 geometry and six-leaf relationships as research evidence only; T2 and P6 remain blocked. Prepare one bounded hybrid texture-finish probe instead of stacking more Figma vector effects.'
    lock['status'] = 'VPD_P1_CHAZUO_V6_HIFI_SURFACE_HUMAN_FAIL_ROUTE_STOP'
    lock['next_required_action'] = 'P1_PREPARE_HYBRID_TEXTURE_FINISH_PROBE'
    lock['p6_allowed'] = False
    lock['completed_this_revision'] = [
      'recorded the human verdict that leaf visibility improved only slightly and remains insufficient',
      'recorded the human verdict that the right-side Figma result still reads low/flat and does not justify continuing the same route',
      'stopped further Figma-vector-only surface micro-refinement on Chazuo frame 118:2',
      'preserved V6 geometry and the original six-leaf placement/scale/overlap as research-only evidence',
      'kept T2, P6 reintegration, photography and candidate promotion blocked',
      'set the next step to preparation of one bounded hybrid texture-finish probe rather than more vector-effect stacking'
    ]
    lock['blockers'] = [
      'Chazuo V6 high-fidelity Figma surface route is human-rejected; frame 118:2 is not an approved production wordmark.',
      'T2 remains blocked until a title route achieves human visual acceptance, not merely structural correctness or editability.',
      'P6 reintegration and photo regeneration remain blocked; prior image gains are preserved.',
      'Candidate promotion, Commercial, Golden and Scale remain blocked.'
    ]
    tr = lock.get('typography_repair', {})
    tr = {**tr,
          'status': 'CHAZUO_V6_HIFI_SURFACE_HUMAN_FAIL_ROUTE_STOP',
          'phase': 'V6_SURFACE_ROUTE_RESET',
          'v7_hifi_surface_test': sr,
          'v7_hifi_surface_human_rejection': er,
          'current_vector_only_surface_route': 'STOPPED_NOT_WORTH_CONTINUING',
          'selected_direction_geometry': {'茶作': 'V6 full-concept geometry preserved as research-only'},
          'T2_allowed': False,
          'P6_reintegration_allowed': False,
          'next_required_action': 'P1_PREPARE_HYBRID_TEXTURE_FINISH_PROBE'}
    lock['typography_repair'] = tr
    lock['updated_at'] = recorded
    dump(LOCK, lock); lock_sha = sha(LOCK)

    prev = None
    for line in LEDGER.read_text(encoding='utf-8').splitlines():
        o = json.loads(line); prev = {'event_id': o['event_id'], 'event_hash': o['event_hash']}
    event = {
      'schema_version': 'upcp-state-ledger-event/v1',
      'stream_id': 'commercial_design_pipeline',
      'event_id': 'EVT-VPD-P1-CHAZUO-V6-HIFI-HUMAN-FAIL-20260916-001',
      'event_type': 'CHAZUO_V6_HIFI_SURFACE_HUMAN_FAIL_ROUTE_STOP',
      'task_id': lock['parent_active_task_id'],
      'project_id': lock['project_id'],
      'recorded_at': recorded,
      'material': True,
      'previous_event_id': prev['event_id'] if prev else None,
      'previous_event_hash': prev['event_hash'] if prev else None,
      'lock_sha256': lock_sha,
      'authorization': {
        'source': 'current controlling ChatGPT conversation',
        'authority': 'explicit human visual verdict',
        'feedback': evidence['human_feedback_exact']
      },
      'before': {'state': before_state, 'next_action': before_next},
      'after': {'state': lock['status'], 'next_action': lock['next_required_action']},
      'evidence': [er['path'], sr['path']],
      'reason': 'Human review says the leaves are only slightly better while the premium-quality gap remains. The same Figma-vector-only surface route is therefore stopped as a taste failure; no further effect/rule stacking is authorized.',
      'remote_authority': {'repository': lock['repository'], 'branch': lock['branch']}
    }
    event['event_hash'] = eh(event)
    with LEDGER.open('a', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(event, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n')

    cp['sequence'] = max(int(cp.get('sequence', 0)) + 1, 74)
    cp['recorded_at'] = recorded
    cp['current_focus'] = lock['current_stage']
    for item in ['p1_chazuo_v6_hifi_surface_test', 'p1_chazuo_v6_hifi_surface_human_fail_route_stop']:
        if item not in cp['completed']: cp['completed'].append(item)
    cp['incomplete'] = [
      'p1_hybrid_texture_finish_probe',
      'p1_typography_support_hierarchy_bench',
      'p6_reintegration_after_typography_repair',
      'candidate_promotion',
      'second_style_family_validation',
      'golden',
      'scale'
    ]
    cp['blocked'] = list(lock['blockers'])
    cp['next_required_action'] = lock['next_required_action']
    cp['status'] = lock['status']
    cp['task_lock'] = {'path': 'continuity/vpd/CURRENT_TASK_LOCK.json', 'sha256': lock_sha}
    cp['ledger_tails'] = {'commercial_design_pipeline': {'event_id': event['event_id'], 'event_hash': event['event_hash']}}
    cp['typography_repair'] = {**cp.get('typography_repair', {}),
                               'status': tr['status'],
                               'phase': tr['phase'],
                               'v7_hifi_surface_test': sr,
                               'v7_hifi_surface_human_rejection': er,
                               'T2_allowed': False,
                               'P6_reintegration_allowed': False,
                               'next_required_action': lock['next_required_action']}
    dump(CP, cp)

    adapter['task_lock']['revision'] = 52
    adapter['task_lock']['sha256'] = lock_sha
    adapter['vpd_system_goal_authority']['checkpoint'] = lock['status']
    adapter['vpd_system_goal_authority']['next_required_action'] = lock['next_required_action']
    adapter['vpd_system_goal_authority']['render_allowed'] = False
    adapter['forward_commercial_pipeline']['status'] = 'PAUSED_FOR_P1_HYBRID_TEXTURE_FINISH_PROBE_PREPARATION'
    adapter['forward_commercial_pipeline']['next_required_action'] = lock['next_required_action']
    adapter['change_authorities'].insert(0, {**er, 'priority': 0, 'purpose': 'Current human authority: Chazuo V6 high-fidelity Figma vector-only surface route failed and is stopped; prepare one bounded hybrid texture-finish probe before any T2 or P6.'})
    dump(ADAPTER, adapter)

    print(json.dumps({'status': lock['status'], 'revision': 52, 'checkpoint_sequence': cp['sequence'], 'next_required_action': lock['next_required_action'], 'evidence': er, 'lock_sha256': lock_sha}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
