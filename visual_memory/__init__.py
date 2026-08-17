"""Minimal LIU VISUAL SYSTEM V0.1 persistence scaffold.

This package implements the frozen raw-evidence contract only. It intentionally
contains no preference model, embeddings, visual Skill, critic, or router.
"""

from .store import VisualMemoryStore, new_id, utc_now
from .replay import effective_evidence, discovery_evidence
from .validation import validate_record
from .distillation_v3 import (
    build_promotion_package,
    build_runtime_package,
    build_validation_receipt,
    classify_liked_work,
    package_distillation_hypothesis,
    rank_candidate_evidence,
    validate_deep_evidence,
    validate_distillation_hypothesis,
    validate_mechanism,
    validate_semantic_identity,
    validate_transfer_plan,
    validate_visual_program,
)

__all__ = [
    "VisualMemoryStore",
    "new_id",
    "utc_now",
    "effective_evidence",
    "discovery_evidence",
    "validate_record",
    "build_promotion_package",
    "build_runtime_package",
    "build_validation_receipt",
    "classify_liked_work",
    "package_distillation_hypothesis",
    "rank_candidate_evidence",
    "validate_deep_evidence",
    "validate_distillation_hypothesis",
    "validate_mechanism",
    "validate_semantic_identity",
    "validate_transfer_plan",
    "validate_visual_program",
]
