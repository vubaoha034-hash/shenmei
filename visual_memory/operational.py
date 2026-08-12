"""Operational guardrails for the frozen LIU VISUAL SYSTEM V0.1 private root."""
from __future__ import annotations

import json
import os
import socket
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class OperationalConfigError(RuntimeError):
    pass


def _within(path: Path, parent: Path) -> bool:
    path = path.expanduser().resolve()
    parent = parent.expanduser().resolve()
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


@dataclass(frozen=True)
class OperationalConfig:
    data_root: Path
    backup_dir: Path
    writer_id: str
    calibration_overlay: Path | None = None

    @classmethod
    def from_values(
        cls,
        *,
        data_root: str | os.PathLike[str],
        backup_dir: str | os.PathLike[str],
        writer_id: str,
        calibration_overlay: str | os.PathLike[str] | None = None,
    ) -> "OperationalConfig":
        if not str(writer_id).strip():
            raise OperationalConfigError("writer_id must be non-empty")
        overlay = None if calibration_overlay is None else Path(calibration_overlay).expanduser().resolve()
        return cls(
            data_root=Path(data_root).expanduser().resolve(),
            backup_dir=Path(backup_dir).expanduser().resolve(),
            writer_id=str(writer_id).strip(),
            calibration_overlay=overlay,
        )

    @classmethod
    def from_env(cls) -> "OperationalConfig":
        data_root = os.environ.get("LIU_VISUAL_DATA_ROOT")
        backup_dir = os.environ.get("LIU_VISUAL_BACKUP_DIR")
        writer_id = os.environ.get("LIU_VISUAL_WRITER_ID")
        if not data_root or not backup_dir or not writer_id:
            raise OperationalConfigError(
                "LIU_VISUAL_DATA_ROOT, LIU_VISUAL_BACKUP_DIR and LIU_VISUAL_WRITER_ID are required"
            )
        return cls.from_values(
            data_root=data_root,
            backup_dir=backup_dir,
            writer_id=writer_id,
            calibration_overlay=os.environ.get("LIU_VISUAL_CALIBRATION_OVERLAY"),
        )


def validate_operational_paths(config: OperationalConfig, repo_root: Path) -> list[str]:
    repo_root = repo_root.expanduser().resolve()
    errors: list[str] = []
    if _within(config.data_root, repo_root):
        errors.append("data_root must be outside the public repository")
    if _within(config.backup_dir, repo_root):
        errors.append("backup_dir must be outside the public repository")
    if _within(config.backup_dir, config.data_root) or _within(config.data_root, config.backup_dir):
        errors.append("data_root and backup_dir must not contain one another")
    if config.calibration_overlay is not None:
        if _within(config.calibration_overlay, repo_root):
            errors.append("private calibration overlay must be outside the public repository")
        if _within(config.calibration_overlay, config.data_root / "raw"):
            errors.append("calibration overlay must not be stored inside the canonical raw record tree")
    return errors


class WriterLease:
    """Cross-platform single-writer lock using atomic O_EXCL file creation.

    Stale locks are never broken automatically. A crash therefore fails closed;
    an operator must inspect/remove the stale lock deliberately.
    """

    def __init__(self, root: Path, writer_id: str) -> None:
        self.root = Path(root).expanduser().resolve()
        self.writer_id = writer_id
        self.path = self.root / ".liu_visual_writer.lock"
        self.token = uuid.uuid4().hex
        self._held = False

    def acquire(self) -> "WriterLease":
        self.root.mkdir(parents=True, exist_ok=True)
        payload = {
            "writer_id": self.writer_id,
            "pid": os.getpid(),
            "host": socket.gethostname(),
            "token": self.token,
        }
        flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
        try:
            fd = os.open(str(self.path), flags, 0o600)
        except FileExistsError as exc:
            current = None
            try:
                current = json.loads(self.path.read_text(encoding="utf-8"))
            except Exception:
                pass
            raise RuntimeError(f"visual-memory writer lock already exists: {current or self.path}") from exc
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(payload, handle, ensure_ascii=False, sort_keys=True)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
        except Exception:
            self.path.unlink(missing_ok=True)
            raise
        self._held = True
        return self

    def release(self) -> None:
        if not self._held:
            return
        try:
            current = json.loads(self.path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            self._held = False
            return
        if current.get("token") != self.token:
            raise RuntimeError("writer lock token changed; refusing to remove another writer's lock")
        self.path.unlink()
        self._held = False

    def __enter__(self) -> "WriterLease":
        return self.acquire()

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        self.release()


def initialize_operational_root(
    config: OperationalConfig,
    *,
    repo_root: Path,
    store_factory: Any,
) -> Any:
    errors = validate_operational_paths(config, repo_root)
    if errors:
        raise OperationalConfigError("; ".join(errors))

    config.data_root.mkdir(parents=True, exist_ok=True)
    config.backup_dir.mkdir(parents=True, exist_ok=True)
    marker = config.data_root / ".liu_visual_private_root.json"
    marker_payload = {
        "architecture_version": "0.1",
        "writer_id": config.writer_id,
        "personal_fit_private_overlay_configured": config.calibration_overlay is not None,
    }
    if marker.exists():
        existing = json.loads(marker.read_text(encoding="utf-8"))
        if existing.get("writer_id") != config.writer_id:
            raise OperationalConfigError(
                f"private root is owned by writer_id={existing.get('writer_id')!r}; "
                "writer changes require an explicit operational migration"
            )
    else:
        marker.write_text(json.dumps(marker_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if config.calibration_overlay is not None:
        config.calibration_overlay.parent.mkdir(parents=True, exist_ok=True)

    store = store_factory(config.data_root)
    if hasattr(store, "assert_outside_public_repo"):
        store.assert_outside_public_repo(repo_root)
    return store


def operational_status(config: OperationalConfig, repo_root: Path) -> dict[str, Any]:
    errors = validate_operational_paths(config, repo_root)
    return {
        "status": "PASS" if not errors else "BLOCKED",
        "errors": errors,
        "single_writer_required": True,
        "private_calibration_overlay_configured": config.calibration_overlay is not None,
        "formal_personal_fit_authorized": False,
    }
