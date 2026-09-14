#!/usr/bin/env python3
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
PLAN = ROOT / "evidence/vpd/p1_typography_repair_v2/WORDMARK_SYSTEM_REPAIR_V2_PLAN.json"
EVID = ROOT / "evidence/vpd/p1_typography_repair_v2/T1_TECHNICAL_RETRY_HUMAN_FINAL_SETTLEMENT_20260914.json"
VALIDATOR = ROOT / "visual_memory/vpd_p6_composition_state.py"


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


def event_hash(obj):
    raw = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def patch_validator():
    text = VALIDATOR.read_text(encoding="utf-8")
    if '"P1_EXECUTE_WORDMARK_SYSTEM_REPAIR_V2",' not in text:
        needle = '    "P1_WAIT_HUMAN_TITLE_TECHNICAL_RETRY_VERDICT",\n}'
        if needle not in text:
            raise SystemExit("validator ACTIONS insertion point missing")
        text = text.replace(
            needle,
            '    "P1_WAIT_HUMAN_TITLE_TECHNICAL_RETRY_VERDICT",\n    "P1_EXECUTE_WORDMARK_SYSTEM_REPAIR_V2",\n}'
        )
    if 'elif action == "P1_EXECUTE_WORDMARK_SYSTEM_REPAIR_V2":' not in text:
        needle = '    require(not set(cp["completed"]) & set(cp["incomplete"]), "COMPLETED_AND_INCOMPLETE")'
        if needle not in text:
            raise SystemExit("validator branch insertion point missing")
        branch = '''    elif action == "P1_EXECUTE_WORDMARK_SYSTEM_REPAIR_V2":
        tr = lock["typography_repair"]
        require(tr["status"] == "T1_FAILED_CURRENT_COMPILER_STOPPED_WORDMARK_V2_READY", "WORDMARK_V2_STATE")
        require(tr["wordmark_v2_render_allowed"] is True, "WORDMARK_V2_RENDER_NOT_OPEN")
        require(tr["support_typography_bench_allowed"] is False and tr["poster_reintegration_allowed"] is False, "WORDMARK_V2_BOUNDARY")
        require(tr["technical_retry_budget_remaining"] == 0, "OLD_T1_RETRY_REOPENED")
        for name in ("bench_plan", "execution_evidence", "human_verdict_evidence", "technical_retry_receipt", "final_t1_settlement", "wordmark_v2_plan"):
            check_ref(root, tr[name])
        settlement = read(root, tr["final_t1_settlement"]["path"])
        require(settlement["formal_verdict"] == "FAIL_CURRENT_TYPOGRAPHY_COMPILER_WORDMARK_COHERENCE", "WORDMARK_V2_SETTLEMENT")
        require(settlement["T2_allowed"] is False and settlement["P6_reintegration_allowed"] is False, "WORDMARK_V2_PREMATURE_ADVANCE")
        require(settlement["preservation_lock"]["photo_bases"] is True and settlement["preservation_lock"]["overall_visual_direction"] is True, "WORDMARK_V2_PRESERVATION_LOST")

'''
        text = text.replace(needle, branch + needle)
    VALIDATOR.write_text(text, encoding="utf-8")


def main():
    lock = load(LOCK)
    cp = load(CP)
    adapter = load(ADAPTER)

    if lock.get("revision") != 37:
        raise SystemExit("unexpected source revision")
    if lock.get("next_required_action") != "P1_WAIT_HUMAN_TITLE_TECHNICAL_RETRY_VERDICT":
        raise SystemExit("unexpected source action")
    tr = lock["typography_repair"]
    if tr.get("technical_retry_budget_remaining") != 0:
        raise SystemExit("technical retry budget expected exhausted")
    if not PLAN.exists():
        raise SystemExit("wordmark V2 plan missing")

    recorded = now_iso()
    old_blob = git_blob("continuity/vpd/CURRENT_TASK_LOCK.json")
    plan_ref = ref(PLAN)

    evidence = {
        "schema_version": "vpd-t1-technical-retry-human-final-settlement/v1",
        "recorded_at": recorded,
        "status": "HUMAN_FINAL_FAIL_CURRENT_TYPOGRAPHY_COMPILER",
        "scope": "P1_T1_TITLE_ONLY_TECHNICAL_RETRY",
        "human_authority": "CURRENT_USER",
        "human_feedback": [
            "完全两种风格凑一起。这次修复算很失败。",
            "这个设计感有限，跟山野集的图片差了很多。前面明明做出了还好看的参考设计，现在反倒越来越差。",
            "图片现在比以前好了一些，这是肯定的，但是远远没有到完成的地步。文字确实不行。",
            "局部意见不能自动扩大成整套否定；已经变好的部分必须保留，失败层单独修。"
        ],
        "formal_verdict": "FAIL_CURRENT_TYPOGRAPHY_COMPILER_WORDMARK_COHERENCE",
        "diagnosis": {
            "design_sense_gain_preserved": True,
            "glyph_correctness_after_retry": "IMPROVED_BUT_NOT_SUFFICIENT_FOR_PASS",
            "wordmark_system_coherence": "FAIL",
            "mother_reference_gap": "LARGE",
            "root_cause": "The current execution method designs or repairs glyphs locally and assembles them afterward. It does not first establish one shared wordmark grammar, so paired characters drift into different visual languages.",
            "not_a_total_project_reset": True
        },
        "preservation_lock": {
            "photo_bases": True,
            "photo_directional_evidence": True,
            "overall_visual_direction": True,
            "current_image_improvement": True,
            "candidate1_strong_baselines": True,
            "failed_t1_outputs_as_negative_evidence": True,
            "p6_failed_posters_as_negative_evidence": True
        },
        "closed_work": {
            "current_typography_compiler": "STOPPED",
            "old_T1_additional_retry_allowed": False,
            "technical_retry_budget_remaining": 0
        },
        "next_experiment": {
            "id": "WORDMARK_SYSTEM_REPAIR_V2",
            "plan": plan_ref,
            "method": "WORDMARK_FIRST_THEN_GLYPH_DETAIL",
            "reset_scope": "TYPOGRAPHY_LAYER_ONLY",
            "photo_regeneration": False,
            "overall_visual_direction_reset": False
        },
        "T2_allowed": False,
        "P6_reintegration_allowed": False,
        "candidate_promotion_allowed": False,
        "next_required_action": "P1_EXECUTE_WORDMARK_SYSTEM_REPAIR_V2"
    }
    dump(EVID, evidence)
    evid_ref = ref(EVID)

    lock["revision"] = 38
    lock["preserved_prior_revision"] = {
        "revision": 37,
        "git_blob_sha": old_blob,
        "note": "Revision 37 froze the one technical correctness retry and awaited human re-review."
    }
    lock["current_stage"] = (
        "T1 technical retry is human-rejected: readability improved but wordmark coherence failed and the result remains far below the approved mother reference. "
        "The current typography compiler is stopped. Photography, directional photo gains and the improved overall visual direction are explicitly preserved. "
        "Only the typography layer moves forward into the prepared wordmark-first V2 experiment; T2 and P6 reintegration remain blocked."
    )
    lock["status"] = "VPD_P1_T1_FAIL_CURRENT_COMPILER_STOPPED_WORDMARK_V2_READY"
    lock["next_required_action"] = "P1_EXECUTE_WORDMARK_SYSTEM_REPAIR_V2"
    lock["workflow"]["focus_stage"] = "P1"
    lock["completed_this_revision"] = [
        "recorded the user's final human rejection of the T1 technical retry",
        "classified the failure as wordmark-system coherence and insufficient authored quality rather than total-project failure",
        "stopped the current per-glyph typography compiler with no additional retry budget",
        "froze and preserved current photography, directional gains and improved overall visual direction",
        "prepared a wordmark-first V2 typography experiment that changes only the failed typography layer"
    ]
    lock["blockers"] = [
        "The old T1 typography compiler is stopped; no additional technical or aesthetic retry is authorized on the failed Candidate 2 outputs.",
        "T2 support typography remains blocked until wordmark-first V2 passes both 豆坊 and 茶作.",
        "P6 reintegration remains blocked; retained photography must not be regenerated merely because typography failed.",
        "Candidate promotion, Commercial, Golden and Scale remain blocked."
    ]
    lock["typography_repair"] = {
        **tr,
        "status": "T1_FAILED_CURRENT_COMPILER_STOPPED_WORDMARK_V2_READY",
        "phase": "WORDMARK_SYSTEM_REPAIR_V2",
        "title_bench_render_allowed": False,
        "wordmark_v2_render_allowed": True,
        "poster_reintegration_allowed": False,
        "support_typography_bench_allowed": False,
        "technical_retry_budget_remaining": 0,
        "post_retry_human_verdict": {
            "status": "FAIL",
            "reason": "WORDMARK_SYSTEM_COHERENCE_FAIL_AND_DESIGN_QUALITY_STILL_FAR_BELOW_MOTHER_REFERENCE"
        },
        "final_t1_settlement": evid_ref,
        "wordmark_v2_plan": plan_ref,
        "next_required_action": "P1_EXECUTE_WORDMARK_SYSTEM_REPAIR_V2"
    }
    lock["t1_final_settlement_evidence"] = evid_ref
    lock["wordmark_v2_plan"] = plan_ref
    lock["updated_at"] = recorded
    dump(LOCK, lock)
    lock_sha = sha_file(LOCK)

    previous = None
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        obj = json.loads(line)
        previous = {"event_id": obj["event_id"], "event_hash": obj["event_hash"]}
    event = {
        "schema_version": "upcp-state-ledger-event/v1",
        "stream_id": "commercial_design_pipeline",
        "event_id": "EVT-VPD-P1-T1-FINAL-FAIL-WORDMARK-V2-20260914-001",
        "event_type": "T1_TECHNICAL_RETRY_HUMAN_FAIL_CURRENT_COMPILER_STOPPED_WORDMARK_V2_READY",
        "task_id": lock["parent_active_task_id"],
        "project_id": lock["project_id"],
        "recorded_at": recorded,
        "material": True,
        "previous_event_id": previous["event_id"] if previous else None,
        "previous_event_hash": previous["event_hash"] if previous else None,
        "lock_sha256": lock_sha,
        "authorization": {
            "source": "current controlling ChatGPT conversation",
            "authority": "user human re-review",
            "summary": "Technical retry failed as a coherent wordmark; preserve image improvements and repair typography only."
        },
        "before": {
            "state": "T1_TECHNICAL_RETRY_FROZEN_WAITING_HUMAN_REVIEW",
            "next_action": "P1_WAIT_HUMAN_TITLE_TECHNICAL_RETRY_VERDICT"
        },
        "after": {
            "state": lock["status"],
            "next_action": lock["next_required_action"],
            "old_compiler": "STOPPED",
            "wordmark_v2": "READY"
        },
        "evidence": [evid_ref["path"], plan_ref["path"], tr["technical_retry_receipt"]["path"]],
        "reason": "Human re-review rejects the technical retry because paired glyphs form inconsistent design languages and remain far below the approved Shanyeji reference. The user explicitly preserves image improvements and rejects whole-project rollback, so the next bounded experiment changes only the typography mechanism.",
        "remote_authority": {
            "repository": lock["repository"],
            "branch": lock["branch"]
        }
    }
    event["event_hash"] = event_hash(event)
    with LEDGER.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(event, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")

    cp["sequence"] = 60
    cp["recorded_at"] = recorded
    cp["current_focus"] = lock["current_stage"]
    if "p1_t1_technical_retry_human_verdict" not in cp["completed"]:
        cp["completed"].append("p1_t1_technical_retry_human_verdict")
    cp["incomplete"] = [
        "p1_wordmark_system_repair_v2_execution",
        "p1_typography_support_hierarchy_bench",
        "p6_reintegration_after_typography_repair",
        "candidate_promotion",
        "second_style_family_validation",
        "golden",
        "scale"
    ]
    cp["blocked"] = list(lock["blockers"])
    cp["next_required_action"] = lock["next_required_action"]
    cp["status"] = lock["status"]
    cp["task_lock"] = {"path": "continuity/vpd/CURRENT_TASK_LOCK.json", "sha256": lock_sha}
    cp["ledger_tails"] = {
        "commercial_design_pipeline": {
            "event_id": event["event_id"],
            "event_hash": event["event_hash"]
        }
    }
    cp["typography_repair"] = {
        "status": lock["typography_repair"]["status"],
        "phase": "WORDMARK_SYSTEM_REPAIR_V2",
        "wordmark_v2_plan": plan_ref,
        "old_compiler": "STOPPED",
        "T2_allowed": False,
        "P6_reintegration_allowed": False,
        "preserve_photo_bases": True,
        "next_required_action": lock["next_required_action"]
    }
    dump(CP, cp)

    adapter["vpd_system_goal_authority"]["checkpoint"] = lock["status"]
    adapter["vpd_system_goal_authority"]["next_required_action"] = lock["next_required_action"]
    adapter["vpd_system_goal_authority"]["render_allowed"] = False
    adapter["task_lock"]["revision"] = 38
    adapter["task_lock"]["sha256"] = lock_sha
    adapter["forward_commercial_pipeline"]["status"] = "PAUSED_FOR_P1_WORDMARK_SYSTEM_REPAIR_V2"
    adapter["forward_commercial_pipeline"]["next_required_action"] = lock["next_required_action"]
    adapter["change_authorities"].insert(0, {
        **evid_ref,
        "priority": 0,
        "purpose": "Current human T1 final settlement: stop the failed typography compiler, preserve image improvements, and move only typography into wordmark-first V2."
    })
    adapter["change_authorities"].insert(1, {
        **plan_ref,
        "priority": 0,
        "purpose": "Prepared bounded wordmark-first V2 typography experiment; no photo or whole-project reset."
    })
    dump(ADAPTER, adapter)

    patch_validator()

    print(json.dumps({
        "status": lock["status"],
        "lock_revision": 38,
        "checkpoint_sequence": 60,
        "next_required_action": lock["next_required_action"],
        "settlement": evid_ref,
        "wordmark_v2_plan": plan_ref,
        "lock_sha256": lock_sha,
        "ledger_event_id": event["event_id"],
        "ledger_event_hash": event["event_hash"]
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
