"""Visible-copy lint for pages GitHub Pages publishes.

Reads data/copy_lint.json. Checks rendered text, not HTML comments or
ordinary attributes. Script and style contents are skipped for code tokens.
Editorial phrases are also checked inside quoted script strings, because
those strings are what the page shows after it runs.
"""
import json
import os
import re
from html.parser import HTMLParser

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEFAULT_RULES = os.path.join(ROOT, "data", "copy_lint.json")


class CopyLintError(Exception):
    def __init__(self, hits):
        self.hits = hits
        lines = ["%s: %r in %s" % (hit["path"], hit["phrase"], hit["snippet"]) for hit in hits]
        super().__init__("\n".join(lines))


class _Visible(HTMLParser):
    def __init__(self, visible_attributes):
        super().__init__(convert_charrefs=True)
        self.visible_attributes = set(visible_attributes)
        self.parts = []
        self.scripts = []
        self._skip = 0
        self._script = None

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._skip += 1
            if tag == "script":
                self._script = []
            return
        if self._skip:
            return
        found = dict(attrs)
        for name in self.visible_attributes:
            value = found.get(name)
            if value:
                self.parts.append(value)

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._skip:
            self._skip -= 1
            if tag == "script" and self._script is not None:
                self.scripts.append("".join(self._script))
                self._script = None

    def handle_data(self, data):
        if self._script is not None:
            self._script.append(data)
        elif not self._skip:
            self.parts.append(data)

    def handle_comment(self, data):
        return


def _quoted_strings(script):
    """String contents from a script, without comments."""
    script = re.sub(r"/\*.*?\*/", " ", script, flags=re.S)
    script = re.sub(r"(^|[^:\\])//[^\n]*", r"\1", script)
    out = []
    pattern = re.compile(r"\"([^\"\\]|\\.)*\"|'([^'\\]|\\.)*'|`([^`\\]|\\.)*`", re.S)
    for match in pattern.finditer(script):
        raw = match.group(0)[1:-1]
        if "\\" in raw and match.group(0)[0] != "`":
            try:
                raw = bytes(raw, "utf-8").decode("unicode_escape")
            except UnicodeError:
                pass
        out.append(raw)
    return "\n".join(out)


def visible_text(html, visible_attributes):
    parser = _Visible(visible_attributes)
    parser.feed(html)
    parser.close()
    text = " ".join(parser.parts)
    text = re.sub(r"\s+", " ", text)
    return text, parser.scripts


def _pattern(phrase, word_boundary):
    escaped = re.escape(phrase)
    if word_boundary:
        return re.compile(r"(?<!\w)" + escaped + r"(?!\w)", re.I)
    return re.compile(escaped, re.I)


def _snippet(text, match, radius=48):
    start = max(0, match.start() - radius)
    end = min(len(text), match.end() + radius)
    snippet = text[start:end].replace("\n", " ")
    snippet = re.sub(r"\s+", " ", snippet).strip()
    return snippet


def load_rules(path=None):
    with open(path or DEFAULT_RULES, encoding="utf-8") as handle:
        return json.load(handle)


def whitelist_for(rules, rel_path, phrase):
    rel = rel_path.replace("\\", "/")
    for entry in rules.get("whitelist", []):
        if entry.get("phrase", "").lower() != phrase.lower():
            continue
        allowed = entry.get("path", "")
        if allowed in ("*", rel) or rel.endswith(allowed):
            return entry.get("reason", "")
    return None


def check_copy(html, rel_path, rules=None):
    """Return a list of hits. Each hit has path, phrase, and snippet."""
    if rules is None:
        rules = load_rules()
    if not isinstance(html, str):
        html = html.decode("utf-8", "replace")
    scan = rules.get("scan", {})
    visible_attributes = scan.get("visible_attributes", ["alt", "title", "aria-label", "placeholder"])
    text, scripts = visible_text(html, visible_attributes)
    quoted = _quoted_strings("\n".join(scripts))
    hits = []
    for item in rules.get("phrases", []):
        phrase = item["phrase"]
        if whitelist_for(rules, rel_path, phrase):
            continue
        pattern = _pattern(phrase, item.get("word_boundary", False))
        surfaces = [("text", text)]
        if item.get("scan_script_strings", False):
            surfaces.append(("script", quoted))
        for surface, blob in surfaces:
            match = pattern.search(blob)
            if not match:
                continue
            hits.append({
                "path": rel_path,
                "phrase": phrase,
                "surface": surface,
                "snippet": _snippet(blob, match),
            })
            break
    return hits


def published_html_paths(root=None):
    """HTML files GitHub Pages serves from the repo root, excluding saastruth."""
    root = root or ROOT
    paths = []
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root)
        parts = [] if rel_dir == "." else rel_dir.split(os.sep)
        if parts and parts[0] in ("saastruth", "public", ".git", "node_modules", "scripts", "tests"):
            dirnames[:] = []
            continue
        dirnames[:] = [name for name in dirnames if name not in ("saastruth", "public", ".git", "node_modules")]
        for name in filenames:
            if name.endswith(".html"):
                paths.append(os.path.join(dirpath, name))
    return sorted(paths)


def lint_tree(root=None, rules=None):
    root = root or ROOT
    rules = rules or load_rules()
    hits = []
    for path in published_html_paths(root):
        rel = os.path.relpath(path, root)
        with open(path, encoding="utf-8") as handle:
            html = handle.read()
        hits.extend(check_copy(html, rel, rules))
    return hits
