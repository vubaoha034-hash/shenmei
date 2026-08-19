#!/usr/bin/env python3
"""Repository-level dry-run validation for the strict VPD V1 renderer adapter."""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from visual_memory.vpd_renderer_adapter import execute_task, load_freeze, validate_freeze

FREEZE = REPO_ROOT / "VPD_DISTILLATION_ONLY_RUNTIME_TEST_V1_CONTROLLER_PAYLOAD_FREEZE.json"
EXPECTED_PROMPT_SHA256 = {
    "T1": "dbd9fc6a3aa61f005b83764de74e4804b81380a2ae0bae8bed4dd44fb9008ea4",
    "T2": "d3e407c9ff69de75b1c79105add030f2576620c992613acef78f1bb65b78a5a2",
    "T3": "815178e9a653267619e01a8d16db30eaa5747ce0c78ed3129d322b243283bda7",
}


def main() -> int:
    frozen = validate_freeze(load_freeze(FREEZE))
    actual = {
        row["test_id"]: row["final_renderer_payload_sha256"]
        for row in frozen["tasks"]
    }
    if actual != EXPECTED_PROMPT_SHA256:
        raise SystemExit(f"frozen prompt identity drift: {actual!r}")

    with tempfile.TemporaryDirectory(prefix="vpd-renderer-dry-run-") as temp:
        results = [
            execute_task(FREEZE, task_id, temp, allow_network=False)
            for task_id in ("T1", "T2", "T3")
        ]

    if any(row.get("status") != "DRY_RUN_PASS" for row in results):
        raise SystemExit("one or more VPD renderer dry-runs failed")
    if any(row.get("exact_prompt_binding_proven") is not True for row in results):
        raise SystemExit("exact prompt binding was not proven")
    if any(row.get("reference_images_attached") != 0 for row in results):
        raise SystemExit("reference-image count drifted above zero")

    print(json.dumps({
        "status": "VPD_RENDERER_ADAPTER_DRY_RUN_PASS",
        "freeze": str(FREEZE.relative_to(REPO_ROOT)),
        "tasks": results,
    }, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
