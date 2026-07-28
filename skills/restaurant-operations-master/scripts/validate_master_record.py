#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,sys
from pathlib import Path
SECTIONS=["contract","baseline","unit_economics","menu_capacity","customer_brand","supplier_safety","panels","pilot","status"]
PANELS={"customer","front","kitchen","finance","brand","safety"}
STATUSES={"DATA_INCOMPLETE","DIAGNOSIS_ONLY","HYPOTHESIS_READY","PILOT_READY","PILOT_RUNNING","PILOT_PASS","PILOT_FAIL","ROLLOUT_READY","ROLLOUT_RUNNING","STANDARDIZED"}
def digest(d):
 c=dict(d);c.pop("record_sha256",None);return hashlib.sha256(json.dumps(c,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
 if len(sys.argv)!=2:print("usage: validate_master_record.py RECORD.json",file=sys.stderr);return 2
 try:d=json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
 except Exception as e:print(f"FAIL invalid_json:{e}");return 1
 errors=[f"missing:{k}" for k in SECTIONS if k not in d]
 if not PANELS.issubset(d.get("panels",{})):errors.append("incomplete_panels")
 if d.get("status") not in STATUSES:errors.append("invalid_status")
 if d.get("supplier_safety",{}).get("blocker") and d.get("status") not in {"DATA_INCOMPLETE","DIAGNOSIS_ONLY","PILOT_FAIL"}:errors.append("food_safety_blocker_not_enforced")
 if d.get("status") in {"ROLLOUT_READY","ROLLOUT_RUNNING","STANDARDIZED"} and d.get("pilot",{}).get("result")!="PASS":errors.append("rollout_without_pilot_pass")
 if d.get("record_sha256") and d["record_sha256"]!=digest(d):errors.append("sha_mismatch")
 if errors:print("FAIL");[print(x) for x in errors];return 1
 print("PASS");print(f"record_sha256:{digest(d)}");return 0
if __name__=="__main__":raise SystemExit(main())
