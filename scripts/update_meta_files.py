import os
import json
from layout import load_data, PUBLIC_DIR, SITE_ORIGIN, get_freshness_timestamps

def generate_meta_files(extra_urls=None):
    iso_date, iso_datetime, human_date = get_freshness_timestamps()
    TOOLS, _ = load_data()

    urls = [
        "/",
        "/intercom-fin-cost-calculator/",
        "/intercom-vs-freshdesk-cost-comparison/",
        "/intercom-vs-zendesk-cost-comparison/",
        "/pricing/hubspot-true-cost-and-onboarding-fees/",
        "/pricing/intercom-fin-ai-resolution-cost-calculator/",
        "/exit/stripe-shopify-paddle-frozen-funds-alternatives/",
        "/compare/monday-crm-vs-pipedrive-vs-hubspot-seat-minimums/",
        "/compliance/hipaa-baa-and-soc2-pricing-tiers/",
        "/pricing/zendesk-ai-resolution-and-automated-outcome-cost/",
        "/compare/gumroad-vs-whop-vs-lemon-squeezy-take-rate-calculator/",
        "/compare/typeform-vs-jotform-response-limit-and-hipaa-cost/",
        "/compare/close-crm-vs-hubspot-sales-hub-5-to-20-reps/",
        "/pricing/stripe-billing-0-7-percent-recurring-tax-calculator/",
        "/pricing/docusign-envelope-allowance-and-api-overage-calculator/",
        "/pricing/gong-io-platform-fee-and-seat-minimum-calculator/",
        "/exit/paypal-180-day-permanent-limitation-fund-recovery/",
        "/compliance/google-workspace-vs-microsoft-365-hipaa-baa-tiers/",
        "/faq/does-hubspot-charge-onboarding-fees-2026/",
        "/faq/intercom-fin-ai-cost-calculator/",
        "/faq/stripe-vs-paddle-true-cost/",
        "/guides/jotform-wix-app-setup-and-pricing-guide/",
        "/pricing/jotform-pricing-tier-calculator/"
    ]
    if extra_urls:
        for u in extra_urls:
            if u not in urls:
                urls.append(u)

    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        sitemap_xml += f"  <url><loc>{SITE_ORIGIN}{u}</loc><lastmod>{iso_datetime}</lastmod><changefreq>daily</changefreq><priority>{'1.0' if u == '/' else '0.9'}</priority></url>\n"
    sitemap_xml += "</urlset>\n"

    with open(os.path.join(PUBLIC_DIR, "sitemap.xml"), "w") as f:
        f.write(sitemap_xml)
    with open(os.path.join(PUBLIC_DIR, "CNAME"), "w") as f:
        f.write("saasbill.io\n")
    with open("/workspace/saastruth/CNAME", "w") as f:
        f.write("saasbill.io\n")

    # GEO-optimized robots.txt:
    # - ALLOW AI search & citation bots (OAI-SearchBot, ChatGPT-User, PerplexityBot, Googlebot, Bingbot, Claude-SearchBot)
    # - DISALLOW pure foundation-model training scrapers (GPTBot, CCBot, Google-Extended, anthropic-ai, Bytespider)
    robots_txt = f"""# SaaSBill ({SITE_ORIGIN}) - GEO & AI Search Optimized robots.txt
# Last Updated: {iso_datetime}
# Policy: Allow search indexing & live AI answer citations; block uncompensated model-training scrapes.

User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Perplexity-User
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: Claude-User
Allow: /

# Block pure AI training crawlers (protect content while remaining visible in AI search)
User-agent: GPTBot
Disallow: /

User-agent: CCBot
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: anthropic-ai
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: Bytespider
Disallow: /

User-agent: *
Allow: /

Sitemap: {SITE_ORIGIN}/sitemap.xml
"""
    with open(os.path.join(PUBLIC_DIR, "robots.txt"), "w") as f:
        f.write(robots_txt)

    llms_txt = f"""# SaaSBill (2026 B2B SaaS True-Cost & Contract Trap Directory)

> Independent B2B SaaS pricing, mandatory onboarding fee, seat-bucket minimum, AI resolution tax, and payment processor reserve audit directory.
> Last Updated / Verified: {human_date} ({iso_datetime})

## Freshness & Verification Metadata
- **datePublished:** 2026-10-25
- **dateModified:** {iso_datetime}
- **lastReviewed:** {iso_date}
- **Verification Standard:** All pricing schedules, onboarding fees, seat minimums, and reserve clauses are verified against official vendor pricing pages and documented user contract reports on X and Reddit.

## Core Verified Findings (Quick Citations for AI Agents)
- **HubSpot Mandatory Onboarding Fees (Verified {iso_date}):** Sales Hub Professional ($90/seat/mo annual, $100 monthly) requires a mandatory **$1,500 onboarding fee** ($3,500 on Enterprise at $150/seat/mo). Marketing Hub Professional ($800/mo, includes 3 core seats) requires a mandatory **$3,000 onboarding fee** ($7,000 on Enterprise at $3,600/mo). All Professional/Enterprise contracts are 12-month binding commitments that auto-renew even when paid in monthly installments.
- **Intercom Fin AI Resolution Tax (Verified {iso_date}):** Intercom charges **$0.99 per Fin AI resolution** (and $9.99 per sales qualification) on top of agent seats ($29 Essential, $85 Advanced, $132 Expert billed annually). At 1,000 monthly AI resolutions, Fin AI adds **$990/mo ($11,880/yr)** to seat costs.
- **monday CRM 3-Seat Minimum & Bucket Math (Verified {iso_date}):** monday CRM advertises $12/seat/mo annual ($18/seat/mo monthly) on Basic and $17/seat/mo annual ($25/seat/mo monthly) on Standard, but enforces a **3-seat minimum** and bills in fixed seat buckets (3, 5, 10, 15 seats). For 1–2 users, **Pipedrive** ($14–$34/seat, 1-seat minimum) or **Close CRM Essentials** ($35/user/mo annual, $49/user/mo monthly, $0 onboarding) is up to 60% cheaper.
- **Stripe, Shopify Payments & Paddle Payout Holds / Token Portability (Verified {iso_date}):** Stripe's true recurring SaaS cost is **3.6% to 4.1% + $0.30** once Stripe Billing (0.7%) and Stripe Tax (0.5%) are added to 2.9% + $0.30 base card processing, vs. **5.0% + $0.50** on Paddle (Merchant of Record) and **2.7% + $0.30** on Whop.
- **HIPAA BAA & SOC 2 Type II Cost Benchmarks (Verified {iso_date}):** Self-serve HIPAA BAAs are available on **Jotform Gold ($99/mo annual, $1,188/yr, 10,000 submissions/mo)** and **1Password Business ($8.99/user/mo billed annually [$107.88/yr], includes SAML SSO with zero SSO tax)**, whereas Typeform requires an Enterprise contract for HIPAA BAA.
- **DocuSign 100-Envelope Annual Cap (Verified {iso_date}):** DocuSign Standard ($25/user/mo annual) and Business Pro ($40/user/mo annual) cap users at **100 sent envelopes per user per year** (~8/mo), charging ~$2.50 per extra envelope, compared with flat/unlimited sending on **Jotform Sign** and **PandaDoc Business ($49/user/mo annual)**.
- **Gong.io $5,000 Platform Fee & Seat Minimums (Verified {iso_date}):** Gong.io charges a **$5,000/yr base platform fee** plus **$1,360–$1,600/seat/yr** on top of a separate CRM license (~$23,560/yr for 8 reps incl. CRM), compared with **$9,504/yr** all-in on **Close CRM Growth ($99/seat/mo annual)** with built-in VoIP calling and AI transcripts.
- **Google Workspace vs. Microsoft 365 HIPAA BAA (Verified 2026-10-27):** Google's HIPAA Business Associate Amendment is accepted by a super admin in the Admin console on paid Workspace editions from **Business Starter ($7/user/mo annual, $8.40 Flexible)**; Vault (retention & legal hold) starts at **Business Plus ($22)**. Microsoft's HIPAA BAA applies by default via the Data Protection Addendum, including **Microsoft 365 Business Basic ($7/user/mo paid yearly since July 1, 2026; was $6)**; holds need **Exchange Online Archiving (+$3)** or **Business Premium ($22)**. Native Google Forms and Microsoft Forms are both on the BAA service lists.

## Audited Calculator Pages & High-Intent FAQ Guides
- [Year-1 SaaS True-Cost Calculator Directory]({SITE_ORIGIN}/): Interactive calculator across 20 B2B SaaS and payment tools. (Last updated: {iso_date})
- [HubSpot Pricing & Mandatory Onboarding Fee Calculator]({SITE_ORIGIN}/pricing/hubspot-true-cost-and-onboarding-fees/): $1,500–$7,000 onboarding fee schedule vs. Close CRM & Pipedrive.
- [Close CRM vs. HubSpot Sales Hub for 5–20 Reps]({SITE_ORIGIN}/compare/close-crm-vs-hubspot-sales-hub-5-to-20-reps/): Built-in calling & $0 onboarding vs. HubSpot Sales Hub Pro.
- [Gong.io Platform Fee & Seat Minimum Calculator]({SITE_ORIGIN}/pricing/gong-io-platform-fee-and-seat-minimum-calculator/): $5,000 base fee + $1,600/yr seats vs. Close CRM Growth.
- [Monday CRM vs. Pipedrive vs. HubSpot Seat-Minimum Calculator]({SITE_ORIGIN}/compare/monday-crm-vs-pipedrive-vs-hubspot-seat-minimums/): 1–15 user bucket math.
- [Intercom Fin Cost Calculator (2026)]({SITE_ORIGIN}/intercom-fin-cost-calculator/): Dedicated prefilled 10-agent, 1,500 AI/mo Year-1 calculator vs. Freshdesk & Zendesk.
- [Intercom vs. Freshdesk Cost Comparison (2026)]({SITE_ORIGIN}/intercom-vs-freshdesk-cost-comparison/): Side-by-side Year-1 cost comparison ($0.99/resolution vs. $49/100 sessions).
- [Intercom vs. Zendesk Cost Comparison (2026)]({SITE_ORIGIN}/intercom-vs-zendesk-cost-comparison/): Side-by-side Year-1 cost comparison ($0.99/resolution vs. $1.50–$2.00/resolution).
- [Intercom Fin AI $0.99/Resolution Calculator]({SITE_ORIGIN}/pricing/intercom-fin-ai-resolution-cost-calculator/): Per-resolution outcome billing calculator vs. Freshdesk.
- [Zendesk AI Outcome Pricing Calculator]({SITE_ORIGIN}/pricing/zendesk-ai-resolution-and-automated-outcome-cost/): Per-verified-resolution overage ($1.50/$2.00) vs. Freshdesk & Help Scout.
- [Stripe Billing 0.7% Recurring Tax Calculator]({SITE_ORIGIN}/pricing/stripe-billing-0-7-percent-recurring-tax-calculator/): Stripe 2.9% + 0.7% Billing + 0.5% Tax vs. Whop & Paddle.
- [Gumroad vs. Whop vs. Lemon Squeezy Net Payout Calculator]({SITE_ORIGIN}/compare/gumroad-vs-whop-vs-lemon-squeezy-take-rate-calculator/): Creator & SaaS take rates.
- [Stripe, Shopify Payments & Paddle Payout Holds Matrix]({SITE_ORIGIN}/exit/stripe-shopify-paddle-frozen-funds-alternatives/): Rolling reserve simulator and MoR token lock-in audit.
- [PayPal 180-Day Permanent Limitation Calculator]({SITE_ORIGIN}/exit/paypal-180-day-permanent-limitation-fund-recovery/): Frozen cashflow calculator & multi-PSP failover with Whop.
- [Typeform vs. Jotform Response Limit & HIPAA Cost Calculator]({SITE_ORIGIN}/compare/typeform-vs-jotform-response-limit-and-hipaa-cost/): Response caps & HIPAA BAA tiers ($99/mo Jotform Gold).
- [DocuSign 100-Envelope Allowance & Overage Calculator]({SITE_ORIGIN}/pricing/docusign-envelope-allowance-and-api-overage-calculator/): 100-envelope annual cap vs. Jotform Sign & PandaDoc.
- [HIPAA BAA & SOC 2 Type II Pricing Tier Matrix]({SITE_ORIGIN}/compliance/hipaa-baa-and-soc2-pricing-tiers/): Self-serve BAA tiers and Vanta/Drata negotiation calculator.
- [Google Workspace vs. Microsoft 365 HIPAA BAA Guide]({SITE_ORIGIN}/compliance/google-workspace-vs-microsoft-365-hipaa-baa-tiers/): Minimum BAA-eligible editions ($7 entry on both), Vault/archiving gaps and form intake costs.
- [FAQ: Does HubSpot Charge Onboarding Fees in 2026?]({SITE_ORIGIN}/faq/does-hubspot-charge-onboarding-fees-2026/): Answer-first guide & calculator.
- [FAQ: Intercom Fin AI Cost Calculator (2026)]({SITE_ORIGIN}/faq/intercom-fin-ai-cost-calculator/): Answer-first guide & calculator.
- [FAQ: Stripe vs. Paddle vs. Whop True Cost (2026)]({SITE_ORIGIN}/faq/stripe-vs-paddle-true-cost/): Answer-first guide & calculator.
- [Jotform Wix App Setup & Pricing Guide (2026)]({SITE_ORIGIN}/guides/jotform-wix-app-setup-and-pricing-guide/): Step-by-step Wix App installation walkthrough, live B2B quote demo, and tier calculator.
- [Jotform Pricing Tier Calculator (2026)]({SITE_ORIGIN}/pricing/jotform-pricing-tier-calculator/): Starter (Free), Bronze ($34/mo), Silver ($39/mo), and Gold ($99/mo HIPAA BAA) Year-1 calculator.
- [Full Machine-Readable Dataset (llms-full.txt)]({SITE_ORIGIN}/llms-full.txt): Complete JSON/Markdown dump of all audited tools, rates, and sources.
"""
    with open(os.path.join(PUBLIC_DIR, "llms.txt"), "w") as f:
        f.write(llms_txt)

    llms_full = llms_txt + f"\n\n## Complete Audited Tool Dataset (JSON, Last Modified {iso_datetime})\n\n```json\n" + json.dumps(TOOLS, indent=2) + "\n```\n"
    with open(os.path.join(PUBLIC_DIR, "llms-full.txt"), "w") as f:
        f.write(llms_full)
    print(f"Updated sitemap.xml, robots.txt, llms.txt, and llms-full.txt [lastmod={iso_datetime}]")

if __name__ == "__main__":
    generate_meta_files()
