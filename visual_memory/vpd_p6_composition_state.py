"""P6 integrated-composition state guard.

This profile begins only after all four formal photo nodes have real-image readback.
It preserves the frozen A/B inputs and equal-budget rule, records the single
correction pass and final validation, and can return a human-failed typography
result to a bounded P1 typography-repair bench without rewriting the P6 evidence.
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
PAIR2_VALIDATOR_REPAIR_ACTION = "REPAIR_VPD_STATE_VALIDATOR_FORWARD_COMPATIBILITY_BEFORE_PAIR2_FIGMA_CANVAS_WRITE"
PAIR2_VALIDATOR_CI_ACTION = "WAIT_FOR_VPD_STATE_VALIDATOR_CI_PASS_BEFORE_PAIR2_FIGMA_CANVAS_WRITE"
PAIR2_WAIT_CANVAS_AUTH_ACTION = "WAIT_FOR_USER_AUTHORIZATION_PAIR2_EQUAL_BUDGET_FIGMA_CANVAS_WRITE"
PAIR2_POSTER_BLIND_RESULT_ACTION = "WAIT_FOR_USER_DECISION_PAIR2_COMPLETE_POSTER_CORRECTION_OR_SETTLEMENT"
PAIR2_PREWRITE_ACTIONS = {PAIR2_VALIDATOR_REPAIR_ACTION, PAIR2_VALIDATOR_CI_ACTION, PAIR2_WAIT_CANVAS_AUTH_ACTION}
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
    "P1_PREPARE_TYPOGRAPHY_ONLY_DISTILLATION_REPAIR_BENCH",
    "P1_EXECUTE_TYPOGRAPHY_ONLY_TITLE_BENCH",
    "P1_WAIT_HUMAN_TITLE_BENCH_VERDICT",
    "P1_WAIT_HUMAN_TITLE_TECHNICAL_RETRY_VERDICT",
    "P1_EXECUTE_WORDMARK_SYSTEM_REPAIR_V2",
    "P1_WAIT_HUMAN_WORDMARK_V2_VERDICT",
    "P1_EXECUTE_SEMANTIC_ANCHOR_WORDMARK_V3",
    "P1_WAIT_HUMAN_SEMANTIC_ANCHOR_WORDMARK_V3_VERDICT",
    "P1_EXECUTE_STRUCTURAL_WORDMARK_V4",
    "P1_WAIT_HUMAN_STRUCTURAL_WORDMARK_V4_DIRECTION_VERDICT",
    "P1_EXECUTE_GENERATIVE_CUSTOM_WORDMARK_EXPLORATION_V5",
    "P1_WAIT_HUMAN_GENERATIVE_CUSTOM_WORDMARK_V5_DIRECTION_VERDICT",
    "P1_EXECUTE_NONCALLIGRAPHIC_SEMANTIC_WORDMARK_V6",
    "P1_VECTOR_RECONSTRUCT_V6_IN_FIGMA",
    "P1_WAIT_HUMAN_V6_FIGMA_VECTOR_REVIEW",
    "P1_PREPARE_HYBRID_TEXTURE_FINISH_PROBE",
    "P1_EXECUTE_TYPOGRAPHY_METHOD_SANDBOX_TEST_01",
    "P1_EXECUTE_TYPOGRAPHY_METHOD_SANDBOX_TEST_02",
    PAIR2_VALIDATOR_REPAIR_ACTION,
    PAIR2_VALIDATOR_CI_ACTION,
    PAIR2_WAIT_CANVAS_AUTH_ACTION,
    "PREPARE_PAIR2_COMPLETE_POSTER_BLIND_REVIEW_PACKAGE_NO_CANVAS_WRITE",
    "RUN_PAIR2_COMPLETE_POSTER_INDEPENDENT_BLIND_EVALUATION_AND_RETURN_VERDICT",
    PAIR2_POSTER_BLIND_RESULT_ACTION,
}


def validate_t1_retry_record(record):
    """Validate scope/budget only; this never certifies lettering or taste."""
    require(record["status"] == "FROZEN_WAITING_HUMAN_REVIEW", "T1_RETRY_STATUS")
    require(record["technical_retries_used"] == {"豆坊": 1, "茶作": 1}, "T1_RETRY_BUDGET")
    require(record["additional_aesthetic_corrections"] == 0, "T1_EXTRA_AESTHETIC_RETRY")
    require(record["original_title_gate"] == "NOT_PASS_GLYPH_CORRECTNESS_FAIL", "T1_FAILURE_RECLASSIFIED")
    require(record["post_retry_human_verdict"] is None, "T1_PREMATURE_HUMAN_VERDICT")
    require(record["T2_allowed"] is False and record["P6_reintegration_allowed"] is False, "T1_PREMATURE_ADVANCE")
    require(record["candidate1_frame_ids"] == ["53:3", "53:10"] and record["candidate2_frame_ids"] == ["53:17", "53:33"], "T1_TARGET_DRIFT")
    require(record["mutated_glyphs"] == ["55:4", "55:7"], "T1_MUTATION_SCOPE")
    require(len(record["exports"]) == 4 and all(e["metadata_readback_verified"] and e["dimensions"] == [1600, 900] for e in record["exports"]), "T1_EXPORT_READBACK")
    require(record["on_repeat_glyph_failure"] == "STOP_CURRENT_TYPOGRAPHY_COMPILER_DO_NOT_ENTER_T2", "T1_STOP_RULE")
    require(record["no_more_retry_authorized"] is True, "T1_RETRY_REOPENED")


def _validate_commercial_ledger(root, lock, cp):
    stream = "commercial_design_pipeline"
    p = path(root, f"continuity/vpd/state_ledger/{stream}.jsonl")
    freeze_ref = lock.get("authority_repair", {}).get("commercial_ledger_preexisting_hash_defects")
    frozen = {}
    if freeze_ref:
        check_ref(root, freeze_ref)
        freeze = read(root, freeze_ref["path"])
        require(freeze["ledger_path"] == f"continuity/vpd/state_ledger/{stream}.jsonl", "COMMERCIAL_LEDGER_FREEZE_PATH")
        frozen = {item["event_id"]: item for item in freeze["frozen_invalid_events"]}
        require(len(frozen) == freeze["defect_count"], "COMMERCIAL_LEDGER_FREEZE_DUPLICATE_ID")

    previous = None
    seen_frozen = set()
    for raw_line in p.read_text(encoding="utf-8").splitlines():
        event = json.loads(raw_line)
        claimed = event.pop("event_hash")
        actual = hashlib.sha256(
            json.dumps(event, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        frozen_item = frozen.get(event["event_id"])
        if frozen_item is not None:
            require(
                hashlib.sha256(raw_line.encode()).hexdigest() == frozen_item["line_sha256"],
                "COMMERCIAL_LEDGER_FROZEN_DEFECT_MUTATED",
            )
            require(claimed == frozen_item["claimed_event_hash"], "COMMERCIAL_LEDGER_FROZEN_CLAIM_DRIFT")
            require(actual == frozen_item["recomputed_canonical_hash"], "COMMERCIAL_LEDGER_FROZEN_RECOMPUTE_DRIFT")
            require(claimed != actual, "COMMERCIAL_LEDGER_FROZEN_DEFECT_REWRITTEN")
            seen_frozen.add(event["event_id"])
        else:
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
    require(seen_frozen == set(frozen), "COMMERCIAL_LEDGER_FROZEN_DEFECT_SET_DRIFT")
    require(previous is not None, "COMMERCIAL_LEDGER_EMPTY")
    require(
        cp["ledger_tails"] == {
            stream: {"event_id": previous["event_id"], "event_hash": previous["event_hash"]}
        },
        "COMMERCIAL_LEDGER_TAIL_MISMATCH",
    )
    require(previous.get("lock_sha256") == digest(path(root, LOCK_PATH)), "COMMERCIAL_LEDGER_STALE_LOCK")


def _validate_pair2_equal_budget_prewrite(root, lock, cp, action):
    pair = lock.get("pair2_equal_budget_figma_ab", {})
    require(pair.get("status") == "PREPARED_NO_CANVAS_WRITE", "PAIR2_FIGMA_PREP_STATUS")
    require(cp.get("pair2_equal_budget_figma_ab") == pair, "PAIR2_FIGMA_CHECKPOINT_DRIFT")
    require(pair.get("figma_file_key") == FILE_KEY, "PAIR2_FIGMA_FILE_DRIFT")
    require(pair.get("current_canvas_write_authorization") == 0, "PAIR2_PREMATURE_CANVAS_WRITE_AUTH")
    require(pair.get("composition_pass_per_poster") == 1, "PAIR2_COMPOSITION_BUDGET")
    require(pair.get("correction_pass_max_per_poster") == 1, "PAIR2_CORRECTION_BUDGET")
    require(pair.get("route_B_extra_manual_budget") is False, "PAIR2_B_EXTRA_POLISH")
    require(pair.get("typography_control_is_not_typography_distillation_pass") is True, "PAIR2_FALSE_TYPOGRAPHY_PASS")
    check_ref(root, pair["prep"])
    check_ref(root, pair["blind_evaluator_prompt"])

    prep = read(root, pair["prep"]["path"])
    require(prep["status"] == "PREPARED_NO_CANVAS_WRITE", "PAIR2_PREP_NOT_FROZEN")
    require(prep["fixed_poster_input"]["frame_size"] == [2400, 3200] and prep["fixed_poster_input"]["aspect"] == "3:4", "PAIR2_FRAME_DRIFT")
    require(prep["fixed_poster_input"]["copy"] == {"title":"豆坊","english":"HANDMADE TOFU","support":"手作豆腐 · 当日现制"}, "PAIR2_COPY_DRIFT")
    require(prep["fixed_poster_input"]["no_new_image_generation"] is True, "PAIR2_IMAGE_GENERATION_REOPENED")
    require(prep["fixed_poster_input"]["no_photo_retouch"] is True and prep["fixed_poster_input"]["no_photo_regeneration"] is True, "PAIR2_PHOTO_MUTATION_REOPENED")
    require(prep["source_pair"]["route_A"]["sha256"] == pair["source_pair"]["route_A_sha256"], "PAIR2_ROUTE_A_SOURCE_DRIFT")
    require(prep["source_pair"]["route_B"]["sha256"] == pair["source_pair"]["route_B_sha256"], "PAIR2_ROUTE_B_SOURCE_DRIFT")
    require(prep["source_pair"]["route_A"]["dimensions"] == [1086, 1448] and prep["source_pair"]["route_B"]["dimensions"] == [1086, 1448], "PAIR2_SOURCE_DIMENSION_DRIFT")
    require(prep["typography_control_layer"]["old_failed_p6_custom_title_vectors_reused"] is False, "PAIR2_FAILED_TITLE_REUSED")
    require(prep["typography_control_layer"]["typography_design_gate_claimed_by_this_control"] is False, "PAIR2_FALSE_TYPOGRAPHY_GATE")
    require(prep["shared_composition_rule"]["same_rule_for_A_and_B"] is True, "PAIR2_ASYMMETRIC_COMPOSITION_RULE")
    require(prep["equal_budget"] == {
        "same_figma_file": True,
        "same_frame_size": True,
        "same_copy": True,
        "same_font_sources": True,
        "same_typography_control_layer": True,
        "composition_pass_per_poster": 1,
        "correction_pass_max_per_poster": 1,
        "hidden_polish": False,
        "extra_assets_after_assignment": False,
        "route_B_extra_manual_budget": False,
    }, "PAIR2_EQUAL_BUDGET_DRIFT")
    old_page = prep["figma_plan"]["old_negative_evidence_page"]
    require(old_page == {"page_id":"12:2","name":"P6 Equal Budget Integrated Validation","modify":False}, "PAIR2_OLD_P6_PAGE_MUTATION")
    require(prep["figma_plan"]["new_page"]["page_id"] == "PENDING_CANVAS_WRITE", "PAIR2_PREMATURE_FIGMA_PAGE_WRITE")
    require(prep["authorization"]["current_canvas_write_authorization"] == 0 and prep["authorization"]["current_image_generation_authorization"] == 0, "PAIR2_PREMATURE_RESOURCE_AUTH")
    blind = prep["evaluation"]["blind_review"]
    require(blind["prewrite_prompt"] == {k: pair["blind_evaluator_prompt"][k] for k in ("path", "sha256")}, "PAIR2_BLIND_PROMPT_DRIFT")
    require(pair["blind_evaluator_prompt"].get("prewrite_frozen") is True, "PAIR2_BLIND_PROMPT_NOT_FROZEN")
    require(blind["mapping_frozen_before_canvas_write"] is True and blind["mapping"] == {"X":"Route A","Y":"Route B"}, "PAIR2_BLIND_MAPPING_DRIFT")
    require(blind["evaluator_must_not_know_mapping"] is True, "PAIR2_BLIND_LEAK")

    gate = pair.get("validator_gate", {})
    require(gate.get("figma_canvas_write_allowed") is False, "PAIR2_VALIDATOR_GATE_BYPASSED")
    if action == PAIR2_VALIDATOR_REPAIR_ACTION:
        require(lock["status"] == "VPD_PAIR2_FIGMA_AB_PREP_SAVED_VALIDATOR_FORWARD_COMPATIBILITY_BLOCKED_NO_CANVAS_WRITE", "PAIR2_REPAIR_STATE")
        require(gate.get("status") == "BLOCKED_FORWARD_INCOMPATIBLE", "PAIR2_REPAIR_GATE_STATE")
        check_ref(root, gate["blocker"])
    elif action == PAIR2_VALIDATOR_CI_ACTION:
        require(lock["status"] == "VPD_PAIR2_FIGMA_AB_VALIDATOR_REPAIR_IMPLEMENTED_AWAITING_CI_PASS_NO_CANVAS_WRITE", "PAIR2_VALIDATOR_CI_STATE")
        require(gate.get("status") == "REPAIR_IMPLEMENTED_AWAITING_CI", "PAIR2_VALIDATOR_CI_GATE")
        check_ref(root, gate["blocker"])
        check_ref(root, gate["repair_implementation"])
        implementation = read(root, gate["repair_implementation"]["path"])
        require(implementation["status"] == "IMPLEMENTED_AWAITING_CI", "PAIR2_VALIDATOR_IMPLEMENTATION_STATE")
        require(implementation["figma_canvas_write_authorized"] is False, "PAIR2_IMPLEMENTATION_PREMATURE_WRITE")
        require(implementation["commercial_ledger_defect_freeze"] == lock["authority_repair"]["commercial_ledger_preexisting_hash_defects"], "PAIR2_LEDGER_FREEZE_REFERENCE_DRIFT")
    elif action == PAIR2_WAIT_CANVAS_AUTH_ACTION:
        require(lock["status"] == "VPD_P3_PAIR2_EQUAL_BUDGET_FIGMA_COMPLETE_POSTER_AB_PREPARED_AWAITING_CANVAS_WRITE_AUTHORIZATION", "PAIR2_WAIT_CANVAS_STATE")
        require(gate.get("status") == "PASS", "PAIR2_VALIDATOR_NOT_PASSED")
        check_ref(root, gate["validation_receipt"])
        receipt = read(root, gate["validation_receipt"]["path"])
        require(receipt["conclusion"] == "SUCCESS" and receipt["state_validator"] == "VPD_STATE_VALID", "PAIR2_VALIDATOR_PASS_RECEIPT")
        require(receipt["figma_canvas_write_authorized"] is False, "PAIR2_RECEIPT_PREMATURE_WRITE")
    require(lock.get("p6_allowed") is False, "PAIR2_P6_PREMATURE_OPEN")


def _validate_pair2_complete_poster_blind_package(root, lock, cp):
    pair = lock.get("pair2_equal_budget_figma_ab", {})
    require(pair.get("status") == "COMPLETE_POSTER_BLIND_PACKAGE_READY", "PAIR2_POSTER_BLIND_PACKAGE_STATE")
    require(cp.get("pair2_equal_budget_figma_ab") == pair, "PAIR2_POSTER_BLIND_CHECKPOINT_DRIFT")
    require(pair.get("current_canvas_write_authorization") == 0, "PAIR2_POSTER_BLIND_CANVAS_REOPENED")
    require(pair.get("composition_passes_used") == {"A":1,"B":1}, "PAIR2_POSTER_COMPOSITION_BUDGET_DRIFT")
    require(pair.get("correction_passes_used") == {"A":0,"B":0}, "PAIR2_POSTER_CORRECTION_BUDGET_DRIFT")
    require(pair.get("route_B_extra_manual_budget") is False, "PAIR2_POSTER_B_EXTRA_POLISH")
    for name in ("composition_evidence", "blind_package", "blind_mapping", "blind_evaluator_prompt", "blind_handoff"):
        check_ref(root, pair[name])
    package = read(root, pair["blind_package"]["path"])
    mapping = read(root, pair["blind_mapping"]["path"])
    require(package["status"] == "READY_FOR_INDEPENDENT_BLIND_EVALUATION", "PAIR2_POSTER_PACKAGE_NOT_READY")
    require(package["no_canvas_write_this_step"] is True, "PAIR2_POSTER_PACKAGE_CANVAS_WRITE")
    require(package["evaluator_identity_boundary"]["current_verdict"] == "PENDING", "PAIR2_POSTER_PREMATURE_VERDICT")
    require(package["evaluator_identity_boundary"]["evaluator_must_not_know_mapping"] is True, "PAIR2_POSTER_BLIND_LEAK")
    require(mapping["blind_X"]["route"] == "A" and mapping["blind_Y"]["route"] == "B", "PAIR2_POSTER_MAPPING_DRIFT")
    require(mapping["blind_X"]["sha256"] == package["library_assets"]["X"]["sha256"], "PAIR2_POSTER_X_HASH_DRIFT")
    require(mapping["blind_Y"]["sha256"] == package["library_assets"]["Y"]["sha256"], "PAIR2_POSTER_Y_HASH_DRIFT")
    require(mapping["blind_X"]["dimensions"] == mapping["blind_Y"]["dimensions"] == [2400,3200], "PAIR2_POSTER_DIMENSION_DRIFT")
    require(package["composition_budget_unchanged"]["correction_passes_used"] == {"A":0,"B":0}, "PAIR2_POSTER_HIDDEN_CORRECTION")
    require(lock.get("p6_allowed") is False, "PAIR2_POSTER_PREMATURE_P6_OPEN")


def _validate_pair2_complete_poster_blind_result(root, lock, cp):
    pair = lock.get("pair2_equal_budget_figma_ab", {})
    require(pair.get("status") == "COMPLETE_POSTER_BLIND_VERDICT_RECORDED_ROUTE_A_WINS_WAITING_USER_SETTLEMENT", "PAIR2_POSTER_RESULT_STATE")
    require(cp.get("pair2_equal_budget_figma_ab") == pair, "PAIR2_POSTER_RESULT_CHECKPOINT_DRIFT")
    require(pair.get("current_canvas_write_authorization") == 0, "PAIR2_POSTER_RESULT_CANVAS_REOPENED")
    require(pair.get("composition_passes_used") == {"A":1,"B":1}, "PAIR2_POSTER_RESULT_COMPOSITION_BUDGET_DRIFT")
    require(pair.get("correction_passes_used") == {"A":0,"B":0}, "PAIR2_POSTER_RESULT_CORRECTION_BUDGET_DRIFT")
    require(pair.get("complete_poster_blind_verdict") == "X_WINS_ROUTE_A_MEDIUM_CONFIDENCE", "PAIR2_POSTER_RESULT_VERDICT_DRIFT")
    require(pair.get("blind_outcome") == "ROUTE_A_WINS", "PAIR2_POSTER_RESULT_ROUTE_DRIFT")
    require(pair.get("correction_pass_decision") == "PENDING_USER_DECISION", "PAIR2_POSTER_RESULT_DECISION_DRIFT")
    for name in ("composition_evidence", "blind_package", "blind_mapping", "blind_evaluator_prompt", "blind_handoff", "blind_result"):
        check_ref(root, pair[name])
    package = read(root, pair["blind_package"]["path"])
    mapping = read(root, pair["blind_mapping"]["path"])
    result = read(root, pair["blind_result"]["path"])
    require(result["pair_id"] == "VPD-PAIR2-EQUAL-BUDGET-FIGMA-COMPLETE-POSTER-BLIND", "PAIR2_POSTER_RESULT_PAIR_ID")
    verdict = result["evaluator_verdict"]
    require(verdict["winner"] == "X" and verdict["confidence"] == "MEDIUM", "PAIR2_POSTER_RESULT_EVALUATOR_VERDICT")
    require(verdict["correctness_X"] == verdict["correctness_Y"] == "PASS", "PAIR2_POSTER_RESULT_CORRECTNESS")
    require(result["revealed_mapping_after_verdict"] == {"X":"A","Y":"B"} and result["blind_outcome"] == "ROUTE_A_WINS", "PAIR2_POSTER_RESULT_MAPPING")
    require(result["inputs"]["X"]["sha256"] == package["library_assets"]["X"]["sha256"] == mapping["blind_X"]["sha256"], "PAIR2_POSTER_RESULT_X_HASH")
    require(result["inputs"]["Y"]["sha256"] == package["library_assets"]["Y"]["sha256"] == mapping["blind_Y"]["sha256"], "PAIR2_POSTER_RESULT_Y_HASH")
    require(result["conclusion"]["correction_passes_used"] == {"A":0,"B":0}, "PAIR2_POSTER_RESULT_HIDDEN_CORRECTION")
    require(result["conclusion"]["style_capsule_promotion_allowed"] is False and result["conclusion"]["stable_baseline_replacement_allowed"] is False, "PAIR2_POSTER_RESULT_FALSE_PROMOTION")
    require(lock.get("p6_allowed") is False, "PAIR2_POSTER_RESULT_PREMATURE_P6_OPEN")


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
    expected_focus = "P1" if action.startswith("P1_") else "P6"
    require(lock["workflow"]["focus_stage"] == expected_focus and lock["workflow"]["status_authority"] == LOCK_PATH, "WORKFLOW_STAGE_DRIFT")

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
    if action in PAIR2_PREWRITE_ACTIONS:
        _validate_pair2_equal_budget_prewrite(root, lock, cp, action)
    if action == "RUN_PAIR2_COMPLETE_POSTER_INDEPENDENT_BLIND_EVALUATION_AND_RETURN_VERDICT":
        _validate_pair2_complete_poster_blind_package(root, lock, cp)
    if action == PAIR2_POSTER_BLIND_RESULT_ACTION:
        _validate_pair2_complete_poster_blind_result(root, lock, cp)
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
    elif action == "P1_PREPARE_TYPOGRAPHY_ONLY_DISTILLATION_REPAIR_BENCH":
        require(all(v == 1 for v in used.values()), "CORRECTION_NOT_COMPLETE")
        check_ref(root, lock["correction_pass_evidence"])
        check_ref(root, lock["final_validation_evidence"])
        check_ref(root, lock["human_set_verdict_evidence"])
        require(p6.get("formal_human_set_verdict") == "FAIL_TYPOGRAPHY_DISTILLATION_NOT_DEMONSTRATED", "HUMAN_VERDICT_MISSING")
        require(p6.get("status") == "HUMAN_FAIL_TYPOGRAPHY_PROGRAM_REPAIR_REQUIRED", "P6_HUMAN_FAIL_STATE")
        require(p6.get("final_pixel_validation_completed") is True, "FINAL_VALIDATION_NOT_COMPLETE")
    elif action == "P1_EXECUTE_TYPOGRAPHY_ONLY_TITLE_BENCH":
        require(all(v == 1 for v in used.values()), "CORRECTION_NOT_COMPLETE")
        check_ref(root, lock["human_set_verdict_evidence"])
        tr = lock.get("typography_repair", {})
        require(tr.get("status") == "PREPARED_TITLE_ONLY_BENCH_READY", "TYPOGRAPHY_BENCH_NOT_READY")
        require(tr.get("title_bench_render_allowed") is True, "TYPOGRAPHY_BENCH_RENDER_NOT_OPEN")
        check_ref(root, tr["bench_plan"])
        require(tr.get("phase") == "T1_TITLE_ONLY", "TYPOGRAPHY_BENCH_PHASE")
    elif action == "P1_WAIT_HUMAN_TITLE_BENCH_VERDICT":
        require(all(v == 1 for v in used.values()), "CORRECTION_NOT_COMPLETE")
        check_ref(root, lock["human_set_verdict_evidence"])
        tr = lock.get("typography_repair", {})
        require(tr.get("status") == "T1_EXECUTED_WAITING_HUMAN_BLIND_VERDICT", "TYPOGRAPHY_BENCH_EXECUTION_STATE")
        require(tr.get("phase") == "T1_TITLE_ONLY", "TYPOGRAPHY_BENCH_PHASE")
        require(tr.get("title_bench_render_allowed") is False, "TYPOGRAPHY_BENCH_SHOULD_BE_CLOSED")
        require(tr.get("human_blind_verdict") is None, "TYPOGRAPHY_BENCH_VERDICT_ALREADY_SET")
        require(tr.get("correction_passes_used") == {"豆坊": 1, "茶作": 1}, "TYPOGRAPHY_BENCH_CORRECTION_BUDGET")
        require(tr.get("blind_order_mapping_revealed") is False, "TYPOGRAPHY_BLIND_MAPPING_LEAK")
        check_ref(root, tr["bench_plan"])
        check_ref(root, tr["execution_evidence"])

    elif action == "P1_WAIT_HUMAN_TITLE_TECHNICAL_RETRY_VERDICT":
        tr = lock["typography_repair"]
        require(tr["status"] == "T1_TECHNICAL_RETRY_FROZEN_WAITING_HUMAN_REVIEW", "T1_RETRY_STATE")
        require(tr["title_bench_render_allowed"] is False and tr["support_typography_bench_allowed"] is False and tr["poster_reintegration_allowed"] is False, "T1_RETRY_BOUNDARY")
        require(tr["correction_passes_used"] == {"豆坊": 1, "茶作": 1}, "T1_AESTHETIC_HISTORY_CHANGED")
        for name in ("bench_plan", "execution_evidence", "human_verdict_evidence", "technical_retry_receipt", "glyphs_before", "glyphs_after", "tree_before", "tree_after"):
            check_ref(root, tr[name])
        verdict = read(root, tr["human_verdict_evidence"]["path"])
        require(verdict["glyph_correctness_verdict"] == "FAIL" and verdict["formal_title_gate"] == "NOT_PASS", "T1_HUMAN_FAIL_MISSING")
        require(tr["human_blind_verdict"] == {"design_sense": "B_ROUTE_DESIGN_SENSE_ADVANTAGE", "glyph_correctness": "FAIL", "title_gate": "NOT_PASS"}, "T1_HUMAN_VERDICT_DRIFT")
        validate_t1_retry_record(read(root, tr["technical_retry_receipt"]["path"]))
        before = read(root, tr["glyphs_before"]["path"])
        after = read(root, tr["glyphs_after"]["path"])
        for node_id in ("53:6", "53:9", "53:13", "53:16", "55:18", "55:21"):
            require(next(n for n in before if n["id"] == node_id) == next(n for n in after if n["id"] == node_id), "T1_FROZEN_VECTOR_CHANGED")
        tb, ta = (read(root, tr[k]["path"]) for k in ("tree_before", "tree_after"))
        require(tb[:2] == ta[:2], "T1_CANDIDATE1_TREE_CHANGED")
        require([{k: v for k, v in n.items() if k != "children"} for n in tb] == [{k: v for k, v in n.items() if k != "children"} for n in ta], "T1_FRAME_CHANGED")
        require(cp["typography_repair"] == tr, "T1_RETRY_CHECKPOINT_DRIFT")

    elif action == "P1_EXECUTE_WORDMARK_SYSTEM_REPAIR_V2":
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

    elif action == "P1_WAIT_HUMAN_WORDMARK_V2_VERDICT":
        tr = lock["typography_repair"]
        require(tr["status"] == "WORDMARK_V2_EXECUTED_WAITING_HUMAN_REVIEW", "WORDMARK_V2_WAIT_STATE")
        require(tr["wordmark_v2_render_allowed"] is False, "WORDMARK_V2_SHOULD_BE_FROZEN")
        require(tr["wordmark_v2_correction_passes_used"] == {"豆坊": 1, "茶作": 1}, "WORDMARK_V2_BUDGET")
        require(tr["wordmark_v2_human_verdict"] is None, "WORDMARK_V2_PREMATURE_VERDICT")
        require(tr["support_typography_bench_allowed"] is False and tr["poster_reintegration_allowed"] is False, "WORDMARK_V2_PREMATURE_ADVANCE")
        for name in ("final_t1_settlement", "wordmark_v2_plan", "wordmark_v2_execution"):
            check_ref(root, tr[name])

    elif action == "P1_EXECUTE_SEMANTIC_ANCHOR_WORDMARK_V3":
        tr = lock["typography_repair"]
        require(tr["status"] == "WORDMARK_V2_HUMAN_FAIL_SEMANTIC_ANCHOR_V3_READY", "WORDMARK_V3_READY_STATE")
        require(tr["phase"] == "SEMANTIC_ANCHOR_WORDMARK_V3", "WORDMARK_V3_PHASE")
        require(tr["wordmark_v3_render_allowed"] is True, "WORDMARK_V3_RENDER_NOT_OPEN")
        require(tr["support_typography_bench_allowed"] is False and tr["poster_reintegration_allowed"] is False, "WORDMARK_V3_PREMATURE_ADVANCE")
        require(tr["wordmark_v2_human_verdict"] == {"豆坊":"FAIL","茶作":"FAIL","overall":"FAIL_CONTINUE_TYPOGRAPHY_ONLY"}, "WORDMARK_V2_HUMAN_VERDICT_DRIFT")
        check_ref(root, tr["wordmark_v2_execution"])
        check_ref(root, tr["wordmark_v2_human_fail_and_v3_plan"])

    elif action == "P1_WAIT_HUMAN_SEMANTIC_ANCHOR_WORDMARK_V3_VERDICT":
        tr = lock["typography_repair"]
        require(tr["status"] == "SEMANTIC_ANCHOR_WORDMARK_V3_EXECUTED_WAITING_HUMAN_REVIEW", "WORDMARK_V3_EXECUTION_STATE")
        require(tr["phase"] == "SEMANTIC_ANCHOR_WORDMARK_V3", "WORDMARK_V3_PHASE")
        require(tr["wordmark_v3_render_allowed"] is False, "WORDMARK_V3_SHOULD_BE_FROZEN")
        require(tr["wordmark_v3_correction_passes_used"] == {"豆坊":1,"茶作":1}, "WORDMARK_V3_CORRECTION_BUDGET")
        require(tr["wordmark_v3_human_verdict"] is None, "WORDMARK_V3_PREMATURE_VERDICT")
        require(tr["support_typography_bench_allowed"] is False and tr["poster_reintegration_allowed"] is False, "WORDMARK_V3_PREMATURE_ADVANCE")
        require(tr["wordmark_v2_human_verdict"] == {"豆坊":"FAIL","茶作":"FAIL","overall":"FAIL_CONTINUE_TYPOGRAPHY_ONLY"}, "WORDMARK_V2_VERDICT_DRIFT")
        check_ref(root, tr["wordmark_v2_human_fail_and_v3_plan"])
        check_ref(root, tr["wordmark_v3_execution"])

    elif action == "P1_EXECUTE_STRUCTURAL_WORDMARK_V4":
        tr = lock["typography_repair"]
        require(tr["status"] == "WORDMARK_V3_DIRECTIONAL_IMPROVEMENT_V4_READY", "WORDMARK_V4_READY_STATE")
        require(tr["phase"] == "STRUCTURAL_WORDMARK_V4", "WORDMARK_V4_PHASE")
        require(tr["wordmark_v4_render_allowed"] is True, "WORDMARK_V4_RENDER_NOT_OPEN")
        require(tr["wordmark_v4_direction_budget"] == {"豆坊":3,"茶作":3}, "WORDMARK_V4_BUDGET")
        require(tr["wordmark_v3_human_verdict"] == {"豆坊":"IMPROVED_NOT_PASS","茶作":"IMPROVED_NOT_PASS","overall":"FAIL_FAR_FROM_SHANYEJI_CONTINUE_TYPOGRAPHY_ONLY"}, "WORDMARK_V3_HUMAN_VERDICT_DRIFT")
        require(tr["support_typography_bench_allowed"] is False and tr["poster_reintegration_allowed"] is False, "WORDMARK_V4_PREMATURE_ADVANCE")
        check_ref(root, tr["wordmark_v3_execution"])
        check_ref(root, tr["wordmark_v3_human_fail_and_v4_plan"])

    elif action == "P1_WAIT_HUMAN_STRUCTURAL_WORDMARK_V4_DIRECTION_VERDICT":
        tr = lock["typography_repair"]
        require(tr["status"] == "STRUCTURAL_WORDMARK_V4_EXECUTED_WAITING_HUMAN_DIRECTION_VERDICT", "WORDMARK_V4_EXECUTION_STATE")
        require(tr["phase"] == "STRUCTURAL_WORDMARK_V4", "WORDMARK_V4_PHASE")
        require(tr["wordmark_v4_render_allowed"] is False, "WORDMARK_V4_SHOULD_BE_FROZEN")
        require(tr["wordmark_v4_direction_budget"] == {"豆坊":3,"茶作":3}, "WORDMARK_V4_BUDGET")
        require(tr["wordmark_v4_visible_directions_generated"] == {"豆坊":3,"茶作":3}, "WORDMARK_V4_VISIBLE_COUNT")
        require(tr["wordmark_v4_hidden_variants"] == 0 and tr["wordmark_v4_preselection_polish_passes"] == 0, "WORDMARK_V4_HIDDEN_WORK")
        require(tr["wordmark_v4_selected_direction"] == {"豆坊":None,"茶作":None}, "WORDMARK_V4_PREMATURE_SELECTION")
        require(tr["support_typography_bench_allowed"] is False and tr["poster_reintegration_allowed"] is False, "WORDMARK_V4_PREMATURE_ADVANCE")
        require(tr["wordmark_v3_human_verdict"] == {"豆坊":"IMPROVED_NOT_PASS","茶作":"IMPROVED_NOT_PASS","overall":"FAIL_FAR_FROM_SHANYEJI_CONTINUE_TYPOGRAPHY_ONLY"}, "WORDMARK_V3_VERDICT_DRIFT")
        check_ref(root, tr["wordmark_v3_human_fail_and_v4_plan"])
        check_ref(root, tr["wordmark_v4_execution"])

    elif action == "P1_EXECUTE_GENERATIVE_CUSTOM_WORDMARK_EXPLORATION_V5":
        tr = lock["typography_repair"]
        require(tr["status"] == "WORDMARK_V4_HUMAN_NONE_GENERATIVE_V5_READY", "WORDMARK_V5_READY_STATE")
        require(tr["phase"] == "GENERATIVE_CUSTOM_WORDMARK_V5", "WORDMARK_V5_PHASE")
        require(tr["wordmark_v5_generation_allowed"] is True, "WORDMARK_V5_GENERATION_NOT_OPEN")
        require(tr["wordmark_v4_human_direction_verdict"] == {"豆坊":"NONE","茶作":"NONE","overall":"FAIL_ALL_V4_STRUCTURES_NO_DESIGN_SENSE"}, "WORDMARK_V4_HUMAN_VERDICT_DRIFT")
        require(tr["support_typography_bench_allowed"] is False and tr["poster_reintegration_allowed"] is False, "WORDMARK_V5_PREMATURE_ADVANCE")
        check_ref(root, tr["wordmark_v4_execution"])
        check_ref(root, tr["wordmark_v4_human_none_and_v5_plan"])

    elif action == "P1_WAIT_HUMAN_GENERATIVE_CUSTOM_WORDMARK_V5_DIRECTION_VERDICT":
        tr = lock["typography_repair"]
        require(tr["status"] == "GENERATIVE_CUSTOM_WORDMARK_V5_EXECUTED_WAITING_HUMAN_DIRECTION_VERDICT", "WORDMARK_V5_WAIT_STATE")
        require(tr["phase"] == "GENERATIVE_CUSTOM_WORDMARK_V5", "WORDMARK_V5_PHASE")
        require(tr["wordmark_v5_generation_allowed"] is False, "WORDMARK_V5_SHOULD_BE_FROZEN")
        require(tr["wordmark_v5_visible_concept_budget"] == {"豆坊":6,"茶作":6}, "WORDMARK_V5_BUDGET")
        require(tr["wordmark_v5_selected_direction"] == {"豆坊":None,"茶作":None}, "WORDMARK_V5_PREMATURE_SELECTION")
        require(tr["support_typography_bench_allowed"] is False and tr["poster_reintegration_allowed"] is False, "WORDMARK_V5_PREMATURE_ADVANCE")
        check_ref(root, tr["wordmark_v4_human_none_and_v5_plan"])
        check_ref(root, tr["wordmark_v5_execution"])

    elif action == "P1_EXECUTE_NONCALLIGRAPHIC_SEMANTIC_WORDMARK_V6":
        tr = lock["typography_repair"]
        require(tr["status"] == "GENERATIVE_V5_HUMAN_SELECTION_NONCALLIGRAPHIC_V6_READY", "WORDMARK_V6_READY_STATE")
        require(tr["phase"] == "NONCALLIGRAPHIC_SEMANTIC_WORDMARK_V6", "WORDMARK_V6_PHASE")
        require(tr["wordmark_v6_generation_allowed"] is True, "WORDMARK_V6_GENERATION_NOT_OPEN")
        require(tr["wordmark_v5_selected_direction"] == {"豆坊":"B","茶作":"D"}, "WORDMARK_V5_SELECTION_DRIFT")
        require(tr["wordmark_v5_selection_status"] == "SELECTED_AS_SEEDS_NOT_PASS", "WORDMARK_V5_FALSE_PASS")
        require(tr["support_typography_bench_allowed"] is False and tr["poster_reintegration_allowed"] is False, "WORDMARK_V6_PREMATURE_ADVANCE")
        check_ref(root, tr["wordmark_v5_execution"])
        check_ref(root, tr["wordmark_v5_human_selection_and_v6_plan"])

    elif action == "P1_VECTOR_RECONSTRUCT_V6_IN_FIGMA":
        tr = lock["typography_repair"]
        require(tr["status"] == "V6_DIRECTIONAL_POSITIVE_FIGMA_VECTOR_RECONSTRUCTION_READY", "V6_VECTOR_READY_STATE")
        require(tr["phase"] == "V6_FIGMA_VECTOR_RECONSTRUCTION", "V6_VECTOR_PHASE")
        require(tr["figma_vector_reconstruction_allowed"] is True, "V6_VECTOR_NOT_OPEN")
        require(tr["selected_direction"] == {"豆坊":"B","茶作":"D"}, "V6_SEED_SELECTION_DRIFT")
        require(tr["T2_allowed"] is False and tr["P6_reintegration_allowed"] is False, "V6_PREMATURE_ADVANCE")
        check_ref(root, tr["v6_execution"])

    elif action == "P1_WAIT_HUMAN_V6_FIGMA_VECTOR_REVIEW":
        tr = lock["typography_repair"]
        require(tr["status"] == "V6_FIGMA_VECTOR_RECONSTRUCTED_WAITING_HUMAN_REVIEW", "V6_VECTOR_REVIEW_STATE")
        require(tr["phase"] == "V6_FIGMA_VECTOR_REVIEW", "V6_VECTOR_REVIEW_PHASE")
        require(tr["figma_vector_reconstruction_allowed"] is False, "V6_VECTOR_RECONSTRUCTION_STILL_OPEN")
        require(tr["T2_allowed"] is False and tr["P6_reintegration_allowed"] is False, "V6_VECTOR_PREMATURE_ADVANCE")
        check_ref(root, tr["v6_execution"])
        check_ref(root, tr["v6_vector_reconstruction"])
        rec = read(root, tr["v6_vector_reconstruction"]["path"])
        require(rec["status"] == "EDITABLE_VECTOR_RECONSTRUCTION_COMPLETE_WAITING_HUMAN_REVIEW", "V6_VECTOR_RECORD_STATUS")
        require(rec["figma"]["page_id"] == "70:2", "V6_VECTOR_PAGE_DRIFT")
        require(rec["figma"]["editable_nodes"] == {"豆坊":"70:5","茶作字形":"70:7","茶作叶形":"70:9"}, "V6_VECTOR_NODE_DRIFT")
        require(rec["editability_readback_verified"] is True, "V6_VECTOR_EDITABILITY_UNVERIFIED")

    if action == "P1_PREPARE_HYBRID_TEXTURE_FINISH_PROBE":
        tr = lock["typography_repair"]
        require(lock["status"] == "VPD_P1_CHAZUO_V6_HIFI_SURFACE_HUMAN_FAIL_ROUTE_STOP", "CHAZUO_HIFI_ROUTE_STOP_STATE")
        require(tr.get("status") == "CHAZUO_V6_HIFI_SURFACE_HUMAN_FAIL_ROUTE_STOP", "CHAZUO_HIFI_TYPOGRAPHY_STATE")
        require(tr.get("phase") == "V6_SURFACE_ROUTE_RESET", "CHAZUO_HIFI_ROUTE_RESET_PHASE")
        require(tr.get("current_vector_only_surface_route") == "STOPPED_NOT_WORTH_CONTINUING", "CHAZUO_HIFI_ROUTE_NOT_STOPPED")
        require(tr.get("T2_allowed") is False and tr.get("P6_reintegration_allowed") is False, "CHAZUO_HIFI_PREMATURE_ADVANCE")
        check_ref(root, tr["v7_hifi_surface_test"])
        check_ref(root, tr["v7_hifi_surface_human_rejection"])

    if action == "P1_EXECUTE_TYPOGRAPHY_METHOD_SANDBOX_TEST_01":
        tr = lock["typography_repair"]
        require(lock["status"] == "VPD_P1_TYPOGRAPHY_METHOD_SANDBOX_READY", "TYPOGRAPHY_SANDBOX_NOT_READY")
        require(tr.get("status") == "TYPOGRAPHY_METHOD_SANDBOX_READY", "TYPOGRAPHY_SANDBOX_TYPOGRAPHY_STATE")
        require(tr.get("phase") == "TYPOGRAPHY_METHOD_SANDBOX", "TYPOGRAPHY_SANDBOX_PHASE")
        require(tr.get("sandbox_rule_promotion_allowed") is False, "TYPOGRAPHY_SANDBOX_PREMATURE_RULE_PROMOTION")
        require(tr.get("sandbox_first_test") == "TYP-M01", "TYPOGRAPHY_SANDBOX_FIRST_TEST_DRIFT")
        check_ref(root, tr["typography_method_research"])
        check_ref(root, tr["typography_method_sandbox_plan"])
        plan = read(root, tr["typography_method_sandbox_plan"]["path"])
        require(plan["status"] == "FROZEN_SANDBOX_PLAN_NOT_RULE", "TYPOGRAPHY_SANDBOX_PLAN_STATUS")
        require(plan["first_test"] == "TYP-M01", "TYPOGRAPHY_SANDBOX_PLAN_FIRST_TEST")
        require(plan["rule_admission"]["automatic_promotion"] is False, "TYPOGRAPHY_SANDBOX_AUTO_PROMOTION")
        require(tr.get("T2_allowed") is False and tr.get("P6_reintegration_allowed") is False, "TYPOGRAPHY_SANDBOX_PREMATURE_ADVANCE")

    if action == "P1_EXECUTE_TYPOGRAPHY_METHOD_SANDBOX_TEST_02":
        tr = lock["typography_repair"]
        require(lock["status"] == "VPD_P1_TYPOGRAPHY_METHOD_SANDBOX_TEST01_FAIL", "TYPOGRAPHY_SANDBOX_TEST02_NOT_READY")
        require(tr.get("status") == "TYPOGRAPHY_METHOD_SANDBOX_TEST01_FAIL", "TYPOGRAPHY_SANDBOX_TEST01_FAIL_STATE")
        require(tr.get("sandbox_test01_verdict") == "FAIL_NOT_READABLE_AS_CHA", "TYPOGRAPHY_SANDBOX_TEST01_VERDICT")
        require(tr.get("sandbox_rule_promotion_allowed") is False, "TYPOGRAPHY_SANDBOX_PREMATURE_RULE_PROMOTION")
        require(tr.get("sandbox_next_test") == "TYP-M02", "TYPOGRAPHY_SANDBOX_TEST02_DRIFT")
        check_ref(root, tr["typography_method_sandbox_plan"])
        check_ref(root, tr["sandbox_test01_evidence"])
        require(tr.get("T2_allowed") is False and tr.get("P6_reintegration_allowed") is False, "TYPOGRAPHY_SANDBOX_PREMATURE_ADVANCE")

    require(not set(cp["completed"]) & set(cp["incomplete"]), "COMPLETED_AND_INCOMPLETE")
    _validate_commercial_ledger(root, lock, cp)
    return lock, cp
