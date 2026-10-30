"""Build the Pipedrive Year-1 calculator and the Pipedrive vs HubSpot comparison.

Prices come from data/crm_pricing.json. HubSpot Sales Hub Professional and
Enterprise come from data/tools.json. Starter ($15/seat/month annual, $0
onboarding) is the figure already published in the HubSpot onboarding FAQ.
Unknown add-on price bases and unverified monthly prices are never treated as $0.
"""
import html
import json
import os
import re
import shutil
import subprocess
from datetime import date

from layout import BASE_DIR, DATA_DIR, PUBLIC_DIR, load_data, render_page, render_workbench

CALC_JS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pipedrive_year1_calc.js")
PD_REL = "pricing/pipedrive-true-year-1-cost-calculator/index.html"
PD_SLUG = "/pricing/pipedrive-true-year-1-cost-calculator/"
HS_REL = "compare/pipedrive-vs-hubspot-sales-hub-year-1-cost/index.html"
HS_SLUG = "/compare/pipedrive-vs-hubspot-sales-hub-year-1-cost/"
ADDON_ORDER = ["leadbooster", "smart_docs", "projects", "campaigns", "web_visitors"]
ADDON_LABELS = {
    "leadbooster": "LeadBooster",
    "smart_docs": "Smart Docs",
    "projects": "Projects",
    "campaigns": "Campaigns",
    "web_visitors": "Web Visitors",
}
DEFAULT = {"seats": 5, "plan": "growth", "tier": "professional", "addons": {k: False for k in ADDON_ORDER}}


def load_pricing():
    with open(os.path.join(DATA_DIR, "crm_pricing.json"), encoding="utf-8") as f:
        return json.load(f)


def human(iso):
    d = date.fromisoformat(iso)
    return d.strftime("%b ") + str(d.day) + d.strftime(", %Y")


def money(n):
    return "$" + format(int(round(n)), ",")


def unit(n):
    return "$" + (format(int(n), ",") if float(n).is_integer() else "%.2f" % n)


def starter_from_existing_faq():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build_queued_batch1.py")
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    match = re.search(r"HubSpot Starter \(\$(\d+)/seat/month annual\) has \$(\d+) mandatory onboarding", text)
    if not match:
        raise SystemExit("HubSpot Starter price is not in the existing onboarding FAQ")
    return int(match.group(1)), int(match.group(2))


def hubspot_plans():
    tools, _ = load_data()
    hs = next(t for t in tools if t["id"] == "hubspot-sales-pro")
    starter, starter_onboarding = starter_from_existing_faq()
    return {
        "starter": {"label": "Sales Hub Starter", "annual": starter, "onboarding": starter_onboarding},
        "professional": {
            "label": "Sales Hub Professional",
            "annual": hs["advertised_monthly_price_usd"],
            "onboarding": hs["mandatory_onboarding_fee_usd"],
        },
        "enterprise": {
            "label": "Sales Hub Enterprise",
            "annual": hs["enterprise_seat_price_usd"],
            "onboarding": hs["enterprise_onboarding_fee_usd"],
        },
        "sourceUrl": hs["source_urls"][0],
        "verified": human(hs["verified_date"]),
        "verifiedDate": hs["verified_date"],
    }


def page_data(pricing):
    p = pricing["pipedrive"]
    allow = bool(pricing["calc_policy"]["allow_secondary"])
    plans = {}
    for key, plan in p["plans"].items():
        annual = plan["annual"] if plan["annual_status"] == "verified" or (plan["annual_status"] == "secondary" and allow) else None
        plans[key] = {"label": plan["label"], "annual": annual}
    addons = {}
    for key in ADDON_ORDER:
        raw = p["addons"][key]
        addons[key] = {
            "label": ADDON_LABELS[key],
            "annual": raw.get("annual"),
            "from": raw.get("from"),
            "per": raw.get("per"),
            "includedIn": raw.get("included_in") or [],
        }
    hs = hubspot_plans()
    return {
        "pipedrive": {
            "plans": plans,
            "addons": addons,
            "addonOrder": ADDON_ORDER,
            "sourceUrl": p["source_url"],
            "verified": human(p["plans"]["growth"]["verified_date"]),
            "ctaLabel": "Try Pipedrive (14-day trial)",
        },
        "hubspot": {
            "plans": {k: {"label": hs[k]["label"], "annual": hs[k]["annual"], "onboarding": hs[k]["onboarding"]} for k in ("starter", "professional", "enterprise")},
            "sourceUrl": hs["sourceUrl"],
            "verified": hs["verified"],
        },
    }


def js_core(data):
    with open(CALC_JS, encoding="utf-8") as f:
        calc = f.read()
    return "const PY_DATA = " + json.dumps(data, separators=(",", ":")) + ";\n" + calc


def run_node(core, kind, scenarios):
    fn = "calcPipedriveYear1" if kind == "pd" else "calcPipedriveVsHubspot"
    cards = "pyCardsHtml" if kind == "pd" else "pyCompareCards"
    table = "pyTableHtml" if kind == "pd" else "pyCompareTable"
    best = "pyBestLine" if kind == "pd" else "pyCompareBest"
    scenario = "pyScenario" if kind == "pd" else "pyCompareScenario"
    script = core + """
const SC = %s;
const out = {};
for (const k of Object.keys(SC)) {
  const r = %s(SC[k]);
  out[k] = {r: r, cards: %s(r), table: %s(r), best: %s(r), scenario: %s(r)};
}
console.log(JSON.stringify(out));
""" % (json.dumps(scenarios), fn, cards, table, best, scenario)
    res = subprocess.run(["node", "-e", script], capture_output=True, text=True, check=True)
    return json.loads(res.stdout)


def addon_controls():
    bits = []
    for key in ADDON_ORDER:
        bits.append(
            '<label class="cp-check"><input type="checkbox" id="py-%s" data-track="calculator-control" data-control="py-%s" /><span>%s</span></label>'
            % (key, key, ADDON_LABELS[key])
        )
    return "\n".join(bits)


def plan_options(data, selected):
    out = []
    for key, plan in data["pipedrive"]["plans"].items():
        sel = " selected" if key == selected else ""
        out.append('<option value="%s"%s>%s (%s/seat/mo annual)</option>' % (key, sel, plan["label"], unit(plan["annual"])))
    return "".join(out)


def hs_options(data, selected):
    out = []
    for key, plan in data["hubspot"]["plans"].items():
        sel = " selected" if key == selected else ""
        out.append('<option value="%s"%s>%s (%s/seat/mo annual)</option>' % (key, sel, plan["label"], unit(plan["annual"])))
    return "".join(out)


def shell_for(controls, cta_href, cta_label, cta_vendor, best, scenario, cards, cards_id):
    shell = render_workbench(controls, cta_href=cta_href, cta_label=cta_label, cta_vendor=cta_vendor)
    rel = ' rel="sponsored nofollow noopener"' if cta_vendor == "pipedrive-crm" else ' rel="nofollow noopener"'
    shell = shell.replace('<a id="shell-cta" ', '<a id="shell-cta" target="_blank"' + rel + ' ', 1)
    shell = shell.replace('<div class="workbench-grid">', '<div class="workbench-grid wb-fill-chart">', 1)
    shell = shell.replace('<div class="wb-best-option" id="shell-best"></div>',
                          '<div class="wb-best-option" id="shell-best">%s</div>' % best, 1)
    v_start = shell.index('<section class="verdict-section"')
    shell = shell[:v_start] + (
        '<section class="verdict-section" aria-label="Year-1 cost summary">\n'
        '  <p class="summary-scenario summary-shared-scenario" id="py-scenario">Based on %s</p>\n'
        '  <div class="summary-strip" id="%s" aria-live="polite">%s</div>\n'
        '</section>\n' % (scenario, cards_id, cards)
    )
    return shell


def sources_table(pricing, hs):
    p = pricing["pipedrive"]
    rows = [(
        p["source_url"],
        "Pipedrive annual seat prices: " + ", ".join("%s %s" % (v["label"], unit(v["annual"])) for v in p["plans"].values()) + ". Monthly prices are not verified and are not used.",
        p["plans"]["growth"]["verified_date"],
        "verified",
    )]
    for key in ADDON_ORDER:
        raw = p["addons"][key]
        basis = raw.get("per") or "per seat or per company is not stated"
        price = raw.get("annual") if raw.get("annual") is not None else raw.get("from")
        rows.append((
            raw["source_url"],
            "%s from %s per month (%s). Included in: %s." % (ADDON_LABELS[key], unit(price), basis, ", ".join(raw.get("included_in") or []) or "no plan"),
            raw["verified_date"],
            raw["status"],
        ))
    rows.append((
        hs["sourceUrl"],
        "HubSpot Sales Hub annual: Starter %s/seat and $%s onboarding (existing onboarding FAQ), Professional %s/seat plus %s onboarding, Enterprise %s/seat plus %s onboarding."
        % (unit(hs["starter"]["annual"]), hs["starter"]["onboarding"], unit(hs["professional"]["annual"]), money(hs["professional"]["onboarding"]), unit(hs["enterprise"]["annual"]), money(hs["enterprise"]["onboarding"])),
        hs["verifiedDate"],
        "verified",
    ))
    out = []
    for url, what, when, status in rows:
        pill = "verified" if str(status).startswith("verified") else "unverified"
        klass = "status-verified" if pill == "verified" else "status-unknown"
        out.append(
            '<tr><td data-label="Source"><a href="%s" target="_blank" rel="noopener">%s</a></td><td data-label="What">%s</td><td data-label="Verified"><time datetime="%s">%s</time></td><td data-label="Status"><span class="status-pill %s">%s</span></td></tr>'
            % (html.escape(url), html.escape(url.replace("https://", "").rstrip("/")), what, when, human(when), klass, pill)
        )
    return "".join(out)


SHARED_TAIL = """
<section class="editorial-below-section cp-below">
  <details class="full-table-disclosure below-disclosure">
    <summary class="full-table-summary"><span class="below-disclosure-title">Assumptions</span><span class="full-table-toggle-pill" aria-hidden="true">&darr;</span></summary>
    <div class="full-table-body"><ul class="cp-list">
      <li>USD, excluding VAT. Year 1 = 12 months of annual billing. Pipedrive monthly prices are not verified, so this page does not total them.</li>
      <li>LeadBooster's annual price is per company. Smart Docs, Projects, Campaigns and Web Visitors publish a from-price only. Whether that price is per seat or per company is unknown, so a selected add-on is a floor (at least the from-price times 12), never $0.</li>
      <li>LeadBooster, Smart Docs and Projects are included in Premium and Ultimate. That inclusion is a verified extra of $0, labeled Included.</li>
      <li>Pipedrive has no built-in dialer. A Marketplace dialer is not added on these pages, and it is not entered as $0.</li>
      <li>HubSpot Sales Hub Professional is {pro}/seat/month annual plus {pro_on} onboarding. Enterprise is {ent}/seat/month annual plus {ent_on} onboarding. Starter is {st}/seat/month annual and {st_on} onboarding, from the onboarding FAQ already published on this site. Calling credits are not in the HubSpot total.</li>
    </ul></div>
  </details>
  <details class="full-table-disclosure below-disclosure" id="py-sources">
    <summary class="full-table-summary"><span class="below-disclosure-title">Sources &amp; last verified</span><span class="full-table-toggle-pill" aria-hidden="true">&darr;</span></summary>
    <div class="full-table-body"><div class="table-wrap mobile-cards"><table>
      <thead><tr><th>Source</th><th>What was checked</th><th>Verified</th><th>Status</th></tr></thead>
      <tbody>{sources}</tbody>
    </table></div></div>
  </details>
  <p class="summary-interpretation"><a href="{sibling}" data-track="internal-audit">{sibling_label} &rarr;</a></p>
</section>
"""


PD_JS = r"""
(function () {
  function el(id) { return document.getElementById(id); }
  function clamp(v) { var n = Math.round(Number(v)); if (!isFinite(n)) n = 5; return Math.min(50, Math.max(1, n)); }
  function read() {
    var addons = {};
    PY_DATA.pipedrive.addonOrder.forEach(function (id) { addons[id] = el('py-' + id).checked; });
    return { seats: clamp(el('py-seats').value), plan: el('py-plan').value, addons: addons };
  }
  function apply(r) {
    if (typeof window.saasbillApplyWorkbench !== 'function') return;
    var row = r.current, known = 0, floor = 0;
    row.lines.forEach(function (line) {
      if (!line.on || line.included) return;
      if (line.unknown) floor += line.floor || 0;
      else known += line.amount || 0;
    });
    window.saasbillApplyWorkbench({
      product: 'Pipedrive ' + row.planLabel,
      sticker: row.seat || 0,
      seats: known,
      hidden: floor,
      total: row.total === null ? (row.floor || 0) : row.total,
      seatsTitle: 'Known add-ons',
      seatsLabel: 'Priced per company, or included',
      hiddenLabel: floor > 0 ? 'Add-ons with an unpublished price basis (floor)' : 'No unpublished add-on on this plan',
      baseLabel: row.seats + ' seats x ' + (row.rate === null ? 'unverified' : ('$' + row.rate)) + ' x 12',
      mathHtml: pyMathRows(row),
      bestHtml: pyBestLine(r),
      ctaHref: '/go/pipedrive',
      ctaLabel: PY_DATA.pipedrive.ctaLabel,
      ctaVendor: 'pipedrive-crm'
    });
    if (row.total === null) {
      el('shell-big').innerHTML = row.floor === null ? 'unknown' : '&ge; ' + pyMoney(row.floor);
      el('shell-sub').textContent = 'Includes an unpublished add-on price basis, which is not counted as $0.';
    }
  }
  function render() {
    var input = read();
    el('py-seats-num').value = input.seats;
    var r = calcPipedriveYear1(input);
    el('py-cards').innerHTML = pyCardsHtml(r);
    el('py-scenario').innerHTML = 'Based on ' + pyScenario(r);
    el('py-tbody').innerHTML = pyTableHtml(r);
    apply(r);
    if (typeof window.trackSaaSBillEvent === 'function') window.trackSaaSBillEvent('result_rendered', { page: '%s' });
  }
  var range = el('py-seats'), box = el('py-seats-num');
  range.addEventListener('input', render);
  box.addEventListener('change', function () { range.value = clamp(box.value); render(); });
  el('py-plan').addEventListener('change', render);
  PY_DATA.pipedrive.addonOrder.forEach(function (id) { el('py-' + id).addEventListener('change', render); });
  render();
})();
"""


HS_JS = r"""
(function () {
  function el(id) { return document.getElementById(id); }
  function clamp(v) { var n = Math.round(Number(v)); if (!isFinite(n)) n = 5; return Math.min(50, Math.max(1, n)); }
  function read() {
    var addons = {};
    PY_DATA.pipedrive.addonOrder.forEach(function (id) { addons[id] = el('py-' + id).checked; });
    return { seats: clamp(el('py-seats').value), plan: el('py-plan').value, tier: el('py-tier').value, addons: addons };
  }
  function apply(r) {
    if (typeof window.saasbillApplyWorkbench !== 'function') return;
    var view = el('py-view').value === 'hubspot' ? 'hubspot' : 'pipedrive';
    var row = view === 'hubspot' ? r.hubspot : r.pipedrive;
    var known = 0, floor = 0;
    if (view === 'pipedrive') {
      row.lines.forEach(function (line) {
        if (!line.on || line.included) return;
        if (line.unknown) floor += line.floor || 0;
        else known += line.amount || 0;
      });
    }
    window.saasbillApplyWorkbench({
      product: view === 'hubspot' ? row.planLabel : ('Pipedrive ' + row.planLabel),
      sticker: row.seat || 0,
      seats: view === 'hubspot' ? 0 : known,
      hidden: view === 'hubspot' ? row.onboarding : floor,
      total: row.total === null ? (row.floor || 0) : row.total,
      seatsTitle: 'Known add-ons',
      hiddenLabel: view === 'hubspot' ? 'Mandatory onboarding' : (floor > 0 ? 'Add-ons with an unpublished price basis (floor)' : 'No unpublished add-on on this plan'),
      baseLabel: row.seats + ' seats x $' + row.rate + ' x 12',
      mathHtml: view === 'hubspot' ? pyHsMath(row) : pyMathRows(row),
      bestHtml: pyCompareBest(r),
      ctaHref: view === 'hubspot' ? PY_DATA.hubspot.sourceUrl : '/go/pipedrive',
      ctaLabel: view === 'hubspot' ? 'View HubSpot pricing' : PY_DATA.pipedrive.ctaLabel,
      ctaVendor: view === 'hubspot' ? 'hubspot' : 'pipedrive-crm'
    });
    var cta = el('shell-cta');
    if (cta) cta.setAttribute('rel', view === 'hubspot' ? 'nofollow noopener' : 'sponsored nofollow noopener');
    if (row.total === null) {
      el('shell-big').innerHTML = '&ge; ' + pyMoney(row.floor);
      el('shell-sub').textContent = 'Includes an unpublished add-on price basis, which is not counted as $0.';
    }
  }
  function render() {
    var input = read();
    el('py-seats-num').value = input.seats;
    var r = calcPipedriveVsHubspot(input);
    el('py-cards').innerHTML = pyCompareCards(r);
    el('py-scenario').innerHTML = 'Based on ' + pyCompareScenario(r);
    el('py-tbody').innerHTML = pyCompareTable(r);
    apply(r);
    if (typeof window.trackSaaSBillEvent === 'function') window.trackSaaSBillEvent('result_rendered', { page: '%s' });
  }
  var range = el('py-seats'), box = el('py-seats-num');
  range.addEventListener('input', render);
  box.addEventListener('change', function () { range.value = clamp(box.value); render(); });
  ['py-plan', 'py-tier', 'py-view'].forEach(function (id) { el(id).addEventListener('change', render); });
  PY_DATA.pipedrive.addonOrder.forEach(function (id) { el('py-' + id).addEventListener('change', render); });
  render();
})();
"""


def seats_control():
    return """
        <div class="wb-control-item">
          <label class="wb-control-label" for="py-seats">Sales seats</label>
          <div class="wb-slider-row cp-slider-row">
            <input type="range" id="py-seats" min="1" max="50" step="1" value="5" aria-label="Sales seats" data-track="calculator-control" data-control="py-seats" />
            <input type="number" class="wb-slider-val cp-num" id="py-seats-num" min="1" max="50" step="1" value="5" inputmode="numeric" aria-label="Sales seats (number)" data-track="calculator-control" data-control="py-seats" />
          </div>
        </div>
"""


def pd_controls(data):
    return seats_control() + """
        <div class="wb-control-item">
          <label class="wb-control-label" for="py-plan">Pipedrive plan</label>
          <select id="py-plan" class="wb-tool-select" data-track="calculator-control" data-control="py-plan">%s</select>
        </div>
        <fieldset class="wb-control-item cp-checks">
          <legend class="wb-control-label">Add-ons</legend>
          %s
        </fieldset>
        <div class="wb-quiet-options"><div class="wb-quiet-field"><label>Billing:</label><span>Annual</span></div></div>
""" % (plan_options(data, "growth"), addon_controls())


def hs_controls(data):
    return """
        <div class="wb-control-item">
          <label class="wb-control-label" for="py-view">Platform to inspect</label>
          <select id="py-view" class="wb-tool-select" data-track="calculator-control" data-control="py-view">
            <option value="pipedrive" selected>Pipedrive</option>
            <option value="hubspot">HubSpot Sales Hub</option>
          </select>
        </div>
""" + seats_control() + """
        <div class="wb-control-item">
          <label class="wb-control-label" for="py-plan">Pipedrive plan</label>
          <select id="py-plan" class="wb-tool-select" data-track="calculator-control" data-control="py-plan">%s</select>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="py-tier">HubSpot Sales Hub plan</label>
          <select id="py-tier" class="wb-tool-select" data-track="calculator-control" data-control="py-tier">%s</select>
        </div>
        <fieldset class="wb-control-item cp-checks">
          <legend class="wb-control-label">Pipedrive add-ons</legend>
          %s
        </fieldset>
        <div class="wb-quiet-options"><div class="wb-quiet-field"><label>Billing:</label><span>Annual</span></div></div>
""" % (plan_options(data, "growth"), hs_options(data, "professional"), addon_controls())


def table_section(rows, fine):
    return """
<section aria-labelledby="py-compare-heading" class="cp-compare">
  <h2 id="py-compare-heading">Side by side for your inputs</h2>
  <div class="table-wrap editorial-gap-table mobile-cards cp-table">
    <table>
      <thead><tr><th>Platform</th><th>Plan chosen</th><th>Seats &amp; add-ons</th><th>Calling / dialer</th><th>True Year-1 cost</th><th>Action</th></tr></thead>
      <tbody id="py-tbody">%s</tbody>
    </table>
  </div>
  <p class="cp-fineprint">%s</p>
</section>
""" % (rows, fine)


def tail(pricing, hs, sibling, sibling_label):
    return SHARED_TAIL.format(
        pro=unit(hs["professional"]["annual"]),
        pro_on=money(hs["professional"]["onboarding"]),
        ent=unit(hs["enterprise"]["annual"]),
        ent_on=money(hs["enterprise"]["onboarding"]),
        st=unit(hs["starter"]["annual"]),
        st_on=money(hs["starter"]["onboarding"]),
        sources=sources_table(pricing, hs),
        sibling=sibling,
        sibling_label=sibling_label,
    )


def copy_to_root(rel):
    src = os.path.join(PUBLIC_DIR, rel)
    dst = os.path.join(BASE_DIR, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src, dst)


def pd_faqs(pricing, result):
    p = pricing["pipedrive"]
    row = result["current"]
    lite = next(r for r in result["rows"] if r["id"] == "lite")
    return [
        ("What does Pipedrive Growth cost for 5 seats in Year 1?",
         "On annual billing, Growth is %s per seat per month, so 5 seats are %s in Year 1 before add-ons. Lite at the same seat count is %s. Prices were checked %s."
         % (unit(p["plans"]["growth"]["annual"]), money(row["seat"]), money(lite["seat"]), human(p["plans"]["growth"]["verified_date"]))),
        ("Which Pipedrive add-ons have a published price basis?",
         "LeadBooster is %s per month per company on annual billing, and it is included in Premium and Ultimate. Smart Docs (from %s), Projects (from %s), Campaigns (from %s) and Web Visitors (from %s) publish a starting price only. Per seat versus per company is not stated, so those add-ons are a floor, not a $0 line."
         % (unit(p["addons"]["leadbooster"]["annual"]), unit(p["addons"]["smart_docs"]["from"]), unit(p["addons"]["projects"]["from"]), unit(p["addons"]["campaigns"]["from"]), unit(p["addons"]["web_visitors"]["from"]))),
        ("Does this total include a dialer?",
         "No. Pipedrive has no built-in calling. This calculator does not add a Marketplace dialer, and it does not enter that missing price as $0."),
    ]


def hs_faqs(pricing, hs, result):
    pd, hub = result["pipedrive"], result["hubspot"]
    return [
        ("Is Pipedrive or HubSpot Sales Hub cheaper for 5 seats?",
         "On the default annual example, Pipedrive %s is %s and %s is %s, which is %s in seats plus %s onboarding. Lowest Year-1 cost: Pipedrive. Change the plan or add an add-on with an unpublished price basis and the page stops naming a lowest option when that unknown could change the order."
         % (pd["planLabel"], money(pd["total"]), hub["planLabel"], money(hub["total"]), money(hub["seat"]), money(hub["onboarding"]))),
        ("What HubSpot prices are in this comparison?",
         "Sales Hub Starter is %s per seat per month annual with %s onboarding. Professional is %s per seat per month annual plus %s onboarding. Enterprise is %s per seat per month annual plus %s onboarding. Calling credits are not included."
         % (unit(hs["starter"]["annual"]), money(hs["starter"]["onboarding"]), unit(hs["professional"]["annual"]), money(hs["professional"]["onboarding"]), unit(hs["enterprise"]["annual"]), money(hs["enterprise"]["onboarding"]))),
        ("Why are some Pipedrive add-ons shown as at least?",
         "Campaigns, Web Visitors, Projects and Smart Docs publish a from-price, not whether it is per seat or per company. The Year-1 line uses at least that from-price times 12. It is not counted as $0, and no lowest option is named while that choice is open. Pipedrive monthly prices are unverified and are not used."),
    ]


def build():
    pricing = load_pricing()
    data = page_data(pricing)
    hs = hubspot_plans()
    core = js_core(data)
    pd_run = run_node(core, "pd", {"default": DEFAULT})["default"]
    hs_run = run_node(core, "hs", {"default": DEFAULT})["default"]
    disclosure = "SaaSBill may earn a commission if you sign up for Pipedrive via the link. It does not change the calculation."
    pd_row = pd_run["r"]["current"]
    pd_lead = (
        "Pipedrive %s for %d seats, billed annually, is %s in Year 1 before add-ons. "
        "Lite at the same seat count is %s. Add-ons whose price basis is unpublished are shown as at least the published starting price, never as $0."
        % (pd_row["planLabel"], pd_row["seats"], money(pd_row["total"]), money(next(r["seat"] for r in pd_run["r"]["rows"] if r["id"] == "lite")))
    )
    cmp = hs_run["r"]
    hs_lead = (
        "For %d seats on annual billing, Pipedrive %s is %s in Year 1 and %s is %s, including %s of mandatory onboarding. "
        "Lowest Year-1 cost: Pipedrive."
        % (cmp["seats"], cmp["pipedrive"]["planLabel"], money(cmp["pipedrive"]["total"]), cmp["hubspot"]["planLabel"], money(cmp["hubspot"]["total"]), money(cmp["hubspot"]["onboarding"]))
    )
    fine = "Prices last verified: Pipedrive <time datetime=\"%s\">%s</time>, HubSpot <time datetime=\"%s\">%s</time> &middot; USD, annual billing" % (
        pricing["pipedrive"]["plans"]["growth"]["verified_date"], human(pricing["pipedrive"]["plans"]["growth"]["verified_date"]), hs["verifiedDate"], hs["verified"])
    pd_body = f"""
<section class="hero editorial-hero editorial-hero-wrap">
  <h1>Pipedrive true Year-1 cost (2026): seats, plan and add-ons</h1>
  <p class="lead">{pd_lead}</p>
  <p class="calc-affiliate-disclosure">{disclosure}</p>
</section>
{shell_for(pd_controls(data), "/go/pipedrive", data["pipedrive"]["ctaLabel"], "pipedrive-crm", pd_run["best"], pd_run["scenario"], pd_run["cards"], "py-cards")}
{table_section(pd_run["table"], fine)}
{tail(pricing, hs, "../compare/pipedrive-vs-hubspot-sales-hub-year-1-cost/", "Compare Pipedrive with HubSpot Sales Hub")}
<script>
{core}
{PD_JS % PD_SLUG}
</script>
"""
    hs_body = f"""
<section class="hero editorial-hero editorial-hero-wrap">
  <h1>Pipedrive vs HubSpot Sales Hub (2026): true Year-1 cost</h1>
  <p class="lead">{hs_lead}</p>
  <p class="calc-affiliate-disclosure">{disclosure}</p>
</section>
{shell_for(hs_controls(data), "/go/pipedrive", data["pipedrive"]["ctaLabel"], "pipedrive-crm", hs_run["best"], hs_run["scenario"], hs_run["cards"], "py-cards")}
{table_section(hs_run["table"], fine)}
{tail(pricing, hs, "../pricing/pipedrive-true-year-1-cost-calculator/", "Open the Pipedrive Year-1 calculator")}
<script>
{core}
{HS_JS % HS_SLUG}
</script>
"""
    render_page(PD_REL, "Pipedrive True Year-1 Cost Calculator (2026) – saasbill.io",
                "Pipedrive Year-1 cost from published annual seat prices and add-ons. Unknown price bases are a floor, not $0. Example: %s for 5 Growth seats." % money(pd_row["total"]),
                PD_SLUG, pd_body, faqs=pd_faqs(pricing, pd_run["r"]), published_date="2026-10-30")
    render_page(HS_REL, "Pipedrive vs HubSpot Sales Hub True Year-1 Cost (2026) – saasbill.io",
                "Compare Pipedrive and HubSpot Sales Hub Year-1 cost for the same seats. Default: %s vs %s. Unpublished add-on price bases are not ranked."
                % (money(cmp["pipedrive"]["total"]), money(cmp["hubspot"]["total"])),
                HS_SLUG, hs_body, faqs=hs_faqs(pricing, hs, cmp), published_date="2026-10-30")
    copy_to_root(PD_REL)
    copy_to_root(HS_REL)
    return pd_run, hs_run


def llms_lines():
    pricing = load_pricing()
    data = page_data(pricing)
    core = js_core(data)
    pd = run_node(core, "pd", {"default": DEFAULT})["default"]["r"]["current"]
    both = run_node(core, "hs", {"default": DEFAULT})["default"]["r"]
    p = pricing["pipedrive"]
    finding = (
        "- **Pipedrive Year-1 cost (Verified %s):** Annual seats: Lite %s, Growth %s, Premium %s, Ultimate %s per seat per month. "
        "LeadBooster is %s per month per company and is included in Premium and Ultimate. "
        "Smart Docs, Projects, Campaigns and Web Visitors publish from-prices only; per seat vs per company is unknown and is not counted as $0. "
        "Example, 5 Growth seats, no add-ons: %s. Versus HubSpot Sales Hub Professional (%s/seat annual plus %s onboarding) the same 5 seats are %s. Lowest Year-1 cost on that example: Pipedrive."
        % (p["plans"]["growth"]["verified_date"], unit(p["plans"]["lite"]["annual"]), unit(p["plans"]["growth"]["annual"]), unit(p["plans"]["premium"]["annual"]), unit(p["plans"]["ultimate"]["annual"]),
           unit(p["addons"]["leadbooster"]["annual"]), money(pd["total"]), unit(data["hubspot"]["plans"]["professional"]["annual"]), money(data["hubspot"]["plans"]["professional"]["onboarding"]), money(both["hubspot"]["total"]))
    )
    pages = (
        "- [Pipedrive True Year-1 Cost Calculator](https://saasbill.io%s): Seats, Lite through Ultimate, and LeadBooster, Smart Docs, Projects, Campaigns and Web Visitors on annual billing.\n"
        "- [Pipedrive vs HubSpot Sales Hub Year-1 Cost](https://saasbill.io%s): Same seats, Pipedrive add-ons, and HubSpot Sales Hub Starter, Professional or Enterprise including onboarding."
        % (PD_SLUG, HS_SLUG)
    )
    return finding, pages


if __name__ == "__main__":
    build()
