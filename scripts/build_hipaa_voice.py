"""AI voice and transcription HIPAA BAA matrix.

Sources checked 2026-11-09. Unknown stays the word unknown.
A BAA is necessary but not sufficient. The page does not rank vendors.
"""
import os
import shutil

from layout import BASE_DIR, PUBLIC_DIR, render_page, render_workbench, wrap_calculator_shell

TITLE = "AI voice HIPAA BAA matrix – saasbill.io"
DESCRIPTION = (
    "A BAA is necessary but not sufficient. Zoom healthcare Pro lists $14.16 a user a month on the annual plan. "
    "Otter's HIPAA add-on price is unknown. Checked 9 Nov 2026."
)
REL = "compliance/ai-voice-and-transcription-hipaa-baa-matrix-2026/index.html"
CANONICAL = "/compliance/ai-voice-and-transcription-hipaa-baa-matrix-2026/"

CONTROLS = """
        <div class="wb-control-item">
          <label class="wb-control-label" for="hv-seats">Seats <span class="val-pill" id="hv-seats-val">5</span></label>
          <div class="wb-slider-row">
            <input type="range" id="hv-seats" min="1" max="25" step="1" value="5" aria-label="Seats" data-track="calculator-control" data-control="seats" />
          </div>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="hv-bill">Billing</label>
          <select id="hv-bill" class="wb-tool-select" aria-label="Billing" data-track="calculator-control" data-control="billing">
            <option value="annual" selected>Annual</option>
            <option value="monthly">Monthly</option>
          </select>
        </div>
        <p class="wb-budget-subnote">A BAA is necessary but not sufficient. The matrix does not rank vendors.</p>
"""

REST = r"""
<section id="hv-matrix">
  <h2>BAA plan and Year-1</h2>
  <p>Each row is that vendor's plan that lists a BAA. A missing price stays unknown. Fathom's Team and Business standard BAA was on the pricing page on 9 Nov 2026.</p>
  <div class="table-wrap editorial-gap-table mobile-cards">
    <table>
      <caption id="hv-caption">5 seats, annual billing, BAA required. Not a ranking.</caption>
      <thead>
        <tr>
          <th>Vendor</th>
          <th>Plan</th>
          <th>Year-1</th>
          <th>Still unknown</th>
        </tr>
      </thead>
      <tbody id="hv-body">
        <tr><td data-label="Vendor">Otter</td><td data-label="Plan">Enterprise, HIPAA add-on</td><td data-label="Year-1">unknown</td><td data-label="Still unknown">Enterprise price and HIPAA add-on price</td></tr>
        <tr><td data-label="Vendor">Fireflies</td><td data-label="Plan">Enterprise, annual only</td><td data-label="Year-1">Base $2,340. HIPAA total unknown</td><td data-label="Still unknown">Private Storage, required for HIPAA</td></tr>
        <tr><td data-label="Vendor">Fathom</td><td data-label="Plan">Team, standard BAA</td><td data-label="Year-1">$900</td><td data-label="Still unknown">None on this seat line</td></tr>
        <tr><td data-label="Vendor">Granola</td><td data-label="Plan">Enterprise</td><td data-label="Year-1">$2,100</td><td data-label="Still unknown">A separate annual rate</td></tr>
        <tr><td data-label="Vendor">Zoom</td><td data-label="Plan">Healthcare Pro</td><td data-label="Year-1">$849.60</td><td data-label="Still unknown">Business and above, sold through sales</td></tr>
        <tr><td data-label="Vendor">AssemblyAI</td><td data-label="Plan">BAA, no premium pricing</td><td data-label="Year-1">unknown</td><td data-label="Still unknown">Per-hour usage. $50 of credits</td></tr>
        <tr><td data-label="Vendor">Deepgram</td><td data-label="Plan">Enterprise</td><td data-label="Year-1">unknown</td><td data-label="Still unknown">Custom price. Growth is not the BAA plan</td></tr>
      </tbody>
    </table>
  </div>
  <p id="hv-note" class="summary-caveat">A BAA is necessary but not sufficient. No vendor is ranked.</p>
</section>

<section>
  <h2>What a BAA does not cover</h2>
  <ul class="key-list">
    <li>A signed BAA does not, by itself, finish the vendor's setup. Fireflies requires Private Storage as well as the BAA. Removing Private Storage, or downgrading, turns HIPAA off. The Private Storage price is unknown.</li>
    <li>Turn off public sharing and auto-join bots where the vendor's own HIPAA setup tells you to. Those switches are not priced here.</li>
    <li>Zoom says some AI features may be unavailable for healthcare customers with a BAA.</li>
    <li>Otter's HIPAA add-on is sold through an account manager. The add-on price is unknown. SSO and SCIM on Enterprise have a 100-user minimum license. That minimum is not stated as the HIPAA price.</li>
  </ul>
</section>

<section>
  <h2>Prices checked on 9 Nov 2026</h2>
  <div class="table-wrap editorial-gap-table mobile-cards">
    <table>
      <caption>Published list prices. Quote-only lines stay unknown.</caption>
      <thead>
        <tr>
          <th>Item</th>
          <th>Published price</th>
          <th>In the Year-1 column</th>
        </tr>
      </thead>
      <tbody>
        <tr><td data-label="Item">Otter</td><td data-label="Published price">Basic is free. Pro is $16.99 per user per month, or $8.33 per user per month annual. Business is $30 per user per month, or $19.99 annual. HIPAA is only on Enterprise, as an add-on, through an account manager.</td><td data-label="In the Year-1 column">Enterprise and the HIPAA add-on are unknown. Pro and Business do not list a BAA.</td></tr>
        <tr><td data-label="Item">Fireflies</td><td data-label="Published price">Enterprise is $39 per seat per month, billed annually only. HIPAA needs Private Storage and a signed BAA. AI credits are not in the base price. The add-on starts at $5 per user per month.</td><td data-label="In the Year-1 column">The $39 line is the base only. The HIPAA total is unknown because Private Storage is unknown. Credits are not added.</td></tr>
        <tr><td data-label="Item">Fathom</td><td data-label="Published price">Team is $19 per user per month, or $15 annual, with a 2-user minimum, and includes a standard BAA. Business is $34 monthly or $25 annual, also a standard BAA, same minimum. Enterprise is $35 per user per month, annual only, and is eligible for a custom BAA. Free and Premium ($20 monthly or $16 annual) have no BAA.</td><td data-label="In the Year-1 column">Team, with the 2-user minimum. Checked 9 Nov 2026.</td></tr>
        <tr><td data-label="Item">Granola</td><td data-label="Published price">Basic is free. Business is $14 per user per month. Enterprise is $35 per user per month. HIPAA workspaces are on Enterprise only. The pricing page says to contact sales. SSO is for enterprise workspaces with 50 or more users.</td><td data-label="In the Year-1 column">$35 times 12 times seats. No separate annual rate was on the page, so both billing choices use that monthly rate. The 50-user note is for SSO, not a price floor.</td></tr>
        <tr><td data-label="Item">Zoom</td><td data-label="Published price">A BAA is for paid plans. Pro can accept it at checkout. Business, Business Plus, and Enterprise go through sales. Free Basic is not eligible. Healthcare Pro is $16.99 per user per month, or $14.16 annual.</td><td data-label="In the Year-1 column">Healthcare Pro. Higher healthcare editions are unknown.</td></tr>
        <tr><td data-label="Item">AssemblyAI</td><td data-label="Published price">A HIPAA BAA is signable in minutes without a sales call, with no premium pricing. Usage is billed per hour. New accounts get $50 of free credits.</td><td data-label="In the Year-1 column">unknown. Seats do not set the bill.</td></tr>
        <tr><td data-label="Item">Deepgram</td><td data-label="Published price">BAAs are for Enterprise customers, custom pricing, through sales. Pay as you go includes $200 of free credit. Growth is from $4,000 a year prepaid.</td><td data-label="In the Year-1 column">Enterprise is unknown. The $4,000 Growth floor is not a BAA price.</td></tr>
      </tbody>
    </table>
  </div>
  <p class="src-cluster"><a class="src-link" href="https://help.otter.ai/hc/en-us/articles/33975072019991-HIPAA-Otter-ai" target="_blank" rel="noopener">Otter HIPAA</a> <span class="src-date">Accessed 2026-11-09</span></p>
  <p class="src-cluster"><a class="src-link" href="https://otter.ai/pricing" target="_blank" rel="noopener">Otter pricing</a> <span class="src-date">Accessed 2026-11-09</span></p>
  <p class="src-cluster"><a class="src-link" href="https://guide.fireflies.ai/articles/4771323041-learn-about-fireflies-enterprise-plan" target="_blank" rel="noopener">Fireflies Enterprise</a> <span class="src-date">Accessed 2026-11-09</span></p>
  <p class="src-cluster"><a class="src-link" href="https://guide.fireflies.ai/articles/3704059205-set-up-hipaa-compliance-for-your-workspace" target="_blank" rel="noopener">Fireflies HIPAA setup</a> <span class="src-date">Accessed 2026-11-09</span></p>
  <p class="src-cluster"><a class="src-link" href="https://fireflies.ai/baa" target="_blank" rel="noopener">Fireflies BAA</a> <span class="src-date">Accessed 2026-11-09</span></p>
  <p class="src-cluster"><a class="src-link" href="https://fireflies.ai/pricing" target="_blank" rel="noopener">Fireflies pricing</a> <span class="src-date">Accessed 2026-11-09</span></p>
  <p class="src-cluster"><a class="src-link" href="https://www.fathom.ai/pricing" target="_blank" rel="noopener">Fathom pricing</a> <span class="src-date">Accessed 2026-11-09</span></p>
  <p class="src-cluster"><a class="src-link" href="https://www.granola.ai/pricing" target="_blank" rel="noopener">Granola pricing</a> <span class="src-date">Accessed 2026-11-09</span></p>
  <p class="src-cluster"><a class="src-link" href="https://docs.granola.ai/help-center/consent-security-privacy/is-granola-hipaa-compliant" target="_blank" rel="noopener">Granola HIPAA</a> <span class="src-date">Accessed 2026-11-09</span></p>
  <p class="src-cluster"><a class="src-link" href="https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0067751" target="_blank" rel="noopener">Zoom BAA</a> <span class="src-date">Accessed 2026-11-09</span></p>
  <p class="src-cluster"><a class="src-link" href="https://zoom.us/pricing/healthcare" target="_blank" rel="noopener">Zoom healthcare pricing</a> <span class="src-date">Accessed 2026-11-09</span></p>
  <p class="src-cluster"><a class="src-link" href="https://www.assemblyai.com/pricing/" target="_blank" rel="noopener">AssemblyAI pricing</a> <span class="src-date">Accessed 2026-11-09</span></p>
  <p class="src-cluster"><a class="src-link" href="https://deepgram.com/pricing" target="_blank" rel="noopener">Deepgram pricing</a> <span class="src-date">Accessed 2026-11-09</span></p>
  <p class="src-cluster"><a class="src-link" href="https://developers.deepgram.com/trust-security/data-privacy-compliance" target="_blank" rel="noopener">Deepgram privacy</a> <span class="src-date">Accessed 2026-11-09</span></p>
</section>
<script>
function hvMoney(cents) {
  if (cents < 0) return "unknown";
  var v = Math.round(cents);
  var dollars = Math.floor(v / 100);
  var rest = v % 100;
  var text = "$" + dollars.toLocaleString("en-US");
  if (rest) text += "." + (rest < 10 ? "0" : "") + rest;
  return text;
}

function hvYear(centsPerUserMonth, seats) {
  return seats * centsPerUserMonth * 12;
}

function hvCaption(seats, annual) {
  return seats + " " + (seats === 1 ? "seat" : "seats") + ", " + (annual ? "annual" : "monthly") + " billing, BAA required. Not a ranking.";
}

function calcHipaa(input) {
  var seats = Math.max(1, Math.min(25, Math.round(Number(input.seats) || 1)));
  var annual = String(input.billing || "annual") !== "monthly";
  var fathomSeats = Math.max(seats, 2);
  return {
    seats: seats,
    annual: annual,
    fathomSeats: fathomSeats,
    fathomYear: hvYear(annual ? 1500 : 1900, fathomSeats),
    zoomYear: hvYear(annual ? 1416 : 1699, seats),
    granolaYear: hvYear(3500, seats),
    firefliesBase: annual ? hvYear(3900, seats) : -1,
    otterYear: -1,
    assemblyYear: -1,
    deepgramYear: -1
  };
}

function hvRead() {
  return {
    seats: document.getElementById("hv-seats").value,
    billing: document.getElementById("hv-bill").value
  };
}

function renderHipaa() {
  var c = calcHipaa(hvRead());
  var seatWord = c.seats === 1 ? "seat" : "seats";
  var term = c.annual ? "annual" : "monthly";
  document.getElementById("hv-seats-val").textContent = String(c.seats);
  document.getElementById("hv-caption").textContent = hvCaption(c.seats, c.annual);
  document.getElementById("shell-big").textContent = "Not a ranking";
  var perYear = document.querySelector("#shell-result .wb-per-year");
  if (perYear) perYear.textContent = "";
  document.getElementById("shell-product").textContent = "Published seat list prices";
  document.getElementById("shell-quote").textContent = "Published seat list prices, not a full cost";
  document.getElementById("shell-sub").textContent = "A BAA is necessary but not sufficient. Missing prices stay unknown.";
  document.getElementById("shell-best").textContent = "Not a ranking.";
  var bars = [
    ["shell-row-base", "shell-amt-base", "shell-title-base", "shell-sub-base", "Zoom Pro", c.zoomYear, "Healthcare list price"],
    ["shell-row-seats", "shell-amt-seats", "shell-title-seats", "shell-sub-seats", "Fathom Team", c.fathomYear, "Standard BAA, 2-seat minimum"],
    ["shell-row-hidden", "shell-amt-hidden", "shell-title-hidden", "shell-sub-hidden", "Granola Enterprise", c.granolaYear, "$35 per user per month"]
  ];
  var maxBar = 1;
  bars.forEach(function (bar) { if (bar[5] > maxBar) maxBar = bar[5]; });
  bars.forEach(function (bar) {
    document.getElementById(bar[0]).style.flex = "1 1 0px";
    var block = document.querySelector("#" + bar[0] + " .wb-vbar-block");
    if (block) block.style.height = Math.max(56, Math.round(bar[5] / maxBar * 160)) + "px";
    document.getElementById(bar[1]).textContent = hvMoney(bar[5]);
    document.getElementById(bar[2]).textContent = bar[4];
    document.getElementById(bar[3]).textContent = bar[6];
  });
  document.getElementById("shell-sticker").textContent = "3";
  document.getElementById("shell-sticker-note").textContent = "Zoom, Fathom, and Granola seat lists";
  document.getElementById("shell-gap").textContent = "4";
  var labels = document.querySelectorAll("#shell-summary .summary-label");
  if (labels.length >= 2) {
    labels[0].textContent = "Published seat lists";
    labels[1].textContent = "Unknown or incomplete";
  }
  var notes = document.querySelectorAll("#shell-summary .summary-scenario");
  if (notes.length >= 2) notes[1].textContent = "Not a full HIPAA cost";
  var firefliesText = c.annual ? "Base " + hvMoney(c.firefliesBase) + ". HIPAA total unknown" : "unknown. Annual only";
  var billed = c.fathomSeats === 1 ? "1 billed seat" : c.fathomSeats + " billed seats";
  function row(vendor, plan, yearText, unknownText) {
    return "<tr><td data-label=\"Vendor\">" + vendor + "</td><td data-label=\"Plan\">" + plan + "</td><td data-label=\"Year-1\">" + yearText + "</td><td data-label=\"Still unknown\">" + unknownText + "</td></tr>";
  }
  document.getElementById("hv-body").innerHTML = ""
    + row("Otter", "Enterprise, HIPAA add-on", hvMoney(c.otterYear), "Enterprise price and HIPAA add-on price")
    + row("Fireflies", "Enterprise", firefliesText, "Private Storage, required for HIPAA")
    + row("Fathom", "Team, standard BAA", hvMoney(c.fathomYear), billed + ". Custom BAA is Enterprise.")
    + row("Granola", "Enterprise", hvMoney(c.granolaYear), "No separate annual rate was published")
    + row("Zoom", "Healthcare Pro", hvMoney(c.zoomYear), "Business and above are unknown")
    + row("AssemblyAI", "BAA, no premium pricing", "unknown", "Per-hour usage. $50 of credits")
    + row("Deepgram", "Enterprise", "unknown", "Enterprise is custom. Growth from $4,000 is not a BAA price");
  document.getElementById("shell-math").textContent = c.seats + " " + seatWord + ", " + term + ". Otter unknown. Fireflies " + firefliesText + ". Fathom " + hvMoney(c.fathomYear) + " on " + billed + ". Granola " + hvMoney(c.granolaYear) + ". Zoom " + hvMoney(c.zoomYear) + ". AssemblyAI unknown. Deepgram unknown. Published seat list prices, not a full cost. Not a ranking.";
  document.getElementById("hv-note").textContent = "A BAA is necessary but not sufficient. No vendor is ranked. Fathom Team and Business list a standard BAA on the pricing page checked 9 Nov 2026.";
  if (typeof window.trackSaaSBillEvent === "function") {
    window.trackSaaSBillEvent("result_rendered", { page: "hipaa-voice", seats: c.seats });
  }
}
["hv-seats", "hv-bill"].forEach(function (id) {
  var el = document.getElementById(id);
  el.addEventListener("input", renderHipaa);
  el.addEventListener("change", renderHipaa);
});
renderHipaa();
</script>
"""

FAQS = [
    (
        "Which Otter plan signs a BAA?",
        "Only Enterprise, and HIPAA is an add-on arranged with an account manager. Pro and Business publish seat prices and do not list that add-on. The Enterprise price and the add-on price are unknown. SSO and SCIM on Enterprise require a 100-user minimum license.",
    ),
    (
        "Does Fireflies include HIPAA in the $39 price?",
        "No. Enterprise is $39 per seat per month, billed annually only. HIPAA also requires Private Storage and a signed BAA. Private Storage has no published price, so the HIPAA total is unknown. Removing Private Storage or downgrading turns HIPAA off. AI credits start at $5 per user per month and are not in the base price.",
    ),
    (
        "Does a BAA make the product safe to use?",
        "A BAA is necessary but not sufficient. You still follow the vendor's setup, including storage and sharing rules. Zoom says some AI features may be unavailable for healthcare customers with a BAA.",
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
    if "\u2014" in TITLE or "\u2014" in REST or "\u2014" in CONTROLS:
        raise SystemExit("em dash in hipaa voice copy")
    workbench = render_workbench(
        CONTROLS,
        controls_title="Your team",
        chart_title="Published BAA seat prices",
        cta_href="#hv-matrix",
        cta_label="See the matrix",
        cta_vendor="saasbill",
    )
    for old, new in (
        ('class="wb-vbar-container"', 'class="wb-vbar-container wb-vbar-separate"'),
        ('id="shell-product">Year-1 total<', 'id="shell-product">Published seat list prices<'),
        ('id="shell-big">$0</span> <span class="wb-per-year">/ year</span>', 'id="shell-big">Not a ranking</span> <span class="wb-per-year"></span>'),
        ('id="shell-quote">True Year-1 cost<', 'id="shell-quote">Published seat list prices, not a full cost<'),
        ('id="shell-sub">Matches advertised price ($0 hidden fees).</p>', 'id="shell-sub">A BAA is necessary but not sufficient. Missing prices stay unknown.</p>'),
        ('id="shell-title-base">Sticker Price<', 'id="shell-title-base">Zoom Pro<'),
        ('id="shell-sub-base">Advertised price<', 'id="shell-sub-base">Healthcare list price<'),
        ('id="shell-amt-base">$0<', 'id="shell-amt-base">$849.60<'),
        ('id="shell-title-seats">Other sticker fees<', 'id="shell-title-seats">Fathom Team<'),
        ('id="shell-sub-seats">Included in the sticker<', 'id="shell-sub-seats">Standard BAA, 2-seat minimum<'),
        ('id="shell-amt-seats">$0<', 'id="shell-amt-seats">$900<'),
        ('id="shell-title-hidden">Hidden Cost Gap<', 'id="shell-title-hidden">Granola Enterprise<'),
        ('id="shell-sub-hidden">Fees above the advertised price<', 'id="shell-sub-hidden">$35 per user per month<'),
        ('id="shell-amt-hidden">$0<', 'id="shell-amt-hidden">$2,100<'),
        ('<div class="summary-label">Sticker Price</div>', '<div class="summary-label">Published seat lists</div>'),
        ('id="shell-sticker">$0<', 'id="shell-sticker">3<'),
        ('id="shell-sticker-note">Advertised price<', 'id="shell-sticker-note">Zoom, Fathom, and Granola seat lists<'),
        ('<div class="summary-label">Hidden Cost Gap</div>', '<div class="summary-label">Unknown or incomplete</div>'),
        ('id="shell-gap">$0<', 'id="shell-gap">4<'),
        ('<div class="summary-scenario">Above the advertised price</div>', '<div class="summary-scenario">Not a full HIPAA cost</div>'),
        ('aria-label="Sticker price and hidden cost gap"', 'aria-label="Published prices and unknown lines"'),
    ):
        if old not in workbench:
            raise SystemExit("missing workbench fallback: " + old)
        workbench = workbench.replace(old, new, 1)
    body = (
        '<section class="hero">'
        "<h1>AI voice and transcription HIPAA BAA matrix (2026)</h1>"
        '<p class="lead">A BAA is necessary but not sufficient. '
        "The matrix lists which plan publishes a BAA, and which Year-1 prices stay unknown.</p>"
        "</section>"
        + workbench
        + REST
    )
    if "/go/" in body or "sponsored" in body or "jotform" in body.lower():
        raise SystemExit("unexpected affiliate link on the HIPAA voice page")
    render_page(
        REL,
        TITLE,
        DESCRIPTION,
        CANONICAL,
        wrap_calculator_shell(body),
        faqs=FAQS,
        published_date="2026-11-09",
        show_affiliate_note=False,
    )
    copy_to_root(REL)


if __name__ == "__main__":
    build()
