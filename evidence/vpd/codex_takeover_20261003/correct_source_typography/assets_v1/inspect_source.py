"""Read the licensed source, preserve its exact contour basis, render source only."""
from pathlib import Path
import hashlib
import json
import sys

sys.dont_write_bytecode = True
sys.path.append(r"C:/Users/Administrator/AppData/Local/hermes/hermes-agent/venv/Lib/site-packages")
import fontTools
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.svgPathPen import SVGPathPen

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
PRIVATE = ROOT / ".liu-visual-private/correct_source_typography/lettering_v1"
FONT = ROOT / "evidence/vpd/codex_takeover_20261003/skill_research/fonttools_bounded_probe_v1/upstream/adobe-fonts/source-han-serif/OTF/SimplifiedChinese/SourceHanSerifSC-Regular.otf"
LICENSE = FONT.parents[2] / "LICENSE.txt"
PHOTO = ROOT / ".liu-visual-private/source_recovery_20261003/photography-local-reconstruction-final.png"
REF = ROOT / ".liu-visual-private/reference.jpg"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

font = TTFont(FONT)
glyphset = font.getGlyphSet()
cmap = font.getBestCmap()
records = []
for ch in "\u8336\u4f5c\u4e00\u676f\uff0c\u6162\u4e0b\u6765":
    name = cmap[ord(ch)]
    bound = BoundsPen(glyphset)
    rec = RecordingPen()
    svg = SVGPathPen(glyphset)
    for pen in (bound, rec, svg):
        glyphset[name].draw(pen)
    records.append({
        "character": ch, "codepoint": f"U+{ord(ch):04X}", "glyph_name": name,
        "exact_bounds_font_units": bound.bounds,
        "advance_and_lsb_font_units": font["hmtx"][name],
        "recording_pen_commands": rec.value,
        "source_svg_path_d": svg.getCommands(),
    })

document = {
    "purpose": "Correct source glyph structure, headline outline source, and actual geometry basis. These source contours are not the custom logo.",
    "font": {
        "path": str(FONT.relative_to(ROOT)).replace("\\", "/"),
        "sha256": sha(FONT), "bytes": FONT.stat().st_size,
        "family": font["name"].getDebugName(1), "version": font["name"].getDebugName(5),
        "units_per_em": font["head"].unitsPerEm,
        "copyright": font["name"].getDebugName(0),
        "license": "SIL Open Font License 1.1",
        "license_source_path": str(LICENSE.relative_to(ROOT)).replace("\\", "/"),
        "license_sha256": sha(LICENSE),
    },
    "fonttools": {"version": fontTools.__version__, "runtime_file": fontTools.__file__, "methods_executed": ["TTFont.getBestCmap", "TTFont.getGlyphSet", "BoundsPen", "RecordingPen", "SVGPathPen"]},
    "actual_input_identity": {"photography_sha256": sha(PHOTO), "reference_sha256": sha(REF)},
    "glyphs": records,
}
OUT.mkdir(parents=True, exist_ok=True)
PRIVATE.mkdir(parents=True, exist_ok=True)
(OUT / "source_geometry.json").write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(OUT / "SOURCE_HAN_SERIF_OFL.txt").write_bytes(LICENSE.read_bytes())

source_paths = []
for i, record in enumerate(records[:2]):
    source_paths.append(f'<path data-character="{record["character"]}" transform="translate({45 + i*560} 560) scale(.5 -.5)" d="{record["source_svg_path_d"]}"/>')
source_svg = '<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="620" viewBox="0 0 1120 620"><title>Original Source Han Serif SC Regular glyph structure reference; not custom lettering</title><rect width="1120" height="620" fill="#fff"/><g fill="#111">' + ''.join(source_paths) + '</g></svg>'
(OUT / "original_glyph_reference.svg").write_text(source_svg, encoding="utf-8")

print(json.dumps({"fonttools": fontTools.__version__, "source_font_sha256": sha(FONT), "photography_sha256": sha(PHOTO), "source_geometry": str(OUT / "source_geometry.json"), "source_reference": str(OUT / "original_glyph_reference.svg")}, ensure_ascii=True, indent=2))
