"""V24's finite JSON contour editor; no maker program or arbitrary SVG is run.

The authoring entry point replays actual alpha128 input, explicit contour edits,
positive per-glyph pose, and two fixed Bezier exclusion envelopes. Registration
additionally requires the sealed actual manifest/profile. Neither proves copy
recognition, generated-image semantics, Figma authenticity, or visual quality.
"""
from pathlib import Path
import copy
import hashlib
import io
import json
import math
import re
import sys
import xml.etree.ElementTree as ET

from PIL import Image

NS = '{http://www.w3.org/2000/svg}'
ET.register_namespace('', NS[1:-1])
KIND = 'alpha128-vtracer-edited/v1'
SCHEMA = 'vpd-source-bound-glyph-edits/v1'
COPY = '一杯茶，慢下来'
BASE = 'evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v24/'
DEPDIR = '.liu-visual-private/dependencies/skia_pathops_0_9_2_abi3/'
INPUTS = {
    'generated_png': {'path': '.liu-visual-private/correct_source_typography/v24/headline-generated-01.png',
        'sha256': '34b9b720d7d39b85c48d36220d2d53e4261d4ee88a5c27056fa796a52c39f774'},
    'trace_svg': {'path': BASE + 'upstream-alpha128-trace.svg',
        'sha256': '46344044630cd58081d3ce1520b34dc8665b574fcdf0f35179a208a818b47571', 'bytes': 37932},
    'generation_evidence': {'path': BASE + 'IMAGEGEN_EXECUTION.json',
        'sha256': 'd4865c9e43454f230047e05b5c831c00ba7696f5f52df64e7e840d47ab36ffb0'},
    'provenance': {'path': BASE + 'SOURCE_TRACE.json',
        'sha256': '0052bbf8ef4472e05d54eac79695b7a3eadf8fe687b7f842a75983fd9bf05378'},
    'source_commands': {'path': BASE + 'TRACE_COMMANDS.json',
        'sha256': 'e95467a5af1a3ee19eac5dced61ccf94e616f185e3cb0565cadb86b40a497a63'},
    'art_direction': {'path': BASE + 'ART_DIRECTION.json',
        'sha256': '5fa2a8203ca957d1732fc2c02477faf41d27015813135e87879409c2438ed945', 'bytes': 7037},
    'trace_builder': {'path': BASE + 'trace_source_once.py',
        'sha256': '45f7eb01e6863601bd9e4ffe0c8d07bb851f0809d7566afefbf8b415996d52a7'},
}
# Actual maker output is sealed once complete, never supplied as its own authority.
SEALED_EDIT = {'path': BASE + 'V24_GLYPH_EDIT_MANIFEST.json',
               'sha256': '4ab54d352c45202a8ca8d13fdc12311950c3bd48181da4be0d9ec33b22216cc3'}
SEALED_MAKER = {'path': BASE + 'make_glyph_program.py',
                'sha256': 'bfe62e36f12c31a2b3581d61bf0adc8453abaa8bb88b950be1a522ba540690ca'}
SEALED_BUILDER = {'path': BASE + 'build_headline_asset.py',
                  'sha256': 'ef8dfd533e8de9ef1d0f93b3d4ad3059156bd07ccbb817b692c02960b0ae0855'}
PATHOPS_FILES = {
    'pathops/__init__.py': '4a5c51dbc66a8c643c0ac183f9b8808c8c73c260ea0c403072be8917743446ce',
    'pathops/_pathops.pyd': '31378f0d26e850eeb73249b73c0e208836bc0b6e004551fafed3e69dfdbc38aa',
    'pathops/_version.py': '62185f19724d16d672544bbc62ec156c2a79bf2baf3c6942a19a8485f1dd712f',
    'pathops/operations.py': '2ccd482ae0d04da22b020de64b852b71cefddc5efbf5800d1e6f552b0edb4b7a',
    'pathops/skia.dll': 'b22fa4d5f9b9293b7221ca3b1802e4983f06f769340fc8f1ce79f81bb1aac819',
}
VT = '.liu-visual-private/dependencies/vtracer_0_6_15_cp312/'
VTRACER_FILES = {
    'vtracer/__init__.py': '3e697358d7fb4a880b60fc279864b6f30e619807c183f2b54ccbd81c5d78d2f2',
    'vtracer/vtracer.cp312-win_amd64.pyd': '59e2053fca8666479e7163eec45d8b15143435c7a8d14f6dbd26eec9716bfe66',
}
OWNERSHIP = [[4], [0, 2, 6], [1, 3, 5, 8, 9], [7], [11, 12, 15, 16], [13], [10, 14]]
FLAGS = {'fix_winding': True, 'keep_starting_points': True, 'clockwise': False}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def commands_sha(commands):
    return sha(json.dumps(commands, ensure_ascii=False, sort_keys=True,
        separators=(',', ':'), allow_nan=False).encode('utf-8'))


def checked(root, reference):
    require(isinstance(reference, dict), 'EDIT_REFERENCE_REQUIRED')
    path = (Path(root) / reference['path']).resolve()
    require(path.is_relative_to(Path(root).resolve()), 'EDIT_REFERENCE_OUTSIDE_REPOSITORY')
    raw = path.read_bytes()
    require(sha(raw) == reference['sha256'], 'EDIT_REFERENCE_SHA_MISMATCH:' + reference['path'])
    return raw


def load_bound(root, name, directory, files):
    directory = (Path(root) / directory / 'site-packages').resolve()
    for filename, digest in files.items():
        require(sha((directory / filename).read_bytes()) == digest, 'EDIT_DEPENDENCY_CHANGED:' + filename)
    for module_name, module in tuple(sys.modules.items()):
        if module_name == name or module_name.startswith(name + '.'):
            require(hasattr(module, '__file__') and Path(module.__file__).resolve().is_relative_to(directory / name),
                    'EDIT_DEPENDENCY_WRONG_IMPORT:' + module_name)
    sys.path.insert(0, str(directory))
    try:
        return __import__(name)
    finally:
        sys.path.remove(str(directory))


def pathops_runtime(root):
    wheel = Path(root) / DEPDIR / 'skia_pathops-0.9.2-cp310-abi3-win_amd64.whl'
    require(sha(wheel.read_bytes()) == '9ae72d801b5f4c5dbb937fb25476a12fa2da70860f28dd637da2b529dbd8271c',
            'PATHOPS_WHEEL_CHANGED')
    library = load_bound(root, 'pathops', DEPDIR, PATHOPS_FILES)
    require(library.__version__ == '0.9.2' and sys.version_info[:3] == (3, 12, 14),
            'EDIT_RUNTIME_VERSION_CHANGED')
    return library


def parse_closed(d, translate=(0.0, 0.0)):
    """Only explicit absolute M/L/C/Z; source VTracer emits precisely M/C/Z."""
    token = r'[MLCZ]|[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?'
    require(not re.sub(token, '', d).replace(',', '').strip(), 'EDIT_PATH_SYNTAX_FORBIDDEN')
    values = re.findall(token, d)
    contours, current = [], []
    i, operation, endpoint, start = 0, None, None, None
    mapping = {'M': ('moveTo', 1), 'L': ('lineTo', 1), 'C': ('curveTo', 3)}
    while i < len(values):
        if values[i] in 'MLCZ':
            operation = values[i]
            i += 1
        require(operation is not None, 'EDIT_PATH_COMMAND_REQUIRED')
        if operation == 'Z':
            require(current and start is not None, 'EDIT_PATH_CLOSE_WITHOUT_MOVE')
            # Match normalized SVG closure rather than hide an implied final line.
            if endpoint != start:
                current.append({'op': 'lineTo', 'points': [list(start)]})
            current.append({'op': 'closePath', 'points': []})
            contours.append(current)
            current, endpoint, start, operation = [], None, None, None
            continue
        opname, count = mapping[operation]
        require(i + 2 * count <= len(values), 'EDIT_PATH_POINT_MISSING')
        points = []
        for unused in range(count):
            x, y = float(values[i]), float(values[i + 1])
            require(math.isfinite(x) and math.isfinite(y), 'EDIT_POINT_NONFINITE')
            points.append([x + translate[0], y + translate[1]])
            i += 2
        if operation == 'M':
            require(not current, 'EDIT_PATH_PREVIOUS_CONTOUR_OPEN')
            start = tuple(points[0])
            operation = 'L'
        else:
            require(current, 'EDIT_PATH_MOVE_REQUIRED')
        endpoint = tuple(points[-1])
        current.append({'op': opname, 'points': points})
    require(not current, 'EDIT_PATH_CONTOUR_OPEN')
    return contours


def source_contours(root):
    generated = Image.open(io.BytesIO(checked(root, INPUTS['generated_png'])))
    require(generated.format == 'PNG' and generated.mode == 'RGBA' and generated.size == (1774, 887),
            'EDIT_SOURCE_ALPHA_PNG_REQUIRED')
    minimum, maximum = generated.getchannel('A').getextrema()
    require(minimum == 0 and maximum >= 128, 'EDIT_SOURCE_TRANSPARENCY_REQUIRED')
    wheel = Path(root) / VT / 'vtracer-0.6.15-cp312-cp312-win_amd64.whl'
    require(sha(wheel.read_bytes()) == 'b0f08b66734e41872d4ac343ed6d08870b3235346def3e112e10b3b2443e619e',
            'EDIT_VTRACER_WHEEL_CHANGED')
    vtracer = load_bound(root, 'vtracer', VT, VTRACER_FILES)
    binary = generated.getchannel('A').point(lambda v: 0 if v >= 128 else 255).convert('RGB')
    buffer = io.BytesIO()
    binary.save(buffer, format='PNG')
    trace = vtracer.convert_raw_image_to_svg(buffer.getvalue(), img_format='png', colormode='binary',
        mode='spline', filter_speckle=0, corner_threshold=60, length_threshold=4.0,
        max_iterations=10, splice_threshold=45, path_precision=3)
    original = ET.fromstring(checked(root, INPUTS['trace_svg']))
    actual = ET.fromstring(trace)
    require(original.attrib == actual.attrib and [(n.tag, n.attrib) for n in original]
            == [(n.tag, n.attrib) for n in actual], 'EDIT_GENERATED_ALPHA_TRACE_MISMATCH')
    records = json.loads(checked(root, INPUTS['source_commands']))
    result = []
    for index, node in enumerate(original):
        require(node.tag == NS + 'path', 'EDIT_SOURCE_PATH_REQUIRED')
        match = re.fullmatch(r'translate\(([-.\d]+),([-.\d]+)\)', node.get('transform', ''))
        require(match, 'EDIT_SOURCE_TRANSLATION_REQUIRED')
        contours = parse_closed(node.get('d', ''), tuple(map(float, match.groups())))
        require(contours == records['paths'][index]['closed_contours'], 'EDIT_SOURCE_NORMALIZATION_MISMATCH')
        result.append(contours)
    require(len(result) == 17 and records['path_count'] == 17, 'EDIT_SOURCE_PATH_COUNT_CHANGED')
    return result


def finite_point(point):
    require(isinstance(point, list) and len(point) == 2 and
        all(type(v) in (int, float) and math.isfinite(v) for v in point), 'EDIT_POINT_INVALID')


def closed_commands(commands):
    require(isinstance(commands, list) and len(commands) >= 3 and commands[0]['op'] == 'moveTo'
            and commands[-1]['op'] == 'closePath', 'EDIT_CLOSED_CONTOUR_REQUIRED')
    counts = {'moveTo': 1, 'lineTo': 1, 'curveTo': 3, 'closePath': 0}
    for index, command in enumerate(commands):
        require(set(command) == {'op', 'points'} and command['op'] in counts
                and isinstance(command['points'], list) and len(command['points']) == counts[command['op']],
                'EDIT_COMMAND_INVALID')
        require(command['op'] not in ('moveTo', 'closePath') or index in (0, len(commands) - 1),
                'EDIT_CONTOUR_COMMAND_ORDER')
        for point in command['points']:
            finite_point(point)


def make_path(library, contours, placement=None):
    path = library.Path()
    pen = path.getPen()
    for contour in contours:
        closed_commands(contour)
        for command in contour:
            points = command['points']
            if placement:
                points = [[placement['scale'] * x + placement['tx'], placement['scale'] * y + placement['ty']]
                          for x, y in points]
            getattr(pen, command['op'])(*[tuple(p) for p in points])
    return path


def path_d(path):
    letters = {'moveTo': 'M', 'lineTo': 'L', 'curveTo': 'C', 'closePath': 'Z'}
    parts = []
    for operation, points in path.segments:
        require(operation in letters, 'EDIT_BOOLEAN_UNEXPECTED_COMMAND')
        parts.append(letters[operation] + ' '.join(format(float(v), '.9g') for p in points for v in p))
    return ' '.join(parts)


def replay_edit_program(root, manifest):
    """Authoring replay; writes nothing and grants no registration or taste PASS."""
    require(set(manifest) == {'schema', 'formal_version', 'copy', 'source_trace', 'glyphs', 'negative_space'},
            'EDIT_MANIFEST_FIELDS_INVALID')
    require(manifest['schema'] == SCHEMA and manifest['formal_version'] == 24 and manifest['copy'] == COPY,
            'EDIT_MANIFEST_IDENTITY_CHANGED')
    require(manifest['source_trace'] == INPUTS['trace_svg'], 'EDIT_SOURCE_TRACE_BINDING_CHANGED')
    source = source_contours(root)
    library = pathops_runtime(root)
    space = manifest['negative_space']
    require(space == {'art_direction': INPUTS['art_direction'], 'operation': 'difference-union', **FLAGS},
            'EDIT_EXCLUSION_PARAMETERS_CHANGED')
    direction = json.loads(checked(root, INPUTS['art_direction']))
    cup = make_path(library, parse_closed(direction['negative_space']['cup_air']))
    leaf = make_path(library, parse_closed(direction['negative_space']['leaf_air']))
    air = library.op(cup, leaf, library.PathOp.UNION, **FLAGS)
    require(isinstance(manifest['glyphs'], list) and [g['char'] for g in manifest['glyphs']] == list(COPY),
            'EDIT_COPY_OWNERSHIP_CHANGED')
    svg = ET.Element(NS + 'svg', {'width': '1536', 'height': '1024', 'viewBox': '0 0 1536 1024'})
    report = {'schema': 'vpd-source-bound-glyph-edit-replay/v1', 'formal_version': 24,
              'source_path_count': 17, 'approximation': 'alpha128/VTracer spline then Skia float32 Bezier operations',
              'font_files_loaded': 0, 'maker_program_executed': False, 'aesthetic_pass_claimed': False, 'glyphs': []}
    assigned = set()
    for index, glyph in enumerate(manifest['glyphs']):
        require(set(glyph) == {'char', 'source', 'edits', 'placement'}, 'EDIT_GLYPH_FIELDS_INVALID')
        rows = glyph['source']
        require([r['path_index'] for r in rows] == OWNERSHIP[index], 'EDIT_GLYPH_SOURCE_OWNERSHIP_CHANGED')
        local = {}
        for row in rows:
            require(set(row) == {'path_index', 'contour_indices'}, 'EDIT_SELECTOR_FIELDS_INVALID')
            pi = row['path_index']
            require(row['contour_indices'] == list(range(len(source[pi]))), 'EDIT_SOURCE_CONTOUR_OMITTED')
            for ci in row['contour_indices']:
                require((pi, ci) not in assigned, 'EDIT_SOURCE_CONTOUR_DUPLICATE')
                assigned.add((pi, ci))
                local[(pi, ci)] = [copy.deepcopy(source[pi][ci])]
        replaced, changes = set(), []
        require(isinstance(glyph['edits'], list), 'EDIT_OPERATION_LIST_REQUIRED')
        for edit in glyph['edits']:
            require(type(edit['path_index']) is int and type(edit['contour_index']) is int,
                    'EDIT_SELECTOR_INTEGER_REQUIRED')
            selector = (edit['path_index'], edit['contour_index'])
            require(selector in local and selector not in replaced, 'EDIT_SELECTOR_INVALID_OR_REPLACED')
            before = local[selector][0]
            if edit['op'] == 'set_point':
                require(set(edit) == {'op', 'path_index', 'contour_index', 'command_index', 'point_index', 'before', 'after'},
                        'EDIT_SET_POINT_FIELDS_INVALID')
                finite_point(edit['before']); finite_point(edit['after'])
                require(type(edit['command_index']) is int and type(edit['point_index']) is int
                    and 0 <= edit['command_index'] < len(before), 'EDIT_POINT_SELECTOR_INVALID')
                points = before[edit['command_index']]['points']
                require(0 <= edit['point_index'] < len(points) and points[edit['point_index']] == edit['before'],
                        'EDIT_BEFORE_POINT_MISMATCH')
                points[edit['point_index']] = copy.deepcopy(edit['after'])
            elif edit['op'] == 'replace_contour':
                require(set(edit) == {'op', 'path_index', 'contour_index', 'before_sha256', 'after_contours', 'reason'},
                        'EDIT_REPLACE_FIELDS_INVALID')
                require(commands_sha(before) == edit['before_sha256'], 'EDIT_BEFORE_CONTOUR_MISMATCH')
                require(isinstance(edit['reason'], str) and edit['reason'].strip(), 'EDIT_REDESIGN_REASON_REQUIRED')
                require(isinstance(edit['after_contours'], list), 'EDIT_AFTER_CONTOURS_REQUIRED')
                for contour in edit['after_contours']:
                    closed_commands(contour)
                local[selector] = copy.deepcopy(edit['after_contours'])
                replaced.add(selector)
            else:
                raise ValueError('EDIT_OPERATION_FORBIDDEN:' + str(edit['op']))
            changes.append(copy.deepcopy(edit))
        placement = glyph['placement']
        require(set(placement) == {'scale', 'tx', 'ty'} and all(type(v) in (int, float) and math.isfinite(v)
            for v in placement.values()) and placement['scale'] > 0, 'EDIT_PLACEMENT_INVALID')
        contours = [contour for group in local.values() for contour in group]
        before = make_path(library, [c for row in rows for c in source[row['path_index']]], placement)
        edited = make_path(library, contours, placement)
        # Simplify resolves each glyph's overlapping strokes with nonzero winding.
        pre = library.simplify(edited, **FLAGS)
        post = library.op(pre, air, library.PathOp.DIFFERENCE, **FLAGS)
        require(post.area > 0, 'EDIT_GLYPH_EMPTY_AFTER_EXCLUSION')
        d = path_d(post)
        ET.SubElement(svg, NS + 'path', {'id': 'glyph-' + str(index), 'd': d,
                                      'fill': '#F5F2E6', 'fill-rule': 'nonzero'})
        report['glyphs'].append({'char': glyph['char'], 'source_contours': len(local),
            'source_posed_d': path_d(before), 'edited_contours': contours, 'changes': changes,
            'pre_difference_d': path_d(pre), 'post_difference_d': d,
            'pre_area': pre.area, 'post_area': post.area, 'removed_area': pre.area - post.area,
            'bounds': list(post.bounds), 'output_contours': sum(1 for unused in post.contours)})
    require(assigned == {(pi, ci) for pi, contours in enumerate(source) for ci in range(len(contours))},
            'EDIT_SOURCE_CONTOUR_ACCOUNTING_CHANGED')
    return ET.tostring(svg, encoding='utf-8'), report


def expected_lineage(kernel_reference):
    require(SEALED_EDIT is not None and SEALED_MAKER is not None and SEALED_BUILDER is not None,
            'V24_EDIT_PROFILE_NOT_SEALED')
    return {'kind': KIND, **copy.deepcopy(INPUTS), 'edit_manifest': copy.deepcopy(SEALED_EDIT),
            'maker_source': copy.deepcopy(SEALED_MAKER), 'maker_builder': copy.deepcopy(SEALED_BUILDER),
            'edit_kernel': kernel_reference}


def validate(root, tree, lineage, formal_version, kernel_reference):
    require(formal_version == 24, 'EDIT_LINEAGE_V24_ONLY')
    require(lineage == expected_lineage(kernel_reference), 'V24_EDIT_PROFILE_CHANGED')
    for key, value in lineage.items():
        if key != 'kind':
            checked(root, value)
    raw, report = replay_edit_program(root, json.loads(checked(root, SEALED_EDIT)))
    # All attributes, order and visible metadata are exact, not merely shape hashes.
    def semantic(node):
        return [(n.tag, sorted(n.attrib.items()), (n.text or '').strip(), (n.tail or '').strip()) for n in node.iter()]
    require(semantic(tree) == semantic(ET.fromstring(raw)), 'EDIT_FINAL_SVG_REPLAY_MISMATCH')
    return report
