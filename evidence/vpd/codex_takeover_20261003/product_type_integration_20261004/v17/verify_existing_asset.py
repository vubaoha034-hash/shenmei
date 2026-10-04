"""Read-only V17 verification added after creation. Never calls maker.main.
Uses existing dependencies, in-memory tracing/rasterisation and stdout only.
--source-image is a read-only binding override for refusal checks.
"""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,importlib.metadata,io,json,re,sys
import xml.etree.ElementTree as ET
from PIL import Image,ImageChops,ImageFilter
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[4]
PRIVATE=ROOT/'.liu-visual-private/correct_source_typography/v17'
HANDOFF_SHA='94477b2790d717cb9d7ee05afd3f84b2ce5b4f1367d1390090af0330c9949b26'
BUILDER_SHA='c5b41f85fed13a638d585cd348a2c6333c80b143581eaf1b138798fb241b0db3'
SOURCE_SHA='57f469ed142b64b037827cd3df616b22c0435c70a2bad547278591ee7c31ad7a'
PHOTO_SHA='7fd7777fed21100cb6b47bc305701476054263565e73246ac469d065aa080618'
V16_SHA='db4b7e602c3c9d967b178e62c2234b6e4401ca1fc2325fef43bb9ac0d1474261'
FORMAL_SHA='7037751665c04f6f5d3a5aa59cdb4da7148b9d88769e70e790c612ae100f437d'
NS='{http://www.w3.org/2000/svg}'
def require(ok,reason):
 if not ok:raise ValueError(reason)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def read_bound(path,digest):
 raw=path.read_bytes();require(sha(raw)==digest,'SHA_BINDING_MISMATCH:'+path.name);return raw
def changed_mask(a,b):
 d=ImageChops.difference(a.convert('RGB'),b.convert('RGB'))
 return ImageChops.lighter(ImageChops.lighter(d.getchannel('R'),d.getchannel('G')),d.getchannel('B')).point(lambda v:255 if v else 0)
def count(mask):return sum(mask.histogram()[1:])
def check(source_override=None):
 handoff=json.loads(read_bound(OUT/'HANDOFF.json',HANDOFF_SHA))
 source=Path(source_override) if source_override else PRIVATE/'headline-generated-01.png'
 if not source.is_absolute():source=ROOT/source
 read_bound(source,SOURCE_SHA)
 files={}
 for scope in ['public_files','private_files']:
  for name,row in handoff[scope].items():
   raw=read_bound(ROOT/row['path'],row['sha256']);require(len(raw)==row['bytes'],'SIZE_MISMATCH:'+name);files[row['path']]=row['sha256']
 builder=OUT/'build_headline_asset.py';read_bound(builder,BUILDER_SHA)
 spec=importlib.util.spec_from_file_location('frozen_v17_maker_readonly_helpers',builder)
 maker=importlib.util.module_from_spec(spec);spec.loader.exec_module(maker)
 # Only the frozen pure serialiser and pipe renderer are reused; main is never called.
 sys.path.append('C:/Users/Administrator/AppData/Local/hermes/hermes-agent/venv/Lib/site-packages')
 import fontTools
 from fontTools.pens.boundsPen import BoundsPen
 from fontTools.svgLib.path import parse_path
 require(fontTools.__version__=='4.63.0','FONTTOOLS_VERSION_MISMATCH')
 sys.path.insert(0,str(ROOT/'.liu-visual-private/dependencies/vtracer_0_6_15_cp312/site-packages'))
 import vtracer
 require(importlib.metadata.version('vtracer')=='0.6.15','VTRACER_VERSION_MISMATCH')
 alpha=Image.open(source).getchannel('A');binary=alpha.point(lambda v:0 if v>=128 else 255).convert('RGB');buffer=io.BytesIO();binary.save(buffer,format='PNG')
 replay=vtracer.convert_raw_image_to_svg(buffer.getvalue(),img_format='png',colormode='binary',mode='spline',filter_speckle=0,corner_threshold=60,length_threshold=4.0,max_iterations=10,splice_threshold=45,path_precision=3)
 upstream=ET.parse(OUT/'upstream-alpha128-trace.svg').getroot()
 require([dict(n.attrib) for n in upstream]==[dict(n.attrib) for n in ET.fromstring(replay)],'ALPHA128_TRACE_ATTRIBUTES_MISMATCH')
 require(len(upstream)==84,'UPSTREAM_COUNT_MISMATCH');paths=[];rows=[];empty=[]
 for index,n in enumerate(upstream):
  if not n.get('d','').strip():empty.append(index);continue
  pen=BoundsPen(None);parse_path(n.get('d'),pen);require(pen.bounds is not None,'NONEMPTY_PATH_HAS_NO_BOUNDS')
  t=re.fullmatch(r'translate\(([-.\d]+),([-.\d]+)\)',n.get('transform',''));require(t is not None,'SOURCE_TRANSFORM_CHANGED')
  dx,dy=map(float,t.groups());x0,y0,x1,y1=pen.bounds;b=[x0+dx,y0+dy,x1+dx,y1+dy]
  rows.append({'upstream_index':index,'d_sha256':sha(n.get('d').encode()),'literal_source_transform':n.get('transform'),'source_curve_bounds':b})
  p=copy.deepcopy(n);p.set('fill','#F5F2E6');p.set('id','original-alpha-contour-'+str(index));paths.append(p)
 require(len(paths)==27 and len(empty)==57,'RETAINED_OR_EMPTY_COUNT_MISMATCH')
 provenance=json.loads((OUT/'LETTERING_PROVENANCE.json').read_text(encoding='utf-8'))
 require(rows==provenance['source_to_output_contours'] and empty==provenance['empty_paths_omitted'],'PROVENANCE_PATH_MAPPING_MISMATCH')
 x0=min(r['source_curve_bounds'][0] for r in rows);y0=min(r['source_curve_bounds'][1] for r in rows)
 affine=f'matrix(0.285 0 0 0.285 {625-0.285*x0} {400-0.285*y0})'
 require(affine==handoff['whole_phrase_affine']==provenance['one_whole_sentence_affine'],'AFFINE_MISMATCH')
 defs=ET.Element(NS+'defs');clip=ET.SubElement(defs,NS+'clipPath',{'id':'S-product-negative-space','clipPathUnits':'userSpaceOnUse'})
 mask_raw=(OUT/'foreground-protection.svg').read_bytes();mask_root=ET.fromstring(mask_raw)
 ET.SubElement(clip,NS+'path',{'d':'M0 0H1536V1024H0Z'+''.join(n.get('d') for n in mask_root),'clip-rule':'evenodd'})
 def make(nodes,clipped=True):
  r=ET.Element(NS+'svg',{'width':'1536','height':'1024','viewBox':'0 0 1536 1024','fill':'none'})
  ET.SubElement(r,NS+'title').text='一杯茶，慢下来';r.append(copy.deepcopy(defs))
  outer=ET.SubElement(r,NS+'g',{'id':'V17-one-whole-sentence',**({'clip-path':'url(#S-product-negative-space)'} if clipped else {})})
  group=ET.SubElement(outer,NS+'g',{'transform':affine})
  for p in nodes:group.append(copy.deepcopy(p))
  return maker.xml(r)
 whole=make(paths);require(whole==(OUT/'headline.svg').read_bytes(),'WHOLE_SVG_REPLAY_MISMATCH')
 upper=[];lower=[]
 for p,row in zip(paths,rows):
  b=row['source_curve_bounds'];(upper if (b[1]+b[3])/2<525 else lower).append(p)
 rgba=maker.render(whole);layer=Image.new('RGBA',(1536,1024));part_chars=[]
 for i,nodes in enumerate([upper,lower],1):
  part=make(nodes);require(part==(OUT/f'headline-part-{i}.svg').read_bytes(),'TRANSPORT_BYTES_MISMATCH');part_chars.append(len(part.decode('utf-8')))
  require(part_chars[-1]<40000,'TRANSPORT_TOO_LARGE');layer.alpha_composite(maker.render(part))
 require(ImageChops.difference(layer,rgba).getbbox(alpha_only=False) is None,'TRANSPORT_RGBA_MISMATCH')
 require(ImageChops.difference(rgba,Image.open(PRIVATE/'headline-render.png').convert('RGBA')).getbbox(alpha_only=False) is None,'FROZEN_HEADLINE_RENDER_MISMATCH')
 a=rgba.getchannel('A');require(list(a.getbbox())==[625,400,1008,595],'ALPHA_BBOX_MISMATCH')
 without_clip=maker.render(make(paths,False)).getchannel('A')
 removed_alpha=ImageChops.subtract(without_clip,a);added_alpha=ImageChops.subtract(a,without_clip)
 # Original creation promised no removed lettering; exact alpha equality is
 # diagnostic only because clipping can introduce one-step raster rounding.
 require(removed_alpha.getbbox() is None,'MASK_CUTS_LETTERING')
 core=maker.render(mask_raw).getchannel('A').filter(ImageFilter.MinFilter(7)).point(lambda v:255 if v==255 else 0)
 require(count(core)==162052 and ImageChops.darker(a,core).getbbox() is None,'PRODUCT_CORE_INTERSECTION')
 photo_path=ROOT/'.liu-visual-private/source_recovery_20261003/photography-local-reconstruction-final.png';read_bound(photo_path,PHOTO_SHA);photo=Image.open(photo_path).convert('RGBA')
 old_path=ROOT/'.liu-visual-private/correct_source_typography/v16/poster.png';read_bound(old_path,V16_SHA);old=Image.open(old_path).convert('RGBA')
 preview=Image.open(PRIVATE/'preview.png').convert('RGBA');expected=photo.copy();expected.paste(old.crop((104,96,400,256)),(104,96));expected.alpha_composite(rgba)
 require(ImageChops.difference(expected,preview).getbbox(alpha_only=False) is None,'PREVIEW_REPLAY_MISMATCH')
 touched=a.point(lambda v:255 if v else 0);touched.paste(255,(104,96,400,256));outside=ImageChops.invert(touched);preview_diff=changed_mask(preview,photo)
 require(ImageChops.darker(preview_diff,outside).getbbox() is None and ImageChops.darker(preview_diff,core).getbbox() is None,'PREVIEW_PHOTO_PROTECTION_FAILED')
 formal_path=PRIVATE/'poster.png';read_bound(formal_path,FORMAL_SHA);formal=Image.open(formal_path).convert('RGBA');require(formal.size==(1536,1024),'FORMAL_DIMENSIONS_MISMATCH')
 formal_allowance=Image.new('L',(1536,1024));formal_allowance.paste(255,(104,96,400,256));formal_allowance.paste(255,(616,400,1024,608));formal_outside=ImageChops.invert(formal_allowance);formal_diff=changed_mask(formal,photo)
 require(count(formal_outside)==1440640 and ImageChops.darker(formal_diff,formal_outside).getbbox() is None,'FORMAL_OUTSIDE_PROTECTION_FAILED')
 require(ImageChops.darker(formal_diff,core).getbbox() is None,'FORMAL_CORE_PROTECTION_FAILED')
 require(changed_mask(formal.crop((104,96,400,256)),old.crop((104,96,400,256))).getbbox() is None,'FORMAL_BRAND_CHANGED')
 return {'status':'PASS','mode':'READ_ONLY_EXISTING_V17','physical_asset_writes':0,'all_handoff_bound_files_verified':len(files),'alpha128_trace_paths':84,'nonempty_source_paths':27,'empty_source_paths':57,'all_source_output_path_attributes_equal':True,'whole_affine':affine,'whole_and_transport_bytes_replayed':True,'transport_RGBA_equal':True,'part_chars':part_chars,'headline_alpha_bbox':[625,400,1008,595],'mask_cut_pixels':count(removed_alpha),'mask_alpha_diagnostic':{'removed_alpha_pixels':count(removed_alpha),'added_alpha_pixels':count(added_alpha),'max_added_alpha':added_alpha.getextrema()[1],'max_removed_alpha':removed_alpha.getextrema()[1],'exact_alpha_equal':added_alpha.getbbox() is None and removed_alpha.getbbox() is None,'exact_equality_is_acceptance_requirement':False},'product_core_pixels':162052,'maker_preview_core_and_outside_RGB_diff_pixels':0,'maker_outside_pixels':count(outside),'formal_export_sha256':FORMAL_SHA,'formal_outside_pixels':1440640,'formal_core_and_outside_RGB_diff_pixels':0,'formal_brand_RGB_diff_pixels':0,'original_builder_main_called':False,'created_after_original_asset':True,'aesthetic_verdict':None}
def main():
 parser=argparse.ArgumentParser(description=__doc__,allow_abbrev=False);parser.add_argument('--source-image');args=parser.parse_args()
 try:result=check(args.source_image)
 except Exception as exc:
  print(json.dumps({'status':'REFUSED','mode':'READ_ONLY_EXISTING_V17','error':str(exc),'physical_asset_writes':0,'original_builder_main_called':False}));return 1
 print(json.dumps(result,ensure_ascii=False));return 0
if __name__=='__main__':sys.exit(main())
