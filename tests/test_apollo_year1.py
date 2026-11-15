"""Apollo versus ZoomInfo versus Sales Navigator, Year 1."""
import json
import os
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REL = "pricing/apollo-vs-zoominfo-vs-sales-navigator-year-1-cost/index.html"
URL = "https://saasbill.io/pricing/apollo-vs-zoominfo-vs-sales-navigator-year-1-cost/"
LEAD = "This page compares Apollo, ZoomInfo, and LinkedIn Sales Navigator for one year."
TITLE = "Apollo vs ZoomInfo Year-1 – saasbill.io"


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


class TestApolloYear1(unittest.TestCase):
    def test_copy_sources_and_affiliate_line(self):
        html = read(os.path.join(ROOT, REL))
        public = read(os.path.join(ROOT, "public", REL))
        self.assertEqual(html, public)
        self.assertIn("<h1>What does Apollo cost in Year 1 versus ZoomInfo and Sales Navigator?</h1>", html)
        self.assertIn('<p class="lead">%s</p>' % LEAD, html)
        self.assertEqual(html.count(LEAD), 1)
        self.assertIn(TITLE, html)
        self.assertLessEqual(len(TITLE), 60)
        self.assertIn('id="shell-big">$4,740<', html)
        self.assertIn('id="shell-amt-base">$4,740<', html)
        self.assertIn('id="shell-amt-seats">$5,399.40<', html)
        self.assertIn('id="shell-amt-hidden">$22,495<', html)
        self.assertIn("wb-vbar-separate", html)
        self.assertIn("--wb-bar-share: 21.1%", html)
        self.assertIn("--wb-bar-share: 24%", html)
        self.assertIn("--wb-bar-share: 100%", html)
        self.assertIn("$659.40 less than Sales Navigator.", html)
        self.assertIn("$8,339.40", html)
        self.assertEqual(html.count("Some links are affiliate links. They never change the math."), 1)
        self.assertIn('href="../../go/apollo/" target="_blank" rel="sponsored nofollow noopener"', html)
        self.assertIn("https://www.apollo.io/pricing", html)
        self.assertIn("https://www.apollo.io/pricing/about-credits", html)
        self.assertIn("https://business.linkedin.com/sales-solutions/compare-plans", html)
        self.assertIn("https://www.zoominfo.com/legal/ltc_05_01_2025", html)
        self.assertNotIn("get.apollo.io", html)
        self.assertNotIn("2 credits", html)
        self.assertIn("A phone number is 8 credits.", html)
        self.assertIn("No email or phone credits", html)
        self.assertEqual(html.count("No email or phone credits"), 1)
        self.assertIn("class=\"table-wrap editorial-gap-table mobile-cards\"", html)
        self.assertNotIn("<td>", html)
        self.assertNotIn("\u2014", html)
        self.assertNotIn("Best option", html)
        self.assertNotIn("Winner", html)
        self.assertNotIn("SaaSTruth", html)
        self.assertIn("True Year-1 cost", html)
        self.assertIn("Show calculation", html)
        self.assertIn("2026-11-14", html)
        self.assertIn("unknown", html)
        self.assertIn("$149", html)
        self.assertEqual(html.count("$149"), 1)
        self.assertIn("$33,500", html)
        self.assertEqual(html.count("$33,500"), 1)

    def test_homepage_queue_and_sitemap(self):
        home = read(os.path.join(ROOT, "index.html"))
        self.assertEqual(home, read(os.path.join(ROOT, "public", "index.html")))
        cards = home[home.index('id="all-calculators"'):home.index('id="site-directory"')]
        self.assertIn("./pricing/apollo-vs-zoominfo-vs-sales-navigator-year-1-cost/", cards)
        directory = home[home.index('id="site-directory"'):]
        self.assertIn("./pricing/apollo-vs-zoominfo-vs-sales-navigator-year-1-cost/", directory)
        self.assertIn(URL, read(os.path.join(ROOT, "sitemap.xml")))
        self.assertEqual(read(os.path.join(ROOT, "sitemap.xml")), read(os.path.join(ROOT, "public", "sitemap.xml")))
        for name in ("llms.txt", "llms-full.txt"):
            self.assertIn(URL, read(os.path.join(ROOT, name)))
            self.assertEqual(read(os.path.join(ROOT, name)), read(os.path.join(ROOT, "public", name)))
        with open(os.path.join(ROOT, "data", "publishing_queue.json"), encoding="utf-8") as handle:
            queue = json.load(handle)
        item = next(row for row in queue if row["priority"] == 22)
        self.assertEqual(item["status"], "published")
        self.assertEqual(item["published_at"], "2026-11-14")
        self.assertEqual(item["slug"], "/pricing/apollo-vs-zoominfo-vs-sales-navigator-year-1-cost/")
        self.assertEqual(item["url"], URL)
        self.assertIn("$49", item["verification_note"])
        self.assertIn("$79", item["verification_note"])
        self.assertIn("8 credits", item["verification_note"])
        self.assertIn("/go/apollo", item["verification_note"])
        go = read(os.path.join(ROOT, "go", "apollo", "index.html"))
        self.assertEqual(go, read(os.path.join(ROOT, "public", "go", "apollo", "index.html")))
        self.assertIn("https://get.apollo.io/712wq4xq4p7v", go)
        self.assertIn('rel="sponsored nofollow"', go)


if __name__ == "__main__":
    unittest.main()
