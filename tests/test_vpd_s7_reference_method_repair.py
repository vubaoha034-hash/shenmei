"""TEST_ONLY S7 guard fixtures; no business writes or aesthetic verdicts."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from visual_memory import vpd_reference_typography_study as study
from visual_memory.vpd_task_lock import TaskLockError, digest

ROOT = Path(__file__).resolve().parents[1]
B = 'evidence/vpd/codex_takeover_20261003/liuxiansheng_content_transfer_20261005/'


class ReferenceMethodFollowupTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix='.s7-test-', dir=ROOT)
        self.temp = temp
        self.local = Path(temp.name).resolve()
        self.assertTrue(self.local.is_relative_to(ROOT.resolve()))
        self.addCleanup(temp.cleanup)
        lock = json.loads((ROOT/'continuity/vpd/CURRENT_TASK_LOCK.json').read_text(encoding='utf8'))
        self.unit = lock['codex_takeover']['worker_continuation']
        self.transfer = self.unit['content_transfer_experiment']
        self.transfer.pop('reference_grain_method_allocation', None)
        self.transfer['attempts'] = self.transfer['attempts'][:5]
        self.review = study._load(ROOT, {'path':study.S6_FAILED_REVIEW,
                                         'sha256':digest(ROOT/study.S6_FAILED_REVIEW)})
        export = '.liu-visual-private/liuxiansheng_transfer_20261005/FIGMA_COMPLETE_S6.png'
        self.assertEqual(digest(ROOT/export), self.review['study_export_sha256'])
        self.transfer['attempts'].append({'kind':'TARGETED_REPAIR',
            'export':{'path':export,'sha256':self.review['study_export_sha256']},
            'repair_basis':{'path':study.S5_FAILED_REVIEW,'sha256':digest(ROOT/study.S5_FAILED_REVIEW)}})
        self.audit_path = self.review['isolation_audit']['path']
        self.audit = study._load(ROOT, self.review['isolation_audit'])
        self.manifest_path = self.audit['reviewed_call_manifest']['path']
        self.manifest = study._load(ROOT, self.audit['reviewed_call_manifest'])
        self.grant = {
            'schema_version':'vpd-content-transfer-failed-reference-method-followup/v1',
            'scope':study.TRANSFER_SCOPE,
            'task_id':'VPD-CHAZUO-CODEX-COMPLETE-POSTER-20261003-01',
            'work_unit_id':'CHAZUO_APPROVED_SOURCE_TYPOGRAPHY_20261003_R1',
            'authorization':self.transfer['authorization'], 'copy_manifest':self.transfer['copy_manifest'],
            'continuous_repair_authorization':study.CONTINUOUS_AUTH,
            'parent_allocation':self.transfer['human_local_followup_allocation'],
            'prior_failed_export':self.transfer['attempts'][5]['export'],
            'protected_photo_sha256':study.PROTECTED_PHOTO_SHA,
            'image_guide':self.transfer['supplemental_image_guide']['export'],
            'attempt_budget':{'base_attempts':6,'total_max':7,'method_repairs_max':1},
            'limits':study.HUMAN_LOCAL_LIMITS.copy(), 'real_current_task_actor':'ROOT_ONLY',
            'human_acceptance':'PENDING', 'allocation_is_not_human_stop_condition':True,
            'method_change_reason':'TEST_ONLY: bounded reference-derived repair, not runtime authorization.',
            'expert_spec_refs':[{'path':B+'EXPERT_S6_METHOD_PLAN.md',
                                'sha256':digest(ROOT/(B+'EXPERT_S6_METHOD_PLAN.md'))}],
            'test_fixture_only':True,
        }
        self.reseal()
        original_load = study._load
        cache = {}

        def isolated_load(root, ref):
            target = self.local if (self.local/ref['path']).exists() else ROOT
            if target == self.local:
                return original_load(target,ref)
            key = (ref['path'],ref['sha256'])
            if key not in cache:
                cache[key] = original_load(ROOT,ref)
            return copy.deepcopy(cache[key])
        loader = patch.object(study,'_load',isolated_load)
        loader.start()
        self.addCleanup(loader.stop)
        self.request = {'intent':'TARGETED_REPAIR','attempt_count':6,'figma_write':True,
            'actor':'ROOT_EXECUTOR','task_id':self.grant['task_id'],'work_unit_id':self.grant['work_unit_id'],
            'authorization':self.transfer['authorization'],'copy_manifest':self.transfer['copy_manifest'],
            'protected_photo_sha256':study.PROTECTED_PHOTO_SHA,
            'repair_basis':self.grant['prior_failed_review'],
            'method_authorization':self.transfer['reference_grain_method_allocation']}
        self.original = copy.deepcopy((self.grant,self.review,self.audit,self.manifest))

    def save(self, path, data):
        p = self.local/path
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        return {'path':path,'sha256':digest(p)}

    def reseal(self):
        self.audit['reviewed_call_manifest'] = self.save(self.manifest_path,self.manifest)
        self.review['isolation_audit'] = self.save(self.audit_path,self.audit)
        self.grant['prior_failed_review'] = self.save(study.S6_FAILED_REVIEW,self.review)
        self.transfer['reference_grain_method_allocation'] = self.save(study.REFERENCE_GRAIN_ALLOCATION_AUTH,self.grant)
        if hasattr(self,'request'):
            self.request.update(repair_basis=self.grant['prior_failed_review'],
                                method_authorization=self.transfer['reference_grain_method_allocation'])

    def reset(self):
        self.grant,self.review,self.audit,self.manifest = copy.deepcopy(self.original)
        self.reseal()

    def test_one_root_write_then_exhaustion_preserves_history(self):
        before = copy.deepcopy(self.transfer['attempts'])
        self.assertEqual(study.transfer_attempt_limit(self.transfer,ROOT),7)
        study.validate_transfer_write(ROOT,self.transfer,self.request)
        self.assertEqual(self.transfer['attempts'],before)
        old = copy.deepcopy(self.transfer)
        self.transfer['attempts'].append({'kind':'TARGETED_REPAIR','export':before[-1]['export'],
                                         'repair_basis':self.grant['prior_failed_review']})
        study.validate_transfer_transition(old,self.transfer)
        self.request['attempt_count'] = 7
        with self.assertRaisesRegex(TaskLockError,'BUDGET_EXHAUSTED'):
            study.validate_transfer_write(ROOT,self.transfer,self.request)

    def test_no_grant_and_wrong_parent_and_scope_fail(self):
        self.transfer.pop('reference_grain_method_allocation')
        self.assertEqual(study.transfer_attempt_limit(self.transfer,ROOT),6)
        with self.assertRaisesRegex(TaskLockError,'BUDGET_EXHAUSTED'):
            study.validate_transfer_write(ROOT,self.transfer,self.request)
        for field,value in [('parent_allocation',{}),('image_guide',{}),('scope','TEA'),
                            ('real_current_task_actor','WORKER'),('human_acceptance','ACCEPTED'),
                            ('expert_spec_refs',[]),('attempt_budget',{'base_attempts':6,'total_max':8})]:
            with self.subTest(field=field):
                self.reset();self.grant[field]=value;self.reseal()
                with self.assertRaisesRegex(TaskLockError,'SCOPE_CONFLICT'):
                    study.transfer_attempt_limit(self.transfer,ROOT)

    def test_actual_fail_and_isolation_and_exact_calls_are_required(self):
        for field,value in [('verdict','CONTENT_TRANSFER_PASS_WITH_LIMITATIONS'),
                            ('actual_pixels_seen',False),('study_export_sha256','0'*64)]:
            with self.subTest(field=field):
                self.reset();self.review[field]=value;self.reseal()
                with self.assertRaisesRegex(TaskLockError,'ACTUAL_REPAIR_BASIS_REQUIRED'):
                    study.transfer_attempt_limit(self.transfer,ROOT)
        for field,value in [('fork_turns','all'),('actual_model','gpt-6-astra'),('pixels_seen',3),
                            ('actual_tool_calls',[]),('actual_image_reads',[])]:
            with self.subTest(field=field):
                self.reset();self.audit[field]=value;self.reseal()
                with self.assertRaisesRegex(TaskLockError,'ISOLATION_REQUIRED'):
                    study.transfer_attempt_limit(self.transfer,ROOT)
        self.reset();self.audit['actual_child_spawn_source']['agent_path']='/root/creator';self.reseal()
        with self.assertRaisesRegex(TaskLockError,'ISOLATION_REQUIRED'):
            study.transfer_attempt_limit(self.transfer,ROOT)
        self.reset();self.manifest['calls'][0]['input_sha256']='0'*64;self.reseal()
        with self.assertRaisesRegex(TaskLockError,'CALL_BINDING_REQUIRED'):
            study.transfer_attempt_limit(self.transfer,ROOT)

    def test_no_scope_expansion_and_explicit_method_binding(self):
        for field in ['new_tea_version','photo_change','wordmark_image_tool','paid_compute','model_training',
                      'automation','mainline_change','budget_reset']:
            with self.subTest(field=field):
                req=copy.deepcopy(self.request);req[field]=True
                with self.assertRaisesRegex(TaskLockError,'WRITE_SCOPE_CONFLICT'):
                    study.validate_transfer_write(ROOT,self.transfer,req)
        req=copy.deepcopy(self.request);req['method_authorization']={}
        with self.assertRaisesRegex(TaskLockError,'METHOD_AUTHORIZATION_REQUIRED'):
            study.validate_transfer_write(ROOT,self.transfer,req)

    def test_immutable_grant_and_attempt_prefix(self):
        for mutate in ['grant','attempt']:
            newer=copy.deepcopy(self.transfer)
            if mutate=='grant':newer['reference_grain_method_allocation']={'path':'other','sha256':'0'*64}
            else:newer['attempts'][0]['kind']='TARGETED_REPAIR'
            with self.assertRaisesRegex(TaskLockError,'REWRITTEN'):
                study.validate_transfer_transition(self.transfer,newer)

    def test_final_append_must_use_frozen_isolated_fail(self):
        self.unit['phase'] = 'REFERENCE_STUDY_ACTIVE'
        self.transfer['attempts'].append({'kind':'TARGETED_REPAIR',
            'export':self.transfer['attempts'][5]['export'],
            'repair_basis':self.grant['prior_failed_review'], 'test_fixture_only':True})
        self.assertIs(study._validate_transfer(ROOT,self.unit),self.transfer)
        unisolated = copy.deepcopy(self.review)
        unisolated.pop('isolation_audit')
        unisolated['reviewer_thread_id'] = 'TEST_ONLY_CREATOR_NO_ISOLATION'
        fake_ref = self.save(B+'TEST_ONLY_OTHER_FAIL.json',unisolated)
        self.transfer['attempts'][6]['repair_basis'] = fake_ref
        with self.assertRaisesRegex(TaskLockError,'FAILED_LOCAL_REVIEW_REQUIRED'):
            study._validate_transfer(ROOT,self.unit)


if __name__=='__main__':
    unittest.main()
