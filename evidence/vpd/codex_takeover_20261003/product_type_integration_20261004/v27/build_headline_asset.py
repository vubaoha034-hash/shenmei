"""Build V27 once with the unchanged V24 finite contour kernel.

Keep the saved manifest identity 27; use formal_version 24 only in a memory copy.
No photograph alteration, masks, font outlines, production trace or business write.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import io
import json
import sys

sys.dont_write_bytecode = True
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
PRIVATE = ROOT / '.liu-visual-private/correct_source_typography/v27'
sys.path.insert(0, str(ROOT))
from visual_memory import vpd_registered_type_composite as g


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def jb(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def ref(path, raw=None):
    path = Path(path).resolve()
    assert path.is_relative_to(ROOT.resolve()), 'OUTPUT_OUTSIDE_REPOSITORY'
    raw = path.read_bytes() if raw is None else raw
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': sha(raw), 'bytes': len(raw)}


def png(image):
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    return buffer.getvalue()


def root_write_gate():
    raw = (ROOT / 'continuity/vpd/CURRENT_TASK_LOCK.json').read_bytes()
    lock = json.loads(raw)
    unit = lock['codex_takeover']['worker_continuation']
    last = unit['versions'][-1]
    assert (lock['revision'] == 328 and unit['phase'] == 'REVISION_REQUIRED'
            and unit['unit_id'] == 'CHAZUO_APPROVED_SOURCE_TYPOGRAPHY_20261003_R1'
            and last['number'] == 26 and last['verdict'] == 'AI_FAIL'), 'ROOT_V27_GO_GATE_NOT_SATISFIED'
    return {'revision': 328, 'phase': unit['phase'], 'last_version': 26,
            'last_verdict': 'AI_FAIL', 'lock_sha256': sha(raw), 'explicit_root_go': 'GO_V27'}


def calculate():
    source_raw = g.checked_bytes(ROOT, g.SOURCE)
    brand_raw = g.checked_bytes(ROOT, g.BRAND)
    kernel = g.edited_kernel(ROOT)
    program_path = OUT / 'V27_GLYPH_EDIT_MANIFEST.json'
    program_raw = program_path.read_bytes()
    program = json.loads(program_raw)
    assert program['formal_version'] == 27, 'OUTER_V27_MANIFEST_REQUIRED'
    assert program['source_trace'] == kernel['INPUTS']['trace_svg']
    assert program['negative_space']['art_direction'] == kernel['INPUTS']['art_direction']
    compatibility = copy.deepcopy(program)
    compatibility['formal_version'] = 24
    headline_raw, raw_kernel_report = kernel['replay_edit_program'](ROOT, compatibility)
    assert program['formal_version'] == 27 and program_path.read_bytes() == program_raw
    glyphs = [{key: row[key] for key in ('char', 'source_contours', 'pre_area', 'post_area',
              'removed_area', 'bounds', 'output_contours') if key in row}
             for row in raw_kernel_report['glyphs']]
    # Boolean re-expression changes floating area integration by <1e-3 px² even
    # for disjoint paths. Test the actual intersection instead of subtracting it.
    library = kernel['pathops_runtime'](ROOT)
    direction = json.loads(kernel['checked'](ROOT, kernel['INPUTS']['art_direction']))
    cup = kernel['make_path'](library, kernel['parse_closed'](direction['negative_space']['cup_air']))
    leaf = kernel['make_path'](library, kernel['parse_closed'](direction['negative_space']['leaf_air']))
    air = library.op(cup, leaf, library.PathOp.UNION, **kernel['FLAGS'])
    intersection_checks = []
    for row in raw_kernel_report['glyphs']:
        pre = kernel['make_path'](library, kernel['parse_closed'](row['pre_difference_d']))
        intersection = library.op(pre, air, library.PathOp.INTERSECTION, **kernel['FLAGS'])
        count = sum(1 for unused in intersection.contours)
        assert intersection.area == 0 and count == 0, 'REQUIRED_STROKE_RISK_FROM_OBJECT_EXCLUSION'
        intersection_checks.append({'char': row['char'], 'intersection_area': intersection.area,
                                    'intersection_contours': count,
                                    'reported_float_area_delta': row['removed_area']})
    tree = g.svg_tree(headline_raw)
    assert all(node.tag in {g.NS + tag for tag in ('svg', 'g', 'path')} for node in tree.iter())
    assert len(list(tree.iter(g.NS + 'path'))) == 7, 'SEVEN_GLYPH_PATHS_REQUIRED'
    assert [tree.get(k) for k in ('width', 'height', 'viewBox')] == ['1536', '1024', '0 0 1536 1024']
    render = g.renderer(ROOT)
    headline = render(headline_raw)
    brand = render(g.brand_canvas(brand_raw))
    source = Image.open(io.BytesIO(source_raw)).convert('RGBA')
    assert source.size == headline.size == brand.size == (1536, 1024)
    assert source.getchannel('A').getextrema() == (255, 255)
    box = headline.getchannel('A').getbbox()
    assert box is not None and box[0] >= 288 and box[1] >= 400 and box[2] <= 1328 and box[3] <= 720
    preview = source.copy()
    preview.alpha_composite(brand)
    preview.alpha_composite(headline)
    overlay = Image.new('RGBA', source.size)
    overlay.alpha_composite(brand)
    overlay.alpha_composite(headline)
    alpha_zero = overlay.getchannel('A').point(lambda value: 255 if value == 0 else 0)
    difference = ImageChops.difference(preview.convert('RGB'), source.convert('RGB'))
    outside_changed = ImageChops.darker(ImageChops.lighter(
        ImageChops.lighter(difference.getchannel('R'), difference.getchannel('G')),
        difference.getchannel('B')), alpha_zero).getbbox()
    assert outside_changed is None, 'ALPHA_ZERO_SOURCE_CHANGED'
    assert (ROOT / g.SOURCE['path']).read_bytes() == source_raw, 'PHOTOGRAPH_BYTES_CHANGED'
    assert (ROOT / g.BRAND['path']).read_bytes() == brand_raw, 'BRAND_BYTES_CHANGED'
    g.checked_bytes(ROOT, kernel['INPUTS']['generated_png'])
    g.checked_bytes(ROOT, kernel['INPUTS']['generation_evidence'])
    trace_record = json.loads(g.checked_bytes(ROOT, kernel['INPUTS']['provenance']))
    assert trace_record['outputs']['trace']['sha256'] == kernel['INPUTS']['trace_svg']['sha256']
    replay = {'outer_formal_version': 27, 'actual_saved_manifest_version': 27,
              'in_memory_kernel_manifest_version': 24,
              'operation': 'deepcopy manifest; set only formal_version to24 in memory; call unchanged fixed replay_edit_program',
              'original_kernel': g.EDIT_KERNEL,
              'original_kernel_report_formal_version': raw_kernel_report['formal_version'],
              'raw_kernel_report_sha256': sha(jb(raw_kernel_report)),
              'source_trace_verification': 'Kernel recomputes the fixed alpha128 source trace in memory and checks V24 attributes/commands; no new production trace is written.',
              'new_generation_or_production_trace_claimed': False}
    build = {'schema': 'vpd-v27-product-organized-lettering-build/v1', 'formal_version': 27,
             'copy': '一杯茶，慢下来', 'program': ref(program_path, program_raw),
             'source_generation_evidence': kernel['INPUTS']['generation_evidence'],
             'source_png': kernel['INPUTS']['generated_png'],
             'source_trace': kernel['INPUTS']['trace_svg'],
             'source_trace_commands': kernel['INPUTS']['source_commands'],
             'source_trace_record': kernel['INPUTS']['provenance'],
             'maker_source': ref(OUT / 'make_glyph_program.py'),
             'maker_notes': ref(OUT / 'SOURCE_REAUTHORING_NOTES.json'),
             'builder': ref(Path(__file__)), 'kernel_compatibility': replay,
             'glyphs': glyphs, 'actual_alpha_bbox_exclusive': list(box),
             'object_exclusion_intersection_checks': intersection_checks,
             'headline_paths': 7, 'original_source_paths': 17, 'original_source_contours': 21,
             'original_source_contours_bound_once': True,
             'manual_local_outline_refinement_claimed': True,
             'bounded_original_source_curve_editing_claimed': True,
             'unchanged_generated_outline_claimed': False,
             'photograph': g.SOURCE, 'brand': g.BRAND, 'brand_placement': g.PLACEMENT,
             'photograph_bytes_unchanged': True, 'brand_bytes_unchanged': True,
             'alpha_zero_source_RGB_differences': 0,
             'composition': 'Frozen S source-over frozen brand at285/198 width205, then the one transparent seven-compound V27 cup/leaf/platter headline. No other layer.',
             'photo_patchback_mask_clip_filter_layers': 0,
             'worker_imagegen_calls': 0, 'new_photograph_generations': 0,
             'new_production_traces': 0, 'font_files_loaded_for_outlines': 0,
             'reference_outlines_copied': 0, 'business_state_writes': 0,
             'Figma_Drive_Git_writes': 0, 'real_generation_version': 24,
             'headline_phrase_group_count': 2,
             'single_main_change': 'CUP_ARC_LEAF_FALLING_TERMINAL_AND_DESCENDING_PLATTER_PHRASE',
             'aesthetic_pass_claimed': False, 'independent_review': None}
    assets = {'headline.svg': headline_raw, 'brand.svg': brand_raw, 'BUILD_REPORT.json': jb(build)}
    private = {'headline-render.png': png(headline), 'preview.png': png(preview),
               'cup-leaf-inspection.png': png(preview.crop((288, 400, 1328, 720)))}
    provenance = {'schema': 'vpd-v27-source-bound-local-lettering-provenance/v1', 'formal_version': 27,
                  'copy': '一杯茶，慢下来', 'real_generation_version': 24,
                  'source_generation_evidence': kernel['INPUTS']['generation_evidence'],
                  'generated_original': kernel['INPUTS']['generated_png'],
                  'production_trace': kernel['INPUTS']['trace_svg'],
                  'production_trace_commands': kernel['INPUTS']['source_commands'],
                  'source_trace_provenance': kernel['INPUTS']['provenance'],
                  'edit_manifest': ref(program_path, program_raw),
                  'maker_source': ref(OUT / 'make_glyph_program.py'),
                  'maker_notes': ref(OUT / 'SOURCE_REAUTHORING_NOTES.json'),
                  'builder': ref(Path(__file__)), 'kernel_compatibility': replay,
                  'method': 'Reuse natural V24 source curves and fixed V26 housekeeping; author one smooth One cup arc and one complete Tea falling component, then place two cup/platter phrase groups. All21 before contours bound once; ordinary seven closed compound paths; actual intersection with original object exclusions empty.',
                  'natural_source_recovery_not_new_style': True,
                  'new_imagegen_calls': 0, 'new_production_traces': 0,
                  'additional_candidates_or_layout_selection': 0,
                  'source_glyph_roles_preserved_and_all_contours_bound': True,
                  'fonts_used_for_final_outlines': 0, 'reference_glyphs_copied': 0,
                  'approximation': 'Actual fixed alpha128/VTracer source evidence and Skia float32 Bezier operations; locally reauthored Tea stroke is not lossless source alpha; no photographic segmentation claim.',
                  'outputs': {name: ref(OUT / name, raw) for name, raw in assets.items()},
                  'private_outputs': {name: ref(PRIVATE / name, raw) for name, raw in private.items()},
                  'photograph': g.SOURCE, 'brand': g.BRAND, 'brand_placement': g.PLACEMENT,
                  'business_state_writes': 0, 'Figma_Drive_Git_writes': 0,
                  'aesthetic_pass_claimed': False, 'human_acceptance_claimed': False}
    assets['LETTERING_PROVENANCE.json'] = jb(provenance)
    return ({**{OUT / name: raw for name, raw in assets.items()},
             **{PRIVATE / name: raw for name, raw in private.items()}}, build)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--write', action='store_true')
    modes.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    gate = root_write_gate() if args.write else None
    expected = [OUT / name for name in ('headline.svg', 'brand.svg', 'BUILD_REPORT.json', 'LETTERING_PROVENANCE.json')]
    expected += [PRIVATE / name for name in ('headline-render.png', 'preview.png', 'cup-leaf-inspection.png')]
    if args.write:
        assert not any(path.exists() for path in expected), 'ASSET_ALREADY_EXISTS'
    outputs, build = calculate()
    assert set(outputs) == set(expected)
    if args.write:
        assert not any(path.exists() for path in outputs), 'ASSET_APPEARED_DURING_BUILD'
        PRIVATE.mkdir(parents=True, exist_ok=True)
        for path, raw in outputs.items():
            with path.open('xb') as handle:
                handle.write(raw)
    for path, raw in outputs.items():
        assert path.read_bytes() == raw, 'EXACT_BUILD_READBACK_MISMATCH:' + str(path)
    print(json.dumps({'action': 'built-one-V27-product-organized-writing' if args.write else 'verified-existing',
                      'writes': len(outputs) if args.write else 0, 'formal_version': 27,
                      'root_write_gate': gate, 'headline': ref(OUT / 'headline.svg'),
                      'brand': ref(OUT / 'brand.svg'), 'preview': ref(PRIVATE / 'preview.png'),
                      'alpha_bbox': build['actual_alpha_bbox_exclusive'], 'glyphs': build['glyphs'],
                      'aesthetic_pass_claimed': False}, ensure_ascii=True))


if __name__ == '__main__':
    main()
