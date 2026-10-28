import json
import os
from datetime import datetime

# Repo root (this file lives in scripts/). Published pages are copied from public/ to the root for GitHub Pages.
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
PUBLIC_DIR = os.path.join(BASE_DIR, "public")
SITE_ORIGIN = "https://saasbill.io"
BASE_PATH = ""

def get_freshness_timestamps():
    now_local = datetime.now().astimezone()
    iso_date = now_local.strftime("%Y-%m-%d")
    iso_datetime = now_local.isoformat(timespec="seconds")
    human_date = now_local.strftime("%b %d, %Y")
    return iso_date, iso_datetime, human_date

def load_data():
    with open(os.path.join(DATA_DIR, "tools.json")) as f:
        tools = json.load(f)
    with open(os.path.join(DATA_DIR, "affiliate_links.json")) as f:
        affiliates = json.load(f)
    return tools, affiliates

def render_related_links(rel_path, prefix):
    if rel_path == "index.html":
        return ""
    all_links = [
        ("index.html", "Year-1 SaaS True-Cost Directory (Homepage)", "Compare 20+ B2B tools across CRM, Helpdesk AI, Payments & Compliance."),
        ("pricing/hubspot-true-cost-and-onboarding-fees/index.html", "HubSpot True Year-1 Cost & Onboarding Fees", "Model $1,500–$7,000 mandatory onboarding fees vs. Close CRM & Pipedrive."),
        ("compare/close-crm-vs-hubspot-sales-hub-5-to-20-reps/index.html", "Close CRM vs. HubSpot Sales Hub (5–20 Reps)", "Compare built-in VoIP calling & SMS against HubSpot seat + onboarding fees."),
        ("pricing/gong-io-platform-fee-and-seat-minimum-calculator/index.html", "Gong.io $5,000 Platform Fee & Seat Calculator", "Benchmark Gong's $5k base fee + $1,600/yr seats against Close CRM."),
        ("compare/monday-crm-vs-pipedrive-vs-hubspot-seat-minimums/index.html", "CRM Seat-Minimum & Bucket Calculator", "See where monday CRM's 3/5/10-seat buckets cost more than 1:1 CRMs."),
        ("intercom-fin-cost-calculator/index.html", "Intercom Fin Cost Calculator ($0.99/Resolution)", "Prefilled 10-agent, 1,500 AI/mo Year-1 calculator vs. Freshdesk & Zendesk."),
        ("intercom-vs-freshdesk-cost-comparison/index.html", "Intercom vs. Freshdesk Cost Comparison (2026)", "Compare Intercom Fin ($0.99/res) vs. Freshdesk Freddy AI ($49/100 sessions) Year-1 cost."),
        ("intercom-vs-zendesk-cost-comparison/index.html", "Intercom vs. Zendesk Cost Comparison (2026)", "Compare Intercom Fin ($0.99/res) vs. Zendesk AI ($1.50/res) Year-1 cost and overages."),
        ("pricing/intercom-fin-ai-resolution-cost-calculator/index.html", "Intercom Fin AI ($0.99/Resolution) True Cost", "Calculate monthly Fin AI resolution fees vs. Freshdesk session packs."),
        ("zendesk-ai-cost-calculator/index.html", "Zendesk AI Cost Calculator (2026)", "Prefilled 10-agent, 1,500 AI/mo Year-1 calculator vs. Freshdesk & Intercom."),
        ("zendesk-vs-freshdesk-cost-comparison/index.html", "Zendesk vs. Freshdesk Cost Comparison (2026)", "Compare Zendesk AI ($1.50/res) vs. Freshdesk Freddy AI ($49/100 sessions) Year-1 cost."),
        ("hubspot-onboarding-fee-calculator/index.html", "HubSpot Onboarding Fee & True Cost Calculator", "Model the $1,500–$7,000 onboarding fee, extra seats, and contact tiers vs. Close CRM & Pipedrive."),
        ("pricing/zendesk-ai-resolution-and-automated-outcome-cost/index.html", "Zendesk AI Automated Resolution Fee Calculator", "Model $1.50–$2.00 AI overage rates vs. Freshdesk & Help Scout."),
        ("pricing/stripe-billing-0-7-percent-recurring-tax-calculator/index.html", "Stripe Billing 0.7% Recurring Fee Calculator", "Compare Stripe 2.9% + 0.7% Billing + 0.5% Tax vs. Whop (2.7% + 30¢) & Paddle."),
        ("compare/gumroad-vs-whop-vs-lemon-squeezy-take-rate-calculator/index.html", "Gumroad vs. Whop vs. Lemon Squeezy Net Payouts", "Compare real creator & SaaS take rates after card processing and surcharges."),
        ("exit/stripe-shopify-paddle-frozen-funds-alternatives/index.html", "Stripe, Shopify & Paddle Reserve & Hold Simulator", "Model 25% rolling reserves and compare Merchant of Record token portability."),
        ("chargeback-fee-and-recovery-calculator/index.html", "Stripe & Shopify Chargeback Cost Calculator", "Dispute fees plus lost order value versus Chargeflow recovery and a 0.40% fee on all sales."),
        ("exit/paypal-180-day-permanent-limitation-fund-recovery/index.html", "PayPal 180-Day Hold & Working Capital Calculator", "Calculate frozen cashflow impact and multi-processor failover with Whop."),
        ("exit/zoominfo-60-day-auto-renewal-notice-and-cancellation/index.html", "ZoomInfo 60-Day Renewal Notice Calculator", "Deadline from your contract end date, and the March 2024 +10% extension versus a negotiated fee."),
        ("compare/typeform-vs-jotform-response-limit-and-hipaa-cost/index.html", "Typeform vs. Jotform Response Limit & HIPAA Cost", "Compare Typeform response tiers & Enterprise BAA vs. Jotform Gold ($99/mo)."),
        ("guides/jotform-wix-app-setup-and-pricing-guide/index.html", "Jotform Wix App Setup & B2B Quote Form Guide (2026)", "5-step visual & video walkthrough for embedding Jotform on Wix plus tier pricing."),
        ("pricing/jotform-pricing-tier-calculator/index.html", "Jotform Pricing Tier Calculator (2026)", "Compare Starter (Free), Bronze ($34/mo), Silver ($39/mo) & Gold HIPAA ($99/mo)."),
        ("pricing/docusign-envelope-allowance-and-api-overage-calculator/index.html", "DocuSign 100-Envelope Cap & Overage Calculator", "Expose the 100 envelopes/user/yr cap vs. PandaDoc & Jotform Sign."),
        ("compliance/hipaa-baa-and-soc2-pricing-tiers/index.html", "HIPAA BAA & SOC 2 + CPA Auditor Cost Calculator", "Compare self-serve HIPAA BAA plans and negotiated Vanta/Drata + CPA costs."),
        ("compliance/google-workspace-vs-microsoft-365-hipaa-baa-tiers/index.html", "Google Workspace vs. Microsoft 365 HIPAA BAA Calculator", "Cheapest BAA-eligible edition per suite ($7 entry), Vault/archiving gaps and form intake costs."),
        ("faq/does-hubspot-charge-onboarding-fees-2026/index.html", "FAQ: Does HubSpot Charge Onboarding Fees in 2026?", "Direct answer on $1,500–$7,000 fees, partner waivers, and $0-onboarding alternatives."),
        ("faq/intercom-fin-ai-cost-calculator/index.html", "FAQ: How Much Does Intercom Fin AI Cost in 2026?", "Quick calculator for $0.99/resolution AI support bills vs. Freshdesk & Help Scout."),
        ("faq/stripe-vs-paddle-true-cost/index.html", "FAQ: Stripe vs. Paddle vs. Whop True Cost (2026)", "Side-by-side effective take rate calculator with Billing, Tax, and FX fees."),
    ]
    cards = []
    for target_rel, label, summary in all_links:
        if target_rel == rel_path:
            continue
        href = prefix + target_rel.replace("index.html", "")
        cards.append(f"""
        <div class="card" style="padding:14px 16px;">
          <h3 style="margin:0 0 6px; font-size:0.98rem;"><a href="{href}" data-track="internal-audit">{label} &rarr;</a></h3>
          <p style="margin:0; font-size:0.84rem; color:var(--muted);">{summary}</p>
        </div>""")
        if len(cards) >= 6:
            break
    # Always ensure the 3 FAQ guides and related category links are reachable
    extra_faq_links = []
    for target_rel, label, _ in all_links[1:]:
        if target_rel == rel_path:
            continue
        href = prefix + target_rel.replace("index.html", "")
        extra_faq_links.append(f'<a href="{href}" data-track="internal-audit" style="font-size:0.84rem; margin-right:14px; display:inline-block; margin-bottom:6px;">{label} &rarr;</a>')
    return f"""
    <section aria-labelledby="related-calculators-heading" style="margin-top:36px; padding-top:24px; border-top:1px solid var(--border);">
      <h2 id="related-calculators-heading" style="font-size:1.2rem; margin-top:0;">Related Year-1 True-Cost Calculators &amp; Contract Audits</h2>
      <div class="card-grid" style="margin-bottom:16px;">
        {''.join(cards)}
      </div>
      <div style="padding:12px 14px; background:var(--surface-alt, #F2F4F0); border-radius:8px; line-height:1.7;">
        <strong style="font-size:0.84rem; display:block; margin-bottom:4px;">All Audited Calculators &amp; High-Intent Guides:</strong>
        {''.join(extra_faq_links)}
      </div>
    </section>
    """

def render_page(rel_path, title, description, canonical_path, body_html, faqs=None, extra_schema=None, published_date=None):
    iso_date, iso_datetime, human_date = get_freshness_timestamps()
    pub_date = published_date or iso_date
    full_title = title if ("saasbill" in title.lower()) else f"{title} – saasbill.io"

    faq_html = ""
    graph = [
        {
            "@type": "TechArticle",
            "@id": f"{SITE_ORIGIN}{canonical_path}#article",
            "headline": full_title,
            "description": description,
            "datePublished": pub_date,
            "dateModified": iso_datetime,
            "author": {
                "@type": "Organization",
                "name": "SaaSBill Editorial",
                "url": f"{SITE_ORIGIN}/"
            },
            "publisher": {
                "@type": "Organization",
                "name": "SaaSBill",
                "url": f"{SITE_ORIGIN}/"
            },
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": f"{SITE_ORIGIN}{canonical_path}"
            }
        },
        {
            "@type": "WebPage",
            "@id": f"{SITE_ORIGIN}{canonical_path}",
            "url": f"{SITE_ORIGIN}{canonical_path}",
            "name": full_title,
            "description": description,
            "inLanguage": "en-US",
            "datePublished": pub_date,
            "dateModified": iso_datetime,
            "lastReviewed": iso_date,
            "reviewedBy": {
                "@type": "Organization",
                "name": "SaaSBill Editorial"
            }
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "SaaSBill",
                    "item": f"{SITE_ORIGIN}/"
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": title,
                    "item": f"{SITE_ORIGIN}{canonical_path}"
                }
            ]
        }
    ]

    if extra_schema:
        extra_copy = dict(extra_schema)
        extra_copy["dateModified"] = iso_datetime
        extra_copy.setdefault("datePublished", pub_date)
        extra_copy.setdefault("temporalCoverage", "2026")
        graph.append(extra_copy)

    if faqs:
        faq_entities = []
        faq_items_html = []
        for q, a in faqs:
            faq_entities.append({
                "@type": "Question",
                "name": q,
                "dateCreated": pub_date,
                "dateModified": iso_datetime,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": a,
                    "dateCreated": pub_date,
                    "dateModified": iso_datetime
                }
            })
            faq_items_html.append(f"""
            <div class="faq-item" itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">
              <h3 itemprop="name">{q}</h3>
              <div itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">
                <p itemprop="text">{a}</p>
              </div>
            </div>
            """)
        graph.append({
            "@type": "FAQPage",
            "@id": f"{SITE_ORIGIN}{canonical_path}#faq",
            "datePublished": pub_date,
            "dateModified": iso_datetime,
            "mainEntity": faq_entities
        })
        faq_html = f"""
        <section aria-labelledby="faq-heading">
          <h2 id="faq-heading">Common questions</h2>
          <div class="faq-list">
            {''.join(faq_items_html)}
          </div>
        </section>
        """

    schema_obj = {
        "@context": "https://schema.org",
        "@graph": graph
    }
    schema_block = f'<script type="application/ld+json">{json.dumps(schema_obj)}</script>'

    depth = len([p for p in rel_path.split("/") if p]) - 1
    prefix = "../" * depth if depth > 0 else "./"
    related_html = render_related_links(rel_path, prefix)

    byline_bar = f'<span class="byline-bar">Updated <time datetime="{iso_date}" itemprop="dateModified">{human_date}</time></span>'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="google-site-verification" content="W7-m7km1_5pZZUG38dpallcgdGss6_Vl2qo5pjVoMdA" />
  <!-- Bing Webmaster Tools verification: paste <meta name="msvalidate.01" content="YOUR_BING_CODE" /> here or use 1-click Google Search Console import (see BING_WEBMASTER_VERIFICATION.md) -->
  <title>{full_title}</title>
  <meta name="description" content="{description}" />
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large" />
  <meta property="og:site_name" content="SaaSBill" />
  <meta property="og:type" content="article" />
  <meta property="og:title" content="{full_title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:url" content="{SITE_ORIGIN}{canonical_path}" />
  <meta property="og:updated_time" content="{iso_datetime}" />
  <meta property="article:published_time" content="{pub_date}T00:00:00+01:00" />
  <meta property="article:modified_time" content="{iso_datetime}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{full_title}" />
  <meta name="twitter:description" content="{description}" />
  <meta name="last-modified" content="{iso_datetime}" />
  <meta name="dcterms.modified" content="{iso_datetime}" />
  <meta name="dcterms.issued" content="{pub_date}" />
  <link rel="canonical" href="{SITE_ORIGIN}{canonical_path}" />
  <link rel="stylesheet" href="{prefix}assets/styles.css?v=20261028b" />
  <link rel="alternate" type="text/plain" href="{SITE_ORIGIN}/llms.txt" title="SaaSBill LLMs.txt Summary" />
  <!-- Privacy-friendly analytics by Plausible -->
  <script defer data-domain="saasbill.io" src="https://plausible.io/js/pa-VAaSVNs5XOobt9cv2UtKo.js"></script>
  <script>
    window.plausible=window.plausible||function(){{(plausible.q=plausible.q||[]).push(arguments)}},plausible.init=plausible.init||function(i){{plausible.o=i||{{}}}};
    plausible.init();
    window.__saasbillEvents = window.__saasbillEvents || [];
    window.trackSaaSBillEvent = function(eventName, props) {{
      var p = props || {{}};
      var entry = {{ event: eventName, ts: Date.now() }};
      for (var k in p) {{
        if (Object.prototype.hasOwnProperty.call(p, k)) entry[k] = p[k];
      }}
      window.__saasbillEvents.push(entry);
      if (typeof window.plausible === 'function') {{
        window.plausible(eventName, {{ props: p }});
      }}
    }};
  </script>
  {schema_block}
</head>
<body>
  <header class="site-header">
    <div class="container nav-inner">
      <div class="brand-wrap">
        <a href="{prefix}index.html" class="brand">SaaSBill<span>.io</span></a>
        <span class="brand-tagline">Year-1 software cost &amp; contract calculators</span>
      </div>
      <nav class="nav-links" aria-label="Primary Navigation">
        <a href="{prefix}index.html#all-calculators">Audits &amp; Guides</a>
        <a href="{prefix}index.html#methodology">Methodology</a>
        {byline_bar}
      </nav>
    </div>
  </header>
  <main class="container">
    <article itemscope itemtype="https://schema.org/TechArticle">
      <meta itemprop="datePublished" content="{pub_date}" />
      <meta itemprop="dateModified" content="{iso_datetime}" />
      {body_html}
      {faq_html}
      {related_html}
    </article>
  </main>
  <footer class="site-footer">
    <div class="container">
      <p><strong>SaaSBill</strong> &middot; Year-1 cost &amp; contract calculators for B2B software.</p>
      <p class="footer-note">Independent calculations. Some vendor links are affiliate links. This never changes our rankings or calculations. &middot; Updated <time datetime="{iso_date}">{human_date}</time> &middot; Inquiries: <a href="mailto:info@saasbill.io">info@saasbill.io</a></p>
    </div>
  </footer>
  <script>
  /* Plausible + local event dispatcher for: calculator_interaction, category_select, result_rendered, vendor_cta_click */
  window.__saasbillEvents = window.__saasbillEvents || [];
  try {{
    var p = (window.location && window.location.pathname ? window.location.pathname : '').toLowerCase();
    if (p && p !== '/' && p !== '/index.html') {{
      var ctxCat = '';
      var ctxTool = '';
      if (p.indexOf('zoominfo') !== -1) {{
        ctxCat = 'CRM & Sales';
        ctxTool = 'close-crm';
      }} else if (p.indexOf('stripe') !== -1 || p.indexOf('paddle') !== -1 || p.indexOf('whop') !== -1 || p.indexOf('gumroad') !== -1 || p.indexOf('paypal') !== -1) {{
        ctxCat = 'Payment Processors & MoR';
        ctxTool = p.indexOf('paddle') !== -1 ? 'paddle-mor' : (p.indexOf('whop') !== -1 ? 'whop-payments' : 'stripe-payments');
      }} else if (p.indexOf('hubspot') !== -1 || p.indexOf('close-crm') !== -1 || p.indexOf('pipedrive') !== -1 || p.indexOf('monday-crm') !== -1 || p.indexOf('gong') !== -1) {{
        ctxCat = 'CRM & Sales';
        ctxTool = p.indexOf('monday') !== -1 ? 'monday-crm' : (p.indexOf('close') !== -1 ? 'close-crm' : (p.indexOf('pipedrive') !== -1 ? 'pipedrive-crm' : 'hubspot-sales-pro'));
      }} else if (p.indexOf('hipaa') !== -1 || p.indexOf('soc2') !== -1 || p.indexOf('docusign') !== -1 || p.indexOf('typeform') !== -1 || p.indexOf('jotform') !== -1) {{
        ctxCat = 'Compliance, HIPAA & SOC 2';
        ctxTool = (p.indexOf('typeform') !== -1 || p.indexOf('jotform') !== -1) ? 'jotform-hipaa' : 'vanta-soc2';
      }} else if (p.indexOf('intercom') !== -1 || p.indexOf('zendesk') !== -1 || p.indexOf('freshdesk') !== -1) {{
        ctxCat = 'Helpdesk & AI Support';
        ctxTool = p.indexOf('intercom') !== -1 ? 'intercom-fin-ai' : (p.indexOf('freshdesk') !== -1 ? 'freshdesk-support' : 'zendesk-suite-team');
      }}
      if (ctxCat && window.sessionStorage) {{
        sessionStorage.setItem('saasbill_last_cat', ctxCat);
        if (ctxTool) sessionStorage.setItem('saasbill_last_tool', ctxTool);
      }}
    }}
  }} catch (err) {{}}
  document.addEventListener('click', function(e) {{
    var cta = e.target.closest('[data-track="vendor-cta"], [data-track="vendor_cta_click"]');
    if (cta) {{
      var vendor = cta.getAttribute('data-vendor') || '';
      var location = cta.getAttribute('data-cta-location') || 'subpage-result';
      var href = cta.getAttribute('href') || '';
      if (typeof window.trackSaaSBillEvent === 'function') {{
        window.trackSaaSBillEvent('vendor_cta_click', {{ vendor: vendor, location: location, href: href }});
      }}
      return;
    }}
    var catBtn = e.target.closest('[data-track="category-select"], [data-track="category_select"]');
    if (catBtn) {{
      var cat = catBtn.getAttribute('data-cat') || '';
      if (typeof window.trackSaaSBillEvent === 'function') {{
        window.trackSaaSBillEvent('category_select', {{ category: cat }});
      }}
    }}
  }});
  var _lastCalcTrackKey = '';
  var _lastCalcTrackTs = 0;
  function handleCalcControlEvent(e) {{
    var ctrl = e.target.closest('[data-track="calculator-control"], [data-track="calculator_interaction"], input[type="range"], select');
    if (ctrl) {{
      var control = ctrl.getAttribute('data-control') || ctrl.id || '';
      var val = String(ctrl.value);
      var now = Date.now();
      var key = control + ':' + val;
      if (key === _lastCalcTrackKey && (now - _lastCalcTrackTs) < 150) return;
      _lastCalcTrackKey = key;
      _lastCalcTrackTs = now;
      if (typeof window.trackSaaSBillEvent === 'function') {{
        window.trackSaaSBillEvent('calculator_interaction', {{ control: control, value: val }});
        if (ctrl.id === 'cat-filter') {{
          window.trackSaaSBillEvent('category_select', {{ category: val }});
        }}
      }}
    }}
  }}
  document.addEventListener('input', handleCalcControlEvent);
  document.addEventListener('change', handleCalcControlEvent);
  </script>
</body>
</html>"""
    full_path = os.path.join(PUBLIC_DIR, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(html)
    print(f"Wrote {full_path} [dateModified={iso_datetime}]")
