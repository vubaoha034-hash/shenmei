"""Actual private V24 edit/dependency controls; no Figma or taste approval."""
from pathlib import Path
import argparse
import copy
import io
import json
import sys
import time
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from PIL import Image
from visual_memory import vpd_registered_type_composite as g
from visual_memory import vpd_registered_type_edited_lineage as e

PRIVATE = ROOT / '.liu-visual-private/composite-guard-probe/edited-lineage-v24'
AUDIT = ROOT / 'evidence/vpd/codex_takeover_20261003/audit'


def jb(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def save(name, raw):
    path = PRIVATE / name
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        g.require(path.read_bytes() == raw, 'EDIT_PROBE_FILE_CONFLICT:' + name)
    else:
        with path.open('xb') as stream:
            stream.write(raw)
    return g.ref(ROOT, path)


def geometry():
    library = e.pathops_runtime(ROOT)

    def rect(x0, y0, x1, y1):
        return e.make_path(library, [[{'op': 'moveTo', 'points': [[x0, y0]]},
            {'op': 'lineTo', 'points': [[x1, y0]]}, {'op': 'lineTo', 'points': [[x1, y1]]},
            {'op': 'lineTo', 'points': [[x0, y1]]}, {'op': 'closePath', 'points': []}]])

    a, b = rect(0, 0, 10, 10), rect(5, 5, 15, 15)
    intersection = library.op(a, b, library.PathOp.INTERSECTION, **e.FLAGS)
    union = library.op(a, b, library.PathOp.UNION, **e.FLAGS)
    hole = library.op(a, rect(3, 3, 7, 7), library.PathOp.DIFFERENCE, **e.FLAGS)
    arch = e.make_path(library, e.parse_closed('M0 0 C0 10 10 10 10 0 L0 0 Z'))
    curved = library.op(arch, rect(-10, -10, 5, 20), library.PathOp.DIFFERENCE, **e.FLAGS)
    g.require(intersection.area == 25 and union.area == 175, 'PATHOPS_RECTANGLE_CONTROL_FAILED')
    g.require(hole.area == 84 and not hole.contains((5, 5)) and hole.contains((1, 1)), 'PATHOPS_HOLE_CONTROL_FAILED')
    g.require(arch.area == 60 and curved.area == 30 and curved.bounds == (5.0, 0.0, 10.0, 7.5)
        and curved.contains((7, 2)) and not curved.contains((2, 2))
        and any(v == library.PathVerb.CUBIC for v, points in curved), 'PATHOPS_BEZIER_CONTROL_FAILED')
    repeated = library.op(arch, rect(-10, -10, 5, 20), library.PathOp.DIFFERENCE, **e.FLAGS)
    g.require(e.path_d(curved) == e.path_d(repeated), 'PATHOPS_REPEAT_CONTROL_FAILED')
    return {'pathops': library.__version__, 'python': sys.version.split()[0], 'intersection_area': 25,
        'union_area': 175, 'hole_area': 84, 'hole_center_excluded': True,
        'arch_area': 60, 'curved_difference_area': 30, 'curved_bounds': list(curved.bounds),
        'cubic_retained': True, 'repeat_segments_equal': True}


def dependency_evidence(observed):
    dep = ROOT / e.DEPDIR
    files = ['pypi-0.9.2.json', 'upstream-tree.json', 'upstream-source/LICENSE',
        'upstream-source/README.md', 'upstream-source/src/python/pathops/operations.py',
        'upstream-source/src/python/pathops/_pathops.pyx', 'upstream-source/tests/operations_test.py',
        'upstream-source/tests/pathops_test.py', 'skia_pathops-0.9.2-cp310-abi3-win_amd64.whl']
    metadata = json.loads((dep / 'pypi-0.9.2.json').read_text(encoding='utf-8'))
    wheel = next(u for u in metadata['urls'] if u['filename'] == files[-1])
    return {'schema': 'vpd-private-pathops-dependency-evidence/v1', 'package': 'skia-pathops',
        'version': '0.9.2', 'upstream_commit': 'c11e91f442462d1efc1a45d76c76ae9e74aa0de4',
        'primary_sources': ['https://pypi.org/project/skia-pathops/0.9.2/',
            'https://api.github.com/repos/fonttools/skia-pathops/git/trees/c11e91f442462d1efc1a45d76c76ae9e74aa0de4?recursive=1',
            'https://raw.githubusercontent.com/fonttools/skia-pathops/c11e91f442462d1efc1a45d76c76ae9e74aa0de4/LICENSE'],
        'license': 'BSD-3-Clause; full upstream and bundled wheel notices retained unchanged',
        'wheel': {'url': wheel['url'], 'bytes': wheel['size'], 'sha256': wheel['digests']['sha256'],
            'tag': 'cp310-abi3-win_amd64', 'requires_python': wheel['requires_python']},
        'runtime_dependencies': [r for r in metadata['info']['requires_dist'] or [] if 'extra ==' not in r],
        'actual_install': {'command': 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe -m pip install --no-index --no-deps --no-cache-dir --no-compile --target .liu-visual-private/dependencies/skia_pathops_0_9_2_abi3/site-packages .liu-visual-private/dependencies/skia_pathops_0_9_2_abi3/skia_pathops-0.9.2-cp310-abi3-win_amd64.whl',
            'chunk': '1902b2', 'exit_code': 0, 'built_from_source': False},
        'actual_probe': {'command': 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe scripts/vpd_probe_registered_type_edited_lineage.py --dependency-only --write-evidence',
            'exit_code': 0, 'geometry': observed},
        'read_before_install': ['full LICENSE and README', 'operations.py union/difference wrappers',
            '_pathops.pyx path/op signatures and behavior', 'official geometry tests'],
        'downloaded_inputs': [g.ref(ROOT, dep / n) for n in files],
        'installed_bound_files': e.PATHOPS_FILES,
        'retained_failures': ['initial GitHub web open InternalError', 'first urllib GitHub API TLS EOF; authorized-UA retry succeeded without disabling TLS', 'README.rst HTTP404; actual README.md fetched'],
        'limitations': ['PyPI publisher-commit attestation observed; no independent Sigstore verification performed',
            'Skia uses float32 coordinates; small signed area roundoff is recorded',
            'Library arithmetic is not typography recognition or aesthetic approval'],
        'paid_calls': 0, 'business_state_writes': 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dependency-only', action='store_true')
    parser.add_argument('--write-evidence', action='store_true')
    args = parser.parse_args()
    start = time.monotonic()
    observed = geometry()
    if args.dependency_only:
        result = dependency_evidence(observed)
        if args.write_evidence:
            path = AUDIT / 'SKIA_PATHOPS_0_9_2_DEPENDENCY_EVIDENCE.json'
            with path.open('xb') as stream:
                stream.write(jb(result))
        print(json.dumps({'result': 'PASS', 'geometry': observed, 'seconds': round(time.monotonic() - start, 3)}))
        return
    tests = []

    def reject(name, operation, error_code):
        try:
            operation()
        except (ValueError, KeyError, IndexError) as error:
            g.require(error_code in str(error), 'WRONG_EDIT_REJECTION:' + name + ':' + str(error))
            tests.append({'test': name, 'result': 'REJECTED', 'actual': str(error)})
            return
        raise AssertionError('NEGATIVE_EDIT_ACCEPTED:' + name)

    baseline = json.loads((PRIVATE / 'sealed-22-23-before-adaptation.json').read_text(encoding='utf-8'))
    for v in (22, 23):
        registration = g.ref(ROOT, ROOT / (g.SERIES + f'v{v}/REGISTERED_TYPE_COMPOSITE.json'))
        expected, overlay, reg = g.replay(ROOT, registration)
        actual = {'registration': reg, 'expected_RGB_sha256': g.sha(expected.tobytes()),
            'overlay_RGBA_sha256': g.sha(overlay.tobytes()), 'complete_compare_result': g.compare_pixels(ROOT,
                registration, g.ref(ROOT, ROOT / f'.liu-visual-private/correct_source_typography/v{v}/poster.png'),
                g.ref(ROOT, ROOT / f'.liu-visual-private/correct_source_typography/v{v}/figma-raw.png'))}
        g.require(actual == baseline[str(v)], 'SEALED_OLD_RETURN_CHANGED:' + str(v))
        tests.append({'test': f'V{v}_complete_registration_pixels_and_compare_return_unchanged', 'result': 'PASS'})
    manifest = json.loads(e.checked(ROOT, e.SEALED_EDIT))
    svg, detailed = e.replay_edit_program(ROOT, manifest)
    headline = g.ref(ROOT, ROOT / (e.BASE + 'headline.svg'))
    g.require(g.checked_bytes(ROOT, headline) == svg, 'ACTUAL_MAKER_SVG_BYTES_DIFFER')
    lineage = e.expected_lineage(g.EDIT_KERNEL)
    reg = g.register(ROOT, 24, headline, lineage)
    rr = save('actual-v24-registration.json', jb(reg))
    expected, overlay, unused = g.replay(ROOT, rr)
    buf = io.BytesIO(); expected.save(buf, format='PNG')
    final = save('actual-v24-control.png', buf.getvalue())
    checked = g.compare_pixels(ROOT, rr, final)
    tests.append({'test': 'actual_V24_retrace_edit_difference_final_SVG_and_full_frame_source_over',
        'result': 'PASS', 'whole_frame': checked['whole_frame_expected'],
        'core_covered': checked['core_alpha_positive_pixels'], 'core_uncovered': checked['core_alpha_zero_pixels']})
    bad = copy.deepcopy(manifest); bad['glyphs'][0]['edits'][0]['before_sha256'] = '0' * 64
    reject('incorrect_source_contour_before', lambda: e.replay_edit_program(ROOT, bad), 'EDIT_BEFORE_CONTOUR_MISMATCH')
    bad = copy.deepcopy(manifest); bad['glyphs'][4]['source'][1]['contour_indices'].pop()
    reject('hidden_source_contour_omission', lambda: e.replay_edit_program(ROOT, bad), 'EDIT_SOURCE_CONTOUR_OMITTED')
    bad = copy.deepcopy(manifest); bad['negative_space']['operation'] = 'skip'
    reject('omitted_cup_leaf_difference', lambda: e.replay_edit_program(ROOT, bad), 'EDIT_EXCLUSION_PARAMETERS_CHANGED')
    bad = copy.deepcopy(manifest); bad['glyphs'][0]['edits'][0]['after_contours'][0][-1]['op'] = 'lineTo'
    reject('open_authored_contour', lambda: e.replay_edit_program(ROOT, bad), 'EDIT_CLOSED_CONTOUR_REQUIRED')
    bad = copy.deepcopy(manifest); bad['glyphs'][0]['edits'][0]['op'] = 'execute_python'
    reject('arbitrary_maker_code_operation', lambda: e.replay_edit_program(ROOT, bad), 'EDIT_OPERATION_FORBIDDEN')
    bad = copy.deepcopy(lineage); bad['edit_manifest']['sha256'] = '0' * 64
    reject('self_asserted_alternate_manifest', lambda: g.register(ROOT, 24, headline, bad), 'V24_EDIT_PROFILE_CHANGED')
    tree = g.svg_tree(svg); tree[0].set('opacity', '.5')
    altered = save('unregistered-half-alpha.svg', ET.tostring(tree))
    reject('unregistered_alpha', lambda: g.register(ROOT, 24, altered, lineage), 'EDIT_FINAL_SVG_REPLAY_MISMATCH')
    tree = g.svg_tree(svg); tree[0].set('transform', 'translate(1 0)')
    altered = save('unregistered-geometry.svg', ET.tostring(tree))
    reject('unregistered_geometry', lambda: g.register(ROOT, 24, altered, lineage), 'EDIT_FINAL_SVG_REPLAY_MISMATCH')
    reject('edited_kind_future25_fail_closed', lambda: g.register(ROOT, 25, headline, lineage), 'EDIT_LINEAGE_V24_ONLY')
    core = g.core_mask(ROOT)
    p = next((x, y) for y in range(g.SIZE[1]) for x in range(g.SIZE[0]) if core.getpixel((x, y)))
    broken = expected.copy(); rgb = list(broken.getpixel(p)); rgb[0] ^= 1; broken.putpixel(p, tuple(rgb))
    buf = io.BytesIO(); broken.save(buf, format='PNG')
    altered = save('one-core-channel-wrong.png', buf.getvalue())
    reject('one_actual_core_channel_wrong', lambda: g.compare_pixels(ROOT, rr, altered), 'UNEXPLAINED_COMPOSITE_PIXEL_CHANGE')
    from visual_memory.vpd_correct_source_worker import compare_pixels as old_compare
    t = json.loads((ROOT / (g.SERIES + 'v21/TECHNICAL_CHECK.json')).read_text(encoding='utf-8'))
    old_compare(ROOT, t, t['overlay_envelopes'])
    tests.append({'test': 'unchanged_V21_pixel_gate', 'result': 'PASS'})
    result = {'schema': 'vpd-edited-lineage-v24-controls/v1', 'result': 'PASS', 'exit_code': 0,
        'actual_command': 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe scripts/vpd_probe_registered_type_edited_lineage.py --write-evidence',
        'seconds': round(time.monotonic() - start, 3), 'tests': tests, 'test_count': len(tests),
        'code': [g.ref(ROOT, ROOT / 'visual_memory/vpd_registered_type_composite.py'),
                 g.ref(ROOT, ROOT / 'visual_memory/vpd_registered_type_edited_lineage.py'), g.ref(ROOT, __file__)],
        'actual_edit_manifest': e.SEALED_EDIT, 'actual_maker_source': e.SEALED_MAKER,
        'actual_maker_builder': e.SEALED_BUILDER, 'dependencies': observed,
        'baseline': g.ref(ROOT, PRIVATE / 'sealed-22-23-before-adaptation.json'),
        'inputs': e.INPUTS, 'private_controls_only': True, 'real_Figma_checked': False,
        'limits': ['Correct Chinese meaning and visual effect require real image review',
            'Actual V24 Figma runtime/capture/export binding remains unsupported pending real evidence',
            'Source PNG alpha128 trace approximates its raster edge; edited contours are explicitly reauthored',
            'Skia float32 area changes may include small signed numeric roundoff'],
        'source_photography_edited': False, 'paid_calls': 0, 'business_state_writes': 0}
    if args.write_evidence:
        path = AUDIT / 'REGISTERED_TYPE_EDITED_LINEAGE_V24_TESTS.json'
        with path.open('xb') as stream:
            stream.write((json.dumps(result, ensure_ascii=False, indent=1) + '\n').encode('utf-8'))
    print(json.dumps({'result': 'PASS', 'tests': len(tests), 'seconds': result['seconds']}))


if __name__ == '__main__':
    main()
