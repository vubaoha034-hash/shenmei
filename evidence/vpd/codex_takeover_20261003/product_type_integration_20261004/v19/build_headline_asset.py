"""V19 bounded adapter: keep V18 contours and move the whole phrase down 18px.
Reuses the fixed V18 renderer/helpers without changing that builder.
Explicit --verify-only computes/readbacks with no writes; --write creates new files
exclusively. Calling without an explicit mode is rejected. Product clipping is intentional and measured.
"""
from pathlib import Path
import argparse, copy, hashlib, json, runpy, sys, xml.etree.ElementTree as ET
from PIL import Image, ImageChops, ImageFilter

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
OLD = OUT.parent / 'v18'
PRIVATE = ROOT / '.liu-visual-private/correct_source_typography/v19'
NS = '{http://www.w3.org/2000/svg}'
BEFORE = 'matrix(0.24 0 0 0.24 401.7667811927463 343.4383065956895)'
AFFINE = 'matrix(0.24 0 0 0.24 401.7667811927463 361.4383065956895)'
BRAND_BOX = (104, 96, 400, 256)
BOXES = [BRAND_BOX, (416, 400, 760, 576)]
HEADLINE_ALLOWANCE = [288, 400, 1328, 720]
PUBLIC = ['headline.svg', 'headline-part-1.svg', 'headline-part-2.svg',
          'brand.svg', 'foreground-protection.svg', 'LETTERING_PROVENANCE.json', 'HANDOFF.json']
PRIV = ['preview.png', 'headline-render.png']
INPUTS = {
    'whole': (OLD / 'headline.svg', '466538676e1a6395e0167f5765306e26ae05ea34d168856bbfd2617c2d630aa6'),
    'part1': (OLD / 'headline-part-1.svg', '5edd3b9d04905cb8d2cc0b7c5f6d5d3a80db4488c0ded7364ca33ac78d6db514'),
    'part2': (OLD / 'headline-part-2.svg', '097dc15503e75cd4b325568a7b9accce416dacb74a8f4f581a226d98ead02280'),
    'brand': (OLD / 'brand.svg', 'dd8e9e899393dc36eb3f5b1652bdbb740787d41a108ea6aa1eae05cb1368b1ff'),
    'mask': (OLD / 'foreground-protection.svg', 'b567253a07b4689f2869b5013d07cb625705d09f4e525f64e6878ab6c8f482e4'),
    'provenance18': (OLD / 'LETTERING_PROVENANCE.json', 'd5700d75edafe7ddb414616d78bbe26ef0301e10c47cb392b98de6698de8437e'),
    'helper18': (OLD / 'build_headline_asset.py', '24102f462f379255c29be0209cd63f91d3e862f80956a96b012471eccc18e8e5'),
    'poster18': (PRIVATE.parent / 'v18/poster.png', '2357e745eeaed1faf26bce0fc4680810dfceea04fbd9bf9463b84b6c970feaee'),
    'photo': (ROOT / '.liu-visual-private/source_recovery_20261003/photography-local-reconstruction-final.png',
              '7fd7777fed21100cb6b47bc305701476054263565e73246ac469d065aa080618'),
    'trace': (OLD.parent / 'v17/upstream-alpha128-trace.svg', '2f02f6f795bfc43842cfdf493485f5750265f6b5a06ca6da36d55cb6a223c5c2'),
    'alpha': (PRIVATE.parent / 'v17/headline-generated-01.png', '57f469ed142b64b037827cd3df616b22c0435c70a2bad547278591ee7c31ad7a'),
}

def count(im):
    return sum(im.histogram()[1:])

def alpha_sum(im):
    return sum(v * n for v, n in enumerate(im.histogram()))

def alpha_stats(im):
    return {'nonzero_pixels': count(im), 'maximum_alpha_delta': im.getextrema()[1],
            'alpha_coverage_equivalent_pixels': alpha_sum(im) / 255,
            'bbox_exclusive': list(im.getbbox()) if im.getbbox() else None}

def without_clip(raw):
    root = ET.fromstring(raw)
    root.find(NS + 'g').attrib.pop('clip-path')
    return ET.tostring(root)

def calculate():
    source = {}
    for k, (p, fixed) in INPUTS.items():
        source[k] = p.read_bytes()
        assert hashlib.sha256(source[k]).hexdigest() == fixed, 'FIXED_SOURCE_CHANGED:' + str(p)
    h = runpy.run_path(str(INPUTS['helper18'][0]))
    render, ref, jb, png = h['render'], h['ref_bytes'], h['json_bytes'], h['png_bytes']
    attrs, protect_rgb = h['contour_attributes'], h['masked_count']
    ET.register_namespace('', NS[1:-1])
    def moved(raw):
        assert raw.count(BEFORE.encode()) == 1
        new = raw.replace(BEFORE.encode(), AFFINE.encode())
        assert attrs(raw)[3] == attrs(new)[3]
        assert new.replace(AFFINE.encode(), BEFORE.encode()) == raw
        return new
    assets = {'headline.svg': moved(source['whole']), 'headline-part-1.svg': moved(source['part1']),
              'headline-part-2.svg': moved(source['part2']), 'brand.svg': source['brand'],
              'foreground-protection.svg': source['mask']}
    prior = json.loads(source['provenance18'])
    root, _, group, contours = attrs(assets['headline.svg'])
    rows = prior['source_to_output_contours']
    trace = list(ET.fromstring(source['trace']))
    assert len(rows) == len(contours) == 27
    for c, row in zip(contours, rows):
        original = trace[row['upstream_index']]
        assert c['d'] == original.get('d') and c['transform'] == original.get('transform')
        assert c['fill'] == '#F5F2E6'
    mask = render(source['mask']).getchannel('A')
    mask_on = mask.point(lambda v: 255 if v else 0)
    mask_off = mask_on.point(lambda v: 255 - v)
    clipped = render(assets['headline.svg'])
    unclipped = render(without_clip(assets['headline.svg']))
    a, u = clipped.getchannel('A'), unclipped.getchannel('A')
    assert u.getbbox() == (425, 402, 748, 566) and a.getbbox() == (425, 402, 748, 565)
    lower, higher = ImageChops.subtract(u, a), ImageChops.subtract(a, u)
    removed = ImageChops.darker(lower, mask_on)
    aa_lower = ImageChops.darker(lower, mask_off)
    aa_higher = ImageChops.darker(higher, mask_off)
    per_contour = []
    glyphs = {50: '慢左竖末端', 51: '下端缘', 66: '慢下部外展', 71: '慢内部微轮廓', 74: '慢内部微轮廓'}
    for node, row in zip(list(group), rows):
        if 0.24 * row['source_curve_bounds'][3] + 361.4383065956895 < 549:
            continue
        one = copy.deepcopy(root)
        og = one.find(NS + 'g').find(NS + 'g')
        og[:] = [copy.deepcopy(node)]
        ca = render(ET.tostring(one)).getchannel('A')
        ua = render(without_clip(ET.tostring(one))).getchannel('A')
        loss = ImageChops.darker(ImageChops.subtract(ua, ca), mask_on)
        if count(loss):
            per_contour.append({'upstream_index': row['upstream_index'], 'glyph_part': glyphs.get(row['upstream_index'], 'original contour'),
                                'true_removed_alpha': alpha_stats(loss), 'unclipped_nonzero_alpha_pixels': count(ua),
                                'lost_alpha_coverage_fraction': alpha_sum(loss) / alpha_sum(ua),
                                'entire_visible_contour_occluded': ca.getbbox() is None})
    parts, unclip_parts = Image.new('RGBA', (1536, 1024)), Image.new('RGBA', (1536, 1024))
    part_attrs, part_sizes = [], []
    for i in (1, 2):
        raw = assets[f'headline-part-{i}.svg']
        assert len(raw.decode('utf-8')) < 40000
        part_sizes.append(len(raw.decode('utf-8')))
        part_attrs += attrs(raw)[3]
        parts.alpha_composite(render(raw))
        unclip_parts.alpha_composite(render(without_clip(raw)))
    assert sorted(part_attrs, key=lambda c: c['id']) == sorted(contours, key=lambda c: c['id'])
    parts_diff = ImageChops.difference(parts, clipped)
    unclip_parts_diff = ImageChops.difference(unclip_parts, unclipped)
    assert parts_diff.getbbox(alpha_only=False) is None
    core = mask.filter(ImageFilter.MinFilter(7)).point(lambda v: 255 if v == 255 else 0)
    assert count(core) == 162052 and ImageChops.darker(a, core).getbbox() is None
    photo = Image.open(INPUTS['photo'][0]).convert('RGBA')
    poster18 = Image.open(INPUTS['poster18'][0]).convert('RGBA')
    assert photo.size == poster18.size == clipped.size == (1536, 1024)
    preview = photo.copy()
    preview.paste(poster18.crop(BRAND_BOX), BRAND_BOX[:2])
    preview.alpha_composite(clipped)
    difference = ImageChops.difference(preview.convert('RGB'), photo.convert('RGB'))
    protect_rgb(difference, core)
    protected = Image.new('L', (1536, 1024), 255)
    for box in BOXES:
        protected.paste(0, box)
    protect_rgb(difference, protected)
    assert ImageChops.difference(preview.crop(BRAND_BOX), poster18.crop(BRAND_BOX)).getbbox(alpha_only=False) is None
    private = {'preview.png': png(preview), 'headline-render.png': png(clipped)}
    report = copy.deepcopy(prior)
    report.update(version=19, method='Only the whole phrase V18 affine moves down 18px; fixed product foreground clip intentionally occludes text',
                  source_inputs={k: ref(INPUTS[k][0], raw) for k, raw in source.items()},
                  original_alpha=ref(INPUTS['alpha'][0], source['alpha']), trace=ref(INPUTS['trace'][0], source['trace']),
                  previous_whole_sentence_affine=BEFORE, one_whole_sentence_affine=AFFINE,
                  actual_alpha_bbox_exclusive=list(a.getbbox()), unclipped_alpha_bbox_exclusive=list(u.getbbox()),
                  authorised_headline_rectangle=HEADLINE_ALLOWANCE, visible_design_overlay_envelopes=[list(b) for b in BOXES],
                  protected_outside_overlay_pixels=count(protected), all_V18_contour_attributes_preserved=True, brand_V18_RGB_differences=0,
                  retained_paths_in_svg_are_not_a_claim_of_no_visible_occlusion=True,
                  unclipped_lettering_product_mask_intersection_pixels=count(ImageChops.darker(u, mask)),
                  mask_removed_alpha_pixels=count(removed),
                  mask_removed_alpha_interpretation='Actual text occlusion inside the fixed product mask, reported separately from exterior AA differences.',
                  clipped_unclipped_renderer_alpha_difference={'true_product_occlusion': alpha_stats(removed),
                    'true_removed_alpha_pixel_fraction': count(removed) / count(u),
                    'lost_alpha_coverage_fraction': alpha_sum(removed) / alpha_sum(u),
                    'unclipped_nonzero_alpha_pixels': count(u), 'outside_mask_AA_lower': alpha_stats(aa_lower),
                    'outside_mask_AA_higher': alpha_stats(aa_higher), 'all_lower': alpha_stats(lower), 'all_higher': alpha_stats(higher),
                    'per_original_contour_occlusion': per_contour, 'per_contour_counts_must_not_be_summed_due_to_overlap': True},
                  part_character_lengths=part_sizes,
                  parts_RGBA_equal_to_whole=parts_diff.getbbox(alpha_only=False) is None,
                  unclipped_parts_RGBA_equal_to_whole=unclip_parts_diff.getbbox(alpha_only=False) is None,
                  unclipped_parts_RGBA_difference_bbox_exclusive=unclip_parts_diff.getbbox(alpha_only=False),
                  outputs={k: ref(OUT / k, raw) for k, raw in assets.items()},
                  private_preview=ref(PRIVATE / 'preview.png', private['preview.png']),
                  private_headline_render=ref(PRIVATE / 'headline-render.png', private['headline-render.png']),
                  native_TEXT_claimed=False, aesthetic_pass_claimed=False, formal_independent_review=None)
    report['cup_anchor']['output_curve_bounds'][1] += 18
    report['cup_anchor']['output_curve_bounds'][3] += 18
    report['cup_anchor']['whole_phrase_bottom_exclusive'] = 565
    report['cup_anchor'].pop('rim_top_to_phrase_bottom_estimated_gap_px', None)
    report['cup_anchor']['whole_phrase_unclipped_bottom_exclusive'] = 566
    report['software']['reused_helper18'] = ref(INPUTS['helper18'][0], source['helper18'])
    records = {'LETTERING_PROVENANCE.json': jb(report)}
    handoff = {'schema': 'vpd-v19-single-affine-foreground-occlusion-handoff/v1', 'asset_number': 19,
               'viewport': [1536, 1024], 'whole_phrase_affine': AFFINE, 'retained_nonempty_contours': 27,
               'headline_alpha_bbox_exclusive': list(a.getbbox()), 'unclipped_headline_alpha_bbox_exclusive': list(u.getbbox()),
               'public_files': {k: ref(OUT / k, raw) for k, raw in {**assets, **records}.items()},
               'private_files': {k: ref(PRIVATE / k, raw) for k, raw in private.items()},
               'builder': ref(Path(__file__), Path(__file__).read_bytes()), 'part_character_lengths': part_sizes,
               'native_TEXT_claimed': False, 'formal_aesthetic_verdict': None, 'new_image_generation_operations': 0,
               'photo_generations_or_edits': 0, 'business_state_writes_by_maker': 0, 'Figma_Drive_Git_writes_by_maker': 0,
               'root_actions_remaining': ['Figma official import/export and source/core checks', 'Drive original archive/readback',
                                          'Fresh independent pixel review', 'Root-only current-state registration']}
    records['HANDOFF.json'] = jb(handoff)
    return {**{OUT / k: v for k, v in {**assets, **records}.items()},
            **{PRIVATE / k: v for k, v in private.items()}}, report

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--verify-only', action='store_true')
    mode.add_argument('--write', action='store_true')
    args = parser.parse_args()
    targets = [OUT / n for n in PUBLIC] + [PRIVATE / n for n in PRIV]
    if args.write:
        assert not any(p.exists() for p in targets), 'OUTPUT_ALREADY_EXISTS'
    outputs, report = calculate()
    assert set(outputs) == set(targets)
    if args.verify_only:
        existing = [p for p in targets if p.exists()]
        if existing:
            assert len(existing) == len(targets), 'PARTIAL_OUTPUTS_PRESENT'
            for p, raw in outputs.items():
                assert p.read_bytes() == raw, 'OUTPUT_READBACK_MISMATCH:' + str(p)
        action = 'verified-existing' if existing else 'verified-before-write'
    else:
        assert not any(p.exists() for p in targets), 'OUTPUT_ALREADY_EXISTS'
        PRIVATE.mkdir(parents=True, exist_ok=True)
        for p, raw in outputs.items():
            with p.open('xb') as file:
                file.write(raw)
        action = 'wrote-new'
    print(json.dumps({'mode': 'verify-only' if args.verify_only else 'write', 'action': action,
                      'writes': 0 if args.verify_only else len(outputs), 'paths': 27, 'affine': AFFINE,
                      'bbox': report['actual_alpha_bbox_exclusive'], 'unclipped_bbox': report['unclipped_alpha_bbox_exclusive'],
                      'true_occlusion': report['clipped_unclipped_renderer_alpha_difference']['true_product_occlusion'],
                      'core_pixels': 162052, 'core_RGB_differences': 0, 'part_character_lengths': report['part_character_lengths'],
                      'headline': report['outputs']['headline.svg'], 'preview': report['private_preview'],
                      'parts_RGBA_equal_to_whole': report['parts_RGBA_equal_to_whole'],
                      'unclipped_parts_RGBA_equal_to_whole': report['unclipped_parts_RGBA_equal_to_whole']}, ensure_ascii=False))

if __name__ == '__main__':
    main()

