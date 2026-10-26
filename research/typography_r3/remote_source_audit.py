#!/usr/bin/env python3
"""Bounded same-designer R3 source audit on a GitHub public standard runner.

Verifies original uploaded 2025 SVG bytes against official Commons imageinfo
(SHA-1 + length), then measures STATIC ink morphology only. Source bytes remain
temporary in memory; only derived metrics and failure records are written.

This does NOT prove original author process, pen pressure, style transfer,
copyright clearance, or human design quality.
"""
import hashlib
import io
import json
import re
import tempfile
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

SOURCES = [
    {
        "id": "R1908_A",
        "title": "實業之日本",
        "year": 1908,
        "wiki_url": "https://commons.wikimedia.org/wiki/File:%E5%AF%A6%E6%A5%AD%E4%B9%8B%E6%97%A5%E6%9C%AC_(Calligraphy_by_Rosanjin).svg",
        "original_url": "https://upload.wikimedia.org/wikipedia/commons/9/9c/%E5%AF%A6%E6%A5%AD%E4%B9%8B%E6%97%A5%E6%9C%AC_%28Calligraphy_by_Rosanjin%29.svg",
        "expected_sha1": "4af1251c7f8c9861722c41ff893daf7dc566677a",
        "expected_size": 21305,
    },
    {
        "id": "R1909_B",
        "title": "婦人世界",
        "year": 1909,
        "wiki_url": "https://commons.wikimedia.org/wiki/File:%E5%A9%A6%E4%BA%BA%E4%B8%96%E7%95%8C_(Calligraphy_by_Rosanjin).svg",
        "original_url": "https://upload.wikimedia.org/wikipedia/commons/2/27/%E5%A9%A6%E4%BA%BA%E4%B8%96%E7%95%8C_%28Calligraphy_by_Rosanjin%29.svg",
        "expected_sha1": "48bc9dd60add5f2eb4a5feee75e82d72a49aa44c",
        "expected_size": 7101,
    },
    {
        "id": "R1909_C",
        "title": "小學男生",
        "year": 1909,
        "wiki_url": "https://commons.wikimedia.org/wiki/File:%E5%B0%8F%E5%AD%B8%E7%94%B7%E7%94%9F_(Calligraphy_by_Rosanjin).svg",
        "original_url": "https://upload.wikimedia.org/wikipedia/commons/6/62/%E5%B0%8F%E5%AD%B8%E7%94%B7%E7%94%9F_%28Calligraphy_by_Rosanjin%29.svg",
        "expected_sha1": "6d5e5aa23bf61e235d6dd1aa9b70e935c256ce16",
        "expected_size": 16597,
    },
]

def acquire(item):
    request = urllib.request.Request(
        item["original_url"],
        headers={"User-Agent": "shenmei-lettering-research/0.1 (public archival source verification; github.com/vubaoha034-hash/shenmei)", "Accept": "image/svg+xml,*/*;q=0.8"},
        method="GET",
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        raw = response.read(200_000)
    return raw

def verify_svg(raw, item):
    sha1=hashlib.sha1(raw).hexdigest()
    sha256=hashlib.sha256(raw).hexdigest()
    if len(raw) != item["expected_size"] or sha1 != item["expected_sha1"]:
        raise ValueError("OFFICIAL_IMAGEINFO_BYTE_OR_SHA1_MISMATCH")
    if b"<svg" not in raw[:8000]:
        raise ValueError("NOT_SVG_ROOT")
    if re.search(rb"<!ENTITY|<script|<foreignObject|<image\b", raw, re.I):
        raise ValueError("UNSAFE_OR_NON_VECTOR_SVG")
    root = ET.fromstring(raw)
    if root.tag.rsplit("}",1)[-1] != "svg":
        raise ValueError("SVG_XML_ROOT_INVALID")
    for node in root.iter():
        for key,val in node.attrib.items():
            if key.rsplit("}",1)[-1] in {"href","src"} and str(val).startswith(("https:","http:","file:","//")):
                raise ValueError("EXTERNAL_SVG_REFERENCE_BLOCKED")
    return sha1,sha256,root

def measure_svg(raw,root):
    import numpy as np
    import cairosvg
    from PIL import Image
    from scipy.ndimage import distance_transform_edt, label
    from skimage.morphology import skeletonize, convex_hull_image
    from skimage.measure import perimeter
    png=cairosvg.svg2png(bytestring=raw,unsafe=False,output_width=None,output_height=None)
    image=Image.open(io.BytesIO(png)).convert("RGBA")
    image.thumbnail((1250,1250))
    bg=Image.new("RGBA",image.size,(255,255,255,255))
    bg.alpha_composite(image)
    rgb=np.asarray(bg.convert("RGB"),dtype=np.uint8)
    gray=np.dot(rgb.astype(np.float32),[.299,.587,.114])
    # Conservative dark-on-white threshold: count visible dark ink only.
    ink=(gray<180)
    if not np.any(ink):
        raise ValueError("NO_INK_OVER_WHITE")
    yy,xx=np.nonzero(ink)
    x0,x1=int(xx.min()),int(xx.max()+1)
    y0,y1=int(yy.min()),int(yy.max()+1)
    roi=ink[y0:y1,x0:x1]
    if roi.shape[0]<10 or roi.shape[1]<10:
        raise ValueError("TOO_SMALL_TO_MEASURE")
    skeleton=skeletonize(roi)
    widths=2*distance_transform_edt(roi)[skeleton]
    widths=widths[np.isfinite(widths)&(widths>0)]
    q=np.percentile(widths,[10,50,90])
    perim=float(perimeter(roi,neighborhood=8))
    hull=convex_hull_image(roi)
    hull_perim=float(perimeter(hull,neighborhood=8))
    labeled,count=label(roi)
    vals=np.bincount(labeled.ravel())[1:]
    weights=sorted([int(x) for x in vals if x>=3],reverse=True)
    counts=np.asarray(roi,dtype=np.float32)
    column=counts.mean(axis=0)
    blank=column<.015
    # Contiguous blank corridors as a spacing proxy, NOT character boundaries.
    a=np.diff(np.r_[0,blank.astype(int),0])
    corridors=[(int(x),int(y)) for x,y in zip(np.where(a==1)[0],np.where(a==-1)[0])
               if (y-x)/roi.shape[1] >=.02]
    tags=[node.tag.rsplit('}',1)[-1] for node in root.iter()]
    return {
      "raster_resolution":[int(image.width),int(image.height)],
      "ink_bbox_px":[x0,y0,int(roi.shape[1]),int(roi.shape[0])],
      "ink_fraction_inside_bbox":round(float(roi.mean()),6),
      "ink_centroid_norm_xy":[round(float(xx.mean()/max(1,(x1-x0))-x0/max(1,(x1-x0))),5),round(float(yy.mean()/max(1,(y1-y0))-y0/max(1,(y1-y0))),5)],
      "stroke_width_ratio_to_bbox_h_p10_p50_p90":[round(float(v/roi.shape[0]),5) for v in q],
      "stroke_width_px_p10_p50_p90":[round(float(v),3) for v in q],
      "stroke_width_tail_ratio_p90_over_p10":round(float(q[2]/max(q[0],.01)),4),
      "ink_connected_regions_ge3px":len(weights),
      "largest_ink_region_frac_of_bbox":[round(v/float(roi.size),5) for v in weights[:5]],
      "ink_perimeter_over_hull_perimeter":round(perim/max(1,hull_perim),4),
      "blank_column_corridors_pct":[[round(a/roi.shape[1],4),round(b/roi.shape[1],4)] for a,b in corridors],
      "svg_fragment_path_count":tags.count("path"),
      "svg_element_count":len(tags),
      "caution":"2025 digitizer vectorization, not the artist's brush strokes, motion, tool or intention."
    }

def main():
    result={
      "schema_version":"r3-remote-exact-source-audit/1.0",
      "date":"2026-10-26",
      "scope":"PUBLIC_PROJECT_READONLY_SOURCE_ANALYSIS; DERIVED_METRICS_ONLY",
      "source_bytes_published":False,
      "source_license_clear_for_commercial_use":False,
      "learned_designer_method_validated":False,
      "artistic_quality_validated":False,
      "verified_sources":0,"intended_sources":len(SOURCES),
      "source_status":[],
      "style_family_repeat_mechanism_proven":False,
    }
    for item in SOURCES:
        status={"id":item["id"],"title":item["title"],"creator":"Kitaoji Rosanjin (author attribution per Commons)",
          "year":item["year"],"source_page":item["wiki_url"],"source_svg_sha1_expected":item["expected_sha1"],
          "expected_bytes":item["expected_size"],"retrieved":False}
        try:
            raw=acquire(item)
            sha1,sha256,root=verify_svg(raw,item)
            status["retrieved"]=True
            status["sha1_verified"]=sha1
            status["sha256_verified"]=sha256
            status["bytes"]=len(raw)
            status["morphology"]=measure_svg(raw,root)
            status["status"]="SOURCE_VERIFIED_STATIC_IMAGE_MEASURED"
            result["verified_sources"]+=1
        except Exception as exc:
            status["status"]="BLOCKED_OR_INVALID"
            status["error"]=str(exc)[:280]
        result["source_status"].append(status)
    if result["verified_sources"]==len(SOURCES):
        result["static_family_measurement_complete"]=True
        result["still_needed"]=["Independent visual examination of three original artworks",
          "prove that repeated characteristics are not dependent on character content",
          "derive falsifiable creative operations, not descriptive surface averages",
          "same-input equal-budget unseen character blind study with human aesthetic review"]
    else:
        result["static_family_measurement_complete"]=False
        result["still_needed"]=["Resolve source-byte acquisition for failed entries before family analysis"]
    out=Path("research/typography_r3/ROSANJIN_REMOTE_SOURCE_RECEIPT.json")
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("R3_RECEIPT_START")
    print(json.dumps({"verified_sources":result["verified_sources"],
      "source_status":[{"id":x["id"],"status":x["status"],"error":x.get("error")} for x in result["source_status"]],
      "static_family_measurement_complete":result["static_family_measurement_complete"]},ensure_ascii=False))
    print("R3_RECEIPT_END")

if __name__=="__main__":
    main()
