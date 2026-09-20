import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const vendorDir = join(root, "static", "vendor");

const files = [
  ["node_modules/gsap/dist/gsap.min.js", "gsap.min.js"],
  ["node_modules/gsap/dist/ScrollTrigger.min.js", "ScrollTrigger.min.js"],
  ["node_modules/alpinejs/dist/cdn.min.js", "alpine.min.js"],
];

mkdirSync(vendorDir, { recursive: true });

for (const [source, target] of files) {
  copyFileSync(join(root, source), join(vendorDir, target));
}
