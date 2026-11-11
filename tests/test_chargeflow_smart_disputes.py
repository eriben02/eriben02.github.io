"""Chargeflow vs Stripe Smart Disputes Year-1 page."""
import json
import os
import re
import unittest

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REL = "pricing/chargeflow-vs-stripe-smart-disputes-year-1-cost/index.html"
URL = "https://saasbill.io/pricing/chargeflow-vs-stripe-smart-disputes-year-1-cost/"


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


class TestChargeflowSmartDisputes(unittest.TestCase):
    def page(self):
        root = read(os.path.join(BASE, REL))
        public = read(os.path.join(BASE, "public", REL))
        self.assertEqual(root, public)
        return root

    def test_copy_sources_and_no_affiliate(self):
        html = self.page()
        title = re.search(r"<title>(.*?)</title>", html).group(1)
        self.assertLessEqual(len(title), 60, title)
        self.assertIn("Chargeflow vs Stripe Smart Disputes", title)
        self.assertIn("What does Chargeflow cost versus Stripe Smart Disputes in Year 1?", html)
        self.assertIn("True Year-1 cost", html)
        self.assertIn('id="shell-big">$2,700<', html)
        self.assertIn('id="shell-amt-seats">$3,600<', html)
        self.assertIn('id="shell-amt-hidden">$3,300<', html)
        self.assertIn("assumption", html)
        self.assertIn("Chargeback Protection is not listed", html)
        self.assertNotIn("0.4%", html)
        self.assertNotIn("/go/", html)
        self.assertNotIn("sponsored", html)
        self.assertNotIn("Some links are affiliate links", html)
        self.assertNotIn("Winner", html)
        self.assertNotIn("Best option", html)
        self.assertNotIn("\u2014", html)
        self.assertIn("https://stripe.com/us/pricing", html)
        self.assertIn("https://www.chargeflow.io/pricing", html)
        self.assertIn("mobile-cards", html)
        self.assertNotIn("<td>", html)
        self.assertIn("data-label=", html)
        self.assertIn("2026-11-11", html)
        home = read(os.path.join(BASE, "index.html"))
        self.assertEqual(home, read(os.path.join(BASE, "public", "index.html")))
        self.assertIn("./pricing/chargeflow-vs-stripe-smart-disputes-year-1-cost/", home)
        self.assertIn(URL, read(os.path.join(BASE, "sitemap.xml")))
        self.assertEqual(read(os.path.join(BASE, "sitemap.xml")), read(os.path.join(BASE, "public", "sitemap.xml")))
        with open(os.path.join(BASE, "data", "publishing_queue.json"), encoding="utf-8") as handle:
            queue = json.load(handle)
        item = next(row for row in queue if row["priority"] == 19)
        self.assertEqual(item["status"], "published")
        self.assertEqual(item["published_at"], "2026-11-11")
        self.assertEqual(item["slug"], "/pricing/chargeflow-vs-stripe-smart-disputes-year-1-cost/")
        self.assertNotIn("0.4%", item["verification_note"])


if __name__ == "__main__":
    unittest.main()
