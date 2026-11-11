"""SSO tax calculator: app plan step-ups, plus IdP and vault context.

Sources checked 2026-11-06. Unknown stays the word unknown.
Okta Workforce includes SSO from Starter. WorkOS bills per IdP connection.
1Password Business unlocks with OIDC SSO. It is not an IdP and it does not
offer a HIPAA BAA. No affiliate redirect.
"""
import os
import shutil

from layout import BASE_DIR, PUBLIC_DIR, render_page, render_workbench, wrap_calculator_shell

TITLE = "SSO tax: Okta, WorkOS, 1Password – saasbill.io"
DESCRIPTION = (
    "At 25 people, the SAML step-up is $1,251 a year on Zoom and $3,000 on Notion. "
    "Okta Starter already includes SSO and is $1,800. Checked 6 Nov 2026."
)
REL = "compliance/okta-vs-workos-vs-1password-sso-tax-calculator/index.html"
CANONICAL = "/compliance/okta-vs-workos-vs-1password-sso-tax-calculator/"

CONTROLS = """
        <div class="wb-control-item">
          <label class="wb-control-label" for="ss-users">People on the app <span class="val-pill" id="ss-users-val">25</span></label>
          <div class="wb-slider-row">
            <input type="range" id="ss-users" min="0" max="3" step="1" value="1" aria-label="Team size" data-track="calculator-control" data-control="users" />
          </div>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="ss-conn">WorkOS production connections <span class="val-pill" id="ss-conn-val">5</span></label>
          <div class="wb-slider-row">
            <input type="range" id="ss-conn" min="1" max="40" step="1" value="5" aria-label="WorkOS connections" data-track="calculator-control" data-control="connections" />
          </div>
        </div>
        <p class="wb-budget-subnote">WorkOS is priced per IdP connection, not per person. The per-person figure below only divides that connection bill by the team size.</p>
"""

REST = r"""
<section id="ss-apps">
  <h2>What the apps charge to turn SAML on</h2>
  <p>These are the extra dollars for the same people when the plan that includes SAML costs more than the plan below it. Slack's US step-up is unknown because the Pro price in US dollars was not re-checked on 6 Nov 2026.</p>
  <div class="table-wrap editorial-gap-table mobile-cards">
    <table>
      <caption>Year-1 list price and the step-up for SAML, at the team size above</caption>
      <thead>
        <tr>
          <th>App</th>
          <th>Without SAML</th>
          <th>With SAML</th>
          <th>Year-1 step-up</th>
        </tr>
      </thead>
      <tbody id="ss-apps-body">
        <tr><td data-label="App">Notion</td><td data-label="Without SAML">Plus $10</td><td data-label="With SAML">Business $20</td><td data-label="Year-1 step-up">$3,000</td></tr>
        <tr><td data-label="App">Zoom</td><td data-label="Without SAML">Pro $14.16</td><td data-label="With SAML">Business $18.33</td><td data-label="Year-1 step-up">$1,251</td></tr>
        <tr><td data-label="App">GitHub</td><td data-label="Without SAML">Team $4</td><td data-label="With SAML">Enterprise $21</td><td data-label="Year-1 step-up">$5,100</td></tr>
        <tr><td data-label="App">Figma</td><td data-label="Without SAML">Professional $16</td><td data-label="With SAML">Organization $55</td><td data-label="Year-1 step-up">$11,700</td></tr>
        <tr><td data-label="App">Slack</td><td data-label="Without SAML">Pro, US dollars unknown</td><td data-label="With SAML">Business+ $15</td><td data-label="Year-1 step-up">unknown</td></tr>
      </tbody>
    </table>
  </div>
  <p class="summary-caveat">Slack also publishes a euro pair, Pro €6.75 to Business+ €15 per active user per month. That pair is not converted into the dollar totals.</p>
</section>

<section id="ss-context">
  <h2>IdP and vault, which are different bills</h2>
  <div class="table-wrap editorial-gap-table mobile-cards">
    <table>
      <caption>Year-1 context at the team size and connection count above</caption>
      <thead>
        <tr>
          <th>Product</th>
          <th>What you are buying</th>
          <th>Year-1</th>
        </tr>
      </thead>
      <tbody id="ss-context-body">
        <tr><td data-label="Product">Okta Starter</td><td data-label="What you are buying">IdP. SSO is included.</td><td data-label="Year-1">$1,800</td></tr>
        <tr><td data-label="Product">WorkOS SSO</td><td data-label="What you are buying">5 connections at $125 each</td><td data-label="Year-1">$7,500</td></tr>
        <tr><td data-label="Product">1Password Business</td><td data-label="What you are buying">Vault. Unlock with SSO is OIDC.</td><td data-label="Year-1">$2,697</td></tr>
      </tbody>
    </table>
  </div>
  <p id="ss-split" class="summary-caveat">Five WorkOS connections are $7,500 a year. Divided by 25 people, that is $300 a person for the year. WorkOS does not publish a per-person SSO price.</p>
</section>

<section>
  <h2>Prices checked on 6 Nov 2026</h2>
  <div class="table-wrap editorial-gap-table mobile-cards">
    <table>
      <caption>Published list prices. Inquire and quote-only rows stay unknown.</caption>
      <thead>
        <tr>
          <th>Item</th>
          <th>Published price</th>
          <th>In the Year-1 totals</th>
        </tr>
      </thead>
      <tbody>
        <tr><td data-label="Item">Okta Starter</td><td data-label="Published price">$6 per user per month. SSO, MFA, Universal Directory, and 5 Workflows are included.</td><td data-label="In the Year-1 totals">Seat price times 12, or the $1,500 Workforce Identity floor, whichever is higher.</td></tr>
        <tr><td data-label="Item">Okta Core Essentials and Essentials</td><td data-label="Published price">$14 and $17 per user per month.</td><td data-label="In the Year-1 totals">Shown beside Starter. The same $1,500 floor applies.</td></tr>
        <tr><td data-label="Item">Okta Professional and Enterprise</td><td data-label="Published price">Inquire.</td><td data-label="In the Year-1 totals">unknown</td></tr>
        <tr><td data-label="Item">Okta standalone SSO</td><td data-label="Published price">Not listed as a public dollar amount on the pricing page.</td><td data-label="In the Year-1 totals">unknown</td></tr>
        <tr><td data-label="Item">Okta Customer Identity Enterprise</td><td data-label="Published price">$3,000 per month, billed annually. A separate product line.</td><td data-label="In the Year-1 totals">$36,000. Not added to the Workforce seat total.</td></tr>
        <tr><td data-label="Item">WorkOS AuthKit</td><td data-label="Published price">First 1 million monthly active users included. Each further 1 million is $2,500 per month. Includes enterprise SSO from one integration.</td><td data-label="In the Year-1 totals">Included while you stay under 1 million. Not a per-person SSO fee.</td></tr>
        <tr><td data-label="Item">WorkOS SSO connections</td><td data-label="Published price">Per connection per month: 1 to 15 at $125, 16 to 30 at $100, 31 to 50 at $80, 51 to 100 at $65, 101 and above is custom.</td><td data-label="In the Year-1 totals">Connection count times the tier price times 12. Above 100 connections: unknown.</td></tr>
        <tr><td data-label="Item">WorkOS Directory Sync</td><td data-label="Published price">The same per-connection ladder.</td><td data-label="In the Year-1 totals">Not added. Turning it on would be a second ladder, not a per-person fee.</td></tr>
        <tr><td data-label="Item">WorkOS support</td><td data-label="Published price">Staging has no production charge. Scale support is $1,000 per month. Enterprise support is custom.</td><td data-label="In the Year-1 totals">Scale support is $12,000 a year and is not in the connection total. Enterprise support is unknown.</td></tr>
        <tr><td data-label="Item">1Password Teams Starter Pack</td><td data-label="Published price">$24.95 per month for 10 members, billed annually. The page also lists $2.49 per user. Unlock with SSO is not included.</td><td data-label="In the Year-1 totals">$299.40 for that 10-member pack. Not scaled to the team slider.</td></tr>
        <tr><td data-label="Item">1Password Business</td><td data-label="Published price">$8.99 per user per month, billed yearly ($107.88 per user per year). Unlock with SSO is included, and it is OIDC, not SAML. IdP provisioning covers Okta, Entra, and others.</td><td data-label="In the Year-1 totals">The vault line. It does not replace an IdP.</td></tr>
        <tr><td data-label="Item">1Password Enterprise and SaaS Manager SAML</td><td data-label="Published price">Quote only.</td><td data-label="In the Year-1 totals">unknown</td></tr>
        <tr><td data-label="Item">1Password HIPAA BAA</td><td data-label="Published price">1Password does not offer a HIPAA BAA.</td><td data-label="In the Year-1 totals">Not a priced add-on.</td></tr>
      </tbody>
    </table>
  </div>
  <p class="src-cluster"><a class="src-link" href="https://www.okta.com/pricing/">Okta pricing</a> <span class="src-date">Accessed 2026-11-06</span></p>
  <p class="src-cluster"><a class="src-link" href="https://workos.com/pricing">WorkOS pricing</a> <span class="src-date">Accessed 2026-11-06</span></p>
  <p class="src-cluster"><a class="src-link" href="https://1password.com/pricing/business" target="_blank" rel="noopener">1Password Business pricing</a> <span class="src-date">Accessed 2026-11-06</span></p>
  <p class="src-cluster"><a class="src-link" href="https://1password.com/pricing/enterprise" target="_blank" rel="noopener">1Password Enterprise pricing</a> <span class="src-date">Accessed 2026-11-06</span></p>
  <p class="src-cluster"><a class="src-link" href="https://www.notion.com/pricing">Notion pricing</a> <span class="src-date">Accessed 2026-11-06</span></p>
  <p class="src-cluster"><a class="src-link" href="https://zoom.us/pricing">Zoom pricing</a> <span class="src-date">Accessed 2026-11-06</span></p>
  <p class="src-cluster"><a class="src-link" href="https://github.com/pricing">GitHub pricing</a> <span class="src-date">Accessed 2026-11-06</span></p>
  <p class="src-cluster"><a class="src-link" href="https://www.figma.com/pricing/">Figma pricing</a> <span class="src-date">Accessed 2026-11-06</span></p>
  <p class="src-cluster"><a class="src-link" href="https://slack.com/pricing">Slack pricing</a> <span class="src-date">Accessed 2026-11-06</span></p>
  <p class="src-cluster"><a class="src-link" href="https://slack.com/help/articles/203772216-Set-up-SAML-single-sign-on-for-Slack">Slack SAML setup</a> <span class="src-date">Accessed 2026-11-06</span></p>
</section>
<script>
var SS_USERS = [10, 25, 50, 100];

function ssWorkosRate(connections) {
  if (connections < 1) return -1;
  if (connections <= 15) return 125;
  if (connections <= 30) return 100;
  if (connections <= 50) return 80;
  if (connections <= 100) return 65;
  return -1;
}

function ssYearFloor(centsPerUserMonth, users) {
  var seats = users * centsPerUserMonth * 12;
  return seats > 150000 ? seats : 150000;
}

function calcSsoTax(input) {
  var idx = Math.max(0, Math.min(3, Math.round(Number(input.usersIndex) || 0)));
  var users = SS_USERS[idx];
  var connections = Math.max(1, Math.round(Number(input.connections) || 1));
  var rate = ssWorkosRate(connections);
  var workos = rate < 0 ? -1 : connections * rate * 12 * 100;
  var notionLow = users * 1000 * 12;
  var notionHigh = users * 2000 * 12;
  var zoomLow = users * 1416 * 12;
  var zoomHigh = users * 1833 * 12;
  var githubLow = users * 400 * 12;
  var githubHigh = users * 2100 * 12;
  var figmaLow = users * 1600 * 12;
  var figmaHigh = users * 5500 * 12;
  var slackHigh = users * 1500 * 12;
  return {
    users: users,
    connections: connections,
    rate: rate,
    oktaStarter: ssYearFloor(600, users),
    oktaCore: ssYearFloor(1400, users),
    oktaEssentials: ssYearFloor(1700, users),
    workos: workos,
    password: users * 899 * 12,
    notionLow: notionLow,
    notionHigh: notionHigh,
    notionDelta: notionHigh - notionLow,
    zoomLow: zoomLow,
    zoomHigh: zoomHigh,
    zoomDelta: zoomHigh - zoomLow,
    githubLow: githubLow,
    githubHigh: githubHigh,
    githubDelta: githubHigh - githubLow,
    figmaLow: figmaLow,
    figmaHigh: figmaHigh,
    figmaDelta: figmaHigh - figmaLow,
    slackHigh: slackHigh
  };
}

function ssMoney(cents) {
  var negative = cents < 0;
  var v = Math.abs(Math.round(cents));
  var dollars = Math.floor(v / 100);
  var rest = v % 100;
  var text = "$" + dollars.toLocaleString("en-US");
  if (rest) text += "." + (rest < 10 ? "0" : "") + rest;
  return (negative ? "-" : "") + text;
}

function ssLowestApps(c) {
  var rows = [
    ["Zoom", c.zoomDelta],
    ["Notion", c.notionDelta],
    ["GitHub", c.githubDelta],
    ["Figma", c.figmaDelta]
  ];
  var low = rows[0][1];
  rows.forEach(function (row) { if (row[1] < low) low = row[1]; });
  var lows = [];
  var rest = [];
  rows.forEach(function (row) {
    if (row[1] === low) lows.push(row[0]);
    else rest.push(row[0] + " " + ssMoney(row[1]));
  });
  var tail = rest.length ? rest.join(". ") + ". " : "";
  return "Lowest Year-1 cost: " + lows.join(" and ") + ", " + ssMoney(low) + ". " + tail + "That is the smallest published step-up to the plan that includes SAML. Slack's US dollar step-up is unknown.";
}

function ssRead() {
  return {
    usersIndex: document.getElementById("ss-users").value,
    connections: document.getElementById("ss-conn").value
  };
}

function renderSsoTax() {
  var c = calcSsoTax(ssRead());
  document.getElementById("ss-users-val").textContent = String(c.users);
  document.getElementById("ss-conn-val").textContent = String(c.connections);
  var line = ssLowestApps(c);
  var label = "Lowest Year-1 cost:";
  document.getElementById("shell-best").innerHTML = "<strong>" + label + "</strong>" + line.slice(label.length);
  document.getElementById("shell-big").textContent = ssMoney(c.zoomDelta);
  document.getElementById("shell-product").textContent = "Zoom SAML step-up, " + c.users + " people";
  document.getElementById("shell-sub").textContent = "App plan step-up only. Okta, WorkOS, and 1Password are separate bills.";
  var bars = [
    ["shell-row-base", "shell-amt-base", "shell-title-base", "shell-sub-base", "Zoom step-up", c.zoomDelta, "Pro to Business, annual"],
    ["shell-row-seats", "shell-amt-seats", "shell-title-seats", "shell-sub-seats", "Notion step-up", c.notionDelta, "Plus to Business"],
    ["shell-row-hidden", "shell-amt-hidden", "shell-title-hidden", "shell-sub-hidden", "GitHub step-up", c.githubDelta, "Team to Enterprise"]
  ];
  var maxBar = 1;
  bars.forEach(function (bar) { if (bar[5] > maxBar) maxBar = bar[5]; });
  bars.forEach(function (bar) {
    document.getElementById(bar[0]).style.flex = Math.max(12, Math.round(bar[5] / maxBar * 100)) + " 1 0px";
    document.getElementById(bar[1]).textContent = ssMoney(bar[5]);
    document.getElementById(bar[2]).textContent = bar[4];
    document.getElementById(bar[3]).textContent = bar[6];
  });
  document.getElementById("shell-sticker").textContent = ssMoney(c.zoomDelta) + " / yr";
  document.getElementById("shell-sticker-note").textContent = "Smallest published SAML step-up";
  document.getElementById("shell-gap").textContent = "+" + ssMoney(c.figmaDelta - c.zoomDelta);
  var labels = document.querySelectorAll("#shell-summary .summary-label");
  if (labels.length >= 2) {
    labels[0].textContent = "Zoom step-up";
    labels[1].textContent = "Figma above Zoom";
  }
  var notes = document.querySelectorAll("#shell-summary .summary-scenario");
  if (notes.length >= 2) notes[1].textContent = "Organization minus the Zoom step-up";
  var workosText = c.workos < 0 ? "unknown" : ssMoney(c.workos);
  var perPerson = c.workos < 0 ? "unknown" : ssMoney(Math.round(c.workos / c.users));
  document.getElementById("ss-split").textContent = c.connections + " WorkOS connections are " + workosText + " a year. Divided by " + c.users + " people, that is " + perPerson + " a person for the year. WorkOS does not publish a per-person SSO price.";
  document.getElementById("shell-math").textContent = c.users + " people. Zoom " + ssMoney(c.zoomLow) + " to " + ssMoney(c.zoomHigh) + ", step-up " + ssMoney(c.zoomDelta) + ". Notion " + ssMoney(c.notionLow) + " to " + ssMoney(c.notionHigh) + ", step-up " + ssMoney(c.notionDelta) + ". GitHub " + ssMoney(c.githubLow) + " to " + ssMoney(c.githubHigh) + ", step-up " + ssMoney(c.githubDelta) + ". Figma " + ssMoney(c.figmaLow) + " to " + ssMoney(c.figmaHigh) + ", step-up " + ssMoney(c.figmaDelta) + ". Slack Business+ " + ssMoney(c.slackHigh) + "; Pro in US dollars is unknown, so the step-up is unknown. Okta Starter " + ssMoney(c.oktaStarter) + " (the $1,500 floor is included). WorkOS " + workosText + " at " + (c.rate < 0 ? "a custom rate" : "$" + c.rate + " per connection per month") + ". 1Password Business " + ssMoney(c.password) + ".";
  function appRow(name, lowLabel, highLabel, low, high, delta) {
    var step = delta < 0 ? "unknown" : ssMoney(delta);
    return "<tr><td data-label=\"App\">" + name + "</td><td data-label=\"Without SAML\">" + lowLabel + " " + (low < 0 ? "unknown" : ssMoney(low)) + "</td><td data-label=\"With SAML\">" + highLabel + " " + ssMoney(high) + "</td><td data-label=\"Year-1 step-up\">" + step + "</td></tr>";
  }
  document.getElementById("ss-apps-body").innerHTML = ""
    + appRow("Notion", "Plus $10/member/mo", "Business $20/member/mo", c.notionLow, c.notionHigh, c.notionDelta)
    + appRow("Zoom", "Pro $14.16/user/mo annual", "Business $18.33/user/mo annual", c.zoomLow, c.zoomHigh, c.zoomDelta)
    + appRow("GitHub", "Team $4/user/mo", "Enterprise $21/user/mo", c.githubLow, c.githubHigh, c.githubDelta)
    + appRow("Figma", "Professional $16/editor/mo", "Organization $55/editor/mo", c.figmaLow, c.figmaHigh, c.figmaDelta)
    + "<tr><td data-label=\"App\">Slack</td><td data-label=\"Without SAML\">Pro, US dollars unknown. Euro list is €6.75.</td><td data-label=\"With SAML\">Business+ " + ssMoney(c.slackHigh) + " at $15. Euro list is €15.</td><td data-label=\"Year-1 step-up\">unknown</td></tr>";
  var rateLabel = c.rate < 0 ? "custom rate" : "$" + c.rate + " per connection per month";
  document.getElementById("ss-context-body").innerHTML = ""
    + "<tr><td data-label=\"Product\">Okta Starter</td><td data-label=\"What you are buying\">IdP. SSO is included from this suite. Floor $1,500.</td><td data-label=\"Year-1\">" + ssMoney(c.oktaStarter) + "</td></tr>"
    + "<tr><td data-label=\"Product\">Okta Core Essentials</td><td data-label=\"What you are buying\">$14 per user per month, same floor.</td><td data-label=\"Year-1\">" + ssMoney(c.oktaCore) + "</td></tr>"
    + "<tr><td data-label=\"Product\">Okta Essentials</td><td data-label=\"What you are buying\">$17 per user per month, same floor.</td><td data-label=\"Year-1\">" + ssMoney(c.oktaEssentials) + "</td></tr>"
    + "<tr><td data-label=\"Product\">Okta Professional and Enterprise</td><td data-label=\"What you are buying\">Inquire.</td><td data-label=\"Year-1\">unknown</td></tr>"
    + "<tr><td data-label=\"Product\">WorkOS SSO</td><td data-label=\"What you are buying\">" + c.connections + " connections, " + rateLabel + ".</td><td data-label=\"Year-1\">" + workosText + "</td></tr>"
    + "<tr><td data-label=\"Product\">1Password Business</td><td data-label=\"What you are buying\">Vault. Unlock with SSO is OIDC, not SAML.</td><td data-label=\"Year-1\">" + ssMoney(c.password) + "</td></tr>";
  if (typeof window.trackSaaSBillEvent === "function") {
    window.trackSaaSBillEvent("result_rendered", { page: "sso-tax", users: c.users, connections: c.connections });
  }
}
["ss-users", "ss-conn"].forEach(function (id) {
  var el = document.getElementById(id);
  el.addEventListener("input", renderSsoTax);
  el.addEventListener("change", renderSsoTax);
});
renderSsoTax();
</script>
"""

FAQS = [
    (
        "Does Okta charge extra for SAML?",
        "On the Workforce Identity pricing page checked 6 Nov 2026, SSO is included from the Starter suite at $6 per user per month, along with MFA, Universal Directory, and 5 Workflows. Suites are billed annually, and the annual contract minimum is $1,500. Professional and Enterprise are inquire, so those list prices are unknown. A standalone SSO dollar price is not on that page, so it is unknown.",
    ),
    (
        "How does WorkOS charge for SSO?",
        "WorkOS prices production SSO per IdP connection per month: $125 for 1 to 15 connections, then $100, $80, and $65 on the higher rungs. 101 or more is custom, so that bill is unknown. AuthKit includes the first 1 million monthly active users. That is not a per-person SSO rate. Five connections at $125 are $7,500 a year, which is $300 a person only if you divide the connection bill by 25 people.",
    ),
    (
        "Does 1Password replace Okta?",
        "No. 1Password Business, at $8.99 per user per month billed yearly, includes Unlock with Single Sign-On and that unlock is OIDC, not SAML. The Teams Starter Pack does not include it. Enterprise and SaaS Manager SAML are quote-only, so those prices are unknown. 1Password does not offer a HIPAA BAA. You still bring your own IdP.",
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
    if "\u2014" in TITLE or "\u2014" in REST or "2x" in REST:
        raise SystemExit("banned phrasing in sso tax copy")
    workbench = render_workbench(
        CONTROLS,
        controls_title="Your team",
        chart_title="Year-1 SAML step-up",
        cta_href="#ss-apps",
        cta_label="See the app step-ups",
        cta_vendor="saasbill",
    )
    body = (
        "<section class=\"hero\">"
        "<h1>The B2B SaaS SSO tax calculator (2026)</h1>"
        "<p class=\"lead\">What selected apps charge to turn on SAML, plus Okta, WorkOS, and 1Password as separate bills.</p>"
        "</section>"
        + workbench
        + REST
    )
    if "/go/1password" in body or "sponsored" in body:
        raise SystemExit("affiliate tracking on the SSO page")
    render_page(
        REL,
        TITLE,
        DESCRIPTION,
        CANONICAL,
        wrap_calculator_shell(body),
        faqs=FAQS,
        published_date="2026-11-06",
        show_affiliate_note=False,
    )
    copy_to_root(REL)


if __name__ == "__main__":
    build()
