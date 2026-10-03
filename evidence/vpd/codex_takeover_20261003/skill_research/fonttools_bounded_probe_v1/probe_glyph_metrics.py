"""Read-only glyph engineering probe. Writes JSON, never SVG/PNG/PDF or fonts."""
from pathlib import Path
import argparse
from collections import Counter
import hashlib
import json
import sys
import time
import fontTools
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen, ControlBoundsPen
from fontTools.pens.statisticsPen import StatisticsPen
from fontTools.pens.recordingPen import RecordingPen

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

parser = argparse.ArgumentParser()
parser.add_argument("--font", type=Path, required=True)
parser.add_argument("--text", default="茶作")
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
start = time.perf_counter()
sample_hash_before = sha256(args.font)
font = TTFont(args.font, lazy=False)
glyphset = font.getGlyphSet()
cmap = font.getBestCmap()
units = font["head"].unitsPerEm
result = {
    "status": "ENGINEERING_DIAGNOSTIC_ONLY_NOT_AESTHETIC_PASS",
    "fixed_project_source_commit": "003cfdfaa6481f8ac41cc46f56539bb4782ec34b",
    "experiment": "same text/font/weight; compare advance-box baseline with exact Bezier contour bounds",
    "font_path": str(args.font.resolve()), "font_sha256": sample_hash_before,
    "text": args.text, "fonttools_version": fontTools.__version__,
    "python": sys.version, "python_executable": sys.executable,
    "font_family": font["name"].getDebugName(1), "font_version_name": font["name"].getDebugName(5),
    "units_per_em": units, "missing_codepoints": [], "glyphs": [],
    "limitations": [
        "cmap lookup is not OpenType shaping; HarfBuzz was not installed or executed",
        "signed contour area/centroid is not necessarily the union-of-ink area for overlapping outlines",
        "these metrics cannot establish a preferred spacing, identity, premium feel or custom wordmark quality",
        "no glyph outline changed; no finished artwork, raster, SVG, or font was created",
    ],
}
for char in args.text:
    name = cmap.get(ord(char))
    if name is None:
        result["missing_codepoints"].append(f"U+{ord(char):04X}")
        continue
    glyph = glyphset[name]
    exact = BoundsPen(glyphset)
    control = ControlBoundsPen(glyphset)
    stats = StatisticsPen(glyphset)
    recording = RecordingPen()
    for pen in (exact, control, stats, recording):
        glyph.draw(pen)
    advance, nominal_lsb = font["hmtx"][name]
    bbox = exact.bounds
    x0, y0, x1, y1 = bbox
    result["glyphs"].append({
        "character": char, "codepoint": f"U+{ord(char):04X}", "glyph_name": name,
        "advance_units": advance, "nominal_lsb_units": nominal_lsb,
        "exact_contour_bounds_units": list(bbox), "control_bounds_units": list(control.bounds),
        "contour_width_em": (x1 - x0) / units, "contour_height_em": (y1 - y0) / units,
        "actual_left_space_units": x0, "actual_right_space_units": advance - x1,
        "signed_contour_area_em2": stats.area / (units * units),
        "signed_contour_centroid_em": [stats.meanX / units, stats.meanY / units],
        "bbox_center_em": [(x0 + x1) / (2 * units), (y0 + y1) / (2 * units)],
        "path_operation_counts": dict(Counter(op for op, _ in recording.value)),
    })
font.close()
assert sha256(args.font) == sample_hash_before, "Read-only input changed unexpectedly"
result["font_hash_unchanged"] = True
result["elapsed_seconds"] = round(time.perf_counter() - start, 6)
args.output.parent.mkdir(parents=True, exist_ok=True)
with args.output.open("x", encoding="utf-8") as stream:
    json.dump(result, stream, ensure_ascii=False, indent=2)
print(json.dumps(result, ensure_ascii=False, indent=2))
