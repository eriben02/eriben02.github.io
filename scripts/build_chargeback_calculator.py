"""Chargeback cost calculator.

Default check (Stripe, $15 dispute fee, $30 evidence prep per dispute):
2,000 orders/mo x $120 x 12 = $2,880,000 GMV.
0.65% of 24,000 orders = 156 disputes.
156 x $120 = $18,720 disputed sales.
156 x $15 = $2,340 processor dispute fees.
Unmanaged loss (disputed sales + dispute fees, no labor) = $21,060.
Manual 20% win rate:
  gross recovered 156 x 20% x $120 = $3,744
  unrecovered sales = $14,976
  evidence prep 156 x $30 = $4,680
  total annual drain = $2,340 + $4,680 + $14,976 = $21,996
  net after prep = $3,744 - $4,680 = -$936
Chargeflow planning benchmark, 65% win rate, 25% success fee, $0 monthly, $0 prep:
  gross recovered 156 x 65% x $120 = $12,168
  success fee 25% = $3,042
  net recovered = $9,126
  unrecovered sales (35%) = $6,552
  total annual drain = $2,340 + $6,552 + $3,042 = $11,934
  savings vs manual = $21,996 - $11,934 = $10,062
A 0.40% fee on all GMV = $11,520.
The 65% recovery rate is a labeled planning benchmark, not a Chargeflow guarantee.
Stripe's separate $15 counter fee is named on the processor menu and is covered
inside the $30 handling line so it is not added a second time.
"""
from layout import render_page

TITLE = "Stripe &amp; Shopify Chargeback Cost Calculator (2026): Dispute Fees, Lost Revenue &amp; Chargeflow ROI"
DESCRIPTION = (
    "See what chargebacks cost on Stripe and Shopify: lost order value, a dispute fee, "
    "and manual evidence prep, compared with Chargeflow's 25% success fee and a 0.40% fee on all sales."
)
LEAD = (
    "Every chargeback costs the full order value plus a non-refundable $15 to $25 processor dispute fee. "
    "Adjust your monthly orders and dispute rate below to see the annual loss against automated recovery."
)
H1 = TITLE

CF = "https://www.chargeflow.io/"

TEMPLATE = r"""
<section class="hero">
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
            <option value="stripe" selected>Stripe ($15 dispute fee + $15 counter fee)</option>
            <option value="shopify">Shopify Payments ($15 dispute fee)</option>
            <option value="paddle">Paddle ($20 dispute fee)</option>
            <option value="highrisk">High-volume / high-risk ($25 dispute fee)</option>
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
      <div class="wb-col-title">Manual drain, split</div>
      <div id="cb-vbar" class="wb-vbar-container" aria-live="polite">
        <div class="wb-vbar-row" id="cb-row-lost" style="flex: 68 1 0px;">
          <div class="wb-vbar-block block-hidden"><span class="wb-block-amount" id="cb-amt-lost">$14,976</span></div>
          <div class="wb-callout-item"><div class="wb-leader-line"></div><div class="wb-callout-text"><strong>Lost order value</strong><span>80% of disputed sales at a 20% manual win rate</span></div></div>
        </div>
        <div class="wb-vbar-row" id="cb-row-ops" style="flex: 21 1 0px;">
          <div class="wb-vbar-block block-base"><span class="wb-block-amount" id="cb-amt-ops">$4,680</span></div>
          <div class="wb-callout-item"><div class="wb-leader-line"></div><div class="wb-callout-text"><strong>Evidence prep</strong><span id="cb-ops-note">156 disputes x $30</span></div></div>
        </div>
        <div class="wb-vbar-row" id="cb-row-fees" style="flex: 11 1 0px;">
          <div class="wb-vbar-block block-seats"><span class="wb-block-amount" id="cb-amt-fees">$2,340</span></div>
          <div class="wb-callout-item"><div class="wb-leader-line"></div><div class="wb-callout-text"><strong>Dispute fees</strong><span id="cb-fee-note">156 disputes x $15</span></div></div>
        </div>
      </div>
    </div>

    <div class="wb-result-col" id="cb-result">
      <div class="wb-selected-product">Manual annual drain</div>
      <div class="wb-big-total"><span id="cb-big">$21,996</span> <span class="wb-per-year">/ year</span></div>
      <p class="wb-budget-quote" id="cb-quote">Based on 2,000 orders a month, a $120 average order, and a 0.65% dispute rate on Stripe.</p>
      <p class="wb-budget-subnote" id="cb-sub">Unmanaged loss $21,060 (disputed sales + fees). Prep $4,680. A 20% win recovers $3,744, or -$936 after prep.</p>
      <div class="wb-best-option" id="cb-best"><strong>Best option:</strong> <a href="%%CF%%" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="chargeflow" data-cta-location="workbench-best-option">Chargeflow</a> recovers $9,126/yr net after its 25% success fee and saves $10,062/yr vs. manual in-house handling ($11,520/yr for 0.40% GMV protection).</div>
      <div class="cta-stack">
        <a id="cb-primary" class="btn-cta wb-primary-cta" href="%%CF%%" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="chargeflow" data-cta-location="workbench">Recover $9,126/yr net with Chargeflow (save $10,062/yr vs manual) &rarr;</a>
      </div>
      <details class="calc-disclosure" id="cb-calc-details">
        <summary class="calc-disclosure-toggle">See exactly how we calculated this</summary>
        <div class="calc-disclosure-body" id="cb-math"></div>
      </details>
    </div>
  </div>
</section>
</div>

<section class="verdict-section" aria-label="Recovery comparison">
  <div id="cb-summary" class="summary-strip" aria-live="polite"></div>
</section>

<p><strong>Hidden Cost Highlight:</strong> Manual fighting at a 20% win rate still loses 80% of the disputed order value, and evidence prep is priced at $30 per dispute. The dispute fee stays in the total even when a dispute is won.</p>

<section class="hidden-gap-section" aria-labelledby="cb-compare-heading">
  <details class="full-table-disclosure" id="full-table-details">
    <summary class="full-table-summary">
      <div class="full-table-summary-text">
        <h2 id="cb-compare-heading" class="full-table-heading">Compare all tools in this category</h2>
        <span class="full-table-summary-sub">Chargeflow, a percent-of-sales protection fee, Shopify Protect, and doing it yourself</span>
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
  <p class="calc-affiliate-disclosure">Independent calculations. Some vendor links are affiliate links. This never changes our rankings or calculations.</p>
</section>

<section>
  <h2>What we are using for the fee facts</h2>
  <ul class="key-list">
    <li><strong>Stripe:</strong> a cardholder dispute is modeled at a $15 fee. Stripe has also described a separate $15 counter fee when a dispute is challenged without Chargeback Protection. That counter fee is covered inside the $30 evidence-prep line below, so it is not added a second time on top of the $15 dispute fee.</li>
    <li><strong>Shopify Payments:</strong> modeled at $15 per dispute. Shopify refunds that fee in the US when you win. In several other regions the fee is not returned. This calculator keeps the fee in the loss so the total is not optimistic.</li>
    <li><strong>Paddle:</strong> public notes put the dispute fee around $15 to $20. The Paddle option uses $20.</li>
    <li><strong>High-volume or high-risk:</strong> modeled at $25 per dispute, before any monitoring program penalty.</li>
    <li><strong>Manual in-house:</strong> a 20% win rate, plus $30 per dispute for evidence prep and counter handling. At the default volume that prep is 156 x $30 = $4,680, which is more than the $3,744 gross recovered.</li>
    <li><strong>Chargeflow:</strong> $0 monthly and $0 setup in this model, then 25% of recovered dispute dollars only, and $0 evidence prep. The 65% recovery rate is a planning benchmark so the fee is easy to audit. Ask Chargeflow for the win rate on your category before you treat the savings as a forecast.</li>
    <li><strong>Percent of all sales:</strong> 0.40% of yearly GMV. That is the comparison for a protection product billed on every dollar, not only on disputes. Stripe Radar for Fraud Teams is a different product and is often billed per screened payment. We do not treat 0.40% as Radar's only price.</li>
    <li><strong>Shopify Protect:</strong> covers eligible Shop Pay orders in the US. It does not cover a standard card gateway or PayPal dispute.</li>
  </ul>
  <p>Sources: <a href="https://docs.stripe.com/disputes" target="_blank" rel="noopener">Stripe disputes</a>, <a href="https://stripe.com/radar" target="_blank" rel="noopener">Stripe Radar</a>, <a href="https://help.shopify.com/en/manual/payments/chargebacks" target="_blank" rel="noopener">Shopify chargebacks</a>, <a href="%%CF%%" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="chargeflow" data-cta-location="sources">Chargeflow</a>.</p>
</section>

<script>
function calcChargeback(input) {
  const orders = input.orders;
  const aov = input.aov;
  const rate = input.rate;
  const fee = input.fee;
  const annualOrders = orders * 12;
  const gmv = annualOrders * aov;
  const disputes = Math.round(annualOrders * rate);
  const disputed = disputes * aov;
  const fees = disputes * fee;
  const manualWin = 0.20;
  const cfWin = 0.65;
  const successRate = 0.25;
  const radarRate = 0.004;
  const opsPerDispute = 30;
  const manualGross = Math.round(disputed * manualWin);
  const manualLost = disputed - manualGross;
  const manualOps = disputes * opsPerDispute;
  const manualNetAfterOps = manualGross - manualOps;
  const unmanaged = disputed + fees;
  const manualLoss = fees + manualOps + manualLost;
  const recovered = Math.round(disputed * cfWin);
  const successFee = Math.round(recovered * successRate);
  const netRecovered = recovered - successFee;
  const cfLost = disputed - recovered;
  const cfOps = 0;
  const cfLoss = fees + cfLost + successFee + cfOps;
  const savings = manualLoss - cfLoss;
  const radar = Math.round(gmv * radarRate);
  return {
    annualOrders: annualOrders,
    gmv: gmv,
    disputes: disputes,
    disputesMo: disputes / 12,
    disputed: disputed,
    fees: fees,
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
    radar: radar,
    radarRate: radarRate,
    successRate: successRate,
    opsPerDispute: opsPerDispute,
    fee: fee,
    aov: aov,
    orders: orders,
    rate: rate
  };
}

function renderChargeback() {
  const fees = { stripe: 15, shopify: 15, paddle: 20, highrisk: 25 };
  const names = {
    stripe: 'Stripe',
    shopify: 'Shopify Payments',
    paddle: 'Paddle',
    highrisk: 'High-volume / high-risk'
  };
  const processor = document.getElementById('cb-processor').value;
  const orders = parseInt(document.getElementById('cb-orders').value, 10);
  const aov = parseInt(document.getElementById('cb-aov').value, 10);
  const ratePct = parseFloat(document.getElementById('cb-rate').value);
  const rate = ratePct / 100;
  const fee = fees[processor];
  const c = calcChargeback({ orders: orders, aov: aov, rate: rate, fee: fee });
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
  const parts = Math.max(c.manualLoss, 1);
  document.getElementById('cb-row-lost').style.flex = (c.manualLost / parts * 100) + ' 1 0px';
  document.getElementById('cb-row-ops').style.flex = (c.manualOps / parts * 100) + ' 1 0px';
  document.getElementById('cb-row-fees').style.flex = (c.fees / parts * 100) + ' 1 0px';
  document.getElementById('cb-amt-lost').textContent = money(c.manualLost);
  document.getElementById('cb-amt-ops').textContent = money(c.manualOps);
  document.getElementById('cb-amt-fees').textContent = money(c.fees);
  document.getElementById('cb-ops-note').textContent = c.disputes.toLocaleString('en-US') + ' disputes x $' + c.opsPerDispute;
  document.getElementById('cb-fee-note').textContent = c.disputes.toLocaleString('en-US') + ' disputes x ' + money(fee);
  document.getElementById('cb-big').textContent = money(c.manualLoss);
  document.getElementById('cb-quote').textContent = 'Based on ' + orders.toLocaleString('en-US') + ' orders a month, a ' + money(aov) + ' average order, and a ' + ratePct.toFixed(2) + '% dispute rate on ' + names[processor] + '.';
  document.getElementById('cb-sub').textContent = 'Unmanaged loss ' + money(c.unmanaged) + ' (disputed sales + fees). Prep ' + money(c.manualOps) + '. A 20% win recovers ' + money(c.manualGross) + ', or ' + money(c.manualNetAfterOps) + ' after prep.';
  const saveLabel = 'Recover ' + money(c.netRecovered) + '/yr net with Chargeflow (save ' + money(c.savings) + '/yr vs manual)';
  const callout = 'recovers ' + money(c.netRecovered) + '/yr net after its 25% success fee and saves ' + money(c.savings) + '/yr vs. manual in-house handling (' + money(c.radar) + '/yr for 0.40% GMV protection).';
  document.getElementById('cb-best').innerHTML = '<strong>Best option:</strong> <a href="%%CF%%" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="chargeflow" data-cta-location="workbench-best-option">Chargeflow</a> ' + callout;
  document.getElementById('cb-primary').textContent = saveLabel + ' →';
  const row = function(label, formula, val) {
    return '<div class="calc-math-row"><span class="calc-math-label"><strong>' + label + '</strong><span class="calc-math-formula">' + formula + '</span></span><span class="calc-math-val">' + val + '</span></div>';
  };
  const total = function(label, val) {
    return '<div class="calc-math-total"><span>' + label + '</span><span>' + val + '</span></div>';
  };
  document.getElementById('cb-math').innerHTML =
    '<div class="calc-math-list">' +
    row('Yearly orders', orders.toLocaleString('en-US') + ' x 12', c.annualOrders.toLocaleString('en-US')) +
    row('Yearly sales', c.annualOrders.toLocaleString('en-US') + ' x ' + money(aov), money(c.gmv)) +
    row('Disputes', c.annualOrders.toLocaleString('en-US') + ' x ' + ratePct.toFixed(2) + '%', c.disputes.toLocaleString('en-US')) +
    row('Disputed sales', c.disputes.toLocaleString('en-US') + ' x ' + money(aov), money(c.disputed)) +
    row('Processor dispute fees', c.disputes.toLocaleString('en-US') + ' x ' + money(fee), money(c.fees)) +
    row('Unmanaged loss', money(c.disputed) + ' + ' + money(c.fees), money(c.unmanaged)) +
    row('Manual gross recovered', '20% of ' + money(c.disputed), money(c.manualGross)) +
    row('Unrecovered disputed sales', money(c.disputed) + ' minus ' + money(c.manualGross), money(c.manualLost)) +
    row('Evidence prep and counter handling', c.disputes.toLocaleString('en-US') + ' x $' + c.opsPerDispute, money(c.manualOps)) +
    row('Net after prep', money(c.manualGross) + ' minus ' + money(c.manualOps), money(c.manualNetAfterOps)) +
    total('Manual in-house total annual drain', money(c.manualLoss) + ' / yr') +
    row('Chargeflow gross recovered', '65% of ' + money(c.disputed) + ' (planning benchmark)', money(c.recovered)) +
    row('Chargeflow success fee', '25% of ' + money(c.recovered) + ', $0 monthly, $0 setup', money(c.successFee)) +
    row('Net recovered after the success fee', money(c.recovered) + ' minus ' + money(c.successFee), money(c.netRecovered)) +
    row('Unrecovered with Chargeflow', '35% of ' + money(c.disputed), money(c.cfLost)) +
    row('Chargeflow evidence prep', '$0, fully automated', money(c.cfOps)) +
    total('Total annual drain with Chargeflow', money(c.cfLoss) + ' / yr') +
    total('Savings vs manual in-house', money(c.savings) + ' / yr') +
    row('Stripe Chargeback Protection comparison', '0.40% x ' + money(c.gmv), money(c.radar)) +
    '</div>' + counterNote(processor, c, money);
  const manualMath = 'Disputes = ' + c.disputes.toLocaleString('en-US') + '. Gross recovered at a 20% win rate = ' + money(c.manualGross) + '. Unrecovered sales = ' + money(c.manualLost) + '. Processor dispute fees = ' + money(c.fees) + '. Evidence prep = ' + c.disputes.toLocaleString('en-US') + ' x $30 = ' + money(c.manualOps) + '. Total annual drain = ' + money(c.fees) + ' + ' + money(c.manualOps) + ' + ' + money(c.manualLost) + ' = ' + money(c.manualLoss) + '. Net after prep = ' + money(c.manualGross) + ' minus ' + money(c.manualOps) + ' = ' + money(c.manualNetAfterOps) + '.';
  const cfMath = 'Gross recovered at a 65% automated win rate = ' + money(c.recovered) + '. Success fee = 25% of ' + money(c.recovered) + ' = ' + money(c.successFee) + ', with a $0 monthly fee and a $0 setup fee. Net recovered = ' + money(c.netRecovered) + '. Unrecovered sales (35%) = ' + money(c.cfLost) + '. Processor dispute fees = ' + money(c.fees) + '. Evidence prep = $0. Total annual drain = ' + money(c.fees) + ' + ' + money(c.cfLost) + ' + ' + money(c.successFee) + ' = ' + money(c.cfLoss) + '. Savings vs manual = ' + money(c.manualLoss) + ' minus ' + money(c.cfLoss) + ' = ' + money(c.savings) + '. The 65% win rate is a planning benchmark, not a guaranteed Chargeflow win rate.';
  const radarMath = 'Protection fee = 0.40% x ' + money(c.gmv) + ' yearly sales = ' + money(c.radar) + '. That fee is charged on every sale, including orders nobody disputes. Chargeflow success fee on this scenario is ' + money(c.successFee) + ', and only on recovered dollars. The 0.40% fee is ' + money(c.radar - c.successFee) + ' higher than that success fee. Stripe Radar for Fraud Teams is often priced per screened payment, so 0.40% is the percent-of-sales comparison, not Radar\'s only price.';
  const cards = document.getElementById('cb-summary');
  cards.innerHTML =
    '<div class="summary-card result-card">' +
      '<span class="val-pill">Baseline (20% Win Rate)</span>' +
      '<div class="summary-scenario"><strong>Manual In-House Dispute Handling</strong></div>' +
      '<div class="summary-metric">' + money(c.manualLoss) + ' / yr</div>' +
      '<div class="summary-breakdown">Gross recovered ' + money(c.manualGross) + ' vs evidence prep ' + money(c.manualOps) + '. Net after prep ' + money(c.manualNetAfterOps) + '.</div>' +
      '<p class="summary-caveat"><strong>Hidden Cost Highlight:</strong> 80% of disputed sales stays lost, and the $30 per dispute prep cost is inside this drain.</p>' +
      '<details class="calc-disclosure"><summary class="calc-disclosure-toggle">See calculation</summary><div class="calc-disclosure-body">' + manualMath + '</div></details>' +
    '</div>' +
    '<div class="summary-card result-card best-card card-lowest">' +
      '<span class="val-pill">Highest Net Recovery</span>' +
      '<div class="summary-scenario"><strong>Chargeflow Pay-On-Performance</strong></div>' +
      '<div class="summary-metric">' + money(c.netRecovered) + ' net</div>' +
      '<div class="summary-breakdown">$0 a month. 25% only on recovered dollars. 65% win rate is a planning benchmark. Evidence prep $0.</div>' +
      '<details class="calc-disclosure"><summary class="calc-disclosure-toggle">See calculation</summary><div class="calc-disclosure-body">' + cfMath + '</div></details>' +
      '<div class="summary-actions"><a class="btn-cta" href="%%CF%%" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="chargeflow" data-cta-location="summary-card">' + saveLabel + ' &rarr;</a></div>' +
    '</div>' +
    '<div class="summary-card result-card card-hidden">' +
      '<span class="val-pill">Flat Volume Fee</span>' +
      '<div class="summary-scenario"><strong>Stripe Chargeback Protection (0.40% of GMV)</strong></div>' +
      '<div class="summary-metric">' + money(c.radar) + ' / yr</div>' +
      '<div class="summary-breakdown">0.40% x ' + money(c.gmv) + ', charged on every sale whether or not it is disputed.</div>' +
      '<details class="calc-disclosure"><summary class="calc-disclosure-toggle">See calculation</summary><div class="calc-disclosure-body">' + radarMath + '</div></details>' +
    '</div>';
  const rows = [
    ['Chargeflow Pay-On-Performance', '$0 a month, then 25% of recovered dispute dollars', money(c.successFee) + ' success fee, ' + money(c.netRecovered) + ' net recovered', '2-click Stripe and Shopify connection. $0 evidence prep. The 65% win rate is a planning benchmark, not a promise.', '%%CF%%', 'chargeflow', 'View Chargeflow'],
    ['Stripe Chargeback Protection (0.40% of GMV)', '0.40% of yearly sales, disputes or not', money(c.radar) + ' a year', 'Charged on 100% of sales. Not a claim that Radar for Fraud Teams only has this price.', 'https://stripe.com/radar', 'stripe-payments', 'View Stripe Radar'],
    ['Shopify Protect', '$0 on eligible Shop Pay orders in the US', 'No dollar fee in this model', 'Does not cover a standard card gateway or PayPal dispute.', 'https://help.shopify.com/en/manual/payments/shopify-protect', 'shopify', 'View Shopify Protect'],
    ['Manual In-House Dispute Handling', 'Staff time at $30 per dispute plus about a 20% win rate', money(c.manualLoss) + ' total annual drain', 'Gross recovered ' + money(c.manualGross) + '. Evidence prep ' + money(c.manualOps) + '. Lost sales ' + money(c.manualLost) + '.', 'https://docs.stripe.com/disputes', 'stripe-payments', 'Read dispute docs']
  ];
  document.getElementById('cb-tbody').innerHTML = rows.map(function(r) {
    return '<tr><td data-label="Option"><strong>' + r[0] + '</strong></td><td data-label="How you pay">' + r[1] + '</td><td data-label="What this scenario costs">' + r[2] + '</td><td data-label="Coverage note">' + r[3] + ' <a href="' + r[4] + '" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="' + r[5] + '" data-cta-location="table-row">' + r[6] + ' &rarr;</a></td></tr>';
  }).join('');
  if (typeof window.trackSaaSBillEvent === 'function') {
    window.trackSaaSBillEvent('result_rendered', { page: 'chargeback-fee-and-recovery-calculator', orders: orders, aov: aov, rate: ratePct, processor: processor });
  }
}

function counterNote(processor, c, money) {
  if (processor !== 'stripe') return '';
  return '<p>Stripe may also charge a $15 counter fee when you contest a dispute without Chargeback Protection. This model keeps that cost inside the $30 evidence-prep line (' + money(c.manualOps) + '), and does not add another ' + money(c.disputes * 15) + ' on top of the ' + money(c.fees) + ' dispute-fee line.</p>';
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
    del prefix
    return (
        TEMPLATE.replace("%%H1%%", H1)
        .replace("%%LEAD%%", LEAD)
        .replace("%%CF%%", CF)
    )


def build():
    faqs = [
        (
            "How much is a Stripe or Shopify dispute fee?",
            "This calculator uses $15 per dispute for Stripe and for Shopify Payments. Shopify refunds that fee in the US when you win. In several other regions it does not. Paddle is modeled at $20, inside a $15 to $20 range. A high-risk processor is modeled at $25. Stripe's separate $15 counter fee, when you contest without Chargeback Protection, is covered inside the $30 evidence-prep line and is not added a second time.",
        ),
        (
            "What does Chargeflow charge?",
            "In this model Chargeflow has a $0 monthly fee and a $0 setup fee, then 25% of the dispute dollars it recovers, and $0 evidence prep. The 65% recovery figure is a planning benchmark so you can audit the fee. It is not a guaranteed win rate.",
        ),
        (
            "Why compare a 0.40% fee on all sales?",
            "0.40% of yearly sales is $11,520 on $2.88 million, charged whether or not an order is disputed. A 25% fee only on the dollars actually recovered is $3,042 in the default scenario. Stripe Radar for Fraud Teams is often priced per screened payment, so do not read 0.40% as its only rate.",
        ),
    ]
    render_page(
        "chargeback-fee-and-recovery-calculator/index.html",
        TITLE,
        DESCRIPTION,
        "/chargeback-fee-and-recovery-calculator/",
        body("../"),
        faqs=faqs,
    )
    render_page(
        "pricing/stripe-shopify-chargeback-fee-and-chargeflow-roi-calculator/index.html",
        TITLE,
        DESCRIPTION,
        "/pricing/stripe-shopify-chargeback-fee-and-chargeflow-roi-calculator/",
        body("../../"),
        faqs=faqs,
    )


if __name__ == "__main__":
    build()
