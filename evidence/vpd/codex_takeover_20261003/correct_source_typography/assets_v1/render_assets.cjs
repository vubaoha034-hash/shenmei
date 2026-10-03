// Rasterize one authored vector direction. No finished-asset review is performed.
const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");
const sharp = require("C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp");
const out = __dirname;
const root = path.resolve(out, "../../../../../");
const privateDir = path.join(root, ".liu-visual-private/correct_source_typography/lettering_v1");
const names = ["chazuo-wordmark", "headline", "typography-overlay"];

async function main() {
  const records = [];
  for (const name of names) {
    const source = path.join(out, `${name}.svg`);
    const destination = path.join(privateDir, `${name}.png`);
    const info = await sharp(source).png().toFile(destination);
    const bytes = fs.readFileSync(destination);
    records.push({file: path.relative(root, destination).replaceAll("\\", "/"), sha256: crypto.createHash("sha256").update(bytes).digest("hex"), width:info.width, height:info.height, channels:info.channels, transparent_background:info.channels===4, bytes:bytes.length});
  }
  fs.writeFileSync(path.join(out, "raster_exports.json"), JSON.stringify({rasterizer:"bundled sharp", assets:records}, null, 2)+"\n", "utf8");
  const evidenceProvenance = path.join(out,"provenance.json");
  const provenance = JSON.parse(fs.readFileSync(evidenceProvenance,"utf8"));
  provenance.raster_exports = records;
  fs.writeFileSync(evidenceProvenance, JSON.stringify(provenance,null,2)+"\n","utf8");
  fs.writeFileSync(path.join(privateDir,"provenance.json"),JSON.stringify(provenance,null,2)+"\n","utf8");
  process.stdout.write(JSON.stringify(records,null,2)+"\n");
}
main().catch(error => {process.stderr.write(String(error)+"\n");process.exitCode=1;});
