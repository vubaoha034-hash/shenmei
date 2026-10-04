"""V24 fixed-kernel replay, transparent render and frozen-photo inspection.

Only the authored JSON program supplies edited geometry.  The fixed guard
kernel independently checks source contours and performs exact curve booleans.
This worker does not register business state or write Figma/Drive/final poster.
"""
from pathlib import Path
import argparse
import hashlib
import io
import json
import sys

sys.dont_write_bytecode = True
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
PRIVATE = ROOT / '.liu-visual-private/correct_source_typography/v24'
sys.path.insert(0, str(ROOT))
from visual_memory import vpd_registered_type_composite as g
from visual_memory.vpd_registered_type_edited_lineage import replay_edit_program


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


def root_gate():
    raw = (ROOT / 'continuity/vpd/CURRENT_TASK_LOCK.json').read_bytes()
    lock = json.loads(raw)
    unit = lock['codex_takeover']['worker_continuation']
    last = unit['versions'][-1]
    assert (lock['revision'] >= 322 and unit['phase'] == 'REVISION_REQUIRED'
            and unit['unit_id'] == 'CHAZUO_APPROVED_SOURCE_TYPOGRAPHY_20261003_R1'
            and last['number'] == 23 and last['verdict'] == 'AI_FAIL'), 'ROOT_V24_GO_GATE_NOT_SATISFIED'
    return {'revision': lock['revision'], 'phase': unit['phase'], 'last_version': last['number'],
            'verdict': last['verdict'], 'lock_sha256': sha(raw)}


def calculate():
    source_raw = g.checked_bytes(ROOT, g.SOURCE)
    brand_raw = g.checked_bytes(ROOT, g.BRAND)
    program_path = OUT / 'V24_GLYPH_EDIT_MANIFEST.json'
    program_raw = program_path.read_bytes()
    program = json.loads(program_raw)
    headline_raw, kernel_report = replay_edit_program(ROOT, program)
    tree = g.svg_tree(headline_raw)
    assert len(list(tree.iter(g.NS + 'path'))) == 7, 'SEVEN_GLYPH_PATHS_REQUIRED'
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
    execution = json.loads((OUT / 'IMAGEGEN_EXECUTION.json').read_bytes())
    g.checked_bytes(ROOT, execution['preserved_source_copy'])
    glyph_report = []
    for row in kernel_report['glyphs']:
        glyph_report.append({key: row[key] for key in
            ('char', 'pre_area', 'post_area', 'removed_area', 'bounds', 'output_contours') if key in row})
    build = {'schema': 'vpd-v24-edited-lettering-build/v1', 'formal_version': 24,
             'copy': '一杯茶，慢下来', 'program': ref(program_path, program_raw),
             'source_generation_evidence': ref(OUT / 'IMAGEGEN_EXECUTION.json'),
             'source_png': execution['preserved_source_copy'],
             'source_trace': ref(OUT / 'upstream-alpha128-trace.svg'),
             'source_trace_record': ref(OUT / 'SOURCE_TRACE.json'),
             'maker_program_source': ref(OUT / 'make_glyph_program.py'),
             'builder': ref(Path(__file__)),
             'independent_kernel': ref(ROOT / 'visual_memory/vpd_registered_type_edited_lineage.py'),
             'kernel_report_sha256': sha(jb(kernel_report)), 'glyphs': glyph_report,
             'actual_alpha_bbox_exclusive': list(box), 'headline_paths': 7,
             'geometry_lineage_kind': 'alpha128-vtracer-edited/v1',
             'actual_nonempty_original_trace_paths': 17,
             'manual_outline_edits_claimed': True,
             'unchanged_generated_outline_claimed': False,
             'photograph': g.SOURCE, 'brand': g.BRAND, 'brand_placement': g.PLACEMENT,
             'photograph_bytes_unchanged': True, 'brand_bytes_unchanged': True,
             'alpha_zero_source_RGB_differences': 0,
             'composition': 'Frozen S RGBA source-over frozen brand at285/198 width205, then edited transparent headline. No other layer.',
             'photo_patchback_mask_clip_filter_layers': 0,
             'worker_imagegen_calls': 0, 'new_photograph_generations': 0,
             'business_state_writes': 0, 'Figma_Drive_Git_writes': 0,
             'aesthetic_pass_claimed': False, 'independent_review': None}
    assets = {'headline.svg': headline_raw, 'brand.svg': brand_raw,
              'BUILD_REPORT.json': jb(build)}
    private = {'headline-render.png': png(headline), 'preview.png': png(preview),
               'cup-leaf-inspection.png': png(preview.crop((600, 410, 1260, 720)))}
    provenance = {'schema': 'vpd-v24-manually-edited-lettering-provenance/v1', 'formal_version': 24,
                  'copy': '一杯茶，慢下来', 'source_generation_evidence': ref(OUT / 'IMAGEGEN_EXECUTION.json'),
                  'generated_original': execution['preserved_source_copy'],
                  'trace': ref(OUT / 'upstream-alpha128-trace.svg'),
                  'edit_manifest': ref(program_path, program_raw),
                  'maker_source': ref(OUT / 'make_glyph_program.py'),
                  'maker_authorship_notes': ref(OUT / 'SOURCE_REAUTHORING_NOTES.json'),
                  'builder': ref(Path(__file__)),
                  'kernel': ref(ROOT / 'visual_memory/vpd_registered_type_edited_lineage.py'),
                  'method': 'One real Root-generated original, one preserved production trace; source-bound manual contour replacement with explicit before hashes and closed after data; positive per-glyph placement; native curve union/difference; source-over frozen photography and brand.',
                  'original_source_paths_unchanged_in_final': False,
                  'source_glyph_roles_preserved_and_all_contours_bound': True,
                  'additional_candidates_or_rerolls': 0, 'fonts_used_for_final_outlines': 0,
                  'reference_glyphs_copied': 0,
                  'approximation': 'Alpha128 spline tracing approximates the source alpha. Edited contours are authored reinterpretations; native Skia float32 boolean geometry changes curves by numerical rounding. No photographic segmentation or alpha-lossless claim.',
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
    gate = root_gate()
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
    print(json.dumps({'action': 'wrote-one-edited-asset' if args.write else 'verified-existing',
                      'writes': len(outputs) if args.write else 0, 'root_gate': gate,
                      'headline': ref(OUT / 'headline.svg'), 'preview': ref(PRIVATE / 'preview.png'),
                      'alpha_bbox': build['actual_alpha_bbox_exclusive'],
                      'glyphs': build['glyphs'], 'aesthetic_pass_claimed': False}, ensure_ascii=True))


if __name__ == '__main__':
    main()
