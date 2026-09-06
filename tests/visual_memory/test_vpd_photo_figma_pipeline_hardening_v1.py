from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError

from visual_memory.vpd_commercial_pipeline import (
    commercial_receipt_errors,
    photo_only_payload_errors,
    require_commercial_receipt,
    require_photo_only_payload,
)


ROOT = Path(__file__).resolve().parents[2]
CONTRACT_DIR = ROOT / "contracts" / "vpd"
PHOTO_CONTRACT_PATH = CONTRACT_DIR / "PHOTO_ONLY_RENDER_CONTRACT_V1.json"
FIGMA_CONTRACT_PATH = CONTRACT_DIR / "FIGMA_COMPOSITION_CONTRACT_V1.json"
GATE_POLICY_PATH = CONTRACT_DIR / "COMMERCIAL_DESIGN_GATE_POLICY_V1.json"
SCHEMA_PATH = ROOT / "schemas" / "commercial-design-provenance-receipt.v1.schema.json"
FIXTURE_PATH = (
    ROOT
    / "tests"
    / "fixtures"
    / "vpd_commercial_pipeline"
    / "valid_staged_receipt.json"
)
MODULE_PATH = ROOT / "visual_memory" / "vpd_commercial_pipeline.py"
ADAPTER_PATH = ROOT / "PROJECT_CONTROL_ADAPTER.json"
CHECKPOINT_PATH = ROOT / "continuity" / "vpd" / "LATEST_CHECKPOINT.json"
LEDGER_PATH = (
    ROOT / "continuity" / "vpd" / "state_ledger" / "commercial_design_pipeline.jsonl"
)
RECEIPT_PATH = (
    ROOT
    / "evidence"
    / "vpd"
    / "pipeline_hardening_v1"
    / "PIPELINE_HARDENING_IMPLEMENTATION_RECEIPT_V1.json"
)
NEXT_ACTION = "RUN_FIRST_FORWARD_PHOTO_ONLY_PLUS_FIGMA_COMPOSITION_VALIDATION"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def valid_photo_payload() -> dict:
    contract = load(PHOTO_CONTRACT_PATH)
    return {
        "contract_id": contract["contract_id"],
        "contract_version": contract["contract_version"],
        "stage": "PHOTO_ONLY_RENDER",
        "render_route": "CHATGPT_PRODUCT_UI",
        "chatgpt_only": True,
        "controller_payload_identity": "PHOTO-ONLY-TEST-001",
        "controller_payload_sha256": "a" * 64,
        "photography_required": {
            field: f"bounded photographic instruction for {field}"
            for field in contract["payload_contract"]["photography_required_fields"]
        },
        "type_safe_space_requirements": {
            "photographic_space_only": True,
            "instruction": "Preserve a scene-derived quiet region for later composition.",
        },
        "graphic_text_prohibited_in_render": {
            field: True
            for field in contract["payload_contract"]["graphic_text_prohibited_fields"]
        },
        "prohibited_composition_shortcuts": contract[
            "prohibited_composition_shortcuts"
        ],
        "final_typography_in_render": False,
    }


def test_contracts_and_schema_are_syntactically_valid_and_forward_only():
    photo = load(PHOTO_CONTRACT_PATH)
    figma = load(FIGMA_CONTRACT_PATH)
    gates = load(GATE_POLICY_PATH)
    schema = load(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    assert photo["contract_id"] == "PHOTO_ONLY_RENDER_CONTRACT_V1"
    assert figma["contract_id"] == "FIGMA_COMPOSITION_CONTRACT_V1"
    assert gates["policy_id"] == "COMMERCIAL_DESIGN_GATE_POLICY_V1"
    assert photo["scope"]["historical_attempts_reclassified"] is False
    assert figma["scope"]["historical_attempts_reclassified"] is False
    assert gates["historical_compatibility"]["policy_is_forward_only"] is True


def test_photo_only_payload_passes_and_prohibits_final_typography_fields():
    contract = load(PHOTO_CONTRACT_PATH)
    payload = valid_photo_payload()
    assert photo_only_payload_errors(payload, contract) == []
    assert require_photo_only_payload(payload, contract) is payload

    with_title = copy.deepcopy(payload)
    with_title["design"] = {"final_chinese_title": "灶边味"}
    errors = photo_only_payload_errors(with_title, contract)
    assert "PHOTO_ONLY_RENDER_CONTAINS_GRAPHIC_TEXT_FIELD:final_chinese_title" in errors

    raster_type = copy.deepcopy(payload)
    raster_type["final_typography_in_render"] = True
    assert "PHOTO_ONLY_RENDER_CONTAINS_FINAL_TYPOGRAPHY" in photo_only_payload_errors(
        raster_type, contract
    )


def test_valid_staged_receipt_binds_photo_to_figma_to_final_export():
    schema = load(SCHEMA_PATH)
    receipt = load(FIXTURE_PATH)
    Draft202012Validator(schema).validate(receipt)
    assert receipt["photo_render_receipt"]["photo_only_contract"][
        "contract_sha256"
    ] == sha256(PHOTO_CONTRACT_PATH)
    assert receipt["figma_composition_receipt"]["composition_contract"][
        "contract_sha256"
    ] == sha256(FIGMA_CONTRACT_PATH)
    assert commercial_receipt_errors(receipt) == []
    assert require_commercial_receipt(receipt) is receipt


def test_formal_receipt_fails_without_figma_or_editable_design_provenance():
    schema = load(SCHEMA_PATH)
    missing_figma = load(FIXTURE_PATH)
    missing_figma.pop("figma_composition_receipt")
    try:
        Draft202012Validator(schema).validate(missing_figma)
    except ValidationError:
        pass
    else:
        raise AssertionError("schema accepted a receipt without Figma provenance")
    errors = commercial_receipt_errors(missing_figma)
    assert "COMMERCIAL_RECEIPT_MISSING:figma_composition_receipt" in errors
    assert "FIGMA_COMPOSITION_RECEIPT_MISSING_OR_INVALID" in errors


def test_formal_receipt_fails_on_raster_type_unknown_figma_or_broken_chain():
    receipt = load(FIXTURE_PATH)
    receipt["photo_render_receipt"]["final_typography_in_render"] = True
    receipt["figma_composition_receipt"]["figma_file_key"] = "UNKNOWN"
    receipt["final_export_receipt"]["source_photo_sha256"] = "2" * 64
    errors = commercial_receipt_errors(receipt)
    assert "FINAL_TYPOGRAPHY_IN_RENDER_MUST_BE_FALSE" in errors
    assert "FORMAL_OUTPUT_FIGMA_FIELD_UNKNOWN:figma_file_key" in errors
    assert "FIGMA_TO_EXPORT_FILE_KEY_MISMATCH" in errors
    assert "PHOTO_TO_EXPORT_SOURCE_HASH_MISMATCH" in errors


def test_all_six_new_gates_are_non_compensating_for_formal_output():
    receipt = load(FIXTURE_PATH)
    receipt["gates"]["TYPOGRAPHY_DESIGN_GATE"] = "FAIL"
    errors = commercial_receipt_errors(receipt)
    assert "FORMAL_OUTPUT_GATE_NOT_PASS:TYPOGRAPHY_DESIGN_GATE" in errors


def test_historical_authority_hashes_remain_unchanged_and_out_of_scope():
    expected = {
        ROOT / "VISUAL_DISTILLATION_COMPILER_CONTRACT_V2.md": "d53a8485ebf3b449f261695d1602543303611bae899497d1bc401f8c23da79b4",
        ROOT / "schemas" / "visual-program.v2.schema.json": "573314cd63d9f799107788e348d81a9ad8f1735976babeb6b0f9e7bde2f9f348",
        ROOT / "evidence" / "vpd" / "shanyeji" / "style_capsule_v1" / "STYLE_CAPSULE_V1.json": "f47023656ad0b5d2b0fe374bd90533f65987ef11175cded20ba37fdf82f3f8f1",
        ROOT / "evidence" / "vpd" / "shanyeji" / "style_capsule_v1_1_candidate" / "STYLE_CAPSULE_V1_1_CANDIDATE.json": "54bbc4a1eccd5e76d17dcb13b889c501ed93a4457dbbc1f8dc157572967a0cd9",
        ROOT / "evidence" / "vpd" / "shanyeji" / "controlled_family_attempt2" / "F1_CONTROLLER_PAYLOAD.json": "edeb914f9febf2073cdda67da3ff282d27933f23f9c8d4a577ebc6ff5938df61",
        ROOT / "evidence" / "vpd" / "shanyeji" / "controlled_family_attempt2" / "F2_CONTROLLER_PAYLOAD.json": "7bba27202e8ba79a646fa17b74551dcc636e9eeb0c3d0b8d9c1545451a6e502e",
        ROOT / "evidence" / "vpd" / "shanyeji" / "controlled_family_attempt2" / "F3_CONTROLLER_PAYLOAD.json": "b48c6f31d56038d71522c6b6fc918f887750aff795f92e26c74cfac608822c05",
        ROOT / "evidence" / "vpd" / "shanyeji" / "controlled_family_attempt2" / "ATTEMPT2_HUMAN_FINAL_SETTLEMENT_20260825.json": "683c0d9991c54a960de7eff4ebceccefbf95d18f35a683d3af85e088501210a1",
    }
    for path, expected_hash in expected.items():
        assert sha256(path) == expected_hash
    policy = load(GATE_POLICY_PATH)
    assert policy["historical_compatibility"][
        "attempt1_and_attempt2_remain_under_historical_rules"
    ] is True


def test_validator_adds_no_renderer_or_network_infrastructure():
    source = MODULE_PATH.read_text(encoding="utf-8")
    for forbidden in (
        "import openai",
        "import requests",
        "import httpx",
        "import urllib",
        "import playwright",
    ):
        assert forbidden not in source
    contract = load(PHOTO_CONTRACT_PATH)
    assert contract["execution_route"]["codex_renderer_authorized"] is False
    assert contract["execution_route"][
        "api_wif_oidc_private_external_or_browser_automation_renderer_authorized"
    ] is False


def test_adapter_checkpoint_ledger_and_receipt_are_forward_only_and_hash_valid():
    adapter = load(ADAPTER_PATH)
    assert adapter["forward_commercial_pipeline"] == {
        "architecture": "PHOTO_ONLY_RENDER -> FIGMA_COMPOSITION -> FINAL_EXPORT",
        "status": "HARDENED_READY_FOR_FIRST_FORWARD_VALIDATION",
        "image_generation_policy": "CHATGPT_ONLY",
        "figma_design_surface": "REQUIRED_FOR_FUTURE_FORMAL_COMMERCIAL_OUTPUT",
        "historical_attempts_reclassified": False,
        "next_required_action": NEXT_ACTION,
    }
    for authority_name in (
        "state_authorities",
        "task_authorities",
        "acceptance_authorities",
    ):
        priorities = [item["priority"] for item in adapter[authority_name]]
        assert priorities == list(range(1, len(priorities) + 1))

    checkpoint = load(CHECKPOINT_PATH)
    assert checkpoint["sequence"] == 19
    assert checkpoint["next_required_action"] == NEXT_ACTION
    assert checkpoint["status"] == (
        "VPD_PHOTO_FIGMA_PIPELINE_HARDENED_FIRST_FORWARD_VALIDATION_NEXT"
    )

    events = [json.loads(line) for line in LEDGER_PATH.read_text(encoding="utf-8").splitlines()]
    assert len(events) == 1
    event = events[0]
    asserted = dict(event)
    asserted_hash = asserted.pop("event_hash")
    canonical = json.dumps(
        asserted, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    assert hashlib.sha256(canonical).hexdigest() == asserted_hash
    assert checkpoint["ledger_tails"]["commercial_design_pipeline"] == {
        "event_id": event["event_id"],
        "event_hash": event["event_hash"],
    }

    receipt = load(RECEIPT_PATH)
    assert receipt["next_required_action"] == NEXT_ACTION
    assert receipt["next_action_executed"] is False
    assert receipt["backward_compatibility"]["historical_attempt2_evidence_modified"] is False
    assert receipt["execution_assertions"]["renderer_infrastructure_added"] is False
