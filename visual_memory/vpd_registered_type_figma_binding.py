"""Actual V22 Figma creation proof, independently checked from host tool events.

Only the already inspected collector invocation is supported. A future collector
or unavailable host runtime fails closed, rather than trusting an attestation.
Coordinate precision covers float32 storage and official SVG decimal export;
there is no RGB tolerance. This is not an aesthetic or operating-system proof.
"""
from pathlib import Path
import json
import math
import re
import struct
import sys
import xml.etree.ElementTree as ET

from . import vpd_registered_type_composite as g

FONTTOOLS_PATH = 'C:/Users/Administrator/AppData/Local/hermes/hermes-agent/venv/Lib/site-packages'
sys.path.append(FONTTOOLS_PATH)
try:
    import fontTools
    from fontTools.misc.transform import Transform
    from fontTools.pens.recordingPen import RecordingPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.svgLib.path import parse_path
finally:
    sys.path.remove(FONTTOOLS_PATH)

FILE_KEY = 'uyDxOoN1iNDPpEHTKSUWg1'
PHOTO_HASH = '074a11ff4345752bae19150e799d9cae49518b8b'
SCRIPT_SHA = '79f8c946643aa21c22b62eae5b5a3ab5d92b0a29b9bb7fa99811c0b01c917607'
PREFIX_INPUT_SHA = '5b8c5ce6b5827d6d7d5f55f5a32b0725bcf545c1cc66a95982e01da8125306f1'
BINDING_INPUT_SHA = '2c2b5c64e546c82ef953827ccc93c76bada5e491c292155dcd4faeef93074797'
BINDING_OUTPUT_SHA = '000eecf16b00575e581d642c46c18b73f2a3e188c1d50119da63084aec7d5430'
DOWNLOAD_INPUT_SHA = 'bc3a89b2425461d4d79767dc4ae153a2eac2d6af99566e7713da0c3dc70c91ba'
DOWNLOAD_OUTPUT_SHA = 'e59137f676f4e9d4cbe85fd83ccf130268ac89b78fd0ba016e4abc3bfb3ae1a8'
DOWNLOAD_CALL = 'call_eDqQE83Jz6MLz0Euv0i5ecFR'
DOWNLOAD_WAIT = 'call_M2LSEz5elSk0LW5TJQlLEkTf'
DOWNLOAD_TOOL_RESULT = {'path': '.liu-visual-private/correct_source_typography/v22/figma-download-tool-result.json',
                        'sha256': '78b567f72c6b3e80a759d91732f216ed04f8287ba1438d2ab69ba7cb7f5a2b6c'}
IDENTITY = [[1, 0, 0], [0, 1, 0]]


def f32(value):
    return struct.unpack('<f', struct.pack('<f', value))[0]


def ulp32(value):
    value = abs(f32(value))
    bits = struct.unpack('<I', struct.pack('<f', value))[0]
    return struct.unpack('<f', struct.pack('<I', bits + 1))[0] - value


def finite(value):
    return type(value) in (int, float) and math.isfinite(value)


def json_file(root, reference):
    return json.loads(g.checked_bytes(root, reference))


def json_outputs(event):
    for item in event['payload']['output']:
        if item.get('type') == 'input_text':
            try:
                yield json.loads(item['text'])
            except json.JSONDecodeError:
                pass


def tool_result(event):
    results = [j for j in json_outputs(event) if isinstance(j, dict)
               and j.get('isError') is False and isinstance(j.get('content'), list)]
    g.require(len(results) == 1, 'ACTUAL_MCP_RESULT_REQUIRED')
    return results[0]


def runtime_proof(root, evidence):
    g.require(evidence.get('schema') == 'vpd-figma-binding-runtime-evidence/v1'
              and evidence.get('formal_version') == 22, 'ACTUAL_RUNTIME_EVIDENCE_REQUIRED')
    host = Path(evidence['root_rollout_host_path']).resolve()
    sessions = Path('C:/Users/Administrator/.codex/sessions').resolve()
    g.require(host.is_relative_to(sessions) and host.suffix == '.jsonl', 'ACTUAL_HOST_RUNTIME_REQUIRED')
    ids = {evidence['prefix_call_id'], evidence['binding_call_id'], DOWNLOAD_CALL, DOWNLOAD_WAIT}
    calls, outputs, metadata = {}, {}, None
    with host.open(encoding='utf-8') as stream:
        for line in stream:
            event = json.loads(line)
            payload = event.get('payload', {})
            if event['type'] == 'session_meta':
                metadata = payload
            call_id = payload.get('call_id')
            if call_id not in ids:
                continue
            if payload.get('type') in ('custom_tool_call', 'function_call'):
                g.require(call_id not in calls, 'DUPLICATE_RUNTIME_CALL')
                calls[call_id] = event
            elif payload.get('type') in ('custom_tool_call_output', 'function_call_output'):
                g.require(call_id not in outputs, 'DUPLICATE_RUNTIME_OUTPUT')
                outputs[call_id] = event
    g.require(metadata and Path(metadata['cwd']).resolve() in (Path(root).resolve(), Path(root).resolve().parent)
              and set(calls) == ids and set(outputs) == ids, 'COMPLETE_REAL_RUNTIME_REQUIRED')
    prefix, binding = calls[evidence['prefix_call_id']], calls[evidence['binding_call_id']]
    for event, expected in ((prefix, PREFIX_INPUT_SHA), (binding, BINDING_INPUT_SHA),
                            (calls[DOWNLOAD_CALL], DOWNLOAD_INPUT_SHA)):
        g.require(event['payload'].get('name') == 'exec'
                  and g.sha(event['payload']['input'].encode('utf-8')) == expected,
                  'INSPECTED_ACTUAL_COLLECTOR_INVOCATION_REQUIRED')
    g.require(binding['timestamp'] == evidence['binding_call_timestamp']
              and evidence['binding_call_input_sha256'] == BINDING_INPUT_SHA,
              'ACTUAL_BINDING_CALL_IDENTITY_CONFLICT')
    returned = outputs[evidence['binding_call_id']]
    output_sha = g.sha(json.dumps(returned['payload']['output'], ensure_ascii=False, sort_keys=True).encode('utf-8'))
    g.require(output_sha == evidence['binding_output_sha256'] == BINDING_OUTPUT_SHA,
              'ACTUAL_BINDING_OUTPUT_CONFLICT')
    excerpt = json_file(root, evidence['private_exact_runtime_excerpt'])
    g.require(excerpt == [prefix, outputs[evidence['prefix_call_id']], binding, returned],
              'EXCERPT_DOES_NOT_MATCH_REAL_HOST_RUNTIME')
    # Reconstruct code:script from the actual earlier store and literal strings.
    decoder = json.JSONDecoder()
    pre, _ = decoder.raw_decode(prefix['payload']['input'][len('const pre='):])
    sha_code, _ = decoder.raw_decode(binding['payload']['input'][len('const shaCode='):])
    marker = 'const script=shaCode+"\\n"+load("v22CaptureCodePrefix")+'
    g.require(marker in binding['payload']['input'], 'COLLECTOR_SCRIPT_FLOW_CHANGED')
    suffix, _ = decoder.raw_decode(binding['payload']['input'].split(marker, 1)[1])
    script = (sha_code + '\n' + pre + suffix + '\n').encode('utf-8')
    g.require(evidence['actual_script']['sha256'] == SCRIPT_SHA
              and script == g.checked_bytes(root, evidence['actual_script']), 'ACTUAL_COLLECTOR_SCRIPT_CHANGED')
    mcp = tool_result(returned)
    text = [item['text'] for item in mcp['content'] if item.get('type') == 'text']
    g.require(len(text) == 1, 'SINGLE_ACTUAL_BINDING_RESULT_REQUIRED')
    actual = json.loads(text[0])
    g.require(actual == json_file(root, evidence['actual_result']), 'SELF_REPORTED_BINDING_NOT_ACTUAL_TOOL_RESULT')
    # The yielded download result must be the completion of that exact exec cell.
    first_output = str(outputs[DOWNLOAD_CALL]['payload']['output'])
    wait_args = json.loads(calls[DOWNLOAD_WAIT]['payload'].get('arguments', calls[DOWNLOAD_WAIT]['payload'].get('input')))
    g.require('cell ID 505' in first_output and wait_args.get('cell_id') == '505', 'DOWNLOAD_WAIT_NOT_BOUND_TO_CALL')
    g.require(g.sha(json.dumps(outputs[DOWNLOAD_WAIT]['payload']['output'], ensure_ascii=False,
                              sort_keys=True).encode('utf-8')) == DOWNLOAD_OUTPUT_SHA,
              'INSPECTED_OFFICIAL_DOWNLOAD_OUTPUT_CHANGED')
    download = tool_result(outputs[DOWNLOAD_WAIT])
    return actual, download, {'session_id': metadata['id'], 'binding_call_id': evidence['binding_call_id'],
                              'binding_input_sha256': BINDING_INPUT_SHA, 'binding_output_sha256': output_sha,
                              'download_call_id': DOWNLOAD_CALL, 'download_wait_call_id': DOWNLOAD_WAIT}


def svg_transform(value):
    transform = Transform()
    for op, values in re.findall(r'(matrix|translate|scale)\(([^()]*)\)', value):
        args = [float(v) for v in re.split(r'[,\s]+', values.strip())]
        current = Transform(*args) if op == 'matrix' else Transform().translate(*args) if op == 'translate' else Transform().scale(*args)
        transform = transform.transform(current)
    return transform


def svg_paths(raw, allow_official_wrapper=False):
    root = ET.fromstring(raw)
    if allow_official_wrapper:
        g.require(root.tag == g.NS + 'svg', 'OFFICIAL_SVG_ROOT_REQUIRED')
        for key, expected in [('preserveAspectRatio', 'none'), ('overflow', 'visible'), ('style', 'display: block;')]:
            g.require(root.get(key) == expected, 'OFFICIAL_SVG_WRAPPER_CHANGED')
            root.attrib.pop(key, None)
        raw = ET.tostring(root)
    tree = g.svg_tree(raw)
    paths = []
    def visit(node, transform=Transform(), opacity=1):
        transform = transform.transform(svg_transform(node.get('transform', '')))
        opacity *= float(node.get('opacity', '1')) * float(node.get('fill-opacity', '1'))
        if node.tag == g.NS + 'path':
            pen = RecordingPen()
            parse_path(node.get('d'), TransformPen(pen, transform))
            paths.append({'id': node.get('id'), 'commands': pen.value, 'opacity': opacity,
                          'winding': 'EVENODD' if node.get('fill-rule') == 'evenodd' else 'NONZERO'})
        for child in node:
            visit(child, transform, opacity)
    visit(tree)
    return paths


def native_commands(node, tx, ty):
    g.require(len(node['vectorPaths']) == 1, 'ONE_COMPOUND_NATIVE_PATH_REQUIRED')
    pen = RecordingPen()
    parse_path(node['vectorPaths'][0]['data'], TransformPen(pen, Transform(1, 0, 0, 1, tx, ty)))
    return pen.value


def compare_curves(expected, actual, anchor_budget, decimal_export=False):
    g.require(len(expected) == len(actual) and [x[0] for x in expected] == [x[0] for x in actual],
              'FIGMA_GLYPH_TOPOLOGY_CHANGED')
    first_a, first_b = expected[0][1][0], actual[0][1][0]
    anchor = [b - a for a, b in zip(first_a, first_b)]
    g.require(all(abs(v) <= budget for v, budget in zip(anchor, anchor_budget)), 'FIGMA_GLYPH_ANCHOR_CHANGED')
    maximum, shape_maximum = 0, 0
    for (_, left), (_, right) in zip(expected, actual):
        g.require(len(left) == len(right), 'FIGMA_GLYPH_POINT_COUNT_CHANGED')
        for p, q in zip(left, right):
            for axis, (a, b) in enumerate(zip(p, q)):
                g.require(finite(a) and finite(b), 'FIGMA_NONFINITE_PATH_COORDINATE')
                delta = abs(a - b)
                # Subtraction precision follows the coordinate operands, not
                # their possibly tiny difference. Four float32 roundings cover
                # parse, resize, normalization, and container-coordinate sum.
                budget = 4 * ulp32(max(abs(a), abs(b), abs(first_a[axis]), abs(first_b[axis]), 1))
                if decimal_export:
                    budget += 0.001  # difference of two coordinates each printed at 3 decimals
                shape = abs((a - first_a[axis]) - (b - first_b[axis]))
                g.require(shape <= budget, 'FIGMA_GLYPH_CONTROL_COORDINATE_CHANGED')
                maximum, shape_maximum = max(maximum, delta), max(shape_maximum, shape)
    return {'coordinates_compared': sum(len(points) * 2 for _, points in expected),
            'max_absolute_coordinate_difference': maximum, 'max_shape_coordinate_difference': shape_maximum}


def native_capture(root, capture, registration):
    g.require(fontTools.__version__ == '4.63.0', 'FONTTOOLS_GEOMETRY_RUNTIME_CHANGED')
    g.require(capture.get('schema') == 'vpd-native-figma-capture/v1' and capture.get('fileKey') == FILE_KEY
              and capture.get('frameId') == '366:2' and capture.get('pageId') == '251:2', 'ACTUAL_FRAME_CAPTURE_REQUIRED')
    rows = capture['nodes']
    nodes = {n['id']: n for n in rows}
    g.require(len(nodes) == len(rows), 'DUPLICATE_CAPTURE_NODE')
    required_frames = {'366:2', '366:3', '366:4', '366:5', '366:33'}
    g.require({n['id'] for n in rows if n['type'] == 'FRAME'} == required_frames, 'UNREGISTERED_FRAME_OR_PHOTOGRAPHIC_COPY')
    traversed = []
    def walk(ident):
        g.require(ident in nodes and ident not in traversed, 'INCOMPLETE_OR_CYCLIC_CAPTURE')
        traversed.append(ident)
        for child in nodes[ident]['children']:
            g.require(nodes.get(child, {}).get('parentId') == ident, 'CAPTURE_PARENT_CHILD_CONFLICT')
            walk(child)
    walk('366:2')
    g.require(traversed == [n['id'] for n in rows], 'COMPLETE_ORDERED_SUBTREE_REQUIRED')
    g.require(nodes['366:2']['parentId'] == '251:2' and nodes['366:2']['children'] == ['366:3', '366:4']
              and nodes['366:4']['children'] == ['366:5', '366:33'], 'REGISTERED_LAYER_ORDER_CHANGED')
    g.require(all(nodes[i]['relativeTransform'] == IDENTITY and [nodes[i]['width'], nodes[i]['height']] == list(g.SIZE)
                  for i in ('366:3', '366:4', '366:33'))
              and [nodes['366:2']['width'], nodes['366:2']['height']] == list(g.SIZE), 'FROZEN_PHOTO_OR_CANVAS_GEOMETRY_CHANGED')
    brand = nodes['366:5']
    brand_svg = ET.fromstring(g.checked_bytes(root, g.BRAND))
    brand_height = 205 * float(brand_svg.get('height')) / float(brand_svg.get('width'))
    g.require(brand['relativeTransform'] == [[1, 0, 285], [0, 1, 198]]
              and brand['width'] == 205 and brand['height'] == f32(brand_height) and not brand['clipsContent'],
              'FROZEN_BRAND_PLACEMENT_CHANGED')
    transforms = {}
    def local(n):
        if n['id'] == '366:2':
            return (0, 0)
        x, y = n['relativeTransform'][0][2], n['relativeTransform'][1][2]
        parent = nodes[n['parentId']]
        while parent['type'] == 'GROUP':
            parent = nodes[parent['parentId']]
        a, b = local(parent)
        return a + x, b + y
    for node in rows:
        g.require(node['type'] in ('FRAME', 'GROUP', 'VECTOR') and node['visible'] is True
                  and node['opacity'] == 1 and node['blendMode'] == 'PASS_THROUGH'
                  and node['effects'] == [] and node['strokes'] == [] and node['isMask'] is False,
                  'FIGMA_EFFECT_STYLE_VISIBILITY_OR_MASK_CHANGED')
        g.require(node['clipsContent'] is (node['id'] in ('366:2', '366:3', '366:4', '366:33')),
                  'FIGMA_CLIPPING_CHANGED')
        rt = node['relativeTransform']
        g.require(len(rt) == 2 and all(len(row) == 3 and all(finite(v) for v in row) for row in rt)
                  and [rt[0][:2], rt[1][:2]] == [[1, 0], [0, 1]]
                  and node['x'] == rt[0][2] and node['y'] == rt[1][2], 'FIGMA_NATIVE_TRANSFORM_CHANGED')
        transforms[node['id']] = local(node)
        actual_absolute = node['absoluteTransform']
        # GROUP-relative offsets are exposed relative to their container, but
        # absolute accumulation rounds at each immediate parent. Replay the
        # captured parent float32 sum exactly; use container coordinates below.
        parent = nodes.get(node['parentId'])
        expected_absolute = [f32(rt[axis][2]) if parent is None else
                             f32(parent['absoluteTransform'][axis][2] + rt[axis][2]
                                 - (parent['relativeTransform'][axis][2] if parent['type'] == 'GROUP' else 0))
                             for axis in (0, 1)]
        g.require([actual_absolute[0][:2], actual_absolute[1][:2]] == [[1, 0], [0, 1]]
                  and [actual_absolute[axis][2] for axis in (0, 1)] == expected_absolute,
                  'FIGMA_ABSOLUTE_RELATIVE_TRANSFORM_CONFLICT')
        fills = node['fills']
        if node['id'] == '366:3':
            g.require(len(fills) == 1, 'ONE_ORIGINAL_PHOTO_FILL_REQUIRED')
            fill = fills[0]
            g.require(fill['type'] == 'IMAGE' and fill['visible'] is True and fill['opacity'] == 1
                      and fill['blendMode'] == 'NORMAL' and fill['imageHash'] == PHOTO_HASH
                      and fill['scaleMode'] == 'FILL' and fill['rotation'] == 0
                      and fill['scalingFactor'] == 0.5
                      and fill['imageTransform'] == IDENTITY and set(fill['filters']) ==
                          {'exposure', 'contrast', 'saturation', 'temperature', 'tint', 'highlights', 'shadows'}
                      and all(v == 0 for v in fill['filters'].values()), 'ORIGINAL_PHOTOGRAPHIC_FILL_CHANGED')
        else:
            g.require(all(p.get('type') != 'IMAGE' for p in fills), 'HIDDEN_OR_DUPLICATE_PHOTOGRAPHIC_FILL')
            visible = [p for p in fills if p.get('visible', True)]
            if node['type'] == 'VECTOR':
                g.require(len(visible) == len(fills) == 1 and not node['clipsContent'], 'REGISTERED_VECTOR_FILL_REQUIRED')
                fill = visible[0]
                g.require(fill['type'] == 'SOLID' and fill['opacity'] == 1 and fill['blendMode'] == 'NORMAL'
                          and fill.get('boundVariables', {}) == {}
                          and fill['color'] == dict(zip(('r', 'g', 'b'), [f32(v / 255) for v in (245, 242, 230)])),
                          'REGISTERED_VECTOR_COLOR_OR_ALPHA_CHANGED')
            else:
                g.require(not visible and not node['vectorPaths'], 'UNREGISTERED_VISIBLE_SHAPE_OR_BACKGROUND')
    summaries, native = {}, {}
    for role, node_id, raw in [('brand', '366:5', g.brand_canvas(g.checked_bytes(root, g.BRAND))),
                              ('headline', '366:33', g.checked_bytes(root, registration['layers'][1]['svg']))]:
        expected = svg_paths(raw)
        descendants = []
        def collect(ident):
            if nodes[ident]['type'] == 'VECTOR':
                descendants.append(nodes[ident])
            for child in nodes[ident]['children']:
                collect(child)
        collect(node_id)
        g.require(len(descendants) == len(expected), 'REGISTERED_GLYPH_PATH_COUNT_CHANGED')
        results = []
        native[role] = []
        for wanted, node in zip(expected, descendants):
            g.require(wanted['id'] == node['name'] and wanted['opacity'] == 1
                      and node['vectorPaths'][0]['windingRule'] == wanted['winding'], 'REGISTERED_GLYPH_ORDER_OR_WINDING_CHANGED')
            commands = native_commands(node, *transforms[node['id']])
            first = wanted['commands'][0][1][0]
            budget = [4 * ulp32(max(abs(v), 1)) for v in first]
            if role == 'brand':
                # Frozen brand passed through earlier Figma absolute placement
                # and resize. Permit one half-ulp of its actual page coordinate
                # for translation only; shape points retain the tighter bound.
                budget = [b + 0.5 * ulp32(node['absoluteTransform'][axis][2]) for axis, b in enumerate(budget)]
            results.append(compare_curves(wanted['commands'], commands, budget))
            native[role].append({'id': wanted['id'], 'commands': commands, 'winding': wanted['winding']})
        summaries[role] = {'paths': len(results), 'coordinates_compared': sum(x['coordinates_compared'] for x in results),
                           'max_absolute_coordinate_difference': max(x['max_absolute_coordinate_difference'] for x in results),
                           'max_shape_coordinate_difference': max(x['max_shape_coordinate_difference'] for x in results)}
    g.require(sum(x['paths'] for x in summaries.values()) == sum(n['type'] == 'VECTOR' for n in rows),
              'UNREGISTERED_OR_HIDDEN_VECTOR')
    return summaries, native, nodes, transforms


def verify_actual_binding(root, registration_ref, runtime_evidence_ref, download_readback_ref):
    """Recompute real provenance, graph, paths/styles/order, and export identities."""
    _, _, registration = g.replay(root, registration_ref)
    g.require(registration['formal_version'] == 22, 'INSPECTED_V22_COLLECTOR_REQUIRED')
    evidence = json_file(root, runtime_evidence_ref)
    actual, tool_download, runtime = runtime_proof(root, evidence)
    capture_raw = g.checked_bytes(root, evidence['actual_capture'])
    body = capture_raw.removesuffix(b'\n')
    g.require(actual['schema'] == 'vpd-figma-runtime-binding/v1' and actual['fileKey'] == FILE_KEY
              and actual['frameId'] == '366:2' and actual['pageId'] == '251:2'
              and g.sha(body) == actual['capture_sha256']
              and len(body.decode('utf-8').encode('utf-16-le')) // 2 == actual['capture_chars']
              and actual['sha256_known_answer_abc'] == g.sha(b'abc'), 'ACTUAL_CAPTURE_BODY_FINGERPRINT_CONFLICT')
    capture = json.loads(body)
    g.require(actual['node_count'] == len(capture['nodes'])
              and actual['vector_count'] == sum(n['type'] == 'VECTOR' for n in capture['nodes'])
              and actual['ancestors'] == [{'id': '251:2', 'type': 'PAGE', 'name': 'VPD Codex Chazuo 20261003', 'parentId': '0:0'},
                                          {'id': '0:0', 'type': 'DOCUMENT', 'name': 'Document', 'parentId': None}],
              'REAL_COMPLETE_SUBTREE_OR_ANCESTOR_CHAIN_REQUIRED')
    source = g.checked_bytes(root, evidence['actual_source_bytes_ref'])
    raw = g.checked_bytes(root, evidence['actual_native_export_ref'])
    g.require(actual['actual_photo_imageHash'] == PHOTO_HASH and actual['actual_photo_sha256'] == g.SOURCE['sha256']
              and actual['actual_photo_bytes'] == len(source) and source == g.checked_bytes(root, g.SOURCE)
              and actual['actual_png_export_sha256'] == g.sha(raw) and actual['actual_png_export_bytes'] == len(raw),
              'ACTUAL_ORIGINAL_IMAGE_OR_FRAME_EXPORT_CHANGED')
    g.png_image(root, evidence['actual_native_export_ref'], enforce_source_profile=False)
    summary, native, nodes, transforms = native_capture(root, capture, registration)
    readback = json_file(root, download_readback_ref)
    g.require(readback['schema'] == 'vpd-official-figma-download-readback/v1'
              and readback['frameId'] == actual['frameId'] and readback['fileKey'] == FILE_KEY,
              'OFFICIAL_DOWNLOAD_READBACK_REQUIRED')
    g.require(tool_download == json_file(root, DOWNLOAD_TOOL_RESULT), 'OFFICIAL_DOWNLOAD_NOT_ACTUAL_TOOL_RETURN')
    metadata = json.loads(next(x['text'] for x in tool_download['content'] if x['type'] == 'text'))
    g.require(metadata['export']['nodeId'] == actual['frameId'] and metadata['export']['format'] == 'png'
              and metadata['export']['sizeBytes'] == len(raw) and metadata['rawImagesTruncated'] is False
              and metadata['svgAssetsTruncated'] is False and len(metadata['rawImages']) == 1
              and len(metadata['svgAssets']) == 2, 'COMPLETE_OFFICIAL_FIGMA_DOWNLOAD_REQUIRED')
    files = readback['actual_downloads']
    g.require(len(files) == 4 and all(x['http_status'] == 200 for x in files), 'SUCCESSFUL_OFFICIAL_DOWNLOADS_REQUIRED')
    seen_roles, seen_png = set(), set()
    for item in files:
        payload = g.checked_bytes(root, item)
        g.require(len(payload) == item['bytes'], 'DOWNLOADED_BYTES_CONFLICT')
        if item['format'] == 'png':
            role = 'source' if payload == source else 'raw' if payload == raw else None
            g.require(role is not None and role not in seen_png
                      and item['nodeId'] == ('366:2' if role == 'raw' else None), 'UNBOUND_OFFICIAL_PNG')
            seen_png.add(role)
            continue
        g.require(item['format'] == 'svg' and len(payload) in [x['sizeBytes'] for x in metadata['svgAssets']],
                  'UNBOUND_OFFICIAL_SVG')
        paths = svg_paths(payload, allow_official_wrapper=True)
        role = 'brand' if len(paths) == 7 else 'headline'
        g.require(role not in seen_roles and len(paths) == len(native[role]), 'OFFICIAL_SVG_ROLE_OR_PATH_COUNT_CONFLICT')
        dimensions = {'brand': ['205', '99.9478', '0 0 205 99.9478'],
                      'headline': ['475.837', '258', '0 0 475.837 258']}[role]
        wrapper = ET.fromstring(payload)
        g.require([wrapper.get(k) for k in ('width', 'height', 'viewBox')] == dimensions,
                  'OFFICIAL_SVG_VIEWPORT_CHANGED')
        seen_roles.add(role)
        origin = transforms['366:6' if role == 'brand' else '366:34']
        for saved, observed in zip(paths, native[role]):
            g.require(saved['id'] == observed['id'] and saved['opacity'] == 1
                      and saved['winding'] == observed['winding'], 'OFFICIAL_SVG_GLYPH_CONTENT_CHANGED')
            relative = [(op, tuple((x - origin[0], y - origin[1]) for x, y in points)) for op, points in observed['commands']]
            compare_curves(relative, saved['commands'], [0.0005 + 4 * ulp32(max(abs(v), 1))
                                                       for v in relative[0][1][0]], decimal_export=True)
    g.require(seen_roles == {'brand', 'headline'} and seen_png == {'source', 'raw'}, 'ALL_FOUR_OFFICIAL_ASSETS_REQUIRED')
    return {'schema': 'vpd-actual-registered-type-figma-check/v1', 'result': 'PASS_ACTUAL_BINDING_WITH_RENDERER_LIMITATIONS',
            'formal_version': 22, 'registration': registration_ref, 'runtime_evidence': runtime_evidence_ref,
            'download_readback': download_readback_ref, 'runtime': runtime,
            'capture': evidence['actual_capture'], 'frame_id': actual['frameId'], 'photo_node_id': '366:3',
            'source': g.SOURCE, 'raw_figma_export': evidence['actual_native_export_ref'],
            'node_count': actual['node_count'], 'vector_count': actual['vector_count'], 'geometry': summary,
            'registered_path_fill_RGB_tolerance': 0, 'native_png_equals_registered_final_required': False,
            'aesthetic_pass_claimed': False,
            'limitations': ['Figma native PNG and registered Sharp/Pillow final are different renderers; raw equality is not required.',
                            'Actual local host runtime log is required; portable replay without that local tool evidence is unsupported.',
                            'Only the inspected V22 collector invocation is accepted; future collectors need an explicit bounded update.']}
