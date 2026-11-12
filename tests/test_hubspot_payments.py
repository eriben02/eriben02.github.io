"""HubSpot payments versus a connected Stripe account."""
import json
import os
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REL = "pricing/hubspot-payments-vs-stripe-platform-fee-year-1-cost/index.html"
URL = "https://saasbill.io/pricing/hubspot-payments-vs-stripe-platform-fee-year-1-cost/"


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


class TestHubspotPayments(unittest.TestCase):
    def test_copy_sources_and_no_affiliate(self):
        html = read(os.path.join(ROOT, REL))
        public = read(os.path.join(ROOT, "public", REL))
        self.assertEqual(html, public)
        self.assertIn("<h1>What do HubSpot Payments fees cost versus connecting Stripe?</h1>", html)
        self.assertIn('<p class="lead">This page compares HubSpot payments with Stripe connected to HubSpot.</p>', html)
        self.assertEqual(html.count("This page compares HubSpot payments with Stripe connected to HubSpot."), 1)
        self.assertIn("HubSpot Payments vs Stripe fees – saasbill.io", html)
        self.assertLessEqual(len("HubSpot Payments vs Stripe fees – saasbill.io"), 60)
        self.assertIn('id="shell-big">$4,080<', html)
        self.assertIn('id="shell-amt-seats">$4,740<', html)
        self.assertIn("Lower Year-1 fee: HubSpot payments, $4,080.", html)
        self.assertEqual(html.count("The 0.75% platform fee applies on top of Stripe's own fees. On bank debits, that 0.75% is uncapped."), 1)
        self.assertEqual(html.count("Who qualifies is not stated"), 1)
        self.assertIn("https://knowledge.hubspot.com/payment-processing/payments-frequently-asked-questions", html)
        self.assertIn("https://stripe.com/us/pricing", html)
        self.assertIn("2.9% + $0.30", html)
        self.assertIn("class=\"table-wrap editorial-gap-table mobile-cards\"", html)
        self.assertNotIn("<td>", html)
        self.assertNotIn("/go/", html)
        self.assertNotIn("sponsored", html)
        self.assertNotIn("\u2014", html)
        self.assertNotIn("Best option", html)
        self.assertNotIn("Some links are affiliate links", html)
        self.assertIn("True Year-1 cost", html)

    def test_homepage_queue_and_sitemap(self):
        home = read(os.path.join(ROOT, "index.html"))
        self.assertEqual(home, read(os.path.join(ROOT, "public", "index.html")))
        cards = home[home.index('id="all-calculators"'):]
        self.assertIn("./pricing/hubspot-payments-vs-stripe-platform-fee-year-1-cost/", cards)
        directory = home[home.index('id="site-directory"'):]
        self.assertIn("./pricing/hubspot-payments-vs-stripe-platform-fee-year-1-cost/", directory)
        self.assertIn(URL, read(os.path.join(ROOT, "sitemap.xml")))
        self.assertIn(URL, read(os.path.join(ROOT, "public", "sitemap.xml")))
        with open(os.path.join(ROOT, "data", "publishing_queue.json"), encoding="utf-8") as handle:
            queue = json.load(handle)
        item = next(row for row in queue if row["priority"] == 20)
        self.assertEqual(item["status"], "published")
        self.assertEqual(item["published_at"], "2026-11-12")
        self.assertEqual(item["slug"], "/pricing/hubspot-payments-vs-stripe-platform-fee-year-1-cost/")
        self.assertIn("No HubSpot affiliate link", item["verification_note"])
        self.assertIn("0.75%", item["verification_note"])


if __name__ == "__main__":
    unittest.main()
