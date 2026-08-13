"""Frozen-context replication helpers for LIU VISUAL SYSTEM PHASE 10.

This module intentionally adds no retrieval, preference learning, or Skill logic.
It only snapshots already-frozen private state and scores locked blind results.
"""
from __future__ import annotations

import hashlib
import json
from math import comb
from typing import Any, Iterable

from .pilot import build_context_pack
from .store import VisualMemoryStore, utc_now


def canonical_sha256(payload: Any) -> str:
    """Return SHA-256 over canonical UTF-8 JSON."""
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def build_replication_snapshot(
    store: VisualMemoryStore,
    *,
    domain: str,
    max_positive: int = 4,
    max_negative: int = 2,
) -> dict[str, Any]:
    """Build a private deterministic snapshot of the frozen discovery/context state.

    The returned payload may contain private IDs and must stay outside public Git.
    """
    context = build_context_pack(
        store,
        domain=domain,
        max_positive=max_positive,
        max_negative=max_negative,
    )
    discovery_samples = sorted(
        sample["sample_id"] for sample in store.discovery_samples()
    )
    discovery_events = sorted(
        event["event_id"] for event in store.discovery_evidence()
    )
    state = {
        "domain": domain,
        "max_positive": max_positive,
        "max_negative": max_negative,
        "discovery_sample_ids": discovery_samples,
        "discovery_event_ids": discovery_events,
        "context_pack": context,
    }
    return {
        "phase": "10",
        "created_at": utc_now(),
        "state": state,
        "state_sha256": canonical_sha256(state),
    }


def verify_replication_snapshot(
    store: VisualMemoryStore,
    snapshot: dict[str, Any],
) -> bool:
    """Return True only when the current private state still matches the snapshot."""
    state = snapshot.get("state")
    if not isinstance(state, dict):
        return False
    expected = snapshot.get("state_sha256")
    if expected != canonical_sha256(state):
        return False
    domain = state.get("domain")
    max_positive = state.get("max_positive")
    max_negative = state.get("max_negative")
    if not isinstance(domain, str):
        return False
    if not isinstance(max_positive, int) or not isinstance(max_negative, int):
        return False
    current = build_replication_snapshot(
        store,
        domain=domain,
        max_positive=max_positive,
        max_negative=max_negative,
    )["state"]
    return canonical_sha256(current) == expected


def exact_binomial_one_sided_p(
    successes: int,
    trials: int,
    *,
    null_p: float = 0.5,
) -> float:
    """P[X >= successes] for X~Binomial(trials, null_p), standard library only."""
    if not isinstance(successes, int) or not isinstance(trials, int):
        raise TypeError("successes and trials must be integers")
    if trials < 0 or successes < 0 or successes > trials:
        raise ValueError("invalid successes/trials")
    if not 0.0 <= null_p <= 1.0:
        raise ValueError("null_p must be in [0, 1]")
    if trials == 0:
        return 1.0
    tail = 0.0
    for k in range(successes, trials + 1):
        tail += comb(trials, k) * (null_p**k) * ((1.0 - null_p) ** (trials - k))
    return min(1.0, max(0.0, tail))


def count_locked_results(results: Iterable[dict[str, str]]) -> dict[str, int]:
    counts = {"personalized": 0, "baseline": 0, "tie": 0}
    for row in results:
        value = row.get("result")
        if value not in counts:
            raise ValueError(f"invalid locked blind result: {value}")
        counts[value] += 1
    return counts


def summarize_replication(
    phase10_results: Iterable[dict[str, str]],
    *,
    phase9_personalized_wins: int = 6,
    phase9_baseline_wins: int = 4,
    phase9_ties: int = 0,
    safety_ok: bool = True,
    frozen_state_unchanged: bool = True,
) -> dict[str, Any]:
    """Apply the pre-registered PHASE 10 decision rule."""
    rows = list(phase10_results)
    counts10 = count_locked_results(rows)
    valid_pairs = len(rows)
    non_ties10 = counts10["personalized"] + counts10["baseline"]
    rate10 = (
        counts10["personalized"] / non_ties10 if non_ties10 else None
    )

    combined_personalized = phase9_personalized_wins + counts10["personalized"]
    combined_baseline = phase9_baseline_wins + counts10["baseline"]
    combined_ties = phase9_ties + counts10["tie"]
    combined_non_ties = combined_personalized + combined_baseline
    combined_rate = (
        combined_personalized / combined_non_ties if combined_non_ties else None
    )
    p_value = exact_binomial_one_sided_p(
        combined_personalized,
        combined_non_ties,
        null_p=0.5,
    )

    if not safety_ok or not frozen_state_unchanged:
        decision = "INVALID"
    elif valid_pairs < 20:
        decision = "INCONCLUSIVE"
    elif counts10["personalized"] <= counts10["baseline"]:
        decision = "NOT_REPLICATED"
    elif p_value <= 0.05:
        decision = "REPLICATION_PASS"
    else:
        decision = "INCONCLUSIVE"

    return {
        "phase10": {
            "valid_pairs": valid_pairs,
            "wins": counts10,
            "non_tie_personalized_win_rate": rate10,
        },
        "combined_phase9_phase10": {
            "personalized_wins": combined_personalized,
            "baseline_wins": combined_baseline,
            "ties": combined_ties,
            "non_ties": combined_non_ties,
            "personalized_non_tie_win_rate": combined_rate,
            "one_sided_exact_binomial_p": p_value,
        },
        "safety_ok": safety_ok,
        "frozen_state_unchanged": frozen_state_unchanged,
        "decision": decision,
    }
