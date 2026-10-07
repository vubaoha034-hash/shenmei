import test from 'node:test';
import assert from 'node:assert/strict';
import {createTask,applyStage,STAGES,TASK_CONTRACT} from './typography-task.mjs';

const h=n=>String(n).repeat(64).slice(0,64);
const ref='a'.repeat(64), local='b'.repeat(64), exp='c'.repeat(64);
const base=createTask(
  {request_key:'request_001',reference_source:'attachment://reference.png',requested_copy:{title:'地图以外'},request_title:'地图以外独立文字'},
  {source:{commit:'d'.repeat(40)},task_id:'native',stage:'S7',next_required_action:'HUMAN',snapshot_only:true},
  '2026-10-07T05:00:00Z',
  'typo_00000000-0000-4000-8000-000000000000'
);

test('contract freezes exact five-stage delivery order',()=>{
  assert.deepEqual(TASK_CONTRACT.stages,STAGES);
  assert.equal(TASK_CONTRACT.target_delivery,'FIGMA_EDITABLE_ISOLATED_TYPOGRAPHY');
  assert.equal(base.stage,'REFERENCE_TEXT_EXTRACTION');
  assert.equal(base.native_state_write,false);
  assert.equal(base.s7_state_unchanged,true);
});

test('full poster cannot substitute for isolated lettering stage',()=>{
  const t=applyStage(base,'REFERENCE_TEXT_EXTRACTION',{
    artifact_type:'REFERENCE_TEXT_EXTRACTION',reference_source:base.reference_source,reference_sha256:ref,
    actual_reference_pixels_viewed:true,extracted_reference_text:{title:'最长的旅途'},
    typography_observations:'错落书法主标题',geometry_evidence:'evidence://geometry'
  },'2026-10-07T05:01:00Z');
  assert.throws(()=>applyStage(t,'LOCAL_LETTERING_ASSET',{
    artifact_type:'LOCAL_LETTERING_ASSET',reference_sha256:ref,asset_sha256:local,asset_locator:'asset://letters',
    transparent_background:true,isolated_typography_only:true,copy_confirmed:true,target_copy:{title:'地图以外'},contains_full_poster:true
  },'2026-10-07T05:02:00Z'),/FULL_POSTER/);
});

test('editable Figma source is mandatory; flattened image-only is rejected',()=>{
  let t=applyStage(base,'REFERENCE_TEXT_EXTRACTION',{
    artifact_type:'REFERENCE_TEXT_EXTRACTION',reference_source:base.reference_source,reference_sha256:ref,
    actual_reference_pixels_viewed:true,extracted_reference_text:{title:'最长的旅途'},
    typography_observations:'错落书法主标题',geometry_evidence:'evidence://geometry'
  },'2026-10-07T05:01:00Z');
  t=applyStage(t,'LOCAL_LETTERING_ASSET',{
    artifact_type:'LOCAL_LETTERING_ASSET',reference_sha256:ref,asset_sha256:local,asset_locator:'asset://letters',
    transparent_background:true,isolated_typography_only:true,copy_confirmed:true,target_copy:{title:'地图以外'},contains_full_poster:false
  },'2026-10-07T05:02:00Z');
  assert.throws(()=>applyStage(t,'FIGMA_EDITABLE_REBUILD',{
    artifact_type:'FIGMA_EDITABLE_TYPOGRAPHY_REBUILD',reference_sha256:ref,source_asset_sha256:local,
    file_key:'file',page_id:'1:1',node_id:'2:2',figma_url:'https://figma.example/file',readback_evidence:'evidence://readback',
    export_locator:'evidence://export',export_sha256:exp,actual_readback_verified:true,isolated_typography_only:true,
    contains_full_poster:false,flattened_image_only:true,native_text_node_count:0,editable_vector_node_count:0,image_node_count:1
  },'2026-10-07T05:03:00Z'),/FIGMA_READBACK_OR_SCOPE_INVALID|FIGMA_IMAGE_NODE/);
});

test('review failure loops back to Figma; passing review enables isolated delivery only',()=>{
  let t=base;
  t=applyStage(t,'REFERENCE_TEXT_EXTRACTION',{
    artifact_type:'REFERENCE_TEXT_EXTRACTION',reference_source:t.reference_source,reference_sha256:ref,actual_reference_pixels_viewed:true,
    extracted_reference_text:{title:'最长的旅途'},typography_observations:'错落书法主标题',geometry_evidence:'evidence://geometry'
  },'2026-10-07T05:01:00Z');
  t=applyStage(t,'LOCAL_LETTERING_ASSET',{
    artifact_type:'LOCAL_LETTERING_ASSET',reference_sha256:ref,asset_sha256:local,asset_locator:'asset://letters',
    transparent_background:true,isolated_typography_only:true,copy_confirmed:true,target_copy:{title:'地图以外'},contains_full_poster:false
  },'2026-10-07T05:02:00Z');
  const figma={artifact_type:'FIGMA_EDITABLE_TYPOGRAPHY_REBUILD',reference_sha256:ref,source_asset_sha256:local,
    file_key:'file',page_id:'1:1',node_id:'2:2',figma_url:'https://figma.example/file',readback_evidence:'evidence://readback',
    export_locator:'evidence://export',export_sha256:exp,actual_readback_verified:true,isolated_typography_only:true,
    contains_full_poster:false,flattened_image_only:false,native_text_node_count:1,editable_vector_node_count:4,image_node_count:0};
  t=applyStage(t,'FIGMA_EDITABLE_REBUILD',figma,'2026-10-07T05:03:00Z');
  const review=v=>({artifact_type:'ACTUAL_INDEPENDENT_TYPOGRAPHY_REVIEW',reference_sha256:ref,contains_full_poster:false,
    reviewed_export_sha256:exp,verdict:v,actual_pixels_viewed:true,reference_pixels_viewed:true,output_pixels_viewed:true,
    independent_context:true,creator_history_inherited:false,human_verdict_leaked:false,typography_only_scope:true,
    carrier_evidence:'evidence://carrier',pixel_transport_evidence:'evidence://pixels',review_notes:'真实像素审核'});
  let failed=applyStage(t,'ACTUAL_INDEPENDENT_TYPOGRAPHY_REVIEW',review('FAIL'),'2026-10-07T05:04:00Z');
  assert.equal(failed.stage,'FIGMA_EDITABLE_REBUILD');
  assert.equal(failed.status,'NEEDS_REPAIR');
  failed=applyStage(failed,'FIGMA_EDITABLE_REBUILD',{...figma,export_sha256:'e'.repeat(64),export_locator:'evidence://export2'},'2026-10-07T05:05:00Z');
  const passReview={...review('PASS'),reviewed_export_sha256:'e'.repeat(64)};
  failed=applyStage(failed,'ACTUAL_INDEPENDENT_TYPOGRAPHY_REVIEW',passReview,'2026-10-07T05:06:00Z');
  assert.equal(failed.stage,'ISOLATED_TYPOGRAPHY_DELIVERY');
  failed=applyStage(failed,'ISOLATED_TYPOGRAPHY_DELIVERY',{
    artifact_type:'ISOLATED_EDITABLE_TYPOGRAPHY_DELIVERY',reference_sha256:ref,contains_full_poster:false,
    file_key:'file',page_id:'1:1',node_id:'2:2',reviewed_export_sha256:'e'.repeat(64),review_verdict:'PASS',
    delivery_scope:'ISOLATED_EDITABLE_TYPOGRAPHY_ONLY',actual_figma_readback_verified:true,includes_editable_source:true,
    flattened_image_only:false,share_url:'https://figma.example/file',delivery_evidence:'evidence://delivery'
  },'2026-10-07T05:07:00Z');
  assert.equal(failed.status,'COMPLETE');
  assert.equal(failed.next_required_action,'NONE_COMPLETE');
});
