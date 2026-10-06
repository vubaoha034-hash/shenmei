import importlib.util
import tempfile
import unittest
from pathlib import Path
from PIL import Image

spec = importlib.util.spec_from_file_location('exact', Path(__file__).with_name('exact_composite.py'))
exact = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exact)

class CompositeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.ref = self.root/'reference.png'
        source = Image.new('RGB', (7, 15))
        source.putdata([(x*23, y*13, (x+y)*7) for y in range(15) for x in range(7)])
        source.save(self.ref)
        self.mask = self.root/'mask.png'
        m = Image.new('L', (3, 3), 0)
        m.putpixel((1, 1), 255)
        m.save(self.mask)
        self.patch = self.root/'patch.png'
        Image.new('RGBA', (3, 3), (255, 0, 0, 255)).save(self.patch)
        self.out = self.root/'output.png'
        self.region = {'id': 'title', 'role': 'main_title_text', 'x': 1, 'y': 8, 'width': 3, 'height': 3, 'mask_source': str(self.mask), 'mask_sha256': exact.digest(self.mask)}
        self.plan = {'action': 'VERIFY_BINDING_THEN_MASKED_EDIT_AND_COMPOSITE', 'execution_contract': {'final_canvas_policy': 'EXACT_REFERENCE_DIMENSIONS', 'finalization_mode': 'MASKED_LOCAL_EDIT_OR_DETERMINISTIC_COMPOSITE', 'whole_canvas_generative_edit_as_final': False, 'outside_edit_regions_policy': 'BIT_IDENTICAL', 'generative_output_role': 'GUIDE_ONLY', 'on_exact_composite_unavailable': 'STOP', 'reference_binding': {'sha256': exact.digest(self.ref)}, 'reference_dimensions': {'width': 7, 'height': 15}, 'editable_regions': [self.region]}}
        self.patches = [{'region_id': 'title', 'path': str(self.patch), 'sha256': exact.digest(self.patch), 'role': 'LOCAL_TEXT_OR_TEXTURE_CANDIDATE'}]

    def test_composite_exact_dimensions_and_zero_outside_mask_diff(self):
        provenance, result = exact.compose(self.ref, self.out, self.plan, self.patches)
        self.assertTrue(result['engineering_pass'])
        self.assertEqual(result['output_dimensions'], [7, 15])
        self.assertTrue(result['exact_aspect_ratio'])
        self.assertEqual(result['outside_mask_changed_pixels'], 0)
        self.assertFalse(result['final_eligible']) # no manufactured semantic PASS
        self.assertNotEqual(Image.open(self.ref).getpixel((2, 9)), Image.open(self.out).getpixel((2, 9)))
        self.assertEqual(exact.validate(self.ref, self.out, self.plan, provenance)['failures'], [])

    def test_actual_reported_941x1672_output_cannot_be_final(self):
        guide = self.root/'guide.png'
        Image.new('RGB', (941, 1672)).save(guide)
        result = exact.validate(self.ref, guide, self.plan, candidate_role='GUIDE_ONLY')
        self.assertFalse(result['final_eligible'])
        self.assertIn('EXACT_REFERENCE_DIMENSIONS_REQUIRED', result['failures'])
        self.assertIn('GENERATIVE_GUIDE_CANNOT_BE_FINAL', result['failures'])

    def test_same_dimensions_whole_canvas_guide_cannot_be_final(self):
        provenance, _ = exact.compose(self.ref, self.out, self.plan, self.patches)
        result = exact.validate(self.ref, self.out, self.plan, provenance, candidate_role='GUIDE_ONLY')
        self.assertIn('GENERATIVE_GUIDE_CANNOT_BE_FINAL', result['failures'])

    def test_one_outside_pixel_change_is_failure_without_tolerance(self):
        provenance, _ = exact.compose(self.ref, self.out, self.plan, self.patches)
        candidate = Image.open(self.out).copy()
        candidate.putpixel((0, 0), (1, 0, 0))
        candidate.save(self.out)
        result = exact.validate(self.ref, self.out, self.plan, provenance)
        self.assertEqual(result['outside_mask_changed_pixels'], 1)
        self.assertFalse(result['engineering_pass'])
        self.assertIn('OUTSIDE_EDIT_MASK_PIXELS_CHANGED', result['failures'])

    def test_whole_canvas_patch_no_resize_fallback(self):
        Image.new('RGBA', (941, 1672)).save(self.patch)
        self.patches[0]['sha256'] = exact.digest(self.patch)
        with self.assertRaisesRegex(ValueError, 'no scaling'):
            exact.compose(self.ref, self.out, self.plan, self.patches)
        self.assertFalse(self.out.exists())

    def test_mask_hash_and_soft_mask_fail_closed(self):
        with self.assertRaisesRegex(ValueError, 'hash mismatch'):
            self.region['mask_sha256'] = '0'*64
            exact.compose(self.ref, self.out, self.plan, self.patches)
        m = Image.new('L', (3, 3), 128)
        m.save(self.mask)
        self.region['mask_sha256'] = exact.digest(self.mask)
        with self.assertRaisesRegex(ValueError, 'binary mask'):
            exact.compose(self.ref, self.out, self.plan, self.patches)

    def test_mask_union_full_canvas_and_cleanup_escape_stop(self):
        self.region.update(x=0, y=0, width=7, height=15)
        with self.assertRaisesRegex(ValueError, 'whole-canvas'):
            exact.compose(self.ref, self.out, self.plan, self.patches)
        self.region.update(x=1, y=8, width=3, height=3, role='minimal_text_cleanup')
        with self.assertRaisesRegex(ValueError, 'cleanup'):
            exact.compose(self.ref, self.out, self.plan, self.patches)

    def test_original_is_not_overwritten(self):
        original_hash = exact.digest(self.ref)
        with self.assertRaisesRegex(ValueError, 'overwritten'):
            exact.compose(self.ref, self.ref, self.plan, self.patches)
        self.assertEqual(exact.digest(self.ref), original_hash)

    def test_jpeg_final_reencoding_not_allowed(self):
        provenance, _ = exact.compose(self.ref, self.out, self.plan, self.patches)
        jpg = self.root/'output.jpg'
        Image.open(self.out).save(jpg)
        result = exact.validate(self.ref, jpg, self.plan, provenance)
        self.assertIn('LOSSLESS_ORIGINAL_SAMPLE_MODE_REQUIRED', result['failures'])
        self.assertFalse(result['final_eligible'])

    def test_same_samples_with_changed_color_profile_are_not_final(self):
        provenance, _ = exact.compose(self.ref, self.out, self.plan, self.patches)
        image = Image.open(self.out).copy()
        image.save(self.out, icc_profile=b'SYNTHETIC_CHANGED_COLOR_PROFILE')
        result = exact.validate(self.ref, self.out, self.plan, provenance)
        self.assertEqual(result['outside_mask_changed_pixels'], 0)
        self.assertIn('ORIGINAL_COLOR_PROFILE_AND_ORIENTATION_REQUIRED', result['failures'])
        self.assertFalse(result['final_eligible'])

    def test_patch_and_mask_sources_cannot_be_overwritten(self):
        for path in [self.patch, self.mask]:
            with self.assertRaisesRegex(ValueError, 'source files cannot be overwritten'):
                exact.compose(self.ref, path, self.plan, self.patches)

    def test_visual_review_must_bind_actual_result_and_all_seven_checks(self):
        provenance, _ = exact.compose(self.ref, self.out, self.plan, self.patches)
        review = {'reference_sha256': exact.digest(self.ref), 'output_sha256': exact.digest(self.out), 'actual_pixels_viewed': True, 'mask_scope_text_only': True, 'evidence_locator': 'SYNTHETIC_TEST_NOT_REAL_VISUAL_ACCEPTANCE', 'checks': {k: True for k in exact.SEMANTICS}}
        result = exact.validate(self.ref, self.out, self.plan, provenance, review)
        self.assertTrue(result['final_eligible'])
        review['checks']['two_people'] = False
        self.assertFalse(exact.validate(self.ref, self.out, self.plan, provenance, review)['final_eligible'])
        review['checks']['two_people'] = True
        review['output_sha256'] = '0'*64
        self.assertFalse(exact.validate(self.ref, self.out, self.plan, provenance, review)['final_eligible'])

if __name__ == '__main__':
    unittest.main()
