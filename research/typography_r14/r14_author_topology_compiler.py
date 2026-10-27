#!/usr/bin/env python3
"""R14 nonrendering stroke subgraph/topology decision compilation.
Learn *eligibility* for creator's 喜 restructuring across new characters.
It cannot fabricate the original calligrapher's aesthetic decisions.
"""
import hashlib,json,pathlib,urllib.request,urllib.parse,math,numpy as np

HERE=pathlib.Path(__file__).resolve().parent
LOCK=json.loads((HERE/"R14_TOPOLOGY_COMPILATION_FREEZE.json").read_text(encoding="utf8"))
COMMIT=LOCK["source_data"]["commit"]
TARGETS=[LOCK["source_glyph"],*LOCK["sample_family_exploratory"],*LOCK["frozen_unseen_holdout"],*LOCK["negative_controls"]]
def ghash(b):
  return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def fetch(ch):
  u=f"https://raw.githubusercontent.com/chanind/hanzi-writer-data/{COMMIT}/data/{urllib.parse.quote(ch)}.json"
  request=urllib.request.Request(u,headers={"User-Agent":"shenmei-R14-research/1.0"})
  with urllib.request.urlopen(request,timeout=22) as f:
    buf=f.read(85000)
  d=json.loads(buf)
  if len(d["strokes"])!=len(d["medians"]):raise ValueError("BAD_STROKE_COUNT_"+ch)
  return {"content":d,"original_git_blob_sha":ghash(buf),"download_len":len(buf)}
def descriptor(med):
  pts=np.asarray([p for s in med for p in s],dtype=np.float64)
  if pts.size==0:raise ValueError("NO_SOURCE_STROKES")
  lo=np.min(pts,axis=0); hi=np.max(pts,axis=0);size=np.maximum(hi-lo,1.)
  v=[]
  for stroke in med:
    ps=np.asarray(stroke,dtype=np.float64)
    q=ps[[0,len(ps)//2,len(ps)-1]]
    q=(q-lo)/size
    v.append(q)
  return np.asarray(v)
def score(ref,other):
  if len(ref)!=len(other):raise ValueError("STROKE_LENGTH_MISMATCH")
  rms=np.sqrt(np.sum((ref-other)**2,axis=-1))
  return float(np.mean(rms))
def find(ch,ref,source):
  m=source["content"]["medians"]
  n=LOCK["compiler"]["reference_consecutive_strokes"]
  if len(m)<n:
    return {"character":ch,"source_count":len(m),"eligibility":"ABSTAIN_NOT_SAME_TOPOLOGY",
      "reason":"SOURCE_HAS_FEWER_THAN_12_STROKES","best_score":None,"best_window":None,
      "source_git_blob_sha":source["original_git_blob_sha"]}
  candidates=[]
  for start in range(len(m)-n+1):
    cur=descriptor(m[start:start+n])
    candidates.append((score(ref,cur),start))
  s,st=min(candidates)
  threshold=LOCK["compiler"]["fixed_discovery_threshold"]
  eligible=bool(s<=threshold)
  obj={"character":ch,"source_count":len(m),"eligibility":"PLAN_CANDIDATE_ONLY" if eligible else "ABSTAIN_NOT_SAME_TOPOLOGY",
    "reason":"GLYPH_MORPHOLOGY_SIMILAR_TO_SOURCE_喜" if eligible else "STRUCTURAL_SIGNATURE_OUTSIDE_FROZEN_TOLERANCE",
    "best_score":round(s,6),"threshold":threshold,"best_window":[st,st+n-1],
    "source_git_blob_sha":source["original_git_blob_sha"],
    "graphic_reauthored":False,"source_artist_model_copied":False}
  if eligible:
    obj["compilation"]={
      "top_break_whole_stroke":st,
      "upper_mouth_bottom_stroke":st+5,
      "dot_stroke_pair":[st+6,st+7],
      "shared_horizontal_stroke":st+8,
      "lower_mouth_bottom_stroke":st+11,
      "operator_status":"STRUCTURAL_EDITS_ONLY_PROPOSED_NOT_EXECUTED",
      "rejection_conditions":["EDIT_CANNOT_PRESERVE_CHARACTER_IDENTITY","NO_VALID_SHARED_GRAPHIC_GESTURE","FAMILY_STYLE_NOT_COHERENT"]}
  return obj
def main():
  data={ch:fetch(ch) for ch in TARGETS}
  ref=descriptor(data[LOCK["source_glyph"]]["content"]["medians"])
  if len(ref)!=12:raise ValueError("REFERENCE_GLYPH_NOT_12_STROKES")
  out=[]
  for ch in TARGETS[1:]:
    p=find(ch,ref,data[ch])
    p["group"]="exploratory" if ch in LOCK["sample_family_exploratory"] else "heldout" if ch in LOCK["frozen_unseen_holdout"] else "negative"
    out.append(p)
  positive_exploratory=[x for x in out if x["group"]=="exploratory"]
  holdout=[x for x in out if x["group"]=="heldout"]
  negatives=[x for x in out if x["group"]=="negative"]
  gate=(len(holdout)==1 and len(negatives)==3 and 
        all(x["eligibility"].startswith("ABSTAIN") for x in negatives) and
        all(x["source_git_blob_sha"] for x in out))
  report={
    "schema":"vpd-r14-artist-source-topology-transfer-eligibility/1.0",
    "date":"2026-10-27",
    "source_creator":"梁志坚 / 放肆喜欢 喜",
    "firsthand":LOCK["original_creator"]["first_person_article"],
    "source_evidence":"R12_VERIFIED_REAL_ARTIST_LETTERING_STAGES_AND_NEW_DECISIONS_20261027.json",
    "dataset_source":f"chanind/hanzi-writer-data@{COMMIT}",
    "source_reference":{"glyph":"喜","sha":data["喜"]["original_git_blob_sha"],"strokes":12},
    "exact_glyphs_checked":len(data),
    "eligibility_test":out,
    "known_positive_examples":len(positive_exploratory),
    "unseen_holdout_eligible":sum(x["eligibility"]=="PLAN_CANDIDATE_ONLY" for x in holdout),
    "negative_control_false_positives":sum(x["eligibility"]=="PLAN_CANDIDATE_ONLY" for x in negatives),
    "new_glyph_pixels_generated":False,
    "glyph_topology_actually_edited":False,
    "printed_baseline_source_is_NOT_designers_source":True,
    "creator_edits_not_trained_as_visual_model":True,
    "independent_human_approval":False,
    "aesthetic_transfer_success":False,
    "valid_structural_compiler_gate":gate,
    "overall_stage":"CONDITIONAL_TOPOLOGY_PLAN_ONLY_NOT_ARTIST_QUALITY",
    "limitations":["Hanzi Writer data comes from Arphic font, independent of original expressive designer's visuals.",
      "Normalized median endpoint similarity is a structural proxy, not a true semantic radical recognizer.",
      "Even a positive structural match doesn't allow directly deleting strokes; changes require authored replacement contours and visual legibility checks.",
      "A planned edit is NOT demonstrated AI creativity; no stroke geometry, ink expression or human visual transfer passed."]
   }
  (HERE/"R14_SOURCE_TO_HOLDOUT_TOPOLOGY_COMPILATION.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
  print("R14_TOPOLOGY_GATE",json.dumps({
    "gate":gate,
    "exploratory": [(v["character"],v["eligibility"],v["best_score"]) for v in positive_exploratory],
    "heldout": [(v["character"],v["eligibility"],v["best_score"]) for v in holdout],
    "negatives": [(v["character"],v["eligibility"],v["best_score"]) for v in negatives],
    "design_success":False},ensure_ascii=False))
if __name__=="__main__":main()
