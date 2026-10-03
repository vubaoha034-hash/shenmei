"""Synthetic PNGs test photograph preservation; no fixture is a design output."""
import json
import zlib

import pytest

from visual_memory.vpd_task_lock import TaskLockError, digest
from visual_memory.vpd_locked_mainline_state import (
    TAKEOVER_TASK, OVERLAY_ENVELOPES, _png_rgb_rows, _protected_pixel_comparison,
    _validate_takeover_technical,
)


def chunk(tag, data):
    return len(data).to_bytes(4, 'big') + tag + data + zlib.crc32(tag + data).to_bytes(4, 'big')


def png(root, name, changed=None, filters=False, rgba=False):
    channels = 4 if rgba else 3
    unit = b'\x50\xa0\x30\xff' if rgba else b'\x50\xa0\x30'
    plain, rows, previous = unit * 1536, bytearray(), bytearray(1536 * channels)
    for y in range(1024):
        row = bytearray(plain)
        if changed and y == changed[1]:
            row[changed[0] * channels] = 81
        kind = y % 5 if filters else 0
        encoded = bytearray(row)
        # Standard PNG filter encoding, independent of the verifier's reconstruction.
        for x in range(len(row)) if kind else []:
            a = row[x - channels] if x >= channels else 0
            b = previous[x]
            c = previous[x - channels] if x >= channels else 0
            if kind == 1:
                predict = a
            elif kind == 2:
                predict = b
            elif kind == 3:
                predict = (a + b) // 2
            else:
                distances = [abs(b - c), abs(a - c), abs(a + b - 2 * c)]
                predict = [a, b, c][distances.index(min(distances))]
            encoded[x] = (row[x] - predict) % 256
        rows.extend(bytes([kind]) + encoded)
        previous = row
    header = (1536).to_bytes(4, 'big') + (1024).to_bytes(4, 'big') + bytes([8, 6 if rgba else 2, 0, 0, 0])
    raw = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', header) + chunk(b'IDAT', zlib.compress(rows)) + chunk(b'IEND', b'')
    p = root / name
    p.write_bytes(raw)
    return {'path': name, 'sha256': digest(p)}


def save(root, name, data):
    p = root / name
    p.write_text(json.dumps(data, ensure_ascii=False) + '\n', encoding='utf-8')
    return {'path': name, 'sha256': digest(p)}


def test_all_png_filters_and_rgba_decode_to_the_known_pixels(tmp_path):
    ref = png(tmp_path, 'SYNTHETIC_FILTER_RGBA.png', filters=True, rgba=True)
    rows = list(_png_rgb_rows(tmp_path, ref))
    assert len(rows) == 1024
    assert all(row == b'\x50\xa0\x30' * 1536 for row in rows)


def test_design_occlusion_is_allowed_and_protected_pixel_change_is_measured(tmp_path):
    source = png(tmp_path, 'SYNTHETIC_SOURCE.png')
    design = png(tmp_path, 'SYNTHETIC_DESIGN.png', changed=(100, 80))
    assert _protected_pixel_comparison(tmp_path, source, design) == (1356936, 0)
    outside = png(tmp_path, 'SYNTHETIC_PHOTO_DRIFT.png', changed=(300, 500))
    assert _protected_pixel_comparison(tmp_path, source, outside) == (1356936, 1)


@pytest.mark.parametrize('changed,expected', [((100, 80), None),
                                           ((300, 500), 'PROTECTED_PHOTO_PIXELS_CHANGED')])
def test_zero_change_report_is_checked_against_actual_pixels(tmp_path, changed, expected):
    source = png(tmp_path, 'SYNTHETIC_SOURCE.png')
    exported = png(tmp_path, 'SYNTHETIC_EXPORT.png', changed=changed)
    frame = {'file_key': 'SYNTHETIC_NOT_RUNTIME', 'node_id': '251:3',
             'url': 'https://www.figma.com/design/SYNTHETIC_NOT_RUNTIME/example?node-id=251-3'}
    readback = save(tmp_path, 'SYNTHETIC_READBACK.json', {
        'file_key': frame['file_key'], 'node_id': frame['node_id'],
        'source_layer': {'source_sha256': source['sha256'], 'x': 0, 'y': 0,
                         'width': 1536, 'height': 1024, 'rotation': 0, 'locked': True}})
    trace = save(tmp_path, 'SYNTHETIC_TRACE.json', {'source': 'SYNTHETIC_NOT_RUNTIME_EVIDENCE'})
    data = {'task_id': TAKEOVER_TASK, 'version': 1, 'source_sha256': source['sha256'],
            'dimensions': [1536, 1024], 'overlay_envelopes': OVERLAY_ENVELOPES,
            'source_layer_unchanged': True, 'protected_pixels_changed': 0,
            'protected_pixels_compared': 1356936, 'source': source, 'export': exported,
            'figma_readback': readback, 'trace': trace, 'figma': frame}
    ref = save(tmp_path, 'SYNTHETIC_FALSE_ZERO_CHANGE_REPORT.json', data)
    protection = {'source': {'sha256': source['sha256'], 'dimensions': [1536, 1024]}}
    if expected:
        with pytest.raises(TaskLockError, match=expected):
            _validate_takeover_technical(tmp_path, ref, 1, protection)
    else:
        assert _validate_takeover_technical(tmp_path, ref, 1, protection) == data
