#!/usr/bin/env python3
"""Atomically authorize one controlled Doufang B relay retry after a verified placement probe.

This is a one-time P6 authority transition. It does not upload raster bytes and it does
not claim any formal binding. It only moves the state from placement-mismatch diagnosis
back to the normal ordered relay action after the isolated placement protocol was
verified in the same Figma file.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRANCH_HEAD = "fd2d03cf6e5be4ca856e3d4e102eee7262c5f80e"
NOW = "2026-09-13T21:41:00Z"
LOCK_PATH = ROOT / "continuity/vpd/CURRENT_TASK_LOCK.json"
CP_PATH = ROOT / "continuity/vpd/LATEST_CHECKPOINT.json"
ADAPTER_PATH = ROOT / "PROJECT_CONTROL_ADAPTER.json"
LEDGER_PATH = ROOT / "continuity/vpd/state_ledger/system_validation.jsonl"
PROBE_RECEIPT_PATH = ROOT / "evidence/vpd/figma_upload_relay/receipts/P6-PLACEMENT-PROBE-20260913-01.json"
PROBE_EVIDENCE_REL = "evidence/vpd/p6_authority_repair_v1/P6_PLACEMENT_PROTOCOL_PROBE_VERIFIED_20260914.json"
PROBE_EVIDENCE_PATH = ROOT / PROBE_EVIDENCE_REL

OLD_STATUS = "VPD_P6_RELAY_UPLOAD_PASS_PLACEMENT_MISMATCH_BLOCKED"
NEW_STATUS = "VPD_P6_RELAY_PLACEMENT_PROTOCOL_VERIFIED_DOUFANG_B_RETRY_READY"
OLD_ACTION = "RESOLVE_P6_RELAY_PLACEMENT_MISMATCH_NO_REUPLOAD"
NEW_ACTION = "RUN_LIVE_DOUFANG_B_RELAY"
LOCK_SHA256_OLD = "0cf20eb6a0824018d4b137e147cca7f4e4fdab98c50f386258a99bd64731dcf6"
LOCK_BLOB_OLD = "75d0558a06a0ec42142cb1afd9ede8f8d5c0af52"
PROBE_HASH = "582220b50db8d380597a2c240de216fa9ec24ce4"
PROBE_SOURCE_SHA256 = "d333d4fc614379a3b9a3b95661d8b1c76cc38a73f68358234a9699fa94e52829"
DOUFANG_B_SOURCE_SHA256 = "78137a59779a37f08b4df3aef23164d115cc61afb443610b6f6eb066e99671d9"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def canonical_event_hash(event_without_hash: dict) -> str:
    payload = json.dumps(event_without_hash, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def main() -> None:
    lock = read_json(LOCK_PATH)
    cp = read_json(CP_PATH)
    adapter = read_json(ADAPTER_PATH)
    receipt = read_json(PROBE_RECEIPT_PATH)

    assert lock["revision"] == 26
    assert lock["status"] == OLD_STATUS
    assert lock["next_required_action"] == OLD_ACTION
    assert cp["sequence"] == 48 and cp["status"] == OLD_STATUS and cp["next_required_action"] == OLD_ACTION
    assert adapter["task_lock"]["revision"] == 26
    assert adapter["task_lock"]["sha256"] == LOCK_SHA256_OLD
    assert adapter["vpd_system_goal_authority"]["checkpoint"] == OLD_STATUS
    assert adapter["vpd_system_goal_authority"]["next_required_action"] == OLD_ACTION
    assert sha256_file(LOCK_PATH) == LOCK_SHA256_OLD
    assert lock["p6_integrated_design"]["bound_count"] == 1
    assert [f["bound"] for f in lock["p6_integrated_design"]["frames"]] == [True, False, False, False]
    assert lock["p6_integrated_design"]["frames"][1]["photo"] == "12:12"
    assert "relay_placement_blocker" in lock

    assert receipt["status"] == "UPLOAD_PASS"
    assert receipt["http_status"] == "200"
    assert receipt["node_id"] == "40:3"
    assert receipt["source_sha256"] == PROBE_SOURCE_SHA256
    assert receipt["response"]["imageHash"] == PROBE_HASH

    probe_evidence = {
        "schema_version": "vpd-p6-placement-protocol-probe-verification/v1",
        "project_id": "visual-aesthetic-vpd",
        "task_id": "VPD-SYSTEM-LEVEL-HOLDOUT-TRANSFER-VALIDATION-V1",
        "repository": "vubaoha034-hash/shenmei",
        "branch": "visual-program-distillation-v2-photography-design-20260814",
        "input_head": BRANCH_HEAD,
        "status": "PASS_PLACEMENT_PROTOCOL_VERIFIED_SAME_FILE",
        "scope": "ISOLATED_DIAGNOSTIC_ONLY_NO_FORMAL_P6_BINDING",
        "figma_file_key": "uyDxOoN1iNDPpEHTKSUWg1",
        "probe": {
            "page_id": "40:2",
            "target_node_id": "40:3",
            "target_node_name": "PLACEMENT_PROBE_TARGET",
            "source_sha256": PROBE_SOURCE_SHA256,
            "source_size": 583,
            "receipt_path": "evidence/vpd/figma_upload_relay/receipts/P6-PLACEMENT-PROBE-20260913-01.json",
            "http_status": 200,
            "receipt_status": "UPLOAD_PASS",
            "returned_image_hash": PROBE_HASH,
            "live_figma_readback": {
                "node_locked": False,
                "fill_type": "IMAGE",
                "scale_mode": "FILL",
                "node_image_hash": PROBE_HASH,
                "image_store_present": True,
                "image_store_width": 96,
                "image_store_height": 96,
                "image_store_bytes": 583
            }
        },
        "formal_target_pretransition": {
            "node_id": "12:12",
            "name": "PHOTO_RAW_LOCKED",
            "locked": False,
            "fill_type": "IMAGE",
            "scale_mode": "FILL",
            "image_hash": "7f57313e7409ff16d76ab867893a1229a5769962",
            "modified_by_probe": False
        },
        "established": [
            "The same Figma file accepts node-targeted upload_assets placement through the encrypted relay.",
            "The probe image entered the file image store and the target node fill hash matched the relay-returned image hash.",
            "Relay secret, HTTP POST transport, file write permission, default single-asset commit and node-targeted placement are therefore operational for the verified protocol.",
            "The historical Doufang B mismatch remains a historical failed placement transaction and is not reclassified as a binding pass."
        ],
        "authorization_consequence": {
            "one_controlled_doufang_b_retry_allowed": True,
            "required_node_id": "12:12",
            "required_source_sha256": DOUFANG_B_SOURCE_SHA256,
            "required_upload_assets_mode": "nodeIds:[12:12], count:1, scaleMode:FILL, default non-batch commit",
            "tea_a_b_still_blocked_until_doufang_b_binding_pass": True,
            "success_requires": [
                "relay receipt UPLOAD_PASS / HTTP 200",
                "returned imageHash exists in current Figma file image store",
                "node 12:12 IMAGE/FILL imageHash equals returned imageHash",
                "non-photo nodes unchanged",
                "screenshot verified"
            ]
        },
        "recorded_at": NOW
    }
    write_json(PROBE_EVIDENCE_PATH, probe_evidence)
    probe_evidence_sha = sha256_file(PROBE_EVIDENCE_PATH)

    lock["revision"] = 27
    lock["preserved_prior_revision"] = {
        "revision": 26,
        "git_blob_sha": LOCK_BLOB_OLD,
        "note": "Revision 26 preserved the historical Doufang B HTTP-200 placement mismatch and prohibited blind reupload."
    }
    lock["p6_integrated_design"]["status"] = "PLACEMENT_PROTOCOL_VERIFIED_DOUFANG_B_RETRY_READY"
    lock["figma_upload_relay"]["status"] = "PLACEMENT_PROTOCOL_VERIFIED_DOUFANG_B_RETRY_READY"
    lock["current_stage"] = (
        "An isolated node-targeted placement probe in the same Figma file passed end-to-end: relay HTTP 200, "
        "returned imageHash present in the file image store, and target node 40:3 fill hash matched. The formal "
        "node 12:12 remains unchanged. One controlled Doufang B retry is now authorized with nodeIds:[12:12]; "
        "Tea A/B remain gated until Doufang B binding passes."
    )
    lock["status"] = NEW_STATUS
    lock["next_required_action"] = NEW_ACTION
    lock["completed_this_revision"] = [
        "isolated same-file placement probe transport receipt verified",
        "live Figma probe node 40:3 readback matched returned imageHash",
        "live Figma image store contains the probe hash with 96x96 / 583-byte source",
        "formal node 12:12 revalidated unchanged before retry authorization",
        "one controlled Doufang B retry authorized without changing any design node"
    ]
    lock["updated_at"] = NOW
    lock["input_commit"] = BRANCH_HEAD
    lock["blockers"] = [
        "Doufang B formal binding remains incomplete until the newly authorized controlled retry passes full placement verification.",
        "Tea A/B remain blocked until ordered Doufang B binding passes.",
        "Historical ledger prefix preserved with three known event-hash defects; not recertified."
    ]
    lock.pop("relay_placement_blocker", None)
    lock["relay_placement_protocol_probe"] = {
        "path": PROBE_EVIDENCE_REL,
        "sha256": probe_evidence_sha
    }
    write_json(LOCK_PATH, lock)
    lock_sha = sha256_file(LOCK_PATH)

    cp["sequence"] = 49
    cp["recorded_at"] = NOW
    cp["current_focus"] = lock["current_stage"]
    if "p6_placement_protocol_probe_pass" not in cp["completed"]:
        cp["completed"].append("p6_placement_protocol_probe_pass")
    cp["blocked"] = list(lock["blockers"])
    cp["next_required_action"] = NEW_ACTION
    cp["relay"]["status"] = "PLACEMENT_PROTOCOL_VERIFIED_DOUFANG_B_RETRY_READY"
    cp["status"] = NEW_STATUS
    cp["task_lock"] = {"path": "continuity/vpd/CURRENT_TASK_LOCK.json", "sha256": lock_sha}
    cp["requirements"]["p6_integrated_design"]["status"] = "PLACEMENT_PROTOCOL_VERIFIED_DOUFANG_B_RETRY_READY"

    adapter["vpd_system_goal_authority"]["checkpoint"] = NEW_STATUS
    adapter["vpd_system_goal_authority"]["next_required_action"] = NEW_ACTION
    adapter["task_lock"]["revision"] = 27
    adapter["task_lock"]["sha256"] = lock_sha

    raw = LEDGER_PATH.read_bytes()
    lines = raw.splitlines()
    previous = json.loads(lines[-1].decode("utf-8"))
    assert previous["event_id"] == cp["ledger_tails"]["system_validation"]["event_id"]
    assert previous["event_hash"] == cp["ledger_tails"]["system_validation"]["event_hash"]
    event = {
        "schema_version": "upcp-state-ledger-event/v1",
        "event_id": "EVT-VPD-P6-PLACEMENT-PROTOCOL-PROBE-PASS-20260914-001",
        "event_type": "P6_PLACEMENT_PROTOCOL_PROBE_PASS_DOUFANG_B_RETRY_AUTHORIZED",
        "stream_id": "system_validation",
        "project_id": "visual-aesthetic-vpd",
        "task_id": "VPD-SYSTEM-LEVEL-HOLDOUT-TRANSFER-VALIDATION-V1",
        "previous_event_id": previous["event_id"],
        "previous_event_hash": previous["event_hash"],
        "recorded_at": NOW,
        "input_remote_head": BRANCH_HEAD,
        "lock_sha256": lock_sha,
        "scope": "PLACEMENT_PROTOCOL_VERIFIED_ONE_CONTROLLED_DOUFANG_B_RETRY_ONLY",
        "probe": {"path": PROBE_EVIDENCE_REL, "sha256": probe_evidence_sha},
        "next_required_action": NEW_ACTION
    }
    event["event_hash"] = canonical_event_hash(event)
    if raw and not raw.endswith(b"\n"):
        raw += b"\n"
    raw += (json.dumps(event, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
    LEDGER_PATH.write_bytes(raw)
    cp["ledger_tails"]["system_validation"] = {
        "event_id": event["event_id"],
        "event_hash": event["event_hash"]
    }

    write_json(CP_PATH, cp)
    write_json(ADAPTER_PATH, adapter)

    # Final internal consistency assertions before the external validator runs.
    assert read_json(CP_PATH)["task_lock"]["sha256"] == sha256_file(LOCK_PATH)
    assert read_json(ADAPTER_PATH)["task_lock"]["sha256"] == sha256_file(LOCK_PATH)
    assert read_json(ADAPTER_PATH)["vpd_system_goal_authority"]["checkpoint"] == NEW_STATUS
    assert read_json(ADAPTER_PATH)["vpd_system_goal_authority"]["next_required_action"] == NEW_ACTION


if __name__ == "__main__":
    main()
