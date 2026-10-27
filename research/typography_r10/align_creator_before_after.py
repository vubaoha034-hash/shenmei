#!/usr/bin/env python3
"""R10c: contrast author-drawn contour change vs simple screenshot registration.
Hold out bottom 50% raster rows from shift optimization. No source pixels retained.
"""
import datetime,hashlib,io,json,pathlib,urllib.request
import numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt

ROOT=pathlib.Path(__file__).resolve().parent
FROZEN=json.loads((ROOT/"R10_ALIGN_BEFORE_AFTER_FREEZE.json").read_text())
SOURCE=FROZEN["source"]
req=urllib.request.Request(SOURCE,headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/121.0.0.0 Safari/537.36"})
with urllib.request.urlopen(req,timeout=28) as f:
    raw=f.read(11_000_000)
if hashlib.sha256(raw).hexdigest()!=FROZEN["source_sha256"]:raise ValueError("SOURCE_SHA_MISMATCH")
im=Image.open(io.BytesIO(raw)).convert("RGB")
if list(im.size)!=FROZEN["dimensions"]:raise ValueError("SOURCE_SIZE_MISMATCH")
w,h=im.size
crop=np.asarray(im.crop((0,0,round(w*.58),round(h*.93))),dtype=np.uint8)
r=crop[:,:,0].astype(np.float32);g=crop[:,:,1].astype(np.float32);b=crop[:,:,2].astype(np.float32)
red=(r>=110)&((r-g)>=38)&((r-b)>=24)&(r>g*1.35)
blue=(b>=110)&((b-r)>=43)&((b-g)>=14)&(b>r*1.35)
before=np.argwhere(red);after=np.argwhere(blue)
if min(len(before),len(after))<300:raise ValueError("SOURCE_COLOR_OUTLINES_NOT_FOUND")
split=crop.shape[0]//2
train=after[after[:,0]<split]
held=after[after[:,0]>=split]
if min(len(train),len(held))<100:raise ValueError("HOLDOUT_COLOR_SOURCE_TOO_SPARSE")
dist=distance_transform_edt(~red)
H,W=dist.shape
def sample(pts,maxlen=3000):
    if len(pts)<=maxlen:return pts
    return pts[np.linspace(0,len(pts)-1,maxlen,dtype=np.int64)]
train=sample(train);held=sample(held)
def evaldist(pts,dx,dy):
    ys=pts[:,0]+dy;xs=pts[:,1]+dx
    ok=(ys>=0)&(ys<H)&(xs>=0)&(xs<W)
    good=dist[ys[ok],xs[ok]]
    if good.size<.98*len(pts):raise ValueError("SHIFTED_MASK_OUTSIDE_ROI")
    return good
def metrics(pts,dx,dy):
    vals=evaldist(pts,dx,dy)
    return {"sampled":len(vals),
      "q25":round(float(np.percentile(vals,25)),3),
      "median":round(float(np.median(vals)),3),
      "q90":round(float(np.percentile(vals,90)),3),
      "fraction_within_4px":round(float(np.mean(vals<=4)),5),
      "fraction_more_than_10px":round(float(np.mean(vals>10)),5)}
results=[]
for dx in range(-50,51,2):
    for dy in range(-20,21,2):
        try:vals=evaldist(train,dx,dy)
        except ValueError:continue
        v=(round(float(np.median(vals)),5),abs(dx)+abs(dy),dx,dy)
        results.append(v)
if not results:raise ValueError("NO_CANDIDATE_REGISTRATION")
opt=min(results)
dx,dy=opt[2],opt[3]
zero_train=metrics(train,0,0);fit_train=metrics(train,dx,dy)
zero_test=metrics(held,0,0);fit_test=metrics(held,dx,dy)
s={
 "schema":"vpd-r10c-registered-author-before-after-overlay/1.0",
 "date":datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "creator":"Typotheque / Zheng Chuyang",
 "source_url":SOURCE,"source_sha256":FROZEN["source_sha256"],"image_dimensions":[w,h],
 "roi":[0,0,W,H],"training_rows":"top 50%","untuned_heldout_rows":"bottom 50%",
 "before_red_pixel_count":len(before),"after_blue_pixel_count":len(after),
 "training_after_sampled":len(train),"holdout_after_sampled":len(held),
 "registration_strategy":"search integer translation of after blue to before red, minimize median nearest red outline distance on top image portion only",
 "train_optimized_shift_after_to_before_px":{"dx":dx,"dy":dy},
 "training_before_shift":zero_train,"training_after_fit":fit_train,
 "heldout_before_shift":zero_test,"heldout_after_fit":fit_test,
 "heldout_median_distance_change_px":round(zero_test["median"]-fit_test["median"],3),
 "heldout_median_distance_reduction_fraction":round((zero_test["median"]-fit_test["median"])/max(zero_test["median"],1e-8),5),
 "creator_change_inference":"After subtracting a global translation estimated without using bottom-half samples, residual colored-edge mismatch is measured but cannot uniquely determine edited contour curves, design reason or preference.",
 "no_new_italic_glyphs":True,"no_human_blind":True,"source_pixels_published":False,
 "rights":"Only aggregate color/registration metrics are committed; copyrighted source image remains remote/transient",
 "limitations":["Color masks do not capture neutral/black portions and are anti-aliasing dependent.","An uneven output may reflect art-layout registration, RGB markers, or genuine glyph revisions.","This is a falsification/control audit, NOT an aesthetic score or successful typography transfer."],
 "gate_pass":True
}
path=ROOT/"R10_REGISTERED_CONTOUR_HOLDOUT_METRICS.json"
path.write_text(json.dumps(s,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("R10_REGISTERED_HOLDOUT "+json.dumps({
 "shift":[dx,dy],"red":len(before),"blue":len(after),
 "before_median":zero_test["median"],"after_median":fit_test["median"],
 "reduction":s["heldout_median_distance_reduction_fraction"]},ensure_ascii=False))
