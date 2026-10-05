"""Actual registered Figma proof, independently checked from host tool events.

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
V23 = {'binding_call': 'call_tCCbrp4HOJyWbziY3WEZJ3zZ',
       'binding_input': '4c86ed9e21b4bd1e70615be9fa40c470941441e6f1ae6d108c6440d19aab31be',
       'binding_output': '7e6cce132e2337459be6bc4dcf9e31522510f23032c551e46444eb159c7dcb99',
       'script': 'cb68cca48de8a9a2b7e9393cf944255fdf24bd9e7fad95b65cecefca56b9e793',
       'download_call': 'call_QicmGyYyIKDrR7THDQ5IxrOj',
       'download_input': '6988c4074d8827ec4c2c729ecf65ed075974890e9e56659e4e34aa82a84f55be',
       'download_output': '5de1c79f920477e2bb2247d2fa13761ef747a1481d9a2909e8c40a2b0dc7c474',
       'download_tool': {'path': '.liu-visual-private/correct_source_typography/v23/figma-download-tool-result.json',
                         'sha256': '0f4087cfeac2d6df2ceaf9a2e865bc7ee371821bb6e4a128477c1abe75d4df20'}}
V24 = {'binding_call': 'call_MGST85que1frWIYg3AXCGhr5',
       'binding_input': 'e7ec1b440b788481a0fa2f5f63b771394b48339ea58e78b3507f2486ca9245ac',
       'binding_output': '64ff43cbb51cf6951fd5e40c555f5192488270884467a7226b1bd4e227d6ec22',
       'script': 'cc03e8584d7263f587d63bc7bdcc01e10a3dc41c1d565095a1c19c88140d2937',
       'download_call': 'call_WfxLnhX9NR3ls10pnvJdJWNM',
       'download_input': '5319c8237491f242b326b541a1ecca49b036aa3c5d6b0c1501d1032bb0f97ffc',
       'download_output': '3aaa67660e8213a00b8e5cb023df210c7021839329cd3ee26fddd8747aac0a42',
       'download_tool': {'path': '.liu-visual-private/correct_source_typography/v24/figma-download-tool-result.json',
                         'sha256': 'befccda57e8b16675e91615de1a676225e665f9b1ebc08726982a4329dc82893'}}
V25 = {'binding_call': 'call_KFLsFIhOQqATXkOLlFGYOKF8',
       'binding_input': '04c7e986461134c66884a2fd57c1c5c46c4fa9bae2b018185457ebc5421c26b0',
       'binding_output': 'bf47f93a9ecb09c0bff9a939d76d19c7d5cc85f10c48b149bf1f10868b0b3488',
       'script': '64ec65eb0b00ad06e52ceca13d144e7560c2aa01002db22cf575052be0fd86ea',
       'download_call': 'call_o8muNTfnNwO47azkamlHyc6T',
       'download_input': 'bc82c571139ffe2d08111f4d60bba2a41ea5bfbe8ae17a6ed69753be27e9186c',
       'download_output': '2c2e064293701dc70a470d3c5001a20bd14b0886917430659ba42c2fa2cc2281',
       'download_tool': {'path': '.liu-visual-private/correct_source_typography/v25/figma-download-tool-result.json',
                         'sha256': '4d34534fe8704d95deb217e8c5eee7eb556cf5eeab6f9e2bae6088c46d54791f'}}
V26 = {'binding_call': 'call_fQ1b7XEsDxHgxgKpWcpZoGqF',
       'binding_input': '97f40c1b9aa1a163a105a544094e67d43c68d213b98c887127d787f22cbccc0a',
       'binding_output': '706400de1f1bde3c1d0339337cc2ef30a3c661d9d5449788231ff6960887ee85',
       'script': 'eb59226bc9846d46af5941f82106d1bd5eb6962ab65b424bb22693d75f1d08f2',
       'download_call': 'call_W0slq1jKHi4LO8JFsr3c8WV8',
       'download_input': '5176f33c42ba287324c8999d120249eecebe6ab4bcc37836923d6903a107ad10',
       'download_output': '45d2d49e0f15df72666f68914250928136ad4e3287113a63028339475ca37bc4',
       'download_tool': {'path': '.liu-visual-private/correct_source_typography/v26/figma-download-tool-result.json',
                         'sha256': 'f8520effc61b265e132065d34e9a00937aea389ab4f76fdc034af07ec32e8c8b'}}
V27 = {'binding_call': 'call_4D3Wt6FsE4HAn5njG20yfc8Q',
       'binding_input': '3336e71e26b409b12e913ddc741fc88603d35cc53521d82186c2136cedad0eda',
       'binding_output': '7bc834bd1c034f18e98cc7755b0700b92c95e25211ade632791bd5f798215a4b',
       'script': 'ae424ba67af3fedd482083f5af95e14bb7b24e2ba7852953fd2bab6f91ba4729',
       'download_call': 'call_i7FGKFUmXe0xuz4Tb2sB8Arm',
       'download_input': '7320bf35cebacf6f2a325ea3d54b073acaf34b00f880b79c6593d9026bf0c9e0',
       'download_output': '02caaea2fc6d023b72d7f4fae6cd962754efe3a74b29d57db87574ba79ca3116',
       'download_tool': {'path': '.liu-visual-private/correct_source_typography/v27/figma-download-tool-result.json',
                         'sha256': '0021fd31f2708f9e75cdcd414d16cfabbe82297b757e038946cb8ef3484fdef0'}}

V28 = {'binding_call': 'call_lfWG12TO1g8NFsfo0wuDI1eM',
 'binding_input': 'e4c9ef974718780acc7c8ff6ce2af2cd3e6334c6dce756d8e9a30fec489f059c',
 'binding_output': 'f6a7b66926b4ec075f112508637dc7e384e378d831e65977777281184cd19b11',
 'download_call': 'call_y5P5ZKPMTtvLkcYs20VaJ65H',
 'download_input': '5e92e637fe743ebb1dcffa0636575a3d7b3fe69080bed2ccd399520347932ef5',
 'download_output': '866dc7b02a349dfedf1cb218abff03d96a90c6e08f09800d8a4986b54eaf315b',
 'script': '0983b767e6567305c15cca71417a29838322849af045005942a57e0da2cdeb1f',
 'download_tool': {'path': '.liu-visual-private/correct_source_typography/v28/figma-download-tool-result.json',
                   'sha256': '2462c0d1e39c9a4aa33f4733805a1db830a486d64ece75db499bf33c5c2784ee'},
 'download_literal': 'const result=await '
                     'tools.mcp__codex_apps__figma_download_assets({fileKey:"uyDxOoN1iNDPpEHTKSUWg1",nodeId:"398:2"});store("v28BoundOfficialDownload",result);text(result)\n'}
V28_NATIVE = {'prefix': '398',
 'ids': {'2': '398:2',
         '3': '398:3',
         '4': '398:4',
         '5': '398:5',
         '6': '398:6',
         '23': '398:23',
         '31': '398:31',
         '7': '398:7',
         '8': '398:8',
         '9': '398:9',
         '10': '398:10',
         '11': '398:11',
         '12': '398:12',
         '13': '398:13',
         '24': '398:24',
         '25': '398:25',
         '26': '398:26',
         '27': '398:27',
         '28': '398:28',
         '29': '398:29',
         '30': '398:30'},
 'group_box': [380, 354, 968.6055908203125, 309],
 'headline_viewport': ['968.606', '309', '0 0 968.606 309'],
 'official_brand_name': 'figma-vector-0.svg'}


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
    if evidence.get('formal_version') == 23:
        return runtime_proof_v23(root, evidence)
    if evidence.get('formal_version') == 24:
        return runtime_proof_v23(root, evidence, 24)
    if evidence.get('formal_version') == 25:
        return runtime_proof_v23(root, evidence, 25)
    if evidence.get('formal_version') == 26:
        return runtime_proof_v23(root, evidence, 26)
    if evidence.get('formal_version') == 27:
        return runtime_proof_v23(root, evidence, 27)
    if evidence.get('formal_version') == 28:
        return runtime_proof_v23(root, evidence, 28)
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


def runtime_proof_v23(root, evidence, version=23):
    """Two individually inspected direct literals/immediate downloads; no prefix or wait."""
    g.require(version in (23, 24, 25, 26, 27, 28), 'INSPECTED_DIRECT_COLLECTOR_REQUIRED')
    profile = {23: V23, 24: V24, 25: V25, 26: V26, 27: V27, 28: V28}[version]
    g.require(evidence.get('schema') == 'vpd-figma-binding-runtime-evidence/v1'
              and evidence.get('formal_version') == version
              and evidence.get('binding_call_id') == profile['binding_call']
              and evidence.get('download_call_id') == profile['download_call']
              and evidence.get('download_result_transport') == 'IMMEDIATE_FULL_ACTUAL_RESULT_NO_WAIT',
              f'ACTUAL_V{version}_RUNTIME_EVIDENCE_REQUIRED')
    host = Path(evidence['root_rollout_host_path']).resolve()
    g.require(host.is_relative_to(Path('C:/Users/Administrator/.codex/sessions').resolve())
              and host.suffix == '.jsonl', 'ACTUAL_HOST_RUNTIME_REQUIRED')
    ids = {profile['binding_call'], profile['download_call']}
    calls, outputs, metadata = {}, {}, None
    with host.open(encoding='utf-8') as stream:
        for line in stream:
            event = json.loads(line)
            payload = event.get('payload', {})
            if event['type'] == 'session_meta':
                metadata = payload
            ident = payload.get('call_id')
            if ident not in ids:
                continue
            if payload.get('type') == 'custom_tool_call':
                g.require(ident not in calls, 'DUPLICATE_RUNTIME_CALL')
                calls[ident] = event
            elif payload.get('type') == 'custom_tool_call_output':
                g.require(ident not in outputs, 'DUPLICATE_RUNTIME_OUTPUT')
                outputs[ident] = event
    g.require(metadata and Path(metadata['cwd']).resolve() in (Path(root).resolve(), Path(root).resolve().parent)
              and set(calls) == ids and set(outputs) == ids, 'COMPLETE_REAL_RUNTIME_REQUIRED')
    for role in ('binding', 'download'):
        call, output = calls[profile[role + '_call']], outputs[profile[role + '_call']]
        g.require(call['payload']['name'] == 'exec'
                  and g.sha(call['payload']['input'].encode('utf-8')) == profile[role + '_input']
                  == evidence[role + '_call_input_sha256'], 'INSPECTED_ACTUAL_COLLECTOR_INVOCATION_REQUIRED')
        g.require(g.sha(json.dumps(output['payload']['output'], ensure_ascii=False, sort_keys=True).encode('utf-8'))
                  == profile[role + '_output'] == evidence[role + '_output_sha256'], 'ACTUAL_BINDING_OUTPUT_CONFLICT')
    binding, returned = calls[profile['binding_call']], outputs[profile['binding_call']]
    g.require(binding['timestamp'] == evidence['binding_call_timestamp'], 'ACTUAL_BINDING_CALL_IDENTITY_CONFLICT')
    g.require(json_file(root, evidence['private_exact_runtime_excerpt'])
              == [binding, returned, calls[profile['download_call']], outputs[profile['download_call']]],
              'EXCERPT_DOES_NOT_MATCH_REAL_HOST_RUNTIME')
    text = binding['payload']['input']
    g.require(text.startswith('const script='), 'COLLECTOR_SCRIPT_FLOW_CHANGED')
    script, _ = json.JSONDecoder().raw_decode(text[len('const script='):])
    g.require(evidence['actual_script']['sha256'] == profile['script']
              and script.encode('utf-8') == g.checked_bytes(root, evidence['actual_script']),
              'ACTUAL_COLLECTOR_SCRIPT_CHANGED')
    mcp = tool_result(returned)
    result = [item['text'] for item in mcp['content'] if item.get('type') == 'text']
    g.require(len(result) == 1, 'SINGLE_ACTUAL_BINDING_RESULT_REQUIRED')
    actual = json.loads(result[0])
    g.require(actual == json_file(root, evidence['actual_result']), 'SELF_REPORTED_BINDING_NOT_ACTUAL_TOOL_RESULT')
    if version == 25:
        # The inspected actual call polls a shell first. Its literal download
        # and text(result) remain in the same SHA-bound exec; no fictitious wait.
        download_input = calls[profile['download_call']]['payload']['input']
        literal = ('\nconst result=await tools.mcp__codex_apps__figma_download_assets('
                   '{fileKey:"uyDxOoN1iNDPpEHTKSUWg1",nodeId:"388:2"});'
                   'store("v25BoundOfficialDownload",result);text(result);')
        g.require(download_input.startswith('text(await tools.write_stdin(')
                  and download_input.endswith(literal + '\n'), 'V25_ACTUAL_LITERAL_DOWNLOAD_FLOW_CHANGED')
    if version == 26:
        literal = ('const result=await tools.mcp__codex_apps__figma_download_assets('
                   '{fileKey:"uyDxOoN1iNDPpEHTKSUWg1",nodeId:"391:2"});'
                   'store("v26BoundOfficialDownload",result);text(result);\n')
        g.require(calls[profile['download_call']]['payload']['input'] == literal,
                  'V26_ACTUAL_LITERAL_DOWNLOAD_FLOW_CHANGED')
    if version == 27:
        literal = ('const result=await tools.mcp__codex_apps__figma_download_assets('
                   '{fileKey:"uyDxOoN1iNDPpEHTKSUWg1",nodeId:"395:2"});'
                   'store("v27BoundOfficialDownload",result);text(result)\n')
        g.require(calls[profile['download_call']]['payload']['input'] == literal,
                  'V27_ACTUAL_LITERAL_DOWNLOAD_FLOW_CHANGED')
    if version == 28:
        g.require(calls[profile['download_call']]['payload']['input'] == V28['download_literal'], 'V28_ACTUAL_LITERAL_DOWNLOAD_FLOW_CHANGED')
    return actual, tool_result(outputs[profile['download_call']]), {
        'session_id': metadata['id'], 'binding_call_id': profile['binding_call'],
        'binding_input_sha256': profile['binding_input'], 'binding_output_sha256': profile['binding_output'],
        'download_call_id': profile['download_call'], 'download_input_sha256': profile['download_input'],
        'download_output_sha256': profile['download_output'],
        'download_result_transport': 'IMMEDIATE_FULL_ACTUAL_RESULT_NO_WAIT'}


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


def native_capture(root, capture, registration, version=22):
    g.require(version in (22, 23, 24, 25, 26, 27, 28), 'INSPECTED_NATIVE_VERSION_REQUIRED')
    prefix = {22: '366', 23: '373', 24: '384', 25: '388', 26: '391', 27: '395', 28: V28_NATIVE['prefix']}[version]
    def node_id(suffix):
        return V28_NATIVE['ids'][str(suffix)] if version == 28 else prefix + ':' + str(suffix)
    g.require(fontTools.__version__ == '4.63.0', 'FONTTOOLS_GEOMETRY_RUNTIME_CHANGED')
    g.require(capture.get('schema') == 'vpd-native-figma-capture/v1' and capture.get('fileKey') == FILE_KEY
              and capture.get('frameId') == node_id(2) and capture.get('pageId') == '251:2', 'ACTUAL_FRAME_CAPTURE_REQUIRED')
    rows = capture['nodes']
    nodes = {n['id']: n for n in rows}
    g.require(len(nodes) == len(rows), 'DUPLICATE_CAPTURE_NODE')
    if version == 24:
        g.require(set(nodes) == {node_id(i) for i in (*range(2, 14), *range(33, 42))}
                  and nodes[node_id(33)]['children'] == [node_id(41)]
                  and nodes[node_id(41)]['type'] == 'GROUP'
                  and nodes[node_id(41)]['children'] == [node_id(i) for i in range(34, 41)]
                  and [nodes[node_id(41)][k] for k in ('x', 'y', 'width', 'height')] == [612, 419, 623, 262],
                  'V24_REGISTERED_COMPOUND_GROUP_CHANGED')
    if version in (25, 26, 27, 28):
        group_box = ([625, 419, 610, 208.00003051757812] if version == 25
                     else [535, 402, 743.0169677734375, 133.51461791992188] if version == 26
                     else [331, 403, 995.384765625, 283.20428466796875] if version == 27 else V28_NATIVE['group_box'])
        g.require(set(nodes) == {node_id(i) for i in (*range(2, 14), *range(23, 32))}
                  and nodes[node_id(23)]['children'] == [node_id(31)]
                  and nodes[node_id(31)]['type'] == 'GROUP'
                  and nodes[node_id(31)]['children'] == [node_id(i) for i in range(24, 31)]
                  and [nodes[node_id(31)][k] for k in ('x', 'y', 'width', 'height')]
                      == group_box, f'V{version}_REGISTERED_COMPOUND_GROUP_CHANGED')
    headline_frame = node_id(23 if version in (25, 26, 27, 28) else 33)
    required_frames = {node_id(i) for i in (2, 3, 4, 5)} | {headline_frame}
    g.require({n['id'] for n in rows if n['type'] == 'FRAME'} == required_frames, 'UNREGISTERED_FRAME_OR_PHOTOGRAPHIC_COPY')
    traversed = []
    def walk(ident):
        g.require(ident in nodes and ident not in traversed, 'INCOMPLETE_OR_CYCLIC_CAPTURE')
        traversed.append(ident)
        for child in nodes[ident]['children']:
            g.require(nodes.get(child, {}).get('parentId') == ident, 'CAPTURE_PARENT_CHILD_CONFLICT')
            walk(child)
    walk(node_id(2))
    g.require(traversed == [n['id'] for n in rows], 'COMPLETE_ORDERED_SUBTREE_REQUIRED')
    g.require(nodes[node_id(2)]['parentId'] == '251:2' and nodes[node_id(2)]['children'] == [node_id(3), node_id(4)]
              and nodes[node_id(4)]['children'] == [node_id(5), headline_frame], 'REGISTERED_LAYER_ORDER_CHANGED')
    g.require(all(nodes[i]['relativeTransform'] == IDENTITY and [nodes[i]['width'], nodes[i]['height']] == list(g.SIZE)
                  for i in (node_id(3), node_id(4), headline_frame))
              and [nodes[node_id(2)]['width'], nodes[node_id(2)]['height']] == list(g.SIZE), 'FROZEN_PHOTO_OR_CANVAS_GEOMETRY_CHANGED')
    brand = nodes[node_id(5)]
    brand_svg = ET.fromstring(g.checked_bytes(root, g.BRAND))
    brand_height = 205 * float(brand_svg.get('height')) / float(brand_svg.get('width'))
    g.require(brand['relativeTransform'] == [[1, 0, 285], [0, 1, 198]]
              and brand['width'] == 205 and brand['height'] == f32(brand_height) and not brand['clipsContent'],
              'FROZEN_BRAND_PLACEMENT_CHANGED')
    transforms = {}
    def local(n):
        if n['id'] == node_id(2):
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
        g.require(node['clipsContent'] is (node['id'] in (node_id(2), node_id(3), node_id(4), headline_frame)),
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
        if node['id'] == node_id(3):
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
    for role, role_id, raw in [('brand', node_id(5), g.brand_canvas(g.checked_bytes(root, g.BRAND))),
                              ('headline', headline_frame, g.checked_bytes(root, registration['layers'][1]['svg']))]:
        expected = svg_paths(raw)
        descendants = []
        def collect(ident):
            if nodes[ident]['type'] == 'VECTOR':
                descendants.append(nodes[ident])
            for child in nodes[ident]['children']:
                collect(child)
        collect(role_id)
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
    version = registration['formal_version']
    g.require(version in (22, 23, 24, 25, 26, 27, 28), 'INSPECTED_V22_COLLECTOR_REQUIRED')
    prefix = {22: '366', 23: '373', 24: '384', 25: '388', 26: '391', 27: '395', 28: V28_NATIVE['prefix']}[version]
    if version == 23:
        new = g.svg_tree(g.checked_bytes(root, registration['layers'][1]['svg']))
        original = g.svg_tree(g.checked_bytes(root, {'path': g.SERIES + 'v22/headline.svg',
            'sha256': 'e9feab432466d4f1a7188fdeff746ab6773a538ff59d1f2c3fa477aa3de6d14d'}))
        g.require([dict(p.attrib) for p in new.iter(g.NS + 'path')]
                  == [dict(p.attrib) for p in original.iter(g.NS + 'path')], 'V23_ORIGINAL_17_PATH_ATTRIBUTES_CHANGED')
        groups = list(new.iter(g.NS + 'g'))
        g.require(len(groups) == 1 and len(groups[0]) == 17 and all(n.tag == g.NS + 'path' for n in groups[0]),
                  'V23_SINGLE_WHOLE_PHRASE_GROUP_REQUIRED')
        transform = svg_transform(groups[0].get('transform', ''))
        g.require(re.fullmatch(r'matrix\([^()]+\)', groups[0].get('transform', ''))
                  and transform.xx == transform.yy > 0 and transform.xy == transform.yx == 0,
                  'V23_POSITIVE_UNIFORM_SCALE_TRANSLATE_REQUIRED')
    evidence = json_file(root, runtime_evidence_ref)
    g.require(evidence.get('formal_version') == version, 'ACTUAL_RUNTIME_VERSION_CONFLICT')
    actual, tool_download, runtime = runtime_proof(root, evidence)
    capture_raw = g.checked_bytes(root, evidence['actual_capture'])
    body = capture_raw.removesuffix(b'\n')
    g.require(actual['schema'] == 'vpd-figma-runtime-binding/v1' and actual['fileKey'] == FILE_KEY
              and actual['frameId'] == (V28_NATIVE['ids']['2'] if version == 28 else prefix + ':2') and actual['pageId'] == '251:2'
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
    summary, native, nodes, transforms = native_capture(root, capture, registration, version)
    readback = json_file(root, download_readback_ref)
    if version == 22:
        g.require(readback['schema'] == 'vpd-official-figma-download-readback/v1'
                  and readback['frameId'] == actual['frameId'] and readback['fileKey'] == FILE_KEY,
                  'OFFICIAL_DOWNLOAD_READBACK_REQUIRED')
    else:
        g.require(isinstance(readback, list) and {x['name'] for x in readback}
                  == {'figma-raw.png', 'figma-source-0.png', 'figma-vector-0.svg', 'figma-vector-1.svg'},
                  'OFFICIAL_DOWNLOAD_READBACK_REQUIRED')
    g.require(tool_download == json_file(root, DOWNLOAD_TOOL_RESULT if version == 22 else
                                        {23: V23, 24: V24, 25: V25, 26: V26, 27: V27, 28: V28}[version]['download_tool']),
              'OFFICIAL_DOWNLOAD_NOT_ACTUAL_TOOL_RETURN')
    metadata = json.loads(next(x['text'] for x in tool_download['content'] if x['type'] == 'text'))
    g.require(metadata['export']['nodeId'] == actual['frameId'] and metadata['export']['format'] == 'png'
              and metadata['export']['sizeBytes'] == len(raw) and metadata['rawImagesTruncated'] is False
              and metadata['svgAssetsTruncated'] is False and len(metadata['rawImages']) == 1
              and len(metadata['svgAssets']) == 2, 'COMPLETE_OFFICIAL_FIGMA_DOWNLOAD_REQUIRED')
    files = readback['actual_downloads'] if version == 22 else readback
    g.require(len(files) == 4 and all(x['http_status'] == 200 for x in files), 'SUCCESSFUL_OFFICIAL_DOWNLOADS_REQUIRED')
    seen_roles, seen_png = set(), set()
    for item in files:
        payload = g.checked_bytes(root, item)
        g.require(len(payload) == item['bytes'], 'DOWNLOADED_BYTES_CONFLICT')
        file_format = item['format'] if version == 22 else Path(item['name']).suffix[1:]
        if file_format == 'png':
            role = 'source' if payload == source else 'raw' if payload == raw else None
            g.require(role is not None and role not in seen_png
                      and (item['nodeId'] == ('366:2' if role == 'raw' else None) if version == 22
                           else item['name'] == ('figma-raw.png' if role == 'raw' else 'figma-source-0.png')),
                      'UNBOUND_OFFICIAL_PNG')
            seen_png.add(role)
            continue
        g.require(file_format == 'svg' and len(payload) in [x['sizeBytes'] for x in metadata['svgAssets']],
                  'UNBOUND_OFFICIAL_SVG')
        paths = svg_paths(payload, allow_official_wrapper=True)
        if version in (24, 25, 26, 27, 28):
            # Both real exports have seven paths: use the ordered registered
            # node/path identities, then verify their viewport and all curves.
            roles = [role for role in ('brand', 'headline') if [p['id'] for p in paths]
                     == [p['id'] for p in native[role]]]
            g.require(len(roles) == 1, 'OFFICIAL_SVG_ROLE_OR_PATH_COUNT_CONFLICT')
            role = roles[0]
        else:
            role = 'brand' if len(paths) == 7 else 'headline'
        g.require(role not in seen_roles and len(paths) == len(native[role]), 'OFFICIAL_SVG_ROLE_OR_PATH_COUNT_CONFLICT')
        dimensions = {'brand': ['205', '99.9478', '0 0 205 99.9478'],
                      'headline': (['475.837', '258', '0 0 475.837 258'] if version == 22
                                   else ['379.932', '206', '0 0 379.932 206'] if version == 23
                                   else ['623', '262', '0 0 623 262'] if version == 24
                                   else ['610', '208', '0 0 610 208'] if version == 25
                                   else ['743.017', '133.515', '0 0 743.017 133.515'] if version == 26
                                   else ['995.385', '283.204', '0 0 995.385 283.204'] if version == 27
                                   else V28_NATIVE['headline_viewport'])}[role]
        wrapper = ET.fromstring(payload)
        g.require([wrapper.get(k) for k in ('width', 'height', 'viewBox')] == dimensions,
                  'OFFICIAL_SVG_VIEWPORT_CHANGED')
        seen_roles.add(role)
        origin = transforms[V28_NATIVE['ids']['6' if role == 'brand' else '31'] if version == 28 else prefix + (':6' if role == 'brand' else ':31' if version in (25, 26, 27, 28) else ':41' if version == 24 else ':34')]
        for saved, observed in zip(paths, native[role]):
            g.require(saved['id'] == observed['id'] and saved['opacity'] == 1
                      and saved['winding'] == observed['winding'], 'OFFICIAL_SVG_GLYPH_CONTENT_CHANGED')
            relative = [(op, tuple((x - origin[0], y - origin[1]) for x, y in points)) for op, points in observed['commands']]
            compare_curves(relative, saved['commands'], [0.0005 + 4 * ulp32(max(abs(v), 1))
                                                       for v in relative[0][1][0]], decimal_export=True)
    g.require(seen_roles == {'brand', 'headline'} and seen_png == {'source', 'raw'}, 'ALL_FOUR_OFFICIAL_ASSETS_REQUIRED')
    return {'schema': 'vpd-actual-registered-type-figma-check/v1', 'result': 'PASS_ACTUAL_BINDING_WITH_RENDERER_LIMITATIONS',
            'formal_version': version, 'registration': registration_ref, 'runtime_evidence': runtime_evidence_ref,
            'download_readback': download_readback_ref, 'runtime': runtime,
            'capture': evidence['actual_capture'], 'frame_id': actual['frameId'], 'photo_node_id': V28_NATIVE['ids']['3'] if version == 28 else prefix + ':3',
            'source': g.SOURCE, 'raw_figma_export': evidence['actual_native_export_ref'],
            'node_count': actual['node_count'], 'vector_count': actual['vector_count'], 'geometry': summary,
            'registered_path_fill_RGB_tolerance': 0, 'native_png_equals_registered_final_required': False,
            'aesthetic_pass_claimed': False,
            'limitations': ['Figma native PNG and registered Sharp/Pillow final are different renderers; raw equality is not required.',
                            'Actual local host runtime log is required; portable replay without that local tool evidence is unsupported.',
                            'Only the inspected V22 collector invocation is accepted; future collectors need an explicit bounded update.'
                            if version == 22 else
                            'Only the inspected V23 direct collector invocation is accepted; V24 and later fail closed.'
                            if version == 23 else
                            'Only the inspected V24 direct collector invocation is accepted; V25 and later fail closed.'
                            if version == 24 else
                            'Only the inspected V25 direct collector invocation is accepted; V26 and later fail closed.'
                            if version == 25 else
                            'Only the inspected V26 direct collector invocation is accepted; V27 and later fail closed.'
                            if version == 26 else
                            'Only the inspected V27 direct collector invocation is accepted; V28 and later fail closed.'
                            if version == 27 else
                            'Only the inspected V28 direct collector invocation is accepted; V29 and later fail closed.']}
