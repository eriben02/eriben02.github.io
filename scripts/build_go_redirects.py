"""Write the static /go/ affiliate redirect pages.

GitHub Pages has no server redirects, so each /go/<vendor>/ is a tiny HTML page
with meta refresh + location.replace. The target URL comes from
data/affiliate_links.json (go_url). These pages are noindex, are not in the
sitemap, are disallowed in robots.txt, and do NOT go through render_page (the
deploy guard's 20 KiB page minimum is for content pages).

Pageview: one navigator.sendBeacon to Plausible's Events API
(https://plausible.io/docs/events-api, text/plain JSON body) right before
location.replace. A beacon is queued by the browser and survives the
navigation, so the redirect is not delayed; it is skipped off saasbill.io
(local previews, tests) and when sendBeacon is missing or blocked. The meta
refresh stays as the no-JS fallback.
"""
import html
import json
import os
from urllib.parse import urlparse

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
PUBLIC_DIR = os.path.join(BASE_DIR, "public")

# go slug -> affiliate_links.json key
GO_PAGES = {
    "close": "close-crm",
    "pipedrive": "pipedrive",
}

TEMPLATE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="robots" content="noindex,nofollow">
<meta http-equiv="refresh" content="0;url={attr}">
<link rel="canonical" href="{attr}">
<title>Redirecting…</title>
<script>try{{if(location.hostname==="saasbill.io"&&navigator.sendBeacon)navigator.sendBeacon("https://plausible.io/api/event",JSON.stringify({{name:"pageview",url:location.href,domain:"saasbill.io",referrer:document.referrer||null}}));}}catch(e){{}}location.replace({js});</script>
</head><body><a href="{attr}" rel="sponsored nofollow">Continue</a></body></html>
"""


def load_affiliates():
    with open(os.path.join(DATA_DIR, "affiliate_links.json"), encoding="utf-8") as f:
        return json.load(f)


def go_target(affiliates, key):
    entry = affiliates[key]
    url = entry.get("go_url") or ""
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc:
        raise SystemExit("affiliate_links.json %s.go_url must be an https URL, got %r" % (key, url))
    return url


def render_redirect(url):
    return TEMPLATE.format(attr=html.escape(url, quote=True), js=json.dumps(url))


def build():
    affiliates = load_affiliates()
    written = []
    for slug, key in GO_PAGES.items():
        rel = os.path.join("go", slug, "index.html")
        page = render_redirect(go_target(affiliates, key))
        for root in (PUBLIC_DIR, BASE_DIR):
            path = os.path.join(root, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(page)
        written.append(rel)
    print("Wrote /go/ redirects: " + ", ".join(written))
    return written


if __name__ == "__main__":
    build()
