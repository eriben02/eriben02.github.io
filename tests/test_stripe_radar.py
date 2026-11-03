"""Stripe dispute fee and Radar calculator. Facts checked 2026-11-02."""
import json
import os
import re
import unittest

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REL = "pricing/stripe-radar-and-dispute-fee-calculator-2026/index.html"
URL = "https://saasbill.io/pricing/stripe-radar-and-dispute-fee-calculator-2026/"


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


class TestStripeRadarCalculator(unittest.TestCase):
    def page(self):
        root = read(os.path.join(BASE, REL))
        public = read(os.path.join(BASE, "public", REL))
        self.assertEqual(root, public)
        return root

    def test_title_sources_and_neutral_copy(self):
        html = self.page()
        title = re.search(r"<title>(.*?)</title>", html).group(1)
        self.assertLessEqual(len(title), 60, title)
        self.assertTrue(title.endswith(" – saasbill.io"), title)
        self.assertEqual(title, re.search(r'property="og:title" content="(.*?)"', html).group(1))
        self.assertIn("<h1>Stripe dispute and Radar cost</h1>", html)
        self.assertIn("Lowest Year-1 cost:", html)
        self.assertNotIn("Best option", html)
        self.assertNotIn("Winner", html)
        self.assertNotIn("answer first", html.lower())
        self.assertNotIn("chargeflow.io", html.lower())
        self.assertNotIn('data-vendor="chargeflow"', html)
        self.assertNotIn("—", html)
        self.assertNotIn("&mdash;", html)
        self.assertNotIn("SaaSTruth", html)
        self.assertNotIn("Erik", html)
        for source in (
            "https://stripe.com/pricing",
            "https://stripe.com/radar/pricing",
            "https://docs.stripe.com/disputes/measuring",
            "https://www.reddit.com/r/stripe/comments/1xj7m34/",
            "https://x.com/Darrentheadsguy/status/2117006751610421290",
        ):
            self.assertIn(source, html)
        self.assertIn("2 Nov 2026", html)
        self.assertIn("0.75%", html)
        self.assertIn("$15.00", html)
        self.assertIn("30%", html)
        self.assertIn("unknown", html)
        self.assertEqual(html.count("Some links are affiliate links. They never change the math."), 1)
        self.assertIn('rel="sponsored nofollow noopener"', html)
        self.assertIn("https://whop.com/sell?a=baggyprairieae", html)
        self.assertNotIn("Direct vendor link", html)
        self.assertIn("mobile-cards", html)
        self.assertNotIn("<td>", html)
        self.assertGreaterEqual(len(html.encode("utf-8")), 20 * 1024)

    def test_homepage_queue_and_sitemap(self):
        home = read(os.path.join(BASE, "index.html"))
        public_home = read(os.path.join(BASE, "public", "index.html"))
        self.assertEqual(home, public_home)
        self.assertIn("./pricing/stripe-radar-and-dispute-fee-calculator-2026/", home[home.index('id="all-calculators"'):])
        for name in ("sitemap.xml", "llms.txt", "llms-full.txt"):
            self.assertIn("/pricing/stripe-radar-and-dispute-fee-calculator-2026/", read(os.path.join(BASE, name)))
            self.assertIn("/pricing/stripe-radar-and-dispute-fee-calculator-2026/", read(os.path.join(BASE, "public", name)))
        with open(os.path.join(BASE, "data", "publishing_queue.json"), encoding="utf-8") as handle:
            queue = json.load(handle)
        item = next(row for row in queue if row["slug"] == "/pricing/stripe-radar-and-dispute-fee-calculator-2026/")
        self.assertEqual(item["status"], "published")
        self.assertEqual(item["primary_affiliate"], "whop")
        self.assertEqual(item["url"], URL)
        self.assertIn("2026-11-02", item["verification_note"])


if __name__ == "__main__":
    unittest.main()
