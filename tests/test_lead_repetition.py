"""The sentence under the H1 should not be pasted again later on the page."""
import os
import re
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def visible(html):
    text = re.sub(r"<script\b[^>]*>.*?</script>", " ", html, flags=re.S | re.I)
    text = re.sub(r"<style\b[^>]*>.*?</style>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&\w+;", " ", text)
    return re.sub(r"\s+", " ", text)


class TestLeadRepetition(unittest.TestCase):
    def test_lead_sentence_is_not_repeated(self):
        with open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8") as handle:
            locs = re.findall(r"<loc>https://saasbill.io([^<]*)</loc>", handle.read())
        problems = []
        for loc in locs:
            path = os.path.join(ROOT, "index.html" if loc == "/" else loc.strip("/") + "/index.html")
            with open(path, encoding="utf-8") as handle:
                html = handle.read()
            match = re.search(r'<p class="lead">(.*?)</p>', html, re.S)
            if not match:
                continue
            lead = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", match.group(1))).strip()
            if len(lead) < 40:
                continue
            body = visible(html)
            if body.count(lead) > 1:
                problems.append(loc)
        self.assertEqual(problems, [])


if __name__ == "__main__":
    unittest.main()
