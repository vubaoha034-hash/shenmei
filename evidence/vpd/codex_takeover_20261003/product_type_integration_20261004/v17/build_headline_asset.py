"""One V17 asset: original alpha128 -> unchanged VTracer -> whole-phrase affine.
This bounded maker adapter writes assets and a technical preview only.
It does not edit the source raster, photography, business state or upstream.
"""
from pathlib import Path
import copy,hashlib,io,json,os,re,subprocess,sys,xml.etree.ElementTree as ET
import importlib.metadata
from PIL import Image,ImageChops,ImageFilter
import PIL
ROOT=Path(__file__).resolve().parents[5]
OUT=Path(__file__).resolve().parent
PRIVATE=ROOT/'.liu-visual-private/correct_source_typography/v17'
NS='{http://www.w3.org/2000/svg}'
ET.register_namespace('',NS[1:-1])
RUNTIME=Path('C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies')
SOURCE_SHA='57f469ed142b64b037827cd3df616b22c0435c70a2bad547278591ee7c31ad7a'
TRACE_SHA='2f02f6f795bfc43842cfdf493485f5750265f6b5a06ca6da36d55cb6a223c5c2'
S_SHA='7fd7777fed21100cb6b47bc305701476054263565e73246ac469d065aa080618'
BRAND_SHA='dd8e9e899393dc36eb3f5b1652bdbb740787d41a108ea6aa1eae05cb1368b1ff'
MASK_SHA='b567253a07b4689f2869b5013d07cb625705d09f4e525f64e6878ab6c8f482e4'
def sha(b):return hashlib.sha256(b).hexdigest()
def ref(p):return {'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size}
def xml(r):return (ET.tostring(r,encoding='unicode')+'\n').encode('utf-8')
def render(raw):
 code='const s=require('+json.dumps((RUNTIME/'node/node_modules/sharp').as_posix())+');let a=[];process.stdin.on("data",x=>a.push(x));process.stdin.on("end",async()=>process.stdout.write(await s(Buffer.concat(a)).ensureAlpha().png().toBuffer()));'
 env={k:v for k,v in os.environ.items() if k.upper() not in {'NODE_PATH','NODE_OPTIONS'}}
 raw=subprocess.run([str(RUNTIME/'node/bin/node.exe'),'-e',code],input=raw,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True,env=env).stdout
 return Image.open(io.BytesIO(raw)).convert('RGBA')
def main():
 source=PRIVATE/'headline-generated-01.png';trace=PRIVATE/'headline-alpha128-traced.svg'
 photo=ROOT/'.liu-visual-private/source_recovery_20261003/photography-local-reconstruction-final.png'
 brand=ROOT/'evidence/vpd/codex_takeover_20261003/continuous_typography_20261004/v9/brand.svg'
 mask=OUT.parent/'v16/foreground-protection.svg'
 for p,h in [(source,SOURCE_SHA),(trace,TRACE_SHA),(photo,S_SHA),(brand,BRAND_SHA),(mask,MASK_SHA)]:assert sha(p.read_bytes())==h,'FIXED_SOURCE_CHANGED:'+str(p)
 for name in ['headline.svg','headline-part-1.svg','brand.svg','foreground-protection.svg','LETTERING_PROVENANCE.json']:assert not (OUT/name).exists(),'OUTPUT_ALREADY_EXISTS'
 assert not (PRIVATE/'preview.png').exists(),'PREVIEW_ALREADY_EXISTS'
 sys.path.append('C:/Users/Administrator/AppData/Local/hermes/hermes-agent/venv/Lib/site-packages')
 import fontTools
 from fontTools.pens.boundsPen import BoundsPen
 from fontTools.svgLib.path import parse_path
 assert fontTools.__version__=='4.63.0'
 sys.path.insert(0,str(ROOT/'.liu-visual-private/dependencies/vtracer_0_6_15_cp312/site-packages'))
 import vtracer
 assert importlib.metadata.version('vtracer')=='0.6.15'
 im=Image.open(source);alpha=im.getchannel('A');binary=alpha.point(lambda v:0 if v>=128 else 255).convert('RGB');buf=io.BytesIO();binary.save(buf,format='PNG')
 replay=vtracer.convert_raw_image_to_svg(buf.getvalue(),img_format='png',colormode='binary',mode='spline',filter_speckle=0,corner_threshold=60,length_threshold=4.0,max_iterations=10,splice_threshold=45,path_precision=3)
 upstream=ET.parse(trace).getroot();assert [dict(n.attrib) for n in upstream]==[dict(n.attrib) for n in ET.fromstring(replay)],'ALPHA_TRACE_BINDING_MISMATCH'
 rows=[];paths=[];empty=[]
 for index,node in enumerate(upstream):
  if not node.get('d','').strip():empty.append(index);continue
  pen=BoundsPen(None);parse_path(node.get('d'),pen)
  if not pen.bounds:empty.append(index);continue
  match=re.fullmatch(r'translate\(([-.\d]+),([-.\d]+)\)',node.get('transform',''));assert match
  dx,dy=map(float,match.groups());x0,y0,x1,y1=pen.bounds;bounds=[x0+dx,y0+dy,x1+dx,y1+dy]
  rows.append({'upstream_index':index,'d_sha256':sha(node.get('d').encode()),'literal_source_transform':node.get('transform'),'source_curve_bounds':bounds})
  n=copy.deepcopy(node);n.set('fill','#F5F2E6');n.set('id','original-alpha-contour-'+str(index));paths.append(n)
 x0=min(r['source_curve_bounds'][0] for r in rows);y0=min(r['source_curve_bounds'][1] for r in rows);x1=max(r['source_curve_bounds'][2] for r in rows);y1=max(r['source_curve_bounds'][3] for r in rows)
 scale=0.285;tx=625-scale*x0;ty=400-scale*y0;affine=f'matrix({scale} 0 0 {scale} {tx} {ty})'
 defs=ET.Element(NS+'defs');clip=ET.SubElement(defs,NS+'clipPath',{'id':'S-product-negative-space','clipPathUnits':'userSpaceOnUse'})
 mask_root=ET.parse(mask).getroot();combined='M0 0H1536V1024H0Z'+''.join(n.get('d') for n in mask_root)
 ET.SubElement(clip,NS+'path',{'d':combined,'clip-rule':'evenodd'})
 def make(nodes,clipped=True):
  r=ET.Element(NS+'svg',{'width':'1536','height':'1024','viewBox':'0 0 1536 1024','fill':'none'})
  ET.SubElement(r,NS+'title').text='一杯茶，慢下来'
  r.append(copy.deepcopy(defs));outer=ET.SubElement(r,NS+'g',{'id':'V17-one-whole-sentence',**({'clip-path':'url(#S-product-negative-space)'} if clipped else {})})
  group=ET.SubElement(outer,NS+'g',{'transform':affine})
  for n in nodes:group.append(copy.deepcopy(n))
  return xml(r)
 whole=make(paths);rgba=render(whole);unclipped=render(make(paths,False));a=rgba.getchannel('A');bbox=a.getbbox()
 assert bbox and bbox[0]>=288 and bbox[1]>=400 and bbox[2]<=1328 and bbox[3]<=720,'OUTSIDE_TEXT_ALLOWANCE'
 removed=ImageChops.subtract(unclipped.getchannel('A'),a);assert removed.getbbox() is None,'PROTECTION_WOULD_CUT_GENERATED_STROKES'
 core=render(mask.read_bytes()).getchannel('A').filter(ImageFilter.MinFilter(7)).point(lambda v:255 if v==255 else 0)
 core_count=sum(core.histogram()[1:]);assert core_count==162052
 assert ImageChops.darker(a,core).getbbox() is None,'LETTERING_INTERSECTS_PRODUCT_CORE'
 # Transport-only correction: keep each original line's adjacent contours
 # together; the artwork, source d/transform and whole-phrase affine stay fixed.
 upper=[];lower=[]
 for p,row in zip(paths,rows):
  b=row['source_curve_bounds'];(upper if (b[1]+b[3])/2<525 else lower).append(p)
 chunks=[make(upper),make(lower)]
 layer=Image.new('RGBA',(1536,1024))
 for chunk in chunks:assert len(chunk.decode('utf-8'))<40000;layer.alpha_composite(render(chunk))
 assert ImageChops.difference(layer,rgba).getbbox(alpha_only=False) is None,'PART_RGBA_DIFFERS_FROM_WHOLE'
 preview=Image.open(photo).convert('RGBA');previous=Image.open(ROOT/'.liu-visual-private/correct_source_typography/v16/poster.png').convert('RGBA')
 brand_box=(104,96,400,256);preview.paste(previous.crop(brand_box),brand_box[:2]);preview.alpha_composite(rgba)
 diff=ImageChops.difference(preview.convert('RGB'),Image.open(photo).convert('RGB'))
 assert ImageChops.darker(diff.getchannel('R'),core).getbbox() is None and ImageChops.darker(diff.getchannel('G'),core).getbbox() is None and ImageChops.darker(diff.getchannel('B'),core).getbbox() is None,'PRODUCT_CORE_RGB_CHANGED'
 output={'headline.svg':whole,'upstream-alpha128-trace.svg':trace.read_bytes(),'brand.svg':brand.read_bytes(),'foreground-protection.svg':mask.read_bytes()}
 for i,chunk in enumerate(chunks,1):output[f'headline-part-{i}.svg']=chunk
 for name,raw in output.items():(OUT/name).write_bytes(raw)
 preview.save(PRIVATE/'preview.png');rgba.save(PRIVATE/'headline-render.png')
 report={'version':17,'copy':'一杯茶，慢下来','original_alpha':ref(source),'alpha_extrema':list(alpha.getextrema()),'alpha_threshold':128,'alpha128_mask_pixels':sum(alpha.histogram()[128:]),'trace':ref(OUT/'upstream-alpha128-trace.svg'),'upstream_path_count':len(upstream),'empty_paths_omitted':empty,'retained_paths':len(paths),'nonempty_paths_omitted':0,'source_to_output_contours':rows,'source_curve_bounds':[x0,y0,x1,y1],'one_whole_sentence_affine':affine,'actual_alpha_bbox_exclusive':list(bbox),'authorised_headline_rectangle':[288,400,1328,720],'brand_rectangle':[104,96,400,256],'product_core_pixels':core_count,'product_core_RGB_differences':0,'mask_removed_alpha_pixels':0,'transport_parts':len(chunks),'parts_RGBA_equal_to_whole':True,'outputs':{name:ref(OUT/name) for name in output},'private_preview':ref(PRIVATE/'preview.png'),'original_alpha_preserved':True,'source_trace_replay_all_path_attributes_equal':True,'software':{'VTracer':'Python0.6.15/SVG-generator0.6.12, MIT, upstream unchanged','FontTools':fontTools.__version__,'FontTools_role':'BoundsPen/svgLib path only; no fonts loaded','Pillow':PIL.__version__,'Python':sys.version},'licence_boundary':'Reference-informed generated phrase, not a licensed commercial font. Local vectorisation loads no font files and imports/traces no R commercial outlines; image generator backend/font mechanism is NOT_EXPOSED. Software MIT licences do not establish trademark clearance or aesthetic acceptance.','approximation_boundary':'Alpha128 binarisation, VTracer spline approximation with path_precision3 and constant ivory fill are transformations, not lossless source-raster reproduction. Original PNG retained. No per-character distortion or photography editing.','aesthetic_pass_claimed':False}
 (OUT/'LETTERING_PROVENANCE.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
 print(json.dumps({'paths':len(paths),'parts':len(chunks),'bbox':bbox,'affine':affine,'core':core_count,'mask_cut_pixels':0,'headline':report['outputs']['headline.svg'],'preview':report['private_preview']},ensure_ascii=False))
if __name__=='__main__':main()
