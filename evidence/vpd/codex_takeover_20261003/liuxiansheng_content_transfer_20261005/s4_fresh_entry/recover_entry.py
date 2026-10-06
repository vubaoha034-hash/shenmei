import base64
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent.parent
sys.path.insert(0, str(ROOT))
from visual_memory.vpd_task_lock import digest as repository_digest

def sha(data):
    return hashlib.sha256(data).hexdigest()

def read_json(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8-sig"))

def save(name, obj):
    (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

manifest_path = "evidence/vpd/codex_takeover_20261003/liuxiansheng_content_transfer_20261005/DELIVERY_MANIFEST_S4.json"
manifest = read_json(manifest_path)
raw_response = json.loads((OUT / "DRIVE_RAW_RESPONSE.json").read_text(encoding="utf-8"))
drive = raw_response["structuredContent"]
data = base64.b64decode(drive["b64_string"], validate=True)
assert drive["id"] == manifest["drive"]["file_id"]
assert drive["mime_type"] == "image/png"
assert len(data) == drive["file_size_bytes"] == 62055
assert sha(data) == manifest["export"]["sha256"]
assert data[:8] == b"\x89PNG\r\n\x1a\n"
png = OUT / "S4_DRIVE_ORIGINAL.png"
png.write_bytes(data)
with Image.open(png) as im:
    size = list(im.size)
    mode = im.mode
    pixels = im.convert("RGBA").tobytes()
assert size == [960,1280]
drive_evidence = {
    "tool": "mcp__codex_apps__google_drive_fetch",
    "request": {"url":manifest["drive"]["url"],"download_raw_file":True,"include_base64":True},
    "route": "Explicit bounded legacy compatibility; metadata first; one 62055-byte raw fetch; no signed file_uri or known 403 materialization path requested.",
    "original_file_id":drive["id"],"original_file_name":drive["file_name"],
    "file_uri_id":drive["file_uri"]["file_id"],"mime_type":drive["mime_type"],
    "restored_file":str(png),"bytes":len(data),"sha256":sha(data),
    "manifest_sha256_match":True,"dimensions":size,"mode":mode,
    "decoded_rgba_sha256":sha(pixels),"authenticated_original_read_succeeded":True,
    "anonymous_access_checked":False,"upload_or_permission_change":False,
    "response_evidence":"DRIVE_RAW_RESPONSE.json",
    "response_evidence_sha256":sha((OUT / "DRIVE_RAW_RESPONSE.json").read_bytes()),
    "signed_bearer_urls_redacted_from_evidence":True,
    "restored_at_utc":datetime.now(timezone.utc).isoformat()
}
save("DRIVE_RECOVERY_EVIDENCE.json",drive_evidence)
figma_wrapper = json.loads((OUT / "FIGMA_COMPACT_ACTUAL_TOOL_RESULT.json").read_text(encoding="utf-8"))
figma = json.loads(next(x["text"] for x in figma_wrapper["content"] if x["type"] == "text" and x["text"].startswith("{")))
save("FIGMA_NODE_SNAPSHOT.json",figma)
recorded = read_json("evidence/vpd/codex_takeover_20261003/liuxiansheng_content_transfer_20261005/FIGMA_READBACK_S4.json")
native_paths = ["START_HERE.md","AGENTS.md","PROJECT_CONTROL_ADAPTER.json","VPD_PROJECT_ROADMAP.md","continuity/vpd/CURRENT_TASK_LOCK.json","continuity/vpd/LATEST_CHECKPOINT.json","continuity/vpd/codex_takeover_20261003/WORKER_CURRENT_REUSE.md"]
digests = [{"path":x,"sha256":repository_digest(ROOT/x),"raw_worktree_sha256":sha((ROOT/x).read_bytes()),"bytes":(ROOT/x).stat().st_size} for x in native_paths]
lock = read_json("continuity/vpd/CURRENT_TASK_LOCK.json")
cp = read_json("continuity/vpd/LATEST_CHECKPOINT.json")
adapter = read_json("PROJECT_CONTROL_ADAPTER.json")
unit = lock["codex_takeover"]["worker_continuation"]
experiment = unit["content_transfer_experiment"]
refs = [cp["task_lock"],adapter["task_lock"],adapter["workflow"],
        lock["codex_takeover"]["receipt"],lock["codex_takeover"]["reuse_entry"],
        lock["codex_takeover"]["authorization"],lock["codex_takeover"]["photo_protection"],
        unit["worker_contract"],unit["repair_authorization"],
        experiment["authorization"],experiment["copy_manifest"],experiment["delivery"],
        experiment["review"],experiment["supplemental_repair_allocation"],
        manifest["figma_readback"],manifest["drive_readback"],manifest["wordmark_svg"]["source"],
        manifest["wordmark_svg"]["provenance"],manifest["independent_review"],
        manifest["professional_review"],manifest["protected_photo"],manifest["methods"]]
source_names = {"build-wordmark.py","prepare-inputs.cjs","render-preview.cjs","FIGMA_ASSEMBLY_S4.js","FROZEN_SPEC.json","PROVENANCE.json","S4_WORDMARK.svg","REUSE_METHOD.json"}
refs += [x for x in manifest["production_sources"] if Path(x["path"]).name in source_names]
seen=set()
hashes=[]
for ref in refs:
    if ref["path"] in seen:
        continue
    seen.add(ref["path"])
    target=ROOT/ref["path"]
    actual=repository_digest(target) if target.is_file() else None
    raw_sha=sha(target.read_bytes()) if target.is_file() else None
    hashes.append({"path":ref["path"],"expected_sha256":ref["sha256"],"actual_sha256":actual,"raw_worktree_sha256":raw_sha,"match":actual==ref["sha256"]})
save("KEY_REFERENCE_HASHES.json",hashes)
state = {
    "read_at_utc":datetime.now(timezone.utc).isoformat(),
    "root":str(ROOT),"repository":lock["repository"],"branch":lock["branch"],
    "task_id":lock["current_task_id"],"revision":lock["revision"],"checkpoint_sequence":cp["sequence"],
    "stage":lock["current_stage"],"status":lock["status"],"next_required_action":lock["next_required_action"],
    "checkpoint_next_required_action":cp["next_required_action"],
    "adapter_next_required_action":adapter["current_mainline"]["next_required_action"],
    "adapter_task_id":adapter["current_mainline"]["task_id"],
    "checkpoint_task_ids":cp["active_task_ids"],
    "state_writer":lock["codex_takeover"]["state_writer"],"render_allowed":lock["render_allowed"],
    "content_transfer_human_acceptance":experiment["human_acceptance"],
    "content_transfer_review_verdict":manifest["review_verdict"],
    "formal_transfer_versions":manifest["formal_transfer_versions"],
    "typography_guide_tool_calls":manifest["typography_guide_tool_calls"],
    "tea_formal_versions":unit["budget"]["formal_versions_used"],"tea_revisions":unit["budget"]["revisions_used"],
    "legacy_takeover_human_verdict":lock["codex_takeover"]["human_verdict"],
    "tea_poster_human_verdict":unit["poster_human_verdict"],
    "frozen_photo":unit["frozen_source"],
    "digests":digests,
    "key_reference_hash_count":len(hashes),
    "key_reference_hash_mismatches":[x for x in hashes if not x["match"]],
    "figma_created_id_match":set(recorded["createdNodeIds"])==set(x["id"] for x in figma["nodes"]),
    "figma_actual_node_count":figma["nodeCount"],
    "figma_recorded_created_node_count":len(recorded["createdNodeIds"]),
    "figma_document_prose_count_observed_before_final_digest":28,
    "native_identity_consistent":cp["task_lock"]["revision"]==adapter["task_lock"]["revision"]==lock["revision"] and cp["task_lock"]["sha256"]==adapter["task_lock"]["sha256"]==sha((ROOT/"continuity/vpd/CURRENT_TASK_LOCK.json").read_bytes()) and lock["next_required_action"]==cp["next_required_action"]==adapter["current_mainline"]["next_required_action"]
}
save("STATE_DIGESTS.json",digests)
save("NATIVE_ENTRY_SNAPSHOT.json",state)
print(json.dumps({"drive":drive_evidence,"native_identity_consistent":state["native_identity_consistent"],"revision":state["revision"],"checkpoint_sequence":state["checkpoint_sequence"],"next_required_action":state["next_required_action"],"human_acceptance":state["content_transfer_human_acceptance"],"key_reference_hash_count":len(hashes),"key_reference_hash_mismatches":state["key_reference_hash_mismatches"],"figma_created_id_match":state["figma_created_id_match"],"figma_node_count":figma["nodeCount"]},ensure_ascii=False,indent=2))
