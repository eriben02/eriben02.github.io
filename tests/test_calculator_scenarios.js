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

function idText(html, id) {
  const match = html.match(new RegExp('id="' + id + '"[^>]*>([^<]*)<'));
  return match ? match[1] : null;
}

function walkHtml(dir, out) {
  for (const name of fs.readdirSync(dir)) {
    const full = path.join(dir, name);
    const stat = fs.statSync(full);
    if (stat.isDirectory()) {
      // go/ holds the static affiliate redirect stubs (no analytics, noindex);
      // tests/test_close_vs_pipedrive.py checks them.
      if (name === "preview" || name === "node_modules" || (name === "go" && dir === pub)) continue;
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
      "Lower cost:",
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

function shopifyReserve() {
  const rel = "exit/shopify-payments-chargeback-threshold-and-reserve-appeal/index.html";
  const html = read(rel);
  const title = (html.match(/<title>(.*?)<\/title>/) || [])[1] || "";
  check(title.length > 0 && title.length <= 60, "Shopify title length " + title.length + ": " + title);
  check(title.indexOf("saasbill.io") !== -1, "Shopify title should end with saasbill.io");
  check(html.indexOf("True Year-1 cost") !== -1, "Shopify page should use True Year-1 cost");
  check(html.indexOf("above advertised price.") !== -1, "Shopify page should use the short percent line");
  check(html.indexOf("Estimated Year-1 total including mandatory fees") === -1, "Shopify page should not use the old quote");
  check(html.indexOf("Shopify Payments Reserve &amp; Dispute Threshold Calculator (2026)") !== -1, "missing Shopify H1");
  check(html.indexOf("Does Shopify publish a 0.75% dispute threshold") !== -1, "missing Shopify FAQ");
  check(html.indexOf("../chargeback-fee-and-recovery-calculator/") !== -1, "missing chargeback cross-link");
  check(html.indexOf("../exit/stripe-shopify-paddle-frozen-funds-alternatives/") !== -1 || html.indexOf("stripe-shopify-paddle-frozen-funds-alternatives/") !== -1, "missing frozen-funds cross-link");
  check(html.indexOf("stripe-billing-0-7-percent-recurring-tax-calculator/") !== -1, "missing Stripe Billing cross-link");
  check(html.indexOf('class="table-wrap mobile-cards"') !== -1, "Shopify table should use mobile-cards");
  check(html.indexOf('data-label="Path"') !== -1, "Shopify table cells need data-label");
  check(html.indexOf("\u2014") === -1 && html.indexOf("&mdash;") === -1, "Shopify page has an em dash");
  check(html.indexOf("referral link") === -1, "Shopify page should not label CTAs as referral links");
  const plans = html.match(/const SH_PLANS = \{[\s\S]*?\};/);
  const fn = extractBalanced(html, "function calcShopifyReserve");
  check(!!plans && !!fn, "missing calcShopifyReserve");
  const box = {};
  vm.createContext(box);
  vm.runInContext(plans[0] + "\n" + fn + "\nthis.fn = calcShopifyReserve;", box);
  const zero = box.fn({ orders: 1000, aov: 50, rate: 0, plan: "basic" });
  const normal = box.fn({ orders: 1000, aov: 50, rate: 0.0065, plan: "basic" });
  const high = box.fn({ orders: 2000, aov: 80, rate: 0.02, plan: "basic" });
  check(zero.disputesYr === 0 && zero.hiddenYr === 0 && zero.reserveMo === 0 && zero.stickerYr > 0, "Zero dispute rate should keep the sticker and add no dispute gap");
  check(normal.gmvMo === 50000 && normal.stickerMo === 1750 && normal.hiddenYr > 0 && normal.ndrp === false && normal.reserveMo === 0, "Normal 0.65% case should bill the Basic sticker without an NDRP reserve");
  check(normal.trueYr === normal.stickerYr + normal.hiddenYr, "True Year-1 cost should equal sticker plus hidden gap");
  check(high.ndrp === true && high.reserveMo === 16000 && high.lostYr === high.disputedYr && high.trueYr > normal.trueYr, "At 2% the NDRP path should reimburse every order and hold 10% of GMV");
  check(high.vampRatio === true && high.vampCount === false, "A 2% rate on 2,000 orders crosses the Visa ratio and not the 1,500 count");
  const snaps = runPage(rel, "renderShopifyReserve", [
    { "sh-orders": 0, "sh-aov": 50, "sh-rate": 0, "sh-plan": "basic" },
    { "sh-orders": 1000, "sh-aov": 50, "sh-rate": 0.65, "sh-plan": "basic" },
    { "sh-orders": 5000, "sh-aov": 120, "sh-rate": 2, "sh-plan": "basic" }
  ]);
  if (snaps.length === 3) assertGrowing(rel, snaps, "renderShopifyReserve");
}

function intercomFreshdesk() {
  const rel = "exit/intercom-to-freshdesk-ticket-and-help-center-migration/index.html";
  const html = read(rel);
  const fn = ["calcIntercomFreshdesk", "imMoney", "imPlanName", "imLowerSentence"].map(function (name) {
    return extractBalanced(html, "function " + name);
  }).join("\n");
  check(fn.indexOf("null") === -1 || !!extractBalanced(html, "function calcIntercomFreshdesk"), "missing calcIntercomFreshdesk");
  check(html.indexOf("/go/fresh") === -1, "Freshworks affiliate path must stay off this page");
  check(html.indexOf('rel="sponsored') === -1, "this page has no sponsored link");
  check(html.indexOf("Lower Year-1 cost:") !== -1, "page should label the lower Year-1 cost");
  check(html.indexOf("Those units are not the same") !== -1, "the outcome and session assumption should be visible");
  check(html.indexOf("https://www.intercom.com/pricing") !== -1, "missing Intercom pricing source");
  check(html.indexOf("https://www.freshworks.com/freshdesk/pricing/") !== -1, "missing Freshdesk pricing source");
  check(html.indexOf("4 Nov 2026") !== -1, "missing 4 Nov 2026 check date");
  const title = (html.match(/<title>(.*?)<\/title>/) || [])[1] || "";
  check(title.length > 0 && title.length <= 60, "migration title length " + title.length + ": " + title);
  const box = {};
  vm.createContext(box);
  vm.runInContext(fn + "\nthis.fn = calcIntercomFreshdesk;\nthis.line = imLowerSentence;", box);
  const normal = box.fn({ agents: 5, outcomes: 1000, records: 10000, intercom: "essential", freshdesk: "growth", billing: "annual", copilot: false });
  check(normal.icYear === 1362000 && normal.fdYear === 728900 && normal.diff === 633100 && normal.packs === 115 && normal.lower === "freshdesk", "default 5 seats and 1,000 outcomes should be $13,620 vs $7,289");
  const line = box.line(normal);
  check(line.indexOf("Lower Year-1 cost: Freshdesk, $7,289.") === 0 && line.indexOf("Difference $6,331.") !== -1, "default lower line should name Freshdesk once, got " + line);
  const unknown = box.fn({ agents: 5, outcomes: 1000, records: 2500, intercom: "essential", freshdesk: "growth", billing: "annual", copilot: false });
  check(unknown.migration === null && unknown.fdYear === null && unknown.diff === null && unknown.icYear === 1362000, "2,500 records should leave migration and the Freshdesk total unknown");
  check(box.line(unknown).indexOf("Difference: unknown.") !== -1, "unknown migration should not be priced as zero");
  const monthly = box.fn({ agents: 1, outcomes: 50, records: 0, intercom: "essential", freshdesk: "growth", billing: "monthly", copilot: false });
  const annual = box.fn({ agents: 1, outcomes: 50, records: 0, intercom: "essential", freshdesk: "growth", billing: "annual", copilot: false });
  check(annual.packs === 1 && monthly.packs === 2 && monthly.fdRate === 23, "monthly billing should buy a wasted Freddy pack the annual pool does not");
  const copilot = box.fn({ agents: 5, outcomes: 1000, records: 10000, intercom: "essential", freshdesk: "growth", billing: "annual", copilot: true });
  check(copilot.copilotState === "not-on-growth" && copilot.copilot === 0 && copilot.fdYear === normal.fdYear, "Copilot on Growth should not be priced as $0 or as $29");
  const pro = box.fn({ agents: 5, outcomes: 1000, records: 10000, intercom: "essential", freshdesk: "pro", billing: "annual", copilot: true });
  check(pro.copilot === 174000 && pro.fdYear === 1118900, "Pro Copilot for 5 agents should add $1,740");
  const tiny = box.fn({ agents: 1, outcomes: 1, records: 0, intercom: "essential", freshdesk: "growth", billing: "annual", copilot: false });
  check(tiny.fin === 1188 && tiny.packs === 0, "one outcome should bill $11.88 and should not jump to a 50-outcome minimum");
}

function stripeRadar() {
  const rel = "pricing/stripe-radar-and-dispute-fee-calculator-2026/index.html";
  const html = read(rel);
  const fn = extractBalanced(html, "function calcStripeRadar");
  check(!!fn, "missing calcStripeRadar");
  check(html.indexOf("chargeflow.io") === -1 && html.indexOf('data-vendor="chargeflow"') === -1, "Stripe Radar page must not link Chargeflow");
  check(html.indexOf("Lowest Year-1 cost:") !== -1, "Stripe Radar page should label the lowest Year-1 cost");
  check(html.indexOf("https://stripe.com/pricing") !== -1, "missing Stripe pricing source");
  check(html.indexOf("https://stripe.com/radar/pricing") !== -1, "missing Radar pricing source");
  check(html.indexOf("https://docs.stripe.com/disputes/measuring") !== -1, "missing dispute measurement source");
  check(html.indexOf("2 Nov 2026") !== -1, "missing 2 Nov 2026 check date");
  const box = {};
  vm.createContext(box);
  vm.runInContext(fn + "\nthis.fn = calcStripeRadar;", box);
  const normal = box.fn({ payments: 2000, aov: 100, rate: 0.6, counter: 100, win: 50, smart: false, radar: "lite" });
  check(normal.disputes === 12 && normal.won === 6 && normal.lostFought === 6, "Default 0.60% case should be 12 disputes and 6 losses");
  check(normal.receivedMo === 180 && normal.manual.counterMo === 90 && normal.manual.disputeFeesMo === 270, "Default dispute fees should be $180 received plus $90 kept");
  check(normal.manual.lostMo === 600 && normal.manual.totalMo === 870 && normal.manual.totalYr === 10440, "Default manual Year-1 total should be $10,440");
  check(normal.smart.totalYr === 11520 && normal.accept.totalYr === 16560, "Smart Disputes $11,520 and accept $16,560 at the default");
  check(normal.lowestKeys.length === 1 && normal.lowestKeys[0] === "manual" && normal.threshold === "below", "Manual counter is the lowest cost and 0.60% is below 0.75%");
  const sentenceFn = extractBalanced(html, "function rdLowestSentence");
  check(!!sentenceFn, "missing rdLowestSentence");
  vm.runInContext(sentenceFn + "\nfunction rdMoney(n){return '$'+Math.round(n).toLocaleString('en-US');}\nfunction rdRadarName(){return 'Radar Lite, included';}\nthis.line = rdLowestSentence;", box);
  const line = box.line(normal);
  check(line === "Lowest Year-1 cost: Manual counter, $10,440. Smart Disputes $11,520. Accept all disputes $16,560. The win rate is the one you entered, not a Stripe figure. Radar Lite is included at no extra charge.", "default lowest line should name Manual counter once, got " + line);
  check(line.indexOf("Manual counter") === line.lastIndexOf("Manual counter"), "Manual counter should appear once");
  const at = box.fn({ payments: 2000, aov: 100, rate: 0.75, counter: 0, win: 0, smart: false, radar: "lite" });
  check(at.threshold === "at" && at.disputes === 15, "0.75% should sit on the industry threshold");
  const high = box.fn({ payments: 2000, aov: 80, rate: 2, counter: 100, win: 20, smart: true, radar: "pro" });
  check(high.threshold === "above" && high.selectedKey === "smart" && high.radarMo === 20 && high.selected.totalYr > normal.manual.totalYr, "2% with Radar Pro should be above the threshold and above the default");
  const zero = box.fn({ payments: 0, aov: 100, rate: 0.6, counter: 100, win: 50, smart: false, radar: "standard" });
  check(zero.disputes === 0 && zero.selected.disputeFeesMo === 0 && zero.selected.radarMo === 10 && zero.selected.totalYr === 120, "Zero payments should keep the Radar Standard starting price only");
}

function pipedriveSalesforce() {
  const rel = "compare/pipedrive-vs-salesforce-starter-and-pro-suite-cost/index.html";
  const html = read(rel);
  const fn = extractBalanced(html, "function calcPipedriveSalesforce");
  const lineFn = extractBalanced(html, "function psLowestSentence");
  check(!!fn && !!lineFn, "missing pipedrive salesforce math");
  check(html.indexOf('href="../../go/pipedrive/"') !== -1, "Pipedrive CTA should use /go/pipedrive");
  check(html.indexOf("salesforce.com") !== -1, "Salesforce pricing sources should be linked");
  check(!/btn-cta[^>]*salesforce\.com|salesforce\.com[^<]*btn-cta/.test(html), "no Salesforce affiliate button");
  const box = {};
  vm.createContext(box);
  vm.runInContext(fn + "\n" + lineFn + "\nfunction psMoney(n){return '$'+Math.round(n).toLocaleString('en-US');}\nthis.fn = calcPipedriveSalesforce;\nthis.line = psLowestSentence;", box);
  const five = box.fn({ seats: 5, leadbooster: false, engagement: false, premier: false });
  check(five.growth === 2340 && five.premium === 3540 && five.starter === 1500 && five.pro === 6000 && five.proApi === 7500, "5-seat headline license totals");
  check(five.lite === 840 && five.ultimate === 4740, "5-seat Lite and Ultimate");
  const line = box.line(five);
  check(line.indexOf("Lowest Year-1 cost: Salesforce Starter, $1,500.") === 0, "5 seats, Starter is the lowest of the five paths: " + line);
  check(line.indexOf("Pipedrive Growth $2,340") !== -1 && line.indexOf("Pro plus API $7,500") !== -1, "five-path amounts stay in the sentence");
  check(line.indexOf("implementation is unknown") !== -1, "implementation stays unknown");
  const ten = box.fn({ seats: 10, leadbooster: false, engagement: false, premier: false });
  check(ten.growth === 4680 && ten.premium === 7080 && ten.starter === 3000 && ten.pro === 12000 && ten.proApi === 15000, "10-seat headline license totals");
  const add = box.fn({ seats: 5, leadbooster: true, engagement: true, premier: true });
  check(add.growthTotal === 2730 && add.leadYr === 390 && add.engageYr === 3000 && add.proBill === 11700 && add.proApiBill === 13650, "LeadBooster, Sales Engagement, and Premier Success at 5 seats");
}

function ssoTax() {
  const rel = "compliance/okta-vs-workos-vs-1password-sso-tax-calculator/index.html";
  const html = read(rel);
  const fn = extractBalanced(html, "function calcSsoTax");
  const lineFn = extractBalanced(html, "function ssLowestApps");
  check(!!fn && !!lineFn, "missing sso tax math");
  check(html.indexOf("/go/1password") === -1, "no 1Password affiliate redirect");
  check(html.indexOf("https://1password.com/pricing/business") !== -1, "plain 1Password pricing link");
  check(html.indexOf("OIDC") !== -1 && html.indexOf("HIPAA BAA") !== -1, "1Password OIDC and BAA notes");
  check(html.indexOf("2x") === -1, "do not claim a 2x SSO multiple");
  const box = {};
  vm.createContext(box);
  vm.runInContext("var SS_USERS = [10, 25, 50, 100];\n" + extractBalanced(html, "function ssWorkosRate") + "\n" + extractBalanced(html, "function ssYearFloor") + "\n" + fn + "\n" + lineFn + "\nfunction ssMoney(cents){var v=Math.abs(Math.round(cents));var d=Math.floor(v/100);var r=v%100;var t='$'+d.toLocaleString('en-US');if(r)t+='.'+(r<10?'0':'')+r;return t;}\nthis.fn=calcSsoTax;\nthis.line=ssLowestApps;", box);
  const def = box.fn({ usersIndex: 1, connections: 5 });
  check(def.users === 25 && def.oktaStarter === 180000 && def.password === 269700 && def.workos === 750000, "default 25 people: Okta $1,800, 1Password $2,697, WorkOS $7,500");
  check(def.zoomDelta === 125100 && def.notionDelta === 300000 && def.githubDelta === 510000 && def.figmaDelta === 1170000, "app step-ups at 25 people");
  const line = box.line(def);
  check(line.indexOf("Lowest Year-1 cost: Zoom, $1,251.") === 0, "Zoom is the lowest published step-up: " + line);
  check(line.indexOf("unknown") !== -1, "Slack USD step-up stays unknown");
  const small = box.fn({ usersIndex: 0, connections: 5 });
  check(small.users === 10 && small.oktaStarter === 150000, "10 people hit the $1,500 Okta floor");
  const mid = box.fn({ usersIndex: 1, connections: 20 });
  check(mid.rate === 100 && mid.workos === 2400000, "20 connections use the $100 rung");
  const custom = box.fn({ usersIndex: 1, connections: 120 });
  check(custom.workos === -1, "101 or more connections stay unknown");
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

function soc2Cost() {
  const rel = "compliance/vanta-vs-drata-vs-comp-ai-soc2-negotiation-benchmarks/index.html";
  const html = read(rel);
  const fn = extractBalanced(html, "function calcSoc2");
  const listFn = extractBalanced(html, "function socPlatformList");
  const nameFn = extractBalanced(html, "function socPlatformName");
  const lineFn = extractBalanced(html, "function socLowest");
  const moneyFn = extractBalanced(html, "function socMoney");
  check(!!fn && !!listFn && !!nameFn && !!lineFn && !!moneyFn, "missing soc2 math");
  check(html.indexOf('href="../../go/vanta/"') !== -1, "primary CTA uses /go/vanta");
  check(html.indexOf('href="../../go/drata/"') !== -1, "secondary CTA uses /go/drata");
  check(html.indexOf("https://www.trycomp.ai/pricing") !== -1, "Comp AI stays a plain pricing link");
  check(html.indexOf("partnerstack.com") === -1, "no invented PartnerStack tracking URL");
  const box = {};
  vm.createContext(box);
  const modFn = extractBalanced(html, "function socModules");
  check(!!modFn, "missing soc module overlap math");
  vm.runInContext(listFn + "\n" + nameFn + "\n" + modFn + "\n" + fn + "\n" + lineFn + "\n" + moneyFn + "\nthis.fn=calcSoc2;\nthis.line=socLowest;\nthis.money=socMoney;", box);
  const def = box.fn({ platform: "vanta-essentials", band: "1-20", auditor: 30000, trust: "none", quest: "none", ctm: false, tprm: false, ftr: false, tools: false });
  check(def.list === 14000 && def.year1 === 44000 && def.year2 === 44000 && def.auditor === 30000, "default Essentials plus midpoint auditor is $44,000");
  const workbench = html.split('id="soc-compare"', 1)[0];
  ["SAML", "Zoom step-up", "Notion step-up", "GitHub step-up", "Smallest published", "Figma above Zoom", "Okta, WorkOS", "$1,251", "$10,449"].forEach(function (banned) {
    check(workbench.indexOf(banned) === -1, "SOC 2 no-JS fallback must not contain " + banned);
  });
  check(idText(html, "shell-best") === "", "static SOC 2 result does not pre-rank");
  check(idText(html, "shell-product") === def.name + ", modeled Year-1", "SOC 2 static product");
  check(idText(html, "shell-big") === box.money(def.year1), "SOC 2 static Year-1 " + idText(html, "shell-big"));
  check(idText(html, "shell-amt-base") === box.money(def.list), "SOC 2 static platform");
  check(idText(html, "shell-amt-seats") === "none", "SOC 2 static add-ons");
  check(idText(html, "shell-amt-hidden") === box.money(def.auditor), "SOC 2 static auditor");
  check(idText(html, "shell-sticker") === box.money(def.list), "SOC 2 static sticker");
  check(idText(html, "shell-gap") === "+" + box.money(def.year1 - def.list), "SOC 2 static gap");
  const compare = (html.match(/id="soc-compare-body">([\s\S]*?)<\/tbody>/) || [""])[1];
  [["Vanta Essentials", 14000], ["Vanta Plus", 21500], ["Vanta Professional", 23000], ["Drata Foundation (1 to 50 FTE)", 15000]].forEach(function (row) {
    const total = box.money(row[1] + def.auditor);
    check(compare.indexOf(row[0] + "</td><td data-label=\"12-month list\">" + box.money(row[1]) + "</td><td data-label=\"Year-1\">" + total) !== -1, "SOC 2 static row " + row[0] + " " + total);
  });
  check(html.indexOf("2026-11-07T06:11:32+00:00") !== -1 && html.indexOf("2026-11-09") === -1, "SOC 2 check date stays 2026-11-07");
  const line = box.line("1-20", 30000);
  check(line.indexOf("Lowest Year-1 cost: Vanta Essentials, $44,000.") === 0, "Essentials is the lowest published AWS list plus this CPA fee: " + line);
  check(line.indexOf("published AWS lists") !== -1 && line.indexOf("before add-ons") !== -1 && line.indexOf("1 to 50 FTE") !== -1, "the comparison names its scope: " + line);
  check(line.indexOf("Comp AI") === -1, "unpriced plans stay outside the lowest sentence");
  const one = box.line("21-50", 30000);
  check(one.indexOf("Lowest Year-1 cost") === -1, "one published list is not a competitive label: " + one);
  check(one.indexOf("1 to 50 FTE") !== -1 && one.indexOf("before add-ons") !== -1, one);
  const plus = box.fn({ platform: "vanta-plus", band: "1-20", auditor: 30000, trust: "none", quest: "none", ctm: false, tprm: false, ftr: true, tools: true });
  check(plus.list === 21500 && plus.modules === 7500 && plus.tools === 10000 && plus.year1 === 69000 && plus.year2 === 59000, "Plus, AWS FTR, and the Year-1 allowance");
  const ctm = box.fn({ platform: "vanta-essentials", band: "1-20", auditor: 30000, trust: "advanced", quest: "advanced", ctm: true, tprm: false, ftr: false, tools: false });
  check(ctm.modules === 22250 && ctm.year1 === 66250, "CTM includes the advanced modules and is not added again: " + ctm.modules);
  check(ctm.modules !== 48250, "do not confirm a $48,250 double count");
  const pro = box.fn({ platform: "vanta-professional", band: "1-20", auditor: 30000, trust: "advanced", quest: "qa", ctm: false, tprm: false, ftr: false, tools: false });
  check(pro.modules === -1 && pro.year1 === -1, "Professional inclusions are not a confirmed extra");
  const proCtm = box.fn({ platform: "vanta-professional", band: "1-20", auditor: 30000, trust: "none", quest: "none", ctm: true, tprm: false, ftr: false, tools: false });
  check(proCtm.modules === -1 && proCtm.year1 === -1, "CTM on Professional stays unknown");
  const plusTrust = box.fn({ platform: "vanta-plus", band: "1-20", auditor: 30000, trust: "standard", quest: "none", ctm: false, tprm: false, ftr: false, tools: false });
  check(plusTrust.modules === -1 && plusTrust.year1 === -1, "Trust Center on Plus is not a confirmed $6,000 extra");
  const plusQa = box.fn({ platform: "vanta-plus", band: "1-20", auditor: 30000, trust: "none", quest: "qa", ctm: false, tprm: false, ftr: false, tools: false });
  check(plusQa.modules === -1 && plusQa.year1 === -1, "Plus upgrade to 144 has no confirmed price");
  const ent = box.fn({ platform: "vanta-quote", band: "1-20", auditor: 30000, trust: "none", quest: "none", ctm: true, tprm: true, ftr: true, tools: false });
  check(ent.list === -1 && ent.modules === -1 && ent.year1 === -1, "Enterprise entitlements stay unknown");
  const wider = box.fn({ platform: "vanta-essentials", band: "21-50", auditor: 30000, trust: "none", quest: "none", ctm: false, tprm: false, ftr: false, tools: false });
  check(wider.list === -1 && wider.year1 === -1, "Vanta list stops at 1 to 20 employees");
  const drata = box.fn({ platform: "drata-foundation", band: "21-50", auditor: 10000, trust: "none", quest: "none", ctm: false, tprm: false, ftr: false, tools: false });
  check(drata.list === 15000 && drata.year1 === 25000 && drata.year2 === 25000, "Drata Foundation still lists at 21 to 50");
  const drataMod = box.fn({ platform: "drata-foundation", band: "1-20", auditor: 30000, trust: "standard", quest: "none", ctm: false, tprm: false, ftr: false, tools: false });
  check(drataMod.modules === -1 && drataMod.year1 === -1, "Vanta add-on prices are not applied to Drata");
  const big = box.fn({ platform: "drata-foundation", band: "51", auditor: 30000, trust: "none", quest: "none", ctm: false, tprm: false, ftr: false, tools: false });
  check(big.list === -1 && big.year1 === -1, "Drata Foundation list stops at 50 employees");
  const comp = box.fn({ platform: "comp-ai", band: "1-20", auditor: 30000, trust: "none", quest: "none", ctm: false, tprm: false, ftr: false, tools: false });
  check(comp.list === -1 && comp.year1 === -1, "Comp AI stays unknown");
  check(box.line("51", 30000).indexOf("No published AWS list") === 0, "51 or more has no published AWS list: " + box.line("51", 30000));
}

function eorCost() {
  const rel = "compare/deel-vs-rippling-eor-hidden-fx-and-offboarding-fees/index.html";
  const html = read(rel);
  const fn = extractBalanced(html, "function calcEor");
  const monthFn = extractBalanced(html, "function eorRipplingMonth");
  const lineFn = extractBalanced(html, "function eorScenario");
  const moneyFn = extractBalanced(html, "function eorMoney");
  check(!!fn && !!monthFn && !!lineFn && !!moneyFn, "missing eor math");
  check(html.indexOf("/go/deel") === -1 && html.indexOf("/go/rippling") === -1, "no Deel or Rippling affiliate redirect");
  check(html.indexOf("sponsored") === -1, "no sponsored affiliate markup");
  check(html.indexOf("https://www.deel.com/pricing/") !== -1, "plain Deel pricing link");
  check(html.indexOf("https://www.rippling.com/pricing") !== -1, "plain Rippling pricing link");
  const box = {};
  vm.createContext(box);
  vm.runInContext(monthFn + "\n" + fn + "\n" + lineFn + "\n" + moneyFn + "\nthis.fn=calcEor;\nthis.line=eorScenario;\nthis.money=eorMoney;", box);
  const base = { employees: 1, salary: 5000, employerPct: 0, allowances: 0, depositTenths: 10, ripplingMode: "unknown", ripplingFee: 499, fxPct: 0, payMethod: "none", platform8: false };
  const def = box.fn(base);
  check(def.deelYear === 7188 && def.deposit === 5599 && def.ripplingYear === -1 && def.vendorCents === 718800, "default is Deel $7,188 and a $5,599 deposit, Rippling unknown");
  check(idText(html, "shell-product") === "Deel management fee, " + def.employees + " employee", "Deel static product");
  check(idText(html, "shell-big") === box.money(def.vendorCents), "Deel static Year-1 " + idText(html, "shell-big"));
  check(idText(html, "shell-amt-base") === box.money(def.deelYear * 100), "Deel static fee");
  check(idText(html, "shell-amt-seats") === box.money(def.deposit * 100), "Deel static deposit");
  check(idText(html, "shell-amt-hidden") === box.money(def.ripplingYear), "Deel static Rippling");
  check(idText(html, "shell-sticker") === box.money(def.deelYear * 100), "Deel static sticker");
  check(idText(html, "shell-gap") === box.money(def.deposit * 100), "Deel static gap");
  check(html.indexOf("2026-11-08T06:05:08+00:00") !== -1 && html.indexOf("2026-11-09") === -1, "Deel check date stays 2026-11-08");
  const line = box.line(def.deelYear, def.ripplingYear, "unknown");
  check(line.indexOf("Lowest Year-1 cost") === -1, "default is not a ranking: " + line);
  check(line.indexOf("not a ranking") !== -1 && line.indexOf("unknown") !== -1, line);
  const blog = box.fn(Object.assign({}, base, { ripplingMode: "blog" }));
  check(blog.ripplingYear === 5988, "blog figure treated as $499 per employee is $5,988");
  const blogLine = box.line(blog.deelYear, blog.ripplingYear, "blog");
  check(blogLine.indexOf("Lowest Year-1 cost") === -1, "blog mode is not a winner: " + blogLine);
  check(blogLine.indexOf("does not say per employee") !== -1 && blogLine.indexOf("$5,988") !== -1, blogLine);
  const entered = box.fn(Object.assign({}, base, { ripplingMode: "entered", ripplingFee: 400 }));
  check(entered.ripplingYear === 4800, "entered fee stays a per-employee assumption");
  const enteredLine = box.line(entered.deelYear, entered.ripplingYear, "entered");
  check(enteredLine.indexOf("Lowest Year-1 cost") === -1 && enteredLine.indexOf("you entered") !== -1, enteredLine);
  const cad = box.fn(Object.assign({}, base, { payMethod: "pad" }));
  check(cad.payIncomplete === true && cad.payCents === -1 && cad.vendorCents === 718800, "CAD fee stays out of the USD subtotal");
  const aud = box.fn(Object.assign({}, base, { payMethod: "becs" }));
  check(aud.payIncomplete === true && aud.vendorCents === 718800, "AUD fee stays out of the USD subtotal");
  const five = box.fn(Object.assign({}, base, { employees: 5 }));
  check(five.deelYear === 35940 && five.deposit === 27995, "five employees scale the fee and the deposit");
  const fx = box.fn(Object.assign({}, base, { fxPct: 2 }));
  check(fx.fxYear === 1200 && fx.vendorCents === 838800 && fx.deelYear === 7188, "FX is an assumption on the pass-through, not a change to the $599 fee");
  const high = box.fn(Object.assign({}, base, { depositTenths: 15 }));
  check(high.deposit === 8399, "1.5 times monthly charges");
  check(box.line(7188, -1, "unknown").indexOf("Lowest Year-1 cost") === -1, "incomplete comparison is not a ranking");
}

function hipaaVoice() {
  const rel = "compliance/ai-voice-and-transcription-hipaa-baa-matrix-2026/index.html";
  const html = read(rel);
  const fn = extractBalanced(html, "function calcHipaa");
  const yearFn = extractBalanced(html, "function hvYear");
  const capFn = extractBalanced(html, "function hvCaption");
  check(!!fn && !!yearFn && !!capFn, "missing hipaa voice math");
  check(html.indexOf("/go/") === -1, "no affiliate redirect");
  check(html.indexOf("sponsored") === -1, "no sponsored markup");
  check(html.indexOf("$99.99") === -1, "do not invent Otter's $99.99 annual total");
  const quote = (html.match(/id="shell-quote">([^<]*)</) || [])[1] || "";
  check(quote === "Published seat list prices, not a full cost", "neutral result label: " + quote);
  check(quote.indexOf("True Year-1 cost") === -1, "this page does not label one vendor as the Year-1 cost");
  check(html.indexOf("Lowest Year-1 cost") === -1 && html.indexOf("Winner") === -1, "no ranking label");
  check(html.indexOf("necessary but not sufficient") !== -1, "BAA scope line");
  const ctaAt = html.indexOf('id="shell-cta"');
  const cta = html.slice(ctaAt, html.indexOf("</a>", ctaAt));
  check(cta.indexOf('href="#hv-matrix"') !== -1, "matrix CTA is internal");
  check(cta.indexOf("vendor-cta") === -1 && cta.indexOf("data-vendor") === -1, "internal CTA is not a vendor click");
  const box = {};
  vm.createContext(box);
  const moneyFn = extractBalanced(html, "function hvMoney");
  vm.runInContext(yearFn + "\n" + capFn + "\n" + moneyFn + "\n" + fn + "\nthis.fn=calcHipaa;\nthis.cap=hvCaption;\nthis.money=hvMoney;", box);
  check(box.cap(1, true) === "1 seat, annual billing, BAA required. Not a ranking.", "1 seat grammar: " + box.cap(1, true));
  check(box.cap(5, false) === "5 seats, monthly billing, BAA required. Not a ranking.", box.cap(5, false));
  const def = box.fn({ seats: 5, billing: "annual" });
  check(def.zoomYear === 84960 && def.fathomYear === 90000 && def.granolaYear === 210000, "5 annual seats: Zoom $849.60, Fathom $900, Granola $2,100");
  check(idText(html, "shell-big") === "Not a ranking", "HIPAA static total is not one vendor");
  check(idText(html, "shell-product") === "Published seat list prices", "HIPAA static product");
  check(idText(html, "shell-amt-base") === box.money(def.zoomYear), "HIPAA static Zoom");
  check(idText(html, "shell-amt-seats") === box.money(def.fathomYear), "HIPAA static Fathom");
  check(idText(html, "shell-amt-hidden") === box.money(def.granolaYear), "HIPAA static Granola");
  check(idText(html, "hv-caption") === box.cap(5, true), "HIPAA static caption");
  check(def.firefliesBase === 234000 && def.otterYear === -1 && def.assemblyYear === -1 && def.deepgramYear === -1, "Fireflies base is not a HIPAA total; Otter, AssemblyAI, and Deepgram stay unknown");
  const one = box.fn({ seats: 1, billing: "annual" });
  check(one.fathomSeats === 2 && one.fathomYear === 36000, "Fathom bills a 2-seat minimum");
  const monthly = box.fn({ seats: 5, billing: "monthly" });
  check(monthly.zoomYear === 101940 && monthly.fathomYear === 114000 && monthly.firefliesBase === -1, "monthly Zoom and Fathom; Fireflies HIPAA is annual only");
}

function smartDisputes() {
  const rel = "pricing/chargeflow-vs-stripe-smart-disputes-year-1-cost/index.html";
  const html = read(rel);
  const fn = extractBalanced(html, "function calcSmartDisputes");
  check(!!fn, "missing smart disputes math");
  check(html.indexOf("/go/") === -1 && html.indexOf("sponsored") === -1, "no Chargeflow affiliate link");
  check(html.indexOf("0.4%") === -1, "do not use 0.4% as a current Chargeback Protection price");
  check(html.indexOf("Chargeback Protection is not listed") !== -1, "Chargeback Protection status note");
  const box = {};
  vm.createContext(box);
  vm.runInContext(fn + "\nthis.fn=calcSmartDisputes;", box);
  const def = box.fn({ disputes: 10, amount: 100, win: 50 });
  check(def.manual === 270000 && def.smart === 360000 && def.chargeflow === 330000, "default year cents " + def.manual + " " + def.smart + " " + def.chargeflow);
  const high = box.fn({ disputes: 10, amount: 20, win: 50 });
  check(high.chargeflow < high.manual, "a small disputed amount can make Chargeflow less than manual");
  const none = box.fn({ disputes: 10, amount: 100, win: 0 });
  check(none.smartFee === 0 && none.cfFee === 0 && none.smart === none.chargeflow, "a 0% win rate drops the success fees");
  check(none.manual === none.received + none.countered, "losses still keep the countered fee");
}

function hubspotPayments() {
  const rel = "pricing/hubspot-payments-vs-stripe-platform-fee-year-1-cost/index.html";
  const html = read(rel);
  const fn = extractBalanced(html, "function calcHubspotPayments");
  check(!!fn, "missing HubSpot payments math");
  check(html.indexOf("/go/") === -1 && html.indexOf("sponsored") === -1, "no HubSpot affiliate link");
  check(html.indexOf("The 0.75% platform fee applies on top of Stripe's own fees. On bank debits, that 0.75% is uncapped.") !== -1, "platform fee note once");
  check(html.split("On bank debits, that 0.75% is uncapped.").length === 2, "uncapped note is not repeated");
  const box = {};
  vm.createContext(box);
  vm.runInContext(fn + "\nthis.fn=calcHubspotPayments;", box);
  const base = { card: 10000, avg: 100, intl: 0, ach: 0, stripePct: 2.9, stripeFixed: 0.3, promo: "no", ukIntl: "eea" };
  const def = box.fn(Object.assign({ country: "us" }, base));
  check(def.hubspot1 === 408000 && def.hubspot2 === 408000 && def.stripe1 === 474000 && def.stripe2 === 474000, "US default cents " + def.hubspot1 + " " + def.stripe1);
  const promo = box.fn(Object.assign({}, base, { country: "us", promo: "yes" }));
  check(promo.hubspot1 === 348000 && promo.hubspot2 === 408000 && promo.stripe1 === 474000, "promotion drops only HubSpot Year 1");
  const foreign = box.fn(Object.assign({}, base, { country: "us", intl: 100 }));
  check(foreign.hubspot1 === 588000 && foreign.stripe1 === 474000, "US foreign cards use 4.4% on HubSpot payments only");
  const uk = box.fn(Object.assign({}, base, { country: "uk", intl: 100, ukIntl: "eea" }));
  const ukFar = box.fn(Object.assign({}, base, { country: "uk", intl: 100, ukIntl: "noneea" }));
  check(uk.hubspot1 === 360000 && ukFar.hubspot1 === 450000, "UK international adders " + uk.hubspot1 + " " + ukFar.hubspot1);
  const other = box.fn(Object.assign({}, base, { country: "other" }));
  check(other.offered === false && other.hubspot1 === null && other.stripe1 === 474000, "other countries keep only the Stripe path");
  const ach = box.fn({ country: "us", card: 2000, avg: 2000, intl: 0, ach: 100, stripePct: 2.9, stripeFixed: 0.3, promo: "no", ukIntl: "eea" });
  check(ach.achProcSample === 1000 && ach.stripeAchSample === 500, "ACH caps: HubSpot $10, Stripe $5");
  const ukAch = box.fn({ country: "uk", card: 2000, avg: 2000, intl: 0, ach: 100, stripePct: 2.9, stripeFixed: 0.3, promo: "no", ukIntl: "eea" });
  check(ukAch.stripeAchUnknown === true && ukAch.stripeAchSample === null, "non-US Stripe bank debit stays unknown");
}

function esignYear1() {
  const rel = "pricing/pandadoc-vs-docusign-vs-jotform-sign-year-1-cost/index.html";
  const html = read(rel);
  const fn = extractBalanced(html, "function calcEsign");
  const formulaFn = extractBalanced(html, "function esFormula");
  const ratesFn = extractBalanced(html, "function esDefaultRates");
  const moneyFn = extractBalanced(html, "function esMoney");
  const rateFn = extractBalanced(html, "function esRate");
  check(!!fn && !!formulaFn && !!ratesFn && !!moneyFn && !!rateFn, "missing e-sign math");
  check(html.indexOf('rel="sponsored nofollow noopener"') !== -1, "Jotform link is sponsored");
  check(html.indexOf("https://www.pandadoc.com/pricing/") !== -1, "plain PandaDoc link");
  check(html.split("Paid partnership with Jotform (#JotformPartner)").length === 2, "one Jotform partnership line");
  const box = {};
  vm.createContext(box);
  vm.runInContext([fn, formulaFn, ratesFn, moneyFn, rateFn, "this.fn=calcEsign;this.formula=esFormula;this.rates=esDefaultRates;"].join("\n"), box);
  const base = { seats: 3, docs: 20, billing: "annual", hipaa: "no", auto: 0, stdRate: 3.6, bpRate: 5.8 };
  const def = box.fn(base);
  check(def.starterSeat === 68400 && def.businessSeat === 176400, "PandaDoc annual seats " + def.starterSeat);
  check(def.standard === 90000 && def.businessPro === 144000 && def.over === 0, "DocuSign annual within allowance");
  check(def.jfName === "Bronze" && def.jfOne === 40800 && def.jfPer === 122400, "Jotform one account vs per user");
  check(def.personal === "off", "Personal stays off for 3 senders");
  const math = box.formula(def);
  check(html.indexOf(math) !== -1, "static formula matches the default");
  check(math.indexOf("DocuSign counts sent envelopes") === -1, "formula does not repeat the intro");
  const high = box.fn(Object.assign({}, base, { docs: 100 }));
  check(high.over === 900 && high.standard === 414000 && high.businessPro === 666000, "annual overage " + high.standard + " " + high.businessPro);
  check(high.jfOne === 40800, "100 signed documents still fits Bronze");
  const silver = box.fn(Object.assign({}, base, { docs: 101 }));
  check(silver.jfName === "Silver" && silver.jfOne === 46800, "Silver starts at 101");
  const gold = box.fn(Object.assign({}, base, { docs: 251 }));
  check(gold.jfName === "Gold" && gold.jfOne === 118800, "Gold starts at 251");
  const enterprise = box.fn(Object.assign({}, base, { docs: 1001 }));
  check(enterprise.jfQuote === "quote (Enterprise)" && enterprise.jfOne === null, "over 1,000 is a Jotform quote");
  const monthly = box.fn(Object.assign({}, base, { billing: "monthly", stdRate: 5.4, bpRate: 7.8 }));
  check(monthly.starterSeat === 126000 && monthly.standard === 162000 && monthly.jfOne === 46800, "month-to-month within allowance");
  const monthlyOver = box.fn({ seats: 3, docs: 50, billing: "monthly", hipaa: "no", auto: 0, stdRate: 5.4, bpRate: 7.8 });
  check(monthlyOver.over === 240 && monthlyOver.standard === 291600 && monthlyOver.businessPro === 421200, "month-to-month overage " + monthlyOver.standard);
  const hipaa = box.fn(Object.assign({}, base, { hipaa: "yes" }));
  check(hipaa.pandaQuote === "quote (Enterprise)" && hipaa.dsQuote === "quote (Enhanced)", "HIPAA quotes");
  check(hipaa.starterSeat === null && hipaa.standard === null && hipaa.jfName === "Gold" && hipaa.jfOne === 118800, "HIPAA keeps Jotform Gold");
  const auto = box.fn(Object.assign({}, base, { auto: 50 }));
  check(auto.autoMonth === 10 && auto.creditUnknown === true && auto.starterSeat === 68400, "automation credit pack stays unknown");
  const one = box.fn({ seats: 1, docs: 5, billing: "annual", hipaa: "no", auto: 0, stdRate: 3.6, bpRate: 5.8 });
  check(one.personal === "price" && one.personalCents === 12000 && one.jfOne === 0, "one sender inside Personal and Starter");
  const oneOver = box.fn(Object.assign({}, one, { docs: 6 }));
  const overPersonal = box.fn({ seats: 1, docs: 6, billing: "annual", hipaa: "no", auto: 0, stdRate: 3.6, bpRate: 5.8 });
  check(overPersonal.personal === "over" && overPersonal.personalCents === null, "Personal does not sell extra envelopes");
  const cap = box.fn(Object.assign({}, base, { seats: 51 }));
  check(cap.dsQuote === "quote (Enhanced)" && cap.standard === null && cap.starterSeat === 1162800, "above 50 users leaves DocuSign as a quote");
  check(box.rates("annual").std === 360 && box.rates("monthly").bp === 780, "third-party starting rates");
  check(oneOver.docs === 6, "input passes through");
}

function apolloYear() {
  const html = fs.readFileSync(path.join(root, "pricing/apollo-vs-zoominfo-vs-sales-navigator-year-1-cost/index.html"), "utf8");
  const fn = extractBalanced(html, "function calcApolloYear");
  check(!!fn, "missing Apollo year math");
  const box = {};
  vm.createContext(box);
  vm.runInContext(fn + "\nthis.fn = calcApolloYear;", box);
  const base = { seats: 5, billing: "annual", emails: 300, phones: 30, plan: "professional", addon: "", ziPlatform: 14995, ziSeat: 1500, sn: "core" };
  const day = box.fn(base);
  check(day.apolloYear === 474000 && day.apolloSeat === 474000, "apollo professional annual " + day.apolloYear);
  check(day.snYear === 539940 && day.ziYear === 2249500 && day.split === 833940, "navigator zoominfo and split");
  check(day.need === 32400 && day.included === 240000 && day.shortfall === 0 && day.addonCost === 0, "default credits");
  check(day.exports === 19800 && day.ziSeats === 5, "default exports");
  const monthlyOrg = box.fn(Object.assign({}, base, { plan: "organization", billing: "monthly" }));
  check(monthlyOrg.forcedAnnual === true && monthlyOrg.apolloYear === 714000 && monthlyOrg.billed === 5, "organization monthly uses the annual price");
  const orgMin = box.fn(Object.assign({}, base, { plan: "organization", seats: 2 }));
  check(orgMin.billed === 3 && orgMin.apolloSeat === 428400, "organization bills at least 3 seats");
  const custom = box.fn(Object.assign({}, base, { plan: "custom" }));
  check(custom.apolloYear === null && custom.split === 833940, "custom is a quote and the basic split stays priced");
  const plus = box.fn(Object.assign({}, base, { sn: "plus" }));
  check(plus.snYear === null && plus.split === null, "advanced plus is a quote");
  const over = box.fn(Object.assign({}, base, { sn: "advanced", seats: 6 }));
  check(over.snYear === null && over.snSeat === null, "advanced above five seats is unknown");
  const blank = box.fn(Object.assign({}, base, { plan: "basic", billing: "monthly", seats: 1, emails: 3000, phones: 0 }));
  check(blank.shortfall === 6000 && blank.apolloSeat === 78000 && blank.apolloYear === null, "blank add-on leaves a shortfall unknown");
  const priced = box.fn(Object.assign({}, base, { plan: "basic", billing: "monthly", seats: 1, emails: 3000, phones: 0, addon: "0.10" }));
  check(priced.addonCost === 60000 && priced.apolloYear === 138000, "typed add-on price");
  const zero = box.fn(Object.assign({}, base, { plan: "basic", billing: "monthly", seats: 1, emails: 3000, phones: 0, addon: "0" }));
  check(zero.addonCost === 0 && zero.apolloYear === 78000, "an entered zero is a real zero");
  const ziSmall = box.fn(Object.assign({}, base, { seats: 1 }));
  check(ziSmall.ziSeats === 3 && ziSmall.ziYear === 1949500, "zoominfo estimate keeps a 3-seat minimum");
  const monthly = box.fn(Object.assign({}, base, { billing: "monthly" }));
  check(monthly.apolloYear === 594000 && monthly.snYear === 719940, "monthly rates are not the annual rates");
  const free = box.fn(Object.assign({}, base, { plan: "free", emails: 0, phones: 0 }));
  check(free.apolloYear === 0 && free.included === 4500, "free is a published zero");
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
  shopifyReserve();
  intercomFreshdesk();
  stripeRadar();
  pipedriveSalesforce();
  ssoTax();
  soc2Cost();
  eorCost();
  hipaaVoice();
  smartDisputes();
  hubspotPayments();
  esignYear1();
  apolloYear();
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
