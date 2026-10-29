"""Fail the suite if GitHub Pages would publish a placeholder homepage."""
import os
import re
import sys
import tempfile
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from deploy_guard import (  # noqa: E402
    MIN_HOMEPAGE_BYTES,
    MIN_PAGE_BYTES,
    DeployGuardError,
    check_html,
    check_published_file,
)


def published_path(url_path):
    if url_path in ("", "/"):
        return os.path.join(ROOT, "index.html")
    return os.path.join(ROOT, url_path.strip("/"), "index.html")


class TestDeployGuard(unittest.TestCase):
    def test_published_homepage_is_a_real_calculator(self):
        path = os.path.join(ROOT, "index.html")
        size = check_published_file(path, homepage=True)
        self.assertGreaterEqual(size, MIN_HOMEPAGE_BYTES)
        with open(path, encoding="utf-8") as handle:
            html = handle.read()
        self.assertIn('id="all-calculators"', html)
        self.assertIn("editorial-workbench", html)
        self.assertIn("workbench-grid", html)
        self.assertNotIn("placeholder", html.lower())

    def test_every_sitemap_page_is_present_and_not_a_placeholder(self):
        sitemap = os.path.join(ROOT, "sitemap.xml")
        with open(sitemap, encoding="utf-8") as handle:
            xml = handle.read()
        locs = re.findall(r"<loc>https://saasbill\.io([^<]*)</loc>", xml)
        self.assertGreaterEqual(len(locs), 30)
        for url_path in locs:
            path = published_path(url_path)
            homepage = url_path in ("", "/")
            size = check_published_file(path, homepage=homepage)
            floor = MIN_HOMEPAGE_BYTES if homepage else MIN_PAGE_BYTES
            self.assertGreaterEqual(size, floor, path)

    def test_build_output_homepage_matches_the_published_file(self):
        """Generators write public/index.html. Pages serves the root copy."""
        with open(os.path.join(ROOT, "index.html"), encoding="utf-8") as handle:
            root_html = handle.read()
        with open(os.path.join(ROOT, "public", "index.html"), encoding="utf-8") as handle:
            public_html = handle.read()
        check_html(root_html, "index.html", homepage=True)
        check_html(public_html, "public/index.html", homepage=True)
        self.assertEqual(root_html, public_html)

    def test_guard_rejects_a_placeholder_homepage(self):
        stub = "<html>PLACEHOLDER</html>"
        with self.assertRaises(DeployGuardError):
            check_html(stub, "index.html", homepage=True)
        with self.assertRaises(DeployGuardError):
            check_html("x" * (MIN_HOMEPAGE_BYTES + 10), "index.html", homepage=True)
        big = "x" * (MIN_HOMEPAGE_BYTES + 10)
        big += 'id="all-calculators" editorial-workbench workbench-grid'
        big += " placeholder "
        with self.assertRaises(DeployGuardError):
            check_html(big, "index.html", homepage=True)

    def test_guard_rejects_a_tiny_inner_page(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "index.html")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write("ok")
            with self.assertRaises(DeployGuardError):
                check_published_file(path, homepage=False)


if __name__ == "__main__":
    unittest.main()
