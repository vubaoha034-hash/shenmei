#!/usr/bin/env python3
"""R4: exact-text expressive-handwriting controls against 3 SHA-verified Rosanjin works.
Read-only external Google Fonts files are verified by fixed Git blob checksums, used in memory,
and NOT redistributed. No claims of designer motion, creation process or aesthetic victory.
"""
import hashlib, io, json, pathlib, urllib.request
import numpy as np
from PIL import Image,ImageFont,ImageDraw
from fontTools.ttLib import TTFont
from scipy.ndimage import distance_transform_edt, label
from skimage.morphology import skeletonize,convex_hull_image
from skimage.measure import perimeter

DIR=pathlib.Path("research/typography_r3")
SRC=DIR/"ROSANJIN_REMOTE_SOURCE_RECEIPT.json"
OUT=DIR/"R4_EXPRESSIVE_SAME_TEXT_CONTROLS.json"
FONTS=[
 ("Yuji Syuku","yujisyuku/YujiSyuku-Regular.ttf",8430348,"8a7db48fbf431ea97f14bedf6a4f5472347ab8a0"),
 ("Yuji Boku","yujiboku/YujiBoku-Regular.ttf",8525588,"3a8cb821f00c7c03ac2eb90915898749b9bce4df"),
 ("Zhi Mang Xing","zhimangxing/ZhiMangXing-Regular.ttf",4063532,"d037d1f00395175de01de33e62957c30a008a1b1"),
 ("Long Cang","longcang/LongCang-Regular.ttf",5162508,"363bb08696fe4d3827bd36d3d2fbc028d1205161"),
 ("Liu Jian Mao Cao","liujianmaocao/LiuJianMaoCao-Regular.ttf",4951804,"f380deef04a5ee6d5af2c6fba60d1613d831c1aa"),
 ("Ma Shan Zheng","mashanzheng/MaShanZheng-Regular.ttf",5857936,"11bbfb9867d70612158229d037e7a5f622bd0e38"),
 ("Iansui","iansui/Iansui-Regular.ttf",9420560,"1ecd53c7c6badf6c04d9623db769ce59d50f12b7"),
 ("LXGW WenKai TC Bold","lxgwwenkaitc/LXGWWenKaiTC-Bold.ttf",12881104,"4c48b0882af4edb7b161327ca1726ffe6da3b282"),
 ("Klee One SemiBold","kleeone/KleeOne-SemiBold.ttf",8905128,"aa30525e375c811d763675277cb3ae3ed56ddcbc"),
 ("Yuji Mai","yujimai/YujiMai-Regular.ttf",8496292,"5d1d1e6899c3c1483f8ed774551e324d9785ca03")
]
def original_receipt():
 r=json.loads(SRC.read_text(encoding="utf-8"))
 if r.get("verified_sources")!=3 or len(r.get("source_status",[]))!=3:raise ValueError("SOURCE_MISSING_OR_NOT_VERIFIED")
 for a in r["source_status"]:
  if a["status"]!="SOURCE_VERIFIED_STATIC_IMAGE_MEASURED" or a["sha1_verified"]!=a["source_svg_sha1_expected"]:
   raise ValueError("UNVERIFIED_REFERENCE")
 return r["source_status"]
def acquire_font(name,path,n,blobsha):
 url="https://raw.githubusercontent.com/google/fonts/main/ofl/"+path
 req=urllib.request.Request(url,headers={"User-Agent":"shenmei-r4-design-research/0.1","Accept":"application/octet-stream"})
 with urllib.request.urlopen(req,timeout=30) as v:raw=v.read(14_000_000)
 if len(raw)!=n: raise ValueError("FONT_BYTES_MISMATCH")
 git_sha=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
 if git_sha!=blobsha:raise ValueError("FONT_GIT_SHA_MISMATCH")
 tt=TTFont(io.BytesIO(raw),lazy=True)
 cmap=tt.getBestCmap()
 return raw,cmap,hashlib.sha256(raw).hexdigest()
def image_word(text,font):
 cw=font.size
 tmp=Image.new("L",(cw*(len(text)+5),cw*4),255)
 ImageDraw.Draw(tmp).text((cw,cw),text,font=font,fill=0)
 ink=np.asarray(tmp)<180
 if not ink.any():raise ValueError("NO_INK")
 y,x=np.nonzero(ink)
 return tmp.crop((int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)))
def fit(img,w,h,mode):
 if mode=="aspect_preserving":
  s=min(w/img.width,h/img.height)
  tw=max(1,int(img.width*s+0.5));th=max(1,int(img.height*s+0.5))
 else:tw,th=w,h
 o=Image.new("L",(w,h),255);o.paste(img.resize((tw,th),Image.Resampling.LANCZOS),((w-tw)//2,(h-th)//2));return o
def measure(img):
 arr=np.asarray(img)<180
 y,x=np.nonzero(arr)
 if len(y)<30: raise ValueError("INSUFFICIENT_INK")
 roi=arr[int(y.min()):int(y.max()+1),int(x.min()):int(x.max()+1)]
 sk=skeletonize(roi); dist=2*distance_transform_edt(roi);ws=dist[sk];ws=ws[np.isfinite(ws)&(ws>0)]
 if len(ws)<30:raise ValueError("INSUFFICIENT_STROKE_SAMPLES")
 q=np.percentile(ws,[10,50,90]);h,w=roi.shape
 comp,c=label(roi);counts=np.bincount(comp.ravel())[1:]
 per=perimeter(roi,neighborhood=8); hullper=perimeter(convex_hull_image(roi),neighborhood=8)
 # 3x2 spatial field: position of heavy ink on SKELETON, not fictitious stroke ordering.
 top=max(np.percentile(ws,75),3.0)
 counts=[[0.,0.,0.] for _ in range(2)]
 sy,sx=np.nonzero(sk)
 for yy,xx in zip(sy,sx):
  if dist[yy,xx]>=top:
   counts[min(1,2*yy//max(1,h))][min(2,3*xx//max(1,w))]+=1
 total=sum(map(sum,counts)) or 1
 spatial=[[round(z/total,4) for z in row] for row in counts]
 return {
  "ink_ratio":round(float(roi.mean()),5),
  "thick_thin_ratio":round(float(q[2]/q[0]),4),
  "typical_thickness_vs_height":round(float(q[1]/h),5),
  "complexity_perimeter_hull":round(float(per/max(1,hullper)),4),
  "connected_components_ge3px":int(sum(z>=3 for z in counts if False)) if False else int(sum(z>=3 for z in np.bincount(comp.ravel())[1:])),
  "heavy_ink_3x2_position_share":spatial,
  "ink_bbox":[int(w),int(h)],
  "width_q10_50_90":[round(float(z),3) for z in q]
 }
def main():
 sources=original_receipt()
 output={"schema_version":"r4-professional-calligraphic-typeface-counterfactual/1.0",
 "date":"2026-10-26","study":"Three matched-input professionally styled font controls × original same-text 3 logos; preserve form with two alignments.",
 "original_count":3,"font_candidates":len(FONTS),"font_checks":[],"runs":[],
 "limitations":["Source SVG was digitally traced in 2025. Results are static image morphology ONLY.",
 "Measuring 3x2 spatial heavy-ink cells does not segment actual pen strokes or prove designer intention.",
 "Six expressive fonts may fail glyph coverage for traditional characters; excluded fonts never silently substitute.",
 "Aesthetic superiority or new-character method generalization requires actual unseen image production and blinded human review.",
 "No original SVG bytes, reference images or font binaries are saved in this repo."] }
 for name,path,size,sha in FONTS:
  check={"font":name,"upstream_repo":"google/fonts","upstream_path":"ofl/"+path,"expected_git_blob_sha":sha,"expected_bytes":size}
  try:
   raw,cmap,sha256=acquire_font(name,path,size,sha)
   check.update({"status":"FONT_BYTES_HASH_VERIFIED","sha256":sha256})
  except Exception as e:
   check.update({"status":"FETCH_OR_HASH_FAIL","error":str(e)[:240]});output["font_checks"].append(check);continue
  allowed=[s for s in sources if all(ord(ch) in cmap for ch in s["title"])]
  excluded=[{"id":s["id"],"missing":"".join(ch for ch in s["title"] if ord(ch) not in cmap)} for s in sources if s not in allowed]
  check.update({"supported_titles":[s["id"] for s in allowed],"excluded_titles":excluded})
  try:
   font=ImageFont.truetype(io.BytesIO(raw),210)
   for s in allowed:
    actual=image_word(s["title"],font)
    _,_,w,h=s["morphology"]["ink_bbox_px"]
    for mode in ["aspect_preserving","match_ink_bbox"]:
     image=fit(actual,w,h,mode)
     metrics=measure(image)
     pixel_sha=hashlib.sha256(image.tobytes()).hexdigest()
     output["runs"].append({"font":name,"work_id":s["id"],"text":s["title"],"mode":mode,"pixel_sha256":pixel_sha,"metrics":metrics})
   check["status"]="MEASURED" if allowed else "NO_EXACT_TITLE_COVERAGE"
  except Exception as e:check.update({"status":"RENDER_FAILED","error":str(e)[:200]})
  output["font_checks"].append(check)
 output["complete_controls"]=len(output["runs"])
 # Robust only when at least one expressive font covers EACH original in BOTH modes.
 out={}
 for key,src_key in [("thick_thin_ratio","stroke_width_tail_ratio_p90_over_p10"),
                      ("typical_thickness_vs_height","stroke_width_ratio_to_bbox_h_p10_p50_p90"),
                      ("complexity_perimeter_hull","ink_perimeter_over_hull_perimeter")]:
  one=[]
  for source in sources:
   s=source["morphology"][src_key];s=s[1] if isinstance(s,list) else s
   rs=[r for r in output["runs"] if r["work_id"]==source["id"]]
   groups=[]
   for mode in ["aspect_preserving","match_ink_bbox"]:
    cand=[r for r in rs if r["mode"]==mode]
    diff=[{"font":r["font"],"value":r["metrics"][key],"source_minus_control_pct":round(100*(s-r["metrics"][key])/max(1e-8,r["metrics"][key]),2)} for r in cand]
    groups.append({"mode":mode,"control_count":len(diff),"source_higher_than_all_by_15pct":bool(diff) and all(v["source_minus_control_pct"]>=15 for v in diff),"controls":diff})
   one.append({"work":source["id"],"original":s,"modes":groups})
  reliable=all(all(g["source_higher_than_all_by_15pct"] for g in v["modes"]) for v in one)
  out[key]={"robust_expressive_font_separation":reliable,"by_original":one}
 output["metric_assessment"]=out
 output["pixel_geometry_independence"]=[
  {"work_id":source["id"],"mode":mode,"controls":len(group),
   "unique_raster_hashes":len({x["pixel_sha256"] for x in group}),
   "same_raster_note":"If equal, apparently different font files are not independent geometry controls for this exact rendered title.",
   "hashes":[{"font":x["font"],"pixel_sha256":x["pixel_sha256"]} for x in group]}
  for source in sources for mode in ["aspect_preserving","match_ink_bbox"]
  for group in [[v for v in output["runs"] if v["work_id"]==source["id"] and v["mode"]==mode]]
 ]
 output["independent_expressive_family_gate_pass"] = all(x["unique_raster_hashes"]>=2 for x in output["pixel_geometry_independence"])
 output["any_general_creator_method_proven"]=False
 output["stop_condition"]="If generic expressive fonts show similar heavy-light contrast, retire global width quantiles as an author-specific rule; investigate per-glyph stroke roles only with evidence from original pixels and matched semantic positions."
 OUT.write_text(json.dumps(output,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print("R4_EXPRESSIVE_AUDIT "+json.dumps({"fonts":len(FONTS),"measured":output["complete_controls"],"each_font":[{"font":v["font"],"status":v["status"],"supported":v.get("supported_titles",[])} for v in output["font_checks"]],"robust":{k:v["robust_expressive_font_separation"] for k,v in out.items()}},ensure_ascii=False))
if __name__=="__main__":main()
