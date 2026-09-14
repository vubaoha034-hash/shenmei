#!/usr/bin/env python3
"""Use an immutable historical encrypted Figma task only as the frozen raster source.

The historical task's stale submit URL is ignored. A fresh URL arrives separately as a
small CMS-encrypted trigger. Plain image bytes and URLs are only materialized on the
GitHub runner and never committed.
"""
from __future__ import annotations
import argparse, hashlib, json, os, re, subprocess, tarfile, tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

NODE_RE=re.compile(r"^\d+:\d+$")
SAFE_RESPONSE_KEYS={'imageHash','targetNodeId','nodeId','status','message','placement'}

def sha256_file(p:Path)->str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for c in iter(lambda:f.read(1024*1024),b''): h.update(c)
    return h.hexdigest()

def safe_extract(tf:tarfile.TarFile,dest:Path)->None:
    base=dest.resolve()
    for m in tf.getmembers():
        target=(dest/m.name).resolve()
        if os.path.commonpath([str(base),str(target)])!=str(base): raise RuntimeError('unsafe archive path')
    tf.extractall(dest)

def decrypt(src:Path,dst:Path,cert:Path,key:Path)->None:
    subprocess.run(['openssl','cms','-decrypt','-binary','-inform','DER','-in',str(src),'-recip',str(cert),'-inkey',str(key),'-out',str(dst)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)

def write_receipt(p:Path,body:dict)->None:
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(body,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--legacy-task',required=True); ap.add_argument('--url-trigger',required=True)
    ap.add_argument('--cert',required=True); ap.add_argument('--private-key',required=True); ap.add_argument('--receipt',required=True)
    ap.add_argument('--expected-node-id',required=True); ap.add_argument('--expected-source-sha256',required=True)
    a=ap.parse_args(); started=datetime.now(timezone.utc).isoformat()
    legacy=Path(a.legacy_task).resolve(); trig=Path(a.url_trigger).resolve(); cert=Path(a.cert).resolve(); key=Path(a.private_key).resolve(); receipt=Path(a.receipt).resolve()
    base={'schema_version':'vpd-figma-upload-receipt/v1','transport_version':'historical-asset-fresh-url-v1','started_at':started,'legacy_task_sha256':sha256_file(legacy),'trigger_file':trig.name}
    try:
        with tempfile.TemporaryDirectory(prefix='vpd-figma-historical-') as td_s:
            td=Path(td_s); archive=td/'legacy.tar.gz'; trigger_json=td/'trigger.json'
            decrypt(legacy,archive,cert,key); decrypt(trig,trigger_json,cert,key)
            with tarfile.open(archive,'r:gz') as tf: safe_extract(tf,td)
            m=json.loads((td/'manifest.json').read_text(encoding='utf-8'))
            asset=td/m['asset_name']
            if m.get('schema_version')!='vpd-figma-upload-task/v1': raise RuntimeError('legacy schema mismatch')
            if m.get('node_id')!=a.expected_node_id or not NODE_RE.match(a.expected_node_id): raise RuntimeError('legacy node mismatch')
            if m.get('source_sha256')!=a.expected_source_sha256 or sha256_file(asset)!=a.expected_source_sha256: raise RuntimeError('frozen source sha mismatch')
            if asset.stat().st_size!=int(m.get('source_size',-1)): raise RuntimeError('frozen source size mismatch')
            if m.get('content_type') not in {'image/png','image/jpeg','image/gif','image/webp'}: raise RuntimeError('content type rejected')
            t=json.loads(trigger_json.read_text(encoding='utf-8'))
            if t.get('schema_version')!='vpd-figma-legacy-submit-url-trigger/v1': raise RuntimeError('trigger schema mismatch')
            if t.get('node_id')!=a.expected_node_id or t.get('source_sha256')!=a.expected_source_sha256: raise RuntimeError('trigger identity mismatch')
            p=urlparse(str(t.get('submit_url','')))
            if p.scheme!='https' or p.hostname!='mcp.figma.com' or not p.path.startswith('/mcp/upload/') or not p.path.endswith('/submit'): raise RuntimeError('submit URL rejected')
            response_file=td/'figma-response.json'
            cp=subprocess.run(['curl','--fail-with-body','--silent','--show-error','--connect-timeout','15','--max-time','90','--request','POST','--header',f"Content-Type: {m['content_type']}",'--header','Accept: application/json','--data-binary',f'@{asset}','--output',str(response_file),'--write-out','%{http_code}',t['submit_url']],text=True,capture_output=True)
            http=cp.stdout.strip()[-3:] if cp.stdout.strip() else None
            raw=response_file.read_text(encoding='utf-8',errors='replace') if response_file.exists() else ''
            parsed={}
            try:
                data=json.loads(raw) if raw else {}
                if isinstance(data,dict): parsed={k:data[k] for k in SAFE_RESPONSE_KEYS if k in data}
            except Exception: parsed={'message':'non-JSON response omitted'}
            meta={'task_id':t['task_id'],'node_id':a.expected_node_id,'source_filename':m['source_filename'],'source_sha256':a.expected_source_sha256,'source_size':m['source_size'],'content_type':m['content_type']}
            if cp.returncode!=0:
                write_receipt(receipt,{**base,**meta,'status':'UPLOAD_FAILED','http_status':http,'error':'curl upload failed; URL omitted','response':parsed,'finished_at':datetime.now(timezone.utc).isoformat()}); return 2
            if parsed.get('targetNodeId') not in {None,a.expected_node_id}: raise RuntimeError('response targetNodeId mismatch')
            write_receipt(receipt,{**base,**meta,'status':'UPLOAD_PASS','http_status':http,'response':parsed,'finished_at':datetime.now(timezone.utc).isoformat()})
            print(json.dumps({'status':'UPLOAD_PASS','task_id':t['task_id'],'node_id':a.expected_node_id,'http_status':http})); return 0
    except Exception as e:
        write_receipt(receipt,{**base,'status':'RELAY_FAILED','error':type(e).__name__+': '+str(e)[:400],'finished_at':datetime.now(timezone.utc).isoformat()}); print(json.dumps({'status':'RELAY_FAILED'})); return 3
if __name__=='__main__': raise SystemExit(main())
