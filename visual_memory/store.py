"""Private file-backed minimal store for LIU VISUAL SYSTEM V0.1.

The store is deliberately small and single-writer. It proves the frozen
contract without selecting a permanent database or cloud asset provider.
"""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .replay import discovery_evidence, effective_evidence
from .validation import RecordValidationError, validate_record

SCHEMA_VERSION = "1"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def new_id(kind: str) -> str:
    prefixes = {"sample": "smp", "asset": "ast", "event": "ev", "generation": "gen"}
    try:
        prefix = prefixes[kind]
    except KeyError as exc:
        raise ValueError(f"unknown id kind: {kind}") from exc
    return f"{prefix}_{uuid.uuid4()}"


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


class VisualMemoryStore:
    """Single-writer V0.1 private store.

    The caller must pass an explicit private root. No default path points into
    the public repository, preventing accidental personal-data persistence in
    Git by convenience.
    """

    def __init__(self, root: str | os.PathLike[str]) -> None:
        self.root = Path(root).expanduser().resolve()
        self.raw_root = self.root / "raw"
        self.samples_dir = self.raw_root / "samples"
        self.assets_dir = self.raw_root / "assets"
        self.generations_dir = self.raw_root / "generations"
        self.evidence_dir = self.raw_root / "evidence"
        self.evidence_file = self.evidence_dir / "events.jsonl"
        self.vault_dir = self.root / "vault"
        self.derived_dir = self.root / "derived"
        for path in (
            self.samples_dir,
            self.assets_dir,
            self.generations_dir,
            self.evidence_dir,
            self.vault_dir,
            self.derived_dir,
        ):
            path.mkdir(parents=True, exist_ok=True)

    @classmethod
    def from_env(cls, env_var: str = "LIU_VISUAL_DATA_ROOT") -> "VisualMemoryStore":
        value = os.environ.get(env_var)
        if not value:
            raise RuntimeError(f"{env_var} must point to an explicit private data root")
        return cls(value)

    @staticmethod
    def _atomic_json_write(path: Path, record: dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, temp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(record, handle, ensure_ascii=False, indent=2, sort_keys=True)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temp_name, path)
        except Exception:
            try:
                os.unlink(temp_name)
            except FileNotFoundError:
                pass
            raise

    @staticmethod
    def _load_json(path: Path) -> dict[str, Any]:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        if not isinstance(data, dict):
            raise RecordValidationError(f"{path} must contain a JSON object")
        return data

    def write_sample(self, record: dict[str, Any]) -> Path:
        validate_record("sample", record)
        path = self.samples_dir / f"{record['sample_id']}.json"
        if path.exists():
            raise FileExistsError(path)
        self._atomic_json_write(path, record)
        return path

    def assert_outside_public_repo(self, public_repo_root: str | os.PathLike[str]) -> None:
        repo = Path(public_repo_root).expanduser().resolve()
        try:
            self.root.relative_to(repo)
        except ValueError:
            return
        raise RuntimeError(f"private data root must be outside public repository: {self.root}")

    def write_asset(self, record: dict[str, Any]) -> Path:
        validate_record("asset", record)
        path = self.assets_dir / f"{record['asset_id']}.json"
        if path.exists():
            raise FileExistsError(path)
        self._atomic_json_write(path, record)
        return path

    def update_asset_locator(self, asset_id: str, *, locator_kind: str, locator: str) -> Path:
        record = self.read_asset(asset_id)
        if record is None:
            raise FileNotFoundError(asset_id)
        updated = dict(record)
        updated["locator_kind"] = locator_kind
        updated["locator"] = locator
        validate_record("asset", updated)
        path = self.assets_dir / f"{asset_id}.json"
        self._atomic_json_write(path, updated)
        return path

    def write_generation(self, record: dict[str, Any]) -> Path:
        validate_record("generation", record)
        if any(self.sample_role(sample_id) == "blind_eval_reserved" for sample_id in record.get("reference_sample_ids", [])):
            not_reserved = [sample_id for sample_id in record.get("output_sample_ids", []) if self.sample_role(sample_id) != "blind_eval_reserved"]
            if not_reserved:
                raise RecordValidationError("outputs from a reserved-reference blind case must also be blind_eval_reserved")
        path = self.generations_dir / f"{record['generation_id']}.json"
        if path.exists():
            raise FileExistsError(path)
        self._atomic_json_write(path, record)
        return path

    def append_evidence(self, record: dict[str, Any]) -> None:
        validate_record("evidence", record)
        if any(event.get("event_id") == record["event_id"] for event in self.read_evidence()):
            raise FileExistsError(f"duplicate event_id: {record['event_id']}")
        line = json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"
        self.evidence_file.parent.mkdir(parents=True, exist_ok=True)
        with self.evidence_file.open("a", encoding="utf-8") as handle:
            handle.write(line)
            handle.flush()
            os.fsync(handle.fileno())

    def _load_typed_json(self, path: Path, kind: str) -> dict[str, Any]:
        record = self._load_json(path)
        validate_record(kind, record)
        return record

    def read_sample(self, sample_id: str) -> dict[str, Any] | None:
        path = self.samples_dir / f"{sample_id}.json"
        return self._load_typed_json(path, "sample") if path.is_file() else None

    def read_asset(self, asset_id: str) -> dict[str, Any] | None:
        path = self.assets_dir / f"{asset_id}.json"
        return self._load_typed_json(path, "asset") if path.is_file() else None

    def read_generation(self, generation_id: str) -> dict[str, Any] | None:
        path = self.generations_dir / f"{generation_id}.json"
        return self._load_typed_json(path, "generation") if path.is_file() else None

    def _read_all_json(self, directory: Path, kind: str) -> list[dict[str, Any]]:
        return [self._load_typed_json(path, kind) for path in sorted(directory.glob("*.json"))]

    def read_samples(self) -> list[dict[str, Any]]:
        return self._read_all_json(self.samples_dir, "sample")

    def read_assets(self) -> list[dict[str, Any]]:
        return self._read_all_json(self.assets_dir, "asset")

    def read_generations(self) -> list[dict[str, Any]]:
        return self._read_all_json(self.generations_dir, "generation")

    def read_evidence(self) -> list[dict[str, Any]]:
        if not self.evidence_file.exists():
            return []
        out: list[dict[str, Any]] = []
        with self.evidence_file.open("r", encoding="utf-8") as handle:
            for line_no, line in enumerate(handle, 1):
                if not line.strip():
                    continue
                data = json.loads(line)
                validate_record("evidence", data)
                out.append(data)
        return out

    def write_vault_bytes(self, asset_id: str, data: bytes, suffix: str = ".bin") -> Path:
        if not suffix.startswith(".") or any(ch in suffix for ch in ("/", "\\")):
            raise ValueError("suffix must be a simple extension")
        path = self.vault_dir / f"{asset_id}{suffix.lower()}"
        if path.exists():
            raise FileExistsError(path)
        path.write_bytes(data)
        return path

    def resolve_asset(self, asset_id: str, *, repo_root: Path | None = None) -> Path | None:
        record = self.read_asset(asset_id)
        if record is None:
            return None
        kind = record["locator_kind"]
        locator = str(record["locator"])
        if kind == "local_file":
            path = Path(locator).expanduser()
            if not path.is_absolute():
                path = self.root / path
            path = path.resolve()
        elif kind == "repo_relative":
            if repo_root is None:
                return None
            path = (repo_root.resolve() / locator).resolve()
            try:
                path.relative_to(repo_root.resolve())
            except ValueError:
                return None
        else:
            return None
        if not path.is_file():
            return None
        if sha256_file(path) != record["sha256"]:
            return None
        return path

    def sample_role(self, sample_id: str) -> str | None:
        record = self.read_sample(sample_id)
        return str(record["dataset_role"]) if record else None

    def generation_is_reserved(self, generation_id: str) -> bool:
        record = self.read_generation(generation_id)
        if record is None:
            return False
        ids = list(record.get("reference_sample_ids", [])) + list(record.get("output_sample_ids", []))
        return any(self.sample_role(sample_id) == "blind_eval_reserved" for sample_id in ids)

    def effective_evidence(self) -> list[dict[str, Any]]:
        return effective_evidence(self.read_evidence())

    def discovery_evidence(self) -> list[dict[str, Any]]:
        return discovery_evidence(
            self.read_evidence(),
            sample_role=self.sample_role,
            generation_is_reserved=self.generation_is_reserved,
        )

    def tombstoned_ids(self) -> set[str]:
        ids: set[str] = set()
        for event in self.read_evidence():
            if event.get("event_type") == "tombstone":
                ids.update(str(x) for x in event.get("payload", {}).get("target_record_ids", []))
        return ids

    def discovery_samples(self) -> list[dict[str, Any]]:
        tombstoned = self.tombstoned_ids()
        return [
            sample
            for sample in self.read_samples()
            if sample["sample_id"] not in tombstoned
            and sample["dataset_role"] in {"discovery", "production"}
        ]

    def write_derived_artifact(
        self,
        *,
        artifact_id: str,
        artifact_type: str,
        builder_version: str,
        source_record_ids: Iterable[str],
        content: dict[str, Any],
    ) -> Path:
        record = {
            "artifact_id": artifact_id,
            "artifact_type": artifact_type,
            "built_at": utc_now(),
            "builder_version": builder_version,
            "source_record_ids": list(source_record_ids),
            "content": content,
        }
        path = self.derived_dir / f"{artifact_id}.json"
        self._atomic_json_write(path, record)
        return path

    def clear_derived(self) -> None:
        for path in self.derived_dir.glob("*"):
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                import shutil
                shutil.rmtree(path)

    def doctor(self) -> list[str]:
        """Return integrity errors; an empty list is PASS."""
        errors: list[str] = []
        samples = {r["sample_id"]: r for r in self.read_samples()}
        assets = {r["asset_id"]: r for r in self.read_assets()}
        generations = {r["generation_id"]: r for r in self.read_generations()}
        events = self.read_evidence()
        event_ids = {r["event_id"] for r in events}

        for sample in samples.values():
            if sample["primary_asset_id"] not in assets:
                errors.append(f"sample {sample['sample_id']} missing primary asset {sample['primary_asset_id']}")
        for asset in assets.values():
            if asset["sample_id"] not in samples:
                errors.append(f"asset {asset['asset_id']} missing sample {asset['sample_id']}")
            parent = asset.get("derived_from_asset_id")
            if parent is not None and parent not in assets:
                errors.append(f"asset {asset['asset_id']} missing parent asset {parent}")
            if asset.get("locator_kind") == "local_file":
                resolved = self.resolve_asset(asset["asset_id"])
                if resolved is None:
                    errors.append(f"asset {asset['asset_id']} local bytes missing or sha256 mismatch")
        for generation in generations.values():
            for sample_id in generation.get("reference_sample_ids", []) + generation.get("output_sample_ids", []):
                if sample_id not in samples:
                    errors.append(f"generation {generation['generation_id']} missing sample {sample_id}")
            parent = generation.get("parent_generation_id")
            if parent is not None and parent not in generations:
                errors.append(f"generation {generation['generation_id']} missing parent generation {parent}")
        for event in events:
            for sample_id in event.get("target_sample_ids", []):
                if sample_id not in samples and sample_id not in self.tombstoned_ids():
                    errors.append(f"event {event['event_id']} missing target sample {sample_id}")
            for generation_id in event.get("target_generation_ids", []):
                if generation_id not in generations and generation_id not in self.tombstoned_ids():
                    errors.append(f"event {event['event_id']} missing target generation {generation_id}")
            if event.get("event_type") == "correction":
                for target_id in event.get("payload", {}).get("target_event_ids", []):
                    if target_id not in event_ids and target_id not in self.tombstoned_ids():
                        errors.append(f"correction {event['event_id']} missing event {target_id}")
        return sorted(set(errors))
