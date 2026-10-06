"""TEST_ONLY S6 guard fixtures; passing tests are never runtime design receipts."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from visual_memory import vpd_reference_typography_study as study
from visual_memory.vpd_locked_mainline_state import validate_locked_request
from visual_memory.vpd_task_lock import LOCK_PATH, TaskLockError, digest

ROOT = Path(__file__).resolve().parents[1]
TASK = 'VPD-CHAZUO-CODEX-COMPLETE-POSTER-20261003-01'
UNIT = 'CHAZUO_APPROVED_SOURCE_TYPOGRAPHY_20261003_R1'


def save(root, path, value):
    dest = root / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return {'path': path, 'sha256': digest(dest)}


class FailedLocalMethodFollowupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='.s6-test-', dir=ROOT)
        self.root = Path(self.temp.name).resolve()
        # Required before TemporaryDirectory performs recursive Windows cleanup.
        self.assertTrue(self.root.is_relative_to(ROOT.resolve()))
        self.addCleanup(self.temp.cleanup)
        self.lock = json.loads((ROOT / LOCK_PATH).read_text(encoding='utf-8'))
        self.unit = self.lock['codex_takeover']['worker_continuation']
        self.transfer = self.unit['content_transfer_experiment']
        self.transfer['attempts'] = self.transfer['attempts'][:5]
        self.transfer.pop('human_local_followup_allocation', None)
        self.transfer.pop('reference_grain_method_allocation', None)
        self.base = study._load(ROOT, self.transfer['human_local_repair_allocation'])
        # The immutable S5 artifact is the basis even after Root arms or completes S6.
        self.review = json.loads((ROOT / study.S5_FAILED_REVIEW).read_text(encoding='utf-8'))
        if len(self.transfer['attempts']) == 4:
            export_path = '.liu-visual-private/liuxiansheng_transfer_20261005/FIGMA_COMPLETE_S5.png'
            self.assertEqual(digest(ROOT / export_path), self.review['study_export_sha256'])
            # Root owns production state; this fifth attempt exists only in the fixture.
            self.transfer['attempts'].append({
                'kind': 'TARGETED_REPAIR',
                'export': {'path': export_path, 'sha256': self.review['study_export_sha256']},
                'repair_basis': self.base['feedback'], 'test_fixture_only': True,
            })
        self.assertEqual(len(self.transfer['attempts']), 5)
        self.audit_path = self.review['isolation_audit']['path']
        self.audit = study._load(ROOT, self.review['isolation_audit'])
        self.manifest_path = self.audit['reviewed_call_manifest']['path']
        self.manifest = study._load(ROOT, self.audit['reviewed_call_manifest'])
        self.review['test_fixture_only'] = True
        self.audit['test_fixture_only'] = True
        self.manifest['test_fixture_only'] = True
        self.grant = {
            'schema_version': 'vpd-content-transfer-failed-local-method-followup/v1',
            'scope': study.TRANSFER_SCOPE, 'task_id': TASK, 'work_unit_id': UNIT,
            'authorization': self.transfer['authorization'], 'copy_manifest': self.transfer['copy_manifest'],
            'continuous_repair_authorization': study.CONTINUOUS_AUTH,
            'human_feedback': self.base['feedback'],
            'base_allocation': self.transfer['human_local_repair_allocation'],
            'prior_failed_export': self.transfer['attempts'][4]['export'],
            'protected_photo_sha256': study.PROTECTED_PHOTO_SHA,
            'image_guide': self.transfer['supplemental_image_guide']['export'],
            'attempt_budget': {'base_attempts': 5, 'total_max': 6, 'method_repairs_max': 1},
            'limits': study.HUMAN_LOCAL_LIMITS.copy(), 'real_current_task_actor': 'ROOT_ONLY',
            'human_acceptance': 'PENDING', 'allocation_is_not_human_stop_condition': True,
            'method_change_reason': 'TEST_ONLY: verified S5 FAIL triggers one same-direction local method repair.',
            'test_fixture_only': True,
        }
        self.reseal()
        original_load = study._load
        verified_root_receipts = {}

        def isolated_load(root, ref):
            target = self.root if isinstance(ref, dict) and (self.root / ref['path']).exists() else ROOT
            if target == ROOT and isinstance(ref, dict):
                key = (ref.get('path'), ref.get('sha256'))
                if key not in verified_root_receipts:
                    verified_root_receipts[key] = original_load(ROOT, ref)
                return copy.deepcopy(verified_root_receipts[key])
            return original_load(target, ref)

        loader_patch = patch.object(study, '_load', isolated_load)
        loader_patch.start()
        self.addCleanup(loader_patch.stop)
        auth = study._load(ROOT, self.transfer['authorization'])
        self.request = {
            'intent': 'TARGETED_REPAIR', 'attempt_count': 5, 'repair_basis': self.grant['prior_failed_review'],
            'figma_write': True, 'protected_photo_sha256': study.PROTECTED_PHOTO_SHA,
            'lock_sha256': digest(ROOT / LOCK_PATH), 'action': self.lock['next_required_action'],
            'actor': 'ROOT_EXECUTOR', 'work_unit_id': UNIT, 'task_id': TASK,
            'authorization': self.transfer['authorization'], 'copy_manifest': self.transfer['copy_manifest'],
            'reference_sha256': study.REFERENCE, 'study_only': True,
            'file_key': auth['allowed_figma_page']['file_key'], 'page_id': auth['allowed_figma_page']['page_id'],
            'new_frame_name': 'LIUXIANSHENG_CONTENT_TRANSFER_S6_TEST_ONLY',
            'existing_node_mutations': [], 'protected_poster_node': '402:2',
        }
        self.original = copy.deepcopy((self.grant, self.review, self.audit, self.manifest))

    def reseal(self):
        self.audit['reviewed_call_manifest'] = save(self.root, self.manifest_path, self.manifest)
        self.review['isolation_audit'] = save(self.root, self.audit_path, self.audit)
        self.grant['prior_failed_review'] = save(self.root, study.S5_FAILED_REVIEW, self.review)
        self.transfer['human_local_followup_allocation'] = save(
            self.root, study.HUMAN_LOCAL_FOLLOWUP_ALLOCATION_AUTH, self.grant)
        if hasattr(self, 'request'):
            self.request['repair_basis'] = self.grant['prior_failed_review']

    def reset(self):
        self.grant, self.review, self.audit, self.manifest = copy.deepcopy(self.original)
        self.reseal()

    def test_verified_failed_s5_opens_exactly_one_native_root_write(self):
        old_attempts = copy.deepcopy(self.transfer['attempts'])
        old_budget = copy.deepcopy(self.unit['budget'])
        self.assertEqual(study.transfer_attempt_limit(self.transfer, ROOT), 6)
        self.assertEqual(study.available_guide_calls(self.unit, ROOT), 0)
        study.validate_transfer_write(ROOT, self.transfer, self.request)
        self.unit['phase'] = 'REFERENCE_STUDY_ACTIVE'
        self.assertIs(validate_locked_request(ROOT, self.request, self.lock), self.lock)
        self.assertEqual(self.transfer['attempts'], old_attempts)
        self.assertEqual(self.unit['budget'], old_budget)
        self.assertEqual(self.base['attempt_budget'], {'base_attempts': 4, 'total_max': 5, 'local_repairs_max': 1})

    def test_missing_followup_allocation_exhausts_existing_five_attempts(self):
        self.transfer.pop('human_local_followup_allocation')
        self.assertEqual(study.transfer_attempt_limit(self.transfer, ROOT), 5)
        with self.assertRaisesRegex(TaskLockError, 'ATTEMPT_BUDGET_EXHAUSTED'):
            study.validate_transfer_write(ROOT, self.transfer, self.request)

    def test_positive_review_and_wrong_export_cannot_authorize_followup(self):
        for field, value in [
            ('verdict', 'CONTENT_TRANSFER_PASS_WITH_LIMITATIONS'),
            ('verdict', 'CONTENT_TRANSFER_AI_FAIL'),
            ('study_export_sha256', '0' * 64),
            ('reference_sha256', '0' * 64),
            ('scope', 'TEA_FORMAL_RELEASE'),
            ('actual_pixels_seen', False),
            ('human_acceptance', 'ACCEPTED'),
            ('evidence_class', 'SYNTHETIC_NOT_RUNTIME_EVIDENCE'),
        ]:
            with self.subTest(field=field, value=value):
                self.reset()
                self.review[field] = value
                self.reseal()
                with self.assertRaisesRegex(TaskLockError, 'ACTUAL_REPAIR_BASIS_REQUIRED'):
                    study.transfer_attempt_limit(self.transfer, ROOT)

    def test_review_isolation_and_exact_two_image_runtime_are_required(self):
        mutations = [
            ('verified', False), ('history_inherited', True), ('fork_turns', 'all'),
            ('actual_model', 'gpt-6-astra'), ('actual_reasoning_effort', 'high'),
            ('pixels_seen', 3), ('scope', 'TEA_FORMAL_RELEASE'),
            ('reference_sha256', '0' * 64), ('study_export_sha256', '0' * 64),
            ('reviewer_thread_id', 'wrong-reviewer'), ('tool_scope_violations', ['other_image_read']),
            ('actual_image_reads', []), ('parent_spawn_verified', False),
            ('actual_parent_spawn', []), ('actual_tool_calls', []),
        ]
        for field, value in mutations:
            with self.subTest(field=field):
                self.reset()
                self.audit[field] = value
                self.reseal()
                with self.assertRaisesRegex(TaskLockError, 'REVIEW_ISOLATION_REQUIRED'):
                    study.transfer_attempt_limit(self.transfer, ROOT)
        for mutation in ['wrong_image', 'third_image', 'duplicate_call', 'wrong_parent', 'unbound_parent',
                         'parent_fork', 'parent_model', 'parent_effort', 'child_depth', 'child_path']:
            with self.subTest(mutation=mutation):
                self.reset()
                if mutation == 'wrong_image':
                    self.audit['actual_image_reads'][1]['sha256'] = '0' * 64
                elif mutation == 'third_image':
                    self.audit['actual_image_reads'].append(copy.deepcopy(self.audit['actual_image_reads'][0]))
                elif mutation == 'duplicate_call':
                    self.audit['actual_tool_calls'][1]['call_id'] = self.audit['actual_tool_calls'][0]['call_id']
                elif mutation == 'wrong_parent':
                    self.audit['actual_child_spawn_source']['parent_thread_id'] = self.review['reviewer_thread_id']
                elif mutation == 'unbound_parent':
                    self.audit['actual_child_spawn_source']['parent_thread_id'] = 'unrelated-parent-thread'
                elif mutation in ['parent_fork', 'parent_model', 'parent_effort']:
                    key = {'parent_fork': 'fork_turns', 'parent_model': 'model',
                           'parent_effort': 'reasoning_effort'}[mutation]
                    self.audit['actual_parent_spawn'][0][key] = 'wrong'
                else:
                    key = 'depth' if mutation == 'child_depth' else 'agent_path'
                    self.audit['actual_child_spawn_source'][key] = 2 if key == 'depth' else '/root/creator'
                self.reseal()
                with self.assertRaisesRegex(TaskLockError, 'REVIEW_ISOLATION_REQUIRED'):
                    study.transfer_attempt_limit(self.transfer, ROOT)

    def test_call_manifest_must_bind_the_observed_calls(self):
        for mutation in ['input_hash', 'call_id', 'reviewer', 'export', 'uninspected', 'calls_removed']:
            with self.subTest(mutation=mutation):
                self.reset()
                if mutation in ['input_hash', 'call_id']:
                    key = 'input_sha256' if mutation == 'input_hash' else 'call_id'
                    self.manifest['calls'][0][key] = '0' * 64
                elif mutation == 'reviewer':
                    self.manifest['reviewer_thread_id'] = 'different-reviewer'
                elif mutation == 'export':
                    self.manifest['study_export_sha256'] = '0' * 64
                elif mutation == 'uninspected':
                    self.manifest['root_read_actual_call_bodies'] = False
                else:
                    self.manifest['calls'] = []
                self.reseal()
                with self.assertRaisesRegex(TaskLockError, 'CALL_BINDING_REQUIRED'):
                    study.transfer_attempt_limit(self.transfer, ROOT)

    def test_allocation_cannot_replace_source_grants_or_increase_limits(self):
        replacements = [
            ('schema_version', 'vpd-unbounded/v1'), ('scope', 'TEA_FORMAL_RELEASE'),
            ('task_id', 'other-task'), ('work_unit_id', 'other-unit'),
            ('authorization', {'path': 'other.json', 'sha256': '0' * 64}),
            ('copy_manifest', {'path': 'other.json', 'sha256': '0' * 64}),
            ('continuous_repair_authorization', {'path': 'other.json', 'sha256': '0' * 64}),
            ('base_allocation', {'path': 'other.json', 'sha256': '0' * 64}),
            ('human_feedback', {'path': 'other.json', 'sha256': '0' * 64}),
            ('prior_failed_export', {'path': 'other.png', 'sha256': '0' * 64}),
            ('protected_photo_sha256', '0' * 64),
            ('image_guide', {'path': 'other.png', 'sha256': '0' * 64}),
            ('attempt_budget', {'base_attempts': 5, 'total_max': 7, 'method_repairs_max': 2}),
            ('attempt_budget', {'base_attempts': 4, 'total_max': 6, 'method_repairs_max': 1}),
            ('real_current_task_actor', 'WORKER'),
            ('human_acceptance', 'ACCEPTED'),
            ('allocation_is_not_human_stop_condition', False), ('method_change_reason', '   '),
        ] + [('limits', dict(study.HUMAN_LOCAL_LIMITS, **{field: 1}))
             for field in study.HUMAN_LOCAL_LIMITS]
        for field, value in replacements:
            with self.subTest(field=field, value=value):
                self.reset()
                self.grant[field] = value
                self.transfer['human_local_followup_allocation'] = save(
                    self.root, study.HUMAN_LOCAL_FOLLOWUP_ALLOCATION_AUTH, self.grant)
                with self.assertRaisesRegex(TaskLockError, 'FOLLOWUP_SCOPE_CONFLICT'):
                    study.transfer_attempt_limit(self.transfer, ROOT)

    def test_fixed_allocation_path_and_s5_review_path_are_required(self):
        self.transfer['human_local_followup_allocation'] = save(self.root, 'TEST_ONLY/other.json', self.grant)
        with self.assertRaisesRegex(TaskLockError, 'FOLLOWUP_SCOPE_CONFLICT'):
            study.transfer_attempt_limit(self.transfer, ROOT)
        self.reset()
        self.grant['prior_failed_review'] = save(self.root, 'TEST_ONLY/other_review.json', self.review)
        self.transfer['human_local_followup_allocation'] = save(
            self.root, study.HUMAN_LOCAL_FOLLOWUP_ALLOCATION_AUTH, self.grant)
        with self.assertRaisesRegex(TaskLockError, 'FOLLOWUP_SCOPE_CONFLICT'):
            study.transfer_attempt_limit(self.transfer, ROOT)

    def test_write_requires_bound_failed_review_root_and_existing_source_grants(self):
        for field, value in [
            ('repair_basis', self.base['feedback']), ('repair_basis', self.transfer['attempts'][3]['repair_basis']),
            ('actor', 'WORKER_EXECUTOR'), ('task_id', 'other-task'), ('work_unit_id', 'other-unit'),
            ('authorization', {'path': 'other.json', 'sha256': '0' * 64}),
            ('copy_manifest', {'path': 'other.json', 'sha256': '0' * 64}),
            ('figma_write', False), ('protected_photo_sha256', '0' * 64),
        ]:
            with self.subTest(field=field):
                request = dict(self.request, **{field: value})
                with self.assertRaises(TaskLockError):
                    study.validate_transfer_write(ROOT, self.transfer, request)

    def test_native_writer_rejects_actor_source_grant_and_non_active_phase(self):
        self.unit['phase'] = 'REFERENCE_STUDY_ACTIVE'
        for field, value in [('actor', 'WORKER_EXECUTOR'), ('task_id', 'other-task'),
                             ('authorization', {'path': 'other.json', 'sha256': '0' * 64}),
                             ('existing_node_mutations', ['402:3'])]:
            with self.subTest(field=field):
                with self.assertRaises(TaskLockError):
                    validate_locked_request(ROOT, dict(self.request, **{field: value}), self.lock)
        for phase in ['REFERENCE_STUDY_DELIVERED', 'REFERENCE_STUDY_ARCHIVE_BLOCKED', 'REVISION_REQUIRED']:
            with self.subTest(phase=phase):
                self.unit['phase'] = phase
                with self.assertRaises(TaskLockError):
                    validate_locked_request(ROOT, self.request, self.lock)

    def test_no_extra_image_photo_tea_paid_training_automation_or_acceptance(self):
        forbidden = list(study.HUMAN_LOCAL_LIMITS) + [
            'wordmark_image_tool', 'typography_guide', 'render', 'photo_generation', 'photo_change',
            'guide_generation', 'paid_compute_usd', 'paid_compute', 'training', 'model_training',
            'automations', 'automation', 'second_style', 'hidden_variants', 'new_tea_version',
            'new_tea_poster', 'tea_verdict', 'final_acceptance', 'budget_reset', 'mainline_change',
        ]
        for field in forbidden:
            with self.subTest(field=field):
                with self.assertRaisesRegex(TaskLockError, 'FAILED_LOCAL_WRITE_SCOPE_CONFLICT'):
                    study.validate_transfer_write(ROOT, self.transfer, dict(self.request, **{field: True}))
        for field, value in [('formal_version', 30), ('intent', 'PRIMARY'),
                             ('attempt_count', 6), ('attempt_count', True)]:
            with self.subTest(field=field):
                with self.assertRaises(TaskLockError):
                    study.validate_transfer_write(ROOT, self.transfer, dict(self.request, **{field: value}))

    def test_sixth_attempt_is_consumed_and_seventh_is_rejected(self):
        self.transfer['attempts'].append({
            'kind': 'TARGETED_REPAIR', 'export': {'path': 'TEST_ONLY_s6.png', 'sha256': '6' * 64},
            'repair_basis': self.grant['prior_failed_review'],
        })
        self.assertEqual(len(study.transfer_attempts(self.transfer, ROOT)), 6)
        with self.assertRaisesRegex(TaskLockError, 'ATTEMPT_BUDGET_EXHAUSTED'):
            study.validate_transfer_write(ROOT, self.transfer, dict(self.request, attempt_count=6))
        self.transfer['attempts'].append(copy.deepcopy(self.transfer['attempts'][-1]))
        with self.assertRaisesRegex(TaskLockError, 'ATTEMPT_BUDGET_EXCEEDED'):
            study.transfer_attempts(self.transfer, ROOT)

    def test_transition_preserves_all_allocations_attempts_artifacts_and_guides(self):
        fields = ['authorization', 'copy_manifest', 'final_repair_allocation',
                  'supplemental_repair_allocation', 'human_local_repair_allocation',
                  'human_local_followup_allocation']
        mutations = fields + ['old_export', 'old_basis', 'clear_attempts', 'clear_artifacts',
                              'guide_export', 'guide_calls', 'guide_phase', 'acceptance']
        self.assertTrue(self.transfer['artifacts'])
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                new = copy.deepcopy(self.transfer)
                if mutation in fields:
                    new[mutation]['sha256'] = '0' * 64
                elif mutation in ['old_export', 'old_basis']:
                    key = 'export' if mutation == 'old_export' else 'repair_basis'
                    new['attempts'][4][key]['sha256'] = '0' * 64
                elif mutation == 'clear_attempts':
                    new['attempts'] = []
                elif mutation == 'clear_artifacts':
                    new['artifacts'] = []
                elif mutation == 'guide_export':
                    new['supplemental_image_guide']['export']['sha256'] = '0' * 64
                elif mutation == 'guide_calls':
                    new['supplemental_image_guide']['calls_used'] = 0
                elif mutation == 'guide_phase':
                    new['supplemental_image_guide']['phase'] = 'AUTHORIZED'
                else:
                    new['human_acceptance'] = 'ACCEPTED'
                with self.assertRaises(TaskLockError):
                    study.validate_transfer_transition(self.transfer, new)

    def test_s6_append_checks_new_basis_and_keeps_prior_history(self):
        exported = self.root / 'TEST_ONLY_NOT_AN_S6_RUNTIME_EXPORT.png'
        exported.write_bytes((ROOT / self.transfer['attempts'][4]['export']['path']).read_bytes())
        test_export = {'path': exported.relative_to(ROOT).as_posix(), 'sha256': digest(exported)}
        new = copy.deepcopy(self.transfer)
        new['attempts'].append({'kind': 'TARGETED_REPAIR', 'export': test_export,
                                'repair_basis': self.grant['prior_failed_review']})
        study.validate_transfer_transition(self.transfer, new)
        unit = copy.deepcopy(self.unit)
        unit['phase'] = 'REFERENCE_STUDY_ACTIVE'
        unit['content_transfer_experiment'] = new
        self.assertIs(study._validate_transfer(ROOT, unit), new)
        new['attempts'][5]['repair_basis'] = self.base['feedback']
        with self.assertRaisesRegex(TaskLockError, 'FAILED_LOCAL_REVIEW_REQUIRED'):
            study._validate_transfer(ROOT, unit)

    def test_count_four_keeps_exact_s4_human_feedback_special_case(self):
        self.transfer.pop('human_local_followup_allocation')
        self.transfer['attempts'] = self.transfer['attempts'][:4]
        request = dict(self.request, attempt_count=4, repair_basis=self.base['feedback'])
        self.assertEqual(study.transfer_attempt_limit(self.transfer, ROOT), 5)
        study.validate_transfer_write(ROOT, self.transfer, request)
        with self.assertRaisesRegex(TaskLockError, 'CURRENT_HUMAN_LOCAL_FEEDBACK_REQUIRED'):
            study.validate_transfer_write(ROOT, self.transfer,
                                           dict(request, repair_basis=self.grant['prior_failed_review']))

    def test_counts_zero_to_three_keep_existing_repair_contracts(self):
        full = copy.deepcopy(self.transfer)
        for count in range(4):
            with self.subTest(count=count):
                transfer = copy.deepcopy(full)
                transfer['attempts'] = transfer['attempts'][:count]
                transfer.pop('human_local_followup_allocation')
                transfer.pop('human_local_repair_allocation')
                if count < 3:
                    transfer.pop('supplemental_repair_allocation')
                    transfer.pop('supplemental_image_guide')
                if count < 2:
                    transfer.pop('final_repair_allocation')
                    transfer.pop('image_guide')
                request = dict(self.request, attempt_count=count,
                               intent='PRIMARY' if count == 0 else 'TARGETED_REPAIR')
                if count == 0:
                    request.pop('repair_basis')
                else:
                    request['repair_basis'] = full['attempts'][count]['repair_basis']
                self.assertEqual(study.transfer_attempt_limit(transfer, ROOT), max(2, count + 1))
                study.validate_transfer_write(ROOT, transfer, request)


if __name__ == '__main__':
    unittest.main()
