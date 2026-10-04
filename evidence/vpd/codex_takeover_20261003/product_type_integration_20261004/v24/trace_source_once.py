"""V24 production trace, once, from Root's single transparent generated PNG.

This preserves the original PNG reference and the literal VTracer result.  It
does not choose or edit glyphs, render a candidate, update state, or invoke an
image generator.  Exclusive writes keep any previous trace intact.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.metadata
import io
import json
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

sys.dont_write_bytecode = True
import PIL
from PIL import Image

ROOT = Path(__file__).resolve().parents[5]
SERIES = ROOT / 'evidence/vpd/codex_takeover_20261003/product_type_integration_20261004'
OUT = Path(__file__).resolve().parent
PRIVATE = ROOT / '.liu-visual-private/correct_source_typography/v24'
DEP = ROOT / '.liu-visual-private/dependencies/vtracer_0_6_15_cp312'
NS = '{http://www.w3.org/2000/svg}'
SOURCE = {'path': '.liu-visual-private/source_recovery_20261003/photography-local-reconstruction-final.png',
          'sha256': '7fd7777fed21100cb6b47bc305701476054263565e73246ac469d065aa080618'}
BRAND = {'path': 'evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v21/brand.svg',
         'sha256': 'dd8e9e899393dc36eb3f5b1652bdbb740787d41a108ea6aa1eae05cb1368b1ff'}
WHEEL_SHA = 'b0f08b66734e41872d4ac343ed6d08870b3235346def3e112e10b3b2443e619e'
TRACE_PARAMETERS = {'img_format': 'png', 'colormode': 'binary', 'mode': 'spline',
                    'filter_speckle': 0, 'corner_threshold': 60,
                    'length_threshold': 4.0, 'max_iterations': 10,
                    'splice_threshold': 45, 'path_precision': 3}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def jb(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def ref(path, raw=None):
    path = Path(path).resolve()
    assert path.is_relative_to(ROOT.resolve()), 'SOURCE_REFERENCE_OUTSIDE_REPOSITORY'
    raw = path.read_bytes() if raw is None else raw
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': sha(raw), 'bytes': len(raw)}


def checked(reference):
    path = (ROOT / reference['path']).resolve()
    assert path.is_relative_to(ROOT.resolve()), 'SOURCE_REFERENCE_OUTSIDE_REPOSITORY'
    raw = path.read_bytes()
    assert sha(raw) == reference['sha256'], 'SOURCE_SHA_MISMATCH:' + reference['path']
    return raw


def root_gate():
    raw = (ROOT / 'continuity/vpd/CURRENT_TASK_LOCK.json').read_bytes()
    lock = json.loads(raw)
    unit = lock['codex_takeover']['worker_continuation']
    last = unit['versions'][-1]
    assert (lock['revision'] >= 322
            and unit['unit_id'] == 'CHAZUO_APPROVED_SOURCE_TYPOGRAPHY_20261003_R1'
            and unit['phase'] == 'REVISION_REQUIRED'
            and last['number'] == 23 and last['verdict'] == 'AI_FAIL'), 'ROOT_V24_GO_GATE_NOT_SATISFIED'
    return {'revision': lock['revision'], 'phase': unit['phase'],
            'last_version': last['number'], 'verdict': last['verdict'],
            'lock_sha256': sha(raw)}


def source_commands(trace):
    # FontTools is used only to inspect SVG commands, never to supply a font.
    sys.path.append('C:/Users/Administrator/AppData/Local/hermes/hermes-agent/venv/Lib/site-packages')
    import fontTools
    from fontTools.pens.boundsPen import BoundsPen
    from fontTools.pens.recordingPen import RecordingPen
    from fontTools.svgLib.path import parse_path
    tree = ET.fromstring(trace)
    rows = []
    for index, node in enumerate(tree):
        assert node.tag == NS + 'path', 'NON_PATH_TRACE_ELEMENT'
        d = node.get('d', '')
        transform = node.get('transform', '')
        match = re.fullmatch(r'translate\(([-.\d]+),([-.\d]+)\)', transform)
        assert match, 'UNEXPECTED_TRACE_TRANSLATION'
        dx, dy = map(float, match.groups())
        recording = RecordingPen()
        bounds = BoundsPen(None)
        if d.strip():
            parse_path(d, recording)
            parse_path(d, bounds)
        contours, current = [], []
        for command, points in recording.value:
            if command == 'moveTo':
                assert not current, 'PREVIOUS_TRACE_CONTOUR_OPEN'
            assert command in {'moveTo', 'lineTo', 'curveTo', 'qCurveTo', 'closePath'}, 'TRACE_COMMAND_UNSUPPORTED'
            translated = [[float(x) + dx, float(y) + dy] for x, y in points]
            current.append({'op': command, 'points': translated})
            if command == 'closePath':
                contours.append(current)
                current = []
        assert not current, 'TRACE_CONTOUR_OPEN'
        b = bounds.bounds
        rows.append({'path_index': index, 'd_sha256': sha(d.encode('utf-8')),
                     'literal_transform': transform,
                     'empty_d': not d.strip(),
                     'bounds_png_coordinates': None if b is None else [b[0] + dx, b[1] + dy, b[2] + dx, b[3] + dy],
                     'closed_contours': contours})
    return {'schema': 'vpd-v24-source-trace-command-inspection/v1',
            'coordinate_space': 'original generated PNG; literal per-path translate already applied',
            'fonttools_version': fontTools.__version__, 'font_files_loaded': 0,
            'path_count': len(rows), 'paths': rows}


def production_trace(source_ref, generation_ref):
    source_raw = checked(source_ref)
    checked(generation_ref)
    checked(SOURCE)
    checked(BRAND)
    image = Image.open(io.BytesIO(source_raw))
    assert image.format == 'PNG' and image.mode == 'RGBA', 'ROOT_TRANSPARENT_RGBA_PNG_REQUIRED'
    alpha = image.getchannel('A')
    extrema = alpha.getextrema()
    assert extrema[0] == 0 and extrema[1] >= 128, 'SOURCE_TRANSPARENCY_REQUIRED'
    assert PIL.__version__ == '12.3.0' and sys.version_info[:3] == (3, 12, 14), 'RUNTIME_CHANGED'
    wheel_path = DEP / 'vtracer-0.6.15-cp312-cp312-win_amd64.whl'
    wheel_raw = wheel_path.read_bytes()
    assert sha(wheel_raw) == WHEEL_SHA, 'FIXED_VTRACER_WHEEL_CHANGED'
    sys.path.insert(0, str(DEP / 'site-packages'))
    import vtracer
    assert importlib.metadata.version('vtracer') == '0.6.15', 'FIXED_VTRACER_VERSION_CHANGED'
    wrapper = Path(vtracer.__file__).read_bytes()
    binary_path = Path(vtracer.__file__).parent / 'vtracer.cp312-win_amd64.pyd'
    implementation = binary_path.read_bytes()
    with zipfile.ZipFile(io.BytesIO(wheel_raw)) as wheel:
        assert wrapper == wheel.read('vtracer/__init__.py'), 'VTRACER_WRAPPER_CHANGED'
        assert implementation == wheel.read('vtracer/vtracer.cp312-win_amd64.pyd'), 'VTRACER_BINARY_CHANGED'
    binary = alpha.point(lambda value: 0 if value >= 128 else 255).convert('RGB')
    buffer = io.BytesIO()
    binary.save(buffer, format='PNG')
    binary_raw = buffer.getvalue()
    trace = vtracer.convert_raw_image_to_svg(binary_raw, **TRACE_PARAMETERS).encode('utf-8')
    commands = source_commands(trace)
    hist = alpha.histogram()
    metadata = {'schema': 'vpd-v24-one-production-trace/v1', 'formal_version': 24,
                'copy': '一杯茶，慢下来', 'generated_png': source_ref,
                'generation_evidence': generation_ref,
                'original_png_preserved_by_this_script': True,
                'production_trace_calls_by_this_script': 1,
                'new_imagegen_calls_by_this_script': 0,
                'trace_parameters': TRACE_PARAMETERS,
                'alpha_threshold_inclusive': 128,
                'alpha_facts': {'size': list(image.size), 'mode': image.mode,
                                'extrema': list(extrema), 'alpha0_pixels': hist[0],
                                'alpha255_pixels': hist[255], 'alpha128_pixels': sum(hist[128:]),
                                'alpha128_bbox_exclusive': list(alpha.point(lambda value: 255 if value >= 128 else 0).getbbox())},
                'path_count': commands['path_count'],
                'empty_path_indices': [row['path_index'] for row in commands['paths'] if row['empty_d']],
                'software': {'Python': sys.version, 'Pillow': PIL.__version__,
                             'VTracer': importlib.metadata.version('vtracer'),
                             'FontTools': commands['fonttools_version']},
                'dependencies': {'wheel': ref(wheel_path, wheel_raw),
                                 'wrapper': ref(Path(vtracer.__file__), wrapper),
                                 'binary': ref(binary_path, implementation)},
                'builder': ref(Path(__file__)),
                'outputs': {'trace': ref(OUT / 'upstream-alpha128-trace.svg', trace),
                            'commands': ref(OUT / 'TRACE_COMMANDS.json', jb(commands)),
                            'alpha128': ref(PRIVATE / 'headline-alpha128.png', binary_raw)},
                'source_photo': SOURCE, 'frozen_brand': BRAND,
                'glyph_edits_performed': False, 'aesthetic_pass_claimed': False,
                'business_state_writes': 0, 'Figma_Drive_Git_writes': 0,
                'approximation_boundary': 'alpha>=128 threshold and fixed spline tracing approximate the generated alpha edge; the raw generated PNG is a distinct preserved source.'}
    return {OUT / 'upstream-alpha128-trace.svg': trace,
            OUT / 'TRACE_COMMANDS.json': jb(commands),
            OUT / 'SOURCE_TRACE.json': jb(metadata),
            PRIVATE / 'headline-alpha128.png': binary_raw}, metadata


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-reference', required=True, help='Root-frozen JSON reference object file')
    parser.add_argument('--generation-evidence', required=True, help='Root actual image-generation evidence path')
    parser.add_argument('--write', action='store_true', required=True)
    args = parser.parse_args()
    targets = [OUT / name for name in ('upstream-alpha128-trace.svg', 'TRACE_COMMANDS.json', 'SOURCE_TRACE.json')]
    targets.append(PRIVATE / 'headline-alpha128.png')
    assert not any(path.exists() for path in targets), 'V24_PRODUCTION_TRACE_ALREADY_EXISTS'
    gate = root_gate()
    source_document = json.loads(Path(args.source_reference).read_bytes())
    source_ref = source_document.get('preserved_source_copy', source_document)
    generation_ref = ref(Path(args.generation_evidence))
    source_path = (ROOT / source_ref['path']).resolve()
    assert source_path == (PRIVATE / 'headline-generated-01.png').resolve(), 'ROOT_CANONICAL_GENERATED_PATH_REQUIRED'
    outputs, metadata = production_trace(source_ref, generation_ref)
    assert set(outputs) == set(targets)
    assert not any(path.exists() for path in targets), 'OUTPUT_APPEARED_DURING_TRACE'
    OUT.mkdir(parents=True, exist_ok=True)
    PRIVATE.mkdir(parents=True, exist_ok=True)
    for path, raw in outputs.items():
        with path.open('xb') as handle:
            handle.write(raw)
    for path, raw in outputs.items():
        assert path.read_bytes() == raw, 'TRACE_POST_WRITE_READBACK_MISMATCH'
    print(json.dumps({'action': 'one-production-trace-preserved', 'root_gate': gate,
                      'writes': len(outputs), 'trace': metadata['outputs']['trace'],
                      'path_count': metadata['path_count'], 'alpha_facts': metadata['alpha_facts']}, ensure_ascii=True))


if __name__ == '__main__':
    main()
