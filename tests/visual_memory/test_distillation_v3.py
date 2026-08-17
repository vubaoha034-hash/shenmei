from __future__ import annotations

import json
import unittest
from pathlib import Path

from visual_memory.distillation_v3 import (
    DistillationValidationError,
    build_promotion_package,
    build_runtime_package,
    build_validation_receipt,
    classify_liked_work,
    rank_candidate_evidence,
    validate_deep_evidence,
    validate_distillation_hypothesis,
    validate_mechanism,
    validate_semantic_identity,
    validate_transfer_plan,
    validate_visual_program,
)


REPO_ROOT = Path(__file__).resolve().parents[2]


def load_json(relative: str):
    return json.loads((REPO_ROOT / relative).read_text(encoding="utf-8"))


def sample_program(*, status: str = "PROVISIONAL_VISUAL_PROGRAM"):
    return {
        "program_id": "program_test",
        "family_id": "family_test",
        "status": status,
        "visual_philosophy": "A reviewed concise philosophy.",
        "mother_reference": None,
        "golden_exemplars": [{"asset_id": "ast_one"}, {"asset_id": "ast_two"}],
        "stable_grammar": [
            {"mechanism_id": f"m{index}", "statement": f"mechanism {index}", "state": "INVARIANT_HYPOTHESIS", "evidence_ids": [f"e{index}"]}
            for index in range(4)
        ],
        "variation_axes": [],
        "content_compatibility": [],
        "content_bound_features": [],
        "brand_bound_features": [],
        "typography_role": {},
        "color_light_material_signature": {},
        "integration_rules": [],
        "generic_shortcut_blockers": ["generic shortcut one", "generic shortcut two"],
        "freedoms": ["macro layout"],
        "transfer_operators": ["RECONSTRUCT", "CONTENT_SWAP", "COMPOSITION_OR_ASPECT_TRANSFER"],
        "validation_evidence": [],
        "renderer_provenance_requirements": {
            "renderer": "required",
            "model": "required",
            "model_version": "required-or-explicitly-unavailable",
            "parameters": "required",
            "actual_attachments": "required",
            "final_invocation_evidence": "required",
        },
        "anchor_dependence": "UNKNOWN",
        "promotion_history": [],
        "evidence_lineage": ["ev_one"],
    }


class DistillationV3Tests(unittest.TestCase):
    def test_public_schemas_are_parseable_draft_2020_documents(self):
        paths = [
            "schemas/distillation-evidence.v3.schema.json",
            "schemas/distillation-hypothesis.v3.schema.json",
            "schemas/visual-program.v3.schema.json",
            "schemas/visual-mechanism.v3.schema.json",
            "schemas/semantic-identity.v3.schema.json",
        ]
        for path in paths:
            schema = load_json(path)
            self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
            self.assertEqual(schema["type"], "object")
            self.assertIn("required", schema)
            self.assertIsInstance(schema["properties"], dict)

    def test_initial_deep_evidence_and_hypotheses_validate(self):
        for ref in ("05", "13"):
            evidence = load_json(f"distillation/v3/reference-{ref}.deep-evidence.json")
            hypothesis = load_json(f"distillation/v3/reference-{ref}.distillation-hypothesis.json")
            self.assertIs(validate_deep_evidence(evidence), evidence)
            self.assertIs(validate_distillation_hypothesis(hypothesis), hypothesis)
            self.assertEqual(hypothesis["status"], "HUMAN_DISTILLATION_REVIEW_PENDING")
            self.assertTrue(all(row["state"] == "INVARIANT_HYPOTHESIS" for row in hypothesis["candidate_stable_grammar"]))

    def test_deterministic_ranking_only_deduplicates_and_bounds_evidence(self):
        evidence = load_json("distillation/v3/reference-05.deep-evidence.json")
        ranked = rank_candidate_evidence(evidence, limit=3)
        self.assertEqual(len(ranked), 3)
        self.assertTrue(all(row["evidence_class"] == "DIRECT_VISIBLE" for row in ranked))
        self.assertNotIn("aesthetic_pass", ranked[0])

    def test_substrate_is_reused_without_parallel_raw_store(self):
        reuse = (REPO_ROOT / "V3_SUBSTRATE_REUSE_MAP.md").read_text(encoding="utf-8")
        for capability in ("VisualMemoryStore", "Asset Vault", "WriterLease", "skill-refiner"):
            self.assertIn(capability, reuse)
        v3_module = (REPO_ROOT / "visual_memory/distillation_v3.py").read_text(encoding="utf-8")
        self.assertNotIn("class VisualMemoryStore", v3_module)
        self.assertNotIn("events.jsonl", v3_module)

    def test_deep_evidence_cannot_be_dumped_into_visual_program_or_runtime(self):
        contaminated = sample_program()
        contaminated["deep_evidence"] = load_json("distillation/v3/reference-05.deep-evidence.json")
        with self.assertRaises(DistillationValidationError):
            validate_visual_program(contaminated)

        package = build_runtime_package(
            sample_program(),
            current_content_assets=[{"asset_id": "current"}],
            active_mechanisms=[{"mechanism_id": "m1"}],
            semantic_contract=None,
            copy_constraints=[],
            brand_constraints=[],
        )
        self.assertNotIn("deep_evidence", package)
        self.assertNotIn("analysis", package)

    def test_runtime_package_is_bounded(self):
        program = sample_program()
        program["golden_exemplars"].append({"asset_id": "ast_three"})
        package = build_runtime_package(
            program,
            current_content_assets=[{"asset_id": "current"}],
            active_mechanisms=[{"mechanism_id": f"m{index}"} for index in range(8)],
            semantic_contract=None,
            copy_constraints=[],
            brand_constraints=[],
        )
        self.assertEqual(len(package["golden_exemplars"]), 2)
        self.assertLessEqual(len(package["generic_shortcut_blockers"]), 3)
        with self.assertRaises(DistillationValidationError):
            build_runtime_package(
                sample_program(),
                current_content_assets=[],
                active_mechanisms=[{"mechanism_id": f"m{index}"} for index in range(9)],
                semantic_contract=None,
                copy_constraints=[],
                brand_constraints=[],
            )

    def test_hypothesis_cannot_enter_runtime_before_human_review(self):
        with self.assertRaises(DistillationValidationError):
            build_runtime_package(
                sample_program(status="DEPRECATED"),
                current_content_assets=[],
                active_mechanisms=[],
                semantic_contract=None,
                copy_constraints=[],
                brand_constraints=[],
            )

    def test_grammar_default_count_is_not_aesthetic_validator(self):
        program = sample_program()
        program["stable_grammar"] = program["stable_grammar"][:2]
        program["grammar_count_exception"] = "Human review found two mechanisms sufficient for this narrow family."
        self.assertIs(validate_visual_program(program), program)

    def test_whole_image_approval_does_not_promote_components(self):
        library = load_json("V3_VISUAL_MECHANISM_LIBRARY.json")
        for mechanism in library["mechanisms"]:
            validate_mechanism(mechanism)
            self.assertEqual(mechanism["component_approval_status"], "UNCONFIRMED")
            self.assertEqual(mechanism["promotion_status"], "UNPROMOTED")

        invalid = dict(library["mechanisms"][0])
        invalid["component_approval_status"] = "SUPPORTED"
        with self.assertRaises(DistillationValidationError):
            validate_mechanism(invalid)

        with self.assertRaises(DistillationValidationError):
            classify_liked_work(
                sample_id="smp_one",
                primary_action="REINFORCE_EXISTING_FAMILY",
                whole_image_evidence_ids=["ev_one"],
                component_evidence=[{"support_kind": "WHOLE_IMAGE_APPROVAL"}],
            )

    def test_reference_families_remain_separate_and_unmerged(self):
        registry = load_json("V3_VISUAL_FAMILY_REGISTRY.json")
        families = registry["families"]
        self.assertEqual(len(families), 2)
        self.assertNotEqual(families[0]["family_id"], families[1]["family_id"])
        self.assertTrue(all(row["merge_prohibited_without_human_approval"] for row in families))
        self.assertTrue(all(row["program_version"] is None for row in families))

    def test_anchor_dependence_is_explicit(self):
        for ref in ("05", "13"):
            hypothesis = load_json(f"distillation/v3/reference-{ref}.distillation-hypothesis.json")
            self.assertEqual(hypothesis["expected_anchor_dependence"], "HIGH_REFERENCE_CONDITIONED")

    def test_generic_semantic_core_and_restaurant_adapter(self):
        registry = load_json("V3_SEMANTIC_IDENTITY_REGISTRY.json")
        self.assertTrue(registry["core_domain_neutral"])
        record = registry["records"][0]
        validate_semantic_identity(record)
        self.assertEqual(record["canonical_name"], "柠檬叶怪味里脊")
        self.assertEqual(record["primary_entity"], "猪里脊肉")
        self.assertEqual(record["hero_suitability"], "FAIL_FOR_HERO_SOURCE")
        self.assertEqual(record["adapter"]["adapter_type"], "restaurant_semantic_adapter_v1")

    def test_transfer_plan_requires_preconditions_and_renderer_provenance(self):
        plan = {
            "transfer_id": "transfer_one",
            "operator": "CONTENT_SWAP",
            "program_id": "program_one",
            "preconditions": ["human-reviewed program"],
            "stable_grammar_to_preserve": ["m1"],
            "allowed_variation": ["content"],
            "semantic_identity_requirements": {"required": True},
            "content_compatibility": {"status": "PASS"},
            "reference_attachments": [],
            "expected_anchor_dependence_test": {"expected": "MODERATE_REFERENCE_ASSISTED"},
            "failure_criteria": ["family collapse"],
            "renderer_provenance_requirements": {"renderer": True, "model": True, "model_version": True, "parameters": True, "actual_attachments": True},
        }
        self.assertIs(validate_transfer_plan(plan), plan)
        bad = dict(plan)
        bad["preconditions"] = []
        with self.assertRaises(DistillationValidationError):
            validate_transfer_plan(bad)
        bad = dict(plan)
        bad["renderer_provenance_requirements"] = {"renderer": True}
        with self.assertRaises(DistillationValidationError):
            validate_transfer_plan(bad)

    def test_validation_keeps_technical_and_aesthetic_axes_separate(self):
        receipt = build_validation_receipt(
            artifact_id="artifact_one",
            technical_checks={"integrity": "PASS"},
            human_pixel_review={"absolute_usable": False},
            relative_gain=True,
        )
        self.assertEqual(receipt["decision"], "RELATIVE_GAIN / ABSOLUTE_FAIL")
        self.assertFalse(receipt["codex_aesthetic_authority"])

    def test_promotion_requires_transfer_human_user_and_provenance_gates(self):
        common = dict(
            target="visual-skill",
            evidence_ids=["ev_one"],
            transfer_evidence=[{"transfer_id": "t1"}],
            human_pixel_reviews=[{"passed": True}],
            explicit_user_approval=True,
            provenance_complete=True,
            unresolved_contradictions=[],
        )
        package = build_promotion_package(**common)
        self.assertEqual(package["promotion_authority"], "skill-refiner")
        self.assertFalse(package["durable_promotion_executed"])

        for field, value in (
            ("transfer_evidence", []),
            ("human_pixel_reviews", []),
            ("explicit_user_approval", False),
            ("provenance_complete", False),
            ("unresolved_contradictions", [{"issue": "open"}]),
        ):
            blocked = dict(common)
            blocked[field] = value
            with self.assertRaises(DistillationValidationError):
                build_promotion_package(**blocked)


if __name__ == "__main__":
    unittest.main()
