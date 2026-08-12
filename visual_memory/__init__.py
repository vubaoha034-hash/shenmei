"""Minimal LIU VISUAL SYSTEM V0.1 persistence scaffold.

This package implements the frozen raw-evidence contract only. It intentionally
contains no preference model, embeddings, visual Skill, critic, or router.
"""

from .store import VisualMemoryStore, new_id, utc_now
from .replay import effective_evidence, discovery_evidence
from .validation import validate_record

__all__ = [
    "VisualMemoryStore",
    "new_id",
    "utc_now",
    "effective_evidence",
    "discovery_evidence",
    "validate_record",
]
