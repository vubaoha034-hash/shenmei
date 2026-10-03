"""One authored lettering direction; outputs paths and layout, no project state edits."""
from pathlib import Path
import hashlib
import json
import math
import sys
from xml.sax.saxutils import escape

sys.dont_write_bytecode = True
sys.path.append(r"C:/Users/Administrator/AppData/Local/hermes/hermes-agent/venv/Lib/site-packages")
import fontTools
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
PRIVATE = ROOT / ".liu-visual-private/correct_source_typography/lettering_v1"
SOURCE = json.loads((OUT / "source_geometry.json").read_text(encoding="utf-8"))
SOURCE_GLYPHS = {x["character"]: x for x in SOURCE["glyphs"]}
COLOR = "#F5F5EF"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def M(x,y): return ("moveTo", ((x,y),))
def L(x,y): return ("lineTo", ((x,y),))
def C(x1,y1,x2,y2,x3,y3): return ("curveTo", ((x1,y1),(x2,y2),(x3,y3)))
def Z(): return ("closePath", ())

# These are newly authored closed outlines in y-down drawing coordinates.
# They are not an outline, warp, trace, or damaged copy of Source Han Serif.
# The source font above serves only as a correct structural reference for the brand.
STROKES = [
    {"id":"cha-grass-crossbar", "character":"\u8336", "component":"\u8279", "role":"One slightly cupped horizontal, lifted right end", "commands":[M(70,188),C(320,171,640,185,900,167),L(938,192),C(743,224,336,213,84,226),Z()]},
    {"id":"cha-grass-left", "character":"\u8336", "component":"\u8279", "role":"Short upright; cut top, soft lower taper", "commands":[M(290,58),C(310,59,335,62,354,72),L(344,252),C(342,273,319,288,279,291),C(286,208,289,128,290,58),Z()]},
    {"id":"cha-grass-right", "character":"\u8336", "component":"\u8279", "role":"Splayed second upright with open inner space", "commands":[M(680,40),C(705,39,731,44,751,55),C(744,148,735,238,722,282),C(708,301,683,307,659,305),C(671,216,678,126,680,40),Z()]},
    {"id":"cha-roof-left", "character":"\u8336", "component":"\u4eba", "role":"Long tapering descent keeps the person component intact", "commands":[M(507,315),C(481,378,436,436,376,489),C(286,574,185,639,70,683),L(60,664),C(170,605,266,537,340,455),C(405,383,446,322,469,278),C(492,283,526,296,548,305),C(535,311,522,314,507,315),Z()]},
    {"id":"cha-roof-right", "character":"\u8336", "component":"\u4eba", "role":"Weight opens to the right, ending in a small controlled lift", "commands":[M(516,311),C(604,418,738,514,930,561),L(954,595),C(916,617,892,642,883,668),C(731,602,606,488,493,332),Z()]},
    {"id":"cha-lower-crossbar", "character":"\u8336", "component":"lower tea element", "role":"Shared shallow arc with the grass bar and the horizontal strokes of zuo", "commands":[M(235,683),C(390,677,588,677,745,665),L(782,697),C(755,717,667,713,556,717),L(238,722),Z()]},
    {"id":"cha-stem-hook", "character":"\u8336", "component":"lower tea element", "role":"Central stem remains a hooked stroke, not a detached leaf icon", "commands":[M(484,535),C(508,536,539,539,561,548),C(549,653,548,772,545,868),C(543,927,506,958,426,963),L(401,918),C(470,922,487,918,488,878),C(489,760,485,651,484,535),Z()]},
    {"id":"cha-left-dot", "character":"\u8336", "component":"lower tea element", "role":"Left sweep tapers outward; kept as the actual lower stroke", "commands":[M(331,763),C(351,771,379,790,397,807),C(336,866,253,918,164,944),L(154,922),C(232,870,287,812,331,763),Z()]},
    {"id":"cha-right-dot", "character":"\u8336", "component":"lower tea element", "role":"Right dot is a continuous closed stroke with a soft end", "commands":[M(633,767),C(727,792,804,839,849,898),C(868,924,853,946,821,952),C(775,878,711,821,622,790),Z()]},
    {"id":"zuo-person-falling", "character":"\u4f5c", "component":"\u4ebb", "offset_x":1100, "role":"Long left falling stroke, normal person radical", "commands":[M(260,45),C(232,197,161,365,59,533),L(40,516),C(121,390,177,226,200,41),Z()]},
    {"id":"zuo-person-upright", "character":"\u4f5c", "component":"\u4ebb", "offset_x":1100, "role":"Slightly tapered upright shares the lower terminal with cha", "commands":[M(187,390),C(206,389,230,394,253,408),C(245,551,244,733,247,928),C(234,949,211,957,174,958),C(181,755,182,562,187,390),Z()]},
    {"id":"zuo-zha-falling", "character":"\u4f5c", "component":"\u4e4d", "offset_x":1100, "role":"The top-left falling stroke of zha remains structurally explicit", "commands":[M(473,53),C(496,55,518,63,538,74),C(501,245,425,416,319,532),L(297,519),C(395,374,453,206,473,53),Z()]},
    {"id":"zuo-zha-upper-bar", "character":"\u4f5c", "component":"\u4e4d", "offset_x":1100, "role":"Shallow cupped horizontal shares the tea-rim behavior", "commands":[M(441,266),C(573,257,751,258,906,244),L(949,274),C(941,299,921,308,882,312),C(739,309,575,305,431,307),Z()]},
    {"id":"zuo-zha-upright", "character":"\u4f5c", "component":"\u4e4d", "offset_x":1100, "role":"Long continuous upright anchors all three right horizontals", "commands":[M(576,287),C(599,288,625,294,651,303),C(635,452,634,730,638,922),C(619,945,593,955,557,958),C(566,714,570,476,576,287),Z()]},
    {"id":"zuo-zha-middle-bar", "character":"\u4f5c", "component":"\u4e4d", "offset_x":1100, "role":"The middle bar is shorter and shares the lifted endpoint", "commands":[M(601,527),C(691,519,791,519,862,509),L(913,536),C(904,558,887,568,852,570),C(767,567,676,568,598,568),Z()]},
    {"id":"zuo-zha-lower-bar", "character":"\u4f5c", "component":"\u4e4d", "offset_x":1100, "role":"Lower bar opens further to balance the bottom of cha", "commands":[M(594,756),C(699,748,800,744,897,733),L(942,763),C(934,787,910,797,871,798),C(775,793,681,795,591,796),Z()]},
]

def replay(commands, pen):
    for op, pts in commands:
        getattr(pen, op)(*pts)

def bbox_union(boxes):
    return [min(x[0] for x in boxes), min(x[1] for x in boxes), max(x[2] for x in boxes), max(x[3] for x in boxes)]

logo_elements = []
logo_boxes = []
for stroke in STROKES:
    offset = stroke.get("offset_x", 0)
    svgp = SVGPathPen(None)
    replay(stroke["commands"], svgp)
    bound = BoundsPen(None)
    replay(stroke["commands"], TransformPen(bound, (1,0,0,1,offset,0)))
    stroke["svg_path_d"] = svgp.getCommands()
    stroke["exact_bounds_logo_units"] = bound.bounds
    logo_boxes.append(bound.bounds)
    logo_elements.append(f'<path id="{stroke["id"]}" data-character="{stroke["character"]}" data-component="{escape(stroke["component"])}" transform="translate({offset} 0)" d="{stroke["svg_path_d"]}"/>')

logo_frame = [40,30,2030,950]
logo_on_poster = {"x":92,"y":77,"width":224,"height":224*950/2030}
logo_scale = logo_on_poster["width"]/logo_frame[2]
logo_ink = bbox_union(logo_boxes)
logo_ink_poster = [
    logo_on_poster["x"]+(logo_ink[0]-logo_frame[0])*logo_scale,
    logo_on_poster["y"]+(logo_ink[1]-logo_frame[1])*logo_scale,
    logo_on_poster["x"]+(logo_ink[2]-logo_frame[0])*logo_scale,
    logo_on_poster["y"]+(logo_ink[3]-logo_frame[1])*logo_scale,
]
logo_group = '<g id="custom-chazuo" fill="'+COLOR+'">'+''.join(logo_elements)+'</g>'
logo_svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="224" height="{logo_on_poster["height"]:.6f}" viewBox="40 30 2030 950"><title>茶作 — original closed Bézier stroke lettering</title><desc>Every visible brand stroke is an individually editable original path. Shallow cupped horizontals and tapered continuous terminals derive from the tea bowl and the flowing scene. No added leaf, source-font trace, or random damage.</desc>{logo_group}</svg>'

# Correct Unicode and unmodified licensed contours; design is in the placement.
headline_text = "\u4e00\u676f\u8336\uff0c\u6162\u4e0b\u6765"
headline_frame = {"x":1018,"y":125,"width":344,"height":218}
headline_positions = [
    {"character":"\u4e00","x":1114,"baseline_y":190,"font_size":68,"line":1},
    {"character":"\u676f","x":1189,"baseline_y":190,"font_size":68,"line":1},
    {"character":"\u8336","x":1264,"baseline_y":190,"font_size":68,"line":1},
    {"character":"\uff0c","x":1339,"baseline_y":190,"font_size":68,"line":1},
    {"character":"\u6162","x":1021,"baseline_y":329,"font_size":104,"line":2},
    {"character":"\u4e0b","x":1137,"baseline_y":329,"font_size":104,"line":2},
    {"character":"\u6765","x":1253,"baseline_y":329,"font_size":104,"line":2},
]
headline_elements = []
headline_boxes = []
for index, placement in enumerate(headline_positions):
    source = SOURCE_GLYPHS[placement["character"]]
    s = placement["font_size"]/1000
    x0,y0,x1,y1 = source["exact_bounds_font_units"]
    bounds = [placement["x"]+x0*s, placement["baseline_y"]-y1*s, placement["x"]+x1*s, placement["baseline_y"]-y0*s]
    placement["ink_bounds_poster_px"] = bounds
    placement["source_glyph_name"] = source["glyph_name"]
    headline_boxes.append(bounds)
    headline_elements.append(f'<path id="headline-{index+1}" data-character="{placement["character"]}" data-codepoint="U+{ord(placement["character"]):04X}" data-source-glyph="{source["glyph_name"]}" transform="translate({placement["x"]} {placement["baseline_y"]}) scale({s} {-s})" d="{source["source_svg_path_d"]}"/>')

headline_group = '<g id="headline-outlines" fill="'+COLOR+'">'+''.join(headline_elements)+'</g>'
headline_svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="344" height="218" viewBox="1018 125 344 218"><title>{headline_text}</title><desc>Source Han Serif SC Regular 2.003, SIL OFL 1.1. Exact licensed glyph outlines. First line 一杯茶， at 68 px / 7 px tracking; second line 慢下来 at 104 px / 12 px tracking. Both lines share their right ink edge; the second line steps down-left toward the stream and bowl.</desc>{headline_group}</svg>'

overlay_logo = f'<g transform="translate({logo_on_poster["x"]} {logo_on_poster["y"]}) scale({logo_scale:.12f}) translate(-40 -30)">{logo_group}</g>'
overlay_svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="1536" height="1024" viewBox="0 0 1536 1024"><title>茶作 — 一杯茶，慢下来 — typography only, transparent overlay</title><desc>One typography direction. Photography is not embedded. Source image dimensions 1536 × 1024. Every visible glyph is an editable path.</desc>{overlay_logo}{headline_group}</svg>'

live_glyphs = []
for placement in headline_positions:
    live_glyphs.append(f'<text data-line="{placement["line"]}" x="{placement["x"]}" y="{placement["baseline_y"]}" font-size="{placement["font_size"]}">{placement["character"]}</text>')
live_svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="344" height="218" viewBox="1018 125 344 218"><title>{headline_text} — Unicode text source</title><desc>Requires the exact Source Han Serif SC Regular 2.003 font. Use headline.svg for deterministic outlines.</desc><g fill="{COLOR}" font-family="Source Han Serif SC" font-weight="400">'+''.join(live_glyphs)+'</g></svg>'

files = {
    "chazuo-wordmark.svg": logo_svg,
    "headline.svg": headline_svg,
    "headline-live-text.svg": live_svg,
    "typography-overlay.svg": overlay_svg,
}
for filename, content in files.items():
    (OUT / filename).write_text(content + "\n", encoding="utf-8")
    (PRIVATE / filename).write_text(content + "\n", encoding="utf-8")

construction = {
    "brand": "\u8336\u4f5c", "coordinate_system": "y down; original 1000-unit drawing cells; 作 begins at x=1100",
    "authorship": "Original closed Bézier stroke shapes created in build_lettering.py. The logo imports zero source-font contours.",
    "structural_basis": {"\u8336":"艹 + 人 + lower horizontal / central hook / two lower strokes; 9 authored stroke outlines", "\u4f5c":"亻 + 乍; 7 authored stroke outlines"},
    "shared_behavior": ["Shallow cupped horizontals with gently lifted right endpoints", "Short flat starts and continuous tapered terminals", "Open space between the grass radical, person roof, and lower tea strokes"],
    "source_reference_only": "original_glyph_reference.svg and source_geometry.json establish correct original characters; their paths are not used in chazuo-wordmark.svg.",
    "editable_strokes": STROKES,
    "logo_ink_bounds_units": logo_ink,
}
(OUT / "lettering_construction.json").write_text(json.dumps(construction, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

layout = {
    "canvas": {"width":1536,"height":1024,"aspect_ratio":"3:2"},
    "brand":{"text":"茶作", "file":"chazuo-wordmark.svg", "frame_poster_px":logo_on_poster, "ink_bounds_poster_px":logo_ink_poster},
    "headline":{"text":headline_text, "line_breaks":["一杯茶，","慢下来"],"file":"headline.svg", "frame_poster_px":headline_frame, "ink_bounds_poster_px":bbox_union(headline_boxes), "glyph_placements":headline_positions},
    "type_color":COLOR,
    "placement_reason":"Brand sits on the bowl side at upper left. Headline has a shared right edge; its larger second line steps left and down, continuing toward the diagonal stream then the bowl. The final visible text ends before y=338.",
    "product_region_clear":"No typography at y>=344. Bowl, tea leaves, tray, tabletop and stream highlights keep their original pixels.",
    "compositing":"Overlay typography-overlay.svg or its transparent PNG at x=0,y=0,width=1536,height=1024. Do not crop or rescale the frozen photography.",
}
(OUT / "typography-layout.json").write_text(json.dumps(layout, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

provenance = {
    "asset_direction":"One custom 茶作 lettering and one two-line headline arrangement",
    "maker_role":"Typography asset production only; no self review or mainline/state modification",
    "actual_inputs_seen":{"photography_path":".liu-visual-private/source_recovery_20261003/photography-local-reconstruction-final.png","photography_sha256":SOURCE["actual_input_identity"]["photography_sha256"],"photography_view":"view_image, original detail; full 1536 × 1024 pixels","reference_path":".liu-visual-private/reference.jpg","reference_sha256":SOURCE["actual_input_identity"]["reference_sha256"],"reference_view":"view_image, original detail; mechanism taken only from upper horizontal advertisement, not lower application","source_glyph_reference":"original_glyph_reference.svg rendered with sharp, then viewed with view_image as a structural source reference"},
    "logo":{"text":"茶作","creation":"16 independently editable, authored closed Bézier paths","source_font_contours_in_final_logo":0,"geometry_evidence":"lettering_construction.json","geometry_method":"Explicit moveTo / curveTo / lineTo / closePath commands replayed into SVGPathPen and BoundsPen","design_intervention":"All brand stroke silhouettes, component proportions, hook, tapered terminals, curved crossbars and character interval were newly drawn. No leaf added and no random eroded texture."},
    "headline":{"text":headline_text,"font_source":SOURCE["font"],"outline_modification":"none; licensed glyph geometry is preserved","layout_design":"68 px first line / 104 px second line; respective 7 px / 12 px tracking; first line 93 px farther right; paired right ink edges at approximately x=1354","editing_source":"headline-live-text.svg plus build_lettering.py; exact paths headline.svg"},
    "actual_execution":{"python_executable":sys.executable,"fonttools_version":fontTools.__version__,"fonttools_runtime":fontTools.__file__,"methods":["TTFont.getBestCmap","TTFont.getGlyphSet","BoundsPen","RecordingPen","SVGPathPen","TransformPen"],"runtime_extension":"Existing Hermes site-packages appended for fontTools; no package installation","rasterizer":"Bundled Node sharp; separate render_assets.cjs","dependencies_note":"Initial bundled Python fontTools import was unavailable; existing 4.63.0 reused. PIL could not load a transitive package from that secondary path, so no PIL rendering was used.","image_generation_calls":0,"figma_calls":0},
    "license_evidence":"SOURCE_HAN_SERIF_OFL.txt is an exact byte copy of upstream Adobe license. Source Han Serif is used for headline and structural reference; no modified font software is distributed.",
    "limits":["Maker has viewed source photography, reference, and original font glyph reference only; finished assets need the independently assigned review.","This is typography only. A final commercial-poster assessment depends on the full composition at 1536 × 1024 and on human acceptance.","Live text requires Source Han Serif SC Regular 2.003; path assets and outlined overlay are deterministic without installed fonts."],
    "file_sha256":{filename:sha(OUT/filename) for filename in files},
    "structural_geometry_sha256":sha(OUT/"lettering_construction.json"),
    "source_geometry_sha256":sha(OUT/"source_geometry.json"),
}
(OUT / "provenance.json").write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(PRIVATE / "provenance.json").write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

notes = """# 茶作文字资产的几何依据

这是同一个摄影方向的一组文字资产。品牌来源于自身笔画：横画有浅弧、右端轻提，竖画与撇捺有连续的粗细变化。没有独立叶子或随机破损。

品牌共 16 条原创封闭贝塞尔路径：茶 9 条，作 7 条。`lettering_construction.json` 保存每一条的控制点、组件身份和实测轮廓边界；`build_lettering.py` 通过 fontTools SVGPathPen 实际生成路径。Source Han Serif 的品牌轮廓只用于核对茶作结构，最终字标没有导入它的轮廓。

标题准确为“一杯茶，慢下来”，换行为“一杯茶，”和“慢下来”。字体是有 OFL 1.1 许可的 Adobe Source Han Serif SC Regular 2.003，原始 OTF SHA256 为 78aa7a328fd974df2d688c8a9fd74a33d8334dfa84ab24d9d11efb2ffc464117。标题保持真实字形；第一行 68 px、字距 7 px，第二行 104 px、字距 12 px，右侧墨迹边界相齐。第二行从上行向左下移 93 px，接向溪流和茶碗方向。文件 `headline-live-text.svg` 保留准确 Unicode；`headline.svg` 是逐字可编辑轮廓。

建议直接使用 `typography-overlay.svg` 或其透明 PNG，在原摄影上按 1536×1024、x=0、y=0 合成。字标框 x=92、y=77、宽224、高约104.83；标题框 x=1018、y=125、宽344、高218。颜色统一为 #F5F5EF。产品区域没有文字。

本资产制作角色没有看或审核完成资产，也不提供审美评分；独立复审需实际查看它们与原摄影组成的成品。
"""
(OUT / "geometry_notes.md").write_text(notes, encoding="utf-8")
print(json.dumps({"assets":list(files),"brand_frame":logo_on_poster,"headline_frame":headline_frame,"brand_stroke_count":len(STROKES),"logo_ink":logo_ink_poster,"headline_ink":bbox_union(headline_boxes)}, ensure_ascii=True, indent=2))
