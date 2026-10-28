#!/usr/bin/env node
const assert = require("assert");
const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const pages = [];
function walk(dir) {
  for (const name of fs.readdirSync(dir)) {
    if (name === "node_modules" || name === "preview" || name === "saastruth" || name === "preview.html") continue;
    const full = path.join(dir, name);
    const stat = fs.statSync(full);
    if (stat.isDirectory()) walk(full);
    else if (name.endsWith(".html")) pages.push(full);
  }
}
walk(path.join(root, "public"));

function singleWrapper(fragment) {
  const open = fragment.match(/^<(div|ul)\b[^>]*class="(math-drawer-body|math-steps)"[^>]*>/);
  if (!open) return false;
  const tag = open[1];
  const re = new RegExp("<" + tag + "\\b|</" + tag + ">", "g");
  re.lastIndex = open[0].length;
  let depth = 1;
  let match;
  while ((match = re.exec(fragment))) {
    depth += match[0].startsWith("</") ? -1 : 1;
    if (depth === 0) return fragment.slice(re.lastIndex).trim() === "";
  }
  return false;
}

let drawers = 0;
for (const file of pages) {
  const html = fs.readFileSync(file, "utf8");
  const rel = path.relative(root, file);
  assert.ok(!html.includes("See exactly how we calculated this"), rel + " still has the long label");
  assert.ok(!html.includes(">See calculation<"), rel + " still has See calculation");
  if (!html.includes("math-drawer")) continue;
  assert.ok(html.includes(">Show calculation<"), rel + " is missing Show calculation");
  const blocks = html.match(/<details class="math-drawer"[\s\S]*?<\/details>/g) || [];
  assert.ok(blocks.length > 0, rel + " has no math-drawer block");
  for (const block of blocks) {
    const after = block.replace(/[\s\S]*?<\/summary>/, "").replace(/<\/details>\s*$/, "").trim();
    assert.ok(singleWrapper(after), rel + " drawer needs one math-drawer-body wrapper");
    drawers += 1;
  }
}
assert.ok(drawers > 0, "no math drawers found");

const css = fs.readFileSync(path.join(root, "assets/styles.css"), "utf8");
assert.ok(css.includes(".math-drawer > :not(summary)"));
assert.ok(css.includes("z-index: 40"));
assert.ok(css.includes("position: absolute"));

const app = fs.readFileSync(path.join(root, "assets/app.js"), "utf8");
assert.ok(app.includes("details.math-drawer"));
assert.ok(app.includes("Escape"));

console.log("ok Show calculation on " + drawers + " math drawers");
