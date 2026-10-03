// Compose the one image_gen text-cleanup result over the frozen original, within explicit neighborhoods.
// This performs masking and alpha composition only; no image synthesis, inpainting, resampling or color grading.
const fs=require('fs'),crypto=require('crypto'),{PNG}=require('pngjs');
const a={};for(let i=2;i<process.argv.length;i+=2)a[process.argv[i].replace(/^--/,'')]=process.argv[i+1];
for(const k of ['source','material','out','overlay','receipt','mask'])if(!a[k])throw Error('Missing '+k);
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const sourceBytes=fs.readFileSync(a.source),materialBytes=fs.readFileSync(a.material);
if(sha(sourceBytes)!=='e7af9c9e88ff9dd38357a570305c4b5d40e98678d14c174957d4bdf2e7bdfd29'||sha(materialBytes)!=='01faebaaee47f8c42cd4aad96225fe23bf610655e5b457877a1b91c0197c9748')throw Error('Wrong frozen inputs');
const s=PNG.sync.read(sourceBytes),m=PNG.sync.read(materialBytes);if(s.width!==1536||s.height!==1024||m.width!==1536||m.height!==1024)throw Error('Wrong dimensions');
// The transition lies inside these declared envelopes. It never reaches cup, plate, moss or foreground leaves.
const regions=[['wordmark',74,64,434,336],['hero',870,105,1504,375],['small_copy',903,372,1039,507],['english',1322,66,1514,182],['footer',1323,860,1511,978]];
const feather=20,alpha=new Uint8Array(1536*1024),final=new PNG({width:1536,height:1024}),overlay=new PNG({width:1536,height:1024});final.data=Buffer.from(s.data);
for(const [name,x0,y0,x1,y1] of regions)for(let y=y0;y<y1;y++)for(let x=x0;x<x1;x++){const dist=Math.min(x-x0+.5,x1-x-.5,y-y0+.5,y1-y-.5),t=Math.min(1,Math.max(0,dist/feather)),v=Math.round(255*t*t*(3-2*t));alpha[y*1536+x]=Math.max(alpha[y*1536+x],v);}
let allowed=0,changed=0,protectedPixels=0,outsideChanged=0,maxOutside=0;
for(let p=0;p<alpha.length;p++){const i=p*4,al=alpha[p];if(al){allowed++;for(let c=0;c<3;c++){overlay.data[i+c]=m.data[i+c];final.data[i+c]=Math.round((m.data[i+c]*al+s.data[i+c]*(255-al))/255);}overlay.data[i+3]=al;final.data[i+3]=255;if([0,1,2].some(c=>final.data[i+c]!==s.data[i+c]))changed++;}else{protectedPixels++;overlay.data[i+3]=0;}}
const finalBytes=PNG.sync.write(final,{colorType:2,inputColorType:6}),overlayBytes=PNG.sync.write(overlay,{colorType:6});const check=PNG.sync.read(finalBytes);
for(let p=0;p<alpha.length;p++)if(!alpha[p]){const i=p*4;let diff=false;for(let c=0;c<3;c++){const d=Math.abs(check.data[i+c]-s.data[i+c]);maxOutside=Math.max(maxOutside,d);diff ||= d!==0;}if(diff)outsideChanged++;}
if(outsideChanged||maxOutside)throw Error('Protection failed');
for(const [name,x0,y0,x1,y1] of [['cup',320,549,754,830],['plate',750,606,1320,809],['moss',0,410,320,750],['central_stream',1040,507,1410,606]])for(let y=y0;y<y1;y++)for(let x=x0;x<x1;x++)if(alpha[y*1536+x])throw Error('Protected subject overlap: '+name);
fs.writeFileSync(a.out,finalBytes);fs.writeFileSync(a.overlay,overlayBytes);
const mask={source_sha256:sha(sourceBytes),material_sha256:sha(materialBytes),dimensions:[1536,1024],envelopes:regions,feather_px:feather,mask_pixels:allowed,mask_percent:allowed/1572864*100,definition:'Smoothstep alpha within declared text neighborhoods; zero outside; no pixel resizing',affected_background_is_reconstruction:true,hidden_original_recovered:false};fs.writeFileSync(a.mask,JSON.stringify(mask,null,2)+'\n');
const receipt={operation:'ONE_IMAGEGEN_EDIT_PLUS_SOURCE_PRESERVING_ALPHA_COMPOSITION',source:{path:a.source,sha256:sha(sourceBytes)},material:{path:a.material,sha256:sha(materialBytes)},output:{path:a.out,sha256:sha(finalBytes),bytes:finalBytes.length,dimensions:[1536,1024]},editable_overlay:{path:a.overlay,sha256:sha(overlayBytes),bytes:overlayBytes.length,dimensions:[1536,1024],alpha:true},mask:{path:a.mask,sha256:sha(fs.readFileSync(a.mask))},mask_pixels:allowed,mask_pixels_changed:changed,protected_pixels_compared:protectedPixels,protected_pixels_changed:outsideChanged,protected_max_channel_difference:maxOutside,protected_subject_rectangles_checked:['cup','plate','moss','central_stream'],hidden_original_recovered:false,formal_poster_versions_added:0,new_generation_by_this_script:false,dependency:{name:'pngjs',version:require('pngjs/package.json').version,license:require('pngjs/package.json').license}};fs.writeFileSync(a.receipt,JSON.stringify(receipt,null,2)+'\n');process.stdout.write(JSON.stringify(receipt));
