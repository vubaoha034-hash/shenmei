// Thin raster shim. It reads only the three generated full-canvas vector files.
// Photography is deliberately never supplied to sharp/librsvg.
const fs = require('node:fs');
const path = require('node:path');
const outputDirectory = path.resolve(process.argv[2]);
if (path.basename(outputDirectory) !== 'shanyeji-v29-production' || path.basename(path.dirname(outputDirectory)) !== '.liu-visual-private') {
  throw new Error('Output directory is outside the sole authorized private production directory.');
}
const sharpPath = process.argv[3];
const sharp = require(sharpPath);
async function main() {
  const rendered = [];
  for (const [svgName, pngName] of [
    ['brand.svg', 'brand-render.png'],
    ['headline.svg', 'headline-render.png'],
    ['typography.svg', 'typography-overlay.png'],
  ]) {
    const svgBytes = fs.readFileSync(path.join(outputDirectory, svgName));
    const metadata = await sharp(svgBytes, { density: 72 }).metadata();
    if (metadata.width !== 1536 || metadata.height !== 1024) throw new Error('Wrong vector dimensions');
    const info = await sharp(svgBytes, { density: 72 }).ensureAlpha().png().toFile(path.join(outputDirectory, pngName));
    rendered.push({ input: svgName, output: pngName, density: 72, inputBytes: svgBytes.length, outputInfo: info });
  }
  process.stdout.write(JSON.stringify({
    executable: process.execPath,
    nodeVersion: process.version,
    sharpResolvedModule: require.resolve(sharpPath),
    libraryVersions: sharp.versions,
    renders: rendered,
    photographsReadByRenderer: 0,
  }, null, 2) + '\n');
}
main().catch(error => { console.error(error.stack); process.exitCode = 1; });
