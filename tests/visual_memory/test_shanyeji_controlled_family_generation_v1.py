import hashlib
import json
import subprocess
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
OLD_FREEZE_PATH = ROOT / "VPD_DISTILLATION_ONLY_RUNTIME_TEST_V1_CONTROLLER_PAYLOAD_FREEZE.json"
CHECKPOINT_PATH = ROOT / "continuity" / "vpd" / "LATEST_CHECKPOINT.json"
LEDGER_PATH = (
    ROOT / "continuity" / "vpd" / "state_ledger" / "controlled_family_validation.jsonl"
)
ADAPTER_PATH = ROOT / "PROJECT_CONTROL_ADAPTER.json"

CAPSULE_ID = "style_capsule_shanyeji_brand_editorial_v1"
CAPSULE_VERSION = "1.0.0"
CAPSULE_SHA256 = "f47023656ad0b5d2b0fe374bd90533f65987ef11175cded20ba37fdf82f3f8f1"
EXPERIMENT = "SHANYEJI_CONTROLLED_FAMILY_GENERATION_V1"
ROUTE = "CHATGPT_UI_CONTROLLED_FAMILY_VALIDATION"
INPUT_HEAD = "a3d4d8ee350edf21498e86913f380c37fe315fc9"
NEXT_ACTION = (
    "RETURN_CHATGPT_RENDER_HANDOFF_TO_CHATGPT_AND_GENERATE_EXACTLY_"
    "F1_F2_F3_ONCE_EACH_THEN_RUN_HUMAN_PIXEL_REVIEW"
)
PAYLOADS = {
    "SHY-FAM-V1-F1": (
        "F1_CONTROLLER_PAYLOAD.json",
        "b63148048b536534fdc23da4865d976d644b072c2233b2ad9bb24ed67f79d2a7",
        "3:4",
        ["TYPOGRAPHY_REBIND", "COPY_REBIND"],
        "SHY-FAM-V1-F1.png",
    ),
    "SHY-FAM-V1-F2": (
        "F2_CONTROLLER_PAYLOAD.json",
        "79353ff30b38aa66910806ea54afec5df91397d311abe769867770704065d2fd",
        "3:4",
        ["CONTENT_SWAP", "MOTIF_REBIND", "MATERIAL_SHIFT"],
        "SHY-FAM-V1-F2.png",
    ),
    "SHY-FAM-V1-F3": (
        "F3_CONTROLLER_PAYLOAD.json",
        "af690bdb927d9987d2a3b267fd55bbac543856e795890cc16e075c04a4ae8169",
        "9:16",
        ["ASPECT_ADAPT", "DENSITY_SHIFT"],
        "SHY-FAM-V1-F3.png",
    ),
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob_sha1(path: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path.relative_to(ROOT))],
        cwd=ROOT,
        text=True,
    ).strip()


def payloads():
    return {
        experiment_id: load(DIR / values[0])
        for experiment_id, values in PAYLOADS.items()
    }


def test_capsule_identity_and_input_remote_head_are_exact():
    assert sha256(CAPSULE_PATH) == CAPSULE_SHA256
    receipt = load(DIR / "CONTROLLED_FAMILY_PAYLOAD_FREEZE_RECEIPT_V1.json")
    assert receipt["style_capsule"] == {
        "id": CAPSULE_ID,
        "version": CAPSULE_VERSION,
        "path": "evidence/vpd/shanyeji/style_capsule_v1/STYLE_CAPSULE_V1.json",
        "sha256": CAPSULE_SHA256,
        "verified": True,
        "maturity": "CONTROLLED_VALIDATION_REQUIRED",
    }
    remote = receipt["input_remote_authority"]
    assert remote["repository"] == "vubaoha034-hash/shenmei"
    assert remote["branch"] == "visual-program-distillation-v2-photography-design-20260814"
    assert remote["remote_head"] == INPUT_HEAD
    assert remote["status"] == "PASS"


def test_exactly_three_new_payloads_have_frozen_hash_bindings():
    actual_json = {path.name for path in DIR.glob("F*_CONTROLLER_PAYLOAD.json")}
    assert actual_json == {values[0] for values in PAYLOADS.values()}
    receipt = load(DIR / "CONTROLLED_FAMILY_PAYLOAD_FREEZE_RECEIPT_V1.json")
    bound = {item["experiment_id"]: item for item in receipt["frozen_payloads"]}
    assert set(bound) == set(PAYLOADS)
    for experiment_id, (filename, expected_hash, _, _, expected_output) in PAYLOADS.items():
        path = DIR / filename
        assert sha256(path) == expected_hash
        assert bound[experiment_id]["sha256"] == expected_hash
        assert bound[experiment_id]["byte_length"] == path.stat().st_size
        assert bound[experiment_id]["expected_output_filename"] == expected_output
        assert bound[experiment_id]["output_count"] == 1


def test_all_payloads_enforce_new_family_route_and_zero_runtime_references():
    for experiment_id, payload in payloads().items():
        assert payload["payload_state"] == "FROZEN"
        assert payload["experiment_name"] == EXPERIMENT
        assert payload["experiment_id"] == experiment_id
        assert payload["family_capsule_id"] == CAPSULE_ID
        assert payload["family_capsule_version"] == CAPSULE_VERSION
        assert payload["family_capsule_sha256"] == CAPSULE_SHA256
        assert payload["mode"] == "FAMILY"
        assert payload["route"] == ROUTE
        assert payload["reference_runtime_policy"] == "NONE"
        assert payload["reference_image_count"] == 0
        assert payload["output_count"] == 1
        assert payload["no_hidden_variants"] is True
        assert payload["no_best_of_n"] is True
        assert payload["no_aesthetic_retry_before_human_review"] is True
        assert payload["human_pixel_review_required"] is True
        assert payload["codex_aesthetic_selection_authorized"] is False
        for key in (
            "source_reference_pixels_provided_to_renderer",
            "current_adhoc_poster_pixels_provided_to_renderer",
            "diagnostic_crop_pixels_provided_to_renderer",
            "historical_lettering_pixels_provided_to_renderer",
        ):
            assert payload[key] is False


def test_copy_aspect_and_progressive_operator_tiers_are_exact():
    for experiment_id, payload in payloads().items():
        _, _, aspect, operators, output = PAYLOADS[experiment_id]
        literal = payload["literal_copy_to_render"]
        assert literal["main_chinese_title"] == "灶边味"
        assert literal["english_support_lines"] == ["WOK HEI", "MOUNTAIN KITCHEN"]
        assert literal["chinese_support_copy"] == "山野风味 · 现炒现做"
        assert payload["aspect_intent"]["ratio"] == aspect
        assert payload["operator_focus"] == operators
        assert payload["expected_output_filename"] == output
    assert "real layered mountain-kitchen" in payloads()["SHY-FAM-V1-F1"]["photographic_subject_direction"]
    assert "Real Chinese wok cooking" in payloads()["SHY-FAM-V1-F2"]["photographic_subject_direction"]
    assert "authored for 9:16" in payloads()["SHY-FAM-V1-F3"]["photographic_subject_direction"]


def test_handoff_binds_hashes_instructions_order_and_provenance_manifest():
    handoff_path = DIR / "VPD_SHANYEJI_CHATGPT_RENDER_HANDOFF_V1.txt"
    handoff = handoff_path.read_text(encoding="utf-8")
    assert "Generate in this exact serial order: F1 -> F2 -> F3." in handoff
    assert "Reference runtime policy: NONE" in handoff
    assert "Reference image count: 0" in handoff
    assert "Do not open or inspect the canonical reference image for generation." in handoff
    for experiment_id, payload in payloads().items():
        _, expected_hash, _, _, output = PAYLOADS[experiment_id]
        assert experiment_id in handoff
        assert expected_hash in handoff
        assert output in handoff
        assert payload["renderer_instruction"] in handoff
    for field in (
        "output_sha256",
        "generated_at",
        "generation_attempt_number",
        "hidden_variants_created",
        "human_pixel_review_status",
    ):
        assert field in handoff


def test_plan_and_human_review_keep_controlled_validation_boundaries():
    plan = load(DIR / "CONTROLLED_FAMILY_GENERATION_PLAN_V1.json")
    assert plan["experiment"]["name"] == EXPERIMENT
    assert plan["experiment"]["route"] == ROUTE
    assert plan["experiment"]["generation_order"] == list(PAYLOADS)
    assert len(plan["progressive_challenge_tiers"]) == 3
    limit = plan["validation_limit"]
    assert limit["classification"] == "CONTROLLED_VALIDATION_NOT_DURABLE_PROOF"
    assert limit["durable_invariants_claimed"] is False
    assert limit["commercial_quality"] == "NOT_YET"
    assert limit["golden"] == "NO"
    assert limit["scale"] == "BLOCKED_NOT_EXECUTED"

    protocol = load(DIR / "HUMAN_PIXEL_REVIEW_PROTOCOL_V1.json")
    assert protocol["authority"]["final_aesthetic_authority"] == "HUMAN"
    assert protocol["authority"]["codex_final_aesthetic_score_authorized"] is False
    assert set(protocol["review_dimensions"]) == {
        "A_TECHNICAL_VALIDITY",
        "B_FAMILY_TRANSFER_QUALITY",
        "C_ABSOLUTE_COMMERCIAL_AESTHETIC_QUALITY",
    }
    assert {item["code"] for item in protocol["permitted_outcomes"]} == {
        "FAMILY_MECHANISM_PASS_COMMERCIAL_QUALITY_FAIL",
        "FAMILY_MECHANISM_FAIL",
        "TECHNICAL_INVALID",
        "STRONG_CONTROLLED_FAMILY_PASS",
    }
    assert protocol["cross_image_diversity_review"]["required_after_per_image_reviews"] is True


def test_old_formal_v1_freeze_is_byte_identical_and_not_reused():
    receipt = load(DIR / "CONTROLLED_FAMILY_PAYLOAD_FREEZE_RECEIPT_V1.json")
    old = receipt["old_formal_v1_preservation"]
    assert sha256(OLD_FREEZE_PATH) == old["sha256_before"] == (
        "1fac472395678deef72f69c70cc862dc4e1b94c3603024eaa7cdb4c826e101b9"
    )
    assert git_blob_sha1(OLD_FREEZE_PATH) == old["git_blob_before"] == (
        "d62b507207019526c8e9de6036f9198508513ca6"
    )
    assert old["modified"] is False
    assert old["payload_content_read_or_reused"] is False


def test_drive_upload_and_readback_receipt_is_complete():
    upload = load(DIR / "DRIVE_HANDOFF_UPLOAD_RECEIPT_V1.json")
    assert upload["status"] == "PASS"
    handoff = upload["render_handoff"]
    assert handoff["drive_file_id"] == "1ou3DznAbMyHuYiW26lTdT3mY_3IpcLve"
    assert handoff["local_sha256"] == sha256(DIR / handoff["filename"])
    assert handoff["local_byte_length"] == handoff["drive_reported_byte_length"]
    assert handoff["readback_verified"] is True
    freeze = upload["freeze_receipt"]
    assert freeze["drive_file_id"] == "1MNQmC9lBMquHq4UzgueccBLdyIs_hMLW"
    assert freeze["local_sha256"] == sha256(DIR / freeze["filename"])
    assert freeze["local_byte_length"] == freeze["drive_reported_byte_length"]
    assert freeze["readback_verified"] is True


def test_checkpoint_and_controlled_family_ledger_are_hash_consistent():
    checkpoint = load(CHECKPOINT_PATH)
    assert checkpoint["sequence"] >= 15
    tail = checkpoint["ledger_tails"]["controlled_family_validation"]
    lines = LEDGER_PATH.read_text(encoding="utf-8").splitlines()
    assert len(lines) >= 1
    events = [json.loads(line) for line in lines]
    event = events[0]
    assert event["previous_event_id"] is None
    assert event["previous_event_hash"] is None
    for index, item in enumerate(events):
        asserted = dict(item)
        asserted_hash = asserted.pop("event_hash")
        canonical = json.dumps(
            asserted, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        assert hashlib.sha256(canonical).hexdigest() == asserted_hash
        if index:
            assert item["previous_event_id"] == events[index - 1]["event_id"]
            assert item["previous_event_hash"] == events[index - 1]["event_hash"]
    assert events[-1]["event_id"] == tail["event_id"]
    assert events[-1]["event_hash"] == tail["event_hash"]
    assert event["after"]["generated_outputs"] == 0
    assert event["after"]["human_pixel_review"] == "PENDING_GENERATION"


def test_adapter_promotes_new_authority_without_erasing_old_authority():
    adapter = load(ADAPTER_PATH)
    tasks = {item["path"]: item for item in adapter["task_authorities"]}
    plan_path = (
        "evidence/vpd/shanyeji/controlled_family_generation_v1/"
        "CONTROLLED_FAMILY_GENERATION_PLAN_V1.json"
    )
    handoff_path = (
        "evidence/vpd/shanyeji/controlled_family_generation_v1/"
        "VPD_SHANYEJI_CHATGPT_RENDER_HANDOFF_V1.txt"
    )
    assert tasks[plan_path]["priority"] < tasks[handoff_path]["priority"]
    assert tasks[handoff_path]["priority"] < tasks[
        "VPD_DISTILLATION_ONLY_RUNTIME_TEST_V1.md"
    ]["priority"]
    assert "preserved separate historical" in tasks[
        "VPD_DISTILLATION_ONLY_RUNTIME_TEST_V1.md"
    ]["purpose"]


def test_preparation_contains_no_generated_images():
    assert list(DIR.glob("*.png")) == []
    receipt = load(DIR / "CONTROLLED_FAMILY_PAYLOAD_FREEZE_RECEIPT_V1.json")
    assertions = receipt["execution_assertions"]
    assert assertions["codex_image_generation_executed"] is False
    assert assertions["image_editing_executed"] is False
    assert assertions["global_compiler_modified"] is False
    assert assertions["golden_entered"] is False
    assert assertions["scale_entered"] is False


def main():
    tests = [
        value
        for name, value in sorted(globals().items())
        if name.startswith("test_") and callable(value)
    ]
    for test in tests:
        test()
    print(f"SHANYEJI_CONTROLLED_FAMILY_GENERATION_V1_VALIDATION_PASS tests={len(tests)}")


if __name__ == "__main__":
    main()
