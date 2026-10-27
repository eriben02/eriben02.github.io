import json
from layout import load_data, render_page, SITE_ORIGIN

TOOLS, AFFILIATES = load_data()
tools_js = json.dumps(TOOLS)
aff_js = json.dumps(AFFILIATES)

# ---------------------------------------------------------
# 1. Homepage: /index.html
# ---------------------------------------------------------
home_body = f"""
<section class="hero editorial-hero">
  <h1>Your SaaS bill is lying to you.</h1>
  <p class="lead">Most teams only look at the sticker price. But mandatory onboarding fees, seat-bucket minimums, and metered AI overages compound quietly and can significantly increase the real Year-1 cost of your tools.</p>
</section>

<div class="editorial-cat-bar">
  <div class="editorial-cat-top">
    <div class="cat-tabs" role="tablist" aria-label="Software Categories">
      <button type="button" class="cat-tab active" data-cat="Helpdesk & AI Support" data-track="category-select">Helpdesk &amp; AI Support</button>
      <button type="button" class="cat-tab" data-cat="CRM & Sales" data-track="category-select">CRM &amp; Sales</button>
      <button type="button" class="cat-tab" data-cat="Compliance, HIPAA & SOC 2" data-track="category-select">Compliance &amp; SOC 2</button>
      <button type="button" class="cat-tab" data-cat="Payment Processors & MoR" data-track="category-select">Payment Processors</button>
      <button type="button" class="cat-tab" data-cat="ALL" data-track="category-select">All Audited Tools</button>
    </div>
  </div>
</div>

<div class="unified-inspector-tray" id="unified-inspector-tray">
  <svg class="inspector-left-rail" id="inspector-left-rail" aria-hidden="true" overflow="visible">
    <path id="rail-svg-path" fill="none" stroke="#536B56" stroke-width="2.25" stroke-linecap="round" stroke-linejoin="round" d="" />
    <circle id="rail-svg-dot" cx="22" cy="180" r="4" fill="#536B56" />
    <polygon id="rail-svg-arrow" points="16,415 23,420 16,425" fill="#536B56" />
  </svg>
<section class="calc-box editorial-workbench" aria-labelledby="calc-heading">
  <h2 id="calc-heading" class="sr-only-control">Interactive Year-1 True-Cost Calculator (2026)</h2>
  <div class="control-group sr-only-control">
    <label for="cat-filter">Software category</label>
    <select id="cat-filter" data-track="calculator-control" data-control="category">
      <option value="Helpdesk & AI Support" selected>Helpdesk &amp; AI Support (6 tools)</option>
      <option value="CRM & Sales">CRM &amp; Sales (5 tools)</option>
      <option value="Compliance, HIPAA & SOC 2">Compliance, HIPAA &amp; SOC 2 (4 tools)</option>
      <option value="Payment Processors & MoR">Payment Processors &amp; MoR (5 rails)</option>
      <option value="ALL">All Subscription SaaS (15 tools)</option>
    </select>
  </div>

  <div class="workbench-grid">
    <!-- Left Column: ESTIMATE YOUR TRUE COST -->
    <div class="wb-col-controls">
      <div class="wb-col-title">Estimate Your True Cost</div>
      <div class="wb-controls-stack">
        <div class="wb-control-item" id="tool-select-group">
          <label class="wb-control-label" for="spotlight-tool-select">Platform to inspect</label>
          <select id="spotlight-tool-select" class="wb-tool-select" data-track="calculator-control" data-control="spotlight-tool"></select>
        </div>

        <div class="wb-control-item" id="seat-control-group">
          <span class="wb-control-label">Users / seats</span>
          <div class="wb-slider-row">
            <input type="range" id="seat-slider" min="1" max="50" value="5" aria-label="Users / seats" data-track="calculator-control" data-control="seats" />
            <span class="wb-slider-val" id="seat-val">5</span>
          </div>
        </div>

        <div class="wb-control-item" id="ai-control-group">
          <span class="wb-control-label">AI-resolved tickets / month</span>
          <div class="wb-slider-row">
            <input type="range" id="ai-slider" min="0" max="5000" step="100" value="500" aria-label="AI-resolved tickets per month" data-track="calculator-control" data-control="ai-tickets" />
            <span class="wb-slider-val" id="ai-val">500</span>
          </div>
        </div>

        <div class="wb-quiet-options" id="billing-control-group">
          <div class="wb-quiet-field">
            <label for="billing-mode">Billing:</label>
            <select id="billing-mode" data-track="calculator-control" data-control="billing-mode">
              <option value="annual">Annual</option>
              <option value="monthly">Monthly</option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <!-- Center Column: YOUR ESTIMATED TRUE COST (Static DOM 3-Row Vertical Stacked Bar + Leader Lines) -->
    <div class="wb-col-chart">
      <div class="wb-col-title" id="wb-chart-col-title">Your Estimated True Cost</div>
      <div id="wb-vbar-mount" class="wb-vbar-container" aria-live="polite">
        <div class="wb-vbar-row" id="wb-row-base" style="flex: 11.5 1 0px;">
          <div class="wb-vbar-block block-base">
            <span class="wb-block-amount" id="wb-amt-base">$660</span>
          </div>
          <div class="wb-callout-item">
            <div class="wb-leader-line"></div>
            <div class="wb-callout-text">
              <strong id="wb-call-title-base">Sticker Price: Base plan</strong>
              <span id="wb-call-sub-base">1st seat at advertised rate</span>
            </div>
          </div>
        </div>

        <div class="wb-vbar-row" id="wb-row-seats" style="flex: 20.91 1 0px;">
          <div class="wb-vbar-block block-seats">
            <span class="wb-block-amount" id="wb-amt-seats">$2,640</span>
          </div>
          <div class="wb-callout-item">
            <div class="wb-leader-line"></div>
            <div class="wb-callout-text">
              <strong id="wb-call-title-seats">Sticker Price: Added seats</strong>
              <span id="wb-call-sub-seats">Remaining team seat licenses</span>
            </div>
          </div>
        </div>

        <div class="wb-vbar-row" id="wb-row-hidden" style="flex: 67.59 1 0px;">
          <div class="wb-vbar-block block-hidden">
            <span class="wb-block-amount" id="wb-amt-hidden">$8,550</span>
          </div>
          <div class="wb-callout-item">
            <div class="wb-leader-line"></div>
            <div class="wb-callout-text">
              <strong id="wb-call-title-hidden">Hidden Cost Gap</strong>
              <span id="wb-call-sub-hidden">Onboarding, AI &amp; seat minimums</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Right Column: Progressive Disclosure (1. Result & Best Option -> 2. Why + Expandable Calculation -> 3. Contextual Primary CTA) -->
    <div class="wb-result-col" id="wb-result-mount" aria-live="polite">
      <div class="wb-selected-product" id="wb-selected-product">Zendesk Suite Team + AI</div>
      <div class="wb-big-total" id="wb-big-total-wrap"><span id="wb-big-amount">$11,850</span> <span class="wb-per-year" id="wb-big-unit">/ year</span></div>
      <p class="wb-budget-quote" id="wb-budget-quote">Estimated Year-1 total including mandatory fees &amp; overages.</p>
      <p class="wb-budget-subnote" id="wb-budget-subnote"></p>
      <div class="wb-best-option" id="wb-best-option"><strong>Best option:</strong> <a href="https://www.freshworks.com/freshdesk/pricing/" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="freshdesk-support" data-cta-location="workbench-best-option">Freshdesk Pro + Freddy AI ($3,835/yr)</a> &middot; saves $8,015/yr</div>
      <details class="calc-disclosure" id="wb-calc-details">
        <summary class="calc-disclosure-toggle" id="wb-calc-summary">See exactly how we calculated this</summary>
        <div class="calc-disclosure-body" id="wb-calc-body"></div>
      </details>
      <div class="cta-stack">
        <a id="wb-primary-cta" class="btn-cta wb-primary-cta" href="https://www.zendesk.com/pricing/" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="zendesk-suite-team" data-cta-location="workbench">View Zendesk pricing &rarr;</a>
      </div>
    </div>
  </div>
</section>

<!-- STEP 2: CATEGORY VERDICT CARDS (Best Option, Hidden Cost Highlight, Highest Cost) -->
<section class="verdict-section" id="verdict-card" aria-label="Category Verdict &amp; Best-Value Recommendations">
  <div id="calc-summary-strip" class="summary-strip" aria-live="polite"></div>
</section>

<!-- STEP 3 & 4: COMPARE ALL TOOLS (Visual Comparison Graph + Full Contract & Renewal Table behind Progressive Disclosure) -->
<section class="hidden-gap-section" aria-labelledby="gap-heading">
  <details class="full-table-disclosure" id="full-table-details">
    <summary class="full-table-summary" id="full-table-summary">
      <div class="full-table-summary-text">
        <h2 id="gap-heading" class="full-table-heading">Compare all tools in this category</h2>
        <span class="full-table-summary-sub">Visual Year-1 cost comparison graph &amp; full contract table (all tiers, lock-in rules &amp; verified sources)</span>
      </div>
      <span class="full-table-toggle-pill" id="full-table-toggle-pill">Compare all tools &darr;</span>
    </summary>
    <div class="full-table-body">
      <div class="gap-toolbar">
        <p class="gap-subhead" id="gap-dynamic-subhead">All 6 tools compared for 5 seats &middot; annual billing &middot; 500 AI tickets/mo &middot; click any row to inspect its breakdown above.</p>
        <div class="wb-quiet-field gap-sort-field" id="sort-control-group">
          <label for="sort-mode">Sort by:</label>
          <select id="sort-mode" data-track="calculator-control" data-control="sort-mode">
            <option value="lowest" selected>Lowest cost</option>
            <option value="hidden_fees">Hidden gap</option>
            <option value="highest">Highest cost</option>
            <option value="name">A&ndash;Z</option>
          </select>
        </div>
      </div>

      <div id="calc-viz-panel" class="viz-panel" role="region" aria-labelledby="viz-panel-title">
        <div class="viz-header">
          <div class="viz-title" id="viz-panel-title">Apples-to-Apples Year-1 Cost Comparison</div>
          <div class="viz-legend" id="viz-panel-legend">
            <span class="viz-legend-item"><span class="viz-swatch" style="background:var(--bar-seats);"></span>Base Licenses</span>
            <span class="viz-legend-item"><span class="viz-swatch" style="background:var(--bar-onboarding);"></span>Mandatory Onboarding</span>
            <span class="viz-legend-item"><span class="viz-swatch" style="background:var(--bar-ai);"></span>AI Overages</span>
          </div>
        </div>
        <div id="calc-viz-rows" class="viz-rows"></div>
      </div>

      <div class="table-wrap editorial-gap-table mobile-cards">
        <table>
          <caption>2026 B2B Software Year-1 True-Cost Comparison &amp; Contract Audit (USD, verified Oct 25, 2026)</caption>
          <thead>
            <tr>
              <th id="th-col-1">Scenario</th>
              <th id="th-col-2"><span class="legend-dot dot-sticker" aria-hidden="true"></span>Sticker Price / Year</th>
              <th id="th-col-3">True Cost / Year (Est.)</th>
              <th id="th-col-4"><span class="legend-dot dot-hidden" aria-hidden="true"></span>Hidden Cost Gap</th>
              <th id="th-col-5">Official Pricing</th>
            </tr>
          </thead>
          <tbody id="calc-tbody"></tbody>
        </table>
      </div>

      <p id="calc-payment-note" style="font-size:0.8rem; color:var(--muted); margin-top:6px;">
        <strong>Payment Processors &amp; MoR (Fees vs. Temporary Reserves):</strong> Because payment rails charge per transaction rather than per seat, selecting <em>Payment Processors</em> models a standardized benchmark of <strong>$50,000/month GMV across 1,000 transactions ($50 AOV, 30% international cards)</strong>. <strong>Estimated monthly processing fees</strong> (percentage + per-transaction + FX/billing surcharges) are shown separately from <strong>potential funds temporarily held</strong> (such as a 25% rolling reserve held for 90&ndash;180 days on a risk flag, which is a cashflow hold rather than a fee). To model your exact volume, open the <a href="./exit/stripe-shopify-paddle-frozen-funds-alternatives/">Interactive Payout Hold &amp; Reserve Simulator &rarr;</a>
      </p>
    </div>
  </details>
  <p class="calc-affiliate-disclosure">Independent calculations. Some vendor links are affiliate links. This never changes our rankings or calculations.</p>
</section>
</div>

<section id="all-calculators" class="editorial-below-section">
  <h2>Calculators &amp; contract audits</h2>
  <p class="gap-subhead">Dedicated models for onboarding tiers, AI resolution packs, payout reserve holds, and SOC 2 audit quotes.</p>
  <div class="card-grid">
    <div class="card">
      <span class="badge badge-high">CRM</span>
      <h3><a href="./pricing/hubspot-true-cost-and-onboarding-fees/">HubSpot Year-1 calculator &amp; onboarding audit</a></h3>
      <p>Sales Pro ($1,500), Marketing Pro ($3,000), and Enterprise onboarding fees next to Close CRM and Pipedrive.</p>
    </div>
    <div class="card">
      <span class="badge badge-high">CRM</span>
      <h3><a href="./compare/close-crm-vs-hubspot-sales-hub-5-to-20-reps/">Close CRM vs. HubSpot Sales Hub (5–20 reps)</a></h3>
      <p>Built-in VoIP calling, SMS, and $0 onboarding in Close CRM versus HubSpot Sales Pro and Pipedrive add-on stacks.</p>
    </div>
    <div class="card">
      <span class="badge badge-high">CRM</span>
      <h3><a href="./pricing/gong-io-platform-fee-and-seat-minimum-calculator/">Gong.io $5,000 platform fee &amp; seat calculator</a></h3>
      <p>Gong&rsquo;s $5,000/yr base platform fee and ~$1,600/seat licenses plus a separate CRM versus Close CRM all-in-one.</p>
    </div>
    <div class="card">
      <span class="badge badge-medium">CRM</span>
      <h3><a href="./compare/monday-crm-vs-pipedrive-vs-hubspot-seat-minimums/">monday CRM 3/5/10-seat bucket calculator</a></h3>
      <p>Where monday CRM&rsquo;s fixed 3-, 5-, and 10-seat blocks cost more than exact per-seat billing in Pipedrive or Close.</p>
    </div>
    <div class="card">
      <span class="badge badge-high">Helpdesk</span>
      <h3><a href="./intercom-fin-cost-calculator/">Intercom Fin ($0.99/resolution) cost calculator</a></h3>
      <p>How monthly ticket volume and AI resolution rates scale an Intercom invoice versus Freshdesk Freddy AI session packs.</p>
    </div>
    <div class="card">
      <span class="badge badge-high">Helpdesk</span>
      <h3><a href="./pricing/zendesk-ai-resolution-and-automated-outcome-cost/">Zendesk AI automated resolution overage calculator</a></h3>
      <p>Zendesk&rsquo;s 5&ndash;10 included AR/agent allowance and $1.50&ndash;$2.00 overage rates versus Help Scout and Freshdesk.</p>
    </div>
    <div class="card">
      <span class="badge badge-high">Payments</span>
      <h3><a href="./pricing/stripe-billing-0-7-percent-recurring-tax-calculator/">Stripe Billing 0.7% recurring revenue tax calculator</a></h3>
      <p>Stripe&rsquo;s 2.9% + 30&cent; base rate once 0.7% Billing, 0.5% Tax, and 0.4% Invoicing are added against Whop and Paddle.</p>
    </div>
    <div class="card">
      <span class="badge badge-high">Payments</span>
      <h3><a href="./compare/gumroad-vs-whop-vs-lemon-squeezy-take-rate-calculator/">Gumroad vs. Whop vs. Lemon Squeezy net payout calculator</a></h3>
      <p>Net creator payouts after Gumroad&rsquo;s 10% + 50&cent; (+ 2.9% + 30&cent;), Lemon Squeezy&rsquo;s 5% + 50&cent;, and Whop&rsquo;s 2.7% + 30&cent;.</p>
    </div>
    <div class="card">
      <span class="badge badge-high">Payments</span>
      <h3><a href="./exit/stripe-shopify-paddle-frozen-funds-alternatives/">Stripe, Shopify &amp; Paddle payout hold simulator</a></h3>
      <p>Cashflow impact of a 25% rolling reserve or capital holdback, plus card-token export rules across payment rails.</p>
    </div>
    <div class="card">
      <span class="badge badge-high">Payments</span>
      <h3><a href="./exit/paypal-180-day-permanent-limitation-fund-recovery/">PayPal 180-day limitation &amp; reserve calculator</a></h3>
      <p>Working capital locked under a 180-day PayPal hold and 3.49% + 49&cent; domestic rates versus Whop multi-processor routing.</p>
    </div>
    <div class="card">
      <span class="badge badge-low">Compliance</span>
      <h3><a href="./compare/typeform-vs-jotform-response-limit-and-hipaa-cost/">Typeform vs. Jotform response &amp; HIPAA calculator</a></h3>
      <p>Typeform&rsquo;s monthly response caps and Enterprise-only HIPAA BAA versus Jotform Gold ($99/mo annual with BAA included).</p>
    </div>
    <div class="card">
      <span class="badge badge-low">Guide</span>
      <h3><a href="./guides/jotform-wix-app-setup-and-pricing-guide/">Jotform Wix App setup &amp; B2B quote form guide</a></h3>
      <p>5-step visual and video walkthrough for embedding a B2B quote form on Wix using the official Jotform Wix App.</p>
    </div>
    <div class="card">
      <span class="badge badge-low">Pricing</span>
      <h3><a href="./pricing/jotform-pricing-tier-calculator/">Jotform 2026 pricing tier calculator (Starter to Gold)</a></h3>
      <p>Compare Starter (Free), Bronze ($34/mo), Silver ($39/mo), and Gold ($99/mo HIPAA BAA) submission and storage limits.</p>
    </div>
    <div class="card">
      <span class="badge badge-medium">Compliance</span>
      <h3><a href="./pricing/docusign-envelope-allowance-and-api-overage-calculator/">DocuSign 100-envelope cap &amp; overage calculator</a></h3>
      <p>DocuSign&rsquo;s 100 envelopes/user/year cap on Standard &amp; Business Pro plans compared with PandaDoc and Jotform Sign.</p>
    </div>
    <div class="card">
      <span class="badge badge-low">Compliance</span>
      <h3><a href="./compliance/hipaa-baa-and-soc2-pricing-tiers/">HIPAA BAA tiers &amp; SOC 2 + CPA auditor estimator</a></h3>
      <p>Minimum plans for a signed HIPAA BAA or SAML SSO, plus Vanta/Drata platform quotes and external CPA audit fees.</p>
    </div>
    <div class="card">
      <span class="badge badge-low">Compliance</span>
      <h3><a href="./compliance/google-workspace-vs-microsoft-365-hipaa-baa-tiers/">Google Workspace vs. Microsoft 365 HIPAA BAA calculator</a></h3>
      <p>Cheapest BAA-eligible edition on each suite ($7 entry), Vault and archiving gaps, and HIPAA form intake costs.</p>
    </div>
    <div class="card">
      <span class="badge badge-low">FAQ</span>
      <h3><a href="./faq/does-hubspot-charge-onboarding-fees-2026/">Does HubSpot charge onboarding fees in 2026?</a></h3>
      <p>Mandatory $1,500–$7,000 HubSpot onboarding fees by tier, Solutions Partner waivers, and $0-onboarding CRMs.</p>
    </div>
    <div class="card">
      <span class="badge badge-low">FAQ</span>
      <h3><a href="./faq/intercom-fin-ai-cost-calculator/">How much does Intercom Fin AI actually cost in 2026?</a></h3>
      <p>Per-seat + $0.99/resolution support math comparing Intercom against Freshdesk and Help Scout.</p>
    </div>
    <div class="card">
      <span class="badge badge-low">FAQ</span>
      <h3><a href="./faq/stripe-vs-paddle-true-cost/">Stripe vs. Paddle vs. Whop true cost (2026)</a></h3>
      <p>Effective take rates once Stripe Billing (0.7%), Stripe Tax (0.5%), and international FX surcharges are included.</p>
    </div>
  </div>
</section>

<section class="editorial-below-section">
  <h2>Contract clauses that rarely show up on a pricing page</h2>
  <div class="methodology-grid fine-print-grid">
    <div class="methodology-item">
      <strong>30–60 Day Auto-Renewal Locks</strong>
      Annual SaaS order forms (including HubSpot and Zendesk) typically disallow mid-term seat downgrades and require written non-renewal notice 30 to 60 days before term end, otherwise the contract auto-renews at list rate.
    </div>
    <div class="methodology-item">
      <strong>Card Vaults &amp; Rolling Reserves</strong>
      Direct processors (Stripe, Whop) let you export card tokens if you face a 25% rolling reserve. Merchants of Record (Paddle, Lemon Squeezy) are the legal seller of record and lock subscriber card tokens on termination.
    </div>
    <div class="methodology-item">
      <strong>SOC 2 Platform vs. External CPA Fees</strong>
      Compliance automation quotes (Vanta, Drata) are routinely negotiated down 30%&ndash;50% from list price, but never include the mandatory $6,500&ndash;$15,000+ independent CPA penetration and audit fee.
    </div>
  </div>
</section>

<section id="methodology" class="methodology-box" aria-labelledby="methodology-heading">
  <h2 id="methodology-heading" style="margin-top:0;">How we calculate &amp; verify Year-1 costs</h2>
  <p style="color:var(--muted); font-size:0.94rem;">Every figure on SaaSBill is computed from deterministic formulas and linked directly to the vendor&rsquo;s published pricing page, help-center billing documentation, or Master Subscription Agreement (MSA).</p>
  <div class="methodology-grid">
    <div class="methodology-item">
      <strong>Year-1 Total Formula</strong>
      <code>Year-1 Total = (12 &times; Billed Monthly Seats) + Mandatory Onboarding + (12 &times; Net AI Overage)</code>. Seat minimums and included AI allowances are applied automatically based on your slider inputs.
    </div>
    <div class="methodology-item">
      <strong>Verification Status Badges</strong>
      <span class="status-pill status-verified">Verified</span> indicates published self-serve pricing and contract terms checked directly against official vendor docs on Oct 25, 2026.<br/>
      <span class="status-pill status-estimated">Estimated (Benchmark)</span> indicates non-public, sales-quoted pricing modeled from verified buyer contract benchmarks.
    </div>
    <div class="methodology-item">
      <strong>Affiliate Disclosure &amp; Sources</strong>
      Independent calculations. Some vendor links are affiliate links. This never changes our rankings or calculations. Every CTA button links directly to the vendor&rsquo;s official site (<code>rel="nofollow noopener"</code>), alongside a primary-source link for contract verification. Spot a pricing change? Email <a href="mailto:info@saasbill.io">info@saasbill.io</a>.
    </div>
  </div>
</section>

<script>
const TOOLS = {tools_js};
const AFFILIATES = {aff_js};

function calcEffectiveSeats(tool, seats) {{
  if (tool.id === 'monday-crm') {{
    if (seats <= 3) return 3;
    if (seats <= 5) return 5;
    if (seats <= 10) return 10;
    return Math.ceil(seats / 5) * 5;
  }}
  if (tool.id === 'help-scout-plus' && seats > 50) return Math.max(seats, 10);
  return Math.max(seats, tool.seat_minimum || 1);
}}

function calcToolYear1(t, seats, aiVol, mode) {{
  const effSeats = calcEffectiveSeats(t, seats);
  const unitRate = mode === 'annual' ? t.advertised_monthly_price_usd : t.monthly_billing_price_usd;
  const fmtUnit = n => Number.isInteger(n) ? n.toLocaleString() : n.toFixed(2);
  let monthlySoftware = 0;
  let seatPaddingAnnual = 0;
  const calcSteps = [];
  if (t.id === 'hubspot-marketing-pro') {{
    const extraSeats = Math.max(0, seats - 3);
    const baseAnnual = Math.round(unitRate * 12);
    const extraAnnual = Math.round(extraSeats * 45 * 12);
    monthlySoftware = unitRate + extraSeats * 45;
    calcSteps.push({{
      key: 'base_plan',
      label: 'Base platform plan (3 core seats incl.)',
      formula: `$${{fmtUnit(unitRate)}}/mo (${{mode}}) × 12 mos`,
      amount: baseAnnual
    }});
    if (extraSeats > 0) {{
      calcSteps.push({{
        key: 'extra_seats',
        label: 'Additional core seats above 3',
        formula: `${{extraSeats}} seat${{extraSeats === 1 ? '' : 's'}} × $45/mo × 12 mos`,
        amount: extraAnnual
      }});
    }}
  }} else if (t.id === 'vanta-soc2' || t.id === 'drata-soc2' || t.id === 'jotform-hipaa') {{
    monthlySoftware = unitRate;
    const flatAnnual = Math.round(monthlySoftware * 12);
    calcSteps.push({{
      key: 'base_plan',
      label: 'Base platform subscription (flat tier)',
      formula: `$${{fmtUnit(unitRate)}}/mo (${{mode}}) × 12 mos`,
      amount: flatAnnual
    }});
  }} else {{
    monthlySoftware = effSeats * unitRate;
    seatPaddingAnnual = Math.round(Math.max(0, effSeats - seats) * unitRate * 12);
    const activeAnnual = Math.round(monthlySoftware * 12) - seatPaddingAnnual;
    calcSteps.push({{
      key: 'active_seats',
      label: `Active user licenses (${{seats}} seat${{seats === 1 ? '' : 's'}})`,
      formula: `${{seats}} × $${{fmtUnit(unitRate)}}/mo (${{mode}}) × 12 mos`,
      amount: activeAnnual
    }});
    if (seatPaddingAnnual > 0) {{
      const unused = effSeats - seats;
      calcSteps.push({{
        key: 'seat_padding',
        label: `Seat-bucket / minimum padding (${{unused}} unused seat${{unused === 1 ? '' : 's'}})`,
        formula: `${{unused}} × $${{fmtUnit(unitRate)}}/mo (${{effSeats}}-seat min) × 12 mos`,
        amount: seatPaddingAnnual
      }});
    }}
  }}
  let aiAnnual = 0;
  let aiNote = '';
  let aiFormula = 'No metered AI overage ($0)';
  if (t.id === 'zendesk-suite-team') {{
    const incl = Math.min(seats * 5, 833);
    const overageRate = mode === 'annual' ? 1.50 : 2.00;
    const aiMonthly = Math.max(0, aiVol - incl) * overageRate;
    aiAnnual = Math.round(aiMonthly * 12);
    aiNote = `${{incl}} AR/mo incl., then $${{overageRate.toFixed(2)}}/${{mode === 'annual' ? 'committed' : 'PAYG'}}`;
    aiFormula = `max(0, ${{aiVol.toLocaleString()}} - ${{incl}} incl.) × $${{overageRate.toFixed(2)}} × 12 mos`;
  }} else if (t.id === 'zendesk-suite-professional') {{
    const incl = Math.min(seats * 10, 833);
    const overageRate = mode === 'annual' ? 1.50 : 2.00;
    const aiMonthly = Math.max(0, aiVol - incl) * overageRate;
    aiAnnual = Math.round(aiMonthly * 12);
    aiNote = `${{incl}} AR/mo incl., then $${{overageRate.toFixed(2)}}/${{mode === 'annual' ? 'committed' : 'PAYG'}}`;
    aiFormula = `max(0, ${{aiVol.toLocaleString()}} - ${{incl}} incl.) × $${{overageRate.toFixed(2)}} × 12 mos`;
  }} else if (t.id === 'freshdesk-support') {{
    const annualSessions = aiVol * 12;
    const billableSessions = Math.max(0, annualSessions - 500);
    const packs = Math.ceil(billableSessions / 100);
    aiAnnual = packs * 49;
    aiNote = `500 1x free sessions, then $49/100 sessions (${{packs}} packs/yr)`;
    aiFormula = `ceil(max(0, ${{aiVol.toLocaleString()}}×12 - 500 free) / 100) = ${{packs}} packs × $49`;
  }} else {{
    const aiMonthly = (t.ai_per_resolution_usd || 0) * aiVol;
    aiAnnual = Math.round(aiMonthly * 12);
    if (t.ai_per_resolution_usd > 0) {{
      aiNote = `$${{t.ai_per_resolution_usd.toFixed(2)}}/resolution (${{aiVol.toLocaleString()}}/mo)`;
      aiFormula = `${{aiVol.toLocaleString()}}/mo × $${{t.ai_per_resolution_usd.toFixed(2)}}/res × 12 mos`;
    }}
  }}
  const annualSeatsCost = Math.round(monthlySoftware * 12);
  const onboarding = Math.round(t.mandatory_onboarding_fee_usd || 0);
  calcSteps.push({{
    key: 'onboarding',
    label: 'Mandatory Year-1 onboarding fee',
    formula: onboarding > 0 ? `One-time required setup (${{t.vendor}})` : '$0 required setup fee',
    amount: onboarding
  }});
  calcSteps.push({{
    key: 'ai_overage',
    label: 'Metered AI resolution / session usage',
    formula: aiFormula,
    amount: aiAnnual
  }});
  const year1Total = annualSeatsCost + onboarding + aiAnnual;
  const year2Total = annualSeatsCost + aiAnnual;
  const hiddenFees = onboarding + aiAnnual + seatPaddingAnnual;
  return {{
    tool: t,
    effSeats,
    unitRate,
    monthlySoftware,
    annualSeatsCost,
    onboarding,
    aiAnnual,
    seatPaddingAnnual,
    hiddenFees,
    aiNote,
    year1Total,
    year2Total,
    calcSteps
  }};
}}

const VENDOR_CTA_LABELS = {{
  'hubspot-sales-pro': 'View HubSpot pricing →',
  'hubspot-marketing-pro': 'View HubSpot pricing →',
  'hubspot-service-hub': 'View HubSpot pricing →',
  'close-crm': 'View Close pricing →',
  'pipedrive-crm': 'View Pipedrive pricing →',
  'monday-crm': 'View monday CRM pricing →',
  'intercom-fin-ai': 'View Intercom pricing →',
  'freshdesk-support': 'View Freshdesk pricing →',
  'zendesk-suite-team': 'View Zendesk pricing →',
  'zendesk-suite-professional': 'View Zendesk pricing →',
  'help-scout-plus': 'View Help Scout pricing →',
  'stripe-payments': 'View Stripe pricing →',
  'paddle-mor': 'View Paddle pricing →',
  'whop-payments': 'View Whop Payments pricing →',
  'lemon-squeezy': 'View Lemon Squeezy pricing →',
  'chargeflow': 'View Chargeflow pricing →',
  'jotform-hipaa': 'View Jotform HIPAA pricing →',
  '1password-business': 'View 1Password pricing →',
  'vanta-soc2': 'View Vanta pricing →',
  'drata-soc2': 'View Drata pricing →'
}};

const INTERNAL_AUDIT_LINKS = {{
  'hubspot-sales-pro': {{ url: './pricing/hubspot-true-cost-and-onboarding-fees/', label: 'Read HubSpot onboarding audit →' }},
  'hubspot-marketing-pro': {{ url: './pricing/hubspot-true-cost-and-onboarding-fees/', label: 'Read HubSpot onboarding audit →' }},
  'hubspot-service-hub': {{ url: './pricing/hubspot-true-cost-and-onboarding-fees/', label: 'Read HubSpot onboarding audit →' }},
  'close-crm': {{ url: './pricing/hubspot-true-cost-and-onboarding-fees/', label: 'Compare vs. HubSpot →' }},
  'pipedrive-crm': {{ url: './compare/monday-crm-vs-pipedrive-vs-hubspot-seat-minimums/', label: 'Read 1–15 seat comparison →' }},
  'monday-crm': {{ url: './compare/monday-crm-vs-pipedrive-vs-hubspot-seat-minimums/', label: 'Read 3-seat bucket audit →' }},
  'intercom-fin-ai': {{ url: './intercom-fin-cost-calculator/', label: 'Open Intercom Fin cost calculator →' }},
  'freshdesk-support': {{ url: './intercom-fin-cost-calculator/', label: 'Compare vs. Intercom Fin AI →' }},
  'zendesk-suite-team': {{ url: './pricing/zendesk-ai-resolution-and-automated-outcome-cost/', label: 'Read Zendesk AI overage audit →' }},
  'zendesk-suite-professional': {{ url: './pricing/zendesk-ai-resolution-and-automated-outcome-cost/', label: 'Read Zendesk AI overage audit →' }},
  'help-scout-plus': {{ url: './pricing/zendesk-ai-resolution-and-automated-outcome-cost/', label: 'Compare vs. Zendesk AI →' }},
  'stripe-payments': {{ url: './exit/stripe-shopify-paddle-frozen-funds-alternatives/', label: 'Open reserve simulator →' }},
  'paddle-mor': {{ url: './exit/stripe-shopify-paddle-frozen-funds-alternatives/', label: 'Read MoR token lock-in audit →' }},
  'whop-payments': {{ url: './exit/stripe-shopify-paddle-frozen-funds-alternatives/', label: 'Open reserve simulator →' }},
  'lemon-squeezy': {{ url: './exit/stripe-shopify-paddle-frozen-funds-alternatives/', label: 'Read MoR token audit →' }},
  'chargeflow': {{ url: './exit/stripe-shopify-paddle-frozen-funds-alternatives/', label: 'Open reserve simulator →' }},
  'jotform-hipaa': {{ url: './compliance/hipaa-baa-and-soc2-pricing-tiers/', label: 'Read HIPAA BAA tier matrix →' }},
  '1password-business': {{ url: './compliance/hipaa-baa-and-soc2-pricing-tiers/', label: 'Read SSO & BAA audit →' }},
  'vanta-soc2': {{ url: './compliance/hipaa-baa-and-soc2-pricing-tiers/', label: 'Open SOC 2 + auditor estimator →' }},
  'drata-soc2': {{ url: './compliance/hipaa-baa-and-soc2-pricing-tiers/', label: 'Open SOC 2 + auditor estimator →' }}
}};

const SHORT_VENDOR_NAMES = {{
  'hubspot-sales-pro': 'HubSpot',
  'hubspot-marketing-pro': 'HubSpot',
  'hubspot-service-hub': 'HubSpot',
  'close-crm': 'Close',
  'pipedrive-crm': 'Pipedrive',
  'monday-crm': 'monday CRM',
  'intercom-fin-ai': 'Intercom',
  'freshdesk-support': 'Freshdesk',
  'zendesk-suite-team': 'Zendesk',
  'zendesk-suite-professional': 'Zendesk',
  'help-scout-plus': 'Help Scout',
  'stripe-payments': 'Stripe',
  'paddle-mor': 'Paddle',
  'whop-payments': 'Whop',
  'lemon-squeezy': 'Lemon Squeezy',
  'chargeflow': 'Chargeflow',
  'jotform-hipaa': 'Jotform',
  '1password-business': '1Password',
  'vanta-soc2': 'Vanta',
  'drata-soc2': 'Drata'
}};

function getVendorCtaLabel(tool) {{
  return VENDOR_CTA_LABELS[tool.id] || `View ${{tool.vendor || tool.name}} pricing →`;
}}

function getContextualCtaLabel(tool, rowTotal, refTotal, isTrapOrHighest) {{
  const shortVendor = SHORT_VENDOR_NAMES[tool.id] || tool.vendor || tool.name;
  if (tool.id === 'chargeflow') {{
    return 'Prevent reserve holds with Chargeflow →';
  }}
  if (!isTrapOrHighest && typeof rowTotal === 'number' && typeof refTotal === 'number' && refTotal > rowTotal) {{
    const saved = Math.round(refTotal - rowTotal);
    if (saved > 0) {{
      return `Save $${{saved.toLocaleString()}}/yr with ${{shortVendor}} →`;
    }}
  }}
  return getVendorCtaLabel(tool);
}}

function renderCalcBreakdownHtml(r, seats, aiVol, mode, cat) {{
  if (cat === 'Payment Processors & MoR' && PAY_PROFILES[r.tool.id]) {{
    const prof = PAY_PROFILES[r.tool.id];
    const srcUrl = (r.tool.source_urls && r.tool.source_urls[0]) ? r.tool.source_urls[0] : '#';
    return `
      <div class="calc-math-list">
        <div class="calc-math-row">
          <span class="calc-math-label"><strong>${{prof.callTitleBase}}</strong><span class="calc-math-formula">${{prof.callSubBase}}</span></span>
          <span class="calc-math-val">$${{prof.b.toLocaleString()}}/mo</span>
        </div>
        <div class="calc-math-row">
          <span class="calc-math-label"><strong>${{prof.callTitleSeats}}</strong><span class="calc-math-formula">${{prof.callSubSeats}}</span></span>
          <span class="calc-math-val">$${{prof.s.toLocaleString()}}/mo</span>
        </div>
        <div class="calc-math-row">
          <span class="calc-math-label"><strong>${{prof.callTitleHidden}}</strong><span class="calc-math-formula">${{prof.callSubHidden}}</span></span>
          <span class="calc-math-val">$${{prof.h.toLocaleString()}}/mo</span>
        </div>
        <div class="calc-math-total">
          <span>Monthly Processing Fees ($50k GMV)</span>
          <span>$${{prof.total.toLocaleString()}}/mo ($${{(prof.total * 12).toLocaleString()}}/yr)</span>
        </div>
        <div class="calc-math-meta">
          <span>Potential 25% reserve holdback: <strong>$${{prof.held.toLocaleString()}}/mo</strong> (temporary hold, not a fee)</span>
          <a href="${{srcUrl}}" target="_blank" rel="noopener">Verified source &nearr;</a>
        </div>
      </div>
    `;
  }}
  const srcUrl = (r.tool.source_urls && r.tool.source_urls[0]) ? r.tool.source_urls[0] : '#';
  const rowsHtml = (r.calcSteps || []).map(step => `
    <div class="calc-math-row">
      <span class="calc-math-label"><strong>${{step.label}}</strong><span class="calc-math-formula">${{step.formula}}</span></span>
      <span class="calc-math-val">${{step.amount > 0 && (step.key === 'onboarding' || step.key === 'ai_overage' || step.key === 'seat_padding') ? '+' : ''}}$${{step.amount.toLocaleString()}}</span>
    </div>
  `).join('');
  const renewalText = r.onboarding > 0
    ? `Year-2 renewal (after 1x onboarding): <strong>$${{r.year2Total.toLocaleString()}}/yr</strong>`
    : `Year-2 recurring estimate: <strong>$${{r.year2Total.toLocaleString()}}/yr</strong>`;
  return `
    <div class="calc-math-list">
      ${{rowsHtml}}
      <div class="calc-math-total">
        <span>True Year-1 Total (${{mode}} billing)</span>
        <span>$${{r.year1Total.toLocaleString()}} / yr</span>
      </div>
      <div class="calc-math-meta">
        <span>${{renewalText}}</span>
        <a href="${{srcUrl}}" target="_blank" rel="noopener">Verified source &nearr;</a>
      </div>
    </div>
  `;
}}

function formatScenarioText(cat, seats, aiVol, mode) {{
  const seatStr = `${{seats}} seat${{seats === 1 ? '' : 's'}}`;
  const billStr = mode === 'annual' ? 'annual billing' : 'monthly billing';
  if (cat === 'Helpdesk & AI Support' || cat === 'ALL') {{
    return `Based on ${{seatStr}}, ${{billStr}}, ${{aiVol.toLocaleString()}} AI tickets/month`;
  }}
  return `Based on ${{seatStr}}, ${{billStr}}`;
}}

function formatHiddenReason(r) {{
  const parts = [];
  if (r.onboarding > 0) parts.push(`$${{r.onboarding.toLocaleString()}} mandatory onboarding`);
  if (r.aiAnnual > 0) parts.push(`$${{r.aiAnnual.toLocaleString()}}/yr metered AI charges`);
  if (r.seatPaddingAnnual > 0) parts.push(`$${{r.seatPaddingAnnual.toLocaleString()}}/yr unused seat-minimum padding`);
  if (parts.length === 0) return `No mandatory onboarding or metered AI overages ($0 non-seat fees)`;
  return `Adds ${{parts.join(' + ')}} on top of $${{r.annualSeatsCost.toLocaleString()}} base licenses`;
}}

// Compute high-fidelity proportional flex shares (sum = 100, each in [9, 82] -> 23px to 207px inside the 252px container)
// A 9% floor (23px) keeps the leader line and a compact 1-line label aligned at $0 or small values, while 73% of the height scales 1:1 with the true dollar amounts!
function computeSmoothBarShares(v1, v2, v3) {{
  const vals = [Math.max(0, v1), Math.max(0, v2), Math.max(0, v3)];
  const total = vals[0] + vals[1] + vals[2];
  if (total <= 0) return [33.3, 33.3, 33.4];
  const MIN_SHARE = 15.5; // 45px out of 310px so 2-line callout never pushes row height
  let shares = [0, 0, 0];
  let locked = [false, false, false];
  let remainingShare = 100;
  for (let pass = 0; pass < 3; pass++) {{
    let unlockedTotal = 0;
    for (let i = 0; i < 3; i++) {{
      if (!locked[i]) unlockedTotal += vals[i];
    }}
    if (unlockedTotal <= 0) {{
      const unlockedCount = locked.filter(x => !x).length;
      for (let i = 0; i < 3; i++) {{
        if (!locked[i]) shares[i] = remainingShare / Math.max(1, unlockedCount);
      }}
      break;
    }}
    let changed = false;
    for (let i = 0; i < 3; i++) {{
      if (!locked[i]) {{
        const raw = (vals[i] / unlockedTotal) * remainingShare;
        if (raw < MIN_SHARE) {{
          shares[i] = MIN_SHARE;
          locked[i] = true;
          remainingShare -= MIN_SHARE;
          changed = true;
        }} else {{
          shares[i] = raw;
        }}
      }}
    }}
    if (!changed) break;
  }}
  return shares.map(s => Number(s.toFixed(2)));
}}

function applyBarRowState(rowEl, share, val) {{
  if (!rowEl) return;
  rowEl.style.flex = `${{share}} 1 0%`;
  rowEl.classList.remove('is-compact');
  rowEl.classList.toggle('is-zero', val === 0);
}}

const PAY_PROFILES = {{
  'stripe-payments': {{
    b: 1450,
    s: 300,
    h: 575,
    total: 2325,
    held: 12500,
    unit: '/ mo',
    callTitleBase: 'Base card rate (2.9%)',
    callSubBase: '2.9% on $50k/mo GMV ($1,450)',
    callTitleSeats: 'Per-transaction fee ($0.30)',
    callSubSeats: '$0.30 × 1,000 tx ($300/mo)',
    callTitleHidden: 'Billing & FX surcharges',
    callSubHidden: '+0.7% Billing + 1.5% intl ($575)',
    quote: '<strong>Estimated monthly processing fees:</strong> $2,325/mo<br/><strong>Potential funds temporarily held:</strong> $12,500/mo (25% reserve)',
    sub: 'Assumptions ($50k/mo GMV, 1,000 tx, 30% intl): $1,750 base + $575 Billing/FX.',
    tableFeeSub: '$1,750 base (2.9% + $0.30) + $575 Billing/FX',
    tableHeldPill: '$12,500 / mo temporarily held',
    tableHeldSub: 'If 25% rolling reserve triggers (held 90–180 days, not a fee) · Portable card tokens'
  }},
  'paddle-mor': {{
    b: 2500,
    s: 500,
    h: 450,
    total: 3450,
    held: 12500,
    unit: '/ mo',
    callTitleBase: 'Base MoR fee (5.0%)',
    callSubBase: '5.0% on $50k/mo incl. VAT',
    callTitleSeats: 'Per-transaction fee ($0.50)',
    callSubSeats: '$0.50 × 1,000 tx ($500/mo)',
    callTitleHidden: 'FX conversion spread',
    callSubHidden: 'Est. spread on 30% intl ($450)',
    quote: '<strong>Estimated monthly processing fees:</strong> $3,450/mo<br/><strong>Potential funds temporarily held:</strong> $12,500/mo (25% hold risk)',
    sub: 'Assumptions ($50k/mo GMV, 1,000 tx, 30% intl): $3,000 MoR base + $450 FX spread.',
    tableFeeSub: '$3,000 MoR base (5.0% + $0.50) + $450 est. FX spread',
    tableHeldPill: '$12,500 / mo temporarily held',
    tableHeldSub: 'If 25% payout hold triggers on review (not a fee) · Non-exportable MoR card vault'
  }},
  'whop-payments': {{
    b: 1650,
    s: 400,
    h: 225,
    total: 2275,
    held: 0,
    unit: '/ mo',
    callTitleBase: 'Base processing (2.7% + 30¢)',
    callSubBase: '2.7% ($1,350) + 30¢ × 1k tx',
    callTitleSeats: 'Failover routing (0.8%)',
    callSubSeats: '+0.8% multi-PSP routing ($400)',
    callTitleHidden: 'International card surcharge',
    callSubHidden: '+1.5% on 30% intl volume ($225)',
    quote: '<strong>Estimated monthly processing fees:</strong> $2,275/mo<br/><strong>Potential funds temporarily held:</strong> $0/mo (multi-acquirer routing)',
    sub: 'Assumptions ($50k/mo GMV, 1,000 tx, 30% intl): $1,875/mo without orchestration.',
    tableBaseAmt: 1650,
    tableFeeSub: '$1,650 base + $400 orchestration (0.8%) + $225 intl ($1,875/mo without orchestration)',
    tableHeldPill: '$0 single-PSP hold exposure',
    tableHeldSub: 'Multi-acquirer failover routing (+0.8% / $400/mo included in fees) avoids single-processor freezes'
  }},
  'lemon-squeezy': {{
    b: 2500,
    s: 500,
    h: 475,
    total: 3475,
    held: 12500,
    unit: '/ mo',
    callTitleBase: 'Base MoR fee (5.0%)',
    callSubBase: '5.0% on $50k/mo incl. tax MoR',
    callTitleSeats: 'Per-transaction fee ($0.50)',
    callSubSeats: '$0.50 × 1,000 tx ($500/mo)',
    callTitleHidden: 'Subscription & intl surcharges',
    callSubHidden: '+0.5% sub ($250) + 1.5% intl',
    quote: '<strong>Estimated monthly processing fees:</strong> $3,475/mo<br/><strong>Potential funds temporarily held:</strong> $12,500/mo (25% reserve)',
    sub: 'Assumptions ($50k/mo GMV, 1,000 tx, 30% intl): $3,000 MoR base + $475 surcharges.',
    tableFeeSub: '$3,000 MoR base (5.0% + $0.50) + $475 subscription/intl fees',
    tableHeldPill: '$12,500 / mo temporarily held',
    tableHeldSub: 'If 25% rolling reserve triggers during onboarding review (not a fee)'
  }},
  'chargeflow': {{
    b: 0,
    s: 0,
    h: 500,
    total: 500,
    held: 0,
    unit: '/ mo',
    callTitleBase: 'Monthly platform fee ($0)',
    callSubBase: '$0 base fee or seat minimums',
    callTitleSeats: 'Lost-dispute fee ($0)',
    callSubSeats: '$0 fee on unrecovered disputes',
    callTitleHidden: '25% recovery success fee',
    callSubHidden: '25% of $2k recovered ($500/mo)',
    quote: '<strong>Estimated monthly processing fees:</strong> $500/mo<br/><strong>Potential funds temporarily held:</strong> $0/mo (add-on dispute layer)',
    sub: 'Assumptions ($50k/mo GMV, $2,000/mo recovered disputes): 25% performance fee.',
    tableBaseSub: '$0 fixed monthly base · 25% of recovered chargebacks',
    tableFeeSub: '25% fee on $2,000/mo recovered disputes ($0 if unrecovered)',
    tableHeldPill: 'Reduces PSP reserve risk',
    tableHeldSub: 'Keeps dispute ratio below 0.75% threshold · 90-day ROI guarantee'
  }}
}};

let currentSpotlightId = '';
let lastCategory = '';

function renderDirectory() {{
  const cat = document.getElementById('cat-filter').value;
  const seats = parseInt(document.getElementById('seat-slider').value, 10);
  const aiVol = parseInt(document.getElementById('ai-slider').value, 10);
  const mode = document.getElementById('billing-mode').value;
  const sortEl = document.getElementById('sort-mode');
  const sortMode = sortEl ? sortEl.value : 'lowest';
  document.getElementById('seat-val').textContent = seats.toLocaleString();
  document.getElementById('ai-val').textContent = aiVol.toLocaleString();

  const _rrKey = `${{cat}}|${{seats}}|${{aiVol}}|${{mode}}|${{sortMode}}|${{currentSpotlightId}}`;
  const _rrNow = Date.now();
  if (!window._lastRrKey || window._lastRrKey !== _rrKey || (_rrNow - (window._lastRrTs || 0)) > 150) {{
    window._lastRrKey = _rrKey;
    window._lastRrTs = _rrNow;
    if (typeof window.trackSaaSBillEvent === 'function') {{
      window.trackSaaSBillEvent('result_rendered', {{ category: cat, seats: seats, aiTickets: aiVol, billingMode: mode, sortMode: sortMode }});
    }} else {{
      window.__saasbillEvents = window.__saasbillEvents || [];
      window.__saasbillEvents.push({{ event: 'result_rendered', category: cat, seats: seats, aiTickets: aiVol, billingMode: mode, sortMode: sortMode, ts: _rrNow }});
      if (typeof window.plausible === 'function') {{
        window.plausible('result_rendered', {{ props: {{ category: cat, seats: seats, aiTickets: aiVol, billingMode: mode, sortMode: sortMode }} }});
      }}
    }}
  }}

  document.querySelectorAll('.cat-tab').forEach(btn => {{
    if (btn.getAttribute('data-cat') === cat) {{
      btn.classList.add('active');
    }} else {{
      btn.classList.remove('active');
    }}
  }});

  // Dim controls instead of hiding them with display:none so the left column height never shifts
  const aiControl = document.getElementById('ai-control-group');
  const seatControl = document.getElementById('seat-control-group');
  const billingControl = document.getElementById('billing-control-group');
  if (aiControl) {{
    if (cat === 'Helpdesk & AI Support' || cat === 'ALL') {{
      aiControl.classList.remove('is-dimmed');
    }} else {{
      aiControl.classList.add('is-dimmed');
    }}
  }}
  if (seatControl && billingControl) {{
    if (cat === 'Payment Processors & MoR') {{
      seatControl.classList.add('is-dimmed');
      billingControl.classList.add('is-dimmed');
    }} else {{
      seatControl.classList.remove('is-dimmed');
      billingControl.classList.remove('is-dimmed');
    }}
  }}

  const filtered = TOOLS.filter(t => {{
    if (cat === 'ALL') return t.category !== 'Payment Processors & MoR';
    return t.category === cat;
  }});
  const rows = filtered.map(t => calcToolYear1(t, seats, aiVol, mode));

  const getRowTotal = r => (cat === 'Payment Processors & MoR' && PAY_PROFILES[r.tool.id]) ? PAY_PROFILES[r.tool.id].total : r.year1Total;
  const getRowHidden = r => (cat === 'Payment Processors & MoR' && PAY_PROFILES[r.tool.id]) ? (PAY_PROFILES[r.tool.id].held + PAY_PROFILES[r.tool.id].h) : r.hiddenFees;
  if (sortMode === 'highest') {{
    rows.sort((a, b) => getRowTotal(b) - getRowTotal(a));
  }} else if (sortMode === 'hidden_fees') {{
    rows.sort((a, b) => getRowHidden(b) - getRowHidden(a) || getRowTotal(b) - getRowTotal(a));
  }} else if (sortMode === 'name') {{
    rows.sort((a, b) => a.tool.name.localeCompare(b.tool.name));
  }} else {{
    rows.sort((a, b) => getRowTotal(a) - getRowTotal(b));
  }}

  const toolSelect = document.getElementById('spotlight-tool-select');
  const byHiddenOrder = [...rows].sort((a, b) => getRowHidden(b) - getRowHidden(a) || getRowTotal(b) - getRowTotal(a));
  if (cat !== lastCategory || !rows.some(r => r.tool.id === currentSpotlightId)) {{
    lastCategory = cat;
    if (cat === 'Payment Processors & MoR' && rows.some(r => r.tool.id === 'stripe-payments')) {{
      currentSpotlightId = 'stripe-payments';
    }} else {{
      currentSpotlightId = byHiddenOrder.length > 0 ? byHiddenOrder[0].tool.id : (rows[0] ? rows[0].tool.id : '');
    }}
  }}
  if (toolSelect) {{
    // Update options without resetting focus if only labels changed
    const existingIds = Array.from(toolSelect.options).map(o => o.value).join(',');
    const newIds = rows.map(r => r.tool.id).join(',');
    const SHORT_TOOL_LABELS = {{
      'hubspot-sales-pro': 'HubSpot Sales Pro',
      'hubspot-marketing-pro': 'HubSpot Marketing Pro',
      'close-crm': 'Close CRM (Essentials)',
      'pipedrive-crm': 'Pipedrive CRM',
      'monday-crm': 'monday CRM (Basic)',
      'intercom-fin-ai': 'Intercom + Fin AI',
      'freshdesk-support': 'Freshdesk Pro + Freddy AI',
      'zendesk-suite-team': 'Zendesk Suite Team + AI',
      'zendesk-suite-professional': 'Zendesk Suite Pro + AI',
      'help-scout-plus': 'Help Scout Plus + AI',
      'hubspot-service-hub': 'HubSpot Service Hub',
      'stripe-payments': 'Stripe Payments',
      'paddle-mor': 'Paddle (MoR)',
      'whop-payments': 'Whop Payments',
      'lemon-squeezy': 'Lemon Squeezy (MoR)',
      'chargeflow': 'Chargeflow Defense',
      'jotform-hipaa': 'Jotform Gold (HIPAA)',
      '1password-business': '1Password Business',
      'vanta-soc2': 'Vanta (SOC 2)',
      'drata-soc2': 'Drata (SOC 2)'
    }};
    if (existingIds !== newIds) {{
      toolSelect.innerHTML = rows.map(r => {{
        const sel = r.tool.id === currentSpotlightId ? 'selected' : '';
        const shortName = SHORT_TOOL_LABELS[r.tool.id] || r.tool.name;
        return `<option value="${{r.tool.id}}" ${{sel}}>${{shortName}}</option>`;
      }}).join('');
    }} else {{
      toolSelect.value = currentSpotlightId;
    }}
  }}

  const rowBase = document.getElementById('wb-row-base');
  const rowSeats = document.getElementById('wb-row-seats');
  const rowHidden = document.getElementById('wb-row-hidden');

  const summaryEl = document.getElementById('calc-summary-strip');
  const vizPanel = document.getElementById('calc-viz-panel');
  const vizRowsEl = document.getElementById('calc-viz-rows');
  const scenarioLine = formatScenarioText(cat, seats, aiVol, mode);


  const th2 = document.getElementById('th-col-2');
  const th3 = document.getElementById('th-col-3');
  const th4 = document.getElementById('th-col-4');
  const chartColTitle = document.getElementById('wb-chart-col-title');
  const dynSubhead = document.getElementById('gap-dynamic-subhead');
  if (dynSubhead) {{
    if (cat === 'Payment Processors & MoR') {{
      dynSubhead.textContent = `All ${{rows.length}} tools compared for $50,000/mo GMV · 1,000 tx · 30% international · click any row to inspect its breakdown above.`;
    }} else if (cat === 'Helpdesk & AI Support' || cat === 'ALL') {{
      dynSubhead.textContent = `All ${{rows.length}} tools compared for ${{seats}} seat${{seats === 1 ? '' : 's'}} · ${{mode === 'annual' ? 'annual' : 'monthly'}} billing · ${{aiVol.toLocaleString()}} AI tickets/mo &middot; click any row to inspect its breakdown above.`;
    }} else {{
      dynSubhead.textContent = `All ${{rows.length}} tools compared for ${{seats}} seat${{seats === 1 ? '' : 's'}} · ${{mode === 'annual' ? 'annual' : 'monthly'}} billing · click any row to inspect its breakdown above.`;
    }}
  }}
  if (th2 && th3 && th4) {{
    if (cat === 'Payment Processors & MoR') {{
      th2.innerHTML = '<span class="legend-dot dot-sticker" aria-hidden="true"></span>Base Rate ($50k/mo Ex.)';
      th3.textContent = 'Estimated Monthly Processing Fees';
      th4.innerHTML = '<span class="legend-dot dot-hidden" aria-hidden="true"></span>Potential Funds Temporarily Held';
      if (chartColTitle) chartColTitle.textContent = 'Estimated Monthly Fees';
    }} else {{
      th2.innerHTML = '<span class="legend-dot dot-sticker" aria-hidden="true"></span>Sticker Price / Year';
      th3.textContent = 'True Cost / Year (Est.)';
      th4.innerHTML = '<span class="legend-dot dot-hidden" aria-hidden="true"></span>Hidden Cost Gap';
      if (chartColTitle) chartColTitle.textContent = 'Your Estimated True Cost';
    }}
  }}

  const wbCalcBody = document.getElementById('wb-calc-body');
  const vizTitleEl = document.getElementById('viz-panel-title');
  const vizLegendEl = document.getElementById('viz-panel-legend');

  if (cat === 'Payment Processors & MoR') {{
    const spotPayR = rows.find(r => r.tool.id === currentSpotlightId) || rows[0];
    const spotPayAff = AFFILIATES[spotPayR.tool.affiliate_slug] || {{ destination_url: '#' }};
    const prof = PAY_PROFILES[spotPayR.tool.id] || PAY_PROFILES['stripe-payments'];
    const maxPayMo = 3475;
    const [s1, s2, s3] = computeSmoothBarShares(prof.b, prof.s, prof.h);
    if (rowBase && rowSeats && rowHidden) {{
      applyBarRowState(rowBase, s1, prof.b);
      applyBarRowState(rowSeats, s2, prof.s);
      applyBarRowState(rowHidden, s3, prof.h);
      document.getElementById('wb-amt-base').textContent = `$${{prof.b.toLocaleString()}}`;
      document.getElementById('wb-call-title-base').textContent = prof.callTitleBase;
      document.getElementById('wb-call-sub-base').textContent = prof.callSubBase;

      document.getElementById('wb-amt-seats').textContent = `$${{prof.s.toLocaleString()}}`;
      document.getElementById('wb-call-title-seats').textContent = prof.callTitleSeats;
      document.getElementById('wb-call-sub-seats').textContent = prof.callSubSeats;

      document.getElementById('wb-amt-hidden').textContent = `$${{prof.h.toLocaleString()}}`;
      document.getElementById('wb-call-title-hidden').textContent = prof.callTitleHidden;
      document.getElementById('wb-call-sub-hidden').textContent = prof.callSubHidden;
    }}
    const selProdEl = document.getElementById('wb-selected-product');
    if (selProdEl) selProdEl.textContent = `${{spotPayR.tool.name}} · $50k/mo Example`;
    document.getElementById('wb-big-amount').textContent = `$${{prof.total.toLocaleString()}}`;
    document.getElementById('wb-big-unit').textContent = prof.unit;
    const quoteEl = document.getElementById('wb-budget-quote');
    if (quoteEl) quoteEl.innerHTML = prof.quote;
    document.getElementById('wb-budget-subnote').textContent = prof.sub;
    const bestOptPayEl = document.getElementById('wb-best-option');
    if (bestOptPayEl) {{
      const whopAffBest = AFFILIATES['whop'] || {{ destination_url: '#' }};
      if (spotPayR.tool.id === 'whop-payments') {{
        bestOptPayEl.innerHTML = '<strong>Best option in category:</strong> Lowest direct fee ($2,275/mo) &amp; multi-PSP failover';
      }} else {{
        bestOptPayEl.innerHTML = `<strong>Best option:</strong> <a href="${{whopAffBest.destination_url}}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="whop-payments" data-cta-location="workbench-best-option">Whop Payments ($2,275/mo)</a> &middot; $0 single-PSP reserve hold`;
      }}
    }}
    if (wbCalcBody) {{
      wbCalcBody.innerHTML = renderCalcBreakdownHtml(spotPayR, seats, aiVol, mode, cat);
    }}
    const ctaEl = document.getElementById('wb-primary-cta');
    if (ctaEl) {{
      ctaEl.href = spotPayAff.destination_url;
      ctaEl.setAttribute('data-vendor', spotPayR.tool.id);
      const isPayWinner = spotPayR.tool.id === 'whop-payments';
      ctaEl.textContent = isPayWinner
        ? getContextualCtaLabel(spotPayR.tool, prof.total * 12, maxPayMo * 12, false)
        : (spotPayR.tool.id === 'chargeflow' ? getContextualCtaLabel(spotPayR.tool, 500, 0, false) : getVendorCtaLabel(spotPayR.tool));
    }}

    if (summaryEl) {{
      const whopR = rows.find(r => r.tool.id === 'whop-payments') || rows[0];
      const paddleR = rows.find(r => r.tool.id === 'paddle-mor') || rows[0];
      const cfR = rows.find(r => r.tool.id === 'chargeflow') || rows[0];
      const whopAff = AFFILIATES[whopR.tool.affiliate_slug] || {{ destination_url: '#' }};
      const paddleAff = AFFILIATES[paddleR.tool.affiliate_slug] || {{ destination_url: '#' }};
      const cfAff = AFFILIATES[cfR.tool.affiliate_slug] || {{ destination_url: '#' }};
      summaryEl.innerHTML = `
        <div class="summary-card result-card card-lowest">
          <div class="summary-label">Lowest Direct Fee &amp; Failover Routing</div>
          <div class="summary-metric" style="color:var(--emerald);">$2,275 / mo &middot; Whop Payments</div>
          <div class="summary-scenario">Based on $50,000/mo GMV, 1,000 tx, 30% international</div>
          <div class="summary-breakdown">$1,650 base (2.7% + 30&cent;) + $400 multi-PSP routing + $225 intl ($1,875/mo without orchestration)</div>
          <div class="summary-caveat"><strong>Contract note:</strong> Direct payouts with multi-PSP failover and portable card tokens ($0 reserve hold in baseline model).</div>
          <details class="calc-disclosure">
            <summary class="calc-disclosure-toggle">See calculation</summary>
            <div class="calc-disclosure-body">${{renderCalcBreakdownHtml(whopR, seats, aiVol, mode, cat)}}</div>
          </details>
          <div class="summary-actions">
            <div class="cta-stack">
              <a class="btn-cta" href="${{whopAff.destination_url}}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="whop-payments" data-cta-location="summary-card">${{getContextualCtaLabel(whopR.tool, 2275 * 12, 3450 * 12, false)}}</a>
            </div>
          </div>
        </div>
        <div class="summary-card result-card card-hidden">
          <div class="summary-label">Hidden Cost Highlight (MoR &amp; Reserves)</div>
          <div class="summary-metric" style="color:var(--rose);">$12,500 / mo temporarily held</div>
          <div class="summary-scenario">On <strong>Paddle / Stripe / Lemon Squeezy</strong> (25% rolling reserve scenario)</div>
          <div class="summary-breakdown">$3,450/mo Paddle MoR fees ($41,400/yr) + non-exportable subscriber card vault on termination</div>
          <div class="summary-caveat"><strong>Hidden Cost Highlight:</strong> A 25% rolling reserve locks $12,500/mo in working capital for 90&ndash;180 days.</div>
          <details class="calc-disclosure">
            <summary class="calc-disclosure-toggle">See calculation</summary>
            <div class="calc-disclosure-body">${{renderCalcBreakdownHtml(paddleR, seats, aiVol, mode, cat)}}</div>
          </details>
          <div class="summary-actions">
            <div class="cta-stack">
              <a class="btn-secondary" href="${{paddleAff.destination_url}}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="paddle-mor" data-cta-location="summary-card">${{getVendorCtaLabel(paddleR.tool)}}</a>
            </div>
          </div>
        </div>
        <div class="summary-card result-card card-highest">
          <div class="summary-label">Pre-Dispute Reserve Shield</div>
          <div class="summary-metric">$500 / mo &middot; Chargeflow</div>
          <div class="summary-scenario">Based on $2,000/mo recovered chargebacks (25% success fee)</div>
          <div class="summary-breakdown">$0 monthly base fee &middot; keeps dispute ratio below 0.5% monitoring threshold</div>
          <div class="summary-caveat"><strong>Contract note:</strong> Performance-based fee (25% of recovered chargebacks only; $0 monthly minimum).</div>
          <details class="calc-disclosure">
            <summary class="calc-disclosure-toggle">See calculation</summary>
            <div class="calc-disclosure-body">${{renderCalcBreakdownHtml(cfR, seats, aiVol, mode, cat)}}</div>
          </details>
          <div class="summary-actions">
            <div class="cta-stack">
              <a class="btn-secondary" href="${{cfAff.destination_url}}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="chargeflow" data-cta-location="summary-card">${{getContextualCtaLabel(cfR.tool, 500, 0, false)}}</a>
            </div>
          </div>
        </div>
      `;
    }}

    if (vizPanel && vizRowsEl) {{
      vizPanel.style.display = 'block';
      if (vizTitleEl) vizTitleEl.textContent = 'Apples-to-Apples Monthly Processing Fee Comparison ($50k/mo GMV)';
      if (vizLegendEl) {{
        vizLegendEl.innerHTML = `
          <span class="viz-legend-item"><span class="viz-swatch" style="background:var(--bar-seats);"></span>Base Rate</span>
          <span class="viz-legend-item"><span class="viz-swatch" style="background:var(--bar-onboarding);"></span>Per-Tx / Routing</span>
          <span class="viz-legend-item"><span class="viz-swatch" style="background:var(--bar-ai);"></span>Billing / FX / Recovery</span>
        `;
      }}
      vizRowsEl.innerHTML = rows.map(r => {{
        const aff = AFFILIATES[r.tool.affiliate_slug] || {{ destination_url: '#' }};
        const p = PAY_PROFILES[r.tool.id] || PAY_PROFILES['stripe-payments'];
        const bPct = Math.max(0, (p.b / maxPayMo) * 100);
        const sPct = Math.max(0, (p.s / maxPayMo) * 100);
        const hPct = Math.max(0, (p.h / maxPayMo) * 100);
        const isSpotViz = r.tool.id === currentSpotlightId ? 'is-spotlight-row' : '';
        const rowCta = r.tool.id === 'whop-payments'
          ? getContextualCtaLabel(r.tool, p.total * 12, 3450 * 12, false)
          : (r.tool.id === 'chargeflow' ? getContextualCtaLabel(r.tool, 500, 0, false) : getVendorCtaLabel(r.tool));
        return `
          <div class="viz-row ${{isSpotViz}}" data-tool-id="${{r.tool.id}}" style="cursor:pointer;">
            <div class="viz-label" title="${{r.tool.name}}">${{r.tool.name}}</div>
            <div class="viz-bar-wrap">
              <div class="viz-bar-track" title="$${{p.total.toLocaleString()}}/mo processing fees">
                <div class="viz-seg-seats" style="width:${{bPct.toFixed(2)}}%"></div>
                ${{p.s > 0 ? `<div class="viz-seg-onboarding" style="width:${{sPct.toFixed(2)}}%"></div>` : ''}}
                ${{p.h > 0 ? `<div class="viz-seg-ai" style="width:${{hPct.toFixed(2)}}%"></div>` : ''}}
              </div>
              <div class="viz-breakdown-text">${{p.tableFeeSub}} &middot; ${{p.tableHeldPill}}</div>
            </div>
            <div class="viz-total-label">$${{p.total.toLocaleString()}} / mo</div>
            <a class="viz-action-link" href="${{aff.destination_url}}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="${{r.tool.id}}" data-cta-location="chart-row">${{rowCta}}</a>
          </div>
        `;
      }}).join('');
    }}
  }} else if (rows.length > 0) {{
    const byLowest = [...rows].sort((a, b) => a.year1Total - b.year1Total);
    const minR = byLowest[0];
    const maxR = byLowest[byLowest.length - 1];
    const byHidden = [...rows].sort((a, b) => b.hiddenFees - a.hiddenFees || b.year1Total - a.year1Total);
    const topHidden = byHidden[0];
    const maxTotal = Math.max(...rows.map(r => r.year1Total), 1);

    const spotR = rows.find(r => r.tool.id === currentSpotlightId) || topHidden || minR;
    const spotAff = AFFILIATES[spotR.tool.affiliate_slug] || {{ destination_url: '#' }};
    const refBenchmarkR = (spotR.year1Total > minR.year1Total && spotR.tool.id !== minR.tool.id)
      ? spotR
      : (topHidden.year1Total > minR.year1Total ? topHidden : maxR);

    // 3 vertical stacked bar segments that sum 100% identically to spotR.year1Total:
    const baseSubYr = Math.min(spotR.annualSeatsCost, Math.round(spotR.unitRate * 12));
    const seatsUsageYr = Math.max(0, spotR.annualSeatsCost - baseSubYr);
    const overagesAddonsYr = spotR.onboarding + spotR.aiAnnual;
    const [s1, s2, s3] = computeSmoothBarShares(baseSubYr, seatsUsageYr, overagesAddonsYr);

    if (rowBase && rowSeats && rowHidden) {{
      applyBarRowState(rowBase, s1, baseSubYr);
      applyBarRowState(rowSeats, s2, seatsUsageYr);
      applyBarRowState(rowHidden, s3, overagesAddonsYr);

      document.getElementById('wb-amt-base').textContent = `$${{baseSubYr.toLocaleString()}}`;
      document.getElementById('wb-call-title-base').textContent = 'Sticker Price: Base plan';
      document.getElementById('wb-call-sub-base').textContent = '1st seat at advertised rate';

      document.getElementById('wb-amt-seats').textContent = `$${{seatsUsageYr.toLocaleString()}}`;
      document.getElementById('wb-call-title-seats').textContent = 'Sticker Price: Added seats';
      document.getElementById('wb-call-sub-seats').textContent = 'Remaining team seat licenses';

      document.getElementById('wb-amt-hidden').textContent = `$${{overagesAddonsYr.toLocaleString()}}`;
      document.getElementById('wb-call-title-hidden').textContent = 'Hidden Cost Gap';
      document.getElementById('wb-call-sub-hidden').textContent = 'Onboarding, AI & seat minimums';
    }}

    const selProdEl = document.getElementById('wb-selected-product');
    if (selProdEl) selProdEl.textContent = spotR.tool.name;
    document.getElementById('wb-big-amount').textContent = `$${{spotR.year1Total.toLocaleString()}}`;
    document.getElementById('wb-big-unit').textContent = '/ year';
    const quoteEl = document.getElementById('wb-budget-quote');
    if (quoteEl) quoteEl.innerHTML = 'Estimated Year-1 total including mandatory fees &amp; overages.';
    const subNoteEl = document.getElementById('wb-budget-subnote');
    if (subNoteEl) {{
      const stickerYr = Math.max(0, spotR.annualSeatsCost - spotR.seatPaddingAnnual);
      const extraYr = spotR.year1Total - stickerYr;
      if (extraYr > 0) {{
        const pctOver = stickerYr > 0 ? Math.round((extraYr / stickerYr) * 100) : 0;
        subNoteEl.textContent = `+$${{extraYr.toLocaleString()}}/yr (+${{pctOver}}%) above the $${{stickerYr.toLocaleString()}} advertised price.`;
      }} else {{
        subNoteEl.textContent = `Matches advertised price ($0 hidden fees).`;
      }}
    }}
    const bestOptEl = document.getElementById('wb-best-option');
    if (bestOptEl) {{
      const minAffBest = AFFILIATES[minR.tool.affiliate_slug] || {{ destination_url: '#' }};
      const diffBest = Math.max(0, spotR.year1Total - minR.year1Total);
      if (spotR.tool.id === minR.tool.id || diffBest === 0) {{
        bestOptEl.innerHTML = `<strong>Best option in category:</strong> Lowest Year-1 true cost ($${{minR.year1Total.toLocaleString()}}/yr)`;
      }} else {{
        bestOptEl.innerHTML = `<strong>Best option:</strong> <a href="${{minAffBest.destination_url}}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="${{minR.tool.id}}" data-cta-location="workbench-best-option">${{minR.tool.name}} ($${{minR.year1Total.toLocaleString()}}/yr)</a> &middot; saves $${{diffBest.toLocaleString()}}/yr`;
      }}
    }}
    if (wbCalcBody) {{
      wbCalcBody.innerHTML = renderCalcBreakdownHtml(spotR, seats, aiVol, mode, cat);
    }}
    const ctaEl = document.getElementById('wb-primary-cta');
    if (ctaEl) {{
      ctaEl.href = spotAff.destination_url;
      ctaEl.setAttribute('data-vendor', spotR.tool.id);
      const isSpotTrapOrHighest = spotR.tool.id === topHidden.tool.id || spotR.tool.id === maxR.tool.id || spotR.onboarding > 0;
      const wbRefTotal = topHidden.year1Total > spotR.year1Total ? topHidden.year1Total : maxR.year1Total;
      ctaEl.textContent = getContextualCtaLabel(spotR.tool, spotR.year1Total, wbRefTotal, isSpotTrapOrHighest);
    }}

    const minAff = AFFILIATES[minR.tool.affiliate_slug] || {{ destination_url: '#' }};
    const maxAff = AFFILIATES[maxR.tool.affiliate_slug] || {{ destination_url: '#' }};
    const hidAff = AFFILIATES[topHidden.tool.affiliate_slug] || {{ destination_url: '#' }};

    const minAudit = INTERNAL_AUDIT_LINKS[minR.tool.id];
    const maxAudit = INTERNAL_AUDIT_LINKS[maxR.tool.id];
    const hidAudit = INTERNAL_AUDIT_LINKS[topHidden.tool.id];

    if (summaryEl) {{
      const hiddenPct = topHidden.year1Total > 0 ? Math.round((topHidden.hiddenFees / topHidden.year1Total) * 100) : 0;
      const hiddenReasonText = formatHiddenReason(topHidden);
      const savedVsRef = Math.max(0, refBenchmarkR.year1Total - minR.year1Total);
      const minCtaText = getContextualCtaLabel(minR.tool, minR.year1Total, refBenchmarkR.year1Total, false);
      summaryEl.innerHTML = `
        <div class="summary-card result-card card-lowest">
          <div class="summary-label">Best Value &middot; Lowest Year-1 Cost</div>
          <div class="summary-metric" style="color:var(--emerald);">$${{minR.year1Total.toLocaleString()}} / yr &middot; ${{minR.tool.name}}</div>
          <div class="summary-scenario">${{scenarioLine}}${{savedVsRef > 0 ? ` &middot; saves $${{savedVsRef.toLocaleString()}}/yr vs. ${{refBenchmarkR.tool.name}}` : ''}}</div>
          <div class="summary-breakdown">$${{minR.annualSeatsCost.toLocaleString()}} licenses + $${{minR.onboarding.toLocaleString()}} onboarding + $${{minR.aiAnnual.toLocaleString()}} AI</div>
          <div class="summary-caveat"><strong>Contract note:</strong> ${{minR.tool.trap_badge}} (${{minR.tool.billing_lock_in_type}})</div>
          <details class="calc-disclosure">
            <summary class="calc-disclosure-toggle">See calculation</summary>
            <div class="calc-disclosure-body">${{renderCalcBreakdownHtml(minR, seats, aiVol, mode, cat)}}</div>
          </details>
          <div class="summary-actions">
            <div class="cta-stack">
              <a class="btn-cta" href="${{minAff.destination_url}}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="${{minR.tool.id}}" data-cta-location="summary-card">${{minCtaText}}</a>
            </div>
            ${{minAudit ? `<a class="summary-audit-link" href="${{minAudit.url}}" data-track="internal-audit">${{minAudit.label}}</a>` : ''}}
          </div>
        </div>
        <div class="summary-card result-card card-hidden">
          <div class="summary-label">Hidden Cost Highlight (Largest Non-Seat Add-On)</div>
          <div class="summary-metric" style="color:var(--rose);">+$${{topHidden.hiddenFees.toLocaleString()}} / yr (${{hiddenPct}}% of Year-1 bill)</div>
          <div class="summary-scenario">On <strong>${{topHidden.tool.name}}</strong> ($${{topHidden.year1Total.toLocaleString()}}/yr total &middot; ${{scenarioLine.replace('Based on ', '')}})</div>
          <div class="summary-breakdown">$${{topHidden.annualSeatsCost.toLocaleString()}} licenses + $${{topHidden.onboarding.toLocaleString()}} onboarding + $${{topHidden.aiAnnual.toLocaleString()}} AI</div>
          <div class="summary-caveat"><strong>Hidden Cost Highlight:</strong> ${{hiddenReasonText}}.</div>
          <details class="calc-disclosure">
            <summary class="calc-disclosure-toggle">See calculation</summary>
            <div class="calc-disclosure-body">${{renderCalcBreakdownHtml(topHidden, seats, aiVol, mode, cat)}}</div>
          </details>
          <div class="summary-actions">
            <div class="cta-stack">
              <a class="btn-secondary" href="${{hidAff.destination_url}}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="${{topHidden.tool.id}}" data-cta-location="summary-card">${{getVendorCtaLabel(topHidden.tool)}}</a>
            </div>
            ${{hidAudit ? `<a class="summary-audit-link" href="${{hidAudit.url}}" data-track="internal-audit">${{hidAudit.label}}</a>` : ''}}
          </div>
        </div>
        <div class="summary-card result-card card-highest">
          <div class="summary-label">Highest Estimated Year-1 Cost</div>
          <div class="summary-metric">$${{maxR.year1Total.toLocaleString()}} / yr &middot; ${{maxR.tool.name}}</div>
          <div class="summary-scenario">${{scenarioLine}}</div>
          <div class="summary-breakdown">$${{maxR.annualSeatsCost.toLocaleString()}} licenses + $${{maxR.onboarding.toLocaleString()}} onboarding + $${{maxR.aiAnnual.toLocaleString()}} AI</div>
          <div class="summary-caveat"><strong>Contract note:</strong> ${{maxR.tool.trap_badge}}</div>
          <details class="calc-disclosure">
            <summary class="calc-disclosure-toggle">See calculation</summary>
            <div class="calc-disclosure-body">${{renderCalcBreakdownHtml(maxR, seats, aiVol, mode, cat)}}</div>
          </details>
          <div class="summary-actions">
            <div class="cta-stack">
              <a class="btn-secondary" href="${{maxAff.destination_url}}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="${{maxR.tool.id}}" data-cta-location="summary-card">${{getVendorCtaLabel(maxR.tool)}}</a>
            </div>
            ${{maxAudit ? `<a class="summary-audit-link" href="${{maxAudit.url}}" data-track="internal-audit">${{maxAudit.label}}</a>` : ''}}
          </div>
        </div>
      `;
    }}

    if (vizPanel && vizRowsEl) {{
      vizPanel.style.display = 'block';
      if (vizTitleEl) vizTitleEl.textContent = 'Apples-to-Apples Year-1 Cost Comparison';
      if (vizLegendEl) {{
        vizLegendEl.innerHTML = `
          <span class="viz-legend-item"><span class="viz-swatch" style="background:var(--bar-seats);"></span>Base Licenses</span>
          <span class="viz-legend-item"><span class="viz-swatch" style="background:var(--bar-onboarding);"></span>Mandatory Onboarding</span>
          <span class="viz-legend-item"><span class="viz-swatch" style="background:var(--bar-ai);"></span>AI Overages</span>
        `;
      }}
      vizRowsEl.innerHTML = rows.map(r => {{
        const aff = AFFILIATES[r.tool.affiliate_slug] || {{ destination_url: '#' }};
        const seatPct = Math.max(0, (r.annualSeatsCost / maxTotal) * 100);
        const onbPct = Math.max(0, (r.onboarding / maxTotal) * 100);
        const aiPct = Math.max(0, (r.aiAnnual / maxTotal) * 100);
        const parts = [`$${{r.annualSeatsCost.toLocaleString()}} licenses`];
        if (r.onboarding > 0) parts.push(`$${{r.onboarding.toLocaleString()}} onboarding`);
        if (r.aiAnnual > 0) parts.push(`$${{r.aiAnnual.toLocaleString()}} AI overage`);
        const isSpotViz = r.tool.id === currentSpotlightId ? 'is-spotlight-row' : '';
        const isSavingsOption = (r.tool.id === minR.tool.id || (r.onboarding === 0 && r.hiddenFees === 0)) && r.tool.id !== topHidden.tool.id && r.tool.id !== maxR.tool.id;
        const rowCta = getContextualCtaLabel(r.tool, r.year1Total, refBenchmarkR.year1Total, !isSavingsOption);
        return `
          <div class="viz-row ${{isSpotViz}}" data-tool-id="${{r.tool.id}}" style="cursor:pointer;">
            <div class="viz-label" title="${{r.tool.name}}">${{r.tool.name}}</div>
            <div class="viz-bar-wrap">
              <div class="viz-bar-track" title="${{parts.join(' + ')}} = $${{r.year1Total.toLocaleString()}}/yr">
                <div class="viz-seg-seats" style="width:${{seatPct.toFixed(2)}}%"></div>
                ${{r.onboarding > 0 ? `<div class="viz-seg-onboarding" style="width:${{onbPct.toFixed(2)}}%"></div>` : ''}}
                ${{r.aiAnnual > 0 ? `<div class="viz-seg-ai" style="width:${{aiPct.toFixed(2)}}%"></div>` : ''}}
              </div>
              <div class="viz-breakdown-text">${{parts.join(' + ')}}</div>
            </div>
            <div class="viz-total-label">$${{r.year1Total.toLocaleString()}} / yr</div>
            <a class="viz-action-link" href="${{aff.destination_url}}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="${{r.tool.id}}" data-cta-location="chart-row">${{rowCta}}</a>
          </div>
        `;
      }}).join('');
    }}
  }}

  document.getElementById('calc-tbody').innerHTML = rows.map(r => {{
    const t = r.tool;
    const aff = AFFILIATES[t.affiliate_slug] || {{ destination_url: '#', is_affiliate: false }};
    const verStatus = t.verification_status || 'Verified';
    const verClass = verStatus.startsWith('Verified') ? 'status-verified' : 'status-estimated';
    const srcUrl = (t.source_urls && t.source_urls[0]) ? t.source_urls[0] : aff.destination_url;
    const srcLabel = t.source_label || 'Official pricing & terms';
    const auditObj = INTERNAL_AUDIT_LINKS[t.id];
    const fmtRate = n => Number.isInteger(n) ? n.toLocaleString() : n.toFixed(2);

    const stickerAnnual = Math.max(0, r.annualSeatsCost - r.seatPaddingAnnual);
    const gapDollars = r.year1Total - stickerAnnual;
    const gapPct = stickerAnnual > 0 ? Math.round((gapDollars / stickerAnnual) * 100) : 0;

    const payProf = t.category === 'Payment Processors & MoR' ? PAY_PROFILES[t.id] : null;
    let stickerDisplay = '';
    if (payProf) {{
      const baseMo = payProf.tableBaseAmt !== undefined ? payProf.tableBaseAmt : (payProf.b + payProf.s);
      stickerDisplay = `<div class="gap-figure">$${{baseMo.toLocaleString()}} / mo</div><div class="gap-sub-detail">${{t.transaction_fee_display}}</div>`;
    }} else if (t.transaction_fee_display) {{
      stickerDisplay = `<div class="gap-figure">${{t.transaction_fee_display}}</div>`;
    }} else {{
      stickerDisplay = `<div class="gap-figure">$${{stickerAnnual.toLocaleString()}}</div><div class="gap-sub-detail">$${{fmtRate(r.unitRate)}}/seat/mo</div>`;
    }}

    const totalText = payProf
      ? `<div class="gap-figure">$${{payProf.total.toLocaleString()}} / mo</div><div class="gap-sub-detail">${{payProf.tableFeeSub}}</div>`
      : `<div class="gap-figure">$${{r.year1Total.toLocaleString()}}</div><div class="gap-sub-detail">${{r.effSeats}} billed seat${{r.effSeats === 1 ? '' : 's'}}</div>`;

    let gapCellHtml = '';
    if (payProf) {{
      const pillClass = payProf.held > 0 ? 'gap-orange-pill' : 'gap-zero-pill';
      gapCellHtml = `
        <div class="${{pillClass}}">${{payProf.tableHeldPill}}</div>
        <div class="gap-sub-detail">${{payProf.tableHeldSub}} &middot; <a href="${{srcUrl}}" target="_blank" rel="noopener">Verified source &nearr;</a></div>
      `;
    }} else if (gapDollars > 0) {{
      const breakdownParts = [];
      if (r.onboarding > 0) breakdownParts.push(`+$${{r.onboarding.toLocaleString()}} onboarding`);
      if (r.aiAnnual > 0) breakdownParts.push(`+$${{r.aiAnnual.toLocaleString()}} AI overage`);
      if (r.seatPaddingAnnual > 0) breakdownParts.push(`+$${{r.seatPaddingAnnual.toLocaleString()}} seat min`);
      gapCellHtml = `
        <div class="gap-orange-pill">${{gapPct}}% more (+$${{gapDollars.toLocaleString()}}/yr)</div>
        <div class="gap-sub-detail">${{breakdownParts.join(' · ')}} &middot; <a href="${{srcUrl}}" target="_blank" rel="noopener">Verified source &nearr;</a></div>
      `;
    }} else {{
      gapCellHtml = `
        <div class="gap-zero-pill">0% hidden gap</div>
        <div class="gap-sub-detail">${{t.trap_badge}} &middot; <a href="${{srcUrl}}" target="_blank" rel="noopener">Verified source &nearr;</a></div>
      `;
    }}

    const isSpot = t.id === currentSpotlightId ? 'is-spotlight-row' : '';
    return `
      <tr class="${{isSpot}}" data-row-tool="${{t.id}}" style="cursor:pointer;">
        <td data-label="Platform">
          <div class="gap-platform-name">
            <strong>${{t.name}}</strong>
            <span class="status-pill ${{verClass}}">${{verStatus}}</span>
          </div>
          <div class="gap-platform-meta">${{t.category}}${{auditObj ? ` &middot; <a class="audit-inline-link" href="${{auditObj.url}}" data-track="internal-audit">${{auditObj.label}}</a>` : ''}}</div>
        </td>
        <td data-label="Sticker Price / Year">${{stickerDisplay}}</td>
        <td data-label="Year-1 Total">${{totalText}}</td>
        <td data-label="Hidden Cost Gap">${{gapCellHtml}}</td>
        <td data-label="Official Pricing">
          <div class="cta-stack">
            <a class="btn-secondary" href="${{aff.destination_url}}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="${{t.id}}" data-cta-location="table-row">${{getVendorCtaLabel(t)}}</a>
          </div>
        </td>
      </tr>
    `;
  }}).join('');
  equalizeSummaryCards(summaryEl);
}}

function equalizeSummaryCards(stripEl) {{
  if (!stripEl) return;
  const cards = Array.from(stripEl.querySelectorAll('.summary-card'));
  if (!cards.length) return;
  const rowSelectors = ['.summary-label', '.summary-metric', '.summary-scenario', '.summary-breakdown', '.summary-caveat', '.summary-actions'];
  const disclosures = cards.map(c => c.querySelector('.calc-disclosure'));
  rowSelectors.forEach(sel => {{
    cards.forEach(c => {{
      const el = c.querySelector(sel);
      if (el) el.style.minHeight = '';
    }});
  }});
  disclosures.forEach(d => {{ if (d) d.style.marginTop = '4px'; }});
  if (window.innerWidth <= 768 || cards.length < 2) return;
  const firstTop = cards[0].getBoundingClientRect().top;
  const sameRow = cards.every(c => Math.abs(c.getBoundingClientRect().top - firstTop) < 5);
  if (!sameRow) return;
  rowSelectors.forEach(sel => {{
    const els = cards.map(c => c.querySelector(sel));
    const maxH = Math.max(...els.map(el => el ? el.getBoundingClientRect().height : 0));
    if (maxH > 0) {{
      els.forEach(el => {{ if (el) el.style.minHeight = `${{maxH}}px`; }});
    }}
  }});
  const offsets = cards.map((c, i) => {{
    const d = disclosures[i];
    return d ? (d.getBoundingClientRect().top - c.getBoundingClientRect().top) : 0;
  }});
  const maxOffset = Math.max(...offsets);
  cards.forEach((c, i) => {{
    const d = disclosures[i];
    if (d) {{
      const extra = Math.max(0, maxOffset - offsets[i]);
      d.style.marginTop = `${{4 + extra}}px`;
      if (!d.dataset.railBound) {{
        d.dataset.railBound = '1';
        d.addEventListener('toggle', () => requestAnimationFrame(updateInspectorRail));
      }}
    }}
  }});
}}

['cat-filter', 'seat-slider', 'ai-slider', 'billing-mode', 'sort-mode'].forEach(id => {{
  const el = document.getElementById(id);
  if (el) {{
    el.addEventListener('input', renderDirectory);
    el.addEventListener('change', renderDirectory);
  }}
}});

const spotSelectEl = document.getElementById('spotlight-tool-select');
if (spotSelectEl) {{
  spotSelectEl.addEventListener('change', (e) => {{
    currentSpotlightId = e.target.value;
    renderDirectory();
  }});
}}

document.addEventListener('click', (e) => {{
  const tr = e.target.closest('tr[data-row-tool]');
  if (tr && !e.target.closest('a')) {{
    currentSpotlightId = tr.getAttribute('data-row-tool');
    if (typeof window.trackSaaSBillEvent === 'function') {{
      window.trackSaaSBillEvent('calculator_interaction', {{ control: 'inspect-row', value: currentSpotlightId }});
    }}
    renderDirectory();
  }}
  const vizRow = e.target.closest('.viz-row[data-tool-id]');
  if (vizRow && !e.target.closest('a')) {{
    currentSpotlightId = vizRow.getAttribute('data-tool-id');
    if (typeof window.trackSaaSBillEvent === 'function') {{
      window.trackSaaSBillEvent('calculator_interaction', {{ control: 'inspect-row', value: currentSpotlightId }});
    }}
    renderDirectory();
  }}
}});

document.querySelectorAll('.cat-tab').forEach(btn => {{
  btn.addEventListener('click', () => {{
    const catSelect = document.getElementById('cat-filter');
    if (catSelect) {{
      catSelect.value = btn.getAttribute('data-cat');
      renderDirectory();
    }}
  }});
}});
let _railAnimId = null;
let _railCurrY1 = null;
let _railCurrY2 = null;

function drawRailSvg(y1, y2) {{
  const path = document.getElementById('rail-svg-path');
  const dot = document.getElementById('rail-svg-dot');
  const arrow = document.getElementById('rail-svg-arrow');
  if (!path || !dot || !arrow) return;
  const r = 6;
  const xStem = 2;
  const xTopEnd = 22;
  const xBotEnd = 18;
  // Single continuous path with rounded corners: from top card (xTopEnd, y1) -> left stem (xStem) -> down to active row (y2) -> right to arrow base (xBotEnd, y2)
  const d = `M ${{xTopEnd}} ${{y1.toFixed(1)}} L ${{xStem + r}} ${{y1.toFixed(1)}} Q ${{xStem}} ${{y1.toFixed(1)}} ${{xStem}} ${{(y1 + r).toFixed(1)}} L ${{xStem}} ${{(y2 - r).toFixed(1)}} Q ${{xStem}} ${{y2.toFixed(1)}} ${{xStem + r}} ${{y2.toFixed(1)}} L ${{xBotEnd}} ${{y2.toFixed(1)}}`;
  path.setAttribute('d', d);
  dot.setAttribute('cy', y1.toFixed(1));
  arrow.setAttribute('points', `${{xBotEnd - 2}},${{(y2 - 4.8).toFixed(1)}} ${{xBotEnd + 5}},${{y2.toFixed(1)}} ${{xBotEnd - 2}},${{(y2 + 4.8).toFixed(1)}}`);
}}

function updateInspectorRail() {{
  const tray = document.getElementById('unified-inspector-tray');
  const rail = document.getElementById('inspector-left-rail');
  const wbCard = tray ? tray.querySelector('.editorial-workbench') : null;
  const tableDetails = document.getElementById('full-table-details');
  const activeTableRow = tray ? tray.querySelector('tr.is-spotlight-row') : null;
  const activeVizRow = tray ? tray.querySelector('.viz-row.is-spotlight-row') : null;
  const activeRow = (tableDetails && tableDetails.open) ? (activeVizRow || activeTableRow) : null;
  if (!tray || !rail || !wbCard || !activeRow || window.innerWidth <= 960) {{
    if (rail) rail.style.opacity = '0';
    return;
  }}
  const trayRect = tray.getBoundingClientRect();
  const wbRect = wbCard.getBoundingClientRect();
  const rowRect = activeRow.getBoundingClientRect();
  const targetY1 = (wbRect.top - trayRect.top) + wbRect.height * 0.5;
  const targetY2 = (rowRect.top - trayRect.top) + rowRect.height * 0.5;
  if (targetY2 <= targetY1 + 20) {{
    rail.style.opacity = '0';
    return;
  }}
  rail.style.opacity = '1';
  if (_railCurrY1 === null || _railCurrY2 === null) {{
    _railCurrY1 = targetY1;
    _railCurrY2 = targetY2;
    drawRailSvg(_railCurrY1, _railCurrY2);
    return;
  }}
  if (_railAnimId) cancelAnimationFrame(_railAnimId);
  const startY1 = _railCurrY1;
  const startY2 = _railCurrY2;
  const startTime = performance.now();
  const duration = 260;
  function step(now) {{
    const t = Math.min(1, (now - startTime) / duration);
    const ease = 1 - Math.pow(1 - t, 3); // cubic ease-out
    _railCurrY1 = startY1 + (targetY1 - startY1) * ease;
    _railCurrY2 = startY2 + (targetY2 - startY2) * ease;
    drawRailSvg(_railCurrY1, _railCurrY2);
    if (t < 1) {{
      _railAnimId = requestAnimationFrame(step);
    }} else {{
      _railAnimId = null;
    }}
  }}
  _railAnimId = requestAnimationFrame(step);
}}

function resolveContextFromToken(raw) {{
  if (!raw) return null;
  const s = String(raw).toLowerCase().trim();
  if (!s) return null;
  const exactTool = TOOLS.find(t => t.id === s);
  if (exactTool) {{
    return {{ cat: exactTool.category, tool: exactTool.id }};
  }}
  const toolAliases = [
    ['hubspot-marketing', 'hubspot-marketing-pro'],
    ['hubspot-service', 'hubspot-service-hub'],
    ['hubspot', 'hubspot-sales-pro'],
    ['close-crm', 'close-crm'],
    ['close', 'close-crm'],
    ['pipedrive', 'pipedrive-crm'],
    ['monday', 'monday-crm'],
    ['intercom', 'intercom-fin-ai'],
    ['zendesk-pro', 'zendesk-suite-professional'],
    ['zendesk', 'zendesk-suite-team'],
    ['freshdesk', 'freshdesk-support'],
    ['helpscout', 'help-scout-plus'],
    ['help-scout', 'help-scout-plus'],
    ['stripe', 'stripe-payments'],
    ['whop', 'whop-payments'],
    ['paddle', 'paddle-mor'],
    ['lemon-squeezy', 'lemon-squeezy'],
    ['lemonsqueezy', 'lemon-squeezy'],
    ['chargeflow', 'chargeflow'],
    ['jotform', 'jotform-hipaa'],
    ['typeform', 'jotform-hipaa'],
    ['1password', '1password-business'],
    ['vanta', 'vanta-soc2'],
    ['drata', 'drata-soc2']
  ];
  for (let i = 0; i < toolAliases.length; i++) {{
    const k = toolAliases[i][0];
    const tid = toolAliases[i][1];
    if (s === k || s.indexOf(k) !== -1) {{
      const tObj = TOOLS.find(t => t.id === tid);
      if (tObj) return {{ cat: tObj.category, tool: tObj.id }};
    }}
  }}
  if (s === 'all') return {{ cat: 'ALL', tool: '' }};
  if (s.indexOf('payment') !== -1 || s.indexOf('mor') !== -1 || s.indexOf('paypal') !== -1 || s.indexOf('gumroad') !== -1) {{
    return {{ cat: 'Payment Processors & MoR', tool: 'stripe-payments' }};
  }}
  if (s.indexOf('crm') !== -1 || s.indexOf('sales') !== -1 || s.indexOf('gong') !== -1) {{
    return {{ cat: 'CRM & Sales', tool: 'hubspot-sales-pro' }};
  }}
  if (s.indexOf('compliance') !== -1 || s.indexOf('hipaa') !== -1 || s.indexOf('soc2') !== -1 || s.indexOf('docusign') !== -1) {{
    return {{ cat: 'Compliance, HIPAA & SOC 2', tool: 'jotform-hipaa' }};
  }}
  if (s.indexOf('helpdesk') !== -1 || s.indexOf('support') !== -1 || s === 'ai') {{
    return {{ cat: 'Helpdesk & AI Support', tool: 'zendesk-suite-team' }};
  }}
  return null;
}}

function applyInitialContext(onlyHash) {{
  try {{
    const catSelect = document.getElementById('cat-filter');
    if (!catSelect) return;
    let resolved = null;
    const hashRaw = (window.location && window.location.hash ? window.location.hash.replace(/^#/, '') : '').toLowerCase();
    if (onlyHash) {{
      if (hashRaw && hashRaw !== 'all-calculators' && hashRaw !== 'methodology') {{
        resolved = resolveContextFromToken(hashRaw);
      }}
    }} else {{
      const params = new URLSearchParams(window.location ? window.location.search : '');
      const qTool = params.get('tool');
      const qCat = params.get('cat') || params.get('category');
      if (qTool) {{
        resolved = resolveContextFromToken(qTool);
      }}
      if (!resolved && qCat) {{
        resolved = resolveContextFromToken(qCat);
      }}
      if (!resolved && hashRaw && hashRaw !== 'all-calculators' && hashRaw !== 'methodology') {{
        resolved = resolveContextFromToken(hashRaw);
      }}
      if (!resolved && typeof document !== 'undefined' && document.referrer) {{
        resolved = resolveContextFromToken(document.referrer);
      }}
      if (!resolved && typeof sessionStorage !== 'undefined') {{
        const savedCat = sessionStorage.getItem('saasbill_last_cat');
        const savedTool = sessionStorage.getItem('saasbill_last_tool') || '';
        if (savedCat) {{
          resolved = {{ cat: savedCat, tool: savedTool }};
        }}
      }}
    }}
    if (resolved && resolved.cat) {{
      catSelect.value = resolved.cat;
      if (resolved.tool) {{
        currentSpotlightId = resolved.tool;
        lastCategory = resolved.cat;
      }}
    }}
  }} catch (err) {{}}
}}

const _origRenderDirectory = renderDirectory;
renderDirectory = function() {{
  _origRenderDirectory();
  requestAnimationFrame(updateInspectorRail);
}};
const fullTableDetailsEl = document.getElementById('full-table-details');
if (fullTableDetailsEl) {{
  fullTableDetailsEl.addEventListener('toggle', () => {{
    const pillEl = document.getElementById('full-table-toggle-pill');
    if (pillEl) {{
      pillEl.innerHTML = fullTableDetailsEl.open ? 'Hide comparison &uarr;' : 'Compare all tools &darr;';
    }}
    if (typeof window.trackSaaSBillEvent === 'function') {{
      window.trackSaaSBillEvent('calculator_interaction', {{ control: 'compare-all-tools', value: fullTableDetailsEl.open ? 'open' : 'closed' }});
    }}
    requestAnimationFrame(updateInspectorRail);
  }});
}}
const wbCalcDetailsEl = document.getElementById('wb-calc-details');
if (wbCalcDetailsEl) {{
  wbCalcDetailsEl.addEventListener('toggle', () => {{
    requestAnimationFrame(updateInspectorRail);
  }});
}}
window.addEventListener('resize', () => {{
  equalizeSummaryCards(document.getElementById('calc-summary-strip'));
  requestAnimationFrame(updateInspectorRail);
}});
window.addEventListener('hashchange', () => {{
  applyInitialContext(true);
  renderDirectory();
}});
applyInitialContext(false);
renderDirectory();
</script>
"""

home_faqs = [
    ("Which B2B SaaS tools charge mandatory onboarding fees in 2026?", "HubSpot charges mandatory one-time onboarding fees on its Professional and Enterprise tiers: $1,500 for Sales Hub Professional, $3,500 for Sales Hub Enterprise, $3,000 for Marketing Hub Professional, and $7,000 for Marketing Hub Enterprise (verified Oct 2026). Alternatives like Close CRM, Pipedrive, and Freshdesk charge $0 for onboarding."),
    ("How does Intercom's $0.99 per Fin AI resolution pricing work?", "Intercom charges a per-seat monthly fee ($29 Essential, $85 Advanced, or $132 Expert billed annually) plus $0.99 for every customer conversation resolved by its Fin AI agent (and $9.99 for sales qualification). If Fin AI resolves 2,000 tickets a month, it adds $1,980/month ($23,760/year) to your seat invoice."),
    ("Why does monday CRM cost more than advertised for 1 or 2 users?", "monday CRM enforces a 3-seat minimum and bills in fixed seat buckets (3, 5, 10, 15 seats). A solo user on the $12/seat Basic ($18/seat monthly) or $17/seat Standard ($25/seat monthly) plan must pay for 3 seats ($36/month annual or $54/month monthly on Basic). For 1–2 users, Pipedrive ($14–$34/seat) or Close CRM Essentials ($35/user/month annual, $49/user/month monthly) is cheaper because they bill per exact seat."),
    ("What happens to subscriber card tokens if Paddle or Stripe terminates my account?", "With Stripe (2.9% + $0.30), you are the merchant and own the customer relationship, allowing PGP-encrypted card token exports unless terminated for fraud. With a Merchant of Record like Paddle (5% + $0.50), Paddle is the legal seller of record and owns the card vault; if Paddle terminates your account on a risk review, you cannot export card tokens and every subscriber must re-enter their payment details.")
]

render_page(
    "index.html",
    "saasbill.io – True Year-1 SaaS Cost & Fee Calculator (2026)",
    "Calculate the 2026 true cost and Year-1 invoice of B2B SaaS tools including HubSpot mandatory onboarding fees ($1,500-$7,000), Intercom and Zendesk AI cost overages, CRM seat minimums, and Stripe vs. Paddle vs. Whop fees.",
    "/",
    home_body,
    faqs=home_faqs,
    extra_schema={
        "@type": "Dataset",
        "name": "SaaSBill 2026 B2B SaaS True-Cost & Contract Trap Dataset",
        "description": "Verified 2026 pricing, mandatory onboarding fees, seat-bucket minimums, AI resolution rates, and payout reserve rules across 20 B2B SaaS and payment platforms.",
        "url": f"{SITE_ORIGIN}/",
        "dateModified": "2026-10-25",
        "creator": {"@type": "Organization", "name": "SaaSBill Editorial"}
    }
)

# ---------------------------------------------------------
# 2. Page 1: HubSpot True Cost & Onboarding Fees
# ---------------------------------------------------------
p1_body = """
<section class="hero">
  <h1>What HubSpot actually costs in Year 1 (once you add onboarding).</h1>
  <p class="lead">In 2026, HubSpot Sales Hub Professional costs $90/seat/month billed annually plus a mandatory $1,500 onboarding fee ($6,900 in Year 1 for five reps), while Marketing Hub Professional costs $800/month plus a $3,000 onboarding fee ($12,600 in Year 1). Every Professional and Enterprise order form is a 12-month commitment that auto-renews even on monthly installments.</p>
</section>

<section class="calc-box editorial-bar-chart-card" id="crm-apples-to-apples-chart" aria-labelledby="chart-dynamic-headline">
  <div class="calc-grid ebc-controls-grid">
    <div class="control-group">
      <label for="hs-seats">Sales team size (core seats): <span class="val-pill" id="hs-seats-val">5</span> reps</label>
      <input type="range" id="hs-seats" min="1" max="30" value="5" data-track="calculator-control" data-control="hs-seats" />
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
  <p id="chart-dynamic-subtitle" class="ebc-subtitle">Year-1 total contract cost for 5 sales reps on annual billing with multi-pipeline automation and sales sequences (licenses + mandatory onboarding).</p>

  <div class="ebc-rows" role="list" aria-live="polite">
    <div class="ebc-row" role="listitem">
      <div class="ebc-label-col">
        <div class="ebc-tool-name">
          <a href="https://www.pipedrive.com/en/pricing" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="pipedrive-crm" data-cta-location="benchmark-chart">Pipedrive Growth &nearr;</a>
        </div>
        <div class="ebc-tool-meta">Sequences &amp; automation incl. &middot; Calling add-on extra &middot; $0 onboarding</div>
      </div>
      <div class="ebc-bar-col">
        <div class="ebc-bar-track">
          <div id="bar-pipedrive" class="ebc-bar-fill ebc-fill-neutral" style="width: 33.9%;"></div>
        </div>
      </div>
      <div class="ebc-val-col">
        <span id="val-pipedrive" class="ebc-val-main">$2,340</span>
        <span class="ebc-val-sub">$39/seat/mo</span>
      </div>
    </div>

    <div class="ebc-row" role="listitem">
      <div class="ebc-label-col">
        <div class="ebc-tool-name">
          <a href="https://www.freshworks.com/crm/pricing/" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="freshsales" data-cta-location="benchmark-chart">Freshsales Pro &nearr;</a>
        </div>
        <div class="ebc-tool-meta">Multi-pipeline &amp; workflows incl. &middot; $0 onboarding</div>
      </div>
      <div class="ebc-bar-col">
        <div class="ebc-bar-track">
          <div id="bar-freshsales" class="ebc-bar-fill ebc-fill-neutral" style="width: 33.9%;"></div>
        </div>
      </div>
      <div class="ebc-val-col">
        <span id="val-freshsales" class="ebc-val-main">$2,340</span>
        <span class="ebc-val-sub">$39/seat/mo</span>
      </div>
    </div>

    <div class="ebc-row ebc-row-sage" role="listitem">
      <div class="ebc-label-col">
        <div class="ebc-tool-name">
          <a href="https://refer.close.com/3k5hp07b8soi-fetl0j" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="close" data-cta-location="benchmark-chart">Close CRM Startup &nearr;</a>
        </div>
        <div class="ebc-tool-meta">Includes built-in VoIP calling &amp; SMS workflows &middot; $0 onboarding</div>
      </div>
      <div class="ebc-bar-col">
        <div class="ebc-bar-track">
          <div id="bar-close-startup" class="ebc-bar-fill ebc-fill-sage" style="width: 40.9%;"></div>
        </div>
      </div>
      <div class="ebc-val-col">
        <span id="val-close-startup" class="ebc-val-main ebc-val-sage">$2,820</span>
        <span class="ebc-val-sub">$47/seat/mo</span>
      </div>
    </div>

    <div class="ebc-row" role="listitem">
      <div class="ebc-label-col">
        <div class="ebc-tool-name">
          <a href="https://refer.close.com/3k5hp07b8soi-fetl0j" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="close" data-cta-location="benchmark-chart">Close CRM Growth &nearr;</a>
        </div>
        <div class="ebc-tool-meta">Includes Power Dialer &amp; AI call summaries &middot; $0 onboarding</div>
      </div>
      <div class="ebc-bar-col">
        <div class="ebc-bar-track">
          <div id="bar-close-growth" class="ebc-bar-fill ebc-fill-slate" style="width: 86.1%;"></div>
        </div>
      </div>
      <div class="ebc-val-col">
        <span id="val-close-growth" class="ebc-val-main">$5,940</span>
        <span class="ebc-val-sub">$99/seat/mo</span>
      </div>
    </div>

    <div class="ebc-row ebc-row-terracotta" role="listitem">
      <div class="ebc-label-col">
        <div id="label-hs-name" class="ebc-tool-name">HubSpot Sales Hub Professional</div>
        <div id="meta-hs-breakdown" class="ebc-tool-meta">$5,400 seats + $1,500 onboarding</div>
      </div>
      <div class="ebc-bar-col">
        <div class="ebc-bar-track">
          <div id="bar-hs-total" class="ebc-bar-fill ebc-fill-terracotta" style="width: 100%;">
            <span id="bar-hs-seats" class="ebc-bar-seg-seats" style="width: 78.26%;" title="$5,400 annual seats"></span>
            <span id="bar-hs-onb" class="ebc-bar-seg-onb" style="width: 21.74%;" title="+$1,500 mandatory onboarding"></span>
          </div>
        </div>
      </div>
      <div class="ebc-val-col">
        <span id="val-hs-total" class="ebc-val-main ebc-val-terracotta">$6,900</span>
        <span id="sub-hs-onb" class="ebc-val-sub">+$1,500 onboarding</span>
      </div>
    </div>
  </div>

  <details class="calc-disclosure" id="hs-calc-details" style="margin-top:12px;">
    <summary class="calc-disclosure-toggle">See exactly how we calculated this</summary>
    <div class="calc-disclosure-body" id="hs-calc-body"></div>
  </details>

  <div id="hs-summary" class="ebc-action-strip">
    <a id="hs-close-cta" class="btn-affiliate" href="https://refer.close.com/3k5hp07b8soi-fetl0j" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="close" data-cta-location="benchmark-cta">Save $4,080/yr with Close CRM ($0 Onboarding) &rarr;</a>
    <a class="ebc-secondary-link" href="https://www.hubspot.com/pricing/sales" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="hubspot" data-cta-location="benchmark-cta">View official HubSpot Sales Hub pricing &nearr;</a>
  </div>

  <p id="chart-dynamic-footnote" class="ebc-footer-note"><strong>Hidden Cost Highlight:</strong> Based on 5 seats, annual billing. Official prices verified Oct 2026. All tiers compared include multi-stage pipelines and automated sales sequences for 5 seats billed annually (Close CRM Essentials is $35/user/mo for basic pipelines without sequences). HubSpot Sales Pro requires a one-time $1,500 onboarding fee in Year 1; Year-2 renewal drops to $5,400/yr. Source: saasbill.io</p>
</section>

<section>
  <h2>The 2026 HubSpot onboarding fee schedule</h2>
  <p class="section-tldr">HubSpot requires paid onboarding across all Professional and Enterprise hubs purchased directly. The only way to waive HubSpot’s direct onboarding fee is to sign through an accredited HubSpot Solutions Partner who handles the implementation instead.</p>
  <div class="table-wrap mobile-cards">
    <table>
      <caption>HubSpot 2026 Seat Rates &amp; Mandatory Onboarding Fees (USD, verified Oct 25, 2026)</caption>
      <thead>
        <tr>
          <th>HubSpot Hub &amp; Edition</th>
          <th>Annual Billing Rate</th>
          <th>Monthly Installment Rate (12-Mo Term)</th>
          <th>Mandatory Onboarding Fee</th>
          <th>Year-1 Minimum Spend</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td data-label="Edition"><strong>Sales Hub Professional</strong> <span class="status-pill status-verified">Verified</span></td>
          <td data-label="Annual Rate">$90 / seat / mo</td>
          <td data-label="Monthly Installment">$100 / seat / mo</td>
          <td data-label="Onboarding"><span class="badge badge-high">$1,500 one-time</span></td>
          <td data-label="Year-1 Min Spend">$2,580 (1 seat) &middot; $6,900 (5 seats)</td>
        </tr>
        <tr>
          <td data-label="Edition"><strong>Sales Hub Enterprise</strong> <span class="status-pill status-verified">Verified</span></td>
          <td data-label="Annual Rate">$150 / seat / mo</td>
          <td data-label="Monthly Installment">$150 / seat / mo (Annual only)</td>
          <td data-label="Onboarding"><span class="badge badge-high">$3,500 one-time</span></td>
          <td data-label="Year-1 Min Spend">$5,300 (1 seat) &middot; $12,500 (5 seats)</td>
        </tr>
        <tr>
          <td data-label="Edition"><strong>Marketing Hub Professional</strong> <span class="status-pill status-verified">Verified</span></td>
          <td data-label="Annual Rate">$800 / mo (3 core seats incl.)</td>
          <td data-label="Monthly Installment">$890 / mo (12-mo commitment)</td>
          <td data-label="Onboarding"><span class="badge badge-high">$3,000 one-time</span></td>
          <td data-label="Year-1 Min Spend">$12,600 / yr (+$45/mo per extra seat)</td>
        </tr>
        <tr>
          <td data-label="Edition"><strong>Marketing Hub Enterprise</strong> <span class="status-pill status-verified">Verified</span></td>
          <td data-label="Annual Rate">$3,600 / mo (5 core seats incl.)</td>
          <td data-label="Monthly Installment">$3,600 / mo (Annual only)</td>
          <td data-label="Onboarding"><span class="badge badge-high">$7,000 one-time</span></td>
          <td data-label="Year-1 Min Spend">$50,200 / yr (+$75/mo per extra seat)</td>
        </tr>
      </tbody>
    </table>
  </div>

  <h2>Contract clauses to check before you sign</h2>
  <div class="evidence-box">
    <strong>1. "Monthly payment" is still a binding 12-month contract with auto-renewal</strong>
    <p style="margin-top:6px;">All HubSpot Professional and Enterprise agreements are annual commitments that auto-renew by default, even when paid in monthly installments. On day 1 of the auto-renewal window, you are liable for the full 12-month renewal balance unless you submitted non-renewal notice in advance.</p>
    <cite>Sources: <a href="https://legal.hubspot.com/terms-of-service" target="_blank" rel="noopener">HubSpot Customer Terms of Service (Renewal &amp; Subscription Term)</a> &amp; <a href="https://www.reddit.com/r/sales/comments/pyqpjq/hubspot_a_psa_contracts_and_review/" target="_blank" rel="noopener">r/sales contract review</a></cite>
  </div>
  <div class="evidence-box">
    <strong>2. Onboarding fees are mandatory on direct orders (waivable via Solutions Partners)</strong>
    <p style="margin-top:6px;">Sales Hub Pro requires a $1,500 onboarding fee ($3,500 on Enterprise), while Marketing Hub Pro requires $3,000 ($7,000 on Enterprise). HubSpot waives its direct onboarding fee when you purchase through an accredited HubSpot Solutions Partner with a signed implementation scope.</p>
    <cite>Sources: <a href="https://www.hubspot.com/pricing/sales" target="_blank" rel="noopener">HubSpot Sales Hub Pricing Schedule</a> &amp; <a href="https://www.reddit.com/r/sales/comments/1htoulv/onboarding_fee/" target="_blank" rel="noopener">r/sales &ndash; "Onboarding Fee"</a></cite>
  </div>
  <div class="evidence-box">
    <strong>3. You cannot downgrade committed seats mid-term</strong>
    <p style="margin-top:6px;">Under HubSpot’s Customer Terms of Service, seat upgrades take effect immediately and prorate for the remainder of the subscription term, whereas seat reductions or edition downgrades are only permitted at the end of the 12-month commitment window.</p>
    <cite>Source: <a href="https://legal.hubspot.com/terms-of-service" target="_blank" rel="noopener">HubSpot Customer Terms of Service &ndash; No Early Cancellation or Downgrades</a></cite>
  </div>
</section>

<script>
function updateHs() {
  const seats = parseInt(document.getElementById('hs-seats').value, 10);
  const tier = document.getElementById('hs-tier').value;
  document.getElementById('hs-seats-val').textContent = seats;

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

  const hsSeatsYr = hsMonthly * 12;
  const hsYear1 = hsSeatsYr + hsOnboard;
  const pipeYr = seats * 39 * 12;
  const freshYr = seats * 39 * 12;
  const closeStartupYr = seats * 47 * 12;
  const closeGrowthYr = seats * 99 * 12;
  const closeEssentialsYr = seats * 35 * 12;

  const maxVal = Math.max(hsYear1, closeGrowthYr, 1);
  const ratio = (hsYear1 / Math.max(closeStartupYr, 1)).toFixed(1);
  const repWord = seats === 1 ? '1 sales rep' : `${seats} sales reps`;
  const seatWord = seats === 1 ? '1 seat' : `${seats} seats`;

  document.getElementById('chart-dynamic-headline').textContent =
    `At ${seatWord}, ${hsShortName} ($${hsYear1.toLocaleString()}) costs ${ratio}x Close Startup ($${closeStartupYr.toLocaleString()}) in Year 1`;
  document.getElementById('chart-dynamic-subtitle').textContent =
    `Year-1 total contract cost for ${repWord} on annual billing with multi-pipeline automation and sales sequences (licenses + mandatory onboarding).`;

  document.getElementById('bar-pipedrive').style.width = `${((pipeYr / maxVal) * 100).toFixed(1)}%`;
  document.getElementById('val-pipedrive').textContent = `$${pipeYr.toLocaleString()}`;

  document.getElementById('bar-freshsales').style.width = `${((freshYr / maxVal) * 100).toFixed(1)}%`;
  document.getElementById('val-freshsales').textContent = `$${freshYr.toLocaleString()}`;

  document.getElementById('bar-close-startup').style.width = `${((closeStartupYr / maxVal) * 100).toFixed(1)}%`;
  document.getElementById('val-close-startup').textContent = `$${closeStartupYr.toLocaleString()}`;

  document.getElementById('bar-close-growth').style.width = `${((closeGrowthYr / maxVal) * 100).toFixed(1)}%`;
  document.getElementById('val-close-growth').textContent = `$${closeGrowthYr.toLocaleString()}`;

  document.getElementById('label-hs-name').textContent = hsFullName;
  document.getElementById('meta-hs-breakdown').textContent = `$${hsSeatsYr.toLocaleString()} seats + $${hsOnboard.toLocaleString()} onboarding`;
  document.getElementById('bar-hs-total').style.width = `${((hsYear1 / maxVal) * 100).toFixed(1)}%`;

  const seatSegPct = ((hsSeatsYr / hsYear1) * 100).toFixed(2);
  const onbSegPct = (100 - parseFloat(seatSegPct)).toFixed(2);
  const segSeatsEl = document.getElementById('bar-hs-seats');
  const segOnbEl = document.getElementById('bar-hs-onb');
  if (segSeatsEl && segOnbEl) {
    segSeatsEl.style.width = `${seatSegPct}%`;
    segSeatsEl.setAttribute('title', `$${hsSeatsYr.toLocaleString()} annual seats`);
    segOnbEl.style.width = `${onbSegPct}%`;
    segOnbEl.setAttribute('title', `+$${hsOnboard.toLocaleString()} mandatory onboarding`);
  }

  document.getElementById('val-hs-total').textContent = `$${hsYear1.toLocaleString()}`;
  document.getElementById('sub-hs-onb').textContent = `+$${hsOnboard.toLocaleString()} onboarding`;

  const hsCloseCta = document.getElementById('hs-close-cta');
  if (hsCloseCta) {
    const savedVsHs = Math.max(0, hsYear1 - closeStartupYr);
    hsCloseCta.textContent = savedVsHs > 0
      ? `Save $${savedVsHs.toLocaleString()}/yr with Close CRM ($0 Onboarding) →`
      : 'Compare Close CRM ($0 Onboarding) →';
  }
  const hsCalcBody = document.getElementById('hs-calc-body');
  if (hsCalcBody) {
    hsCalcBody.innerHTML = `
      <div class="calc-math-list">
        <div class="calc-math-row">
          <span class="calc-math-label"><strong>${hsFullName} Licenses</strong><span class="calc-math-formula">$${hsMonthly.toLocaleString()}/mo × 12 mos (${seatWord})</span></span>
          <span class="calc-math-val">$${hsSeatsYr.toLocaleString()}</span>
        </div>
        <div class="calc-math-row">
          <span class="calc-math-label"><strong>Mandatory HubSpot Onboarding</strong><span class="calc-math-formula">One-time direct implementation fee</span></span>
          <span class="calc-math-val">+$${hsOnboard.toLocaleString()}</span>
        </div>
        <div class="calc-math-total">
          <span>${hsShortName} Year-1 Total</span>
          <span>$${hsYear1.toLocaleString()} / yr</span>
        </div>
        <div class="calc-math-row" style="margin-top:6px;">
          <span class="calc-math-label"><strong>Close CRM Startup Comparison</strong><span class="calc-math-formula">${seats} × $47/seat/mo × 12 mos + $0 onboarding</span></span>
          <span class="calc-math-val">$${closeStartupYr.toLocaleString()} / yr</span>
        </div>
      </div>
    `;
  }
  const footEl = document.getElementById('chart-dynamic-footnote');
  if (footEl) {
    footEl.innerHTML = `<strong>Hidden Cost Highlight:</strong> Based on ${seatWord}, annual billing. Official prices verified Oct 2026. All tiers compared include multi-stage pipelines and automated sales sequences for ${seatWord} billed annually (Close CRM (Essentials) is $${closeEssentialsYr.toLocaleString()}/yr at $35/user/mo for basic pipelines without sequences). ${hsShortName} requires a one-time $${hsOnboard.toLocaleString()} onboarding fee in Year 1; Year-2 renewal drops to $${hsSeatsYr.toLocaleString()}/yr. Source: saasbill.io`;
  }
  if (typeof window.trackSaaSBillEvent === 'function') {
    window.trackSaaSBillEvent('result_rendered', { page: 'hubspot-true-cost', seats: seats, tier: tier });
  }
}
document.getElementById('hs-seats').addEventListener('input', updateHs);
document.getElementById('hs-tier').addEventListener('input', updateHs);
updateHs();
</script>
"""

p1_faqs = [
    ("How much is the mandatory HubSpot onboarding fee in 2026?", "In 2026, HubSpot charges a mandatory one-time onboarding fee of $1,500 for Sales Hub Professional, $3,500 for Sales Hub Enterprise, $3,000 for Marketing Hub Professional, and $7,000 for Marketing Hub Enterprise when purchasing directly."),
    ("Can you cancel a HubSpot monthly payment plan at any time?", "On HubSpot Starter, yes. However, on HubSpot Professional and Enterprise tiers, selecting 'monthly billing' ($100/seat/mo instead of $90/seat/mo on Sales Pro) is still a binding 12-month annual contract paid in monthly installments, with automatic annual renewal unless cancelled prior to the notice deadline."),
    ("How do you waive the HubSpot $1,500 or $3,000 onboarding fee?", "You can waive HubSpot's direct onboarding fee by purchasing your license through an accredited HubSpot Solutions Partner (agency/consultant) and signing an onboarding scope with them, or by switching to a zero-onboarding CRM such as Close CRM or Pipedrive."),
    ("How much does HubSpot Sales Hub Professional cost for 5 users in Year 1?", "For 5 core sales seats billed annually at $90/seat/month ($450/month or $5,400/year) plus the mandatory $1,500 onboarding fee, HubSpot Sales Hub Professional costs $6,900 in Year 1 (excluding taxes and calling credit overages).")
]

render_page(
    "pricing/hubspot-true-cost-and-onboarding-fees/index.html",
    "HubSpot True Year-1 Cost & Onboarding Fees – saasbill.io",
    "Calculate the 2026 HubSpot true cost and Year-1 invoice including mandatory $1,500-$7,000 onboarding fees on Sales Hub Pro and Marketing Hub Pro vs. Close CRM ($0 onboarding) and Pipedrive.",
    "/pricing/hubspot-true-cost-and-onboarding-fees/",
    p1_body,
    faqs=p1_faqs
)

# ---------------------------------------------------------
# 3. Page 2: Intercom Fin AI Resolution Calculator
# ---------------------------------------------------------
p2_body = """
<section class="hero">
  <h1>What Intercom’s $0.99 AI resolution fee actually does to your support bill.</h1>
  <p class="lead">Seat licenses start at $29 to $132 a month, but Fin AI adds $0.99 every time it resolves a ticket. Here is how fast the variable meter outgrows your seat bill, and how session-pack helpdesks compare.</p>
  <div class="geo-direct-answer">
    <p><strong>The short version:</strong> Intercom charges <strong>$0.99 per Fin AI resolution</strong> (including automated resolutions, procedure handoffs, and disqualifications, plus <strong>$9.99 per sales qualification</strong>) on top of agent seat licenses (<strong>$29/mo Essential, $85/mo Advanced, $132/mo Expert</strong> billed annually; $39/$99/$139 monthly). For a 5-agent team on Advanced ($425/mo) handling 3,000 tickets/month with a 50% AI resolution rate (1,500 resolutions), Fin AI adds <strong>$1,485/mo</strong>, bringing the total bill to <strong>$1,910/mo ($22,920/yr)</strong>. By comparison, <strong>Freshdesk Pro ($55/agent/mo annual)</strong> includes <strong>500 one-time Freddy AI Agent sessions</strong> and then bills <strong>$49 per 100-session pack</strong> (charged per AI session handled, whether resolved or not; Freddy AI Copilot is an optional $29/agent/mo add-on).</p>
  </div>
</section>

<section class="calc-box">
  <h2 style="margin-top:0;">Calculate your monthly Intercom + Fin AI invoice</h2>
  <p style="color:var(--muted); margin-bottom:20px; font-size:0.95rem;">Every 1,000 tickets resolved by Fin AI adds $990/month ($11,880/year) on top of your agent seat subscriptions. Drag the sliders to compare Intercom’s $0.99/resolution meter against Freshdesk Pro + Freddy AI Agent session packs ($49 per 100 sessions after 500 one-time free sessions).</p>
  <div class="calc-grid">
    <div class="control-group">
      <label for="ic-seats">Support agents (full seats): <span class="val-pill" id="ic-seats-val">5</span> seats</label>
      <input type="range" id="ic-seats" min="1" max="40" value="5" />
    </div>
    <div class="control-group">
      <label for="ic-plan">Intercom plan tier (annual billing)</label>
      <select id="ic-plan">
        <option value="29">Essential ($29/seat annual &middot; $39 monthly)</option>
        <option value="85" selected>Advanced ($85/seat annual &middot; 20 Lite seats)</option>
        <option value="132">Expert ($132/seat annual &middot; 50 Lite seats)</option>
      </select>
    </div>
    <div class="control-group">
      <label for="ic-tickets">Total monthly support conversations: <span class="val-pill" id="ic-tickets-val">3,000</span> /mo</label>
      <input type="range" id="ic-tickets" min="200" max="20000" step="200" value="3000" />
    </div>
    <div class="control-group">
      <label for="ic-rate">Fin AI resolution rate: <span class="val-pill" id="ic-rate-val">50</span>%</label>
      <input type="range" id="ic-rate" min="10" max="85" step="5" value="50" />
    </div>
  </div>
  <div id="ic-summary" class="summary-strip" aria-live="polite"></div>
  <p class="summary-interpretation"><strong>How to read this comparison:</strong> Intercom charges $0.99 only when Fin AI resolves a conversation, whereas Freshdesk charges $49 per 100 AI sessions (whether resolved or escalated). Compare both models against your resolution rate.</p>
  <div class="table-wrap mobile-cards">
    <table>
      <caption>Intercom + Fin AI ($0.99/Resolution) vs. Freshdesk Pro + Freddy AI Agent ($49/100 Sessions) Breakdown (USD, verified Oct 25, 2026)</caption>
      <thead>
        <tr>
          <th>Helpdesk Solution</th>
          <th>Monthly Agent Seats</th>
          <th>Monthly AI Usage Charge</th>
          <th>Total Monthly Bill</th>
          <th>Year-1 Total (USD)</th>
          <th>Compare</th>
        </tr>
      </thead>
      <tbody id="ic-tbody"></tbody>
    </table>
  </div>
</section>

<section>
  <h2>Why support teams call $0.99/resolution an "AI tax"</h2>
  <p class="section-tldr">When outcome-based AI meters have no hard cap by default, seasonal support spikes or better help-center articles immediately increase your monthly software invoice.</p>
  <div class="evidence-box">
    <strong>1. Billable resolution definition includes silent exits after Fin replies</strong>
    <p style="margin-top:6px;">Under Intercom’s Fin AI pricing rules, a billable $0.99 resolution is counted whenever a customer confirms Fin’s answer helped OR leaves the conversation without requesting a human agent after Fin’s response, at most once per conversation.</p>
    <cite>Source: <a href="https://www.intercom.com/pricing" target="_blank" rel="noopener">Intercom Official Pricing &amp; Fin AI Agent Billing FAQ</a></cite>
  </div>
  <div class="evidence-box">
    <strong>2. Session-pack pricing vs. per-resolution pricing</strong>
    <p style="margin-top:6px;">Freshdesk’s Freddy AI Agent includes 500 complimentary one-time sessions and then charges $49 per 100-session pack (spanning 72 hours for email or 24 hours for chat), giving admins fixed session-pack budgets that expire at cycle end unless auto-recharge is enabled.</p>
    <cite>Source: <a href="https://support.freshdesk.com/support/solutions/articles/50000011515-manage-freddy-ai-add-ons" target="_blank" rel="noopener">Freshdesk Support &ndash; Purchase and Manage Freddy AI Add-ons</a></cite>
  </div>
</section>

<script>
function updateIcCalc() {
  const seats = parseInt(document.getElementById('ic-seats').value, 10);
  const seatRate = parseInt(document.getElementById('ic-plan').value, 10);
  const tickets = parseInt(document.getElementById('ic-tickets').value, 10);
  const resRate = parseInt(document.getElementById('ic-rate').value, 10) / 100;
  document.getElementById('ic-seats-val').textContent = seats;
  document.getElementById('ic-tickets-val').textContent = tickets.toLocaleString();
  document.getElementById('ic-rate-val').textContent = Math.round(resRate * 100);
  const resolvedTickets = Math.round(tickets * resRate);
  const icSeatCost = seats * seatRate;
  const icAiCost = Math.round(resolvedTickets * 0.99);
  const icTotalMo = icSeatCost + icAiCost;
  const icYear = icTotalMo * 12;

  // Freshdesk Pro ($55/seat/mo annual) + Freddy AI Agent session packs ($49 per 100 sessions; 500 1x free in Year 1)
  const fdSeatCost = seats * 55;
  const fdMonthlyPacks = Math.ceil(tickets / 100);
  const fdAiCostMo = fdMonthlyPacks * 49;
  const fdTotalMo = fdSeatCost + fdAiCostMo;
  const fdAnnualBillableSessions = Math.max(0, tickets * 12 - 500);
  const fdAnnualAiCost = Math.ceil(fdAnnualBillableSessions / 100) * 49;
  const fdYear = fdSeatCost * 12 + fdAnnualAiCost;
  const diff = icYear - fdYear;
  const diffLabel = diff > 0 ? `(saves $${diff.toLocaleString()}/yr)` : `(+$${Math.abs(diff).toLocaleString()}/yr vs Intercom)`;

  const icSeatsYr = icSeatCost * 12;
  const icAiYr = icAiCost * 12;
  const fdSeatsYr = fdSeatCost * 12;
  const aiSharePct = icYear > 0 ? Math.round((icAiYr / icYear) * 100) : 0;
  const scenarioLine = `Based on ${seats} seat${seats === 1 ? '' : 's'}, annual billing, ${tickets.toLocaleString()} tickets/mo (${Math.round(resRate * 100)}% AI resolution = ${resolvedTickets.toLocaleString()} resolutions/mo)`;

  const icSummary = document.getElementById('ic-summary');
  if (icSummary) {
    icSummary.innerHTML = `
      <div class="summary-card card-hidden">
        <div class="summary-label">Intercom Year-1 Total</div>
        <div class="summary-metric" style="color:var(--rose);">$${icYear.toLocaleString()} / yr ($${icTotalMo.toLocaleString()}/mo)</div>
        <div class="summary-scenario">${scenarioLine}</div>
        <div class="summary-breakdown">$${icSeatsYr.toLocaleString()} licenses + $0 onboarding + $${icAiYr.toLocaleString()} Fin AI</div>
        <div class="summary-caveat"><strong>Hidden Cost Highlight:</strong> Metered Fin AI resolution fees ($0.99 &times; ${resolvedTickets.toLocaleString()}/mo) add $${icAiYr.toLocaleString()}/yr (${aiSharePct}% of your total Year-1 bill).</div>
        <div class="summary-actions">
          <div class="cta-stack">
            <a class="btn-secondary" href="https://www.intercom.com/pricing" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="intercom-fin-ai" data-cta-location="summary-card">Check Intercom pricing &rarr;</a>
          </div>
        </div>
      </div>
      <div class="summary-card card-lowest">
        <div class="summary-label">Freshdesk Session-Pack Plan</div>
        <div class="summary-metric" style="color:var(--emerald);">$${fdYear.toLocaleString()} / yr ${diffLabel}</div>
        <div class="summary-scenario">${scenarioLine}</div>
        <div class="summary-breakdown">$${fdSeatsYr.toLocaleString()} licenses + $0 onboarding + $${fdAnnualAiCost.toLocaleString()} AI session packs</div>
        <div class="summary-caveat"><strong>Contract note:</strong> Includes 500 one-time free sessions, then $49 per 100 sessions (billed per session handled, resolved or not).</div>
        <div class="summary-actions">
          <div class="cta-stack">
            <a class="btn-cta" href="https://www.freshworks.com/freshdesk/pricing/" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="freshdesk-support" data-cta-location="summary-card">View Freshdesk plans &rarr;</a>
          </div>
          <a class="summary-audit-link" href="../zendesk-ai-resolution-and-automated-outcome-cost/" data-track="internal-audit">Compare Zendesk AI ($1.50&ndash;$2.00) &rarr;</a>
        </div>
      </div>
    `;
  }

  document.getElementById('ic-tbody').innerHTML = `
    <tr>
      <td data-label="Helpdesk Solution">
        <strong>Intercom + Fin AI (${resolvedTickets.toLocaleString()} resolutions/mo)</strong>
        <span class="status-pill status-verified">Verified</span>
        <div class="source-inline">Source: <a href="https://www.intercom.com/pricing" target="_blank" rel="noopener">Intercom pricing &nearr;</a></div>
      </td>
      <td data-label="Monthly Agent Seats" style="font-family:var(--sans); font-variant-numeric:tabular-nums;">$${icSeatCost.toLocaleString()} / mo</td>
      <td data-label="Monthly AI Usage"><span class="badge badge-high">$${icAiCost.toLocaleString()} / mo ($0.99 &times; ${resolvedTickets.toLocaleString()})</span></td>
      <td data-label="Total Monthly Bill" class="price-highlight">$${icTotalMo.toLocaleString()} / mo</td>
      <td data-label="Year-1 Total" class="price-highlight">$${icYear.toLocaleString()} / yr<div class="cell-scenario">${scenarioLine}</div></td>
      <td data-label="Next Step"><div class="cta-stack"><a class="btn-secondary" href="https://www.intercom.com/pricing" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="intercom-fin-ai" data-cta-location="table-row">Check Intercom pricing &rarr;</a></div></td>
    </tr>
    <tr>
      <td data-label="Helpdesk Solution">
        <strong>Freshdesk Pro + Freddy AI Agent (Freshworks)</strong>
        <span class="status-pill status-verified">Verified</span>
        <div style="font-size:0.78rem; color:var(--emerald);">$55/agent/mo + $49/100 AI sessions (500 one-time free sessions deducted in Yr 1; optional Copilot $29/agent/mo)</div>
        <div class="source-inline">Verified source: <a href="https://www.freshworks.com/freshdesk/pricing/" target="_blank" rel="noopener">Freshdesk pricing &nearr;</a></div>
      </td>
      <td data-label="Monthly Agent Seats" style="font-family:var(--sans); font-variant-numeric:tabular-nums;">$${fdSeatCost.toLocaleString()} / mo</td>
      <td data-label="Monthly AI Usage"><span class="badge badge-low">$${fdAiCostMo.toLocaleString()} / mo (${fdMonthlyPacks} &times; $49 session packs)</span></td>
      <td data-label="Total Monthly Bill" class="price-highlight" style="color:var(--emerald);">$${fdTotalMo.toLocaleString()} / mo</td>
      <td data-label="Year-1 Total" class="price-highlight" style="color:var(--emerald);">$${fdYear.toLocaleString()} / yr ${diffLabel}<div class="cell-scenario">${scenarioLine}</div></td>
      <td data-label="Next Step"><div class="cta-stack"><a class="btn-secondary" href="https://www.freshworks.com/freshdesk/pricing/" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="freshdesk-support" data-cta-location="table-row">View Freshdesk plans &rarr;</a></div></td>
    </tr>
  `;
  if (typeof window.trackSaaSBillEvent === 'function') {
    window.trackSaaSBillEvent('result_rendered', { page: 'intercom-fin-ai', seats: seats, tickets: tickets });
  }
}
['ic-seats', 'ic-plan', 'ic-tickets', 'ic-rate'].forEach(id => document.getElementById(id).addEventListener('input', updateIcCalc));
updateIcCalc();
</script>
"""

p2_faqs = [
    ("How much does Intercom Fin AI charge per resolution in 2026?", "Intercom charges $0.99 per Fin AI outcome/resolution (and $9.99 per sales qualification outcome), billed at most once per conversation, on top of your monthly per-seat plan ($29 Essential, $85 Advanced, or $132 Expert billed annually)."),
    ("What counts as a billable Fin AI resolution in Intercom?", "A billable $0.99 Fin outcome occurs when the customer confirms their question was answered, exits the conversation without requesting a human agent after Fin's answer, or triggers a configured procedure handoff/disqualification outcome."),
    ("How does Freshdesk Freddy AI pricing compare to Intercom's $0.99 per-resolution meter?", "Freshdesk (by Freshworks) charges $19 (Growth), $55 (Pro), or $89 (Enterprise) per agent/month billed annually ($23/$66/$107 monthly). For autonomous AI support, Freddy AI Agent includes 500 one-time complimentary sessions per account and then bills $49 per 100-session pack (charged per session, resolved or not), while Freddy AI Copilot for human agents is an optional $29/agent/month add-on.")
]

render_page(
    "pricing/intercom-fin-ai-resolution-cost-calculator/index.html",
    "Intercom Fin AI True Cost & Year-1 Calculator – saasbill.io",
    "Calculate your 2026 Intercom Fin AI true cost and Year-1 support bill at $0.99 per AI resolution plus seat licenses ($29-$132/mo), and compare AI cost against Freshdesk and Help Scout.",
    "/pricing/intercom-fin-ai-resolution-cost-calculator/",
    p2_body,
    faqs=p2_faqs
)
