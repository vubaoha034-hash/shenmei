"""Private, deterministic contour study of the authorized SHANYEJI JPEG.

No font substitution, image generation, OCR transcription, or background recovery.
The source image and generated images/SVG must remain in the private directory.
Uses the unmodified MIT VTracer 0.6.15 dependency installed by the parent task.
"""
from __future__ import annotations

import argparse
from collections import deque
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
SOURCE = ROOT / '.liu-visual-private/product-type-integration-20261004/SHANYEJI-canonical-readback-20261005.jpg'
EXPECTED_SHA = '9a29fbdc7dd908017924bed270e8dfe18351519eed3fa7bc7001789f2a383414'
sys.path.insert(0, str(ROOT / '.liu-visual-private/dependencies/vtracer_0_6_15_cp312/site-packages'))
import vtracer  # noqa: E402

SVG_NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', SVG_NS)
NODE = Path('C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe')
SHARP = 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp'


def retained_components(mask: np.ndarray, min_area: int) -> np.ndarray:
    """Remove only positive islands below the ROI-specific scale; preserve holes."""
    out = np.zeros_like(mask)
    remaining = mask.copy()
    h, w = mask.shape
    for y, x in zip(*np.nonzero(mask)):
        if not remaining[y, x]:
            continue
        q = deque([(int(y), int(x))])
        remaining[y, x] = False
        points = []
        while q:
            py, px = q.popleft()
            points.append((py, px))
            for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                ny, nx = py + dy, px + dx
                if 0 <= ny < h and 0 <= nx < w and remaining[ny, nx]:
                    remaining[ny, nx] = False
                    q.append((ny, nx))
        if len(points) >= min_area:
            yy, xx = zip(*points)
            out[yy, xx] = True
    return out


def in_roi(mask: np.ndarray, roi: tuple[int, int, int, int], min_area: int = 1) -> np.ndarray:
    x0, y0, x1, y1 = roi
    result = np.zeros_like(mask)
    result[y0:y1, x0:x1] = retained_components(mask[y0:y1, x0:x1], min_area)
    return result


def poly_mask(size: tuple[int, int], points: list[tuple[int, int]]) -> np.ndarray:
    image = Image.new('L', size)
    ImageDraw.Draw(image).polygon(points, fill=255)
    return np.asarray(image) > 0


def fill_enclosed_holes(mask: np.ndarray) -> np.ndarray:
    remaining = ~mask.copy()
    h,w = mask.shape
    q = deque()
    for x in range(w):
        for y in (0,h-1):
            if remaining[y,x]:
                remaining[y,x] = False; q.append((y,x))
    for y in range(h):
        for x in (0,w-1):
            if remaining[y,x]:
                remaining[y,x] = False; q.append((y,x))
    while q:
        y,x = q.popleft()
        for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)):
            ny,nx = y+dy,x+dx
            if 0<=ny<h and 0<=nx<w and remaining[ny,nx]:
                remaining[ny,nx] = False; q.append((ny,nx))
    return mask | remaining


def bilateral_underpaint(white: np.ndarray, orange_front: np.ndarray) -> np.ndarray:
    """Estimate white ink beneath observed orange only with opposite white support."""
    result = np.zeros_like(white)
    for dx,dy in ((1,0),(0,1),(1,1),(1,-1)):
        for distance in range(1,7):
            p = np.roll(white,(dy*distance,dx*distance),(0,1))
            n = np.roll(white,(-dy*distance,-dx*distance),(0,1))
            result |= p & n & orange_front
    return result


def weak_ink_near_core(core: np.ndarray, weak: np.ndarray, roi: tuple[int,int,int,int], radius: int = 2, min_area: int = 2) -> np.ndarray:
    """Recover JPEG's weak edge pixels only close to an independently colored core."""
    x0,y0,x1,y1 = roi
    c = core[y0:y1,x0:x1]
    w = weak[y0:y1,x0:x1]
    near = np.asarray(Image.fromarray(c.astype(np.uint8)*255).filter(ImageFilter.MaxFilter(radius*2+1))) > 0
    result = np.zeros_like(core)
    result[y0:y1,x0:x1] = retained_components(c | (w & near),min_area)
    return result


def vector_group(name: str, mask: np.ndarray, color: str, revision: Path, metadata: dict, aux_vector_scale: int = 1) -> ET.Element:
    yy, xx = np.nonzero(mask)
    group = ET.Element(f'{{{SVG_NS}}}g', {'id': name, 'data-name': name})
    desc = ET.SubElement(group, f'{{{SVG_NS}}}desc')
    desc.text = metadata.get('description', name)
    if not len(xx):
        return group
    x0, y0, x1, y1 = int(xx.min()), int(yy.min()), int(xx.max())+1, int(yy.max())+1
    crop = mask[y0:y1, x0:x1]
    # VTracer binary mode traces black foreground. White is not a backdrop layer.
    trace_image = Image.fromarray(np.where(crop, 0, 255).astype(np.uint8), 'L').convert('RGB')
    trace_path = revision / 'masks' / (name + '.png')
    trace_image.save(trace_path)
    # The source mask remains identical. Higher trace resolution protects 1px
    # auxiliary strokes from native-scale spline simplification.
    trace_scale = 1 if name.startswith(('main_','orange_line_')) else aux_vector_scale
    if trace_scale > 1:
        trace_image = trace_image.resize((trace_image.width*trace_scale,trace_image.height*trace_scale),Image.Resampling.NEAREST)
        trace_path = revision / 'raw-vector' / (name + '_trace_input.png')
        trace_image.save(trace_path)
    tmp_svg = revision / 'raw-vector' / (name + '.svg')
    vtracer.convert_image_to_svg_py(str(trace_path), str(tmp_svg), colormode='binary', mode='spline',
        filter_speckle=0, corner_threshold=40, length_threshold=1.5, max_iterations=10,
        splice_threshold=25, path_precision=3)
    raw = ET.parse(tmp_svg).getroot()
    group.set('transform', f'translate({x0} {y0}) scale({1/trace_scale})')
    i = 0
    empty_paths_removed = 0
    for element in raw:
        if element.tag.split('}')[-1] != 'path':
            continue
        if element.get('fill', '').lower() in ('#ffffff', '#fff', 'white'):
            continue
        i += 1
        if not element.get('d','').strip():
            empty_paths_removed += 1
            continue
        element.set('id', f'{name}_contour_{i:04d}')
        element.set('fill', color)
        # Native VTracer paths encode holes as subpaths; use explicit even-odd.
        element.set('fill-rule', 'evenodd')
        group.append(element)
    metadata.update({'name': name, 'fill': color, 'bbox': [x0,y0,x1,y1], 'mask_positive_pixels': int(mask.sum()), 'path_count': i-empty_paths_removed,'empty_tool_paths_removed':empty_paths_removed,'vector_trace_input_scale':trace_scale})
    return group


def render_svg(svg_path: Path, png_path: Path, background: str | None = None) -> None:
    code = 'const sharp=require(process.argv[1]); let s=sharp(process.argv[2]); if(process.argv[4]) s=s.flatten({background:process.argv[4]}); s.png().toFile(process.argv[3]).catch(e=>{console.error(e);process.exit(1)});'
    subprocess.run([str(NODE), '-e', code, SHARP, str(svg_path), str(png_path), background or ''], check=True)


def save_overlay(source: Image.Image, layers: list[tuple[str,np.ndarray,str,dict]], destination: Path) -> None:
    base = source.convert('RGBA')
    overlay = Image.new('RGBA', base.size)
    for _, mask, color, _ in layers:
        rgba = np.zeros((base.height, base.width, 4), dtype=np.uint8)
        rgba[:, :, :3] = (255, 20, 185)
        rgba[:, :, 3] = mask.astype(np.uint8) * 155
        overlay = Image.alpha_composite(overlay, Image.fromarray(rgba, 'RGBA'))
    Image.alpha_composite(base, overlay).save(destination)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--revision', default='00_main_baseline')
    parser.add_argument('--phase', choices=('main','full'), default='main')
    parser.add_argument('--correction', type=int, choices=(0,1,2), default=0)
    parser.add_argument('--aux-vector-scale',type=int,choices=(1,4),default=1)
    args = parser.parse_args()
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest() != EXPECTED_SHA:
        raise SystemExit('SOURCE_SHA_MISMATCH')
    source = Image.open(SOURCE).convert('RGB')
    if source.size != (960,1280):
        raise SystemExit('SOURCE_SIZE_MISMATCH')
    rgb = np.asarray(source).astype(np.int16)
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    white = (r>185)&(g>185)&(b>165)&(r>=g-16)&(r>=b-8)
    orange = (r>168)&(g>94)&(r-g>28)&(r-g<135)&(g-b>28)&(b<140)
    layers = []
    # Only observed orange segments are traced; the hidden continuous trajectory
    # beneath the mountain cannot be recovered from the source JPEG.
    line = in_roi(orange, (220,439,810,615), 18)
    front_roi = poly_mask(source.size, [(438,484),(548,484),(554,540),(438,540)]) | poly_mask(source.size, [(691,465),(801,465),(801,586),(691,586)])
    front = line & front_roi
    back = line & ~front_roi
    layers.append(('orange_line_visible_behind_main',back,'#E1903B', {'description':'Observed orange contour segments below white main mark; no hidden line completion.'}))
    for name,roi in [('shan',(216,424,428,547)),('ye',(441,442,646,608)),('ji',(645,434,798,612))]:
        mask = in_roi(white,roi,80)
        grain_removed = 0
        underpaint_pixels = 0
        if args.correction >= 1:
            # Correction 01 is bounded to the three main-glyph ROIs. Keep the
            # baseline outside edge, but expose darker inner printed distress.
            silhouette = fill_enclosed_holes(mask)
            interior = np.asarray(Image.fromarray(silhouette.astype(np.uint8)*255).filter(ImageFilter.MinFilter(3))) > 0
            printed_grain = interior & ((r<228)|(g<224)|(b<215))
            grain_removed = int((mask & printed_grain).sum())
            mask = mask & ~printed_grain
            underpaint = bilateral_underpaint(mask, front) & in_roi(np.ones_like(mask),roi)
            underpaint_pixels = int((underpaint & ~mask).sum())
            mask |= underpaint
        layers.append((f'main_{name}_white',mask,'#F6F4E8',{'description':f'Editable original-position contour of {name}; observed counters and texture holes are transparent.', 'grain_cutout_pixels_added':grain_removed,'estimated_white_under_orange_pixels':underpaint_pixels}))
    layers.append(('orange_line_visible_front_ye_and_ji',front,'#E1903B', {'description':'Observed orange crossing segments in front of ye upper-left block and ji upper-right strokes.'}))
    if args.phase == 'full':
        top_rois = [('WOK_HEI',(58,39,125,95)),('ORIGINAL_TASTE',(264,39,394,95)),('WILD_AROMA',(530,39,632,97)),('OLD_FARM_RECIPES',(770,39,907,95))]
        for label,roi in top_rois:
            layers.append((f'top_english_{label}',in_roi(white,roi,3),'#F4F4ED',{'description':'Observed English letters traced as paths: '+label.replace('_',' / ')}))
        gold = (r>141)&(g>126)&(b>78)&(r-g>=0)&(r-g<38)&(g-b>22)&(g-b<76)
        gold_en_mask = in_roi(gold,(220,556,359,613),3)
        gold_cn_mask = in_roi(gold,(302,644,660,681),3)
        handwriting = in_roi(orange,(229,785,738,858),4)
        if args.correction >= 2:
            # Correction 02 is bounded to auxiliary-text ROIs. Core/weak edge
            # colors differ because the JPEG mixes ink with the photograph.
            gold_en_core = (r>134)&(g>131)&(b>74)&(r-g>-18)&(r-g<34)&(g-b>27)&(r-b>26)
            gold_en_weak = (r>105)&(g>115)&(b>57)&(r-g>-24)&(r-g<36)&(g-b>25)&(r-b>26)
            gold_en_mask = weak_ink_near_core(gold_en_core,gold_en_weak,(220,556,359,613),2,2)
            gold_cn_core = (r>150)&(g>139)&(b>92)&(r-g>-8)&(r-g<40)&(g-b>22)&(r-b>30)
            gold_cn_weak = (r>110)&(g>110)&(b>60)&(r-g>-14)&(r-g<45)&(g-b>20)&(r-b>27)
            gold_cn_mask = weak_ink_near_core(gold_cn_core,gold_cn_weak,(302,644,660,681),2,2)
            handwriting_weak = (r>131)&(g>89)&(b>36)&(r-g>20)&(r-g<145)&(g-b>20)&(r-b>64)
            handwriting = weak_ink_near_core(orange,handwriting_weak,(229,785,738,858),2,3)
        layers.append(('gold_Mountain_market',gold_en_mask,'#B2AB7C',{'description':'Original two-line Mountain / market lettering traced as paths; raster softness is approximate.'}))
        layers.append(('gold_chinese_descriptor',gold_cn_mask,'#BAAC83',{'description':'Observed 常德饮食文化代表名片 outlines; no replacement font.'}))
        layers.append(('orange_handwriting_UNREADABLE_contours',handwriting,'#E1903B',{'description':'Observed handwritten contours only. Text identity is UNREADABLE for this study and is not guessed.'}))
        seal_orange = in_roi(orange,(151,428,209,552),5)
        seal_fill = fill_enclosed_holes(seal_orange)
        seal_black = seal_fill & (r<142)&(g<111)&(b<93)
        seal_black = retained_components(seal_black,3)
        layers.append(('LiJiaBan_seal_orange_shape',seal_fill,'#E78D36',{'description':'Orange stamp silhouette, holes under black lettering filled to support separate editable black layer.'}))
        layers.append(('LiJiaBan_seal_black_glyphs',seal_black,'#24190F',{'description':'Observed 李家班 black contours as separate paths over the orange stamp.'}))
        footerwhite = (r>160)&(g>158)&(b>145)&(np.abs(r-g)<26)&(np.abs(r-b)<45)
        footer_mark = in_roi(footerwhite,(329,1161,634,1212),4)
        footer_mark[:,429:449] = False
        layers.append(('attribution_NON_BRAND_WANCE_main',footer_mark,'#F4F4EB',{'description':'NON-BRAND designer attribution: 万策 / WANCE. Keep distinct from SHANYEJI content.'}))
        footerthin = (r>138)&(g>138)&(b>121)&(np.abs(r-g)<24)&(np.abs(r-b)<44)
        if args.correction >= 2:
            footerthin = (r>98)&(g>99)&(b>90)&(np.abs(r-g)<25)&(np.abs(r-b)<39)
        layers.append(('attribution_NON_BRAND_tagline',in_roi(footerthin,(374,1222,588,1248),1),'#B7B9AD',{'description':'NON-BRAND designer attribution tagline outlines; thin JPEG strokes are approximate.'}))
        layers.append(('attribution_NON_BRAND_WANCE_left',in_roi(footerthin,(33,1222,98,1243),1),'#9C9E94',{'description':'NON-BRAND left footer WANCE outlines.'}))
        layers.append(('attribution_NON_BRAND_DESIGN_right',in_roi(footerthin,(859,1222,931,1245),1),'#9C9E94',{'description':'NON-BRAND right footer DESIGN outlines.'}))
        footerseal = (r>131)&(g>131)&(b>115)&(np.abs(r-g)<25)&(np.abs(r-b)<42)
        if args.correction >= 2:
            footerseal = (r>95)&(g>98)&(b>87)&(np.abs(r-g)<25)&(np.abs(r-b)<42)
        layers.append(('attribution_NON_BRAND_tiny_seal_UNREADABLE',in_roi(footerseal,(428,1160,449,1196),1),'#ACAFA0',{'description':'NON-BRAND tiny attribution seal: contour trace only, UNREADABLE content not transcribed.'}))
    revision = HERE / args.revision
    for child in ('masks','raw-vector','reference-crops','comparisons'):
        (revision/child).mkdir(parents=True,exist_ok=True)
    svg = ET.Element(f'{{{SVG_NS}}}svg', {'width':'960','height':'1280','viewBox':'0 0 960 1280','version':'1.1'})
    ET.SubElement(svg,f'{{{SVG_NS}}}title').text = 'SHANYEJI original-position typography contour study, private reference reconstruction'
    ET.SubElement(svg,f'{{{SVG_NS}}}desc').text = 'Outline-only traced typography; no embedded image or font text. JPEG alpha and hidden outlines are estimates, not exact original assets.'
    manifest = {'source_sha256':EXPECTED_SHA,'source_size':[960,1280],'phase':args.phase,'revision':args.revision,'mask_correction':args.correction,'aux_vector_scale':args.aux_vector_scale,'groups':[], 'limits':['JPEG alpha is unavailable','Outlines, grain holes and occlusion edges are raster-derived approximations','White portions under visible orange crossings are locally estimated with opposite-side white support','No font identity claim','No new logo or background generation','Bottom-right tiny JPEG corner mark is UNREADABLE and not part of the brand reconstruction']}
    family_groups = {}
    for name,mask,color,data in layers:
        if name.startswith(('main_','orange_line_')):
            family = 'main_mark_editable_layers'
        elif name.startswith('top_english'):
            family = 'top_english_four_columns'
        elif name.startswith('gold_Mountain'):
            family = 'gold_English_support'
        elif name.startswith('gold_chinese'):
            family = 'gold_Chinese_support'
        elif name.startswith('orange_handwriting'):
            family = 'orange_handwriting_UNREADABLE'
        elif name.startswith('LiJiaBan'):
            family = 'LiJiaBan_orange_seal_black_letters'
        else:
            family = 'NON_BRAND_designer_attribution_WANCE'
        if family not in family_groups:
            family_groups[family] = ET.SubElement(svg,f'{{{SVG_NS}}}g',{'id':family,'data-name':family})
        family_groups[family].append(vector_group(name,mask,color,revision,data,args.aux_vector_scale))
        manifest['groups'].append(data)
    svg_path = revision/'SHANYEJI_typography_contours.svg'
    ET.ElementTree(svg).write(svg_path,encoding='utf-8',xml_declaration=True)
    render_svg(svg_path,revision/'SHANYEJI_typography_transparent.png')
    render_svg(svg_path,revision/'SHANYEJI_typography_darkgray_preview.png','#272927')
    save_overlay(source,layers,revision/'SHANYEJI_mask_overlay.png')
    rois = {'main_mark':(143,415,819,622),'shan_counter':(220,426,428,552),'ye_crossing':(435,438,646,609),'ji_crossing':(644,432,808,612)}
    if args.phase == 'full':
        rois.update({'top_english':(40,28,925,112),'gold_english':(211,548,365,620),'gold_chinese':(291,632,666,689),'orange_handwriting':(218,771,742,866),'seal':(149,425,212,556),'footer_attribution':(25,1148,941,1259)})
    rendered = Image.open(revision/'SHANYEJI_typography_darkgray_preview.png').convert('RGB')
    for name,roi in rois.items():
        source.crop(roi).save(revision/'reference-crops'/f'{name}_original.png')
        rendered.crop(roi).save(revision/'comparisons'/f'{name}_trace.png')
        crop_a = source.crop(roi)
        crop_b = rendered.crop(roi)
        pair = Image.new('RGB',(crop_a.width*2,crop_a.height),'#272927')
        pair.paste(crop_a,(0,0)); pair.paste(crop_b,(crop_a.width,0))
        pair.save(revision/'comparisons'/f'{name}_original_vs_trace.png')
    (revision/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'svg':str(svg_path),'svg_bytes':svg_path.stat().st_size,'groups':[(x['name'],x.get('path_count')) for x in manifest['groups']]},ensure_ascii=False))


if __name__ == '__main__':
    main()
