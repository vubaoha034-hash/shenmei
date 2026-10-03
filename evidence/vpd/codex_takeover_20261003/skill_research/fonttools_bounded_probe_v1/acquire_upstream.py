"""Download selected official source files; do not execute any downloaded code."""
from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
HEADER = {"User-Agent": "Codex-Bounded-Font-Research", "Accept": "application/vnd.github+json"}

def get(url):
    with urlopen(Request(url, headers=HEADER), timeout=25) as response:
        return response.read()

def save(relative, data):
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(f"Append-only acquisition refuses overwrite: {path}")
    path.write_bytes(data)
    return {"path": relative, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}

repositories = [
    ("anthropics/skills", "main", ["README.md", "THIRD_PARTY_NOTICES.md", "skills/canvas-design/SKILL.md", "skills/canvas-design/LICENSE.txt", "skills/frontend-design/SKILL.md", "skills/frontend-design/LICENSE.txt", "skills/skill-creator/SKILL.md", "skills/skill-creator/LICENSE.txt"]),
    ("adobe-fonts/source-han-serif", "release", ["README.md", "LICENSE.txt"]),
    ("harfbuzz/harfbuzz", "main", ["README.md", "COPYING"]),
]
manifest = {"retrieved_at_utc": datetime.now(timezone.utc).isoformat(), "fixed_project_source_commit": "003cfdfaa6481f8ac41cc46f56539bb4782ec34b", "repositories": [], "errors": []}
for repo, ref, paths in repositories:
    try:
        commit = json.loads(get(f"https://api.github.com/repos/{repo}/commits/{ref}"))
        sha = commit["sha"]
        entry = {"repository": repo, "requested_ref": ref, "commit": sha, "commit_date": commit["commit"]["committer"]["date"], "files": []}
        for path in paths:
            url = f"https://raw.githubusercontent.com/{repo}/{sha}/{path}"
            try:
                record = save(f"upstream/{repo}/{path}", get(url))
                record["url"] = url
                entry["files"].append(record)
            except Exception as error:
                manifest["errors"].append({"url": url, "error": str(error)})
        if repo == "anthropics/skills":
            for path in ["skills", "skills/canvas-design/canvas-fonts"]:
                url = f"https://api.github.com/repos/{repo}/contents/{path}?ref={sha}"
                listing = json.loads(get(url))
                record = save(f"upstream/{repo}/{path.replace('/', '_')}_listing.json", json.dumps([{"name": f["name"], "type": f["type"], "sha": f["sha"]} for f in listing], ensure_ascii=False, indent=2).encode())
                record["url"] = url
                entry["files"].append(record)
        manifest["repositories"].append(entry)
        print(repo, sha, "source files", len(entry["files"]), flush=True)
    except Exception as error:
        manifest["errors"].append({"repository": repo, "error": str(error)})
        print(repo, type(error).__name__, str(error), flush=True)
save("UPSTREAM_SOURCE_MANIFEST.json", json.dumps(manifest, ensure_ascii=False, indent=2).encode())
print("Errors:", manifest["errors"], flush=True)
