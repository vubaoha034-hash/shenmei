#!/usr/bin/env python3
"""Structural path-ID mapping for a frozen Chinese glyph.
Does NOT validate normative handwriting, visual glyph identity, or beauty.
Usage: python HANZI_SEMANTIC_GATE_V1.py mapping.json source.svg --arm A
"""
import argparse, json, xml.etree.ElementTree as ET, sys
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument("mapping")
p.add_argument("svg")
p.add_argument("--arm",choices=("A","B"),required=True)
a=p.parse_args()
metadata=json.loads(Path(a.mapping).read_text(encoding="utf8"))
rows=metadata["canonical_mapping"]
source=metadata["source"]
if len(rows)!=source["canonical_stroke_count"] or [r["stroke_index"] for r in rows]!=list(range(1,len(rows)+1)):
    raise SystemExit("INVALID_OFFICIAL_STROKE_INDEX_DATA")
if "喜" != source["char"]:
    raise SystemExit("WRONG_GLYPH_REFERENCE")
actual={}
for n in ET.parse(a.svg).getroot().iter():
    if n.tag.rsplit("}",1)[-1]=="path" and n.attrib.get("id"):
        i=n.attrib["id"]
        if i in actual:raise SystemExit("DUPLICATE_PATH_ID_"+i)
        actual[i]=n.attrib.get("d","")
key=a.arm+"_art_paths"
expected=set()
missing_strokes=[]
for r in rows:
    names=r[key]
    if not names:missing_strokes.append(r["stroke_index"])
    expected.update(names)
unknown=sorted(set(actual)-expected)
missing=sorted(expected-set(actual))
if unknown or missing or missing_strokes:
    print(json.dumps({"status":"BLOCKED_SEMANTIC_MAPPING","unknown_svg_contours":unknown,"missing_contours":missing,"unmapped_normative_strokes":missing_strokes},ensure_ascii=False,indent=2))
    sys.exit(2)
print(json.dumps({
"status":"SEMANTIC_PATH_IDS_MATCH_REFERENCE_ONLY",
"char":source["char"],"canonical_strokes":source["canonical_stroke_count"],
"SVG_contours":len(actual),
"certifies_normative_visual_correctness":False,
"requires_real_Chinese_readability_review":True,
"user_review_from_repository":metadata["interpretation"]["user_judgment"],
"method_validated":False},ensure_ascii=False,indent=2))
