"""Thin CLI for the private 2026-10-05 SHANYEJI typography study.

The public repository contains this adapter, not the source artwork or assets.
Missing private material or an identity mismatch is a refusal, not a request to
download, regenerate, substitute a font, or reconstruct photography.

Commands:
  inspect   Read existing source/SVG/PNG/masks and check actual integrity.
  trace     Call the pinned private VTracer producer into a new private folder.
  soft-ink  Call the pinned private soft-alpha producer into a new private folder.

Dependencies: Python, Pillow and NumPy for inspect/soft-ink; trace additionally
uses unmodified MIT VTracer 0.6.15 (the existing cp312 local wheel) and Node sharp.
The producer's bundled Windows Node/sharp paths are defaults; trace can receive
explicit --node and --sharp runtime locations. No packages are auto-installed.
This machine's help/inspect are verified. A fresh machine and new production
runs through this adapter have NOT been validated.

Examples from the repository root:
  python -B scripts/vpd_shanyeji_typography_study.py inspect
  python -B scripts/vpd_shanyeji_typography_study.py trace --output .liu-visual-private/new-trace-run
  python -B scripts/vpd_shanyeji_typography_study.py soft-ink --output .liu-visual-private/new-soft-run

Production requires an output directory that does not yet exist, below the
repository's .liu-visual-private tree. Existing output folders are never reused.
Results are approximation studies; integrity checks do not grant fidelity or
human acceptance, recover true JPEG alpha, or change project business state.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from types import ModuleType
import xml.etree.ElementTree as ET

sys.dont_write_bytecode = True

SOURCE_SHA = "9a29fbdc7dd908017924bed270e8dfe18351519eed3fa7bc7001789f2a383414"
CLEAN_SHA = "59376f5da7fa880efa8c0e92adcb1e60845cfdf697c5a8cf04430abbd9ec4a6b"
TRACE_CODE_SHA = "badccb256bb95a95e25106d8d70d3058d9ddc4f9be49fb9892776d6b6dc3d55b"
SOFT_CODE_SHA = "55a0c90d24b24827fe8afdf104396f55b55f8ce2baa474339284debc4eb8baa8"
S2_SHAS = {
    "SHANYEJI_soft_foreground_all.png": "0c4fb7f9499edc7949f326d70000fc745dbd956a9f7813ddf84df4db6a4f5337",
    "SHANYEJI_soft_foreground_typography.png": "6915bd41da6c96480376cdd2495ae2a2ca7eaabf8bc0ccd0dc60c7f7e70d1cb3",
    "tiny_corner_UNREADABLE_graphic.png": "50f385f7a94908039d7f4396b3d9f9aac7c2f865af9fc35635d72065d9225dcd",
}
SVG_NS = {"s": "http://www.w3.org/2000/svg"}


class StudyRefusal(RuntimeError):
    pass


class Layout:
    def __init__(self, repo: Path):
        self.repo = repo.resolve()
        self.private = self.repo / ".liu-visual-private"
        self.study = self.private / "shanyeji_typography_study_20261005/reconstruction"
        self.source = self.private / "product-type-integration-20261004/SHANYEJI-canonical-readback-20261005.jpg"
        self.trace_code = self.study / "reconstruct_typography.py"
        self.soft = self.study / "03_soft_foreground_trial"
        self.soft_code = self.soft / "soft_foreground_trial.py"
        self.s1 = self.study / "02_full_final_vector_detail"
        self.baseline = self.study / "00_main_baseline"


def required(path: Path) -> Path:
    if not path.is_file():
        raise StudyRefusal(f"PRIVATE_MATERIAL_MISSING: {path}; provide authorized private material; no substitute is produced")
    return path


def digest(path: Path) -> str:
    return hashlib.sha256(required(path).read_bytes()).hexdigest()


def identity(path: Path, expected: str) -> dict:
    actual = digest(path)
    if actual != expected:
        raise StudyRefusal(f"SHA_MISMATCH: {path}; expected {expected}, actual {actual}")
    return {"path": str(path), "sha256": actual, "bytes": path.stat().st_size}


def read_json(path: Path) -> dict:
    return json.loads(required(path).read_text(encoding="utf-8"))


def load_producer(path: Path, expected: str, name: str) -> ModuleType:
    identity(path, expected)
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise StudyRefusal(f"PRODUCER_LOAD_FAILED: {path}")
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except ImportError as exc:
        raise StudyRefusal(f"DEPENDENCY_MISSING: {exc}; dependencies are not auto-installed") from exc
    return module


def private_output(layout: Layout, argument: str) -> Path:
    raw = Path(argument)
    candidate = raw if raw.is_absolute() else layout.repo / raw
    if candidate.exists() or candidate.is_symlink():
        raise StudyRefusal(f"OUTPUT_ALREADY_EXISTS: {candidate}; existing outputs are never overwritten")
    target = candidate.resolve()
    private = layout.private.resolve()
    if not private.is_relative_to(layout.repo) or not target.is_relative_to(private):
        raise StudyRefusal("OUTPUT_NOT_PRIVATE: output must stay within this repository's .liu-visual-private tree")
    if target.exists() or target.is_symlink():
        raise StudyRefusal(f"OUTPUT_ALREADY_EXISTS: {target}; existing outputs are never overwritten")
    return target


def soft_inputs(layout: Layout) -> tuple[dict, dict]:
    current = read_json(layout.s1 / "MANIFEST.json")
    baseline = read_json(layout.baseline / "MANIFEST.json")
    for item in current["groups"]:
        required(layout.s1 / "masks" / f"{item['name']}.png")
    for item in baseline["groups"]:
        if item["name"].startswith("main_"):
            required(layout.baseline / "masks" / f"{item['name']}.png")
    required(layout.s1 / "SHANYEJI_typography_transparent.png")
    return current, baseline


def measured_support(layout: Layout, producer: ModuleType, current: dict, baseline: dict):
    """Recompute support geometry only through existing producer helpers; no RGB image is produced."""
    import numpy as np

    old = {x["name"]: producer.full_mask(x, layout.baseline) for x in baseline["groups"] if x["name"].startswith("main_")}
    allowed = np.zeros((1280, 960), dtype=bool)
    for item in current["groups"]:
        name = item["name"]
        if name == "LiJiaBan_seal_black_glyphs":
            continue
        mask = producer.full_mask(item, layout.s1)
        is_main = name.startswith("main_")
        is_seal = name == "LiJiaBan_seal_orange_shape"
        x0, y0, x1, y1 = producer.local_box(item["bbox"], 3 if is_seal else 10)
        core = mask[y0:y1, x0:x1]
        if is_seal:
            support = producer.filter_bool(core, 3, "dilate")
        else:
            observed = old[name][y0:y1, x0:x1] if is_main else core
            closed = producer.fill_holes(observed)
            holes = producer.components_at_least(closed & ~observed, 12 if is_main else 3)
            hole_core = producer.filter_bool(holes, 3, "erode")
            support = producer.filter_bool(closed, 3 if is_main else 5, "dilate") & ~hole_core
        allowed[y0:y1, x0:x1] |= support
    return allowed


def inspect(layout: Layout) -> dict:
    import numpy as np
    from PIL import Image

    source = identity(layout.source, SOURCE_SHA)
    trace_identity = identity(layout.trace_code, TRACE_CODE_SHA)
    with Image.open(layout.source) as image:
        if image.size != (960, 1280):
            raise StudyRefusal(f"SOURCE_SIZE_MISMATCH: {image.size}")
    clean = identity(layout.s1 / "SHANYEJI_typography_contours_clean.svg", CLEAN_SHA)
    root = ET.parse(clean["path"]).getroot()
    paths = root.findall(".//s:path", SVG_NS)
    forbidden = [element.tag.split("}")[-1] for element in root.iter() if element.tag.split("}")[-1] in ("image", "text", "foreignObject")]
    if len(paths) != 241 or any(not path.get("d", "").strip() for path in paths) or forbidden:
        raise StudyRefusal(f"CLEAN_SVG_STRUCTURE_MISMATCH: paths={len(paths)}, forbidden={forbidden}")
    if root.get("viewBox") != "0 0 960 1280":
        raise StudyRefusal("CLEAN_SVG_VIEWBOX_MISMATCH")
    clean.update({"nonempty_path_count": len(paths), "forbidden_painted_element_types": forbidden, "viewBox": root.get("viewBox")})
    images = {}
    asset_report = {}
    for name, expected in S2_SHAS.items():
        path = layout.soft / name
        asset_report[name] = identity(path, expected)
        with Image.open(path) as image:
            expected_size = (50, 31) if name.startswith("tiny_corner_") else (960, 1280)
            if image.mode != "RGBA" or image.size != expected_size:
                raise StudyRefusal(f"S2_RGBA_STRUCTURE_MISMATCH: {name}, mode={image.mode}, size={image.size}")
            asset_report[name].update({"mode": image.mode, "size": list(image.size)})
            images[name] = np.asarray(image).copy()
    producer = load_producer(layout.soft_code, SOFT_CODE_SHA, "shanyeji_inspect_support")
    current, baseline = soft_inputs(layout)
    support = measured_support(layout, producer, current, baseline)
    typ = images["SHANYEJI_soft_foreground_typography.png"]
    all_image = images["SHANYEJI_soft_foreground_all.png"]
    alpha = all_image[:, :, 3]
    outside = int(((typ[:, :, 3] > 0) & ~support).sum())
    probes = {"empty_canvas": int(alpha[300, 480]), "shan_counter": int(alpha[518, 261]), "WANCE_Lambda_opening": int(alpha[1202, 513])}
    if outside != 0 or any(probes.values()):
        raise StudyRefusal(f"S2_ALPHA_SUPPORT_MISMATCH: outside={outside}, probes={probes}")
    return {"status": "STRUCTURAL_INTEGRITY_PASS_ONLY", "operation": "inspect", "production_run": False,
            "source": source, "clean_svg": clean, "S2_assets": asset_report,
            "alpha_measurements": {"outside_text_support_nonzero": outside, "nonzero": int((alpha > 0).sum()),
                                   "intermediate": int(((alpha > 0) & (alpha < 255)).sum()), "transparent_probes": probes},
            "producer_SHA": {"trace": trace_identity["sha256"], "soft": digest(layout.soft_code)},
            "limits": ["Existing private assets only; no new artwork was generated", "This does not reassess reference fidelity or human approval",
                       "Original JPEG alpha remains unknown", "Fresh-machine execution is not verified"]}


def trace(layout: Layout, args) -> dict:
    identity(layout.source, SOURCE_SHA)
    output = private_output(layout, args.output)
    producer = load_producer(layout.trace_code, TRACE_CODE_SHA, "shanyeji_trace_producer")
    if args.node:
        producer.NODE = Path(args.node).resolve()
    if args.sharp:
        producer.SHARP = str(Path(args.sharp).resolve())
    if not producer.NODE.is_file() or not Path(producer.SHARP).is_dir():
        raise StudyRefusal("TRACE_RUNTIME_MISSING: requires an existing Node executable and installed sharp directory; use --node/--sharp")
    output.mkdir(parents=True, exist_ok=False)
    producer.HERE = output.parent
    producer.ROOT = layout.repo
    producer.SOURCE = layout.source
    old_argv = sys.argv
    try:
        sys.argv = [str(layout.trace_code), "--phase", "full", "--correction", "2", "--aux-vector-scale", "4", "--revision", output.name]
        producer.main()
    finally:
        sys.argv = old_argv
    return {"status": "NEW_PRIVATE_TRACE_OUTPUT_CREATED", "output": str(output), "producer_sha256": TRACE_CODE_SHA,
            "method": "existing pinned producer, VTracer 0.6.15, full/correction2/aux-vector-scale4", "fidelity_pass_claimed": False}


def soft_ink(layout: Layout, args) -> dict:
    identity(layout.source, SOURCE_SHA)
    soft_inputs(layout)
    output = private_output(layout, args.output)
    producer = load_producer(layout.soft_code, SOFT_CODE_SHA, "shanyeji_soft_producer")
    output.mkdir(parents=True, exist_ok=False)
    producer.HERE = output
    producer.ROOT = layout.repo
    producer.SOURCE = layout.source
    producer.S1 = layout.s1
    producer.BASELINE = layout.baseline
    producer.main()
    return {"status": "NEW_PRIVATE_SOFT_OUTPUT_CREATED", "output": str(output), "producer_sha256": SOFT_CODE_SHA,
            "method": "existing pinned source-color/soft-alpha producer", "original_alpha_recovered": False, "fidelity_pass_claimed": False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1], help="repository containing the authorized .liu-visual-private material")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("inspect", help="read and measure existing canonical/S1-clean/S2 assets; no production writes")
    trace_parser = sub.add_parser("trace", help="call the existing VTracer producer in a new private output directory")
    trace_parser.add_argument("--output", required=True, help="new directory below .liu-visual-private; must not exist")
    trace_parser.add_argument("--node", help="optional existing Node executable override")
    trace_parser.add_argument("--sharp", help="optional installed sharp directory override")
    soft_parser = sub.add_parser("soft-ink", help="call the existing soft-alpha producer in a new private output directory")
    soft_parser.add_argument("--output", required=True, help="new directory below .liu-visual-private; must not exist")
    args = parser.parse_args()
    try:
        layout = Layout(args.repo_root)
        result = inspect(layout) if args.command == "inspect" else trace(layout, args) if args.command == "trace" else soft_ink(layout, args)
    except (StudyRefusal, OSError, ValueError, ImportError, KeyError, ET.ParseError) as exc:
        print(json.dumps({"status": "REFUSED_OR_FAILED", "operation": args.command, "reason": str(exc), "production_success_claimed": False}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
