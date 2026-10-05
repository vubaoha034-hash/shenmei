"""One bounded source-color/soft-alpha foreground trial, not image generation.

Reads the canonical JPEG and existing S1 masks. Does not rewrite S1, reconstruct
photography, change typography placement, or claim to recover original alpha.
The output is raster IMAGE data intended to remain a separate optional Figma
layer while the S1 vector contours remain independently editable.
"""
from __future__ import annotations
from collections import deque
import hashlib
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
ROOT = BASE.parents[2]
SOURCE = ROOT/'.liu-visual-private/product-type-integration-20261004/SHANYEJI-canonical-readback-20261005.jpg'
SHA = '9a29fbdc7dd908017924bed270e8dfe18351519eed3fa7bc7001789f2a383414'
S1 = BASE/'02_full_final_vector_detail'
BASELINE = BASE/'00_main_baseline'
W,H = 960,1280


def filter_bool(mask: np.ndarray, size: int, kind: str) -> np.ndarray:
    image = Image.fromarray(mask.astype(np.uint8)*255)
    operation = ImageFilter.MaxFilter(size) if kind=='dilate' else ImageFilter.MinFilter(size)
    return np.asarray(image.filter(operation)) > 0


def fill_holes(mask: np.ndarray) -> np.ndarray:
    remaining = ~mask.copy()
    h,w = mask.shape
    queue = deque()
    for x in range(w):
        for y in (0,h-1):
            if remaining[y,x]:
                remaining[y,x]=False; queue.append((y,x))
    for y in range(h):
        for x in (0,w-1):
            if remaining[y,x]:
                remaining[y,x]=False; queue.append((y,x))
    while queue:
        y,x=queue.popleft()
        for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)):
            ny,nx=y+dy,x+dx
            if 0<=ny<h and 0<=nx<w and remaining[ny,nx]:
                remaining[ny,nx]=False; queue.append((ny,nx))
    return mask | remaining


def components_at_least(mask: np.ndarray, minimum: int) -> np.ndarray:
    remainder=mask.copy(); result=np.zeros_like(mask)
    h,w=mask.shape
    for y,x in zip(*np.nonzero(mask)):
        if not remainder[y,x]: continue
        queue=deque([(int(y),int(x))]); points=[]; remainder[y,x]=False
        while queue:
            py,px=queue.popleft(); points.append((py,px))
            for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)):
                ny,nx=py+dy,px+dx
                if 0<=ny<h and 0<=nx<w and remainder[ny,nx]:
                    remainder[ny,nx]=False; queue.append((ny,nx))
        if len(points)>=minimum:
            yy,xx=zip(*points); result[yy,xx]=True
    return result


def full_mask(item: dict, directory: Path) -> np.ndarray:
    x0,y0,x1,y1=item['bbox']
    mask=np.asarray(Image.open(directory/'masks'/f"{item['name']}.png").convert('L'))<128
    result=np.zeros((H,W),dtype=bool); result[y0:y1,x0:x1]=mask
    return result


def local_box(bbox: list[int], margin: int = 10) -> tuple[int,int,int,int]:
    x0,y0,x1,y1=bbox
    return max(0,x0-margin),max(0,y0-margin),min(W,x1+margin),min(H,y1+margin)


def soft_foreground(source: np.ndarray, item: dict, mask: np.ndarray, all_ink: np.ndarray,
                    white_under_orange: np.ndarray, old_main: np.ndarray | None = None) -> tuple[Image.Image,dict,np.ndarray]:
    name=item['name']; box=local_box(item['bbox'])
    x0,y0,x1,y1=box
    rgb=source[y0:y1,x0:x1].astype(np.float32)
    core_mask=mask[y0:y1,x0:x1]
    is_main=name.startswith('main_')
    is_orange=name.startswith('orange_')
    is_gold=name.startswith('gold_')
    if is_main and old_main is not None:
        observed=old_main[y0:y1,x0:x1]
        closed=fill_holes(observed)
        clear_counters=components_at_least(closed & ~observed,12)
        # Keep large observed counters, while letting dark grain retain graded
        # opacity inferred from the actual source colors rather than hard cuts.
        support=closed
        preserve_hole_core=filter_bool(clear_counters,3,'erode')
    else:
        support=fill_holes(core_mask)
        clear_counters=components_at_least(support & ~core_mask,3)
        preserve_hole_core=filter_bool(clear_counters,3,'erode')
    support=filter_bool(support,5 if not is_main else 3,'dilate')
    support &= ~preserve_hole_core
    outer=filter_bool(core_mask,15,'dilate') & ~filter_bool(core_mask,7,'dilate')
    outer &= ~all_ink[y0:y1,x0:x1]
    background_pixels=rgb[outer]
    if len(background_pixels)<12:
        background_pixels=rgb[~support]
    if len(background_pixels)<12:
        background_pixels=rgb.reshape(-1,3)
    bg=np.median(background_pixels,axis=0)
    fg_pixels=rgb[core_mask]
    if is_orange:
        colored=(fg_pixels[:,0]-fg_pixels[:,1]>34)&(fg_pixels[:,1]-fg_pixels[:,2]>30)
        if colored.sum()>12: fg_pixels=fg_pixels[colored]
    fg=np.quantile(fg_pixels,.92 if is_main else .85,axis=0).astype(np.float32)
    bgmap=np.broadcast_to(bg,rgb.shape).copy()
    if name.startswith('orange_line_'):
        over_white=white_under_orange[y0:y1,x0:x1]
        bgmap[over_white]=[247,244,236]
    direction=fg-bgmap
    alpha=np.sum((rgb-bgmap)*direction,axis=2)/np.maximum(np.sum(direction*direction,axis=2),1.)
    alpha=np.clip(alpha,0,1)
    r,g,b=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
    if is_orange:
        rg=(r-g-(bgmap[:,:,0]-bgmap[:,:,1]))/np.maximum(fg[0]-fg[1]-(bgmap[:,:,0]-bgmap[:,:,1]),12.)
        gb=(g-b-(bgmap[:,:,1]-bgmap[:,:,2]))/np.maximum(fg[1]-fg[2]-(bgmap[:,:,1]-bgmap[:,:,2]),12.)
        alpha=np.minimum(alpha,(np.clip(rg,0,1)+np.clip(gb,0,1))*.5)
    elif is_gold:
        alpha*=np.clip((r-b-13)/18,0,1)*np.clip((g-b-15)/18,0,1)
    else:
        alpha*=np.clip((42-(g-r))/25,0,1)*np.clip((80-(g-b))/42,0,1)
    alpha*=support
    alpha[alpha<.045]=0
    alpha[preserve_hole_core]=0
    # Preserve the JPEG's actual RGB in high-confidence cores. Estimated edge
    # RGB removes an approximate local background contribution for soft rims.
    estimate=(rgb-(1-alpha[:,:,None])*bgmap)/np.maximum(alpha[:,:,None],.05)
    estimate=np.clip(estimate,0,255)
    direct_core=(alpha>=.94)&core_mask
    estimate[direct_core]=rgb[direct_core]
    alpha[direct_core]=1
    rgba=np.zeros((*alpha.shape,4),dtype=np.uint8)
    rgba[:,:,:3]=np.rint(estimate).astype(np.uint8)
    rgba[:,:,3]=np.rint(alpha*255).astype(np.uint8)
    rgba[rgba[:,:,3]==0,:3]=0
    output=Image.new('RGBA',(W,H))
    output.paste(Image.fromarray(rgba,'RGBA'),(x0,y0))
    roi_support=np.zeros((H,W),dtype=bool); roi_support[y0:y1,x0:x1]=support
    data={'name':name,'source_bbox':item['bbox'],'processing_bbox':list(box),'estimated_foreground_RGB':[float(v) for v in fg],
          'estimated_background_RGB':[float(v) for v in bg],'nonzero_alpha_pixels':int((rgba[:,:,3]>0).sum()),
          'intermediate_alpha_pixels':int(((rgba[:,:,3]>0)&(rgba[:,:,3]<255)).sum()),'source_RGB_exact_core_pixels':int(direct_core.sum()),
          'preserved_clear_hole_core_pixels':int(preserve_hole_core.sum()),'method':'local projected color matte; direct source RGB in confident core, estimated RGB at soft edge'}
    return output,data,roi_support


def combined_seal(source: np.ndarray, orange_item: dict, orange_mask: np.ndarray) -> tuple[Image.Image,dict,np.ndarray]:
    box=local_box(orange_item['bbox'],3); x0,y0,x1,y1=box
    body=orange_mask[y0:y1,x0:x1]
    rgb=source[y0:y1,x0:x1].astype(np.float32)
    alpha=np.asarray(Image.fromarray(body.astype(np.uint8)*255).filter(ImageFilter.GaussianBlur(.55))).astype(np.float32)/255
    interior=filter_bool(body,3,'erode'); alpha[interior]=1
    support=filter_bool(body,3,'dilate'); alpha*=support
    rgba=np.zeros((*body.shape,4),dtype=np.uint8); rgba[:,:,:3]=rgb.astype(np.uint8); rgba[:,:,3]=np.rint(alpha*255).astype(np.uint8)
    rgba[rgba[:,:,3]==0,:3]=0
    output=Image.new('RGBA',(W,H)); output.paste(Image.fromarray(rgba,'RGBA'),(x0,y0))
    allowed=np.zeros((H,W),dtype=bool); allowed[y0:y1,x0:x1]=support
    return output,{'name':'LiJiaBan_combined_source_color','processing_bbox':list(box),'nonzero_alpha_pixels':int((alpha>0).sum()),
                   'source_RGB_exact_core_pixels':int(interior.sum()),'intermediate_alpha_pixels':int(((alpha>0)&(alpha<1)).sum()),
                   'method':'source RGB preserves orange paper and actual black characters; only silhouette edge receives a 0.55px approximate soft alpha'},allowed


def tiny_corner(source: np.ndarray) -> tuple[Image.Image,dict]:
    box=(908,1249,958,1280); x0,y0,x1,y1=box
    rgb=source[y0:y1,x0:x1].astype(np.float32)
    ellipse=Image.new('L',(x1-x0,y1-y0))
    ImageDraw.Draw(ellipse).ellipse((7,7,44,30),fill=255)
    support=np.asarray(ellipse)>0
    background=np.median(rgb[~support],axis=0)
    foreground=np.array([225,229,220],dtype=np.float32)
    direction=foreground-background
    alpha=np.clip(np.sum((rgb-background)*direction,axis=2)/np.sum(direction*direction),0,.38)
    alpha*=support
    alpha[alpha<.018]=0
    rgba=np.zeros((*alpha.shape,4),dtype=np.uint8)
    rgba[:,:,:3]=foreground.astype(np.uint8); rgba[:,:,3]=np.rint(alpha*255).astype(np.uint8)
    rgba[rgba[:,:,3]==0,:3]=0
    return Image.fromarray(rgba,'RGBA'),{'name':'tiny_corner_UNREADABLE_source_graphic','bbox':list(box),'nonzero_alpha_pixels':int((rgba[:,:,3]>0).sum()),
        'alpha_max':int(rgba[:,:,3].max()),'estimated_background_RGB':[float(v) for v in background],
        'method':'weak positive source contrast inside a restricted oval ROI; nominal pale ink projection, opacity capped at 0.38',
        'content':'UNREADABLE, no character transcription','limitation':'source is very faint and includes JPEG/background contamination; shape/opacity are approximate'}


def darkgray(image: Image.Image) -> Image.Image:
    return Image.alpha_composite(Image.new('RGBA',image.size,(39,41,39,255)),image).convert('RGB')


def main() -> None:
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=SHA: raise SystemExit('SOURCE_SHA_MISMATCH')
    source_image=Image.open(SOURCE).convert('RGB'); source=np.asarray(source_image)
    manifest=json.loads((S1/'MANIFEST.json').read_text(encoding='utf-8'))
    prior=json.loads((BASELINE/'MANIFEST.json').read_text(encoding='utf-8'))
    items={x['name']:x for x in manifest['groups']}
    old={x['name']:full_mask(x,BASELINE) for x in prior['groups'] if x['name'].startswith('main_')}
    masks={name:full_mask(item,S1) for name,item in items.items()}
    all_ink=np.zeros((H,W),dtype=bool)
    white_under=np.zeros((H,W),dtype=bool)
    for name,mask in masks.items():
        all_ink |= mask
        if name.startswith('main_'):
            x0,y0,x1,y1=items[name]['bbox']
            white_under[y0:y1,x0:x1] |= fill_holes(mask[y0:y1,x0:x1])
    typography=Image.new('RGBA',(W,H))
    allowed_union=np.zeros((H,W),dtype=bool)
    group_reports=[]; (HERE/'layers').mkdir(exist_ok=True)
    for item in manifest['groups']:
        name=item['name']
        if name=='LiJiaBan_seal_black_glyphs': continue
        if name=='LiJiaBan_seal_orange_shape':
            image,report,support=combined_seal(source,item,masks[name])
        else:
            image,report,support=soft_foreground(source,item,masks[name],all_ink,white_under,old.get(name))
        image.save(HERE/'layers'/f'{name}_soft.png')
        typography=Image.alpha_composite(typography,image)
        allowed_union |= support; group_reports.append(report)
    tiny,tiny_report=tiny_corner(source)
    tiny.save(HERE/'tiny_corner_UNREADABLE_graphic.png')
    all_foreground=typography.copy(); tiny_full=Image.new('RGBA',(W,H)); tiny_full.paste(tiny,(908,1249))
    all_foreground=Image.alpha_composite(all_foreground,tiny_full)
    typography.save(HERE/'SHANYEJI_soft_foreground_typography.png')
    all_foreground.save(HERE/'SHANYEJI_soft_foreground_all.png')
    darkgray(all_foreground).save(HERE/'SHANYEJI_soft_foreground_darkgray_preview.png')
    # Same single trial composited over retained S1 shows the practical residual
    # from opaque underlying vector paint. It is a comparison, not a new asset.
    s1_png=Image.open(S1/'SHANYEJI_typography_transparent.png').convert('RGBA')
    over_s1=Image.alpha_composite(s1_png,all_foreground)
    darkgray(over_s1).save(HERE/'S1_vectors_plus_same_soft_layer_darkgray.png')
    comparison_rois={'main_mark':(137,410,824,626),'main_shan_grain':(216,422,429,552),'ye_crossing':(435,438,646,609),
      'gold_english':(211,548,365,620),'gold_chinese':(291,632,666,689),'orange_handwriting':(218,771,742,866),
      'top_english':(40,28,925,112),'footer_attribution':(25,1148,941,1259),'tiny_corner_UNREADABLE':(908,1249,958,1280)}
    (HERE/'comparisons').mkdir(exist_ok=True)
    preview=darkgray(all_foreground)
    for name,box in comparison_rois.items():
        left=source_image.crop(box); right=preview.crop(box)
        pair=Image.new('RGB',(left.width*2,left.height),'#272927'); pair.paste(left,(0,0)); pair.paste(right,(left.width,0))
        pair.save(HERE/'comparisons'/f'{name}_source_vs_soft.png')
    alpha=np.asarray(all_foreground)[:,:,3]
    typ_alpha=np.asarray(typography)[:,:,3]
    overlay=np.zeros((H,W,4),dtype=np.uint8); overlay[:,:,:3]=[255,20,185]; overlay[:,:,3]=np.rint(alpha*.6).astype(np.uint8)
    Image.alpha_composite(source_image.convert('RGBA'),Image.fromarray(overlay,'RGBA')).save(HERE/'SHANYEJI_soft_mask_overlay.png')
    checks={'size':[W,H],'RGBA':all_foreground.mode,'single_trial_only':True,'S1_masks_or_vectors_modified':False,
      'outside_text_support_alpha_nonzero':int(((typ_alpha>0)&~allowed_union).sum()),
      'intermediate_alpha_pixels':int(((alpha>0)&(alpha<255)).sum()),'nonzero_alpha_pixels':int((alpha>0).sum()),
      'clear_canvas_empty_alpha':int(alpha[300,480]),'shan_main_counter_probe_alpha':int(alpha[518,261]),
      'WANCE_Lambda_opening_probe_alpha':int(alpha[1202,513]),'WANCE_Lambda_opening_probe_xy':[513,1202],'tiny_graphic_independent_file':True,
      'source_JPEG_unchanged_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest()}
    result={'trial':'S2_SINGLE_SOFT_FOREGROUND_TRIAL','source_sha256':SHA,'source_size':[W,H],'groups':group_reports,'tiny_graphic':tiny_report,'checks':checks,
      'Figma_instruction':'Keep S1 vectors editable. Import typography-only PNG plus tiny graphic crop at x908,y1249,w50,h31 as separate IMAGE objects, or use the all-in-one PNG once. Never use both forms at the same time.',
      'limitations':['This is an approximate foreground matte from a JPEG, not recovered original alpha.',
        'RGB at high-confidence cores comes directly from the source; soft edges use estimated local photograph background and foreground colors.',
        'Residual photographic/JPEG color contamination, halos, cutout/opacity errors and imperfect grain remain possible.',
        'An opaque vector underneath a semi-transparent soft pixel remains visible; S1+soft comparison records this residual.',
        'Tiny corner shape/opacity is especially uncertain and content remains UNREADABLE.',
        'No source photo pixels outside the bounded supports are carried into the typography image; no background recovery or image generation was used.',
        'No independent fidelity pass or human approval is claimed.'],
      'assets':{p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(HERE.glob('*.png'))}}
    (HERE/'SOFT_TRIAL_MANIFEST.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'status':'ONE_TRIAL_CREATED_REVIEW_PENDING','transparent_all_sha256':result['assets']['SHANYEJI_soft_foreground_all.png']['sha256'],'checks':checks},ensure_ascii=False))


if __name__=='__main__': main()
