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
  "Stripe ($15 + $15 counter fee)",
  "Shopify Payments ($15 fee)",
  "Manual In-House Dispute Handling",
  "Chargeflow Pay-On-Performance",
  "Stripe Chargeback Protection (0.40% of GMV)",
  "Baseline (20% Win Rate)",
  "25% of recovered dollars",
  "Flat Volume Fee",
  "best-card",
  "Lowest modeled cost",
  "planning benchmark",
  "Chargeblast",
  "Show calculation",
  "math-drawer",
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
assert.strictEqual(c.radarFee, 11520);
assert.strictEqual(c.nonFraudDisputes, 47);
assert.strictEqual(c.fraudDisputes, 109);
assert.strictEqual(c.nonFraudDisputed, 5640);
assert.strictEqual(c.nonFraudLost, 4512);
assert.strictEqual(c.nonFraudFees, 705);
assert.strictEqual(c.nonFraudOps, 1410);
assert.strictEqual(c.nonFraudDrain, 6627);
assert.strictEqual(c.radarLoss, 18147);
assert.strictEqual(c.radar, 18147);
assert.ok(c.cfLoss < c.radar);

const severe = sandbox.calcChargeback({ orders: 2000, aov: 120, rate: 0.02, fee: 15 });
assert.ok(severe.radar < severe.cfLoss, "at a 2% dispute rate the 0.40% path should cost less than pay-on-performance");
assert.strictEqual(c.cfWin, 0.65);
assert.strictEqual(c.manualWin, 0.2);

const paddle = sandbox.calcChargeback({ orders: 2000, aov: 120, rate: 0.0065, fee: 20 });
assert.strictEqual(paddle.fees, 3120);
assert.strictEqual(paddle.manualLoss, 22776);
assert.strictEqual(paddle.cfLoss, 12714);
assert.strictEqual(paddle.savings, 10062);

console.log("ok chargeback calculator: net $9,126, save $10,062 vs manual drain $21,996");

function extractFn(file, name) {
  const text = fs.readFileSync(path.join(root, file), "utf8");
  for (const bad of ["\u2014", "&mdash;", "SaaSTruth", "Erik Bengtsson"]) {
    if (text.includes(bad)) fail(file + " banned token " + bad);
  }
  const re = new RegExp("function " + name + "\\([^)]*\\) \\{[\\s\\S]*?\\n\\}");
  const m = text.match(re);
  if (!m) fail("missing " + name + " in " + file);
  const box = {};
  vm.createContext(box);
  vm.runInContext(m[0], box);
  return { text, fn: box[name] };
}

const reserve = extractFn("public/exit/stripe-shopify-paddle-frozen-funds-alternatives/index.html", "calcReserveDisputes");
if (!reserve.text.includes('id="res-dispute-rate"')) fail("missing res-dispute-rate");
if (!reserve.text.includes('id="res-output"')) fail("missing res-output");
if (!reserve.text.includes('data-vendor="chargeflow"')) fail("reserve page missing chargeflow vendor");
if (!reserve.text.includes("https://www.chargeflow.io/")) fail("reserve page missing chargeflow url");
const rd = reserve.fn(50000, 0.65);
assert.strictEqual(rd.disputesYr, 39);
assert.strictEqual(rd.disputed, 3900);
assert.strictEqual(rd.fees, 585);
assert.strictEqual(rd.prep, 1170);
assert.strictEqual(rd.drain, 5655);
assert.strictEqual(rd.netRecovered, 1901);

const stripe = extractFn("public/pricing/stripe-billing-0-7-percent-recurring-tax-calculator/index.html", "calcStripeDisputes");
if (!stripe.text.includes('id="sb-dispute-rate"')) fail("missing sb-dispute-rate");
if (!stripe.text.includes("Annual chargeback and dispute drain")) fail("stripe billing missing drain label");
const sd = stripe.fn(40000, 800, 0.5);
assert.strictEqual(sd.disputes, 48);
assert.strictEqual(sd.disputed, 2400);
assert.strictEqual(sd.fees, 720);
assert.strictEqual(sd.counter, 720);
assert.strictEqual(sd.drain, 3840);
assert.strictEqual(sd.net, 1170);
for (const token of [
  "Chargeflow (Automated Dispute Recovery)",
  "25% of recovered disputes ($0/mo fixed)",
  "$0/yr base fee",
  "Pay-on-performance add-on for Stripe/Shopify: 65% benchmark recovery rate on disputed volume ($0 fee on unrecovered disputes)",
  "Saves $' + cb.net.toLocaleString('en-US') + '/yr net",
  "https://www.chargeflow.io/pricing",
  'href="https://www.chargeflow.io/"',
  'data-vendor="${r.vendor}"',
  "ctaLocation: 'table-row'",
  "View Chargeflow pricing"
]) {
  if (!stripe.text.includes(token)) fail("stripe billing table missing " + token);
}

const both = extractFn("public/faq/stripe-vs-paddle-true-cost/index.html", "calcProcessorDisputes");
if (!both.text.includes('id="sp-dispute-rate"')) fail("missing sp-dispute-rate");
const ss = both.fn(50000, 1000, 0.5, 15);
const pp = both.fn(50000, 1000, 0.5, 20);
assert.strictEqual(ss.disputes, 60);
assert.strictEqual(ss.disputed, 3000);
assert.strictEqual(ss.unrecovered, 2400);
assert.strictEqual(ss.fees, 900);
assert.strictEqual(ss.drain, 3300);
assert.strictEqual(ss.net, 1462);
assert.strictEqual(pp.fees, 1200);
assert.strictEqual(pp.drain, 3600);
for (const token of [
  "Chargeflow (Automated Dispute Recovery)",
  "Saves $' + stripeCb.net.toLocaleString('en-US') + '/yr net",
  "https://www.chargeflow.io/pricing",
  "ctaLocation: 'table-row'"
]) {
  if (!both.text.includes(token)) fail("stripe vs paddle table missing " + token);
}

const take = extractFn("public/compare/gumroad-vs-whop-vs-lemon-squeezy-take-rate-calculator/index.html", "calcChargeflowOnDisputes");
if (!take.text.includes('id="tr-cf-cta"')) fail("missing take-rate chargeflow cta");
const td = take.fn(29, 200, 0.5);
assert.strictEqual(td.disputedYr, 348);
assert.strictEqual(td.feeYr, 180);
assert.strictEqual(td.net, 169);

const home = fs.readFileSync(path.join(root, "public/index.html"), "utf8");
for (const token of ["Sticker Price: Base rate", "Sticker Price: Per-tx fees", "0.65% chargeback drain", "Monthly GMV ($k)", "Monthly transactions", "$0 evidence prep", "0.5% to 0.75%"]) {
  if (!home.includes(token)) fail("homepage missing " + token);
}
const payStart = home.indexOf("/* QUOTE_PAY_PROFILE_START */");
const payEnd = home.indexOf("/* QUOTE_PAY_PROFILE_END */");
if (payStart < 0 || payEnd < 0) fail("homepage missing quotePayProfile");
const paySandbox = { window: {} };
paySandbox.window = paySandbox;
vm.runInNewContext(home.slice(payStart, payEnd), paySandbox);
const payStripe = paySandbox.quotePayProfile("stripe-payments", 50000, 1000);
const payWhop = paySandbox.quotePayProfile("whop-payments", 50000, 1000);
const payPaddle = paySandbox.quotePayProfile("paddle-mor", 50000, 1000);
const payLemon = paySandbox.quotePayProfile("lemon-squeezy", 50000, 1000);
const payCf = paySandbox.quotePayProfile("chargeflow", 50000, 1000);
assert.strictEqual(payStripe.total, 2683);
assert.strictEqual(payStripe.h, 933);
assert.strictEqual(payStripe.gapLine, "+$933/mo (+$11,196/yr, +53% Hidden Cost Gap above the $1,750/mo advertised sticker rate)");
assert.strictEqual(payWhop.total, 2275);
assert.strictEqual(payWhop.without, 1875);
assert.strictEqual(payWhop.held, 0);
assert.strictEqual(payPaddle.total, 3840);
assert.strictEqual(payPaddle.h, 840);
assert.strictEqual(payLemon.total, 3833);
assert.strictEqual(payLemon.h, 833);
assert.strictEqual(payCf.netYr, 1901);
assert.strictEqual(payCf.netMo, 158);
assert.strictEqual(payCf.b, 0);
assert.strictEqual(payCf.s, 0);

console.log("ok payment calculators: reserve net $1,901, stripe billing net $1,170, stripe vs paddle net $1,462");
require(path.join(root, "tests/test_calculator_scenarios.js")).main();
