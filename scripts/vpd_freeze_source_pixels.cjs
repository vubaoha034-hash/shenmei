// Mechanical export protection: preserve Figma's repair region and restore untouched source RGB.
// The actual image edit is performed by image_gen; this adds no generated or retouched content.
const fs = require('fs');
const crypto = require('crypto');
const {PNG} = require('pngjs');
const args={};for(let i=2;i<process.argv.length;i+=2)args[process.argv[i].replace(/^--/,'')]=process.argv[i+1];
for(const k of ['source','render','mask','out','receipt'])if(!args[k])throw Error('Missing '+k);
const digest=b=>crypto.createHash('sha256').update(b).digest('hex');
const sourceBytes=fs.readFileSync(args.source),rawBytes=fs.readFileSync(args.render),maskBytes=fs.readFileSync(args.mask);
const mask=JSON.parse(maskBytes),source=PNG.sync.read(sourceBytes),raw=PNG.sync.read(rawBytes);
if(digest(sourceBytes)!==mask.source_sha256||mask.source_sha256!=='e7af9c9e88ff9dd38357a570305c4b5d40e98678d14c174957d4bdf2e7bdfd29')throw Error('Wrong frozen source');
if(source.width!==1536||source.height!==1024||raw.width!==source.width||raw.height!==source.height)throw Error('Dimensions differ');
const allowed=new Uint8Array(source.width*source.height);
for(const [x0,y0,x1,y1] of mask.allowed_pixel_runs){if(x0<0||x1>1536||y0<0||y1>1024||y1!==y0+1||x1<=x0)throw Error('Invalid pixel run');for(let x=x0;x<x1;x++)allowed[y0*1536+x]=1;}
if(allowed.reduce((a,b)=>a+b,0)!==mask.mask_pixels)throw Error('Mask count differs');
const out=new PNG({width:1536,height:1024});out.data=Buffer.from(raw.data);
let protectedPixels=0,rawChanged=0,rawMax=0,maskChanged=0;
for(let p=0;p<allowed.length;p++){const i=p*4;if(allowed[p]){if([0,1,2].some(c=>raw.data[i+c]!==source.data[i+c]))maskChanged++;continue;}protectedPixels++;let changed=false;for(let c=0;c<3;c++){const d=Math.abs(raw.data[i+c]-source.data[i+c]);rawMax=Math.max(rawMax,d);changed ||= d!==0;out.data[i+c]=source.data[i+c];}out.data[i+3]=source.data[i+3];if(changed)rawChanged++;}
const finalBytes=PNG.sync.write(out,{colorType:2,inputColorType:6,bitDepth:8});const verify=PNG.sync.read(finalBytes);let outsideChanged=0,maxDiff=0;
for(let p=0;p<allowed.length;p++)if(!allowed[p]){const i=p*4;let changed=false;for(let c=0;c<3;c++){let d=Math.abs(verify.data[i+c]-source.data[i+c]);maxDiff=Math.max(maxDiff,d);changed ||= d!==0;}if(changed)outsideChanged++;}
if(outsideChanged||maxDiff)throw Error('Frozen source verification failed');
fs.writeFileSync(args.out,finalBytes);
const receipt={operation:'SOURCE_RGB_COPY_OUTSIDE_NARROW_TEXT_MASK',source:{path:args.source,sha256:digest(sourceBytes)},raw_figma_export:{path:args.render,sha256:digest(rawBytes)},mask:{path:args.mask,sha256:digest(maskBytes)},output:{path:args.out,sha256:digest(finalBytes),bytes:finalBytes.length,dimensions:[1536,1024]},protected_pixels_compared:protectedPixels,raw_protected_pixels_changed:rawChanged,raw_max_channel_difference:rawMax,protected_pixels_changed:outsideChanged,protected_max_channel_difference:maxDiff,mask_pixels:mask.mask_pixels,mask_pixels_changed:maskChanged,hidden_original_recovered:false,new_content_generated_by_this_script:false,dependency:{name:'pngjs',version:require('pngjs/package.json').version,license:require('pngjs/package.json').license}};
fs.writeFileSync(args.receipt,JSON.stringify(receipt,null,2)+'\n');process.stdout.write(JSON.stringify(receipt));
