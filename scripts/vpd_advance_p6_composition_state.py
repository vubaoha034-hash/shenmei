#!/usr/bin/env python3
"""Advance VPD P6 from relay diagnosis to integrated-composition correction.

This is a one-way state migration. It records the direct Figma readback already
performed in the controlling chat, closes the stale relay-placement blocker,
records the equal-budget round-1 composition review, and opens exactly one
correction pass per poster. It does not edit Figma pixels or claim aesthetic pass.
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
EVID_DIR = ROOT / "evidence/vpd/p6_equal_budget_integrated_design_v1"
TRANSITION = EVID_DIR / "P6_FORMAL_PHOTO_BINDINGS_LATE_READBACK_RESOLUTION_20260914.json"
REVIEW = EVID_DIR / "P6_EQUAL_BUDGET_COMPOSITION_REVIEW_ROUND1_20260914.json"


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


def canonical_event_hash(event_without_hash):
    raw = json.dumps(event_without_hash, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def main():
    lock = load(LOCK)
    cp = load(CP)
    adapter = load(ADAPTER)
    if lock.get("revision") != 30 or lock.get("state_profile") != "p6-figma-relay/v1":
        raise SystemExit("unexpected source state; migration is revision-30-only")
    if lock.get("next_required_action") != "RESOLVE_P6_RELAY_PLACEMENT_MISMATCH_NO_REUPLOAD":
        raise SystemExit("unexpected source action")

    recorded = now_iso()
    old_blob = git_blob("continuity/vpd/CURRENT_TASK_LOCK.json")

    transition = {
        "schema_version": "vpd-p6-formal-photo-bindings-late-readback-resolution/v1",
        "status": "ALL_FOUR_FORMAL_PHOTO_NODES_READBACK_CONFIRMED",
        "recorded_at": recorded,
        "scope": "P6_FIGMA_BINDING_STATE_RESOLUTION_ONLY",
        "user_authorization": "Current controlling chat: user instructed to continue the next project step.",
        "figma": {"file_key": "uyDxOoN1iNDPpEHTKSUWg1", "page_id": "12:2", "frame_size": [2400, 3200]},
        "diagnostic_control": {
            "first_source_url_observation": {
                "result": "NOT_AN_EXACT_ORIGINAL_LARGE_SOURCE_CONTROL",
                "downloaded_format": "jpeg",
                "downloaded_dimensions": [960, 1280],
                "downloaded_bytes": 161623,
                "downloaded_sha256": "8c936f551cc8a15dc5f06d8a696f35d6355346314b5bc146b4620e835dd0abf8",
                "historical_original_sha256": "45943cf0b0d04e11e19694a6b1e04cf6fcf29a9b97832ee93bdf2f08d0c57909"
            },
            "bound_node_full_export_control": {
                "source_node": "12:4",
                "target_scratch_node": "44:3",
                "format": "png",
                "dimensions": [2400, 3200],
                "bytes": 3269051,
                "sha256": "546551a7c8b55840f001ed5e3f42d5b6a79b901e263d4a3acb2f260ff81098d3",
                "http_status": 200,
                "status": "UPLOAD_PASS",
                "returned_imageHash": "1dc2da042e6c47aa9852bb4b451bf3bf7a8b7270",
                "scratch_raw_image_readback_present": True
            }
        },
        "formal_node_readback": [
            {"frame_id": "12:3", "photo_node_id": "12:4", "role": "DOUFANG_A_BASELINE", "raw_image_present": True, "raw_format": "jpeg", "export_png_bytes": 3269051, "canvas_dimensions": [2400, 3200], "visual_subject": "handmade tofu process", "visual_identity_match_to_registered_arm": True},
            {"frame_id": "12:11", "photo_node_id": "12:12", "role": "DOUFANG_B_DISTILLED", "raw_image_present": True, "raw_format": "jpeg", "export_png_bytes": 3582791, "canvas_dimensions": [2400, 3200], "visual_subject": "distinct handmade tofu process with mill, curd press, soybeans and formed tofu", "visual_identity_match_to_registered_arm": True},
            {"frame_id": "12:19", "photo_node_id": "12:20", "role": "CHAZUO_A_BASELINE", "raw_image_present": True, "raw_format": "jpeg", "export_png_bytes": 3583873, "canvas_dimensions": [2400, 3200], "visual_subject": "handmade tea non-heating process with bamboo trays and multiple leaf states", "visual_identity_match_to_registered_arm": True},
            {"frame_id": "12:27", "photo_node_id": "12:28", "role": "CHAZUO_B_DISTILLED", "raw_image_present": True, "raw_format": "jpeg", "export_png_bytes": 3621414, "canvas_dimensions": [2400, 3200], "visual_subject": "distinct handmade tea non-heating process with trays, cloth and multiple leaf states", "visual_identity_match_to_registered_arm": True}
        ],
        "established": [
            "All four formal P6 photo nodes now expose a real raw image and a 2400x3200 full-frame visual readback.",
            "The two tofu nodes and the two tea nodes are visually distinct A/B images rather than one repeated placeholder.",
            "A 2400x3200 PNG from the already-bound Doufang A node successfully traversed the same relay to the known-good scratch target, so generic large-PNG relay failure is not supported.",
            "The earlier HTTP-200/no-observable-placement state is superseded as a current blocker by later direct Figma readback; exact backend commit timing remains unknown."
        ],
        "limitations": [
            "No claim is made that Figma internal JPEG derivative bytes equal the originally generated source bytes.",
            "Binding identity is semantic and arm-specific as required by the current P6 lock; final photo-to-Figma-to-export provenance still requires final-stage receipt completion.",
            "No typography, integrated-design or final-pixel aesthetic pass is implied."
        ],
        "reupload_policy": "NO_FURTHER_FORMAL_PHOTO_REUPLOAD_WHILE_CURRENT_REAL_BINDINGS_REMAIN_PRESENT",
        "next": "REVIEW_EQUAL_BUDGET_INTEGRATED_FRAMES"
    }
    dump(TRANSITION, transition)

    review = {
        "schema_version": "vpd-p6-equal-budget-composition-review-round1/v1",
        "recorded_at": recorded,
        "figma_file_key": "uyDxOoN1iNDPpEHTKSUWg1",
        "page_id": "12:2",
        "reviewed_frames": ["12:3", "12:11", "12:19", "12:27"],
        "review_basis": [
            "actual full-frame Figma pixel readback at 2400x3200 canvas",
            "FIGMA_COMPOSITION_CONTRACT_V1",
            "COMMERCIAL_DESIGN_GATE_POLICY_V1",
            "frozen equal-budget rule: one composition pass plus at most one correction pass per poster"
        ],
        "verdict": "CORRECTION_REQUIRED_ALL_FOUR",
        "commercial_pass_claimed": False,
        "findings": {
            "12:3": {
                "role": "DOUFANG_A_BASELINE",
                "result": "FAIL_CORRECTION_REQUIRED",
                "issues": [
                    "A-arm title uses conspicuous planar cuts and deconstruction too close to the B-arm authored-display mechanism instead of moderate optical correction.",
                    "Title and support copy read as an overlay stack rather than a fully integrated photo-type relationship.",
                    "The same display treatment remains too interchangeable with the tea posters."
                ],
                "correction_intent": "Rebuild as a clean, sturdy tofu-specific editorial lockup with immediately readable glyphs, restrained optical edits, lower center of gravity and support copy placed in a genuinely quiet pocket."
            },
            "12:11": {
                "role": "DOUFANG_B_DISTILLED",
                "result": "FAIL_CORRECTION_REQUIRED",
                "issues": [
                    "B-arm title does not diverge enough from A; cuts look decorative rather than a deliberate counter/negative-space topology.",
                    "The title/support block competes with the wooden press instead of cleanly counterbalancing the process mass.",
                    "Brand-distinctive tofu/press/stone logic is under-authored."
                ],
                "correction_intent": "Use the frozen B plan: one broad planar two-glyph mass, purposeful counter geometry, 豆 broader/horizontal and 坊 slightly taller/heavier, with support copy clearly subordinate in the upper quiet region."
            },
            "12:19": {
                "role": "CHAZUO_A_BASELINE",
                "result": "FAIL_CORRECTION_REQUIRED",
                "issues": [
                    "Tea A repeats the same heavy cut-title vocabulary used by tofu, creating brand-swap template risk.",
                    "The oversized title suppresses the airy drying-workshop depth and the support copy sits close to active tray detail.",
                    "The typography does not express a lighter tea-specific editorial rhythm."
                ],
                "correction_intent": "Use a cleaner, more open A-arm title with restrained optical editing, more breathing room and a quiet-region alignment that lets bamboo trays and leaf-state progression remain primary evidence."
            },
            "12:27": {
                "role": "CHAZUO_B_DISTILLED",
                "result": "FAIL_CORRECTION_REQUIRED",
                "issues": [
                    "B title is large and readable but still shares the same generic cut-language as the tofu set.",
                    "Tea-specific rhythm from rack/tray spacing and the long calm table field is not translated into the title/support system.",
                    "Brand distinctiveness and photo-type integration remain below formal commercial standard."
                ],
                "correction_intent": "Build a tea-specific authored planar lockup with more open counters and directional spacing related to tray/rack rhythm; preserve strong first read while keeping support copy quiet and secondary."
            }
        },
        "equal_budget": {
            "composition_pass_per_poster": 1,
            "correction_pass_max_per_poster": 1,
            "correction_passes_used_before_this_review": {"12:3": 0, "12:11": 0, "12:19": 0, "12:27": 0},
            "B_extra_manual_budget": False
        },
        "next_required_action": "P6_APPLY_SINGLE_CORRECTION_PASS_ALL_POSTERS",
        "human_final_aesthetic_authority_preserved": True,
        "candidate_promotion_allowed": False
    }
    dump(REVIEW, review)

    trans_ref = ref(TRANSITION)
    review_ref = ref(REVIEW)

    lock["revision"] = 31
    lock["preserved_prior_revision"] = {
        "revision": 30,
        "git_blob_sha": old_blob,
        "note": "Revision 30 recorded the unresolved relay placement mismatch before later direct Figma readback proved all four formal photo nodes present."
    }
    p6 = lock["p6_integrated_design"]
    p6["status"] = "COMPOSITION_REVIEW_FAIL_CORRECTION_AUTHORIZED"
    for frame in p6["frames"]:
        frame["bound"] = True
        frame["locked"] = False
    p6["bound_count"] = 4
    p6["remaining_bindings"] = []
    p6["normal_chat_blocker"] = None
    p6["correction_passes_used"] = {"12:3": 0, "12:11": 0, "12:19": 0, "12:27": 0}
    p6["final_pixel_validation_allowed"] = False
    lock["figma_upload_relay"]["status"] = "FORMAL_BINDINGS_LATE_READBACK_CONFIRMED"
    lock["current_stage"] = "All four formal P6 photo nodes now contain distinct real A/B images on direct Figma readback. Round-1 equal-budget integrated composition review failed all four on typography/photo-type integration/brand-distinctiveness grounds. Exactly one symmetric correction pass per poster is now authorized; no further photo reupload or taste rerender is authorized."
    lock["status"] = "VPD_P6_COMPOSITION_CORRECTION_REQUIRED"
    lock["next_required_action"] = "P6_APPLY_SINGLE_CORRECTION_PASS_ALL_POSTERS"
    lock["completed_this_revision"] = [
        "identified the first Doufang A source URL as a 960x1280 JPEG derivative rather than an exact original large-source control",
        "completed a 2400x3200 bound-node PNG scratch control with HTTP 200 and observable raw-image placement",
        "directly reread formal nodes 12:4, 12:12, 12:20 and 12:28 and confirmed distinct real tofu/tea A/B images",
        "closed the relay placement mismatch as a current blocker while preserving all prior failure receipts as historical evidence",
        "reviewed all four complete 2400x3200 Figma frames under the composition contract and commercial-gate policy",
        "authorized exactly one symmetric correction pass for each of the four posters; none consumed yet"
    ]
    lock["updated_at"] = recorded
    lock["state_profile"] = "p6-composition/v1"
    lock["composition_transition_evidence"] = trans_ref
    lock["composition_review_evidence"] = review_ref
    lock["blockers"] = [
        "Final pixel and editability validation remains blocked until the single correction pass is completed or explicitly waived for every poster.",
        "Human set verdict, candidate promotion, second-family completion, Golden and Scale remain blocked.",
        "Historical system-validation ledger prefix retains its disclosed pre-existing hash defects and is not recertified."
    ]
    lock["diagnostic_next_required_action"] = None
    lock["relay_placement_resolution"] = trans_ref
    lock["render_allowed"] = False
    dump(LOCK, lock)
    lock_sha = sha_file(LOCK)

    previous = None
    lines = LEDGER.read_text(encoding="utf-8").splitlines()
    for line in lines:
        obj = json.loads(line)
        previous = {"event_id": obj["event_id"], "event_hash": obj["event_hash"]}
    event = {
        "schema_version": "upcp-state-ledger-event/v1",
        "stream_id": "commercial_design_pipeline",
        "event_id": "EVT-VPD-P6-COMPOSITION-CORRECTION-AUTHORIZED-20260914-001",
        "event_type": "P6_FORMAL_BINDINGS_RESOLVED_COMPOSITION_REVIEW_CORRECTION_AUTHORIZED",
        "task_id": "VPD-SYSTEM-LEVEL-HOLDOUT-TRANSFER-VALIDATION-V1",
        "project_id": "visual-aesthetic-vpd",
        "recorded_at": recorded,
        "material": True,
        "previous_event_id": previous["event_id"] if previous else None,
        "previous_event_hash": previous["event_hash"] if previous else None,
        "lock_sha256": lock_sha,
        "authorization": {
            "source": "current controlling ChatGPT conversation",
            "instruction": "continue the next project step",
            "scope": "close stale P6 relay blocker, review four integrated frames, open one correction pass per poster"
        },
        "before": {"state": "UPLOAD_PASS_PLACEMENT_MISMATCH_BLOCKED", "recorded_bound_count": 1},
        "after": {"state": "COMPOSITION_REVIEW_FAIL_CORRECTION_AUTHORIZED", "readback_bound_count": 4, "correction_budget_each": 1, "correction_used_each": 0},
        "evidence": [trans_ref["path"], review_ref["path"], "contracts/vpd/FIGMA_COMPOSITION_CONTRACT_V1.json", "contracts/vpd/COMMERCIAL_DESIGN_GATE_POLICY_V1.json"],
        "reason": "Direct Figma readback superseded the stale placement blocker: all four formal photo nodes contain distinct real A/B images. Full-frame review then found the existing typography system below the forward commercial design contract, so the only next authorized design action is the predeclared single symmetric correction pass.",
        "remote_authority": {"repository": "vubaoha034-hash/shenmei", "branch": "visual-program-distillation-v2-photography-design-20260814"}
    }
    event["event_hash"] = canonical_event_hash(event)
    with LEDGER.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(event, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")

    cp["sequence"] = 53
    cp["recorded_at"] = recorded
    cp["current_focus"] = lock["current_stage"]
    for item in [
        "p6_doufang_A_large_bound_node_control_pass",
        "p6_all_four_formal_photo_nodes_direct_readback_confirmed",
        "p6_equal_budget_composition_review_round1_completed"
    ]:
        if item not in cp["completed"]:
            cp["completed"].append(item)
    cp["incomplete"] = [
        "p6_single_correction_pass_per_poster",
        "p6_final_pixel_and_editability_validation",
        "human_set_verdict",
        "candidate_promotion",
        "second_style_family_validation",
        "golden",
        "scale"
    ]
    cp["blocked"] = lock["blockers"]
    cp["next_required_action"] = lock["next_required_action"]
    cp["p6"]["photo_nodes"] = {f["photo"]: {"bound": True, "locked": False} for f in p6["frames"]}
    cp["p6"]["real_images_bound_count"] = 4
    cp["p6"]["figma_entry_allowed"] = True
    cp["p6"]["final_pixel_validation_allowed"] = False
    cp["p6"]["composition_review_completed"] = True
    cp["p6"]["correction_passes_used"] = dict(p6["correction_passes_used"])
    cp["relay"]["status"] = "FORMAL_BINDINGS_LATE_READBACK_CONFIRMED"
    cp["status"] = lock["status"]
    cp["task_lock"] = {"path": "continuity/vpd/CURRENT_TASK_LOCK.json", "sha256": lock_sha}
    cp["requirements"]["p6_integrated_design"]["status"] = "COMPOSITION_REVIEW_FAIL_CORRECTION_AUTHORIZED"
    cp["ledger_tails"] = {"commercial_design_pipeline": {"event_id": event["event_id"], "event_hash": event["event_hash"]}}
    dump(CP, cp)

    adapter["vpd_system_goal_authority"]["checkpoint"] = lock["status"]
    adapter["vpd_system_goal_authority"]["next_required_action"] = lock["next_required_action"]
    adapter["vpd_system_goal_authority"]["render_allowed"] = False
    adapter["task_lock"]["revision"] = 31
    adapter["task_lock"]["sha256"] = lock_sha
    adapter["forward_commercial_pipeline"]["status"] = "ACTIVE_P6_INTEGRATED_COMPOSITION_CORRECTION"
    adapter["forward_commercial_pipeline"]["next_required_action"] = lock["next_required_action"]
    for new_auth in [
        {**trans_ref, "priority": 0, "purpose": "Direct Figma readback resolution closing the stale P6 relay-placement blocker without reupload."},
        {**review_ref, "priority": 0, "purpose": "Round-1 equal-budget integrated-frame review authorizing exactly one correction pass per poster."}
    ]:
        adapter["change_authorities"].insert(0, new_auth)
    dump(ADAPTER, adapter)

    print(json.dumps({
        "status": "P6_COMPOSITION_STATE_ADVANCED",
        "lock_revision": 31,
        "checkpoint_sequence": 53,
        "next_required_action": lock["next_required_action"],
        "transition_evidence": trans_ref,
        "review_evidence": review_ref,
        "lock_sha256": lock_sha,
        "ledger_event_id": event["event_id"],
        "ledger_event_hash": event["event_hash"]
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
