#!/usr/bin/env python3
from pathlib import Path

p=Path(__file__).resolve().parent/'vpd_record_v6_and_prepare_figma_vector_reconstruction.py'
src=p.read_text(encoding='utf-8')
src=src.replace("'phase':'V6_FIGMA_VECTOR_RECONSTRUCTION',\n        'v6_execution':er,", "'phase':'V6_FIGMA_VECTOR_RECONSTRUCTION',\n        'selected_direction':{'豆坊':'B','茶作':'D'},\n        'v6_execution':er,")
src=src.replace("'selected_direction':tr['selected_direction']", "'selected_direction':{'豆坊':'B','茶作':'D'}")
ns={'__name__':'__main__','__file__':str(p)}
exec(compile(src,str(p),'exec'),ns,ns)
