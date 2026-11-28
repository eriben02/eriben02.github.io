"""Chargeback cost calculator.

Sources checked 2026-11-28:
- https://stripe.com/us/pricing: dispute received $15, not returned. Dispute
  countered $15 on a manual response, returned only if you win. Dispute appealed
  $15, not returned. Smart Disputes is 30% of the disputed amount on a win.
  Chargeback Protection is not listed.
- https://docs.stripe.com/payments/analytics/disputes: a Protected outcome is
  part of deprecated Chargeback Protection.
- https://stripe.com/legal/chargeback-protection: last updated 3 June 2019.
  The fee is the one Stripe sends by email or shows in the Dashboard.
  A 2019 launch price is not used.
- https://help.shopify.com/en/manual/payments/chargebacks/chargeback-process:
  United States fee $15, returned if you win.
- https://www.paddle.com/help/manage/risk-prevention/understanding-chargebacks-with-paddle:
  20 USD, not returned if the dispute is won.
- https://www.chargeflow.io/pricing: Automation is 25% of the recovered amount,
  no monthly fee, and the 25% does not include the dispute fee.

Default check (Stripe):
2,000 orders/mo x $120 x 12 = $2,880,000 sales.
0.65% of 24,000 orders = 156 disputes.
156 x $120 = $18,720 disputed.
Received fees 156 x $15 = $2,340.
Counter fee kept on the 80% not won = $1,872.
Staff prep, a planning assumption, 156 x $30 = $4,680.
Unrecovered sales at a 20% win rate = $14,976.
Manual drain = 2,340 + 1,872 + 4,680 + 14,976 = $23,868.
Chargeflow, 65% win rate is our assumption, 25% of recovered, received fee stays,
counter fee when Chargeflow files is unknown and is not added:
  gross recovered = $12,168
  success fee = $3,042
  net = $9,126
  unrecovered = $6,552
  drain = 2,340 + 6,552 + 3,042 = $11,934
  savings vs manual = $11,934
Paddle at $20, not returned: fees $3,120, manual drain $22,776, Chargeflow drain $12,714.
"""
import os
import shutil

from layout import BASE_DIR, PUBLIC_DIR, WORKBENCH_JS, render_page

TITLE = "Stripe chargeback fee: $15 received"
DESCRIPTION = (
    "Every chargeback costs the order plus a processor dispute fee. "
    "Chargeflow Automation is 25% of the amount recovered, with no monthly fee."
)
LEAD = DESCRIPTION
H1 = "What does a chargeback cost?"

CF = "https://www.chargeflow.io/"
SMART = "pricing/chargeflow-vs-stripe-smart-disputes-year-1-cost/"

TEMPLATE = r"""
<section class="hero editorial-hero editorial-hero-wrap">
  <h1>%%H1%%</h1>
  <p class="lead">%%LEAD%%</p>
</section>

<div class="unified-inspector-tray">
<section class="calc-box editorial-workbench" aria-labelledby="cb-heading">
  <h2 id="cb-heading" class="sr-only-control">Chargeback cost and recovery calculator</h2>
  <div class="workbench-grid">
    <div class="wb-col-controls">
      <div class="wb-col-title">Estimate your dispute loss</div>
      <div class="wb-controls-stack">
        <div class="wb-control-item">
          <label class="wb-control-label" for="cb-processor">Payment processor</label>
          <select id="cb-processor" class="wb-tool-select" data-track="calculator-control" data-control="processor">
            <option value="stripe" selected>Stripe ($15 + $15 counter fee)</option>
            <option value="shopify">Shopify Payments ($15 fee)</option>
            <option value="paddle">Paddle ($20 dispute fee)</option>
            <option value="highrisk">High-risk assumption ($25)</option>
          </select>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="cb-orders">Monthly orders <span class="val-pill" id="cb-orders-val">2,000</span></label>
          <div class="wb-slider-row">
            <input type="range" id="cb-orders" min="100" max="25000" step="100" value="2000" aria-label="Monthly orders" data-track="calculator-control" data-control="orders" />
          </div>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="cb-aov">Average order value <span class="val-pill" id="cb-aov-val">$120</span></label>
          <div class="wb-slider-row">
            <input type="range" id="cb-aov" min="20" max="500" step="5" value="120" aria-label="Average order value" data-track="calculator-control" data-control="aov" />
          </div>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="cb-rate">Dispute rate <span class="val-pill" id="cb-rate-val">0.65%</span></label>
          <div class="wb-slider-row">
            <input type="range" id="cb-rate" min="0.10" max="2.00" step="0.05" value="0.65" aria-label="Dispute rate percent" data-track="calculator-control" data-control="dispute-rate" />
          </div>
        </div>
        <p id="cb-monitor" class="wb-budget-subnote">Below the usual Visa 0.75% and Mastercard 1.00% monitoring marks.</p>
      </div>
    </div>

    <div class="wb-col-chart">
      <div class="wb-col-title">Annual Dispute Drain Breakdown</div>
      <div id="cb-vbar" class="wb-vbar-container" aria-live="polite">
        <div class="wb-vbar-row" id="cb-row-lost" style="flex: 63 1 0px;">
          <div class="wb-vbar-block block-hidden"><span class="wb-block-amount" id="cb-amt-lost">$14,976</span></div>
          <div class="wb-callout-item"><div class="wb-leader-line"></div><div class="wb-callout-text"><strong>Cost above list price: Lost sales</strong><span>Unrecovered disputed sales</span></div></div>
        </div>
        <div class="wb-vbar-row" id="cb-row-ops" style="flex: 20 1 0px;">
          <div class="wb-vbar-block block-base"><span class="wb-block-amount" id="cb-amt-ops">$4,680</span></div>
          <div class="wb-callout-item"><div class="wb-leader-line"></div><div class="wb-callout-text"><strong>Hidden Cost: Evidence prep</strong><span id="cb-ops-note">156 disputes x $30 staff handling</span></div></div>
        </div>
        <div class="wb-vbar-row" id="cb-row-fees" style="flex: 18 1 0px;">
          <div class="wb-vbar-block block-seats"><span class="wb-block-amount" id="cb-amt-fees">$4,212</span></div>
          <div class="wb-callout-item"><div class="wb-leader-line"></div><div class="wb-callout-text"><strong>Sticker Fee: Processor dispute fees</strong><span id="cb-fee-note">156 disputes x $15 received, plus $1,872 counter fee kept</span></div></div>
        </div>
      </div>
    </div>

    <div class="wb-result-col" id="cb-result">
      <div class="wb-selected-product">Manual annual drain</div>
      <div class="wb-big-total"><span id="cb-big">$23,868</span> <span class="wb-per-year">/ year</span></div>
      <details class="math-drawer" id="cb-calc-details">
        <summary>Show calculation</summary>
        <div class="math-drawer-body" id="cb-math"></div>
      </details>
      <p class="wb-budget-quote" id="cb-quote">True Year-1 cost</p>
      <p class="wb-budget-subnote" id="cb-sub">+$19,656 (+467%) above advertised price.</p>
      <div class="wb-best-option" id="cb-best">Based on 2,000 orders a month, a $120 average order, and a 0.65% dispute rate on Stripe. <strong>Lowest modeled cost:</strong> Pay-on-performance recovery at $11,934/yr. That is $11,934 less than manual handling ($23,868). Net kept $9,126.</div>
      <div class="cta-stack">
        <a id="cb-primary" class="btn-cta wb-primary-cta" href="%%CF%%" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="chargeflow" data-cta-location="workbench">Recover $9,126/yr net with Chargeflow (save $11,934/yr vs manual) &rarr;</a>
      </div>
    </div>
  </div>
</section>
</div>

<section class="verdict-section" aria-label="Recovery comparison">
  <div id="cb-summary" class="summary-strip" aria-live="polite"></div>
</section>

<section class="hidden-gap-section" aria-labelledby="cb-compare-heading">
  <details class="full-table-disclosure" id="full-table-details">
    <summary class="full-table-summary">
      <div class="full-table-summary-text">
        <h2 id="cb-compare-heading" class="full-table-heading">Compare all tools in this category</h2>
        <span class="full-table-summary-sub">Manual handling, pay-on-performance recovery, Shopify Protect, and pre-dispute alerts</span>
      </div>
      <span class="full-table-toggle-pill">Compare all tools &darr;</span>
    </summary>
    <div class="full-table-body">
      <div class="table-wrap editorial-gap-table mobile-cards">
        <table>
          <caption>Chargeback recovery options for the volume entered above</caption>
          <thead>
            <tr>
              <th>Option</th>
              <th>How you pay</th>
              <th>What this scenario costs</th>
              <th>Coverage note</th>
            </tr>
          </thead>
          <tbody id="cb-tbody"></tbody>
        </table>
      </div>
    </div>
  </details>
</section>

<section>
  <h2>What we are using for the fee facts</h2>
  <ul class="key-list">
    <li><strong>Stripe:</strong> a dispute received fee is $15 and is not returned. A manual response adds a $15 counter fee, which Stripe returns only if you win. This model counters every dispute on the manual path, so the counter fee stays on the share that is not won. An appeal is another $15 and is not returned. Network fees can also apply. This page does not count appeals or network fees, so those amounts stay unknown.</li>
    <li><strong>Shopify Payments:</strong> the United States fee is $15. Shopify's chargeback fee table says the fee is returned if you win. This model returns it on the share the win rate marks as won.</li>
    <li><strong>Paddle:</strong> the chargeback fee is 20 USD, and Paddle does not return it if the dispute is won.</li>
    <li><strong>High-risk:</strong> $25 per dispute is a planning assumption, not a quoted processor fee.</li>
    <li><strong>Manual in-house:</strong> a 20% win rate and $30 of staff time per dispute. Both are planning assumptions.</li>
    <li><strong>Chargeflow Automation:</strong> the 25% does not include the processor dispute fee. If Stripe bills its counter fee when Chargeflow files the response, that amount is unknown and is not added. The 65% win rate is our planning assumption, not a Chargeflow figure. Adjust it to yours.</li>
    <li><strong>Shopify Protect:</strong> covers eligible Shop Pay orders in the United States. It does not cover a standard card gateway or PayPal dispute, so this model does not give it a total for the whole volume.</li>
    <li><strong>Pre-dispute alerts (Ethoca, Verifi RDR, Chargeblast):</strong> priced per alert and quoted. This model does not invent an alert fee.</li>
  </ul>
</section>

<section>
  <h2>Stripe Chargeback Protection</h2>
  <p>Stripe Chargeback Protection is not listed on the US pricing page. Stripe's disputes analytics calls a Protected outcome part of deprecated Chargeback Protection. Terms last updated 3 June 2019 say the fee is sent by email or shown in the Dashboard. The current price is unknown. A 2019 launch price is not used here.</p>
  <p>A Year-1 comparison of a manual Stripe response, Smart Disputes, and Chargeflow Automation is on the <a href="%%ROOT%%%%SMART%%">Chargeflow vs Stripe Smart Disputes</a> page.</p>
  <p class="src-cluster"><a class="src-link" href="https://stripe.com/us/pricing" target="_blank" rel="noopener">Stripe US pricing</a> <span class="src-date">Accessed 2026-11-28</span></p>
  <p class="src-cluster"><a class="src-link" href="https://docs.stripe.com/payments/analytics/disputes" target="_blank" rel="noopener">Stripe disputes analytics</a> <span class="src-date">Accessed 2026-11-28</span></p>
  <p class="src-cluster"><a class="src-link" href="https://stripe.com/legal/chargeback-protection" target="_blank" rel="noopener">Stripe Chargeback Protection terms</a> <span class="src-date">Accessed 2026-11-28</span></p>
  <p class="src-cluster"><a class="src-link" href="https://help.shopify.com/en/manual/payments/chargebacks/chargeback-process" target="_blank" rel="noopener">Shopify chargeback fees</a> <span class="src-date">Accessed 2026-11-28</span></p>
  <p class="src-cluster"><a class="src-link" href="https://www.paddle.com/help/manage/risk-prevention/understanding-chargebacks-with-paddle" target="_blank" rel="noopener">Paddle chargebacks</a> <span class="src-date">Accessed 2026-11-28</span></p>
  <p class="src-cluster"><a class="src-link" href="%%CF%%pricing" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="chargeflow" data-cta-location="sources">Chargeflow pricing</a> <span class="src-date">Accessed 2026-11-28</span></p>
</section>
<script>
function calcChargeback(input) {
  const orders = input.orders;
  const aov = input.aov;
  const rate = input.rate;
  const fee = input.fee;
  const counterFee = input.counterFee || 0;
  const feeReturnedOnWin = !!input.feeReturnedOnWin;
  const annualOrders = orders * 12;
  const gmv = annualOrders * aov;
  const disputes = Math.round(annualOrders * rate);
  const disputed = disputes * aov;
  const fees = disputes * fee;
  const manualWin = 0.20;
  const cfWin = 0.65;
  const successRate = 0.25;
  const opsPerDispute = 30;
  const manualGross = Math.round(disputed * manualWin);
  const manualLost = disputed - manualGross;
  const manualOps = disputes * opsPerDispute;
  const manualNetAfterOps = manualGross - manualOps;
  const manualLossShare = 1 - manualWin;
  const cfLossShare = 1 - cfWin;
  const manualFeeKept = feeReturnedOnWin ? Math.round(disputes * manualLossShare * fee) : fees;
  const cfFeeKept = feeReturnedOnWin ? Math.round(disputes * cfLossShare * fee) : fees;
  const manualCounterKept = Math.round(disputes * manualLossShare * counterFee);
  const unmanaged = disputed + fees;
  const manualLoss = manualFeeKept + manualCounterKept + manualOps + manualLost;
  const recovered = Math.round(disputed * cfWin);
  const successFee = Math.round(recovered * successRate);
  const netRecovered = recovered - successFee;
  const cfLost = disputed - recovered;
  const cfOps = 0;
  const cfLoss = cfFeeKept + cfLost + successFee + cfOps;
  const savings = manualLoss - cfLoss;
  return {
    annualOrders: annualOrders,
    gmv: gmv,
    disputes: disputes,
    disputed: disputed,
    fees: fees,
    feeReturnedOnWin: feeReturnedOnWin,
    counterFee: counterFee,
    manualFeeKept: manualFeeKept,
    cfFeeKept: cfFeeKept,
    manualCounterKept: manualCounterKept,
    manualWin: manualWin,
    manualGross: manualGross,
    manualLost: manualLost,
    manualOps: manualOps,
    manualNetAfterOps: manualNetAfterOps,
    unmanaged: unmanaged,
    manualLoss: manualLoss,
    cfWin: cfWin,
    recovered: recovered,
    successFee: successFee,
    netRecovered: netRecovered,
    cfLost: cfLost,
    cfOps: cfOps,
    cfLoss: cfLoss,
    savings: savings,
    successRate: successRate,
    opsPerDispute: opsPerDispute,
    fee: fee,
    aov: aov,
    orders: orders,
    rate: rate
  };
}

function renderChargeback() {
  const processors = {
    stripe: { fee: 15, counterFee: 15, feeReturnedOnWin: false },
    shopify: { fee: 15, counterFee: 0, feeReturnedOnWin: true },
    paddle: { fee: 20, counterFee: 0, feeReturnedOnWin: false },
    highrisk: { fee: 25, counterFee: 0, feeReturnedOnWin: false }
  };
  const names = {
    stripe: 'Stripe',
    shopify: 'Shopify Payments',
    paddle: 'Paddle',
    highrisk: 'High-risk assumption'
  };
  const processor = document.getElementById('cb-processor').value;
  const spec = processors[processor];
  const orders = parseInt(document.getElementById('cb-orders').value, 10);
  const aov = parseInt(document.getElementById('cb-aov').value, 10);
  const ratePct = parseFloat(document.getElementById('cb-rate').value);
  const rate = ratePct / 100;
  const fee = spec.fee;
  const c = calcChargeback({
    orders: orders,
    aov: aov,
    rate: rate,
    fee: fee,
    counterFee: spec.counterFee,
    feeReturnedOnWin: spec.feeReturnedOnWin
  });
  const money = function(n) {
    const rounded = Math.round(n);
    const sign = rounded < 0 ? '-' : '';
    return sign + '$' + Math.abs(rounded).toLocaleString('en-US');
  };
  document.getElementById('cb-orders-val').textContent = orders.toLocaleString('en-US');
  document.getElementById('cb-aov-val').textContent = money(aov);
  document.getElementById('cb-rate-val').textContent = ratePct.toFixed(2) + '%';
  const monitor = document.getElementById('cb-monitor');
  if (ratePct >= 1) {
    monitor.textContent = 'At or above both the Visa 0.75% and Mastercard 1.00% monitoring marks.';
  } else if (ratePct >= 0.75) {
    monitor.textContent = 'At or above the Visa 0.75% monitoring mark. Still under the Mastercard 1.00% mark.';
  } else {
    monitor.textContent = 'Below the usual Visa 0.75% and Mastercard 1.00% monitoring marks.';
  }
  const feeBar = c.manualFeeKept + c.manualCounterKept;
  const parts = Math.max(c.manualLoss, 1);
  document.getElementById('cb-row-lost').style.flex = (c.manualLost / parts * 100) + ' 1 0px';
  document.getElementById('cb-row-ops').style.flex = (c.manualOps / parts * 100) + ' 1 0px';
  document.getElementById('cb-row-fees').style.flex = (feeBar / parts * 100) + ' 1 0px';
  document.getElementById('cb-amt-lost').textContent = money(c.manualLost);
  document.getElementById('cb-amt-ops').textContent = money(c.manualOps);
  document.getElementById('cb-amt-fees').textContent = money(feeBar);
  document.getElementById('cb-ops-note').textContent = c.disputes.toLocaleString('en-US') + ' disputes x $' + c.opsPerDispute + ' staff handling';
  let feeNote = c.disputes.toLocaleString('en-US') + ' disputes x ' + money(fee);
  if (c.counterFee) {
    feeNote = c.disputes.toLocaleString('en-US') + ' disputes x ' + money(fee) + ' received, plus ' + money(c.manualCounterKept) + ' counter fee kept';
  } else if (c.feeReturnedOnWin) {
    feeNote = c.disputes.toLocaleString('en-US') + ' disputes, ' + money(c.manualFeeKept) + ' kept after wins return the fee';
  }
  document.getElementById('cb-fee-note').textContent = feeNote;
  document.getElementById('cb-big').textContent = money(c.manualLoss);
  document.getElementById('cb-quote').textContent = 'True Year-1 cost';
  document.getElementById('cb-sub').textContent = window.saasbillResultLine(Math.max(0, c.manualLoss - feeBar), feeBar);
  const paths = [
    { id: 'manual', cost: c.manualLoss, name: 'Manual in-house handling' },
    { id: 'chargeflow', cost: c.cfLoss, name: 'Pay-on-performance recovery' }
  ].sort(function(a, b) { return a.cost - b.cost; });
  const lower = paths[0];
  const saveLabel = 'Recover ' + money(c.netRecovered) + '/yr net with Chargeflow (save ' + money(c.savings) + '/yr vs manual)';
  const versus = lower.id === 'chargeflow'
    ? ' That is ' + money(c.savings) + ' less than manual handling (' + money(c.manualLoss) + '). Net kept ' + money(c.netRecovered) + '.'
    : ' Manual handling ' + money(c.manualLoss) + '. Pay-on-performance ' + money(c.cfLoss) + '.';
  document.getElementById('cb-best').innerHTML = 'Based on ' + orders.toLocaleString('en-US') + ' orders a month, a ' + money(aov) + ' average order, and a ' + ratePct.toFixed(2) + '% dispute rate on ' + names[processor] + '. <strong>Lowest modeled cost:</strong> ' + lower.name + ' at ' + money(lower.cost) + '/yr.' + versus;
  const primary = document.getElementById('cb-primary');
  if (lower.id === 'chargeflow') {
    primary.href = '%%CF%%';
    primary.setAttribute('data-vendor', 'chargeflow');
    primary.textContent = saveLabel + ' →';
  } else {
    primary.href = 'https://docs.stripe.com/disputes';
    primary.setAttribute('data-vendor', 'stripe-payments');
    primary.textContent = 'Manual handling is the lower modeled cost (' + money(c.manualLoss) + '/yr) →';
  }
  const row = function(label, formula, val) {
    return '<div class="calc-math-row"><span class="calc-math-label"><strong>' + label + '</strong><span class="calc-math-formula">' + formula + '</span></span><span class="calc-math-val">' + val + '</span></div>';
  };
  const total = function(label, val) {
    return '<div class="calc-math-total"><span>' + label + '</span><span>' + val + '</span></div>';
  };
  const feeRowLabel = c.feeReturnedOnWin ? 'Dispute fee kept on losses' : 'Dispute fee kept';
  const feeFormula = c.feeReturnedOnWin ? '80% of ' + c.disputes.toLocaleString('en-US') + ' x ' + money(fee) : c.disputes.toLocaleString('en-US') + ' x ' + money(fee);
  const cfFeeFormula = c.feeReturnedOnWin ? '35% of ' + c.disputes.toLocaleString('en-US') + ' x ' + money(fee) : c.disputes.toLocaleString('en-US') + ' x ' + money(fee);
  let counterRow = '';
  if (c.counterFee) {
    counterRow = row('Counter fee kept on losses', '80% of ' + c.disputes.toLocaleString('en-US') + ' x ' + money(c.counterFee), money(c.manualCounterKept));
  }
  document.getElementById('cb-math').innerHTML =
    '<div class="calc-math-list">' +
    row('Yearly orders', orders.toLocaleString('en-US') + ' x 12', c.annualOrders.toLocaleString('en-US')) +
    row('Yearly sales', c.annualOrders.toLocaleString('en-US') + ' x ' + money(aov), money(c.gmv)) +
    row('Disputes', c.annualOrders.toLocaleString('en-US') + ' x ' + ratePct.toFixed(2) + '%', c.disputes.toLocaleString('en-US')) +
    row('Disputed sales', c.disputes.toLocaleString('en-US') + ' x ' + money(aov), money(c.disputed)) +
    row(feeRowLabel, feeFormula, money(c.manualFeeKept)) +
    counterRow +
    row('If every dispute is lost with no response', money(c.disputed) + ' + ' + money(c.fees), money(c.unmanaged)) +
    row('Manual gross recovered', '20% of ' + money(c.disputed), money(c.manualGross)) +
    row('Unrecovered disputed sales', money(c.disputed) + ' minus ' + money(c.manualGross), money(c.manualLost)) +
    row('Evidence prep', c.disputes.toLocaleString('en-US') + ' x $' + c.opsPerDispute, money(c.manualOps)) +
    row('Net after prep', money(c.manualGross) + ' minus ' + money(c.manualOps), money(c.manualNetAfterOps)) +
    total('Manual in-house total annual drain', money(c.manualLoss) + ' / yr') +
    row('Chargeflow gross recovered', '65% of ' + money(c.disputed), money(c.recovered)) +
    row('Chargeflow success fee', '25% of ' + money(c.recovered) + ', no monthly fee', money(c.successFee)) +
    row('Net recovered after the success fee', money(c.recovered) + ' minus ' + money(c.successFee), money(c.netRecovered)) +
    row('Unrecovered with Chargeflow', '35% of ' + money(c.disputed), money(c.cfLost)) +
    row('Processor dispute fee with Chargeflow', cfFeeFormula, money(c.cfFeeKept)) +
    row('Chargeflow evidence prep', 'No staff prep in this model', money(c.cfOps)) +
    total('Total annual drain with Chargeflow', money(c.cfLoss) + ' / yr') +
    total('Savings vs manual in-house', money(c.savings) + ' / yr') +
    '</div>';
  const manualMath = 'Disputes = ' + c.disputes.toLocaleString('en-US') + '. Gross recovered at a 20% win rate = ' + money(c.manualGross) + '. Unrecovered sales = ' + money(c.manualLost) + '. Dispute fees kept = ' + money(feeBar) + '. Evidence prep = ' + c.disputes.toLocaleString('en-US') + ' x $30 = ' + money(c.manualOps) + '. Total annual drain = ' + money(c.manualLoss) + '.';
  const cfMath = 'Gross recovered at 65% = ' + money(c.recovered) + '. Success fee = 25% of ' + money(c.recovered) + ' = ' + money(c.successFee) + ', with no monthly fee. Net recovered = ' + money(c.netRecovered) + '. Unrecovered sales = ' + money(c.cfLost) + '. Processor dispute fees kept = ' + money(c.cfFeeKept) + '. Staff prep is not added. Total annual drain = ' + money(c.cfLoss) + '.';
  const mark = function(id) { return lower.id === id ? ' card-lowest best-card' : ''; };
  const cards = document.getElementById('cb-summary');
  cards.innerHTML =
    '<div class="summary-card result-card' + mark('manual') + '">' +
      '<div class="summary-label">Baseline (20% Win Rate)</div>' +
      '<div class="summary-metric">' + money(c.manualLoss) + ' / yr</div>' +
      '<details class="math-drawer"><summary>Show calculation</summary><div class="math-drawer-body">' + manualMath + '</div></details>' +
      '<div class="summary-scenario"><strong>Manual In-House Dispute Handling</strong></div>' +
      '<div class="summary-breakdown">Gross recovered ' + money(c.manualGross) + '. Evidence prep ' + money(c.manualOps) + '. Dispute fees kept ' + money(feeBar) + '.</div>' +
    '</div>' +
    '<div class="summary-card result-card' + mark('chargeflow') + '">' +
      '<div class="summary-label">25% of recovered dollars</div>' +
      '<div class="summary-metric">' + money(c.cfLoss) + ' / yr drain</div>' +
      '<details class="math-drawer"><summary>Show calculation</summary><div class="math-drawer-body">' + cfMath + '</div></details>' +
      '<div class="summary-scenario"><strong>Chargeflow Pay-On-Performance</strong></div>' +
      '<div class="summary-breakdown">Net kept ' + money(c.netRecovered) + ' after a ' + money(c.successFee) + ' success fee.</div>' +
      '<div class="summary-actions"><a class="' + (lower.id === 'chargeflow' ? 'btn-cta' : 'btn-secondary') + '" href="%%CF%%" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="chargeflow" data-cta-location="summary-card">' + (lower.id === 'chargeflow' ? saveLabel + ' →' : 'View Chargeflow →') + '</a></div>' +
    '</div>';
  const rows = [
    ['Chargeflow Pay-On-Performance', '25% of the amount recovered, no monthly fee', money(c.successFee) + ' success fee, ' + money(c.netRecovered) + ' net recovered', 'The processor dispute fee is extra. Staff prep is not added in this model.', '%%CF%%', 'chargeflow', 'View Chargeflow'],
    ['Shopify Protect', 'Eligible Shop Pay orders in the United States', 'No total in this model', 'Does not cover a standard card gateway or PayPal dispute.', 'https://help.shopify.com/en/manual/payments/shopify-protect', 'shopify', 'View Shopify Protect'],
    ['Pre-dispute alerts (Ethoca, Verifi RDR, Chargeblast)', 'Per alert, quoted', 'Not priced in this model', 'Alert fees vary and are not used to choose the lowest cost.', 'https://www.chargeblast.com/', 'chargeblast', 'View Chargeblast'],
    ['Manual In-House Dispute Handling', 'Staff time at $30 per dispute, plus a 20% win rate', money(c.manualLoss) + ' total annual drain', 'Gross recovered ' + money(c.manualGross) + '. Evidence prep ' + money(c.manualOps) + '. Lost sales ' + money(c.manualLost) + '.', 'https://docs.stripe.com/disputes', 'stripe-payments', 'Read dispute docs']
  ];
  document.getElementById('cb-tbody').innerHTML = rows.map(function(r) {
    return '<tr><td data-label="Option"><strong>' + r[0] + '</strong></td><td data-label="How you pay">' + r[1] + '</td><td data-label="What this scenario costs">' + r[2] + '</td><td data-label="Coverage note">' + r[3] + ' <a href="' + r[4] + '" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="' + r[5] + '" data-cta-location="table-row">' + r[6] + ' &rarr;</a></td></tr>';
  }).join('');
  if (typeof window.trackSaaSBillEvent === 'function') {
    window.trackSaaSBillEvent('result_rendered', { page: 'chargeback-fee-and-recovery-calculator', orders: orders, aov: aov, rate: ratePct, processor: processor });
  }
}

['cb-processor', 'cb-orders', 'cb-aov', 'cb-rate'].forEach(function(id) {
  const el = document.getElementById(id);
  el.addEventListener('input', renderChargeback);
  el.addEventListener('change', renderChargeback);
});
renderChargeback();
</script>
"""


def body(prefix):
    html = (
        TEMPLATE.replace("%%H1%%", H1)
        .replace("%%LEAD%%", LEAD)
        .replace("%%CF%%", CF)
        .replace("%%ROOT%%", prefix)
        .replace("%%SMART%%", SMART)
    )
    return html.replace("<script>\n", "<script>\n" + WORKBENCH_JS + "\n", 1)


def copy_to_root(rel):
    src = os.path.join(PUBLIC_DIR, rel)
    dst = os.path.join(BASE_DIR, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src, dst)


def build():
    full_title = TITLE + " – saasbill.io"
    if len(full_title) > 60:
        raise SystemExit("Title is %s chars: %s" % (len(full_title), full_title))
    blob = TITLE + DESCRIPTION + LEAD + TEMPLATE
    if "\u2014" in blob or "&mdash;" in blob:
        raise SystemExit("em dash in the chargeback calculator")
    if "0.4%" in blob or "0.40%" in blob:
        raise SystemExit("do not print 0.40% as a Chargeback Protection price")
    if blob.count("The 65% win rate is our planning assumption, not a Chargeflow figure. Adjust it to yours.") != 1:
        raise SystemExit("the 65% assumption sentence must appear once")
    pages = (
        ("chargeback-fee-and-recovery-calculator/index.html", "/chargeback-fee-and-recovery-calculator/", "../"),
        (
            "pricing/stripe-shopify-chargeback-fee-and-chargeflow-roi-calculator/index.html",
            "/pricing/stripe-shopify-chargeback-fee-and-chargeflow-roi-calculator/",
            "../../",
        ),
    )
    for rel, canonical, prefix in pages:
        render_page(
            rel,
            TITLE,
            DESCRIPTION,
            canonical,
            body(prefix),
            faqs=None,
            published_date="2026-10-30",
        )
        copy_to_root(rel)


if __name__ == "__main__":
    build()
