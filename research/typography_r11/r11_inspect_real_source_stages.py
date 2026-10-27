#!/usr/bin/env python3
"""R11: real developer-provenanced stages, not invented appearance-rule parameters.
Download into memory only; verify R10 SHA; compute aggregate process evidence.
Original copyrighted pictures are never committed, exported, or included in job artifacts.
"""
from __future__ import annotations
import datetime, hashlib, io, json, pathlib, urllib.request, time
import numpy as np
from PIL import Image
from scipy.ndimage import label, find_objects

HERE=pathlib.Path(__file__).resolve().parent
R10=HERE.parent/"typography_r10"/"R10_IMAGE_SOURCE_BYTE_AUDIT.json"
FROZEN=HERE/"R11_FROZEN_CREATOR_STAGE_INTERPRETATION.json"
OUT=HERE/"R11_REAL_STAGE_VISUAL_AUDIT.json"
AGENT="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

def grab(url):
    errors=[]
    for i in range(2):
        try:
            origin=url.split("/")[0]+"//"+url.split("/")[2]+"/"
            req=urllib.request.Request(url,headers={"User-Agent":AGENT,"Referer":origin,"Accept":"image/webp,image/jpeg,image/png,*/*"})
            with urllib.request.urlopen(req,timeout=25) as f: raw=f.read(12_000_001)
            if len(raw)>12_000_000:raise RuntimeError("SIZE_LIMIT")
            im=Image.open(io.BytesIO(raw)); im.load()
            if im.width*im.height>36_000_000:raise RuntimeError("PIXEL_LIMIT")
            if min(im.width,im.height)<350:raise RuntimeError("TOO_SMALL")
            return im,raw
        except Exception as e:
            errors.append(f"{type(e).__name__}:{str(e)[:190]}")
            if not i:time.sleep(1.2)
    raise RuntimeError(" | ".join(errors))

def mask_stats(mask):
    y,x=np.nonzero(mask)
    if not len(x):return {"pixels":0,"bbox":None}
    x0,x1=int(x.min()),int(x.max());y0,y1=int(y.min()),int(y.max())
    return {"pixels":int(len(x)),"bbox":[x0,y0,x1,y1],"centroid":[round(float(x.mean()),2),round(float(y.mean()),2)],
            "percentile_bbox":[round(float(np.percentile(x,2)),2),round(float(np.percentile(y,2)),2),
                               round(float(np.percentile(x,98)),2),round(float(np.percentile(y,98)),2)]}
def top_clusters(mask,limit=8):
    # Exact component pixel area counted, but NOT a unique letter or true pen stroke.
    lab,count=label(mask)
    boxes=find_objects(lab)
    counts=np.bincount(lab.ravel())
    ranked=np.argsort(counts[1:])[::-1][:limit]+1
    rows=[]
    for key in ranked:
        if key-1>=len(boxes) or boxes[key-1] is None:continue
        b=boxes[key-1]
        rows.append({"size":int(counts[key]),"bbox":[b[1].start,b[0].start,b[1].stop-1,b[0].stop-1]})
    return rows

def component_ratio(mask,box):
    if not box:return None
    x0,y0,x1,y1=box
    return round(float(mask[y0:y1+1,x0:x1+1].mean()),6)

def rgb_compare(im,roi):
    a=np.asarray(im.convert("RGB")).astype(np.int16)
    H,W=a.shape[:2];r,g,b=a[:,:,0],a[:,:,1],a[:,:,2]
    red=(r>120)&((r-g)>54)&((r-b)>50)
    blue=(b>135)&((b-r)>50)&((b-g)>12)
    xr=float(roi["right_x_fraction_min"]); rr=roi["red_y_fraction"];br=roi["blue_y_fraction"]
    rx,by=np.meshgrid(np.arange(W),np.arange(H))
    red &= (rx>=round(xr*W)) &(by>=round(rr[0]*H))&(by<=round(rr[1]*H))
    blue &= (rx>=round(xr*W))&(by>=round(br[0]*H))&(by<=round(br[1]*H))
    rs=mask_stats(red); bs=mask_stats(blue)
    rs["major_clusters"]=top_clusters(red,5)
    bs["major_clusters"]=top_clusters(blue,5)
    rs["bbox_occupancy"]=component_ratio(red,rs["bbox"])
    bs["bbox_occupancy"]=component_ratio(blue,bs["bbox"])
    enough=rs["pixels"]>500 and bs["pixels"]>500
    ratio=None
    if enough:
        rb=rs["percentile_bbox"];bb=bs["percentile_bbox"]
        rw=rb[2]-rb[0];bw=bb[2]-bb[0];rh=rb[3]-rb[1];bh=bb[3]-bb[1]
        ratio={"after_to_before_width":round(float(bw/max(1,rw)),4),
               "after_to_before_height":round(float(bh/max(1,rh)),4),
               "after_to_before_color_pixel_count":round(float(bs["pixels"]/max(1,rs["pixels"])),4)}
    return {"color_masks_real_pixels_read":True,"segmentation_logic_frozen_before_run":True,
            "right_panel_source_fraction":xr,"red_before":rs,"blue_after":bs,
            "nonregistered_bbox_ratios":ratio,
            "nonregistered_glyph_pair_pixel_gate":bool(enough),
            "measure_does_not_prove_intended_improvement":True,
            "needs_human_stage_registration":True,
            "limitation":"Cropped areas may include overlaid draft lines and small before/after text; never interpret color masks or bbox ratios as verified matched outline paths without human stage registration."}

def main():
    spec=json.loads(FROZEN.read_text("utf-8"));old=json.loads(R10.read_text("utf-8"))
    frozen={x["id"]:x for x in spec["stage_classification"]}
    oldsources={x["id"]:x for x in old["complete_sources"]}
    sources=[];failed=[];segment=None
    for key,ident in frozen.items():
        rec={"id":key,"stage_kind":ident["stage_kind"],"visual_decision_hypothesis":ident.get("decision_hypothesis"),
             "safe_for_before_after_learning":ident["stage_kind"] not in ["SIDE_BY_SIDE_VARIANT_NOT_CHRONOLOGICAL"]}
        parent=oldsources.get(key)
        url=ident.get("image_url") or (parent or {}).get("image_url")
        if not url:
            rec["verified"]=False;rec["error"]="NO_FROZEN_IMAGE_URL";failed.append(rec);continue
        rec["source_page"]=ident.get("page") or (parent or {}).get("source_page")
        rec["image_url"]=url
        try:
            im,raw=grab(url);h=hashlib.sha256(raw).hexdigest()
            if parent and h!=parent["sha256"]:raise ValueError("R10_EXACT_SOURCE_HASH_MISMATCH_"+h)
            rec.update({"verified":True,"sha256":h,"bytes":len(raw),"dimensions":[im.width,im.height],
                        "frozen_source_bytes_match_R10":bool(parent),
                        "creator_original_asset_republished":False})
            if key=="TPTQ_REVISION_NA":
                segment=rgb_compare(im,ident["roi_heuristic"])
                rec["color_before_after_test"]=segment
            sources.append(rec)
            print("R11_SOURCE_VERIFIED",key,im.size,h)
        except Exception as e:
            rec.update({"verified":False,"error":str(e)[:700]});failed.append(rec)
            print("R11_SOURCE_FAIL",key,rec["error"])
    did_typo=any(x["id"]=="TPTQ_REVISION_NA" for x in sources)
    did_hy=any(x["id"]=="HY_RED_CLOUD" for x in sources)
    paired=bool(did_typo and segment is not None and segment["nonregistered_glyph_pair_pixel_gate"])
    result={
       "schema":"r11-author-actual-before-after-pixel-structure/1.0",
       "utc_verified_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),
       "frozen_before_running":"R11_FROZEN_CREATOR_STAGE_INTERPRETATION.json",
       "r10_source_sha_backchecked":True,
       "records":sources,"failures":failed,
       "verified_count":len(sources),"actual_typotheque_color_stage_present":paired,
       "has_authored_historical_to_draft_to_final":did_hy,
       "reclassified_variant_as_NOT_chronological":True,
       "unsupported_inferences":[
          "Artist's pen pressure, tool settings, vector edits, time ordered version history are NOT captured",
          "Changing a metric is not a professional artistic quality win",
          "Color-coded outlines in one panel cannot be blindly image-IoU compared without stage registration",
          "Arphic standard vs C80 shows variants, not proven chronological sketch→final",
          "No post-hoc ratios copied to generate unseen text"
       ],
       "approved_for_source_study":paired and did_hy,
       "independent_user_blind_review":False,"new_glyph_transfer":False,"learning_method_success":False,
       "potential_creative_decisions":[
         {"case":"TPTQ_AUTHOR_STATEMENT","trigger":"Same radical geometry repeated across many different characters becomes stylistically inconsistent",
          "action":"Audit group and make contextual changes, undo globally over-wide radical proportions if the family loses rhythm",
          "failure_condition":"A globally imposed width ratio damages contextual glyph balance",
          "status":"DESIGNER_STATED_PROCESS_NOT_NEW_GENERATED_ART"},
         {"case":"HANYI_STAGES","trigger":"Creating original modern display lettering from traditional source",
          "action":"Use a designer-controlled hand-painted draft to explore whole-stroke mass/gesture before locking the final digital contours",
          "failure_condition":"Direct trace lacks new legible structure or coherent design family",
          "status":"PUBLISHED_STAGE_INFERENCE_NOT_CREATOR_PEN_TIMELINE"},
         {"case":"ARPHIC_COUNTERS","trigger":"Condensing display glyphs creates tight internal negative spaces",
          "action":"Review and locally redraw the enclosed counter; do not uniformly scale type contours",
          "failure_condition":"Counter closes or damages readability",
          "status":"CREATOR_PUBLISHED_BEFORE_AFTER_ILLUSTRATION"},
         {"case":"MORISAWA_HUMAN_FEEDBACK","trigger":"Real readers observe a stroke ending suggesting unnatural stop rather than continued motion",
          "action":"Correct the gesture in that family of glyphs and verify across related radicals",
          "failure_condition":"Unproven extrapolation from one usage group to all display type",
          "status":"DIRECT_INTERVIEW_CONTEXT_BOUNDED"}
       ],
       "all_copyrighted_source_image_bytes_transient":True,
       "source_image_bytes_in_public_artifacts":False,
       "professional_aesthetic_transfer_NOT_PROVEN":True
    }
    OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("R11_REAL_PUBLISHED_STAGES_GATE",json.dumps({"count":len(sources),"paired":paired,"hanyi":did_hy,
        "approved":result["approved_for_source_study"],
        "pixel_analysis":segment["nonregistered_bbox_ratios"] if segment else None},ensure_ascii=False))
if __name__=="__main__":main()
