import pathlib
b=pathlib.Path('.liu-visual-private/s7_outline_implementation');s=pathlib.Path('.liu-visual-private/s6_outline_implementation/render-preview.cjs').read_text(encoding='utf8');(b/'render-preview.cjs').write_text(s.replace('S6','S7').replace('s6-','s7-'),encoding='utf8')
