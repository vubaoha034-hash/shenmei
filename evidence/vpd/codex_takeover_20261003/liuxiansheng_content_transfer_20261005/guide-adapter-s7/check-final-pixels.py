from PIL import Image,ImageFilter
import numpy as np,pathlib,json,re
b=pathlib.Path('.liu-visual-private/s7_outline_implementation');a=np.array(Image.open(b/'S7_CREAM_ALPHA_TECHNICAL.png').getchannel('A'));solid=np.array(Image.open(b/'S7_SOLID_ALPHA_TECHNICAL.png').getchannel('A'));index=np.array(Image.open(b/'TIER_INDEX_FIELD_TECHNICAL.png'));labels=np.zeros_like(a);labels[420:612,216:800]=index
expected=np.array([255,235,204,153,89,0],dtype=np.int16)[labels];inside=solid==255;error=np.abs(a.astype(np.int16)-expected);bad=np.argwhere(inside&(error>1));maxerr=int(error[inside].max())
def comps(mask):
 h,w=mask.shape;seen=np.zeros_like(mask,dtype=bool);counts=[]
 for y,x in zip(*np.where(mask)):
  if seen[y,x]:continue
  q=[(int(y),int(x))];seen[y,x]=True
  for yy,xx in q:
   for dy in [-1,0,1]:
    for dx in [-1,0,1]:
     yp,xp=yy+dy,xx+dx
     if 0<=yp<h and 0<=xp<w and mask[yp,xp] and not seen[yp,xp]:seen[yp,xp]=True;q.append((yp,xp))
  counts.append(len(q))
 return counts
counts_x=sorted(comps(a[425:610,430:610]>=128),reverse=True);counts_s=sorted(comps(a[425:610,610:800]>=128),reverse=True)
negative={f'{x},{y}':int(a[y,x]) for x,y in [(495,565),(495,570),(492,575),(684,505),(680,508),(685,548),(685,555)]}
safe=np.array(Image.fromarray((solid>=254).astype(np.uint8)*255).filter(ImageFilter.MinFilter(7)))==255
stats=[]
for t in range(6):
 mask=safe&(labels==t);cs=comps(mask[420:612,216:800]);stats.append({'tier':t,'cream_opacity':[1,.92,.8,.6,.35,0][t],'safe_interior_source_designated_pixels':int(mask.sum()),'source_designated_components':len(cs),'component_density_per10000safe':len(cs)/safe.sum()*10000,'median_component_pixels':float(np.median(cs)) if cs else 0,'actual_alpha_min_max':([int(a[mask].min()),int(a[mask].max())] if mask.any() else [])})
renderstats={}
for threshold in [150,180,210,225,235]:
 image=np.array(Image.open(b/'S7_ORANGE_HIDDEN_TECHNICAL_PREVIEW.png').convert('RGB')).mean(2);m=safe&(image<threshold);cs=comps(m[420:612,216:800]);renderstats[str(threshold)]={'pixels':int(m.sum()),'components':len(cs),'component_density_per10000safe':len(cs)/safe.sum()*10000,'median_component_pixels':float(np.median(cs)) if cs else 0}
check={'schema':'s7-actual-svg-sharp-pixel-check/v1','tested_render':'S7_CREAM_ALPHA_TECHNICAL.png from actual final SVG via sharp','solid_fully_covered_centers_tested':int(inside.sum()),'expected_alpha8':[255,235,204,153,89,0],'interior_alpha_max_abs_error':maxerr,'interior_alpha_errors_above1':len(bad),'error_examples_yx':bad[:20].tolist(),'XIAN_alpha128_components':counts_x,'SHENG_alpha128_components':counts_s,'negative_space_actual_alpha':negative,'safe_interior_pixels':int(safe.sum()),'source_tier_stats':stats,'rendered_green_composite_Y_stats':renderstats,'composite_Y_limit':'MeanRGB over exact solid7px-eroded safe support, no orange; background affects numbers, not original reference alpha. Statistics are diagnostic and never taste pass.','aesthetic_verdict':None}
(b/'LOCAL_PIXEL_CHECK.json').write_text(json.dumps(check,indent=2)+'\n');print(json.dumps({k:check[k] for k in ['solid_fully_covered_centers_tested','interior_alpha_max_abs_error','interior_alpha_errors_above1','XIAN_alpha128_components','SHENG_alpha128_components','negative_space_actual_alpha']}))
