#!/usr/bin/env python3
"""R12 source-only, no training: independently verify artist authored stage images.
Read all remote image bytes in ephemeral runner memory. Never commit source pixels.
"""
import datetime, hashlib, io, json, pathlib, time, urllib.request
from PIL import Image, ImageOps
ROOT=pathlib.Path(__file__).resolve().parent
SRC=json.loads((ROOT/"R12_FROZEN_ARTIST_AUTHORED_STAGE_SOURCES.json").read_text(encoding="utf-8"))
MAX_BYTES=12_000_000
RESULT=ROOT/"R12_AUTHENTIC_EXPRESSIVE_ARTIST_STAGE_BYTE_AUDIT.json"
AGENT="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
def download(url, referer):
    problems=[]
    for attempt in range(2):
        try:
            req=urllib.request.Request(url,headers={
               "User-Agent":AGENT,"Referer":referer,
               "Accept":"image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8"})
            with urllib.request.urlopen(req,timeout=22) as res:
                raw=res.read(MAX_BYTES+1)
                mime=res.headers.get("Content-Type","").split(";")[0]
            if len(raw)>MAX_BYTES:raise ValueError("FILE_OVER_12MB_CAP")
            img=Image.open(io.BytesIO(raw));img.load()
            if img.width<250 or img.height<150:raise ValueError("UNDERSIZE:"+str(img.size))
            if img.width*img.height>60_000_000:raise ValueError("OVER_PIXEL_CAP")
            return img,raw,mime
        except Exception as exc:
            problems.append(type(exc).__name__+":"+str(exc)[:240])
            if attempt==0:time.sleep(.65)
    raise RuntimeError(" | ".join(problems))
def footprint(img):
    rgb=ImageOps.exif_transpose(img.convert("RGB"))
    mini=rgb.copy();mini.thumbnail((160,160))
    total=max(1,mini.width*mini.height)
    pixels=list(mini.getdata())
    black=sum(max(p)<75 for p in pixels)/total
    white=sum(min(p)>236 for p in pixels)/total
    red=sum(p[0]>130 and p[0]>p[1]*1.4 and p[0]>p[2]*1.4 for p in pixels)/total
    # Not an image hash, only aggregate content clue; no source pixels in repo.
    return dict(dark_fraction=round(black,5),paper_fraction=round(white,5),red_fraction=round(red,5))
def read_case(which):
    rows=[];errors=[]
    manifest=SRC[which]
    for item in manifest["images"]:
        row={k:item[k] for k in ("id","url","phase")}
        try:
            image,raw,mime=download(item["url"],manifest["original_article"])
            row.update(readable=True,sha256=hashlib.sha256(raw).hexdigest(),byte_length=len(raw),
                       pixel_size=[image.width,image.height],decoded_format=image.format,mime=mime,
                       frame_count=getattr(image,"n_frames",1),
                       image_footprint=footprint(image),redistributed=False)
            print("R12_IMAGE_OK",row["id"],row["pixel_size"],row["byte_length"],row["sha256"])
            rows.append(row)
        except Exception as e:
            row.update(readable=False,error=str(e)[:600])
            print("R12_IMAGE_FAILED",row["id"],row["error"])
            errors.append(row)
    return rows,errors
def main():
    xa,xb=read_case("case1")
    ya,yb=read_case("case2")
    mandatory=["FAS_XIHE_02_EARLY","FAS_XIHE_03_DRAFT",
               "FAS_XIHE_05_ALTERNATIVES","FAS_XIHE_07_FINAL"]
    stage_ids={row["id"] for row in xa}
    same_work_stages=sum(x in stage_ids for x in mandatory)
    sha_unique=len({r["sha256"] for r in xa})
    stage_pass=same_work_stages>=3 and sha_unique>=3
    independent_secondary=bool(ya)
    gate=stage_pass and independent_secondary
    d={"schema":"r12-explicit-expressive-lettering-process-byte-audit/1.0",
       "utc_recorded_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),
       "source_manifest":"R12_FROZEN_ARTIST_AUTHORED_STAGE_SOURCES.json",
       "firsthand_main_work":"梁志坚/放肆喜欢",
       "main_author_stages_accessible":len(xa),
       "main_work_chronology_stage_names_from_author_text":mandatory,
       "mandatory_stages_seen":sorted(stage_ids.intersection(mandatory)),
       "verified_distinct_image_bytes":sha_unique,
       "second_independent_author":"张家佳/上座",
       "second_author_published_images_accessible":len(ya),
       "images_first_artist":xa,"images_second_artist":ya,
       "errors":xb+yb,"stage_byte_gate_pass":gate,
       "actual_per_image_stage_visual_interpretation":"NOT_CONFIRMED_BY_THIS_HASH_ONLY",
       "image_model_trained_on_these_pixels":False,
       "author_asset_bytes_committed_to_repo":False,
       "authorship_confidence":"Article published as author-written; cannot reconstruct unpublished intermediate documents or claim all choices exhaustive",
       "premium_unseen_lettering_success":False,
       "user_blind_review":"NOT_DONE",
       "next":"Independently inspect image stage contents and use author explanations to distinguish real contour/topology decisions; no raw source re-hosting."}
    RESULT.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("R12_REAL_SOURCE_GATE",json.dumps({"pass":gate,"main":len(xa),"required":same_work_stages,
                                          "second_artist":len(ya),"errors":len(xb)+len(yb)},ensure_ascii=False))
if __name__=="__main__":main()
