#!/usr/bin/env python3
"""Evidence-gated continual improvement ledger for Agent Skills and agent/repo rules.

Standard library only. Writes machine-readable state under:
  <repo>/.skill-evolution/<target>/state.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

SCHEMA = 1
LAYERS = {"skill", "agent", "repo"}
KINDS = {"failure", "success", "correction", "regression", "tactic", "invariant", "tool"}
CONFIDENCE = {"low", "medium", "high", "verified"}
SEVERITY = {"low", "medium", "high", "critical"}
SCOPES = {"core", "reference", "script", "test", "agent", "repo"}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def out(payload: dict[str, Any], code: int = 0) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    raise SystemExit(code)


def slug(value: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip()).strip("-.").lower()
    if not s:
        raise ValueError("target becomes empty after normalization")
    return s[:100]


def stable_id(prefix: str, *parts: str) -> str:
    h = hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()[:12]
    return f"{prefix}_{h}"


def state_dir(repo_root: Path, target: str) -> Path:
    return repo_root / ".skill-evolution" / slug(target)


def state_path(repo_root: Path, target: str) -> Path:
    return state_dir(repo_root, target) / "state.json"


def empty_state(target: str) -> dict[str, Any]:
    ts = now()
    return {
        "schema": SCHEMA,
        "target": target,
        "created_at": ts,
        "updated_at": ts,
        "evidence": [],
        "candidates": [],
        "evaluations": [],
    }


def load_state(repo_root: Path, target: str) -> dict[str, Any]:
    p = state_path(repo_root, target)
    if not p.exists():
        return empty_state(target)
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        raise RuntimeError(f"cannot read {p}: {exc}") from exc
    if not isinstance(data, dict) or data.get("schema") != SCHEMA:
        raise RuntimeError(f"unsupported or corrupt state file: {p}")
    for key in ("evidence", "candidates", "evaluations"):
        if not isinstance(data.get(key), list):
            raise RuntimeError(f"state field {key!r} must be a list")
    return data


def save_state(repo_root: Path, target: str, state: dict[str, Any]) -> None:
    d = state_dir(repo_root, target)
    d.mkdir(parents=True, exist_ok=True)
    p = d / "state.json"
    tmp = d / f".state.{os.getpid()}.tmp"
    state["updated_at"] = now()
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, p)


def repo(args: argparse.Namespace) -> Path:
    root = Path(args.repo_root).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise ValueError(f"repo root does not exist: {root}")
    return root


def find(items: list[dict[str, Any]], item_id: str, label: str) -> dict[str, Any]:
    for item in items:
        if item.get("id") == item_id:
            return item
    raise ValueError(f"unknown {label} id: {item_id}")


def parse_ids(raw: list[str] | None) -> list[str]:
    if not raw:
        return []
    ids: list[str] = []
    for chunk in raw:
        ids.extend(x.strip() for x in chunk.split(",") if x.strip())
    return list(dict.fromkeys(ids))


def cmd_observe(args: argparse.Namespace) -> None:
    root = repo(args)
    state = load_state(root, args.target)
    fp = stable_id(
        "fp",
        args.layer,
        args.kind,
        args.source,
        args.case_id,
        args.summary.strip().lower(),
    )
    for ev in state["evidence"]:
        if ev.get("fingerprint") == fp:
            out({"ok": True, "deduplicated": True, "evidence": ev})
    ev_id = stable_id("ev", fp, now())
    ev = {
        "id": ev_id,
        "fingerprint": fp,
        "layer": args.layer,
        "kind": args.kind,
        "source": args.source,
        "case_id": args.case_id,
        "confidence": args.confidence,
        "severity": args.severity,
        "summary": args.summary.strip(),
        "detail": (args.detail or "").strip(),
        "contradicts": parse_ids(args.contradicts),
        "created_at": now(),
    }
    state["evidence"].append(ev)
    save_state(root, args.target, state)
    out({"ok": True, "deduplicated": False, "evidence": ev, "state": str(state_path(root, args.target))})


def cmd_candidate(args: argparse.Namespace) -> None:
    root = repo(args)
    state = load_state(root, args.target)
    evidence_ids = parse_ids(args.evidence_ids)
    if not evidence_ids:
        raise ValueError("candidate requires at least one evidence id")
    for ev_id in evidence_ids:
        find(state["evidence"], ev_id, "evidence")
    seed = "|".join([args.title, args.layer, args.scope, args.target_file, *evidence_ids, now()])
    cand = {
        "id": stable_id("cand", seed),
        "layer": args.layer,
        "scope": args.scope,
        "target_file": args.target_file,
        "title": args.title.strip(),
        "proposal": args.proposal.strip(),
        "rationale": args.rationale.strip(),
        "evidence_ids": evidence_ids,
        "deterministic_bug": bool(args.deterministic_bug),
        "core_line_delta": int(args.core_line_delta),
        "status": "candidate",
        "git_ref": None,
        "created_at": now(),
        "updated_at": now(),
    }
    state["candidates"].append(cand)
    save_state(root, args.target, state)
    out({"ok": True, "candidate": cand})


def cmd_evaluate(args: argparse.Namespace) -> None:
    root = repo(args)
    state = load_state(root, args.target)
    cand = find(state["candidates"], args.candidate_id, "candidate")
    ev = {
        "id": stable_id("eval", args.candidate_id, args.suite, now()),
        "candidate_id": args.candidate_id,
        "suite": args.suite,
        "result": args.result,
        "baseline_score": args.baseline_score,
        "candidate_score": args.candidate_score,
        "regressions": args.regressions,
        "notes": (args.notes or "").strip(),
        "created_at": now(),
    }
    state["evaluations"].append(ev)
    cand["updated_at"] = now()
    save_state(root, args.target, state)
    out({"ok": True, "evaluation": ev})


def core_line_count(root: Path, target: str, candidate: dict[str, Any]) -> int | None:
    target_file = candidate.get("target_file") or ""
    if candidate.get("scope") != "core" and not target_file.endswith("SKILL.md"):
        return None
    choices = [
        root / target_file,
        root / "skills" / target / "SKILL.md",
    ]
    for p in choices:
        if p.exists() and p.is_file():
            return len(p.read_text(encoding="utf-8", errors="replace").splitlines())
    return None


def decision_for(root: Path, state: dict[str, Any], cand: dict[str, Any]) -> dict[str, Any]:
    evidence = [find(state["evidence"], eid, "evidence") for eid in cand.get("evidence_ids", [])]
    evals = [e for e in state["evaluations"] if e.get("candidate_id") == cand.get("id")]
    unique_cases = {e.get("case_id") for e in evidence if e.get("case_id")}
    verified = [e for e in evidence if e.get("confidence") == "verified"]
    contradictions = sorted({x for e in evidence for x in e.get("contradicts", []) if x})
    failed_evals = [e for e in evals if e.get("result") == "fail"]
    passing_evals = [e for e in evals if e.get("result") == "pass"]
    regressions = sum(max(0, int(e.get("regressions") or 0)) for e in evals)
    reasons: list[str] = []

    if failed_evals:
        decision = "REJECT"
        reasons.append("at least one recorded evaluation failed")
    elif regressions > 0:
        decision = "REWORK"
        reasons.append(f"recorded regressions: {regressions}")
    elif contradictions:
        decision = "REWORK"
        reasons.append("linked evidence contains unresolved contradiction references")
    else:
        evidence_ready = len(unique_cases) >= 3 or (cand.get("deterministic_bug") and len(verified) >= 1)
        if not evidence_ready:
            decision = "HOLD"
            reasons.append("needs 3 independent cases, or a deterministic bug with verified evidence")
        elif not passing_evals:
            decision = "HOLD"
            reasons.append("needs at least one passing baseline-vs-candidate evaluation")
        else:
            decision = "PROMOTE"
            reasons.append("evidence and evaluation gates passed")

    lines = core_line_count(root, state["target"], cand)
    delta = int(cand.get("core_line_delta") or 0)
    projected = None if lines is None else lines + delta
    if lines is not None:
        if projected is not None and projected > 500:
            decision = "REWORK"
            reasons.append(f"core budget exceeded: projected SKILL.md {projected} lines > 500")
        elif lines > 250 and delta > 0:
            decision = "REWORK" if decision == "PROMOTE" else decision
            reasons.append(
                f"target SKILL.md is already {lines} lines; positive core growth ({delta:+d}) requires compaction/replacement"
            )

    return {
        "decision": decision,
        "candidate_id": cand["id"],
        "unique_cases": len(unique_cases),
        "verified_evidence": len(verified),
        "evaluation_count": len(evals),
        "passing_evaluations": len(passing_evals),
        "regressions": regressions,
        "contradictions": contradictions,
        "core_lines": lines,
        "core_line_delta": delta,
        "projected_core_lines": projected,
        "reasons": reasons,
    }


def cmd_decision(args: argparse.Namespace) -> None:
    root = repo(args)
    state = load_state(root, args.target)
    cand = find(state["candidates"], args.candidate_id, "candidate")
    out({"ok": True, **decision_for(root, state, cand)})


def cmd_promote(args: argparse.Namespace) -> None:
    root = repo(args)
    state = load_state(root, args.target)
    cand = find(state["candidates"], args.candidate_id, "candidate")
    gate = decision_for(root, state, cand)
    if gate["decision"] != "PROMOTE":
        out({"ok": False, "error": "promotion gate not passed", **gate}, 2)
    cand["status"] = "promoted"
    cand["git_ref"] = args.git_ref.strip()
    cand["updated_at"] = now()
    save_state(root, args.target, state)
    out({"ok": True, "candidate": cand, "gate": gate})


def cmd_status(args: argparse.Namespace) -> None:
    root = repo(args)
    state = load_state(root, args.target)
    summaries = []
    for cand in state["candidates"]:
        gate = decision_for(root, state, cand)
        summaries.append({
            "id": cand["id"],
            "title": cand["title"],
            "status": cand["status"],
            "gate": gate["decision"],
            "reasons": gate["reasons"],
        })
    out({
        "ok": True,
        "target": state["target"],
        "state": str(state_path(root, args.target)),
        "evidence_count": len(state["evidence"]),
        "candidate_count": len(state["candidates"]),
        "evaluation_count": len(state["evaluations"]),
        "candidates": summaries,
    })


def cmd_compact(args: argparse.Namespace) -> None:
    root = repo(args)
    state = load_state(root, args.target)
    cutoff = datetime.now(timezone.utc) - timedelta(days=args.older_than_days)
    linked = {eid for c in state["candidates"] for eid in c.get("evidence_ids", [])}
    keep: list[dict[str, Any]] = []
    archive: list[dict[str, Any]] = []
    for ev in state["evidence"]:
        try:
            created = datetime.fromisoformat(ev["created_at"])
        except Exception:
            keep.append(ev)
            continue
        if ev.get("id") not in linked and created < cutoff:
            archive.append(ev)
        else:
            keep.append(ev)
    if archive:
        d = state_dir(root, args.target)
        d.mkdir(parents=True, exist_ok=True)
        with (d / "archive.jsonl").open("a", encoding="utf-8") as fh:
            for ev in archive:
                fh.write(json.dumps(ev, ensure_ascii=False, sort_keys=True) + "\n")
        state["evidence"] = keep
        save_state(root, args.target, state)
    out({"ok": True, "archived": len(archive), "active_evidence": len(keep)})


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Evidence-gated Skill/Agent/Repo continual improvement ledger")
    sub = p.add_subparsers(dest="command", required=True)

    def common(sp: argparse.ArgumentParser) -> None:
        sp.add_argument("--repo-root", default=".")
        sp.add_argument("--target", required=True)

    s = sub.add_parser("observe", help="record one evidence item")
    common(s)
    s.add_argument("--layer", choices=sorted(LAYERS), required=True)
    s.add_argument("--kind", choices=sorted(KINDS), required=True)
    s.add_argument("--source", required=True, help="user|test|ci|agent|tool|source-code|other")
    s.add_argument("--case-id", required=True)
    s.add_argument("--confidence", choices=sorted(CONFIDENCE), default="medium")
    s.add_argument("--severity", choices=sorted(SEVERITY), default="medium")
    s.add_argument("--summary", required=True)
    s.add_argument("--detail")
    s.add_argument("--contradicts", action="append", help="evidence IDs this item contradicts; repeat or comma-separate")
    s.set_defaults(func=cmd_observe)

    s = sub.add_parser("candidate", help="create a proposed reusable improvement")
    common(s)
    s.add_argument("--layer", choices=sorted(LAYERS), required=True)
    s.add_argument("--scope", choices=sorted(SCOPES), required=True)
    s.add_argument("--target-file", required=True)
    s.add_argument("--title", required=True)
    s.add_argument("--proposal", required=True)
    s.add_argument("--rationale", required=True)
    s.add_argument("--evidence-ids", action="append", required=True)
    s.add_argument("--deterministic-bug", action="store_true")
    s.add_argument("--core-line-delta", type=int, default=0)
    s.set_defaults(func=cmd_candidate)

    s = sub.add_parser("evaluate", help="record baseline-vs-candidate evaluation")
    common(s)
    s.add_argument("--candidate-id", required=True)
    s.add_argument("--suite", required=True)
    s.add_argument("--result", choices=["pass", "fail"], required=True)
    s.add_argument("--baseline-score", type=float)
    s.add_argument("--candidate-score", type=float)
    s.add_argument("--regressions", type=int, default=0)
    s.add_argument("--notes")
    s.set_defaults(func=cmd_evaluate)

    s = sub.add_parser("decision", help="compute promotion gate")
    common(s)
    s.add_argument("--candidate-id", required=True)
    s.set_defaults(func=cmd_decision)

    s = sub.add_parser("promote", help="mark a gate-passed candidate as promoted after Git merge")
    common(s)
    s.add_argument("--candidate-id", required=True)
    s.add_argument("--git-ref", required=True)
    s.set_defaults(func=cmd_promote)

    s = sub.add_parser("status", help="show active evidence/candidates")
    common(s)
    s.set_defaults(func=cmd_status)

    s = sub.add_parser("compact", help="archive old unlinked evidence")
    common(s)
    s.add_argument("--older-than-days", type=int, default=180)
    s.set_defaults(func=cmd_compact)
    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except ValueError as exc:
        out({"ok": False, "error": str(exc)}, 2)
    except RuntimeError as exc:
        out({"ok": False, "error": str(exc)}, 3)


if __name__ == "__main__":
    main()
