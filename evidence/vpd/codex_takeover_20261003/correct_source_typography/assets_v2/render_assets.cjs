// Export this one V2 and preserve source RGB everywhere outside fixed regions.
const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");
const sharp = require("C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp");
const out = __dirname;
const root = path.resolve(out,"../../../../../");
const privateDir = path.join(root,".liu-visual-private/correct_source_typography/lettering_v2");
const photograph = path.join(root,".liu-visual-private/source_recovery_20261003/photography-local-reconstruction-final.png");
const rects = [[64,56,504,304],[800,72,1504,440]];
const inside = (x,y) => rects.some(([left,top,right,bottom]) => x>=left&&x<right&&y>=top&&y<bottom);
const sha = bytes => crypto.createHash("sha256").update(bytes).digest("hex");

async function main(){
  const records=[];
  for(const name of ["chazuo-wordmark","headline","typography-overlay"]){
    const destination=path.join(privateDir,`${name}.png`);
    const info=await sharp(path.join(out,`${name}.svg`)).png().toFile(destination);
    const bytes=fs.readFileSync(destination);
    records.push({file:path.relative(root,destination).replaceAll("\\","/"),sha256:sha(bytes),width:info.width,height:info.height,channels:info.channels,transparent_background:info.channels===4,bytes:bytes.length});
  }
  const base = await sharp(photograph).removeAlpha().raw().toBuffer({resolveWithObject:true});
  const overlay = await sharp(path.join(privateDir,"typography-overlay.png")).ensureAlpha().raw().toBuffer({resolveWithObject:true});
  if(base.info.width!==1536||base.info.height!==1024||base.info.channels!==3)throw Error("Unexpected source image dimensions or channels");
  if(overlay.info.width!==1536||overlay.info.height!==1024||overlay.info.channels!==4)throw Error("Unexpected overlay dimensions or channels");
  const composed=Buffer.from(base.data);
  let alphaOutside=0, changedInside=0, changedOutside=0;
  const bounds=[1536,1024,-1,-1];
  for(let y=0;y<1024;y++)for(let x=0;x<1536;x++){
    const index=y*1536+x, oi=index*4, bi=index*3, alpha=overlay.data[oi+3];
    if(!alpha)continue;
    if(!inside(x,y)){alphaOutside++;continue;}
    bounds[0]=Math.min(bounds[0],x);bounds[1]=Math.min(bounds[1],y);bounds[2]=Math.max(bounds[2],x);bounds[3]=Math.max(bounds[3],y);
    for(let c=0;c<3;c++)composed[bi+c]=Math.round((overlay.data[oi+c]*alpha+base.data[bi+c]*(255-alpha))/255);
  }
  if(alphaOutside)throw Error(`Overlay nonzero alpha outside protected rectangles: ${alphaOutside}`);
  const poster=path.join(privateDir,"composited-v2.png");
  await sharp(composed,{raw:{width:1536,height:1024,channels:3}}).png().toFile(poster);
  const decoded=await sharp(poster).removeAlpha().raw().toBuffer();
  for(let y=0;y<1024;y++)for(let x=0;x<1536;x++){
    const index=(y*1536+x)*3;
    const differs=decoded[index]!==base.data[index]||decoded[index+1]!==base.data[index+1]||decoded[index+2]!==base.data[index+2];
    if(differs){if(inside(x,y))changedInside++;else changedOutside++;}
  }
  if(changedOutside)throw Error(`RGB changed outside protected regions: ${changedOutside}`);
  const posterBytes=fs.readFileSync(poster);
  records.push({file:path.relative(root,poster).replaceAll("\\","/"),sha256:sha(posterBytes),width:1536,height:1024,channels:3,transparent_background:false,bytes:posterBytes.length});
  const evidence={rasterizer:"bundled sharp",exports:records,raw_rgb_protection:{source_sha256:sha(fs.readFileSync(photograph)),protection_rectangles:rects,overlay_alpha_outside_rectangles:alphaOutside,changed_rgb_pixels_outside_rectangles:changedOutside,changed_rgb_pixels_inside_rectangles:changedInside,overlay_nonzero_alpha_bounds:bounds,method:"Source decoded to raw RGB; original bytes copied, overlay blended only at nonzero-alpha pixels; final PNG decoded for equality check."}};
  fs.writeFileSync(path.join(out,"raster_exports.json"),JSON.stringify(evidence,null,2)+"\n","utf8");
  const provenanceFile=path.join(out,"provenance.json");
  const provenance=JSON.parse(fs.readFileSync(provenanceFile,"utf8"));
  provenance.raster_exports=records;
  provenance.engineering_pixel_protection=evidence.raw_rgb_protection;
  fs.writeFileSync(provenanceFile,JSON.stringify(provenance,null,2)+"\n","utf8");
  fs.writeFileSync(path.join(privateDir,"provenance.json"),JSON.stringify(provenance,null,2)+"\n","utf8");
  process.stdout.write(JSON.stringify(evidence,null,2)+"\n");
}
main().catch(error=>{process.stderr.write(String(error)+"\n");process.exitCode=1;});
