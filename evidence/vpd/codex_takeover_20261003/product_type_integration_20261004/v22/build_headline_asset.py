"""V22 single generated phrase -> fixed alpha128 -> unchanged VTracer -> SVG.

No new image generation, glyph rewriting, foreground mask or photo editing.
All nonempty upstream d/translate strings survive under one uniform matrix.
--verify-only renders in memory and reads existing outputs, without file writes.
--write requires Root's closed V21 failure gate and rejects existing assets.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import importlib.metadata
import io
import json
import re
import runpy
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile

sys.dont_write_bytecode = True
from PIL import Image, ImageChops
import PIL

ROOT = Path(__file__).resolve().parents[5]
FIXED_ROOT = Path('C:/Users/Administrator/OneDrive/文档/足球/shenmei-vpd-codex-20261003')
SERIES = ROOT / 'evidence/vpd/codex_takeover_20261003/product_type_integration_20261004'
OUT = Path(__file__).resolve().parent
PRIVATE = ROOT / '.liu-visual-private/correct_source_typography/v22'
DEP = ROOT / '.liu-visual-private/dependencies/vtracer_0_6_15_cp312'
RUNTIME = Path('C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies')
NS = '{http://www.w3.org/2000/svg}'
ET.register_namespace('',NS[1:-1])
COPY = '一杯茶，慢下来'
ALLOWANCE = (680,455,1230,715)
FIT = (681,456,1229,714)
TRACE_SHA = '1c1d0af28c3534426432441ff8944be0ea5f8ae33736c225740c65541017ff6c'
TRACE_PARAMETERS = {'img_format':'png','colormode':'binary','mode':'spline','filter_speckle':0,
                    'corner_threshold':60,'length_threshold':4.0,'max_iterations':10,
                    'splice_threshold':45,'path_precision':3}
INPUTS = {
    'generated_phrase':(PRIVATE/'headline-generated-01.png','fcb4b5097ae1610dfd84ba6eb49fef7853d254d0c405c5e47600f35095064d2c'),
    'photo':(ROOT/'.liu-visual-private/source_recovery_20261003/photography-local-reconstruction-final.png',
             '7fd7777fed21100cb6b47bc305701476054263565e73246ac469d065aa080618'),
    'brand':(SERIES/'v21/brand.svg','dd8e9e899393dc36eb3f5b1652bdbb740787d41a108ea6aa1eae05cb1368b1ff'),
    'prompt':(OUT/'IMAGEGEN_PROMPT.txt','c8b3ea1435e12f8c159cc0adc215d965e8b49fcda461477499a3f498cb9e935c'),
    'renderer_helper':(SERIES/'v18/build_headline_asset.py','24102f462f379255c29be0209cd63f91d3e862f80956a96b012471eccc18e8e5'),
    'vtracer_wrapper':(DEP/'site-packages/vtracer/__init__.py','3e697358d7fb4a880b60fc279864b6f30e619807c183f2b54ccbd81c5d78d2f2'),
    'vtracer_binary':(DEP/'site-packages/vtracer/vtracer.cp312-win_amd64.pyd','59e2053fca8666479e7163eec45d8b15143435c7a8d14f6dbd26eec9716bfe66'),
    'vtracer_wheel':(DEP/'vtracer-0.6.15-cp312-cp312-win_amd64.whl','b0f08b66734e41872d4ac343ed6d08870b3235346def3e112e10b3b2443e619e'),
    'vtracer_license':(DEP/'source/vtracer-0.6.15/LICENSE','81ee739f355765c110fc89feff14ffffce829901f96ba811fd0b65a41a8636c7')}
PUBLIC = ['upstream-alpha128-trace.svg','headline.svg','brand.svg','IMAGEGEN_EXECUTION.json','LETTERING_PROVENANCE.json']
PRIV = ['headline-alpha128.png','headline-render.png','preview.png']


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def jb(obj):
    return (json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode('utf-8')


def ref(path,raw):
    return {'path':path.relative_to(ROOT).as_posix(),'sha256':sha(raw),'bytes':len(raw)}


def png(image):
    buffer = io.BytesIO()
    image.save(buffer,format='PNG')
    return buffer.getvalue()


def xml(root):
    return (ET.tostring(root,encoding='unicode')+'\n').encode('utf-8')


def root_gate():
    raw = (ROOT/'continuity/vpd/CURRENT_TASK_LOCK.json').read_bytes()
    lock = json.loads(raw); unit=lock['codex_takeover']['worker_continuation']; last=unit['versions'][-1]
    assert (lock['revision']>=318 and unit['unit_id']=='CHAZUO_APPROVED_SOURCE_TYPOGRAPHY_20261003_R1'
            and unit['phase']=='REVISION_REQUIRED' and last['number']==21 and last['verdict']=='AI_FAIL'), 'ROOT_GO_GATE_NOT_SATISFIED'
    return {'revision':lock['revision'],'phase':unit['phase'],'last_version':last['number'],
            'verdict':last['verdict'],'lock_sha256':sha(raw)}


def read_inputs(photo_path=None,lettering_path=None):
    assert ROOT.resolve()==FIXED_ROOT.resolve(), 'ROOT_PATH_IDENTITY_MISMATCH'
    assert OUT.resolve()==(SERIES/'v22').resolve(), 'OUTPUT_PATH_IDENTITY_MISMATCH'
    if photo_path is not None:
        assert Path(photo_path).resolve()==INPUTS['photo'][0].resolve(), 'SOURCE_PHOTO_PATH_IDENTITY_MISMATCH'
    if lettering_path is not None:
        assert Path(lettering_path).resolve()==INPUTS['generated_phrase'][0].resolve(), 'SOURCE_LETTERING_PATH_IDENTITY_MISMATCH'
    raw = {}
    for key,(path,expected) in INPUTS.items():
        raw[key]=path.read_bytes()
        assert sha(raw[key])==expected, 'FIXED_SOURCE_CHANGED:'+key
    return raw


def assert_rectangle(box,allowed,label):
    assert box and box[0]>=allowed[0] and box[1]>=allowed[1] and box[2]<=allowed[2] and box[3]<=allowed[3], label


def trace_alpha(raw):
    sys.path.insert(0,str(DEP/'site-packages'))
    import vtracer
    assert importlib.metadata.version('vtracer')=='0.6.15', 'VTRACER_VERSION_CHANGED'
    with zipfile.ZipFile(io.BytesIO(raw['vtracer_wheel'])) as wheel:
        assert raw['vtracer_wrapper']==wheel.read('vtracer/__init__.py'), 'VTRACER_WRAPPER_MODIFIED'
        assert raw['vtracer_binary']==wheel.read('vtracer/vtracer.cp312-win_amd64.pyd'), 'VTRACER_IMPLEMENTATION_MODIFIED'
    source = Image.open(io.BytesIO(raw['generated_phrase']))
    assert source.mode=='RGBA' and source.size==(1536,1024), 'GENERATED_PHRASE_FORMAT_CHANGED'
    alpha = source.getchannel('A'); hist=alpha.histogram()
    binary = alpha.point(lambda v:0 if v>=128 else 255).convert('RGB')
    binary_png = png(binary)
    traced = vtracer.convert_raw_image_to_svg(binary_png,**TRACE_PARAMETERS).encode('utf-8')
    assert sha(traced)==TRACE_SHA, 'FIXED_ALPHA_TRACE_REPLAY_CHANGED'
    stats = {'source_mode':source.mode,'source_size':list(source.size),'alpha_extrema':list(alpha.getextrema()),
             'alpha0_pixels':hist[0],'alpha255_pixels':hist[255],
             'alpha1_to127_pixels':sum(hist[1:128]),'alpha128_to254_pixels':sum(hist[128:255]),
             'alpha_threshold_inclusive':128,'alpha128_pixels':sum(hist[128:]),
             'alpha128_bbox_exclusive':list(alpha.point(lambda v:255 if v>=128 else 0).getbbox()),
             'raw_visual_fact':'Original PNG includes glow. Fixed threshold removes low-alpha pixels, including glow and edge antialiasing; it does not reproduce source alpha losslessly.'}
    return traced,binary_png,stats


def compose_headline(trace_raw):
    sys.path.append('C:/Users/Administrator/AppData/Local/hermes/hermes-agent/venv/Lib/site-packages')
    import fontTools
    from fontTools.pens.boundsPen import BoundsPen
    from fontTools.svgLib.path import parse_path
    assert fontTools.__version__=='4.63.0', 'FONTTOOLS_VERSION_CHANGED'
    upstream = ET.fromstring(trace_raw)
    rows,paths,empty = [],[],[]
    for index,node in enumerate(upstream):
        assert node.tag==NS+'path', 'UNEXPECTED_UPSTREAM_ELEMENT'
        d=node.get('d','')
        if not d.strip():
            empty.append(index); continue
        bounds = BoundsPen(None); parse_path(d,bounds)
        assert bounds.bounds is not None, 'NONEMPTY_SOURCE_PATH_HAS_NO_BOUNDS'
        match=re.fullmatch(r'translate\(([-.\d]+),([-.\d]+)\)',node.get('transform',''))
        assert match, 'UNEXPECTED_SOURCE_TRANSLATE'
        dx,dy=map(float,match.groups()); b=bounds.bounds
        box=[b[0]+dx,b[1]+dy,b[2]+dx,b[3]+dy]
        rows.append({'upstream_index':index,'d_sha256':sha(d.encode('utf-8')),
                     'literal_source_translate':node.get('transform'),'source_curve_bounds':box})
        output=copy.deepcopy(node); output.set('fill','#F5F2E6'); output.set('id',f'original-alpha-contour-{index}')
        assert output.get('d')==d and output.get('transform')==node.get('transform')
        paths.append(output)
    assert len(paths)==17 and len(empty)==0, 'FIXED_TRACE_PATH_COUNT_CHANGED'
    box=[min(r['source_curve_bounds'][0] for r in rows),min(r['source_curve_bounds'][1] for r in rows),
         max(r['source_curve_bounds'][2] for r in rows),max(r['source_curve_bounds'][3] for r in rows)]
    scale=min((FIT[2]-FIT[0])/(box[2]-box[0]),(FIT[3]-FIT[1])/(box[3]-box[1]))
    tx=(FIT[0]+FIT[2])/2-scale*(box[0]+box[2])/2
    ty=FIT[1]-scale*box[1]
    affine=f'matrix({scale} 0 0 {scale} {tx} {ty})'
    root=ET.Element(NS+'svg',{'width':'1536','height':'1024','viewBox':'0 0 1536 1024','fill':'none'})
    ET.SubElement(root,NS+'title').text=COPY
    ET.SubElement(root,NS+'desc').text='V22 one generated phrase, fixed alpha128, original VTracer path strings and translations; one uniform whole-sentence placement. No fonts or photograph pixels embedded.'
    group=ET.SubElement(root,NS+'g',{'id':'V22-one-whole-sentence','transform':affine})
    for path in paths:
        group.append(path)
    assert all(node.tag in {NS+'svg',NS+'g',NS+'path',NS+'title',NS+'desc'} for node in root.iter()), 'UNREGISTERED_SVG_ELEMENT'
    headline=xml(root)
    assert len(headline.decode('utf-8'))<=45000
    return headline,{'upstream_path_count':len(upstream),'empty_d_paths_omitted':empty,'retained_paths':len(paths),
        'nonempty_paths_omitted':0,'source_to_output_contours':rows,'source_curve_bounds':box,
        'one_whole_sentence_affine':affine,'uniform_scale':scale,'translation':[tx,ty],
        'geometric_output_bounds':[scale*box[0]+tx,scale*box[1]+ty,scale*box[2]+tx,scale*box[3]+ty],
        'source_d_and_translate_preserved':True,'one_uniform_matrix':True,
        'defs_clip_mask_raster_elements':0,'FontTools_version':fontTools.__version__}


def brand_canvas(brand_raw,render):
    source=ET.fromstring(brand_raw); assert len(list(source.iter(NS+'path')))==7
    width,height=float(source.get('width')),float(source.get('height')); scale=205/width
    root=ET.Element(NS+'svg',{'width':'1536','height':'1024','viewBox':'0 0 1536 1024'})
    group=ET.SubElement(root,NS+'g',{'transform':f'translate(285 198) scale({scale})'})
    for node in source:
        group.append(copy.deepcopy(node))
    image=render(xml(root)); box=image.getchannel('A').getbbox()
    assert_rectangle(box,(64,56,504,304),'BRAND_OUTSIDE_AUTHORISED_AREA')
    return image,{'x':285,'y':198,'width':205,'height':height*scale,'uniform_scale':scale,
                  'actual_alpha_bbox_exclusive':list(box),'source_svg_bytes_preserved':True}


def calculate(photo_path=None,lettering_path=None):
    raw=read_inputs(photo_path,lettering_path)
    assert PIL.__version__=='12.3.0' and sys.version_info[:3]==(3,12,14), 'RUNTIME_VERSION_CHANGED'
    render=runpy.run_path(str(INPUTS['renderer_helper'][0]))['render']
    code='const s=require('+json.dumps((RUNTIME/'node/node_modules/sharp').as_posix())+');process.stdout.write(JSON.stringify({node:process.version,sharp:s.versions.sharp,rsvg:s.versions.rsvg}));'
    runtime=json.loads(subprocess.run([str(RUNTIME/'node/bin/node.exe'),'-e',code],capture_output=True,check=True).stdout)
    assert runtime=={'node':'v24.19.0','sharp':'0.35.4','rsvg':'2.62.91'}, 'RENDERER_VERSION_CHANGED'
    trace,binary,alpha_stats=trace_alpha(raw)
    headline,geometry=compose_headline(trace)
    rgba=render(headline); box=rgba.getchannel('A').getbbox()
    assert_rectangle(box,ALLOWANCE,'HEADLINE_OUTSIDE_AUTHORISED_AREA')
    brand,brand_metrics=brand_canvas(raw['brand'],render)
    photo=Image.open(io.BytesIO(raw['photo'])).convert('RGBA')
    assert photo.size==rgba.size==brand.size==(1536,1024)
    preview=photo.copy(); preview.alpha_composite(brand); preview.alpha_composite(rgba)
    # Full preview is exactly the frozen S plus these two registered SVG layers.
    source_check=INPUTS['photo'][0].read_bytes()
    assert source_check==raw['photo'], 'PHOTO_SOURCE_CHANGED_DURING_BUILD'
    outside=Image.new('L',(1536,1024),255)
    for b in (box,tuple(brand_metrics['actual_alpha_bbox_exclusive'])):
        outside.paste(0,b)
    diff=ImageChops.difference(preview.convert('RGB'),photo.convert('RGB'))
    for channel in diff.split():
        assert ImageChops.darker(channel,outside).getbbox() is None, 'UNREGISTERED_OUTSIDE_RGB_CHANGED'
    execution={'schema':'vpd-v22-built-in-imagegen-execution/v1','asset_number':22,
        'tool':'built-in image_gen imagegen','execution_metadata_provider':'Root; worker did not invoke generation',
        'started_at_utc':'2026-10-04T11:47:18Z','completed_at_utc':'2026-10-04T11:47:56Z',
        'generator_backend':'NOT_EXPOSED','generated_images_used':1,'new_imagegen_calls_by_this_worker':0,
        'alternate_samples_or_rerolls':0,'transparent_background_requested':True,
        'prompt':ref(INPUTS['prompt'][0],raw['prompt']),
        'original_returned_path':'C:/Users/Administrator/.codex/generated_images/01a0ffab-c9b7-7c40-b55b-e51535c156dd/exec-39096204-b580-40d4-9e5b-c6a3411984ed.png',
        'original_returned_path_SHA_verified_by_worker':'fcb4b5097ae1610dfd84ba6eb49fef7853d254d0c405c5e47600f35095064d2c',
        'preserved_source_copy':ref(INPUTS['generated_phrase'][0],raw['generated_phrase']),
        'alpha_facts':alpha_stats,'scope':'Exact one generated lettering asset; no photograph/logo generation or edit.'}
    assets={'upstream-alpha128-trace.svg':trace,'headline.svg':headline,'brand.svg':raw['brand'],
            'IMAGEGEN_EXECUTION.json':jb(execution)}
    private={'headline-alpha128.png':binary,'headline-render.png':png(rgba),'preview.png':png(preview)}
    report={'schema':'vpd-v22-single-generated-lettering-provenance/v1','version':22,'copy':COPY,
        'brand':'茶作','lines':['一杯茶，','慢下来'],'source_inputs':{k:ref(INPUTS[k][0],v) for k,v in raw.items()},
        'alpha_facts':alpha_stats,'trace_parameters':TRACE_PARAMETERS,**geometry,
        'actual_alpha_bbox_exclusive':list(box),'authorised_headline_rectangle':list(ALLOWANCE),
        'fit_rectangle_with_one_pixel_inset':list(FIT),'brand_placement':brand_metrics,
        'source_photo_bytes_unchanged':True,
        'preview_composition':'Frozen S decoded RGBA, then frozen brand SVG at registered uniform placement, then registered full-frame headline SVG; no other layer.',
        'foreground_mask_or_photo_raster_layers_added':0,'old_product_core_RGB0_rule_used':False,
        'strict_source_plus_registered_SVG_composition_used':True,
        'outside_registered_overlay_RGB_differences':0,
        'actual_leaf_mask_or_occlusion_claimed':False,
        'original_generated_PNG_preserved':True,'source_trace_replay_SHA_equal':True,
        'svg_character_length':len(headline.decode('utf-8')),
        'software':{'Python':sys.version,'Pillow':PIL.__version__,**runtime,
            'VTracer_python_package':'0.6.15','SVG_generator_comment':'visioncortex VTracer 0.6.12',
            'VTracer_implementation':'Existing official archived wheel; installed wrapper and binary byte-equal to archived wheel, unchanged',
            'VTracer_license':'MIT; existing full license retained and hashed in source_inputs',
            'FontTools_role':'Version4.63.0 BoundsPen/svgLib.path only; no font files loaded',
            'renderer':'Fixed existing V18 Sharp/librsvg helper; unchanged'},
        'lettering_source':'The one built-in generated PNG, informed by R and accurate source text. It is not the original Source Han font outline.',
        'licence_boundary':'No commercial/reference glyph files copied; VTracer MIT covers software. Image generator backend/font mechanism NOT_EXPOSED.',
        'approximation_boundary':'Fixed alpha>=128, spline trace/path_precision3, flat ivory fill and one uniform transform are not lossless reproduction of original glow/alpha.',
        'native_TEXT_claimed':False,'editability':'17 individually editable source spline paths under one whole-phrase matrix.',
        'worker_new_imagegen_calls':0,'worker_photo_edits':0,'private_fullpreview_files':1,
        'worker_business_state_writes':0,'worker_Figma_Drive_Git_writes':0,
        'aesthetic_pass_claimed':False,'formal_independent_review':None,'human_approval_claimed':False,
        'outputs':{k:ref(OUT/k,v) for k,v in assets.items()},
        'private_outputs':{k:ref(PRIVATE/k,v) for k,v in private.items()},
        'builder':ref(Path(__file__),Path(__file__).read_bytes()),
        'builder_modes':{'verify_only':'In-memory calculation and exact existing-file readback, no mkdir/save/write.',
            'write':'Settled V21 failure Root gate; canonical source/hash checks; all-target preflight and exclusive creation. No multi-file atomicity claim.'}}
    assets['LETTERING_PROVENANCE.json']=jb(report)
    return {**{OUT/k:v for k,v in assets.items()},**{PRIVATE/k:v for k,v in private.items()}},report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--verify-only',action='store_true'); mode.add_argument('--write',action='store_true')
    parser.add_argument('--source-photo'); parser.add_argument('--source-lettering')
    args=parser.parse_args(); targets=[OUT/n for n in PUBLIC]+[PRIVATE/n for n in PRIV]
    if args.write:
        assert not any(p.exists() for p in targets), 'OUTPUT_ALREADY_EXISTS'
        gate=root_gate()
    outputs,report=calculate(args.source_photo,args.source_lettering)
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
        OUT.mkdir(parents=True,exist_ok=True); PRIVATE.mkdir(parents=True,exist_ok=True)
        for path,raw in outputs.items():
            with path.open('xb') as file:
                file.write(raw)
        for path,raw in outputs.items():
            assert path.read_bytes()==raw, 'POST_WRITE_READBACK_MISMATCH:'+str(path)
        action='wrote-new'
    print(json.dumps({'mode':'verify-only' if args.verify_only else 'write','action':action,
        'writes':0 if args.verify_only else len(outputs),'paths':17,'nonempty_omission':0,
        'svg_chars':report['svg_character_length'],'bbox':report['actual_alpha_bbox_exclusive'],
        'affine':report['one_whole_sentence_affine'],'alpha_facts':report['alpha_facts'],
        'headline':report['outputs']['headline.svg'],'preview':report['private_outputs']['preview.png'],
        'provenance':ref(OUT/'LETTERING_PROVENANCE.json',outputs[OUT/'LETTERING_PROVENANCE.json']),
        **({'root_gate':gate} if args.write else {})},ensure_ascii=True))


if __name__=='__main__':
    main()
