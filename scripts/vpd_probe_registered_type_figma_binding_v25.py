"""Bounded V25 actual binding controls; countercases stay in a private folder."""
from pathlib import Path
import argparse
import copy
from datetime import datetime, timezone
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from visual_memory import vpd_registered_type_composite as g
from visual_memory import vpd_registered_type_figma_binding as b

BASELINE_SHA = '953e1299e15b12fb89dc9216511dd439fc30afb1541fc6445d1fb3a450f4a53c'
BEFORE_CODE_SHA = '3b23fc512c46b88f58a3c2a562db0c927a0521ca69219c6eccdde1258fa32e0c'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write-evidence', action='store_true')
    args = parser.parse_args()
    started = time.monotonic()
    private = ROOT / '.liu-visual-private/composite-guard-probe/figma-binding-v25-prospective'
    private.mkdir(parents=True, exist_ok=True)
    earlier = private / 'complete-probe-report.json'
    if earlier.exists():
        retained = private / ('prior-probe-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f') + '.json')
        retained.write_bytes(earlier.read_bytes())
    folder = ROOT / g.SERIES / 'v25'
    registration_ref = g.ref(ROOT, folder / 'REGISTERED_TYPE_COMPOSITE.json')
    runtime_ref = g.ref(ROOT, folder / 'FIGMA_BINDING_RUNTIME_EVIDENCE.json')
    download_ref = g.ref(ROOT, ROOT / '.liu-visual-private/correct_source_typography/v25/figma-download-readback.json')
    evidence = b.json_file(ROOT, runtime_ref)
    registration = b.json_file(ROOT, registration_ref)
    capture = b.json_file(ROOT, evidence['actual_capture'])
    baseline_ref = {'path': (private / 'sealed-22-23-24-before-adaptation.json').relative_to(ROOT).as_posix(),
                    'sha256': BASELINE_SHA}
    baseline = b.json_file(ROOT, baseline_ref)
    checks = []

    def save(name, value):
        path = private / (name + '.json')
        path.write_bytes((json.dumps(value, ensure_ascii=False, separators=(',', ':')) + '\n').encode('utf-8'))
        return g.ref(ROOT, path)

    def reject(name, operation, expected):
        try:
            operation()
        except (ValueError, KeyError, FileNotFoundError) as error:
            checks.append({'case': name, 'pass': expected in str(error), 'rejected': str(error)})
        else:
            checks.append({'case': name, 'pass': False, 'rejected': None})

    def run(runtime=runtime_ref, download=download_ref):
        return b.verify_actual_binding(ROOT, registration_ref, runtime, download)

    actual = run()
    positive_ref = save('actual-positive-recomputed', actual)
    checks.append({'case': 'actual25_21nodes_14vectors_two_distinct_7path_SVGs',
                   'pass': actual['frame_id'] == '388:2' and actual['node_count'] == 21
                   and actual['vector_count'] == 14 and all(x['paths'] == 7 for x in actual['geometry'].values())})
    for version in (22, 23, 24):
        old = ROOT / g.SERIES / f'v{version}'
        returned = b.verify_actual_binding(ROOT, g.ref(ROOT, old / 'REGISTERED_TYPE_COMPOSITE.json'),
            g.ref(ROOT, old / 'FIGMA_BINDING_RUNTIME_EVIDENCE.json'),
            g.ref(ROOT, ROOT / f'.liu-visual-private/correct_source_typography/v{version}/figma-download-readback.json'))
        checks.append({'case': f'v{version}_complete_return_unchanged', 'pass': returned == baseline[str(version)]})

    old_ref = g.ref(ROOT, ROOT / g.SERIES / 'v24/FIGMA_BINDING_RUNTIME_EVIDENCE.json')
    old_evidence = b.json_file(ROOT, old_ref)
    reject('v24_runtime_reused25', lambda: run(runtime=old_ref), 'ACTUAL_RUNTIME_VERSION_CONFLICT')
    fake = copy.deepcopy(old_evidence); fake['formal_version'] = 25
    reject('v24_runtime_relabelled25', lambda: run(runtime=save('failed-v24-relabelled', fake)),
           'ACTUAL_V25_RUNTIME_EVIDENCE_REQUIRED')
    for name, field, error in [('v24_capture_reused25', 'actual_capture', 'ACTUAL_CAPTURE_BODY_FINGERPRINT_CONFLICT'),
                               ('v24_native_PNG_reused25', 'actual_native_export_ref', 'ACTUAL_ORIGINAL_IMAGE_OR_FRAME_EXPORT_CHANGED')]:
        fake = copy.deepcopy(evidence); fake[field] = old_evidence[field]
        reject(name, lambda ref=save('failed-' + name, fake): run(runtime=ref), error)

    excerpt = b.json_file(ROOT, evidence['private_exact_runtime_excerpt'])
    excerpt[2]['payload']['input'] = excerpt[2]['payload']['input'].replace('nodeId:"388:2"', 'nodeId:"384:2"')
    fake = copy.deepcopy(evidence); fake['private_exact_runtime_excerpt'] = save('failed-download-carrier-excerpt', excerpt)
    reject('invented_literal_download_carrier', lambda: run(runtime=save('failed-carrier-evidence', fake)),
           'EXCERPT_DOES_NOT_MATCH_REAL_HOST_RUNTIME')
    fake = copy.deepcopy(evidence); fake['download_output_sha256'] = '0' * 64
    reject('spoof_immediate_download_output_digest', lambda: run(runtime=save('failed-download-output', fake)),
           'ACTUAL_BINDING_OUTPUT_CONFLICT')
    duplicate = copy.deepcopy(b.json_file(ROOT, download_ref))
    duplicate[3] = dict(duplicate[2], name='figma-vector-1.svg')
    reject('two_7path_exports_cannot_both_be_brand', lambda: run(download=save('failed-two-brand-exports', duplicate)),
           'OFFICIAL_SVG_ROLE_OR_PATH_COUNT_CONFLICT')

    def native_case(name, mutate, expected):
        value = copy.deepcopy(capture)
        nodes = {n['id']: n for n in value['nodes']}
        mutate(nodes); save('failed-native-' + name, value)
        reject(name, lambda: b.native_capture(ROOT, value, registration, 25), expected)

    native_case('hidden_photo_fill_in_new_headline_frame',
        lambda n: n['388:23']['fills'].append(dict(n['388:3']['fills'][0], visible=False)),
        'HIDDEN_OR_DUPLICATE_PHOTOGRAPHIC_FILL')
    native_case('glyph_one_RGB_unit', lambda n: n['388:25']['fills'][0]['color'].update(r=b.f32(244 / 255)),
                'REGISTERED_VECTOR_COLOR_OR_ALPHA_CHANGED')
    native_case('glyph_unregistered_alpha', lambda n: n['388:25']['fills'][0].update(opacity=.999),
                'REGISTERED_VECTOR_COLOR_OR_ALPHA_CHANGED')

    def shift(nodes):
        q, p = nodes['388:25'], nodes['388:31']
        q['x'] += 1; q['relativeTransform'][0][2] += 1
        q['absoluteTransform'][0][2] = b.f32(p['absoluteTransform'][0][2] + q['x'] - p['x'])
    native_case('coherent_glyph_shift_1px', shift, 'FIGMA_GLYPH_ANCHOR_CHANGED')
    fake = copy.deepcopy(registration); fake['formal_version'] = 26
    reject('future26_fails_closed', lambda: b.verify_actual_binding(ROOT, save('failed-future26', fake), runtime_ref, download_ref),
           'EDIT_LINEAGE_V24_ONLY')
    check = g.compare_pixels(ROOT, registration_ref,
        g.ref(ROOT, ROOT / '.liu-visual-private/correct_source_typography/v25/poster.png'), actual['raw_figma_export'])
    composite_ref = save('actual-whole-frame-composite', check)
    checks.append({'case': 'actual25_full_frame_core78_and_distinct_native_renderer',
        'pass': check['whole_frame_expected']['pixels'] == 0 and check['core_pixels'] == 162052
        and check['core_alpha_positive_pixels'] == 78 and check['core_alpha_zero_pixels'] == 161974
        and not check['figma_raw_bytes_equal_final']
        and check['figma_raw_to_final'] == {'pixels': 7917, 'max_channel_difference': 41}})
    passed = all(x['pass'] for x in checks)
    report = {'schema': 'vpd-registered-type-figma-binding-tests/v1', 'formal_version': 25,
        'result': 'PASS' if passed else 'FAIL', 'exit_code': 0 if passed else 1,
        'actual_command': str(g.RUNTIME / 'python/python.exe') + ' scripts/vpd_probe_registered_type_figma_binding_v25.py --write-evidence',
        'elapsed_seconds': round(time.monotonic() - started, 3), 'checked_utc': datetime.now(timezone.utc).isoformat(),
        'cases': len(checks), 'checks': checks,
        'code': g.ref(ROOT, ROOT / 'visual_memory/vpd_registered_type_figma_binding.py'), 'probe': g.ref(ROOT, Path(__file__)),
        'before_code_sha256': BEFORE_CODE_SHA, 'baseline': baseline_ref, 'positive': positive_ref,
        'registration': registration_ref, 'runtime': runtime_ref, 'download_readback': download_ref,
        'composite': composite_ref, 'positive_geometry': actual['geometry'],
        'source_sha256': g.SOURCE['sha256'], 'native_PNG_sha256': actual['raw_figma_export']['sha256'],
        'native_to_registered_final': check['figma_raw_to_final'],
        'dependencies': dict(g.VERSIONS, fonttools=b.fontTools.__version__),
        'precision': 'Unchanged exact topology/order and immediate-parent float32 sum. Four operand float32 ULPs; frozen brand anchor adds half page ULP. Official export anchor .0005/centered shape .001 plus ULPs. RGB and alpha zero tolerance.',
        'limitations': ['Real host log plus fixed call/input/output/script fingerprints are the trust boundary; no OS attestation.',
            'Inspected V25 download polls write_stdin first then uses literal download args and text(result) in the same actual exec; no wait/cell invented.',
            'Native PNG uses a distinct renderer; its real difference is retained, no aesthetic PASS claimed.',
            'Native-* files isolate geometry/style checks as failed fixtures; whole-entry controls check actual provenance.',
            'Only this private probe and new audit are written; source/assets/caches/old probes/Root guard/business remain untouched.',
            'Old22/23/24 complete returned dictionaries preserved; uninspected26+ fails closed.']}
    encoded = (json.dumps(report, ensure_ascii=False, separators=(',', ':')) + '\n').encode('utf-8')
    g.require(len(encoded) <= 6144, 'BOUNDED_PUBLIC_EVIDENCE_EXCEEDED')
    earlier.write_bytes(encoded)
    if args.write_evidence:
        public = ROOT / 'evidence/vpd/codex_takeover_20261003/audit/REGISTERED_TYPE_FIGMA_BINDING_V25_TESTS.json'
        with public.open('xb') as stream:
            stream.write(encoded)
    print(json.dumps({'result': report['result'], 'cases': len(checks), 'seconds': report['elapsed_seconds'],
                      'failures': [x for x in checks if not x['pass']], 'code': report['code'], 'probe': report['probe']}))
    return report['exit_code']


if __name__ == '__main__':
    raise SystemExit(main())
