#!/usr/bin/env python3
"""VPD Figma image upload relay.

Consumes one short-lived job JSON, reconstructs/downloads the exact source bytes,
verifies SHA-256, POSTs the bytes to the one-time Figma MCP upload URL, and writes
only a sanitized receipt. The submit URL is never printed to logs or receipts.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import urllib.request

ALLOWED_JOB_ROOT = Path("evidence/vpd/p6_equal_budget_integrated_design_v1/relay_jobs")
ALLOWED_ASSET_ROOT = Path("evidence/vpd/p6_equal_budget_integrated_design_v1/relay_assets")
ALLOWED_NODES = {"12:4", "12:12", "12:20", "12:28"}


def die(msg: str) -> "NoReturn":
    raise SystemExit(msg)


def load_job(path: Path) -> dict:
    resolved = path.resolve()
    root = ALLOWED_JOB_ROOT.resolve()
    if root not in resolved.parents:
        die(f"job path outside allowlisted root: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    required = ["job_id", "submit_url", "node_id", "content_type", "sha256", "source"]
    missing = [k for k in required if not data.get(k)]
    if missing:
        die(f"missing job fields: {missing}")
    if data["node_id"] not in ALLOWED_NODES:
        die(f"node_id is not allowlisted: {data['node_id']}")
    if not str(data["submit_url"]).startswith("https://mcp.figma.com/mcp/upload/"):
        die("submit_url is not a Figma MCP upload URL")
    if data["content_type"] not in {"image/png", "image/jpeg", "image/webp", "image/gif"}:
        die(f"unsupported content_type: {data['content_type']}")
    expires_at = int(data.get("expires_at_epoch", 0) or 0)
    if expires_at and int(time.time()) >= expires_at:
        die("job submit URL is already expired")
    return data


def safe_repo_asset(path_str: str) -> Path:
    p = Path(path_str)
    resolved = p.resolve()
    root = ALLOWED_ASSET_ROOT.resolve()
    if root not in resolved.parents:
        die(f"asset path outside allowlisted root: {p}")
    return p


def materialize_source(source: dict, out: Path) -> None:
    kind = source.get("kind")
    if kind == "repo_chunks":
        chunks = source.get("chunks") or []
        if not chunks:
            die("repo_chunks source has no chunks")
        b64_parts: list[str] = []
        for chunk in chunks:
            p = safe_repo_asset(str(chunk))
            b64_parts.append(p.read_text(encoding="ascii").strip())
        try:
            out.write_bytes(base64.b64decode("".join(b64_parts), validate=True))
        except Exception as exc:
            die(f"invalid base64 relay asset: {exc}")
    elif kind == "local_repo_file":
        p = safe_repo_asset(str(source.get("path", "")))
        out.write_bytes(p.read_bytes())
    elif kind == "public_url":
        url = str(source.get("url", ""))
        if not url.startswith("https://"):
            die("public_url source must be https")
        req = urllib.request.Request(url, headers={"User-Agent": "vpd-figma-relay/1.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            out.write_bytes(r.read())
    else:
        die(f"unsupported source kind: {kind}")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def mask_secret(value: str) -> None:
    # GitHub log command. This does not make a public git commit private; it only
    # prevents accidental re-emission by subsequent commands/logs.
    print(f"::add-mask::{value}")


def post_to_figma(job: dict, source_file: Path) -> dict:
    submit_url = str(job["submit_url"])
    mask_secret(submit_url)
    with tempfile.NamedTemporaryFile(prefix="figma-upload-response-", suffix=".json", delete=False) as tf:
        response_path = Path(tf.name)
    try:
        cmd = [
            "curl", "--fail-with-body", "--silent", "--show-error",
            "--connect-timeout", "20", "--max-time", "90",
            "--retry", "2", "--retry-delay", "1", "--retry-all-errors",
            "-H", f"Content-Type: {job['content_type']}",
            "--data-binary", f"@{source_file}",
            "-o", str(response_path),
            submit_url,
        ]
        proc = subprocess.run(cmd, text=True, capture_output=True)
        if proc.returncode != 0:
            # curl stderr is safe unless upstream echoes the URL; mask command above
            # protects the exact capability URL in GitHub logs.
            err = (proc.stderr or proc.stdout or "curl failed").strip()
            die(f"Figma upload POST failed (curl {proc.returncode}): {err[:1000]}")
        raw = response_path.read_text(encoding="utf-8", errors="replace")
        try:
            return json.loads(raw) if raw.strip() else {}
        except json.JSONDecodeError:
            return {"non_json_response": raw[:1000]}
    finally:
        response_path.unlink(missing_ok=True)


def sanitize_response(response: dict) -> dict:
    safe_keys = {
        "imageHash", "nodeId", "targetNodeId", "fileKey", "status", "success",
        "width", "height", "name", "scaleMode", "placement",
    }
    out = {}
    for k, v in response.items():
        if k in safe_keys:
            out[k] = v
    if not out and response:
        out["response_keys"] = sorted(response.keys())
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--job", required=True)
    ap.add_argument("--receipt-dir", required=True)
    args = ap.parse_args()

    job_path = Path(args.job)
    job = load_job(job_path)
    receipt_dir = Path(args.receipt_dir)
    receipt_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(prefix="vpd-figma-asset-", delete=False) as tf:
        source_file = Path(tf.name)
    try:
        materialize_source(job["source"], source_file)
        actual_sha = sha256_file(source_file)
        if actual_sha.lower() != str(job["sha256"]).lower():
            die(f"asset SHA-256 mismatch: expected {job['sha256']}, got {actual_sha}")

        response = post_to_figma(job, source_file)
        receipt = {
            "schema_version": "vpd-figma-upload-relay-receipt/v1",
            "job_id": job["job_id"],
            "status": "UPLOAD_POST_COMPLETED",
            "node_id": job["node_id"],
            "source_sha256": actual_sha,
            "source_bytes": source_file.stat().st_size,
            "content_type": job["content_type"],
            "figma_response": sanitize_response(response),
            "completed_at_epoch": int(time.time()),
        }
        receipt_path = receipt_dir / f"{job['job_id']}.json"
        receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"status": receipt["status"], "node_id": job["node_id"], "sha256": actual_sha}, ensure_ascii=False))
        return 0
    finally:
        source_file.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
