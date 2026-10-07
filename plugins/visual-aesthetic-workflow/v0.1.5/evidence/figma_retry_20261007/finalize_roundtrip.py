from pathlib import Path
import json,hashlib,importlib.util
from PIL import Image
import numpy as np
p=Path(__file__).resolve().parent; prior=p.parent/'repair-v2'
h=lambda x:hashlib.sha256(x.read_bytes()).hexdigest()
assert h(p/'raw-4.jpeg')==h(p.parent/'delivery/original.jpg')
plan=json.loads((prior/'plan.json').read_text());old=json.loads((prior/'patches.json').read_text());mapping={'top':'raw-0.png','old_glyph_residue_cleanup':'raw-1.png','title':'raw-2.png','right':'raw-3.png','footer':'raw-5.png'}
patches=[];readbacks=[]
for item in old:
 rid=item['region_id'];f=p/mapping[rid];submitted=p/(rid+'.png');assert h(f)==h(submitted)
 patches.append(dict(region_id=rid,path=str(f),sha256=h(f),role='LOCAL_TEXT_OR_TEXTURE_CANDIDATE'))
 readbacks.append(dict(region_id=rid,figma_download_file=f.name,sha256=h(f),uploaded_original_bytes_identical=True))
(plan_path:=p/'roundtrip-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n');(p/'roundtrip-patches.json').write_text(json.dumps(patches,indent=2)+'\n')
spec=importlib.util.spec_from_file_location('exact',str(p.parents[1]/'.sites-checkout/scripts/exact_composite.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
prov,report=m.compose(str(p/'raw-4.jpeg'),str(p/'map-outside-figma-exact-final.png'),plan,patches)
(p/'roundtrip-provenance.json').write_text(json.dumps(prov,indent=2)+'\n');(p/'roundtrip-postconditions.json').write_text(json.dumps(report,indent=2)+'\n')
assert h(p/'map-outside-figma-exact-final.png')==h(prior/'map-outside-cleanup-v2.png')
a=np.array(Image.open(p/'raw-4.jpeg').convert('RGB')).astype(int);b=np.array(Image.open(p/'figma-export.png').convert('RGB')).astype(int)
receipt={'schema':'figma-roundtrip-exact-composite/v1','figma_file_key':'uyDxOoN1iNDPpEHTKSUWg1','figma_page_id':'457:2','figma_frame_id':'457:3','figma_upload_status':'SUCCEEDED_VIA_OPERA_NEON_POST','figma_export_status':'SUCCEEDED','figma_export_sha256':h(p/'figma-export.png'),'reference_sha256':h(p/'raw-4.jpeg'),'final_sha256':h(p/'map-outside-figma-exact-final.png'),'source_readback':readbacks,'method':'FIGMA_BOUND_RAW_LOCAL_LAYER_RECOVERY_THEN_ORIGINAL_PIXEL_MASKED_COMPOSITE','engineering_pass':report['engineering_pass'],'outside_mask_changed_pixels':report['outside_mask_changed_pixels'],'dimensions':report['output_dimensions'],'approved_prior_png_byte_identical':True,'strict_structure_verdict':'FAIL_UNRESOLVED_TITLE_GEOMETRY','independent_review_performed':False,'whole_workflow_complete':False,'native_state_changed':False,'s7_human':'PENDING','raw_export_measured_max_rgb_difference':int(np.max(np.abs(a-b))),'raw_export_pixel_diff_cause':'UNPROVEN_RENDERER_DECODING_OR_COLOR_MANAGEMENT_DIFFERENCE_NOT_TOLERATED','new_image_generation_calls':0}
(p/'FIGMA_ROUNDTRIP_RECEIPT.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n');print(json.dumps(receipt,ensure_ascii=False))
