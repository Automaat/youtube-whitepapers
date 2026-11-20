import { bundle } from "@remotion/bundler";
import { renderMedia, selectComposition } from "@remotion/renderer";
import { readFileSync } from "node:fs";
import path from "node:path";

const [timelinePath, publicDir, output] = process.argv.slice(2);
if (!timelinePath || !publicDir || !output) {
  console.error("usage: node scripts/render.mjs <timeline.json> <publicDir> <out.mp4>");
  process.exit(1);
}
const inputProps = JSON.parse(readFileSync(timelinePath, "utf8"));
const serveUrl = await bundle({ entryPoint: path.resolve("src/index.ts"), publicDir: path.resolve(publicDir) });
const composition = await selectComposition({ serveUrl, id: "Episode", inputProps });
let last = -5;
await renderMedia({
  composition,
  serveUrl,
  codec: "h264",
  crf: 18,
  audioCodec: "aac",
  audioBitrate: "192k",
  pixelFormat: "yuv420p",
  outputLocation: output,
  inputProps,
  imageFormat: "jpeg",
  jpegQuality: 92,
  onProgress: ({ progress }) => {
    const pct = Math.floor(progress * 100);
    if (pct >= last + 5) {
      last = pct;
      console.log(`render ${pct}%`);
    }
  },
});
console.log(output);
