import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]
CANDIDATE_DIR = (
    ROOT / "evidence" / "vpd" / "shanyeji" / "style_capsule_v1_1_candidate"
)
ATTEMPT1_DIR = (
    ROOT / "evidence" / "vpd" / "shanyeji" / "controlled_family_generation_v1"
)
V1_PATH = (
    ROOT
    / "evidence"
    / "vpd"
    / "shanyeji"
    / "style_capsule_v1"
    / "STYLE_CAPSULE_V1.json"
)
CANDIDATE_PATH = CANDIDATE_DIR / "STYLE_CAPSULE_V1_1_CANDIDATE.json"
IDENTITY_PATH = CANDIDATE_DIR / "CAPSULE_V1_1_CANDIDATE_IDENTITY.json"
DELTA_PATH = CANDIDATE_DIR / "CAPSULE_V1_1_REFINEMENT_DELTA_V1.json"
POLICY_PATH = CANDIDATE_DIR / "CAPSULE_LOCAL_CONTROLLED_VALIDATION_POLICY_V1.json"
RECEIPT_PATH = CANDIDATE_DIR / "STYLE_CAPSULE_V1_1_CANDIDATE_CREATION_RECEIPT.json"
SCHEMA_PATH = ROOT / "schemas" / "visual-program.v2.schema.json"
COMPILER_PATH = ROOT / "VISUAL_DISTILLATION_COMPILER_CONTRACT_V2.md"
CHECKPOINT_PATH = ROOT / "continuity" / "vpd" / "LATEST_CHECKPOINT.json"
LEDGER_PATH = ROOT / "continuity" / "vpd" / "state_ledger" / "distillation_evidence.jsonl"
ADAPTER_PATH = ROOT / "PROJECT_CONTROL_ADAPTER.json"

CANDIDATE_ID = "style_capsule_shanyeji_brand_editorial_v1_1_candidate"
CANDIDATE_VERSION = "1.1.0-candidate"
V1_ID = "style_capsule_shanyeji_brand_editorial_v1"
V1_SHA = "f47023656ad0b5d2b0fe374bd90533f65987ef11175cded20ba37fdf82f3f8f1"
INPUT_HEAD = "f9c94db0251c654a19129f8aaa1c2c1128a21a97"
NEXT_ACTION = (
    "DESIGN_AND_FREEZE_ATTEMPT2_CONTROLLED_FAMILY_VALIDATION_FROM_"
    "SHANYEJI_STYLE_CAPSULE_V1_1_CANDIDATE"
)
STATE = "STYLE_CAPSULE_V1_1_CANDIDATE_CREATED_ATTEMPT2_CONTROLLED_VALIDATION_NEXT"
EVENT_ID = "EVT-VISUAL-VPD-SHANYEJI-STYLE-CAPSULE-V1-1-CANDIDATE-20260821-003"
EVENT_HASH = "ec09bf7fe4a133d8d74dce48a18d045824784dc7eb6e6d9ec2208b2a1efdb418"
ARTIFACT_HASHES = {
    CANDIDATE_PATH: "54bbc4a1eccd5e76d17dcb13b889c501ed93a4457dbbc1f8dc157572967a0cd9",
    IDENTITY_PATH: "7c79aa39f5e3bd94547749a2277c54623a8d1a0087d236c742b332df7c51fc21",
    DELTA_PATH: "2f9e90d81eabf5fd5cfa97711dfa248baef7d12c88164b988a6a3252338b7763",
    POLICY_PATH: "fa46184715da92630d79bb556ed10c89b5543a36fec5d12eb1c7656f5f17eb8f",
    RECEIPT_PATH: "21385719bea8805bc2bb2be40b92014b4367d43bfb6a4ce4972805cb8e126351",
}
INPUT_HASHES = {
    ATTEMPT1_DIR / "ATTEMPT1_HUMAN_PIXEL_REVIEW_SETTLEMENT_V1.json": (
        "70549b7e0bc307c16d0c228fac6d36ec25bc4b4cddeafeea173090e89f8709e9"
    ),
    ATTEMPT1_DIR / "ATTEMPT1_FAILURE_EVIDENCE_REGISTRY_V1.json": (
        "283fc7f3337d19caeeed652a80aebe79af746b55ed50adbd027461d9216e48c0"
    ),
    ATTEMPT1_DIR / "STYLE_CAPSULE_V1_1_REFINEMENT_REQUIREMENTS_V1.json": (
        "6ae57ac7cb13074d2e99205f69055850e2bc686ee89ab8050f5ebc3223f6709f"
    ),
    ATTEMPT1_DIR / "ATTEMPT1_SETTLEMENT_RECEIPT_V1.json": (
        "4e899123162c24a859dacad4a744997027dd45e43d866e95b35f2393df5bd6dd"
    ),
    ATTEMPT1_DIR / "F1_CONTROLLER_PAYLOAD.json": (
        "b63148048b536534fdc23da4865d976d644b072c2233b2ad9bb24ed67f79d2a7"
    ),
    ATTEMPT1_DIR / "F2_CONTROLLER_PAYLOAD.json": (
        "79353ff30b38aa66910806ea54afec5df91397d311abe769867770704065d2fd"
    ),
    ATTEMPT1_DIR / "F3_CONTROLLER_PAYLOAD.json": (
        "af690bdb927d9987d2a3b267fd55bbac543856e795890cc16e075c04a4ae8169"
    ),
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_all_candidate_artifacts_are_parseable_hash_bound_and_schema_valid():
    for path, expected_hash in ARTIFACT_HASHES.items():
        load(path)
        assert sha256(path) == expected_hash
    schema = load(SCHEMA_PATH)
    candidate = load(CANDIDATE_PATH)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(candidate)
    assert candidate["program_id"] == CANDIDATE_ID
    assert candidate["version"] == "2.0.0"
    assert candidate["status"] == "BENCHMARKING"


def test_candidate_identity_has_exact_semantic_version_and_immutable_lineage():
    identity = load(IDENTITY_PATH)
    assert identity["candidate_id"] == CANDIDATE_ID
    assert identity["candidate_semantic_version"] == CANDIDATE_VERSION
    assert identity["candidate_artifact"]["sha256"] == sha256(CANDIDATE_PATH)
    assert identity["semantic_version_boundary"] == {
        "capsule_semantic_version": CANDIDATE_VERSION,
        "visual_program_schema_version": "2.0.0",
        "versions_are_independent": True,
    }
    baseline = identity["lineage"]["immutable_baseline_v1"]
    assert baseline["id"] == V1_ID
    assert baseline["sha256"] == sha256(V1_PATH) == V1_SHA
    assert baseline["immutable"] is True
    assert baseline["modified"] is False
    assert identity["lineage"]["attempt1_human_settlement"]["sha256"] == (
        INPUT_HASHES[ATTEMPT1_DIR / "ATTEMPT1_HUMAN_PIXEL_REVIEW_SETTLEMENT_V1.json"]
    )
    assert identity["lineage"]["attempt1_failure_registry"]["sha256"] == (
        INPUT_HASHES[ATTEMPT1_DIR / "ATTEMPT1_FAILURE_EVIDENCE_REGISTRY_V1.json"]
    )
    assert identity["lineage"]["refinement_requirements"]["sha256"] == (
        INPUT_HASHES[ATTEMPT1_DIR / "STYLE_CAPSULE_V1_1_REFINEMENT_REQUIREMENTS_V1.json"]
    )


def test_all_twelve_requirements_have_a_material_delta_and_retest_criterion():
    requirements = load(
        ATTEMPT1_DIR / "STYLE_CAPSULE_V1_1_REFINEMENT_REQUIREMENTS_V1.json"
    )
    expected_ids = {item["requirement_id"] for item in requirements["requirements"]}
    changes = load(DELTA_PATH)["changes"]
    assert {item["requirement_id"] for item in changes} == expected_ids
    assert len(changes) == 12
    required_fields = {
        "field_or_mechanism_affected",
        "old_v1_behavior",
        "attempt1_failure_evidence",
        "candidate_change",
        "why_capsule_local",
        "future_retest_criterion",
    }
    assert all(required_fields <= set(item) for item in changes)
    assert all(item["attempt1_failure_evidence"] for item in changes)
    boundary = load(DELTA_PATH)["change_boundary"]
    assert boundary["style_capsule_v1_modified"] is False
    assert boundary["attempt2_payloads_created"] is False
    assert boundary["global_compiler_modified"] is False
    assert boundary["global_schema_modified"] is False


def test_surface_tokens_are_non_sufficient_and_display_mass_is_structural():
    policy = load(POLICY_PATH)
    anti = policy["anti_surface_token_collapse"]
    assert anti["surface_bundle_is_family_pass_evidence"] is False
    assert len(anti["non_sufficient_tokens"]) == 8
    structural = policy["structural_display_mass_contract"]
    assert len(structural["required_structural_properties"]) == 6
    assert structural["surface_treatment_sufficient"] is False
    assert structural["non_brush_implementation_valid"] is True
    assert structural["failure_condition"] == "GENERIC_BRUSH_CALLIGRAPHY_SHORTCUT"
    identity = load(IDENTITY_PATH)["required_refinements_realized"]
    assert identity["surface_bundle_is_family_pass_evidence"] is False
    assert identity["structural_display_mass_separated_from_surface_treatment"] is True


def test_operator_isolation_is_machine_readable_and_no_payload_was_created():
    contract = load(POLICY_PATH)["operator_isolation_contract"]
    assert contract["contract_state"] == (
        "MACHINE_READABLE_DESIGN_CONSTRAINTS_NOT_PAYLOADS"
    )
    assert contract["attempt2_payloads_created"] is False
    assert len(contract["tiers"]) == 3
    for tier in contract["tiers"]:
        assert set(tier) == {
            "tier_id",
            "HELD_CONSTANTS",
            "CHANGED_VARIABLES",
            "PROHIBITED_LEAKAGE",
        }
        assert tier["HELD_CONSTANTS"]
        assert tier["CHANGED_VARIABLES"]
        assert tier["PROHIBITED_LEAKAGE"]
    assert contract["automatic_failure_rule"]["result"] == (
        "OPERATOR_ISOLATION_FAILURE"
    )


def test_composition_is_relation_topology_and_type_safe_space_can_move():
    policy = load(POLICY_PATH)
    topology = policy["composition_topology"]
    assert topology["encoding"] == "RELATION_GRAPH_NOT_SCREEN_COORDINATES"
    assert topology["major_mass_location_change_allowed"] is True
    assert len(topology["required_edges"]) == 4
    assert set(topology["forbidden_fixed_position_requirements"]) >= {
        "TITLE_UPPER_LEFT",
        "WOK_LOWER_RIGHT",
        "MOUNTAIN_REAR_CENTER",
        "QUIET_SPACE_FIXED_LOCATION",
    }
    safe = policy["type_safe_space_policy"]
    assert safe["location_variable"] is True
    assert set(safe["valid_sources"]) == {
        "CROP",
        "SCENE_STAGING",
        "LOCAL_LUMINANCE_AND_SPATIAL_FREQUENCY",
        "DEPTH_AND_OCCLUSION",
        "TITLE_PHOTO_COUNTER_MASS_PLANNING",
    }
    assert "FIXED_DARK_LEFT_COLUMN" in safe["prohibited_default_solutions"]


def test_aspect_reflow_and_motif_omit_are_explicit():
    policy = load(POLICY_PATH)
    aspect = policy["aspect_reflow_contract"]
    assert aspect["required_operation"] == "ZONE_REALLOCATION_AND_RELATION_REFLOW"
    assert aspect["native_target_aspect_composition_required"] is True
    assert aspect["reading_order_graph_preserved"] is True
    assert set(aspect["failure_conditions"]) >= {
        "GENERIC_VERTICAL_POSTER_FALLBACK",
        "UNJUSTIFIED_FILLER_TOKEN",
        "ASPECT_STRETCH_OR_STACK_ONLY",
    }
    motif = policy["motif_policy"]
    assert motif["default"] == "OMIT"
    assert motif["attempt1_f3_mountain_line_role"] == (
        "IMMUTABLE_NEGATIVE_EVIDENCE_NOT_INSPIRATION"
    )


def test_surface_divergence_and_mechanism_explanation_are_predeclared():
    policy = load(POLICY_PATH)
    divergence = policy["surface_divergence_predeclaration"]
    assert divergence["required_before_generation"] is True
    assert divergence["maximum_difference_in_every_field_required"] is False
    assert len(divergence["tracked_fields"]) == 9
    assert "LAYOUT_TOPOLOGY" in divergence["tracked_fields"]
    assert "AT_LEAST_ONE_DIVERGENCE_IN_LAYOUT_TOPOLOGY_OR_MAJOR_MASS_LOCATION" in (
        divergence["required_evidence_shape"]
    )
    explanation = policy["mechanism_explanation_sufficiency"]
    assert explanation["criterion"] == "MECHANISM_EXPLANATION_SUFFICIENCY"
    assert explanation["required_core_relationships"] == [
        "HIERARCHY",
        "COUNTER_MASS",
    ]
    assert set(explanation["insufficient_primary_explanations"]) == {
        "SAME_PALETTE",
        "SAME_BRUSH_FONT",
        "SAME_MOUNTAIN_SCENE",
        "SAME_WOK",
        "SAME_COMPOSITION",
    }


def test_realism_and_family_mechanisms_are_independent_non_compensating_scores():
    scores = load(POLICY_PATH)["independent_score_channels"]
    assert set(scores) == {
        "TECHNICAL_PHOTOGRAPHIC_REALISM",
        "FAMILY_MECHANISM_VALIDATION",
    }
    assert scores["TECHNICAL_PHOTOGRAPHIC_REALISM"][
        "can_override_family_failure"
    ] is False
    assert scores["FAMILY_MECHANISM_VALIDATION"][
        "can_be_compensated_by_realism"
    ] is False
    candidate = load(CANDIDATE_PATH)
    joined_photo = "\n".join(candidate["quality_gates"]["photography"])
    joined_integration = "\n".join(candidate["quality_gates"]["integration"])
    assert "TECHNICAL_PHOTOGRAPHIC_REALISM" in joined_photo
    assert "FAMILY_MECHANISM_VALIDATION" in joined_integration


def test_receipt_binds_exact_artifacts_inputs_and_non_promotion_state():
    receipt = load(RECEIPT_PATH)
    assert receipt["repository_authority"]["input_remote_head"] == INPUT_HEAD
    assert receipt["immutable_baseline_v1"]["sha256_before"] == V1_SHA
    assert receipt["immutable_baseline_v1"]["sha256_after"] == V1_SHA
    assert receipt["immutable_baseline_v1"]["modified"] is False
    created = receipt["created_candidate"]
    assert created["artifact_sha256"] == sha256(CANDIDATE_PATH)
    assert created["identity_sha256"] == sha256(IDENTITY_PATH)
    assert created["refinement_delta_sha256"] == sha256(DELTA_PATH)
    assert created["local_policy_sha256"] == sha256(POLICY_PATH)
    for path, expected_hash in INPUT_HASHES.items():
        assert sha256(path) == expected_hash
    maturity = receipt["maturity_validation"]
    assert maturity["candidate_created"] is True
    assert maturity["controlled_validation_required"] is True
    assert maturity["family_validated"] is False
    assert maturity["durable_family_signature"] is False
    assert maturity["commercial_quality"] == "NOT_YET"
    assert maturity["golden"] == "NO"
    assert maturity["scale"] == "BLOCKED_NOT_EXECUTED"
    assert receipt["next_allowed_action"] == NEXT_ACTION
    assert receipt["primary_verdict"] == (
        "STYLE_CAPSULE_V1_1_CANDIDATE_CREATED_READY_FOR_ATTEMPT2_DESIGN"
    )


def test_global_compiler_schema_and_attempt1_evidence_remain_immutable():
    assert sha256(V1_PATH) == V1_SHA
    assert sha256(COMPILER_PATH) == (
        "d53a8485ebf3b449f261695d1602543303611bae899497d1bc401f8c23da79b4"
    )
    assert sha256(SCHEMA_PATH) == (
        "573314cd63d9f799107788e348d81a9ad8f1735976babeb6b0f9e7bde2f9f348"
    )
    compiler = load(IDENTITY_PATH)["compiler_schema"]
    assert compiler["global_compiler_modified"] is False
    assert compiler["global_schema_modified"] is False
    assert compiler["local_policy_required"] is True
    assertion = load(IDENTITY_PATH)["provenance_assertions"]
    assert assertion["current_adhoc_poster"] == (
        "CURRENT_灶边味_POSTER_IS_NOT_CAPSULE_PROVENANCE"
    )
    assert assertion["current_adhoc_poster_role"] == (
        "NON_PROVENANCE_DIAGNOSTIC_ONLY"
    )
    assert assertion["attempt1_outputs_role"] == (
        "IMMUTABLE_NEGATIVE_VALIDATION_EVIDENCE_ONLY"
    )


def test_checkpoint_ledger_and_adapter_are_consistent():
    checkpoint = load(CHECKPOINT_PATH)
    assert checkpoint["sequence"] == 17
    assert checkpoint["status"] == STATE
    assert checkpoint["highest_accepted_checkpoint"] == STATE
    assert checkpoint["next_required_action"] == NEXT_ACTION
    lines = LEDGER_PATH.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 3
    events = [json.loads(line) for line in lines]
    event = events[-1]
    previous = events[-2]
    assert event["event_id"] == EVENT_ID
    assert event["event_hash"] == EVENT_HASH
    assert event["previous_event_id"] == previous["event_id"]
    assert event["previous_event_hash"] == previous["event_hash"]
    asserted = dict(event)
    asserted_hash = asserted.pop("event_hash")
    canonical = json.dumps(
        asserted, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    assert hashlib.sha256(canonical).hexdigest() == asserted_hash
    tail = checkpoint["ledger_tails"]["distillation_evidence"]
    assert tail == {"event_id": EVENT_ID, "event_hash": EVENT_HASH}
    adapter = load(ADAPTER_PATH)
    state = {item["path"]: item for item in adapter["state_authorities"]}
    task = {item["path"]: item for item in adapter["task_authorities"]}
    identity_path = (
        "evidence/vpd/shanyeji/style_capsule_v1_1_candidate/"
        "CAPSULE_V1_1_CANDIDATE_IDENTITY.json"
    )
    policy_path = (
        "evidence/vpd/shanyeji/style_capsule_v1_1_candidate/"
        "CAPSULE_LOCAL_CONTROLLED_VALIDATION_POLICY_V1.json"
    )
    assert state[identity_path]["priority"] == 1
    assert task[policy_path]["priority"] == 1
    adapter_ref = next(
        item
        for item in checkpoint["source_state_refs"]
        if item.get("path") == "PROJECT_CONTROL_ADAPTER.json"
    )
    assert adapter_ref["sha256"] == sha256(ADAPTER_PATH)


def test_task_created_no_images_attempt2_payloads_or_renderer_route():
    assert list(CANDIDATE_DIR.glob("*.png")) == []
    assert list(CANDIDATE_DIR.glob("*PAYLOAD*.json")) == []
    identity = load(IDENTITY_PATH)
    boundary = identity["execution_boundary"]
    assert boundary["chatgpt_only"] is True
    for key in (
        "image_generation_executed",
        "image_editing_executed",
        "attempt1_rerun",
        "attempt2_payloads_created",
        "attempt2_generation_executed",
        "api_key_used",
        "openai_api_used",
        "wif_used",
        "oidc_used",
        "private_or_external_renderer_used",
        "renderer_infrastructure_work",
        "commercial_executed",
        "golden_executed",
        "scale_executed",
    ):
        assert boundary[key] is False
    assert boundary["next_allowed_action"] == NEXT_ACTION


def main():
    tests = [
        value
        for name, value in sorted(globals().items())
        if name.startswith("test_") and callable(value)
    ]
    for test in tests:
        test()
    print(
        "SHANYEJI_STYLE_CAPSULE_V1_1_CANDIDATE_VALIDATION_PASS "
        f"tests={len(tests)}"
    )


if __name__ == "__main__":
    main()
