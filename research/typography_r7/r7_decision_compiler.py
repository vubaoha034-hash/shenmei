#!/usr/bin/env python3
"""R7 human-documented design decision -> transferable conditional rule.
Source: https://www.hellofont.cn/article/229775 ("海浪", identical left 氵).
Research-only CONTROL-PLANE TEST. No glyph output and no aesthetics claimed.
This program is independent of any paid design software or generation model.
"""
from __future__ import annotations
import json

REFERENCE_CASE = "海浪"
SOURCE = "https://www.hellofont.cn/article/229775"
DATASET_COMMIT = "68d10a4b21150cae5e1ebbd223eed289cf32d90c"
# From actual chanind/hanzi-writer-data JSON: [stroke count, radStrokes, normalized X centroids
# of first three strokes, original blob SHA]. The centroid list is an auditable diagnostic,
# NOT original creator brush pressure or intent.
VERIFIED = {
 "江":[6,[0,1,2],[.173,.061,.084],"4fb2b227381ff901c9be5e4ebf7313784f97ce03"],
 "湖":[12,[0,1,2],[.191,.062,.087],"62bafe237e8d4095a888c1fb80afaca9115df833"],
 "清":[11,[0,1,2],[.177,.073,.116],"2aac34a81a0f1f4dc51d9b53c9100bdc6fdfcc91"],
 "河":[8,[0,1,2],[.193,.072,.104],"8450dfca95600dd073ec6e0d547267e45c22150f"],
 "波":[8,[0,1,2],[.158,.064,.079],"0dc564377b2d1de00e4858849c13f765ec6c9f7d"],
 "浪":[10,[0,1,2],[.162,.070,.117],"310eb1a768f3d09ebcd39791f9820d8cfbc3deb1"],
 "山":[3,[],[.467,.345,.957],"0d48c7e5ca8596271e6602d0c031d9971489c097"],
 "灯":[6,[0,1,2,3],[.070,.338,.169],"7c93a314147af42a73628aa3d88e28d5c03f5182"],
 "火":[4,[],[.136,.686,.317],"30b9baf27fc7802a4144fa20c016f0833f98b7"],
 "树":[9,[0,1,2,3],[.190,.255,.153],"8e95d5baa906b938d03f05d1cf41cd26b7573c1d"],
 "林":[8,[0,1,2,3],[.216,.243,.151],"83f566fae63ddd6fb4a278fdff5246f7c44f3044"],
 "木":[4,[],[.499,.433,.248],"46f52bd8a9e5baeb06bc20622497015ac1c31046"]
}
TRIALS = [("江湖","APPLICABLE"),("清河","APPLICABLE"),
          ("波浪","APPLICABLE"),("山河","NOT_APPLICABLE"),
          ("江山","NOT_APPLICABLE"),("灯火","NOT_APPLICABLE"),
          ("树木","NOT_APPLICABLE"),("云湖","INSUFFICIENT_SOURCE")]

def water_left(glyph):
    num,rad,centroids,_=VERIFIED[glyph]
    return rad == [0,1,2] and len(centroids)==3 and max(centroids)<.25 and num>=4

def decide(word):
    if len(word)!=2: raise ValueError("ONLY_TWO_CHARACTER_PROOF_OF_CONCEPT")
    if any(c not in VERIFIED for c in word):
        return {"word":word,"decision":"INSUFFICIENT_SOURCE",
                "reason":"Unknown source-authenticated component data. Fail closed."}
    if not all(water_left(c) for c in word):
        return {"word":word,"decision":"NOT_APPLICABLE",
                "reason":"Only apply the common-left-氵 motif when BOTH glyphs exhibit that component."}
    right=[VERIFIED[c][0]-3 for c in word]
    return {
      "word":word,"decision":"APPLICABLE","matching_structure":"left 氵",
      "reason":"Source designer uses shared radical rather than indiscriminate global stroke modification.",
      "creative_decisions":[
        "Fix each glyph structure before styling its shared radical.",
        "Explore a consistent gesture in the lower stroke of 氵 without copying source outlines.",
        "Balance the remaining components independently; do not enforce identical motif length.",
        "Check upper dots remain unmerged and leave readable breathing room next to right components.",
        "If the shared gesture damages structure, scale back or reject it."
      ],
      "right_hand_stroke_counts":right,
      "exception_if_unequal_density":abs(right[0]-right[1])>=4,
      "visual_quality":"NOT_TESTED",
      "pixels_generated":False
    }

def main():
    assert REFERENCE_CASE not in [w for w,_ in TRIALS], "SOURCE_LEAKAGE"
    tests=[]
    for word,expect in TRIALS:
        got=decide(word)
        tests.append({"word":word,"expect":expect,"actual":got["decision"],
                      "correct":got["decision"]==expect,"details":got})
    assert all(x["correct"] for x in tests)
    assert decide("湖江")["decision"]=="APPLICABLE"
    assert decide("江山")["decision"]=="NOT_APPLICABLE"
    known=[x for x in tests if x["expect"]!="INSUFFICIENT_SOURCE"]
    baseline=sum(x["expect"]=="APPLICABLE" for x in known)  # naive: style every word
    output={
      "source":SOURCE,"method_type":"CONDITIONAL_DECISION_OPERATOR_NOT_VISUAL_RENDERER",
      "reference_example":REFERENCE_CASE,"dataset_commit":DATASET_COMMIT,
      "results":tests,"known_condition_cases":len(known),
      "always_apply_baseline_correct":baseline,
      "conditioned_rule_correct":sum(x["correct"] for x in known),
      "unknown_cases_rejected":len(tests)-len(known),
      "limitations":[
        "Expected judgments are source-grounded but hand curated; NOT independently blinded.",
        "Source text contains the author's stepwise design demonstration, not ground-truth geometry of future glyphs.",
        "A structural applicability test is NOT a transfer success or human aesthetic assessment.",
        "No protected commercial font files or source artwork were copied."
      ],
      "next_gate":"Validate at least one visually new wordmark with matched baselines and true human aesthetic review."
    }
    print(json.dumps(output,ensure_ascii=False,indent=2))

if __name__=="__main__":main()
