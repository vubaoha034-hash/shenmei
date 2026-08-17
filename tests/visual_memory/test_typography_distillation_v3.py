import copy
import json
import unittest
from pathlib import Path

from visual_memory.distillation_v3 import (
    DistillationValidationError,
    TYPOGRAPHY_ROLES,
    build_typography_runtime_package,
    classify_liked_work,
    validate_figma_dry_run_receipt,
    validate_figma_production_contract,
    validate_mechanism,
    validate_typography_evidence,
    validate_typography_hypothesis,
    validate_visual_program,
)


ROOT = Path(__file__).resolve().parents[2]


def load(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


class TypographyDistillationV3Tests(unittest.TestCase):
    def setUp(self):
        self.evidence05 = load("V3_TYPOGRAPHY_EVIDENCE_REFERENCE_05.json")
        self.evidence13 = load("V3_TYPOGRAPHY_EVIDENCE_REFERENCE_13.json")
        self.hypothesis05 = load("V3_TYPOGRAPHY_HYPOTHESIS_REFERENCE_05.json")
        self.hypothesis13 = load("V3_TYPOGRAPHY_HYPOTHESIS_REFERENCE_13.json")
        self.contract05 = load("V3_FIGMA_PRODUCTION_CONTRACT_REFERENCE_05.json")
        self.contract13 = load("V3_FIGMA_PRODUCTION_CONTRACT_REFERENCE_13.json")
        self.program05 = load("V3_VISUAL_PROGRAM_REFERENCE_05_PROVISIONAL.json")
        self.program13 = load("V3_VISUAL_PROGRAM_REFERENCE_13_PROVISIONAL.json")

    def test_typography_evidence_schema_and_instances_validate(self):
        schema = load("schemas/typography-distillation-evidence.v3.schema.json")
        self.assertEqual(schema["properties"]["schema_version"]["const"], "3.0.0")
        self.assertIn("text_role_inventory", schema["required"])
        for evidence in (self.evidence05, self.evidence13):
            self.assertIs(validate_typography_evidence(evidence), evidence)
            self.assertEqual({row["role"] for row in evidence["text_role_inventory"]}, TYPOGRAPHY_ROLES)

    def test_typography_hypothesis_schema_and_instances_validate(self):
        schema = load("schemas/typography-distillation-hypothesis.v3.schema.json")
        self.assertIn("typography_visual_philosophy", schema["required"])
        for hypothesis in (self.hypothesis05, self.hypothesis13):
            self.assertIs(validate_typography_hypothesis(hypothesis), hypothesis)
            self.assertEqual(hypothesis["status"], "PROVISIONAL_PROGRAM_COMPONENT")
            self.assertEqual(hypothesis["review_status"], "HUMAN_REVIEWED")

    def test_figma_contract_schema_and_instances_validate(self):
        schema = load("schemas/figma-production-contract.v3.schema.json")
        self.assertIn("fail_closed_conditions", schema["required"])
        for contract in (self.contract05, self.contract13):
            self.assertIs(validate_figma_production_contract(contract), contract)
            self.assertEqual(contract["contract_status"], "FIGMA_CONTRACT_READY")

    def test_reference_families_and_typography_programs_remain_separate(self):
        self.assertNotEqual(self.program05["family_id"], self.program13["family_id"])
        self.assertNotEqual(self.hypothesis05["hypothesis_id"], self.hypothesis13["hypothesis_id"])
        self.assertNotEqual(self.contract05["contract_id"], self.contract13["contract_id"])
        self.assertNotEqual(
            set(self.program05["typography_program"]["mechanism_ids"]),
            set(self.program13["typography_program"]["mechanism_ids"]),
        )

    def test_whole_image_like_does_not_approve_typography_component(self):
        classified = classify_liked_work(
            sample_id="sample_one",
            primary_action="REINFORCE_EXISTING_FAMILY",
            whole_image_evidence_ids=["whole_like"],
            component_evidence=[],
        )
        self.assertFalse(classified["whole_image_like_implies_component_like"])
        library = load("V3_VISUAL_MECHANISM_LIBRARY.json")
        typography = [row for row in library["mechanisms"] if row["domain"] == "typography_lettering"]
        self.assertTrue(typography)
        self.assertEqual({row["component_approval_status"] for row in typography}, {"UNCONFIRMED"})
        self.assertEqual({row["promotion_status"] for row in typography}, {"UNPROMOTED"})
        for row in typography:
            validate_mechanism(row)

    def test_copy_fidelity_and_live_text_vector_policies_are_complete(self):
        for contract in (self.contract05, self.contract13):
            verbatim = set(contract["copy_fidelity_rules"]["VERBATIM_REQUIRED"])
            self.assertTrue({"brand name", "dish name", "price", "date", "address"}.issubset(verbatim))
            policies = {row["policy"] for row in contract["live_text_vs_vector_policy"]}
            self.assertIn("LIVE_TEXT_REQUIRED", policies)
            self.assertIn("APPROVED_DISPLAY_ASSET", policies)
            self.assertIn("NOT_FIGMA_ZERO_TO_ONE", policies)

    def test_figma_contract_fails_closed_on_unresolved_font_or_asset(self):
        for contract in (self.contract05, self.contract13):
            self.assertIn("FONT_SELECTION_HUMAN_PENDING", contract["unresolved_dependencies"])
            self.assertIn("APPROVED_DISPLAY_LETTERING_ASSET", contract["unresolved_dependencies"])
            self.assertIn("required font or lettering asset not bound", contract["fail_closed_conditions"])

    def test_runtime_package_is_bounded_and_excludes_deep_evidence(self):
        package = build_typography_runtime_package(
            self.program05,
            self.hypothesis05,
            self.contract05,
            exact_copy={"display_title": "LOCKED COPY"},
            approved_typography_mechanisms=[],
            purpose="HUMAN_REVIEW",
        )
        self.assertFalse(package["deep_evidence_embedded"])
        self.assertLessEqual(len(package["family_typography_program"]["stable_grammar"]), 6)
        self.assertLessEqual(len(package["family_typography_program"]["variation_axes"]), 4)
        self.assertLessEqual(len(package["figma_production_contract"]["live_text_vs_vector_policy"]), 12)
        self.assertNotIn("evidence_sections", json.dumps(package))

    def test_visual_program_typography_linkage_and_backward_compatibility(self):
        for program in (self.program05, self.program13):
            self.assertIs(validate_visual_program(program), program)
            self.assertIn("typography_program", program)
            self.assertEqual(program["typography_program"]["component_approval_status"], "UNCONFIRMED")
        old_shape = copy.deepcopy(self.program05)
        del old_shape["typography_program"]
        self.assertIs(validate_visual_program(old_shape), old_shape)

    def test_promotion_and_production_blocked_without_human_approval(self):
        with self.assertRaises(DistillationValidationError):
            build_typography_runtime_package(
                self.program05,
                self.hypothesis05,
                self.contract05,
                exact_copy={},
                approved_typography_mechanisms=[],
                purpose="PRODUCTION",
            )

    def test_runtime_builder_does_not_mutate_program_or_raw_substrate(self):
        before = copy.deepcopy((self.program05, self.hypothesis05, self.contract05))
        build_typography_runtime_package(
            self.program05,
            self.hypothesis05,
            self.contract05,
            exact_copy={},
            approved_typography_mechanisms=[],
            purpose="HUMAN_REVIEW",
        )
        self.assertEqual((self.program05, self.hypothesis05, self.contract05), before)
        module = (ROOT / "visual_memory/distillation_v3.py").read_text(encoding="utf-8")
        self.assertNotIn("VisualMemoryStore(", module)
        self.assertNotIn("record_feedback(", module)
        self.assertNotIn("ingest_visual_file(", module)

    def test_historical_human_review_package_preserves_then_valid_blocker(self):
        review = load("V3_TYPOGRAPHY_DISTILLATION_HUMAN_REVIEW_PACKAGE.json")
        self.assertFalse(review["whole_image_approval_implies_component_approval"])
        self.assertEqual(
            review["shan_ye_ji_candidate"]["status"],
            "TYPOGRAPHY_REFERENCE_SOURCE_NOT_CANONICALIZED",
        )
        self.assertFalse(review["shan_ye_ji_candidate"]["evidence_or_hypothesis_created"])

    def test_figma_dry_run_receipt_validates_when_executed(self):
        receipt_path = ROOT / "V3_FIGMA_TECHNICAL_DRY_RUN_RECEIPT.json"
        if not receipt_path.exists():
            self.skipTest("Figma technical dry run has not executed in this context")
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        self.assertIs(validate_figma_dry_run_receipt(receipt), receipt)


if __name__ == "__main__":
    unittest.main()
