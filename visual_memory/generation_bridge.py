"""Minimal generation bridge and observability contract for G2.

The bridge deliberately does not call a renderer.  It proves what a caller is
allowed to send, what a provider actually exposed, and whether an output may
advance to a diagnostic experiment.  Personal data remains in the private
store; callers persist request/receipt objects outside Git.
"""
from __future__ import annotations

import hashlib
import re
import struct
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .store import VisualMemoryStore, sha256_file


BRIDGE_VERSION = "1"
UNAVAILABLE_BY_PROVIDER = "UNAVAILABLE_BY_PROVIDER"

PROMPT_INVARIANTS: dict[str, str] = {
    "PRODUCT_REALISM_PRIORITY": "Product realism outranks decoration.",
    "NO_SYNTHETIC_FOOD_MATERIAL": "No plastic, waxy, or rubber food material.",
    "NATURAL_INGREDIENT_DISTRIBUTION": "Ingredients have natural irregularity and distribution, never copied repetition.",
    "CONTROLLED_OIL_GLOSS": "Oil and specular gloss are controlled and physically believable.",
    "BELIEVABLE_CONTACT_SHADOW": "Products and vessels have believable physical contact and contact shadows.",
    "HEAT_COHERENT_STEAM": "Steam or smoke originates from and remains related to an actual heat source.",
    "PRODUCT_DRIVEN_COMPOSITION": "Product shape, structure, material, vessel, or preparation motion drives the composition.",
    "NO_DEFAULT_CULTURAL_SHORTCUT": "Do not default to Chinese ink, brush strokes, or red-seal shortcuts.",
    "NO_GENERIC_RESTAURANT_TEMPLATE": "Do not use a generic repeated restaurant template or a color-swap template.",
}

_FIELD_PROVENANCE = {
    "tool_exposed",
    "provider_exposed",
    "output_metadata",
    "unavailable_by_provider",
}
_PIXEL_CHECKS = {
    "food_material_realism",
    "structure_anatomy_if_applicable",
    "natural_irregularity",
    "oil_specular_realism",
    "physical_contact_shadow",
    "heat_steam_coherence",
    "generic_template_collapse",
    "obvious_ai_material",
    "task_compliance",
}


class GenerationBridgeError(ValueError):
    """Raised before rendering or experiment admission when the contract fails."""


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def text_sha256(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def append_mandatory_prompt_invariants(
    compiler_output: str,
    *,
    invariant_codes: Iterable[str] = PROMPT_INVARIANTS,
) -> str:
    """Append only the G1-proven existing invariants in a machine-checkable form."""
    if not isinstance(compiler_output, str) or not compiler_output.strip():
        raise GenerationBridgeError("compiler_output may not be empty")
    codes = list(dict.fromkeys(invariant_codes))
    unknown = sorted(set(codes) - set(PROMPT_INVARIANTS))
    if unknown:
        raise GenerationBridgeError("unknown prompt invariant codes: " + ", ".join(unknown))
    block = ["Mandatory renderer invariants:"]
    block.extend(f"[{code}] {PROMPT_INVARIANTS[code]}" for code in codes)
    return compiler_output.rstrip() + "\n\n" + "\n".join(block)


def validate_prompt_preservation(
    *,
    task_brief: str,
    compiler_input: dict[str, Any],
    compiler_output: str,
    final_renderer_prompt: str,
    invariant_codes: Iterable[str] = PROMPT_INVARIANTS,
) -> dict[str, Any]:
    """Return a prompt receipt or block before rendering on any missing invariant."""
    if not isinstance(task_brief, str) or not task_brief.strip():
        raise GenerationBridgeError("task_brief may not be empty")
    if not isinstance(compiler_input, dict):
        raise GenerationBridgeError("compiler_input must be an object")
    if not isinstance(compiler_output, str) or not compiler_output.strip():
        raise GenerationBridgeError("compiler_output may not be empty")
    if not isinstance(final_renderer_prompt, str) or not final_renderer_prompt.strip():
        raise GenerationBridgeError("final_renderer_prompt may not be empty")
    if compiler_output not in final_renderer_prompt:
        raise GenerationBridgeError("compiler output was not preserved in final renderer prompt")
    if task_brief not in compiler_output:
        raise GenerationBridgeError("task brief was not preserved in compiler output")

    codes = list(dict.fromkeys(invariant_codes))
    unknown = sorted(set(codes) - set(PROMPT_INVARIANTS))
    if unknown:
        raise GenerationBridgeError("unknown prompt invariant codes: " + ", ".join(unknown))
    preserved = {
        code: f"[{code}] {PROMPT_INVARIANTS[code]}" in final_renderer_prompt
        for code in codes
    }
    missing = [code for code, present in preserved.items() if not present]
    if missing:
        raise GenerationBridgeError(
            "render blocked; missing mandatory prompt invariants: " + ", ".join(missing)
        )
    return {
        "task_brief": task_brief,
        "compiler_input": compiler_input,
        "compiler_output": compiler_output,
        "final_renderer_prompt": final_renderer_prompt,
        "prompt_sha256": text_sha256(final_renderer_prompt),
        "mandatory_invariant_codes": codes,
        "invariants_preserved": preserved,
        "all_invariants_preserved": True,
        "render_allowed": True,
    }


def _context_rows(context_pack: dict[str, Any], key: str) -> list[dict[str, Any]]:
    if not isinstance(context_pack, dict):
        raise GenerationBridgeError("context_pack must be an object")
    value = context_pack.get(key)
    if not isinstance(value, list):
        raise GenerationBridgeError(f"context_pack.{key} must be a list")
    if any(not isinstance(row, dict) for row in value):
        raise GenerationBridgeError(f"context_pack.{key} rows must be objects")
    return value


def prepare_direct_reference_attachments(
    store: VisualMemoryStore,
    context_pack: dict[str, Any],
) -> dict[str, Any]:
    """Resolve each positive canonical asset to one independent attachment.

    Negative exemplars remain upstream evidence only.  This function never
    builds a contact sheet, montage, crop, thumbnail, or mixed-polarity image.
    """
    positive = _context_rows(context_pack, "positive_exemplars")
    negative = _context_rows(context_pack, "negative_exemplars")
    negative_assets = {str(row.get("asset_id")) for row in negative if row.get("asset_id")}
    negative_samples = {str(row.get("sample_id")) for row in negative if row.get("sample_id")}
    attachments: list[dict[str, Any]] = []
    seen_assets: set[str] = set()

    for index, row in enumerate(positive):
        sample_id = str(row.get("sample_id") or "")
        asset_id = str(row.get("asset_id") or "")
        if not sample_id or not asset_id:
            raise GenerationBridgeError("positive exemplar requires sample_id and asset_id")
        if sample_id in negative_samples or asset_id in negative_assets:
            raise GenerationBridgeError("a rejected exemplar cannot enter the positive attachment set")
        if asset_id in seen_assets:
            raise GenerationBridgeError(f"duplicate positive attachment asset: {asset_id}")
        sample = store.read_sample(sample_id)
        asset = store.read_asset(asset_id)
        if sample is None or asset is None:
            raise GenerationBridgeError(f"canonical positive record is missing: {sample_id}/{asset_id}")
        if sample.get("primary_asset_id") != asset_id or asset.get("sample_id") != sample_id:
            raise GenerationBridgeError(f"sample/asset link mismatch: {sample_id}/{asset_id}")
        if sample.get("dataset_role") not in {"discovery", "production"}:
            raise GenerationBridgeError("only discovery/production positives may become attachments")
        resolved = store.resolve_asset(asset_id)
        if resolved is None:
            raise GenerationBridgeError(f"positive asset does not resolve: {asset_id}")
        digest = sha256_file(resolved)
        if digest != asset.get("sha256"):
            raise GenerationBridgeError(f"positive attachment hash mismatch: {asset_id}")
        attachments.append(
            {
                "attachment_index": index,
                "sample_id": sample_id,
                "asset_id": asset_id,
                "canonical_sha256": digest,
                "resolved_file": str(resolved),
                "transport": "CANONICAL_DIRECT",
                "source_asset_count": 1,
                "source_sha256": digest,
                "attachment_sha256": digest,
                "attachment_identity": f"canonical-sha256:{digest.removeprefix('sha256:')}",
                "conversion": None,
                "included_in_renderer_invocation": True,
            }
        )
        seen_assets.add(asset_id)

    negative_behavior = []
    for row in negative:
        negative_behavior.append(
            {
                "sample_id": row.get("sample_id"),
                "asset_id": row.get("asset_id"),
                "role": "UPSTREAM_NEGATIVE_EVIDENCE_ONLY",
                "included_in_renderer_invocation": False,
                "negative_image_conditioning_supported": False,
            }
        )
    return {
        "positive_attachments": attachments,
        "negative_reference_behavior": negative_behavior,
        "renderer_attachment_paths": [row["resolved_file"] for row in attachments],
        "binding_classification": classify_direct_reference_binding(positive, attachments),
    }


def classify_direct_reference_binding(
    positive_exemplars: Iterable[dict[str, Any]],
    attachments: Iterable[dict[str, Any]],
) -> str:
    """Require one identity-preserving file per selected positive asset."""
    selected = {
        str(row.get("asset_id")): str(row.get("sample_id"))
        for row in positive_exemplars
        if isinstance(row, dict) and row.get("asset_id") and row.get("sample_id")
    }
    if not selected:
        return "UNPROVEN_BINDING"
    rows = [row for row in attachments if isinstance(row, dict)]
    if not rows:
        return "TEXT_ONLY_PERSONALIZATION"
    bound: set[str] = set()
    for row in rows:
        asset_id = str(row.get("asset_id") or "")
        if asset_id not in selected:
            continue
        if row.get("transport") not in {"CANONICAL_DIRECT", "SINGLE_IMAGE_DERIVATIVE"}:
            continue
        if row.get("source_asset_count") != 1:
            continue
        if row.get("included_in_renderer_invocation") is not True:
            continue
        source_sha = row.get("source_sha256")
        canonical_sha = row.get("canonical_sha256")
        attachment_sha = row.get("attachment_sha256")
        if not all(isinstance(value, str) and value.startswith("sha256:") for value in (
            source_sha,
            canonical_sha,
            attachment_sha,
        )):
            continue
        if source_sha != canonical_sha:
            continue
        if row.get("transport") == "CANONICAL_DIRECT" and attachment_sha != canonical_sha:
            continue
        if row.get("transport") == "SINGLE_IMAGE_DERIVATIVE" and not isinstance(
            row.get("conversion"), dict
        ):
            continue
        bound.add(asset_id)
    if not bound:
        return "UNPROVEN_BINDING"
    if bound == set(selected):
        return "MULTIMODAL_BOUND"
    return "PARTIAL_MULTIMODAL_BOUND"


def validate_renderer_request(request: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise GenerationBridgeError("renderer request must be an object")
    if request.get("bridge_version") != BRIDGE_VERSION:
        raise GenerationBridgeError("unsupported bridge_version")
    prompt = request.get("prompt_contract")
    if not isinstance(prompt, dict) or prompt.get("render_allowed") is not True:
        raise GenerationBridgeError("prompt preservation gate did not pass")
    final_prompt = prompt.get("final_renderer_prompt")
    if not isinstance(final_prompt, str) or text_sha256(final_prompt) != prompt.get("prompt_sha256"):
        raise GenerationBridgeError("prompt SHA-256 mismatch")
    context = request.get("context_pack")
    refs = request.get("reference_transport")
    if not isinstance(context, dict) or not isinstance(refs, dict):
        raise GenerationBridgeError("context/reference transport is missing")
    classification = classify_direct_reference_binding(
        _context_rows(context, "positive_exemplars"),
        refs.get("positive_attachments", []),
    )
    if classification != "MULTIMODAL_BOUND":
        raise GenerationBridgeError(f"render blocked; reference binding is {classification}")
    if any(row.get("included_in_renderer_invocation") for row in refs.get("negative_reference_behavior", [])):
        raise GenerationBridgeError("negative reference entered positive renderer conditioning")
    tool_name = request.get("tool_name")
    if not isinstance(tool_name, str) or not tool_name.strip():
        raise GenerationBridgeError("tool_name may not be empty")
    ratio = request.get("ratio_request")
    if not isinstance(ratio, str) or not ratio.strip():
        raise GenerationBridgeError("ratio_request may not be empty")
    return request


def build_renderer_request(
    *,
    store: VisualMemoryStore,
    task_id: str,
    task_brief: str,
    compiler_input: dict[str, Any],
    compiler_output: str,
    final_renderer_prompt: str,
    context_pack: dict[str, Any],
    tool_name: str,
    ratio_request: str,
) -> dict[str, Any]:
    prompt_contract = validate_prompt_preservation(
        task_brief=task_brief,
        compiler_input=compiler_input,
        compiler_output=compiler_output,
        final_renderer_prompt=final_renderer_prompt,
    )
    references = prepare_direct_reference_attachments(store, context_pack)
    request = {
        "bridge_version": BRIDGE_VERSION,
        "task_id": task_id,
        "created_at": utc_now(),
        "tool_name": tool_name,
        "ratio_request": ratio_request,
        "prompt_contract": prompt_contract,
        "context_pack": context_pack,
        "reference_transport": references,
        "actual_tool_arguments": {
            "prompt": final_renderer_prompt,
            "referenced_image_paths": references["renderer_attachment_paths"],
        },
    }
    return validate_renderer_request(request)


def provider_field(
    value: Any,
    *,
    provenance: str,
    reason: str | None = None,
) -> dict[str, Any]:
    """Record the strongest public value without permitting guessed fields."""
    if provenance not in _FIELD_PROVENANCE:
        raise GenerationBridgeError(f"invalid or guessed provider-field provenance: {provenance}")
    if provenance == "unavailable_by_provider":
        if value != UNAVAILABLE_BY_PROVIDER:
            raise GenerationBridgeError("unavailable provider field must use UNAVAILABLE_BY_PROVIDER")
        if not isinstance(reason, str) or not reason.strip():
            raise GenerationBridgeError("unavailable provider field requires a reason")
    elif value == UNAVAILABLE_BY_PROVIDER:
        raise GenerationBridgeError("UNAVAILABLE_BY_PROVIDER requires unavailable provenance")
    if value is None:
        raise GenerationBridgeError("provider field value may not be null")
    return {"value": value, "provenance": provenance, "reason": reason}


def build_renderer_receipt(
    request: dict[str, Any],
    *,
    output_path: str | Path,
    provider_name: dict[str, Any],
    declared_model: dict[str, Any],
    declared_model_version: dict[str, Any],
    software_agent: dict[str, Any],
    quality: dict[str, Any],
    seed: dict[str, Any],
    size: dict[str, Any],
    invocation_evidence: dict[str, Any],
    actual_renderer_attachments: list[dict[str, Any]],
    timestamp: str | None = None,
) -> dict[str, Any]:
    validate_renderer_request(request)
    for name, field in {
        "provider_name": provider_name,
        "declared_model": declared_model,
        "declared_model_version": declared_model_version,
        "software_agent": software_agent,
        "quality": quality,
        "seed": seed,
        "size": size,
    }.items():
        if not isinstance(field, dict):
            raise GenerationBridgeError(f"{name} must be a provider-field receipt")
        provider_field(field.get("value"), provenance=field.get("provenance"), reason=field.get("reason"))
    if not isinstance(invocation_evidence, dict):
        raise GenerationBridgeError("invocation_evidence must be an object")
    for key in ("call_id", "status", "timestamp", "prompt_sha256"):
        if not isinstance(invocation_evidence.get(key), str) or not invocation_evidence[key].strip():
            raise GenerationBridgeError(f"invocation_evidence.{key} may not be empty")
    if invocation_evidence["status"] != "completed":
        raise GenerationBridgeError("renderer invocation did not complete")
    if invocation_evidence["prompt_sha256"] != request["prompt_contract"]["prompt_sha256"]:
        raise GenerationBridgeError("renderer invocation prompt identity mismatch")
    if not isinstance(actual_renderer_attachments, list):
        raise GenerationBridgeError("actual_renderer_attachments must be a list")
    expected_attachments = request["reference_transport"]["positive_attachments"]
    identity_keys = (
        "sample_id",
        "asset_id",
        "canonical_sha256",
        "resolved_file",
        "attachment_sha256",
        "attachment_identity",
    )
    expected_identity = [
        {key: row.get(key) for key in identity_keys}
        for row in expected_attachments
    ]
    actual_identity = [
        {key: row.get(key) for key in identity_keys}
        for row in actual_renderer_attachments
    ]
    if actual_identity != expected_identity:
        raise GenerationBridgeError("actual renderer attachment identity mismatch")
    if any(row.get("included_in_renderer_invocation") is not True for row in actual_renderer_attachments):
        raise GenerationBridgeError("renderer attachment was not proven present in invocation")
    output = Path(output_path).expanduser().resolve()
    if not output.is_file():
        raise GenerationBridgeError(f"renderer output does not exist: {output}")
    return {
        "bridge_version": BRIDGE_VERSION,
        "receipt_status": "PASS_WITH_EXPOSED_FIELDS",
        "timestamp": timestamp or utc_now(),
        "tool_name": request["tool_name"],
        "provider_name": provider_name,
        "declared_model": declared_model,
        "declared_model_version": declared_model_version,
        "software_agent": software_agent,
        "ratio_request": request["ratio_request"],
        "quality": quality,
        "seed": seed,
        "size": size,
        "parameters": {
            "ratio_request": request["ratio_request"],
            "quality": quality,
            "seed": seed,
            "size": size,
        },
        "prompt_sha256": request["prompt_contract"]["prompt_sha256"],
        "invocation_evidence": invocation_evidence,
        "actual_renderer_attachments": actual_renderer_attachments,
        "output_path": str(output),
        "output_sha256": sha256_file(output),
    }


def _jpeg_dimensions(data: bytes) -> tuple[int, int] | None:
    index = 2
    while index + 9 <= len(data):
        if data[index] != 0xFF:
            index += 1
            continue
        while index < len(data) and data[index] == 0xFF:
            index += 1
        if index >= len(data):
            break
        marker = data[index]
        index += 1
        if marker in {0xD8, 0xD9}:
            continue
        if index + 2 > len(data):
            break
        length = struct.unpack(">H", data[index:index + 2])[0]
        if length < 2 or index + length > len(data):
            break
        if marker in {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}:
            height, width = struct.unpack(">HH", data[index + 3:index + 7])
            return width, height
        index += length
    return None


def inspect_image_file(path: str | Path) -> dict[str, Any]:
    source = Path(path).expanduser().resolve()
    if not source.is_file():
        raise GenerationBridgeError(f"image file does not exist: {source}")
    data = source.read_bytes()
    if not data:
        raise GenerationBridgeError("image file is empty")
    actual_format: str
    mime_type: str
    dimensions: tuple[int, int] | None
    valid_extensions: set[str]
    if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24:
        actual_format, mime_type = "PNG", "image/png"
        dimensions = struct.unpack(">II", data[16:24])
        valid_extensions = {".png"}
    elif data.startswith(b"\xff\xd8\xff"):
        actual_format, mime_type = "JPEG", "image/jpeg"
        dimensions = _jpeg_dimensions(data)
        valid_extensions = {".jpg", ".jpeg"}
    elif data.startswith((b"GIF87a", b"GIF89a")) and len(data) >= 10:
        actual_format, mime_type = "GIF", "image/gif"
        dimensions = struct.unpack("<HH", data[6:10])
        valid_extensions = {".gif"}
    elif len(data) >= 12 and data[4:8] == b"ftyp" and data[8:12] in {
        b"heic", b"heix", b"hevc", b"hevx", b"mif1", b"msf1", b"avif"
    }:
        brand = data[8:12]
        actual_format = "AVIF" if brand == b"avif" else "HEIF"
        mime_type = "image/avif" if brand == b"avif" else "image/heif"
        dimensions = None
        valid_extensions = {".avif"} if brand == b"avif" else {".heif", ".heic"}
    elif data.startswith(b"RIFF") and len(data) >= 16 and data[8:12] == b"WEBP":
        actual_format, mime_type = "WEBP", "image/webp"
        dimensions = None
        valid_extensions = {".webp"}
    else:
        raise GenerationBridgeError("unsupported or corrupt image bytes")
    extension = source.suffix.lower()
    if extension not in valid_extensions:
        raise GenerationBridgeError(
            f"extension/actual MIME mismatch: {extension or '<none>'} vs {mime_type}"
        )
    if dimensions is None:
        raise GenerationBridgeError(f"dimensions unavailable for {actual_format}; machine gate cannot pass")
    width, height = dimensions
    if width <= 0 or height <= 0:
        raise GenerationBridgeError("invalid image dimensions")
    return {
        "file_readable": True,
        "actual_format": actual_format,
        "actual_mime_type": mime_type,
        "extension_matches_actual_format": True,
        "actual_width": width,
        "actual_height": height,
        "output_sha256": sha256_file(source),
        "corruption_detected": False,
    }


def machine_integrity_gate(
    path: str | Path,
    *,
    expected_ratio: str,
    ratio_tolerance: float = 0.02,
) -> dict[str, Any]:
    receipt = inspect_image_file(path)
    match = re.search(r"(\d+(?:\.\d+)?)\s*:\s*(\d+(?:\.\d+)?)", expected_ratio)
    if not match:
        raise GenerationBridgeError(f"expected ratio is invalid: {expected_ratio}")
    expected = float(match.group(1)) / float(match.group(2))
    actual = receipt["actual_width"] / receipt["actual_height"]
    relative_error = abs(actual - expected) / expected
    if relative_error > ratio_tolerance:
        raise GenerationBridgeError(
            f"actual ratio {actual:.6f} differs from requested {expected:.6f}"
        )
    return {
        **receipt,
        "expected_ratio": expected_ratio,
        "actual_ratio": actual,
        "ratio_relative_error": relative_error,
        "ratio_pass": True,
        "machine_integrity_status": "PASS",
        "executed": True,
    }


def build_pixel_review_receipt(
    *,
    output_sha256: str,
    reviewer_kind: str,
    transport: str,
    evidence_ref: str,
    status: str,
    checks: dict[str, str],
    reviewed_at: str | None = None,
) -> dict[str, Any]:
    if reviewer_kind not in {"chatgpt_pixel_reviewer", "human_pixel_reviewer"}:
        raise GenerationBridgeError("real pixel visual gate requires an independent pixel reviewer")
    if transport != "GOOGLE_DRIVE_RAW_PIXEL_DOWNLOAD":
        raise GenerationBridgeError("real pixel visual gate requires the approved Google Drive transport")
    if status not in {"PASS_FOR_DIAGNOSTIC", "REJECTED_BELOW_FLOOR"}:
        raise GenerationBridgeError("invalid real pixel visual gate status")
    if not isinstance(evidence_ref, str) or not evidence_ref.strip():
        raise GenerationBridgeError("pixel review requires an evidence reference")
    if set(checks) != _PIXEL_CHECKS:
        missing = sorted(_PIXEL_CHECKS - set(checks))
        extra = sorted(set(checks) - _PIXEL_CHECKS)
        raise GenerationBridgeError(f"pixel review checks mismatch; missing={missing}, extra={extra}")
    allowed_results = {"PASS", "FAIL", "NOT_APPLICABLE"}
    if any(value not in allowed_results for value in checks.values()):
        raise GenerationBridgeError("invalid pixel review check result")
    if status == "PASS_FOR_DIAGNOSTIC" and any(value == "FAIL" for value in checks.values()):
        raise GenerationBridgeError("a failing visual check cannot pass for diagnostic")
    if status == "REJECTED_BELOW_FLOOR" and not any(value == "FAIL" for value in checks.values()):
        raise GenerationBridgeError("a rejection requires at least one failed visual check")
    return {
        "executed": True,
        "reviewed_at": reviewed_at or utc_now(),
        "reviewer_kind": reviewer_kind,
        "transport": transport,
        "evidence_ref": evidence_ref,
        "output_sha256": output_sha256,
        "checks": checks,
        "real_pixel_visual_gate_status": status,
    }


def diagnostic_eligibility(
    machine_gate: dict[str, Any] | None,
    pixel_review: dict[str, Any] | None,
) -> dict[str, Any]:
    if not isinstance(machine_gate, dict) or machine_gate.get("executed") is not True:
        return {"eligible": False, "status": "BLOCKED_MACHINE_INTEGRITY_NOT_EXECUTED"}
    if machine_gate.get("machine_integrity_status") != "PASS":
        return {"eligible": False, "status": "BLOCKED_MACHINE_INTEGRITY_FAILED"}
    if not isinstance(pixel_review, dict) or pixel_review.get("executed") is not True:
        return {"eligible": False, "status": "BLOCKED_REAL_PIXEL_GATE_NOT_EXECUTED"}
    if pixel_review.get("output_sha256") != machine_gate.get("output_sha256"):
        return {"eligible": False, "status": "BLOCKED_REVIEW_OUTPUT_IDENTITY_MISMATCH"}
    if pixel_review.get("real_pixel_visual_gate_status") != "PASS_FOR_DIAGNOSTIC":
        return {"eligible": False, "status": "REJECTED_BELOW_FLOOR"}
    return {
        "eligible": True,
        "status": "ELIGIBLE_FOR_DIAGNOSTIC_ONLY",
        "production_quality_proven": False,
    }
