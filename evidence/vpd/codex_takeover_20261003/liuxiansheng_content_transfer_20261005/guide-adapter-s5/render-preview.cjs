// Same-candidate technical renders only; does not create alternative designs.
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const sharp=require('C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
function cliOption(flag){const i=process.argv.indexOf(flag);if(i<0)return null;if(!process.argv[i+1]||process.argv[i+1].startsWith('--'))throw new Error('Missing value for '+flag);return process.argv[i+1];}
function findRepository(start){let p=path.resolve(start);while(true){if(fs.existsSync(path.join(p,'PROJECT_CONTROL_ADAPTER.json')))return p;const q=path.dirname(p);if(q===p)throw new Error('No PROJECT_CONTROL_ADAPTER.json ancestor; pass --root');p=q;}}
const ROOT=cliOption('--root')?path.resolve(cliOption('--root')):findRepository(__dirname);
if(!fs.existsSync(path.join(ROOT,'PROJECT_CONTROL_ADAPTER.json')))throw new Error('Explicit --root lacks PROJECT_CONTROL_ADAPTER.json');
const BASE=cliOption('--output-dir')?path.resolve(cliOption('--output-dir')):__dirname,W=960,H=1280,BG={r:24,g:48,b:31,alpha:1};
const svgPath=path.join(BASE,'S5_WORDMARK.svg');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
function alphaStats(data,w,h){
 let x0=w,y0=h,x1=0,y1=0,count=0,opaque=0;
 for(let p=0;p<w*h;p++)if(data[p*4+3]){
   const x=p%w,y=Math.floor(p/w);x0=Math.min(x0,x);y0=Math.min(y0,y);x1=Math.max(x1,x+1);y1=Math.max(y1,y+1);count++;
   if(data[p*4+3]===255)opaque++;
 }
 return {alpha_nonzero_bbox_xyxy:[x0,y0,x1,y1],nonzero_pixels:count,opaque_pixels:opaque,transparent_pixels:w*h-count};
}
async function pngRecord(name,bytes){
 const p=path.join(BASE,name);fs.writeFileSync(p,bytes);
 const meta=await sharp(bytes).metadata();
 return {path:name,sha256:sha(bytes),bytes:bytes.length,width:meta.width,height:meta.height,has_alpha:meta.hasAlpha};
}
async function green(raster,w,h){
 return sharp({create:{width:w,height:h,channels:4,background:BG}}).composite([{input:raster}]).png().toBuffer();
}
(async()=>{
 const svg=fs.readFileSync(svgPath),s=svg.toString('utf8');
 const removed=(s.match(/<g id="ORANGE_(?:BEHIND_GLYPHS|IN_FRONT_OF_GLYPHS)">[\s\S]*?<\/g>/g)||[]);
 if(removed.length!==2)throw new Error('Orange diagnostic group extraction failed');
 const hidden=Buffer.from(s.replace(/<g id="ORANGE_(?:BEHIND_GLYPHS|IN_FRONT_OF_GLYPHS)">[\s\S]*?<\/g>/g,''));
 const full=await sharp(svg).png().toBuffer(),whiteOnly=await sharp(hidden).png().toBuffer();
 const [allRaw,creamRaw]=await Promise.all([
  sharp(full).ensureAlpha().raw().toBuffer({resolveWithObject:true}),
  sharp(whiteOnly).ensureAlpha().raw().toBuffer({resolveWithObject:true})
 ]);
 if(allRaw.info.width!==W||allRaw.info.height!==H||creamRaw.info.width!==W||creamRaw.info.height!==H)throw new Error('Render dimension mismatch');
 const derived=[];
 derived.push(await pngRecord('S5_WORDMARK_TRANSPARENT_RENDER.png',full));
 derived.push(await pngRecord('S5_WORDMARK_TECHNICAL_PREVIEW.png',await green(full,W,H)));
 derived.push(await pngRecord('S5_ORANGE_HIDDEN_TECHNICAL_PREVIEW.png',await green(whiteOnly,W,H)));
 const half=await sharp(svg).resize({width:480,height:640}).png().toBuffer();
 derived.push(await pngRecord('S5_WORDMARK_480PX_TECHNICAL_PREVIEW.png',await green(half,480,640)));
 const fact={
  schema:'s5-technical-render/v1',status:'RENDERED_NOT_AESTHETIC_REVIEW',
  parent_svg:{path:'S5_WORDMARK.svg',sha256:sha(svg),bytes:svg.length},
  candidate_count:1,technical_background_rgb:[BG.r,BG.g,BG.b],actual_full_canvas:[W,H],
  final_all_layers_alpha:alphaStats(allRaw.data,W,H),
  final_cream_only_alpha:alphaStats(creamRaw.data,W,H),
  orange_hidden_method:'Remove the two orange groups from the same final SVG in memory; cream geometry is unchanged.',
  derived_files:derived,
  not_a_complete_poster:true,no_helper_copy:true,
  limits:['Technical backgrounds are neutral visibility aids only.','PNG derivatives and path counts cannot establish aesthetic quality or human acceptance.','480px legibility and hidden-line negative-space checks require actual pixel viewing.']
 };
 fs.writeFileSync(path.join(BASE,'TECHNICAL_RENDER.json'),JSON.stringify(fact,null,2)+'\n');
 console.log(JSON.stringify({status:fact.status,all_alpha:fact.final_all_layers_alpha,cream_alpha:fact.final_cream_only_alpha,files:derived.map(x=>({path:x.path,sha256:x.sha256}))}));
})().catch(e=>{console.error(e.stack);process.exitCode=1;});
