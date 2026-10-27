#!/usr/bin/env python3
"""R11: source-pixel admission for REAL creator before/after glyph revision evidence.

Process only source image bytes in runner RAM. GitHub repo retains no third-party source
images or contours, only individual SHA256, decoded dimensions, coarse color statistics,
and source URLs for an auditable decision-supervision corpus.
"""
from __future__ import annotations
import datetime, hashlib, io, json, pathlib, time, urllib.request
from PIL import Image
import numpy as np

D=pathlib.Path(__file__).resolve().parent
MANIFEST=json.loads((D/"R11_FROZEN_AUTHORED_REVISION_CASES.json").read_text(encoding="utf-8"))
R10=json.loads((D.parent/"typography_r10"/"R10_IMAGE_SOURCE_BYTE_AUDIT.json").read_text(encoding="utf-8"))
OUT=D/"R11_ACTUAL_AUTHOR_IMAGE_AUDIT.json"
AGENT="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
def fetch(url):
    errors=[]
    for trial in range(3):
        try:
            host=url.split("/")[2]
            req=urllib.request.Request(url,headers={
                "User-Agent":AGENT,
                "Accept":"image/avif,image/webp,image/png,image/jpeg,image/*,*/*;q=0.8",
                "Referer":"https://"+host+"/"})
            with urllib.request.urlopen(req,timeout=26) as rsp:
                size=rsp.headers.get("Content-Length")
                if size and int(size)>8_000_000:raise ValueError("SOURCE_SIZE_HEADER_CAP")
                original=rsp.read(8_000_001)
                mimetype=rsp.headers.get("Content-Type","")
            if len(original)>8_000_000:raise ValueError("SOURCE_SIZE_CAP")
            im=Image.open(io.BytesIO(original));im.load()
            if im.width<360 or im.height<270 or im.width*im.height>32_000_000:
                raise ValueError("UNSUPPORTED_IMAGE_DIMENSIONS")
            return original,im,mimetype
        except Exception as e:
            errors.append(type(e).__name__+":"+str(e)[:280])
            if trial<2:time.sleep(1.5)
    raise RuntimeError(" | ".join(errors))
def color_proportions(im):
    # Do not record any original source image patches or author glyph contours.
    rgb=im.convert("RGB")
    rgb.thumbnail((160,160))
    arr=np.asarray(rgb,dtype=np.float32)
    r,g,b=np.moveaxis(arr,-1,0)
    red=(r>110)&(r>g*1.50)&(r>b*1.50)
    blue=(b>115)&(b>r*1.40)&(b>g*1.12)
    green=(g>110)&(g>r*1.22)&(g>b*1.15)
    yellow=(r>145)&(g>95)&(r>b*1.28)&(g>b*1.28)&(r>g*.9)
    colored={name:float(m.mean()) for name,m in [
        ("red",red),("blue",blue),("green",green),("yellow",yellow)]}
    graymask=(abs(r-g)<21)&(abs(r-b)<21)
    return {"color_fractions":{k:round(v,6) for k,v in colored.items()},
      "gray_neutral_fraction":round(float(graymask.mean()),6),
      "dark_fraction":round(float((arr.max(axis=-1)<95).mean()),6),
      "colors_present_above_0_15_pct":[k for k,v in colored.items() if v>=.0015]}
def main():
    a={x["id"]:x for x in R10.get("complete_sources",[])}
    results=[];failures=[]
    for case in MANIFEST["cases"]:
        item={k:case[k] for k in ["id","creator","source_page","image_url","original_stages","independent_visual_claim","negative_bound"]}
        item["creator_process_claim"]=case["process_author_claim"]
        try:
            if case["already_verified_r10"] and case["id"] in a:
                # Input reproducibility of previously checked bytes; do not simply trust a
                # previous run if the figure has drifted or image URL was substituted.
                item["previous_source_sha256"]=a[case["id"]]["sha256"]
            raw,im,mime=fetch(case["image_url"])
            digest=hashlib.sha256(raw).hexdigest()
            if case.get("expected_sha256") and digest!=case["expected_sha256"]:
                raise RuntimeError("FROZEN_ORIGINAL_SHA_CHANGED:"+digest)
            if item.get("previous_source_sha256") and item["previous_source_sha256"]!=digest:
                raise RuntimeError("PRIOR_AUDIT_DIGEST_MISMATCH")
            item.update({"actual_image_decoded":True,"sha256":digest,
               "bytes":len(raw),"dimensions":[im.width,im.height],"pixel_format":im.format,
               "response_media_type":mime,"coarse_color_evidence":color_proportions(im),
               "original_pixels_archived_to_repo":False,
               "actual_designer_source_project_available":False})
            results.append(item)
            print("REVISION_SOURCE_VERIFIED",case["id"],digest,im.size,item["coarse_color_evidence"]["color_fractions"])
        except Exception as e:
            item["actual_image_decoded"]=False
            item["download_error"]=str(e)[:940]
            failures.append(item)
            print("REVISION_SOURCE_FAIL",case["id"],str(e)[:300])
    studios={"Typotheque" if "Typotheque" in i["creator"] else
       "justfont" if "justfont" in i["creator"] else
       "Morisawa" if "Morisawa" in i["creator"] else i["creator"] for i in results}
    color_pairs=[]
    for z in results:
       f=z["coarse_color_evidence"]["color_fractions"]
       if z["id"]=="TPTQ_RADICAL_REVIEW" and f["red"]>.0015 and f["blue"]>.0015:
           color_pairs.append(z["id"])
       if z["id"].startswith("JUSTFONT_") and f["yellow"]>.0015 and f["green"]>.0015:
           color_pairs.append(z["id"])
    gate=(len(results)>=MANIFEST["positive_gate"]["min_verified_source_images"]
           and len(studios)>=MANIFEST["positive_gate"]["min_distinct_studios"]
           and len(color_pairs)>=MANIFEST["positive_gate"]["min_explicit_before_after_color_or_labels"])
    body={
      "schema":"vpd-r11-authentic-before-after-supervision-image-audit/1.0",
      "timestamp":datetime.datetime.now(datetime.timezone.utc).isoformat(),
      "frozen_manifest":"research/typography_r11/R11_FROZEN_AUTHORED_REVISION_CASES.json",
      "frozen_prior_receipt":"research/typography_r10/R10_IMAGE_SOURCE_BYTE_AUDIT.json",
      "verified_images":len(results),"verified_studios":sorted(studios),
      "before_after_color_evidence_verified":color_pairs,
      "verified":results,"failed":failures,
      "source_gate_pass":bool(gate),
      "training_samples_extracted":0,
      "authentic_executive_design_decisions_with_source_links":"STAGE_ADMISSION_ONLY",
      "visual_ranking_or_human_quality_scores":"NOT_ATTEMPTED",
      "actual_new_characters_drawn":False,
      "fine_grained_author_intent_verified_per_shape_change":False,
      "note":"Low-res color proportion is evidence of image-coded stages, NOT proof of what author intended, path geometry, tool movement, or aesthetic improvement.",
      "source_image_binary_copied_to_public_repo":False}
    OUT.write_text(json.dumps(body,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("R11_ACTUAL_DESIGNER_STAGE_GATE",json.dumps({
         "passed":gate,"verified_image_count":len(results),"studio_count":len(studios),
         "color_coded_phase_figures":len(color_pairs),"failed":len(failures)}))
if __name__=="__main__":main()
