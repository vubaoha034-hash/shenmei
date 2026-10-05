"""Actual V28 binding controls; old full returns and budgets remain exact."""
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
PRIVATE = ROOT / '.liu-visual-private/guard-v28-proposal/actual-binding'
AUDIT = ROOT / 'evidence/vpd/codex_takeover_20261003/audit/REGISTERED_TYPE_FIGMA_BINDING_V28_TESTS.json'
BASELINE = {'path': '.liu-visual-private/guard-v28-proposal/OLD_22_23_24_25_26_27_BASELINE.json', 'sha256': '888fe9360d3ac2a4d9fd596cb3f297f5851caf86eefd601fb78d04d5abb4b3fd'}
LINEAGE_TESTS = g.ref(ROOT, ROOT / 'evidence/vpd/codex_takeover_20261003/audit/REGISTERED_TYPE_EDITED_LINEAGE_V28_TESTS.json')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--actual', action='store_true', required=True)
    parser.parse_args()
    started = time.monotonic()
    PRIVATE.mkdir(parents=True, exist_ok=True)
    folder = ROOT / g.SERIES / 'v28'
    rr = g.ref(ROOT, ROOT / '.liu-visual-private/guard-v28-proposal/actual-lineage/actual-registration.json')
    runtime_ref = g.ref(ROOT, folder / 'FIGMA_BINDING_RUNTIME_EVIDENCE.json')
    download_ref = g.ref(ROOT, ROOT / '.liu-visual-private/correct_source_typography/v28/figma-download-readback.json')
    evidence = b.json_file(ROOT, runtime_ref)
    registration = b.json_file(ROOT, rr)
    capture = b.json_file(ROOT, evidence['actual_capture'])
    baseline = b.json_file(ROOT, BASELINE)
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
    g.require(actual['frame_id'] == b.V28_NATIVE['ids']['2'] and actual['node_count'] == 21 and (actual['vector_count'] == 14) and all((x['paths'] == 7 for x in actual['geometry'].values())), 'ACTUAL_V28_STRUCTURE_CHANGED')
    checks.append({'case': 'actual28_real_runtime_capture_source_nativePNG_two7pathSVGs', 'result': 'PASS'})
    print(json.dumps({'actual28_binding': 'PASS', 'geometry': actual['geometry']}), flush=True)
    reverse_ref = save('actual-official-order-reversed', list(reversed(b.json_file(ROOT, download_ref))))
    reversed_actual = run(download=reverse_ref)
    g.require(reversed_actual == dict(actual, download_readback=reverse_ref), 'ACTUAL28_OFFICIAL_ROLE_ORDER_DEPENDENCE')
    checks.append({'case':'actual28_both7path_official_roles_independent_of_file_order','result':'PASS'})
    for version in (22, 23, 24, 25, 26, 27):
        prior = baseline['versions'][str(version)]
        old_rr, old = (prior['registration_ref'], prior['actual_binding'])
        image, overlay, old_reg = g.replay(ROOT, old_rr)
        observed = {'registration_ref': old_rr, 'registration': old_reg, 'expected_RGB': {'mode': image.mode, 'size': list(image.size), 'bytes': len(image.tobytes()), 'sha256': g.sha(image.tobytes())}, 'overlay_RGBA': {'mode': overlay.mode, 'size': list(overlay.size), 'bytes': len(overlay.tobytes()), 'sha256': g.sha(overlay.tobytes()), 'alpha_sha256': g.sha(overlay.getchannel('A').tobytes())}, 'compare_pixels': g.compare_pixels(ROOT, old_rr, prior['compare_pixels']['final'], old['raw_figma_export']), 'actual_binding': b.verify_actual_binding(ROOT, old_rr, old['runtime_evidence'], old['download_readback']), 'frozen_binding_check_ref': g.ref(ROOT, ROOT / prior['frozen_binding_check_ref']['path'])}
        g.require(observed == prior, 'OLD_COMPLETE_RETURN_CHANGED:' + str(version))
        original_pixels = baseline['replayed_pixel_files'][str(version)]
        g.require(image.tobytes() == g.checked_bytes(ROOT, original_pixels['expected_RGB']) and overlay.tobytes() == g.checked_bytes(ROOT, original_pixels['overlay_RGBA']) and (overlay.getchannel('A').tobytes() == g.checked_bytes(ROOT, original_pixels['overlay_alpha'])), 'OLD_COMPLETE_PIXEL_BYTES_CHANGED:' + str(version))
        checks.append({'case': f'old{version}_complete_registration_RGB_RGBA_alpha_compare_binding', 'result': 'PASS'})
        print(json.dumps({'old_version': version, 'complete_equal': True}), flush=True)
    g.require(g.edited_lineage(ROOT) == baseline['factories']['24'] and all((g.edited_lineage(ROOT, v) == baseline['factories'][str(v)] for v in (24, 25, 26, 27))), 'OLD_FACTORY_RETURN_CHANGED')
    old = baseline['versions']['27']['actual_binding']
    old_evidence = b.json_file(ROOT, old['runtime_evidence'])
    fake = copy.deepcopy(old_evidence)
    fake['formal_version'] = 28
    reject('v27_runtime_relabelled28', lambda: run(runtime=save('failed-v27-relabelled', fake)), 'ACTUAL_V28_RUNTIME_EVIDENCE_REQUIRED')
    for name, field, error in [('v27_capture_reuse', 'actual_capture', 'ACTUAL_CAPTURE_BODY_FINGERPRINT_CONFLICT'), ('v27_nativePNG_reuse', 'actual_native_export_ref', 'ACTUAL_ORIGINAL_IMAGE_OR_FRAME_EXPORT_CHANGED')]:
        fake = copy.deepcopy(evidence)
        fake[field] = old_evidence[field]
        reject(name, lambda f=save('failed-' + name, fake): run(runtime=f), error)
    excerpt = b.json_file(ROOT, evidence['private_exact_runtime_excerpt'])
    excerpt[2]['payload']['input'] = 'text(await tools.write_stdin({session_id:0}));\n' + excerpt[2]['payload']['input']
    fake = copy.deepcopy(evidence)
    fake['private_exact_runtime_excerpt'] = save('failed-invented-poll-carrier', excerpt)
    reject('invented_poll_download_carrier', lambda: run(runtime=save('failed-carrier-evidence', fake)), 'EXCERPT_DOES_NOT_MATCH_REAL_HOST_RUNTIME')
    duplicate = copy.deepcopy(b.json_file(ROOT, download_ref))
    brand = next((item for item in duplicate if item['name'] == b.V28_NATIVE['official_brand_name']))
    duplicate = [dict(brand, name=item['name']) if item['name'].endswith('.svg') and item['name'] != brand['name'] else item for item in duplicate]
    reject('two7path_exports_cannot_both_be_brand', lambda: run(download=save('failed-two-brand-exports', duplicate)), 'OFFICIAL_SVG_ROLE_OR_PATH_COUNT_CONFLICT')

    def native_case(name, mutate, expected):
        value = copy.deepcopy(capture)
        nodes = {n['id']: n for n in value['nodes']}
        mutate(nodes)
        save('failed-native-' + name, value)
        reject(name, lambda: b.native_capture(ROOT, value, registration, 28), expected)
    native_case('glyph_one_RGB_unit', lambda n: n[b.V28_NATIVE['ids']['25']]['fills'][0]['color'].update(r=b.f32(244 / 255)), 'REGISTERED_VECTOR_COLOR_OR_ALPHA_CHANGED')

    def control_point(nodes):
        vector = nodes[b.V28_NATIVE['ids']['30']]['vectorPaths'][0]
        d = vector['data']
        last = list(re.finditer('C\\s*([^MLCZ]*)', d))[-1]
        numbers = list(re.finditer('[-+]?(?:\\d*\\.\\d+|\\d+\\.?\\d*)(?:[eE][-+]?\\d+)?', last[1]))
        g.require(len(numbers) == 6, 'ACTUAL_LAST_NATIVE_CUBIC_REQUIRED')
        q = numbers[0]
        start, stop = (last.start(1) + q.start(), last.start(1) + q.end())
        vector['data'] = d[:start] + str(float(q[0]) + 1) + d[stop:]
    native_case('actual_native_last_C_control_one_unit', control_point, 'FIGMA_GLYPH_CONTROL_COORDINATE_CHANGED')
    fake = copy.deepcopy(registration)
    fake['formal_version'] = 29
    reject('future29', lambda: b.verify_actual_binding(ROOT, save('failed-future29', fake), runtime_ref, download_ref), 'EDIT_LINEAGE_V24_ONLY')
    check = g.compare_pixels(ROOT, rr, {'path': '.liu-visual-private/correct_source_typography/v28/preview.png', 'sha256': '1000c0a35a43cf1cfb8803735cd00abb039d20147676254a1db57c2722f6a8ac'}, actual['raw_figma_export'])
    composite_ref = save('actual-whole-frame-composite', check)
    g.require(check['whole_frame_expected'] == {'pixels': 0, 'max_channel_difference': 0} and check['core_pixels'] == 162052 and (check['core_alpha_positive_pixels'] + check['core_alpha_zero_pixels'] == 162052), 'ACTUAL_V28_FINAL_CHANGED')
    checks.append({'case': 'actual28_full_frame_complete_core_native_renderer_difference_retained', 'result': 'PASS'})
    g.checked_bytes(ROOT, LINEAGE_TESTS)
    for key in ('vpd_registered_type_edited_lineage', 'vpd_registered_type_edited_lineage_v25', 'vpd_registered_type_edited_lineage_v26', 'vpd_registered_type_edited_lineage_v27'):
        g.checked_bytes(ROOT, baseline['before_code'][key])
    report = {'schema': 'vpd-registered-type-figma-binding-tests/v1', 'formal_version': 28, 'result': 'PASS', 'exit_code': 0, 'actual_command': str(g.RUNTIME / 'python/python.exe') + ' -B -u scripts/vpd_probe_registered_type_figma_binding_v28.py --actual', 'seconds': round(time.monotonic() - started, 3), 'checked_utc': datetime.now(timezone.utc).isoformat(), 'cases': len(checks), 'checks': checks, 'code': g.ref(ROOT, ROOT / 'visual_memory/vpd_registered_type_figma_binding.py'), 'probe': g.ref(ROOT, Path(__file__)), 'registration': rr, 'runtime': runtime_ref, 'download_readback': download_ref, 'baseline': BASELINE, 'positive': positive_ref, 'composite': composite_ref, 'geometry': actual['geometry'], 'source_sha256': g.SOURCE['sha256'], 'nativePNG_sha256': actual['raw_figma_export']['sha256'], 'native_to_final': check['figma_raw_to_final'], 'previous_lineage_controls': LINEAGE_TESTS, 'default24_and_old25_26_factories_equal': True, 'dependencies': dict(g.VERSIONS, fonttools=b.fontTools.__version__), 'precision': 'Unchanged exact topology/order and immediate-parent float32 sum. Four operand float32 ULPs; frozen brand anchor half page ULP. Official 3-decimal anchor .0005/centered shape .001 plus ULPs. RGB/alpha zero tolerance.', 'limitations': ['Real host log and fixed input/output/script fingerprints are the boundary; no operating-system attestation.', 'V28 literal download is immediate full actual result; no invented prefix, poll or wait.', 'Two official SVGs both have seven paths; IDs/viewport/all curves identify the roles independently of file order.', 'Raw native PNG differs from registered final; actual difference retained, no aesthetic PASS.', 'Native-* countercases isolate curve/color checks; complete-entry negatives enforce actual provenance.', 'Only own private fixtures and new probe/audit written. Old22-27 complete registration/pixel/compare/binding returns and old factories unchanged; 29+ fails closed.']}
    raw = (json.dumps(report, ensure_ascii=False, separators=(',', ':')) + '\n').encode('utf-8')
    g.require(len(raw) <= 6144, 'BOUNDED_PUBLIC_EVIDENCE_EXCEEDED')
    with AUDIT.open('xb') as stream:
        stream.write(raw)
    print(json.dumps({'result': 'PASS', 'cases': len(checks), 'seconds': report['seconds'], 'code': report['code'], 'probe': report['probe'], 'audit': g.ref(ROOT, AUDIT), 'positive': positive_ref}))
if __name__ == '__main__':
    main()
