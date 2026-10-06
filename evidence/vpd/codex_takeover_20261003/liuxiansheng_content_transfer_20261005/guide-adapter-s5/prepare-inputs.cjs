// S4 technical mask extraction only. Original package and input files are read-only.
// Geometry edits and orange centerline reconstruction are in build-wordmark.py.
const fs = require('fs'), path = require('path'), crypto = require('crypto');
const sharp = require('C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
function cliOption(flag){const i=process.argv.indexOf(flag);if(i<0)return null;if(!process.argv[i+1]||process.argv[i+1].startsWith('--'))throw new Error('Missing value for '+flag);return process.argv[i+1];}
function findRepository(start){let p=path.resolve(start);while(true){if(fs.existsSync(path.join(p,'PROJECT_CONTROL_ADAPTER.json')))return p;const q=path.dirname(p);if(q===p)throw new Error('No PROJECT_CONTROL_ADAPTER.json ancestor; pass --root');p=q;}}
const ROOT = cliOption('--root')?path.resolve(cliOption('--root')):findRepository(__dirname);
if(!fs.existsSync(path.join(ROOT,'PROJECT_CONTROL_ADAPTER.json')))throw new Error('Explicit --root lacks PROJECT_CONTROL_ADAPTER.json');
const BASE = cliOption('--output-dir')?path.resolve(cliOption('--output-dir')):__dirname;
const SOURCE = path.join(ROOT, '.liu-visual-private/liuxiansheng_transfer_20261005/IMAGE_GUIDE_S4.png');
const REFERENCE = path.join(ROOT, '.liu-visual-private/product-type-integration-20261004/SHANYEJI-canonical-readback-20261005.jpg');
const EXPECTED_G = '9ef09dd1814343a938445227ce9a8906f0eb1ae4531a857baaba0720606aa558';
const EXPECTED_R = '9a29fbdc7dd908017924bed270e8dfe18351519eed3fa7bc7001789f2a383414';
const COPY_MANIFEST = path.join(ROOT,'evidence/vpd/codex_takeover_20261003/liuxiansheng_content_transfer_20261005/COPY_MANIFEST.json');
const EXPECTED_COPY = 'a94dfbcbe831a34ca17c3069c57109d0bfdf6cc667b65f26b8e4a80cc6654f3a';
const ROI = [220, 468, 1021, 776];
const BRIDGE_WINDOWS = [
  {id:'XIAN_VERTICAL', box:[585,565,645,598]},
  {id:'XIAN_MIDDLE_BAR', box:[603,585,667,632]},
  {id:'XIAN_RIGHT_FOOT', box:[681,661,722,698]},
  {id:'SHENG_UPPER_BAR', box:[824,535,938,590]},
  {id:'SHENG_MIDDLE_LEFT', box:[781,605,836,672]},
  {id:'SHENG_MIDDLE_RIGHT', box:[883,612,938,676]},
  {id:'SHENG_BOTTOM_BAR', box:[758,674,956,718]},
];
const hash = b => crypto.createHash('sha256').update(b).digest('hex');
function bounds(mask, w, h) {
  let x0=w,y0=h,x1=0,y1=0,n=0;
  for(let p=0;p<mask.length;p++) if(mask[p]) {
    const x=p%w,y=Math.floor(p/w);x0=Math.min(x0,x);y0=Math.min(y0,y);
    x1=Math.max(x1,x+1);y1=Math.max(y1,y+1);n++;
  }
  return {pixels:n, box:[x0,y0,x1,y1]};
}
function cleanComponents(mask,w,h,minArea) {
  const seen=new Uint8Array(mask.length), keep=new Uint8Array(mask.length),queue=new Int32Array(mask.length),records=[];
  let removedCount=0, removedPixels=0;
  for(let p=0;p<mask.length;p++) {
    if(!mask[p]||seen[p]) continue;
    let head=0,tail=0,x0=w,y0=h,x1=0,y1=0;queue[tail++]=p;seen[p]=1;
    while(head<tail) {
      const q=queue[head++],x=q%w,y=Math.floor(q/w);
      x0=Math.min(x0,x);y0=Math.min(y0,y);x1=Math.max(x1,x+1);y1=Math.max(y1,y+1);
      for(let yy=Math.max(0,y-1);yy<=Math.min(h-1,y+1);yy++) for(let xx=Math.max(0,x-1);xx<=Math.min(w-1,x+1);xx++) {
        const n=yy*w+xx;
        if(mask[n]&&!seen[n]){seen[n]=1;queue[tail++]=n;}
      }
    }
    if(tail<minArea){removedCount++;removedPixels+=tail;continue;}
    records.push({pixels:tail, box:[x0,y0,x1,y1]});
    for(let j=0;j<tail;j++) keep[queue[j]]=1;
  }
  records.sort((a,b)=>b.pixels-a.pixels);
  return {mask:keep,records,removed_count:removedCount,removed_pixels:removedPixels};
}
function summarizeColor(mask,raw) {
  const channels=[[],[],[]];
  for(let p=0;p<mask.length;p++)if(mask[p])for(let c=0;c<3;c++)channels[c].push(raw[p*4+c]);
  const rgb=channels.map(v=>{v.sort((a,b)=>a-b);return v[Math.floor(v.length/2)];});
  return {median_rgb:rgb, flat_color:'#'+rgb.map(v=>v.toString(16).padStart(2,'0')).join('')};
}
function enclosedHoles(mask,w,h,raw,box) {
  const [x0,y0,x1,y1]=box,bw=x1-x0,bh=y1-y0,seen=new Uint8Array(bw*bh),queue=new Int32Array(bw*bh),holes=[];
  for(let p=0;p<bw*bh;p++){
    const sx=p%bw+x0,sy=Math.floor(p/bw)+y0;
    if(mask[sy*w+sx]||seen[p])continue;
    let head=0,tail=0,edge=false,mx0=bw,my0=bh,mx1=0,my1=0,opaqueOrange=0;
    const alpha=[],rgb=[[],[],[]];queue[tail++]=p;seen[p]=1;
    while(head<tail){
      const q=queue[head++],x=q%bw,y=Math.floor(q/bw),i=((y+y0)*w+x+x0)*4;
      edge ||= x===0||x===bw-1||y===0||y===bh-1;
      mx0=Math.min(mx0,x);my0=Math.min(my0,y);mx1=Math.max(mx1,x+1);my1=Math.max(my1,y+1);
      alpha.push(raw[i+3]);for(let c=0;c<3;c++)rgb[c].push(raw[i+c]);
      if(raw[i+3]>=192&&raw[i]>=235&&raw[i+1]>=70&&raw[i+1]<=182&&raw[i+2]<=64)opaqueOrange++;
      for(let yy=Math.max(0,y-1);yy<=Math.min(bh-1,y+1);yy++)for(let xx=Math.max(0,x-1);xx<=Math.min(bw-1,x+1);xx++){
        const n=yy*bw+xx;
        if(!mask[(yy+y0)*w+xx+x0]&&!seen[n]){seen[n]=1;queue[tail++]=n;}
      }
    }
    if(edge)continue;
    alpha.sort((a,b)=>a-b);rgb.forEach(v=>v.sort((a,b)=>a-b));
    holes.push({area:tail,box:[mx0+x0,my0+y0,mx1+x0,my1+y0],alpha_min_median_max:[alpha[0],alpha[Math.floor(tail/2)],alpha[tail-1]],median_rgb:rgb.map(v=>v[Math.floor(tail/2)]),opaque_orange_pixels:opaqueOrange,source_pixel_positions_xy:Array.from(queue.subarray(0,tail),q=>[q%bw+x0,Math.floor(q/bw)+y0])});
  }
  holes.sort((a,b)=>b.area-a.area);
  return {count:holes.length,pixels:holes.reduce((n,h)=>n+h.area,0),holes};
}
// The first hidden-orange render exposed actual high-alpha orange/cream edge
// mixtures outside the strict S3 color class. This correction is limited to
// the seven frozen windows and 3 source pixels from observed pure orange.
// All 61 enclosed original holes are explicitly excluded.
function actualOrangeEdgeMix(cream,orange,raw,w,h,grain){
  const mask=Uint8Array.from(orange),extra=new Uint8Array(w*h),protectedGrain=new Uint8Array(w*h),disc=[],colors=[[],[],[],[]];
  for(const hole of grain.holes)for(const [x,y] of hole.source_pixel_positions_xy)protectedGrain[y*w+x]=1;
  for(let dy=-3;dy<=3;dy++)for(let dx=-3;dx<=3;dx++)if(dx*dx+dy*dy<=9)disc.push([dx,dy]);
  for(const win of BRIDGE_WINDOWS)for(let y=win.box[1];y<win.box[3];y++)for(let x=win.box[0];x<win.box[2];x++){
    const p=y*w+x,i=p*4,R=raw[i],G=raw[i+1],B=raw[i+2],A=raw[i+3];
    if(cream[p]||orange[p]||protectedGrain[p]||A<192||R<235||G<70||G>235||B>218||R-G<15||G-B<15)continue;
    let near=false;for(const [dx,dy] of disc)if(orange[(y+dy)*w+x+dx]){near=true;break;}
    if(near&&!extra[p]){mask[p]=extra[p]=1;for(let c=0;c<4;c++)colors[c].push(raw[i+c]);}
  }
  return {mask,extra,protectedGrain,evidence:{classification:'ACTUAL_HIGH_ALPHA_ORANGE_CREAM_EDGE_MIX_NOT_ORIGINAL_WHITE',bounds:bounds(extra,w,h),rgba_min_median_max:colors.map(a=>{a.sort((a,b)=>a-b);return a.length?[a[0],a[Math.floor(a.length/2)],a.at(-1)]:null;}),source_gate:'A>=192,R>=235,70<=G<=235,B<=218,R-G>=15,G-B>=15; within 3px Euclidean distance of strict pure-orange and one frozen bridge window',protected_original_grain_components:grain.count,protected_original_grain_pixels:grain.pixels}};
}
// A 2px overlap with already measured cream supports trace joins. These pixels
// are not new white restoration: they were present in the source cream mask.
function bridgeTraceSupport(added,cream,w,h){
  const mask=Uint8Array.from(added),overlap=new Uint8Array(w*h),disc=[];
  for(let dy=-2;dy<=2;dy++)for(let dx=-2;dx<=2;dx++)if(dx*dx+dy*dy<=4)disc.push([dx,dy]);
  for(const win of BRIDGE_WINDOWS)for(let y=win.box[1];y<win.box[3];y++)for(let x=win.box[0];x<win.box[2];x++){
    const p=y*w+x;if(!cream[p]||mask[p])continue;
    for(const [dx,dy] of disc)if(added[(y+dy)*w+x+dx]){mask[p]=overlap[p]=1;break;}
  }
  return {mask,overlap,evidence:{classification:'TRACE_JOIN_OVERLAP_EXISTING_G_CREAM_NOT_NEW_RESTORATION',radius_source_px:2,...bounds(overlap,w,h)}};
}
// Disc morphology reads existing cream within a 16px margin. It can add cream only
// at measured orange pixels inside each frozen expert window. No global closing.
function localOrangeBridge(original,orange,w,h) {
  const result=Uint8Array.from(original),r=8,disc=[];
  for(let dy=-r;dy<=r;dy++)for(let dx=-r;dx<=r;dx++)if(dx*dx+dy*dy<=r*r)disc.push([dx,dy]);
  const operations=[];
  for(const win of BRIDGE_WINDOWS) {
    const [wx0,wy0,wx1,wy1]=win.box;
    const ex0=Math.max(0,wx0-2*r),ey0=Math.max(0,wy0-2*r),ex1=Math.min(w,wx1+2*r),ey1=Math.min(h,wy1+2*r);
    const ew=ex1-ex0,eh=ey1-ey0,dilated=new Uint8Array(ew*eh);
    for(let y=ey0;y<ey1;y++)for(let x=ex0;x<ex1;x++) {
      let value=0;
      for(const [dx,dy] of disc){const xx=x+dx,yy=y+dy;if(xx>=0&&xx<w&&yy>=0&&yy<h&&original[yy*w+xx]){value=1;break;}}
      dilated[(y-ey0)*ew+x-ex0]=value;
    }
    let additions=0;
    for(let y=wy0;y<wy1;y++)for(let x=wx0;x<wx1;x++){
      const p=y*w+x;if(original[p]||!orange[p])continue;
      let closed=1;
      for(const [dx,dy] of disc){const xx=x+dx-ex0,yy=y+dy-ey0;if(xx<0||xx>=ew||yy<0||yy>=eh||!dilated[yy*ew+xx]){closed=0;break;}}
      if(closed){if(!result[p])additions++;result[p]=1;}
    }
    operations.push({...win,disc_radius_source_px:r,unique_added_pixels_this_window:additions});
  }
  const added=new Uint8Array(original.length);let n=0;
  for(let p=0;p<added.length;p++)if(result[p]&&!original[p]){
    if(!orange[p])throw new Error('Bridge escaped the measured orange mask');
    const x=p%w,y=Math.floor(p/w);
    if(!BRIDGE_WINDOWS.some(win=>x>=win.box[0]&&x<win.box[2]&&y>=win.box[1]&&y<win.box[3]))throw new Error('Bridge escaped frozen windows');
    added[p]=1;n++;
  }
  return {mask:result,added,operations,added_pixels:n};
}
async function binaryPNG(mask,w,h,name) {
  const binary=Buffer.alloc(mask.length);
  for(let i=0;i<mask.length;i++)binary[i]=mask[i]?0:255;
  await sharp(binary,{raw:{width:w,height:h,channels:1}}).png().toFile(path.join(BASE,name));
}
function pointInPolygon(x,y,points){let inside=false;for(let i=0,j=points.length-1;i<points.length;j=i++){const [xi,yi]=points[i],[xj,yj]=points[j];if((yi>y)!==(yj>y)&&x<(xj-xi)*(y-yi)/(yj-yi)+xi)inside=!inside;}return inside;}
function recoverShengCrossing(bridge,cream,supportedOrange,protectedGrain,w,h,spec){
  const polygon=spec.polygon,additions=new Uint8Array(w*h);let added=0;
  const xs=polygon.map(p=>p[0]),ys=polygon.map(p=>p[1]);
  for(let y=Math.min(...ys);y<Math.max(...ys);y++)for(let x=Math.min(...xs);x<Math.max(...xs);x++){
    const p=y*w+x;if(bridge.mask[p]||cream[p]||!supportedOrange[p]||protectedGrain[p]||!pointInPolygon(x+.5,y+.5,polygon))continue;
    bridge.mask[p]=bridge.added[p]=additions[p]=1;added++;
  }
  bridge.added_pixels+=added;
  return {mask:additions,evidence:{classification:'EXPERT_INFERRED_SHENG_BASE_CROSSING_RECOVERY',original_source_white:false,polygon,original_bottom_window:spec.original_window,revised_bottom_window:spec.revised_window,closing_condition_exception:'Only inside Q at actual pure-orange/approved high-alpha mixed-edge pixels; grain excluded',unique_added_pixels:added,...bounds(additions,w,h),visible_source_cream_anchors:spec.anchors}};
}
(async()=>{
  const frozen=JSON.parse(fs.readFileSync(path.join(BASE,'FROZEN_SPEC.json'),'utf8'));
  const g=fs.readFileSync(SOURCE),r=fs.readFileSync(REFERENCE),copy=fs.readFileSync(COPY_MANIFEST);
  if(hash(g)!==EXPECTED_G||hash(r)!==EXPECTED_R||hash(copy)!==EXPECTED_COPY)throw new Error('Frozen reference/guide byte identity failed');
  const {data,info}=await sharp(g).ensureAlpha().raw().toBuffer({resolveWithObject:true});
  const w=info.width,h=info.height;
  if(w!==1086||h!==1448)throw new Error('Frozen source canvas identity failed');
  const cream=new Uint8Array(w*h),orange=new Uint8Array(w*h),alphaHistogram={zero:0,low_1_63:0,mid_64_199:0,high_200_255:0};
  for(let p=0;p<cream.length;p++){const a=data[p*4+3];alphaHistogram[a===0?'zero':a<64?'low_1_63':a<200?'mid_64_199':'high_200_255']++;}
  for(let y=ROI[1];y<ROI[3];y++)for(let x=ROI[0];x<ROI[2];x++){
    const p=y*w+x,i=p*4,R=data[i],G=data[i+1],B=data[i+2],A=data[i+3];
    if(A>=200&&R>=232&&G>=224&&B>=205&&B<=246&&Math.abs(R-G)<=25&&G-B<=50)cream[p]=1;
    if(A>=192&&R>=235&&G>=70&&G<=182&&B<=64&&R-G>=70&&G-B>=25)orange[p]=1;
  }
  const c=cleanComponents(cream,w,h,150),o=cleanComponents(orange,w,h,25);
  const grain=enclosedHoles(c.mask,w,h,data,[246,478,963,747]);
  const edgeMix=actualOrangeEdgeMix(c.mask,o.mask,data,w,h,grain);
  const bridge=localOrangeBridge(c.mask,edgeMix.mask,w,h);
  for(let p=0;p<bridge.added.length;p++)if(bridge.added[p]&&edgeMix.protectedGrain[p])throw new Error('Bridge attempted to fill measured original grain');
  const crossing=recoverShengCrossing(bridge,c.mask,edgeMix.mask,edgeMix.protectedGrain,w,h,frozen.sheng_base_local_revision);
  const traceSupport=bridgeTraceSupport(bridge.added,c.mask,w,h);
  fs.writeFileSync(path.join(BASE,'CREAM_SOURCE_CLEAN.raw'),c.mask);
  fs.writeFileSync(path.join(BASE,'ORANGE_SOURCE_CLEAN.raw'),o.mask);
  fs.writeFileSync(path.join(BASE,'CREAM_BRIDGED.raw'),bridge.mask);
  fs.writeFileSync(path.join(BASE,'BRIDGE_ADDITIONS.raw'),bridge.added);
  fs.writeFileSync(path.join(BASE,'ORANGE_ACTUAL_EDGE_MIX.raw'),edgeMix.extra);
  fs.writeFileSync(path.join(BASE,'BRIDGE_TRACE_SUPPORT.raw'),traceSupport.mask);
  fs.writeFileSync(path.join(BASE,'SHENG_BASE_CROSSING_RECOVERY.raw'),crossing.mask);
  await binaryPNG(c.mask,w,h,'CREAM_SOURCE_TRACE_INPUT.png');
  await binaryPNG(traceSupport.mask,w,h,'BRIDGE_ADDITIONS_TRACE_INPUT.png');
  const facts={
    schema:'s4-mask-extraction/v1',status:'TECHNICAL_SOURCE_EXTRACTION_NOT_AESTHETIC_PASS',
    source:{path:SOURCE,sha256:hash(g),canvas:[w,h],actual_view_image:true},
    reference:{path:REFERENCE,sha256:hash(r),actual_view_image:true},
    copy_manifest:{path:COPY_MANIFEST,sha256:hash(copy),not_rendered_in_svg:true},
    roi_source_xyxy:ROI,alpha_histogram:alphaHistogram,
    threshold_source:'Same alpha/RGB class rules as prepare-trace-inputs.cjs from S3 implementation; this is preprocessing, not an aesthetic threshold.',
    cream_class:'A>=200,R>=232,G>=224,205<=B<=246,abs(R-G)<=25,G-B<=50',
    orange_class:'A>=192,R>=235,70<=G<=182,B<=64,R-G>=70,G-B>=25',
    component_neighbors:8,cream_min_component_area:150,orange_min_component_area:25,
    cream:{...bounds(c.mask,w,h),...summarizeColor(c.mask,data),retained_components:c.records,rejected_components:c.removed_count,rejected_pixels:c.removed_pixels,mask_sha256:hash(c.mask)},
    orange:{...bounds(o.mask,w,h),...summarizeColor(o.mask,data),retained_components:o.records,rejected_components:o.removed_count,rejected_pixels:o.removed_pixels,mask_sha256:hash(o.mask)},
    source_internal_grain:grain,
    bridge:{classification:'EXPERT_INFERRED_HIDDEN_CREAM_NOT_ORIGINAL_PIXELS',...bounds(bridge.added,w,h),added_pixels:bridge.added_pixels,operations:bridge.operations,mask_sha256:hash(bridge.mask),additions_sha256:hash(bridge.added),measured_mixed_edge_correction:edgeMix.evidence,original_cream_trace_overlap:traceSupport.evidence,sheng_base_local_revision:crossing.evidence,trace_support_mask_sha256:hash(traceSupport.mask),original_grain_overlap_pixels:0},
    limitations:[
      'Opaque class selection flattens original foreground shading and low-alpha fringe.',
      'Internal holes are selected from actual G pixels; alpha is binarized rather than preserved continuously.',
      'Local closing additions are inferred only at observed opaque orange pixels within frozen windows.',
      'No image-generation call, Figma write, business-state write, upstream modification or original guide write.'
    ]
  };
  fs.writeFileSync(path.join(BASE,'SOURCE_EXTRACTION.json'),JSON.stringify(facts,null,2)+'\n');
  console.log(JSON.stringify({cream:facts.cream.box,cream_components:c.records.length,orange_components:o.records.length,grain_holes:facts.source_internal_grain.count,grain_pixels:facts.source_internal_grain.pixels,bridge_additions:bridge.added_pixels,colors:[facts.cream.flat_color,facts.orange.flat_color]}));
})().catch(e=>{console.error(e.stack);process.exitCode=1;});
