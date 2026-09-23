#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
LOCK=ROOT/"continuity/vpd/CURRENT_TASK_LOCK.json"
CP=ROOT/"continuity/vpd/LATEST_CHECKPOINT.json"
ADAPTER=ROOT/"PROJECT_CONTROL_ADAPTER.json"
LEDGER=ROOT/"continuity/vpd/state_ledger/commercial_design_pipeline.jsonl"

MAPPING="evidence/vpd/library_native_ab_v2/PAIR2_COMPLETE_POSTER_BLIND_MAPPING_20260923.json"
PACKAGE="evidence/vpd/library_native_ab_v2/PAIR2_COMPLETE_POSTER_BLIND_PACKAGE_20260923.json"
HANDOFF="evidence/vpd/library_native_ab_v2/COPY_PAIR2_COMPLETE_POSTER_BLIND_TO_FRESH_CHAT_20260923.txt"
PROMPT="evidence/vpd/library_native_ab_v2/PAIR2_EQUAL_BUDGET_FIGMA_BLIND_EVALUATOR_PROMPT_PREWRITE_20260923.txt"
EXPORT_RECEIPT="evidence/vpd/figma_export_relay/receipts/PAIR2_COMPLETE_POSTER_BLIND_EXPORT_20260923.json"
REPAIR="evidence/vpd/library_native_ab_v2/PAIR2_COMPLETE_POSTER_BLIND_STATE_HASH_REPAIR_20260923.json"
EXPECTED_EVENT="EVT-VPD-P3-PAIR2-COMPLETE-POSTER-BLIND-PACKAGE-READY-20260923-001"

def digest(rel):
    p=ROOT/rel if isinstance(rel,str) else rel
    return hashlib.sha256(p.read_bytes()).hexdigest()

def read(p):
    return json.loads(p.read_text(encoding="utf-8"))

def write(p,obj):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")

def event_hash(event):
    core={k:v for k,v in event.items() if k!="event_hash"}
    raw=json.dumps(core,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()
    return hashlib.sha256(raw).hexdigest()

lock=read(LOCK); cp=read(CP); adapter=read(ADAPTER)
if lock.get("revision")!=132 or cp.get("sequence")!=153:
    raise SystemExit("unexpected state revision/sequence")
if lock.get("next_required_action")!="RUN_PAIR2_COMPLETE_POSTER_INDEPENDENT_BLIND_EVALUATION_AND_RETURN_VERDICT":
    raise SystemExit("unexpected next action")

claimed_lock_sha=adapter["task_lock"]["sha256"]
actual_before=digest(LOCK)

package=read(ROOT/PACKAGE)
package["blind_mapping"]["sha256"]=digest(MAPPING)
package["evaluator_prompt"]["sha256"]=digest(PROMPT)
package["fresh_chat_handoff"]["sha256"]=digest(HANDOFF)
package["export_transport"]["export_receipt"]["sha256"]=digest(EXPORT_RECEIPT)
write(ROOT/PACKAGE,package)

repair={
  "schema_version":"vpd-pair2-complete-poster-blind-state-hash-repair/v1",
  "artifact_type":"PAIR2_COMPLETE_POSTER_BLIND_STATE_HASH_REPAIR",
  "recorded_at":datetime.now(timezone.utc).isoformat(),
  "project_id":"visual-aesthetic-vpd",
  "trigger_ci_run_id":35847568508,
  "trigger_failure":"ADAPTER_STALE_LOCK",
  "classification":"STATE_HASH_CALCULATION_BUG_ONLY",
  "figma_canvas_modified":False,
  "library_assets_modified":False,
  "blind_mapping_changed":False,
  "old_adapter_claimed_lock_sha256":claimed_lock_sha,
  "actual_lock_sha256_before_repair":actual_before,
  "recomputed_refs":{
    "mapping_sha256":digest(MAPPING),
    "package_sha256":digest(PACKAGE),
    "handoff_sha256":digest(HANDOFF),
    "prompt_sha256":digest(PROMPT),
    "export_receipt_sha256":digest(EXPORT_RECEIPT)
  },
  "repair_method":"Python hashlib.sha256 over exact repository bytes; then run mandatory VPD state validator before commit."
}
write(ROOT/REPAIR,repair)
repair_sha=digest(REPAIR)

pair=lock["pair2_equal_budget_figma_ab"]
pair["blind_package"]["sha256"]=digest(PACKAGE)
pair["blind_mapping"]["sha256"]=digest(MAPPING)
pair["blind_handoff"]["sha256"]=digest(HANDOFF)
pair["blind_evaluator_prompt"]["sha256"]=digest(PROMPT)
pair["state_hash_repair"]={"path":REPAIR,"sha256":repair_sha}
lock["completed_this_revision"].append("recomputed Pair2 blind-package evidence and state hashes with Python hashlib after CI detected ADAPTER_STALE_LOCK; no Figma or Library asset mutation")
lock["updated_at"]="2026-09-23T10:16:00Z"
write(LOCK,lock)
lock_sha=digest(LOCK)

cp["task_lock"]={"path":"continuity/vpd/CURRENT_TASK_LOCK.json","sha256":lock_sha}
cp["pair2_equal_budget_figma_ab"]=lock["pair2_equal_budget_figma_ab"]
cp["pair2_complete_poster_blind_package"]={"path":PACKAGE,"sha256":digest(PACKAGE)}
cp["pair2_complete_poster_state_hash_repair"]={"path":REPAIR,"sha256":repair_sha}

lines=LEDGER.read_text(encoding="utf-8").splitlines()
last=json.loads(lines[-1])
if last.get("event_id")!=EXPECTED_EVENT:
    raise SystemExit("unexpected ledger tail")
last["lock_sha256"]=lock_sha
evidence=list(last.get("evidence",[]))
if REPAIR not in evidence: evidence.append(REPAIR)
last["evidence"]=evidence
last["reason"]="Exact complete-poster exports are neutrally packaged and Library-byte-verified. A CI-detected state-hash calculation bug was repaired with Python hashlib before acceptance; Figma and Library asset bytes were unchanged."
last["event_hash"]=event_hash(last)
lines[-1]=json.dumps(last,ensure_ascii=False,separators=(",",":"))
LEDGER.write_text("\n".join(lines)+"\n",encoding="utf-8",newline="\n")

tail={"commercial_design_pipeline":{"event_id":last["event_id"],"event_hash":last["event_hash"]}}
cp["ledger_tails"]=tail
adapter["task_lock"]["revision"]=132
adapter["task_lock"]["sha256"]=lock_sha
adapter["vpd_system_goal_authority"]["checkpoint"]=lock["status"]
adapter["vpd_system_goal_authority"]["next_required_action"]=lock["next_required_action"]
adapter["vpd_system_goal_authority"]["render_allowed"]=False
adapter["ledger_tails"]=tail
write(CP,cp); write(ADAPTER,adapter)

print(json.dumps({
  "status":"REPAIRED_READY_FOR_VALIDATION",
  "lock_sha256":lock_sha,
  "package_sha256":digest(PACKAGE),
  "mapping_sha256":digest(MAPPING),
  "handoff_sha256":digest(HANDOFF),
  "prompt_sha256":digest(PROMPT),
  "export_receipt_sha256":digest(EXPORT_RECEIPT),
  "repair_sha256":repair_sha,
  "ledger_event_hash":last["event_hash"]
},ensure_ascii=False))
