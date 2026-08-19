#!/usr/bin/env python3
"""Serial T1/T2/T3 runner for VPD Distillation-Only Runtime Test V1.

The runner never reads Drive or reference images. It reuses the already-frozen
controller payload JSON, invokes the strict zero-reference renderer adapter in
T1 -> T2 -> T3 order, and stops on the first technical failure.

Network execution is opt-in via ``--execute``. Outputs must live outside the
repository so formal image bytes and provider receipts cannot be accidentally
committed to the public source tree.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from visual_memory.vpd_renderer_adapter import (
    VPDRendererAdapterError,
    execute_task,
    load_freeze,
    validate_freeze,
)

FREEZE = REPO_ROOT / "VPD_DISTILLATION_ONLY_RUNTIME_TEST_V1_CONTROLLER_PAYLOAD_FREEZE.json"
TASK_ORDER = ("T1", "T2", "T3")


def _ensure_external_output_dir(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    repo = REPO_ROOT.resolve()
    try:
        resolved.relative_to(repo)
    except ValueError:
        return resolved
    raise VPDRendererAdapterError(
        "output directory must be outside the repository; formal V1 images/receipts may not be written into Git"
    )


def run(output_dir: str | Path, *, execute: bool = False, quality: str = "high") -> dict:
    output_root = _ensure_external_output_dir(Path(output_dir))
    validate_freeze(load_freeze(FREEZE))
    output_root.mkdir(parents=True, exist_ok=True)

    manifest_path = output_root / "VPD-DOR-V1_RUN_MANIFEST.json"
    if manifest_path.exists():
        raise VPDRendererAdapterError("refusing to overwrite an existing V1 run manifest")

    manifest = {
        "schema_version": "vpd-distillation-only-runtime-test-v1-run/v1",
        "protocol": "VPD_DISTILLATION_ONLY_RUNTIME_TEST_V1.md",
        "freeze": str(FREEZE),
        "task_order": list(TASK_ORDER),
        "reference_runtime_policy": "NONE",
        "reference_images_attached": 0,
        "hidden_variants": 0,
        "best_of_n": "NO",
        "aesthetic_retries": 0,
        "network_execution": bool(execute),
        "results": [],
        "status": "RUNNING",
    }

    try:
        for task_id in TASK_ORDER:
            result = execute_task(
                FREEZE,
                task_id,
                output_root,
                quality=quality,
                allow_network=execute,
            )
            manifest["results"].append(result)
        manifest["status"] = "THREE_TASKS_DRY_RUN_PASS" if not execute else "THREE_FORMAL_OUTPUTS_TECHNICALLY_VALID"
        return manifest
    except Exception as exc:
        manifest["status"] = "STOPPED_ON_TECHNICAL_FAILURE"
        manifest["failure"] = {
            "type": type(exc).__name__,
            "message": str(exc),
            "completed_task_count": len(manifest["results"]),
            "next_task_if_any": TASK_ORDER[len(manifest["results"])] if len(manifest["results"]) < len(TASK_ORDER) else None,
        }
        raise
    finally:
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run VPD Distillation-Only Runtime Test V1 serially")
    parser.add_argument("--output-dir", required=True, help="External/private directory; must be outside the Git repository")
    parser.add_argument("--quality", default="high", choices=("low", "medium", "high"))
    parser.add_argument("--execute", action="store_true", help="Call the OpenAI Images API; requires OPENAI_API_KEY")
    args = parser.parse_args(argv)
    try:
        manifest = run(args.output_dir, execute=args.execute, quality=args.quality)
    except VPDRendererAdapterError as exc:
        print(json.dumps({"status": "FAILED_CLOSED", "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
