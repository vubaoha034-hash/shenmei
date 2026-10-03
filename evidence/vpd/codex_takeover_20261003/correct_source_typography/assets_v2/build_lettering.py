"""Revise the existing single typography direction after independent V1 review."""
from pathlib import Path
import copy
import hashlib
import json
import sys
from xml.sax.saxutils import escape

sys.dont_write_bytecode = True
sys.path.append(r"C:/Users/Administrator/AppData/Local/hermes/hermes-agent/venv/Lib/site-packages")
import fontTools
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
PRIVATE = ROOT / ".liu-visual-private/correct_source_typography/lettering_v2"
V1 = OUT.parent / "assets_v1"
REVIEW = OUT.parent / "v1/pixel_review/REVIEWER_OUTPUT.json"
V1_POSTER = ROOT / ".liu-visual-private/correct_source_typography/v1/poster.png"
FONT = ROOT / "evidence/vpd/codex_takeover_20261003/skill_research/fonttools_bounded_probe_v1/upstream/adobe-fonts/source-han-serif/OTF/SimplifiedChinese/SourceHanSerifSC-Regular.otf"
LICENSE = FONT.parents[2] / "LICENSE.txt"
PHOTO = ROOT / ".liu-visual-private/source_recovery_20261003/photography-local-reconstruction-final.png"
REFERENCE = ROOT / ".liu-visual-private/reference.jpg"
PHOTO_SHA = "7fd7777fed21100cb6b47bc305701476054263565e73246ac469d065aa080618"
COLOR = "#F5F5EF"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

assert sha(PHOTO) == PHOTO_SHA
review = json.loads(REVIEW.read_text(encoding="utf-8"))
v1_construction = json.loads((V1 / "lettering_construction.json").read_text(encoding="utf-8"))

def M(x,y): return ("moveTo", ((x,y),))
def L(x,y): return ("lineTo", ((x,y),))
def C(x1,y1,x2,y2,x3,y3): return ("curveTo", ((x1,y1),(x2,y2),(x3,y3)))
def Z(): return ("closePath", ())

# The same authored V1 stroke identities are preserved, with deliberate geometry
# adjustments to shared width, spacing and terminal behavior. No font-logo tracing.
changes = {
    "cha-grass-crossbar": [M(76,178),C(320,166,640,181,894,165),C(921,164,934,174,938,190),C(929,209,908,217,870,217),C(640,211,326,220,84,229),Z()],
    "cha-roof-left": [M(507,315),C(481,378,436,436,376,489),C(286,574,185,639,74,683),C(67,685,59,681,57,671),C(170,605,266,537,340,455),C(405,383,446,322,469,278),C(492,283,526,296,548,305),C(535,311,522,314,507,315),Z()],
    "cha-roof-right": [M(516,311),C(604,418,738,514,916,565),C(935,571,947,589,943,604),C(920,616,901,632,887,653),C(731,602,606,488,493,332),Z()],
    "cha-lower-crossbar": [M(235,683),C(390,675,592,676,721,665),C(748,662,770,675,782,696),C(766,714,744,719,710,717),C(559,716,398,722,239,722),Z()],
    "cha-left-dot": [M(331,763),C(351,771,379,790,397,807),C(336,866,253,918,166,944),C(155,948,148,935,154,922),C(232,870,287,812,331,763),Z()],
    "cha-right-dot": [M(631,765),C(727,792,804,839,849,898),C(868,924,853,946,821,952),C(775,878,711,821,625,791),C(620,786,621,774,631,765),Z()],
    "zuo-person-falling": [M(286,52),C(265,221,209,400,103,551),L(71,570),C(63,567,58,557,54,547),C(146,393,197,232,202,42),C(234,42,266,45,286,52),Z()],
    "zuo-person-upright": [M(186,393),C(224,387,248,395,266,412),C(253,575,250,778,253,928),C(232,946,207,955,171,956),C(182,756,181,571,186,393),Z()],
    "zuo-zha-falling": [M(487,53),C(515,54,543,64,566,88),C(550,257,476,429,367,548),C(352,549,345,544,341,535),C(428,385,471,211,487,53),Z()],
    "zuo-zha-upper-bar": [M(448,262),C(608,257,754,261,884,246),C(918,242,942,254,952,276),C(944,298,927,308,882,310),C(710,304,574,309,428,310),L(434,284),Z()],
    "zuo-zha-upright": [M(574,285),C(606,285,638,295,666,308),C(651,502,648,737,653,918),C(638,943,607,955,558,958),C(568,718,569,479,574,285),Z()],
    "zuo-zha-middle-bar": [M(620,524),C(707,516,795,514,852,506),C(887,499,909,511,920,535),C(912,557,887,570,850,569),C(763,564,686,571,613,573),Z()],
    "zuo-zha-lower-bar": [M(614,753),C(713,745,802,743,887,734),C(917,730,938,741,949,765),C(940,786,914,799,873,798),C(773,792,684,796,607,800),Z()],
}
strokes = copy.deepcopy(v1_construction["editable_strokes"])
for stroke in strokes:
    if stroke["id"] in changes:
        stroke["commands"] = changes[stroke["id"]]
    if stroke["character"] == "\u4f5c":
        stroke["offset_x"] = 1015

def replay(commands, pen):
    for operation, points in commands:
        getattr(pen, operation)(*points)

def union(boxes):
    return [min(x[0] for x in boxes),min(x[1] for x in boxes),max(x[2] for x in boxes),max(x[3] for x in boxes)]

logo_paths, logo_bounds = [], []
for stroke in strokes:
    pen = SVGPathPen(None)
    replay(stroke["commands"], pen)
    stroke["svg_path_d"] = pen.getCommands()
    offset = stroke.get("offset_x", 0)
    bounds = BoundsPen(None)
    replay(stroke["commands"], TransformPen(bounds, (1,0,0,1,offset,0)))
    stroke["exact_bounds_logo_units"] = bounds.bounds
    logo_bounds.append(bounds.bounds)
    logo_paths.append(f'<path id="{stroke["id"]}" data-character="{stroke["character"]}" transform="translate({offset} 0)" d="{stroke["svg_path_d"]}"/>')
assert len(strokes) == 16
logo_frame = [40,30,1940,950]
logo_placement = {"x":92,"y":77,"width":224,"height":224*950/1940}
logo_scale = logo_placement["width"]/logo_frame[2]
logo_ink_units = union(logo_bounds)
logo_ink = [92+(logo_ink_units[0]-40)*logo_scale,77+(logo_ink_units[1]-30)*logo_scale,92+(logo_ink_units[2]-40)*logo_scale,77+(logo_ink_units[3]-30)*logo_scale]
logo_group = f'<g id="custom-chazuo-v2" fill="{COLOR}">'+''.join(logo_paths)+'</g>'
logo_svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="224" height="{logo_placement["height"]:.6f}" viewBox="40 30 1940 950"><title>茶作 — revised original closed Bézier lettering</title><desc>Same 16 authored strokes. Wider 作 main strokes, closer character interval, shared soft lifted horizontal terminals. No source-font contours are imported into the brand.</desc>{logo_group}</svg>'

font = TTFont(FONT)
glyphset = font.getGlyphSet()
cmap = font.getBestCmap()
text = "\u4e00\u676f\u8336\uff0c\u6162\u4e0b\u6765"
title_positions = [
    {"character":"\u4e00","x":1090,"baseline_y":299,"font_size":76,"line":1},
    {"character":"\u676f","x":1171,"baseline_y":299,"font_size":76,"line":1},
    {"character":"\u8336","x":1252,"baseline_y":299,"font_size":76,"line":1},
    {"character":"\uff0c","x":1333,"baseline_y":299,"font_size":76,"line":1},
    {"character":"\u6162","x":1045,"baseline_y":412,"font_size":98,"line":2},
    {"character":"\u4e0b","x":1150,"baseline_y":412,"font_size":98,"line":2},
    {"character":"\u6765","x":1255,"baseline_y":412,"font_size":98,"line":2},
]
title_frame = {"x":1040,"y":229,"width":320,"height":198}
source_records, title_paths, title_boxes = [], [], []
stroke_width_font_units = 11
for index, position in enumerate(title_positions):
    ch = position["character"]
    name = cmap[ord(ch)]
    svg = SVGPathPen(glyphset)
    bounds = BoundsPen(glyphset)
    record = RecordingPen()
    for pen in (svg,bounds,record):
        glyphset[name].draw(pen)
    x0,y0,x1,y1 = bounds.bounds
    scale = position["font_size"]/1000
    half_stroke = scale*stroke_width_font_units/2
    ink = [position["x"]+x0*scale-half_stroke,position["baseline_y"]-y1*scale-half_stroke,position["x"]+x1*scale+half_stroke,position["baseline_y"]-y0*scale+half_stroke]
    position["source_glyph_name"] = name
    position["ink_bounds_including_round_stroke_poster_px"] = ink
    title_boxes.append(ink)
    source_records.append({"character":ch,"codepoint":f"U+{ord(ch):04X}","glyph_name":name,"source_bounds_font_units":bounds.bounds,"source_svg_path_d":svg.getCommands(),"source_recording_commands":record.value})
    title_paths.append(f'<path id="headline-v2-{index+1}" data-character="{ch}" data-codepoint="U+{ord(ch):04X}" data-source-glyph="{name}" transform="translate({position["x"]} {position["baseline_y"]}) scale({scale} {-scale})" d="{svg.getCommands()}"/>')
title_group = f'<g id="licensed-headline-v2" fill="{COLOR}" stroke="{COLOR}" stroke-width="11" stroke-linejoin="round" paint-order="stroke fill">'+''.join(title_paths)+'</g>'
title_svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="320" height="198" viewBox="1040 229 320 198"><title>{text}</title><desc>Source Han Serif SC Regular 2.003, OFL 1.1. Exact source contours with an explicit 11-font-unit round outline reinforcement, resulting in 0.836 px / 1.078 px stroke widths. First line 76 px, 5 px tracking; second 98 px, 7 px tracking; baseline separation 113 px. Text is precise and all paths are editable.</desc>{title_group}</svg>'
overlay_logo = f'<g transform="translate(92 77) scale({logo_scale:.12f}) translate(-40 -30)">{logo_group}</g>'
overlay_svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="1536" height="1024" viewBox="0 0 1536 1024"><title>茶作 — 一杯茶，慢下来 — V2 transparent typography</title><desc>Same typography direction revised after independent V1 comments. Photography is not embedded or altered. All text remains within the fixed left and right protection regions.</desc>{overlay_logo}{title_group}</svg>'
live_elements = [f'<text x="{p["x"]}" y="{p["baseline_y"]}" font-size="{p["font_size"]}" stroke-width="{p["font_size"]*.011}">{p["character"]}</text>' for p in title_positions]
live_svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="320" height="198" viewBox="1040 229 320 198"><title>{text}</title><desc>Unicode editing source; requires Source Han Serif SC Regular 2.003. headline.svg is the deterministic outlined production asset.</desc><g fill="{COLOR}" stroke="{COLOR}" stroke-linejoin="round" paint-order="stroke fill" font-family="Source Han Serif SC" font-weight="400">'+''.join(live_elements)+'</g></svg>'

OUT.mkdir(parents=True,exist_ok=True)
PRIVATE.mkdir(parents=True,exist_ok=True)
files = {"chazuo-wordmark.svg":logo_svg,"headline.svg":title_svg,"headline-live-text.svg":live_svg,"typography-overlay.svg":overlay_svg}
for filename,contents in files.items():
    (OUT/filename).write_text(contents+"\n",encoding="utf-8")
    (PRIVATE/filename).write_text(contents+"\n",encoding="utf-8")
(OUT/"SOURCE_HAN_SERIF_OFL.txt").write_bytes(LICENSE.read_bytes())

construction = {"brand":"茶作","source_version":"assets_v1/lettering_construction.json","coordinate_system":"y down; original drawing cells; 作 offset now x=1015","authoring":"Original V1 closed Bézier paths revised, 16 independently editable strokes retained; zero source-font logo contours","editable_strokes":strokes,"logo_ink_bounds_units":logo_ink_units,"logo_ink_bounds_poster_px":logo_ink}
(OUT/"lettering_construction.json").write_text(json.dumps(construction,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
font_record = {"path":str(FONT.relative_to(ROOT)).replace("\\","/"),"sha256":sha(FONT),"family":font["name"].getDebugName(1),"version":font["name"].getDebugName(5),"units_per_em":font["head"].unitsPerEm,"license":"SIL Open Font License 1.1","license_sha256":sha(LICENSE)}
source_geometry = {"font":font_record,"fonttools_version":fontTools.__version__,"headline_source_glyphs":source_records,"explicit_document_style":{"stroke_width_font_units":11,"line_join":"round","rendered_stroke_width_px":{"line_1":.836,"line_2":1.078}},"note":"Font software is unmodified. Round stroke reinforcement is explicit in the SVG document and preserves the exact source outlines."}
(OUT/"source_geometry.json").write_text(json.dumps(source_geometry,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

layout = {"canvas":{"width":1536,"height":1024,"aspect_ratio":"3:2"},"brand":{"text":"茶作","frame_poster_px":logo_placement,"ink_bounds_poster_px":logo_ink},"headline":{"text":text,"line_breaks":["一杯茶，","慢下来"],"frame_poster_px":title_frame,"ink_bounds_poster_px":union(title_boxes),"glyph_placements":title_positions,"nominal_font_sizes_px":[76,98],"tracking_px":[5,7],"baseline_separation_px":113,"visible_interline_gap_approx_px":union(title_boxes[4:])[1]-union(title_boxes[:4])[3]},"type_color":COLOR,"fixed_protection_rectangles":[[64,56,504,304],[800,72,1504,440]],"composition_instruction":"Overlay typography-overlay.svg/PNG at x=0,y=0,1536x1024 on the exact frozen photograph. Typography remains in both established rectangles; do not modify or rescale photography."}
(OUT/"typography-layout.json").write_text(json.dumps(layout,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

delta = {"scope":"One main revision: common typography stroke and spacing rhythm within the same visual direction","independent_review_source":{"path":str(REVIEW.relative_to(ROOT)).replace("\\","/"),"sha256":sha(REVIEW),"source_verdict":review["verdict"]},"basis":[{"review_issue":"茶/作 weight, width and terminals not unified","changes":"作 falling strokes and verticals widened; shared gently lifted round horizontal terminals; 茶 sharp right roof corner replaced with a continuous rounded terminal; existing 茶/作 identities and structures retained","specific_geometry":"13 of 16 existing stroke shapes locally revised; all 16 closed paths remain. 作 x offset 1100 -> 1015; physical character gap decreases rather than adding a new shape."},{"review_issue":"Brand and headline share too little stroke rhythm","changes":"Brand horizontals share continuous soft terminals; licensed headline outline is reinforced by 11 font units with round joins, reducing the frailty of thin horizontals; first/second size ratio 68:104 -> 76:98","specific_geometry":"Final visible stroke style is fill + explicit same-color SVG stroke. Font data is not edited and all Unicode characters remain exact."},{"review_issue":"Headline stands too high and lines are too far apart","changes":"Title baseline y 190/329 -> 299/412; first/second tracking 7/12 -> 5/7; baseline separation 139 -> 113; visible interline space approx 41 -> 15 px","specific_geometry":"Headline is approximately x1048..1351, y235..421, with its lower edge closer to the stream and tea-tray reading line; fixed right region still ends at440."}],"retained":["Exact frozen photograph 7fd7777…","Brand 茶作 and core copy 一杯茶，慢下来","Same upper-left brand / upper-right two-line wording","Same type color #F5F5EF","Same original 16 stroke identities and licensed Source Han Serif headline","Existing fixed protection rectangles"],"review_boundary":"This records revision intent and actual geometry, not self scoring or design acceptance."}
(OUT/"revision_basis.json").write_text(json.dumps(delta,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

provenance = {"asset_direction":"Same typography direction, V2 local revision","maker_role":"Asset production only; no business-state edits or self scoring","actual_pixels_seen_for_revision":{"v1_poster":{"path":str(V1_POSTER.relative_to(ROOT)).replace("\\","/"),"sha256":sha(V1_POSTER),"view":"view_image original detail"},"frozen_photography":{"path":str(PHOTO.relative_to(ROOT)).replace("\\","/"),"sha256":sha(PHOTO),"view":"view_image original detail"},"reference":{"path":str(REFERENCE.relative_to(ROOT)).replace("\\","/"),"sha256":sha(REFERENCE),"view":"view_image original detail; mechanism interpreted only from the upper horizontal advertisement"}},"independent_v1_review":{"path":str(REVIEW.relative_to(ROOT)).replace("\\","/"),"sha256":sha(REVIEW)},"logo":{"text":"茶作","original_editable_paths":16,"source_font_contours_imported":0,"construction_file":"lettering_construction.json","relationship_to_v1":"Same original stroke identities, 13 locally redrawn, 作 offset changed to1015"},"headline":{"text":text,"source_font":font_record,"glyphs":"Exact source geometry freshly read through TTFont, RecordingPen, BoundsPen and SVGPathPen","document_reinforcement":"11 font unit same-color stroke, round joins; visible stroke widths .836/1.078 px","layout":"76/98 px, 5/7 px tracking, baselines299/412, visible line gap approximately15px","unicode_source":"headline-live-text.svg"},"execution":{"python":sys.executable,"fonttools_version":fontTools.__version__,"fonttools_runtime":fontTools.__file__,"mature_methods":["TTFont.getBestCmap","TTFont.getGlyphSet","RecordingPen","BoundsPen","SVGPathPen","TransformPen"],"raster_and_composition":"render_assets.cjs, bundled sharp, raw RGB blending","image_generation_calls":0,"figma_calls":0,"business_state_writes":0},"license":"Exact Adobe Source Han Serif OFL 1.1 license preserved in SOURCE_HAN_SERIF_OFL.txt. Font software unchanged; font outlines are used in this graphic document.","limitations":["This production does not establish independent aesthetic acceptance or human acceptance.","Live text needs the exact font; outlined assets render independently of font installation.","Raw pixel-protection and Unicode checks establish engineering facts only."],"asset_sha256":{name:sha(OUT/name) for name in files},"construction_sha256":sha(OUT/"lettering_construction.json"),"source_geometry_sha256":sha(OUT/"source_geometry.json"),"revision_basis_sha256":sha(OUT/"revision_basis.json")}
(OUT/"provenance.json").write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
(PRIVATE/"provenance.json").write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"logo_frame":logo_placement,"logo_ink":logo_ink,"headline_frame":title_frame,"headline_ink":union(title_boxes),"line_gap":layout["headline"]["visible_interline_gap_approx_px"],"strokes":len(strokes),"fonttools":fontTools.__version__},ensure_ascii=True,indent=2))
