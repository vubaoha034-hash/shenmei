"""Construct the single V16 cup / leaf / tray lettering asset.

Creation is exclusive and fixed-source guarded. --verify-only constructs and
compares every production byte in memory, writes nothing, and does not create
directories. The source override flags exist to exercise refusal checks.
Run with the bundled Python and -B; no fonts or generation models are loaded.
"""
from pathlib import Path
import argparse, copy, hashlib, io, json, os, re, subprocess, sys
import xml.etree.ElementTree as ET
from PIL import Image, ImageChops, ImageFilter
import PIL

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[4]
PREVIEW = ROOT / '.liu-visual-private/correct_source_typography/v16/preview.png'
RUNTIME = Path('C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies')
SITE = Path('C:/Users/Administrator/AppData/Local/hermes/hermes-agent/venv/Lib/site-packages')
NS = '{http://www.w3.org/2000/svg}'
ET.register_namespace('', NS[1:-1])
COPY = '一杯茶，慢下来'
COLOR = '#F5F2E6'
FIXED = {
    'headline': ('evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v15/headline.svg', '99ab0d29a19f1f95dd29db2c87e37219f2727c5583475ab3c82aec50aacea37a'),
    'brand': ('evidence/vpd/codex_takeover_20261003/continuous_typography_20261004/v9/brand.svg', 'dd8e9e899393dc36eb3f5b1652bdbb740787d41a108ea6aa1eae05cb1368b1ff'),
    'mask': ('evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v14/foreground-protection.svg', 'b567253a07b4689f2869b5013d07cb625705d09f4e525f64e6878ab6c8f482e4'),
    'P': ('.liu-visual-private/product-type-integration-20261004/P-approved-typography.png', '57c21466512a79cbb25c75db1d6a1748b595c3bc2d00c85ba51615557f74f925'),
    'R': ('.liu-visual-private/product-type-integration-20261004/R-current-reference.jpg', '87a28f5cd4b5d15b01e6536206127c357043a904b3c0dab3bfa0c50080782167'),
    'S': ('.liu-visual-private/source_recovery_20261003/photography-local-reconstruction-final.png', '7fd7777fed21100cb6b47bc305701476054263565e73246ac469d065aa080618'),
    'T': ('.liu-visual-private/correct_source_typography/v15/poster.png', '9f94b42f6fa92122ed56a0e6a78364b125bdba19da956b4d2345ca961097d714'),
}
FILES = ('headline.svg', 'headline-part-1.svg', 'headline-part-2.svg', 'brand.svg', 'foreground-protection.svg', 'PROVENANCE.json')
CHAR_MAP = ['茶','杯','杯','茶','一','杯','茶','，','茶','茶','慢','慢','来','下','慢','慢','来','下','慢']
# Maker-chosen optical extents, entirely within Root's production allowance.
TARGETS = {
    '杯': (605,405,134,137), '茶': (772,414,166,160),
    '，': (990,532,12,27), '慢': (1032,492,100,123),
    '下': (1138,511,74,109), '来': (1220,530,98,123),
}
# These are actual closed brush-stroke paths, not appended botanical icons.
# All coordinates here are the final viewport coordinates, with no transform.
DRAWN = {
    5: 'M437 529 C474 515 527 508 571 509 C578 509 583 507 587 504 C585 511 582 517 576 520 C530 516 479 523 444 532 C440 533 438 532 437 529 Z',
    7: 'M842 501 C848 497 853 496 860 501 L859 514 C868 514 874 516 879 521 C872 526 862 530 855 532 L853 586 C853 594 851 598 847 600 C841 598 835 594 830 585 C829 578 834 571 836 563 C841 543 839 518 842 501 Z',
    9: 'M847 515 C872 530 895 548 916 554 C936 561 956 563 978 554 C967 570 952 581 940 581 C918 578 895 558 874 542 C862 532 852 522 847 515 Z',
    19: 'M1092 555 C1097 552 1103 554 1109 559 C1111 562 1106 567 1102 571 L1096 578 C1109 585 1119 591 1132 595 C1127 604 1121 608 1114 605 C1102 598 1094 590 1087 587 C1077 594 1068 596 1056 593 C1066 591 1077 586 1082 581 C1075 578 1070 575 1066 571 C1077 572 1081 574 1087 575 C1091 571 1092 567 1094 563 C1088 565 1082 566 1076 563 C1071 561 1068 559 1067 557 C1079 557 1085 556 1092 555 Z',
}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encode_xml(element):
    return (ET.tostring(element, encoding='unicode') + '\n').encode('utf-8')


def assert_new():
    assert not PREVIEW.exists() and all(not (OUT / name).exists() for name in FILES), 'V16_OUTPUT_EXISTS_NO_OVERWRITE'


def preflight(args):
    paths, refs = {}, {}
    overrides = {'headline': args.source_headline, 'S': args.source_photo}
    for key, (relative, expected) in FIXED.items():
        path = Path(overrides[key]).resolve() if overrides.get(key) else ROOT / relative
        raw = path.read_bytes()
        assert sha(raw) == expected, 'FIXED_SOURCE_CHANGED:' + key
        paths[key] = path
        refs[key] = {'path': relative, 'sha256': expected, 'bytes': len(raw)}
    if not args.verify_only:
        assert_new()
    sys.path.append(str(SITE))
    import fontTools
    from fontTools.pens.boundsPen import BoundsPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.svgLib.path import parse_path
    assert sys.version_info[:3] == (3,12,14) and PIL.__version__ == '12.3.0' and fontTools.__version__ == '4.63.0', 'PYTHON_DEPENDENCY_CHANGED'
    node, sharp = RUNTIME / 'node/bin/node.exe', RUNTIME / 'node/node_modules/sharp'
    assert node.is_file() and sharp.is_dir(), 'RENDERER_MISSING'
    env = {k:v for k,v in os.environ.items() if k.upper() not in {'NODE_PATH','NODE_OPTIONS'}}
    code = 'const s=require(' + json.dumps(sharp.as_posix()) + ');process.stdout.write(JSON.stringify({node:process.version,sharp:s.versions.sharp,rsvg:s.versions.rsvg}));'
    versions = json.loads(subprocess.run([str(node),'-e',code], capture_output=True, text=True, env=env, check=True).stdout)
    assert versions == {'node':'v24.19.0','sharp':'0.35.4','rsvg':'2.62.91'}, 'RENDERER_VERSION_CHANGED'
    license_file = SITE / 'fonttools-4.63.0.dist-info/licenses/LICENSE'
    license_bytes = license_file.read_bytes()
    assert license_bytes.decode().startswith('MIT License'), 'FONTTOOLS_LICENSE_NOT_INSPECTED'
    deps = {'python':sys.version, 'Pillow':PIL.__version__, 'fontTools':fontTools.__version__, **versions,
            'fontTools_license': {'local_path':str(license_file),'sha256':sha(license_bytes),'license':'MIT'}}
    return paths, refs, BoundsPen, TransformPen, parse_path, node, sharp, env, deps


def render(svg, node, sharp, env):
    code = 'const s=require(' + json.dumps(sharp.as_posix()) + ');let a=[];process.stdin.on("data",x=>a.push(x));process.stdin.on("end",async()=>process.stdout.write(await s(Buffer.concat(a)).ensureAlpha().png().toBuffer()));'
    data = subprocess.run([str(node),'-e',code], input=svg, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, check=True).stdout
    return Image.open(io.BytesIO(data)).convert('RGBA')


def retouch_cup_stem(d):
    # Keep every untouched numeric token literal. Displace only control/end
    # points below raw y485 in the existing 木 stem; no sampling or retracing.
    token_re = re.compile(r'-?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?')
    tokens = list(token_re.finditer(d))
    changes = {}
    for i in range(0,len(tokens),2):
        x, y = float(tokens[i].group()), float(tokens[i+1].group())
        if y > 485:
            t = (y-485)/(509.3472167196971-485)
            changes[i] = repr(x-5*t*t)
            changes[i+1] = repr(y-2.5*t*t)
    result, start = [], 0
    for i,match in enumerate(tokens):
        result.extend((d[start:match.start()], changes.get(i,match.group())))
        start = match.end()
    result.append(d[start:])
    return ''.join(result), len(changes)//2


def construct(paths, BoundsPen, TransformPen, parse_path):
    source = ET.parse(paths['headline']).getroot()
    original = list(source.find(NS+'g'))
    assert source.find(NS+'title').text == COPY and [p.get('data-character') for p in original] == CHAR_MAP, 'SOURCE_CHARACTER_MAP_CHANGED'
    char_bounds = {}
    for char in set(CHAR_MAP):
        bs = []
        for element in original:
            if element.get('data-character') == char:
                pen = BoundsPen(None); parse_path(element.get('d'),pen); bs.append(pen.bounds)
        char_bounds[char] = (min(b[0] for b in bs),min(b[1] for b in bs),max(b[2] for b in bs),max(b[3] for b in bs))
    whole = ET.Element(NS+'svg', {'width':'1536','height':'1024','viewBox':'0 0 1536 1024','fill':'none'})
    ET.SubElement(whole,NS+'title').text = COPY
    ET.SubElement(whole,NS+'desc').text = 'V16 single sentence generated from cup-rim arc, real-leaf negative space and tray-edge cadence; literal inherited contours and explicitly reconstructed strokes. S photograph and V9 brand unchanged.'
    whole.append(copy.deepcopy(source.find(NS+'defs')))
    group = ET.SubElement(whole,NS+'g', {'id':'V16-one-cup-leaf-tray-sentence','clip-path':'url(#S-product-negative-space)'})
    details = []
    for index,p in enumerate(original,1):
        e = copy.deepcopy(p)
        char = p.get('data-character')
        e.set('id',f'V16-lettering-{index:02d}')
        e.set('fill',COLOR)
        e.set('data-line','1' if char in '一杯茶，' else '2')
        method = 'V15 source d retained literally, with declared optical affine placement.'
        if index in DRAWN:
            e.set('d',DRAWN[index]); e.attrib.pop('transform',None)
            matrix = (1,0,0,1,0,0)
            method = {5:'V16 original closed 一 stroke: upper cup-rim arc, no literal source d retained.',
                      7:'V16 replacement of existing 茶 木 stem: bent lower return and open leaf-side corridor; semantic stroke inherited, no literal source d retained.',
                      9:'V16 replacement of 茶 right 捺: forward sweep and upturned release beside real leaf tip; no literal source d retained.',
                      19:'V16 replacement of 慢 又 lower contour: crossing and bowl-like lower sweep; no literal source d retained.'}[index]
        else:
            x,y,w,h = TARGETS[char]; b = char_bounds[char]
            sx,sy = w/(b[2]-b[0]),h/(b[3]-b[1])
            matrix = (sx,0,0,sy,x-sx*b[0],y-sy*b[1])
            e.set('transform','matrix('+' '.join(repr(v) for v in matrix)+')')
            if index == 2:
                changed, point_count = retouch_cup_stem(p.get('d'))
                e.set('d',changed)
                method = 'V15 木 stem control/end points at raw y>485 displaced by x=-5t²,y=-2.5t²; '+str(point_count)+' points modified, all other numeric tokens retained; t=(y-485)/(509.3472167196971-485).'
        pen = BoundsPen(None); parse_path(e.get('d'),TransformPen(pen,matrix))
        group.append(e)
        details.append({'output_id':e.get('id'),'character':char,'source_V15_path_index_1based':index,
                        'source_V15_id':p.get('id'),'source_d_sha256':sha(p.get('d').encode()),
                        'output_d_sha256':sha(e.get('d').encode()),'source_d_retained_literal':e.get('d')==p.get('d'),
                        'method':method,'matrix':list(matrix),'unclipped_curve_bbox':list(pen.bounds),
                        'fill_rule':e.get('fill-rule','SVG nonzero default; source compound contours retained')})
    full = encode_xml(whole)
    # Sequential path intervals balance actual UTF-8 bytes. No coordinate or
    # path-string serialization happens again for the transport fragments.
    parts = []
    for first,last in ((1,10),(11,19)):
        part = copy.deepcopy(whole); g = part.find(NS+'g')
        for element in list(g):
            index = int(element.get('id').rsplit('-',1)[1])
            if not first <= index <= last: g.remove(element)
        parts.append(encode_xml(part))
    assert max(map(len,parts)) <= 40000, 'LITERAL_TRANSPORT_TOO_LARGE'
    return whole,full,parts,details


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--verify-only',action='store_true')
    ap.add_argument('--source-headline',type=Path)
    ap.add_argument('--source-photo',type=Path)
    args = ap.parse_args()
    paths,refs,BoundsPen,TransformPen,parse_path,node,sharp,env,deps = preflight(args)
    whole,full,parts,details = construct(paths,BoundsPen,TransformPen,parse_path)
    rgba = render(full,node,sharp,env); alpha = rgba.getchannel('A')
    bbox = alpha.getbbox()
    assert bbox and bbox[0]>=288 and bbox[1]>=400 and bbox[2]<=1328 and bbox[3]<=720, 'ROOT_PRODUCTION_BOUNDARY_EXCEEDED'
    layered = Image.new('RGBA',(1536,1024))
    for part in parts: layered.alpha_composite(render(part,node,sharp,env))
    assert ImageChops.difference(layered,rgba).getbbox(alpha_only=False) is None, 'TRANSPORT_RGBA_NOT_EQUAL_TO_WHOLE'
    no_clip = copy.deepcopy(whole); no_clip.find(NS+'g').attrib.pop('clip-path')
    raw_alpha = render(encode_xml(no_clip),node,sharp,env).getchannel('A')
    clipped = ImageChops.subtract(raw_alpha,alpha)
    clipped_pixels = sum(clipped.histogram()[1:])
    assert clipped_pixels == 0, 'ESSENTIAL_STROKE_WOULD_BE_CLIPPED'
    mask_bytes = paths['mask'].read_bytes()
    mask = render(mask_bytes,node,sharp,env).getchannel('A')
    core = mask.filter(ImageFilter.MinFilter(7)).point(lambda x:255 if x==255 else 0)
    core_count = sum(core.histogram()[1:])
    assert core_count == 162052, 'FIXED_PRODUCT_CORE_CHANGED'
    assert ImageChops.darker(alpha,core).getbbox() is None, 'LETTERING_INTERSECTS_PRODUCT_CORE'
    frozen = Image.open(paths['S']).convert('RGBA'); previous = Image.open(paths['T']).convert('RGBA')
    assert frozen.size == previous.size == rgba.size == (1536,1024), 'SOURCE_DIMENSIONS_CHANGED'
    preview = frozen.copy(); brand_box = (112,104,389,240)
    preview.paste(previous.crop(brand_box),brand_box[:2]); preview.alpha_composite(rgba)
    assert preview.crop(brand_box).tobytes() == previous.crop(brand_box).tobytes(), 'BRAND_PIXEL_BLOCK_CHANGED'
    diff = ImageChops.difference(preview.convert('RGB'),frozen.convert('RGB')).convert('L')
    assert ImageChops.darker(diff,core).getbbox() is None, 'PRODUCT_CORE_RGB_CHANGED'
    allowed = Image.new('L',(1536,1024),0); allowed.paste(255,brand_box); allowed.paste(255,(288,400,1328,720))
    assert ImageChops.multiply(diff,ImageChops.invert(allowed)).getbbox() is None, 'OUTSIDE_ENVELOPE_PHOTO_RGB_CHANGED'
    # All photo pixels outside actual headline alpha and the brand block also
    # remain exactly S, a tighter proof than the broad production envelope.
    touched = alpha.point(lambda v:255 if v else 0); touched.paste(255,brand_box)
    assert ImageChops.multiply(diff,ImageChops.invert(touched)).getbbox() is None, 'UNTOUCHED_PHOTO_RGB_CHANGED'
    buf=io.BytesIO(); preview.convert('RGB').save(buf,format='PNG'); preview_bytes=buf.getvalue()
    outputs = {'headline.svg':full,'headline-part-1.svg':parts[0],'headline-part-2.svg':parts[1],
               'brand.svg':paths['brand'].read_bytes(),'foreground-protection.svg':mask_bytes}
    proof = {
        'formal_asset':'V16','unique_design_count':1,'maker_role':'AI lettering maker, no professional human identity claimed',
        'copy':COPY,'viewport':[0,0,1536,1024],'import_position':[0,0],'import_dimensions':[1536,1024],
        'source_and_reference_files':refs,'actual_input_view_image':['P','R','S','T'],
        'reference_use':{'P':'Typography and hierarchy only. Rejected P photography not used.',
                         'R':'Upper advertisement only: product and lower-right message share composition. No asset/font/brand tracing; lower wall display excluded.',
                         'S':'Human-approved fixed photographic source; no generation, retouch, filter or RGB change.',
                         'T':'Actual V15 full poster viewed anonymously; V15 geometry is source input only, prior creator judgment not used as visual proof.'},
        'entry_and_skill_read':['AESTHETIC_SKILL_DESIGN_CHARTER.md','START_HERE.md','skills/restaurant-poster-art-director/SKILL.md','generation/RESTAURANT_POSTER_IMAGE_RULES_V1.md','config/restaurant-poster-generation.v1.json','calibration/README.md','calibration/anchors.json'],
        'product_derived_mechanism':'One descending sentence from cup-rim arc through a real-leaf negative corridor to the tray upper edge. Actual stroke reconstruction, not an added leaf symbol.',
        'actual_curve_and_alpha_bounds':{'alpha_bbox_exclusive':list(bbox),'root_allowance_not_human_aesthetic_coordinates':[288,400,1328,720]},
        'path_count':19,'source_d_retained_literal_count':sum(row['source_d_retained_literal'] for row in details),
        'path_provenance':details,
        'glyph_and_license_boundary':{'loaded_font_files':0,'new_imagegen_calls':0,
            'inherited_outline_source':'Fixed V15 title, descended project lettering contours. Direct per-path source SHA and changed-method recorded here.',
            'V16_handmade_outline_changes':'Indices 5,7,9,19 rebuilt as closed Bézier strokes; index2 source control points edited. No font imported, no font license invented.',
            'inherited_asset_license':'Existing project assets used within Root-assigned authorized scope; independent copyright/original-font clearance not performed. No third-party typeface license or public redistribution rights are asserted.',
            'brand':'V9 source copied byte-for-byte; preview brand block copied from T without any alteration.'},
        'tools_actually_used':{'Python':'Construction, parsing, provenance and fixed-source checks','FontTools':'SVG path parser, BoundsPen and TransformPen only; no fonts loaded','Pillow':'In-memory alpha composite and pixel checks','Node_sharp_librsvg':'Technical SVG raster preview','imagegen':0,'Figma':0,'Drive':0,'paid_API_or_CLI':0},
        'dependencies':deps,
        'method_references':{'implementation_basis':'Local actual SVG curve editing and the repository poster skill. No official proprietary method, plugin certification, or tutorial execution claimed.',
                             'skill_scope_overrides':'1536x1024, fixed brand/copy and one version from Root; default portrait/4K and independent batch quotas do not apply.'},
        'brand_preview_box':list(brand_box),'brand_preview_bytes_exact_to_V15':True,
        'protection':{'fixed_mask_bytes_exact':True,'3px_eroded_opaque_core_pixels':core_count,
                      'core_RGB_difference_vs_S_pixels':0,'clipped_headline_pixels':clipped_pixels,
                      'outside_actual_lettering_alpha_and_brand_RGB_difference_pixels':0,
                      'limit':'Fixed manual mask and 3px eroded core are exact; uncertain photographed silhouette edge outside mask is not claimed as independently segmented.'},
        'transport':{'parts':[{'filename':f'headline-part-{i+1}.svg','bytes':len(p),'sha256':sha(p)} for i,p in enumerate(parts)],
                     'literal_d_transform_fill_and_clip_defs':True,'additional_transport_rounding':False,'raster_RGBA_matches_whole':True,
                     'native_Figma_import_verified':False},
        'outputs':{name:{'sha256':sha(raw),'bytes':len(raw)} for name,raw in outputs.items()},
        'private_preview':{'path':PREVIEW.relative_to(ROOT).as_posix(),'sha256':sha(preview_bytes),'dimensions':[1536,1024]},
        'builder_sha256':sha(Path(__file__).read_bytes()),
        'operation_counts':{'formal_designs':1,'imagegen':0,'photo_editing':0,'Figma':0,'Drive':0,'Git':0,'business_state_write':0},
        'limitations':['Curve source title metadata is not OCR proof. Maker reads the saved full preview separately.',
                       'The product/lettering relationship requires new independent whole-poster review; no aesthetic PASS or human acceptance asserted.',
                       'Fixed Windows runtime reuse only; cross-platform automatic dependency discovery and concurrent/transactional creation are not validated.'],
    }
    outputs['PROVENANCE.json']=(json.dumps(proof,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    if args.verify_only:
        checked=[]
        for name,raw in outputs.items():
            if (OUT/name).exists():
                assert (OUT/name).read_bytes()==raw, 'SAVED_ASSET_DIFFERS_FROM_IN_MEMORY_REPLAY:'+name
                checked.append(name)
        if PREVIEW.exists():
            assert PREVIEW.read_bytes()==preview_bytes, 'SAVED_PRIVATE_PREVIEW_DIFFERS_FROM_REPLAY'
            checked.append(PREVIEW.relative_to(ROOT).as_posix())
        print(json.dumps({'mode':'verify-only','writes':0,'matched_outputs':checked,'core_pixels':core_count,'core_RGB_diff':0,'clipped_pixels':0,'alpha_bbox':bbox},ensure_ascii=True))
    else:
        # No writes precede all source, geometry, size, split, core and RGB checks.
        assert_new()
        for key,(_,expected) in FIXED.items():
            assert sha(paths[key].read_bytes())==expected, 'FIXED_SOURCE_CHANGED_BEFORE_WRITE:'+key
        PREVIEW.parent.mkdir(parents=True,exist_ok=True)
        for name,raw in outputs.items():
            with (OUT/name).open('xb') as fh: fh.write(raw)
        with PREVIEW.open('xb') as fh: fh.write(preview_bytes)
        print(json.dumps({'mode':'create-single-V16','outputs':proof['outputs'],'preview':proof['private_preview'],'core_pixels':core_count,'clipped_pixels':0,'alpha_bbox':bbox},ensure_ascii=True))


if __name__=='__main__':
    main()
