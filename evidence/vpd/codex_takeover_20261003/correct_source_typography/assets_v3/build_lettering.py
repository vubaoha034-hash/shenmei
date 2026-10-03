"""One final source-based contour revision. No project-state or other-version writes."""
from pathlib import Path
import copy
import hashlib
import importlib
import json
import os
import sys

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
PRIVATE = ROOT / ".liu-visual-private/correct_source_typography/lettering_v3"
FONT = ROOT / "evidence/vpd/codex_takeover_20261003/skill_research/fonttools_bounded_probe_v1/upstream/adobe-fonts/source-han-serif/OTF/SimplifiedChinese/SourceHanSerifSC-Regular.otf"
FONT_SHA = "78aa7a328fd974df2d688c8a9fd74a33d8334dfa84ab24d9d11efb2ffc464117"
LICENSE = FONT.parents[2] / "LICENSE.txt"
PHOTO = ROOT / ".liu-visual-private/source_recovery_20261003/photography-local-reconstruction-final.png"
PHOTO_SHA = "7fd7777fed21100cb6b47bc305701476054263565e73246ac469d065aa080618"
REFERENCE = ROOT / ".liu-visual-private/reference.jpg"
REVIEW = OUT.parent / "v2/pixel_review/REVIEWER_OUTPUT.json"
V2_POSTER = ROOT / ".liu-visual-private/correct_source_typography/v2/poster.png"
COLOR = "#F5F5EF"

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
assert sha(PHOTO) == PHOTO_SHA
assert sha(FONT) == FONT_SHA
review = json.loads(REVIEW.read_text(encoding="utf-8"))
font = TTFont(FONT)
glyphset = font.getGlyphSet()
cmap = font.getBestCmap()

def M(x,y): return ("moveTo", ((x,y),))
def L(x,y): return ("lineTo", ((x,y),))
def C(x1,y1,x2,y2,x3,y3): return ("curveTo", ((x1,y1),(x2,y2),(x3,y3)))
def Z(): return ("closePath", ())
def replay(commands, pen):
    for operation, points in commands: getattr(pen,operation)(*points)
def union(boxes):
    return [min(x[0] for x in boxes),min(x[1] for x in boxes),max(x[2] for x in boxes),max(x[3] for x in boxes)]
def split_contours(commands):
    result, current = [], []
    for command in commands:
        current.append(command)
        if command[0] == "closePath": result.append(current); current=[]
    if current: result.append(current)
    return result
def join_contours(contours): return [cmd for contour in contours for cmd in contour]

# Explicit source coordinate sites: triangular horizontal terminals are redrawn
# as low, continuous Bézier shoulders. This is document-outline work, not font software.
PEAKS = {
    "\u8336": {(869,777):717,(696,354):303},
    "\u4f5c": {(853,275):215,(839,487):429,(879,698):637},
    "\u4e00": {(841,514):431},
    "\u676f": {(876,810):750,(369,664):607},
    "\u6162": {(819,835):798,(885,531):495,(837,290):251},
    "\u4e0b": {(863,815):748},
    "\u6765": {(858,450):387,(818,740):679},
}

def soft_shoulders(commands, peaks):
    """Redraw the turn into and out of each named shoulder, preserving source topology."""
    result=[]
    previous_endpoint=None
    for operation, points in commands:
        endpoint=tuple(points[-1]) if points else None
        prior_peak=previous_endpoint if previous_endpoint in peaks else None
        if endpoint in peaks:
            px,py=endpoint; base=peaks[endpoint]
            height=base+(py-base)*.32
            p=(float(px),float(height))
            if operation == "moveTo": result.append((operation,(p,)))
            elif operation == "curveTo":
                first=tuple(points[0]); first=(first[0],base+(first[1]-base)*.32 if first[1]>base else first[1])
                result.append(("curveTo",(first,(px+14,height),p)))
            elif operation == "lineTo":
                ex,ey=previous_endpoint
                result.append(("curveTo",((ex-8,ey+8),(px+14,height),p)))
            else: raise ValueError(operation)
        elif operation == "lineTo" and prior_peak:
            px,py=prior_peak; base=peaks[prior_peak]; height=base+(py-base)*.32
            ax,ay=endpoint
            result.append(("curveTo",((px-14,height),(ax+12,ay),(ax,ay))))
        else: result.append(copy.deepcopy((operation,points)))
        if endpoint is not None: previous_endpoint=endpoint
    return result

def remap_x(commands, mapping):
    return [(op,tuple((mapping(x),y) for x,y in pts)) for op,pts in commands]

def cupped_lines(commands, amplitude, left=0, right=1000, band=None):
    """Continuous shallow y displacement; source horizontal lines become exact cubics."""
    middle=(left+right)/2; half=(right-left)/2
    def delta(x): return -amplitude*(1-((x-middle)/half)**2)
    def derivative(x): return 2*amplitude*(x-middle)/(half*half)
    def selected(y): return band is None or band[0]<=y<=band[1]
    def point(p):
        x,y=p; return (x,y+delta(x) if selected(y) else y)
    result=[]; previous=None; start=None
    for operation, pts in commands:
        if operation == "moveTo":
            result.append((operation,(point(pts[0]),))); previous=tuple(pts[0]); start=previous
        elif operation == "lineTo":
            target=tuple(pts[0])
            if previous[1] == target[1] and selected(target[1]) and previous[0] != target[0]:
                p0=point(previous); p3=point(target); dx=target[0]-previous[0]
                c1=(previous[0]+dx/3,p0[1]+derivative(previous[0])*dx/3)
                c2=(target[0]-dx/3,p3[1]-derivative(target[0])*dx/3)
                result.append(("curveTo",(c1,c2,p3)))
            else: result.append((operation,(point(target),)))
            previous=target
        elif operation == "curveTo":
            result.append((operation,tuple(point(p) for p in pts))); previous=tuple(pts[-1])
        elif operation == "closePath": result.append((operation,())); previous=start
        else: raise ValueError(operation)
    return result

original = {}
processed = {}
source_records=[]
for ch in "\u8336\u4f5c\u4e00\u676f\u6162\u4e0b\u6765\uff0c":
    name=cmap[ord(ch)]
    record=RecordingPen(); glyphset[name].draw(record)
    bounds=BoundsPen(glyphset); glyphset[name].draw(bounds)
    original[ch]=copy.deepcopy(record.value)
    modified=soft_shoulders(record.value,PEAKS.get(ch,{}))
    contours=split_contours(modified)
    if ch == "\u8336":
        # Newly drawn person roof, using the source's correct component and connections.
        contours[0]=[M(518,605),C(590,475,730,363,899,292),C(915,307,933,324,948,339),C(959,350,954,362,943,366),C(780,414,629,504,538,616),C(554,620,565,623,568,631),L(463,653),C(406,523,213,357,40,281),C(35,277,36,267,45,264),C(246,334,430,470,518,605),Z()]
        def grass_width(x):
            if 294<=x<=394: return 294+(x-294)*1.12
            if 637<=x<=737: return 637+(x-637)*1.12
            return x
        contours[3]=cupped_lines(remap_x(contours[3],grass_width),20,48,955)
        def stem_width(x):
            return 470+(x-470)*(74/65) if 470<=x<=566 else x
        lower=remap_x(contours[4],stem_width)
        lower[11:17]=[C(470,8,457,1,438,1),C(406,1,363,8,331,12),L(329,-8),C(373,-16,405,-33,419,-55),C(427,-67,431,-77,433,-82),C(521,-74,544,-27,544,22)]
        contours[4]=cupped_lines(lower,14,211,778,(250,360))
    elif ch == "\u4f5c":
        # Source main shafts are brought to the 72–75 unit rhythm of the tea stem.
        contours[0]=remap_x(contours[0],lambda x:648 if x==640 else x)
        contours[1]=remap_x(contours[1],lambda x:256 if x==249 else x)
        contours[0]=cupped_lines(contours[0],12,640,941,(180,280))
        contours[0]=cupped_lines(contours[0],12,640,922,(395,490))
        contours[0]=cupped_lines(contours[0],18,512,966,(600,710))
    # This final small curvature is shared by brand and headline glyphs, including 茶.
    modified=cupped_lines(join_contours(contours),12,0,1000)
    processed[ch]=modified
    exact=BoundsPen(None); replay(modified,exact)
    svg=SVGPathPen(None); replay(modified,svg)
    source_records.append({"character":ch,"codepoint":f"U+{ord(ch):04X}","source_glyph_name":name,"original_bounds_font_units":bounds.bounds,"original_recording_commands":record.value,"modified_bounds_design_units":exact.bounds,"modified_recording_commands":modified,"modified_svg_path_d":svg.getCommands(),"contour_count":len(split_contours(modified))})

glyph_record={g["character"]:g for g in source_records}
logo_paths=[]; logo_boxes=[]
brand_glyph_placements=[{"character":"茶","x_units":0},{"character":"作","x_units":985}]
for placement in brand_glyph_placements:
    ch=placement["character"]; offset=placement["x_units"]
    bounds=BoundsPen(None)
    replay(processed[ch],TransformPen(bounds,(.98,0,0,-1,offset,858)))
    logo_boxes.append(bounds.bounds)
    logo_paths.append(f'<path id="wordmark-{ord(ch):x}" data-character="{ch}" data-origin="font-derived-contour-design" transform="translate({offset} 858) scale(.98 -1)" d="{glyph_record[ch]["modified_svg_path_d"]}"/>')
logo_units=[0,0,1950,960]
logo_placement={"x":92,"y":86,"width":278,"height":278*960/1950}
logo_scale=278/1950
logo_box=union(logo_boxes)
logo_ink=[92+logo_box[0]*logo_scale,86+logo_box[1]*logo_scale,92+logo_box[2]*logo_scale,86+logo_box[3]*logo_scale]
logo_group=f'<g id="font-derived-chazuo-v3" fill="{COLOR}">'+''.join(logo_paths)+'</g>'
logo_svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="278" height="{logo_placement["height"]:.6f}" viewBox="0 0 1950 960"><title>茶作 — source-based contour lettering</title><desc>Based on licensed Source Han Serif SC Regular 2.003. The 茶 roof and stem-hook are locally redrawn, grass and crossbar arcs are rebuilt, 作 shafts and bars are adjusted. Both share continuous low Bézier shoulders. This is font-derived contour design, not 100% original lettering.</desc>{logo_group}</svg>'

text="\u4e00\u676f\u8336\uff0c\u6162\u4e0b\u6765"
title_positions=[
    {"character":"\u4e00","x":958,"baseline_y":315,"font_size":80,"line":1},
    {"character":"\u676f","x":1044,"baseline_y":315,"font_size":80,"line":1},
    {"character":"\u8336","x":1130,"baseline_y":315,"font_size":80,"line":1},
    {"character":"\uff0c","x":1216,"baseline_y":315,"font_size":80,"line":1},
    {"character":"\u6162","x":938,"baseline_y":422,"font_size":96,"line":2},
    {"character":"\u4e0b","x":1042,"baseline_y":422,"font_size":96,"line":2},
    {"character":"\u6765","x":1146,"baseline_y":422,"font_size":96,"line":2},
]
title_frame={"x":934,"y":239,"width":312,"height":197}
title_boxes=[]; title_paths=[]
for index,placement in enumerate(title_positions):
    ch=placement["character"]; s=placement["font_size"]/1000
    bounds=BoundsPen(None)
    replay(processed[ch],TransformPen(bounds,(s*.98,0,0,-s,placement["x"],placement["baseline_y"])))
    placement["ink_bounds_poster_px"]=bounds.bounds
    placement["source_glyph_name"]=glyph_record[ch]["source_glyph_name"]
    placement["modified_glyph_definition_sha256"]=hashlib.sha256(glyph_record[ch]["modified_svg_path_d"].encode()).hexdigest()
    title_boxes.append(bounds.bounds)
    title_paths.append(f'<path id="headline-v3-{index+1}" data-character="{ch}" data-codepoint="U+{ord(ch):04X}" data-origin="font-derived-contour-design" transform="translate({placement["x"]} {placement["baseline_y"]}) scale({s*.98} {-s})" d="{glyph_record[ch]["modified_svg_path_d"]}"/>')
title_group=f'<g id="shared-contour-headline-v3" fill="{COLOR}">'+''.join(title_paths)+'</g>'
title_svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="312" height="197" viewBox="934 239 312 197"><title>{text}</title><desc>Real edited Source Han Serif SC outlines with shared low Bézier shoulders and shallow cupped horizontal lines. The headline 茶 uses the exact same edited glyph definition as the brand. No synthetic stroke thickening or arbitrary italic transform is used. Line sizes80/96px, baselines315/422.</desc>{title_group}</svg>'
overlay_logo=f'<g transform="translate(92 86) scale({logo_scale:.12f})">{logo_group}</g>'
overlay_svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="1536" height="1024" viewBox="0 0 1536 1024"><title>茶作 — 一杯茶，慢下来 — final typography revision</title><desc>One shared font-derived contour language, used for brand and headline. Exact photography is not embedded. Typography remains within the two fixed protected envelopes.</desc>{overlay_logo}{title_group}</svg>'

OUT.mkdir(parents=True,exist_ok=True); PRIVATE.mkdir(parents=True,exist_ok=True)
files={"chazuo-wordmark.svg":logo_svg,"headline.svg":title_svg,"typography-overlay.svg":overlay_svg}
for filename,content in files.items():
    (OUT/filename).write_text(content+"\n",encoding="utf-8")
    (PRIVATE/filename).write_text(content+"\n",encoding="utf-8")
(OUT/"SOURCE_HAN_SERIF_OFL.txt").write_bytes(LICENSE.read_bytes())
(OUT/"headline-copy.txt").write_text(text+"\n一杯茶，\n慢下来\n",encoding="utf-8")

font_record={"path":str(FONT.relative_to(ROOT)).replace("\\","/"),"sha256":FONT_SHA,"family":font["name"].getDebugName(1),"version":font["name"].getDebugName(5),"units_per_em":font["head"].unitsPerEm,"license":"SIL Open Font License 1.1","license_sha256":sha(LICENSE),"copyright":font["name"].getDebugName(0)}
geometry={"authorship":"Font-derived graphic outlines with explicit local redraws, not 100% original letters and not modified font software","source_font":font_record,"source_and_modified_glyphs":source_records,"editable_brand_compound_paths":2,"brand_closed_contours":sum(len(split_contours(processed[ch])) for ch in '茶作'),"shared_character_definition":{"character":"茶","brand_and_headline_exact_modified_path_match":True,"definition_sha256":hashlib.sha256(glyph_record['茶']['modified_svg_path_d'].encode()).hexdigest()},"recipes":{"horizontal_shoulder_sites":{ch:[{"peak":p,"base_y":base} for p,base in peaks.items()] for ch,peaks in PEAKS.items()},"shoulder_peak_height_multiplier":.32,"shoulder_turn_controls":"±14 units around the new peak, then a cubic to the original horizontal return","shared_shallow_displacement":"y -=12*(1-((x-500)/500)^2); source horizontal lines are replaced by cubic curves","茶_specific":"Source roof contour replaced with authored closed Bézier contour; grass shafts widened12%, crossbar cupped20units; central stem widened65->74units and left hook controls redrawn; lower crossbar cupped14units","作_specific":"Right vertical640->648, left radical vertical249->256; three horizontal bar arcs reconstructed at12/12/18units","glyph_width_scale":.98}}
(OUT/"contour_design.json").write_text(json.dumps(geometry,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
layout={"canvas":{"width":1536,"height":1024,"aspect_ratio":"3:2"},"brand":{"text":"茶作","frame_poster_px":logo_placement,"ink_bounds_poster_px":logo_ink,"glyph_placements_design_units":brand_glyph_placements},"headline":{"text":text,"line_breaks":["一杯茶，","慢下来"],"frame_poster_px":title_frame,"ink_bounds_poster_px":union(title_boxes),"glyph_placements":title_positions,"font_sizes_px":[80,96],"nominal_tracking_px":[6,8],"baseline_separation_px":107,"visible_interline_gap_px":union(title_boxes[4:])[1]-union(title_boxes[:4])[3]},"type_color":COLOR,"fixed_protection_envelopes":[[64,56,504,304],[800,72,1504,440]],"spatial_change":"Brand width224->278 and follows the same controlled source-based stroke language. Headline moves approximately100px left toward the tea tray's axis; the bottom is close to430 and remains below440. The two lines have closer relative sizes80/96.","compositing":"Place typography-overlay.svg/PNG at0,0 without crop or rescale on frozen source. PNG preview uses source RGB copying and explicit alpha blend only inside the two original envelopes."}
(OUT/"typography-layout.json").write_text(json.dumps(layout,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

delta={"scope":"Final one-direction repair of the lettering language, not another weight-only or location-only variation","independent_v2_review":{"path":str(REVIEW.relative_to(ROOT)).replace("\\","/"),"sha256":sha(REVIEW),"source_verdict":review['verdict']},"actual_changes":[{"issue":"Free narrow wordmark and standard Song headline are visibly separate","change":"Rebase the wordmark on the licensed correct glyph skeleton and redesign its roof, hook, shaft widths and horizontal contours. Use the same edited definition of 茶 in the headline. Replace all named headline horizontal serif peaks with continuous low Bézier shoulders.","evidence":"contour_design.json contains original and edited operations, exact source glyph IDs, every replacement coordinate and shared 茶 path hash."},{"issue":"Wordmark lacks a stable two-character structure","change":"茶 and 作 now share the source family's established stroke topology and width proportions, with72–75unit main-shaft rhythm, a shared shallow curved horizontal treatment and a compact985unit cell start for作.","evidence":"Brand no longer preserves the V1/V2 16-outline count. Final two compound paths retain7 closed source-based contours with local redraws."},{"issue":"Headline remains distant from the tea tray","change":"Shift the headline from approximately1047..1351 to approximately940..1240, keep its lower edge close to430, and relate its narrower width to the enlarged upper-left wordmark. Line sizes become80/96 with107px baseline spacing.","evidence":"typography-layout.json and final raster export alpha bounds record the exact result."}],"retained":["Frozen source photography7fd7777…","1536x1024 and3:2","Tea brand 茶作","Exact copy 一杯茶，慢下来","Quiet mountain/forest photograph and #F5F5EF type","Original fixed left/right envelopes","No standalone leaf, band, badge or new style"],"production_boundary":"This is one V3 asset set. No self score, independent acceptance claim, hidden alternate, image generation or project-state update."}
(OUT/"revision_basis.json").write_text(json.dumps(delta,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

module_records=[]
for name in ['fontTools.ttLib.ttFont','fontTools.pens.recordingPen','fontTools.pens.svgPathPen','fontTools.pens.boundsPen','fontTools.pens.transformPen']:
    module=importlib.import_module(name); path=Path(module.__file__)
    module_records.append({"module":name,"runtime_file":str(path),"sha256":sha(path)})
provenance={"direction":"Same quiet山野 direction; V3 shared source-based contour system","maker_role":"Typography production only; no self scoring or business-state writes","actual_pixels_seen_for_revision":{"formal_figma_v2":{"path":str(V2_POSTER.relative_to(ROOT)).replace('\\','/'),"sha256":sha(V2_POSTER),"view":"view_image original detail"},"frozen_photography":{"path":str(PHOTO.relative_to(ROOT)).replace('\\','/'),"sha256":PHOTO_SHA,"view":"Previously viewed with view_image original detail; exact hash rechecked in this build"},"reference":{"path":str(REFERENCE.relative_to(ROOT)).replace('\\','/'),"sha256":sha(REFERENCE),"view":"Previously viewed with view_image original detail; only upper horizontal advertisement informed mechanism"}},"independent_v2_review":{"path":str(REVIEW.relative_to(ROOT)).replace('\\','/'),"sha256":sha(REVIEW)},"font_source":font_record,"logo_authorship":"Based on licensed font contours with specific locally authored Bézier replacements and point/control redesign. The final letters are not claimed100% original.","headline_authorship":"Same font-derived contour processor and exact shared 茶 definition. Correct glyph topology retained. Synthetic outline stroke fromV2 removed; shape changes are actual filled contour changes.","execution":{"python_executable":sys.executable,"python_version":sys.version,"fonttools_version":fontTools.__version__,"fonttools_runtime":fontTools.__file__,"code_modules":module_records,"code_thread_id":os.environ.get('CODEX_THREAD_ID'),"rasterizer":"Bundled Node sharp, see render_assets.cjs for exact require path and version recorded at execution","image_generation_calls":0,"figma_calls":0,"business_state_writes":0},"license_boundary":"The unchanged Source Han Serif font is OFL1.1, exact license copied. This is a graphic document made with edited font outlines, not a redistributed modified font. No endorsement by the font author is claimed.","limits":["Only one final V3 produced; no independent aesthetic acceptance or human acceptance is asserted.","Correct text, protected RGB and editability are engineering facts; they do not replace independent review.","The fixed y<440 envelope limits how far typography can descend toward the photographed tea tray; its subject contour is preserved."],"svg_sha256":{name:sha(OUT/name) for name in files},"contour_design_sha256":sha(OUT/'contour_design.json'),"revision_basis_sha256":sha(OUT/'revision_basis.json')}
(OUT/"provenance.json").write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+"\n",encoding='utf-8')
(PRIVATE/"provenance.json").write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+"\n",encoding='utf-8')
print(json.dumps({"brand_frame":logo_placement,"brand_ink":logo_ink,"headline_frame":title_frame,"headline_ink":union(title_boxes),"headline_interline_gap":layout['headline']['visible_interline_gap_px'],"brand_compound_paths":2,"brand_contours":geometry['brand_closed_contours'],"shared_tea_definition":geometry['shared_character_definition']},ensure_ascii=True,indent=2))
