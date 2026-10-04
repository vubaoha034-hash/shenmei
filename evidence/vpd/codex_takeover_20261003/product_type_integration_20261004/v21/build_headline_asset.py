"""V21: one compact two-line Source Han Serif artwork on the frozen tea photo.

The seven original compound glyph outlines and all counters are retained.
Only optical positions, one uniform 145-pixel em, and the line break change.
No font binary is rewritten/distributed; no imagegen or raster tracing is used.
--verify-only renders in memory and reads outputs without creating files.
--write requires Root's settled V20 failure gate and rejects existing outputs.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import io
import json
import math
import runpy
import subprocess
import sys
import xml.etree.ElementTree as ET

sys.dont_write_bytecode = True
from PIL import Image, ImageChops, ImageFilter
import PIL
sys.path.append('C:/Users/Administrator/AppData/Local/hermes/hermes-agent/venv/Lib/site-packages')
import fontTools
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.recordingPen import RecordingPen

ROOT = Path(__file__).resolve().parents[5]
FIXED_ROOT = Path('C:/Users/Administrator/OneDrive/文档/足球/shenmei-vpd-codex-20261003')
SERIES = ROOT / 'evidence/vpd/codex_takeover_20261003/product_type_integration_20261004'
OUT = Path(__file__).resolve().parent
PRIVATE = ROOT / '.liu-visual-private/correct_source_typography/v21'
RUNTIME = Path('C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies')
FONT_ROOT = ROOT / 'evidence/vpd/codex_takeover_20261003/skill_research/fonttools_bounded_probe_v1/upstream/adobe-fonts/source-han-serif'
NS = '{http://www.w3.org/2000/svg}'
ET.register_namespace('', NS[1:-1])
COPY = '一杯茶，慢下来'
SCALE = 0.145
BODY_ALLOWANCE = (832, 72, 1504, 624)
BRAND_ALLOWANCE = (64, 56, 504, 304)
BRAND_X, BRAND_Y, BRAND_WIDTH = 285, 198, 205
LAYOUT = [(990,477),(1140,477),(1290,477),(1450,477),
          (990,611),(1140,611),(1290,611)]
CID_ORDER = ['cid09511','cid20810','cid33872','cid58986','cid18201','cid09524','cid20797']
COMMAND_SHAS = [
    'b2985959007a2f3073bdc5268c195e2ce5aa8d3f455cf00945f4afdf5ba27c93',
    'cbce27f51d31118633ef69d7ed74bdabca85cf7b6db80171f4c37557df1b7480',
    'bc743f866d697009aa56d30072ba40123e4cc2c4bab419e0569aa6bf19dd4c86',
    'fa6e302bace4eb4dbc269335afc9223f9a5e57db18f60210cc2dc3a8b0143b91',
    'cd90114c7f62e012f0b76679018066c26b9546307692751ebe9033e689ec9ccb',
    'a6b94e99ab3cc21d35bf581fb3288a2fa598ffbeced0fbb537293a111a56f0d1',
    'd23fe1abd62bd02dde953399ce11b479d1a63c4063def8037d47af0a6dc9ff39']
INPUTS = {
    'photo': (ROOT / '.liu-visual-private/source_recovery_20261003/photography-local-reconstruction-final.png',
              '7fd7777fed21100cb6b47bc305701476054263565e73246ac469d065aa080618'),
    'brand': (SERIES / 'v19/brand.svg','dd8e9e899393dc36eb3f5b1652bdbb740787d41a108ea6aa1eae05cb1368b1ff'),
    'mask': (SERIES / 'v19/foreground-protection.svg','b567253a07b4689f2869b5013d07cb625705d09f4e525f64e6878ab6c8f482e4'),
    'font': (FONT_ROOT / 'OTF/SimplifiedChinese/SourceHanSerifSC-Regular.otf',
             '78aa7a328fd974df2d688c8a9fd74a33d8334dfa84ab24d9d11efb2ffc464117'),
    'font_license': (FONT_ROOT / 'LICENSE.txt','9ff5bb567e1b92c801fc1069e5fbf992ff8efccacb9db94e5959a5b3ba9bb903'),
    'renderer_helper': (SERIES / 'v18/build_headline_asset.py',
                       '24102f462f379255c29be0209cd63f91d3e862f80956a96b012471eccc18e8e5')}
PUBLIC = ['headline.svg','brand.svg','foreground-protection.svg','METHOD_SOURCES.json','MANIFEST.json']
PRIV = ['preview.png','headline-render.png']


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def jb(obj):
    return (json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode('utf-8')


def ref(path, raw):
    return {'path':path.relative_to(ROOT).as_posix(),'sha256':sha(raw),'bytes':len(raw)}


def png(im):
    b = io.BytesIO()
    im.save(b,format='PNG')
    return b.getvalue()


def count(im):
    return sum(im.histogram()[1:])


def mass(im):
    return sum(v*n for v,n in enumerate(im.histogram()))


def check_rect(box, allowance, name):
    assert box and all((box[0]>=allowance[0],box[1]>=allowance[1],
                        box[2]<=allowance[2],box[3]<=allowance[3])), name


def protected_rgb(diff, mask):
    for channel in diff.split():
        assert ImageChops.darker(channel,mask).getbbox() is None, 'PROTECTED_RGB_CHANGED'


def root_gate():
    raw = (ROOT / 'continuity/vpd/CURRENT_TASK_LOCK.json').read_bytes()
    lock = json.loads(raw)
    unit = lock['codex_takeover']['worker_continuation']
    last = unit['versions'][-1]
    assert (lock['revision']>=316 and unit['unit_id']=='CHAZUO_APPROVED_SOURCE_TYPOGRAPHY_20261003_R1'
            and unit['phase']=='REVISION_REQUIRED' and last['number']==20 and last['verdict']=='AI_FAIL'), 'ROOT_GO_GATE_NOT_SATISFIED'
    return {'revision':lock['revision'],'phase':unit['phase'],'last_version':last['number'],
            'verdict':last['verdict'],'lock_sha256':sha(raw)}


def read_inputs(photo_path=None):
    assert ROOT.resolve()==FIXED_ROOT.resolve(), 'ROOT_PATH_IDENTITY_MISMATCH'
    assert OUT.resolve()==(SERIES/'v21').resolve(), 'OUTPUT_PATH_IDENTITY_MISMATCH'
    if photo_path is not None:
        assert Path(photo_path).resolve()==INPUTS['photo'][0].resolve(), 'SOURCE_PHOTO_PATH_IDENTITY_MISMATCH'
    raw = {}
    for key,(path,expected) in INPUTS.items():
        raw[key] = path.read_bytes()
        assert sha(raw[key])==expected, 'FIXED_SOURCE_CHANGED:'+key
    return raw


def replay(record, pen):
    for operator, operands in record:
        getattr(pen,operator)(*operands)


def original_glyphs(font_raw):
    font = TTFont(io.BytesIO(font_raw),lazy=False)
    version = font['name'].getDebugName(5)
    assert version=='Version 2.003;hotconv 1.1.1;makeotfexe 2.6.0', 'FONT_VERSION_CHANGED'
    assert font['head'].unitsPerEm==1000, 'FONT_UNITS_CHANGED'
    gs, cmap = font.getGlyphSet(), font.getBestCmap()
    result = []
    for i,ch in enumerate(COPY):
        cid = cmap[ord(ch)]
        assert cid==CID_ORDER[i], 'FONT_CID_CHANGED'
        glyph = gs[cid]
        pen, bounds, recording = SVGPathPen(gs), BoundsPen(gs), RecordingPen()
        glyph.draw(pen); glyph.draw(bounds); glyph.draw(recording)
        d = pen.getCommands()
        assert sha(d.encode('utf-8'))==COMMAND_SHAS[i], 'SOURCE_GLYPH_COMMAND_CHANGED'
        contours, current = [], []
        for command in recording.value:
            current.append(command)
            if command[0] in ('closePath','endPath'):
                cp, bp = SVGPathPen(gs), BoundsPen(gs)
                replay(current,cp); replay(current,bp)
                contours.append({'index':len(contours),'source_d_sha256':sha(cp.getCommands().encode('utf-8')),
                                 'source_bounds':list(bp.bounds),'source_command_count':len(current),
                                 'outline_edit':'none; source coordinates retained verbatim'})
                current = []
        assert not current, 'UNCLOSED_SOURCE_CONTOUR'
        x,base = LAYOUT[i]
        b = bounds.bounds
        result.append({'character':ch,'unicode':f'U+{ord(ch):04X}','CID':cid,'d':d,
                       'source_d_sha256':sha(d.encode('utf-8')),'source_bounds':list(b),
                       'source_contours':contours,'group_id':f'glyph-{i+1}',
                       'uniform_scale':SCALE,'origin_x':x,'baseline_y':base,
                       'geometric_bounds':[x+b[0]*SCALE,base-b[3]*SCALE,
                                           x+b[2]*SCALE,base-b[1]*SCALE]})
    assert sum(len(r['source_contours']) for r in result)==26
    font.close()
    return result, version


def svg_asset(mask_raw, rows):
    root = ET.Element(NS+'svg',{'width':'1536','height':'1024','viewBox':'0 0 1536 1024','fill':'none'})
    ET.SubElement(root,NS+'title').text = COPY
    ET.SubElement(root,NS+'desc').text = ('V21 two-line artwork; Source Han Serif SC Regular 2.003 original compound outlines; '
        'SIL OFL 1.1; no modified font binary or native text supplied.')
    defs = ET.SubElement(root,NS+'defs')
    clip = ET.SubElement(defs,NS+'clipPath',{'id':'S-product-negative-space','clipPathUnits':'userSpaceOnUse'})
    mask_root = ET.fromstring(mask_raw)
    assert len(mask_root)==2 and all(n.tag==NS+'path' for n in mask_root)
    ET.SubElement(clip,NS+'path',{'d':'M0 0H1536V1024H0Z'+''.join(n.get('d') for n in mask_root),'clip-rule':'evenodd'})
    phrase = ET.SubElement(root,NS+'g',{'id':'V21-compact-two-line-phrase','clip-path':'url(#S-product-negative-space)'})
    for row in rows:
        g = ET.SubElement(phrase,NS+'g',{'id':row['group_id'],
            'transform':f"matrix({SCALE} 0 0 {-SCALE} {row['origin_x']} {row['baseline_y']})"})
        ET.SubElement(g,NS+'title').text = row['character']
        ET.SubElement(g,NS+'path',{'id':row['CID'],'d':row['d'],'fill':'#F5F2E6','fill-rule':'nonzero'})
    return root


def svg_bytes(root):
    return (ET.tostring(root,encoding='unicode')+'\n').encode('utf-8')


def one_glyph_svg(root, group_id, clipped):
    single = copy.deepcopy(root)
    phrase = single.find(NS+'g')
    for glyph in list(phrase):
        if glyph.get('id')!=group_id:
            phrase.remove(glyph)
    if not clipped:
        phrase.attrib.pop('clip-path')
    return svg_bytes(single)


def components(alpha, threshold=128):
    """Actual raster components: 8-neighbour connectivity at alpha >=128."""
    box = alpha.getbbox()
    if box is None:
        return {'threshold':threshold,'connectivity':8,'count':0,'sizes_descending':[]}
    image = alpha.crop(box)
    width,height = image.size
    pixels = bytearray(1 if p>=threshold else 0 for p in image.tobytes())
    sizes = []
    for index in range(len(pixels)):
        if not pixels[index]:
            continue
        pixels[index] = 0
        todo,size = [index],0
        while todo:
            cell = todo.pop(); size += 1
            x,y = cell%width,cell//width
            for dy in (-1,0,1):
                for dx in (-1,0,1):
                    if (dx or dy) and 0<=x+dx<width and 0<=y+dy<height:
                        neighbour = (y+dy)*width+x+dx
                        if pixels[neighbour]:
                            pixels[neighbour]=0; todo.append(neighbour)
        sizes.append(size)
    return {'threshold':threshold,'connectivity':8,'count':len(sizes),'sizes_descending':sorted(sizes,reverse=True)}


def alpha_report(before, after, mask_on):
    lower, higher = ImageChops.subtract(before,after),ImageChops.subtract(after,before)
    intersection = ImageChops.darker(before,mask_on)
    occluded = ImageChops.darker(lower,mask_on)
    cb,ca = components(before),components(after)
    return {'unclipped_alpha_bbox':list(before.getbbox()) if before.getbbox() else None,
            'clipped_alpha_bbox':list(after.getbbox()) if after.getbbox() else None,
            'unclipped_nonzero_pixels':count(before),'clipped_nonzero_pixels':count(after),
            'unclipped_alpha_mass':mass(before),'clipped_alpha_mass':mass(after),
            'source_alpha_intersection_with_full_mask_pixels':count(intersection),
            'true_product_occluded_alpha_pixels':count(occluded),
            'true_product_occluded_alpha_mass':mass(occluded),
            'all_rendered_alpha_lower_pixels':count(lower),'all_rendered_alpha_higher_pixels':count(higher),
            'all_lower_alpha_mass':mass(lower),'all_higher_alpha_mass':mass(higher),
            'components_before':cb,'components_after':ca,'components_equal':cb==ca}


def brand_canvas(brand_raw, render):
    source = ET.fromstring(brand_raw)
    assert len(list(source.iter(NS+'path')))==7, 'BRAND_PATH_COUNT_CHANGED'
    width,height = float(source.get('width')),float(source.get('height'))
    scale = BRAND_WIDTH/width
    canvas = ET.Element(NS+'svg',{'width':'1536','height':'1024','viewBox':'0 0 1536 1024'})
    group = ET.SubElement(canvas,NS+'g',{'transform':f'translate({BRAND_X} {BRAND_Y}) scale({scale})'})
    for child in source:
        group.append(copy.deepcopy(child))
    rgba = render(svg_bytes(canvas))
    box = rgba.getchannel('A').getbbox()
    check_rect(box,BRAND_ALLOWANCE,'BRAND_OUTSIDE_AUTHORISED_AREA')
    return rgba, {'x':BRAND_X,'y':BRAND_Y,'width':BRAND_WIDTH,'height':height*scale,
                  'scale':scale,'actual_alpha_bbox_exclusive':list(box),
                  'original_svg_bytes_preserved':True,'glyph_outline_edits':0}


def calculate(photo_path=None):
    raw = read_inputs(photo_path)
    assert fontTools.__version__=='4.63.0' and PIL.__version__=='12.3.0' and sys.version_info[:3]==(3,12,14), 'RUNTIME_VERSION_CHANGED'
    helper = runpy.run_path(str(INPUTS['renderer_helper'][0]))
    render = helper['render']
    node_code = 'const s=require('+json.dumps((RUNTIME/'node/node_modules/sharp').as_posix())+');process.stdout.write(JSON.stringify({node:process.version,sharp:s.versions.sharp,rsvg:s.versions.rsvg}));'
    runtime = json.loads(subprocess.run([str(RUNTIME/'node/bin/node.exe'),'-e',node_code],capture_output=True,check=True).stdout)
    assert runtime=={'node':'v24.19.0','sharp':'0.35.4','rsvg':'2.62.91'}, 'RENDERER_VERSION_CHANGED'
    rows,version = original_glyphs(raw['font'])
    root = svg_asset(raw['mask'],rows)
    headline = svg_bytes(root)
    assert len(headline.decode('utf-8'))<=45000
    mask = render(raw['mask']).getchannel('A')
    mask_on = mask.point(lambda v:255 if v else 0)
    core = mask.filter(ImageFilter.MinFilter(7)).point(lambda v:255 if v==255 else 0)
    assert count(core)==162052, 'FIXED_CORE_CHANGED'
    # Per-glyph alpha loss and connectivity are measured before creating preview bytes.
    for row in rows:
        before = render(one_glyph_svg(root,row['group_id'],False)).getchannel('A')
        after = render(one_glyph_svg(root,row['group_id'],True)).getchannel('A')
        row['actual_mask_and_alpha'] = alpha_report(before,after,mask_on)
        assert row['actual_mask_and_alpha']['components_equal'], 'GLYPH_CONNECTIVITY_CHANGED:'+row['CID']
        assert row['actual_mask_and_alpha']['true_product_occluded_alpha_pixels']==0, 'SOURCE_STRUCTURE_CLIPPED:'+row['CID']
        row.pop('d')
    rgba = render(headline)
    alpha = rgba.getchannel('A')
    bbox = alpha.getbbox()
    check_rect(bbox,BODY_ALLOWANCE,'HEADLINE_OUTSIDE_AUTHORISED_AREA')
    unclip = copy.deepcopy(root)
    unclip.find(NS+'g').attrib.pop('clip-path')
    whole_before = render(svg_bytes(unclip)).getchannel('A')
    whole_alpha = alpha_report(whole_before,alpha,mask_on)
    assert ImageChops.darker(alpha,mask_on).getbbox() is None, 'VISIBLE_ALPHA_INTERSECTS_FIXED_MASK'
    brand,brand_metrics = brand_canvas(raw['brand'],render)
    assert ImageChops.darker(brand.getchannel('A'),mask_on).getbbox() is None
    photo = Image.open(io.BytesIO(raw['photo'])).convert('RGBA')
    assert photo.size==rgba.size==brand.size==(1536,1024)
    preview = photo.copy()
    preview.alpha_composite(brand)
    preview.alpha_composite(rgba)
    diff = ImageChops.difference(preview.convert('RGB'),photo.convert('RGB'))
    protected_rgb(diff,core); protected_rgb(diff,mask_on)
    # Tight visible boxes, each wholly contained in an existing authorised field.
    body_box = tuple(bbox)
    brand_box = tuple(brand_metrics['actual_alpha_bbox_exclusive'])
    outside = Image.new('L',(1536,1024),255)
    for box in (brand_box,body_box):
        outside.paste(0,box)
    protected_rgb(diff,outside)
    methods = {'schema':'v21-bounded-type-source-method/v1','sources':[
        {'url':'https://github.com/adobe-fonts/source-han-serif/tree/7889f11bf31170b5d092a083b357c8c8130f89e0',
         'read':'Official fixed-commit README body plus local full LICENSE.txt and actual OTF name/CID/contour data; no linked PDF claimed read.',
         'applied':'Mature original SC compound glyph outlines, counters and stroke contrast as the one lettering foundation.',
         'boundary':'Original sharp Song terminals retained; no claim that this is the reference handwritten font.'},
        {'url':'https://blog.justfont.com/2015/08/introducing-jinshuan/',
         'read':'Previously read article body on skeleton, counters, gravity and terminals; reused reading, no new source collection.',
         'applied':'Preserve a coherent character system rather than separately inventing each single-line glyph.',
         'boundary':'No proprietary Jinxuan glyph data loaded or copied.'}],
        'reference_pixel_scope':'R upper advertising image only; no lower wall mockup used.',
        'layout_inference':'Compact two-line sentence right of cup and above tray; product protection is not aesthetic certification.'}
    method_raw = jb(methods)
    assert len(method_raw)<=3072
    assets = {'headline.svg':headline,'brand.svg':raw['brand'],'foreground-protection.svg':raw['mask'],
              'METHOD_SOURCES.json':method_raw}
    private = {'preview.png':png(preview),'headline-render.png':png(rgba)}
    report = {'schema':'vpd-v21-source-han-compact-two-line-artwork/v1','asset_number':21,
        'brand':'茶作','copy':COPY,'line_break':['一杯茶，','慢下来'],'viewport':[1536,1024],
        'source_inputs':{k:ref(INPUTS[k][0],v) for k,v in raw.items()},
        'source_font':{'family':'Source Han Serif SC','style':'Regular','version':version,'units_per_em':1000,
            'official_commit':'7889f11bf31170b5d092a083b357c8c8130f89e0','license':'SIL OFL 1.1',
            'reserved_font_name':'Source','copyright':'Copyright 2017-2022 Adobe',
            'font_binary_modified_or_distributed':False,'license_reference':ref(INPUTS['font_license'][0],raw['font_license'])},
        'glyphs':rows,'source_contour_count':26,'compound_glyph_path_count':7,
        'contour_modifications':[],
        'actual_design_changes':[
            'Replace V20 authored monoline lettering with one mature original SC glyph system; no old headline d strings used.',
            'Break only after existing comma; two optical rows share a 150-pixel character-origin rhythm.',
            'Use one uniform 145-pixel em; baselines 477 and 611; comma hangs at the top line end.',
            'Keep every source outline coordinate and internal contour; no custom stroke warping or artificial cup contour.',
            'Move and uniformly scale frozen brand only for private preview, using Root placement x285/y198/width205.'],
        'layout_rationale':'One compact reading mass in the frozen right product field. Lower-row left whitespace faces the leaf tip; full source contours take priority over forcing overlap.',
        'authorised_body_rectangle':list(BODY_ALLOWANCE),'authorised_brand_rectangle':list(BRAND_ALLOWANCE),
        'actual_alpha_bbox_exclusive':list(bbox),'visible_design_overlay_envelopes':[list(brand_box),list(body_box)],
        'brand_placement':brand_metrics,'whole_headline_mask_and_alpha':whole_alpha,
        'fixed_product_mask_nonzero_pixels':count(mask_on),'fixed_product_core_pixels':count(core),
        'product_core_RGB_differences':0,'full_fixed_mask_RGB_differences':0,
        'protected_outside_overlay_pixels':count(outside),'protected_outside_overlay_RGB_differences':0,
        'svg_character_length':len(headline.decode('utf-8')),'font_outline_serialisation':'Original SVGPathPen command strings retained verbatim; one uniform transform per glyph.',
        'software':{'Python':sys.version,'Pillow':PIL.__version__,'FontTools':fontTools.__version__,**runtime,
            'FontTools_source_manifest_commit':'978d9edccb60ea0e5fbad7015cb11817c3532328',
            'FontTools_license':'MIT; existing project source manifest retains external notices',
            'fonttools_operation':'TTFont read-only parsing and pens only; no TTFont.save or font rewrite',
            'renderer':'Fixed existing V18 Sharp/librsvg helper; unchanged'},
        'new_imagegen_operations':0,'raster_trace_operations':0,'photo_generations_or_edits':0,
        'formal_poster_versions_by_worker':0,'private_fullpreview_outputs':1,
        'business_state_writes_by_worker':0,'Figma_Drive_Git_writes_by_worker':0,
        'native_TEXT_claimed':False,'editability':'7 compound filled glyph paths with 26 source subcontours in 7 editable SVG groups; fixed clip path.',
        'aesthetic_pass_claimed':False,'formal_independent_review':None,'human_approval_claimed':False,
        'outputs':{k:ref(OUT/k,v) for k,v in assets.items()},
        'private_outputs':{k:ref(PRIVATE/k,v) for k,v in private.items()},
        'builder':ref(Path(__file__),Path(__file__).read_bytes()),
        'builder_modes':{'verify_only':'In-memory render and optional exact readback; no mkdir, save or write.',
            'write':'Settled V20 failure Root gate, source identity/hash checks, all-target preflight and exclusive creation; no multi-file atomicity claim.'}}
    assets['MANIFEST.json'] = jb(report)
    return {**{OUT/k:v for k,v in assets.items()},**{PRIVATE/k:v for k,v in private.items()}},report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--verify-only',action='store_true')
    modes.add_argument('--write',action='store_true')
    parser.add_argument('--source-photo',help='Only the canonical frozen source path is accepted.')
    args = parser.parse_args()
    targets = [OUT/n for n in PUBLIC]+[PRIVATE/n for n in PRIV]
    if args.write:
        assert not any(p.exists() for p in targets), 'OUTPUT_ALREADY_EXISTS'
        gate = root_gate()
    outputs,report = calculate(args.source_photo)
    assert set(outputs)==set(targets)
    if args.verify_only:
        existing = [p for p in targets if p.exists()]
        if existing:
            assert len(existing)==len(targets), 'PARTIAL_OUTPUTS_PRESENT'
            for path,raw in outputs.items():
                assert path.read_bytes()==raw, 'OUTPUT_READBACK_MISMATCH:'+str(path)
        action = 'verified-existing' if existing else 'verified-before-write'
    else:
        assert not any(p.exists() for p in targets), 'OUTPUT_ALREADY_EXISTS'
        OUT.mkdir(parents=True,exist_ok=True)
        PRIVATE.mkdir(parents=True,exist_ok=True)
        for path,raw in outputs.items():
            with path.open('xb') as file:
                file.write(raw)
        for path,raw in outputs.items():
            assert path.read_bytes()==raw, 'POST_WRITE_READBACK_MISMATCH:'+str(path)
        action = 'wrote-new'
    print(json.dumps({'mode':'verify-only' if args.verify_only else 'write','action':action,
        'writes':0 if args.verify_only else len(outputs),'svg_chars':report['svg_character_length'],
        'compound_paths':7,'source_contours':26,'bbox':report['actual_alpha_bbox_exclusive'],
        'core_pixels':162052,'core_RGB_differences':0,'full_mask_RGB_differences':0,'outside_RGB_differences':0,
        'glyph_mask_loss':[{'cid':r['CID'],'pixels':r['actual_mask_and_alpha']['true_product_occluded_alpha_pixels'],
                            'components_equal':r['actual_mask_and_alpha']['components_equal']} for r in report['glyphs']],
        'headline':report['outputs']['headline.svg'],'preview':report['private_outputs']['preview.png'],
        'manifest':ref(OUT/'MANIFEST.json',outputs[OUT/'MANIFEST.json']),
        **({'root_gate':gate} if args.write else {})},ensure_ascii=True))


if __name__=='__main__':
    main()
