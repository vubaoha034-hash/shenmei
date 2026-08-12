"""Conservative physical purge helpers for tombstoned private V0.1 data."""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Iterable


class PurgeError(RuntimeError):
    pass


def _prefix_kind(record_id: str) -> str | None:
    for prefix, kind in (("smp_", "sample"), ("ast_", "asset"), ("ev_", "event"), ("gen_", "generation")):
        if record_id.startswith(prefix):
            return kind
    return None


def _atomic_jsonl_write(path: Path, events: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            for event in events:
                handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def purge_tombstoned(store: Any, record_ids: Iterable[str], *, dry_run: bool = False) -> dict[str, Any]:
    targets = {str(x) for x in record_ids}
    if not targets:
        raise PurgeError("at least one record id is required")
    tombstoned = set(store.tombstoned_ids())
    missing = sorted(targets - tombstoned)
    if missing:
        raise PurgeError(f"physical purge requires prior tombstone for: {', '.join(missing)}")

    sample_ids = {x for x in targets if _prefix_kind(x) == "sample"}
    asset_ids = {x for x in targets if _prefix_kind(x) == "asset"}
    event_ids = {x for x in targets if _prefix_kind(x) == "event"}
    generation_ids = {x for x in targets if _prefix_kind(x) == "generation"}

    # Purging a logical sample always purges its owned asset bytes/locators too.
    for asset in store.read_assets():
        if asset.get("sample_id") in sample_ids:
            asset_ids.add(str(asset["asset_id"]))

    # Scrub execution metadata for generations explicitly targeted or touching purged samples.
    generation_scrub_ids = set(generation_ids)
    for generation in store.read_generations():
        refs = set(str(x) for x in generation.get("reference_sample_ids", []))
        outs = set(str(x) for x in generation.get("output_sample_ids", []))
        if (refs | outs) & sample_ids:
            generation_scrub_ids.add(str(generation["generation_id"]))

    plan = {
        "sample_ids": sorted(sample_ids),
        "asset_ids": sorted(asset_ids),
        "event_ids_removed": sorted(event_ids),
        "generation_ids_scrubbed": sorted(generation_scrub_ids),
        "derived_cleared": True,
    }
    if dry_run:
        return plan

    # Keep non-sensitive logical identity/audit skeletons; remove user/source payload.
    for sample_id in sample_ids:
        sample = store.read_sample(sample_id)
        if sample is None:
            continue
        sample = dict(sample)
        sample["provenance"] = {"source_type": "unknown", "source_ref": None, "creator": None, "license": None}
        sample["user_tags"] = []
        store._atomic_json_write(store.samples_dir / f"{sample_id}.json", sample)

    for asset_id in asset_ids:
        asset = store.read_asset(asset_id)
        if asset is None:
            continue
        resolved = store.resolve_asset(asset_id)
        if resolved is not None:
            try:
                resolved.relative_to(store.vault_dir.resolve())
            except ValueError:
                pass  # Never delete arbitrary external source files.
            else:
                resolved.unlink(missing_ok=True)
        asset = dict(asset)
        asset["locator_kind"] = "opaque"
        asset["locator"] = f"purged:{asset_id}"
        store._atomic_json_write(store.assets_dir / f"{asset_id}.json", asset)

    for generation_id in generation_scrub_ids:
        generation = store.read_generation(generation_id)
        if generation is None:
            continue
        generation = dict(generation)
        generation["task_ref"] = None
        generation["prompt_text"] = None
        generation["parameters"] = {}
        store._atomic_json_write(store.generations_dir / f"{generation_id}.json", generation)

    if event_ids:
        remaining = [event for event in store.read_evidence() if str(event.get("event_id")) not in event_ids]
        _atomic_jsonl_write(store.evidence_file, remaining)

    # Derived state is cache; clearing all is safer than attempting partial redaction.
    store.clear_derived()
    return plan
