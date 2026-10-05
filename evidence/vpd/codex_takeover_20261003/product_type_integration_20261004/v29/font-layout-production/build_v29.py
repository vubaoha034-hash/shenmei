"""One private V29 production trial. No photography or source outline editing.

Run with the already installed bundled Python:
  python.exe -X utf8 build_v29.py
Only this script's private directory is an output destination.
"""
from __future__ import annotations

import PIL  # Keep bundled Pillow before appending the existing FontTools environment.
from PIL import Image
import sys
from pathlib import Path

FONTTOOLS_SITE = Path("C:/Users/Administrator/AppData/Local/hermes/hermes-agent/venv/Lib/site-packages")
sys.path.append(str(FONTTOOLS_SITE))

import fontTools
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
import copy
import datetime as dt
import hashlib
import json
import platform
import subprocess
import xml.etree.ElementTree as ET
from xml.sax.saxutils import quoteattr

OUT = Path(__file__).resolve().parent
BASE = OUT.parents[1]
assert OUT.name == "shanyeji-v29-production" and OUT.parent.name == ".liu-visual-private"
W, H = 1536, 1024
INPUTS = {
    "reference": {
        "path": ".liu-visual-private/product-type-integration-20261004/SHANYEJI-canonical-readback-20261005.jpg",
        "sha256": "9a29fbdc7dd908017924bed270e8dfe18351519eed3fa7bc7001789f2a383414",
    },
    "photography": {
        "path": ".liu-visual-private/source_recovery_20261003/photography-local-reconstruction-final.png",
        "sha256": "7fd7777fed21100cb6b47bc305701476054263565e73246ac469d065aa080618",
    },
    "brand": {
        "path": "evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v21/brand.svg",
        "sha256": "dd8e9e899393dc36eb3f5b1652bdbb740787d41a108ea6aa1eae05cb1368b1ff",
    },
    "provenance": {
        "path": "evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v21/ASSET_PROVENANCE.json",
    },
}
NODE = Path("C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe")
SHARP = "C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp"
COPY = {
    "brand": "茶作",
    "headline": "一杯茶，慢下来",
    "description": "煮水、沏茶，把一刻留给自己。",
    "english_hint": "TEA FOR SLOW DAYS",
}
LAYOUT = {
    "canvas": [W, H],
    "brand": {"ink_x": 140, "ink_y": 100, "uniform_visible_width": 340, "fill_inherited": "#F5F2E6"},
    "headline": {"ink_x": 140, "ink_top": 303, "font_size_px": 60, "tracking_px": 0.6,
                 "advance_overrides_px": {"，": 31}, "fill": "#E5E4D4"},
    "description": {"ink_x": 140, "ink_top": 391, "font_size_px": 22, "tracking_px": 0.25,
                    "advance_overrides_px": {"、": 12, "，": 11, "。": 12}, "fill": "#C1C6B1"},
    "english_hint": {"ink_x": 140, "ink_top": 433, "font_size_px": 18, "tracking_px": 1.2,
                     "advance_overrides_px": {}, "fill": "#BE9861",
                     "pair_adjustments_px": {"TE": -0.4, "EA": -0.3, "FO": -0.3, "DA": -0.2, "AY": -0.5}},
    "photography_guard_y": 455,
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest(p: Path) -> str:
    return sha(p.read_bytes())


def write(name: str, content: str | bytes) -> Path:
    p = OUT / name
    assert p.resolve().parent == OUT
    if isinstance(content, bytes):
        p.write_bytes(content)
    else:
        p.write_text(content, encoding="utf-8", newline="\n")
    return p


def json_text(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + "\n"


def numbers(v) -> str:
    return " ".join(format(float(x), ".12g") for x in v)


def svg_document(title: str, content: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<title>{title}</title>\n{content}\n</svg>\n')


def changed_pixel_count(a: Image.Image, b: Image.Image) -> int:
    assert a.mode == b.mode and a.size == b.size
    return sum(x != y for x, y in zip(a.getdata(), b.getdata()))


def main() -> None:
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    for key, item in INPUTS.items():
        p = BASE / item["path"]
        actual = digest(p)
        if "sha256" in item:
            assert actual == item["sha256"], f"Incorrect {key} identity"
        item["sha256"] = actual
        item["bytes"] = p.stat().st_size

    provenance = json.loads((BASE / INPUTS["provenance"]["path"]).read_text(encoding="utf-8"))
    font_item = copy.deepcopy(provenance["font_foundation"])
    license_item = copy.deepcopy(provenance["font_license"])
    assert digest(BASE / font_item["path"]) == font_item["sha256"]
    assert font_item["sha256"] == "78aa7a328fd974df2d688c8a9fd74a33d8334dfa84ab24d9d11efb2ffc464117"
    assert digest(BASE / license_item["path"]) == license_item["sha256"]
    font = TTFont(BASE / font_item["path"], lazy=True)
    glyphset = font.getGlyphSet()
    cmap = font.getBestCmap()
    upem = font["head"].unitsPerEm
    assert upem == 1000
    font_version = [n.toUnicode() for n in font["name"].names if n.nameID == 5]
    assert "Version 2.003;hotconv 1.1.1;makeotfexe 2.6.0" in font_version

    source_brand = (BASE / INPUTS["brand"]["path"]).read_text(encoding="utf-8")
    src_tree = ET.fromstring(source_brand)
    ns = {"s": "http://www.w3.org/2000/svg"}
    original_paths = src_tree.findall(".//s:path", ns)
    assert len(original_paths) == 7
    assert all(p.attrib["fill"] == "#F5F2E6" for p in original_paths)
    prohibited = {"image", "mask", "filter", "clipPath", "text", "use", "foreignObject"}
    assert not any(e.tag.rsplit("}", 1)[-1] in prohibited for e in src_tree.iter())
    viewbox = [float(n) for n in src_tree.attrib["viewBox"].split()]
    assert viewbox[:2] == [0, 0]
    brand_scale = LAYOUT["brand"]["uniform_visible_width"] / viewbox[2]
    brand_affine = [brand_scale, 0, 0, brand_scale, 140, 100]
    # The complete inner source is retained verbatim; its original group and per-path transforms remain.
    raw_brand_inner = source_brand[source_brand.index(">") + 1:source_brand.rindex("</svg>")]
    brand_content = f'<g id="chazuo-brand-placement" transform="matrix({numbers(brand_affine)})">\n{raw_brand_inner}\n</g>'
    brand_svg = svg_document("茶作 — inherited seven source paths", brand_content)
    brand_p = write("brand.svg", brand_svg)
    out_tree = ET.fromstring(brand_svg)
    output_brand_paths = out_tree.findall(".//s:path", ns)
    assert [p.attrib for p in original_paths] == [p.attrib for p in output_brand_paths]

    glyph_sources = {}
    line_evidence = []
    aux_content = []

    def get_source(char: str):
        if char in glyph_sources:
            return glyph_sources[char]
        glyph_name = cmap[ord(char)]
        glyph = glyphset[glyph_name]
        recording = RecordingPen()
        glyph.draw(recording)
        # No transformed, synthetic or hand-authored command is supplied to the SVGPathPen.
        svgpen = SVGPathPen(glyphset)
        recording.replay(svgpen)
        commands = svgpen.getCommands()
        verify_pen = SVGPathPen(glyphset)
        glyph.draw(verify_pen)
        assert commands == verify_pen.getCommands()
        assert not any(op == "addComponent" for op, _ in recording.value)
        bounds = BoundsPen(glyphset)
        recording.replay(bounds)
        recording_bytes = json.dumps(recording.value, separators=(",", ":")).encode("utf-8")
        source = {
            "character": char,
            "unicode": f"U+{ord(char):04X}",
            "codepoint": ord(char),
            "cmap_glyph_name": glyph_name,
            "glyph_id": font.getGlyphID(glyph_name),
            "hmtx_advance_font_units": glyph.width,
            "bounds_font_units": bounds.bounds,
            "recording_pen_operations": recording.value,
            "recording_pen_sha256": sha(recording_bytes),
            "svg_path_pen_original_commands": commands,
            "svg_command_sha256": sha(commands.encode("utf-8")),
            "contour_count": sum(op == "closePath" for op, _ in recording.value),
            "direct_glyph_draw_and_recording_replay_commands_identical": True,
            "outline_modifications": [],
        }
        glyph_sources[char] = source
        return source

    for role in ["headline", "description", "english_hint"]:
        spec = LAYOUT[role]
        text = COPY[role]
        scale = spec["font_size_px"] / upem
        sources = [get_source(char) for char in text]
        max_y = max(g["bounds_font_units"][3] for g in sources if g["bounds_font_units"])
        baseline = spec["ink_top"] + max_y * scale
        pen_x = spec["ink_x"] - sources[0]["bounds_font_units"][0] * scale
        instances = []
        transformed_bounds = []
        paths = []
        for index, (char, source) in enumerate(zip(text, sources)):
            if index:
                pair = text[index - 1] + char
                pen_x += spec.get("pair_adjustments_px", {}).get(pair, 0)
            affine = [scale, 0, 0, -scale, pen_x, baseline]
            pid = f"{role}-u{ord(char):04x}-{index:02d}"
            bounds = source["bounds_font_units"]
            ink = None
            if bounds:
                ink = [pen_x + bounds[0] * scale, baseline - bounds[3] * scale,
                       pen_x + bounds[2] * scale, baseline - bounds[1] * scale]
                transformed_bounds.append(ink)
                paths.append(f'<path id="{pid}" data-character={quoteattr(char)} data-source-glyph="{source["cmap_glyph_name"]}" '
                             f'd={quoteattr(source["svg_path_pen_original_commands"])} '
                             f'transform="matrix({numbers(affine)})" fill="{spec["fill"]}"/>')
            advance = spec["advance_overrides_px"].get(char, source["hmtx_advance_font_units"] * scale)
            instances.append({"index": index, "character": char, "unicode": source["unicode"],
                              "cmap_glyph_name": source["cmap_glyph_name"], "source_command_sha256": source["svg_command_sha256"],
                              "path_id": pid if bounds else None, "affine": affine, "ink_bounds_px": ink,
                              "source_advance_px": source["hmtx_advance_font_units"] * scale,
                              "used_advance_px": advance, "following_tracking_px": spec["tracking_px"] if index < len(text) - 1 else 0,
                              "outline_modified": False})
            pen_x += advance + (spec["tracking_px"] if index < len(text) - 1 else 0)
        ink_bounds = [min(b[0] for b in transformed_bounds), min(b[1] for b in transformed_bounds),
                      max(b[2] for b in transformed_bounds), max(b[3] for b in transformed_bounds)]
        assert ink_bounds[3] < LAYOUT["photography_guard_y"]
        aux_content.append(f'<g id="{role}">\n' + "\n".join(paths) + "\n</g>")
        line_evidence.append({"role": role, "text": text, "regular_font_role": True, "custom_wordmark_claim": False,
                              "spec": spec, "baseline_px": baseline, "ink_bounds_px": ink_bounds,
                              "glyph_instances": instances})

    headline_content = "\n".join(aux_content)
    headline_p = write("headline.svg", svg_document("茶作 — regular Source Han Serif supporting copy", headline_content))
    combined_p = write("typography.svg", svg_document("茶作 — single V29 typography composition", brand_content + "\n" + headline_content))
    headline_tree = ET.parse(headline_p).getroot()
    assert not any(e.tag.rsplit("}", 1)[-1] in prohibited for e in headline_tree.iter())
    actual_headline_paths = headline_tree.findall(".//s:path", ns)
    by_id = {p.attrib["id"]: p for p in actual_headline_paths}
    for line in line_evidence:
        for instance in line["glyph_instances"]:
            if instance["path_id"]:
                path = by_id[instance["path_id"]]
                assert path.attrib["d"] == glyph_sources[instance["character"]]["svg_path_pen_original_commands"]

    glyph_p = write("glyph-evidence.json", json_text({
        "schema": "v29-original-font-outline-recording/v1",
        "font": font_item, "font_version_from_name_table": font_version, "units_per_em": upem,
        "method": "TTFont.getBestCmap -> getGlyphSet[character] -> RecordingPen -> replay(SVGPathPen); original d with outer affine only",
        "automatic_shaping_used": False,
        "shaping_boundary": "Simple horizontal Han copy and uppercase Latin; cmap/hmtx plus explicit recorded optical spacing, no GSUB or GPOS substitution.",
        "unique_glyph_sources": list(glyph_sources.values()), "lines": line_evidence,
    }))

    renderer_cmd = [str(NODE), str(OUT / "render_svg.cjs"), str(OUT), SHARP]
    process = subprocess.run(renderer_cmd, capture_output=True, text=True, encoding="utf-8", check=False)
    write("renderer-stdout.json", process.stdout)
    write("renderer-stderr.txt", process.stderr)
    assert process.returncode == 0, process.stderr
    renderer = json.loads(process.stdout)
    original = Image.open(BASE / INPUTS["photography"]["path"])
    assert original.size == (W, H) and original.mode == "RGB"
    overlay = Image.open(OUT / "typography-overlay.png").convert("RGBA")
    alpha = overlay.getchannel("A")
    alpha_bounds = alpha.getbbox()
    assert alpha_bounds and alpha_bounds[3] <= LAYOUT["photography_guard_y"]
    # Source RGB is never fed through an SVG renderer, resizer, colour transform, or image generator.
    poster = original.copy()
    poster.paste(overlay.convert("RGB"), (0, 0), alpha)
    poster.save(OUT / "poster.png", format="PNG", compress_level=6)
    exported = Image.open(OUT / "poster.png")
    assert exported.mode == "RGB" and exported.size == (W, H)
    original_bytes = original.tobytes()
    exported_bytes = exported.tobytes()
    alpha_bytes = alpha.tobytes()
    changed = 0
    changed_outside_alpha = 0
    for idx, alpha_value in enumerate(alpha_bytes):
        off = idx * 3
        difference = original_bytes[off:off + 3] != exported_bytes[off:off + 3]
        changed += difference
        changed_outside_alpha += difference and alpha_value == 0
    guard_box = (0, LAYOUT["photography_guard_y"], W, H)
    guard_original = original.crop(guard_box)
    guard_exported = exported.crop(guard_box)
    guard_changed = changed_pixel_count(guard_original, guard_exported)
    assert changed_outside_alpha == 0 and guard_changed == 0
    pixel_evidence = {
        "schema": "v29-source-rgb-protection/v1",
        "source_mode": original.mode, "poster_mode": exported.mode, "dimensions": [W, H],
        "source_decoded_rgb_sha256": sha(original_bytes), "poster_decoded_rgb_sha256": sha(exported_bytes),
        "typography_alpha_bounds_px_exclusive": alpha_bounds,
        "alpha_nonzero_pixel_count": sum(v != 0 for v in alpha_bytes),
        "changed_rgb_pixel_count": changed, "changed_pixel_count_where_text_alpha_zero": changed_outside_alpha,
        "protected_lower_rectangle": guard_box, "protected_lower_pixel_count": W * (H - LAYOUT["photography_guard_y"]),
        "protected_lower_changed_pixel_count": guard_changed,
        "protected_lower_original_rgb_sha256": sha(guard_original.tobytes()),
        "protected_lower_poster_rgb_sha256": sha(guard_exported.tobytes()),
        "photography_regeneration": False, "imagegen_calls": 0,
        "scope": "All photography outside actual text alpha is pixel identical. Whole canvas is the same decoded source RGB under the composited text; the complete original file is unchanged.",
    }
    pixel_p = write("pixel-protection.json", json_text(pixel_evidence))

    brand_evidence = {
        "source": INPUTS["brand"], "source_viewbox": viewbox, "compound_paths": len(original_paths),
        "complete_original_inner_svg_retained_verbatim": True,
        "per_path_attributes_identical": [p.attrib == q.attrib for p, q in zip(original_paths, output_brand_paths)],
        "uniform_group_affine": brand_affine, "placed_viewbox_bounds_px": [140, 100, 480, 100 + viewbox[3] * brand_scale],
        "source_path_records": [{"id": p.attrib["id"], "source_transform": p.attrib.get("transform"),
                                 "d_sha256": sha(p.attrib["d"].encode("utf-8")), "source_d": p.attrib["d"]} for p in original_paths],
        "outline_modified": False,
        "leaf_independently_repositioned": False,
        "provenance_boundary": "Inherited approved brand outlines; the production worker does not claim to have drawn or obtained the original wordmark's upstream font/source genealogy.",
    }
    brand_ev_p = write("brand-source-evidence.json", json_text(brand_evidence))
    write("font-license-OFL1.1.txt", (BASE / license_item["path"]).read_bytes())
    method = {
        "schema": "v29-production-method-sources/v1",
        "consulted_utc": started,
        "official_sources": [
            {"url": "https://fonttools.readthedocs.io/en/latest/ttLib/ttFont.html", "method_used": "Read the actual OpenType font, cmap, glyph set, hmtx and name table."},
            {"url": "https://fonttools.readthedocs.io/en/latest/pens/recordingPen.html", "method_used": "Record original glyph.draw operations and replay them to the SVG pen."},
            {"url": "https://fonttools.readthedocs.io/en/latest/pens/svgPathPen.html", "method_used": "Generate original SVG d commands; apply y inversion and uniform em scale in an outer affine."},
            {"url": "https://github.com/adobe-fonts/source-han-serif/blob/7889f11bf31170b5d092a083b357c8c8130f89e0/LICENSE.txt", "method_used": "OFL 1.1 license reference; local license is hashed and copied unchanged."},
        ],
        "font_upstream": {"repository": "https://github.com/adobe-fonts/source-han-serif", "commit_from_existing_provenance": provenance["font_upstream_commit"], "release_version_from_actual_font_name_table": font_version},
        "license": {**license_item, "copy": "font-license-OFL1.1.txt", "font_binary_modified": False},
        "recipe": "Read/verify exact source identities; preserve seven complete brand paths; use original cmap glyph outlines; optical spacing by advances/position only; rasterize vector layers with existing sharp/librsvg; paste RGBA text onto copied source RGB with Pillow.",
        "reference_transfer": {"reference_brand": "山野集", "migrated": ["wordmark dominates supporting text", "short copy below wordmark", "tight related information group", "natural light primary type", "small muted accent"], "composition": "Single left-aligned information group at x140, y100–447 above the product.", "not_transferred_assets": ["山野集商标字形", "山形", "橙色绕线", "广告署名", "参考原文"]},
        "limits": ["The SVG output is editable path geometry, without live text reflow.", "No GSUB/GPOS shaping is claimed; all used per-character cmap mappings and spacing are recorded.", "The wordmark is inherited geometry; its original source genealogy is outside this production scope.", "Runtime model and reasoning strength are not observable through the tools available to this worker.", "Engineering identity and pixel checks do not establish visual or human approval."],
    }
    method_p = write("method-sources.json", json_text(method))
    runtime = {
        "python_version": sys.version, "python_executable": sys.executable, "platform": platform.platform(),
        "pillow_version": PIL.__version__, "pillow_module": PIL.__file__,
        "fonttools_version": fontTools.__version__, "fonttools_module": fontTools.__file__,
        "fonttools_import_path_appended": str(FONTTOOLS_SITE), "bundled_pillow_imported_before_appending": True,
        "renderer": renderer, "actual_inference_model": None, "actual_reasoning_effort": None,
        "model_binding_limit": "No tool response available to the production worker exposes the actual current inference backend or reasoning strength. No requested model name is used as runtime evidence.",
    }
    runtime_p = write("runtime-and-invocation.json", json_text({
        "schema": "v29-actual-production-execution/v1", "start_utc": started,
        "completion_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "python_argv": sys.orig_argv,
        "python_argv_basis": "Actual interpreter arguments exposed by sys.orig_argv; interpreter identity observed from sys.executable.",
        "actual_argv_seen_by_script": sys.argv, "renderer_subprocess_argv": renderer_cmd,
        "renderer_exit_code": process.returncode, "runtime": runtime,
        "preflight_failure_preserved": ["Default bundled Python import of fontTools raised ModuleNotFoundError before existing hermes site-packages was appended.", "Default shell Node 22.22.3 could not resolve sharp; actual rendering uses bundled Node 24.19.0 and absolute existing sharp path."],
        "production_design_count": 1, "rendered_poster_trial_count": 1, "paid_compute_or_package_install": False,
        "actual_original_image_views": ["Worker functions.exec/tools.view_image(detail=original): canonical 山野集 960×1280", "Worker functions.exec/tools.view_image(detail=original): approved tea photography 1536×1024"],
    }))
    output_files = [brand_p, headline_p, combined_p, glyph_p, pixel_p, brand_ev_p, method_p, runtime_p,
                    OUT / "poster.png", OUT / "brand-render.png", OUT / "headline-render.png", OUT / "typography-overlay.png",
                    OUT / "renderer-stdout.json", OUT / "renderer-stderr.txt", OUT / "font-license-OFL1.1.txt",
                    Path(__file__).resolve(), OUT / "render_svg.cjs"]
    manifest = {
        "schema": "private-shanyeji-v29-production-trial/v1", "production_role": "MAKER_ONLY",
        "formal_version_hint": 29, "formal_freeze_performed": False, "aesthetic_pass_claimed": False,
        "single_design": True, "copy": COPY, "layout": LAYOUT, "source_inputs": INPUTS,
        "font_foundation": font_item, "font_version": font_version,
        "brand_inherited_original_paths": {"count": 7, "attributes_and_commands_preserved": True, "uniform_affine": brand_affine,
                                           "evidence": "brand-source-evidence.json"},
        "supporting_type": {"font_role": "Regular Source Han Serif SC supporting typography; not a custom wordmark", "per_character_editable_path_count": len(actual_headline_paths), "source_evidence": "glyph-evidence.json", "ink_line_bounds": [{"role": x["role"], "bounds": x["ink_bounds_px"]} for x in line_evidence]},
        "vector_contract": {"brand_svg_paths": 7, "headline_svg_paths": len(actual_headline_paths), "combined_svg_paths": 7 + len(actual_headline_paths), "full_canvas": [W, H], "forbidden_svg_elements": ["image", "mask", "filter", "clipPath", "text", "use", "foreignObject"], "path_fills": ["#F5F2E6", "#E5E4D4", "#C1C6B1", "#BE9861"]},
        "photography_protection": pixel_evidence, "runtime_evidence": "runtime-and-invocation.json",
        "methods_and_license": "method-sources.json",
        "write_boundary": ".liu-visual-private/shanyeji-v29-production/ only; no shared/public, state, Git, Figma or Drive writes",
        "assets": [{"path": p.name, "sha256": digest(p), "bytes": p.stat().st_size} for p in output_files],
        "next_owner_action": "Root verifies these private production files before prospective formal V29 binding and an independent cold review.",
    }
    write("manifest.json", json_text(manifest))
    print(json_text({"output_directory": str(OUT), "poster_sha256": digest(OUT / "poster.png"),
                     "manifest_sha256": digest(OUT / "manifest.json"), "auxiliary_path_count": len(actual_headline_paths),
                     "text_alpha_bounds": alpha_bounds, "outside_alpha_changed_pixels": changed_outside_alpha,
                     "lower_protected_changed_pixels": guard_changed, "line_bounds": manifest["supporting_type"]["ink_line_bounds"]}))


if __name__ == "__main__":
    main()
