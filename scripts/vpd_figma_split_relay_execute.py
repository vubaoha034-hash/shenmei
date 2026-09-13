#!/usr/bin/env python3
"""Execute a split VPD Figma relay task.

The frozen raster is stored in a durable CMS-encrypted asset vault. The short-lived
Figma submit URL is stored separately in a tiny CMS-encrypted trigger. Both are
decrypted only on the GitHub runner using the existing relay private-key secret.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import tarfile
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

NODE_RE = re.compile(r"^\d+:\d+$")
SAFE_RESPONSE_KEYS = {"imageHash", "targetNodeId", "nodeId", "status", "message", "placement"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_extract(tf: tarfile.TarFile, dest: Path) -> None:
    base = dest.resolve()
    for member in tf.getmembers():
        target = (dest / member.name).resolve()
        if os.path.commonpath([str(base), str(target)]) != str(base):
            raise RuntimeError("unsafe archive path")
    tf.extractall(dest)


def decrypt_cms(src: Path, dst: Path, cert: Path, key: Path) -> None:
    subprocess.run(
        [
            "openssl", "cms", "-decrypt", "-binary", "-inform", "DER",
            "-in", str(src), "-recip", str(cert), "-inkey", str(key), "-out", str(dst),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )


def validate_asset_manifest(m: dict, asset: Path) -> None:
    if m.get("schema_version") != "vpd-figma-encrypted-asset-vault/v1":
        raise RuntimeError("unsupported asset-vault schema")
    if not NODE_RE.match(str(m.get("node_id", ""))):
        raise RuntimeError("invalid asset-vault node id")
    if m.get("content_type") not in {"image/png", "image/jpeg", "image/gif", "image/webp"}:
        raise RuntimeError("content type rejected")
    if asset.stat().st_size != int(m.get("source_size", -1)):
        raise RuntimeError("asset size mismatch")
    if sha256_file(asset) != m.get("source_sha256"):
        raise RuntimeError("asset sha256 mismatch")


def validate_trigger(t: dict, asset_manifest: dict, vault_sha256: str) -> None:
    if t.get("schema_version") != "vpd-figma-submit-url-trigger/v1":
        raise RuntimeError("unsupported trigger schema")
    if not NODE_RE.match(str(t.get("node_id", ""))):
        raise RuntimeError("invalid trigger node id")
    if t.get("node_id") != asset_manifest.get("node_id"):
        raise RuntimeError("trigger/asset node mismatch")
    if t.get("source_sha256") != asset_manifest.get("source_sha256"):
        raise RuntimeError("trigger/asset source mismatch")
    if t.get("asset_vault_sha256") != vault_sha256:
        raise RuntimeError("trigger/asset-vault digest mismatch")
    p = urlparse(str(t.get("submit_url", "")))
    if p.scheme != "https" or p.hostname != "mcp.figma.com":
        raise RuntimeError("submit URL host rejected")
    if not p.path.startswith("/mcp/upload/") or not p.path.endswith("/submit"):
        raise RuntimeError("submit URL path rejected")


def write_receipt(path: Path, body: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(body, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Execute split encrypted VPD Figma upload relay task.")
    ap.add_argument("--asset-vault", required=True)
    ap.add_argument("--url-trigger", required=True)
    ap.add_argument("--cert", required=True)
    ap.add_argument("--private-key", required=True)
    ap.add_argument("--receipt", required=True)
    args = ap.parse_args()

    vault = Path(args.asset_vault).resolve()
    trigger = Path(args.url_trigger).resolve()
    cert = Path(args.cert).resolve()
    key = Path(args.private_key).resolve()
    receipt = Path(args.receipt).resolve()
    started = datetime.now(timezone.utc).isoformat()
    base = {
        "schema_version": "vpd-figma-upload-receipt/v1",
        "transport_version": "split-cms-v1",
        "started_at": started,
        "asset_vault_sha256": sha256_file(vault),
        "trigger_file": trigger.name,
    }

    try:
        with tempfile.TemporaryDirectory(prefix="vpd-figma-split-") as td_s:
            td = Path(td_s)
            archive = td / "asset-vault.tar.gz"
            trigger_json = td / "trigger.json"
            decrypt_cms(vault, archive, cert, key)
            decrypt_cms(trigger, trigger_json, cert, key)
            with tarfile.open(archive, "r:gz") as tf:
                safe_extract(tf, td)
            manifest = json.loads((td / "asset_manifest.json").read_text(encoding="utf-8"))
            asset = td / manifest["asset_name"]
            validate_asset_manifest(manifest, asset)
            t = json.loads(trigger_json.read_text(encoding="utf-8"))
            validate_trigger(t, manifest, base["asset_vault_sha256"])

            safe_meta = {
                "task_id": t["task_id"],
                "node_id": manifest["node_id"],
                "source_filename": manifest["source_filename"],
                "source_sha256": manifest["source_sha256"],
                "source_size": manifest["source_size"],
                "content_type": manifest["content_type"],
            }
            response_file = td / "figma-response.json"
            cp = subprocess.run(
                [
                    "curl", "--fail-with-body", "--silent", "--show-error",
                    "--connect-timeout", "15", "--max-time", "90", "--request", "POST",
                    "--header", f"Content-Type: {manifest['content_type']}",
                    "--header", "Accept: application/json",
                    "--data-binary", f"@{asset}",
                    "--output", str(response_file), "--write-out", "%{http_code}", t["submit_url"],
                ],
                text=True,
                capture_output=True,
            )
            http_code = cp.stdout.strip()[-3:] if cp.stdout.strip() else None
            raw = response_file.read_text(encoding="utf-8", errors="replace") if response_file.exists() else ""
            parsed = {}
            try:
                data = json.loads(raw) if raw else {}
                if isinstance(data, dict):
                    parsed = {k: data[k] for k in SAFE_RESPONSE_KEYS if k in data}
            except Exception:
                parsed = {"message": "non-JSON response omitted"}

            if cp.returncode != 0:
                body = {
                    **base, **safe_meta, "status": "UPLOAD_FAILED", "http_status": http_code,
                    "error": "curl upload failed; submit URL intentionally omitted", "response": parsed,
                    "finished_at": datetime.now(timezone.utc).isoformat(),
                }
                write_receipt(receipt, body)
                print(json.dumps({"status": "UPLOAD_FAILED", "task_id": t["task_id"], "node_id": manifest["node_id"]}))
                return 2

            body = {
                **base, **safe_meta, "status": "UPLOAD_PASS", "http_status": http_code,
                "response": parsed, "finished_at": datetime.now(timezone.utc).isoformat(),
            }
            write_receipt(receipt, body)
            print(json.dumps({"status": "UPLOAD_PASS", "task_id": t["task_id"], "node_id": manifest["node_id"], "http_status": http_code}))
            return 0
    except Exception as e:
        body = {
            **base, "status": "RELAY_FAILED", "error": type(e).__name__ + ": " + str(e)[:400],
            "finished_at": datetime.now(timezone.utc).isoformat(),
        }
        write_receipt(receipt, body)
        print(json.dumps({"status": "RELAY_FAILED", "trigger_file": trigger.name}))
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
