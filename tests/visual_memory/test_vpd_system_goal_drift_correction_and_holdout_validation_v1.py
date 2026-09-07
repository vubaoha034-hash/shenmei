from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DIR = (
    ROOT
    / "evidence"
    / "vpd"
    / "shanyeji"
    / "system_level_holdout_validation_v1"
)
DRIFT_PATH = DIR / "PROJECT_GOAL_DRIFT_CORRECTION_RECORD_V1.json"
PLAN_PATH = DIR / "SYSTEM_LEVEL_HOLDOUT_VALIDATION_PLAN_V1.json"
MATRIX_PATH = DIR / "HOLDOUT_CHALLENGE_MATRIX.json"
PROTOCOL_PATH = DIR / "HOLDOUT_EVALUATION_PROTOCOL_V1.json"
ANCHOR_PATH = DIR / "VISUAL_ANCHOR_RUNTIME_POLICY_RECONCILIATION_V1.json"
ADAPTER_PATH = ROOT / "PROJECT_CONTROL_ADAPTER.json"
CHECKPOINT_PATH = ROOT / "continuity" / "vpd" / "LATEST_CHECKPOINT.json"
LEDGER_PATH = ROOT / "continuity" / "vpd" / "state_ledger" / "system_validation.jsonl"

NEXT_ACTION = "RETURN_TO_CHATGPT_FOR_FORMAL_RENDER_ATTEMPT2_H1_H2_H3_H4"
HISTORICAL_NEXT_ACTION = "RETURN_TO_CHATGPT_FOR_EXACT_VISUAL_ANCHOR_RUNTIME_AUTHORIZATION"
STATE = "VPD_FORMAL_RENDER_ATTEMPT1_INVALID_ATTEMPT2_READY_FOR_CHATGPT_RENDER"
EVENT_ID = "EVT-VISUAL-VPD-SYSTEM-GOAL-DRIFT-CORRECTION-HOLDOUT-20260907-001"
EVENT_HASH = "30e17399af34ace062fb32da02594863833efda20cda202b50e118e771519928"
CANONICAL_SHA = "9a29fbdc7dd908017924bed270e8dfe18351519eed3fa7bc7001789f2a383414"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_exact_drive_authority_and_original_vpd_goal_are_recorded():
    drift = load(DRIFT_PATH)
    source = drift["source_authority"]
    assert source["drive_file_id"] == "1HRjbFI9_8yWbtEPjPQ0ebKvlRPXjlklc"
    assert source["title"] == (
        "VPD_CODEX_SYSTEM_GOAL_DRIFT_CORRECTION_AND_HOLDOUT_VALIDATION_V1.txt"
    )
    assert source["full_text_read"] is True
    assert "STRONG_VISUAL_MODEL" in drift["original_vpd_objective"]
    correction = drift["drift_correction"]
    assert correction["photo_figma_pipeline_role"] == (
        "DOWNSTREAM_PRODUCTION_PIPELINE_AFTER_VISUAL_DIRECTION_ACCEPTANCE"
    )
    assert correction["single_poster_figma_optimization_as_current_goal"] == "STOPPED"
    figma = drift["existing_figma_v3_v6_classification"]
    assert figma["classification"] == "DIAGNOSTIC_PRODUCTION_PIPELINE_EVIDENCE"
    assert figma["style_capsule_promotion_evidence"] is False
    assert figma["figma_metadata_fabricated"] is False


def test_holdout_plan_is_system_level_and_not_an_attempt3_polish_loop():
    plan = load(PLAN_PATH)
    assert plan["task_id"] == "VPD-SYSTEM-LEVEL-HOLDOUT-TRANSFER-VALIDATION-V1"
    assert plan["validation_mode"] == "SYSTEM_LEVEL_HOLDOUT_TRANSFER"
    assert plan["not_an_attempt3_poster_polish_loop"] is True
    assert plan["challenge_order"] == ["H1", "H2", "H3", "H4"]
    assert plan["candidate"]["promoted_by_this_plan"] is False
    assert plan["visual_anchor_runtime_policy"] == (
        "VISUAL_ANCHOR_RUNTIME_AUTHORITY_MISSING"
    )
    assert plan["payload_freeze_gate"]["payloads_created"] is False
    assert plan["future_run_requirements"]["figma_is_zero_to_one_art_director"] is False
    assert plan["next_action_if_authority_missing"] == HISTORICAL_NEXT_ACTION


def test_exact_four_holdouts_and_h3_h4_isolation_are_predeclared():
    matrix = load(MATRIX_PATH)
    assert matrix["challenge_count"] == 4
    assert list(matrix["challenges"]) == ["H1", "H2", "H3", "H4"]
    h1, h2, h3, h4 = (matrix["challenges"][key] for key in ("H1", "H2", "H3", "H4"))
    assert h1["communication_job"] == {
        "main_title": "晨席",
        "english_support": "MORNING TABLE",
        "chinese_support": "山野早餐 · 当日鲜作",
    }
    assert h2["communication_job"]["main_title"] == "山菌"
    assert h3["communication_job"]["main_title"] == "豆坊"
    assert h3["communication_job"] == h4["communication_job"]
    assert h3["subject_process_class_id"] == h4["subject_process_class_id"]
    assert h3["aspect"] == "3:4"
    assert h4["aspect"] == "9:16"
    assert h4["operators_under_test"][0] == "ASPECT_ADAPT"
    assert set(h4["hard_failures"]) >= {
        "CROP_ONLY",
        "STRETCH_ONLY",
        "STACK_ONLY",
        "GENERIC_CENTERED_VERTICAL_POSTER",
        "NEW_DECORATIVE_FILLER_FOR_VERTICAL_SPACE",
    }
    assert matrix["cross_challenge_rules"]["reuse_attempt1_or_attempt2_payloads"] is False
    assert matrix["cross_challenge_rules"]["payloads_created"] is False


def test_evaluation_channels_separate_quality_mechanism_copy_template_and_reflow():
    protocol = load(PROTOCOL_PATH)
    assert set(protocol["evaluation_channels"]) == {
        "A_FRESH_BLIND_PIXEL_EVALUATION",
        "B_FRESH_REFERENCE_AWARE_FAMILY_EVALUATION",
        "C_FRESH_MECHANISM_CONTRACT_EVALUATION",
        "D_HUMAN_PIXEL_REVIEW",
    }
    assert set(protocol["separate_required_score_channels"]) == {
        "ABSOLUTE_COMMERCIAL_PIXEL_QUALITY",
        "VPD_FAMILY_MECHANISM_TRANSFER",
        "NEWNESS_LITERAL_COPY_RISK",
        "TEMPLATE_COLLAPSE_RISK",
        "H4_ASPECT_REFLOW",
    }
    assert protocol["evaluation_channels"]["D_HUMAN_PIXEL_REVIEW"]["authority"] == (
        "HUMAN_FINAL_AESTHETIC_AUTHORITY"
    )
    rules = protocol["set_level_verdict_rules"]
    assert rules["one_image_pass_cannot_pass_set"] is True
    assert rules["similarity_only_cannot_pass_set"] is True
    assert rules["commercial_golden_scale_promotion_authorized"] is False


def test_visual_anchor_policy_fails_closed_on_distillation_only_authority():
    policy = load(ANCHOR_PATH)
    assert policy["result"] == "VISUAL_ANCHOR_RUNTIME_AUTHORITY_MISSING"
    missing = policy["missing_authorization"]["exact_required_user_authorization"]
    assert "R1C-APPROVED-SHANYEJI-CANONICAL.jpg" in missing
    assert "1fG2OQ7IphZfGnH1csu1qZKYCsyAMDOAZ" in missing
    assert CANONICAL_SHA in missing
    minimum = policy["minimum_lawful_runtime_anchor_set_if_future_authorized"]
    assert minimum["count"] == 1
    assert minimum["anchors"][0]["sha256"] == CANONICAL_SHA
    assert minimum["attempt1_or_attempt2_outputs_allowed"] is False
    assert minimum["current_zaobianwei_or_figma_variants_allowed"] is False
    assert policy["current_boundary"]["renderer_payloads_created"] is False
    assert policy["current_boundary"]["next_action"] == HISTORICAL_NEXT_ACTION


def test_adapter_checkpoint_and_ledger_restore_system_goal():
    adapter = load(ADAPTER_PATH)
    system = adapter["vpd_system_goal_authority"]
    assert system["active_task_id"] == "VPD-SYSTEM-LEVEL-HOLDOUT-TRANSFER-VALIDATION-V1"
    assert system["checkpoint"] == STATE
    assert system["challenge_ids"] == ["H1", "H2", "H3", "H4"]
    assert system["visual_anchor_runtime_policy"] == "AUTHORIZED_FOR_THIS_HOLDOUT_RUN"
    assert system["formal_outputs_generated"] == "0/4"
    assert system["payload_ids_frozen"] == [
        "SHY-SYS-HOLDOUT-V1-H1",
        "SHY-SYS-HOLDOUT-V1-H2",
        "SHY-SYS-HOLDOUT-V1-H3",
        "SHY-SYS-HOLDOUT-V1-H4",
    ]
    assert system["next_required_action"] == NEXT_ACTION
    pipeline = adapter["forward_commercial_pipeline"]
    assert pipeline["role"] == (
        "DOWNSTREAM_PRODUCTION_PIPELINE_AFTER_VISUAL_DIRECTION_ACCEPTANCE"
    )
    assert pipeline["highest_active_project_objective"] is False
    for authority_name in ("state_authorities", "task_authorities", "acceptance_authorities"):
        priorities = [item["priority"] for item in adapter[authority_name]]
        assert priorities == list(range(1, len(priorities) + 1))

    checkpoint = load(CHECKPOINT_PATH)
    assert checkpoint["sequence"] == 22
    assert checkpoint["status"] == STATE
    assert checkpoint["highest_accepted_checkpoint"] == STATE
    assert checkpoint["active_task_ids"] == [
        "VPD-SYSTEM-LEVEL-HOLDOUT-TRANSFER-VALIDATION-V1"
    ]
    assert checkpoint["next_required_action"] == NEXT_ACTION
    assert checkpoint["ledger_tails"]["system_validation"] == {
        "event_id": "EVT-VISUAL-VPD-FORMAL-RENDER-ATTEMPT1-INVALID-ATTEMPT2-READY-20260907-001",
        "event_hash": "2aac3fe5ba3cfe5813538edf25ff96feac722e2204749c70b389fc4b1570146c",
    }

    events = [json.loads(line) for line in LEDGER_PATH.read_text(encoding="utf-8").splitlines()]
    assert len(events) == 3
    event = events[2]
    asserted = dict(event)
    asserted_hash = asserted.pop("event_hash")
    canonical = json.dumps(
        asserted, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    assert event["event_id"] == "EVT-VISUAL-VPD-FORMAL-RENDER-ATTEMPT1-INVALID-ATTEMPT2-READY-20260907-001"
    assert asserted_hash == "2aac3fe5ba3cfe5813538edf25ff96feac722e2204749c70b389fc4b1570146c"
    assert hashlib.sha256(canonical).hexdigest() == asserted_hash


def test_historical_authorities_and_downstream_pipeline_are_immutable():
    expected = {
        ROOT / "VISUAL_DISTILLATION_COMPILER_CONTRACT_V2.md": "d53a8485ebf3b449f261695d1602543303611bae899497d1bc401f8c23da79b4",
        ROOT / "schemas" / "visual-program.v2.schema.json": "573314cd63d9f799107788e348d81a9ad8f1735976babeb6b0f9e7bde2f9f348",
        ROOT / "evidence" / "vpd" / "shanyeji" / "style_capsule_v1" / "STYLE_CAPSULE_V1.json": "f47023656ad0b5d2b0fe374bd90533f65987ef11175cded20ba37fdf82f3f8f1",
        ROOT / "evidence" / "vpd" / "shanyeji" / "style_capsule_v1_1_candidate" / "STYLE_CAPSULE_V1_1_CANDIDATE.json": "54bbc4a1eccd5e76d17dcb13b889c501ed93a4457dbbc1f8dc157572967a0cd9",
        ROOT / "evidence" / "vpd" / "shanyeji" / "controlled_family_attempt2" / "F1_CONTROLLER_PAYLOAD.json": "edeb914f9febf2073cdda67da3ff282d27933f23f9c8d4a577ebc6ff5938df61",
        ROOT / "evidence" / "vpd" / "shanyeji" / "controlled_family_attempt2" / "F2_CONTROLLER_PAYLOAD.json": "7bba27202e8ba79a646fa17b74551dcc636e9eeb0c3d0b8d9c1545451a6e502e",
        ROOT / "evidence" / "vpd" / "shanyeji" / "controlled_family_attempt2" / "F3_CONTROLLER_PAYLOAD.json": "b48c6f31d56038d71522c6b6fc918f887750aff795f92e26c74cfac608822c05",
        ROOT / "evidence" / "vpd" / "shanyeji" / "controlled_family_attempt2" / "ATTEMPT2_HUMAN_FINAL_SETTLEMENT_20260825.json": "683c0d9991c54a960de7eff4ebceccefbf95d18f35a683d3af85e088501210a1",
        ROOT / "contracts" / "vpd" / "PHOTO_ONLY_RENDER_CONTRACT_V1.json": "e9fb29a2d91acd1312787dca67daf602d4fbd8a81492ec9d20bc435be4586a66",
        ROOT / "contracts" / "vpd" / "FIGMA_COMPOSITION_CONTRACT_V1.json": "a2d59629041ae9b43a357025efaf7fca34e33691b8f11b30eee4ae99a9c0a309",
        ROOT / "contracts" / "vpd" / "COMMERCIAL_DESIGN_GATE_POLICY_V1.json": "6eadc9a5ea1c82ae7904d79d3c7b33b272d6d10887b9650267ac41f5f672641f",
    }
    for path, expected_hash in expected.items():
        assert sha256(path) == expected_hash


def test_current_task_created_no_pixels_figma_or_renderer_payloads():
    forbidden_suffixes = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".fig"}
    assert [path for path in DIR.rglob("*") if path.suffix.lower() in forbidden_suffixes] == []
    assert sorted(path.name for path in DIR.glob("H[1-4]_CONTROLLER_PAYLOAD.json")) == [
        "H1_CONTROLLER_PAYLOAD.json",
        "H2_CONTROLLER_PAYLOAD.json",
        "H3_CONTROLLER_PAYLOAD.json",
        "H4_CONTROLLER_PAYLOAD.json",
    ]
    for path in (DRIFT_PATH, PLAN_PATH, MATRIX_PATH, PROTOCOL_PATH, ANCHOR_PATH):
        assert load(path)["artifact_type"]
