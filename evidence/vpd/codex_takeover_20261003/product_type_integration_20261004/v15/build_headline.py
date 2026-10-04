"""Construct one V15 compact two-line phrase from the fixed V14/V12 curves.

Only lettering is constructed. S, the V9 brand, and V14's product-protection
SVG are immutable. --verify-only replays all raster/vector outputs in memory
without writing. A normal run refuses all existing production output files.
"""
from pathlib import Path
import argparse, copy, hashlib, io, json, os, subprocess, sys
import xml.etree.ElementTree as ET
from PIL import Image, ImageChops, ImageFilter
import PIL

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[4]
PRIVATE_PREVIEW = ROOT / '.liu-visual-private/correct_source_typography/v15/preview.png'
RUNTIME = Path('C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies')
SITE = 'C:/Users/Administrator/AppData/Local/hermes/hermes-agent/venv/Lib/site-packages'
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
COPY = '一杯茶，慢下来'
FIXED = {
    'source_V14': ('evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v14/headline.svg', '0bf136ea73f15688d2cf44638ec0cbe131b9f8dc66d7142458a3df107e4d07e7'),
    'source_V12': ('evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v12/headline.svg', 'fb8e4106184083a2a6e6eea88cbccc2f08ea8dc9c5a1d3bd50d7404c264ff89e'),
    'brand': ('evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v14/brand.svg', 'dd8e9e899393dc36eb3f5b1652bdbb740787d41a108ea6aa1eae05cb1368b1ff'),
    'protection': ('evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v14/foreground-protection.svg', 'b567253a07b4689f2869b5013d07cb625705d09f4e525f64e6878ab6c8f482e4'),
    'feedback': ('evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v14/pixel_review/PIXEL_REVIEW.json', 'abc5f1af77d050692e600c00734ee08e1c94e3cf0bc461c45a7b96a765d1734d'),
    'P': ('.liu-visual-private/correct_source_typography/v14/packet/P.png', '57c21466512a79cbb25c75db1d6a1748b595c3bc2d00c85ba51615557f74f925'),
    'R': ('.liu-visual-private/correct_source_typography/v14/packet/R.jpg', '87a28f5cd4b5d15b01e6536206127c357043a904b3c0dab3bfa0c50080782167'),
    'S': ('.liu-visual-private/correct_source_typography/v14/packet/S.png', '7fd7777fed21100cb6b47bc305701476054263565e73246ac469d065aa080618'),
    'T': ('.liu-visual-private/correct_source_typography/v14/packet/T.png', '805aea7d33d0637b05421c034797d53f2b6368604f6e08e8e414f1f20e1a11a2'),
}
FILES = ('headline.svg', 'headline-part-1.svg', 'headline-part-2.svg', 'foreground-protection.svg', 'PROVENANCE.json')
# These are maker-selected construction targets within Root's technical bounds.
# Character extents are optical, rather than identical boxes imposed on 一/，.
TARGETS = {
    '一': (389, 422, 58, 8), '杯': (458, 400, 65, 57),
    '茶': (536, 400, 73, 58), '，': (624, 437, 9.5, 17),
    '慢': (408, 477, 66, 57), '下': (486, 478, 53, 53),
    '来': (551, 477, 68, 57),
}
INDEX_CHAR = ['茶', '杯', '杯', '茶', '一', '杯', '茶', '，', '茶', '茶', '慢', '慢', '来', '下', '慢', '慢', '来', '下', '慢']


def digest(b):
    return hashlib.sha256(b).hexdigest()


def preflight(verify):
    paths, refs = {}, {}
    for key, (relative, expected) in FIXED.items():
        path = ROOT / relative
        raw = path.read_bytes()
        assert digest(raw) == expected, 'FIXED_SOURCE_CHANGED:' + key
        paths[key] = path
        refs[key] = {'path': relative, 'sha256': expected, 'bytes': len(raw)}
    # PIL is imported before exposing the Hermes site to optional imports.
    sys.path.append(SITE)
    import fontTools
    from fontTools.pens.boundsPen import BoundsPen
    from fontTools.pens.recordingPen import RecordingPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.svgLib.path import parse_path
    assert sys.version_info[:3] == (3, 12, 14)
    assert PIL.__version__ == '12.3.0' and fontTools.__version__ == '4.63.0'
    node = RUNTIME / 'node/bin/node.exe'
    sharp = RUNTIME / 'node/node_modules/sharp'
    assert node.is_file() and sharp.is_dir(), 'REQUIRED_DEPENDENCY_MISSING'
    env = {k: v for k, v in os.environ.items() if k.upper() not in {'NODE_OPTIONS', 'NODE_PATH'}}
    code = 'const s=require(' + json.dumps(sharp.as_posix()) + ');process.stdout.write(JSON.stringify({node:process.version,sharp:s.versions.sharp,rsvg:s.versions.rsvg}));'
    versions = json.loads(subprocess.run([str(node), '-e', code], capture_output=True, text=True, check=True, env=env).stdout)
    assert versions == {'node': 'v24.19.0', 'sharp': '0.35.4', 'rsvg': '2.62.91'}, 'DEPENDENCY_VERSION_CHANGED'
    if not verify:
        assert all(not (OUT / f).exists() for f in FILES) and not PRIVATE_PREVIEW.exists(), 'V15_OUTPUT_EXISTS_NO_OVERWRITE'
    deps = {'python': sys.version, 'Pillow': PIL.__version__, 'fontTools': fontTools.__version__, **versions}
    return paths, refs, BoundsPen, RecordingPen, TransformPen, parse_path, node, sharp, env, deps


def raster(svg, node, sharp, env):
    code = 'const s=require(' + json.dumps(sharp.as_posix()) + ');let a=[];process.stdin.on("data",b=>a.push(b));process.stdin.on("end",async()=>process.stdout.write(await s(Buffer.concat(a)).ensureAlpha().png().toBuffer()));'
    return subprocess.run([str(node), '-e', code], input=svg, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, env=env).stdout


def xml(root):
    return (ET.tostring(root, encoding='unicode') + '\n').encode('utf-8')


def root_svg():
    return ET.Element('{' + NS + '}svg', {'width': '1536', 'height': '1024', 'viewBox': '0 0 1536 1024', 'fill': 'none'})


def altered_d(d, index, RecordingPen, parse_path):
    rec = RecordingPen()
    parse_path(d, rec)
    parts = []
    commands = {'moveTo': 'M', 'lineTo': 'L', 'curveTo': 'C', 'closePath': 'Z'}
    for command, points in rec.value:
        values = []
        for x, y in points:
            if index == 9:
                # Shorten the pre-existing connected right 捺, not a separate leaf.
                x = 620.8 + (x - 620.8) * .65
                y = 492.6 + (y - 492.6) * .70
            elif index == 19 and x > 900:
                # Compress only the outer tip of 慢's existing 又 stroke.
                x = 900 + (x - 900) * .78
            values.extend((x, y))
        parts.append(commands[command] + ' '.join(format(v, '.12g') for v in values))
    return ''.join(parts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    paths, refs, BoundsPen, RecordingPen, TransformPen, parse_path, node, sharp, env, deps = preflight(args.verify_only)
    source = ET.parse(paths['source_V14']).getroot()
    source12 = ET.parse(paths['source_V12']).getroot()
    sp = list(source.find('{' + NS + '}g'))
    sp12 = list(source12.find('{' + NS + '}g'))
    assert len(sp) == len(sp12) == 19
    assert source.find('{' + NS + '}title').text == source12.find('{' + NS + '}title').text == COPY
    assert [e.get('data-character') for e in sp] == INDEX_CHAR
    paths_out = [copy.deepcopy(e) for e in sp]
    # Restore 一's literal V12 stroke rather than V14's forced cup-rim tangent.
    paths_out[4].set('d', sp12[4].get('d'))
    for index in (9, 19):
        paths_out[index - 1].set('d', altered_d(sp[index - 1].get('d'), index, RecordingPen, parse_path))
    char_bounds = {}
    for char in COPY:
        bounds = []
        for element in paths_out:
            if element.get('data-character') == char:
                pen = BoundsPen(None)
                parse_path(element.get('d'), pen)
                bounds.append(pen.bounds)
        char_bounds[char] = (min(b[0] for b in bounds), min(b[1] for b in bounds), max(b[2] for b in bounds), max(b[3] for b in bounds))
    result = root_svg()
    ET.SubElement(result, '{' + NS + '}title').text = COPY
    ET.SubElement(result, '{' + NS + '}desc').text = 'One V15 compact two-line phrase. Sixteen V14 literal source paths retained; 一 restored from V12, 茶 and 慢 outer strokes shortened. Original S and V9 brand are unchanged. V14 fixed product core protection is retained byte-for-byte.'
    # Preserve the actual V14 clip definition and its original product contours.
    defs = copy.deepcopy(source.find('{' + NS + '}defs'))
    result.append(defs)
    group = ET.SubElement(result, '{' + NS + '}g', {'id': 'V15-one-compact-phrase', 'clip-path': 'url(#S-product-negative-space)'})
    rows = []
    for index, (original, element) in enumerate(zip(sp, paths_out), 1):
        char = element.get('data-character')
        x, y, w, h = TARGETS[char]
        b = char_bounds[char]
        sx, sy = w / (b[2] - b[0]), h / (b[3] - b[1])
        matrix = (sx, 0, 0, sy, x - sx * b[0], y - sy * b[1])
        element.set('transform', 'matrix(' + ' '.join(repr(v) for v in matrix) + ')')
        element.set('id', f'V15-lettering-{index:02d}')
        element.set('data-line', '1' if char in '一杯茶，' else '2')
        group.append(element)
        pen = BoundsPen(None)
        parse_path(element.get('d'), TransformPen(pen, matrix))
        rows.append({'source_path_index': index, 'character': char, 'V14_source_d_sha256': digest(original.get('d').encode()), 'V15_d_sha256': digest(element.get('d').encode()), 'V14_source_d_exact': original.get('d') == element.get('d'), 'matrix': list(matrix), 'unclipped_global_curve_bbox': list(pen.bounds)})
    changed_indices = [row['source_path_index'] for row in rows if not row['V14_source_d_exact']]
    assert changed_indices == [5, 9, 19], 'UNDECLARED_SOURCE_D_CHANGE'
    full = xml(result)
    parts = []
    for first, last in ((1, 10), (11, 19)):
        part = copy.deepcopy(result)
        g = part.find('{' + NS + '}g')
        for child in list(g):
            index = int(child.get('id').rsplit('-', 1)[1])
            if not first <= index <= last:
                g.remove(child)
        parts.append(xml(part))
    assert max(map(len, parts)) <= 40000, 'TRANSPORT_PART_EXCEEDS_40000_BYTES'
    protect_bytes = paths['protection'].read_bytes()
    rgba = Image.open(io.BytesIO(raster(full, node, sharp, env))).convert('RGBA')
    alpha = rgba.getchannel('A')
    alpha_bbox = alpha.getbbox()
    assert alpha_bbox[0] >= 288 and alpha_bbox[1] >= 400 and alpha_bbox[2] <= 1328 and alpha_bbox[3] <= 720, 'OUTSIDE_ROOT_TECHNICAL_ALLOWANCE'
    split = Image.new('RGBA', (1536, 1024))
    for part in parts:
        split.alpha_composite(Image.open(io.BytesIO(raster(part, node, sharp, env))).convert('RGBA'))
    assert ImageChops.difference(split, rgba).getbbox(alpha_only=False) is None, 'SPLIT_TRANSPORT_NOT_PIXEL_EXACT'
    unclipped = copy.deepcopy(result)
    unclipped.find('{' + NS + '}g').attrib.pop('clip-path')
    rawalpha = Image.open(io.BytesIO(raster(xml(unclipped), node, sharp, env))).convert('RGBA').getchannel('A')
    removed = ImageChops.subtract(rawalpha, alpha)
    removed_count = sum(removed.histogram()[1:])
    assert removed_count == 0, 'COMPACT_SENTENCE_MUST_NOT_LOSE_NEEDED_STROKES'
    mask = Image.open(io.BytesIO(raster(protect_bytes, node, sharp, env))).convert('RGBA').getchannel('A')
    core = mask.filter(ImageFilter.MinFilter(7)).point(lambda v: 255 if v == 255 else 0)
    core_count = sum(core.histogram()[1:])
    assert core_count == 162052, 'FIXED_PROTECTION_CORE_CHANGED'
    assert ImageChops.darker(alpha, core).getbbox() is None, 'TEXT_COVERS_PRODUCT_CORE'
    frozen = Image.open(paths['S']).convert('RGBA')
    previous = Image.open(paths['T']).convert('RGBA')
    assert frozen.size == previous.size == rgba.size == (1536, 1024)
    preview = frozen.copy()
    brand_box = (112, 104, 389, 240)
    preview.paste(previous.crop(brand_box), brand_box[:2])
    preview.alpha_composite(rgba)
    assert preview.crop(brand_box).tobytes() == previous.crop(brand_box).tobytes(), 'V9_BRAND_PIXEL_BLOCK_CHANGED'
    difference = ImageChops.difference(preview.convert('RGB'), frozen.convert('RGB')).convert('L')
    assert ImageChops.darker(difference, core).getbbox() is None, 'PRODUCT_CORE_RGB_CHANGED'
    # Stronger full-photo protection outside the allowed brand/headline envelopes.
    allowed = Image.new('L', (1536, 1024), 0)
    allowed.paste(255, brand_box)
    for box in ((389, 400, 635, 459), (408, 477, 620, 535)):
        allowed.paste(255, box)
    outside = ImageChops.multiply(difference, ImageChops.invert(allowed))
    assert outside.getbbox() is None, 'PHOTOGRAPHY_CHANGED_OUTSIDE_TEXT_ENVELOPES'
    preview_io = io.BytesIO()
    preview.convert('RGB').save(preview_io, format='PNG')
    preview_bytes = preview_io.getvalue()
    proof = {
        'asset_sequence': 'V15', 'exact_copy': COPY, 'unique_design_count': 1,
        'maker_only_no_review_pass_claim': True,
        'fixed_source_and_references': refs, 'input_view_image_actual': ['P', 'R', 'S', 'T'],
        'full_V14_feedback_read': True,
        'reference_limits': {'P': 'Typography only, excluded photography.', 'R': 'Upper advertisement only; grouping and product hierarchy studied, no tracing.'},
        'dependencies': deps,
        'viewport': [0, 0, 1536, 1024], 'import_position': [0, 0], 'import_dimensions': [1536, 1024],
        'root_technical_allowance_not_user_coordinates': [288, 400, 1328, 720],
        'brand_root_allowance': [104, 96, 400, 256], 'brand_actual_preview_block': list(brand_box),
        'actual_final_alpha_bbox_exclusive': list(alpha_bbox),
        'headline_two_envelopes_exclusive': [[389, 400, 635, 459], [408, 477, 620, 535]],
        'lettering_path_count': 19, 'changed_V14_source_d_indices': changed_indices,
        'source_d_changes': {
            '5': 'Literal V12 一 restored, then optical affine normalization to 58x8; removes V14 forced cup-rim tangent.',
            '9': 'Existing 茶 right descending connected stroke contracted about (620.8,492.6), x factor 0.65/y factor 0.70; no independent leaf component.',
            '19': 'Existing 慢 又 outer tip x>900 compressed about x900 by factor 0.78; left skeleton and y coordinates retained.',
            'other_16': 'V14 source d strings retained byte-exact; all characters receive declared affine placement matrices.',
        },
        'path_details': rows,
        'structure_implementation': 'One compact two-line group: 一杯茶， above 慢下来. Full-character cap heights settle around57px; optical treatment for 一/逗号. No glyph rotations, no long sentence across bokeh, no supplementary leaf/steam/connector shapes.',
        'visible_spatial_connections_for_independent_review': [
            {'location': 'brand to main sentence', 'actual_geometry': 'First row begins at x389, exactly the unchanged brand preview block right boundary. Second row inset19px creates one descending reading stair; the brand itself is untouched.', 'limit': 'This is a spatial alignment claim, not a claim that independent review will accept the remaining vertical gap.'},
            {'location': 'main sentence to cup lip', 'actual_geometry': 'Second row finishes at y534; cup protection begins at y550. Text has a continuous unbroken negative band above the actual convex cup rim, with no touching or clipped glyph.', 'limit': 'The gap varies with the actual photographic cup ellipse. It does not mathematically retrace the complete rim.'},
            {'location': 'terminal 来 to cup/leaf/tray passage', 'actual_geometry': 'Second row right edge x619 retreats14.5px from row1 comma edge. Its existing descending terminal points into the open lower-right region, which continues across the cup right flank toward the fixed fresh-leaf/tea-tray group.', 'limit': 'No leaf icon or joining line is added. Whether the distant leaf/tray is sufficiently linked remains a whole-poster review question.'},
        ],
        'foreground_protection': {
            'source_sha256': refs['protection']['sha256'], 'output_byte_exact_to_V14': True,
            'core_method': 'Opaque V14 protect raster, MinFilter(7), exactly255 threshold; 3px erosion.',
            'core_pixels': core_count, 'core_text_alpha_pixels': 0, 'core_preview_rgb_difference_pixels_vs_S': 0,
            'foreground_cropped_text_pixels': removed_count,
            'clip_behavior': 'Exact V14 negative-space clip retained only as safety protection; V15 has zero text occlusion. No product-depth integration is claimed from the clip itself.',
            'limitation': 'The162052-pixel fixed core excludes uncertain photographic silhouette edge pixels; full outside-envelope comparison provides additional protection.',
        },
        'photography_source_unchanged_sha256': refs['S']['sha256'],
        'brand_source_unchanged_sha256': refs['brand']['sha256'], 'brand_preview_pixel_block_exact_to_V14': True,
        'photo_rgb_difference_outside_brand_and_two_headline_envelopes_pixels': 0,
        'transport': {
            'parts': [{'filename': f'headline-part-{i+1}.svg', 'bytes': len(b), 'sha256': digest(b), 'indices': [1,10] if i == 0 else [11,19]} for i, b in enumerate(parts)],
            'parts_literal_d_transform_and_clipDefs_exact_to_whole': True,
            'parts_alpha_composite_matches_whole_pixel_exactly': True,
            'no_additional_coordinate_rounding_in_transport': True,
            'native_Figma_import_check': 'Root must verify actual imported SVG; maker performs no Figma operations.',
        },
        'copy_validation': 'Exact Unicode title and per-path character mapping checked. Preserved/declared curves and full private preview inspection documented in MAKER_INSPECTION.json after writing. Outlines have no semantic OCR guarantee.',
        'technical_method': 'Manual static SVG vector lettering and inherited evenodd clipPath. No generative image call, no photographed foreground replacement, no AI ObjectMask/Premiere invocation.',
        'operations': {'imagegen': 0, 'Figma': 0, 'Drive': 0, 'business_state': 0, 'git': 0},
        'outputs': {
            'headline.svg': {'sha256': digest(full), 'bytes': len(full)},
            'foreground-protection.svg': {'sha256': digest(protect_bytes), 'bytes': len(protect_bytes)},
            'preview.png': {'path': PRIVATE_PREVIEW.relative_to(ROOT).as_posix(), 'sha256': digest(preview_bytes), 'dimensions': [1536,1024]},
        },
        'script_sha256': digest(Path(__file__).read_bytes()),
    }
    content = {'headline.svg': full, 'headline-part-1.svg': parts[0], 'headline-part-2.svg': parts[1], 'foreground-protection.svg': protect_bytes, 'PROVENANCE.json': (json.dumps(proof, ensure_ascii=False, indent=2) + '\n').encode()}
    saved_checks = []
    if args.verify_only:
        for filename, raw in content.items():
            path = OUT / filename
            if path.exists():
                assert path.read_bytes() == raw, 'SAVED_ASSET_NOT_EQUAL_TO_REPLAY:' + filename
                saved_checks.append(filename)
        if PRIVATE_PREVIEW.exists():
            assert PRIVATE_PREVIEW.read_bytes() == preview_bytes, 'PRIVATE_PREVIEW_NOT_EQUAL_TO_REPLAY'
            saved_checks.append(PRIVATE_PREVIEW.relative_to(ROOT).as_posix())
    else:
        # Final no-overwrite and fixed-source check before the first output write.
        assert all(not (OUT / f).exists() for f in FILES) and not PRIVATE_PREVIEW.exists(), 'V15_OUTPUT_EXISTS_NO_OVERWRITE'
        for key, (_, expected) in FIXED.items():
            assert digest(paths[key].read_bytes()) == expected, 'FIXED_SOURCE_CHANGED_BEFORE_WRITE:' + key
        PRIVATE_PREVIEW.parent.mkdir(parents=True, exist_ok=True)
        for filename, raw in content.items():
            with (OUT / filename).open('xb') as handle:
                handle.write(raw)
        with PRIVATE_PREVIEW.open('xb') as handle:
            handle.write(preview_bytes)
    assert digest(paths['S'].read_bytes()) == FIXED['S'][1]
    print(json.dumps({'mode': 'zero_write' if args.verify_only else 'unique_asset_written', 'writes': 0 if args.verify_only else len(content)+1, 'alpha_bbox': alpha_bbox, 'SVG_sha256': digest(full), 'SVG_bytes': len(full), 'part_bytes': list(map(len, parts)), 'changed_source_d_indices': changed_indices, 'fixed_core_pixels': core_count, 'core_RGB_diff_pixels': 0, 'text_occlusion_pixels': removed_count, 'private_preview_path': str(PRIVATE_PREVIEW), 'private_preview_sha256': digest(preview_bytes), 'saved_outputs_byte_exact_verified': saved_checks}, ensure_ascii=False))


if __name__ == '__main__':
    main()
