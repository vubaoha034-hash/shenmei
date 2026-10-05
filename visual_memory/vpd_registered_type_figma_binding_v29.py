"""Private draft: finite actual V29 geometry/export adapter, no state or taste.

Root may copy the finished source to visual_memory and add only a V29 dispatch.
The existing V22--28 helpers supply float32/curve precision without changes.
"""
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from visual_memory import vpd_registered_type_composite as g
from visual_memory import vpd_registered_type_figma_binding as base


B = g.SERIES + 'v29/'
P = '.liu-visual-private/correct_source_typography/v29/'
CREATION = {'path': B + 'FIGMA_SOURCE_READBACK.json',
            'sha256': 'ad3c4baf711853560e78ed6b003fe2576cdd2b616e68de8bb48587cfd53e4b7e'}
CAPTURE = {'path': B + 'FIGMA_NATIVE_CAPTURE.json',
           'sha256': '3754482f93034d7cf46842376fad0c0055517de5a2bb97c22a9bbb0fa1e39847'}
BINDING = {'path': B + 'FIGMA_RUNTIME_BINDING_RESULT.json',
           'sha256': '5c9d1fce4cb13b97df17c8ed325c228dd91fbb22216b52b5e54e63c92e51c19d'}
DOWNLOAD = {'path': P + 'figma-download-tool-result.json',
            'sha256': 'b2e0cde4e70b695f7c6271ab3289127b76d827903bfe8315d8c7e7fb89bd4cc1'}
IDENTITY = [[1, 0, 0], [0, 1, 0]]
RAW_SHA = 'c070121c5fddf588bcbd103aacd2934f4428912baa228525a8518335cb833a5b'
FILE_KEY = 'uyDxOoN1iNDPpEHTKSUWg1'


def json_file(root, reference):
    return json.loads(g.checked_bytes(root, reference))


def svg_paths_v29(raw, official=False):
    tree = ET.fromstring(raw)
    if official:
        for key, expected in [('preserveAspectRatio', 'none'), ('overflow', 'visible'),
                              ('style', 'display: block;')]:
            g.require(tree.get(key) == expected, 'V29_OFFICIAL_WRAPPER_CHANGED')
            del tree.attrib[key]
        raw = ET.tostring(tree)
    tree = g.svg_tree(raw, formal_version=29)
    paths = []
    def visit(node, transform=base.Transform(), opacity=1):
        transform = transform.transform(base.svg_transform(node.get('transform', '')))
        opacity *= float(node.get('opacity', '1')) * float(node.get('fill-opacity', '1'))
        if node.tag == g.NS + 'path':
            pen = base.RecordingPen()
            base.parse_path(node.get('d'), base.TransformPen(pen, transform))
            paths.append({'id': node.get('id'), 'commands': pen.value, 'opacity': opacity,
                          'fill': node.get('fill'),
                          'winding': 'EVENODD' if node.get('fill-rule') == 'evenodd' else 'NONZERO'})
        for child in node:
            visit(child, transform, opacity)
    visit(tree)
    return paths


def official_payload(result):
    g.require(result.get('isError') is False, 'V29_ACTUAL_OFFICIAL_RESULT_REQUIRED')
    candidates = []
    for item in result['content']:
        if item.get('type') != 'text':
            continue
        try:
            value = json.loads(item['text'])
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict) and {'export', 'rawImages', 'svgAssets'} <= value.keys():
            candidates.append(value)
    g.require(len(candidates) == 1, 'V29_COMPLETE_OFFICIAL_JSON_REQUIRED')
    return candidates[0]


def native_commands_affine(node, transform):
    g.require(len(node['vectorPaths']) == 1, 'V29_ONE_COMPOUND_NATIVE_PATH_REQUIRED')
    pen = base.RecordingPen()
    base.parse_path(node['vectorPaths'][0]['data'], base.TransformPen(pen, transform))
    return pen.value


def native_capture(root, capture):
    contract = g.font_layout_kernel(root)['contract'](root)
    creation = json_file(root, CREATION)
    g.require(capture == json_file(root, CAPTURE) and capture['schema'] == 'vpd-native-figma-capture/v1'
              and capture['fileKey'] == FILE_KEY and capture['pageId'] == '251:2'
              and capture['frameId'] == creation['frame_id'] == '402:2', 'V29_ACTUAL_CAPTURE_REQUIRED')
    rows = capture['nodes']
    nodes = {row['id']: row for row in rows}
    g.require(len(nodes) == len(rows) == creation['node_count'] == 52
              and {row['id'] for row in rows if row['type'] == 'FRAME'} ==
                  {creation[key] for key in ('frame_id', 'photo_node', 'overlay_node', 'brand_node', 'title_node')}
              and {row['id'] for row in rows if row['type'] == 'GROUP'} ==
                  set(creation['brand_group_ids'] + creation['headline_group_ids'])
              and {row['id'] for row in rows if row['type'] == 'VECTOR'} ==
                  set(creation['brand_vector_ids'] + creation['headline_vector_ids']),
              'V29_EXACT_52_NODE_5_FRAME_5_GROUP_42_VECTOR_GRAPH_REQUIRED')
    traversed = []
    def walk(ident):
        g.require(ident in nodes and ident not in traversed, 'V29_INCOMPLETE_OR_CYCLIC_CAPTURE')
        traversed.append(ident)
        for child in nodes[ident]['children']:
            g.require(nodes.get(child, {}).get('parentId') == ident, 'V29_PARENT_CHILD_CONFLICT')
            walk(child)
    walk(creation['frame_id'])
    g.require(traversed == [row['id'] for row in rows]
              and nodes[creation['frame_id']]['children'] == [creation['photo_node'], creation['overlay_node']]
              and nodes[creation['overlay_node']]['children'] == [creation['brand_node'], creation['title_node']],
              'V29_COMPLETE_ORDERED_LAYER_SUBTREE_REQUIRED')
    frames = {creation[key] for key in ('frame_id', 'photo_node', 'overlay_node', 'brand_node', 'title_node')}
    g.require(nodes[creation['frame_id']]['parentId'] == '251:2'
              and all([nodes[ident]['width'], nodes[ident]['height']] == list(g.SIZE) for ident in frames)
              and all(nodes[ident]['relativeTransform'] == IDENTITY for ident in frames - {creation['frame_id']}),
              'V29_FULL_CANVAS_PHOTO_AND_TWO_SOURCE_LAYERS_REQUIRED')
    for topology in creation['brand_group_topology'] + creation['headline_group_topology']:
        row = nodes[topology['id']]
        g.require(row['type'] == topology['type'] and row['parentId'] == topology['parent_id']
                  and all(row[key] == topology[key] for key in
                          ('name', 'children', 'x', 'y', 'width', 'height', 'relativeTransform')),
                  'V29_ACTUAL_RETURNED_GROUP_TOPOLOGY_CHANGED')
    transforms = {}
    def local(node):
        if node['id'] == creation['frame_id']:
            return base.Transform()
        parent = nodes[node['parentId']]
        while parent['type'] == 'GROUP':
            parent = nodes[parent['parentId']]
        rt = node['relativeTransform']
        return local(parent).transform(base.Transform(rt[0][0], rt[1][0], rt[0][1],
                                                       rt[1][1], rt[0][2], rt[1][2]))
    for node in rows:
        g.require(node['type'] in ('FRAME', 'GROUP', 'VECTOR') and node['visible'] is True
                  and node['opacity'] == 1 and node['blendMode'] == 'PASS_THROUGH'
                  and node['effects'] == [] and node['strokes'] == [] and node['isMask'] is False
                  and node['clipsContent'] is (node['id'] in frames)
                  and node['locked'] is (node['id'] == creation['photo_node']), 'V29_STYLE_OR_MASK_CHANGED')
        rt = node['relativeTransform']
        linear = [[1, 0], [0, -1]] if node['id'] in creation['headline_vector_ids'] else [[1, 0], [0, 1]]
        g.require(len(rt) == 2 and all(len(axis) == 3 and all(base.finite(value) for value in axis) for axis in rt)
                  and [rt[0][:2], rt[1][:2]] == linear
                  and [node['x'], node['y']] == [rt[0][2], rt[1][2]], 'V29_NATIVE_TRANSFORM_CHANGED')
        transforms[node['id']] = local(node)
        parent = nodes.get(node['parentId'])
        absolute = node['absoluteTransform']
        expected = [base.f32(rt[axis][2]) if parent is None else
                    base.f32(parent['absoluteTransform'][axis][2] + rt[axis][2]
                             - (parent['relativeTransform'][axis][2] if parent['type'] == 'GROUP' else 0))
                    for axis in (0, 1)]
        g.require([absolute[0][:2], absolute[1][:2]] == linear
                  and [absolute[axis][2] for axis in (0, 1)] == expected,
                  'V29_ABSOLUTE_RELATIVE_TRANSFORM_CONFLICT')
        if node['id'] == creation['photo_node']:
            fill = node['fills'][0]
            g.require(len(node['fills']) == 1 and fill['type'] == 'IMAGE' and fill['visible'] is True
                      and fill['opacity'] == 1 and fill['blendMode'] == 'NORMAL'
                      and fill['imageHash'] == creation['photo_image_hash']
                      and fill['scaleMode'] == 'FILL' and fill['rotation'] == 0 and fill['scalingFactor'] == 0.5
                      and fill['imageTransform'] == IDENTITY
                      and set(fill['filters']) == {'exposure', 'contrast', 'saturation', 'temperature',
                                                   'tint', 'highlights', 'shadows'}
                      and all(value == 0 for value in fill['filters'].values()), 'V29_ORIGINAL_PHOTO_FILL_CHANGED')
        elif node['type'] != 'VECTOR':
            expected_fills = ([{'type': 'SOLID', 'visible': False, 'opacity': 1, 'blendMode': 'NORMAL',
                               'color': {'r': 1, 'g': 1, 'b': 1}, 'boundVariables': {}}]
                              if node['id'] in (creation['brand_node'], creation['title_node']) else [])
            g.require(node['fills'] == expected_fills, 'V29_CONTAINER_FILL_CHANGED')
    expected = svg_paths_v29(g.checked_bytes(root, contract['brand_layer'])) + \
               svg_paths_v29(g.checked_bytes(root, contract['headline_layer']))
    vector_ids = creation['brand_vector_ids'] + creation['headline_vector_ids']
    native, comparisons = {}, []
    for wanted, ident in zip(expected, vector_ids):
        node = nodes[ident]
        g.require(node['name'] == wanted['id'] and wanted['opacity'] == 1
                  and len(node['vectorPaths']) == 1 and node['vectorPaths'][0]['windingRule'] == wanted['winding'],
                  'V29_ORIGINAL_PATH_ID_ORDER_OR_WINDING_CHANGED')
        color = {key: base.f32(int(wanted['fill'][1 + index * 2:3 + index * 2], 16) / 255)
                 for index, key in enumerate(('r', 'g', 'b'))}
        g.require(node['fills'] == [{'type': 'SOLID', 'visible': True, 'opacity': 1,
                                    'blendMode': 'NORMAL', 'color': color, 'boundVariables': {}}],
                  'V29_EXACT_FOUR_REGISTERED_FILLS_REQUIRED')
        commands = native_commands_affine(node, transforms[ident])
        first = wanted['commands'][0][1][0]
        budget = [4 * base.ulp32(max(abs(value), 1)) for value in first]
        if ident in creation['brand_vector_ids']:
            budget = [value + 0.5 * base.ulp32(node['absoluteTransform'][axis][2])
                      for axis, value in enumerate(budget)]
        comparisons.append(base.compare_curves(wanted['commands'], commands, budget))
        native[ident] = {'id': wanted['id'], 'commands': commands, 'fill': wanted['fill'],
                         'winding': wanted['winding'], 'node_id': ident}
    g.require(len(expected) == len(vector_ids) == len(native) == 42, 'V29_ALL_NATIVE_CURVES_REQUIRED')
    roles = {}
    for role, group_ids, vectors in [('brand', creation['brand_group_ids'], creation['brand_vector_ids'])] + \
            [(role, creation['headline_group_ids'],
              [ident for ident in creation['headline_vector_ids'] if nodes[ident]['parentId'] == group])
             for role, group in [(nodes[ident]['name'], ident) for ident in creation['headline_group_ids']]]:
        candidates = [ident for ident in group_ids if nodes[ident]['children'] == vectors]
        g.require(len(candidates) == 1, 'V29_ONE_ACTUAL_ROLE_GROUP_REQUIRED:' + role)
        roles[role] = {'group_id': candidates[0], 'vectors': [native[ident] for ident in vectors],
                       'origin': tuple(transforms[candidates[0]][4:6]),
                       'width': nodes[candidates[0]]['width'], 'height': nodes[candidates[0]]['height']}
    g.require(set(roles) == {'brand', 'headline', 'description', 'english_hint'}, 'V29_FOUR_ACTUAL_EXPORT_GROUPS_REQUIRED')
    return roles, {'paths': 42, 'coordinates_compared': sum(row['coordinates_compared'] for row in comparisons),
                   'max_absolute_coordinate_difference': max(row['max_absolute_coordinate_difference'] for row in comparisons),
                   'max_shape_coordinate_difference': max(row['max_shape_coordinate_difference'] for row in comparisons)}


def verify_official_assets(root, capture, result, assets):
    g.require(result == json_file(root, DOWNLOAD), 'V29_FIXED_ACTUAL_DOWNLOAD_RESULT_REQUIRED')
    payload = official_payload(result)
    g.require(payload['rawImagesTruncated'] is False and payload['svgAssetsTruncated'] is False
              and len(payload['rawImages']) == 1 and len(payload['svgAssets']) == 4
              and payload['export']['nodeId'] == '402:2', 'V29_SIX_REAL_OFFICIAL_ORIGINALS_REQUIRED')
    roles, summary = native_capture(root, capture)
    binding = json_file(root, BINDING)
    rows, seen = [], set()
    metadata = [(payload['export'], 'figma-raw.png', 'raw'),
                (payload['rawImages'][0], 'figma-source-0.png', 'source')] + \
               [(value, 'figma-vector-%d.svg' % index, None)
                for index, value in enumerate(payload['svgAssets'])]
    for item, name, role in metadata:
        raw = assets[name]
        g.require(item['format'] == name.rsplit('.', 1)[1]
                  and ('sizeBytes' not in item or len(raw) == item['sizeBytes']), 'V29_OFFICIAL_BYTES_LENGTH_CHANGED')
        row = {'name': name, 'bytes': len(raw), 'sha256': g.sha(raw)}
        if role:
            expected_sha = binding['actual_png_export_sha256'] if role == 'raw' else binding['actual_photo_sha256']
            expected_size = binding['actual_png_export_bytes'] if role == 'raw' else binding['actual_photo_bytes']
            g.require(g.sha(raw) == expected_sha and len(raw) == expected_size, 'V29_OFFICIAL_PNG_RUNTIME_MISMATCH')
        else:
            saved = svg_paths_v29(raw, official=True)
            matches = [key for key, value in roles.items() if [path['id'] for path in saved] ==
                       [path['id'] for path in value['vectors']]]
            g.require(len(matches) == 1 and matches[0] not in seen, 'V29_OFFICIAL_ROLE_PATH_IDENTITIES_REQUIRED')
            role = matches[0]
            observed = roles[role]
            wrapper = ET.fromstring(raw)
            viewport = [float(value) for value in wrapper.get('viewBox').split()]
            g.require(len(viewport) == 4 and viewport[:2] == [0, 0]
                      and abs(viewport[2] - observed['width']) <= 0.0005
                      and abs(viewport[3] - observed['height']) <= 0.0005
                      and float(wrapper.get('width')) == viewport[2]
                      and float(wrapper.get('height')) == viewport[3], 'V29_OFFICIAL_ROLE_VIEWPORT_CHANGED')
            if 'nodeId' in item:
                g.require(item['nodeId'] == observed['group_id'], 'V29_RETURNED_OFFICIAL_NODE_ID_CONFLICT')
            tx, ty = observed['origin']
            comparisons = []
            for exported, native in zip(saved, observed['vectors']):
                g.require(exported['fill'] == native['fill'] and exported['opacity'] == 1
                          and exported['winding'] == native['winding'], 'V29_OFFICIAL_PATH_FILL_OR_WINDING_CHANGED')
                relative = [(operation, tuple((x - tx, y - ty) for x, y in points))
                            for operation, points in native['commands']]
                comparisons.append(base.compare_curves(relative, exported['commands'],
                    [0.0005 + 4 * base.ulp32(max(abs(value), 1)) for value in relative[0][1][0]],
                    decimal_export=True))
            row.update(svg_viewBox=wrapper.get('viewBox'), svg_paths=len(saved),
                       actual_role_node_id=observed['group_id'],
                       actual_role_vector_ids=[value['node_id'] for value in observed['vectors']],
                       role_node_id_returned='nodeId' in item,
                       role_node_id_basis='ORDERED_ORIGINAL_PATH_IDS_ALL_CURVES_FILL_VIEWPORT_AND_COMPLETE_ACTUAL_NATIVE_GROUP; download nodeId absent unless explicitly returned',
                       geometry_coordinates_compared=sum(value['coordinates_compared'] for value in comparisons))
        seen.add(role)
        row['role'] = role
        rows.append(row)
    g.require(seen == {'raw', 'source', 'brand', 'headline', 'description', 'english_hint'},
              'V29_ALL_SIX_ORIGINAL_EXPORTS_BOUND_REQUIRED')
    return rows, summary


# Actual collector's already-used read-only kernel, mechanically inlined.
import hashlib
import re
MARKERS = ('v29FigmaPart1Source', 'v29FigmaPart2Source', 'v29BindingReadSource',
           'v29ActualChunkSources', 'v29ActualDownloadAssets', 'v29ActualCaptureBodyRead')

def require(value, detail):
    g.require(value, 'REQUIRED_ACTUAL_DATA: ' + detail)

PROFILE = json.loads('{"runtime_evidence": {"path": "evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v29/FIGMA_BINDING_RUNTIME_EVIDENCE.json", "sha256": "413a0e4ea0727355deaa866340db55d1f70faca135d6e96a8092a726d19f73a6"}, "creation_runtime": {"path": "evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v29/CREATION_RUNTIME_EVIDENCE.json", "sha256": "9dd9e897c709f99a8660218206e56f710c7bd62bf66c35f2a666314c45d48c2b"}, "root_host": "C:\\\\Users\\\\Administrator\\\\.codex\\\\sessions\\\\2026\\\\10\\\\04\\\\rollout-2026-10-04T11-12-31-01a0ffab-c9b7-7c40-b55b-e51535c156dd_01a104e6-1b34-70a3-b5fa-04cac3947c09.jsonl", "creation_calls": [{"call_id": "call_AglSxsbUcFaJECDeanSllEnq", "timestamp": "2026-10-05T05:19:54.825Z", "input_sha256": "2717f1f4ea59b44cf30ad2ecba8cd7d4ef9e7f4460c1b49cb252944dd3b9505f", "output_sha256": "78f5d78238cee6127fc3871fd334762fb0b6cfa18077e3d0d65a9d1f273b7ac2", "source": {"path": "evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v29/FIGMA_ASSEMBLY_PART1.js", "sha256": "3e7778aade47cc6f82fc454efd90b18613f372bbfa880d56266a542b32d0323a"}, "code_carrier": "ACTUAL_AWAITED_FILE_READ_JSON_PARSE_PACKET_CODE", "nested_exec_read_output_printed_separately": false, "source_sha_asserted_in_wrapper": true, "actual_transport": {"initial_output_sha256": "78f5d78238cee6127fc3871fd334762fb0b6cfa18077e3d0d65a9d1f273b7ac2", "yield_wait_events": [], "completion_call_id": "call_AglSxsbUcFaJECDeanSllEnq"}, "literal_script_claimed": false}, {"call_id": "call_Bt6OFWOg3K3wYnvs42p99w1T", "timestamp": "2026-10-05T05:21:58.048Z", "input_sha256": "89998da363158f93155c1c6b96bbc77aea3e7e09aa0ccf36e9f17109d8c26013", "output_sha256": "7d8f8180409a7bbc89389f4d0f90eb8c63ceb299835063379c8af2b8fa656c2f", "source": {"path": "evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v29/FIGMA_ASSEMBLY_PART2.js", "sha256": "150a1cacc3d49ba1d5fe869b334f3bfc6a0758a5c30c4e12aba5f24077c9bbe3"}, "code_carrier": "ACTUAL_AWAITED_FILE_READ_JSON_PARSE_PACKET_CODE", "nested_exec_read_output_printed_separately": false, "source_sha_asserted_in_wrapper": true, "actual_transport": {"initial_output_sha256": "7d8f8180409a7bbc89389f4d0f90eb8c63ceb299835063379c8af2b8fa656c2f", "yield_wait_events": [], "completion_call_id": "call_Bt6OFWOg3K3wYnvs42p99w1T"}, "literal_script_claimed": false}], "binding_read_use": {"call_id": "call_leHiPlkFOaIwrAPDTYUEjhtK", "timestamp": "2026-10-05T05:23:58.611Z", "input_sha256": "07471f6f585c2d3c354aac2885d34dd485a0708af4718b0a12742deabdc0e181", "output_sha256": "217396dccb8b1bf98ad3bdbe6c95c0c63c59bb6ce8dc83e9524fd5e168fba555", "source": {"path": "evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v29/FIGMA_BINDING_READ.js", "sha256": "9e11cb57035cc24c83bd716b75db0cb31ebaa023d14eb839bf654cf5978aae7e"}, "code_carrier": "ACTUAL_AWAITED_FILE_READ_JSON_PARSE_PACKET_CODE", "nested_exec_read_output_printed_separately": false, "source_sha_asserted_in_wrapper": false, "actual_transport": {"initial_output_sha256": "d78bfd2d0d13b3faa91df3468ae3aec16941c0b076d1e4cc0e5784683bd0987f", "yield_wait_events": [{"call_id": "call_8VDnDIVOAQYo95fmiLRFaLcD", "timestamp": "2026-10-05T05:24:51.387Z", "input_sha256": "bc837ee63dba63e76a2b511461e90af68b8cc220eedbb2d4d9bc83720b02c30d", "output_sha256": "217396dccb8b1bf98ad3bdbe6c95c0c63c59bb6ce8dc83e9524fd5e168fba555"}], "completion_call_id": "call_8VDnDIVOAQYo95fmiLRFaLcD", "yield_cell_id": "1236"}, "literal_script_claimed": false}, "chunk_source_reader": {"call_id": "call_pKFmK0kX0Is7GNYSuhaDOufa", "timestamp": "2026-10-05T05:32:58.697Z", "input_sha256": "250ac707ed07d8ecf989a5c39f70e19aab79419c7d2712d302f71624aa5f943a", "output_sha256": "cb9f1f62b5b6a2b183950eb3a6ec4cc042889e8164d52d7e84e32a5bb380b1cb"}, "chunk_batches": [{"call_id": "call_rY9y8Tu3zOzddUva0RzvVklN", "timestamp": "2026-10-05T05:33:32.039Z", "input_sha256": "61a946842c816c39c0448335a8ba0b94612ae0f82832ea974c2cf5b63c95ad07", "output_sha256": "65e6b7e27af86523b8bcfdc8ee76661fe6b023f232229b65d280291ad2be123d", "indices": [0, 1, 2, 3], "actual_transport": {"initial_output_sha256": "4bfcff35c518d8bd6d0c3826196cd523a451050683b4807307031f66ae238d8b", "yield_wait_events": [{"call_id": "call_wBvnjqpOPPNaMTDs3DHg9cQH", "timestamp": "2026-10-05T05:34:33.666Z", "input_sha256": "204af9e26fa20190e92d8668913e6c9b0c233d184acaff48660dbf5ab828718d", "output_sha256": "31f8baed41716172b16adcae688285042cdfdd284c82b2ddb80dfb8b67777a62"}, {"call_id": "call_hrsovkZzvYDxcRGcCGaIxSPB", "timestamp": "2026-10-05T05:34:49.822Z", "input_sha256": "8473e8d04137f3b5ca57b38780c8191ddd2da2aa06b98df7b05768bb90118c77", "output_sha256": "65e6b7e27af86523b8bcfdc8ee76661fe6b023f232229b65d280291ad2be123d"}], "completion_call_id": "call_hrsovkZzvYDxcRGcCGaIxSPB", "yield_cell_id": "1249"}, "complete_mcp_printed_in_host": false, "actual_full_return_carrier": "JSON_PARSED_FROM_AWAITED_MCP_AND_SAVED_BY_ACTUAL_APPLY_PATCH"}, {"call_id": "call_nSHPIZ5FYbS7DZ0uJNJLJTBx", "timestamp": "2026-10-05T05:35:08.514Z", "input_sha256": "d51037f065541937b39ffc216a558522b067cfe8d9fbe53564781a8426b6cfd1", "output_sha256": "fe338a183d078eef540e2b77acd978ab412d56f4e5ec13a8ff983dc323aadb48", "indices": [4, 5, 6, 7], "actual_transport": {"initial_output_sha256": "c04e03f0b888ae524d9303171628a3d72cb7a97b320bdaa97664b499035c4d57", "yield_wait_events": [{"call_id": "call_RDmE2ozFjwOfbyCzVoWzeZeG", "timestamp": "2026-10-05T05:36:48.268Z", "input_sha256": "8f85ca2ec4fe690928877e2e640a23d42c6295dd5abc1f149bd30a66afcb5481", "output_sha256": "fe338a183d078eef540e2b77acd978ab412d56f4e5ec13a8ff983dc323aadb48"}], "completion_call_id": "call_RDmE2ozFjwOfbyCzVoWzeZeG", "yield_cell_id": "1250"}, "complete_mcp_printed_in_host": false, "actual_full_return_carrier": "JSON_PARSED_FROM_AWAITED_MCP_AND_SAVED_BY_ACTUAL_APPLY_PATCH"}, {"call_id": "call_213d4UFPhdPJ9pkacH8CSOFP", "timestamp": "2026-10-05T05:37:06.415Z", "input_sha256": "f1d3d727e798311590c558b4b57d3aeb223ab33621511efb4edbed2dcabcd45e", "output_sha256": "74765c79c1b02a0f3595e98db838f45e2810eb02bb67efbd8e45a81d15a2d8af", "indices": [8, 9, 10, 11], "actual_transport": {"initial_output_sha256": "82c92fda4b7783dd0b9c33c37f60eb47791dc85413b9ff00ceaa638f33522e3f", "yield_wait_events": [{"call_id": "call_TaixH9rnDUx4UtfsgjXxoe4X", "timestamp": "2026-10-05T05:37:59.685Z", "input_sha256": "c36e6376e216dfe323f3cf90e0f4b5d8d736db2d0490ca510e6916e4e03f29a6", "output_sha256": "a048c6a5f6d7e41a355c9544edd0e9f02261c9d36fecbc1384955cc0f80caf15"}, {"call_id": "call_o5TGFSrB3ggiEWBzQOwTtxJA", "timestamp": "2026-10-05T05:38:09.100Z", "input_sha256": "c36e6376e216dfe323f3cf90e0f4b5d8d736db2d0490ca510e6916e4e03f29a6", "output_sha256": "a048c6a5f6d7e41a355c9544edd0e9f02261c9d36fecbc1384955cc0f80caf15"}, {"call_id": "call_av4xvFqpvCDVlvT3hX5xKc2V", "timestamp": "2026-10-05T05:38:34.276Z", "input_sha256": "e968fb70006a4091ff1dedbe299478b084d4f1433e309d87e50dbc3ee9544a66", "output_sha256": "74765c79c1b02a0f3595e98db838f45e2810eb02bb67efbd8e45a81d15a2d8af"}], "completion_call_id": "call_av4xvFqpvCDVlvT3hX5xKc2V", "yield_cell_id": "1251"}, "complete_mcp_printed_in_host": false, "actual_full_return_carrier": "JSON_PARSED_FROM_AWAITED_MCP_AND_SAVED_BY_ACTUAL_APPLY_PATCH"}, {"call_id": "call_jKNCzuIYhUG2jKw5fc7mU2FR", "timestamp": "2026-10-05T05:38:51.065Z", "input_sha256": "1bfde8cb178d7f97f3fed24246631c89aabcc18e0f046b7016228bd9504f8efe", "output_sha256": "945e895ff344cafb440c123b7a16d1e5515cd5e3b30dea583b5e257920cb1da8", "indices": [12, 13, 14, 15], "actual_transport": {"initial_output_sha256": "e0f0f7d47c3987db5dfaab65343526c7a95a1762e81cac93340a4dfec539cf4c", "yield_wait_events": [{"call_id": "call_isdErYLxN3MedlqDxP5A5mlF", "timestamp": "2026-10-05T05:39:47.462Z", "input_sha256": "b0285f18761d6131eb8fc4e706af9b380ae84091aa070053a024f86d4daa4d90", "output_sha256": "9f0413e2fa05d66d3bf2d9074fdad86a8075ba2d58bf0f826bbc7d2be686c7fe"}, {"call_id": "call_GzUxGO6wk3R3rj4JsjH1lKOg", "timestamp": "2026-10-05T05:40:58.746Z", "input_sha256": "b0285f18761d6131eb8fc4e706af9b380ae84091aa070053a024f86d4daa4d90", "output_sha256": "945e895ff344cafb440c123b7a16d1e5515cd5e3b30dea583b5e257920cb1da8"}], "completion_call_id": "call_GzUxGO6wk3R3rj4JsjH1lKOg", "yield_cell_id": "1252"}, "complete_mcp_printed_in_host": false, "actual_full_return_carrier": "JSON_PARSED_FROM_AWAITED_MCP_AND_SAVED_BY_ACTUAL_APPLY_PATCH"}], "chunk_plan": {"path": "evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v29/FIGMA_CAPTURE_CHUNKS_PLAN.json", "sha256": "ad35296692825d95191b564ad89fc51ab517717604f71759af7c94929856baaf"}, "complete_chunk_returns": [{"index": 0, "batch_call_id": "call_rY9y8Tu3zOzddUva0RzvVklN", "source": {"path": "evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v29/FIGMA_CAPTURE_CHUNK_00.js", "sha256": "4c02d936db39d4091ed01466ec8fb878e8eac145f33dc03f98904ad325cfede4"}, "actual_complete_return": {"path": "evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v29/FIGMA_CAPTURE_CHUNK_00_READBACK.json", "sha256": "a87f47b462b7ec59e7441c7dee3a09e3e81569c4387046e7e2c782745375848c"}, "offset": 0, "end": 13000}, {"index": 1, "batch_call_id": "call_rY9y8Tu3zOzddUva0RzvVklN", "source": {"path": "evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v29/FIGMA_CAPTURE_CHUNK_01.js", "sha256": "2b36653582949f3d2b8fad485331847db2768a20e72867c42389aea366369209"}, "actual_complete_return": {"path": "evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v29/FIGMA_CAPTURE_CHUNK_01_READBACK.json", "sha256": "addf4532d28ac275b839e83b536107082e8f931337d4f561a7bd54d5c7ca9bb6"}, "offset": 13000, "end": 26000}, {"index": 2, "batch_call_id": "call_rY9y8Tu3zOzddUva0RzvVklN", "source": {"path": "evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v29/FIGMA_CAPTURE_CHUNK_02.js", "sha256": "b53ff87eab46f47d735bbaad8994870542bbee8158788e37cde483c532e5492c"}, "actual_complete_return": {"path": "evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v29/FIGMA_CAPTURE_CHUNK_02_READBACK.json", "sha256": "51d40dc46cf62c2b785c159ea0a390f69ade123372b9fc361b9a245e9580fa8b"}, "offset": 26000, "end": 39000}, {"index": 3, "batch_call_id": "call_rY9y8Tu3zOzddUva0RzvVklN", "source": {"path": "evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v29/FIGMA_CAPTURE_CHUNK_03.js", "sha256": "bf06b61c82cc81b4df8e845b2b6d52b59b39311d8f97900a3b68f55ca46a6c51"}, "actual_complete_return": {"path": "evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v29/FIGMA_CAPTURE_CHUNK_03_READBACK.json", "sha256": "8e9c318f8cd6922e4975be184f0e0f5483199a20e8b7a3ffc43124f2b8c756d3"}, "offset": 39000, "end": 52000}, {"index": 4, "batch_call_id": "call_nSHPIZ5FYbS7DZ0uJNJLJTBx", "source": {"path": "evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v29/FIGMA_CAPTURE_CHUNK_04.js", "sha256": "66e50bacfccd38a0eee343e0044027c3a38b0a27e37f1d01ed988c712d266c17"}, "actual_complete_return": {"path": "evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v29/FIGMA_CAPTURE_CHUNK_04_READBACK.json", "sha256": "47a1461463ba4fa8b50e58b0afe29af62d310c531d8858ef4db6cc03f07bcdc8"}, "offset": 52000, "end": 65000}, {"index": 5, "batch_call_id": "call_nSHPIZ5FYbS7DZ0uJNJLJTBx", "source": {"path": "evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v29/FIGMA_CAPTURE_CHUNK_05.js", "sha256": "05c1e4011698343b161d09afff458853bd4dcf016d9364676953ac4ff8f874bb"}, "actual_complete_return": {"path": "evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v29/FIGMA_CAPTURE_CHUNK_05_READBACK.json", "sha256": "df64c33b36a09f8759806d76227b4cb441c82603ca4e5ddfd772afe6feaf28b4"}, "offset": 65000, "end": 78000}, {"index": 6, "batch_call_id": "call_nSHPIZ5FYbS7DZ0uJNJLJTBx", "source": {"path": "evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v29/FIGMA_CAPTURE_CHUNK_06.js", "sha256": "ede1ea14138cbaff2c884b7f29ce69ea81e11151dc795fe2960b7436c29e5222"}, "actual_complete_return": {"path": "evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v29/FIGMA_CAPTURE_CHUNK_06_READBACK.json", "sha256": "154338fe1f9146bbfa09cf712779f98432afcd23c0b1c7fe9dcbeac4d742a396"}, "offset": 78000, "end": 91000}, {"index": 7, "batch_call_id": "call_nSHPIZ5FYbS7DZ0uJNJLJTBx", "source": {"path": "evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v29/FIGMA_CAPTURE_CHUNK_07.js", "sha256": "4af3ab9fccc6a929a873cfc93e2d6b0b0780ee1a13a0bcedd0611306cf63d870"}, "actual_complete_return": {"path": "evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v29/FIGMA_CAPTURE_CHUNK_07_READBACK.json", "sha256": "fe57d98fdc65795cd71dd24d027fdb90197c7b8589cb8be1651d32ca7a26136c"}, "offset": 91000, "end": 104000}, {"index": 8, "batch_call_id": "call_213d4UFPhdPJ9pkacH8CSOFP", "source": {"path": "evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v29/FIGMA_CAPTURE_CHUNK_08.js", "sha256": "94c3714b78ab9abca5d77dd8983edcc8f8bd3e224c88377d2a02b3b810e3ff16"}, "actual_complete_return": {"path": "evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v29/FIGMA_CAPTURE_CHUNK_08_READBACK.json", "sha256": "cc87aba2fd17fe84a35c626510bd8464a39d03bd0151e7f2f0a909b3638d408c"}, "offset": 104000, "end": 117000}, {"index": 9, "batch_call_id": "call_213d4UFPhdPJ9pkacH8CSOFP", "source": {"path": "evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v29/FIGMA_CAPTURE_CHUNK_09.js", "sha256": "dc6d2d95bc7f4afbc5e45e1f0a4169519f685d4f7e98249a0a5ca3694c72e0dd"}, "actual_complete_return": {"path": "evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v29/FIGMA_CAPTURE_CHUNK_09_READBACK.json", "sha256": "0a24a298c8c275db65c8b030744cb6ed8537d52d9d669e1e2b5fb8a0d14a0cce"}, "offset": 117000, "end": 130000}, {"index": 10, "batch_call_id": "call_213d4UFPhdPJ9pkacH8CSOFP", "source": {"path": "evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v29/FIGMA_CAPTURE_CHUNK_10.js", "sha256": "4bc54a18566c48a87a7c2a3ce3203a4c9421b583072b28c437264c809c3adec3"}, "actual_complete_return": {"path": "evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v29/FIGMA_CAPTURE_CHUNK_10_READBACK.json", "sha256": "b42778eca10b2604f4153a5bf26e0d6aac65b59d85b1469531d1e1e3845d2d98"}, "offset": 130000, "end": 143000}, {"index": 11, "batch_call_id": "call_213d4UFPhdPJ9pkacH8CSOFP", "source": {"path": "evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v29/FIGMA_CAPTURE_CHUNK_11.js", "sha256": "5fbb095074bfc985ed2120d5fd568bf57e87f050da3c11cd464168243919dbd9"}, "actual_complete_return": {"path": "evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v29/FIGMA_CAPTURE_CHUNK_11_READBACK.json", "sha256": "0136ab01c11b3ce5f39412c690ec625b8b3f457ba657258dc9b1e392f94f0e4b"}, "offset": 143000, "end": 156000}, {"index": 12, "batch_call_id": "call_jKNCzuIYhUG2jKw5fc7mU2FR", "source": {"path": "evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v29/FIGMA_CAPTURE_CHUNK_12.js", "sha256": "285af10021f175da76a22dce92cf19eb1201cacac05eb6972523ee53116c5805"}, "actual_complete_return": {"path": "evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v29/FIGMA_CAPTURE_CHUNK_12_READBACK.json", "sha256": "86209d50cc1bd7031388499e7efc52404f910b58f9cbf79ddd951ab3171aa787"}, "offset": 156000, "end": 169000}, {"index": 13, "batch_call_id": "call_jKNCzuIYhUG2jKw5fc7mU2FR", "source": {"path": "evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v29/FIGMA_CAPTURE_CHUNK_13.js", "sha256": "0e4d2c6da687d70379b1804f4e98573526ff5c6051058fc855a9bf4a3c6fadb8"}, "actual_complete_return": {"path": "evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v29/FIGMA_CAPTURE_CHUNK_13_READBACK.json", "sha256": "5a5633d84f9757c8db0a93c775f5ea91538e59910cf56966ac735ca689ffbbc8"}, "offset": 169000, "end": 182000}, {"index": 14, "batch_call_id": "call_jKNCzuIYhUG2jKw5fc7mU2FR", "source": {"path": "evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v29/FIGMA_CAPTURE_CHUNK_14.js", "sha256": "b5d06f492a0631929d60c986f8867f53815f1be2edf3f12df048cabec00ea736"}, "actual_complete_return": {"path": "evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v29/FIGMA_CAPTURE_CHUNK_14_READBACK.json", "sha256": "789e976f81621ff538da8a07e0d602895e96ec70774c37a1d5efe33d07930069"}, "offset": 182000, "end": 195000}, {"index": 15, "batch_call_id": "call_jKNCzuIYhUG2jKw5fc7mU2FR", "source": {"path": "evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v29/FIGMA_CAPTURE_CHUNK_15.js", "sha256": "2d5a2d3a4da69b71c20964d40ff87775d3f4d717309b090548dc0a036071857c"}, "actual_complete_return": {"path": "evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v29/FIGMA_CAPTURE_CHUNK_15_READBACK.json", "sha256": "fcec0a29409fa5b4777b3af0520944d3ded223ebbc30a8bad68b8cf6e7e93157"}, "offset": 195000, "end": 197755}], "download": {"download_call_id": "call_J0jmSpPNiZGjmAATw4Ui4zEm", "download_call_input_sha256": "a42099bece3488a22754e9c06e79183382154b704f0f81624a90832f4a82cdd3", "download_output_sha256": "58b0a1c97004a9bb3fa02c2e458e2388c40c07abc4189934c658926747f0a46a", "actual_download_transport": {"initial_output_sha256": "8f048ed3d59d35eddc3666def6530c9d881e56bb72ff249f36537d2f96803ab9", "yield_wait_events": [{"call_id": "call_ex0Z7tYxgmmHQpZdLExBavVg", "timestamp": "2026-10-05T05:27:57.816Z", "input_sha256": "47325e3a06c83d84487dc5b30bd9ed88ea5c540860d8a62614b19229e10e6983", "output_sha256": "3c5b526a29ba81214fd100582f768e822f873dc3ce1dca1456766c616325716d"}, {"call_id": "call_b8OvLCShgSbEI3Ael4GD2VBv", "timestamp": "2026-10-05T05:28:10.494Z", "input_sha256": "644de8ba1f3cf382e445be4f8a27baf574f9a5ff7ea24d7ca438c780a2f135e4", "output_sha256": "58b0a1c97004a9bb3fa02c2e458e2388c40c07abc4189934c658926747f0a46a"}], "completion_call_id": "call_b8OvLCShgSbEI3Ael4GD2VBv", "yield_cell_id": "1239"}, "actual_download_supplemental_existing_print": {"call_id": "call_mPzbQw0hK6ICqIYxu3PE8num", "timestamp": "2026-10-05T05:48:00.315Z", "input_sha256": "c6f73970e7474adc2b5c86b9235680f5a38b482b1d031951946e8af908ce5d99", "output_sha256": "d8f37168932d8d3a2a852849c5b029493a1b3a6e8a0b69c75a7d4f384a00632c", "actual_transport": {"initial_output_sha256": "d8f37168932d8d3a2a852849c5b029493a1b3a6e8a0b69c75a7d4f384a00632c", "yield_wait_events": [], "completion_call_id": "call_mPzbQw0hK6ICqIYxu3PE8num"}}}, "copied_readonly_kernel_source": {"path": ".liu-visual-private/v29-helper-adaptation/collect-v29-runtime.py", "sha256": "3167363eb4bf7286f91af53d733718ff360a46657a25ca77e19c2488b2991be7"}}')

def selected_events(host):
    selected, contexts = [], []
    with host.open(encoding='utf-8-sig') as stream:
        for line in stream:
            if re.search(r'"type"\s*:\s*"turn_context"', line):
                row = json.loads(line)
                if row.get('type') == 'turn_context':
                    contexts.append(row)
            elif 'custom_tool_call' in line and any(marker in line for marker in MARKERS):
                row = json.loads(line)
                if row.get('payload', {}).get('type') == 'custom_tool_call':
                    selected.append(row)
    ids = {row['payload']['call_id'] for row in selected}
    outputs = []
    with host.open(encoding='utf-8-sig') as stream:
        for line in stream:
            if 'custom_tool_call_output' not in line or not any(value in line for value in ids):
                continue
            row = json.loads(line)
            if row.get('payload', {}).get('type') == 'custom_tool_call_output' \
                    and row['payload'].get('call_id') in ids:
                outputs.append(row)
    cells = {cell for row in outputs for value in output_texts(row)
             for cell in re.findall(r'Script running with cell ID\s+(\w+)', value)}
    waits = []
    with host.open(encoding='utf-8-sig') as stream:
        for line in stream:
            if not re.search(r'"name"\s*:\s*"wait"', line):
                continue
            row = json.loads(line)
            value = row.get('payload', {})
            if value.get('type') == 'function_call' and value.get('name') == 'wait':
                args = json.loads(value['arguments'])
                if args.get('cell_id') in cells:
                    waits.append(row)
    wait_ids = {row['payload']['call_id'] for row in waits}
    wait_outputs = []
    with host.open(encoding='utf-8-sig') as stream:
        for line in stream:
            if 'function_call_output' not in line or not any(value in line for value in wait_ids):
                continue
            row = json.loads(line)
            if row.get('payload', {}).get('type') == 'function_call_output' \
                    and row['payload'].get('call_id') in wait_ids:
                wait_outputs.append(row)
    return contexts + selected + outputs + waits + wait_outputs

def output_texts(event):
    value = event['payload']['output']
    return [value] if isinstance(value, str) else [item['text'] for item in value
                                                 if item.get('type') == 'input_text']

def json_values(event):
    values = []
    for text in output_texts(event):
        try:
            values.append(json.loads(text))
        except json.JSONDecodeError:
            pass
    return values

def payload_sha(event):
    value = event['payload']
    if value['type'] in ('custom_tool_call', 'function_call'):
        return hashlib.sha256(value.get('input', value.get('arguments')).encode('utf-8')).hexdigest()
    return hashlib.sha256(json.dumps(value['output'], ensure_ascii=False,
                                     sort_keys=True).encode('utf-8')).hexdigest()

def call_reference(call, output):
    return {'call_id': call['payload']['call_id'], 'timestamp': call['timestamp'],
            'input_sha256': payload_sha(call), 'output_sha256': payload_sha(output)}

def actual_completion(rows, call):
    initial = output_for(rows, call)
    cells = {cell for value in output_texts(initial)
             for cell in re.findall(r'Script running with cell ID\s+(\w+)', value)}
    proof = {'initial_output_sha256': payload_sha(initial), 'yield_wait_events': [],
             'completion_call_id': initial['payload']['call_id']}
    if not cells:
        require(any('Script completed' in value for value in output_texts(initial)),
                'actual immediate completed functions result')
        return initial, proof
    require(len(cells) == 1, 'one actual yielded exec cell')
    cell = next(iter(cells))
    completed = []
    waits = [row for row in rows if row['payload'].get('type') == 'function_call'
             and row['payload'].get('name') == 'wait'
             and json.loads(row['payload']['arguments']).get('cell_id') == cell]
    for wait in waits:
        output = output_for(rows, wait)
        proof['yield_wait_events'].append(call_reference(wait, output))
        if any('Script completed' in value for value in output_texts(output)):
            completed.append(output)
    require(len(completed) == 1, 'actual single completed wait result for cell ' + cell)
    proof.update(yield_cell_id=cell, completion_call_id=completed[0]['payload']['call_id'])
    return completed[0], proof

def complete_mcp_json(output):
    result = actual_mcp(output)
    texts = [item['text'] for item in result['content'] if item.get('type') == 'text']
    require(len(texts) == 1 and '// truncated to 20kb' not in texts[0],
            'complete actual JSON MCP return, not the failed full-body clamp')
    return json.loads(texts[0])

def file_read_use(rows, script_path, source_marker, root):
    relative = script_path.relative_to(root).as_posix()
    raw = script_path.read_bytes()
    require(b'\r' not in raw and script_path.read_text('utf-8').encode('utf-8') == raw,
            'fixed LF UTF-8 Figma source')
    matches = [row for row in rows if row['payload'].get('type') == 'custom_tool_call'
               and source_marker in row['payload']['input']
               and relative in row['payload']['input']
               and 'tools.mcp__codex_apps__figma_use_figma(' in row['payload']['input']]
    require(len(matches) == 1, 'one actual file-read-and-use ' + script_path.name)
    call = matches[0]
    code = call['payload']['input']
    match = re.search(r'const\s+(\w+)\s*=\s*await\s+tools\.exec_command\(\{cmd:', code)
    require(match, 'actual awaited source exec_command')
    command, _ = json.JSONDecoder().raw_decode(code[match.end():])
    expected_read = "p=pathlib.Path('" + relative + "'); print(json.dumps({'code':p.read_text('utf-8'),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()},ensure_ascii=False))"
    require(expected_read in command and '-X utf8 -B -c' in command,
            'actual Python file code/hash read expression')
    parsed = re.search(r'const\s+(\w+)\s*=\s*JSON\.parse\(' + match[1] + r'\.output\)', code)
    require(parsed and 'if(' + match[1] + '.exit_code!==0)' in code,
            'actual checked exec output and JSON.parse')
    packet = parsed[1]
    require(re.search(r'store\(["\']' + re.escape(source_marker) + r'["\'],\s*' + packet + r'\)', code)
            and 'code:' + packet + '.code' in code
            and 'fileKey:' + json.dumps(FILE_KEY) in code,
            'actual source packet stored and its code passed to use_figma')
    require(not re.search(r'\b' + packet + r'\s*=(?!=)', code[parsed.end():])
            and not re.search(r'\b' + packet + r'\.code\s*=', code),
            'source packet/code not reassigned before the actual tool')
    output, transport = actual_completion(rows, call)
    actual = complete_mcp_json(output)
    proof = dict(call_reference(call, output), source=g.ref(root, script_path),
                 code_carrier='ACTUAL_AWAITED_FILE_READ_JSON_PARSE_PACKET_CODE',
                 nested_exec_read_output_printed_separately=False,
                 source_sha_asserted_in_wrapper=g.sha(script_path.read_bytes()) in code,
                 actual_transport=transport,
                 literal_script_claimed=False)
    return call, output, actual, proof

def output_for(rows, call):
    found = [row for row in rows if row['payload'].get('type') in ('custom_tool_call_output', 'function_call_output')
             and row['payload'].get('call_id') == call['payload']['call_id']]
    require(len(found) == 1, 'one actual output for ' + call['payload']['call_id'])
    return found[0]

def actual_mcp(out):
    found = []
    for item in out['payload']['output']:
        if item.get('type') != 'input_text':
            continue
        try:
            value = json.loads(item['text'])
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict) and value.get('isError') is False and value.get('content'):
            found.append(value)
    require(len(found) == 1, 'one complete actual MCP result')
    return found[0]


def runtime_proof(root, evidence):
    """Independent real-host read; no collector main or evidence-file writes."""
    require(type(evidence.get('formal_version')) is int and evidence == json_file(root, PROFILE['runtime_evidence'])
            and evidence['formal_version'] == 29
            and evidence['code_carrier'] == 'ACTUAL_FILE_READ_AND_USE_V29',
            'fixed actual V29 runtime proof')
    host = Path(evidence['root_rollout_host_path']).resolve()
    require(host == Path(PROFILE['root_host']).resolve() and host.is_file(), 'actual local Root host')
    rows = selected_events(host)
    calls = {row['payload']['call_id']: row for row in rows
             if row['payload'].get('type') in ('custom_tool_call', 'function_call')}
    def known_call(reference):
        require(reference['call_id'] in calls, 'actual fixed host call ' + reference['call_id'])
        call = calls[reference['call_id']]
        output, transport = actual_completion(rows, call)
        observed = call_reference(call, output)
        require(all(observed[key] == reference[key] for key in observed), 'actual host call/input/completed output SHA')
        if 'actual_transport' in reference:
            require(transport == reference['actual_transport'], 'actual initial/yield/wait/completion chain')
        return call, output, transport
    for expected, marker, saved in zip(PROFILE['creation_calls'],
                                      ('v29FigmaPart1Source', 'v29FigmaPart2Source'),
                                      (B + 'FIGMA_PART1_READBACK.json', CREATION['path'])):
        g.checked_bytes(root, expected['source'])
        call, output, value, proof = file_read_use(rows, Path(root) / expected['source']['path'], marker, root)
        require(proof == expected and value == json.loads((Path(root) / saved).read_bytes()),
                'actual two-part creation source/use/full return')
        contexts = [row for row in rows if row.get('type') == 'turn_context' and row['timestamp'] <= call['timestamp']]
        require(contexts and (contexts[-1]['payload']['model'], contexts[-1]['payload']['effort']) ==
                ('gpt-6.1-sol', 'xhigh'), 'actual creation-time Root Sol/xhigh; no latest-turn/Max substitution')
    wanted = PROFILE['binding_read_use']
    g.checked_bytes(root, wanted['source'])
    _, _, value, proof = file_read_use(rows, Path(root) / wanted['source']['path'], 'v29BindingReadSource', root)
    require(proof == wanted and value == json_file(root, BINDING), 'actual yielded binding/source/complete summary')
    plan = json_file(root, PROFILE['chunk_plan'])
    reader, reader_out, _ = known_call(PROFILE['chunk_source_reader'])
    reader_code = reader['payload']['input']
    for token in ('await tools.exec_command(', 'JSON.parse(prep.output)', 'if(prep.exit_code!==0)',
                  "code=(root/row['source']['path']).read_text('utf8')",
                  "actual_source_sha256=hashlib.sha256((root/row['source']['path']).read_bytes()).hexdigest()",
                  'row.actual_source_sha256!==row.source.sha256', 'store("v29ActualChunkSources",packet)'):
        require(token in reader_code, 'actual guarded chunk source read ' + token)
    coverage = {}
    for batch in PROFILE['chunk_batches']:
        call, output, _ = known_call(batch)
        code = call['payload']['input']
        start, end = batch['indices'][0], batch['indices'][-1] + 1
        require('packet.sources.slice(%d,%d)' % (start, end) in code, 'actual exact batch slice')
        for token in ('load("v29ActualChunkSources")', 'await tools.mcp__codex_apps__figma_use_figma({code:row.code',
                      'if(r.isError)', 'JSON.parse(r.content.find(x=>x.type==="text").text)',
                      'o.index!==row.index', 'o.offset!==row.offset', 'o.end!==row.end',
                      'o.capture_sha256!==packet.plan.capture_sha256', 'o.capture_chars!==packet.plan.capture_chars',
                      'o.chunk.length!==o.chunk_chars', 'batch.push({row,r,o})', 'x.row.actual_readback_path',
                      'JSON.stringify(x.o,null,2)', 'await tools.apply_patch(patch)'):
            require(token in code, 'actual chunk await/parse/check/save chain ' + token)
        metadata = []
        for index in batch['indices']:
            require(index not in coverage, 'one actual planned chunk call')
            coverage[index] = batch['call_id']
            row = plan['chunks'][index]
            chunk = json.loads((Path(root) / row['actual_readback_path']).read_bytes())
            metadata.append({'index': index, 'chars': chunk['chunk_chars'], 'sha': chunk['capture_sha256'],
                             'actual_complete_return_saved': True})
        require(metadata in json_values(output), 'actual completed wait metadata matches saved complete returns')
    require(sorted(coverage) == list(range(plan['chunk_count'])) == list(range(16)), 'all sixteen actual read calls')
    pieces, cursor = [], 0
    for row, reference in zip(plan['chunks'], PROFILE['complete_chunk_returns']):
        g.checked_bytes(root, row['source'])
        require(row['source'] == reference['source'] and coverage[row['index']] == reference['batch_call_id'],
                'fixed chunk source and actual host batch binding')
        chunk = json_file(root, reference['actual_complete_return'])
        require(chunk['index'] == row['index'] and chunk['frameId'] == '402:2'
                and chunk['schema'] == 'vpd-native-figma-capture-chunk-read/v1'
                and chunk['chunk_count'] == 16 and chunk['offset'] == cursor == row['offset']
                and chunk['end'] == row['end'] and chunk['capture_chars'] == 197755
                and chunk['capture_sha256'] == CAPTURE['sha256']
                and chunk['sha256_known_answer_abc'] == value['sha256_known_answer_abc'],
                'actual continuous chunk offsets and fixed whole hash')
        raw = chunk['chunk'].encode('utf-16-le', errors='surrogatepass')
        require(len(raw) // 2 == chunk['chunk_chars'] == chunk['end'] - chunk['offset'], 'actual UTF16 payload size')
        pieces.append(raw)
        cursor = chunk['end']
    whole = b''.join(pieces).decode('utf-16-le').encode('utf-8')
    require(cursor == 197755 and whole == g.checked_bytes(root, CAPTURE), 'actual chunks equal exact complete capture')
    download = PROFILE['download']
    call = calls[download['download_call_id']]
    output, transport = actual_completion(rows, call)
    require(payload_sha(call) == download['download_call_input_sha256']
            and payload_sha(output) == download['download_output_sha256']
            and transport == download['actual_download_transport'], 'actual download yield/wait provenance')
    code = call['payload']['input']
    for token in ('const r=await tools.mcp__codex_apps__figma_download_assets(', 'nodeId:"402:2"',
                  'store("v29ActualDownloadAssets",r)', 'figma-download-tool-result.json',
                  'JSON.stringify(r,null,2)', 'await tools.apply_patch('):
        require(token in code, 'actual original download/store/save chain')
    supplemental = download['actual_download_supplemental_existing_print']
    call, output, _ = known_call(supplemental)
    require('load("v29ActualDownloadAssets")' in call['payload']['input']
            and 'store("v29ActualDownloadAssetsPrintedExisting",r)' in call['payload']['input']
            and 'figma_download_assets(' not in call['payload']['input']
            and actual_mcp(output) == json_file(root, DOWNLOAD), 'existing store/load/full MCP supplemental print')
    return {'actual_host_read': True, 'root_model': 'gpt-6.1-sol', 'root_effort': 'xhigh',
            'creation_mutation_calls': 2, 'capture_read_calls': 16, 'download_tool_calls': 1,
            'code_carrier': 'FILE_READ_AND_USE_WITH_ACTUAL_YIELD_WAIT_AND_SAVED_BOUNDED_MCP_RETURNS',
            'direct_literal_claimed': False, 'failed_fullbody_clamp_not_complete': True}


def verify_actual_binding(root, registration_ref, runtime_evidence_ref, download_readback_ref):
    """Only V29, independently authenticated source/host/native/all six originals."""
    registration = json_file(root, registration_ref)
    require(type(registration.get('formal_version')) is int and registration['formal_version'] == 29,
            'finite actual V29 binding only; unknown30/default rejected')
    _, _, fresh = g.replay(root, registration_ref)
    require(fresh == registration and registration['headline_lineage']['kind'] == 'source-han-serif-font-layout/v29',
            'actual independently replayed font-layout registration')
    require(all(runtime_evidence_ref[key] == PROFILE['runtime_evidence'][key] for key in ('path', 'sha256')),
            'fixed actual V29 runtime reference')
    evidence = json_file(root, runtime_evidence_ref)
    runtime = runtime_proof(root, evidence)
    capture = json_file(root, CAPTURE)
    saved = json_file(root, download_readback_ref)
    require(len(saved) == 6 and {row['name'] for row in saved} ==
            {'figma-raw.png', 'figma-source-0.png'} | {'figma-vector-%d.svg' % index for index in range(4)},
            'actual six role readbacks')
    assets = {}
    for row in saved:
        require(row['http_status'] == 200 and row.get('download_repeated') is False,
                'actual original successful six-asset readback receipt')
        assets[row['name']] = g.checked_bytes(root, {'path': row['path'], 'sha256': row['sha256']})
        require(len(assets[row['name']]) == row['bytes'], 'actual original readback byte size')
    observed, summary = verify_official_assets(root, capture, json_file(root, DOWNLOAD), assets)
    for row, bound in zip(observed, saved):
        require(all(bound[key] == value for key, value in row.items()), 'recomputed actual six SVG/PNG role bindings')
    actual = json_file(root, BINDING)
    return {'schema': 'vpd-actual-registered-type-figma-check/v1',
            'result': 'PASS_ACTUAL_BINDING_WITH_RENDERER_LIMITATIONS', 'formal_version': 29,
            'registration': registration_ref, 'runtime_evidence': runtime_evidence_ref,
            'download_readback': download_readback_ref, 'runtime': runtime, 'capture': CAPTURE,
            'frame_id': actual['frameId'], 'photo_node_id': '402:3', 'source': g.SOURCE,
            'raw_figma_export': evidence['actual_native_export_ref'],
            'node_count': actual['node_count'], 'vector_count': actual['vector_count'], 'geometry': summary,
            'registered_path_fill_RGB_tolerance': 0, 'native_png_equals_registered_final_required': False,
            'aesthetic_pass_claimed': False,
            'limitations': ['Figma native PNG and registered Sharp/Pillow final use different renderers.',
                            'Actual local host, yielded waits and saved bounded returns are required.',
                            'Complete chunk data was saved within real MCP batch loops; host output is metadata.',
                            'Only this actual font-layout V29 profile is accepted; V30 and later fail closed.']}
