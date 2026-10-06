const page=await figma.getNodeByIdAsync('412:2');await figma.setCurrentPageAsync(page);
const name='LIUXIANSHENG_CONTENT_TRANSFER_S3_IMAGE_GUIDE';
if(page.children.some(n=>n.name===name))throw Error('Already exists; inspect, never replay');
function fp(n){const a=[];function walk(x){let q={id:x.id,name:x.name,type:x.type};for(const k of ['x','y','width','height','visible','opacity','locked','fills','strokes','vectorPaths','characters','fontName','fontSize','relativeTransform']){if(k in x)q[k]=x[k];}a.push(q);if('children'in x)x.children.forEach(walk)}walk(n);const j=JSON.stringify(a);let h=2166136261;for(let i=0;i<j.length;i++){h^=j.charCodeAt(i);h=Math.imul(h,16777619)}return {fnv1a32:h>>>0,serialized_length:j.length,nodes:a.length}}
const protectedIds=['416:2','424:2','429:2'],before={};for(const id of protectedIds)before[id]=fp(await figma.getNodeByIdAsync(id));
const C={ink:'#f7f3e7',green:'#183325',orange:'#ff7b12',gold:'#c5af6f',black:'#101811',quiet:'#c4c8ba'};
function paint(h){return {type:'SOLID',color:{r:parseInt(h.slice(1,3),16)/255,g:parseInt(h.slice(3,5),16)/255,b:parseInt(h.slice(5,7),16)/255}}}
const I={family:'Inter',style:'Bold'},IR={family:'Inter',style:'Regular'},NS={family:'Noto Sans SC',style:'Regular'},NB={family:'Noto Sans SC',style:'Bold'},SE={family:'Noto Serif SC',style:'Bold'},MA={family:'Ma Shan Zheng',style:'Regular'};
await Promise.all([I,IR,NS,NB,SE,MA].map(x=>figma.loadFontAsync(x)));
const f=figma.createFrame();f.name=name;f.resize(960,1280);f.fills=[paint(C.green)];page.appendChild(f);f.x=Math.max(...page.children.filter(n=>n.id!==f.id).map(n=>n.x+n.width),0)+160;f.y=200;f.clipsContent=true;
function text(value,font,size,color,parent,label){const t=figma.createText();t.fontName=font;t.characters=value;t.fontSize=size;t.fills=[paint(color)];t.lineHeight={unit:'PERCENT',value:103};t.textAutoResize='WIDTH_AND_HEIGHT';parent.appendChild(t);t.name=label;return t;}
function stack(direction,label,parent,x,y,w,h){const s=figma.createAutoLayout(direction);s.name=label;parent.appendChild(s);s.fills=[];s.x=x;s.y=y;s.resize(w,h);s.primaryAxisSizingMode=direction==='HORIZONTAL'?'FIXED':'AUTO';s.counterAxisSizingMode='FIXED';s.counterAxisAlignItems='CENTER';s.paddingLeft=s.paddingRight=s.paddingTop=s.paddingBottom=0;return s;}
const header=stack('HORIZONTAL','EDITABLE_TOP_COPY_S3',f,56,68,848,70);header.primaryAxisAlignItems='SPACE_BETWEEN';
for(const value of ['LIVE\nWILD','STAY\nWEIRD','FREE\nSOUL','NO FIXED\nADDRESS']){const t=text(value,I,31,C.ink,header,'EDITABLE_TOP_'+value.replace('\n','_'));t.textAlignHorizontal='CENTER';}
const w=figma.createNodeFromSvg(WORDMARK_SVG);f.appendChild(w);w.name='IMAGE_GUIDE_RECONSTRUCTED_LIU_VECTOR_S3';w.resize(960,1280);w.x=0;w.y=0;
const seal=figma.createEllipse();f.appendChild(seal);seal.name='IMAGE_GUIDE_SEAL_SHAPE_S3';seal.resize(84,196);seal.x=76;seal.y=416;seal.fills=[paint(C.orange)];
const st=text('不住山',MA,46,C.black,f,'EDITABLE_SEAL_COPY_S3');st.textAutoResize='HEIGHT';st.resize(48,166);st.textAlignHorizontal='CENTER';st.lineHeight={unit:'PERCENT',value:112};st.x=94;st.y=435;
const en=text('Mister\nLiu',I,38,C.gold,f,'EDITABLE_ENGLISH_SUBMARK_S3');en.x=171;en.y=628;
const main=stack('VERTICAL','EDITABLE_MAIN_COPY_STACK_S3',f,135,727,690,310);main.itemSpacing=100;
const cap=text('疯疯癫癫 · 自在人间',SE,50,C.gold,main,'EDITABLE_GOLD_CAPTION_S3');if(cap.width>690)cap.fontSize=50*690/cap.width;
const orange=text('山人不住山  心里有青山',MA,62,C.orange,main,'EDITABLE_ORANGE_HANDWRITING_S3');if(orange.width>690)orange.fontSize=62*690/orange.width;
const footer=stack('VERTICAL','EDITABLE_FOOTER_S3',f,220,1120,520,100);footer.itemSpacing=8;
text('自由闲人',NB,62,C.ink,footer,'EDITABLE_FOOTER_IDENTITY_S3');text('不赶路，不合群，偶尔认真。',NS,24,C.ink,footer,'EDITABLE_FOOTER_COPY_S3');
const left=text('FREE SPIRIT',IR,17,C.quiet,f,'EDITABLE_CORNER_LEFT_S3');left.x=48;left.y=1202;
const right=text('MOUNTAINS WITHIN',IR,17,C.quiet,f,'EDITABLE_CORNER_RIGHT_S3');right.x=916-right.width;right.y=1202;
const after={};for(const id of protectedIds){after[id]=fp(await figma.getNodeByIdAsync(id));if(JSON.stringify(before[id])!==JSON.stringify(after[id]))throw Error('Protected study/version changed '+id);}
const all=[f,...f.findAll()],ts=f.findAllWithCriteria({types:['TEXT']});
return {createdNodeIds:all.map(n=>n.id),mutatedExistingNodeIds:[],file_key:figma.fileKey,page_id:page.id,page_name:page.name,frame_id:f.id,frame_name:f.name,width:f.width,height:f.height,text_count:ts.length,candidate_texts:ts.map(t=>t.characters),fonts:ts.map(t=>({id:t.id,text:t.characters,font:t.fontName,size:t.fontSize,bounds:t.absoluteBoundingBox,visible:t.visible,locked:t.locked,hasMissingFont:t.hasMissingFont})),wordmark_node:w.id,wordmark_vector_count:w.findAllWithCriteria({types:['VECTOR']}).length,vector_count:f.findAllWithCriteria({types:['VECTOR']}).length,type_frame_image_paints:all.flatMap(n=>Array.isArray(n.fills)?n.fills:[]).filter(p=>p.type==='IMAGE').length,reconstruction_source_sha256:'e4c9ba5f928cd63e8c7feb8ff0480ff142e0953e02ca7e8b5c8acf1a6f763f6f',before,after,protected_s2_unchanged:true,protected_transfer_s1_s2_unchanged:true};
