"""Jotform separate accounts versus Enterprise, Year 1."""
import json
import os
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REL = "pricing/jotform-multi-user-vs-enterprise-year-1-cost/index.html"
URL = "https://saasbill.io/pricing/jotform-multi-user-vs-enterprise-year-1-cost/"
LEAD = (
    "Standard plans run on shared servers with online support. "
    "Enterprise runs on a dedicated server, and the customer signs an agreement."
)
TITLE = "Jotform Year-1 cost, team of 3 to 4 – saasbill.io"


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


class TestJotformTeamYear1(unittest.TestCase):
    def test_copy_sources_and_affiliate_line(self):
        html = read(os.path.join(ROOT, REL))
        public = read(os.path.join(ROOT, "public", REL))
        self.assertEqual(html, public)
        self.assertIn("<h1>What does Jotform cost in Year 1 for a team of 3 to 4?</h1>", html)
        self.assertIn('<p class="lead">%s</p>' % LEAD, html)
        self.assertEqual(html.count(LEAD), 1)
        self.assertIn(TITLE, html)
        self.assertLessEqual(len(TITLE), 60)
        self.assertIn('id="shell-big">$4,752<', html)
        self.assertIn('id="shell-amt-base">$1,188<', html)
        self.assertIn('id="shell-amt-seats">$4,752<', html)
        self.assertIn('id="shell-amt-hidden">unknown<', html)
        self.assertIn("wb-vbar-separate", html)
        self.assertIn("--wb-bar-share: 25%", html)
        self.assertIn("--wb-bar-share: 100%", html)
        self.assertIn("--wb-bar-share: 0%", html)
        self.assertIn("Enterprise is cheaper only if the quote is below $4,752.", html)
        self.assertEqual(html.count("Paid partnership with Jotform (#JotformPartner)"), 1)
        self.assertEqual(html.count("Some links are affiliate links. They never change the math."), 1)
        self.assertIn('rel="sponsored nofollow noopener"', html)
        self.assertIn('href="/go/jotform"', html)
        self.assertNotIn("partner=saasbill", html)
        go = read(os.path.join(ROOT, "go", "jotform", "index.html"))
        self.assertIn("partner=saasbill", go)
        self.assertIn("https://www.jotform.com/pricing/", html)
        self.assertIn("https://www.jotform.com/teams/pricing/", html)
        self.assertIn("https://www.jotform.com/enterprise/faq/", html)
        self.assertIn("https://www.jotform.com/hipaa/", html)
        self.assertIn("https://www.jotform.com/answers/34688901-inquiry-about-multi-user-organizational-account-options", html)
        self.assertIn("https://www.jotform.com/answers/35726381-adding-another-user-to-license", html)
        self.assertIn("https://www.reddit.com/r/jotform/comments/1w0ud3g/why_cant_a_small_team_have_separate_individual/", html)
        self.assertIn("class=\"table-wrap editorial-gap-table mobile-cards\"", html)
        self.assertNotIn("<td>", html)
        self.assertNotIn("\u2014", html)
        self.assertNotIn("Best option", html)
        self.assertNotIn("SaaSTruth", html)
        self.assertIn("True Year-1 cost", html)
        self.assertIn("2026-11-15", html)
        self.assertIn("unknown", html)
        self.assertIn("Yes, I qualify", html)
        self.assertIn('id="jf-quote"', html)
        self.assertNotIn('value=""', html[html.find('id="jf-quote"') - 80:html.find('id="jf-quote"') + 220])

    def test_homepage_queue_and_sitemap(self):
        home = read(os.path.join(ROOT, "index.html"))
        self.assertEqual(home, read(os.path.join(ROOT, "public", "index.html")))
        cards = home[home.index('id="all-calculators"'):home.index('id="site-directory"')]
        self.assertIn("./pricing/jotform-multi-user-vs-enterprise-year-1-cost/", cards)
        directory = home[home.index('id="site-directory"'):]
        self.assertIn("./pricing/jotform-multi-user-vs-enterprise-year-1-cost/", directory)
        self.assertIn(URL, read(os.path.join(ROOT, "sitemap.xml")))
        self.assertIn("<lastmod>2026-11-15T00:00:00+00:00</lastmod>", read(os.path.join(ROOT, "sitemap.xml")))
        self.assertEqual(read(os.path.join(ROOT, "sitemap.xml")), read(os.path.join(ROOT, "public", "sitemap.xml")))
        for name in ("llms.txt", "llms-full.txt"):
            self.assertIn(URL, read(os.path.join(ROOT, name)))
            self.assertEqual(read(os.path.join(ROOT, name)), read(os.path.join(ROOT, "public", name)))
        with open(os.path.join(ROOT, "data", "publishing_queue.json"), encoding="utf-8") as handle:
            queue = json.load(handle)
        item = next(row for row in queue if row["priority"] == 23)
        self.assertEqual(item["status"], "published")
        self.assertEqual(item["published_at"], "2026-11-15")
        self.assertEqual(item["slug"], "/pricing/jotform-multi-user-vs-enterprise-year-1-cost/")
        self.assertEqual(item["url"], URL)
        self.assertIn("Paid partnership with Jotform (#JotformPartner)", item["verification_note"])
        self.assertIn("$4,752", item["verification_note"])
        self.assertIn("unknown", item["verification_note"].lower())


if __name__ == "__main__":
    unittest.main()
