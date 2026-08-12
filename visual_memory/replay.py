"""Replay direct user evidence without mutating the raw ledger."""
from __future__ import annotations

from typing import Any, Callable, Iterable


def _tombstoned_ids(events: Iterable[dict[str, Any]]) -> set[str]:
    ids: set[str] = set()
    for event in events:
        if event.get("event_type") == "tombstone":
            ids.update(str(x) for x in event.get("payload", {}).get("target_record_ids", []))
    return ids


def effective_evidence(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return the effective append-log view.

    - `supersede` / `retract` deactivate target evidence events.
    - `clarify` keeps prior evidence visible and adds the clarification event.
    - tombstoned events/targets are excluded from the effective view.
    """
    tombstoned = _tombstoned_ids(events)
    inactive: set[str] = set()
    for event in events:
        if event.get("event_type") != "correction":
            continue
        effect = event.get("payload", {}).get("effect")
        if effect in {"supersede", "retract"}:
            inactive.update(str(x) for x in event.get("payload", {}).get("target_event_ids", []))

    out: list[dict[str, Any]] = []
    for event in events:
        event_id = str(event.get("event_id", ""))
        if event_id in tombstoned or event_id in inactive:
            continue
        targets = set(str(x) for x in event.get("target_sample_ids", []))
        targets.update(str(x) for x in event.get("target_generation_ids", []))
        if targets & tombstoned:
            continue
        if event.get("event_type") == "tombstone":
            continue
        out.append(event)
    return out


def discovery_evidence(
    events: list[dict[str, Any]],
    *,
    sample_role: Callable[[str], str | None],
    generation_is_reserved: Callable[[str], bool],
) -> list[dict[str, Any]]:
    """Return direct user evidence eligible for preference discovery.

    Blind-eval isolation is transitive: evidence touching a reserved sample or a
    generation designated as reserved is excluded. Corrections that depend on
    quarantined blind-case evidence are quarantined as well.
    """
    effective = effective_evidence(events)
    by_id = {str(event.get("event_id")): event for event in events}
    memo: dict[str, bool] = {}

    def depends_on_reserved(event: dict[str, Any], stack: set[str] | None = None) -> bool:
        event_id = str(event.get("event_id", ""))
        if event_id in memo:
            return memo[event_id]
        stack = set() if stack is None else set(stack)
        if event_id in stack:
            return False
        stack.add(event_id)

        sample_ids = [str(x) for x in event.get("target_sample_ids", [])]
        generation_ids = [str(x) for x in event.get("target_generation_ids", [])]
        payload = event.get("payload", {})
        for key in ("left_sample_id", "right_sample_id", "before_sample_id", "after_sample_id"):
            value = payload.get(key)
            if isinstance(value, str):
                sample_ids.append(value)

        reserved = any(sample_role(sample_id) == "blind_eval_reserved" for sample_id in sample_ids)
        reserved = reserved or any(generation_is_reserved(generation_id) for generation_id in generation_ids)

        if not reserved and event.get("event_type") == "correction":
            for target_id in payload.get("target_event_ids", []):
                target = by_id.get(str(target_id))
                if target is not None and depends_on_reserved(target, stack):
                    reserved = True
                    break

        memo[event_id] = reserved
        return reserved

    return [event for event in effective if not depends_on_reserved(event)]
