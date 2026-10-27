#!/usr/bin/env python3
"""R10: author-published BEFORE/AFTER pixels are evidence, not style-training labels.
Public-repo output: checksums, source stage audit, red-blue alignment stats, no image bytes.
"""
from __future__ import annotations
import datetime, hashlib, io, json, pathlib, time, urllib.request, urllib.error
import numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt

ROOT=pathlib.Path(__file__).resolve().parent
FROZEN=json.loads((ROOT/"R10_FROZEN_FIRST_PARTY_STAGE_SOURCES.json").read_text(encoding="utf-8"))
FIRST_AUDIT=json.loads((ROOT/"R10_IMAGE_SOURCE_BYTE_AUDIT.json").read_text(encoding="utf-8"))
TARGET=ROOT/"R10_REAL_STAGE_AUTHOR_PIXEL_INTERPRETATION.json"
PIN={x["id"]:x for x in FIRST_AUDIT["complete_sources"]}
AGENT="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
STAGE_LABELS={
 "HY_RED_CLOUD":{
   "classification":"HISTORIC_MODEL_TO_DESIGN_DRAFT_TO_FINAL",
   "confirmed_visible_stages":["older historical reference shape (gray)","hand-drawn/traced exploratory outline marked hand-painted first draft","final bold Chinese font glyph"],
   "high_confidence_observation":"Across two same-character rows, the middle outline drafts clearly are not a flat stroke-width expansion; the finals merge and prioritize distinct structural masses and shaped terminals.",
   "source_process_boundary":"Historical reference is NOT first designer-authored intermediate; finished-font artwork cannot reveal physical pen speed/pressure or unique artist algorithm.",
   "claim_license":"Published DFA winner showcase of Hanyi Fonts, not libre training data. Text/aggregate study only."},
 "TPTQ_REVISION_NA":{
   "classification":"AUTHORED_BEFORE_AFTER_SAME_RADICAL",
   "confirmed_visible_stages":["red BEFORE contours/small specimen","blue AFTER contours/small specimen","overlay explicitly labels correction of 阝 radical"],
   "high_confidence_observation":"There is a before/after outline shift in the same component's proportions and curve trajectory, beyond a full-image filter or global stroke taper.",
   "source_process_boundary":"DO NOT confuse this 阝 demonstration with the different prose example where a widened 口 design had to be rolled back after a large-character set test.",
   "claim_license":"Creator Typotheque article; observational image analysis only, rights not cleared for training or redistribution."},
 "ARPHIC_FANGXINSHU":{
   "classification":"AUTHORED_BEFORE_AFTER_DETAIL_CORRECTION",
   "confirmed_visible_stages":["top BEFORE and lower AFTER Chinese phrase","bottom BEFORE/AFTER magnified narrowed terminal/counter with labels"],
   "high_confidence_observation":"The same compressed-style glyph uses a locally different inner aperture/corner shape after correction; improving smaller counters calls for localized geometry, not whole-glyph uniform narrowing.",
   "source_process_boundary":"This figure does not on its own establish effects on unknown calligraphic lettering or a controlled typography preference win.",
   "claim_license":"Creator owned Behance Arphic/Lin Mickey project, no source-contour redistribution or model training rights assumed."},
 "ARPHIC_FANGXINSHU_SPACE":{
   "classification":"DESIGNED_VARIANT_NOT_CHRONOLOGICAL_REVISION",
   "confirmed_visible_stages":["normal-width face characters 仁 and 空","condensed C80 variant with differently arranged internal negative space"],
   "high_confidence_observation":"Condensed design changes relative internal spaces and structural balance; visually distinct from a literal squeezed screenshot.",
   "source_process_boundary":"The labels describe standard vs C80 FONT VARIANTS, not author-before vs author-after chronological stages. EXCLUDE from before/after training pairs.",
   "claim_license":"Creator owned Arphic Behance source; no train permission inferred."}
}
def fetch(url):
    host=url.split("/")[2]
    req=urllib.request.Request(url,headers={"User-Agent":AGENT,"Accept":"image/*,*/*;q=0.8","Referer":"https://"+host+"/"})
    with urllib.request.urlopen(req,timeout=28) as fd:
        b=fd.read(12_000_001)
        if len(b)>12_000_000:raise RuntimeError("DOWNLOAD_LIMIT")
    im=Image.open(io.BytesIO(b));im.load()
    return b,im.convert("RGB")
def bbox(mask):
    ys,xs=np.nonzero(mask)
    if not len(xs):return None
    return [int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
def red_blue_channel_pair(im):
    x=np.asarray(im).astype(np.float32)
    red=(x[:,:,0]>120)&(x[:,:,0]>x[:,:,1]*1.65)&(x[:,:,0]>x[:,:,2]*1.3)
    blue=(x[:,:,2]>120)&(x[:,:,2]>x[:,:,0]*1.27)&(x[:,:,2]>x[:,:,1]*1.07)
    h,w=red.shape
    # The visual overlay is displayed on the LEFT in source image; right samples are separated before/after.
    # This region is frozen from article figure layout before run (not optimized after result).
    zone_stop_x=round(w*0.60)
    mr=red[:, :zone_stop_x]
    mb=blue[:, :zone_stop_x]
    n1,n2=int(mr.sum()),int(mb.sum())
    if n1<150 or n2<150:return {"is_overlay_separable":False,"red_count":n1,"blue_count":n2,
        "note":"NOT_ENOUGH_COLOR_PIXELS_TO_INFER_OVERLAY_CHANGE"}
    def nearest(mask,other):
       dt=distance_transform_edt(~other)
       values=dt[mask]
       return {"median_px":round(float(np.median(values)),3),"p90_px":round(float(np.percentile(values,90)),3),"max_px":round(float(values.max()),3)}
    # 4x4 heat map for target observation, no bitmap replication; localized sparse diagnostics.
    grid=[]
    for yy in range(4):
        row=[]
        for xx in range(4):
            y0=round(h*yy/4);y1=round(h*(yy+1)/4)
            x0=round(zone_stop_x*xx/4);x1=round(zone_stop_x*(xx+1)/4)
            row.append([int(mr[y0:y1,x0:x1].sum()),int(mb[y0:y1,x0:x1].sum())])
        grid.append(row)
    return {
      "is_overlay_separable":True,
      "overlay_left_fraction":0.6,"red_before_outline_pixels":n1,
      "blue_after_outline_pixels":n2,
      "red_bbox_px":bbox(mr),"blue_bbox_px":bbox(mb),
      "red_to_blue_nearest":nearest(mr,mb),
      "blue_to_red_nearest":nearest(mb,mr),
      "coarse_red_blue_pixel_count_4x4":grid,
      "interpretation_boundary":"These are after JPEG/PNG rasterization and masks of colored outlines; displacement means observable revision, NOT proof of improvement or original vector-point path."
    }
def main():
    results=[];errs=[]
    for src in FROZEN["sources"]:
        sid=src["id"]
        if sid not in STAGE_LABELS:raise RuntimeError("UNCLASSIFIED_SOURCE_"+sid)
        try:
            raw,im=fetch(src["image_url"])
            original=PIN[sid]
            sha=hashlib.sha256(raw).hexdigest()
            if sha!=original["sha256"]:raise RuntimeError("CHECKSUM_DIFFERENT_FROM_R10_FIRST_AUDIT")
            if list(im.size)!=original["dimensions"]:raise RuntimeError("DIMENSIONS_DIFFER_FROM_R10_FIRST_AUDIT")
            record={"source_id":sid,"source_page":src["source_page"],
              "original_sha256":sha,"original_pixel_size":[im.width,im.height],
              "byte_verified_against_first_audit":True,**STAGE_LABELS[sid],
              "has_actual_author_better_output":True,
              "human_blind_quality_preference":"NOT_MEASURED",
              "raw_source_images_committed":False}
            if sid=="TPTQ_REVISION_NA":
                record["quantitative_overlay_evidence"]=red_blue_channel_pair(im)
                assert record["quantitative_overlay_evidence"]["is_overlay_separable"],"NO_ACTUAL_BEFORE_AFTER_PIXELS"
            results.append(record)
            print("R10_STAGE_PIXEL_VERIFIED",sid,sha[:16],str(im.size),record["classification"])
        except Exception as ex:
            print("R10_STAGE_SOURCE_FAILURE",sid,str(ex)[:280])
            errs.append({"source_id":sid,"error":str(ex)[:360]})
    # Public evidence *must* separate real stages from designs compared only as width variants.
    actual=[x for x in results if x["classification"] in
        ("HISTORIC_MODEL_TO_DESIGN_DRAFT_TO_FINAL","AUTHORED_BEFORE_AFTER_SAME_RADICAL",
         "AUTHORED_BEFORE_AFTER_DETAIL_CORRECTION")]
    variant=[x for x in results if x["classification"]=="DESIGNED_VARIANT_NOT_CHRONOLOGICAL_REVISION"]
    verdict={
       "schema":"vpd-r10-authored-stage-image-visual-audit/1.0",
       "utc_recorded_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),
       "source_images_reverified":len(results),"actual_author_revision_or_draft_sources":len(actual),
       "author_variant_not_timeline_sources":len(variant),
       "verified_no_raw_visual_redistribution":True,"original_design_process_layers":False,
       "stage_sources":results,"source_errors":errs,
       "admissible_insights":[
         "AUTHORING_STAGES: source style reference → many preliminary contour ideas → purposefully recomposed final mass; NOT naive font weight increase.",
         "RADICAL_SYSTEM_REVISION: one component must be revised against many occurrences, and contextual shapes must adapt; same-glyph red/blue overlay grounds a real change.",
         "LOCAL_NEGATIVE_SPACE_REPAIR: compressed font needs re-design of enclosed pockets and stroke clearance, rather than uniform squeezed shape."
       ],
       "blocking_unknowns":[
         "No native editable author design documents, Bezier histories or ground truth reasons for all local changes.",
         "Cannot establish causality of improved aesthetics from after-before alone; the authors' expert decisions and evaluation remain key.",
         "These precedents show typography/system font work. Transferability to unique brush calligraphy headlines is not yet validated.",
         "Commercial/private AI training use of these copyrighted images is NOT licensed just by web availability."
       ],
       "human_blind_aesthetic_review":"NOT_RUN",
       "new_unseen_Chinese_lettering_output":"NOT_RUN",
       "claim_validated_creator_method":False,
       "minimum_gate_pass":len(actual)==3 and len(variant)==1 and
                any(x.get("quantitative_overlay_evidence",{}).get("is_overlay_separable") for x in actual),
       "next_gate":"Freeze ONE character-level shape decision with author-supported visual cause and source example, identify 2+ held-out structurally distinct cases, compare against do-nothing and mechanical controls with equal output budget; do NOT copy artwork."
    }
    (ROOT/"R10_AUTHORED_STAGE_VISUAL_AUDIT.json").write_text(
       json.dumps(verdict,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("R10_VISUAL_AUDIT_GATES",json.dumps({"source_images":len(results),"stage_sources":len(actual),
       "variant_not_before_after":len(variant),"pass":verdict["minimum_gate_pass"]},ensure_ascii=False))
if __name__=="__main__":main()
