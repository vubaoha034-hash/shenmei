"""One bounded V11 adaptation of the existing nineteen V10 lettering paths.

Only headline.svg and PROVENANCE.json are production outputs. The optional
temporary PNG is for actual pixel inspection, never a second artwork candidate.
FontTools reads curves, not fonts; Sharp rasterizes them without generation.
"""
from pathlib import Path
import copy, hashlib, io, json, math, os, subprocess, sys, tempfile
import xml.etree.ElementTree as ET
from PIL import Image

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[4]
SOURCE = OUT.parent / 'v10/headline.svg'
FONTTOOLS_SITE = 'C:/Users/Administrator/AppData/Local/hermes/hermes-agent/venv/Lib/site-packages'
RUNTIME = Path('C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies')
sys.path.append(FONTTOOLS_SITE)
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.svgLib.path import parse_path
import fontTools
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
COPY = '一杯茶，慢下来'
SOURCE_SHA = '6c2030441b42775b68d442310c0be93434fb4991625d65215ffad67f6ec06fe2'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def ref(p):
    return {'path': p.relative_to(ROOT).as_posix(), 'sha256': sha(p), 'bytes': p.stat().st_size}

def bounds(d):
    pen = BoundsPen(None)
    parse_path(d, pen)
    return list(pen.bounds)

def record(d):
    pen = RecordingPen()
    parse_path(d, pen)
    return pen.value

def rotate(x, y, cx, cy, degrees):
    a = math.radians(degrees)
    dx, dy = x-cx, y-cy
    return cx+dx*math.cos(a)-dy*math.sin(a), cy+dx*math.sin(a)+dy*math.cos(a)

# Original path indices belong to characters, not invented decorative strokes.
GROUPS = [
    ('一', [5]), ('杯', [2,3,6]), ('茶', [1,4,7,9,10]),
    ('，', [8]), ('慢', [11,12,15,16,19]), ('下', [14,18]), ('来', [13,17])
]

def sculpt(char, index, x, y):
    if char == '一':
        # Preserve its rising brush taper; a small central lift bends the stroke itself.
        t = (x-39.5)/38.1
        return 345+(x-1.48485)*1.08, 443+y*1.07-4.4*max(0,1-t*t)
    if char == '杯':
        xx = 435+(x-81.8333)*1.10
        yy = 422+(y-7.656)*1.10
        # Ease the long lower stems upward near the cup centre without changing anatomy.
        yy -= 3.0*max(0,(y-48)/41)*max(0,1-((x-136)/54)**2)
        return rotate(xx,yy,494,470,-1.3)
    if char == '茶':
        xx = 572+(x-192.297)*1.12
        yy = 428+(y-1.0320906885)*1.10
        # The central stem and low right strokes carry the descending rim contour.
        if index in (7,9,10):
            yy += 2.7*max(0,(y-48)/45)*(x-216)/53
        return rotate(xx,yy,626,477,1.8)
    if char == '，':
        return 711+(x-299.409)*.94, 493+(y-60.209480632)*.94
    if char == '慢':
        xx = 805+(x-401.485)*1.10
    elif char == '下':
        xx = 953+(x-516.208)*1.10
    else:
        xx = 1052+(x-590.265)*1.10
    yy = 401+y*1.075+0.067*(xx-805)
    # The long right exit of 慢 and the final 来 sweep inherit a modest leaf direction.
    if index == 19:
        yy += 2.6*max(0,(x-477)/40)*max(0,(y-72)/29)
    if char == '来' and index == 13:
        yy += 2.0*max(0,(x-634)/42)*max(0,(y-58)/26)
    return xx,yy

def transformed(d, char, index):
    source = record(d)
    parts = []
    commands = {'moveTo':'M','lineTo':'L','curveTo':'C','qCurveTo':'Q','closePath':'Z','endPath':''}
    for command, points in source:
        mapped = tuple(tuple(round(v,6) for v in sculpt(char,index,*p)) for p in points)
        parts.append(commands[command]+' '.join(format(v,'.6f').rstrip('0').rstrip('.') for p in mapped for v in p))
    result = ''.join(parts)
    assert [x[0] for x in record(result)] == [x[0] for x in source]
    return result

def raster(svg):
    node = RUNTIME/'node/bin/node.exe'
    sharp = RUNTIME/'node/node_modules/sharp'
    env = {k:v for k,v in os.environ.items() if k.upper() not in {'NODE_OPTIONS','NODE_PATH'}}
    code = 'const sharp=require('+json.dumps(sharp.as_posix())+');let a=[];process.stdin.on("data",b=>a.push(b));process.stdin.on("end",async()=>{process.stdout.write(await sharp(Buffer.concat(a)).ensureAlpha().png().toBuffer());});'
    return subprocess.run([str(node),'-e',code],input=svg,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True,env=env).stdout

def main():
    assert fontTools.__version__ == '4.63.0'
    assert sha(SOURCE) == SOURCE_SHA
    src = ET.parse(SOURCE).getroot()
    paths = list(src.iter('{'+NS+'}path'))
    assert len(paths) == 19
    assert not list(src.iter('{'+NS+'}text'))
    assert all(not n.get('transform') for n in paths)
    lookup = {i:c for c,indices in GROUPS for i in indices}
    rows, nodes = [], []
    for index, source in enumerate(paths,1):
        char = lookup[index]
        d = transformed(source.get('d'),char,index)
        node = ET.Element('{'+NS+'}path',{'id':f'v10-derived-{index:02d}','d':d,'fill':'#F5F2E6','data-character':char})
        nodes.append(node)
        rows.append({'source_path_index':index,'character':char,'source_d_sha256':hashlib.sha256(source.get('d').encode()).hexdigest(),'actual_global_bbox':bounds(d),'original_curve_command_topology_preserved':True})
    bbox = [min(r['actual_global_bbox'][0] for r in rows),min(r['actual_global_bbox'][1] for r in rows),max(r['actual_global_bbox'][2] for r in rows),max(r['actual_global_bbox'][3] for r in rows)]
    x0,y0 = math.floor(bbox[0])-2, math.floor(bbox[1])-2
    x1,y1 = math.ceil(bbox[2])+2, math.ceil(bbox[3])+2
    width,height = x1-x0,y1-y0
    svg = ET.Element('{'+NS+'}svg',{'width':str(width),'height':str(height),'viewBox':f'{x0} {y0} {width} {height}','fill':'none'})
    ET.SubElement(svg,'{'+NS+'}title').text = COPY
    ET.SubElement(svg,'{'+NS+'}desc').text = 'V11: existing V10 lettering contours adapted to the frozen cup rim and fresh-leaf direction; all nineteen source paths retained.'
    group = ET.SubElement(svg,'{'+NS+'}g',{'id':'V11-headline'})
    for n in nodes: group.append(n)
    target = OUT/'headline.svg'
    assert not target.exists(), 'V11_ALREADY_EXISTS_DO_NOT_OVERWRITE'
    target.write_text(ET.tostring(svg,encoding='unicode')+'\n',encoding='utf-8',newline='\n')
    png = raster(target.read_bytes())
    im = Image.open(io.BytesIO(png)).convert('RGBA')
    alpha = im.getchannel('A')
    actual = alpha.getbbox()
    global_pixels = [actual[0]+x0,actual[1]+y0,actual[2]+x0,actual[3]+y0]
    assert im.size == (width,height)
    assert global_pixels[0]>=300 and global_pixels[1]>=380 and global_pixels[2]<=1350 and global_pixels[3]<=550
    refs = {key:ref(ROOT/path) for key,path in {
        'P':'.liu-visual-private/product-type-integration-20261004/P-approved-typography.png',
        'R':'.liu-visual-private/product-type-integration-20261004/R-current-reference.jpg',
        'S':'.liu-visual-private/source_recovery_20261003/photography-local-reconstruction-final.png',
        'T':'.liu-visual-private/correct_source_typography/v10/poster.png'}.items()}
    proof = {'formal_version':11,'asset_role':'headline_only','exact_copy':COPY,'source':ref(SOURCE),'output':ref(target),
        'primary_change':'EXISTING_LETTERING_CONTOURS_RESPOND_TO_CUP_RIM_AND_FRESH_LEAF',
        'method':'Hand-directed local control-point deformation and character optical placement; source closed contours retained; no new typeface, icons, steam, connector, or image generation.',
        'source_character_path_groups':dict(GROUPS),'path_count':19,'path_details':rows,
        'actual_svg_global_curve_bbox':bbox,'svg_dimensions':[width,height],'import_position_global':[x0,y0],
        'raster_alpha_bbox_local_exclusive':list(actual),'raster_alpha_bbox_global_exclusive':global_pixels,
        'nonzero_alpha_pixel_count':sum(alpha.histogram()[1:]),'required_background_region_global':[300,380,1350,550],
        'all_nontransparent_pixels_within_required_region':True,'full_poster_canvas':[1536,1024],
        'frozen_photo_untouched':True,'brand_untouched':True,'brand_expected_position':[112,104],
        'references':refs,'actual_view_image_inputs':['P','R','S','T'],'reference_limits':{'P':'Typography gesture only; its photography is excluded.','R':'Only upper food advertisement considered.','S':'Frozen photography shape and placement.','T':'Existing V10 full composition.'},
        'dependencies':{'python':sys.version,'python_executable':sys.executable,'fontTools':fontTools.__version__,'fontTools_use':'SVG contours and exact Bezier bounds only; no fonts loaded','fonttools_site':FONTTOOLS_SITE,'rasterizer':'Existing bundled Sharp'},
        'copy_verification':{'title_metadata':COPY,'source_path_count_and_character_groups':'All nineteen original paths mapped to six Chinese characters and Chinese comma; all move/line/curve/close command topology retained.','rendered_visual_inspection':'PENDING_ACTUAL_VIEW_IMAGE','limitation':'Semantic title and contour provenance establish intended text; a vector shape cannot be proved readable by metadata. Independent cold pixel review remains required.'},
        'imagegen_calls':0,'Figma_writes':0,'business_state_writes':0,'git_operations':0,'aesthetic_pass_claimed':False}
    report = OUT/'PROVENANCE.json'
    report.write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    temp = Path(tempfile.mkdtemp(prefix='v11-headline-pixel-'))
    preview = temp/'headline.png'; preview.write_bytes(png)
    photo = Image.open(ROOT/'.liu-visual-private/source_recovery_20261003/photography-local-reconstruction-final.png').convert('RGBA')
    photo.alpha_composite(im,(x0,y0))
    composite = temp/'headline-on-frozen-photo.png'; photo.convert('RGB').save(composite)
    print(json.dumps({'headline':str(target),'provenance':str(report),'svg_bbox':bbox,'global_alpha_bbox':global_pixels,'placement':[x0,y0],'dimensions':[width,height],'preview':str(preview),'context_preview':str(composite)},ensure_ascii=False))

if __name__ == '__main__':
    main()
