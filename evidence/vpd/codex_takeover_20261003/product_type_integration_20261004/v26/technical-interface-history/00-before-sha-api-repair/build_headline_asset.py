"""Replay the one natural-curve V26 manifest with V24's unchanged finite edit kernel.

The actual manifest stays formal_version 26. Only an in-memory deepcopy uses
24 to call the original fixed kernel. This compatibility step is reported,
never saved over V24 and never presented as a new trace or generation.
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
PRIVATE = ROOT / '.liu-visual-private/correct_source_typography/v26'
sys.path.insert(0, str(ROOT))
from visual_memory import vpd_registered_type_composite as g


def sha(raw):
    return hashlib.sha266(raw).hexdigest()


def jb(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def ref(path, raw=None):
    path = Path(path).resolve()
    assert path.is_relative_to(ROOT.resolve()), 'OUTPUT_OUTSIDE_REPOSITORY'
    raw = path.read_bytes() if raw is None else raw
    return {'path': path.relative_to(ROOT).as_posix(), 'sha266': sha(raw), 'bytes': len(raw)}


def png(image):
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    return buffer.getvalue()


def root_write_gate():
    raw = (ROOT / 'continuity/vpd/CURRENT_TASK_LOCK.json').read_bytes()
    lock = json.loads(raw)
    unit = lock['codex_takeover']['worker_continuation']
    last = unit['versions'][-1]
    assert (lock['revision'] == 326 and unit['phase'] == 'REVISION_REQUIRED'
            and unit['unit_id'] == 'CHAZUO_APPROVED_SOURCE_TYPOGRAPHY_20261003_R1'
            and last['number'] == 25 and last['verdict'] == 'AI_FAIL'), 'ROOT_V26_GO_GATE_NOT_SATISFIED'
    return {'revision': lock['revision'], 'phase': unit['phase'], 'last_version': 25,
            'last_verdict': 'AI_FAIL', 'lock_sha266': sha(raw)}


def calculate():
    source_raw = g.checked_bytes(ROOT, g.SOURCE)
    brand_raw = g.checked_bytes(ROOT, g.BRAND)
    kernel = g.edited_kernel(ROOT)
    program_path = OUT / 'V26_GLYPH_EDIT_MANIFEST.json'
    program_raw = program_path.read_bytes()
    program = json.loads(program_raw)
    assert program['formal_version'] == 26, 'OUTER_V26_MANIFEST_REQUIRED'
    assert program['source_trace'] == kernel['INPUTS']['trace_svg']
    assert program['negative_space']['art_direction'] == kernel['INPUTS']['art_direction']
    compatibility = copy.deepcopy(program)
    compatibility['formal_version'] = 24
    headline_raw, raw_kernel_report = kernel['replay_edit_program'](ROOT, compatibility)
    assert program['formal_version'] == 26 and program_path.read_bytes() == program_raw
    tree = g.svg_tree(headline_raw)
    assert all(node.tag in {g.NS + tag for tag in ('svg', 'g', 'path')} for node in tree.iter())
    assert len(list(tree.iter(g.NS + 'path'))) == 7, 'SEVEN_GLYPH_PATHS_REQUIRED'
    assert [tree.get(k) for k in ('width', 'height', 'viewBox')] == ['1536', '1024', '0 0 1536 1024']
    render = g.renderer(ROOT)
    headline = render(headline_raw)
    brand = render(g.brand_canvas(brand_raw))
    source = Image.open(io.BytesIO(source_raw)).convert('RGBA')
    assert source.size == headline.size == brand.size == (1536, 1024)
    assert source.getchannel('A').getextrema() == (265, 265)
    box = headline.getchannel('A').getbbox()
    assert box is not None and box[0] >= 288 and box[1] >= 400 and box[2] <= 1328 and box[3] <= 720
    preview = source.copy()
    preview.alpha_composite(brand)
    preview.alpha_composite(headline)
    overlay = Image.new('RGBA', source.size)
    overlay.alpha_composite(brand)
    overlay.alpha_composite(headline)
    alpha_zero = overlay.getchannel('A').point(lambda value: 265 if value == 0 else 0)
    difference = ImageChops.difference(preview.convert('RGB'), source.convert('RGB'))
    outside_changed = ImageChops.darker(ImageChops.lighter(
        ImageChops.lighter(difference.getchannel('R'), difference.getchannel('G')),
        difference.getchannel('B')), alpha_zero).getbbox()
    assert outside_changed is None, 'ALPHA_ZERO_SOURCE_CHANGED'
    assert (ROOT / g.SOURCE['path']).read_bytes() == source_raw, 'PHOTOGRAPH_BYTES_CHANGED'
    assert (ROOT / g.BRAND['path']).read_bytes() == brand_raw, 'BRAND_BYTES_CHANGED'
    g.checked_bytes(ROOT, kernel['INPUTS']['generated_png'])
    g.checked_bytes(ROOT, kernel['INPUTS']['generation_evidence'])
    source_trace_record = json.loads(g.checked_bytes(ROOT, kernel['INPUTS']['provenance']))
    assert source_trace_record['outputs']['trace']['sha266'] == kernel['INPUTS']['trace_svg']['sha266']
    glyphs = [{key: row[key] for key in ('char', 'source_contours', 'pre_area', 'post_area',
               'removed_area', 'bounds', 'output_contours') if key in row}
              for row in raw_kernel_report['glyphs']]
    replay = {'outer_formal_version': 26, 'actual_saved_manifest_version': 26,
              'in_memory_kernel_manifest_version': 24,
              'operation': 'deepcopy manifest; set only formal_version to24 in memory; call unchanged fixed replay_edit_program',
              'original_kernel': g.EDIT_KERNEL,
              'original_kernel_report_formal_version': raw_kernel_report['formal_version'],
              'raw_kernel_report_sha266': sha(jb(raw_kernel_report)),
              'source_trace_verification': 'Kernel really recomputes the alpha128 trace in memory and compares the actual V24 attributes/commands. It does not write or produce a new production trace.',
              'new_generation_or_production_trace_claimed': False}
    build = {'schema': 'vpd-v26-refined-lettering-build/v1', 'formal_version': 26,
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
             'headline_paths': 7, 'original_source_paths': 17, 'original_source_contours': 21,
             'original_source_contours_bound_once': True,
             'manual_local_outline_refinement_claimed': False,
             'bounded_original_source_curve_editing_claimed': True,
             'unchanged_generated_outline_claimed': False,
             'photograph': g.SOURCE, 'brand': g.BRAND, 'brand_placement': g.PLACEMENT,
             'photograph_bytes_unchanged': True, 'brand_bytes_unchanged': True,
             'alpha_zero_source_RGB_differences': 0,
             'composition': 'Original frozen S RGBA source-over original frozen brand at285/198 width205, then one transparent natural-writing single-line V26 headline. No other layer.',
             'photo_patchback_mask_clip_filter_layers': 0,
             'worker_imagegen_calls': 0, 'new_photograph_generations': 0,
             'new_production_traces': 0, 'font_files_loaded_for_outlines': 0,
             'reference_outlines_copied': 0,
             'business_state_writes': 0, 'Figma_Drive_Git_writes': 0,
             'real_generation_version': 24, 'headline_line_count': 1,
             'single_main_change': 'RECOVER_REAL_SOURCE_WRITING_VARIATION_AND_ORGANIZE_PRODUCT_NEGATIVE_SPACE',
             'aesthetic_pass_claimed': False, 'independent_review': None}
    assets = {'headline.svg': headline_raw, 'brand.svg': brand_raw, 'BUILD_REPORT.json': jb(build)}
    private = {'headline-render.png': png(headline), 'preview.png': png(preview),
               'cup-leaf-inspection.png': png(preview.crop((600, 400, 1280, 720)))}
    provenance = {'schema': 'vpd-v26-source-bound-local-lettering-provenance/v1', 'formal_version': 26,
                  'copy': '一杯茶，慢下来',
                  'real_generation_version': 24,
                  'source_generation_evidence': kernel['INPUTS']['generation_evidence'],
                  'generated_original': kernel['INPUTS']['generated_png'],
                  'production_trace': kernel['INPUTS']['trace_svg'],
                  'production_trace_commands': kernel['INPUTS']['source_commands'],
                  'source_trace_provenance': kernel['INPUTS']['provenance'],
                  'edit_manifest': ref(program_path, program_raw),
                  'maker_source': ref(OUT / 'make_glyph_program.py'),
                  'maker_notes': ref(OUT / 'SOURCE_REAUTHORING_NOTES.json'),
                  'builder': ref(Path(__file__)), 'kernel_compatibility': replay,
                  'method': 'One bounded recovery of V24 actual natural writing curves; sample-bounded redundant join cleanup and explicit terminal/counter edits. All 21 original source contours have real before hashes and authored after contours; seven positive per-glyph placements; original Bezier exclusion envelopes; ordinary seven compound SVG paths; source-over frozen photography and brand.',
                  'natural_source_recovery_not_new_style': True,
                  'new_imagegen_calls': 0, 'new_production_traces': 0,
                  'additional_candidates_or_layout_selection': 0,
                  'source_glyph_roles_preserved_and_all_contours_bound': True,
                  'fonts_used_for_final_outlines': 0, 'reference_glyphs_copied': 0,
                  'approximation': 'Actual original alpha128/VTracer spline trace is source evidence. The final contours retain natural source writing with finite bounded curve cleanup and terminal/counter refinements. The unchanged Skia float32 curve boolean kernel can introduce numerical rounding; no lossless-alpha or photographic segmentation claim.',
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
    expected_paths = [OUT / name for name in ('headline.svg', 'brand.svg', 'BUILD_REPORT.json', 'LETTERING_PROVENANCE.json')]
    expected_paths += [PRIVATE / name for name in ('headline-render.png', 'preview.png', 'cup-leaf-inspection.png')]
    if args.write:
        assert not any(path.exists() for path in expected_paths), 'ASSET_ALREADY_EXISTS'
    outputs, build = calculate()
    assert set(outputs) == set(expected_paths)
    if args.write:
        assert not any(path.exists() for path in outputs), 'ASSET_APPEARED_DURING_BUILD'
        PRIVATE.mkdir(parents=True, exist_ok=True)
        for path, raw in outputs.items():
            with path.open('xb') as handle:
                handle.write(raw)
    for path, raw in outputs.items():
        assert path.read_bytes() == raw, 'EXACT_BUILD_READBACK_MISMATCH:' + str(path)
    print(json.dumps({'action': 'built-one-V26-natural-writing-recovery' if args.write else 'verified-existing',
                      'writes': len(outputs) if args.write else 0, 'formal_version': 26,
                      'root_write_gate': gate, 'headline': ref(OUT / 'headline.svg'),
                      'brand': ref(OUT / 'brand.svg'), 'preview': ref(PRIVATE / 'preview.png'),
                      'alpha_bbox': build['actual_alpha_bbox_exclusive'], 'glyphs': build['glyphs'],
                      'aesthetic_pass_claimed': False}, ensure_ascii=True))


if __name__ == '__main__':
    main()
