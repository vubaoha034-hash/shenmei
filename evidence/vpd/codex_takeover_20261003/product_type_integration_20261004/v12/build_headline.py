"""V12: a fresh-leaf contour is the right descending stroke of 茶's 木.

No new candidate selection, fonts, image generation, photography edits or state
writes. All dependencies and seven immutable inputs are checked before output.
--verify-only reproduces SVG, alpha evidence and full poster preview in memory;
--emit-preview emits images as base64 without writing any raster file.
"""
from pathlib import Path
import argparse, base64, copy, hashlib, io, json, os, subprocess, sys
import xml.etree.ElementTree as ET

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[4]
RUNTIME = Path('C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies')
FONTTOOLS_SITE = 'C:/Users/Administrator/AppData/Local/hermes/hermes-agent/venv/Lib/site-packages'
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('',NS)
COPY = '一杯茶，慢下来'
TEA_INDICES = {1,4,7,9,10}
FIXED = {
    'headline':('evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v11/headline.svg','67db67ebbdf1d61176efd826e3ec2b737a1be2fc0c39ddfae6bb7fdb8b4198ee'),
    'brand':('evidence/vpd/codex_takeover_20261003/product_type_integration_20261004/v11/brand.svg','dd8e9e899393dc36eb3f5b1652bdbb740787d41a108ea6aa1eae05cb1368b1ff'),
    'S':('.liu-visual-private/source_recovery_20261003/photography-local-reconstruction-final.png','7fd7777fed21100cb6b47bc305701476054263565e73246ac469d065aa080618'),
    'V11_full':('.liu-visual-private/correct_source_typography/v11/poster.png','4f112b3596da33f35f2fa81f1f13858e9043b070abc8bf4f275c36895564e5fc'),
    'P':('.liu-visual-private/product-type-integration-20261004/P-approved-typography.png','57c21466512a79cbb25c75db1d6a1748b595c3bc2d00c85ba51615557f74f925'),
    'R':('.liu-visual-private/product-type-integration-20261004/R-current-reference.jpg','87a28f5cd4b5d15b01e6536206127c357043a904b3c0dab3bfa0c50080782167'),
    'SHANYEJI':('.liu-visual-private/product-type-integration-20261004/SHANYEJI-approved-historical.jpg','9a29fbdc7dd908017924bed270e8dfe18351519eed3fa7bc7001789f2a383414')}

# One continuous character junction: stem/crossbar of 木, then its descending
# right stroke. The latter adapts the real leaf's narrow base, broad belly and
# long pointed tip. Their filled contours overlap at the original 木 junction.
WOOD_CORE = (
    'M614.8 480.7C617.4 480.8 620.1 481.4 622 482.9'
    'C623 484 623.2 486.4 623.1 489.9'
    'C623 491.1 624.5 491.4 626 491.1'
    'C631.2 490.7 634.2 490.7 637.4 493'
    'C636 494.8 633.2 495.6 630.4 495.8L624.2 497'
    'C623.6 497.1 623 497.8 623 499.3L623 520.8'
    'C623 524.3 622.1 527.1 620.6 528.8'
    'C617.9 529.6 613.8 527.6 609 522.6'
    'C607.9 521.5 608.4 521.3 610.1 520.4'
    'C612.8 519.2 614 516.5 614.4 511.6L615.4 500.1'
    'C615.4 499 614.3 498.5 612.9 498.9'
    'C607.8 500.2 605 501.8 602.1 499.8'
    'C600.6 498.8 599.4 497.2 599 495.8L613.9 493.5'
    'C614.6 493.4 615 492.8 615 491.9'
    'C615.1 487.4 615.3 484 614.8 480.7Z')
LEAF_RIGHT_STROKE = (
    'M620.8 492.6C628.4 491.6 634 494.3 640.3 496.7'
    'C653.6 493.8 665.5 495.8 676.8 503.1'
    'C687.7 510.3 695.5 522.5 707 530.8'
    'C690.9 525.7 679.4 527.9 665.3 523.6'
    'C650.3 519.1 637.9 508.3 627.3 500.1'
    'C623.8 497.4 621.5 496.6 620.8 495.3'
    'C620.3 494.5 620.1 493.4 620.8 492.6Z')

def digest(data):return hashlib.sha256(data).hexdigest()

def preflight(verify_only):
    paths, refs = {}, {}
    for role,(relative,expected) in FIXED.items():
        path = ROOT/relative
        raw = path.read_bytes()
        assert digest(raw)==expected, 'FIXED_INPUT_SHA_MISMATCH:'+role
        paths[role]=path
        refs[role]={'path':relative,'sha256':expected,'bytes':len(raw)}
    import PIL
    from PIL import Image, ImageChops
    sys.path.append(FONTTOOLS_SITE)
    import fontTools
    from fontTools.pens.boundsPen import BoundsPen
    from fontTools.svgLib.path import parse_path
    assert sys.version_info[:3]==(3,12,14), 'PYTHON_VERSION_CHANGED'
    assert fontTools.__version__=='4.63.0' and PIL.__version__=='12.3.0', 'DEPENDENCY_VERSION_CHANGED'
    node = RUNTIME/'node/bin/node.exe'
    sharp = RUNTIME/'node/node_modules/sharp'
    assert node.is_file() and sharp.is_dir(), 'BUNDLED_NODE_SHARP_MISSING'
    env = {k:v for k,v in os.environ.items() if k.upper() not in {'NODE_OPTIONS','NODE_PATH'}}
    code = 'const s=require('+json.dumps(sharp.as_posix())+');process.stdout.write(JSON.stringify({node:process.version,sharp:s.versions.sharp,rsvg:s.versions.rsvg}));'
    versions=json.loads(subprocess.run([str(node),'-e',code],capture_output=True,text=True,env=env,check=True).stdout)
    assert versions=={'node':'v24.19.0','sharp':'0.35.4','rsvg':'2.62.91'}, 'RASTER_DEPENDENCY_VERSION_CHANGED'
    output_paths=[OUT/'headline.svg',OUT/'PROVENANCE.json']
    if not verify_only:
        assert all(not p.exists() for p in output_paths), 'V12_OUTPUT_EXISTS_NO_OVERWRITE'
    return paths,refs,Image,ImageChops,BoundsPen,parse_path,node,sharp,env,{'python':sys.version,'python_executable':sys.executable,'Pillow':PIL.__version__,'fontTools':fontTools.__version__,'fontTools_site':FONTTOOLS_SITE,**versions}

def render(svg,node,sharp,env):
    code = 'const sharp=require('+json.dumps(sharp.as_posix())+');let a=[];process.stdin.on("data",b=>a.push(b));process.stdin.on("end",async()=>{process.stdout.write(await sharp(Buffer.concat(a)).ensureAlpha().png().toBuffer());});'
    return subprocess.run([str(node),'-e',code],input=svg,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env,check=True).stdout

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--verify-only',action='store_true')
    parser.add_argument('--emit-preview',action='store_true')
    args=parser.parse_args()
    paths,refs,Image,ImageChops,BoundsPen,parse_path,node,sharp,env,deps=preflight(args.verify_only)
    original=ET.parse(paths['headline']).getroot()
    assert original.attrib=={'width':'805','height':'127','viewBox':'343 405 805 127','fill':'none'}
    source_paths=list(original.iter('{'+NS+'}path'))
    assert len(source_paths)==19 and not list(original.iter('{'+NS+'}text'))
    result=copy.deepcopy(original)
    result.find('{'+NS+'}desc').text='V12: real fresh-leaf silhouette becomes the connected right descending stroke of 茶; other fourteen character paths remain identical to V11.'
    result.find('{'+NS+'}g').set('id','V12-headline')
    output_paths=list(result.iter('{'+NS+'}path'))
    output_paths[6].set('d',WOOD_CORE)
    output_paths[8].set('d',LEAF_RIGHT_STROKE)
    rows=[]
    for index,(source,target) in enumerate(zip(source_paths,output_paths),1):
        if index not in TEA_INDICES:assert target.attrib==source.attrib,'NON_TEA_PATH_CHANGED'
        pen=BoundsPen(None);parse_path(target.get('d'),pen)
        rows.append({'source_path_index':index,'character':target.get('data-character'),'d_sha256':digest(target.get('d').encode()),'attribute_exact_to_V11':target.attrib==source.attrib,'actual_global_curve_bbox':list(pen.bounds)})
    assert [r['source_path_index'] for r in rows if not r['attribute_exact_to_V11']]==[7,9]
    svg=(ET.tostring(result,encoding='unicode')+'\n').encode('utf-8')
    raster=render(svg,node,sharp,env)
    im=Image.open(io.BytesIO(raster)).convert('RGBA')
    assert im.size==(805,127)
    alpha=im.getchannel('A');b=alpha.getbbox()
    global_box=[b[0]+343,b[1]+405,b[2]+343,b[3]+405]
    assert global_box[0]>=300 and global_box[1]>=380 and global_box[2]<=1350 and global_box[3]<=550
    tea=copy.deepcopy(result);tg=tea.find('{'+NS+'}g')
    for child in list(tg):
        if int(child.get('id').rsplit('-',1)[-1]) not in TEA_INDICES:tg.remove(child)
    tea_rgba=Image.open(io.BytesIO(render(ET.tostring(tea),node,sharp,env))).convert('RGBA')
    tb=tea_rgba.getchannel('A').getbbox();tea_box=[tb[0]+343,tb[1]+405,tb[2]+343,tb[3]+405]
    assert tea_box[0]>=560 and tea_box[1]>=418 and tea_box[2]<=710 and tea_box[3]<=548
    core_alpha=[]
    for keep in (7,9):
        single=copy.deepcopy(result);g=single.find('{'+NS+'}g')
        for child in list(g):
            if int(child.get('id').rsplit('-',1)[-1])!=keep:g.remove(child)
        core_alpha.append(Image.open(io.BytesIO(render(ET.tostring(single),node,sharp,env))).convert('RGBA').getchannel('A'))
    intersection=ImageChops.darker(*core_alpha)
    shared_pixels=sum(intersection.histogram()[128:])
    assert shared_pixels>0,'LEAF_STROKE_NOT_CONNECTED_TO_CHARACTER_CORE'
    source_raster=Image.open(io.BytesIO(render(paths['headline'].read_bytes(),node,sharp,env))).convert('RGBA')
    source_diff=ImageChops.difference(source_raster,im).getbbox(alpha_only=False)
    changes=[source_diff[0]+343,source_diff[1]+405,source_diff[2]+343,source_diff[3]+405]
    assert changes[0]>=560 and changes[1]>=418 and changes[2]<=710 and changes[3]<=548
    frozen=Image.open(paths['S']).convert('RGBA')
    base=Image.open(paths['V11_full']).convert('RGBA')
    assert base.size==frozen.size==(1536,1024)
    # Exact V11 brand and every pixel outside the headline asset are retained.
    preview=base.copy()
    preview.paste(frozen.crop((343,405,1148,532)),(343,405))
    preview.alpha_composite(im,(343,405))
    assert preview.crop((112,104,388,240)).tobytes()==base.crop((112,104,388,240)).tobytes()
    assert preview.crop((0,550,1536,1024)).tobytes()==base.crop((0,550,1536,1024)).tobytes()
    full_buffer=io.BytesIO();preview.convert('RGB').save(full_buffer,format='PNG')
    poster=full_buffer.getvalue()
    for path,data in ((OUT/'headline.svg',svg),):
        if args.verify_only and path.exists():assert path.read_bytes()==data,'SAVED_V12_DIFFERS_FROM_ZERO_WRITE_REPLAY'
    proof={'formal_version':12,'exact_copy':COPY,'asset_role':'headline_only','source':refs['headline'],
        'output':{'path':(OUT/'headline.svg').relative_to(ROOT).as_posix(),'sha256':digest(svg),'bytes':len(svg)},
        'single_mechanism':'REAL_FRESH_LEAF_CONTOUR_IS_THE_CONNECTED_RIGHT_DESCENDING_STROKE_OF_TEA_WOOD_RADICAL',
        'contour_basis':'Manual silhouette adaptation from the S foreground fresh leaf: tapered base, broad central blade, long right-down tip. It replaces the old detached right dot at path 9 and shares the existing 木 core at path 7. No independent leaf illustration, vein, texture fill, steam, or connector is added.',
        'changed_indices':[7,9],'permitted_tea_indices':sorted(TEA_INDICES),'non_tea_paths_exactly_preserved':14,'unchanged_tea_indices':[1,4,10],
        'path_count':19,'path_groups_retained':True,'path_details':rows,'shared_opaque_core_and_right_stroke_pixels':shared_pixels,
        'svg_dimensions':[805,127],'viewBox':[343,405,805,127],'import_position_global':[343,405],
        'actual_svg_global_curve_bbox':[min(r['actual_global_curve_bbox'][0] for r in rows),min(r['actual_global_curve_bbox'][1] for r in rows),max(r['actual_global_curve_bbox'][2] for r in rows),max(r['actual_global_curve_bbox'][3] for r in rows)],
        'raster_alpha_bbox_global_exclusive':global_box,'tea_raster_alpha_bbox_global_exclusive':tea_box,'actual_changed_pixels_global_exclusive':changes,
        'all_nontransparent_pixels_in_required_background_region':True,'new_tea_ink_in_tighter_ROI':True,
        'dependencies':deps,'fixed_source_and_references':refs,'actual_view_image_inputs':['S','V11_full','P','R','SHANYEJI'],
        'reference_roles':{'P':'Typography gesture only; photography excluded.','R':'Upper advertisement only.','SHANYEJI':'Historical approved example of form carrying message; its assets and brand are not copied.','S':'Real fresh-leaf silhouette and frozen photo.','V11_full':'Fixed complete composition and exact brand pixels.'},
        'inspection_rasters':{'headline_png_sha256':digest(raster),'complete_preview_png_sha256':digest(poster),'complete_preview_size':[1536,1024],'complete_preview_method':'Exact V11 full image with old headline ROI restored from frozen S, then V12 vector raster at unchanged placement; brand pixel block remains byte-for-byte identical.'},
        'copy_verification':{'title':COPY,'source_trace_method':'Fourteen non-tea original path attributes and all three unchanged tea paths verified exactly; only 茶 core and right descending stroke are redesigned.','actual_full_pixel_inspection':'Pending maker inspection of emitted full image.','limitation':'The leaf shape is adapted to an ivory character stroke, not photographic material. Path continuity and metadata cannot prove intuitive visual integration or character recognition; independent cold review of the complete Figma export remains required.'},
        'frozen_photography_changed':False,'brand_changed':False,'brand_expected_position':[112,104],
        'imagegen_calls':0,'Figma_writes':0,'business_state_writes':0,'git_operations':0,'aesthetic_pass_claimed':False,
        'script':{'path':Path(__file__).relative_to(ROOT).as_posix(),'sha256':digest(Path(__file__).read_bytes())}}
    if not args.verify_only:
        # No write occurs until every input, dependency, contour and pixel check passes.
        assert not (OUT/'headline.svg').exists() and not (OUT/'PROVENANCE.json').exists()
        (OUT/'headline.svg').write_bytes(svg)
        (OUT/'PROVENANCE.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    response={'mode':'zero_write_verification' if args.verify_only else 'unique_asset_written','writes':0 if args.verify_only else 2,'svg_sha256':digest(svg),'global_bbox':global_box,'tea_bbox':tea_box,'changed_pixel_bbox':changes,'shared_core_leaf_opaque_pixels':shared_pixels,'output':str(OUT/'headline.svg'),'provenance':str(OUT/'PROVENANCE.json')}
    if args.emit_preview:
        response['images']=[{'role':'actual_headline','mime':'image/png','data':base64.b64encode(raster).decode()}]
        display=preview.convert('RGB');buffer=io.BytesIO();display.save(buffer,format='JPEG',quality=82)
        response['images'].append({'role':'complete_1536x1024_with_exact_V11_brand','mime':'image/jpeg','data':base64.b64encode(buffer.getvalue()).decode()})
    print(json.dumps(response,ensure_ascii=False))

if __name__=='__main__':main()
