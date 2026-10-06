import { sha256 } from './core.mjs';
// Cooperating executor gate, not a host-wide intercept. Call immediately before the tool.
export async function executeStructureLockedEdit({plan, referenceBytes, context, invokeEdit}) {
  const c=plan?.execution_contract, b=c?.reference_binding;
  const stop=reason=>{throw new Error('STOP: '+reason);};
  if(c?.image_operation!=='EDIT_EXISTING_IMAGE_ONLY'||c.text_to_image_allowed!==false||c.fallback_allowed!==false)stop('not an edit-only contract');
  if(plan.action==='STOP'||!b)stop('reference not bound');
  if(!(referenceBytes instanceof Uint8Array)||!referenceBytes.length)stop('actual reference bytes unavailable');
  if(!context||context.context_id!==b.context_id||context.attachment_id!==b.attachment_id||context.attached_in_current_context!==true||context.pixels_viewed!==true||context.edit_target!==b.edit_target)stop('current pixel context or edit target mismatch');
  if(await sha256(referenceBytes)!==b.sha256)stop('actual reference SHA mismatch');
  if(typeof invokeEdit!=='function')stop('image editor unavailable');
  const input=Object.freeze({image_operation:'EDIT_EXISTING_IMAGE_ONLY',edit_target:b.edit_target,reference_sha256:b.sha256,reference_bytes:referenceBytes,hard_preserve:c.hard_preserve,allowed_changes:c.allowed_changes,prohibited_additions:c.prohibited_additions,replace_text_only:plan.proposed_copy,text_to_image_allowed:false});
  // No catch/retry/fallback: editor errors propagate and must be preserved.
  return invokeEdit(input);
}
