"""Prospective V22+ pixel proof; registration must be frozen by Root before use.

This reads and independently renders literal, source-bound lettering. It never
infers alpha from the final image, changes S, writes files, or judges typography.
It cannot authenticate a Figma/tool transcript or determine that generated curves
spell the copy: real read-only Figma collection and fresh image review remain due.
"""
from pathlib import Path
import copy
import hashlib
import importlib.metadata
import io
import json
import math
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

import PIL
from PIL import Image, ImageChops

SCHEMA = 'vpd-registered-type-composite/v1'
COPY = '一杯茶，慢下来'
SIZE = (1536, 1024)
NS = '{http://www.w3.org/2000/svg}'
ET.register_namespace('', NS[1:-1])
SERIES = 'evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/'
SOURCE = {'path': '.liu-visual-private/source_recovery_20261003/photography-local-reconstruction-final.png',
          'sha256': '7fd7777fed21100cb6b47bc305701476054263565e73246ac469d065aa080618'}
BRAND = {'path': SERIES + 'v21/brand.svg',
         'sha256': 'dd8e9e899393dc36eb3f5b1652bdbb740787d41a108ea6aa1eae05cb1368b1ff'}
CORE = {'path': SERIES + 'audit/FIXED_PRODUCT_CORE_MAP.json',
        'sha256': '6f17681f217db23c0ccbb2a30ac01878581d1ee867800169156cb66b60b3092f'}
HELPER = {'path': SERIES + 'v18/build_headline_asset.py',
          'sha256': '24102f462f379255c29be0209cd63f91d3e862f80956a96b012471eccc18e8e5'}
FONT_SHA = '78aa7a328fd974df2d688c8a9fd74a33d8334dfa84ab24d9d11efb2ffc464117'
FONT_COMMAND_SHAS = [
    'b2985959007a2f3073bdc5268c195e2ce5aa8d3f455cf00945f4afdf5ba27c93',
    'cbce27f51d31118633ef69d7ed74bdabca85cf7b6db80171f4c37557df1b7480',
    'bc743f866d697009aa56d30072ba40123e4cc2c4bab419e0569aa6bf19dd4c86',
    'fa6e302bace4eb4dbc269335afc9223f9a5e57db18f60210cc2dc3a8b0143b91',
    'cd90114c7f62e012f0b76679018066c26b9546307692751ebe9033e689ec9ccb',
    'a6b94e99ab3cc21d35bf581fb3288a2fa598ffbeced0fbb537293a111a56f0d1',
    'd23fe1abd62bd02dde953399ce11b479d1a63c4063def8037d47af0a6dc9ff39']
RUNTIME = Path('C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies')
VERSIONS = {'python': '3.12.14', 'pillow': '12.3.0', 'node': 'v24.19.0',
            'sharp': '0.35.4', 'rsvg': '2.62.91'}
PLACEMENT = {'x': 285, 'y': 198, 'width': 205}
EDIT_KERNEL = {'path': 'visual_memory/vpd_registered_type_edited_lineage.py',
               'sha256': 'a29d62e9888613594414c408233282fc3b29c5e724d576eaebc7c1bf81d014cd'}
EDIT_ADAPTER_V25 = {'path': 'visual_memory/vpd_registered_type_edited_lineage_v25.py',
                    'sha256': '0b4f33ae6f6c1aa4be585a4cdb5745398127ed9918880dc4d3031779a5394440'}
EDIT_ADAPTER_V26 = {'path': 'visual_memory/vpd_registered_type_edited_lineage_v26.py',
                    'sha256': 'cf10cace120bc2d369a633583895152924bcbd868ad8c9e8dc4bbba6803bb3d5'}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def ref(root, path):
    path = Path(path).resolve()
    return {'path': path.relative_to(Path(root).resolve()).as_posix(), 'sha256': sha(path.read_bytes())}


def checked_bytes(root, reference):
    require(isinstance(reference, dict), 'REFERENCE_REQUIRED')
    path = (Path(root) / reference['path']).resolve()
    require(path.is_relative_to(Path(root).resolve()), 'REFERENCE_OUTSIDE_REPOSITORY')
    raw = path.read_bytes()
    require(sha(raw) == reference['sha256'], 'REFERENCE_SHA_MISMATCH:' + reference['path'])
    return raw


def svg_tree(raw):
    """Finite path geometry only; no CSS, images, URLs, shapes, clips or filters."""
    require(b'<!' not in raw and b'<?' not in raw, 'SVG_DECLARATION_FORBIDDEN')
    root = ET.fromstring(raw)
    allowed = {'svg': {'width', 'height', 'viewBox', 'fill', 'version'},
               'g': {'id', 'transform', 'opacity'},
               'path': {'id', 'd', 'transform', 'fill', 'fill-rule', 'opacity', 'fill-opacity'},
               'title': set(), 'desc': set()}
    for node in root.iter():
        tag = node.tag.removeprefix(NS)
        require(node.tag.startswith(NS) and tag in allowed, 'SVG_ELEMENT_FORBIDDEN:' + tag)
        require(set(node.attrib) <= allowed[tag], 'SVG_ATTRIBUTE_FORBIDDEN:' + tag)
        if tag in ('title', 'desc'):
            require(not len(node), 'SVG_METADATA_CHILD_FORBIDDEN')
            continue
        require(not (node.text or '').strip() and not (node.tail or '').strip(), 'SVG_NON_METADATA_TEXT')
        for key, value in node.attrib.items():
            if key in ('width', 'height', 'viewBox', 'opacity', 'fill-opacity'):
                values = [float(v) for v in value.replace(',', ' ').split()]
                require(bool(values) and all(math.isfinite(v) for v in values), 'SVG_NONFINITE_NUMBER')
                if key in ('opacity', 'fill-opacity'):
                    require(len(values) == 1 and 0 <= values[0] <= 1, 'SVG_ALPHA_INVALID')
            elif key == 'transform':
                parts = re.findall(r'(matrix|translate|scale)\(([^()]*)\)', value)
                require(parts and re.sub(r'(matrix|translate|scale)\([^()]*\)', '', value).strip() == '',
                        'SVG_TRANSFORM_FORBIDDEN')
                for operation, numbers in parts:
                    nums = [float(v) for v in numbers.replace(',', ' ').split()]
                    require(len(nums) in {'matrix': (6,), 'translate': (1, 2), 'scale': (1, 2)}[operation]
                            and all(math.isfinite(v) for v in nums), 'SVG_TRANSFORM_INVALID')
            elif key == 'd':
                require(value.strip() and re.fullmatch(r'[MmLlHhVvCcSsQqTtAaZz0-9eE+.,\s-]+', value),
                        'SVG_PATH_COMMAND_INVALID')
            elif key == 'fill':
                require(value == 'none' if tag == 'svg' else value == '#F5F2E6', 'SVG_FILL_FORBIDDEN')
            elif key == 'fill-rule':
                require(value in ('nonzero', 'evenodd'), 'SVG_FILL_RULE_INVALID')
        if tag == 'path':
            require(node.get('d') and node.get('fill') == '#F5F2E6' and not len(node), 'FILLED_GLYPH_REQUIRED')
    require(root.tag == NS + 'svg', 'SVG_ROOT_REQUIRED')
    return root


def semantic_sha(root):
    return sha(json.dumps([(n.tag, sorted(n.attrib.items()), (n.text or '').strip())
                           for n in root.iter()], ensure_ascii=False, separators=(',', ':')).encode('utf-8'))


def renderer(root):
    env = {k: v for k, v in os.environ.items() if k.upper() not in {'NODE_PATH', 'NODE_OPTIONS'}}
    code = ('const s=require(' + json.dumps((RUNTIME / 'node/node_modules/sharp').as_posix())
            + ');console.log(JSON.stringify({node:process.version,sharp:s.versions.sharp,rsvg:s.versions.rsvg}));')
    observed = json.loads(subprocess.run([str(RUNTIME / 'node/bin/node.exe'), '-e', code],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env).stdout)
    observed.update(python='.'.join(map(str, sys.version_info[:3])), pillow=PIL.__version__)
    require(observed == VERSIONS, 'RENDERER_VERSION_CHANGED')
    # Execute the already verified bytes, never reread an unbound helper by run_path.
    filename = str(Path(root) / HELPER['path'])
    namespace = {'__file__': filename, '__name__': '_trusted_v18_render_helper'}
    exec(compile(checked_bytes(root, HELPER), filename, 'exec'), namespace)
    return namespace['render']


def edited_kernel(root, formal_version=24):
    require(type(formal_version) is int and formal_version in (24, 25, 26), 'INSPECTED_EDIT_VERSION_REQUIRED')
    reference = EDIT_ADAPTER_V26 if formal_version == 26 else EDIT_ADAPTER_V25 if formal_version == 25 else EDIT_KERNEL
    filename = str(Path(root) / reference['path'])
    namespace = {'__file__': filename, '__name__': '_trusted_v24_edit_kernel'}
    exec(compile(checked_bytes(root, reference), filename, 'exec'), namespace)
    return namespace


def edited_lineage(root, formal_version=24):
    """Construct a sealed actual profile; default V24 is retained byte-for-byte."""
    if formal_version == 26:
        return edited_kernel(root, 26)['expected_lineage'](root, EDIT_ADAPTER_V26)
    if formal_version == 25:
        return edited_kernel(root, 25)['expected_lineage'](root, EDIT_ADAPTER_V25)
    require(formal_version == 24, 'INSPECTED_EDIT_VERSION_REQUIRED')
    return edited_kernel(root)['expected_lineage'](EDIT_KERNEL)


def check_lineage(root, tree, lineage, formal_version=None):
    if lineage['kind'] == 'alpha128-vtracer-edited/v1':
        if formal_version == 26:
            return edited_kernel(root, 26)['validate'](root, tree, lineage, formal_version, EDIT_ADAPTER_V26)
        if formal_version == 25:
            return edited_kernel(root, 25)['validate'](root, tree, lineage, formal_version, EDIT_ADAPTER_V25)
        return edited_kernel(root)['validate'](root, tree, lineage, formal_version, EDIT_KERNEL)
    paths = list(tree.iter(NS + 'path'))
    checked_bytes(root, lineage['provenance'])
    if lineage['kind'] == 'source-han-serif-2.003':
        require(lineage['font']['sha256'] == FONT_SHA, 'FONT_SOURCE_CHANGED')
        checked_bytes(root, lineage['font'])
        require([sha(p.get('d').encode('utf-8')) for p in paths] == FONT_COMMAND_SHAS,
                'FONT_GLYPH_COMMANDS_CHANGED')
        return
    require(lineage['kind'] == 'alpha128-vtracer', 'HEADLINE_LINEAGE_UNSUPPORTED')
    checked_bytes(root, lineage['generation_evidence'])
    generated = Image.open(io.BytesIO(checked_bytes(root, lineage['generated_png'])))
    require(generated.format == 'PNG' and generated.mode == 'RGBA', 'GENERATED_ALPHA_PNG_REQUIRED')
    minimum, maximum = generated.getchannel('A').getextrema()
    require(minimum == 0 and maximum >= 128, 'TRANSPARENT_LETTERING_ALPHA_REQUIRED')
    source_trace = ET.fromstring(checked_bytes(root, lineage['trace_svg']))
    dependency = Path(root) / '.liu-visual-private/dependencies/vtracer_0_6_15_cp312/site-packages'
    sys.path.insert(0, str(dependency))
    try:
        import vtracer
        require(importlib.metadata.version('vtracer') == '0.6.15', 'VTRACER_VERSION_CHANGED')
        binary = generated.getchannel('A').point(lambda v: 0 if v >= 128 else 255).convert('RGB')
        buffer = io.BytesIO()
        binary.save(buffer, format='PNG')
        replay = vtracer.convert_raw_image_to_svg(buffer.getvalue(), img_format='png', colormode='binary',
            mode='spline', filter_speckle=0, corner_threshold=60, length_threshold=4.0,
            max_iterations=10, splice_threshold=45, path_precision=3)
    finally:
        sys.path.remove(str(dependency))
    original = list(source_trace)
    require(all(n.tag == NS + 'path' for n in original), 'TRACE_PATHS_REQUIRED')
    require([dict(n.attrib) for n in original] == [dict(n.attrib) for n in ET.fromstring(replay)],
            'GENERATED_ALPHA_TRACE_MISMATCH')
    retained = [n for n in original if n.get('d', '').strip()]
    require([(p.get('d'), p.get('transform')) for p in paths]
            == [(p.get('d'), p.get('transform')) for p in retained], 'TRACE_GLYPH_COMMANDS_CHANGED')


def brand_canvas(raw):
    tree = svg_tree(raw)
    require(len(list(tree.iter(NS + 'path'))) == 7, 'FROZEN_BRAND_PATHS_CHANGED')
    scale = PLACEMENT['width'] / float(tree.get('width'))
    canvas = ET.Element(NS + 'svg', {'width': '1536', 'height': '1024', 'viewBox': '0 0 1536 1024'})
    group = ET.SubElement(canvas, NS + 'g', {'transform': f'translate(285 198) scale({scale})'})
    for child in tree:
        group.append(copy.deepcopy(child))
    return ET.tostring(canvas)


def register(root, formal_version, headline_ref, lineage):
    """In-memory registration. Root must review and freeze its returned bytes/ref."""
    require(type(formal_version) is int and formal_version >= 22, 'PROSPECTIVE_V22_REQUIRED')
    checked_bytes(root, SOURCE)
    headline = svg_tree(checked_bytes(root, headline_ref))
    require([headline.get(k) for k in ('width', 'height', 'viewBox')] == ['1536', '1024', '0 0 1536 1024'],
            'HEADLINE_CANVAS_CHANGED')
    check_lineage(root, headline, lineage, formal_version)
    render = renderer(root)
    layers = []
    for role, reference, raw in [('brand', BRAND, brand_canvas(checked_bytes(root, BRAND))),
                                ('headline', headline_ref, ET.tostring(headline))]:
        image = render(raw)
        require(image.size == SIZE and image.mode == 'RGBA' and image.getchannel('A').getbbox(),
                'REGISTERED_LETTERING_EMPTY_OR_WRONG_SIZE')
        layers.append({'role': role, 'svg': reference, 'semantic_sha256': semantic_sha(svg_tree(raw)),
                       'rgba_sha256': sha(image.tobytes()), 'alpha_sha256': sha(image.getchannel('A').tobytes())})
    return {'schema': SCHEMA, 'formal_version': formal_version, 'copy': COPY, 'brand': '茶作',
            'dimensions': list(SIZE), 'source': SOURCE, 'renderer_helper': HELPER, 'renderer': VERSIONS,
            'brand_placement': PLACEMENT, 'layer_order': ['brand', 'headline'], 'layers': layers,
            'headline_lineage': lineage, 'core_map': CORE,
            'composite': 'Pillow12.3.0 RGBA source-over in stored 8-bit channels; brand then headline; opaque RGB output'}


def replay(root, registration_ref):
    registration = json.loads(checked_bytes(root, registration_ref))
    require(registration['schema'] == SCHEMA, 'REGISTRATION_SCHEMA_REQUIRED')
    fresh = register(root, registration['formal_version'], registration['layers'][1]['svg'],
                     registration['headline_lineage'])
    require(fresh == registration, 'REGISTERED_LAYER_REPLAY_MISMATCH')
    render = renderer(root)
    overlay = Image.new('RGBA', SIZE)
    for layer in registration['layers']:
        raw = checked_bytes(root, layer['svg'])
        overlay.alpha_composite(render(brand_canvas(raw) if layer['role'] == 'brand' else raw))
    source = Image.open(io.BytesIO(checked_bytes(root, SOURCE))).convert('RGBA')
    require(source.size == SIZE and source.getchannel('A').getextrema() == (255, 255), 'SOURCE_SIZE_OR_ALPHA_CHANGED')
    expected = source.copy()
    # Sequential source-over is intentional; do not collapse layers (rounding differs).
    for layer in registration['layers']:
        raw = checked_bytes(root, layer['svg'])
        expected.alpha_composite(render(brand_canvas(raw) if layer['role'] == 'brand' else raw))
    return expected.convert('RGB'), overlay, registration


def pixel_difference(a, b, mask=None):
    diff = ImageChops.difference(a.convert('RGB'), b.convert('RGB'))
    maximum = max(channel.getextrema()[1] for channel in diff.split())
    any_channel = ImageChops.lighter(ImageChops.lighter(diff.getchannel('R'), diff.getchannel('G')), diff.getchannel('B'))
    if mask is not None:
        any_channel = ImageChops.darker(any_channel, mask)
        maximum = any_channel.getextrema()[1]
    return {'pixels': sum(any_channel.histogram()[1:]), 'max_channel_difference': maximum}


def core_mask(root):
    core = json.loads(checked_bytes(root, CORE))
    checked_bytes(root, core['mask_asset'])
    require(core['source_sha256'] == SOURCE['sha256'] and core['dimensions'] == list(SIZE)
            and core['pixels'] == 162052, 'FIXED_CORE_CHANGED')
    mask = Image.new('L', SIZE)
    for y, intervals in core['rows']:
        for x0, x1 in intervals:
            mask.paste(255, (x0, y, x1, y + 1))
    require(sum(mask.histogram()[1:]) == 162052, 'FIXED_CORE_PIXEL_COUNT_CHANGED')
    return mask


def png_image(root, reference, enforce_source_profile=True):
    im = Image.open(io.BytesIO(checked_bytes(root, reference)))
    require(im.format == 'PNG' and im.size == SIZE and im.mode in ('RGB', 'RGBA')
            and getattr(im, 'n_frames', 1) == 1, 'OPAQUE_FULL_FRAME_PNG_REQUIRED')
    require(im.convert('RGBA').getchannel('A').getextrema() == (255, 255), 'FINAL_TRANSPARENCY_FORBIDDEN')
    original = Image.open(io.BytesIO(checked_bytes(root, SOURCE)))
    require(not enforce_source_profile or all(im.info.get(k) == original.info.get(k) for k in ('icc_profile', 'gamma', 'srgb')),
            'UNREGISTERED_PNG_COLOR_PROFILE')
    return im.convert('RGB')


def compare_pixels(root, registration_ref, final_ref, figma_raw_ref=None):
    """Control-only if figma_raw_ref is absent; this does not authenticate Figma."""
    expected, overlay, registration = replay(root, registration_ref)
    final = png_image(root, final_ref)
    source = Image.open(io.BytesIO(checked_bytes(root, SOURCE))).convert('RGB')
    zero = overlay.getchannel('A').point(lambda v: 255 if v == 0 else 0)
    covered = ImageChops.invert(zero)
    core = core_mask(root)
    result = {'schema': 'vpd-registered-type-composite-check/v1', 'formal_version': registration['formal_version'],
              'registration': registration_ref, 'source': SOURCE, 'final': final_ref,
              'whole_frame_expected': pixel_difference(final, expected),
              'alpha_zero_source': pixel_difference(final, source, zero),
              'alpha_positive_expected': pixel_difference(final, expected, covered),
              'core_pixels': 162052, 'core_alpha_zero_pixels': sum(ImageChops.darker(core, zero).histogram()[1:]),
              'core_alpha_positive_pixels': sum(ImageChops.darker(core, covered).histogram()[1:]),
              'core_alpha_zero_source': pixel_difference(final, source, ImageChops.darker(core, zero)),
              'core_alpha_positive_expected': pixel_difference(final, expected, ImageChops.darker(core, covered)),
              'figma_authenticity_verified_offline': False, 'aesthetic_pass_claimed': False}
    require(all(result[k]['pixels'] == 0 for k in ('whole_frame_expected', 'alpha_zero_source',
        'alpha_positive_expected', 'core_alpha_zero_source', 'core_alpha_positive_expected')),
        'UNEXPLAINED_COMPOSITE_PIXEL_CHANGE')
    if figma_raw_ref is not None:
        result['figma_raw'] = figma_raw_ref
        result['figma_raw_to_final'] = pixel_difference(png_image(root, figma_raw_ref, enforce_source_profile=False), final)
        raw_image = Image.open(io.BytesIO(checked_bytes(root, figma_raw_ref)))
        result['figma_raw_color_metadata'] = {k: (sha(v) if isinstance(v, bytes) else v)
            for k, v in raw_image.info.items() if k in ('icc_profile', 'gamma', 'srgb')}
        result['figma_difference_semantics'] = 'Stored 8-bit RGB channels; raw Figma color metadata recorded separately; no ICC perceptual equivalence claimed.'
        result['figma_raw_bytes_equal_final'] = checked_bytes(root, figma_raw_ref) == checked_bytes(root, final_ref)
    else:
        result['scope'] = 'OFFLINE_CONTROL_ONLY_NO_ACTUAL_FIGMA_BINDING'
    return result
