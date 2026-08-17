import copy
import json
import subprocess
import unittest
from pathlib import Path

from visual_memory.distillation_v3 import (
    DistillationValidationError,
    validate_display_lettering_source_pipeline,
    validate_mechanism,
    validate_shanyeji_figma_producibility_map,
    validate_typography_component_evidence_contract,
    validate_typography_evidence,
    validate_typography_hypothesis,
)


ROOT = Path(__file__).resolve().parents[2]


def load(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


class TypographyPostReviewShanYeJiV3Tests(unittest.TestCase):
    def setUp(self):
        self.h05 = load("V3_TYPOGRAPHY_HYPOTHESIS_REFERENCE_05.json")
        self.h13 = load("V3_TYPOGRAPHY_HYPOTHESIS_REFERENCE_13.json")
        self.syj_evidence = load("V3_TYPOGRAPHY_EVIDENCE_SHANYEJI.json")
        self.syj_hypothesis = load("V3_TYPOGRAPHY_HYPOTHESIS_SHANYEJI.json")
        self.library = load("V3_VISUAL_MECHANISM_LIBRARY.json")

    def test_reference_05_bilingual_is_supporting_not_stable(self):
        stable = {row["mechanism_id"] for row in self.h05["stable_typography_grammar"]}
        self.assertNotIn("mech_05_dual_script_support_system", stable)
        self.assertTrue(any("OPTIONAL_VARIATION / SUPPORTING_MECHANISM" in row["statement"] for row in self.h05["variation_axes_typography"]))
        mechanism = next(row for row in self.library["mechanisms"] if row["mechanism_id"] == "mech_05_dual_script_support_system")
        self.assertEqual(mechanism["grammar_role"], "OPTIONAL_VARIATION / SUPPORTING_MECHANISM")

    def test_reference_13_side_rail_and_bilingual_are_not_stable(self):
        stable = {row["mechanism_id"] for row in self.h13["stable_typography_grammar"]}
        self.assertNotIn("mech_13_editorial_side_rail", stable)
        self.assertNotIn("mech_13_dual_script_editorial_support", stable)
        by_id = {row["mechanism_id"]: row for row in self.library["mechanisms"]}
        self.assertEqual(by_id["mech_13_editorial_side_rail"]["grammar_role"], "OPTIONAL_OR_EQUIVALENT_COUNTERWEIGHT")
        self.assertEqual(by_id["mech_13_dual_script_editorial_support"]["grammar_role"], "OPTIONAL_VARIATION / SUPPORTING_MECHANISM")

    def test_display_lettering_pipeline_has_three_routes_and_never_auto_promotes(self):
        pipeline = load("V3_DISPLAY_LETTERING_SOURCE_PIPELINE_CONTRACT.json")
        self.assertIs(validate_display_lettering_source_pipeline(pipeline), pipeline)
        self.assertEqual(len(pipeline["routes"]), 3)
        self.assertEqual(pipeline["promotion_status"], "UNPROMOTED")
        self.assertIn("exact_copy", pipeline["required_common_record"])
        broken = copy.deepcopy(pipeline)
        broken["promotion_status"] = "PROMOTED"
        with self.assertRaises(DistillationValidationError):
            validate_display_lettering_source_pipeline(broken)

    def test_exact_copy_and_approved_asset_identity_are_mandatory(self):
        pipeline = load("V3_DISPLAY_LETTERING_SOURCE_PIPELINE_CONTRACT.json")
        for required in ("exact_copy", "correctness_verification", "human_review", "approved_asset_identity"):
            self.assertIn(required, pipeline["required_common_record"])

    def test_shanyeji_requires_direct_canonical_pixels(self):
        self.assertIs(validate_typography_evidence(self.syj_evidence), self.syj_evidence)
        broken = copy.deepcopy(self.syj_evidence)
        broken["subject"]["pixel_binding"] = "CHAT_SUMMARY_ONLY"
        with self.assertRaises(DistillationValidationError):
            validate_typography_evidence(broken)
        self.assertEqual(self.syj_evidence["subject"]["canonical_sha256"], "9a29fbdc7dd908017924bed270e8dfe18351519eed3fa7bc7001789f2a383414")

    def test_shanyeji_is_typography_only_pending_and_not_component_approved(self):
        self.assertIs(validate_typography_hypothesis(self.syj_hypothesis), self.syj_hypothesis)
        self.assertEqual(self.syj_hypothesis["distillation_scope"], "TYPOGRAPHY_ONLY_FAMILY_CANDIDATE")
        self.assertEqual(self.syj_hypothesis["review_status"], "HUMAN_REVIEW_PENDING")
        self.assertEqual(self.syj_hypothesis["component_approval_status"], "UNCONFIRMED")
        self.assertEqual(self.syj_hypothesis["promotion_status"], "UNPROMOTED")

    def test_component_scoped_evidence_separates_request_from_approval(self):
        contract = load("V3_TYPOGRAPHY_COMPONENT_SCOPED_EVIDENCE_CONTRACT.json")
        self.assertIs(validate_typography_component_evidence_contract(contract), contract)
        self.assertFalse(contract["separation_rules"]["whole_image_approval_populates_component_approval"])
        self.assertFalse(contract["separation_rules"]["distillation_request_implies_approval"])

    def test_shanyeji_figma_map_keeps_display_title_unresolved(self):
        figma = load("V3_TYPOGRAPHY_FIGMA_PRODUCIBILITY_SHANYEJI.json")
        self.assertIs(validate_shanyeji_figma_producibility_map(figma), figma)
        self.assertEqual(figma["central_title_claim"], "NOT_AUTOMATICALLY_REPRODUCIBLE_IN_FIGMA")

    def test_all_typography_mechanisms_remain_unconfirmed_and_unpromoted(self):
        typography = [row for row in self.library["mechanisms"] if row["domain"] == "typography_lettering"]
        for row in typography:
            self.assertIs(validate_mechanism(row), row)
            self.assertEqual(row["component_approval_status"], "UNCONFIRMED")
            self.assertEqual(row["promotion_status"], "UNPROMOTED")

    def test_transfer_plans_are_planning_only(self):
        plans = load("V3_TYPOGRAPHY_TRANSFER_PLANS_POST_REVIEW.json")
        self.assertEqual(len(plans["plans"]), 3)
        self.assertEqual({row["execution_status"] for row in plans["plans"]}, {"PLANNED_NOT_EXECUTED"})
        self.assertFalse(plans["typography_transfer_executed"])

    def test_ingestion_receipt_preserves_discovery_and_private_pixels(self):
        receipt = load("V3_TYPOGRAPHY_SHANYEJI_CANONICAL_INGESTION_RECEIPT.json")
        self.assertEqual(receipt["private_substrate"]["dataset_role"], "unassigned")
        self.assertEqual(receipt["discovery"]["approved_before"], receipt["discovery"]["approved_after"])
        self.assertEqual(receipt["discovery"]["rejected_before"], receipt["discovery"]["rejected_after"])
        self.assertFalse(receipt["discovery"]["modified"])
        self.assertFalse(receipt["private_pixels_committed_to_git"])

    def test_raw_private_pixels_are_not_git_tracked(self):
        tracked = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True, encoding="utf-8")
        self.assertNotIn("1-Photo-1.jpg", tracked)
        self.assertNotIn("9a29fbdc7dd908017924bed270e8dfe18351519eed3fa7bc7001789f2a383414.jpg", tracked)

    def test_figma_contract_runtime_separation_is_preserved(self):
        for suffix in ("05", "13"):
            contract = load(f"V3_FIGMA_PRODUCTION_CONTRACT_REFERENCE_{suffix}.json")
            self.assertEqual(contract["contract_status"], "FIGMA_CONTRACT_READY")
            self.assertEqual(contract["runtime_status"], "FIGMA_RUNTIME_VERIFIED")
            self.assertTrue(contract["runtime_receipt"])
        figma = load("V3_TYPOGRAPHY_FIGMA_PRODUCIBILITY_SHANYEJI.json")
        self.assertNotEqual(figma["status"], "FIGMA_PRODUCTION_CONTRACT_READY")


if __name__ == "__main__":
    unittest.main()
