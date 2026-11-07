"""SSO tax calculator. Prices checked 2026-11-06."""
import json
import os
import re
import unittest

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REL = "compliance/okta-vs-workos-vs-1password-sso-tax-calculator/index.html"


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


class TestSsoTax(unittest.TestCase):
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
        self.assertIn("<h1>The B2B SaaS SSO tax calculator (2026)</h1>", html)
        self.assertIn("Lowest Year-1 cost:", html)
        self.assertNotIn("2x", html)
        self.assertNotIn("4x", html)
        self.assertNotIn("Best option", html)
        self.assertNotIn("Winner", html)
        self.assertNotIn("/go/1password", html)
        self.assertNotIn("sponsored", html)
        self.assertNotIn("Some links are affiliate links", html)
        self.assertIn("https://1password.com/pricing/business", html)
        self.assertIn("OIDC, not SAML", html)
        self.assertIn("does not offer a HIPAA BAA", html)
        self.assertIn("per connection", html.lower())
        self.assertIn("Accessed 2026-11-06", html)
        for url in (
            "https://www.okta.com/pricing/",
            "https://workos.com/pricing",
            "https://www.notion.com/pricing",
            "https://zoom.us/pricing",
            "https://github.com/pricing",
            "https://www.figma.com/pricing/",
            "https://slack.com/pricing",
        ):
            self.assertIn(url, html)
        self.assertIn("unknown", html)
        self.assertIn("mobile-cards", html)
        self.assertNotIn("<td>", html)
        self.assertNotIn("—", html)
        self.assertGreaterEqual(len(html.encode("utf-8")), 20 * 1024)
        home = read(os.path.join(BASE, "index.html"))
        self.assertEqual(home, read(os.path.join(BASE, "public", "index.html")))
        self.assertIn("./compliance/okta-vs-workos-vs-1password-sso-tax-calculator/", home)
        with open(os.path.join(BASE, "data", "publishing_queue.json"), encoding="utf-8") as handle:
            queue = json.load(handle)
        pipedrive = next(row for row in queue if row["priority"] == 14)
        self.assertEqual(pipedrive["status"], "published")
        self.assertEqual(pipedrive["published_at"], "2026-11-05")
        item = next(row for row in queue if row["priority"] == 15)
        self.assertEqual(item["status"], "published")
        self.assertEqual(item["published_at"], "2026-11-06")
        self.assertEqual(
            item["url"],
            "https://saasbill.io/compliance/okta-vs-workos-vs-1password-sso-tax-calculator/",
        )


if __name__ == "__main__":
    unittest.main()
