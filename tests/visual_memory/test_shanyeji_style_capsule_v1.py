import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]
UPSTREAM = ROOT / "evidence" / "vpd" / "shanyeji" / "full_image_distillation_v1"
CAPSULE_DIR = ROOT / "evidence" / "vpd" / "shanyeji" / "style_capsule_v1"
CAPSULE_PATH = CAPSULE_DIR / "STYLE_CAPSULE_V1.json"
IDENTITY_PATH = CAPSULE_DIR / "CAPSULE_IDENTITY_V1.json"
RECEIPT_PATH = CAPSULE_DIR / "STYLE_CAPSULE_CREATION_RECEIPT_V1.json"
SCHEMA_PATH = ROOT / "schemas" / "visual-program.v2.schema.json"
CHECKPOINT_PATH = ROOT / "continuity" / "vpd" / "LATEST_CHECKPOINT.json"
LEDGER_PATH = ROOT / "continuity" / "vpd" / "state_ledger" / "distillation_evidence.jsonl"

CAPSULE_ID = "style_capsule_shanyeji_brand_editorial_v1"
REFERENCE_SHA256 = "9a29fbdc7dd908017924bed270e8dfe18351519eed3fa7bc7001789f2a383414"
INPUT_COMMIT = "8bc1c265994a5b4f0d6a1b329bc76956355e8df4"
NEXT_ACTION = (
    "DESIGN_AND_RUN_FIRST_CONTROLLED_FAMILY_GENERATION_FROM_FORMAL_"
    "SHANYEJI_STYLE_CAPSULE_V1_WITH_CHATGPT_ONLY_AND_HUMAN_PIXEL_REVIEW"
)
PROVENANCE_ASSERTION = "CURRENT_灶边味_POSTER_IS_NOT_CAPSULE_PROVENANCE"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_new_artifacts_are_machine_readable_and_schema_valid():
    capsule = load(CAPSULE_PATH)
    load(IDENTITY_PATH)
    load(RECEIPT_PATH)
    schema = load(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(capsule)


def test_repository_contract_represents_style_capsule_as_visual_program():
    capsule = load(CAPSULE_PATH)
    identity = load(IDENTITY_PATH)
    relationship = identity["visual_program_relationship"]
    assert identity["capsule_id"] == CAPSULE_ID
    assert identity["capsule_version"] == "1.0.0"
    assert relationship["relationship"] == "STYLE_CAPSULE_IS_VISUALPROGRAM_FORM"
    assert relationship["program_id"] == capsule["program_id"] == CAPSULE_ID
    assert relationship["schema_path"] == "schemas/visual-program.v2.schema.json"
    assert relationship["compiler_id"] == "visual-distillation-compiler-v2"
    assert capsule["version"] == "2.0.0"
    assert capsule["status"] == "DISTILLED"


def test_source_reference_and_approval_authority_are_exact():
    capsule = load(CAPSULE_PATH)
    identity = load(IDENTITY_PATH)
    source = identity["source_reference"]
    assert source == {
        "filename": "R1C-APPROVED-SHANYEJI-CANONICAL.jpg",
        "sha256": REFERENCE_SHA256,
        "asset_id": "ast_d9e80019-544f-4c0c-9b8d-cc04541ff0ed",
        "drive_file_id": "1fG2OQ7IphZfGnH1csu1qZKYCsyAMDOAZ",
        "role": "CANONICAL_FULL_REFERENCE_VISUAL_ANCHOR",
        "diagnostic_crop_ids": [],
    }
    assert capsule["source_evidence"]["reference_assets"] == [
        {
            "asset_id": source["asset_id"],
            "sha256": REFERENCE_SHA256,
            "role": "PRIMARY_REFERENCE",
        }
    ]
    approval = identity["approval_authority"]
    assert approval["record_id"] == "vpd_shanyeji_full_image_approval_20260821_001"
    assert approval["authority_class"] == "HUMAN_AUTHORITY"
    assert sha256(ROOT / approval["record_path"]) == approval["record_sha256"]


def test_every_upstream_artifact_hash_is_exact_and_attributed_to_input_commit():
    identity = load(IDENTITY_PATH)
    receipt = load(RECEIPT_PATH)
    assert identity["upstream_distillation"]["commit"] == INPUT_COMMIT
    assert receipt["input_commit"] == INPUT_COMMIT
    identity_artifacts = {
        item["path"]: item["sha256"]
        for item in identity["upstream_distillation"]["artifacts"]
    }
    assert identity_artifacts == receipt["upstream_artifact_sha256"]
    assert len(identity_artifacts) == 14
    for relative_path, expected_hash in identity_artifacts.items():
        assert sha256(ROOT / relative_path) == expected_hash


def test_all_required_grammar_and_hypothesis_layers_are_retained():
    identity = load(IDENTITY_PATH)
    retained = identity["retained_layers"]
    assert set(retained) == {
        "visual_anchors",
        "photography_grammar",
        "graphic_design_grammar",
        "typography_component_grammar",
        "photo_design_integration_grammar",
        "mechanism_candidates",
        "invariant_hypotheses",
        "degrees_of_freedom",
        "transformation_operator_hypotheses",
        "failure_boundaries",
        "provenance",
    }
    artifacts = {
        item["identity"]
        for item in identity["upstream_distillation"]["artifacts"]
    }
    assert set(retained.values()) <= artifacts


def test_three_engines_and_typography_component_reuse_are_compiled():
    capsule = load(CAPSULE_PATH)
    assert all(capsule["photography_engine"][key] for key in capsule["photography_engine"])
    assert all(capsule["graphic_design_engine"][key] for key in capsule["graphic_design_engine"])
    assert all(capsule["integration_engine"][key] for key in capsule["integration_engine"])
    identity = load(IDENTITY_PATH)
    typography = identity["typography_component_reuse"]
    assert typography["source_family"] == "family_shanyeji_typography_candidate"
    assert typography["reusable_as_component_evidence"] == [
        "display_landscape_mass",
        "hierarchical_three_read_field",
        "photo_type_contrast_relationship",
    ]
    assert typography["typography_transfer_validated"] is False


def test_mechanisms_retain_evidence_causality_scope_and_validation_requirements():
    upstream = load(UPSTREAM / "MECHANISM_CANDIDATE_REGISTRY_V1.json")
    mechanisms = upstream["mechanisms"]
    required = {
        "evidence_class",
        "confidence",
        "causal_hypothesis",
        "transfer_scope",
        "validation_requirement",
    }
    assert all(required <= set(item) for item in mechanisms)
    capsule = load(CAPSULE_PATH)
    compiled_ids = {item["variable"] for item in capsule["causal_priority_map"]}
    assert compiled_ids == {item["mechanism_id"] for item in mechanisms}
    registry_ref = capsule["graphic_design_engine"]["semantic_intent"][1]["value"]
    assert registry_ref["sha256"] == sha256(
        UPSTREAM / "MECHANISM_CANDIDATE_REGISTRY_V1.json"
    )
    assert set(registry_ref["retained_fields"]) >= required


def test_invariants_and_operators_remain_unvalidated_hypotheses():
    capsule = load(CAPSULE_PATH)
    identity = load(IDENTITY_PATH)
    assert all(
        value.startswith("HYPOTHESIS / CONTROLLED VALIDATION REQUIRED:")
        for value in capsule["transfer_model"]["fixed_invariants"]
    )
    assert identity["maturity_status"] == (
        "FORMAL_CAPSULE_CREATED_CONTROLLED_VALIDATION_REQUIRED"
    )
    state = identity["validation_state"]
    assert state["family_level_invariants"] == "UNVALIDATED_HYPOTHESES"
    assert state["transformation_operators"] == "UNVALIDATED_HYPOTHESES"
    assert state["commercial_quality"] == "NOT_YET"
    assert state["golden"] == "NO"
    assert state["scale"] == "BLOCKED_NOT_EXECUTED"
    receipt_state = load(RECEIPT_PATH)["maturity_validation"]
    assert receipt_state["durable_style_signature"] is False
    assert receipt_state["family_level_invariants_validated"] is False
    assert receipt_state["transformation_operators_validated"] is False


def test_brand_bound_identity_and_current_poster_are_excluded():
    capsule = load(CAPSULE_PATH)
    identity = load(IDENTITY_PATH)
    receipt = load(RECEIPT_PATH)
    exclusions = "\n".join(capsule["transfer_model"]["do_not_copy"])
    for token in ("山野集", "李家班", "WANCE", "万策", "灶边味"):
        assert token in exclusions
    assert identity["provenance_assertion"] == PROVENANCE_ASSERTION
    assert receipt["provenance_assertion"] == PROVENANCE_ASSERTION
    assert receipt["brand_bound_exclusions_validated"] is True
    for item in capsule["causal_priority_map"]:
        assert item["variable"] not in {
            "exact 山野集 contours",
            "李家班 identity",
            "WANCE identity",
            "current 灶边味 poster",
        }


def test_mode_boundary_is_non_executing_and_family_maps_to_schema_variate():
    capsule = load(CAPSULE_PATH)
    identity = load(IDENTITY_PATH)
    boundary = identity["execution_boundary"]
    assert capsule["renderer_contract"]["supported_modes"] == [
        "RECONSTRUCT",
        "VARIATE",
        "TRANSFER",
    ]
    assert boundary["schema_mode_mapping"]["FAMILY"] == "VARIATE"
    assert boundary["next_allowed_operation"] == NEXT_ACTION
    for key in (
        "image_generation_executed",
        "image_editing_executed",
        "reconstruct_executed",
        "family_executed",
        "transfer_executed",
        "api_wif_oidc_private_renderer_used",
        "global_compiler_rules_modified",
    ):
        assert boundary[key] is False


def test_creation_receipt_binds_capsule_identity_schema_and_no_global_change():
    receipt = load(RECEIPT_PATH)
    capsule = receipt["capsule"]
    compiler = receipt["compiler_schema"]
    assert capsule["artifact_sha256"] == sha256(CAPSULE_PATH)
    assert capsule["identity_sha256"] == sha256(IDENTITY_PATH)
    assert compiler["visual_program_schema_sha256"] == sha256(SCHEMA_PATH)
    assert compiler["compiler_id"] == "visual-distillation-compiler-v2"
    assert compiler["global_compiler_rules_modified"] is False
    assert compiler["global_schema_modified"] is False
    assert compiler["upstream_evidence_modified"] is False
    assert receipt["remote_authority_sync_gate"]["status"] == "PASS"
    assert receipt["next_allowed_operation"] == NEXT_ACTION
    assert receipt["primary_verdict"] == (
        "FORMAL_STYLE_CAPSULE_V1_CREATED_READY_FOR_CONTROLLED_GENERATION"
    )


def test_checkpoint_and_append_only_ledger_are_consistent():
    checkpoint = load(CHECKPOINT_PATH)
    assert checkpoint["sequence"] >= 14
    tail = checkpoint["ledger_tails"]["distillation_evidence"]
    lines = LEDGER_PATH.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    previous = json.loads(lines[-2])
    event = json.loads(lines[-1])
    assert event["event_id"] == tail["event_id"]
    assert event["event_hash"] == tail["event_hash"]
    assert event["previous_event_id"] == previous["event_id"]
    assert event["previous_event_hash"] == previous["event_hash"]
    asserted = dict(event)
    asserted_hash = asserted.pop("event_hash")
    canonical = json.dumps(
        asserted, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    assert hashlib.sha256(canonical).hexdigest() == asserted_hash


def main():
    tests = [
        value
        for name, value in sorted(globals().items())
        if name.startswith("test_") and callable(value)
    ]
    for test in tests:
        test()
    print(f"SHANYEJI_STYLE_CAPSULE_V1_VALIDATION_PASS tests={len(tests)}")


if __name__ == "__main__":
    main()
