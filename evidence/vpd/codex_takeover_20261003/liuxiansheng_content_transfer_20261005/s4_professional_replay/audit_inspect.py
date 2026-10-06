"""Read-only measurements for the independent S4 professional audit."""
import base64, csv, hashlib, io, json, pathlib, re, struct, sys, xml.etree.ElementTree as ET
ROOT = pathlib.Path(sys.argv[1]).resolve()
OUT = pathlib.Path(sys.argv[2]).resolve()
B = ROOT / 'evidence/vpd/codex_takeover_20261003/liuxiansheng_content_transfer_20261005'
P = B / 'guide-adapter-s4'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def record(p): return {'path': str(p.relative_to(ROOT)), 'sha256': sha(p), 'bytes': p.stat().st_size}
public_names = ['COPY_MANIFEST.json','FIGMA_WRITE_GUARD_S4.json','FIGMA_READBACK_S4.json','FIGMA_PHOTO_PROTECTION_S4.json','IMAGE_GUIDE_GENERATION_RECEIPT_S4.json']
sources = ['prepare-inputs.cjs','build-wordmark.py','render-preview.cjs','FIGMA_ASSEMBLY_S4.js','FROZEN_SPEC.json','S4_WORDMARK.svg','PROVENANCE.json','SOURCE_EXTRACTION.json','LICENSE-VTracer-LICENSE.txt','LICENSE-skia-pathops-LICENSE.txt','TECHNICAL_ATTEMPTS.json','GRAIN_SOURCE_EVIDENCE.json']
copy = load(B/'COPY_MANIFEST.json')
rb = load(B/'FIGMA_READBACK_S4.json')
photo = load(B/'FIGMA_PHOTO_PROTECTION_S4.json')
prov = load(P/'PROVENANCE.json')
own = load(OUT/'PROVENANCE.json')
sx = load(OUT/'SOURCE_EXTRACTION.json')
render = load(OUT/'TECHNICAL_RENDER.json')
grain_final = load(P/'GRAIN_SOURCE_EVIDENCE.json')
expected_copy = [*copy['copy']['top_columns'], copy['copy']['side_seal'], copy['copy']['english_submark'], copy['copy']['gold_caption'], copy['copy']['orange_statement'], copy['copy']['footer_identity'], copy['copy']['footer_statement'], copy['copy']['lower_left'], copy['copy']['lower_right']]
svg = (OUT/'S4_WORDMARK.svg').read_text(encoding='utf-8')
et = ET.fromstring(svg)
nodes = list(et.iter())
tag = lambda n:n.tag.rsplit('}',1)[-1]
path_nodes = [n for n in nodes if tag(n)=='path']
assembly = (P/'FIGMA_ASSEMBLY_S4.js').read_text(encoding='utf-8')
embedded_svg, end = json.JSONDecoder().raw_decode(assembly.split('const WORDMARK_SVG=',1)[1])
seal_match = re.search(r"const seal=figma\.createNodeFromSvg\('([^']+)'\)",assembly)
seal = ET.fromstring(seal_match[1]) if seal_match else None
grain_positions = [tuple(q) for hole in sx['source_internal_grain']['holes'] for q in hole['source_pixel_positions_xy']]
width = sx['source']['canvas'][0]
bridge = (OUT/'BRIDGE_ADDITIONS.raw').read_bytes()
cream = (OUT/'CREAM_SOURCE_CLEAN.raw').read_bytes()
edge = (OUT/'ORANGE_ACTUAL_EDGE_MIX.raw').read_bytes()
grain_overlap = sum(bool(bridge[y*width+x]) for x,y in grain_positions)
ops = sx['bridge']['operations']
escaped = []
for p,value in enumerate(bridge):
    if value:
        x,y = p%width,p//width
        if not any(o['box'][0]<=x<o['box'][2] and o['box'][1]<=y<o['box'][3] for o in ops):
            escaped.append([x,y])
def png_dimensions(p):
    b=p.read_bytes()
    if b[:8]!=b'\x89PNG\r\n\x1a\n': raise ValueError('Not PNG')
    return list(struct.unpack('>II',b[16:24]))
inputs = {}
for label,rel in [('G','.liu-visual-private/liuxiansheng_transfer_20261005/IMAGE_GUIDE_S4.png'),('T','.liu-visual-private/liuxiansheng_transfer_20261005/FIGMA_COMPLETE_S4.png'),('R','.liu-visual-private/product-type-integration-20261004/SHANYEJI-canonical-readback-20261005.jpg')]:
    p=ROOT/rel
    inputs[label]=record(p)
    if p.suffix=='.png': inputs[label]['dimensions']=png_dimensions(p)
deps=[]
for label,sub,dist in [('VTracer','vtracer_0_6_15_cp312','vtracer-0.6.15.dist-info'),('skia-pathops','skia_pathops_0_9_2_abi3','skia_pathops-0.9.2.dist-info')]:
    base=ROOT/'.liu-visual-private/dependencies'/sub/'site-packages'
    di=base/dist
    checked=[]; failures=[]; unhashed=[]
    for rel,digest,size in csv.reader((di/'RECORD').read_text(encoding='utf-8').splitlines()):
        f=base/rel
        if not digest: unhashed.append(rel); continue
        if not f.is_file(): failures.append({'path':rel,'error':'missing'});continue
        algorithm,desired=digest.split('=',1)
        actual=base64.urlsafe_b64encode(hashlib.new(algorithm,f.read_bytes()).digest()).rstrip(b'=').decode('ascii')
        if actual!=desired: failures.append({'path':rel,'error':'hash_mismatch'})
        checked.append(rel)
    native=[record(q) for q in base.rglob('*.pyd')]
    licenses=[record(q) for q in di.rglob('LICENSE')]
    deps.append({'tool':label,'site_packages':str(base),'metadata':record(di/'METADATA'),'record':record(di/'RECORD'),'record_hashed_members_checked':len(checked),'record_unhashed_rows':unhashed,'record_failures':failures,'native_extensions':native,'license_files':licenses,'license_copy_matches':all(sha(OUT/('LICENSE-'+label+'-'+q.name+'.txt'))==sha(q) for q in di.rglob('LICENSE'))})
font_contract = [{'id':f['id'],'characters':f['text'],'visible':f['visible'],'locked':f['locked'],'hasMissingFont':f['hasMissingFont'],'font':f['font'],'segment_characters_equal':''.join(s['characters'] for s in f['segments'])==f['text']} for f in rb['fonts']]
measure = {
    'schema':'s4-professional-independent-measurements/v1',
    'read_source_policy':{'review_results_read':False,'creator_self_scores_read':False,'creator_LOCAL_PIXEL_CHECK_read':False,'technical_attempt_failure_history_read':True,'root_entry_rules_read':True},
    'python':{'executable':sys.executable,'version':sys.version,'executable_sha256':sha(pathlib.Path(sys.executable)),'PIL_required_for_pipeline':False},
    'node_sharp':{'package_version':load(pathlib.Path('C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp/package.json'))['version'],'dependency_path_is_absolute_host_path':True},
    'public_inputs':[record(B/n) for n in public_names],
    'public_adapter_files':[record(P/n) for n in sources],
    'images':inputs,
    'copy_contract':{'dimension_match':rb['width']==copy['dimensions'][0] and rb['height']==copy['dimensions'][1],'text_count':rb['text_count'],'expected_native_text_count':len(expected_copy),'candidate_texts_exact_match':rb['candidate_texts']==expected_copy,'required_anchors_present':all(a in '\n'.join(rb['candidate_texts']) for a in copy['required_copy_anchors']),'fonts':font_contract,'all_native_text_unlocked_visible_fonts_present':all(f['visible'] and not f['locked'] and not f['hasMissingFont'] and f['segment_characters_equal'] for f in font_contract),'live_readback_performed_by_auditor':False},
    'svg':{'reproduced':record(OUT/'S4_WORDMARK.svg'),'public_svg_equal_bytes':(OUT/'S4_WORDMARK.svg').read_bytes()==(P/'S4_WORDMARK.svg').read_bytes(),'expected_sha_equal':sha(OUT/'S4_WORDMARK.svg')=='0f0a43f7547ded5afa46f36de391dd4ac536c1d7018facabad988248da78d2b9','canvas':{k:et.attrib[k] for k in ['width','height','viewBox']},'path_count':len(path_nodes),'path_ids':[n.attrib['id'] for n in path_nodes],'each_path_ends_closed':all(n.attrib['d'].rstrip().endswith('Z') for n in path_nodes),'image_count':sum(tag(n)=='image' for n in nodes),'text_count':sum(tag(n)=='text' for n in nodes),'foreignObject_count':sum(tag(n)=='foreignObject' for n in nodes),'external_or_data_payload':bool(re.search(r'data:|https?://(?!www.w3.org/2000/svg)|href=',svg)),'embedded_assembly_svg_equals_reproduced_after_whitespace_trim':embedded_svg.strip()==svg.strip(),'seal_path_count':sum(tag(n)=='path' for n in seal.iter()) if seal is not None else None},
    'recorded_figma_topology':{'file_key':rb['file_key'],'page_id':rb['page_id'],'frame_id':rb['frame_id'],'frame_name':rb['frame_name'],'canvas':[rb['width'],rb['height']],'wordmark_vector_count':rb['wordmark_vector_count'],'total_vectors':rb['vector_count'],'seal_vectors_inferred_from_total':rb['vector_count']-rb['wordmark_vector_count'],'image_paints':rb['type_frame_image_paints'],'export_sha_matches_T':rb['export_sha256']==inputs['T']['sha256'],'export_dimensions_matches_T':inputs['T']['dimensions']==[rb['width'],rb['height']],'created_node_ids':rb['createdNodeIds'],'declared_mutated_existing_ids':rb['mutatedExistingNodeIds'],'declared_mutation_list_is_not_a_general_mutation_log':True},
    'provenance':{'final_public_provenance':record(P/'PROVENANCE.json'),'public_metadata_changed_after_initial_read':True,'initial_public_provenance_sha256':None,'pipeline_source_not_replayed_after_metadata_refresh':True,'own':record(OUT/'PROVENANCE.json'),'own_source_extraction':record(OUT/'SOURCE_EXTRACTION.json'),'public_source_extraction_byte_equal':(OUT/'SOURCE_EXTRACTION.json').read_bytes()==(P/'SOURCE_EXTRACTION.json').read_bytes(),'own_traces':own['trace_runs'],'trace_generation_calls_this_audit':own['trace_generation_calls_this_builder_run'],'trace_generation_calls_recorded_creator_chain':prov['total_trace_generation_calls_in_this_asset_chain'],'mapping':own['coordinate_mapping'],'source_visible_cream_components':len(sx['cream']['retained_components']),'inferred_bridge_pixels':sum(bool(x) for x in bridge),'bridge_fact_pixels':sx['bridge']['added_pixels'],'bridge_pixels_outside_frozen_windows':len(escaped),'bridge_overlapping_actual_grain_pixels':grain_overlap,'actual_grain_components':sx['source_internal_grain']['count'],'actual_grain_pixels':len(grain_positions),'final_grain_record_matches_own_source_positions':grain_final['internal_grain']==sx['source_internal_grain'],'mixed_edge_pixels':sum(bool(x) for x in edge),'existing_source_cream_trace_overlap':sx['bridge']['original_cream_trace_overlap'],'sheng_crossing_inferred_pixels':sx['bridge']['sheng_base_local_revision']['unique_added_pixels'],'expert_cut_count':len(load(P/'FROZEN_SPEC.json')['source_coordinate_cuts']),'expert_window_intersection_count':len(load(P/'FROZEN_SPEC.json')['source_coordinate_intersections']),'expert_single_component_replacement':load(P/'FROZEN_SPEC.json')['replacement']['id'],'final_vector_grain_hole_count_not_claimed':True},
    'licenses_and_dependency_integrity':deps,
    'render':render,
    'recorded_protection':{'old_node_ids':list(rb['before']),'old_subtree_selected_property_fingerprints_equal':rb['before']==rb['after'],'protected_photo_selected_snapshot_equal':photo['before']==photo['after'],'protected_photo_frame_id':photo['before']['frame_id'],'photo_node_id':photo['before']['photo']['id'],'photo_node_locked':photo['before']['photo']['locked'],'photo_image_hash_same':photo['before']['photo']['fills'][0]['imageHash']==photo['after']['photo']['fills'][0]['imageHash'],'protected_raw_source_sha_recorded':photo['raw_photo_sha256'],'raw_protected_photo_bytes_verified_by_auditor':False,'scope_limit':'Recorded selected properties and FNV-1a-32 snapshots; no independent fresh Figma read or protected-photo pixel export in this audit. Existing page gains a child frame; mutatedExistingNodeIds is declarative and does not enumerate page navigation/child-list edits.'}
}
(OUT/'MEASUREMENTS.json').write_text(json.dumps(measure,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'svg':measure['svg'],'copy_summary':{k:v for k,v in measure['copy_contract'].items() if k!='fonts'},'dependency_record_failures':[d['record_failures'] for d in deps],'metadata_final_sha':measure['provenance']['final_public_provenance']['sha256'],'measurements_sha256':sha(OUT/'MEASUREMENTS.json')},ensure_ascii=True))

