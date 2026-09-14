#!/usr/bin/env python3
"""Prepare the bounded P1 typography-only distillation repair bench.

This transition does not generate any title artwork. It freezes the mother-reference
identity, the strong ordinary-typesetting baseline, the distilled-title arm, equal
budget, stop rules, and human-first acceptance before any new typography pixels.
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
VALIDATOR = ROOT / "visual_memory/vpd_p6_composition_state.py"
EVID = ROOT / "evidence/vpd/p1_typography_repair_v1/TYPOGRAPHY_ONLY_DISTILLATION_REPAIR_BENCH_V1.json"


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


def update_validator():
    text = VALIDATOR.read_text(encoding="utf-8")
    old = '    "P1_PREPARE_TYPOGRAPHY_ONLY_DISTILLATION_REPAIR_BENCH",\n}'
    new = '    "P1_PREPARE_TYPOGRAPHY_ONLY_DISTILLATION_REPAIR_BENCH",\n    "P1_EXECUTE_TYPOGRAPHY_ONLY_TITLE_BENCH",\n}'
    if old not in text and '"P1_EXECUTE_TYPOGRAPHY_ONLY_TITLE_BENCH"' not in text:
        raise SystemExit("validator ACTIONS anchor missing")
    if old in text:
        text = text.replace(old, new, 1)
    text = text.replace(
        'expected_focus = "P1" if action == "P1_PREPARE_TYPOGRAPHY_ONLY_DISTILLATION_REPAIR_BENCH" else "P6"',
        'expected_focus = "P1" if action.startswith("P1_") else "P6"',
        1,
    )
    anchor = '''        require(p6.get("final_pixel_validation_completed") is True, "FINAL_VALIDATION_NOT_COMPLETE")\n\n    require(not set(cp["completed"]) & set(cp["incomplete"]), "COMPLETED_AND_INCOMPLETE")'''
    replacement = '''        require(p6.get("final_pixel_validation_completed") is True, "FINAL_VALIDATION_NOT_COMPLETE")\n    elif action == "P1_EXECUTE_TYPOGRAPHY_ONLY_TITLE_BENCH":\n        require(all(v == 1 for v in used.values()), "CORRECTION_NOT_COMPLETE")\n        check_ref(root, lock["human_set_verdict_evidence"])\n        tr = lock.get("typography_repair", {})\n        require(tr.get("status") == "PREPARED_TITLE_ONLY_BENCH_READY", "TYPOGRAPHY_BENCH_NOT_READY")\n        require(tr.get("title_bench_render_allowed") is True, "TYPOGRAPHY_BENCH_RENDER_NOT_OPEN")\n        check_ref(root, tr["bench_plan"])\n        require(tr.get("phase") == "T1_TITLE_ONLY", "TYPOGRAPHY_BENCH_PHASE")\n\n    require(not set(cp["completed"]) & set(cp["incomplete"]), "COMPLETED_AND_INCOMPLETE")'''
    if anchor not in text and 'elif action == "P1_EXECUTE_TYPOGRAPHY_ONLY_TITLE_BENCH"' not in text:
        raise SystemExit("validator branch anchor missing")
    if anchor in text:
        text = text.replace(anchor, replacement, 1)
    VALIDATOR.write_text(text, encoding="utf-8")


def main():
    lock = load(LOCK)
    cp = load(CP)
    adapter = load(ADAPTER)
    if lock.get("revision") != 34:
        raise SystemExit("unexpected source revision")
    if lock.get("next_required_action") != "P1_PREPARE_TYPOGRAPHY_ONLY_DISTILLATION_REPAIR_BENCH":
        raise SystemExit("unexpected source action")
    if lock.get("p6_integrated_design", {}).get("formal_human_set_verdict") != "FAIL_TYPOGRAPHY_DISTILLATION_NOT_DEMONSTRATED":
        raise SystemExit("human typography failure verdict missing")

    recorded = now_iso()
    old_blob = git_blob("continuity/vpd/CURRENT_TASK_LOCK.json")

    bench = {
        "schema_version": "vpd-typography-only-distillation-repair-bench/v1",
        "bench_id": "TYPOGRAPHY_ONLY_DISTILLATION_REPAIR_BENCH_V1",
        "recorded_at": recorded,
        "status": "PREPARED_NOT_EXECUTED",
        "scope": "P1_TYPOGRAPHY_REPAIR_TITLE_ONLY_FIRST_GATE",
        "purpose": "Prove or falsify visible typography-distillation benefit before any poster reintegration. Photography cannot compensate for weak lettering.",
        "authority": {
            "human_failure": {
                "path": "evidence/vpd/p6_equal_budget_integrated_design_v1/P6_HUMAN_SET_VERDICT_TYPOGRAPHY_FAIL_20260914.json",
                "verdict": "FAIL_TYPOGRAPHY_DISTILLATION_NOT_DEMONSTRATED"
            },
            "workflow_correction": {
                "path": "evidence/vpd/project_roadmap_v1/TYPOGRAPHY_WORKFLOW_CORRECTION.json",
                "key_rule": "Figma composition is not itself a special Chinese lettering generator."
            },
            "aesthetic_charter": {
                "path": "AESTHETIC_SKILL_DESIGN_CHARTER.md",
                "policy": "Use a compact set of high-leverage visual variables; taste is human judged and must not be replaced by validators."
            }
        },
        "canonical_mother_reference": {
            "filename": "R1C-APPROVED-SHANYEJI-CANONICAL.jpg",
            "drive_file_id": "1fG2OQ7IphZfGnH1csu1qZKYCsyAMDOAZ",
            "manifest_path": "evidence/vpd/shanyeji/full_image_distillation_v1/CANONICAL_VISUAL_ANCHOR_MANIFEST.json",
            "sha256": "9a29fbdc7dd908017924bed270e8dfe18351519eed3fa7bc7001789f2a383414",
            "dimensions": [960, 1280],
            "allowed_role": "MOTHER_REFERENCE_FOR_MECHANISM_STUDY_ONLY",
            "literal_copy_forbidden": True
        },
        "visible_reference_mechanisms": {
            "facts": [
                "The three-character title behaves as one irregular high-mass graphic object rather than ordinary typeset text.",
                "Glyphs have unequal optical width, height, weight and center of gravity.",
                "The first character is substantially re-authored toward a semantic landscape form rather than being a stretched stock glyph.",
                "Counters, gaps and missing-stroke regions are designed as large negative-space structures, not random decorative cuts.",
                "Inter-glyph spacing and silhouette are optically asymmetric while remaining one first-read cluster.",
                "Surface erosion exists, but it is secondary to the structural lettering and is not sufficient evidence of family transfer."
            ],
            "brand_bound_do_not_copy": [
                "exact 山野集 contours",
                "exact missing-stroke locations",
                "exact orange thread path",
                "李家班 badge",
                "WANCE footer identity"
            ]
        },
        "title_tasks": [
            {"task_id": "T1_DOUFANG", "exact_copy": "豆坊"},
            {"task_id": "T1_CHAZUO", "exact_copy": "茶作"}
        ],
        "canvas": {
            "width": 1600,
            "height": 900,
            "background": "neutral light or neutral dark, identical within each A/B pair",
            "title_only": True,
            "photography": False,
            "support_copy": False,
            "logos_badges_motifs": False,
            "shadows_gradients_mockups": False,
            "surface_distress": False,
            "reason": "Isolate structural lettering quality before color, texture, support typography or photography can hide failure."
        },
        "high_leverage_variables": [
            {
                "id": "semantic_glyph_rebinding",
                "rule": "Each glyph must contain an authored structural move derived from the new word's meaning/process; do not paste literal ingredient icons or reuse 山野集 contours."
            },
            {
                "id": "unequal_optical_mass",
                "rule": "Deliberately vary glyph width, height, weight and center of gravity so the wordmark has authored internal hierarchy rather than two equal font boxes."
            },
            {
                "id": "counter_negative_space_topology",
                "rule": "Design counters, openings, voids and selective omissions as large coherent geometry that improves silhouette and reading; random notches do not count."
            },
            {
                "id": "wordmark_object_silhouette",
                "rule": "The two characters must resolve as one memorable irregular object with a strong outer contour at thumbnail scale."
            },
            {
                "id": "interglyph_tension",
                "rule": "Spacing, overlap or near-contact must be optically authored so the pair has tension and unity; default tracking is insufficient."
            },
            {
                "id": "surface_is_subordinate",
                "rule": "Texture, erosion, brushiness and distress are disabled in T1; structure must work before any surface treatment is allowed."
            }
        ],
        "arm_A_strong_ordinary_baseline": {
            "objective": "Represent what a competent designer can achieve quickly with mature Chinese display typography, not a deliberately weak control.",
            "allowed": [
                "choose a mature available CJK display typeface appropriate to each title",
                "choose weight",
                "optical kerning/tracking",
                "baseline/alignment adjustment",
                "per-glyph scale adjustment up to 8 percent when needed for optical balance"
            ],
            "forbidden": [
                "editing glyph vector contours",
                "cutting/removing strokes",
                "adding distress/erosion",
                "drawing custom semantic shapes",
                "using the failed P6 glyph vectors"
            ],
            "budget": "one primary build plus at most one aesthetic correction per title"
        },
        "arm_B_distilled_authored_lettering": {
            "objective": "Use the distilled structural mechanism to author new wordmarks whose visual identity cannot be explained as ordinary font selection plus stretching.",
            "requirements": [
                "A stock font may be used only as a legibility/proportion scaffold; unedited font outlines cannot be final contours.",
                "All six high-leverage variables must be visibly addressed, but exact shape decisions remain free.",
                "豆坊 may derive structural logic from bean/tofu craft and workshop/press relationships without literal bean or tofu icons.",
                "茶作 may derive structural logic from tea/leaf/process/rack/handwork relationships without literal leaf stickers.",
                "Do not force the same deformation recipe onto 豆坊 and 茶作."
            ],
            "hard_avoids": [
                "generic chopped bold sans",
                "same cut corners on every glyph",
                "simple horizontal/vertical stretching as the main design move",
                "fake calligraphy shortcut",
                "texture used to disguise ordinary typography",
                "mountain/badge/orange-thread token reuse as family proof"
            ],
            "budget": "one primary build plus at most one aesthetic correction per title"
        },
        "technical_retry_policy": {
            "wrong_character_or_unreadable_character": "technical invalid; log and retry without counting as aesthetic correction",
            "taste_failure": "counts; do not relabel as technical"
        },
        "blind_human_review": {
            "presentation": "Within each title pair, hide A/B labels and randomize Candidate 1 / Candidate 2 ordering.",
            "questions": [
                "Which candidate is better as a standalone Chinese wordmark?",
                "Does either candidate look authored rather than like a font with simple deformation?",
                "Which candidate has stronger silhouette, negative space, character relationship and memorability?"
            ],
            "assistant_known_labels_are_not_independent_blind_review": True
        },
        "title_gate": {
            "pass": "Distilled B is human-preferred over the strong ordinary baseline on both 豆坊 and 茶作, with visible structural/authored reasons and no character-correctness failure.",
            "split_or_tie": "At most one bounded typography-mechanism repair round, then repeat the same two-title test.",
            "fail": "If B loses either title after the bounded repair round, stop current typography compiler and do not reintegrate into posters.",
            "after_pass": "Open T2 support-typography hierarchy bench; poster/Figma reintegration remains blocked until T2 passes."
        },
        "preservation": {
            "retain_existing_photo_bases": True,
            "failed_p6_frames_remain_negative_evidence": True,
            "no_second_p6_correction_pass": True,
            "no_candidate_promotion": True,
            "no_second_family_golden_or_scale": True
        },
        "next_required_action": "P1_EXECUTE_TYPOGRAPHY_ONLY_TITLE_BENCH"
    }
    dump(EVID, bench)
    bench_ref = ref(EVID)

    lock["revision"] = 35
    lock["preserved_prior_revision"] = {
        "revision": 34,
        "git_blob_sha": old_blob,
        "note": "Revision 34 records the formal human P6 typography failure and returns only typography to a bounded P1 repair bench."
    }
    lock["current_stage"] = "P1 typography-only repair bench is prepared and frozen from the canonical mother reference and human P6 failure. T1 isolates standalone title structure for 豆坊 and 茶作: strong ordinary typesetting versus distilled authored lettering, no photography/support copy/texture. No pixels have been generated yet."
    lock["status"] = "VPD_P1_TYPOGRAPHY_REPAIR_BENCH_READY"
    lock["next_required_action"] = "P1_EXECUTE_TYPOGRAPHY_ONLY_TITLE_BENCH"
    lock["workflow"]["focus_stage"] = "P1"
    lock["typography_repair"] = {
        "status": "PREPARED_TITLE_ONLY_BENCH_READY",
        "bench_id": "TYPOGRAPHY_ONLY_DISTILLATION_REPAIR_BENCH_V1",
        "phase": "T1_TITLE_ONLY",
        "bench_plan": bench_ref,
        "preserve_photo_bases": True,
        "failed_p6_frames_are_negative_evidence": True,
        "title_bench_render_allowed": True,
        "poster_reintegration_allowed": False,
        "support_typography_bench_allowed": False,
        "next_required_action": "P1_EXECUTE_TYPOGRAPHY_ONLY_TITLE_BENCH"
    }
    lock["completed_this_revision"] = [
        "re-read the canonical 960x1280 Shanyeji mother reference identity and typography evidence",
        "isolated six high-leverage structural lettering variables without adding taste validators",
        "defined a strong ordinary CJK typesetting baseline rather than a deliberately weak control",
        "defined a distilled authored-lettering arm that forbids font-stretch/cut-corner shortcuts",
        "froze two title tasks: 豆坊 and 茶作, title-only with photography/support copy/texture disabled",
        "froze equal budget, blind human review, bounded retry and stop rules before generation"
    ]
    lock["blockers"] = [
        "Existing P6 compositions remain frozen negative evidence and cannot be polished further in place.",
        "Only the T1 standalone-title bench is authorized; poster reintegration and support typography remain blocked.",
        "The distilled title arm must visibly beat a strong ordinary typesetting baseline on both titles before T2 opens.",
        "Candidate promotion, second-family completion, Golden and Scale remain blocked."
    ]
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
        "event_id": "EVT-VPD-P1-TYPOGRAPHY-REPAIR-BENCH-PREPARED-20260914-001",
        "event_type": "P1_TYPOGRAPHY_ONLY_REPAIR_BENCH_PREPARED",
        "task_id": "VPD-SYSTEM-LEVEL-HOLDOUT-TRANSFER-VALIDATION-V1",
        "project_id": "visual-aesthetic-vpd",
        "recorded_at": recorded,
        "material": True,
        "previous_event_id": previous["event_id"] if previous else None,
        "previous_event_hash": previous["event_hash"] if previous else None,
        "lock_sha256": lock_sha,
        "authorization": {"source": "current controlling ChatGPT conversation", "instruction": "下一步", "scope": "prepare the next locked P1 typography-only repair bench"},
        "before": {"state": "VPD_P6_HUMAN_FAIL_TYPOGRAPHY_PROGRAM_REPAIR_REQUIRED", "typography_repair": "REQUIRED_NOT_STARTED"},
        "after": {"state": "VPD_P1_TYPOGRAPHY_REPAIR_BENCH_READY", "typography_repair": "PREPARED_TITLE_ONLY_BENCH_READY", "next_action": "P1_EXECUTE_TYPOGRAPHY_ONLY_TITLE_BENCH"},
        "evidence": [bench_ref["path"], lock["human_set_verdict_evidence"]["path"], "evidence/vpd/shanyeji/full_image_distillation_v1/TYPOGRAPHY_COMPONENT_GRAMMAR_V1.json", "evidence/vpd/shanyeji/style_capsule_v1_1_candidate/STYLE_CAPSULE_V1_1_CANDIDATE.json", "AESTHETIC_SKILL_DESIGN_CHARTER.md"],
        "reason": "The failed P6 implementation reduced distilled typography to generic font deformation. The repair isolates structural lettering against a strong ordinary baseline before any photo or support-type reintegration.",
        "remote_authority": {"repository": "vubaoha034-hash/shenmei", "branch": "visual-program-distillation-v2-photography-design-20260814"}
    }
    event["event_hash"] = event_hash(event)
    with LEDGER.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(event, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")

    cp["sequence"] = 57
    cp["recorded_at"] = recorded
    cp["current_focus"] = lock["current_stage"]
    if "p1_typography_only_distillation_repair_bench" not in cp["completed"]:
        cp["completed"].append("p1_typography_only_distillation_repair_bench")
    cp["incomplete"] = [
        "p1_typography_title_only_ab_execution",
        "p1_typography_support_hierarchy_bench",
        "p6_reintegration_after_typography_repair",
        "candidate_promotion",
        "second_style_family_validation",
        "golden",
        "scale"
    ]
    cp["blocked"] = lock["blockers"]
    cp["next_required_action"] = lock["next_required_action"]
    cp["current_focus"] = lock["current_stage"]
    cp["status"] = lock["status"]
    cp["task_lock"] = {"path": "continuity/vpd/CURRENT_TASK_LOCK.json", "sha256": lock_sha}
    cp["typography_repair"] = {
        "status": "PREPARED_TITLE_ONLY_BENCH_READY",
        "phase": "T1_TITLE_ONLY",
        "bench_plan": bench_ref,
        "title_tasks": ["豆坊", "茶作"],
        "title_bench_render_allowed": True,
        "poster_reintegration_allowed": False
    }
    cp["requirements"]["p6_integrated_design"]["status"] = "HUMAN_FAIL_TYPOGRAPHY_PROGRAM_REPAIR_REQUIRED"
    cp["ledger_tails"] = {"commercial_design_pipeline": {"event_id": event["event_id"], "event_hash": event["event_hash"]}}
    dump(CP, cp)

    adapter["vpd_system_goal_authority"]["checkpoint"] = lock["status"]
    adapter["vpd_system_goal_authority"]["next_required_action"] = lock["next_required_action"]
    adapter["vpd_system_goal_authority"]["render_allowed"] = False
    adapter["task_lock"]["revision"] = 35
    adapter["task_lock"]["sha256"] = lock_sha
    adapter["forward_commercial_pipeline"]["status"] = "P1_TYPOGRAPHY_REPAIR_TITLE_BENCH_READY"
    adapter["forward_commercial_pipeline"]["next_required_action"] = lock["next_required_action"]
    adapter["change_authorities"].insert(0, {**bench_ref, "priority": 0, "purpose": "Frozen P1 title-only typography repair bench: strong ordinary baseline versus distilled authored lettering before any poster reintegration."})
    dump(ADAPTER, adapter)

    update_validator()

    print(json.dumps({
        "status": "P1_TYPOGRAPHY_REPAIR_BENCH_PREPARED",
        "lock_revision": 35,
        "checkpoint_sequence": 57,
        "next_required_action": lock["next_required_action"],
        "bench_plan": bench_ref,
        "lock_sha256": lock_sha,
        "ledger_event_id": event["event_id"],
        "ledger_event_hash": event["event_hash"]
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
