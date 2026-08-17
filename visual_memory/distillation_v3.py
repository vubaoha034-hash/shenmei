"""Domain-neutral V3 visual-distillation support utilities.

This module deliberately lives above the frozen PHASE 1-8 raw substrate.  It
does not write raw records, choose an aesthetic essence, or promote Skills.
Deterministic code here validates evidence, preserves lineage, bounds runtime
packages, and enforces human-review gates around aesthetic decisions.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any, Iterable


class DistillationValidationError(ValueError):
    """Raised when a V3 derived artifact violates its contract."""


EVIDENCE_CLASSES = {"DIRECT_VISIBLE", "METADATA", "INFERENCE"}
BINDING_CLASSIFICATIONS = {
    "STYLE_SIGNATURE",
    "CONTENT_BOUND",
    "BRAND_BOUND",
    "PRODUCTION_BOUND",
    "OPTIONAL_VARIATION",
}
MECHANISM_DOMAINS = {
    "lighting",
    "color_grade",
    "capture_geometry",
    "focus_depth_blur",
    "material_treatment",
    "composition",
    "whitespace",
    "typography_lettering",
    "grid_layout",
    "graphic_language",
    "photo_type_integration",
    "retouch_finish",
}
MECHANISM_STATUSES = {
    "FAMILY_LOCAL",
    "CROSS_FAMILY_CANDIDATE",
    "CONTENT_BOUND",
    "BRAND_BOUND",
    "UNVERIFIED",
}
ANCHOR_DEPENDENCE = {
    "HIGH_REFERENCE_CONDITIONED",
    "MODERATE_REFERENCE_ASSISTED",
    "LOW_PROGRAM_DRIVEN",
    "UNKNOWN",
}
TRANSFER_OPERATORS = {"RECONSTRUCT", "CONTENT_SWAP", "COMPOSITION_OR_ASPECT_TRANSFER"}
WHOLE_WORK_ACTIONS = {
    "DUPLICATE_OR_NEAR_DUPLICATE",
    "REINFORCE_EXISTING_FAMILY",
    "REFINE_EXISTING_FAMILY",
    "NEW_FAMILY_CANDIDATE",
    "CONTRADICTION_EVIDENCE",
}
COMPONENT_SUPPORT_KINDS = {"DIRECT_COMPONENT_FEEDBACK", "REPEATED_EVIDENCE", "TRANSFER_VALIDATION"}
PROGRAM_STATUSES = {"PROVISIONAL_VISUAL_PROGRAM", "VALIDATED_VISUAL_PROGRAM", "DEPRECATED"}
TYPOGRAPHY_ROLES = {
    "display_title", "subtitle", "claim", "caption", "body", "tag", "seal_badge", "side_rail",
    "english_support", "handwritten_slogan", "module_label", "footer_brand_lockup", "data_chip", "other",
}
FIGMA_PRODUCIBILITY_MODES = {
    "LIVE_TEXT_REQUIRED", "LIVE_TEXT_PREFERRED", "VECTOR_LETTERING_REQUIRED",
    "APPROVED_SVG_ASSET_ALLOWED", "IMAGE_ONLY_ART_ASSET", "HUMAN_REVIEW_REQUIRED",
}
FIGMA_TEXT_POLICIES = {
    "LIVE_TEXT_REQUIRED", "LIVE_TEXT_PREFERRED", "VECTOR_ASSET_REQUIRED",
    "APPROVED_DISPLAY_ASSET", "NOT_FIGMA_ZERO_TO_ONE",
}
TYPOGRAPHY_OBSERVATION_SECTIONS = {
    "title_architecture", "glyph_mechanisms", "hierarchy_mechanisms",
    "layout_coupling", "color_material_binding", "failure_modes",
}
FIGMA_REQUIRED_QUALITY_GATES = {
    "no wrong characters", "no fake glyphs", "no English misspelling", "no spacing collapse",
    "no line-height failure", "no unintended overflow", "no lost footer lockup", "no wrong hierarchy",
    "no generic font substitution when family behavior requires approved lettering",
    "no pixel-art layer unintentionally covered", "export matches target dimensions",
}
FIGMA_REQUIRED_FAIL_CLOSED = {
    "locked copy missing", "required font or lettering asset not bound",
    "exact glyph correctness cannot be guaranteed", "Figma runtime/tool unavailable",
    "component asset unresolved", "layout contract cannot map to target aspect ratio",
    "export or readback failed",
}
DISPLAY_LETTERING_ROUTES = {
    "APPROVED_FONT_PLUS_CONTROLLED_DEFORMATION",
    "SPECIALIZED_VISUAL_SYNTHESIS_TO_APPROVED_ASSET",
    "HUMAN_OR_EXISTING_VECTOR_ASSET",
}
COMPONENT_EVIDENCE_STATES = {
    "WHOLE_IMAGE_APPROVED",
    "TYPOGRAPHY_DISTILLATION_REQUESTED",
    "TYPOGRAPHY_APPROVED",
    "TYPOGRAPHY_REJECTED",
    "DISPLAY_TITLE_APPROVED",
    "FUNCTIONAL_TYPE_APPROVED",
    "LAYOUT_APPROVED",
    "BILINGUAL_SYSTEM_APPROVED",
    "BADGE_OR_MARK_APPROVED",
    "COMPONENT_UNCONFIRMED",
}


def _object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise DistillationValidationError(f"{label} must be an object")
    return value


def _list(value: Any, label: str, *, nonempty: bool = False) -> list[Any]:
    if not isinstance(value, list):
        raise DistillationValidationError(f"{label} must be a list")
    if nonempty and not value:
        raise DistillationValidationError(f"{label} may not be empty")
    return value


def _text(value: Any, label: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str) or (not allow_empty and not value.strip()):
        raise DistillationValidationError(f"{label} must be a non-empty string")
    return value


def _required(record: dict[str, Any], fields: Iterable[str], label: str) -> None:
    missing = [field for field in fields if field not in record]
    if missing:
        raise DistillationValidationError(f"{label} missing: {', '.join(missing)}")


def _confidence(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= value <= 1:
        raise DistillationValidationError(f"{label} must be between 0 and 1")
    return float(value)


def _sha(value: Any, label: str) -> str:
    text = _text(value, label)
    digest = text.removeprefix("sha256:")
    if len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
        raise DistillationValidationError(f"{label} must be a lowercase SHA-256")
    return digest


def stable_fingerprint(value: Any) -> str:
    """Return a deterministic fingerprint for a derived artifact."""
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def validate_evidence_item(item: Any) -> dict[str, Any]:
    row = _object(item, "evidence item")
    _required(
        row,
        (
            "evidence_id",
            "dimension",
            "claim",
            "evidence_class",
            "confidence",
            "evidence_pointer",
            "uncertainty",
            "binding_classification",
        ),
        "evidence item",
    )
    _text(row["evidence_id"], "evidence_id")
    _text(row["dimension"], "dimension")
    _text(row["claim"], "claim")
    if row["evidence_class"] not in EVIDENCE_CLASSES:
        raise DistillationValidationError("invalid evidence_class")
    _confidence(row["confidence"], "confidence")
    pointer = _object(row["evidence_pointer"], "evidence_pointer")
    _required(pointer, ("asset_id", "sha256", "region"), "evidence_pointer")
    _text(pointer["asset_id"], "evidence_pointer.asset_id")
    _sha(pointer["sha256"], "evidence_pointer.sha256")
    _text(pointer["region"], "evidence_pointer.region")
    if not isinstance(row["uncertainty"], (str, type(None))):
        raise DistillationValidationError("uncertainty must be string or null")
    if row["binding_classification"] not in BINDING_CLASSIFICATIONS:
        raise DistillationValidationError("invalid binding_classification")
    if "measurements" in row and not isinstance(row["measurements"], dict):
        raise DistillationValidationError("measurements must be an object")
    return row


def validate_deep_evidence(record: Any) -> dict[str, Any]:
    data = _object(record, "deep evidence")
    _required(
        data,
        ("schema_version", "evidence_object_id", "status", "subject", "analysis", "evidence_lineage"),
        "deep evidence",
    )
    if data["schema_version"] != "3.0.0" or data["status"] != "DEEP_EVIDENCE":
        raise DistillationValidationError("deep evidence version/status is invalid")
    subject = _object(data["subject"], "subject")
    _required(subject, ("family_id", "canonical_asset_id", "canonical_sha256"), "subject")
    _sha(subject["canonical_sha256"], "subject.canonical_sha256")
    analysis = _object(data["analysis"], "analysis")
    for domain in ("photography", "graphic_design", "integration"):
        rows = _list(analysis.get(domain), f"analysis.{domain}", nonempty=True)
        for row in rows:
            validate_evidence_item(row)
    lineage = _list(data["evidence_lineage"], "evidence_lineage", nonempty=True)
    if any(not isinstance(item, str) or not item for item in lineage):
        raise DistillationValidationError("evidence_lineage must contain IDs")
    return data


def rank_candidate_evidence(record: Any, *, limit: int = 12) -> list[dict[str, Any]]:
    """Rank and deduplicate evidence without deciding what the style *is*."""
    if limit < 1:
        raise ValueError("limit must be positive")
    evidence = validate_deep_evidence(record)
    best_by_claim: dict[tuple[str, str], dict[str, Any]] = {}
    for rows in evidence["analysis"].values():
        for row in rows:
            key = (row["dimension"].strip().casefold(), row["claim"].strip().casefold())
            current = best_by_claim.get(key)
            if current is None or row["confidence"] > current["confidence"]:
                best_by_claim[key] = row
    class_rank = {"DIRECT_VISIBLE": 0, "METADATA": 1, "INFERENCE": 2}
    ranked = sorted(
        best_by_claim.values(),
        key=lambda row: (class_rank[row["evidence_class"]], -row["confidence"], row["evidence_id"]),
    )
    return ranked[:limit]


def validate_distillation_hypothesis(record: Any) -> dict[str, Any]:
    data = _object(record, "distillation hypothesis")
    _required(
        data,
        (
            "schema_version",
            "artifact_type",
            "hypothesis_id",
            "family_id",
            "status",
            "source_evidence_object_ids",
            "candidate_visual_philosophy",
            "candidate_stable_grammar",
            "candidate_variation_axes",
            "candidate_compatibility_constraints",
            "unresolved_contradictions",
            "expected_anchor_dependence",
            "evidence_lineage",
            "synthesizer",
        ),
        "distillation hypothesis",
    )
    if data["schema_version"] != "3.0.0" or data["artifact_type"] != "DISTILLATION_HYPOTHESIS":
        raise DistillationValidationError("distillation hypothesis type/version is invalid")
    if data["status"] != "HUMAN_DISTILLATION_REVIEW_PENDING":
        raise DistillationValidationError("hypothesis must remain pending human review")
    philosophy = _object(data["candidate_visual_philosophy"], "candidate_visual_philosophy")
    _required(philosophy, ("statement", "confidence", "evidence_ids"), "candidate_visual_philosophy")
    _text(philosophy["statement"], "candidate_visual_philosophy.statement")
    _confidence(philosophy["confidence"], "candidate_visual_philosophy.confidence")
    _list(philosophy["evidence_ids"], "candidate_visual_philosophy.evidence_ids", nonempty=True)
    grammar = _list(data["candidate_stable_grammar"], "candidate_stable_grammar", nonempty=True)
    for item in grammar:
        row = _object(item, "candidate grammar item")
        _required(row, ("mechanism_id", "statement", "state", "confidence", "evidence_ids"), "candidate grammar item")
        if row["state"] != "INVARIANT_HYPOTHESIS":
            raise DistillationValidationError("unreviewed grammar may only be INVARIANT_HYPOTHESIS")
        _confidence(row["confidence"], "candidate grammar confidence")
        _list(row["evidence_ids"], "candidate grammar evidence_ids", nonempty=True)
    if data["expected_anchor_dependence"] not in ANCHOR_DEPENDENCE:
        raise DistillationValidationError("invalid expected_anchor_dependence")
    _list(data["evidence_lineage"], "evidence_lineage", nonempty=True)
    return data


def package_distillation_hypothesis(
    *,
    hypothesis_id: str,
    family_id: str,
    source_evidence_object_ids: list[str],
    candidate_visual_philosophy: dict[str, Any],
    candidate_stable_grammar: list[dict[str, Any]],
    candidate_variation_axes: list[dict[str, Any]],
    candidate_compatibility_constraints: list[dict[str, Any]],
    unresolved_contradictions: list[dict[str, Any]],
    expected_anchor_dependence: str,
    evidence_lineage: list[str],
    synthesizer: dict[str, Any],
) -> dict[str, Any]:
    """Package analyst/model hypotheses; no claim is promoted by this function."""
    record = {
        "schema_version": "3.0.0",
        "artifact_type": "DISTILLATION_HYPOTHESIS",
        "hypothesis_id": hypothesis_id,
        "family_id": family_id,
        "status": "HUMAN_DISTILLATION_REVIEW_PENDING",
        "source_evidence_object_ids": source_evidence_object_ids,
        "candidate_visual_philosophy": candidate_visual_philosophy,
        "candidate_stable_grammar": candidate_stable_grammar,
        "candidate_variation_axes": candidate_variation_axes,
        "candidate_compatibility_constraints": candidate_compatibility_constraints,
        "unresolved_contradictions": unresolved_contradictions,
        "expected_anchor_dependence": expected_anchor_dependence,
        "evidence_lineage": evidence_lineage,
        "synthesizer": synthesizer,
    }
    return validate_distillation_hypothesis(record)


def validate_visual_program(record: Any) -> dict[str, Any]:
    data = _object(record, "visual program")
    required = (
        "program_id", "family_id", "status", "validation_status", "visual_philosophy", "mother_reference", "golden_exemplars",
        "stable_grammar", "variation_axes", "content_compatibility", "content_bound_features",
        "brand_bound_features", "production_bound_features", "typography_role", "color_light_material_signature", "integration_rules",
        "generic_shortcut_blockers", "freedoms", "transfer_operators", "validation_evidence",
        "renderer_provenance_requirements", "anchor_dependence", "promotion_history", "evidence_lineage",
    )
    _required(data, required, "visual program")
    if data["status"] not in PROGRAM_STATUSES:
        raise DistillationValidationError("invalid visual program status")
    validation_statuses = {
        "TRANSFER_VALIDATION_PENDING",
        "TRANSFER_VALIDATION_IN_PROGRESS",
        "TRANSFER_VALIDATED",
        "TRANSFER_VALIDATION_FAILED",
        "NOT_APPLICABLE",
    }
    if data["validation_status"] not in validation_statuses:
        raise DistillationValidationError("invalid visual program validation_status")
    if data["status"] == "PROVISIONAL_VISUAL_PROGRAM" and data["validation_status"] not in {
        "TRANSFER_VALIDATION_PENDING",
        "TRANSFER_VALIDATION_IN_PROGRESS",
    }:
        raise DistillationValidationError("provisional programs must remain pending or in transfer validation")
    grammar = _list(data["stable_grammar"], "stable_grammar", nonempty=True)
    for row in grammar:
        item = _object(row, "stable grammar item")
        if item.get("state") not in {"INVARIANT_HYPOTHESIS", "VALIDATED_INVARIANT"}:
            raise DistillationValidationError("stable grammar state must expose validation state")
    if not 4 <= len(grammar) <= 8 and not _text(data.get("grammar_count_exception"), "grammar_count_exception"):
        raise DistillationValidationError("grammar counts outside default 4-8 need an explicit exception")
    blockers = _list(data["generic_shortcut_blockers"], "generic_shortcut_blockers")
    if len(blockers) > 3:
        raise DistillationValidationError("generic_shortcut_blockers hard max is 3")
    if data["anchor_dependence"] not in ANCHOR_DEPENDENCE:
        raise DistillationValidationError("invalid anchor_dependence")
    if "deep_evidence" in data or "analysis" in data:
        raise DistillationValidationError("deep evidence may not be dumped into a runtime program")
    typography = data.get("typography_program")
    if typography is not None:
        link = _object(typography, "typography_program")
        _required(
            link,
            (
                "evidence_id", "evidence_path", "hypothesis_id", "hypothesis_path", "hypothesis_status",
                "mechanism_ids", "figma_contract_id", "figma_contract_path", "copy_fidelity_policy",
                "transfer_risks", "runtime_builder", "component_approval_status", "promotion_status",
            ),
            "typography_program",
        )
        if link["hypothesis_status"] not in {
            "DISTILLATION_HYPOTHESIS / HUMAN_REVIEW_PENDING", "PROVISIONAL_PROGRAM_COMPONENT",
        }:
            raise DistillationValidationError("invalid typography hypothesis linkage state")
        if len(_list(link["mechanism_ids"], "typography mechanism_ids", nonempty=True)) > 8:
            raise DistillationValidationError("typography linkage exceeds bounded mechanism count")
        if link["component_approval_status"] != "UNCONFIRMED" or link["promotion_status"] != "UNPROMOTED":
            raise DistillationValidationError("Visual Program cannot self-approve or promote typography")
    return data


def validate_mechanism(record: Any) -> dict[str, Any]:
    data = _object(record, "visual mechanism")
    _required(
        data,
        (
            "mechanism_id", "domain", "description", "evidence_pointers", "family_scope", "transfer_scope",
            "status", "support_basis", "component_approval_status", "transfer_validation_support",
            "contradiction_evidence", "promotion_status",
        ),
        "visual mechanism",
    )
    if data["domain"] not in MECHANISM_DOMAINS or data["status"] not in MECHANISM_STATUSES:
        raise DistillationValidationError("invalid mechanism domain/status")
    support = _list(data["support_basis"], "support_basis")
    support_kinds = {row.get("kind") for row in support if isinstance(row, dict)}
    if data["component_approval_status"] != "UNCONFIRMED" and not support_kinds.intersection(COMPONENT_SUPPORT_KINDS):
        raise DistillationValidationError("whole-image approval cannot establish component approval")
    if data["promotion_status"] == "PROMOTED" and data["component_approval_status"] != "HUMAN_APPROVED":
        raise DistillationValidationError("promoted mechanisms require human component approval")
    if data["domain"] == "typography_lettering":
        _required(
            data,
            (
                "human_name_zh", "definition", "visual_role", "observed_in_families", "evidence_refs",
                "figma_execution_mode", "anti_collapse_notes",
            ),
            "typography mechanism",
        )
        _list(data["observed_in_families"], "observed_in_families", nonempty=True)
        _list(data["evidence_refs"], "evidence_refs", nonempty=True)
        _list(data["anti_collapse_notes"], "anti_collapse_notes", nonempty=True)
        if not set(data["observed_in_families"]).issubset(set(data["family_scope"])):
            raise DistillationValidationError("observed typography families must be included in family_scope")
        if data.get("grammar_role") not in {
            None, "STABLE_HYPOTHESIS", "OPTIONAL_VARIATION / SUPPORTING_MECHANISM",
            "OPTIONAL_OR_EQUIVALENT_COUNTERWEIGHT", "TYPOGRAPHY_ONLY_CANDIDATE",
        }:
            raise DistillationValidationError("invalid typography grammar_role")
    return data


def _validate_typography_observation(record: Any) -> dict[str, Any]:
    row = _object(record, "typography observation")
    _required(
        row,
        ("observation_id", "statement", "evidence_class", "confidence", "evidence_pointer", "uncertainty", "binding_classification"),
        "typography observation",
    )
    _text(row["observation_id"], "observation_id")
    _text(row["statement"], "statement")
    if row["evidence_class"] not in EVIDENCE_CLASSES:
        raise DistillationValidationError("invalid typography evidence_class")
    _confidence(row["confidence"], "typography confidence")
    pointer = _object(row["evidence_pointer"], "typography evidence_pointer")
    _required(pointer, ("asset_id", "sha256", "region"), "typography evidence_pointer")
    _text(pointer["asset_id"], "typography evidence_pointer.asset_id")
    _sha(pointer["sha256"], "typography evidence_pointer.sha256")
    _text(pointer["region"], "typography evidence_pointer.region")
    if row["binding_classification"] not in BINDING_CLASSIFICATIONS:
        raise DistillationValidationError("invalid typography binding_classification")
    if not isinstance(row["uncertainty"], (str, type(None))):
        raise DistillationValidationError("typography uncertainty must be string or null")
    return row


def validate_typography_evidence(record: Any) -> dict[str, Any]:
    """Validate component-separated typography evidence against canonical pixels."""
    data = _object(record, "typography evidence")
    _required(
        data,
        (
            "schema_version", "artifact_type", "evidence_id", "family_id", "status", "subject",
            "text_role_inventory", "script_system", "evidence_sections", "figma_producibility",
            "component_approval_status", "evidence_lineage",
        ),
        "typography evidence",
    )
    if data["schema_version"] != "3.0.0" or data["artifact_type"] != "TYPOGRAPHY_DEEP_EVIDENCE":
        raise DistillationValidationError("typography evidence type/version is invalid")
    if data["status"] != "DEEP_EVIDENCE":
        raise DistillationValidationError("typography evidence must remain DEEP_EVIDENCE")
    if data["component_approval_status"] != "UNCONFIRMED":
        raise DistillationValidationError("whole-image evidence cannot approve typography components")
    if "distillation_scope" in data and data["distillation_scope"] not in {
        "FAMILY_TYPOGRAPHY_COMPONENT", "TYPOGRAPHY_ONLY_FAMILY_CANDIDATE"
    }:
        raise DistillationValidationError("invalid typography distillation_scope")
    subject = _object(data["subject"], "typography subject")
    _required(subject, ("canonical_asset_id", "canonical_sample_id", "canonical_sha256", "canonical_dimensions", "pixel_binding"), "typography subject")
    _sha(subject["canonical_sha256"], "typography subject canonical_sha256")
    if subject["pixel_binding"] != "CANONICAL_PIXELS_DIRECTLY_INSPECTED":
        raise DistillationValidationError("typography evidence requires direct canonical-pixel inspection")
    roles = _list(data["text_role_inventory"], "text_role_inventory", nonempty=True)
    role_names = []
    for row in roles:
        item = _object(row, "text role")
        _required(item, ("role", "present", "observed_content", "visual_job", "evidence_refs"), "text role")
        if item["role"] not in TYPOGRAPHY_ROLES or not isinstance(item["present"], bool):
            raise DistillationValidationError("invalid typography role inventory")
        role_names.append(item["role"])
    if set(role_names) != TYPOGRAPHY_ROLES or len(role_names) != len(TYPOGRAPHY_ROLES):
        raise DistillationValidationError("text role inventory must cover each V3 role exactly once")
    script = _object(data["script_system"], "script_system")
    _required(script, ("scripts", "script_relationship", "type_family_behavior", "language_hierarchy", "evidence_refs"), "script_system")
    sections = _object(data["evidence_sections"], "evidence_sections")
    if set(sections) != TYPOGRAPHY_OBSERVATION_SECTIONS:
        raise DistillationValidationError("typography evidence sections are incomplete")
    for name, rows in sections.items():
        for row in _list(rows, name, nonempty=True):
            _validate_typography_observation(row)
    production = _list(data["figma_producibility"], "figma_producibility", nonempty=True)
    covered_roles = set()
    for row in production:
        item = _object(row, "figma producibility row")
        _required(item, ("role", "mode", "rationale", "dependencies"), "figma producibility row")
        if item["role"] not in TYPOGRAPHY_ROLES or item["mode"] not in FIGMA_PRODUCIBILITY_MODES:
            raise DistillationValidationError("invalid Figma producibility row")
        covered_roles.add(item["role"])
    required_roles = {row["role"] for row in roles if row["present"] and row["role"] != "other"}
    if not required_roles.issubset(covered_roles):
        raise DistillationValidationError("every present typography role needs a Figma producibility policy")
    _list(data["evidence_lineage"], "typography evidence_lineage", nonempty=True)
    return data


def validate_typography_hypothesis(record: Any) -> dict[str, Any]:
    data = _object(record, "typography hypothesis")
    _required(
        data,
        (
            "schema_version", "artifact_type", "hypothesis_id", "family_id", "status", "review_status",
            "source_evidence_ids", "typography_visual_philosophy", "stable_typography_grammar",
            "variation_axes_typography", "content_bound_typography", "brand_bound_typography",
            "production_bound_typography", "typography_content_compatibility", "figma_execution_hypothesis",
            "transfer_risks", "unresolved_uncertainties", "component_approval_status", "promotion_status", "evidence_lineage",
        ),
        "typography hypothesis",
    )
    if data["schema_version"] != "3.0.0" or data["artifact_type"] != "TYPOGRAPHY_DISTILLATION_HYPOTHESIS":
        raise DistillationValidationError("typography hypothesis type/version is invalid")
    if data["status"] not in {"DISTILLATION_HYPOTHESIS", "PROVISIONAL_PROGRAM_COMPONENT"}:
        raise DistillationValidationError("invalid typography hypothesis status")
    if data["status"] == "DISTILLATION_HYPOTHESIS" and data["review_status"] != "HUMAN_REVIEW_PENDING":
        raise DistillationValidationError("distillation hypothesis must remain pending human review")
    if data["status"] == "PROVISIONAL_PROGRAM_COMPONENT" and data["review_status"] != "HUMAN_REVIEWED":
        raise DistillationValidationError("provisional typography component requires human review")
    if data["component_approval_status"] != "UNCONFIRMED" or data["promotion_status"] != "UNPROMOTED":
        raise DistillationValidationError("typography hypothesis cannot self-approve or promote")
    if "distillation_scope" in data and data["distillation_scope"] not in {
        "FAMILY_TYPOGRAPHY_COMPONENT", "TYPOGRAPHY_ONLY_FAMILY_CANDIDATE"
    }:
        raise DistillationValidationError("invalid typography hypothesis distillation_scope")
    philosophy = _object(data["typography_visual_philosophy"], "typography_visual_philosophy")
    _required(philosophy, ("statement", "confidence", "evidence_ids"), "typography_visual_philosophy")
    _confidence(philosophy["confidence"], "typography philosophy confidence")
    grammar = _list(data["stable_typography_grammar"], "stable_typography_grammar", nonempty=True)
    if len(grammar) > 8:
        raise DistillationValidationError("typography grammar exceeds bounded default")
    for row in grammar:
        item = _object(row, "typography grammar")
        _required(item, ("mechanism_id", "statement", "state", "confidence", "evidence_ids"), "typography grammar")
        if item["state"] != "INVARIANT_HYPOTHESIS":
            raise DistillationValidationError("typography grammar remains hypothesis before transfer validation")
        _confidence(item["confidence"], "typography grammar confidence")
        _list(item["evidence_ids"], "typography grammar evidence_ids", nonempty=True)
    execution = _object(data["figma_execution_hypothesis"], "figma_execution_hypothesis")
    if execution.get("not_figma_zero_to_one") is not True:
        raise DistillationValidationError("Figma may not be assigned zero-to-one lettering art direction")
    _list(data["transfer_risks"], "typography transfer_risks", nonempty=True)
    _list(data["evidence_lineage"], "typography hypothesis evidence_lineage", nonempty=True)
    return data


def validate_display_lettering_source_pipeline(record: Any) -> dict[str, Any]:
    """Validate the auditable source-to-approved-asset boundary for display lettering."""
    data = _object(record, "display lettering source pipeline")
    _required(
        data,
        (
            "schema_version", "pipeline_id", "status", "routes", "required_common_record",
            "approval_boundary", "figma_boundary", "promotion_status",
        ),
        "display lettering source pipeline",
    )
    if data["schema_version"] != "3.0.0" or data["status"] != "CONTRACT_READY":
        raise DistillationValidationError("invalid display lettering pipeline version/status")
    routes = _list(data["routes"], "display lettering routes", nonempty=True)
    route_names = {row.get("route") for row in routes if isinstance(row, dict)}
    if route_names != DISPLAY_LETTERING_ROUTES or len(routes) != len(DISPLAY_LETTERING_ROUTES):
        raise DistillationValidationError("display lettering pipeline must define every route exactly once")
    required_fields = {
        "exact_copy", "source_identity", "provenance", "family_behavior_target", "source_material",
        "transform_record", "correctness_verification", "human_review", "approved_asset_identity",
        "figma_placement_contract", "promotion_status",
    }
    common = set(_list(data["required_common_record"], "required_common_record", nonempty=True))
    if not required_fields.issubset(common):
        raise DistillationValidationError("display lettering common record is incomplete")
    for route in routes:
        row = _object(route, "display lettering route")
        _required(row, ("route", "source_requirements", "allowed_transformations", "fail_closed_conditions"), "display lettering route")
        _list(row["source_requirements"], "source_requirements", nonempty=True)
        _list(row["fail_closed_conditions"], "fail_closed_conditions", nonempty=True)
    if data["approval_boundary"] != "HUMAN_REVIEW_REQUIRED_BEFORE_APPROVED_ASSET":
        raise DistillationValidationError("display lettering output requires human review")
    if data["figma_boundary"] != "PLACE_OR_CONTROLLED_TRANSFORM_APPROVED_SOURCE_NOT_ZERO_TO_ONE":
        raise DistillationValidationError("Figma display-lettering boundary is invalid")
    if data["promotion_status"] != "UNPROMOTED":
        raise DistillationValidationError("display lettering pipeline cannot auto-promote")
    return data


def validate_typography_component_evidence_contract(record: Any) -> dict[str, Any]:
    data = _object(record, "typography component evidence contract")
    _required(data, ("schema_version", "contract_id", "allowed_states", "separation_rules", "default_state"), "typography component evidence contract")
    if data["schema_version"] != "3.0.0":
        raise DistillationValidationError("invalid component evidence contract version")
    if set(_list(data["allowed_states"], "allowed_states", nonempty=True)) != COMPONENT_EVIDENCE_STATES:
        raise DistillationValidationError("component evidence state vocabulary is incomplete")
    if data["default_state"] != "COMPONENT_UNCONFIRMED":
        raise DistillationValidationError("component evidence must default to unconfirmed")
    rules = _object(data["separation_rules"], "separation_rules")
    if rules.get("whole_image_approval_populates_component_approval") is not False:
        raise DistillationValidationError("whole-image approval cannot populate typography components")
    if rules.get("distillation_request_implies_approval") is not False:
        raise DistillationValidationError("a distillation request cannot imply component approval")
    return data


def validate_shanyeji_figma_producibility_map(record: Any) -> dict[str, Any]:
    data = _object(record, "Shan Ye Ji Figma producibility map")
    _required(data, ("schema_version", "map_id", "family_id", "status", "review_status", "role_map", "central_title_claim", "runtime_status"), "Shan Ye Ji Figma producibility map")
    if data["schema_version"] != "3.0.0" or data["status"] != "PROVISIONAL_FIGMA_PRODUCIBILITY_MAP":
        raise DistillationValidationError("invalid Shan Ye Ji Figma map status")
    if data["review_status"] != "HUMAN_REVIEW_PENDING":
        raise DistillationValidationError("Shan Ye Ji Figma map must remain pending human review")
    roles = {row.get("role"): row.get("production_mode") for row in _list(data["role_map"], "role_map", nonempty=True)}
    required = {
        "functional_chinese": "LIVE_TEXT_REQUIRED",
        "functional_english": "LIVE_TEXT_REQUIRED",
        "top_english_claims": "LIVE_TEXT_REQUIRED",
        "orange_semantic_line": "FIGMA_VECTOR_PATH",
        "central_display_title": "DISPLAY_LETTERING_SOURCE_PIPELINE_REQUIRED",
    }
    if any(roles.get(role) != mode for role, mode in required.items()):
        raise DistillationValidationError("Shan Ye Ji Figma role policy is incomplete")
    if data["central_title_claim"] != "NOT_AUTOMATICALLY_REPRODUCIBLE_IN_FIGMA":
        raise DistillationValidationError("central display title capability must remain unresolved")
    return data


def validate_figma_production_contract(record: Any) -> dict[str, Any]:
    data = _object(record, "Figma production contract")
    _required(
        data,
        (
            "schema_version", "contract_id", "program_id", "family_id", "typography_hypothesis_id",
            "contract_status", "runtime_status", "production_layer_scope", "live_text_vs_vector_policy",
            "typography_tokens", "layout_contract", "copy_fidelity_rules", "componentization_plan",
            "quality_gate_for_figma_output", "fail_closed_conditions", "unresolved_dependencies", "evidence_lineage",
        ),
        "Figma production contract",
    )
    if data["schema_version"] != "3.0.0" or data["contract_status"] != "FIGMA_CONTRACT_READY":
        raise DistillationValidationError("invalid Figma contract version/status")
    if data["runtime_status"] not in {"FIGMA_RUNTIME_UNVERIFIED", "FIGMA_RUNTIME_VERIFIED", "FIGMA_RUNTIME_UNAVAILABLE_IN_CURRENT_CONTEXT"}:
        raise DistillationValidationError("invalid Figma runtime status")
    if data["runtime_status"] == "FIGMA_RUNTIME_VERIFIED" and not data.get("runtime_receipt"):
        raise DistillationValidationError("verified Figma runtime requires a receipt")
    scope = _object(data["production_layer_scope"], "production_layer_scope")
    _required(scope, ("figma_owns", "figma_may_place", "figma_must_not_own"), "production_layer_scope")
    must_not = " ".join(scope["figma_must_not_own"]).casefold()
    if "zero-to-one" not in must_not:
        raise DistillationValidationError("Figma scope must reject zero-to-one lettering authorship")
    policies = _list(data["live_text_vs_vector_policy"], "live_text_vs_vector_policy", nonempty=True)
    if not any(row.get("policy") == "NOT_FIGMA_ZERO_TO_ONE" for row in policies if isinstance(row, dict)):
        raise DistillationValidationError("Figma policy must expose NOT_FIGMA_ZERO_TO_ONE")
    for row in policies:
        item = _object(row, "live-text/vector policy")
        if item.get("policy") not in FIGMA_TEXT_POLICIES:
            raise DistillationValidationError("invalid live-text/vector policy")
    copy = _object(data["copy_fidelity_rules"], "copy_fidelity_rules")
    _required(copy, ("VERBATIM_REQUIRED", "PLACEHOLDER_ALLOWED", "HUMAN_APPROVAL_REQUIRED"), "copy_fidelity_rules")
    verbatim = {item.casefold() for item in copy["VERBATIM_REQUIRED"]}
    for required in ("brand name", "dish name", "price", "date", "address"):
        if required not in verbatim and required.replace("dish", "product") not in verbatim:
            raise DistillationValidationError(f"copy fidelity missing {required}")
    gates = set(_list(data["quality_gate_for_figma_output"], "quality_gate_for_figma_output", nonempty=True))
    if not FIGMA_REQUIRED_QUALITY_GATES.issubset(gates):
        raise DistillationValidationError("Figma quality gate is incomplete")
    blockers = set(_list(data["fail_closed_conditions"], "fail_closed_conditions", nonempty=True))
    if not FIGMA_REQUIRED_FAIL_CLOSED.issubset(blockers):
        raise DistillationValidationError("Figma fail-closed contract is incomplete")
    tokens = _list(data["typography_tokens"], "typography_tokens", nonempty=True)
    if any("FONT_SELECTION_HUMAN_PENDING" in str(row.get("font_family")) for row in tokens):
        if "FONT_SELECTION_HUMAN_PENDING" not in data["unresolved_dependencies"]:
            raise DistillationValidationError("unresolved font token must remain an explicit dependency")
    return data


def validate_figma_dry_run_receipt(record: Any) -> dict[str, Any]:
    data = _object(record, "Figma dry-run receipt")
    _required(
        data,
        (
            "schema_version", "receipt_id", "status", "figma_file_key", "figma_account_email", "page_id",
            "frame_id", "component_id", "variable_collection_id", "variable_ids", "text_style_id", "text_nodes",
            "vector_nodes", "export", "readback_verified", "aesthetic_approval", "golden_exemplar", "durable_promotion",
        ),
        "Figma dry-run receipt",
    )
    if data["schema_version"] != "3.0.0" or data["status"] != "FIGMA_RUNTIME_VERIFIED":
        raise DistillationValidationError("invalid Figma dry-run status")
    if not data["readback_verified"] or data["aesthetic_approval"] or data["golden_exemplar"] or data["durable_promotion"]:
        raise DistillationValidationError("technical dry run may not imply aesthetic approval or promotion")
    text_nodes = _list(data["text_nodes"], "Figma dry-run text_nodes", nonempty=True)
    expected = {"山野集", "常德饮食文化代表名片", "MOUNTAIN MARKET", "WILD AROMA"}
    if {row.get("characters") for row in text_nodes} != expected or any(row.get("live_text") is not True for row in text_nodes):
        raise DistillationValidationError("Figma dry run must read back the exact live neutral test copy")
    export = _object(data["export"], "Figma dry-run export")
    if export.get("format") != "PNG" or export.get("readable") is not True:
        raise DistillationValidationError("Figma dry-run export must be a readable PNG")
    _sha(export.get("sha256"), "Figma dry-run export SHA")
    return data


def build_typography_runtime_package(
    program: dict[str, Any],
    hypothesis: dict[str, Any],
    figma_contract: dict[str, Any],
    *,
    exact_copy: dict[str, str],
    approved_typography_mechanisms: list[dict[str, Any]],
    purpose: str = "HUMAN_REVIEW",
) -> dict[str, Any]:
    """Build a bounded typography package without turning hypotheses into production truth."""
    validate_visual_program(program)
    validate_typography_hypothesis(hypothesis)
    validate_figma_production_contract(figma_contract)
    if purpose not in {"HUMAN_REVIEW", "PRODUCTION"}:
        raise DistillationValidationError("invalid typography runtime purpose")
    if not (program["family_id"] == hypothesis["family_id"] == figma_contract["family_id"]):
        raise DistillationValidationError("typography runtime family mismatch")
    if len(exact_copy) > 12:
        raise DistillationValidationError("exact typography copy hard max is 12 roles")
    if len(approved_typography_mechanisms) > 4:
        raise DistillationValidationError("active typography mechanisms hard max is 4")
    for mechanism in approved_typography_mechanisms:
        validate_mechanism(mechanism)
        if mechanism["component_approval_status"] not in {"SUPPORTED", "HUMAN_APPROVED"}:
            raise DistillationValidationError("unconfirmed typography mechanism cannot enter active runtime")
    production_authorized = (
        purpose == "PRODUCTION"
        and hypothesis["status"] == "PROVISIONAL_PROGRAM_COMPONENT"
        and hypothesis["review_status"] == "HUMAN_REVIEWED"
        and not figma_contract["unresolved_dependencies"]
    )
    if purpose == "PRODUCTION" and not production_authorized:
        raise DistillationValidationError("typography production is blocked pending review/dependency resolution")
    package = {
        "package_version": "3.0.0",
        "purpose": purpose,
        "program_id": program["program_id"],
        "family_id": program["family_id"],
        "family_typography_program": {
            "hypothesis_id": hypothesis["hypothesis_id"],
            "status": hypothesis["status"],
            "review_status": hypothesis["review_status"],
            "visual_philosophy": hypothesis["typography_visual_philosophy"],
            "stable_grammar": hypothesis["stable_typography_grammar"][:6],
            "variation_axes": hypothesis["variation_axes_typography"][:4],
        },
        "exact_copy": dict(exact_copy),
        "figma_production_contract": {
            "contract_id": figma_contract["contract_id"],
            "contract_status": figma_contract["contract_status"],
            "runtime_status": figma_contract["runtime_status"],
            "live_text_vs_vector_policy": figma_contract["live_text_vs_vector_policy"][:12],
            "copy_fidelity_rules": figma_contract["copy_fidelity_rules"],
            "fail_closed_conditions": figma_contract["fail_closed_conditions"][:8],
        },
        "approved_typography_mechanisms": list(approved_typography_mechanisms),
        "unresolved_typography_dependencies": figma_contract["unresolved_dependencies"][:8],
        "renderer_vs_figma_responsibility_split": hypothesis["figma_execution_hypothesis"],
        "production_authorized": production_authorized,
        "deep_evidence_embedded": False,
    }
    if "evidence_sections" in json.dumps(package, ensure_ascii=False):
        raise AssertionError("typography runtime leaked deep evidence")
    return package


def classify_liked_work(
    *,
    sample_id: str,
    primary_action: str,
    whole_image_evidence_ids: list[str],
    component_evidence: list[dict[str, Any]],
) -> dict[str, Any]:
    """Package a liked-work decision without extrapolating component approval."""
    if primary_action not in WHOLE_WORK_ACTIONS:
        raise DistillationValidationError("invalid liked-work primary action")
    for row in component_evidence:
        if row.get("support_kind") not in COMPONENT_SUPPORT_KINDS:
            raise DistillationValidationError("component evidence needs direct, repeated, or transfer support")
    return {
        "sample_id": _text(sample_id, "sample_id"),
        "primary_action": primary_action,
        "whole_image_evidence_ids": list(whole_image_evidence_ids),
        "component_evidence": list(component_evidence),
        "whole_image_like_implies_component_like": False,
    }


def validate_semantic_identity(record: Any) -> dict[str, Any]:
    data = _object(record, "semantic identity")
    _required(
        data,
        (
            "schema_version", "semantic_identity_id", "domain", "canonical_name", "aliases", "primary_entity",
            "process", "required_visible_identity_cues", "forbidden_substitutions", "hero_suitability",
            "authority", "confidence", "evidence_sources",
        ),
        "semantic identity",
    )
    if data["schema_version"] != "3.0.0":
        raise DistillationValidationError("invalid semantic identity version")
    _text(data["domain"], "domain")
    _text(data["canonical_name"], "canonical_name")
    _text(data["primary_entity"], "primary_entity")
    _list(data["required_visible_identity_cues"], "required_visible_identity_cues", nonempty=True)
    _confidence(data["confidence"], "confidence")
    return data


def validate_transfer_plan(record: Any) -> dict[str, Any]:
    data = _object(record, "transfer plan")
    _required(
        data,
        (
            "transfer_id", "operator", "program_id", "execution_status", "preconditions", "stable_grammar_to_preserve",
            "allowed_variation", "semantic_identity_requirements", "content_compatibility",
            "reference_attachments", "expected_anchor_dependence_test", "failure_criteria",
            "technical_correctness_gates", "human_aesthetic_review_axes", "absolute_quality_floor",
            "renderer_provenance_requirements", "output_artifacts",
        ),
        "transfer plan",
    )
    if data["operator"] not in TRANSFER_OPERATORS:
        raise DistillationValidationError("invalid transfer operator")
    if data["execution_status"] != "PLANNED_NOT_EXECUTED" or data["output_artifacts"]:
        raise DistillationValidationError("prepared transfer plans may not contain executed outputs")
    _list(data["preconditions"], "preconditions", nonempty=True)
    _list(data["stable_grammar_to_preserve"], "stable_grammar_to_preserve", nonempty=True)
    _object(data["expected_anchor_dependence_test"], "expected_anchor_dependence_test")
    _list(data["technical_correctness_gates"], "technical_correctness_gates", nonempty=True)
    _list(data["human_aesthetic_review_axes"], "human_aesthetic_review_axes", nonempty=True)
    _object(data["absolute_quality_floor"], "absolute_quality_floor")
    provenance = _object(data["renderer_provenance_requirements"], "renderer_provenance_requirements")
    _required(
        provenance,
        ("renderer", "model", "model_version", "parameters", "actual_attachments", "final_invocation_evidence"),
        "renderer provenance",
    )
    return data


def build_runtime_package(
    program: dict[str, Any],
    *,
    current_content_assets: list[dict[str, Any]],
    active_mechanisms: list[dict[str, Any]],
    semantic_contract: dict[str, Any] | None,
    copy_constraints: list[str],
    brand_constraints: list[str],
) -> dict[str, Any]:
    """Build a bounded downstream package from a reviewed visual program."""
    validate_visual_program(program)
    if program["status"] not in {"PROVISIONAL_VISUAL_PROGRAM", "VALIDATED_VISUAL_PROGRAM"}:
        raise DistillationValidationError("runtime requires a provisional or validated visual program")
    if len(active_mechanisms) > 8:
        raise DistillationValidationError("active runtime mechanisms hard max is 8")
    golden = list(program["golden_exemplars"][:2])
    blockers = list(program["generic_shortcut_blockers"][:3])
    package = {
        "package_version": "3.0.0",
        "program_id": program["program_id"],
        "family_id": program["family_id"],
        "mother_reference": program["mother_reference"],
        "golden_exemplars": golden,
        "current_content_assets": list(current_content_assets),
        "visual_philosophy": program["visual_philosophy"],
        "active_mechanisms": list(active_mechanisms),
        "generic_shortcut_blockers": blockers,
        "semantic_contract": semantic_contract,
        "copy_constraints": list(copy_constraints),
        "brand_constraints": list(brand_constraints),
        "freedoms": list(program["freedoms"]),
        "renderer_provenance_requirements": program["renderer_provenance_requirements"],
        "source_evidence_lineage": list(program["evidence_lineage"]),
    }
    if "deep_evidence" in package or "analysis" in package:
        raise AssertionError("runtime package leaked deep evidence")
    return package


def build_validation_receipt(
    *,
    artifact_id: str,
    technical_checks: dict[str, Any],
    human_pixel_review: dict[str, Any] | None,
    relative_gain: bool,
) -> dict[str, Any]:
    technical = _object(technical_checks, "technical_checks")
    if human_pixel_review is None:
        decision = "HUMAN_PIXEL_REVIEW_PENDING"
    elif not human_pixel_review.get("absolute_usable", False):
        decision = "RELATIVE_GAIN / ABSOLUTE_FAIL" if relative_gain else "ABSOLUTE_FAIL"
    else:
        decision = "HUMAN_AESTHETIC_PASS"
    return {
        "artifact_id": artifact_id,
        "technical_correctness": technical,
        "human_aesthetic_judgment": human_pixel_review,
        "decision": decision,
        "codex_aesthetic_authority": False,
    }


def build_promotion_package(
    *,
    target: str,
    evidence_ids: list[str],
    transfer_evidence: list[dict[str, Any]],
    human_pixel_reviews: list[dict[str, Any]],
    explicit_user_approval: bool,
    provenance_complete: bool,
    unresolved_contradictions: list[dict[str, Any]],
) -> dict[str, Any]:
    """Prepare, but never execute, a skill-refiner handoff."""
    if not transfer_evidence:
        raise DistillationValidationError("promotion requires transfer evidence")
    if not human_pixel_reviews or any(not row.get("passed") for row in human_pixel_reviews):
        raise DistillationValidationError("promotion requires passing human pixel review")
    if not explicit_user_approval:
        raise DistillationValidationError("promotion requires explicit user approval")
    if not provenance_complete:
        raise DistillationValidationError("promotion requires complete provenance")
    if unresolved_contradictions:
        raise DistillationValidationError("promotion is blocked by unresolved contradictions")
    return {
        "target": target,
        "evidence_ids": list(evidence_ids),
        "transfer_evidence": list(transfer_evidence),
        "human_pixel_reviews": list(human_pixel_reviews),
        "explicit_user_approval": True,
        "provenance_complete": True,
        "unresolved_contradictions": [],
        "promotion_authority": "skill-refiner",
        "status": "READY_FOR_SKILL_REFINER_REVIEW",
        "durable_promotion_executed": False,
    }
