"""Shopify Payments reserve and dispute-threshold calculator.

Sources checked 2026-10-29:
- Shopify Payments US online standard rates: Basic 2.9% + 30c, Grow 2.7% + 30c,
  Advanced 2.5% + 30c, Plus 2.25% + 30c (shopify.com/pricing).
- US chargeback fee $15, returned if you win (Shopify chargeback process).
- NDRP: 1.5% NDRP-inclusive rate over 90 days can auto-enroll; 10% reserve;
  disputes are reimbursed in full, $15 fee, no appeal. A 90-day rate still
  above 1% after the reserve expires can bring further reserves or payout holds.
  Reserve length is emailed, not a published 90-day hold.
- Visa VAMP excessive merchant, Shopify help table: 1.5% and 1,500 count
  outside CEMEA; CEMEA 2.2%, 150 count and $75,000. Non-compliant column: 0.5% and count of 5.
- Mastercard ECM 100-299 and 1.5%-2.99%; HECM 300+ and 3% (Shopify help).
The 0.75% US Plus multi-currency payout fee is a different charge.
"""
from layout import render_page, wrap_calculator_shell

TITLE = "Shopify Reserve & Dispute Threshold – saasbill.io"
DESCRIPTION = (
    "US Shopify Payments card rate, the $15 dispute fee, a 10% NDRP reserve, "
    "and Visa VAMP and Mastercard ECM thresholds. No invented 0.75% dispute line."
)
H1 = "Shopify Payments Reserve &amp; Dispute Threshold Calculator (2026)"
LEAD = (
    "Adjust monthly orders, average order value, and dispute rate to see the published US card rate beside dispute fees and any reserve Shopify actually describes. "
    "Shopify does not publish a universal 0.75% dispute threshold or a 90-day hold length. The 0.75% figure on the US Plus plan is a multi-currency payout fee."
)

BODY = r"""
<section class="hero">
  <h1>Shopify Payments Reserve &amp; Dispute Threshold Calculator (2026)</h1>
  <p class="lead">Adjust monthly orders, average order value, and dispute rate to see the published US card rate beside dispute fees and any reserve Shopify actually describes. Shopify does not publish a universal 0.75% dispute threshold or a 90-day hold length. The 0.75% figure on the US Plus plan is a multi-currency payout fee.</p>
</section>

<div class="unified-inspector-tray">
<section class="calc-box editorial-workbench" aria-labelledby="sh-heading">
  <h2 id="sh-heading" class="sr-only-control">Shopify Payments reserve and dispute threshold calculator</h2>
  <div class="workbench-grid">
    <div class="wb-col-controls">
      <div class="wb-col-title">Estimate Your True Cost</div>
      <div class="wb-controls-stack">
        <div class="wb-control-item">
          <label class="wb-control-label" for="sh-orders">Monthly orders <span class="val-pill" id="sh-orders-val">1,000</span></label>
          <div class="wb-slider-row">
            <input type="range" id="sh-orders" min="0" max="20000" step="50" value="1000" aria-label="Monthly orders" data-track="calculator-control" data-control="orders" />
          </div>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="sh-aov">Average order value <span class="val-pill" id="sh-aov-val">$50</span></label>
          <div class="wb-slider-row">
            <input type="range" id="sh-aov" min="10" max="500" step="5" value="50" aria-label="Average order value" data-track="calculator-control" data-control="aov" />
          </div>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="sh-rate">Dispute rate <span class="val-pill" id="sh-rate-val">0.65%</span></label>
          <div class="wb-slider-row">
            <input type="range" id="sh-rate" min="0" max="3" step="0.05" value="0.65" aria-label="Dispute rate percent" data-track="calculator-control" data-control="dispute-rate" />
          </div>
        </div>
        <div class="wb-quiet-options">
          <div class="wb-quiet-field">
            <label for="sh-plan">US online standard cards:</label>
            <select id="sh-plan" data-track="calculator-control" data-control="shopify-plan">
              <option value="basic" selected>Basic, 2.9% + 30¢</option>
              <option value="grow">Grow, 2.7% + 30¢</option>
              <option value="advanced">Advanced, 2.5% + 30¢</option>
              <option value="plus">Plus, 2.25% + 30¢</option>
            </select>
          </div>
        </div>
        <p id="sh-gmv" class="wb-budget-subnote">Monthly GMV $50,000.</p>
      </div>
    </div>

    <div class="wb-col-chart">
      <div class="wb-col-title">Your Estimated True Cost</div>
      <div id="sh-vbar" class="wb-vbar-container" aria-live="polite">
        <div class="wb-vbar-row" id="sh-row-base">
          <div class="wb-vbar-block block-base"><span class="wb-block-amount" id="sh-amt-base">$1,450</span></div>
          <div class="wb-callout-item"><div class="wb-leader-line"></div><div class="wb-callout-text"><strong>Sticker Price: Base rate</strong><span id="sh-sub-base">2.9% card rate</span></div></div>
        </div>
        <div class="wb-vbar-row" id="sh-row-tx">
          <div class="wb-vbar-block block-seats"><span class="wb-block-amount" id="sh-amt-tx">$300</span></div>
          <div class="wb-callout-item"><div class="wb-leader-line"></div><div class="wb-callout-text"><strong>Sticker Price: Per-order fees</strong><span id="sh-sub-tx">30¢ x orders</span></div></div>
        </div>
        <div class="wb-vbar-row" id="sh-row-hidden">
          <div class="wb-vbar-block block-hidden"><span class="wb-block-amount" id="sh-amt-hidden">$0</span></div>
          <div class="wb-callout-item"><div class="wb-leader-line"></div><div class="wb-callout-text"><strong>Hidden Cost Gap</strong><span id="sh-sub-hidden">Dispute fees and unrecovered orders</span></div></div>
        </div>
      </div>
    </div>

    <div class="wb-result-col" id="sh-result">
      <div class="wb-selected-product" id="sh-product">Shopify Payments, Basic</div>
      <div class="wb-big-total"><span id="sh-big">$21,000</span> <span class="wb-per-year">/ year</span></div>
      <details class="math-drawer" id="sh-calc-details">
        <summary>Show calculation</summary>
        <div class="math-drawer-body" id="sh-math"></div>
      </details>
      <p class="wb-budget-quote" id="sh-quote">True Year-1 cost</p>
      <p class="wb-budget-subnote" id="sh-sub"></p>
      <div class="wb-best-option" id="sh-best"></div>
      <div class="cta-stack">
        <a id="sh-primary" class="btn-cta wb-primary-cta" href="../chargeback-fee-and-recovery-calculator/" data-track="internal-audit">Open the chargeback cost calculator &rarr;</a>
      </div>
    </div>
  </div>
</section>
</div>

<div id="sh-summary" class="summary-strip" aria-live="polite"></div>

<div class="table-wrap mobile-cards">
  <table>
    <thead>
      <tr>
        <th>Path</th>
        <th>What you pay</th>
        <th>Cash held</th>
        <th>Limitation</th>
      </tr>
    </thead>
    <tbody id="sh-tbody"></tbody>
  </table>
</div>

<section class="editorial-below-section">
  <h2>What Shopify, Visa, and Mastercard actually print</h2>
  <div class="methodology-grid fine-print-grid">
    <div class="methodology-item">
      <strong>1. The card rate is the sticker</strong>
      US online standard cards are 2.9% + 30¢ on Basic, 2.7% + 30¢ on Grow, 2.5% + 30¢ on Advanced, and 2.25% + 30¢ on Plus. Premium cards and international cards cost more. That extra is not in this sticker.
    </div>
    <div class="methodology-item">
      <strong>2. The $15 fee comes back only if you win</strong>
      Shopify's US chargeback fee is $15, and the help center says the fee is returned if you win. This model uses a 20% manual win rate as a planning benchmark, not a Shopify promise. Staff time is not priced here.
    </div>
    <div class="methodology-item">
      <strong>3. The 90 days are a lookback, not a hold length</strong>
      An NDRP-inclusive chargeback rate of 1.5% or higher over the last 90 days can auto-enroll the store. Enrollment applies a 10% reserve and resolves disputes automatically: the order is reimbursed, a fee is charged, and you cannot submit evidence. If the 90-day rate is still above 1% after that reserve expires, Shopify says further reserves or payout holds may follow. The reserve's length is in the email, not in a published 90-day rule.
    </div>
  </div>
  <p>Network lines, cited from Shopify's monitoring guide and Visa's VAMP fact sheet: Visa's excessive merchant ratio is 1.5% with at least 1,500 combined fraud reports and disputes outside CEMEA (2.2%, 150 events, and $75,000 in CEMEA). Shopify's table also lists a non-compliant column at 0.5% and a count of 5. Mastercard ECM is 100 to 299 chargebacks and a 1.5% to 2.99% ratio. HECM is 300 or more and 3% or higher. One test without the other does not place you in ECM. A count of disputes on all cards is not the same as Visa-only or Mastercard-only volume, so this page flags the ratio and tells you the count test is separate.</p>
  <p>Sources: <a href="https://www.shopify.com/pricing" target="_blank" rel="noopener">Shopify pricing</a>, <a href="https://help.shopify.com/en/manual/payments/chargebacks/chargeback-process" target="_blank" rel="noopener">Shopify chargeback fees</a>, <a href="https://help.shopify.com/en/manual/payments/chargebacks/network-dispute-resolution-programs" target="_blank" rel="noopener">Shopify NDRP</a>, <a href="https://help.shopify.com/en/manual/payments/shopify-payments/payouts/reserves" target="_blank" rel="noopener">Shopify reserves</a>, <a href="https://help.shopify.com/en/manual/payments/chargebacks/monitoring-programs" target="_blank" rel="noopener">Shopify network monitoring</a>, <a href="https://corporate.visa.com/content/dam/VCOM/corporate/visa-perspectives/security-and-trust/documents/visa-acquirer-monitoring-program-fact-sheet-2025.pdf" target="_blank" rel="noopener">Visa VAMP fact sheet</a>.</p>
</section>

<script>
const SH_PLANS = {
  basic: { pct: 0.029, fixed: 0.30, name: 'Basic' },
  grow: { pct: 0.027, fixed: 0.30, name: 'Grow' },
  advanced: { pct: 0.025, fixed: 0.30, name: 'Advanced' },
  plus: { pct: 0.0225, fixed: 0.30, name: 'Plus' }
};

function calcShopifyReserve(input) {
  const orders = Math.max(0, Math.round(Number(input.orders) || 0));
  const aov = Math.max(0, Number(input.aov) || 0);
  const rate = Math.max(0, Number(input.rate) || 0);
  const plan = SH_PLANS[input.plan] || SH_PLANS.basic;
  const gmvMo = Math.round(orders * aov);
  const pctMo = Math.round(gmvMo * plan.pct);
  const fixedMo = Math.round(orders * plan.fixed);
  const stickerMo = pctMo + fixedMo;
  const stickerYr = stickerMo * 12;
  const disputesYr = Math.round(orders * 12 * rate);
  const disputesMo = Math.round(orders * rate);
  const disputedYr = disputesYr * aov;
  const ndrp = rate >= 0.015;
  const aboveOne = rate >= 0.01;
  const win = 0.20;
  let feesYr;
  let lostYr;
  let mode;
  if (ndrp) {
    feesYr = disputesYr * 15;
    lostYr = disputedYr;
    mode = 'ndrp';
  } else {
    const lostCount = Math.round(disputesYr * (1 - win));
    feesYr = lostCount * 15;
    lostYr = Math.round(disputedYr * (1 - win));
    mode = 'manual';
  }
  const hiddenYr = feesYr + lostYr;
  const reserveMo = ndrp ? Math.round(gmvMo * 0.10) : 0;
  const recovered = Math.round(disputedYr * 0.65);
  const successFee = Math.round(recovered * 0.25);
  const net = recovered - successFee;
  return {
    orders: orders,
    aov: aov,
    rate: rate,
    plan: plan.name,
    pct: plan.pct,
    fixed: plan.fixed,
    gmvMo: gmvMo,
    pctMo: pctMo,
    fixedMo: fixedMo,
    stickerMo: stickerMo,
    stickerYr: stickerYr,
    disputesYr: disputesYr,
    disputesMo: disputesMo,
    disputedYr: disputedYr,
    feesYr: feesYr,
    lostYr: lostYr,
    hiddenYr: hiddenYr,
    trueYr: stickerYr + hiddenYr,
    reserveMo: reserveMo,
    ndrp: ndrp,
    aboveOne: aboveOne,
    vampRatio: rate >= 0.015,
    vampCount: disputesMo >= 1500,
    shopifyWatch: rate >= 0.005 && disputesMo >= 5,
    ecmCount: disputesMo >= 100 && disputesMo <= 299,
    ecmRate: rate >= 0.015 && rate < 0.03,
    hecm: disputesMo >= 300 && rate >= 0.03,
    recovered: recovered,
    successFee: successFee,
    net: net,
    mode: mode
  };
}

function shMoney(n) {
  const rounded = Math.round(n);
  const sign = rounded < 0 ? '-' : '';
  return sign + '$' + Math.abs(rounded).toLocaleString('en-US');
}

function renderShopifyReserve() {
  const orders = parseInt(document.getElementById('sh-orders').value, 10);
  const aov = parseInt(document.getElementById('sh-aov').value, 10);
  const ratePct = parseFloat(document.getElementById('sh-rate').value);
  const planId = document.getElementById('sh-plan').value;
  const c = calcShopifyReserve({ orders: orders, aov: aov, rate: ratePct / 100, plan: planId });
  document.getElementById('sh-orders-val').textContent = orders.toLocaleString('en-US');
  document.getElementById('sh-aov-val').textContent = shMoney(aov);
  document.getElementById('sh-rate-val').textContent = ratePct.toFixed(2) + '%';
  document.getElementById('sh-gmv').textContent = 'Monthly GMV ' + shMoney(c.gmvMo) + ' (' + orders.toLocaleString('en-US') + ' orders x ' + shMoney(aov) + ').';
  const parts = Math.max(c.pctMo + c.fixedMo + Math.round(c.hiddenYr / 12), 1);
  document.getElementById('sh-row-base').style.flex = (c.pctMo / parts * 100) + ' 1 0px';
  document.getElementById('sh-row-tx').style.flex = (c.fixedMo / parts * 100) + ' 1 0px';
  document.getElementById('sh-row-hidden').style.flex = (Math.round(c.hiddenYr / 12) / parts * 100) + ' 1 0px';
  document.getElementById('sh-amt-base').textContent = shMoney(c.pctMo);
  document.getElementById('sh-amt-tx').textContent = shMoney(c.fixedMo);
  document.getElementById('sh-amt-hidden').textContent = shMoney(Math.round(c.hiddenYr / 12));
  document.getElementById('sh-sub-base').textContent = (c.pct * 100).toFixed(2).replace(/0$/, '').replace(/\.$/, '') + '% of ' + shMoney(c.gmvMo) + '/mo';
  document.getElementById('sh-sub-tx').textContent = '30¢ x ' + orders.toLocaleString('en-US') + ' orders';
  document.getElementById('sh-sub-hidden').textContent = c.ndrp
    ? 'NDRP: full order reimbursed + $15 fee, no appeal'
    : '80% unrecovered at a 20% manual win rate, plus $15 on lost disputes';
  document.getElementById('sh-product').textContent = 'Shopify Payments, ' + c.plan + ', US standard cards';
  document.getElementById('sh-big').textContent = shMoney(c.trueYr);
  document.getElementById('sh-sub').textContent = (typeof window.saasbillResultLine === 'function')
    ? window.saasbillResultLine(c.hiddenYr, c.stickerYr)
    : (c.hiddenYr > 0
      ? '+' + shMoney(c.hiddenYr) + ' (+' + (c.stickerYr > 0 ? Math.round((c.hiddenYr / c.stickerYr) * 100) : 0) + '%) above advertised price.'
      : 'Matches advertised price ($0 hidden fees).');
  const reserveLine = c.reserveMo > 0
    ? 'Cash held under the published 10% NDRP reserve: ' + shMoney(c.reserveMo) + '/mo. The length is in the Shopify email, not a published 90-day rule.'
    : 'No published reserve percent applies below the 1.5% NDRP line. A reserve can still be emailed for other risk reasons.';
  let status = 'Under the Shopify 1% follow-up line.';
  if (c.ndrp) status = 'At or above the 1.5% NDRP enrollment line.';
  else if (c.aboveOne) status = 'Above the 1% line that can bring further reserves after an NDRP reserve expires. Under the 1.5% auto-enroll line.';
  document.getElementById('sh-best').innerHTML = '<strong>Threshold:</strong> ' + status + ' ' + reserveLine;
  const manualNote = '20% win rate is a planning benchmark. Shopify returns the $15 fee only when you win, and a win still counts in the chargeback rate.';
  const ndrpNote = 'At 1.5% or higher over 90 days, Shopify can auto-enroll an NDRP: the order is reimbursed, the fee is charged, and you cannot submit evidence.';
  document.getElementById('sh-math').innerHTML = 'Monthly GMV = ' + orders.toLocaleString('en-US') + ' x ' + shMoney(aov) + ' = ' + shMoney(c.gmvMo) + '. Sticker = ' + (c.pct * 100).toFixed(2) + '% x ' + shMoney(c.gmvMo) + ' + 30¢ x ' + orders.toLocaleString('en-US') + ' = ' + shMoney(c.stickerMo) + '/mo (' + shMoney(c.stickerYr) + '/yr). Disputes/yr = round(' + orders.toLocaleString('en-US') + ' x 12 x ' + ratePct.toFixed(2) + '%) = ' + c.disputesYr.toLocaleString('en-US') + '. Disputed sales = ' + shMoney(c.disputedYr) + '. ' + (c.ndrp ? ndrpNote : manualNote) + ' Dispute fees ' + shMoney(c.feesYr) + '. Unrecovered or reimbursed orders ' + shMoney(c.lostYr) + '. Hidden Cost Gap ' + shMoney(c.hiddenYr) + '. True Year-1 cost ' + shMoney(c.stickerYr) + ' + ' + shMoney(c.hiddenYr) + ' = ' + shMoney(c.trueYr) + '. Reserve cash ' + shMoney(c.reserveMo) + '/mo is held working capital, not added to that fee total. Visa excessive ratio is 1.5% and also needs 1,500 combined fraud reports and disputes in a month outside CEMEA. Dispute count this month is ' + c.disputesMo.toLocaleString('en-US') + (c.vampCount ? ', which meets that count.' : ', which does not meet that count.') + ' A 65% recovery benchmark on the disputed sales would keep ' + shMoney(c.net) + ' after a 25% fee, and only if the disputes can be contested. NDRP disputes cannot.';
  const cfLimit = c.ndrp
    ? 'Chargeflow cannot submit evidence on an NDRP dispute. Shopify says those outcomes are final.'
    : 'A 65% win rate is a planning benchmark. Shopify still counts a won dispute in the chargeback rate.';
  document.getElementById('sh-summary').innerHTML = ''
    + '<div class="summary-card result-card"><div class="summary-label">Sticker Price</div><div class="summary-metric">' + shMoney(c.stickerYr) + ' / yr</div><div class="summary-scenario">US online standard cards on ' + c.plan + '</div><div class="summary-breakdown">' + shMoney(c.pctMo) + '/mo percentage + ' + shMoney(c.fixedMo) + '/mo per-order fees.</div><p class="summary-caveat"><strong>Limitation:</strong> Premium and international cards are extra. This sticker is not the whole bill.</p></div>'
    + '<div class="summary-card result-card card-hidden"><div class="summary-label">Hidden Cost Gap</div><div class="summary-metric" style="color:var(--rose);">+' + shMoney(c.hiddenYr) + ' / yr</div><div class="summary-scenario">' + status + '</div><div class="summary-breakdown">Fees ' + shMoney(c.feesYr) + ' + unrecovered or reimbursed orders ' + shMoney(c.lostYr) + '.</div><p class="summary-caveat"><strong>Cash held:</strong> ' + shMoney(c.reserveMo) + '/mo. ' + reserveLine + '</p><details class="math-drawer"><summary>Show calculation</summary><div class="math-drawer-body">' + document.getElementById('sh-math').textContent + '</div></details></div>'
    + '<div class="summary-card result-card"><div class="summary-label">Add-on: contested recovery</div><div class="summary-metric">+' + shMoney(c.net) + ' / yr net</div><div class="summary-scenario">65% planning benchmark, 25% fee, $0/mo</div><div class="summary-breakdown">Gross recovered ' + shMoney(c.recovered) + ' minus ' + shMoney(c.successFee) + '.</div><p class="summary-caveat"><strong>Limitation:</strong> ' + cfLimit + '</p><div class="summary-actions"><a class="btn-secondary" href="https://www.chargeflow.io/" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="chargeflow" data-cta-location="summary-card">Review Chargeflow</a></div></div>';
  document.getElementById('sh-tbody').innerHTML = ''
    + '<tr><td data-label="Path"><strong>Shopify Payments, manual contest</strong></td><td data-label="What you pay">' + shMoney(c.stickerYr) + '/yr sticker + dispute drain if you can fight</td><td data-label="Cash held">' + (c.ndrp ? 'Not this path' : shMoney(0) + ' published reserve') + '</td><td data-label="Limitation">Win rate is not guaranteed. Won disputes still count. <a href="https://help.shopify.com/en/manual/payments/chargebacks/chargeback-process" target="_blank" rel="noopener">Verified source</a></td></tr>'
    + '<tr><td data-label="Path"><strong>Shopify NDRP</strong></td><td data-label="What you pay">Full order reimbursed + $15 US fee</td><td data-label="Cash held">' + shMoney(c.reserveMo) + '/mo at the published 10%</td><td data-label="Limitation">' + (c.ndrp ? 'This rate is on the 1.5% enrollment line.' : 'Not on the 1.5% enrollment line at this rate.') + ' <a href="https://help.shopify.com/en/manual/payments/chargebacks/network-dispute-resolution-programs" target="_blank" rel="noopener">Verified source</a></td></tr>'
    + '<tr><td data-label="Path"><strong>Chargeflow</strong></td><td data-label="What you pay">25% of recovered dollars, $0/mo in this model</td><td data-label="Cash held">Does not release a Shopify reserve</td><td data-label="Limitation">' + cfLimit + '</td></tr>'
    + '<tr><td data-label="Path"><strong>Another processor</strong></td><td data-label="What you pay">Its own rate. See the Stripe, Paddle, and Whop calculators.</td><td data-label="Cash held">Does not erase Shopify Payments history</td><td data-label="Limitation">Moving new volume elsewhere does not rewrite the 90-day Shopify rate. <a href="../exit/stripe-shopify-paddle-frozen-funds-alternatives/" data-track="internal-audit">Stripe, Shopify and Paddle reserves</a></td></tr>';
  if (typeof window.trackSaaSBillEvent === 'function') {
    window.trackSaaSBillEvent('result_rendered', { page: 'shopify-reserve', orders: orders, aov: aov, rate: ratePct, plan: planId });
  }
}
['sh-orders', 'sh-aov', 'sh-rate', 'sh-plan'].forEach(function (id) {
  const el = document.getElementById(id);
  el.addEventListener('input', renderShopifyReserve);
  el.addEventListener('change', renderShopifyReserve);
});
renderShopifyReserve();
</script>
"""

FAQS = [
    (
        "Does Shopify publish a 0.75% dispute threshold or a 90-day payout hold?",
        "No. Shopify's help center does not print a 0.75% dispute line. The 0.75% rate on the US Shopify Plus plan is the multi-currency payout fee, which is a different charge. The 90 days in the NDRP article are the window used to measure the chargeback rate. Reserve length is sent by email. Shopify does not publish a rule that every reserve lasts 90 days.",
    ),
    (
        "When does Shopify Payments apply a 10% reserve?",
        "If a store is enrolled in a network dispute resolution program because of a high chargeback rate, Shopify says a 10% reserve is applied to Shopify Payments payouts. Merchants with an NDRP-inclusive chargeback rate of 1.5% or higher over the last 90 days can be enrolled automatically. If the 90-day rate is still above 1% after that reserve expires, Shopify says further reserves or payout holds may follow. Other reserves can still be applied for risk reasons that are not a published percent.",
    ),
    (
        "What are the Visa VAMP and Mastercard ECM lines?",
        "Shopify's monitoring guide lists Visa VAMP excessive thresholds of 1.5% and 1,500 combined fraud reports and disputes outside Central Europe, the Middle East, and Africa, and 2.2% with 150 events and $75,000 there. The same table lists a non-compliant column at 0.5% and a count of 5. Visa's own fact sheet says the excessive merchant ratio in AP, Canada, EU, and the US drops to 150 basis points on 1 April 2026, and that this merchant test applies when the acquirer is not already Above Standard or Excessive. Mastercard ECM needs both 100 to 299 chargebacks and a 1.5% to 2.99% ratio. HECM needs 300 or more and 3% or higher. This calculator can see your all-card dispute rate. It cannot see Visa-only or Mastercard-only counts.",
    ),
]


def build():
    if len(TITLE) > 60:
        raise SystemExit("Title is %s chars: %s" % (len(TITLE), TITLE))
    render_page(
        "exit/shopify-payments-chargeback-threshold-and-reserve-appeal/index.html",
        TITLE,
        DESCRIPTION,
        "/exit/shopify-payments-chargeback-threshold-and-reserve-appeal/",
        wrap_calculator_shell(BODY),
        faqs=FAQS,
        published_date="2026-10-29",
    )


if __name__ == "__main__":
    build()
