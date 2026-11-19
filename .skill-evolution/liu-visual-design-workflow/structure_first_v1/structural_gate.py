#!/usr/bin/env python3
"""Isolated, structure-first Chinese lettering research gate.
Only tests *technical eligibility*. It cannot assert visual/aesthetic quality.
Does not invoke any generator, mutate Figma or touch production state.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

GLYPHS = tuple('地图以外')
REFERENCE_SHA = '690ecf6950db3abc8f123a690357a0b5b2e44ab985b3ac3cdf3184cd2bea2b04'
BASELINE_SHA = 'd9f9987ce5533be407aeec2b41f4b551e710980f8bee1054bca914c815d08f8e'
DENY_SVG_TAGS = {'image', 'filter', 'pattern', 'foreignObject', 'text', 'tspan', 'use'}


def file_hash(path):
    p = Path(path) if path else None
    return hashlib.sha256(p.read_bytes()).hexdigest() if p is not None and p.is_file() else None


def evaluate(manifest: dict) -> dict:
    reasons = []
    def deny(code):
        if code not in reasons: reasons.append(code)

    if manifest.get('target') != ''.join(GLYPHS): deny('TEXT_NOT_FROZEN')
    if manifest.get('scope') != 'ISOLATED_RESEARCH': deny('SCOPE_NOT_ISOLATED')
    if manifest.get('method') != 'CUSTOM_VECTOR_STRUCTURE_FIRST': deny('UNCONTROLLED_IMAGEGEN_METHOD')
    if manifest.get('render_stage') != 'STRUCTURE_ONLY': deny('STAGE_NOT_STRUCTURE_ONLY')
    if manifest.get('reference_sha256') != REFERENCE_SHA or file_hash(manifest.get('reference_path')) != REFERENCE_SHA:
        deny('REFERENCE_NOT_BOUND_TO_ACTUAL_BYTES')
    if manifest.get('baseline_sha256') != BASELINE_SHA or file_hash(manifest.get('baseline_path')) != BASELINE_SHA:
        deny('BASELINE_NOT_BOUND_TO_ACTUAL_BYTES')
    if manifest.get('explicit_new_image_authorization') is not True: deny('NO_NEW_RENDER_AUTHORIZATION')
    if manifest.get('new_candidate_limit') != 1 or manifest.get('reused_candidate_count') != 0: deny('CANDIDATE_BUDGET_EXCEEDED')
    if manifest.get('preserve_originals') is not True: deny('ORIGINAL_PRESERVATION_NOT_VERIFIED')
    if manifest.get('glyph_plan') != [
        {'glyph': '地', 'role': 'entry'},
        {'glyph': '图', 'role': 'boundary'},
        {'glyph': '以', 'role': 'exit'},
        {'glyph': '外', 'role': 'release'},
    ]: deny('FOUR_GLYPH_ROLES_NOT_FROZEN')
    if manifest.get('interglyph_mechanism') != 'BOUNDARY_EXIT_FROM_TU_TO_YI':
        deny('STRUCTURAL_RELATION_NOT_FROZEN')
    if manifest.get('texture_enabled') is not False: deny('TEXTURE_MUST_WAIT_FOR_STRUCTURE_APPROVAL')
    if manifest.get('human_structure_verdict') == 'APPROVED':
        deny('CANNOT_ASSUME_HUMAN_APPROVAL_BEFORE_OUTPUT')

    path = Path(manifest['structural_candidate_path']) if manifest.get('structural_candidate_path') else None
    if not path or not path.is_file():
        deny('NO_STRUCTURAL_CANDIDATE')
    elif path.suffix.lower() != '.svg':
        deny('STAGE_A_REQUIRES_NATIVE_VECTOR_NOT_RASTER')
    else:
        try:
            root = ET.parse(path).getroot()
            def local(tag): return tag.rsplit('}',1)[-1]
            if local(root.tag) != 'svg': deny('NOT_AN_SVG')
            tags = [local(el.tag) for el in root.iter()]
            if set(tags) & DENY_SVG_TAGS: deny('RASTER_TEXT_OR_EFFECT_PRESENT')
            groups = {el.attrib.get('data-glyph'):el for el in root.iter() if local(el.tag)=='g' and el.attrib.get('data-glyph')}
            if set(groups.keys()) != set(GLYPHS): deny('GLYPH_GROUPS_MISSING_OR_WRONG')
            else:
                for char in GLYPHS:
                    paths = [el for el in groups[char].iter() if local(el.tag)=='path' and len(el.attrib.get('d',''))>10]
                    if not paths: deny('MISSING_AUTHORED_PATH_FOR_'+char)
            if sum(1 for t in tags if t=='path')<8: deny('NOT_ENOUGH_CUSTOM_VECTOR_PATHS')
            if any('url(' in ''.join(str(v) for v in el.attrib.values()) for el in root.iter()):
                deny('SVG_EFFECT_OR_EXTERNAL_RESOURCE')
        except (ET.ParseError, OSError, ValueError): deny('INVALID_SVG')
    return {'state': 'BLOCKED' if reasons else 'TECHNICAL_STAGE_A_ELIGIBLE_NOT_AESTHETIC_PASS',
            'reasons': reasons,'user_aesthetic_verdict':'NOT_REVIEWED',
            'authorization_to_texture':'NO', 'formal_rule_promoted':False}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--manifest',required=True)
    args=parser.parse_args()
    print(json.dumps(evaluate(json.loads(Path(args.manifest).read_text(encoding='utf-8'))),ensure_ascii=False,indent=2))


if __name__=='__main__': main()
