"""Jotform Year-1 cost for a small team: separate accounts versus Enterprise.

Checked 2026-11-15 on Jotform pricing, the teams pricing page, the Enterprise
FAQ, two Jotform staff answers, and the HIPAA page. The Enterprise price stays
unknown until someone types a quote. The Jotform link is the pricing URL in
data/affiliate_links.json.
"""
import json
import os
import shutil

from layout import BASE_DIR, DATA_DIR, PUBLIC_DIR, render_page, render_workbench, wrap_calculator_shell

TITLE = "Jotform Year-1 cost, team of 3 to 4 – saasbill.io"
DESCRIPTION = "Year-1 cost of separate Jotform accounts versus an Enterprise quote. Checked 15 Nov 2026."
CANONICAL = "/pricing/jotform-multi-user-vs-enterprise-year-1-cost/"
REL = "pricing/jotform-multi-user-vs-enterprise-year-1-cost/index.html"
LEAD = (
    "Standard plans run on shared servers with online support. "
    "Enterprise runs on a dedicated server, and the customer signs an agreement."
)
FORMULA_DEFAULT = (
    "4 people. Annual billing. HIPAA is off. Discount is off. "
    "One Gold account is $1,188. "
    "4 separate Gold accounts are 4 times $1,188, which is $4,752. "
    "Enterprise quote is unknown."
)
BREAK_EVEN_DEFAULT = "Enterprise is cheaper only if the quote is below $4,752."

with open(os.path.join(DATA_DIR, "affiliate_links.json"), encoding="utf-8") as handle:
    JOTFORM_PRICING = json.load(handle)["jotform"]["custom_links"]["pricing"]

CONTROLS = r"""
        <div class="wb-control-item">
          <label class="wb-control-label" for="jf-team">People <span class="val-pill" id="jf-team-val">4</span></label>
          <div class="wb-slider-row">
            <input type="range" id="jf-team" min="1" max="10" step="1" value="4" aria-label="Number of people" data-track="calculator-control" data-control="team" />
          </div>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="jf-billing">Billing</label>
          <select id="jf-billing" class="wb-tool-select" data-track="calculator-control" data-control="billing">
            <option value="annual" selected>Annual</option>
            <option value="monthly">Month to month</option>
          </select>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="jf-hipaa">Needs HIPAA</label>
          <select id="jf-hipaa" class="wb-tool-select" data-track="calculator-control" data-control="hipaa">
            <option value="no" selected>No</option>
            <option value="yes">Yes</option>
          </select>
          <p class="wb-budget-subnote">Yes uses Gold.</p>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="jf-plan">Plan for separate accounts</label>
          <select id="jf-plan" class="wb-tool-select" data-track="calculator-control" data-control="plan">
            <option value="bronze">Bronze</option>
            <option value="silver">Silver</option>
            <option value="gold" selected>Gold</option>
          </select>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="jf-quote">Enterprise quote per year</label>
          <input type="text" inputmode="decimal" class="wb-tool-select" id="jf-quote" autocomplete="off" aria-label="Enterprise quote per year" data-track="calculator-control" data-control="enterprise-quote" />
          <p class="wb-budget-subnote">Leave this blank when you have no quote.</p>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="jf-discount">Nonprofit or education discount</label>
          <select id="jf-discount" class="wb-tool-select" data-track="calculator-control" data-control="discount">
            <option value="no" selected>No</option>
            <option value="yes">Yes, I qualify</option>
          </select>
          <p class="wb-budget-subnote">Only if you qualify. 50% off Bronze, Silver, and Gold. Enterprise is 30% off user fees only, so a quote you type is left as you typed it.</p>
        </div>
"""

REST = r"""
<section id="jf-costs">
  <h2>Year-1 cost</h2>
  <div class="table-wrap editorial-gap-table mobile-cards">
    <table>
      <caption>Twelve months at the list price for the numbers above. An empty Enterprise quote stays unknown.</caption>
      <thead>
        <tr>
          <th>Plan</th>
          <th>Year 1</th>
        </tr>
      </thead>
      <tbody id="jf-body">
        <tr><td data-label="Plan">One Gold account</td><td data-label="Year 1">$1,188</td></tr>
        <tr><td data-label="Plan">4 separate Gold accounts</td><td data-label="Year 1">$4,752</td></tr>
        <tr><td data-label="Plan">Enterprise</td><td data-label="Year 1">unknown</td></tr>
      </tbody>
    </table>
  </div>
  <p id="jf-collab">Separate accounts mean separate forms and submissions for each person. Those people can use Form Collaboration, and they can share data through Jotform Tables. Enterprise is one shared workspace.</p>
  <p class="paid-partnership-note">Paid partnership with Jotform (#JotformPartner)</p>
  <div class="cta-stack">
    <a class="btn-cta" href="__JOTFORM_PRICING__" target="_blank" rel="sponsored nofollow noopener" data-track="vendor-cta" data-vendor="jotform" data-cta-location="subpage-summary">Jotform pricing &rarr;</a>
  </div>
</section>

<section>
  <h2>Plan prices and limits</h2>
  <div class="table-wrap editorial-gap-table mobile-cards">
    <table>
      <caption>List prices checked 15 Nov 2026. Monthly Year-1 totals are the monthly rate times 12.</caption>
      <thead>
        <tr>
          <th>Plan</th>
          <th>One account</th>
          <th>HIPAA features</th>
          <th>Limits</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td data-label="Plan">Starter</td>
          <td data-label="One account">Free</td>
          <td data-label="HIPAA features">Unavailable</td>
          <td data-label="Limits">1 user</td>
        </tr>
        <tr>
          <td data-label="Plan">Bronze</td>
          <td data-label="One account">$408 a year ($34 a month, billed annually) or $468 a year ($39 a month)</td>
          <td data-label="HIPAA features">Unavailable</td>
          <td data-label="Limits">1 user. 25 forms, 1,000 submissions a month</td>
        </tr>
        <tr>
          <td data-label="Plan">Silver</td>
          <td data-label="One account">$468 a year ($39 a month, billed annually) or $588 a year ($49 a month)</td>
          <td data-label="HIPAA features">Unavailable</td>
          <td data-label="Limits">1 user. 50 forms, 2,500 submissions a month</td>
        </tr>
        <tr>
          <td data-label="Plan">Gold</td>
          <td data-label="One account">$1,188 a year ($99 a month, billed annually) or $1,548 a year ($129 a month)</td>
          <td data-label="HIPAA features">Available</td>
          <td data-label="Limits">1 user. 100 forms, 10,000 submissions a month, 100 GB</td>
        </tr>
        <tr>
          <td data-label="Plan">Enterprise</td>
          <td data-label="One account">unknown</td>
          <td data-label="HIPAA features">Available</td>
          <td data-label="Limits">Unlimited forms and submissions. Multi-user platform, user management, SSO, SLA, data residency, and professional services.</td>
        </tr>
      </tbody>
    </table>
  </div>
</section>

<section>
  <h2>What applies to a team</h2>
  <ul class="key-list">
    <li>A standard plan has a 30-day money-back guarantee: a full refund if you cancel within 30 days of payment. You can cancel at any time. It is a recurring subscription.</li>
    <li>Enterprise has no month-to-month price. Fees for the whole term are paid up front. There is no trial and no refund. Users added during the term are prorated.</li>
    <li>Jotform staff say a standard plan cannot add seats, and sharing a login is against the Terms of Use. Enterprise requires a unique person and email for each user, does not allow group aliases, includes up to 5 users in the base package, and sells extra users in bundles of 5. <span class="src-cluster"><a class="src-link" href="https://www.jotform.com/answers/34688901-inquiry-about-multi-user-organizational-account-options" target="_blank" rel="noopener">Jotform staff answer on multi-user accounts</a> <span class="src-date">Accessed 15 Nov 2026.</span></span> <span class="src-cluster"><a class="src-link" href="https://www.jotform.com/answers/35726381-adding-another-user-to-license" target="_blank" rel="noopener">Jotform staff answer on adding a user</a> <span class="src-date">Accessed 15 Nov 2026.</span></span></li>
    <li>HIPAA features are unavailable on Starter, Bronze, and Silver, and available on Gold and Enterprise. Eligible customers with HIPAA features enabled can sign a BAA with Jotform.</li>
    <li>On a HIPAA server, administrators only see submission data that was explicitly shared with them. The HIPAA server add-on price, and any extra BAA or HIPAA fee on Enterprise, are unknown.</li>
    <li>Whether several separate individual accounts are fine in practice when an organization wants shared data is unknown.</li>
    <li>On Reddit, a small team asked why they cannot have separate individual accounts. This page uses only that question. <span class="src-cluster"><a class="src-link" href="https://www.reddit.com/r/jotform/comments/1w0ud3g/why_cant_a_small_team_have_separate_individual/" target="_blank" rel="noopener">Reddit thread</a> <span class="src-date">Accessed 15 Nov 2026.</span></span></li>
  </ul>
</section>

<p class="summary-caveat">Checked 15 Nov 2026. <span class="src-cluster"><a class="src-link" href="https://www.jotform.com/pricing/" target="_blank" rel="noopener">Jotform pricing</a> <span class="src-date">Accessed 15 Nov 2026.</span></span> <span class="src-cluster"><a class="src-link" href="https://www.jotform.com/teams/pricing/" target="_blank" rel="noopener">Jotform teams pricing</a> <span class="src-date">Accessed 15 Nov 2026.</span></span> <span class="src-cluster"><a class="src-link" href="https://www.jotform.com/enterprise/faq/" target="_blank" rel="noopener">Jotform Enterprise FAQ</a> <span class="src-date">Accessed 15 Nov 2026.</span></span> <span class="src-cluster"><a class="src-link" href="https://www.jotform.com/hipaa/" target="_blank" rel="noopener">Jotform HIPAA</a> <span class="src-date">Accessed 15 Nov 2026.</span></span></p>
""".replace("__JOTFORM_PRICING__", JOTFORM_PRICING)

SCRIPT = r"""
<script>
var JF_PLAN_BEFORE_HIPAA = "gold";

function calcJotformTeam(input) {
  var team = Math.round(Number(input.team));
  if (!isFinite(team)) team = 4;
  team = Math.max(1, Math.min(10, team));
  var billing = input.billing === "monthly" ? "monthly" : "annual";
  var hipaa = input.hipaa === "yes";
  var plan = input.plan === "bronze" || input.plan === "silver" ? input.plan : "gold";
  if (hipaa) plan = "gold";
  var discount = input.discount === "yes";
  var rates = {
    bronze: { name: "Bronze", annual: 40800, monthlyYear: 46800, month: 3900 },
    silver: { name: "Silver", annual: 46800, monthlyYear: 58800, month: 4900 },
    gold: { name: "Gold", annual: 118800, monthlyYear: 154800, month: 12900 }
  };
  var picked = rates[plan];
  var one = billing === "annual" ? picked.annual : picked.monthlyYear;
  var monthEach = picked.month;
  if (discount) {
    one = Math.round(one / 2);
    monthEach = Math.round(monthEach / 2);
  }
  var quote = jfQuoteCents(input.quote);
  return {
    team: team,
    billing: billing,
    hipaa: hipaa,
    plan: plan,
    planName: picked.name,
    discount: discount,
    one: one,
    monthEach: monthEach,
    separate: one * team,
    quote: quote
  };
}

function jfQuoteCents(raw) {
  if (raw === null || raw === undefined) return null;
  var text = String(raw).replace(/[$,\s]/g, "");
  if (!text) return null;
  if (!/^\d+(\.\d\d?)?$/.test(text)) return null;
  var parts = text.split(".");
  var dollars = parseInt(parts[0], 10);
  var cents = 0;
  if (parts.length === 2) {
    var frac = parts[1];
    if (frac.length === 1) frac += "0";
    cents = parseInt(frac, 10);
  }
  var total = dollars * 100 + cents;
  if (!isFinite(total) || total <= 0) return null;
  return total;
}

function jfMoney(cents) {
  if (cents === null) return "unknown";
  var v = Math.round(cents);
  var neg = v < 0;
  v = Math.abs(v);
  var dollars = Math.floor(v / 100);
  var rem = v % 100;
  var text = String(dollars);
  var grouped = "";
  while (text.length > 3) {
    grouped = "," + text.slice(-3) + grouped;
    text = text.slice(0, -3);
  }
  var out = "$" + text + grouped;
  if (rem) out += "." + (rem < 10 ? "0" : "") + rem;
  return neg ? "-" + out : out;
}

function jfAccountWord(team) {
  return team === 1 ? "account" : "accounts";
}

function jfFormula(c) {
  var word = jfAccountWord(c.team);
  var verb = c.team === 1 ? "is" : "are";
  var parts = [];
  parts.push(c.team + (c.team === 1 ? " person." : " people."));
  parts.push(c.billing === "annual" ? "Annual billing." : "Month-to-month billing.");
  parts.push(c.hipaa ? "HIPAA is on." : "HIPAA is off.");
  parts.push(c.discount ? "Nonprofit or education discount is on." : "Discount is off.");
  if (c.billing === "annual") {
    parts.push("One " + c.planName + " account is " + jfMoney(c.one) + ".");
    parts.push(c.team + " separate " + c.planName + " " + word + " " + verb + " " + c.team + " times " + jfMoney(c.one) + ", which is " + jfMoney(c.separate) + ".");
  } else {
    parts.push("One " + c.planName + " account is " + jfMoney(c.monthEach) + " a month.");
    parts.push(c.team + " separate " + c.planName + " " + word + " " + verb + " " + c.team + " times " + jfMoney(c.monthEach) + " times 12, which is " + jfMoney(c.separate) + ".");
  }
  parts.push(c.quote === null ? "Enterprise quote is unknown." : "Enterprise quote is " + jfMoney(c.quote) + ".");
  return parts.join(" ");
}

function jfBreakEven(c) {
  return "Enterprise is cheaper only if the quote is below " + jfMoney(c.separate) + ".";
}

function renderJotformTeam(event) {
  var hipaaEl = document.getElementById("jf-hipaa");
  var planEl = document.getElementById("jf-plan");
  if (event && event.target && event.target.id === "jf-plan" && hipaaEl.value !== "yes") {
    JF_PLAN_BEFORE_HIPAA = planEl.value;
  }
  if (event && event.target && event.target.id === "jf-hipaa") {
    if (hipaaEl.value === "yes") {
      if (planEl.value === "bronze" || planEl.value === "silver") JF_PLAN_BEFORE_HIPAA = planEl.value;
      planEl.value = "gold";
    } else if (JF_PLAN_BEFORE_HIPAA === "bronze" || JF_PLAN_BEFORE_HIPAA === "silver" || JF_PLAN_BEFORE_HIPAA === "gold") {
      planEl.value = JF_PLAN_BEFORE_HIPAA;
    }
  }
  planEl.disabled = hipaaEl.value === "yes";
  if (hipaaEl.value === "yes") planEl.value = "gold";
  var c = calcJotformTeam({
    team: document.getElementById("jf-team").value,
    billing: document.getElementById("jf-billing").value,
    hipaa: hipaaEl.value,
    plan: planEl.value,
    quote: document.getElementById("jf-quote").value,
    discount: document.getElementById("jf-discount").value
  });
  document.getElementById("jf-team-val").textContent = String(c.team);
  var word = jfAccountWord(c.team);
  var separateName = c.team + " separate " + c.planName + " " + word;
  var oneName = "One " + c.planName + " account";
  var showEnterprise = c.quote !== null && c.quote < c.separate;
  document.getElementById("shell-product").textContent = showEnterprise ? "Enterprise" : separateName;
  document.getElementById("shell-big").textContent = jfMoney(showEnterprise ? c.quote : c.separate);
  document.getElementById("shell-sub").textContent = "";
  document.getElementById("shell-best").textContent = jfBreakEven(c);
  var bars = [
    { row: "shell-row-base", amt: "shell-amt-base", cents: c.one },
    { row: "shell-row-seats", amt: "shell-amt-seats", cents: c.separate },
    { row: "shell-row-hidden", amt: "shell-amt-hidden", cents: c.quote }
  ];
  document.getElementById("shell-title-base").textContent = oneName;
  document.getElementById("shell-title-seats").textContent = separateName;
  document.getElementById("shell-title-hidden").textContent = "Enterprise";
  document.getElementById("shell-sub-base").textContent = "Year 1";
  document.getElementById("shell-sub-seats").textContent = "Year 1";
  document.getElementById("shell-sub-hidden").textContent = "Quote";
  var maxCents = 1;
  bars.forEach(function (bar) {
    if (bar.cents !== null && bar.cents > maxCents) maxCents = bar.cents;
  });
  bars.forEach(function (bar) {
    var known = bar.cents !== null;
    var share = known ? (Math.round(bar.cents / maxCents * 1000) / 10) : 0;
    document.getElementById(bar.amt).textContent = known ? jfMoney(bar.cents) : "unknown";
    document.getElementById(bar.row).style.setProperty("--wb-bar-share", share + "%");
  });
  var rows = [
    { name: oneName, text: jfMoney(c.one) },
    { name: separateName, text: jfMoney(c.separate) },
    { name: "Enterprise", text: c.quote === null ? "unknown" : jfMoney(c.quote) }
  ];
  var html = "";
  rows.forEach(function (row) {
    html += "<tr><td data-label=\"Plan\">" + row.name + "</td><td data-label=\"Year 1\">" + row.text + "</td></tr>";
  });
  document.getElementById("jf-body").innerHTML = html;
  document.getElementById("shell-math").textContent = jfFormula(c);
}

["jf-team", "jf-billing", "jf-hipaa", "jf-plan", "jf-quote", "jf-discount"].forEach(function (id) {
  var el = document.getElementById(id);
  el.addEventListener("input", renderJotformTeam);
  el.addEventListener("change", renderJotformTeam);
});
renderJotformTeam();
</script>
"""


def copy_to_root(rel):
    src = os.path.join(PUBLIC_DIR, rel)
    dst = os.path.join(BASE_DIR, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src, dst)


def build():
    if len(TITLE) > 60:
        raise SystemExit("Title is %s chars: %s" % (len(TITLE), TITLE))
    if "partner=" not in JOTFORM_PRICING:
        raise SystemExit("Jotform pricing URL is missing the partner id")
    blob = TITLE + DESCRIPTION + LEAD + CONTROLS + REST + FORMULA_DEFAULT + BREAK_EVEN_DEFAULT + SCRIPT
    for banned in ("\u2014", "Best option", "Best choice", "Winner", "SaaSTruth", "answer first", "test section", "placeholder"):
        if banned.lower() in blob.lower():
            raise SystemExit("banned copy: " + banned)
    if LEAD.count(LEAD) != 1:
        raise SystemExit("lead repeated in the source")
    workbench = render_workbench(
        CONTROLS,
        controls_title="Your team",
        chart_title="Year-1 cost",
        cta_href="#jf-costs",
        cta_label="Cost table",
        cta_vendor="saasbill",
    )
    for old, new in (
        ('class="wb-vbar-container"', 'class="wb-vbar-container wb-vbar-separate"'),
        ('id="shell-row-base" style="flex: 40 1 0px;"', 'id="shell-row-base" style="--wb-bar-share: 25%;"'),
        ('id="shell-row-seats" style="flex: 8 1 0px;"', 'id="shell-row-seats" style="--wb-bar-share: 100%;"'),
        ('id="shell-row-hidden" style="flex: 52 1 0px;"', 'id="shell-row-hidden" style="--wb-bar-share: 0%;"'),
        ('id="shell-product">Year-1 total<', 'id="shell-product">4 separate Gold accounts<'),
        ('id="shell-big">$0<', 'id="shell-big">$4,752<'),
        ('id="shell-sub">Matches advertised price ($0 hidden fees).</p>', 'id="shell-sub"></p>'),
        ('id="shell-title-base">Sticker Price<', 'id="shell-title-base">One Gold account<'),
        ('id="shell-sub-base">Advertised price<', 'id="shell-sub-base">Year 1<'),
        ('id="shell-amt-base">$0<', 'id="shell-amt-base">$1,188<'),
        ('id="shell-title-seats">Other sticker fees<', 'id="shell-title-seats">4 separate Gold accounts<'),
        ('id="shell-sub-seats">Included in the sticker<', 'id="shell-sub-seats">Year 1<'),
        ('id="shell-amt-seats">$0<', 'id="shell-amt-seats">$4,752<'),
        ('id="shell-title-hidden">Hidden Cost Gap<', 'id="shell-title-hidden">Enterprise<'),
        ('id="shell-sub-hidden">Fees above the advertised price<', 'id="shell-sub-hidden">Quote<'),
        ('id="shell-amt-hidden">$0<', 'id="shell-amt-hidden">unknown<'),
        ('id="shell-best"></div>', 'id="shell-best">%s</div>' % BREAK_EVEN_DEFAULT),
        ('<div class="math-drawer-body" id="shell-math"></div>', '<div class="math-drawer-body" id="shell-math">%s</div>' % FORMULA_DEFAULT),
    ):
        if old not in workbench:
            raise SystemExit("missing workbench fallback: " + old)
        workbench = workbench.replace(old, new, 1)
    start = workbench.find('<section class="verdict-section"')
    end = workbench.find("</section>", start)
    if start < 0 or end < 0:
        raise SystemExit("missing summary strip")
    workbench = workbench[:start] + workbench[end + len("</section>"):]
    if "$0" in workbench:
        raise SystemExit("workbench still shows $0")
    body = (
        '<section class="hero">'
        "<h1>What does Jotform cost in Year 1 for a team of 3 to 4?</h1>"
        '<p class="lead">%s</p>' % LEAD
        + "</section>"
        + workbench
        + REST
        + SCRIPT
    )
    if body.count(LEAD) != 1:
        raise SystemExit("lead repeated before render")
    render_page(
        REL,
        TITLE,
        DESCRIPTION,
        CANONICAL,
        wrap_calculator_shell(body),
        faqs=None,
        published_date="2026-11-15",
        modified_datetime="2026-11-15T00:00:00+00:00",
        show_affiliate_note=True,
    )
    copy_to_root(REL)


if __name__ == "__main__":
    build()
