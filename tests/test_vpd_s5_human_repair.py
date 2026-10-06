"""S5 guard tests; isolated temporary receipts are never runtime evidence."""
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


class HumanLocalRepairTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='.s5-test-', dir=ROOT)
        self.root = Path(self.temp.name)
        # Verify the absolute temporary target before recursive cleanup on Windows.
        self.assertTrue(self.root.resolve().is_relative_to(ROOT.resolve()))
        self.addCleanup(self.temp.cleanup)
        self.lock = json.loads((ROOT / LOCK_PATH).read_text(encoding='utf-8'))
        self.unit = self.lock['codex_takeover']['worker_continuation']
        self.transfer = self.unit['content_transfer_experiment']
        # Keep S1-S4 as the baseline if Root has armed S5 during this run.
        self.transfer['attempts'] = self.transfer['attempts'][:4]
        self.transfer.pop('human_local_repair_allocation', None)
        self.transfer.pop('human_local_followup_allocation', None)
        self.transfer.pop('reference_grain_method_allocation', None)
        self.feedback = {
            'schema_version': 'vpd-content-transfer-human-local-feedback/v1',
            'source_kind': 'CURRENT_HUMAN_USER_MESSAGE', 'task_id': TASK, 'work_unit_id': UNIT,
            'user_literal': study.HUMAN_LOCAL_LITERAL,
            'target_export': self.transfer['attempts'][3]['export'],
            'verdict': 'LOCAL_REPAIR_REQUESTED', 'scope': study.HUMAN_LOCAL_SCOPE,
            'human_acceptance': 'PENDING',
            **dict.fromkeys(['final_acceptance', 'mainline_change', 'second_style',
                            'photo_change', 'photo_generation', 'guide_generation'], False),
        }
        self.grant = {
            'schema_version': 'vpd-content-transfer-human-local-repair-allocation/v1',
            'scope': study.TRANSFER_SCOPE, 'task_id': TASK, 'work_unit_id': UNIT,
            'authorization': self.transfer['authorization'], 'copy_manifest': self.transfer['copy_manifest'],
            'continuous_repair_authorization': study.CONTINUOUS_AUTH,
            'feedback': save(self.root, study.HUMAN_FEEDBACK_AUTH, self.feedback),
            'target_export': self.transfer['attempts'][3]['export'],
            'protected_photo_sha256': study.PROTECTED_PHOTO_SHA,
            'image_guide': self.transfer['supplemental_image_guide']['export'],
            'attempt_budget': {'base_attempts': 4, 'total_max': 5, 'local_repairs_max': 1},
            'limits': study.HUMAN_LOCAL_LIMITS.copy(), 'real_current_task_actor': 'ROOT_ONLY',
            'human_acceptance': 'PENDING',
        }
        self.transfer['human_local_repair_allocation'] = save(
            self.root, study.HUMAN_LOCAL_ALLOCATION_AUTH, self.grant)
        original_load = study._load

        def isolated_load(root, ref):
            return original_load(self.root if (self.root / ref['path']).exists() else ROOT, ref)

        loader_patch = patch.object(study, '_load', isolated_load)
        loader_patch.start()
        self.addCleanup(loader_patch.stop)
        auth = isolated_load(ROOT, self.transfer['authorization'])
        self.request = {
            'intent': 'TARGETED_REPAIR', 'attempt_count': 4, 'repair_basis': self.grant['feedback'],
            'figma_write': True, 'protected_photo_sha256': study.PROTECTED_PHOTO_SHA,
            'lock_sha256': digest(ROOT / LOCK_PATH), 'action': self.lock['next_required_action'],
            'actor': 'ROOT_EXECUTOR', 'work_unit_id': UNIT, 'task_id': TASK,
            'authorization': self.transfer['authorization'], 'copy_manifest': self.transfer['copy_manifest'],
            'reference_sha256': study.REFERENCE, 'study_only': True,
            'file_key': auth['allowed_figma_page']['file_key'],
            'page_id': auth['allowed_figma_page']['page_id'],
            'new_frame_name': 'LIUXIANSHENG_CONTENT_TRANSFER_S5',
            'existing_node_mutations': [], 'protected_poster_node': '402:2',
        }

    def reseal(self, feedback=False):
        if feedback:
            self.grant['feedback'] = save(self.root, study.HUMAN_FEEDBACK_AUTH, self.feedback)
            self.request['repair_basis'] = self.grant['feedback']
        self.transfer['human_local_repair_allocation'] = save(
            self.root, study.HUMAN_LOCAL_ALLOCATION_AUTH, self.grant)

    def test_exact_s4_feedback_opens_one_slot_and_native_active_writer(self):
        self.assertEqual(study.transfer_attempt_limit(self.transfer, ROOT), 5)
        self.assertEqual(study.available_guide_calls(self.unit, ROOT), 0)
        study.validate_transfer_write(ROOT, self.transfer, self.request)
        self.unit['phase'] = 'REFERENCE_STUDY_ACTIVE'
        self.assertIs(validate_locked_request(ROOT, self.request, self.lock), self.lock)
        self.assertEqual(len(self.transfer['attempts']), 4)
        self.assertEqual(self.unit['budget']['formal_versions_used'], 29)
        self.assertEqual(self.unit['budget']['revisions_used'], 28)

    def test_without_allocation_old_budget_is_unchanged(self):
        self.transfer.pop('human_local_repair_allocation')
        self.assertEqual(study.transfer_attempt_limit(self.transfer, ROOT), 4)
        with self.assertRaisesRegex(TaskLockError, 'ATTEMPT_BUDGET_EXHAUSTED'):
            study.validate_transfer_write(ROOT, self.transfer, self.request)

    def test_wrong_feedback_cannot_be_used_even_after_rehash(self):
        original = copy.deepcopy(self.feedback)
        for field, value in [
            ('target_export', {'path': 'other.png', 'sha256': '0' * 64}),
            ('source_kind', 'REFERENCE_DESCRIPTION'), ('verdict', 'CONTENT_TRANSFER_FAIL'),
            ('verdict', 'CONTENT_TRANSFER_PASS_WITH_LIMITATIONS'), ('user_literal', '改善一下'),
            ('scope', study.TRANSFER_SCOPE), ('human_acceptance', 'ACCEPTED'),
            ('final_acceptance', True), ('mainline_change', True), ('second_style', True),
            ('photo_change', True), ('photo_generation', True), ('guide_generation', True),
        ]:
            with self.subTest(field=field, value=value):
                self.feedback = dict(original, **{field: value})
                self.reseal(feedback=True)
                with self.assertRaisesRegex(TaskLockError, 'CURRENT_HUMAN_LOCAL_FEEDBACK_REQUIRED'):
                    study.transfer_attempt_limit(self.transfer, ROOT)

    def test_allocation_cannot_change_identity_or_expand_budgets(self):
        original = copy.deepcopy(self.grant)
        for field, value in [
            ('target_export', {'path': 'other.png', 'sha256': '0' * 64}),
            ('authorization', {'path': 'other.json', 'sha256': '0' * 64}),
            ('copy_manifest', {'path': 'other.json', 'sha256': '0' * 64}),
            ('continuous_repair_authorization', {'path': 'other.json', 'sha256': '0' * 64}),
            ('protected_photo_sha256', '0' * 64),
            ('image_guide', {'path': 'guide.png', 'sha256': '0' * 64}),
            ('attempt_budget', {'base_attempts': 4, 'total_max': 6, 'local_repairs_max': 2}),
        ] + [('limits', dict(study.HUMAN_LOCAL_LIMITS, **{limit: 1}))
             for limit in study.HUMAN_LOCAL_LIMITS]:
            with self.subTest(field=field, value=value):
                self.grant = dict(original, **{field: value})
                self.reseal()
                with self.assertRaisesRegex(TaskLockError, 'HUMAN_LOCAL_ALLOCATION_SCOPE_CONFLICT'):
                    study.transfer_attempt_limit(self.transfer, ROOT)

    def test_old_ai_fail_and_unbound_feedback_cannot_be_s5_basis(self):
        for ref in [self.transfer['attempts'][3]['repair_basis'],
                    save(self.root, 'synthetic/unbound_feedback.json', self.feedback)]:
            with self.subTest(ref=ref):
                self.request['repair_basis'] = ref
                with self.assertRaisesRegex(TaskLockError, 'CURRENT_HUMAN_LOCAL_FEEDBACK_REQUIRED'):
                    study.validate_transfer_write(ROOT, self.transfer, self.request)

    def test_native_writer_rejects_all_non_active_phases(self):
        for phase in ['REFERENCE_STUDY_DELIVERED', 'REFERENCE_STUDY_ARCHIVE_BLOCKED',
                      'DELIVERED', 'REVISION_REQUIRED']:
            with self.subTest(phase=phase):
                self.unit['phase'] = phase
                with self.assertRaises(TaskLockError):
                    validate_locked_request(ROOT, self.request, self.lock)

    def test_request_cannot_reopen_other_actions(self):
        for field, value in [
            ('photo_change', True), ('wordmark_image_tool', True), ('guide_generation', True),
            ('photo_generation', True), ('second_style', True), ('mainline_change', True),
            ('final_acceptance', True), ('budget_reset', True), ('paid_compute', True),
            ('protected_photo_sha256', '0' * 64), ('formal_version', 30),
        ]:
            with self.subTest(field=field):
                request = dict(self.request, **{field: value})
                with self.assertRaisesRegex(TaskLockError, 'HUMAN_LOCAL_WRITE_SCOPE_CONFLICT'):
                    study.validate_transfer_write(ROOT, self.transfer, request)

    def test_sixth_attempt_and_second_s5_write_are_rejected(self):
        self.transfer['attempts'].append({'kind': 'TARGETED_REPAIR',
            'export': {'path': 's5.png', 'sha256': '5' * 64}, 'repair_basis': self.request['repair_basis']})
        self.assertEqual(len(study.transfer_attempts(self.transfer, ROOT)), 5)
        self.request['attempt_count'] = 5
        with self.assertRaisesRegex(TaskLockError, 'ATTEMPT_BUDGET_EXHAUSTED'):
            study.validate_transfer_write(ROOT, self.transfer, self.request)
        self.transfer['attempts'].append(copy.deepcopy(self.transfer['attempts'][-1]))
        with self.assertRaisesRegex(TaskLockError, 'ATTEMPT_BUDGET_EXCEEDED'):
            study.transfer_attempts(self.transfer, ROOT)

    def test_transition_preserves_authority_history_and_terminal_guides(self):
        for mutation in ['auth', 'copy', 'acceptance', 'old_attempt', 'clear_attempts',
                         'allocation', 'guide_export', 'guide_calls', 'guide_phase']:
            with self.subTest(mutation=mutation):
                new = copy.deepcopy(self.transfer)
                if mutation in ['auth', 'copy', 'allocation']:
                    field = {'auth': 'authorization', 'copy': 'copy_manifest',
                             'allocation': 'human_local_repair_allocation'}[mutation]
                    new[field]['sha256'] = '0' * 64
                elif mutation == 'acceptance':
                    new['human_acceptance'] = 'ACCEPTED'
                elif mutation == 'old_attempt':
                    new['attempts'][3]['export']['sha256'] = '0' * 64
                elif mutation == 'clear_attempts':
                    new['attempts'] = []
                elif mutation == 'guide_export':
                    new['supplemental_image_guide']['export']['sha256'] = '0' * 64
                elif mutation == 'guide_calls':
                    new['supplemental_image_guide']['calls_used'] = 0
                else:
                    new['supplemental_image_guide']['phase'] = 'AUTHORIZED'
                with self.assertRaises(TaskLockError):
                    study.validate_transfer_transition(self.transfer, new)

    def test_append_s5_preserves_old_history_and_verifies_new_basis(self):
        new = copy.deepcopy(self.transfer)
        new['attempts'].append({'kind': 'TARGETED_REPAIR',
            'export': {'path': 's5.png', 'sha256': '5' * 64}, 'repair_basis': self.request['repair_basis']})
        study.validate_transfer_transition(self.transfer, new)
        # The actual fifth-attempt basis path is independently checked against S4.
        study._human_feedback(ROOT, new['attempts'][4]['repair_basis'], new['attempts'][3]['export'])


if __name__ == '__main__':
    unittest.main()
