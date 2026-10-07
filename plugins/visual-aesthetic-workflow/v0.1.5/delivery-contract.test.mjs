import test from 'node:test';
import assert from 'node:assert/strict';
import {validateDelivery,DELIVERY_REQUIREMENTS} from './delivery-contract.mjs';
const a='a'.repeat(64),b='b'.repeat(64),c='c'.repeat(64);
function complete(){return {schema:DELIVERY_REQUIREMENTS.schema,reference_sha256:a,final_sha256:b,figma:{file_key:'fixture-file',page_id:'1:2',node_id:'1:3',readback_evidence:'fixture-readback',reference_sha256:a,original_pixels_present:true,masked_local_layers_present:true,upload_status:'SUCCEEDED',export_status:'SUCCEEDED',export_sha256:c,export_evidence:'fixture-export'},exact_validation:{reference_sha256:a,output_sha256:b,engineering_pass:true,lossless_png:true,outside_mask_changed_pixels:0,reference_width:709,reference_height:1536,output_width:709,output_height:1536,evidence:'fixture-validation'},provenance:{reference_sha256:a,final_sha256:b,figma_export_sha256:c,evidence:'fixture-provenance'},review:{reference_sha256:a,output_sha256:b,actual_pixels_viewed:true,independent:true,carrier_evidence:'fixture-carrier',pixel_transport_evidence:'fixture-original-byte-transport',copy_confirmed:true,checks:Object.fromEntries(['photo','two_people','cabin','sunset','water','crop','layout'].map(k=>[k,true]))}};}
test('empty/locator/PNG-only receipts cannot complete workflow',()=>{for(const r of [null,{}, {reference_source:'sediment://fixture'},{reference_sha256:a,final_sha256:b}])assert.equal(validateDelivery(r).action,'STOP');});
for(const [name,mutate,code] of [
 ['HTTP405 empty Figma frame',r=>{r.figma.upload_status='HTTP405';r.figma.original_pixels_present=false;},'FIGMA_ASSET_UPLOAD_NOT_COMPLETE'],
 ['missing real export',r=>delete r.figma.export_sha256,'ACTUAL_FIGMA_EXPORT_REQUIRED'],
 ['changed dimensions',r=>r.exact_validation.output_width=941,'EXACT_FINAL_PIXEL_VALIDATION_REQUIRED'],
 ['changed protected pixels',r=>r.exact_validation.outside_mask_changed_pixels=1,'EXACT_FINAL_PIXEL_VALIDATION_REQUIRED'],
 ['unrelated final artifact',r=>r.provenance.final_sha256=c,'FIGMA_EXPORT_TO_EXACT_FINAL_PROVENANCE_REQUIRED'],
 ['self review',r=>r.review.independent=false,'BOUND_INDEPENDENT_ACTUAL_PIXEL_REVIEW_REQUIRED'],
 ['strict layout fail',r=>r.review.checks.layout=false,'BOUND_INDEPENDENT_ACTUAL_PIXEL_REVIEW_REQUIRED'],
 ['wrong reviewed hash',r=>r.review.output_sha256=c,'BOUND_INDEPENDENT_ACTUAL_PIXEL_REVIEW_REQUIRED'],
 ['absent pixel transport',r=>delete r.review.pixel_transport_evidence,'BOUND_INDEPENDENT_ACTUAL_PIXEL_REVIEW_REQUIRED']
])test(name,()=>{const r=complete();mutate(r);const v=validateDelivery(r);assert.equal(v.action,'STOP');assert.ok(v.blockers.includes(code));assert.equal(v.final_eligible,false);});
test('complete synthetic receipt only admits executor recheck, never external or business PASS',()=>{const v=validateDelivery(complete());assert.equal(v.evidence_complete,true);assert.equal(v.action,'RECHECK_ACTUAL_EXTERNAL_ARTIFACTS');assert.equal(v.workflow_complete,false);assert.equal(v.final_eligible,false);assert.equal(v.business_state_changed,false);assert.equal(v.human_acceptance_changed,false);});
