#!/usr/bin/env python3
"""Record completed P6 final pixel/editability validation and wait for human set verdict.

This script records already-observed Figma evidence. It does not edit Figma, does
not spend another correction pass, and does not turn assistant aesthetic review
into the required human-final verdict.
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
EVID = ROOT / "evidence/vpd/p6_equal_budget_integrated_design_v1/P6_FINAL_PIXEL_EDITABILITY_VALIDATION_20260914.json"


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
    if lock.get("revision") != 32 or lock.get("state_profile") != "p6-composition/v1":
        raise SystemExit("unexpected source state; final validation record is revision-32-only")
    if lock.get("next_required_action") != "P6_VALIDATE_FINAL_PIXELS_EDITABILITY":
        raise SystemExit("unexpected source action")
    used = lock["p6_integrated_design"].get("correction_passes_used", {})
    if set(used.values()) != {1}:
        raise SystemExit("single correction pass must be consumed for all four posters")

    recorded = now_iso()
    old_blob = git_blob("continuity/vpd/CURRENT_TASK_LOCK.json")

    evidence = {
        "schema_version": "vpd-p6-final-pixel-editability-validation/v1",
        "recorded_at": recorded,
        "status": "FINAL_VALIDATION_COMPLETE_HUMAN_SET_VERDICT_REQUIRED",
        "scope": "P6_EQUAL_BUDGET_FOUR_POSTER_FINAL_PIXEL_AND_EDITABILITY_VALIDATION",
        "figma_file_key": "uyDxOoN1iNDPpEHTKSUWg1",
        "page_id": "12:2",
        "frame_size": [2400, 3200],
        "review_boundary": {
            "assistant_review_is_not_independent_blind": True,
            "human_final_aesthetic_authority_preserved": True,
            "second_correction_pass_authorized": False,
            "commercial_pass_claimed": False,
            "candidate_promotion_allowed": False
        },
        "pixel_review_scales": {
            "thumbnail": [360, 480],
            "normal": [1200, 1600],
            "detail": [2400, 3200]
        },
        "frames": [
            {
                "frame_id": "12:3",
                "role": "DOUFANG_A_BASELINE",
                "photo_node": "12:4",
                "title_vectors": ["51:4", "51:7"],
                "support_text_nodes": ["12:8", "12:9"],
                "hairline_node": "12:10",
                "copy": ["豆坊", "HANDMADE TOFU", "手作豆腐 · 当日现制"],
                "thumbnail_observation": "Primary title remains immediately readable; support copy becomes small and contributes little to thumbnail identity.",
                "detail_observation": "Pixels are clean and the tofu process is credible, but the title still reads primarily as a heavy sans-derived overlay rather than a distinctive authored brand wordmark.",
                "editable_structure": "PASS",
                "export": {"format": "png", "dimensions": [2400, 3200], "reported_size_bytes": 3223603, "sha256": None},
                "safe_margin_check": "PASS"
            },
            {
                "frame_id": "12:11",
                "role": "DOUFANG_B_DISTILLED",
                "photo_node": "12:12",
                "title_vectors": ["51:10", "51:13"],
                "support_text_nodes": ["12:16", "12:17"],
                "hairline_node": "12:18",
                "copy": ["豆坊", "HANDMADE TOFU", "手作豆腐 · 当日现制"],
                "thumbnail_observation": "Process mass is stronger than A, but the large title and small support copy still read as a conventional overlay system.",
                "detail_observation": "The asymmetric title geometry is technically clean, but it competes with the wooden press and does not create a sufficiently unique tofu-specific typographic mechanism.",
                "editable_structure": "PASS",
                "export": {"format": "png", "dimensions": [2400, 3200], "reported_size_bytes": 3549415, "sha256": None},
                "safe_margin_check": "PASS"
            },
            {
                "frame_id": "12:19",
                "role": "CHAZUO_A_BASELINE",
                "photo_node": "12:20",
                "title_vectors": ["51:16", "51:19"],
                "support_text_nodes": ["12:24", "12:25"],
                "hairline_node": "12:26",
                "copy": ["茶作", "HANDCRAFTED TEA", "鲜叶入作 · 手工成茶"],
                "thumbnail_observation": "Title is readable, but the support layer is near the threshold of useful thumbnail legibility and the whole lockup reads as photo plus title.",
                "detail_observation": "Tea materials and depth are credible; the title remains generic in construction and the title x=138 is 6 px inside the frozen 6% minimum margin without a logged intentional crop.",
                "editable_structure": "PASS",
                "export": {"format": "png", "dimensions": [2400, 3200], "reported_size_bytes": 3566858, "sha256": None},
                "safe_margin_check": "MINOR_FAIL_X138_LT_144"
            },
            {
                "frame_id": "12:27",
                "role": "CHAZUO_B_DISTILLED",
                "photo_node": "12:28",
                "title_vectors": ["51:22", "51:25"],
                "support_text_nodes": ["12:32", "12:33"],
                "hairline_node": "12:34",
                "copy": ["茶作", "HANDCRAFTED TEA", "鲜叶入作 · 手工成茶"],
                "thumbnail_observation": "The B photograph gives a stronger quiet upper field, but the typography still dominates as a generic cream headline and the support copy collapses at small scale.",
                "detail_observation": "The broad-茶/narrow-作 rhythm is clean but not sufficiently brand-specific; the graphic system can still be swapped with the tofu title/copy with little structural consequence.",
                "editable_structure": "PASS",
                "export": {"format": "png", "dimensions": [2400, 3200], "reported_size_bytes": 3650285, "sha256": None},
                "safe_margin_check": "PASS"
            }
        ],
        "machine_checks": {
            "all_four_full_resolution_renders_returned": True,
            "all_four_thumbnail_renders_returned": True,
            "normal_scale_readback_preserved_from_correction_receipt": True,
            "all_four_photo_nodes_present": True,
            "all_four_primary_titles_are_editable_vectors": True,
            "all_eight_support_copy_nodes_are_editable_text": True,
            "exact_copy_preserved": True,
            "all_four_framed_exports_report_png_2400x3200": True,
            "export_urls_not_committed": True,
            "final_export_sha256_chain": "INCOMPLETE_CURRENT_RUNTIME_COULD_NOT_MATERIALIZE_SHORT_LIVED_FIGMA_URLS"
        },
        "six_gate_validation": {
            "PHOTO_QUALITY_GATE": {
                "machine_evidence": "PASS_PROCESS_CONTENT_AND_PIXEL_INTEGRITY",
                "assistant_pre_review": "PASS_WITH_RESERVATIONS",
                "human_final_required": True,
                "reason": "Materials, process evidence, depth and lighting are credible enough for evaluation; absolute photography taste remains human authority."
            },
            "TYPOGRAPHY_DESIGN_GATE": {
                "machine_evidence": "EDITABLE_VECTOR_AND_COPY_PASS",
                "assistant_pre_review": "FAIL_RECOMMENDED",
                "human_final_required": True,
                "reason": "The corrected titles remain visibly close to heavy sans skeletons; A/B differences are mainly width, height and placement rather than a mature, category-specific authored wordmark system."
            },
            "PHOTO_TYPE_INTEGRATION_GATE": {
                "machine_evidence": "NO_DETACHED_PANEL_AND_SCENE_SPACE_USED",
                "assistant_pre_review": "FAIL_RECOMMENDED",
                "human_final_required": True,
                "reason": "The relationship is still mostly quiet-zone overlay. In the distilled tofu arm the title competes with press geometry; in both tea arms typography floats above the process field rather than becoming structurally integrated with it."
            },
            "BRAND_DISTINCTIVENESS_GATE": {
                "machine_evidence": "SWAP_TEST_NOT_PROVEN",
                "assistant_pre_review": "FAIL_RECOMMENDED",
                "human_final_required": True,
                "reason": "Both content families retain the same cream headline, stacked English/Chinese support and hairline grammar. Swapping brand names and support copy would leave the template largely interchangeable."
            },
            "EDITABLE_DESIGN_PROVENANCE_GATE": {
                "machine_evidence": "EDITABLE_NODE_STRUCTURE_PASS_FORMAL_EXPORT_HASH_CHAIN_INCOMPLETE",
                "assistant_pre_review": "FORMAL_PASS_NOT_AVAILABLE",
                "human_final_required": False,
                "reason": "Figma frame/photo/vector/text identities are auditable, but the required photo-to-Figma-to-final-export SHA-256 chain is incomplete because final export bytes could not be materialized in this runtime."
            },
            "FINAL_PIXEL_QUALITY_GATE": {
                "machine_evidence": "CLEAN_RENDER_NO_CLIPPING_OR_GLYPH_ERROR",
                "assistant_pre_review": "FAIL_RECOMMENDED",
                "human_final_required": True,
                "reason": "At thumbnail scale support copy loses practical value and the set still reads closer to high-quality photography with large overlay type than to a resolved commercial campaign identity."
            }
        },
        "equal_budget_integrated_comparison": {
            "doufang": "B has stronger process density and counter-mass in the photograph, but no clear integrated commercial-design win after the same Figma budget.",
            "chazuo": "B has a stronger quiet field and spatial direction, but no clear integrated commercial-design win because typography and brand distinctiveness remain unresolved.",
            "set_level": "NO_CLEAR_INTEGRATED_COMMERCIAL_BENEFIT_PROVEN_AFTER_EQUAL_BUDGET_FIGMA",
            "photo_only_mechanism_evidence_preserved": "PASS_REPEATED_DIRECTIONAL_EVIDENCE_ONLY_MEAN_DELTA_0_6"
        },
        "assistant_set_recommendation": "FAIL_HOLD_NOT_COMMERCIAL_READY",
        "formal_human_set_verdict": None,
        "next_required_action": "P6_WAIT_HUMAN_SET_VERDICT"
    }
    dump(EVID, evidence)
    evid_ref = ref(EVID)

    lock["revision"] = 33
    lock["preserved_prior_revision"] = {
        "revision": 32,
        "git_blob_sha": old_blob,
        "note": "Revision 32 completed the one allowed correction pass and opened final pixel/editability validation without claiming commercial acceptance."
    }
    p6 = lock["p6_integrated_design"]
    p6["status"] = "FINAL_VALIDATION_COMPLETE_HUMAN_VERDICT_REQUIRED"
    p6["final_pixel_validation_allowed"] = False
    p6["final_pixel_validation_completed"] = True
    p6["assistant_set_recommendation"] = "FAIL_HOLD_NOT_COMMERCIAL_READY"
    p6["formal_human_set_verdict"] = None
    lock["current_stage"] = "P6 final pixel/editability validation is complete. Editable vector/text structure and clean full-resolution rendering are verified, but the formal export hash chain is incomplete and assistant pre-review recommends FAIL/HOLD on typography, photo-type integration, brand distinctiveness and final commercial pixel quality. Human set verdict is now the only next action; no second correction pass is authorized."
    lock["status"] = "VPD_P6_FINAL_VALIDATION_COMPLETE_HUMAN_VERDICT_REQUIRED"
    lock["next_required_action"] = "P6_WAIT_HUMAN_SET_VERDICT"
    lock["completed_this_revision"] = [
        "verified four 360x480 thumbnail renders, preserved four 1200x1600 normal readbacks, and verified four 2400x3200 detail renders",
        "verified all four primary titles remain editable two-vector glyph constructions and all support copy remains editable text",
        "verified exact copy and photo-node identities remain present with no clipping or technical glyph failure",
        "recorded four formal PNG export identities by frame/dimensions/reported byte size without committing short-lived URLs",
        "recorded formal export SHA-256 chain as incomplete because this runtime could not materialize short-lived Figma export URLs",
        "completed non-blind assistant commercial pre-review with FAIL/HOLD recommendation while preserving human final authority"
    ]
    lock["updated_at"] = recorded
    lock["final_validation_evidence"] = evid_ref
    lock["blockers"] = [
        "Human set verdict is required before any P6 aesthetic/commercial acceptance or rejection is final.",
        "No second aesthetic correction pass is authorized under the frozen equal-budget comparison.",
        "Formal commercial provenance pass is unavailable until a durable final-export SHA-256 chain exists.",
        "Candidate promotion, second-family completion, Golden and Scale remain blocked."
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
        "event_id": "EVT-VPD-P6-FINAL-VALIDATION-COMPLETE-20260914-001",
        "event_type": "P6_FINAL_PIXEL_EDITABILITY_VALIDATION_COMPLETE",
        "task_id": "VPD-SYSTEM-LEVEL-HOLDOUT-TRANSFER-VALIDATION-V1",
        "project_id": "visual-aesthetic-vpd",
        "recorded_at": recorded,
        "material": True,
        "previous_event_id": previous["event_id"] if previous else None,
        "previous_event_hash": previous["event_hash"] if previous else None,
        "lock_sha256": lock_sha,
        "authorization": {"source": "current controlling ChatGPT conversation", "instruction": "continue", "scope": "execute P6 final pixel and editability validation only"},
        "before": {"state": "CORRECTION_PASS_COMPLETE_FINAL_VALIDATION_READY", "next": "P6_VALIDATE_FINAL_PIXELS_EDITABILITY"},
        "after": {"state": "FINAL_VALIDATION_COMPLETE_HUMAN_VERDICT_REQUIRED", "next": "P6_WAIT_HUMAN_SET_VERDICT", "assistant_recommendation": "FAIL_HOLD_NOT_COMMERCIAL_READY"},
        "evidence": [evid_ref["path"], lock["correction_pass_evidence"]["path"], "contracts/vpd/FIGMA_COMPOSITION_CONTRACT_V1.json", "contracts/vpd/COMMERCIAL_DESIGN_GATE_POLICY_V1.json"],
        "reason": "Final multi-scale pixels and editable Figma structure were reviewed without further design mutation. Machine editability/render checks pass, formal export hash provenance remains incomplete, and the non-blind assistant pre-review recommends FAIL/HOLD. Human final set authority is preserved.",
        "remote_authority": {"repository": "vubaoha034-hash/shenmei", "branch": "visual-program-distillation-v2-photography-design-20260814"}
    }
    event["event_hash"] = event_hash(event)
    with LEDGER.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(event, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")

    cp["sequence"] = 55
    cp["recorded_at"] = recorded
    cp["current_focus"] = lock["current_stage"]
    if "p6_final_pixel_and_editability_validation" not in cp["completed"]:
        cp["completed"].append("p6_final_pixel_and_editability_validation")
    cp["incomplete"] = [
        "human_set_verdict",
        "candidate_promotion",
        "second_style_family_validation",
        "golden",
        "scale"
    ]
    cp["blocked"] = lock["blockers"]
    cp["next_required_action"] = lock["next_required_action"]
    cp["p6"]["final_pixel_validation_allowed"] = False
    cp["p6"]["final_pixel_validation_completed"] = True
    cp["p6"]["assistant_set_recommendation"] = "FAIL_HOLD_NOT_COMMERCIAL_READY"
    cp["status"] = lock["status"]
    cp["task_lock"] = {"path": "continuity/vpd/CURRENT_TASK_LOCK.json", "sha256": lock_sha}
    cp["requirements"]["p6_integrated_design"]["status"] = "FINAL_VALIDATION_COMPLETE_HUMAN_VERDICT_REQUIRED"
    cp["ledger_tails"] = {"commercial_design_pipeline": {"event_id": event["event_id"], "event_hash": event["event_hash"]}}
    dump(CP, cp)

    adapter["vpd_system_goal_authority"]["checkpoint"] = lock["status"]
    adapter["vpd_system_goal_authority"]["next_required_action"] = lock["next_required_action"]
    adapter["vpd_system_goal_authority"]["render_allowed"] = False
    adapter["task_lock"]["revision"] = 33
    adapter["task_lock"]["sha256"] = lock_sha
    adapter["forward_commercial_pipeline"]["status"] = "P6_FINAL_VALIDATION_COMPLETE_WAITING_HUMAN_SET_VERDICT"
    adapter["forward_commercial_pipeline"]["next_required_action"] = lock["next_required_action"]
    adapter["change_authorities"].insert(0, {**evid_ref, "priority": 0, "purpose": "P6 final multi-scale pixel and editability validation; assistant FAIL/HOLD recommendation with human-final authority preserved."})
    dump(ADAPTER, adapter)

    print(json.dumps({
        "status": "P6_FINAL_VALIDATION_RECORDED",
        "lock_revision": 33,
        "checkpoint_sequence": 55,
        "next_required_action": lock["next_required_action"],
        "assistant_set_recommendation": "FAIL_HOLD_NOT_COMMERCIAL_READY",
        "final_validation_evidence": evid_ref,
        "lock_sha256": lock_sha,
        "ledger_event_id": event["event_id"],
        "ledger_event_hash": event["event_hash"]
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
