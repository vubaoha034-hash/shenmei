"""V28: stable source writing; Tea right-na ends into the actual frozen leaf.

No V27 arch or dragged tail is reused. Original V24 contour ownership is bound
one-to-one, with the fixed V26 curve housekeeping and one contextual Tea stroke.
"""
from pathlib import Path
import argparse, copy, hashlib, importlib.util, json, sys
sys.dont_write_bytecode = True
import PIL

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
BASE_MAKER = ROOT / 'evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v26/make_glyph_program.py'
BASE_SHA = '514e370da517fdb47981d02e4e11a914a68087bcd7c4c251cf18773212578b80'
assert hashlib.sha256(BASE_MAKER.read_bytes()).hexdigest() == BASE_SHA
spec = importlib.util.spec_from_file_location('bound_v26_natural_curve_helper', BASE_MAKER)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
g = helper.g
COPY = '一杯茶，慢下来'
SOURCES = helper.SOURCES
# First ideographic cells share the original source first-row vertical frame.
# The natural One bar lies in the centre of that frame, not on the lower baseline.
# Second row keeps the original relative ink top/bottom with a common ~555 baseline.
POSES = {'一': (.30, 420, 451.918), '杯': (.49, 538, 360),
         '茶': (.49, 726, 362.0078), '，': (.32, 941, 489.556),
         '慢': (.33, 1020, 454.229), '下': (.33, 1145, 463.61275),
         '来': (.31, 1247, 445)}
# Actual original-source inspection: foreground oblique leaf has a narrow upper
# left start at approximately (824,663), then reaches its lower-right tip(987,758).
# This closed white component stops at that seam; the unchanged green leaf supplies
# the later right-na body. It is context-dependent lettering, not a portable glyph.
TEA_RIGHT_NA_GLOBAL = [
    {'op':'moveTo','points':[[793,512]]},
    {'op':'curveTo','points':[[803,520],[809,548],[806,575]]},
    {'op':'curveTo','points':[[804,601],[810,631],[822,659]]},
    {'op':'curveTo','points':[[823,660],[824,662],[825,663]]},
    {'op':'curveTo','points':[[822,663],[819,662],[817,660]]},
    {'op':'curveTo','points':[[804,647],[790,625],[788,602]]},
    {'op':'curveTo','points':[[785,570],[785,538],[793,512]]},
    {'op':'closePath','points':[]},
]

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def jb(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')

def ref(path):
    p = Path(path).resolve()
    assert p.is_relative_to(ROOT.resolve())
    raw = p.read_bytes()
    return {'path':p.relative_to(ROOT).as_posix(),'sha256':sha(raw),'bytes':len(raw)}

def root_write_gate():
    raw = (ROOT / 'continuity/vpd/CURRENT_TASK_LOCK.json').read_bytes()
    lock = json.loads(raw)
    u = lock['codex_takeover']['worker_continuation']
    last = u['versions'][-1]
    assert lock['revision'] == 330 and u['phase'] == 'REVISION_REQUIRED'
    assert u['unit_id'] == 'CHAZUO_APPROVED_SOURCE_TYPOGRAPHY_20261003_R1'
    assert last['number'] == 27 and last['verdict'] == 'AI_FAIL'
    return {'native_revision':330,'phase':u['phase'],'last_version':27,
            'last_verdict':'AI_FAIL','lock_sha256':sha(raw),'explicit_parent_go':'GO_V28',
            'parent_reported_fixed_remote_commit':'63c2d83f46e2a01b432f61fd88cbdc69bc408434'}

def build_program():
    k = g.edited_kernel(ROOT)
    original = json.loads(k['checked'](ROOT,k['INPUTS']['source_commands']))
    k['checked'](ROOT,k['INPUTS']['trace_svg'])
    k['checked'](ROOT,k['INPUTS']['art_direction'])
    assert original['path_count'] == 17
    glyphs, details, geometry, accounted = [], [], [], []
    for char in COPY:
        rows, work = [], {}
        for pi in SOURCES[char]:
            contours = original['paths'][pi]['closed_contours']
            rows.append({'path_index':pi,'contour_indices':list(range(len(contours)))})
            for ci, before in enumerate(contours):
                b = helper.bounds([before])
                center = [(b[0]+b[2])/2,(b[1]+b[3])/2]
                warped = copy.deepcopy(before)
                max_move = 0.0
                for command in warped:
                    for index, point in enumerate(command['points']):
                        moved = helper.local_warp(pi,ci,point,center)
                        max_move = max(max_move,helper.distance(point,moved))
                        command['points'][index] = moved
                assert max_move <= 20.0001
                after, joins = helper.tidy_curves(warped)
                work[(pi,ci)] = after
                details.append({'char':char,'path_index':pi,'contour_index':ci,
                    'before_sha256':helper.commands_sha(before),'source_bounds':b,
                    'original_commands':len(before),'after_commands':len(after),
                    'joins':joins,'maximum_source_node_move_px':max_move,
                    'component_reauthoring':False,'pointwise_bound_applicable':True})
        natural_box = helper.bounds(list(work.values()))
        if char == '茶':
            scale,tx,ty = POSES[char]
            component = copy.deepcopy(TEA_RIGHT_NA_GLOBAL)
            for command in component:
                command['points'] = [[natural_box[0]+(p[0]-tx)/scale,
                                      natural_box[1]+(p[1]-ty)/scale] for p in command['points']]
            k['closed_commands'](component)
            work[(8,0)] = component
            d = next(r for r in details if r['path_index']==8 and r['contour_index']==0)
            d.update(after_commands=len(component),joins=[],maximum_source_node_move_px=None,
                     component_reauthoring=True,pointwise_bound_applicable=False,
                     actual_authored_global_curve=TEA_RIGHT_NA_GLOBAL,
                     contextual_leaf_supplies_later_na=True)
        box = helper.bounds(list(work.values()))
        origin, edits = box[:2], []
        for pi in SOURCES[char]:
            for ci,before in enumerate(original['paths'][pi]['closed_contours']):
                after = copy.deepcopy(work[(pi,ci)])
                for command in after:
                    command['points'] = [[p[0]-origin[0],p[1]-origin[1]] for p in command['points']]
                k['closed_commands'](after)
                reason = ('Contextual Tea right-na closed vector ends at the actual S leaf upper-left seam; the frozen green leaf supplies its later stroke; original source ownership is retained.'
                    if pi==8 else 'Retain V24 natural writing, fixed V26 bounded local housekeeping and curve joins; restore shared reading frame without the V27 One arch or Tea dragged component.')
                edits.append({'op':'replace_contour','path_index':pi,'contour_index':ci,
                              'before_sha256':helper.commands_sha(before),
                              'after_contours':[after],'reason':reason})
                accounted.append((pi,ci))
        scale,tx,ty = POSES[char]
        glyphs.append({'char':char,'source':rows,'edits':edits,
                       'placement':{'scale':scale,'tx':tx,'ty':ty}})
        geometry.append({'char':char,'source_local_origin':origin,'natural_source_bounds':natural_box,
                         'authored_source_bounds':box,'placement':{'scale':scale,'tx':tx,'ty':ty},
                         'ink_bounds_before_fixed_exclusion':[tx,ty,
                             tx+scale*(box[2]-origin[0]),ty+scale*(box[3]-origin[1])]})
    expected = [(r['path_index'],ci) for r in original['paths'] for ci in range(len(r['closed_contours']))]
    assert sorted(accounted)==sorted(expected) and len(accounted)==len(set(accounted))==21
    program = {'schema':'vpd-source-bound-glyph-edits/v1','formal_version':28,'copy':COPY,
               'source_trace':k['INPUTS']['trace_svg'],'glyphs':glyphs,
               'negative_space':{'art_direction':k['INPUTS']['art_direction'],
                                'operation':'difference-union',**k['FLAGS']}}
    notes = {'schema':'vpd-v28-contextual-leaf-terminal-lettering/v1','formal_version':28,
        'copy':COPY,'direction_count':1,'main_mechanism':'WHITE_TEA_NA_START_TO_REAL_S_LEAF_TERMINAL',
        'source_generation':k['INPUTS']['generated_png'],'source_generation_evidence':k['INPUTS']['generation_evidence'],
        'production_trace':k['INPUTS']['trace_svg'],'production_trace_commands':k['INPUTS']['source_commands'],
        'source_trace_provenance':k['INPUTS']['provenance'],'maker_source':ref(Path(__file__)),
        'reused_curve_helper':ref(BASE_MAKER),'method_readback':ref(OUT/'METHOD_AND_AUTHORIZATION.md'),
        'independent_art_direction':ref(ROOT/'evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/audit/INDEPENDENT_V28_ART_DIRECTION.json'),
        'local_method':ref(ROOT/'generation/RESTAURANT_POSTER_IMAGE_RULES_V1.md'),
        'local_method_sections':[6,7],'source_roles':SOURCES,'original_paths':17,'original_contours':21,
        'original_contours_bound_once':True,'replacement_details':details,'glyph_geometry':geometry,
        'source_specific_lettering':True,'standalone_complete_portable_Tea_glyph_claimed':False,
        'leaf_seam_observation':{'actual_source_sha256':'7fd7777fed21100cb6b47bc305701476054263565e73246ac469d065aa080618',
            'source_native_coordinates':'approximately(824,663) upper-left narrow start; (987,758) lower-right tip',
            'white_closed_vector_endpoint_native':[825,663],'inspection':ref(ROOT/'.liu-visual-private/correct_source_typography/v28/S-leaf-original-inspection.png'),
            'exact_photographic_segmentation_claimed':False},
        'preserved_glyph_parts':['Tea grass head','Tea human centre','Tea wood vertical','Tea wood left-falling stroke','all other source glyph contours including comma'],
        'reading_structure':'Original first-row ideographic frame, natural One centre-bar; second phrase uses original-row ink offsets and a common lower reading edge near555. No per-letter rotation or V27 stair-step.',
        'object_exclusion':'Fixed original cup_air/leaf_air replay only; no new photographic mask. Builder records actual empty/nonempty intersections explicitly.',
        'libraries':{'python':sys.version,'Pillow':PIL.__version__,'FontTools':helper.fontTools.__version__},
        'new_imagegen_calls':0,'new_production_traces':0,'font_files_for_final_outlines':0,
        'photo_patch_mask_filter_reconstruction_operations':0,'business_state_writes':0,'Figma_Drive_Git_writes':0,
        'aesthetic_pass_claimed':False,'limitations':['The photograph supplies the later Tea right-na, so lettering is specific to this S composition.',
            'Authored Tea component is local reauthoring, not a lossless alpha transform.',
            'Product handoff and readability need fresh independent pixel review.']}
    return program,notes

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write',action='store_true')
    mode.add_argument('--verify-only',action='store_true')
    args=parser.parse_args()
    paths=[OUT/'V28_GLYPH_EDIT_MANIFEST.json',OUT/'SOURCE_REAUTHORING_NOTES.json']
    gate=root_write_gate() if args.write else None
    if args.write:
        assert not any(p.exists() for p in paths),'PROGRAM_ALREADY_EXISTS'
    program,notes=build_program()
    for p,value in zip(paths,[program,notes]):
        raw=jb(value)
        if args.write:
            with p.open('xb') as f:f.write(raw)
        assert p.read_bytes()==raw,'EXACT_PROGRAM_READBACK_MISMATCH'
    print(json.dumps({'action':'authored-one-V28-program' if args.write else 'verified-existing',
        'formal_version':28,'writes':2 if args.write else 0,'root_gate':gate,
        'manifest':ref(paths[0]),'notes':ref(paths[1]),'source_contours':21,
        'aesthetic_pass_claimed':False},ensure_ascii=False))

if __name__=='__main__':
    main()
