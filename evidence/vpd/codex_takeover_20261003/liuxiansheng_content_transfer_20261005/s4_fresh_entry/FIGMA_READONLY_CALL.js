const page = await figma.getNodeByIdAsync("412:2");
if (!page || page.type !== "PAGE") throw new Error("Declared page 412:2 missing");
await figma.setCurrentPageAsync(page);
const frame = await figma.getNodeByIdAsync("442:2");
if (!frame || frame.type !== "FRAME" || frame.parent.id !== "412:2") throw new Error("Declared S4 frame identity mismatch");
const nodes = [];
function inspect(n) {
  const s = {id:n.id,type:n.type,name:n.name,parentId:n.parent?n.parent.id:null};
  for (const k of ["visible","locked","opacity","x","y","width","height","layoutMode","itemSpacing"]) if (k in n) s[k]=n[k];
  for (const k of ["fills","strokes"]) if (k in n && Array.isArray(n[k])) s[k]=n[k];
  if (n.type === "TEXT") {
    s.characters=n.characters;
    s.hasMissingFont=n.hasMissingFont;
    s.segments=n.getStyledTextSegments(["fontName","fontSize"]);
  }
  if (n.type === "VECTOR") s.vectorPaths=n.vectorPaths;
  if ("children" in n) s.childIds=n.children.map(c=>c.id);
  nodes.push(s);
  if ("children" in n) for (const child of n.children) inspect(child);
}
inspect(frame);
const wm = await figma.getNodeByIdAsync("442:8");
return {readOnly:true,fileKey:"uyDxOoN1iNDPpEHTKSUWg1",editorType:figma.editorType,pageId:page.id,pageName:page.name,frameId:frame.id,width:frame.width,height:frame.height,wordmarkId:wm?wm.id:null,wordmarkType:wm?wm.type:null,wordmarkChildren:wm&&"children" in wm?wm.children.map(n=>({id:n.id,type:n.type,name:n.name})):[],nodeCount:nodes.length,textCount:nodes.filter(n=>n.type==="TEXT").length,vectorCount:nodes.filter(n=>n.type==="VECTOR").length,imagePaintCount:nodes.reduce((v,n)=>v+(n.fills||[]).filter(p=>p.type==="IMAGE").length,0),nodes,createdNodeIds:[],mutatedNodeIds:[]};
