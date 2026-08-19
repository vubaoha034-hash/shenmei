"""Strict zero-reference renderer adapter for VPD Distillation-Only Runtime Test V1.

This module binds the exact controller-frozen ``final_renderer_payload`` to an
explicit provider request. It does not re-distill references, change aesthetic
rules, or support reference-image conditioning.

The adapter fails closed before network I/O unless the frozen V1 contract is
internally consistent, including prompt SHA-256 and NONE/0 reference policy.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import struct
import tempfile
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping


ADAPTER_VERSION = "1"
FREEZE_SCHEMA = "vpd-distillation-only-runtime-test-v1-controller-freeze/v1"
OPENAI_IMAGES_ENDPOINT = "https://api.openai.com/v1/images/generations"
DEFAULT_MODEL = "gpt-image-2-2026-04-21"
DEFAULT_QUALITY = "high"
ALLOWED_SIZE = "1024x1536"
ALLOWED_OUTPUT_FORMAT = "png"
UNAVAILABLE_BY_PROVIDER = "UNAVAILABLE_BY_PROVIDER"


class VPDRendererAdapterError(RuntimeError):
    """Raised whenever V1 runtime integrity cannot be proven."""


@dataclass(frozen=True)
class HTTPResult:
    status: int
    headers: Mapping[str, str]
    body: bytes


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def text_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def bytes_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json_sha256(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return text_sha256(payload)


def _require_dict(value: Any, field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise VPDRendererAdapterError(f"{field} must be an object")
    return value


def _require_str(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise VPDRendererAdapterError(f"{field} must be a non-empty string")
    return value


def load_freeze(path: str | Path) -> dict[str, Any]:
    source = Path(path)
    try:
        value = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise VPDRendererAdapterError(f"cannot load freeze file: {source}") from exc
    return _require_dict(value, "freeze")


def select_task(freeze: dict[str, Any], task_id: str) -> dict[str, Any]:
    tasks = freeze.get("tasks")
    if not isinstance(tasks, list):
        raise VPDRendererAdapterError("freeze.tasks must be a list")
    matches = [row for row in tasks if isinstance(row, dict) and row.get("test_id") == task_id]
    if len(matches) != 1:
        raise VPDRendererAdapterError(f"expected exactly one frozen task for {task_id}")
    return matches[0]


def validate_freeze(freeze: dict[str, Any]) -> dict[str, Any]:
    if freeze.get("schema_version") != FREEZE_SCHEMA:
        raise VPDRendererAdapterError("unsupported freeze schema")

    preflight = _require_dict(freeze.get("fresh_context_preflight"), "fresh_context_preflight")
    required_false = (
        "approved_reference_pixels_loaded",
        "mother_reference_loaded",
        "golden_exemplar_loaded",
        "contact_sheet_loaded",
        "drive_preview_loaded",
        "previous_vpd_output_images_loaded",
        "drive_accessed",
    )
    for field in required_false:
        if preflight.get(field) is not False:
            raise VPDRendererAdapterError(f"fresh-context isolation failed: {field}")
    if preflight.get("github_text_only_before_freeze") is not True:
        raise VPDRendererAdapterError("GitHub-text-only preflight was not proven")
    if preflight.get("verdict") != "FRESH_CONTEXT_PREFLIGHT_PASS":
        raise VPDRendererAdapterError("fresh-context preflight did not pass")
    if preflight.get("reference_runtime_policy") != "NONE":
        raise VPDRendererAdapterError("preflight reference_runtime_policy must be NONE")
    if preflight.get("explicit_runtime_reference_image_count") != 0:
        raise VPDRendererAdapterError("preflight reference image count must be 0")
    if preflight.get("context_isolation_proven") != "YES" or preflight.get("render_allowed") != "YES":
        raise VPDRendererAdapterError("preflight does not authorize rendering")
    if preflight.get("provider_internal_prompt") != UNAVAILABLE_BY_PROVIDER:
        raise VPDRendererAdapterError("provider-internal prompt must remain unavailable, not guessed")

    budget = _require_dict(freeze.get("output_budget"), "output_budget")
    expected_budget = {
        "formal_outputs": 3,
        "one_per_task": True,
        "hidden_variants": 0,
        "best_of_n": "NO",
        "aesthetic_retries": 0,
        "technical_retry_max_per_task": 1,
    }
    for field, expected in expected_budget.items():
        if budget.get(field) != expected:
            raise VPDRendererAdapterError(f"unexpected output budget {field}: {budget.get(field)!r}")

    tasks = freeze.get("tasks")
    if not isinstance(tasks, list) or [row.get("test_id") for row in tasks if isinstance(row, dict)] != ["T1", "T2", "T3"]:
        raise VPDRendererAdapterError("freeze must contain exactly ordered T1/T2/T3 tasks")
    for task_id in ("T1", "T2", "T3"):
        validate_task(select_task(freeze, task_id))
    return freeze


def validate_task(task: dict[str, Any]) -> dict[str, Any]:
    task_id = _require_str(task.get("test_id"), "test_id")
    if task_id not in {"T1", "T2", "T3"}:
        raise VPDRendererAdapterError(f"unsupported V1 task: {task_id}")
    if task.get("reference_runtime_policy") != "NONE":
        raise VPDRendererAdapterError(f"{task_id}: reference_runtime_policy must be NONE")
    if task.get("explicit_runtime_reference_image_count") != 0:
        raise VPDRendererAdapterError(f"{task_id}: explicit runtime reference count must be 0")
    if task.get("context_isolation_proven") != "YES" or task.get("render_allowed") != "YES":
        raise VPDRendererAdapterError(f"{task_id}: task is not authorized to render")
    if task.get("provider_internal_prompt") != UNAVAILABLE_BY_PROVIDER:
        raise VPDRendererAdapterError(f"{task_id}: provider-internal prompt must not be guessed")

    prompt = _require_str(task.get("final_renderer_payload"), f"{task_id}.final_renderer_payload")
    declared_sha = _require_str(task.get("final_renderer_payload_sha256"), f"{task_id}.final_renderer_payload_sha256")
    actual_sha = text_sha256(prompt)
    if actual_sha != declared_sha:
        raise VPDRendererAdapterError(
            f"{task_id}: frozen payload SHA mismatch: declared={declared_sha} actual={actual_sha}"
        )

    settings = _require_dict(task.get("renderer_settings_if_exposed"), f"{task_id}.renderer_settings_if_exposed")
    if settings.get("size") != ALLOWED_SIZE:
        raise VPDRendererAdapterError(f"{task_id}: frozen size must be {ALLOWED_SIZE}")
    if settings.get("n") != 1:
        raise VPDRendererAdapterError(f"{task_id}: n must be exactly 1")
    if settings.get("referenced_image_ids") is not None:
        raise VPDRendererAdapterError(f"{task_id}: referenced_image_ids must be null")
    if task.get("production_typography") != "NOT_EVALUATED":
        raise VPDRendererAdapterError(f"{task_id}: production typography boundary changed")
    _require_str(task.get("planned_output_filename"), f"{task_id}.planned_output_filename")
    return task


def build_openai_request(
    task: dict[str, Any],
    *,
    model: str = DEFAULT_MODEL,
    quality: str = DEFAULT_QUALITY,
) -> dict[str, Any]:
    validate_task(task)
    if model != DEFAULT_MODEL:
        raise VPDRendererAdapterError(
            f"model drift blocked; expected pinned model {DEFAULT_MODEL}, got {model}"
        )
    if quality not in {"low", "medium", "high"}:
        raise VPDRendererAdapterError("quality must be low, medium, or high")
    request = {
        "model": model,
        "prompt": task["final_renderer_payload"],
        "n": 1,
        "size": ALLOWED_SIZE,
        "quality": quality,
        "output_format": ALLOWED_OUTPUT_FORMAT,
    }
    if request["prompt"] != task["final_renderer_payload"]:
        raise VPDRendererAdapterError("exact prompt binding failed before serialization")
    if text_sha256(request["prompt"]) != task["final_renderer_payload_sha256"]:
        raise VPDRendererAdapterError("request prompt hash diverges from frozen payload")
    return request


def build_pre_request_receipt(
    freeze: dict[str, Any],
    task: dict[str, Any],
    request: dict[str, Any],
) -> dict[str, Any]:
    validate_freeze(freeze)
    validate_task(task)
    if request.get("prompt") != task.get("final_renderer_payload"):
        raise VPDRendererAdapterError("pre-request receipt cannot prove exact prompt binding")
    return {
        "schema_version": "vpd-renderer-adapter-pre-request/v1",
        "adapter_version": ADAPTER_VERSION,
        "created_at": utc_now(),
        "project_id": freeze.get("project_id"),
        "protocol": freeze.get("protocol"),
        "test_id": task["test_id"],
        "task_type": task.get("task_type"),
        "endpoint": OPENAI_IMAGES_ENDPOINT,
        "provider": "OpenAI API",
        "request_body": request,
        "request_body_sha256": canonical_json_sha256(request),
        "frozen_prompt_sha256": task["final_renderer_payload_sha256"],
        "exact_prompt_binding_proven": True,
        "reference_runtime_policy": "NONE",
        "reference_images_attached": 0,
        "provider_internal_prompt": UNAVAILABLE_BY_PROVIDER,
        "authorization_header_persisted": False,
        "status": "FROZEN_BEFORE_NETWORK_IO",
    }


def _atomic_write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as tmp:
        tmp.write(payload)
        temp_path = Path(tmp.name)
    temp_path.replace(path)


def _atomic_write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("wb", dir=path.parent, delete=False) as tmp:
        tmp.write(data)
        temp_path = Path(tmp.name)
    temp_path.replace(path)


def _png_dimensions(data: bytes) -> tuple[int, int]:
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise VPDRendererAdapterError("provider output is not a valid PNG header")
    width, height = struct.unpack(">II", data[16:24])
    return int(width), int(height)


def _default_http_post(url: str, body: bytes, headers: Mapping[str, str], timeout: float) -> HTTPResult:
    req = urllib.request.Request(url, data=body, headers=dict(headers), method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return HTTPResult(
                status=int(response.status),
                headers={key.lower(): value for key, value in response.headers.items()},
                body=response.read(),
            )
    except urllib.error.HTTPError as exc:
        body_bytes = exc.read()
        raise VPDRendererAdapterError(
            f"OpenAI image request failed with HTTP {exc.code}: {body_bytes[:2000].decode('utf-8', 'replace')}"
        ) from exc
    except urllib.error.URLError as exc:
        raise VPDRendererAdapterError(f"OpenAI image request transport failure: {exc.reason}") from exc


def execute_task(
    freeze_path: str | Path,
    task_id: str,
    output_dir: str | Path,
    *,
    api_key: str | None = None,
    model: str = DEFAULT_MODEL,
    quality: str = DEFAULT_QUALITY,
    timeout: float = 180.0,
    http_post: Callable[[str, bytes, Mapping[str, str], float], HTTPResult] = _default_http_post,
    allow_network: bool = False,
) -> dict[str, Any]:
    """Validate, freeze exact request, and optionally execute one V1 task.

    ``allow_network`` is false by default so a dry-run receipt can be inspected
    before any provider call.
    """
    freeze = validate_freeze(load_freeze(freeze_path))
    task = select_task(freeze, task_id)
    request = build_openai_request(task, model=model, quality=quality)
    output_root = Path(output_dir)
    receipt_root = output_root / "receipts"
    pre_path = receipt_root / f"{task_id}_pre_request.json"
    post_path = receipt_root / f"{task_id}_post_render.json"
    failure_path = receipt_root / f"{task_id}_technical_failure.json"
    output_path = output_root / task["planned_output_filename"]

    if output_path.exists() or post_path.exists():
        raise VPDRendererAdapterError(f"{task_id}: refusing to overwrite an existing formal output/receipt")
    pre_receipt = build_pre_request_receipt(freeze, task, request)
    _atomic_write_json(pre_path, pre_receipt)

    if not allow_network:
        return {
            "status": "DRY_RUN_PASS",
            "test_id": task_id,
            "pre_request_receipt": str(pre_path),
            "request_body_sha256": pre_receipt["request_body_sha256"],
            "frozen_prompt_sha256": task["final_renderer_payload_sha256"],
            "exact_prompt_binding_proven": True,
            "reference_images_attached": 0,
        }

    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not isinstance(key, str) or not key.strip():
        failure = {
            "schema_version": "vpd-renderer-adapter-technical-failure/v1",
            "created_at": utc_now(),
            "test_id": task_id,
            "failure_class": "MISSING_OPENAI_API_KEY",
            "network_request_sent": False,
            "pre_request_receipt": str(pre_path),
            "reference_images_attached": 0,
        }
        _atomic_write_json(failure_path, failure)
        raise VPDRendererAdapterError("OPENAI_API_KEY is required for --execute")

    body = json.dumps(request, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {key.strip()}",
        "Content-Type": "application/json",
        "User-Agent": f"vpd-renderer-adapter/{ADAPTER_VERSION}",
    }
    try:
        response = http_post(OPENAI_IMAGES_ENDPOINT, body, headers, timeout)
        if response.status < 200 or response.status >= 300:
            raise VPDRendererAdapterError(f"unexpected provider HTTP status: {response.status}")
        payload = json.loads(response.body.decode("utf-8"))
        if not isinstance(payload, dict):
            raise VPDRendererAdapterError("provider response is not a JSON object")
        data = payload.get("data")
        if not isinstance(data, list) or len(data) != 1 or not isinstance(data[0], dict):
            raise VPDRendererAdapterError("provider response must contain exactly one generated image")
        encoded = data[0].get("b64_json")
        if not isinstance(encoded, str) or not encoded:
            raise VPDRendererAdapterError("provider response did not expose data[0].b64_json")
        image_bytes = base64.b64decode(encoded, validate=True)
        width, height = _png_dimensions(image_bytes)
        if (width, height) != (1024, 1536):
            raise VPDRendererAdapterError(
                f"provider geometry mismatch: expected 1024x1536, got {width}x{height}"
            )
        _atomic_write_bytes(output_path, image_bytes)

        sanitized_response = {key: value for key, value in payload.items() if key != "data"}
        image_meta = {key: value for key, value in data[0].items() if key != "b64_json"}
        post_receipt = {
            "schema_version": "vpd-renderer-adapter-post-render/v1",
            "adapter_version": ADAPTER_VERSION,
            "created_at": utc_now(),
            "test_id": task_id,
            "provider": "OpenAI API",
            "endpoint": OPENAI_IMAGES_ENDPOINT,
            "provider_request_id": response.headers.get("x-request-id", UNAVAILABLE_BY_PROVIDER),
            "requested_model": request["model"],
            "requested_size": request["size"],
            "requested_quality": request["quality"],
            "requested_output_format": request["output_format"],
            "exact_prompt_binding_proven": request["prompt"] == task["final_renderer_payload"],
            "frozen_prompt_sha256": task["final_renderer_payload_sha256"],
            "actual_request_prompt_sha256": text_sha256(request["prompt"]),
            "request_body_sha256": canonical_json_sha256(request),
            "provider_internal_prompt": UNAVAILABLE_BY_PROVIDER,
            "reference_runtime_policy": "NONE",
            "reference_images_attached": 0,
            "output_filename": output_path.name,
            "output_sha256": bytes_sha256(image_bytes),
            "dimensions": f"{width}x{height}",
            "technical_validity": "PASS",
            "production_typography": "NOT_EVALUATED",
            "provider_response_metadata": sanitized_response,
            "provider_image_metadata": image_meta,
            "pre_request_receipt": str(pre_path),
            "status": "FORMAL_OUTPUT_READY_FOR_HUMAN_REVIEW",
        }
        _atomic_write_json(post_path, post_receipt)
        return post_receipt
    except Exception as exc:
        failure = {
            "schema_version": "vpd-renderer-adapter-technical-failure/v1",
            "created_at": utc_now(),
            "test_id": task_id,
            "failure_class": type(exc).__name__,
            "failure_message": str(exc),
            "network_request_sent": True,
            "pre_request_receipt": str(pre_path),
            "reference_images_attached": 0,
        }
        _atomic_write_json(failure_path, failure)
        if isinstance(exc, VPDRendererAdapterError):
            raise
        raise VPDRendererAdapterError(f"provider execution failed: {exc}") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Strict VPD V1 zero-reference renderer adapter")
    parser.add_argument("--freeze", required=True, help="Path to frozen V1 controller payload JSON")
    parser.add_argument("--task", required=True, choices=("T1", "T2", "T3"))
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--quality", default=DEFAULT_QUALITY, choices=("low", "medium", "high"))
    parser.add_argument("--execute", action="store_true", help="Actually call the OpenAI Images API")
    args = parser.parse_args(argv)
    result = execute_task(
        args.freeze,
        args.task,
        args.output_dir,
        quality=args.quality,
        allow_network=args.execute,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
