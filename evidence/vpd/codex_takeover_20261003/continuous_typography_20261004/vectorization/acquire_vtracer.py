"""Acquire a pinned official wheel/source to private cache; do not install globally."""
from pathlib import Path
from urllib.request import Request, urlopen
import hashlib, io, json, tarfile, zipfile

REPO = Path(__file__).resolve().parents[5]
REPORT = Path(__file__).resolve().parent
PRIVATE = REPO / '.liu-visual-private/dependencies/vtracer_0_6_15_cp312'
PRIVATE.mkdir(parents=True, exist_ok=True)
for path in (REPORT, PRIVATE):
    if not path.resolve().is_relative_to(REPO.resolve()):
        raise ValueError('outside repository')

def get(url):
    with urlopen(Request(url, headers={'User-Agent':'Codex-bounded-vectorization-check'}), timeout=25) as response:
        return response.read()

metadata = json.loads(get('https://pypi.org/pypi/vtracer/0.6.15/json'))
files = [f for f in metadata['urls'] if f['filename'].endswith('cp312-cp312-win_amd64.whl') or f['packagetype']=='sdist']
assert len(files)==2
records=[]
for item in files:
    raw=get(item['url']); digest=hashlib.sha256(raw).hexdigest()
    assert digest==item['digests']['sha256']
    path=PRIVATE/item['filename']
    if path.exists(): assert path.read_bytes()==raw
    else: path.write_bytes(raw)
    records.append({'filename':item['filename'],'url':item['url'],'path':str(path),'sha256':digest,'bytes':len(raw)})

source=next(r for r in records if r['filename'].endswith('.tar.gz'))
source_members={}
with tarfile.open(source['path'],'r:gz') as archive:
    for member in archive.getmembers():
        if member.isfile():
            content=archive.extractfile(member).read()
            source_members[member.name]={'sha256':hashlib.sha256(content).hexdigest(),'bytes':len(content)}
            if member.name.endswith(('.cargo_vcs_info.json','Cargo.toml','pyproject.toml','LICENSE','README.md','lib.rs')):
                target=(PRIVATE/'source'/member.name).resolve()
                assert target.is_relative_to(PRIVATE.resolve())
                target.parent.mkdir(parents=True,exist_ok=True); target.write_bytes(content)

wheel=next(r for r in records if r['filename'].endswith('.whl'))
wheel_texts={}
with zipfile.ZipFile(wheel['path']) as archive:
    for name in archive.namelist():
        if name.endswith(('METADATA','WHEEL','LICENSE','LICENSE-MIT','LICENSE-APACHE')):
            wheel_texts[name]=archive.read(name).decode('utf-8')
result={'pypi_version':metadata['info']['version'],'license_expression':metadata['info'].get('license_expression'),
        'files':records,'source_members':source_members,'wheel_metadata':wheel_texts,'requires_dist':metadata['info'].get('requires_dist')}
(REPORT/'UPSTREAM_MANIFEST.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'version':result['pypi_version'],'license_expression':result['license_expression'],'files':records,
                  'source_members':list(source_members),'wheel_metadata_files':list(wheel_texts)},ensure_ascii=False,indent=2))
