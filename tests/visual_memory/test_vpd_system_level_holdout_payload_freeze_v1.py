from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "evidence" / "vpd" / "shanyeji" / "system_level_holdout_validation_v1"
ANCHOR_SHA = "9a29fbdc7dd908017924bed270e8dfe18351519eed3fa7bc7001789f2a383414"
ANCHOR_ID = "1fG2OQ7IphZfGnH1csu1qZKYCsyAMDOAZ"
OLD_PAYLOAD_HASHES = {
    "b63148048b536534fdc23da4865d976d644b072c2233b2ad9bb24ed67f79d2a7",
    "79353ff30b38aa66910806ea54afec5df91397d311abe769867770704065d2fd",
    "af690bdb927d9987d2a3b267fd55bbac543856e795890cc16e075c04a4ae8169",
    "edeb914f9febf2073cdda67da3ff282d27933f23f9c8d4a577ebc6ff5938df61",
    "7bba27202e8ba79a646fa17b74551dcc636e9eeb0c3d0b8d9c1545451a6e502e",
    "b48c6f31d56038d71522c6b6fc918f887750aff795f92e26c74cfac608822c05",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_authorization_and_binding_manifest_are_exactly_one_anchor():
    auth = load(DIR / "VISUAL_ANCHOR_RUNTIME_AUTHORIZATION_RECEIPT_V1.json")
    assert auth["authorization_state"] == "AUTHORIZED_FOR_THIS_HOLDOUT_RUN"
    assert auth["source_authority"]["drive_task_file_id"] == "1mlpl6fWHPMC11nUUeXsu-34GkAI1iZzo"
    assert auth["canonical_anchor"]["drive_file_id"] == ANCHOR_ID
    assert auth["canonical_anchor"]["sha256"] == ANCHOR_SHA
    assert auth["canonical_anchor"]["runtime_reference_count"] == 1
    assert auth["scope"]["authorizes_image_generation_in_this_codex_task"] is False

    manifest = load(DIR / "RUNTIME_VISUAL_ANCHOR_BINDING_MANIFEST_V1.json")
    assert manifest["reference_image_count"] == 1
    assert len(manifest["positive_runtime_anchors"]) == 1
    assert manifest["positive_runtime_anchors"][0]["drive_file_id"] == ANCHOR_ID
    assert manifest["positive_runtime_anchors"][0]["sha256"] == ANCHOR_SHA
    assert all(value is False for key, value in manifest["binding_invariants"].items() if key != "same_single_anchor_for_all_four_payloads")
    assert manifest["binding_invariants"]["same_single_anchor_for_all_four_payloads"] is True
    assert manifest["execution_boundary"]["images_generated_by_this_freeze_task"] is False


def test_four_payloads_are_new_frozen_and_anchor_bound():
    expected = {
        "H1": ("d8b1e301742f07918c9036e8f92a04ee974baa1605908287a9084fe0b616f5f7", "3:4"),
        "H2": ("18f899b6fa78d3bce78997fbba325a0f237fc9482eb99eb3f65614753e6c25bc", "3:4"),
        "H3": ("97deab9813c792e3de97571c545f3ccd70ec522cacc226ade36d72e43a5be99f", "3:4"),
        "H4": ("f1e695e7dd3499138cef8ee40d4b8be7bf4c1b62ccd4c3cea35bdaf8a238b28d", "9:16"),
    }
    seen = set()
    for challenge, (expected_hash, aspect) in expected.items():
        path = DIR / f"{challenge}_CONTROLLER_PAYLOAD.json"
        payload = load(path)
        assert sha256(path) == expected_hash
        assert payload["payload_state"] == "FROZEN"
        assert payload["challenge_id"] == challenge
        assert payload["aspect_intent"]["ratio"] == aspect
        assert payload["runtime_visual_anchor"]["reference_image_count"] == 1
        assert payload["runtime_visual_anchor"]["drive_file_id"] == ANCHOR_ID
        assert payload["runtime_visual_anchor"]["sha256"] == ANCHOR_SHA
        assert payload["output_count"] == 1
        assert payload["no_hidden_variants"] is True
        assert payload["no_best_of_n"] is True
        assert payload["no_unreported_retries"] is True
        current = sha256(path)
        assert current not in OLD_PAYLOAD_HASHES
        assert current not in seen
        seen.add(current)
    h3 = load(DIR / "H3_CONTROLLER_PAYLOAD.json")
    h4 = load(DIR / "H4_CONTROLLER_PAYLOAD.json")
    assert h4["comparison_payload_id"] == h3["experiment_id"]
    assert h4["communication_job"] == h3["communication_job"]
    assert h4["subject_process_class_id"] == h3["subject_process_class_id"]


def test_freeze_receipt_and_handoff_bind_hashes_without_outputs():
    receipt = load(DIR / "SYSTEM_LEVEL_HOLDOUT_PAYLOAD_FREEZE_RECEIPT_V1.json")
    assert receipt["experiment"]["formal_outputs"] == "0/4"
    assert receipt["experiment"]["generation_completed"] is False
    assert receipt["runtime_anchor"]["drive_file_id"] == ANCHOR_ID
    assert receipt["runtime_anchor"]["sha256"] == ANCHOR_SHA
    assert len(receipt["frozen_payloads"]) == 4
    assert receipt["render_handoff"]["sha256"] == sha256(DIR / "VPD_SHANYEJI_SYSTEM_LEVEL_HOLDOUT_CHATGPT_RENDER_HANDOFF_V1.txt")

    handoff = (DIR / "VPD_SHANYEJI_SYSTEM_LEVEL_HOLDOUT_CHATGPT_RENDER_HANDOFF_V1.txt").read_text(encoding="utf-8")
    for value in [ANCHOR_ID, ANCHOR_SHA, "d8b1e301742f07918c9036e8f92a04ee974baa1605908287a9084fe0b616f5f7", "18f899b6fa78d3bce78997fbba325a0f237fc9482eb99eb3f65614753e6c25bc", "97deab9813c792e3de97571c545f3ccd70ec522cacc226ade36d72e43a5be99f", "f1e695e7dd3499138cef8ee40d4b8be7bf4c1b62ccd4c3cea35bdaf8a238b28d"]:
        assert value in handoff
    assert "serial" in handoff.lower()
    assert "no hidden variants" in handoff.lower()
    assert "Figma" in handoff

    blocked = load(DIR / "SYSTEM_LEVEL_HOLDOUT_DRIVE_HANDOFF_UPLOAD_BLOCKED_RECEIPT_V1.json")
    assert blocked["drive_upload"]["status"] == "BLOCKED_USAGE_LIMIT"
    assert blocked["drive_upload"]["readback_verified"] is False
    assert blocked["drive_upload"]["workaround_attempted"] is False


def test_no_raster_outputs_and_unbound_diagnostics_are_invalid():
    forbidden = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".fig"}
    assert [path for path in DIR.rglob("*") if path.suffix.lower() in forbidden] == []
    diagnostics = load(DIR / "PRE_FREEZE_UNBOUND_DIAGNOSTIC_OUTPUTS_RECORD_V1.json")
    assert diagnostics["classification"] == "UNBOUND_DIAGNOSTIC_INVALID_FOR_FORMAL_HOLDOUT"
    assert diagnostics["evidence_boundary"]["formal_holdout_evaluation_allowed"] is False
