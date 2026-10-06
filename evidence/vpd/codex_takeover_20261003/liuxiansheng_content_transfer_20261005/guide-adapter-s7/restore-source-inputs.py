"""Restore exact source inputs from the original Drive archive; no design runs."""
import argparse,pathlib,hashlib,json,zipfile
p=argparse.ArgumentParser();p.add_argument('--root',type=pathlib.Path,required=True);p.add_argument('--archive',type=pathlib.Path,required=True);p.add_argument('--destination',type=pathlib.Path,required=True);a=p.parse_args()
root=a.root.resolve();destination=a.destination.resolve();destination.relative_to(root/'.liu-visual-private')
expected='535cae9b6f7367ed3faf328c040a1d856b1bdb75962db6992890eba040f28861'
assert hashlib.sha256(a.archive.read_bytes()).hexdigest()==expected,'ARCHIVE_HASH_MISMATCH'
spec=json.loads((pathlib.Path(__file__).parent/'SOURCE.json').read_text(encoding='utf8'));members={x['file']:x['sha256'] for x in spec['exact_inputs']};data={}
with zipfile.ZipFile(a.archive) as z:
 assert set(z.namelist())==set(members) and len(z.namelist())==len(members),'MEMBERS_MISMATCH'
 for name,sha in members.items():
  assert pathlib.PurePosixPath(name).name==name and '\\' not in name and '/' not in name
  data[name]=z.read(name);assert hashlib.sha256(data[name]).hexdigest()==sha,'MEMBER_HASH_MISMATCH'
  target=destination/name
  if target.exists():assert target.read_bytes()==data[name],'EXISTING_INPUT_DIFFERS'
destination.mkdir(parents=True,exist_ok=True)
for name,raw in data.items():
 target=destination/name
 if not target.exists():target.write_bytes(raw)
print(json.dumps({'result':'PASS','archive_sha256':expected,'restored_exact_inputs':len(data),'destination':str(destination),'imagegen_calls':0,'formal_versions_created':0}))
