"""Scoped two-image carrier adapter; the existing Tea/reconstruction collector is unchanged.

Run the pinned existing collector to extract only actual call/context/image/final
evidence. Then require Root's separately inspected exact-call manifest. This is
observed read-scope verification, not an OS sandbox or project-external Tea audit.
"""
import argparse, hashlib, json, pathlib, subprocess, sys

CORE_SHA = '403f44ceaf3332b5febd91f8b02d98bcb9d0bc4b102c9dc0aed4d5f11dd900ba'
SCOPE = 'SHANYEJI_REFERENCE_TYPOGRAPHY_CONTENT_TRANSFER_EXPERIMENT'
REFERENCE = '9a29fbdc7dd908017924bed270e8dfe18351519eed3fa7bc7001789f2a383414'
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('child_runtime', type=pathlib.Path)
p.add_argument('output', type=pathlib.Path)
p.add_argument('--parent-runtime', required=True, type=pathlib.Path)
p.add_argument('--reviewed-call-manifest', required=True, type=pathlib.Path)
q = p.parse_args()
def require(ok, message):
    if not ok:raise RuntimeError(message)
root = pathlib.Path.cwd()
core = root/'scripts/vpd_collect_reference_study_review.py'
require(hashlib.sha256(core.read_bytes()).hexdigest() == CORE_SHA, 'CORE_CHANGED_REVIEW_REQUIRED')
m = json.loads(q.reviewed_call_manifest.read_text(encoding='utf-8'))
require(m['schema'] == 'vpd-root-inspected-review-call-manifest/v1' and m['scope'] == SCOPE, 'MANIFEST_SCOPE_REQUIRED')
require(m['root_read_actual_call_bodies'] is True and m['reference_sha256'] == REFERENCE, 'ROOT_INSPECTION_AND_REFERENCE_REQUIRED')
require(m['allowed_inputs'] == ['specified_reference', 'specified_export', 'installed_design_critique', 'own_runtime_identity', 'own_report_readback'], 'INPUT_SCOPE_REQUIRED')
require(m['allowed_writes'] == ['own_review_report'], 'WRITE_SCOPE_REQUIRED')
subprocess.run([sys.executable, '-X', 'utf8', '-B', str(core), str(q.child_runtime), str(q.output), '--parent-runtime', str(q.parent_runtime)], check=True)
out = root/q.output
ap = out/'ISOLATION_AUDIT.json'
a = json.loads(ap.read_text(encoding='utf-8'))
review = json.loads((out/'PIXEL_REVIEW.json').read_text(encoding='utf-8'))
native_finals = []
for line in q.child_runtime.open(encoding='utf-8'):
    row = json.loads(line); payload = row.get('payload', {})
    if row.get('type') == 'response_item' and payload.get('type') == 'message' and payload.get('role') == 'assistant' and (payload.get('channel') == 'final' or payload.get('phase') == 'final_answer'):
        for block in payload.get('content', []):
            if block.get('type') in ['output_text', 'text']:
                try: value = json.loads(block.get('text', '').strip())
                except ValueError: continue
                if value.get('schema') == 'vpd-reference-typography-pixel-review/v1':native_finals.append(value)
raw_final_exact = bool(native_finals) and native_finals[-1] == review
identity_enriched = bool(native_finals) and 'reviewer_thread_id' not in native_finals[-1]
if native_finals:
    native_finals[-1].setdefault('reviewer_thread_id', a['reviewer_thread_id'])
require(native_finals and native_finals[-1] == review, 'NATIVE_FINAL_REVIEW_BINDING_REQUIRED')
(out/'UNCHANGED_CORE_AUDIT.json').write_bytes(ap.read_bytes())
actual = a['actual_tool_calls']
expected = [{k:x[k] for k in ['name', 'call_id', 'input_sha256']} for x in m['calls']]
exact = actual == expected and all(x['purpose'] for x in m['calls'])
bound = (a['scope'] == SCOPE and a['reference_sha256'] == REFERENCE
    and a['study_export_sha256'] == m['study_export_sha256'] == review['study_export_sha256']
    and a['reviewer_thread_id'] == m['reviewer_thread_id'] == review['reviewer_thread_id']
    and len(a['actual_turn_contexts']) == 1 and a['actual_model'] == 'gpt-6.1-sol'
    and a['actual_reasoning_effort'] == 'max' and a['parent_spawn_verified'] is True
    and len(a['actual_image_reads']) == 2
    and {x['sha256'] for x in a['actual_image_reads']} == {REFERENCE, m['study_export_sha256']}
    and review['actual_pixels_seen'] is True and review['human_acceptance'] == 'PENDING')
a['carrier'] = 'CONTENT_TRANSFER_FRESH_TWO_IMAGE_SUBAGENT'
a['original_project_external_tea_review_route_replaced'] = False
a['verified'] = exact and bound
a['pixels_seen'] = len(a['actual_image_reads'])
a['tool_scope_violations'] = [] if exact else ['EXACT_CALL_MANIFEST_MISMATCH']
a['reviewed_call_manifest'] = {'path':q.reviewed_call_manifest.as_posix(), 'sha256':hashlib.sha256(q.reviewed_call_manifest.read_bytes()).hexdigest()}
a['unchanged_core_sha256'] = CORE_SHA
a['native_final_exact_match'] = True
a['native_final_raw_exact_match'] = raw_final_exact
a['identity_enrichment_applied'] = identity_enriched
a['native_final_compared_equality'] = True
a['limitations'].append('Root inspected each exact observed call body; this allowlist cannot authorize any unobserved future call. Original Tea project-external audit remains required for Tea.')
ap.write_text(json.dumps(a, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
review['isolation_audit'] = {'path':ap.relative_to(root).as_posix(), 'sha256':hashlib.sha256(ap.read_bytes()).hexdigest()}
(out/'PIXEL_REVIEW.json').write_text(json.dumps(review, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps({'verified':a['verified'], 'actual_calls':len(actual), 'pixels':a['pixels_seen'], 'verdict':review['verdict']}))
if not a['verified']:raise SystemExit(2)
