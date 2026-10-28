#!/usr/bin/env node
/**
 * Zero / normal / high scenarios for every SaaSBill calculator, plus Plausible events.
 * Run: node tests/test_calculator_scenarios.js
 */
const assert = require("assert");
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const root = path.resolve(__dirname, "..");
const pub = path.join(root, "public");
const errors = [];
let checks = 0;

function fail(msg) {
  errors.push(msg);
}
function check(cond, msg) {
  checks += 1;
  if (!cond) fail(msg);
}

function read(rel) {
  return fs.readFileSync(path.join(pub, rel), "utf8");
}

function walkHtml(dir, out) {
  for (const name of fs.readdirSync(dir)) {
    const full = path.join(dir, name);
    const stat = fs.statSync(full);
    if (stat.isDirectory()) {
      if (name === "preview" || name === "saastruth" || name === "node_modules") continue;
      walkHtml(full, out);
    } else if (name.endsWith(".html") && name !== "preview.html" && !/^google[0-9a-f]+\.html$/.test(name)) {
      out.push(full);
    }
  }
  return out;
}

function extractBalanced(src, signature) {
  const start = src.indexOf(signature);
  if (start < 0) return null;
  const brace = src.indexOf("{", start);
  let depth = 0;
  for (let i = brace; i < src.length; i++) {
    const ch = src[i];
    if (ch === "{") depth += 1;
    else if (ch === "}") {
      depth -= 1;
      if (depth === 0) return src.slice(start, i + 1);
    }
  }
  return null;
}

function extractJsonConst(src, name) {
  const token = "const " + name + " = ";
  const start = src.indexOf(token);
  if (start < 0) throw new Error("missing const " + name);
  const jsonStart = start + token.length;
  const open = src[jsonStart];
  const close = open === "[" ? "]" : "}";
  let depth = 0;
  for (let i = jsonStart; i < src.length; i++) {
    if (src[i] === open) depth += 1;
    else if (src[i] === close) {
      depth -= 1;
      if (depth === 0) return JSON.parse(src.slice(jsonStart, i + 1));
    }
  }
  throw new Error("unclosed " + name);
}

function loadHomepageEngine() {
  const html = read("index.html");
  const tools = extractJsonConst(html, "TOOLS");
  const seatsFn = extractBalanced(html, "function calcEffectiveSeats");
  const yearFn = extractBalanced(html, "function calcToolYear1");
  const payFn = extractBalanced(html, "function quotePayProfile");
  const box = {};
  vm.createContext(box);
  vm.runInContext(seatsFn + "\n" + yearFn + "\n" + payFn + "\nthis.calcToolYear1 = calcToolYear1;\nthis.quotePayProfile = quotePayProfile;", box);
  const byId = {};
  tools.forEach(function (t) { byId[t.id] = t; });
  return { tools: byId, calc: box.calcToolYear1, pay: box.quotePayProfile };
}

function makeEl(id, values) {
    const el = {
    id: id,
    value: values[id] != null ? String(values[id]) : "",
    selectedIndex: 0,
    options: [{ text: values[id] != null ? String(values[id]) : "" }],
    textContent: "",
    innerHTML: "",
    style: {},
    className: "",
    open: false,
    dataset: {},
    addEventListener: function () {},
    removeEventListener: function () {},
    setAttribute: function (k, v) { el[k] = v; },
    getAttribute: function (k) { return el[k] || ""; },
    querySelector: function () { return makeEl("", values); },
    querySelectorAll: function () { return []; },
    appendChild: function () {},
    insertAdjacentElement: function () {},
    closest: function () { return null; },
    contains: function () { return false; },
    classList: { add: function () {}, remove: function () {}, toggle: function () {}, contains: function () { return false; } }
  };
  return el;
}

function runPage(rel, fnName, scenarios, outputId) {
  const html = read(rel);
  const scripts = html.match(/<script>([\s\S]*?)<\/script>/g) || [];
  const body = scripts.map(function (s) { return s.replace(/<\/?script>/g, ""); }).find(function (s) {
    return s.indexOf("function " + fnName) !== -1;
  });
  if (!body) {
    fail(rel + " missing function " + fnName);
    return [];
  }
  const snapshots = [];
  scenarios.forEach(function (values, index) {
    const els = {};
    const document = {
      getElementById: function (id) {
        if (!els[id]) els[id] = makeEl(id, values);
        if (values[id] != null) els[id].value = String(values[id]);
        return els[id];
      },
      querySelector: function () { return null; },
      querySelectorAll: function () { return []; },
      addEventListener: function () {},
      body: makeEl("body", values)
    };
    const sandbox = { document: document, window: {}, console: console, Date: Date, Math: Math, Number: Number, parseInt: parseInt, parseFloat: parseFloat, isNaN: isNaN };
    sandbox.window = sandbox;
    vm.createContext(sandbox);
    try {
      vm.runInContext(body, sandbox, { filename: rel });
      if (typeof sandbox[fnName] === "function") sandbox[fnName]();
    } catch (err) {
      fail(rel + " scenario " + index + " threw " + err.message);
      snapshots.push("");
      return;
    }
    const ids = outputId ? [outputId] : Object.keys(els);
    const chunks = ids.map(function (id) {
      const el = els[id];
      return el ? ((el.innerHTML || "") + " " + (el.textContent || "")) : "";
    });
    snapshots.push(chunks.join("\n"));
  });
  return snapshots;
}

function maxDollars(text) {
  const nums = [];
  const re = /\$([0-9][0-9,]*)/g;
  let m;
  while ((m = re.exec(text))) nums.push(Number(m[1].replace(/,/g, "")));
  return nums.length ? Math.max.apply(null, nums) : 0;
}

function scenarioDollars(text) {
  const m = String(text).match(/summary-metric[^>]*>[\s\S]{0,120}\$([0-9][0-9,]*)/);
  if (m) return Number(m[1].replace(/,/g, ""));
  return maxDollars(text);
}
function assertGrowing(rel, snapshots, label) {
  const highs = snapshots.map(scenarioDollars);
  check(highs[2] > highs[0] && highs[1] >= highs[0] && highs[2] >= highs[1] && !(highs[0] === highs[1] && highs[1] === highs[2]), rel + " " + label + " should rise from zero/low to high: " + highs.join(" -> "));
}

function helpdeskMath(engine) {
  const ic = engine.tools["intercom-fin-ai"];
  const fd = engine.tools["freshdesk-support"];
  const zd = engine.tools["zendesk-suite-team"];
  const pro = engine.tools["zendesk-suite-professional"];
  const zeroIc = engine.calc(ic, 10, 0, "annual");
  const zeroFd = engine.calc(fd, 10, 0, "annual");
  const zeroZd = engine.calc(zd, 10, 0, "annual");
  const zeroPro = engine.calc(pro, 10, 0, "annual");
  check(zeroIc.year1Total === 3480 && zeroIc.aiAnnual === 0, "Intercom zero AI should be $3,480, got " + zeroIc.year1Total);
  check(zeroFd.year1Total === 2280 && zeroFd.aiAnnual === 0, "Freshdesk zero AI should be $2,280, got " + zeroFd.year1Total);
  check(zeroZd.year1Total === 6600 && zeroZd.aiAnnual === 0, "Zendesk Suite Team zero AI should be $6,600, got " + zeroZd.year1Total);
  check(zeroPro.year1Total === 13800 && zeroPro.aiAnnual === 0, "Zendesk Suite Pro zero AI base should be $13,800, got " + zeroPro.year1Total);
  check(zeroPro.year1Total + 10 * 50 * 12 === 19800, "Suite Pro plus the separate $50 Copilot add-on is $19,800 and is not inside year1Total");

  const nIc = engine.calc(ic, 10, 1500, "annual");
  const nFd = engine.calc(fd, 10, 1500, "annual");
  const nZd = engine.calc(zd, 10, 1500, "annual");
  check(nIc.year1Total === 21300, "Intercom normal should be $21,300, got " + nIc.year1Total);
  check(nFd.year1Total === 10855, "Freshdesk normal should be $10,855, got " + nFd.year1Total);
  check(nZd.year1Total === 32700, "Zendesk normal should be $32,700, got " + nZd.year1Total);
  check(nIc.annualSeatsCost + nIc.aiAnnual + nIc.onboarding === nIc.year1Total, "Intercom base + hidden identity");
  check(nFd.hiddenFees === nFd.aiAnnual && nZd.hiddenFees === nZd.aiAnnual, "Freshdesk and Zendesk hidden cost is the AI meter at this volume");

  const hIc = engine.calc(ic, 25, 5000, "monthly");
  const hFd = engine.calc(fd, 25, 5000, "monthly");
  const hZd = engine.calc(zd, 25, 5000, "monthly");
  check(hIc.year1Total > nIc.year1Total && hFd.year1Total > nFd.year1Total && hZd.year1Total > nZd.year1Total, "High usage should exceed the normal annual totals");
  check(hIc.annualSeatsCost + hIc.onboarding + hIc.aiAnnual === hIc.year1Total, "High Intercom base vs hidden identity");
  const normalWinner = [nIc, nFd, nZd].slice().sort(function (a, b) { return a.year1Total - b.year1Total; })[0].tool.id;
  const highWinner = [hIc, hFd, hZd].slice().sort(function (a, b) { return a.year1Total - b.year1Total; })[0].tool.id;
  check(normalWinner === "freshdesk-support", "Normal winner should be Freshdesk, got " + normalWinner);
  check(typeof highWinner === "string" && highWinner.length > 0, "High scenario should name a winner");
  const zeroOrder = [zeroIc.year1Total, zeroZd.year1Total];
  const highOrder = [hIc.year1Total, hZd.year1Total];
  check(zeroOrder[0] < zeroOrder[1], "At zero AI Intercom is below Zendesk");
  check(highOrder[0] !== highOrder[1], "High monthly totals for Intercom and Zendesk should not tie");

  ["intercom-fin-cost-calculator/index.html", "pricing/intercom-fin-ai-resolution-cost-calculator/index.html", "intercom-vs-freshdesk-cost-comparison/index.html", "intercom-vs-zendesk-cost-comparison/index.html", "zendesk-ai-cost-calculator/index.html", "pricing/zendesk-ai-resolution-and-automated-outcome-cost/index.html", "zendesk-vs-freshdesk-cost-comparison/index.html"].forEach(function (rel) {
    const page = read(rel);
    const pageFn = extractBalanced(page, "function calcToolYear1");
    check(!!pageFn, rel + " should ship calcToolYear1");
  });
}

function crmMath(engine) {
  const close = engine.tools["close-crm"];
  const hs = engine.tools["hubspot-sales-pro"];
  const pipe = engine.tools["pipedrive-crm"];
  const monday = engine.tools["monday-crm"];
  [1, 8, 25].forEach(function (seats, i, all) {
    if (i === 0) return;
    const prev = all[i - 1];
    check(engine.calc(close, seats, 0, "annual").year1Total > engine.calc(close, prev, 0, "annual").year1Total, "Close should grow from " + prev + " to " + seats + " seats");
    check(engine.calc(pipe, seats, 0, "annual").year1Total > engine.calc(pipe, prev, 0, "annual").year1Total, "Pipedrive should grow with seats");
  });
  const mon1 = engine.calc(monday, 1, 0, "annual");
  const mon3 = engine.calc(monday, 3, 0, "annual");
  const mon10 = engine.calc(monday, 10, 0, "annual");
  const mon25 = engine.calc(monday, 25, 0, "annual");
  check(mon1.effSeats === mon3.effSeats && mon1.year1Total === mon3.year1Total, "monday 1-seat and 3-seat minimum should match");
  check(mon25.year1Total > mon10.year1Total && mon10.year1Total > mon1.year1Total, "monday high seats should cost more than 10 and 1");
  const hs1 = engine.calc(hs, 1, 0, "annual");
  const hs10 = engine.calc(hs, 10, 0, "annual");
  const hs25 = engine.calc(hs, 25, 0, "annual");
  check(hs1.onboarding > 0 && hs10.year1Total > hs1.year1Total && hs25.year1Total > hs10.year1Total, "HubSpot onboarding stays and seats scale");
  check(hs1.annualSeatsCost + hs1.onboarding + hs1.aiAnnual === hs1.year1Total, "HubSpot year-1 identity");
}

function paymentMath(engine) {
  const zero = engine.pay("stripe-payments", 0, 0);
  const normal = engine.pay("stripe-payments", 50000, 1000);
  const high = engine.pay("stripe-payments", 250000, 10000);
  check(zero.total === 0 && zero.held === 0, "Zero GMV Stripe total should be $0");
  check(normal.total === 2683 && normal.h === 933, "Normal Stripe true cost should stay $2,683 with a $933 gap");
  check(high.total > normal.total && high.held > normal.held && high.h > normal.h, "High GMV should raise Stripe fees, hold, and hidden gap");
  const cf0 = engine.pay("chargeflow", 0, 0);
  const cfN = engine.pay("chargeflow", 50000, 1000);
  const cfH = engine.pay("chargeflow", 250000, 10000);
  check(cf0.netYr === 0 && cfN.netYr === 1901 && cfH.netYr > cfN.netYr, "Chargeflow net recovered should scale with GMV");
  ["whop-payments", "paddle-mor", "lemon-squeezy"].forEach(function (id) {
    const a = engine.pay(id, 10000, 100);
    const b = engine.pay(id, 50000, 1000);
    const c = engine.pay(id, 200000, 8000);
    check(a.total < b.total && b.total < c.total, id + " should increase from low to high volume");
    check(a.b + a.s + a.h === a.total, id + " sticker plus hidden gap should equal the total");
  });
}

function chargebackMath() {
  const html = read("chargeback-fee-and-recovery-calculator/index.html");
  const src = extractBalanced(html, "function calcChargeback");
  const box = {};
  vm.createContext(box);
  vm.runInContext(src + "\nthis.calcChargeback = calcChargeback;", box);
  const zero = box.calcChargeback({ orders: 2000, aov: 120, rate: 0, fee: 15 });
  const normal = box.calcChargeback({ orders: 2000, aov: 120, rate: 0.0065, fee: 15 });
  const high = box.calcChargeback({ orders: 2000, aov: 120, rate: 0.02, fee: 15 });
  check(zero.disputes === 0 && zero.fees === 0 && zero.netRecovered === 0, "Zero dispute rate should have no disputes and $0 recovery");
  check(normal.disputes === 156 && normal.netRecovered === 9126 && normal.cfLoss < normal.radar, "At 0.65% Chargeflow's modeled drain should beat the 0.40% path");
  check(high.disputes > normal.disputes && high.radar < high.cfLoss, "At 2% the 0.40% of GMV path should cost less than 25% pay-on-performance");
  check(high.manualLoss > normal.manualLoss, "High dispute volume should raise the manual drain");
}

function namedPaymentFns() {
  const stripe = read("pricing/stripe-billing-0-7-percent-recurring-tax-calculator/index.html");
  const both = read("faq/stripe-vs-paddle-true-cost/index.html");
  const reserve = read("exit/stripe-shopify-paddle-frozen-funds-alternatives/index.html");
  const take = read("compare/gumroad-vs-whop-vs-lemon-squeezy-take-rate-calculator/index.html");
  const zoom = read("exit/zoominfo-60-day-auto-renewal-notice-and-cancellation/index.html");
  function load(src, name) {
    const body = extractBalanced(src, "function " + name);
    const box = {};
    vm.createContext(box);
    vm.runInContext(body + "\nthis.fn = " + name + ";", box);
    return box.fn;
  }
  const calcStripe = load(stripe, "calcStripeDisputes");
  const z0 = calcStripe(40000, 800, 0);
  const zN = calcStripe(40000, 800, 0.5);
  const zH = calcStripe(40000, 800, 2);
  check(z0.net === 0 && z0.disputes === 0, "Stripe Billing at 0% disputes recovers $0");
  check(zN.net === 1170, "Stripe Billing normal net should be $1,170, got " + zN.net);
  check(zH.net > zN.net && zH.drain > zN.drain, "Stripe Billing high dispute rate should raise drain and net recovery");

  const calcBoth = load(both, "calcProcessorDisputes");
  const p0 = calcBoth(50000, 1000, 0, 15);
  const pN = calcBoth(50000, 1000, 0.5, 15);
  const pH = calcBoth(50000, 1000, 1.6, 15);
  check(p0.net === 0 && pN.net === 1462 && pH.net > pN.net, "Stripe vs Paddle recovery should be $0, $1,462, then higher at 1.60%");

  const calcRes = load(reserve, "calcReserveDisputes");
  check(calcRes(50000, 0).disputesYr === 0, "Reserve calculator at 0% has no disputes");
  const rN = calcRes(50000, 0.65);
  const rH = calcRes(50000, 2);
  check(rN.netRecovered === 1901 && rH.drain > rN.drain && rH.netRecovered > rN.netRecovered, "Reserve dispute drain and recovery should rise from 0.65% to 2%");

  const feesStart = take.indexOf("const TR_FEES = ");
  const feesSrc = take.slice(feesStart, take.indexOf(";", feesStart) + 1);
  function loadWith(src, name, prelude) {
    const body = extractBalanced(src, "function " + name);
    const box = {};
    vm.createContext(box);
    vm.runInContext((prelude || "") + "\n" + body + "\nthis.fn = " + name + ";", box);
    return box.fn;
  }
  const calcCf = loadWith(take, "calcChargeflowOnDisputes", feesSrc);
  const calcPlat = loadWith(take, "calcPlatforms", feesSrc);
  check(calcCf(29, 200, 0).net === 0, "Gumroad Chargeflow line at 0% dispute rate is $0");
  check(calcCf(29, 200, 0.5).net === 169, "Gumroad normal dispute recovery should stay $169");
  check(calcCf(29, 200, 2).net > 169, "Gumroad high dispute rate should recover more");
  const low = calcPlat({ price: 10, sales: 20, intl: 0, paypal: 0, sub: false, discover: 0, dispute: 0, payout: "domestic", whop_fx: false, whop_risk: false, whop_tax: "none" });
  const mid = calcPlat({ price: 29, sales: 200, intl: 30, paypal: 10, sub: true, discover: 0, dispute: 0.5, payout: "domestic", whop_fx: false, whop_risk: false, whop_tax: "none" });
  const hi = calcPlat({ price: 100, sales: 800, intl: 60, paypal: 20, sub: true, discover: 25, dispute: 2, payout: "intl", whop_fx: true, whop_risk: true, whop_tax: "none" });
  check(low.gmv < mid.gmv && mid.gmv < hi.gmv, "Take-rate GMV should rise across zero, normal, and high");
  check(low.whop.total <= mid.whop.total && mid.whop.total < hi.whop.total, "Whop fees on the take-rate page should rise with volume");

  const calcZi = load(zoom, "calcZoomInfoRenewal");
  const zi0 = calcZi({ annual: 0, discountPct: 0, initialYears: 1, negotiatedPct: 0, version: "2024", customUpliftPct: 0 });
  const ziN = calcZi({ annual: 20000, discountPct: 0, initialYears: 1, negotiatedPct: 0, version: "2024", customUpliftPct: 0 });
  const ziH = calcZi({ annual: 80000, discountPct: 20, initialYears: 3, negotiatedPct: 5, version: "2024", customUpliftPct: 0 });
  check(zi0.extensionTotal === 0, "ZoomInfo zero contract should extend at $0");
  check(ziN.extensionTotal > zi0.extensionTotal && ziH.extensionTotal > ziN.extensionTotal, "ZoomInfo extension cost should rise from a small contract to a high one");
}

function pageScenarios() {
  const pages = [
    ["compare/typeform-vs-jotform-response-limit-and-hipaa-cost/index.html", "runPageCalc", [
      { "p-slider": 100, "p-select": "standard" },
      { "p-slider": 2500, "p-select": "standard" },
      { "p-slider": 10000, "p-select": "hipaa" }
    ]],
    ["compare/close-crm-vs-hubspot-sales-hub-5-to-20-reps/index.html", "runPageCalc", [
      { "p-slider": 1, "p-select": "essentials" },
      { "p-slider": 8, "p-select": "essentials" },
      { "p-slider": 20, "p-select": "growth" }
    ]],
    ["pricing/gong-io-platform-fee-and-seat-minimum-calculator/index.html", "runPageCalc", [
      { "p-slider": 3, "p-select": "gong_only" },
      { "p-slider": 8, "p-select": "with_crm" },
      { "p-slider": 25, "p-select": "with_crm" }
    ]],
    ["pricing/docusign-envelope-allowance-and-api-overage-calculator/index.html", "runPageCalc", [
      { "p-slider": 20, "p-select": "2_users" },
      { "p-slider": 120, "p-select": "5_users" },
      { "p-slider": 400, "p-select": "5_users" }
    ], "p-tbody"],
    ["exit/paypal-180-day-permanent-limitation-fund-recovery/index.html", "runPageCalc", [
      { "p-slider": 5000, "p-select": "hold_30" },
      { "p-slider": 30000, "p-select": "hold_30" },
      { "p-slider": 100000, "p-select": "hold_100" }
    ]],
    ["faq/does-hubspot-charge-onboarding-fees-2026/index.html", "runPageCalc", [
      { "p-slider": 1, "p-select": "sales_pro" },
      { "p-slider": 5, "p-select": "sales_pro" },
      { "p-slider": 20, "p-select": "marketing_pro" }
    ]],
    ["faq/intercom-fin-ai-cost-calculator/index.html", "runPageCalc", [
      { "p-slider": 100, "p-select": "5_essential" },
      { "p-slider": 1000, "p-select": "5_essential" },
      { "p-slider": 3000, "p-select": "5_advanced" }
    ]],
    ["pricing/jotform-pricing-tier-calculator/index.html", "runJfTierCalc", [
      { "jf-subs": 100, "jf-mode": "annual" },
      { "jf-subs": 1000, "jf-mode": "annual" },
      { "jf-subs": 10000, "jf-mode": "monthly" }
    ], "jf-tier-summary"],
    ["guides/jotform-wix-app-setup-and-pricing-guide/index.html", "updateJotformWixCalc", [
      { "jw-vol": 100, "jw-billing": "annual" },
      { "jw-vol": 1000, "jw-billing": "annual" },
      { "jw-vol": 10000, "jw-billing": "monthly" }
    ], "jw-summary"],
    ["hubspot-onboarding-fee-calculator/index.html", "updateHs", [
      { "hs-users": 1, "hs-contacts": 1000, "hs-tier": "sales_pro" },
      { "hs-users": 8, "hs-contacts": 10000, "hs-tier": "sales_pro" },
      { "hs-users": 25, "hs-contacts": 100000, "hs-tier": "sales_ent" }
    ]],
    ["pricing/hubspot-true-cost-and-onboarding-fees/index.html", "updateHs", [
      { "hs-seats": 1, "hs-tier": "sales_pro" },
      { "hs-seats": 8, "hs-tier": "sales_pro" },
      { "hs-seats": 25, "hs-tier": "sales_ent" }
    ]],
    ["compare/monday-crm-vs-pipedrive-vs-hubspot-seat-minimums/index.html", "updateSmCalc", [
      { "sm-users": 1, "sm-tier": "entry" },
      { "sm-users": 5, "sm-tier": "entry" },
      { "sm-users": 15, "sm-tier": "pro" }
    ]],
    ["compliance/hipaa-baa-and-soc2-pricing-tiers/index.html", "updateSocCalc", [
      { "soc-emp": 10, "soc-fw": "1", "soc-disc": 0 },
      { "soc-emp": 50, "soc-fw": "1.45", "soc-disc": 35 },
      { "soc-emp": 200, "soc-fw": "1.85", "soc-disc": 0 }
    ], "soc2-summary"],
    ["compliance/google-workspace-vs-microsoft-365-hipaa-baa-tiers/index.html", "updateGm", [
      { "gm-seats": 1, "gm-tier": "entry", "gm-term": "annual", "gm-mslist": "new", "gm-promo": "0", "gm-forms": "0" },
      { "gm-seats": 10, "gm-tier": "mid", "gm-term": "annual", "gm-mslist": "new", "gm-promo": "0", "gm-forms": "0" },
      { "gm-seats": 50, "gm-tier": "retention", "gm-term": "flex", "gm-mslist": "new", "gm-promo": "0", "gm-forms": "1" }
    ], "gm-summary"],
    ["exit/stripe-shopify-paddle-frozen-funds-alternatives/index.html", "updateReserveSim", [
      { "gm-rev": 10000, "gm-res": 0, "gm-cap": 0, "res-dispute-rate": 0 },
      { "gm-rev": 50000, "gm-res": 25, "gm-cap": 10, "res-dispute-rate": 0.65 },
      { "gm-rev": 150000, "gm-res": 100, "gm-cap": 20, "res-dispute-rate": 2 }
    ], "res-output"]
  ];
  pages.forEach(function (spec) {
    const snaps = runPage(spec[0], spec[1], spec[2], spec[3]);
    if (snaps.length === 3) assertGrowing(spec[0], snaps, spec[1]);
  });

  const billing = runPage("pricing/stripe-billing-0-7-percent-recurring-tax-calculator/index.html", "runPageCalc", [
    { "p-slider": 40000, "p-select": "full", "sb-dispute-rate": 0 },
    { "p-slider": 40000, "p-select": "full", "sb-dispute-rate": 0.5 },
    { "p-slider": 40000, "p-select": "full", "sb-dispute-rate": 2 }
  ]);
  check(billing[0] && billing[0].indexOf("Saves $0/yr net") !== -1, "Stripe Billing table should show Saves $0/yr net at a 0% dispute rate");
  check(billing[1] && billing[1].indexOf("Saves $1,170/yr net") !== -1 && billing[1].indexOf("$1,170 net / yr") !== -1, "Stripe Billing table and Card 3 should both show $1,170 at 0.50%");
  function savedNet(text) {
    const m = String(text || "").match(/Saves \$([0-9,]+)\/yr net/);
    return m ? Number(m[1].replace(/,/g, "")) : -1;
  }
  check(savedNet(billing[2]) > savedNet(billing[1]), "Stripe Billing high dispute rate should raise net recovery above $1,170, got " + savedNet(billing[2]));

  const paddle = runPage("faq/stripe-vs-paddle-true-cost/index.html", "runPageCalc", [
    { "p-slider": 50000, "p-select": "domestic", "sp-dispute-rate": 0 },
    { "p-slider": 50000, "p-select": "domestic", "sp-dispute-rate": 0.5 },
    { "p-slider": 50000, "p-select": "intl_40", "sp-dispute-rate": 1.6 }
  ]);
  check(paddle[0] && paddle[0].indexOf("Saves $0/yr net") !== -1, "Stripe vs Paddle table should show Saves $0/yr net at 0%");
  check(paddle[1] && paddle[1].indexOf("Saves $1,462/yr net") !== -1 && paddle[1].indexOf("$1,462 net / yr") !== -1, "Stripe vs Paddle table and Card 3 should both show $1,462 at 0.50%");
  check(savedNet(paddle[2]) > savedNet(paddle[1]), "Stripe vs Paddle high dispute rate should raise net recovery above $1,462, got " + savedNet(paddle[2]));
}

function helpdeskCopy() {
  const expect = {
    "intercom-vs-freshdesk-cost-comparison/index.html": [
      "Intercom vs. Freshdesk Year-1 Cost &amp; AI Resolution Calculator (2026)",
      "Why Intercom ($21,300/yr) costs nearly 2x Freshdesk ($10,855/yr) at 1,500 AI resolutions/month",
      "Lowest Year-1 Cost: Freshdesk",
      "Head-to-Head Gap: Intercom vs. Freshdesk"
    ],
    "intercom-vs-zendesk-cost-comparison/index.html": [
      "Intercom vs. Zendesk Year-1 Cost &amp; AI Resolution Calculator (2026)",
      "Why Zendesk ($32,700/yr) costs $11,400/yr more than Intercom ($21,300/yr) at 10 seats",
      "Head-to-Head Winner:",
      "Lowest-Cost Alternative: Freshdesk"
    ],
    "zendesk-vs-freshdesk-cost-comparison/index.html": [
      "Zendesk vs. Freshdesk Year-1 Cost &amp; AI Resolution Calculator (2026)",
      "How Freshdesk saves $21,845 in Year 1 compared to Zendesk Suite Professional + AI",
      "Head-to-Head Savings:"
    ]
  };
  Object.keys(expect).forEach(function (rel) {
    const html = read(rel);
    expect[rel].forEach(function (token) {
      check(html.indexOf(token) !== -1, rel + " missing " + token);
    });
    check(html.indexOf("Interactive Intercom Fin AI Year-1 True-Cost Calculator") === -1, rel + " still uses the shared Intercom calculator heading");
    check(html.indexOf("Interactive Zendesk AI Year-1 True-Cost Calculator") === -1, rel + " still uses the shared Zendesk calculator heading");
  });
  const helpdesk = [
    "intercom-fin-cost-calculator/index.html",
    "pricing/intercom-fin-ai-resolution-cost-calculator/index.html",
    "faq/intercom-fin-ai-cost-calculator/index.html",
    "intercom-vs-freshdesk-cost-comparison/index.html",
    "intercom-vs-zendesk-cost-comparison/index.html",
    "zendesk-ai-cost-calculator/index.html",
    "pricing/zendesk-ai-resolution-and-automated-outcome-cost/index.html",
    "zendesk-vs-freshdesk-cost-comparison/index.html"
  ];
  helpdesk.forEach(function (rel) {
    const html = read(rel);
    const grid = html.split('class="related-calc-grid">')[1] || "";
    const cards = grid.split("<details")[0];
    check(cards.indexOf("hubspot-true-cost") === -1 && cards.indexOf("close-crm-vs-hubspot") === -1, rel + " related cards should not be CRM");
    check((cards.match(/data-track="internal-audit"/g) || []).length === 3, rel + " should have 3 helpdesk related cards");
    const self = rel.replace("index.html", "");
    check(cards.indexOf(self) === -1, rel + " related cards should not link to itself");
  });
}

function plausible() {
  const files = walkHtml(pub, []);
  check(files.length >= 29, "expected the built HTML pages, found " + files.length);
  files.forEach(function (full) {
    const html = fs.readFileSync(full, "utf8");
    const rel = path.relative(pub, full);
    check(html.indexOf('data-domain="saasbill.io"') !== -1, rel + " missing Plausible data-domain");
    check(html.indexOf("window.trackSaaSBillEvent") !== -1 && html.indexOf("window.trackEvent = window.trackSaaSBillEvent") !== -1, rel + " missing trackEvent dispatcher");
    ["calculator_interaction", "category_select", "result_rendered", "vendor_cta_click"].forEach(function (name) {
      check(html.indexOf(name) !== -1, rel + " dispatcher missing " + name);
    });
    check(html.indexOf('input[type="range"], select') !== -1, rel + " dispatcher should bind range inputs and selects");
    const tags = html.match(/<a\b[^>]*>/g) || [];
    tags.forEach(function (tag) {
      const href = (tag.match(/href="([^"]*)"/) || [])[1] || "";
      const isButton = /btn-cta|btn-affiliate/.test(tag) && !/btn-secondary/.test(tag);
      if (isButton && /^https?:\/\//.test(href)) {
        check(/data-track="vendor-cta"/.test(tag), rel + " external CTA missing data-track: " + tag.slice(0, 180));
        check(/data-vendor="[^"]+"/.test(tag), rel + " external CTA missing data-vendor: " + tag.slice(0, 180));
      }
      if (/data-track="vendor-cta"/.test(tag)) {
        check(/data-vendor="[^"]+"/.test(tag), rel + " vendor CTA missing data-vendor: " + tag.slice(0, 180));
      }
    });
  });

  const home = read("index.html");
  const start = home.indexOf("window.plausible=window.plausible");
  const end = home.indexOf("window.trackEvent = window.trackSaaSBillEvent;");
  check(start > 0 && end > start, "homepage dispatcher block should be extractable");
  const snippet = home.slice(start, end + "window.trackEvent = window.trackSaaSBillEvent;".length);
  const sandbox = { window: {}, Date: Date };
  sandbox.window = sandbox;
  vm.createContext(sandbox);
  vm.runInContext(snippet, sandbox);
  const calls = [];
  sandbox.plausible = function (name, payload) { calls.push({ name: name, payload: payload }); };
  sandbox.trackEvent("calculator_interaction", { control: "seats", value: "10" });
  sandbox.trackEvent("vendor_cta_click", { vendor: "whop-payments", location: "summary-card" });
  check(calls.length === 2 && calls[0].name === "calculator_interaction" && calls[0].payload.props.control === "seats" && calls[0].payload.props.value === "10", "trackEvent should forward props to plausible");
  check(calls[1].name === "vendor_cta_click" && calls[1].payload.props.vendor === "whop-payments", "vendor_cta_click props should reach plausible");
  check(sandbox.__saasbillEvents.length === 2, "trackEvent should push onto __saasbillEvents");
  check(sandbox.__saasbillEvents[0].event === "calculator_interaction" && sandbox.__saasbillEvents[0].control === "seats" && sandbox.__saasbillEvents[0].value === "10", "__saasbillEvents should keep the exact calculator_interaction props");
  check(sandbox.__saasbillEvents[1].event === "vendor_cta_click" && sandbox.__saasbillEvents[1].vendor === "whop-payments" && sandbox.__saasbillEvents[1].location === "summary-card", "__saasbillEvents should keep the exact vendor_cta_click props");
}

function main() {
  errors.length = 0;
  checks = 0;
  const engine = loadHomepageEngine();
  helpdeskMath(engine);
  crmMath(engine);
  paymentMath(engine);
  chargebackMath();
  namedPaymentFns();
  pageScenarios();
  helpdeskCopy();
  plausible();
  if (errors.length) {
    console.error(errors.join("\n"));
    throw new Error(errors.length + " scenario failures");
  }
  console.log("ok calculator scenarios: " + checks + " checks");
}

if (require.main === module) {
  try {
    main();
  } catch (err) {
    console.error(err.message);
    process.exit(1);
  }
}

module.exports = { main };
