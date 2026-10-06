const page = await figma.getNodeByIdAsync("412:2");
if (!page || page.type !== "PAGE") throw new Error("Missing authorized source page");
await figma.setCurrentPageAsync(page);
const frame = await figma.getNodeByIdAsync("453:10");
const wordmark = await figma.getNodeByIdAsync("453:37");
if (!frame || frame.type !== "FRAME" || frame.parent.id !== "412:2") throw new Error("Wrong current source identity");
function fnv(s) { let h=2166136261; for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,16777619)>>>0;} return h; }
const nodes = []; function walk(n) {nodes.push(n); if("children" in n) for(const c of n.children) walk(c);} walk(frame);
const texts = nodes.filter(n=>n.type==="TEXT").map(n=>({id:n.id,name:n.name,characters:n.characters,fontName:n.fontName,fontSize:n.fontSize,hasMissingFont:n.hasMissingFont,textAutoResize:n.textAutoResize,visible:n.visible,locked:n.locked,x:n.x,y:n.y,width:n.width,height:n.height,fills:n.fills}));
const vectors = nodes.filter(n=>n.type==="VECTOR").map(n=>{const vp=n.vectorPaths; const serialized=JSON.stringify(vp); return {id:n.id,name:n.name,parent:n.parent.id,visible:n.visible,locked:n.locked,opacity:n.opacity,x:n.x,y:n.y,width:n.width,height:n.height,fills:n.fills,strokes:n.strokes,vectorPathCount:vp.length,vectorPathSerializedLength:serialized.length,vectorPathFnv1a32:fnv(serialized)};});
const stats={}; for(const n of nodes) stats[n.type]=(stats[n.type]||0)+1;
return {read_only:true,createdNodeIds:[],mutatedNodeIds:[],file_key:"uyDxOoN1iNDPpEHTKSUWg1",page_id:page.id,page_name:page.name,frame:{id:frame.id,name:frame.name,x:frame.x,y:frame.y,width:frame.width,height:frame.height,visible:frame.visible,locked:frame.locked},wordmark:{id:wordmark.id,type:wordmark.type,parent:wordmark.parent.id},node_count:nodes.length,types:stats,texts,vectors,sourceContainsImage:nodes.some(n=>"fills" in n && Array.isArray(n.fills) && n.fills.some(p=>p.type==="IMAGE")),preserved_page_frames:page.children.filter(n=>n.type==="FRAME").map(n=>({id:n.id,name:n.name,width:n.width,height:n.height}))};
