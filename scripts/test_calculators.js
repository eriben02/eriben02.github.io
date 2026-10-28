#!/usr/bin/env node
/**
 * Chargeback calculator checks.
 * Run from the repo root: node scripts/test_calculators.js
 */
const assert = require("assert");
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const root = path.resolve(__dirname, "..");
const rel = "public/chargeback-fee-and-recovery-calculator/index.html";
const mirrorRel = "public/pricing/stripe-shopify-chargeback-fee-and-chargeflow-roi-calculator/index.html";
const html = fs.readFileSync(path.join(root, rel), "utf8");
const mirror = fs.readFileSync(path.join(root, mirrorRel), "utf8");

function fail(msg) {
  console.error("FAIL:", msg);
  process.exit(1);
}

for (const bad of ["\u2014", "&mdash;", "SaaSTruth", "Erik Bengtsson"]) {
  if (html.includes(bad) || mirror.includes(bad)) fail("banned token " + bad);
}

const required = [
  "Paddle ($20 dispute fee)",
  "Stripe ($15 dispute fee + $15 counter fee)",
  "Shopify Payments ($15 dispute fee)",
  "Manual In-House Dispute Handling",
  "Chargeflow Pay-On-Performance",
  "Stripe Chargeback Protection (0.40% of GMV)",
  "Baseline (20% Win Rate)",
  "Highest Net Recovery",
  "Flat Volume Fee",
  "best-card",
  "Recover $9,126/yr net with Chargeflow (save $10,062/yr vs manual)",
  "saves $10,062/yr vs. manual in-house handling",
  "See exactly how we calculated this",
  "See calculation",
  'data-track="vendor-cta"',
  'data-vendor="chargeflow"',
  "https://www.chargeflow.io/",
];
for (const token of required) {
  if (!html.includes(token)) fail("missing " + token);
  if (!mirror.includes(token)) fail("mirror missing " + token);
}

const match = html.match(/function calcChargeback\(input\) \{[\s\S]*?\n\}\n\nfunction renderChargeback/);
if (!match) fail("could not extract calcChargeback");
const sandbox = {};
vm.createContext(sandbox);
vm.runInContext(match[0].replace(/\nfunction renderChargeback$/, ""), sandbox);
const c = sandbox.calcChargeback({ orders: 2000, aov: 120, rate: 0.0065, fee: 15 });

assert.strictEqual(c.gmv, 2880000);
assert.strictEqual(c.disputes, 156);
assert.strictEqual(c.disputed, 18720);
assert.strictEqual(c.fees, 2340);
assert.strictEqual(c.unmanaged, 21060);
assert.strictEqual(c.manualGross, 3744);
assert.strictEqual(c.manualLost, 14976);
assert.strictEqual(c.manualOps, 4680);
assert.strictEqual(c.manualNetAfterOps, -936);
assert.strictEqual(c.manualLoss, 21996);
assert.strictEqual(c.recovered, 12168);
assert.strictEqual(c.successFee, 3042);
assert.strictEqual(c.netRecovered, 9126);
assert.strictEqual(c.cfLost, 6552);
assert.strictEqual(c.cfOps, 0);
assert.strictEqual(c.cfLoss, 11934);
assert.strictEqual(c.savings, 10062);
assert.strictEqual(c.radar, 11520);
assert.strictEqual(c.cfWin, 0.65);
assert.strictEqual(c.manualWin, 0.2);

const paddle = sandbox.calcChargeback({ orders: 2000, aov: 120, rate: 0.0065, fee: 20 });
assert.strictEqual(paddle.fees, 3120);
assert.strictEqual(paddle.manualLoss, 22776);
assert.strictEqual(paddle.cfLoss, 12714);
assert.strictEqual(paddle.savings, 10062);

console.log("ok chargeback calculator: net $9,126, save $10,062 vs manual drain $21,996");
