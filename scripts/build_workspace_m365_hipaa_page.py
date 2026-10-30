"""Builds /compliance/google-workspace-vs-microsoft-365-hipaa-baa-tiers/ (published 2026-10-27).
All prices and BAA rules verified 2026-10-27 against the sources listed in SOURCES.
Unverifiable figures (Google Enterprise pricing, Microsoft month-to-month premium on the
public US page) are labelled on the page instead of guessed."""
from layout import render_page, wrap_calculator_shell

SLUG = "/compliance/google-workspace-vs-microsoft-365-hipaa-baa-tiers/"
REL = "compliance/google-workspace-vs-microsoft-365-hipaa-baa-tiers/index.html"
TITLE = "Google Workspace vs M365 HIPAA BAA (2026) – saasbill.io"
DESC = ("Google Workspace vs. Microsoft 365 HIPAA BAA guide for 2026: the cheapest BAA-eligible editions both start at $7/user/mo. "
        "Compare Vault and archiving gaps, billing terms, auto-renewal and HIPAA form intake costs.")
JOTFORM = "https://www.jotform.com/hipaa/pricing/?partner=saasbill"
GW_PRICING = "https://workspace.google.com/pricing"
MS_PRICING = "https://www.microsoft.com/en-us/microsoft-365/business/compare-all-microsoft-365-business-products"

# Verified list prices (USD per user per month), Oct 27, 2026
GW = {"starter": 7, "standard": 14, "plus": 22}
GW_FLEX = {"starter": 8.40, "standard": 16.80, "plus": 26.40}
MS_NEW = {"basic": 7, "standard": 14, "premium": 22}       # effective July 1, 2026
MS_OLD = {"basic": 6, "standard": 12.50, "premium": 22}    # existing customers until renewal
EOA = 3

SOURCES = [
 ("Google Workspace Help: HIPAA Compliance with Google Workspace and Cloud Identity (BAA must be accepted before PHI; third-party add-ons not covered)", "https://support.google.com/a/answer/3407054?hl=en"),
 ("Google Workspace Help: Privacy compliance and records (super admin accepts the HIPAA Business Associate Amendment under Account settings > Legal and compliance; legacy free edition cannot)", "https://knowledge.workspace.google.com/admin/compliance/privacy-compliance-and-records-for-google-workspace-and-cloud-identity"),
 ("Google: HIPAA Included Functionality (Gmail, Calendar, Drive incl. Docs/Sheets/Forms, Meet, Chat, Vault if applicable, Gemini in Workspace, Voice managed users only)", "https://workspace.google.com/terms/2015/1/hipaa_functionality/"),
 ("Google Workspace pricing page (Starter $7, Standard $14, Plus $22 per user/mo; Vault from Business Plus; 300-user cap; 50% intro offer for first 20 users for 12 months)", "https://workspace.google.com/intl/en/pricing.html"),
 ("Google Workspace Help: Understand bills & charges (Flexible $8.40 / $16.80 / $26.40 vs Annual $7 / $14 / $22; annual licenses reduced only at renewal)", "https://support.google.com/a/answer/1230658?hl=en"),
 ("Google Workspace Help: Flexible Plan (cancel any time; 20 to 50 user cap in the first 90 days)", "https://support.google.com/a/answer/1247362?hl=en"),
 ("Google Workspace Help: Renew your Annual/Fixed-Term Plan (auto-renews for one year; reminders 30 and 3 days before)", "https://knowledge.workspace.google.com/admin/billing/renew-your-annual-fixed-term-plan-contract"),
 ("Microsoft Learn: HIPAA & HITECH offering (BAA included by default via the Data Protection Addendum; in-scope services incl. Exchange Online, Teams, SharePoint, OneDrive, Forms, Copilot)", "https://learn.microsoft.com/en-us/compliance/regulatory/offering-hipaa-hitech"),
 ("Microsoft Licensing: Microsoft 365 pricing and packaging updates effective July 1, 2026 (Business Basic $6 to $7, Business Standard $12.50 to $14, Business Premium $22 unchanged; existing customers keep current price until renewal)", "https://www.microsoft.com/en-us/licensing/news/2026-m365-packaging-pricing-updates"),
 ("Microsoft 365 business plan comparison (annual subscription auto-renews; 7-day prorated refund window; monthly vs annual commitment options)", MS_PRICING),
 ("Microsoft Partner Center, March 2025 announcements (annual-term subscriptions billed monthly priced 5% higher than upfront billing from April 1, 2025)", "https://learn.microsoft.com/en-us/partner-center/announcements/2025-march"),
 ("Microsoft Learn: Exchange Online service description (Basic/Standard lack In-Place/Litigation Hold, manual retention policies and DLP; Business Premium includes them)", "https://learn.microsoft.com/en-us/office365/servicedescriptions/exchange-online-service-description/exchange-online-service-description"),
 ("Microsoft Learn: Exchange Online Archiving service description (add-on for Business Basic and Standard; already included in Business Premium)", "https://learn.microsoft.com/en-us/office365/servicedescriptions/exchange-online-archiving-service-description/exchange-online-archiving-service-description"),
 ("Microsoft Q&A: How to get a BAA with Microsoft Business Basic (Jan 2026 user thread)", "https://learn.microsoft.com/en-us/answers/questions/5747401/how-to-get-a-baa-with-microsoft-business-basic"),
 ("Microsoft Q&A: Where to find the BAA for Microsoft 365 Business Standard (Jan 2024 user thread)", "https://learn.microsoft.com/en-us/answers/questions/5295837/where-to-find-the-business-associate-agreement-for"),
 ("Jotform HIPAA pricing (Gold $99/mo billed annually or $129 monthly; HIPAA features on Gold and Enterprise only; 10,000 submissions, 1,000 signed documents, 1 user)", "https://www.jotform.com/hipaa/pricing/"),
]

def rows_sources():
    return "\n".join(f'<li><a href="{u}" target="_blank" rel="noopener">{t}</a> &middot; <em>verified Oct 27, 2026</em></li>' for t, u in SOURCES)

f0 = lambda n: f"{n:,.0f}"
S = 10  # example seats
EX_ENTRY = S * 7 * 12
EX_PLUS = S * 22 * 12
EX_BASIC_EOA = S * (7 + EOA) * 12

body = f"""
<section class="hero">
  <h1>Google Workspace vs. Microsoft 365 HIPAA BAA Guide (2026): Exact Minimum Editions &amp; Form Intake Rules</h1>
  <p class="lead">In 2026 the cheapest edition you can run under a HIPAA BAA costs $7 per user per month on both suites: Google Workspace Business Starter on the Annual plan and Microsoft 365 Business Basic paid yearly (sources: Google Workspace pricing and Microsoft 365 pricing pages, verified Oct 27, 2026). The real cost gap opens when you need retention and legal hold, pay month to month, or add a dedicated HIPAA intake form.</p>
  <div class="geo-direct-answer">
    <p><strong>The short version:</strong> Google lets a super admin accept its <strong>HIPAA Business Associate Amendment</strong> in the Admin console on paid Workspace editions (only the legacy free edition is excluded). Microsoft includes its <strong>HIPAA BAA by default</strong> in the Data Protection Addendum for covered entities and business associates, with nothing to click. For {S} users on annual terms, the entry tier costs <strong>${f0(EX_ENTRY)}/yr on either suite</strong>. If you need retention and holds, Google requires <strong>Business Plus ($22, Vault included)</strong> and Microsoft offers <strong>Business Premium ($22)</strong>, both <strong>${f0(EX_PLUS)}/yr</strong>, or the narrower <strong>Business Basic + Exchange Online Archiving ($7 + $3)</strong> at <strong>${f0(EX_BASIC_EOA)}/yr</strong>. Native Google Forms and Microsoft Forms are both on the BAA service lists; a dedicated HIPAA form tool such as <strong>Jotform Gold</strong> adds <strong>$1,188/yr</strong> (annual billing) for e-signatures, payments and encrypted intake.</p>
  </div>
</section>

<section aria-labelledby="facts-heading">
  <h2 id="facts-heading">What the official terms say in 2026</h2>
  <ul class="key-list">
    <li><strong>Google accepts the BAA in the Admin console:</strong> a super administrator goes to Account &rarr; Account settings &rarr; Legal and compliance, opens the Google Workspace/Cloud Identity HIPAA Business Associate Amendment, answers three questions and clicks OK. A screenshot of that page is Google's stated proof of acceptance.</li>
    <li><strong>Microsoft's BAA is automatic:</strong> Microsoft states the HIPAA BAA is available through the Microsoft Online Services Data Protection Addendum by default to all customers who are covered entities or business associates. You download the DPA or BAA from the Service Trust Portal for your files.</li>
    <li><strong>Google covered services:</strong> Gmail, Calendar, Drive (including Docs, Sheets, Slides, Forms), Meet, Chat, Groups, Keep, Sites, Tasks, AppSheet, Gemini in Workspace, Vault (if applicable) and Voice (managed users only). Third-party apps and Marketplace add-ons are not covered.</li>
    <li><strong>Microsoft covered services (commercial):</strong> Exchange Online, Teams, SharePoint Online, OneDrive for Business, Forms, Planner, Power Apps, Power BI, Microsoft Copilot and Copilot Chat, Entra ID and more.</li>
    <li><strong>Retention is the tier trap:</strong> Google Vault is not included in Business Starter or Standard. Microsoft 365 Business Basic and Standard do not include In-Place Hold, Litigation Hold or manual retention policies; Business Premium does, and Basic or Standard can add Exchange Online Archiving for holds and archive.</li>
    <li><strong>Microsoft raised prices on July 1, 2026:</strong> Business Basic went from $6 to $7 and Business Standard from $12.50 to $14; Business Premium stayed at $22. Existing customers keep the old price until renewal.</li>
  </ul>
</section>

<section class="calc-box">
  <h2 style="margin-top:0;">Calculate the cheapest BAA-eligible edition on each suite</h2>
  <p style="color:var(--muted); margin-bottom:20px; font-size:0.95rem;">Same seat count, same billing term and the closest feature level on both sides. Feature differences that remain are written into each row.</p>
  <div class="calc-grid">
    <div class="control-group">
      <label for="gm-seats">Users (seats): <span class="val-pill" id="gm-seats-val">10</span></label>
      <input type="range" id="gm-seats" min="1" max="300" value="10" />
    </div>
    <div class="control-group">
      <label for="gm-tier">Feature level you need</label>
      <select id="gm-tier">
        <option value="entry" selected>Email, files, video (entry tier)</option>
        <option value="mid">Larger storage, recordings, booking (mid tier)</option>
        <option value="retention">Retention, legal hold &amp; eDiscovery</option>
      </select>
    </div>
    <div class="control-group">
      <label for="gm-term">Billing term (both suites)</label>
      <select id="gm-term">
        <option value="annual" selected>Annual commitment, paid upfront</option>
        <option value="annual_monthly">Annual commitment, paid monthly</option>
        <option value="flex">No commitment (month to month)</option>
      </select>
    </div>
    <div class="control-group">
      <label for="gm-mslist">Microsoft price list</label>
      <select id="gm-mslist">
        <option value="new" selected>New purchase or renewal (from Jul 1, 2026)</option>
        <option value="old">Existing contract before renewal</option>
      </select>
    </div>
    <div class="control-group">
      <label for="gm-promo">Google intro offer (new customers)</label>
      <select id="gm-promo">
        <option value="0" selected>List price (no promo)</option>
        <option value="1">50% off first 20 users for 12 months</option>
      </select>
    </div>
    <div class="control-group">
      <label for="gm-forms">HIPAA form intake add-on</label>
      <select id="gm-forms">
        <option value="0" selected>Native forms only (Google Forms / Microsoft Forms)</option>
        <option value="1">Add Jotform Gold (HIPAA features, 1 account)</option>
      </select>
    </div>
  </div>
  <div id="gm-summary" class="summary-strip" aria-live="polite"></div>
  <p class="summary-interpretation"><strong>How to read this comparison:</strong> Both suites now list the same per-user prices at each tier, so the Year-1 gap comes from billing term surcharges, the old vs. new Microsoft price list, Google's intro offer and what each tier leaves out. A lower total is not automatically the right fit; check which apps your staff will actually use for PHI.</p>
  <div class="table-wrap mobile-cards">
    <table>
      <caption>Year-1 cost of the cheapest BAA-eligible edition per suite (USD list prices, verified Oct 27, 2026)</caption>
      <thead><tr><th>Suite &amp; edition</th><th>BAA route</th><th>Price / user / mo</th><th>Seats</th><th>Add-ons / yr</th><th>Year-1 total</th><th>Next step</th></tr></thead>
      <tbody id="gm-tbody"></tbody>
    </table>
  </div>
  <p id="gm-note" style="font-size:0.84rem; color:var(--muted); margin-top:10px;"></p>
</section>

<section aria-labelledby="min-edition-heading">
  <h2 id="min-edition-heading">Minimum edition by HIPAA requirement</h2>
  <p class="section-tldr">Signing the BAA is free on both suites. What you pay for is the tier that contains the controls your compliance program needs.</p>
  <div class="table-wrap mobile-cards">
    <table>
      <caption>Cheapest BAA-eligible edition per requirement (verified Oct 27, 2026)</caption>
      <thead><tr><th>Requirement</th><th>Google Workspace</th><th>Microsoft 365</th><th>Feature difference to note</th></tr></thead>
      <tbody>
        <tr><td data-label="Requirement"><strong>BAA in place + email, files, video</strong></td><td data-label="Google Workspace">Business Starter, $7 annual / $8.40 Flexible</td><td data-label="Microsoft 365">Business Basic, $7 paid yearly</td><td data-label="Feature difference">Starter has 30 GB pooled storage per user; Basic has 1 TB OneDrive per user and web/mobile Office apps only.</td></tr>
        <tr><td data-label="Requirement"><strong>Mid tier (recordings, more storage, desktop apps)</strong></td><td data-label="Google Workspace">Business Standard, $14 annual / $16.80 Flexible</td><td data-label="Microsoft 365">Business Standard, $14 paid yearly</td><td data-label="Feature difference">Google adds 2 TB pooled storage, Meet recording and booking pages; Microsoft adds installed desktop Office apps and webinars.</td></tr>
        <tr><td data-label="Requirement"><strong>Retention rules, legal hold, eDiscovery</strong></td><td data-label="Google Workspace">Business Plus, $22 annual / $26.40 Flexible (Vault)</td><td data-label="Microsoft 365">Business Premium, $22 paid yearly; or Basic + Exchange Online Archiving ($7 + $3)</td><td data-label="Feature difference">Basic + archiving adds holds and archive mailboxes, but not manual retention policies or DLP, which Premium includes.</td></tr>
        <tr><td data-label="Requirement"><strong>DLP, S/MIME, context-aware access</strong></td><td data-label="Google Workspace">Enterprise editions (price not published; sales quote)</td><td data-label="Microsoft 365">Business Premium includes Purview DLP; S/MIME is listed for all Exchange plans</td><td data-label="Feature difference">We could not verify a public Google Enterprise price, so the calculator does not model this tier.</td></tr>
      </tbody>
    </table>
  </div>
</section>

<section aria-labelledby="baa-heading">
  <h2 id="baa-heading">How the BAA is actually put in place</h2>
  <div class="table-wrap mobile-cards">
    <table>
      <caption>BAA mechanics: Google Workspace vs. Microsoft 365 (verified Oct 27, 2026)</caption>
      <thead><tr><th>Item</th><th>Google Workspace</th><th>Microsoft 365</th></tr></thead>
      <tbody>
        <tr><td data-label="Item"><strong>Document name</strong></td><td data-label="Google Workspace">Google Workspace/Cloud Identity HIPAA Business Associate Amendment</td><td data-label="Microsoft 365">Microsoft HIPAA Business Associate Agreement, part of the Products and Services Data Protection Addendum</td></tr>
        <tr><td data-label="Item"><strong>How you accept</strong></td><td data-label="Google Workspace">Super admin clicks Review and Accept in Admin console, Account settings, Legal and compliance</td><td data-label="Microsoft 365">No click required; applies by default to covered entities and business associates</td></tr>
        <tr><td data-label="Item"><strong>Proof for auditors</strong></td><td data-label="Google Workspace">Screenshot of the acceptance shown in Legal and compliance</td><td data-label="Microsoft 365">Download the DPA or BAA from the Service Trust Portal with a work account</td></tr>
        <tr><td data-label="Item"><strong>Excluded</strong></td><td data-label="Google Workspace">Legacy free edition; third-party apps and add-ons; Additional Google Services</td><td data-label="Microsoft 365">Services not on the in-scope list; consumer Microsoft accounts</td></tr>
        <tr><td data-label="Item"><strong>Native forms on the BAA</strong></td><td data-label="Google Workspace">Yes, Google Forms (via Drive)</td><td data-label="Microsoft 365">Yes, Microsoft Forms</td></tr>
        <tr><td data-label="Item"><strong>AI assistant on the BAA</strong></td><td data-label="Google Workspace">Gemini in Workspace and Gemini app (not Gemini in Chrome)</td><td data-label="Microsoft 365">Microsoft Copilot and Copilot Chat (commercial)</td></tr>
      </tbody>
    </table>
  </div>
</section>

<section aria-labelledby="terms-heading">
  <h2 id="terms-heading">Billing terms, seat limits and auto-renewal</h2>
  <div class="table-wrap mobile-cards">
    <table>
      <caption>Contract terms compared (verified Oct 27, 2026)</caption>
      <thead><tr><th>Term</th><th>Google Workspace (Business)</th><th>Microsoft 365 (Business)</th></tr></thead>
      <tbody>
        <tr><td data-label="Term"><strong>Seat minimum / maximum</strong></td><td data-label="Google Workspace">From 1 user; Business plans capped at 300 users</td><td data-label="Microsoft 365">No minimum published; Business plans capped at 300 users</td></tr>
        <tr><td data-label="Term"><strong>Month-to-month price</strong></td><td data-label="Google Workspace">Flexible Plan: $8.40 / $16.80 / $26.40</td><td data-label="Microsoft 365">Monthly commitment available; roughly 20% above annual per partner price guides (not printed on Microsoft's US page) <span class="badge badge-medium">estimate</span></td></tr>
        <tr><td data-label="Term"><strong>Annual term paid monthly</strong></td><td data-label="Google Workspace">Same annual price ($7 / $14 / $22), billed monthly or annually by region</td><td data-label="Microsoft 365">5% above upfront annual billing since April 1, 2025</td></tr>
        <tr><td data-label="Term"><strong>Auto-renewal</strong></td><td data-label="Google Workspace">Annual plan renews for one year if you do nothing; reminders 30 and 3 days before</td><td data-label="Microsoft 365">Annual subscription auto-renews; recurring billing can be turned off in the admin center</td></tr>
        <tr><td data-label="Term"><strong>Reducing seats</strong></td><td data-label="Google Workspace">Annual licenses can only be reduced at renewal; Flexible any time</td><td data-label="Microsoft 365">Annual paid upfront: no refund after the 7-day window; annual paid monthly may incur early-cancel penalties</td></tr>
        <tr><td data-label="Term"><strong>Extra costs to plan for</strong></td><td data-label="Google Workspace">Vault needs Business Plus or higher; intro offer ends after 12 months</td><td data-label="Microsoft 365">Exchange Online Archiving $3/user/mo on Basic or Standard; Purview Message Encryption needs Premium or an add-on</td></tr>
      </tbody>
    </table>
  </div>
</section>

<section aria-labelledby="forms-heading">
  <h2 id="forms-heading">Form intake: native forms vs. a dedicated HIPAA form tool</h2>
  <p class="section-tldr">Both suites list their own forms product under the BAA, so a basic intake questionnaire costs nothing extra. A dedicated tool is worth paying for when you need e-signatures, card payments or encrypted submissions on the same form.</p>
  <div class="table-wrap mobile-cards">
    <table>
      <caption>HIPAA form intake options (verified Oct 27, 2026)</caption>
      <thead><tr><th>Option</th><th>Extra cost</th><th>Covered by a BAA</th><th>Limits &amp; notes</th><th>Next step</th></tr></thead>
      <tbody>
        <tr><td data-label="Option"><strong>Google Forms</strong></td><td data-label="Extra cost">$0 (included in Workspace)</td><td data-label="Covered by a BAA">Yes, under Google's BAA (Drive incl. Forms)</td><td data-label="Limits &amp; notes">Responses live in Drive/Sheets; Marketplace form add-ons are not covered</td><td data-label="Next step"><a class="btn-secondary" href="{GW_PRICING}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="google-workspace" data-cta-location="forms-table">View Google Workspace plans &rarr;</a></td></tr>
        <tr><td data-label="Option"><strong>Microsoft Forms</strong></td><td data-label="Extra cost">$0 (included in Microsoft 365)</td><td data-label="Covered by a BAA">Yes, listed in Microsoft's in-scope services</td><td data-label="Limits &amp; notes">Responses stored in Forms/Excel within your tenant</td><td data-label="Next step"><a class="btn-secondary" href="{MS_PRICING}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="microsoft-365" data-cta-location="forms-table">View Microsoft 365 plans &rarr;</a></td></tr>
        <tr><td data-label="Option"><strong>Jotform Gold</strong></td><td data-label="Extra cost">$99/mo billed annually ($1,188/yr) or $129/mo monthly</td><td data-label="Covered by a BAA">HIPAA features on Gold and Enterprise only</td><td data-label="Limits &amp; notes">10,000 submissions/mo, 1,000 signed documents/mo, 1,000 payment submissions/mo, 1 user account</td><td data-label="Next step"><a class="btn-cta" href="{JOTFORM}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="jotform-hipaa" data-cta-location="forms-table">View Jotform HIPAA pricing &rarr;</a></td></tr>
      </tbody>
    </table>
  </div>
</section>

<section aria-labelledby="evidence-heading">
  <h2 id="evidence-heading">What admins run into</h2>
  <p class="section-tldr">The most common friction we found is not price but paperwork: small practices on Microsoft 365 cannot find a BAA to sign because there is nothing to sign.</p>
  <div class="evidence-box">
    <strong>1. "I cannot find the HIPPA/HITECH BAA to review or accept."</strong>
    <p style="margin-top:6px;">A Microsoft 365 Business Basic customer in January 2026, following older guides that pointed to an acceptance screen in the admin center. A Microsoft moderator replied that those pages are no longer available and that the BAA applies by default through the Data Protection Addendum.</p>
    <cite>Source: <a href="https://learn.microsoft.com/en-us/answers/questions/5747401/how-to-get-a-baa-with-microsoft-business-basic" target="_blank" rel="noopener">Microsoft Q&amp;A, "How to get a BAA with Microsoft Business Basic" (Jan 2026)</a></cite>
  </div>
  <div class="evidence-box">
    <strong>2. "If a government authority tells me 'Show us your BAA signed with Microsoft', what do I do? Where is it?"</strong>
    <p style="margin-top:6px;">A Business Standard customer asking where the actual agreement lives. The answer was to download the DPA and follow its link to the full BAA text.</p>
    <cite>Source: <a href="https://learn.microsoft.com/en-us/answers/questions/5295837/where-to-find-the-business-associate-agreement-for" target="_blank" rel="noopener">Microsoft Q&amp;A, "Where to Find the Business Associate Agreement..." (Jan 2024)</a></cite>
  </div>
  <div class="evidence-box">
    <strong>3. Google's own warning: no BAA, no PHI</strong>
    <p style="margin-top:6px;">Google's help center states that customers who have not signed a BAA must not use PHI in Google Workspace, and that third-party applications including add-ons are not covered by the BAA.</p>
    <cite>Source: <a href="https://support.google.com/a/answer/3407054?hl=en" target="_blank" rel="noopener">Google Workspace Help, HIPAA Compliance with Google Workspace and Cloud Identity</a></cite>
  </div>
</section>

<section aria-labelledby="howto-heading">
  <h2 id="howto-heading">Setup checklist before any PHI goes in</h2>
  <ol class="key-list">
    <li><strong>Google:</strong> sign in as super admin, accept the HIPAA Business Associate Amendment under Account settings &rarr; Legal and compliance, and save a screenshot.</li>
    <li><strong>Microsoft:</strong> download the Data Protection Addendum and BAA from the Service Trust Portal and file it with your subscription records.</li>
    <li><strong>Turn off what is not covered:</strong> disable Marketplace or AppSource add-ons and any service outside the included functionality list for users who handle PHI.</li>
    <li><strong>Decide on retention up front:</strong> if you need holds or retention rules, budget for Google Business Plus, Microsoft 365 Business Premium or Exchange Online Archiving from day one.</li>
    <li><strong>Calendar the renewal:</strong> both annual plans auto-renew; Google sends reminders 30 and 3 days before, and annual seats can only be reduced at renewal.</li>
  </ol>
</section>

<section aria-labelledby="methodology-heading">
  <h2 id="methodology-heading">Methodology &amp; assumptions</h2>
  <ul class="key-list">
    <li><strong>Apples to apples:</strong> each calculator row uses the same seat count and billing term on both suites, and pairs tiers by the HIPAA-relevant capability (entry, mid, retention). Remaining feature differences are written into the row itself.</li>
    <li><strong>Prices:</strong> US list prices in USD per user per month, before tax, reseller discounts or nonprofit pricing, checked on official vendor pages on Oct 27, 2026.</li>
    <li><strong>Microsoft monthly commitment:</strong> modeled at 20% above the annual price based on partner price guides, because Microsoft's public US page does not print the month-to-month price. Rows using it are labelled as an estimate.</li>
    <li><strong>Exchange Online Archiving:</strong> $3 per user per month is the annual-commitment list price; for other terms we apply the same 5% or 20% term surcharge as the base plan (estimate).</li>
    <li><strong>Google intro offer:</strong> 50% off the first 20 users for 12 months, shown on Google's pricing page for new customers; applied only to annual terms when switched on.</li>
    <li><strong>Not modeled:</strong> Google Enterprise editions (no public price), Microsoft 365 E3/E5, Copilot add-ons, Teams Phone and Google Voice.</li>
  </ul>
</section>

<section aria-labelledby="sources-heading">
  <h2 id="sources-heading">Sources &amp; verification dates</h2>
  <ol class="key-list" style="font-size:0.9rem;">
    {rows_sources()}
  </ol>
</section>
"""

script = """
<script>
const GW = {starter:{annual:7, flex:8.40}, standard:{annual:14, flex:16.80}, plus:{annual:22, flex:26.40}};
const MS = {new:{basic:7, standard:14, premium:22}, old:{basic:6, standard:12.50, premium:22}};
const EOA = 3;
const JF = {annual:99, monthly:129};
const URLS = {gw:'https://workspace.google.com/pricing', ms:'https://www.microsoft.com/en-us/microsoft-365/business/compare-all-microsoft-365-business-products', jf:'https://www.jotform.com/hipaa/pricing/?partner=saasbill'};
const fmt = n => '$' + Math.round(n).toLocaleString('en-US');
const fmt2 = n => '$' + n.toFixed(2);
function msRate(base, term) {
  if (term === 'annual_monthly') return Math.round(base * 1.05 * 100) / 100;
  if (term === 'flex') return Math.round(base * 1.20 * 100) / 100;
  return base;
}
function gwRate(ed, term) { return term === 'flex' ? GW[ed].flex : GW[ed].annual; }
function updateGm() {
  const seats = parseInt(document.getElementById('gm-seats').value, 10);
  const tier = document.getElementById('gm-tier').value;
  const term = document.getElementById('gm-term').value;
  const list = document.getElementById('gm-mslist').value;
  const promo = document.getElementById('gm-promo').value === '1';
  const forms = document.getElementById('gm-forms').value === '1';
  document.getElementById('gm-seats-val').textContent = seats;
  const gEd = tier === 'entry' ? 'starter' : (tier === 'mid' ? 'standard' : 'plus');
  const gName = {starter:'Business Starter', standard:'Business Standard', plus:'Business Plus (Vault)'}[gEd];
  const mEd = tier === 'entry' ? 'basic' : (tier === 'mid' ? 'standard' : 'premium');
  const mName = {basic:'Business Basic', standard:'Business Standard', premium:'Business Premium'}[mEd];
  const gRate = gwRate(gEd, term);
  const promoSeats = (promo && term !== 'flex') ? Math.min(seats, 20) : 0;
  const gYr = (seats * gRate - promoSeats * gRate * 0.5) * 12;
  const mRate = msRate(MS[list][mEd], term);
  const mYr = seats * mRate * 12;
  const jfYr = forms ? (term === 'flex' ? JF.monthly : JF.annual) * 12 : 0;
  const termLabel = {annual:'annual commitment paid upfront', annual_monthly:'annual commitment paid monthly', flex:'month-to-month'}[term];
  const scenarioLine = `Based on ${seats} user${seats===1?'':'s'}, ${termLabel}, ${tier === 'entry' ? 'entry' : (tier === 'mid' ? 'mid' : 'retention')} tier${forms ? ', plus Jotform Gold intake' : ''}`;
  const msEst = term === 'flex' ? ' (estimate)' : '';
  const rows = [
    {id:'google-workspace', name:'Google Workspace ' + gName, baa:'Accept HIPAA amendment in Admin console', rate:gRate, rateText: fmt2(gRate) + (promoSeats ? ' (50% off ' + promoSeats + ' seats, yr 1)' : ''), addon:jfYr, addonText: forms ? fmt(jfYr) + ' Jotform Gold' : '$0', yr:gYr + jfYr, url:URLS.gw, cta:'View Google Workspace plans', diff: gEd === 'starter' ? '30 GB pooled storage/user; no Vault' : (gEd === 'standard' ? '2 TB pooled/user; no Vault' : 'Vault retention, holds, eDiscovery'), status:'Verified'},
    {id:'microsoft-365', name:'Microsoft 365 ' + mName, baa:'Included by default via DPA', rate:mRate, rateText: fmt2(mRate) + msEst, addon:jfYr, addonText: forms ? fmt(jfYr) + ' Jotform Gold' : '$0', yr:mYr + jfYr, url:URLS.ms, cta:'View Microsoft 365 plans', diff: mEd === 'basic' ? '1 TB OneDrive/user; web apps; no holds' : (mEd === 'standard' ? 'Desktop apps; no holds' : 'Archiving, holds, retention, DLP'), status: term === 'flex' ? 'Estimated (Benchmark)' : 'Verified'}
  ];
  if (tier === 'retention') {
    const eoaRate = msRate(EOA, term);
    const bRate = msRate(MS[list].basic, term);
    const bYr = seats * (bRate + eoaRate) * 12;
    rows.push({id:'microsoft-365', name:'Microsoft 365 Business Basic + Exchange Online Archiving', baa:'Included by default via DPA', rate:bRate + eoaRate, rateText: fmt2(bRate) + ' + ' + fmt2(eoaRate) + (term !== 'annual' ? ' (estimate)' : ''), addon:jfYr, addonText: forms ? fmt(jfYr) + ' Jotform Gold' : '$0', yr:bYr + jfYr, url:URLS.ms, cta:'View Microsoft 365 plans', diff:'Holds and archive only; no retention policies or DLP', status: term !== 'annual' ? 'Estimated (Benchmark)' : 'Verified'});
  }
  rows.sort((a, b) => a.yr - b.yr);
  const low = rows[0];
  const high = rows[rows.length - 1];
  const gap = high.yr - low.yr;
  const tie = Math.abs(rows[0].yr - rows[1].yr) < 0.5;
  let hidden;
  if (tier !== 'retention') {
    const gPlusYr = seats * gwRate('plus', term) * 12;
    hidden = `Neither ${gName} nor ${mName} includes legal hold or retention rules. Adding them means Google Business Plus (${fmt(gPlusYr)}/yr for ${seats} users) or Exchange Online Archiving on Microsoft (+${fmt(seats * msRate(EOA, term) * 12)}/yr).`;
  } else {
    hidden = `On Google, Vault is only in Business Plus, so retention costs ${fmt(seats * (gwRate('plus', term) - gwRate('starter', term)) * 12)}/yr more than Business Starter for ${seats} users.`;
  }
  if (term === 'annual_monthly') hidden += ' Microsoft prices annual terms paid monthly 5% above upfront billing; Google does not.';
  if (list === 'old') hidden += ' Your Microsoft price rises to the July 2026 list at renewal.';
  const summary = document.getElementById('gm-summary');
  if (summary) {
    summary.innerHTML = `
      <div class="summary-card card-hidden">
        <div class="summary-label">Year-1 gap between options</div>
        <div class="summary-metric" style="color:var(--rose);">${gap > 0.5 ? fmt(gap) + ' / yr' : '$0: same list price'}</div>
        <div class="summary-scenario">${scenarioLine}</div>
        <div class="summary-breakdown">${rows.map(r => r.name + ': ' + fmt(r.yr)).join(' &middot; ')}</div>
        <div class="summary-caveat"><strong>Hidden Cost Highlight:</strong> ${hidden}</div>
        <div class="summary-actions">
          <div class="cta-stack">
            <a class="btn-secondary" href="${high.url}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="${high.id}" data-cta-location="summary-card">${high.cta} &rarr;</a>
          </div>
        </div>
      </div>
      <div class="summary-card card-lowest">
        <div class="summary-label">${tie ? 'Year-1 total on both suites' : 'Lowest Year-1 total at this feature level'}</div>
        <div class="summary-metric" style="color:var(--emerald);">${fmt(low.yr)} / yr</div>
        <div class="summary-scenario">${tie ? 'Tie at list price: decide on features, not price' : low.name}</div>
        <div class="summary-breakdown">${fmt(low.yr - low.addon)} licenses + ${fmt(low.addon)} form intake</div>
        <div class="summary-caveat"><strong>Feature note:</strong> ${low.diff}. Native Google Forms and Microsoft Forms are both on the BAA lists.</div>
        <div class="summary-actions">
          <div class="cta-stack">
            <a class="btn-cta" href="${low.url}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="${low.id}" data-cta-location="summary-card">${low.cta} &rarr;</a>
          </div>
          <a class="summary-audit-link" href="${URLS.jf}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="jotform-hipaa" data-cta-location="summary-card">Need e-signatures or payments on intake? View Jotform HIPAA pricing &rarr;</a>
        </div>
      </div>`;
  }
  if (typeof window.saasbillApplyWorkbench === 'function') {
    window.saasbillApplyWorkbench({
      product: high.name,
      sticker: Math.max(0, high.yr - high.addon),
      hidden: high.addon,
      total: high.yr,
      baseLabel: 'Suite licenses',
      hiddenLabel: high.addon ? 'Jotform Gold intake' : 'No add-on on this scenario',
      bestHtml: '<strong>Lowest modeled cost:</strong> ' + low.name + ' at $' + Math.round(low.yr).toLocaleString() + '/yr.',
      ctaHref: low.url,
      ctaLabel: low.cta,
      ctaVendor: low.id
    });
  }
  document.getElementById('gm-tbody').innerHTML = rows.map(r => `
    <tr>
      <td data-label="Suite &amp; edition"><strong>${r.name}</strong> <span class="status-pill status-verified">${r.status}</span><div style="font-size:0.78rem; color:var(--muted);">${r.diff}</div><div class="source-inline">Verified source: <a href="${r.url}" target="_blank" rel="noopener">Official pricing &nearr;</a></div></td>
      <td data-label="BAA route">${r.baa}</td>
      <td data-label="Price / user / mo" style="font-family:var(--sans); font-variant-numeric:tabular-nums;">${r.rateText}</td>
      <td data-label="Seats"><span class="badge badge-low">${seats} (1:1, max 300)</span></td>
      <td data-label="Add-ons / yr">${r.addonText}</td>
      <td data-label="Year-1 total" class="price-highlight">${fmt(r.yr)}<div class="cell-scenario">${scenarioLine}</div></td>
      <td data-label="Next step"><div class="cta-stack"><a class="btn-secondary" href="${r.url}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="${r.id}" data-cta-location="table-row">${r.cta} &rarr;</a></div></td>
    </tr>`).join('');
  let note = 'Assumptions: US list prices, same seats and billing term on both suites, no taxes or reseller discounts.';
  if (term === 'flex') note += ' Microsoft month-to-month modeled at +20% over annual (partner price guides; not printed on Microsoft\\'s US page).';
  if (promo && term === 'flex') note += ' Google intro offer not applied to month-to-month terms.';
  if (forms) note += ' Jotform Gold is a single-user account at a flat price; multi-user Jotform needs an Enterprise quote.';
  document.getElementById('gm-note').textContent = note;
}
['gm-seats','gm-tier','gm-term','gm-mslist','gm-promo','gm-forms'].forEach(id => document.getElementById(id).addEventListener('input', updateGm));
updateGm();
</script>
"""

faqs = [
 ("Which Google Workspace editions are covered by Google's HIPAA BAA in 2026?",
  "Google's HIPAA Business Associate Amendment can be accepted by a super administrator on paid Google Workspace editions, starting with Business Starter at $7 per user per month on the Annual plan ($8.40 Flexible). Google's help center says only users of the legacy free edition and non-administrators cannot accept it. Vault, which handles retention and legal hold, starts at Business Plus ($22 annual)."),
 ("How do I accept the Google Workspace BAA?",
  "Sign in to the Google Admin console as a super administrator, go to Account, Account settings, Legal and compliance, open the Google Workspace/Cloud Identity HIPAA Business Associate Amendment, click Review and Accept, answer the three questions and click OK. Google says a screenshot of that page is your proof of acceptance."),
 ("Does Microsoft 365 Business Basic include a HIPAA BAA?",
  "Yes. Microsoft states that its HIPAA BAA is available through the Microsoft Online Services Data Protection Addendum by default to all customers who are covered entities or business associates, and Exchange Online, Teams, SharePoint, OneDrive and Forms are in scope. There is nothing to sign; download the DPA from the Service Trust Portal for your records. Business Basic costs $7 per user per month paid yearly since July 1, 2026."),
 ("Is Google Workspace or Microsoft 365 cheaper for HIPAA in 2026?",
  "At list price they tie at every tier: $7 entry (Business Starter vs. Business Basic), $14 mid (Business Standard on both) and $22 for retention (Business Plus vs. Business Premium) per user per month on annual terms. Differences come from billing: Microsoft charges 5% more for annual terms paid monthly, existing Microsoft customers keep $6 and $12.50 until renewal, and Google offers new customers 50% off the first 20 users for 12 months."),
 ("Can I use Google Forms or Microsoft Forms for HIPAA patient intake?",
  "Both are listed as covered services: Google Forms under Drive in Google's HIPAA Included Functionality, and Microsoft Forms in Microsoft's in-scope services. A dedicated tool such as Jotform Gold ($99 per month billed annually, $129 monthly) adds HIPAA form features, e-signatures (1,000 signed documents per month) and payment collection on the same form."),
 ("Do Google Workspace and Microsoft 365 annual plans auto-renew?",
  "Yes. Google's Annual/Fixed-Term Plan automatically renews for one year if you do nothing, with reminders 30 and 3 days before, and annual licenses can only be reduced at renewal. Microsoft 365 annual subscriptions also auto-renew; there is a 7-day window for a prorated refund, and annual terms paid upfront are not refunded if cancelled early."),
]

extra = {"@type": "Dataset", "name": "Google Workspace & Microsoft 365 HIPAA BAA edition and price data (verified 2026-10-27)",
         "description": "BAA acceptance rules, covered services, per-user list prices by billing term, archiving add-ons, renewal terms and HIPAA form intake prices.",
         "creator": {"@type": "Organization", "name": "SaaSBill Editorial"}, "dateModified": "2026-10-27",
         "isBasedOn": [u for _, u in SOURCES], "license": "https://creativecommons.org/licenses/by/4.0/"}

render_page(REL, TITLE, DESC, SLUG, wrap_calculator_shell(body) + script, faqs=faqs, extra_schema=extra, published_date="2026-10-27")
