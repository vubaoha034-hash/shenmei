"""Actual V26 binding controls; old binding returns and budgets remain exact."""
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

PRIVATE = ROOT / '.liu-visual-private/composite-guard-probe/figma-binding-v26'
AUDIT = ROOT / 'evidence/vpd/codex_takeover_20261003/audit/REGISTERED_TYPE_FIGMA_BINDING_V26_TESTS.json'
BASELINE = {'path': '.liu-visual-private/guard-v26-proposal/OLD_22_23_24_25_BASELINE.json',
            'sha256': 'c4d1a50f0e1de5c7b69ba16805b2999147cb5c7503d6acb7cd95461eedd0dd4b'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--actual', action='store_true', required=True)
    parser.parse_args()
    started = time.monotonic()
    PRIVATE.mkdir(parents=True, exist_ok=True)
    folder = ROOT / g.SERIES / 'v26'
    rr = g.ref(ROOT, folder / 'REGISTERED_TYPE_COMPOSITE.json')
    runtime_ref = g.ref(ROOT, folder / 'FIGMA_BINDING_RUNTIME_EVIDENCE.json')
    download_ref = g.ref(ROOT, ROOT / '.liu-visual-private/correct_source_typography/v26/figma-download-readback.json')
    evidence = b.json_file(ROOT, runtime_ref)
    registration = b.json_file(ROOT, rr)
    capture = b.json_file(ROOT, evidence['actual_capture'])
    baseline = b.json_file(ROOT, BASELINE)['versions']
    checks = []

    def save(name, value):
        path = PRIVATE / (name + '.json')
        raw = (json.dumps(value, ensure_ascii=False, separators=(',', ':')) + '\n').encode('utf-8')
        if path.exists():
            g.require(path.read_bytes() == raw, 'PRIVATE_FIXTURE_CONFLICT:' + name)
        else:
            with path.open('xb') as stream:
                stream.write(raw)
        return g.ref(ROOT, path)

    def reject(name, operation, expected):
        try:
            operation()
        except (ValueError, KeyError, FileNotFoundError) as error:
            g.require(expected in str(error), 'WRONG_NEGATIVE:' + name + ':' + str(error))
            checks.append({'case': name, 'result': 'REJECTED', 'actual': str(error)})
            return
        raise AssertionError('NEGATIVE_ACCEPTED:' + name)

    def run(runtime=runtime_ref, download=download_ref):
        return b.verify_actual_binding(ROOT, rr, runtime, download)

    actual = run()
    positive_ref = save('actual-positive-recomputed', actual)
    g.require(actual['frame_id'] == '391:2' and actual['node_count'] == 21 and actual['vector_count'] == 14
              and all(x['paths'] == 7 for x in actual['geometry'].values()), 'ACTUAL_V26_STRUCTURE_CHANGED')
    checks.append({'case': 'actual26_21nodes_14vectors_source_nativePNG_two7pathSVGs', 'result': 'PASS'})
    for version in (22, 23, 24, 25):
        old = baseline[str(version)]['actual_binding']
        observed = b.verify_actual_binding(ROOT, old['registration'], old['runtime_evidence'], old['download_readback'])
        g.require(observed == old, 'OLD_COMPLETE_BINDING_CHANGED:' + str(version))
        checks.append({'case': f'old{version}_complete_binding_return', 'result': 'PASS'})
    old = baseline['25']['actual_binding']
    old_evidence = b.json_file(ROOT, old['runtime_evidence'])
    fake = copy.deepcopy(old_evidence); fake['formal_version'] = 26
    reject('v25_runtime_relabelled26', lambda: run(runtime=save('failed-v25-relabelled', fake)),
           'ACTUAL_V26_RUNTIME_EVIDENCE_REQUIRED')
    for name, field, error in [('v25_capture_reuse', 'actual_capture', 'ACTUAL_CAPTURE_BODY_FINGERPRINT_CONFLICT'),
                               ('v25_nativePNG_reuse', 'actual_native_export_ref', 'ACTUAL_ORIGINAL_IMAGE_OR_FRAME_EXPORT_CHANGED')]:
        fake = copy.deepcopy(evidence); fake[field] = old_evidence[field]
        reject(name, lambda f=save('failed-' + name, fake): run(runtime=f), error)
    excerpt = b.json_file(ROOT, evidence['private_exact_runtime_excerpt'])
    excerpt[2]['payload']['input'] = 'text(await tools.write_stdin({session_id:0}));\n' + excerpt[2]['payload']['input']
    fake = copy.deepcopy(evidence); fake['private_exact_runtime_excerpt'] = save('failed-v25-poll-carrier', excerpt)
    reject('invented_poll_download_carrier', lambda: run(runtime=save('failed-carrier-evidence', fake)),
           'EXCERPT_DOES_NOT_MATCH_REAL_HOST_RUNTIME')
    duplicate = copy.deepcopy(b.json_file(ROOT, download_ref))
    duplicate[2] = dict(duplicate[3], name='figma-vector-0.svg')
    reject('two7path_exports_cannot_both_be_brand', lambda: run(download=save('failed-two-brand-exports', duplicate)),
           'OFFICIAL_SVG_ROLE_OR_PATH_COUNT_CONFLICT')

    def native_case(name, mutate, expected):
        value = copy.deepcopy(capture); nodes = {n['id']: n for n in value['nodes']}
        mutate(nodes); save('failed-native-' + name, value)
        reject(name, lambda: b.native_capture(ROOT, value, registration, 26), expected)

    native_case('glyph_one_RGB_unit', lambda n: n['391:25']['fills'][0]['color'].update(r=b.f32(244 / 255)),
                'REGISTERED_VECTOR_COLOR_OR_ALPHA_CHANGED')
    native_case('glyph_alpha_unregistered', lambda n: n['391:25']['fills'][0].update(opacity=.999),
                'REGISTERED_VECTOR_COLOR_OR_ALPHA_CHANGED')

    def endpoint(nodes):
        vector = nodes['391:30']['vectorPaths'][0]
        d = vector['data']
        last = list(re.finditer(r'C\s*([^MLCZ]*)', d))[-1]
        numbers = list(re.finditer(r'[-+]?(?:\d*\.\d+|\d+\.?\d*)(?:[eE][-+]?\d+)?', last[1]))
        g.require(len(numbers) == 6, 'ACTUAL_LAST_NATIVE_CUBIC_REQUIRED')
        q = numbers[-1]
        start, stop = last.start(1) + q.start(), last.start(1) + q.end()
        vector['data'] = d[:start] + str(float(q[0]) + 1) + d[stop:]
    native_case('actual_native_last_C_endpoint_one_unit', endpoint, 'FIGMA_GLYPH_TOPOLOGY_CHANGED')
    fake = copy.deepcopy(registration); fake['formal_version'] = 27
    reject('future27', lambda: b.verify_actual_binding(ROOT, save('failed-future27', fake), runtime_ref, download_ref),
           'EDIT_LINEAGE_V24_ONLY')
    check = g.compare_pixels(ROOT, rr,
        g.ref(ROOT, ROOT / '.liu-visual-private/correct_source_typography/v26/poster.png'), actual['raw_figma_export'])
    composite_ref = save('actual-whole-frame-composite', check)
    g.require(check['whole_frame_expected']['pixels'] == 0 and check['core_pixels'] == 162052
              and check['core_alpha_positive_pixels'] == 0 and check['core_alpha_zero_pixels'] == 162052
              and not check['figma_raw_bytes_equal_final']
              and check['figma_raw_to_final'] == {'pixels': 7666, 'max_channel_difference': 42}, 'ACTUAL_V26_FINAL_CHANGED')
    checks.append({'case': 'actual26_full_frame_core0_native_renderer_difference_retained', 'result': 'PASS'})
    report = {'schema': 'vpd-registered-type-figma-binding-tests/v1', 'formal_version': 26, 'result': 'PASS', 'exit_code': 0,
        'actual_command': str(g.RUNTIME / 'python/python.exe') + ' scripts/vpd_probe_registered_type_figma_binding_v26.py --actual',
        'seconds': round(time.monotonic() - started, 3), 'checked_utc': datetime.now(timezone.utc).isoformat(),
        'cases': len(checks), 'checks': checks, 'code': g.ref(ROOT, ROOT / 'visual_memory/vpd_registered_type_figma_binding.py'),
        'probe': g.ref(ROOT, Path(__file__)), 'registration': rr, 'runtime': runtime_ref, 'download_readback': download_ref,
        'baseline': BASELINE, 'positive': positive_ref, 'composite': composite_ref,
        'geometry': actual['geometry'], 'source_sha256': g.SOURCE['sha256'],
        'nativePNG_sha256': actual['raw_figma_export']['sha256'], 'native_to_final': check['figma_raw_to_final'],
        'previous_complete_pixels_and_factory_tests': {'path': 'evidence/vpd/codex_takeover_20261003/audit/REGISTERED_TYPE_EDITED_LINEAGE_V26_TESTS.json',
            'sha256': '60a6e87d416cc614e6614ebb54f653fa6831e66fb04d2b1457445c434da0f9eb'},
        'dependencies': dict(g.VERSIONS, fonttools=b.fontTools.__version__),
        'initial_actual_failure': {'completion_chunk': '97da53', 'exit_code': 1,
            'error': 'WRONG_NEGATIVE:actual_native_last_C_endpoint_one_unit:FIGMA_GLYPH_TOPOLOGY_CHANGED',
            'repair': 'Probe error classification only: changed closing endpoint adds an implicit lineTo; validator correctly rejects topology.',
            'preserved': g.ref(ROOT, PRIVATE / 'first-failed-probe.json')},
        'precision': 'Unchanged exact topology/order and immediate-parent float32 sum. Four operand float32 ULPs; frozen brand anchor half page ULP. Official 3-decimal export anchor .0005/centered shape .001 plus ULPs. RGB and alpha zero tolerance.',
        'limitations': ['Real host log and fixed input/output/script fingerprints are the trust boundary; no operating-system attestation.',
            'V26 inspected literal download is immediate full result; V25 poll carrier is not invented or reused.',
            'Both official SVGs contain seven paths; IDs/viewport/all curves determine the role, independent of returned file order.',
            'Actual native PNG differs from registered final; all differences retained, no aesthetic PASS.',
            'Native-* files isolate style/curve checks as failed fixtures; complete-entry controls check actual provenance.',
            'Only own private fixtures and new probe/audit written; source/assets/caches/Root guard/business untouched. Old22–25 complete binding returns unchanged; 27+ fails closed.']}
    raw = (json.dumps(report, ensure_ascii=False, separators=(',', ':')) + '\n').encode('utf-8')
    g.require(len(raw) <= 6144, 'BOUNDED_PUBLIC_EVIDENCE_EXCEEDED')
    with AUDIT.open('xb') as stream:
        stream.write(raw)
    print(json.dumps({'result': 'PASS', 'cases': len(checks), 'seconds': report['seconds'], 'code': report['code'],
                      'probe': report['probe'], 'audit': g.ref(ROOT, AUDIT)}))


if __name__ == '__main__':
    main()
