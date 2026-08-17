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
    return data


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
