"""P6 integrated-composition state guard.

This profile begins only after all four formal photo nodes have real-image readback.
It preserves the frozen A/B inputs and equal-budget rule, and authorizes only the
single recorded correction pass and subsequent final pixel/editability review.
It is an evidence/state guard, never an aesthetic oracle.
"""
from __future__ import annotations

import hashlib
import json

from .vpd_task_lock import (
    LOCK_PATH, CHECKPOINT_PATH, PROJECT, PARENT,
    read, path, require, check_ref, digest,
)

PROFILE = "p6-composition/v1"
FILE_KEY = "uyDxOoN1iNDPpEHTKSUWg1"
TARGETS = [
    ("12:3", "DOUFANG_A_BASELINE", "12:4"),
    ("12:11", "DOUFANG_B_DISTILLED", "12:12"),
    ("12:19", "CHAZUO_A_BASELINE", "12:20"),
    ("12:27", "CHAZUO_B_DISTILLED", "12:28"),
]
ACTIONS = {
    "P6_APPLY_SINGLE_CORRECTION_PASS_ALL_POSTERS",
    "P6_VALIDATE_FINAL_PIXELS_EDITABILITY",
    "P6_WAIT_HUMAN_SET_VERDICT",
}


def _validate_commercial_ledger(root, lock, cp):
    stream = "commercial_design_pipeline"
    p = path(root, f"continuity/vpd/state_ledger/{stream}.jsonl")
    previous = None
    for line in p.read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        claimed = event.pop("event_hash")
        actual = hashlib.sha256(
            json.dumps(event, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        require(claimed == actual, "COMMERCIAL_LEDGER_HASH_MISMATCH")
        require(
            event["previous_event_id"] == (previous["event_id"] if previous else None),
            "COMMERCIAL_LEDGER_PARENT_ID",
        )
        require(
            event["previous_event_hash"] == (previous["event_hash"] if previous else None),
            "COMMERCIAL_LEDGER_PARENT_HASH",
        )
        previous = {"event_id": event["event_id"], "event_hash": claimed, **event}
    require(previous is not None, "COMMERCIAL_LEDGER_EMPTY")
    require(
        cp["ledger_tails"] == {
            stream: {"event_id": previous["event_id"], "event_hash": previous["event_hash"]}
        },
        "COMMERCIAL_LEDGER_TAIL_MISMATCH",
    )
    require(previous.get("lock_sha256") == digest(path(root, LOCK_PATH)), "COMMERCIAL_LEDGER_STALE_LOCK")


def validate_p6_composition_state(root):
    lock = read(root, LOCK_PATH)
    cp = read(root, CHECKPOINT_PATH)
    adapter = read(root, "PROJECT_CONTROL_ADAPTER.json")

    require(lock["schema_version"] == "vpd-current-task-lock/v1", "LOCK_SCHEMA")
    require(lock.get("state_profile") == PROFILE, "STATE_PROFILE")
    require(lock["project_id"] == cp["project_id"] == adapter["project_id"] == PROJECT, "PROJECT_ID_MISMATCH")
    require(lock["parent_active_task_id"] == PARENT and cp["active_task_ids"] == [PARENT], "PARENT_TASK_CHANGED")
    require(lock["repository"] == adapter["repository"] == "vubaoha034-hash/shenmei", "REPOSITORY_DRIFT")
    require(lock["branch"] == adapter["canonical_branch"] == "visual-program-distillation-v2-photography-design-20260814", "BRANCH_DRIFT")

    dispatch = adapter["task_lock"]
    require(dispatch["path"] == adapter["task_registry_path"] == LOCK_PATH, "COMPETING_TASK_INDEX")
    require(dispatch["revision"] == lock["revision"] >= 31, "STALE_LOCK_REVISION")
    require(dispatch["sha256"] == digest(path(root, LOCK_PATH)), "ADAPTER_STALE_LOCK")
    require(cp["task_lock"] == {"path": LOCK_PATH, "sha256": digest(path(root, LOCK_PATH))}, "STALE_CHECKPOINT_LOCK")

    require(cp["status"] == lock["status"] == adapter["vpd_system_goal_authority"]["checkpoint"], "STATE_STATUS_CONFLICT")
    action = lock["next_required_action"]
    require(action in ACTIONS, "COMPOSITION_ACTION_UNKNOWN")
    require(action == cp["next_required_action"] == adapter["vpd_system_goal_authority"]["next_required_action"], "NEXT_ACTION_DRIFT")
    require(lock["render_allowed"] is False and adapter["vpd_system_goal_authority"]["render_allowed"] is False, "RENDER_NOT_AUTHORIZED")

    old = read(root, "evidence/vpd/p6_authority_repair_v1/LOCK_BEFORE.json")
    require(lock["objective"] == old["objective"] and lock["family"] == old["family"], "OBJECTIVE_DRIFT")
    require(lock["capsule"] == old["capsule"] and not lock["capsule"]["promoted"], "CAPSULE_IDENTITY_DRIFT")
    require(lock["mechanism_transfer_verdict"] == old["mechanism_transfer_verdict"], "UNSUPPORTED_PROMOTION")

    wf = lock["workflow"]["document"]
    check_ref(root, wf)
    require(cp["workflow"] == wf == {k: adapter["workflow"][k] for k in ("path", "sha256")}, "WORKFLOW_REFERENCE_CONFLICT")
    require(lock["workflow"]["focus_stage"] == "P6" and lock["workflow"]["status_authority"] == LOCK_PATH, "WORKFLOW_STAGE_DRIFT")

    transition = lock["composition_transition_evidence"]
    review = lock["composition_review_evidence"]
    check_ref(root, transition)
    check_ref(root, review)
    transition_doc = read(root, transition["path"])
    review_doc = read(root, review["path"])
    require(transition_doc["status"] == "ALL_FOUR_FORMAL_PHOTO_NODES_READBACK_CONFIRMED", "PHOTO_BINDING_TRANSITION_INVALID")
    require(review_doc["verdict"] == "CORRECTION_REQUIRED_ALL_FOUR", "COMPOSITION_REVIEW_NOT_CLOSED")

    p6 = lock["p6_integrated_design"]
    require(p6["figma_file_key"] == FILE_KEY and p6["frame_size"] == [2400, 3200], "P6_GEOMETRY_DRIFT")
    require([(f["id"], f["name"], f["photo"]) for f in p6["frames"]] == TARGETS, "P6_TARGET_DRIFT")
    require(all(f["bound"] is True and f["locked"] is False for f in p6["frames"]), "P6_BINDING_NOT_COMPLETE")
    require(p6["bound_count"] == cp["p6"]["real_images_bound_count"] == 4, "P6_COUNT_CONFLICT")
    require(p6["remaining_bindings"] == [], "P6_REMAINING_CONFLICT")
    require(cp["p6"]["photo_nodes"] == {f["photo"]: {"bound": True, "locked": False} for f in p6["frames"]}, "P6_MIRROR_CONFLICT")
    require(p6["semantic_raw_asset_identity_locked"] is True and p6["figma_photo_node_locked_required"] is False, "ASSET_LOCK_DRIFT")
    require(p6["equal_budget"] == {"composition_pass_per_poster": 1, "correction_pass_max_per_poster": 1, "B_extra_manual_budget": False}, "P6_BUDGET_DRIFT")

    used = p6["correction_passes_used"]
    require(set(used) == {f["id"] for f in p6["frames"]}, "CORRECTION_BUDGET_KEYS")
    require(all(v in (0, 1) for v in used.values()), "CORRECTION_BUDGET_RANGE")
    if action == "P6_APPLY_SINGLE_CORRECTION_PASS_ALL_POSTERS":
        require(all(v == 0 for v in used.values()), "CORRECTION_ALREADY_CONSUMED")
        require(p6["final_pixel_validation_allowed"] is False and cp["p6"]["final_pixel_validation_allowed"] is False, "PREMATURE_PIXEL_VALIDATION")
    elif action == "P6_VALIDATE_FINAL_PIXELS_EDITABILITY":
        require(all(v == 1 for v in used.values()), "CORRECTION_NOT_COMPLETE")
        require(p6["final_pixel_validation_allowed"] is True and cp["p6"]["final_pixel_validation_allowed"] is True, "PIXEL_VALIDATION_NOT_OPEN")
        check_ref(root, lock["correction_pass_evidence"])
    elif action == "P6_WAIT_HUMAN_SET_VERDICT":
        require(all(v == 1 for v in used.values()), "CORRECTION_NOT_COMPLETE")
        check_ref(root, lock["correction_pass_evidence"])
        check_ref(root, lock["final_validation_evidence"])

    require(not set(cp["completed"]) & set(cp["incomplete"]), "COMPLETED_AND_INCOMPLETE")
    _validate_commercial_ledger(root, lock, cp)
    return lock, cp
