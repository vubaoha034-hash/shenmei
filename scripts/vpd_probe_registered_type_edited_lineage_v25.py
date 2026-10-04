"""Necessary actual V25 adapter controls only; writes private fixtures and one own audit."""
from pathlib import Path
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
from visual_memory import vpd_registered_type_edited_lineage_v25 as e

PRIVATE = ROOT / '.liu-visual-private/composite-guard-probe/edited-lineage-v25'
AUDIT = ROOT / 'evidence/vpd/codex_takeover_20261003/audit/REGISTERED_TYPE_EDITED_LINEAGE_V25_TESTS.json'


def jb(value):
    return (json.dumps(value, ensure_ascii=False, indent=1) + '\n').encode('utf-8')


def save(name, raw):
    path = PRIVATE / name
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        g.require(path.read_bytes() == raw, 'V25_PROBE_CONFLICT:' + name)
    else:
        with path.open('xb') as stream:
            stream.write(raw)
    return g.ref(ROOT, path)


def main():
    started = time.monotonic()
    checks = []
    baseline = json.loads((ROOT / '.liu-visual-private/guard-v25-proposal/OLD_22_23_24_BASELINE.json').read_bytes())
    for version in (22, 23, 24):
        folder = ROOT / g.SERIES / f'v{version}'
        rr = g.ref(ROOT, folder / 'REGISTERED_TYPE_COMPOSITE.json')
        image, overlay, reg = g.replay(ROOT, rr)
        observed = {'registration': reg, 'expected_RGB_sha256': g.sha(image.tobytes()),
            'overlay_RGBA_sha256': g.sha(overlay.tobytes()), 'compare': g.compare_pixels(ROOT, rr,
                g.ref(ROOT, ROOT / f'.liu-visual-private/correct_source_typography/v{version}/poster.png'),
                g.ref(ROOT, ROOT / f'.liu-visual-private/correct_source_typography/v{version}/figma-raw.png'))}
        g.require(observed == baseline[str(version)], 'OLD_COMPLETE_RETURN_CHANGED:' + str(version))
        checks.append({'case': f'old{version}_complete_registration_RGBA_compare_return', 'result': 'PASS'})
    folder = ROOT / g.SERIES / 'v25'
    headline = g.ref(ROOT, folder / 'headline.svg')
    lineage = g.edited_lineage(ROOT, 25)
    reg = g.register(ROOT, 25, headline, lineage)
    rr = save('actual-registration.json', jb(reg))
    image, overlay, unused = g.replay(ROOT, rr)
    buffer = io.BytesIO(); image.save(buffer, format='PNG')
    final = save('actual-control.png', buffer.getvalue())
    checked = g.compare_pixels(ROOT, rr, final)
    checks.append({'case': 'actual25_sealed_profile_and_full_replay', 'result': 'PASS',
        'whole_frame': checked['whole_frame_expected'], 'core_covered': checked['core_alpha_positive_pixels'],
        'core_uncovered': checked['core_alpha_zero_pixels']})

    def reject(name, operation, error_code):
        try:
            operation()
        except ValueError as error:
            g.require(error_code in str(error), 'WRONG_NEGATIVE:' + name + ':' + str(error))
            checks.append({'case': name, 'result': 'REJECTED', 'actual': str(error)})
            return
        raise AssertionError('NEGATIVE_ACCEPTED:' + name)

    manifest = json.loads(g.checked_bytes(ROOT, e.SEALED_EDIT))
    bad = copy.deepcopy(manifest); bad['glyphs'][0]['edits'][0]['before_sha256'] = '0' * 64
    reject('actual_source_contour_before_wrong', lambda: e.replay_edit_program(ROOT, bad), 'EDIT_BEFORE_CONTOUR_MISMATCH')
    tree = g.svg_tree(g.checked_bytes(ROOT, headline))
    d = tree[0].get('d')
    changed = re.sub(r'(C\s*)([-+0-9.eE]+)', lambda m: m[1] + str(float(m[2]) + 1), d, count=1)
    g.require(changed != d, 'ACTUAL_CUBIC_REQUIRED_FOR_CONTROL')
    tree[0].set('d', changed)
    bad_svg = save('one-authored-control-point-wrong.svg', ET.tostring(tree))
    reject('actual_final_curve_input_wrong', lambda: g.register(ROOT, 25, bad_svg, lineage), 'EDIT_FINAL_SVG_REPLAY_MISMATCH')
    core = g.core_mask(ROOT)
    covered = ImageChops.darker(core, overlay.getchannel('A').point(lambda v: 255 if v else 0))
    bbox = covered.getbbox(); g.require(bbox is not None, 'ACTUAL_COVERED_CORE_POINT_REQUIRED')
    point = next((x, y) for y in range(bbox[1], bbox[3]) for x in range(bbox[0], bbox[2]) if covered.getpixel((x, y)))
    bad_image = image.copy(); pixel = list(image.getpixel(point)); pixel[0] ^= 1; bad_image.putpixel(point, tuple(pixel))
    buffer = io.BytesIO(); bad_image.save(buffer, format='PNG')
    bad_png = save('one-covered-core-R-channel-wrong.png', buffer.getvalue())
    reject('actual_covered_core_one_RGB_unit', lambda: g.compare_pixels(ROOT, rr, bad_png), 'UNEXPLAINED_COMPOSITE_PIXEL_CHANGE')
    checks[-1]['point'] = list(point)
    reject('future26', lambda: g.register(ROOT, 26, headline, lineage), 'EDIT_LINEAGE_V24_ONLY')
    g.checked_bytes(ROOT, e.BASE_KERNEL)
    report = {'schema': 'vpd-actual-v25-thin-edit-adapter-controls/v1', 'formal_version': 25,
        'result': 'PASS', 'exit_code': 0, 'seconds': round(time.monotonic() - started, 3), 'checks': checks,
        'cases': len(checks), 'actual_command': str(g.RUNTIME / 'python/python.exe') + ' scripts/vpd_probe_registered_type_edited_lineage_v25.py',
        'code': [g.ref(ROOT, ROOT / 'visual_memory/vpd_registered_type_composite.py'), g.EDIT_ADAPTER_V25,
                 g.ref(ROOT, __file__)], 'base_kernel_unchanged': e.BASE_KERNEL,
        'actual_edit_manifest': e.SEALED_EDIT, 'actual_maker': e.SEALED_MAKER, 'actual_builder': e.SEALED_BUILDER,
        'baseline': g.ref(ROOT, ROOT / '.liu-visual-private/guard-v25-proposal/OLD_22_23_24_BASELINE.json'),
        'dependencies': dict(g.VERSIONS, pathops='0.9.2', vtracer='0.6.15'),
        'limitations': ['Control source-over only; real V25 Figma binding is unavailable until actual host calls/capture/exports are sealed.',
            'No recognition or aesthetic PASS; original V25 bytes retained and only an in-memory version mapped for the fixed old kernel.',
            'No new generation or production trace; old kernel independently retraces existing source for verification.',
            'Fixtures only in own private folder; source photograph/old evidence/Root guard/business untouched.']}
    raw = jb(report); g.require(len(raw) <= 6144, 'BOUNDED_EVIDENCE_EXCEEDED')
    with AUDIT.open('xb') as stream:
        stream.write(raw)
    print(json.dumps({'result': 'PASS', 'cases': len(checks), 'seconds': report['seconds'], 'audit': g.ref(ROOT, AUDIT)}))


if __name__ == '__main__':
    main()
