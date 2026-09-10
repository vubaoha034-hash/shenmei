from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "evidence" / "vpd" / "shanyeji" / "system_level_holdout_validation_v1"
EXPECTED = {
    "H1_CONTROLLER_PAYLOAD.json": "d8b1e301742f07918c9036e8f92a04ee974baa1605908287a9084fe0b616f5f7",
    "H2_CONTROLLER_PAYLOAD.json": "18f899b6fa78d3bce78997fbba325a0f237fc9482eb99eb3f65614753e6c25bc",
    "H3_CONTROLLER_PAYLOAD.json": "97deab9813c792e3de97571c545f3ccd70ec522cacc226ade36d72e43a5be99f",
    "H4_CONTROLLER_PAYLOAD.json": "f1e695e7dd3499138cef8ee40d4b8be7bf4c1b62ccd4c3cea35bdaf8a238b28d",
    "RUNTIME_VISUAL_ANCHOR_BINDING_MANIFEST_V1.json": "d8880a328524c26eee16df2cddf8914e4338b04ea193736a76c480ec3602825c",
    "SYSTEM_LEVEL_HOLDOUT_PAYLOAD_FREEZE_RECEIPT_V1.json": "32255718f315deb3a4dbebee9d3aa5eb6a14b0469b9cdce73363b6f433786867",
}


def load(name: str):
    return json.loads((DIR / name).read_text(encoding="utf-8"))


def sha256(name: str) -> str:
    return hashlib.sha256((DIR / name).read_bytes()).hexdigest()


def test_attempt1_settlement_is_protocol_invalid_without_capsule_inference():
    settlement = load("FORMAL_RENDER_ATTEMPT1_PROTOCOL_INVALID_SETTLEMENT_V1.json")
    assert settlement["classification"] == "PROTOCOL_INVALID"
    assert settlement["formal_holdout_verdict"] == "INVALID_FOR_FORMAL_HOLDOUT_VERDICT"
    assert settlement["capsule_inference"] == "NO_CAPSULE_INFERENCE"
    assert len(settlement["reasons"]) == 4
    assert settlement["evidence_boundary"]["attempt1_images_are_capsule_evidence"] is False
    assert settlement["transition"]["new_payloads_created"] is False


def test_attempt2_identity_and_preflight_bind_existing_frozen_inputs():
    identity = load("FORMAL_RENDER_ATTEMPT2_IDENTITY_V1.json")
    assert identity["identity_id"] == "SHANYEJI_SYSTEM_LEVEL_HOLDOUT_TRANSFER_RENDER_ATTEMPT2"
    assert identity["attempt_number"] == 2
    assert identity["payload_semantics"] == "H1_H2_H3_H4_FROZEN_BYTES_UNCHANGED"
    assert identity["payloads_created"] is False
    assert identity["runtime_anchor"]["reference_image_count"] == 1
    assert identity["runtime_anchor"]["sha256"] == "9a29fbdc7dd908017924bed270e8dfe18351519eed3fa7bc7001789f2a383414"
    for name, expected in EXPECTED.items():
        assert sha256(name) == expected
        if name.startswith("H"):
            assert identity["frozen_payloads"][name[:2]]["sha256"] == expected

    checklist = load("FORMAL_RENDER_ATTEMPT2_PREFLIGHT_CHECKLIST_V1.json")
    assert checklist["fail_closed"] is True
    assert checklist["preflight_result"] == "PENDING_EXTERNAL_CHATGPT_RENDER_PREFLIGHT"
    assert checklist["global_gates"]["no_other_images_attached"] is True
    assert checklist["global_gates"]["hidden_variants_best_of_n_and_pre_evaluation_retry"] is False
    assert checklist["challenge_gates"]["H1"]["scenic_mountain_forest_prohibited"] is True
    assert checklist["challenge_gates"]["H1"]["cool_neutral_morning_behavior_required"] is True


def test_attempt2_handoff_preserves_each_frozen_renderer_instruction():
    handoff = (DIR / "VPD_SHANYEJI_SYSTEM_LEVEL_HOLDOUT_CHATGPT_RENDER_HANDOFF_ATTEMPT2_V1.txt").read_text(encoding="utf-8")
    assert "SHANYEJI_SYSTEM_LEVEL_HOLDOUT_TRANSFER_RENDER_ATTEMPT2" in handoff
    assert "Generation only: no evaluation, human review, Figma" in handoff
    for name in ("H1_CONTROLLER_PAYLOAD.json", "H2_CONTROLLER_PAYLOAD.json", "H3_CONTROLLER_PAYLOAD.json", "H4_CONTROLLER_PAYLOAD.json"):
        payload = load(name)
        assert payload["renderer_instruction"] in handoff
    assert handoff.count("Compliance checklist before instruction:") == 4
    assert "Attempt-1 visible outputs are prohibited" not in handoff or "Attempt-1" in handoff
    assert "No hidden variants, alternates, best-of-N" in handoff
    assert "END OF HANDOFF" in handoff


def test_creation_receipt_and_checkpoint_ledger_are_consistent():
    # Historical sequence 22, preserved byte-for-byte; current state has a separate guard.
    receipt = load("FORMAL_RENDER_ATTEMPT2_CREATION_RECEIPT_V1.json")
    assert receipt["attempt1_settlement"]["classification"] == "PROTOCOL_INVALID / INVALID_FOR_FORMAL_HOLDOUT_VERDICT / NO_CAPSULE_INFERENCE"
    assert receipt["attempt2_identity"]["identity"] == "SHANYEJI_SYSTEM_LEVEL_HOLDOUT_TRANSFER_RENDER_ATTEMPT2"
    assert receipt["execution_boundary"]["images_generated"] is False
    assert receipt["execution_boundary"]["figma_executed"] is False
    assert receipt["execution_boundary"]["evaluation_executed"] is False
    assert receipt["frozen_payload_integrity"]["H4"] == EXPECTED["H4_CONTROLLER_PAYLOAD.json"]

    checkpoint = json.loads((ROOT / "continuity" / "vpd" / "history" / "sequence_22" / "LATEST_CHECKPOINT.json").read_text(encoding="utf-8"))
    assert checkpoint["sequence"] == 22
    assert checkpoint["status"] == "VPD_FORMAL_RENDER_ATTEMPT1_INVALID_ATTEMPT2_READY_FOR_CHATGPT_RENDER"
    assert checkpoint["next_required_action"] == "RETURN_TO_CHATGPT_FOR_FORMAL_RENDER_ATTEMPT2_H1_H2_H3_H4"
    assert checkpoint["ledger_tails"]["system_validation"] == {
        "event_id": "EVT-VISUAL-VPD-FORMAL-RENDER-ATTEMPT1-INVALID-ATTEMPT2-READY-20260907-001",
        "event_hash": "2aac3fe5ba3cfe5813538edf25ff96feac722e2204749c70b389fc4b1570146c",
    }
    events = [json.loads(line) for line in (ROOT / "continuity" / "vpd" / "history" / "sequence_22" / "system_validation.jsonl").read_text(encoding="utf-8").splitlines()]
    assert len(events) == 3
    event = events[-1]
    asserted = dict(event)
    event_hash = asserted.pop("event_hash")
    canonical = json.dumps(asserted, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    assert event_hash == "2aac3fe5ba3cfe5813538edf25ff96feac722e2204749c70b389fc4b1570146c"
    assert hashlib.sha256(canonical).hexdigest() == event_hash


def test_no_attempt2_outputs_or_raster_artifacts_created():
    forbidden = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".fig"}
    assert [p for p in DIR.rglob("*") if p.suffix.lower() in forbidden] == []
