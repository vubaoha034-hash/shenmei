import hashlib
import tempfile
import unittest
from pathlib import Path
from structural_gate import evaluate, GLYPHS, REFERENCE_SHA, BASELINE_SHA

class GateTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.d=Path(self.tmp.name)
        self.ref=self.d/'reference';self.ref.write_bytes(b'fake reference')
        self.old=self.d/'baseline';self.old.write_bytes(b'fake baseline')
        self.svg=self.d/'structure.svg'
        paths=''.join('<g data-glyph="%s"><path d="M 1 1 L 20 20 L 40 30"/><path d="M 5 3 L 30 20 L 20 45"/></g>'%g for g in GLYPHS)
        self.svg.write_text('<svg xmlns="http://www.w3.org/2000/svg">'+paths+'</svg>',encoding='utf-8')
        self.q={'target':'地图以外','scope':'ISOLATED_RESEARCH','method':'CUSTOM_VECTOR_STRUCTURE_FIRST',
          'render_stage':'STRUCTURE_ONLY','reference_sha256':REFERENCE_SHA,'reference_path':str(self.ref),
          'baseline_sha256':BASELINE_SHA,'baseline_path':str(self.old),'explicit_new_image_authorization':True,
          'new_candidate_limit':1,'reused_candidate_count':0,'preserve_originals':True,
          'glyph_plan':[{'glyph':'地','role':'entry'},{'glyph':'图','role':'boundary'},{'glyph':'以','role':'exit'},{'glyph':'外','role':'release'}],
          'interglyph_mechanism':'BOUNDARY_EXIT_FROM_TU_TO_YI','texture_enabled':False,
          'structural_candidate_path':str(self.svg)}
    def test_fake_reference_blocks(self):
        self.assertIn('REFERENCE_NOT_BOUND_TO_ACTUAL_BYTES',evaluate(self.q)['reasons'])
    def test_no_render_permission_blocks(self):
        q=dict(self.q,explicit_new_image_authorization=False)
        self.assertIn('NO_NEW_RENDER_AUTHORIZATION',evaluate(q)['reasons'])
    def test_texture_blocks(self):
        q=dict(self.q,texture_enabled=True)
        self.assertIn('TEXTURE_MUST_WAIT_FOR_STRUCTURE_APPROVAL',evaluate(q)['reasons'])
    def test_generic_imagegen_blocks(self):
        q=dict(self.q,method='IMAGEGEN_GENERIC_BRUSH')
        self.assertIn('UNCONTROLLED_IMAGEGEN_METHOD',evaluate(q)['reasons'])
    def test_pixel_instead_of_vector_blocks(self):
        p=self.d/'candidate.png';p.write_bytes(b'png')
        q=dict(self.q,structural_candidate_path=str(p))
        self.assertIn('STAGE_A_REQUIRES_NATIVE_VECTOR_NOT_RASTER',evaluate(q)['reasons'])
    def test_omitted_character_blocks(self):
        txt=self.svg.read_text(encoding='utf-8').replace('data-glyph="外"','data-glyph="X"')
        self.svg.write_text(txt,encoding='utf-8')
        self.assertIn('GLYPH_GROUPS_MISSING_OR_WRONG',evaluate(self.q)['reasons'])
    def test_raster_svg_blocks(self):
        txt=self.svg.read_text(encoding='utf-8').replace('</svg>','<image href="x" /></svg>')
        self.svg.write_text(txt,encoding='utf-8')
        self.assertIn('RASTER_TEXT_OR_EFFECT_PRESENT',evaluate(self.q)['reasons'])
    def test_no_future_approval_claim(self):
        q=dict(self.q,human_structure_verdict='APPROVED')
        self.assertIn('CANNOT_ASSUME_HUMAN_APPROVAL_BEFORE_OUTPUT',evaluate(q)['reasons'])
    def test_false_glyph_plan_blocks(self):
        import copy
        q=copy.deepcopy(self.q);q['glyph_plan'][1]['role']='normal_box'
        self.assertIn('FOUR_GLYPH_ROLES_NOT_FROZEN',evaluate(q)['reasons'])
    def test_incomplete_paths_blocks(self):
        self.svg.write_text('<svg><g data-glyph="地"><path d="M1 1 L2 2"/></g></svg>')
        self.assertIn('GLYPH_GROUPS_MISSING_OR_WRONG',evaluate(self.q)['reasons'])
    def test_identical_shapes_falsely_labeled_four_hanzi_block(self):
        # Red-team case with genuine source hashes can pass the old path-count gate.
        # No image generator is invoked; this is an intentionally invalid synthetic vector.
        paths=''.join('<g data-glyph="%s"><path d="M 0 0 L 100 100 L 200 100"/><path d="M 0 50 L 100 150 L 200 150"/></g>'%g for g in GLYPHS)
        self.svg.write_text('<svg xmlns="http://www.w3.org/2000/svg">'+paths+'</svg>',encoding='utf-8')
        self.assertIn('DUPLICATED_GLYPH_OUTLINES',evaluate(self.q)['reasons'])
    def test_not_claiming_visual_authenticity_even_if_nonduplicate(self):
        # Different path strings still do not establish four correct and beautiful glyphs.
        src=self.svg.read_text(encoding='utf-8')
        for i, char in enumerate(GLYPHS):
            src=src.replace('data-glyph="'+char+'"','data-glyph="'+char+'" transform="translate('+str(i*230)+',0)"')
        self.svg.write_text(src,encoding='utf-8')
        actual=evaluate(self.q)
        self.assertEqual(actual['user_aesthetic_verdict'],'NOT_REVIEWED')
        self.assertFalse(actual['formal_rule_promoted'])
        self.assertEqual(actual['authorization_to_texture'],'NO')

    def test_no_output_blocks(self):
        q=dict(self.q,structural_candidate_path=str(self.d/'missing.svg'))
        self.assertIn('NO_STRUCTURAL_CANDIDATE',evaluate(q)['reasons'])

if __name__=='__main__':unittest.main()
