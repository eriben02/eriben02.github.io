"""SOC 2 platform plus CPA auditor calculator. Prices checked 2026-11-07."""
import json
import os
import re
import unittest

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REL = "compliance/vanta-vs-drata-vs-comp-ai-soc2-negotiation-benchmarks/index.html"


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


class TestSoc2Cost(unittest.TestCase):
    def page(self):
        root = read(os.path.join(BASE, REL))
        public = read(os.path.join(BASE, "public", REL))
        self.assertEqual(root, public)
        return root

    def test_copy_sources_and_affiliate(self):
        html = self.page()
        title = re.search(r"<title>(.*?)</title>", html).group(1)
        self.assertLessEqual(len(title), 60, title)
        self.assertTrue(title.endswith(" – saasbill.io"), title)
        self.assertEqual(title, re.search(r'property="og:title" content="(.*?)"', html).group(1))
        self.assertIn("<h1>Vanta, Drata, and Comp AI SOC 2 cost (2026)</h1>", html)
        self.assertIn("Lowest Year-1 cost:", html)
        self.assertNotIn("Best option", html)
        self.assertNotIn("Winner", html)
        self.assertNotIn("—", html)
        self.assertNotIn("&mdash;", html)
        self.assertNotIn("partnerstack.com", html)
        self.assertIn('href="../../go/vanta/"', html)
        self.assertIn('href="../../go/drata/"', html)
        self.assertIn('rel="sponsored nofollow noopener"', html)
        self.assertEqual(html.count("Some links are affiliate links. They never change the math."), 1)
        self.assertIn("https://www.trycomp.ai/pricing", html)
        comp = re.search(r'<a class="src-link" href="https://www.trycomp.ai/pricing"[^>]*>', html)
        self.assertIsNotNone(comp)
        self.assertNotIn("sponsored", comp.group(0))
        self.assertIn("Accessed 2026-11-07", html)
        for url in (
            "https://aws.amazon.com/marketplace/pp/prodview-5ophamrbfxt44",
            "https://www.vanta.com/pricing",
            "https://www.vanta.com/collection/soc-2/soc-2-audit-cost",
            "https://drata.com/plans",
            "https://aws.amazon.com/marketplace/pp/prodview-3xw4sjqv2pb22",
        ):
            self.assertIn(url, html)
        self.assertIn("unknown", html)
        self.assertIn("non-cancellable", html)
        self.assertIn("does not issue the SOC 2 report", html)
        self.assertIn("1 to 50 FTE", html)
        self.assertIn("before add-ons", html)
        self.assertIn("Not an all-in quote", html)
        self.assertIn("includes Trust Center Advanced and Questionnaire Automation Advanced", html)
        self.assertIn('id="soc-extras"', html)
        self.assertIn("not evidence that tools do not recur", html)
        self.assertNotIn("reddit.com", html)
        self.assertNotIn("r/soc2", html)
        self.assertIn("mobile-cards", html)
        self.assertNotIn("<td>", html)
        self.assertNotIn("$0.00", html)
        self.assertGreaterEqual(len(html.encode("utf-8")), 20 * 1024)
        home = read(os.path.join(BASE, "index.html"))
        self.assertEqual(home, read(os.path.join(BASE, "public", "index.html")))
        self.assertIn("./compliance/vanta-vs-drata-vs-comp-ai-soc2-negotiation-benchmarks/", home)
        with open(os.path.join(BASE, "data", "publishing_queue.json"), encoding="utf-8") as handle:
            queue = json.load(handle)
        item = next(row for row in queue if row["priority"] == 16)
        self.assertEqual(item["status"], "published")
        self.assertEqual(item["published_at"], "2026-11-07")
        self.assertEqual(
            item["url"],
            "https://saasbill.io/compliance/vanta-vs-drata-vs-comp-ai-soc2-negotiation-benchmarks/",
        )
        self.assertEqual(item["primary_affiliate"], "vanta")
        with open(os.path.join(BASE, "data", "affiliate_links.json"), encoding="utf-8") as handle:
            affiliates = json.load(handle)
        self.assertNotIn("go_url", affiliates["vanta"])
        self.assertNotIn("go_url", affiliates["drata"])
        self.assertIn("pending", affiliates["vanta"]["status"])
        self.assertIn("pending", affiliates["drata"]["status"])
        self.assertEqual(affiliates["vanta"]["destination_url"], "https://www.vanta.com/pricing")
        self.assertEqual(affiliates["drata"]["destination_url"], "https://drata.com/")
        for slug, target in (("vanta", "https://www.vanta.com/pricing"), ("drata", "https://drata.com/")):
            page = read(os.path.join(BASE, "go", slug, "index.html"))
            self.assertEqual(page, read(os.path.join(BASE, "public", "go", slug, "index.html")))
            self.assertIn(target, page)
            self.assertNotIn("partnerstack", page.lower())


if __name__ == "__main__":
    unittest.main()
