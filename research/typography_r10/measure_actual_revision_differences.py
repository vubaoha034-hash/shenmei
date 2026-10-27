#!/usr/bin/env python3
"""R10b: inspect actual RED-before / CYAN-after contour drawing by its author.
Upstream original remains in RAM only. Publish summary edge-distance statistics,
not proprietary pixel images, SVG, crops, or traced paths. NOT an aesthetic score.
"""
import hashlib, io, json, pathlib, urllib.request, datetime
import numpy as np
from PIL import Image
from scipy.spatial import cKDTree

HERE=pathlib.Path(__file__).resolve().parent
PRIOR=json.loads((HERE/"R10_IMAGE_SOURCE_BYTE_AUDIT.json").read_text())
d={r["id"]:r for r in PRIOR["complete_sources"]}
src=d["TPTQ_REVISION_NA"]
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/121.0.0.0 Safari/537.36"
rq=urllib.request.Request(src["image_url"],headers={"User-Agent":UA})
with urllib.request.urlopen(rq,timeout=30) as response:
    content=response.read(11_000_000)
if hashlib.sha256(content).hexdigest()!=src["sha256"]:
    raise RuntimeError("SOURCE_IMAGE_BYTES_CHANGED_STOP")
im=Image.open(io.BytesIO(content)).convert("RGB")
if [im.width,im.height]!=src["dimensions"]:
    raise RuntimeError("SOURCE_DIMENSIONS_CHANGED_STOP")
w,h=im.size
# Enlarged left-side contour overlay. Exclude right-side "before/after"
# isolated demonstration glyphs and their red/blue labels from this analytic ROI.
ROI=[0,0,round(w*.58),round(h*.93)]
crop=np.asarray(im.crop(tuple(ROI)),dtype=np.uint8)
r=crop[:,:,0].astype(float);g=crop[:,:,1].astype(float);bl=crop[:,:,2].astype(float)
# saturated red and saturated cyan/blue, not generic dark contour ink
red=(r>=110)&((r-g)>=38)&((r-bl)>=24)&(r>g*1.35)
blue=(bl>=110)&((bl-r)>=43)&((bl-g)>=14)&(bl>r*1.35)
rpts=np.column_stack(np.nonzero(red))
bpts=np.column_stack(np.nonzero(blue))
if min(len(rpts),len(bpts))<200:
    raise RuntimeError(f"COLOR_STAGE_PIXELS_MISSING red={len(rpts)} blue={len(bpts)}")
# control geometry sampling resolution, does not re-publish the source.
def spatial_sample(coords,nmax=30000):
    if len(coords)<=nmax:return coords
    # sorted pixel-order stride samples; reproducible and no random sample/best-of.
    return coords[np.linspace(0,len(coords)-1,nmax,dtype=np.int64)]
ra=spatial_sample(rpts);ba=spatial_sample(bpts)
r_tree=cKDTree(ra.astype(np.float32));b_tree=cKDTree(ba.astype(np.float32))
b_dist,b_near=r_tree.query(ba.astype(np.float32),k=1)
r_dist,r_near=b_tree.query(ra.astype(np.float32),k=1)
def quart(vals):
    a=np.asarray(vals,float)
    return {str(p):round(float(np.percentile(a,p)),3) for p in [5,25,50,75,95]}
def region(coords):
    return {"count":int(len(coords)),
      "x_quantile_px":quart(coords[:,1]),"y_quantile_px":quart(coords[:,0]),
      "pixel_fraction":round(len(coords)/(crop.shape[0]*crop.shape[1]),7)}
bands=[]
for i in range(4):
    lo,hi=round(i*crop.shape[0]/4),round((i+1)*crop.shape[0]/4)
    a=ba[(ba[:,0]>=lo)&(ba[:,0]<hi)]
    rr=ra[(ra[:,0]>=lo)&(ra[:,0]<hi)]
    if len(a)<25 or len(rr)<25: 
        bands.append({"band":i,"valid":False,"reason":"INSUFFICIENT_STAGE_PIXELS"})
        continue
    localtree=cKDTree(rr.astype(np.float32))
    dd,ii=localtree.query(a.astype(np.float32),k=1)
    # Signed blue/after pixel x minus nearest red/before pixel x: local shift proxy
    dx=a[:,1].astype(float)-rr[ii,1].astype(float)
    bands.append({"band":i,"valid":True,
      "after_pixels_sampled":len(a),"before_pixels_sampled":len(rr),
      "nearest_before_after_distance_px":quart(dd),
      "nearest_horizontal_offset_px":quart(dx)})
report={
 "schema":"vpd-r10-authored-real-outline-color-differential/1.0",
 "observed_date_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "source_page":"https://www.typotheque.com/articles/designing-large-scale-chinese-fonts",
 "source_author":"Zheng Chuyang (Typotheque / Mallikātype)",
 "source_asset_url":src["image_url"],"source_verified_sha256":src["sha256"],
 "source_dimensions":list(im.size),
 "evidence_semantics":"Same enlarged right-hand 阝 component drawing is annotated red before and blue after in the designer's own article; isolated colored contour lines are the only measured pixels.",
 "roi_xyxy":ROI,"roi_policy":"Left 58% X and upper 93% Y of original to exclude reference glyph labels and side captions. Fixed before inspection of output.",
 "color_thresholds":{"red":"r>=110,r-g>=38,r-b>=24,r>1.35*g","blue":"b>=110,b-r>=43,b-g>=14,b>1.35*r"},
 "before_red":region(rpts),"after_blue":region(bpts),
 "symmetric_nearest_contour_distance":{
   "after_to_before_px":quart(b_dist),"before_to_after_px":quart(r_dist),
   "after_more_than_4px_from_before_fraction":round(float((b_dist>4).mean()),5),
   "after_more_than_10px_from_before_fraction":round(float((b_dist>10).mean()),5)},
 "four_vertical_bands":bands,
 "sample_count":{"before_used":len(ra),"after_used":len(ba)},
 "is_new_design_output":False,
 "not_aesthetic_score":True,
 "not_independent_human_test":True,
 "rights":"Image bytes transient only. Public repo stores aggregate distances/metadata, not source pixels, glyph outlines or crops.",
 "scope_limits":[
  "Red and blue channel segmentation from a creator-published composite is imperfect due to anti-alias and color mixing.",
  "Nearest red-blue colored pixel distance cannot uniquely infer author intent, B-spline move, glyph pressure, or exact stroke editing sequence.",
  "Counts and sample alignment show that two visible annotated contour stages DIFFER, not whether the change improved aesthetic quality.",
  "No transfer to unseen characters occurred in this specific evidence measurement."],
 "gate_pass":True
}
out=HERE/"R10_TRUE_BEFORE_AFTER_PIXEL_DIFFERENCE.json"
out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
print("R10_REVISIONS_PIXEL_PROOF "+json.dumps({
  "source":src["sha256"],"roi":ROI,
  "before":len(rpts),"after":len(bpts),"q50_px":report["symmetric_nearest_contour_distance"]["after_to_before_px"]["50"],
  "frac_gt4":report["symmetric_nearest_contour_distance"]["after_more_than_4px_from_before_fraction"],
  "band_count":sum(x["valid"] for x in bands)},ensure_ascii=False))
