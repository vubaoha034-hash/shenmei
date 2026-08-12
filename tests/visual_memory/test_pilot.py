from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from visual_memory.pilot import (
    blind_pair_result,
    build_context_pack,
    ingest_visual_file,
    record_batch_feedback,
    summarize_blind_results,
)
from visual_memory.store import VisualMemoryStore


class Phase9PilotTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "private"
        self.store = VisualMemoryStore(self.root)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _source(self, name: str, content: bytes) -> Path:
        path = Path(self.tmp.name) / name
        path.write_bytes(content)
        return path

    def test_ingest_does_not_create_preference_evidence(self):
        sample, asset = ingest_visual_file(self.store, self._source("a.jpg", b"a"))
        self.assertEqual(self.store.read_evidence(), [])
        self.assertEqual(sample["dataset_role"], "discovery")
        self.assertIsNotNone(self.store.resolve_asset(asset["asset_id"]))

    def test_exact_duplicate_ingest_is_rejected(self):
        ingest_visual_file(self.store, self._source("a.jpg", b"same-bytes"))
        with self.assertRaises(ValueError):
            ingest_visual_file(self.store, self._source("b.jpg", b"same-bytes"))
        self.assertEqual(len(self.store.read_samples()), 1)
        self.assertEqual(len(self.store.read_assets()), 1)

    def test_ingest_rolls_back_if_asset_metadata_write_fails(self):
        source = self._source("a.jpg", b"rollback")
        with patch.object(self.store, "write_asset", side_effect=RuntimeError("synthetic failure")):
            with self.assertRaises(RuntimeError):
                ingest_visual_file(self.store, source)
        self.assertEqual(self.store.read_samples(), [])
        self.assertEqual(self.store.read_assets(), [])
        self.assertEqual(list(self.store.vault_dir.iterdir()), [])

    def test_batch_feedback_requires_explicit_text(self):
        sample, _ = ingest_visual_file(self.store, self._source("a.jpg", b"a"))
        with self.assertRaises(ValueError):
            record_batch_feedback(
                self.store,
                [sample["sample_id"]],
                verdict="approved",
                user_text="",
                scope_level="domain",
                domain="poster",
            )

    def test_blind_reserved_sample_cannot_enter_discovery_feedback(self):
        sample, _ = ingest_visual_file(
            self.store,
            self._source("blind.jpg", b"blind"),
            dataset_role="blind_eval_reserved",
        )
        with self.assertRaises(ValueError):
            record_batch_feedback(
                self.store,
                [sample["sample_id"]],
                verdict="approved",
                user_text="这张喜欢。",
                scope_level="domain",
                domain="poster",
            )

    def test_context_pack_uses_only_matching_domain_and_global_explicit(self):
        food, _ = ingest_visual_file(self.store, self._source("food.jpg", b"food"))
        sci, _ = ingest_visual_file(self.store, self._source("sci.jpg", b"sci"))
        unspecified, _ = ingest_visual_file(self.store, self._source("u.jpg", b"u"))
        global_sample, _ = ingest_visual_file(self.store, self._source("g.jpg", b"g"))

        record_batch_feedback(
            self.store,
            [food["sample_id"]],
            verdict="approved",
            user_text="这张作为 food 域喜欢参考。",
            scope_level="domain",
            domain="food",
        )
        record_batch_feedback(
            self.store,
            [sci["sample_id"]],
            verdict="approved",
            user_text="这张作为 sci-fi 域喜欢参考。",
            scope_level="domain",
            domain="sci-fi",
        )
        record_batch_feedback(
            self.store,
            [unspecified["sample_id"]],
            verdict="approved",
            user_text="这张喜欢。",
            scope_level="unspecified",
        )
        record_batch_feedback(
            self.store,
            [global_sample["sample_id"]],
            verdict="rejected",
            user_text="这个问题所有视觉任务都不要。",
            scope_level="global_explicit",
        )

        pack = build_context_pack(self.store, domain="food", max_positive=5, max_negative=5)
        positive_ids = {x["sample_id"] for x in pack["positive_exemplars"]}
        negative_ids = {x["sample_id"] for x in pack["negative_exemplars"]}
        self.assertIn(food["sample_id"], positive_ids)
        self.assertNotIn(sci["sample_id"], positive_ids)
        self.assertNotIn(unspecified["sample_id"], positive_ids)
        self.assertIn(global_sample["sample_id"], negative_ids)

    def test_context_pack_skips_unresolvable_assets(self):
        sample, asset = ingest_visual_file(self.store, self._source("gone.jpg", b"gone"))
        record_batch_feedback(
            self.store,
            [sample["sample_id"]],
            verdict="approved",
            user_text="这张喜欢。",
            scope_level="domain",
            domain="poster",
        )
        resolved = self.store.resolve_asset(asset["asset_id"])
        self.assertIsNotNone(resolved)
        resolved.unlink()
        pack = build_context_pack(self.store, domain="poster")
        self.assertEqual(pack["positive_exemplars"], [])

    def test_context_pack_is_bounded(self):
        ids = []
        for index in range(8):
            sample, _ = ingest_visual_file(self.store, self._source(f"p{index}.jpg", bytes([index])))
            ids.append(sample["sample_id"])
        record_batch_feedback(
            self.store,
            ids,
            verdict="approved",
            user_text="这批都喜欢。",
            scope_level="domain",
            domain="poster",
        )
        pack = build_context_pack(self.store, domain="poster", max_positive=3, max_negative=1)
        self.assertEqual(len(pack["positive_exemplars"]), 3)

    def test_blind_pair_unblinding(self):
        self.assertEqual(blind_pair_result("p1", "baseline", "A")["result"], "baseline")
        self.assertEqual(blind_pair_result("p2", "baseline", "B")["result"], "personalized")
        self.assertEqual(blind_pair_result("p3", "personalized", "A")["result"], "personalized")
        self.assertEqual(blind_pair_result("p4", "personalized", "B")["result"], "baseline")
        self.assertEqual(blind_pair_result("p5", "baseline", "tie")["result"], "tie")

    def test_pilot_decision_rule(self):
        passing = ([{"result": "personalized"}] * 6) + ([{"result": "baseline"}] * 3) + [{"result": "tie"}]
        self.assertEqual(summarize_blind_results(passing)["decision"], "PASS_TO_EXPAND")

        even = ([{"result": "personalized"}] * 5) + ([{"result": "baseline"}] * 5)
        self.assertEqual(summarize_blind_results(even)["decision"], "FAIL_REWORK")

        too_small = ([{"result": "personalized"}] * 6) + ([{"result": "baseline"}] * 2)
        self.assertEqual(summarize_blind_results(too_small)["decision"], "INCONCLUSIVE")


if __name__ == "__main__":
    unittest.main()
