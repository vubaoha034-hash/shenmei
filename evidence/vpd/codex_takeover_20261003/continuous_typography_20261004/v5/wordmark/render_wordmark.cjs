const fs=require('node:fs');
const path=require('node:path');
const crypto=require('node:crypto');
const sharp=require('C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const out=__dirname;
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
(async()=>{
  const source=path.join(out,'chazuo-wordmark.svg');
  const dest=path.join(out,'chazuo-wordmark.png');
  const info=await sharp(source).png().toFile(dest);
  const record={file:'chazuo-wordmark.png',sha256:sha(fs.readFileSync(dest)),width:info.width,height:info.height,channels:info.channels,transparent_background:info.channels===4,node_version:process.version,node_executable:process.execPath,sharp_version:sharp.versions.sharp};
  const pp=path.join(out,'provenance.json');
  const provenance=JSON.parse(fs.readFileSync(pp,'utf8'));provenance.actual_raster_export=record;
  fs.writeFileSync(pp,JSON.stringify(provenance,null,2)+'\n','utf8');
  const manifest={files:fs.readdirSync(out).filter(n=>fs.statSync(path.join(out,n)).isFile()&&n!=='manifest.json').map(n=>({file:n,sha256:sha(fs.readFileSync(path.join(out,n))),bytes:fs.statSync(path.join(out,n)).size}))};
  fs.writeFileSync(path.join(out,'manifest.json'),JSON.stringify(manifest,null,2)+'\n','utf8');
  process.stdout.write(JSON.stringify(record,null,2)+'\n');
})().catch(e=>{process.stderr.write(String(e)+'\n');process.exitCode=1;});
