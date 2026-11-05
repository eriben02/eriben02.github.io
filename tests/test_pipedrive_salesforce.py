"""Pipedrive vs Salesforce Starter and Pro Suite. Facts checked 2026-11-05."""
import json
import os
import re
import unittest

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REL = "compare/pipedrive-vs-salesforce-starter-and-pro-suite-cost/index.html"


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


class TestPipedriveSalesforce(unittest.TestCase):
    def page(self):
        root = read(os.path.join(BASE, REL))
        public = read(os.path.join(BASE, "public", REL))
        self.assertEqual(root, public)
        return root

    def test_copy_sources_and_affiliate(self):
        html = self.page()
        title = re.search(r"<title>(.*?)</title>", html).group(1)
        self.assertLessEqual(len(title), 60, title)
        self.assertEqual(title, "Pipedrive vs Salesforce Year-1 – saasbill.io")
        self.assertEqual(title, re.search(r'property="og:title" content="(.*?)"', html).group(1))
        self.assertIn("<h1>Pipedrive vs Salesforce Year-1 cost</h1>", html)
        self.assertIn("Lowest Year-1 cost:", html)
        self.assertNotIn("Best option", html)
        self.assertNotIn("Winner", html)
        self.assertNotIn("answer first", html.lower())
        self.assertNotIn("SaaSTruth", html)
        self.assertNotIn("Erik", html)
        self.assertNotIn("—", html)
        self.assertNotIn("&mdash;", html)
        self.assertIn("https://www.pipedrive.com/en/pricing", html)
        self.assertIn("https://support.pipedrive.com/en/article/new-pipedrive-plans", html)
        self.assertIn("https://www.salesforce.com/editions-pricing/sales-cloud/", html)
        self.assertIn("https://www.salesforce.com/sales/pricing/", html)
        self.assertIn("5 Nov 2026", html)
        self.assertIn("src-cluster", html)
        self.assertIn('href="../../go/pipedrive/"', html)
        self.assertIn('rel="sponsored nofollow noopener"', html)
        self.assertNotIn("salesforce.com\" class=\"btn", html)
        self.assertEqual(html.count("Some links are affiliate links. They never change the math."), 1)
        self.assertIn("unknown", html)
        self.assertIn("$1,500", html)
        self.assertIn("$2,340", html)
        self.assertIn("$6,000", html)
        self.assertIn("$7,500", html)
        self.assertIn("mobile-cards", html)
        self.assertNotIn("<td>", html)
        self.assertNotIn("<style", html.lower())
        self.assertGreaterEqual(len(html.encode("utf-8")), 20 * 1024)
        home = read(os.path.join(BASE, "index.html"))
        self.assertEqual(home, read(os.path.join(BASE, "public", "index.html")))
        self.assertIn("./compare/pipedrive-vs-salesforce-starter-and-pro-suite-cost/", home)
        with open(os.path.join(BASE, "data", "publishing_queue.json"), encoding="utf-8") as handle:
            queue = json.load(handle)
        item = next(row for row in queue if row["priority"] == 14)
        self.assertEqual(item["status"], "in_progress")
        self.assertNotIn("published_at", item)
        self.assertEqual(item["primary_affiliate"], "pipedrive")


if __name__ == "__main__":
    unittest.main()
