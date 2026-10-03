#!/usr/bin/env python3
"""Restore declared Drive PNG bytes to the private cache; never write task state.

The caller supplies actual connected-Drive fetch(download_raw_file=True,
include_base64=True) results as {"entries":[{"drive_id": "...",
"raw_base64": "..."}]}. No signed URL, token, generation or upload is needed.
"""
import argparse,base64,hashlib,json,pathlib,os,sys,tempfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from visual_memory.vpd_task_lock import check_ref,read
UNIT='CHAZUO_APPROVED_SOURCE_TYPOGRAPHY_20261003_R1'

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--bundle',required=True)
    args=parser.parse_args()
    lock=read(ROOT,'continuity/vpd/CURRENT_TASK_LOCK.json')
    unit=lock['codex_takeover']['worker_continuation']
    if unit['unit_id']!=UNIT:raise ValueError('CURRENT_UNIT_CHANGED')
    source=unit['frozen_source']
    declared={source['drive_id']:{'path':source['local_path'],'sha256':source['sha256']}}
    for version in unit['versions']:
        archive_ref=version.get('drive_archive')
        if not archive_ref:continue
        check_ref(ROOT,archive_ref);archive=read(ROOT,archive_ref['path'])
        if archive['poster_sha256']!=version['export']['sha256']:raise ValueError('ARCHIVE_VERSION_IDENTITY_CONFLICT')
        declared[archive['drive_id']]=version['export']
    packet=json.loads(pathlib.Path(args.bundle).read_text(encoding='utf-8'))
    entries=packet['entries']
    if not entries or len({e['drive_id'] for e in entries})!=len(entries):raise ValueError('EMPTY_OR_DUPLICATE_INPUT')
    staged=[]
    private=(ROOT/'.liu-visual-private').resolve()
    if private==ROOT or not private.is_relative_to(ROOT):raise ValueError('PRIVATE_CACHE_ESCAPES_REPOSITORY')
    for entry in entries:
        if entry['drive_id'] not in declared:raise ValueError('UNDECLARED_DRIVE_FILE')
        binding=declared[entry['drive_id']]
        target=(ROOT/binding['path']).resolve()
        if not target.is_relative_to(private) or not target.is_relative_to(ROOT):raise ValueError('PRIVATE_CACHE_ONLY')
        relative=str(target.relative_to(ROOT)).replace('\\','/')
        data=base64.b64decode(entry['raw_base64'],validate=True)
        if not data.startswith(b'\x89PNG\r\n\x1a\n') or hashlib.sha256(data).hexdigest()!=binding['sha256']:
            raise ValueError('ACTUAL_DRIVE_BYTES_DO_NOT_MATCH_NATIVE_IDENTITY')
        if target.exists() and target.read_bytes()!=data:raise ValueError('EXISTING_PRIVATE_CACHE_CONFLICT')
        staged.append((entry['drive_id'],target,data,binding['sha256'],relative))
    report=[]
    for drive_id,target,data,expected,relative in staged:
        target.parent.mkdir(parents=True,exist_ok=True)
        if target.parent.resolve()!=target.parent or not target.parent.is_relative_to(private):raise ValueError('CACHE_PARENT_CHANGED')
        if not target.exists():
            descriptor,name=tempfile.mkstemp(prefix='.drive-restore-',suffix='.tmp',dir=target.parent)
            temp=pathlib.Path(name)
            try:
                with os.fdopen(descriptor,'wb') as stream:stream.write(data)
                if hashlib.sha256(temp.read_bytes()).hexdigest()!=expected:raise ValueError('STAGED_READBACK_FAILED')
                os.replace(temp,target)
            finally:
                if temp.exists():temp.unlink()
        if hashlib.sha256(target.read_bytes()).hexdigest()!=expected:raise ValueError('RESTORE_READBACK_FAILED')
        report.append({'drive_id':drive_id,'path':relative,'sha256':expected,'bytes':len(data)})
    print(json.dumps({'result':'PASS','restored':report,'business_state_writes':0,'new_design_versions':0},ensure_ascii=False))

if __name__=='__main__':main()
