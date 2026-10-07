from pathlib import Path
import os,json,hashlib
from exact_composite import compose
root=Path(__file__).resolve().parent
os.chdir(root)
plan=json.loads(Path('portable-plan.json').read_text())
patches=json.loads(Path('portable-patches.json').read_text())
provenance,report=compose('original.jpg','reconstructed.png',plan,patches)
for name,value in [('reconstruction-provenance.json',provenance),('reconstruction-postconditions.json',report)]:
    Path(name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
from PIL import Image,ImageChops
with Image.open('delivered-final.png') as a,Image.open('reconstructed.png') as b:
    assert a.size==b.size==(709,1536)
    assert ImageChops.difference(a,b).getbbox() is None
assert report['engineering_pass'] and report['outside_mask_changed_pixels']==0
assert hashlib.sha256(Path('reconstructed.png').read_bytes()).digest()==hashlib.sha256(Path('delivered-final.png').read_bytes()).digest()
print('PASS: same PNG bytes, exact dimensions, outside mask diff=0; strict typography verdict remains FAIL')
