#!/usr/bin/env python3
"""Physically purge tombstoned private records/assets from LIU VISUAL SYSTEM V0.1."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from visual_memory.operational import WriterLease
from visual_memory.purge import purge_tombstoned
from visual_memory.store import VisualMemoryStore


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record_ids", nargs="+")
    parser.add_argument("--data-root", default=os.environ.get("LIU_VISUAL_DATA_ROOT"))
    parser.add_argument("--writer-id", default=os.environ.get("LIU_VISUAL_WRITER_ID"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if not args.data_root or not args.writer_id:
        raise SystemExit("--data-root and --writer-id are required (or set LIU_VISUAL_* env vars)")
    store = VisualMemoryStore(args.data_root)
    with WriterLease(store.root, args.writer_id):
        result = purge_tombstoned(store, args.record_ids, dry_run=args.dry_run)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
