from __future__ import annotations

import binascii
import struct
import tempfile
import unittest
import uuid
import zlib
from pathlib import Path

from visual_memory.generation_bridge import (
    PROMPT_INVARIANTS,
    UNAVAILABLE_BY_PROVIDER,
    GenerationBridgeError,
    append_mandatory_prompt_invariants,
    build_pixel_review_receipt,
    build_renderer_receipt,
    build_renderer_request,
    classify_direct_reference_binding,
    diagnostic_eligibility,
    machine_integrity_gate,
    prepare_direct_reference_attachments,
    provider_field,
    validate_prompt_preservation,
)
from visual_memory.store import SCHEMA_VERSION, VisualMemoryStore, sha256_file, utc_now


def _png(width: int = 4, height: int = 4) -> bytes:
    def chunk(kind: bytes, payload: bytes) -> bytes:
        return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", binascii.crc32(kind + payload) & 0xFFFFFFFF)

    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    rows = b"".join(b"\x00" + (b"\x80\x40\x20" * width) for _ in range(height))
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"IDAT", zlib.compress(rows)) + chunk(b"IEND", b"")


class GenerationBridgeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.store = VisualMemoryStore(self.root)
        self.positive = [self._asset("positive-1"), self._asset("positive-2")]
        self.negative = [self._asset("negative-1")]
        self.context = {
            "domain": "餐饮",
            "positive_exemplars": self.positive,
            "negative_exemplars": self.negative,
            "source_event_ids": [],
        }

    def tearDown(self):
        self.temp.cleanup()

    def _asset(self, name: str) -> dict:
        sample_id = f"smp_{uuid.uuid4()}"
        asset_id = f"ast_{uuid.uuid4()}"
        path = self.store.vault_dir / f"{asset_id}.png"
        path.write_bytes(_png())
        sample = {
            "schema_version": SCHEMA_VERSION,
            "sample_id": sample_id,
            "created_at": utc_now(),
            "sample_kind": "imported",
            "primary_asset_id": asset_id,
            "dataset_role": "discovery",
            "provenance": {"source_type": "user_upload", "source_ref": None, "creator": None, "license": None},
            "user_tags": [name],
        }
        asset = {
            "schema_version": SCHEMA_VERSION,
            "asset_id": asset_id,
            "sample_id": sample_id,
            "created_at": utc_now(),
            "sha256": sha256_file(path),
            "locator_kind": "local_file",
            "locator": str(path.relative_to(self.store.root)),
            "asset_relation": "primary",
            "derived_from_asset_id": None,
            "media_type": "image/png",
        }
        self.store.write_sample(sample)
        self.store.write_asset(asset)
        return {"sample_id": sample_id, "asset_id": asset_id, "evidence_ids": [], "raw_text": name, "resolvable": True}

    def _prompt_parts(self):
        brief = "Create a synthetic restaurant food diagnostic."
        compiler_output = f"Primary request: {brief}\nUse one realistic food hero."
        final_prompt = append_mandatory_prompt_invariants(compiler_output)
        return brief, compiler_output, final_prompt

    def _pixel_checks(self, *, fail: str | None = None):
        checks = {
            "food_material_realism": "PASS",
            "structure_anatomy_if_applicable": "NOT_APPLICABLE",
            "natural_irregularity": "PASS",
            "oil_specular_realism": "PASS",
            "physical_contact_shadow": "PASS",
            "heat_steam_coherence": "PASS",
            "generic_template_collapse": "PASS",
            "obvious_ai_material": "PASS",
            "task_compliance": "PASS",
        }
        if fail:
            checks[fail] = "FAIL"
        return checks

    def test_positive_canonical_reference_has_direct_attachment_lineage(self):
        result = prepare_direct_reference_attachments(self.store, self.context)
        self.assertEqual(result["binding_classification"], "MULTIMODAL_BOUND")
        self.assertEqual(len(result["positive_attachments"]), 2)
        for attachment in result["positive_attachments"]:
            self.assertEqual(attachment["transport"], "CANONICAL_DIRECT")
            self.assertEqual(attachment["canonical_sha256"], attachment["attachment_sha256"])
            self.assertTrue(attachment["included_in_renderer_invocation"])

    def test_contact_sheet_cannot_satisfy_direct_binding(self):
        montage = [{
            "asset_id": self.positive[0]["asset_id"],
            "sample_id": self.positive[0]["sample_id"],
            "transport": "CONTACT_SHEET",
            "source_asset_count": 2,
            "source_sha256": "sha256:one",
            "canonical_sha256": "sha256:one",
            "attachment_sha256": "sha256:montage",
            "included_in_renderer_invocation": True,
        }]
        self.assertEqual(classify_direct_reference_binding(self.positive, montage), "UNPROVEN_BINDING")

    def test_rejected_image_cannot_silently_enter_positive_attachment_set(self):
        result = prepare_direct_reference_attachments(self.store, self.context)
        attached = {row["asset_id"] for row in result["positive_attachments"]}
        self.assertNotIn(self.negative[0]["asset_id"], attached)
        self.assertFalse(result["negative_reference_behavior"][0]["included_in_renderer_invocation"])
        bad = dict(self.context)
        bad["positive_exemplars"] = self.positive + self.negative
        with self.assertRaises(GenerationBridgeError):
            prepare_direct_reference_attachments(self.store, bad)

    def test_missing_prompt_invariant_blocks_render(self):
        brief, compiler_output, final_prompt = self._prompt_parts()
        final_prompt = final_prompt.replace(f"[PRODUCT_REALISM_PRIORITY] {PROMPT_INVARIANTS['PRODUCT_REALISM_PRIORITY']}", "")
        with self.assertRaises(GenerationBridgeError):
            validate_prompt_preservation(
                task_brief=brief,
                compiler_input={"task": brief},
                compiler_output=compiler_output,
                final_renderer_prompt=final_prompt,
            )

    def test_complete_prompt_invariants_allow_request(self):
        brief, compiler_output, final_prompt = self._prompt_parts()
        request = build_renderer_request(
            store=self.store,
            task_id="g2-synthetic",
            task_brief=brief,
            compiler_input={"task": brief},
            compiler_output=compiler_output,
            final_renderer_prompt=final_prompt,
            context_pack=self.context,
            tool_name="synthetic-renderer",
            ratio_request="1:1",
        )
        self.assertTrue(request["prompt_contract"]["all_invariants_preserved"])
        self.assertEqual(request["reference_transport"]["binding_classification"], "MULTIMODAL_BOUND")

    def test_unavailable_provider_field_is_explicit(self):
        field = provider_field(
            UNAVAILABLE_BY_PROVIDER,
            provenance="unavailable_by_provider",
            reason="The renderer tool does not expose a seed.",
        )
        self.assertEqual(field["value"], UNAVAILABLE_BY_PROVIDER)

    def test_guessed_provider_field_is_invalid(self):
        with self.assertRaises(GenerationBridgeError):
            provider_field("made-up-model", provenance="guessed")

    def test_renderer_receipt_captures_actual_attachment_identity(self):
        brief, compiler_output, final_prompt = self._prompt_parts()
        request = build_renderer_request(
            store=self.store,
            task_id="g2-synthetic",
            task_brief=brief,
            compiler_input={"task": brief},
            compiler_output=compiler_output,
            final_renderer_prompt=final_prompt,
            context_pack=self.context,
            tool_name="synthetic-renderer",
            ratio_request="1:1",
        )
        output = self.root / "output.png"
        output.write_bytes(_png())
        unavailable = provider_field(
            UNAVAILABLE_BY_PROVIDER,
            provenance="unavailable_by_provider",
            reason="Synthetic provider does not expose this field.",
        )
        receipt = build_renderer_receipt(
            request,
            output_path=output,
            provider_name=provider_field("synthetic", provenance="tool_exposed"),
            declared_model=unavailable,
            declared_model_version=unavailable,
            software_agent=unavailable,
            quality=unavailable,
            seed=unavailable,
            size=unavailable,
            invocation_evidence={
                "call_id": "call-synthetic",
                "status": "completed",
                "timestamp": utc_now(),
                "prompt_sha256": request["prompt_contract"]["prompt_sha256"],
            },
            actual_renderer_attachments=request["reference_transport"]["positive_attachments"],
        )
        self.assertEqual(
            receipt["actual_renderer_attachments"],
            request["reference_transport"]["positive_attachments"],
        )
        self.assertEqual(receipt["declared_model_version"]["value"], UNAVAILABLE_BY_PROVIDER)

    def test_renderer_receipt_rejects_attachment_identity_mismatch(self):
        brief, compiler_output, final_prompt = self._prompt_parts()
        request = build_renderer_request(
            store=self.store,
            task_id="g2-synthetic",
            task_brief=brief,
            compiler_input={"task": brief},
            compiler_output=compiler_output,
            final_renderer_prompt=final_prompt,
            context_pack=self.context,
            tool_name="synthetic-renderer",
            ratio_request="1:1",
        )
        output = self.root / "output.png"
        output.write_bytes(_png())
        unavailable = provider_field(
            UNAVAILABLE_BY_PROVIDER,
            provenance="unavailable_by_provider",
            reason="Synthetic provider does not expose this field.",
        )
        actual = [dict(row) for row in request["reference_transport"]["positive_attachments"]]
        actual[0]["attachment_sha256"] = "sha256:wrong"
        with self.assertRaises(GenerationBridgeError):
            build_renderer_receipt(
                request,
                output_path=output,
                provider_name=provider_field("synthetic", provenance="tool_exposed"),
                declared_model=unavailable,
                declared_model_version=unavailable,
                software_agent=unavailable,
                quality=unavailable,
                seed=unavailable,
                size=unavailable,
                invocation_evidence={
                    "call_id": "call-synthetic",
                    "status": "completed",
                    "timestamp": utc_now(),
                    "prompt_sha256": request["prompt_contract"]["prompt_sha256"],
                },
                actual_renderer_attachments=actual,
            )

    def test_extension_actual_mime_mismatch_fails(self):
        path = self.root / "not-a-jpeg.jpg"
        path.write_bytes(_png())
        with self.assertRaises(GenerationBridgeError):
            machine_integrity_gate(path, expected_ratio="1:1")

    def test_quality_gate_not_executed_cannot_enter_experiment(self):
        path = self.root / "output.png"
        path.write_bytes(_png())
        machine = machine_integrity_gate(path, expected_ratio="1:1")
        result = diagnostic_eligibility(machine, None)
        self.assertFalse(result["eligible"])
        self.assertEqual(result["status"], "BLOCKED_REAL_PIXEL_GATE_NOT_EXECUTED")

    def test_quality_gate_rejected_cannot_enter_experiment(self):
        path = self.root / "output.png"
        path.write_bytes(_png())
        machine = machine_integrity_gate(path, expected_ratio="1:1")
        review = build_pixel_review_receipt(
            output_sha256=machine["output_sha256"],
            reviewer_kind="chatgpt_pixel_reviewer",
            transport="GOOGLE_DRIVE_RAW_PIXEL_DOWNLOAD",
            evidence_ref="drive://synthetic",
            status="REJECTED_BELOW_FLOOR",
            checks=self._pixel_checks(fail="food_material_realism"),
        )
        result = diagnostic_eligibility(machine, review)
        self.assertFalse(result["eligible"])
        self.assertEqual(result["status"], "REJECTED_BELOW_FLOOR")

    def test_quality_gate_pass_is_eligible_for_diagnostic_only(self):
        path = self.root / "output.png"
        path.write_bytes(_png())
        machine = machine_integrity_gate(path, expected_ratio="1:1")
        review = build_pixel_review_receipt(
            output_sha256=machine["output_sha256"],
            reviewer_kind="human_pixel_reviewer",
            transport="GOOGLE_DRIVE_RAW_PIXEL_DOWNLOAD",
            evidence_ref="drive://synthetic",
            status="PASS_FOR_DIAGNOSTIC",
            checks=self._pixel_checks(),
        )
        result = diagnostic_eligibility(machine, review)
        self.assertTrue(result["eligible"])
        self.assertEqual(result["status"], "ELIGIBLE_FOR_DIAGNOSTIC_ONLY")
        self.assertFalse(result["production_quality_proven"])


if __name__ == "__main__":
    unittest.main()
