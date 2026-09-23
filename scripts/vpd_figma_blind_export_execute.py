#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import subprocess
import tempfile
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

TASK_ID_RE = re.compile(r"^[A-Za-z0-9._-]{1,120}$")
NODE_RE = re.compile(r"^\d+:\d+$")
ALLOWED_NAMES = {"PAIR2_POSTER_X.png", "PAIR2_POSTER_Y.png"}


def write_receipt(path: Path, body: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(body, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)
    ap.add_argument("--cert", required=True)
    ap.add_argument("--private-key", required=True)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--receipt", required=True)
    args = ap.parse_args()

    task = Path(args.task).resolve()
    cert = Path(args.cert).resolve()
    key = Path(args.private_key).resolve()
    out_dir = Path(args.output_dir).resolve()
    receipt = Path(args.receipt).resolve()
    started = datetime.now(timezone.utc).isoformat()
    base = {
        "schema_version": "vpd-figma-blind-export-receipt/v1",
        "task_file": task.name,
        "started_at": started,
        "route_mapping_in_receipt": False,
    }

    try:
        with tempfile.TemporaryDirectory(prefix="vpd-figma-blind-export-") as td:
            manifest_path = Path(td) / "task.json"
            subprocess.run([
                "openssl", "cms", "-decrypt", "-binary", "-inform", "DER",
                "-in", str(task), "-recip", str(cert), "-inkey", str(key),
                "-out", str(manifest_path),
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

            m = json.loads(manifest_path.read_text(encoding="utf-8"))
            if m.get("schema_version") != "vpd-figma-blind-export-task/v1":
                raise RuntimeError("unsupported blind export task schema")
            task_id = str(m.get("task_id", ""))
            if not TASK_ID_RE.fullmatch(task_id):
                raise RuntimeError("invalid task id")
            exports = m.get("exports")
            if not isinstance(exports, list) or len(exports) != 2:
                raise RuntimeError("expected exactly two blind exports")

            out_dir.mkdir(parents=True, exist_ok=True)
            seen = set()
            rows = []
            for e in exports:
                name = str(e.get("blind_name", ""))
                if name not in ALLOWED_NAMES or name in seen:
                    raise RuntimeError("invalid or duplicate blind filename")
                seen.add(name)
                node_id = str(e.get("node_id", ""))
                if not NODE_RE.fullmatch(node_id):
                    raise RuntimeError("invalid node id")
                url = str(e.get("url", ""))
                p = urllib.parse.urlparse(url)
                if p.scheme != "https" or p.hostname != "www.figma.com" or not p.path.startswith("/api/mcp/asset/"):
                    raise RuntimeError("rejected Figma export URL")

                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "image/png"})
                with urllib.request.urlopen(req, timeout=60) as response:
                    data = response.read()
                if not data.startswith(b"\x89PNG\r\n\x1a\n") or len(data) < 24:
                    raise RuntimeError("download is not PNG")
                width, height = struct.unpack(">II", data[16:24])
                expected = (int(e["expected_width"]), int(e["expected_height"]))
                if (width, height) != expected:
                    raise RuntimeError(f"dimension mismatch for {name}: {(width, height)} != {expected}")

                dest = out_dir / name
                dest.write_bytes(data)
                rows.append({
                    "blind_name": name,
                    "node_id": node_id,
                    "width": width,
                    "height": height,
                    "bytes": len(data),
                    "sha256": sha256_bytes(data),
                })

            body = {
                **base,
                "task_id": task_id,
                "status": "EXPORT_PASS",
                "exports": sorted(rows, key=lambda x: x["blind_name"]),
                "finished_at": datetime.now(timezone.utc).isoformat(),
            }
            write_receipt(receipt, body)
            print(json.dumps({"status": "EXPORT_PASS", "task_id": task_id}, ensure_ascii=False))
            return 0
    except Exception as exc:
        body = {
            **base,
            "status": "EXPORT_FAILED",
            "error": type(exc).__name__ + ": " + str(exc)[:400],
            "finished_at": datetime.now(timezone.utc).isoformat(),
        }
        write_receipt(receipt, body)
        print(json.dumps({"status": "EXPORT_FAILED", "task_file": task.name}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
