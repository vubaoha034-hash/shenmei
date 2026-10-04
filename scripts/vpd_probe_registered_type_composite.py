"""Private real-asset controls, not a Figma or aesthetic approval.

Only --write-evidence publishes a compact actual run at the one allowed audit
path. Reproducible PNG/SVG controls stay in the fixed private probe directory.
"""
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
from PIL import Image, ImageChops
from visual_memory import vpd_registered_type_composite as g
from visual_memory.vpd_correct_source_worker import compare_pixels as old_compare

PRIVATE = ROOT / '.liu-visual-private/composite-guard-probe'
EVIDENCE = ROOT / 'evidence/vpd/codex_takeover_20261003/audit/REGISTERED_TYPE_COMPOSITE_TESTS.json'


def save(name, raw):
    path = PRIVATE / name
    if path.exists():
        g.require(path.read_bytes() == raw, 'PROBE_CONFLICT:' + name)
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as stream:
            stream.write(raw)
    return g.ref(ROOT, path)


def json_raw(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def png(image):
    stream = io.BytesIO()
    image.save(stream, format='PNG')
    return stream.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-evidence', action='store_true')
    args = parser.parse_args()
    start = time.monotonic()
    immutable = [g.SOURCE, g.BRAND, g.CORE, g.HELPER]
    original = [(r, g.sha(g.checked_bytes(ROOT, r)), (ROOT / r['path']).stat().st_mtime_ns) for r in immutable]
    tests = []

    def reject(name, operation, expected_error):
        try:
            operation()
        except (ValueError, KeyError, FileNotFoundError) as error:
            actual = str(error)
            g.require(expected_error in actual, 'WRONG_REJECTION:' + name + ':' + actual)
            tests.append({'test': name, 'result': 'REJECTED', 'actual': actual})
            return
        raise AssertionError('NEGATIVE_ACCEPTED:' + name)

    # Real V21 font commands and geometry; remove clip only in private control.
    v21 = ROOT / (g.SERIES + 'v21')
    manifest = json.loads((v21 / 'MANIFEST.json').read_text(encoding='utf-8'))
    tree = ET.fromstring((v21 / 'headline.svg').read_bytes())
    tree.remove(tree.find(g.NS + 'defs'))
    tree.find(g.NS + 'g').attrib.pop('clip-path')
    font_lineage = {'kind': 'source-han-serif-2.003', 'font': manifest['source_inputs']['font'],
                    'provenance': g.ref(ROOT, v21 / 'MANIFEST.json')}
    headline = save('font-control-default-namespace.svg', ET.tostring(tree))
    registration = g.register(ROOT, 22, headline, font_lineage)
    registration_ref = save('font-registration.json', json_raw(registration))
    image, overlay, _ = g.replay(ROOT, registration_ref)
    final_ref = save('font-composite.png', png(image))
    actual_v21_raw = g.ref(ROOT, ROOT / '.liu-visual-private/correct_source_typography/v21/figma-raw-export.png')
    control = g.compare_pixels(ROOT, registration_ref, final_ref, actual_v21_raw)
    tests.append({'test': 'real_S_and_V21_font_source_over', 'result': 'PASS',
                  'core_covered_pixels': control['core_alpha_positive_pixels'],
                  'full_frame_difference': control['whole_frame_expected'],
                  'actual_V21_Figma_raw_to_control': control['figma_raw_to_final'],
                  'actual_V21_Figma_raw_bytes_equal_control': control['figma_raw_bytes_equal_final'],
                  'actual_V21_Figma_raw_color_metadata': control['figma_raw_color_metadata']})

    # Foreground positive control uses every actual V17 nonempty trace contour.
    v17 = ROOT / (g.SERIES + 'v17')
    trace = ET.fromstring((v17 / 'upstream-alpha128-trace.svg').read_bytes())
    actual_paths = [n for n in trace if n.get('d', '').strip()]
    canvas = ET.Element(g.NS + 'svg', {'width': '1536', 'height': '1024', 'viewBox': '0 0 1536 1024', 'fill': 'none'})
    ET.SubElement(canvas, g.NS + 'title').text = g.COPY
    group = ET.SubElement(canvas, g.NS + 'g', {'transform': 'matrix(0.4 0 0 0.4 250 450)'})
    for node in actual_paths:
        node = copy.deepcopy(node)
        node.set('fill', '#F5F2E6')
        group.append(node)
    trace_headline = save('trace-foreground-control.svg', ET.tostring(canvas))
    trace_lineage = {'kind': 'alpha128-vtracer',
        'generated_png': g.ref(ROOT, ROOT / '.liu-visual-private/correct_source_typography/v17/headline-generated-01.png'),
        'trace_svg': g.ref(ROOT, v17 / 'upstream-alpha128-trace.svg'),
        'generation_evidence': g.ref(ROOT, v17 / 'IMAGEGEN_EXECUTION.json'),
        'provenance': g.ref(ROOT, v17 / 'LETTERING_PROVENANCE.json')}
    trace_registration = g.register(ROOT, 22, trace_headline, trace_lineage)
    trace_reg_ref = save('trace-registration.json', json_raw(trace_registration))
    foreground, trace_overlay, _ = g.replay(ROOT, trace_reg_ref)
    foreground_ref = save('trace-foreground-composite.png', png(foreground))
    foreground_check = g.compare_pixels(ROOT, trace_reg_ref, foreground_ref)
    g.require(foreground_check['core_alpha_positive_pixels'] > 0, 'FOREGROUND_CONTROL_DID_NOT_COVER_CORE')
    tests.append({'test': 'real_S_V17_alpha128_retrace_foreground', 'result': 'PASS',
                  'retained_nonempty_paths': len(actual_paths),
                  'core_covered_pixels': foreground_check['core_alpha_positive_pixels'],
                  'full_frame_difference': foreground_check['whole_frame_expected']})

    corrupted_source = bytearray(g.checked_bytes(ROOT, g.SOURCE))
    corrupted_source[-1] ^= 1
    bad_source_ref = save('source-bytes-countercase.png', bytes(corrupted_source))
    reject('changed_source_byte', lambda: g.checked_bytes(ROOT, {**bad_source_ref, 'sha256': g.SOURCE['sha256']}),
           'REFERENCE_SHA_MISMATCH')
    core = g.core_mask(ROOT)
    alpha = trace_overlay.getchannel('A')
    positions = [(x, y) for y, intervals in json.loads(g.checked_bytes(ROOT, g.CORE))['rows']
                 for x0, x1 in intervals for x in range(x0, x1)]
    for label, condition in [('covered', lambda value: value > 0), ('uncovered', lambda value: value == 0)]:
        x, y = next((x, y) for x, y in positions if condition(alpha.getpixel((x, y))))
        bad = foreground.copy()
        value = list(bad.getpixel((x, y)))
        value[0] = value[0] + 1 if value[0] < 255 else value[0] - 1
        bad.putpixel((x, y), tuple(value))
        bad_ref = save('core-' + label + '-one-channel.png', png(bad))
        reject('core_' + label + '_one_channel_change',
               lambda: g.compare_pixels(ROOT, trace_reg_ref, bad_ref), 'UNEXPLAINED_COMPOSITE_PIXEL_CHANGE')
    missing_alpha = copy.deepcopy(registration)
    del missing_alpha['layers'][1]['alpha_sha256']
    missing_alpha_ref = save('missing-alpha-registration.json', json_raw(missing_alpha))
    reject('unregistered_alpha', lambda: g.replay(ROOT, missing_alpha_ref), 'REGISTERED_LAYER_REPLAY_MISMATCH')
    wrong_order = copy.deepcopy(registration)
    wrong_order['layer_order'].reverse()
    wrong_order_ref = save('wrong-layer-order.json', json_raw(wrong_order))
    reject('changed_registered_layer_order', lambda: g.replay(ROOT, wrong_order_ref), 'REGISTERED_LAYER_REPLAY_MISMATCH')
    shifted = copy.deepcopy(tree)
    shifted.find(g.NS + 'g').set('transform', 'translate(1 0)')
    shifted_ref = save('shifted-font-control.svg', ET.tostring(shifted))
    shifted_registration = copy.deepcopy(registration)
    shifted_registration['layers'][1]['svg'] = shifted_ref
    shifted_reg_ref = save('shifted-registration.json', json_raw(shifted_registration))
    reject('changed_registered_geometry', lambda: g.replay(ROOT, shifted_reg_ref), 'REGISTERED_LAYER_REPLAY_MISMATCH')
    for label, element in [('image', '<image href="data:image/png;base64,eA=="/>'),
                           ('filter', '<filter id="retouch"/>'),
                           ('external_URL', '<path d="M0 0L1 1Z" fill="url(https://example.invalid/x)"/>'),
                           ('shape_patch', '<rect width="1536" height="1024" fill="#F5F2E6"/>')]:
        raw = ('<svg xmlns="http://www.w3.org/2000/svg" width="1536" height="1024">' + element + '</svg>').encode()
        reject('forbidden_' + label, lambda: g.svg_tree(raw), 'FORBIDDEN')
    block = copy.deepcopy(canvas)
    block.find(g.NS + 'g')[0].set('d', 'M0 0H1536V1024H0Z')
    block_ref = save('path-block-countercase.svg', ET.tostring(block))
    reject('large_path_patch_disguised_as_glyph',
           lambda: g.register(ROOT, 22, block_ref, trace_lineage), 'TRACE_GLYPH_COMMANDS_CHANGED')
    wrong_generated = copy.deepcopy(trace_lineage)
    wrong_generated['generated_png'] = final_ref
    reject('photograph_as_generated_alpha', lambda: g.register(ROOT, 22, trace_headline, wrong_generated),
           'GENERATED_ALPHA_PNG_REQUIRED')
    opaque_rgba = save('opaque-RGBA-photograph.png', png(Image.open(io.BytesIO(g.checked_bytes(ROOT, g.SOURCE))).convert('RGBA')))
    opaque_lineage = {**trace_lineage, 'generated_png': opaque_rgba}
    reject('opaque_RGBA_photograph_as_lettering', lambda: g.register(ROOT, 22, trace_headline, opaque_lineage),
           'TRANSPARENT_LETTERING_ALPHA_REQUIRED')
    changed_alpha = Image.open(io.BytesIO(g.checked_bytes(ROOT, trace_lineage['generated_png']))).copy()
    changed_alpha.putalpha(ImageChops.offset(changed_alpha.getchannel('A'), 1, 0))
    changed_alpha_ref = save('shifted-generated-alpha.png', png(changed_alpha))
    changed_alpha_lineage = {**trace_lineage, 'generated_png': changed_alpha_ref}
    reject('original_alpha_shifted_without_trace_change',
           lambda: g.register(ROOT, 22, trace_headline, changed_alpha_lineage), 'GENERATED_ALPHA_TRACE_MISMATCH')
    technical = json.loads((v21 / 'TECHNICAL_CHECK.json').read_text(encoding='utf-8'))
    old_compare(ROOT, technical, technical['overlay_envelopes'])
    tests.append({'test': 'frozen_V21_actual_old_guard_regression', 'result': 'PASS',
                  'final_sha256': technical['export']['sha256'], 'core_pixels': 162052})
    for reference, digest, modified in original:
        path = ROOT / reference['path']
        g.require(g.sha(path.read_bytes()) == digest and path.stat().st_mtime_ns == modified,
                  'FROZEN_FILE_MODIFIED:' + reference['path'])
    report = {'schema': 'vpd-registered-type-composite-actual-tests/v1',
        'verdict': 'PASS_OFFLINE_CONTROLS_ONLY_ROOT_INTEGRATION_AND_FIGMA_REVIEW_PENDING',
        'command': '"' + sys.executable + '" -B scripts/vpd_probe_registered_type_composite.py'
                   + (' --write-evidence' if args.write_evidence else ''),
        'exit_code': 0, 'runtime': g.VERSIONS, 'vtracer': '0.6.15; actual original alpha128 replay',
        'renderer_helper': g.HELPER, 'guard_sha256': g.ref(ROOT, ROOT / 'visual_memory/vpd_registered_type_composite.py')['sha256'],
        'probe_sha256': g.ref(ROOT, Path(__file__))['sha256'], 'source': g.SOURCE, 'fixed_core': g.CORE,
        'tests': tests, 'private_control_refs': [registration_ref, final_ref, trace_reg_ref, foreground_ref],
        'elapsed_seconds': round(time.monotonic() - start, 3),
        'initial_actual_failures': [
            {'exit_code': 1, 'cause': 'Sharp rejected ns0:svg; use default SVG namespace; failed font-control.svg retained privately.'},
            {'exit_code': 1, 'cause': 'Raw Figma has sRGB metadata; record raw metadata separately; final source-profile equality stays enforced.'},
            {'exit_code': 1, 'cause': 'Actual tool alpha max254; require min0/max>=128 for alpha128 rather than invented max255.'}],
        'frozen_S_brand_core_helper_sha_and_mtime_unchanged': True,
        'business_state_writes': 0, 'existing_guard_writes': 0, 'new_photography_or_design_outputs': 0,
        'paid_compute_usd': 0, 'actual_Figma_binding_collected': False, 'aesthetic_pass_claimed': False,
        'limitations': ['Registration trust is Root frozen references; semantic generated-copy identity needs real image/tool review.',
            'No authenticity proof for maker Figma/transcript declarations; real read-only node/style/path capture plus independent review is still required.',
            'Prospective module only; not integrated into existing production state validator by this worker.',
            'Existing cached machine/runtime paths are pinned; cross-machine dependency discovery is not implemented.',
            'Private controls remove old clips for legitimate foreground text; historical originals remain frozen.']}
    raw = (json.dumps(report, ensure_ascii=False, indent=1) + '\n').encode('utf-8')
    g.require(len(raw) <= 6144, 'PUBLIC_TEST_EVIDENCE_OVER_6KB')
    if args.write_evidence:
        if EVIDENCE.exists():
            prior = EVIDENCE.read_bytes()
            g.require(json.loads(prior)['schema'] == report['schema'], 'UNRELATED_AUDIT_FILE_CONFLICT')
            save('prior-public-offline-tests-' + g.sha(prior)[:12] + '.json', prior)
        EVIDENCE.write_bytes(raw)
    print(json.dumps({'tests': len(tests), 'all_pass': True, 'exit_code': 0,
                      'evidence_bytes': len(raw), 'private_folder': str(PRIVATE), 'report': report}, ensure_ascii=False))


if __name__ == '__main__':
    main()
