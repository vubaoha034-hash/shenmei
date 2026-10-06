"""Frozen S7 exact-grid technical fallback, zero new VTracer calls."""
import pathlib,sys,json,hashlib,re,xml.etree.ElementTree as ET,argparse
from PIL import Image
import numpy as np
cli=argparse.ArgumentParser();cli.add_argument('--root',type=pathlib.Path);cli.add_argument('--output-dir',type=pathlib.Path);a=cli.parse_args()
BASE=a.output_dir.resolve() if a.output_dir else pathlib.Path(__file__).resolve().parent
ROOT=a.root.resolve() if a.root else next(p for p in BASE.parents if (p/'PROJECT_CONTROL_ADAPTER.json').exists())
sys.path[:0]=[str(ROOT/'.liu-visual-private/dependencies/skia_pathops_0_9_2_abi3/site-packages')]
import pathops
import vector_adapter as va
from pixel_grid_geometry import mask_to_winding_path
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(BASE/'S7_FROZEN_METHOD.json')=='b3dde0c032e393ffdbdefd3e1fc0a71fbbb6dde143e35a3c43c2b902c0246812'
assert sha(BASE/'S7_PIXEL_GRID_TECHNICAL_ADDENDUM.json')=='164c770083237914ef9676d961751823b6c87af090746e6cae9bf50e82e707ce'
assert sha(BASE/'pixel_grid_geometry.py')=='c8e5c2335b8390c2f9c06b80b2f9e104fbf9fed04c00f0da769ae52fe94fdf4c'
spec=json.loads((BASE/'S7_FROZEN_METHOD.json').read_text(encoding='utf8'));add=json.loads((BASE/'S7_PIXEL_GRID_TECHNICAL_ADDENDUM.json').read_text(encoding='utf8'))
assert sha(BASE/'TIER_INDEX_FIELD_TECHNICAL.png')==add['input']['sha256']
index=np.array(Image.open(BASE/'TIER_INDEX_FIELD_TECHNICAL.png'));solid=va.union_all(va.parse_svg_path(d) for d in spec['paths'].values()).transform(567/717,0,0,170/269,29.46443514644352,128.91821561338293)
parts=[];stats=[]
for t in range(1,6):
 p=BASE/f'TIER_{t}_TRACE_INPUT.png';assert sha(p)==add['input']['mask_sources'][t-1]['input_sha256']
 arr=np.array(Image.open(p).convert('L'));assert set(np.unique(arr))=={0,255};mask=arr==0
 expected=np.zeros_like(mask);expected[420:612,216:800]=index==t;assert np.array_equal(mask,expected)
 raw,st=mask_to_winding_path(mask);assert abs(raw.area-mask.sum())<1e-9
 part=pathops.op(solid,raw,pathops.PathOp.INTERSECTION);parts.append(part);stats.append({'tier':t,**st,'clipped_area':float(part.area),'clipped_contours':len(list(part.contours))})
allmask=np.zeros((1280,960),dtype=bool);allmask[420:612,216:800]=index>0;rawall,rawstats=mask_to_winding_path(allmask);base=pathops.op(solid,rawall,pathops.PathOp.DIFFERENCE)
overlap={f'{i+1}_{j+1}':float(pathops.op(parts[i],parts[j],pathops.PathOp.INTERSECTION).area) for i in range(5) for j in range(i+1,5)};error=abs(base.area+sum(p.area for p in parts)-solid.area)
assert max(overlap.values())<.0001 and error<.001,(overlap,error)
# Only serialization changes: six decimals preserve thin compound-partition boundaries.
def six(v):
 s=f'{float(v):.6f}'.rstrip('0').rstrip('.');return '0' if s in ['-0',''] else s
va.n=six
cream=''.join(f'<path id="S7_CREAM_TIER_{i}" fill="#fdf4e5" fill-opacity="{opacity}" fill-rule="nonzero" d="{va.svg_d(p)}"/>' for i,(p,opacity) in enumerate(zip([base,*parts[:4]],[1,.92,.8,.6,.35])))
groups=re.findall(r'<g id="ORANGE_(?:BEHIND_GLYPHS|IN_FRONT_OF_GLYPHS)">[\s\S]*?</g>',(BASE/'S6_WORDMARK.svg').read_text(encoding='utf8'));assert len(groups)==2
svg='<svg xmlns="http://www.w3.org/2000/svg" width="960" height="1280" viewBox="0 0 960 1280"><title>刘先生 S7 frozen facets and exact-grid reference opacity wear</title>'+groups[0]+'<g id="CREAM_WORDMARK">'+cream+'</g>'+groups[1]+'</svg>\n';ET.fromstring(svg)
(BASE/'S7_WORDMARK.svg').write_text(svg,encoding='utf8',newline='\n')
(BASE/'S7_SOLID_TECHNICAL.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="960" height="1280"><path fill="#fdf4e5" d="'+va.svg_d(solid)+'"/></svg>',encoding='utf8')
rec={'schema':'s7-exact-grid-provenance/v1','status':'IMPLEMENTED_PENDING_ACTUAL_RENDER_CHECK_AND_COLD_REVIEW','spec_sha256':sha(BASE/'S7_FROZEN_METHOD.json'),'addendum_sha256':sha(BASE/'S7_PIXEL_GRID_TECHNICAL_ADDENDUM.json'),'helper_sha256':sha(BASE/'pixel_grid_geometry.py'),'tier_field_sha256':sha(BASE/'TIER_INDEX_FIELD_TECHNICAL.png'),'reference_sha256':spec['texture']['reference_sha256'],'donor_sha256':sha(BASE/'REFERENCE_DONOR_TILES.json'),'unchanged_visual_parameters':True,'nine_S6_stroke_strings_unchanged':True,'orange_groups_byte_equal_S6':True,'upstream_skia_pathops':pathops.__version__,'upstream_modified':False,'new_VTracer_calls':0,'historical_failed_VTracer_calls':5,'exact_grid_tier_stats':stats,'raw_all_stats':rawstats,'base_method':'solid DIFFERENCE exact raw_all, no clipped aggregate/reassembly','base_area':float(base.area),'solid_area':float(solid.area),'partition_area_error':error,'ten_pair_overlap_areas':overlap,'svg_coordinate_precision':6,'output':{'file':'S7_WORDMARK.svg','sha256':sha(BASE/'S7_WORDMARK.svg'),'bytes':(BASE/'S7_WORDMARK.svg').stat().st_size,'cream_paths':5,'orange_paths':4},'source_alpha':'UNKNOWN; opacity is fixed design translation of reference JPEG luminance','aesthetic_verdict':None,'failed_production_source':'technical-failures/polygon-refuted/','limits':['Original R donor tiles repeated1:1 deterministically; not recovered print-plate alpha.','Exact-grid fallback uses immutable prior five binary tier masks. VTracer failed output is preserved but excluded from final production.','Native Figma export and independent cold review remain Root-owned.']}
(BASE/'PROVENANCE.json').write_text(json.dumps(rec,indent=2)+'\n',encoding='utf8');print(json.dumps(rec))
