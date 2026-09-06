import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "evidence" / "vpd" / "shanyeji" / "controlled_family_attempt2"
CANDIDATE_PATH = (
    ROOT
    / "evidence"
    / "vpd"
    / "shanyeji"
    / "style_capsule_v1_1_candidate"
    / "STYLE_CAPSULE_V1_1_CANDIDATE.json"
)
POLICY_PATH = CANDIDATE_PATH.parent / "CAPSULE_LOCAL_CONTROLLED_VALIDATION_POLICY_V1.json"
V1_PATH = (
    ROOT
    / "evidence"
    / "vpd"
    / "shanyeji"
    / "style_capsule_v1"
    / "STYLE_CAPSULE_V1.json"
)
ATTEMPT1_DIR = ROOT / "evidence" / "vpd" / "shanyeji" / "controlled_family_generation_v1"
CHECKPOINT_PATH = ROOT / "continuity" / "vpd" / "LATEST_CHECKPOINT.json"
LEDGER_PATH = ROOT / "continuity" / "vpd" / "state_ledger" / "controlled_family_validation.jsonl"
ADAPTER_PATH = ROOT / "PROJECT_CONTROL_ADAPTER.json"
COMPILER_PATH = ROOT / "VISUAL_DISTILLATION_COMPILER_CONTRACT_V2.md"
SCHEMA_PATH = ROOT / "schemas" / "visual-program.v2.schema.json"

CANDIDATE_ID = "style_capsule_shanyeji_brand_editorial_v1_1_candidate"
CANDIDATE_SHA = "54bbc4a1eccd5e76d17dcb13b889c501ed93a4457dbbc1f8dc157572967a0cd9"
POLICY_ID = "style_capsule_shanyeji_brand_editorial_v1_1_candidate_controlled_validation_policy_v1"
POLICY_SHA = "fa46184715da92630d79bb556ed10c89b5543a36fec5d12eb1c7656f5f17eb8f"
V1_SHA = "f47023656ad0b5d2b0fe374bd90533f65987ef11175cded20ba37fdf82f3f8f1"
EXPERIMENT = "SHANYEJI_CONTROLLED_FAMILY_VALIDATION_ATTEMPT2"
ROUTE = "CHATGPT_UI_CONTROLLED_FAMILY_VALIDATION"
INPUT_HEAD = "bc15d1a2cf35f6deb2ba13c2cb72b035af1cd6bb"
STATE = "SHANYEJI_ATTEMPT2_PAYLOADS_FROZEN_CHATGPT_RENDER_NEXT"
NEXT_ACTION = (
    "RETURN_ATTEMPT2_CHATGPT_RENDER_HANDOFF_AND_GENERATE_EXACTLY_"
    "F1_F2_F3_ONCE_EACH_THEN_RUN_ATTEMPT2_HUMAN_PIXEL_REVIEW"
)
EVENT_ID = "EVT-VISUAL-VPD-SHANYEJI-ATTEMPT2-PAYLOAD-FREEZE-20260824-002"
EVENT_HASH = "2f799ec0cd3d82a0ab3ebf1b8f482cc7c636c705547f04b43592fb8c781f28f1"
DRIVE_FILE_ID = "1NZL-Jl6SvM-7TMHQOLeNUyj22jfQdx6e"

ARTIFACT_HASHES = {
    "ATTEMPT2_CONTROLLED_FAMILY_VALIDATION_PLAN_V1.json": "cd6d633cc63a3f9b92d1659f0cc6953c88b1ffeb07ee518d665286b49a878de0",
    "ATTEMPT2_OPERATOR_ISOLATION_MATRIX.json": "a8a1621ffd7d26438321e61c08fdb6d0d9bedd15591fe409ce50502cdbc42611",
    "ATTEMPT2_SURFACE_DIVERGENCE_MATRIX.json": "0dbae1012bd6bb74a9c8671a7413651a765c6428656db9a514d571e750f870aa",
    "F1_CONTROLLER_PAYLOAD.json": "edeb914f9febf2073cdda67da3ff282d27933f23f9c8d4a577ebc6ff5938df61",
    "F2_CONTROLLER_PAYLOAD.json": "7bba27202e8ba79a646fa17b74551dcc636e9eeb0c3d0b8d9c1545451a6e502e",
    "F3_CONTROLLER_PAYLOAD.json": "b48c6f31d56038d71522c6b6fc918f887750aff795f92e26c74cfac608822c05",
    "ATTEMPT2_HUMAN_PIXEL_REVIEW_PROTOCOL_V1.json": "9790fb50c346cadc40f37ffd093a9b5a12dcf49066865a36b4c38c0585f87f1a",
    "ATTEMPT2_PAYLOAD_FREEZE_RECEIPT_V1.json": "8ad807e9b6d6bb5ac8e149a87f1fbd0a648a7209cb8f33475c15ed79a5db86b2",
    "VPD_SHANYEJI_ATTEMPT2_CHATGPT_RENDER_HANDOFF_V1.txt": "2623e02f0ac431aefc83bbc4e75994e6bfce30006f2ed95c9c0e58020b5121df",
    "ATTEMPT2_DRIVE_HANDOFF_UPLOAD_RECEIPT_V1.json": "f790398ef9ef829e526a70b8311c67604d08e0a8bd6a0b90b1ba03912705b293",
}

PAYLOADS = {
    "SHY-FAM-V1-1-A2-F1": (
        "F1_CONTROLLER_PAYLOAD.json",
        ARTIFACT_HASHES["F1_CONTROLLER_PAYLOAD.json"],
        "3:4",
        ["TYPOGRAPHY_REBIND", "COPY_REBIND"],
        "SHY-FAM-V1-1-A2-F1.png",
    ),
    "SHY-FAM-V1-1-A2-F2": (
        "F2_CONTROLLER_PAYLOAD.json",
        ARTIFACT_HASHES["F2_CONTROLLER_PAYLOAD.json"],
        "3:4",
        ["CONTENT_SWAP", "PROCESS_TRANSFER", "MATERIAL_SHIFT"],
        "SHY-FAM-V1-1-A2-F2.png",
    ),
    "SHY-FAM-V1-1-A2-F3": (
        "F3_CONTROLLER_PAYLOAD.json",
        ARTIFACT_HASHES["F3_CONTROLLER_PAYLOAD.json"],
        "9:16",
        ["ASPECT_ADAPT", "DENSITY_SHIFT"],
        "SHY-FAM-V1-1-A2-F3.png",
    ),
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def payloads():
    return {
        experiment_id: load(DIR / values[0])
        for experiment_id, values in PAYLOADS.items()
    }


def test_all_attempt2_artifacts_are_parseable_and_exactly_hash_bound():
    for filename, expected_hash in ARTIFACT_HASHES.items():
        path = DIR / filename
        if path.suffix == ".json":
            load(path)
        assert sha256(path) == expected_hash


def test_immutable_authority_inputs_and_global_surfaces_are_unchanged():
    assert sha256(CANDIDATE_PATH) == CANDIDATE_SHA
    assert sha256(POLICY_PATH) == POLICY_SHA
    assert sha256(V1_PATH) == V1_SHA
    assert sha256(COMPILER_PATH) == (
        "d53a8485ebf3b449f261695d1602543303611bae899497d1bc401f8c23da79b4"
    )
    assert sha256(SCHEMA_PATH) == (
        "573314cd63d9f799107788e348d81a9ad8f1735976babeb6b0f9e7bde2f9f348"
    )
    expected_attempt1 = {
        "F1_CONTROLLER_PAYLOAD.json": "b63148048b536534fdc23da4865d976d644b072c2233b2ad9bb24ed67f79d2a7",
        "F2_CONTROLLER_PAYLOAD.json": "79353ff30b38aa66910806ea54afec5df91397d311abe769867770704065d2fd",
        "F3_CONTROLLER_PAYLOAD.json": "af690bdb927d9987d2a3b267fd55bbac543856e795890cc16e075c04a4ae8169",
        "ATTEMPT1_HUMAN_PIXEL_REVIEW_SETTLEMENT_V1.json": "70549b7e0bc307c16d0c228fac6d36ec25bc4b4cddeafeea173090e89f8709e9",
        "ATTEMPT1_FAILURE_EVIDENCE_REGISTRY_V1.json": "283fc7f3337d19caeeed652a80aebe79af746b55ed50adbd027461d9216e48c0",
    }
    for filename, expected_hash in expected_attempt1.items():
        assert sha256(ATTEMPT1_DIR / filename) == expected_hash


def test_plan_is_attempt2_controlled_validation_not_durable_proof():
    plan = load(DIR / "ATTEMPT2_CONTROLLED_FAMILY_VALIDATION_PLAN_V1.json")
    assert plan["input_remote_authority"]["remote_head"] == INPUT_HEAD
    assert plan["candidate_capsule"]["id"] == CANDIDATE_ID
    assert plan["candidate_capsule"]["sha256"] == CANDIDATE_SHA
    assert plan["candidate_capsule"]["modified"] is False
    assert plan["local_validation_policy"]["id"] == POLICY_ID
    assert plan["local_validation_policy"]["sha256"] == POLICY_SHA
    assert plan["experiment"]["name"] == EXPERIMENT
    assert plan["experiment"]["attempt_number"] == 2
    assert plan["experiment"]["generation_order"] == list(PAYLOADS)
    boundary = plan["pass_evidence_boundary"]
    assert boundary["single_surface_template_sufficient"] is False
    assert boundary["visual_similarity_sufficient"] is False
    assert boundary["mechanism_explanation_sufficiency_required"] is True
    assert boundary["classification"] == "CONTROLLED_VALIDATION_NOT_DURABLE_PROOF"
    assert boundary["commercial_quality"] == "NOT_YET"
    assert boundary["golden"] == "NO"
    assert boundary["scale"] == "BLOCKED_NOT_EXECUTED"


def test_operator_isolation_matrix_is_machine_readable_and_tier_exact():
    matrix = load(DIR / "ATTEMPT2_OPERATOR_ISOLATION_MATRIX.json")
    assert matrix["matrix_state"] == "FROZEN_PRE_RENDER"
    assert matrix["automatic_failure_rule"]["result"] == "OPERATOR_ISOLATION_FAILURE"
    assert len(matrix["tiers"]) == 3
    for tier in matrix["tiers"]:
        assert set(tier) >= {
            "experiment_id",
            "HELD_CONSTANTS",
            "CHANGED_VARIABLES",
            "PROHIBITED_LEAKAGE",
            "SURFACE_DOF_STRESSORS",
            "CAUSAL_ATTRIBUTION_LIMITS",
        }
        assert all(tier[key] for key in (
            "HELD_CONSTANTS",
            "CHANGED_VARIABLES",
            "PROHIBITED_LEAKAGE",
            "SURFACE_DOF_STRESSORS",
            "CAUSAL_ATTRIBUTION_LIMITS",
        ))
    f1, f2, f3 = matrix["tiers"]
    assert "WOK_ACTION" in f1["PROHIBITED_LEAKAGE"]
    assert "ACTIVE_CHINESE_WOK_COOKING_PROCESS" in f2["CHANGED_VARIABLES"]
    assert "F2_ACTIVE_CHINESE_WOK_COOKING_SUBJECT_AND_PROCESS_CLASS" in f3["HELD_CONSTANTS"]
    assert "ASPECT_RATIO_3_BY_4_TO_9_BY_16" in f3["CHANGED_VARIABLES"]


def test_surface_divergence_is_predeclared_before_render():
    matrix = load(DIR / "ATTEMPT2_SURFACE_DIVERGENCE_MATRIX.json")
    assert matrix["matrix_state"] == "FROZEN_PRE_RENDER"
    assert len(matrix["tracked_fields"]) == 9
    assert set(matrix["tiers"]) == set(PAYLOADS)
    f1 = matrix["tiers"]["SHY-FAM-V1-1-A2-F1"]
    f2 = matrix["tiers"]["SHY-FAM-V1-1-A2-F2"]
    f3 = matrix["tiers"]["SHY-FAM-V1-1-A2-F3"]
    assert f1["PHOTOGRAPHIC_SUBJECT_CLASS"] == "QUIET_DINING_PREP_INTERIOR_NO_ACTIVE_COOKING"
    assert f2["PHOTOGRAPHIC_SUBJECT_CLASS"] == "ACTIVE_WOK_COOKING_PROCESS"
    assert f3["PHOTOGRAPHIC_SUBJECT_CLASS"] == "SAME_ACTIVE_WOK_COOKING_PROCESS_AS_F2"
    assert f1["MOTIF_PRESENCE_OR_ABSENCE"] == f2["MOTIF_PRESENCE_OR_ABSENCE"] == f3["MOTIF_PRESENCE_OR_ABSENCE"] == "OMIT"
    interpretation = matrix["divergence_interpretation"]
    assert interpretation["surface_dof_variation_is_primary_operator_proof"] is False
    assert interpretation["single_obvious_template_sufficient_for_pass"] is False


def test_all_payloads_are_new_frozen_zero_reference_and_copy_exact():
    for experiment_id, payload in payloads().items():
        filename, expected_hash, aspect, operators, output = PAYLOADS[experiment_id]
        assert sha256(DIR / filename) == expected_hash
        assert payload["payload_state"] == "FROZEN"
        assert payload["experiment_name"] == EXPERIMENT
        assert payload["attempt_number"] == 2
        assert payload["experiment_id"] == experiment_id
        assert payload["candidate_capsule_id"] == CANDIDATE_ID
        assert payload["candidate_capsule_sha256"] == CANDIDATE_SHA
        assert payload["local_validation_policy_id"] == POLICY_ID
        assert payload["local_validation_policy_sha256"] == POLICY_SHA
        assert payload["route"] == ROUTE
        assert payload["reference_runtime_policy"] == "NONE"
        assert payload["reference_image_count"] == 0
        assert payload["aspect_intent"]["ratio"] == aspect
        assert payload["primary_operator_focus"] == operators
        assert payload["expected_output_filename"] == output
        copy = payload["literal_copy_to_render"]
        assert copy["main_chinese_title"] == "灶边味"
        assert copy["english_support_lines"] == ["WOK HEI", "MOUNTAIN KITCHEN"]
        assert copy["chinese_support_copy"] == "山野风味 · 现炒现做"
        assert copy["additional_copy_allowed"] is False
        assert payload["motif_policy"]["default"] == "OMIT"
        assert payload["graphic_accent_policy"]["default"] == "ABSENT"
        assert "GENERIC_BRUSH_CALLIGRAPHY_SHORTCUT" in payload["failure_conditions"]
        assert payload["mechanism_explanation_sufficiency"]["criterion"] == "MECHANISM_EXPLANATION_SUFFICIENCY"
        assert payload["independent_score_channels"]["cross_channel_compensation_allowed"] is False
        assert payload["output_count"] == 1
        assert payload["no_hidden_variants"] is True
        assert payload["no_best_of_n"] is True
        assert payload["no_aesthetic_retry_before_human_review"] is True
        for key in (
            "source_reference_pixels_provided_to_renderer",
            "attempt1_output_pixels_provided_to_renderer",
            "current_adhoc_poster_pixels_provided_to_renderer",
            "historical_lettering_pixels_provided_to_renderer",
        ):
            assert payload[key] is False


def test_f1_f2_f3_progression_enforces_isolation_and_structural_reflow():
    loaded = payloads()
    f1 = loaded["SHY-FAM-V1-1-A2-F1"]
    for code in (
        "VISIBLE_HUMAN_HAND_ACTIVELY_COOKING",
        "WOK_ACTION",
        "VISIBLE_FLAME_USED_AS_ACTION",
        "STEAM_OR_SMOKE_SPECTACLE",
    ):
        assert code in f1["PROHIBITED_LEAKAGE"]
    assert "no active cooking" in f1["photographic_subject_direction"].lower()
    f2 = loaded["SHY-FAM-V1-1-A2-F2"]
    assert "ACTIVE_CHINESE_WOK_COOKING_PROCESS" in f2["CHANGED_VARIABLES"]
    assert f2["relation_topology"]["comparison_binding"] == (
        "SAME_GENERAL_RELATION_GRAPH_AS_F1_FOR_OPERATOR_ISOLATION"
    )
    f3 = loaded["SHY-FAM-V1-1-A2-F3"]
    assert f3["same_subject_process_contract"]["new_subject_or_process_class_allowed"] is False
    assert f3["structural_aspect_reflow_contract"]["required_operation"] == (
        "ZONE_REALLOCATION_AND_RELATION_REFLOW"
    )
    assert f3["relation_topology"]["f2_screen_coordinates_retained"] is False
    assert f3["relation_topology"]["simple_title_above_or_below_same_composition"] is False


def test_handoff_has_exact_hashes_serial_order_and_complete_renderer_text():
    handoff = (DIR / "VPD_SHANYEJI_ATTEMPT2_CHATGPT_RENDER_HANDOFF_V1.txt").read_text(
        encoding="utf-8"
    )
    assert "It is Attempt 2, not a retry, mutation or continuation of Attempt 1." in handoff
    assert "Generate in this exact serial order: F1 -> F2 -> F3." in handoff
    assert "Reference runtime policy: NONE" in handoff
    assert "Reference image count: 0" in handoff
    assert "Do not use any runtime reference image." in handoff
    assert "Do not use OpenAI API, API keys, WIF, OIDC, private renderer" in handoff
    assert handoff.count("Complete renderer-readable textual serialization:") == 3
    for experiment_id, payload in payloads().items():
        filename, expected_hash, _, _, output = PAYLOADS[experiment_id]
        assert experiment_id in handoff
        assert filename in handoff
        assert expected_hash in handoff
        assert output in handoff
        assert payload["renderer_instruction"] in handoff


def test_review_protocol_separates_realism_and_family_mechanisms():
    protocol = load(DIR / "ATTEMPT2_HUMAN_PIXEL_REVIEW_PROTOCOL_V1.json")
    assert protocol["authority"]["final_aesthetic_authority"] == "HUMAN"
    assert protocol["authority"]["codex_final_aesthetic_score_authorized"] is False
    channels = protocol["independent_score_channels"]
    assert set(channels) == {
        "TECHNICAL_PHOTOGRAPHIC_REALISM",
        "FAMILY_MECHANISM_VALIDATION",
    }
    assert channels["TECHNICAL_PHOTOGRAPHIC_REALISM"]["can_compensate_for_family_mechanism_failure"] is False
    assert channels["FAMILY_MECHANISM_VALIDATION"]["can_be_compensated_by_technical_realism"] is False
    assert protocol["mechanism_explanation_sufficiency"]["criterion"] == "MECHANISM_EXPLANATION_SUFFICIENCY"
    assert set(protocol["permitted_final_verdicts"]) == {
        "ATTEMPT2_FAMILY_VALIDATION_PASS",
        "ATTEMPT2_FAMILY_VALIDATION_PASS_WITH_REVISIONS",
        "ATTEMPT2_FAMILY_VALIDATION_FAIL",
    }
    assert protocol["promotion_boundary"]["commercial_promotion_in_same_review"] is False


def test_freeze_and_drive_receipts_bind_exact_artifacts():
    receipt = load(DIR / "ATTEMPT2_PAYLOAD_FREEZE_RECEIPT_V1.json")
    assert receipt["input_remote_authority"]["remote_head"] == INPUT_HEAD
    assert receipt["candidate_capsule"]["sha256_before"] == CANDIDATE_SHA
    assert receipt["candidate_capsule"]["sha256_after"] == CANDIDATE_SHA
    assert receipt["candidate_capsule"]["modified"] is False
    assert receipt["local_validation_policy"]["sha256_before"] == POLICY_SHA
    assert receipt["local_validation_policy"]["modified"] is False
    assert receipt["immutable_v1_baseline"]["sha256_before"] == V1_SHA
    assert receipt["immutable_v1_baseline"]["modified"] is False
    bound = {item["experiment_id"]: item for item in receipt["frozen_payloads"]}
    assert set(bound) == set(PAYLOADS)
    for experiment_id, (filename, expected_hash, _, _, output) in PAYLOADS.items():
        assert bound[experiment_id]["sha256"] == expected_hash
        assert bound[experiment_id]["byte_length"] == (DIR / filename).stat().st_size
        assert bound[experiment_id]["expected_output_filename"] == output
    assertions = receipt["execution_assertions"]
    assert assertions["codex_image_generation_executed"] is False
    assert assertions["style_capsule_v1_1_candidate_modified"] is False
    global_surfaces = receipt["global_compiler_and_schema"]
    assert global_surfaces["compiler_modified"] is False
    assert global_surfaces["schema_modified"] is False
    assert receipt["next_required_action"] == NEXT_ACTION

    drive = load(DIR / "ATTEMPT2_DRIVE_HANDOFF_UPLOAD_RECEIPT_V1.json")
    assert drive["status"] == "PASS"
    handoff = drive["render_handoff"]
    assert handoff["drive_file_id"] == DRIVE_FILE_ID
    assert handoff["local_sha256"] == sha256(DIR / handoff["filename"])
    assert handoff["local_byte_length"] == handoff["drive_reported_byte_length"]
    assert handoff["readback_verified"] is True
    assert all(drive["readback_checks"].values())


def test_checkpoint_ledger_and_adapter_promote_attempt2_without_rollback():
    checkpoint = load(CHECKPOINT_PATH)
    # Sequence 18 is historical Attempt-2 freeze evidence. Forward-only
    # project contracts may advance the current checkpoint without rewriting
    # this event or making its consumed handoff current again.
    assert checkpoint["sequence"] >= 18
    tail = checkpoint["ledger_tails"]["controlled_family_validation"]
    assert tail == {"event_id": EVENT_ID, "event_hash": EVENT_HASH}

    events = [
        json.loads(line)
        for line in LEDGER_PATH.read_text(encoding="utf-8").splitlines()
    ]
    assert len(events) == 2
    event = events[-1]
    assert event["event_id"] == EVENT_ID
    assert event["event_hash"] == EVENT_HASH
    assert event["previous_event_id"] == events[-2]["event_id"]
    assert event["previous_event_hash"] == events[-2]["event_hash"]
    asserted = dict(event)
    asserted_hash = asserted.pop("event_hash")
    canonical = json.dumps(
        asserted, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    assert hashlib.sha256(canonical).hexdigest() == asserted_hash
    assert event["after"]["generated_outputs"] == 0
    assert event["after"]["human_pixel_review"] == "PENDING_GENERATION"

    adapter = load(ADAPTER_PATH)
    for authority_name in (
        "state_authorities",
        "task_authorities",
        "acceptance_authorities",
    ):
        priorities = [item["priority"] for item in adapter[authority_name]]
        assert priorities == list(range(1, len(priorities) + 1))
    tasks = {item["path"]: item for item in adapter["task_authorities"]}
    handoff_path = (
        "evidence/vpd/shanyeji/controlled_family_attempt2/"
        "VPD_SHANYEJI_ATTEMPT2_CHATGPT_RENDER_HANDOFF_V1.txt"
    )
    assert handoff_path in tasks
    assert "historical consumed" in tasks[handoff_path]["purpose"]
    adapter_ref = next(
        item
        for item in checkpoint["source_state_refs"]
        if item.get("path") == "PROJECT_CONTROL_ADAPTER.json"
    )
    assert adapter_ref["sha256"] == sha256(ADAPTER_PATH)


def test_preparation_created_no_images_or_renderer_route():
    image_suffixes = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
    assert [path for path in DIR.iterdir() if path.suffix.lower() in image_suffixes] == []
    receipt = load(DIR / "ATTEMPT2_PAYLOAD_FREEZE_RECEIPT_V1.json")
    assertions = receipt["execution_assertions"]
    for key in (
        "codex_image_generation_executed",
        "image_editing_executed",
        "attempt1_assets_modified",
        "style_capsule_v1_modified",
        "style_capsule_v1_1_candidate_modified",
        "openai_api_used",
        "api_key_used",
        "wif_used",
        "oidc_used",
        "private_or_external_renderer_used",
        "renderer_infrastructure_built",
        "commercial_executed",
        "golden_executed",
        "scale_executed",
    ):
        assert assertions[key] is False


def main():
    tests = [
        value
        for name, value in sorted(globals().items())
        if name.startswith("test_") and callable(value)
    ]
    for test in tests:
        test()
    print(
        "SHANYEJI_ATTEMPT2_CONTROLLED_FAMILY_DESIGN_AND_FREEZE_V1_"
        f"VALIDATION_PASS tests={len(tests)}"
    )


if __name__ == "__main__":
    main()
