#!/usr/bin/env python3
"""Validate the V3 typography distillation and Figma production layer."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from visual_memory.distillation_v3 import (
    build_typography_runtime_package,
    validate_figma_dry_run_receipt,
    validate_figma_production_contract,
    validate_mechanism,
    validate_typography_evidence,
    validate_typography_hypothesis,
    validate_visual_program,
)


def load(name: str) -> dict:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def main() -> None:
    pairs = []
    for suffix in ("05", "13"):
        evidence = load(f"V3_TYPOGRAPHY_EVIDENCE_REFERENCE_{suffix}.json")
        hypothesis = load(f"V3_TYPOGRAPHY_HYPOTHESIS_REFERENCE_{suffix}.json")
        contract = load(f"V3_FIGMA_PRODUCTION_CONTRACT_REFERENCE_{suffix}.json")
        program = load(f"V3_VISUAL_PROGRAM_REFERENCE_{suffix}_PROVISIONAL.json")
        validate_typography_evidence(evidence)
        validate_typography_hypothesis(hypothesis)
        validate_figma_production_contract(contract)
        validate_visual_program(program)
        runtime = build_typography_runtime_package(
            program,
            hypothesis,
            contract,
            exact_copy={},
            approved_typography_mechanisms=[],
            purpose="HUMAN_REVIEW",
        )
        pairs.append(
            {
                "family_id": program["family_id"],
                "evidence": "VALID",
                "hypothesis": "VALID",
                "figma_contract": "VALID",
                "visual_program_linkage": "VALID",
                "runtime_bounded": runtime["deep_evidence_embedded"] is False,
                "production_authorized": runtime["production_authorized"],
            }
        )

    mechanism_library = load("V3_VISUAL_MECHANISM_LIBRARY.json")
    for mechanism in mechanism_library["mechanisms"]:
        validate_mechanism(mechanism)

    receipt_path = ROOT / "V3_FIGMA_TECHNICAL_DRY_RUN_RECEIPT.json"
    receipt_status = "NOT_EXECUTED"
    if receipt_path.exists():
        validate_figma_dry_run_receipt(json.loads(receipt_path.read_text(encoding="utf-8")))
        receipt_status = "VALID"

    result = {
        "status": "PASS",
        "families": pairs,
        "families_separate": pairs[0]["family_id"] != pairs[1]["family_id"],
        "typography_mechanism_count": sum(
            row["domain"] == "typography_lettering" for row in mechanism_library["mechanisms"]
        ),
        "component_approval_statuses": sorted(
            {
                row["component_approval_status"]
                for row in mechanism_library["mechanisms"]
                if row["domain"] == "typography_lettering"
            }
        ),
        "promotion_statuses": sorted(
            {
                row["promotion_status"]
                for row in mechanism_library["mechanisms"]
                if row["domain"] == "typography_lettering"
            }
        ),
        "figma_dry_run_receipt": receipt_status,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
