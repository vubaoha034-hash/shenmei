#!/usr/bin/env python3
"""Validate a restaurant brand project against the mandatory Figma-first gates.

Usage:
    python restaurant_design_system/scripts/validate_figma_first_project.py \
        restaurant_design_system/projects/<project-slug>

The validator is intentionally conservative: a claimed CONCEPT_SET fails when
required evidence is absent, ambiguous, or recorded under unsupported fields.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = (
    REPO_ROOT
    / "restaurant_design_system"
    / "config"
    / "figma-first-brand-gates.v1.json"
)


def load_json(path: Path, errors: list[str]) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"missing_json:{path.name}")
    except json.JSONDecodeError as exc:
        errors.append(f"invalid_json:{path.name}:{exc.msg}")
    return {}


def as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if value is None:
        return []
    return [value]


def get_first(mapping: dict[str, Any], *keys: str, default: Any = None) -> Any:
    for key in keys:
        if key in mapping:
            return mapping[key]
    return default


def truthy_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def extract_assets(manifest: Any) -> list[dict[str, Any]]:
    if isinstance(manifest, list):
        return [x for x in manifest if isinstance(x, dict)]
    if isinstance(manifest, dict):
        return [
            x
            for x in as_list(get_first(manifest, "assets", "items", default=[]))
            if isinstance(x, dict)
        ]
    return []


def extract_pages(figma: dict[str, Any], key: str) -> list[dict[str, Any]]:
    aliases = {
        "proof": ("three_page_proof", "proof_pages", "three_pages"),
        "ten": ("ten_page_portfolio", "portfolio_pages", "ten_pages"),
    }
    raw = get_first(figma, *aliases[key], default=[])
    return [x for x in as_list(raw) if isinstance(x, dict)]


def page_node_id(page: dict[str, Any]) -> Any:
    return get_first(page, "node_id", "figma_node_id", "frame_node_id")


def page_export(page: dict[str, Any]) -> Any:
    return get_first(page, "export_url", "export_path", "export", "output")


def page_brand_evidence(page: dict[str, Any]) -> Any:
    return get_first(page, "brand_evidence", "evidence")


def page_layout(page: dict[str, Any]) -> Any:
    return get_first(page, "layout_archetype", "layout")


def validate(project_dir: Path, config_path: Path) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    config = load_json(config_path, errors)
    required_files = config.get("required_project_files", [])
    for name in required_files:
        if not (project_dir / name).exists():
            errors.append(f"missing_required_file:{name}")

    project = load_json(project_dir / "PROJECT_RECORD.json", errors)
    delivery = load_json(project_dir / "delivery_manifest.json", errors)
    assets_manifest = load_json(project_dir / "ASSET_MANIFEST.json", errors)
    figma = load_json(project_dir / "FIGMA_MANIFEST.json", errors)
    aesthetic = load_json(project_dir / "AESTHETIC_EVALUATION.json", errors)

    status = get_first(project, "status", default=get_first(delivery, "status", default=""))
    allowed_statuses = config.get("statuses", {}).get("allowed", [])
    if status not in allowed_statuses:
        errors.append(f"invalid_or_missing_status:{status!r}")

    # Hard prohibition: image generators may create assets, not complete pages.
    full_page_flags = [
        get_first(project, "ai_full_page_used", "full_page_image_generation"),
        get_first(delivery, "ai_full_page_used", "full_page_image_generation"),
        get_first(figma, "imported_ai_full_pages", "ai_full_page_used"),
    ]
    if any(flag is True for flag in full_page_flags):
        errors.append("forbidden_ai_full_page_generation:true")

    assets = extract_assets(assets_manifest)
    for index, asset in enumerate(assets, start=1):
        if asset.get("selected") is False:
            continue
        if asset.get("text_present") is True:
            errors.append(f"asset_{index}:generated_text_present")
        if asset.get("logo_present") is True:
            errors.append(f"asset_{index}:generated_logo_present")
        result = str(get_first(asset, "audit_result", "status", default="")).upper()
        if result.startswith("REJECTED"):
            errors.append(f"asset_{index}:selected_rejected_asset:{result}")

    figma_url = get_first(figma, "file_url", "figma_file_url")
    figma_key = get_first(figma, "file_key", "figma_file_key")
    if not truthy_string(figma_url):
        errors.append("figma_missing_file_url")
    if not truthy_string(figma_key):
        errors.append("figma_missing_file_key")

    proof_pages = extract_pages(figma, "proof")
    proof_gate = config.get("three_page_gate", {})
    required_proof_count = int(proof_gate.get("required_page_count", 3))
    if len(proof_pages) != required_proof_count:
        errors.append(f"figma_proof_page_count:{len(proof_pages)}!=3")
    for idx, page in enumerate(proof_pages, start=1):
        if not truthy_string(page_node_id(page)):
            errors.append(f"proof_page_{idx}:missing_node_id")

    proof_eval = get_first(aesthetic, "three_page_gate", "three_page_proof", "proof", default={})
    if not isinstance(proof_eval, dict):
        proof_eval = {}
    proof_total = get_first(proof_eval, "total_score", "score")
    minimum_total = float(proof_gate.get("minimum_total_score", 78))
    if not isinstance(proof_total, (int, float)):
        errors.append("aesthetic_proof:missing_total_score")
    elif proof_total < minimum_total:
        errors.append(f"aesthetic_proof:total_score:{proof_total}<{minimum_total}")

    dimensions = get_first(proof_eval, "dimensions", "dimension_scores", default={})
    if not isinstance(dimensions, dict):
        dimensions = {}
    for dim, minimum in proof_gate.get("minimum_dimension_scores", {}).items():
        value = dimensions.get(dim)
        if not isinstance(value, (int, float)):
            errors.append(f"aesthetic_proof:missing_dimension:{dim}")
        elif value < minimum:
            errors.append(f"aesthetic_proof:{dim}:{value}<{minimum}")

    if status in {"THREE_PAGE_PROOF_PASS", "TEN_PAGE_LAYOUT", "CONCEPT_SET", "DESIGN_DEVELOPMENT", "READY_TO_POST_SET", "PRODUCTION_READY"}:
        proof_status = str(get_first(proof_eval, "status", "gate_status", default=""))
        if proof_status not in {"PASS", "THREE_PAGE_PROOF_PASS"}:
            errors.append(f"aesthetic_proof:not_passed:{proof_status!r}")

    if status in {"CONCEPT_SET", "DESIGN_DEVELOPMENT", "READY_TO_POST_SET", "PRODUCTION_READY"}:
        ten_gate = config.get("ten_page_gate", {})
        ten_pages = extract_pages(figma, "ten")
        required_ten_count = int(ten_gate.get("required_page_count", 10))
        if len(ten_pages) != required_ten_count:
            errors.append(f"figma_ten_page_count:{len(ten_pages)}!=10")

        layouts: list[str] = []
        for idx, page in enumerate(ten_pages, start=1):
            if not truthy_string(page_node_id(page)):
                errors.append(f"portfolio_page_{idx}:missing_node_id")
            if not truthy_string(page_export(page)):
                errors.append(f"portfolio_page_{idx}:missing_export")
            if not truthy_string(page_brand_evidence(page)):
                errors.append(f"portfolio_page_{idx}:missing_brand_evidence")
            layout = page_layout(page)
            if truthy_string(layout):
                layouts.append(str(layout))
            else:
                errors.append(f"portfolio_page_{idx}:missing_layout_archetype")
            page_status = str(get_first(page, "status", default="")).upper()
            if "REJECTED" in page_status:
                errors.append(f"portfolio_page_{idx}:rejected:{page_status}")

        distinct_layouts = len(set(layouts))
        minimum_layouts = int(ten_gate.get("minimum_layout_archetypes", 4))
        if distinct_layouts < minimum_layouts:
            errors.append(f"portfolio_layout_archetypes:{distinct_layouts}<{minimum_layouts}")

        max_consecutive = int(ten_gate.get("maximum_consecutive_same_layout", 2))
        run = 0
        previous = None
        for layout in layouts:
            run = run + 1 if layout == previous else 1
            previous = layout
            if run > max_consecutive:
                errors.append(f"portfolio_layout_repetition:{layout}:run={run}")
                break

        final_eval = get_first(aesthetic, "ten_page_gate", "ten_page_portfolio", "final", default={})
        if not isinstance(final_eval, dict):
            final_eval = {}
        average = get_first(final_eval, "average_score", "score")
        minimum_average = float(ten_gate.get("minimum_average_score", 80))
        if not isinstance(average, (int, float)):
            errors.append("aesthetic_ten_page:missing_average_score")
        elif average < minimum_average:
            errors.append(f"aesthetic_ten_page:average:{average}<{minimum_average}")

        page_scores = get_first(final_eval, "page_scores", "pages", default=[])
        score_map: dict[int, float] = {}
        if isinstance(page_scores, dict):
            for key, value in page_scores.items():
                try:
                    score_map[int(key)] = float(value)
                except (TypeError, ValueError):
                    continue
        elif isinstance(page_scores, list):
            for item in page_scores:
                if not isinstance(item, dict):
                    continue
                number = get_first(item, "page", "index", "number")
                score = get_first(item, "score", "total_score")
                if isinstance(number, int) and isinstance(score, (int, float)):
                    score_map[number] = float(score)

        minimum_key = float(ten_gate.get("minimum_key_page_score", 75))
        for page_number in ten_gate.get("key_pages", []):
            score = score_map.get(int(page_number))
            if score is None:
                errors.append(f"aesthetic_ten_page:key_page_{page_number}:missing_score")
            elif score < minimum_key:
                errors.append(f"aesthetic_ten_page:key_page_{page_number}:{score}<{minimum_key}")

    if not assets:
        warnings.append("asset_manifest_contains_no_assets")

    result = {
        "validator_version": "1.0.0",
        "project_dir": str(project_dir),
        "project_status": status,
        "result": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_dir", type=Path)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    args = parser.parse_args()

    project_dir = args.project_dir.resolve()
    config_path = args.config.resolve()
    result = validate(project_dir, config_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["result"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
