"""Build the 6 queued calculators + 3 high-intent Answer-First FAQ pages for saasbill.io."""
import json
import os

from layout import DATA_DIR, WORKBENCH_JS, render_page, render_workbench

# Pipedrive row on the Close vs HubSpot page: Premium is the current name of the
# tier that used to be "Professional". Annual price from data/crm_pricing.json.
with open(os.path.join(DATA_DIR, "crm_pricing.json")) as _f:
    _PD_PREMIUM = json.load(_f)["pipedrive"]["plans"]["premium"]
assert _PD_PREMIUM["annual_status"] == "verified"
PD_PREMIUM_LABEL = _PD_PREMIUM["label"]
PD_PREMIUM_ANNUAL = "%g" % _PD_PREMIUM["annual"]

PAGES = [
    {
        "rel": "compare/typeform-vs-jotform-response-limit-and-hipaa-cost/index.html",
        "slug": "/compare/typeform-vs-jotform-response-limit-and-hipaa-cost/",
        "title": "Typeform vs Jotform True Cost & HIPAA (2026) – saasbill.io",
        "desc": "Calculate the 2026 true cost and Year-1 price of Typeform vs. Jotform including response overages and HIPAA BAA tiers ($99/mo Jotform Gold vs. Typeform Enterprise).",
        "summary_id": "tf-summary",
        "h1": "Typeform vs. Jotform True Cost (2026): Response Caps &amp; HIPAA BAA Tiers",
        "lead": "Jotform Gold includes a signed HIPAA BAA and 10,000 monthly submissions for $99/month billed annually ($1,188/year) in 2026, whereas Typeform requires a custom Enterprise contract (benchmark $6,000+/year) for HIPAA compliance and caps Plus plans at 1,000 responses/month (sources: Jotform &amp; Typeform pricing pages, verified Oct 2026).",
        "ctrl_label": "Monthly Form Submissions",
        "ctrl_min": 100, "ctrl_max": 10000, "ctrl_step": 100, "ctrl_val": 2500, "ctrl_unit": "responses/mo",
        "opt_label": "Compliance Tier",
        "opt1_val": "hipaa", "opt1_text": "HIPAA BAA Required (Healthcare / Regulated)",
        "opt2_val": "standard", "opt2_text": "Standard Business Forms (No HIPAA BAA)",
        "winner_name": "Jotform Gold (HIPAA BAA Included)",
        "winner_url": "https://www.jotform.com/hipaa/pricing/?partner=saasbill",
        "winner_cta": "View Jotform HIPAA pricing",
        "winner_vendor": "jotform-hipaa",
        "js_logic": """
        const vol = parseInt(document.getElementById('p-slider').value, 10);
        const mode = document.getElementById('p-select').value;
        document.getElementById('p-slider-val').textContent = vol.toLocaleString('en-US') + ' responses/mo';
        const jfMo = mode === 'hipaa' ? 99 : (vol <= 1000 ? 34 : (vol <= 2500 ? 39 : 99));
        const jfYr = jfMo * 12;
        const tfMo = mode === 'hipaa' ? 500 : (vol <= 100 ? 25 : (vol <= 1000 ? 50 : 83));
        const tfYr = tfMo * 12;
        const saved = Math.max(0, tfYr - jfYr);
        const rows = [
          {name: mode === 'hipaa' ? 'Jotform Gold (HIPAA BAA)' : 'Jotform (Bronze/Silver/Gold)', plan: '$' + jfMo + '/mo annual', base: '$' + jfYr.toLocaleString('en-US') + '/yr', hidden: '$0 (BAA & 10k responses incl.)', total: '$' + jfYr.toLocaleString('en-US') + '/yr', url: 'https://www.jotform.com/hipaa/pricing/?partner=saasbill', cta: 'View Jotform HIPAA pricing', vendor: 'jotform-hipaa', status: 'Verified', src: 'https://www.jotform.com/hipaa/pricing/'},
          {name: mode === 'hipaa' ? 'Typeform Enterprise (HIPAA)' : 'Typeform (Basic/Plus/Business)', plan: mode === 'hipaa' ? 'Custom (~$500/mo est.)' : '$' + tfMo + '/mo annual', base: '$' + tfYr.toLocaleString('en-US') + '/yr', hidden: mode === 'hipaa' ? 'Mandatory Enterprise upgrade for BAA' : 'Hard response tier jumps at 100 & 1,000/mo', total: '$' + tfYr.toLocaleString('en-US') + '/yr', url: 'https://www.typeform.com/pricing/', cta: 'View Typeform pricing', vendor: 'typeform', status: mode === 'hipaa' ? 'Estimated (Benchmark)' : 'Verified', src: 'https://www.typeform.com/pricing/'}
        ];
        """,
        "faqs": [
            ("Does Typeform offer a HIPAA BAA on Plus or Business plans in 2026?", "No. Typeform only signs a HIPAA Business Associate Agreement (BAA) on custom Enterprise contracts, whereas Jotform includes a HIPAA BAA on its self-serve Gold plan at $99/month billed annually ($1,188/year)."),
            ("How many monthly submissions are included in Jotform Gold vs. Typeform Business?", "Both Jotform Gold ($99/mo annual) and Typeform Business ($83/mo annual) include 10,000 monthly submissions, but only Jotform Gold includes HIPAA compliance and signed BAA at that price.")
        ]
    },
    {
        "rel": "compare/close-crm-vs-hubspot-sales-hub-5-to-20-reps/index.html",
        "slug": "/compare/close-crm-vs-hubspot-sales-hub-5-to-20-reps/",
        "title": "Close CRM vs HubSpot True Year-1 Cost (2026) – saasbill.io",
        "desc": "Compare the 2026 true cost and Year-1 price of Close CRM ($0 onboarding, built-in calling) vs. HubSpot Sales Hub Pro ($90/seat/mo + $1,500 onboarding fee) for 5–20 reps.",
        "summary_id": "ch-summary",
        "h1": "Close CRM vs. HubSpot Sales Hub for 5&ndash;20 Reps (2026): True Year-1 Cost",
        "lead": "For an 8-rep sales team in 2026, HubSpot Sales Hub Professional costs $10,140 in Year 1 ($90/seat/month annual plus a mandatory $1,500 onboarding fee), compared with $3,360/year on Close CRM Essentials ($35/seat/month) or $9,504/year on Close CRM Growth ($99/seat/month with $0 onboarding and built-in VoIP calling &amp; SMS) (sources: HubSpot &amp; Close official pricing pages, verified Oct 2026).",
        "ctrl_label": "Sales Reps (Seats)",
        "ctrl_min": 1, "ctrl_max": 25, "ctrl_step": 1, "ctrl_val": 8, "ctrl_unit": "sales reps",
        "opt_label": "Close CRM Tier Comparison",
        "opt1_val": "essentials", "opt1_text": "Close Essentials ($35/seat/mo) vs. HubSpot Sales Pro",
        "opt2_val": "growth", "opt2_text": "Close Growth ($99/seat/mo · AI & Sequences) vs. HubSpot Sales Pro",
        "winner_name": "Close CRM ($0 Mandatory Onboarding)",
        "winner_url": "https://refer.close.com/3k5hp07b8soi-fetl0j",
        "winner_cta": "View Close pricing",
        "winner_vendor": "close-crm",
        "after_summary_html": '<p class="summary-interpretation"><a href="../close-vs-pipedrive-year-1-cost-calculator/" data-track="internal-audit">Comparing Close with Pipedrive instead? Include calling costs &rarr;</a></p>',
        "js_logic": """
        const vol = parseInt(document.getElementById('p-slider').value, 10);
        const mode = document.getElementById('p-select').value;
        document.getElementById('p-slider-val').textContent = vol + ' sales reps';
        const closeRate = mode === 'essentials' ? 35 : 99;
        const closeYr = vol * closeRate * 12;
        const hsSeatsYr = vol * 90 * 12;
        const hsYr = hsSeatsYr + 1500;
        const pipeYr = vol * __PD_PREMIUM_ANNUAL__ * 12;
        const saved = Math.max(0, hsYr - closeYr);
        const rows = [
          {name: mode === 'essentials' ? 'Close CRM (Essentials)' : 'Close CRM (Growth)', plan: '$' + closeRate + '/seat/mo annual', base: '$' + closeYr.toLocaleString('en-US') + '/yr', hidden: '$0 mandatory onboarding', total: '$' + closeYr.toLocaleString('en-US') + '/yr', url: 'https://refer.close.com/3k5hp07b8soi-fetl0j', cta: 'View Close pricing', vendor: 'close-crm', status: 'Verified', src: 'https://www.close.com/pricing'},
          {name: 'Pipedrive CRM (__PD_PREMIUM_LABEL__)', plan: '$__PD_PREMIUM_ANNUAL__/seat/mo annual', base: '$' + pipeYr.toLocaleString('en-US') + '/yr', hidden: '$0 onboarding (add-ons extra)', total: '$' + pipeYr.toLocaleString('en-US') + '/yr', url: 'https://www.pipedrive.com/en/pricing', cta: 'View Pipedrive pricing', vendor: 'pipedrive-crm', status: 'Verified', src: 'https://www.pipedrive.com/en/pricing'},
          {name: 'HubSpot Sales Hub Professional', plan: '$90/seat/mo annual', base: '$' + hsSeatsYr.toLocaleString('en-US') + '/yr', hidden: '+$1,500 mandatory onboarding fee', total: '$' + hsYr.toLocaleString('en-US') + '/yr', url: 'https://www.hubspot.com/pricing/sales', cta: 'View HubSpot pricing', vendor: 'hubspot-sales-pro', status: 'Verified', src: 'https://www.hubspot.com/pricing/sales'}
        ];
        """,
        "faqs": [
            ("Does Close CRM charge an onboarding or implementation fee?", "No. Close CRM charges $0 mandatory onboarding across Essentials ($35/seat/mo annual), Growth ($99/seat/mo annual), and Scale ($139/seat/mo annual), and includes built-in VoIP calling and SMS capabilities."),
            ("What is HubSpot Sales Hub Professional's mandatory onboarding fee in 2026?", "HubSpot Sales Hub Professional requires a mandatory one-time $1,500 onboarding fee ($3,500 on Sales Hub Enterprise) in addition to $90/seat/month billed annually.")
        ]
    },
    {
        "rel": "pricing/stripe-billing-0-7-percent-recurring-tax-calculator/index.html",
        "slug": "/pricing/stripe-billing-0-7-percent-recurring-tax-calculator/",
        "title": "Stripe Billing 0.7% Fee & True Cost (2026) – saasbill.io",
        "desc": "Calculate the 2026 true cost and Year-1 fee of Stripe Billing (0.7% recurring fee) + Stripe Tax (0.5%) + 2.9% + 30¢ card processing vs. Whop (2.7% + 30¢) and Paddle.",
        "summary_id": "sb-summary",
        "h1": "Stripe Billing 0.7% Recurring Revenue Tax &amp; Chargeback Cost Calculator (2026)",
        "lead": "In 2026, Stripe charges an extra 0.7% on recurring subscription volume (Stripe Billing) plus 0.5% for automated tax calculation (Stripe Tax) on top of 2.9% + $0.30 card processing, pushing effective recurring take rates to ~4.1% + $0.30 per charge versus 2.7% + $0.30 base card processing on Whop (sources: Stripe, Whop &amp; Paddle pricing pages, verified Oct 2026).",
        "ctrl_label": "Monthly Recurring Revenue (MRR)",
        "ctrl_min": 5000, "ctrl_max": 150000, "ctrl_step": 5000, "ctrl_val": 40000, "ctrl_unit": "MRR ($/mo)",
        "opt_label": "Automated Tax & Invoicing Stack",
        "opt1_val": "full", "opt1_text": "Include Stripe Billing (+0.7%) & Automated Tax (+0.5%)",
        "opt2_val": "billing_only", "opt2_text": "Stripe Billing (+0.7%) Only · No Automated Tax",
        "winner_name": "Whop Payments (2.7% + 30¢ Base Processing)",
        "winner_url": "https://whop.com/sell?a=baggyprairieae",
        "winner_cta": "View Whop Payments pricing",
        "winner_vendor": "whop-payments",
        "extra_controls": """
    <div class="control-group">
      <label for="sb-dispute-rate">Subscription dispute / chargeback rate: <span class="val-pill" id="sb-dispute-val">0.50%</span></label>
      <input type="range" id="sb-dispute-rate" min="0.0" max="2.0" step="0.05" value="0.50" data-track="calculator-control" data-control="dispute-rate" />
    </div>
""",
        "extra_listener_ids": ["sb-dispute-rate"],
        "extra_script": """
function calcStripeDisputes(mrr, txCount, disputePct) {
  const disputes = Math.round(txCount * 12 * (disputePct / 100));
  const aov = txCount > 0 ? mrr / txCount : 50;
  const disputed = Math.round(disputes * aov);
  const fees = disputes * 15;
  const counter = disputes * 15;
  const drain = disputed + fees + counter;
  const recovered = Math.round(disputed * 0.65);
  const successFee = Math.round(recovered * 0.25);
  const net = recovered - successFee;
  return { disputes: disputes, disputed: disputed, fees: fees, counter: counter, drain: drain, recovered: recovered, successFee: successFee, net: net };
}
""",
        "js_logic": """
        const mrr = parseInt(document.getElementById('p-slider').value, 10);
        const mode = document.getElementById('p-select').value;
        const disputePct = parseFloat(document.getElementById('sb-dispute-rate').value);
        document.getElementById('p-slider-val').textContent = '$' + mrr.toLocaleString('en-US') + '/mo MRR';
        document.getElementById('sb-dispute-val').textContent = disputePct.toFixed(2) + '%';
        const txCount = Math.round(mrr / 50);
        const cb = calcStripeDisputes(mrr, txCount, disputePct);
        const stripeBaseYr = Math.round((mrr * 0.029 + txCount * 0.30) * 12);
        const stripeHiddenRate = mode === 'full' ? (0.007 + 0.005) : 0.007;
        const stripeHiddenYr = Math.round(mrr * stripeHiddenRate * 12);
        const stripeYr = stripeBaseYr + stripeHiddenYr + cb.drain;
        const whopBaseYr = Math.round((mrr * 0.027 + txCount * 0.30) * 12);
        const whopHiddenYr = mode === 'full' ? Math.round(mrr * 0.008 * 12) : 0;
        const whopYr = whopBaseYr + whopHiddenYr;
        const paddleYr = Math.round((mrr * 0.05 + txCount * 0.50) * 12);
        const saved = Math.max(0, stripeYr - whopYr);
        const rows = [
          {name: 'Whop Payments', plan: '2.7% + $0.30 per card charge', base: '$' + whopBaseYr.toLocaleString('en-US') + '/yr', hidden: whopHiddenYr > 0 ? '+$' + whopHiddenYr.toLocaleString('en-US') + '/yr orchestration' : '$0 subscription billing tax', total: '$' + whopYr.toLocaleString('en-US') + '/yr', url: 'https://whop.com/sell?a=baggyprairieae', cta: 'View Whop Payments pricing', vendor: 'whop-payments', status: 'Verified', src: 'https://whop.com/sell'},
          {name: 'Stripe (Cards + Billing + Tax)', plan: '2.9% + $0.30 base card rate', base: '$' + stripeBaseYr.toLocaleString('en-US') + '/yr', hidden: '+$' + stripeHiddenYr.toLocaleString('en-US') + '/yr (0.7% Billing' + (mode === 'full' ? ' + 0.5% Tax' : '') + ') + $' + cb.drain.toLocaleString('en-US') + '/yr chargeback drain', total: '$' + stripeYr.toLocaleString('en-US') + '/yr', url: 'https://stripe.com/pricing', cta: 'View Stripe pricing', vendor: 'stripe-payments', status: 'Verified', src: 'https://stripe.com/pricing'},
          {name: 'Paddle (Merchant of Record)', plan: '5.0% + $0.50 all-in MoR', base: '$' + paddleYr.toLocaleString('en-US') + '/yr', hidden: 'Global tax incl. (non-portable card vault)', total: '$' + paddleYr.toLocaleString('en-US') + '/yr', url: 'https://www.paddle.com/pricing', cta: 'View Paddle pricing', vendor: 'paddle-mor', status: 'Verified', src: 'https://www.paddle.com/pricing'},
          {name: 'Chargeflow (Automated Dispute Recovery)', plan: '25% of recovered disputes ($0/mo fixed)', base: '$0/yr base fee', hidden: 'Pay-on-performance add-on for Stripe/Shopify: 65% benchmark recovery rate on disputed volume ($0 fee on unrecovered disputes)', total: 'Saves $' + cb.net.toLocaleString('en-US') + '/yr net', url: 'https://www.chargeflow.io/', cta: 'View Chargeflow pricing', vendor: 'chargeflow', status: 'Verified', src: 'https://www.chargeflow.io/pricing', ctaLocation: 'table-row'}
        ];
        const sbMathText = 'Charges/mo = MRR / $50 = ' + txCount.toLocaleString('en-US') + '. Disputes/yr = ' + txCount.toLocaleString('en-US') + ' x 12 x ' + disputePct.toFixed(2) + '% = ' + cb.disputes.toLocaleString('en-US') + '. Disputed MRR = ' + cb.disputes.toLocaleString('en-US') + ' x $' + (txCount ? Math.round(mrr / txCount) : 50) + ' = $' + cb.disputed.toLocaleString('en-US') + '. Stripe dispute fees = ' + cb.disputes.toLocaleString('en-US') + ' x $15 = $' + cb.fees.toLocaleString('en-US') + '. Counter fee / manual prep = ' + cb.disputes.toLocaleString('en-US') + ' x $15 = $' + cb.counter.toLocaleString('en-US') + '. Annual chargeback and dispute drain = $' + cb.drain.toLocaleString('en-US') + '. Stripe Year-1 true cost adds that drain on top of card, Billing, and Tax fees ($' + stripeHiddenYr.toLocaleString('en-US') + '/yr). Paddle processing on this volume is $' + paddleYr.toLocaleString('en-US') + '/yr before disputes.';
        customSummaryHtml = '<div class="summary-card result-card card-lowest"><div class="summary-label">Best value: Whop Payments</div><div class="summary-metric">$' + whopYr.toLocaleString('en-US') + ' / yr</div><div class="summary-scenario">Based on $' + mrr.toLocaleString('en-US') + '/mo MRR</div><div class="summary-breakdown">' + rows[0].plan + '. ' + rows[0].hidden + '.</div><div class="summary-actions"><a class="btn-cta" href="https://whop.com/sell?a=baggyprairieae" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="whop-payments" data-cta-location="summary-card">View Whop Payments pricing &rarr;</a></div></div>'
          + '<div class="summary-card result-card card-highest"><div class="summary-label">Stripe / Paddle hidden cost breakdown</div><div class="summary-metric">$' + stripeYr.toLocaleString('en-US') + ' / yr</div><div class="summary-scenario">Based on $' + mrr.toLocaleString('en-US') + '/mo MRR and a ' + disputePct.toFixed(2) + '% dispute rate</div><div class="summary-breakdown">Stripe card + Billing + Tax $' + (stripeBaseYr + stripeHiddenYr).toLocaleString('en-US') + '/yr, plus $' + cb.drain.toLocaleString('en-US') + '/yr chargeback drain. Paddle processing $' + paddleYr.toLocaleString('en-US') + '/yr.</div><p class="summary-caveat"><strong>Hidden Cost Highlight:</strong> The dispute drain is disputed MRR plus a $15 dispute fee and a $15 counter fee on every dispute.</p><details class="math-drawer"><summary>Show calculation</summary><div class="math-drawer-body">' + sbMathText + '</div></details></div>'
          + '<div class="summary-card result-card card-lowest"><div class="summary-label">Dispute recovery: Chargeflow pay-on-performance</div><div class="summary-metric">$' + cb.net.toLocaleString('en-US') + ' net / yr</div><div class="summary-scenario">65% planning win rate, 25% success fee, $0/mo fixed</div><div class="summary-breakdown">Gross recovered $' + cb.recovered.toLocaleString('en-US') + ' minus a $' + cb.successFee.toLocaleString('en-US') + ' success fee.</div><details class="math-drawer"><summary>Show calculation</summary><div class="math-drawer-body">65% of $' + cb.disputed.toLocaleString('en-US') + ' = $' + cb.recovered.toLocaleString('en-US') + '. Success fee 25% = $' + cb.successFee.toLocaleString('en-US') + '. Net recovered = $' + cb.net.toLocaleString('en-US') + '. The 65% win rate is a planning benchmark.</div></details><div class="summary-actions"><a id="sb-cf-cta" class="btn-secondary" href="https://www.chargeflow.io/" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="chargeflow" data-cta-location="summary-card">Recover $' + cb.net.toLocaleString('en-US') + '/yr net with Chargeflow &rarr;</a><a class="summary-audit-link" href="../../chargeback-fee-and-recovery-calculator/">Open the full chargeback calculator &rarr;</a></div></div>';
        """,
        "faqs": [
            ("How much does Stripe Billing charge for recurring subscriptions in 2026?", "Stripe Billing pay-as-you-go charges 0.7% of recurring subscription volume on top of standard 2.9% + $0.30 card processing fees. Adding Stripe Tax adds another 0.5% per transaction."),
            ("Does Whop charge an extra 0.7% fee on recurring subscriptions?", "No. Whop's domestic card processing starts at 2.7% + $0.30 without a separate 0.7% recurring billing surcharge.")
        ]
    },
    {
        "rel": "pricing/docusign-envelope-allowance-and-api-overage-calculator/index.html",
        "slug": "/pricing/docusign-envelope-allowance-and-api-overage-calculator/",
        "title": "DocuSign 100-Envelope Cap & True Cost (2026) – saasbill.io",
        "desc": "Calculate the 2026 true cost and Year-1 overage fees of DocuSign's 100 envelopes/user/year cap vs. Jotform Sign and PandaDoc unlimited e-signature plans.",
        "summary_id": "ds-summary",
        "h1": "DocuSign 100-Envelope Cap Calculator (2026): True Year-1 Cost vs. Jotform Sign &amp; PandaDoc",
        "lead": "DocuSign Standard ($25/user/month annual) and Business Pro ($40/user/month annual) cap every user at just 100 sent envelopes per year (~8/month) in 2026 and charging ~$2.50 per extra envelope beyond your allowance, whereas Jotform Gold ($99/month flat) and PandaDoc Business ($49/user/month) include high-volume e-signatures without per-envelope overage penalties (sources: DocuSign, PandaDoc &amp; Jotform pricing pages, verified Oct 2026).",
        "ctrl_label": "Monthly Envelopes Sent (Total Team)",
        "ctrl_min": 20, "ctrl_max": 400, "ctrl_step": 20, "ctrl_val": 120, "ctrl_unit": "envelopes/mo",
        "opt_label": "Team Size & Compliance",
        "opt1_val": "5_users", "opt1_text": "5 Team Senders (500 DocuSign Envelopes/Yr Included)",
        "opt2_val": "2_users", "opt2_text": "2 Team Senders (200 DocuSign Envelopes/Yr Included)",
        "winner_name": "Jotform Sign / Gold (Flat Team Pricing)",
        "winner_url": "https://www.jotform.com/hipaa/pricing/?partner=saasbill",
        "winner_cta": "View Jotform HIPAA pricing",
        "winner_vendor": "jotform-hipaa",
        "js_logic": """
        const envMo = parseInt(document.getElementById('p-slider').value, 10);
        const mode = document.getElementById('p-select').value;
        document.getElementById('p-slider-val').textContent = envMo + ' envelopes/mo (' + (envMo * 12).toLocaleString('en-US') + '/yr)';
        const users = mode === '5_users' ? 5 : 2;
        const envYr = envMo * 12;
        const dsIncluded = users * 100;
        const dsOverageCount = Math.max(0, envYr - dsIncluded);
        const dsBaseYr = users * 40 * 12;
        const dsHiddenYr = Math.round(dsOverageCount * 2.50);
        const dsYr = dsBaseYr + dsHiddenYr;
        const jfYr = 99 * 12;
        const pdYr = users * 49 * 12;
        const saved = Math.max(0, dsYr - jfYr);
        const rows = [
          {name: 'Jotform Sign (Gold HIPAA Plan)', plan: '$99/mo flat annual', base: '$' + jfYr.toLocaleString('en-US') + '/yr', hidden: '$0 per-envelope overage fees', total: '$' + jfYr.toLocaleString('en-US') + '/yr', url: 'https://www.jotform.com/hipaa/pricing/?partner=saasbill', cta: 'View Jotform HIPAA pricing', vendor: 'jotform-hipaa', status: 'Verified', src: 'https://www.jotform.com/hipaa/pricing/'},
          {name: 'PandaDoc (Business)', plan: '$49/seat/mo annual (' + users + ' seats)', base: '$' + pdYr.toLocaleString('en-US') + '/yr', hidden: '$0 envelope cap on manual sends', total: '$' + pdYr.toLocaleString('en-US') + '/yr', url: 'https://www.pandadoc.com/pricing/', cta: 'View PandaDoc pricing', vendor: 'pandadoc', status: 'Verified', src: 'https://www.pandadoc.com/pricing/'},
          {name: 'DocuSign (Business Pro)', plan: '$40/user/mo annual (' + users + ' users)', base: '$' + dsBaseYr.toLocaleString('en-US') + '/yr', hidden: dsHiddenYr > 0 ? '+$' + dsHiddenYr.toLocaleString('en-US') + '/yr (' + dsOverageCount + ' extra envelopes @ $2.50)' : '$0 (within ' + dsIncluded + '/yr cap)', total: '$' + dsYr.toLocaleString('en-US') + '/yr', url: 'https://www.docusign.com/products-and-pricing', cta: 'View DocuSign pricing', vendor: 'docusign', status: 'Verified', src: 'https://www.docusign.com/products-and-pricing'}
        ];
        """,
        "faqs": [
            ("How many envelopes are included in DocuSign Standard and Business Pro in 2026?", "Both DocuSign Standard ($25/user/mo annual) and Business Pro ($40/user/mo annual) include an annual allowance of 100 sent envelopes per user per year (about 8 envelopes per month)."),
            ("Which alternatives avoid per-envelope overage fees?", "Jotform Sign (included in Jotform Gold at $99/mo flat with HIPAA compliance) and PandaDoc Business ($49/seat/mo annual) allow high-volume e-signature workflows without a 100-envelope annual cap.")
        ]
    },
    {
        "rel": "pricing/gong-io-platform-fee-and-seat-minimum-calculator/index.html",
        "slug": "/pricing/gong-io-platform-fee-and-seat-minimum-calculator/",
        "title": "Gong.io $5,000 Platform Fee & True Cost – saasbill.io",
        "desc": "Calculate the 2026 Gong.io true cost and Year-1 contract price ($5,000 base platform fee + ~$1,600/seat/yr + separate CRM cost) vs. Close CRM all-in-one calling.",
        "summary_id": "gong-summary",
        "h1": "Gong.io Platform Fee &amp; Seat Calculator (2026): True Year-1 Cost vs. Close CRM",
        "lead": "Based on 2026 contract benchmarks, Gong.io charges a mandatory $5,000/year base platform fee plus $1,360&ndash;$1,600 per user/year (and requires a separate CRM license on top), bringing an 8-rep team's Year-1 total to ~$23,560/year versus $9,504/year all-in on Close CRM Growth with built-in VoIP calling, recording, and AI call transcripts (sources: public procurement benchmarks &amp; Close pricing page, verified Oct 2026).",
        "ctrl_label": "Sales Reps (Recorded Seats)",
        "ctrl_min": 3, "ctrl_max": 25, "ctrl_step": 1, "ctrl_val": 8, "ctrl_unit": "sales reps",
        "opt_label": "Include Separate CRM License for Gong?",
        "opt1_val": "with_crm", "opt1_text": "Yes: Include Separate CRM ($90/seat/mo HubSpot Sales Pro)",
        "opt2_val": "gong_only", "opt2_text": "No: Calculate Gong.io Standalone Contract Only",
        "winner_name": "Close CRM Growth (CRM + Calling + AI Transcripts)",
        "winner_url": "https://refer.close.com/3k5hp07b8soi-fetl0j",
        "winner_cta": "View Close pricing",
        "winner_vendor": "close-crm",
        "js_logic": """
        const reps = parseInt(document.getElementById('p-slider').value, 10);
        const mode = document.getElementById('p-select').value;
        document.getElementById('p-slider-val').textContent = reps + ' sales reps';
        const gongSeatsYr = reps * 1600;
        const crmExtraYr = mode === 'with_crm' ? (reps * 90 * 12) : 0;
        const gongHiddenYr = 5000 + crmExtraYr;
        const gongYr = gongSeatsYr + gongHiddenYr;
        const closeYr = reps * 99 * 12;
        const saved = Math.max(0, gongYr - closeYr);
        const rows = [
          {name: 'Close CRM (Growth + Built-In Calling)', plan: '$99/seat/mo annual', base: '$' + closeYr.toLocaleString('en-US') + '/yr', hidden: '$0 platform fee · CRM + VoIP included', total: '$' + closeYr.toLocaleString('en-US') + '/yr', url: 'https://refer.close.com/3k5hp07b8soi-fetl0j', cta: 'View Close pricing', vendor: 'close-crm', status: 'Verified', src: 'https://www.close.com/pricing'},
          {name: 'Gong.io (Enterprise Revenue Intelligence)', plan: '~$1,600/user/yr benchmark', base: '$' + gongSeatsYr.toLocaleString('en-US') + '/yr', hidden: '+$5,000 platform fee' + (crmExtraYr > 0 ? ' + $' + crmExtraYr.toLocaleString('en-US') + ' CRM' : ''), total: '$' + gongYr.toLocaleString('en-US') + '/yr', url: 'https://www.gong.io/pricing/', cta: 'View Gong pricing', vendor: 'gong-io', status: 'Estimated (Benchmark)', src: 'https://www.gong.io/pricing/'}
        ];
        """,
        "faqs": [
            ("How much is Gong.io's base platform fee in 2026?", "Procurement benchmarks show Gong.io typically charges a $5,000/year mandatory base platform fee plus $1,360 to $1,600 per recorded user per year on annual contracts."),
            ("Can Close CRM replace both a separate CRM and call recording tool for 5–20 reps?", "Yes. Close CRM Growth ($99/seat/mo annual) includes a full B2B sales CRM, built-in VoIP dialer, call recording, and AI call summaries with $0 base platform fee.")
        ]
    },
    {
        "rel": "exit/paypal-180-day-permanent-limitation-fund-recovery/index.html",
        "slug": "/exit/paypal-180-day-permanent-limitation-fund-recovery/",
        "title": "PayPal 180-Day Hold & True Cost (2026) – saasbill.io",
        "desc": "Calculate the 2026 true cost and working-capital impact of a PayPal 180-day permanent limitation hold and 3.49% + 49¢ fees vs. Whop multi-processor orchestration.",
        "summary_id": "pp-summary",
        "h1": "PayPal 180-Day Hold &amp; Reserve Cost Calculator (2026)",
        "lead": "Under the 2026 PayPal US User Agreement, a permanent account limitation locks 100% of your held balance for up to 180 days on top of 3.49% + $0.49 commercial transaction fees and $15&ndash;$30 dispute fees, whereas routing checkouts through Whop (2.7% + $0.30 base) distributes volume across redundant payment processors (sources: PayPal User Agreement &amp; Whop pricing, verified Oct 2026).",
        "ctrl_label": "Monthly Checkout Volume (GMV)",
        "ctrl_min": 5000, "ctrl_max": 100000, "ctrl_step": 5000, "ctrl_val": 30000, "ctrl_unit": "GMV ($/mo)",
        "opt_label": "PayPal Reserve / Hold Scenario",
        "opt1_val": "hold_30", "opt1_text": "30% Rolling Reserve / Frozen Monthly Balance",
        "opt2_val": "hold_100", "opt2_text": "100% Monthly Balance Frozen (180-Day Limitation)",
        "winner_name": "Whop Payments (Multi-Processor Failover)",
        "winner_url": "https://whop.com/sell?a=baggyprairieae",
        "winner_cta": "View Whop Payments pricing",
        "winner_vendor": "whop-payments",
        "js_logic": """
        const gmv = parseInt(document.getElementById('p-slider').value, 10);
        const mode = document.getElementById('p-select').value;
        document.getElementById('p-slider-val').textContent = '$' + gmv.toLocaleString('en-US') + '/mo GMV';
        const tx = Math.round(gmv / 60);
        const ppFeeYr = Math.round((gmv * 0.0349 + tx * 0.49) * 12);
        const ppHeld = Math.round(gmv * (mode === 'hold_100' ? 1.0 : 0.30));
        const whopFeeYr = Math.round((gmv * 0.027 + tx * 0.30) * 12);
        const saved = Math.max(0, ppFeeYr - whopFeeYr) + ppHeld;
        const rows = [
          {name: 'Whop Payments (Multi-PSP Orchestration)', plan: '2.7% + $0.30 per card charge', base: '$' + whopFeeYr.toLocaleString('en-US') + '/yr fees', hidden: '$0 single-processor freeze (multi-PSP routing)', total: '$' + whopFeeYr.toLocaleString('en-US') + '/yr', url: 'https://whop.com/sell?a=baggyprairieae', cta: 'View Whop Payments pricing', vendor: 'whop-payments', status: 'Verified', src: 'https://whop.com/sell'},
          {name: 'Chargeflow (Automated Dispute Recovery)', plan: '25% performance-only rev-share', base: '$0 fixed monthly fee', hidden: 'Prevents >1.5% High-Volume Dispute tier', total: 'Pay on won disputes only', url: 'https://www.chargeflow.io/pricing', cta: 'View Chargeflow pricing', vendor: 'chargeflow', status: 'Verified', src: 'https://www.chargeflow.io/pricing'},
          {name: 'PayPal Commercial Checkout', plan: '3.49% + $0.49 per transaction', base: '$' + ppFeeYr.toLocaleString('en-US') + '/yr fees', hidden: '$' + ppHeld.toLocaleString('en-US') + ' cash locked up to 180 days', total: '$' + ppFeeYr.toLocaleString('en-US') + '/yr + $' + ppHeld.toLocaleString('en-US') + ' held', url: 'https://www.paypal.com/us/business/paypal-business-fees', cta: 'View PayPal fees', vendor: 'paypal', status: 'Verified', src: 'https://www.paypal.com/us/business/paypal-business-fees'}
        ];
        """,
        "faqs": [
            ("Why does PayPal hold funds for 180 days on a permanent limitation?", "Roughly 180 days matches the maximum card-network chargeback window (Visa and Mastercard allow cardholders up to 120–180 days to file a dispute). PayPal holds the balance as collateral until the chargeback liability window expires."),
            ("What is PayPal's High Volume Dispute Fee in 2026?", "PayPal charges a $15 Standard Dispute Fee, which doubles to a $30 High Volume Dispute Fee if your dispute rate reaches 1.5% or higher with more than 100 transactions in the prior three full months.")
        ]
    },
    # === 3 NEW HIGH-INTENT ANSWER-FIRST FAQ LANDING PAGES ===
    {
        "rel": "faq/does-hubspot-charge-onboarding-fees-2026/index.html",
        "slug": "/faq/does-hubspot-charge-onboarding-fees-2026/",
        "title": "Does HubSpot Charge Onboarding Fees (2026)? – saasbill.io",
        "desc": "Yes: HubSpot charges mandatory $1,500–$7,000 onboarding fees on Professional and Enterprise plans in 2026. Calculate your true Year-1 cost vs. Close CRM ($0 onboarding).",
        "summary_id": "faq-hs-summary",
        "h1": "Does HubSpot Charge Onboarding Fees in 2026? (Exact Fee Schedule &amp; Waivers)",
        "lead": "Yes. HubSpot charges a mandatory $1,500 onboarding fee for Sales Hub Professional ($3,500 for Enterprise) and a mandatory $3,000 onboarding fee for Marketing Hub Professional ($7,000 for Enterprise) in 2026 (source: HubSpot official pricing &amp; product catalog, verified Oct 2026).",
        "ctrl_label": "Sales / Marketing Team Seats",
        "ctrl_min": 1, "ctrl_max": 20, "ctrl_step": 1, "ctrl_val": 5, "ctrl_unit": "seats",
        "opt_label": "HubSpot Hub Edition",
        "opt1_val": "sales_pro", "opt1_text": "Sales Hub Professional ($90/seat/mo + $1,500 Onboarding)",
        "opt2_val": "marketing_pro", "opt2_text": "Marketing Hub Professional ($800/mo base + $3,000 Onboarding)",
        "winner_name": "Close CRM ($0 Mandatory Onboarding Fee)",
        "winner_url": "https://refer.close.com/3k5hp07b8soi-fetl0j",
        "winner_cta": "View Close pricing",
        "winner_vendor": "close-crm",
        "js_logic": """
        const seats = parseInt(document.getElementById('p-slider').value, 10);
        const mode = document.getElementById('p-select').value;
        document.getElementById('p-slider-val').textContent = seats + ' seats';
        const hsBaseYr = mode === 'sales_pro' ? (seats * 90 * 12) : ((800 + Math.max(0, seats - 3) * 45) * 12);
        const hsOnboard = mode === 'sales_pro' ? 1500 : 3000;
        const hsYr = hsBaseYr + hsOnboard;
        const closeYr = seats * 35 * 12;
        const saved = Math.max(0, hsYr - closeYr);
        const rows = [
          {name: 'Close CRM (Essentials)', plan: '$35/seat/mo annual', base: '$' + closeYr.toLocaleString('en-US') + '/yr', hidden: '$0 mandatory onboarding fee', total: '$' + closeYr.toLocaleString('en-US') + '/yr', url: 'https://refer.close.com/3k5hp07b8soi-fetl0j', cta: 'View Close pricing', vendor: 'close-crm', status: 'Verified', src: 'https://www.close.com/pricing'},
          {name: mode === 'sales_pro' ? 'HubSpot Sales Hub Pro' : 'HubSpot Marketing Hub Pro', plan: mode === 'sales_pro' ? '$90/seat/mo annual' : '$800/mo (3 seats) + $45/extra seat', base: '$' + hsBaseYr.toLocaleString('en-US') + '/yr', hidden: '+$' + hsOnboard.toLocaleString('en-US') + ' mandatory onboarding fee', total: '$' + hsYr.toLocaleString('en-US') + '/yr', url: 'https://www.hubspot.com/pricing', cta: 'View HubSpot pricing', vendor: 'hubspot-sales-pro', status: 'Verified', src: 'https://www.hubspot.com/pricing'}
        ];
        """,
        "faqs": [
            ("Can you waive HubSpot's $1,500 or $3,000 onboarding fee in 2026?", "HubSpot waives its direct onboarding fee only if you sign up through an accredited HubSpot Solutions Partner agency (who bills their own retainer) or negotiate a multi-hub annual contract at quarter-end."),
            ("Do HubSpot Starter plans charge an onboarding fee?", "No. HubSpot Starter ($15/seat/month annual) has $0 mandatory onboarding fee; mandatory onboarding starts on Professional and Enterprise tiers.")
        ]
    },
    {
        "rel": "faq/intercom-fin-ai-cost-calculator/index.html",
        "slug": "/faq/intercom-fin-ai-cost-calculator/",
        "title": "Intercom Fin AI True Cost Calculator (2026) – saasbill.io",
        "desc": "Intercom Fin AI costs $0.99 per resolved conversation in 2026 plus $29–$132/seat/mo. Calculate your true Year-1 AI support cost vs. Freshdesk and Help Scout.",
        "summary_id": "faq-ic-summary",
        "h1": "Intercom Fin AI Cost Calculator (2026): True Year-1 Price at $0.99/Resolution",
        "lead": "Intercom Fin AI costs $0.99 per resolved conversation in 2026 on top of mandatory helpdesk agent seat licenses ($29 to $132/seat/month annual), meaning 1,000 monthly AI resolutions add $990/month ($11,880/year) to your base subscription (source: Intercom official pricing page, verified Oct 2026).",
        "ctrl_label": "Monthly AI-Resolved Tickets",
        "ctrl_min": 100, "ctrl_max": 3000, "ctrl_step": 100, "ctrl_val": 1000, "ctrl_unit": "AI resolutions/mo",
        "opt_label": "Support Team Agent Seats",
        "opt1_val": "5_essential", "opt1_text": "5 Agents on Intercom Essential ($29/seat/mo annual)",
        "opt2_val": "5_advanced", "opt2_text": "5 Agents on Intercom Advanced ($85/seat/mo annual)",
        "winner_name": "Freshdesk (Predictable AI Session Packs)",
        "winner_url": "https://www.freshworks.com/freshdesk/pricing/",
        "winner_cta": "View Freshdesk pricing",
        "winner_vendor": "freshdesk-support",
        "js_logic": """
        const aiVol = parseInt(document.getElementById('p-slider').value, 10);
        const mode = document.getElementById('p-select').value;
        document.getElementById('p-slider-val').textContent = aiVol.toLocaleString('en-US') + ' AI resolutions/mo';
        const seatRate = mode === '5_essential' ? 29 : 85;
        const icBaseYr = 5 * seatRate * 12;
        const icAiYr = Math.round(aiVol * 0.99 * 12);
        const icYr = icBaseYr + icAiYr;
        const hsBaseYr = 5 * 45 * 12;
        const hsAiYr = Math.round(aiVol * 0.75 * 12);
        const hsYr = hsBaseYr + hsAiYr;
        const fdBaseYr = 5 * 19 * 12;
        const fdPacksYr = Math.max(0, Math.ceil((aiVol * 12 - 500) / 100)) * 49;
        const fdYr = fdBaseYr + fdPacksYr;
        const saved = Math.max(0, icYr - fdYr);
        const rows = [
          {name: 'Freshdesk Growth + Freddy AI', plan: '$19/agent/mo annual (5 agents)', base: '$' + fdBaseYr.toLocaleString('en-US') + '/yr', hidden: '+$' + fdPacksYr.toLocaleString('en-US') + '/yr ($49 per 100 AI sessions)', total: '$' + fdYr.toLocaleString('en-US') + '/yr', url: 'https://www.freshworks.com/freshdesk/pricing/', cta: 'View Freshdesk pricing', vendor: 'freshdesk-support', status: 'Verified', src: 'https://www.freshworks.com/freshdesk/pricing/'},
          {name: 'Help Scout Plus + AI Answers', plan: '$45/user/mo annual (5 users)', base: '$' + hsBaseYr.toLocaleString('en-US') + '/yr', hidden: '+$' + hsAiYr.toLocaleString('en-US') + '/yr ($0.75/resolution · hard cap available)', total: '$' + hsYr.toLocaleString('en-US') + '/yr', url: 'https://www.helpscout.com/pricing/', cta: 'View Help Scout pricing', vendor: 'help-scout-plus', status: 'Verified', src: 'https://www.helpscout.com/pricing/'},
          {name: 'Intercom + Fin AI ($0.99/res)', plan: '$' + seatRate + '/seat/mo annual (5 seats)', base: '$' + icBaseYr.toLocaleString('en-US') + '/yr', hidden: '+$' + icAiYr.toLocaleString('en-US') + '/yr ($0.99 per AI resolution)', total: '$' + icYr.toLocaleString('en-US') + '/yr', url: 'https://www.intercom.com/pricing', cta: 'View Intercom pricing', vendor: 'intercom-fin-ai', status: 'Verified', src: 'https://www.intercom.com/pricing'}
        ];
        """,
        "faqs": [
            ("What counts as a billable $0.99 Fin AI resolution in Intercom?", "Intercom bills $0.99 whenever a customer confirms Fin's answer solved their question or exits the conversation without requesting a human agent within the session window."),
            ("How does Help Scout's AI resolution pricing compare with Intercom Fin?", "Help Scout charges $0.75 per AI resolution (24% less than Intercom's $0.99) and lets admins set a hard monthly spending limit so AI costs never exceed budget.")
        ]
    },
    {
        "rel": "faq/stripe-vs-paddle-true-cost/index.html",
        "slug": "/faq/stripe-vs-paddle-true-cost/",
        "title": "Stripe vs Paddle vs Whop True Cost (2026) – saasbill.io",
        "desc": "Compare the 2026 true cost and Year-1 take rate of Stripe (2.9% + 0.7% Billing + 0.5% Tax) vs. Paddle (5% + 50¢ MoR) vs. Whop (2.7% + 30¢ with $0 billing tax).",
        "summary_id": "faq-sp-summary",
        "h1": "Stripe vs. Paddle vs. Whop True Cost &amp; Chargeback Calculator (2026)",
        "lead": "In 2026, Stripe's true recurring SaaS cost is 3.6% to 4.1% + $0.30 per charge once you add Stripe Billing (0.7%) and Stripe Tax (0.5%) to the 2.9% + $0.30 base card rate, compared with 5.0% + $0.50 all-in on Paddle (Merchant of Record) and 2.7% + $0.30 on Whop with $0 extra subscription billing tax (source: Stripe, Paddle, and Whop official pricing pages, verified Oct 2026).",
        "ctrl_label": "Monthly SaaS Revenue (GMV)",
        "ctrl_min": 5000, "ctrl_max": 150000, "ctrl_step": 5000, "ctrl_val": 50000, "ctrl_unit": "GMV ($/mo)",
        "opt_label": "International Card Share",
        "opt1_val": "domestic", "opt1_text": "Mostly Domestic Cards (0% International FX)",
        "opt2_val": "intl_40", "opt2_text": "40% International Cards (+1.5% Intl + 1% FX on Stripe/Whop)",
        "winner_name": "Whop Payments (Lowest Recurring Take Rate)",
        "winner_url": "https://whop.com/sell?a=baggyprairieae",
        "winner_cta": "View Whop Payments pricing",
        "winner_vendor": "whop-payments",
        "extra_controls": """
    <div class="control-group">
      <label for="sp-dispute-rate">Dispute / chargeback rate: <span class="val-pill" id="sp-dispute-val">0.50%</span></label>
      <input type="range" id="sp-dispute-rate" min="0.0" max="2.0" step="0.05" value="0.50" data-track="calculator-control" data-control="dispute-rate" />
    </div>
""",
        "extra_listener_ids": ["sp-dispute-rate"],
        "extra_script": """
function calcProcessorDisputes(gmv, tx, disputePct, fee) {
  const disputes = Math.round(tx * 12 * (disputePct / 100));
  const aov = tx > 0 ? gmv / tx : 50;
  const disputed = Math.round(disputes * aov);
  const unrecovered = Math.round(disputed * 0.80);
  const fees = disputes * fee;
  const drain = unrecovered + fees;
  const recovered = Math.round(disputed * 0.65);
  const successFee = Math.round(recovered * 0.25);
  const net = recovered - successFee;
  return { disputes: disputes, disputed: disputed, unrecovered: unrecovered, fees: fees, drain: drain, recovered: recovered, successFee: successFee, net: net };
}
""",
        "js_logic": """
        const gmv = parseInt(document.getElementById('p-slider').value, 10);
        const mode = document.getElementById('p-select').value;
        const disputePct = parseFloat(document.getElementById('sp-dispute-rate').value);
        document.getElementById('p-slider-val').textContent = '$' + gmv.toLocaleString('en-US') + '/mo GMV';
        document.getElementById('sp-dispute-val').textContent = disputePct.toFixed(2) + '%';
        const tx = Math.round(gmv / 50);
        const intlMult = mode === 'intl_40' ? (0.40 * 0.025) : 0;
        const stripeCb = calcProcessorDisputes(gmv, tx, disputePct, 15);
        const paddleCb = calcProcessorDisputes(gmv, tx, disputePct, 20);
        const whopBaseYr = Math.round((gmv * 0.027 + tx * 0.30) * 12);
        const whopHiddenYr = Math.round(gmv * intlMult * 12);
        const whopYr = whopBaseYr + whopHiddenYr;
        const stripeBaseYr = Math.round((gmv * 0.029 + tx * 0.30) * 12);
        const stripeHiddenYr = Math.round(gmv * (0.007 + 0.005 + intlMult) * 12);
        const stripeYr = stripeBaseYr + stripeHiddenYr + stripeCb.drain;
        const paddleYr = Math.round((gmv * 0.05 + tx * 0.50) * 12) + paddleCb.drain;
        const saved = Math.max(0, paddleYr - whopYr);
        const rows = [
          {name: 'Whop Payments', plan: '2.7% + $0.30 base domestic rate', base: '$' + whopBaseYr.toLocaleString('en-US') + '/yr', hidden: whopHiddenYr > 0 ? '+$' + whopHiddenYr.toLocaleString('en-US') + '/yr intl/FX' : '$0 subscription billing tax', total: '$' + whopYr.toLocaleString('en-US') + '/yr', url: 'https://whop.com/sell?a=baggyprairieae', cta: 'View Whop Payments pricing', vendor: 'whop-payments', status: 'Verified', src: 'https://whop.com/sell'},
          {name: 'Stripe (Cards + Billing + Tax)', plan: '2.9% + $0.30 base card rate', base: '$' + stripeBaseYr.toLocaleString('en-US') + '/yr', hidden: '+$' + stripeHiddenYr.toLocaleString('en-US') + '/yr billing/tax + $' + stripeCb.drain.toLocaleString('en-US') + '/yr chargebacks ($15/dispute + 80% unrecovered sales)', total: '$' + stripeYr.toLocaleString('en-US') + '/yr', url: 'https://stripe.com/pricing', cta: 'View Stripe pricing', vendor: 'stripe-payments', status: 'Verified', src: 'https://stripe.com/pricing'},
          {name: 'Paddle (Merchant of Record)', plan: '5.0% + $0.50 all-in MoR rate', base: '$' + Math.round((gmv * 0.05 + tx * 0.50) * 12).toLocaleString('en-US') + '/yr', hidden: 'Global VAT handled + $' + paddleCb.drain.toLocaleString('en-US') + '/yr chargebacks ($20/dispute + 80% unrecovered sales)', total: '$' + paddleYr.toLocaleString('en-US') + '/yr', url: 'https://www.paddle.com/pricing', cta: 'View Paddle pricing', vendor: 'paddle-mor', status: 'Verified', src: 'https://www.paddle.com/pricing'},
          {name: 'Chargeflow (Automated Dispute Recovery)', plan: '25% of recovered disputes ($0/mo fixed)', base: '$0/yr base fee', hidden: 'Pay-on-performance add-on for Stripe/Shopify: 65% benchmark recovery rate on disputed volume ($0 fee on unrecovered disputes)', total: 'Saves $' + stripeCb.net.toLocaleString('en-US') + '/yr net', url: 'https://www.chargeflow.io/', cta: 'View Chargeflow pricing', vendor: 'chargeflow', status: 'Verified', src: 'https://www.chargeflow.io/pricing', ctaLocation: 'table-row'}
        ];
        const spMathText = 'Charges/mo = GMV / $50 = ' + tx.toLocaleString('en-US') + '. Disputes/yr = ' + tx.toLocaleString('en-US') + ' x 12 x ' + disputePct.toFixed(2) + '% = ' + stripeCb.disputes.toLocaleString('en-US') + '. Disputed sales = $' + stripeCb.disputed.toLocaleString('en-US') + '. Unrecovered at a 20% manual win rate (80%) = $' + stripeCb.unrecovered.toLocaleString('en-US') + '. Stripe dispute fees = ' + stripeCb.disputes.toLocaleString('en-US') + ' x $15 = $' + stripeCb.fees.toLocaleString('en-US') + '. Stripe annual chargeback line = $' + stripeCb.drain.toLocaleString('en-US') + '. Paddle dispute fees = ' + paddleCb.disputes.toLocaleString('en-US') + ' x $20 = $' + paddleCb.fees.toLocaleString('en-US') + '. Paddle annual chargeback line = $' + paddleCb.drain.toLocaleString('en-US') + '.';
        customSummaryHtml = '<div class="summary-card result-card card-lowest"><div class="summary-label">Best value: Whop Payments</div><div class="summary-metric">$' + whopYr.toLocaleString('en-US') + ' / yr</div><div class="summary-scenario">Based on $' + gmv.toLocaleString('en-US') + '/mo GMV</div><div class="summary-breakdown">' + rows[0].hidden + '.</div><div class="summary-actions"><a class="btn-cta" href="https://whop.com/sell?a=baggyprairieae" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="whop-payments" data-cta-location="summary-card">View Whop Payments pricing &rarr;</a></div></div>'
          + '<div class="summary-card result-card card-highest"><div class="summary-label">Stripe / Paddle hidden cost breakdown</div><div class="summary-metric">$' + stripeYr.toLocaleString('en-US') + ' / yr Stripe</div><div class="summary-scenario">Based on $' + gmv.toLocaleString('en-US') + '/mo GMV and a ' + disputePct.toFixed(2) + '% dispute rate</div><div class="summary-breakdown">Stripe chargeback line $' + stripeCb.drain.toLocaleString('en-US') + '/yr ($15/dispute + 80% unrecovered). Paddle chargeback line $' + paddleCb.drain.toLocaleString('en-US') + '/yr ($20/dispute + 80% unrecovered). Paddle all-in $' + paddleYr.toLocaleString('en-US') + '/yr.</div><p class="summary-caveat"><strong>Hidden Cost Highlight:</strong> Dispute fees sit on top of the processing rate, and 80% of disputed sales stay lost at a 20% manual win rate.</p><details class="math-drawer"><summary>Show calculation</summary><div class="math-drawer-body">' + spMathText + '</div></details></div>'
          + '<div class="summary-card result-card card-lowest"><div class="summary-label">Dispute recovery: Chargeflow pay-on-performance</div><div class="summary-metric">$' + stripeCb.net.toLocaleString('en-US') + ' net / yr</div><div class="summary-scenario">65% planning win rate, 25% success fee, $0/mo fixed</div><div class="summary-breakdown">Gross recovered $' + stripeCb.recovered.toLocaleString('en-US') + ' minus a $' + stripeCb.successFee.toLocaleString('en-US') + ' success fee.</div><details class="math-drawer"><summary>Show calculation</summary><div class="math-drawer-body">65% of $' + stripeCb.disputed.toLocaleString('en-US') + ' = $' + stripeCb.recovered.toLocaleString('en-US') + '. Success fee 25% = $' + stripeCb.successFee.toLocaleString('en-US') + '. Net recovered = $' + stripeCb.net.toLocaleString('en-US') + '. The 65% win rate is a planning benchmark.</div></details><div class="summary-actions"><a id="sp-cf-cta" class="btn-secondary" href="https://www.chargeflow.io/" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="chargeflow" data-cta-location="summary-card">Recover $' + stripeCb.net.toLocaleString('en-US') + '/yr net with Chargeflow &rarr;</a><a class="summary-audit-link" href="../../chargeback-fee-and-recovery-calculator/">Open the full chargeback calculator &rarr;</a></div></div>';
        """,
        "faqs": [
            ("When is Paddle cheaper than Stripe in 2026?", "Paddle's 5% + $0.50 all-in Merchant of Record rate covers global VAT remittance and compliance liability, which can save accounting overhead for micro-SaaS teams selling globally, though Stripe (3.6%–4.1% + $0.30) and Whop (2.7% + $0.30) leave higher net revenue."),
            ("Can you export subscriber card tokens from Paddle to Stripe or Whop?", "Paddle owns the merchant-of-record relationship, so migrating off Paddle requires support-assisted token migration and freezes if an account is terminated for risk.")
        ]
    }
]


def build_all():
    for p in PAGES:
        listener_ids = ["p-slider", "p-select"] + p.get("extra_listener_ids", [])
        listener_js = ", ".join("'" + i + "'" for i in listener_ids)
        controls = f"""
        <div class="wb-control-item">
          <label class="wb-control-label" for="p-slider">{p["ctrl_label"]}</label>
          <div class="wb-slider-row wb-slider-row-wide">
            <input type="range" id="p-slider" min="{p["ctrl_min"]}" max="{p["ctrl_max"]}" step="{p["ctrl_step"]}" value="{p["ctrl_val"]}" aria-label="{p["ctrl_label"]}" data-track="calculator-control" data-control="primary-slider" />
            <span class="wb-slider-val" id="p-slider-val">{p["ctrl_val"]} {p["ctrl_unit"]}</span>
          </div>
        </div>
        <div class="wb-control-item">
          <div class="control-group">
            <label for="p-select">{p["opt_label"]}</label>
            <select id="p-select" data-track="calculator-control" data-control="primary-select">
              <option value="{p["opt1_val"]}" selected>{p["opt1_text"]}</option>
              <option value="{p["opt2_val"]}">{p["opt2_text"]}</option>
            </select>
          </div>
        </div>
        {p.get("extra_controls", "")}
"""
        shell = render_workbench(
            controls,
            cta_href=p["winner_url"],
            cta_label=p["winner_cta"],
            cta_vendor=p["winner_vendor"],
        )
        body = f"""
<section class="hero editorial-hero editorial-hero-wrap">
  <h1>{p["h1"]}</h1>
  <p class="lead">{p["lead"]}</p>
</section>
{shell}
<section aria-label="Comparison">
  <div class="summary-strip" id="{p["summary_id"]}"></div>
  {p.get("after_summary_html", "")}
  {p.get("extra_html", "")}
  <div class="table-wrap editorial-gap-table mobile-cards">
    <table>
      <thead>
        <tr>
          <th>Platform</th>
          <th>Advertised Plan</th>
          <th>Base Cost</th>
          <th>Hidden Cost Highlight</th>
          <th>True Year-1 Cost</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody id="p-tbody"></tbody>
    </table>
  </div>
</section>

<script>
{p.get("extra_script", "")}
{WORKBENCH_JS}
function runPageCalc() {{
  var customSummaryHtml;
  {p["js_logic"].replace("__PD_PREMIUM_ANNUAL__", PD_PREMIUM_ANNUAL).replace("__PD_PREMIUM_LABEL__", PD_PREMIUM_LABEL)}
  document.getElementById('{p["summary_id"]}').innerHTML = (typeof customSummaryHtml === 'string' && customSummaryHtml) ? customSummaryHtml : `
    <div class="summary-card result-card card-lowest">
      <div class="summary-label">Lowest modeled cost</div>
      <div class="summary-metric">${{rows[0].total}}</div>
      <div class="summary-scenario"><strong>${{rows[0].name}}</strong> &middot; Based on ${{document.getElementById('p-slider-val').textContent}}</div>
      <div class="summary-actions">
        <a href="{p["winner_url"]}" target="_blank" rel="noopener" class="btn-cta" data-track="vendor-cta" data-vendor="{p["winner_vendor"]}" data-cta-location="subpage-summary">{p["winner_cta"]} &rarr;</a>
      </div>
    </div>
  `;
  document.getElementById('p-tbody').innerHTML = rows.map(r => `
    <tr>
      <td data-label="Platform"><strong>${{r.name}}</strong><br><span class="status-pill status-verified">${{r.status}}</span> &middot; <a href="${{r.src}}" target="_blank" rel="noopener" class="source-link">Verified source</a></td>
      <td data-label="Advertised Plan">${{r.plan}}</td>
      <td data-label="Base Cost">${{r.base}}</td>
      <td data-label="Hidden Cost Highlight"><span style="color:var(--warn); font-weight:600;">Hidden Cost Highlight:</span> ${{r.hidden}}</td>
      <td data-label="True Year-1 Cost"><strong>${{r.total}}</strong></td>
      <td data-label="Action"><a href="${{r.url}}" target="_blank" rel="noopener" class="btn-secondary" data-track="vendor-cta" data-vendor="${{r.vendor}}" data-cta-location="${{r.ctaLocation || 'subpage-table'}}">${{r.cta}} &rarr;</a></td>
    </tr>
  `).join('');
  (function () {{
    function firstMoney(s) {{
      var m = String(s || '').replace(/,/g, '').match(/\\$([0-9]+(?:\\.[0-9]+)?)/);
      return m ? Number(m[1]) : 0;
    }}
    function rowGap(r) {{
      var sticker = firstMoney(r.base);
      var total = firstMoney(r.total);
      return Math.max(Math.max(0, total - sticker), firstMoney(r.hidden));
    }}
    var pool = rows.filter(function (r) {{ return !/^saves/i.test(String(r.total || '')); }});
    var h1el = document.querySelector('h1');
    var h1 = h1el ? (h1el.textContent || '') : '';
    var named = pool.filter(function (r) {{
      return String(r.name || '').split(/[^A-Za-z0-9]+/).some(function (w) {{
        return w.length > 3 && h1.indexOf(w) !== -1;
      }});
    }});
    var candidates = named.length ? named : pool;
    var focus = candidates[0] || rows[0];
    var bestGap = -1;
    var bestTotal = -1;
    candidates.forEach(function (r) {{
      var g = rowGap(r);
      var t = firstMoney(r.total);
      if (g > bestGap || (g === bestGap && t > bestTotal)) {{
        bestGap = g;
        bestTotal = t;
        focus = r;
      }}
    }});
    var sticker = firstMoney(focus.base);
    var total = firstMoney(focus.total);
    var hidden = Math.max(Math.max(0, total - sticker), firstMoney(focus.hidden));
    var shown = Math.max(total, sticker + hidden);
    var math = '<div class="calc-math-list">' + rows.map(function (r) {{
      return '<div class="calc-math-row"><span class="calc-math-label"><strong>' + r.name + '</strong><span class="calc-math-formula">' + r.plan + ' · ' + r.hidden + '</span></span><span class="calc-math-val">' + r.total + '</span></div>';
    }}).join('') + '</div>';
    if (typeof window.saasbillApplyWorkbench === 'function') {{
      window.saasbillApplyWorkbench({{
        product: focus.name,
        sticker: sticker,
        hidden: hidden,
        total: shown,
        baseLabel: String(focus.plan || ''),
        hiddenLabel: String(focus.hidden || '').replace(/<[^>]+>/g, ''),
        mathHtml: math,
        bestHtml: '<strong>Lowest modeled cost:</strong> ' + rows[0].name + ' at ' + rows[0].total + '.',
        ctaHref: rows[0].url,
        ctaLabel: rows[0].cta,
        ctaVendor: rows[0].vendor
      }});
    }}
  }})();
  if (typeof window.trackSaaSBillEvent === 'function') window.trackSaaSBillEvent('result_rendered', {{ page: '{p["slug"]}' }});
}}
[{listener_js}].forEach(id => {{
  const el = document.getElementById(id);
  if (!el) return;
  el.addEventListener('input', runPageCalc);
  el.addEventListener('change', runPageCalc);
}});
runPageCalc();
</script>
"""
        render_page(
            p["rel"],
            p["title"],
            p["desc"],
            p["slug"],
            body,
            faqs=p["faqs"],
        )


if __name__ == "__main__":
    build_all()
