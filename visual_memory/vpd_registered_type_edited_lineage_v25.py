"""V25 thin adapter; exact reuse of the sealed V24 finite contour editor.

Original V25 input bytes have their own frozen profile. Only a deep copy's
version is mapped for the old interpreter. Maker code is never executed; copy
recognition and aesthetics still require actual image review.
"""
import copy
import json
import xml.etree.ElementTree as ET
from pathlib import Path

from visual_memory import vpd_registered_type_composite as g

KIND = 'alpha128-vtracer-edited/v1'
BASE_KERNEL = {'path': 'visual_memory/vpd_registered_type_edited_lineage.py',
               'sha256': 'a29d62e9888613594414c408233282fc3b29c5e724d576eaebc7c1bf81d014cd'}
BASE = 'evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v25/'
SEALED_EDIT = {'path': BASE + 'V25_GLYPH_EDIT_MANIFEST.json',
               'sha256': '9c4d0bc62f22b9e404f153247603340593d25acacec6365e4fe990ef7c650777'}
SEALED_MAKER = {'path': BASE + 'make_glyph_program.py',
                'sha256': '7d6c0846372e6cb6f040d6686ff67327b820e9f0dae2dbd944756fd3751b23f3'}
SEALED_BUILDER = {'path': BASE + 'build_headline_asset.py',
                  'sha256': '496109814afd254805744ee29e5d58bb5996abf92fd8ca3a5898d25bab0bc10f'}


def base_kernel(root):
    filename = str(Path(root) / BASE_KERNEL['path'])
    namespace = {'__file__': filename, '__name__': '_trusted_sealed_v24_kernel'}
    exec(compile(g.checked_bytes(root, BASE_KERNEL), filename, 'exec'), namespace)
    return namespace


def replay_edit_program(root, manifest):
    g.require(type(manifest.get('formal_version')) is int and manifest['formal_version'] == 25,
              'EDIT_LINEAGE_V25_ONLY')
    mapped = copy.deepcopy(manifest)
    mapped['formal_version'] = 24
    raw, report = base_kernel(root)['replay_edit_program'](root, mapped)
    report['formal_version'] = 25
    report['base_kernel'] = copy.deepcopy(BASE_KERNEL)
    report['version_mapping'] = 'V25 original retained; deep-copy formal_version25 to24 solely for sealed finite editor'
    return raw, report


def expected_lineage(root, adapter_reference):
    g.require(SEALED_EDIT is not None and SEALED_MAKER is not None and SEALED_BUILDER is not None,
              'V25_EDIT_PROFILE_NOT_SEALED')
    return {'kind': KIND, **copy.deepcopy(base_kernel(root)['INPUTS']),
            'edit_manifest': copy.deepcopy(SEALED_EDIT), 'maker_source': copy.deepcopy(SEALED_MAKER),
            'maker_builder': copy.deepcopy(SEALED_BUILDER), 'base_edit_kernel': copy.deepcopy(BASE_KERNEL),
            'edit_kernel': adapter_reference}


def validate(root, tree, lineage, formal_version, adapter_reference):
    g.require(formal_version == 25, 'EDIT_LINEAGE_V25_ONLY')
    g.require(lineage == expected_lineage(root, adapter_reference), 'V25_EDIT_PROFILE_CHANGED')
    for key, reference in lineage.items():
        if key != 'kind':
            g.checked_bytes(root, reference)
    raw, report = replay_edit_program(root, json.loads(g.checked_bytes(root, SEALED_EDIT)))
    def semantic(node):
        return [(n.tag, sorted(n.attrib.items()), (n.text or '').strip(), (n.tail or '').strip()) for n in node.iter()]
    g.require(semantic(tree) == semantic(ET.fromstring(raw)), 'EDIT_FINAL_SVG_REPLAY_MISMATCH')
    return report
