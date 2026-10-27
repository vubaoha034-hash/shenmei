#!/usr/bin/env python3
"""R11 - first-party Chinese letterform draft and before/after source verification.

Source bitmap bytes are decoded in memory and never saved to the repository.
Computed, nonreconstructable statistics only are committed; never distribute
source intellectual property as model training data.
"""
from __future__ import annotations
import datetime, hashlib, io, json, pathlib, time, urllib.request
from PIL import Image

HERE=pathlib.Path(__file__).parent
SOURCE=json.loads((HERE/"R11_SOURCE_SET_FROZEN.json").read_text(encoding="utf-8"))
OUTPUT=HERE/"R11_SOURCE_IMAGE_BYTE_AND_STAGE_CHECK.json"
USER_AGENT="Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"

def fetch(url):
    failures=[]
    for k in range(2):
        try:
            req=urllib.request.Request(url,headers={
                "User-Agent":USER_AGENT,
                "Accept":"image/avif,image/webp,image/png,image/jpeg,image/*,*/*;q=0.8",
                "Referer":"/".join(url.split("/")[:3])+"/"
            })
            with urllib.request.urlopen(req,timeout=26) as f:
                raw=f.read(12_000_001); declared_mime=f.headers.get("Content-Type","").split(";")[0].strip()
            if len(raw)>12_000_000:raise RuntimeError("IMAGE_TOO_LARGE")
            im=Image.open(io.BytesIO(raw));im.load()
            if im.width<400 or im.height<300:raise RuntimeError("IMAGE_TOO_SMALL")
            if im.width*im.height>30_000_000:raise RuntimeError("DECODED_SIZE_TOO_BIG")
            return im,raw,declared_mime
        except Exception as e:
            failures.append(type(e).__name__+":"+str(e)[:210])
            if k==0:time.sleep(1.1)
    raise RuntimeError(" | ".join(failures))

def colors(img):
    # CRITICAL: transparent images must be composited on neutral white before
    # measuring visible darkness or edge colors; RGB conversion alone treats
    # invisible black transparent pixels as visible black and corrupts metrics.
    rgba=img.convert("RGBA")
    rgba.thumbnail((450,450))
    alpha=list(rgba.getchannel("A").getdata())
    opaque_fraction=sum(1 for a in alpha if a>250)/max(1,len(alpha))
    transparent_fraction=sum(1 for a in alpha if a<5)/max(1,len(alpha))
    canvas=Image.new("RGBA",rgba.size,(255,255,255,255))
    canvas.alpha_composite(rgba)
    im=canvas.convert("RGB")
    pp=list(im.getdata());total=len(pp) or 1
    colors0={}
    for name,fn in [
      ("black_ink",lambda r,g,b:max(r,g,b)<85),
      ("bright_paper",lambda r,g,b:min(r,g,b)>239),
      ("yellow_before",lambda r,g,b:r>145 and g>80 and b<180 and r>g*1.10 and g>b*1.23),
      ("green_after",lambda r,g,b:g>78 and g>r*1.17 and g>b*1.09 and b<190),
      ("red_annotations",lambda r,g,b:r>120 and r>g*1.6 and r>b*1.55),
      ("cyan_annotations",lambda r,g,b:g>110 and b>110 and g>r*1.35 and b>r*1.3),
      ("neutral_ink",lambda r,g,b: abs(r-g)<24 and abs(g-b)<24 and max(r,g,b)<180),
    ]:
        colors0[name]=sum(1 for t in pp if fn(*t))
    bbox_masks={}
    w,h=im.size
    for name in ["yellow_before","green_after","red_annotations","cyan_annotations"]:
        fn={
            "yellow_before":lambda r,g,b:r>145 and g>80 and b<180 and r>g*1.10 and g>b*1.23,
            "green_after":lambda r,g,b:g>78 and g>r*1.17 and g>b*1.09 and b<190,
            "red_annotations":lambda r,g,b:r>120 and r>g*1.6 and r>b*1.55,
            "cyan_annotations":lambda r,g,b:g>110 and b>110 and g>r*1.35 and b>r*1.3,
        }[name]
        xs,ys=[],[]
        for y in range(h):
            for x in range(w):
                if fn(*pp[y*w+x]):xs.append(x);ys.append(y)
        if len(xs)>=60:
            bbox_masks[name]=[round(min(xs)/w,4),round(min(ys)/h,4),
                              round(max(xs)/w,4),round(max(ys)/h,4)]
    return {"downsampled_size":list(im.size),
       "visible_background_compositing":"RGBA_OVER_OPAQUE_WHITE",
       "original_alpha_fraction_opaque":round(opaque_fraction,5),
       "original_alpha_fraction_transparent":round(transparent_fraction,5),
       "source_mode":img.mode,
       "pixel_counts":colors0,
       "relative_color_fractions":{k:round(v/total,5) for k,v in colors0.items()},
       "normalized_color_bbox_of_visible_deviation":bbox_masks}

def run():
    ok=[];fail=[]
    for source in SOURCE["firsthand_sources"]:
        row={k:source[k] for k in ["id","creator","source_page","url","evidence_type"]}
        try:
            im,raw,mime=fetch(source["url"])
            # Record exact visible pixels independent of metadata/compression.
            composite=Image.new("RGBA",im.size,(255,255,255,255))
            composite.alpha_composite(im.convert("RGBA"))
            visible_hash=hashlib.sha256(composite.convert("RGB").tobytes()).hexdigest()
            row["visible_pixel_sha256"]=visible_hash
            if source["id"]=="JUSTFONT_BEFORE_AFTER":
                # The original URL has returned different PNG byte hashes across
                # runs. Recheck content in this SAME audit. Fail closed on actual
                # artwork changes even if a CDN recompresses the bytes.
                re_im,re_raw,_=fetch(source["url"])
                re_comp=Image.new("RGBA",re_im.size,(255,255,255,255))
                re_comp.alpha_composite(re_im.convert("RGBA"))
                rerender_hash=hashlib.sha256(re_comp.convert("RGB").tobytes()).hexdigest()
                row["second_fetch_byte_sha256"]=hashlib.sha256(re_raw).hexdigest()
                row["second_fetch_visible_pixel_sha256"]=rerender_hash
                row["same_visible_pixels_double_fetch"]=bool(rerender_hash==visible_hash)
                row["same_exact_bytes_double_fetch"]=bool(re_raw==raw)
            row.update({"verified":True,"sha256":hashlib.sha256(raw).hexdigest(),
               "bytes":len(raw),"dimensions":[im.width,im.height],
               "format":im.format,"mime_from_server":mime,
               "pixel_color_analysis":colors(im),
               "source_pixels_uploaded":False})
            if source["id"]=="JUSTFONT_BEFORE_AFTER":
                pp=row["pixel_color_analysis"]["pixel_counts"]
                # Distinct orange/yellow and green outlines must both exist.
                row["before_after_color_visible"]=bool(
                    pp["yellow_before"]>=70 and pp["green_after"]>=80)
            ok.append(row)
            print("AUTHORED_IMAGE_OK",row["id"],row["dimensions"],row["sha256"],
              "color_pair=",row.get("before_after_color_visible","not_applicable"))
        except Exception as e:
            row.update({"verified":False,"error":str(e)[:650]})
            fail.append(row);print("AUTHORED_IMAGE_FAIL",row["id"],row["error"])
    byid={x["id"]:x for x in ok}
    paired_source=byid.get("JUSTFONT_BEFORE_AFTER",{})
    visible_pair=paired_source.get("before_after_color_visible",False)
    stable_picture=paired_source.get("same_visible_pixels_double_fetch",False)
    source_gate=bool(visible_pair and stable_picture and "LEFTFONT_STAGES" in byid and
       len(set(x["creator"] for x in ok))>=2)
    result={
      "schema":"vpd-r11-artist-authored-revision-stage-source-pixel-audit/1.0",
      "observed_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
      "source_manifest":"R11_SOURCE_SET_FROZEN.json",
      "downloaded_count":len(ok),"failed_count":len(fail),
      "actual_read_and_decoded":ok,"not_accessible":fail,
      "first_party_visual_stage_gate":source_gate,
      "actual_same_character_colored_before_after_detected":visible_pair,
      "selected_before_after_raster_stable_on_double_fetch":stable_picture,
      "copyrighted_image_bytes_distributed":False,
      "historical_author_editable_source_access":False,
      "artist_style_transfer_to_unseen_glyph_executed":False,
      "independent_visual_preference":False,
      "method_learned":False,
      "critical_limit":"Color difference or adjacent stages on promotional web image only establish visible revisions; no recoverable pen movement, Bezier edit history, or artist aesthetics scoring.",
      "next":"Annotate one original same-glyph revision by phase and purpose; freeze human-grounded conditional action and fail/rollback conditions before testing unrelated glyph families."
    }
    OUTPUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("R11_STAGE_SOURCE_GATE",json.dumps({
      "pass":source_gate,"read":len(ok),"failed":len(fail),
      "colored_same_glyph_pair":visible_pair,"pixel_reproducible":stable_picture},ensure_ascii=False))

if __name__=="__main__":run()
