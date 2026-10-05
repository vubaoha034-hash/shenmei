"""Prepare only the one new V29 four-glyph source material.

The unchanged mature V24 tracer script is executed from fixed original bytes.
Only source/output refs and upstream filter_speckle=8 adapt to the new source.
No formal poster, placement, redraw, image generation, state or external writes.
--verify-only parses saved SVG and checks every original before; never retraces.
"""
from pathlib import Path
import argparse,copy,hashlib,json,sys,xml.etree.ElementTree as ET
sys.dont_write_bytecode=True
import PIL
from PIL import Image
ROOT=Path(__file__).resolve().parents[5]
OUT=Path(__file__).resolve().parent
PRIVATE=ROOT/'.liu-visual-private/correct_source_typography/v29'
SERIES=OUT.parent
UPSTREAM=SERIES/'v24/trace_source_once.py'
UPSTREAM_SHA='45f7eb01e6863601bd9e4ffe0c8d07bb851f0809d7566afefbf8b415996d52a7'
NS='{http://www.w3.org/2000/svg}'
SOURCE_COPY='山野慢饮'
INTERVALS=[('山',0,540),('野',540,1096),('慢',1096,1640),('饮',1640,2172)]
PARAMETERS={'img_format':'png','colormode':'binary','mode':'spline',
            'filter_speckle':8,'corner_threshold':60,'length_threshold':4.0,
            'max_iterations':10,'splice_threshold':45,'path_precision':3}

def sha(raw):return hashlib.sha256(raw).hexdigest()
def jb(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def commands_sha(v):
    return sha(json.dumps(v,ensure_ascii=False,sort_keys=True,
                         separators=(',',':'),allow_nan=False).encode('utf-8'))
def ref(p,raw=None):
    p=Path(p).resolve();assert p.is_relative_to(ROOT.resolve())
    raw=p.read_bytes() if raw is None else raw
    return {'path':p.relative_to(ROOT).as_posix(),'sha256':sha(raw),'bytes':len(raw)}
def ident(p):
    v=ref(p);v['mtime_ns']=str(Path(p).stat().st_mtime_ns);return v
def checked(r):
    b=(ROOT/r['path']).read_bytes();assert sha(b)==r['sha256'],'BOUND_SOURCE_CHANGED:'+r['path']
    if 'bytes' in r:assert len(b)==r['bytes']
    return b

def context():
    intake=json.loads((OUT/'SOURCE_MATERIAL_INTAKE.json').read_bytes())
    assert intake['stage']=='PREP_V29_SOURCE_ONLY'
    assert intake['requested_source_copy']==SOURCE_COPY
    assert not intake['formal_V29_poster_created'] and intake['source_bitmap_edits']==0
    source=intake['preserved_source_copy'];checked(source)
    original=Path(intake['original_generated_output']['absolute_path'])
    assert original.read_bytes()==checked(source)
    assert str(original.stat().st_mtime_ns)==intake['original_generated_output']['mtime_ns']
    for r in intake['V28_declared_assets_preserved']:
        assert ident(ROOT/r['path'])==r,'V28_ASSET_CHANGED:'+r['path']
    checked(intake['frozen_photograph']);checked(intake['frozen_brand'])
    auth=json.loads(checked(intake['authorization']))
    assert auth['scope']['copy_content_change'] and auth['scope']['copy_layout_change']
    checked(intake['independent_design_diagnosis'])
    upstream=UPSTREAM.read_bytes();assert sha(upstream)==UPSTREAM_SHA
    k={'__file__':str(UPSTREAM),'__name__':'v29_unchanged_upstream_trace'}
    exec(compile(upstream,str(UPSTREAM),'exec'),k)
    original_parameters=copy.deepcopy(k['TRACE_PARAMETERS'])
    assert {key:v for key,v in PARAMETERS.items() if key!='filter_speckle'}=={
        key:v for key,v in original_parameters.items() if key!='filter_speckle'}
    assert original_parameters['filter_speckle']==0
    k['OUT']=OUT;k['PRIVATE']=PRIVATE;k['TRACE_PARAMETERS']=copy.deepcopy(PARAMETERS)
    return k,intake,original_parameters

def inspect_commands(k,trace):
    records=k['source_commands'](trace)
    records['schema']='vpd-v29-four-glyph-source-command-inspection/v1'
    records['copy']=SOURCE_COPY
    records['stage']='PREP_V29_SOURCE_ONLY'
    records['source_bitmap_edited']=False
    return records

def replay_contour(pen,contour):
    for cmd in contour:
        op=cmd['op'];points=[tuple(v) for v in cmd['points']]
        if op=='moveTo':pen.moveTo(points[0])
        elif op=='lineTo':pen.lineTo(points[0])
        elif op=='curveTo':pen.curveTo(*points)
        elif op=='qCurveTo':pen.qCurveTo(*points)
        elif op=='closePath':pen.closePath()
        else:raise AssertionError('SOURCE_COMMAND_UNSUPPORTED:'+op)

def contour_d(contour):
    names={'moveTo':'M','lineTo':'L','curveTo':'C','qCurveTo':'Q','closePath':'Z'}
    return ' '.join(names[c['op']]+(' '+' '.join(format(float(v),'.17g')
                for point in c['points'] for v in point) if c['points'] else '')
                for c in contour)

def group_source(records,source_ref,trace_ref,commands_ref):
    from fontTools.pens.boundsPen import BoundsPen
    from fontTools.pens.recordingPen import RecordingPen
    from fontTools.svgLib.path import parse_path
    glyphs=[{'char':char,'source_ownership_interval':[left,right],
             'source_contours':[],'natural_ink_bounds':None,
             'local_curve_edits':0,'poster_placement':None}
             for char,left,right in INTERVALS]
    used=[];empty=[]
    for row in records['paths']:
        if row['empty_d']:
            assert not row['closed_contours'];empty.append(row['path_index']);continue
        for ci,before in enumerate(row['closed_contours']):
            assert before[0]['op']=='moveTo' and before[-1]['op']=='closePath'
            pen=BoundsPen(None);replay_contour(pen,before);b=list(pen.bounds)
            centre=(b[0]+b[2])/2
            matches=[i for i,(_,left,right) in enumerate(INTERVALS) if left<=centre<right]
            assert len(matches)==1,'AMBIGUOUS_SOURCE_GLYPH'
            i=matches[0];char,left,right=INTERVALS[i]
            assert b[0]>=left-1 and b[2]<=right+1,'SOURCE_CONTOUR_SPANS_GLYPHS'
            d=contour_d(before)
            r=RecordingPen();parse_path(d,r)
            parsed=[{'op':op,'points':[[float(x),float(y)] for x,y in pts]}
                    for op,pts in r.value]
            assert parsed==before,'LOSSLESS_SOURCE_CURVE_SERIALIZATION_FAILED'
            item={'path_index':row['path_index'],'contour_index':ci,
                  'before_sha256':commands_sha(before),'before':before,
                  'literal_upstream_d_sha256':row['d_sha256'],
                  'literal_upstream_transform':row['literal_transform'],
                  'bounds_png_coordinates':b,
                  'source_command_reference':commands_ref,'curve_edits':0}
            glyphs[i]['source_contours'].append(item);used.append((row['path_index'],ci))
            old=glyphs[i]['natural_ink_bounds']
            glyphs[i]['natural_ink_bounds']=b if old is None else [
                min(old[0],b[0]),min(old[1],b[1]),max(old[2],b[2]),max(old[3],b[3])]
    expected=[(r['path_index'],ci) for r in records['paths']
              for ci in range(len(r['closed_contours']))]
    assert sorted(used)==sorted(expected) and len(used)==len(set(used))
    assert all(g['source_contours'] for g in glyphs)
    for g in glyphs:
        b=g['natural_ink_bounds'];g['natural_width']=b[2]-b[0];g['natural_height']=b[3]-b[1]
        g['closed_contour_count']=len(g['source_contours'])
    mapping={'schema':'vpd-v29-four-glyph-original-before-map/v1',
             'stage':'PREP_V29_SOURCE_ONLY','source_version':29,'copy':SOURCE_COPY,
             'generated_source':source_ref,'literal_upstream_trace':trace_ref,
             'original_commands':commands_ref,'path_count':records['path_count'],
             'empty_path_indices':empty,'closed_contour_count':len(expected),
             'all_retained_before_bound_once':True,
             'before_hash_serialization':'Same mature kernel commands_sha: ensure_ascii=False,sort_keys=True,separators=(comma,colon),allow_nan=False; UTF-8 SHA256.',
             'glyphs':glyphs,'uniform_source_scale_applied':1,
             'source_original_coordinate_system':[2172,724],
             'manual_curve_redraws':0,'manual_component_deletions':0,
             'poster_layout_or_scaling_performed':False,'aesthetic_pass_claimed':False}
    raw=['<svg xmlns="http://www.w3.org/2000/svg" width="2172" height="724" viewBox="0 0 2172 724">']
    for g in glyphs:
        d=' '.join(contour_d(c['before']) for c in g['source_contours'])
        raw.append('<path data-char="'+g['char']+'" fill="#000000" fill-rule="nonzero" d="'+d+'"/>')
    raw.append('</svg>')
    vector=('\n'.join(raw)+'\n').encode('utf-8')
    tree=ET.fromstring(vector)
    assert len(list(tree))==4 and all(n.tag==NS+'path' for n in tree)
    assert [n.get('data-char') for n in tree]==list(SOURCE_COPY)
    return mapping,vector

def produce_one(k,intake,original_parameters):
    # This is the only VTracer call in this program, inside original fixed bytes.
    outputs,metadata=k['production_trace'](intake['preserved_source_copy'],
                                           ref(OUT/'SOURCE_MATERIAL_INTAKE.json'))
    trace=outputs[OUT/'upstream-alpha128-trace.svg']
    commands=inspect_commands(k,trace);command_raw=jb(commands)
    outputs[OUT/'TRACE_COMMANDS.json']=command_raw
    old_builder=metadata['builder']
    metadata['schema']='vpd-v29-one-new-four-glyph-production-trace/v1'
    metadata['formal_version']=29
    metadata['stage']='PREP_V29_SOURCE_ONLY'
    metadata['copy']=SOURCE_COPY
    metadata['builder']=ref(Path(__file__))
    metadata['unchanged_mature_upstream_builder']=old_builder
    metadata['upstream_parameters_before_adaptation']=original_parameters
    metadata['parameter_adaptation']={
        'only_changed_parameter':'filter_speckle','from':0,'to':8,
        'observed_native_alpha128_micro_components':{'count':21,'total_px2':56,'max_px2':7},
        'smallest_main_component_px2':5115,
        'no_manual_bitmap_or_contour_deletion':True}
    metadata['outputs']['commands']=ref(OUT/'TRACE_COMMANDS.json',command_raw)
    metadata['formal_poster_created']=False
    metadata['source_bitmap_edits']=0
    metadata['source_imagegen_actor']='Root'
    metadata['source_imagegen_backend_model']='NOT_EXPOSED'
    metadata['worker_imagegen_calls']=0
    outputs[OUT/'SOURCE_TRACE.json']=jb(metadata)
    mapping,vector=group_source(commands,intake['preserved_source_copy'],
                               ref(OUT/'upstream-alpha128-trace.svg',trace),
                               ref(OUT/'TRACE_COMMANDS.json',command_raw))
    outputs[OUT/'SOURCE_GLYPH_MAP.json']=jb(mapping)
    outputs[OUT/'SOURCE_GLYPHS.svg']=vector
    return outputs,metadata,mapping

def verify_existing(k,intake):
    metadata=json.loads((OUT/'SOURCE_TRACE.json').read_bytes())
    assert metadata['schema']=='vpd-v29-one-new-four-glyph-production-trace/v1'
    assert metadata['formal_version']==29 and metadata['copy']==SOURCE_COPY
    assert metadata['stage']=='PREP_V29_SOURCE_ONLY'
    assert metadata['production_trace_calls_by_this_script']==1
    assert metadata['trace_parameters']==PARAMETERS
    assert metadata['unchanged_mature_upstream_builder']==ref(UPSTREAM)
    assert metadata['builder']==ref(Path(__file__))
    assert not metadata['formal_poster_created'] and metadata['source_bitmap_edits']==0
    for r in metadata['dependencies'].values():checked(r)
    for r in metadata['outputs'].values():checked(r)
    assert metadata['generated_png']==intake['preserved_source_copy']
    assert metadata['generation_evidence']==ref(OUT/'SOURCE_MATERIAL_INTAKE.json')
    trace=checked(metadata['outputs']['trace'])
    commands=inspect_commands(k,trace)
    assert (OUT/'TRACE_COMMANDS.json').read_bytes()==jb(commands)
    mapping,vector=group_source(commands,intake['preserved_source_copy'],
                               metadata['outputs']['trace'],metadata['outputs']['commands'])
    assert (OUT/'SOURCE_GLYPH_MAP.json').read_bytes()==jb(mapping)
    assert (OUT/'SOURCE_GLYPHS.svg').read_bytes()==vector
    # No convert call. Verify derived tracing input using preserved alpha only.
    import io
    im=Image.open(io.BytesIO(checked(intake['preserved_source_copy'])))
    binary=im.getchannel('A').point(lambda v:0 if v>=128 else 255).convert('RGB')
    saved=Image.open(PRIVATE/'headline-alpha128.png')
    assert im.size==saved.size and saved.mode=='RGB' and saved.tobytes()==binary.tobytes()
    return metadata,mapping

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write',action='store_true')
    mode.add_argument('--verify-only',action='store_true')
    args=parser.parse_args()
    expected=[OUT/n for n in ['upstream-alpha128-trace.svg','TRACE_COMMANDS.json',
                             'SOURCE_TRACE.json','SOURCE_GLYPH_MAP.json','SOURCE_GLYPHS.svg']]
    expected += [PRIVATE/'headline-alpha128.png']
    k,intake,old_params=context()
    if args.write:
        assert not any(p.exists() for p in expected),'SOURCE_TRACE_ALREADY_EXISTS'
        outputs,metadata,mapping=produce_one(k,intake,old_params)
        assert set(outputs)==set(expected)
        assert not any(p.exists() for p in expected),'OUTPUT_APPEARED_DURING_TRACE'
        for p,b in outputs.items():
            with p.open('xb') as f:f.write(b)
        for p,b in outputs.items():assert p.read_bytes()==b
        context()
    else:metadata,mapping=verify_existing(k,intake)
    print(json.dumps({'action':'one-new-source-traced-and-bound' if args.write else 'existing-source-verified-no-retrace',
        'stage':'PREP_V29_SOURCE_ONLY','writes':len(expected) if args.write else 0,
        'production_trace_calls_this_execution':1 if args.write else 0,
        'trace':ref(OUT/'upstream-alpha128-trace.svg'),'commands':ref(OUT/'TRACE_COMMANDS.json'),
        'provenance':ref(OUT/'SOURCE_TRACE.json'),'source_glyph_map':ref(OUT/'SOURCE_GLYPH_MAP.json'),
        'source_glyph_vector':ref(OUT/'SOURCE_GLYPHS.svg'),'parameters':PARAMETERS,
        'paths':mapping['path_count'],'closed_contours':mapping['closed_contour_count'],
        'glyphs':[{'char':g['char'],'source_contours':g['closed_contour_count'],
                  'natural_bounds':g['natural_ink_bounds'],'natural_width':g['natural_width'],
                  'natural_height':g['natural_height']} for g in mapping['glyphs']],
        'manual_redraws':0,'manual_component_deletions':0,'source_bitmap_edits':0,
        'formal_poster_created':False,'aesthetic_pass_claimed':False},ensure_ascii=False))
if __name__=='__main__':main()
