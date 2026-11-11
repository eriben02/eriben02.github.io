"""Pipedrive vs Salesforce Starter and Pro Suite, Year-1 license cost.

Primary sources checked 2026-11-05:
- https://www.pipedrive.com/en/pricing
- https://support.pipedrive.com/en/article/new-pipedrive-plans (updated 2026-09-03)
- https://www.salesforce.com/editions-pricing/sales-cloud/
- https://www.salesforce.com/sales/pricing/

Annual list, VAT extra. Pipedrive monthly rates in secondary write-ups are not used.
Unknown stays the word unknown and is not added as $0.

Default, 5 seats, add-ons off:
Growth 5 x $39 x 12 = $2,340
Premium 5 x $59 x 12 = $3,540
Starter 5 x $25 x 12 = $1,500
Pro 5 x $100 x 12 = $6,000
Pro plus API 5 x $125 x 12 = $7,500
Lite 5 x $14 x 12 = $840
Ultimate 5 x $79 x 12 = $4,740
Lowest of the five headline paths is Salesforce Starter at $1,500.
"""
import os
import shutil

from layout import BASE_DIR, PUBLIC_DIR, render_page, render_workbench, wrap_calculator_shell

TITLE = "Pipedrive vs Salesforce Year-1 – saasbill.io"
DESCRIPTION = (
    "At 5 seats, Salesforce Starter Suite is $1,500 for the year and Pipedrive Growth is $2,340. "
    "Pro Suite is $6,000 before the API add-on. Checked 5 Nov 2026."
)
REL = "compare/pipedrive-vs-salesforce-starter-and-pro-suite-cost/index.html"
CANONICAL = "/compare/pipedrive-vs-salesforce-starter-and-pro-suite-cost/"

CONTROLS = """
        <div class="wb-control-item">
          <label class="wb-control-label" for="ps-seats">Seats <span class="val-pill" id="ps-seats-val">5</span></label>
          <div class="wb-slider-row">
            <input type="range" id="ps-seats" min="1" max="25" step="1" value="5" aria-label="Number of seats" data-track="calculator-control" data-control="seats" />
          </div>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="ps-lead">LeadBooster on Growth</label>
          <select id="ps-lead" class="wb-tool-select" data-track="calculator-control" data-control="leadbooster">
            <option value="no" selected>Off</option>
            <option value="yes">On, $32.50/mo</option>
          </select>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="ps-engage">Sales Engagement on Pro</label>
          <select id="ps-engage" class="wb-tool-select" data-track="calculator-control" data-control="sales-engagement">
            <option value="no" selected>Off</option>
            <option value="yes">On, $50/user</option>
          </select>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="ps-premier">Premier Success on Pro</label>
          <select id="ps-premier" class="wb-tool-select" data-track="calculator-control" data-control="premier">
            <option value="no" selected>Off</option>
            <option value="yes">On, 30% of net</option>
          </select>
        </div>
        <p class="wb-budget-subnote">Annual list prices, VAT extra. Pipedrive bills every seat whether or not it is assigned. Salesforce implementation is unknown and is not added.</p>
"""

REST = r"""
<section>
  <h2>Five headline paths</h2>
  <p>These are license totals for the plans in the title. Pro plus API adds the published $25 per user per month Web Services API, which Pro Suite does not include. LeadBooster, Sales Engagement, and Premier Success change the totals only when you turn them on.</p>
  <div class="table-wrap editorial-gap-table mobile-cards">
    <table>
      <caption>Year-1 license cost for the seat count above</caption>
      <thead>
        <tr>
          <th>Path</th>
          <th>How it is priced</th>
          <th>Year-1</th>
        </tr>
      </thead>
      <tbody id="ps-tbody">
        <tr><td data-label="Path">Salesforce Starter</td><td data-label="How it is priced">$25 per user per month</td><td data-label="Year-1">$1,500</td></tr>
        <tr><td data-label="Path">Pipedrive Growth</td><td data-label="How it is priced">$39 per seat per month, annual</td><td data-label="Year-1">$2,340</td></tr>
        <tr><td data-label="Path">Pipedrive Premium</td><td data-label="How it is priced">$59 per seat per month, annual</td><td data-label="Year-1">$3,540</td></tr>
        <tr><td data-label="Path">Salesforce Pro</td><td data-label="How it is priced">$100 per user per month, billed annually</td><td data-label="Year-1">$6,000</td></tr>
        <tr><td data-label="Path">Pro plus API</td><td data-label="How it is priced">$100 plus $25 API per user per month</td><td data-label="Year-1">$7,500</td></tr>
      </tbody>
    </table>
  </div>
</section>

<section>
  <h2>Published annual seat prices</h2>
  <div class="table-wrap editorial-gap-table mobile-cards">
    <table>
      <caption>List price per seat, checked 5 Nov 2026. VAT extra.</caption>
      <thead>
        <tr>
          <th>Plan</th>
          <th>Per seat</th>
          <th>5 seats, Year-1</th>
          <th>10 seats, Year-1</th>
        </tr>
      </thead>
      <tbody>
        <tr><td data-label="Plan">Pipedrive Lite</td><td data-label="Per seat">$14/mo annual</td><td data-label="5 seats, Year-1">$840</td><td data-label="10 seats, Year-1">$1,680</td></tr>
        <tr><td data-label="Plan">Pipedrive Growth</td><td data-label="Per seat">$39/mo annual</td><td data-label="5 seats, Year-1">$2,340</td><td data-label="10 seats, Year-1">$4,680</td></tr>
        <tr><td data-label="Plan">Pipedrive Premium</td><td data-label="Per seat">$59/mo annual</td><td data-label="5 seats, Year-1">$3,540</td><td data-label="10 seats, Year-1">$7,080</td></tr>
        <tr><td data-label="Plan">Pipedrive Ultimate</td><td data-label="Per seat">$79/mo annual</td><td data-label="5 seats, Year-1">$4,740</td><td data-label="10 seats, Year-1">$9,480</td></tr>
        <tr><td data-label="Plan">Salesforce Starter Suite</td><td data-label="Per seat">$25/user/mo, monthly or annually</td><td data-label="5 seats, Year-1">$1,500</td><td data-label="10 seats, Year-1">$3,000</td></tr>
        <tr><td data-label="Plan">Salesforce Pro Suite</td><td data-label="Per seat">$100/user/mo, billed annually</td><td data-label="5 seats, Year-1">$6,000</td><td data-label="10 seats, Year-1">$12,000</td></tr>
        <tr><td data-label="Plan">Pro Suite plus API</td><td data-label="Per seat">$125/user/mo annual</td><td data-label="5 seats, Year-1">$7,500</td><td data-label="10 seats, Year-1">$15,000</td></tr>
      </tbody>
    </table>
  </div>
  <p>Pipedrive renamed its plans in 2025: Essential to Lite, Advanced to Growth, Professional and Power to Premium, Enterprise to Ultimate. This page uses the new names.</p>
  <p class="src-cluster"><a class="src-link" href="https://www.pipedrive.com/en/pricing">Pipedrive pricing</a> <span class="src-date">5 Nov 2026</span></p>
  <p class="src-cluster"><a class="src-link" href="https://support.pipedrive.com/en/article/new-pipedrive-plans">Pipedrive plan names</a> <span class="src-date">5 Nov 2026</span></p>
  <p class="src-cluster"><a class="src-link" href="https://www.salesforce.com/editions-pricing/sales-cloud/">Salesforce Sales Cloud editions</a> <span class="src-date">5 Nov 2026</span></p>
  <p class="src-cluster"><a class="src-link" href="https://www.salesforce.com/sales/pricing/">Salesforce sales pricing</a> <span class="src-date">5 Nov 2026</span></p>
</section>

<section>
  <h2>Add-ons with a published price</h2>
  <div class="table-wrap editorial-gap-table mobile-cards">
    <table>
      <caption>What is included, and what this calculator can add</caption>
      <thead>
        <tr>
          <th>Add-on</th>
          <th>Published price</th>
          <th>In the Year-1 total</th>
        </tr>
      </thead>
      <tbody>
        <tr><td data-label="Add-on">LeadBooster</td><td data-label="Published price">Starting at $32.50 per month per company. Included on Premium and Ultimate.</td><td data-label="In the Year-1 total">$390 for the year when you turn it on for Growth. Included on Premium.</td></tr>
        <tr><td data-label="Add-on">Web Services API</td><td data-label="Published price">$25 per user per month, annual. Not included in Pro Suite.</td><td data-label="In the Year-1 total">The Pro plus API row. Not added to Starter.</td></tr>
        <tr><td data-label="Add-on">Premier Success</td><td data-label="Published price">30% of net on Pro.</td><td data-label="In the Year-1 total">30% of the Pro fees in this model when you turn it on. Starter is not included.</td></tr>
        <tr><td data-label="Add-on">Sales Engagement</td><td data-label="Published price">$50 per user per month, annual.</td><td data-label="In the Year-1 total">Added to Pro and Pro plus API when you turn it on. Whether Starter can buy it: unknown.</td></tr>
        <tr><td data-label="Add-on">Einstein for Sales</td><td data-label="Published price">$75 per user per month.</td><td data-label="In the Year-1 total">unknown. The pages checked do not say Pro Suite can buy it.</td></tr>
        <tr><td data-label="Add-on">Marketing email sends</td><td data-label="Published price">$10 per 1,000 per month.</td><td data-label="In the Year-1 total">unknown. Send volume is not an input.</td></tr>
        <tr><td data-label="Add-on">Sales Dialer</td><td data-label="Published price">Starting at $5 per user per month.</td><td data-label="In the Year-1 total">unknown. The exact rate above the starting price is not published here.</td></tr>
        <tr><td data-label="Add-on">Projects</td><td data-label="Published price">Starting at $16. Included on Premium and Ultimate.</td><td data-label="In the Year-1 total">unknown. The line does not say per month or per seat.</td></tr>
        <tr><td data-label="Add-on">Campaigns</td><td data-label="Published price">Starting at $13.33. Not included.</td><td data-label="In the Year-1 total">unknown. The line does not say per month or per seat.</td></tr>
        <tr><td data-label="Add-on">Web Visitors</td><td data-label="Published price">Starting at $41. Not included.</td><td data-label="In the Year-1 total">unknown. The line does not say per month or per seat.</td></tr>
        <tr><td data-label="Add-on">Smart Docs</td><td data-label="Published price">Starting at $32.50. Included on Premium and Ultimate.</td><td data-label="In the Year-1 total">unknown. The line does not say per month or per seat.</td></tr>
        <tr><td data-label="Add-on">Sandboxes</td><td data-label="Published price">A percent of net spend.</td><td data-label="In the Year-1 total">unknown. The percent is not published here.</td></tr>
        <tr><td data-label="Add-on">Data Cloud</td><td data-label="Published price">unknown</td><td data-label="In the Year-1 total">unknown</td></tr>
        <tr><td data-label="Add-on">Implementation</td><td data-label="Published price">unknown. Salesforce setup is partner-driven.</td><td data-label="In the Year-1 total">unknown</td></tr>
      </tbody>
    </table>
  </div>
  <p class="summary-caveat">Secondary write-ups list Pipedrive monthly rates of Lite $24, Growth $49, Premium $79, and Ultimate $99 per seat. The official page we checked was on annual pricing, so those monthly rates are not in the total. Do not read a $24 homepage figure as the Growth list.</p>
</section>

<section>
  <h2>What the contract pages add</h2>
  <ul class="key-list">
    <li>Pipedrive prices are VAT exclusive. SSO (SAML) is on every plan. The company blog says HIPAA is not supported.</li>
    <li>Salesforce Pro Suite is an annual commitment. The main services agreement dated 15 Oct 2026 says fees are not cancelable, and section 11.2 sets written notice at least 30 days before renewal.</li>
    <li>The storage figure named for the org is 10 GB. A full storage price list is unknown. A negotiated discount is unknown.</li>
    <li>Pipedrive phone and SMS list prices, AI overage, and credit unit prices are unknown.</li>
  </ul>
</section>

<section>
  <h2>What buyers asked</h2>
  <ul class="key-list">
    <li>A Reddit thread asks about life on Salesforce Starter Suite. <a href="https://www.reddit.com/r/salesforce/comments/1jmkjw3/experience_with_salesforce_starter_suite/" target="_blank" rel="noopener">Salesforce Starter thread</a></li>
    <li>A 2026 Reddit thread says the Pipedrive bill is more than the plan price. <a href="https://www.reddit.com/r/PipedriveConsultant/comments/1qwlm88/pipedrive_pricing_in_2026_isnt_just_the_plan/" target="_blank" rel="noopener">Pipedrive pricing thread</a></li>
    <li>A G2 review by Abby M on 17 Sep 2026 said the self-service pricing was hard to follow. No Salesforce partner quote is used as a list price.</li>
  </ul>
</section>
<script>
function calcPipedriveSalesforce(input) {
  var seats = Math.max(1, Math.round(Number(input.seats) || 1));
  var lead = !!input.leadbooster;
  var engage = !!input.engagement;
  var premier = !!input.premier;
  var lite = seats * 14 * 12;
  var growth = seats * 39 * 12;
  var premium = seats * 59 * 12;
  var ultimate = seats * 79 * 12;
  var starter = seats * 25 * 12;
  var pro = seats * 100 * 12;
  var api = seats * 25 * 12;
  var leadYr = lead ? Math.round(32.5 * 12) : 0;
  var engageYr = engage ? seats * 50 * 12 : 0;
  var growthTotal = growth + leadYr;
  var proBill = pro + engageYr;
  var proApiBill = pro + api + engageYr;
  if (premier) {
    proBill = Math.round(proBill * 1.3);
    proApiBill = Math.round(proApiBill * 1.3);
  }
  return {
    seats: seats,
    lead: lead,
    engage: engage,
    premier: premier,
    lite: lite,
    growth: growth,
    growthTotal: growthTotal,
    premium: premium,
    ultimate: ultimate,
    starter: starter,
    pro: pro,
    api: api,
    proApi: pro + api,
    leadYr: leadYr,
    engageYr: engageYr,
    proBill: proBill,
    proApiBill: proApiBill
  };
}

function psMoney(n) {
  return "$" + Math.round(n).toLocaleString("en-US");
}

function psLowestSentence(c) {
  var rows = [
    ["Salesforce Starter", c.starter],
    ["Pipedrive Growth", c.growthTotal],
    ["Pipedrive Premium", c.premium],
    ["Salesforce Pro", c.proBill],
    ["Pro plus API", c.proApiBill]
  ];
  var low = rows[0][1];
  rows.forEach(function (row) { if (row[1] < low) low = row[1]; });
  var lows = [];
  var rest = [];
  rows.forEach(function (row) {
    if (row[1] === low) lows.push(row[0]);
    else rest.push(row[0] + " " + psMoney(row[1]));
  });
  var tail = rest.length ? rest.join(". ") + ". " : "";
  return "Lowest Year-1 cost: " + lows.join(" and ") + ", " + psMoney(low) + ". " + tail + "Pipedrive Lite is " + psMoney(c.lite) + " and Ultimate is " + psMoney(c.ultimate) + ". Lite and Ultimate are list prices, not part of the five paths. Salesforce implementation is unknown and is not in these totals.";
}

function psRead() {
  return {
    seats: document.getElementById("ps-seats").value,
    leadbooster: document.getElementById("ps-lead").value === "yes",
    engagement: document.getElementById("ps-engage").value === "yes",
    premier: document.getElementById("ps-premier").value === "yes"
  };
}

function renderPipedriveSalesforce() {
  var c = calcPipedriveSalesforce(psRead());
  document.getElementById("ps-seats-val").textContent = String(c.seats);
  var bars = [
    ["shell-row-base", "shell-amt-base", "shell-title-base", "shell-sub-base", "Salesforce Starter", c.starter, "$25 per user per month"],
    ["shell-row-seats", "shell-amt-seats", "shell-title-seats", "shell-sub-seats", "Pipedrive Growth", c.growthTotal, c.lead ? "$39 annual plus LeadBooster" : "$39 per seat per month, annual"],
    ["shell-row-hidden", "shell-amt-hidden", "shell-title-hidden", "shell-sub-hidden", "Salesforce Pro", c.proBill, "Pro Suite license" + (c.engage ? " plus Sales Engagement" : "") + (c.premier ? " plus Premier Success" : "")]
  ];
  var maxBar = 1;
  bars.forEach(function (bar) { if (bar[5] > maxBar) maxBar = bar[5]; });
  bars.forEach(function (bar) {
    document.getElementById(bar[0]).style.flex = Math.max(12, Math.round(bar[5] / maxBar * 100)) + " 1 0px";
    document.getElementById(bar[1]).textContent = psMoney(bar[5]);
    document.getElementById(bar[2]).textContent = bar[4];
    document.getElementById(bar[3]).textContent = bar[6];
  });
  var line = psLowestSentence(c);
  var label = "Lowest Year-1 cost:";
  var lows = line.indexOf(",");
  var firstName = line.slice(label.length + 1, lows);
  document.getElementById("shell-product").textContent = firstName + ", " + c.seats + " seats";
  document.getElementById("shell-big").textContent = psMoney(c.starter < c.growthTotal && c.starter < c.premium && c.starter < c.proBill && c.starter < c.proApiBill ? c.starter : Math.min(c.starter, c.growthTotal, c.premium, c.proBill, c.proApiBill));
  document.getElementById("shell-best").innerHTML = "<strong>" + label + "</strong>" + line.slice(label.length);
  document.getElementById("shell-math").textContent = c.seats + " seats. Starter " + c.seats + " x $25 x 12 = " + psMoney(c.starter) + ". Growth " + c.seats + " x $39 x 12 = " + psMoney(c.growth) + (c.lead ? " plus LeadBooster " + psMoney(c.leadYr) : "") + ". Premium " + c.seats + " x $59 x 12 = " + psMoney(c.premium) + ". Pro " + c.seats + " x $100 x 12 = " + psMoney(c.pro) + ". API " + c.seats + " x $25 x 12 = " + psMoney(c.api) + ". Pro plus API " + psMoney(c.proApi) + ". Sales Engagement " + psMoney(c.engageYr) + ". Premier Success is 30% of the Pro fees in this model when it is on. Lite " + psMoney(c.lite) + ". Ultimate " + psMoney(c.ultimate) + ".";
  document.getElementById("shell-sub").textContent = "VAT extra. A negotiated discount is unknown. Implementation is unknown.";
  document.getElementById("shell-sticker").textContent = psMoney(c.starter) + " / yr";
  document.getElementById("shell-sticker-note").textContent = "Salesforce Starter license";
  var gap = c.proBill - c.starter;
  document.getElementById("shell-gap").textContent = (gap >= 0 ? "+" : "") + psMoney(gap);
  var labels = document.querySelectorAll("#shell-summary .summary-label");
  if (labels.length >= 2) {
    labels[0].textContent = "Starter Suite";
    labels[1].textContent = "Pro above Starter";
  }
  var notes = document.querySelectorAll("#shell-summary .summary-scenario");
  if (notes.length >= 2) notes[1].textContent = "Pro Suite license minus Starter";
  var body = "";
  [
    ["Salesforce Starter", "$25 per user per month", c.starter],
    ["Pipedrive Growth", c.lead ? "$39 annual plus LeadBooster $390" : "$39 per seat per month, annual", c.growthTotal],
    ["Pipedrive Premium", "$59 per seat per month, annual", c.premium],
    ["Salesforce Pro", "Pro Suite" + (c.engage ? " plus Sales Engagement" : "") + (c.premier ? " plus 30% Premier Success" : ""), c.proBill],
    ["Pro plus API", "$100 plus $25 API" + (c.engage ? " plus Sales Engagement" : "") + (c.premier ? " plus 30% Premier Success" : ""), c.proApiBill]
  ].forEach(function (row) {
    body += "<tr><td data-label=\"Path\">" + row[0] + "</td><td data-label=\"How it is priced\">" + row[1] + "</td><td data-label=\"Year-1\">" + psMoney(row[2]) + "</td></tr>";
  });
  document.getElementById("ps-tbody").innerHTML = body;
  var cta = document.getElementById("shell-cta");
  cta.setAttribute("rel", "sponsored nofollow noopener");
  cta.setAttribute("target", "_blank");
  if (typeof window.trackSaaSBillEvent === "function") {
    window.trackSaaSBillEvent("result_rendered", { page: "pipedrive-salesforce", seats: c.seats });
  }
}
["ps-seats", "ps-lead", "ps-engage", "ps-premier"].forEach(function (id) {
  var el = document.getElementById(id);
  el.addEventListener("input", renderPipedriveSalesforce);
  el.addEventListener("change", renderPipedriveSalesforce);
});
renderPipedriveSalesforce();
</script>
"""

FAQS = [
    (
        "What do 5 seats cost in Year 1 on the annual list?",
        "Checked 5 Nov 2026: Salesforce Starter Suite is $1,500, Pipedrive Growth is $2,340, Pipedrive Premium is $3,540, and Salesforce Pro Suite is $6,000. Pro Suite plus the $25 Web Services API is $7,500. Pipedrive Lite is $840 and Ultimate is $4,740. VAT is extra. Implementation is unknown.",
    ),
    (
        "Is the Salesforce API included in Pro Suite?",
        "No. The editions page prices the Web Services API at $25 per user per month on an annual term, and Pro Suite does not include it. Ten users are $15,000 for the year with the API, against $12,000 for Pro Suite seats alone.",
    ),
    (
        "Which Pipedrive names replaced Essential and Advanced?",
        "Pipedrive's plan article, updated 3 Sep 2026, maps Essential to Lite, Advanced to Growth, Professional and Power to Premium, and Enterprise to Ultimate. This page uses the new names.",
    ),
]


def copy_to_root(rel):
    src = os.path.join(PUBLIC_DIR, rel)
    dst = os.path.join(BASE_DIR, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src, dst)


def build():
    if len(TITLE) > 60:
        raise SystemExit("Title is %s chars: %s" % (len(TITLE), TITLE))
    if "\u2014" in TITLE or "\u2014" in REST or "\u2014" in DESCRIPTION:
        raise SystemExit("em dash in pipedrive salesforce copy")
    workbench = render_workbench(
        CONTROLS,
        controls_title="Your seats",
        chart_title="Year-1 license cost",
        cta_href="../../go/pipedrive/",
        cta_label="See Pipedrive pricing",
        cta_vendor="pipedrive",
    )
    workbench = workbench.replace(
        'href="../../go/pipedrive/" data-track="vendor-cta"',
        'href="../../go/pipedrive/" target="_blank" rel="sponsored nofollow noopener" data-track="vendor-cta"',
        1,
    )
    body = (
        "<section class=\"hero\">"
        "<h1>Pipedrive vs Salesforce Year-1 cost</h1>"
        "<p class=\"lead\">Annual list prices for Salesforce Starter Suite and Pro Suite next to Pipedrive. Implementation stays unknown.</p>"
        "</section>"
        + workbench
        + REST
    )
    if "salesforce.com" in workbench and "btn-cta" in workbench.split("salesforce.com")[0][-200:]:
        raise SystemExit("Salesforce affiliate CTA")
    render_page(
        REL,
        TITLE,
        DESCRIPTION,
        CANONICAL,
        wrap_calculator_shell(body),
        faqs=FAQS,
        published_date="2026-11-05",
    )
    copy_to_root(REL)


if __name__ == "__main__":
    build()
