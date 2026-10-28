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
        self.assertIn("card-hidden", html)
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
        self.assertEqual(c["manualLoss"], 17316)
        self.assertEqual(c["recovered"], 9360)
        self.assertEqual(c["successFee"], 2340)
        self.assertEqual(c["netRecovered"], 7020)
        self.assertEqual(c["savings"], 3276)
        self.assertEqual(c["radar"], 11520)

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
