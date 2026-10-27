#!/usr/bin/env python3
"""Image provenance of three authored whole-brush-stroke sources, no image redistribution."""
import hashlib,io,json,pathlib,urllib.request,time,datetime
from PIL import Image
BASE=pathlib.Path(__file__).resolve().parent
MAN=json.loads((BASE/"R11_HANYI_ARTIST_WHOLE_STROKE_SOURCES_FROZEN.json").read_text(encoding="utf-8"))
OUT=BASE/"R11_HANYI_REAL_WHOLE_STROKE_SOURCE_AUDIT.json"
def probe(url):
  last=[]
  for i in range(2):
    try:
      req=urllib.request.Request(url,headers={
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122 Safari/537.36",
        "Accept":"image/webp,image/jpeg,image/avif,image/*,*/*;q=0.8","Referer":"https://dfaawards.viewingrooms.com/"})
      with urllib.request.urlopen(req,timeout=24) as f:
        data=f.read(8_000_001)
        mime=f.headers.get("Content-Type","")
      if len(data)>8_000_000:raise ValueError("EXCEEDS_8MB")
      im=Image.open(io.BytesIO(data));im.load()
      if im.width<580 or im.height<400:raise ValueError("INVALID_SMALL_IMAGE")
      return data,im,mime
    except Exception as e:
      last.append(type(e).__name__+":"+str(e)[:190]);time.sleep(1)
  raise RuntimeError("|".join(last))
results=[];fails=[]
for r in MAN["sources"]:
  item={"id":r["id"],"url":r["url"],"role":r["role"],
        "visual_content_summary_comes_from_official_published_figure":r["actual_observed_content"]}
  try:
     raw,im,mime=probe(r["url"])
     sha=hashlib.sha256(raw).hexdigest()
     if r.get("expected_sha256") and sha!=r["expected_sha256"]:
       raise ValueError("FROZEN_SHA_MISMATCH:"+sha)
     item.update({"read_and_decoded":True,"sha256":sha,"bytes":len(raw),
                  "width":im.width,"height":im.height,"actual_file_format":im.format,
                  "response_media_type":mime,"public_repo_includes_source_image_bytes":False})
     results.append(item)
     print("HANYI_SAME_AUTHOR_SOURCE_PASS",r["id"],sha,im.size)
  except Exception as e:
     item.update({"read_and_decoded":False,"error":str(e)[:650]});fails.append(item)
     print("HANYI_SAME_AUTHOR_SOURCE_FAIL",r["id"],str(e)[:270])
pass_gate=len(results)==3 and not fails
d={"schema":"vpd-r11-authored-entire-brush-gesture-source-audit/1.0",
   "recorded_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
   "artist":"行行珂, Hanyi Redcloud Li",
   "source_set_count":3,"successfully_verified_count":len(results),"verified":results,"failures":fails,
   "same_artist_claim_grounded_by_award_and_creator_portfolio":True,
   "source_stage_set_verification_pass":pass_gate,
   "source_raw_images_saved_to_public_repo":False,
   "creator_original_illustrator_or_hand_motion_files_available":False,
   "actual_creative_method_learned":False,
   "recommended_next_subproblem":"Study complete stroke roles and stylistic interaction from the two same-character artist stage panels, with strict cases where classification unknown; validate on genuinely unseen Chinese wordmark via human review only after learned visual method is implemented."}
OUT.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("R11_EXPRESSION_SOURCE_GATE",json.dumps({"pass":pass_gate,"verified_count":len(results),"fail":len(fails)}))
