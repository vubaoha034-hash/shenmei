const ROLES = new Set(['top_text','main_title_text','right_vertical_text','footer_short_text','minimal_text_cleanup']);
const KEYS = new Set(['id','role','x','y','width','height','mask_source','mask_sha256','parent_region_id']);
export function validateEditRegions(regions,width,height) {
  const fail=reason=>({valid:false,reason});
  if(!Array.isArray(regions)||regions.length<1||regions.length>20)return fail('EXPLICIT_EDIT_MASKS_REQUIRED');
  const seen=new Set();
  for(const r of regions){
    if(!r||typeof r!=='object'||Array.isArray(r)||Object.keys(r).some(k=>!KEYS.has(k))||typeof r.id!=='string'||!r.id.trim()||r.id.length>128||seen.has(r.id)||!ROLES.has(r.role))return fail('INVALID_EDIT_REGION');
    seen.add(r.id);
    if(![r.x,r.y,r.width,r.height].every(Number.isInteger)||r.x<0||r.y<0||r.width<1||r.height<1||r.x+r.width>width||r.y+r.height>height)return fail('REGION_OUT_OF_BOUNDS');
    if(r.width===width&&r.height===height)return fail('WHOLE_CANVAS_MASK_FORBIDDEN');
    if(typeof r.mask_source!=='string'||!r.mask_source.trim()||r.mask_source.length>2048||/[\u0000-\u001f\u007f]/.test(r.mask_source)||typeof r.mask_sha256!=='string'||!/^[a-f0-9]{64}$/.test(r.mask_sha256))return fail('BINARY_MASK_IDENTITY_REQUIRED');
  }
  for(const r of regions){
    if(r.role==='minimal_text_cleanup'){
      const p=regions.find(p=>p.id===r.parent_region_id&&p.role!=='minimal_text_cleanup');
      if(!p||r.x<p.x||r.y<p.y||r.x+r.width>p.x+p.width||r.y+r.height>p.y+p.height)return fail('CLEANUP_MUST_BE_INSIDE_TEXT_REGION');
    }else if(r.parent_region_id!==undefined)return fail('INVALID_PARENT_REGION');
  }
  return {valid:true,reason:null};
}
