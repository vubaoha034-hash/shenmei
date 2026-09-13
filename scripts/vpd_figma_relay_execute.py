#!/usr/bin/env python3
import argparse, hashlib, json, os, re, subprocess, tarfile, tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

NODE_RE = re.compile(r"^\d+:\d+$")
SAFE_RESPONSE_KEYS = {'imageHash', 'targetNodeId', 'nodeId', 'status', 'message', 'placement'}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def safe_extract(tf: tarfile.TarFile, dest: Path) -> None:
    base = dest.resolve()
    for member in tf.getmembers():
        target = (dest / member.name).resolve()
        if os.path.commonpath([str(base), str(target)]) != str(base):
            raise RuntimeError('unsafe archive path')
    tf.extractall(dest)


def validate_manifest(m: dict, asset: Path) -> None:
    if m.get('schema_version') != 'vpd-figma-upload-task/v1':
        raise RuntimeError('unsupported task schema')
    if not NODE_RE.match(str(m.get('node_id', ''))):
        raise RuntimeError('invalid node id')
    p = urlparse(str(m.get('submit_url', '')))
    if p.scheme != 'https' or p.hostname != 'mcp.figma.com':
        raise RuntimeError('submit URL host rejected')
    if not p.path.startswith('/mcp/upload/') or not p.path.endswith('/submit'):
        raise RuntimeError('submit URL path rejected')
    if m.get('content_type') not in {'image/png', 'image/jpeg', 'image/gif', 'image/webp'}:
        raise RuntimeError('content type rejected')
    if asset.stat().st_size != int(m.get('source_size', -1)):
        raise RuntimeError('asset size mismatch')
    if sha256_file(asset) != m.get('source_sha256'):
        raise RuntimeError('asset sha256 mismatch')


def write_receipt(path: Path, body: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(body, ensure_ascii=False, indent=2, sort_keys=True) + '\n', encoding='utf-8')


def main() -> int:
    ap = argparse.ArgumentParser(description='Decrypt and execute one VPD Figma upload relay task.')
    ap.add_argument('--task', required=True)
    ap.add_argument('--cert', required=True)
    ap.add_argument('--private-key', required=True)
    ap.add_argument('--receipt', required=True)
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    task = Path(args.task).resolve(); cert = Path(args.cert).resolve(); key = Path(args.private_key).resolve(); receipt = Path(args.receipt).resolve()
    started = datetime.now(timezone.utc).isoformat()
    base_receipt = {'schema_version':'vpd-figma-upload-receipt/v1','started_at':started,'task_file':task.name}
    try:
        with tempfile.TemporaryDirectory(prefix='vpd-figma-exec-') as td_s:
            td = Path(td_s); archive = td / 'task.tar.gz'
            subprocess.run([
                'openssl','cms','-decrypt','-binary','-inform','DER','-in',str(task),
                '-recip',str(cert),'-inkey',str(key),'-out',str(archive)
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            with tarfile.open(archive, 'r:gz') as tf:
                safe_extract(tf, td)
            m = json.loads((td / 'manifest.json').read_text(encoding='utf-8'))
            asset = td / m['asset_name']
            validate_manifest(m, asset)
            safe_meta = {
                'task_id': m['task_id'], 'node_id': m['node_id'], 'source_filename': m['source_filename'],
                'source_sha256': m['source_sha256'], 'source_size': m['source_size'], 'content_type': m['content_type']
            }
            if args.dry_run:
                body = {**base_receipt, **safe_meta, 'status':'DRY_RUN_PASS', 'finished_at':datetime.now(timezone.utc).isoformat()}
                write_receipt(receipt, body); print(json.dumps({'status':'DRY_RUN_PASS','task_id':m['task_id'],'node_id':m['node_id']})); return 0

            response_file = td / 'figma-response.json'
            cp = subprocess.run([
                'curl','--fail-with-body','--silent','--show-error','--connect-timeout','15','--max-time','90',
                '--request','POST','--header',f"Content-Type: {m['content_type']}", '--header','Accept: application/json',
                '--data-binary',f"@{asset}", '--output',str(response_file), '--write-out','%{http_code}', m['submit_url']
            ], text=True, capture_output=True)
            http_code = cp.stdout.strip()[-3:] if cp.stdout.strip() else None
            raw = response_file.read_text(encoding='utf-8', errors='replace') if response_file.exists() else ''
            parsed = {}
            try:
                data = json.loads(raw) if raw else {}
                if isinstance(data, dict): parsed = {k:data[k] for k in SAFE_RESPONSE_KEYS if k in data}
            except Exception:
                parsed = {'message':'non-JSON response omitted'}
            if cp.returncode != 0:
                body = {**base_receipt, **safe_meta, 'status':'UPLOAD_FAILED','http_status':http_code,
                        'error':'curl upload failed; submit URL intentionally omitted','response':parsed,
                        'finished_at':datetime.now(timezone.utc).isoformat()}
                write_receipt(receipt, body); print(json.dumps({'status':'UPLOAD_FAILED','task_id':m['task_id'],'node_id':m['node_id']})); return 2
            body = {**base_receipt, **safe_meta, 'status':'UPLOAD_PASS','http_status':http_code,'response':parsed,
                    'finished_at':datetime.now(timezone.utc).isoformat()}
            write_receipt(receipt, body); print(json.dumps({'status':'UPLOAD_PASS','task_id':m['task_id'],'node_id':m['node_id'],'http_status':http_code})); return 0
    except Exception as e:
        body = {**base_receipt,'status':'RELAY_FAILED','error':type(e).__name__ + ': ' + str(e)[:400],
                'finished_at':datetime.now(timezone.utc).isoformat()}
        write_receipt(receipt, body); print(json.dumps({'status':'RELAY_FAILED','task_file':task.name})); return 3

if __name__ == '__main__':
    raise SystemExit(main())
