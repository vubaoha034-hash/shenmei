from pathlib import Path
import json,hashlib,copy,xml.etree.ElementTree as ET,datetime
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'START_HERE.md').is_file());B=ROOT/'evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v13';B.mkdir(exist_ok=True)
src=B.parent/'v12/headline.svg';s=ROOT/'.liu-visual-private/source_recovery_20261003/photography-local-reconstruction-final.png'
assert hashlib.sha256(src.read_bytes()).hexdigest()=='fb8e4106184083a2a6e6eea88cbccc2f08ea8dc9c5a1d3bd50d7404c264ff89e'
assert hashlib.sha256(s.read_bytes()).hexdigest()=='7fd7777fed21100cb6b47bc305701476054263565e73246ac469d065aa080618'
review=json.loads((B.parent/'v12/pixel_review/PIXEL_REVIEW.json').read_text(encoding='utf-8'));assert review['verdict']=='AI_FAIL' and review['version']==12
for n in ['headline.svg','PROVENANCE.json']:assert not (B/n).exists()
NS='http://www.w3.org/2000/svg';ET.register_namespace('',NS);old=ET.parse(src).getroot();paths=old.findall('.//{'+NS+'}path');assert len(paths)==19
e=ET.Element('{'+NS+'}svg',{'width':'750','height':'215','viewBox':'380 405 750 215'});ET.SubElement(e,'{'+NS+'}title').text='一杯茶，慢下来'
for name,transform,group in [('cup_phrase','matrix(0.82 0 0 0.82 104.1 68)',paths[:10]),('leaf_and_plate_phrase','matrix(0.7 0 0 0.7 311.5 234.4887203457885)',paths[10:])]:
 g=ET.SubElement(e,'{'+NS+'}g',{'id':name,'transform':transform})
 for p in group:g.append(copy.deepcopy(p))
data=(ET.tostring(e,encoding='unicode')+'\n').encode('utf-8');outpaths=ET.fromstring(data).findall('.//{'+NS+'}path');assert [p.attrib for p in outpaths]==[p.attrib for p in paths]
def ref(p):return {'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
prov={'formal_version':13,'primary_change':'TWO_SMALLER_STAGGERED_PHRASE_BLOCKS_AROUND_EXISTING_CUP_AND_LEAF_PLATE','source':ref(src),'output':{'path':(B/'headline.svg').relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)},'exact_copy':'一杯茶，慢下来','all_19_source_path_attributes_preserved':True,'no_new_letterforms_or_leaf_icons':True,'transforms':[{'phrase':'一杯茶，','path_indices':[1,10],'matrix':[0.82,0,0,0.82,104.1,68]},{'phrase':'慢下来','path_indices':[11,19],'matrix':[0.7,0,0,0.7,311.5,234.4887203457885]}],'svg_dimensions':[750,215],'import_position':[380,405],'source_glyphs_not_deformed':True,'brand_preserved':'V9 unchanged','photography_preserved':ref(s),'overlay_envelopes':[[104,96,400,256],[380,408,708,512],[864,512,1128,616]],'bounded_guard_adaptation':'Three separate text envelopes for preserved brand and two distinct phrases. Existing permitted regions are unchanged; no larger umbrella box or product-protection waiver.','design_rationale':'Reduce long headline dominance; cup phrase optical left387 aligns with brand frame right387 and lies inside cup horizontal span; second phrase steps right/down into existing leaf/plate background. This is a Root layout decision to test, not an aesthetic pass.','imagegen_calls':0,'new_fonts':0,'photo_generations':0,'aesthetic_pass_claimed':False,'recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
with (B/'headline.svg').open('xb') as f:f.write(data)
with (B/'PROVENANCE.json').open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(prov,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'formal_version':13,'headline_sha256':prov['output']['sha256'],'source_paths_preserved':19,'new_letterforms':0,'photo_generations':0}))
