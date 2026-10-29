"""Playwright check that every sitemap URL shares the editorial calculator shell."""
import os
import re
import threading
import unittest
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

from playwright.sync_api import sync_playwright

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CHROME = "/opt/google/chrome/chrome"


class TestVisualConsistency(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.path.exists(CHROME):
            raise unittest.SkipTest("Chrome is not available for the consistency check")
        handler = partial(SimpleHTTPRequestHandler, directory=ROOT)
        cls.httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        cls.port = cls.httpd.server_address[1]
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()
        with open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8") as f:
            xml = f.read()
        cls.paths = []
        for loc in re.findall(r"<loc>(https://saasbill\.io[^<]*)</loc>", xml):
            path = loc.replace("https://saasbill.io", "") or "/"
            cls.paths.append(path)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "httpd"):
            cls.httpd.shutdown()

    def test_every_sitemap_url_matches_the_shell(self):
        problems = []
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox"])
            page = browser.new_page(viewport={"width": 390, "height": 900})
            for path in self.paths:
                page.goto("http://127.0.0.1:%s%s" % (self.port, path), wait_until="networkidle", timeout=30000)
                info = page.evaluate(
                    """() => {
                      const h1 = document.querySelector('h1');
                      const cs = h1 ? getComputedStyle(h1) : null;
                      const hero = h1 ? h1.closest('section') : null;
                      const slider = document.querySelector('input[type=range]');
                      const doc = document.documentElement;
                      return {
                        h1: !!h1,
                        whiteSpace: cs ? cs.whiteSpace : '',
                        heroClass: hero ? hero.className : '',
                        h1Overflow: h1 ? h1.scrollWidth - h1.clientWidth : 0,
                        pageOverflow: doc.scrollWidth - doc.clientWidth,
                        sliderH: slider ? getComputedStyle(slider).height : '',
                        hasRange: !!slider,
                        show: document.body.innerText.indexOf('Show calculation') !== -1,
                        quote: document.body.innerText.indexOf('True Year-1 cost') !== -1,
                        calcCard: !!document.querySelector('.calc-card'),
                        styleTag: !!document.querySelector('style')
                      };
                    }"""
                )
                flags = []
                if not info["h1"]:
                    flags.append("missing h1")
                if info["pageOverflow"] > 2:
                    flags.append("horizontal overflow %s" % info["pageOverflow"])
                if path == "/":
                    if "editorial-hero" not in info["heroClass"]:
                        flags.append("homepage hero")
                else:
                    if "editorial-hero-wrap" not in info["heroClass"]:
                        flags.append("deep hero " + info["heroClass"])
                    if info["whiteSpace"] == "nowrap" or info["h1Overflow"] > 4:
                        flags.append("h1 clipped")
                if info["hasRange"]:
                    if info["sliderH"] != "8px":
                        flags.append("slider " + info["sliderH"])
                    if not info["show"]:
                        flags.append("missing Show calculation")
                    if not info["quote"]:
                        flags.append("missing True Year-1 cost")
                if info["calcCard"]:
                    flags.append("calc-card")
                if info["styleTag"]:
                    flags.append("inline style")
                if flags:
                    problems.append(path + ": " + ", ".join(flags))
            browser.close()
        self.assertEqual(problems, [], "\n".join(problems))


if __name__ == "__main__":
    unittest.main()
