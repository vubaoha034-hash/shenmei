"""Audit runtime Python files against the pinned official source, without edits."""
from pathlib import Path
import hashlib
import importlib
import json

ROOT = Path(__file__).resolve().parent
MODULES = ["fontTools.ttLib.ttFont", "fontTools.pens.boundsPen", "fontTools.pens.statisticsPen", "fontTools.pens.momentsPen", "fontTools.pens.recordingPen", "fontTools.pens.svgPathPen"]
records = []
for module_name in MODULES:
    module = importlib.import_module(module_name)
    runtime = Path(module.__file__)
    source = ROOT / "upstream/fonttools/fonttools/Lib" / Path(*module_name.split(".")).with_suffix(".py")
    runtime_bytes = runtime.read_bytes()
    source_bytes = source.read_bytes()
    records.append({
        "module": module_name, "runtime_file": str(runtime),
        "pinned_source_file": str(source),
        "runtime_sha256": hashlib.sha256(runtime_bytes).hexdigest(),
        "pinned_source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "exact_byte_match": runtime_bytes == source_bytes,
        "newline_normalized_match": runtime_bytes.replace(b"\r\n", b"\n") == source_bytes.replace(b"\r\n", b"\n"),
    })
with (ROOT / "RUNTIME_SOURCE_MATCH.json").open("x", encoding="utf-8") as stream:
    json.dump(records, stream, ensure_ascii=False, indent=2)
for record in records:
    print(record["module"], "exact_match", record["exact_byte_match"], "newline_normalized_match", record["newline_normalized_match"])
