#!/usr/bin/env python3
"""Run PHASE 7 synthetic verification using only the standard library."""
from __future__ import annotations

import sys
import argparse
import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--vpd-state', action='store_true')
    parser.add_argument('--status-card', action='store_true')
    parser.add_argument('--request', type=Path)
    args = parser.parse_args()
    if args.vpd_state:
        from visual_memory.vpd_task_lock import validate_state, validate_request, status_card
        try:
            lock, checkpoint = validate_state(REPO_ROOT)
            if args.request:
                validate_request(REPO_ROOT, json.loads(args.request.read_text(encoding='utf-8')))
            print(json.dumps(status_card(lock, checkpoint) if args.status_card else {'status':'VPD_STATE_VALID', 'next_action':lock['next_required_action']}, ensure_ascii=False, indent=2))
            return 0
        except (ValueError, KeyError, OSError, TypeError, IndexError) as exc:
            print(json.dumps({'status':'VPD_STATE_BLOCKED','reason':str(exc)}, ensure_ascii=False))
            return 1
    suite = unittest.defaultTestLoader.discover(str(REPO_ROOT / "tests" / "visual_memory"), pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
