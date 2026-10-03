"""Mechanical export fidelity: keep Figma design only inside declared envelopes.

This copies immutable source RGB outside the overlays; no new photo content is
invented. Raw Figma export remains preserved. This is not hidden-photo recovery.
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True)
    p.add_argument('--raw',required=True)
    p.add_argument('--output',required=True)
    p.add_argument('--report',required=True)
    p.add_argument('--protection',default='continuity/vpd/codex_takeover_20261003/PHOTO_PROTECTION.json')
    a=p.parse_args()
    protection=json.loads(Path(a.protection).read_text(encoding='utf-8'))
    assert digest(a.source)==protection['source']['sha256'], 'Source identity mismatch'
    source=np.array(Image.open(a.source).convert('RGB'))
    raw=np.array(Image.open(a.raw).convert('RGB'))
    assert source.shape==raw.shape==(1024,1536,3), 'Dimensions changed'
    protected=np.ones(source.shape[:2],dtype=bool)
    for x0,y0,x1,y1 in protection['visible_design_overlay_envelopes']:
        protected[y0:y1,x0:x1]=False
    diff=np.abs(raw.astype(np.int16)-source.astype(np.int16))
    count=int(np.any(diff!=0,axis=2)[protected].sum())
    # Only compensate documented renderer rounding, never mask a changed photo.
    assert int(diff[protected].max())<=1, 'Beyond known one-level Figma rounding; stop'
    final=raw.copy(); final[protected]=source[protected]
    assert np.array_equal(final[protected],source[protected])
    assert np.array_equal(final[~protected],raw[~protected])
    output=Path(a.output);output.parent.mkdir(parents=True,exist_ok=True)
    Image.fromarray(final).save(output,compress_level=9)
    decoded=np.array(Image.open(output).convert('RGB'))
    report={
        'source':{'path':a.source,'sha256':digest(a.source)},
        'raw_figma_export':{'path':a.raw,'sha256':digest(a.raw)},
        'final_delivery_export':{'path':a.output,'sha256':digest(a.output)},
        'dimensions':[1536,1024],
        'overlay_envelopes':protection['visible_design_overlay_envelopes'],
        'protected_pixels_compared':int(protected.sum()),
        'raw_protected_pixels_changed':count,
        'raw_max_channel_difference':int(diff[protected].max()),
        'protected_pixels_changed':int(np.any(decoded!=source,axis=2)[protected].sum()),
        'design_pixels_equal_raw_figma':bool(np.array_equal(decoded[~protected],raw[~protected])),
        'operation':'SOURCE_RGB_COPY_OUTSIDE_OVERLAYS',
        'photo_generation':False,'hidden_background_recovery':False}
    Path(a.report).parent.mkdir(parents=True,exist_ok=True)
    Path(a.report).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__':main()
