from __future__ import annotations

import json
import unittest
from pathlib import Path

from visual_memory.distillation_v3 import validate_mechanism, validate_transfer_plan, validate_visual_program


REPO_ROOT = Path(__file__).resolve().parents[2]


def load_json(name: str):
    return json.loads((REPO_ROOT / name).read_text(encoding="utf-8"))


class PostHumanReviewV3Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p05 = load_json("V3_VISUAL_PROGRAM_REFERENCE_05_PROVISIONAL.json")
        cls.p13 = load_json("V3_VISUAL_PROGRAM_REFERENCE_13_PROVISIONAL.json")
        cls.mechanisms = {row["mechanism_id"]: row for row in load_json("V3_VISUAL_MECHANISM_LIBRARY.json")["mechanisms"]}
        cls.families = {row["family_id"]: row for row in load_json("V3_VISUAL_FAMILY_REGISTRY.json")["families"]}
        cls.plans05 = load_json("V3_TRANSFER_PLANS_REFERENCE_05.json")["plans"]
        cls.plans13 = load_json("V3_TRANSFER_PLANS_REFERENCE_13.json")["plans"]

    def test_provisional_programs_validate_and_remain_transfer_pending(self):
        for program in (self.p05, self.p13):
            validate_visual_program(program)
            self.assertEqual(program["status"], "PROVISIONAL_VISUAL_PROGRAM")
            self.assertEqual(program["validation_status"], "TRANSFER_VALIDATION_PENDING")
            self.assertEqual(program["golden_exemplars"], [])
            self.assertEqual(program["anchor_dependence"], "HIGH_REFERENCE_CONDITIONED")
            self.assertTrue(all(row["state"] == "INVARIANT_HYPOTHESIS" for row in program["stable_grammar"]))
            self.assertEqual(program["promotion_history"], [])

    def test_reference_05_human_revisions_are_applied(self):
        ids = {row["mechanism_id"] for row in self.p05["stable_grammar"]}
        self.assertEqual(len(ids), 7)
        for expected in (
            "mech_05_process_scene_hierarchy",
            "mech_05_multi_tier_information",
            "mech_05_campaign_module_logic",
            "mech_05_semantic_graphic_derivation",
            "mech_05_dining_world_context",
            "mech_05_low_key_heat_tonal_orchestration",
            "mech_05_display_lettering_structural_mass",
        ):
            self.assertIn(expected, ids)
        philosophy = self.p05["visual_philosophy"]
        self.assertIn("live process and heat", philosophy)
        self.assertIn("product proof", philosophy)
        self.assertIn("contextual world-building", philosophy)
        self.assertIn("display lettering", philosophy)
        compatibility = json.dumps(self.p05["content_compatibility"], ensure_ascii=False)
        self.assertIn("Equivalent brand-relevant roles", compatibility)
        self.assertIn("single isolated product", compatibility)
        production_bound = json.dumps(self.p05["production_bound_features"])
        self.assertIn("exact three-band", production_bound)

    def test_reference_13_human_revisions_are_applied(self):
        ids = {row["mechanism_id"] for row in self.p13["stable_grammar"]}
        self.assertEqual(len(ids), 7)
        for expected in (
            "mech_13_asymmetric_title_field",
            "mech_13_active_whitespace",
            "mech_13_vessel_ingredient_anchor",
            "mech_13_editorial_information_rhythm",
            "mech_13_shared_optical_geometry",
            "mech_13_organic_display_lettering_behavior",
            "mech_13_matte_mineral_soft_light_materiality",
        ):
            self.assertIn(expected, ids)
        philosophy = self.p13["visual_philosophy"]
        self.assertIn("expressive handmade title geometry", philosophy)
        self.assertIn("object/raw-material still life", philosophy)
        self.assertIn("muted tonal relationships", philosophy)
        compatibility = json.dumps(self.p13["content_compatibility"], ensure_ascii=False)
        self.assertIn("literal vessel is not required", compatibility)
        self.assertIn("high-risk", compatibility)
        production_bound = json.dumps(self.p13["production_bound_features"])
        self.assertIn("exact paper texture/grain", production_bound)

    def test_old_family_ids_resolve_as_alias_history(self):
        family05 = self.families["family_reference_05_process_campaign_brand_world"]
        family13 = self.families["family_reference_13_editorial_titlefield_stilllife"]
        self.assertIn("family_reference_05_black_red_brand_world", family05["family_aliases"])
        self.assertIn("family_reference_13_warm_editorial_still_life", family13["family_aliases"])
        self.assertEqual(family05["family_id_history"][0]["superseded_by"], family05["family_id"])
        self.assertEqual(family13["family_id_history"][0]["superseded_by"], family13["family_id"])
        self.assertTrue(family05["merge_prohibited_without_human_approval"])
        self.assertTrue(family13["merge_prohibited_without_human_approval"])

    def test_reclassified_mechanisms_separate_principle_from_exact_assets(self):
        semantic_graphic = self.mechanisms["mech_05_semantic_graphic_derivation"]
        still_life = self.mechanisms["mech_13_vessel_ingredient_anchor"]
        self.assertEqual(semantic_graphic["status"], "FAMILY_LOCAL")
        self.assertEqual(still_life["status"], "FAMILY_LOCAL")
        brand_bound_05 = json.dumps(self.p05["brand_bound_features"])
        content_bound_13 = json.dumps(self.p13["content_bound_features"])
        self.assertIn("exact pepper/stove drawings", brand_bound_05)
        self.assertIn("exact vessel and lid", content_bound_13)

    def test_new_mechanisms_remain_unpromoted_and_unconfirmed(self):
        new_ids = {
            "mech_05_low_key_heat_tonal_orchestration",
            "mech_05_display_lettering_structural_mass",
            "mech_13_organic_display_lettering_behavior",
            "mech_13_matte_mineral_soft_light_materiality",
        }
        self.assertTrue(new_ids.issubset(self.mechanisms))
        for mechanism in self.mechanisms.values():
            validate_mechanism(mechanism)
            self.assertEqual(mechanism["component_approval_status"], "UNCONFIRMED")
            self.assertEqual(mechanism["promotion_status"], "UNPROMOTED")
            self.assertEqual({row["kind"] for row in mechanism["support_basis"]}, {"WHOLE_IMAGE_APPROVAL"})

    def test_each_program_has_exactly_three_unexecuted_transfer_plans(self):
        expected = {"RECONSTRUCT", "CONTENT_SWAP", "COMPOSITION_OR_ASPECT_TRANSFER"}
        for program, plans in ((self.p05, self.plans05), (self.p13, self.plans13)):
            self.assertEqual(len(plans), 3)
            self.assertEqual({row["operator"] for row in plans}, expected)
            self.assertEqual({row["program_id"] for row in plans}, {program["program_id"]})
            for plan in plans:
                validate_transfer_plan(plan)
                self.assertEqual(plan["execution_status"], "PLANNED_NOT_EXECUTED")
                self.assertEqual(plan["output_artifacts"], [])
                self.assertFalse(plan["absolute_quality_floor"]["relative_gain_is_sufficient"])
                self.assertTrue(plan["absolute_quality_floor"]["human_pixel_review_required"])

    def test_no_transfer_validation_or_durable_promotion_was_created(self):
        for program in (self.p05, self.p13):
            transfer = [row for row in program["validation_evidence"] if row["kind"] == "TRANSFER_VALIDATION"]
            self.assertEqual(transfer, [{"kind": "TRANSFER_VALIDATION", "status": "PENDING", "outputs": []}])
            self.assertEqual(program["promotion_history"], [])
        self.assertFalse(any(plan["output_artifacts"] for plan in self.plans05 + self.plans13))


if __name__ == "__main__":
    unittest.main()
