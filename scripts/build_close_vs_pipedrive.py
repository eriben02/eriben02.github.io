"""Build /compare/close-vs-pipedrive-year-1-cost-calculator/.

Every price comes from data/crm_pricing.json (with source URL, status and
verified date). The Year-1 math lives in close_vs_pipedrive_calc.js; this
script inlines it, runs it in Node to prerender the default scenario and the
FAQ examples, and writes the page with render_workbench() + render_page().
public/ is written by render_page and then copied to the repo root.
"""
import html
import json
import os
import shutil
import subprocess
from datetime import date

from layout import BASE_DIR, DATA_DIR, PUBLIC_DIR, render_page, render_workbench

REL = "compare/close-vs-pipedrive-year-1-cost-calculator/index.html"
SLUG = "/compare/close-vs-pipedrive-year-1-cost-calculator/"
CALC_JS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "close_vs_pipedrive_calc.js")

DEFAULT_INPUT = {
    "users": 5, "billing": "annual", "email": True, "sequences": False,
    "leadcapture": False, "calling": "click", "minutes": 500, "excludeDialer": False,
}


def load_pricing():
    with open(os.path.join(DATA_DIR, "crm_pricing.json"), encoding="utf-8") as f:
        return json.load(f)


def load_affiliates():
    with open(os.path.join(DATA_DIR, "affiliate_links.json"), encoding="utf-8") as f:
        return json.load(f)


def human(iso):
    d = date.fromisoformat(iso)
    return d.strftime("%b ") + str(d.day) + d.strftime(", %Y")


def verified_dates(node, out):
    if isinstance(node, dict):
        if node.get("verified_date") and str(node.get("status", "")).startswith("verified"):
            out.append(node["verified_date"])
        for v in node.values():
            verified_dates(v, out)
    elif isinstance(node, list):
        for v in node:
            verified_dates(v, out)
    return out


def oldest_verified(pricing):
    return min(verified_dates(pricing, []))


def money(n):
    return "$" + format(int(round(n)), ",")


def unit(n):
    return "$" + (format(int(n), ",") if float(n).is_integer() else "%.2f" % n)


def calc_data(pricing):
    """The subset of crm_pricing.json the browser needs. Secondary prices are
    dropped (null) unless calc_policy.allow_secondary is true."""
    policy = pricing["calc_policy"]
    allow = bool(policy["allow_secondary"])
    c, p, a = pricing["close"], pricing["pipedrive"], pricing["dialer_reference_aircall"]

    def close_plan(v):
        ok = v["status"] == "verified"
        return {"label": v["label"], "annual": v["annual"] if ok else None, "monthly": v["monthly"] if ok else None}

    def pd_plan(v):
        def pick(kind):
            st = v[kind + "_status"]
            return v[kind] if (st == "verified" or (st == "secondary" and allow)) else None
        return {"label": v["label"], "annual": pick("annual"), "monthly": pick("monthly")}

    lb = p["addons"]["leadbooster"]
    return {
        "allowSecondary": allow,
        "numbersPerRep": policy["numbers_per_rep"],
        "defaultMinutes": policy["default_minutes_per_rep_month"],
        "close": {
            "plans": {k: close_plan(v) for k, v in c["plans"].items()},
            "callPerMin": c["usage"]["call_per_min_usd"]["value"],
            "numberPerMonth": c["usage"]["number_per_month_usd"]["value"],
            "sourceUrl": c["source_url"],
            "verified": human(c["plans"]["essentials"]["verified_date"]),
            "ctaLabel": "Try Close (14-day trial)",
        },
        "pipedrive": {
            "plans": {k: pd_plan(v) for k, v in p["plans"].items()},
            "leadbooster": {"annual": lb["annual"], "monthly": lb["monthly"]},
            "sourceUrl": p["source_url"],
            "verified": human(p["plans"]["growth"]["verified_date"]),
            "ctaLabel": "Try Pipedrive (14-day trial)",
        },
        "aircall": {
            "essentials": {"label": a["essentials"]["label"], "annual": a["essentials"]["annual"], "monthly": a["essentials"]["monthly"]},
            "professional": {"label": a["professional"]["label"], "annual": a["professional"]["annual"], "monthly": a["professional"]["monthly"]},
            "minLicenses": a["min_licenses"],
            "extraNumber": a["extra_number_monthly_usd"],
            "includedNumbers": a["included_numbers"],
        },
    }


def js_core(data):
    with open(CALC_JS, encoding="utf-8") as f:
        calc = f.read()
    return "const CP_DATA = " + json.dumps(data, separators=(",", ":")) + ";\n" + calc


def run_node(core, scenarios):
    """Run the page's own JS in Node so prerendered HTML and FAQ numbers come
    from exactly the same function as the live calculator."""
    script = core + """
const SC = %s;
const out = {};
for (const k of Object.keys(SC)) {
  const r = calcCloseVsPipedrive(SC[k]);
  out[k] = {r: r, cards: cpCardsHtml(r), best: cpBestLine(r), scenario: cpScenario(r), table: cpTableHtml(r), math: cpMathRows(r, 'both')};
}
console.log(JSON.stringify(out));
""" % json.dumps(scenarios)
    res = subprocess.run(["node", "-e", script], capture_output=True, text=True, check=True)
    return json.loads(res.stdout)


def scenarios():
    base = dict(DEFAULT_INPUT)
    return {
        "default": base,
        "power": dict(base, sequences=True, calling="power", minutes=1000),
        "solo_lc": {"users": 1, "billing": "annual", "email": True, "leadcapture": True, "calling": "none", "minutes": 0},
        "duo_lc": {"users": 2, "billing": "annual", "email": True, "leadcapture": True, "calling": "none", "minutes": 0},
    }


def pct_saving(annual, monthly):
    return round((1 - float(annual) / float(monthly)) * 100)


def build_faqs(pricing, runs):
    c, p, a = pricing["close"], pricing["pipedrive"], pricing["dialer_reference_aircall"]
    d, pw = runs["default"]["r"], runs["power"]["r"]
    s1, s2 = runs["solo_lc"]["r"]["pipedrive"], runs["duo_lc"]["r"]["pipedrive"]
    minutes = pricing["calc_policy"]["default_minutes_per_rep_month"]
    cp = c["plans"]
    savings = {k: pct_saving(v["annual"], v["monthly"]) for k, v in cp.items()}
    lo_plan = min(savings, key=savings.get)
    hi_plan = max(savings, key=savings.get)
    growth_scale = [cp[k]["label"] for k in c["features"]["power_dialer"]]
    pred = [cp[k]["label"] for k in c["features"]["predictive_dialer"]]
    calls = c["usage"]["call_per_min_usd"]["value"]
    number = c["usage"]["number_per_month_usd"]["value"]
    vat_pd = p["vat"]["value"]

    def name(r, v):
        if v == "close":
            return "Close " + r["close"]["planLabel"]
        q = r["pipedrive"]
        s = "Pipedrive " + q["planLabel"]
        if q["leadbooster"]:
            s += " + LeadBooster"
        if q["dialerTier"]:
            s += " + Aircall " + q["dialerLabel"]
        return s

    return [
        ("Is Close or Pipedrive cheaper for a team that makes calls?",
         "It depends on plan needs and call volume. For %d reps on annual billing with email tracking, click-to-call and %d billed minutes per rep per month (an example assumption), %s comes to %s and %s to %s in Year 1. With sequences, a power dialer and 1,000 minutes, %s comes to %s and %s to %s."
         % (d["seats"], minutes, name(d, "close"), money(d["close"]["total"]), name(d, "pipedrive"), money(d["pipedrive"]["total"]),
            name(pw, "close"), money(pw["close"]["total"]), name(pw, "pipedrive"), money(pw["pipedrive"]["total"]))),
        ("Does Pipedrive have a built-in dialer?",
         "No. Pipedrive's help center says it doesn't have a built-in calling integration and that calls are made through a calling app from its Marketplace, such as Aircall, CloudTalk, Kixie, JustCall or CallHippo. This calculator prices Aircall as the reference dialer: %s at %s and %s at %s per license per month billed annually, with a minimum of %d licenses."
         % (a["essentials"]["label"], unit(a["essentials"]["annual"]), a["professional"]["label"], unit(a["professional"]["annual"]), a["min_licenses"])),
        ("How much do calls cost in Close?",
         "Close says most outbound calls cost around %s per minute, varying by country and number type. Each call is rounded up to the next full minute, so billed minutes are at least your talk time. Phone numbers start at about %s per month."
         % (unit(calls), unit(number))),
        ("Do Close or Pipedrive have a seat minimum?",
         "Neither states a seat minimum, and Close Solo is limited to 1 user. Pipedrive charges per seat whether the seat is assigned to a user or not. The Aircall dialer requires at least %d licenses, so a 1-rep Pipedrive team pays for %d."
         % (a["min_licenses"], a["min_licenses"])),
        ("Annual vs monthly billing: how much do you save?",
         "On Close, annual billing saves %d%% to %d%% depending on the plan (%s %s vs %s per seat per month; %s %s vs %s). Pipedrive's pricing page says annual billing saves %s. Pipedrive's monthly prices are not verified here, so monthly totals for Pipedrive are shown as a minimum and marked unverified."
         % (savings[lo_plan], savings[hi_plan], cp[lo_plan]["label"], unit(cp[lo_plan]["annual"]), unit(cp[lo_plan]["monthly"]),
            cp[hi_plan]["label"], unit(cp[hi_plan]["annual"]), unit(cp[hi_plan]["monthly"]), p["annual_savings_claim"]["value"])),
        ("When is Pipedrive Premium cheaper than Growth + LeadBooster?",
         "Only at 1 seat on annual billing: Premium costs %s a year and Growth + LeadBooster %s. At 2 seats Growth + LeadBooster is lower (%s vs %s), because LeadBooster is priced per company (from %s per month) while Premium adds %s per seat per month."
         % (money(s1["total"]), money(s1["altTotal"]), money(s2["total"]), money(s2["altTotal"]),
            unit(p["addons"]["leadbooster"]["annual"]), unit(p["plans"]["premium"]["annual"] - p["plans"]["growth"]["annual"]))),
        ("Which Close plan includes the power dialer?",
         "%s (%s per seat per month billed annually). The predictive dialer is %s only."
         % (" and ".join(growth_scale), " and ".join(unit(cp[k]["annual"]) for k in c["features"]["power_dialer"]), " and ".join(pred))),
        ("Are prices in USD and do they include VAT?",
         "All prices are in USD from the vendors' US pricing pages. Pipedrive states its prices are VAT %s. Close's VAT treatment is unknown here. Pipedrive may show localized prices outside the US."
         % vat_pd),
    ]


def pill(status):
    if status in ("verified", "verified_from_price_only"):
        return '<span class="status-pill status-verified">verified</span>'
    if status == "secondary":
        return '<span class="status-pill status-unknown">unverified</span>'
    return '<span class="status-pill status-unknown">unknown</span>'


def sources_rows(pricing):
    c, p, a = pricing["close"], pricing["pipedrive"], pricing["dialer_reference_aircall"]
    cp, pp = c["plans"], p["plans"]
    lb = p["addons"]["leadbooster"]
    rows = [
        (c["source_url"], "Close plans per seat per month: " + ", ".join("%s %s annual / %s monthly" % (v["label"], unit(v["annual"]), unit(v["monthly"])) for v in cp.values()) + ". Features by plan, ~%s/min calls, numbers from ~%s/mo, Call Assistant, extra org." % (unit(c["usage"]["call_per_min_usd"]["value"]), unit(c["usage"]["number_per_month_usd"]["value"])), cp["essentials"]["verified_date"], "verified"),
        (c["usage"]["call_rounding"]["source_url"], "Close call rounding: per call, up to the next full minute. SMS price per unit: unknown.", c["usage"]["call_rounding"]["verified_date"], "verified"),
        (c["volume_discount"]["source_url"], "Close discount for 10+ seats and 12+ months exists; amount not stated.", c["volume_discount"]["verified_date"], "unknown"),
        (p["source_url"], "Pipedrive plans per seat per month billed annually: " + ", ".join("%s %s" % (v["label"], unit(v["annual"])) for v in pp.values()) + ". VAT exclusive. 14-day trial.", pp["growth"]["verified_date"], "verified"),
        (p["source_url"], "Pipedrive monthly prices: not verified on the vendor page, not used in totals.", pp["growth"]["verified_date"], "secondary"),
        (lb["source_url"], "LeadBooster from %s per month per company (annual). Monthly price unknown." % unit(lb["annual"]), lb["verified_date"], "verified"),
        (p["addons"]["inclusion_source"], "LeadBooster, Projects and Smart Docs included in Premium and Ultimate. Seats charged whether assigned or not.", p["seat_billing"]["verified_date"], "verified"),
        (p["features"]["calling_source"], "Pipedrive has no built-in calling; calls via Marketplace apps.", p["features"]["verified_date"], "verified"),
        (a["source_url"], "Aircall (reference dialer, not an affiliate): Essentials %s, Professional %s per license per month billed annually, minimum %d licenses, 1 number included, extra numbers %s/mo. Monthly prices unknown." % (unit(a["essentials"]["annual"]), unit(a["professional"]["annual"]), a["min_licenses"], unit(a["extra_number_monthly_usd"])), a["verified_date"], "verified"),
    ]
    out = []
    for url, what, when, status in rows:
        out.append(
            '<tr><td data-label="Source"><a href="%s" target="_blank" rel="noopener">%s</a></td>'
            '<td data-label="What">%s</td><td data-label="Verified"><time datetime="%s">%s</time></td><td data-label="Status">%s</td></tr>'
            % (html.escape(url), html.escape(url.replace("https://", "").rstrip("/")), what, when, human(when), pill(status))
        )
    return "".join(out)


def controls_html(policy):
    """Same control vocabulary as the homepage workbench: a platform select on
    top, sliders with a value box, wb-tool-select selects and the quiet billing
    field at the bottom. Checkboxes are the only page-specific control."""
    minutes = policy["default_minutes_per_rep_month"]
    return f"""
        <div class="wb-control-item">
          <label class="wb-control-label" for="cp-view">Platform to inspect</label>
          <select id="cp-view" class="wb-tool-select" data-track="calculator-control" data-control="cp-view">
            <option value="close" selected>Close</option>
            <option value="pipedrive">Pipedrive</option>
          </select>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="cp-users">Sales reps (seats)</label>
          <div class="wb-slider-row cp-slider-row">
            <input type="range" id="cp-users" min="1" max="50" step="1" value="5" aria-label="Sales reps who need a CRM seat" data-track="calculator-control" data-control="cp-users" />
            <input type="number" class="wb-slider-val cp-num" id="cp-users-num" min="1" max="50" step="1" value="5" inputmode="numeric" aria-label="Sales reps (number)" data-track="calculator-control" data-control="cp-users" />
          </div>
        </div>
        <fieldset class="wb-control-item cp-checks">
          <legend class="wb-control-label">Your team needs</legend>
          <label class="cp-check"><input type="checkbox" id="cp-email" checked data-track="calculator-control" data-control="cp-email" /><span>Email open tracking</span></label>
          <label class="cp-check"><input type="checkbox" id="cp-sequences" data-track="calculator-control" data-control="cp-sequences" /><span>Follow-up sequences</span></label>
          <label class="cp-check"><input type="checkbox" id="cp-leadcapture" data-track="calculator-control" data-control="cp-leadcapture" /><span>Website lead capture</span></label>
        </fieldset>
        <div class="wb-control-item">
          <label class="wb-control-label" for="cp-calling">How reps call</label>
          <select id="cp-calling" class="wb-tool-select" data-track="calculator-control" data-control="cp-calling">
            <option value="none">No calling in the CRM</option>
            <option value="click" selected>Click-to-call</option>
            <option value="power">Power dialer</option>
          </select>
        </div>
        <div class="wb-control-item" id="cp-minutes-wrap">
          <label class="wb-control-label" for="cp-minutes">Billed minutes / rep / month</label>
          <div class="wb-slider-row cp-slider-row">
            <input type="range" id="cp-minutes" min="0" max="3000" step="50" value="{minutes}" aria-label="Billed call minutes per rep per month" data-track="calculator-control" data-control="cp-minutes" />
            <input type="number" class="wb-slider-val cp-num" id="cp-minutes-num" min="0" max="3000" step="50" value="{minutes}" inputmode="numeric" aria-label="Billed call minutes (number)" data-track="calculator-control" data-control="cp-minutes" />
          </div>
          <p class="cp-hint">{minutes} is an example assumption.</p>
          <label class="cp-check"><input type="checkbox" id="cp-exclude-dialer" data-track="calculator-control" data-control="cp-exclude-dialer" /><span>Already have a dialer (exclude it)</span></label>
        </div>
        <div class="wb-quiet-options">
          <div class="wb-quiet-field">
            <label for="cp-billing">Billing:</label>
            <select id="cp-billing" data-track="calculator-control" data-control="cp-billing">
              <option value="annual" selected>Annual</option>
              <option value="monthly">Monthly</option>
            </select>
          </div>
        </div>
"""


PAGE_JS = r"""
(function () {
  var viewTouched = false;
  function el(id) { return document.getElementById(id); }
  function clampInt(v, lo, hi, fallback) {
    var n = Math.round(Number(v));
    if (!isFinite(n)) n = fallback;
    return Math.min(hi, Math.max(lo, n));
  }
  function readInput() {
    return {
      users: clampInt(el('cp-users').value, 1, 50, 5),
      billing: el('cp-billing').value || 'annual',
      email: el('cp-email').checked,
      sequences: el('cp-sequences').checked,
      leadcapture: el('cp-leadcapture').checked,
      calling: el('cp-calling').value,
      minutes: clampInt(el('cp-minutes').value, 0, 3000, CP_DATA.defaultMinutes),
      excludeDialer: el('cp-exclude-dialer').checked
    };
  }
  function applyWorkbench(r, view) {
    if (typeof window.saasbillApplyWorkbench !== 'function') return;
    var v = view === 'pipedrive' ? r.pipedrive : r.close;
    var isPd = view === 'pipedrive';
    var hidden = isPd ? v.dialer : (v.usage + v.numbers);
    var best = cpBestLine(r);
    window.saasbillApplyWorkbench({
      product: cpName(r, view),
      sticker: v.seat || 0,
      seats: isPd ? (v.addons || 0) : 0,
      hidden: hidden || 0,
      total: v.total === null ? v.floor : v.total,
      baseLabel: r.seats + ' seats &times; ' + (v.rate === null ? 'unverified' : cpUnit(v.rate)) + ' &times; 12 (' + v.planLabel + ', ' + r.billing + ')',
      seatsTitle: 'Add-ons',
      seatsLabel: 'LeadBooster below Premium',
      hiddenLabel: isPd ? 'Third-party dialer (Pipedrive has no built-in calling)' : 'Call minutes &amp; numbers (usage)',
      mathHtml: cpMathRows(r, view),
      bestHtml: best,
      ctaHref: isPd ? '/go/pipedrive' : '/go/close',
      ctaLabel: isPd ? CP_DATA.pipedrive.ctaLabel : CP_DATA.close.ctaLabel,
      ctaVendor: isPd ? 'pipedrive-crm' : 'close-crm'
    });
    ['shell-sub-base', 'shell-sub-seats', 'shell-sub-hidden'].forEach(function (id) {
      var n = el(id);
      if (n) n.innerHTML = n.textContent;
    });
    if (isPd && v.leadbooster && v.addons === null) {
      var row = el('shell-row-seats');
      if (row) row.style.display = '';
      el('shell-amt-seats').textContent = 'unknown';
    }
    if (isPd && v.seat === null) el('shell-amt-base').textContent = 'unverified';
    if (isPd && v.dialer === null) el('shell-amt-hidden').textContent = '\u2265 ' + cpMoney(v.dialerNumbers);
    if (v.total === null) {
      el('shell-big').innerHTML = '&ge; ' + cpMoney(v.floor) + cpPill('unverified');
      el('shell-sub').textContent = 'Includes unverified prices, which are not counted as $0.';
    }
  }
  function render() {
    var input = readInput();
    el('cp-users-num').value = input.users;
    el('cp-minutes-num').value = input.minutes;
    var calling = input.calling !== 'none';
    var wrap = el('cp-minutes-wrap');
    if (wrap) wrap.hidden = !calling;
    var r = calcCloseVsPipedrive(input);
    if (!viewTouched) el('cp-view').value = r.lowest === 'pipedrive' ? 'pipedrive' : 'close';
    el('cp-cards').innerHTML = cpCardsHtml(r);
    el('cp-scenario').innerHTML = 'Based on ' + cpScenario(r);
    el('cp-tbody').innerHTML = cpTableHtml(r);
    applyWorkbench(r, el('cp-view').value || 'close');
    if (typeof window.trackSaaSBillEvent === 'function') window.trackSaaSBillEvent('result_rendered', { page: '/compare/close-vs-pipedrive-year-1-cost-calculator/' });
  }
  function pair(rangeId, numId, lo, hi) {
    var range = el(rangeId), box = el(numId);
    range.addEventListener('input', render);
    box.addEventListener('input', function () {
      if (box.value === '') return;
      range.value = clampInt(box.value, lo, hi, lo);
      render();
    });
    box.addEventListener('change', function () {
      range.value = clampInt(box.value, lo, hi, lo);
      render();
    });
  }
  pair('cp-users', 'cp-users-num', 1, 50);
  pair('cp-minutes', 'cp-minutes-num', 0, 3000);
  ['cp-email', 'cp-sequences', 'cp-leadcapture', 'cp-calling', 'cp-exclude-dialer', 'cp-billing'].forEach(function (id) {
    el(id).addEventListener('change', render);
  });
  el('cp-view').addEventListener('change', function () { viewTouched = true; render(); });
  render();
})();
"""


def body_html(pricing, affiliates, runs, data, core):
    policy = pricing["calc_policy"]
    c, p, a = pricing["close"], pricing["pipedrive"], pricing["dialer_reference_aircall"]
    oldest = oldest_verified(pricing)
    d = runs["default"]
    lb = p["addons"]["leadbooster"]
    ad = p["addons"]
    cu = c["usage"]

    shell = render_workbench(
        controls_html(policy),
        cta_href="/go/close",
        cta_label=data["close"]["ctaLabel"],
        cta_vendor="close-crm",
    ).replace('<a id="shell-cta" ', '<a id="shell-cta" target="_blank" rel="sponsored nofollow noopener" ', 1)
    # The chart column fills the height of the (taller) controls column.
    shell = shell.replace('<div class="workbench-grid">', '<div class="workbench-grid wb-fill-chart">', 1)
    shell = shell.replace('<div class="wb-best-option" id="shell-best"></div>',
                          '<div class="wb-best-option" id="shell-best">%s</div>' % d["best"], 1)
    # Same verdict-section as the shared shell, with the three equal cards this
    # comparison needs instead of the generic sticker / gap pair.
    v_start = shell.index('<section class="verdict-section"')
    shell = shell[:v_start] + f"""<section class="verdict-section" aria-label="Year-1 cost summary">
  <p class="summary-scenario summary-shared-scenario" id="cp-scenario">Based on {d["scenario"]}</p>
  <div class="summary-strip" id="cp-cards" aria-live="polite">{d["cards"]}</div>
</section>
"""

    disclosure = "SaaSBill may earn a commission if you sign up via these links. It does not change the calculation; both vendors get the same button."
    dc, dp = d["r"]["close"], d["r"]["pipedrive"]
    lead = (
        "Pipedrive has no built-in calling, so a team that calls from its CRM also pays for a dialer. "
        "For %d reps, Close %s comes to %s in Year 1 and Pipedrive %s + Aircall to %s (example: %s billed min/rep/mo)."
        % (d["r"]["seats"], dc["planLabel"], money(dc["total"]), dp["planLabel"], money(dp["total"]), policy["default_minutes_per_rep_month"])
    )

    return f"""
<section class="hero editorial-hero editorial-hero-wrap">
  <h1>Close vs Pipedrive (2026): True Year-1 Cost for Your Sales Team, Calling Included</h1>
  <p class="lead">{lead}</p>
  <p class="calc-affiliate-disclosure">{disclosure}</p>
</section>

{shell}

<section aria-labelledby="cp-compare-heading" class="cp-compare">
  <h2 id="cp-compare-heading">Side by side for your inputs</h2>
  <div class="table-wrap editorial-gap-table mobile-cards cp-table">
    <table>
      <thead>
        <tr>
          <th>Platform</th><th>Plan chosen</th><th>Seats &amp; add-ons</th><th>Calling / dialer</th><th>True Year-1 cost</th><th>Action</th>
        </tr>
      </thead>
      <tbody id="cp-tbody">{d["table"]}</tbody>
    </table>
  </div>
  <p class="cp-fineprint">Prices last verified: <time datetime="{oldest}">{human(oldest)}</time> &middot; USD, excl. VAT &middot; Aircall is a reference dialer, not an affiliate.</p>
</section>

<section class="editorial-below-section cp-below">
  <details class="full-table-disclosure below-disclosure">
    <summary class="full-table-summary">
      <span class="below-disclosure-title">What is not like-for-like</span>
      <span class="full-table-toggle-pill" aria-hidden="true">&darr;</span>
    </summary>
    <div class="full-table-body">
      <ul class="cp-list">
        <li>Close Forms (all plans) is a form builder. Pipedrive LeadBooster adds chatbot, live chat and Prospector, so lead capture is not the same product on both sides.</li>
        <li>The Close power dialer is built in on {" and ".join(c["plans"][k]["label"] for k in c["features"]["power_dialer"])}. Pipedrive needs a Marketplace app; this page prices Aircall {a["professional"]["label"]}, the Aircall plan with a power dialer.</li>
        <li>Close Solo does not include email open tracking, so email tracking moves Close to Essentials.</li>
        <li>Aircall outbound calls are {a["domestic_outbound"]}. Close bills call minutes on top of seats.</li>
      </ul>
    </div>
  </details>

  <details class="full-table-disclosure below-disclosure">
    <summary class="full-table-summary">
      <span class="below-disclosure-title">Assumptions</span>
      <span class="full-table-toggle-pill" aria-hidden="true">&darr;</span>
    </summary>
    <div class="full-table-body">
      <ul class="cp-list">
        <li>USD, excluding VAT. Year 1 = 12 months at the selected billing.</li>
        <li>One phone number per rep, on both sides.</li>
        <li>{unit(cu["call_per_min_usd"]["value"])} per minute is Close's approximate rate for most outbound calls; it varies by country. Each call is rounded up to the next full minute, so billed minutes are at least talk time.</li>
        <li>{policy["default_minutes_per_rep_month"]} billed minutes per rep per month is an example assumption. Set your own.</li>
        <li>Aircall is the only priced dialer, chosen because its prices are published (other Marketplace dialers are not priced here). Aircall requires at least {a["min_licenses"]} licenses and includes {a["included_numbers"]} number; extra numbers are {unit(a["extra_number_monthly_usd"])} per month.</li>
        <li>No discounts. Close offers a discount for 10+ seats on 12+ month terms, but the amount is not published.</li>
        <li>Pipedrive monthly prices, the LeadBooster monthly price and Aircall monthly prices are not verified. Totals that need them are shown as a minimum (&ge;) with an unverified label, never as $0.</li>
        <li>Pipedrive may show localized prices outside the US.</li>
      </ul>
    </div>
  </details>

  <details class="full-table-disclosure below-disclosure">
    <summary class="full-table-summary">
      <span class="below-disclosure-title">Optional add-ons not in the total</span>
      <span class="full-table-toggle-pill" aria-hidden="true">&darr;</span>
    </summary>
    <div class="full-table-body">
      <ul class="cp-list">
        <li>Close Call Assistant: {unit(cu["call_assistant"]["monthly_usd"])} per month per {cu["call_assistant"]["per"]} + {unit(cu["call_assistant"]["per_min_usd"])} per transcribed minute.</li>
        <li>Close extra organization: {unit(cu["extra_org_monthly_usd"]["value"])} per month. Close SMS: price per unit unknown.</li>
        <li>Pipedrive Campaigns from {unit(ad["campaigns"]["from"])}, Web Visitors from {unit(ad["web_visitors"]["from"])}, Projects from {unit(ad["projects"]["from"])}, Smart Docs from {unit(ad["smart_docs"]["from"])} per month. Price basis (per company or per seat) unknown; Projects and Smart Docs are included in Premium and Ultimate.</li>
      </ul>
    </div>
  </details>

  <details class="full-table-disclosure below-disclosure" id="cp-sources">
    <summary class="full-table-summary">
      <span class="below-disclosure-title">Sources &amp; last verified</span>
      <span class="full-table-toggle-pill" aria-hidden="true">&darr;</span>
    </summary>
    <div class="full-table-body">
      <div class="table-wrap mobile-cards">
        <table>
          <thead><tr><th>Source</th><th>What was checked</th><th>Verified</th><th>Status</th></tr></thead>
          <tbody>{sources_rows(pricing)}</tbody>
        </table>
      </div>
    </div>
  </details>

  <p class="summary-interpretation"><a href="../monday-crm-vs-pipedrive-vs-hubspot-seat-minimums/" data-track="internal-audit">Seat buckets instead? monday CRM vs Pipedrive vs HubSpot &rarr;</a></p>
</section>

<script>
{core}
{PAGE_JS}
</script>
"""


def llms_lines():
    """Citation line and page entry for llms.txt, built from the same data and math."""
    pricing = load_pricing()
    core = js_core(calc_data(pricing))
    d = run_node(core, {"default": DEFAULT_INPUT})["default"]["r"]
    c, p, a = pricing["close"], pricing["pipedrive"], pricing["dialer_reference_aircall"]
    cu = c["usage"]
    finding = (
        "- **Close vs Pipedrive Year-1 cost with calling (Verified %s):** Pipedrive has no built-in calling, so a team that calls from the CRM adds a dialer "
        "(reference: Aircall Essentials %s or Professional %s per license/mo billed annually, minimum %d licenses, extra numbers %s/mo). "
        "Close includes calling: around %s/min for most outbound calls (each call rounded up to the next minute) plus numbers from about %s/mo. "
        "Seats billed annually: Close Essentials %s, Growth %s; Pipedrive Lite %s, Growth %s, Premium %s (Pipedrive monthly prices unverified). "
        "Example, %d reps, annual, email tracking, click-to-call, %d billed min/rep/mo (example assumption): %s vs %s."
        % (oldest_verified(pricing), unit(a["essentials"]["annual"]), unit(a["professional"]["annual"]), a["min_licenses"], unit(a["extra_number_monthly_usd"]),
           unit(cu["call_per_min_usd"]["value"]), unit(cu["number_per_month_usd"]["value"]),
           unit(c["plans"]["essentials"]["annual"]), unit(c["plans"]["growth"]["annual"]),
           unit(p["plans"]["lite"]["annual"]), unit(p["plans"]["growth"]["annual"]), unit(p["plans"]["premium"]["annual"]),
           d["seats"], d["minutes"],
           "Close %s %s" % (d["close"]["planLabel"], money(d["close"]["total"])),
           "Pipedrive %s + Aircall %s %s" % (d["pipedrive"]["planLabel"], d["pipedrive"]["dialerLabel"], money(d["pipedrive"]["total"])))
    )
    page = "- [Close vs. Pipedrive Year-1 Cost Calculator (Calling Included)](https://saasbill.io%s): Cheapest plan for your needs on each side, Close call minutes and numbers vs. a third-party dialer for Pipedrive, with sources and verification dates." % SLUG
    return finding, page


def copy_to_root(rel):
    src = os.path.join(PUBLIC_DIR, rel)
    dst = os.path.join(BASE_DIR, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src, dst)


def build():
    pricing = load_pricing()
    affiliates = load_affiliates()
    data = calc_data(pricing)
    core = js_core(data)
    runs = run_node(core, scenarios())
    d = runs["default"]["r"]
    desc = ("Close vs Pipedrive Year-1 cost with calling included: seats, Close call minutes and numbers, "
            "or a third-party dialer for Pipedrive. Example: %s vs %s for 5 reps. Prices verified %s."
            % (money(d["close"]["total"]), money(d["pipedrive"]["total"]), human(oldest_verified(pricing))))
    render_page(
        REL,
        "Close vs Pipedrive True Year-1 Cost (2026) – saasbill.io",
        desc,
        SLUG,
        body_html(pricing, affiliates, runs, data, core),
        faqs=build_faqs(pricing, runs),
        published_date="2026-10-30",
    )
    copy_to_root(REL)
    return runs


if __name__ == "__main__":
    build()
