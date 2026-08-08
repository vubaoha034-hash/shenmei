#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "evolve.py"


def run(root: Path, *args: str, expect: int = 0) -> dict:
    p = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=root,
        text=True,
        capture_output=True,
    )
    if p.returncode != expect:
        raise AssertionError(f"exit={p.returncode} expected={expect}\nstdout={p.stdout}\nstderr={p.stderr}")
    return json.loads(p.stdout)


def main() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        skill = root / "skills" / "demo"
        skill.mkdir(parents=True)
        skill.joinpath("SKILL.md").write_text("---\nname: demo\ndescription: demo\n---\n# Demo\n", encoding="utf-8")

        evidence_ids = []
        for i in range(3):
            res = run(
                root,
                "observe", "--repo-root", ".", "--target", "demo", "--layer", "skill",
                "--kind", "failure", "--source", "test", "--case-id", f"case-{i}",
                "--confidence", "verified", "--severity", "high", "--summary", f"repeat failure {i}",
            )
            evidence_ids.append(res["evidence"]["id"])

        cand = run(
            root,
            "candidate", "--repo-root", ".", "--target", "demo", "--layer", "skill",
            "--scope", "reference", "--target-file", "skills/demo/references/rule.md",
            "--title", "Stable rule", "--proposal", "Add scoped rule", "--rationale", "Repeated verified failures",
            "--evidence-ids", ",".join(evidence_ids),
        )["candidate"]

        hold = run(root, "decision", "--repo-root", ".", "--target", "demo", "--candidate-id", cand["id"])
        assert hold["decision"] == "HOLD", hold

        run(
            root,
            "evaluate", "--repo-root", ".", "--target", "demo", "--candidate-id", cand["id"],
            "--suite", "regression", "--result", "pass", "--baseline-score", "0.7",
            "--candidate-score", "0.9", "--regressions", "0",
        )
        promote = run(root, "decision", "--repo-root", ".", "--target", "demo", "--candidate-id", cand["id"])
        assert promote["decision"] == "PROMOTE", promote

        marked = run(
            root,
            "promote", "--repo-root", ".", "--target", "demo", "--candidate-id", cand["id"],
            "--git-ref", "PR#1 / abc123",
        )
        assert marked["candidate"]["status"] == "promoted"

        status = run(root, "status", "--repo-root", ".", "--target", "demo")
        assert status["evidence_count"] == 3
        assert status["candidate_count"] == 1

    print("skill-refiner self-test: PASS")


if __name__ == "__main__":
    main()
