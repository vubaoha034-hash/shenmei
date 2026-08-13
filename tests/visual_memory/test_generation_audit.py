from __future__ import annotations

import unittest

from visual_memory.generation_audit import (
    GenerationAuditError,
    classify_reference_binding,
    summarize_absolute_quality,
    trace_summary,
    validate_trace,
)


def _base_trace(condition: str = "personalized") -> dict:
    return {
        "trace_version": "1",
        "trace_id": "trace_test",
        "task_id": "diag-01",
        "condition": condition,
        "task_text": "synthetic restaurant diagnostic",
        "route": {"route_id": "B", "evidence": "START_HERE route B"},
        "skills_read": [
            {"path": "skills/restaurant-poster-art-director/SKILL.md", "git_blob_sha": "abc"}
        ],
        "mandatory_files_read": [
            {"path": "generation/RESTAURANT_POSTER_IMAGE_RULES_V1.md", "git_blob_sha": "def"}
        ],
        "compiler": {"name": "synthetic", "output_text": "food hero, realistic, restrained"},
        "context": {
            "domain": "餐饮",
            "positive_exemplars": [
                {"sample_id": "s1", "asset_id": "a1"},
                {"sample_id": "s2", "asset_id": "a2"},
            ],
            "negative_exemplars": [],
            "source_event_ids": ["e1"],
        },
        "reference_bindings": [],
        "renderer": {
            "tool": "synthetic-renderer",
            "model": "synthetic-model",
            "model_version": "1",
            "ratio": "4:5",
            "parameters": {},
            "final_prompt": "food hero, realistic, restrained",
        },
        "output": {"sample_id": "out-s", "asset_id": "out-a", "sha256": "sha256:out"},
        "quality_gate": {
            "realism_status": "PASS",
            "design_status": "PASS",
            "absolute_quality": "USABLE",
            "reasons": [],
        },
    }


class GenerationAuditTests(unittest.TestCase):
    def test_no_bindings_is_text_only(self):
        trace = _base_trace()
        self.assertEqual(
            classify_reference_binding(trace["context"]["positive_exemplars"], []),
            "TEXT_ONLY_PERSONALIZATION",
        )

    def test_all_hash_matched_bindings_are_multimodal(self):
        trace = _base_trace()
        bindings = [
            {
                "asset_id": "a1",
                "asset_sha256": "sha256:1",
                "resolved_path_or_private_ref": "private://a1",
                "renderer_attachment_present": True,
                "renderer_attachment_sha256": "sha256:1",
                "renderer_attachment_index": 0,
            },
            {
                "asset_id": "a2",
                "asset_sha256": "sha256:2",
                "resolved_path_or_private_ref": "private://a2",
                "renderer_attachment_present": True,
                "renderer_attachment_sha256": "sha256:2",
                "renderer_attachment_index": 1,
            },
        ]
        self.assertEqual(
            classify_reference_binding(trace["context"]["positive_exemplars"], bindings),
            "MULTIMODAL_BOUND",
        )

    def test_partial_bindings_are_partial(self):
        trace = _base_trace()
        bindings = [
            {
                "asset_id": "a1",
                "asset_sha256": "sha256:1",
                "resolved_path_or_private_ref": "private://a1",
                "renderer_attachment_present": True,
                "renderer_attachment_sha256": "sha256:1",
            }
        ]
        self.assertEqual(
            classify_reference_binding(trace["context"]["positive_exemplars"], bindings),
            "PARTIAL_MULTIMODAL_BOUND",
        )

    def test_mismatched_hash_is_not_proven(self):
        trace = _base_trace()
        bindings = [
            {
                "asset_id": "a1",
                "asset_sha256": "sha256:1",
                "resolved_path_or_private_ref": "private://a1",
                "renderer_attachment_present": True,
                "renderer_attachment_sha256": "sha256:other",
            }
        ]
        self.assertEqual(
            classify_reference_binding(trace["context"]["positive_exemplars"], bindings),
            "UNPROVEN_BINDING",
        )

    def test_trace_requires_compiler_output(self):
        trace = _base_trace()
        trace["compiler"]["output_text"] = ""
        with self.assertRaises(GenerationAuditError):
            validate_trace(trace)

    def test_trace_requires_skill_evidence(self):
        trace = _base_trace()
        trace["skills_read"] = []
        with self.assertRaises(GenerationAuditError):
            validate_trace(trace)

    def test_trace_summary_includes_binding_and_quality(self):
        trace = _base_trace()
        trace["reference_bindings"] = [
            {
                "asset_id": "a1",
                "asset_sha256": "sha256:1",
                "resolved_path_or_private_ref": "private://a1",
                "renderer_attachment_present": True,
                "renderer_attachment_sha256": "sha256:1",
            }
        ]
        summary = trace_summary(trace)
        self.assertEqual(summary["binding_classification"], "PARTIAL_MULTIMODAL_BOUND")
        self.assertEqual(summary["absolute_quality"], "USABLE")
        self.assertTrue(summary["trace_sha256"].startswith("sha256:"))

    def test_absolute_quality_is_separate_by_condition(self):
        a = _base_trace("baseline")
        a["trace_id"] = "a"
        a["quality_gate"]["absolute_quality"] = "UNUSABLE"
        b = _base_trace("personalized")
        b["trace_id"] = "b"
        b["quality_gate"]["absolute_quality"] = "UNUSABLE"
        c = _base_trace("expert_direct")
        c["trace_id"] = "c"
        c["quality_gate"]["absolute_quality"] = "USABLE"
        result = summarize_absolute_quality([a, b, c])
        self.assertEqual(result["by_condition"]["baseline"]["UNUSABLE"], 1)
        self.assertEqual(result["by_condition"]["personalized"]["UNUSABLE"], 1)
        self.assertEqual(result["by_condition"]["expert_direct"]["USABLE"], 1)


if __name__ == "__main__":
    unittest.main()
