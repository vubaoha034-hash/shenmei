from pathlib import Path
import json, hashlib
import numpy as np
import cv2
from PIL import Image

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'repair-v2';OUT.mkdir(exist_ok=True)
ref=ROOT.parent/'attachments/3cb32e1b-e60b-459c-a610-b2710a3d760b/1000031560.jpg'
source=Image.open(ref);source.load()
prior=Image.open(ROOT/'map-outside-test.png');prior.load()
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
regions=json.loads((ROOT/'regions.json').read_text());patches=json.loads((ROOT/'patches.json').read_text())
title=next(r for r in regions if r['id']=='title')
x,y,w,h=[title[k] for k in ('x','y','width','height')]
asset=Image.open(ROOT.parent/'generated_images/exec-1720aae8-4417-4ad0-88ae-77e9c122c7c3.png').convert('RGBA')
glyph=asset.crop(asset.getchannel('A').getbbox()).resize((665,255),Image.Resampling.LANCZOS)
protection=Image.new('L',(w,h),0);protection.paste(glyph.getchannel('A'),(4,7))
protected=np.array(protection)>0
rgb=np.array(prior.crop((x,y,x+w,y+h)))
native=np.array(source)
allowed=np.zeros((h,w),np.uint8)
# Located by actually comparing the original title and enlarged saved output.
windows=[(128,996,153,1078),(302,994,338,1032),(60,982,107,1026),(170,821,194,844),(519,843,548,864),(385,896,420,916)]
for a,b,c,d in windows:allowed[b-y:d-y,a-x:c-x]=255
# Change only visible cleanup residues in these small windows, plus their immediate edge.
lum=cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY)
residue=((lum>12)&(allowed>0)&(~protected)).astype(np.uint8)*255
mask=cv2.dilate(residue,np.ones((3,3),np.uint8))
mask[(allowed==0)|protected]=0
cleaned=cv2.inpaint(rgb,mask,5,cv2.INPAINT_NS)
sample_rows=[]
for ly in range(h):
    gy=y+ly
    if gy<950:continue
    row=native[gy].astype(int)
    stable=(row[:,0]<20)&(row[:,1]<8)&(row[:,2]<8)
    # Existing unlettered dark background; deterministic sampling, not hidden-pixel recovery.
    if not stable.any():raise RuntimeError('STOP: native dark background samples unavailable')
    sample=np.median(row[stable],axis=0).astype(np.uint8)
    cleaned[ly,mask[ly]>0]=sample
    if (mask[ly]>0).any():sample_rows.append(dict(y=gy,rgb=sample.tolist(),sample_count=int(stable.sum())))
mp=OUT/'cleanup-mask.png';pp=OUT/'cleanup-patch.png'
Image.fromarray(mask).save(mp);Image.fromarray(cleaned).convert('RGBA').save(pp)
regions.append(dict(id='old_glyph_residue_cleanup',role='minimal_text_cleanup',parent_region_id='title',x=x,y=y,width=w,height=h,mask_source=str(mp),mask_sha256=sha(mp)))
patches.append(dict(region_id='old_glyph_residue_cleanup',path=str(pp),sha256=sha(pp),role='LOCAL_TEXT_OR_TEXTURE_CANDIDATE'))
(OUT/'regions.json').write_text(json.dumps(regions,indent=2))
(OUT/'patches.json').write_text(json.dumps(patches,indent=2))
protection.save(OUT/'approved-title-alpha.png')
(OUT/'cleanup-method.json').write_text(json.dumps(dict(method='SCOPED_VISIBLE_RESIDUE_CLEANUP_WITH_NATIVE_DARK_BACKGROUND_ROW_SAMPLES',approved_prior_sha256=sha(ROOT/'map-outside-test.png'),reference_sha256=sha(ref),cleanup_windows=windows,cleanup_pixel_count=int((mask>0).sum()),new_title_alpha_preserved=True,rows=sample_rows,hidden_background_exact_recovery_claimed=False),indent=2))
print(json.dumps(dict(cleanup_pixels=int((mask>0).sum()),mask_sha256=sha(mp),patch_sha256=sha(pp))))
