"""Deel vs Rippling EOR. Prices checked 2026-11-08."""
import json
import os
import re
import unittest

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REL = "compare/deel-vs-rippling-eor-hidden-fx-and-offboarding-fees/index.html"


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


class TestEorCost(unittest.TestCase):
    def page(self):
        root = read(os.path.join(BASE, REL))
        public = read(os.path.join(BASE, "public", REL))
        self.assertEqual(root, public)
        return root

    def test_copy_sources_and_no_affiliate(self):
        html = self.page()
        title = re.search(r"<title>(.*?)</title>", html).group(1)
        self.assertLessEqual(len(title), 60, title)
        self.assertTrue(title.endswith(" – saasbill.io"), title)
        self.assertEqual(title, re.search(r'property="og:title" content="(.*?)"', html).group(1))
        self.assertIn("<h1>Deel vs. Rippling EOR cost (2026)</h1>", html)
        self.assertIn("$7,188", html)
        self.assertIn("$599", html)
        self.assertIn("not a ranking", html)
        self.assertIn("Not a deposit quote", html)
        self.assertIn("Fees excluded", html)
        self.assertIn("does not say per employee", html)
        self.assertNotIn("Lowest Year-1 cost", html)
        self.assertNotIn("Invoice currency, no fee", html)
        self.assertNotIn("unless you move this slider", html)
        self.assertNotIn("Best option", html)
        self.assertNotIn("Winner", html)
        self.assertNotIn("—", html)
        self.assertNotIn("&mdash;", html)
        self.assertNotIn("/go/deel", html)
        self.assertNotIn("/go/rippling", html)
        self.assertNotIn("sponsored", html)
        self.assertNotIn("Some links are affiliate links", html)
        self.assertIn("https://www.deel.com/pricing/", html)
        self.assertIn("https://www.rippling.com/pricing", html)
        self.assertIn("1 to 1.5", html)
        self.assertIn("Accessed 2026-11-08", html)
        self.assertIn("$499", html)
        self.assertIn("unknown", html)
        self.assertIn("mobile-cards", html)
        self.assertNotIn("<td>", html)
        self.assertNotIn("$0.00", html)
        self.assertGreaterEqual(len(html.encode("utf-8")), 20 * 1024)
        home = read(os.path.join(BASE, "index.html"))
        self.assertEqual(home, read(os.path.join(BASE, "public", "index.html")))
        self.assertIn("./compare/deel-vs-rippling-eor-hidden-fx-and-offboarding-fees/", home)
        with open(os.path.join(BASE, "data", "publishing_queue.json"), encoding="utf-8") as handle:
            queue = json.load(handle)
        item = next(row for row in queue if row["priority"] == 17)
        self.assertEqual(item["status"], "in_progress")
        self.assertNotIn("published_at", item)
        self.assertIn("unknown", item["verification_note"])
        with open(os.path.join(BASE, "data", "affiliate_links.json"), encoding="utf-8") as handle:
            affiliates = json.load(handle)
        self.assertTrue(affiliates["deel"]["status"].startswith("applied"))
        self.assertNotIn("rippling", affiliates)


if __name__ == "__main__":
    unittest.main()
