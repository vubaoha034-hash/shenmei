#!/usr/bin/env python3
"""R5 source-authentic endpoint/turn primitive atlas (research only).

Training-only Ma Shan Zheng OFL glyph pixels + HanziWriter pedagogic medians.
Stroke-role assignment is a geometric HYPOTHESIS, not verified human brush data.
No holdout glyph from the source font is rendered during atlas extraction.
"""
import hashlib, io, json, math, pathlib, urllib.parse, urllib.request, collections
import numpy as np
from PIL import Image,ImageFont,ImageDraw
from scipy import ndimage
from scipy.optimize import linear_sum_assignment
from skimage.morphology import skeletonize
from fontTools.ttLib import TTFont

ROOT=pathlib.Path("research/typography_r5")
PROTO=json.loads((ROOT/"R5_FROZEN_PROTOCOL.json").read_text(encoding="utf-8"))
OUT=ROOT/"R5_TRAINING_ONLY_ROLE_ATLAS.json"
FONT_URL="https://raw.githubusercontent.com/google/fonts/main/ofl/mashanzheng/MaShanZheng-Regular.ttf"
FONT_SHA="11bbfb9867d70612158229d037e7a5f622bd0e38"
HANZI_COMMIT="68d10a4b21150cae5e1ebbd223eed289cf32d90c"
SIZE=512; PAD=32
def download(url,cap=12_000_000):
    req=urllib.request.Request(url,headers={"User-Agent":"shenmei-R5-research/1.0 (github.com/vubaoha034-hash/shenmei)"})
    with urllib.request.urlopen(req,timeout=22) as response:
        raw=response.read(cap+1)
    if len(raw)>cap:raise ValueError("DOWNLOAD_CAP_EXCEEDED")
    return raw
def blobsha(data):return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
def role_of_stroke(stroke):
    pts=np.array(stroke,float);pts[:,1]*=-1
    steps=np.diff(pts,axis=0); lens=np.linalg.norm(steps,axis=1)
    length=lens.sum(); d=pts[-1]-pts[0];dx,dy=d
    if length<95 or (length<135 and np.linalg.norm(d)<80):return "点"
    turns=[]
    for u,v in zip(steps[:-1],steps[1:]):
      c=float(np.dot(u,v)/max(1e-4,np.linalg.norm(u)*np.linalg.norm(v)))
      turns.append(math.degrees(math.acos(np.clip(c,-1,1))))
    if len(turns)>1 and max(turns[-2:])>52 and length>130:return "钩"
    if turns and max(turns)>57:return "折"
    if abs(dx)>abs(dy)*1.6:return "横"
    if abs(dy)>abs(dx)*1.8:return "竖"
    if dx<0 and dy>=0:return "撇"
    if dx>=0 and dy>=0:return "捺"
    if dx<0 and dy<0:return "撇"
    return "捺"
def render_font_glyph(font,char):
    tmp=Image.new("L",(1200,1200),255)
    ImageDraw.Draw(tmp).text((180,100),char,font=font,fill=0)
    ink=np.array(tmp)<180
    if not np.any(ink):raise ValueError("NO_INK")
    yy,xx=np.nonzero(ink);crop=tmp.crop((int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)))
    r=min((SIZE-2*PAD)/crop.width,(SIZE-2*PAD)/crop.height)
    scaled=crop.resize((max(1,int(crop.width*r)),max(1,int(crop.height*r))),Image.Resampling.LANCZOS)
    out=Image.new("L",(SIZE,SIZE),255)
    out.paste(scaled,((SIZE-scaled.width)//2,(SIZE-scaled.height)//2))
    return np.asarray(out)<180
def median_norm(medians):
    pts=np.array([p for s in medians for p in s],dtype=float)
    x0,y0=pts.min(axis=0);x1,y1=pts.max(axis=0)
    w=x1-x0;h=y1-y0
    if w<50 or h<50:raise ValueError("UNUSABLE_MEDIANS")
    # Match the true style glyph's own visible bbox (font paths are not identical).
    ratio=min((SIZE-2*PAD)/w,(SIZE-2*PAD)/h)
    tx=(SIZE-w*ratio)/2;ty=(SIZE-h*ratio)/2
    def mappt(pt):return np.array([tx+(pt[0]-x0)*ratio,ty+(y1-pt[1])*ratio])
    return mappt
def neighbors(p,skel):
    y,x=p;Y,X=skel.shape;out=[]
    for dy in [-1,0,1]:
      for dx in [-1,0,1]:
       if not dx and not dy:continue
       yy,xx=y+dy,x+dx
       if 0<=yy<Y and 0<=xx<X and skel[yy,xx]:out.append((yy,xx))
    return out
def trace_endpoint(ep,skel,maxlength=31):
    route=[ep];prev=None
    while len(route)<maxlength:
       ns=[x for x in neighbors(route[-1],skel) if x!=prev]
       if len(ns)!=1:break
       prev=route[-1];route.append(ns[0])
    return route
def terminal_geom(ep,route,dist):
    if len(route)<11:return None
    width=[float(2*dist[y,x]) for y,x in route[:min(24,len(route))]]
    med=float(np.median(width[min(5,len(width)-2):min(18,len(width))]))
    if med<1.8:return None
    factors=[round(float(width[min(i,len(width)-1)]/med),4) for i in [0,2,4,6,8,10,14,18,22]]
    e=np.array(route[0][::-1],dtype=float);m=np.array(route[6][::-1],dtype=float);n=np.array(route[min(20,len(route)-1)][::-1],dtype=float)
    vx=n-e;vlen=max(np.linalg.norm(vx),1e-6)
    bend=float(np.cross(m-e,vx)/vlen**2)
    return {"terminal_profile":factors,"terminal_base_px":round(med,3),"bend_norm":round(bend,5),
      "endpoint_xy":[int(ep[1]),int(ep[0])],"trace_pixels":len(route)}
def build():
    train=PROTO["frozen_train_characters"];holdouts=PROTO["holdout_unique_codepoints"]
    if set(train)&set(holdouts):raise ValueError("LEAKAGE_TRAIN_TARGET")
    raw=download(FONT_URL)
    if len(raw)!=PROTO["source_font"]["bytes"] or blobsha(raw)!=FONT_SHA:raise ValueError("FONT_SOURCE_HASH_FAIL")
    fnt=TTFont(io.BytesIO(raw),lazy=True)
    cmap=fnt.getBestCmap()
    if not all(ord(ch) in cmap for ch in train+holdouts):raise ValueError("MISSING_CJK_CHARACTER")
    font=ImageFont.truetype(io.BytesIO(raw),720)
    degrees=np.ones((3,3),dtype=np.int8);degrees[1,1]=0
    atlas=[];failures=[];raw_hashes={};counts=collections.Counter()
    for ch in train:
      try:
       url=f"https://raw.githubusercontent.com/chanind/hanzi-writer-data/{HANZI_COMMIT}/data/{urllib.parse.quote(ch)}.json"
       content=download(url,80_000);raw_hashes[ch]=hashlib.sha256(content).hexdigest()
       obj=json.loads(content)
       med=obj["medians"]
       if len(med)!=len(obj["strokes"]):raise ValueError("MEDIAN_STROKE_COUNT_MISMATCH")
       mask=render_font_glyph(font,ch)
       skel=skeletonize(mask)
       deg=ndimage.convolve(skel.astype(np.int16),degrees,mode="constant")
       endpoints=np.argwhere(skel&(deg==1))
       if not len(endpoints):raise ValueError("NO_TERMINI")
       # Work only with endpoint paths long enough to avoid isolated extraction noise.
       traced={};valid_ep=[]
       dist=ndimage.distance_transform_edt(mask)
       for ep in endpoints:
          ep=tuple(map(int,ep))
          route=trace_endpoint(ep,skel)
          geom=terminal_geom(ep,route,dist)
          if geom is not None:
             valid_ep.append(ep);traced[ep]=geom
       mapper=median_norm(med)
       markers=[]
       for k,stroke in enumerate(med):
          role=role_of_stroke(stroke)
          arr=np.asarray(stroke,float);mx,my=mapper(arr.mean(axis=0))
          pos=("左" if mx<SIZE*.35 else "右" if mx>SIZE*.65 else "中")
          for endpoint_index,p in enumerate([stroke[0],stroke[-1]]):
             point=mapper(p);markers.append({"role":role,"stroke_id":k,"kind":"起点" if endpoint_index==0 else "终点",
                 "at_xy":point,"component_position":pos})
       if not len(valid_ep):raise ValueError("NO_VALID_STROKE_ENDS")
       ep_xy=np.asarray([[e[1],e[0]] for e in valid_ep],dtype=float)
       mxy=np.asarray([m["at_xy"] for m in markers],dtype=float)
       cost=np.linalg.norm(mxy[:,None,:]-ep_xy[None,:,:],axis=-1)
       mm,ee=linear_sum_assignment(cost)
       matched=0
       for i,j in zip(mm,ee):
          d=float(cost[i,j])
          # Conservative: endpoint association is ambiguous in visually different fonts.
          row=np.sort(cost[i]);gap=float(row[1]-row[0]) if len(row)>1 else 0.
          if d>56 or gap<5.5:continue
          label=markers[i];match=traced[valid_ep[j]]
          item={"source_glyph":ch,"median_stroke_number":label["stroke_id"],"role":label["role"],
              "kind":label["kind"],"component_position":label["component_position"],
              "distance_to_pedagogic_endpoint_px":round(d,3),
              "runner_up_distance_gap_px":round(gap,3),"confidence_level":"GEOMETRIC_MATCH_ONLY",
              **match}
          atlas.append(item);counts[(item["role"],item["kind"])]+=1
          matched+=1
       if matched==0:failures.append({"char":ch,"error":"ZERO_CONFIDENT_ENDPOINT_ASSOCIATIONS"})
      except Exception as exc:failures.append({"char":ch,"error":str(exc)[:200]})
    bins={}
    for role in ["横","竖","撇","捺","点","折","钩"]:
      for kind in ["起点","终点"]:
        cur=[a for a in atlas if a["role"]==role and a["kind"]==kind]
        if not cur:continue
        vals=np.array([x["terminal_profile"] for x in cur],dtype=float)
        low=np.percentile(vals,25,axis=0);mid=np.median(vals,axis=0);high=np.percentile(vals,75,axis=0)
        widths=[x["terminal_base_px"] for x in cur]
        bends=[x["bend_norm"] for x in cur]
        bins[f"{role}:{kind}"]={"n":len(cur),"unique_train_characters":len(set(x["source_glyph"] for x in cur)),
          "median_normalized_profile":[round(float(v),4) for v in mid],
          "q25_profile":[round(float(v),4) for v in low],
          "q75_profile":[round(float(v),4) for v in high],
          "median_brush_width_px":round(float(np.median(widths)),3),
          "median_bend_norm":round(float(np.median(bends)),5),
          "role_sample_sufficient":len(cur)>=6 and len(set(x["source_glyph"] for x in cur))>=4}
    summary={"schema":"r5-mashanzheng-role-primitive-atlas/1.0","date":"2026-10-26",
      "source_font":"Ma Shan Zheng (SIL OFL 1.1)",
      "font_sha256":hashlib.sha256(raw).hexdigest(),"font_verified_git_blob_sha1":blobsha(raw),
      "hanziwriter_commit":HANZI_COMMIT,"source_chars_requested":len(train),
      "source_chars_processed":len(train)-len(set(x["char"] for x in failures)),
      "holdouts_unseen":holdouts,"holdout_source_font_glyphs_rendered":False,
      "training_hanzi_data_sha256":raw_hashes,"source_glyph_failures":failures,
      "confident_terminal_samples":len(atlas),"role_bins":bins,
      "samples":atlas,
      "role_family_coverage":[k for k,v in bins.items() if v["role_sample_sufficient"]],
      "role_atlas_gate_pass":len(atlas)>=35 and len([x for x in bins.values() if x["role_sample_sufficient"]])>=4,
      "aesthetic_success_proven":False,
      "notes":["Morphological endpoint from a modern licensed font, matched approximately to Hanzi Writer pedagogic stroke start/end; not recovered designer brush session.",
               "Sample association is geometrical, not original pen pressure, real stroke type, or hand annotated feature ground truth.",
               "If match reliability and class coverage are inadequate, candidate generation is not promoted or falsely attributed.",
               "R2 global widths, arbitrary vector twisting, and randomized grain are excluded."]}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("R5_ATLAS_SUMMARY "+json.dumps({"source_count":summary["source_chars_processed"],"glyphs_requested":len(train),
      "failures":len(failures),"matched_samples":len(atlas),"sufficient_roles":summary["role_family_coverage"],
      "gate":summary["role_atlas_gate_pass"],"bins":{k:v["n"] for k,v in bins.items()}},ensure_ascii=False))
if __name__=="__main__":build()
