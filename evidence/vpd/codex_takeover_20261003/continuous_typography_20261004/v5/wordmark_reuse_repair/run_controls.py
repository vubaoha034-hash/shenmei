"""Bounded execution evidence for the new read-only entry point.

Writes only a new, exclusively created technical evidence run. Negative fixtures
are plain binary text, never new images. All nine original files are byte-compared
after every scenario, including five valid calls with different caller identities.
"""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[5]
HISTORICAL = REPO / "evidence/vpd/codex_takeover_20261003/continuous_typography_20261004/v5/wordmark"
ENTRY = REPO / "scripts/vpd_verify_original_wordmark.py"
PYTHON = Path("C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe")
RUN = HERE / "execution_01"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def snapshot():
    return {path.name: (path.read_bytes(), path.stat().st_mtime_ns) for path in HISTORICAL.iterdir() if path.is_file()}


def write_new(path, data):
    with path.open("xb") as handle:
        handle.write(data)


def main():
    before = snapshot()
    assert len(before) == 9
    assert sha(before["manifest.json"][0]) == "1ee9619693a13a87852108c1a42be4026bceba1c85d48c0cc766b7fd71929b0d"
    historical_identity = json.loads(before["provenance.json"][0])["execution"]["thread_id"]
    RUN.mkdir()  # Exclusive evidence directory; never overwrite an earlier run.
    fixture = RUN / "wrong-source.bin"
    write_new(fixture, b"Source-SHA negative fixture; not an image or a lettering candidate.\n")
    scenarios = []
    for name, option in (("wrong_photo", "--photo-path"), ("wrong_reference", "--reference-path"), ("wrong_v4", "--v4-path")):
        scenarios.append((name, [option, str(fixture)], "SOURCE_SHA_MISMATCH", False))
    scenarios += [
        ("existing_bound_output_directory", ["--output-dir", str(HISTORICAL)], "EXISTING_OUTPUT_REJECTED", True),
        ("existing_bound_provenance_file", ["--output-dir", str(HISTORICAL / "provenance.json")], "EXISTING_OUTPUT_REJECTED", True),
        ("new_output_directory_not_created", ["--output-dir", str(RUN / "must-not-exist")], "READ_ONLY_ENTRY_POINT", True),
    ]
    scenarios += [(f"legal_control_{index}", [], None, True) for index in range(1, 6)]
    results = []
    for name, arguments, error, preflight in scenarios:
        environment = dict(os.environ, CODEX_THREAD_ID=f"read-only-control-{name}", PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1")
        command = [str(PYTHON), "-B", str(ENTRY), "--repo", str(REPO), *arguments]
        completed = subprocess.run(command, cwd=REPO, env=environment, capture_output=True, timeout=30)
        write_new(RUN / (name + ".stdout.json"), completed.stdout)
        write_new(RUN / (name + ".stderr.txt"), completed.stderr)
        report = json.loads(completed.stdout.decode("utf-8"))
        assert completed.stderr == b"", (name, completed.stderr)
        assert report["preflight_complete"] == preflight, (name, report)
        assert report["disk_writes"] == 0, (name, report)
        if error:
            assert completed.returncode == 2 and report["code"] == error, (name, report)
            assert not report["reconstruction_started"] and report["captured_write_count"] == 0, (name, report)
        else:
            assert completed.returncode == 0 and report["result"] == "verified_original_geometry_only", (name, report)
            assert report["reconstruction_started"] and report["captured_write_count"] == 5, (name, report)
            assert len(report["paths"]) == 15 and all(path["geometry_matches"] for path in report["paths"]), (name, report)
            assert report["historical_identity_preserved"] == historical_identity, (name, report)
            assert report["historical_files_unchanged"] and report["legacy_builder_disk_executions"] == report["legacy_render_executions"] == report["raster_render_calls"] == 0, (name, report)
        after = snapshot()
        assert after == before, (name, "Historical bytes or modification timestamps changed")
        assert not (RUN / "must-not-exist").exists()
        results.append({"scenario": name, "command": command, "returncode": completed.returncode, "code": report.get("code"), "preflight_complete": report["preflight_complete"], "reconstruction_started": report["reconstruction_started"], "captured_write_count": report["captured_write_count"], "all_nine_historical_files_byte_and_mtime_identical": True, "caller_thread_fixture": environment["CODEX_THREAD_ID"], "stdout_sha256": sha(completed.stdout)})
    result = {
        "scope": "Technical reuse verification only; no aesthetic or independent professional acceptance claim.",
        "entry_point": str(ENTRY),
        "entry_sha256": sha(ENTRY.read_bytes()),
        "controls_script_sha256": sha(Path(__file__).read_bytes()),
        "scenarios_executed": len(results),
        "negative_controls": 6,
        "valid_controls_with_different_caller_ids": 5,
        "all_historical_bytes_and_mtimes_unchanged_after_every_scenario": True,
        "historical_identity_unchanged": historical_identity,
        "no_image_generated_or_rendered": True,
        "no_business_state_modified_by_entry_or_controls": True,
        "original_files": [{"file": name, "bytes": len(data), "sha256": sha(data), "mtime_ns": timestamp} for name, (data, timestamp) in sorted(before.items())],
        "results": results,
    }
    write_new(RUN / "EXECUTION_REPORT.json", (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print(json.dumps({"evidence": str(RUN), "scenarios": len(results), "historical_files_unchanged": True, "images_generated": 0}, ensure_ascii=True))


if __name__ == "__main__":
    main()
