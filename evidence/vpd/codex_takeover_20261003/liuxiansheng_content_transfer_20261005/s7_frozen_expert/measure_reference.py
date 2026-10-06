"""Read-only source analysis; writes only private numerical/crop evidence, never a successor wordmark."""
from PIL import Image,ImageFilter
import numpy as np,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
REF=ROOT/'.liu-visual-private/product-type-integration-20261004/SHANYEJI-canonical-readback-20261005.jpg'
S6=ROOT/'.liu-visual-private/liuxiansheng_transfer_20261005/FIGMA_COMPLETE_S6.png'
ROI=(216,420,800,612)
def components(b):
 h,w=b.shape;seen=np.zeros_like(b);out=[]
 for y,x in zip(*np.where(b)):
  if seen[y,x]:continue
  q=[(int(y),int(x))];seen[y,x]=True
  for yy,xx in q:
   for dy in [-1,0,1]:
    for dx in [-1,0,1]:
     y2,x2=yy+dy,xx+dx
     if 0<=y2<h and 0<=x2<w and b[y2,x2] and not seen[y2,x2]:seen[y2,x2]=True;q.append((y2,x2))
  out.append(q)
 return out
def morph(a,typ,n):return np.array(Image.fromarray(a.astype('uint8')*255).filter(typ(n)))>0
def support(a):
 white=(a.min(2)>180)&((a.max(2)-a.min(2))<50)
 orange=(a[:,:,0]>150)&(a[:,:,1]<200)&(a[:,:,0]-a[:,:,1]>45)&(a[:,:,1]-a[:,:,2]>20)
 full=morph(morph(white,ImageFilter.MaxFilter,5),ImageFilter.MinFilter,5)
 for c in components(~full):
  if len(c)<=50:
   for y,x in c:full[y,x]=True
 return morph(full,ImageFilter.MinFilter,7)&~morph(orange,ImageFilter.MaxFilter,7)
def stats(Y,safe):
 result={'safe_pixels':int(safe.sum()),'thresholds':{}}
 for t in [150,180,210,225,235]:
  cs=components(safe&(Y<t));sz=np.array([len(c) for c in cs]);result['thresholds'][str(t)]={'count':len(cs),'count_per10000':round(float(len(cs)/safe.sum()*10000),3),'pixels':int(sz.sum()),'fraction':round(float(sz.sum()/safe.sum()),6),'singleton_count':int((sz==1).sum()),'area_2_4_count':int(((sz>=2)&(sz<=4)).sum()),'area_5_16_count':int(((sz>=5)&(sz<=16)).sum()),'area_17_64_count':int(((sz>=17)&(sz<=64)).sum()),'area_over64_count':int((sz>64).sum()),'median_area':float(np.median(sz)),'max_area':int(sz.max())}
 return result
a=np.array(Image.open(REF).convert('RGB').crop(ROI)).astype(float);Y=a.mean(2);safe=support(a)
a6=np.array(Image.open(S6).convert('RGB').crop(ROI)).astype(float);Y6=a6.mean(2);safe6=support(a6)
tiles=[]
for y in range(0,192,8):
 for x in range(0,584,8):
  if safe[y:y+8,x:x+8].all():tiles.append([x+216,y+420])
assert len(tiles)==264
raw=np.concatenate([Y[y-420:y-412,x-216:x-208].ravel() for x,y in tiles]);ds=244-raw
result={'schema':'s7-observed-reference-texture-diagnostics/v1','reference_sha256':hashlib.sha256(REF.read_bytes()).hexdigest(),'S6_sha256':hashlib.sha256(S6.read_bytes()).hexdigest(),'ROI_xyxy':ROI,'Y':'mean(encoded RGB)','R':stats(Y,safe),'S6':stats(Y6,safe6),'donor_tiles':len(tiles),'donor_pixels':len(raw),'donor_Y_below_fractions':{str(t):round(float((raw<t).mean()),6) for t in [150,180,210,225,235]},'donor_tier_counts':{str(i):int((np.digitize(ds,[10,25,55,110,165])==i).sum()) for i in range(6)},'limitations':['Segmentation is an observed-image proxy, not ground truth original alpha.','Donor safe support excludes edges and orange; source scan/JPEG artifacts within cream remain part of observed grain.','No successor SVG/image or Figma output was built by this diagnostic.']}
(OUT/'REFERENCE_GRAIN_MEASUREMENTS.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
(OUT/'REFERENCE_DONOR_TILES.json').write_text(json.dumps({'schema':'s7-actual-reference-donor-tiles/v1','reference':str(REF),'reference_sha256':result['reference_sha256'],'ROI':ROI,'tile_size':8,'origins_xy':tiles,'order':'row-major','no_rotations_reflections_resampling':True,'safe_mask_algorithm':'white=minRGB>180 AND rangeRGB<50; PIL MaxFilter5 then MinFilter5; fill all 8-connected zero components area<=50; PIL MinFilter7; subtract orange MaxFilter7; orange=R>150 AND G<200 AND R-G>45 AND G-B>20; donors only if all64 pixels in safe mask'},indent=2)+'\n',encoding='utf8')
print(json.dumps(result))
