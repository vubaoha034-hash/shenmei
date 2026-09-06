"""Forward-only validation for the VPD photo -> Figma -> export route.

This module validates structural correctness and provenance.  It deliberately
does not assign aesthetic scores or attempt to render, edit, or export media.
"""
from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any


PHOTO_ONLY_CONTRACT_ID = "PHOTO_ONLY_RENDER_CONTRACT_V1"
PHOTO_ONLY_STAGE = "PHOTO_ONLY_RENDER"
FIGMA_CONTRACT_ID = "FIGMA_COMPOSITION_CONTRACT_V1"
GATE_POLICY_ID = "COMMERCIAL_DESIGN_GATE_POLICY_V1"
FORMAL_CLASSIFICATION = "FORMAL_COMMERCIAL_OUTPUT"
UNKNOWN = "UNKNOWN"


class PipelineContractError(ValueError):
    """Raised when a staged VPD artifact violates a machine-auditable rule."""


def _is_mapping(value: Any) -> bool:
    return isinstance(value, Mapping)


def _unknown(value: Any) -> bool:
    return value is None or value == "" or value == UNKNOWN


def _walk_keys(value: Any) -> Iterable[str]:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            yield str(key)
            yield from _walk_keys(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from _walk_keys(nested)


def photo_only_payload_errors(
    payload: Mapping[str, Any], contract: Mapping[str, Any]
) -> list[str]:
    """Return deterministic correctness errors for a photo-only payload."""
    errors: list[str] = []
    payload_contract = contract.get("payload_contract", {})
    required = payload_contract.get("required_top_level_fields", [])
    for field in required:
        if field not in payload:
            errors.append(f"MISSING_TOP_LEVEL_FIELD:{field}")

    if payload.get("contract_id") != PHOTO_ONLY_CONTRACT_ID:
        errors.append("PHOTO_ONLY_CONTRACT_ID_MISMATCH")
    if payload.get("contract_version") != contract.get("contract_version"):
        errors.append("PHOTO_ONLY_CONTRACT_VERSION_MISMATCH")
    if payload.get("stage") != PHOTO_ONLY_STAGE:
        errors.append("PHOTO_ONLY_STAGE_MISMATCH")
    if payload.get("render_route") != contract.get("execution_route", {}).get(
        "allowed_render_route"
    ):
        errors.append("PHOTO_ONLY_RENDER_ROUTE_VIOLATION")
    if payload.get("chatgpt_only") is not True:
        errors.append("PHOTO_ONLY_CHATGPT_ONLY_REQUIRED")
    if payload.get("final_typography_in_render") is not False:
        errors.append("PHOTO_ONLY_RENDER_CONTAINS_FINAL_TYPOGRAPHY")

    photography = payload.get("photography_required")
    if not _is_mapping(photography):
        errors.append("PHOTO_ONLY_PHOTOGRAPHY_REQUIRED_NOT_OBJECT")
    else:
        for field in payload_contract.get("photography_required_fields", []):
            if field not in photography or _unknown(photography[field]):
                errors.append(f"PHOTO_ONLY_PHOTOGRAPHY_FIELD_INCOMPLETE:{field}")

    safe_space = payload.get("type_safe_space_requirements")
    if not _is_mapping(safe_space):
        errors.append("PHOTO_ONLY_TYPE_SAFE_SPACE_NOT_OBJECT")
    elif safe_space.get("photographic_space_only") is not True:
        errors.append("PHOTO_ONLY_TYPE_SAFE_SPACE_MUST_BE_PHOTOGRAPHIC")

    prohibited_fields = set(
        payload_contract.get("graphic_text_prohibited_fields", [])
    )
    declared = payload.get("graphic_text_prohibited_in_render")
    if not _is_mapping(declared):
        errors.append("PHOTO_ONLY_GRAPHIC_TEXT_PROHIBITIONS_NOT_OBJECT")
    else:
        for field in sorted(prohibited_fields):
            if declared.get(field) is not True:
                errors.append(f"PHOTO_ONLY_GRAPHIC_TEXT_NOT_PROHIBITED:{field}")

    all_keys = set(_walk_keys(payload))
    # The declaration object is the one allowed location for these names.
    payload_without_declaration = dict(payload)
    payload_without_declaration.pop("graphic_text_prohibited_in_render", None)
    content_keys = set(_walk_keys(payload_without_declaration))
    for field in sorted(prohibited_fields & content_keys):
        errors.append(f"PHOTO_ONLY_RENDER_CONTAINS_GRAPHIC_TEXT_FIELD:{field}")

    required_shortcuts = set(contract.get("prohibited_composition_shortcuts", []))
    declared_shortcuts = payload.get("prohibited_composition_shortcuts")
    if not isinstance(declared_shortcuts, list):
        errors.append("PHOTO_ONLY_SHORTCUT_EXCLUSIONS_NOT_LIST")
    else:
        missing = sorted(required_shortcuts - set(declared_shortcuts))
        errors.extend(f"PHOTO_ONLY_SHORTCUT_NOT_EXCLUDED:{item}" for item in missing)

    if not all_keys:
        errors.append("PHOTO_ONLY_PAYLOAD_EMPTY")
    return errors


def require_photo_only_payload(
    payload: Mapping[str, Any], contract: Mapping[str, Any]
) -> Mapping[str, Any]:
    errors = photo_only_payload_errors(payload, contract)
    if errors:
        raise PipelineContractError("; ".join(errors))
    return payload


def _editable_node_errors(nodes: Any, label: str) -> list[str]:
    if not isinstance(nodes, list) or not nodes:
        return [f"{label}_MISSING"]
    errors: list[str] = []
    for index, node in enumerate(nodes):
        if not _is_mapping(node):
            errors.append(f"{label}_NODE_NOT_OBJECT:{index}")
            continue
        if node.get("editable") is not True:
            errors.append(f"{label}_NODE_NOT_EDITABLE:{index}")
        if node.get("node_type") not in {"TEXT", "VECTOR"}:
            errors.append(f"{label}_NODE_TYPE_INVALID:{index}")
        for field in ("node_id", "exact_copy", "x", "y", "width", "height"):
            if _unknown(node.get(field)):
                errors.append(f"{label}_NODE_FIELD_UNKNOWN:{index}:{field}")
    return errors


def commercial_receipt_errors(receipt: Mapping[str, Any]) -> list[str]:
    """Validate the photo -> Figma -> export provenance and formal gate chain."""
    errors: list[str] = []
    required_top = (
        "photo_render_receipt",
        "figma_composition_receipt",
        "final_export_receipt",
        "gates",
        "forward_only_policy",
    )
    for field in required_top:
        if field not in receipt:
            errors.append(f"COMMERCIAL_RECEIPT_MISSING:{field}")

    photo = receipt.get("photo_render_receipt")
    figma = receipt.get("figma_composition_receipt")
    export = receipt.get("final_export_receipt")
    gates = receipt.get("gates")

    if not _is_mapping(photo):
        errors.append("PHOTO_RENDER_RECEIPT_MISSING_OR_INVALID")
    else:
        if photo.get("render_route") != "CHATGPT_PRODUCT_UI":
            errors.append("PHOTO_RENDER_ROUTE_NOT_CHATGPT_PRODUCT_UI")
        if photo.get("final_typography_in_render") is not False:
            errors.append("FINAL_TYPOGRAPHY_IN_RENDER_MUST_BE_FALSE")
        binding = photo.get("photo_only_contract")
        if not _is_mapping(binding) or binding.get("contract_id") != PHOTO_ONLY_CONTRACT_ID:
            errors.append("PHOTO_ONLY_CONTRACT_BINDING_INVALID")

    if not _is_mapping(figma):
        errors.append("FIGMA_COMPOSITION_RECEIPT_MISSING_OR_INVALID")
    else:
        binding = figma.get("composition_contract")
        if not _is_mapping(binding) or binding.get("contract_id") != FIGMA_CONTRACT_ID:
            errors.append("FIGMA_COMPOSITION_CONTRACT_BINDING_INVALID")
        errors.extend(
            _editable_node_errors(
                figma.get("editable_primary_title_nodes"), "PRIMARY_TITLE"
            )
        )
        errors.extend(
            _editable_node_errors(
                figma.get("editable_support_copy_nodes"), "SUPPORT_COPY"
            )
        )

    if not _is_mapping(export):
        errors.append("FINAL_EXPORT_RECEIPT_MISSING_OR_INVALID")

    if _is_mapping(photo) and _is_mapping(figma):
        source_photo = photo.get("source_photo")
        photo_sha = source_photo.get("sha256") if _is_mapping(source_photo) else None
        if photo_sha != figma.get("source_photo_sha256"):
            errors.append("PHOTO_TO_FIGMA_SOURCE_HASH_MISMATCH")
        photo_identity = (
            source_photo.get("file_identity") if _is_mapping(source_photo) else None
        )
        if photo_identity != figma.get("source_photo_identity"):
            errors.append("PHOTO_TO_FIGMA_SOURCE_IDENTITY_MISMATCH")

    if _is_mapping(figma) and _is_mapping(export):
        if figma.get("figma_file_key") != export.get("source_figma_file_key"):
            errors.append("FIGMA_TO_EXPORT_FILE_KEY_MISMATCH")
        if figma.get("frame_node_id") != export.get("source_figma_frame_node_id"):
            errors.append("FIGMA_TO_EXPORT_FRAME_NODE_MISMATCH")
        if figma.get("source_photo_sha256") != export.get("source_photo_sha256"):
            errors.append("PHOTO_TO_EXPORT_SOURCE_HASH_MISMATCH")
        if figma.get("receipt_id") != export.get("composition_receipt_id"):
            errors.append("FIGMA_TO_EXPORT_RECEIPT_ID_MISMATCH")
        if figma.get("receipt_sha256") != export.get("composition_receipt_sha256"):
            errors.append("FIGMA_TO_EXPORT_RECEIPT_HASH_MISMATCH")

    policy = receipt.get("forward_only_policy")
    if not _is_mapping(policy) or policy.get("policy_id") != GATE_POLICY_ID:
        errors.append("FORWARD_ONLY_POLICY_BINDING_INVALID")
    elif policy.get("historical_artifact_reclassified") is not False:
        errors.append("HISTORICAL_ARTIFACT_RECLASSIFICATION_PROHIBITED")

    if receipt.get("classification") == FORMAL_CLASSIFICATION:
        if not _is_mapping(gates):
            errors.append("FORMAL_OUTPUT_GATES_MISSING")
        else:
            expected = {
                "PHOTO_QUALITY_GATE",
                "TYPOGRAPHY_DESIGN_GATE",
                "PHOTO_TYPE_INTEGRATION_GATE",
                "BRAND_DISTINCTIVENESS_GATE",
                "EDITABLE_DESIGN_PROVENANCE_GATE",
                "FINAL_PIXEL_QUALITY_GATE",
            }
            for gate in sorted(expected):
                if gates.get(gate) != "PASS":
                    errors.append(f"FORMAL_OUTPUT_GATE_NOT_PASS:{gate}")
        if receipt.get("formal_commercial_output_eligible") is not True:
            errors.append("FORMAL_OUTPUT_ELIGIBILITY_NOT_TRUE")
        if _is_mapping(figma):
            for field in (
                "figma_file_key",
                "frame_node_id",
                "composition_timestamp",
                "designer_or_agent_route",
            ):
                if _unknown(figma.get(field)):
                    errors.append(f"FORMAL_OUTPUT_FIGMA_FIELD_UNKNOWN:{field}")
        if _is_mapping(export):
            for field in ("source_figma_file_key", "source_figma_frame_node_id"):
                if _unknown(export.get(field)):
                    errors.append(f"FORMAL_OUTPUT_EXPORT_FIELD_UNKNOWN:{field}")
    elif receipt.get("formal_commercial_output_eligible") is True:
        errors.append("NON_FORMAL_RECEIPT_CANNOT_BE_COMMERCIAL_ELIGIBLE")

    return errors


def require_commercial_receipt(receipt: Mapping[str, Any]) -> Mapping[str, Any]:
    errors = commercial_receipt_errors(receipt)
    if errors:
        raise PipelineContractError("; ".join(errors))
    return receipt
