"""Actual V28 profile over the unchanged sealed V24 finite contour editor.

The original manifest retains version28; a deep copy maps to24 for the old
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
BASE = 'evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v28/'
SEALED_EDIT = {'path': 'evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v28/V28_GLYPH_EDIT_MANIFEST.json',
 'sha256': 'dbc3e543b00265602656b36baf249f9964688df23722279702cc6e326c421d48'}
SEALED_MAKER = {'path': 'evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v28/make_glyph_program.py',
 'sha256': '6e1e6d6953928e1f887560e5cda0290b3eca12c6276eee4cf9d1a05b79262983'}
SEALED_BUILDER = {'path': 'evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v28/build_headline_asset.py',
 'sha256': '7e19236ad9ee4c12a4aee5c981f134c5bae11fe23b2e787ea331b546e2bcedd6'}


SEALED_GEOMETRY = {'path': 'evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v28/ART_DIRECTION_V28_GEOMETRY.json',
 'sha256': 'e700bad285722764e7fc1370d6de8ecbaaf0618181a86fe8c2ec4cc53b8f4c0d',
 'bytes': 2861}

def base_kernel(root):
    filename = str(Path(root) / BASE_KERNEL['path'])
    namespace = {'__file__': filename, '__name__': '_trusted_sealed_v24_kernel'}
    exec(compile(g.checked_bytes(root, BASE_KERNEL), filename, 'exec'), namespace)
    original_inputs = copy.deepcopy(namespace['INPUTS'])
    original_direction = json.loads(g.checked_bytes(root, original_inputs['art_direction']))
    actual_direction = json.loads(g.checked_bytes(root, SEALED_GEOMETRY))
    g.require(actual_direction['negative_space']['cup_air'] == original_direction['negative_space']['cup_air'], 'V28_CUP_GEOMETRY_CHANGED')
    namespace['parse_closed'](actual_direction['negative_space']['leaf_air'])
    namespace['INPUTS'] = copy.deepcopy(original_inputs)
    namespace['INPUTS']['art_direction'] = copy.deepcopy(SEALED_GEOMETRY)
    return namespace


def replay_edit_program(root, manifest):
    g.require(type(manifest.get('formal_version')) is int and manifest['formal_version'] == 28,
              'EDIT_LINEAGE_V28_ONLY')
    mapped = copy.deepcopy(manifest)
    mapped['formal_version'] = 24
    raw, report = base_kernel(root)['replay_edit_program'](root, mapped)
    report['formal_version'] = 28
    report['base_kernel'] = copy.deepcopy(BASE_KERNEL)
    report['version_mapping'] = 'V28 original retained; deep-copy formal_version28 to24 solely for sealed finite editor'
    return raw, report


def expected_lineage(root, adapter_reference):
    return {'kind': KIND, **copy.deepcopy(base_kernel(root)['INPUTS']),
            'edit_manifest': copy.deepcopy(SEALED_EDIT), 'maker_source': copy.deepcopy(SEALED_MAKER),
            'maker_builder': copy.deepcopy(SEALED_BUILDER), 'base_edit_kernel': copy.deepcopy(BASE_KERNEL),
            'edit_kernel': adapter_reference}


def validate(root, tree, lineage, formal_version, adapter_reference):
    g.require(formal_version == 28, 'EDIT_LINEAGE_V28_ONLY')
    g.require(lineage == expected_lineage(root, adapter_reference), 'V28_EDIT_PROFILE_CHANGED')
    for key, reference in lineage.items():
        if key != 'kind':
            g.checked_bytes(root, reference)
    raw, report = replay_edit_program(root, json.loads(g.checked_bytes(root, SEALED_EDIT)))
    def semantic(node):
        return [(n.tag, sorted(n.attrib.items()), (n.text or '').strip(), (n.tail or '').strip()) for n in node.iter()]
    g.require(semantic(tree) == semantic(ET.fromstring(raw)), 'EDIT_FINAL_SVG_REPLAY_MISMATCH')
    return report
