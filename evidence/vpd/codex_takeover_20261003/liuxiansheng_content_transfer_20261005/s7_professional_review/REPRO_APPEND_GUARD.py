"""TEST_ONLY state-copy reproducer. Does not write business state or artifacts."""
from pathlib import Path
import copy, json, hashlib, sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from visual_memory import vpd_reference_typography_study as study
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
unit = copy.deepcopy(json.loads((ROOT/'continuity/vpd/CURRENT_TASK_LOCK.json').read_text(encoding='utf8'))['codex_takeover']['worker_continuation'])
unit['phase'] = 'REFERENCE_STUDY_ACTIVE'
transfer = unit['content_transfer_experiment']
transfer['attempts'] = transfer['attempts'][:6]
assert len(transfer['attempts']) == 6
fixture = Path(__file__).with_name('TEST_ONLY_UNISOLATED_S6_BASIS.json')
transfer['attempts'].append({'kind':'TARGETED_REPAIR','export':copy.deepcopy(transfer['attempts'][5]['export']),'repair_basis':{'path':fixture.relative_to(ROOT).as_posix(),'sha256':sha(fixture)},'test_fixture_only':True})
print('source_sha256', sha(ROOT/'visual_memory/vpd_reference_typography_study.py'), flush=True)
try:
    study._validate_transfer(ROOT, unit)
    print('FAIL: ACCEPTED_UNBOUND_UNISOLATED_S7_BASIS')
except Exception as exc:
    print(type(exc).__name__ + ': ' + str(exc))

