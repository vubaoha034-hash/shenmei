"""S4 single source-guided wordmark implementation.

Upstream VTracer 0.6.15 and skia-pathops 0.9.2 are unchanged.
The adapter extracts G contours, restores only frozen orange-occluded windows,
applies explicit expert-local geometry edits, and expands reconstructed orange paths.
This is not an original font and not an exact all-pixel tracing claim.
"""
import sys, pathlib, json, re, hashlib, datetime, argparse, xml.etree.ElementTree as ET
CLI=argparse.ArgumentParser(description=__doc__)
CLI.add_argument('--root',type=pathlib.Path)
CLI.add_argument('--output-dir',type=pathlib.Path)
CLI.add_argument('--reuse-traces',action='store_true')
ARGS=CLI.parse_args()
SOURCE_BASE=pathlib.Path(__file__).resolve().parent
def find_repository(start):
    for folder in [start,*start.parents]:
        if (folder/'PROJECT_CONTROL_ADAPTER.json').is_file():return folder
    raise RuntimeError('No PROJECT_CONTROL_ADAPTER.json ancestor; pass --root explicitly')
ROOT=ARGS.root.resolve() if ARGS.root else find_repository(SOURCE_BASE)
if not (ROOT/'PROJECT_CONTROL_ADAPTER.json').is_file():raise RuntimeError('Explicit --root lacks PROJECT_CONTROL_ADAPTER.json')
BASE=ARGS.output_dir.resolve() if ARGS.output_dir else SOURCE_BASE
VDEP=ROOT/'.liu-visual-private/dependencies/vtracer_0_6_15_cp312/site-packages'
PDEP=ROOT/'.liu-visual-private/dependencies/skia_pathops_0_9_2_abi3/site-packages'
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
if sha(VDEP/'vtracer/vtracer.cp312-win_amd64.pyd')!='59e2053fca8666479e7163eec45d8b15143435c7a8d14f6dbd26eec9716bfe66':
    raise RuntimeError('Fixed VTracer native extension byte identity failed')
sys.path[:0]=[str(VDEP),str(PDEP)]
import vtracer, pathops, importlib.metadata
if importlib.metadata.version('vtracer')!='0.6.15' or pathops.__version__!='0.9.2':
    raise RuntimeError('Unexpected upstream version')
SPEC=json.loads((BASE/'FROZEN_SPEC.json').read_text(encoding='utf-8'))
INPUT=json.loads((BASE/'SOURCE_EXTRACTION.json').read_text(encoding='utf-8'))
if INPUT['source']['sha256']!=SPEC['source_sha256'] or INPUT['reference']['sha256']!=SPEC['reference_sha256']:
    raise RuntimeError('Source/reference mismatch')
# Identical S3 spline controls, except speckle=0 intentionally retains actual G holes.
PARAMS=dict(colormode='binary',mode='spline',filter_speckle=0,corner_threshold=60,length_threshold=4.0,max_iterations=10,splice_threshold=45,path_precision=2)
TRACE_RUNS=[]
TRACE_CACHE=json.loads((BASE/'TRACE_GENERATION.json').read_text(encoding='utf-8')) if ARGS.reuse_traces else None
for label, infile, outfile in [
    ('G_CREAM_VISIBLE_SOURCE','CREAM_SOURCE_TRACE_INPUT.png','G_CREAM_SOURCE_TRACE.svg'),
    ('INFERRED_LOCAL_BRIDGES','BRIDGE_ADDITIONS_TRACE_INPUT.png','LOCAL_BRIDGE_TRACE.svg'),
]:
    if ARGS.reuse_traces:
        old=next((r for r in TRACE_CACHE['rows'] if r['label']==label),None)
        if not old or old['params']!=PARAMS or old['input_sha256']!=sha(BASE/infile) or old['output_sha256']!=sha(BASE/outfile):
            raise RuntimeError('Trace reuse rejected by exact input/output/parameter binding')
    else:vtracer.convert_image_to_svg_py(str(BASE/infile),str(BASE/outfile),**PARAMS)
    TRACE_RUNS.append({'label':label,'input':infile,'input_sha256':sha(BASE/infile),'output':outfile,'output_sha256':sha(BASE/outfile),'params':PARAMS.copy(),'reused_verified_trace':ARGS.reuse_traces,'generation_origin':old.get('generation_origin') if ARGS.reuse_traces else 'CURRENT_BUILDER_RUN'})
TOKEN=re.compile(r'[A-Za-z]|[-+]?(?:\d*\.\d+|\d+\.?\d*)(?:[eE][-+]?\d+)?')
def parse_svg_path(d, matrix=(1,0,0,1,0,0)):
    """Minimal deterministic SVG pen adapter. Supported commands are explicit."""
    tokens=TOKEN.findall(d)
    # Do not silently skip unsupported characters.
    if re.sub(r'[\s,]','',TOKEN.sub('',d)):
        raise RuntimeError('Unsupported path data syntax')
    p=pathops.Path();i=0;cmd=None;current=(0.,0.);start=(0.,0.);last_cubic=None;last_quad=None
    a,b,c,dd,e,f=matrix
    def point(pt): return (a*pt[0]+c*pt[1]+e,b*pt[0]+dd*pt[1]+f)
    def numbers(n):
        nonlocal i
        if i+n>len(tokens) or any(len(t)==1 and t.isalpha() for t in tokens[i:i+n]): raise RuntimeError('Incomplete SVG path data')
        value=list(map(float,tokens[i:i+n]));i+=n;return value
    def xy(n,relative):
        values=numbers(n*2);pts=[]
        for j in range(n): pts.append((values[2*j]+(current[0] if relative else 0),values[2*j+1]+(current[1] if relative else 0)))
        return pts
    while i<len(tokens):
        if len(tokens[i])==1 and tokens[i].isalpha():
            cmd=tokens[i];i+=1
        if cmd is None: raise RuntimeError('Path has no current command')
        upper=cmd.upper();relative=cmd.islower()
        if upper=='Z':
            p.close();current=start;last_cubic=last_quad=None;cmd=None;continue
        if upper=='M':
            q=xy(1,relative)[0];p.moveTo(*point(q));current=start=q;cmd='l' if relative else 'L';last_cubic=last_quad=None
        elif upper=='L':
            q=xy(1,relative)[0];p.lineTo(*point(q));current=q;last_cubic=last_quad=None
        elif upper=='H':
            x=numbers(1)[0]+(current[0] if relative else 0);current=(x,current[1]);p.lineTo(*point(current));last_cubic=last_quad=None
        elif upper=='V':
            y=numbers(1)[0]+(current[1] if relative else 0);current=(current[0],y);p.lineTo(*point(current));last_cubic=last_quad=None
        elif upper=='C':
            q=xy(3,relative);p.cubicTo(*(v for pt in q for v in point(pt)));current=q[2];last_cubic=q[1];last_quad=None
        elif upper=='S':
            q=xy(2,relative);q0=(2*current[0]-last_cubic[0],2*current[1]-last_cubic[1]) if last_cubic is not None else current
            p.cubicTo(*(v for pt in [q0,*q] for v in point(pt)));current=q[1];last_cubic=q[0];last_quad=None
        elif upper=='Q':
            q=xy(2,relative);p.quadTo(*(v for pt in q for v in point(pt)));current=q[1];last_quad=q[0];last_cubic=None
        elif upper=='T':
            q=xy(1,relative)[0];q0=(2*current[0]-last_quad[0],2*current[1]-last_quad[1]) if last_quad is not None else current
            p.quadTo(*(v for pt in [q0,q] for v in point(pt)));current=q;last_quad=q0;last_cubic=None
        else: raise RuntimeError('Unsupported SVG command: '+cmd)
    return p
def source_matrix(value):
    if not value:return (1,0,0,1,0,0)
    match=re.fullmatch(r'\s*translate\(([^()]*)\)\s*',value)
    if match:
        v=[float(x) for x in re.split(r'[\s,]+',match.group(1).strip())]
        if len(v)==1:v.append(0.)
        if len(v)!=2:raise RuntimeError('Invalid translate')
        return (1,0,0,1,*v)
    match=re.fullmatch(r'\s*matrix\(([^()]*)\)\s*',value)
    if match:
        v=tuple(float(x) for x in re.split(r'[\s,]+',match.group(1).strip()))
        if len(v)==6:return v
    raise RuntimeError('Unsupported VTracer transform: '+value)
def read_paths(name):
    root=ET.parse(BASE/name).getroot();paths=[]
    for node in root.iter():
        if node.tag.rsplit('}',1)[-1]=='path':
            paths.append(parse_svg_path(node.attrib['d'],source_matrix(node.attrib.get('transform'))))
    if not paths:raise RuntimeError('Trace has no contour paths: '+name)
    return paths
def union_all(paths):
    out=pathops.Path()
    for p in paths:out=pathops.op(out,p,pathops.PathOp.UNION)
    return out
def poly(points):
    p=pathops.Path();p.moveTo(*points[0])
    for q in points[1:]:p.lineTo(*q)
    p.close();return p
def rectangle(box):
    x0,y0,x1,y1=box;return poly([(x0,y0),(x1,y0),(x1,y1),(x0,y1)])
def facts(p):
    return {'bounds_source':[float(v) for v in p.bounds],'area_source':float(p.area),'contours':len(list(p.contours))}
source_paths=read_paths('G_CREAM_SOURCE_TRACE.svg')
source=union_all(source_paths)
bridge=union_all(read_paths('LOCAL_BRIDGE_TRACE.svg'))
cream=pathops.op(source,bridge,pathops.PathOp.UNION)
EDIT_EVENTS=[{'id':'LOCAL_OCCLUDED_CREAM_RECOVERY','classification':'EXPERT_INFERRED_NOT_ORIGINAL_PIXELS','before':facts(source),'added_bridge':facts(bridge),'after':facts(cream),'mask_evidence':'SOURCE_EXTRACTION.json'}]
for edit in SPEC['source_coordinate_intersections']:
    window=rectangle(edit['window'])
    inside=pathops.op(cream,window,pathops.PathOp.INTERSECTION)
    retained=pathops.op(inside,poly(edit['polygon']),pathops.PathOp.INTERSECTION)
    before=facts(cream)
    cream=pathops.op(pathops.op(cream,window,pathops.PathOp.DIFFERENCE),retained,pathops.PathOp.UNION)
    EDIT_EVENTS.append({'id':edit['id'],'classification':'EXPERT_LOCAL_WINDOW_INTERSECTION','window':edit['window'],'polygon':edit['polygon'],'before':before,'after':facts(cream),'local_reduction_source_area':float(inside.area-retained.area),'local_backoff':None})
for edit in SPEC['source_coordinate_cuts']:
    before=facts(cream)
    cream=pathops.op(cream,poly(edit['polygon']),pathops.PathOp.DIFFERENCE)
    EDIT_EVENTS.append({'id':edit['id'],'classification':'EXPERT_LOCAL_CUT','polygon':edit['polygon'],'before':before,'after':facts(cream),'local_reduction_source_area':before['area_source']-float(cream.area),'local_backoff':None})
replacement=SPEC['replacement']
# This window isolates the measured short-knife component; the long knife begins
# outside its x range at these y values. No other Liu stem is replaced.
window=rectangle(replacement['source_component_bbox'])
old_short=pathops.op(cream,window,pathops.PathOp.INTERSECTION)
before=facts(cream)
cream=pathops.op(pathops.op(cream,window,pathops.PathOp.DIFFERENCE),poly(replacement['polygon']),pathops.PathOp.UNION)
EDIT_EVENTS.append({'id':replacement['id'],'classification':'EXPERT_ONE_COMPONENT_RECONSTRUCTION','original_component_window':replacement['source_component_bbox'],'removed':facts(old_short),'new_polygon':replacement['polygon'],'before':before,'after':facts(cream),'local_backoff':None})
mapping=SPEC['source_to_final'];matrix=(mapping['sx'],0,0,mapping['sy'],mapping['tx'],mapping['ty'])
cream_final=cream.transform(*matrix)
source_final=source.transform(*matrix)
bridge_final=bridge.transform(*matrix)
def n(value):
    val=round(float(value),2)
    if val==0:return '0'
    return format(val,'.2f').rstrip('0').rstrip('.')
def svg_d(p):
    out=[]
    for command, points in p.segments:
        if command=='moveTo':out.append('M'+' '.join(n(v) for q in points for v in q))
        elif command=='lineTo':out.append('L'+' '.join(n(v) for q in points for v in q))
        elif command=='curveTo':
            if len(points)!=3:raise RuntimeError('Unexpected cubic sequence')
            out.append('C'+' '.join(n(v) for q in points for v in q))
        elif command=='qCurveTo':
            if len(points)<2 or points[-1] is None:raise RuntimeError('Unsupported all-off-curve quadratic sequence')
            for segment in pathops.decompose_quadratic_segment(tuple(points)):
                out.append('Q'+' '.join(n(v) for q in segment for v in q))
        elif command=='closePath':out.append('Z')
        elif command=='endPath':pass
        else:raise RuntimeError('Unsupported pathops segment: '+command)
    return ''.join(out)
def fill_path(d,color,identity):
    return '<path id="'+identity+'" fill="'+color+'" fill-rule="nonzero" d="'+d+'"/>'
orange_shapes=[]
for orange in SPEC['orange_final_paths']:
    p=parse_svg_path(orange['d'])
    p.stroke(SPEC['orange_width_final_px'],pathops.LineCap.ROUND_CAP,pathops.LineJoin.ROUND_JOIN,4.0)
    p.convertConicsToQuads(0.01)
    orange_shapes.append({**orange,'contour':p,'svg':fill_path(svg_d(p),SPEC['orange'],orange['id']),'bounds_final':[float(v) for v in p.bounds]})
back=''.join(o['svg'] for o in orange_shapes if o['position']=='BEHIND_CREAM')
front=''.join(o['svg'] for o in orange_shapes if o['position']=='IN_FRONT_OF_CREAM')
cream_svg=fill_path(svg_d(cream_final),SPEC['cream'],'S4_G_CREAM_WITH_EXPERT_LOCAL_REVISIONS')
svg='<svg xmlns="http://www.w3.org/2000/svg" width="960" height="1280" viewBox="0 0 960 1280"><title>刘先生 S4 source-guided locally revised wordmark</title><g id="ORANGE_BEHIND_GLYPHS">'+back+'</g><g id="CREAM_WORDMARK">'+cream_svg+'</g><g id="ORANGE_IN_FRONT_OF_GLYPHS">'+front+'</g></svg>\n'
for prohibited in ['<image','data:','foreignObject']:
    if prohibited in svg:raise RuntimeError('Forbidden SVG payload: '+prohibited)
ET.fromstring(svg)
out=BASE/'S4_WORDMARK.svg';out.write_text(svg,encoding='utf-8',newline='\n')
# Orange-hidden diagnostics are rendered in memory from this same SVG in render-preview.cjs.
dependency_records=[]
for label,dep,dist in [('VTracer',VDEP,'vtracer-0.6.15.dist-info'),('skia-pathops',PDEP,'skia_pathops-0.9.2.dist-info')]:
    info=dep/dist
    licenses=[p for p in info.rglob('*') if p.is_file() and p.name in ['LICENSE','LICENSE.txt','LICENSE.md']]
    for lic in licenses:
        dest=BASE/('LICENSE-'+label+'-'+lic.name+'.txt')
        dest.write_bytes(lic.read_bytes())
    dependency_records.append({'tool':label,'version':'0.6.15' if label=='VTracer' else '0.9.2','license':'MIT' if label=='VTracer' else 'BSD-3-Clause','unmodified':True,'site_packages':str(dep),'module':vtracer.__file__ if label=='VTracer' else pathops.__file__,'metadata_sha256':sha(info/'METADATA'),'licenses':[{'path':str(p),'sha256':sha(p)} for p in licenses]})
receipt={
 'schema':'s4-wordmark-provenance/v1','status':'IMPLEMENTED_PENDING_INDEPENDENT_PIXEL_REVIEW',
 'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'source':INPUT['source'],'reference':INPUT['reference'],'copy_manifest':INPUT['copy_manifest'],'frozen_spec':{'path':'FROZEN_SPEC.json','sha256':sha(BASE/'FROZEN_SPEC.json')},
 'upstream':dependency_records,
 'source_extraction':{'path':'SOURCE_EXTRACTION.json','sha256':sha(BASE/'SOURCE_EXTRACTION.json')},
 'cream_source_trace':{'classification':'VISIBLE_G_CREAM_CONTOURS_WITH_ACTUAL_INTERNAL_HOLE_POSITIONS','original_clean_components':len(INPUT['cream']['retained_components']),'source_paths':len(source_paths),'source':facts(source),'visible_source_only':True},
 'bridge_recovery':{'classification':'INFERRED_HIDDEN_CREAM','source_mask_added_pixels':INPUT['bridge']['added_pixels'],'frozen_windows':INPUT['bridge']['operations'],'source':facts(bridge),'measured_mixed_edge_correction':INPUT['bridge'].get('measured_mixed_edge_correction'),'existing_source_cream_trace_overlap':INPUT['bridge'].get('original_cream_trace_overlap'),'sheng_base_local_revision':INPUT['bridge'].get('sheng_base_local_revision'),'scope':'Seven local windows/radius8, with only base left edge 770 to 758 revised. Only Q permits direct actual pure-orange/high-alpha orange-white recovery without closing; all 61 original enclosed holes excluded. 2px trace support uses existing cream only.'},
 'local_geometry_revisions':{'classification':'EXPERT_AUTHORED_REVISIONS_NOT_ORIGINAL_PIXELS','events':EDIT_EVENTS,'baseline_source_trace_retained_outside_local_ops':True},
 'grain':{'source':'Actual enclosed noncream pixels of G opaque cream-class mask','count_before_revisions':INPUT['source_internal_grain']['count'],'pixels_before_revisions':INPUT['source_internal_grain']['pixels'],'actual_positions':'SOURCE_EXTRACTION.json/source_internal_grain/holes','random_noise':False,'whole_edge_jitter':False,'preserved_via_filter_speckle_zero':True,'binary_alpha_limit':'Original partial-alpha grain is flattened to binary contour holes. Local expert cuts may remove grain portions inside their exact cut areas.'},
 'orange_reconstruction':{'classification':'EXPERT_RECONSTRUCTED_CENTERLINES_NOT_EXACT_SOURCE_PIXEL_TRACE','color':SPEC['orange'],'stroke_width_final_px':SPEC['orange_width_final_px'],'cap':'round','join':'round','expanded_to_fill':True,'conic_to_quad_tolerance_final_px':0.01,'paths':[{k:v for k,v in o.items() if k not in ['contour','svg']} for o in orange_shapes],'layer_split':'Four early cubic segments plus left arc behind cream; later six cubic segments plus right tail in front.'},
 'parameters':PARAMS,'parameter_source':'S3 thin implementation spline settings, explicitly filter_speckle=0 for G actual grain; package unmodified.',
 'trace_runs':TRACE_RUNS,
 'trace_generation_calls_this_builder_run':0 if ARGS.reuse_traces else 2,
 'prior_failed_builder_trace_calls_retained':2 if ARGS.reuse_traces else None,
 'total_trace_generation_calls_in_this_asset_chain':TRACE_CACHE.get('generation_calls_completed') if ARGS.reuse_traces else 2,
 'coordinate_mapping':{'source_bbox':SPEC['source_bbox'],'target_bbox_reference':SPEC['target_bbox'],'matrix':matrix,'nonuniform':True,'post_edit_recenter':False},
 'output':{'path':str(out),'sha256':sha(out),'bytes':out.stat().st_size,'preferred_under_35k':out.stat().st_size<35000,'canvas':[960,1280],'transparent':True,'path_count':5,'bitmap_embeds':0,'pathops_bounds_are_not_raster_alpha_bounds':True,'cream_final_pathops_bounds':[float(v) for v in cream_final.bounds]},
 'diagnostics':{'same_candidate_orange_hidden':'S4_ORANGE_HIDDEN_TECHNICAL_PREVIEW.png','no_alternate_candidate':True},
 'implementation_source':{'prepare':'prepare-inputs.cjs','builder':'build-wordmark.py'},
 'aesthetic_verdict':None,'independent_review':None,
 'limitations':[
  'G foreground opacity, shades and subpixel fringe are flattened by the documented binary class extraction.',
  'This combines real G cream geometry with explicit expert revisions, inferred bridges and reconstructed orange centerlines; it is not a complete exact-pixel tracing.',
  'VTracer spline fitting and Skia floating-point booleans approximate raster boundary positions.',
  'Preserving actual G grain does not establish R-like textural quality.',
  'Root must perform actual 480px/full-frame pixel checks, native vector import/readback and independent review.',
  'No helper copy, seal, font outline substitution, image-generation call, Figma write, business-state write or protected-photo edit by this worker.'
 ]
}
(BASE/'PROVENANCE.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'status':receipt['status'],'svg_bytes':receipt['output']['bytes'],'sha256':receipt['output']['sha256'],'source_paths':len(source_paths),'cream_final_bounds':receipt['output']['cream_final_pathops_bounds'],'path_count':5},ensure_ascii=True))
