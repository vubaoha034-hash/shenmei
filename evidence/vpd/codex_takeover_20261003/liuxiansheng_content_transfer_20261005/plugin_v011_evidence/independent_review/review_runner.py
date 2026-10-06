from pathlib import Path
import base64
import difflib
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone

out = Path(__file__).resolve().parent
repo = out.parents[1]
old = repo / 'plugins/visual-aesthetic-workflow'
new = old / 'v0.1.1'
current = '3e6a5638c2af2bedcfd66d23fabf6aa7d35c957d'
legacy = '4d128f7b44dc43163f021b5717f5e003ca70a323'
node = Path(r'C:\Users\Administrator\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe')
files = ['.openai/hosting.json','README.md','SKILL.md','baseline-core-v0.1.0.mjs','build.mjs','core.mjs','core.test.mjs','entry.test.mjs','package.json','pnpm-lock.yaml','worker.mjs','worker.test.mjs']
sha = lambda data: hashlib.sha256(data).hexdigest()
def git(*args):
    return subprocess.check_output(['git', *args], cwd=repo)
def write(path, data):
    path = out / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
def save(path, data):
    write(path, (json.dumps(data, ensure_ascii=False, indent=2)+'\n').encode('utf-8'))
def run(label, args, cwd=out):
    completed = subprocess.run(args, cwd=cwd, capture_output=True)
    write('logs/'+label+'.stdout.txt', completed.stdout)
    write('logs/'+label+'.stderr.txt', completed.stderr)
    record = {'label': label, 'command': [str(x) for x in args], 'cwd':str(cwd), 'exit_code':completed.returncode, 'stdout_sha256':sha(completed.stdout),'stderr_sha256':sha(completed.stderr)}
    commands.append(record)
    return completed

commands=[]
source=[]
for name in files:
    data=(new/name).read_bytes()
    source.append({'path':'plugins/visual-aesthetic-workflow/v0.1.1/'+name,'bytes':len(data),'sha256':sha(data)})
    write('source_snapshot/v0.1.1/'+name,data)
save('FINAL_SOURCE_MANIFEST.json',{'schema':'vpd-independent-plugin-source-snapshot/v1','checked_at':datetime.now(timezone.utc).isoformat(),'files':source})

old_records=[]
for raw in git('ls-tree','-r','--name-only',current,'plugins/visual-aesthetic-workflow').decode().splitlines():
    data=git('show',current+':'+raw)
    working=(repo/raw).read_bytes()
    expected_blob=git('rev-parse',current+':'+raw).decode().strip()
    actual_blob=git('hash-object','--path='+raw,str(repo/raw)).decode().strip()
    old_records.append({'path':raw,'git_blob':expected_blob,'workingtree_filtered_git_blob':actual_blob,'git_bytes_sha256':sha(data),'workingtree_raw_sha256':sha(working),'raw_bytes_equal':working==data,'published_git_equivalent':actual_blob==expected_blob,'workingtree_crlf_count':working.count(b'\r\n')})
    write('source_snapshot/old_published/'+raw.removeprefix('plugins/visual-aesthetic-workflow/'),data)
    write('source_snapshot/old_working/'+raw.removeprefix('plugins/visual-aesthetic-workflow/'),working)
save('OLD_SOURCE_PRESERVATION.json',{'fixed_commit':current,'file_count':len(old_records),'failures':[x for x in old_records if not x['published_git_equivalent']],'files':old_records})
assert len(old_records)==15
assert all(x['published_git_equivalent'] for x in old_records)
assert (new/'baseline-core-v0.1.0.mjs').read_bytes()==(old/'core.mjs').read_bytes()

diff_records=[]
for name in ['core.mjs','worker.mjs','build.mjs','core.test.mjs','worker.test.mjs','package.json','pnpm-lock.yaml','.openai/hosting.json','SKILL.md','README.md']:
    before=(old/name).read_bytes()
    after=(new/name).read_bytes()
    diff=''.join(difflib.unified_diff(before.decode().splitlines(keepends=True),after.decode().splitlines(keepends=True),fromfile='0.1.0/'+name,tofile='0.1.1/'+name))
    write('diffs/'+name.replace('/','_')+'.diff.txt',diff.encode())
    diff_records.append({'path':name,'before_sha256':sha(before),'after_sha256':sha(after),'raw_equal':before==after,'diff_sha256':sha(diff.encode())})
save('SOURCE_DIFFS.json',diff_records)

remote=[]
for index in [2,3,4,5]:
    raw=json.loads((out/'raw_remote'/f'{index:02}.json').read_text('utf-8'))
    result=raw['response']['structuredContent']
    data=base64.b64decode(result['content'])
    path=raw['request']['path']
    local=git('show',current+':'+path)
    git_blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    remote.append({'path':path,'fixed_commit':current,'bytes':len(data),'remote_sha256':sha(data),'local_git_blob_sha256':sha(local),'api_git_blob':result['sha'],'calculated_git_blob':git_blob,'bytes_equal':data==local,'git_blob_equal':git_blob==result['sha']})
    write('remote_files/'+path,data)
assert all(x['bytes_equal'] and x['git_blob_equal'] for x in remote)
save('REMOTE_NATIVE_COMPARISONS.json',{'successful_reads':len(remote),'initial_parameter_errors':2,'bounded_path_correction':'initial lock/checkpoint request omitted vpd segment; corrected once from actual source PATHS','files':remote})

for label in ['PLUGIN_V011_LIVE_GITHUB_READBACK.json','PLUGIN_V011_LIVE_GITHUB_DIAGNOSTIC.json']:
    data=(repo/'.liu-visual-private'/label).read_bytes()
    write('parent_transport_records/'+label,data)

# The build runs only in our private copy. It never writes a dist directory in release source.
build_copy=out/'build_copy'
for name in ['build.mjs','worker.mjs','core.mjs','package.json','.openai/hosting.json']:
    target=build_copy/name
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes((new/name).read_bytes())
build=run('build',[str(node),'build.mjs'],build_copy)
assert build.returncode==0
assert (build_copy/'dist/server/index.js').read_bytes()==(new/'worker.mjs').read_bytes()
assert (build_copy/'dist/server/core.mjs').read_bytes()==(new/'core.mjs').read_bytes()
assert (build_copy/'dist/.openai/hosting.json').read_bytes()==(new/'.openai/hosting.json').read_bytes()

package=json.loads((new/'package.json').read_text('utf-8'))
assert package['version']=='0.1.1'
assert package['scripts']['test']=='node --test core.test.mjs worker.test.mjs entry.test.mjs'
tests=run('final_source_tests',[str(node),'--test',str(new/'core.test.mjs'),str(new/'worker.test.mjs'),str(new/'entry.test.mjs')])
independent=run('independent_cases',[str(node),str(out/'independent_cases.mjs')])

after=[]
for item in source:
    after.append({'path':item['path'],'before_sha256':item['sha256'],'after_sha256':sha((repo/item['path']).read_bytes()),'unchanged':item['sha256']==sha((repo/item['path']).read_bytes())})
for item in old_records:
    after.append({'path':item['path'],'before_sha256':item['workingtree_raw_sha256'],'after_sha256':sha((repo/item['path']).read_bytes()),'unchanged':item['workingtree_raw_sha256']==sha((repo/item['path']).read_bytes())})
save('BEFORE_AFTER_SOURCE_STABILITY.json',{'file_count':len(after),'all_unchanged':all(x['unchanged'] for x in after),'files':after})
write('logs/git_status_after.txt',git('status','--short','--branch'))
save('COMMAND_RESULTS.json',commands)
summary={'fixed_commit':current,'parent':git('show','-s','--format=%P',current).decode().strip(),'source_files':len(source),'old_published_files_verified':len(old_records),'remote_native_files_verified':len(remote),'build_exit':build.returncode,'tests_exit':tests.returncode,'independent_exit':independent.returncode,'source_stable':all(x['unchanged'] for x in after)}
save('RUN_SUMMARY.json',summary)
print(json.dumps(summary,ensure_ascii=False,indent=2))
if tests.returncode or independent.returncode or not summary['source_stable']:
    sys.exit(1)
