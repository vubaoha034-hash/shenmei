from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from visual_memory.backup import create_backup
from visual_memory.operational import (
    OperationalConfig,
    OperationalConfigError,
    WriterLease,
    initialize_operational_root,
    validate_operational_paths,
)
from visual_memory.purge import PurgeError, purge_tombstoned
from visual_memory.store import SCHEMA_VERSION, VisualMemoryStore, new_id, sha256_bytes, utc_now


class OperationalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.repo = self.base / "public-repo"
        self.repo.mkdir()
        self.data = self.base / "private-data"
        self.backup = self.base / "private-backup"

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _config(self, writer_id: str = "writer-a") -> OperationalConfig:
        return OperationalConfig.from_values(data_root=self.data, backup_dir=self.backup, writer_id=writer_id)

    def _sample_asset_feedback(self, store: VisualMemoryStore):
        sample_id = new_id("sample")
        asset_id = new_id("asset")
        event_id = new_id("event")
        data = b"phase8-private-synthetic"
        vault = store.write_vault_bytes(asset_id, data, ".bin")
        sample = {
            "schema_version": SCHEMA_VERSION,
            "sample_id": sample_id,
            "created_at": utc_now(),
            "sample_kind": "reference",
            "primary_asset_id": asset_id,
            "dataset_role": "discovery",
            "provenance": {"source_type": "web", "source_ref": "synthetic://secret", "creator": None, "license": None},
            "user_tags": ["synthetic-secret"],
        }
        asset = {
            "schema_version": SCHEMA_VERSION,
            "asset_id": asset_id,
            "sample_id": sample_id,
            "created_at": utc_now(),
            "sha256": sha256_bytes(data),
            "locator_kind": "local_file",
            "locator": str(vault.relative_to(store.root)),
            "asset_relation": "primary",
            "derived_from_asset_id": None,
            "media_type": "application/octet-stream",
        }
        event = {
            "schema_version": SCHEMA_VERSION,
            "event_id": event_id,
            "occurred_at": utc_now(),
            "event_type": "feedback",
            "source_kind": "user",
            "source_ref": None,
            "scope": {"level": "task", "domain": None},
            "raw_text": "synthetic private feedback",
            "target_sample_ids": [sample_id],
            "target_generation_ids": [],
            "payload": {"explicit_verdict": "approved"},
        }
        store.write_sample(sample)
        store.write_asset(asset)
        store.append_evidence(event)
        return sample, asset, event

    def test_operational_paths_reject_public_and_overlapping_roots(self):
        bad_public = OperationalConfig.from_values(
            data_root=self.repo / "private",
            backup_dir=self.backup,
            writer_id="writer-a",
        )
        self.assertTrue(validate_operational_paths(bad_public, self.repo))
        bad_overlap = OperationalConfig.from_values(
            data_root=self.data,
            backup_dir=self.data / "backup",
            writer_id="writer-a",
        )
        self.assertTrue(validate_operational_paths(bad_overlap, self.repo))

    def test_writer_lease_is_exclusive_and_releasable(self):
        with WriterLease(self.data, "writer-a"):
            with self.assertRaises(RuntimeError):
                WriterLease(self.data, "writer-b").acquire()
        with WriterLease(self.data, "writer-b"):
            self.assertTrue((self.data / ".liu_visual_writer.lock").exists())
        self.assertFalse((self.data / ".liu_visual_writer.lock").exists())

    def test_private_root_marker_prevents_silent_writer_change(self):
        initialize_operational_root(self._config("writer-a"), repo_root=self.repo, store_factory=VisualMemoryStore)
        with self.assertRaises(OperationalConfigError):
            initialize_operational_root(self._config("writer-b"), repo_root=self.repo, store_factory=VisualMemoryStore)

    def test_backup_refuses_destination_inside_data_root_or_existing_archive(self):
        store = initialize_operational_root(self._config(), repo_root=self.repo, store_factory=VisualMemoryStore)
        with self.assertRaises(ValueError):
            create_backup(store.root, store.root / "bad.zip")
        existing = self.backup / "existing.zip"
        existing.parent.mkdir(parents=True, exist_ok=True)
        existing.write_bytes(b"x")
        with self.assertRaises(FileExistsError):
            create_backup(store.root, existing)

    def test_physical_purge_requires_tombstone_then_scrubs_private_payload(self):
        store = initialize_operational_root(self._config(), repo_root=self.repo, store_factory=VisualMemoryStore)
        sample, asset, event = self._sample_asset_feedback(store)
        generation_id = new_id("generation")
        generation = {
            "schema_version": SCHEMA_VERSION,
            "generation_id": generation_id,
            "created_at": utc_now(),
            "renderer": "synthetic-renderer",
            "model": "synthetic-model",
            "model_version": None,
            "task_ref": "synthetic-private-task",
            "reference_sample_ids": [sample["sample_id"]],
            "parent_generation_id": None,
            "output_sample_ids": [],
            "prompt_text": "synthetic private prompt",
            "parameters": {"private": "synthetic"},
        }
        store.write_generation(generation)
        store.write_derived_artifact(
            artifact_id="synthetic-profile",
            artifact_type="preference_profile",
            builder_version="test",
            source_record_ids=[event["event_id"]],
            content={"private": "synthetic"},
        )
        with self.assertRaises(PurgeError):
            purge_tombstoned(store, [sample["sample_id"]])

        tombstone = {
            "schema_version": SCHEMA_VERSION,
            "event_id": new_id("event"),
            "occurred_at": utc_now(),
            "event_type": "tombstone",
            "source_kind": "user",
            "source_ref": None,
            "scope": {"level": "task", "domain": None},
            "raw_text": "",
            "target_sample_ids": [sample["sample_id"]],
            "target_generation_ids": [],
            "payload": {
                "target_record_ids": [sample["sample_id"], asset["asset_id"], event["event_id"]],
                "reason": "synthetic purge test",
            },
        }
        store.append_evidence(tombstone)
        purge_tombstoned(store, [sample["sample_id"], asset["asset_id"], event["event_id"]])

        self.assertIsNone(store.resolve_asset(asset["asset_id"]))
        self.assertEqual(store.read_asset(asset["asset_id"])["locator_kind"], "opaque")
        self.assertIsNone(store.read_sample(sample["sample_id"])["provenance"]["source_ref"])
        self.assertEqual(store.read_sample(sample["sample_id"])["user_tags"], [])
        self.assertIsNone(store.read_generation(generation_id)["prompt_text"])
        self.assertEqual(store.read_generation(generation_id)["parameters"], {})
        self.assertNotIn(event["event_id"], {e["event_id"] for e in store.read_evidence()})
        self.assertFalse(any(store.derived_dir.iterdir()))
        self.assertEqual(store.doctor(), [])


if __name__ == "__main__":
    unittest.main()
