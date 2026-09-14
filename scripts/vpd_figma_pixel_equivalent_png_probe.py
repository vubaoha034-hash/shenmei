#!/usr/bin/env python3
"""Diagnostic only: transcode frozen Doufang B decoded RGB pixels losslessly to PNG.

Original JPEG SHA remains the source identity. The PNG exists only on the runner and is
used solely on an isolated scratch target to distinguish visual-pixel behavior from the
original JPEG byte/content-hash path. It is not an authorized formal P6 asset.
"""
from __future__ import annotations
import argparse,hashlib,json,os,subprocess,tarfile,tempfile
from datetime import datetime,timezone
from pathlib import Path
from urllib.parse import urlparse
from PIL import Image
SAFE={'imageHash','targetNodeId','nodeId','status','message','placement'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def safe_extract(tf,dest):
 b=dest.resolve()
 for m in tf.getmembers():
  t=(dest/m.name).resolve()
  if os.path.commonpath([str(b),str(t)])!=str(b):raise RuntimeError('unsafe archive')
 tf.extractall(dest)
def dec(src,dst,cert,key):subprocess.run(['openssl','cms','-decrypt','-binary','-inform','DER','-in',str(src),'-recip',str(cert),'-inkey',str(key),'-out',str(dst)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
def wr(p,o):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--legacy-task',required=True);ap.add_argument('--trigger',required=True);ap.add_argument('--cert',required=True);ap.add_argument('--private-key',required=True);ap.add_argument('--receipt',required=True);ap.add_argument('--source-node-id',required=True);ap.add_argument('--target-node-id',required=True);ap.add_argument('--expected-source-sha256',required=True);a=ap.parse_args();started=datetime.now(timezone.utc).isoformat();receipt=Path(a.receipt)
 base={'schema_version':'vpd-figma-upload-receipt/v1','transport_version':'pixel-equivalent-png-diagnostic-v1','started_at':started,'original_source_sha256':a.expected_source_sha256,'source_node_id':a.source_node_id,'node_id':a.target_node_id}
 try:
  with tempfile.TemporaryDirectory(prefix='vpd-pixel-png-') as td_s:
   td=Path(td_s);arc=td/'legacy.tar.gz';tj=td/'trigger.json';dec(Path(a.legacy_task),arc,Path(a.cert),Path(a.private_key));dec(Path(a.trigger),tj,Path(a.cert),Path(a.private_key))
   with tarfile.open(arc,'r:gz') as tf:safe_extract(tf,td)
   m=json.loads((td/'manifest.json').read_text());src=td/m['asset_name']
   if m.get('node_id')!=a.source_node_id or m.get('source_sha256')!=a.expected_source_sha256 or sha(src)!=a.expected_source_sha256:raise RuntimeError('frozen source identity mismatch')
   im=Image.open(src).convert('RGB');pixels=im.tobytes();pixel_sha=hashlib.sha256(pixels).hexdigest();png=td/'pixel-equivalent.png';im.save(png,format='PNG',optimize=False)
   chk=Image.open(png).convert('RGB');pixel_sha2=hashlib.sha256(chk.tobytes()).hexdigest()
   if chk.size!=im.size or pixel_sha2!=pixel_sha:raise RuntimeError('pixel equivalence failed')
   t=json.loads(tj.read_text());
   if t.get('schema_version')!='vpd-figma-legacy-submit-url-trigger/v1' or t.get('node_id')!=a.target_node_id or t.get('source_sha256')!=a.expected_source_sha256:raise RuntimeError('trigger identity mismatch')
   u=urlparse(str(t.get('submit_url','')))
   if u.scheme!='https' or u.hostname!='mcp.figma.com' or not u.path.startswith('/mcp/upload/') or not u.path.endswith('/submit'):raise RuntimeError('url rejected')
   rf=td/'response.json';cp=subprocess.run(['curl','--fail-with-body','--silent','--show-error','--connect-timeout','15','--max-time','90','--request','POST','--header','Content-Type: image/png','--header','Accept: application/json','--data-binary',f'@{png}','--output',str(rf),'--write-out','%{http_code}',t['submit_url']],text=True,capture_output=True)
   raw=rf.read_text(errors='replace') if rf.exists() else '';parsed={}
   try:
    d=json.loads(raw) if raw else {};parsed={k:d[k] for k in SAFE if isinstance(d,dict) and k in d}
   except Exception:parsed={'message':'non-JSON response omitted'}
   meta={'task_id':t['task_id'],'original_source_filename':m['source_filename'],'original_source_size':m['source_size'],'original_content_type':m['content_type'],'derived_content_type':'image/png','derived_png_sha256':sha(png),'derived_png_size':png.stat().st_size,'dimensions':[im.width,im.height],'mode':'RGB','decoded_pixel_sha256':pixel_sha,'pixel_equivalence_verified':True}
   status='UPLOAD_PASS' if cp.returncode==0 else 'UPLOAD_FAILED';body={**base,**meta,'status':status,'http_status':cp.stdout.strip()[-3:] if cp.stdout.strip() else None,'response':parsed,'finished_at':datetime.now(timezone.utc).isoformat()};wr(receipt,body);print(json.dumps({'status':status,'node_id':a.target_node_id,'pixel_equivalence':True}));return 0 if cp.returncode==0 else 2
 except Exception as e:
  wr(receipt,{**base,'status':'RELAY_FAILED','error':type(e).__name__+': '+str(e)[:400],'finished_at':datetime.now(timezone.utc).isoformat()});return 3
if __name__=='__main__':raise SystemExit(main())
