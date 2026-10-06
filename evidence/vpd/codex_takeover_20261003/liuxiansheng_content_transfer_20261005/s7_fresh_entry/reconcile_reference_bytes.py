from pathlib import Path
import json,hashlib,subprocess
root=Path(r"C:/Users/Administrator/OneDrive/文档/足球/shenmei-vpd-resume-20261006")
out=root/".liu-visual-private/s7_fresh_entry"
refs=json.loads((out/"NATIVE_REFERENCE_CHECK.json").read_text(encoding="utf-8"))
results=[]
for r in refs:
    if r.get("matches") is False and r["exists"]:
        raw=(root/r["path"]).read_bytes()
        git=subprocess.check_output(["git","-C",str(root),"show","HEAD:"+r["path"]])
        normalized=raw.replace(b"\r\n",b"\n")
        lf=hashlib.sha256(normalized).hexdigest()
        gsha=hashlib.sha256(git).hexdigest()
        results.append({"path":r["path"],"expected_sha256":r["expected_sha256"],"raw_worktree_sha256":r["actual_sha256"],"lf_normalized_sha256":lf,"head_git_blob_sha256":gsha,"lf_matches_expected":lf==r["expected_sha256"],"git_blob_matches_expected":gsha==r["expected_sha256"],"only_crlf_difference":normalized==git})
(out/"GIT_LF_REFERENCE_RECONCILIATION.json").write_text(json.dumps(results,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(results,ensure_ascii=False))

