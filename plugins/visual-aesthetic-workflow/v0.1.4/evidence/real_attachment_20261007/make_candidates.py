from pathlib import Path
import json, hashlib, sys
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent
REF=ROOT.parent/'attachments/3cb32e1b-e60b-459c-a610-b2710a3d760b/1000031560.jpg'
original=Image.open(REF); original.load()
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def font(n): return ImageFont.truetype(str(ROOT/'NotoSerifCJKsc-Regular.otf'),n)
def lettering(size,text,pt,color,vertical=False):
    layer=Image.new('RGBA',size,(0,0,0,0)); d=ImageDraw.Draw(layer)
    if vertical:
        steps=(size[1]-pt)/max(1,len(text)-1)
        for i,ch in enumerate(text): d.text((size[0]/2,i*steps),ch,font=font(pt),fill=color,anchor='mt')
    else:
        lines=text.split('\n'); total=len(lines)*pt+(len(lines)-1)*3
        for i,line in enumerate(lines):d.text((size[0]/2,(size[1]-total)/2+i*(pt+3)),line,font=font(pt),fill=color,anchor='mt')
    return layer
def old_white(rgb):
    a=rgb.astype(np.int16);gray=cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY)
    local=cv2.morphologyEx(gray,cv2.MORPH_OPEN,np.ones((5,5),np.uint8))
    return ((a[:,:,2]>95)&(a[:,:,0]-a[:,:,2]<100)&(gray.astype(int)-local.astype(int)>10)).astype(np.uint8)*255
regions=[]; patches=[]
specs=[('top','top_text',(258,323,372,350),'地图以外',21,False),('title','main_title_text',(20,815,692,1080),None,0,False),('right','right_vertical_text',(550,442,570,708),'不是所有远方，都写在地图上',12,True),('footer','footer_short_text',(275,1056,434,1088),'离开既定路线，\n去看未知远方',10,False)]
for rid,role,box,text,pt,vertical in specs:
    x,y,x2,y2=box;w,h=x2-x,y2-y;base=original.crop(box);rgb=np.array(base)
    layer=Image.new('RGBA',(w,h),(0,0,0,0))
    if rid=='title':
        if len(sys.argv)<2:raise RuntimeError('local title alpha required')
        source=Image.open(sys.argv[1]).convert('RGBA');alpha=source.getchannel('A')
        if alpha.getextrema()[0]!=0:raise RuntimeError('STOP: actual transparency required')
        tight=source.crop(alpha.getbbox())
        # Only local glyph material is fitted, never original photo or whole-canvas output.
        glyph=tight.resize((665,255),Image.Resampling.LANCZOS)
        layer.alpha_composite(glyph,(4,7))
        a=rgb.astype(int)
        old=((a[:,:,0]>130)&(a[:,:,1]>60)&(a[:,:,2]<90)&(a[:,:,0]-a[:,:,1]>50)).astype(np.uint8)*255
        low=((a[:,:,0]>32)&(a[:,:,1]>12)&(a[:,:,2]<45)&(a[:,:,0]>a[:,:,1]*1.3)&(a[:,:,0]-a[:,:,2]>26)).astype(np.uint8)*255
        old[60:]=np.maximum(old[60:],low[60:])
        # Existing two-line core English is within the title area.
        english_box=(359,55,464,85)
        ex,ey,ex2,ey2=english_box
        old[ey:ey2,ex:ex2]=np.maximum(old[ey:ey2,ex:ex2],old_white(rgb[ey:ey2,ex:ex2]))
        en=Image.new('RGBA',(105,30));d=ImageDraw.Draw(en)
        ef=ImageFont.truetype('/usr/share/fonts/opentype/urw-base35/NimbusRoman-Regular.otf',10)
        d.text((52,1),'for liuxiansheng',font=ef,fill=(237,213,168,255),anchor='mt')
        layer.alpha_composite(en,(359,55))
    else:
        old=old_white(rgb)
        if rid=='right':
            glyph_windows=np.zeros((h,w),np.uint8)
            for i in range(10):
                oy=round(2+i*27.5);glyph_windows[oy:oy+16,2:17]=255
            old=np.minimum(old,glyph_windows)
        layer=lettering((w,h),text,pt,(236,225,197,255),vertical)
    old=cv2.dilate(old,np.ones((5,5),np.uint8))
    cleaned=cv2.inpaint(rgb,old,7,cv2.INPAINT_NS)
    # Cleanup affects old glyph samples only; unchanged samples inherited by finalizer.
    cleanlayer=Image.fromarray(cleaned).convert('RGBA');cleanlayer.alpha_composite(layer)
    new=np.array(layer.getchannel('A'))>0
    mask=np.where((old>0)|new,255,0).astype(np.uint8)
    mp=ROOT/(rid+'-mask.png'); pp=ROOT/(rid+'-patch.png')
    Image.fromarray(mask).save(mp);cleanlayer.save(pp)
    regions.append(dict(id=rid,role=role,x=x,y=y,width=w,height=h,mask_source=str(mp),mask_sha256=sha(mp)))
    patches.append(dict(region_id=rid,path=str(pp),sha256=sha(pp),role='LOCAL_TEXT_OR_TEXTURE_CANDIDATE'))
    Image.fromarray(old).save(ROOT/(rid+'-old-glyph-mask.png'))
(ROOT/'regions.json').write_text(json.dumps(regions,ensure_ascii=False,indent=2))
(ROOT/'patches.json').write_text(json.dumps(patches,ensure_ascii=False,indent=2))
preview=original.copy(); overlay=original.convert('RGBA')
for r in regions:
    m=Image.open(r['mask_source']);ink=Image.new('RGBA',m.size,(255,0,255,100));ink.putalpha(m.point(lambda a:100 if a else 0));overlay.alpha_composite(ink,(r['x'],r['y']))
overlay.convert('RGB').save(ROOT/'mask-scope-preview.png')
print(json.dumps({'regions':regions,'reference_sha256':sha(REF)},ensure_ascii=False))
