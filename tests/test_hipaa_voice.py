"""AI voice HIPAA BAA matrix. Prices checked 2026-11-09."""
import json
import os
import re
import unittest

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REL = "compliance/ai-voice-and-transcription-hipaa-baa-matrix-2026/index.html"


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


class TestHipaaVoice(unittest.TestCase):
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
        self.assertIn("<h1>AI voice and transcription HIPAA BAA matrix (2026)</h1>", html)
        self.assertIn("A BAA is necessary but not sufficient.", html)
        self.assertIn("$14.16", html)
        self.assertIn("$35", html)
        self.assertNotIn("$99.99", html)
        quote = re.search(r'id="shell-quote">([^<]*)<', html).group(1)
        self.assertEqual(quote, "Published seat list prices, not a full cost")
        self.assertNotIn("True Year-1 cost", quote)
        self.assertNotIn("paid add-on", html)
        self.assertIn("signable in minutes without a sales call", html)
        self.assertNotIn("signed in the dashboard", html)
        self.assertIn("5 seats, annual billing, BAA required. Not a ranking.", html)
        self.assertIn('seats === 1 ? "seat"', html)
        cta = re.search(r'<a id="shell-cta"[^>]*>', html)
        self.assertIsNotNone(cta)
        self.assertIn('href="#hv-matrix"', cta.group(0))
        self.assertNotIn("vendor-cta", cta.group(0))
        self.assertNotIn("data-vendor", cta.group(0))
        self.assertIn("Private Storage", html)
        self.assertIn("Accessed 2026-11-09", html)
        self.assertIn("https://www.granola.ai/pricing", html)
        self.assertIn("https://www.fathom.ai/pricing", html)
        self.assertIn("https://zoom.us/pricing/healthcare", html)
        self.assertNotIn("Lowest Year-1 cost", html)
        self.assertNotIn("Best option", html)
        self.assertNotIn("Winner", html)
        self.assertNotIn("—", html)
        self.assertNotIn("/go/", html)
        self.assertNotIn("sponsored", html)
        self.assertNotIn("JotformPartner", html)
        self.assertNotIn("partner=", html)
        self.assertNotIn("Some links are affiliate links", html)
        self.assertIn("unknown", html)
        self.assertIn("mobile-cards", html)
        self.assertNotIn("<td>", html)
        self.assertNotIn("$0.00", html)
        self.assertGreaterEqual(len(html.encode("utf-8")), 20 * 1024)
        home = read(os.path.join(BASE, "index.html"))
        self.assertEqual(home, read(os.path.join(BASE, "public", "index.html")))
        self.assertIn("./compliance/ai-voice-and-transcription-hipaa-baa-matrix-2026/", home)
        with open(os.path.join(BASE, "data", "publishing_queue.json"), encoding="utf-8") as handle:
            queue = json.load(handle)
        item = next(row for row in queue if row["priority"] == 18)
        self.assertEqual(item["status"], "in_progress")
        self.assertNotIn("published_at", item)
        self.assertIn("unknown", item["verification_note"])


if __name__ == "__main__":
    unittest.main()
