import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "evidence" / "vpd" / "shanyeji" / "controlled_family_generation_v1"
CAPSULE_PATH = (
    ROOT
    / "evidence"
    / "vpd"
    / "shanyeji"
    / "style_capsule_v1"
    / "STYLE_CAPSULE_V1.json"
)
SETTLEMENT_PATH = DIR / "ATTEMPT1_HUMAN_PIXEL_REVIEW_SETTLEMENT_V1.json"
FAILURES_PATH = DIR / "ATTEMPT1_FAILURE_EVIDENCE_REGISTRY_V1.json"
REQUIREMENTS_PATH = DIR / "STYLE_CAPSULE_V1_1_REFINEMENT_REQUIREMENTS_V1.json"
RECEIPT_PATH = DIR / "ATTEMPT1_SETTLEMENT_RECEIPT_V1.json"
CHECKPOINT_PATH = ROOT / "continuity" / "vpd" / "LATEST_CHECKPOINT.json"
LEDGER_PATH = (
    ROOT / "continuity" / "vpd" / "state_ledger" / "controlled_family_human_review.jsonl"
)
ADAPTER_PATH = ROOT / "PROJECT_CONTROL_ADAPTER.json"

CAPSULE_ID = "style_capsule_shanyeji_brand_editorial_v1"
CAPSULE_SHA = "f47023656ad0b5d2b0fe374bd90533f65987ef11175cded20ba37fdf82f3f8f1"
NEXT_ACTION = (
    "CREATE_SHANYEJI_STYLE_CAPSULE_V1_1_CANDIDATE_FROM_V1_PLUS_ATTEMPT1_"
    "FAILURE_EVIDENCE_WITHOUT_GLOBAL_COMPILER_CHANGE"
)
ARTIFACT_HASHES = {
    SETTLEMENT_PATH: "70549b7e0bc307c16d0c228fac6d36ec25bc4b4cddeafeea173090e89f8709e9",
    FAILURES_PATH: "283fc7f3337d19caeeed652a80aebe79af746b55ed50adbd027461d9216e48c0",
    REQUIREMENTS_PATH: "6ae57ac7cb13074d2e99205f69055850e2bc686ee89ab8050f5ebc3223f6709f",
    RECEIPT_PATH: "4e899123162c24a859dacad4a744997027dd45e43d866e95b35f2393df5bd6dd",
}
PAYLOADS = {
    "SHY-FAM-V1-F1": (
        "F1_CONTROLLER_PAYLOAD.json",
        "b63148048b536534fdc23da4865d976d644b072c2233b2ad9bb24ed67f79d2a7",
        "14j_xtKhL77xb0WXA62UO_mWU1SJFLi7H",
        "aceee81249c2f768f742b7c51f6c15b0ad08a45bc5e183cadc7b48599a6f1325",
        [1086, 1448],
    ),
    "SHY-FAM-V1-F2": (
        "F2_CONTROLLER_PAYLOAD.json",
        "79353ff30b38aa66910806ea54afec5df91397d311abe769867770704065d2fd",
        "1gXWUKriPs713OPcYQX49USM1BqmzRB_k",
        "6a5007f93344d76afc5f3f5e3b7a20074e2a69ee961d5776d2384d073d2405fa",
        [1086, 1448],
    ),
    "SHY-FAM-V1-F3": (
        "F3_CONTROLLER_PAYLOAD.json",
        "af690bdb927d9987d2a3b267fd55bbac543856e795890cc16e075c04a4ae8169",
        "1YWYg76jo91URdEbcT7CMt3aeHZEh2S0D",
        "b80ee77ca1ac2d3fd613b6231b19f246a820f23510befd4c73760d1c6a2810e6",
        [941, 1672],
    ),
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_new_artifacts_are_parseable_and_exactly_hash_bound():
    for path, expected in ARTIFACT_HASHES.items():
        load(path)
        assert sha256(path) == expected


def test_style_capsule_v1_and_all_frozen_payloads_remain_immutable():
    assert sha256(CAPSULE_PATH) == CAPSULE_SHA
    settlement = load(SETTLEMENT_PATH)
    assert settlement["source_capsule"]["id"] == CAPSULE_ID
    assert settlement["source_capsule"]["version"] == "1.0.0"
    assert settlement["source_capsule"]["sha256"] == CAPSULE_SHA
    assert settlement["source_capsule"]["modified_for_settlement"] is False
    for experiment_id, values in PAYLOADS.items():
        filename, expected_hash, _, _, _ = values
        payload = load(DIR / filename)
        assert payload["experiment_id"] == experiment_id
        assert payload["payload_state"] == "FROZEN"
        assert sha256(DIR / filename) == expected_hash


def test_human_authority_chain_is_faithful_and_not_overclaimed():
    authority = load(SETTLEMENT_PATH)["human_authority"]
    assert authority["exact_user_continuation_text"] == "下一步"
    assert authority["preceding_recommended_verdict"] == "FAMILY_VALIDATION_FAIL"
    assert authority["preceding_recommended_consequence"] == (
        "CAPSULE_REFINEMENT_REQUIRED"
    )
    assert authority["invented_stronger_user_quote"] is False
    assert "did not need to author every diagnostic phrase" in authority[
        "attribution_boundary"
    ]


def test_manifest_payload_and_actual_output_identities_are_exact():
    settlement = load(SETTLEMENT_PATH)
    receipt = load(RECEIPT_PATH)
    settled_outputs = {item["experiment_id"]: item for item in settlement["outputs"]}
    receipt_outputs = {
        item["experiment_id"]: item for item in receipt["exact_output_identities"]
    }
    assert set(settled_outputs) == set(PAYLOADS) == set(receipt_outputs)
    for experiment_id, values in PAYLOADS.items():
        _, payload_hash, drive_id, output_hash, dimensions = values
        settled = settled_outputs[experiment_id]
        bound = receipt_outputs[experiment_id]
        assert settled["payload_sha256"] == payload_hash
        assert settled["output_drive_file_id"] == drive_id
        assert settled["output_sha256"] == output_hash
        assert settled["dimensions"] == dimensions
        assert settled["raw_bytes_and_dimensions_verified"] is True
        assert bound["drive_file_id"] == drive_id
        assert bound["sha256"] == output_hash
        assert bound["dimensions"] == dimensions
        assert bound["raw_bytes_verified"] is True


def test_attempt_contract_and_required_final_verdict_are_settled():
    settlement = load(SETTLEMENT_PATH)
    assert settlement["settlement_state"] == "IMMUTABLE_NEGATIVE_VALIDATION_SAMPLE"
    contract = settlement["attempt_contract"]
    assert contract == {
        "attempt_number": 1,
        "reference_runtime_policy": "NONE",
        "reference_image_count": 0,
        "hidden_variants_created": False,
        "best_of_n_used": False,
        "retry_before_human_review": False,
        "exactly_one_output_per_payload": True,
    }
    assert settlement["final_verdict"] == {
        "TECHNICAL_GENERATION_VALIDITY": "PASS",
        "FORMAL_FAMILY_VALIDATION": "FAIL",
        "CAPSULE_REFINEMENT_REQUIRED": "YES",
        "COMMERCIAL_QUALITY_READY": "NO",
        "GOLDEN_READY": "NO",
        "SCALE_READY": "NO",
    }
    by_id = {item["experiment_id"]: item for item in settlement["outputs"]}
    assert by_id["SHY-FAM-V1-F1"]["operator_isolation"] == "FAIL"
    assert by_id["SHY-FAM-V1-F2"]["content_material_transfer"] == "PARTIAL"
    assert by_id["SHY-FAM-V1-F3"]["aspect_adapt"] == "FAIL"
    assert all(item["technical"] == "PASS" for item in by_id.values())


def test_four_required_failures_are_preserved_with_inference_limits():
    registry = load(FAILURES_PATH)
    failures = {item["failure_id"]: item for item in registry["failure_modes"]}
    assert set(failures) == {
        "SURFACE_TOKEN_COLLAPSE",
        "OPERATOR_ISOLATION_FAILURE",
        "GENERIC_CHINESE_RESTAURANT_POSTER_FALLBACK",
        "ASPECT_ADAPTATION_FAILURE",
    }
    required = {
        "evidence_outputs",
        "observable_symptom",
        "violated_or_unproven_mechanism_operator",
        "likely_failure_layer",
        "confidence",
        "what_this_evidence_does_prove",
        "what_this_evidence_does_not_prove",
        "corrective_requirement",
        "retest_requirement",
    }
    for failure in failures.values():
        assert failure["status"] == "CONFIRMED_IN_ATTEMPT1"
        assert required <= set(failure)
        assert failure["what_this_evidence_does_prove"]
        assert failure["what_this_evidence_does_not_prove"]
    boundary = registry["cross_failure_inference_boundary"]
    assert boundary["vpd_architecture_failed"] is False
    assert boundary["global_compiler_defect_proven"] is False
    assert boundary["global_compiler_hypothesis_only"] is True


def test_refinement_document_is_requirements_only_and_complete():
    requirements = load(REQUIREMENTS_PATH)
    assert requirements["document_class"] == "REQUIREMENTS_ONLY_NOT_A_STYLE_CAPSULE"
    assert requirements["source_lineage"]["immutable_baseline"]["sha256"] == CAPSULE_SHA
    items = {item["requirement_id"]: item for item in requirements["requirements"]}
    assert set(items) == {
        "R1_FREEZE_V1_AS_BASELINE",
        "R2_ANTI_SURFACE_TOKEN_COLLAPSE",
        "R3_REDEFINE_AUTHORED_DISPLAY_MASS",
        "R4_OPERATOR_ISOLATION_CONTRACT",
        "R5_COMPOSITION_TOPOLOGY_NOT_FIXED_POSITION",
        "R6_ASPECT_ADAPT_STRUCTURAL_REFLOW",
        "R7_EVIDENCE_BASED_SEMANTIC_MOTIF_REBINDING",
        "R8_PHOTO_DESIGN_INTEGRATION_NOT_TEMPLATE",
        "R9_SURFACE_DIVERSITY_VALIDATION",
        "R10_MECHANISM_EXPLANATION_SUFFICIENCY",
        "R11_REALISM_NECESSARY_NOT_SUFFICIENT",
        "R12_NO_GLOBAL_COMPILER_MODIFICATION_YET",
    }
    assert items["R3_REDEFINE_AUTHORED_DISPLAY_MASS"]["new_failure_condition"] == (
        "GENERIC_BRUSH_CALLIGRAPHY_SHORTCUT"
    )
    assert items["R6_ASPECT_ADAPT_STRUCTURAL_REFLOW"]["new_failure_conditions"] == [
        "GENERIC_VERTICAL_POSTER_FALLBACK",
        "UNJUSTIFIED_FILLER_TOKEN",
        "ASPECT_STRETCH_OR_STACK_ONLY",
    ]
    isolation = items["R4_OPERATOR_ISOLATION_CONTRACT"]["operator_isolation_table"]
    assert len(isolation) == 3
    assert all(
        set(tier) >= {"held_constants", "changed_variables", "prohibited_leakage"}
        for tier in isolation
    )
    future = requirements["future_candidate_constraints"]
    assert future["create_capsule_v1_1_in_this_task"] is False
    assert future["mutate_capsule_v1_in_place"] is False
    assert future["modify_global_compiler"] is False
    assert requirements["next_allowed_action"] == NEXT_ACTION


def test_receipt_binds_artifacts_transition_and_no_execution():
    receipt = load(RECEIPT_PATH)
    bound = receipt["settlement_artifacts"]
    assert bound["human_review_settlement"]["sha256"] == sha256(SETTLEMENT_PATH)
    assert bound["failure_evidence_registry"]["sha256"] == sha256(FAILURES_PATH)
    assert bound["v1_1_refinement_requirements"]["sha256"] == sha256(
        REQUIREMENTS_PATH
    )
    assert receipt["checkpoint_transition"] == {
        "old_sequence": 15,
        "new_sequence": 16,
        "new_state": (
            "SHANYEJI_ATTEMPT1_FAMILY_VALIDATION_FAIL_"
            "CAPSULE_V1_1_REFINEMENT_NEXT"
        ),
        "previous_sequence_rewritten": False,
    }
    assertions = receipt["execution_assertions"]
    assert all(value is False for value in assertions.values())
    assert receipt["next_allowed_action"] == NEXT_ACTION
    assert receipt["primary_verdict"] == (
        "ATTEMPT1_FAIL_SETTLED_V1_1_REFINEMENT_REQUIREMENTS_READY"
    )


def test_checkpoint_and_human_review_ledger_are_hash_consistent():
    checkpoint = load(CHECKPOINT_PATH)
    expected_state = (
        "SHANYEJI_ATTEMPT1_FAMILY_VALIDATION_FAIL_CAPSULE_V1_1_REFINEMENT_NEXT"
    )
    assert checkpoint["sequence"] == 16
    assert checkpoint["status"] == expected_state
    assert checkpoint["highest_accepted_checkpoint"] == expected_state
    assert checkpoint["next_required_action"] == NEXT_ACTION
    tail = checkpoint["ledger_tails"]["controlled_family_human_review"]
    lines = LEDGER_PATH.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    event = json.loads(lines[0])
    assert event["event_id"] == tail["event_id"]
    assert event["event_hash"] == tail["event_hash"]
    asserted = dict(event)
    asserted_hash = asserted.pop("event_hash")
    canonical = json.dumps(
        asserted, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    assert hashlib.sha256(canonical).hexdigest() == asserted_hash
    assert event["after"]["formal_family_validation"] == "FAIL"
    assert event["after"]["style_capsule_v1_1_created"] is False


def test_adapter_promotes_settlement_and_requirements_authority():
    adapter = load(ADAPTER_PATH)
    state = {item["path"]: item for item in adapter["state_authorities"]}
    tasks = {item["path"]: item for item in adapter["task_authorities"]}
    settlement = (
        "evidence/vpd/shanyeji/controlled_family_generation_v1/"
        "ATTEMPT1_HUMAN_PIXEL_REVIEW_SETTLEMENT_V1.json"
    )
    requirements = (
        "evidence/vpd/shanyeji/controlled_family_generation_v1/"
        "STYLE_CAPSULE_V1_1_REFINEMENT_REQUIREMENTS_V1.json"
    )
    assert state[settlement]["priority"] == 1
    assert state[requirements]["priority"] == 2
    assert tasks[requirements]["priority"] == 1


def test_no_image_capsule_candidate_or_global_compiler_mutation_occurred():
    assert list(DIR.glob("*.png")) == []
    assert not (DIR / "STYLE_CAPSULE_V1_1.json").exists()
    assert sha256(ROOT / "VISUAL_PROGRAM_DISTILLATION_V1.md") == (
        "dceeb642f4e2f33fd75d7a4987eab0b01a80543818feb159cccb89895ed5bbfd"
    )
    assert sha256(ROOT / "VISUAL_DISTILLATION_COMPILER_CONTRACT_V2.md") == (
        "d53a8485ebf3b449f261695d1602543303611bae899497d1bc401f8c23da79b4"
    )
    assert sha256(ROOT / "schemas" / "visual-program.v2.schema.json") == (
        "573314cd63d9f799107788e348d81a9ad8f1735976babeb6b0f9e7bde2f9f348"
    )


def main():
    tests = [
        value
        for name, value in sorted(globals().items())
        if name.startswith("test_") and callable(value)
    ]
    for test in tests:
        test()
    print(f"SHANYEJI_ATTEMPT1_FAIL_SETTLEMENT_V1_VALIDATION_PASS tests={len(tests)}")


if __name__ == "__main__":
    main()
