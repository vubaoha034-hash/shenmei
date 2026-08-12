"""Minimal real-pilot helpers for LIU VISUAL SYSTEM V0.1.

No embeddings, model training, critic changes, or Skill mutation live here.
"""
from __future__ import annotations

import mimetypes
import shutil
from pathlib import Path
from typing import Any, Iterable

from .store import SCHEMA_VERSION, VisualMemoryStore, new_id, sha256_file, utc_now


_ALLOWED_VERDICTS = {"approved", "rejected", "neutral"}
_ALLOWED_ROLES = {"discovery", "blind_eval_reserved"}


def ingest_visual_file(
    store: VisualMemoryStore,
    source_path: str | Path,
    *,
    dataset_role: str = "discovery",
    user_tags: Iterable[str] = (),
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Copy one visual file into the private vault without assuming preference."""
    source = Path(source_path).expanduser().resolve()
    if not source.is_file():
        raise FileNotFoundError(source)
    if dataset_role not in _ALLOWED_ROLES:
        raise ValueError(f"dataset_role must be one of {sorted(_ALLOWED_ROLES)}")

    sample_id = new_id("sample")
    asset_id = new_id("asset")
    suffix = source.suffix.lower() or ".bin"
    vault_path = store.vault_dir / f"{asset_id}{suffix}"
    if vault_path.exists():
        raise FileExistsError(vault_path)
    shutil.copy2(source, vault_path)

    asset = {
        "schema_version": SCHEMA_VERSION,
        "asset_id": asset_id,
        "sample_id": sample_id,
        "created_at": utc_now(),
        "sha256": sha256_file(vault_path),
        "locator_kind": "local_file",
        "locator": str(vault_path.relative_to(store.root)),
        "asset_relation": "primary",
        "derived_from_asset_id": None,
        "media_type": mimetypes.guess_type(source.name)[0] or "application/octet-stream",
    }
    sample = {
        "schema_version": SCHEMA_VERSION,
        "sample_id": sample_id,
        "created_at": utc_now(),
        "sample_kind": "imported",
        "primary_asset_id": asset_id,
        "dataset_role": dataset_role,
        "provenance": {
            "source_type": "user_upload",
            "source_ref": None,
            "creator": None,
            "license": None,
        },
        "user_tags": list(user_tags),
    }
    store.write_sample(sample)
    store.write_asset(asset)
    return sample, asset


def record_batch_feedback(
    store: VisualMemoryStore,
    sample_ids: Iterable[str],
    *,
    verdict: str,
    user_text: str,
    scope_level: str = "unspecified",
    domain: str | None = None,
) -> dict[str, Any]:
    """Attach one exact user statement to a deliberately selected sample batch."""
    ids = list(dict.fromkeys(sample_ids))
    if not ids:
        raise ValueError("sample_ids may not be empty")
    if verdict not in _ALLOWED_VERDICTS:
        raise ValueError(f"verdict must be one of {sorted(_ALLOWED_VERDICTS)}")
    if not user_text.strip():
        raise ValueError("user_text must preserve an explicit user statement")
    if scope_level == "domain" and not domain:
        raise ValueError("domain scope requires domain")
    if scope_level != "domain":
        domain = None

    for sample_id in ids:
        sample = store.read_sample(sample_id)
        if sample is None:
            raise FileNotFoundError(sample_id)
        if sample["dataset_role"] == "blind_eval_reserved":
            raise ValueError("blind_eval_reserved samples cannot enter discovery feedback")

    event = {
        "schema_version": SCHEMA_VERSION,
        "event_id": new_id("event"),
        "occurred_at": utc_now(),
        "event_type": "feedback",
        "source_kind": "user",
        "source_ref": None,
        "scope": {"level": scope_level, "domain": domain},
        "raw_text": user_text,
        "target_sample_ids": ids,
        "target_generation_ids": [],
        "payload": {"explicit_verdict": verdict},
    }
    store.append_evidence(event)
    return event


def build_context_pack(
    store: VisualMemoryStore,
    *,
    domain: str | None,
    max_positive: int = 4,
    max_negative: int = 2,
) -> dict[str, Any]:
    """Build a transparent, bounded context pack from discovery evidence only."""
    if max_positive < 0 or max_negative < 0:
        raise ValueError("context limits must be non-negative")

    effective = store.discovery_evidence()
    positive: list[dict[str, Any]] = []
    negative: list[dict[str, Any]] = []
    source_event_ids: list[str] = []
    seen: set[str] = set()

    def scope_matches(event: dict[str, Any]) -> bool:
        scope = event.get("scope", {})
        level = scope.get("level")
        if level == "global_explicit":
            return True
        if domain is not None and level == "domain" and scope.get("domain") == domain:
            return True
        return False

    for event in reversed(effective):
        if event.get("event_type") != "feedback" or not scope_matches(event):
            continue
        verdict = event.get("payload", {}).get("explicit_verdict")
        if verdict not in {"approved", "rejected"}:
            continue
        for sample_id in event.get("target_sample_ids", []):
            if sample_id in seen:
                continue
            sample = store.read_sample(sample_id)
            if sample is None or sample["dataset_role"] not in {"discovery", "production"}:
                continue
            resolved = store.resolve_asset(sample["primary_asset_id"])
            if resolved is None:
                continue
            item = {
                "sample_id": sample_id,
                "asset_id": sample["primary_asset_id"],
                "evidence_ids": [event["event_id"]],
                "raw_text": event["raw_text"],
                "resolvable": True,
            }
            target = positive if verdict == "approved" else negative
            limit = max_positive if verdict == "approved" else max_negative
            if len(target) < limit:
                target.append(item)
                source_event_ids.append(event["event_id"])
                seen.add(sample_id)

    return {
        "domain": domain,
        "positive_exemplars": positive,
        "negative_exemplars": negative,
        "source_event_ids": list(dict.fromkeys(source_event_ids)),
    }


def blind_pair_result(pair_id: str, presented_a_condition: str, winner: str) -> dict[str, str]:
    """Unblind one already-locked A/B decision into baseline/personalized/tie."""
    if presented_a_condition not in {"baseline", "personalized"}:
        raise ValueError("presented_a_condition is invalid")
    if winner not in {"A", "B", "tie"}:
        raise ValueError("winner must be A, B, or tie")
    if winner == "tie":
        result = "tie"
    elif winner == "A":
        result = presented_a_condition
    else:
        result = "personalized" if presented_a_condition == "baseline" else "baseline"
    return {"pair_id": pair_id, "result": result}


def summarize_blind_results(results: Iterable[dict[str, str]]) -> dict[str, Any]:
    rows = list(results)
    counts = {"baseline": 0, "personalized": 0, "tie": 0}
    for row in rows:
        value = row.get("result")
        if value not in counts:
            raise ValueError(f"invalid result: {value}")
        counts[value] += 1
    non_ties = counts["baseline"] + counts["personalized"]
    personalized_rate = counts["personalized"] / non_ties if non_ties else None
    if len(rows) < 10:
        decision = "INCONCLUSIVE"
    elif non_ties == 0:
        decision = "INCONCLUSIVE"
    elif personalized_rate >= 0.60 and counts["personalized"] >= counts["baseline"] + 2:
        decision = "PASS_TO_EXPAND"
    elif counts["baseline"] >= counts["personalized"]:
        decision = "FAIL_REWORK"
    else:
        decision = "INCONCLUSIVE"
    return {
        "valid_pairs": len(rows),
        "wins": counts,
        "personalized_non_tie_win_rate": personalized_rate,
        "decision": decision,
    }
