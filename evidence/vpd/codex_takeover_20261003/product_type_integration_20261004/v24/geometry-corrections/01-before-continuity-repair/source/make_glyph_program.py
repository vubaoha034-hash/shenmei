"""Author V24's one source-bound manual outline-edit program.

The generated trace supplies character/stroke identities. Its heavy outer
contours are genuinely redrawn as explicit, closed, sparse Bezier contours.
This is neither an unchanged-trace claim nor a font-outline substitution.
Every original contour, including counters, is explicitly accounted for.
The separate fixed guard kernel interprets the resulting JSON independently.
"""
from pathlib import Path
import hashlib
import json
import sys

sys.dont_write_bytecode = True
sys.path.append('C:/Users/Administrator/AppData/Local/hermes/hermes-agent/venv/Lib/site-packages')
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.reverseContourPen import ReverseContourPen
from fontTools.svgLib.path import parse_path

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
COPY = '一杯茶，慢下来'
ORIGINS = {'一': (612, 526), '杯': (712, 431), '茶': (858, 419),
           '，': (1023, 541), '慢': (851, 539), '下': (1011, 572),
           '来': (1116, 554)}
SOURCES = {'一': [4], '杯': [0, 2, 6], '茶': [1, 3, 5, 8, 9],
           '，': [7], '慢': [11, 12, 15, 16], '下': [13], '来': [10, 14]}

# Canvas-coordinate, authored closed outlines.  These express the one approved
# art direction. The code converts them to each glyph's local coordinates;
# the program's positive uniform placement puts them back on the canvas.
# Keys bind every replacement to a real source path/closed-contour identity.
# Source negative contours remain explicit negative contours after rebuilding.
DRAWINGS = {
 (4, 0): [
  'M612 531 C638 529 672 525 695 528 L700 531 C679 532 638 535 615 538 Z'],
 (0, 0): [
  'M738 432 L746 434 C745 480 746 526 747 563 C748 576 753 590 763 602 L759 606 C749 598 742 581 739 565 C738 523 738 478 738 432 Z',
  'M717 475 C731 473 752 472 770 472 L769 477 C750 477 731 480 719 480 Z',
  'M737 477 C732 497 721 519 699 539 L702 542 C721 525 735 504 743 483 Z',
  'M746 486 C754 489 760 496 765 502 L762 505 C754 501 749 495 744 490 Z'],
 (2, 0): [
  'M778 448 C797 446 818 440 837 443 L839 447 C817 447 798 452 779 452 Z',
  'M807 447 L815 449 C807 470 793 490 771 503 L768 501 C790 481 801 462 807 447 Z',
  'M806 469 L815 468 C815 508 815 553 813 596 L808 601 C806 555 807 510 806 469 Z'],
 (6, 0): [
  'M820 478 C829 488 835 504 841 520 L838 524 C826 511 820 496 816 483 Z'],
 (1, 0): [
  'M871 433 C905 432 947 428 991 430 L994 434 C950 434 904 436 873 438 Z',
  'M906 419 L913 420 L911 453 L906 449 Z',
  'M956 419 L963 421 C960 432 955 445 952 451 L947 450 C951 438 954 428 956 419 Z'],
 (3, 0): [
  'M932 450 L938 454 C920 466 889 477 860 483 L858 480 C890 470 916 459 932 450 Z',
  'M933 451 C956 462 984 472 1007 476 L1008 480 C979 478 952 468 931 456 Z'],
 (5, 0): [
  'M885 488 C909 486 951 481 982 484 L984 488 C950 488 909 492 887 493 Z',
  'M933 472 L941 473 C941 490 941 511 938 523 L934 525 C933 507 934 489 933 472 Z'],
 (8, 0): [
  'M944 493 C961 506 983 524 1005 516 L1008 519 C987 530 961 514 941 497 Z'],
 (9, 0): [
  'M925 495 C916 506 903 517 891 525 L888 523 C901 512 914 501 925 491 Z'],
 (7, 0): [
  'M1028 541 C1037 541 1038 554 1035 557 C1031 563 1026 567 1023 569 L1022 567 C1026 559 1027 552 1026 547 Z'],
 (11, 0): ['M888 539 L958 539 L957 563 L890 565 Z'],
 (11, 1): ['M895 544 L953 544 L953 558 L895 558 L895 553 L946 553 L946 550 L895 550 Z'],
 (12, 0): [
  'M856 541 L864 543 C864 574 864 610 862 643 L858 646 C856 611 858 574 856 541 Z',
  'M869 553 C874 556 880 561 884 565 L882 569 C875 565 870 561 866 557 Z',
  'M883 568 L960 568 L959 591 L885 593 Z'],
 (12, 1): ['M941 573 L954 573 L954 586 L941 587 Z'],
 (12, 2): ['M917 574 L934 574 L934 586 L917 587 Z'],
 (12, 3): ['M890 574 L910 574 L910 587 L891 588 Z'],
 (15, 0): [
  'M854 562 L859 565 C857 570 854 576 853 580 L850 578 C851 572 853 567 854 562 Z'],
 (16, 0): [
  'M897 595 C913 593 935 591 950 592 L952 596 C941 611 926 626 909 638 L905 636 C920 621 936 607 943 598 C930 598 913 600 899 600 Z',
  'M908 598 C922 600 938 610 951 608 L950 612 C934 615 920 607 905 602 Z'],
 (13, 0): [
  'M1011 575 C1036 574 1068 571 1092 572 L1095 576 C1068 577 1036 580 1013 580 Z',
  'M1047 576 L1056 576 C1055 638 1055 661 1053 679 L1049 679 C1047 649 1048 619 1047 576 Z',
  'M1059 601 C1069 606 1077 616 1084 625 L1080 628 C1070 619 1064 609 1057 605 Z'],
 (10, 0): [
  'M1129 568 C1151 566 1200 561 1223 563 L1225 567 C1202 570 1152 572 1131 573 Z',
  'M1169 554 L1177 555 C1177 593 1178 643 1175 675 L1172 681 C1168 644 1170 591 1169 554 Z',
  'M1122 607 C1155 604 1197 602 1231 603 L1235 607 C1197 609 1156 611 1124 612 Z',
  'M1210 582 L1216 584 C1210 592 1203 599 1196 604 L1193 601 C1200 594 1205 588 1210 582 Z',
  'M1171 610 L1178 615 C1163 638 1141 661 1118 674 L1116 671 C1137 651 1155 630 1171 610 Z',
  'M1174 611 C1191 633 1212 653 1235 668 L1233 672 C1207 659 1187 640 1169 618 Z'],
 (14, 0): [
  'M1135 584 C1143 586 1149 594 1153 598 L1150 602 C1143 597 1138 590 1132 587 Z'],
}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def jb(obj):
    return (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def commands_sha(contour):
    raw = json.dumps(contour, ensure_ascii=False, sort_keys=True,
                     separators=(',', ':'), allow_nan=False).encode('utf-8')
    return sha(raw)


def ref(path):
    path = Path(path)
    raw = path.read_bytes()
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': sha(raw), 'bytes': len(raw)}


def command_rows(d, origin, negative):
    pen = RecordingPen()
    parse_path(d, pen)
    values = pen.value
    endpoints = [pts[-1] for op, pts in values if pts]
    area = sum(endpoints[i][0] * endpoints[(i + 1) % len(endpoints)][1]
               - endpoints[(i + 1) % len(endpoints)][0] * endpoints[i][1]
               for i in range(len(endpoints))) / 2
    if (area < 0) != negative:
        reversed_pen = RecordingPen()
        pen.replay(ReverseContourPen(reversed_pen))
        values = reversed_pen.value
    result = []
    for op, points in values:
        assert op in {'moveTo', 'lineTo', 'curveTo', 'closePath'}
        result.append({'op': op, 'points': [[float(x) - origin[0], float(y) - origin[1]] for x, y in points]})
    assert result[0]['op'] == 'moveTo' and result[-1]['op'] == 'closePath'
    return result


def build_program():
    original = json.loads((OUT / 'TRACE_COMMANDS.json').read_bytes())
    trace_record = json.loads((OUT / 'SOURCE_TRACE.json').read_bytes())
    assert original['path_count'] == 17
    assert trace_record['outputs']['trace'] == ref(OUT / 'upstream-alpha128-trace.svg')
    glyphs = []
    accounted = []
    details = []
    for char in COPY:
        source, edits = [], []
        for pi in SOURCES[char]:
            row = original['paths'][pi]
            contours = row['closed_contours']
            source.append({'path_index': pi, 'contour_indices': list(range(len(contours)))})
            for ci, before in enumerate(contours):
                endpoints = [command['points'][-1] for command in before if command['points']]
                old_area = sum(endpoints[i][0] * endpoints[(i + 1) % len(endpoints)][1]
                               - endpoints[(i + 1) % len(endpoints)][0] * endpoints[i][1]
                               for i in range(len(endpoints))) / 2
                negative = old_area < 0
                after = [command_rows(d, ORIGINS[char], negative) for d in DRAWINGS[(pi, ci)]]
                reason = ('Rebuild the real original interior counter with explicit reversed winding; '
                          'its source identity is preserved and its geometry is changed.') if negative else (
                          'Manual redraw of this real generated stroke component: differentiated light '
                          'horizontals, stronger upright bones, short oblique terminals and sparse closed '
                          'Bezier silhouettes. Splits are declared, rather than called unchanged tracing.')
                edits.append({'op': 'replace_contour', 'path_index': pi, 'contour_index': ci,
                              'before_sha256': commands_sha(before),
                              'after_contours': after, 'reason': reason})
                accounted.append((pi, ci))
                details.append({'char': char, 'path_index': pi, 'contour_index': ci,
                                'source_negative_counter': negative, 'original_commands': len(before),
                                'new_contours': len(after), 'new_commands': [len(c) for c in after]})
        glyphs.append({'char': char, 'source': source, 'edits': edits,
                       'placement': {'scale': 1.0, 'tx': ORIGINS[char][0], 'ty': ORIGINS[char][1]}})
    expected = [(row['path_index'], ci) for row in original['paths']
                for ci in range(len(row['closed_contours']))]
    assert sorted(accounted) == sorted(expected) and len(accounted) == len(set(accounted))
    assert set(DRAWINGS) == set(expected)
    program = {'schema': 'vpd-source-bound-glyph-edits/v1', 'formal_version': 24,
               'copy': COPY, 'source_trace': ref(OUT / 'upstream-alpha128-trace.svg'),
               'glyphs': glyphs,
               'negative_space': {'art_direction': ref(OUT / 'ART_DIRECTION.json'),
                                  'operation': 'difference-union', 'fix_winding': True,
                                  'keep_starting_points': True, 'clockwise': False}}
    notes = {'schema': 'vpd-v24-real-manual-contour-authorship/v1', 'formal_version': 24,
             'copy': COPY, 'source_generation': trace_record['generated_png'],
             'trace': trace_record['outputs']['trace'], 'maker_source': ref(Path(__file__)),
             'original_path_count': 17, 'original_contour_count': len(expected),
             'original_contours_accounted_once': True, 'pure_noise_contours_dropped': [],
             'source_noise_boundary': 'Most visible dust was low alpha and did not survive the fixed alpha128 tracing threshold. No surviving source contour is relabelled as noise.',
             'source_roles': SOURCES, 'replacement_details': details,
             'manual_redraw': True, 'original_generated_commands_preserved_in_final': False,
             'outline_method': 'Original generated character/stroke identities were read and assigned. New outer/counter contours were explicitly authored with short slant caps, fine horizontals and stronger verticals. Positive uniform per-character placement follows local outline edits. The independent guard kernel performs unions, literal ART_DIRECTION differences and SVG serialization.',
             'key_stroke_changes': {'杯': 'Wood vertical bends right toward the rim; left fall terminates above its highlight. The right component is tall, narrow and open.',
                                    '茶': 'Grass/crown and central cross separate their stroke weights; the right fall turns upward near its end.',
                                    '慢': 'Long upright 忄, explicit compressed 日/罒 counters and a short rising right terminal of 又.',
                                    '下': 'Thin long horizontal, narrow upright and a tapered short right dot.',
                                    '来': 'Open crossing bones, thin horizontals and differently extended left/right feet.',
                                    '一': 'One low curved fine horizontal, placed against the lower height of 杯.',
                                    '，': 'Small continuous slanted turn, not an isolated large dot.'},
             'font_files_loaded': 0, 'reference_glyph_outlines_copied': 0,
             'additional_generated_assets': 0, 'business_state_writes': 0,
             'Figma_Drive_Git_writes': 0, 'aesthetic_pass_claimed': False,
             'human_acceptance_claimed': False}
    return program, notes


def main():
    outputs = [OUT / 'V24_GLYPH_EDIT_MANIFEST.json', OUT / 'SOURCE_REAUTHORING_NOTES.json']
    assert not any(path.exists() for path in outputs), 'AUTHORED_PROGRAM_ALREADY_EXISTS'
    program, notes = build_program()
    for path, value in zip(outputs, (program, notes)):
        raw = jb(value)
        with path.open('xb') as handle:
            handle.write(raw)
        assert path.read_bytes() == raw
    print(json.dumps({'action': 'one-authored-program-written', 'manifest': ref(outputs[0]),
                      'notes': ref(outputs[1]), 'source_contours': notes['original_contour_count'],
                      'new_closed_contours': sum(row['new_contours'] for row in notes['replacement_details']),
                      'aesthetic_pass_claimed': False}, ensure_ascii=True))


if __name__ == '__main__':
    main()
