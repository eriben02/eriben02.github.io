"""Stripe dispute fee and Radar cost calculator.

Sources checked 2026-11-02:
- https://stripe.com/pricing (US standard): cards 2.9% + 30c domestic, +1% cross-border.
  Dispute received $15. Dispute countered $15, refunded if you win, kept if you lose.
  Appeal $15, not refunded, plus network fees. Smart Disputes 30% of the disputed
  amount on a win only; the received fee still applies. Radar Lite included.
  Standalone 3DS $0.12 per attempt. Refunds do not return the original processing fee.
  Radar pay-as-you-go starting at $0.05 per screened transaction.
- https://stripe.com/radar/pricing: business plans starting at Standard $10/mo,
  Plus $14/mo, Pro $20/mo. Connect plans starting at $20 / $44 / $70 per month.
  Volume tiers are not published.
- https://docs.stripe.com/disputes/measuring: dispute activity above 0.75% is the
  industry line for excessive. Cardholders have up to 120 days. Won and lost
  disputes both count. Visa counts early fraud warnings toward VAMP.

Default example (not a Stripe statistic): 2,000 payments, $100 average order,
0.60% dispute rate, fight 100%, win 50% of those, Smart Disputes off, Radar Lite.
12 disputes. Received fees $180. Counter fee kept on 6 losses $90. Dispute fees
$270/mo ($3,240/yr). Lost orders $600/mo ($7,200/yr). Smart Disputes $0. Radar $0.
Total $870/mo, $10,440 Year-1. Smart Disputes on the same fights is $11,520.
Accepting every dispute is $16,560. Lowest Year-1 cost is manual counter.
"""
import json
import os
import shutil

from layout import BASE_DIR, DATA_DIR, PUBLIC_DIR, render_page, wrap_calculator_shell

TITLE = "Stripe dispute and Radar cost (2026) – saasbill.io"
DESCRIPTION = (
    "Monthly and Year-1 Stripe dispute fees, lost order value, Smart Disputes, "
    "and Radar starting prices at the dispute rate you enter. Checked 2 Nov 2026."
)
H1 = "Stripe dispute and Radar cost"
LEAD = (
    "Twelve disputes a month, from 2,000 card payments at a 0.60% dispute rate, "
    "cost $270 in Stripe dispute fees before any lost orders. "
    "Change the count, the rate, the share you fight, and the Radar plan to see the Year-1 total."
)
REL = "pricing/stripe-radar-and-dispute-fee-calculator-2026/index.html"
CANONICAL = "/pricing/stripe-radar-and-dispute-fee-calculator-2026/"

BODY = r"""
<section class="hero">
  <h1>Stripe dispute and Radar cost</h1>
  <p class="lead">Twelve disputes a month, from 2,000 card payments at a 0.60% dispute rate, cost $270 in Stripe dispute fees before any lost orders. Change the count, the rate, the share you fight, and the Radar plan to see the Year-1 total.</p>
</section>

<div class="unified-inspector-tray">
<section class="calc-box editorial-workbench" aria-labelledby="rd-heading">
  <h2 id="rd-heading" class="sr-only-control">Stripe dispute and Radar cost calculator</h2>
  <div class="workbench-grid">
    <div class="wb-col-controls">
      <div class="wb-col-title">Your dispute rate</div>
      <div class="wb-controls-stack">
        <div class="wb-control-item">
          <label class="wb-control-label" for="rd-payments">Monthly successful card payments <span class="val-pill" id="rd-payments-val">2,000</span></label>
          <div class="wb-slider-row">
            <input type="range" id="rd-payments" min="0" max="20000" step="100" value="2000" aria-label="Monthly successful card payments" data-track="calculator-control" data-control="payments" />
          </div>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="rd-aov">Average order value <span class="val-pill" id="rd-aov-val">$100</span></label>
          <div class="wb-slider-row">
            <input type="range" id="rd-aov" min="10" max="500" step="5" value="100" aria-label="Average order value" data-track="calculator-control" data-control="aov" />
          </div>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="rd-rate">Dispute rate <span class="val-pill" id="rd-rate-val">0.60%</span></label>
          <div class="wb-slider-row">
            <input type="range" id="rd-rate" min="0" max="5" step="0.05" value="0.60" aria-label="Dispute rate percent" data-track="calculator-control" data-control="dispute-rate" />
          </div>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="rd-counter">Share you fight <span class="val-pill" id="rd-counter-val">100%</span></label>
          <div class="wb-slider-row">
            <input type="range" id="rd-counter" min="0" max="100" step="5" value="100" aria-label="Share of disputes you fight" data-track="calculator-control" data-control="counter-share" />
          </div>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="rd-win">Your expected win rate <span class="val-pill" id="rd-win-val">50%</span></label>
          <div class="wb-slider-row">
            <input type="range" id="rd-win" min="0" max="100" step="5" value="50" aria-label="Expected win rate on disputes you fight" data-track="calculator-control" data-control="win-rate" />
          </div>
        </div>
        <div class="wb-quiet-options">
          <div class="wb-quiet-field">
            <label for="rd-smart">Smart Disputes</label>
            <select id="rd-smart" data-track="calculator-control" data-control="smart-disputes">
              <option value="no" selected>Off</option>
              <option value="yes">On</option>
            </select>
          </div>
          <div class="wb-quiet-field">
            <label for="rd-radar">Radar plan, pay monthly</label>
            <select id="rd-radar" data-track="calculator-control" data-control="radar-plan">
              <option value="lite" selected>Lite, included</option>
              <option value="standard">Standard, $10</option>
              <option value="plus">Plus, $14</option>
              <option value="pro">Pro, $20</option>
            </select>
          </div>
        </div>
        <p id="rd-status" class="wb-budget-subnote">Below the 0.75% industry threshold Stripe cites for excessive dispute activity. Won and lost disputes both count. Early fraud warnings also count toward Visa VAMP, and that count is unknown here.</p>
      </div>
    </div>

    <div class="wb-col-chart">
      <div class="wb-col-title">Year-1 dispute and Radar cost</div>
      <div id="rd-vbar" class="wb-vbar-container" aria-live="polite">
        <div class="wb-vbar-row" id="rd-row-lost" style="flex: 69 1 0px;">
          <div class="wb-vbar-block block-hidden"><span class="wb-block-amount" id="rd-amt-lost">$7,200</span></div>
          <div class="wb-callout-item"><div class="wb-leader-line"></div><div class="wb-callout-text"><strong>Lost order value</strong><span id="rd-sub-lost">Orders you do not win back</span></div></div>
        </div>
        <div class="wb-vbar-row" id="rd-row-fees" style="flex: 31 1 0px;">
          <div class="wb-vbar-block block-seats"><span class="wb-block-amount" id="rd-amt-fees">$3,240</span></div>
          <div class="wb-callout-item"><div class="wb-leader-line"></div><div class="wb-callout-text"><strong>Dispute fees</strong><span id="rd-sub-fees">$15 received, plus $15 kept on a lost manual counter</span></div></div>
        </div>
        <div class="wb-vbar-row" id="rd-row-other" style="flex: 8 1 0px;">
          <div class="wb-vbar-block block-base"><span class="wb-block-amount" id="rd-amt-other">$0</span></div>
          <div class="wb-callout-item"><div class="wb-leader-line"></div><div class="wb-callout-text"><strong>Radar and Smart Disputes</strong><span id="rd-sub-other">Radar Lite is included</span></div></div>
        </div>
      </div>
    </div>

    <div class="wb-result-col" id="rd-result">
      <div class="wb-selected-product" id="rd-product">Manual counter, Radar Lite</div>
      <div class="wb-big-total"><span id="rd-big">$10,440</span> <span class="wb-per-year">/ year</span></div>
      <details class="math-drawer" id="rd-calc-details">
        <summary>Show calculation</summary>
        <div class="math-drawer-body" id="rd-math">2,000 payments x 0.60% = 12 disputes. Received fees 12 x $15 = $180. Fights 12, wins 6, losses 6. Counter fee kept 6 x $15 = $90. Dispute fees $270/mo, $3,240/yr. Lost orders 6 x $100 = $600/mo, $7,200/yr. Smart Disputes $0. Radar Lite $0. Total $870/mo, $10,440/yr.</div>
      </details>
      <p class="wb-budget-quote" id="rd-quote">True Year-1 cost</p>
      <p class="wb-budget-subnote" id="rd-sub">$870 / month, before appeal fees, network fees, and 3D Secure.</p>
      <div class="wb-best-option" id="rd-best"><strong>Lowest Year-1 cost:</strong> Manual counter, $10,440. Smart Disputes is $11,520. Accepting every dispute is $16,560.</div>
      <div class="cta-stack">
        <a id="rd-primary" class="btn-cta wb-primary-cta" href="__WHOP_URL__" target="_blank" rel="sponsored nofollow noopener" data-track="vendor-cta" data-vendor="whop" data-cta-location="workbench">See Whop Payments</a>
      </div>
      <p class="summary-caveat">Whop's dispute fee is not on the Stripe pages used here, so it is unknown. The link does not change the totals.</p>
    </div>
  </div>
</section>
</div>

<div id="rd-summary" class="summary-strip" aria-live="polite">
  <div class="summary-card result-card">
    <div class="summary-label">Dispute fees</div>
    <div class="summary-metric" id="rd-sum-fees">$3,240 / yr</div>
    <div class="summary-scenario" id="rd-sum-fees-mo">$270 / month</div>
  </div>
  <div class="summary-card result-card">
    <div class="summary-label">Lost order value</div>
    <div class="summary-metric" id="rd-sum-lost">$7,200 / yr</div>
    <div class="summary-scenario" id="rd-sum-lost-mo">$600 / month</div>
  </div>
  <div class="summary-card result-card">
    <div class="summary-label">Smart Disputes</div>
    <div class="summary-metric" id="rd-sum-smart">$0 / yr</div>
    <div class="summary-scenario" id="rd-sum-smart-mo">$0 / month</div>
  </div>
  <div class="summary-card result-card">
    <div class="summary-label">Radar</div>
    <div class="summary-metric" id="rd-sum-radar">$0 / yr</div>
    <div class="summary-scenario" id="rd-sum-radar-mo">Included</div>
  </div>
</div>

<div class="table-wrap editorial-gap-table mobile-cards">
  <table>
    <caption>Selected path. Appeal fees, network fees, and 3D Secure attempts stay unknown.</caption>
    <thead>
      <tr>
        <th>Line</th>
        <th>Monthly</th>
        <th>Year-1</th>
      </tr>
    </thead>
    <tbody id="rd-tbody">
      <tr><td data-label="Line">Dispute fees</td><td data-label="Monthly">$270</td><td data-label="Year-1">$3,240</td></tr>
      <tr><td data-label="Line">Lost order value</td><td data-label="Monthly">$600</td><td data-label="Year-1">$7,200</td></tr>
      <tr><td data-label="Line">Smart Disputes</td><td data-label="Monthly">$0</td><td data-label="Year-1">$0</td></tr>
      <tr><td data-label="Line">Radar</td><td data-label="Monthly">$0</td><td data-label="Year-1">$0</td></tr>
      <tr><td data-label="Line">Total in this calculator</td><td data-label="Monthly">$870</td><td data-label="Year-1">$10,440</td></tr>
      <tr><td data-label="Line">Appeal fees</td><td data-label="Monthly">unknown</td><td data-label="Year-1">unknown</td></tr>
      <tr><td data-label="Line">Early fraud warnings</td><td data-label="Monthly">unknown</td><td data-label="Year-1">unknown</td></tr>
    </tbody>
  </table>
</div>

<section class="hidden-gap-section" aria-labelledby="rd-compare-heading">
  <h2 id="rd-compare-heading">Three ways to handle the same disputes</h2>
  <p>The win rate is the one you entered. Stripe does not publish a win rate. Smart Disputes uses that same rate on the disputes you choose to fight. Disputes you do not fight are lost orders, plus the $15 received fee.</p>
  <div class="table-wrap editorial-gap-table mobile-cards">
    <table>
      <caption>Year-1 cost of accepting, countering manually, or using Smart Disputes</caption>
      <thead>
        <tr>
          <th>Path</th>
          <th>Dispute fees</th>
          <th>Lost order value</th>
          <th>Smart Disputes</th>
          <th>Radar</th>
          <th>Year-1 total</th>
        </tr>
      </thead>
      <tbody id="rd-compare">
        <tr>
          <td data-label="Path">Accept disputes</td>
          <td data-label="Dispute fees">$2,160</td>
          <td data-label="Lost order value">$14,400</td>
          <td data-label="Smart Disputes">$0</td>
          <td data-label="Radar">$0</td>
          <td data-label="Year-1 total">$16,560</td>
        </tr>
        <tr>
          <td data-label="Path">Manual counter. Lowest Year-1 cost.</td>
          <td data-label="Dispute fees">$3,240</td>
          <td data-label="Lost order value">$7,200</td>
          <td data-label="Smart Disputes">$0</td>
          <td data-label="Radar">$0</td>
          <td data-label="Year-1 total">$10,440</td>
        </tr>
        <tr>
          <td data-label="Path">Smart Disputes</td>
          <td data-label="Dispute fees">$2,160</td>
          <td data-label="Lost order value">$7,200</td>
          <td data-label="Smart Disputes">$2,160</td>
          <td data-label="Radar">$0</td>
          <td data-label="Year-1 total">$11,520</td>
        </tr>
      </tbody>
    </table>
  </div>
</section>

<section>
  <h2>Prices Stripe publishes</h2>
  <div class="table-wrap editorial-gap-table mobile-cards">
    <table>
      <caption>Figures used in the math, checked 2 Nov 2026</caption>
      <thead>
        <tr>
          <th>Item</th>
          <th>Published price</th>
          <th>In this total</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td data-label="Item">Dispute received</td>
          <td data-label="Published price">$15.00 per dispute. In rare cases, network fees also apply.</td>
          <td data-label="In this total">$15 on every dispute, won or lost. Extra network fees are unknown.</td>
        </tr>
        <tr>
          <td data-label="Item">Dispute countered</td>
          <td data-label="Published price">$15.00 per dispute you respond to manually. Refunded if you win. Not refunded if you lose.</td>
          <td data-label="In this total">$15 kept on each manual loss. Not charged when Smart Disputes is on.</td>
        </tr>
        <tr>
          <td data-label="Item">Dispute appealed</td>
          <td data-label="Published price">$15.00, not refunded even if you win. Additional network fees apply.</td>
          <td data-label="In this total">unknown. There is no appeal count on this page.</td>
        </tr>
        <tr>
          <td data-label="Item">Smart Disputes</td>
          <td data-label="Published price">30% of the disputed amount for each dispute you win. No Smart Disputes fee on a loss. The received fee still applies.</td>
          <td data-label="In this total">Only when Smart Disputes is on, and only on wins.</td>
        </tr>
        <tr>
          <td data-label="Item">Radar for businesses</td>
          <td data-label="Published price">Lite included. Standard starting at $10/mo, Plus starting at $14/mo, Pro starting at $20/mo. Pay-as-you-go starting at $0.05 per screened transaction.</td>
          <td data-label="In this total">The monthly starting price of the plan you pick. Exact volume tiers are not published. Pay-as-you-go is unknown here.</td>
        </tr>
        <tr>
          <td data-label="Item">Radar for platforms</td>
          <td data-label="Published price">Connect plans starting at $20, $44, and $70 per month.</td>
          <td data-label="In this total">unknown. This page prices the business plans.</td>
        </tr>
        <tr>
          <td data-label="Item">Cards and 3D Secure</td>
          <td data-label="Published price">2.9% + 30&cent; domestic, plus 1% cross-border. Standalone 3D Secure is $0.12 per attempt. A refund does not return the original processing fee.</td>
          <td data-label="In this total">Not included. Attempt counts and cross-border share are unknown.</td>
        </tr>
      </tbody>
    </table>
  </div>
  <p class="summary-caveat">Checked 2 Nov 2026. <a href="https://stripe.com/pricing" target="_blank" rel="noopener">Stripe pricing</a>. <a href="https://stripe.com/radar/pricing" target="_blank" rel="noopener">Radar pricing</a>. <a href="https://docs.stripe.com/disputes/measuring" target="_blank" rel="noopener">How Stripe measures disputes</a>.</p>
  <ul class="key-list">
    <li>Dispute activity, counted on the dispute date, is what card network monitoring programs use. Stripe cites 0.75% as the industry line for excessive dispute activity.</li>
    <li>Cardholders can dispute a payment for up to 120 days.</li>
    <li>Every dispute counts toward the rate, whether you win it or lose it. The win rate does not lower the rate in the status line.</li>
    <li>Visa counts early fraud warnings toward its VAMP program. This page does not have that count, so it cannot say whether you are inside VAMP.</li>
  </ul>
</section>

<section>
  <h2>What merchants asked around this check</h2>
  <ul class="key-list">
    <li>On 30 Oct 2026 a merchant on Reddit asked whether refunding orders under $100 before they become chargebacks would keep a 7% to 9% would-be dispute rate out of Visa VAMP. Stripe's measuring guide does not say a refund removes a dispute, and early fraud warnings still count. Whether that refund tactic works is unknown. <a href="https://www.reddit.com/r/stripe/comments/1xj7m34/" target="_blank" rel="noopener">Reddit thread</a>.</li>
    <li>On 1 Nov 2026 a merchant on X said Stripe closed their account after one chargeback on about GBP 90,000 of processing. Stripe does not publish a one-chargeback closure rule, so the threshold for that outcome is unknown. <a href="https://x.com/Darrentheadsguy/status/2117006751610421290" target="_blank" rel="noopener">Post on X</a>.</li>
  </ul>
</section>
<script>
function calcStripeRadar(input) {
  var payments = Math.max(0, Math.round(Number(input.payments) || 0));
  var aov = Math.max(0, Number(input.aov) || 0);
  var ratePct = Math.max(0, Number(input.rate) || 0);
  var counterPct = Math.min(100, Math.max(0, Number(input.counter) || 0));
  var winPct = Math.min(100, Math.max(0, Number(input.win) || 0));
  var radarKey = String(input.radar || "lite");
  var radarTable = { lite: 0, standard: 10, plus: 14, pro: 20 };
  var radarKnown = Object.prototype.hasOwnProperty.call(radarTable, radarKey);
  var radarMo = radarKnown ? radarTable[radarKey] : 0;
  var disputes = Math.round(payments * ratePct / 100);
  var fought = Math.round(disputes * counterPct / 100);
  var won = Math.round(fought * winPct / 100);
  var lostFought = fought - won;
  var accepted = disputes - fought;
  var receivedMo = disputes * 15;
  function cost(kind) {
    var fight = kind === "accept" ? 0 : fought;
    var wins = kind === "accept" ? 0 : won;
    var losses = kind === "accept" ? 0 : lostFought;
    var untouched = disputes - fight;
    var counterMo = kind === "manual" ? losses * 15 : 0;
    var smartMo = kind === "smart" ? Math.round(wins * aov * 0.30) : 0;
    var lostMo = Math.round((losses + untouched) * aov);
    var disputeFeesMo = receivedMo + counterMo;
    var totalMo = disputeFeesMo + lostMo + smartMo + radarMo;
    return {
      disputeFeesMo: disputeFeesMo,
      disputeFeesYr: disputeFeesMo * 12,
      lostMo: lostMo,
      lostYr: lostMo * 12,
      smartMo: smartMo,
      smartYr: smartMo * 12,
      radarMo: radarMo,
      radarYr: radarMo * 12,
      counterMo: counterMo,
      totalMo: totalMo,
      totalYr: totalMo * 12
    };
  }
  var manual = cost("manual");
  var smart = cost("smart");
  var accept = cost("accept");
  var selectedKey = input.smart ? "smart" : "manual";
  var selected = selectedKey === "smart" ? smart : manual;
  var low = Math.min(accept.totalYr, manual.totalYr, smart.totalYr);
  var lowestKeys = [];
  if (accept.totalYr === low) lowestKeys.push("accept");
  if (manual.totalYr === low) lowestKeys.push("manual");
  if (smart.totalYr === low) lowestKeys.push("smart");
  var hundredths = Math.round(ratePct * 100);
  var threshold = hundredths > 75 ? "above" : (hundredths === 75 ? "at" : "below");
  return {
    payments: payments,
    aov: aov,
    ratePct: ratePct,
    counterPct: counterPct,
    winPct: winPct,
    disputes: disputes,
    fought: fought,
    won: won,
    lostFought: lostFought,
    accepted: accepted,
    receivedMo: receivedMo,
    receivedYr: receivedMo * 12,
    radarKey: radarKey,
    radarKnown: radarKnown,
    radarMo: radarMo,
    manual: manual,
    smart: smart,
    accept: accept,
    selectedKey: selectedKey,
    selected: selected,
    lowestYr: low,
    lowestKeys: lowestKeys,
    threshold: threshold
  };
}

function rdMoney(n) {
  var v = Math.round(Number(n) || 0);
  return "$" + v.toLocaleString("en-US");
}

function rdRead() {
  return {
    payments: document.getElementById("rd-payments").value,
    aov: document.getElementById("rd-aov").value,
    rate: document.getElementById("rd-rate").value,
    counter: document.getElementById("rd-counter").value,
    win: document.getElementById("rd-win").value,
    smart: document.getElementById("rd-smart").value === "yes",
    radar: document.getElementById("rd-radar").value
  };
}

function rdPathName(key) {
  if (key === "accept") return "Accept disputes";
  if (key === "smart") return "Smart Disputes";
  return "Manual counter";
}

function rdRadarName(key) {
  if (key === "standard") return "Radar Standard, starting at $10/mo";
  if (key === "plus") return "Radar Plus, starting at $14/mo";
  if (key === "pro") return "Radar Pro, starting at $20/mo";
  return "Radar Lite, included";
}

function renderStripeRadar() {
  var input = rdRead();
  var c = calcStripeRadar(input);
  var s = c.selected;
  document.getElementById("rd-payments-val").textContent = c.payments.toLocaleString("en-US");
  document.getElementById("rd-aov-val").textContent = rdMoney(c.aov);
  document.getElementById("rd-rate-val").textContent = c.ratePct.toFixed(2) + "%";
  document.getElementById("rd-counter-val").textContent = c.counterPct + "%";
  document.getElementById("rd-win-val").textContent = c.winPct + "%";
  var status = "Below the 0.75% industry threshold Stripe cites for excessive dispute activity.";
  if (c.threshold === "above") status = "Above the 0.75% industry threshold Stripe cites for excessive dispute activity.";
  if (c.threshold === "at") status = "At the 0.75% industry threshold Stripe cites for excessive dispute activity.";
  document.getElementById("rd-status").textContent = status + " Won and lost disputes both count. Early fraud warnings also count toward Visa VAMP, and that count is unknown here.";
  var otherYr = s.smartYr + s.radarYr;
  var barTotal = Math.max(1, s.lostYr + s.disputeFeesYr + otherYr);
  document.getElementById("rd-row-lost").style.flex = Math.max(8, Math.round(s.lostYr / barTotal * 100)) + " 1 0px";
  document.getElementById("rd-row-fees").style.flex = Math.max(8, Math.round(s.disputeFeesYr / barTotal * 100)) + " 1 0px";
  document.getElementById("rd-row-other").style.flex = Math.max(8, Math.round(otherYr / barTotal * 100)) + " 1 0px";
  document.getElementById("rd-amt-lost").textContent = rdMoney(s.lostYr);
  document.getElementById("rd-amt-fees").textContent = rdMoney(s.disputeFeesYr);
  document.getElementById("rd-amt-other").textContent = rdMoney(otherYr);
  document.getElementById("rd-sub-lost").textContent = c.lostFought + c.accepted + " orders not won back, at " + rdMoney(c.aov);
  document.getElementById("rd-sub-fees").textContent = rdMoney(c.receivedYr) + " received, plus " + rdMoney(s.counterMo * 12) + " counter fee kept on losses";
  document.getElementById("rd-sub-other").textContent = rdRadarName(c.radarKey) + (c.selectedKey === "smart" ? ". Smart Disputes is 30% of each win." : ". Smart Disputes is off.");
  document.getElementById("rd-product").textContent = rdPathName(c.selectedKey) + ", " + rdRadarName(c.radarKey);
  document.getElementById("rd-big").textContent = rdMoney(s.totalYr);
  document.getElementById("rd-sub").textContent = rdMoney(s.totalMo) + " / month. Appeal fees, extra network fees, and 3D Secure attempts are unknown and are not in this total.";
  var lowNames = c.lowestKeys.map(rdPathName).join(" and ");
  var radarNote = c.radarKey === "lite" ? " Radar Lite is included at no extra charge." : " " + rdRadarName(c.radarKey) + ". Stripe does not publish the volume tier, so this Radar line is a starting price.";
  document.getElementById("rd-best").innerHTML = "<strong>Lowest Year-1 cost:</strong> " + lowNames + ", " + rdMoney(c.lowestYr) + ". Accept disputes " + rdMoney(c.accept.totalYr) + ". Manual counter " + rdMoney(c.manual.totalYr) + ". Smart Disputes " + rdMoney(c.smart.totalYr) + ". The win rate is the one you entered, not a Stripe figure." + radarNote;
  document.getElementById("rd-sum-fees").textContent = rdMoney(s.disputeFeesYr) + " / yr";
  document.getElementById("rd-sum-fees-mo").textContent = rdMoney(s.disputeFeesMo) + " / month";
  document.getElementById("rd-sum-lost").textContent = rdMoney(s.lostYr) + " / yr";
  document.getElementById("rd-sum-lost-mo").textContent = rdMoney(s.lostMo) + " / month";
  document.getElementById("rd-sum-smart").textContent = rdMoney(s.smartYr) + " / yr";
  document.getElementById("rd-sum-smart-mo").textContent = c.selectedKey === "smart" ? rdMoney(s.smartMo) + " / month" : "$0 / month";
  document.getElementById("rd-sum-radar").textContent = rdMoney(s.radarYr) + " / yr";
  document.getElementById("rd-sum-radar-mo").textContent = c.radarKey === "lite" ? "Included" : rdMoney(s.radarMo) + " / month, starting price";
  var lines = [
    ["Dispute fees", s.disputeFeesMo, s.disputeFeesYr],
    ["Lost order value", s.lostMo, s.lostYr],
    ["Smart Disputes", s.smartMo, s.smartYr],
    ["Radar", s.radarMo, s.radarYr],
    ["Total in this calculator", s.totalMo, s.totalYr]
  ];
  var body = "";
  lines.forEach(function (row) {
    body += "<tr><td data-label=\"Line\">" + row[0] + "</td><td data-label=\"Monthly\">" + rdMoney(row[1]) + "</td><td data-label=\"Year-1\">" + rdMoney(row[2]) + "</td></tr>";
  });
  body += "<tr><td data-label=\"Line\">Appeal fees</td><td data-label=\"Monthly\">unknown</td><td data-label=\"Year-1\">unknown</td></tr>";
  body += "<tr><td data-label=\"Line\">Early fraud warnings</td><td data-label=\"Monthly\">unknown</td><td data-label=\"Year-1\">unknown</td></tr>";
  body += "<tr><td data-label=\"Line\">3D Secure attempts</td><td data-label=\"Monthly\">unknown</td><td data-label=\"Year-1\">unknown</td></tr>";
  document.getElementById("rd-tbody").innerHTML = body;
  function compareRow(key, path) {
    var name = rdPathName(key);
    if (c.lowestKeys.indexOf(key) !== -1) name += ". Lowest Year-1 cost.";
    return "<tr><td data-label=\"Path\">" + name + "</td><td data-label=\"Dispute fees\">" + rdMoney(path.disputeFeesYr) + "</td><td data-label=\"Lost order value\">" + rdMoney(path.lostYr) + "</td><td data-label=\"Smart Disputes\">" + rdMoney(path.smartYr) + "</td><td data-label=\"Radar\">" + rdMoney(path.radarYr) + "</td><td data-label=\"Year-1 total\">" + rdMoney(path.totalYr) + "</td></tr>";
  }
  document.getElementById("rd-compare").innerHTML = compareRow("accept", c.accept) + compareRow("manual", c.manual) + compareRow("smart", c.smart);
  document.getElementById("rd-math").textContent = c.payments.toLocaleString("en-US") + " payments x " + c.ratePct.toFixed(2) + "% = " + c.disputes + " disputes. Received fees " + c.disputes + " x $15 = " + rdMoney(c.receivedMo) + "/mo (" + rdMoney(c.receivedYr) + "/yr). Fights " + c.fought + ", wins " + c.won + ", losses " + c.lostFought + ", not fought " + c.accepted + ". Counter fee kept on manual losses " + rdMoney(c.manual.counterMo) + "/mo. Selected dispute fees " + rdMoney(s.disputeFeesMo) + "/mo, " + rdMoney(s.disputeFeesYr) + "/yr. Lost order value " + rdMoney(s.lostMo) + "/mo, " + rdMoney(s.lostYr) + "/yr. Smart Disputes " + rdMoney(s.smartMo) + "/mo. Radar " + rdMoney(s.radarMo) + "/mo. Total " + rdMoney(s.totalMo) + "/mo, " + rdMoney(s.totalYr) + "/yr.";
  if (typeof window.trackSaaSBillEvent === "function") {
    window.trackSaaSBillEvent("result_rendered", { page: "stripe-radar", payments: c.payments, rate: c.ratePct, radar: c.radarKey });
  }
}
["rd-payments", "rd-aov", "rd-rate", "rd-counter", "rd-win", "rd-smart", "rd-radar"].forEach(function (id) {
  var el = document.getElementById(id);
  el.addEventListener("input", renderStripeRadar);
  el.addEventListener("change", renderStripeRadar);
});
renderStripeRadar();
</script>
"""

FAQS = [
    (
        "What does Stripe charge when a dispute arrives?",
        "On the US pricing page checked 2 Nov 2026, the dispute received fee is $15.00 per dispute. Stripe says network fees also apply in rare cases. This calculator adds the $15. It does not add a network fee, because that amount is not published as a single figure.",
    ),
    (
        "Is the counter fee refunded if you win?",
        "Yes, for a manual response. Stripe's pricing page says the $15.00 dispute countered fee is refunded if you win and is not refunded if you lose. An appeal is a separate $15.00 fee, and Stripe says that one is not refunded even if you win. This page does not ask for an appeal count, so appeal fees stay unknown.",
    ),
    (
        "What is the 0.75% line?",
        "Stripe's dispute measurement guide says the industry standard treats dispute activity above 0.75% as excessive, and that card network monitoring programs use dispute activity by dispute date. Won and lost disputes both count. Cardholders can dispute for up to 120 days. Visa also counts early fraud warnings toward VAMP. This calculator can see the dispute rate you type. It cannot see early fraud warnings, so that part is unknown.",
    ),
    (
        "What does Radar cost?",
        "Radar Lite is included on standard pricing. Stripe's Radar pricing page lists business plans that start at $10 a month for Standard, $14 for Plus, and $20 for Pro. Pay-as-you-go starts at $0.05 per screened transaction. Connect plans start at $20, $44, and $70 a month. The page does not publish the exact volume tiers, so the business-plan lines in this calculator are starting prices.",
    ),
]


def whop_url():
    with open(os.path.join(DATA_DIR, "affiliate_links.json"), encoding="utf-8") as handle:
        data = json.load(handle)
    url = data["whop"]["destination_url"]
    if "whop.com" not in url:
        raise SystemExit("whop destination_url is missing")
    return url


def copy_to_root(rel):
    src = os.path.join(PUBLIC_DIR, rel)
    dst = os.path.join(BASE_DIR, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src, dst)


def build():
    if len(TITLE) > 60:
        raise SystemExit("Title is %s chars: %s" % (len(TITLE), TITLE))
    if "\u2014" in TITLE or "\u2014" in BODY or "\u2014" in LEAD:
        raise SystemExit("em dash in stripe radar copy")
    body = BODY.replace("__WHOP_URL__", whop_url())
    if "chargeflow" in body.lower():
        raise SystemExit("Chargeflow link slipped into the Stripe Radar page")
    render_page(
        REL,
        TITLE,
        DESCRIPTION,
        CANONICAL,
        wrap_calculator_shell(body),
        faqs=FAQS,
        published_date="2026-11-02",
    )
    copy_to_root(REL)


if __name__ == "__main__":
    build()
