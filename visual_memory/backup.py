"""Small deterministic backup/restore helpers for the private V0.1 root."""
from __future__ import annotations

import shutil
from pathlib import Path


def _within(path: Path, parent: Path) -> bool:
    path = path.resolve()
    parent = parent.resolve()
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def create_backup(root: Path, destination_zip: Path) -> Path:
    root = root.resolve()
    destination_zip = destination_zip.resolve()
    if not root.is_dir():
        raise FileNotFoundError(root)
    if _within(destination_zip, root):
        raise ValueError("backup destination must be outside the data root")
    if destination_zip.exists():
        raise FileExistsError(destination_zip)
    destination_zip.parent.mkdir(parents=True, exist_ok=True)
    base = destination_zip.with_suffix("")
    archive = shutil.make_archive(str(base), "zip", root_dir=str(root))
    return Path(archive)


def restore_backup(archive_zip: Path, destination_root: Path) -> Path:
    archive_zip = archive_zip.resolve()
    destination_root = destination_root.resolve()
    if not archive_zip.is_file():
        raise FileNotFoundError(archive_zip)
    if destination_root.exists() and any(destination_root.iterdir()):
        raise FileExistsError(f"restore destination is not empty: {destination_root}")
    destination_root.mkdir(parents=True, exist_ok=True)
    shutil.unpack_archive(str(archive_zip), str(destination_root), "zip")
    return destination_root
