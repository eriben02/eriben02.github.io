"""Structure checks for the /ai-act/ test section."""
import os
import re
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PUBLIC = os.path.join(ROOT, "public")
MIN_BYTES = 20 * 1024

PAGES = [
    "ai-act/index.html",
    "ai-act/article-50-deployer-checklist/index.html",
    "ai-act/deepfake-labelling-patterns/index.html",
    "ai-act/c2pa-watermarking-tools-compared/index.html",
    "ai-act/etsi-ts-104-275-explained/index.html",
]

AFFILIATE_MARKERS = (
    'rel="sponsored',
    "/go/",
    "refer.close.com",
    "get.apollo.io",
    "partner=",
    "aff.trypipedrive.com",
    "whop.com/sell?a=",
    "footer-disclosure",
    "Some links are affiliate links",
)

SOURCE_URLS = (
    "https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-50",
    "https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/when-does-enforcement-start",
    "https://digital-strategy.ec.europa.eu/en/policies/eu-icons-labelling-ai-generated-content",
    "https://www.etsi.org/deliver/etsi_TS/104200_104299/104275/01.01.01_60/ts_104275v010101p.pdf",
)


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


class TestAiActSection(unittest.TestCase):
    def test_pages_are_published_and_neutral(self):
        for rel in PAGES:
            public = os.path.join(PUBLIC, rel)
            root = os.path.join(ROOT, rel)
            self.assertTrue(os.path.isfile(public), rel)
            self.assertTrue(os.path.isfile(root), rel)
            html = read(public)
            self.assertEqual(html, read(root), rel)
            self.assertGreaterEqual(len(html.encode("utf-8")), MIN_BYTES, rel)
            self.assertNotIn("placeholder", html.lower(), rel)
            self.assertNotIn("—", html, rel)
            self.assertNotIn("&mdash;", html, rel)
            self.assertIn('class="hero editorial-hero editorial-hero-wrap"', html, rel)
            self.assertIn("<h1>", html, rel)
            self.assertIn("Not legal advice", html, rel)
            self.assertIn("Accessed 30 Oct 2026.", html, rel)
            self.assertIn("<details", html, rel)
            self.assertIn('id="related-ai-act-heading"', html, rel)
            self.assertNotIn("Related Year-1 True-Cost Calculators", html, rel)
            self.assertNotIn("<form", html.lower(), rel)
            self.assertNotIn('type="email"', html, rel)
            for marker in AFFILIATE_MARKERS:
                self.assertNotIn(marker, html, "%s contains %s" % (rel, marker))
            self.assertIsNone(re.search(r'<a\b[^>]*data-track="vendor-cta"', html), rel)
            nav = re.search(r'<nav class="nav-links".*?</nav>', html, re.S).group(0)
            self.assertNotIn("/ai-act/", nav, rel)

    def test_sources_and_offer(self):
        index = read(os.path.join(PUBLIC, "ai-act/index.html"))
        patterns = read(os.path.join(PUBLIC, "ai-act/deepfake-labelling-patterns/index.html"))
        tools = read(os.path.join(PUBLIC, "ai-act/c2pa-watermarking-tools-compared/index.html"))
        etsi = read(os.path.join(PUBLIC, "ai-act/etsi-ts-104-275-explained/index.html"))
        for url in SOURCE_URLS:
            self.assertIn(url, index + patterns + tools + etsi, url)
        self.assertIn("Free checklist (PDF) coming soon", index)
        self.assertIn("Free checklist (PDF) coming soon", read(os.path.join(PUBLIC, "ai-act/article-50-deployer-checklist/index.html")))
        self.assertIn("LABEL_AI_black.svg", patterns)
        self.assertIn("https://digital-strategy.ec.europa.eu/en/policies/eu-icons-labelling-ai-generated-content", patterns)
        self.assertIn("$1,000/month", tools)
        self.assertIn("$1,450/month", tools)
        self.assertIn("29 Sep 2026", etsi)
        self.assertIn("29 Oct 2026", etsi)
        self.assertIn("2 August 2026", index)
        self.assertIn("2 Dec 2026", index)

    def test_sitemap_and_llms_list_the_section(self):
        sitemap = read(os.path.join(PUBLIC, "sitemap.xml"))
        llms = read(os.path.join(PUBLIC, "llms.txt"))
        for path in (
            "https://saasbill.io/ai-act/",
            "https://saasbill.io/ai-act/article-50-deployer-checklist/",
            "https://saasbill.io/ai-act/deepfake-labelling-patterns/",
            "https://saasbill.io/ai-act/c2pa-watermarking-tools-compared/",
            "https://saasbill.io/ai-act/etsi-ts-104-275-explained/",
        ):
            self.assertIn(path, sitemap)
            self.assertIn(path, llms)
        self.assertIn("AI Act Article 50 (test section)", llms)
        self.assertIn("Accessed 30 Oct 2026", llms)
        home = read(os.path.join(PUBLIC, "index.html"))
        self.assertIn("Some links are affiliate links. They never change the math.", home)

    def test_design_principle_is_not_visible_copy(self):
        """'Answer first' and 'explanation on demand' stay off every published page."""
        forbidden = ("answer first", "explanation on demand")
        pages = []
        for base in (ROOT, PUBLIC):
            for dirpath, dirnames, filenames in os.walk(base):
                dirnames[:] = [name for name in dirnames if name not in (".git", "node_modules", "saastruth", "scripts", "tests")]
                for name in filenames:
                    if name.endswith(".html"):
                        pages.append(os.path.join(dirpath, name))
        self.assertGreaterEqual(len(pages), 30)
        for path in pages:
            html = read(path)
            html = re.sub(r"<script\b[^>]*>.*?</script>", " ", html, flags=re.S | re.I)
            html = re.sub(r"<style\b[^>]*>.*?</style>", " ", html, flags=re.S | re.I)
            html = re.sub(r"<!--.*?-->", " ", html, flags=re.S)
            text = re.sub(r"<[^>]+>", " ", html).lower()
            rel = os.path.relpath(path, ROOT)
            for phrase in forbidden:
                self.assertNotIn(phrase, text, "%s shows %r" % (rel, phrase))
