#!/usr/bin/env python3
"""Compare repeated official evaluations and reject unstable AI scoring."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def load(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain an object")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare two shenmei evaluation records")
    parser.add_argument("first", type=Path)
    parser.add_argument("second", type=Path)
    parser.add_argument("--score-tolerance", type=float, default=3.0)
    parser.add_argument("--dimension-tolerance", type=float, default=5.0)
    args = parser.parse_args()

    try:
        first = load(args.first)
        second = load(args.second)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL\n- {exc}")
        return 1

    errors: list[str] = []
    warnings: list[str] = []

    first_id = first.get("input", {}).get("input_id")
    second_id = second.get("input", {}).get("input_id")
    first_hash = first.get("input", {}).get("file_sha256")
    second_hash = second.get("input", {}).get("file_sha256")
    if first_hash and second_hash:
        if first_hash != second_hash:
            errors.append("file_sha256 differs; these are not the same input")
    elif first_id != second_id:
        errors.append("input_id differs and no matching file hash is available")
    else:
        warnings.append("comparison relies on input_id because file_sha256 is absent")

    if first.get("category") != second.get("category"):
        errors.append("category changed between repeated evaluations")
    if first.get("rubric_version") != second.get("rubric_version"):
        errors.append("rubric_version changed; scores are not directly comparable")
    if first.get("penalty_version") != second.get("penalty_version"):
        errors.append("penalty_version changed; scores are not directly comparable")

    score_1 = first.get("scores", {}).get("final_score")
    score_2 = second.get("scores", {}).get("final_score")
    if not isinstance(score_1, (int, float)) or not isinstance(score_2, (int, float)):
        errors.append("both records need numeric final_score values")
    elif abs(float(score_1) - float(score_2)) > args.score_tolerance:
        errors.append(
            f"final_score drift is {abs(float(score_1) - float(score_2)):.1f}, "
            f"above tolerance {args.score_tolerance:.1f}"
        )

    dims_1 = first.get("final_dimensions", {})
    dims_2 = second.get("final_dimensions", {})
    if set(dims_1) != set(dims_2):
        errors.append("dimension sets differ")
    for name in sorted(set(dims_1) & set(dims_2)):
        value_1 = dims_1[name].get("score") if isinstance(dims_1[name], dict) else None
        value_2 = dims_2[name].get("score") if isinstance(dims_2[name], dict) else None
        if value_1 is None and value_2 is None:
            continue
        if not isinstance(value_1, (int, float)) or not isinstance(value_2, (int, float)):
            errors.append(f"dimension {name} changed between scored and null")
            continue
        difference = abs(float(value_1) - float(value_2))
        if difference > args.dimension_tolerance:
            errors.append(
                f"dimension {name} drift is {difference:.1f}, "
                f"above tolerance {args.dimension_tolerance:.1f}"
            )

    penalty_ids_1 = sorted(item.get("id") for item in first.get("penalties", []) if isinstance(item, dict))
    penalty_ids_2 = sorted(item.get("id") for item in second.get("penalties", []) if isinstance(item, dict))
    if penalty_ids_1 != penalty_ids_2:
        errors.append("penalty set changed between repeated evaluations")

    anchors_1 = sorted(first.get("anchors_used", []))
    anchors_2 = sorted(second.get("anchors_used", []))
    if anchors_1 != anchors_2:
        errors.append("anchor set changed; repeatability comparison is invalid")

    if first.get("scores", {}).get("band") != second.get("scores", {}).get("band"):
        warnings.append("rating band changed even though the score may be within tolerance")

    if errors:
        print("FAIL")
        for item in errors:
            print(f"- {item}")
        for item in warnings:
            print(f"! {item}")
        return 1

    print("PASS")
    print(json.dumps({
        "input_id": first_id,
        "score_1": score_1,
        "score_2": score_2,
        "score_drift": round(abs(float(score_1) - float(score_2)), 2),
        "score_tolerance": args.score_tolerance,
        "dimension_tolerance": args.dimension_tolerance,
        "same_penalties": True,
        "same_anchors": True
    }, ensure_ascii=False, indent=2))
    for item in warnings:
        print(f"! {item}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
