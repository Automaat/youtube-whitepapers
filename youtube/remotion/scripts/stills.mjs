import { bundle } from "@remotion/bundler";
import { renderStill, selectComposition } from "@remotion/renderer";
import { mkdirSync, readFileSync } from "node:fs";
import path from "node:path";

const [compositionId, timelinePath, publicDir, outDir, ...specs] = process.argv.slice(2);
if (!compositionId || !timelinePath || !publicDir || !outDir || specs.length === 0) {
  console.error("usage: node scripts/stills.mjs <composition> <timeline.json> <publicDir> <outDir> <frame[:name]>...");
  process.exit(1);
}
const inputProps = JSON.parse(readFileSync(timelinePath, "utf8"));
mkdirSync(outDir, { recursive: true });
const serveUrl = await bundle({ entryPoint: path.resolve("src/index.ts"), publicDir: path.resolve(publicDir) });
const composition = await selectComposition({ serveUrl, id: compositionId, inputProps });
for (const spec of specs) {
  const [frame, name] = spec.split(":");
  const output = path.join(outDir, `${name ?? frame}.png`);
  await renderStill({ composition, serveUrl, output, frame: Number(frame), inputProps });
  console.log(output);
}
