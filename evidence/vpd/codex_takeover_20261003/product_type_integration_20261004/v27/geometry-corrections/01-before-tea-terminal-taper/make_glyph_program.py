"""V27: one cup-rim / fresh-leaf / platter-organized writing composition.

Reuse the source-bound V26 curve housekeeping unchanged. Author only the cup
arc in the original One contour, the right falling Tea stroke, and seven poses.
No generation, production tracing, fonts, photograph edit, or business write.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import importlib.util
import json
import sys

sys.dont_write_bytecode = True
# Load the healthy bundled Pillow before the bound V26 FontTools helper.
import PIL

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
BASE_MAKER = ROOT / 'evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v26/make_glyph_program.py'
BASE_MAKER_SHA = '514e370da517fdb47981d02e4e11a914a68087bcd7c4c251cf18773212578b80'
assert hashlib.sha256(BASE_MAKER.read_bytes()).hexdigest() == BASE_MAKER_SHA
spec = importlib.util.spec_from_file_location('bound_v26_curve_housekeeping', BASE_MAKER)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
g = helper.g
COPY = '一杯茶，慢下来'
SOURCES = helper.SOURCES

# A cup-width first body with a falling Tea terminal, then a smaller descending
# phrase seated in the original dry-tea / platter field. These are one authored
# composition, not alternative poses selected by an aesthetic score.
POSES = {'一': (.340, 331, 515), '杯': (.342, 457, 403),
         '茶': (.360, 625, 407), '，': (.310, 876, 539),
         '慢': (.370, 1018, 548), '下': (.320, 1155, 581),
         '来': (.230, 1251, 605)}

# The existing Tea lower-right component is the falling 木 stroke. Its authoring
# coordinates retain the original starting region and extend its complete outer
# and inner edges around the cup's right rim towards the original leaf diagonal.
# It is a glyph stroke; no leaf symbol, connector, mask or extra contour is added.
TEA_FALLING_STROKE = [
    {'op': 'moveTo', 'points': [[1009, 378]]},
    {'op': 'curveTo', 'points': [[1028, 380], [1058, 403], [1084, 420]]},
    {'op': 'curveTo', 'points': [[1180, 473], [1290, 456], [1410, 625]]},
    {'op': 'curveTo', 'points': [[1370, 636], [1348, 646], [1327, 630]]},
    {'op': 'curveTo', 'points': [[1250, 539], [1200, 505], [1122, 487]]},
    {'op': 'curveTo', 'points': [[1072, 462], [1018, 459], [1009, 378]]},
    {'op': 'closePath', 'points': []},
]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def jb(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def ref(path):
    path = Path(path).resolve()
    assert path.is_relative_to(ROOT.resolve())
    raw = path.read_bytes()
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': sha(raw), 'bytes': len(raw)}


def root_write_gate():
    raw = (ROOT / 'continuity/vpd/CURRENT_TASK_LOCK.json').read_bytes()
    lock = json.loads(raw)
    unit = lock['codex_takeover']['worker_continuation']
    last = unit['versions'][-1]
    assert (lock['revision'] == 328 and unit['phase'] == 'REVISION_REQUIRED'
            and unit['unit_id'] == 'CHAZUO_APPROVED_SOURCE_TYPOGRAPHY_20261003_R1'
            and last['number'] == 26 and last['verdict'] == 'AI_FAIL'), 'ROOT_V27_GO_GATE_NOT_SATISFIED'
    return {'revision': 328, 'phase': unit['phase'], 'last_version': 26,
            'last_verdict': 'AI_FAIL', 'lock_sha256': sha(raw),
            'explicit_root_go': 'GO_V27', 'root_validation_chunk': 'b31b2d',
            'root_independent_readback_chunk': '07a1f5'}


def cup_arc_warp(pi, ci, point, center):
    x, y = helper.local_warp(pi, ci, point, center)
    if pi == 4:
        # The original writing's inner/outer edges receive the same smooth bend.
        # This adds cup-rear-arc rise to the left part without equalizing weight.
        u = min(1.0, max(0.0, (x - 68.0) / (403.062017578125 - 68.0)))
        y += 50.0 * (1.0 - u) ** 2
    return [x, y]


def build_program():
    kernel = g.edited_kernel(ROOT)
    original = json.loads(kernel['checked'](ROOT, kernel['INPUTS']['source_commands']))
    kernel['checked'](ROOT, kernel['INPUTS']['trace_svg'])
    kernel['checked'](ROOT, kernel['INPUTS']['art_direction'])
    assert original['path_count'] == 17
    glyphs, accounted, details, geometry = [], [], [], []
    for char in COPY:
        source_rows, work = [], {}
        for pi in SOURCES[char]:
            contours = original['paths'][pi]['closed_contours']
            source_rows.append({'path_index': pi, 'contour_indices': list(range(len(contours)))})
            for ci, before in enumerate(contours):
                box = helper.bounds([before])
                center = [(box[0] + box[2]) / 2, (box[1] + box[3]) / 2]
                if pi == 8:
                    assert ci == 0
                    after = copy.deepcopy(TEA_FALLING_STROKE)
                    merges, max_shift = [], None
                    method = 'Complete original lower-right Tea stroke replaced with the explicitly authored tapered falling curve; its before hash and semantic ownership remain bound.'
                else:
                    warped = copy.deepcopy(before)
                    max_shift = 0.0
                    for row in warped:
                        for index, point in enumerate(row['points']):
                            moved = cup_arc_warp(pi, ci, point, center)
                            max_shift = max(max_shift, helper.distance(point, moved))
                            row['points'][index] = moved
                    assert max_shift <= 50.0001
                    after, merges = helper.tidy_curves(warped)
                    method = 'Original natural-writing contour retained with the fixed V26 local housekeeping; One additionally receives one smooth cup-rear-arc warp applied to both stroke edges.'
                kernel['closed_commands'](after)
                work[(pi, ci)] = after
                details.append({'char': char, 'path_index': pi, 'contour_index': ci,
                                'source_before_sha256': helper.commands_sha(before),
                                'source_bounds': box, 'original_commands': len(before),
                                'authored_commands': len(after), 'joined_curve_segments': merges,
                                'maximum_source_node_move_px': max_shift,
                                'pointwise_bound_applicable': pi != 8,
                                'component_reauthoring': pi == 8,
                                'method': method, 'required_stroke_removed': False,
                                'original_contour_ownership_retained': True})
        local_bounds = helper.bounds(list(work.values()))
        origin, edits = local_bounds[:2], []
        for pi in SOURCES[char]:
            for ci, before in enumerate(original['paths'][pi]['closed_contours']):
                after = copy.deepcopy(work[(pi, ci)])
                for row in after:
                    row['points'] = [[p[0] - origin[0], p[1] - origin[1]] for p in row['points']]
                kernel['closed_commands'](after)
                edits.append({'op': 'replace_contour', 'path_index': pi, 'contour_index': ci,
                              'before_sha256': helper.commands_sha(before), 'after_contours': [after],
                              'reason': next(r['method'] for r in details if r['path_index'] == pi and r['contour_index'] == ci)})
                accounted.append((pi, ci))
        scale, tx, ty = POSES[char]
        glyphs.append({'char': char, 'source': source_rows, 'edits': edits,
                       'placement': {'scale': scale, 'tx': tx, 'ty': ty}})
        geometry.append({'char': char, 'source_local_origin': origin,
                         'authored_source_bounds': local_bounds,
                         'placement': {'scale': scale, 'tx': tx, 'ty': ty},
                         'pre_exclusion_ink_bounds': [tx, ty,
                             tx + scale * (local_bounds[2] - origin[0]),
                             ty + scale * (local_bounds[3] - origin[1])]})
    expected = [(row['path_index'], ci) for row in original['paths']
                for ci in range(len(row['closed_contours']))]
    assert sorted(accounted) == sorted(expected) and len(accounted) == len(set(accounted)) == 21
    program = {'schema': 'vpd-source-bound-glyph-edits/v1', 'formal_version': 27,
               'copy': COPY, 'source_trace': kernel['INPUTS']['trace_svg'], 'glyphs': glyphs,
               'negative_space': {'art_direction': kernel['INPUTS']['art_direction'],
                                  'operation': 'difference-union', 'fix_winding': True,
                                  'keep_starting_points': True, 'clockwise': False}}
    notes = {'schema': 'vpd-v27-product-organized-natural-writing/v1', 'formal_version': 27,
             'copy': COPY, 'direction_count': 1, 'phrase_group_count': 2,
             'single_main_change': 'CUP_ARC_LEAF_FALLING_TERMINAL_AND_DESCENDING_PLATTER_PHRASE',
             'source_generation': kernel['INPUTS']['generated_png'],
             'source_generation_evidence': kernel['INPUTS']['generation_evidence'],
             'production_trace': kernel['INPUTS']['trace_svg'],
             'production_trace_commands': kernel['INPUTS']['source_commands'],
             'source_trace_provenance': kernel['INPUTS']['provenance'],
             'maker_source': ref(Path(__file__)), 'reused_curve_helper': ref(BASE_MAKER),
             'method_sources': ref(OUT / 'PROFESSIONAL_METHOD_READBACK.md'),
             'source_roles': SOURCES, 'original_path_count': 17, 'original_contour_count': 21,
             'original_contours_accounted_once': True, 'dropped_source_contours': [],
             'replacement_details': details, 'glyph_geometry': geometry,
             'design_basis': {
                 'cup': 'The first phrase body spans the actual cup mouth, with One bending upwards through the left cup-rim direction. Cup and Tea retain their original writing skeletons above the rear rim; the Tea falling stroke curves outside the right rim.',
                 'leaf': 'The complete Tea lower-right wood stroke extends down-right towards the original fresh-leaf diagonal. Its authored inner and outer edges preserve a tapered brush gesture; no detached leaf or connecting graphic is added.',
                 'platter': 'Slow, Down and Come progressively descend and reduce in scale through the upper-right dry-tea/platter field. The rightmost terminal ends by the original right platter rim. This intentionally places part of the phrase over original dark dry tea.',
                 'rhythm': 'A cup-width first body and a separated, diminishing second group replace the equal-weight horizontal sentence; the comma remains a complete source glyph.'},
             'negative_space': 'Unchanged original CUP_AIR and LEAF_AIR are replayed by the finite kernel. Builder requires the actual glyph/exclusion intersection to be empty, preventing key-stroke truncation. The reported pre/post floating area integration may still differ slightly.',
             'preserved_evidence': 'V26 full copy and comma were readable and contrast was sufficient. Reuse its natural source curves and fixed counter/terminal housekeeping instead of a thin uniform redraw.',
             'formal_26_failure': ref(ROOT / 'evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v26/pixel_review/PIXEL_REVIEW.json'),
             'formal_26_evidence_limitations': ref(ROOT / 'evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v26/REVIEW_EVIDENCE_LIMITATIONS.json'),
             'libraries': {'Python': sys.version, 'Pillow': PIL.__version__,
                           'FontTools': helper.fontTools.__version__,
                           'FontTools_role': 'BoundsPen for authored curves; no font file'},
             'new_imagegen_calls': 0, 'new_production_traces': 0, 'font_files_loaded': 0,
             'reference_outlines_copied': 0, 'business_state_writes': 0, 'Figma_Drive_Git_writes': 0,
             'aesthetic_pass_claimed': False, 'human_acceptance_claimed': False,
             'limitations': ['The long Tea falling component is locally reauthored, not a lossless transformation of the original stroke.',
                             'The fixed source kernel uses sample-based VTracer source evidence and float32 Skia operations.',
                             'The second phrase covers some dry-tea pixels through ordinary source-over; no exact object segmentation is claimed.',
                             'Product integration and the readability of the new curved phrase require fresh independent pixel review.']}
    return program, notes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--write', action='store_true')
    modes.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    outputs = [OUT / 'V27_GLYPH_EDIT_MANIFEST.json', OUT / 'SOURCE_REAUTHORING_NOTES.json']
    gate = root_write_gate() if args.write else None
    if args.write:
        assert not any(path.exists() for path in outputs), 'AUTHORED_PROGRAM_ALREADY_EXISTS'
    program, notes = build_program()
    if args.write:
        for path, value in zip(outputs, [program, notes]):
            with path.open('xb') as handle:
                handle.write(jb(value))
    for path, value in zip(outputs, [program, notes]):
        assert path.read_bytes() == jb(value), 'AUTHORED_PROGRAM_EXACT_READBACK_MISMATCH'
    print(json.dumps({'action': 'authored-one-program' if args.write else 'verified-existing',
                      'formal_version': 27, 'writes': len(outputs) if args.write else 0,
                      'root_write_gate': gate, 'manifest': ref(outputs[0]), 'notes': ref(outputs[1]),
                      'source_contours': 21, 'authored_closed_contours': 21,
                      'aesthetic_pass_claimed': False}, ensure_ascii=True))


if __name__ == '__main__':
    main()
