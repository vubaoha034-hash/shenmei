"""One bounded, pinned upstream snapshot and Codex metadata adaptation."""
import hashlib,json,pathlib,urllib.request

ROOT=pathlib.Path(__file__).resolve().parents[1]
COMMIT='d3ee81913e5e179273313345847a2a4f42449bd2'
BASE='https://raw.githubusercontent.com/anthropics/knowledge-work-plugins/'+COMMIT+'/'
INSTALL=pathlib.Path('C:/Users/Administrator/.codex/skills/design-critique')
DEST=ROOT/'skills/design-critique'

def main():
    files={'SKILL.md':'design/skills/design-critique/SKILL.md','LICENSE':'LICENSE',
           'CONNECTORS.md':'design/CONNECTORS.md','README.md':'design/README.md'}
    contents={}
    for name,remote in files.items():
        req=urllib.request.Request(BASE+remote,headers={'User-Agent':'vpd-review-skill-pinned-snapshot'})
        with urllib.request.urlopen(req,timeout=25) as response:
            if response.status!=200:raise ValueError('UPSTREAM_HTTP_FAILED')
            contents[name]=response.read()
    # This is the already installed, unmodified skill from the official helper.
    if (INSTALL/'SKILL.md').read_bytes()!=contents['SKILL.md']:
        raise ValueError('INSTALLED_PINNED_SNAPSHOT_MISMATCH')
    active=contents['SKILL.md'].decode('utf-8')
    active=active.replace('argument-hint: "<Figma URL, screenshot, or description>"\n','')
    active=active.replace('[CONNECTORS.md](../../CONNECTORS.md)',
                          '[CONNECTORS.md](references/CONNECTORS.md)')
    active_bytes=active.encode('utf-8')
    (DEST/'upstream').mkdir(parents=True,exist_ok=True)
    (DEST/'references').mkdir(exist_ok=True)
    (INSTALL/'references').mkdir(exist_ok=True)
    for name,content in contents.items():(DEST/'upstream'/name).write_bytes(content)
    for base in [DEST,INSTALL]:
        (base/'SKILL.md').write_bytes(active_bytes)
        (base/'LICENSE').write_bytes(contents['LICENSE'])
        (base/'references/CONNECTORS.md').write_bytes(contents['CONNECTORS.md'])
    result={'source_repository':'anthropics/knowledge-work-plugins','commit':COMMIT,
      'license':'Apache-2.0','fixed_snapshot_actual_bytes_read':True,
      'official_installer_original_matches_fixed_raw':True,
      'install_path':str(INSTALL),'discovery':'Codex user skills directory; next-turn discovery, this turn explicit reading',
      'adaptations':['Remove unsupported argument-hint YAML metadata','Repair packaged CONNECTORS relative link'],
      'upstream_core_changed':False,'installed_sha256':hashlib.sha256(active_bytes).hexdigest(),
      'files':[{'name':name,'source_url':BASE+files[name],'sha256':hashlib.sha256(content).hexdigest()} for name,content in contents.items()]}
    (DEST/'SOURCE_SNAPSHOT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
