"""V20: one authored thin-stroke Hanzi reading band above the frozen product.

Original cubic stroke boundaries, not a font or a raster trace. No candidate grid.
--verify-only computes in memory and optionally reads exact existing outputs.
--write requires Root's settled V19 gate and exclusively creates all outputs.
No business state, photography, Figma, Drive, or Git is written by this builder.
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

ROOT = Path(__file__).resolve().parents[5]
FIXED_ROOT = Path('C:/Users/Administrator/OneDrive/文档/足球/shenmei-vpd-codex-20261003')
OUT = Path(__file__).resolve().parent
PRIVATE = ROOT / '.liu-visual-private/correct_source_typography/v20'
SERIES = ROOT / 'evidence/vpd/codex_takeover_20261003/product_type_integration_20261004'
RUNTIME = Path('C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies')
NS = '{http://www.w3.org/2000/svg}'
ET.register_namespace('', NS[1:-1])
COPY = '一杯茶，慢下来'
BRAND_BOX = (104, 96, 400, 256)
ALLOWANCE = (288, 400, 1328, 720)
INPUTS = {
    'photo': (ROOT / '.liu-visual-private/source_recovery_20261003/photography-local-reconstruction-final.png',
              '7fd7777fed21100cb6b47bc305701476054263565e73246ac469d065aa080618'),
    'poster19': (ROOT / '.liu-visual-private/correct_source_typography/v19/poster.png',
                 'bbb830cca9110e0cad256bdf996da4276aa04e15c59b80ab6976d15eaa7dc26f'),
    'brand': (SERIES / 'v19/brand.svg', 'dd8e9e899393dc36eb3f5b1652bdbb740787d41a108ea6aa1eae05cb1368b1ff'),
    'mask': (SERIES / 'v19/foreground-protection.svg',
             'b567253a07b4689f2869b5013d07cb625705d09f4e525f64e6878ab6c8f482e4'),
    'renderer_helper': (SERIES / 'v18/build_headline_asset.py',
                        '24102f462f379255c29be0209cd63f91d3e862f80956a96b012471eccc18e8e5'),
}
PUBLIC = ['headline.svg', 'brand.svg', 'foreground-protection.svg', 'METHOD_SOURCES.json', 'MANIFEST.json']
PRIV = ['preview.png', 'headline-render.png']


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def jb(obj):
    return (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def ref(path, raw):
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': sha(raw), 'bytes': len(raw)}


def png(im):
    b = io.BytesIO()
    im.save(b, format='PNG')
    return b.getvalue()


def count(im):
    return sum(im.histogram()[1:])


def protected_rgb(diff, mask):
    for channel in diff.split():
        assert ImageChops.darker(channel, mask).getbbox() is None, 'PROTECTED_RGB_CHANGED'


def root_gate():
    raw = (ROOT / 'continuity/vpd/CURRENT_TASK_LOCK.json').read_bytes()
    lock = json.loads(raw)
    w = lock['codex_takeover']['worker_continuation']
    v = w['versions'][-1]
    assert (lock['revision'] >= 314 and w['unit_id'] == 'CHAZUO_APPROVED_SOURCE_TYPOGRAPHY_20261003_R1'
            and w['phase'] == 'REVISION_REQUIRED' and v['number'] == 19 and v['verdict'] == 'AI_FAIL'), 'ROOT_GO_GATE_NOT_SATISFIED'
    return {'revision': lock['revision'], 'phase': w['phase'], 'last_version': v['number'],
            'verdict': v['verdict'], 'lock_sha256': sha(raw)}


def read_inputs(photo_path=None):
    assert ROOT.resolve() == FIXED_ROOT.resolve(), 'ROOT_PATH_IDENTITY_MISMATCH'
    assert OUT.resolve() == (SERIES / 'v20').resolve(), 'OUTPUT_PATH_IDENTITY_MISMATCH'
    if photo_path is not None:
        assert Path(photo_path).resolve() == INPUTS['photo'][0].resolve(), 'SOURCE_PHOTO_PATH_IDENTITY_MISMATCH'
    raw = {}
    for key, (path, expected) in INPUTS.items():
        raw[key] = path.read_bytes()
        assert sha(raw[key]) == expected, 'FIXED_SOURCE_CHANGED:' + key
    return raw


def line(a, b):
    return (a, (a[0] + (b[0] - a[0]) / 3, a[1] + (b[1] - a[1]) / 3),
            (a[0] + 2 * (b[0] - a[0]) / 3, a[1] + 2 * (b[1] - a[1]) / 3), b)


def tangent(p, t):
    u = 1 - t
    x = 3 * (u*u*(p[1][0]-p[0][0]) + 2*u*t*(p[2][0]-p[1][0]) + t*t*(p[3][0]-p[2][0]))
    y = 3 * (u*u*(p[1][1]-p[0][1]) + 2*u*t*(p[2][1]-p[1][1]) + t*t*(p[3][1]-p[2][1]))
    length = math.hypot(x, y)
    assert length > 0
    return x / length, y / length


def stroke_boundary(p, width, origin):
    """Author a pair of cubic boundaries and two blunt curved end caps.

    The boundary construction is an intentional stroke model. It is not a
    mathematically exact offset of the center curve or a reproduced font path.
    All final SVG coordinates are absolute; no affine modifies old lettering.
    """
    left, right = [], []
    for i, ratio in enumerate((0.76, 1.06, 1.02, 0.72)):
        tx, ty = tangent(p, i / 3)
        nx, ny = -ty, tx
        half = width * ratio / 2
        x, y = p[i][0] + origin[0], p[i][1] + origin[1]
        left.append((x + nx*half, y + ny*half))
        right.append((x - nx*half, y - ny*half))
    start_t, end_t = tangent(p, 0), tangent(p, 1)
    end_cap = width * 0.72 / 2 * 4 / 3
    start_cap = width * 0.76 / 2 * 4 / 3
    ec1 = (left[3][0] + end_t[0]*end_cap, left[3][1] + end_t[1]*end_cap)
    ec2 = (right[3][0] + end_t[0]*end_cap, right[3][1] + end_t[1]*end_cap)
    sc1 = (right[0][0] - start_t[0]*start_cap, right[0][1] - start_t[1]*start_cap)
    sc2 = (left[0][0] - start_t[0]*start_cap, left[0][1] - start_t[1]*start_cap)
    def xy(q):
        return f'{q[0]:.3f} {q[1]:.3f}'
    return (f'M{xy(left[0])}C{xy(left[1])} {xy(left[2])} {xy(left[3])}'
            f'C{xy(ec1)} {xy(ec2)} {xy(right[3])}'
            f'C{xy(right[2])} {xy(right[1])} {xy(right[0])}'
            f'C{xy(sc1)} {xy(sc2)} {xy(left[0])}Z')


def authored_glyphs():
    """The sole V20 layout, with individually authored everyday-handwriting strokes.

    Cup-side glyphs open horizontally; the right phrase opens above the leaf
    and tray. The restrained valley at 下 leaves room above the fresh-leaf tip.
    These are new Hanzi structures, with no previous glyph d strings loaded.
    """
    def c(a, b, cc, d, w):
        return ((a, b, cc, d), w)
    def l(a, b, w):
        return (line(a, b), w)
    return [
        ('一', (350, 443), [c((1,59),(34,61),(75,54),(109,55),7.4)]),
        ('杯', (477, 438), [
            c((3,31),(17,30),(29,29),(42,30),6.6),
            c((23,3),(22,32),(23,69),(22,100),7.1),
            c((21,34),(18,49),(11,64),(3,76),6.4),
            c((24,45),(29,48),(35,57),(39,65),6.0),
            c((47,9),(65,8),(83,7),(101,9),6.7),
            c((81,10),(76,26),(67,43),(49,58),6.7),
            c((76,33),(74,50),(75,77),(74,99),7.0),
            c((82,43),(91,49),(96,56),(102,68),6.3)]),
        ('茶', (603, 453), [
            c((3,15),(37,14),(69,13),(105,14),6.7),
            c((30,2),(30,10),(29,21),(28,28),6.4),
            c((76,2),(76,10),(76,20),(75,28),6.4),
            c((53,30),(43,40),(26,49),(7,56),6.8),
            c((55,31),(68,43),(86,49),(106,56),6.8),
            c((20,65),(42,64),(64,64),(88,65),6.5),
            c((53,52),(52,67),(53,86),(52,100),7.0),
            c((49,70),(39,80),(25,88),(14,93),6.6),
            c((57,71),(69,81),(82,89),(97,94),6.6)]),
        ('，', (743, 544), [c((3,-2),(8,2),(7,11),(0,16),6.4)]),
        ('慢', (787, 474), [
            c((5,31),(5,37),(4,43),(2,48),5.9),
            c((27,27),(29,31),(30,35),(32,40),5.6),
            c((18,3),(17,32),(18,68),(17,100),6.7),
            c((47,3),(46,12),(46,23),(46,32),5.6),
            c((48,3),(62,2),(81,2),(95,3),5.8),
            c((95,5),(95,13),(94,23),(94,32),5.6),
            c((48,17),(63,16),(79,16),(92,17),5.5),
            c((47,32),(64,32),(82,31),(94,32),5.8),
            c((39,43),(38,50),(38,59),(38,65),5.6),
            c((41,42),(62,42),(84,41),(107,42),5.9),
            c((107,44),(107,51),(106,58),(106,64),5.6),
            c((40,65),(61,65),(85,64),(105,65),5.9),
            c((61,45),(61,51),(61,57),(60,62),5.4),
            c((84,45),(83,51),(84,57),(83,62),5.4),
            c((42,77),(56,77),(77,76),(101,77),6.0),
            c((100,79),(91,92),(69,99),(42,102),6.4),
            c((43,82),(58,92),(84,101),(111,102),6.5)]),
        ('下', (926, 471), [
            c((2,8),(33,7),(66,6),(107,8),7.0),
            c((49,11),(48,38),(49,74),(49,100),7.2),
            c((65,35),(75,39),(88,45),(99,53),6.6)]),
        ('来', (1061, 496), [
            c((3,11),(34,10),(71,9),(111,10),6.6),
            c((24,24),(28,29),(31,35),(33,41),6.2),
            c((89,22),(85,29),(81,36),(76,42),6.2),
            c((10,48),(37,47),(72,47),(103,48),6.8),
            c((56,2),(55,33),(56,69),(55,103),7.2),
            c((51,56),(40,74),(23,88),(6,98),6.9),
            c((61,58),(73,74),(90,89),(111,98),6.9)]),
    ]


def svg_asset(mask_raw):
    root = ET.Element(NS+'svg', {'width':'1536','height':'1024','viewBox':'0 0 1536 1024','fill':'none'})
    ET.SubElement(root, NS+'title').text = COPY
    ET.SubElement(root, NS+'desc').text = 'V20 original authored cubic outlines; font files loaded: 0; native text: 0.'
    defs = ET.SubElement(root, NS+'defs')
    clip = ET.SubElement(defs, NS+'clipPath', {'id':'S-product-negative-space','clipPathUnits':'userSpaceOnUse'})
    mask_root = ET.fromstring(mask_raw)
    assert len(mask_root) == 2 and all(n.tag == NS+'path' for n in mask_root)
    combined = 'M0 0H1536V1024H0Z'+''.join(n.get('d') for n in mask_root)
    ET.SubElement(clip, NS+'path', {'d':combined,'clip-rule':'evenodd'})
    phrase = ET.SubElement(root, NS+'g', {'id':'V20-authored-reading-band','clip-path':'url(#S-product-negative-space)'})
    metrics = []
    for i, (char, origin, strokes) in enumerate(authored_glyphs(), 1):
        group = ET.SubElement(phrase, NS+'g', {'id':f'glyph-{i}'})
        ET.SubElement(group, NS+'title').text = char
        for j, (curve, width) in enumerate(strokes, 1):
            ET.SubElement(group, NS+'path', {'id':f'glyph-{i}-stroke-{j}',
                'd':stroke_boundary(curve,width,origin),'fill':'#F5F2E6'})
        metrics.append({'character':char,'group_id':f'glyph-{i}','origin':list(origin),
                        'authored_strokes':len(strokes),'stroke_widths':[w for _,w in strokes]})
    return root, metrics


def calculate(photo_path=None):
    raw = read_inputs(photo_path)
    assert PIL.__version__ == '12.3.0' and sys.version_info[:3] == (3,12,14), 'RUNTIME_VERSION_CHANGED'
    helper = runpy.run_path(str(INPUTS['renderer_helper'][0]))
    render = helper['render']
    node_code = 'const s=require('+json.dumps((RUNTIME/'node/node_modules/sharp').as_posix())+');process.stdout.write(JSON.stringify({node:process.version,sharp:s.versions.sharp,rsvg:s.versions.rsvg}));'
    runtime = json.loads(subprocess.run([str(RUNTIME/'node/bin/node.exe'),'-e',node_code],capture_output=True,check=True).stdout)
    assert runtime == {'node':'v24.19.0','sharp':'0.35.4','rsvg':'2.62.91'}, 'RENDERER_VERSION_CHANGED'
    root, glyph_metrics = svg_asset(raw['mask'])
    headline = (ET.tostring(root,encoding='unicode')+'\n').encode('utf-8')
    assert len(headline.decode('utf-8')) <= 45000
    rgba = render(headline)
    unclip = copy.deepcopy(root)
    unclip.find(NS+'g').attrib.pop('clip-path')
    unclipped = render(ET.tostring(unclip)).getchannel('A')
    alpha = rgba.getchannel('A')
    bbox = alpha.getbbox()
    assert bbox and bbox[0]>=ALLOWANCE[0] and bbox[1]>=ALLOWANCE[1] and bbox[2]<=ALLOWANCE[2] and bbox[3]<=ALLOWANCE[3], 'HEADLINE_OUTSIDE_AUTHORISED_AREA'
    mask = render(raw['mask']).getchannel('A')
    mask_on = mask.point(lambda v:255 if v else 0)
    core = mask.filter(ImageFilter.MinFilter(7)).point(lambda v:255 if v == 255 else 0)
    assert count(core) == 162052, 'FIXED_CORE_CHANGED'
    assert ImageChops.darker(unclipped,mask_on).getbbox() is None, 'AUTHORED_STRUCTURE_REQUIRES_PRODUCT_TRUNCATION'
    assert ImageChops.darker(alpha,mask_on).getbbox() is None, 'VISIBLE_LETTERING_INTERSECTS_FIXED_MASK'
    lower = ImageChops.subtract(unclipped,alpha)
    higher = ImageChops.subtract(alpha,unclipped)
    assert ImageChops.darker(lower,mask_on).getbbox() is None, 'PRODUCT_CLIP_REMOVES_LETTER_STRUCTURE'
    # These per-character bounds come from the actual whole rendered alpha.
    for row in glyph_metrics:
        x,y = row['origin']
        box = ((x-8,y-8,x+16,y+23) if row['character']=='，' else
               (max(0,x-6),max(0,y-8),min(1536,x+122),min(1024,y+110)))
        cb = alpha.crop(box).getbbox()
        assert cb is not None, 'EMPTY_GLYPH:'+row['character']
        row['whole_alpha_window'] = list(box)
        row['whole_alpha_window_bbox'] = [cb[0]+box[0],cb[1]+box[1],cb[2]+box[0],cb[3]+box[1]]
        row['window_can_include_neighbour_antialias'] = False
    photo = Image.open(io.BytesIO(raw['photo'])).convert('RGBA')
    poster19 = Image.open(io.BytesIO(raw['poster19'])).convert('RGBA')
    assert photo.size == poster19.size == rgba.size == (1536,1024)
    preview = photo.copy()
    preview.paste(poster19.crop(BRAND_BOX),BRAND_BOX[:2])
    preview.alpha_composite(rgba)
    diff = ImageChops.difference(preview.convert('RGB'),photo.convert('RGB'))
    protected_rgb(diff,core)
    protected_rgb(diff,mask_on)
    headline_box = (bbox[0]-3,bbox[1]-3,bbox[2]+3,bbox[3]+3)
    protected = Image.new('L',(1536,1024),255)
    for box in (BRAND_BOX,headline_box):
        protected.paste(0,box)
    protected_rgb(diff,protected)
    assert ImageChops.difference(preview.crop(BRAND_BOX),poster19.crop(BRAND_BOX)).getbbox(alpha_only=False) is None, 'BRAND_PIXELS_CHANGED'
    methods = {'schema':'v20-bounded-primary-method-reading/v1',
      'sources':[
        {'url':'https://blog.justfont.com/2015/08/introducing-jinshuan/',
         'read':'Article body, especially skeleton and stroke design paragraphs; no video claimed watched.',
         'applied':'Treat skeleton, counters, centre of gravity and terminals as one glyph system.',
         'not_imported':'No Jinxuan font, proprietary glyph outlines or article images copied.'},
        {'url':'https://www.adobe.com/creativecloud/photography/type/negative-space-photography.html',
         'read':'Article body on subject-surrounding relationships, varied negative spaces and breathing room.',
         'applied':'Use the frozen cup/leaf/tray surroundings as the headline reading space.',
         'boundary':'The new layout is the maker\'s inference, not an aesthetic outcome certified by this source.'}],
      'reference_pixel_scope':'R top 1080x720 advertising area only; lower wall mockup excluded.',
      'new_style_or_skill_promotion':False}
    method_raw = jb(methods)
    assert len(method_raw) <= 3072
    assets = {'headline.svg':headline,'brand.svg':raw['brand'],'foreground-protection.svg':raw['mask'],
              'METHOD_SOURCES.json':method_raw}
    private = {'preview.png':png(preview),'headline-render.png':png(rgba)}
    report = {'schema':'vpd-v20-authored-cubic-reading-band/v1','asset_number':20,'brand':'茶作','copy':COPY,
       'viewport':[1536,1024],
       'method':'One new authored thin-stroke sentence: cup-side shallow lower contour, open counters over leaf, last glyph over tray.',
       'lettering_source':'Original worker-authored Hanzi strokes and cubic boundaries; no commercial/reference/previous glyph paths loaded.',
       'font_files_loaded':0,'font_licence_required_by_this_asset':False,
       'path_licence':'Original authored artwork; no third-party typeface outlines embedded.',
       'boundary_model':'Paired cubic boundaries and blunt cubic end caps; not an exact mathematical centerline offset.',
       'source_inputs':{k:ref(INPUTS[k][0],v) for k,v in raw.items()},
       'glyphs':glyph_metrics,'path_count':sum(r['authored_strokes'] for r in glyph_metrics),
       'svg_character_length':len(headline.decode('utf-8')),'coordinate_serialisation_decimals':3,
       'authorised_headline_rectangle':list(ALLOWANCE),'actual_alpha_bbox_exclusive':list(bbox),
       'visible_design_overlay_envelopes':[list(BRAND_BOX),list(headline_box)],
       'fixed_product_mask_nonzero_pixels':count(mask_on),'fixed_product_core_pixels':count(core),
       'product_core_RGB_differences':0,'full_fixed_mask_RGB_differences':0,
       'protected_outside_overlay_pixels':count(protected),'protected_outside_overlay_RGB_differences':0,
       'brand_V19_RGB_differences':0,'brand_placement_preserved':{'x':112,'y':104,'width':275},
       'unclipped_alpha_product_mask_intersection_pixels':0,'true_product_occluded_alpha_pixels':0,
       'clipped_vs_unclipped_renderer_alpha':{'lower_pixels':count(lower),'higher_pixels':count(higher),
              'lower_max':lower.getextrema()[1],'higher_max':higher.getextrema()[1],
              'boundary':'Any listed differences are outside the fixed product mask; not product occlusion.'},
       'software':{'Python':sys.version,'Pillow':PIL.__version__,**runtime,
           'renderer':'Reuse fixed V18 bundled Sharp/librsvg render helper; upstream unchanged.'},
       'new_imagegen_operations':0,'raster_trace_operations':0,'photo_generations_or_edits':0,
       'formal_poster_versions_by_worker':0,'private_preview_outputs':1,
       'business_state_writes_by_worker':0,'Figma_Drive_Git_writes_by_worker':0,
       'native_TEXT_claimed':False,'editability':f"{sum(r['authored_strokes'] for r in glyph_metrics)} individually editable filled SVG stroke paths in 7 Hanzi/punctuation groups.",
       'aesthetic_pass_claimed':False,'formal_independent_review':None,'human_approval_claimed':False,
       'outputs':{k:ref(OUT/k,v) for k,v in assets.items()},
       'private_outputs':{k:ref(PRIVATE/k,v) for k,v in private.items()},
       'builder':ref(Path(__file__),Path(__file__).read_bytes()),
       'builder_modes':{'verify_only':'In-memory render and optional exact readback; no mkdir/save/write.',
                        'write':'Settled-V19 Root gate, all-target preflight and exclusive creation; multi-file atomicity not claimed.'}}
    assets['MANIFEST.json'] = jb(report)
    return {**{OUT/k:v for k,v in assets.items()},**{PRIVATE/k:v for k,v in private.items()}},report


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    modes = ap.add_mutually_exclusive_group(required=True)
    modes.add_argument('--verify-only',action='store_true')
    modes.add_argument('--write',action='store_true')
    ap.add_argument('--source-photo',help='Optional source identity check; only the frozen canonical path is accepted.')
    args = ap.parse_args()
    targets = [OUT/n for n in PUBLIC]+[PRIVATE/n for n in PRIV]
    if args.write:
        assert not any(p.exists() for p in targets), 'OUTPUT_ALREADY_EXISTS'
        gate = root_gate()
    outputs,report = calculate(args.source_photo)
    assert set(outputs) == set(targets)
    if args.verify_only:
        existing = [p for p in targets if p.exists()]
        if existing:
            assert len(existing) == len(targets), 'PARTIAL_OUTPUTS_PRESENT'
            for p,raw in outputs.items():
                assert p.read_bytes() == raw, 'OUTPUT_READBACK_MISMATCH:'+str(p)
        action = 'verified-existing' if existing else 'verified-before-write'
    else:
        assert not any(p.exists() for p in targets), 'OUTPUT_ALREADY_EXISTS'
        OUT.mkdir(parents=True,exist_ok=True)
        PRIVATE.mkdir(parents=True,exist_ok=True)
        for p,raw in outputs.items():
            with p.open('xb') as f:
                f.write(raw)
        for p,raw in outputs.items():
            assert p.read_bytes() == raw, 'POST_WRITE_READBACK_MISMATCH:'+str(p)
        action = 'wrote-new'
    print(json.dumps({'mode':'verify-only' if args.verify_only else 'write','action':action,
         'writes':0 if args.verify_only else len(outputs),'paths':report['path_count'],
         'svg_chars':report['svg_character_length'],'bbox':report['actual_alpha_bbox_exclusive'],
         'core_pixels':162052,'core_RGB_differences':0,'fixed_mask_RGB_differences':0,
         'protected_outside_RGB_differences':0,'true_product_occluded_alpha_pixels':0,
         'headline':report['outputs']['headline.svg'],'preview':report['private_outputs']['preview.png'],
         'manifest':ref(OUT/'MANIFEST.json',outputs[OUT/'MANIFEST.json']),
         **({'root_gate':gate} if args.write else {})},ensure_ascii=False))


if __name__ == '__main__':
    main()
