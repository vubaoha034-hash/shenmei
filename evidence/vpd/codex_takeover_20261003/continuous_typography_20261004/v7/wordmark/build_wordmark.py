"""Export one original V7 茶作 wordmark into an exclusively new directory.

All source/dep/output preflight checks finish before geometry or rasterization.
Outputs are assembled in memory, sources are checked again, then the directory
and every file are created exclusively. Historical assets are never output paths.
"""
from __future__ import annotations

import argparse
import hashlib
import json
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
RUNTIME = Path("C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies")
FONTTOOLS_SITE = "C:/Users/Administrator/AppData/Local/hermes/hermes-agent/venv/Lib/site-packages"
SOURCES = {
    "photography": (".liu-visual-private/source_recovery_20261003/photography-local-reconstruction-final.png", "7fd7777fed21100cb6b47bc305701476054263565e73246ac469d065aa080618"),
    "reference": (".liu-visual-private/reference.jpg", "87a28f5cd4b5d15b01e6536206127c357043a904b3c0dab3bfa0c50080782167"),
    "formal_v6": (".liu-visual-private/correct_source_typography/v6/poster.png", "150d778dedd39e170943617b062df153ca3096c91b46cf475ab450ee889bfdd2"),
}


class ExportError(Exception):
    def __init__(self, code, detail):
        super().__init__(detail)
        self.code = code


def require(condition, code, detail):
    if not condition:
        raise ExportError(code, detail)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encode_json(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def source_preflight(photo_override=None):
    records = {}
    for name, (relative, expected) in SOURCES.items():
        data = (REPO / relative).read_bytes()
        require(sha(data) == expected, "SOURCE_SHA_MISMATCH", name)
        records[name] = {"path": relative, "sha256": expected, "bytes": len(data)}
    if photo_override:
        supplied = Path(photo_override).resolve()
        require(sha(supplied.read_bytes()) == SOURCES["photography"][1], "SOURCE_SHA_MISMATCH", "photography override")
    return records


def preflight(photo_override, progress):
    sources = source_preflight(photo_override)
    require(not OUT.exists(), "OUTPUT_EXISTS", f"Refusing any overwrite: {OUT}")
    require(OUT.parent == HERE and HERE.is_dir(), "OUTPUT_SCOPE_INVALID", str(OUT))
    if FONTTOOLS_SITE not in sys.path:
        sys.path.append(FONTTOOLS_SITE)
    import fontTools
    from fontTools.pens.boundsPen import BoundsPen
    require(fontTools.__version__ == "4.63.0", "DEPENDENCY_VERSION_MISMATCH", "fontTools")
    node = RUNTIME / "node/bin/node.exe"
    sharp = RUNTIME / "node/node_modules/sharp"
    require(node.is_file() and sharp.is_dir(), "DEPENDENCY_MISSING", "Bundled Node or Sharp")
    env = {name: value for name, value in os.environ.items() if name.upper() not in {"NODE_OPTIONS", "NODE_PATH"}}
    code = "const sharp=require(" + json.dumps(str(sharp).replace("\\", "/")) + ");process.stdout.write(JSON.stringify({node:process.version,sharp:sharp.versions.sharp}));"
    probe = subprocess.run([str(node), "-e", code], check=True, capture_output=True, timeout=15, env=env)
    versions = json.loads(probe.stdout)
    require(versions == {"node": "v24.19.0", "sharp": "0.35.4"}, "DEPENDENCY_VERSION_MISMATCH", str(versions))
    progress["preflight_complete"] = True
    return sources, {"python": sys.version, "python_executable": sys.executable, "fontTools": fontTools.__version__, **versions}, BoundsPen, node, sharp, env


def M(x, y): return ("moveTo", ((x, y),))
def L(x, y): return ("lineTo", ((x, y),))
def C(a, b, c, d, e, f): return ("curveTo", ((a, b), (c, d), (e, f)))
def Z(): return ("closePath", ())


def authored_geometry():
    """Sixteen fresh contours. Coordinates are final SVG pixels, not font units."""
    return [
        {"id": "cha-grass-crossbar", "character": "茶", "component": "艹", "stroke": "横", "commands": [M(23, 26), C(57, 27, 112, 25, 149, 21), L(155, 29), L(149, 33), C(112, 37, 61, 38, 22, 35), L(17, 31), Z()], "basis": "Original shallow bowed grass crossbar; its interior top edge leaves room for the two verticals rather than adding a botanical pictogram."},
        {"id": "cha-grass-left-upright", "character": "茶", "component": "艹", "stroke": "左竖", "commands": [M(49, 9), L(61, 7), C(62, 17, 61, 31, 59, 42), L(49, 46), L(47, 40), C(50, 29, 50, 19, 49, 9), Z()], "basis": "Original 12px top-to-10px lower shaft; the grass stem is slightly inset, with an angled foot, and remains a genuine艹stroke."},
        {"id": "cha-grass-right-upright", "character": "茶", "component": "艹", "stroke": "右竖", "commands": [M(116, 8), L(129, 10), C(126, 23, 124, 33, 122, 42), L(112, 45), L(111, 39), C(114, 27, 115, 18, 116, 8), Z()], "basis": "Original independently drawn second草stem, with its own balanced inward lean; no rotated copy of a V5 path."},
        {"id": "cha-person-left-fall", "character": "茶", "component": "人", "stroke": "撇", "commands": [M(79, 47), L(91, 52), C(72, 71, 46, 85, 15, 95), L(9, 85), C(39, 74, 65, 60, 79, 47), Z()], "basis": "Original tapered roof-left stroke. Its apex overlaps the roof-right start to preserve the人construction."},
        {"id": "cha-person-right-fall-shared", "character": "茶", "component": "人", "stroke": "捺，与作亻撇嵌合", "shared_with": "zuo-person-fall-shared", "commands": [M(85, 45), C(104, 61, 126, 73, 151, 79), C(158, 82, 166, 82, 179, 79), L(176, 90), C(167, 97, 153, 97, 142, 92), C(121, 83, 103, 69, 78, 54), Z()], "basis": "Original roof-right contour curves into the left-fall of作at the intercharacter shoulder. This is a real人right stroke joined to a real亻left stroke; its bowl-like lower arc is the character's own outline, not an added symbol."},
        {"id": "cha-wood-crossbar", "character": "茶", "component": "木", "stroke": "横", "commands": [M(39, 95), C(69, 95, 105, 92, 135, 89), L(138, 97), C(108, 104, 70, 107, 36, 105), L(33, 100), Z()], "basis": "Original rising木crossbar. Its thickness and sweep support the lower component without repeating a uniform bar template."},
        {"id": "cha-wood-main-shaft", "character": "茶", "component": "木", "stroke": "竖钩", "commands": [M(84, 74), L(96, 71), C(97, 88, 96, 112, 96, 128), C(96, 138, 90, 143, 74, 144), L(59, 139), L(62, 132), L(77, 132), C(83, 132, 84, 127, 84, 120), Z()], "basis": "Original subtly modulated central木shaft with a shallow left hook. The hook stays within茶and is not used to connect the two words."},
        {"id": "cha-wood-left-fall", "character": "茶", "component": "木", "stroke": "撇", "commands": [M(65, 104), L(73, 112), C(60, 123, 43, 133, 25, 138), L(18, 131), C(39, 124, 53, 115, 65, 104), Z()], "basis": "Original lower-left stroke with an open angled tip, balancing the longer人roof above."},
        {"id": "cha-wood-right-fall", "character": "茶", "component": "木", "stroke": "捺/右点", "commands": [M(104, 103), L(114, 102), C(126, 115, 140, 124, 156, 129), L(151, 141), C(131, 137, 116, 126, 101, 112), Z()], "basis": "Original lower-right stroke, kept separate from the interlocking shoulder and the作vertical so木remains open and legible."},
        {"id": "zuo-person-fall-shared", "character": "作", "component": "亻", "stroke": "撇，与茶人部捺嵌合", "shared_with": "cha-person-right-fall-shared", "commands": [M(209, 12), L(222, 17), C(212, 41, 195, 64, 177, 83), C(171, 90, 162, 97, 150, 102), L(142, 96), C(157, 80, 175, 61, 185, 41), C(192, 29, 196, 18, 198, 11), Z()], "basis": "Original亻falling stroke reaches into the existing茶right-roof contour, forming the only intercharacter contact. Its head and descending direction still construct作rather than an isolated ornament."},
        {"id": "zuo-person-upright", "character": "作", "component": "亻", "stroke": "竖", "commands": [M(184, 70), L(195, 72), C(195, 91, 194, 114, 193, 134), L(186, 143), L(180, 137), C(183, 116, 183, 91, 184, 70), Z()], "basis": "Original long亻vertical touches its own falling stroke at the shoulder and retains a visible lower opening from茶木."},
        {"id": "zuo-zha-upper-fall", "character": "作", "component": "乍", "stroke": "上撇", "commands": [M(251, 9), L(264, 14), C(257, 34, 245, 53, 228, 67), L(220, 60), C(235, 44, 243, 27, 251, 9), Z()], "basis": "Original short乍head stroke, clearly distinguished from the longer亻stroke. It joins the乍upper crossbar as required by the character."},
        {"id": "zuo-zha-upper-crossbar", "character": "作", "component": "乍", "stroke": "上横", "commands": [M(248, 39), C(275, 40, 310, 38, 342, 34), L(347, 42), L(342, 47), C(312, 51, 278, 52, 242, 49), Z()], "basis": "Original longest upper crossbar. The gently curved surfaces and angled end support a clear乍structure without cloning the茶horizontal."},
        {"id": "zuo-zha-main-shaft", "character": "作", "component": "乍", "stroke": "竖", "commands": [M(260, 47), L(274, 45), C(272, 80, 273, 111, 273, 132), L(266, 143), L(256, 139), C(261, 116, 260, 82, 260, 47), Z()], "basis": "Original modulated main乍shaft. It has a visual mass related to茶木but a distinct stance determined by its own three crossbars."},
        {"id": "zuo-zha-middle-crossbar", "character": "作", "component": "乍", "stroke": "中横", "commands": [M(271, 76), C(293, 77, 317, 75, 337, 72), L(341, 81), L(337, 86), C(315, 89, 291, 89, 269, 87), Z()], "basis": "Original shorter middle crossbar, leaving the middle/lower aperture open and avoiding equal-length mechanical striping."},
        {"id": "zuo-zha-lower-crossbar", "character": "作", "component": "乍", "stroke": "下横", "commands": [M(270, 106), C(295, 107, 320, 105, 345, 102), L(349, 112), L(343, 117), C(316, 119, 291, 120, 268, 117), Z()], "basis": "Original lower crossbar, slightly fuller than the middle bar to balance the grass-heavy茶and keep the paired baseline stable."},
    ]


def data_string(commands):
    symbols = {"moveTo": "M", "lineTo": "L", "curveTo": "C", "closePath": "Z"}
    return " ".join(symbols[op] + " ".join(f"{value:g}" for point in points for value in point) for op, points in commands)


def assemble(strokes, BoundsPen, sources, dependencies, progress):
    svg_paths, vectors, boxes = [], [], []
    for stroke in strokes:
        pen = BoundsPen(None)
        for op, points in stroke["commands"]:
            getattr(pen, op)(*points)
        require(stroke["commands"][0][0] == "moveTo" and stroke["commands"][-1][0] == "closePath", "PATH_NOT_CLOSED", stroke["id"])
        stroke["path_d"] = data_string(stroke["commands"])
        stroke["exact_bounds_px"] = pen.bounds
        stroke["origin"] = "Newly authored explicit Bezier/line control geometry. No font, raster trace or prior-version path was imported."
        boxes.append(pen.bounds)
        svg_paths.append(f'<path id="{stroke["id"]}" data-character="{stroke["character"]}" data-component="{stroke["component"]}" d="{stroke["path_d"]}"/>')
        vectors.append({"name": stroke["id"], "character": stroke["character"], "component": stroke["component"], "windingRule": "NONZERO", "data": stroke["path_d"]})
    ink = [min(box[0] for box in boxes), min(box[1] for box in boxes), max(box[2] for box in boxes), max(box[3] for box in boxes)]
    require(0 <= ink[0] < ink[2] <= 360 and 0 <= ink[1] < ink[3] <= 150, "CANVAS_BOUNDS_INVALID", str(ink))
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="360" height="150" viewBox="0 0 360 150">'
           '<title>茶作</title><desc>Original two-character wordmark. The right-fall of 茶 人 and the left-fall of 作 亻 share an interlocking shoulder. All contours remain individually editable.</desc>'
           '<g id="chazuo-shared-shoulder-wordmark" fill="#F5F2E6" fill-rule="nonzero">' + "".join(svg_paths) + '</g></svg>\n').encode("utf-8")
    tree = ET.fromstring(svg)
    require(len(tree.findall(".//{http://www.w3.org/2000/svg}path")) == 16, "PATH_COUNT_INVALID", "Expected sixteen original contours.")
    construction = {
        "brand": "茶作", "canvas_px": [360, 150], "ink_bounds_px": ink,
        "unique_structural_decision": "茶人部的右捺与作亻的撇形成两字间唯一嵌合肩部；下部保持开口。识别关系由字的真实笔画产生，没有外加图形。",
        "structural_contact": {"path_ids": ["cha-person-right-fall-shared", "zuo-person-fall-shared"], "design_region_px": [142, 79, 179, 102], "ink_relation": "Two actual strokes overlap at one shoulder, while their per-stroke editable contours preserve the complete character construction."},
        "character_structure": {"茶": "艹3 + 人2 + 木4 separate editable contours", "作": "亻2 + 乍5 separate editable contours"},
        "open_spaces": {"below_shared_shoulder": "茶木右点 terminates at x156; 作亻shaft starts to its right at x180 and continues down independently.", "zha_apertures": "乍 retains distinct upper/middle/lower bars with unequal lengths; their openings come from the character skeleton."},
        "surface_and_weight": "Main shafts are roughly12–15px with gradual contour modulation; horizontals have different masses determined by their character role. Curved bodies end in drawn angled faces, not round caps or a uniform-cut template.",
        "stroke_by_stroke": strokes,
        "placement_suggestion": {"x": 112, "y": 104, "width": 360, "height": 150, "purpose": "Above the tea-bowl side in the dark upper left; final poster assembly belongs to root."},
    }
    methods = {
        "primary_method_sources": [
            {"url": "https://glyphsapp.com/learn/drawing-good-paths", "applied": "Explicit corner nodes and separate smooth cubic surfaces; contours close without texture fragments."},
            {"url": "https://handbook.glyphsapp.com/drawing-paths/", "applied": "Original on-curve nodes/off-curve cubic handles, with editable stroke components."},
            {"url": "https://developers.figma.com/docs/plugins/api/properties/VectorPath-data/", "applied": "Only supported absoluteM/L/C/Z path strings with NONZERO fill information."},
        ],
        "actual_tools": "Python and fontTools BoundsPen calculate geometry; Sharp rasterizes the same SVG only in memory. This maker did not call Figma or Glyphs desktop.",
        "sources_of_character_shape": "Original controls in this builder, using the stated Chinese character skeleton. No font outline files loaded and no older wordmark geometry read.",
    }
    provenance = {
        "asset": "One original V7茶作 wordmark", "sources": sources,
        "actual_view_evidence": ["view_image originaldetail: frozen photography", "view_image originaldetail: designatedreference upper advertisement", "view_image originaldetail: formalV6poster"],
        "dependencies": dependencies, "execution": {"thread_id": os.environ.get("CODEX_THREAD_ID"), "fonttools_use": "BoundsPen only; no font loading", "figma_calls": 0, "glyphs_app_calls": 0, "imagegen_calls": 0, "business_state_writes": 0},
        "authorship": {"font_outline_imports": 0, "prior_wordmark_path_imports": 0, "raster_traces": 0, "original_editable_contours": 16},
        "safety": {"all_preflight_before_geometry": progress["preflight_complete"], "outputs_assembled_in_memory": True, "exclusive_output_directory": str(OUT), "existing_output_rejected": True, "files_exclusively_created": True},
        "limitations": ["This export establishes a single editable asset, not aesthetic acceptance.", "Root handles title hierarchy and poster placement; an independent reviewer evaluates the assembled poster."],
    }
    return {"chazuo-wordmark.svg": svg, "construction.json": encode_json(construction), "figma-vector-paths.json": encode_json({"width": 360, "height": 150, "ink_bounds_px": ink, "paths": vectors}), "method_basis.json": encode_json(methods)}, provenance, ink


def export(args, progress):
    sources, dependencies, bounds_pen, node, sharp, env = preflight(args.photo_path, progress)
    builder_bytes = Path(__file__).read_bytes()
    progress["geometry_started"] = True
    assets, provenance, ink = assemble(authored_geometry(), bounds_pen, sources, dependencies, progress)
    # Rasterization cannot touch any disk image: both stdin and stdout are bytes.
    code = ("const sharp=require(" + json.dumps(str(sharp).replace("\\", "/")) + ");const chunks=[];process.stdin.on('data',b=>chunks.push(b));"
            "process.stdin.on('end',async()=>{try{const b=await sharp(Buffer.concat(chunks)).ensureAlpha().png().toBuffer();process.stdout.write(b);}catch(e){process.stderr.write(String(e));process.exitCode=1;}});")
    rendered = subprocess.run([str(node), "-e", code], input=assets["chazuo-wordmark.svg"], capture_output=True, check=True, timeout=20, env=env)
    require(rendered.stdout[:8] == b"\x89PNG\r\n\x1a\n", "PNG_EXPORT_INVALID", "Sharp did not return a PNG.")
    require(rendered.stdout[12:16] == b"IHDR" and struct.unpack(">IIBB", rendered.stdout[16:26]) == (360, 150, 8, 6), "PNG_EXPORT_INVALID", "Expected360x150 RGBA8 transparent preview.")
    assets["chazuo-wordmark.png"] = rendered.stdout
    provenance["raster_export"] = {"source": "same uniqueSVG in memory", "width": 360, "height": 150, "transparent_background": True, "png_sha256": sha(rendered.stdout)}
    assets["provenance.json"] = encode_json(provenance)
    require(source_preflight(args.photo_path) == sources, "SOURCE_CHANGED_DURING_BUILD", "Source bindings changed.")
    require(Path(__file__).read_bytes() == builder_bytes, "BUILDER_CHANGED_DURING_BUILD", "Builder changed before export.")
    require(not OUT.exists(), "OUTPUT_EXISTS", f"Refusing any overwrite: {OUT}")
    manifest = {"builder": {"path": "../build_wordmark.py", "sha256": sha(builder_bytes), "bytes": len(builder_bytes)}, "files": [{"file": name, "sha256": sha(data), "bytes": len(data)} for name, data in sorted(assets.items())], "one_formal_svg": "chazuo-wordmark.svg", "one_transparent_preview": "chazuo-wordmark.png"}
    assets["manifest.json"] = encode_json(manifest)
    OUT.mkdir()  # Atomic exclusive directory reservation; no parents/no exist_ok.
    progress["directory_created"] = True
    for name, data in assets.items():
        with (OUT / name).open("xb") as handle:
            handle.write(data)
        progress["files_created"] += 1
    for name, data in assets.items():
        require((OUT / name).read_bytes() == data, "EXPORT_READBACK_MISMATCH", name)
    return {"result": "exported_one_original_wordmark", **progress, "directory": str(OUT), "dimensions": [360, 150], "ink_bounds_px": ink, "editable_contours": 16, "svg_sha256": sha(assets["chazuo-wordmark.svg"]), "png_sha256": sha(assets["chazuo-wordmark.png"]), "manifest_sha256": sha(assets["manifest.json"]), "aesthetic_acceptance_claimed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--photo-path", help="Read-only negative source probe; fixed photograph SHA remains mandatory.")
    args = parser.parse_args()
    progress = {"preflight_complete": False, "geometry_started": False, "directory_created": False, "files_created": 0}
    try:
        report = export(args, progress)
        code = 0
    except ExportError as exc:
        report = {"result": "rejected", "code": exc.code, "detail": str(exc), **progress}
        code = 2
    except (OSError, ImportError, ValueError, subprocess.SubprocessError) as exc:
        report = {"result": "rejected", "code": "EXECUTION_ERROR", "detail": f"{type(exc).__name__}: {exc}", **progress}
        code = 2
    print(json.dumps(report, ensure_ascii=True, indent=2))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
