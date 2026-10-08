// Evidence completeness only. This server cannot read Figma, Drive or reviewer pixels.
const hash = x => typeof x === 'string' && /^[a-f0-9]{64}$/.test(x);
const obj = x => x && typeof x === 'object' && !Array.isArray(x);
const text = x => typeof x === 'string' && x.trim().length > 0 && x.length <= 2048;
export const DELIVERY_REQUIREMENTS = Object.freeze({schema:'figma-structure-edit-delivery/v1',figma_source_required:true,figma_source_must_contain_bound_reference_and_local_layers:true,figma_export_required:true,python_composite_alone_completes_workflow:false,independent_pixel_review_required:true,on_figma_upload_or_export_unavailable:'STOP_WORKFLOW_INCOMPLETE',finalization:'FIGMA_PRODUCTION_THEN_EXACT_ORIGINAL_PIXEL_FINALIZATION',server_verifies_external_artifacts:false});
export function validateDelivery(receipt) {
  const r=obj(receipt)?receipt:{}, blockers=[];
  const add=(pass,code)=>{if(!pass)blockers.push(code);};
  add(r.schema===DELIVERY_REQUIREMENTS.schema,'DELIVERY_RECEIPT_SCHEMA_REQUIRED');
  add(hash(r.reference_sha256)&&hash(r.final_sha256),'REFERENCE_AND_FINAL_HASH_REQUIRED');
  const f=obj(r.figma)?r.figma:{};
  add(text(f.file_key)&&text(f.page_id)&&text(f.node_id)&&text(f.readback_evidence),'ACTUAL_FIGMA_SOURCE_READBACK_REQUIRED');
  add(f.reference_sha256===r.reference_sha256&&hash(f.reference_sha256)&&f.original_pixels_present===true&&f.masked_local_layers_present===true,'FIGMA_BOUND_ORIGINAL_AND_LOCAL_LAYERS_REQUIRED');
  add(f.upload_status==='SUCCEEDED','FIGMA_ASSET_UPLOAD_NOT_COMPLETE');
  add(f.export_status==='SUCCEEDED'&&hash(f.export_sha256)&&text(f.export_evidence),'ACTUAL_FIGMA_EXPORT_REQUIRED');
  const e=obj(r.exact_validation)?r.exact_validation:{};
  add(e.reference_sha256===r.reference_sha256&&e.output_sha256===r.final_sha256&&hash(e.reference_sha256)&&hash(e.output_sha256)&&e.engineering_pass===true&&e.lossless_png===true&&e.outside_mask_changed_pixels===0&&Number.isInteger(e.reference_width)&&Number.isInteger(e.reference_height)&&e.reference_width>0&&e.reference_height>0&&e.output_width===e.reference_width&&e.output_height===e.reference_height&&text(e.evidence),'EXACT_FINAL_PIXEL_VALIDATION_REQUIRED');
  const p=obj(r.provenance)?r.provenance:{};
  add(p.reference_sha256===r.reference_sha256&&p.final_sha256===r.final_sha256&&hash(p.final_sha256)&&p.figma_export_sha256===f.export_sha256&&hash(p.figma_export_sha256)&&text(p.evidence),'FIGMA_EXPORT_TO_EXACT_FINAL_PROVENANCE_REQUIRED');
  const v=obj(r.review)?r.review:{};
  add(v.reference_sha256===r.reference_sha256&&v.output_sha256===r.final_sha256&&hash(v.output_sha256)&&v.actual_pixels_viewed===true&&v.independent===true&&text(v.carrier_evidence)&&text(v.pixel_transport_evidence)&&v.copy_confirmed===true&&['photo','two_people','cabin','sunset','water','crop','layout'].every(k=>v.checks?.[k]===true),'BOUND_INDEPENDENT_ACTUAL_PIXEL_REVIEW_REQUIRED');
  return {status:blockers.length?'BLOCKED':'EVIDENCE_COMPLETE_PENDING_EXECUTOR_RECHECK',action:blockers.length?'STOP':'RECHECK_ACTUAL_EXTERNAL_ARTIFACTS',blockers,evidence_complete:!blockers.length,workflow_complete:false,final_eligible:false,external_evidence_verification:'CALLER_SUPPLIED_NOT_SERVER_VERIFIED',business_state_changed:false,human_acceptance_changed:false};
}
const str={type:'string',maxLength:2048};const sha={type:'string',pattern:'^[a-f0-9]{64}$'};const bool={type:'boolean'};const integer={type:'integer',minimum:0};
const record=properties=>({type:'object',properties,additionalProperties:false});
export const DELIVERY_RECEIPT_SCHEMA=record({schema:{type:'string',const:DELIVERY_REQUIREMENTS.schema},reference_sha256:sha,final_sha256:sha,
 figma:record({file_key:str,page_id:str,node_id:str,readback_evidence:str,reference_sha256:sha,original_pixels_present:bool,masked_local_layers_present:bool,upload_status:str,export_status:str,export_sha256:sha,export_evidence:str}),
 exact_validation:record({reference_sha256:sha,output_sha256:sha,engineering_pass:bool,lossless_png:bool,outside_mask_changed_pixels:integer,reference_width:integer,reference_height:integer,output_width:integer,output_height:integer,evidence:str}),
 provenance:record({reference_sha256:sha,final_sha256:sha,figma_export_sha256:sha,evidence:str}),
 review:record({reference_sha256:sha,output_sha256:sha,actual_pixels_viewed:bool,independent:bool,carrier_evidence:str,pixel_transport_evidence:str,copy_confirmed:bool,checks:record(Object.fromEntries(['photo','two_people','cabin','sunset','water','crop','layout'].map(k=>[k,bool])))})});
