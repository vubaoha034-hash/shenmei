import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BUNDLE = ROOT / "evidence" / "vpd" / "shanyeji" / "full_image_distillation_v1"
REFERENCE_SHA256 = "9a29fbdc7dd908017924bed270e8dfe18351519eed3fa7bc7001789f2a383414"
EXPECTED_JSON = {
    "FULL_IMAGE_HUMAN_APPROVAL_RECORD.json",
    "CANONICAL_VISUAL_ANCHOR_MANIFEST.json",
    "PHOTOGRAPHY_GRAMMAR_V1.json",
    "GRAPHIC_DESIGN_GRAMMAR_V1.json",
    "TYPOGRAPHY_COMPONENT_GRAMMAR_V1.json",
    "PHOTO_DESIGN_INTEGRATION_GRAMMAR_V1.json",
    "MECHANISM_CANDIDATE_REGISTRY_V1.json",
    "INVARIANT_HYPOTHESES_V1.json",
    "DEGREES_OF_FREEDOM_V1.json",
    "TRANSFORMATION_OPERATOR_HYPOTHESES_V1.json",
    "FAILURE_BOUNDARY_REGISTRY_V1.json",
    "PROVENANCE_EVIDENCE_MATRIX_V1.json",
    "DISTILLATION_RECEIPT_V1.json",
}


def load(name: str):
    return json.loads((BUNDLE / name).read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_required_bundle_is_complete_and_machine_readable():
    assert BUNDLE.is_dir()
    assert EXPECTED_JSON == {path.name for path in BUNDLE.glob("*.json")}
    assert (BUNDLE / "FULL_IMAGE_DISTILLATION_REPORT_V1.md").is_file()
    for name in EXPECTED_JSON:
        artifact = load(name)
        assert artifact["schema_version"]
        assert artifact["artifact_type"]


def test_approval_is_forward_only_and_reference_identity_is_exact():
    approval = load("FULL_IMAGE_HUMAN_APPROVAL_RECORD.json")
    anchor = load("CANONICAL_VISUAL_ANCHOR_MANIFEST.json")["anchor"]
    assert approval["approval_status"] == (
        "APPROVED_FOR_FULL_IMAGE_VPD_DISTILLATION_AS_SHANYEJI_BRAND_EDITORIAL_REFERENCE"
    )
    assert approval["approval_effect"] == "FORWARD_ONLY"
    assert approval["historical_receipts_rewritten"] is False
    assert anchor["drive_file_id"] == "1fG2OQ7IphZfGnH1csu1qZKYCsyAMDOAZ"
    assert anchor["sha256"] == REFERENCE_SHA256
    assert anchor["dimensions"] == {"width": 960, "height": 1280, "aspect_ratio": "3:4"}
    assert anchor["byte_size"] == 142983
    assert anchor["raw_pixels_verified"] is True
    assert load("CANONICAL_VISUAL_ANCHOR_MANIFEST.json")["raw_pixels_committed_to_git"] is False


def test_full_image_grammars_are_complete_but_not_promoted():
    for name in (
        "PHOTOGRAPHY_GRAMMAR_V1.json",
        "GRAPHIC_DESIGN_GRAMMAR_V1.json",
        "PHOTO_DESIGN_INTEGRATION_GRAMMAR_V1.json",
    ):
        artifact = load(name)
        assert artifact["status"] == "COMPLETE_FOR_CAPSULE_HYPOTHESIS_CREATION"
        assert artifact["reference_sha256"] == REFERENCE_SHA256

    typography = load("TYPOGRAPHY_COMPONENT_GRAMMAR_V1.json")
    assert typography["status"] == "COMPLETE_AS_COMPONENT_GRAMMAR_UNPROMOTED"
    assert typography["known_controlled_validation_history"]["typography_transfer_validated"] is False
    assert typography["known_controlled_validation_history"]["golden"] is False
    assert typography["font_identity"] == "UNKNOWN"


def test_mechanisms_and_invariants_remain_hypotheses():
    mechanisms = load("MECHANISM_CANDIDATE_REGISTRY_V1.json")["mechanisms"]
    mechanism_ids = {item["mechanism_id"] for item in mechanisms}
    assert {
        "mech_sy_display_landscape_mass",
        "mech_sy_hierarchical_three_read_field",
        "mech_sy_photo_type_contrast_relationship",
    } <= mechanism_ids
    assert all("VALIDATED_STYLE_SIGNATURE" not in item["validation_status"] for item in mechanisms)

    invariants = load("INVARIANT_HYPOTHESES_V1.json")
    assert invariants["single_reference_warning"].startswith("No item is a VALIDATED_STYLE_SIGNATURE")
    assert len(invariants["hypotheses"]) >= 6
    assert "forest subject" in invariants["explicit_non_invariants"]
    assert "orange path" in invariants["explicit_non_invariants"]


def test_operator_hypotheses_cover_required_classes_without_claiming_validation():
    artifact = load("TRANSFORMATION_OPERATOR_HYPOTHESES_V1.json")
    operators = {item["operator"]: item for item in artifact["operators"]}
    assert set(operators) == {
        "CONTENT_SWAP",
        "ASPECT_ADAPT",
        "PALETTE_SHIFT",
        "DENSITY_SHIFT",
        "MOTIF_REBIND",
        "TYPOGRAPHY_REBIND",
        "MATERIAL_SHIFT",
    }
    assert artifact["validation_status"] == "NO_OPERATOR_VALIDATED_IN_THIS_TASK"
    assert all(item["classification"] in {"READY_AS_TESTABLE_HYPOTHESIS", "PARTIAL", "UNSUPPORTED"} for item in operators.values())
    assert all(item["minimum_future_validation_experiment"] for item in operators.values())


def test_failure_registry_covers_all_required_domains():
    boundaries = load("FAILURE_BOUNDARY_REGISTRY_V1.json")["boundaries"]
    assert {item["category"] for item in boundaries} == {
        "TYPOGRAPHY",
        "PHOTOGRAPHY",
        "GRAPHIC_DESIGN",
        "INTEGRATION",
    }
    assert all(item["observable_signatures"] for item in boundaries)


def test_provenance_reconciles_history_without_merging_or_rewriting():
    provenance = load("PROVENANCE_EVIDENCE_MATRIX_V1.json")
    reconciliation = provenance["lineage_reconciliation"]
    assert reconciliation["historical_branch_merged"] is False
    assert reconciliation["historical_commits_cherry_picked"] is False
    assert reconciliation["historical_files_rewritten"] is False
    assert reconciliation["new_full_image_approval_is_append_only"] is True
    rows = {row["evidence_id"]: row for row in provenance["evidence_rows"]}
    assert rows["ev_sy_current_ad_hoc_poster"]["status"] == "EXCLUDED_FROM_DISTILLATION_INPUT"


def test_receipt_is_non_generative_and_hashes_are_current():
    receipt = load("DISTILLATION_RECEIPT_V1.json")
    assert receipt["primary_verdict"] == "FULL_IMAGE_DISTILLATION_COMPLETE_FOR_CAPSULE_CREATION"
    assert receipt["image_generation_executed"] is False
    assert receipt["image_editing_executed"] is False
    assert receipt["style_capsule_created"] is False
    assert receipt["visual_program_created"] is False
    assert receipt["api_wif_oidc_private_renderer_used"] is False
    expected_hashed = (EXPECTED_JSON - {"DISTILLATION_RECEIPT_V1.json"}) | {
        "FULL_IMAGE_DISTILLATION_REPORT_V1.md"
    }
    assert set(receipt["artifact_sha256"]) == expected_hashed
    for name, expected in receipt["artifact_sha256"].items():
        assert sha256(BUNDLE / name) == expected


def test_no_capsule_or_visual_program_was_created_in_bundle():
    names = {path.name.lower() for path in BUNDLE.iterdir()}
    assert "style_capsule.json" not in names
    assert "visual_program.json" not in names


def test_checkpoint_and_global_ledger_record_durable_distillation_state():
    checkpoint = json.loads((ROOT / "continuity" / "vpd" / "LATEST_CHECKPOINT.json").read_text(encoding="utf-8"))
    assert checkpoint["sequence"] >= 13

    lines = (ROOT / "continuity" / "vpd" / "state_ledger" / "distillation_evidence.jsonl").read_text(encoding="utf-8").splitlines()
    events = [json.loads(line) for line in lines]
    event = next(
        item
        for item in events
        if item["event_id"]
        == "EVT-VISUAL-VPD-SHANYEJI-FULL-IMAGE-DISTILLATION-20260821-001"
    )
    assert event["event_hash"] == (
        "5b8b930cdb927888029990895f1acd3eec9e3338349a513161350927c90aafde"
    )
    asserted = dict(event)
    asserted_hash = asserted.pop("event_hash")
    canonical = json.dumps(asserted, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    assert hashlib.sha256(canonical).hexdigest() == asserted_hash


def main():
    tests = [
        value
        for name, value in sorted(globals().items())
        if name.startswith("test_") and callable(value)
    ]
    for test in tests:
        test()
    print(f"SHANYEJI_FULL_IMAGE_DISTILLATION_VALIDATION_PASS tests={len(tests)}")


if __name__ == "__main__":
    main()
