"""V26: reuse actual V24 writing curves in one product-organized headline.

No new generation or production trace. The bounded operations preserve natural
stroke variation, tidy redundant curve joins, shorten specified terminal regions,
and open four existing counters. All 21 original contours remain hash-bound.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import json
import math
import sys

sys.dont_write_bytecode = True
# Load the healthy bundled PIL first; Hermes is used only during FontTools import.
import PIL
from PIL import Image
HERMES_FT = 'C:/Users/Administrator/AppData/Local/hermes/hermes-agent/venv/Lib/site-packages'
sys.path.append(HERMES_FT)
try:
    import fontTools
    from fontTools.pens.boundsPen import BoundsPen
finally:
    sys.path.remove(HERMES_FT)

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from visual_memory import vpd_registered_type_composite as g

COPY = '一杯茶，慢下来'
SOURCES = {'一': [4], '杯': [0, 2, 6], '茶': [1, 3, 5, 8, 9],
           '，': [7], '慢': [11, 12, 15, 16], '下': [13], '来': [10, 14]}
# One natural rising/falling line, not a selection among layouts. The cup word
# sits over the actual cup's outer-right rim; the second phrase stops above the
# original leaf tips and platter field. Every key stroke stays above bright water.
POSES = {'一': (.260, 535, 477), '杯': (.296, 642, 421),
         '茶': (.295, 783, 404), '，': (.270, 910, 493),
         '慢': (.314, 943, 409), '下': (.324, 1067, 412),
         '来': (.296, 1181, 402)}
FIT_LIMIT_SOURCE_PX = 1.0
MAX_JOINED_SOURCE_SEGMENTS = 6
MAX_JOIN_ANGLE_DEG = 12.0
MAX_END_ANGLE_DEG = 8.0
COUNTER_EXPANSIONS = {(11, 1): (1.08, 1.035), (12, 1): (1.08, 1.04),
                      (12, 2): (1.08, 1.04), (12, 3): (1.08, 1.04)}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def jb(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def commands_sha(contour):
    return sha(json.dumps(contour, ensure_ascii=False, sort_keys=True,
                          separators=(',', ':'), allow_nan=False).encode('utf-8'))


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
    assert (lock['revision'] == 326 and unit['phase'] == 'REVISION_REQUIRED'
            and unit['unit_id'] == 'CHAZUO_APPROVED_SOURCE_TYPOGRAPHY_20261003_R1'
            and last['number'] == 25 and last['verdict'] == 'AI_FAIL'), 'ROOT_V26_GO_GATE_NOT_SATISFIED'
    return {'revision': 326, 'phase': unit['phase'], 'last_version': 25,
            'last_verdict': 'AI_FAIL', 'lock_sha256': sha(raw),
            'explicit_root_go': 'GO_NATIVE326', 'root_validation_chunk': '78936e'}


def bounds(contours):
    pen = BoundsPen(None)
    for contour in contours:
        for row in contour:
            getattr(pen, row['op'])(*[tuple(p) for p in row['points']])
    assert pen.bounds is not None
    return list(pen.bounds)


def cubic(points, t):
    u = 1.0 - t
    weights = (u * u * u, 3 * u * u * t, 3 * u * t * t, t * t * t)
    return [sum(w * p[axis] for w, p in zip(weights, points)) for axis in (0, 1)]


def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def subtract(a, b):
    return [a[0] - b[0], a[1] - b[1]]


def angle(a, b):
    la, lb = math.hypot(*a), math.hypot(*b)
    if la < 1e-8 or lb < 1e-8:
        return 180.0
    return math.degrees(math.acos(max(-1.0, min(1.0, (a[0] * b[0] + a[1] * b[1]) / (la * lb)))))


def fit_join(components):
    """Fit only almost-tangent source joins; compare to all original samples.

    No raster rewrite, centerline extraction or font outline. Retain an explicit
    cubic only if 33 samples per source cubic deviate by <=1 source pixel, and
    endpoint directions remain within eight degrees. Sharp corners stay intact.
    """
    if not 2 <= len(components) <= MAX_JOINED_SOURCE_SEGMENTS:
        return None
    for left, right in zip(components, components[1:]):
        if angle(subtract(left[3], left[2]), subtract(right[1], right[0])) > MAX_JOIN_ANGLE_DEG:
            return None
    lengths = []
    for points in components:
        samples = [cubic(points, i / 32) for i in range(33)]
        lengths.append(sum(distance(a, b) for a, b in zip(samples, samples[1:])))
    total = sum(lengths)
    if not 1e-6 < total <= 170:
        return None
    sample_rows, start = [], 0.0
    for points, length in zip(components, lengths):
        for i in range(33):
            sample_rows.append(((start + length * i / 32) / total, cubic(points, i / 32)))
        start += length
    p0, p3 = components[0][0], components[-1][3]
    aa = ab = bb = 0.0
    rhs_a, rhs_b = [0.0, 0.0], [0.0, 0.0]
    for t, point in sample_rows:
        u = 1 - t
        a, b = 3 * u * u * t, 3 * u * t * t
        aa += a * a; ab += a * b; bb += b * b
        for axis in (0, 1):
            target = point[axis] - u * u * u * p0[axis] - t * t * t * p3[axis]
            rhs_a[axis] += a * target
            rhs_b[axis] += b * target
    determinant = aa * bb - ab * ab
    if determinant <= 1e-8:
        return None
    p1 = [(rhs_a[k] * bb - rhs_b[k] * ab) / determinant for k in (0, 1)]
    p2 = [(rhs_b[k] * aa - rhs_a[k] * ab) / determinant for k in (0, 1)]
    candidate = [p0, p1, p2, p3]
    error = max(distance(cubic(candidate, t), point) for t, point in sample_rows)
    if error > FIT_LIMIT_SOURCE_PX:
        return None
    if (angle(subtract(p1, p0), subtract(components[0][1], p0)) > MAX_END_ANGLE_DEG
            or angle(subtract(p3, p2), subtract(p3, components[-1][2])) > MAX_END_ANGLE_DEG):
        return None
    return candidate, error


def tidy_curves(contour):
    segments, current = [], contour[0]['points'][0]
    for row in contour[1:-1]:
        if row['op'] == 'curveTo':
            points = [copy.deepcopy(current)] + copy.deepcopy(row['points'])
            segments.append({'op': 'curveTo', 'points': copy.deepcopy(row['points']),
                             'components': [points], 'error': 0.0})
        else:
            assert row['op'] == 'lineTo'
            segments.append({'op': row['op'], 'points': copy.deepcopy(row['points'])})
        current = row['points'][-1]
    reduced, merges = [], []
    for segment in segments:
        if reduced and reduced[-1]['op'] == segment['op'] == 'curveTo':
            group = reduced[-1]['components'] + segment['components']
            result = fit_join(group)
            if result is not None:
                points, error = result
                reduced[-1] = {'op': 'curveTo', 'points': points[1:],
                               'components': group, 'error': error}
                merges.append({'source_segments': len(group), 'sample_max_deviation_source_px': error})
                continue
        reduced.append(segment)
    result = [copy.deepcopy(contour[0])]
    result += [{'op': row['op'], 'points': row['points']} for row in reduced]
    result.append(copy.deepcopy(contour[-1]))
    return result, merges


def local_warp(pi, ci, point, center):
    x, y = point
    if (pi, ci) in COUNTER_EXPANSIONS:
        sx, sy = COUNTER_EXPANSIONS[(pi, ci)]
        return [center[0] + sx * (x - center[0]), center[1] + sy * (y - center[1])]
    # Positive, continuous, bounded maps; only specified existing endpoint regions.
    if pi == 0 and y > 386:
        y = 386 + .92 * (y - 386)
    if pi == 2 and y > 400:
        y = 400 + .96 * (y - 400)
    if pi == 3 and x > 1086:
        x = 1086 + .82 * (x - 1086)
    if pi == 16 and x > 1000:
        y -= .075 * (x - 1000)
        x = 1000 + .88 * (x - 1000)
    if pi == 10 and x > 1615:
        y -= .035 * (x - 1615)
        x = 1615 + .86 * (x - 1615)
    return [x, y]


def build_program():
    kernel = g.edited_kernel(ROOT)
    original = json.loads(kernel['checked'](ROOT, kernel['INPUTS']['source_commands']))
    kernel['checked'](ROOT, kernel['INPUTS']['trace_svg'])
    kernel['checked'](ROOT, kernel['INPUTS']['art_direction'])
    assert original['path_count'] == 17
    glyphs, accounted, details, glyph_details = [], [], [], []
    for char in COPY:
        source_rows, work = [], {}
        for pi in SOURCES[char]:
            contours = original['paths'][pi]['closed_contours']
            source_rows.append({'path_index': pi, 'contour_indices': list(range(len(contours)))})
            for ci, before in enumerate(contours):
                box = bounds([before])
                center = [(box[0] + box[2]) / 2, (box[1] + box[3]) / 2]
                warped = copy.deepcopy(before)
                max_shift = 0.0
                for row in warped:
                    for index, point in enumerate(row['points']):
                        after_point = local_warp(pi, ci, point, center)
                        max_shift = max(max_shift, distance(point, after_point))
                        row['points'][index] = after_point
                assert max_shift <= 20.0, 'BOUNDED_SOURCE_NODE_MOVE_EXCEEDED'
                after, merges = tidy_curves(warped)
                work[(pi, ci)] = after
                details.append({'char': char, 'path_index': pi, 'contour_index': ci,
                                'source_before_sha256': commands_sha(before),
                                'source_bounds': box, 'original_commands': len(before),
                                'tidied_commands': len(after), 'joined_curve_segments': merges,
                                'maximum_source_node_move_px': max_shift,
                                'existing_counter_expansion': list(COUNTER_EXPANSIONS.get((pi, ci), (1, 1))),
                                'whole_original_contour_retained': True,
                                'required_stroke_removed': False})
        local_bounds = bounds(list(work.values()))
        origin = local_bounds[:2]
        edits = []
        for pi in SOURCES[char]:
            for ci, before in enumerate(original['paths'][pi]['closed_contours']):
                after = copy.deepcopy(work[(pi, ci)])
                for row in after:
                    row['points'] = [[p[0] - origin[0], p[1] - origin[1]] for p in row['points']]
                kernel['closed_commands'](after)
                reason = ('Retain this actual V24 natural writing contour and its stroke variation; '
                          'bounded tangent-join cleanup, specified terminal-region moves or existing '
                          'counter opening only, then normalize the whole glyph without changing its '
                          'relative contour ownership. No uniform thin skeleton redraw.')
                edits.append({'op': 'replace_contour', 'path_index': pi, 'contour_index': ci,
                              'before_sha256': commands_sha(before), 'after_contours': [after], 'reason': reason})
                accounted.append((pi, ci))
        scale, tx, ty = POSES[char]
        glyphs.append({'char': char, 'source': source_rows, 'edits': edits,
                       'placement': {'scale': scale, 'tx': tx, 'ty': ty}})
        glyph_details.append({'char': char, 'source_local_origin': origin,
                              'natural_edited_source_bounds': local_bounds,
                              'placement': {'scale': scale, 'tx': tx, 'ty': ty},
                              'pre_exclusion_ink_bounds': [tx, ty,
                                  tx + scale * (local_bounds[2] - origin[0]),
                                  ty + scale * (local_bounds[3] - origin[1])]})
    expected = [(row['path_index'], ci) for row in original['paths']
                for ci in range(len(row['closed_contours']))]
    assert sorted(accounted) == sorted(expected) and len(accounted) == len(set(accounted)) == 21
    assert sum(row['original_commands'] - row['tidied_commands'] for row in details) > 0
    program = {'schema': 'vpd-source-bound-glyph-edits/v1', 'formal_version': 26,
               'copy': COPY, 'source_trace': kernel['INPUTS']['trace_svg'], 'glyphs': glyphs,
               'negative_space': {'art_direction': kernel['INPUTS']['art_direction'],
                                  'operation': 'difference-union', 'fix_winding': True,
                                  'keep_starting_points': True, 'clockwise': False}}
    notes = {'schema': 'vpd-v26-natural-source-curve-recovery/v1', 'formal_version': 26,
             'copy': COPY, 'direction_count': 1, 'line_count': 1,
             'single_main_change': 'RECOVER_REAL_SOURCE_WRITING_VARIATION_AND_ORGANIZE_PRODUCT_NEGATIVE_SPACE',
             'source_generation': kernel['INPUTS']['generated_png'],
             'source_generation_evidence': kernel['INPUTS']['generation_evidence'],
             'production_trace': kernel['INPUTS']['trace_svg'],
             'production_trace_commands': kernel['INPUTS']['source_commands'],
             'source_trace_provenance': kernel['INPUTS']['provenance'],
             'maker_source': ref(Path(__file__)), 'source_roles': SOURCES,
             'original_path_count': 17, 'original_contour_count': 21,
             'original_contours_accounted_once': True, 'dropped_source_contours': [],
             'replacement_details': details, 'glyph_geometry': glyph_details,
             'cleanup': {'sampled_fit_tolerance_source_px': FIT_LIMIT_SOURCE_PX,
                         'samples_per_original_curve': 33,
                         'maximum_joined_source_segments': MAX_JOINED_SOURCE_SEGMENTS,
                         'join_angle_limit_degrees': MAX_JOIN_ANGLE_DEG,
                         'end_angle_limit_degrees': MAX_END_ANGLE_DEG,
                         'maximum_terminal_region_node_move_source_px': 20,
                         'original_and_final_inner_outer_edges_inspection_required': True,
                         'continuous_global_error_bound_claimed': False},
             'design_basis': {'cup': 'Cup letter ends over the physical cup outer-right rim, leaving original rim and tea visible beneath a shaped gap; original downward wood/vertical gestures remain.',
                              'leaf': 'The lower terminals of the latter phrase end above the rising leaf edge. The actual leaf silhouette occupies the continuous negative space underneath the phrase instead of being appended to a glyph.',
                              'platter': 'The latter phrase spans the original leaf/platter upper field while its major strokes stay in the dark upper background, before the bright water band.',
                              'writing': 'Original cubic shoulders, variable stroke bodies, turns and distinct terminals are retained. Source proportions replace V25 wide thin Tea and flat Slow frame. The larger title footprint is reorganized into one gently rising/falling line.'},
             'negative_space': 'Original fixed V24 CUP_AIR and LEAF_AIR applied only to glyph outlines. No photograph segmentation, patch-back, enlarged exclusion or core omission.',
             'formal_25_failure_read': ref(ROOT / 'evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v25/pixel_review/REVIEWER_OUTPUT.json'),
             'professional_method_read': ref(ROOT / 'evidence/vpd/codex_takeover_20261003/continuous_typography_20261004/tutorials/TUTORIAL_METHODS.md'),
             'source_alpha128_observation': 'The original RGBA has broad low-alpha outside noise; the existing alpha128/17-path trace contains smooth complete natural glyphs. Reuse is technically sufficient; no new transparent asset needed.',
             'libraries': {'Python': sys.version, 'Pillow': PIL.__version__, 'FontTools': fontTools.__version__,
                           'FontTools_role': 'BoundsPen evaluates actual existing authored curves; no font file loaded',
                           'FontTools_init_sha256': sha(Path(fontTools.__file__).read_bytes())},
             'new_imagegen_calls': 0, 'new_production_traces': 0,
             'font_files_loaded': 0, 'reference_outlines_copied': 0,
             'business_state_writes': 0, 'Figma_Drive_Git_writes': 0,
             'aesthetic_pass_claimed': False, 'human_acceptance_claimed': False,
             'limitations': ['Sample-bound cubic cleanup approximates source edges; not a lossless-alpha claim.',
                             'Real source writing curves are reused, not claimed newly hand-drawn from nothing.',
                             'Product relationship and writing improvement remain subject to fresh external pixel review.']}
    return program, notes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--write', action='store_true')
    modes.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    outputs = [OUT / 'V26_GLYPH_EDIT_MANIFEST.json', OUT / 'SOURCE_REAUTHORING_NOTES.json']
    gate = root_write_gate() if args.write else None
    if args.write:
        assert not any(path.exists() for path in outputs), 'AUTHORED_PROGRAM_ALREADY_EXISTS'
    program, notes = build_program()
    values = [program, notes]
    if args.write:
        assert not any(path.exists() for path in outputs), 'PROGRAM_APPEARED_DURING_BUILD'
        for path, value in zip(outputs, values):
            with path.open('xb') as handle:
                handle.write(jb(value))
    for path, value in zip(outputs, values):
        assert path.read_bytes() == jb(value), 'AUTHORED_PROGRAM_EXACT_READBACK_MISMATCH'
    print(json.dumps({'action': 'authored-one-program' if args.write else 'verified-existing',
                      'formal_version': 26, 'writes': len(outputs) if args.write else 0,
                      'root_write_gate': gate, 'manifest': ref(outputs[0]), 'notes': ref(outputs[1]),
                      'source_contours': 21, 'authored_closed_contours': 21,
                      'curve_commands_removed': sum(row['original_commands'] - row['tidied_commands']
                                                    for row in notes['replacement_details']),
                      'aesthetic_pass_claimed': False}, ensure_ascii=True))


if __name__ == '__main__':
    main()
