#!/usr/bin/env python3
"""Validate shenmei aesthetic-evaluation records without external dependencies."""
from __future__ import annotations

import argparse
import json
import math
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Any

TOLERANCE = 0.11


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def round_nearest_five(value: float) -> int:
    return int((Decimal(str(value)) / Decimal("5")).quantize(Decimal("1"), rounding=ROUND_HALF_UP) * 5)


def close(a: Any, b: float, tol: float = TOLERANCE) -> bool:
    try:
        return abs(float(a) - b) <= tol
    except (TypeError, ValueError):
        return False


def score_increment_ok(value: Any, increment: int) -> bool:
    return isinstance(value, int) and 0 <= value <= 100 and value % increment == 0


def band_for(score: float, bands: list[dict[str, Any]]) -> str:
    for band in bands:
        if float(band["min"]) <= score <= float(band["max"]) + 1e-9:
            return str(band["label"])
    raise ValueError(f"No band configured for score {score}")


def validate_dimension_set(
    label: str,
    dimensions: Any,
    rubric_dims: dict[str, Any],
    increment: int,
    anchors_count: int,
    errors: list[str],
) -> float:
    if not isinstance(dimensions, dict):
        errors.append(f"{label}.dimensions must be an object")
        return 0.0

    expected = set(rubric_dims)
    actual = set(dimensions)
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing:
        errors.append(f"{label} missing dimensions: {', '.join(missing)}")
    if extra:
        errors.append(f"{label} has unknown dimensions: {', '.join(extra)}")

    numerator = 0.0
    denominator = 0.0
    for name, spec in rubric_dims.items():
        result = dimensions.get(name)
        if not isinstance(result, dict):
            continue
        score = result.get("score")
        requires_anchors = bool(spec.get("requires_anchors"))
        if score is None:
            if not requires_anchors:
                errors.append(f"{label}.{name}.score may not be null")
            elif anchors_count >= 3:
                errors.append(f"{label}.{name}.score is null although at least 3 anchors are declared")
            continue
        if requires_anchors and anchors_count < 3:
            errors.append(f"{label}.{name} must be null when fewer than 3 anchors are used")
        if not score_increment_ok(score, increment):
            errors.append(f"{label}.{name}.score must be 0-100 in increments of {increment}")
            continue
        evidence = result.get("evidence")
        min_evidence = int(spec.get("min_evidence", 1))
        if not isinstance(evidence, list) or len(evidence) < min_evidence:
            errors.append(f"{label}.{name} needs at least {min_evidence} evidence items")
        elif any(not isinstance(item, str) or len(item.strip()) < 8 for item in evidence):
            errors.append(f"{label}.{name} contains vague/empty evidence")
        reasoning = result.get("reasoning")
        if not isinstance(reasoning, str) or len(reasoning.strip()) < 8:
            errors.append(f"{label}.{name}.reasoning is too short")
        if result.get("uncertainty") not in {"low", "medium", "high"}:
            errors.append(f"{label}.{name}.uncertainty is invalid")
        weight = float(spec["weight"])
        numerator += float(score) * weight
        denominator += weight

    if denominator <= 0:
        errors.append(f"{label} has no scorable dimensions")
        return 0.0
    return numerator / denominator


def expected_confidence(record: dict[str, Any], anchors_count: int) -> float:
    inp = record.get("input", {})
    confidence = 0.95
    width = inp.get("width_px")
    height = inp.get("height_px")
    long_edge = max(width, height) if isinstance(width, int) and isinstance(height, int) else None
    if long_edge is None:
        confidence -= 0.15
    elif long_edge < 640:
        confidence -= 0.20
    elif long_edge < 1200:
        confidence -= 0.15
    if not inp.get("brief_present", False):
        confidence -= 0.10
    if inp.get("reference_required", False) and not inp.get("reference_present", False):
        confidence -= 0.15
    if inp.get("critical_occlusion", False):
        confidence -= 0.08
    if anchors_count < 3:
        confidence -= 0.08
    if inp.get("text_check_required", False) and not inp.get("text_readable", False):
        confidence -= 0.05
    if inp.get("strong_compression", False):
        confidence -= 0.05
    return round(min(0.95, max(0.35, confidence)), 2)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a shenmei evaluation JSON record")
    parser.add_argument("evaluation", type=Path)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    try:
        record = load_json(args.evaluation)
        rubric = load_json(args.repo_root / "config" / "rubric.v1.json")
        penalty_cfg = load_json(args.repo_root / "config" / "penalties.v1.json")
        anchors_cfg = load_json(args.repo_root / "calibration" / "anchors.json")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL\n- {exc}")
        return 1

    if record.get("rubric_version") != rubric.get("rubric_version"):
        errors.append("rubric_version does not match config/rubric.v1.json")
    if record.get("penalty_version") != penalty_cfg.get("penalty_version"):
        errors.append("penalty_version does not match config/penalties.v1.json")

    category = record.get("category")
    categories = rubric.get("categories", {})
    if category not in categories:
        errors.append(f"unknown category: {category!r}")
        category_cfg = {"dimensions": {}}
    else:
        category_cfg = categories[category]
    rubric_dims = category_cfg.get("dimensions", {})
    if rubric_dims and not math.isclose(sum(float(v["weight"]) for v in rubric_dims.values()), 100.0, abs_tol=1e-9):
        errors.append(f"configured weights for {category} do not sum to 100")

    all_anchors = anchors_cfg.get("anchors", [])
    anchor_index = {
        a.get("id"): a
        for a in all_anchors
        if isinstance(a, dict) and a.get("id") and a.get("active", True)
    }
    anchors_used = record.get("anchors_used", [])
    if not isinstance(anchors_used, list) or len(set(anchors_used)) != len(anchors_used):
        errors.append("anchors_used must be a unique list")
        anchors_used = []
    for anchor_id in anchors_used:
        anchor = anchor_index.get(anchor_id)
        if anchor is None:
            errors.append(f"unknown or inactive anchor: {anchor_id}")
        elif anchor.get("category") != category:
            errors.append(f"anchor {anchor_id} belongs to another category")
    anchors_count = len(anchors_used)

    evidence_inventory = record.get("evidence_inventory")
    if not isinstance(evidence_inventory, dict) or len(evidence_inventory) < 4:
        errors.append("evidence_inventory must contain at least four evidence sections")
    elif any(not isinstance(items, list) or not items for items in evidence_inventory.values()):
        errors.append("every evidence_inventory section must contain evidence")

    passes = record.get("passes", {})
    pass_a = passes.get("A", {}).get("dimensions") if isinstance(passes, dict) else None
    pass_b = passes.get("B", {}).get("dimensions") if isinstance(passes, dict) else None
    increment = int(rubric.get("score_increment", 5))
    pass_a_score = validate_dimension_set("passes.A", pass_a, rubric_dims, increment, anchors_count, errors)
    pass_b_score = validate_dimension_set("passes.B", pass_b, rubric_dims, increment, anchors_count, errors)

    trigger_total = float(rubric["adjudication"]["total_score_difference_trigger"])
    trigger_dim = int(rubric["adjudication"]["dimension_score_difference_trigger"])
    disputed: list[str] = []
    for name in rubric_dims:
        a = pass_a.get(name, {}).get("score") if isinstance(pass_a, dict) else None
        b = pass_b.get(name, {}).get("score") if isinstance(pass_b, dict) else None
        if isinstance(a, int) and isinstance(b, int) and abs(a - b) > trigger_dim:
            disputed.append(name)
    adjudication_needed = abs(pass_a_score - pass_b_score) > trigger_total or bool(disputed)
    adjudication = record.get("adjudication", {})
    if not isinstance(adjudication, dict):
        errors.append("adjudication must be an object")
        adjudication = {}
    if adjudication.get("required") is not adjudication_needed:
        errors.append(f"adjudication.required should be {adjudication_needed}")
    if adjudication_needed and not adjudication.get("performed", False):
        errors.append("adjudication was required but not performed")
    declared_disputed = set(adjudication.get("disputed_dimensions", []))
    if not set(disputed).issubset(declared_disputed):
        errors.append("adjudication.disputed_dimensions omits triggered dimensions")

    final_dims = record.get("final_dimensions")
    final_score_weighted = validate_dimension_set("final_dimensions", final_dims, rubric_dims, increment, anchors_count, errors)
    if isinstance(final_dims, dict) and isinstance(pass_a, dict) and isinstance(pass_b, dict):
        for name in rubric_dims:
            a = pass_a.get(name, {}).get("score")
            b = pass_b.get(name, {}).get("score")
            final = final_dims.get(name, {}).get("score")
            if not adjudication_needed:
                expected = None if a is None and b is None else round_nearest_five((a + b) / 2)
                if final != expected:
                    errors.append(f"final_dimensions.{name}.score should be {expected} without adjudication")

    applied_penalties = record.get("penalties", [])
    if not isinstance(applied_penalties, list):
        errors.append("penalties must be a list")
        applied_penalties = []
    penalty_total = 0.0
    caps: list[float] = []
    seen_penalties: set[str] = set()
    for idx, item in enumerate(applied_penalties):
        prefix = f"penalties[{idx}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue
        penalty_id = item.get("id")
        if penalty_id in seen_penalties:
            errors.append(f"duplicate penalty id: {penalty_id}")
        seen_penalties.add(penalty_id)
        rule = penalty_cfg.get("rules", {}).get(penalty_id)
        if rule is None:
            errors.append(f"unknown penalty id: {penalty_id}")
            continue
        if category not in rule.get("applies_to", []):
            errors.append(f"penalty {penalty_id} does not apply to {category}")
        points = item.get("points")
        if not isinstance(points, (int, float)) or not (float(rule["min_points"]) <= float(points) <= float(rule["max_points"])):
            errors.append(f"{prefix}.points outside configured range")
        else:
            penalty_total += float(points)
        evidence = item.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            errors.append(f"{prefix} requires visible evidence")
        reason = item.get("non_duplicate_reason")
        if not isinstance(reason, str) or len(reason.strip()) < 8:
            errors.append(f"{prefix}.non_duplicate_reason is too short")
        cap = rule.get("score_cap")
        if cap is not None:
            caps.append(float(cap))

    active_cap = min(caps) if caps else None
    expected_final = max(0.0, final_score_weighted - penalty_total)
    if active_cap is not None:
        expected_final = min(expected_final, active_cap)
    expected_final = round(expected_final, 1)
    expected_band = band_for(expected_final, rubric.get("bands", []))

    scores = record.get("scores", {})
    if not isinstance(scores, dict):
        errors.append("scores must be an object")
        scores = {}
    checks = {
        "pass_a_weighted": pass_a_score,
        "pass_b_weighted": pass_b_score,
        "weighted_before_penalties": final_score_weighted,
        "penalty_total": penalty_total,
        "final_score": expected_final,
    }
    for field, expected in checks.items():
        if not close(scores.get(field), expected):
            errors.append(f"scores.{field} should be {round(expected, 2)}")
    if active_cap is None:
        if scores.get("active_cap") is not None:
            errors.append("scores.active_cap should be null")
    elif not close(scores.get("active_cap"), active_cap):
        errors.append(f"scores.active_cap should be {active_cap}")
    if scores.get("band") != expected_band:
        errors.append(f"scores.band should be {expected_band}")

    confidence = expected_confidence(record, anchors_count)
    if not close(record.get("confidence"), confidence, tol=0.011):
        errors.append(f"confidence should be {confidence}")

    inp = record.get("input", {})
    width = inp.get("width_px") if isinstance(inp, dict) else None
    height = inp.get("height_px") if isinstance(inp, dict) else None
    long_edge = max(width, height) if isinstance(width, int) and isinstance(height, int) else None
    if record.get("status") == "OFFICIAL":
        if long_edge is None or long_edge < 640:
            errors.append("OFFICIAL score forbidden when image size is unknown or long edge is below 640 px")
        if inp.get("reference_required", False) and not inp.get("reference_present", False):
            errors.append("OFFICIAL reference-match score forbidden without reference image")
        if inp.get("critical_occlusion", False):
            warnings.append("critical_occlusion is true; confirm core criteria remain visible")
    elif record.get("status") not in {"DRAFT", "NO_SCORE"}:
        errors.append("status must be OFFICIAL, DRAFT, or NO_SCORE")

    if expected_final >= 90 and rubric_dims and isinstance(final_dims, dict):
        active_scores = {
            name: final_dims.get(name, {}).get("score")
            for name in rubric_dims
            if final_dims.get(name, {}).get("score") is not None
        }
        high_weight_below_85 = [
            name for name, score in active_scores.items()
            if float(rubric_dims[name]["weight"]) >= 10 and score < 85
        ]
        weight_at_90 = sum(
            float(rubric_dims[name]["weight"])
            for name, score in active_scores.items() if score >= 90
        )
        active_weight = sum(float(rubric_dims[name]["weight"]) for name in active_scores)
        if high_weight_below_85:
            errors.append("90+ gate failed: high-weight dimension below 85")
        if active_weight and weight_at_90 < active_weight / 2:
            errors.append("90+ gate failed: less than half of active weight is scored 90+")
        if active_cap is not None and active_cap < 90:
            errors.append("90+ gate failed: active cap below 90")

    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        for warning in warnings:
            print(f"! {warning}")
        return 1

    print("PASS")
    print(json.dumps({
        "status": record.get("status"),
        "category": category,
        "pass_a_weighted": round(pass_a_score, 2),
        "pass_b_weighted": round(pass_b_score, 2),
        "weighted_before_penalties": round(final_score_weighted, 2),
        "penalty_total": round(penalty_total, 2),
        "active_cap": active_cap,
        "final_score": expected_final,
        "band": expected_band,
        "confidence": confidence,
        "adjudication_required": adjudication_needed
    }, ensure_ascii=False, indent=2))
    for warning in warnings:
        print(f"! {warning}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
