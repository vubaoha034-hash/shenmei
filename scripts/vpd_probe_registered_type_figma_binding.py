"""Bounded actual V22 proof and negative controls; never writes work or source."""
from pathlib import Path
import argparse
import copy
from datetime import datetime, timezone
import json
import re
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from visual_memory import vpd_registered_type_composite as g
from visual_memory import vpd_registered_type_figma_binding as b


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write-evidence', action='store_true')
    args = parser.parse_args()
    started = time.monotonic()
    private = ROOT / '.liu-visual-private/composite-guard-probe/figma-binding'
    private.mkdir(parents=True, exist_ok=True)
    earlier = private / 'complete-probe-report.json'
    if earlier.exists() and json.loads(earlier.read_bytes()).get('result') == 'FAIL':
        retained = private / ('failed-probe-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S') + '.json')
        retained.write_bytes(earlier.read_bytes())
    folder = ROOT / g.SERIES / 'v22'
    registration_ref = g.ref(ROOT, folder / 'REGISTERED_TYPE_COMPOSITE.json')
    runtime_ref = g.ref(ROOT, folder / 'FIGMA_BINDING_RUNTIME_EVIDENCE.json')
    download_ref = g.ref(ROOT, ROOT / '.liu-visual-private/correct_source_typography/v22/figma-download-readback.json')
    registration = b.json_file(ROOT, registration_ref)
    evidence = b.json_file(ROOT, runtime_ref)
    readback = b.json_file(ROOT, download_ref)
    capture = b.json_file(ROOT, evidence['actual_capture'])
    checks = []

    def save(name, value):
        path = private / (name + '.json')
        path.write_text(json.dumps(value, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
        return g.ref(ROOT, path)

    def reject(name, operation, expected):
        try:
            operation()
        except (ValueError, KeyError, FileNotFoundError) as error:
            message = str(error)
            ok = expected in message
            checks.append({'case': name, 'pass': ok, 'rejected': message})
        else:
            checks.append({'case': name, 'pass': False, 'rejected': None})

    def run(runtime=runtime_ref, download=download_ref):
        return b.verify_actual_binding(ROOT, registration_ref, runtime, download)

    actual = run()
    save('actual-positive-recomputed', actual)
    checks.append({'case': 'real-host-capture-source-png-2svg', 'pass': actual['node_count'] == 31 and actual['vector_count'] == 24})
    # This is explicitly a failed countercase, never real Figma evidence.
    forgery = {'result': 'PASS_WHOLE_FRAME_PIXEL_EXACT_WITH_NATIVE_RENDERER_LIMITATIONS', 'formal_version': 22,
               'whole_frame_check_ref': g.ref(ROOT, folder / 'REGISTERED_TYPE_COMPOSITE_CHECK.json'),
               'actual_figma_registered_vectors_verified': True, 'actual_original_photo_verified': True,
               'raw_figma_export': g.SOURCE, 'countercase_only': True}
    reject('historical-five-boolean-forgery', lambda: run(runtime=save('failed-five-boolean-forgery', forgery)),
           'ACTUAL_RUNTIME_EVIDENCE_REQUIRED')

    for name, field, value, expected in [
        ('missing-real-host-runtime', 'root_rollout_host_path', str(private / 'missing.jsonl'), 'ACTUAL_HOST_RUNTIME_REQUIRED'),
        ('spoof-binding-output-digest', 'binding_output_sha256', '0' * 64, 'ACTUAL_BINDING_OUTPUT_CONFLICT'),
        ('native-png-replaced-by-source', 'actual_native_export_ref', g.SOURCE, 'ACTUAL_ORIGINAL_IMAGE_OR_FRAME_EXPORT_CHANGED')]:
        mutant = copy.deepcopy(evidence)
        mutant[field] = value
        mutant_ref = save('failed-' + name, mutant)
        reject(name, lambda mr=mutant_ref: run(runtime=mr), expected)

    mutant_capture = copy.deepcopy(capture)
    mutant_capture['nodes'][0]['name'] += ' invented'
    mutant = copy.deepcopy(evidence)
    mutant['actual_capture'] = save('failed-capture-body', mutant_capture)
    reject('rehash-self-reported-capture', lambda: run(runtime=save('failed-capture-report', mutant)),
           'ACTUAL_CAPTURE_BODY_FINGERPRINT_CONFLICT')
    actual_result = b.json_file(ROOT, evidence['actual_result'])
    actual_result['ancestors'].insert(0, {'id': '999:1', 'type': 'FRAME', 'effects': []})
    mutant = copy.deepcopy(evidence)
    mutant['actual_result'] = save('failed-ancestor-result', actual_result)
    reject('self-reported-extra-ancestor', lambda: run(runtime=save('failed-ancestor-report', mutant)),
           'SELF_REPORTED_BINDING_NOT_ACTUAL_TOOL_RESULT')
    excerpt = b.json_file(ROOT, evidence['private_exact_runtime_excerpt'])
    excerpt[-1]['timestamp'] = '2000-01-01T00:00:00Z'
    mutant = copy.deepcopy(evidence)
    mutant['private_exact_runtime_excerpt'] = save('failed-runtime-excerpt', excerpt)
    reject('forged-tool-runtime-excerpt', lambda: run(runtime=save('failed-excerpt-report', mutant)),
           'EXCERPT_DOES_NOT_MATCH_REAL_HOST_RUNTIME')
    bad_download = copy.deepcopy(readback)
    bad_download['actual_downloads'] = bad_download['actual_downloads'][1:]
    reject('missing-official-native-png', lambda: run(download=save('failed-missing-export', bad_download)),
           'SUCCESSFUL_OFFICIAL_DOWNLOADS_REQUIRED')
    bad_download = copy.deepcopy(readback)
    bad_download['actual_downloads'][0] = copy.deepcopy(bad_download['actual_downloads'][1])
    reject('duplicate-source-as-native-png', lambda: run(download=save('failed-duplicate-png', bad_download)),
           'UNBOUND_OFFICIAL_PNG')

    def native_case(name, mutate, expected):
        value = copy.deepcopy(capture)
        nodes = {n['id']: n for n in value['nodes']}
        mutate(value, nodes)
        save('failed-native-' + name, value)
        reject(name, lambda: b.native_capture(ROOT, value, registration), expected)

    native_case('wrong-imagehash', lambda c, n: n['366:3']['fills'][0].update(imageHash='0' * 40), 'ORIGINAL_PHOTOGRAPHIC_FILL_CHANGED')
    native_case('nonzero-photo-filter', lambda c, n: n['366:3']['fills'][0]['filters'].update(contrast=0.001), 'ORIGINAL_PHOTOGRAPHIC_FILL_CHANGED')
    native_case('photo-fill-alpha', lambda c, n: n['366:3']['fills'][0].update(opacity=0.999), 'ORIGINAL_PHOTOGRAPHIC_FILL_CHANGED')
    native_case('hidden-photo-copy-in-fill', lambda c, n: n['366:33']['fills'].append(dict(n['366:3']['fills'][0], visible=False)), 'HIDDEN_OR_DUPLICATE_PHOTOGRAPHIC_FILL')
    native_case('unregistered-hidden-node', lambda c, n: n['366:4'].update(visible=False), 'FIGMA_EFFECT_STYLE_VISIBILITY_OR_MASK_CHANGED')
    native_case('group-blend-change', lambda c, n: n['366:34'].update(blendMode='NORMAL'), 'FIGMA_EFFECT_STYLE_VISIBILITY_OR_MASK_CHANGED')
    native_case('inactive-effect-also-rejected', lambda c, n: n['366:34']['effects'].append({'type': 'DROP_SHADOW', 'visible': False}), 'FIGMA_EFFECT_STYLE_VISIBILITY_OR_MASK_CHANGED')
    native_case('group-clipping-change', lambda c, n: n['366:34'].update(clipsContent=True), 'FIGMA_CLIPPING_CHANGED')
    native_case('brand-width-change', lambda c, n: n['366:5'].update(width=204), 'FROZEN_BRAND_PLACEMENT_CHANGED')
    native_case('glyph-fill-one-RGB-unit', lambda c, n: n['366:35']['fills'][0]['color'].update(r=b.f32(244 / 255)), 'REGISTERED_VECTOR_COLOR_OR_ALPHA_CHANGED')
    native_case('glyph-fill-alpha', lambda c, n: n['366:35']['fills'][0].update(opacity=0.999), 'REGISTERED_VECTOR_COLOR_OR_ALPHA_CHANGED')
    native_case('glyph-winding-change', lambda c, n: n['366:35']['vectorPaths'][0].update(windingRule='EVENODD'), 'REGISTERED_GLYPH_ORDER_OR_WINDING_CHANGED')
    native_case('absolute-position-change', lambda c, n: n['366:35']['absoluteTransform'][0].__setitem__(2, n['366:35']['absoluteTransform'][0][2] + 1), 'FIGMA_ABSOLUTE_RELATIVE_TRANSFORM_CONFLICT')

    def shift_anchor(c, n):
        q, p = n['366:35'], n['366:34']
        q['x'] += 1
        q['relativeTransform'][0][2] += 1
        q['absoluteTransform'][0][2] = b.f32(p['absoluteTransform'][0][2] + q['x'] - p['x'])
    native_case('coherent-glyph-shift-1px', shift_anchor, 'FIGMA_GLYPH_ANCHOR_CHANGED')

    def change_control(c, n):
        q = n['366:35']['vectorPaths'][0]
        q['data'] = re.sub(r'(C\s*)([-+0-9.eE]+)', lambda m: m[1] + str(float(m[2]) + 1), q['data'], count=1)
    native_case('glyph-control-shift-1px', change_control, 'FIGMA_GLYPH_CONTROL_COORDINATE_CHANGED')

    def reverse_order(c, n):
        n['366:4']['children'].reverse()
        ordered = []
        def walk(i):
            ordered.append(n[i])
            for child in n[i]['children']:
                walk(child)
        walk('366:2')
        c['nodes'] = ordered
    native_case('brand-headline-layer-order', reverse_order, 'REGISTERED_LAYER_ORDER_CHANGED')

    sealed_first = ROOT / 'evidence/vpd/codex_takeover_20261003/audit/REGISTERED_TYPE_COMPOSITE_TESTS.json'
    checks.append({'case': 'first-17-controls-evidence-unchanged',
                   'pass': g.sha(sealed_first.read_bytes()) == '73bebe1b2f63920605873d1d20942803d7a0063b08544bb1a919e320b40a1612'})
    elapsed = round(time.monotonic() - started, 3)
    passed = all(x['pass'] for x in checks)
    report = {
        'schema': 'vpd-registered-type-figma-binding-tests/v1', 'result': 'PASS' if passed else 'FAIL',
        'formal_version': 22, 'checked_utc': datetime.now(timezone.utc).isoformat(),
        'actual_command': str(g.RUNTIME / 'python/python.exe') + ' scripts/vpd_probe_registered_type_figma_binding.py --write-evidence',
        'exit_code': 0 if passed else 1, 'elapsed_seconds': elapsed, 'cases': len(checks), 'checks': checks,
        'code': g.ref(ROOT, ROOT / 'visual_memory/vpd_registered_type_figma_binding.py'),
        'probe': g.ref(ROOT, Path(__file__)), 'registration': registration_ref, 'runtime': runtime_ref,
        'positive_geometry': actual['geometry'], 'actual_source_sha256': g.SOURCE['sha256'],
        'actual_native_png_sha256': actual['raw_figma_export']['sha256'],
        'dependencies': dict(g.VERSIONS, fonttools=font_version()),
        'initial_actual_failures': ['exit1: absolute sum ignored GROUP intermediate float32 (two attempts)',
                                  'exit1: shape subtraction used ulp(delta) instead of ulp(operands)',
                                  'exit1: first 27-case probe had 2 download controls blocked by inferred tool-result path; retained privately'],
        'precision': 'Immediate-parent absolute float32 sum must match exactly. Glyph topology/order exact; coordinate shape uses four float32 ULPs of operands. Frozen brand anchor adds half page-coordinate ULP. Official SVG uses 3 decimal digits: anchor .0005; centered shape .001 plus ULPs. RGB/alpha zero tolerance.',
        'limitations': ['Only the inspected actual V22 host invocation is accepted; no new Figma API call was made by this probe.',
                        'Full-entry forgery tests check provenance; native-* files isolate node/style/geometry validation and are failed fixtures.',
                        'Native fd15 PNG differs from registered final; this validates authenticity, not equality or aesthetics.',
                        'Local session log and frozen event hashes are the trust boundary; this is not operating-system attestation.',
                        'No writes to source/design/Root guard/business state; original challenge FAIL and first 17-test audit remain sealed.']}
    save('complete-probe-report', report)
    if args.write_evidence:
        public = ROOT / 'evidence/vpd/codex_takeover_20261003/audit/REGISTERED_TYPE_FIGMA_BINDING_TESTS.json'
        encoded = (json.dumps(report, ensure_ascii=False, separators=(',', ':')) + '\n').encode('utf-8')
        g.require(len(encoded) <= 6144, 'BOUNDED_PUBLIC_EVIDENCE_EXCEEDED')
        public.write_bytes(encoded)
    print(json.dumps({'result': report['result'], 'cases': len(checks), 'elapsed_seconds': elapsed,
                      'failures': [x for x in checks if not x['pass']]}, ensure_ascii=True))
    return report['exit_code']


def font_version():
    return b.fontTools.__version__


if __name__ == '__main__':
    raise SystemExit(main())
