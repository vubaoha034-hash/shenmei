"""Read source pixels to derive a narrow editable SVG mask; never retouch a photo."""
import argparse, hashlib, json, pathlib
from PIL import Image
SOURCE_SHA = 'e7af9c9e88ff9dd38357a570305c4b5d40e98678d14c174957d4bdf2e7bdfd29'
REGIONS = [('brand',98,84,403,223),('latin',110,238,370,271),('subline',110,289,370,313),('hero',895,123,1474,354),('middle',924,391,1013,489),('english1',1343,86,1488,109),('english2',1343,111,1492,133),('footer1',1343,876,1434,900),('footer2',1343,904,1488,925)]
EXPLICIT = [('old_leaf',230,164,271,220),('left_rule',113,299,145,304),('right_rule',335,299,369,304),('top_rule',1345,154,1391,158),('bottom_rule',1345,946,1391,951)]
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',required=True);ap.add_argument('--out-dir',required=True);a=ap.parse_args()
    src=pathlib.Path(a.source);assert hashlib.sha256(src.read_bytes()).hexdigest()==SOURCE_SHA
    im=Image.open(src).convert('RGB');assert im.size==(1536,1024);px=im.load();core=set();counts={}
    for name,x0,y0,x1,y1 in REGIONS:
        before=len(core)
        for y in range(y0,y1):
            for x in range(x0,x1):
                rr,g,b=px[x,y]
                if rr>150 and g>150 and b>115 and g<=rr+6 and abs(rr-g)<30 and g-b<55:core.add((x,y))
        counts[name]=len(core)-before
    for _,x0,y0,x1,y1 in EXPLICIT:
        core.update((x,y) for y in range(y0,y1) for x in range(x0,x1))
    def dilate(points,radius):
        return {(x+dx,y+dy) for x,y in points for dx in range(-radius,radius+1) for dy in range(-radius,radius+1) if dx*dx+dy*dy<=radius*radius and 0<=x+dx<1536 and 0<=y+dy<1024}
    full=dilate(core,3);middle=dilate(core,2);inner=dilate(core,1)
    def runs(points):
        rows={}
        for x,y in points:rows.setdefault(y,[]).append(x)
        result=[]
        for y in sorted(rows):
            xs=sorted(rows[y]);start=last=xs[0]
            for x in xs[1:]:
                if x==last+1:last=x;continue
                result.append([start,y,last+1,y+1]);start=last=x
            result.append([start,y,last+1,y+1])
        return result
    full_runs=runs(full)
    def path(points):return ''.join('M%d %dh%dv1H%dz'%(x,y,x1-x,x) for x,y,x1,_ in runs(points))
    layers=[(full,.35),(middle,.6),(inner,.85),(core,1)]
    svg='<svg xmlns="http://www.w3.org/2000/svg" width="1536" height="1024" viewBox="0 0 1536 1024">'+''.join('<path fill="white" fill-opacity="%s" d="%s"/>'%(alpha,path(points)) for points,alpha in layers)+'</svg>'
    out=pathlib.Path(a.out_dir);out.mkdir(parents=True,exist_ok=True);(out/'text-repair-mask.svg').write_text(svg,encoding='utf-8',newline='\n')
    data={'source_sha256':SOURCE_SHA,'dimensions':[1536,1024],'kind':'BRIGHT_NEUTRAL_GLYPH_CORE_PLUS_3PX_BOUNDARY_AND_DECLARED_LEAF_RULES','regions':[list(v) for v in REGIONS],'explicit_regions':[list(v) for v in EXPLICIT],'core_pixels':len(core),'mask_pixels':len(full),'mask_percent':round(len(full)/1572864*100,4),'neutral_core_counts':counts,'allowed_pixel_runs':full_runs,'hidden_background_is_original':False,'subject_regions_untouched':True,'mask_svg_sha256':hashlib.sha256((out/'text-repair-mask.svg').read_bytes()).hexdigest()}
    (out/'MASK_DEFINITION.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps({k:data[k] for k in ['mask_pixels','mask_percent','core_pixels','mask_svg_sha256']}))
if __name__=='__main__':main()
