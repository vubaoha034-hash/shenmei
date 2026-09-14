#!/usr/bin/env python3
"""Record the already-executed P1 T1 typography-only title bench.

This script does not create or modify Figma pixels. It records the completed
A/B builds, the consumed one-pass B corrections, the Drive blind-review deck,
and advances state to the human blind-verdict gate. Candidate A/B mapping is
not committed; only a pre-verdict commitment hash is stored.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "continuity/vpd/CURRENT_TASK_LOCK.json"
CP = ROOT / "continuity/vpd/LATEST_CHECKPOINT.json"
ADAPTER = ROOT / "PROJECT_CONTROL_ADAPTER.json"
LEDGER = ROOT / "continuity/vpd/state_ledger/commercial_design_pipeline.jsonl"
EVID = ROOT / "evidence/vpd/p1_typography_repair_v1/T1_TITLE_BENCH_EXECUTION_20260914.json"


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def dump(p: Path, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha_file(p: Path):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def ref(p: Path):
    return {"path": p.relative_to(ROOT).as_posix(), "sha256": sha_file(p)}


def git_blob(path: str):
    return subprocess.check_output(["git", "rev-parse", f"HEAD:{path}"], cwd=ROOT, text=True).strip()


def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def event_hash(event_without_hash):
    raw = json.dumps(event_without_hash, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def main():
    lock = load(LOCK)
    cp = load(CP)
    adapter = load(ADAPTER)
    if lock.get("revision") != 35 or lock.get("state_profile") != "p6-composition/v1":
        raise SystemExit("unexpected source state; T1 execution record is revision-35-only")
    if lock.get("next_required_action") != "P1_EXECUTE_TYPOGRAPHY_ONLY_TITLE_BENCH":
        raise SystemExit("unexpected source action")
    tr = lock.get("typography_repair", {})
    if tr.get("status") != "PREPARED_TITLE_ONLY_BENCH_READY" or not tr.get("title_bench_render_allowed"):
        raise SystemExit("typography title bench was not open")

    recorded = now_iso()
    old_blob = git_blob("continuity/vpd/CURRENT_TASK_LOCK.json")

    evidence = {
        "schema_version": "vpd-p1-typography-title-bench-execution/v1",
        "recorded_at": recorded,
        "status": "EXECUTED_WAITING_HUMAN_BLIND_VERDICT",
        "scope": "P1_T1_TITLE_ONLY_STRONG_BASELINE_VS_DISTILLED",
        "bench_plan": tr["bench_plan"],
        "figma": {
            "file_key": "uyDxOoN1iNDPpEHTKSUWg1",
            "page_id": "53:2",
            "page_name": "P1 Typography Repair Bench T1",
            "canvas": [1600, 900],
            "frames": {
                "T1_DOUFANG_A_STRONG_BASELINE": "53:3",
                "T1_CHAZUO_A_STRONG_BASELINE": "53:10",
                "T1_DOUFANG_B_DISTILLED": "53:17",
                "T1_CHAZUO_B_DISTILLED": "53:33"
            }
        },
        "execution_budget": {
            "primary_build_completed": {"豆坊": True, "茶作": True},
            "distilled_aesthetic_correction_passes_used": {"豆坊": 1, "茶作": 1},
            "additional_aesthetic_corrections_authorized": False,
            "technical_invalid_retries": 0
        },
        "first_b_readback": {
            "classification": "AESTHETIC_FAILURE_NOT_TECHNICAL",
            "doufang": "overbuilt with added beams; still read as modified-font mechanics rather than mature lettering",
            "chazuo": "mechanically deconstructed and visually congested; did not beat the strong baseline",
            "action": "consume the single predeclared B correction pass for each title"
        },
        "corrected_b_readback": {
            "completed": True,
            "note": "Second B pixels are frozen for human blind review. No assistant pass/fail is substituted for the human title gate."
        },
        "drive_blind_review": {
            "folder_id": "1TaQJeK5BGskE7gVXUL5yEfEDVNSSvCG9",
            "folder_name": "视觉审美操作系统_P1_文字T1盲评_20260914",
            "presentation_id": "1vdviPhYzHyOP4BDiOZzsMGBMHSLbQfRosHal7PSiYsc",
            "presentation_name": "T1_豆坊茶作_纯文字盲评_20260914",
            "slides": [
                {"slide": 1, "title": "豆坊｜纯文字盲评", "labels": ["Candidate 1", "Candidate 2"]},
                {"slide": 2, "title": "茶作｜纯文字盲评", "labels": ["Candidate 1", "Candidate 2"]}
            ],
            "google_import_readback_confirmed": True
        },
        "blind_order": {
            "mapping_revealed": False,
            "mapping_committed_to_public_repo": False,
            "pre_verdict_commitment_sha256": "e5fdde8d13c03c8e319b28b7d36cabd4d618abbc8ddc478de717c375a5511ac0",
            "commitment_note": "The A/B mapping and nonce are intentionally withheld until after the user's blind verdict."
        },
        "human_blind_verdict": None,
        "next_required_action": "P1_WAIT_HUMAN_TITLE_BENCH_VERDICT"
    }
    dump(EVID, evidence)
    evid_ref = ref(EVID)

    lock["revision"] = 36
    lock["preserved_prior_revision"] = {
        "revision": 35,
        "git_blob_sha": old_blob,
        "note": "Revision 35 prepared and froze the T1 typography-only bench before pixel execution."
    }
    lock["current_stage"] = (
        "P1 T1 standalone-title A/B execution is complete for 豆坊 and 茶作. "
        "Both distilled B titles consumed their single allowed aesthetic correction after the first B readback failed aesthetically. "
        "The corrected four candidates are now frozen in a Drive blind-review deck; A/B mapping remains unrevealed. "
        "The only next action is the user's blind title verdict."
    )
    lock["status"] = "VPD_P1_TYPOGRAPHY_TITLE_BENCH_WAITING_HUMAN_BLIND_VERDICT"
    lock["next_required_action"] = "P1_WAIT_HUMAN_TITLE_BENCH_VERDICT"
    lock["completed_this_revision"] = [
        "created the isolated Figma T1 page and four 1600x900 standalone title frames",
        "built strong ordinary baselines for 豆坊 and 茶作",
        "built distilled B wordmarks and classified the first B readback as aesthetic failure rather than technical failure",
        "consumed exactly one authorized B aesthetic correction pass for 豆坊 and one for 茶作",
        "froze corrected candidates with no photography, support copy, texture, shadow or poster reintegration",
        "created and read back a two-slide Google Drive blind-review deck with Candidate 1 / Candidate 2 labels",
        "committed only a pre-verdict order hash; A/B mapping remains withheld"
    ]
    lock["updated_at"] = recorded
    lock["blockers"] = [
        "T1 pixels are frozen; no further title aesthetic correction is authorized before the human blind verdict.",
        "Candidate mapping must remain unrevealed until the human blind verdict is recorded.",
        "T2 support typography and P6 poster reintegration remain blocked until the T1 title gate settles.",
        "Candidate promotion, second-family completion, Golden and Scale remain blocked."
    ]
    tr = lock["typography_repair"]
    tr["status"] = "T1_EXECUTED_WAITING_HUMAN_BLIND_VERDICT"
    tr["phase"] = "T1_TITLE_ONLY"
    tr["title_bench_render_allowed"] = False
    tr["poster_reintegration_allowed"] = False
    tr["support_typography_bench_allowed"] = False
    tr["correction_passes_used"] = {"豆坊": 1, "茶作": 1}
    tr["human_blind_verdict"] = None
    tr["blind_order_mapping_revealed"] = False
    tr["blind_order_commitment_sha256"] = evidence["blind_order"]["pre_verdict_commitment_sha256"]
    tr["execution_evidence"] = evid_ref
    tr["drive_blind_review"] = {
        "folder_id": evidence["drive_blind_review"]["folder_id"],
        "presentation_id": evidence["drive_blind_review"]["presentation_id"]
    }
    tr["next_required_action"] = lock["next_required_action"]
    dump(LOCK, lock)
    lock_sha = sha_file(LOCK)

    previous = None
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        obj = json.loads(line)
        previous = {"event_id": obj["event_id"], "event_hash": obj["event_hash"]}
    event = {
        "schema_version": "upcp-state-ledger-event/v1",
        "stream_id": "commercial_design_pipeline",
        "event_id": "EVT-VPD-P1-T1-TITLE-BENCH-EXECUTED-20260914-001",
        "event_type": "P1_TYPOGRAPHY_TITLE_BENCH_EXECUTED_WAITING_HUMAN_BLIND_VERDICT",
        "task_id": "VPD-SYSTEM-LEVEL-HOLDOUT-TRANSFER-VALIDATION-V1",
        "project_id": "visual-aesthetic-vpd",
        "recorded_at": recorded,
        "material": True,
        "previous_event_id": previous["event_id"] if previous else None,
        "previous_event_hash": previous["event_hash"] if previous else None,
        "lock_sha256": lock_sha,
        "authorization": {"source": "current controlling ChatGPT conversation", "instruction": "下一步", "scope": "execute frozen T1 typography-only title bench and prepare blind human review"},
        "before": {"state": "P1_TYPOGRAPHY_REPAIR_BENCH_READY", "next_action": "P1_EXECUTE_TYPOGRAPHY_ONLY_TITLE_BENCH"},
        "after": {"state": lock["status"], "next_action": lock["next_required_action"], "mapping_revealed": False},
        "evidence": [evid_ref["path"], tr["bench_plan"]["path"], lock["human_set_verdict_evidence"]["path"]],
        "reason": "The predeclared T1 title-only A/B bench was executed. Each B arm used its single aesthetic correction after a genuine taste failure. Corrected candidates are frozen and presented blind in Drive; human verdict is required before any T2 or poster reintegration.",
        "remote_authority": {"repository": "vubaoha034-hash/shenmei", "branch": "visual-program-distillation-v2-photography-design-20260814"}
    }
    event["event_hash"] = event_hash(event)
    with LEDGER.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(event, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")

    cp["sequence"] = int(cp["sequence"]) + 1
    cp["recorded_at"] = recorded
    cp["current_focus"] = lock["current_stage"]
    if "p1_typography_title_only_ab_execution" not in cp["completed"]:
        cp["completed"].append("p1_typography_title_only_ab_execution")
    cp["incomplete"] = [
        "p1_typography_title_blind_human_verdict",
        "p1_typography_support_hierarchy_bench",
        "p6_reintegration_after_typography_repair",
        "candidate_promotion",
        "second_style_family_validation",
        "golden",
        "scale"
    ]
    cp["blocked"] = lock["blockers"]
    cp["next_required_action"] = lock["next_required_action"]
    cp["status"] = lock["status"]
    cp["task_lock"] = {"path": "continuity/vpd/CURRENT_TASK_LOCK.json", "sha256": lock_sha}
    cp["typography_repair"] = {
        "status": tr["status"],
        "phase": tr["phase"],
        "bench_plan": tr["bench_plan"],
        "title_tasks": ["豆坊", "茶作"],
        "title_bench_render_allowed": False,
        "correction_passes_used": dict(tr["correction_passes_used"]),
        "human_blind_verdict": None,
        "blind_order_mapping_revealed": False,
        "blind_order_commitment_sha256": tr["blind_order_commitment_sha256"],
        "execution_evidence": evid_ref,
        "drive_blind_review": dict(tr["drive_blind_review"]),
        "poster_reintegration_allowed": False
    }
    cp["ledger_tails"] = {"commercial_design_pipeline": {"event_id": event["event_id"], "event_hash": event["event_hash"]}}
    dump(CP, cp)

    adapter["vpd_system_goal_authority"]["checkpoint"] = lock["status"]
    adapter["vpd_system_goal_authority"]["next_required_action"] = lock["next_required_action"]
    adapter["vpd_system_goal_authority"]["render_allowed"] = False
    adapter["task_lock"]["revision"] = 36
    adapter["task_lock"]["sha256"] = lock_sha
    adapter["forward_commercial_pipeline"]["status"] = "PAUSED_FOR_P1_TYPOGRAPHY_TITLE_BLIND_VERDICT"
    adapter["forward_commercial_pipeline"]["next_required_action"] = lock["next_required_action"]
    adapter["change_authorities"].insert(0, {**evid_ref, "priority": 0, "purpose": "Executed T1 title-only A/B bench with frozen correction budget and Drive blind-review commitment; no human verdict yet."})
    dump(ADAPTER, adapter)

    print(json.dumps({
        "status": "P1_T1_TITLE_BENCH_RECORDED",
        "lock_revision": 36,
        "checkpoint_sequence": cp["sequence"],
        "next_required_action": lock["next_required_action"],
        "execution_evidence": evid_ref,
        "lock_sha256": lock_sha,
        "ledger_event_id": event["event_id"],
        "ledger_event_hash": event["event_hash"]
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
