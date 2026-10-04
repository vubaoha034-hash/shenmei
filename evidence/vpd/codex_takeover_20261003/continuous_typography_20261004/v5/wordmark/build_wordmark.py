"""Build exactly one original 茶作 wordmark from authored closed contours."""
from pathlib import Path
import hashlib
import json
import math
import os
import sys

sys.dont_write_bytecode=True
sys.path.append(r"C:/Users/Administrator/AppData/Local/hermes/hermes-agent/venv/Lib/site-packages")
import fontTools
from fontTools.pens.boundsPen import BoundsPen

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[5]
SCALE=.13
COLOR="#F5F2E6"

def M(x,y): return ("moveTo",((x,y),))
def L(x,y): return ("lineTo",((x,y),))
def C(x1,y1,x2,y2,x3,y3): return ("curveTo",((x1,y1),(x2,y2),(x3,y3)))
def Z(): return ("closePath",())

def bar(left,right,top,width=64,cut=22,bend=6):
    """Original horizontal profile: matching45-degree cuts, mild paired curvature."""
    span=right-left
    return [M(left+cut,top),C(left+span/3,top-bend,right-span/3,top-bend,right-cut,top),L(right,top+cut),L(right,top+width-cut),L(right-cut,top+width),C(right-span/3,top+width-bend,left+span/3,top+width-bend,left+cut,top+width),L(left,top+width-cut),L(left,top+cut),Z()]

def upright(left,top,bottom,width=82,cut=22):
    """Original straight shaft, with the same octagonal cut ends as horizontal bars."""
    right=left+width
    return [M(left+cut,top),L(right-cut,top),L(right,top+cut),L(right,bottom-cut),L(right-cut,bottom),L(left+cut,bottom),L(left,bottom-cut),L(left,top+cut),Z()]

strokes=[
    {"id":"cha-grass-horizontal","character":"茶","component":"艹","skeleton_role":"艹共享横画","origin":"Authored bar profile; no font contour or prior artwork copied","commands":bar(84,884,179,72,22,6)},
    {"id":"cha-grass-left-upright","character":"茶","component":"艹","skeleton_role":"艹左竖","origin":"Authored upright profile,88unit shaft","commands":upright(250,72,281,88,22)},
    {"id":"cha-grass-right-upright","character":"茶","component":"艹","skeleton_role":"艹右竖","origin":"Authored upright profile, matches left upright exactly","commands":upright(628,72,281,88,22)},
    {"id":"cha-person-roof","character":"茶","component":"人","skeleton_role":"人撇捺合为一个连续屋顶轮廓，仍为两笔的真实骨架","origin":"Newly authored closed cubic outline; the terminal straight cuts use the same diagonal as bars","commands":[M(489,303),L(559,373),C(664,464,766,532,894,568),L(928,602),L(883,647),C(725,589,599,488,517,400),C(418,500,285,595,133,652),L(88,607),C(267,523,402,414,489,303),Z()]},
    {"id":"cha-wood-horizontal","character":"茶","component":"木","skeleton_role":"木横画","origin":"Authored bar profile,64unit weight, same profile as乍中下横","commands":bar(226,752,654,64,22,6)},
    {"id":"cha-wood-stem-hook","character":"茶","component":"木","skeleton_role":"木主竖及浅左钩","origin":"Authored82unit shaft and cubic hook. Top is the same22unit cut-cap used in作; hook is part of the correct stroke, not a separate graphic","commands":[M(492,526),L(530,526),L(552,548),L(552,884),C(552,927,531,959,482,970),L(402,970),L(380,948),L(420,908),L(454,908),C(466,908,470,898,470,885),L(470,548),Z()]},
    {"id":"cha-wood-left-falling","character":"茶","component":"木","skeleton_role":"木左撇","origin":"Authored paired cubic boundaries; both flat ends follow45degree cuts","commands":[M(342,748),L(398,804),C(353,859,283,909,209,939),L(169,899),C(254,849,304,796,342,748),Z()]},
    {"id":"cha-wood-right-falling","character":"茶","component":"木","skeleton_role":"木右点/捺","origin":"Authored paired cubic boundaries; both ends use the same cut relation as the left stroke","commands":[M(627,794),L(672,749),C(749,802,819,863,861,915),L(822,954),C(760,895,699,841,627,794),Z()]},
    {"id":"zuo-person-falling","character":"作","component":"亻","offset_x":1012,"skeleton_role":"亻撇","origin":"New closed cubic outline with45degree cut terminals; no brush texture","commands":[M(274,72),L(330,128),C(299,278,223,447,107,574),L(64,531),C(162,406,232,250,274,72),Z()]},
    {"id":"zuo-person-upright","character":"作","component":"亻","offset_x":1012,"skeleton_role":"亻竖","origin":"Authored82unit upright, exactly the main-shaft width of茶木","commands":upright(184,392,970,82,22)},
    {"id":"zuo-zha-falling","character":"作","component":"乍","offset_x":1012,"skeleton_role":"乍上撇","origin":"New closed cubic outline with45degree cuts, same grammar as亻撇","commands":[M(529,72),L(585,128),C(551,279,479,436,354,549),L(311,506),C(422,383,492,230,529,72),Z()]},
    {"id":"zuo-zha-upper-horizontal","character":"作","component":"乍","offset_x":1012,"skeleton_role":"乍上横","origin":"Authored64unit bar with the common cut profile","commands":bar(438,920,293,64,22,6)},
    {"id":"zuo-zha-main-upright","character":"作","component":"乍","offset_x":1012,"skeleton_role":"乍主竖","origin":"Authored82unit upright matching茶木主竖 and亻竖","commands":upright(568,324,970,82,22)},
    {"id":"zuo-zha-middle-horizontal","character":"作","component":"乍","offset_x":1012,"skeleton_role":"乍中横","origin":"Exact shared bar construction profile of茶木横,64unit weight","commands":bar(622,900,548,64,22,6)},
    {"id":"zuo-zha-lower-horizontal","character":"作","component":"乍","offset_x":1012,"skeleton_role":"乍下横","origin":"Exact shared bar construction profile of茶木横,64unit weight","commands":bar(622,920,761,64,22,6)},
]

def to_pixels(commands,offset=0):
    return [(op,tuple(((x+offset)*SCALE,y*SCALE) for x,y in pts)) for op,pts in commands]

def number(n):
    return f"{n:.6f}".rstrip('0').rstrip('.')

def svg_data(commands):
    letters={"moveTo":"M","lineTo":"L","curveTo":"C","closePath":"Z"}
    return ' '.join(letters[op]+(' '.join(number(n) for pt in pts for n in pt) if pts else '') for op,pts in commands)

def exact_bounds(commands):
    pen=BoundsPen(None)
    for op,pts in commands:getattr(pen,op)(*pts)
    return pen.bounds

paths=[]; figma_paths=[]; all_boxes=[]
for item in strokes:
    pixel_commands=to_pixels(item['commands'],item.get('offset_x',0))
    data=svg_data(pixel_commands)
    item['final_pixel_commands']=pixel_commands
    item['svg_path_d']=data
    item['exact_ink_bounds_px']=exact_bounds(pixel_commands)
    all_boxes.append(item['exact_ink_bounds_px'])
    paths.append(f'<path id="{item["id"]}" data-character="{item["character"]}" data-component="{item["component"]}" d="{data}"/>')
    figma_paths.append({"name":item['id'],"character":item['character'],"windingRule":"NONZERO","data":data})

ink=[min(b[0] for b in all_boxes),min(b[1] for b in all_boxes),max(b[2] for b in all_boxes),max(b[3] for b in all_boxes)]
svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="260" height="135" viewBox="0 0 260 135"><title>茶作 — original cut-contour wordmark</title><desc>One authored wordmark. 茶 contains艹、人、木; 作 contains亻、乍. All15 closed path contours are newly authored M/L/C/Z geometry. Main verticals82design units, key horizontal bars64units, shared45degree cut ends and22unit corner cuts. There is no font outline, calligraphic texture, added leaf, seal or auxiliary copy.</desc><g id="chazuo-original-wordmark" fill="{COLOR}" fill-rule="nonzero">'+''.join(paths)+'</g></svg>\n'
OUT.mkdir(parents=True,exist_ok=True)
(OUT/'chazuo-wordmark.svg').write_text(svg,encoding='utf-8')
(OUT/'figma-vector-paths.json').write_text(json.dumps({"width":260,"height":135,"ink_bounds_px":ink,"paths":figma_paths,"integration":"Every data string uses only the supported absoluteM/L/C/Z commands. Put separate paths under one vector group or importchazuo-wordmark.svg; apply one fill. No font is required."},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

construction={"brand":"茶作","authorship":"Original Bézier and polygon geometry drawn directly in this script, not based on any font outline, raster trace or previous version path","unique_direction":"Compact cut-contour identity, with a shallow curved body and controlled angled endpoints; this wordmark is distinct in detail fromV4 brush headline","canvas_px":[260,135],"design_unit_scale":SCALE,"glyph_cells":{"茶":0,"作":1012},"character_structure":{"茶":"艹3strokes + 人2strokes combined as one closed contour + 木4strokes","作":"亻2strokes + 乍5strokes"},"editable_contours":len(strokes),"shared_identity":{"main_vertical_weight_units":82,"main_vertical_weight_px":10.66,"wood_and_zha_horizontal_weight_units":64,"wood_and_zha_horizontal_weight_px":8.32,"corner_cut_units":22,"corner_cut_px":2.86,"key_terminal_angle_degrees":45,"horizontal_cubic_bend_units":6,"grass_shaft_units":88,"mechanism":"茶木与作乍采用同一主竖重量、横画轮廓配方与端点切口；左右字的斜画同为平切收笔。两字保持独立而以相同构形建立身份，不作夸张连笔。"},"counter_space":{"grass_to_person_top_gap_units":22,"wood_top_to_crossbar_gap_units":106,"zha_middle_to_lower_clear_space_units":149,"intercharacter_nearest_bbox_gap_units":148,"note":"Optical spacing is compact without joined strokes. Internal openings come from actual character construction and remain clear at260px wordmark width."},"stroke_by_stroke_origin":strokes,"ink_bounds_px":ink}
(OUT/'construction.json').write_text(json.dumps(construction,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

methods={"bounded_primary_sources":[{"title":"Glyphs: Drawing good paths","url":"https://glyphsapp.com/learn/drawing-good-paths","accessed_utc":"2026-10-03","applied":"Separate intentional corner nodes from smooth curves, use two explicit controls for each cubic, avoid redundant points and close contours. Keep component outlines separately editable."},{"title":"Glyphs Handbook: Drawing Paths","url":"https://handbook.glyphsapp.com/drawing-paths/","accessed_utc":"2026-10-03","applied":"Use line segments for cut faces and cubic segments for gentle body curvature, with explicit on-curve nodes and off-curve handles."},{"title":"Figma Developer Docs: VectorPath data","url":"https://developers.figma.com/docs/plugins/api/properties/VectorPath-data/","accessed_utc":"2026-10-03","applied":"Output supported absoluteM/L/C/Z path commands andNONZERO winding information so the outline remains directly editable in Figma."}],"boundary":"The methods were read in official documentation and applied to an independently authored SVG. Glyphs desktop app and Figma were not run by this maker. There is no claim that the official applications created or endorsed this lettering."}
(OUT/'method_basis.json').write_text(json.dumps(methods,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
photo=ROOT/'.liu-visual-private/source_recovery_20261003/photography-local-reconstruction-final.png'
ref=ROOT/'.liu-visual-private/reference.jpg'
v4=ROOT/'.liu-visual-private/correct_source_typography/v4/poster.png'
if not photo.exists():raise ValueError(f'Wrong workspace root: {ROOT}')
assert sha(photo)=='7fd7777fed21100cb6b47bc305701476054263565e73246ac469d065aa080618'
provenance={"unique_asset":"V5 original茶作 wordmark, one SVG, no alternate candidate","actual_pixels_seen":{"reference":{"path":str(ref.relative_to(ROOT)).replace('\\','/'),"sha256":sha(ref),"view":"view_image originaldetail; only upper advertisement used for mechanism"},"formal_v4":{"path":str(v4.relative_to(ROOT)).replace('\\','/'),"sha256":sha(v4),"view":"view_image originaldetail"}},"photography":{"sha256":sha(photo),"original_unchanged":True,"usage":"Not embedded, edited or rendered by this wordmark maker"},"sources":{"font_outline_imports":0,"raster_outline_traces":0,"prior_wordmark_path_imports":0,"font_license_required_for_final_asset":False,"original_control_geometry":"build_wordmark.py andconstruction.json, every contour identified by actual character stroke"},"execution":{"python_executable":sys.executable,"fonttools_version":fontTools.__version__,"fonttools_usage":"BoundsPen for exact cubic geometry bounds only; no font loading","thread_id":os.environ.get('CODEX_THREAD_ID'),"figma_calls":0,"glyphs_app_calls":0,"image_generation_calls":0,"state_writes":0,"rasterizer":"render_wordmark.cjs uses bundled Node sharp"},"limitations":["Maker performs no self aesthetic scoring or acceptance judgement.","Professional path methods and correct character construction do not establish AI_PASS or human acceptance.","Root is responsible for title hierarchy and final placement; this asset contains only the brand name."],"svg_sha256":sha(OUT/'chazuo-wordmark.svg'),"construction_sha256":sha(OUT/'construction.json')}
(OUT/'provenance.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({"svg":str(OUT/'chazuo-wordmark.svg'),"sha256":provenance['svg_sha256'],"dimensions":[260,135],"ink_bounds":ink,"closed_contours":len(strokes)},ensure_ascii=True,indent=2))
