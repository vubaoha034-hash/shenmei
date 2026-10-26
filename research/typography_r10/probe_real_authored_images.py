#!/usr/bin/env python3
"""R10: independently verify official third-party before/after evidence images.
Fetch originals into memory; commit only hashes, dimensions, limited derived diagnostics.
Never persist/reupload the original image pixels to a public GitHub repository.
"""
import datetime, hashlib, io, json, pathlib, time, urllib.error, urllib.request
from PIL import Image, ImageStat

HERE=pathlib.Path(__file__).resolve().parent
SOURCE=json.loads((HERE/"R10_FROZEN_FIRST_PARTY_STAGE_SOURCES.json").read_text(encoding="utf-8"))
RESULT=HERE/"R10_IMAGE_SOURCE_BYTE_AUDIT.json"
AGENT="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"

def image_stats(im):
    # Publicly safe aggregate statistics, not source pixel/contour reproductions.
    rgb=im.convert("RGB")
    thumb=rgb.copy(); thumb.thumbnail((128,128))
    pix=list(thumb.getdata()); count=max(len(pix),1)
    grayscale=sum(1 for r,g,b in pix if abs(r-g)<22 and abs(r-b)<22)/count
    dark=sum(1 for r,g,b in pix if max(r,g,b)<95)/count
    white=sum(1 for r,g,b in pix if min(r,g,b)>235)/count
    red=sum(1 for r,g,b in pix if r>g*1.55 and r>b*1.55 and r>100)/count
    blue=sum(1 for r,g,b in pix if b>r*1.37 and b>g*1.09 and b>95)/count
    return {k:round(v,5) for k,v in {
      "gray_neutral_fraction":grayscale,"dark_fraction":dark,
      "white_fraction":white,"red_fraction":red,"blue_fraction":blue}.items()}

def download(url):
    exceptions=[]
    for attempt in range(2):
      try:
        req=urllib.request.Request(url,headers={
           "User-Agent":AGENT,"Accept":"image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
           "Referer":url.split("/")[0]+"//"+url.split("/")[2]+"/"})
        with urllib.request.urlopen(req,timeout=28) as fd:
            mime=fd.headers.get("Content-Type","").split(";")[0].strip()
            raw=fd.read(10_000_001)
            if len(raw)>10_000_000: raise ValueError("DOWNLOAD_SIZE_CAP")
        im=Image.open(io.BytesIO(raw))
        im.load()
        if im.width<380 or im.height<250: raise ValueError("IMAGE_TOO_SMALL")
        if im.width*im.height>35_000_000: raise ValueError("IMAGE_PIXEL_CAP")
        return im,raw,mime
      except Exception as exc:
        exceptions.append(type(exc).__name__+":"+str(exc)[:230])
        if attempt==0:time.sleep(1.2)
    raise RuntimeError(" | ".join(exceptions))

def main():
   assets=[];errors=[]
   for item in SOURCE["sources"]:
      record={k:item[k] for k in ("id","type","creator","source_page","image_url","phase_labels")}
      try:
        im,raw,mime=download(item["image_url"])
        record.update({"source_bytes_read":True,"byte_length":len(raw),
          "sha256":hashlib.sha256(raw).hexdigest(),"media_type":mime,
          "actual_format":im.format,"dimensions":[im.width,im.height],
          "aggregate_neutral_rgb_diagnostic":image_stats(im),
          "stage_authenticity_classification":"Creator/publisher supplied illustration, not recoverable layered author source project",
          "uploaded_source_bytes_to_repository":False})
        assets.append(record)
        print("SOURCE_OK",record["id"],record["dimensions"],record["sha256"],record["byte_length"])
      except Exception as exc:
        record.update({"source_bytes_read":False,"error":str(exc)[:750]})
        errors.append(record)
        print("SOURCE_FAIL",record["id"],record["error"])
   unique_creators=len(set(x["creator"].split("/")[0] for x in assets))
   stages=[x for x in assets if x["type"] in
      ("direct-designer-same-glyph-before-after","creator-showcase-before-after")]
   verified=bool(len(assets)>=2 and unique_creators>=2 and len(stages)>=1)
   body={"schema":"vpd-r10-visual-author-evidence-byte-audit/1.0",
    "utc_recorded_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "input_frozen_source_manifest":"R10_FROZEN_FIRST_PARTY_STAGE_SOURCES.json",
    "aim":"Verify actual official author-provided multi-stage visual artwork, replace guesswork-only rule development.",
    "downloaded_sources":len(assets),"unique_creator_claims":unique_creators,
    "direct_before_after_sources_downloaded":len(stages),
    "actual_byte_and_decode_checked":True,
    "complete_sources":assets,"missing_sources":errors,
    "no_third_party_images_committed":True,
    "source_visual_pixels_used_for_training":False,
    "original_creator_psd_ai_figma_layers_available":False,
    "human_styled_glyph_review":"NOT_RUN",
    "shape_transfer_to_unseen_text":"NOT_RUN",
    "source_gate_pass":verified,
    "method_success_claimed":False,
    "next":"If source_gate_pass inspect published same-glyph before/after visually, transcribe changes and possible rule bounds. Must NOT infer pen pressure or exact Bezier control points from static images."}
   RESULT.write_text(json.dumps(body,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
   print("R10_SOURCE_GATE",json.dumps({"pass":verified,"downloaded":len(assets),"real_revision_pairs":len(stages),"unique_creator_names":unique_creators},ensure_ascii=False))
if __name__=="__main__":main()
