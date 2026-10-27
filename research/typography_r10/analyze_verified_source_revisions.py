#!/usr/bin/env python3
"""R10-B: designer's original before/after image pixels, with provenance gates.
Original copyrighted photos processed in transient memory. Only low-dimensional
aggregate diagnostics and URL/source SHA are saved. No cropped source imagery.
"""
from __future__ import annotations
import hashlib, json, pathlib
from PIL import Image
import numpy as np
from scipy.ndimage import distance_transform_edt
from probe_real_authored_images import download

BASE=pathlib.Path(__file__).resolve().parent
SOURCE=json.loads((BASE/"R10_FROZEN_FIRST_PARTY_STAGE_SOURCES.json").read_text(encoding="utf-8"))
PREV=json.loads((BASE/"R10_IMAGE_SOURCE_BYTE_AUDIT.json").read_text(encoding="utf-8"))
KNOWN={v["id"]:v for v in PREV["complete_sources"]}
assert PREV["source_gate_pass"] is True

def basic(x):
    return {k:float(round(v,4)) if isinstance(v,float) else v for k,v in x.items()}

def color_contours(im):
    """Detect original red BEFORE, cyan/blue AFTER printed ink traces.
    No pixel content or detailed contour coordinates leave the runner.
    """
    im.thumbnail((1600,1600))
    z=np.asarray(im.convert("RGB")).astype(np.int16)
    r,g,b=z[:,:,0],z[:,:,1],z[:,:,2]
    before=(r>=125)&((r-g)>=42)&((r-b)>=38)
    after=(b>=111)&((b-r)>=34)&((b-g)>=9)
    h,w=before.shape
    out={
      "resampled_dimensions":[int(w),int(h)],
      "global_before_red_pixels":int(before.sum()),
      "global_after_blue_pixels":int(after.sum()),
      "before_after_color_labels_verified":bool(before.sum()>200 and after.sum()>200)
    }
    # Large source comparison figure on left; caption/specimen figures on right.
    # Regions explicitly labeled so metrics never silently represent same-glyph.
    for name,xstart,xend,ystart,yend in [
        ("full_image",0,w,0,h),
        ("left_visual_overlay",0,int(w*.60),0,int(h*.94)),
        ("right_context_specimens",int(w*.61),w,0,h)]:
      bm=before[ystart:yend,xstart:xend]
      am=after[ystart:yend,xstart:xend]
      rs=int(bm.sum());bs=int(am.sum())
      item={"region_label":name,"region_crop_ratio":[round(xstart/w,3),round(xend/w,3),round(ystart/h,3),round(yend/h,3)],
            "before_outline_red_pixels":rs,"after_outline_blue_pixels":bs}
      if rs>60 and bs>60:
        dist_to_after=distance_transform_edt(~am)
        dist_to_before=distance_transform_edt(~bm)
        d_before=dist_to_after[bm];d_after=dist_to_before[am]
        item.update({
          "median_before_to_after_distance_px":round(float(np.median(d_before)),3),
          "p90_before_to_after_distance_px":round(float(np.percentile(d_before,90)),3),
          "median_after_to_before_distance_px":round(float(np.median(d_after)),3),
          "pct_before_outline_within_4px_of_after":round(float((d_before<=4).mean()),4),
          "pct_before_outline_within_16px_of_after":round(float((d_before<=16).mean()),4),
          "note":"Color-label matching is geometric proximity in a collage, not outline-to-outline source path mapping. Caption figures and labels may affect pixels.",
        })
      out[name]=item
    return out

def stage_rules(item):
    uid=item["id"]
    if uid=="TPTQ_REVISION_NA":
       return {
          "visual_read":"Author's illustration labels red BEFORE and cyan AFTER for the same 阝 radical family, including a detailed overlay and example character 那.",
          "author_process_from_firsthand_text":"The project's component decisions are evaluated across large families; 阝 proportion was revised and the initially widened 口 was later narrowed after thousands of glyphs revealed inconsistency.",
          "supported_operator":"SHARED_COMPONENT_CROSS_GLYPH_REASSESSMENT",
          "input_condition":"A stylistic change appears coherent on one character but a related character family reveals inconsistency or altered readable space.",
          "author_response":"Recheck a whole family, revise affected component shape/proportion, then recheck in multi-character visual context.",
          "NOT_supported":"No recovered numerical universal formula; no original editable path; no proof all glyphs use exactly the same compensation.",
          "direct_same_glyph_before_after":True,"stage_order_verified_in_source":True
       }
    if uid=="HY_RED_CLOUD":
       return {
          "visual_read":"Award's staged poster shows historical gray exemplar, contour/hand-painted draft in the middle and bold finished glyph; the repeated examples include 樂 and 雲.",
          "author_process_from_firsthand_text":"Hanyi's designer credits historic clerical script, bolder contemporary stroke shape, distinctive stroke tip motion and refined overall character ink mass.",
          "supported_operator":"HISTORICAL_FORM_TO_DESIGNED_DRAWN_SHAPE_NOT_OUTLINE_COPY",
          "input_condition":"Historical source is a reference family, not a completed contemporary brand font.",
          "author_response":"First redraw at the whole-character level, then rebuild the finished glyph and review across multiple members of the family.",
          "NOT_supported":"Original vector node chronology/brush velocity and precise subjective decisions are unavailable; intermediate frame is an explanatory exhibit rather than a timestamped original design file.",
          "direct_same_glyph_before_after":False,"stage_order_verified_in_source":True
       }
    if uid=="ARPHIC_FANGXINSHU":
       return {
          "visual_read":"Designer's graphic explicitly labels Before and After around the same glyph phrase and a separately enlarged inner turn/curve. Changes remain local and targeted, not universal texture application.",
          "author_process_from_firsthand_text":"Designer presents shape refinements as necessary to maintain consistency/readability in a condensed typeface.",
          "supported_operator":"LOCAL_INNER_COUNTER_COMPENSATION_IN_CONTEXT",
          "input_condition":"Narrow type variant makes inner contour too tight or shape visually inconsistent.",
          "author_response":"Modify the relevant curved stroke/counter; visually compare with an unchanged glyph and at the word/line scale.",
          "NOT_supported":"Neither the poster nor source demonstrates that its before and after can be encoded as one generic scale coefficient.",
          "direct_same_glyph_before_after":True,"stage_order_verified_in_source":True
       }
    return {
      "visual_read":"Standard and condensed variants compare left components and white-space allocation, not an authenticated chronological single-glyph revision.",
      "supported_operator":"TYPEFACE_VARIANT_SIDE_BY_SIDE_ONLY",
      "direct_same_glyph_before_after":False,"stage_order_verified_in_source":False,
      "NOT_supported":"Do not count this as a distinct historical before/after creator edit.",
    }

def main():
  out=[]
  for source in SOURCE["sources"]:
    ident=source["id"];expect=KNOWN[ident]
    im,raw,mime=download(source["image_url"])
    digest=hashlib.sha256(raw).hexdigest()
    assert digest==expect["sha256"],f"IMAGE_HASH_CHANGED:{ident}"
    assert [im.width,im.height]==expect["dimensions"],f"IMAGE_DIMENSIONS_CHANGED:{ident}"
    entry={"id":ident,"source_page":source["source_page"],"image_url":source["image_url"],
           "verified_source_sha256":digest,
           "verified_dimensions":expect["dimensions"],
           "authored_content":stage_rules(source),
           "source_rights":"Observation and citations only; no rights claimed to redistribute or model-train on source artwork."}
    if ident=="TPTQ_REVISION_NA":
       entry["observed_overlay_pixel_diagnostics"]=color_contours(im)
       assert entry["observed_overlay_pixel_diagnostics"]["before_after_color_labels_verified"],"NO_VERIFIED_RED_BLUE_OUTLINES"
       assert entry["observed_overlay_pixel_diagnostics"]["left_visual_overlay"]["before_outline_red_pixels"]>100
       assert entry["observed_overlay_pixel_diagnostics"]["left_visual_overlay"]["after_outline_blue_pixels"]>100
    out.append(entry)
  evidenced=[item for item in out if item["authored_content"]["direct_same_glyph_before_after"]]
  compliant={
    "schema":"vpd-r10-designer-authored-before-after-visual-observation/1.0",
    "date":"2026-10-27",
    "all_original_images_re_read_and_hash_verified":True,
    "source_cases_checked":len(out),
    "real_same_glyph_revision_cases":len(evidenced),
    "direct_before_after_ids":[x["id"] for x in evidenced],
    "research_allowed":"Critique source changes at high level, do not reuse source's copyrighted glyph geometry or train proprietary model.",
    "stages":out,
    "discovered_procedure":[
       "Select source that actually documents author changes across stages, not only a gallery of final fonts.",
       "Pair the visual edit with the author's explicit reason: distortion of counters, cross-family inconsistency, historical style adaptation.",
       "Form condition/action/rejection criteria, never universal direction-only thickness formulas.",
       "Test whether operator even applies to a different structural family BEFORE generating output.",
       "Actual unseen authored lettering + independent human preference is necessary to declare creative-method transfer."
    ],
    "non_gates":[
       "This documents causal direction from credited author narratives, not exactly inferred original path-edit actions.",
       "Pixel color distances in the illustrative image are not aesthetic goodness scores.",
       "The user's past R1-R9 shape modifications were not proven artistically superior.",
       "No new pay-per-image service, no commercial rights established or paid font obtained."
    ],
    "source_visual_gate":True,
    "author_intent_deduced_from_art_only":False,
    "unseen_visual_transfer_pass":False,
    "human_blind_review_pass":False,
    "professional_lettering_skill_learned":False
  }
  p=BASE/"R10_VERIFIED_ACTUAL_BEFORE_AFTER_VISUAL_AUDIT.json"
  p.write_text(json.dumps(compliant,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
  summary={"image_hash_pass":True,"images":len(out),"same_glyph_cases":len(evidenced),
           "color_edit_diagnostics":next(x["observed_overlay_pixel_diagnostics"] for x in out if x["id"]=="TPTQ_REVISION_NA"),
           "source_only":True,"quality_claim":False}
  print("R10_VISUAL_SEMANTIC_GATE",json.dumps(summary,ensure_ascii=False))
if __name__=="__main__":main()
