"""Thin color/alpha-region adaptation around unmodified VTracer0.6.15.
Only visible guide pixels are traced; no invented hidden strokes or bitmap SVG embeds.
"""
import sys, json, hashlib, pathlib, xml.etree.ElementTree as ET, importlib.metadata
BASE=pathlib.Path(__file__).resolve().parent
DEP=pathlib.Path('C:/Users/Administrator/OneDrive/文档/足球/shenmei-vpd-codex-20261003/.liu-visual-private/dependencies/vtracer_0_6_15_cp312')
sys.path.insert(0,str(DEP/'site-packages'))
import vtracer
VERSION=importlib.metadata.version('vtracer')
if VERSION!='0.6.15': raise RuntimeError('Wrong VTracer version: '+VERSION)
e=json.loads((BASE/'TRACE_INPUT_EVIDENCE.json').read_text(encoding='utf-8'))
PARAMS=dict(colormode='binary',mode='spline',filter_speckle=12,corner_threshold=60,length_threshold=4.0,max_iterations=10,splice_threshold=45,path_precision=2)
for name in ['CREAM','ORANGE']:
    vtracer.convert_image_to_svg_py(str(BASE/(name+'_TRACE_INPUT.png')),str(BASE/(name+'_TRACE.svg')),**PARAMS)
def traced_paths(name,color):
    root=ET.parse(BASE/(name+'_TRACE.svg')).getroot()
    out=[]
    for p in root.iter():
        if p.tag.rsplit('}',1)[-1]!='path':continue
        at={'d':p.attrib['d'],'fill':color}
        if 'transform' in p.attrib:at['transform']=p.attrib['transform']
        out.append('<path '+' '.join(k+'="'+v+'"' for k,v in at.items())+'/>')
    return ''.join(out),len(out)
c,cn=traced_paths('CREAM',e['cream']['flat_vector_color'])
o,on=traced_paths('ORANGE',e['orange']['flat_vector_color'])
svg='<svg xmlns="http://www.w3.org/2000/svg" width="1086" height="1448" viewBox="0 0 1086 1448"><title>Image guide S3 visible wordmark reconstruction</title><g id="GUIDE_CREAM_WORDMARK">'+c+'</g><g id="GUIDE_ORANGE_VISIBLE_RIBBON">'+o+'</g></svg>\n'
if '<image' in svg or 'data:image' in svg:raise RuntimeError('Bitmap embeds forbidden')
if len(svg.encode('utf-8'))>42000:raise RuntimeError('Trace exceeds42k byte target; assess documented spline simplification before Figma insertion')
target=BASE/'IMAGE_GUIDE_S3_WORDMARK_TRACE.svg'
target.write_text(svg,encoding='utf-8',newline='\n')
notice=(DEP/'source/vtracer-0.6.15/LICENSE').read_text(encoding='utf-8')
(BASE/'LICENSE-VTracer.txt').write_text(notice,encoding='utf-8')
receipt={'status':'VECTOR_RECONSTRUCTION_PENDING_PIXEL_REVIEW','source':e['source'],'source_sha256':e['source_sha256'],'source_canvas':[1086,1448],'trace_scope':'Only native guide main 刘先生 cream silhouettes and visible orange ribbon in ROI202/465/803x317. No helper text or seal traced.','upstream':{'tool':'VTracer','version':VERSION,'module':vtracer.__file__,'license':'MIT','license_source':str(DEP/'source/vtracer-0.6.15/LICENSE'),'license_sha256':hashlib.sha256(notice.encode()).hexdigest(),'modified':False},'thin_adapter':'prepare-trace-inputs.cjs + trace-guide.py; alpha/color gate and connected-component dust rejection only','parameters':PARAMS,'cream':e['cream'],'orange':e['orange'],'layers':{'cream_paths':cn,'orange_visible_paths':on},'output':str(target),'output_bytes':len(svg.encode('utf-8')),'output_sha256':hashlib.sha256(svg.encode('utf-8')).hexdigest(),'target_canvas_conversion':{'matrix':[160/181,0,0,160/181,0,0],'canvas':[960,1280]},'limitations':['Flattened each sampled foreground class to its actual selected-pixel median RGB; source gradients and low-alpha edge haze are not preserved.','Traced only visible orange fragments; no hidden portions beneath cream were inferred. Cream remains source-visible geometry, so occlusion is preserved in rendered output.','Connected color speckles below the recorded area gates and VTracer speckle filter are omitted; no claim of perfect pixel identity.','Vector curves are recovered from generated raster; these are not hand-authored original glyphs or font outlines.','No Figma, business-state, upstream package or original guide writes. Independent cold pixel review remains required.']}
(BASE/'PROVENANCE.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:receipt[k] for k in ['status','layers','output_bytes','output_sha256','parameters']},ensure_ascii=False))
