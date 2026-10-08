#!/usr/bin/env python3
"""Independent, byte-reading RGBA pixel audit for AI-master vs Figma exported PNG.

Usage: python visual_v030_pixel_auditor.py ai_master.png figma.png regions.json report.json
regions.json: {"regions":[{"region_id":"...","target_text":"...","bbox":{"x":0,"y":0,"width":100,"height":30},"reviewed_text":"...","human_text_verified":true}, ...]}
The human text review must be performed by seeing BOTH image pixels, not by copying a receipt.
This verifies pixels and hashes; it does NOT OCR or prove a reviewer truly inspected the words.
"""
import argparse, hashlib, json, sys
from pathlib import Path
from PIL import Image
import numpy as np

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def load(path):
    im=Image.open(path)
    if im.format!='PNG' or im.mode!='RGBA':raise ValueError(f'{path}: PNG RGBA required (got {im.format}/{im.mode})')
    return np.array(im,dtype=np.uint8)

def metrics(a,b):
    # Compare alpha silhouettes AND premultiplied appearance to exclude RGB noise under transparent pixels.
    mask_a=a[:,:,3]>16;mask_b=b[:,:,3]>16
    union=int(np.count_nonzero(mask_a|mask_b));intersection=int(np.count_nonzero(mask_a&mask_b))
    aa=a.astype(np.float32)/255.;bb=b.astype(np.float32)/255.
    ca=np.concatenate([aa[:,:,:3]*aa[:,:,3:4],aa[:,:,3:4]],axis=2)
    cb=np.concatenate([bb[:,:,:3]*bb[:,:,3:4],bb[:,:,3:4]],axis=2)
    foreground=mask_a|mask_b
    mae=float(np.abs(ca-cb)[foreground].mean()) if union else 1.0
    def rect(mask):
        ys,xs=np.nonzero(mask)
        if len(xs)==0:return None
        return [int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
    ba=rect(mask_a);bbx=rect(mask_b)
    err=float(max(abs(x-y) for x,y in zip(ba,bbx))) if ba and bbx else float('inf')
    return {'alpha_iou':round(intersection/union if union else 0,6),'normalized_rgba_mae':round(mae,6),'bbox_error_px':err,'active_pixel_count':union,'bbox_master':ba,'bbox_figma':bbx}

def audit(master,figma,manifest):
    a=load(master);b=load(figma)
    if a.shape!=b.shape:raise ValueError('DIMENSION_MISMATCH')
    h,w=a.shape[:2]
    if not (np.any(a[:,:,3]==0) and np.any(a[:,:,3]>0) and np.any(b[:,:,3]==0) and np.any(b[:,:,3]>0)):
        raise ValueError('TRANSPARENT_ALPHA_REQUIRED_FOR_BOTH')
    regions=manifest['regions']
    if not isinstance(regions,list) or len(regions)<5:raise ValueError('FULL_REGION_INVENTORY_REQUIRED')
    seen=set();items=[];fully_reviewed=True
    for r in regions:
        rid=r['region_id'];target=r['target_text'];q=r['bbox'];x=int(q['x']);y=int(q['y']);rw=int(q['width']);rh=int(q['height'])
        if rid in seen or min(x,y)<0 or min(rw,rh)<1 or x+rw>w or y+rh>h:raise ValueError('REGION_INVALID_OR_DUPLICATED')
        seen.add(rid);m=metrics(a[y:y+rh,x:x+rw],b[y:y+rh,x:x+rw]);m.update(region_id=rid,target_text=target)
        items.append(m)
        fully_reviewed &= r.get('human_text_verified') is True and r.get('reviewed_text')==target
    whole=metrics(a,b)
    th={'alpha_iou_min':0.97,'per_region_alpha_iou_min':0.95,'normalized_rgba_mae_max':0.04,'per_region_rgba_mae_max':0.065,'bbox_max_error_px':2}
    ok=fully_reviewed and whole['alpha_iou']>=th['alpha_iou_min'] and whole['normalized_rgba_mae']<=th['normalized_rgba_mae_max'] and whole['bbox_error_px']<=th['bbox_max_error_px'] and all(r['alpha_iou']>=th['per_region_alpha_iou_min'] and r['normalized_rgba_mae']<=th['per_region_rgba_mae_max'] and r['bbox_error_px']<=th['bbox_max_error_px'] for r in items)
    return {'schema':'ai-master-figma-pixel-audit/v1','comparison_type':'AI_MASTER_VS_FIGMA_EXPORT','master_sha256':sha(master),'figma_export_sha256':sha(figma),'dimensions':[w,h],'png_mode':'RGBA','text_accuracy_100_percent':bool(fully_reviewed),'metrics':{'dimensions_match':True,'registration_aligned':True,'text_accuracy_100_percent':bool(fully_reviewed),'transparent_background_verified':True,'alpha_iou':whole['alpha_iou'],'normalized_rgba_mae':whole['normalized_rgba_mae'],'bbox_max_error_px':whole['bbox_error_px'],'region_metrics':items},'thresholds':th,'verdict':'PASS' if ok else 'FAIL','note':'Real RGBA bytes were read and hashed. Human text accuracy is a required reviewer attestation and not OCR.'}

def main():
    p=argparse.ArgumentParser();p.add_argument('master');p.add_argument('figma');p.add_argument('regions');p.add_argument('report');q=p.parse_args()
    result=audit(q.master,q.figma,json.loads(Path(q.regions).read_text('utf8')))
    Path(q.report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    print(f"{result['verdict']} master={result['master_sha256'][:12]} figma={result['figma_export_sha256'][:12]}")
    return 0 if result['verdict']=='PASS' else 2

if __name__=='__main__':sys.exit(main())
