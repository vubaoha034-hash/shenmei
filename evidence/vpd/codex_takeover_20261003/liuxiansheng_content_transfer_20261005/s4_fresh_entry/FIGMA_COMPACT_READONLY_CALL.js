const page=await figma.getNodeByIdAsync("412:2");
if(!page||page.type!=="PAGE")throw new Error("Declared page missing");
await figma.setCurrentPageAsync(page);
const frame=await figma.getNodeByIdAsync("442:2");
if(!frame||frame.type!=="FRAME"||frame.parent.id!=="412:2")throw new Error("S4 frame identity mismatch");
const all=[];
function walk(n){all.push(n);if("children" in n)for(const c of n.children)walk(c);}
walk(frame);
function fnv(s){let h=2166136261;for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,16777619)>>>0;}return h;}
const texts=all.filter(n=>n.type==="TEXT").map(n=>({id:n.id,characters:n.characters,hasMissingFont:n.hasMissingFont,segments:n.getStyledTextSegments(["fontName","fontSize"]).map(s=>({start:s.start,end:s.end,fontName:{family:s.fontName.family,style:s.fontName.style},fontSize:s.fontSize}))}));
const vectors=all.filter(n=>n.type==="VECTOR").map(n=>{const p=n.vectorPaths;const d=p.map(x=>x.data).join("\n");return{id:n.id,pathCount:p.length,pathDataCharacters:d.length,pathDataFnv1a32:fnv(d)};});
const nodes=all.map(n=>({id:n.id,type:n.type,name:n.name,parentId:n.parent?n.parent.id:null,visible:"visible" in n?n.visible:null,locked:"locked" in n?n.locked:null}));
const wm=await figma.getNodeByIdAsync("442:8");
return{readOnly:true,fileKey:"uyDxOoN1iNDPpEHTKSUWg1",pageId:page.id,pageName:page.name,frameId:frame.id,width:frame.width,height:frame.height,wordmarkId:wm.id,wordmarkType:wm.type,wordmarkVectorIds:all.filter(n=>n.type==="VECTOR"&&(n.id==="442:10"||n.id==="442:11"||n.id==="442:13"||n.id==="442:15"||n.id==="442:16")).map(n=>n.id),nodeCount:nodes.length,nodeCountIncludesFrame:true,textCount:texts.length,vectorCount:vectors.length,imagePaintCount:all.reduce((v,n)=>v+("fills" in n&&Array.isArray(n.fills)?n.fills.filter(p=>p.type==="IMAGE").length:0),0),nodes,texts,vectors,createdNodeIds:[],mutatedNodeIds:[],digestLimit:"FNV path summaries are non-cryptographic; exact source paths intentionally excluded to avoid tool transport truncation."};
