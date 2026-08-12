"""Deterministic validation for LIU VISUAL SYSTEM V0.1 raw records.

The repository publishes JSON Schemas for interoperability, but runtime
validation deliberately uses only the Python standard library so the scaffold
has no third-party dependency.
"""
from __future__ import annotations

import re
from typing import Any

SCHEMA_VERSION = "1"
_ID_PATTERNS = {
    "sample": re.compile(r"^smp_[0-9a-f-]{32,36}$"),
    "asset": re.compile(r"^ast_[0-9a-f-]{32,36}$"),
    "event": re.compile(r"^ev_[0-9a-f-]{32,36}$"),
    "generation": re.compile(r"^gen_[0-9a-f-]{32,36}$"),
}

SAMPLE_KINDS = {"reference", "generated", "imported"}
DATASET_ROLES = {"discovery", "blind_eval_reserved", "production", "unassigned"}
SOURCE_TYPES = {"user_upload", "web", "repo", "generated", "unknown"}
LOCATOR_KINDS = {"repo_relative", "local_file", "remote_url", "opaque"}
ASSET_RELATIONS = {"primary", "alternate", "derivative"}
EVENT_TYPES = {"feedback", "comparison", "revision", "correction", "tombstone"}
EVIDENCE_SOURCE_KINDS = {"user", "imported_user_evidence"}
SCOPE_LEVELS = {"task", "domain", "global_explicit", "unspecified"}
VERDICTS = {"approved", "rejected", "neutral", None}
WINNERS = {"left", "right", "tie", "unclear"}
COMPARISON_KINDS = {"natural", "controlled"}
CAUSAL_ATTRIBUTION = {"user_stated", "controlled", "unknown"}
CORRECTION_EFFECTS = {"supersede", "retract", "clarify"}


class RecordValidationError(ValueError):
    """Raised when a raw record violates the frozen V0.1 contract."""


def _require_obj(record: Any) -> dict[str, Any]:
    if not isinstance(record, dict):
        raise RecordValidationError("record must be a JSON object")
    return record


def _require(record: dict[str, Any], *fields: str) -> None:
    missing = [field for field in fields if field not in record]
    if missing:
        raise RecordValidationError(f"missing required fields: {', '.join(missing)}")


def _string(value: Any, field: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str):
        raise RecordValidationError(f"{field} must be a string")
    if not allow_empty and not value.strip():
        raise RecordValidationError(f"{field} may not be empty")
    return value


def _id(value: Any, kind: str, field: str) -> str:
    text = _string(value, field)
    if not _ID_PATTERNS[kind].match(text):
        raise RecordValidationError(f"{field} is not a valid {kind} id")
    return text


def _id_list(value: Any, kind: str, field: str) -> list[str]:
    if not isinstance(value, list):
        raise RecordValidationError(f"{field} must be a list")
    out = [_id(item, kind, field) for item in value]
    if len(out) != len(set(out)):
        raise RecordValidationError(f"{field} contains duplicates")
    return out


def _no_extra(record: dict[str, Any], allowed: set[str], label: str) -> None:
    extra = sorted(set(record) - allowed)
    if extra:
        raise RecordValidationError(f"{label} has unknown fields: {', '.join(extra)}")


def _schema_version(record: dict[str, Any]) -> None:
    if record.get("schema_version") != SCHEMA_VERSION:
        raise RecordValidationError(f"schema_version must be {SCHEMA_VERSION!r}")


def validate_sample(record: Any) -> dict[str, Any]:
    r = _require_obj(record)
    _require(r, "schema_version", "sample_id", "created_at", "sample_kind", "primary_asset_id", "dataset_role", "provenance")
    _no_extra(r, {"schema_version", "sample_id", "created_at", "sample_kind", "primary_asset_id", "dataset_role", "provenance", "user_tags"}, "SampleRecord")
    _schema_version(r)
    _id(r["sample_id"], "sample", "sample_id")
    _string(r["created_at"], "created_at")
    if r["sample_kind"] not in SAMPLE_KINDS:
        raise RecordValidationError("sample_kind is invalid")
    _id(r["primary_asset_id"], "asset", "primary_asset_id")
    if r["dataset_role"] not in DATASET_ROLES:
        raise RecordValidationError("dataset_role is invalid")
    provenance = _require_obj(r["provenance"])
    _require(provenance, "source_type")
    _no_extra(provenance, {"source_type", "source_ref", "creator", "license"}, "SampleRecord.provenance")
    if provenance["source_type"] not in SOURCE_TYPES:
        raise RecordValidationError("provenance.source_type is invalid")
    for key in ("source_ref", "creator", "license"):
        if key in provenance and provenance[key] is not None and not isinstance(provenance[key], str):
            raise RecordValidationError(f"provenance.{key} must be string or null")
    tags = r.get("user_tags", [])
    if not isinstance(tags, list) or any(not isinstance(tag, str) for tag in tags):
        raise RecordValidationError("user_tags must be a list of strings")
    return r


def validate_asset(record: Any) -> dict[str, Any]:
    r = _require_obj(record)
    _require(r, "schema_version", "asset_id", "sample_id", "created_at", "sha256", "locator_kind", "locator", "asset_relation")
    _no_extra(r, {"schema_version", "asset_id", "sample_id", "created_at", "sha256", "locator_kind", "locator", "asset_relation", "derived_from_asset_id", "media_type"}, "AssetRecord")
    _schema_version(r)
    _id(r["asset_id"], "asset", "asset_id")
    _id(r["sample_id"], "sample", "sample_id")
    _string(r["created_at"], "created_at")
    digest = _string(r["sha256"], "sha256")
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", digest):
        raise RecordValidationError("sha256 must be 'sha256:' followed by 64 lowercase hex characters")
    if r["locator_kind"] not in LOCATOR_KINDS:
        raise RecordValidationError("locator_kind is invalid")
    _string(r["locator"], "locator")
    if r["asset_relation"] not in ASSET_RELATIONS:
        raise RecordValidationError("asset_relation is invalid")
    parent = r.get("derived_from_asset_id")
    if parent is not None:
        _id(parent, "asset", "derived_from_asset_id")
    media_type = r.get("media_type")
    if media_type is not None:
        _string(media_type, "media_type")
    return r


def validate_generation(record: Any) -> dict[str, Any]:
    r = _require_obj(record)
    _require(r, "schema_version", "generation_id", "created_at", "renderer", "model", "reference_sample_ids", "output_sample_ids", "parameters")
    _no_extra(r, {"schema_version", "generation_id", "created_at", "renderer", "model", "model_version", "task_ref", "reference_sample_ids", "parent_generation_id", "output_sample_ids", "prompt_text", "parameters"}, "GenerationRecord")
    _schema_version(r)
    _id(r["generation_id"], "generation", "generation_id")
    _string(r["created_at"], "created_at")
    _string(r["renderer"], "renderer")
    _string(r["model"], "model")
    if r.get("model_version") is not None:
        _string(r["model_version"], "model_version")
    if r.get("task_ref") is not None:
        _string(r["task_ref"], "task_ref")
    _id_list(r["reference_sample_ids"], "sample", "reference_sample_ids")
    _id_list(r["output_sample_ids"], "sample", "output_sample_ids")
    parent = r.get("parent_generation_id")
    if parent is not None:
        _id(parent, "generation", "parent_generation_id")
    if r.get("prompt_text") is not None and not isinstance(r["prompt_text"], str):
        raise RecordValidationError("prompt_text must be string or null")
    if not isinstance(r["parameters"], dict):
        raise RecordValidationError("parameters must be an object")
    return r


def validate_evidence(record: Any) -> dict[str, Any]:
    r = _require_obj(record)
    _require(
        r,
        "schema_version",
        "event_id",
        "occurred_at",
        "event_type",
        "source_kind",
        "scope",
        "raw_text",
        "target_sample_ids",
        "target_generation_ids",
        "payload",
    )
    _no_extra(r, {"schema_version", "event_id", "occurred_at", "event_type", "source_kind", "source_ref", "scope", "raw_text", "target_sample_ids", "target_generation_ids", "payload"}, "EvidenceEvent")
    _schema_version(r)
    _id(r["event_id"], "event", "event_id")
    _string(r["occurred_at"], "occurred_at")
    if r["event_type"] not in EVENT_TYPES:
        raise RecordValidationError("event_type is invalid")
    if r["source_kind"] not in EVIDENCE_SOURCE_KINDS:
        raise RecordValidationError("source_kind must be direct or faithfully imported user evidence")
    if r.get("source_ref") is not None:
        _string(r["source_ref"], "source_ref")
    if r["source_kind"] == "imported_user_evidence" and not r.get("source_ref"):
        raise RecordValidationError("imported_user_evidence requires traceable source_ref")
    scope = _require_obj(r["scope"])
    _require(scope, "level")
    _no_extra(scope, {"level", "domain"}, "EvidenceEvent.scope")
    if scope["level"] not in SCOPE_LEVELS:
        raise RecordValidationError("scope.level is invalid")
    if scope["level"] == "domain":
        _string(scope.get("domain"), "scope.domain")
    elif scope.get("domain") is not None and not isinstance(scope.get("domain"), str):
        raise RecordValidationError("scope.domain must be string or null")
    raw_text = r["raw_text"]
    if not isinstance(raw_text, str):
        raise RecordValidationError("raw_text must be a string")
    _id_list(r["target_sample_ids"], "sample", "target_sample_ids")
    _id_list(r["target_generation_ids"], "generation", "target_generation_ids")
    payload = _require_obj(r["payload"])

    et = r["event_type"]
    if et == "feedback":
        _no_extra(payload, {"explicit_verdict"}, "feedback.payload")
        if payload.get("explicit_verdict") not in VERDICTS:
            raise RecordValidationError("feedback.explicit_verdict is invalid")
    elif et == "comparison":
        _no_extra(payload, {"left_sample_id", "right_sample_id", "winner", "comparison_kind"}, "comparison.payload")
        _require(payload, "left_sample_id", "right_sample_id", "winner", "comparison_kind")
        left = _id(payload["left_sample_id"], "sample", "payload.left_sample_id")
        right = _id(payload["right_sample_id"], "sample", "payload.right_sample_id")
        if left == right:
            raise RecordValidationError("comparison samples must differ")
        if payload["winner"] not in WINNERS:
            raise RecordValidationError("comparison.winner is invalid")
        if payload["comparison_kind"] not in COMPARISON_KINDS:
            raise RecordValidationError("comparison.comparison_kind is invalid")
    elif et == "revision":
        _no_extra(payload, {"before_sample_id", "after_sample_id", "requested_change_text", "result_feedback_event_id", "causal_attribution"}, "revision.payload")
        _require(payload, "before_sample_id", "after_sample_id", "requested_change_text", "causal_attribution")
        before = _id(payload["before_sample_id"], "sample", "payload.before_sample_id")
        after = _id(payload["after_sample_id"], "sample", "payload.after_sample_id")
        if before == after:
            raise RecordValidationError("revision before and after samples must differ")
        _string(payload["requested_change_text"], "payload.requested_change_text")
        result_id = payload.get("result_feedback_event_id")
        if result_id is not None:
            _id(result_id, "event", "payload.result_feedback_event_id")
        if payload["causal_attribution"] not in CAUSAL_ATTRIBUTION:
            raise RecordValidationError("revision.causal_attribution is invalid")
    elif et == "correction":
        _no_extra(payload, {"target_event_ids", "effect"}, "correction.payload")
        _require(payload, "target_event_ids", "effect")
        if not _id_list(payload["target_event_ids"], "event", "payload.target_event_ids"):
            raise RecordValidationError("correction.target_event_ids may not be empty")
        if payload["effect"] not in CORRECTION_EFFECTS:
            raise RecordValidationError("correction.effect is invalid")
    elif et == "tombstone":
        _no_extra(payload, {"target_record_ids", "reason"}, "tombstone.payload")
        _require(payload, "target_record_ids", "reason")
        if not isinstance(payload["target_record_ids"], list) or not payload["target_record_ids"]:
            raise RecordValidationError("tombstone.target_record_ids must be a non-empty list")
        if any(not isinstance(item, str) or not item for item in payload["target_record_ids"]):
            raise RecordValidationError("tombstone.target_record_ids must contain ids")
        _string(payload["reason"], "payload.reason")

    if not raw_text and et not in {"comparison", "tombstone"}:
        raise RecordValidationError("raw_text may be empty only for structured comparison/tombstone events")
    return r


def validate_record(kind: str, record: Any) -> dict[str, Any]:
    validators = {
        "sample": validate_sample,
        "asset": validate_asset,
        "evidence": validate_evidence,
        "generation": validate_generation,
    }
    try:
        validator = validators[kind]
    except KeyError as exc:
        raise RecordValidationError(f"unknown record kind: {kind}") from exc
    return validator(record)
