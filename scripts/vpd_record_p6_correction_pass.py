#!/usr/bin/env python3
"""Record the one authorized P6 equal-budget composition correction pass.

This script records the already-executed Figma edits and advances state to final
pixel/editability validation. It does not modify Figma and does not claim any
commercial/aesthetic pass.
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
EVID = ROOT / "evidence/vpd/p6_equal_budget_integrated_design_v1/P6_SINGLE_CORRECTION_PASS_EXECUTION_20260914.json"


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
    if lock.get("revision") != 31 or lock.get("state_profile") != "p6-composition/v1":
        raise SystemExit("unexpected source state; correction record is revision-31-only")
    if lock.get("next_required_action") != "P6_APPLY_SINGLE_CORRECTION_PASS_ALL_POSTERS":
        raise SystemExit("unexpected source action")
    used = lock["p6_integrated_design"].get("correction_passes_used", {})
    if set(used.values()) != {0}:
        raise SystemExit("correction budget was already consumed")

    recorded = now_iso()
    old_blob = git_blob("continuity/vpd/CURRENT_TASK_LOCK.json")

    evidence = {
        "schema_version": "vpd-p6-single-correction-pass-execution/v1",
        "recorded_at": recorded,
        "status": "CORRECTION_EXECUTED_NOT_YET_FINAL_ACCEPTED",
        "scope": "P6_EQUAL_BUDGET_SINGLE_CORRECTION_PASS_ALL_FOUR",
        "figma_file_key": "uyDxOoN1iNDPpEHTKSUWg1",
        "page_id": "12:2",
        "frame_size": [2400, 3200],
        "user_authorization": "Current controlling chat: user instructed to continue the next project step.",
        "budget": {
            "composition_pass_per_poster": 1,
            "correction_pass_max_per_poster": 1,
            "B_extra_manual_budget": False,
            "correction_passes_consumed": {"12:3": 1, "12:11": 1, "12:19": 1, "12:27": 1}
        },
        "write_method": "Figma Plugin API through use_figma; all four posters corrected in one controlled write call",
        "fonts_loaded": ["Noto Sans SC Black", "Noto Sans SC Medium", "Inter Medium"],
        "color": {"title_and_support_rgb_normalized": [0.965, 0.949, 0.902]},
        "frames": [
            {
                "frame_id": "12:3",
                "role": "DOUFANG_A_BASELINE",
                "photo_node": "12:4",
                "photo_geometry_after": [0, 0, 2400, 3200],
                "photo_modified": False,
                "old_title_node_removed": "12:7",
                "new_editable_title_vectors": ["51:4", "51:7"],
                "title_copy": "豆坊",
                "title_block": {"x": 150, "y": 250, "width": 977.8464050292969, "height": 470},
                "title_strategy": "A-arm restrained optical correction only: clean two-glyph vectorization, no added structural cuts; 豆 mildly broader, 坊 mildly narrower.",
                "support": {
                    "en": {"node": "12:8", "copy": "HANDMADE TOFU", "x": 158, "y": 775, "font_size": 58, "tracking_percent": 7},
                    "cn": {"node": "12:9", "copy": "手作豆腐 · 当日现制", "x": 158, "y": 866, "font_size": 52, "tracking_percent": 4},
                    "hairline": {"node": "12:10", "x": 158, "y": 957, "width": 190, "height": 3}
                },
                "pixel_readback": {"reviewed": True, "rendered_dimensions": [1200, 1600], "natural_dimensions": [2400, 3200], "technical_error": False}
            },
            {
                "frame_id": "12:11",
                "role": "DOUFANG_B_DISTILLED",
                "photo_node": "12:12",
                "photo_geometry_after": [0, 0, 2400, 3200],
                "photo_modified": False,
                "old_title_node_removed": "12:15",
                "new_editable_title_vectors": ["51:10", "51:13"],
                "title_copy": "豆坊",
                "title_block": {"x": 1035, "y": 225, "width": 1088.9970397949219, "height": 520},
                "title_strategy": "B-arm authored planar counter-mass: 豆 broader and more horizontal, 坊 taller/heavier at right, with asymmetric optical weighting aligned to press/mill process mass.",
                "support": {
                    "en": {"node": "12:16", "copy": "HANDMADE TOFU", "x": 1045, "y": 790, "font_size": 58, "tracking_percent": 7},
                    "cn": {"node": "12:17", "copy": "手作豆腐 · 当日现制", "x": 1045, "y": 882, "font_size": 52, "tracking_percent": 4},
                    "hairline": {"node": "12:18", "x": 1045, "y": 974, "width": 210, "height": 3}
                },
                "pixel_readback": {"reviewed": True, "rendered_dimensions": [1200, 1600], "natural_dimensions": [2400, 3200], "technical_error": False}
            },
            {
                "frame_id": "12:19",
                "role": "CHAZUO_A_BASELINE",
                "photo_node": "12:20",
                "photo_geometry_after": [0, 0, 2400, 3200],
                "photo_modified": False,
                "old_title_node_removed": "12:23",
                "new_editable_title_vectors": ["51:16", "51:19"],
                "title_copy": "茶作",
                "title_block": {"x": 138, "y": 205, "width": 899.7398986816406, "height": 445},
                "title_strategy": "A-arm open reference-led lockup: smaller mass, more breathing room, restrained optical editing and no added structural cut motif.",
                "support": {
                    "en": {"node": "12:24", "copy": "HANDCRAFTED TEA", "x": 145, "y": 705, "font_size": 56, "tracking_percent": 9},
                    "cn": {"node": "12:25", "copy": "鲜叶入作 · 手工成茶", "x": 145, "y": 792, "font_size": 50, "tracking_percent": 5},
                    "hairline": {"node": "12:26", "x": 145, "y": 884, "width": 160, "height": 3}
                },
                "pixel_readback": {"reviewed": True, "rendered_dimensions": [1200, 1600], "natural_dimensions": [2400, 3200], "technical_error": False}
            },
            {
                "frame_id": "12:27",
                "role": "CHAZUO_B_DISTILLED",
                "photo_node": "12:28",
                "photo_geometry_after": [0, 0, 2400, 3200],
                "photo_modified": False,
                "old_title_node_removed": "12:31",
                "new_editable_title_vectors": ["51:22", "51:25"],
                "title_copy": "茶作",
                "title_block": {"x": 875, "y": 205, "width": 998.4595336914062, "height": 500},
                "title_strategy": "B-arm tea-specific rhythm: broad 茶 canopy, narrower upright 作 and larger inter-glyph interval aligned to rack/tray directional spacing.",
                "support": {
                    "en": {"node": "12:32", "copy": "HANDCRAFTED TEA", "x": 895, "y": 770, "font_size": 56, "tracking_percent": 9},
                    "cn": {"node": "12:33", "copy": "鲜叶入作 · 手工成茶", "x": 895, "y": 858, "font_size": 50, "tracking_percent": 5},
                    "hairline": {"node": "12:34", "x": 895, "y": 950, "width": 175, "height": 3}
                },
                "pixel_readback": {"reviewed": True, "rendered_dimensions": [1200, 1600], "natural_dimensions": [2400, 3200], "technical_error": False}
            }
        ],
        "copy_check": {
            "DOUFANG": ["豆坊", "HANDMADE TOFU", "手作豆腐 · 当日现制"],
            "CHAZUO": ["茶作", "HANDCRAFTED TEA", "鲜叶入作 · 手工成茶"],
            "unexpected_copy_added": False
        },
        "technical_readback": {
            "all_four_screenshots_returned": True,
            "all_four_natural_dimensions": [2400, 3200],
            "photo_nodes_unchanged_by_write": True,
            "support_copy_exact_after_write": True,
            "second_aesthetic_correction_authorized": False
        },
        "acceptance_boundary": {
            "commercial_pass_claimed": False,
            "typography_gate_claimed": False,
            "photo_type_integration_gate_claimed": False,
            "brand_distinctiveness_gate_claimed": False,
            "final_pixel_gate_claimed": False,
            "human_final_aesthetic_authority_preserved": True,
            "candidate_promotion_allowed": False
        },
        "next_required_action": "P6_VALIDATE_FINAL_PIXELS_EDITABILITY"
    }
    dump(EVID, evidence)
    evid_ref = ref(EVID)

    lock["revision"] = 32
    lock["preserved_prior_revision"] = {
        "revision": 31,
        "git_blob_sha": old_blob,
        "note": "Revision 31 authorized exactly one symmetric correction pass per P6 poster after all four real image bindings were confirmed."
    }
    p6 = lock["p6_integrated_design"]
    p6["status"] = "CORRECTION_PASS_COMPLETE_FINAL_VALIDATION_READY"
    p6["correction_passes_used"] = {"12:3": 1, "12:11": 1, "12:19": 1, "12:27": 1}
    p6["final_pixel_validation_allowed"] = True
    lock["current_stage"] = "The single authorized equal-budget correction pass has been consumed for all four P6 posters with no photo edits and exact copy preserved. Four full-frame pixel readbacks completed without technical error. No commercial/aesthetic gate is claimed yet; final pixel and editability validation is now authorized."
    lock["status"] = "VPD_P6_CORRECTION_COMPLETE_FINAL_VALIDATION_READY"
    lock["next_required_action"] = "P6_VALIDATE_FINAL_PIXELS_EDITABILITY"
    lock["completed_this_revision"] = [
        "consumed exactly one correction pass for each of frames 12:3, 12:11, 12:19 and 12:27 in one symmetric Figma write",
        "replaced the four old single-vector titles with arm-specific editable vector glyph pairs",
        "reduced and repositioned all editable EN/CN support copy and hairlines while preserving exact wording",
        "left formal photo nodes 12:4, 12:12, 12:20 and 12:28 unchanged in geometry and content",
        "completed full-frame post-write pixel readback for all four at natural 2400x3200 canvas",
        "opened final pixel/editability validation without claiming aesthetic or commercial pass"
    ]
    lock["updated_at"] = recorded
    lock["correction_pass_evidence"] = evid_ref
    lock["blockers"] = [
        "Human set verdict remains blocked until final pixel and editability validation is completed.",
        "No second aesthetic correction pass is authorized under the frozen equal-budget comparison.",
        "Candidate promotion, second-family completion, Golden and Scale remain blocked.",
        "Historical system-validation ledger prefix retains its disclosed pre-existing hash defects and is not recertified."
    ]
    dump(LOCK, lock)
    lock_sha = sha_file(LOCK)

    previous = None
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        obj = json.loads(line)
        previous = {"event_id": obj["event_id"], "event_hash": obj["event_hash"]}
    event = {
        "schema_version": "upcp-state-ledger-event/v1",
        "stream_id": "commercial_design_pipeline",
        "event_id": "EVT-VPD-P6-SINGLE-CORRECTION-COMPLETE-20260914-001",
        "event_type": "P6_EQUAL_BUDGET_SINGLE_CORRECTION_PASS_COMPLETE",
        "task_id": "VPD-SYSTEM-LEVEL-HOLDOUT-TRANSFER-VALIDATION-V1",
        "project_id": "visual-aesthetic-vpd",
        "recorded_at": recorded,
        "material": True,
        "previous_event_id": previous["event_id"] if previous else None,
        "previous_event_hash": previous["event_hash"] if previous else None,
        "lock_sha256": lock_sha,
        "authorization": {"source": "current controlling ChatGPT conversation", "instruction": "continue the next project step", "scope": "consume one equal-budget P6 correction pass per poster"},
        "before": {"state": "COMPOSITION_REVIEW_FAIL_CORRECTION_AUTHORIZED", "correction_used_each": 0},
        "after": {"state": "CORRECTION_PASS_COMPLETE_FINAL_VALIDATION_READY", "correction_used_each": 1, "final_pixel_validation_allowed": True},
        "evidence": [evid_ref["path"], lock["composition_review_evidence"]["path"], "contracts/vpd/FIGMA_COMPOSITION_CONTRACT_V1.json", "contracts/vpd/COMMERCIAL_DESIGN_GATE_POLICY_V1.json"],
        "reason": "The predeclared single correction pass was executed symmetrically across all four posters. Photo nodes were not edited, exact copy remained intact, and pixel readback showed no technical failure. The next gate is final pixel/editability validation, not another taste iteration.",
        "remote_authority": {"repository": "vubaoha034-hash/shenmei", "branch": "visual-program-distillation-v2-photography-design-20260814"}
    }
    event["event_hash"] = event_hash(event)
    with LEDGER.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(event, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")

    cp["sequence"] = 54
    cp["recorded_at"] = recorded
    cp["current_focus"] = lock["current_stage"]
    if "p6_single_correction_pass_per_poster" not in cp["completed"]:
        cp["completed"].append("p6_single_correction_pass_per_poster")
    cp["incomplete"] = [
        "p6_final_pixel_and_editability_validation",
        "human_set_verdict",
        "candidate_promotion",
        "second_style_family_validation",
        "golden",
        "scale"
    ]
    cp["blocked"] = lock["blockers"]
    cp["next_required_action"] = lock["next_required_action"]
    cp["p6"]["final_pixel_validation_allowed"] = True
    cp["p6"]["correction_passes_used"] = dict(p6["correction_passes_used"])
    cp["status"] = lock["status"]
    cp["task_lock"] = {"path": "continuity/vpd/CURRENT_TASK_LOCK.json", "sha256": lock_sha}
    cp["requirements"]["p6_integrated_design"]["status"] = "CORRECTION_PASS_COMPLETE_FINAL_VALIDATION_READY"
    cp["ledger_tails"] = {"commercial_design_pipeline": {"event_id": event["event_id"], "event_hash": event["event_hash"]}}
    dump(CP, cp)

    adapter["vpd_system_goal_authority"]["checkpoint"] = lock["status"]
    adapter["vpd_system_goal_authority"]["next_required_action"] = lock["next_required_action"]
    adapter["vpd_system_goal_authority"]["render_allowed"] = False
    adapter["task_lock"]["revision"] = 32
    adapter["task_lock"]["sha256"] = lock_sha
    adapter["forward_commercial_pipeline"]["status"] = "ACTIVE_P6_FINAL_PIXEL_EDITABILITY_VALIDATION"
    adapter["forward_commercial_pipeline"]["next_required_action"] = lock["next_required_action"]
    adapter["change_authorities"].insert(0, {**evid_ref, "priority": 0, "purpose": "Exact execution record for the one authorized equal-budget P6 correction pass; no aesthetic pass claim."})
    dump(ADAPTER, adapter)

    print(json.dumps({
        "status": "P6_CORRECTION_PASS_RECORDED",
        "lock_revision": 32,
        "checkpoint_sequence": 54,
        "next_required_action": lock["next_required_action"],
        "correction_evidence": evid_ref,
        "lock_sha256": lock_sha,
        "ledger_event_id": event["event_id"],
        "ledger_event_hash": event["event_hash"]
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
