"""
Builds the dedicated high-intent Intercom Fin Cost Calculator page at:
1. /intercom-fin-cost-calculator/index.html (canonical: https://saasbill.io/intercom-fin-cost-calculator/)
2. /pricing/intercom-fin-ai-resolution-cost-calculator/index.html (canonical: https://saasbill.io/pricing/intercom-fin-ai-resolution-cost-calculator/)

Uses the exact same TOOLS, AFFILIATES, and calcToolYear1(t, seats, aiVol, mode) engine as the homepage
with zero new calculation logic, prefilled for a realistic 10-agent, 1,500 AI conversations/month scenario.
"""
import json
from layout import load_data, render_page, SITE_ORIGIN, wrap_calculator_shell

TOOLS, AFFILIATES = load_data()
tools_js = json.dumps(TOOLS)
aff_js = json.dumps(AFFILIATES)


def render_intercom_calculator_body(
    prefix="../",
    h1="Intercom Fin AI Cost Calculator (2026): True Year-1 Price at $0.99 per Resolution",
    lead="See what Intercom Fin actually costs for your team. Adjust the agents and AI volume below to see your real Year-1 total and how it compares to Freshdesk and Zendesk.",
    compare_mode="intercom_fin",
    page_id="intercom-fin-cost-calculator",
    spotlight_id="intercom-fin-ai",
    legacy_summary_id="ic-summary",
    editorial_html=None,
    calc_heading="Interactive Intercom Fin AI Year-1 True-Cost Calculator (2026)",
    gap_sub="Visual Year-1 cost comparison graph &amp; full contract table (Intercom Fin vs. Freshdesk, Zendesk, Help Scout &amp; HubSpot)",
    static_product="Intercom + Fin AI Agent",
    static_total="$21,300",
    static_subnote="+$17,820 (+512%) above advertised price.",
    static_best_html=None,
    static_base="$348",
    static_seats="$3,132",
    static_hidden="$17,820",
    static_hidden_sub="Fin AI $0.99/resolution meter",
):
    if static_best_html is None:
        static_best_html = '<strong>Best option:</strong> <a href="https://www.freshworks.com/freshdesk/pricing/" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="freshdesk-support" data-cta-location="workbench-best-option">Freshdesk (Freshworks) ($10,855/yr)</a> &middot; saves $10,445/yr'
    if editorial_html is None:
        editorial_html = """
<section class="editorial-below-section">
  <h2>Why Intercom&rsquo;s $0.99 Fin AI meter outgrows base seat licenses</h2>
  <div class="methodology-grid fine-print-grid">
    <div class="methodology-item">
      <strong>1. Silent Exits Count as Billable $0.99 Resolutions</strong>
      Under Intercom&rsquo;s Fin AI billing terms, a $0.99 resolution is billed whenever a customer confirms Fin&rsquo;s answer helped or closes the chat without requesting a human agent after Fin replies (at most once per conversation).
    </div>
    <div class="methodology-item">
      <strong>2. Session Packs vs. Per-Resolution Meters</strong>
      Freshdesk includes 500 complimentary one-time Freddy AI Agent sessions and then bills $49 per 100-session pack ($0.49/session), while Help Scout bills $0.75 per resolved answer with an optional hard monthly spending cap.
    </div>
    <div class="methodology-item">
      <strong>3. Zendesk AI Allowance vs. $1.50&ndash;$2.00 Overage</strong>
      Zendesk Suite Team ($55/seat/mo annual) includes only 5 automated resolutions per agent per month (50/mo for 10 agents) before billing $1.50 committed or $2.00 pay-as-you-go per resolution.
    </div>
  </div>
</section>
"""
    spotlight_js = "'" + spotlight_id.replace("'", "") + "'"
    if compare_mode.startswith("zendesk"):
        audit_links_js = f"""{{
  'intercom-fin-ai': {{ url: '{prefix}intercom-fin-cost-calculator/', label: 'Open Intercom Fin calculator →' }},
  'freshdesk-support': {{ url: '{prefix}zendesk-vs-freshdesk-cost-comparison/', label: 'Compare Zendesk vs. Freshdesk →' }},
  'zendesk-suite-team': {{ url: '{prefix}zendesk-ai-cost-calculator/', label: 'Open Zendesk AI calculator →' }},
  'zendesk-suite-professional': {{ url: '{prefix}zendesk-ai-cost-calculator/', label: 'Open Zendesk AI calculator →' }},
  'help-scout-plus': {{ url: '{prefix}zendesk-vs-freshdesk-cost-comparison/', label: 'Compare vs. Freshdesk →' }},
  'hubspot-service-hub': {{ url: '{prefix}hubspot-onboarding-fee-calculator/', label: 'Open HubSpot onboarding calculator →' }}
}}"""
    else:
        audit_links_js = f"""{{
  'intercom-fin-ai': {{ url: '{prefix}intercom-fin-cost-calculator/', label: 'Open Intercom Fin calculator →' }},
  'freshdesk-support': {{ url: '{prefix}intercom-vs-freshdesk-cost-comparison/', label: 'Compare Intercom vs. Freshdesk →' }},
  'zendesk-suite-team': {{ url: '{prefix}intercom-vs-zendesk-cost-comparison/', label: 'Compare Intercom vs. Zendesk →' }},
  'zendesk-suite-professional': {{ url: '{prefix}pricing/zendesk-ai-resolution-and-automated-outcome-cost/', label: 'Read Zendesk AI overage audit →' }},
  'help-scout-plus': {{ url: '{prefix}pricing/zendesk-ai-resolution-and-automated-outcome-cost/', label: 'Compare vs. Zendesk AI →' }},
  'hubspot-service-hub': {{ url: '{prefix}pricing/hubspot-true-cost-and-onboarding-fees/', label: 'Read HubSpot onboarding audit →' }}
}}"""
    html = f"""
<section class="hero">
  <h1>{h1}</h1>
  <p class="lead">{lead}</p>
</section>

<div class="unified-inspector-tray" id="unified-inspector-tray">
  <svg class="inspector-left-rail" id="inspector-left-rail" aria-hidden="true" overflow="visible">
    <path id="rail-svg-path" fill="none" stroke="#536B56" stroke-width="2.25" stroke-linecap="round" stroke-linejoin="round" d="" />
    <circle id="rail-svg-dot" cx="22" cy="180" r="4" fill="#536B56" />
    <polygon id="rail-svg-arrow" points="16,415 23,420 16,425" fill="#536B56" />
  </svg>
<section class="calc-box editorial-workbench" aria-labelledby="calc-heading">
  <h2 id="calc-heading" class="sr-only-control">{calc_heading}</h2>
  <div class="control-group sr-only-control">
    <label for="cat-filter">Software category</label>
    <select id="cat-filter" data-track="calculator-control" data-control="category">
      <option value="Helpdesk & AI Support" selected>Helpdesk &amp; AI Support (6 tools)</option>
    </select>
  </div>

  <div class="workbench-grid">
    <!-- Left Column: ESTIMATE YOUR TRUE COST (Prefilled: Intercom + Fin AI, 10 Agents, 1,500 AI Resolutions/mo, Annual) -->
    <div class="wb-col-controls">
      <div class="wb-col-title">Estimate Your True Cost</div>
      <div class="wb-controls-stack">
        <div class="wb-control-item" id="tool-select-group">
          <label class="wb-control-label" for="spotlight-tool-select">Platform to inspect</label>
          <select id="spotlight-tool-select" class="wb-tool-select" data-track="calculator-control" data-control="spotlight-tool"></select>
        </div>

        <div class="wb-control-item" id="seat-control-group">
          <span class="wb-control-label">Support agents / seats</span>
          <div class="wb-slider-row">
            <input type="range" id="seat-slider" min="1" max="50" value="10" aria-label="Support agents / seats" data-track="calculator-control" data-control="seats" />
            <span class="wb-slider-val" id="seat-val">10</span>
          </div>
        </div>

        <div class="wb-control-item" id="ai-control-group">
          <span class="wb-control-label">AI-resolved tickets / month</span>
          <div class="wb-slider-row">
            <input type="range" id="ai-slider" min="0" max="5000" step="100" value="1500" aria-label="AI-resolved tickets per month" data-track="calculator-control" data-control="ai-tickets" />
            <span class="wb-slider-val" id="ai-val">1,500</span>
          </div>
        </div>

        <div class="wb-quiet-options" id="billing-control-group">
          <div class="wb-quiet-field">
            <label for="billing-mode">Billing:</label>
            <select id="billing-mode" data-track="calculator-control" data-control="billing-mode">
              <option value="annual" selected>Annual</option>
              <option value="monthly">Monthly</option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <!-- Center Column: YOUR ESTIMATED TRUE COST (3-Row Vertical Stacked Bar + Leader Lines) -->
    <div class="wb-col-chart">
      <div class="wb-col-title" id="wb-chart-col-title">Your Estimated True Cost</div>
      <div id="wb-vbar-mount" class="wb-vbar-container" aria-live="polite">
        <div class="wb-vbar-row" id="wb-row-base" style="flex: 15.5 1 0px;">
          <div class="wb-vbar-block block-base">
            <span class="wb-block-amount" id="wb-amt-base">{static_base}</span>
          </div>
          <div class="wb-callout-item">
            <div class="wb-leader-line"></div>
            <div class="wb-callout-text">
              <strong id="wb-call-title-base">Sticker Price: Base plan</strong>
              <span id="wb-call-sub-base">1st seat at advertised rate</span>
            </div>
          </div>
        </div>

        <div class="wb-vbar-row" id="wb-row-seats" style="flex: 15.5 1 0px;">
          <div class="wb-vbar-block block-seats">
            <span class="wb-block-amount" id="wb-amt-seats">{static_seats}</span>
          </div>
          <div class="wb-callout-item">
            <div class="wb-leader-line"></div>
            <div class="wb-callout-text">
              <strong id="wb-call-title-seats">Sticker Price: Added seats</strong>
              <span id="wb-call-sub-seats">Remaining team seat licenses</span>
            </div>
          </div>
        </div>

        <div class="wb-vbar-row" id="wb-row-hidden" style="flex: 69.0 1 0px;">
          <div class="wb-vbar-block block-hidden">
            <span class="wb-block-amount" id="wb-amt-hidden">{static_hidden}</span>
          </div>
          <div class="wb-callout-item">
            <div class="wb-leader-line"></div>
            <div class="wb-callout-text">
              <strong id="wb-call-title-hidden">Hidden Cost Gap</strong>
              <span id="wb-call-sub-hidden">{static_hidden_sub}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Right Column: Progressive Disclosure (1. Result & Best Option -> 2. Why + Expandable Calculation -> 3. Contextual Primary CTA) -->
    <div class="wb-result-col" id="wb-result-mount" aria-live="polite">
      <div class="wb-selected-product" id="wb-selected-product">{static_product}</div>
      <div class="wb-big-total" id="wb-big-total-wrap"><span id="wb-big-amount">{static_total}</span> <span class="wb-per-year" id="wb-big-unit">/ year</span></div>
      <details class="math-drawer" id="wb-calc-details">
        <summary id="wb-calc-summary">Show calculation</summary>
        <div class="math-drawer-body" id="wb-calc-body"></div>
      </details>
      <p class="wb-budget-quote" id="wb-budget-quote">True Year-1 cost</p>
      <p class="wb-budget-subnote" id="wb-budget-subnote">{static_subnote}</p>
      <div class="wb-best-option" id="wb-best-option">{static_best_html}</div>
      <div class="cta-stack">
        <a id="wb-primary-cta" class="btn-cta wb-primary-cta" href="https://www.intercom.com/pricing" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="intercom-fin-ai" data-cta-location="workbench">View Intercom pricing &rarr;</a>
      </div>
    </div>
  </div>
</section>

<!-- STEP 2: CATEGORY VERDICT CARDS (Best Option Freshdesk, Intercom Fin AI Breakdown, Zendesk AI Comparison) -->
<section class="verdict-section" id="verdict-card" aria-label="Helpdesk &amp; AI Support Verdict &amp; Comparison">
  <div id="calc-summary-strip" class="summary-strip" aria-live="polite"></div>
  <div id="{legacy_summary_id}" style="display:none;" aria-hidden="true"></div>
</section>

<!-- STEP 3 & 4: COMPARE ALL TOOLS (Visual Comparison Graph + Full Contract & Renewal Table behind Progressive Disclosure) -->
<section class="hidden-gap-section" aria-labelledby="gap-heading">
  <details class="full-table-disclosure" id="full-table-details">
    <summary class="full-table-summary" id="full-table-summary">
      <div class="full-table-summary-text">
        <h2 id="gap-heading" class="full-table-heading">Compare all tools in this category</h2>
        <span class="full-table-summary-sub">{gap_sub}</span>
      </div>
      <span class="full-table-toggle-pill" id="full-table-toggle-pill">Compare all tools &darr;</span>
    </summary>
    <div class="full-table-body">
      <div class="gap-toolbar">
        <p class="gap-subhead" id="gap-dynamic-subhead">All 6 tools compared for 10 seats &middot; annual billing &middot; 1,500 AI tickets/mo &middot; click any row to inspect its breakdown above.</p>
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
          <caption>2026 Helpdesk &amp; AI Support Year-1 True-Cost Comparison (USD, verified Oct 25, 2026)</caption>
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
    </div>
  </details>
  <p class="calc-affiliate-disclosure">Independent calculations. Some vendor links are affiliate links. This never changes our rankings or calculations.</p>
</section>
</div>

{editorial_html}

<script>
const TOOLS = {tools_js};
const AFFILIATES = {aff_js};
const COMPARE_MODE = {json.dumps(compare_mode)};
const PAGE_ID = {json.dumps(page_id)};

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
  'intercom-fin-ai': 'View Intercom pricing →',
  'freshdesk-support': 'View Freshdesk pricing →',
  'zendesk-suite-team': 'View Zendesk pricing →',
  'zendesk-suite-professional': 'View Zendesk pricing →',
  'help-scout-plus': 'View Help Scout pricing →',
  'hubspot-service-hub': 'View HubSpot pricing →'
}};

const INTERNAL_AUDIT_LINKS = {audit_links_js};

const SHORT_VENDOR_NAMES = {{
  'intercom-fin-ai': 'Intercom',
  'freshdesk-support': 'Freshdesk',
  'zendesk-suite-team': 'Zendesk',
  'zendesk-suite-professional': 'Zendesk',
  'help-scout-plus': 'Help Scout',
  'hubspot-service-hub': 'HubSpot'
}};

function getVendorCtaLabel(tool) {{
  return VENDOR_CTA_LABELS[tool.id] || `View ${{tool.vendor || tool.name}} pricing →`;
}}

function getContextualCtaLabel(tool, rowTotal, refTotal, isTrapOrHighest) {{
  const shortVendor = SHORT_VENDOR_NAMES[tool.id] || tool.vendor || tool.name;
  if (!isTrapOrHighest && typeof rowTotal === 'number' && typeof refTotal === 'number' && refTotal > rowTotal) {{
    const saved = Math.round(refTotal - rowTotal);
    if (saved > 0) {{
      return `Save $${{saved.toLocaleString()}}/yr with ${{shortVendor}} →`;
    }}
  }}
  return getVendorCtaLabel(tool);
}}

function renderCalcBreakdownHtml(r, seats, aiVol, mode) {{
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

function formatScenarioText(seats, aiVol, mode) {{
  const seatStr = `${{seats}} seat${{seats === 1 ? '' : 's'}}`;
  const billStr = mode === 'annual' ? 'annual billing' : 'monthly billing';
  return `Based on ${{seatStr}}, ${{billStr}}, ${{aiVol.toLocaleString()}} AI tickets/month`;
}}

function formatHiddenReason(r) {{
  const parts = [];
  if (r.onboarding > 0) parts.push(`$${{r.onboarding.toLocaleString()}} mandatory onboarding`);
  if (r.aiAnnual > 0) parts.push(`$${{r.aiAnnual.toLocaleString()}}/yr metered AI charges`);
  if (r.seatPaddingAnnual > 0) parts.push(`$${{r.seatPaddingAnnual.toLocaleString()}}/yr unused seat-minimum padding`);
  if (parts.length === 0) return `No mandatory onboarding or metered AI overages ($0 non-seat fees)`;
  return `Adds ${{parts.join(' + ')}} on top of $${{r.annualSeatsCost.toLocaleString()}} base licenses`;
}}

function computeSmoothBarShares(v1, v2, v3) {{
  const vals = [Math.max(0, v1), Math.max(0, v2), Math.max(0, v3)];
  const total = vals[0] + vals[1] + vals[2];
  if (total <= 0) return [33.3, 33.3, 33.4];
  const MIN_SHARE = 15.5;
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

let currentSpotlightId = {spotlight_js};

function renderDirectory() {{
  const cat = 'Helpdesk & AI Support';
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
      window.trackSaaSBillEvent('result_rendered', {{ page: PAGE_ID, category: cat, seats: seats, aiTickets: aiVol, billingMode: mode, sortMode: sortMode }});
    }}
  }}

  const filtered = TOOLS.filter(t => t.category === cat);
  const rows = filtered.map(t => calcToolYear1(t, seats, aiVol, mode));

  if (sortMode === 'highest') {{
    rows.sort((a, b) => b.year1Total - a.year1Total);
  }} else if (sortMode === 'hidden_fees') {{
    rows.sort((a, b) => b.hiddenFees - a.hiddenFees || b.year1Total - a.year1Total);
  }} else if (sortMode === 'name') {{
    rows.sort((a, b) => a.tool.name.localeCompare(b.tool.name));
  }} else {{
    rows.sort((a, b) => a.year1Total - b.year1Total);
  }}

  const toolSelect = document.getElementById('spotlight-tool-select');
  if (toolSelect) {{
    const SHORT_TOOL_LABELS = {{
      'intercom-fin-ai': 'Intercom + Fin AI ($0.99/res)',
      'freshdesk-support': 'Freshdesk Pro + Freddy AI',
      'zendesk-suite-team': 'Zendesk Suite Team + AI',
      'zendesk-suite-professional': 'Zendesk Suite Pro + AI',
      'help-scout-plus': 'Help Scout Plus + AI',
      'hubspot-service-hub': 'HubSpot Service Hub'
    }};
    const existingIds = Array.from(toolSelect.options).map(o => o.value).join(',');
    const newIds = rows.map(r => r.tool.id).join(',');
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

  const dynSubhead = document.getElementById('gap-dynamic-subhead');
  if (dynSubhead) {{
    dynSubhead.textContent = `All ${{rows.length}} tools compared for ${{seats}} seat${{seats === 1 ? '' : 's'}} · ${{mode === 'annual' ? 'annual' : 'monthly'}} billing · ${{aiVol.toLocaleString()}} AI tickets/mo · click any row to inspect its breakdown above.`;
  }}

  const byLowest = [...rows].sort((a, b) => a.year1Total - b.year1Total);
  const minR = byLowest[0];
  const maxR = byLowest[byLowest.length - 1];
  const icR = rows.find(r => r.tool.id === 'intercom-fin-ai') || maxR;
  const zdTeamR = rows.find(r => r.tool.id === 'zendesk-suite-team') || maxR;
  const fdR = rows.find(r => r.tool.id === 'freshdesk-support') || minR;
  const isZendeskFocus = COMPARE_MODE === 'zendesk_ai' || COMPARE_MODE === 'zendesk_vs_freshdesk';
  const primaryR = isZendeskFocus ? zdTeamR : icR;
  const maxTotal = Math.max(...rows.map(r => r.year1Total), 1);

  const spotR = rows.find(r => r.tool.id === currentSpotlightId) || icR;
  const spotAff = AFFILIATES[spotR.tool.affiliate_slug] || {{ destination_url: '#' }};
  const refBenchmarkR = (spotR.year1Total > minR.year1Total && spotR.tool.id !== minR.tool.id) ? spotR : icR;

  const baseSubYr = Math.min(spotR.annualSeatsCost, Math.round(spotR.unitRate * 12));
  const seatsUsageYr = Math.max(0, spotR.annualSeatsCost - baseSubYr);
  const overagesAddonsYr = spotR.onboarding + spotR.aiAnnual;
  const [s1, s2, s3] = computeSmoothBarShares(baseSubYr, seatsUsageYr, overagesAddonsYr);

  const rowBase = document.getElementById('wb-row-base');
  const rowSeats = document.getElementById('wb-row-seats');
  const rowHidden = document.getElementById('wb-row-hidden');
  if (rowBase && rowSeats && rowHidden) {{
    applyBarRowState(rowBase, s1, baseSubYr);
    applyBarRowState(rowSeats, s2, seatsUsageYr);
    applyBarRowState(rowHidden, s3, overagesAddonsYr);

    document.getElementById('wb-amt-base').textContent = `$${{baseSubYr.toLocaleString()}}`;
    document.getElementById('wb-amt-seats').textContent = `$${{seatsUsageYr.toLocaleString()}}`;
    document.getElementById('wb-amt-hidden').textContent = `$${{overagesAddonsYr.toLocaleString()}}`;
  }}

  document.getElementById('wb-selected-product').textContent = spotR.tool.name;
  document.getElementById('wb-big-amount').textContent = `$${{spotR.year1Total.toLocaleString()}}`;
  const subNoteEl = document.getElementById('wb-budget-subnote');
  if (subNoteEl) {{
    const stickerYr = Math.max(0, spotR.annualSeatsCost - spotR.seatPaddingAnnual);
    const extraYr = spotR.year1Total - stickerYr;
    if (extraYr > 0) {{
      const pctOver = stickerYr > 0 ? Math.round((extraYr / stickerYr) * 100) : 0;
      subNoteEl.textContent = `+$${{extraYr.toLocaleString()}} (+${{pctOver}}%) above advertised price.`;
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

  const wbCalcBody = document.getElementById('wb-calc-body');
  if (wbCalcBody) {{
    wbCalcBody.innerHTML = renderCalcBreakdownHtml(spotR, seats, aiVol, mode);
  }}

  const ctaEl = document.getElementById('wb-primary-cta');
  if (ctaEl) {{
    ctaEl.href = spotAff.destination_url;
    ctaEl.setAttribute('data-vendor', spotR.tool.id);
    const isSpotTrapOrHighest = spotR.tool.id === primaryR.tool.id || spotR.tool.id === maxR.tool.id || spotR.onboarding > 0;
    const wbRefTotal = primaryR.year1Total > spotR.year1Total ? primaryR.year1Total : maxR.year1Total;
    ctaEl.textContent = getContextualCtaLabel(spotR.tool, spotR.year1Total, wbRefTotal, isSpotTrapOrHighest);
  }}

  const summaryEl = document.getElementById('calc-summary-strip');
  const scenarioLine = formatScenarioText(seats, aiVol, mode);
  if (summaryEl) {{
    const minAff = AFFILIATES[minR.tool.affiliate_slug] || {{ destination_url: '#' }};
    const primaryAff = AFFILIATES[primaryR.tool.affiliate_slug] || {{ destination_url: '#' }};
    const zdAff = AFFILIATES[zdTeamR.tool.affiliate_slug] || {{ destination_url: '#' }};
    const minAudit = INTERNAL_AUDIT_LINKS[minR.tool.id];
    const primaryAudit = INTERNAL_AUDIT_LINKS[primaryR.tool.id];
    const zdAudit = INTERNAL_AUDIT_LINKS[zdTeamR.tool.id];
    const icAudit = INTERNAL_AUDIT_LINKS[icR.tool.id];

    const fdAff = AFFILIATES[fdR.tool.affiliate_slug] || {{ destination_url: '#' }};
    const thirdR = COMPARE_MODE === 'zendesk_ai' ? icR : ((COMPARE_MODE === 'intercom_vs_freshdesk' || COMPARE_MODE === 'zendesk_vs_freshdesk') ? fdR : zdTeamR);
    const thirdAff = AFFILIATES[thirdR.tool.affiliate_slug] || {{ destination_url: '#' }};
    const thirdLabel = COMPARE_MODE === 'zendesk_ai'
      ? 'Intercom + Fin AI (Same Usage)'
      : ((COMPARE_MODE === 'intercom_vs_freshdesk' || COMPARE_MODE === 'zendesk_vs_freshdesk') ? 'Freshdesk + Freddy AI (Session Packs)' : 'Zendesk AI Comparison (Same Usage)');
    const thirdCta = (COMPARE_MODE === 'intercom_vs_freshdesk' || COMPARE_MODE === 'zendesk_vs_freshdesk' || COMPARE_MODE === 'zendesk_ai')
      ? getContextualCtaLabel(thirdR.tool, thirdR.year1Total, primaryR.year1Total, thirdR.tool.id === primaryR.tool.id)
      : getVendorCtaLabel(zdTeamR.tool);
    const thirdAudit = INTERNAL_AUDIT_LINKS[thirdR.tool.id];
    const thirdAuditLink = COMPARE_MODE === 'intercom_vs_freshdesk'
      ? `<a class="summary-audit-link" href="{prefix}intercom-vs-zendesk-cost-comparison/" data-track="internal-audit">Compare Intercom vs. Zendesk →</a>`
      : (COMPARE_MODE === 'zendesk_vs_freshdesk'
        ? `<a class="summary-audit-link" href="{prefix}zendesk-ai-cost-calculator/" data-track="internal-audit">Open Zendesk AI calculator →</a>`
        : (thirdAudit ? `<a class="summary-audit-link" href="${{thirdAudit.url}}" data-track="internal-audit">${{thirdAudit.label}}</a>` : ''));

    const primaryHiddenPct = primaryR.year1Total > 0 ? Math.round((primaryR.hiddenFees / primaryR.year1Total) * 100) : 0;
    const primaryLabel = isZendeskFocus ? 'Zendesk Suite Team + AI ($1.50/Resolution)' : 'Intercom + Fin AI ($0.99/Resolution Meter)';
    const savedVsPrimary = Math.max(0, primaryR.year1Total - minR.year1Total);
    const minCtaText = getContextualCtaLabel(minR.tool, minR.year1Total, primaryR.year1Total, false);
    const money = n => '$' + Math.round(n).toLocaleString();
    let headToHeadHtml = '';
    if (COMPARE_MODE === 'intercom_vs_freshdesk') {{
      const gap = icR.year1Total - fdR.year1Total;
      const save = Math.abs(gap);
      const pct = icR.year1Total > 0 ? Math.round((save / Math.max(icR.year1Total, 1)) * 100) : 0;
      const cheaperName = gap >= 0 ? 'Freshdesk' : 'Intercom';
      headToHeadHtml = `
      <div class="summary-card result-card card-lowest">
        <div class="summary-label">Lowest Year-1 Cost: Freshdesk</div>
        <div class="summary-metric" style="color:var(--emerald);">${{money(fdR.year1Total)}} / yr &middot; Freshdesk</div>
        <div class="summary-scenario">${{scenarioLine}}</div>
        <div class="summary-breakdown">${{money(fdR.annualSeatsCost)}} licenses + ${{money(fdR.aiAnnual)}} Freddy AI sessions</div>
        <div class="summary-caveat"><strong>Contract note:</strong> Freshdesk (Freddy AI) bills $49 per 100 sessions after 500 one-time free sessions.</div>
        <details class="math-drawer"><summary>Show calculation</summary><div class="math-drawer-body">${{renderCalcBreakdownHtml(fdR, seats, aiVol, mode)}}</div></details>
        <div class="summary-actions"><div class="cta-stack"><a class="btn-cta" href="${{fdAff.destination_url}}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="freshdesk-support" data-cta-location="summary-card">${{getVendorCtaLabel(fdR.tool)}}</a></div></div>
      </div>
      <div class="summary-card result-card card-hidden">
        <div class="summary-label">Intercom + Fin AI ($0.99/resolution)</div>
        <div class="summary-metric" style="color:var(--rose);">${{money(icR.year1Total)}} / yr &middot; Intercom</div>
        <div class="summary-scenario">${{scenarioLine}}</div>
        <div class="summary-breakdown">${{money(icR.annualSeatsCost)}} licenses + ${{money(icR.aiAnnual)}} Fin AI</div>
        <div class="summary-caveat"><strong>Contract note:</strong> Intercom (Fin AI) meters $0.99 per resolution on top of the seat price.</div>
        <details class="math-drawer"><summary>Show calculation</summary><div class="math-drawer-body">${{renderCalcBreakdownHtml(icR, seats, aiVol, mode)}}</div></details>
        <div class="summary-actions"><div class="cta-stack"><a class="btn-secondary" href="${{AFFILIATES[icR.tool.affiliate_slug].destination_url}}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="intercom-fin-ai" data-cta-location="summary-card">${{getVendorCtaLabel(icR.tool)}}</a></div></div>
      </div>
      <div class="summary-card result-card card-highest">
        <div class="summary-label">Head-to-Head Gap: Intercom vs. Freshdesk</div>
        <div class="summary-metric">${{cheaperName}} saves ${{money(save)}}/yr (${{pct}}%)</div>
        <div class="summary-scenario">${{money(icR.year1Total)}} Intercom vs. ${{money(fdR.year1Total)}} Freshdesk at these sliders</div>
        <div class="summary-breakdown">Hidden cost gap on Intercom is ${{money(icR.hiddenFees)}}. Hidden cost gap on Freshdesk is ${{money(fdR.hiddenFees)}}.</div>
        <div class="summary-caveat"><strong>Head-to-head:</strong> ${{cheaperName}} is the lower Year-1 bill. The table below still lists every helpdesk tool.</div>
        <details class="math-drawer"><summary>Show calculation</summary><div class="math-drawer-body">${{renderCalcBreakdownHtml(gap >= 0 ? icR : fdR, seats, aiVol, mode)}}</div></details>
        <div class="summary-actions"><div class="cta-stack"><a class="btn-secondary" href="${{fdAff.destination_url}}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="freshdesk-support" data-cta-location="summary-card">Compare Freshdesk pricing &rarr;</a></div></div>
      </div>`;
    }} else if (COMPARE_MODE === 'intercom_vs_zendesk') {{
      const zdWins = zdTeamR.year1Total < icR.year1Total;
      const winner = zdWins ? 'Zendesk' : 'Intercom';
      const gap = Math.abs(zdTeamR.year1Total - icR.year1Total);
      headToHeadHtml = `
      <div class="summary-card result-card card-lowest">
        <div class="summary-label">Head-to-Head Winner: ${{winner}}</div>
        <div class="summary-metric" style="color:var(--emerald);">${{money(icR.year1Total)}}/yr vs. Zendesk ${{money(zdTeamR.year1Total)}}/yr</div>
        <div class="summary-scenario">${{scenarioLine}} &middot; ${{winner}} saves ${{money(gap)}}/yr</div>
        <div class="summary-breakdown">${{money(icR.annualSeatsCost)}} Intercom licenses + ${{money(icR.aiAnnual)}} Fin AI</div>
        <div class="summary-caveat"><strong>Contract note:</strong> Intercom Fin is $0.99 per resolution on a $29/seat Essential base in this model.</div>
        <details class="math-drawer"><summary>Show calculation</summary><div class="math-drawer-body">${{renderCalcBreakdownHtml(icR, seats, aiVol, mode)}}</div></details>
        <div class="summary-actions"><div class="cta-stack"><a class="btn-cta" href="${{AFFILIATES[icR.tool.affiliate_slug].destination_url}}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="intercom-fin-ai" data-cta-location="summary-card">${{getVendorCtaLabel(icR.tool)}}</a></div></div>
      </div>
      <div class="summary-card result-card card-hidden">
        <div class="summary-label">Zendesk Suite + AI ($55/seat + $1.50/resolution)</div>
        <div class="summary-metric" style="color:var(--rose);">${{money(zdTeamR.year1Total)}} / yr &middot; Zendesk</div>
        <div class="summary-scenario">${{scenarioLine}}</div>
        <div class="summary-breakdown">${{money(zdTeamR.annualSeatsCost)}} licenses + ${{money(zdTeamR.aiAnnual)}} resolution overage</div>
        <div class="summary-caveat"><strong>Contract note:</strong> Suite Pro is $115/seat plus a separate $50/seat Copilot add-on, then $1.50 per resolution over the included allowance. This card is Suite Team and does not add Copilot.</div>
        <details class="math-drawer"><summary>Show calculation</summary><div class="math-drawer-body">${{renderCalcBreakdownHtml(zdTeamR, seats, aiVol, mode)}}</div></details>
        <div class="summary-actions"><div class="cta-stack"><a class="btn-secondary" href="${{zdAff.destination_url}}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="zendesk-suite-team" data-cta-location="summary-card">${{getVendorCtaLabel(zdTeamR.tool)}}</a></div></div>
      </div>
      <div class="summary-card result-card card-highest">
        <div class="summary-label">Lowest-Cost Alternative: Freshdesk</div>
        <div class="summary-metric">${{money(fdR.year1Total)}} / yr &middot; Freshdesk</div>
        <div class="summary-scenario">${{scenarioLine}}</div>
        <div class="summary-breakdown">${{money(fdR.annualSeatsCost)}} licenses + ${{money(fdR.aiAnnual)}} Freddy AI sessions</div>
        <div class="summary-caveat"><strong>Contract note:</strong> Freshdesk stays in the table as the lower-cost helpdesk alternative.</div>
        <details class="math-drawer"><summary>Show calculation</summary><div class="math-drawer-body">${{renderCalcBreakdownHtml(fdR, seats, aiVol, mode)}}</div></details>
        <div class="summary-actions"><div class="cta-stack"><a class="btn-secondary" href="${{fdAff.destination_url}}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="freshdesk-support" data-cta-location="summary-card">${{getVendorCtaLabel(fdR.tool)}}</a></div></div>
      </div>`;
    }} else if (COMPARE_MODE === 'zendesk_vs_freshdesk') {{
      const gap = zdTeamR.year1Total - fdR.year1Total;
      const save = Math.abs(gap);
      const cheaperName = gap >= 0 ? 'Freshdesk' : 'Zendesk';
      headToHeadHtml = `
      <div class="summary-card result-card card-lowest">
        <div class="summary-label">Lowest Year-1 Cost: Freshdesk</div>
        <div class="summary-metric" style="color:var(--emerald);">${{money(fdR.year1Total)}} / yr</div>
        <div class="summary-scenario">${{scenarioLine}}</div>
        <div class="summary-breakdown">${{money(fdR.annualSeatsCost)}} licenses + ${{money(fdR.aiAnnual)}} Freddy AI sessions</div>
        <div class="summary-caveat"><strong>Contract note:</strong> Freshdesk (Freddy AI) uses session packs, not a per-resolution meter.</div>
        <details class="math-drawer"><summary>Show calculation</summary><div class="math-drawer-body">${{renderCalcBreakdownHtml(fdR, seats, aiVol, mode)}}</div></details>
        <div class="summary-actions"><div class="cta-stack"><a class="btn-cta" href="${{fdAff.destination_url}}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="freshdesk-support" data-cta-location="summary-card">${{getVendorCtaLabel(fdR.tool)}}</a></div></div>
      </div>
      <div class="summary-card result-card card-hidden">
        <div class="summary-label">Zendesk Suite + AI</div>
        <div class="summary-metric" style="color:var(--rose);">${{money(zdTeamR.year1Total)}} / yr</div>
        <div class="summary-scenario">${{scenarioLine}}</div>
        <div class="summary-breakdown">${{money(zdTeamR.annualSeatsCost)}} licenses + ${{money(zdTeamR.aiAnnual)}} resolution overage</div>
        <div class="summary-caveat"><strong>Contract note:</strong> Zendesk Suite + Advanced AI bills included resolutions, then $1.50 committed or $2.00 monthly.</div>
        <details class="math-drawer"><summary>Show calculation</summary><div class="math-drawer-body">${{renderCalcBreakdownHtml(zdTeamR, seats, aiVol, mode)}}</div></details>
        <div class="summary-actions"><div class="cta-stack"><a class="btn-secondary" href="${{zdAff.destination_url}}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="zendesk-suite-team" data-cta-location="summary-card">${{getVendorCtaLabel(zdTeamR.tool)}}</a></div></div>
      </div>
      <div class="summary-card result-card card-highest">
        <div class="summary-label">Head-to-Head Savings: Save ${{money(save)}}/yr with ${{cheaperName}}</div>
        <div class="summary-metric">${{cheaperName}} vs. ${{gap >= 0 ? 'Zendesk' : 'Freshdesk'}}</div>
        <div class="summary-scenario">${{money(fdR.year1Total)}} Freshdesk vs. ${{money(zdTeamR.year1Total)}} Zendesk</div>
        <div class="summary-breakdown">Hidden cost gap: Freshdesk ${{money(fdR.hiddenFees)}}, Zendesk ${{money(zdTeamR.hiddenFees)}}.</div>
        <div class="summary-caveat"><strong>Head-to-head:</strong> ${{cheaperName}} is lower at these sliders. Ticket history can be exported from either helpdesk.</div>
        <details class="math-drawer"><summary>Show calculation</summary><div class="math-drawer-body">${{renderCalcBreakdownHtml(fdR, seats, aiVol, mode)}}</div></details>
        <div class="summary-actions"><div class="cta-stack"><a class="btn-secondary" href="${{fdAff.destination_url}}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="freshdesk-support" data-cta-location="summary-card">View Freshdesk pricing &rarr;</a></div></div>
      </div>`;
    }}

    summaryEl.innerHTML = headToHeadHtml || `
      <div class="summary-card result-card card-lowest">
        <div class="summary-label">Best Value &middot; Lowest Year-1 Cost</div>
        <div class="summary-metric" style="color:var(--emerald);">$${{minR.year1Total.toLocaleString()}} / yr &middot; ${{minR.tool.name}}</div>
        <div class="summary-scenario">${{scenarioLine}}${{savedVsPrimary > 0 ? ` &middot; saves $${{savedVsPrimary.toLocaleString()}}/yr vs. ${{primaryR.tool.name}}` : ''}}</div>
        <div class="summary-breakdown">$${{minR.annualSeatsCost.toLocaleString()}} licenses + $${{minR.onboarding.toLocaleString()}} onboarding + $${{minR.aiAnnual.toLocaleString()}} AI</div>
        <div class="summary-caveat"><strong>Contract note:</strong> ${{minR.tool.trap_badge}}</div>
        <details class="math-drawer">
          <summary>Show calculation</summary>
          <div class="math-drawer-body">${{renderCalcBreakdownHtml(minR, seats, aiVol, mode)}}</div>
        </details>
        <div class="summary-actions">
          <div class="cta-stack">
            <a class="btn-cta" href="${{minAff.destination_url}}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="${{minR.tool.id}}" data-cta-location="summary-card">${{minCtaText}}</a>
          </div>
          ${{minAudit ? `<a class="summary-audit-link" href="${{minAudit.url}}" data-track="internal-audit">${{minAudit.label}}</a>` : ''}}
        </div>
      </div>
      <div class="summary-card result-card card-hidden">
        <div class="summary-label">${{primaryLabel}}</div>
        <div class="summary-metric" style="color:var(--rose);">+$${{primaryR.hiddenFees.toLocaleString()}} / yr (${{primaryHiddenPct}}% of Year-1 bill)</div>
        <div class="summary-scenario">On <strong>${{primaryR.tool.name}}</strong> ($${{primaryR.year1Total.toLocaleString()}}/yr total &middot; ${{scenarioLine.replace('Based on ', '')}})</div>
        <div class="summary-breakdown">$${{primaryR.annualSeatsCost.toLocaleString()}} licenses + $${{primaryR.onboarding.toLocaleString()}} onboarding + $${{primaryR.aiAnnual.toLocaleString()}} AI</div>
        <div class="summary-caveat"><strong>Hidden Cost Highlight:</strong> ${{formatHiddenReason(primaryR)}}.</div>
        <details class="math-drawer">
          <summary>Show calculation</summary>
          <div class="math-drawer-body">${{renderCalcBreakdownHtml(primaryR, seats, aiVol, mode)}}</div>
        </details>
        <div class="summary-actions">
          <div class="cta-stack">
            <a class="btn-secondary" href="${{primaryAff.destination_url}}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="${{primaryR.tool.id}}" data-cta-location="summary-card">${{getVendorCtaLabel(primaryR.tool)}}</a>
          </div>
          ${{primaryAudit ? `<a class="summary-audit-link" href="${{primaryAudit.url}}" data-track="internal-audit">${{primaryAudit.label}}</a>` : ''}}
        </div>
      </div>
      <div class="summary-card result-card card-highest">
        <div class="summary-label">${{thirdLabel}}</div>
        <div class="summary-metric">$${{thirdR.year1Total.toLocaleString()}} / yr &middot; ${{thirdR.tool.name}}</div>
        <div class="summary-scenario">${{scenarioLine}}</div>
        <div class="summary-breakdown">$${{thirdR.annualSeatsCost.toLocaleString()}} licenses + $${{thirdR.onboarding.toLocaleString()}} onboarding + $${{thirdR.aiAnnual.toLocaleString()}} AI</div>
        <div class="summary-caveat"><strong>Contract note:</strong> ${{thirdR.tool.trap_badge}}</div>
        <details class="math-drawer">
          <summary>Show calculation</summary>
          <div class="math-drawer-body">${{renderCalcBreakdownHtml(thirdR, seats, aiVol, mode)}}</div>
        </details>
        <div class="summary-actions">
          <div class="cta-stack">
            <a class="btn-secondary" href="${{thirdAff.destination_url}}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="${{thirdR.tool.id}}" data-cta-location="summary-card">${{thirdCta}}</a>
          </div>
          ${{thirdAuditLink}}
        </div>
      </div>
    `;
  }}

  const vizRowsEl = document.getElementById('calc-viz-rows');
  if (vizRowsEl) {{
    vizRowsEl.innerHTML = rows.map(r => {{
      const aff = AFFILIATES[r.tool.affiliate_slug] || {{ destination_url: '#' }};
      const seatPct = Math.max(0, (r.annualSeatsCost / maxTotal) * 100);
      const onbPct = Math.max(0, (r.onboarding / maxTotal) * 100);
      const aiPct = Math.max(0, (r.aiAnnual / maxTotal) * 100);
      const parts = [`$${{r.annualSeatsCost.toLocaleString()}} licenses`];
      if (r.onboarding > 0) parts.push(`$${{r.onboarding.toLocaleString()}} onboarding`);
      if (r.aiAnnual > 0) parts.push(`$${{r.aiAnnual.toLocaleString()}} AI overage`);
      const isSpotViz = r.tool.id === currentSpotlightId ? 'is-spotlight-row' : '';
      const isSavingsOption = r.year1Total < primaryR.year1Total && r.tool.id !== primaryR.tool.id;
      const rowCta = getContextualCtaLabel(r.tool, r.year1Total, primaryR.year1Total, !isSavingsOption);
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

  document.getElementById('calc-tbody').innerHTML = rows.map(r => {{
    const t = r.tool;
    const aff = AFFILIATES[t.affiliate_slug] || {{ destination_url: '#' }};
    const verStatus = t.verification_status || 'Verified';
    const verClass = verStatus.startsWith('Verified') ? 'status-verified' : 'status-estimated';
    const srcUrl = (t.source_urls && t.source_urls[0]) ? t.source_urls[0] : aff.destination_url;
    const auditObj = INTERNAL_AUDIT_LINKS[t.id];
    const fmtRate = n => Number.isInteger(n) ? n.toLocaleString() : n.toFixed(2);

    const stickerAnnual = Math.max(0, r.annualSeatsCost - r.seatPaddingAnnual);
    const gapDollars = r.year1Total - stickerAnnual;
    const gapPct = stickerAnnual > 0 ? Math.round((gapDollars / stickerAnnual) * 100) : 0;

    let gapCellHtml = '';
    if (gapDollars > 0) {{
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
    const isSavingsRow = r.year1Total < primaryR.year1Total && t.id !== primaryR.tool.id;
    const tableCtaText = getContextualCtaLabel(t, r.year1Total, primaryR.year1Total, !isSavingsRow);
    return `
      <tr class="${{isSpot}}" data-row-tool="${{t.id}}" style="cursor:pointer;">
        <td data-label="Platform">
          <div class="gap-platform-name">
            <strong>${{t.name}}</strong>
            <span class="status-pill ${{verClass}}">${{verStatus}}</span>
          </div>
          <div class="gap-platform-meta">${{t.category}}${{auditObj ? ` &middot; <a class="audit-inline-link" href="${{auditObj.url}}" data-track="internal-audit">${{auditObj.label}}</a>` : ''}}</div>
        </td>
        <td data-label="Sticker Price / Year"><div class="gap-figure">$${{stickerAnnual.toLocaleString()}}</div><div class="gap-sub-detail">$${{fmtRate(r.unitRate)}}/seat/mo</div></td>
        <td data-label="Year-1 Total"><div class="gap-figure">$${{r.year1Total.toLocaleString()}}</div><div class="gap-sub-detail">${{r.effSeats}} billed seat${{r.effSeats === 1 ? '' : 's'}}</div></td>
        <td data-label="Hidden Cost Gap">${{gapCellHtml}}</td>
        <td data-label="Official Pricing">
          <div class="cta-stack">
            <a class="btn-secondary" href="${{aff.destination_url}}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="${{t.id}}" data-cta-location="table-row">${{tableCtaText}}</a>
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
  const disclosures = cards.map(c => c.querySelector('.math-drawer'));
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
    }}
  }});
}}

['seat-slider', 'ai-slider', 'billing-mode', 'sort-mode'].forEach(id => {{
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
  }});
}}

window.addEventListener('resize', () => {{
  equalizeSummaryCards(document.getElementById('calc-summary-strip'));
}});

renderDirectory();
</script>
"""
    return wrap_calculator_shell(html)


ic_faqs = [
    (
        "How much does Intercom Fin AI charge per resolution in 2026?",
        "Intercom charges $0.99 per Fin AI outcome/resolution (and $9.99 per sales qualification outcome), billed at most once per conversation, on top of your monthly per-seat plan ($29 Essential, $85 Advanced, or $132 Expert billed annually).",
    ),
    (
        "What counts as a billable Fin AI resolution in Intercom?",
        "A billable $0.99 Fin outcome occurs when the customer confirms their question was answered, exits the conversation without requesting a human agent after Fin's answer, or triggers a configured procedure handoff/disqualification outcome.",
    ),
    (
        "How does Freshdesk Freddy AI pricing compare to Intercom's $0.99 per-resolution meter?",
        "Freshdesk (by Freshworks) charges $19 (Growth), $55 (Pro), or $89 (Enterprise) per agent/month billed annually ($23/$66/$107 monthly). For autonomous AI support, Freddy AI Agent includes 500 one-time complimentary sessions per account and then bills $49 per 100-session pack (charged per session, resolved or not), while Freddy AI Copilot for human agents is an optional $29/agent/month add-on.",
    ),
]


def build_all():
    render_page(
        "intercom-fin-cost-calculator/index.html",
        "Intercom Fin Cost Calculator (2026) – saasbill.io",
        "Calculate your 2026 Intercom Fin AI true Year-1 cost at $0.99 per resolution (prefilled for 10 agents & 1,500 AI resolutions/month) and compare against Freshdesk and Zendesk AI.",
        "/intercom-fin-cost-calculator/",
        render_intercom_calculator_body(prefix="../"),
        faqs=ic_faqs,
    )
    render_page(
        "pricing/intercom-fin-ai-resolution-cost-calculator/index.html",
        "Intercom Fin AI True Cost & Year-1 Calculator – saasbill.io",
        "Calculate your 2026 Intercom Fin AI true cost and Year-1 support bill at $0.99 per AI resolution plus seat licenses ($29-$132/mo), and compare AI cost against Freshdesk and Zendesk.",
        "/pricing/intercom-fin-ai-resolution-cost-calculator/",
        render_intercom_calculator_body(prefix="../../"),
        faqs=ic_faqs,
    )
    render_page(
        "intercom-vs-freshdesk-cost-comparison/index.html",
        "Intercom vs Freshdesk Cost Comparison (2026) – saasbill.io",
        "Compare 2026 Intercom + Fin AI ($0.99/resolution) vs Freshdesk Freddy AI ($49/100 sessions) Year-1 total cost for your exact team size and AI ticket volume.",
        "/intercom-vs-freshdesk-cost-comparison/",
        render_intercom_calculator_body(
            prefix="../",
            h1="Intercom vs Freshdesk Cost Comparison (2026): Real Year-1 Price &amp; AI Fees",
            lead="Compare what Intercom Fin and Freshdesk Freddy AI actually cost for your support team. Adjust the agents and AI volume below to see the real Year-1 total and exact savings side by side.",
            compare_mode="intercom_vs_freshdesk",
            page_id="intercom-vs-freshdesk-cost-comparison",
            calc_heading="Intercom vs. Freshdesk Year-1 Cost &amp; AI Resolution Calculator (2026)",
            editorial_html=IF_EDITORIAL,
        ),
        faqs=if_faqs,
    )
    render_page(
        "intercom-vs-zendesk-cost-comparison/index.html",
        "Intercom vs Zendesk Cost Comparison (2026) – saasbill.io",
        "Compare 2026 Intercom Fin AI ($0.99/resolution) vs Zendesk AI Agents ($1.50/resolution) Year-1 total cost for your exact agent count and monthly AI volume.",
        "/intercom-vs-zendesk-cost-comparison/",
        render_intercom_calculator_body(
            prefix="../",
            h1="Intercom vs Zendesk Cost Comparison (2026): Real Year-1 Price &amp; AI Overage",
            lead="Compare what Intercom Fin and Zendesk AI actually cost for your support team. Adjust the agents and AI volume below to see the real Year-1 total, per-resolution overages, and lower-cost alternatives.",
            compare_mode="intercom_vs_zendesk",
            page_id="intercom-vs-zendesk-cost-comparison",
            calc_heading="Intercom vs. Zendesk Year-1 Cost &amp; AI Resolution Calculator (2026)",
            editorial_html=IZ_EDITORIAL,
        ),
        faqs=iz_faqs,
    )


ZENDESK_EDITORIAL = """
<section class="editorial-below-section">
  <h2>Why Zendesk AI overage outgrows the seat price</h2>
  <div class="methodology-grid fine-print-grid">
    <div class="methodology-item">
      <strong>1. Five included resolutions per agent, then $1.50</strong>
      Suite Team ($55/agent/mo billed annually) includes 5 automated resolutions per agent each month. At 10 agents that is 50 included resolutions. Every resolution above that costs $1.50 committed or $2.00 pay-as-you-go, and overage is on by default.
    </div>
    <div class="methodology-item">
      <strong>2. The prefilled Year-1 total is $32,700</strong>
      10 agents on annual Suite Team are $6,600 in seats. 1,500 AI resolutions a month leave 1,450 billable at $1.50, which is $26,100 a year. Seats plus overage equal $32,700. Freshdesk Growth plus Freddy AI session packs is $10,855 for the same usage, a $21,845 gap.
    </div>
    <div class="methodology-item">
      <strong>3. The $50 Copilot add-on is separate</strong>
      Zendesk lists Copilot at $50 per agent per month on annual billing. That add-on is not inside the $32,700 Suite Team figure above. Buying it for 10 agents would add another $6,000 a year on top of seats and per-resolution overage.
    </div>
  </div>
</section>
"""

ZENDESK_BEST = (
    '<strong>Best option:</strong> <a href="https://www.freshworks.com/freshdesk/pricing/" '
    'target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="freshdesk-support" '
    'data-cta-location="workbench-best-option">Freshdesk Growth + Freddy AI ($10,855/yr)</a> '
    '&middot; saves $21,845/yr'
)

zd_faqs = [
    (
        "How much does Zendesk AI cost for 10 agents and 1,500 resolutions a month?",
        "On Suite Team billed annually, 10 agents cost $55 each ($6,600/year) and include 50 automated resolutions a month. The other 1,450 resolutions at the $1.50 committed rate add $26,100, for a $32,700 Year-1 total. The same usage on Freshdesk Growth plus Freddy AI session packs is $10,855.",
    ),
    (
        "Does the $50 per agent Copilot add-on sit inside that $32,700?",
        "No. The $32,700 figure is Suite Team seats plus committed per-resolution overage. Zendesk lists Copilot separately at $50 per agent per month on annual billing, which is another $6,000 a year for 10 agents.",
    ),
    (
        "How does Freshdesk Freddy AI compare at the same volume?",
        "Freshdesk Growth is $19 per agent per month billed annually. Freddy AI Agent includes 500 one-time sessions, then $49 per 100-session pack. At 1,500 AI tickets a month that is $10,855 in Year 1, which is $21,845 less than Zendesk Suite Team.",
    ),
]


def _zendesk_body(prefix, h1, lead, compare_mode, page_id, legacy_summary_id, calc_heading=None, editorial_html=None):
    return render_intercom_calculator_body(
        prefix=prefix,
        h1=h1,
        lead=lead,
        compare_mode=compare_mode,
        page_id=page_id,
        spotlight_id="zendesk-suite-team",
        legacy_summary_id=legacy_summary_id,
        editorial_html=editorial_html or ZENDESK_EDITORIAL,
        calc_heading=calc_heading or "Interactive Zendesk AI Year-1 True-Cost Calculator (2026)",
        gap_sub="Visual Year-1 cost comparison graph &amp; full contract table (Zendesk AI vs. Freshdesk, Intercom, Help Scout &amp; HubSpot)",
        static_product="Zendesk Suite Team + AI Agents",
        static_total="$32,700",
        static_subnote="+$26,100 (+395%) above advertised price.",
        static_best_html=ZENDESK_BEST,
        static_base="$660",
        static_seats="$5,940",
        static_hidden="$26,100",
        static_hidden_sub="Zendesk AI $1.50/resolution overage",
    )


def build_zendesk_cluster():
    h1 = "Zendesk AI Cost Calculator: Calculate Your Real Year-1 Total ($50/Seat Add-On + $1.50/Resolution)"
    lead = "See what Zendesk AI actually costs once the $50/agent add-on and per-resolution overages are included. Adjust the agents and AI volume below to see your real Year-1 total and how it compares to Freshdesk and Intercom."
    title = "Zendesk AI Cost Calculator (2026): Real Per-Resolution &amp; Add-On Pricing | SaaSBill"
    description = "Calculate Zendesk AI Year-1 cost for 10 agents and 1,500 resolutions: Suite Team is $32,700 versus $10,855 on Freshdesk, a $21,845 gap."
    render_page(
        "zendesk-ai-cost-calculator/index.html",
        title,
        description,
        "/zendesk-ai-cost-calculator/",
        _zendesk_body("../", h1, lead, "zendesk_ai", "zendesk-ai-cost-calculator", "zd-summary"),
        faqs=zd_faqs,
    )
    render_page(
        "pricing/zendesk-ai-resolution-and-automated-outcome-cost/index.html",
        title,
        description,
        "/pricing/zendesk-ai-resolution-and-automated-outcome-cost/",
        _zendesk_body("../../", h1, lead, "zendesk_ai", "zendesk-ai-resolution-cost", "zd-summary"),
        faqs=zd_faqs,
        published_date="2026-10-25",
    )
    render_page(
        "zendesk-vs-freshdesk-cost-comparison/index.html",
        "Zendesk vs Freshdesk Cost Comparison (2026): AI &amp; Seat Pricing Calculator | SaaSBill",
        "Compare Zendesk Suite Team AI at $32,700 with Freshdesk Freddy AI at $10,855 for 10 agents and 1,500 AI resolutions a month.",
        "/zendesk-vs-freshdesk-cost-comparison/",
        _zendesk_body(
            "../",
            "Zendesk vs Freshdesk Cost Comparison: Real Year-1 Pricing with AI Resolutions",
            "Compare what Zendesk AI and Freshdesk Freddy AI actually cost for your support team. Adjust the agents and AI volume below to see the real Year-1 total and exact annual savings side by side.",
            "zendesk_vs_freshdesk",
            "zendesk-vs-freshdesk-cost-comparison",
            "zd-summary",
            calc_heading="Zendesk vs. Freshdesk Year-1 Cost &amp; AI Resolution Calculator (2026)",
            editorial_html=ZF_EDITORIAL,
        ),
        faqs=zf_faqs,
    )


IF_EDITORIAL = """
<section class="editorial-below-section">
  <h2>Why Intercom ($21,300/yr) costs nearly 2x Freshdesk ($10,855/yr) at 1,500 AI resolutions/month</h2>
  <div class="methodology-grid fine-print-grid">
    <div class="methodology-item">
      <strong>1. Per resolution vs. per 100 sessions</strong>
      Intercom Fin bills $0.99 every time a conversation counts as resolved. Freshdesk Freddy AI includes 500 one-time sessions, then $49 per 100-session pack, which is about $0.49 a session.
    </div>
    <div class="methodology-item">
      <strong>2. The default 10-agent gap is $10,445</strong>
      At 10 agents and 1,500 AI resolutions a month on annual billing, Intercom Essential plus Fin is $21,300. Freshdesk Growth plus Freddy session packs is $10,855. Move the sliders and the three cards recompute that gap.
    </div>
    <div class="methodology-item">
      <strong>3. When the Intercom premium is the point</strong>
      Teams pay it for the Fin inbox, messenger, and help center in one product. If the job is ticket deflection at a known session price, Freshdesk stays lower at this volume.
    </div>
  </div>
</section>
"""

IZ_EDITORIAL = """
<section class="editorial-below-section">
  <h2>Why Zendesk ($32,700/yr) costs $11,400/yr more than Intercom ($21,300/yr) at 10 seats</h2>
  <div class="methodology-grid fine-print-grid">
    <div class="methodology-item">
      <strong>1. Seat price plus a thin included allowance</strong>
      This comparison uses Zendesk Suite Team at $55/agent/month annual, with 5 automated resolutions per agent each month, then $1.50 committed. Intercom Essential is $29/seat plus $0.99 per Fin resolution.
    </div>
    <div class="methodology-item">
      <strong>2. The $11,400 gap at the default sliders</strong>
      10 agents and 1,500 resolutions a month is $21,300 on Intercom and $32,700 on Suite Team. Suite Pro is a different plan at $115/seat, and the $50/seat Copilot add-on is not inside either total.
    </div>
    <div class="methodology-item">
      <strong>3. Freshdesk is the lower third option</strong>
      The same usage on Freshdesk Growth plus Freddy AI is $10,855. It stays in the table so the head-to-head is not only Intercom versus Zendesk.
    </div>
  </div>
</section>
"""

ZF_EDITORIAL = """
<section class="editorial-below-section">
  <h2>How Freshdesk saves $21,845 in Year 1 compared to Zendesk Suite Professional + AI</h2>
  <div class="methodology-grid fine-print-grid">
    <div class="methodology-item">
      <strong>1. Seat price</strong>
      Freshdesk Growth is $19 per agent per month billed annually. Zendesk Suite Team in this calculator is $55. Suite Professional is $115, and Copilot is another $50 per agent if you add it.
    </div>
    <div class="methodology-item">
      <strong>2. Freddy sessions vs. Zendesk resolutions</strong>
      Freshdesk bills $49 per 100 Freddy sessions after 500 one-time free sessions. Zendesk includes a small monthly allowance, then $1.50 committed or $2.00 on monthly billing.
    </div>
    <div class="methodology-item">
      <strong>3. The default savings are $21,845</strong>
      At 10 agents and 1,500 AI resolutions a month, Freshdesk is $10,855 and Suite Team is $32,700. Ticket exports exist on both, so the Year-1 gap is the number to compare before a migration.
    </div>
  </div>
</section>
"""

if_faqs = [
    (
        "How does Freshdesk's per-100-session price compare with Intercom's $0.99 resolution?",
        "Intercom Fin bills $0.99 once per conversation that counts as resolved. Freshdesk Freddy AI Agent includes 500 one-time sessions, then $49 per 100-session pack (about $0.49 a session), and those packs are charged per session whether or not the customer marks it resolved.",
    ),
    (
        "Is Freddy AI Copilot the same line item as Intercom Fin?",
        "No. Freddy AI Copilot is an optional $29 per agent per month add-on for human agents. The $10,855 Year-1 figure at 10 agents and 1,500 resolutions is Growth seats plus Freddy session packs, not Copilot. Intercom's $21,300 figure is Essential seats plus the $0.99 Fin meter.",
    ),
    (
        "When is Intercom worth the premium over Freshdesk?",
        "At the default 10 agents and 1,500 AI resolutions a month, Intercom is $21,300 and Freshdesk is $10,855, a $10,445 gap. Intercom is the premium when you want Fin, the messenger, and the help center in one suite. Freshdesk is the lower bill when you want a known session-pack price.",
    ),
]

iz_faqs = [
    (
        "What is Intercom Fin's price on a $29 seat versus Zendesk's seat plus AI add-on?",
        "Intercom Essential is $29 per seat per month on annual billing, plus $0.99 per Fin resolution. Zendesk Suite Team in this calculator is $55 per agent with 5 included automated resolutions per agent each month, then $1.50 committed. Suite Pro is $115 per seat, and Copilot is a separate $50 per agent per month. Neither Copilot nor the Suite Pro seat price is inside the $32,700 Suite Team total.",
    ),
    (
        "Why is Zendesk $11,400 a year more than Intercom at 10 seats and 1,500 resolutions?",
        "Suite Team seats for 10 agents are $6,600. Included resolutions are 50 a month, so 1,450 resolutions at $1.50 add $26,100, for $32,700. Intercom Essential seats are $3,480 and 1,500 Fin resolutions at $0.99 add $17,820, for $21,300. The difference is $11,400.",
    ),
    (
        "Does the $1.50 Zendesk overage replace the $50 Copilot add-on?",
        "No. The $1.50 is the committed per-resolution rate after the included allowance. Copilot is listed separately at $50 per agent per month on annual billing, which would be another $6,000 a year for 10 agents and is not in the $32,700.",
    ),
]

zf_faqs = [
    (
        "How do Zendesk and Freshdesk seat prices compare before AI?",
        "Freshdesk Growth is $19 per agent per month billed annually ($2,280 a year for 10 agents). Zendesk Suite Team is $55 ($6,600). Suite Professional is $115 ($13,800) before any resolution overage or the $50 Copilot add-on.",
    ),
    (
        "How do Freddy AI sessions differ from Zendesk automated resolutions?",
        "Freddy AI Agent includes 500 one-time sessions, then $49 per 100 sessions. Zendesk includes 5 automated resolutions per Suite Team agent each month (10 on Suite Professional) and then bills $1.50 committed or $2.00 pay-as-you-go. At 1,500 resolutions a month those meters, not the seat price alone, create most of the Year-1 gap.",
    ),
    (
        "Can you move tickets if you switch from Zendesk to Freshdesk?",
        "Both products expose ticket export. Freshdesk documents ticket XML, CSV, and API export. A migration still needs a field map and a cutover window, but the Year-1 price gap at 10 agents and 1,500 resolutions is $21,845 ($10,855 on Freshdesk versus $32,700 on Suite Team) before you add that project time.",
    ),
]


if __name__ == "__main__":
    build_all()
    build_zendesk_cluster()
