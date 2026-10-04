"""V23: one uniform smaller/lower-left placement of the frozen V22 path group.

All 17 source path attributes, their row relation, and the raw trace survive.
No generation, retracing, glyph warp, foreground mask, or photo edit occurs.
--verify-only computes in memory and reads exact outputs, without writes.
--write requires Root's settled V22 failure gate and rejects existing outputs.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import io
import json
import runpy
import subprocess
import sys
import xml.etree.ElementTree as ET

sys.dont_write_bytecode = True
from PIL import Image, ImageChops
import PIL

ROOT = Path(__file__).resolve().parents[5]
FIXED_ROOT = Path('C:/Users/Administrator/OneDrive/文档/足球/shenmei-vpd-codex-20261003')
SERIES = ROOT/'evidence/vpd/codex_takeover_20261003/product_type_integration_20261004'
OUT = Path(__file__).resolve().parent
PRIVATE = ROOT/'.liu-visual-private/correct_source_typography/v23'
RUNTIME = Path('C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies')
NS = '{http://www.w3.org/2000/svg}'
ET.register_namespace('',NS[1:-1])
COPY = '一杯茶，慢下来'
SCALE,TX,TY = 0.3488013255394301,524.3160869265243,432.0762262905397
AFFINE = f'matrix({SCALE} 0 0 {SCALE} {TX} {TY})'
EXPECTED_ALPHA_BBOX = (610,515,990,721)
INPUTS = {
    'photo':(ROOT/'.liu-visual-private/source_recovery_20261003/photography-local-reconstruction-final.png',
             '7fd7777fed21100cb6b47bc305701476054263565e73246ac469d065aa080618'),
    'headline22':(SERIES/'v22/headline.svg','e9feab432466d4f1a7188fdeff746ab6773a538ff59d1f2c3fa477aa3de6d14d'),
    'trace22':(SERIES/'v22/upstream-alpha128-trace.svg','1c1d0af28c3534426432441ff8944be0ea5f8ae33736c225740c65541017ff6c'),
    'brand':(SERIES/'v22/brand.svg','dd8e9e899393dc36eb3f5b1652bdbb740787d41a108ea6aa1eae05cb1368b1ff'),
    'provenance22':(SERIES/'v22/LETTERING_PROVENANCE.json','a0347f590446723993b74fa711be39474f5c84295cf2909ad99178fcc7a33142'),
    'generated_phrase22':(ROOT/'.liu-visual-private/correct_source_typography/v22/headline-generated-01.png',
                          'fcb4b5097ae1610dfd84ba6eb49fef7853d254d0c405c5e47600f35095064d2c'),
    'generation_execution22':(SERIES/'v22/IMAGEGEN_EXECUTION.json','810f4dad695cf39a591a2b1e8e1e50ebcea69b72eea6d7d240d297d203b338ad'),
    'v22_builder':(SERIES/'v22/build_headline_asset.py','c08a93bbfe518c96987ea9273692ab5602350c37ccd79d8a3545516c5b9e5fc6'),
    'renderer_helper':(SERIES/'v18/build_headline_asset.py','24102f462f379255c29be0209cd63f91d3e862f80956a96b012471eccc18e8e5')}
PUBLIC = ['headline.svg','upstream-alpha128-trace.svg','brand.svg','LETTERING_PROVENANCE.json']
PRIV = ['headline-render.png','preview.png']


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def jb(obj):
    return (json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode('utf-8')


def ref(path,raw):
    return {'path':path.relative_to(ROOT).as_posix(),'sha256':sha(raw),'bytes':len(raw)}


def xml(root):
    return (ET.tostring(root,encoding='unicode')+'\n').encode('utf-8')


def png(image):
    buffer=io.BytesIO();image.save(buffer,format='PNG');return buffer.getvalue()


def root_gate():
    raw=(ROOT/'continuity/vpd/CURRENT_TASK_LOCK.json').read_bytes()
    lock=json.loads(raw);unit=lock['codex_takeover']['worker_continuation'];last=unit['versions'][-1]
    assert (lock['revision']>=320 and unit['unit_id']=='CHAZUO_APPROVED_SOURCE_TYPOGRAPHY_20261003_R1'
            and unit['phase']=='REVISION_REQUIRED' and last['number']==22 and last['verdict']=='AI_FAIL'), 'ROOT_GO_GATE_NOT_SATISFIED'
    return {'revision':lock['revision'],'phase':unit['phase'],'last_version':last['number'],
            'verdict':last['verdict'],'lock_sha256':sha(raw)}


def read_inputs(photo_path=None,headline_path=None):
    assert ROOT.resolve()==FIXED_ROOT.resolve(), 'ROOT_PATH_IDENTITY_MISMATCH'
    assert OUT.resolve()==(SERIES/'v23').resolve(), 'OUTPUT_PATH_IDENTITY_MISMATCH'
    if photo_path is not None:
        assert Path(photo_path).resolve()==INPUTS['photo'][0].resolve(), 'SOURCE_PHOTO_PATH_IDENTITY_MISMATCH'
    if headline_path is not None:
        assert Path(headline_path).resolve()==INPUTS['headline22'][0].resolve(), 'SOURCE_HEADLINE_PATH_IDENTITY_MISMATCH'
    raw={}
    for key,(path,expected) in INPUTS.items():
        raw[key]=path.read_bytes()
        assert sha(raw[key])==expected, 'FIXED_SOURCE_CHANGED:'+key
    return raw


def relocate(raw):
    prior=json.loads(raw['provenance22'])
    root=ET.fromstring(raw['headline22']);trace=ET.fromstring(raw['trace22'])
    group=root.find(NS+'g');paths=list(group)
    assert group.get('transform')==prior['one_whole_sentence_affine']
    assert len(paths)==len(trace)==17 and all(p.tag==NS+'path' and p.get('d','').strip() for p in paths)
    before=[dict(p.attrib) for p in paths]
    rows=prior['source_to_output_contours']
    assert len(rows)==17 and prior['nonempty_paths_omitted']==0
    for p,row in zip(paths,rows):
        source=trace[row['upstream_index']]
        assert p.get('d')==source.get('d') and p.get('transform')==source.get('transform')==row['literal_source_translate']
        assert sha(p.get('d').encode('utf-8'))==row['d_sha256'] and p.get('fill')=='#F5F2E6'
    group.set('transform',AFFINE);group.set('id','V23-one-whole-sentence')
    root.find(NS+'desc').text='V23 frozen V22 generated lettering; all original 17 d/translate paths retained. Only one whole-phrase uniform smaller/lower-left placement changes. No mask or photograph pixels embedded.'
    assert [dict(p.attrib) for p in group]==before, 'SOURCE_PATH_ATTRIBUTE_CHANGED'
    assert root.get('width')=='1536' and root.get('height')=='1024' and root.get('viewBox')=='0 0 1536 1024'
    assert all(n.tag in {NS+'svg',NS+'g',NS+'path',NS+'title',NS+'desc'} for n in root.iter())
    assert root.find(NS+'title').text==COPY
    headline=xml(root);assert len(headline.decode('utf-8'))<=45000
    return headline,root,prior,rows


def geometric_box(source):
    return [SCALE*source[0]+TX,SCALE*source[1]+TY,SCALE*source[2]+TX,SCALE*source[3]+TY]


def subphrase_alpha(root,indices,render):
    clone=copy.deepcopy(root);group=clone.find(NS+'g')
    for i,node in enumerate(list(group)):
        if i not in indices:
            group.remove(node)
    return render(xml(clone)).getchannel('A')


def calculate(photo_path=None,headline_path=None):
    raw=read_inputs(photo_path,headline_path)
    assert PIL.__version__=='12.3.0' and sys.version_info[:3]==(3,12,14), 'RUNTIME_VERSION_CHANGED'
    helper=runpy.run_path(str(INPUTS['renderer_helper'][0]));render=helper['render']
    v22=runpy.run_path(str(INPUTS['v22_builder'][0]))
    code='const s=require('+json.dumps((RUNTIME/'node/node_modules/sharp').as_posix())+');process.stdout.write(JSON.stringify({node:process.version,sharp:s.versions.sharp,rsvg:s.versions.rsvg}));'
    runtime=json.loads(subprocess.run([str(RUNTIME/'node/bin/node.exe'),'-e',code],capture_output=True,check=True).stdout)
    assert runtime=={'node':'v24.19.0','sharp':'0.35.4','rsvg':'2.62.91'}, 'RENDERER_VERSION_CHANGED'
    headline,root,prior,rows=relocate(raw)
    rgba=render(headline);alpha=rgba.getchannel('A');bbox=alpha.getbbox()
    assert bbox==EXPECTED_ALPHA_BBOX, 'UNEXPECTED_UNIQUE_LAYOUT_ALPHA'
    # Diagnostic renders use this same placement; they are not other candidates.
    one=subphrase_alpha(root,{4},render)
    upper=subphrase_alpha(root,set(range(10)),render)
    lower=subphrase_alpha(root,set(range(10,17)),render)
    brand,brand_metrics=v22['brand_canvas'](raw['brand'],render)
    assert brand_metrics['x']==285 and brand_metrics['y']==198 and brand_metrics['width']==205
    photo=Image.open(io.BytesIO(raw['photo'])).convert('RGBA')
    assert photo.size==rgba.size==brand.size==(1536,1024)
    preview=photo.copy();preview.alpha_composite(brand);preview.alpha_composite(rgba)
    assert INPUTS['photo'][0].read_bytes()==raw['photo'], 'PHOTO_SOURCE_CHANGED_DURING_BUILD'
    outside=Image.new('L',(1536,1024),255)
    for b in (bbox,tuple(brand_metrics['actual_alpha_bbox_exclusive'])):
        outside.paste(0,b)
    diff=ImageChops.difference(preview.convert('RGB'),photo.convert('RGB'))
    for channel in diff.split():
        assert ImageChops.darker(channel,outside).getbbox() is None, 'UNREGISTERED_OUTSIDE_RGB_CHANGED'
    assets={'headline.svg':headline,'upstream-alpha128-trace.svg':raw['trace22'],'brand.svg':raw['brand']}
    private={'headline-render.png':png(rgba),'preview.png':png(preview)}
    report={'schema':'vpd-v23-single-whole-group-placement/v1','version':23,'copy':COPY,'brand':'茶作',
        'viewport':[1536,1024],'lines':['一杯茶，','慢下来'],
        'source_inputs':{k:ref(INPUTS[k][0],v) for k,v in raw.items()},
        'reused_original_generated_source':prior['source_inputs']['generated_phrase'],
        'reused_alpha_facts':prior['alpha_facts'],'reused_trace_parameters':prior['trace_parameters'],
        'source_to_output_contours':rows,'source_curve_bounds':prior['source_curve_bounds'],
        'retained_paths':17,'empty_d_paths_omitted':[],'nonempty_paths_omitted':0,
        'all_V22_path_attributes_preserved':True,'all_source_d_and_translate_preserved':True,
        'only_artwork_change':'One whole-group uniform scale and translation; relative glyph positions and two-line relation retained.',
        'previous_whole_sentence_affine':prior['one_whole_sentence_affine'],'one_whole_sentence_affine':AFFINE,
        'uniform_scale':SCALE,'translation':[TX,TY],'scale_ratio_vs_V22':SCALE/prior['uniform_scale'],
        'geometric_output_bounds':geometric_box(prior['source_curve_bounds']),
        'actual_alpha_bbox_exclusive':list(bbox),
        'one_stroke':{'source_path_index':4,'source_d_sha256':rows[4]['d_sha256'],
            'geometric_output_bounds':geometric_box(rows[4]['source_curve_bounds']),
            'actual_alpha_bbox_exclusive':list(one.getbbox())},
        'actual_upper_row_alpha_bbox':list(upper.getbbox()),'actual_lower_row_alpha_bbox':list(lower.getbbox()),
        'unique_placement_rationale':'Read the frozen S and R actual pixels: move the upper horizontal into the right half of the cup-mouth field; lower row into the tray-left/fresh-leaf field, using one compact unchanged glyph group. Pixel contact must be inspected, not inferred as aesthetic success.',
        'brand_placement':brand_metrics,'source_photo_bytes_unchanged':True,
        'preview_composition':'Exact S decoded RGBA + registered unchanged brand SVG at x285/y198/width205 + registered full-frame headline SVG, and no other layer.',
        'foreground_mask_or_photo_raster_layers_added':0,'old_product_core_RGB0_rule_used':False,
        'strict_source_plus_registered_SVG_composition_used':True,'outside_registered_overlay_RGB_differences':0,
        'original_generated_PNG_preserved_in_V22':True,'upstream_trace_bytes_preserved':True,
        'native_TEXT_claimed':False,'editability':'17 editable original VTracer path elements under one uniform whole-phrase matrix.',
        'svg_character_length':len(headline.decode('utf-8')),
        'software':{'Python':sys.version,'Pillow':PIL.__version__,**runtime,
            'V22_helper':'Unchanged fixed builder; reuse its brand_canvas only, no calculate/trace function called.',
            'renderer':'Unchanged fixed V18 Sharp/librsvg render helper.',
            'trace_dependency_origin':prior['software'],'new_VTracer_or_FontTools_operations':0},
        'source_license_and_approximation_boundaries':{'licence':prior['licence_boundary'],'approximation':prior['approximation_boundary']},
        'new_imagegen_operations':0,'new_vectorization_operations':0,'new_font_outline_operations':0,
        'per_character_repositioning_operations':0,'whole_group_placement_operations':1,
        'worker_photo_edits':0,'private_fullpreview_files':1,'hidden_or_alternate_candidates':0,
        'worker_business_state_writes':0,'worker_Figma_Drive_Git_writes':0,
        'aesthetic_pass_claimed':False,'formal_independent_review':None,'human_approval_claimed':False,
        'outputs':{k:ref(OUT/k,v) for k,v in assets.items()},
        'private_outputs':{k:ref(PRIVATE/k,v) for k,v in private.items()},
        'builder':ref(Path(__file__),Path(__file__).read_bytes()),
        'builder_modes':{'verify_only':'Memory-only render plus optional exact readback; no mkdir/save/write.',
            'write':'Settled V22 failure Root gate, all fixed-input checks, all-target preflight, exclusive creation; no multi-file atomicity claim.'}}
    assets['LETTERING_PROVENANCE.json']=jb(report)
    return {**{OUT/k:v for k,v in assets.items()},**{PRIVATE/k:v for k,v in private.items()}},report


def main():
    parser=argparse.ArgumentParser(description=__doc__);mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--verify-only',action='store_true');mode.add_argument('--write',action='store_true')
    parser.add_argument('--source-photo');parser.add_argument('--source-headline')
    args=parser.parse_args();targets=[OUT/n for n in PUBLIC]+[PRIVATE/n for n in PRIV]
    if args.write:
        assert not any(p.exists() for p in targets), 'OUTPUT_ALREADY_EXISTS'
        gate=root_gate()
    outputs,report=calculate(args.source_photo,args.source_headline)
    assert set(outputs)==set(targets)
    if args.verify_only:
        existing=[p for p in targets if p.exists()]
        if existing:
            assert len(existing)==len(targets), 'PARTIAL_OUTPUTS_PRESENT'
            for path,raw in outputs.items():
                assert path.read_bytes()==raw, 'OUTPUT_READBACK_MISMATCH:'+str(path)
        action='verified-existing' if existing else 'verified-before-write'
    else:
        assert not any(p.exists() for p in targets), 'OUTPUT_ALREADY_EXISTS'
        OUT.mkdir(parents=True,exist_ok=True);PRIVATE.mkdir(parents=True,exist_ok=True)
        for path,raw in outputs.items():
            with path.open('xb') as file:
                file.write(raw)
        for path,raw in outputs.items():
            assert path.read_bytes()==raw, 'POST_WRITE_READBACK_MISMATCH:'+str(path)
        action='wrote-new'
    print(json.dumps({'mode':'verify-only' if args.verify_only else 'write','action':action,
        'writes':0 if args.verify_only else len(outputs),'paths':17,'nonempty_omission':0,
        'all_V22_path_attributes_preserved':True,'svg_chars':report['svg_character_length'],
        'bbox':report['actual_alpha_bbox_exclusive'],'affine':AFFINE,
        'one_alpha_bbox':report['one_stroke']['actual_alpha_bbox_exclusive'],
        'upper_row_bbox':report['actual_upper_row_alpha_bbox'],'lower_row_bbox':report['actual_lower_row_alpha_bbox'],
        'headline':report['outputs']['headline.svg'],'preview':report['private_outputs']['preview.png'],
        'provenance':ref(OUT/'LETTERING_PROVENANCE.json',outputs[OUT/'LETTERING_PROVENANCE.json']),
        **({'root_gate':gate} if args.write else {})},ensure_ascii=True))


if __name__=='__main__':
    main()
