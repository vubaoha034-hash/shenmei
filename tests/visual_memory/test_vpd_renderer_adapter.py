from __future__ import annotations

import base64
import binascii
import json
import struct
import tempfile
import unittest
import zlib
from pathlib import Path

from visual_memory.vpd_renderer_adapter import (
    FREEZE_SCHEMA,
    HTTPResult,
    UNAVAILABLE_BY_PROVIDER,
    VPDRendererAdapterError,
    execute_task,
    text_sha256,
    validate_freeze,
)


def _png(width: int = 1024, height: int = 1536) -> bytes:
    def chunk(kind: bytes, payload: bytes) -> bytes:
        return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", binascii.crc32(kind + payload) & 0xFFFFFFFF)

    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    row = b"\x00" + (b"\x20\x40\x80" * width)
    rows = row * height
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"IDAT", zlib.compress(rows, 1)) + chunk(b"IEND", b"")


def _task(task_id: str) -> dict:
    prompt = f"EXACT {task_id} payload"
    return {
        "test_id": task_id,
        "task_type": task_id,
        "reference_runtime_policy": "NONE",
        "explicit_runtime_reference_image_count": 0,
        "context_isolation_proven": "YES",
        "render_allowed": "YES",
        "provider_internal_prompt": UNAVAILABLE_BY_PROVIDER,
        "final_renderer_payload": prompt,
        "final_renderer_payload_sha256": text_sha256(prompt),
        "renderer_settings_if_exposed": {
            "size": "1024x1536",
            "n": 1,
            "referenced_image_ids": None,
        },
        "production_typography": "NOT_EVALUATED",
        "planned_output_filename": f"{task_id}.png",
    }


def _freeze() -> dict:
    return {
        "schema_version": FREEZE_SCHEMA,
        "project_id": "visual-aesthetic-vpd-test",
        "protocol": "VPD_DISTILLATION_ONLY_RUNTIME_TEST_V1.md",
        "fresh_context_preflight": {
            "verdict": "FRESH_CONTEXT_PREFLIGHT_PASS",
            "approved_reference_pixels_loaded": False,
            "mother_reference_loaded": False,
            "golden_exemplar_loaded": False,
            "contact_sheet_loaded": False,
            "drive_preview_loaded": False,
            "previous_vpd_output_images_loaded": False,
            "drive_accessed": False,
            "github_text_only_before_freeze": True,
            "reference_runtime_policy": "NONE",
            "explicit_runtime_reference_image_count": 0,
            "provider_internal_prompt": UNAVAILABLE_BY_PROVIDER,
            "context_isolation_proven": "YES",
            "render_allowed": "YES",
        },
        "output_budget": {
            "formal_outputs": 3,
            "one_per_task": True,
            "hidden_variants": 0,
            "best_of_n": "NO",
            "aesthetic_retries": 0,
            "technical_retry_max_per_task": 1,
        },
        "tasks": [_task("T1"), _task("T2"), _task("T3")],
    }


class VPDRendererAdapterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.freeze_path = self.root / "freeze.json"
        self.freeze_path.write_text(json.dumps(_freeze(), ensure_ascii=False), encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def test_dry_run_persists_exact_prompt_before_network(self):
        out = self.root / "out"
        result = execute_task(self.freeze_path, "T1", out, allow_network=False)
        self.assertEqual(result["status"], "DRY_RUN_PASS")
        receipt = json.loads((out / "receipts" / "T1_pre_request.json").read_text(encoding="utf-8"))
        self.assertEqual(receipt["request_body"]["prompt"], "EXACT T1 payload")
        self.assertTrue(receipt["exact_prompt_binding_proven"])
        self.assertEqual(receipt["reference_runtime_policy"], "NONE")
        self.assertEqual(receipt["reference_images_attached"], 0)
        self.assertFalse(receipt["authorization_header_persisted"])

    def test_hash_drift_fails_closed_before_network(self):
        frozen = _freeze()
        frozen["tasks"][0]["final_renderer_payload_sha256"] = "0" * 64
        self.freeze_path.write_text(json.dumps(frozen), encoding="utf-8")
        with self.assertRaisesRegex(VPDRendererAdapterError, "SHA mismatch"):
            execute_task(self.freeze_path, "T1", self.root / "out", allow_network=False)

    def test_reference_policy_drift_fails_closed(self):
        frozen = _freeze()
        frozen["tasks"][1]["reference_runtime_policy"] = "EXEMPLAR_BOUND"
        self.freeze_path.write_text(json.dumps(frozen), encoding="utf-8")
        with self.assertRaisesRegex(VPDRendererAdapterError, "reference_runtime_policy"):
            validate_freeze(frozen)

    def test_fake_provider_round_trip_preserves_prompt_and_geometry(self):
        image = _png()

        def fake_http_post(url, body, headers, timeout):
            request = json.loads(body.decode("utf-8"))
            self.assertEqual(request["prompt"], "EXACT T2 payload")
            self.assertEqual(request["model"], "gpt-image-2-2026-04-21")
            self.assertEqual(request["size"], "1024x1536")
            self.assertIn("Authorization", headers)
            response = {
                "created": 1,
                "data": [{"b64_json": base64.b64encode(image).decode("ascii")}],
                "usage": {"total_tokens": 1},
            }
            return HTTPResult(
                status=200,
                headers={"x-request-id": "req_synthetic"},
                body=json.dumps(response).encode("utf-8"),
            )

        out = self.root / "out"
        receipt = execute_task(
            self.freeze_path,
            "T2",
            out,
            api_key="synthetic-secret",
            allow_network=True,
            http_post=fake_http_post,
        )
        self.assertEqual(receipt["provider_request_id"], "req_synthetic")
        self.assertEqual(receipt["dimensions"], "1024x1536")
        self.assertEqual(receipt["technical_validity"], "PASS")
        self.assertEqual(receipt["reference_images_attached"], 0)
        self.assertTrue((out / "T2.png").exists())

    def test_wrong_provider_geometry_is_technical_failure(self):
        image = _png(1536, 1024)

        def fake_http_post(url, body, headers, timeout):
            response = {"data": [{"b64_json": base64.b64encode(image).decode("ascii")}]} 
            return HTTPResult(200, {}, json.dumps(response).encode("utf-8"))

        out = self.root / "out"
        with self.assertRaisesRegex(VPDRendererAdapterError, "geometry mismatch"):
            execute_task(
                self.freeze_path,
                "T3",
                out,
                api_key="synthetic-secret",
                allow_network=True,
                http_post=fake_http_post,
            )
        failure = json.loads((out / "receipts" / "T3_technical_failure.json").read_text(encoding="utf-8"))
        self.assertTrue(failure["network_request_sent"])
        self.assertEqual(failure["reference_images_attached"], 0)


if __name__ == "__main__":
    unittest.main()
