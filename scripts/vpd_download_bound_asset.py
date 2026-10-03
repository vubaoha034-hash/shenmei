"""Restore a pinned private PNG from a fresh official Figma rawImages URL.

No re-render, no public upload. HTTP 202 is pending, never an image. A bounded
poll accepts only status 200, PNG signature, and the manifest's exact SHA.
"""
import argparse, hashlib, json, pathlib, time, urllib.parse, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]

def download(url, expected, attempts=4):
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != 'https' or parsed.hostname != 'www.figma.com' or not parsed.path.startswith('/api/mcp/asset/'):
        raise ValueError('OFFICIAL_FIGMA_ASSET_URL_REQUIRED')
    for attempt in range(attempts):
        # Figma asset service returns pending202 to Python's default UA even
        # when the asset is ready. A conventional UA was verified by actual
        # same-URL A/B reads; authentication/TLS and exact-byte checks remain.
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(request, timeout=25) as response:
            status = response.status
            content = response.read()
        if status == 202:
            if attempt + 1 < attempts:
                time.sleep(2)
                continue
            raise ValueError('ASSET_PENDING_202_REACQUIRE_URL_NO_SUCCESS_CLAIM')
        if status != 200 or not content.startswith(b'\x89PNG\r\n\x1a\n'):
            raise ValueError('HTTP_200_ACTUAL_PNG_REQUIRED')
        actual = hashlib.sha256(content).hexdigest()
        if actual != expected:
            raise ValueError('EXACT_PINNED_ASSET_SHA_MISMATCH')
        return content, attempt + 1
    raise AssertionError('unreachable')

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--url-file', required=True, help='Private JSON containing url')
    p.add_argument('--sha256', required=True)
    p.add_argument('--dest', required=True, help='Repository-relative private path')
    a = p.parse_args()
    private = (ROOT / '.liu-visual-private').resolve()
    dest = (ROOT / a.dest).resolve()
    if not dest.is_relative_to(private):
        raise ValueError('PRIVATE_DESTINATION_REQUIRED')
    content, attempts = download(json.loads(pathlib.Path(a.url_file).read_text(encoding='utf-8'))['url'], a.sha256)
    if dest.exists() and hashlib.sha256(dest.read_bytes()).hexdigest() != a.sha256:
        raise ValueError('DIFFERENT_EXISTING_PRIVATE_ASSET_DO_NOT_OVERWRITE')
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(content)
    print(json.dumps({'path': a.dest, 'sha256': a.sha256, 'size_bytes': len(content),
                      'status': 'RESTORED_EXACT_ORIGINAL_BYTES', 'attempts': attempts}))

if __name__ == '__main__':
    main()
