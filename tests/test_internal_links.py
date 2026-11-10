"""Every sitemap URL is linked from static HTML, including the homepage."""
import os
import re
import unittest
from collections import defaultdict, deque
from html.parser import HTMLParser
from urllib.parse import urljoin

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class _Anchors(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ("script", "style"):
            self.skip += 1
        if tag == "a" and self.skip == 0 and "href" in attrs:
            self.hrefs.append(attrs["href"])

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.skip:
            self.skip -= 1


def _published_pages():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        rel = os.path.relpath(dirpath, ROOT)
        parts = [] if rel == "." else rel.split(os.sep)
        if parts and parts[0] in ("public", "saastruth", ".git", "node_modules", "scripts", "tests", "systemkalkyl", "go", "preview", "docs"):
            dirnames[:] = []
            continue
        dirnames[:] = [name for name in dirnames if name not in ("public", "saastruth", ".git", "node_modules", "go", "preview")]
        for name in filenames:
            if name == "index.html":
                yield os.path.join(dirpath, name)


def _page_url(path):
    rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
    if rel == "index.html":
        return "/"
    return "/" + rel[: -len("index.html")]


def _normalize(base, href):
    href = href.split("#", 1)[0].split("?", 1)[0]
    if not href or href.startswith(("mailto:", "javascript:")):
        return None
    if href.startswith("http") and "saasbill.io" not in href:
        return None
    if href.startswith("http"):
        path = href.split("saasbill.io", 1)[1]
    else:
        path = urljoin(base, href)
    if path.endswith("index.html"):
        path = path[: -len("index.html")]
    if path != "/" and not path.endswith("/"):
        if "." in path.rsplit("/", 1)[-1]:
            return None
        path += "/"
    return path


def _sitemap_urls():
    with open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8") as handle:
        xml = handle.read()
    return re.findall(r"<loc>https://saasbill.io([^<]*)</loc>", xml)


class TestInternalLinks(unittest.TestCase):
    def test_every_sitemap_url_has_a_static_inbound_link(self):
        locs = _sitemap_urls()
        self.assertEqual(len(locs), 45)
        inbound = defaultdict(set)
        graph = defaultdict(set)
        home_directory = set()
        for path in _published_pages():
            src = _page_url(path)
            with open(path, encoding="utf-8") as handle:
                html = handle.read()
            parser = _Anchors()
            parser.feed(html)
            if src == "/":
                section = html.split('id="site-directory"', 1)[1].split("</section>", 1)[0]
                directory = _Anchors()
                directory.feed(section)
                for href in directory.hrefs:
                    target = _normalize("/", href)
                    if target:
                        home_directory.add(target)
            for href in parser.hrefs:
                target = _normalize(src, href)
                if not target or target == src:
                    continue
                inbound[target].add(src)
                if target in locs:
                    graph[src].add(target)

        missing_home = [loc for loc in locs if loc != "/" and loc not in home_directory]
        self.assertEqual(missing_home, [], "homepage directory is missing " + ", ".join(missing_home))

        counts = []
        for loc in locs:
            if loc == "/":
                continue
            sources = inbound.get(loc, set())
            self.assertTrue(sources, loc + " has no internal inbound link")
            others = sources - {"/"}
            self.assertGreaterEqual(len(others), 2, loc + " needs links from related pages, found " + str(sorted(others)))
            counts.append(len(sources))
        self.assertGreaterEqual(min(counts), 1)
        self.assertLessEqual(max(counts), 80)

        seen = {"/": 0}
        queue = deque(["/"])
        while queue:
            current = queue.popleft()
            for nxt in graph[current]:
                if nxt not in seen:
                    seen[nxt] = seen[current] + 1
                    queue.append(nxt)
        too_far = [loc for loc in locs if seen.get(loc, 99) > 2]
        self.assertEqual(too_far, [])

    def test_related_block_has_three_to_five_links(self):
        for path in _published_pages():
            if _page_url(path) == "/":
                continue
            with open(path, encoding="utf-8") as handle:
                html = handle.read()
            self.assertIn("related-calc-grid", html, path)
            block = html.split('class="related-calc-grid"', 1)[1]
            block = block.split("<details", 1)[0] if "<details" in block else block.split("</section>", 1)[0]
            count = block.count("<a ")
            self.assertGreaterEqual(count, 3, path)
            self.assertLessEqual(count, 5, path)


if __name__ == "__main__":
    unittest.main()
