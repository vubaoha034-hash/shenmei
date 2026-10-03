// Render exactly one V3; guarantee original RGB outside the two fixed envelopes.
const fs=require("node:fs");
const path=require("node:path");
const crypto=require("node:crypto");
const sharp=require("C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp");
const out=__dirname;
const root=path.resolve(out,"../../../../../");
const privateDir=path.join(root,".liu-visual-private/correct_source_typography/lettering_v3");
const source=path.join(root,".liu-visual-private/source_recovery_20261003/photography-local-reconstruction-final.png");
const rects=[[64,56,504,304],[800,72,1504,440]];
const inside=(x,y)=>rects.some(([l,t,r,b])=>x>=l&&x<r&&y>=t&&y<b);
const sha=b=>crypto.createHash("sha256").update(b).digest("hex");

async function main(){
  const exports=[];
  for(const name of ["chazuo-wordmark","headline","typography-overlay"]){
    const destination=path.join(privateDir,`${name}.png`);
    const info=await sharp(path.join(out,`${name}.svg`)).png().toFile(destination);
    const b=fs.readFileSync(destination);
    exports.push({file:path.relative(root,destination).replaceAll("\\","/"),sha256:sha(b),width:info.width,height:info.height,channels:info.channels,transparent_background:info.channels===4,bytes:b.length});
  }
  const base=await sharp(source).removeAlpha().raw().toBuffer({resolveWithObject:true});
  const overlay=await sharp(path.join(privateDir,"typography-overlay.png")).ensureAlpha().raw().toBuffer({resolveWithObject:true});
  if(base.info.width!==1536||base.info.height!==1024||base.info.channels!==3)throw Error("Unexpected source layout");
  if(overlay.info.width!==1536||overlay.info.height!==1024||overlay.info.channels!==4)throw Error("Unexpected overlay layout");
  const composed=Buffer.from(base.data); let alphaOutside=0, changedInside=0, changedOutside=0;
  const bounds=[1536,1024,-1,-1];
  for(let y=0;y<1024;y++)for(let x=0;x<1536;x++){
    const i=y*1536+x, a=overlay.data[i*4+3]; if(!a)continue;
    if(!inside(x,y)){alphaOutside++;continue;}
    bounds[0]=Math.min(bounds[0],x);bounds[1]=Math.min(bounds[1],y);bounds[2]=Math.max(bounds[2],x);bounds[3]=Math.max(bounds[3],y);
    for(let c=0;c<3;c++)composed[i*3+c]=Math.round((overlay.data[i*4+c]*a+base.data[i*3+c]*(255-a))/255);
  }
  if(alphaOutside)throw Error(`Nonzero overlay alpha outside fixed envelopes: ${alphaOutside}`);
  const preview=path.join(privateDir,"composited-v3.png");
  await sharp(composed,{raw:{width:1536,height:1024,channels:3}}).png().toFile(preview);
  const decoded=await sharp(preview).removeAlpha().raw().toBuffer();
  for(let y=0;y<1024;y++)for(let x=0;x<1536;x++){
    const i=(y*1536+x)*3;
    if(decoded[i]!==base.data[i]||decoded[i+1]!==base.data[i+1]||decoded[i+2]!==base.data[i+2]){if(inside(x,y))changedInside++;else changedOutside++;}
  }
  if(changedOutside)throw Error(`RGB changed outside fixed envelopes: ${changedOutside}`);
  const pb=fs.readFileSync(preview);
  exports.push({file:path.relative(root,preview).replaceAll("\\","/"),sha256:sha(pb),width:1536,height:1024,channels:3,transparent_background:false,bytes:pb.length});
  const protection={source_sha256:sha(fs.readFileSync(source)),fixed_envelopes:rects,overlay_nonzero_alpha_outside_envelopes:alphaOutside,changed_rgb_pixels_outside_envelopes:changedOutside,changed_rgb_pixels_inside_envelopes:changedInside,overlay_alpha_bounds:bounds,method:"Original decoded RGB copied; only nonzero-alpha overlay pixels blended in existing envelopes; final PNG decoded and compared to original RGB."};
  const record={node_executable:process.execPath,node_version:process.version,sharp_versions:sharp.versions,sharp_require_path:require.resolve("C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp"),exports,protection};
  fs.writeFileSync(path.join(out,"raster_exports.json"),JSON.stringify(record,null,2)+"\n","utf8");
  const provenancePath=path.join(out,"provenance.json");
  const provenance=JSON.parse(fs.readFileSync(provenancePath,"utf8"));
  provenance.raster_execution={node_executable:record.node_executable,node_version:record.node_version,sharp_versions:record.sharp_versions,sharp_require_path:record.sharp_require_path};
  provenance.raster_exports=exports;provenance.engineering_pixel_protection=protection;
  fs.writeFileSync(provenancePath,JSON.stringify(provenance,null,2)+"\n","utf8");
  fs.writeFileSync(path.join(privateDir,"provenance.json"),JSON.stringify(provenance,null,2)+"\n","utf8");
  const files=fs.readdirSync(out).filter(name=>fs.statSync(path.join(out,name)).isFile()&&name!=="asset_manifest.json");
  const manifest={files:files.map(name=>({path:name,bytes:fs.statSync(path.join(out,name)).size,sha256:sha(fs.readFileSync(path.join(out,name)))})),private_exports:exports};
  fs.writeFileSync(path.join(out,"asset_manifest.json"),JSON.stringify(manifest,null,2)+"\n","utf8");
  process.stdout.write(JSON.stringify(record,null,2)+"\n");
}
main().catch(error=>{process.stderr.write(String(error)+"\n");process.exitCode=1;});
