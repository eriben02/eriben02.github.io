"""Dedicated HubSpot onboarding calculator at /hubspot-onboarding-fee-calculator/.

Seat and onboarding math matches pricing/hubspot-true-cost-and-onboarding-fees/
(Sales Pro $90 + $1,500, Sales Ent $150 + $3,500, Marketing Pro $800 + $3,000,
Marketing Ent $3,600 + $7,000). Marketing contact bands come from HubSpot's
Product and Services Catalog (Professional $250 per 5,000 above 2,000;
Enterprise $100 per 10,000 above 10,000).
"""
from layout import render_page

BODY = r"""
<section class="hero">
  <h1>HubSpot Onboarding Fee Calculator: Mandatory Setup &amp; Real Year-1 Cost ($1,500–$7,000)</h1>
  <p class="lead">Calculate your real Year-1 HubSpot cost including the mandatory $1,500 to $7,000 onboarding fee. Adjust your seats, marketing contacts, and tier below to compare your total against Close CRM and Pipedrive.</p>
</section>

<section class="calc-box editorial-bar-chart-card" id="crm-apples-to-apples-chart" aria-labelledby="chart-dynamic-headline">
  <div class="calc-grid ebc-controls-grid">
    <div class="control-group">
      <label for="hs-users">Sales team size (core seats): <span class="val-pill" id="hs-users-val">5</span> reps</label>
      <input type="range" id="hs-users" min="1" max="30" value="5" data-track="calculator-control" data-control="hs-users" />
    </div>
    <div class="control-group">
      <label for="hs-contacts">Marketing contacts</label>
      <select id="hs-contacts" data-track="calculator-control" data-control="hs-contacts">
        <option value="2000" selected>2,000 (included on Marketing Pro)</option>
        <option value="10000">10,000</option>
        <option value="20000">20,000</option>
        <option value="30000">30,000</option>
        <option value="50000">50,000</option>
      </select>
    </div>
    <div class="control-group">
      <label for="hs-tier">HubSpot hub &amp; edition</label>
      <select id="hs-tier" data-track="calculator-control" data-control="hs-tier">
        <option value="sales_pro" selected>Sales Hub Pro ($90/seat + $1,500 onboarding)</option>
        <option value="sales_ent">Sales Hub Ent ($150/seat + $3,500 onboarding)</option>
        <option value="mkt_pro">Marketing Pro ($800/mo + $3,000 onboarding)</option>
        <option value="mkt_ent">Marketing Ent ($3,600/mo + $7,000 onboarding)</option>
      </select>
    </div>
  </div>

  <h2 id="chart-dynamic-headline" class="ebc-title">At 5 seats, HubSpot Sales Pro ($6,900) costs 2.4x Close Startup ($2,820) in Year 1</h2>
  <p id="chart-dynamic-subtitle" class="ebc-subtitle">Year-1 total for 5 sales reps on annual billing, including mandatory onboarding. Marketing contact bands apply only on Marketing Hub.</p>

  <div class="ebc-rows" role="list" aria-live="polite">
    <div class="ebc-row" role="listitem">
      <div class="ebc-label-col">
        <div class="ebc-tool-name"><a href="https://www.pipedrive.com/en/pricing" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="pipedrive-crm" data-cta-location="benchmark-chart">Pipedrive Growth &nearr;</a></div>
        <div class="ebc-tool-meta">Sequences and automation included &middot; $0 onboarding</div>
      </div>
      <div class="ebc-bar-col"><div class="ebc-bar-track"><div id="bar-pipedrive" class="ebc-bar-fill ebc-fill-neutral" style="width: 33.9%;"></div></div></div>
      <div class="ebc-val-col"><span id="val-pipedrive" class="ebc-val-main">$2,340</span><span class="ebc-val-sub">$39/seat/mo</span></div>
    </div>
    <div class="ebc-row ebc-row-sage" role="listitem">
      <div class="ebc-label-col">
        <div class="ebc-tool-name"><a href="https://refer.close.com/3k5hp07b8soi-fetl0j" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="close" data-cta-location="benchmark-chart">Close CRM Startup &nearr;</a></div>
        <div class="ebc-tool-meta">Built-in calling and SMS &middot; $0 onboarding</div>
      </div>
      <div class="ebc-bar-col"><div class="ebc-bar-track"><div id="bar-close-startup" class="ebc-bar-fill ebc-fill-sage" style="width: 40.9%;"></div></div></div>
      <div class="ebc-val-col"><span id="val-close-startup" class="ebc-val-main ebc-val-sage">$2,820</span><span class="ebc-val-sub">$47/seat/mo</span></div>
    </div>
    <div class="ebc-row" role="listitem">
      <div class="ebc-label-col">
        <div class="ebc-tool-name"><a href="https://refer.close.com/3k5hp07b8soi-fetl0j" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="close" data-cta-location="benchmark-chart">Close CRM Growth &nearr;</a></div>
        <div class="ebc-tool-meta">Power Dialer and AI call summaries &middot; $0 onboarding</div>
      </div>
      <div class="ebc-bar-col"><div class="ebc-bar-track"><div id="bar-close-growth" class="ebc-bar-fill ebc-fill-slate" style="width: 86.1%;"></div></div></div>
      <div class="ebc-val-col"><span id="val-close-growth" class="ebc-val-main">$5,940</span><span class="ebc-val-sub">$99/seat/mo</span></div>
    </div>
    <div class="ebc-row ebc-row-terracotta" role="listitem">
      <div class="ebc-label-col">
        <div id="label-hs-name" class="ebc-tool-name">HubSpot Sales Hub Professional</div>
        <div id="meta-hs-breakdown" class="ebc-tool-meta">$5,400 seats + $1,500 onboarding</div>
      </div>
      <div class="ebc-bar-col">
        <div class="ebc-bar-track">
          <div id="bar-hs-total" class="ebc-bar-fill ebc-fill-terracotta" style="width: 100%;">
            <span id="bar-hs-seats" class="ebc-bar-seg-seats" style="width: 78.26%;"></span>
            <span id="bar-hs-onb" class="ebc-bar-seg-onb" style="width: 21.74%;"></span>
          </div>
        </div>
      </div>
      <div class="ebc-val-col">
        <span id="val-hs-total" class="ebc-val-main ebc-val-terracotta">$6,900</span>
        <span id="sub-hs-onb" class="ebc-val-sub">+$1,500 onboarding</span>
      </div>
    </div>
  </div>

  <details class="math-drawer" id="hs-calc-details">
    <summary>Show calculation</summary>
    <div class="math-drawer-body" id="hs-calc-body"></div>
  </details>

  <div id="hs-summary" class="ebc-action-strip">
    <a id="hs-close-cta" class="btn-affiliate" href="https://refer.close.com/3k5hp07b8soi-fetl0j" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="close" data-cta-location="benchmark-cta">Save $4,080/yr with Close CRM ($0 Onboarding) &rarr;</a>
    <a class="ebc-secondary-link" href="https://www.hubspot.com/pricing/sales" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="hubspot" data-cta-location="benchmark-cta">View official HubSpot Sales Hub pricing &nearr;</a>
  </div>
  <p id="chart-dynamic-footnote" class="ebc-footer-note"><strong>Hidden Cost Highlight:</strong> Based on 5 seats, annual billing, 2,000 marketing contacts. HubSpot Sales Pro adds a one-time $1,500 onboarding fee in Year 1. Source: <a href="https://legal.hubspot.com/hubspot-product-and-services-catalog/products" target="_blank" rel="noopener">HubSpot Product and Services Catalog</a>.</p>
</section>

<section class="hidden-gap-section" aria-labelledby="gap-heading">
  <details class="full-table-disclosure" id="full-table-details">
    <summary class="full-table-summary" id="full-table-summary">
      <div class="full-table-summary-text">
        <h2 id="gap-heading" class="full-table-heading">Compare all tools in this category</h2>
        <span class="full-table-summary-sub">HubSpot vs. Close CRM and Pipedrive, including onboarding and marketing contact bands</span>
      </div>
      <span class="full-table-toggle-pill" id="full-table-toggle-pill">Compare all tools &darr;</span>
    </summary>
    <div class="full-table-body">
      <p class="gap-subhead" id="gap-dynamic-subhead">Based on 5 seats, annual billing, 2,000 marketing contacts.</p>
      <div class="table-wrap editorial-gap-table mobile-cards">
        <table>
          <caption>2026 HubSpot vs. Close CRM vs. Pipedrive Year-1 cost (USD)</caption>
          <thead>
            <tr>
              <th>Platform</th>
              <th>Licenses / Year</th>
              <th>Onboarding</th>
              <th>Contact tier / Year</th>
              <th>Year-1 total</th>
            </tr>
          </thead>
          <tbody id="hs-compare-tbody"></tbody>
        </table>
      </div>
    </div>
  </details>
  <p class="calc-affiliate-disclosure">Independent calculations. Some vendor links are affiliate links. This never changes our rankings or calculations.</p>
</section>

<script>
function contactAddonMonthly(contacts, tier) {
  if (tier === 'sales_pro' || tier === 'sales_ent') {
    return { monthly: 0, included: 0, note: 'Sales Hub does not bill marketing-contact tiers.' };
  }
  const pro = tier === 'mkt_pro';
  const included = pro ? 2000 : 10000;
  const size = pro ? 5000 : 10000;
  const bands = pro
    ? [{ upto: 22000, rate: 250 }, { upto: 42000, rate: 225 }, { upto: 62000, rate: 200 }, { upto: 82000, rate: 175 }, { upto: Infinity, rate: 150 }]
    : [{ upto: 50000, rate: 100 }, { upto: 100000, rate: 90 }, { upto: 200000, rate: 80 }, { upto: 500000, rate: 70 }, { upto: Infinity, rate: 60 }];
  if (contacts <= included) {
    return { monthly: 0, included: included, note: included.toLocaleString() + ' marketing contacts included.' };
  }
  let monthly = 0;
  let cursor = included;
  for (let i = 0; i < bands.length && cursor < contacts; i++) {
    const bandEnd = Math.min(bands[i].upto, contacts);
    const span = Math.max(0, bandEnd - cursor);
    const blocks = Math.ceil(span / size);
    monthly += blocks * bands[i].rate;
    cursor += blocks * size;
  }
  return { monthly: monthly, included: included, note: 'Above ' + included.toLocaleString() + ' included contacts.' };
}

function updateHs() {
  const seats = parseInt(document.getElementById('hs-users').value, 10);
  const contacts = parseInt(document.getElementById('hs-contacts').value, 10);
  const tier = document.getElementById('hs-tier').value;
  document.getElementById('hs-users-val').textContent = seats;

  let hsMonthly = 0, hsOnboard = 0, hsShortName = '', hsFullName = '';
  if (tier === 'sales_pro') {
    hsShortName = 'HubSpot Sales Pro';
    hsFullName = 'HubSpot Sales Hub Professional';
    hsMonthly = seats * 90;
    hsOnboard = 1500;
  } else if (tier === 'sales_ent') {
    hsShortName = 'HubSpot Sales Ent';
    hsFullName = 'HubSpot Sales Hub Enterprise';
    hsMonthly = seats * 150;
    hsOnboard = 3500;
  } else if (tier === 'mkt_pro') {
    hsShortName = 'HubSpot Marketing Pro';
    hsFullName = 'HubSpot Marketing Hub Professional';
    hsMonthly = 800 + Math.max(0, seats - 3) * 45;
    hsOnboard = 3000;
  } else {
    hsShortName = 'HubSpot Marketing Ent';
    hsFullName = 'HubSpot Marketing Hub Enterprise';
    hsMonthly = 3600 + Math.max(0, seats - 5) * 75;
    hsOnboard = 7000;
  }

  const contact = contactAddonMonthly(contacts, tier);
  const contactYr = contact.monthly * 12;
  const hsSeatsYr = hsMonthly * 12;
  const hsYear1 = hsSeatsYr + hsOnboard + contactYr;
  const pipeYr = seats * 39 * 12;
  const closeStartupYr = seats * 47 * 12;
  const closeGrowthYr = seats * 99 * 12;
  const maxVal = Math.max(hsYear1, closeGrowthYr, pipeYr, 1);
  const ratio = (hsYear1 / Math.max(closeStartupYr, 1)).toFixed(1);
  const seatWord = seats === 1 ? '1 seat' : seats + ' seats';

  document.getElementById('chart-dynamic-headline').textContent =
    'At ' + seatWord + ', ' + hsShortName + ' ($' + hsYear1.toLocaleString() + ') costs ' + ratio + 'x Close Startup ($' + closeStartupYr.toLocaleString() + ') in Year 1';
  document.getElementById('chart-dynamic-subtitle').textContent =
    'Year-1 total for ' + seatWord + ' on annual billing. ' + contact.note;

  document.getElementById('bar-pipedrive').style.width = ((pipeYr / maxVal) * 100).toFixed(1) + '%';
  document.getElementById('val-pipedrive').textContent = '$' + pipeYr.toLocaleString();
  document.getElementById('bar-close-startup').style.width = ((closeStartupYr / maxVal) * 100).toFixed(1) + '%';
  document.getElementById('val-close-startup').textContent = '$' + closeStartupYr.toLocaleString();
  document.getElementById('bar-close-growth').style.width = ((closeGrowthYr / maxVal) * 100).toFixed(1) + '%';
  document.getElementById('val-close-growth').textContent = '$' + closeGrowthYr.toLocaleString();

  document.getElementById('label-hs-name').textContent = hsFullName;
  document.getElementById('meta-hs-breakdown').textContent =
    '$' + hsSeatsYr.toLocaleString() + ' seats + $' + hsOnboard.toLocaleString() + ' onboarding' +
    (contactYr > 0 ? ' + $' + contactYr.toLocaleString() + ' contacts' : '');
  document.getElementById('bar-hs-total').style.width = ((hsYear1 / maxVal) * 100).toFixed(1) + '%';
  const seatSeg = hsYear1 > 0 ? (hsSeatsYr / hsYear1) * 100 : 100;
  const onbSeg = hsYear1 > 0 ? ((hsOnboard + contactYr) / hsYear1) * 100 : 0;
  document.getElementById('bar-hs-seats').style.width = seatSeg.toFixed(2) + '%';
  document.getElementById('bar-hs-onb').style.width = onbSeg.toFixed(2) + '%';
  document.getElementById('val-hs-total').textContent = '$' + hsYear1.toLocaleString();
  document.getElementById('sub-hs-onb').textContent = '+$' + hsOnboard.toLocaleString() + ' onboarding';

  const saved = Math.max(0, hsYear1 - closeStartupYr);
  const cta = document.getElementById('hs-close-cta');
  cta.textContent = saved > 0
    ? 'Save $' + saved.toLocaleString() + '/yr with Close CRM ($0 Onboarding) →'
    : 'Compare Close CRM ($0 Onboarding) →';

  document.getElementById('hs-calc-body').innerHTML =
    '<div class="calc-math-list">' +
    '<div class="calc-math-row"><span class="calc-math-label"><strong>' + hsFullName + ' licenses</strong><span class="calc-math-formula">$' + hsMonthly.toLocaleString() + '/mo x 12 mos (' + seatWord + ')</span></span><span class="calc-math-val">$' + hsSeatsYr.toLocaleString() + '</span></div>' +
    '<div class="calc-math-row"><span class="calc-math-label"><strong>Mandatory onboarding</strong><span class="calc-math-formula">One-time direct implementation fee</span></span><span class="calc-math-val">+$' + hsOnboard.toLocaleString() + '</span></div>' +
    '<div class="calc-math-row"><span class="calc-math-label"><strong>Marketing contact tier</strong><span class="calc-math-formula">' + contacts.toLocaleString() + ' contacts. ' + contact.note + '</span></span><span class="calc-math-val">+$' + contactYr.toLocaleString() + '</span></div>' +
    '<div class="calc-math-total"><span>' + hsShortName + ' Year-1 total</span><span>$' + hsYear1.toLocaleString() + ' / yr</span></div>' +
    '<div class="calc-math-row" style="margin-top:6px;"><span class="calc-math-label"><strong>Close CRM Startup</strong><span class="calc-math-formula">' + seats + ' x $47/seat/mo x 12 mos + $0 onboarding</span></span><span class="calc-math-val">$' + closeStartupYr.toLocaleString() + ' / yr</span></div>' +
    '</div>';

  document.getElementById('chart-dynamic-footnote').innerHTML =
    '<strong>Hidden Cost Highlight:</strong> Based on ' + seatWord + ', annual billing, ' + contacts.toLocaleString() + ' marketing contacts. ' +
    hsShortName + ' adds a one-time $' + hsOnboard.toLocaleString() + ' onboarding fee' +
    (contactYr > 0 ? ' and $' + contactYr.toLocaleString() + '/yr in contact bands' : '') +
    '. Year-2 renewal drops the onboarding fee. Source: saasbill.io';

  const sub = document.getElementById('gap-dynamic-subhead');
  if (sub) sub.textContent = 'Based on ' + seatWord + ', annual billing, ' + contacts.toLocaleString() + ' marketing contacts.';

  const rows = [
    ['HubSpot ' + hsShortName, hsSeatsYr, hsOnboard, contactYr, hsYear1],
    ['Close CRM Startup', closeStartupYr, 0, 0, closeStartupYr],
    ['Close CRM Growth', closeGrowthYr, 0, 0, closeGrowthYr],
    ['Pipedrive Growth', pipeYr, 0, 0, pipeYr]
  ];
  document.getElementById('hs-compare-tbody').innerHTML = rows.map(function(r) {
    return '<tr>' +
      '<td data-label="Platform"><strong>' + r[0] + '</strong></td>' +
      '<td data-label="Licenses / Year">$' + r[1].toLocaleString() + '</td>' +
      '<td data-label="Onboarding">$' + r[2].toLocaleString() + '</td>' +
      '<td data-label="Contact tier / Year">$' + r[3].toLocaleString() + '</td>' +
      '<td data-label="Year-1 total">$' + r[4].toLocaleString() + '</td>' +
      '</tr>';
  }).join('');

  if (typeof window.trackSaaSBillEvent === 'function') {
    window.trackSaaSBillEvent('result_rendered', { page: 'hubspot-onboarding-fee-calculator', seats: seats, contacts: contacts, tier: tier });
  }
}
document.getElementById('hs-users').addEventListener('input', updateHs);
document.getElementById('hs-contacts').addEventListener('change', updateHs);
document.getElementById('hs-tier').addEventListener('change', updateHs);
const fullTableDetailsEl = document.getElementById('full-table-details');
if (fullTableDetailsEl) {
  fullTableDetailsEl.addEventListener('toggle', function() {
    const pill = document.getElementById('full-table-toggle-pill');
    if (pill) pill.innerHTML = fullTableDetailsEl.open ? 'Hide comparison &uarr;' : 'Compare all tools &darr;';
  });
}
updateHs();
</script>
"""

FAQS = [
    (
        "How much is HubSpot's mandatory onboarding fee in 2026?",
        "Direct orders charge $1,500 for Sales Hub Professional, $3,500 for Sales Hub Enterprise, $3,000 for Marketing Hub Professional, and $7,000 for Marketing Hub Enterprise. Close CRM and Pipedrive charge $0 for onboarding.",
    ),
    (
        "Do marketing contacts change the Sales Hub price?",
        "No. Sales Hub Professional and Enterprise bill seats plus the onboarding fee. Marketing contact bands apply on Marketing Hub: Professional includes 2,000 contacts, then $250 per extra 5,000 up to 22,000. Enterprise includes 10,000, then $100 per extra 10,000 up to 50,000.",
    ),
    (
        "What does HubSpot Sales Hub Professional cost for 5 users in Year 1?",
        "Five seats at $90/month billed annually are $5,400, plus the $1,500 onboarding fee, for $6,900 in Year 1. Close CRM Startup for the same five seats is $2,820 with $0 onboarding.",
    ),
]


def build():
    render_page(
        "hubspot-onboarding-fee-calculator/index.html",
        "HubSpot Onboarding Fee &amp; True Cost Calculator (2026): Pro vs Enterprise | SaaSBill",
        "Calculate HubSpot Year-1 cost with the $1,500 to $7,000 onboarding fee, extra seats, and marketing contact tiers versus Close CRM and Pipedrive.",
        "/hubspot-onboarding-fee-calculator/",
        BODY,
        faqs=FAQS,
    )


if __name__ == "__main__":
    build()
