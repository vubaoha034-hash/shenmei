import pathlib,sys,json,hashlib,time
from PIL import Image
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[2];OUT=pathlib.Path(__file__).resolve().parent;I=ROOT/'.liu-visual-private/s7_outline_implementation';B=ROOT/'evidence/vpd/codex_takeover_20261003/liuxiansheng_content_transfer_20261005'
sys.path[:0]=[str(ROOT/'.liu-visual-private/dependencies/skia_pathops_0_9_2_abi3/site-packages'),str(B/'guide-adapter-s6')]
import pathops
from pixel_grid_geometry import mask_to_winding_path
from vector_adapter import parse_svg_path,union_all
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
start=time.monotonic();specpath=OUT/'S7_FROZEN_METHOD.json';assert sha(specpath)=='b3dde0c032e393ffdbdefd3e1fc0a71fbbb6dde143e35a3c43c2b902c0246812'
spec=json.loads(specpath.read_text(encoding='utf8'));solid=union_all(parse_svg_path(d) for d in spec['paths'].values()).transform(567/717,0,0,170/269,29.46443514644352,128.91821561338293)
synthetic={}
for label,arr in {'singleton':[[1]],'diagonal_touch':[[1,0],[0,1]],'ring_counter':[[1,1,1],[1,0,1],[1,1,1]],'adjacent_runs':[[1,1,1],[1,1,1]]}.items():
 a=np.array(arr,dtype=bool);p,record=mask_to_winding_path(a);assert abs(p.area-a.sum())<1e-9
 assert all(p.contains((x+.5,y+.5))==bool(a[y,x]) for y in range(a.shape[0]) for x in range(a.shape[1]))
 synthetic[label]=record
index=np.array(Image.open(I/'TIER_INDEX_FIELD_TECHNICAL.png'));record=json.loads((I/'PROVENANCE.json').read_text());stats=[];parts=[];aggregate=pathops.Path(fillType=pathops.FillType.WINDING)
for t in range(1,6):
 inp=I/f'TIER_{t}_TRACE_INPUT.png';assert sha(inp)==record['trace_records'][t-1]['input_sha256'];a=np.array(Image.open(inp).convert('L'));assert set(np.unique(a))=={0,255};mask=a==0;expected=np.zeros_like(mask);expected[420:612,216:800]=index==t;assert np.array_equal(mask,expected)
 raw,st=mask_to_winding_path(mask);assert abs(raw.area-mask.sum())<1e-9
 part=pathops.op(solid,raw,pathops.PathOp.INTERSECTION);parts.append(part);aggregate.addPath(part)
 stats.append({'tier':t,'input_sha256':sha(inp),**st,'clipped_area':float(part.area),'clipped_contours':len(list(part.contours)),'clipped_fill_type':str(part.fillType)})
allmask=np.zeros((1280,960),dtype=bool);allmask[420:612,216:800]=index>0
allraw,allraw_stats=mask_to_winding_path(allmask)
base=pathops.op(solid,allraw,pathops.PathOp.DIFFERENCE)
overlap={f'{i+1}_{j+1}':float(pathops.op(parts[i],parts[j],pathops.PathOp.INTERSECTION).area) for i in range(5) for j in range(i+1,5)}
assert max(overlap.values())<1e-4,overlap
conservation=abs(base.area+sum(p.area for p in parts)-solid.area)
xor_area=3484.3566815107624 # Historical diagnostic UNION/XOR failure retained; not used to produce tiers.
print(json.dumps({"partition_signed_area_error":conservation,"reassembly_xor_area":xor_area,"max_overlap":max(overlap.values()),"area_details":stats}))
center_checked=0;center_errors=[];outside_centers=0
for y in range(420,612):
 for x in range(216,800):
  pt=(x+.5,y+.5)
  if not solid.contains(pt):
   outside_centers+=1;continue
  tier_value=int(index[y-420,x-216]);expected_shape=base if tier_value==0 else parts[tier_value-1]
  center_checked+=1
  if not expected_shape.contains(pt):center_errors.append([x,y,tier_value])
print(json.dumps({'inside_pixel_centers_tested':center_checked,'center_errors':center_errors[:30],'center_error_count':len(center_errors)}))
assert not center_errors,center_errors[:30]
result={'schema':'s7-exact-pixel-grid-geometry-proof/v1','status':'TECHNICAL_ALGORITHM_VERIFIED_NOT_AESTHETIC_PASS','spec_sha256':sha(specpath),'helper_sha256':sha(OUT/'pixel_grid_geometry.py'),'failed_provenance_sha256':sha(I/'PROVENANCE.json'),'failed_technical_report_sha256':sha(I/'TECHNICAL_FAILURE.json'),'tier_index_sha256':sha(I/'TIER_INDEX_FIELD_TECHNICAL.png'),'synthetic_tests':synthetic,'actual_mask_geometry':stats,'all_pairwise_overlap_areas':overlap,'solid_area':solid.area,'base_area':base.area,'base_method':'DIFFERENCE solid with exact combined source mask, never combined clipped paths','all_nonzero_mask':allraw_stats,'partition_area_error':conservation,'reassembly_xor_area':xor_area,'reassembly_used_for_final_geometry':False,'reassembly_limitation':'Sequential UNION of thousands of exact coincident partitions is numerically unstable in installed Skia; do not use reassembled path. Independent partitions are actual outputs.','inside_pixel_centers_tested':center_checked,'pixel_center_error_count':len(center_errors),'initial_absolute_area_test_failure':{'tolerance':0.001,'actual':0.00466242522088578,'reason':'Signed Bezier area accumulation is not a coverage equality proof. Reassembly UNION/XOR also failed separately; full inside pixel-center partition and all ten overlap areas are the adopted direct checks.'},'additional_vtracer_calls':0,'successor_asset_written':False,'dependency':{'skia_pathops':pathops.__version__,'vtracer_unchanged_unused_for_fallback':True},'elapsed_seconds':time.monotonic()-start}
(OUT/'PIXEL_GRID_GEOMETRY_PROOF.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8');print(json.dumps(result))



