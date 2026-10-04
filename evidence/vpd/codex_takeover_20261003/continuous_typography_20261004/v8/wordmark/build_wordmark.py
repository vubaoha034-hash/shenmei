"""One V8 local refinement of the V7 sixteen original contours.

Read-only preflight precedes all geometry and rasterization. The original V7
files are snapshotted by bytes and mtime. The sole export directory and every
output file are created exclusively; no prior asset can be overwritten.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import struct
import subprocess
import sys
import xml.etree.ElementTree as ET

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[5]
OUT = HERE / "artwork"
V7 = REPO / "evidence/vpd/codex_takeover_20261003/continuous_typography_20261004/v7/wordmark"
RUNTIME = Path("C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies")
FONTTOOLS_SITE = "C:/Users/Administrator/AppData/Local/hermes/hermes-agent/venv/Lib/site-packages"
FINAL_SCALE = 220 / 360
SOURCE_PINS = {
    "photo": (".liu-visual-private/source_recovery_20261003/photography-local-reconstruction-final.png", "7fd7777fed21100cb6b47bc305701476054263565e73246ac469d065aa080618"),
    "reference": (".liu-visual-private/reference.jpg", "87a28f5cd4b5d15b01e6536206127c357043a904b3c0dab3bfa0c50080782167"),
    "formal_v7": (".liu-visual-private/correct_source_typography/v7/poster.png", "2c5153c62e27874093bdf7ac13a0274d91130487d77fda886da214fdb22fe86d"),
}
V7_CONSTRUCTION_SHA = "772fb9dde73d7726f65dfcf26c34b46740d8c5534eca210d1df153f7fb97671a"
V7_MANIFEST_SHA = "d3215edc1688e2a76720b23cc4fd8eaa83af262d1e99794c30fa2f74da553285"


class ExportError(Exception):
    def __init__(self, code, detail):
        super().__init__(detail)
        self.code = code


def require(condition, code, detail):
    if not condition:
        raise ExportError(code, detail)


def sha(data): return hashlib.sha256(data).hexdigest()
def encoded(value): return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def source_check(photo_override=None):
    sources = {}
    for name, (relative, expected) in SOURCE_PINS.items():
        data = (REPO / relative).read_bytes()
        require(sha(data) == expected, "SOURCE_SHA_MISMATCH", name)
        sources[name] = {"path": relative, "sha256": expected, "bytes": len(data)}
    if photo_override:
        require(sha(Path(photo_override).read_bytes()) == SOURCE_PINS["photo"][1], "SOURCE_SHA_MISMATCH", "photo override")
    return sources


def history_snapshot():
    return {str(path.relative_to(V7)).replace("\\", "/"): (path.read_bytes(), path.stat().st_mtime_ns) for path in V7.rglob("*") if path.is_file()}


def preflight(args, progress):
    sources = source_check(args.photo_path)
    require(not OUT.exists(), "OUTPUT_EXISTS", str(OUT))
    previous = history_snapshot()
    manifest_bytes = previous["artwork/manifest.json"][0]
    require(sha(manifest_bytes) == V7_MANIFEST_SHA, "V7_MANIFEST_CHANGED", "Historical manifest")
    manifest = json.loads(manifest_bytes)
    for item in manifest["files"]:
        data = previous["artwork/" + item["file"]][0]
        require(len(data) == item["bytes"] and sha(data) == item["sha256"], "V7_ASSET_CHANGED", item["file"])
    builder = previous["build_wordmark.py"][0]
    require(sha(builder) == manifest["builder"]["sha256"], "V7_BUILDER_CHANGED", "Historical builder")
    construction_bytes = previous["artwork/construction.json"][0]
    require(sha(construction_bytes) == V7_CONSTRUCTION_SHA, "V7_CONSTRUCTION_CHANGED", "Historical geometry")
    source = json.loads(construction_bytes)
    require(len(source["stroke_by_stroke"]) == 16, "V7_PATH_COUNT_CHANGED", "Expected sixteen source contours")
    if FONTTOOLS_SITE not in sys.path:
        sys.path.append(FONTTOOLS_SITE)
    import fontTools
    from fontTools.pens.boundsPen import BoundsPen
    require(fontTools.__version__ == "4.63.0", "DEPENDENCY_VERSION_MISMATCH", "fontTools")
    node = RUNTIME / "node/bin/node.exe"
    sharp = RUNTIME / "node/node_modules/sharp"
    require(node.is_file() and sharp.is_dir(), "DEPENDENCY_MISSING", "Node or Sharp")
    env = {name: value for name, value in os.environ.items() if name.upper() not in {"NODE_OPTIONS", "NODE_PATH"}}
    probe_code = "const sharp=require(" + json.dumps(str(sharp).replace("\\", "/")) + ");process.stdout.write(JSON.stringify({node:process.version,sharp:sharp.versions.sharp}));"
    probe = subprocess.run([str(node), "-e", probe_code], check=True, capture_output=True, timeout=15, env=env)
    versions = json.loads(probe.stdout)
    require(versions == {"node": "v24.19.0", "sharp": "0.35.4"}, "DEPENDENCY_VERSION_MISMATCH", str(versions))
    progress["preflight_complete"] = True
    return source, previous, sources, {"python": sys.version, "python_executable": sys.executable, "fontTools": fontTools.__version__, **versions}, BoundsPen, node, sharp, env


def M(x, y): return ("moveTo", ((x, y),))
def L(x, y): return ("lineTo", ((x, y),))
def C(a, b, c, d, e, f): return ("curveTo", ((a, b), (c, d), (e, f)))
def Z(): return ("closePath", ())


def refine(source):
    # These are bounded edits of the named V7 strokes; not a replacement font.
    edits = {
        "cha-grass-crossbar": ([M(25,27),C(58,28,109,26,143,23),L(148,30),L(143,34),C(108,38,62,38,26,36),L(22,32),Z()], "草头横画左右回收，整理右端为与作横笔相同的两段转折。"),
        "cha-grass-left-upright": ([M(50,11),L(61,9),C(61,19,60,31,58,41),L(49,44),L(48,39),C(50,29,51,20,50,11),Z()], "草头左竖收短下端，略内收脚部，减少横竖交点边缘的突起。"),
        "cha-grass-right-upright": ([M(114,10),L(126,12),C(124,24,122,34,120,42),L(112,44),L(111,38),C(113,27,114,19,114,10),Z()], "草头右竖左移和收窄，保留原斜势，与左竖的顶底重心对应。"),
        "cha-person-left-fall": ([M(79,48),L(90,53),C(73,70,49,84,19,93),L(13,85),C(40,74,65,61,79,48),Z()], "人部左撇回收左端，保持同一屋顶骨架而减少茶的横向铺开。"),
        "cha-person-right-fall-shared": ([M(85,46),C(104,62,125,75,148,81),C(156,84,164,84,172,81),L(169,89),C(163,93,153,94,144,90),C(123,82,105,69,79,55),Z()], "保留唯一共享右捺，将右端回收7px、下弧收起，缩小与亻撇的交叠肩部。"),
        "cha-wood-crossbar": ([M(42,97),C(69,97,103,95,128,92),L(133,99),L(128,103),C(104,106,71,108,40,107),L(37,102),Z()], "木横画两端回收、右端增加同节奏折面，避开下方撇点起笔处的集中墨量。"),
        "cha-wood-main-shaft": ([M(84,75),L(95,73),C(96,90,95,112,95,128),C(95,137,89,142,76,142),L(62,138),L(65,132),L(78,132),C(83,132,84,127,84,120),Z()], "木主竖局部减薄，浅钩收起2px并回收左端，保留字的竖钩结构。"),
        "cha-wood-left-fall": ([M(64,108),L(71,115),C(59,125,44,133,28,138),L(22,132),C(40,125,53,117,64,108),Z()], "下撇起笔下移4px，缩短左端，整理与横画、主竖之间的开口。"),
        "cha-wood-right-fall": ([M(106,109),L(115,109),C(127,120,139,128,151,132),L(147,142),C(129,136,116,128,103,117),Z()], "右点起笔下移、末端回收5px，放松木部右侧的集中交点，保持与亻竖分开。"),
        "zuo-person-fall-shared": ([M(209,14),L(221,18),C(211,41,193,64,175,82),C(170,87,164,92,157,96),L(151,90),C(164,77,177,60,187,41),C(193,29,198,18,201,13),Z()], "亻撇下端收回，收窄与茶捺相接的宽度；仍为作的完整撇笔。"),
        "zuo-person-upright": ([M(184,73),L(194,75),C(194,94,193,115,192,134),L(186,141),L(180,136),C(183,116,183,92,184,73),Z()], "亻长竖略减重，底部收短2px，保留原倾势与斜切脚部。"),
        "zuo-zha-upper-fall": ([M(251,12),L(263,17),C(256,36,245,53,229,66),L(222,60),C(236,44,244,30,251,12),Z()], "乍上撇顶端下收、底端回收，调整作的视觉高度，保持与上横连接。"),
        "zuo-zha-upper-crossbar": ([M(248,41),C(274,42,308,40,338,36),L(343,43),L(338,47),C(309,51,278,52,242,50),Z()], "上横回收并明确末端两段折面：(+5,+7)、(-5,+4)，弧面延续V7。"),
        "zuo-zha-main-shaft": ([M(261,48),L(273,47),C(272,77,273,109,272,131),L(266,140),L(258,137),C(262,113,261,82,261,48),Z()], "乍主竖收短、减薄，底部不再比茶木钩显著沉重，三条横仍接同一主竖。"),
        "zuo-zha-middle-crossbar": ([M(268,77),C(289,78,312,77,335,74),L(340,81),L(335,85),C(313,89,288,90,268,88),Z()], "中横保留短横角色，收笔转折与上横、下横完全同向同幅。"),
        "zuo-zha-lower-crossbar": ([M(268,107),C(291,108,316,106,340,103),L(345,110),L(340,114),C(315,118,289,120,266,118),Z()], "下横回收右端与下缘，维持略长于中横的原角色，末端折面统一。"),
    }
    strokes = []
    for original in source["stroke_by_stroke"]:
        name = original["id"]
        commands, reason = edits[name]
        if original["character"] == "作":
            commands = [(op, tuple((x+2,y+1) for x,y in points)) for op, points in commands]
            reason += " 作的全部笔画另作(+2,+1)px光学落位，平衡共享肩部字距与基线。"
        stroke = {"id": name, "character": original["character"], "component": original["component"], "stroke": original["stroke"], "commands": commands, "before_v7_commands": copy.deepcopy(original["commands"]), "change_basis": reason, "source_geometry": {"path": "V7/artwork/construction.json", "sha256": V7_CONSTRUCTION_SHA, "source_stroke_id": name}, "origin": "Local refinement of the maker's own originalV7Bezier contours; no font outline or raster trace imported."}
        if "shared_with" in original:
            stroke["shared_with"] = original["shared_with"]
        strokes.append(stroke)
    require(len(strokes) == 16 and len(edits) == 16, "PATH_COUNT_CHANGED", "The sixteen original paths must remain.")
    return strokes


def flatten(commands):
    polygon = []
    current = None
    for op, points in commands:
        if op in ("moveTo", "lineTo"):
            current = points[0]
            polygon.append(current)
        elif op == "curveTo":
            p0 = current
            p1, p2, p3 = points
            for step in range(1,65):
                t = step/64; u = 1-t
                polygon.append(tuple(u*u*u*p0[i]+3*u*u*t*p1[i]+3*u*t*t*p2[i]+t*t*t*p3[i] for i in (0,1)))
            current = p3
    return polygon


def inside(x,y,polygon):
    result = False
    px,py = polygon[-1]
    for qx,qy in polygon:
        if (py>y)!=(qy>y) and x<(qx-px)*(y-py)/(qy-py)+px:
            result = not result
        px,py = qx,qy
    return result


def contacts(strokes):
    shapes = {stroke["id"]: flatten(stroke["commands"]) for stroke in strokes}
    result = []
    for a in (stroke for stroke in strokes if stroke["character"] == "茶"):
        for b in (stroke for stroke in strokes if stroke["character"] == "作"):
            pa,pb = shapes[a["id"]],shapes[b["id"]]
            left,top = max(min(x for x,y in pa),min(x for x,y in pb)),max(min(y for x,y in pa),min(y for x,y in pb))
            right,bottom = min(max(x for x,y in pa),max(x for x,y in pb)),min(max(y for x,y in pa),max(y for x,y in pb))
            if left>=right or top>=bottom: continue
            overlap = []
            for ix in range(math.ceil(left*2),math.floor(right*2)+1):
                for iy in range(math.ceil(top*2),math.floor(bottom*2)+1):
                    x,y = ix/2,iy/2
                    if inside(x,y,pa) and inside(x,y,pb): overlap.append((x,y))
            if overlap:
                result.append({"path_ids":[a["id"],b["id"]],"sampled_bounds_master_px":[min(x for x,y in overlap),min(y for x,y in overlap),max(x for x,y in overlap),max(y for x,y in overlap)],"sampled_area_master_px2":len(overlap)*.25})
    return result


def point_segment_distance(point,a,b):
    x,y = point; ax,ay = a; bx,by = b
    dx,dy = bx-ax,by-ay
    t = max(0,min(1,((x-ax)*dx+(y-ay)*dy)/(dx*dx+dy*dy))) if dx or dy else 0
    return math.hypot(x-ax-t*dx,y-ay-t*dy)


def clearance(a,b):
    def one_way(p,q):
        return min(point_segment_distance(point,q[index-1],end) for point in p for index,end in enumerate(q))
    return min(one_way(a,b),one_way(b,a))


def mechanical_check(source,strokes):
    previous = contacts(source["stroke_by_stroke"])
    current = contacts(strokes)
    expected = {"cha-person-right-fall-shared","zuo-person-fall-shared"}
    require(len(current) == 1 and set(current[0]["path_ids"]) == expected, "STRUCTURAL_CONTACT_CHANGED", "Keep only the original shared stroke pair.")
    shapes = {stroke["id"]:flatten(stroke["commands"]) for stroke in strokes}
    pairs = [("木竖与左撇","cha-wood-main-shaft","cha-wood-left-fall"),("木竖与右点","cha-wood-main-shaft","cha-wood-right-fall"),("茶右点与作亻竖","cha-wood-right-fall","zuo-person-upright"),("草右竖与人右捺","cha-grass-right-upright","cha-person-right-fall-shared"),("乍上横与中横","zuo-zha-upper-crossbar","zuo-zha-middle-crossbar"),("乍中横与下横","zuo-zha-middle-crossbar","zuo-zha-lower-crossbar")]
    gaps = []
    for label,a,b in pairs:
        raw = clearance(shapes[a],shapes[b])
        gaps.append({"opening":label,"path_ids":[a,b],"sampled_minimum_master_px":raw,"at_220px_width":raw*FINAL_SCALE})
    by_id = {stroke["id"]:stroke for stroke in strokes}
    terminal_vectors = {}
    for name in ("zuo-zha-upper-crossbar","zuo-zha-middle-crossbar","zuo-zha-lower-crossbar"):
        commands = by_id[name]["commands"]
        p,q,r = commands[1][1][-1],commands[2][1][0],commands[3][1][0]
        terminal_vectors[name] = [[q[0]-p[0],q[1]-p[1]],[r[0]-q[0],r[1]-q[1]]]
    require(all(value == [[5,7],[-5,4]] for value in terminal_vectors.values()), "TERMINAL_GEOMETRY_MISMATCH", "Three乍terminal turns must match.")
    return {"scope":"Mechanical geometry observations at the requested final220px scale, not aesthetic acceptance.","master_canvas_px":[360,150],"final_width_px":220,"final_vector_height_px":150*FINAL_SCALE,"scale":FINAL_SCALE,"method":"Cubic contours flattened at64 parameter steps; contact areas sampled on0.5px master grid; clearances are nearest sampled-boundary distances.","v7_cross_character_contacts":previous,"v8_cross_character_contacts":current,"shared_area_reduction_master_px2":previous[0]["sampled_area_master_px2"]-current[0]["sampled_area_master_px2"],"openings":gaps,"three_zha_terminal_vectors_master_px":terminal_vectors,"aesthetic_scoring":False}


def path_data(commands):
    letters = {"moveTo":"M","lineTo":"L","curveTo":"C","closePath":"Z"}
    return " ".join(letters[op]+" ".join(f"{value:g}" for point in points for value in point) for op,points in commands)


def assemble(source,strokes,BoundsPen,sources,deps,previous,progress):
    paths,vectors,boxes = [],[],[]
    for stroke in strokes:
        pen = BoundsPen(None)
        require(stroke["commands"][0][0] == "moveTo" and stroke["commands"][-1][0] == "closePath", "PATH_NOT_CLOSED", stroke["id"])
        for op,points in stroke["commands"]: getattr(pen,op)(*points)
        stroke["path_d"] = path_data(stroke["commands"])
        stroke["exact_bounds_px"] = pen.bounds
        boxes.append(pen.bounds)
        paths.append(f'<path id="{stroke["id"]}" data-character="{stroke["character"]}" data-component="{stroke["component"]}" d="{stroke["path_d"]}"/>')
        vectors.append({"name":stroke["id"],"character":stroke["character"],"component":stroke["component"],"windingRule":"NONZERO","data":stroke["path_d"]})
    bounds = [min(b[0] for b in boxes),min(b[1] for b in boxes),max(b[2] for b in boxes),max(b[3] for b in boxes)]
    require(0<=bounds[0]<bounds[2]<=360 and 0<=bounds[1]<bounds[3]<=150, "CANVAS_BOUNDS_INVALID", str(bounds))
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="360" height="150" viewBox="0 0 360 150"><title>茶作</title><desc>One local refinement ofV7. The same16 original contours retain the shared人/亻shoulder and correct character skeleton.</desc><g id="chazuo-refined-shared-shoulder" fill="#F5F2E6" fill-rule="nonzero">'+"".join(paths)+'</g></svg>\n').encode("utf-8")
    require(len(ET.fromstring(svg).findall(".//{http://www.w3.org/2000/svg}path"))==16,"PATH_COUNT_CHANGED","SVG")
    mechanics = mechanical_check(source,strokes)
    construction = {"brand":"茶作","canvas_px":[360,150],"final_width_px":220,"ink_bounds_px":bounds,"retained_structural_relationship":"Same unique茶人right-fall / 作亻left-fall shoulder asV7, with locally reduced overlap.","character_structure":source["character_structure"],"stroke_by_stroke":strokes,"shared_source":"V7original16paths","mechanical_observations":mechanics,"placement":{"x":112,"y":104,"width":220,"height":150*FINAL_SCALE}}
    provenance = {"asset":"OneV8local refinement of theV7wordmark","source_pins":sources,"prior_geometry":{"path":str((V7/'artwork/construction.json').relative_to(REPO)).replace('\\','/'),"sha256":V7_CONSTRUCTION_SHA,"original_path_count":16,"derived_path_count":16,"original_authorship":"V7 maker's originalBezier geometry","v8_authorship":"Per-stroke control-point, terminal and optical-placement edits recorded before/after; not claimed as16freshunrelated paths"},"actual_view_evidence":["view_image originaldetail formalV7poster","view_image originaldetail designatedRupper advertisement","view_image originaldetail frozenSphotography"],"dependencies":deps,"execution":{"thread_id":os.environ.get('CODEX_THREAD_ID'),"fonttools_usage":"BoundsPen only; no fonts loaded","figma_calls":0,"imagegen_calls":0,"business_state_writes":0},"v7_history_preserved":{"files_snapshotted":len(previous),"records":[{"path":name,"sha256":sha(data),"bytes":len(data),"mtime_ns":mtime} for name,(data,mtime) in sorted(previous.items())]},"safety":{"preflight_before_geometry":progress['preflight_complete'],"exclusive_output_directory":str(OUT),"all_artifacts_assembled_in_memory":True,"existing_output_refused":True},"limitations":["Only mechanical identity/spacing is checked by the maker. No taste score orAI_PASS claimed.","Root assembles the poster and an external worker reviews actual pixels."]}
    return {"chazuo-wordmark.svg":svg,"construction.json":encoded(construction),"figma-vector-paths.json":encoded({"width":360,"height":150,"paths":vectors}),"mechanical-220.json":encoded(mechanics)},provenance,bounds


def export(args,progress):
    source,previous,sources,deps,BoundsPen,node,sharp,env = preflight(args,progress)
    builder_bytes = Path(__file__).read_bytes()
    progress['geometry_started'] = True
    assets,provenance,bounds = assemble(source,refine(source),BoundsPen,sources,deps,previous,progress)
    code = "const sharp=require("+json.dumps(str(sharp).replace('\\','/'))+");const chunks=[];process.stdin.on('data',b=>chunks.push(b));process.stdin.on('end',async()=>{try{const b=await sharp(Buffer.concat(chunks)).resize({width:220}).ensureAlpha().png().toBuffer();process.stdout.write(b);}catch(e){process.stderr.write(String(e));process.exitCode=1;}});"
    rendered = subprocess.run([str(node),'-e',code],input=assets['chazuo-wordmark.svg'],capture_output=True,check=True,timeout=20,env=env)
    require(rendered.stdout[:8]==b'\x89PNG\r\n\x1a\n' and struct.unpack('>IIBB',rendered.stdout[16:26])==(220,92,8,6),'PNG_EXPORT_INVALID','Expected220x92RGBA8')
    assets['chazuo-wordmark-220.png'] = rendered.stdout
    provenance['raster_export'] = {'same_unique_svg':True,'preview_dimensions_px':[220,92],'transparent_background':True,'sha256':sha(rendered.stdout)}
    assets['provenance.json'] = encoded(provenance)
    require(source_check(args.photo_path)==sources,'SOURCE_CHANGED_DURING_BUILD','Pinned sources')
    require(history_snapshot()==previous,'V7_HISTORY_CHANGED','All originalV7bytes and mtimes must remain')
    require(Path(__file__).read_bytes()==builder_bytes,'BUILDER_CHANGED','Current builder')
    require(not OUT.exists(),'OUTPUT_EXISTS',str(OUT))
    manifest = {'builder':{'path':'../build_wordmark.py','sha256':sha(builder_bytes),'bytes':len(builder_bytes)},'files':[{'file':name,'sha256':sha(data),'bytes':len(data)} for name,data in sorted(assets.items())],'one_formal_svg':'chazuo-wordmark.svg','one_220px_technical_preview':'chazuo-wordmark-220.png'}
    assets['manifest.json'] = encoded(manifest)
    OUT.mkdir()
    progress['directory_created'] = True
    for name,data in assets.items():
        with (OUT/name).open('xb') as handle: handle.write(data)
        progress['files_created'] += 1
    for name,data in assets.items(): require((OUT/name).read_bytes()==data,'READBACK_MISMATCH',name)
    require(history_snapshot()==previous,'V7_HISTORY_CHANGED','Post-export originalV7byte/mtime comparison')
    return {'result':'exported_one_v8_local_refinement',**progress,'directory':str(OUT),'master_dimensions':[360,150],'final_width':220,'editable_contours':16,'ink_bounds':bounds,'svg_sha256':sha(assets['chazuo-wordmark.svg']),'png_sha256':sha(rendered.stdout),'manifest_sha256':sha(assets['manifest.json']),'v7_files_byte_and_mtime_unchanged':len(previous),'aesthetic_acceptance_claimed':False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--photo-path',help='Read-only negative source probe; fixedSsha remains mandatory')
    args = parser.parse_args()
    progress = {'preflight_complete':False,'geometry_started':False,'directory_created':False,'files_created':0}
    try:
        report = export(args,progress); code = 0
    except ExportError as exc:
        report = {'result':'rejected','code':exc.code,'detail':str(exc),**progress}; code = 2
    except (OSError,ImportError,ValueError,KeyError,subprocess.SubprocessError) as exc:
        report = {'result':'rejected','code':'EXECUTION_ERROR','detail':f'{type(exc).__name__}: {exc}',**progress}; code = 2
    print(json.dumps(report,ensure_ascii=True,indent=2))
    return code


if __name__=='__main__': raise SystemExit(main())
