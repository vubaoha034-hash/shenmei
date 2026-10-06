import pathlib,json,sys,re,xml.etree.ElementTree as ET
from PIL import Image
import numpy as np
root=pathlib.Path.cwd();b=root/'.liu-visual-private/s7_outline_implementation';sys.path[:0]=[str(root/'.liu-visual-private/dependencies/skia_pathops_0_9_2_abi3/site-packages'),str(b)]
from vector_adapter import parse_svg_path,source_matrix
solid=np.array(Image.open(b/'S7_SOLID_ALPHA_TECHNICAL.png').getchannel('A'))[420:612,216:800]>=128;tier=np.array(Image.open(b/'TIER_INDEX_FIELD_TECHNICAL.png'));rows=[]
for t in range(1,6):
 paths=[]
 for node in ET.parse(b/f'TIER_{t}_TRACE.svg').getroot().iter():
  if node.tag.rsplit('}',1)[-1]=='path':paths.append(parse_svg_path(node.attrib['d'],source_matrix(node.attrib.get('transform'))))
 rows.append({'tier':t,'mask_pixels_within_solid_alpha128':int(((tier==t)&solid).sum()),'trace_total_path_count':len(paths),'zero_area_path_count':sum(abs(p.area)<1e-6 for p in paths),'sum_trace_path_areas':sum(abs(float(p.area)) for p in paths)})
fail={'schema':'s7-technical-falsification/v1','status':'STOPPED_DEEP_REQUIRED','actual_records':rows,'cause':'VTracer polygon emits singleton paths M0,0 Z and simplifies other tiny cells. Mutually exclusive masks may produce slightly overlapping approximate polygons. No final texture retention/alpha correctness claim.','tier_overlap_evidence':'PROVENANCE.json/tier_mutual_overlap_area','reproducer':'build-wordmark.py + fixed5input/output traces + frozen spec','no_new_parameter_search':True,'no_additional_trace_calls':True,'aesthetic_verdict':None}
(b/'TECHNICAL_FAILURE.json').write_text(json.dumps(fail,indent=2)+'\n');p=b/'TECHNICAL_ATTEMPTS.json';j=json.loads(p.read_text());j['attempt2']='completed technical SVG but refuted by mask/trace pixel-area and tier-disjointness checks; STOPPED_DEEP_REQUIRED';j['failures'].append({'attempt':2,'classification':'REFUTED_TEXTURE_RETENTION','details':'TECHNICAL_FAILURE.json','action':'Return raw5traces to DEEP; no automatic retry.'});p.write_text(json.dumps(j,indent=2)+'\n');print(json.dumps(rows))
