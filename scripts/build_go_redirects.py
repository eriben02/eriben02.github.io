"""Write the static /go/ affiliate redirect pages.

GitHub Pages has no server redirects, so each /go/<vendor>/ is a tiny HTML page
with meta refresh + location.replace. The target URL comes from
data/affiliate_links.json (go_url). These pages are noindex, are not in the
sitemap, are disallowed in robots.txt, and do NOT go through render_page (the
deploy guard's 20 KiB page minimum is for content pages).

The Cloudflare Web Analytics snippet sits in <head>, before the delay-0 meta
refresh, so the browser starts the beacon while the document is still parsing.
With JavaScript, the refresh tag is removed and location.replace runs when the
beacon script loads or after 300 ms, whichever comes first. Without JavaScript
the meta refresh (content="0") still redirects immediately. The Continue link
keeps rel="sponsored nofollow".
"""
import html
import json
import os
import sys
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(__file__))
from layout import CF_WEB_ANALYTICS  # noqa: E402

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
PUBLIC_DIR = os.path.join(BASE_DIR, "public")

# go slug -> affiliate_links.json key.
# Approved programs use go_url (the network tracking link).
# Pending programs have no go_url. They redirect to destination_url.
# Do not invent a PartnerStack tracking ID.
GO_PAGES = {
    "close": "close-crm",
    "pipedrive": "pipedrive",
    "apollo": "apollo",
    "vanta": "vanta",
    "drata": "drata",
    # Approved tracking URLs already in affiliate_links.json. Not new destinations.
    "whop": "whop",
    "jotform": "jotform",
}

# CF_WEB_ANALYTICS contains {token} braces. Double them so str.format leaves
# the snippet unchanged and only substitutes {attr} and {js}.
TEMPLATE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="robots" content="noindex,nofollow">
""" + CF_WEB_ANALYTICS.replace("{", "{{").replace("}", "}}") + """
<meta http-equiv="refresh" content="0;url={attr}">
<link rel="canonical" href="{attr}">
<title>Redirecting…</title>
<script>(function(){{var meta=document.querySelector('meta[http-equiv="refresh"]');if(meta&&meta.parentNode)meta.parentNode.removeChild(meta);var done=false;function go(){{if(done)return;done=true;location.replace({js});}}var beacon=document.querySelector('script[data-cf-beacon]');if(beacon){{beacon.addEventListener('load',go);beacon.addEventListener('error',go);}}setTimeout(go,300);}})();</script>
</head><body><a href="{attr}" rel="sponsored nofollow">Continue</a></body></html>
"""


def load_affiliates():
    with open(os.path.join(DATA_DIR, "affiliate_links.json"), encoding="utf-8") as f:
        return json.load(f)


def go_target(affiliates, key):
    entry = affiliates[key]
    url = entry.get("go_url") or entry.get("destination_url") or ""
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
