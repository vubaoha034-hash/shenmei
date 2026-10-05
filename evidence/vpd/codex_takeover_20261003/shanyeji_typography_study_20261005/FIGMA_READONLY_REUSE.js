// Read figma-use skill first, then call use_figma(fileKey=uyDxOoN1iNDPpEHTKSUWg1).
// Read only: no creation, toggles, page selection or writes.
const frame = await figma.getNodeByIdAsync('416:2');
const editable = await figma.getNodeByIdAsync('416:3');
const ink = await figma.getNodeByIdAsync('416:271');
if (!frame || !editable || !ink) throw new Error('STUDY_NODES_MISSING');
const vectors = frame.findAll(n => n.type === 'VECTOR');
function effectivelyVisible(n) {
  for (let at=n; at && at.type!=='DOCUMENT'; at=at.parent) {
    if ('visible' in at && !at.visible) return false;
  }
  return true;
}
const result = {
  scope: 'SHANYEJI_WHOLE_TYPOGRAPHY_REFERENCE_RECONSTRUCTION_ONLY',
  frame: {id: frame.id, name: frame.name, width: frame.width, height: frame.height},
  page: {id: frame.parent.id, name: frame.parent.name},
  editable_vector_group: {id: editable.id, visible: editable.visible},
  vector_count: vectors.length,
  effectively_visible_vector_count: vectors.filter(effectivelyVisible).length,
  visible_ink: {id: ink.id, visible: ink.visible, imagePaints: ink.fills.filter(x=>x.type==='IMAGE').map(x=>({imageHash:x.imageHash,scaleMode:x.scaleMode}))},
  writes: 0,
  limitations: ['Geometry group is hidden in S2; visible ink is an approximate raster extraction. Editing vectors does not regenerate ink.']
};
return result;
