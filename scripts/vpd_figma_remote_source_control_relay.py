#!/usr/bin/env python3
"""Diagnostic relay for a short-lived Figma source URL -> Figma scratch target.

Both the source URL and Figma submit URL are supplied only inside one CMS-encrypted
trigger. The runner downloads the source, validates either exact-byte identity or a
bound-node control identity, then POSTs it to the scratch submit URL. Neither URL nor
source bytes are committed.
"""
from __future__ import annotations
import argparse,hashlib,json,struct,subprocess,tempfile
from datetime import datetime,timezone
from pathlib import Path
from urllib.parse import urlparse

SAFE={'imageHash','targetNodeId','nodeId','status','message','placement'}

def sha(p:Path)->str:
 h=hashlib.sha256()
 with p.open('rb') as f:
  for c in iter(lambda:f.read(1024*1024),b''):h.update(c)
 return h.hexdigest()

def image_meta(p:Path)->dict:
 data=p.read_bytes()
 if data.startswith(b'\x89PNG\r\n\x1a\n') and len(data)>=24:
  w,h=struct.unpack('>II',data[16:24]);return {'source_format':'png','source_width':w,'source_height':h}
 if data.startswith(b'\xff\xd8'):
  i=2
  sof={0xC0,0xC1,0xC2,0xC3,0xC5,0xC6,0xC7,0xC9,0xCA,0xCB,0xCD,0xCE,0xCF}
  while i+3<len(data):
   if data[i]!=0xFF:
    i+=1;continue
   while i<len(data) and data[i]==0xFF:i+=1
   if i>=len(data):break
   marker=data[i];i+=1
   if marker in {0xD8,0xD9}:continue
   if i+2>len(data):break
   seglen=struct.unpack('>H',data[i:i+2])[0]
   if seglen<2 or i+seglen>len(data):break
   if marker in sof and seglen>=7:
    h,w=struct.unpack('>HH',data[i+3:i+7]);return {'source_format':'jpeg','source_width':w,'source_height':h}
   i+=seglen
  return {'source_format':'jpeg','source_width':None,'source_height':None}
 return {'source_format':'unknown','source_width':None,'source_height':None}

def decrypt(src:Path,dst:Path,cert:Path,key:Path)->None:
 subprocess.run(['openssl','cms','-decrypt','-binary','-inform','DER','-in',str(src),'-recip',str(cert),'-inkey',str(key),'-out',str(dst)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)

def write_receipt(p:Path,o:dict)->None:
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')

def main()->int:
 ap=argparse.ArgumentParser();ap.add_argument('--trigger',required=True);ap.add_argument('--cert',required=True);ap.add_argument('--private-key',required=True);ap.add_argument('--receipt',required=True);ap.add_argument('--expected-node-id',required=True);ap.add_argument('--expected-source-sha256',required=True);ap.add_argument('--expected-source-node-id');ap.add_argument('--expected-width',type=int);ap.add_argument('--expected-height',type=int);ap.add_argument('--expected-format');a=ap.parse_args()
 started=datetime.now(timezone.utc).isoformat();receipt=Path(a.receipt);base={'schema_version':'vpd-figma-upload-receipt/v1','transport_version':'remote-source-control-v2','started_at':started,'node_id':a.expected_node_id,'historical_source_sha256':a.expected_source_sha256};diag={}
 try:
  with tempfile.TemporaryDirectory(prefix='vpd-remote-control-') as td_s:
   td=Path(td_s);tj=td/'trigger.json';src=td/'source.bin';resp=td/'response.json'
   decrypt(Path(a.trigger),tj,Path(a.cert),Path(a.private_key));t=json.loads(tj.read_text(encoding='utf-8'))
   if t.get('schema_version')!='vpd-figma-remote-source-control-trigger/v1':raise RuntimeError('trigger schema mismatch')
   if t.get('node_id')!=a.expected_node_id:raise RuntimeError('trigger target identity mismatch')
   mode=t.get('source_identity_mode','exact-byte-sha256-v1')
   if mode=='exact-byte-sha256-v1' and t.get('source_sha256')!=a.expected_source_sha256:raise RuntimeError('trigger source identity mismatch')
   if mode=='figma-bound-node-control-v1':
    if not a.expected_source_node_id or t.get('source_node_id')!=a.expected_source_node_id:raise RuntimeError('trigger source node identity mismatch')
    if t.get('original_source_sha256')!=a.expected_source_sha256:raise RuntimeError('trigger historical source identity mismatch')
   su=urlparse(str(t.get('source_url','')));du=urlparse(str(t.get('submit_url','')))
   if su.scheme!='https' or su.hostname!='www.figma.com' or not su.path.startswith('/api/mcp/asset/'):raise RuntimeError('source URL rejected')
   if du.scheme!='https' or du.hostname!='mcp.figma.com' or not du.path.startswith('/mcp/upload/') or not du.path.endswith('/submit'):raise RuntimeError('submit URL rejected')
   dcp=subprocess.run(['curl','--fail-with-body','--silent','--show-error','--location','--connect-timeout','15','--max-time','90','--output',str(src),t['source_url']],text=True,capture_output=True)
   if dcp.returncode!=0:raise RuntimeError('source download failed')
   actual=sha(src);meta=image_meta(src);diag={'actual_source_sha256':actual,'source_size':src.stat().st_size,**meta,'source_identity_mode':mode}
   if mode=='exact-byte-sha256-v1':
    if actual!=a.expected_source_sha256:raise RuntimeError('source sha mismatch')
   elif mode=='figma-bound-node-control-v1':
    if a.expected_width is not None and meta['source_width']!=a.expected_width:raise RuntimeError('source width mismatch')
    if a.expected_height is not None and meta['source_height']!=a.expected_height:raise RuntimeError('source height mismatch')
    if a.expected_format and meta['source_format']!=a.expected_format:raise RuntimeError('source format mismatch')
   else:raise RuntimeError('unknown source identity mode')
   cp=subprocess.run(['curl','--fail-with-body','--silent','--show-error','--connect-timeout','15','--max-time','90','--request','POST','--header',f"Content-Type: {t['content_type']}",'--header','Accept: application/json','--data-binary',f'@{src}','--output',str(resp),'--write-out','%{http_code}',t['submit_url']],text=True,capture_output=True)
   raw=resp.read_text(encoding='utf-8',errors='replace') if resp.exists() else '';parsed={}
   try:
    d=json.loads(raw) if raw else {};parsed={k:d[k] for k in SAFE if isinstance(d,dict) and k in d}
   except Exception:parsed={'message':'non-JSON response omitted'}
   body={**base,**diag,'task_id':t['task_id'],'source_node_id':t.get('source_node_id'),'content_type':t['content_type'],'http_status':cp.stdout.strip()[-3:] if cp.stdout.strip() else None,'response':parsed,'status':'UPLOAD_PASS' if cp.returncode==0 else 'UPLOAD_FAILED','finished_at':datetime.now(timezone.utc).isoformat()};write_receipt(receipt,body);print(json.dumps({'status':body['status'],'node_id':a.expected_node_id,'http_status':body['http_status']}));return 0 if cp.returncode==0 else 2
 except Exception as e:
  write_receipt(receipt,{**base,**diag,'status':'RELAY_FAILED','error':type(e).__name__+': '+str(e)[:400],'finished_at':datetime.now(timezone.utc).isoformat()});return 3
if __name__=='__main__':raise SystemExit(main())
