
const TARGET_DATA = {"泉":{"medians":[[[482,854],[494,847],[512,817],[407,678],[381,665]],[[294,654],[323,632],[330,616],[383,407]],[[353,651],[370,641],[614,687],[667,677],[691,641],[634,463],[621,438],[596,437]],[[383,530],[392,539],[492,558],[544,565],[565,560]],[[401,420],[413,433],[434,438],[588,460]],[[446,417],[474,404],[496,374],[487,38],[471,7],[358,49]],[[148,310],[208,299],[339,321],[370,303],[329,221],[253,122],[173,58],[107,24]],[[723,443],[734,432],[744,401],[650,319],[603,287],[596,290]],[[525,329],[534,303],[620,223],[715,143],[790,92],[971,76]]],"sha":"7020bd8d21d9cd924cfa8a8e53480bd086ddb81d"},"清":{"medians":[[[193,756],[283,699],[310,656]],[[117,539],[195,486],[219,455]],[[187,38],[173,81],[173,115],[316,390]],[[442,699],[504,693],[633,717],[711,739],[737,742],[763,736]],[[457,589],[485,583],[527,585],[696,622],[739,619]],[[561,850],[594,825],[605,803],[594,533],[579,512]],[[338,460],[393,454],[632,499],[867,528],[937,511]],[[452,396],[480,370],[484,335],[470,129],[449,41],[447,0]],[[511,380],[527,375],[693,413],[734,386],[730,297],[740,64],[734,19],[709,-20],[621,19]],[[505,255],[519,266],[575,277],[614,281],[635,275]],[[500,153],[531,167],[579,175],[638,171]]],"sha":"2aac34a81a0f1f4dc51d9b53c9100bdc6fdfcc91"},"风":{"medians":[[[244,673],[274,649],[286,622],[283,456],[270,342],[248,254],[222,187],[168,85],[137,44]],[[327,633],[335,648],[449,677],[672,718],[704,712],[720,690],[703,617],[692,515],[692,387],[706,292],[746,177],[785,118],[821,82],[867,55],[899,50],[922,109],[938,233]],[[537,587],[555,560],[562,537],[532,439],[492,340],[466,291],[411,214],[356,158],[316,128]],[[367,476],[566,259],[604,204],[617,160]]],"sha":"d8dcfdfb3ec64ef5177511f97d09871a1de44f54"},"入":{"medians":[[[499,510],[499,455],[403,320],[273,191],[191,131],[115,88]],[[342,683],[416,659],[466,608],[512,537],[580,405],[638,308],[732,184],[763,157],[780,150],[970,92]]],"sha":"e8ea8370c0bcf6e86b28a3454c7ce2648a2103e5"},"梦":{"medians":[[[193,637],[212,632],[262,635],[411,670],[464,672]],[[323,802],[350,781],[364,760],[344,456],[349,409]],[[328,619],[318,611],[307,573],[258,503],[214,451],[146,389]],[[394,588],[456,544],[469,518]],[[514,666],[578,660],[678,678],[757,700],[806,699]],[[616,841],[629,834],[657,800],[643,572],[640,459],[645,417]],[[662,648],[622,622],[588,567],[528,496],[457,442]],[[673,647],[678,622],[708,581],[809,472],[883,450],[925,444]],[[422,417],[435,396],[438,374],[401,330],[279,219],[204,174]],[[444,333],[523,336],[618,352],[643,347],[660,326],[586,184],[511,85],[458,36],[381,-16],[331,-39],[273,-54]],[[359,255],[374,251],[427,213],[444,193],[454,168]]],"sha":"3ea1f8dbba5bc6c2467ab060c2103bc5e9b36d21"}};
const BRUSH_ATLAS = {"横:起点":{"n":54,"chars":29,"width":34,"profile":[0.6912,0.7736,0.8356,0.8837,0.9388,0.9838,1.041,1.116,1.1521],"bend":-0.00489,"pass":true},"横:终点":{"n":53,"chars":29,"width":38.053,"profile":[0.8089,0.8859,0.9245,0.952,0.9861,1,1.0056,1.0146,1.0214],"bend":-0.0198,"pass":true},"竖:起点":{"n":46,"chars":33,"width":29.866,"profile":[0.6918,0.7903,0.8195,0.872,0.9127,0.9843,1.0719,1.1341,1.1712],"bend":0.00917,"pass":true},"竖:终点":{"n":40,"chars":30,"width":22,"profile":[0.5981,0.7121,0.7872,0.8538,0.9236,0.9752,1.0841,1.1616,1.271],"bend":-0.00774,"pass":true},"撇:起点":{"n":4,"chars":4,"width":30.003,"profile":[0.4819,0.5607,0.6433,0.7624,0.8604,0.9563,1.1326,1.3496,1.5623],"bend":0.08479,"pass":false},"撇:终点":{"n":6,"chars":6,"width":10.303,"profile":[0.2425,0.4925,0.6593,0.7984,0.886,0.9462,1.0856,1.2594,1.3857],"bend":-0.01353,"pass":true},"捺:起点":{"n":16,"chars":13,"width":29.345,"profile":[0.6205,0.7149,0.7654,0.8255,0.947,0.9819,1.1044,1.1931,1.2582],"bend":0.03379,"pass":true},"捺:终点":{"n":24,"chars":20,"width":36.508,"profile":[0.7116,0.7923,0.8396,0.896,0.9384,0.9808,1.0576,1.1124,1.1663],"bend":-0.01019,"pass":true},"点:起点":{"n":6,"chars":4,"width":29.267,"profile":[0.6662,0.7541,0.8073,0.9161,0.9269,1.0143,1.0814,1.1067,1.0696],"bend":0.03086,"pass":true},"点:终点":{"n":3,"chars":2,"width":27.785,"profile":[0.6518,0.7231,0.767,0.9039,0.9269,0.9835,1.0628,1.0427,1.0571],"bend":-0.05,"pass":false},"折:起点":{"n":10,"chars":10,"width":35.464,"profile":[0.5792,0.6719,0.7557,0.8202,0.89,0.9676,1.078,1.1648,1.2956],"bend":0.031,"pass":true},"折:终点":{"n":6,"chars":6,"width":13.893,"profile":[0.4717,0.6263,0.7954,0.8673,0.9494,0.9775,1.0925,1.1419,1.3074],"bend":-0.00877,"pass":true},"钩:起点":{"n":13,"chars":12,"width":28.636,"profile":[0.799,0.8771,0.9193,0.9224,0.9545,1,1.0363,1.0525,1.0051],"bend":0.01247,"pass":true},"钩:终点":{"n":13,"chars":13,"width":21.633,"profile":[0.4298,0.5547,0.625,0.7656,0.8618,0.9587,1.1065,1.25,1.3391],"bend":-0.02687,"pass":true},"横:起点:中":{"n":45,"chars":26,"width":33.526,"profile":[0.6707,0.7685,0.8246,0.8825,0.9318,0.9854,1.0463,1.1365,1.1744],"bend":-0.00489,"pass":true},"横:终点:中":{"n":42,"chars":25,"width":38.471,"profile":[0.8582,0.913,0.9511,0.9777,0.9968,1,1,1,1],"bend":-0.02353,"pass":true},"竖:起点:中":{"n":30,"chars":26,"width":31.048,"profile":[0.7397,0.8009,0.8435,0.8759,0.913,0.9885,1.0655,1.1315,1.1508],"bend":0.00917,"pass":true},"竖:终点:中":{"n":17,"chars":14,"width":20,"profile":[0.5963,0.7071,0.7837,0.8515,0.9372,0.9768,1.067,1.1785,1.2727],"bend":-0.01379,"pass":true},"捺:终点:中":{"n":7,"chars":7,"width":27.857,"profile":[0.7368,0.7808,0.8186,0.8615,0.9054,0.9765,1.1107,1.244,1.3413],"bend":0,"pass":true},"竖:起点:左":{"n":14,"chars":14,"width":26.683,"profile":[0.5759,0.6404,0.7092,0.838,0.9035,0.9744,1.0926,1.1993,1.1993],"bend":0.00917,"pass":true},"竖:终点:左":{"n":21,"chars":20,"width":24,"profile":[0.6009,0.7211,0.7925,0.856,0.8944,0.9751,1.088,1.1662,1.2806],"bend":-0.00671,"pass":true},"钩:起点:中":{"n":8,"chars":7,"width":28.636,"profile":[0.7906,0.858,0.879,0.8907,0.9501,1,1.0363,1.0526,1.0051],"bend":-0.00445,"pass":true},"捺:起点:右":{"n":9,"chars":9,"width":29.53,"profile":[0.6087,0.7041,0.7674,0.8188,0.9303,0.965,1.1028,1.2079,1.331],"bend":0.03846,"pass":true},"捺:终点:右":{"n":11,"chars":11,"width":26,"profile":[0.6679,0.7454,0.7683,0.8771,0.9358,0.9791,1.0463,1.1402,1.1926],"bend":-0.00962,"pass":true},"横:终点:左":{"n":7,"chars":5,"width":34,"profile":[0.595,0.6863,0.7844,0.8886,0.9748,1,1.1237,1.1237,1.129],"bend":-0.00489,"pass":true},"钩:终点:中":{"n":8,"chars":8,"width":16,"profile":[0.4298,0.5203,0.6309,0.7616,0.8571,0.9518,1.1019,1.2206,1.2778],"bend":-0.048,"pass":true},"折:起点:中":{"n":7,"chars":7,"width":34.928,"profile":[0.5657,0.6679,0.7545,0.7919,0.8838,0.9617,1.1031,1.2661,1.3508],"bend":0.03846,"pass":true}};
const TRAINING_COUNT = 48;
const TRAINED_ENDPOINTS = 294;
const FROZEN_HOLDOUTS = ['泉','清风入梦'];
const LABEL_FONT={family:'LXGW WenKai',style:'Regular'};
const ORACLE_FONT={family:'Ma Shan Zheng',style:'Regular'};
const PAGE_NAME='R5真实原型迁移｜泉·清风入梦｜20261026';
const pathRound=(v)=>Number(v).toFixed(2);
function role_of_stroke(stroke){
 const pts=stroke.map(p=>[p[0],-p[1]]);
 const steps=[];let length=0;
 for(let i=1;i<pts.length;i++){let dx=pts[i][0]-pts[i-1][0],dy=pts[i][1]-pts[i-1][1];let l=Math.hypot(dx,dy);steps.push([dx,dy]);length+=l;}
 const dx=pts[pts.length-1][0]-pts[0][0],dy=pts[pts.length-1][1]-pts[0][1];
 if(length<95||(length<135&&Math.hypot(dx,dy)<80))return '点';
 const turns=[];
 for(let i=1;i<steps.length;i++){const a=steps[i-1],b=steps[i];let m=Math.hypot(...a)*Math.hypot(...b),c=(a[0]*b[0]+a[1]*b[1])/Math.max(.0001,m);turns.push(Math.acos(Math.max(-1,Math.min(1,c)))*180/Math.PI);}
 if(turns.length>1&&Math.max(...turns.slice(-2))>52&&length>130)return '钩';
 if(turns.length&&Math.max(...turns)>57)return '折';
 if(Math.abs(dx)>Math.abs(dy)*1.6)return '横';
 if(Math.abs(dy)>Math.abs(dx)*1.8)return '竖';
 if(dx<0)return '撇';
 return '捺';
}
function prepare(ch){
 const strokes=TARGET_DATA[ch].medians;
 if(!Array.isArray(strokes)||!strokes.length)throw Error('NO_TARGET_DATA_'+ch);
 const points=strokes.flat();const minX=Math.min(...points.map(x=>x[0])),maxX=Math.max(...points.map(x=>x[0]));
 const minY=Math.min(...points.map(x=>x[1])),maxY=Math.max(...points.map(x=>x[1]));
 const s=870/Math.max(maxX-minX,maxY-minY),dx=(1024-(maxX-minX)*s)/2,dy=(1024-(maxY-minY)*s)/2;
 return strokes.map(raw=>{
  const v=raw.map(p=>[dx+(p[0]-minX)*s,dy+(maxY-p[1])*s]);
  const mid=v[Math.floor(v.length/2)];
  const position=mid[0]<358?'左':mid[0]>666?'右':'中';
  return {original:raw,p:v,role:role_of_stroke(raw),position,length:v.slice(1).reduce((x,p,i)=>x+Math.hypot(p[0]-v[i][0],p[1]-v[i][1]),0)};
 });
}
function smooth(path){
 if(path.length<2)return path;
 const out=[];const p=path;
 for(let i=0;i<p.length-1;i++){
  const p0=p[Math.max(0,i-1)],p1=p[i],p2=p[i+1],p3=p[Math.min(p.length-1,i+2)];
  const dist=Math.hypot(p2[0]-p1[0],p2[1]-p1[1]),n=Math.max(4,Math.ceil(dist/5));
  const t1=[(p2[0]-p0[0])*.37,(p2[1]-p0[1])*.37],t2=[(p3[0]-p1[0])*.37,(p3[1]-p1[1])*.37];
  for(let j=0;j<n;j++){
   const t=j/n,tt=t*t,ttt=tt*t,a=2*ttt-3*tt+1,b=ttt-2*tt+t,c=-2*ttt+3*tt,d=ttt-tt;
   out.push([a*p1[0]+b*t1[0]+c*p2[0]+d*t2[0],a*p1[1]+b*t1[1]+c*p2[1]+d*t2[1]]);
  }
 }
 out.push(p[p.length-1]);return out;
}
function shapeInfo(role,kind,pos,stats){
 const spec=BRUSH_ATLAS[role+':'+kind+':'+pos];
 if(spec&&spec.pass){stats.exactRolePosition++;return spec;}
 const pure=BRUSH_ATLAS[role+':'+kind];
 if(pure&&pure.pass){stats.roleOnly++;return pure;}
 stats.fallback++;
 const arr=Object.entries(BRUSH_ATLAS).filter(([k,v])=>v.pass&&k.endsWith(':'+kind)&&k.split(':').length===2);
 if(!arr.length)throw Error('NO_SAFE_ROLE_FALLBACK');
 const a=arr.map(x=>x[1]);
 const ix=Math.floor(a.length/2);
 return {width:a[ix].width,profile:a[ix].profile,bend:0,pass:false};
}
const sourceProfiles=[0,2,4,6,8,10,14,18,22];
function capProfile(profile,d){
 const sourceDist=d*.5;
 if(sourceDist>=29)return 1;
 if(sourceDist>=22){const tail=profile[8];return tail+(1-tail)*(sourceDist-22)/7;}
 if(sourceDist<=0)return profile[0];
 for(let i=0;i<sourceProfiles.length-1;i++){
  const a=sourceProfiles[i],b=sourceProfiles[i+1];
  if(a<=sourceDist&&sourceDist<=b){
   const f=(sourceDist-a)/(b-a);
   return profile[i]+(profile[i+1]-profile[i])*f;
  }
 }
 return 1;
}
function polygonPath(points){
 if(points.length<3)return '';
 return 'M'+points.map(p=>pathRound(p[0])+' '+pathRound(p[1])).join(' L')+' Z';
}
function vectorStroke(path,body,capS,capE,variant){
 const p=smooth(path);
 const s=[0];for(let i=1;i<p.length;i++)s[i]=s[i-1]+Math.hypot(p[i][0]-p[i-1][0],p[i][1]-p[i-1][1]);
 const total=s[s.length-1],left=[],right=[];
 for(let i=0;i<p.length;i++){
  const a=p[Math.max(0,i-1)],b=p[Math.min(i+1,p.length-1)];
  const dx=b[0]-a[0],dy=b[1]-a[1],len=Math.max(.0001,Math.hypot(dx,dy));
  const nx=-dy/len,ny=dx/len,dist=s[i],rem=total-dist;
  let width=body,shift=0;
  if(variant==='B'){
   width*=.25+.75*Math.pow(Math.sin(Math.PI*Math.min(.999,Math.max(.001,dist/Math.max(total,1)))),.45);
  }
  if(variant==='C'){
   width*=Math.max(.18,Math.min(1.8,Math.min(capProfile(capS.profile,dist),capProfile(capE.profile,rem))));
   const smoothW=Math.max(0,1-dist/52),smoothE=Math.max(0,1-rem/52);
   shift=body*(capS.bend*smoothW-capE.bend*smoothE)*1.8;
  }
  const px=p[i][0]+shift*nx,py=p[i][1]+shift*ny;
  left.push([px+nx*width*.5,py+ny*width*.5]);
  right.push([px-nx*width*.5,py-ny*width*.5]);
 }
 return polygonPath(left.concat(right.reverse()));
}
function glyphMarkup(ch,variant,stats,pixels){
 const strokes=prepare(ch),lengths=strokes.map(x=>x.length).sort((a,b)=>b-a),base=41;
 const content=[];
 if(variant==='A'){
  for(const stroke of strokes){const p=smooth(stroke.p);content.push('<path d="M'+p.map(v=>pathRound(v[0])+' '+pathRound(v[1])).join(' L')+'" fill="none" stroke="#171717" stroke-width="'+base+'" stroke-linecap="round" stroke-linejoin="round"/>');}
 }else{
  for(const stroke of strokes){
   let body=base,start=null,end=null;
   if(variant==='B'){
    body=base*(stroke.length>=lengths[Math.min(2,lengths.length-1)]?1.40:stroke.length>=lengths[Math.min(5,lengths.length-1)]?1.04:.78);
   }else{
    start=shapeInfo(stroke.role,'起点',stroke.position,stats);
    end=shapeInfo(stroke.role,'终点',stroke.position,stats);
    body=(start.width+end.width)*.84;
    const dense=strokes.length>9?Math.sqrt(9/strokes.length):1;
    body=Math.max(22,Math.min(80,body*dense));
   }
   const shape=vectorStroke(stroke.p,body,start,end,variant);
   content.push('<path d="'+shape+'" fill="#171717"/>');
  }
 }
 return '<svg xmlns="http://www.w3.org/2000/svg" width="'+pixels+'" height="'+pixels+'" viewBox="0 0 1024 1024">'+content.join('')+'</svg>';
}
function label(parent,str,x,y,size){
 const node=figma.createText();parent.appendChild(node);node.fontName=LABEL_FONT;node.fontSize=size;node.characters=str;node.fills=[{type:'SOLID',color:{r:.18,g:.18,b:.18}}];node.textAutoResize='WIDTH_AND_HEIGHT';node.x=x;node.y=y;return node;
}
function frame(parent,name,x,y,w,h,color){
 const f=figma.createFrame();parent.appendChild(f);f.name=name;f.resize(w,h);
 f.fills=[{type:'SOLID',color}];f.x=x;f.y=y;return f;
}
function placeGlyph(panel,ch,varName,x,y,size,stats){
 const obj=figma.createNodeFromSvg(glyphMarkup(ch,varName,stats,size));
 panel.appendChild(obj);obj.name=varName+'_'+ch+'_可编辑矢量';obj.x=x;obj.y=y;
 return obj.id;
}
const existing=figma.root.children.find(n=>n.type==='PAGE'&&n.name===PAGE_NAME);
if(existing)return {status:'EXISTS_PRESERVED_FOR_REVIEW',page:existing.id,frames:existing.children.map(x=>({id:x.id,name:x.name}))};
const fonts=await figma.listAvailableFontsAsync();
const oraclePresent=fonts.some(f=>f.fontName.family===ORACLE_FONT.family&&f.fontName.style===ORACLE_FONT.style);
const labelPresent=fonts.some(f=>f.fontName.family===LABEL_FONT.family&&f.fontName.style===LABEL_FONT.style);
if(!oraclePresent||!labelPresent)throw Error('FONT_MISSING_MASHAN_OR_LABEL');
await Promise.all([figma.loadFontAsync(LABEL_FONT),figma.loadFontAsync(ORACLE_FONT)]);
const page=figma.createPage();page.name=PAGE_NAME;await figma.setCurrentPageAsync(page);
const bg={r:.970,g:.965,b:.955},white={r:1,g:1,b:1};
const board=frame(page,'冻结四路对照板_只供诊断',160,100,3550,1790,bg);
label(board,'R5 / 真实笔画原型迁移',80,48,56);
label(board,'48个训练字 → 294条端部样本　｜　未见：泉 / 清风入梦　｜　无真人审美通过',85,128,25);
const heads=['A 结构基线','B R2旧笔宽','C R5真实端笔','D 原字体参照'];
const explanation=['同一标准笔画中心线','长度分级+统一收尖','来源实测端笔+角色定位','只供质量对照，不参与C'];
const ids=[],stats={exactRolePosition:0,roleOnly:0,fallback:0};
for(let col=0;col<4;col++){
 const x=60+col*866;
 const panel1=frame(board,'R5_'+String(col)+'_单字泉',x,240,820,665,white);
 const panel2=frame(board,'R5_'+String(col)+'_清风入梦',x,975,820,665,white);
 label(panel1,heads[col],34,30,31);label(panel2,heads[col],34,30,31);
 label(panel1,explanation[col],35,92,20);label(panel2,explanation[col],35,92,20);
 if(col!==3){
  ids.push(placeGlyph(panel1,'泉','ABC'[col],132,120,555,stats));
  const words='清风入梦';
  for(let i=0;i<words.length;i++)ids.push(placeGlyph(panel2,words[i],'ABC'[col],32+i*194,190,187,stats));
 }else{
  const single=figma.createText();panel1.appendChild(single);single.fontName=ORACLE_FONT;single.fontSize=475;single.characters='泉';single.fills=[{type:'SOLID',color:{r:.08,g:.08,b:.08}}];single.textAutoResize='WIDTH_AND_HEIGHT';single.x=(820-single.width)/2;single.y=170;ids.push(single.id);
  const word=figma.createText();panel2.appendChild(word);word.fontName=ORACLE_FONT;word.fontSize=166;word.characters='清风入梦';word.fills=[{type:'SOLID',color:{r:.08,g:.08,b:.08}}];word.textAutoResize='WIDTH_AND_HEIGHT';word.x=(820-word.width)/2;word.y=260;ids.push(word.id);
 }
}
label(board,'锁定对照：同字、同结构、同画幅。C只取训练字端笔统计，D不参与C设计。形态不同 ≠ 艺术品质更高。',90,1717,20);
return {status:'R5_REAL_UNSEEN_A_B_C_D_RENDERED_UNREVIEWED',fileKey:'uyDxOoN1iNDPpEHTKSUWg1',pageId:page.id,boardId:board.id,sourceAtlasHash:'3b28f265b9fa5eeaef0999a843792020282f3b89',appliedTerminalMatching:stats,createdGlyphNodes:ids,train:TRAINING_COUNT,exemplars:TRAINED_ENDPOINTS,targets:FROZEN_HOLDOUTS,oracleOnly:true,approval:'TECHNICAL_REVIEW_REQUIRED'};
