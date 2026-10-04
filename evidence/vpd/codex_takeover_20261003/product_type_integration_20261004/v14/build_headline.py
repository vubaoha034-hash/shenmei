"""One V14 continuous phrase, cropped by the actual foreground product silhouette.

This is a preformal lettering asset. No Figma/Drive/state/Git operations occur.
--verify-only constructs and checks every output in memory; --emit-preview also
emits the actual complete raster. The original S photo remains immutable.
"""
from pathlib import Path
import argparse, base64, copy, hashlib, io, json, math, os, subprocess, sys
import xml.etree.ElementTree as ET
from PIL import Image, ImageChops, ImageFilter
import PIL

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[4]
PRIVATE_PREVIEW=ROOT/'.liu-visual-private/correct_source_typography/v14/preview.png'
RUNTIME=Path('C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies')
SITE='C:/Users/Administrator/AppData/Local/hermes/hermes-agent/venv/Lib/site-packages'
NS='http://www.w3.org/2000/svg'; ET.register_namespace('',NS)
COPY='一杯茶，慢下来'
FIXED={
 'source':('evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v12/headline.svg','fb8e4106184083a2a6e6eea88cbccc2f08ea8dc9c5a1d3bd50d7404c264ff89e'),
 'V13_source':('evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v13/headline.svg','454f50e59c5ff3e1b275bb27ac28a82a227741dc4e4004fe26e61720cac76b97'),
 'brand':('evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v13/brand.svg','dd8e9e899393dc36eb3f5b1652bdbb740787d41a108ea6aa1eae05cb1368b1ff'),
 'P':('.liu-visual-private/correct_source_typography/v13/packet/P.png','57c21466512a79cbb25c75db1d6a1748b595c3bc2d00c85ba51615557f74f925'),
 'R':('.liu-visual-private/correct_source_typography/v13/packet/R.jpg','87a28f5cd4b5d15b01e6536206127c357043a904b3c0dab3bfa0c50080782167'),
 'S':('.liu-visual-private/correct_source_typography/v13/packet/S.png','7fd7777fed21100cb6b47bc305701476054263565e73246ac469d065aa080618'),
 'T':('.liu-visual-private/correct_source_typography/v13/packet/T.png','b92d8ab1f3e9a9fa1c3befc6ed8a94f2fae5fda912253888afa3117d5c161ca9')}
FILES=('headline.svg','headline-part-1.svg','headline-part-2.svg','foreground-protection.svg','PROVENANCE.json')

# Manually traced conservative S silhouettes. They protect the complete cup,
# the fresh-leaf canopy, dry tea and tray. They are applied only to lettering.
CUP=('M324 593C324 570 417 550 537 550C638 550 751 571 751 594'
     'C749 650 708 771 620 818C596 831 530 832 492 818'
     'C440 811 408 779 385 736C359 691 339 640 324 605Z')
TEA_LEAF_TRAY=('M694 695C721 678 775 670 809 669'
 'C806 660 804 653 808 649C823 645 840 646 850 646'
 'C848 631 865 617 869 594C875 615 866 638 861 649'
 'C884 622 921 616 943 603C975 592 997 579 1006 574'
 'C1002 609 997 623 983 639C1007 618 1025 621 1040 635'
 'C1054 630 1072 630 1086 633C1107 628 1136 638 1155 646'
 'C1211 648 1282 667 1287 701C1295 767 1216 789 1118 792'
 'C959 808 795 789 716 753C699 739 688 716 694 695Z')
TARGETS={
 '杯':(422,445,151,139,0), '茶':(588,440,166,139,0),
 '，':(770,563,18,31,0), '慢':(802,483,160,148,0),
 '下':(982,508,110,127,0), '来':(1111,514,172,157,8)}

def digest(b):return hashlib.sha256(b).hexdigest()

def preflight(verify):
 paths={};refs={}
 for k,(relative,expected) in FIXED.items():
  p=ROOT/relative;raw=p.read_bytes();assert digest(raw)==expected,'FIXED_SOURCE_CHANGED:'+k
  paths[k]=p;refs[k]={'path':relative,'sha256':expected,'bytes':len(raw)}
 sys.path.append(SITE)
 import fontTools
 from fontTools.pens.boundsPen import BoundsPen
 from fontTools.pens.recordingPen import RecordingPen
 from fontTools.pens.transformPen import TransformPen
 from fontTools.svgLib.path import parse_path
 assert sys.version_info[:3]==(3,12,14) and PIL.__version__=='12.3.0' and fontTools.__version__=='4.63.0'
 node=RUNTIME/'node/bin/node.exe';sharp=RUNTIME/'node/node_modules/sharp'
 assert node.is_file() and sharp.is_dir()
 env={k:v for k,v in os.environ.items() if k.upper() not in {'NODE_OPTIONS','NODE_PATH'}}
 c='const s=require('+json.dumps(sharp.as_posix())+');process.stdout.write(JSON.stringify({node:process.version,sharp:s.versions.sharp,rsvg:s.versions.rsvg}));'
 versions=json.loads(subprocess.run([str(node),'-e',c],capture_output=True,text=True,check=True,env=env).stdout)
 assert versions=={'node':'v24.19.0','sharp':'0.35.4','rsvg':'2.62.91'}
 if not verify:assert all(not (OUT/f).exists() for f in FILES) and not PRIVATE_PREVIEW.exists(),'V14_OUTPUT_EXISTS_NO_OVERWRITE'
 return paths,refs,BoundsPen,RecordingPen,TransformPen,parse_path,node,sharp,env,{'python':sys.version,'Pillow':PIL.__version__,'fontTools':fontTools.__version__,**versions}

def raster(svg,node,sharp,env):
 c='const s=require('+json.dumps(sharp.as_posix())+');let a=[];process.stdin.on("data",b=>a.push(b));process.stdin.on("end",async()=>process.stdout.write(await s(Buffer.concat(a)).ensureAlpha().png().toBuffer()));'
 return subprocess.run([str(node),'-e',c],input=svg,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True,env=env).stdout

def xml(root):return (ET.tostring(root,encoding='unicode')+'\n').encode('utf-8')

def root_svg():return ET.Element('{'+NS+'}svg',{'width':'1536','height':'1024','viewBox':'0 0 1536 1024','fill':'none'})

def main():
 p=argparse.ArgumentParser();p.add_argument('--verify-only',action='store_true');p.add_argument('--emit-preview',action='store_true');args=p.parse_args()
 paths,refs,BoundsPen,RecordingPen,TransformPen,parse_path,node,sharp,env,deps=preflight(args.verify_only)
 source=ET.parse(paths['source']).getroot();sp=list(source.iter('{'+NS+'}path'))
 assert len(sp)==19 and source.find('{'+NS+'}title').text==COPY
 char_bounds={}
 for char in COPY:
  bs=[]
  for e in sp:
   if e.get('data-character')==char:
    b=BoundsPen(None);parse_path(e.get('d'),b);bs.append(b.bounds)
  char_bounds[char]=(min(b[0] for b in bs),min(b[1] for b in bs),max(b[2] for b in bs),max(b[3] for b in bs))
 result=root_svg();ET.SubElement(result,'{'+NS+'}title').text=COPY
 ET.SubElement(result,'{'+NS+'}desc').text='V14 preformal one continuous phrase. Real S cup, fresh-leaf and tea-tray silhouettes crop only the typography; the photo and brand remain intact.'
 defs=ET.SubElement(result,'{'+NS+'}defs');clip=ET.SubElement(defs,'{'+NS+'}clipPath',{'id':'S-product-negative-space','clipPathUnits':'userSpaceOnUse'})
 ET.SubElement(clip,'{'+NS+'}path',{'d':'M0 0H1536V1024H0Z'+CUP+TEA_LEAF_TRAY,'clip-rule':'evenodd'})
 group=ET.SubElement(result,'{'+NS+'}g',{'id':'V14-one-continuous-sentence','clip-path':'url(#S-product-negative-space)'})
 rows=[]
 for index,original in enumerate(sp,1):
  e=copy.deepcopy(original);char=e.get('data-character');b0=char_bounds[char]
  if char=='一':
   rec=RecordingPen();parse_path(e.get('d'),rec);parts=[];cmds={'moveTo':'M','lineTo':'L','curveTo':'C','closePath':'Z'}
   for command,pts in rec.value:
    new=[]
    for x,y in pts:
     xx=296+(x-345)*1.4;rx=max(329,min(745,xx));rim=595-43*math.sqrt(max(0,1-((rx-537)/211)**2))
     yy=rim-15+(y-(505.99-.224*(x-345)))*1.15
     new.extend((xx,yy))
    parts.append(cmds[command]+' '.join(format(v,'.12g') for v in new))
   e.set('d',''.join(parts));matrix=(1,0,0,1,0,0)
  else:
   x,y,w,h,degrees=TARGETS[char];sx=w/(b0[2]-b0[0]);sy=h/(b0[3]-b0[1]);a=math.radians(degrees);co,si=math.cos(a),math.sin(a)
   tx=x-sx*b0[0];ty=y-sy*b0[1];cx,cy=x+w/2,y+h/2
   matrix=(co*sx,si*sx,-si*sy,co*sy,co*(tx-cx)-si*(ty-cy)+cx,si*(tx-cx)+co*(ty-cy)+cy)
   e.set('transform','matrix('+' '.join(repr(v) for v in matrix)+')')
   assert e.get('d')==original.get('d'),'SOURCE_STROKE_REWRITTEN'
  e.set('id',f'V14-lettering-{index:02d}');group.append(e)
  bp=BoundsPen(None);parse_path(e.get('d'),TransformPen(bp,matrix))
  rows.append({'source_path_index':index,'character':char,'source_d_sha256':digest(original.get('d').encode()),'source_d_exact':e.get('d')==original.get('d'),'matrix':list(matrix),'unclipped_global_curve_bbox':list(bp.bounds)})
 full=xml(result);parts=[]
 for start,end in ((1,10),(11,19)):
  part=copy.deepcopy(result);g=part.find('{'+NS+'}g')
  for child in list(g):
   i=int(child.get('id').rsplit('-',1)[1])
   if not start<=i<=end:g.remove(child)
  parts.append(xml(part))
 assert max(map(len,parts))<45000,'TRANSPORT_PART_EXCEEDS_FIGMA_PAYLOAD_ALLOWANCE'
 protect=root_svg()
 ET.SubElement(protect,'{'+NS+'}path',{'id':'S-cup-protection','d':CUP,'fill':'#FFFFFF'})
 ET.SubElement(protect,'{'+NS+'}path',{'id':'S-leaf-tea-tray-protection','d':TEA_LEAF_TRAY,'fill':'#FFFFFF'})
 rgba=Image.open(io.BytesIO(raster(full,node,sharp,env))).convert('RGBA');alpha=rgba.getchannel('A');ab=alpha.getbbox()
 assert ab[0]>=288 and ab[1]>=400 and ab[2]<=1328 and ab[3]<=720,'OUTSIDE_ROOT_TECHNICAL_ALLOWANCE'
 expected=Image.new('RGBA',(1536,1024))
 for part in parts:expected.alpha_composite(Image.open(io.BytesIO(raster(part,node,sharp,env))).convert('RGBA'))
 assert ImageChops.difference(expected,rgba).getbbox(alpha_only=False) is None,'SPLIT_TRANSPORT_NOT_EQUIVALENT'
 unclipped=copy.deepcopy(result);unclipped.find('{'+NS+'}g').attrib.pop('clip-path')
 rawalpha=Image.open(io.BytesIO(raster(xml(unclipped),node,sharp,env))).convert('RGBA').getchannel('A')
 removed=ImageChops.subtract(rawalpha,alpha);removed_bbox=removed.getbbox();removed_count=sum(removed.histogram()[1:])
 mask=Image.open(io.BytesIO(raster(xml(protect),node,sharp,env))).convert('RGBA').getchannel('A')
 core=mask.filter(ImageFilter.MinFilter(7)).point(lambda v:255 if v==255 else 0)
 assert ImageChops.darker(alpha,core).getbbox() is None,'TEXT_COVERS_PROTECTED_PRODUCT_CORE'
 frozen=Image.open(paths['S']).convert('RGBA');base=Image.open(paths['T']).convert('RGBA');assert frozen.size==base.size==(1536,1024)
 preview=frozen.copy();preview.paste(base.crop((112,104,389,240)),(112,104));preview.alpha_composite(rgba)
 assert preview.crop((112,104,389,240)).tobytes()==base.crop((112,104,389,240)).tobytes(),'BRAND_PIXEL_BLOCK_CHANGED'
 diff=ImageChops.difference(preview.convert('RGB'),frozen.convert('RGB')).convert('L')
 assert ImageChops.darker(diff,core).getbbox() is None,'PRODUCT_CORE_PIXELS_NOT_IDENTICAL_TO_S'
 output=io.BytesIO();preview.convert('RGB').save(output,format='PNG');preview_png=output.getvalue()
 occlusion_rows=[]
 for name,box in [('cup_lip',(324,550,751,610)),('fresh_leaf',(808,574,1007,663)),('tea_and_tray_outer_edge',(1040,625,1316,710))]:
  crop=removed.crop(box);local=crop.getbbox()
  occlusion_rows.append({'connection':name,'inspection_region':list(box),'removed_text_pixels':sum(crop.histogram()[1:]),'removed_text_bbox_global':None if not local else [local[0]+box[0],local[1]+box[1],local[2]+box[0],local[3]+box[1]]})
 proof={'asset_sequence':'V14','formal_version_claimed':False,'exact_copy':COPY,'unique_structure':'One continuous descending sentence cropped by real S product foreground; no alternative artwork generated.',
  'fixed_source_and_references':refs,'input_view_image_actual':['P','R','S','T'],'reference_limits':{'P':'Typography only; photography excluded.','R':'Upper advertisement only.'},'dependencies':deps,
  'photography_source_unchanged_sha256':refs['S']['sha256'],'brand_source_unchanged_sha256':refs['brand']['sha256'],'brand_pixel_block_exact_to_V13':True,
  'viewport':[0,0,1536,1024],'import_position':[0,0],'import_dimensions':[1536,1024],'root_technical_allowance_not_user_coordinates':[288,400,1328,720],
  'actual_final_alpha_bbox_exclusive':list(ab),'foreground_mask_paths':{'cup':CUP,'leaf_tea_tray':TEA_LEAF_TRAY},'lettering_paths':19,'path_details':rows,
  'foreground_cropped_text_pixels':removed_count,'foreground_cropped_text_bbox':list(removed_bbox),'visible_product_connections':occlusion_rows,
  'protected_product_core_pixel_count':sum(core.histogram()[1:]),'protected_product_core_text_alpha_pixels':0,'protected_product_core_rgb_difference_pixels_vs_S':0,'protection_measurement':'S conservative manually traced foreground silhouettes, eroded 3px for exact opaque product-core comparison. This does not certify every uncertain photographic edge pixel.',
  'typography_construction':'Eighteen V12 literal path strings retained under exact affine transforms. 一 is adapted to the actual upper-left cup ellipse tangent. Character spacing is one sequence; comma bridges the phrase without the V13 block jump. All typography is ivory editable vector; real cup/leaf/tea/tray silhouettes remove foreground portions.',
  'Figma_transport':{'parts':[{'filename':f'headline-part-{i+1}.svg','bytes':len(b),'sha256':digest(b),'lettering_indices':[1,10] if i==0 else [11,19]} for i,b in enumerate(parts)],'literal_paths_and_clipDefs_exact_to_whole':True,'two_part_alpha_composite_matches_whole_pixel_exactly':True,'native_Figma_clipPath_support':'UNVERIFIED_BY_MAKER_ROOT_MUST_CHECK_ACTUAL_IMPORT','no_additional_coordinate_rounding_in_parts':True},
  'technical_method_provenance':{'implementation':'SVG userSpaceOnUse vector clipPath with evenodd negative product space; foreground crop applies only to typography. Original S is used directly as the lower raster layer.','root_supplied_primary_sources':['https://help.figma.com/hc/en-us/articles/360040450253-Masks','https://www.adobe.com/learn/premiere-pro/web/text-behind-subject-object-mask?ntd=1'],'worker_access_claim':'Root reported reading these primary pages; worker did not watch videos or invoke Premiere/AI ObjectMask.','limits':'Manual static contours; Figma clipPath import and exact frame export must be verified separately. Occlusion alone is not an aesthetic pass.'},
  'copy_inspection':'PENDING_ACTUAL_COMPLETE_PREVIEW_INSPECTION','aesthetic_pass_claimed':False,'imagegen_calls':0,'Figma_writes':0,'Drive_writes':0,'business_state_writes':0,'git_operations':0,
  'outputs':{'headline.svg':{'sha256':digest(full),'bytes':len(full)},'preview.png':{'path':PRIVATE_PREVIEW.relative_to(ROOT).as_posix(),'sha256':digest(preview_png),'dimensions':[1536,1024]},'foreground-protection.svg':{'sha256':digest(xml(protect))}},'script_sha256':digest(Path(__file__).read_bytes())}
 content={'headline.svg':full,'headline-part-1.svg':parts[0],'headline-part-2.svg':parts[1],'foreground-protection.svg':xml(protect),'PROVENANCE.json':(json.dumps(proof,ensure_ascii=False,indent=2)+'\n').encode()}
 if args.verify_only:
  for f in ('headline.svg','headline-part-1.svg','headline-part-2.svg','foreground-protection.svg'):
   if (OUT/f).exists():assert (OUT/f).read_bytes()==content[f],'SAVED_ASSET_NOT_EQUAL_TO_REPLAY:'+f
  if PRIVATE_PREVIEW.exists():assert PRIVATE_PREVIEW.read_bytes()==preview_png,'PRIVATE_PREVIEW_NOT_EQUAL_TO_REPLAY'
 else:
  assert all(not (OUT/f).exists() for f in FILES) and not PRIVATE_PREVIEW.exists()
  PRIVATE_PREVIEW.parent.mkdir(parents=True,exist_ok=True)
  for f,b in content.items():(OUT/f).write_bytes(b)
  PRIVATE_PREVIEW.write_bytes(preview_png)
 assert digest(paths['S'].read_bytes())==FIXED['S'][1]
 response={'mode':'zero_write' if args.verify_only else 'unique_preformal_asset_written','writes':0 if args.verify_only else len(content)+1,'alpha_bbox':ab,'svg_bytes':len(full),'parts_bytes':list(map(len,parts)),'occlusions':occlusion_rows,'product_core_rgb_diff_pixels':0,'svg_sha256':digest(full),'private_preview_path':str(PRIVATE_PREVIEW)}
 if args.emit_preview:
  buf=io.BytesIO();preview.convert('RGB').save(buf,format='JPEG',quality=83)
  response['image']={'mime':'image/jpeg','data':base64.b64encode(buf.getvalue()).decode()}
 print(json.dumps(response,ensure_ascii=False))

if __name__=='__main__':main()
