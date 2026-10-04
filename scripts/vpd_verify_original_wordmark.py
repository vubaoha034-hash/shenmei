"""Read-only verification of the bound V5 wordmark; never run its legacy writers.

The historical builder is immutable evidence, not a safe disk-export entry point.
This verifier pins all inputs, replays its geometry with a closed in-memory Path
facade and a restricted namespace, then compares every contour and shared rule.
No PNG renderer is invoked. No disk-output option is implemented.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
from types import SimpleNamespace
import xml.etree.ElementTree as ET

sys.dont_write_bytecode = True

WORDMARK_REL = Path("evidence/vpd/codex_takeover_20261003/continuous_typography_20261004/v5/wordmark")
SOURCES = {
    "photo": (".liu-visual-private/source_recovery_20261003/photography-local-reconstruction-final.png", "7fd7777fed21100cb6b47bc305701476054263565e73246ac469d065aa080618"),
    "reference": (".liu-visual-private/reference.jpg", "87a28f5cd4b5d15b01e6536206127c357043a904b3c0dab3bfa0c50080782167"),
    "v4": (".liu-visual-private/correct_source_typography/v4/poster.png", "fe382983910d02308ef211594314baa0002a5d9b931eaad49b9353789c75478a"),
}
FILES = {
    "build_wordmark.py": (12811, "f52af4a809ecba1ac21b82eeba1d1a6f7e76e9498b4334d6eb7b520118a1d60d"),
    "chazuo-wordmark.png": (5489, "c63fdceb0b7b75c4ffa70821f2634e444a4c042500b1fad322d2a9b737696efe"),
    "chazuo-wordmark.svg": (3964, "923b4c2fa57fb903ec6234ddc145c3ff476b63fad8289bd36ce892f92da55b74"),
    "construction.json": (52862, "e0446ebddfc65144641473404df704d6426f9b7fb046052d7707a2a576e5c699"),
    "figma-vector-paths.json": (4527, "d5aca14a509f87717cd979ff1a8174565dea0a648532a085ee58625cb92089bd"),
    "method_basis.json": (1326, "e0b56e186037324a29e3eef35e2daea879f5d92cd40e5f346e877903f3364a72"),
    "provenance.json": (2540, "34ea3ce4197d0f8ea109cf284ce2aa11846257b03f29a4069b690e848ce6c663"),
    "render_wordmark.cjs": (1426, "fe772365366598b02483aba4772cc68c20637f001310f65e6e291e3244e942fe"),
}
MANIFEST_SHA = "1ee9619693a13a87852108c1a42be4026bceba1c85d48c0cc766b7fd71929b0d"
RUNTIME = Path("C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies")
FONTTOOLS_SITE = "C:/Users/Administrator/AppData/Local/hermes/hermes-agent/venv/Lib/site-packages"
MEMORY_OUTPUTS = {"chazuo-wordmark.svg", "figma-vector-paths.json", "construction.json", "method_basis.json", "provenance.json"}
SVG_NS = "{http://www.w3.org/2000/svg}"


class VerificationError(Exception):
    def __init__(self, code: str, detail: str):
        super().__init__(detail)
        self.code = code


def require(condition: bool, code: str, detail: str) -> None:
    if not condition:
        raise VerificationError(code, detail)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def key(path: Path) -> str:
    return str(path).replace("\\", "/").casefold()


def load_json(data: bytes):
    return json.loads(data.decode("utf-8"))


def preflight(repo: Path, overrides: dict[str, str | None], progress: dict):
    """Read and validate every binding before allowing any geometry replay."""
    folder = repo / WORDMARK_REL
    snapshots: dict[str, bytes] = {}
    source_report = {}
    for name, (relative, expected) in SOURCES.items():
        supplied = overrides.get(name)
        canonical_path = (repo / relative).resolve()
        try:
            data = canonical_path.read_bytes()
        except OSError as exc:
            raise VerificationError("SOURCE_UNREADABLE", f"{name}: {exc}") from exc
        actual = digest(data)
        require(actual == expected, "SOURCE_SHA_MISMATCH", f"{name}: expected {expected}, got {actual}")
        if supplied:
            supplied_path = Path(supplied).resolve()
            try:
                supplied_hash = digest(supplied_path.read_bytes())
            except OSError as exc:
                raise VerificationError("SOURCE_UNREADABLE", f"{name} override: {exc}") from exc
            require(supplied_hash == expected, "SOURCE_SHA_MISMATCH", f"{name} override: expected {expected}, got {supplied_hash}")
        snapshots[key(repo / relative)] = data
        source_report[name] = {"path": str(canonical_path), "sha256": actual, "bytes": len(data), "override_validated": bool(supplied)}

    try:
        manifest_data = (folder / "manifest.json").read_bytes()
    except OSError as exc:
        raise VerificationError("MANIFEST_UNREADABLE", str(exc)) from exc
    require(digest(manifest_data) == MANIFEST_SHA, "MANIFEST_SHA_MISMATCH", "The historical manifest itself changed.")
    manifest = load_json(manifest_data)
    entries = manifest.get("files", [])
    require(len(entries) == 8 and {item.get("file") for item in entries} == set(FILES), "MANIFEST_MEMBERS_MISMATCH", "Expected the eight bound historical files, exactly once.")
    files = {"manifest.json": manifest_data}
    for item in entries:
        name = item["file"]
        size, expected = FILES[name]
        require(item.get("sha256") == expected and item.get("bytes") == size, "MANIFEST_BINDING_MISMATCH", name)
        try:
            data = (folder / name).read_bytes()
        except OSError as exc:
            raise VerificationError("ASSET_UNREADABLE", f"{name}: {exc}") from exc
        require(len(data) == size and digest(data) == expected, "ASSET_SHA_MISMATCH", name)
        files[name] = data
    for name, data in files.items():
        snapshots[key(folder / name)] = data

    # Importing with bytecode disabled cannot refresh old __pycache__ files.
    if FONTTOOLS_SITE not in sys.path:
        sys.path.append(FONTTOOLS_SITE)
    try:
        import fontTools
        from fontTools.pens.boundsPen import BoundsPen
    except ImportError as exc:
        raise VerificationError("DEPENDENCY_MISSING", f"fontTools: {exc}") from exc
    require(fontTools.__version__ == "4.63.0", "DEPENDENCY_VERSION_MISMATCH", f"fontTools {fontTools.__version__}")
    node = RUNTIME / "node/bin/node.exe"
    sharp = RUNTIME / "node/node_modules/sharp"
    require(node.is_file() and sharp.is_dir(), "DEPENDENCY_MISSING", "Bundled Node or Sharp is unavailable.")
    probe = "const sharp=require(" + json.dumps(str(sharp).replace("\\", "/")) + ");process.stdout.write(JSON.stringify({node:process.version,sharp:sharp.versions.sharp}));"
    environment = {name: value for name, value in os.environ.items() if name not in {"NODE_OPTIONS", "NODE_PATH"}}
    try:
        completed = subprocess.run([str(node), "-e", probe], check=True, capture_output=True, text=True, timeout=15, env=environment, cwd=repo)
        node_info = json.loads(completed.stdout)
    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        raise VerificationError("DEPENDENCY_PROBE_FAILED", str(exc)) from exc
    require(node_info == {"node": "v24.19.0", "sharp": "0.35.4"}, "DEPENDENCY_VERSION_MISMATCH", str(node_info))
    png = files["chazuo-wordmark.png"]
    require(png[:8] == b"\x89PNG\r\n\x1a\n" and png[12:16] == b"IHDR", "PNG_METADATA_MISMATCH", "Expected bound PNG IHDR.")
    require(struct.unpack(">IIBB", png[16:26]) == (260, 135, 8, 6), "PNG_METADATA_MISMATCH", "Expected 260x135 RGBA8.")
    progress["preflight_complete"] = True
    return folder, files, snapshots, source_report, {"python": sys.version, "python_executable": sys.executable, "fontTools": fontTools.__version__, **node_info}, BoundsPen


def replay_in_memory(folder: Path, files: dict, snapshots: dict, BoundsPen, progress: dict):
    """Execute only the pinned builder, with no imports/open/disk Path capability."""
    captures: dict[str, bytes] = {}
    events: list[dict] = []
    print_calls: list[str] = []

    class MemoryPath:
        def __init__(self, value):
            self.path = value.path if isinstance(value, MemoryPath) else Path(value)
            require(self.path.is_absolute(), "MEMORY_PATH_REJECTED", "Only absolute snapshot paths are supported.")

        def __truediv__(self, suffix):
            return MemoryPath(self.path / suffix)

        def __str__(self):
            return str(self.path)

        def resolve(self):
            return self

        @property
        def parent(self):
            return MemoryPath(self.path.parent)

        @property
        def parents(self):
            return tuple(MemoryPath(parent) for parent in self.path.parents)

        def relative_to(self, other):
            return self.path.relative_to(other.path)

        def exists(self):
            return key(self.path) in snapshots or self.path.name in captures and self.path.parent == folder

        def read_bytes(self):
            if self.path.parent == folder and self.path.name in captures:
                return captures[self.path.name]
            require(key(self.path) in snapshots, "MEMORY_READ_REJECTED", str(self.path))
            return snapshots[key(self.path)]

        def mkdir(self, *, parents=False, exist_ok=False):
            require(self.path == folder and parents and exist_ok, "MEMORY_MKDIR_REJECTED", str(self.path))
            events.append({"operation": "mkdir", "path": str(self.path), "destination": "memory_only"})

        def write_text(self, text, *, encoding):
            require(self.path.parent == folder and self.path.name in MEMORY_OUTPUTS, "MEMORY_WRITE_REJECTED", str(self.path))
            require(encoding == "utf-8" and self.path.name not in captures, "MEMORY_WRITE_REJECTED", "Unexpected encoding or duplicate output.")
            # Historical Python Path.write_text used Windows newline translation.
            captures[self.path.name] = text.replace("\n", "\r\n").encode("utf-8")
            events.append({"operation": "write_text", "path": str(self.path), "destination": "memory_only", "bytes": len(captures[self.path.name])})
            progress["captured_write_count"] = len(captures)
            return len(text)

    tree = ast.parse(files["build_wordmark.py"].decode("utf-8"), filename=str(folder / "build_wordmark.py"))
    expected_imports = {"from pathlib import Path", "import hashlib", "import json", "import math", "import os", "import sys", "import fontTools", "from fontTools.pens.boundsPen import BoundsPen"}
    imports = {ast.unparse(node) for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom))}
    require(imports == expected_imports, "LEGACY_IMPORTS_CHANGED", "Only the pinned legacy import set can be replaced.")
    removed_setup = {"sys.dont_write_bytecode = True", "sys.path.append('C:/Users/Administrator/AppData/Local/hermes/hermes-agent/venv/Lib/site-packages')"}
    tree.body = [node for node in tree.body if not isinstance(node, (ast.Import, ast.ImportFrom)) and ast.unparse(node) not in removed_setup]
    require(not any(isinstance(node, (ast.Import, ast.ImportFrom)) for node in ast.walk(tree)), "LEGACY_IMPORTS_CHANGED", "Nested imports are not allowed.")
    historical = load_json(files["provenance.json"])
    safe_builtins = {"str": str, "min": min, "max": max, "len": len, "tuple": tuple, "getattr": getattr, "ValueError": ValueError, "print": lambda value: print_calls.append(str(value))}
    namespace = {
        "__builtins__": safe_builtins,
        "__file__": str(folder / "build_wordmark.py"),
        "Path": MemoryPath,
        "hashlib": hashlib,
        "json": json,
        "os": SimpleNamespace(environ={"CODEX_THREAD_ID": historical["execution"]["thread_id"]}),
        "sys": SimpleNamespace(executable=historical["execution"]["python_executable"]),
        "fontTools": SimpleNamespace(__version__="4.63.0"),
        "BoundsPen": BoundsPen,
    }
    progress["reconstruction_started"] = True
    exec(compile(ast.fix_missing_locations(tree), str(folder / "build_wordmark.py") + " [memory-only]", "exec"), namespace)
    require(set(captures) == MEMORY_OUTPUTS, "CAPTURE_SET_MISMATCH", "Expected exactly five captured legacy write_text operations.")
    return captures, events


def compare_geometry(files: dict, captures: dict):
    for name in ("chazuo-wordmark.svg", "figma-vector-paths.json", "construction.json", "method_basis.json"):
        require(captures[name] == files[name], "RECONSTRUCTION_BYTES_MISMATCH", name)
    captured_provenance = load_json(captures["provenance.json"])
    historical_provenance = load_json(files["provenance.json"])
    historical_without_raster = {name: value for name, value in historical_provenance.items() if name != "actual_raster_export"}
    require(captured_provenance == historical_without_raster, "PROVENANCE_REPLAY_MISMATCH", "The original identity must be reproduced only in memory.")
    actual_svg = ET.fromstring(files["chazuo-wordmark.svg"])
    replay_svg = ET.fromstring(captures["chazuo-wordmark.svg"])
    require(actual_svg.attrib == {"width": "260", "height": "135", "viewBox": "0 0 260 135"}, "SVG_CANVAS_MISMATCH", "Unexpected canvas.")
    actual_paths = actual_svg.findall(".//" + SVG_NS + "path")
    replay_paths = replay_svg.findall(".//" + SVG_NS + "path")
    construction = load_json(captures["construction.json"])
    figma = load_json(files["figma-vector-paths.json"])
    strokes = construction["stroke_by_stroke_origin"]
    require(len(actual_paths) == len(replay_paths) == len(strokes) == len(figma["paths"]) == 15, "CONTOUR_COUNT_MISMATCH", "Expected fifteen contours.")
    path_results = []
    for actual, replay, stroke, vector in zip(actual_paths, replay_paths, strokes, figma["paths"]):
        require(actual.attrib == replay.attrib, "PATH_ATTRIBUTES_MISMATCH", stroke["id"])
        require(actual.get("id") == stroke["id"] == vector["name"], "PATH_ID_MISMATCH", stroke["id"])
        require(actual.get("d") == stroke["svg_path_d"] == vector["data"], "PATH_GEOMETRY_MISMATCH", stroke["id"])
        require(actual.get("data-character") == stroke["character"] == vector["character"] and actual.get("data-component") == stroke["component"], "PATH_STRUCTURE_MISMATCH", stroke["id"])
        require(actual.get("d", "").endswith("Z") and vector["windingRule"] == "NONZERO", "PATH_CLOSURE_MISMATCH", stroke["id"])
        path_results.append({"id": stroke["id"], "character": stroke["character"], "component": stroke["component"], "commands": len(stroke["commands"]), "geometry_matches": True})
    by_id = {stroke["id"]: stroke for stroke in strokes}
    shared = construction["shared_identity"]
    require(shared["main_vertical_weight_units"] == 82 and shared["wood_and_zha_horizontal_weight_units"] == 64 and shared["corner_cut_units"] == 22, "SHARED_STRUCTURE_MISMATCH", "Shared parameters changed.")
    require(by_id["cha-wood-stem-hook"]["commands"][2][1][0][0] - by_id["cha-wood-stem-hook"]["commands"][-2][1][0][0] == 82, "SHARED_STRUCTURE_MISMATCH", "Wood shaft width.")
    for name in ("zuo-person-upright", "zuo-zha-main-upright"):
        points = [point for _, pts in by_id[name]["commands"] for point in pts]
        require(max(point[0] for point in points) - min(point[0] for point in points) == 82, "SHARED_STRUCTURE_MISMATCH", name)
    for name in ("cha-wood-horizontal", "zuo-zha-upper-horizontal", "zuo-zha-middle-horizontal", "zuo-zha-lower-horizontal"):
        commands = by_id[name]["commands"]
        require(commands[4][1][0][1] - commands[1][1][2][1] == 64, "SHARED_STRUCTURE_MISMATCH", name + " weight")
        require(commands[2][1][0][0] - commands[1][1][2][0] == 22 and commands[2][1][0][1] - commands[1][1][2][1] == 22, "SHARED_STRUCTURE_MISMATCH", name + " cut")
    require([stroke["component"] for stroke in strokes] == ["艹"] * 3 + ["人"] + ["木"] * 4 + ["亻"] * 2 + ["乍"] * 5, "CHARACTER_STRUCTURE_MISMATCH", "Component sequence changed.")
    require(construction["glyph_cells"] == {"茶": 0, "作": 1012} and construction["counter_space"]["intercharacter_nearest_bbox_gap_units"] == 148, "SHARED_STRUCTURE_MISMATCH", "Spacing changed.")
    return path_results, shared, historical_provenance["execution"]["thread_id"]


def verify(args, progress: dict):
    repo = Path(args.repo).resolve()
    folder, files, snapshots, sources, dependencies, bounds_pen = preflight(repo, {"photo": args.photo_path, "reference": args.reference_path, "v4": args.v4_path}, progress)
    if args.output_dir is not None:
        requested = Path(args.output_dir).resolve()
        if requested.exists():
            raise VerificationError("EXISTING_OUTPUT_REJECTED", f"No write or overwrite is permitted: {requested}")
        raise VerificationError("READ_ONLY_ENTRY_POINT", "This entry point has no disk export. Reuse the verified existing SVG bytes separately.")
    captures, events = replay_in_memory(folder, files, snapshots, bounds_pen, progress)
    paths, shared, identity = compare_geometry(files, captures)
    for name, previous in files.items():
        require((folder / name).read_bytes() == previous, "HISTORICAL_BYTES_CHANGED", name)
    for name, (relative, expected) in SOURCES.items():
        require(digest((repo / relative).read_bytes()) == expected, "CANONICAL_SOURCE_CHANGED", name)
    return {"result": "verified_original_geometry_only", "mode": "read_only", **progress, "sources": sources, "manifest_sha256": MANIFEST_SHA, "historical_files_verified": len(files), "manifest_entries_verified": len(FILES), "dependencies": dependencies, "paths": paths, "shared_structure": shared, "captured_operations": events, "memory_output_sha256": {name: digest(data) for name, data in captures.items()}, "historical_identity_preserved": identity, "historical_files_unchanged": True, "raster_render_calls": 0, "legacy_builder_disk_executions": 0, "legacy_render_executions": 0, "aesthetic_acceptance_claimed": False}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--photo-path", help="Read-only source override; fixed expected SHA remains mandatory.")
    parser.add_argument("--reference-path", help="Read-only source override; fixed expected SHA remains mandatory.")
    parser.add_argument("--v4-path", help="Read-only source override; fixed expected SHA remains mandatory.")
    parser.add_argument("--output-dir", help="Always rejected; guards callers migrating from the unsafe disk builder.")
    args = parser.parse_args(argv)
    progress = {"preflight_complete": False, "reconstruction_started": False, "captured_write_count": 0, "disk_writes": 0}
    try:
        report = verify(args, progress)
    except VerificationError as exc:
        report = {"result": "rejected", "code": exc.code, "detail": str(exc), **progress}
        print(json.dumps(report, ensure_ascii=True, indent=2))
        return 2
    except (OSError, ValueError, KeyError, TypeError, AssertionError) as exc:
        report = {"result": "rejected", "code": "VERIFICATION_ERROR", "detail": f"{type(exc).__name__}: {exc}", **progress}
        print(json.dumps(report, ensure_ascii=True, indent=2))
        return 2
    print(json.dumps(report, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
