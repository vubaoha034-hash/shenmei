from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from visual_memory.pilot import ingest_visual_file, record_batch_feedback
from visual_memory.replication import (
    build_replication_snapshot,
    canonical_sha256,
    exact_binomial_one_sided_p,
    summarize_replication,
    verify_replication_snapshot,
)
from visual_memory.store import VisualMemoryStore


class Phase10ReplicationTests(unittest.TestCase):
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

    def _seed_restaurant_context(self) -> None:
        approved, _ = ingest_visual_file(
            self.store, self._source("approved.jpg", b"approved")
        )
        rejected, _ = ingest_visual_file(
            self.store, self._source("rejected.jpg", b"rejected")
        )
        record_batch_feedback(
            self.store,
            [approved["sample_id"]],
            verdict="approved",
            user_text="这张餐饮参考我明确喜欢。",
            scope_level="domain",
            domain="餐饮",
        )
        record_batch_feedback(
            self.store,
            [rejected["sample_id"]],
            verdict="rejected",
            user_text="这张餐饮参考我明确不喜欢。",
            scope_level="domain",
            domain="餐饮",
        )

    def test_canonical_hash_is_order_independent_for_object_keys(self):
        a = {"b": 2, "a": 1}
        b = {"a": 1, "b": 2}
        self.assertEqual(canonical_sha256(a), canonical_sha256(b))

    def test_snapshot_verifies_when_state_is_unchanged(self):
        self._seed_restaurant_context()
        snapshot = build_replication_snapshot(self.store, domain="餐饮")
        self.assertTrue(verify_replication_snapshot(self.store, snapshot))

    def test_snapshot_detects_new_discovery_evidence(self):
        self._seed_restaurant_context()
        snapshot = build_replication_snapshot(self.store, domain="餐饮")
        sample, _ = ingest_visual_file(
            self.store, self._source("later.jpg", b"later")
        )
        record_batch_feedback(
            self.store,
            [sample["sample_id"]],
            verdict="approved",
            user_text="后来新增的一张。",
            scope_level="domain",
            domain="餐饮",
        )
        self.assertFalse(verify_replication_snapshot(self.store, snapshot))

    def test_exact_binomial_known_combined_boundary(self):
        # PHASE 9 6:4 + PHASE 10 14:6 => 20 personalized wins out of 30 non-ties.
        p = exact_binomial_one_sided_p(20, 30)
        self.assertAlmostEqual(p, 0.04936857335269451, places=12)

    def test_replication_pass_requires_stronger_combined_evidence(self):
        results = ([{"result": "personalized"}] * 14) + ([{"result": "baseline"}] * 6)
        summary = summarize_replication(results)
        self.assertEqual(summary["decision"], "REPLICATION_PASS")
        self.assertLessEqual(
            summary["combined_phase9_phase10"]["one_sided_exact_binomial_p"],
            0.05,
        )

    def test_twelve_eight_replication_is_still_inconclusive(self):
        results = ([{"result": "personalized"}] * 12) + ([{"result": "baseline"}] * 8)
        summary = summarize_replication(results)
        self.assertEqual(summary["decision"], "INCONCLUSIVE")
        self.assertGreater(
            summary["combined_phase9_phase10"]["one_sided_exact_binomial_p"],
            0.05,
        )

    def test_equal_phase10_direction_is_not_replicated(self):
        results = ([{"result": "personalized"}] * 10) + ([{"result": "baseline"}] * 10)
        self.assertEqual(
            summarize_replication(results)["decision"],
            "NOT_REPLICATED",
        )

    def test_less_than_twenty_pairs_is_inconclusive(self):
        results = ([{"result": "personalized"}] * 13) + ([{"result": "baseline"}] * 6)
        self.assertEqual(
            summarize_replication(results)["decision"],
            "INCONCLUSIVE",
        )

    def test_safety_failure_invalidates_result(self):
        results = ([{"result": "personalized"}] * 20)
        self.assertEqual(
            summarize_replication(results, safety_ok=False)["decision"],
            "INVALID",
        )

    def test_frozen_state_change_invalidates_result(self):
        results = ([{"result": "personalized"}] * 20)
        self.assertEqual(
            summarize_replication(results, frozen_state_unchanged=False)["decision"],
            "INVALID",
        )


if __name__ == "__main__":
    unittest.main()
