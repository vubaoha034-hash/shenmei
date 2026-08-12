#!/usr/bin/env python3
"""Close PHASE 8 operational gates on the actual private writer host.

This command never imports personal reference images. It initializes the private
root and exercises the frozen persistence contract with disposable synthetic
records only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from visual_memory.backup import create_backup, restore_backup
from visual_memory.operational import OperationalConfig, WriterLease, initialize_operational_root, operational_status
from visual_memory.purge import purge_tombstoned
from visual_memory.store import SCHEMA_VERSION, VisualMemoryStore, new_id, sha256_bytes, utc_now


def _file_sha256(path: Path) -> str | None:
    if not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _arg_or_env(value: str | None, env_name: str) -> str | None:
    return value if value else os.environ.get(env_name)


def _make_synthetic(store: VisualMemoryStore) -> tuple[str, str, str]:
    sample_id = new_id("sample")
    asset_id = new_id("asset")
    event_id = new_id("event")
    data = b"PHASE8-SYNTHETIC-NON-SENSITIVE-ASSET"
    vault = store.write_vault_bytes(asset_id, data, ".bin")
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
    sample = {
        "schema_version": SCHEMA_VERSION,
        "sample_id": sample_id,
        "created_at": utc_now(),
        "sample_kind": "reference",
        "primary_asset_id": asset_id,
        "dataset_role": "discovery",
        "provenance": {"source_type": "unknown", "source_ref": None, "creator": None, "license": None},
        "user_tags": [],
    }
    event = {
        "schema_version": SCHEMA_VERSION,
        "event_id": event_id,
        "occurred_at": utc_now(),
        "event_type": "feedback",
        "source_kind": "user",
        "source_ref": None,
        "scope": {"level": "task", "domain": None},
        "raw_text": "PHASE 8 synthetic explicit approval.",
        "target_sample_ids": [sample_id],
        "target_generation_ids": [],
        "payload": {"explicit_verdict": "approved"},
    }
    store.write_sample(sample)
    store.write_asset(asset)
    store.append_evidence(event)
    store.write_derived_artifact(
        artifact_id="phase8-synthetic-profile",
        artifact_type="preference_profile",
        builder_version="phase8-preflight-v1",
        source_record_ids=[event_id],
        content={"synthetic": True},
    )
    return sample_id, asset_id, event_id


def _run_phase7_suite(repo_root: Path) -> None:
    proc = subprocess.run(
        [sys.executable, str(repo_root / "scripts" / "verify_visual_memory.py")],
        cwd=str(repo_root),
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError("PHASE 7 synthetic verification failed in the operational host")


def run_preflight(config: OperationalConfig, repo_root: Path) -> dict[str, object]:
    repo_root = repo_root.resolve()
    public_calibration = repo_root / "calibration" / "anchors.json"
    calibration_before = _file_sha256(public_calibration)
    status = operational_status(config, repo_root)
    if status["status"] != "PASS":
        raise RuntimeError("; ".join(str(x) for x in status["errors"]))

    initialize_operational_root(config, repo_root=repo_root, store_factory=VisualMemoryStore)
    report: dict[str, object] = {
        "phase": "8",
        "status": "RUNNING",
        "writer_id": config.writer_id,
        "real_personal_data_imported": False,
        "formal_personal_fit_authorized": False,
        "private_calibration_overlay_configured": config.calibration_overlay is not None,
    }

    synthetic_root = config.data_root / f".phase8-synthetic-{uuid.uuid4().hex}"
    restore_root = config.data_root / f".phase8-restore-{uuid.uuid4().hex}"
    backup_zip = config.backup_dir / f"phase8-preflight-{uuid.uuid4().hex}.zip"
    try:
        with WriterLease(config.data_root, config.writer_id):
            report["writer_lock"] = "PASS"
            _run_phase7_suite(repo_root)
            report["phase7_synthetic_suite"] = "PASS"

            synthetic = VisualMemoryStore(synthetic_root)
            sample_id, asset_id, event_id = _make_synthetic(synthetic)
            if synthetic.doctor():
                raise RuntimeError(f"synthetic store failed doctor before backup: {synthetic.doctor()}")

            create_backup(synthetic_root, backup_zip)
            restore_backup(backup_zip, restore_root)
            restored = VisualMemoryStore(restore_root)
            if restored.doctor():
                raise RuntimeError(f"restored store failed doctor: {restored.doctor()}")
            if restored.read_sample(sample_id) is None or restored.resolve_asset(asset_id) is None:
                raise RuntimeError("backup/restore did not preserve synthetic ids/assets")
            report["backup_restore"] = "PASS"

            tombstone = {
                "schema_version": SCHEMA_VERSION,
                "event_id": new_id("event"),
                "occurred_at": utc_now(),
                "event_type": "tombstone",
                "source_kind": "user",
                "source_ref": None,
                "scope": {"level": "task", "domain": None},
                "raw_text": "",
                "target_sample_ids": [sample_id],
                "target_generation_ids": [],
                "payload": {
                    "target_record_ids": [sample_id, asset_id, event_id],
                    "reason": "PHASE 8 synthetic purge verification",
                },
            }
            synthetic.append_evidence(tombstone)
            purge_tombstoned(synthetic, [sample_id, asset_id, event_id])
            if synthetic.resolve_asset(asset_id) is not None:
                raise RuntimeError("purge did not make synthetic asset unavailable")
            if any(x.get("event_id") == event_id for x in synthetic.read_evidence()):
                raise RuntimeError("purge did not physically remove targeted synthetic evidence")
            if synthetic.read_sample(sample_id)["provenance"].get("source_ref") is not None:
                raise RuntimeError("purge did not scrub synthetic sample provenance")
            if any(synthetic.derived_dir.iterdir()):
                raise RuntimeError("purge did not clear derived cache")
            report["physical_purge"] = "PASS"
    finally:
        shutil.rmtree(synthetic_root, ignore_errors=True)
        shutil.rmtree(restore_root, ignore_errors=True)
        backup_zip.unlink(missing_ok=True)

    calibration_after = _file_sha256(public_calibration)
    if calibration_before != calibration_after:
        raise RuntimeError("public calibration/anchors.json changed during private preflight")
    report["public_calibration_unchanged"] = True
    report["private_root_outside_public_git"] = True
    report["backup_dir_outside_public_git"] = True
    report["pilot_authorized_on_this_writer_host"] = True
    report["status"] = "PASS"

    operations_dir = config.data_root / "operations"
    operations_dir.mkdir(parents=True, exist_ok=True)
    report_path = operations_dir / "phase8_preflight.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--data-root")
    parser.add_argument("--backup-dir")
    parser.add_argument("--writer-id")
    parser.add_argument("--calibration-overlay")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    data_root = _arg_or_env(args.data_root, "LIU_VISUAL_DATA_ROOT")
    backup_dir = _arg_or_env(args.backup_dir, "LIU_VISUAL_BACKUP_DIR")
    writer_id = _arg_or_env(args.writer_id, "LIU_VISUAL_WRITER_ID")
    calibration_overlay = _arg_or_env(args.calibration_overlay, "LIU_VISUAL_CALIBRATION_OVERLAY")
    if not data_root or not backup_dir or not writer_id:
        raise SystemExit(
            "Provide --data-root/--backup-dir/--writer-id or set "
            "LIU_VISUAL_DATA_ROOT, LIU_VISUAL_BACKUP_DIR, LIU_VISUAL_WRITER_ID"
        )
    config = OperationalConfig.from_values(
        data_root=data_root,
        backup_dir=backup_dir,
        writer_id=writer_id,
        calibration_overlay=calibration_overlay,
    )
    report = run_preflight(config, args.repo_root)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
