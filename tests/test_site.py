"""Checks for the Chargeflow chargeback calculator and the shared workbench shell."""
import json
import os
import re
import subprocess
import unittest

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PUBLIC_DIR = os.path.join(BASE_DIR, "public")
REL = "chargeback-fee-and-recovery-calculator/index.html"
MIRROR = "pricing/stripe-shopify-chargeback-fee-and-chargeflow-roi-calculator/index.html"


class TestChargebackCalculator(unittest.TestCase):
    def test_page_copy_links_and_default_math(self):
        with open(os.path.join(PUBLIC_DIR, REL), encoding="utf-8") as f:
            html = f.read()
        self.assertIn(
            "<h1>Stripe, Shopify &amp; Paddle Chargeback Cost Calculator (2026): Dispute Fees, Manual Prep vs. Automated Recovery</h1>",
            html,
        )
        lead = re.search(r'<p class="lead">(.*?)</p>', html, re.S).group(1)
        self.assertEqual(lead.count(". "), 1)
        self.assertIn("chargeback", lead.lower())
        self.assertIn("dispute", lead.lower())
        self.assertIn('id="cb-orders"', html)
        self.assertIn('id="cb-aov"', html)
        self.assertIn('id="cb-rate"', html)
        self.assertIn('id="cb-processor"', html)
        self.assertIn('id="cb-summary"', html)
        self.assertIn("card-lowest", html)
        self.assertIn("best-card", html)
        self.assertIn("card-hidden", html)
        self.assertIn("Paddle ($20 dispute fee)", html)
        self.assertIn("Stripe ($15 + $15 counter fee)", html)
        self.assertIn("Shopify Payments ($15 fee)", html)
        self.assertIn("Annual Dispute Drain Breakdown", html)
        self.assertIn("Manual In-House Dispute Handling", html)
        self.assertIn("Chargeflow Pay-On-Performance", html)
        self.assertIn("Stripe Chargeback Protection (0.40% of GMV)", html)
        self.assertIn("Baseline (20% Win Rate)", html)
        self.assertIn("25% of recovered dollars", html)
        self.assertIn("Flat Volume Fee", html)
        self.assertIn("Lowest modeled cost", html)
        self.assertIn("planning benchmark", html)
        self.assertIn("Chargeblast", html)
        self.assertIn('id="full-table-details"', html)
        self.assertIn("Show calculation", html)
        self.assertIn("math-drawer", html)
        self.assertIn("https://www.chargeflow.io/", html)
        self.assertIn('data-vendor="chargeflow"', html)
        self.assertIn('data-track="vendor-cta"', html)
        self.assertIn("Shopify Protect", html)
        self.assertIn("0.40%", html)
        for bad in ["—", "&mdash;", "SaaSTruth", "Erik Bengtsson", "Erik", "Bengtsson"]:
            self.assertNotIn(bad, html, bad)

        fn = re.search(r"(function calcChargeback\(input\) \{.*?\n\})\n\nfunction renderChargeback", html, re.S)
        self.assertIsNotNone(fn)
        runner = fn.group(1) + """
        const c = calcChargeback({orders:2000, aov:120, rate:0.0065, fee:15});
        console.log(JSON.stringify(c));
        """
        res = subprocess.run(["node", "-e", runner], capture_output=True, text=True, check=True)
        c = json.loads(res.stdout)
        self.assertEqual(c["gmv"], 2880000)
        self.assertEqual(c["disputes"], 156)
        self.assertEqual(c["disputed"], 18720)
        self.assertEqual(c["fees"], 2340)
        self.assertEqual(c["manualLost"], 14976)
        self.assertEqual(c["manualGross"], 3744)
        self.assertEqual(c["manualOps"], 4680)
        self.assertEqual(c["manualNetAfterOps"], -936)
        self.assertEqual(c["unmanaged"], 21060)
        self.assertEqual(c["manualLoss"], 21996)
        self.assertEqual(c["recovered"], 12168)
        self.assertEqual(c["successFee"], 3042)
        self.assertEqual(c["netRecovered"], 9126)
        self.assertEqual(c["cfLost"], 6552)
        self.assertEqual(c["cfLoss"], 11934)
        self.assertEqual(c["savings"], 10062)
        self.assertEqual(c["radarFee"], 11520)
        self.assertEqual(c["nonFraudDisputes"], 47)
        self.assertEqual(c["fraudDisputes"], 109)
        self.assertEqual(c["nonFraudDisputed"], 5640)
        self.assertEqual(c["nonFraudRecovered"], 1128)
        self.assertEqual(c["nonFraudLost"], 4512)
        self.assertEqual(c["nonFraudFees"], 705)
        self.assertEqual(c["nonFraudOps"], 1410)
        self.assertEqual(c["nonFraudDrain"], 6627)
        self.assertEqual(c["radarLoss"], 18147)
        self.assertEqual(c["radar"], 18147)
        self.assertLess(c["cfLoss"], c["radar"])
        self.assertEqual(c["cfWin"], 0.65)

        with open(os.path.join(PUBLIC_DIR, MIRROR), encoding="utf-8") as f:
            mirror = f.read()
        self.assertIn('href="https://saasbill.io/pricing/stripe-shopify-chargeback-fee-and-chargeflow-roi-calculator/"', mirror)
        self.assertIn("function calcChargeback", mirror)

        with open(os.path.join(PUBLIC_DIR, "index.html"), encoding="utf-8") as f:
            home = f.read()
        self.assertIn("./chargeback-fee-and-recovery-calculator/", home)

        with open(os.path.join(PUBLIC_DIR, "exit/stripe-shopify-paddle-frozen-funds-alternatives/index.html"), encoding="utf-8") as f:
            holds = f.read()
        self.assertIn("chargeback-fee-and-recovery-calculator/", holds)

        with open(os.path.join(PUBLIC_DIR, "pricing/stripe-billing-0-7-percent-recurring-tax-calculator/index.html"), encoding="utf-8") as f:
            stripe = f.read()
        self.assertIn("chargeback-fee-and-recovery-calculator/", stripe)

        with open(os.path.join(BASE_DIR, "data", "affiliate_links.json"), encoding="utf-8") as f:
            affiliates = json.load(f)
        self.assertEqual(affiliates["chargeflow"]["destination_url"], "https://www.chargeflow.io/")

    def test_payment_calculators_include_live_dispute_line(self):
        pages = {
            "exit/stripe-shopify-paddle-frozen-funds-alternatives/index.html": "res-dispute-rate",
            "pricing/stripe-billing-0-7-percent-recurring-tax-calculator/index.html": "sb-dispute-rate",
            "faq/stripe-vs-paddle-true-cost/index.html": "sp-dispute-rate",
            "compare/gumroad-vs-whop-vs-lemon-squeezy-take-rate-calculator/index.html": "tr-cf-cta",
        }
        for rel, token in pages.items():
            with open(os.path.join(PUBLIC_DIR, rel), encoding="utf-8") as f:
                html = f.read()
            self.assertIn(token, html, rel)
            self.assertIn('data-vendor="chargeflow"', html, rel)
            self.assertIn("https://www.chargeflow.io/", html, rel)
            for bad in ["—", "&mdash;", "SaaSTruth", "Erik Bengtsson"]:
                self.assertNotIn(bad, html, rel)
        with open(os.path.join(PUBLIC_DIR, "index.html"), encoding="utf-8") as f:
            home = f.read()
        self.assertIn("Sticker Price: Base rate", home)
        self.assertIn("0.65% chargeback drain", home)
        self.assertIn("Hidden Cost Gap", home)
        self.assertNotIn("25% of $2k recovered", home)

        for rel in (
            "chargeback-fee-and-recovery-calculator/index.html",
            "pricing/stripe-shopify-chargeback-fee-and-chargeflow-roi-calculator/index.html",
        ):
            with open(os.path.join(PUBLIC_DIR, rel), encoding="utf-8") as f:
                page = f.read()
            grid = re.search(r'class="related-calc-grid">(.*?)</div>\s*<details', page, re.S)
            self.assertIsNotNone(grid, rel)
            cards = grid.group(1)
            self.assertNotIn("stripe-shopify-chargeback-fee-and-chargeflow-roi-calculator/", cards, rel)
            self.assertNotIn('href="../chargeback-fee-and-recovery-calculator/"', cards)
            self.assertNotIn('href="../../chargeback-fee-and-recovery-calculator/"', cards)
            self.assertIn("Frozen Funds", cards)
            self.assertIn("stripe-billing-0-7-percent-recurring-tax-calculator/", cards)
            self.assertIn("stripe-vs-paddle-true-cost/", cards)
            self.assertIn("Hidden Cost Gap: Lost sales", page)
            self.assertIn("Hidden Cost: Evidence prep", page)
            self.assertIn("Sticker Fee: Processor dispute fees", page)

        for rel in (
            "exit/stripe-shopify-paddle-frozen-funds-alternatives/index.html",
            "pricing/stripe-billing-0-7-percent-recurring-tax-calculator/index.html",
            "faq/stripe-vs-paddle-true-cost/index.html",
            "compare/gumroad-vs-whop-vs-lemon-squeezy-take-rate-calculator/index.html",
            "exit/paypal-180-day-permanent-limitation-fund-recovery/index.html",
        ):
            with open(os.path.join(PUBLIC_DIR, rel), encoding="utf-8") as f:
                page = f.read()
            grid = re.search(r'class="related-calc-grid">(.*?)</div>\s*<details', page, re.S)
            self.assertIsNotNone(grid, rel)
            cards = grid.group(1)
            self.assertIn("chargeback-fee-and-recovery-calculator/", cards, rel)
            self.assertNotIn("stripe-shopify-chargeback-fee-and-chargeflow-roi-calculator/", cards, rel)


class TestSharedWorkbenchShell(unittest.TestCase):
    QUEUED = [
        "compare/typeform-vs-jotform-response-limit-and-hipaa-cost/index.html",
        "compare/close-crm-vs-hubspot-sales-hub-5-to-20-reps/index.html",
        "pricing/stripe-billing-0-7-percent-recurring-tax-calculator/index.html",
        "pricing/docusign-envelope-allowance-and-api-overage-calculator/index.html",
        "pricing/gong-io-platform-fee-and-seat-minimum-calculator/index.html",
        "exit/paypal-180-day-permanent-limitation-fund-recovery/index.html",
        "faq/does-hubspot-charge-onboarding-fees-2026/index.html",
        "faq/intercom-fin-ai-cost-calculator/index.html",
        "faq/stripe-vs-paddle-true-cost/index.html",
    ]

    def test_queued_pages_use_the_shared_shell(self):
        for rel in self.QUEUED:
            with open(os.path.join(PUBLIC_DIR, rel), encoding="utf-8") as f:
                html = f.read()
            self.assertIn("editorial-hero editorial-hero-wrap", html, rel)
            self.assertIn("editorial-workbench", html, rel)
            self.assertIn(">Show calculation<", html, rel)
            self.assertIn("True Year-1 cost", html, rel)
            self.assertIn("Sticker Price", html, rel)
            self.assertIn("Hidden Cost Gap", html, rel)
            self.assertIn("data-label=", html, rel)
            self.assertNotIn("calc-card", html, rel)
            self.assertNotIn("—", html, rel)
            self.assertNotIn("&mdash;", html, rel)

    def test_chargeback_result_line_uses_the_shared_copy(self):
        for rel in (
            "chargeback-fee-and-recovery-calculator/index.html",
            "pricing/stripe-shopify-chargeback-fee-and-chargeflow-roi-calculator/index.html",
        ):
            with open(os.path.join(PUBLIC_DIR, rel), encoding="utf-8") as f:
                html = f.read()
            self.assertIn(">True Year-1 cost<", html, rel)
            self.assertIn("above advertised price.", html, rel)
            self.assertIn("saasbillResultLine", html, rel)
            self.assertNotIn("Unmanaged loss", html[html.find('id="cb-sub"'):html.find('id="cb-sub"') + 180], rel)


if __name__ == "__main__":
    unittest.main(verbosity=2)
