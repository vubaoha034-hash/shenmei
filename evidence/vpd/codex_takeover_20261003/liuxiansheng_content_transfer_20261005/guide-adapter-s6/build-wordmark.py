"""Single S6 expert envelopes + actual G4 weak-alpha contrast reinforcement."""
import pathlib,sys,json,hashlib,re,xml.etree.ElementTree as ET,argparse,datetime
from PIL import Image,ImageFilter
cli=argparse.ArgumentParser();cli.add_argument('--root',type=pathlib.Path);cli.add_argument('--output-dir',type=pathlib.Path);args=cli.parse_args()
BASE=args.output_dir.resolve() if args.output_dir else pathlib.Path(__file__).resolve().parent
ROOT=args.root.resolve() if args.root else next(p for p in BASE.parents if (p/'PROJECT_CONTROL_ADAPTER.json').exists())
B=ROOT/'evidence/vpd/codex_takeover_20261003/liuxiansheng_content_transfer_20261005'
OLD=BASE if (BASE/'CREAM_BRIDGED.raw').exists() else ROOT/'.liu-visual-private/s5_outline_implementation'
VDEP=ROOT/'.liu-visual-private/dependencies/vtracer_0_6_15_cp312/site-packages';PDEP=ROOT/'.liu-visual-private/dependencies/skia_pathops_0_9_2_abi3/site-packages'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(VDEP/'vtracer/vtracer.cp312-win_amd64.pyd')=='59e2053fca8666479e7163eec45d8b15143435c7a8d14f6dbd26eec9716bfe66'
sys.path[:0]=[str(VDEP),str(PDEP)]
import vtracer,pathops,importlib.metadata
assert importlib.metadata.version('vtracer')=='0.6.15' and pathops.__version__=='0.9.2'
from vector_adapter import parse_svg_path,union_all,svg_d,fill_path
PLAN=BASE/'EXPERT_S6_FROZEN_PATHS.json';METHOD=BASE/'EXPERT_S6_METHOD_PLAN.md'
if not PLAN.exists():PLAN=B/PLAN.name;METHOD=B/METHOD.name
frozen=json.loads(PLAN.read_text(encoding='utf8'));extract=json.loads((OLD/'SOURCE_EXTRACTION.json').read_text(encoding='utf8'))
G=ROOT/'.liu-visual-private/liuxiansheng_transfer_20261005/IMAGE_GUIDE_S4.png';assert sha(G)=='9ef09dd1814343a938445227ce9a8906f0eb1ae4531a857baaba0720606aa558'
w,h=1086,1448;n=w*h
support=bytearray((OLD/'CREAM_BRIDGED.raw').read_bytes());original=bytearray(n)
for hole in extract['source_internal_grain']['holes']:
 for x,y in hole['source_pixel_positions_xy']:support[y*w+x]=1;original[y*w+x]=1
safe=Image.frombytes('L',(w,h),bytes(255 if v else 0 for v in support)).filter(ImageFilter.MinFilter(7)).tobytes()
orange=Image.frombytes('L',(w,h),bytes(255 if v else 0 for v in (OLD/'ORANGE_SOURCE_CLEAN.raw').read_bytes())).filter(ImageFilter.MaxFilter(7)).tobytes()
alpha=Image.open(G).convert('RGBA').getchannel('A').tobytes();weak=bytearray(n)
for i in range(n):
 if safe[i] and not orange[i] and alpha[i]<245:weak[i]=1
seen=bytearray(n);selected=bytearray(n);components=[];all_count=0
for i in range(n):
 if not weak[i] or seen[i]:continue
 q=[i];seen[i]=1;cursor=0
 while cursor<len(q):
  p=q[cursor];cursor+=1;x,y=p%w,p//w
  for yy in range(max(0,y-1),min(h,y+2)):
   for xx in range(max(0,x-1),min(w,x+2)):
    j=yy*w+xx
    if weak[j] and not seen[j]:seen[j]=1;q.append(j)
 all_count+=1
 if 2<=len(q)<=40:
  for p in q:selected[p]=1
  components.append({'pixels':len(q),'positions_xy':[[p%w,p//w] for p in q]})
combined=bytes(255 if original[i] or selected[i] else 0 for i in range(n))
Image.frombytes('L',(w,h),combined).save(BASE/'ACTUAL_GRAIN_UNION_MASK.png')
Image.frombytes('L',(w,h),bytes(0 if v else 255 for v in combined)).save(BASE/'GRAIN_TRACE_INPUT.png')
params=dict(colormode='binary',mode='polygon',filter_speckle=0,path_precision=2)
vtracer.convert_image_to_svg_py(str(BASE/'GRAIN_TRACE_INPUT.png'),str(BASE/'ACTUAL_GRAIN_TRACE.svg'),**params)
grain=[]
for node in ET.parse(BASE/'ACTUAL_GRAIN_TRACE.svg').getroot().iter():
 if node.tag.rsplit('}',1)[-1]=='path':
  transform=node.attrib.get('transform','');match=re.search(r'translate\(([^,]+),([^\)]+)\)',transform)
  matrix=(1,0,0,1,float(match[1]),float(match[2])) if match else (1,0,0,1,0,0)
  grain.append(parse_svg_path(node.attrib['d'],matrix))
strokes={name:parse_svg_path(d) for name,d in frozen['paths'].items()};solid=union_all(strokes.values());grain_union=union_all(grain);clipped=pathops.op(solid,grain_union,pathops.PathOp.INTERSECTION);cream=pathops.op(solid,grain_union,pathops.PathOp.DIFFERENCE)
sx,sy=567/717,170/269;matrix=(sx,0,0,sy,29.46443514644352,128.91821561338293);cream_final=cream.transform(*matrix)
s5=(OLD/'S5_WORDMARK.svg').read_text(encoding='utf8');groups=re.findall(r'<g id="ORANGE_(?:BEHIND_GLYPHS|IN_FRONT_OF_GLYPHS)">[\s\S]*?</g>',s5);assert len(groups)==2
svg='<svg xmlns="http://www.w3.org/2000/svg" width="960" height="1280" viewBox="0 0 960 1280"><title>刘先生 S6 expert envelopes with actual-source contrast reinforced wear</title>'+groups[0]+'<g id="CREAM_WORDMARK">'+fill_path(svg_d(cream_final),'#fdf4e5','S6_EXPERT_ENVELOPES_ACTUAL_G_WEAR')+'</g>'+groups[1]+'</svg>\n'
ET.fromstring(svg);(BASE/'S6_WORDMARK.svg').write_text(svg,encoding='utf8',newline='\n')
# Raw analytic connection falsification: positive area overlaps required; no green joining stripes.
pairs=[('XIAN_UPPER_CLUSTER','XIAN_MIDDLE_BAR'),('XIAN_MIDDLE_BAR','XIAN_LEFT_LEG'),('XIAN_MIDDLE_BAR','XIAN_RIGHT_HOOK'),('SHENG_MAIN_STEM','SHENG_BASE_BAR')]
connections={a+'__'+b:float(pathops.op(strokes[a],strokes[b],pathops.PathOp.INTERSECTION).area) for a,b in pairs}
assert all(v>0 for v in connections.values()),connections
receipt={'schema':'s6-wordmark-provenance/v1','status':'IMPLEMENTED_PENDING_COLD_REVIEW','frozen_expert_paths_sha256':sha(PLAN),'method_sha256':sha(METHOD),'source_G4_sha256':sha(G),'S5_svg_sha256':sha(OLD/'S5_WORDMARK.svg'),'contour_method':frozen['contour_method'],'expert_envelopes':len(strokes),'old_cuts_or_micro_curves_used':False,'new_randomness':False,'source_alpha_contrast_design_transform':True,'pixel_exact_source_or_original_font':False,'safe_internal_pixels':sum(bool(safe[i]) and not orange[i] for i in range(n)),'alpha_lt245_all_components':all_count,'selected_weak_components':len(components),'selected_weak_pixels':sum(c['pixels'] for c in components),'original_grain_components':extract['source_internal_grain']['count'],'original_grain_pixels':sum(original),'union_mask_pixels':sum(bool(v) for v in combined),'traced_grain_paths':len(grain),'clipped_grain_source_area':float(clipped.area),'clipped_grain_contours':len(list(clipped.contours)),'stroke_positive_overlap_source_area':connections,'mapping':matrix,'final_cream_bounds':list(cream_final.bounds),'orange_groups_byte_identical_to_S5':True,'vtracer_params':params,'trace_calls':1,'upstream_unmodified':{'vtracer':'0.6.15','skia_pathops':'0.9.2'},'output':{'file':'S6_WORDMARK.svg','sha256':sha(BASE/'S6_WORDMARK.svg'),'bytes':(BASE/'S6_WORDMARK.svg').stat().st_size,'paths':5,'transparent':True},'aesthetic_verdict':None,'limits':['Entire cream envelopes are expert-authored G landmark adaptations; not exact G contours.','Weak partial-alpha G wear becomes binary transparency; not recovered originally transparent holes.','No actual native Figma import or complete poster export by worker.']}
(BASE/'PROVENANCE.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8')
(BASE/'WEAK_GRAIN_SOURCE_COMPONENTS.json').write_text(json.dumps({'source':str(G),'components':components},indent=2)+'\n',encoding='utf8')
print(json.dumps(receipt))
