"""Actual V26 profile over the unchanged sealed V24 finite contour editor.

The original manifest retains version26; a deep copy maps to24 for the old
interpreter. Maker/builder bytes are bound as provenance, never executed.
"""
import copy
import json
import xml.etree.ElementTree as ET
from pathlib import Path

from visual_memory import vpd_registered_type_composite as g

KIND = 'alpha128-vtracer-edited/v1'
BASE_KERNEL = {'path': 'visual_memory/vpd_registered_type_edited_lineage.py',
               'sha256': 'a29d62e9888613594414c408233282fc3b29c5e724d576eaebc7c1bf81d014cd'}
BASE = 'evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v26/'
SEALED_EDIT = {'path': BASE + 'V26_GLYPH_EDIT_MANIFEST.json',
               'sha256': '0b2f0f6f64e1f2c3435630d1105572ad292d4e31be700ecee2334186c504d381'}
SEALED_MAKER = {'path': BASE + 'make_glyph_program.py',
                'sha256': '514e370da517fdb47981d02e4e11a914a68087bcd7c4c251cf18773212578b80'}
SEALED_BUILDER = {'path': BASE + 'build_headline_asset.py',
                  'sha256': '7ef28b93afd0e1ff2fc89e5d336849030ddb70b2b9041c7aba6aa9b6e9bc08f4'}


def base_kernel(root):
    filename = str(Path(root) / BASE_KERNEL['path'])
    namespace = {'__file__': filename, '__name__': '_trusted_sealed_v24_kernel'}
    exec(compile(g.checked_bytes(root, BASE_KERNEL), filename, 'exec'), namespace)
    return namespace


def replay_edit_program(root, manifest):
    g.require(type(manifest.get('formal_version')) is int and manifest['formal_version'] == 26,
              'EDIT_LINEAGE_V26_ONLY')
    mapped = copy.deepcopy(manifest)
    mapped['formal_version'] = 24
    raw, report = base_kernel(root)['replay_edit_program'](root, mapped)
    report['formal_version'] = 26
    report['base_kernel'] = copy.deepcopy(BASE_KERNEL)
    report['version_mapping'] = 'V26 original retained; deep-copy formal_version26 to24 solely for sealed finite editor'
    return raw, report


def expected_lineage(root, adapter_reference):
    return {'kind': KIND, **copy.deepcopy(base_kernel(root)['INPUTS']),
            'edit_manifest': copy.deepcopy(SEALED_EDIT), 'maker_source': copy.deepcopy(SEALED_MAKER),
            'maker_builder': copy.deepcopy(SEALED_BUILDER), 'base_edit_kernel': copy.deepcopy(BASE_KERNEL),
            'edit_kernel': adapter_reference}


def validate(root, tree, lineage, formal_version, adapter_reference):
    g.require(formal_version == 26, 'EDIT_LINEAGE_V26_ONLY')
    g.require(lineage == expected_lineage(root, adapter_reference), 'V26_EDIT_PROFILE_CHANGED')
    for key, reference in lineage.items():
        if key != 'kind':
            g.checked_bytes(root, reference)
    raw, report = replay_edit_program(root, json.loads(g.checked_bytes(root, SEALED_EDIT)))
    def semantic(node):
        return [(n.tag, sorted(n.attrib.items()), (n.text or '').strip(), (n.tail or '').strip()) for n in node.iter()]
    g.require(semantic(tree) == semantic(ET.fromstring(raw)), 'EDIT_FINAL_SVG_REPLAY_MISMATCH')
    return report
