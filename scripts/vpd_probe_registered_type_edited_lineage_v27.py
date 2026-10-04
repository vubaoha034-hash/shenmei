"""Actual frozen V27 adapter controls; countercases use private copies only."""
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
from visual_memory import vpd_registered_type_edited_lineage_v27 as e

PRIVATE = ROOT / '.liu-visual-private/composite-guard-probe/edited-lineage-v27'
AUDIT = ROOT / 'evidence/vpd/codex_takeover_20261003/audit/REGISTERED_TYPE_EDITED_LINEAGE_V27_TESTS.json'
BASELINE = {'path': '.liu-visual-private/guard-v27-proposal/OLD_22_23_24_25_26_BASELINE.json',
            'sha256': 'e5833b94d5100847299696d1f6a0fb582d641e5cb87b55a7782508aa6b1417a5'}
HEADLINE = {'path': e.BASE + 'headline.svg',
            'sha256': 'b8c0a6a0dbd31225c164535789eeee66042ee7bc8ccfa003df18083fd64b28a4'}
PREVIEW = {'path': '.liu-visual-private/correct_source_typography/v27/preview.png',
           'sha256': '4c7448ef8d7a2fa6aff5194190f607bda77b6c93551ecd9f5d84d47b5bb06e52'}


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
    return next((x, y) for y in range(box[1], box[3]) for x in range(box[0], box[2]) if mask.getpixel((x, y)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--actual', action='store_true', required=True)
    parser.parse_args()
    started = time.monotonic()
    checks = []
    baseline = json.loads(g.checked_bytes(ROOT, BASELINE))
    for version in (22, 23, 24, 25, 26):
        prior = baseline['versions'][str(version)]
        rr, binding = prior['registration_ref'], prior['actual_binding']
        image, overlay, reg = g.replay(ROOT, rr)
        observed = {'registration_ref': rr, 'registration': reg,
            'expected_RGB': {'mode': image.mode, 'size': list(image.size), 'bytes': len(image.tobytes()),
                             'sha256': g.sha(image.tobytes())},
            'overlay_RGBA': {'mode': overlay.mode, 'size': list(overlay.size), 'bytes': len(overlay.tobytes()),
                             'sha256': g.sha(overlay.tobytes()), 'alpha_sha256': g.sha(overlay.getchannel('A').tobytes())},
            'compare_pixels': g.compare_pixels(ROOT, rr, prior['compare_pixels']['final'], binding['raw_figma_export']),
            'actual_binding': b.verify_actual_binding(ROOT, rr, binding['runtime_evidence'], binding['download_readback']),
            'frozen_binding_check_ref': g.ref(ROOT, ROOT / prior['frozen_binding_check_ref']['path'])}
        g.require(observed == prior, 'OLD_COMPLETE_RETURN_CHANGED:' + str(version))
        checks.append({'case': f'old{version}_complete_registration_RGB_RGBA_compare_binding', 'result': 'PASS'})
        print(json.dumps({'old_version': version, 'complete_equal': True}), flush=True)
    g.require(g.edited_lineage(ROOT) == baseline['factories']['24'] and
              all(g.edited_lineage(ROOT, v) == baseline['factories'][str(v)] for v in (24, 25, 26)),
              'OLD_FACTORY_RETURN_CHANGED')
    checks.append({'case': 'default24_and_existing24_25_26_factories_unchanged', 'result': 'PASS'})
    lineage = g.edited_lineage(ROOT, 27)
    rr = save('actual-registration.json', jb(g.register(ROOT, 27, HEADLINE, lineage)))
    image, overlay, reg = g.replay(ROOT, rr)
    checked = g.compare_pixels(ROOT, rr, PREVIEW)
    compare_ref = save('actual-preview-composite-check.json', jb(checked))
    core = g.core_mask(ROOT)
    alpha_positive = overlay.getchannel('A').point(lambda v: 255 if v else 0)
    alpha_zero = ImageChops.invert(alpha_positive)
    headline_alpha = g.renderer(ROOT)(g.checked_bytes(ROOT, HEADLINE)).getchannel('A').point(lambda v: 255 if v else 0)
    checks.append({'case': 'actual27_sealed_profile_independent_replay_and_frozen_maker_preview', 'result': 'PASS',
                   'whole_frame': checked['whole_frame_expected'], 'core_covered': checked['core_alpha_positive_pixels'],
                   'core_uncovered': checked['core_alpha_zero_pixels']})

    def reject(name, operation, expected):
        try:
            operation()
        except ValueError as error:
            g.require(expected in str(error), 'WRONG_NEGATIVE:' + name + ':' + str(error))
            checks.append({'case': name, 'result': 'REJECTED', 'actual': str(error)})
            return
        raise AssertionError('NEGATIVE_ACCEPTED:' + name)

    manifest = json.loads(g.checked_bytes(ROOT, e.SEALED_EDIT))
    bad = copy.deepcopy(manifest); bad['glyphs'][0]['edits'][0]['before_sha256'] = '0' * 64
    save('wrong-source-before-contour.json', jb(bad))
    reject('actual_source_before_wrong', lambda: e.replay_edit_program(ROOT, bad), 'EDIT_BEFORE_CONTOUR_MISMATCH')
    tree = g.svg_tree(g.checked_bytes(ROOT, HEADLINE))
    path = list(tree.iter(g.NS + 'path'))[-1]
    d = path.get('d')
    last_c = list(re.finditer(r'C([^MLCZ]*)', d))[-1]
    numbers = list(re.finditer(r'[-+]?(?:\d*\.\d+|\d+\.?\d*)(?:[eE][-+]?\d+)?', last_c[1]))
    g.require(len(numbers) == 6, 'ACTUAL_LAST_CUBIC_REQUIRED')
    first_control_x = numbers[0]
    start, stop = last_c.start(1) + first_control_x.start(), last_c.start(1) + first_control_x.end()
    path.set('d', d[:start] + str(float(first_control_x[0]) + 1) + d[stop:])
    bad_svg = save('last-C-control-one-unit-wrong.svg', ET.tostring(tree))
    reject('actual_last_C_control_one_unit', lambda: g.register(ROOT, 27, bad_svg, lineage), 'EDIT_FINAL_SVG_REPLAY_MISMATCH')
    rgb_cases = [('actual27_headline_alpha_positive_noncore_one_RGB_unit', ImageChops.darker(headline_alpha, ImageChops.invert(core))),
                 ('actual27_uncovered_core_one_RGB_unit', ImageChops.darker(core, alpha_zero))]
    if checked['core_alpha_positive_pixels']:
        rgb_cases.append(('actual27_covered_core_one_RGB_unit', ImageChops.darker(core, alpha_positive)))
    for name, mask in rgb_cases:
        point = first_point(mask)
        bad_image = image.copy(); pixel = list(bad_image.getpixel(point)); pixel[0] ^= 1
        bad_image.putpixel(point, tuple(pixel))
        buffer = io.BytesIO(); bad_image.save(buffer, format='PNG')
        wrong_ref = save(name + '.png', buffer.getvalue())
        reject(name, lambda f=wrong_ref: g.compare_pixels(ROOT, rr, f), 'UNEXPLAINED_COMPOSITE_PIXEL_CHANGE')
        checks[-1]['point'] = list(point)
    reject('future28_registration', lambda: g.register(ROOT, 28, HEADLINE, lineage), 'EDIT_LINEAGE_V24_ONLY')
    reject('future28_factory', lambda: g.edited_lineage(ROOT, 28), 'INSPECTED_EDIT_VERSION_REQUIRED')
    for key in ('vpd_registered_type_edited_lineage', 'vpd_registered_type_edited_lineage_v25',
                'vpd_registered_type_edited_lineage_v26', 'vpd_registered_type_figma_binding'):
        g.checked_bytes(ROOT, baseline['before_code'][key])
    report = {'schema': 'vpd-actual-v27-thin-edit-adapter-controls/v1', 'formal_version': 27, 'result': 'PASS',
        'exit_code': 0, 'seconds': round(time.monotonic() - started, 3), 'cases': len(checks), 'checks': checks,
        'actual_command': str(g.RUNTIME / 'python/python.exe') + ' -B -u scripts/vpd_probe_registered_type_edited_lineage_v27.py --actual',
        'code': [g.ref(ROOT, ROOT / 'visual_memory/vpd_registered_type_composite.py'), g.EDIT_ADAPTER_V27,
                 g.ref(ROOT, Path(__file__))], 'base_kernel_unchanged': e.BASE_KERNEL,
        'old25_adapter_unchanged': g.EDIT_ADAPTER_V25, 'old26_adapter_unchanged': g.EDIT_ADAPTER_V26,
        'old_binding_unchanged': g.ref(ROOT, ROOT / 'visual_memory/vpd_registered_type_figma_binding.py'),
        'actual_manifest': e.SEALED_EDIT, 'actual_maker': e.SEALED_MAKER, 'actual_builder': e.SEALED_BUILDER,
        'actual_headline': HEADLINE, 'actual_frozen_preview': PREVIEW, 'registration_control': rr,
        'full_frame_check': compare_ref, 'baseline': BASELINE,
        'dependencies': dict(g.VERSIONS, fonttools=b.fontTools.__version__, pathops='0.9.2', vtracer='0.6.15'),
        'limitations': ['Source-over control only; actual V27 Figma binding awaits new real host calls/capture/official exports.',
            'Maker code is provenance only. Original version27 retained; only a deep copy maps to24 for the fixed finite editor.',
            'Existing V24 generated source/production trace reused; verification retraces only in memory.',
            'All 162052 core pixels checked; mutation controls select real headline noncore, uncovered core and covered core when present.',
            'Old22-26 complete returns and every RGB/RGBA/alpha fingerprint equal the sealed prior baseline. Four operand ULP and zero RGB/alpha tolerance unchanged.',
            'Only own private countercases/new audit written; photograph/assets/Root guard/business untouched. No aesthetic PASS.']}
    raw = jb(report)
    g.require(len(raw) <= 6144, 'BOUNDED_EVIDENCE_EXCEEDED')
    with AUDIT.open('xb') as stream:
        stream.write(raw)
    print(json.dumps({'result': 'PASS', 'cases': len(checks), 'seconds': report['seconds'], 'audit': g.ref(ROOT, AUDIT),
                      'adapter': g.EDIT_ADAPTER_V27, 'composite': report['code'][0],
                      'core_covered': checked['core_alpha_positive_pixels']}))


if __name__ == '__main__':
    main()
