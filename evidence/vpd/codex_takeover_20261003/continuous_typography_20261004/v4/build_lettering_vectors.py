"""Preserve one generated lettering source; split and place its traced paths.

No font substitution, photo editing, raster painting, hidden alternatives or
automatic aesthetic judgement. Requires the real pinned VTracer output.
"""
from pathlib import Path
import copy, hashlib, json, re, xml.etree.ElementTree as ET
from PIL import Image

ROOT=Path(__file__).resolve().parents[5]
PRIVATE=ROOT/'.liu-visual-private/correct_source_typography/v4'
OUT=Path(__file__).resolve().parent
NS='http://www.w3.org/2000/svg'
ET.register_namespace('',NS)
source=PRIVATE/'lettering-generated-01.png'
traced=PRIVATE/'lettering-traced-01.svg'
tree=ET.parse(traced)
paths=[p for p in tree.getroot() if p.tag.endswith('path')]
alpha=Image.open(source).getchannel('A').point(lambda n:255 if n>=128 else 0)
boxes={'brand':alpha.crop((0,0,650,345)).getbbox(),
       'headline':alpha.crop((650,345,1536,1024)).getbbox()}
b=boxes['headline'];boxes['headline']=(b[0]+650,b[1]+345,b[2]+650,b[3]+345)
roles={'brand':[],'headline':[]}
empty=0
for p in paths:
    if not p.get('d','').strip():empty+=1;continue
    m=re.fullmatch(r'translate\(([-.\d]+),([-.\d]+)\)',p.get('transform',''))
    if not m:raise ValueError('UNEXPECTED_UPSTREAM_TRANSFORM')
    role='brand' if float(m[2])<345 else 'headline'
    node=copy.deepcopy(p);node.set('fill','#F3EEE3');roles[role].append(node)

placements={'brand':{'x':88,'y':76,'width':285},'headline':{'x':884,'y':280,'width':520}}
def svgroot(w,h):return ET.Element(f'{{{NS}}}svg',{'width':str(w),'height':str(h),'viewBox':f'0 0 {w} {h}'})
def save(name,element):
    p=OUT/name
    if p.exists():raise FileExistsError(p)
    p.write_text(ET.tostring(element,encoding='unicode')+'\n',encoding='utf-8',newline='\n')
    return {'path':str(p.relative_to(ROOT)).replace('\\','/'),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
overlay=svgroot(1536,1024)
exports={}
for role in ['brand','headline']:
    x0,y0,x1,y1=boxes[role];w,h=x1-x0,y1-y0
    asset=svgroot(w,h);grp=ET.SubElement(asset,f'{{{NS}}}g',{'transform':f'translate({-x0},{-y0})'})
    for p in roles[role]:grp.append(copy.deepcopy(p))
    exports[role]=save(role+'.svg',asset)
    place=placements[role];scale=place['width']/w
    place.update(height=round(h*scale,6),scale=scale)
    positioned=ET.SubElement(overlay,f'{{{NS}}}g',{'id':role,'transform':f'translate({place["x"]},{place["y"]}) scale({scale}) translate({-x0},{-y0})'})
    for p in roles[role]:positioned.append(copy.deepcopy(p))
exports['overlay']=save('overlay.svg',overlay)
provenance={'source':{'path':str(source.relative_to(ROOT)).replace('\\','/'),'sha256':hashlib.sha256(source.read_bytes()).hexdigest()},
            'trace':{'path':str(traced.relative_to(ROOT)).replace('\\','/'),'sha256':hashlib.sha256(traced.read_bytes()).hexdigest()},
            'source_alpha_threshold':128,'source_glyph_boxes':boxes,'placements':placements,'assets':exports,
            'paths':{k:len(v) for k,v in roles.items()},'empty_upstream_paths_omitted':empty,
            'brand':'茶作','copy':'一杯茶，慢下来','dimensions':[1536,1024],
            'letterform_origin':'ONE_BUILT_IN_IMAGEGEN_TRANSPARENT_LETTERING_OPERATION',
            'font_software_used':None,'backend_model':'NOT_EXPOSED',
            'upstream_vectorizer':'VTracer Python0.6.15 / SVG generator0.6.12 MIT',
            'adaptation':'alpha threshold; omit empty paths; separate wordmark/headline; one proportional placement per role; ivory vector fill',
            'photography_generation':False,'aesthetic_pass_claimed':False}
(OUT/'LETTERING_PROVENANCE.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(provenance,ensure_ascii=False))
