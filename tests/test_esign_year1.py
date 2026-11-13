"""PandaDoc versus DocuSign versus Jotform Sign, Year 1."""
import json
import os
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REL = "pricing/pandadoc-vs-docusign-vs-jotform-sign-year-1-cost/index.html"
URL = "https://saasbill.io/pricing/pandadoc-vs-docusign-vs-jotform-sign-year-1-cost/"
LEAD = "DocuSign counts sent envelopes, Jotform Sign counts signed documents, and PandaDoc counts seats plus automation credits."
TITLE = "PandaDoc vs DocuSign vs Jotform – saasbill.io"


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


class TestEsignYear1(unittest.TestCase):
    def test_copy_sources_and_affiliate_line(self):
        html = read(os.path.join(ROOT, REL))
        public = read(os.path.join(ROOT, "public", REL))
        self.assertEqual(html, public)
        self.assertIn("<h1>What does PandaDoc cost versus DocuSign and Jotform Sign in Year 1?</h1>", html)
        self.assertIn('<p class="lead">%s</p>' % LEAD, html)
        self.assertEqual(html.count(LEAD), 1)
        self.assertIn(TITLE, html)
        self.assertLessEqual(len(TITLE), 60)
        self.assertIn('id="shell-big">$408<', html)
        self.assertIn('id="shell-amt-base">$684<', html)
        self.assertIn('id="shell-amt-seats">$900<', html)
        self.assertIn("wb-vbar-separate", html)
        self.assertIn("--wb-bar-share: 76%", html)
        self.assertIn("--wb-bar-share: 45.3%", html)
        self.assertIn("Lowest Year-1 cost: Jotform Sign, one account.", html)
        self.assertEqual(html.count("Paid partnership with Jotform (#JotformPartner)"), 1)
        self.assertEqual(html.count("Some links are affiliate links. They never change the math."), 1)
        self.assertIn('rel="sponsored nofollow noopener"', html)
        self.assertIn("https://www.jotform.com/pricing/?partner=saasbill", html)
        self.assertIn("https://www.pandadoc.com/pricing/", html)
        self.assertIn("https://www.docusign.com/blog/docusign-plans-and-pricing", html)
        self.assertIn("https://www.nodshake.com/guides/docusign-cost-per-envelope", html)
        self.assertNotIn('rel="sponsored nofollow noopener" href="https://www.pandadoc.com', html)
        self.assertIn("class=\"table-wrap editorial-gap-table mobile-cards\"", html)
        self.assertNotIn("<td>", html)
        self.assertNotIn("\u2014", html)
        self.assertNotIn("Best option", html)
        self.assertNotIn("SaaSTruth", html)
        self.assertIn("True Year-1 cost", html)
        self.assertIn("2026-11-13", html)
        self.assertIn("unknown", html)

    def test_homepage_queue_and_sitemap(self):
        home = read(os.path.join(ROOT, "index.html"))
        self.assertEqual(home, read(os.path.join(ROOT, "public", "index.html")))
        cards = home[home.index('id="all-calculators"'):home.index('id="site-directory"')]
        self.assertIn("./pricing/pandadoc-vs-docusign-vs-jotform-sign-year-1-cost/", cards)
        directory = home[home.index('id="site-directory"'):]
        self.assertIn("./pricing/pandadoc-vs-docusign-vs-jotform-sign-year-1-cost/", directory)
        self.assertIn(URL, read(os.path.join(ROOT, "sitemap.xml")))
        self.assertEqual(read(os.path.join(ROOT, "sitemap.xml")), read(os.path.join(ROOT, "public", "sitemap.xml")))
        for name in ("llms.txt", "llms-full.txt"):
            self.assertIn(URL, read(os.path.join(ROOT, name)))
            self.assertEqual(read(os.path.join(ROOT, name)), read(os.path.join(ROOT, "public", name)))
        with open(os.path.join(ROOT, "data", "publishing_queue.json"), encoding="utf-8") as handle:
            queue = json.load(handle)
        item = next(row for row in queue if row["priority"] == 21)
        self.assertEqual(item["status"], "published")
        self.assertEqual(item["published_at"], "2026-11-13")
        self.assertEqual(item["slug"], "/pricing/pandadoc-vs-docusign-vs-jotform-sign-year-1-cost/")
        self.assertEqual(item["url"], URL)
        self.assertIn("No PandaDoc affiliate link", item["verification_note"])
        self.assertIn("$3.60", item["verification_note"])
        self.assertIn("nodshake", item["verification_note"])


if __name__ == "__main__":
    unittest.main()
