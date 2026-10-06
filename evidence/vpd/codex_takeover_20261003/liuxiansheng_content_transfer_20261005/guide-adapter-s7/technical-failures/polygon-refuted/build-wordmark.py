"""One frozen S7 build: five authored envelopes + 1:1 JPEG donor graded cream opacity."""
import pathlib,sys,json,hashlib,re,xml.etree.ElementTree as ET,argparse
from PIL import Image
import numpy as np
cli=argparse.ArgumentParser();cli.add_argument('--root',type=pathlib.Path);cli.add_argument('--output-dir',type=pathlib.Path);args=cli.parse_args()
BASE=args.output_dir.resolve() if args.output_dir else pathlib.Path(__file__).resolve().parent
ROOT=args.root.resolve() if args.root else next(p for p in BASE.parents if (p/'PROJECT_CONTROL_ADAPTER.json').exists())
VDEP=ROOT/'.liu-visual-private/dependencies/vtracer_0_6_15_cp312/site-packages';PDEP=ROOT/'.liu-visual-private/dependencies/skia_pathops_0_9_2_abi3/site-packages'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(VDEP/'vtracer/vtracer.cp312-win_amd64.pyd')=='59e2053fca8666479e7163eec45d8b15143435c7a8d14f6dbd26eec9716bfe66'
sys.path[:0]=[str(VDEP),str(PDEP)]
import vtracer,pathops,importlib.metadata
assert importlib.metadata.version('vtracer')=='0.6.15' and pathops.__version__=='0.9.2'
from vector_adapter import parse_svg_path,source_matrix,union_all,svg_d
spec=json.loads((BASE/'S7_FROZEN_METHOD.json').read_text(encoding='utf8'));assert spec['plan_frozen']
B=ROOT/'evidence/vpd/codex_takeover_20261003/liuxiansheng_content_transfer_20261005';S6PATHS=B/'EXPERT_S6_FROZEN_PATHS.json'
assert sha(S6PATHS)==spec['base_paths_sha256']
basepaths=json.loads(S6PATHS.read_text(encoding='utf8'))['paths']
assert all(spec['paths'][k]==basepaths[k] for k in spec['unchanged_path_names'])
assert set(k for k in basepaths if basepaths[k]!=spec['paths'][k])==set(spec['changed_path_names'])
REF=ROOT/'.liu-visual-private/product-type-integration-20261004/SHANYEJI-canonical-readback-20261005.jpg';assert sha(REF)==spec['texture']['reference_sha256']
donor=json.loads((BASE/'REFERENCE_DONOR_TILES.json').read_text(encoding='utf8'));origins=donor['origins_xy'];assert len(origins)==264
rgb=np.array(Image.open(REF).convert('RGB'));tiles=[rgb[y:y+8,x:x+8,:].copy() for x,y in origins]
texture=np.empty((192,584,3),dtype=np.uint8)
for j in range(24):
 for i in range(73):texture[j*8:j*8+8,i*8:i*8+8]=tiles[(j*73+i)%264]
darkness=244-texture.astype(np.float64).mean(axis=2);tier=np.digitize(darkness,[10,25,55,110,165]).astype(np.uint8)
before_counts=np.bincount(tier.ravel(),minlength=6).tolist()
protected=np.zeros(tier.shape,dtype=bool)
yy,xx=np.mgrid[420:612,216:800]
for box in spec['texture']['join_protection_boxes_final_xyxy'].values():
 x0,y0,x1,y1=box;protected|=(xx+.5>=x0)&(xx+.5<x1)&(yy+.5>=y0)&(yy+.5<y1)
downgraded=protected&(tier>=3);tier[downgraded]=2
Image.fromarray(texture).save(BASE/'REFERENCE_DONOR_TILE_FIELD_TECHNICAL.png')
Image.fromarray(tier).save(BASE/'TIER_INDEX_FIELD_TECHNICAL.png')
strokes={name:parse_svg_path(d) for name,d in spec['paths'].items()};solid=union_all(strokes.values());matrix=(567/717,0,0,170/269,29.46443514644352,128.91821561338293);finalsolid=solid.transform(*matrix)
params=dict(colormode='binary',mode='polygon',filter_speckle=0,path_precision=2)
clipped=[];trace_records=[]
for t in range(1,6):
 full=np.zeros((1280,960),dtype=np.uint8);full[420:612,216:800]=(tier==t).astype(np.uint8)
 infile=BASE/f'TIER_{t}_TRACE_INPUT.png';outfile=BASE/f'TIER_{t}_TRACE.svg'
 Image.fromarray(255-full*255).save(infile)
 cache=json.loads((BASE/'TECHNICAL_TRACE_REUSE.json').read_text()) if (BASE/'TECHNICAL_TRACE_REUSE.json').exists() else {}
 if str(t) in cache:
  assert sha(infile)==cache[str(t)]['input_sha256'] and sha(outfile)==cache[str(t)]['output_sha256']
 else:vtracer.convert_image_to_svg_py(str(infile),str(outfile),**params)
 paths=[]
 for node in ET.parse(outfile).getroot().iter():
  if node.tag.rsplit('}',1)[-1]=='path':paths.append(parse_svg_path(node.attrib['d'],source_matrix(node.attrib.get('transform'))))
 whole=pathops.Path()
 for p in paths:whole.addPath(p)
 part=pathops.op(finalsolid,whole,pathops.PathOp.INTERSECTION);clipped.append(part)
 trace_records.append({'tier':t,'mask_pixels':int(full.sum()),'input':infile.name,'input_sha256':sha(infile),'output':outfile.name,'output_sha256':sha(outfile),'trace_paths':len(paths),'reused_verified_trace':str(t) in cache,'clipped_area_final_px2':float(part.area),'clipped_contours':len(list(part.contours))})
alltiers=pathops.Path()
for p in clipped:alltiers.addPath(p)
base=pathops.op(finalsolid,alltiers,pathops.PathOp.DIFFERENCE)
cream_shapes=[base,*clipped[:4]];opacities=[1,.92,.8,.6,.35];cream=[]
for i,(p,opacity) in enumerate(zip(cream_shapes,opacities)):
 cream.append(f'<path id="S7_CREAM_TIER_{i}" fill="#fdf4e5" fill-opacity="{opacity}" fill-rule="nonzero" d="{svg_d(p)}"/>')
s6=(BASE/'S6_WORDMARK.svg').read_text(encoding='utf8');groups=re.findall(r'<g id="ORANGE_(?:BEHIND_GLYPHS|IN_FRONT_OF_GLYPHS)">[\s\S]*?</g>',s6);assert len(groups)==2
svg='<svg xmlns="http://www.w3.org/2000/svg" width="960" height="1280" viewBox="0 0 960 1280"><title>刘先生 S7 frozen facets and actual-reference graded wear</title>'+groups[0]+'<g id="CREAM_WORDMARK">'+''.join(cream)+'</g>'+groups[1]+'</svg>\n'
ET.fromstring(svg);assert all(t not in svg for t in ['<image','data:','foreignObject'])
(BASE/'S7_WORDMARK.svg').write_text(svg,encoding='utf8',newline='\n')
# Solid same-candidate diagnostic for open-space/alpha stats, not alternative asset.
(BASE/'S7_SOLID_TECHNICAL.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="960" height="1280" viewBox="0 0 960 1280"><path fill="#fdf4e5" d="'+svg_d(finalsolid)+'"/></svg>',encoding='utf8')
connections={a+'__'+b:float(pathops.op(strokes[a],strokes[b],pathops.PathOp.INTERSECTION).area) for a,b in [('XIAN_UPPER_CLUSTER','XIAN_MIDDLE_BAR'),('XIAN_MIDDLE_BAR','XIAN_LEFT_LEG'),('XIAN_MIDDLE_BAR','XIAN_RIGHT_HOOK'),('SHENG_MAIN_STEM','SHENG_BASE_BAR')]}
assert all(v>0 for v in connections.values())
mutual={f'{i+1}_{j+1}':float(pathops.op(clipped[i],clipped[j],pathops.PathOp.INTERSECTION).area) for i in range(5) for j in range(i+1,5)}
receipt={'schema':'s7-wordmark-provenance/v1','status':'IMPLEMENTED_PENDING_COLD_REVIEW','spec_sha256':sha(BASE/'S7_FROZEN_METHOD.json'),'base_paths_sha256':sha(S6PATHS),'reference_sha256':sha(REF),'reference_donor_sha256':sha(BASE/'REFERENCE_DONOR_TILES.json'),'S6_svg_sha256':sha(BASE/'S6_WORDMARK.svg'),'changed_path_names':spec['changed_path_names'],'unchanged9path_strings_exact':True,'texture':'Actual JPEG RGB donor tiles1:1, graded cream fill opacity; original alpha UNKNOWN','grid':[73,24],'donors':264,'new_randomness':False,'resampling':False,'old_S6_grain_used':False,'tier_field_before_protection_counts':before_counts,'tier_field_after_protection_counts':np.bincount(tier.ravel(),minlength=6).tolist(),'protected_deep_pixels_downgraded_to_tier2':int(downgraded.sum()),'trace_generation_calls':5,'trace_params':params,'trace_records':trace_records,'tier_mutual_overlap_area':mutual,'base_area_final_px2':float(base.area),'solid_area_final_px2':float(finalsolid.area),'deepest_omitted_area_final_px2':float(clipped[-1].area),'positive_stroke_overlap_source_area':connections,'cream_vector_count':5,'orange_vector_count':4,'orange_groups_bytes_identical':True,'finalsolid_bounds':list(finalsolid.bounds),'output':{'file':'S7_WORDMARK.svg','sha256':sha(BASE/'S7_WORDMARK.svg'),'bytes':(BASE/'S7_WORDMARK.svg').stat().st_size,'paths':9,'transparent':True},'dependencies':{'vtracer':'0.6.15 unchanged','skia_pathops':'0.9.2 unchanged','native_vtracer_hash':'59e2053fca8666479e7163eec45d8b15143435c7a8d14f6dbd26eec9716bfe66'},'aesthetic_verdict':None,'limits':['Opacity is a fixed translation of observed JPEG luminance, not original alpha or print plate.','Five numeric envelope revisions are expert design inferences; nine stroke path strings remain exact S6.','Actual repeated donor field positions are deterministic adaptations, not original R word outlines.','No complete native poster, Figma or Drive output by worker.']}
(BASE/'PROVENANCE.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8');print(json.dumps(receipt))
