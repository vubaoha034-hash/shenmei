"""Attach actual worker tool observations to the unchanged, single production trial."""
from pathlib import Path
import datetime
import hashlib
import json

p = Path(__file__).resolve().parent
assert p.name == "shanyeji-v29-production" and p.parent.name == ".liu-visual-private"
m = p / "manifest.json"
manifest = json.loads(m.read_text(encoding="utf-8"))
record = {
    "schema": "v29-maker-observed-tool-execution/v1",
    "recorded_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "role": "MAKER_ONLY",
    "production_exec_tool_result": {
        "tool": "exec_command",
        "chunk_id": "e62b09",
        "exit_code": 0,
        "command": "& 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -X utf8 '.liu-visual-private/shanyeji-v29-production/build_v29.py'",
        "observed_poster_sha256": "9ef3fb9bcdbf2b6188e95b90d4abe9e6b12ab2c237acf544e73b9c8ab65b7fe4",
        "observed_auxiliary_path_count": 35,
        "observed_alpha_bounds": [140, 100, 530, 447],
        "observed_outside_alpha_changed_pixels": 0,
        "observed_lower_protected_changed_pixels": 0,
        "warning": "Pillow 12.3.0 warned that getdata is deprecated; production completed with exit code 0.",
    },
    "actual_image_tool_calls": [
        {"tool": "view_image", "detail": "original", "path": ".liu-visual-private/product-type-integration-20261004/SHANYEJI-canonical-readback-20261005.jpg", "dimensions": [960, 1280], "pixels_returned_and_viewed": True},
        {"tool": "view_image", "detail": "original", "path": ".liu-visual-private/source_recovery_20261003/photography-local-reconstruction-final.png", "dimensions": [1536, 1024], "pixels_returned_and_viewed": True},
        {"tool": "view_image", "detail": "original", "path": ".liu-visual-private/shanyeji-v29-production/poster.png", "dimensions": [1536, 1024], "pixels_returned_and_viewed": True},
    ],
    "technical_observation": "All four text roles rendered in the one specified information group above y447; no source photograph regeneration or second composition was performed. SVG source/path and raw-pixel protection checks are in the manifest.",
    "aesthetic_evaluation_performed": False,
    "human_approval_claimed": False,
    "formal_freeze_performed": False,
    "existing_dependency_preflight": "Default bundled Python lacked FontTools on sys.path; existing hermes package directory was appended after loading bundled Pillow. Default shell Node lacked sharp; bundled absolute Node and sharp paths succeeded.",
    "finalization_call_error": {"exec_chunk_id": "0ef841", "exit_code": 1, "error": "PowerShell rejected nested inline quote escaping before Python execution; no artifact changed. This separate UTF-8 script replaces that inline command."},
    "write_scope": str(p),
}
r = p / "worker-call-evidence.json"
r.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def asset(path):
    return {"path": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size}

receipt = asset(r)
manifest["worker_call_evidence"] = receipt
assert "worker-call-evidence.json" not in [a["path"] for a in manifest["assets"]]
manifest["assets"].extend([receipt, asset(Path(__file__).resolve())])
m.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
errors = [a["path"] for a in manifest["assets"] if hashlib.sha256((p / a["path"]).read_bytes()).hexdigest() != a["sha256"]]
assert not errors
print(json.dumps({"manifest_sha256": hashlib.sha256(m.read_bytes()).hexdigest(), "asset_hash_failures": errors,
                  "poster_sha256": hashlib.sha256((p / "poster.png").read_bytes()).hexdigest(),
                  "files": [q.name for q in p.iterdir() if q.is_file()]}, ensure_ascii=False, indent=2))
