#!/usr/bin/env python3
"""Record the P6 human set verdict: typography/distillation failed.

This transition preserves the accepted-enough photographic bases, freezes the failed
P6 compositions as evidence, and returns only the typography mechanism to a bounded
P1 typography-only repair bench. It does not authorize photo rerendering or a second
P6 correction pass.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "continuity/vpd/CURRENT_TASK_LOCK.json"
CP = ROOT / "continuity/vpd/LATEST_CHECKPOINT.json"
ADAPTER = ROOT / "PROJECT_CONTROL_ADAPTER.json"
LEDGER = ROOT / "continuity/vpd/state_ledger/commercial_design_pipeline.jsonl"
EVID = ROOT / "evidence/vpd/p6_equal_budget_integrated_design_v1/P6_HUMAN_SET_VERDICT_TYPOGRAPHY_FAIL_20260914.json"
TYPO_GRAMMAR = ROOT / "evidence/vpd/shanyeji/full_image_distillation_v1/TYPOGRAPHY_COMPONENT_GRAMMAR_V1.json"
DESIGN_GRAMMAR = ROOT / "evidence/vpd/shanyeji/full_image_distillation_v1/GRAPHIC_DESIGN_GRAMMAR_V1.json"
TYPO_WORKFLOW = ROOT / "evidence/vpd/project_roadmap_v1/TYPOGRAPHY_WORKFLOW_CORRECTION.json"


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def dump(p: Path, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha_file(p: Path):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def ref(p: Path):
    return {"path": p.relative_to(ROOT).as_posix(), "sha256": sha_file(p)}


def git_blob(path: str):
    return subprocess.check_output(["git", "rev-parse", f"HEAD:{path}"], cwd=ROOT, text=True).strip()


def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def event_hash(event_without_hash):
    raw = json.dumps(event_without_hash, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def main():
    lock = load(LOCK)
    cp = load(CP)
    adapter = load(ADAPTER)

    if lock.get("revision") != 33 or lock.get("state_profile") != "p6-composition/v1":
        raise SystemExit("unexpected source state; human verdict transition is revision-33-only")
    if lock.get("next_required_action") != "P6_WAIT_HUMAN_SET_VERDICT":
        raise SystemExit("unexpected source action")
    p6 = lock["p6_integrated_design"]
    if p6.get("formal_human_set_verdict") is not None:
        raise SystemExit("human verdict already recorded")
    if not p6.get("final_pixel_validation_completed"):
        raise SystemExit("final validation not complete")

    recorded = now_iso()
    old_blob = git_blob("continuity/vpd/CURRENT_TASK_LOCK.json")

    evidence = {
        "schema_version": "vpd-p6-human-set-verdict/v1",
        "recorded_at": recorded,
        "status": "HUMAN_SET_FAIL_TYPOGRAPHY_DISTILLATION_NOT_DEMONSTRATED",
        "scope": "P6_EQUAL_BUDGET_INTEGRATED_SET",
        "figma_file_key": p6["figma_file_key"],
        "page_id": p6["page"]["id"],
        "human_authority": "CURRENT_USER",
        "human_feedback_exact": "这个底图还可以。但是文字设计完全不行，甚至还不如随便用一个PS随便写的好看。这完全没有蒸馏设计效果。",
        "formal_set_verdict": "FAIL_TYPOGRAPHY_DISTILLATION_NOT_DEMONSTRATED",
        "preserve": {
            "photo_bases": "KEEP_AS_ACCEPTABLE_ENOUGH_FOR_TYPOGRAPHY_REPAIR_BENCH_NOT_FINAL_PHOTO_GOLDEN",
            "failed_figma_frames": "FREEZE_AS_NEGATIVE_EVIDENCE",
            "p3_p4_directional_photo_evidence": "PRESERVE_WITH_EXISTING_SCOPE_ONLY",
            "correction_budget_history": "PRESERVE_CONSUMED_1_OF_1"
        },
        "do_not_do": [
            "do not rerender tofu or tea base photography for this failure",
            "do not apply a second aesthetic correction pass to the failed P6 frames",
            "do not promote the current typography vectors as distilled lettering",
            "do not call Figma itself the typography-generation mechanism"
        ],
        "diagnosis": {
            "primary_failure": "TYPOGRAPHY_DISTILLATION_MECHANISM_NOT_DEMONSTRATED",
            "secondary_failures": [
                "display lettering lacks authored high-level glyph system",
                "support typography behaves like generic template furniture",
                "photo/type relationship remains overlay composition rather than a distilled integrated system",
                "cross-content brand distinctiveness remains too interchangeable"
            ],
            "workflow_bug": "The implementation collapsed special Chinese lettering into Noto Sans SC outline deformation inside Figma. The saved workflow had already warned that Figma composition is not a substitute for creating a high-quality Chinese lettering asset.",
            "reference_mechanisms_not_realized": [
                "unequal glyph mass as one authored display object",
                "carved counter/negative-space topology",
                "selective missing-stroke geometry",
                "controlled surface/material behavior",
                "optically asymmetric identity cluster",
                "three-read hierarchy and dense/quiet information rhythm"
            ]
        },
        "authority_evidence": {
            "typography_component_grammar": ref(TYPO_GRAMMAR),
            "graphic_design_grammar": ref(DESIGN_GRAMMAR),
            "typography_workflow_correction": ref(TYPO_WORKFLOW),
            "final_validation": lock["final_validation_evidence"],
            "correction_pass": lock["correction_pass_evidence"]
        },
        "repair_strategy": {
            "return_stage": "P1_TYPOGRAPHY_DISTILLATION_AND_JOINT_DESIGN_INPUT",
            "next_experiment": "TYPOGRAPHY_ONLY_DISTILLATION_REPAIR_BENCH_V1",
            "purpose": "Before reintegrating any poster, prove that a distilled title system visibly outperforms an ordinary professional Photoshop/Figma typography baseline on the same copy under symmetric effort.",
            "photo_regeneration_required": False,
            "figma_reintegration_allowed_now": False,
            "candidate_promotion_allowed": False
        },
        "next_required_action": "P1_PREPARE_TYPOGRAPHY_ONLY_DISTILLATION_REPAIR_BENCH"
    }
    dump(EVID, evidence)
    evid_ref = ref(EVID)

    lock["revision"] = 34
    lock["preserved_prior_revision"] = {
        "revision": 33,
        "git_blob_sha": old_blob,
        "note": "Revision 33 completed P6 final pixel/editability validation and waited for the human set verdict."
    }
    p6["status"] = "HUMAN_FAIL_TYPOGRAPHY_PROGRAM_REPAIR_REQUIRED"
    p6["formal_human_set_verdict"] = "FAIL_TYPOGRAPHY_DISTILLATION_NOT_DEMONSTRATED"
    p6["human_feedback_scope"] = "BOTTOM_IMAGES_ACCEPTABLE_ENOUGH; TYPOGRAPHY_COMPLETELY_FAILS; NO_VISIBLE_DISTILLATION_DESIGN_EFFECT"
    p6["final_pixel_validation_allowed"] = False
    lock["human_set_verdict_evidence"] = evid_ref
    lock["current_stage"] = "Human P6 set verdict is FAIL: the base photography is acceptable enough to retain, while the typography is completely unacceptable and does not visibly demonstrate distillation. The failure is returned to P1 typography-distillation mechanism design. Existing P6 frames are frozen as negative evidence; no photo rerender and no second P6 correction pass are authorized."
    lock["status"] = "VPD_P6_HUMAN_FAIL_TYPOGRAPHY_PROGRAM_REPAIR_REQUIRED"
    lock["next_required_action"] = "P1_PREPARE_TYPOGRAPHY_ONLY_DISTILLATION_REPAIR_BENCH"
    lock["workflow"]["focus_stage"] = "P1"
    lock["completed_this_revision"] = [
        "recorded the user's formal P6 human set FAIL verdict",
        "isolated the failure to typography distillation/design rather than the retained base photography",
        "confirmed the implementation violated the saved warning that Figma composition is not itself a special Chinese lettering generator",
        "froze the four failed P6 compositions as negative evidence and preserved their consumed correction budget",
        "returned only the typography mechanism to a bounded P1 typography-only repair bench before any future poster reintegration"
    ]
    lock["blockers"] = [
        "Current P6 typography is formally human-rejected and cannot be promoted or polished further in place.",
        "No second P6 aesthetic correction pass is authorized.",
        "Typography-only distilled-vs-ordinary baseline evidence must show visible benefit before poster reintegration.",
        "Candidate promotion, second-family completion, Golden and Scale remain blocked."
    ]
    lock["typography_repair"] = {
        "status": "REQUIRED_NOT_STARTED",
        "bench_id": "TYPOGRAPHY_ONLY_DISTILLATION_REPAIR_BENCH_V1",
        "preserve_photo_bases": True,
        "failed_p6_frames_are_negative_evidence": True,
        "next_required_action": "P1_PREPARE_TYPOGRAPHY_ONLY_DISTILLATION_REPAIR_BENCH"
    }
    lock["updated_at"] = recorded
    dump(LOCK, lock)
    lock_sha = sha_file(LOCK)

    previous = None
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        obj = json.loads(line)
        previous = {"event_id": obj["event_id"], "event_hash": obj["event_hash"]}
    event = {
        "schema_version": "upcp-state-ledger-event/v1",
        "stream_id": "commercial_design_pipeline",
        "event_id": "EVT-VPD-P6-HUMAN-TYPOGRAPHY-FAIL-20260914-001",
        "event_type": "P6_HUMAN_SET_FAIL_TYPOGRAPHY_DISTILLATION_NOT_DEMONSTRATED",
        "task_id": "VPD-SYSTEM-LEVEL-HOLDOUT-TRANSFER-VALIDATION-V1",
        "project_id": "visual-aesthetic-vpd",
        "recorded_at": recorded,
        "material": True,
        "previous_event_id": previous["event_id"] if previous else None,
        "previous_event_hash": previous["event_hash"] if previous else None,
        "lock_sha256": lock_sha,
        "authorization": {
            "source": "current controlling ChatGPT conversation",
            "authority": "user human set verdict",
            "exact_feedback": evidence["human_feedback_exact"]
        },
        "before": {
            "state": "FINAL_VALIDATION_COMPLETE_HUMAN_VERDICT_REQUIRED",
            "human_set_verdict": None
        },
        "after": {
            "state": "HUMAN_FAIL_TYPOGRAPHY_PROGRAM_REPAIR_REQUIRED",
            "human_set_verdict": evidence["formal_set_verdict"],
            "next_action": evidence["next_required_action"]
        },
        "evidence": [
            evid_ref["path"],
            lock["final_validation_evidence"]["path"],
            lock["correction_pass_evidence"]["path"],
            "evidence/vpd/shanyeji/full_image_distillation_v1/TYPOGRAPHY_COMPONENT_GRAMMAR_V1.json",
            "evidence/vpd/shanyeji/full_image_distillation_v1/GRAPHIC_DESIGN_GRAMMAR_V1.json",
            "evidence/vpd/project_roadmap_v1/TYPOGRAPHY_WORKFLOW_CORRECTION.json"
        ],
        "reason": "Human review accepts the photographic bases only as usable underlying images but rejects the typography completely and explicitly reports no visible distillation design effect. The repair therefore returns to the typography mechanism rather than polishing the failed posters or rerendering photography.",
        "remote_authority": {
            "repository": "vubaoha034-hash/shenmei",
            "branch": "visual-program-distillation-v2-photography-design-20260814"
        }
    }
    event["event_hash"] = event_hash(event)
    with LEDGER.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(event, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")

    cp["sequence"] = 56
    cp["recorded_at"] = recorded
    cp["current_focus"] = lock["current_stage"]
    if "human_set_verdict" not in cp["completed"]:
        cp["completed"].append("human_set_verdict")
    cp["incomplete"] = [
        "p1_typography_only_distillation_repair_bench",
        "p6_reintegration_after_typography_repair",
        "candidate_promotion",
        "second_style_family_validation",
        "golden",
        "scale"
    ]
    cp["blocked"] = list(lock["blockers"])
    cp["next_required_action"] = lock["next_required_action"]
    cp["status"] = lock["status"]
    cp["task_lock"] = {"path": "continuity/vpd/CURRENT_TASK_LOCK.json", "sha256": lock_sha}
    cp["p6"]["final_pixel_validation_allowed"] = False
    cp["p6"]["final_pixel_validation_completed"] = True
    cp["p6"]["assistant_set_recommendation"] = "FAIL_HOLD_NOT_COMMERCIAL_READY"
    cp["p6"]["formal_human_set_verdict"] = p6["formal_human_set_verdict"]
    cp["requirements"]["p6_integrated_design"]["status"] = "HUMAN_FAIL_TYPOGRAPHY_PROGRAM_REPAIR_REQUIRED"
    cp["requirements"]["candidate_promotion"] = "BLOCKED"
    cp["ledger_tails"] = {
        "commercial_design_pipeline": {
            "event_id": event["event_id"],
            "event_hash": event["event_hash"]
        }
    }
    dump(CP, cp)

    adapter["vpd_system_goal_authority"]["checkpoint"] = lock["status"]
    adapter["vpd_system_goal_authority"]["next_required_action"] = lock["next_required_action"]
    adapter["vpd_system_goal_authority"]["render_allowed"] = False
    adapter["task_lock"]["revision"] = 34
    adapter["task_lock"]["sha256"] = lock_sha
    adapter["forward_commercial_pipeline"]["status"] = "PAUSED_FOR_P1_TYPOGRAPHY_DISTILLATION_REPAIR"
    adapter["forward_commercial_pipeline"]["next_required_action"] = lock["next_required_action"]
    adapter["change_authorities"].insert(0, {
        **evid_ref,
        "priority": 0,
        "purpose": "Current human P6 set FAIL: retain usable base photography and return typography distillation to a bounded P1 repair bench."
    })
    dump(ADAPTER, adapter)

    print(json.dumps({
        "status": "P6_HUMAN_TYPOGRAPHY_FAIL_RECORDED",
        "lock_revision": 34,
        "checkpoint_sequence": 56,
        "next_required_action": lock["next_required_action"],
        "human_verdict_evidence": evid_ref,
        "lock_sha256": lock_sha,
        "ledger_event_id": event["event_id"],
        "ledger_event_hash": event["event_hash"]
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
