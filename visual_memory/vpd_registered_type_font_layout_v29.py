"""Only the actual Root-frozen V29 font/brand source profile; no state or taste.

Re-extracts original glyph.draw geometry and recomputes the frozen line layout.
The approved wordmark's complete inner tree survives one uniform affine. Figma
runtime, graph and official export proof deliberately live outside this helper.
"""
import io
import json
import sys
import xml.etree.ElementTree as ET

from visual_memory import vpd_registered_type_composite as g

FONTTOOLS_SITE = 'C:/Users/Administrator/AppData/Local/hermes/hermes-agent/venv/Lib/site-packages'
sys.path.append(FONTTOOLS_SITE)
try:
    import fontTools
    from fontTools.ttLib import TTFont
    from fontTools.pens.recordingPen import RecordingPen
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.boundsPen import BoundsPen
finally:
    sys.path.remove(FONTTOOLS_SITE)

ROOT_INPUT = {'path': g.SERIES + 'v29/ROOT_FROZEN_INPUT_CONTRACT.json',
              'sha256': '868ba406085d69bf4919420e551977e690e6817789e651c49d113ab40c7bb2e5'}
KIND = 'source-han-serif-font-layout/v29'
ROLES = ('headline', 'description', 'english_hint')


def read_json(root, reference):
    return json.loads(g.checked_bytes(root, reference))


def contract(root):
    value = read_json(root, ROOT_INPUT)
    g.require(value['schema'] == 'vpd-root-frozen-copy-layout-reference/v1'
              and value['formal_version'] == value['min_version'] == 29
              and value['task_id'] == 'VPD-CHAZUO-CODEX-COMPLETE-POSTER-20261003-01'
              and value['unit_id'] == 'CHAZUO_APPROVED_SOURCE_TYPOGRAPHY_20261003_R1'
              and value['brand'] == value['copy_roles']['brand'] == '茶作'
              and value['dimensions'] == list(g.SIZE)
              and value['photography']['sha256'] == g.SOURCE['sha256']
              and value['brand_source']['sha256'] == g.BRAND['sha256']
              and value['font']['sha256'] == g.FONT_SHA
              and value['reference']['sha256'] == '9a29fbdc7dd908017924bed270e8dfe18351519eed3fa7bc7001789f2a383414'
              and value['state_writer'] == 'ROOT_EXECUTOR_ONLY'
              and value['worker_can_change_mainline'] is False
              and value['historical_copy_and_review_inputs_unchanged'] is True
              and value['copy'] == '\n'.join(value['copy_roles'][role] for role in ROLES),
              'V29_ROOT_FROZEN_INPUT_REQUIRED')
    for key in ('amendment', 'reference_clarification', 'reference', 'photography',
                'brand_source', 'font', 'producer_manifest', 'producer_source',
                'glyph_evidence', 'brand_evidence', 'brand_layer', 'headline_layer'):
        g.require(len(g.checked_bytes(root, value[key])) == value[key]['bytes'], 'V29_INPUT_BYTES_CHANGED:' + key)
    for reference in value['production_inputs']:
        g.require(len(g.checked_bytes(root, reference)) == reference['bytes'], 'V29_PRODUCTION_INPUT_CHANGED')
    producer = read_json(root, value['producer_manifest'])
    g.require(producer['copy'] == value['copy_roles'] and producer['layout'] == value['layout']
              and producer['font_foundation'] == value['font']
              and producer['vector_contract']['path_fills'] == value['palette'], 'V29_PRODUCER_CONTRACT_CONFLICT')
    return value


def expected_lineage(root, adapter_reference):
    value = contract(root)
    return {'kind': KIND, 'input_contract': ROOT_INPUT, 'font': value['font'],
            'provenance': value['producer_manifest'], 'producer_source': value['producer_source'],
            'glyph_evidence': value['glyph_evidence'], 'brand_evidence': value['brand_evidence'],
            'source_validator': adapter_reference, 'fonttools_version': '4.63.0'}


def numbers(values):
    return ' '.join(format(float(value), '.12g') for value in values)


def validate_brand(root, tree=None):
    value = contract(root)
    original = g.svg_tree(g.checked_bytes(root, value['brand_source']))
    placed = tree if tree is not None else g.svg_tree(g.checked_bytes(root, value['brand_layer']), formal_version=29)
    viewbox = [float(number) for number in original.get('viewBox').split()]
    placement = value['brand_placement']
    scale = placement['uniform_visible_width'] / viewbox[2]
    affine = [scale, 0, 0, scale, placement['ink_x'], placement['ink_y']]
    children = list(placed)
    g.require(placed.attrib == {'width': '1536', 'height': '1024', 'viewBox': '0 0 1536 1024'}
              and len(children) == 2 and children[0].tag == g.NS + 'title'
              and children[1].tag == g.NS + 'g'
              and children[1].attrib == {'id': 'chazuo-brand-placement', 'transform': 'matrix(' + numbers(affine) + ')'},
              'V29_UNIFORM_BRAND_PLACEMENT_CHANGED')
    g.require([g.semantic_sha(node) for node in children[1]] == [g.semantic_sha(node) for node in original]
              and len(list(placed.iter(g.NS + 'path'))) == value['path_count']['brand'] == 7,
              'V29_FROZEN_BRAND_INNER_CHANGED')
    evidence = read_json(root, value['brand_evidence'])
    g.require(evidence['source'] == value['brand_source'] and evidence['source_viewbox'] == viewbox
              and evidence['uniform_group_affine'] == affine and evidence['outline_modified'] is False
              and evidence['leaf_independently_repositioned'] is False, 'V29_BRAND_EVIDENCE_CONFLICT')
    return {'paths': 7, 'uniform_affine': affine, 'source_inner_unchanged': True}


def validate(root, tree, lineage, formal_version, adapter_reference):
    g.require(type(formal_version) is int and formal_version == 29, 'FONT_LAYOUT_V29_ONLY')
    g.require(lineage == expected_lineage(root, adapter_reference), 'V29_FONT_LAYOUT_PROFILE_CHANGED')
    value = contract(root)
    evidence = read_json(root, value['glyph_evidence'])
    g.require(fontTools.__version__ == '4.63.0', 'FONTTOOLS_GEOMETRY_RUNTIME_CHANGED')
    g.require(evidence['schema'] == 'v29-original-font-outline-recording/v1'
              and evidence['font'] == value['font'] and evidence['automatic_shaping_used'] is False,
              'V29_ACTUAL_FONT_EVIDENCE_REQUIRED')
    sources = {}
    expected_groups, expected_lines = [], []
    with TTFont(io.BytesIO(g.checked_bytes(root, value['font'])), lazy=True) as font:
        glyphset, cmap, upem = font.getGlyphSet(), font.getBestCmap(), font['head'].unitsPerEm
        versions = [name.toUnicode() for name in font['name'].names if name.nameID == 5]
        g.require(upem == evidence['units_per_em'] == 1000
                  and versions == evidence['font_version_from_name_table']
                  and 'Version 2.003;hotconv 1.1.1;makeotfexe 2.6.0' in versions, 'V29_FONT_VERSION_CHANGED')
        def source(char):
            if char not in sources:
                name = cmap[ord(char)]
                glyph, recording = glyphset[name], RecordingPen()
                glyph.draw(recording)
                g.require(not any(op == 'addComponent' for op, _ in recording.value), 'V29_COMPOSITE_GLYPH_UNSUPPORTED')
                pen, direct, bounds = SVGPathPen(glyphset), SVGPathPen(glyphset), BoundsPen(glyphset)
                recording.replay(pen); glyph.draw(direct); recording.replay(bounds)
                commands = pen.getCommands()
                g.require(commands == direct.getCommands(), 'V29_ORIGINAL_GLYPH_REPLAY_CHANGED')
                operations = json.dumps(recording.value, separators=(',', ':')).encode('utf-8')
                sources[char] = {'character': char, 'unicode': f'U+{ord(char):04X}', 'codepoint': ord(char),
                    'cmap_glyph_name': name, 'glyph_id': font.getGlyphID(name), 'hmtx_advance_font_units': glyph.width,
                    'bounds_font_units': list(bounds.bounds) if bounds.bounds else None,
                    'recording_pen_operations': json.loads(operations), 'recording_pen_sha256': g.sha(operations),
                    'svg_path_pen_original_commands': commands, 'svg_command_sha256': g.sha(commands.encode('utf-8')),
                    'contour_count': sum(op == 'closePath' for op, _ in recording.value),
                    'direct_glyph_draw_and_recording_replay_commands_identical': True, 'outline_modifications': []}
            return sources[char]
        for role in ROLES:
            text, spec = value['copy_roles'][role], value['layout'][role]
            scale = spec['font_size_px'] / upem
            glyphs = [source(char) for char in text]
            baseline = spec['ink_top'] + max(item['bounds_font_units'][3] for item in glyphs if item['bounds_font_units']) * scale
            pen_x = spec['ink_x'] - glyphs[0]['bounds_font_units'][0] * scale
            group = ET.Element(g.NS + 'g', {'id': role})
            instances, transformed_bounds = [], []
            for index, (char, item) in enumerate(zip(text, glyphs)):
                if index:
                    pen_x += spec.get('pair_adjustments_px', {}).get(text[index - 1] + char, 0)
                affine = [scale, 0, 0, -scale, pen_x, baseline]
                pid, bounds = f'{role}-u{ord(char):04x}-{index:02d}', item['bounds_font_units']
                ink = None
                if bounds:
                    ink = [pen_x + bounds[0] * scale, baseline - bounds[3] * scale,
                           pen_x + bounds[2] * scale, baseline - bounds[1] * scale]
                    transformed_bounds.append(ink)
                    ET.SubElement(group, g.NS + 'path', {'id': pid, 'data-character': char,
                        'data-source-glyph': item['cmap_glyph_name'], 'd': item['svg_path_pen_original_commands'],
                        'transform': 'matrix(' + numbers(affine) + ')', 'fill': spec['fill']})
                advance = spec['advance_overrides_px'].get(char, item['hmtx_advance_font_units'] * scale)
                tracking = spec['tracking_px'] if index < len(text) - 1 else 0
                instances.append({'index': index, 'character': char, 'unicode': item['unicode'],
                    'cmap_glyph_name': item['cmap_glyph_name'], 'source_command_sha256': item['svg_command_sha256'],
                    'path_id': pid if bounds else None, 'affine': affine, 'ink_bounds_px': ink,
                    'source_advance_px': item['hmtx_advance_font_units'] * scale, 'used_advance_px': advance,
                    'following_tracking_px': tracking, 'outline_modified': False})
                pen_x += advance + tracking
            line_bounds = [min(row[0] for row in transformed_bounds), min(row[1] for row in transformed_bounds),
                           max(row[2] for row in transformed_bounds), max(row[3] for row in transformed_bounds)]
            expected_groups.append(group)
            expected_lines.append({'role': role, 'text': text, 'regular_font_role': True, 'custom_wordmark_claim': False,
                                   'spec': spec, 'baseline_px': baseline, 'ink_bounds_px': line_bounds, 'glyph_instances': instances})
    g.require(evidence['unique_glyph_sources'] == list(sources.values()), 'V29_ORIGINAL_FONT_SOURCE_CHANGED')
    g.require(evidence['lines'] == expected_lines, 'V29_FONT_LAYOUT_EVIDENCE_CHANGED')
    children = list(tree)
    g.require(tree.attrib == {'width': '1536', 'height': '1024', 'viewBox': '0 0 1536 1024'}
              and len(children) == 4 and children[0].tag == g.NS + 'title'
              and all(node.tag == g.NS + 'g' and node.attrib == {'id': role}
                      for node, role in zip(children[1:], ROLES)), 'V29_COPY_LAYOUT_GROUPS_CHANGED')
    g.require([g.semantic_sha(node) for node in children[1:]] == [g.semantic_sha(node) for node in expected_groups]
              and len(list(tree.iter(g.NS + 'path'))) == value['path_count']['headline'] == 35,
              'V29_ORIGINAL_FONT_PATHS_CHANGED')
    brand = validate_brand(root)
    return {'source_font_originals_reextracted': len(sources), 'font_paths': 35,
            'character_instances': sum(len(line['glyph_instances']) for line in expected_lines),
            'brand': brand, 'root_input': ROOT_INPUT, 'aesthetic_pass_claimed': False}
