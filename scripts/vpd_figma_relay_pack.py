#!/usr/bin/env python3
import argparse, hashlib, json, mimetypes, os, re, shutil, subprocess, tarfile, tempfile
from pathlib import Path
from urllib.parse import urlparse, parse_qs

NODE_RE = re.compile(r"^\d+[:\-]\d+$")
TASK_RE = re.compile(r"^[A-Za-z0-9._-]{1,120}$")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def validate_submit_url(url: str) -> None:
    p = urlparse(url)
    if p.scheme != 'https' or p.hostname != 'mcp.figma.com':
        raise SystemExit('submit URL must be https://mcp.figma.com/...')
    if not p.path.startswith('/mcp/upload/') or not p.path.endswith('/submit'):
        raise SystemExit('submit URL path is not a Figma MCP upload submit endpoint')
    q = parse_qs(p.query)
    mode = q.get('scaleMode', ['FILL'])[0]
    if mode not in {'FILL', 'FIT', 'TILE'}:
        raise SystemExit('unsupported scaleMode in submit URL')


def main() -> int:
    ap = argparse.ArgumentParser(description='Package one Figma upload task as CMS-encrypted payload.')
    ap.add_argument('--cert', required=True)
    ap.add_argument('--image', required=True)
    ap.add_argument('--submit-url', required=True)
    ap.add_argument('--node-id', required=True)
    ap.add_argument('--task-id', required=True)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()

    cert = Path(args.cert).resolve()
    image = Path(args.image).resolve()
    out = Path(args.output).resolve()
    if not cert.is_file() or not image.is_file():
        raise SystemExit('certificate or image does not exist')
    if not NODE_RE.match(args.node_id):
        raise SystemExit('invalid Figma node id')
    if not TASK_RE.match(args.task_id):
        raise SystemExit('invalid task id')
    validate_submit_url(args.submit_url)

    mime = mimetypes.guess_type(image.name)[0] or 'application/octet-stream'
    if mime not in {'image/png', 'image/jpeg', 'image/gif', 'image/webp'}:
        raise SystemExit(f'unsupported raster MIME type: {mime}')

    with tempfile.TemporaryDirectory(prefix='vpd-figma-pack-') as td:
        td = Path(td)
        staged_image = td / ('asset' + image.suffix.lower())
        shutil.copyfile(image, staged_image)
        manifest = {
            'schema_version': 'vpd-figma-upload-task/v1',
            'task_id': args.task_id,
            'node_id': args.node_id.replace('-', ':'),
            'submit_url': args.submit_url,
            'content_type': mime,
            'source_filename': image.name,
            'source_sha256': sha256_file(image),
            'source_size': image.stat().st_size,
            'asset_name': staged_image.name,
        }
        (td / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
        archive = td / 'task.tar.gz'
        with tarfile.open(archive, 'w:gz') as tf:
            tf.add(td / 'manifest.json', arcname='manifest.json')
            tf.add(staged_image, arcname=staged_image.name)

        out.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([
            'openssl', 'cms', '-encrypt', '-binary', '-aes-256-cbc',
            '-in', str(archive), '-out', str(out), '-outform', 'DER', str(cert)
        ], check=True, stdout=subprocess.DEVNULL)

    safe = {
        'status': 'PACKED', 'task_id': args.task_id, 'node_id': args.node_id.replace('-', ':'),
        'source_filename': image.name, 'source_sha256': sha256_file(image),
        'source_size': image.stat().st_size, 'output': str(out), 'encrypted_size': out.stat().st_size,
    }
    print(json.dumps(safe, ensure_ascii=False))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
