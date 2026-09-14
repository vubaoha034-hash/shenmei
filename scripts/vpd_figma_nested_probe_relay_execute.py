#!/usr/bin/env python3
import argparse,base64,hashlib,json,subprocess,tempfile
from datetime import datetime,timezone
from pathlib import Path
from urllib.parse import urlparse
PROBE_B64='iVBORw0KGgoAAAANSUhEUgAAAGAAAABgCAIAAABt+uBvAAAA1ElEQVR4nO3QwQ3AIBDAsNLJb3QmQHnCw54gypqZj7P/dsDrDAoGBYOCQcGgYFAwKBgUDAoGBYOCQcGgYFAwKBgUDAoGBYOCQcGgYFAwKBgUDAoGBYOCQcGgYFAwKBgUDAoGBYOCQcGgYFAwKBgUDAoGBYOCQcGgYFAwKBgUDAoGBYOCQcGgYFAwKBgUDAoGBYOCQcGgYFAwKBgUDAoGBYOCQcGgYFAwKBgUDAoGBYOCQcGgYFAwKBgUDAoGBYOCQcGgYFAwKBgUDAoGBYOCQcGgYFDYqUUCQI1+pYYAAAAASUVORK5CYII='
PROBE_SHA='6ddd792040c5ba1cd5eee8c7b98b9ebd045cacf70b4522f35e70dce9edf702a4'
SAFE={'imageHash','targetNodeId','nodeId','status','message','placement'}
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--trigger',required=True); ap.add_argument('--cert',required=True); ap.add_argument('--private-key',required=True); ap.add_argument('--receipt',required=True); ap.add_argument('--expected-node-id',required=True); a=ap.parse_args()
 started=datetime.now(timezone.utc).isoformat(); receipt=Path(a.receipt)
 try:
  with tempfile.TemporaryDirectory(prefix='vpd-nested-probe-') as td_s:
   td=Path(td_s); tj=td/'trigger.json'; png=td/'probe.png'; png.write_bytes(base64.b64decode(PROBE_B64))
   if hashlib.sha256(png.read_bytes()).hexdigest()!=PROBE_SHA: raise RuntimeError('probe sha mismatch')
   subprocess.run(['openssl','cms','-decrypt','-binary','-inform','DER','-in',a.trigger,'-recip',a.cert,'-inkey',a.private_key,'-out',str(tj)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
   t=json.loads(tj.read_text());
   if t.get('schema_version')!='vpd-figma-nested-probe-trigger/v1' or t.get('node_id')!=a.expected_node_id or t.get('source_sha256')!=PROBE_SHA: raise RuntimeError('trigger identity mismatch')
   p=urlparse(t.get('submit_url',''))
   if p.scheme!='https' or p.hostname!='mcp.figma.com' or not p.path.startswith('/mcp/upload/') or not p.path.endswith('/submit'): raise RuntimeError('url rejected')
   rf=td/'response.json'; cp=subprocess.run(['curl','--fail-with-body','--silent','--show-error','--connect-timeout','15','--max-time','90','--request','POST','--header','Content-Type: image/png','--header','Accept: application/json','--data-binary',f'@{png}','--output',str(rf),'--write-out','%{http_code}',t['submit_url']],text=True,capture_output=True)
   raw=rf.read_text(errors='replace') if rf.exists() else ''; data={}
   try:
    d=json.loads(raw) if raw else {}; data={k:d[k] for k in SAFE if isinstance(d,dict) and k in d}
   except Exception: data={'message':'non-JSON response omitted'}
   body={'schema_version':'vpd-figma-upload-receipt/v1','transport_version':'nested-probe-v1','task_id':t['task_id'],'node_id':a.expected_node_id,'source_sha256':PROBE_SHA,'source_size':len(png.read_bytes()),'content_type':'image/png','http_status':cp.stdout.strip()[-3:] if cp.stdout.strip() else None,'response':data,'started_at':started,'finished_at':datetime.now(timezone.utc).isoformat(),'status':'UPLOAD_PASS' if cp.returncode==0 else 'UPLOAD_FAILED'}
   receipt.parent.mkdir(parents=True,exist_ok=True); receipt.write_text(json.dumps(body,indent=2,sort_keys=True)+'\n')
   return 0 if cp.returncode==0 else 2
 except Exception as e:
  receipt.parent.mkdir(parents=True,exist_ok=True); receipt.write_text(json.dumps({'schema_version':'vpd-figma-upload-receipt/v1','transport_version':'nested-probe-v1','status':'RELAY_FAILED','error':type(e).__name__+': '+str(e)[:300],'started_at':started,'finished_at':datetime.now(timezone.utc).isoformat()},indent=2)+'\n'); return 3
if __name__=='__main__': raise SystemExit(main())
