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
        ("index.html", "Year-1 SaaS True-Cost Directory", "Compare 20+ B2B tools across CRM, Helpdesk AI, Payments, and Compliance."),
        ("pricing/hubspot-true-cost-and-onboarding-fees/index.html", "HubSpot True Cost &amp; Onboarding", "What HubSpot costs in Year 1 once mandatory onboarding is included."),
        ("compare/close-crm-vs-hubspot-sales-hub-5-to-20-reps/index.html", "Close CRM vs. HubSpot Sales Hub", "True Year-1 cost for 5 to 20 reps, including HubSpot onboarding."),
        ("pricing/gong-io-platform-fee-and-seat-minimum-calculator/index.html", "Gong.io $5,000 Platform Fee &amp; Seat Calculator", "Platform fee plus per-seat licenses versus Close CRM."),
        ("compare/monday-crm-vs-pipedrive-vs-hubspot-seat-minimums/index.html", "monday CRM 3/5/10-Seat Bucket Calculator", "Where fixed seat buckets cost more than one seat at a time."),
        ("intercom-fin-cost-calculator/index.html", "Intercom Fin AI Cost Calculator", "Year-1 price at $0.99 per resolution versus Freshdesk and Zendesk."),
        ("intercom-vs-freshdesk-cost-comparison/index.html", "Intercom vs. Freshdesk Cost Comparison", "Real Year-1 price and AI fees for the same team."),
        ("intercom-vs-zendesk-cost-comparison/index.html", "Intercom vs. Zendesk Cost Comparison", "Real Year-1 price and per-resolution overage."),
        ("pricing/intercom-fin-ai-resolution-cost-calculator/index.html", "Intercom Fin AI Cost Calculator", "The pricing-page copy of the $0.99 per resolution Year-1 calculator."),
        ("zendesk-ai-cost-calculator/index.html", "Zendesk AI Cost Calculator", "Suite seats plus the per-resolution add-on versus Freshdesk and Intercom."),
        ("zendesk-vs-freshdesk-cost-comparison/index.html", "Zendesk vs. Freshdesk Cost Comparison", "Year-1 pricing with AI resolutions side by side."),
        ("hubspot-onboarding-fee-calculator/index.html", "HubSpot Onboarding Fee Calculator", "Mandatory setup from $1,500 to $7,000 plus the Year-1 license."),
        ("pricing/zendesk-ai-resolution-and-automated-outcome-cost/index.html", "Zendesk AI Cost Calculator", "The pricing-page copy of the Zendesk AI Year-1 calculator."),
        ("pricing/stripe-billing-0-7-percent-recurring-tax-calculator/index.html", "Stripe Billing 0.7% Fee, Tax &amp; Chargeback Calculator", "Recurring revenue tax, Stripe Tax, and subscription chargebacks versus Whop and Paddle."),
        ("compare/gumroad-vs-whop-vs-lemon-squeezy-take-rate-calculator/index.html", "Gumroad vs. Whop vs. Lemon Squeezy Take-Rate &amp; Chargeback Calculator", "10%, 2.7%, and 5% take rates plus dispute fees."),
        ("exit/stripe-shopify-paddle-frozen-funds-alternatives/index.html", "Stripe, Shopify &amp; Paddle Frozen Funds &amp; Reserve Calculator", "25% rolling reserves, payout holds, and the chargeback rate that triggers a freeze."),
        ("chargeback-fee-and-recovery-calculator/index.html", "Stripe, Shopify &amp; Paddle Chargeback Cost Calculator", "Dispute fees, manual prep, and automated recovery."),
        ("exit/paypal-180-day-permanent-limitation-fund-recovery/index.html", "PayPal 180-Day Hold &amp; Reserve Cost Calculator", "Held cashflow, dispute fees, and a failover rail."),
        ("exit/zoominfo-60-day-auto-renewal-notice-and-cancellation/index.html", "ZoomInfo 60-Day Auto-Renewal Notice", "The 60-day window and what the extension costs."),
        ("compare/typeform-vs-jotform-response-limit-and-hipaa-cost/index.html", "Typeform vs. Jotform Response &amp; HIPAA Calculator", "Response caps and which plan signs a HIPAA BAA."),
        ("guides/jotform-wix-app-setup-and-pricing-guide/index.html", "Jotform Wix App Setup &amp; Pricing Guide", "How to embed a B2B quote form on Wix, plus tier pricing."),
        ("pricing/jotform-pricing-tier-calculator/index.html", "Jotform 2026 Pricing Tier Calculator", "Starter, Bronze, Silver, and Gold Year-1 cost."),
        ("pricing/docusign-envelope-allowance-and-api-overage-calculator/index.html", "DocuSign 100-Envelope Cap &amp; Overage Calculator", "The 100-envelope allowance versus Jotform Sign and PandaDoc."),
        ("compliance/hipaa-baa-and-soc2-pricing-tiers/index.html", "HIPAA BAA &amp; SOC 2 Pricing Tiers", "Which plan signs a BAA, and what the CPA audit adds."),
        ("compliance/google-workspace-vs-microsoft-365-hipaa-baa-tiers/index.html", "Google Workspace vs. Microsoft 365 HIPAA BAA", "Minimum editions that sign a BAA, plus form intake rules."),
        ("faq/does-hubspot-charge-onboarding-fees-2026/index.html", "Does HubSpot Charge Onboarding Fees in 2026?", "The fee schedule, waivers, and $0-onboarding alternatives."),
        ("faq/intercom-fin-ai-cost-calculator/index.html", "Intercom Fin AI Cost Calculator", "The FAQ copy of the $0.99 per resolution Year-1 price."),
        ("faq/stripe-vs-paddle-true-cost/index.html", "Stripe vs. Paddle vs. Whop True Cost &amp; Chargeback Calculator", "Processing, billing, tax, and dispute cost side by side."),
        ("pricing/stripe-shopify-chargeback-fee-and-chargeflow-roi-calculator/index.html", "Stripe, Shopify &amp; Paddle Chargeback Cost Calculator", "The pricing-page copy of the dispute fee and recovery calculator."),
    ]
    by_rel = {rel: (label, summary) for rel, label, summary in all_links}
    chargeback_rel = "chargeback-fee-and-recovery-calculator/index.html"
    chargeback_mirror = "pricing/stripe-shopify-chargeback-fee-and-chargeflow-roi-calculator/index.html"
    payment_rels = {
        chargeback_rel,
        "exit/stripe-shopify-paddle-frozen-funds-alternatives/index.html",
        "pricing/stripe-billing-0-7-percent-recurring-tax-calculator/index.html",
        "faq/stripe-vs-paddle-true-cost/index.html",
        "compare/gumroad-vs-whop-vs-lemon-squeezy-take-rate-calculator/index.html",
        "exit/paypal-180-day-permanent-limitation-fund-recovery/index.html",
    }
    if rel_path in (chargeback_rel, chargeback_mirror):
        preferred = [
            "exit/stripe-shopify-paddle-frozen-funds-alternatives/index.html",
            "pricing/stripe-billing-0-7-percent-recurring-tax-calculator/index.html",
            "faq/stripe-vs-paddle-true-cost/index.html",
        ]
    elif rel_path in payment_rels:
        preferred = [chargeback_rel] + [rel for rel, _, _ in all_links if rel in payment_rels and rel != chargeback_rel]
    elif rel_path in {
        "intercom-fin-cost-calculator/index.html",
        "pricing/intercom-fin-ai-resolution-cost-calculator/index.html",
        "faq/intercom-fin-ai-cost-calculator/index.html",
        "intercom-vs-freshdesk-cost-comparison/index.html",
        "intercom-vs-zendesk-cost-comparison/index.html",
        "zendesk-ai-cost-calculator/index.html",
        "pricing/zendesk-ai-resolution-and-automated-outcome-cost/index.html",
        "zendesk-vs-freshdesk-cost-comparison/index.html",
    }:
        helpdesk_order = [
            "intercom-fin-cost-calculator/index.html",
            "zendesk-ai-cost-calculator/index.html",
            "intercom-vs-freshdesk-cost-comparison/index.html",
            "intercom-vs-zendesk-cost-comparison/index.html",
            "zendesk-vs-freshdesk-cost-comparison/index.html",
        ]
        helpdesk_same = {
            "intercom-fin-cost-calculator/index.html": {
                "intercom-fin-cost-calculator/index.html",
                "pricing/intercom-fin-ai-resolution-cost-calculator/index.html",
                "faq/intercom-fin-ai-cost-calculator/index.html",
            },
            "zendesk-ai-cost-calculator/index.html": {
                "zendesk-ai-cost-calculator/index.html",
                "pricing/zendesk-ai-resolution-and-automated-outcome-cost/index.html",
            },
        }
        skip = {rel_path}
        for group in helpdesk_same.values():
            if rel_path in group:
                skip = set(group)
        preferred = [rel for rel in helpdesk_order if rel not in skip]
    else:
        preferred = [rel for rel, _, _ in all_links]
    cards = []
    for target_rel in preferred:
        if target_rel == rel_path or target_rel == chargeback_mirror or target_rel not in by_rel:
            continue
        label, summary = by_rel[target_rel]
        href = prefix + target_rel.replace("index.html", "")
        cards.append(f"""
        <div class="card" style="padding:14px 16px;">
          <h3 style="margin:0 0 6px; font-size:0.98rem;"><a href="{href}" data-track="internal-audit">{label} &rarr;</a></h3>
          <p style="margin:0; font-size:0.84rem; color:var(--muted);">{summary}</p>
        </div>""")
        if len(cards) >= 3:
            break
    directory_links = []
    for target_rel, label, _ in all_links:
        href = prefix + target_rel.replace("index.html", "")
        directory_links.append(f'<a href="{href}" data-track="internal-audit">{label} &rarr;</a>')
    return f"""
    <section aria-labelledby="related-calculators-heading" style="margin-top:36px; padding-top:24px; border-top:1px solid var(--border);">
      <h2 id="related-calculators-heading" style="font-size:1.2rem; margin-top:0;">Related Year-1 True-Cost Calculators &amp; Contract Audits</h2>
      <div class="related-calc-grid">
        {''.join(cards)}
      </div>
      <details class="footer-directory-details">
        <summary>Browse all {len(all_links)} audited calculators &amp; guides</summary>
        <div class="footer-directory-links">
          {''.join(directory_links)}
        </div>
      </details>
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
  <link rel="stylesheet" href="{prefix}assets/styles.css?v=20261028c" />
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
    window.trackEvent = window.trackSaaSBillEvent;
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
  <script src="{prefix}assets/app.js?v=20261028c"></script>
</body>
</html>"""
    full_path = os.path.join(PUBLIC_DIR, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(html)
    print(f"Wrote {full_path} [dateModified={iso_datetime}]")
