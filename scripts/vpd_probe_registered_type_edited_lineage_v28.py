"""Actual frozen V28 adapter controls; countercases use private copies only."""
from pathlib import Path
import argparse
import copy
import io
import json
import re
import sys
import time
import xml.etree.ElementTree as ET
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from PIL import ImageChops
from visual_memory import vpd_registered_type_composite as g
from visual_memory import vpd_registered_type_figma_binding as b
from visual_memory import vpd_registered_type_edited_lineage_v28 as e
PRIVATE = ROOT / '.liu-visual-private/guard-v28-proposal/actual-lineage'
AUDIT = ROOT / 'evidence/vpd/codex_takeover_20261003/audit/REGISTERED_TYPE_EDITED_LINEAGE_V28_TESTS.json'
BASELINE = {'path': '.liu-visual-private/guard-v28-proposal/OLD_22_23_24_25_26_27_BASELINE.json',
 'sha256': '888fe9360d3ac2a4d9fd596cb3f297f5851caf86eefd601fb78d04d5abb4b3fd'}
HEADLINE = {'path': 'evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v28/headline.svg',
 'sha256': 'c8a62fba20faf0d73620487e07a9f0f4a77fad060a18f967a6e96582cf96623a'}
PREVIEW = {'path': '.liu-visual-private/correct_source_typography/v28/preview.png',
 'sha256': '1000c0a35a43cf1cfb8803735cd00abb039d20147676254a1db57c2722f6a8ac'}

def jb(value):
    return (json.dumps(value, ensure_ascii=False, separators=(',', ':')) + '\n').encode('utf-8')

def save(name, raw):
    path = PRIVATE / name
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(raw)
    return g.ref(ROOT, path)

def first_point(mask):
    box = mask.getbbox()
    g.require(box is not None, 'ACTUAL_CONTROL_POINT_REQUIRED')
    return next(((x, y) for y in range(box[1], box[3]) for x in range(box[0], box[2]) if mask.getpixel((x, y))))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--actual', action='store_true', required=True)
    parser.parse_args()
    started = time.monotonic()
    checks = []
    baseline = json.loads(g.checked_bytes(ROOT, BASELINE))
    for version in (22, 23, 24, 25, 26, 27):
        prior = baseline['versions'][str(version)]
        rr, binding = (prior['registration_ref'], prior['actual_binding'])
        image, overlay, reg = g.replay(ROOT, rr)
        observed = {'registration_ref': rr, 'registration': reg, 'expected_RGB': {'mode': image.mode, 'size': list(image.size), 'bytes': len(image.tobytes()), 'sha256': g.sha(image.tobytes())}, 'overlay_RGBA': {'mode': overlay.mode, 'size': list(overlay.size), 'bytes': len(overlay.tobytes()), 'sha256': g.sha(overlay.tobytes()), 'alpha_sha256': g.sha(overlay.getchannel('A').tobytes())}, 'compare_pixels': g.compare_pixels(ROOT, rr, prior['compare_pixels']['final'], binding['raw_figma_export']), 'actual_binding': b.verify_actual_binding(ROOT, rr, binding['runtime_evidence'], binding['download_readback']), 'frozen_binding_check_ref': g.ref(ROOT, ROOT / prior['frozen_binding_check_ref']['path'])}
        g.require(observed == prior, 'OLD_COMPLETE_RETURN_CHANGED:' + str(version))
        original_pixels = baseline['replayed_pixel_files'][str(version)]
        g.require(image.tobytes() == g.checked_bytes(ROOT, original_pixels['expected_RGB']) and overlay.tobytes() == g.checked_bytes(ROOT, original_pixels['overlay_RGBA']) and overlay.getchannel('A').tobytes() == g.checked_bytes(ROOT, original_pixels['overlay_alpha']), 'OLD_COMPLETE_PIXEL_BYTES_CHANGED:' + str(version))
        checks.append({'case': f'old{version}_complete_registration_RGB_RGBA_compare_binding', 'result': 'PASS'})
        print(json.dumps({'old_version': version, 'complete_equal': True}), flush=True)
    g.require(g.edited_lineage(ROOT) == baseline['factories']['24'] and all((g.edited_lineage(ROOT, v) == baseline['factories'][str(v)] for v in (24, 25, 26, 27))), 'OLD_FACTORY_RETURN_CHANGED')
    checks.append({'case': 'default24_and_existing24_25_26_factories_unchanged', 'result': 'PASS'})
    lineage = g.edited_lineage(ROOT, 28)
    rr = save('actual-registration.json', jb(g.register(ROOT, 28, HEADLINE, lineage)))
    image, overlay, reg = g.replay(ROOT, rr)
    checked = g.compare_pixels(ROOT, rr, PREVIEW)
    compare_ref = save('actual-preview-composite-check.json', jb(checked))
    core = g.core_mask(ROOT)
    alpha_positive = overlay.getchannel('A').point(lambda v: 255 if v else 0)
    alpha_zero = ImageChops.invert(alpha_positive)
    headline_alpha = g.renderer(ROOT)(g.checked_bytes(ROOT, HEADLINE)).getchannel('A').point(lambda v: 255 if v else 0)
    checks.append({'case': 'actual28_sealed_profile_independent_replay_and_frozen_maker_preview', 'result': 'PASS', 'whole_frame': checked['whole_frame_expected'], 'core_covered': checked['core_alpha_positive_pixels'], 'core_uncovered': checked['core_alpha_zero_pixels']})

    def reject(name, operation, expected):
        try:
            operation()
        except ValueError as error:
            g.require(expected in str(error), 'WRONG_NEGATIVE:' + name + ':' + str(error))
            checks.append({'case': name, 'result': 'REJECTED', 'actual': str(error)})
            return
        raise AssertionError('NEGATIVE_ACCEPTED:' + name)
    manifest = json.loads(g.checked_bytes(ROOT, e.SEALED_EDIT))
    old_inputs = g.edited_kernel(ROOT, 24)['INPUTS']
    new_inputs = e.base_kernel(ROOT)['INPUTS']
    g.require({k:v for k,v in old_inputs.items() if k != 'art_direction'} == {k:v for k,v in new_inputs.items() if k != 'art_direction'} and lineage['art_direction'] == e.SEALED_GEOMETRY, 'V28_SINGLE_INPUT_SHIM_CHANGED')
    wrong_geometry = copy.deepcopy(manifest)
    wrong_geometry['negative_space']['art_direction'] = old_inputs['art_direction']
    save('wrong-old-negative-geometry.json', jb(wrong_geometry))
    reject('new28_old_geometry_reference_reuse', lambda: e.replay_edit_program(ROOT, wrong_geometry), 'EDIT_EXCLUSION_PARAMETERS_CHANGED')
    altered_geometry = json.loads(g.checked_bytes(ROOT, e.SEALED_GEOMETRY))
    altered_geometry['negative_space']['cup_air'] = altered_geometry['negative_space']['cup_air'].replace('M 318', 'M 319', 1)
    g.require(altered_geometry != json.loads(g.checked_bytes(ROOT, e.SEALED_GEOMETRY)), 'REAL_CUP_MUTATION_REQUIRED')
    altered_geometry_ref = save('wrong-cup-geometry.json', jb(altered_geometry))
    wrong_lineage = copy.deepcopy(lineage); wrong_lineage['art_direction'] = altered_geometry_ref
    reject('new28_unsealed_cup_geometry', lambda: g.register(ROOT, 28, HEADLINE, wrong_lineage), 'V28_EDIT_PROFILE_CHANGED')
    bad = copy.deepcopy(manifest)
    bad['glyphs'][0]['edits'][0]['before_sha256'] = '0' * 64
    save('wrong-source-before-contour.json', jb(bad))
    reject('actual_source_before_wrong', lambda: e.replay_edit_program(ROOT, bad), 'EDIT_BEFORE_CONTOUR_MISMATCH')
    tree = g.svg_tree(g.checked_bytes(ROOT, HEADLINE))
    path = list(tree.iter(g.NS + 'path'))[-1]
    d = path.get('d')
    last_c = list(re.finditer('C([^MLCZ]*)', d))[-1]
    numbers = list(re.finditer('[-+]?(?:\\d*\\.\\d+|\\d+\\.?\\d*)(?:[eE][-+]?\\d+)?', last_c[1]))
    g.require(len(numbers) == 6, 'ACTUAL_LAST_CUBIC_REQUIRED')
    first_control_x = numbers[0]
    start, stop = (last_c.start(1) + first_control_x.start(), last_c.start(1) + first_control_x.end())
    path.set('d', d[:start] + str(float(first_control_x[0]) + 1) + d[stop:])
    bad_svg = save('last-C-control-one-unit-wrong.svg', ET.tostring(tree))
    reject('actual_last_C_control_one_unit', lambda: g.register(ROOT, 28, bad_svg, lineage), 'EDIT_FINAL_SVG_REPLAY_MISMATCH')
    rgb_cases = [('actual28_headline_alpha_positive_noncore_one_RGB_unit', ImageChops.darker(headline_alpha, ImageChops.invert(core))), ('actual28_uncovered_core_one_RGB_unit', ImageChops.darker(core, alpha_zero))]
    if checked['core_alpha_positive_pixels']:
        rgb_cases.append(('actual28_covered_core_one_RGB_unit', ImageChops.darker(core, alpha_positive)))
    for name, mask in rgb_cases:
        point = first_point(mask)
        bad_image = image.copy()
        pixel = list(bad_image.getpixel(point))
        pixel[0] ^= 1
        bad_image.putpixel(point, tuple(pixel))
        buffer = io.BytesIO()
        bad_image.save(buffer, format='PNG')
        wrong_ref = save(name + '.png', buffer.getvalue())
        reject(name, lambda f=wrong_ref: g.compare_pixels(ROOT, rr, f), 'UNEXPLAINED_COMPOSITE_PIXEL_CHANGE')
        checks[-1]['point'] = list(point)
    reject('future29_registration', lambda: g.register(ROOT, 29, HEADLINE, lineage), 'EDIT_LINEAGE_V24_ONLY')
    reject('future29_factory', lambda: g.edited_lineage(ROOT, 29), 'INSPECTED_EDIT_VERSION_REQUIRED')
    for key in ('vpd_registered_type_edited_lineage', 'vpd_registered_type_edited_lineage_v25', 'vpd_registered_type_edited_lineage_v26', 'vpd_registered_type_edited_lineage_v27'):
        g.checked_bytes(ROOT, baseline['before_code'][key])
    report = {'schema': 'vpd-actual-v28-thin-edit-adapter-controls/v1', 'formal_version': 28, 'result': 'PASS', 'exit_code': 0, 'seconds': round(time.monotonic() - started, 3), 'cases': len(checks), 'checks': checks, 'actual_command': str(g.RUNTIME / 'python/python.exe') + ' -B -u scripts/vpd_probe_registered_type_edited_lineage_v28.py --actual', 'code': [g.ref(ROOT, ROOT / 'visual_memory/vpd_registered_type_composite.py'), g.EDIT_ADAPTER_V28, g.ref(ROOT, Path(__file__))], 'base_kernel_unchanged': e.BASE_KERNEL, 'old25_adapter_unchanged': g.EDIT_ADAPTER_V25, 'old26_adapter_unchanged': g.EDIT_ADAPTER_V26, 'old27_adapter_unchanged': g.EDIT_ADAPTER_V27, 'actual_binding_guard': g.ref(ROOT, ROOT / 'visual_memory/vpd_registered_type_figma_binding.py'), 'actual_manifest': e.SEALED_EDIT, 'actual_maker': e.SEALED_MAKER, 'actual_builder': e.SEALED_BUILDER, 'actual_headline': HEADLINE, 'actual_frozen_preview': PREVIEW, 'registration_control': rr, 'full_frame_check': compare_ref, 'baseline': BASELINE, 'dependencies': dict(g.VERSIONS, fonttools=b.fontTools.__version__, pathops='0.9.2', vtracer='0.6.15'), 'limitations': ['Source-over control only; actual V28 Figma binding awaits new real host calls/capture/official exports.', 'Maker code is provenance only. Original version28 retained; only a deep copy maps to24 for the fixed finite editor.', 'Existing V24 generated source/production trace reused; verification retraces only in memory.', 'All 162052 core pixels checked; mutation controls select real headline noncore, uncovered core and covered core when present.', 'Old22-27 complete returns and every RGB/RGBA/alpha fingerprint equal the sealed prior baseline. Four operand ULP and zero RGB/alpha tolerance unchanged.', 'Only own private countercases/new audit written; photograph/assets/Root guard/business untouched. No aesthetic PASS.']}
    raw = jb(report)
    g.require(len(raw) <= 6144, 'BOUNDED_EVIDENCE_EXCEEDED')
    with AUDIT.open('xb') as stream:
        stream.write(raw)
    print(json.dumps({'result': 'PASS', 'cases': len(checks), 'seconds': report['seconds'], 'audit': g.ref(ROOT, AUDIT), 'adapter': g.EDIT_ADAPTER_V28, 'composite': report['code'][0], 'core_covered': checked['core_alpha_positive_pixels']}))
if __name__ == '__main__':
    main()
