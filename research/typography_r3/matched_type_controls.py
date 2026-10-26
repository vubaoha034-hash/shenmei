#!/usr/bin/env python3
"""R3 same-text neutral-font controls for SHA1-verified Rosanjin mastheads.

Three fonts, two geometric alignments, identical text per comparison.
No original copyrighted source pixels are republished and NO actual
designer procedure, brush pressure or user aesthetic gain is claimed.
"""
import hashlib
import json
import pathlib
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
from scipy.ndimage import distance_transform_edt, label
from skimage.morphology import skeletonize, convex_hull_image
from skimage.measure import perimeter

ROOT = pathlib.Path("research/typography_r3")
INPUT = ROOT / "ROSANJIN_REMOTE_SOURCE_RECEIPT.json"
OUTPUT = ROOT / "ROSANJIN_MATCHED_FONT_CONTROLS.json"
FONTS = ("Noto Serif CJK TC", "Noto Sans CJK TC", "AR PL KaitiM Big5")
MODES = ("aspect_preserving", "match_ink_bbox")

def font_location(family):
    spec = subprocess.check_output(
        ["fc-match", "-f", "%{file}|%{index}|%{family}", family], text=True).strip()
    p, i, actual_family = spec.split("|", 2)
    if family not in actual_family:
        raise ValueError("FONT_FALLBACK_UNSUPPORTED_"+family+"_ACTUAL_"+actual_family)
    return pathlib.Path(p), int(i)

def render_font(text, font):
    tmp = Image.new("L", (2500, 600), 255)
    ImageDraw.Draw(tmp).text((35, 150), text, font=font, fill=0)
    ink = np.asarray(tmp) < 180
    if not np.any(ink):
        raise ValueError("FONT_NOT_RENDERED")
    yy, xx = np.nonzero(ink)
    return tmp.crop((int(xx.min()), int(yy.min()),
                     int(xx.max()+1), int(yy.max()+1)))

def place(cropped, width, height, mode):
    if mode == "aspect_preserving":
        scale = min(width/cropped.width, height/cropped.height)
        dest = (max(1, round(cropped.width*scale)),
                max(1, round(cropped.height*scale)))
    else:
        dest = (width, height)
    res = cropped.resize(dest, Image.Resampling.LANCZOS)
    img = Image.new("L", (width, height), 255)
    img.paste(res, ((width-res.width)//2,(height-res.height)//2))
    return img, list(dest)

def measure(img):
    mask = np.asarray(img.convert("L")) < 180
    yy, xx = np.nonzero(mask)
    if not len(xx):
        raise ValueError("MISSING_INK")
    x0, x1 = int(xx.min()), int(xx.max()+1)
    y0, y1 = int(yy.min()), int(yy.max()+1)
    roi = mask[y0:y1, x0:x1]
    widths = 2*distance_transform_edt(roi)[skeletonize(roi)]
    widths = widths[np.isfinite(widths)&(widths>0)]
    if len(widths)<20:
        raise ValueError("STROKE_WIDTH_SAMPLES_TOO_FEW")
    q = np.percentile(widths, (10,50,90))
    region_ids, _ = label(roi)
    regions = np.bincount(region_ids.ravel())[1:]
    outline = perimeter(roi, neighborhood=8)
    hull = perimeter(convex_hull_image(roi), neighborhood=8)
    return {
      "bbox_xywh": [x0,y0,int(x1-x0),int(y1-y0)],
      "ink_fraction_inside_bbox": round(float(roi.mean()),6),
      "stroke_width_px_p10_p50_p90":[round(float(v),4) for v in q],
      "stroke_width_p90_p10": round(float(q[2]/q[0]),5),
      "stroke_width_p50_relheight": round(float(q[1]/roi.shape[0]),6),
      "ink_perimeter_over_hull": round(float(outline/max(1,hull)),5),
      "connected_regions_ge3px": int(sum(v>=3 for v in regions))
    }

def main():
    receipt=json.loads(INPUT.read_text(encoding="utf-8"))
    refs=receipt["source_status"]
    if len(refs)!=3 or receipt.get("verified_sources")!=3:
        raise ValueError("SOURCE_AUDIT_NOT_3_OF_3")
    for ref in refs:
        if ref.get("status")!="SOURCE_VERIFIED_STATIC_IMAGE_MEASURED":
            raise ValueError("UNVERIFIED_SOURCE_"+ref["id"])
        if ref.get("sha1_verified")!=ref["source_svg_sha1_expected"]:
            raise ValueError("SHA1_MISMATCH_"+ref["id"])
    needed = "".join(ref["title"] for ref in refs)
    fonts=[]
    for family in FONTS:
        path,ttc_index=font_location(family)
        cmap=TTFont(str(path),fontNumber=ttc_index,lazy=True).getBestCmap()
        if not all(ord(ch) in cmap for ch in needed):
            raise ValueError("MISSING_CHARACTER_"+family)
        fonts.append((family,path,ttc_index))
    results=[]; metadata=[]
    for family,location,idx in fonts:
        metadata.append({"family":family,"font_basename":location.name,
            "collection_index":idx,"sha256":hashlib.sha256(location.read_bytes()).hexdigest(),
            "all_original_characters_present":True})
        f=ImageFont.truetype(str(location),190,index=idx)
        for ref in refs:
            target=ref["morphology"]["ink_bbox_px"]
            bbox_w,bbox_h=map(int,target[2:])
            src=render_font(ref["title"],f)
            for mode in MODES:
                rendered,sz=place(src,bbox_w,bbox_h,mode)
                results.append({"source_id":ref["id"],"text":ref["title"],
                    "font_family":family,"mode":mode,"target_bbox_wh":[bbox_w,bbox_h],
                    "natural_crop_wh":[src.width,src.height],
                    "fitted_crop_wh":sz,"metrics":measure(rendered)})
    if len(results)!=18:
        raise ValueError("NOT_18_MATCHED_CONTROLS")
    distinctions={}
    for name,source_key,ctrl_key in (
        ("thick_thin_ratio","stroke_width_tail_ratio_p90_over_p10","stroke_width_p90_p10"),
        ("relative_visual_weight","stroke_width_ratio_to_bbox_h_p10_p50_p90","stroke_width_p50_relheight"),
        ("contour_complexity","ink_perimeter_over_hull_perimeter","ink_perimeter_over_hull")):
        by_mode={}
        for mode in MODES:
            checks=[]
            for ref in refs:
                v=ref["morphology"][source_key]
                if name=="relative_visual_weight": v=v[1]
                cand=[x["metrics"][ctrl_key] for x in results if x["source_id"]==ref["id"] and x["mode"]==mode]
                deltas=[round((v-b)/max(b,1e-9),5) for b in cand]
                checks.append({"source_id":ref["id"],"source_value":v,
                   "baselines":cand,"fractional_differences":deltas,
                   "higher_all_three_by_15pct":all(d>=.15 for d in deltas),
                   "lower_all_three_by_15pct":all(d<=-.15 for d in deltas)})
            by_mode[mode]={"checks":checks,
                "higher_all":all(v["higher_all_three_by_15pct"] for v in checks),
                "lower_all":all(v["lower_all_three_by_15pct"] for v in checks)}
        robust=(all(by_mode[m]["higher_all"] for m in MODES) or
                all(by_mode[m]["lower_all"] for m in MODES))
        distinctions[name]={"robust_against_these_three_fonts_and_two_alignments":robust,
                             "threshold":.15,"by_mode":by_mode}
    summary={
      "schema_version":"r3-real-source-vs-matched-print-and-kaiti-fonts/1.0",
      "date":"2026-10-26","source_receipt":str(INPUT),
      "source_verified_sha1_count":3,
      "matched_text_and_glyph_count":3,
      "fonts":metadata,"sample_count":len(results),
      "methods":{"aspect_preserving":"font scaled proportionally to fit authentic ink bounding box",
      "match_ink_bbox":"font horizontally and vertically scaled into exact original bounding box; geometry distorts; test sensitivity",
      "threshold":180,
      "width":"2*distance_transform_edt of black mask at skeleton pixels; same as original validated source audit"},
      "comparisons":results,
      "distinguishing_candidate_features":distinctions,
      "not_conclusions":["This does not infer creator brush pressure, speed, deliberate operations, copyright status, causal superior art or success on unseen words",
      "Traditional block fonts and one Kaiti font are not an exhaustive control for authored expressive calligraphy",
      "N=3 original works cannot establish universal invariant, and digitization may affect image edge features",
      "No image generator has used these rules; no blind human preference data exists"],
      "promotion":"NONE"
    }
    OUTPUT.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("CONTROL_AUDIT_SUMMARY",
      json.dumps({"source_n":3,"control_n":len(results),
      "robust_candidate_features":{k:v["robust_against_these_three_fonts_and_two_alignments"] for k,v in distinctions.items()}},ensure_ascii=False))
if __name__=="__main__":
    main()
