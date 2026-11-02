"""Fail when a page adds an inline style block or a class the stylesheet does not define.

Current exceptions are listed below. They are classes and style blocks that
already shipped. A new page must not add to either list.
"""
import os
import re
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CSS_PATH = os.path.join(ROOT, "assets", "styles.css")
IDENT = re.compile(r"^[A-Za-z_][\w-]*$")

# Pages that already contain a <style> block. systemkalkyl is self-contained.
STYLE_BLOCK_PAGES = {
    "systemkalkyl/index.html",
    "systemkalkyl/jamfor/fortnox-vs-spiris-totalkostnad/index.html",
}

# Class names already used in published HTML but not defined in assets/styles.css.
UNDEFINED_CLASS_WHITELIST = {
    "badge-warn",
    "btn",
    "byline",
    "cp-below",
    "grid",
    "guide-video-frame",
    "highlight",
    "muted",
    "quote",
    "source-link",
    "summary-box",
    "tldr",
    "tw",
    "warn",
}

SKIP_DIRS = {"saastruth", "public", ".git", "node_modules", "scripts", "tests"}


def published_html():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        rel = os.path.relpath(dirpath, ROOT)
        parts = [] if rel == "." else rel.split(os.sep)
        if parts and parts[0] in SKIP_DIRS:
            dirnames[:] = []
            continue
        dirnames[:] = [name for name in dirnames if name not in SKIP_DIRS]
        for name in filenames:
            if name.endswith(".html"):
                yield os.path.join(dirpath, name)


def defined_classes():
    with open(CSS_PATH, encoding="utf-8") as handle:
        css = handle.read()
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    return set(re.findall(r"\.(-?[A-Za-z_][\w-]*)", css))


def classes_in(html):
    scan = re.sub(r"<!--.*?-->", "", html, flags=re.S)
    scan = re.sub(r"<pre\b[^>]*>.*?</pre>", "", scan, flags=re.S | re.I)
    scan = re.sub(r"<code\b[^>]*>.*?</code>", "", scan, flags=re.S | re.I)
    found = set()
    for match in re.finditer(r'\bclass\s*=\s*"([^"]*)"', scan):
        value = match.group(1)
        if "${" in value or "+" in value:
            continue
        for token in value.split():
            if IDENT.match(token):
                found.add(token)
    return found


class TestStyleReuse(unittest.TestCase):
    def test_no_new_inline_style_blocks_or_undefined_classes(self):
        defined = defined_classes()
        new_style_blocks = []
        new_classes = {}
        for path in published_html():
            rel = os.path.relpath(path, ROOT)
            with open(path, encoding="utf-8") as handle:
                html = handle.read()
            if re.search(r"<style\b", html, re.I) and rel not in STYLE_BLOCK_PAGES:
                new_style_blocks.append(rel)
            for token in classes_in(html):
                if token not in defined and token not in UNDEFINED_CLASS_WHITELIST:
                    new_classes.setdefault(token, rel)
        self.assertEqual(new_style_blocks, [])
        self.assertEqual(new_classes, {})
