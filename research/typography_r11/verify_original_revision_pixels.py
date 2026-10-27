#!/usr/bin/env python3
"""R11 original-author before/after visual evidence verifier.

Fetch actual public publisher bitmap bytes only into transient memory, verify SHA,
decode pixels and measure visible color-coded change. Commit derived diagnostics
only; never copy, crop, upload or embed original publisher photos into this repo.
"""
from __future__ import annotations
import hashlib, io, json, math, pathlib, urllib.request, datetime
from PIL import Image
import numpy as np
from scipy import ndimage

BASE=pathlib.Path(__file__).resolve().parent
PROTOCOL=json.loads((BASE/"R11_AUTHORED_REVISION_SOURCE_FREEZE.json").read_text(encoding="utf-8"))
OUT=BASE/"R11_REAL_AUTHOR_STAGE_PIXEL_DIAGNOSTICS.json"
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"

def fetch_image(src):
    url=src["uri"]
    req=urllib.request.Request(url,headers={
        "User-Agent":UA,"Accept":"image/png,image/jpeg,image/webp,image/*;q=.7",
        "Referer":"https://www.typotheque.com/"})
    with urllib.request.urlopen(req,timeout=26) as fd:
        mime=fd.headers.get("Content-Type","").split(";")[0]
        raw=fd.read(15_000_001)
        assert len(raw)<=15_000_000,"SOURCE_SIZE_CAP_EXCEEDED"
    im=Image.open(io.BytesIO(raw));im.load()
    assert im.width>=600 and im.height>=400
    assert im.width*im.height<=12_000_000
    sha=hashlib.sha256(raw).hexdigest()
    if src.get("expected_sha256"): assert sha==src["expected_sha256"],"R10_PINNED_SHA_MISMATCH"
    if src.get("expected_dimensions"): assert list(im.size)==src["expected_dimensions"],"R10_PINNED_SIZE_MISMATCH"
    return im,raw,mime

def scaled_rgb(im,max_side=1000):
    z=im.convert("RGB");z.thumbnail((max_side,max_side),Image.Resampling.LANCZOS)
    return np.asarray(z,dtype=np.uint8)

def color_masks(rgb):
    a=rgb.astype(np.int16)
    r,g,b=a[...,0],a[...,1],a[...,2]
    red=(r>125)&(r-g>65)&(r-b>65)
    cyan=(b>110)&(b-r>65)&(g-r>55)&(b-g>=-35)
    return red,cyan

def bounds(mask):
    yy,xx=np.nonzero(mask)
    if not len(xx):return None
    return [int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)]

def largest_cluster_color(mask,dilate=9,min_color_pixels=80):
    # A glyph's disconnected strokes may become a group; labels remain separate.
    # Grouping is not asserted as perfect segmentation of the author's geometry.
    if not mask.any():return None
    spread=ndimage.binary_dilation(mask,iterations=dilate)
    components,n=ndimage.label(spread)
    best=None
    for k in range(1,n+1):
        component=components==k
        color_pixels=int(np.count_nonzero(component&mask))
        if color_pixels<min_color_pixels:continue
        by=bounds(component&mask)
        if by is None:continue
        item={"color_pixels":color_pixels,"bbox":by,"label_id":k,
              "pixel_mask":component&mask}
        if best is None or color_pixels>best["color_pixels"]:best=item
    return best

def colored_revision_diagnostics(im):
    rgb=scaled_rgb(im)
    h,w=rgb.shape[:2]
    red,cyan=color_masks(rgb)
    split=int(w*.53)
    ys=np.arange(h)[:,None]
    xs=np.arange(w)[None,:]
    # Document-aligned right region; labels may remain and must not masquerade as glyph segments.
    before_region=(xs>=split)&(ys<h*.53)
    after_region=(xs>=split)&(ys>h*.38)
    before=largest_cluster_color(red & before_region)
    after=largest_cluster_color(cyan & after_region)
    color_presence={"global_red_pixels":int(red.sum()),"global_cyan_pixels":int(cyan.sum()),
       "upper_right_red_pixels":int((red&before_region).sum()),
       "lower_right_cyan_pixels":int((cyan&after_region).sum()),
       "red_upper_region_fraction":round(float(np.count_nonzero(red&before_region)/max(1,red.sum())),4),
       "cyan_lower_region_fraction":round(float(np.count_nonzero(cyan&after_region)/max(1,cyan.sum())),4)}
    result={"source_thumbnail_pixels":[w,h],"primary_colors":color_presence,
         "segmentation_method":"hue-masked largest local connected group after 9-pixel dilation; NOT original graphic vector data",
         "same_glyph_claim_source":"Publisher photo explicitly labels red BEFORE and cyan AFTER; author's paragraph identifies the 阝 right-side radical."}
    for key,item in (("before",before),("after",after)):
       result[key+"_region"]=None if item is None else {
         "colored_stroke_pixels":item["color_pixels"],
         "x_y_bounds_thumbnail":item["bbox"],
         "bounding_wh":[item["bbox"][2]-item["bbox"][0],item["bbox"][3]-item["bbox"][1]],
       }
    if before is not None and after is not None:
        # The visual source contains two color-coded fonts and the original color-coded overlay.
        # Different normalized pixel shapes indicate changed contours; aggregate registration is approximate.
        data=[]
        for item in [before,after]:
          mask=item["pixel_mask"];x0,y0,x1,y1=item["bbox"]
          clip=Image.fromarray((mask[y0:y1,x0:x1]*255).astype(np.uint8),"L")
          clip.thumbnail((180,180),Image.Resampling.NEAREST)
          stage=np.zeros((220,220),bool)
          px,py=(220-clip.width)//2,(220-clip.height)//2
          stage[py:py+clip.height,px:px+clip.width]=(np.asarray(clip)>0)
          data.append(stage)
        aa,bb=data
        inter=int((aa&bb).sum());union=int((aa|bb).sum())
        ratio=inter/max(1,union)
        result["approx_shape_overlap_normalized"]=round(ratio,4)
        result["approx_shape_difference_fraction"]=round(1-ratio,4)
        result["registered_before_after_precision"]="LOW: independently cropped color-blobs; color-antialias, unequal display scale, labels and segmentation can affect numbers"
    else:
        result["approx_shape_overlap_normalized"]=None
        result["registered_before_after_precision"]="NOT_MEASURABLE"
    result["source_color_stage_detection_pass"]=bool(
         color_presence["upper_right_red_pixels"]>500
         and color_presence["lower_right_cyan_pixels"]>500
         and before is not None and after is not None
         and before["color_pixels"]>150 and after["color_pixels"]>150)
    return result

def generic_color_diagnostic(im):
    rgb=scaled_rgb(im)
    red,cyan=color_masks(rgb)
    return {"preview_width_height":[int(rgb.shape[1]),int(rgb.shape[0])],
      "red_or_annotation_pixels":int(red.sum()),"cyan_or_annotation_pixels":int(cyan.sum()),
      "not_same_glyph_diff_if_no_explicit_before_after":True}

def main():
    out=[];fail=[]
    for src in PROTOCOL["images"]:
       entry={"id":src["id"],"publisher":"Typotheque","role":src["role"],
              "url":src["uri"],"declared_source_caption":src["source_label"]}
       try:
         im,raw,mime=fetch_image(src)
         entry.update({"source_read":True,"sha256":hashlib.sha256(raw).hexdigest(),
             "bytes":len(raw),"file_format":im.format,"content_type":mime,
             "dimensions":list(im.size),"source_original_raw_pixels_persisted":False})
         if src["id"]=="BEFORE_AFTER_RIGHT_RADICAL":
           entry["author_same_glyph_revision"]=colored_revision_diagnostics(im)
         else:
           entry["diagnostic"]=generic_color_diagnostic(im)
         out.append(entry)
         print("R11_SOURCE_READ",src["id"],im.size,entry["sha256"],"bytes",len(raw))
       except Exception as exc:
         entry.update({"source_read":False,"error":str(exc)[:350]})
         fail.append(entry)
         print("R11_SOURCE_FAILED",src["id"],entry["error"])
    same=next((x for x in out if x["id"]=="BEFORE_AFTER_RIGHT_RADICAL"),{})
    score=same.get("author_same_glyph_revision",{})
    passed=bool(len(out)==3 and score.get("source_color_stage_detection_pass") and
                same.get("sha256")==PROTOCOL["images"][1].get("expected_sha256"))
    report={"schema":"vpd-r11-verified-first-party-revision-pixels/1.0",
            "executed_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "publisher":"Typotheque","source_url":PROTOCOL["source"],
            "before_and_after_character":"那",
            "right_component_under_review":"阝",
            "detector_scope":"separate red-before/cyan-after regions ONLY (not full semantic shape diagnosis)",
            "source_images":out,"failures":fail,
            "source_gate_pass":passed,"pixel_artifact_shas_verified":sum(bool(x.get("sha256")) for x in out),
            "valid_same_glyph_before_after_source":bool(score.get("source_color_stage_detection_pass")),
            "rights_safe":True,"copyrighted_source_images_committed":False,
            "designer_before_after_visual_class":"VERIFIED_PUBLISHER_LABELED_CHANGES",
            "designer_process_parameters_extracted":False,
            "unseen_chinese_wordmark_generated":False,"human_aesthetic_blind_pass":False,
            "limitations":[
              "A published annotated image is not an editable author-layer history nor proof of pen pressure.",
              "Basic hue segmentation does not prove optical superiority or exact per-point contour displacement.",
              "The published text says repeated radical correction was required after looking at many glyphs; exact numerical author choices are unknown.",
              "OCR or blind quality evaluation not run. Do not promote an aesthetic rule from this audit alone."],
            "next":"Frame source-supported when/why/family-scope decisions and compare with R7-R9 false independent width ratios; require a drawn, genuinely changed new character and real human aesthetic review to validate transfer."}
    OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("R11_REAL_REVISION_GATE",json.dumps({"passed":passed,"decoded_sources":len(out),
           "before_after_has_two_separate_color_regions":bool(score.get("source_color_stage_detection_pass")),
           "color_stats":score.get("primary_colors"),"normalized_overlap":score.get("approx_shape_overlap_normalized")},ensure_ascii=False))
if __name__=="__main__":main()
