"""Trace helpers for PHASE 10A generation-chain audit.

This module does not generate images and does not modify preference truth.
It validates private audit receipts and classifies whether Personalized actually
bound approved image assets into a renderer invocation.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any, Iterable


TRACE_VERSION = "1"
_ALLOWED_CONDITIONS = {"baseline", "personalized", "expert_direct"}
_ALLOWED_QUALITY = {"USABLE", "UNUSABLE", "NOT_JUDGED"}
_ALLOWED_GATE = {"PASS", "FAIL", "NOT_RUN"}


class GenerationAuditError(ValueError):
    pass


def canonical_sha256(payload: Any) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _require_obj(value: Any, field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise GenerationAuditError(f"{field} must be an object")
    return value


def _require_str(value: Any, field: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str):
        raise GenerationAuditError(f"{field} must be a string")
    if not allow_empty and not value.strip():
        raise GenerationAuditError(f"{field} may not be empty")
    return value


def classify_reference_binding(
    context_positive_exemplars: Iterable[dict[str, Any]],
    bindings: Iterable[dict[str, Any]],
) -> str:
    """Classify whether selected positive exemplars were actually renderer-bound."""
    selected = {
        str(item.get("asset_id"))
        for item in context_positive_exemplars
        if isinstance(item, dict) and item.get("asset_id")
    }
    rows = [row for row in bindings if isinstance(row, dict)]
    attached: set[str] = set()
    for row in rows:
        asset_id = row.get("asset_id")
        if asset_id not in selected:
            continue
        if row.get("renderer_attachment_present") is not True:
            continue
        asset_sha = row.get("asset_sha256")
        attachment_sha = row.get("renderer_attachment_sha256")
        if not isinstance(asset_sha, str) or not isinstance(attachment_sha, str):
            continue
        if asset_sha != attachment_sha:
            continue
        if not row.get("resolved_path_or_private_ref"):
            continue
        attached.add(str(asset_id))

    if not selected:
        return "UNPROVEN_BINDING"
    if not rows:
        return "TEXT_ONLY_PERSONALIZATION"
    if not attached:
        any_claim = any(row.get("renderer_attachment_present") is True for row in rows)
        return "UNPROVEN_BINDING" if any_claim else "TEXT_ONLY_PERSONALIZATION"
    if attached == selected:
        return "MULTIMODAL_BOUND"
    return "PARTIAL_MULTIMODAL_BOUND"


def validate_trace(trace: Any) -> dict[str, Any]:
    r = _require_obj(trace, "trace")
    required = {
        "trace_version",
        "trace_id",
        "task_id",
        "condition",
        "task_text",
        "route",
        "skills_read",
        "mandatory_files_read",
        "compiler",
        "context",
        "reference_bindings",
        "renderer",
        "output",
        "quality_gate",
    }
    missing = sorted(required - set(r))
    if missing:
        raise GenerationAuditError("missing fields: " + ", ".join(missing))
    if r["trace_version"] != TRACE_VERSION:
        raise GenerationAuditError("unsupported trace_version")
    _require_str(r["trace_id"], "trace_id")
    _require_str(r["task_id"], "task_id")
    _require_str(r["task_text"], "task_text")
    if r["condition"] not in _ALLOWED_CONDITIONS:
        raise GenerationAuditError("condition is invalid")

    route = _require_obj(r["route"], "route")
    _require_str(route.get("route_id"), "route.route_id")
    _require_str(route.get("evidence"), "route.evidence")

    for field in ("skills_read", "mandatory_files_read"):
        value = r[field]
        if not isinstance(value, list) or not value:
            raise GenerationAuditError(f"{field} must be a non-empty list")
        for index, row in enumerate(value):
            row = _require_obj(row, f"{field}[{index}]")
            _require_str(row.get("path"), f"{field}[{index}].path")
            _require_str(row.get("git_blob_sha"), f"{field}[{index}].git_blob_sha")

    compiler = _require_obj(r["compiler"], "compiler")
    _require_str(compiler.get("name"), "compiler.name")
    _require_str(compiler.get("output_text"), "compiler.output_text")

    context = _require_obj(r["context"], "context")
    for field in ("positive_exemplars", "negative_exemplars", "source_event_ids"):
        if not isinstance(context.get(field), list):
            raise GenerationAuditError(f"context.{field} must be a list")

    if not isinstance(r["reference_bindings"], list):
        raise GenerationAuditError("reference_bindings must be a list")

    renderer = _require_obj(r["renderer"], "renderer")
    _require_str(renderer.get("tool"), "renderer.tool")
    _require_str(renderer.get("model"), "renderer.model")
    _require_str(renderer.get("ratio"), "renderer.ratio")
    _require_str(renderer.get("final_prompt"), "renderer.final_prompt")
    if not isinstance(renderer.get("parameters"), dict):
        raise GenerationAuditError("renderer.parameters must be an object")

    output = _require_obj(r["output"], "output")
    for field in ("sample_id", "asset_id", "sha256"):
        _require_str(output.get(field), f"output.{field}")

    quality = _require_obj(r["quality_gate"], "quality_gate")
    if quality.get("realism_status") not in _ALLOWED_GATE:
        raise GenerationAuditError("quality_gate.realism_status is invalid")
    if quality.get("design_status") not in _ALLOWED_GATE:
        raise GenerationAuditError("quality_gate.design_status is invalid")
    if quality.get("absolute_quality") not in _ALLOWED_QUALITY:
        raise GenerationAuditError("quality_gate.absolute_quality is invalid")
    if not isinstance(quality.get("reasons"), list):
        raise GenerationAuditError("quality_gate.reasons must be a list")

    return r


def trace_summary(trace: dict[str, Any]) -> dict[str, Any]:
    r = validate_trace(trace)
    binding = classify_reference_binding(
        r["context"].get("positive_exemplars", []),
        r.get("reference_bindings", []),
    )
    return {
        "trace_id": r["trace_id"],
        "task_id": r["task_id"],
        "condition": r["condition"],
        "route_id": r["route"]["route_id"],
        "binding_classification": binding,
        "absolute_quality": r["quality_gate"]["absolute_quality"],
        "realism_status": r["quality_gate"]["realism_status"],
        "design_status": r["quality_gate"]["design_status"],
        "trace_sha256": canonical_sha256(r),
    }


def summarize_absolute_quality(traces: Iterable[dict[str, Any]]) -> dict[str, Any]:
    rows = [validate_trace(row) for row in traces]
    counts: dict[str, dict[str, int]] = {
        condition: {"USABLE": 0, "UNUSABLE": 0, "NOT_JUDGED": 0}
        for condition in sorted(_ALLOWED_CONDITIONS)
    }
    for row in rows:
        counts[row["condition"]][row["quality_gate"]["absolute_quality"]] += 1
    return {"trace_count": len(rows), "by_condition": counts}
