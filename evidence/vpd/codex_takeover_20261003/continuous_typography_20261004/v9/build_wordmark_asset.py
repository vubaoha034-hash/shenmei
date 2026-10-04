"""Build one V9 vector asset from the real, unmodified generated alpha trace.

VTracer upstream is unchanged. This adapter removes six sub-pixel detached
components, crops to the retained actual path bounds and sets one ivory fill.
It never generates artwork, writes business state or changes photography.
"""
from pathlib import Path
import argparse,copy,hashlib,io,json,re,sys,xml.etree.ElementTree as ET
import importlib.metadata
from PIL import Image

ROOT=Path(__file__).resolve().parents[5]
OUT=Path(__file__).resolve().parent
PRIVATE=ROOT/'.liu-visual-private/correct_source_typography/v9'
SOURCE_SHA='98c03d0c04199840b1f25452ecbc42ebbda254f8c4855898094c60341c2b05f1'
TRACE_SHA='8f1c84e9551f1e911c32414162a486cecff4d94f6ea92887b95c91c5cefe4f56'
P_SHA='57c21466512a79cbb25c75db1d6a1748b595c3bc2d00c85ba51615557f74f925'
S_SHA='7fd7777fed21100cb6b47bc305701476054263565e73246ac469d065aa080618'
NS='http://www.w3.org/2000/svg';ET.register_namespace('',NS)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return {'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size}
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--fonttools-site');parser.add_argument('--verify-only',action='store_true');args=parser.parse_args()
 if args.fonttools_site:sys.path.append(args.fonttools_site)
 import fontTools
 from fontTools.pens.boundsPen import BoundsPen
 from fontTools.svgLib.path import parse_path
 assert fontTools.__version__=='4.63.0','PINNED_GEOMETRY_DEPENDENCY_REQUIRED'
 source=PRIVATE/'wordmark-generated-01.png';traced=PRIVATE/'wordmark-traced-01.svg'
 p=ROOT/'.liu-visual-private/correct_source_typography/v8/packet/P.png'
 frozen=ROOT/'.liu-visual-private/source_recovery_20261003/photography-local-reconstruction-final.png'
 assert sha(source)==SOURCE_SHA and sha(p)==P_SHA and sha(frozen)==S_SHA
 assert sha(traced)==TRACE_SHA,'TRACE_IDENTITY_MISMATCH_BEFORE_ANY_WRITE'
 sys.path.insert(0,str(ROOT/'.liu-visual-private/dependencies/vtracer_0_6_15_cp312/site-packages'))
 import vtracer
 assert importlib.metadata.version('vtracer')=='0.6.15','PINNED_VTRACER_REQUIRED'
 with Image.open(source) as im:
  alpha=im.getchannel('A')
  assert alpha.getextrema()==(0,255)
  mask=alpha.point(lambda value:0 if value>=128 else 255).convert('RGB')
  buffer=io.BytesIO();mask.save(buffer,format='PNG')
 replay=vtracer.convert_raw_image_to_svg(buffer.getvalue(),img_format='png',colormode='binary',mode='spline',filter_speckle=0,corner_threshold=60,length_threshold=4.0,max_iterations=10,splice_threshold=45,path_precision=3)
 original_paths=[dict(node.attrib) for node in ET.parse(traced).getroot()]
 replay_paths=[dict(node.attrib) for node in ET.fromstring(replay)]
 assert replay_paths==original_paths,'TRACE_NOT_DERIVED_FROM_BOUND_GENERATED_ALPHA'
 binding={'source_sha256':SOURCE_SHA,'trace_sha256':TRACE_SHA,'actual_alpha_replay':'PASS_ALL_PATH_ATTRIBUTES_EQUAL','paths_including_empty':len(original_paths),'fontTools':fontTools.__version__,'vtracer':'0.6.15','physical_writes':0}
 if args.verify_only:
  print(json.dumps(binding,ensure_ascii=False));return
 destinations=[OUT/'brand.svg',OUT/'upstream-alpha-trace.svg',OUT/'LETTERING_PROVENANCE.json']
 for d in destinations:
  if d.exists():raise FileExistsError(d)
 rows=[];retained=[];empty=0
 for index,node in enumerate(ET.parse(traced).getroot()):
  if not node.get('d','').strip():empty+=1;continue
  pen=BoundsPen(None);parse_path(node.get('d'),pen)
  if not pen.bounds:empty+=1;continue
  transform=re.fullmatch(r'translate\(([-.\d]+),([-.\d]+)\)',node.get('transform',''));assert transform
  x0,y0,x1,y1=pen.bounds;tx,ty=map(float,transform.groups())
  bounds=[x0+tx,y0+ty,x1+tx,y1+ty];area=(x1-x0)*(y1-y0)
  keep=area>=128;rows.append({'upstream_index':index,'bounds':bounds,'bounding_area':area,'retained':keep})
  if keep:
   element=copy.deepcopy(node);element.set('fill','#F5F2E6');element.set('id',f'original-alpha-contour-{index}');retained.append(element)
 assert len(retained)==7 and sum(not r['retained'] for r in rows)==6
 kept=[r['bounds'] for r in rows if r['retained']]
 x0=min(b[0] for b in kept);y0=min(b[1] for b in kept);x1=max(b[2] for b in kept);y1=max(b[3] for b in kept)
 w,h=x1-x0,y1-y0
 svg=ET.Element(f'{{{NS}}}svg',{'width':str(w),'height':str(h),'viewBox':f'0 0 {w} {h}'})
 ET.SubElement(svg,f'{{{NS}}}title').text='茶作'
 group=ET.SubElement(svg,f'{{{NS}}}g',{'transform':f'translate({-x0},{-y0})'})
 for element in retained:group.append(element)
 (OUT/'brand.svg').write_text(ET.tostring(svg,encoding='unicode')+'\n',encoding='utf-8',newline='\n')
 (OUT/'upstream-alpha-trace.svg').write_bytes(traced.read_bytes())
 report={'schema_version':'vpd-v9-lettering-provenance/v1','formal_version':9,'brand':'茶作','source':ref(source),'calibration_gesture_reference':ref(p),'reference_role':'Actual approved typography gesture and character anatomy; full P photography/copy/layout excluded. This is reference-derived creation, not a wholly unseen calibration test.','image_tool':'BUILT_IN_IMAGE_GEN','backend_model':'NOT_EXPOSED','imagegen_operations':1,'original_generated_alpha_preserved':True,'alpha_threshold':128,'vectorizer':'VTracer Python0.6.15 / SVG label0.6.12 MIT, core unchanged','trace':ref(OUT/'upstream-alpha-trace.svg'),'path_bounds':rows,'empty_paths_omitted':empty,'detached_components_omitted':6,'omission_basis':'All omitted bounding areas are <=20 source pixels^2, becoming sub-pixel at 275px placement; retained strokes start at area12402.32. No meaningful stroke omitted.','actual_bounds':[x0,y0,x1,y1],'retained_paths':7,'brand_asset':ref(OUT/'brand.svg'),'geometry_dependency':{'fontTools':fontTools.__version__,'use':'BoundsPen/svgLib path only, no font loaded','site_arg':args.fonttools_site},'font_software_used':None,'photography_regenerated':False,'frozen_photo':ref(frozen),'aesthetic_pass_claimed':False,'source_trace_binding':binding}
 (OUT/'LETTERING_PROVENANCE.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
 print(json.dumps({'brand_asset':report['brand_asset'],'retained_paths':7,'bounds':report['actual_bounds'],'placement_width':275,'height':h*275/w},ensure_ascii=False))
if __name__=='__main__':main()
