"""Close vs Pipedrive Year-1 calculator: math, links, sources, publishing, Plausible.

Spec: Growth Sprint 1 build spec, section 9. Runs the page's own JS in Node.
"""
import collections
import json
import os
import re
import subprocess
import sys
import threading
import unittest
from datetime import date
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PUBLIC = os.path.join(ROOT, "public")
DATA = os.path.join(ROOT, "data")
REL = "compare/close-vs-pipedrive-year-1-cost-calculator/index.html"
URL = "https://saasbill.io/compare/close-vs-pipedrive-year-1-cost-calculator/"
CLOSE_GO = "https://refer.close.com/3k5hp07b8soi-fetl0j"
PIPEDRIVE_GO = "https://aff.trypipedrive.com/mlquvdui44me"
CHROME = "/opt/google/chrome/chrome"

# refer.close.com links per published page on main before this page existed.
# Other pages' Close affiliate links must not change.
CLOSE_LINK_BASELINE = {
        "compare/close-crm-vs-hubspot-sales-hub-5-to-20-reps/index.html": {
            "refer.close.com/3k5hp07b8soi-fetl0j": 3
        },
        "compare/monday-crm-vs-pipedrive-vs-hubspot-seat-minimums/index.html": {
            "refer.close.com/3k5hp07b8soi-fetl0j": 2
        },
        "exit/zoominfo-60-day-auto-renewal-notice-and-cancellation/index.html": {
            "refer.close.com/3k5hp07b8soi-fetl0j": 4
        },
        "faq/does-hubspot-charge-onboarding-fees-2026/index.html": {
            "refer.close.com/3k5hp07b8soi-fetl0j": 3
        },
        "hubspot-onboarding-fee-calculator/index.html": {
            "refer.close.com/3k5hp07b8soi-fetl0j": 4
        },
        "pricing/gong-io-platform-fee-and-seat-minimum-calculator/index.html": {
            "refer.close.com/3k5hp07b8soi-fetl0j": 3
        },
        "pricing/hubspot-true-cost-and-onboarding-fees/index.html": {
            "refer.close.com/3k5hp07b8soi-fetl0j": 4
        }
    }


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def page():
    return read(os.path.join(PUBLIC, REL))


def pricing():
    return json.loads(read(os.path.join(DATA, "crm_pricing.json")))


def affiliates():
    return json.loads(read(os.path.join(DATA, "affiliate_links.json")))


def balanced(src, signature):
    start = src.index(signature)
    i = src.index("{", start)
    depth = 0
    for j in range(i, len(src)):
        if src[j] == "{":
            depth += 1
        elif src[j] == "}":
            depth -= 1
            if depth == 0:
                return src[start:j + 1]
    raise ValueError("unbalanced " + signature)


def page_js(html):
    data = re.search(r"const CP_DATA = (\{.*?\});\n", html).group(0)
    names = ["calcCloseVsPipedrive", "cpMoney", "cpUnit", "cpPill", "cpTotal", "cpPart", "cpName",
             "cpScenario", "cpLowestLine", "cpMathRows", "cpAnswerHtml", "cpWhy", "cpSourceCell", "cpTableHtml"]
    return data + "\n".join(balanced(html, "function " + n + "(") for n in names)


def run_calc(inputs, render=False):
    html = page()
    script = page_js(html) + """
const IN = %s;
console.log(JSON.stringify(IN.map(function (i) {
  var r = calcCloseVsPipedrive(i);
  return %s;
})));
""" % (json.dumps(inputs), "{r: r, table: cpTableHtml(r), answer: cpAnswerHtml(r)}" if render else "r")
    res = subprocess.run(["node", "-e", script], capture_output=True, text=True, check=True)
    return json.loads(res.stdout)


def calc(**kw):
    base = {"users": 5, "billing": "annual", "email": False, "sequences": False, "leadcapture": False,
            "calling": "none", "minutes": 0, "excludeDialer": False}
    base.update(kw)
    return run_calc([base])[0]


class TestCloseVsPipedriveMath(unittest.TestCase):
    """Section 9A: exact expected numbers."""

    def test_default_scenario_matches_spec_example(self):
        r = calc(users=5, email=True, calling="click", minutes=500)
        self.assertEqual(r["close"]["plan"], "essentials")
        self.assertEqual((r["close"]["seat"], r["close"]["usage"], r["close"]["numbers"], r["close"]["total"]), (2100, 600, 60, 2760))
        p = r["pipedrive"]
        self.assertEqual(p["plan"], "growth")
        self.assertEqual((p["seat"], p["dialerLicenses"], p["dialerNumbers"], p["total"]), (2340, 1800, 288, 4428))
        self.assertEqual(r["lowest"], "close")
        self.assertEqual(r["difference"], 1668)

    def test_zero_minimum(self):
        r = calc(users=1)
        self.assertEqual((r["close"]["plan"], r["close"]["total"], r["close"]["usage"]), ("solo", 108, 0))
        self.assertEqual((r["pipedrive"]["plan"], r["pipedrive"]["total"], r["pipedrive"]["dialer"]), ("lite", 168, 0))

    def test_clamping(self):
        self.assertEqual(calc(users=0)["seats"], 1)
        self.assertEqual(calc(users=999)["seats"], 50)
        self.assertEqual(calc(users="abc")["seats"], 1)

    def test_normal(self):
        r = calc(users=5, email=True, sequences=True, calling="power", minutes=1000)
        c, p = r["close"], r["pipedrive"]
        self.assertEqual((c["plan"], c["seat"], c["usage"], c["numbers"], c["total"]), ("growth", 5940, 1200, 60, 7200))
        self.assertEqual((p["plan"], p["seat"], p["dialerTier"], p["dialerLicenses"], p["dialerNumbers"], p["total"]),
                         ("growth", 2340, "professional", 3000, 288, 5628))
        self.assertEqual(r["lowest"], "pipedrive")

    def test_high(self):
        r = calc(users=20, email=True, sequences=True, leadcapture=True, calling="power", minutes=2000)
        c, p = r["close"], r["pipedrive"]
        self.assertEqual((c["seat"], c["usage"], c["numbers"], c["total"]), (23760, 9600, 240, 33600))
        self.assertEqual((p["plan"], p["leadbooster"], p["seat"], p["addons"], p["dialerLicenses"], p["dialerNumbers"], p["total"]),
                         ("growth", True, 9360, 390, 12000, 1368, 23118))
        self.assertEqual((p["altPlan"], p["altTotal"]), ("premium", 27528))

    def test_breakpoint_one_seat_premium(self):
        p = calc(users=1, email=True, leadcapture=True)["pipedrive"]
        self.assertEqual((p["plan"], p["leadbooster"], p["total"]), ("premium", False, 708))
        self.assertEqual(p["altTotal"], 858)

    def test_breakpoint_two_seats_growth_plus_leadbooster(self):
        p = calc(users=2, email=True, leadcapture=True)["pipedrive"]
        self.assertEqual((p["plan"], p["leadbooster"], p["total"]), ("growth", True, 1326))
        self.assertEqual(p["altTotal"], 1416)

    def test_aircall_minimum(self):
        p = calc(users=1, email=True, calling="power", minutes=0)["pipedrive"]
        self.assertEqual((p["licenses"], p["dialerLicenses"], p["extraNumbers"], p["dialerNumbers"], p["dialer"]), (3, 1800, 0, 0, 1800))

    def test_monthly_unknown_is_never_zero(self):
        r = calc(users=5, billing="monthly", leadcapture=True, calling="click", minutes=500)
        p = r["pipedrive"]
        self.assertIsNone(p["total"])
        self.assertIsNone(p["seat"])
        for key in ("leadbooster_monthly", "aircall_monthly", "pipedrive_monthly"):
            self.assertIn(key, r["unknown"])
        self.assertEqual(p["floor"], 4 * 6 * 12)  # only the verified extra numbers
        self.assertEqual(r["close"]["total"], 5 * 49 * 12 + 600 + 60)
        self.assertIsNone(r["difference"])
        self.assertIsNone(r["lowest"])  # Close 3600 is not below a $288 floor, so no claim

    def test_exclude_dialer(self):
        r = calc(users=5, email=True, sequences=True, calling="power", minutes=1000, excludeDialer=True)
        self.assertEqual(r["pipedrive"]["total"], 2340)
        self.assertEqual(r["close"]["total"], 7200)

    def test_monthly_render_marks_unverified(self):
        out = run_calc([{"users": 5, "billing": "monthly", "email": True, "calling": "click", "minutes": 500}], render=True)[0]
        self.assertIn("&ge; ", out["table"])
        self.assertIn("status-unknown", out["table"])
        self.assertIn("unverified", out["table"])
        self.assertIsNone(out["r"]["pipedrive"]["rate"])
        for secondary in ("$24", "$49/seat", "$79", "$99/seat"):
            self.assertNotIn("Pipedrive " + secondary, out["table"])


class TestCloseVsPipedriveLinks(unittest.TestCase):
    """Section 9B."""

    def test_vendor_ctas(self):
        html = page()
        tags = re.findall(r"<a\b[^>]*data-vendor=\"(?:close-crm|pipedrive-crm)\"[^>]*>", html)
        self.assertGreaterEqual(len(tags), 3)
        locations = collections.defaultdict(set)
        for tag in tags:
            vendor = re.search(r'data-vendor="([^"]+)"', tag).group(1)
            href = re.search(r'href="([^"]+)"', tag).group(1)
            rel = re.search(r'rel="([^"]+)"', tag).group(1).split()
            self.assertEqual(href, {"close-crm": "/go/close", "pipedrive-crm": "/go/pipedrive"}[vendor], tag)
            self.assertIn("sponsored", rel, tag)
            self.assertIn("nofollow", rel, tag)
            self.assertIn('data-track="vendor-cta"', tag)
            self.assertIn('target="_blank"', tag)
            locations[vendor].add(re.search(r'data-cta-location="([^"]+)"', tag).group(1))
        self.assertIn("comparison-table", locations["close-crm"])
        self.assertIn("comparison-table", locations["pipedrive-crm"])
        self.assertIn('id="shell-cta" target="_blank" rel="sponsored nofollow noopener"', html)
        self.assertIn("Try Close (14-day trial) &rarr;", html)
        self.assertIn("Try Pipedrive (14-day trial) &rarr;", html)
        # Disclosure sits above the first vendor CTA.
        first_cta = html.index('data-track="vendor-cta" data-vendor=')
        self.assertLess(html.index("SaaSBill may earn a commission if you sign up via these links."), first_cta)
        # Source links to vendor pricing pages are not affiliate links.
        for src in ("https://www.close.com/pricing", "https://www.pipedrive.com/en/pricing", "https://aircall.io/pricing/"):
            for tag in re.findall(r'<a href="' + re.escape(src) + r'"[^>]*>', html):
                self.assertNotIn("sponsored", tag)
        self.assertNotIn("aircall.io/pricing/\" target=\"_blank\" rel=\"sponsored", html)

    def test_go_redirects(self):
        aff = affiliates()
        self.assertEqual(aff["close-crm"]["go_url"], CLOSE_GO)
        self.assertEqual(aff["pipedrive"]["go_url"], PIPEDRIVE_GO)
        self.assertEqual(aff["pipedrive"]["affiliate_url"], PIPEDRIVE_GO)
        self.assertEqual(aff["pipedrive"]["tracking_url"], "/go/pipedrive")
        self.assertTrue(aff["pipedrive"]["status"].startswith("active"))
        for slug, url in (("close", CLOSE_GO), ("pipedrive", PIPEDRIVE_GO)):
            pub = read(os.path.join(PUBLIC, "go", slug, "index.html"))
            root = read(os.path.join(ROOT, "go", slug, "index.html"))
            self.assertEqual(pub, root)
            self.assertIn('<meta name="robots" content="noindex,nofollow">', pub)
            self.assertIn('<meta http-equiv="refresh" content="0;url=%s">' % url, pub)
            self.assertIn('location.replace("%s")' % url, pub)
            self.assertEqual(set(re.findall(r"https://[^\"<>]+", pub)), {url})

    def test_go_not_in_sitemap_and_disallowed(self):
        for base in (ROOT, PUBLIC):
            self.assertNotIn("/go/", read(os.path.join(base, "sitemap.xml")))
            robots = read(os.path.join(base, "robots.txt"))
            self.assertIn("User-agent: *\nAllow: /\nDisallow: /go/\n", robots)
            self.assertIn("User-agent: Googlebot\nAllow: /\nDisallow: /go/\n", robots)

    def test_internal_links_resolve(self):
        html = page()
        page_dir = os.path.dirname(os.path.join(ROOT, REL))
        for href in re.findall(r'href="([^"]+)"', html):
            if href.startswith(("http://", "https://", "mailto:", "#", "${", "'")) or "' +" in href:
                continue
            path = href.split("#")[0].split("?")[0]
            target = os.path.join(ROOT, path.lstrip("/")) if path.startswith("/") else os.path.normpath(os.path.join(page_dir, path))
            if os.path.isdir(target):
                target = os.path.join(target, "index.html")
            self.assertTrue(os.path.exists(target), href)

    def test_inbound_internal_links(self):
        for rel in ("compare/monday-crm-vs-pipedrive-vs-hubspot-seat-minimums/index.html",
                    "compare/close-crm-vs-hubspot-sales-hub-5-to-20-reps/index.html"):
            self.assertIn('href="../close-vs-pipedrive-year-1-cost-calculator/"', read(os.path.join(PUBLIC, rel)), rel)
        home = read(os.path.join(PUBLIC, "index.html"))
        cards = home[home.index('id="all-calculators"'):]
        self.assertIn('<div class="card" data-cat="crm">\n      <span class="badge badge-high">CRM</span>\n      <h3><a href="./compare/close-vs-pipedrive-year-1-cost-calculator/">', cards)
        llms = read(os.path.join(PUBLIC, "llms.txt"))
        self.assertIn(URL, llms)

    def test_other_close_links_unchanged(self):
        for rel, expected in CLOSE_LINK_BASELINE.items():
            html = read(os.path.join(ROOT, rel))
            # Some pages embed data/affiliate_links.json as data (const AFFILIATES);
            # that copy now also carries close-crm.go_url. Count rendered links only.
            if "const AFFILIATES = " in html:
                html = html.replace(balanced(html, "const AFFILIATES = "), "")
            found = dict(sorted(collections.Counter(re.findall(r"refer\.close\.com/[A-Za-z0-9_-]+", html)).items()))
            self.assertEqual(found, expected, rel)
        close = affiliates()["close-crm"]
        self.assertEqual(close["tracking_url"], CLOSE_GO)
        self.assertEqual(close["destination_url"], CLOSE_GO)
        self.assertEqual(close["custom_links"], {
            "homepage": CLOSE_GO,
            "signup": "https://refer.close.com/7agqaw8t3yje",
            "discount_20pct": "https://refer.close.com/lt6p61c61z57-stack",
        })
        self.assertEqual(affiliates()["pipedrive"]["destination_url"], "https://www.pipedrive.com/en/pricing")
        self.assertNotIn("refer.close.com", page())
        self.assertNotIn("aff.trypipedrive.com", page())


class TestCloseVsPipedriveSources(unittest.TestCase):
    """Section 9C."""

    PRICE_KEYS = ("annual", "monthly", "value", "from", "monthly_usd", "per_min_usd")

    def walk(self, node, path, inherited_url, out):
        if isinstance(node, dict):
            url = node.get("source_url", inherited_url)
            if any(k in node for k in self.PRICE_KEYS) and "label" in node or any(k in node for k in ("value", "from", "monthly_usd")):
                out.append((path, node, url))
            elif "annual" in node or "monthly" in node:
                out.append((path, node, url))
            for k, v in node.items():
                self.walk(v, path + "." + k, url, out)
        return out

    def test_every_price_has_status_source_and_date(self):
        data = pricing()
        fields = self.walk(data, "", None, [])
        self.assertGreater(len(fields), 15)
        for path, node, url in fields:
            if path.startswith(".calc_policy"):
                continue
            status = node.get("status") or node.get("annual_status")
            self.assertIn(status, ("verified", "verified_from_price_only", "secondary", "unknown"), path)
            if status.startswith("verified"):
                self.assertTrue(url and url.startswith("https://"), path)
                self.assertRegex(node.get("verified_date", ""), r"^\d{4}-\d{2}-\d{2}$", path)
        for plan in data["pipedrive"]["plans"].values():
            self.assertEqual(plan["monthly_status"], "secondary")
        self.assertFalse(data["calc_policy"]["allow_secondary"])

    def test_staleness(self):
        data = pricing()
        policy = data["calc_policy"]
        dates = re.findall(r'"verified_date": "(\d{4}-\d{2}-\d{2})"', json.dumps(data))
        oldest = min(dates)
        age = (date.today() - date.fromisoformat(oldest)).days
        if age > policy["stale_warn_days"]:
            print("WARNING: crm_pricing.json oldest verified_date %s is %d days old" % (oldest, age), file=sys.stderr)
        self.assertLessEqual(age, policy["stale_fail_days"], "crm_pricing.json prices are older than %d days" % policy["stale_fail_days"])
        html = page()
        self.assertIn('Prices last verified: <time datetime="%s">' % oldest, html)

    def test_page_prices_exist_in_data(self):
        data = pricing()
        allowed = set()

        def collect(node):
            if isinstance(node, dict):
                for v in node.values():
                    collect(v)
            elif isinstance(node, list):
                for v in node:
                    collect(v)
            elif isinstance(node, (int, float)) and not isinstance(node, bool):
                allowed.add(round(float(node), 2))
        collect(data)
        r = calc(users=5, email=True, calling="click", minutes=500)
        collect(r)
        allowed.add(round(r["close"]["total"] / 5 / 12))
        allowed.add(round(r["pipedrive"]["total"] / 5 / 12))
        html = page()
        tbody = re.search(r'<tbody id="cp-tbody">(.*?)</tbody>', html, re.S).group(1)
        answer = re.search(r'<div id="cp-answer">(.*?)</div>\s*<p class="cp-disclosure">', html, re.S).group(1)
        sources = re.search(r'id="cp-sources"(.*?)</details>', html, re.S).group(1)
        for chunk in (tbody, answer, sources):
            for m in re.findall(r"\$(\d[\d,]*(?:\.\d+)?)", chunk):
                self.assertIn(round(float(m.replace(",", "")), 2), allowed, "$" + m)
        self.assertIn("$2,760", answer)
        self.assertIn("$4,428", answer)
        # Secondary Pipedrive monthly prices never render as numbers.
        for v in data["pipedrive"]["plans"].values():
            self.assertNotIn("$%d/seat" % v["monthly"], tbody)
        self.assertNotIn("$24", html)


class TestCloseVsPipedrivePublishing(unittest.TestCase):
    """Section 9D + 9E (static)."""

    def test_published_copy(self):
        pub = page()
        root = read(os.path.join(ROOT, REL))
        self.assertEqual(pub, root)
        self.assertGreaterEqual(len(pub.encode("utf-8")), 20 * 1024)
        self.assertNotIn("placeholder", pub.lower())
        for bad in ("Erik", "Bengtsson", "SaaSTruth", "\u2014", "&mdash;", "Best option", "Winner"):
            self.assertNotIn(bad, pub, bad)
        self.assertIn(URL, read(os.path.join(ROOT, "sitemap.xml")))
        self.assertIn("<h1>Close vs Pipedrive (2026): True Year-1 Cost for Your Sales Team, Calling Included</h1>", pub)
        lead = re.search(r'<p class="lead">(.*?)</p>', pub, re.S).group(1)
        self.assertEqual(lead.count(". "), 1)
        self.assertIn('"inLanguage": "en-US"', pub)
        self.assertIn("Lowest Year-1 cost", pub)
        for control in ("cp-users", "cp-billing", "cp-email", "cp-sequences", "cp-leadcapture", "cp-calling", "cp-minutes", "cp-exclude-dialer"):
            self.assertIn('data-control="%s"' % control, pub)
        self.assertIn('"@type": "FAQPage"', pub)
        self.assertEqual(pub.count('class="faq-item"'), 8)

    def test_plausible_static(self):
        html = page()
        self.assertIn('data-domain="saasbill.io"', html)
        self.assertIn("window.trackSaaSBillEvent('vendor_cta_click', { vendor: vendor, location: location, href: href });", html)
        self.assertIn("[data-track=\"vendor-cta\"]", html)


def _browser_or_skip():
    if not os.path.exists(CHROME):
        raise unittest.SkipTest("Chrome is not available")
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
    except ImportError:
        raise unittest.SkipTest("playwright is not installed")


PLAUSIBLE_SHIM = """
(function () {
  var q = (window.plausible && window.plausible.q) || [];
  window.plausible = function (name, opts) {
    fetch('https://plausible.io/api/event', {method: 'POST', body: JSON.stringify({n: name, d: 'saasbill.io', u: location.href, p: (opts || {}).props || {}})});
  };
  q.forEach(function (args) { window.plausible.apply(null, args); });
})();
"""


class TestCloseVsPipedriveBrowser(unittest.TestCase):
    """Section 9E (headless) and the mobile layout checks."""

    @classmethod
    def setUpClass(cls):
        _browser_or_skip()
        class Quiet(SimpleHTTPRequestHandler):
            def log_message(self, *args):
                pass
        handler = partial(Quiet, directory=ROOT)
        cls.httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        cls.base = "http://127.0.0.1:%d/%s" % (cls.httpd.server_address[1], REL.replace("index.html", ""))
        threading.Thread(target=cls.httpd.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "httpd"):
            cls.httpd.shutdown()
            cls.httpd.server_close()

    def open(self, p, width, height):
        ctx = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox"]).new_context(viewport={"width": width, "height": height})
        events = []
        # The real Plausible script ignores localhost; serve a shim with the same
        # plausible(name, {props}) contract and capture what reaches the network.
        ctx.route("https://plausible.io/js/**", lambda route: route.fulfill(status=200, content_type="application/javascript", body=PLAUSIBLE_SHIM))
        ctx.route("https://plausible.io/api/event", lambda route: (events.append(json.loads(route.request.post_data)), route.fulfill(status=202, body="ok")))
        pg = ctx.new_page()
        pg.goto(self.base, wait_until="networkidle")
        pg.evaluate("window.addEventListener('click', function (e) { if (e.target.closest('a[href]')) e.preventDefault(); })")
        return ctx, pg, events

    def test_cta_clicks_reach_plausible(self):
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            ctx, pg, events = self.open(p, 1280, 800)
            self.assertEqual(pg.inner_text("#shell-big"), "$2,760")
            ctas = pg.query_selector_all('[data-track="vendor-cta"]')
            expected = []
            for a in ctas:
                a.scroll_into_view_if_needed()
                a.click()
                expected.append({"vendor": a.get_attribute("data-vendor"), "location": a.get_attribute("data-cta-location"), "href": a.get_attribute("href")})
            pg.wait_for_timeout(500)
            pushed = pg.evaluate("window.__saasbillEvents.filter(function (e) { return e.event === 'vendor_cta_click'; }).map(function (e) { return {vendor: e.vendor, location: e.location, href: e.href}; })")
            self.assertEqual(pushed, expected)
            self.assertEqual({e["href"] for e in expected}, {"/go/close", "/go/pipedrive"})
            sent = [e for e in events if e["n"] == "vendor_cta_click"]
            self.assertEqual([e["p"] for e in sent], expected)
            ctx.browser.close()

    def test_mobile_layout_and_tap_targets(self):
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            ctx, pg, _ = self.open(p, 360, 800)
            overflow = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            self.assertLessEqual(overflow, 0)
            small = pg.evaluate("""() => Array.from(document.querySelectorAll(
              '.cp-check, .cp-seg-options label, .cp-num, #cp-calling, .cp-table a.btn-secondary, #shell-cta, .cp-answer .math-drawer > summary, .cp-below summary'))
              .filter(e => e.offsetParent !== null)
              .map(e => [e.className || e.id || e.tagName, Math.round(e.getBoundingClientRect().height)])
              .filter(x => x[1] < 44)""")
            self.assertEqual(small, [])
            # Interaction updates the answer from the same function.
            pg.select_option("#cp-calling", "power")
            pg.check("#cp-sequences")
            pg.fill("#cp-minutes-num", "1000")
            pg.dispatch_event("#cp-minutes-num", "change")
            self.assertIn("$7,200", pg.inner_text("#cp-answer"))
            self.assertIn("$5,628", pg.inner_text("#cp-answer"))
            pg.select_option("#cp-calling", "none")
            self.assertTrue(pg.evaluate("document.getElementById('cp-minutes-wrap').hidden"))
            pg.click('label:has(input[name="cp-billing"][value="monthly"])')
            self.assertIn("\u2265", pg.inner_text("#cp-answer"))
            self.assertIn("unverified", pg.inner_text("#cp-answer"))
            ctx.browser.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
