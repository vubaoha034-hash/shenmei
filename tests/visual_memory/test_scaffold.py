from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from visual_memory.backup import create_backup, restore_backup
from visual_memory.store import SCHEMA_VERSION, VisualMemoryStore, new_id, sha256_bytes, utc_now
from visual_memory.validation import RecordValidationError, validate_record


class VisualMemoryScaffoldTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "private-memory"
        self.store = VisualMemoryStore(self.root)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _sample_with_asset(self, *, role="discovery", kind="reference", data=b"synthetic-image", source_type="unknown"):
        sample_id = new_id("sample")
        asset_id = new_id("asset")
        vault_path = self.store.write_vault_bytes(asset_id, data, ".bin")
        asset = {
            "schema_version": SCHEMA_VERSION,
            "asset_id": asset_id,
            "sample_id": sample_id,
            "created_at": utc_now(),
            "sha256": sha256_bytes(data),
            "locator_kind": "local_file",
            "locator": str(vault_path.relative_to(self.root)),
            "asset_relation": "primary",
            "derived_from_asset_id": None,
            "media_type": "application/octet-stream",
        }
        sample = {
            "schema_version": SCHEMA_VERSION,
            "sample_id": sample_id,
            "created_at": utc_now(),
            "sample_kind": kind,
            "primary_asset_id": asset_id,
            "dataset_role": role,
            "provenance": {"source_type": source_type, "source_ref": None, "creator": None, "license": None},
            "user_tags": [],
        }
        self.store.write_sample(sample)
        self.store.write_asset(asset)
        return sample, asset

    def _event(self, *, event_type, raw_text, sample_ids=None, generation_ids=None, payload=None, scope="task"):
        event = {
            "schema_version": SCHEMA_VERSION,
            "event_id": new_id("event"),
            "occurred_at": utc_now(),
            "event_type": event_type,
            "source_kind": "user",
            "source_ref": None,
            "scope": {"level": scope, "domain": None},
            "raw_text": raw_text,
            "target_sample_ids": sample_ids or [],
            "target_generation_ids": generation_ids or [],
            "payload": payload or {},
        }
        self.store.append_evidence(event)
        return event

    def test_ids_hashes_and_asset_resolution(self):
        sample, asset = self._sample_with_asset(data=b"abc")
        self.assertTrue(sample["sample_id"].startswith("smp_"))
        self.assertTrue(asset["asset_id"].startswith("ast_"))
        self.assertEqual(asset["sha256"], sha256_bytes(b"abc"))
        resolved = self.store.resolve_asset(asset["asset_id"])
        self.assertIsNotNone(resolved)
        self.assertEqual(resolved.read_bytes(), b"abc")
        self.assertEqual(self.store.doctor(), [])

    def test_asset_locator_move_preserves_logical_identity(self):
        sample, asset = self._sample_with_asset(data=b"stable")
        old_path = self.store.resolve_asset(asset["asset_id"])
        new_dir = self.root / "vault-moved"
        new_dir.mkdir()
        new_path = new_dir / old_path.name
        old_path.rename(new_path)
        self.store.update_asset_locator(
            asset["asset_id"],
            locator_kind="local_file",
            locator=str(new_path.relative_to(self.root)),
        )
        updated = self.store.read_asset(asset["asset_id"])
        self.assertEqual(updated["asset_id"], asset["asset_id"])
        self.assertEqual(updated["sample_id"], sample["sample_id"])
        self.assertEqual(self.store.resolve_asset(asset["asset_id"]), new_path.resolve())

    def test_private_root_guard(self):
        repo = Path(self.tmp.name) / "public-repo"
        repo.mkdir()
        unsafe = VisualMemoryStore(repo / "private")
        with self.assertRaises(RuntimeError):
            unsafe.assert_outside_public_repo(repo)
        self.store.assert_outside_public_repo(repo)

    def test_raw_feedback_roundtrip_and_import_fidelity(self):
        sample, _ = self._sample_with_asset()
        text = "这个深黑不是我要的，这个看起来特别脏。"
        event = self._event(event_type="feedback", raw_text=text, sample_ids=[sample["sample_id"]], payload={"explicit_verdict": "rejected"})
        loaded = self.store.read_evidence()[0]
        self.assertEqual(loaded["raw_text"], text)
        self.assertEqual(loaded["event_id"], event["event_id"])

        bad_import = dict(event)
        bad_import["event_id"] = new_id("event")
        bad_import["source_kind"] = "imported_user_evidence"
        bad_import["source_ref"] = None
        with self.assertRaises(RecordValidationError):
            validate_record("evidence", bad_import)


    def test_raw_records_reject_inferred_extra_fields(self):
        sample, _ = self._sample_with_asset()
        contaminated = dict(sample)
        contaminated["aesthetic_score"] = 95
        with self.assertRaises(RecordValidationError):
            validate_record("sample", contaminated)

        event = {
            "schema_version": SCHEMA_VERSION,
            "event_id": new_id("event"),
            "occurred_at": utc_now(),
            "event_type": "feedback",
            "source_kind": "user",
            "source_ref": None,
            "scope": {"level": "task", "domain": None},
            "raw_text": "喜欢。",
            "target_sample_ids": [sample["sample_id"]],
            "target_generation_ids": [],
            "payload": {"explicit_verdict": "approved", "llm_summary": "user likes minimalism"},
        }
        with self.assertRaises(RecordValidationError):
            validate_record("evidence", event)

    def test_pairwise_revision_generation_lineage_and_correction(self):
        before, _ = self._sample_with_asset(kind="generated", role="production", data=b"before")
        after, _ = self._sample_with_asset(kind="generated", role="production", data=b"after")
        reference, _ = self._sample_with_asset(data=b"ref")

        gen1 = {
            "schema_version": SCHEMA_VERSION,
            "generation_id": new_id("generation"),
            "created_at": utc_now(),
            "renderer": "synthetic-renderer",
            "model": "synthetic-model",
            "model_version": "test",
            "task_ref": "synthetic-task",
            "reference_sample_ids": [reference["sample_id"]],
            "parent_generation_id": None,
            "output_sample_ids": [before["sample_id"]],
            "prompt_text": "synthetic only",
            "parameters": {},
        }
        self.store.write_generation(gen1)
        gen2 = dict(gen1)
        gen2["generation_id"] = new_id("generation")
        gen2["created_at"] = utc_now()
        gen2["parent_generation_id"] = gen1["generation_id"]
        gen2["output_sample_ids"] = [after["sample_id"]]
        self.store.write_generation(gen2)

        pair = self._event(
            event_type="comparison",
            raw_text="A更好，B太脏。",
            sample_ids=[reference["sample_id"], before["sample_id"]],
            payload={
                "left_sample_id": reference["sample_id"],
                "right_sample_id": before["sample_id"],
                "winner": "left",
                "comparison_kind": "natural",
            },
        )
        revision = self._event(
            event_type="revision",
            raw_text="把灰尘感去掉，保留黑色层次。",
            sample_ids=[before["sample_id"], after["sample_id"]],
            payload={
                "before_sample_id": before["sample_id"],
                "after_sample_id": after["sample_id"],
                "requested_change_text": "把灰尘感去掉，保留黑色层次。",
                "result_feedback_event_id": None,
                "causal_attribution": "unknown",
            },
        )
        feedback = self._event(event_type="feedback", raw_text="这个好多了。", sample_ids=[after["sample_id"]], payload={"explicit_verdict": "approved"})
        correction = self._event(
            event_type="correction",
            raw_text="刚才 A/B 那句说错了。",
            payload={"target_event_ids": [pair["event_id"]], "effect": "retract"},
        )

        effective_ids = {x["event_id"] for x in self.store.effective_evidence()}
        self.assertNotIn(pair["event_id"], effective_ids)
        self.assertIn(revision["event_id"], effective_ids)
        self.assertIn(feedback["event_id"], effective_ids)
        self.assertIn(correction["event_id"], effective_ids)
        self.assertEqual(self.store.read_generation(gen2["generation_id"])["parent_generation_id"], gen1["generation_id"])
        self.assertEqual(self.store.doctor(), [])

    def test_tombstone_excludes_runtime_discovery(self):
        sample, _ = self._sample_with_asset(role="discovery")
        feedback = self._event(event_type="feedback", raw_text="喜欢。", sample_ids=[sample["sample_id"]], payload={"explicit_verdict": "approved"})
        self._event(
            event_type="tombstone",
            raw_text="",
            sample_ids=[sample["sample_id"]],
            payload={"target_record_ids": [sample["sample_id"], feedback["event_id"]], "reason": "synthetic deletion"},
        )
        self.assertNotIn(sample["sample_id"], {x["sample_id"] for x in self.store.discovery_samples()})
        self.assertNotIn(feedback["event_id"], {x["event_id"] for x in self.store.effective_evidence()})


    def test_blind_reserved_reference_requires_reserved_outputs(self):
        blind, _ = self._sample_with_asset(role="blind_eval_reserved", data=b"blind-ref")
        bad_output, _ = self._sample_with_asset(role="production", kind="generated", data=b"bad-output")
        generation = {
            "schema_version": SCHEMA_VERSION,
            "generation_id": new_id("generation"),
            "created_at": utc_now(),
            "renderer": "synthetic-renderer",
            "model": "synthetic-model",
            "model_version": None,
            "task_ref": "blind-case-bad",
            "reference_sample_ids": [blind["sample_id"]],
            "parent_generation_id": None,
            "output_sample_ids": [bad_output["sample_id"]],
            "prompt_text": None,
            "parameters": {},
        }
        with self.assertRaises(RecordValidationError):
            self.store.write_generation(generation)

    def test_blind_eval_isolation_is_transitive(self):
        blind, _ = self._sample_with_asset(role="blind_eval_reserved", data=b"blind")
        blind_output, _ = self._sample_with_asset(role="blind_eval_reserved", kind="generated", data=b"blind-out")
        normal, _ = self._sample_with_asset(role="discovery", data=b"normal")
        gen = {
            "schema_version": SCHEMA_VERSION,
            "generation_id": new_id("generation"),
            "created_at": utc_now(),
            "renderer": "synthetic-renderer",
            "model": "synthetic-model",
            "model_version": None,
            "task_ref": "blind-case-1",
            "reference_sample_ids": [blind["sample_id"]],
            "parent_generation_id": None,
            "output_sample_ids": [blind_output["sample_id"]],
            "prompt_text": None,
            "parameters": {},
        }
        self.store.write_generation(gen)
        blind_feedback = self._event(event_type="feedback", raw_text="盲测里这张更好。", sample_ids=[blind_output["sample_id"]], generation_ids=[gen["generation_id"]], payload={"explicit_verdict": "approved"})
        blind_correction = self._event(event_type="correction", raw_text="补充说明上一条。", payload={"target_event_ids": [blind_feedback["event_id"]], "effect": "clarify"})
        normal_feedback = self._event(event_type="feedback", raw_text="正常样本喜欢。", sample_ids=[normal["sample_id"]], payload={"explicit_verdict": "approved"})
        discovery_ids = {x["event_id"] for x in self.store.discovery_evidence()}
        self.assertNotIn(blind_feedback["event_id"], discovery_ids)
        self.assertNotIn(blind_correction["event_id"], discovery_ids)
        self.assertIn(normal_feedback["event_id"], discovery_ids)

    def test_unresolvable_asset_fails_truthfully(self):
        sample_id = new_id("sample")
        asset_id = new_id("asset")
        asset = {
            "schema_version": SCHEMA_VERSION,
            "asset_id": asset_id,
            "sample_id": sample_id,
            "created_at": utc_now(),
            "sha256": sha256_bytes(b"not-downloaded"),
            "locator_kind": "remote_url",
            "locator": "https://example.invalid/not-a-real-image",
            "asset_relation": "primary",
            "derived_from_asset_id": None,
            "media_type": "image/jpeg",
        }
        sample = {
            "schema_version": SCHEMA_VERSION,
            "sample_id": sample_id,
            "created_at": utc_now(),
            "sample_kind": "reference",
            "primary_asset_id": asset_id,
            "dataset_role": "discovery",
            "provenance": {"source_type": "web", "source_ref": asset["locator"], "creator": None, "license": None},
            "user_tags": [],
        }
        self.store.write_sample(sample)
        self.store.write_asset(asset)
        self.assertIsNone(self.store.resolve_asset(asset_id))

    def test_derived_layer_can_be_destroyed_and_rebuilt(self):
        sample, _ = self._sample_with_asset()
        event = self._event(event_type="feedback", raw_text="喜欢。", sample_ids=[sample["sample_id"]], payload={"explicit_verdict": "approved"})
        source_ids = [event["event_id"]]
        first = self.store.write_derived_artifact(
            artifact_id="synthetic-profile",
            artifact_type="preference_profile",
            builder_version="synthetic-v1",
            source_record_ids=source_ids,
            content={"discovery_event_count": len(self.store.discovery_evidence())},
        )
        import json
        first_record = json.loads(first.read_text(encoding="utf-8"))
        self.store.clear_derived()
        self.assertFalse(first.exists())
        second = self.store.write_derived_artifact(
            artifact_id="synthetic-profile",
            artifact_type="preference_profile",
            builder_version="synthetic-v1",
            source_record_ids=source_ids,
            content={"discovery_event_count": len(self.store.discovery_evidence())},
        )
        second_record = json.loads(second.read_text(encoding="utf-8"))
        for key in ("artifact_id", "artifact_type", "builder_version", "source_record_ids", "content"):
            self.assertEqual(first_record[key], second_record[key])

    def test_backup_restore_preserves_ids_and_links(self):
        sample, asset = self._sample_with_asset(data=b"backup-bytes")
        event = self._event(event_type="feedback", raw_text="喜欢。", sample_ids=[sample["sample_id"]], payload={"explicit_verdict": "approved"})
        archive = Path(self.tmp.name) / "backup.zip"
        create_backup(self.root, archive)
        restored_root = Path(self.tmp.name) / "restored"
        restore_backup(archive, restored_root)
        restored = VisualMemoryStore(restored_root)
        self.assertEqual(restored.read_sample(sample["sample_id"])["sample_id"], sample["sample_id"])
        self.assertEqual(restored.read_asset(asset["asset_id"])["sha256"], asset["sha256"])
        self.assertEqual(restored.read_evidence()[0]["event_id"], event["event_id"])
        self.assertEqual(restored.doctor(), [])
        self.assertIsNotNone(restored.resolve_asset(asset["asset_id"]))


if __name__ == "__main__":
    unittest.main()
