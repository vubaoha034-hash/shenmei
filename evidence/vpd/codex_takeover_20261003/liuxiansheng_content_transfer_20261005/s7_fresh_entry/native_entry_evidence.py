from pathlib import Path
import json, hashlib, datetime, subprocess, zipfile, collections
ROOT=Path(r"C:/Users/Administrator/OneDrive/文档/足球/shenmei-vpd-resume-20261006")
OUT=ROOT/".liu-visual-private/s7_fresh_entry"
OUT.mkdir(parents=True,exist_ok=True)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p): return json.loads((ROOT/p).read_text(encoding="utf-8-sig"))
def dump(name,data):
    (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
native_paths=["PROJECT_CONTROL_ADAPTER.json","continuity/vpd/CURRENT_TASK_LOCK.json","continuity/vpd/LATEST_CHECKPOINT.json"]
adapter,lock,cp=[load(p) for p in native_paths]
wc=lock["codex_takeover"]["worker_continuation"]
receipt_ref=lock["codex_takeover"]["receipt"]
receipt=load(receipt_ref["path"])
exp=wc["content_transfer_experiment"]
delivery_ref=exp["delivery"]
delivery=load(delivery_ref["path"])
native=[{"path":p,"sha256":sha(ROOT/p),"size":(ROOT/p).stat().st_size} for p in native_paths]
checks={
 "adapter_lock_hash":adapter["task_lock"]["sha256"]==native[1]["sha256"],
 "checkpoint_lock_hash":cp["task_lock"]["sha256"]==native[1]["sha256"],
 "native_lock_revision":lock["revision"],
 "adapter_revision":adapter["task_lock"]["revision"],
 "checkpoint_revision":cp["task_lock"]["revision"],
 "revision_mirrors_match":lock["revision"]==adapter["task_lock"]["revision"]==cp["task_lock"]["revision"],
 "checkpoint_sequence":cp["sequence"],
 "status_mirrors_match":lock["status"]==cp["status"]==receipt["status"],
 "next_action_mirrors_match":lock["next_required_action"]==cp["next_required_action"]==receipt["next_required_action"],
 "receipt_sha_matches":sha(ROOT/receipt_ref["path"])==receipt_ref["sha256"],
 "current_delivery_sha_matches":sha(ROOT/delivery_ref["path"])==delivery_ref["sha256"],
 "workflow_sha_matches":sha(ROOT/adapter["workflow"]["path"])==adapter["workflow"]["sha256"],
 "reuse_sha_matches":sha(ROOT/adapter["workflow"]["current_bounded_delivery_entry"]["path"])==adapter["workflow"]["current_bounded_delivery_entry"]["sha256"]
}
refs=[]
def add(ref,location):
    if isinstance(ref,dict) and isinstance(ref.get("path"),str) and isinstance(ref.get("sha256"),str):
        refs.append((ref["path"],ref["sha256"],location))
for loc,ref in [
 ("adapter.task_lock",adapter["task_lock"]),("adapter.workflow",adapter["workflow"]),
 ("adapter.workflow.current_bounded_delivery_entry",adapter["workflow"]["current_bounded_delivery_entry"]),
 ("checkpoint.task_lock",cp["task_lock"]),("lock.codex_takeover.receipt",receipt_ref),
 ("lock.codex_takeover.reuse_entry",lock["codex_takeover"]["reuse_entry"]),
 ("lock.mainline_lock.plan",lock["mainline_lock"]["plan"]),("lock.mainline_lock.contract",lock["mainline_lock"]["contract"])
]:add(ref,loc)
for idx,ref in enumerate(receipt.get("artifact_refs",[])):add(ref,f"latest_receipt.artifact_refs[{idx}]")
for key,value in exp.items():add(value,"current_transfer."+key)
for key,value in delivery.items():add(value,"current_delivery."+key)
seen={}; ref_results=[]
for p,expected,loc in refs:
    key=(p,expected)
    if key in seen:
        seen[key]["locations"].append(loc);continue
    path=(ROOT/p)
    exists=path.is_file()
    excluded=p.replace("\\","/").startswith(".liu-visual-private/") or "runtime" in p.lower() or "/ROOT_ACTUAL_" in p.upper()
    entry={"path":p,"expected_sha256":expected,"locations":[loc],"exists":exists}
    if excluded:
        entry.update({"byte_hash_status":"NOT_READ_PRIVATE_OR_RUNTIME","actual_sha256":None,"matches":None})
    elif exists:
        actual=sha(path)
        entry.update({"byte_hash_status":"READ_PROJECT_REFERENCE","actual_sha256":actual,"matches":actual==expected})
    else:
        entry.update({"byte_hash_status":"MISSING","actual_sha256":None,"matches":False})
    seen[key]=entry;ref_results.append(entry)
entry_paths=["START_HERE.md","AGENTS.md","VPD_PROJECT_ROADMAP.md","continuity/vpd/MAINLINE_LOCK_20261001.md",
 "continuity/vpd/MAINLINE_CONTRACT_20261001.json","continuity/vpd/codex_takeover_20261003/WORKER_CURRENT_REUSE.md",
 receipt_ref["path"],delivery_ref["path"]]
scope={
 "scope":"WORKING_TREE_RECOVERY","same_machine":True,"no_github_publication_claim":True,
 "repository":lock["repository"],"branch":lock["branch"],
 "head":subprocess.check_output(["git","-C",str(ROOT),"rev-parse","HEAD"],text=True).strip(),
 "current_task_id":lock["current_task_id"],"current_stage":lock["current_stage"],"status":lock["status"],
 "next_required_action":lock["next_required_action"],"state_writer":lock["codex_takeover"]["state_writer"],
 "objective":lock["objective"],"frozen_source":wc["frozen_source"],"worker_budget":wc["budget"],
 "transfer_human_acceptance":exp["human_acceptance"],"transfer_delivery":delivery_ref,
 "delivery_identity":{k:delivery[k] for k in ["figma","export","drive","wordmark_svg","review_verdict","human_acceptance","formal_transfer_versions","typography_guide_tool_calls","whole_visual_system_complete"]},
 "entry_read_hashes":[{"path":p,"exists":(ROOT/p).is_file(),"sha256":sha(ROOT/p)}for p in entry_paths],
 "native":native,"mirror_checks":checks,
 "reference_summary":{"total_unique":len(ref_results),"hashed":sum(r["byte_hash_status"]=="READ_PROJECT_REFERENCE" for r in ref_results),
 "hash_matches":sum(r["matches"] is True for r in ref_results),"mismatched":sum(r["matches"] is False and r["exists"] for r in ref_results),
 "missing":sum(not r["exists"] for r in ref_results),"excluded_private_or_runtime":sum(r["byte_hash_status"]=="NOT_READ_PRIVATE_OR_RUNTIME" for r in ref_results)},
 "expected_public_fresh_entry_report":{"path":delivery["fresh_entry_report_path"],"exists":(ROOT/delivery["fresh_entry_report_path"]).is_file(),
 "status":"EXISTS" if (ROOT/delivery["fresh_entry_report_path"]).is_file() else "MISSING_NOT_COMPLETED"},
 "validator_or_tests_run":False
}
dump("NATIVE_ENTRY_EVIDENCE.json",scope);dump("NATIVE_REFERENCE_CHECK.json",ref_results)
source=load("evidence/vpd/codex_takeover_20261003/liuxiansheng_content_transfer_20261005/guide-adapter-s7/SOURCE.json")
expected={x["file"]:x["sha256"] for x in source["exact_inputs"]}
zip_path=OUT/"S7_REBUILD_INPUTS.zip"; archive_sha=sha(zip_path)
zip_details=[];DEST=OUT/"restored_inputs";DEST.mkdir(exist_ok=True)
with zipfile.ZipFile(zip_path) as z:
    info=z.infolist()
    names=[x.filename for x in info]
    if len(names)!=len(set(names)):raise ValueError("Duplicate ZIP members")
    if set(names)!=set(expected):raise ValueError("ZIP member names differ from SOURCE exact inputs")
    for member in info:
        relative=Path(member.filename)
        if relative.is_absolute() or ".." in relative.parts or member.is_dir():raise ValueError("Unsafe ZIP member")
        data=z.read(member)
        actual=hashlib.sha256(data).hexdigest()
        if actual!=expected[member.filename]:raise ValueError("ZIP input mismatch")
        destination=DEST/relative
        destination.parent.mkdir(parents=True,exist_ok=True)
        destination.write_bytes(data)
        zip_details.append({"file":member.filename,"size":len(data),"expected_sha256":expected[member.filename],"actual_sha256":actual,"matches":True,"restored_path":str(destination),"restored_sha256":sha(destination)})
zip_report={"source_manifest_sha256":sha(ROOT/"evidence/vpd/codex_takeover_20261003/liuxiansheng_content_transfer_20261005/guide-adapter-s7/SOURCE.json"),
 "archive_sha256":archive_sha,"expected_archive_sha256":"535cae9b6f7367ed3faf328c040a1d856b1bdb75962db6992890eba040f28861",
 "archive_sha_matches":archive_sha=="535cae9b6f7367ed3faf328c040a1d856b1bdb75962db6992890eba040f28861",
 "member_count":len(zip_details),"expected_member_count":11,"input_name_set_exact":True,"all_hashes_match":True,"members":zip_details,"no_rebuild_or_trace":True}
dump("ZIP_INPUT_VERIFICATION.json",zip_report)
print(json.dumps({"native":native,"mirrors":checks,"refs":scope["reference_summary"],"fresh_report":scope["expected_public_fresh_entry_report"],"zip_count":len(zip_details),"zip_all_hashes_match":True},ensure_ascii=False))

