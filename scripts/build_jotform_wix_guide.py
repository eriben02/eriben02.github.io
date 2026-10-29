"""
Builds:
1. /guides/jotform-wix-app-setup-and-pricing-guide/index.html
   (Step-by-step visual walkthrough & pricing guide for the Jotform Wix App + #JotformPartner campaign)
2. /pricing/jotform-pricing-tier-calculator/index.html
   (Interactive 2026 Jotform Starter, Bronze, Silver & Gold HIPAA pricing calculator)
"""
from layout import render_page, SITE_ORIGIN, wrap_calculator_shell

JOTFORM_PARTNER_URL = "https://www.jotform.com/?partner=eriben02"
JOTFORM_PRICING_PARTNER_URL = "https://www.jotform.com/pricing/?partner=eriben02"
JOTFORM_HIPAA_PARTNER_URL = "https://www.jotform.com/hipaa/pricing/?partner=saasbill"
WIX_APP_MARKET_URL = "https://www.wix.com/app-market/web-solution/jotform"
LIVE_WIX_DEMO_URL = "https://info149840.wixsite.com/my-site-1"
LIVE_JOTFORM_URL = "https://form.jotform.com/262996430206056"


def build_jotform_wix_guide():
    rel = "guides/jotform-wix-app-setup-and-pricing-guide/index.html"
    slug = "/guides/jotform-wix-app-setup-and-pricing-guide/"
    title = "Jotform Wix App Setup & Pricing Guide (2026) – saasbill.io"
    desc = (
        "Step-by-step 2026 visual guide and video walkthrough showing how to embed a B2B Custom Quote & Bulk Order form on Wix using the official Jotform Wix App, plus Jotform Starter, Bronze, Silver, and Gold pricing."
    )

    body = f"""
<section class="hero">
  <h1>How to Embed a B2B Custom Quote Form on Wix Using the Jotform Wix App (2026 Step-by-Step Guide &amp; Pricing)</h1>
  <p class="lead">Installing the official Jotform Wix App from the Wix App Market lets you embed conditional B2B quote forms, file uploads, and payment flows onto any Wix page in under five minutes while syncing every submission directly to Jotform Tables. Below is our live 5-step installation walkthrough and video demo on a published Wix store, followed by an interactive 2026 cost comparison between Jotform plans (Starter Free, Bronze $34/mo, Silver $39/mo, Gold $99/mo billed annually) and Wix native form tiers.</p>

  <div class="partnership-disclosure-box" role="note" aria-label="Paid Partnership and Affiliate Disclosure">
    <div class="partnership-badge-row">
      <span class="hashtag-pill">#JotformPartner</span>
      <span class="partnership-label">Paid Partnership &amp; Affiliate Disclosure</span>
    </div>
    <p style="margin:6px 0 0 0; font-size:0.86rem; color:#2A2E29; line-height:1.5;">
      <strong>Disclosure (#JotformPartner):</strong> This tutorial and pricing guide is published as part of a paid creator partnership with Jotform and contains affiliate partner links (<a href="{JOTFORM_PARTNER_URL}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="jotform" data-cta-location="disclosure-top">jotform.com/?partner=eriben02</a>). If you sign up through our links, we may earn a commission at no extra cost to you. All pricing figures, plan limits, and live Wix installation screenshots were independently tested and verified on October 27, 2026.
    </p>
  </div>

  <div class="cta-stack" style="flex-direction:row; flex-wrap:wrap; gap:12px; margin-top:18px;">
    <a class="btn-cta" href="{JOTFORM_PARTNER_URL}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="jotform" data-cta-location="hero-primary">Try Jotform Free (5 Forms Included) &rarr;</a>
    <a class="btn-secondary" href="{WIX_APP_MARKET_URL}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="jotform" data-cta-location="hero-wix-market">Open Jotform in Wix App Market &nearr;</a>
    <a class="btn-secondary" href="{LIVE_WIX_DEMO_URL}" target="_blank" rel="noopener">View Our Live Wix Demo Site &nearr;</a>
  </div>
</section>

<section class="calc-box" id="walkthrough-video-section" aria-labelledby="video-walkthrough-heading">
  <h2 id="video-walkthrough-heading" style="margin-top:0;">Video Walkthrough: Installing the Jotform Wix App in Action</h2>
  <p style="color:var(--muted); margin-bottom:14px; font-size:0.94rem;">
    Watch the complete 28-second walkthrough from building our <strong>B2B Custom Quote &amp; Bulk Order Inquiry</strong> form (<code>#262996430206056</code>) in Jotform, installing the official <strong>Jotform Wix App</strong> inside the Wix Editor, submitting a live test order on <a href="{LIVE_WIX_DEMO_URL}" target="_blank" rel="noopener">info149840.wixsite.com/my-site-1</a>, and verifying the structured record inside Jotform Tables.
  </p>
  <div class="guide-video-frame">
    <video controls preload="metadata" poster="../../assets/guides/jotform-wix/video-poster.jpg" width="1280" height="800" style="width:100%; height:auto; display:block; border-radius:6px; border:1px solid var(--border-strong); background:#20231F;">
      <source src="../../assets/guides/jotform-wix/jotform-wix-app-walkthrough.mp4" type="video/mp4" />
      Your browser does not support HTML5 video. You can <a href="../../assets/guides/jotform-wix/jotform-wix-app-walkthrough.mp4">download the MP4 walkthrough video here</a>.
    </video>
  </div>
  <div style="display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; gap:10px; margin-top:12px; font-size:0.82rem; color:var(--muted);">
    <span><strong>Live Use Case:</strong> B2B Custom Quote &amp; Bulk Order Inquiry (<a href="{LIVE_JOTFORM_URL}" target="_blank" rel="noopener">Form #262996430206056 &nearr;</a>) embedded on <a href="{LIVE_WIX_DEMO_URL}" target="_blank" rel="noopener">Wix Live Demo &nearr;</a></span>
    <span>Campaign tag: <strong>#JotformPartner</strong></span>
  </div>
</section>

<section aria-labelledby="use-case-heading" style="margin:32px 0;">
  <h2 id="use-case-heading">Why B2B Wix Store Owners Use the Jotform Wix App Instead of Basic Contact Forms</h2>
  <p>Standard website contact forms work fine for simple messages, but wholesale and B2B merchants on Wix routinely need multi-line SKU quote requests, volume tier logic, tax-exempt certificate uploads, signed purchase agreements, or HIPAA-compliant intake. Embedding Jotform through the native <a href="{WIX_APP_MARKET_URL}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="jotform" data-cta-location="body-link">Jotform Wix App</a> solves four practical bottlenecks:</p>
  <ul class="key-list">
    <li><strong>No manual iframe height clipping:</strong> The official Wix App widget automatically resizes inside the Wix Editor canvas and mobile viewport so multi-field B2B forms never get cut off or trap users in double scrollbars.</li>
    <li><strong>Direct Jotform Tables &amp; CRM pipeline sync:</strong> Every quote inquiry lands immediately in a structured Jotform Table with status tags, timestamps, and 1-click export to Excel, Google Sheets, HubSpot, or Close CRM.</li>
    <li><strong>Generous entry limits on Starter (Free) and Bronze ($34/mo):</strong> You can test the complete Wix workflow on Jotform Starter ($0/month for up to 5 active forms and 100 monthly submissions) before scaling to Bronze (25 forms, 1,000 submissions/mo) or Gold ($99/month annual with 10,000 submissions/mo and HIPAA BAA support).</li>
    <li><strong>Zero developer maintenance:</strong> Any field update you publish inside the Jotform Form Builder updates live on your Wix storefront immediately without republishing your Wix site.</li>
  </ul>
</section>

<section aria-labelledby="steps-heading" style="margin:36px 0;">
  <h2 id="steps-heading">Step-by-Step Visual Walkthrough: Setting Up the Jotform Wix App</h2>
  <p style="color:var(--muted); margin-bottom:20px;">Every screenshot below was captured during our live setup of the <strong>B2B Custom Quote &amp; Bulk Order Inquiry</strong> form on Wix.</p>

  <div class="guide-step-card">
    <div class="guide-step-header">
      <span class="guide-step-num">Step 1</span>
      <h3>Build the B2B Custom Quote &amp; Bulk Order Form in Jotform Form Builder</h3>
    </div>
    <p>Log into <a href="{JOTFORM_PARTNER_URL}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="jotform" data-cta-location="step-1">Jotform</a> and click <strong>Create Form &rarr; Start From Scratch</strong> (or choose one of 10,000+ B2B quote templates). For our wholesale inquiry workflow (<a href="{LIVE_JOTFORM_URL}" target="_blank" rel="noopener">form.jotform.com/262996430206056</a>), we added <strong>Company Name</strong>, <strong>Business Email</strong>, <strong>Product Category</strong> (Industrial Hardware &amp; Sensors), <strong>Estimated Order Volume (Units)</strong>, <strong>Target Delivery Timeline</strong>, and <strong>Custom Specifications / Notes</strong>.</p>
    <figure class="guide-figure">
      <img src="../../assets/guides/jotform-wix/step1-jotform-builder.webp" alt="Step 1: Building the B2B Custom Quote and Bulk Order Inquiry form inside Jotform Form Builder" loading="lazy" width="1280" height="742" />
      <figcaption>Step 1: Configuring our B2B Custom Quote &amp; Bulk Order Inquiry form (#262996430206056) inside the Jotform Form Builder.</figcaption>
    </figure>
  </div>

  <div class="guide-step-card">
    <div class="guide-step-header">
      <span class="guide-step-num">Step 2</span>
      <h3>Install the Official Jotform App from the Wix App Market</h3>
    </div>
    <p>Open the <a href="{WIX_APP_MARKET_URL}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="jotform" data-cta-location="step-2">Jotform listing in the Wix App Market</a> (or click <strong>Add Apps</strong> inside the left sidebar of the Wix Editor and search for <strong>Jotform</strong>). Click <strong>Add to Site</strong>, choose your Wix site, and click <strong>Agree &amp; Add</strong> on the permissions screen so the Jotform widget can render inside your Wix pages.</p>
    <div class="guide-dual-grid">
      <figure class="guide-figure">
        <img src="../../assets/guides/jotform-wix/step2a-wix-app-market.webp" alt="Step 2A: Official Jotform App page in the Wix App Market showing Add to Site button" loading="lazy" width="1280" height="742" />
        <figcaption>Step 2A: Clicking <strong>Add to Site</strong> on the official Jotform page in the Wix App Market.</figcaption>
      </figure>
      <figure class="guide-figure">
        <img src="../../assets/guides/jotform-wix/step2b-wix-permissions.webp" alt="Step 2B: Granting permissions and clicking Agree and Add to install Jotform on Wix" loading="lazy" width="1280" height="742" />
        <figcaption>Step 2B: Confirming Wix App permissions by clicking <strong>Agree &amp; Add</strong>.</figcaption>
      </figure>
    </div>
  </div>

  <div class="guide-step-card">
    <div class="guide-step-header">
      <span class="guide-step-num">Step 3</span>
      <h3>Connect Your Jotform Account &amp; Select the Form Inside Wix Editor</h3>
    </div>
    <p>Once the Jotform app block drops onto your Wix page, click <strong>Settings</strong> above the widget. Authenticate your Jotform account in the Settings drawer, select <strong>B2B Custom Quote &amp; Bulk Order Inquiry</strong> from your form list, and click <strong>Publish</strong> in the top-right corner of the Wix Editor.</p>
    <div class="guide-dual-grid">
      <figure class="guide-figure">
        <img src="../../assets/guides/jotform-wix/step3a-wix-editor-connect.webp" alt="Step 3A: Opening Jotform widget settings inside the Wix Editor to connect account" loading="lazy" width="1280" height="800" />
        <figcaption>Step 3A: Opening the Jotform App Settings panel inside the Wix Editor.</figcaption>
      </figure>
      <figure class="guide-figure">
        <img src="../../assets/guides/jotform-wix/step3b-wix-form-selected.webp" alt="Step 3B: Selecting the B2B Custom Quote and Bulk Order Inquiry form inside the Wix Editor" loading="lazy" width="1280" height="800" />
        <figcaption>Step 3B: Selecting our B2B Custom Quote form from the connected Jotform account list and publishing the Wix page.</figcaption>
      </figure>
    </div>
  </div>

  <div class="guide-step-card">
    <div class="guide-step-header">
      <span class="guide-step-num">Step 4</span>
      <h3>Submit a Live B2B Quote Inquiry on the Published Wix Website</h3>
    </div>
    <p>We opened our published Wix page (<a href="{LIVE_WIX_DEMO_URL}" target="_blank" rel="noopener">info149840.wixsite.com/my-site-1</a>) in a live browser session and submitted a test bulk order for <strong>Northstar Logistics B2B</strong> (contact: <strong>Alex Rivera</strong>, 250 units of Industrial Hardware &amp; Sensors, Q4 2026 rollout). Clicking <strong>Request Custom B2B Quote</strong> immediately rendered the clean in-page confirmation without redirecting away from the Wix storefront.</p>
    <div class="guide-dual-grid">
      <figure class="guide-figure">
        <img src="../../assets/guides/jotform-wix/step4a-live-wix-submission.webp" alt="Step 4A: Filling out the embedded Jotform B2B quote form on the live Wix website" loading="lazy" width="1280" height="742" />
        <figcaption>Step 4A: Filling out the live embedded B2B quote form on <code>info149840.wixsite.com/my-site-1</code>.</figcaption>
      </figure>
      <figure class="guide-figure">
        <img src="../../assets/guides/jotform-wix/step4b-thank-you-confirmation.webp" alt="Step 4B: Instant Thank You confirmation displayed inside the Wix page after submission" loading="lazy" width="1280" height="742" />
        <figcaption>Step 4B: Instant in-page <strong>Thank You!</strong> confirmation displayed to the buyer on the live Wix page.</figcaption>
      </figure>
    </div>
  </div>

  <div class="guide-step-card">
    <div class="guide-step-header">
      <span class="guide-step-num">Step 5</span>
      <h3>Verify the Captured Lead &amp; Specifications in Jotform Tables</h3>
    </div>
    <p>Opening <strong>Jotform Tables</strong> shows the submitted row from <strong>Alex Rivera (Northstar Logistics B2B)</strong> captured in real time with every specification field neatly parsed into columns, ready for sales follow-up, PDF quote generation, or automated webhook routing.</p>
    <figure class="guide-figure">
      <img src="../../assets/guides/jotform-wix/step5-jotform-tables-verified.webp" alt="Step 5: Verified submission from Alex Rivera at Northstar Logistics B2B inside Jotform Tables" loading="lazy" width="1280" height="742" />
      <figcaption>Step 5: The completed Wix submission verified inside Jotform Tables with all B2B quote fields structured.</figcaption>
    </figure>
    <div class="cta-stack" style="flex-direction:row; flex-wrap:wrap; gap:12px; margin-top:14px;">
      <a class="btn-cta" href="{JOTFORM_PARTNER_URL}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="jotform" data-cta-location="step-5-cta">Build Your First Wix Form on Jotform Free &rarr;</a>
      <a class="btn-secondary" href="{WIX_APP_MARKET_URL}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="jotform" data-cta-location="step-5-wix">Get the Jotform Wix App &nearr;</a>
    </div>
  </div>
</section>

<section class="calc-box" id="jotform-wix-cost-calculator" aria-labelledby="cost-calc-heading">
  <h2 id="cost-calc-heading" style="margin-top:0;">2026 Jotform Pricing Breakdown for Wix Store Owners (Starter vs. Bronze, Silver &amp; Gold)</h2>
  <p style="color:var(--muted); margin-bottom:18px; font-size:0.94rem;">
    Use the calculator below to see which Jotform tier fits your monthly Wix lead and quote volume, and compare total Year-1 cost against Typeform and custom HIPAA form tiers. For standalone tier modeling, see our <a href="../../pricing/jotform-pricing-tier-calculator/" data-track="internal-audit">Jotform Pricing Tier Calculator</a> and <a href="../../compare/typeform-vs-jotform-response-limit-and-hipaa-cost/" data-track="internal-audit">Typeform vs. Jotform Response Limit &amp; HIPAA Calculator</a>.
  </p>

  <div class="calc-grid">
    <div class="control-group">
      <label for="jw-vol">Monthly Wix Form Submissions: <span class="val-pill" id="jw-vol-val">500</span> / month</label>
      <input type="range" id="jw-vol" min="50" max="5000" step="50" value="500" data-track="calculator-control" data-control="jw-vol" />
    </div>
    <div class="control-group">
      <label for="jw-billing">Billing Cycle &amp; Compliance Need</label>
      <select id="jw-billing" data-track="calculator-control" data-control="jw-billing">
        <option value="annual" selected>Annual Billing (Save up to 20%)</option>
        <option value="monthly">Monthly Billing (No Annual Lock-In)</option>
        <option value="hipaa">HIPAA BAA Required (Gold Plan Annual)</option>
      </select>
    </div>
  </div>

  <div id="jw-summary" class="summary-strip" aria-live="polite"></div>

  <div class="table-wrap mobile-cards">
    <table>
      <caption>2026 Jotform Plans vs. Wix Native Forms &amp; Typeform (Verified Oct 27, 2026)</caption>
      <thead>
        <tr>
          <th>Plan / Platform</th>
          <th>Monthly Rate (Annual / Monthly)</th>
          <th>Form &amp; Submission Limits</th>
          <th>Hidden Cost Highlight</th>
          <th>True Year-1 Cost</th>
          <th>Official Link</th>
        </tr>
      </thead>
      <tbody id="jw-tbody"></tbody>
    </table>
  </div>
</section>

<script>
function updateJotformWixCalc() {{
  const vol = parseInt(document.getElementById('jw-vol').value, 10);
  const mode = document.getElementById('jw-billing').value;
  document.getElementById('jw-vol-val').textContent = vol.toLocaleString('en-US');

  let recTier = 'Jotform Starter (Free)';
  let recMo = 0;
  let recLimit = '5 forms · 100 submissions/mo · 100 MB storage';
  if (mode === 'hipaa') {{
    recTier = 'Jotform Gold (HIPAA BAA Included)';
    recMo = 99;
    recLimit = '100 forms · 10,000 submissions/mo · Signed HIPAA BAA';
  }} else if (vol <= 100) {{
    recTier = 'Jotform Starter (Free)';
    recMo = 0;
    recLimit = '5 forms · 100 submissions/mo · Includes Jotform branding';
  }} else if (vol <= 1000) {{
    recTier = 'Jotform Bronze (No Branding)';
    recMo = mode === 'annual' ? 34 : 39;
    recLimit = '25 forms · 1,000 submissions/mo · 1 GB storage';
  }} else if (vol <= 2500) {{
    recTier = 'Jotform Silver';
    recMo = mode === 'annual' ? 39 : 49;
    recLimit = '50 forms · 2,500 submissions/mo · 10 GB storage';
  }} else {{
    recTier = 'Jotform Gold';
    recMo = mode === 'annual' ? 99 : 129;
    recLimit = '100 forms · 10,000 submissions/mo · HIPAA BAA eligible';
  }}

  const recYr = recMo * 12;
  const tfMo = mode === 'hipaa' ? 500 : (vol <= 100 ? 25 : (vol <= 1000 ? 50 : 83));
  const tfYr = tfMo * 12;
  const savedVsTf = Math.max(0, tfYr - recYr);
  const modeLabel = mode === 'hipaa' ? 'HIPAA BAA required' : (mode === 'annual' ? 'annual billing' : 'monthly billing');

  document.getElementById('jw-summary').innerHTML = `
    <div class="summary-card result-card card-lowest">
      <div class="summary-label">Best-Fit Jotform Plan for Your Wix Site</div>
      <div class="summary-metric" style="color:var(--emerald);">$${{recYr.toLocaleString('en-US')}} / yr &middot; ${{recTier}}</div>
      <div class="summary-scenario">Based on ${{vol.toLocaleString('en-US')}} submissions/mo, ${{modeLabel}}</div>
      <div class="summary-breakdown">${{recLimit}} &middot; $0 Wix App installation fee</div>
      <div class="summary-actions" style="margin-top:8px;">
        <a class="btn-cta" href="{JOTFORM_PARTNER_URL}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="jotform" data-cta-location="jw-summary">Start with ${{recTier.split(' (')[0]}} &rarr;</a>
      </div>
    </div>
    <div class="summary-card result-card card-hidden">
      <div class="summary-label">Hidden Cost Highlight (Typeform &amp; Native Caps)</div>
      <div class="summary-metric" style="color:var(--rose);">Saves $${{savedVsTf.toLocaleString('en-US')}} / yr vs. Typeform</div>
      <div class="summary-scenario">Based on ${{vol.toLocaleString('en-US')}} submissions/mo (${{modeLabel}})</div>
      <div class="summary-breakdown"><strong>Hidden Cost Highlight:</strong> Typeform Free caps at just 10 responses/mo across all forms and requires Enterprise (~$6,000+/yr) for a HIPAA BAA.</div>
      <div class="summary-actions" style="margin-top:8px;">
        <a class="summary-audit-link" href="../../compare/typeform-vs-jotform-response-limit-and-hipaa-cost/" data-track="internal-audit">Read Typeform vs. Jotform audit &rarr;</a>
      </div>
    </div>
  `;

  const tableRows = [
    {{
      name: 'Jotform Starter (Free + Wix App)',
      rate: '$0 / mo',
      limits: '5 forms · 100 submissions/mo · 10 payment submissions/mo',
      hidden: 'Includes Jotform badge at bottom of embedded Wix form',
      total: '$0 / yr',
      url: '{JOTFORM_PARTNER_URL}',
      cta: 'Start Free on Jotform →'
    }},
    {{
      name: 'Jotform Bronze',
      rate: '$34/mo annual ($39/mo monthly)',
      limits: '25 forms · 1,000 submissions/mo · 100 payment submissions/mo',
      hidden: '$0 onboarding · Removes Jotform branding on Wix',
      total: '$' + ((mode === 'monthly' ? 39 : 34) * 12).toLocaleString('en-US') + ' / yr',
      url: '{JOTFORM_PRICING_PARTNER_URL}',
      cta: 'View Jotform Bronze →'
    }},
    {{
      name: 'Jotform Silver',
      rate: '$39/mo annual ($49/mo monthly)',
      limits: '50 forms · 2,500 submissions/mo · 250 payment submissions/mo',
      hidden: '$0 onboarding · Only $5/mo more than Bronze on annual billing',
      total: '$' + ((mode === 'monthly' ? 49 : 39) * 12).toLocaleString('en-US') + ' / yr',
      url: '{JOTFORM_PRICING_PARTNER_URL}',
      cta: 'View Jotform Silver →'
    }},
    {{
      name: 'Jotform Gold (HIPAA Eligible)',
      rate: '$99/mo annual ($129/mo monthly)',
      limits: '100 forms · 10,000 submissions/mo · Signed HIPAA BAA included',
      hidden: '$0 onboarding · Cheapest self-serve HIPAA BAA form builder',
      total: '$' + ((mode === 'monthly' ? 129 : 99) * 12).toLocaleString('en-US') + ' / yr',
      url: '{JOTFORM_HIPAA_PARTNER_URL}',
      cta: 'View Jotform Gold →'
    }},
    {{
      name: 'Wix Native Forms (Free vs. Ascend/Business)',
      rate: '$0 base (Ascend add-on extra)',
      limits: '4 free forms · Limited conditional logic & file upload quotas',
      hidden: 'Advanced multi-step conditional logic, BAA & PDF workflows require upgrades',
      total: 'Varies by Wix Business plan',
      url: '{WIX_APP_MARKET_URL}',
      cta: 'Compare in Wix App Market →'
    }}
  ];

  if (typeof window.saasbillApplyWorkbench === 'function') {{
    window.saasbillApplyWorkbench({{
      product: recTier,
      sticker: recYr,
      hidden: 0,
      total: recYr,
      baseLabel: recLimit,
      hiddenLabel: 'This tier price is the advertised rate',
      bestHtml: '<strong>Recommended:</strong> ' + recTier + ' at $' + recYr.toLocaleString('en-US') + '/yr.',
      ctaHref: '{JOTFORM_PARTNER_URL}',
      ctaLabel: 'View Jotform pricing',
      ctaVendor: 'jotform'
    }});
  }}
  document.getElementById('jw-tbody').innerHTML = tableRows.map(r => `
    <tr>
      <td data-label="Plan / Platform"><strong>${{r.name}}</strong> <span class="status-pill status-verified">Verified</span></td>
      <td data-label="Monthly Rate">${{r.rate}}</td>
      <td data-label="Form & Submission Limits">${{r.limits}}</td>
      <td data-label="Hidden Cost Highlight"><strong>Hidden Cost Highlight:</strong> ${{r.hidden}}</td>
      <td data-label="True Year-1 Cost"><strong>${{r.total}}</strong></td>
      <td data-label="Official Link"><a class="btn-secondary" href="${{r.url}}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="jotform" data-cta-location="jw-table">${{r.cta}}</a></td>
    </tr>
  `).join('');
}}
['jw-vol', 'jw-billing'].forEach(id => {{
  const el = document.getElementById(id);
  if (el) {{
    el.addEventListener('input', updateJotformWixCalc);
    el.addEventListener('change', updateJotformWixCalc);
  }}
}});
updateJotformWixCalc();
</script>

<section class="partnership-disclosure-box" style="margin-top:28px;" aria-label="Campaign Footer Disclosure">
  <p style="margin:0; font-size:0.84rem; color:#2A2E29;">
    <strong>Campaign &amp; Affiliate Disclosure (#JotformPartner):</strong> Created in paid partnership with Jotform. Try Jotform on your Wix site via our partner link: <a href="{JOTFORM_PARTNER_URL}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="jotform" data-cta-location="disclosure-bottom">https://www.jotform.com/?partner=eriben02</a> or install the <a href="{WIX_APP_MARKET_URL}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="jotform" data-cta-location="disclosure-wix">Jotform Wix App in the Wix App Market</a>.
  </p>
</section>
"""

    faqs = [
        (
            "Is the Jotform Wix App free to install on a Wix website?",
            "Yes. The Jotform Wix App is free to install from the Wix App Market and works with Jotform's free Starter plan (which includes up to 5 active forms and 100 monthly submissions). To remove Jotform branding or accept up to 1,000 monthly submissions, Bronze costs $34/month billed annually ($39/month billed monthly).",
        ),
        (
            "How do I connect my existing Jotform form to a Wix page?",
            "Install the Jotform app from the Wix App Market, click Settings on the Jotform widget inside the Wix Editor, sign in to your Jotform account when prompted, and select your form from the list. Any changes you make later in Jotform Form Builder sync automatically to your live Wix page.",
        ),
        (
            "Which Jotform plan do I need if my Wix site collects HIPAA-regulated health information?",
            "You need Jotform Gold ($99/month billed annually or $129/month billed monthly), which includes HIPAA compliance features and a signed Business Associate Agreement (BAA) alongside 10,000 monthly submissions.",
        ),
    ]

    render_page(
        rel,
        title,
        desc,
        slug,
        wrap_calculator_shell(body),
        faqs=faqs,
        extra_schema={
            "@type": "HowTo",
            "name": "How to Embed a B2B Custom Quote Form on Wix Using the Jotform Wix App",
            "description": desc,
            "step": [
                {"@type": "HowToStep", "position": 1, "name": "Build the B2B Custom Quote Form in Jotform Form Builder"},
                {"@type": "HowToStep", "position": 2, "name": "Install the Official Jotform App from the Wix App Market"},
                {"@type": "HowToStep", "position": 3, "name": "Connect Your Jotform Account and Select the Form in Wix Editor"},
                {"@type": "HowToStep", "position": 4, "name": "Submit a Live Test Quote Inquiry on the Published Wix Website"},
                {"@type": "HowToStep", "position": 5, "name": "Verify the Captured Lead in Jotform Tables"},
            ],
        },
    )


def build_jotform_pricing_calculator():
    rel = "pricing/jotform-pricing-tier-calculator/index.html"
    slug = "/pricing/jotform-pricing-tier-calculator/"
    title = "Jotform Pricing Tier Calculator (2026) – saasbill.io"
    desc = (
        "Calculate your 2026 Jotform Year-1 cost across Starter (Free), Bronze ($34/mo), Silver ($39/mo), and Gold ($99/mo HIPAA BAA) based on monthly submissions, payment volume, and Wix/website embedding."
    )

    body = f"""
<section class="hero">
  <h1>Jotform Pricing Tier Calculator (2026): Starter, Bronze, Silver &amp; Gold True Year-1 Cost</h1>
  <p class="lead">In 2026, Jotform costs $0/month on Starter (100 submissions/mo), $34/month billed annually on Bronze (1,000 submissions/mo), $39/month billed annually on Silver (2,500 submissions/mo), and $99/month billed annually on Gold with a signed HIPAA BAA and 10,000 submissions/month (source: Jotform official pricing page, verified Oct 2026). Because Silver costs only $5/month ($60/year) more than Bronze on annual billing while increasing monthly submissions 2.5x and storage 10x, Silver is the sweet spot for growing B2B teams.</p>
</section>

<section class="calc-box" aria-label="Jotform 2026 Tier Calculator">
  <div class="calc-grid">
    <div class="control-group">
      <label for="jf-subs">Monthly Form Submissions: <span class="val-pill" id="jf-subs-val">800</span> / mo</label>
      <input type="range" id="jf-subs" min="50" max="10000" step="50" value="800" data-track="calculator-control" data-control="jf-subs" />
    </div>
    <div class="control-group">
      <label for="jf-mode">Billing Cycle &amp; Compliance</label>
      <select id="jf-mode" data-track="calculator-control" data-control="jf-mode">
        <option value="annual" selected>Annual Billing (20% Discount)</option>
        <option value="monthly">Monthly Billing (Cancel Anytime)</option>
        <option value="hipaa">HIPAA Compliance &amp; BAA Required</option>
      </select>
    </div>
  </div>

  <div id="jf-tier-summary" class="summary-strip" aria-live="polite"></div>

  <div class="table-wrap mobile-cards">
    <table>
      <caption>2026 Jotform Pricing Tiers &amp; Limits (Verified Oct 27, 2026)</caption>
      <thead>
        <tr>
          <th>Jotform Tier</th>
          <th>Advertised Rate</th>
          <th>Included Quotas</th>
          <th>Hidden Cost Highlight</th>
          <th>True Year-1 Cost</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody id="jf-tier-tbody"></tbody>
    </table>
  </div>

  <p style="margin-top:14px; font-size:0.88rem; color:var(--muted);">
    Embedding forms on Wix? Read our step-by-step <a href="../../guides/jotform-wix-app-setup-and-pricing-guide/" data-track="internal-audit">Jotform Wix App Setup &amp; Pricing Guide (with live video walkthrough) &rarr;</a> or compare against Typeform in our <a href="../../compare/typeform-vs-jotform-response-limit-and-hipaa-cost/" data-track="internal-audit">Typeform vs. Jotform Calculator &rarr;</a>
  </p>
</section>

<script>
function runJfTierCalc() {{
  const subs = parseInt(document.getElementById('jf-subs').value, 10);
  const mode = document.getElementById('jf-mode').value;
  document.getElementById('jf-subs-val').textContent = subs.toLocaleString('en-US');

  const isMonthly = mode === 'monthly';
  const bronzeMo = isMonthly ? 39 : 34;
  const silverMo = isMonthly ? 49 : 39;
  const goldMo = isMonthly ? 129 : 99;

  let bestName = 'Jotform Bronze';
  let bestYr = bronzeMo * 12;
  if (mode === 'hipaa') {{
    bestName = 'Jotform Gold (HIPAA BAA)';
    bestYr = goldMo * 12;
  }} else if (subs <= 100) {{
    bestName = 'Jotform Starter (Free)';
    bestYr = 0;
  }} else if (subs <= 1000) {{
    bestName = 'Jotform Bronze';
    bestYr = bronzeMo * 12;
  }} else if (subs <= 2500) {{
    bestName = 'Jotform Silver';
    bestYr = silverMo * 12;
  }} else {{
    bestName = 'Jotform Gold';
    bestYr = goldMo * 12;
  }}

  const modeDesc = mode === 'hipaa' ? 'HIPAA BAA required' : (isMonthly ? 'monthly billing' : 'annual billing');
  document.getElementById('jf-tier-summary').innerHTML = `
    <div class="summary-card result-card card-lowest">
      <div class="summary-label">Recommended Jotform Tier</div>
      <div class="summary-metric" style="color:var(--emerald);">$${{bestYr.toLocaleString('en-US')}} / yr &middot; ${{bestName}}</div>
      <div class="summary-scenario">Based on ${{subs.toLocaleString('en-US')}} submissions/mo, ${{modeDesc}}</div>
      <div class="summary-breakdown">$0 mandatory onboarding &middot; Works natively with the Jotform Wix App</div>
      <div class="summary-actions" style="margin-top:8px;">
        <a class="btn-cta" href="{JOTFORM_PARTNER_URL}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="jotform" data-cta-location="jf-tier-summary">View Jotform pricing &rarr;</a>
      </div>
    </div>
    <div class="summary-card result-card card-hidden">
      <div class="summary-label">Hidden Cost Highlight (Silver vs. Bronze Spread)</div>
      <div class="summary-metric" style="color:var(--rose);">Only +$60 / yr from Bronze to Silver</div>
      <div class="summary-scenario">Based on annual billing ($34/mo Bronze vs. $39/mo Silver)</div>
      <div class="summary-breakdown"><strong>Hidden Cost Highlight:</strong> Paying $5/mo extra for Silver unlocks 2.5x more monthly submissions (2,500 vs. 1,000) and 10x more file storage (10 GB vs. 1 GB).</div>
    </div>
  `;

  const rows = [
    {{name: 'Jotform Starter (Free)', rate: '$0/mo', quotas: '5 forms · 100 submissions/mo · 100 MB storage', hidden: 'Jotform branding shown on embedded forms', total: '$0/yr', url: '{JOTFORM_PARTNER_URL}'}},
    {{name: 'Jotform Bronze', rate: '$' + bronzeMo + '/mo', quotas: '25 forms · 1,000 submissions/mo · 1 GB storage', hidden: '$0 onboarding · Custom branding unlocked', total: '$' + (bronzeMo * 12).toLocaleString('en-US') + '/yr', url: '{JOTFORM_PRICING_PARTNER_URL}'}},
    {{name: 'Jotform Silver', rate: '$' + silverMo + '/mo', quotas: '50 forms · 2,500 submissions/mo · 10 GB storage', hidden: 'Best value per submission ($0.015/submission at capacity)', total: '$' + (silverMo * 12).toLocaleString('en-US') + '/yr', url: '{JOTFORM_PRICING_PARTNER_URL}'}},
    {{name: 'Jotform Gold (HIPAA BAA)', rate: '$' + goldMo + '/mo', quotas: '100 forms · 10,000 submissions/mo · 100 GB storage + BAA', hidden: 'Includes signed HIPAA BAA (vs. $6,000+/yr Enterprise on Typeform)', total: '$' + (goldMo * 12).toLocaleString('en-US') + '/yr', url: '{JOTFORM_HIPAA_PARTNER_URL}'}}
  ];

  if (typeof window.saasbillApplyWorkbench === 'function') {{
    window.saasbillApplyWorkbench({{
      product: bestName,
      sticker: bestYr,
      hidden: 0,
      total: bestYr,
      baseLabel: modeDesc,
      hiddenLabel: 'This tier price is the advertised rate',
      bestHtml: '<strong>Recommended:</strong> ' + bestName + ' at $' + bestYr.toLocaleString('en-US') + '/yr.',
      ctaHref: '{JOTFORM_PARTNER_URL}',
      ctaLabel: 'View Jotform pricing',
      ctaVendor: 'jotform'
    }});
  }}
  document.getElementById('jf-tier-tbody').innerHTML = rows.map(r => `
    <tr>
      <td data-label="Jotform Tier"><strong>${{r.name}}</strong> <span class="status-pill status-verified">Verified</span> &middot; <a href="https://www.jotform.com/pricing/" target="_blank" rel="noopener">Verified source</a></td>
      <td data-label="Advertised Rate">${{r.rate}}</td>
      <td data-label="Included Quotas">${{r.quotas}}</td>
      <td data-label="Hidden Cost Highlight"><strong>Hidden Cost Highlight:</strong> ${{r.hidden}}</td>
      <td data-label="True Year-1 Cost"><strong>${{r.total}}</strong></td>
      <td data-label="Action"><a class="btn-secondary" href="${{r.url}}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="jotform" data-cta-location="jf-tier-table">View Jotform pricing &rarr;</a></td>
    </tr>
  `).join('');
}}
['jf-subs', 'jf-mode'].forEach(id => {{
  const el = document.getElementById(id);
  if (el) {{
    el.addEventListener('input', runJfTierCalc);
    el.addEventListener('change', runJfTierCalc);
  }}
}});
runJfTierCalc();
</script>
"""

    faqs = [
        (
            "How much does Jotform cost per month in 2026?",
            "On annual billing in 2026, Jotform Starter is free ($0/mo for 5 forms and 100 submissions/mo), Bronze is $34/mo (25 forms, 1,000 submissions/mo), Silver is $39/mo (50 forms, 2,500 submissions/mo), and Gold is $99/mo (100 forms, 10,000 submissions/mo, plus HIPAA BAA eligibility).",
        ),
        (
            "Does Jotform charge extra to embed forms on Wix?",
            "No. The official Jotform Wix App is free to install from the Wix App Market across all Jotform tiers, including the free Starter plan.",
        ),
    ]

    render_page(rel, title, desc, slug, wrap_calculator_shell(body), faqs=faqs)


if __name__ == "__main__":
    build_jotform_wix_guide()
    build_jotform_pricing_calculator()
