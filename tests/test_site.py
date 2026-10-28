"""Checks for the Chargeflow chargeback calculator."""
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
            "<h1>Stripe &amp; Shopify Chargeback Cost Calculator (2026): Dispute Fees, Lost Revenue &amp; Chargeflow ROI</h1>",
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
        self.assertIn("Stripe ($15 dispute fee + $15 counter fee)", html)
        self.assertIn("Shopify Payments ($15 dispute fee)", html)
        self.assertIn("Manual In-House Dispute Handling", html)
        self.assertIn("Chargeflow Pay-On-Performance", html)
        self.assertIn("Stripe Chargeback Protection (0.40% of GMV)", html)
        self.assertIn("Baseline (20% Win Rate)", html)
        self.assertIn("Highest Net Recovery", html)
        self.assertIn("Flat Volume Fee", html)
        self.assertIn("Recover $9,126/yr net with Chargeflow (save $10,062/yr vs manual)", html)
        self.assertIn('id="full-table-details"', html)
        self.assertIn("See exactly how we calculated this", html)
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
        self.assertEqual(c["radar"], 11520)
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
