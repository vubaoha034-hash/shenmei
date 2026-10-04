"""V25: one source-bound refinement of V24's light upright headline.

The original generation and the 17-path/21-contour production trace remain at
their real V24 paths. This file authors local contour geometry; it does not
generate images, produce a new trace, use font outlines, or alter shared state.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys

sys.dont_write_bytecode = True
sys.path.append('C:/Users/Administrator/AppData/Local/hermes/hermes-agent/venv/Lib/site-packages')
import fontTools
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.reverseContourPen import ReverseContourPen
from fontTools.svgLib.path import parse_path
sys.path.remove('C:/Users/Administrator/AppData/Local/hermes/hermes-agent/venv/Lib/site-packages')

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
BASE = ROOT / 'evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v24'
sys.path.insert(0, str(ROOT))
from visual_memory import vpd_registered_type_composite as g

COPY = '一杯茶，慢下来'
ORIGINS = {'一': (625, 476), '杯': (744, 431), '茶': (903, 419),
           '，': (1068, 510), '慢': (865, 539), '下': (1011, 554),
           '来': (1116, 540)}
SOURCES = {'一': [4], '杯': [0, 2, 6], '茶': [1, 3, 5, 8, 9],
           '，': [7], '慢': [11, 12, 15, 16], '下': [13], '来': [10, 14]}

# One layout, explicit closed silhouettes. Local nodes and terminals are
# actually re-authored; a group scale/translation is not called glyph design.
# Counters retain their real source identities and opposite winding.
DRAWINGS = {
 (4, 0): [
  'M625 480 C650 478 687 475 708 477 L713 481 C687 482 652 485 628 486 Z'],
 (0, 0): [
  'M783 431 L791 433 C790 463 791 494 792 519 C794 528 802 538 809 543 L807 547 C797 540 788 529 784 519 C782 490 783 458 783 431 Z',
  'M762 475 C775 473 798 472 815 472 L814 477 C794 477 775 480 764 480 Z',
  'M782 477 C776 493 765 509 744 523 L747 526 C767 512 779 496 789 483 Z',
  'M790 486 C798 490 804 497 809 502 L806 506 C798 501 793 496 788 492 Z'],
 (2, 0): [
  'M823 448 C842 446 863 440 882 443 L885 447 C864 447 845 452 824 452 Z',
  'M852 447 L860 449 C851 467 837 486 817 499 L814 496 C835 479 847 460 852 447 Z',
  'M851 467 L860 468 C860 490 860 515 858 534 L853 539 C851 517 852 490 851 467 Z'],
 (6, 0): [
  'M865 478 C874 487 880 501 886 513 L883 516 C873 506 868 493 862 483 Z'],
 (1, 0): [
  'M916 433 C950 432 992 428 1036 430 L1039 434 C995 434 949 436 918 438 Z',
  'M951 419 L958 420 L956 450 L951 446 Z',
  'M1001 419 L1008 421 C1005 432 1000 443 997 449 L992 448 C996 437 999 428 1001 419 Z'],
 (3, 0): [
  'M977 450 L983 454 C965 466 934 477 905 483 L903 480 C935 470 961 459 977 450 Z',
  'M978 451 C1001 462 1029 472 1052 476 L1053 480 C1024 478 997 468 976 456 Z'],
 (5, 0): [
  'M930 483 C954 481 996 477 1027 480 L1029 484 C995 484 954 488 932 488 Z',
  'M978 469 L986 471 C986 485 986 503 983 509 L979 512 C978 498 979 483 978 469 Z'],
 (8, 0): [
  'M989 488 C1005 497 1029 516 1050 506 L1053 510 C1032 523 1006 505 986 493 Z'],
 (9, 0): [
  'M970 490 C961 500 949 508 938 514 L934 511 C946 502 958 495 970 486 Z'],
 (7, 0): [
  'M1075 510 C1084 510 1088 519 1084 524 C1080 528 1074 533 1070 536 L1068 533 C1072 524 1074 517 1075 510 Z'],
 (11, 0): [
  'M918 542 C938 540 966 538 988 539 L987 562 C965 564 941 566 920 565 Z'],
 (11, 1): [
  'M925 546 C943 544 967 543 982 544 L982 557 C962 559 944 561 926 561 L926 555 L975 552 L975 549 L925 552 Z'],
 (12, 0): [
  'M886 542 L894 544 C894 560 894 577 889 590 C885 602 880 611 868 619 L865 616 C873 604 880 594 883 582 C887 567 888 552 886 542 Z',
  'M899 553 C904 556 910 561 914 565 L912 569 C905 565 900 561 896 557 Z',
  'M913 570 C936 567 967 566 990 566 L989 585 C966 588 941 592 915 594 Z'],
 (12, 1): [
  'M971 572 L984 570 L984 579 L971 582 Z'],
 (12, 2): [
  'M947 574 L964 572 L963 583 L948 585 Z'],
 (12, 3): [
  'M920 576 L939 574 L939 586 L920 589 Z'],
 (15, 0): [
  'M884 562 L889 565 C887 570 884 576 883 580 L880 578 C881 572 883 567 884 562 Z'],
 (16, 0): [
  'M924 597 C937 596 954 593 968 592 L972 596 C958 602 944 611 932 617 L929 614 C943 605 955 598 962 596 C949 597 937 600 926 602 Z',
  'M935 596 C943 598 949 603 957 604 C962 605 966 599 970 595 L973 598 C968 606 963 610 957 608 C949 606 942 602 932 599 Z'],
 (13, 0): [
  'M1011 557 C1036 556 1068 553 1092 554 L1095 558 C1068 559 1036 562 1013 562 Z',
  'M1047 558 L1056 558 C1055 585 1055 609 1053 624 L1049 627 C1047 608 1048 585 1047 558 Z',
  'M1059 579 C1069 584 1077 594 1084 603 L1080 606 C1070 597 1064 587 1057 583 Z'],
 (10, 0): [
  'M1129 553 C1151 551 1200 546 1223 548 L1225 552 C1202 555 1152 557 1131 558 Z',
  'M1169 540 L1177 541 C1177 569 1178 600 1175 620 L1172 625 C1168 603 1170 568 1169 540 Z',
  'M1122 585 C1155 582 1197 580 1231 581 L1235 585 C1197 587 1156 589 1124 590 Z',
  'M1210 564 L1216 566 C1210 574 1203 581 1196 586 L1193 583 C1200 576 1205 570 1210 564 Z',
  'M1171 589 L1178 594 C1163 607 1141 618 1118 624 L1116 621 C1137 610 1155 600 1171 589 Z',
  'M1174 590 C1191 603 1212 614 1235 620 L1233 624 C1207 618 1187 607 1169 596 Z'],
 (14, 0): [
  'M1135 566 C1143 568 1149 576 1153 580 L1150 584 C1143 579 1138 572 1132 569 Z'],
}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def jb(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def commands_sha(contour):
    return sha(json.dumps(contour, ensure_ascii=False, sort_keys=True,
                          separators=(',', ':'), allow_nan=False).encode('utf-8'))


def ref(path):
    path = Path(path).resolve()
    assert path.is_relative_to(ROOT.resolve())
    raw = path.read_bytes()
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': sha(raw), 'bytes': len(raw)}


def root_write_gate():
    raw = (ROOT / 'continuity/vpd/CURRENT_TASK_LOCK.json').read_bytes()
    lock = json.loads(raw)
    unit = lock['codex_takeover']['worker_continuation']
    last = unit['versions'][-1]
    assert (lock['revision'] == 324 and unit['phase'] == 'REVISION_REQUIRED'
            and unit['unit_id'] == 'CHAZUO_APPROVED_SOURCE_TYPOGRAPHY_20261003_R1'
            and last['number'] == 24 and last['verdict'] == 'AI_FAIL'), 'ROOT_V25_GO_GATE_NOT_SATISFIED'
    return {'revision': lock['revision'], 'phase': unit['phase'], 'last_version': 24,
            'last_verdict': 'AI_FAIL', 'lock_sha256': sha(raw)}


def command_rows(d, origin, negative):
    pen = RecordingPen()
    parse_path(d, pen)
    values = pen.value
    endpoints = [pts[-1] for op, pts in values if pts]
    area = sum(endpoints[i][0] * endpoints[(i + 1) % len(endpoints)][1]
               - endpoints[(i + 1) % len(endpoints)][0] * endpoints[i][1]
               for i in range(len(endpoints))) / 2
    if (area < 0) != negative:
        reverse = RecordingPen()
        pen.replay(ReverseContourPen(reverse))
        values = reverse.value
    result = [{'op': op, 'points': [[float(x) - origin[0], float(y) - origin[1]]
                                   for x, y in points]} for op, points in values]
    assert result[0]['op'] == 'moveTo' and result[-1]['op'] == 'closePath'
    assert all(row['op'] in {'moveTo', 'lineTo', 'curveTo', 'closePath'} for row in result)
    return result


def build_program():
    assert fontTools.__version__ == '4.63.0', 'COMMAND_PARSER_VERSION_CHANGED'
    kernel = g.edited_kernel(ROOT)
    original = json.loads(kernel['checked'](ROOT, kernel['INPUTS']['source_commands']))
    kernel['checked'](ROOT, kernel['INPUTS']['trace_svg'])
    kernel['checked'](ROOT, kernel['INPUTS']['art_direction'])
    baseline = json.loads(kernel['checked'](ROOT, kernel['SEALED_EDIT']))
    baseline_edits = {(edit['path_index'], edit['contour_index']): edit['after_contours']
                      for glyph in baseline['glyphs'] for edit in glyph['edits']}
    assert original['path_count'] == 17
    glyphs, accounted, details = [], [], []
    for char in COPY:
        sources, edits = [], []
        for pi in SOURCES[char]:
            contours = original['paths'][pi]['closed_contours']
            sources.append({'path_index': pi, 'contour_indices': list(range(len(contours)))})
            for ci, before in enumerate(contours):
                endpoints = [row['points'][-1] for row in before if row['points']]
                area = sum(endpoints[i][0] * endpoints[(i + 1) % len(endpoints)][1]
                           - endpoints[(i + 1) % len(endpoints)][0] * endpoints[i][1]
                           for i in range(len(endpoints))) / 2
                negative = area < 0
                after = [command_rows(d, ORIGINS[char], negative) for d in DRAWINGS[(pi, ci)]]
                reason = ('Refine the V24 source-bound counter: preserve its original negative '
                          'identity while making inner whitespace follow the slanted outer contour.') if negative else (
                          'Refine the V24 light skeleton with explicitly authored shorter terminals, '
                          'differentiated stroke weight and controlled oblique contour rhythm. '
                          'The local curves are changed before positive per-character placement.')
                edits.append({'op': 'replace_contour', 'path_index': pi, 'contour_index': ci,
                              'before_sha256': commands_sha(before),
                              'after_contours': after, 'reason': reason})
                accounted.append((pi, ci))
                details.append({'char': char, 'path_index': pi, 'contour_index': ci,
                                'source_negative_counter': negative,
                                'source_before_sha256': commands_sha(before),
                                'original_commands': len(before), 'new_contours': len(after),
                                'new_commands': [len(c) for c in after],
                                'local_geometry_changed_from_v24': after != baseline_edits[(pi, ci)]})
        glyphs.append({'char': char, 'source': sources, 'edits': edits,
                       'placement': {'scale': 1.0, 'tx': ORIGINS[char][0], 'ty': ORIGINS[char][1]}})
    expected = [(row['path_index'], ci) for row in original['paths']
                for ci in range(len(row['closed_contours']))]
    assert sorted(accounted) == sorted(expected) and len(accounted) == len(set(accounted)) == 21
    assert set(DRAWINGS) == set(expected)
    program = {'schema': 'vpd-source-bound-glyph-edits/v1', 'formal_version': 25,
               'copy': COPY, 'source_trace': kernel['INPUTS']['trace_svg'], 'glyphs': glyphs,
               'negative_space': {'art_direction': kernel['INPUTS']['art_direction'],
                                  'operation': 'difference-union', 'fix_winding': True,
                                  'keep_starting_points': True, 'clockwise': False}}
    notes = {'schema': 'vpd-v25-real-local-contour-refinement/v1', 'formal_version': 25,
             'copy': COPY, 'direction_count': 1,
             'source_generation': kernel['INPUTS']['generated_png'],
             'source_generation_evidence': kernel['INPUTS']['generation_evidence'],
             'production_trace': kernel['INPUTS']['trace_svg'],
             'production_trace_commands': kernel['INPUTS']['source_commands'],
             'source_trace_provenance': kernel['INPUTS']['provenance'],
             'baseline_edit_manifest': kernel['SEALED_EDIT'], 'maker_source': ref(Path(__file__)),
             'source_roles': SOURCES, 'original_path_count': 17, 'original_contour_count': 21,
             'original_contours_accounted_once': True, 'dropped_source_contours': [],
             'replacement_details': details,
             'design_basis': 'One continuous upper phrase over the cup upper-right field; a clear second line above the tea platter. Local shortened terminals and open whitespace allow the original cup/leaf/platter contours to remain visible.',
             'key_changes': {'一': 'Raised to the reading height of the cup cross stroke.',
                             '杯': 'Both long vertical endings and the left fall actually shortened; the wood terminal keeps a small rightward curve.',
                             '茶': 'Lower stem and diagonal endpoints gathered upward, leaving visible air before the lower row.',
                             '慢': 'Upper and lower counters follow slightly rising edges; lower stems and crossed terminal stop before the leaf envelope.',
                             '下': 'Short vertical finishes above the tea heap rather than running into the platter.',
                             '来': 'Lower stem and diagonals shortened into a restrained open foot line.',
                             '，': 'One visible connected slanted comma after the upper phrase.'},
             'negative_space': 'Original V24 CUP_AIR/LEAF_AIR literals, applied only to letter outlines by the unchanged fixed kernel.',
             'new_imagegen_calls': 0, 'new_production_traces': 0,
             'font_files_loaded': 0, 'reference_outlines_copied': 0,
             'parser': {'library': 'FontTools', 'version': fontTools.__version__, 'purpose': 'Authored SVG command normalization and winding only'},
             'business_state_writes': 0, 'Figma_Drive_Git_writes': 0,
             'aesthetic_pass_claimed': False, 'human_acceptance_claimed': False}
    return program, notes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--write', action='store_true')
    modes.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    outputs = [OUT / 'V25_GLYPH_EDIT_MANIFEST.json', OUT / 'SOURCE_REAUTHORING_NOTES.json']
    gate = root_write_gate() if args.write else None
    if args.write:
        assert not any(path.exists() for path in outputs), 'AUTHORED_PROGRAM_ALREADY_EXISTS'
    program, notes = build_program()
    values = [program, notes]
    if args.write:
        assert not any(path.exists() for path in outputs), 'PROGRAM_APPEARED_DURING_BUILD'
        for path, value in zip(outputs, values):
            with path.open('xb') as handle:
                handle.write(jb(value))
    for path, value in zip(outputs, values):
        assert path.read_bytes() == jb(value), 'AUTHORED_PROGRAM_EXACT_READBACK_MISMATCH'
    print(json.dumps({'action': 'authored-one-program' if args.write else 'verified-existing',
                      'formal_version': 25, 'writes': len(outputs) if args.write else 0,
                      'root_write_gate': gate, 'manifest': ref(outputs[0]), 'notes': ref(outputs[1]),
                      'source_contours': 21,
                      'authored_closed_contours': sum(row['new_contours'] for row in notes['replacement_details']),
                      'aesthetic_pass_claimed': False}, ensure_ascii=True))


if __name__ == '__main__':
    main()
