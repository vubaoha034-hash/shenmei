"""Acquire the matching fontTools source and one licensed CJK font sample."""
from pathlib import Path
import hashlib
import json
from urllib.request import Request, urlopen
from datetime import datetime, timezone
import fontTools

ROOT = Path(__file__).resolve().parent
HEADERS = {"User-Agent": "Codex-Bounded-Font-Research", "Accept": "application/vnd.github+json"}

def get(url):
    with urlopen(Request(url, headers=HEADERS), timeout=45) as response:
        return response.read()

def put(relative, data, url):
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(path)
    path.write_bytes(data)
    return {"path": relative, "url": url, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}

source_manifest = json.loads((ROOT / "UPSTREAM_SOURCE_MANIFEST.json").read_text())
serif = next(r for r in source_manifest["repositories"] if r["repository"] == "adobe-fonts/source-han-serif")
license_text = (ROOT / "upstream/adobe-fonts/source-han-serif/LICENSE.txt").read_text()
assert "SIL OPEN FONT LICENSE Version 1.1" in license_text
tag = fontTools.__version__
commit = json.loads(get(f"https://api.github.com/repos/fonttools/fonttools/commits/{tag}"))
sha = commit["sha"]
manifest = {"created_at_utc": datetime.now(timezone.utc).isoformat(), "fonttools_runtime_version": tag, "fonttools_source_commit": sha, "fonttools_source_commit_date": commit["commit"]["committer"]["date"], "fonttools_source_license": "MIT; external notices preserved", "font_source_commit": serif["commit"], "font_license": "SIL OFL 1.1; Reserved Font Name Source", "files": []}
paths = ["LICENSE", "LICENSE.external", "README.rst", "Lib/fontTools/ttLib/ttFont.py", "Lib/fontTools/pens/boundsPen.py", "Lib/fontTools/pens/statisticsPen.py", "Lib/fontTools/pens/momentsPen.py", "Lib/fontTools/pens/recordingPen.py", "Lib/fontTools/pens/svgPathPen.py"]
for path in paths:
    url = f"https://raw.githubusercontent.com/fonttools/fonttools/{sha}/{path}"
    manifest["files"].append(put(f"upstream/fonttools/fonttools/{path}", get(url), url))
    print(path, flush=True)
font_path = "OTF/SimplifiedChinese/SourceHanSerifSC-Regular.otf"
url = f"https://raw.githubusercontent.com/adobe-fonts/source-han-serif/{serif['commit']}/{font_path}"
font_data = get(url)
assert font_data[:4] == b"OTTO", "Expected real OpenType CFF binary, not an LFS pointer"
manifest["files"].append(put(f"upstream/adobe-fonts/source-han-serif/{font_path}", font_data, url))
put("FONTTOOLS_FONT_SOURCE_MANIFEST.json", json.dumps(manifest, ensure_ascii=False, indent=2).encode(), "local acquisition record")
print("Font bytes", len(font_data), "SHA-256", hashlib.sha256(font_data).hexdigest(), flush=True)
