"""Reference algorithm for S7 technical addendum; exact pixel cells, no tracing or style changes."""
import numpy as np
import pathops

def mask_to_winding_path(mask, origin=(0, 0)):
    mask = np.asarray(mask, dtype=bool)
    if mask.ndim != 2:
        raise ValueError('mask must be two dimensional')
    ox, oy = origin
    if int(ox) != ox or int(oy) != oy:
        raise ValueError('pixel-grid origin must be integral')
    out = pathops.Path(fillType=pathops.FillType.WINDING)
    runs = 0
    for y, row in enumerate(mask):
        endpoints = np.flatnonzero(np.diff(np.r_[False, row, False].astype(np.int8)))
        for x0, x1 in zip(endpoints[::2], endpoints[1::2]):
            # Every contour has identical orientation; each run occupies [x0,x1] x [y,y+1].
            # Adjacent cells/rows may share boundaries, but have no positive-area overlap.
            left, right, top = int(x0)+ox, int(x1)+ox, y+oy
            out.moveTo(left, top)
            out.lineTo(right, top)
            out.lineTo(right, top+1)
            out.lineTo(left, top+1)
            out.close()
            runs += 1
    return out, {'mask_pixels': int(mask.sum()), 'horizontal_runs': runs, 'raw_path_area': float(out.area)}
