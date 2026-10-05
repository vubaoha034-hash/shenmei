"""Build the one V28 contextual Tea-leaf poster with the unchanged finite kernel.

Only a deepcopy manifest receives formal_version24 in memory; saved identity28.
Ordinary source-over frozen photography and brand, seven closed compound glyphs.
"""
from pathlib import Path
import argparse, copy, hashlib, io, json, sys
sys.dont_write_bytecode=True
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parents[5]
OUT=Path(__file__).resolve().parent
PRIVATE=ROOT/'.liu-visual-private/correct_source_typography/v28'
sys.path.insert(0,str(ROOT))
from visual_memory import vpd_registered_type_composite as g
AUTHORIZED_RECT=(360,350,1360,672)

def sha(raw):return hashlib.sha256(raw).hexdigest()
def jb(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def ref(p,raw=None):
    p=Path(p).resolve()
    assert p.is_relative_to(ROOT.resolve())
    raw=p.read_bytes() if raw is None else raw
    return {'path':p.relative_to(ROOT).as_posix(),'sha256':sha(raw),'bytes':len(raw)}
def png(im):
    b=io.BytesIO();im.save(b,format='PNG');return b.getvalue()
def root_write_gate():
    raw=(ROOT/'continuity/vpd/CURRENT_TASK_LOCK.json').read_bytes()
    lock=json.loads(raw);u=lock['codex_takeover']['worker_continuation'];last=u['versions'][-1]
    assert lock['revision']==330 and u['phase']=='REVISION_REQUIRED'
    assert u['unit_id']=='CHAZUO_APPROVED_SOURCE_TYPOGRAPHY_20261003_R1'
    assert last['number']==27 and last['verdict']=='AI_FAIL'
    return {'native_revision':330,'lock_sha256':sha(raw),'parent_go':'GO_V28'}
def calculate():
    source_raw=g.checked_bytes(ROOT,g.SOURCE);brand_raw=g.checked_bytes(ROOT,g.BRAND)
    k=g.edited_kernel(ROOT)
    original_geometry=copy.deepcopy(k['INPUTS']['art_direction'])
    k['INPUTS']=copy.deepcopy(k['INPUTS'])
    k['INPUTS']['art_direction']=ref(OUT/'ART_DIRECTION_V28_GEOMETRY.json')
    finite_geometry=json.loads(k['checked'](ROOT,k['INPUTS']['art_direction']))
    previous_geometry=json.loads(k['checked'](ROOT,original_geometry))
    assert finite_geometry['original_geometry']['sha256']==original_geometry['sha256']
    assert finite_geometry['negative_space']['cup_air']==previous_geometry['negative_space']['cup_air']
    manifest_path=OUT/'V28_GLYPH_EDIT_MANIFEST.json';manifest_raw=manifest_path.read_bytes()
    manifest=json.loads(manifest_raw)
    assert manifest['formal_version']==28 and manifest['copy']=='一杯茶，慢下来'
    assert manifest['source_trace']==k['INPUTS']['trace_svg']
    assert manifest['negative_space']['art_direction']==k['INPUTS']['art_direction']
    compatibility=copy.deepcopy(manifest);compatibility['formal_version']=24
    headline_raw,report=k['replay_edit_program'](ROOT,compatibility)
    assert manifest_path.read_bytes()==manifest_raw and manifest['formal_version']==28
    library=k['pathops_runtime'](ROOT)
    direction=json.loads(k['checked'](ROOT,k['INPUTS']['art_direction']))
    cup=k['make_path'](library,k['parse_closed'](direction['negative_space']['cup_air']))
    leaf=k['make_path'](library,k['parse_closed'](direction['negative_space']['leaf_air']))
    air=library.op(cup,leaf,library.PathOp.UNION,**k['FLAGS'])
    intersections=[]
    for row in report['glyphs']:
        pre=k['make_path'](library,k['parse_closed'](row['pre_difference_d']))
        intersection=library.op(pre,air,library.PathOp.INTERSECTION,**k['FLAGS'])
        n=sum(1 for unused in intersection.contours)
        intersections.append({'char':row['char'],'area':intersection.area,'contours':n,
                              'reported_float_area_delta':row['removed_area']})
        assert intersection.area==0 and n==0,'FIXED_EXCLUSION_WOULD_CUT_AUTHORED_STROKE:'+row['char']
    tree=g.svg_tree(headline_raw)
    assert all(n.tag in {g.NS+t for t in ['svg','g','path']} for n in tree.iter())
    assert len(list(tree.iter(g.NS+'path')))==7
    assert [tree.get(v) for v in ['width','height','viewBox']]==['1536','1024','0 0 1536 1024']
    render=g.renderer(ROOT)
    headline=render(headline_raw);brand=render(g.brand_canvas(brand_raw))
    source=Image.open(io.BytesIO(source_raw)).convert('RGBA')
    assert source.size==headline.size==brand.size==(1536,1024)
    assert source.getchannel('A').getextrema()==(255,255)
    box=headline.getchannel('A').getbbox();r=AUTHORIZED_RECT
    assert box and box[0]>=r[0] and box[1]>=r[1] and box[2]<=r[2] and box[3]<=r[3]
    preview=source.copy();preview.alpha_composite(brand);preview.alpha_composite(headline)
    overlay=Image.new('RGBA',source.size);overlay.alpha_composite(brand);overlay.alpha_composite(headline)
    zero=overlay.getchannel('A').point(lambda v:255 if v==0 else 0)
    diff=ImageChops.difference(preview.convert('RGB'),source.convert('RGB'))
    rgb=ImageChops.lighter(ImageChops.lighter(diff.getchannel('R'),diff.getchannel('G')),diff.getchannel('B'))
    assert ImageChops.darker(rgb,zero).getbbox() is None,'ALPHA_ZERO_SOURCE_CHANGED'
    assert (ROOT/g.SOURCE['path']).read_bytes()==source_raw and (ROOT/g.BRAND['path']).read_bytes()==brand_raw
    for name in ['generated_png','generation_evidence','provenance','source_commands','trace_builder']:
        k['checked'](ROOT,k['INPUTS'][name])
    glyphs=[{key:row[key] for key in ['char','source_contours','pre_area','post_area','removed_area','bounds','output_contours']} for row in report['glyphs']]
    replay={'saved_version':28,'in_memory_kernel_version':24,'kernel':g.EDIT_KERNEL,
            'single_parameter_shim':{'original_geometry':original_geometry,
                'V28_geometry':k['INPUTS']['art_direction'],'cup_air_original_exactly_equal':True,
                'leaf_air':'V28 fixed observed source-specific approximation; no exact segmentation claim',
                'same_original_difference_union_algorithm':True,'original_kernel_bytes_changed':False},
            'operation':'deepcopy saved28 manifest; set only in-memory formal_version24; unchanged kernel replay',
            'raw_kernel_report_sha256':sha(jb(report)),
            'in_memory_trace_verification':'Fixed alpha128 VTracer source replay, no new production trace written'}
    build={'schema':'vpd-v28-contextual-leaf-terminal-build/v1','formal_version':28,'copy':'一杯茶，慢下来',
        'program':ref(manifest_path,manifest_raw),'maker_source':ref(OUT/'make_glyph_program.py'),
        'maker_notes':ref(OUT/'SOURCE_REAUTHORING_NOTES.json'),'builder':ref(Path(__file__)),
        'source_inputs':k['INPUTS'],'original_art_direction':original_geometry,'kernel_compatibility':replay,'glyphs':glyphs,
        'object_exclusion_intersections':intersections,'headline_paths':7,'source_paths':17,'source_contours':21,
        'original_contours_bound_once':True,'actual_alpha_bbox_exclusive':list(box),
        'authorization_rect_for_this_GO_V28':list(r),'prior_V27_box_is_historical':True,
        'photograph':g.SOURCE,'brand':g.BRAND,'brand_placement':g.PLACEMENT,
        'photograph_bytes_unchanged':True,'brand_bytes_unchanged':True,'alpha_zero_source_RGB_changed_pixels':0,
        'context_specific_Tea_leaf_lettering':True,'standalone_complete_portable_Tea_claimed':False,
        'composition':'Frozen S source-over frozen brand at285/198 width205, then the one V28 seven-path headline.',
        'photo_mask_retouch_patch_filter_layers':0,'worker_imagegen_calls':0,'new_production_traces':0,
        'font_files_for_final_outlines':0,'business_state_writes':0,'Figma_Drive_Git_writes':0,
        'real_generation_version':24,'aesthetic_pass_claimed':False}
    assets={'headline.svg':headline_raw,'brand.svg':brand_raw,'BUILD_REPORT.json':jb(build)}
    private={'headline-render.png':png(headline),'preview.png':png(preview),
             'leaf-handoff-inspection.png':png(preview.crop((740,490,1030,790))),
             'reading-inspection.png':png(preview.crop((360,340,1360,672)))}
    provenance={'schema':'vpd-v28-contextual-source-bound-lettering/v1','formal_version':28,
        'copy':'一杯茶，慢下来','real_generation_version':24,'source_inputs':k['INPUTS'],
        'manifest':ref(manifest_path,manifest_raw),'maker_source':ref(OUT/'make_glyph_program.py'),
        'maker_notes':ref(OUT/'SOURCE_REAUTHORING_NOTES.json'),'builder':ref(Path(__file__)),
        'kernel_compatibility':replay,'actual_source_contours_bound_once':21,
        'method':'Restore natural source One, common reading cells, smaller baseline-stable later phrase; author only the closed contextual Tea right-na component ending into the original S leaf.',
        'source_specific_context_dependency':True,'portable_complete_Tea_glyph_claimed':False,
        'outputs':{name:ref(OUT/name,raw) for name,raw in assets.items()},
        'private_outputs':{name:ref(PRIVATE/name,raw) for name,raw in private.items()},
        'photograph':g.SOURCE,'brand':g.BRAND,'brand_placement':g.PLACEMENT,
        'additional_candidates_or_layout_selection':0,'new_imagegen_calls':0,'new_production_traces':0,
        'photo_masks_filters_patchback':0,'aesthetic_pass_claimed':False,'human_acceptance_claimed':False}
    assets['LETTERING_PROVENANCE.json']=jb(provenance)
    return {**{OUT/name:raw for name,raw in assets.items()},**{PRIVATE/name:raw for name,raw in private.items()}},build

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write',action='store_true');mode.add_argument('--verify-only',action='store_true')
    args=parser.parse_args();gate=root_write_gate() if args.write else None
    expected=[OUT/n for n in ['headline.svg','brand.svg','BUILD_REPORT.json','LETTERING_PROVENANCE.json']]
    expected += [PRIVATE/n for n in ['headline-render.png','preview.png','leaf-handoff-inspection.png','reading-inspection.png']]
    if args.write:assert not any(p.exists() for p in expected),'ASSET_ALREADY_EXISTS'
    outputs,build=calculate();assert set(outputs)==set(expected)
    if args.write:
        for p,raw in outputs.items():
            p.parent.mkdir(parents=True,exist_ok=True)
            with p.open('xb') as f:f.write(raw)
    for p,raw in outputs.items():assert p.read_bytes()==raw,'EXACT_BUILD_READBACK_MISMATCH:'+str(p)
    print(json.dumps({'action':'built-one-V28-complete-poster' if args.write else 'verified-existing',
        'formal_version':28,'writes':len(outputs) if args.write else 0,'root_gate':gate,
        'headline':ref(OUT/'headline.svg'),'preview':ref(PRIVATE/'preview.png'),
        'alpha_bbox':build['actual_alpha_bbox_exclusive'],'glyphs':build['glyphs'],
        'object_exclusion_intersections':build['object_exclusion_intersections'],
        'aesthetic_pass_claimed':False},ensure_ascii=False))
if __name__=='__main__':main()
