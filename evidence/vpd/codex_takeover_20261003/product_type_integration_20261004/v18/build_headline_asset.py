"""V18: replace only V17's one whole-sentence affine, then render one preview.

Calling without an explicit mode is rejected. --verify-only computes and verifies without writing.
--write is explicit, prechecks every target, and opens each new file exclusively.
The existing VTracer output, contour attributes, brand and product mask are reused.
This is a bounded asset adapter, not an aesthetic validator or a transaction engine.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import io
import json
import os
import subprocess
import sys
import xml.etree.ElementTree as ET

from PIL import Image, ImageChops, ImageFilter
import PIL

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
PREVIOUS = OUT.parent / 'v17'
PRIVATE = ROOT / '.liu-visual-private/correct_source_typography/v18'
PRIVATE17 = PRIVATE.parent / 'v17'
RUNTIME = Path('C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies')
NS = '{http://www.w3.org/2000/svg}'
OLD_AFFINE = 'matrix(0.285 0 0 0.285 596.784964375 351.83298908238123)'
AFFINE = 'matrix(0.24 0 0 0.24 401.7667811927463 343.4383065956895)'
SCALE, TX, TY = 0.24, 401.7667811927463, 343.4383065956895
BRAND_BOX = (104, 96, 400, 256)
AUTHORIZED_HEADLINE_BOX = (300, 380, 1350, 550)
OVERLAY_BOXES = [BRAND_BOX, (416, 380, 752, 550)]
PUBLIC_ASSETS = ['headline.svg', 'headline-part-1.svg', 'headline-part-2.svg',
                 'brand.svg', 'foreground-protection.svg']
PUBLIC_RECORDS = ['LETTERING_PROVENANCE.json', 'HANDOFF.json']
PRIVATE_ASSETS = ['preview.png', 'headline-render.png']
INPUTS = {
    'whole': (PREVIOUS / 'headline.svg', 'd4f79dc0dc1ae7c277abfa46c173e0823f36fdecc375af250e65758d86e02e42'),
    'part1': (PREVIOUS / 'headline-part-1.svg', '3365da4e3b8ea5c4da443119738e698ed4459b7754d55752eed22bb447687003'),
    'part2': (PREVIOUS / 'headline-part-2.svg', '3759afcdc59163a49a9a57e55a00146987ee3991e08b4cda9327b507f7573e05'),
    'brand': (PREVIOUS / 'brand.svg', 'dd8e9e899393dc36eb3f5b1652bdbb740787d41a108ea6aa1eae05cb1368b1ff'),
    'mask': (PREVIOUS / 'foreground-protection.svg', 'b567253a07b4689f2869b5013d07cb625705d09f4e525f64e6878ab6c8f482e4'),
    'trace': (PREVIOUS / 'upstream-alpha128-trace.svg', '2f02f6f795bfc43842cfdf493485f5750265f6b5a06ca6da36d55cb6a223c5c2'),
    'previous_provenance': (PREVIOUS / 'LETTERING_PROVENANCE.json', '661f60936b4cab773e68c0da2093aa6a8bb4aa56475db8e7e8a86138fef95de0'),
    'alpha': (PRIVATE17 / 'headline-generated-01.png', '57f469ed142b64b037827cd3df616b22c0435c70a2bad547278591ee7c31ad7a'),
    'poster17': (PRIVATE17 / 'poster.png', '7037751665c04f6f5d3a5aa59cdb4da7148b9d88769e70e790c612ae100f437d'),
    'photo': (ROOT / '.liu-visual-private/source_recovery_20261003/photography-local-reconstruction-final.png',
              '7fd7777fed21100cb6b47bc305701476054263565e73246ac469d065aa080618'),
}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def ref_bytes(path, raw):
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': sha(raw), 'bytes': len(raw)}


def json_bytes(obj):
    return (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def png_bytes(im):
    buff = io.BytesIO()
    im.save(buff, format='PNG')
    return buff.getvalue()


def render(raw):
    code = ('const s=require(' + json.dumps((RUNTIME / 'node/node_modules/sharp').as_posix()) + ');'
            'let a=[];process.stdin.on("data",x=>a.push(x));'
            'process.stdin.on("end",async()=>process.stdout.write('
            'await s(Buffer.concat(a)).ensureAlpha().png().toBuffer()));')
    env = {k: v for k, v in os.environ.items() if k.upper() not in {'NODE_PATH', 'NODE_OPTIONS'}}
    process = subprocess.run([str(RUNTIME / 'node/bin/node.exe'), '-e', code], input=raw,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    if process.returncode:
        raise RuntimeError(process.stderr.decode('utf-8', 'replace'))
    return Image.open(io.BytesIO(process.stdout)).convert('RGBA')


def contour_attributes(raw):
    root = ET.fromstring(raw)
    outer = root.find(NS + 'g')
    assert outer is not None and outer.get('clip-path') == 'url(#S-product-negative-space)'
    group = outer.find(NS + 'g')
    assert group is not None
    paths = list(group)
    assert all(p.tag == NS + 'path' and p.get('d', '').strip() for p in paths)
    return root, outer, group, [dict(p.attrib) for p in paths]


def change_affine(raw):
    assert raw.count(OLD_AFFINE.encode()) == 1, 'WHOLE_SENTENCE_AFFINE_NOT_UNIQUE'
    changed = raw.replace(OLD_AFFINE.encode(), AFFINE.encode())
    before = contour_attributes(raw)
    after = contour_attributes(changed)
    assert before[2].get('transform') == OLD_AFFINE
    assert after[2].get('transform') == AFFINE
    assert before[3] == after[3], 'CONTOUR_ATTRIBUTE_CHANGED'
    assert changed.replace(AFFINE.encode(), OLD_AFFINE.encode()) == raw
    return changed


def masked_count(diff, mask):
    for channel in diff.split():
        assert ImageChops.darker(channel, mask).getbbox() is None, 'PROTECTED_RGB_CHANGED'


def measure_alpha_differences(unclipped, clipped):
    lower = ImageChops.subtract(unclipped, clipped)
    higher = ImageChops.subtract(clipped, unclipped)
    coords = []
    bbox = ImageChops.difference(unclipped, clipped).getbbox()
    if bbox:
        a, b = unclipped.load(), clipped.load()
        for y in range(bbox[1], bbox[3]):
            for x in range(bbox[0], bbox[2]):
                if a[x, y] != b[x, y]:
                    coords.append({'x': x, 'y': y, 'unclipped_alpha': a[x, y],
                                   'clipped_alpha': b[x, y], 'signed_delta': b[x, y] - a[x, y]})
    return {'pixels_clipped_alpha_lower': sum(lower.histogram()[1:]),
            'pixels_clipped_alpha_higher': sum(higher.histogram()[1:]),
            'lower_maximum_alpha_delta': lower.getextrema()[1],
            'higher_maximum_alpha_delta': higher.getextrema()[1],
            'difference_bbox_exclusive': list(bbox) if bbox else None,
            'actual_coordinates': coords,
            'interpretation': 'These renderer alpha differences are above the product mask. '
                              'Geometric lettering/mask intersection is checked separately; '
                              'alpha equality is not claimed.'}


def calculate():
    sources = {}
    for name, (path, fixed_sha) in INPUTS.items():
        raw = path.read_bytes()
        assert sha(raw) == fixed_sha, 'FIXED_SOURCE_CHANGED:' + str(path)
        sources[name] = raw
    assets = {'headline.svg': change_affine(sources['whole']),
              'headline-part-1.svg': change_affine(sources['part1']),
              'headline-part-2.svg': change_affine(sources['part2']),
              'brand.svg': sources['brand'], 'foreground-protection.svg': sources['mask']}
    prior = json.loads(sources['previous_provenance'])
    rows = prior['source_to_output_contours']
    root, outer, group, contours = contour_attributes(assets['headline.svg'])
    assert len(contours) == len(rows) == 27 and prior['nonempty_paths_omitted'] == 0
    trace = list(ET.fromstring(sources['trace']))
    for contour, row in zip(contours, rows):
        original = trace[row['upstream_index']]
        assert contour['d'] == original.get('d')
        assert contour['transform'] == original.get('transform') == row['literal_source_transform']
        assert sha(contour['d'].encode()) == row['d_sha256']
        assert contour['fill'] == '#F5F2E6'
    part_contours = [contour_attributes(assets['headline-part-' + str(i) + '.svg'])[3] for i in (1, 2)]
    assert sorted(part_contours[0] + part_contours[1], key=lambda x: x['id']) == sorted(contours, key=lambda x: x['id'])
    assert all(len(assets['headline-part-' + str(i) + '.svg'].decode('utf-8')) < 40000 for i in (1, 2))

    rgba = render(assets['headline.svg'])
    alpha = rgba.getchannel('A')
    bbox = alpha.getbbox()
    assert bbox == (425, 384, 748, 548), 'UNEXPECTED_UNIQUE_GEOMETRY'
    assert bbox[0] >= AUTHORIZED_HEADLINE_BOX[0] and bbox[1] >= AUTHORIZED_HEADLINE_BOX[1]
    assert bbox[2] <= AUTHORIZED_HEADLINE_BOX[2] and bbox[3] <= AUTHORIZED_HEADLINE_BOX[3]
    unclip_root = copy.deepcopy(root)
    unclip_root.find(NS + 'g').attrib.pop('clip-path')
    ET.register_namespace('', NS[1:-1])
    unclip_alpha = render(ET.tostring(unclip_root)).getchannel('A')
    mask = render(sources['mask']).getchannel('A')
    mask_intersection = ImageChops.darker(unclip_alpha, mask)
    assert mask_intersection.getbbox() is None, 'LETTERING_INTERSECTS_PRODUCT_MASK'
    core = mask.filter(ImageFilter.MinFilter(7)).point(lambda v: 255 if v == 255 else 0)
    core_pixels = sum(core.histogram()[1:])
    assert core_pixels == 162052 and ImageChops.darker(alpha, core).getbbox() is None
    alpha_diff = measure_alpha_differences(unclip_alpha, alpha)

    parts = Image.new('RGBA', (1536, 1024))
    for i in (1, 2):
        parts.alpha_composite(render(assets['headline-part-' + str(i) + '.svg']))
    assert ImageChops.difference(parts, rgba).getbbox(alpha_only=False) is None, 'PARTS_RGBA_DIFFER'
    photo = Image.open(io.BytesIO(sources['photo'])).convert('RGBA')
    poster17 = Image.open(io.BytesIO(sources['poster17'])).convert('RGBA')
    assert photo.size == poster17.size == rgba.size == (1536, 1024)
    preview = photo.copy()
    preview.paste(poster17.crop(BRAND_BOX), BRAND_BOX[:2])
    preview.alpha_composite(rgba)
    photo_diff = ImageChops.difference(preview.convert('RGB'), photo.convert('RGB'))
    masked_count(photo_diff, core)
    protect = Image.new('L', (1536, 1024), 255)
    for box in OVERLAY_BOXES:
        protect.paste(0, box)
    masked_count(photo_diff, protect)
    assert ImageChops.difference(preview.crop(BRAND_BOX), poster17.crop(BRAND_BOX)).getbbox(alpha_only=False) is None
    private = {'preview.png': png_bytes(preview), 'headline-render.png': png_bytes(rgba)}

    cup_rows = [r for r in rows if r['upstream_index'] in (4, 7, 15, 28, 34)]
    cb = [min(r['source_curve_bounds'][0] for r in cup_rows),
          min(r['source_curve_bounds'][1] for r in cup_rows),
          max(r['source_curve_bounds'][2] for r in cup_rows),
          max(r['source_curve_bounds'][3] for r in cup_rows)]
    output_bounds = [SCALE * cb[0] + TX, SCALE * cb[1] + TY, SCALE * cb[2] + TX, SCALE * cb[3] + TY]
    report = {'version': 18, 'copy': '一杯茶，慢下来', 'brand': '茶作',
              'method': 'Literal replacement of V17 one whole-sentence uniform affine only',
              'new_image_generation_operations': 0, 'new_vectorization_operations': 0,
              'source_inputs': {k: ref_bytes(INPUTS[k][0], v) for k, v in sources.items()},
              'original_alpha': ref_bytes(INPUTS['alpha'][0], sources['alpha']),
              'trace': ref_bytes(INPUTS['trace'][0], sources['trace']),
              'upstream_path_count': prior['upstream_path_count'],
              'empty_paths_omitted': prior['empty_paths_omitted'],
              'retained_paths': 27, 'nonempty_paths_omitted': 0,
              'source_to_output_contours': rows, 'all_V17_contour_attributes_preserved': True,
              'only_literal_affine_changed_in_each_headline_svg': True,
              'original_alpha_preserved': True, 'source_curve_bounds': prior['source_curve_bounds'],
              'previous_whole_sentence_affine': OLD_AFFINE, 'one_whole_sentence_affine': AFFINE,
              'actual_alpha_bbox_exclusive': list(bbox),
              'authorised_headline_rectangle': list(AUTHORIZED_HEADLINE_BOX),
              'visible_design_overlay_envelopes': [list(b) for b in OVERLAY_BOXES],
              'brand_rectangle': list(BRAND_BOX), 'product_core_pixels': core_pixels,
              'product_core_RGB_differences': 0,
              'protected_outside_overlay_pixels': sum(protect.histogram()[1:]),
              'protected_outside_overlay_RGB_differences': 0,
              'brand_V17_RGB_differences': 0,
              'unclipped_lettering_product_mask_intersection_pixels': 0,
              'mask_removed_alpha_pixels': alpha_diff['pixels_clipped_alpha_lower'],
              'mask_removed_alpha_interpretation': 'Two one-level renderer alpha reductions above the product mask; no lettering/mask intersection.',
              'clipped_unclipped_renderer_alpha_difference': alpha_diff,
              'cup_anchor': {'original_contour_indices': [4, 7, 15, 28, 34],
                             'source_curve_bounds': cb, 'output_curve_bounds': output_bounds,
                             'output_geometric_center_x': (output_bounds[0] + output_bounds[2]) / 2,
                             'physical_cup_axis_x_estimate_from_actual_S_pixels': 535,
                             'physical_cup_rim_top_y_estimate_from_actual_S_pixels': 552,
                             'whole_phrase_bottom_exclusive': 548,
                             'rim_top_to_phrase_bottom_estimated_gap_px': 4,
                             'coordinate_estimates_are_not_hard_user_coordinates': True},
              'transport_parts': 2, 'part_path_counts': [len(p) for p in part_contours],
              'part_character_lengths': [len(assets['headline-part-' + str(i) + '.svg'].decode('utf-8')) for i in (1, 2)],
              'parts_RGBA_equal_to_whole': True,
              'outputs': {k: ref_bytes(OUT / k, v) for k, v in assets.items()},
              'private_preview': ref_bytes(PRIVATE / 'preview.png', private['preview.png']),
              'private_headline_render': ref_bytes(PRIVATE / 'headline-render.png', private['headline-render.png']),
              'software': {'Python': sys.version, 'Pillow': PIL.__version__,
                           'renderer': 'Existing bundled Node/sharp/librsvg render, unchanged',
                           'VTracer': 'Reuse of V17 fixed Python0.6.15/SVG-generator0.6.12 trace; no new conversion'},
              'licence_boundary': prior['licence_boundary'],
              'approximation_boundary': prior['approximation_boundary'],
              'aesthetic_pass_claimed': False, 'formal_independent_review': None,
              'native_TEXT_claimed': False,
              'builder_modes': {'default': 'argument parser rejects missing explicit mode',
                                'verify_only': 'in-memory compute and optional exact output readback; no file writes',
                                'write': 'all-target preflight plus exclusive per-file creation',
                                'multi_file_atomic_transaction_claimed': False}}
    records = {'LETTERING_PROVENANCE.json': json_bytes(report)}
    handoff = {'schema': 'vpd-v18-single-affine-asset-handoff/v1', 'asset_number': 18,
               'viewport': [1536, 1024], 'whole_phrase_affine': AFFINE,
               'headline_alpha_bbox_exclusive': list(bbox), 'retained_nonempty_contours': 27,
               'public_files': {k: ref_bytes(OUT / k, v) for k, v in {**assets, **records}.items()},
               'private_files': {k: ref_bytes(PRIVATE / k, v) for k, v in private.items()},
               'builder': ref_bytes(Path(__file__), Path(__file__).read_bytes()),
               'part_character_lengths': report['part_character_lengths'],
               'native_TEXT_claimed': False, 'path_editability': 'Existing SVG paths remain editable; no font files or native text supplied.',
               'formal_aesthetic_verdict': None, 'new_image_generation_operations': 0,
               'photo_generations_or_edits': 0, 'business_state_writes_by_maker': 0,
               'Figma_Drive_Git_writes_by_maker': 0,
               'root_actions_remaining': ['Figma import/readback', 'official full-frame export and source/core checks',
                                          'Drive private original archive/readback', 'fresh independent cold review',
                                          'root-only current-state registration']}
    records['HANDOFF.json'] = json_bytes(handoff)
    outputs = {**{OUT / k: v for k, v in assets.items()},
               **{OUT / k: v for k, v in records.items()},
               **{PRIVATE / k: v for k, v in private.items()}}
    return outputs, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--verify-only', action='store_true')
    mode.add_argument('--write', action='store_true')
    args = parser.parse_args()
    targets = [OUT / n for n in PUBLIC_ASSETS + PUBLIC_RECORDS] + [PRIVATE / n for n in PRIVATE_ASSETS]
    if args.write:
        assert not any(p.exists() for p in targets), 'OUTPUT_ALREADY_EXISTS'
    outputs, report = calculate()
    assert set(outputs) == set(targets)
    if args.verify_only:
        existing = [p for p in targets if p.exists()]
        if existing:
            assert len(existing) == len(targets), 'PARTIAL_OUTPUTS_PRESENT'
            for path, raw in outputs.items():
                assert path.read_bytes() == raw, 'OUTPUT_READBACK_MISMATCH:' + str(path)
        action = 'verified-existing' if existing else 'verified-before-write'
    else:
        assert not any(p.exists() for p in targets), 'OUTPUT_ALREADY_EXISTS'
        PRIVATE.mkdir(parents=True, exist_ok=True)
        for path, raw in outputs.items():
            with path.open('xb') as file:
                file.write(raw)
        action = 'wrote-new'
    print(json.dumps({'mode': 'verify-only' if args.verify_only else 'write', 'action': action,
                      'writes': 0 if args.verify_only else len(outputs),
                      'paths': report['retained_paths'], 'affine': AFFINE,
                      'bbox': report['actual_alpha_bbox_exclusive'],
                      'cup_center_x': report['cup_anchor']['output_geometric_center_x'],
                      'mask_intersection_pixels': 0, 'core_pixels': report['product_core_pixels'],
                      'core_RGB_differences': 0, 'part_character_lengths': report['part_character_lengths'],
                      'preview': report['private_preview'], 'headline': report['outputs']['headline.svg'],
                      'renderer_alpha_difference': report['clipped_unclipped_renderer_alpha_difference']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
