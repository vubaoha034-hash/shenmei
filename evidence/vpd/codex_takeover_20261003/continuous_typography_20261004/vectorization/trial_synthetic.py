"""One non-artwork binary geometric fixture, one conversion; no production image."""
from pathlib import Path
import hashlib, importlib.metadata, json, os, platform, sys, time, xml.etree.ElementTree as ET
from PIL import Image, ImageDraw
from vectorize_mask import vectorize, PARAMETERS, DEPENDENCY

ROOT=Path(__file__).resolve().parent
source=ROOT/'synthetic_ring_triangle.png'; output=ROOT/'synthetic_ring_triangle.svg'
if source.exists() or output.exists(): raise FileExistsError('trial output already exists')
image=Image.new('RGB',(96,64),'white'); draw=ImageDraw.Draw(image)
draw.rectangle((8,8,38,52),fill='black'); draw.rectangle((15,15,31,42),fill='white')
draw.polygon([(53,10),(88,52),(50,52)],fill='black')
image.save(source)
started=time.perf_counter(); svg=vectorize(source,output); elapsed=time.perf_counter()-started
root=ET.fromstring(svg); paths=root.findall('.//{http://www.w3.org/2000/svg}path')
version=importlib.metadata.version('vtracer')
record={'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'CODEX_THREAD_ID':os.environ.get('CODEX_THREAD_ID'),
        'python':sys.version,'executable':sys.executable,'platform':platform.platform(),'vtracer_distribution_version':version,
        'vtracer_module_path':str(__import__('vtracer').__file__),'dependency_directory':str(DEPENDENCY),
        'pillow_version':importlib.metadata.version('Pillow'),'input_role':'non-artwork synthetic geometry: ring with hole plus triangle',
        'input':str(source),'output':str(output),'size':[96,64],'parameters':PARAMETERS,'elapsed_seconds':elapsed,
        'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'svg_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
        'svg_bytes':output.stat().st_size,'svg_generator_label':'visioncortex VTracer 0.6.12',
        'path_count':len(paths),'path_move_counts':[p.get('d','').count('M') for p in paths],
        'cubic_command_present':any('C' in p.get('d','') for p in paths),
        'embedded_image_count':len(root.findall('.//{http://www.w3.org/2000/svg}image')),
        'text_element_count':len(root.findall('.//{http://www.w3.org/2000/svg}text')),
        'svg_root_attributes':root.attrib,
        'not_tested':['production letter fidelity','Figma import/edit','alpha-mask mode','SVG rerasterization','aesthetic benefit']}
assert record['path_count']>=2 and record['embedded_image_count']==0 and record['text_element_count']==0
(ROOT/'TRIAL_RESULT.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(record,ensure_ascii=False,indent=2))
