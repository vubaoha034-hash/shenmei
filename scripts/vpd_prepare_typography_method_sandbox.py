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
VALIDATOR = ROOT / 'visual_memory/vpd_p6_composition_state.py'
RESEARCH = ROOT / 'evidence/vpd/p1_typography_research_sandbox_v1/TYPOGRAPHY_CREATION_METHODS_RESEARCH_20260916.md'
PLAN = ROOT / 'evidence/vpd/p1_typography_research_sandbox_v1/TYPOGRAPHY_METHOD_SANDBOX_PLAN_V1.json'


def load(p): return json.loads(p.read_text(encoding='utf-8'))
def dump(p, o): p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p): return {'path': p.relative_to(ROOT).as_posix(), 'sha256': sha(p)}
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def blob(path): return subprocess.check_output(['git','rev-parse',f'HEAD:{path}'], cwd=ROOT, text=True).strip()
def eh(o): return hashlib.sha256(json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(',',':')).encode()).hexdigest()


def patch_validator():
    s = VALIDATOR.read_text(encoding='utf-8')
    action = '    "P1_EXECUTE_TYPOGRAPHY_METHOD_SANDBOX_TEST_01",\n'
    if 'P1_EXECUTE_TYPOGRAPHY_METHOD_SANDBOX_TEST_01' not in s:
        marker = '    "P1_PREPARE_HYBRID_TEXTURE_FINISH_PROBE",\n'
        if marker not in s: raise SystemExit('validator action marker missing')
        s = s.replace(marker, marker + action, 1)
    validation_marker = '    require(not set(cp["completed"]) & set(cp["incomplete"]), "COMPLETED_AND_INCOMPLETE")\n'
    if 'TYPOGRAPHY_SANDBOX_NOT_READY' not in s:
        block = '''    if action == "P1_EXECUTE_TYPOGRAPHY_METHOD_SANDBOX_TEST_01":\n        tr = lock["typography_repair"]\n        require(lock["status"] == "VPD_P1_TYPOGRAPHY_METHOD_SANDBOX_READY", "TYPOGRAPHY_SANDBOX_NOT_READY")\n        require(tr.get("status") == "TYPOGRAPHY_METHOD_SANDBOX_READY", "TYPOGRAPHY_SANDBOX_TYPOGRAPHY_STATE")\n        require(tr.get("phase") == "TYPOGRAPHY_METHOD_SANDBOX", "TYPOGRAPHY_SANDBOX_PHASE")\n        require(tr.get("sandbox_rule_promotion_allowed") is False, "TYPOGRAPHY_SANDBOX_PREMATURE_RULE_PROMOTION")\n        require(tr.get("sandbox_first_test") == "TYP-M01", "TYPOGRAPHY_SANDBOX_FIRST_TEST_DRIFT")\n        check_ref(root, tr["typography_method_research"])\n        check_ref(root, tr["typography_method_sandbox_plan"])\n        plan = read(root, tr["typography_method_sandbox_plan"]["path"])\n        require(plan["status"] == "FROZEN_SANDBOX_PLAN_NOT_RULE", "TYPOGRAPHY_SANDBOX_PLAN_STATUS")\n        require(plan["first_test"] == "TYP-M01", "TYPOGRAPHY_SANDBOX_PLAN_FIRST_TEST")\n        require(plan["rule_admission"]["automatic_promotion"] is False, "TYPOGRAPHY_SANDBOX_AUTO_PROMOTION")\n        require(tr.get("T2_allowed") is False and tr.get("P6_reintegration_allowed") is False, "TYPOGRAPHY_SANDBOX_PREMATURE_ADVANCE")\n\n'''
        if validation_marker not in s: raise SystemExit('validator tail marker missing')
        s = s.replace(validation_marker, block + validation_marker, 1)
    VALIDATOR.write_text(s, encoding='utf-8')


def main():
    lock = load(LOCK); cp = load(CP); adapter = load(ADAPTER); plan = load(PLAN)
    if lock.get('revision') != 52 or lock.get('next_required_action') != 'P1_PREPARE_HYBRID_TEXTURE_FINISH_PROBE':
        raise SystemExit('unexpected source task-lock state')
    if plan.get('status') != 'FROZEN_SANDBOX_PLAN_NOT_RULE' or plan.get('first_test') != 'TYP-M01':
        raise SystemExit('sandbox plan not frozen')
    if not RESEARCH.exists(): raise SystemExit('research record missing')

    patch_validator()
    recorded = now(); old_blob = blob('continuity/vpd/CURRENT_TASK_LOCK.json')
    rr = ref(RESEARCH); pr = ref(PLAN)
    before_state = lock['status']; before_next = lock['next_required_action']

    lock['revision'] = 53
    lock['preserved_prior_revision'] = {
      'revision': 52,
      'git_blob_sha': old_blob,
      'note': 'Revision 52 stopped the failed Chazuo V6 Figma-vector-only surface route and proposed a hybrid texture probe. User then required a broader typography-method research sandbox and prohibited untested methods from entering project rules.'
    }
    lock['current_stage'] = 'Typography creation research has been stored as non-authoritative sandbox evidence. No researched method is a VPD rule. A frozen sandbox plan now opens exactly one first test on 茶作 D: TYP-M01 centerline plus variable-width stroke reconstruction, monochrome skeleton only, with no leaves, texture, gradient or shadow. Formal nodes, Doufang, photography, T2 and P6 remain frozen.'
    lock['status'] = 'VPD_P1_TYPOGRAPHY_METHOD_SANDBOX_READY'
    lock['next_required_action'] = 'P1_EXECUTE_TYPOGRAPHY_METHOD_SANDBOX_TEST_01'
    lock['p6_allowed'] = False
    lock['completed_this_revision'] = [
      'stored professional typography/lettering/CJK/vector construction research as RESEARCH_ONLY_NOT_RULE',
      'stored a frozen sandbox plan with an explicit rule-admission firewall',
      'cancelled the immediate hybrid-texture probe as the next action before execution',
      'opened only TYP-M01 centerline plus variable-width stroke reconstruction for a bounded 茶-only monochrome test',
      'kept Doufang, formal Chazuo nodes, photography, T2, P6 reintegration and rule promotion frozen'
    ]
    lock['blockers'] = [
      'No typography research method is an approved VPD rule until a controlled actual-pixel test passes human review and the user explicitly approves promotion.',
      'T2 remains blocked until a title route achieves human visual acceptance.',
      'P6 reintegration and photo regeneration remain blocked; prior image gains are preserved.',
      'Candidate promotion, Commercial, Golden and Scale remain blocked.'
    ]
    tr = lock.get('typography_repair', {})
    tr = {**tr,
      'status': 'TYPOGRAPHY_METHOD_SANDBOX_READY',
      'phase': 'TYPOGRAPHY_METHOD_SANDBOX',
      'typography_method_research': rr,
      'typography_method_sandbox_plan': pr,
      'sandbox_rule_promotion_allowed': False,
      'sandbox_first_test': 'TYP-M01',
      'sandbox_first_test_scope': '茶 only; monochrome centerline plus variable-width construction; no leaves/texture/shadow/gradient; one visible output; zero hidden variants',
      'T2_allowed': False,
      'P6_reintegration_allowed': False,
      'next_required_action': 'P1_EXECUTE_TYPOGRAPHY_METHOD_SANDBOX_TEST_01'
    }
    lock['typography_repair'] = tr
    lock['updated_at'] = recorded
    dump(LOCK, lock); lock_sha = sha(LOCK)

    prev = None
    for line in LEDGER.read_text(encoding='utf-8').splitlines():
        o = json.loads(line); prev = {'event_id': o['event_id'], 'event_hash': o['event_hash']}
    event = {
      'schema_version': 'upcp-state-ledger-event/v1',
      'stream_id': 'commercial_design_pipeline',
      'event_id': 'EVT-VPD-P1-TYPOGRAPHY-METHOD-SANDBOX-READY-20260916-001',
      'event_type': 'TYPOGRAPHY_METHOD_RESEARCH_SANDBOX_READY',
      'task_id': lock['parent_active_task_id'],
      'project_id': lock['project_id'],
      'recorded_at': recorded,
      'material': True,
      'previous_event_id': prev['event_id'] if prev else None,
      'previous_event_hash': prev['event_hash'] if prev else None,
      'lock_sha256': lock_sha,
      'authorization': {
        'source': 'current controlling ChatGPT conversation',
        'authority': 'explicit user instruction',
        'instruction': 'Store the researched typography creation methods first; test them; failed/unproven methods are not allowed into project rules.'
      },
      'before': {'state': before_state, 'next_action': before_next},
      'after': {'state': lock['status'], 'next_action': lock['next_required_action']},
      'evidence': [rr['path'], pr['path']],
      'reason': 'The project is switching from reactive effect-tuning to a controlled typography-method sandbox. Research is quarantined from production rules until actual-pixel human validation.',
      'remote_authority': {'repository': lock['repository'], 'branch': lock['branch']}
    }
    event['event_hash'] = eh(event)
    with LEDGER.open('a', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(event, ensure_ascii=False, sort_keys=True, separators=(',',':')) + '\n')

    cp['sequence'] = max(int(cp.get('sequence', 0)) + 1, 75)
    cp['recorded_at'] = recorded
    cp['current_focus'] = lock['current_stage']
    for item in ['p1_typography_creation_method_research_sandbox', 'p1_typography_method_sandbox_plan']:
        if item not in cp['completed']: cp['completed'].append(item)
    cp['incomplete'] = [
      'p1_typography_method_sandbox_test_01',
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
      'status': tr['status'], 'phase': tr['phase'],
      'typography_method_research': rr,
      'typography_method_sandbox_plan': pr,
      'sandbox_rule_promotion_allowed': False,
      'sandbox_first_test': 'TYP-M01',
      'T2_allowed': False,
      'P6_reintegration_allowed': False,
      'next_required_action': lock['next_required_action']}
    dump(CP, cp)

    adapter['task_lock']['revision'] = 53
    adapter['task_lock']['sha256'] = lock_sha
    adapter['vpd_system_goal_authority']['checkpoint'] = lock['status']
    adapter['vpd_system_goal_authority']['next_required_action'] = lock['next_required_action']
    adapter['vpd_system_goal_authority']['render_allowed'] = False
    adapter['forward_commercial_pipeline']['status'] = 'PAUSED_FOR_P1_TYPOGRAPHY_METHOD_SANDBOX_TEST_01'
    adapter['forward_commercial_pipeline']['next_required_action'] = lock['next_required_action']
    adapter['change_authorities'].insert(0, {**pr, 'priority': 0, 'purpose': 'Current sandbox authority. Research methods are not rules; execute only TYP-M01 next and require human pixel review before any promotion.'})
    adapter['change_authorities'].insert(1, {**rr, 'priority': 1, 'purpose': 'Typography creation research record; non-authoritative and prohibited from automatic rule promotion.'})
    dump(ADAPTER, adapter)

    print(json.dumps({'status': lock['status'], 'revision': 53, 'checkpoint_sequence': cp['sequence'], 'next_required_action': lock['next_required_action'], 'research': rr, 'plan': pr, 'lock_sha256': lock_sha}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
