"""Chargeback cost calculator.

Default check (Stripe, $15 fee):
2,000 orders/mo x $120 x 12 = $2,880,000 GMV.
0.65% of 24,000 orders = 156 disputes.
156 x $120 = $18,720 disputed revenue.
156 x $15 = $2,340 dispute fees.
Manual 20% win rate: 80% of disputed revenue ($14,976) + fees = $17,316 loss.
Illustrated Chargeflow recovery at 50% of disputed dollars, 25% success fee:
recovered $9,360, fee $2,340, net kept $7,020.
Chargeflow all-in cost = unsaved revenue $9,360 + success fee $2,340 + dispute fees $2,340 = $14,040.
Savings vs manual = $3,276.
A 0.40% fee on all GMV = $11,520.
The 50% recovery rate is a labeled planning benchmark, not a Chargeflow guarantee.
"""
from layout import render_page

TITLE = "Stripe &amp; Shopify Chargeback Cost Calculator (2026): Dispute Fees, Lost Revenue &amp; Chargeflow ROI"
DESCRIPTION = (
    "See what chargebacks cost on Stripe and Shopify: lost order value plus a dispute fee, "
    "compared with Chargeflow's 25% success fee and a 0.40% fee on all sales."
)
LEAD = (
    "Every chargeback costs the full order value plus a non-refundable $15 to $25 processor dispute fee. "
    "Adjust your monthly orders and dispute rate below to see the annual loss against automated recovery."
)
H1 = TITLE

CF = "https://www.chargeflow.io/"


def body(prefix):
    return f"""
<section class="hero">
  <h1>{H1}</h1>
  <p class="lead">{LEAD}</p>
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
            <option value="stripe" selected>Stripe ($15 dispute fee)</option>
            <option value="shopify">Shopify Payments ($15 dispute fee)</option>
            <option value="paddle">Paddle ($20 of the $15 to $20 range)</option>
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
      <div class="wb-col-title">Manual loss, split</div>
      <div id="cb-vbar" class="wb-vbar-container" aria-live="polite">
        <div class="wb-vbar-row" id="cb-row-lost" style="flex: 86 1 0px;">
          <div class="wb-vbar-block block-hidden"><span class="wb-block-amount" id="cb-amt-lost">$14,976</span></div>
          <div class="wb-callout-item"><div class="wb-leader-line"></div><div class="wb-callout-text"><strong>Lost order value</strong><span>80% of disputed sales at a 20% manual win rate</span></div></div>
        </div>
        <div class="wb-vbar-row" id="cb-row-fees" style="flex: 14 1 0px;">
          <div class="wb-vbar-block block-seats"><span class="wb-block-amount" id="cb-amt-fees">$2,340</span></div>
          <div class="wb-callout-item"><div class="wb-leader-line"></div><div class="wb-callout-text"><strong>Dispute fees</strong><span id="cb-fee-note">156 disputes x $15</span></div></div>
        </div>
      </div>
    </div>

    <div class="wb-result-col" id="cb-result">
      <div class="wb-selected-product">Manual in-house net loss</div>
      <div class="wb-big-total"><span id="cb-big">$17,316</span> <span class="wb-per-year">/ year</span></div>
      <p class="wb-budget-quote" id="cb-quote">Based on 2,000 orders a month, a $120 average order, and a 0.65% dispute rate.</p>
      <p class="wb-budget-subnote" id="cb-sub">156 disputes a year. $18,720 of sales in dispute. $2,340 of dispute fees.</p>
      <div class="wb-best-option" id="cb-best"><strong>Best option:</strong> <a href="{CF}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="chargeflow" data-cta-location="workbench-best-option">Save $3,276/yr with Chargeflow &rarr;</a></div>
      <details class="calc-disclosure" id="cb-calc-details">
        <summary class="calc-disclosure-toggle">See exactly how we calculated this</summary>
        <div class="calc-disclosure-body" id="cb-math"></div>
      </details>
      <div class="cta-stack">
        <a id="cb-primary" class="btn-cta wb-primary-cta" href="{CF}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="chargeflow" data-cta-location="workbench">Save $3,276/yr with Chargeflow &rarr;</a>
      </div>
    </div>
  </div>
</section>
</div>

<section class="verdict-section" aria-label="Recovery comparison">
  <div id="cb-summary" class="summary-strip" aria-live="polite"></div>
</section>

<p><strong>Hidden Cost Highlight:</strong> The dispute fee line counts one processor fee on every dispute. It does not assume the fee comes back if you win.</p>

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
    <li><strong>Stripe:</strong> a cardholder dispute is modeled at a $15 fee. Stripe has also described a separate $15 counter fee when a dispute is challenged without Chargeback Protection. That counter fee is named in the calculation notes and is not added on top of the $15 x disputes line.</li>
    <li><strong>Shopify Payments:</strong> modeled at $15 per dispute. Shopify refunds that fee in the US when you win. In several other regions the fee is not returned. This calculator keeps the fee in the loss so the total is not optimistic.</li>
    <li><strong>Paddle:</strong> public notes put the dispute fee around $15 to $20. The Paddle option uses $20.</li>
    <li><strong>High-volume or high-risk:</strong> modeled at $25 per dispute, before any monitoring program penalty.</li>
    <li><strong>Chargeflow:</strong> $0 monthly and $0 setup in this model, then 25% of recovered dispute dollars only. The 50% recovery rate is a planning benchmark so the fee is easy to audit. Ask Chargeflow for the win rate on your category before you treat the savings as a forecast.</li>
    <li><strong>Percent of all sales:</strong> 0.40% of yearly GMV. That is the comparison for a protection product billed on every dollar, not only on disputes. Stripe Radar for Fraud Teams is a different product and is often billed per screened payment. We do not treat 0.40% as Radar's only price.</li>
    <li><strong>Shopify Protect:</strong> covers eligible Shop Pay orders in the US. It does not cover a standard card gateway or PayPal dispute.</li>
  </ul>
  <p>Sources: <a href="https://docs.stripe.com/disputes" target="_blank" rel="noopener">Stripe disputes</a>, <a href="https://stripe.com/radar" target="_blank" rel="noopener">Stripe Radar</a>, <a href="https://help.shopify.com/en/manual/payments/chargebacks" target="_blank" rel="noopener">Shopify chargebacks</a>, <a href="https://www.chargeflow.io/" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="chargeflow" data-cta-location="sources">Chargeflow</a>.</p>
</section>

<script>
function calcChargeback(input) {{
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
  const cfWin = 0.50;
  const successRate = 0.25;
  const radarRate = 0.004;
  const manualLost = disputed * (1 - manualWin);
  const manualLoss = manualLost + fees;
  const recovered = disputed * cfWin;
  const successFee = recovered * successRate;
  const netRecovered = recovered - successFee;
  const cfLost = disputed - recovered;
  const cfLoss = cfLost + successFee + fees;
  const savings = manualLoss - cfLoss;
  const radar = gmv * radarRate;
  return {{
    annualOrders: annualOrders,
    gmv: gmv,
    disputes: disputes,
    disputesMo: disputes / 12,
    disputed: disputed,
    fees: fees,
    manualWin: manualWin,
    manualLost: manualLost,
    manualLoss: manualLoss,
    cfWin: cfWin,
    recovered: recovered,
    successFee: successFee,
    netRecovered: netRecovered,
    cfLost: cfLost,
    cfLoss: cfLoss,
    savings: savings,
    radar: radar,
    radarRate: radarRate,
    successRate: successRate,
    fee: fee,
    aov: aov,
    orders: orders,
    rate: rate
  }};
}}

function renderChargeback() {{
  const fees = {{ stripe: 15, shopify: 15, paddle: 20, highrisk: 25 }};
  const names = {{
    stripe: 'Stripe',
    shopify: 'Shopify Payments',
    paddle: 'Paddle',
    highrisk: 'High-volume / high-risk'
  }};
  const processor = document.getElementById('cb-processor').value;
  const orders = parseInt(document.getElementById('cb-orders').value, 10);
  const aov = parseInt(document.getElementById('cb-aov').value, 10);
  const ratePct = parseFloat(document.getElementById('cb-rate').value);
  const rate = ratePct / 100;
  const fee = fees[processor];
  const c = calcChargeback({{ orders: orders, aov: aov, rate: rate, fee: fee }});
  const money = n => '$' + Math.round(n).toLocaleString('en-US');
  document.getElementById('cb-orders-val').textContent = orders.toLocaleString('en-US');
  document.getElementById('cb-aov-val').textContent = money(aov);
  document.getElementById('cb-rate-val').textContent = ratePct.toFixed(2) + '%';
  const monitor = document.getElementById('cb-monitor');
  if (ratePct >= 1) {{
    monitor.textContent = 'At or above both the Visa 0.75% and Mastercard 1.00% monitoring marks.';
  }} else if (ratePct >= 0.75) {{
    monitor.textContent = 'At or above the Visa 0.75% monitoring mark. Still under the Mastercard 1.00% mark.';
  }} else {{
    monitor.textContent = 'Below the usual Visa 0.75% and Mastercard 1.00% monitoring marks.';
  }}
  const lostShare = c.manualLoss > 0 ? (c.manualLost / c.manualLoss) * 100 : 50;
  const feeShare = 100 - lostShare;
  document.getElementById('cb-row-lost').style.flex = lostShare + ' 1 0px';
  document.getElementById('cb-row-fees').style.flex = feeShare + ' 1 0px';
  document.getElementById('cb-amt-lost').textContent = money(c.manualLost);
  document.getElementById('cb-amt-fees').textContent = money(c.fees);
  document.getElementById('cb-fee-note').textContent = c.disputes.toLocaleString('en-US') + ' disputes x ' + money(fee);
  document.getElementById('cb-big').textContent = money(c.manualLoss);
  document.getElementById('cb-quote').textContent = 'Based on ' + orders.toLocaleString('en-US') + ' orders a month, a ' + money(aov) + ' average order, and a ' + ratePct.toFixed(2) + '% dispute rate on ' + names[processor] + '.';
  document.getElementById('cb-sub').textContent = Math.round(c.disputesMo).toLocaleString('en-US') + ' disputes a month, ' + c.disputes.toLocaleString('en-US') + ' a year. ' + money(c.disputed) + ' of sales in dispute. ' + money(c.fees) + ' of dispute fees. Yearly sales ' + money(c.gmv) + '.';
  const saveLabel = 'Save ' + money(c.savings) + '/yr with Chargeflow';
  document.getElementById('cb-best').innerHTML = '<strong>Best option:</strong> <a href="{CF}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="chargeflow" data-cta-location="workbench-best-option">' + saveLabel + ' &rarr;</a>';
  document.getElementById('cb-primary').textContent = saveLabel + ' →';
  const counter = processor === 'stripe' ? '<p>Stripe may also charge a $15 counter fee on disputes you fight without Chargeback Protection. That extra ' + money(c.disputes * 15) + ' is not inside the ' + money(c.fees) + ' fee line.</p>' : '';
  document.getElementById('cb-math').innerHTML =
    '<div class="calc-math-list">' +
    '<div class="calc-math-row"><span class="calc-math-label"><strong>Yearly orders</strong><span class="calc-math-formula">' + orders.toLocaleString('en-US') + ' x 12</span></span><span class="calc-math-val">' + c.annualOrders.toLocaleString('en-US') + '</span></div>' +
    '<div class="calc-math-row"><span class="calc-math-label"><strong>Yearly sales</strong><span class="calc-math-formula">' + c.annualOrders.toLocaleString('en-US') + ' x ' + money(aov) + '</span></span><span class="calc-math-val">' + money(c.gmv) + '</span></div>' +
    '<div class="calc-math-row"><span class="calc-math-label"><strong>Disputes</strong><span class="calc-math-formula">' + c.annualOrders.toLocaleString('en-US') + ' x ' + ratePct.toFixed(2) + '%</span></span><span class="calc-math-val">' + c.disputes.toLocaleString('en-US') + '</span></div>' +
    '<div class="calc-math-row"><span class="calc-math-label"><strong>Disputed sales</strong><span class="calc-math-formula">' + c.disputes.toLocaleString('en-US') + ' x ' + money(aov) + '</span></span><span class="calc-math-val">' + money(c.disputed) + '</span></div>' +
    '<div class="calc-math-row"><span class="calc-math-label"><strong>Dispute fees</strong><span class="calc-math-formula">' + c.disputes.toLocaleString('en-US') + ' x ' + money(fee) + '</span></span><span class="calc-math-val">' + money(c.fees) + '</span></div>' +
    '<div class="calc-math-row"><span class="calc-math-label"><strong>Manual lost sales</strong><span class="calc-math-formula">80% of ' + money(c.disputed) + ' at a 20% win rate</span></span><span class="calc-math-val">' + money(c.manualLost) + '</span></div>' +
    '<div class="calc-math-total"><span>Manual net loss</span><span>' + money(c.manualLoss) + ' / yr</span></div>' +
    '<div class="calc-math-row"><span class="calc-math-label"><strong>Illustrated recovery</strong><span class="calc-math-formula">50% of ' + money(c.disputed) + '</span></span><span class="calc-math-val">' + money(c.recovered) + '</span></div>' +
    '<div class="calc-math-row"><span class="calc-math-label"><strong>Chargeflow success fee</strong><span class="calc-math-formula">25% of ' + money(c.recovered) + ', $0 monthly</span></span><span class="calc-math-val">' + money(c.successFee) + '</span></div>' +
    '<div class="calc-math-row"><span class="calc-math-label"><strong>Net kept after the success fee</strong><span class="calc-math-formula">' + money(c.recovered) + ' minus ' + money(c.successFee) + '</span></span><span class="calc-math-val">' + money(c.netRecovered) + '</span></div>' +
    '<div class="calc-math-row"><span class="calc-math-label"><strong>Chargeflow all-in cost</strong><span class="calc-math-formula">unsaved sales + success fee + dispute fees</span></span><span class="calc-math-val">' + money(c.cfLoss) + '</span></div>' +
    '<div class="calc-math-total"><span>Savings vs manual</span><span>' + money(c.savings) + ' / yr</span></div>' +
    '<div class="calc-math-row"><span class="calc-math-label"><strong>0.40% of all sales</strong><span class="calc-math-formula">0.40% x ' + money(c.gmv) + '</span></span><span class="calc-math-val">' + money(c.radar) + '</span></div>' +
    '</div>' + counterNote(processor, c, money);
  const cards = document.getElementById('cb-summary');
  cards.innerHTML =
    '<div class="summary-card result-card card-lowest">' +
      '<div class="summary-label">Best net recovery</div>' +
      '<div class="summary-metric">' + money(c.netRecovered) + ' kept</div>' +
      '<div class="summary-scenario">Chargeflow. $0 a month. 25% only on recovered dispute dollars. This card uses a 50% recovery benchmark.</div>' +
      '<div class="summary-breakdown">Recovered ' + money(c.recovered) + ' minus a ' + money(c.successFee) + ' success fee.</div>' +
      '<details class="calc-disclosure"><summary class="calc-disclosure-toggle">See calculation</summary><div class="calc-disclosure-body">Net kept = 50% of disputed sales, then minus 25%. Savings versus manual fighting is ' + money(c.savings) + ' a year on this scenario.</div></details>' +
      '<div class="summary-actions"><a class="btn-cta" href="{CF}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="chargeflow" data-cta-location="summary-card">' + saveLabel + ' &rarr;</a></div>' +
    '</div>' +
    '<div class="summary-card result-card">' +
      '<div class="summary-label">Manual in-house fighting</div>' +
      '<div class="summary-metric">' + money(c.manualLoss) + ' / yr</div>' +
      '<div class="summary-scenario">About a 20% win rate when order, 3-D Secure, and shipping evidence is not assembled automatically. Staff time is extra and not priced here.</div>' +
      '<div class="summary-breakdown">' + money(c.manualLost) + ' lost sales + ' + money(c.fees) + ' dispute fees.</div>' +
      '<p class="summary-caveat"><strong>Hidden Cost Highlight:</strong> 80% of the disputed order value stays lost, and the dispute fees stay in the total.</p>' +
    '</div>' +
    '<div class="summary-card result-card card-hidden">' +
      '<div class="summary-label">0.40% of every sale</div>' +
      '<div class="summary-metric">' + money(c.radar) + ' / yr</div>' +
      '<div class="summary-scenario">A protection fee billed on all sales, including orders nobody disputes. Stripe Radar for Fraud Teams is often a per-payment add-on. This row is the percent-of-volume comparison.</div>' +
      '<div class="summary-breakdown">0.40% x ' + money(c.gmv) + '.</div>' +
      '<details class="calc-disclosure"><summary class="calc-disclosure-toggle">See calculation</summary><div class="calc-disclosure-body">The success fee on the illustrated recovery is ' + money(c.successFee) + '. The 0.40% fee is ' + money(c.radar) + '. The percent-of-sales fee is ' + money(c.radar - c.successFee) + ' higher than the success fee on this scenario.</div></details>' +
    '</div>';
  const rows = [
    ['Chargeflow', '$0 a month, then 25% of recovered dispute dollars', money(c.successFee) + ' success fee on this scenario', '2-click Stripe and Shopify connection. Recovery rate here is a 50% benchmark, not a promise.', '{CF}', 'chargeflow', 'View Chargeflow'],
    ['Percent of all sales', '0.40% of yearly sales, disputes or not', money(c.radar) + ' a year', 'Useful comparison with a success fee. Not a claim that Radar for Fraud Teams only has this price.', 'https://stripe.com/radar', 'stripe-payments', 'View Stripe Radar'],
    ['Shopify Protect', '$0 on eligible Shop Pay orders in the US', 'No dollar fee in this model', 'Does not cover a standard card gateway or PayPal dispute.', 'https://help.shopify.com/en/manual/payments/shopify-protect', 'shopify', 'View Shopify Protect'],
    ['Manual dispute management', 'Staff time plus about a 20% win rate', money(c.manualLoss) + ' net loss', 'Lost sales and dispute fees. Labor is not included.', 'https://docs.stripe.com/disputes', 'stripe-payments', 'Read dispute docs']
  ];
  document.getElementById('cb-tbody').innerHTML = rows.map(function(r) {{
    return '<tr><td data-label="Option"><strong>' + r[0] + '</strong></td><td data-label="How you pay">' + r[1] + '</td><td data-label="What this scenario costs">' + r[2] + '</td><td data-label="Coverage note">' + r[3] + ' <a href="' + r[4] + '" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="' + r[5] + '" data-cta-location="table-row">' + r[6] + ' &rarr;</a></td></tr>';
  }}).join('');
  if (typeof window.trackSaaSBillEvent === 'function') {{
    window.trackSaaSBillEvent('result_rendered', {{ page: 'chargeback-fee-and-recovery-calculator', orders: orders, aov: aov, rate: ratePct, processor: processor }});
  }}
}}

function counterNote(processor, c, money) {{
  if (processor !== 'stripe') return '';
  return '<p>Stripe may also charge a $15 counter fee on disputes you fight without Chargeback Protection. That extra ' + money(c.disputes * 15) + ' is not inside the ' + money(c.fees) + ' fee line.</p>';
}}

['cb-processor', 'cb-orders', 'cb-aov', 'cb-rate'].forEach(function(id) {{
  const el = document.getElementById(id);
  el.addEventListener('input', renderChargeback);
  el.addEventListener('change', renderChargeback);
}});
renderChargeback();
</script>
"""


def build():
    faqs = [
        (
            "How much is a Stripe or Shopify dispute fee?",
            "This calculator uses $15 per dispute for Stripe and for Shopify Payments. Shopify refunds that fee in the US when you win. In several other regions it does not. Paddle is modeled at $20, inside a $15 to $20 range. A high-risk processor is modeled at $25.",
        ),
        (
            "What does Chargeflow charge?",
            "In this model Chargeflow has a $0 monthly fee and a $0 setup fee, then 25% of the dispute dollars it recovers. The 50% recovery figure is a planning benchmark so you can audit the fee. It is not a guaranteed win rate.",
        ),
        (
            "Why compare a 0.40% fee on all sales?",
            "0.40% of yearly sales is $11,520 on $2.88 million. A 25% fee on only the dollars actually recovered is much smaller when disputes are a fraction of orders. Stripe Radar for Fraud Teams is often priced per screened payment, so do not read 0.40% as its only rate.",
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
