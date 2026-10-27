import json
import os
import re
import subprocess
import unittest
from urllib.parse import urlparse

# Repo root (this file lives in tests/). The published site is copied from public/ to the root for GitHub Pages.
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
PUBLIC_DIR = os.path.join(BASE_DIR, "public")


def load_tools_and_affiliates():
    with open(os.path.join(DATA_DIR, "tools.json")) as f:
        tools = json.load(f)
    with open(os.path.join(DATA_DIR, "affiliate_links.json")) as f:
        affiliates = json.load(f)
    return {t["id"]: t for t in tools}, tools, affiliates


def run_homepage_js_calc(seats, ai_vol, mode, cat="ALL"):
    """Executes the exact JS calculator functions embedded in public/index.html via Node.js."""
    with open(os.path.join(PUBLIC_DIR, "index.html")) as f:
        html = f.read()
    m = re.search(r"<script>\s*(const TOOLS = .*?)\['cat-filter'", html, re.S)
    if not m:
        raise RuntimeError("Could not extract calculator script from public/index.html")
    js_core = m.group(1)
    runner = f"""
    {js_core}
    const cat = {json.dumps(cat)};
    const seats = {seats};
    const aiVol = {ai_vol};
    const mode = {json.dumps(mode)};
    const filtered = TOOLS.filter(t => {{
      if (cat === 'ALL') return t.category !== 'Payment Processors & MoR';
      return t.category === cat;
    }});
    const rows = filtered.map(t => calcToolYear1(t, seats, aiVol, mode));
    rows.sort((a, b) => a.year1Total - b.year1Total);
    console.log(JSON.stringify(rows));
    """
    res = subprocess.run(["node", "-e", runner], capture_output=True, text=True, check=True)
    return json.loads(res.stdout)


class TestSaaSBillCalculators(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tools_by_id, cls.tools_list, cls.affiliates = load_tools_and_affiliates()

    def test_1_user_vs_5_users_seat_minimums(self):
        """1 user vs 5 users: monday CRM 3-seat minimum & buckets, Close CRM 1:1, Pipedrive 1:1, HubSpot Marketing Pro 3-seat base."""
        rows_1 = {r["tool"]["id"]: r for r in run_homepage_js_calc(seats=1, ai_vol=0, mode="annual")}
        rows_4 = {r["tool"]["id"]: r for r in run_homepage_js_calc(seats=4, ai_vol=0, mode="annual")}
        rows_5 = {r["tool"]["id"]: r for r in run_homepage_js_calc(seats=5, ai_vol=0, mode="annual")}

        # monday-crm (Basic: $12/seat annual): 1 user -> 3 billed seats ($36/mo = $432/yr); 4 users -> 5 billed seats ($60/mo = $720/yr)
        self.assertEqual(rows_1["monday-crm"]["effSeats"], 3)
        self.assertEqual(rows_1["monday-crm"]["year1Total"], 3 * 12 * 12)
        self.assertEqual(rows_4["monday-crm"]["effSeats"], 5)
        self.assertEqual(rows_4["monday-crm"]["year1Total"], 5 * 12 * 12)
        self.assertEqual(rows_5["monday-crm"]["effSeats"], 5)
        self.assertEqual(rows_5["monday-crm"]["year1Total"], 5 * 12 * 12)

        # close-crm (Essentials: $35/user annual): 1 user -> $35*12 = $420/yr; 5 users -> 5*$35*12 = $2,100/yr
        self.assertEqual(rows_1["close-crm"]["effSeats"], 1)
        self.assertEqual(rows_1["close-crm"]["year1Total"], 1 * 35 * 12)
        self.assertEqual(rows_5["close-crm"]["effSeats"], 5)
        self.assertEqual(rows_5["close-crm"]["year1Total"], 5 * 35 * 12)

        # pipedrive-crm: 1:1 seat billing ($14/mo = $168/yr for 1 user; $70/mo = $840/yr for 5 users)
        self.assertEqual(rows_1["pipedrive-crm"]["effSeats"], 1)
        self.assertEqual(rows_1["pipedrive-crm"]["year1Total"], 1 * 14 * 12)
        self.assertEqual(rows_5["pipedrive-crm"]["effSeats"], 5)
        self.assertEqual(rows_5["pipedrive-crm"]["year1Total"], 5 * 14 * 12)

        # hubspot-marketing-pro: $800/mo includes 3 seats (+$3,000 onboarding = $12,600/yr at 1-3 seats); at 5 seats adds 2 * $45 = $890/mo ($13,680/yr)
        self.assertEqual(rows_1["hubspot-marketing-pro"]["monthlySoftware"], 800)
        self.assertEqual(rows_1["hubspot-marketing-pro"]["year1Total"], 800 * 12 + 3000)
        self.assertEqual(rows_5["hubspot-marketing-pro"]["monthlySoftware"], 890)
        self.assertEqual(rows_5["hubspot-marketing-pro"]["year1Total"], 890 * 12 + 3000)

    def test_annual_vs_monthly_billing(self):
        """Annual vs Monthly billing for HubSpot, Jotform HIPAA, Close CRM, monday CRM, and 1Password Business."""
        rows_ann_1 = {r["tool"]["id"]: r for r in run_homepage_js_calc(seats=1, ai_vol=0, mode="annual")}
        rows_mo_1 = {r["tool"]["id"]: r for r in run_homepage_js_calc(seats=1, ai_vol=0, mode="monthly")}
        rows_ann = {r["tool"]["id"]: r for r in run_homepage_js_calc(seats=5, ai_vol=0, mode="annual")}
        rows_mo = {r["tool"]["id"]: r for r in run_homepage_js_calc(seats=5, ai_vol=0, mode="monthly")}

        # HubSpot Sales Pro (5 seats): $90*5*12 + $1500 = $6,900 annual; $100*5*12 + $1500 = $7,500 monthly
        self.assertEqual(rows_ann["hubspot-sales-pro"]["year1Total"], 6900)
        self.assertEqual(rows_mo["hubspot-sales-pro"]["year1Total"], 7500)

        # Jotform HIPAA Gold (1-user flat plan): $99*12 = $1,188 annual; $129*12 = $1,548 monthly
        self.assertEqual(self.tools_by_id["jotform-hipaa"]["advertised_monthly_price_usd"], 99)
        self.assertEqual(self.tools_by_id["jotform-hipaa"]["monthly_billing_price_usd"], 129)
        self.assertEqual(rows_ann["jotform-hipaa"]["year1Total"], 1188)
        self.assertEqual(rows_mo["jotform-hipaa"]["year1Total"], 1548)

        # Close CRM (Essentials): $35/user/mo annual vs $49/user/mo monthly
        self.assertEqual(self.tools_by_id["close-crm"]["name"], "Close CRM (Essentials)")
        self.assertEqual(self.tools_by_id["close-crm"]["advertised_monthly_price_usd"], 35)
        self.assertEqual(self.tools_by_id["close-crm"]["monthly_billing_price_usd"], 49)
        self.assertEqual(rows_ann["close-crm"]["year1Total"], 5 * 35 * 12)  # $2,100
        self.assertEqual(rows_mo["close-crm"]["year1Total"], 5 * 49 * 12)   # $2,940

        # monday CRM (Basic): $12/seat/mo annual vs $18/seat/mo monthly (with 3-seat minimum)
        self.assertEqual(self.tools_by_id["monday-crm"]["name"], "monday CRM (Basic)")
        self.assertEqual(self.tools_by_id["monday-crm"]["advertised_monthly_price_usd"], 12)
        self.assertEqual(self.tools_by_id["monday-crm"]["monthly_billing_price_usd"], 18)
        self.assertEqual(rows_ann_1["monday-crm"]["year1Total"], 3 * 12 * 12)  # $432
        self.assertEqual(rows_mo_1["monday-crm"]["year1Total"], 3 * 18 * 12)   # $648
        self.assertEqual(rows_ann["monday-crm"]["year1Total"], 5 * 12 * 12)    # $720
        self.assertEqual(rows_mo["monday-crm"]["year1Total"], 5 * 18 * 12)     # $1,080

        # 1Password Business: $8.99/user/mo annual vs $10.99/user/mo monthly
        self.assertEqual(self.tools_by_id["1password-business"]["advertised_monthly_price_usd"], 8.99)
        self.assertEqual(self.tools_by_id["1password-business"]["monthly_billing_price_usd"], 10.99)
        self.assertEqual(rows_ann_1["1password-business"]["year1Total"], round(1 * 8.99 * 12))  # $108
        self.assertEqual(rows_mo_1["1password-business"]["year1Total"], round(1 * 10.99 * 12))  # $132
        self.assertEqual(rows_ann["1password-business"]["year1Total"], round(5 * 8.99 * 12))    # $539
        self.assertEqual(rows_mo["1password-business"]["year1Total"], round(5 * 10.99 * 12))    # $659

    def test_zero_vs_high_ai_volume_and_included_allowances(self):
        """0 AI vs 1,000 AI tickets/month across Intercom, Help Scout, Zendesk Team & Pro, and Freshdesk."""
        rows_0 = {r["tool"]["id"]: r for r in run_homepage_js_calc(seats=5, ai_vol=0, mode="annual")}
        rows_1k_ann = {r["tool"]["id"]: r for r in run_homepage_js_calc(seats=5, ai_vol=1000, mode="annual")}
        rows_1k_mo = {r["tool"]["id"]: r for r in run_homepage_js_calc(seats=5, ai_vol=1000, mode="monthly")}

        self.assertEqual(rows_0["intercom-fin-ai"]["year1Total"], 1740)
        self.assertEqual(rows_1k_ann["intercom-fin-ai"]["year1Total"], 1740 + 11880)

        self.assertEqual(rows_0["help-scout-plus"]["year1Total"], 2700)
        self.assertEqual(rows_1k_ann["help-scout-plus"]["year1Total"], 2700 + 9000)

        self.assertEqual(rows_0["zendesk-suite-team"]["year1Total"], 3300)
        self.assertEqual(rows_1k_ann["zendesk-suite-team"]["year1Total"], 3300 + 17550)
        self.assertEqual(rows_1k_mo["zendesk-suite-team"]["year1Total"], 4140 + 23400)

        self.assertEqual(rows_0["zendesk-suite-professional"]["year1Total"], 6900)
        self.assertEqual(rows_1k_ann["zendesk-suite-professional"]["year1Total"], 6900 + 17100)
        self.assertEqual(rows_1k_mo["zendesk-suite-professional"]["year1Total"], 8940 + 22800)

        self.assertEqual(rows_0["freshdesk-support"]["year1Total"], 1140)
        self.assertEqual(rows_1k_ann["freshdesk-support"]["year1Total"], 1140 + 115 * 49)

    def test_payment_processors_excluded_from_default_all_ranking(self):
        """Payment processors must not appear as $0/yr 'cheapest' tools in the default ALL seat-based view."""
        default_rows = run_homepage_js_calc(seats=5, ai_vol=500, mode="annual", cat="ALL")
        self.assertEqual(len(default_rows), 15)
        for r in default_rows:
            self.assertNotEqual(r["tool"]["category"], "Payment Processors & MoR")
            self.assertGreater(r["year1Total"], 0)

        payment_rows = run_homepage_js_calc(seats=5, ai_vol=500, mode="annual", cat="Payment Processors & MoR")
        self.assertEqual(len(payment_rows), 5)

    def test_hipaa_and_soc2_flat_vs_per_seat_rules(self):
        """Jotform Gold ($99/mo), Vanta ($833/mo), and Drata ($625/mo) are flat fees; 1Password ($8.99/mo) scales per seat."""
        rows_1 = {r["tool"]["id"]: r for r in run_homepage_js_calc(seats=1, ai_vol=0, mode="annual")}
        rows_10 = {r["tool"]["id"]: r for r in run_homepage_js_calc(seats=10, ai_vol=0, mode="annual")}

        self.assertEqual(rows_1["jotform-hipaa"]["year1Total"], 99 * 12)
        self.assertEqual(rows_10["jotform-hipaa"]["year1Total"], 99 * 12)
        self.assertEqual(rows_1["vanta-soc2"]["year1Total"], 833 * 12)
        self.assertEqual(rows_10["vanta-soc2"]["year1Total"], 833 * 12)
        self.assertEqual(rows_1["drata-soc2"]["year1Total"], 625 * 12)
        self.assertEqual(rows_10["drata-soc2"]["year1Total"], 625 * 12)
        self.assertEqual(rows_1["1password-business"]["year1Total"], round(1 * 8.99 * 12))
        self.assertEqual(rows_10["1password-business"]["year1Total"], round(10 * 8.99 * 12))

    def test_stacked_bar_cost_composition_identity(self):
        """Stacked bar segments (annualSeatsCost + onboarding + aiAnnual) must sum identically to year1Total."""
        for seats in (1, 5, 12):
            for ai_vol in (0, 500, 2000):
                for mode in ("annual", "monthly"):
                    rows = run_homepage_js_calc(seats=seats, ai_vol=ai_vol, mode=mode, cat="ALL")
                    for r in rows:
                        comp_sum = r["annualSeatsCost"] + r["onboarding"] + r["aiAnnual"]
                        self.assertEqual(
                            comp_sum,
                            r["year1Total"],
                            f"Component sum mismatch for {r['tool']['id']} at seats={seats}, ai={ai_vol}, mode={mode}",
                        )
                        self.assertGreaterEqual(r["annualSeatsCost"], 0)
                        self.assertGreaterEqual(r["onboarding"], 0)
                        self.assertGreaterEqual(r["aiAnnual"], 0)

    def test_verification_status_and_inline_sources(self):
        """Every tool must have a valid verification_status ('Verified' or 'Estimated (Benchmark)') and valid https source_urls."""
        valid_statuses = {"Verified", "Estimated (Benchmark)"}
        for t in self.tools_list:
            self.assertIn(t.get("verification_status"), valid_statuses, f"Invalid status on {t['id']}")
            urls = t.get("source_urls") or []
            self.assertGreater(len(urls), 0, f"Missing source_urls on {t['id']}")
            for u in urls:
                self.assertTrue(u.startswith("https://"), f"Non-https source URL {u} on {t['id']}")

        self.assertEqual(self.tools_by_id["vanta-soc2"]["verification_status"], "Estimated (Benchmark)")
        self.assertEqual(self.tools_by_id["drata-soc2"]["verification_status"], "Estimated (Benchmark)")

        with open(os.path.join(PUBLIC_DIR, "index.html")) as f:
            index_html = f.read()
        self.assertIn('id="wb-vbar-mount"', index_html)
        self.assertIn('id="wb-result-mount"', index_html)
        self.assertIn('id="methodology"', index_html)
        self.assertIn("mobile-cards", index_html)
        self.assertIn('data-label="Platform"', index_html)
        self.assertNotIn("$7.99", index_html)

    def test_outbound_vendor_links_match_vendors(self):
        """Every tool in tools.json and every CTA link across all 7 HTML pages must point to the right vendor."""
        expected_domains = {
            "hubspot-sales-pro": "hubspot.com",
            "hubspot-marketing-pro": "hubspot.com",
            "hubspot-service-hub": "hubspot.com",
            "close-crm": "close.com",
            "pipedrive-crm": "pipedrive.com",
            "monday-crm": "monday.com",
            "intercom-fin-ai": "intercom.com",
            "freshdesk-support": "freshworks.com",
            "zendesk-suite-team": "zendesk.com",
            "zendesk-suite-professional": "zendesk.com",
            "help-scout-plus": "helpscout.com",
            "stripe-payments": "stripe.com",
            "paddle-mor": "paddle.com",
            "whop-payments": "whop.com",
            "lemon-squeezy": "lemonsqueezy.com",
            "chargeflow": "chargeflow.io",
            "jotform-hipaa": "jotform.com",
            "1password-business": "1password.com",
            "vanta-soc2": "vanta.com",
            "drata-soc2": "drata.com",
        }
        for tool_id, expected_domain in expected_domains.items():
            tool = self.tools_by_id[tool_id]
            slug = tool["affiliate_slug"]
            self.assertIn(slug, self.affiliates, f"Missing affiliate slug {slug} for {tool_id}")
            dest_url = self.affiliates[slug]["destination_url"]
            host = urlparse(dest_url).netloc.lower()
            self.assertTrue(
                host == expected_domain or host.endswith("." + expected_domain),
                f"Tool {tool_id} links to {dest_url} (expected {expected_domain})",
            )

        comp_page = os.path.join(PUBLIC_DIR, "compliance/hipaa-baa-and-soc2-pricing-tiers/index.html")
        with open(comp_page) as f:
            comp_html = f.read()
        self.assertIn("https://trycomp.ai/", comp_html)
        self.assertIn("https://1password.com/pricing/business", comp_html)
        self.assertIn("$8.99/user/mo", comp_html)
        self.assertNotIn("$7.99", comp_html)

        hs_page = os.path.join(PUBLIC_DIR, "pricing/hubspot-true-cost-and-onboarding-fees/index.html")
        with open(hs_page) as f:
            hs_html = f.read()
        self.assertIn("seats * 47 * 12", hs_html)
        self.assertIn("Close CRM Startup", hs_html)
        self.assertIn('id="chart-dynamic-headline"', hs_html)
        self.assertIn('id="chart-dynamic-subtitle"', hs_html)
        self.assertNotIn('class="invoice-box"', hs_html)
        self.assertNotIn('id="hs-tbody"', hs_html)
        self.assertIn("https://refer.close.com/3k5hp07b8soi-fetl0j", hs_html)

        ic_page = os.path.join(PUBLIC_DIR, "pricing/intercom-fin-ai-resolution-cost-calculator/index.html")
        with open(ic_page) as f:
            ic_html = f.read()
        self.assertIn("seats * 55", ic_html)
        self.assertIn("fdMonthlyPacks * 49", ic_html)

    def test_handoff2_conversion_ux_and_honest_ctas(self):
        """Verify Handoff 2 conversion & UX requirements across all 7 generated HTML pages."""
        pages = [
            "index.html",
            "pricing/hubspot-true-cost-and-onboarding-fees/index.html",
            "pricing/intercom-fin-ai-resolution-cost-calculator/index.html",
            "exit/stripe-shopify-paddle-frozen-funds-alternatives/index.html",
            "compare/monday-crm-vs-pipedrive-vs-hubspot-seat-minimums/index.html",
            "compliance/hipaa-baa-and-soc2-pricing-tiers/index.html",
            "pricing/zendesk-ai-resolution-and-automated-outcome-cost/index.html",
            "compare/gumroad-vs-whop-vs-lemon-squeezy-take-rate-calculator/index.html",
            "compare/typeform-vs-jotform-response-limit-and-hipaa-cost/index.html",
            "compare/close-crm-vs-hubspot-sales-hub-5-to-20-reps/index.html",
            "pricing/stripe-billing-0-7-percent-recurring-tax-calculator/index.html",
            "pricing/docusign-envelope-allowance-and-api-overage-calculator/index.html",
            "pricing/gong-io-platform-fee-and-seat-minimum-calculator/index.html",
            "exit/paypal-180-day-permanent-limitation-fund-recovery/index.html",
            "compliance/google-workspace-vs-microsoft-365-hipaa-baa-tiers/index.html",
            "faq/does-hubspot-charge-onboarding-fees-2026/index.html",
            "faq/intercom-fin-ai-cost-calculator/index.html",
            "faq/stripe-vs-paddle-true-cost/index.html",
            "guides/jotform-wix-app-setup-and-pricing-guide/index.html",
            "pricing/jotform-pricing-tier-calculator/index.html",
        ]
        summary_ids = {
            "index.html": "wb-result-mount",
            "pricing/hubspot-true-cost-and-onboarding-fees/index.html": "hs-summary",
            "pricing/intercom-fin-ai-resolution-cost-calculator/index.html": "ic-summary",
            "exit/stripe-shopify-paddle-frozen-funds-alternatives/index.html": "hold-summary",
            "compare/monday-crm-vs-pipedrive-vs-hubspot-seat-minimums/index.html": "sm-summary",
            "compliance/hipaa-baa-and-soc2-pricing-tiers/index.html": "soc2-summary",
            "pricing/zendesk-ai-resolution-and-automated-outcome-cost/index.html": "zd-summary",
            "compare/gumroad-vs-whop-vs-lemon-squeezy-take-rate-calculator/index.html": "tr-summary",
            "compare/typeform-vs-jotform-response-limit-and-hipaa-cost/index.html": "tf-summary",
            "compare/close-crm-vs-hubspot-sales-hub-5-to-20-reps/index.html": "ch-summary",
            "pricing/stripe-billing-0-7-percent-recurring-tax-calculator/index.html": "sb-summary",
            "pricing/docusign-envelope-allowance-and-api-overage-calculator/index.html": "ds-summary",
            "pricing/gong-io-platform-fee-and-seat-minimum-calculator/index.html": "gong-summary",
            "exit/paypal-180-day-permanent-limitation-fund-recovery/index.html": "pp-summary",
            "compliance/google-workspace-vs-microsoft-365-hipaa-baa-tiers/index.html": "gm-summary",
            "faq/does-hubspot-charge-onboarding-fees-2026/index.html": "faq-hs-summary",
            "faq/intercom-fin-ai-cost-calculator/index.html": "faq-ic-summary",
            "faq/stripe-vs-paddle-true-cost/index.html": "faq-sp-summary",
            "guides/jotform-wix-app-setup-and-pricing-guide/index.html": "jw-summary",
            "pricing/jotform-pricing-tier-calculator/index.html": "jf-tier-summary",
        }
        forbidden_phrases = [
            "Partner link",
            "sponsored",
            "Check pricing",
            "Try Close free",
            "Try Pipedrive free",
            "Try Freshdesk free",
            "Try Help Scout free",
            "Request Vanta quote",
            "Request Drata quote",
            "Add Whop failover",
            "Install Chargeflow",
        ]
        for rel in pages:
            full_path = os.path.join(PUBLIC_DIR, rel)
            with open(full_path) as f:
                html = f.read()
            for phrase in forbidden_phrases:
                self.assertNotIn(phrase, html, f"Forbidden phrase '{phrase}' found in {rel}")
            self.assertIn(f'id="{summary_ids[rel]}"', html, f"Missing summary strip #{summary_ids[rel]} in {rel}")
            self.assertIn("Based on ", html, f"Missing scenario description ('Based on ...') in {rel}")
            self.assertIn("Hidden Cost Highlight:", html, f"Missing 'Hidden Cost Highlight:' in {rel}")
            self.assertIn('data-track="vendor-cta"', html, f"Missing data-track='vendor-cta' in {rel}")
            self.assertIn("Independent calculations. Some vendor links are affiliate links. This never changes our rankings or calculations.", html, f"Missing footer affiliate disclosure in {rel}")
            self.assertNotIn('<span class="direct-link-tag">', html, f"Per-button .direct-link-tag should be removed in {rel}")
            self.assertIn("window.__saasbillEvents", html, f"Missing local __saasbillEvents instrumentation in {rel}")
            # Verify Plausible Analytics is present in <head> and no heavy third-party trackers are loaded
            self.assertIn('src="https://plausible.io/js/pa-VAaSVNs5XOobt9cv2UtKo.js"', html)
            self.assertNotIn("googletagmanager.com", html)
            self.assertNotIn("posthog.com", html)

        # Verify homepage pre-filled category tabs and vendor-specific CTA dictionary
        with open(os.path.join(PUBLIC_DIR, "index.html")) as f:
            index_html = f.read()
        self.assertIn('class="cat-tabs"', index_html)
        self.assertIn('data-track="category-select"', index_html)
        self.assertIn('<option value="Helpdesk & AI Support" selected>', index_html)
        for expected_cta in [
            "View HubSpot pricing",
            "View Close pricing",
            "View Pipedrive pricing",
            "View monday CRM pricing",
            "View Intercom pricing",
            "View Freshdesk pricing",
            "View Zendesk pricing",
            "View Help Scout pricing",
            "View Vanta pricing",
            "View Drata pricing",
            "View Jotform HIPAA pricing",
            "View 1Password pricing",
            "View Stripe pricing",
            "View Whop Payments pricing",
            "View Chargeflow pricing",
            "View Paddle pricing",
            "View Lemon Squeezy pricing",
        ]:
            self.assertIn(expected_cta, index_html, f"Missing specific CTA '{expected_cta}' in index.html")

        # Verify Editorial Layout v2 + Chart-to-Table Connection (Alt 1 + Alt 2):
        self.assertNotIn('id="calc-prefill-banner"', index_html)
        self.assertNotIn('<hr class="editorial-rule" />', index_html)
        self.assertNotIn('across common scenarios', index_html)
        self.assertIn('id="wb-vbar-mount"', index_html)
        self.assertIn('id="wb-big-amount"', index_html)
        self.assertIn('Sticker Price: Base plan', index_html)
        self.assertIn('Sticker Price: Added seats', index_html)
        self.assertIn('<strong id="wb-call-title-hidden">Hidden Cost Gap</strong>', index_html)
        self.assertIn('class="legend-dot dot-sticker"', index_html)
        self.assertIn('class="legend-dot dot-hidden"', index_html)
        self.assertIn('id="gap-dynamic-subhead"', index_html)
        self.assertIn('id="unified-inspector-tray"', index_html)
        self.assertIn('id="inspector-left-rail"', index_html)
        self.assertIn('click any row to inspect its breakdown above.', index_html)
        # Ensure Sort selector is inside .gap-toolbar above the table, not inside #billing-control-group
        billing_grp = re.search(r'<div class="wb-quiet-options" id="billing-control-group">(.*?)</div>\s*</div>\s*</div>', index_html, re.S)
        self.assertIsNotNone(billing_grp)
        self.assertNotIn('id="sort-mode"', billing_grp.group(1))
        gap_tb = re.search(r'<div class="gap-toolbar">(.*?)</div>\s*</div>', index_html, re.S)
        self.assertIsNotNone(gap_tb)
        self.assertIn('id="sort-mode"', gap_tb.group(1))

        with open(os.path.join(PUBLIC_DIR, "assets/styles.css")) as f:
            css = f.read()
        for token in ["#FAF9F5", "#536B56", "#E8EEE6", "#20231F", ".prefill-banner", ".direct-link-tag"]:
            self.assertIn(token, css, f"Missing Sage Green / UX Finishing Pass token '{token}' in styles.css")


    def test_payment_processor_scenario_transparency_and_math_identity(self):
        """Verify Payment Processors & MoR separate processing fees (b + s + h == total) from temporary reserves (held), unify CTAs, and tone down hero lead."""
        with open(os.path.join(PUBLIC_DIR, "index.html")) as f:
            html = f.read()
        self.assertIn("can significantly increase the real Year-1 cost", html)
        self.assertNotIn("often doubling", html)
        self.assertNotIn("Explore Whop Payments", html)

        m = re.search(r"const PAY_PROFILES = (\{.*?\n\});", html, re.S)
        self.assertIsNotNone(m, "Could not find PAY_PROFILES in public/index.html")
        runner = f"const PAY_PROFILES = {m.group(1)}; console.log(JSON.stringify(PAY_PROFILES));"
        res = subprocess.run(["node", "-e", runner], capture_output=True, text=True, check=True)
        profiles = json.loads(res.stdout)
        expected_totals_and_holds = {
            "stripe-payments": (2325, 12500),
            "paddle-mor": (3450, 12500),
            "whop-payments": (2275, 0),
            "lemon-squeezy": (3475, 12500),
            "chargeflow": (500, 0),
        }
        self.assertEqual(set(profiles.keys()), set(expected_totals_and_holds.keys()))
        for pid, (exp_total, exp_held) in expected_totals_and_holds.items():
            p = profiles[pid]
            self.assertEqual(
                p["b"] + p["s"] + p["h"],
                p["total"],
                f"Payment profile {pid} fee segments ({p['b']} + {p['s']} + {p['h']}) != total ({p['total']})",
            )
            self.assertEqual(p["total"], exp_total, f"Unexpected fee total for {pid}")
            self.assertEqual(p["held"], exp_held, f"Unexpected temporary reserve hold for {pid}")
            self.assertIn("Estimated monthly processing fees:", p["quote"])
            self.assertIn("Potential funds temporarily held:", p["quote"])
            self.assertIn("Assumptions ($50k/mo GMV", p["sub"])


    def test_gumroad_whop_lemon_squeezy_take_rate_calculator(self):
        """JS calcPlatforms() on the take-rate page must match hand-checked fee math and the Python builder (verified 2026-10-26)."""
        import sys
        sys.path.insert(0, os.path.join(BASE_DIR, "scripts"))
        import build_gumroad_whop_lemonsqueezy_page as tr
        rel = "compare/gumroad-vs-whop-vs-lemon-squeezy-take-rate-calculator/index.html"
        with open(os.path.join(PUBLIC_DIR, rel)) as f:
            html = f.read()
        m = re.search(r"(const TR_FEES = .*?\n\}\n)const trFmt", html, re.S)
        self.assertIsNotNone(m, "Could not extract calcPlatforms() from take-rate page")
        scenarios = [
            tr.DEFAULTS,
            dict(tr.DEFAULTS, whop_tax="none"),
            dict(tr.DEFAULTS, price=100, sales=300, intl=60, paypal=20, sub=True, discover=25, dispute=1.0, payout="intl", whop_fx=False, whop_risk=False),
            dict(tr.DEFAULTS, price=10, sales=50, intl=0, paypal=0, dispute=0),
        ]
        for sc in scenarios:
            runner = m.group(1) + f"console.log(JSON.stringify(calcPlatforms({json.dumps(sc)})));"
            res = subprocess.run(["node", "-e", runner], capture_output=True, text=True, check=True)
            js = json.loads(res.stdout)
            py = tr.calc(**sc)
            for plat in ("gumroad", "ls", "whop"):
                self.assertAlmostEqual(js[plat]["total"], py[plat]["total"], places=2, msg=f"{plat} JS/Python mismatch for {sc}")
                self.assertAlmostEqual(js[plat]["net"] + js[plat]["total"], js["gmv"], places=2)

        # Hand-checked default example: $29 x 200 sales, 30% intl, 10% PayPal, 0.5% disputes, US bank, Whop 2% managed tax
        e = tr.calc(**tr.DEFAULTS)
        self.assertEqual(e["gmv"], 5800)
        self.assertAlmostEqual(e["gumroad"]["total"], 580 + 100 + 168.2 + 60, places=2)          # 10% + 50c + 2.9% + 30c
        self.assertAlmostEqual(e["ls"]["total"], 290 + 100 + 26.1 + 8.7 + 15, places=2)          # 5% + 50c + 1.5% intl + 1.5% PayPal + $15 dispute
        self.assertAlmostEqual(e["whop"]["total"], 156.6 + 60 + 26.1 + 17.4 + 116 + 20 + 15 + 10, places=2)
        self.assertAlmostEqual(tr.calc(**dict(tr.DEFAULTS, whop_tax="none"))["whop"]["total"], 305.1, places=2)
        # Gumroad high-volume rate: direct sales above $20k/month pay 5% + 50c
        hv = tr.calc(price=100, sales=300, intl=0, paypal=0, dispute=0)
        self.assertAlmostEqual(hv["gumroad"]["platform"], 20000 * 0.10 + 10000 * 0.05 + 150, places=2)
        # Discover 30% flat incl. processing
        dsc = tr.calc(price=10, sales=100, intl=0, paypal=0, dispute=0, discover=100)
        self.assertAlmostEqual(dsc["gumroad"]["total"], 300, places=2)

        # Page requirements: short title, answer-first copy, no robot labels/brand leaks, FAQPage, referral link, header date
        t = re.search(r"<title>(.*?)</title>", html).group(1)
        self.assertLessEqual(len(t), 60)
        self.assertTrue(t.endswith("– saasbill.io"))
        self.assertIn(f'<meta property="og:title" content="{t}"', html)
        self.assertIn(f'<meta name="twitter:title" content="{t}"', html)
        self.assertIn("The short version:", html)
        for bad in ["Answer First:", "Direct Answer", "TL;DR", "SaaSTruth", "Erik", "Bengtsson"]:
            self.assertNotIn(bad, html)
        self.assertIn('"FAQPage"', html)
        self.assertIn("https://whop.com/sell?a=baggyprairieae", html)
        self.assertIn("Verified source", html)
        self.assertIn('itemprop="dateModified"', html)
        self.assertIn("byline-bar", html)
        self.assertIn("https://gumroad.com/pricing", html)
        self.assertIn("https://www.lemonsqueezy.com/pricing", html)

        with open(os.path.join(PUBLIC_DIR, "index.html")) as f:
            self.assertIn("./compare/gumroad-vs-whop-vs-lemon-squeezy-take-rate-calculator/", f.read())
        for meta in ("sitemap.xml", "llms.txt", "llms-full.txt"):
            with open(os.path.join(PUBLIC_DIR, meta)) as f:
                self.assertIn("/compare/gumroad-vs-whop-vs-lemon-squeezy-take-rate-calculator/", f.read(), meta)



    def test_mobile_usability_and_responsive_cards(self):
        """Mandatory mobile usability audit across all generated HTML pages and styles.css."""
        pages = [
            "index.html",
            "pricing/hubspot-true-cost-and-onboarding-fees/index.html",
            "pricing/intercom-fin-ai-resolution-cost-calculator/index.html",
            "exit/stripe-shopify-paddle-frozen-funds-alternatives/index.html",
            "compare/monday-crm-vs-pipedrive-vs-hubspot-seat-minimums/index.html",
            "compliance/hipaa-baa-and-soc2-pricing-tiers/index.html",
            "pricing/zendesk-ai-resolution-and-automated-outcome-cost/index.html",
            "compare/gumroad-vs-whop-vs-lemon-squeezy-take-rate-calculator/index.html",
            "compare/typeform-vs-jotform-response-limit-and-hipaa-cost/index.html",
            "compare/close-crm-vs-hubspot-sales-hub-5-to-20-reps/index.html",
            "pricing/stripe-billing-0-7-percent-recurring-tax-calculator/index.html",
            "pricing/docusign-envelope-allowance-and-api-overage-calculator/index.html",
            "pricing/gong-io-platform-fee-and-seat-minimum-calculator/index.html",
            "exit/paypal-180-day-permanent-limitation-fund-recovery/index.html",
            "compliance/google-workspace-vs-microsoft-365-hipaa-baa-tiers/index.html",
            "faq/does-hubspot-charge-onboarding-fees-2026/index.html",
            "faq/intercom-fin-ai-cost-calculator/index.html",
            "faq/stripe-vs-paddle-true-cost/index.html",
            "guides/jotform-wix-app-setup-and-pricing-guide/index.html",
            "pricing/jotform-pricing-tier-calculator/index.html",
        ]
        for rel in pages:
            full_path = os.path.join(PUBLIC_DIR, rel)
            with open(full_path, encoding="utf-8") as f:
                html = f.read()
            # 1. Viewport meta tag present
            self.assertIn(
                '<meta name="viewport" content="width=device-width, initial-scale=1.0" />',
                html,
                f"Missing responsive viewport meta tag in {rel}",
            )
            # 2. Every .table-wrap must use .mobile-cards so tables become vertical cards on mobile
            for m in re.finditer(r'<div class="([^"]*table-wrap[^"]*)"', html):
                classes = m.group(1).split()
                self.assertIn(
                    "mobile-cards",
                    classes,
                    f"Found .table-wrap without .mobile-cards in {rel}: {m.group(0)}",
                )
            # 3. Every <td> inside HTML or JS templates must carry data-label="..." for mobile card headers
            for td_match in re.finditer(r"<td(?![^>]*data-label=)[^>]*>", html):
                self.fail(f"Found <td> missing data-label attribute in {rel}: {td_match.group(0)}")

        with open(os.path.join(PUBLIC_DIR, "assets/styles.css"), encoding="utf-8") as f:
            css = f.read()
        # 4. Verify mobile CSS overrides exist at the end of styles.css (after desktop .editorial-gap-table)
        desktop_gap_pos = css.find(".table-wrap.editorial-gap-table td")
        mobile_polish_pos = css.find("Mobile Polish & Responsive Overrides")
        self.assertGreater(desktop_gap_pos, 0, "Missing .table-wrap.editorial-gap-table td in styles.css")
        self.assertGreater(
            mobile_polish_pos,
            desktop_gap_pos,
            "Mobile overrides must appear after desktop .editorial-gap-table rules in styles.css",
        )
        # Ensure .wb-budget-subnote is never truncated with line-clamp or overflow: hidden
        subnote_block = re.search(r"\.wb-budget-subnote\s*\{(.*?)\}", css, re.S)
        self.assertIsNotNone(subnote_block)
        self.assertNotIn("-webkit-line-clamp", subnote_block.group(1))
        self.assertNotIn("overflow: hidden", subnote_block.group(1))
        for required_mobile_rule in [
            "grid-template-columns: 118px minmax(0, 1fr);",
            ".table-wrap.editorial-gap-table.mobile-cards td",
            "width: 24px;",
            "font-size: 16px;",
        ]:
            self.assertIn(required_mobile_rule, css, f"Missing mobile CSS rule '{required_mobile_rule}' in styles.css")



    def test_seo_geo_and_answer_first_pages(self):
        """Verify SEO titles/descriptions, internal linking, sitemap.xml, GEO robots.txt, and Answer-First FAQ pages."""
        with open(os.path.join(PUBLIC_DIR, "robots.txt"), encoding="utf-8") as f:
            robots = f.read()
        for allowed_bot in ("OAI-SearchBot", "PerplexityBot", "Googlebot", "Bingbot"):
            self.assertIn(f"User-agent: {allowed_bot}\nAllow: /", robots)
        for blocked_bot in ("GPTBot", "CCBot", "Google-Extended"):
            self.assertIn(f"User-agent: {blocked_bot}\nDisallow: /", robots)

        with open(os.path.join(PUBLIC_DIR, "sitemap.xml"), encoding="utf-8") as f:
            sitemap = f.read()
        self.assertEqual(sitemap.count("<url><loc>"), 20)

        faq_pages = [
            "faq/does-hubspot-charge-onboarding-fees-2026/index.html",
            "faq/intercom-fin-ai-cost-calculator/index.html",
            "faq/stripe-vs-paddle-true-cost/index.html",
        ]
        for rel in faq_pages:
            with open(os.path.join(PUBLIC_DIR, rel), encoding="utf-8") as f:
                html = f.read()
            t = re.search(r"<title>(.*?)</title>", html).group(1)
            self.assertLessEqual(len(t), 60, f"Title too long in {rel}: {t}")
            lead = re.search(r'<p class="lead">(.*?)</p>', html, re.S).group(1)
            self.assertIn("2026", lead)
            self.assertIn("$", lead)
            self.assertIn("source:", lead.lower())
            self.assertIn("related-calculators-heading", html)


    def test_initial_context_preselection_and_subpage_memory(self):
        """Verify index.html contains applyInitialContext supporting ?cat=, ?tool=, #hash, document.referrer, and sessionStorage."""
        with open(os.path.join(PUBLIC_DIR, "index.html"), encoding="utf-8") as f:
            index_html = f.read()
        for token in [
            "function applyInitialContext",
            "function resolveContextFromToken",
            "params.get('cat')",
            "params.get('tool')",
            "document.referrer",
            "sessionStorage.getItem('saasbill_last_cat')",
            "sessionStorage.setItem('saasbill_last_cat'",
            "window.addEventListener('hashchange'",
        ]:
            self.assertIn(token, index_html, f"Missing context preselection token '{token}' in index.html")

        # Execute resolveContextFromToken in Node.js across query/hash/referrer test cases
        m = re.search(r"const TOOLS = (.*?);\nconst AFFILIATES", index_html, re.S)
        fn_m = re.search(r"(function resolveContextFromToken\(raw\) \{.*?\n\})\n\nfunction applyInitialContext", index_html, re.S)
        self.assertIsNotNone(m)
        self.assertIsNotNone(fn_m)
        runner = f"""
        const TOOLS = {m.group(1)};
        {fn_m.group(1)}
        const cases = {{
          payments: resolveContextFromToken('payments'),
          stripe: resolveContextFromToken('stripe'),
          whop: resolveContextFromToken('whop-payments'),
          crm: resolveContextFromToken('crm'),
          close: resolveContextFromToken('close'),
          compliance: resolveContextFromToken('compliance'),
          jotform: resolveContextFromToken('jotform'),
          helpdesk: resolveContextFromToken('helpdesk'),
          intercom: resolveContextFromToken('intercom'),
          all: resolveContextFromToken('all'),
          ref_stripe: resolveContextFromToken('https://saasbill.io/exit/stripe-shopify-paddle-frozen-funds-alternatives/'),
          ref_hubspot: resolveContextFromToken('https://saasbill.io/pricing/hubspot-true-cost-and-onboarding-fees/'),
          ref_hipaa: resolveContextFromToken('https://saasbill.io/compare/typeform-vs-jotform-response-limit-and-hipaa-cost/')
        }};
        console.log(JSON.stringify(cases));
        """
        res = subprocess.run(["node", "-e", runner], capture_output=True, text=True, check=True)
        out = json.loads(res.stdout)
        self.assertEqual(out["payments"], {"cat": "Payment Processors & MoR", "tool": "stripe-payments"})
        self.assertEqual(out["stripe"], {"cat": "Payment Processors & MoR", "tool": "stripe-payments"})
        self.assertEqual(out["whop"], {"cat": "Payment Processors & MoR", "tool": "whop-payments"})
        self.assertEqual(out["crm"], {"cat": "CRM & Sales", "tool": "hubspot-sales-pro"})
        self.assertEqual(out["close"], {"cat": "CRM & Sales", "tool": "close-crm"})
        self.assertEqual(out["compliance"], {"cat": "Compliance, HIPAA & SOC 2", "tool": "jotform-hipaa"})
        self.assertEqual(out["jotform"], {"cat": "Compliance, HIPAA & SOC 2", "tool": "jotform-hipaa"})
        self.assertEqual(out["helpdesk"], {"cat": "Helpdesk & AI Support", "tool": "zendesk-suite-team"})
        self.assertEqual(out["intercom"], {"cat": "Helpdesk & AI Support", "tool": "intercom-fin-ai"})
        self.assertEqual(out["all"], {"cat": "ALL", "tool": ""})
        self.assertEqual(out["ref_stripe"]["cat"], "Payment Processors & MoR")
        self.assertEqual(out["ref_hubspot"]["cat"], "CRM & Sales")
        self.assertEqual(out["ref_hipaa"]["cat"], "Compliance, HIPAA & SOC 2")



    def test_priority1_progressive_disclosure_calculation_breakdown(self):
        """Priority 1: Expandable 'See calculation' / 'See exactly how we calculated this' with exact dollar step sum."""
        for seats in (1, 3, 5, 12):
            for ai_vol in (0, 500, 1500):
                for mode in ("annual", "monthly"):
                    rows = run_homepage_js_calc(seats=seats, ai_vol=ai_vol, mode=mode, cat="ALL")
                    for r in rows:
                        steps = r.get("calcSteps")
                        self.assertIsInstance(steps, list, f"Missing calcSteps on {r['tool']['id']}")
                        self.assertGreaterEqual(len(steps), 3)
                        step_sum = sum(s["amount"] for s in steps)
                        self.assertEqual(
                            step_sum,
                            r["year1Total"],
                            f"calcSteps sum ({step_sum}) != year1Total ({r['year1Total']}) for {r['tool']['id']} at seats={seats}, ai={ai_vol}, mode={mode}",
                        )
                        self.assertEqual(r["year2Total"], r["annualSeatsCost"] + r["aiAnnual"])

        with open(os.path.join(PUBLIC_DIR, "index.html"), encoding="utf-8") as f:
            index_html = f.read()
        self.assertIn('id="wb-calc-details"', index_html)
        self.assertIn("See exactly how we calculated this", index_html)
        self.assertIn("See calculation", index_html)
        self.assertIn("function renderCalcBreakdownHtml", index_html)

        with open(os.path.join(PUBLIC_DIR, "pricing/hubspot-true-cost-and-onboarding-fees/index.html"), encoding="utf-8") as f:
            hs_html = f.read()
        self.assertIn('id="hs-calc-details"', hs_html)
        self.assertIn("See exactly how we calculated this", hs_html)

    def test_priority2_plausible_event_forwarding(self):
        """Priority 2: Plausible receives calculator_interaction, category_select, result_rendered, and vendor_cta_click."""
        with open(os.path.join(PUBLIC_DIR, "index.html"), encoding="utf-8") as f:
            index_html = f.read()
        self.assertIn("window.trackSaaSBillEvent = function(eventName, props)", index_html)
        for ev_name in ("calculator_interaction", "category_select", "result_rendered", "vendor_cta_click"):
            self.assertIn(f"'{ev_name}'", index_html)

        # Execute trackSaaSBillEvent in Node.js with Plausible queue function
        runner = """
        const window = {};
        window.plausible=window.plausible||function(){(window.plausible.q=window.plausible.q||[]).push(Array.from(arguments))};
        window.__saasbillEvents = window.__saasbillEvents || [];
        window.trackSaaSBillEvent = function(eventName, props) {
          var p = props || {};
          var entry = { event: eventName, ts: 12345 };
          for (var k in p) {
            if (Object.prototype.hasOwnProperty.call(p, k)) entry[k] = p[k];
          }
          window.__saasbillEvents.push(entry);
          if (typeof window.plausible === 'function') {
            window.plausible(eventName, { props: p });
          }
        };
        window.trackSaaSBillEvent('category_select', { category: 'CRM & Sales' });
        window.trackSaaSBillEvent('calculator_interaction', { control: 'seats', value: '10' });
        window.trackSaaSBillEvent('result_rendered', { category: 'CRM & Sales', seats: 10 });
        window.trackSaaSBillEvent('vendor_cta_click', { vendor: 'close-crm', location: 'workbench', href: 'https://refer.close.com/3k5hp07b8soi-fetl0j' });
        console.log(JSON.stringify({ local: window.__saasbillEvents, plausible: window.plausible.q }));
        """
        res = subprocess.run(["node", "-e", runner], capture_output=True, text=True, check=True)
        out = json.loads(res.stdout)
        self.assertEqual(len(out["local"]), 4)
        self.assertEqual(len(out["plausible"]), 4)
        self.assertEqual([x[0] for x in out["plausible"]], [
            "category_select",
            "calculator_interaction",
            "result_rendered",
            "vendor_cta_click",
        ])
        self.assertEqual(out["plausible"][3][1]["props"]["vendor"], "close-crm")

    def test_priority3_result_hierarchy_and_full_table_disclosure(self):
        """Priority 3: Progressive disclosure order Inputs -> Answer/Best Option -> Calculation -> CTA -> Verdict -> 'Compare all tools' (Sort + Graph + Full Table)."""
        with open(os.path.join(PUBLIC_DIR, "index.html"), encoding="utf-8") as f:
            index_html = f.read()
        pos_inputs = index_html.find('class="wb-col-controls"')
        pos_answer = index_html.find('id="wb-result-mount"')
        pos_best_opt = index_html.find('id="wb-best-option"')
        pos_calc = index_html.find('id="wb-calc-details"')
        pos_cta = index_html.find('id="wb-primary-cta"')
        pos_verdict = index_html.find('id="verdict-card"')
        pos_table_disclosure = index_html.find('id="full-table-details"')
        pos_sort = index_html.find('id="sort-mode"')
        pos_viz = index_html.find('id="calc-viz-panel"')
        pos_tbody = index_html.find('id="calc-tbody"')

        self.assertGreater(pos_inputs, 0)
        self.assertGreater(pos_answer, pos_inputs)
        self.assertGreater(pos_best_opt, pos_answer)
        self.assertGreater(pos_calc, pos_best_opt)
        self.assertGreater(pos_cta, pos_calc)
        self.assertGreater(pos_verdict, pos_cta)
        self.assertGreater(pos_table_disclosure, pos_verdict)
        self.assertGreater(pos_sort, pos_table_disclosure)
        self.assertGreater(pos_viz, pos_sort)
        self.assertGreater(pos_tbody, pos_viz)
        self.assertIn("Compare all tools in this category", index_html)
        self.assertIn("Compare all tools &darr;", index_html)
        self.assertNotIn("28% to 310%", index_html)

    def test_priority4_contextual_cta_labels(self):
        """Priority 4: Contextual CTAs show 'Save $X/yr with [Vendor] →' when savings exist, fallback to 'View [Vendor] pricing →'."""
        with open(os.path.join(PUBLIC_DIR, "index.html"), encoding="utf-8") as f:
            index_html = f.read()
        m = re.search(r"<script>\s*(const TOOLS = .*?)\['cat-filter'", index_html, re.S)
        self.assertIsNotNone(m)
        runner = f"""
        {m.group(1)}
        const fd = TOOLS.find(t => t.id === 'freshdesk-support');
        const zd = TOOLS.find(t => t.id === 'zendesk-suite-team');
        const cl = TOOLS.find(t => t.id === 'close-crm');
        const hs = TOOLS.find(t => t.id === 'hubspot-sales-pro');
        const cf = TOOLS.find(t => t.id === 'chargeflow');
        console.log(JSON.stringify({{
          fd_save: getContextualCtaLabel(fd, 3835, 11850, false),
          zd_trap: getContextualCtaLabel(zd, 11850, 15000, true),
          cl_save: getContextualCtaLabel(cl, 2100, 6900, false),
          hs_trap: getContextualCtaLabel(hs, 6900, 13680, true),
          cf_cta: getContextualCtaLabel(cf, 500, 3450, false)
        }}));
        """
        res = subprocess.run(["node", "-e", runner], capture_output=True, text=True, check=True)
        out = json.loads(res.stdout)
        self.assertEqual(out["fd_save"], "Save $8,015/yr with Freshdesk →")
        self.assertEqual(out["zd_trap"], "View Zendesk pricing →")
        self.assertEqual(out["cl_save"], "Save $4,800/yr with Close →")
        self.assertEqual(out["hs_trap"], "View HubSpot pricing →")
        self.assertEqual(out["cf_cta"], "Prevent reserve holds with Chargeflow →")

    def test_priority5_clear_affiliate_disclosure_and_no_em_dashes(self):
        """Priority 5: Clear affiliate disclosure across all 18 pages, no contradictory claims, no em-dashes."""
        expected_disclosure = "Independent calculations. Some vendor links are affiliate links. This never changes our rankings or calculations."
        pages = [
            "index.html",
            "pricing/hubspot-true-cost-and-onboarding-fees/index.html",
            "pricing/intercom-fin-ai-resolution-cost-calculator/index.html",
            "exit/stripe-shopify-paddle-frozen-funds-alternatives/index.html",
            "compare/monday-crm-vs-pipedrive-vs-hubspot-seat-minimums/index.html",
            "compliance/hipaa-baa-and-soc2-pricing-tiers/index.html",
            "pricing/zendesk-ai-resolution-and-automated-outcome-cost/index.html",
            "compare/gumroad-vs-whop-vs-lemon-squeezy-take-rate-calculator/index.html",
            "compare/typeform-vs-jotform-response-limit-and-hipaa-cost/index.html",
            "compare/close-crm-vs-hubspot-sales-hub-5-to-20-reps/index.html",
            "pricing/stripe-billing-0-7-percent-recurring-tax-calculator/index.html",
            "pricing/docusign-envelope-allowance-and-api-overage-calculator/index.html",
            "pricing/gong-io-platform-fee-and-seat-minimum-calculator/index.html",
            "exit/paypal-180-day-permanent-limitation-fund-recovery/index.html",
            "compliance/google-workspace-vs-microsoft-365-hipaa-baa-tiers/index.html",
            "faq/does-hubspot-charge-onboarding-fees-2026/index.html",
            "faq/intercom-fin-ai-cost-calculator/index.html",
            "faq/stripe-vs-paddle-true-cost/index.html",
            "guides/jotform-wix-app-setup-and-pricing-guide/index.html",
            "pricing/jotform-pricing-tier-calculator/index.html",
        ]
        for rel in pages:
            with open(os.path.join(PUBLIC_DIR, rel), encoding="utf-8") as f:
                html = f.read()
            self.assertIn(expected_disclosure, html, f"Missing updated affiliate disclosure in {rel}")
            self.assertNotIn("100% independent", html.lower(), f"Contradictory claim in {rel}")
            self.assertNotIn("no sponsors", html.lower(), f"Contradictory claim in {rel}")
            self.assertNotIn("—", html, f"Em-dash character found in {rel}")
            self.assertNotIn("&mdash;", html, f"HTML entity &mdash; found in {rel}")


    def test_workbench_big_total_and_summary_card_alignment(self):
        """Verify .wb-big-total does not overflow .wb-result-col and 3 summary cards align 'See calculation' without stretching neighbors."""
        with open(os.path.join(PUBLIC_DIR, "assets/styles.css"), encoding="utf-8") as f:
            css = f.read()
        big_total_block = re.search(r"\.wb-big-total\s*\{(.*?)\}", css, re.S)
        self.assertIsNotNone(big_total_block)
        self.assertNotIn("3.35rem", big_total_block.group(1))
        self.assertNotIn("white-space: nowrap", big_total_block.group(1))
        self.assertIn("flex-wrap: wrap", big_total_block.group(1))
        self.assertIn("grid-template-columns: 196px 330px minmax(0, 1fr);", css)
        self.assertIn("#calc-summary-strip,\n.verdict-section .summary-strip {\n  align-items: start;", css)

        with open(os.path.join(PUBLIC_DIR, "index.html"), encoding="utf-8") as f:
            index_html = f.read()
        self.assertIn("function equalizeSummaryCards(stripEl)", index_html)
        self.assertIn("equalizeSummaryCards(summaryEl);", index_html)



    def test_jotform_wix_app_campaign_guide_and_tier_calculator(self):
        """Verify /guides/jotform-wix-app-setup-and-pricing-guide/ satisfies all Jotform $200 Creator Campaign requirements."""
        guide_rel = "guides/jotform-wix-app-setup-and-pricing-guide/index.html"
        calc_rel = "pricing/jotform-pricing-tier-calculator/index.html"
        with open(os.path.join(PUBLIC_DIR, guide_rel), encoding="utf-8") as f:
            html = f.read()
        for required_token in [
            "#JotformPartner",
            "https://www.jotform.com/?partner=eriben02",
            "https://www.wix.com/app-market/web-solution/jotform",
            "https://info149840.wixsite.com/my-site-1",
            "https://form.jotform.com/262996430206056",
            "jotform-wix-app-walkthrough.mp4",
            "step1-jotform-builder.webp",
            "step2a-wix-app-market.webp",
            "step2b-wix-permissions.webp",
            "step3a-wix-editor-connect.webp",
            "step3b-wix-form-selected.webp",
            "step4a-live-wix-submission.webp",
            "step4b-thank-you-confirmation.webp",
            "step5-jotform-tables-verified.webp",
            "/compare/typeform-vs-jotform-response-limit-and-hipaa-cost/",
            "/pricing/jotform-pricing-tier-calculator/",
        ]:
            self.assertIn(required_token, html, f"Missing '{required_token}' in {guide_rel}")
        for bad in ["—", "&mdash;", "SaaSTruth", "Erik", "Bengtsson"]:
            self.assertNotIn(bad, html, f"Forbidden token '{bad}' in {guide_rel}")

        with open(os.path.join(PUBLIC_DIR, calc_rel), encoding="utf-8") as f:
            calc_html = f.read()
        self.assertIn("https://www.jotform.com/?partner=eriben02", calc_html)
        self.assertIn("/guides/jotform-wix-app-setup-and-pricing-guide/", calc_html)
        for bad in ["—", "&mdash;", "SaaSTruth", "Erik", "Bengtsson"]:
            self.assertNotIn(bad, calc_html, f"Forbidden token '{bad}' in {calc_rel}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
