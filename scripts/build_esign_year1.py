"""PandaDoc versus DocuSign versus Jotform Sign, Year-1 list price.

Checked 2026-11-13.
PandaDoc pricing and plan comparison, PandaDoc's BBB response, DocuSign pricing
and the DocuSign plans article, nodshake's third-party overage table, and
Jotform pricing plus Jotform Sign. No PandaDoc affiliate link. The Jotform
link is the pricing URL in data/affiliate_links.json.
"""
import json
import os
import shutil

from layout import BASE_DIR, DATA_DIR, PUBLIC_DIR, render_page, render_workbench, wrap_calculator_shell

TITLE = "PandaDoc vs DocuSign vs Jotform – saasbill.io"
DESCRIPTION = "Year-1 list price for PandaDoc, DocuSign, and Jotform Sign. Checked 13 Nov 2026."
CANONICAL = "/pricing/pandadoc-vs-docusign-vs-jotform-sign-year-1-cost/"
REL = "pricing/pandadoc-vs-docusign-vs-jotform-sign-year-1-cost/index.html"
LEAD = "DocuSign counts sent envelopes, Jotform Sign counts signed documents, and PandaDoc counts seats plus automation credits."

with open(os.path.join(DATA_DIR, "affiliate_links.json"), encoding="utf-8") as handle:
    JOTFORM_PRICING = json.load(handle)["jotform"]["custom_links"]["pricing"]

CONTROLS = r"""
        <div class="wb-control-item">
          <label class="wb-control-label" for="es-seats">Senders <span class="val-pill" id="es-seats-val">3</span></label>
          <div class="wb-slider-row">
            <input type="range" id="es-seats" min="1" max="60" step="1" value="3" aria-label="Number of senders" data-track="calculator-control" data-control="seats" />
          </div>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="es-docs">Documents a month <span class="val-pill" id="es-docs-val">20</span></label>
          <div class="wb-slider-row">
            <input type="range" id="es-docs" min="0" max="1500" step="1" value="20" aria-label="Documents sent per month" data-track="calculator-control" data-control="documents" />
          </div>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="es-billing">Billing</label>
          <select id="es-billing" class="wb-tool-select" data-track="calculator-control" data-control="billing">
            <option value="annual" selected>Annual, paid upfront</option>
            <option value="monthly">Month to month</option>
          </select>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="es-hipaa">HIPAA required</label>
          <select id="es-hipaa" class="wb-tool-select" data-track="calculator-control" data-control="hipaa">
            <option value="no" selected>No</option>
            <option value="yes">Yes</option>
          </select>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="es-auto">PandaDoc forms and automation <span class="val-pill" id="es-auto-val">0%</span></label>
          <div class="wb-slider-row">
            <input type="range" id="es-auto" min="0" max="100" step="5" value="0" aria-label="Share of documents created through forms or automation" data-track="calculator-control" data-control="automation-share" />
          </div>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="es-std-over">Standard overage per envelope <span class="val-pill" id="es-std-over-val">$3.60</span></label>
          <div class="wb-slider-row">
            <input type="range" id="es-std-over" min="0" max="20" step="0.01" value="3.60" aria-label="DocuSign Standard overage per envelope" data-track="calculator-control" data-control="standard-overage" />
          </div>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="es-bp-over">Business Pro overage per envelope <span class="val-pill" id="es-bp-over-val">$5.80</span></label>
          <div class="wb-slider-row">
            <input type="range" id="es-bp-over" min="0" max="20" step="0.01" value="5.80" aria-label="DocuSign Business Pro overage per envelope" data-track="calculator-control" data-control="business-pro-overage" />
          </div>
          <p class="wb-budget-subnote">Starting rates are third-party figures from nodshake: $3.60 and $5.80 on annual plans, $5.40 and $7.80 month to month. DocuSign's pricing article states a range of $3.60 to $7.80 per envelope and does not print this split.</p>
        </div>
"""

REST = r"""
<section id="es-costs">
  <h2>Year-1 list price</h2>
  <div class="table-wrap editorial-gap-table mobile-cards">
    <table>
      <caption>Twelve months at the list price for the numbers above.</caption>
      <thead>
        <tr>
          <th>Plan</th>
          <th>Year 1</th>
        </tr>
      </thead>
      <tbody id="es-body">
        <tr><td data-label="Plan">PandaDoc Starter</td><td data-label="Year 1">$684</td></tr>
        <tr><td data-label="Plan">PandaDoc Business</td><td data-label="Year 1">$1,764</td></tr>
        <tr><td data-label="Plan">DocuSign Standard</td><td data-label="Year 1">$900</td></tr>
        <tr><td data-label="Plan">DocuSign Business Pro</td><td data-label="Year 1">$1,440</td></tr>
        <tr><td data-label="Plan">Jotform Sign, one account</td><td data-label="Year 1">$408</td></tr>
        <tr><td data-label="Plan">Jotform Sign, one account per user</td><td data-label="Year 1">$1,224</td></tr>
      </tbody>
    </table>
  </div>
  <p class="paid-partnership-note">Paid partnership with Jotform (#JotformPartner)</p>
  <div class="cta-stack">
    <a class="btn-cta" href="__JOTFORM_PRICING__" target="_blank" rel="sponsored nofollow noopener" data-track="vendor-cta" data-vendor="jotform" data-cta-location="subpage-summary">Jotform pricing &rarr;</a>
  </div>
</section>

<section>
  <h2>What changes the list price</h2>
  <ul class="key-list">
    <li>PandaDoc Free allows 5 documents a month on one shared limit. It is not a row above.</li>
    <li>Documents sent from the PandaDoc editor are not metered on Starter or Business. Documents created through the API, Zapier, Make, forms, or bulk send use usage credits. The recurring credit pack price is not published. The API stops when credits run out. Other automations continue, and the overage uses the unit price on the order form, or up to $5 a document when the order form has no unit price. Unused documents do not roll over.</li>
    <li>A 14-day PandaDoc trial is listed and is not subtracted here. PandaDoc prices exclude taxes. Qualified electronic signatures are on annual PandaDoc plans only.</li>
    <li>HIPAA is not listed on PandaDoc Starter or Business. A third-party summary calls it an optional Enterprise extra, so this page treats it as a quote. <span class="src-cluster"><a class="src-link" href="https://grouglobal.com/blog/pandadoc-pricing" target="_blank" rel="noopener">Third-party PandaDoc pricing summary</a> <span class="src-date">Listed 14 Oct 2026. Accessed 13 Nov 2026.</span></span></li>
    <li>PandaDoc annual plans renew unless cancellation is requested at least 30 days before renewal. The company says a reminder goes out 45 days ahead.</li>
    <li>DocuSign annual plans include 100 envelopes per user for the year. Month-to-month plans include 10 per user each month. A sent envelope counts even when it is not completed.</li>
    <li>DocuSign also sells annual plans billed monthly: Personal $11 a month ($132 a year), Standard $30 per user ($360), and Business Pro $45 per user ($540). This calculator uses annual upfront or month-to-month, not that middle option.</li>
    <li>An annual DocuSign plan is a 12-month commitment. Cancel within 30 days of purchase for a refund, once per customer. After 30 days, an annual plan billed monthly still owes the rest of the year. Plans renew on their own.</li>
    <li>DocuSign Personal is one user and 5 envelopes a month. Past that, extra envelopes are not offered on Personal. Standard and Business Pro list up to 50 users. Web forms, bulk send, and payment collection are on Business Pro.</li>
    <li>SMS delivery starts at $0.36 a delivery and ID verification starts at $2.40 an attempt. Those add-ons are not in this total. A HIPAA agreement, SSO, and knowledge-based authentication are on Enhanced plans, which are a quote.</li>
    <li>Jotform Sign monthly limits are 10 on Starter, 100 on Bronze, 250 on Silver, and 1,000 on Gold. Paid self-serve plans are one user. Enterprise is the multi-user plan, and its price is a quote. One shared account is not the same thing as one account per person.</li>
    <li>Jotform HIPAA features are on Gold and Enterprise. Plans renew until canceled. A 30-day money-back guarantee is listed, and canceling keeps the plan until the next billing date. A nonprofit or education discount, and any 24-hour signup offer, are not in these prices.</li>
  </ul>
</section>

<section>
  <h2>What users wrote</h2>
  <ul class="key-list">
    <li>On Reddit, one user says a PandaDoc cancellation looked complete in the app, then the annual plan renewed and no refund was given. That is one post. <span class="src-cluster"><a class="src-link" href="https://www.reddit.com/r/software/comments/1vfdwol/dealing_with_pandadocs_terrible_customer_service/" target="_blank" rel="noopener">Reddit thread</a> <span class="src-date">Accessed 13 Nov 2026.</span></span></li>
    <li>On the BBB page, a long-time Business customer was surprised by per-document charges for form-generated documents after renewal. PandaDoc's response on that complaint says the plan included 250 Forms usage credits and further documents cost $2 each. That is one case. <span class="src-cluster"><a class="src-link" href="https://www.bbb.org/us/ca/san-francisco/profile/computer-software-developers/pandadoc-1116-905103/complaints" target="_blank" rel="noopener">PandaDoc BBB complaints</a> <span class="src-date">Accessed 13 Nov 2026.</span></span></li>
  </ul>
</section>

<p class="summary-caveat">Checked 13 Nov 2026. <span class="src-cluster"><a class="src-link" href="https://www.pandadoc.com/pricing/" target="_blank" rel="noopener">PandaDoc pricing</a> <span class="src-date">Accessed 13 Nov 2026.</span></span> <span class="src-cluster"><a class="src-link" href="https://support.pandadoc.com/en/articles/9715033-compare-subscription-plan-features" target="_blank" rel="noopener">PandaDoc plan comparison</a> <span class="src-date">Accessed 13 Nov 2026.</span></span> <span class="src-cluster"><a class="src-link" href="https://www.docusign.com/products-and-pricing" target="_blank" rel="noopener">DocuSign plans and pricing</a> <span class="src-date">Accessed 13 Nov 2026.</span></span> <span class="src-cluster"><a class="src-link" href="https://www.docusign.com/blog/docusign-plans-and-pricing" target="_blank" rel="noopener">DocuSign plans article</a> <span class="src-date">Accessed 13 Nov 2026.</span></span> <span class="src-cluster"><a class="src-link" href="https://www.nodshake.com/guides/docusign-cost-per-envelope" target="_blank" rel="noopener">nodshake overage table</a> <span class="src-date">Updated 15 Oct 2026. Accessed 13 Nov 2026.</span></span> <span class="src-cluster"><a class="src-link" href="https://www.jotform.com/pricing/" target="_blank" rel="noopener">Jotform pricing</a> <span class="src-date">Accessed 13 Nov 2026.</span></span> <span class="src-cluster"><a class="src-link" href="https://www.jotform.com/products/sign/" target="_blank" rel="noopener">Jotform Sign</a> <span class="src-date">Accessed 13 Nov 2026.</span></span></p>
""".replace("__JOTFORM_PRICING__", JOTFORM_PRICING)

FORMULA_DEFAULT = (
    "3 senders. 20 documents a month, 240 in the year. Annual, paid upfront. HIPAA is off. "
    "Automation share is 0%. No PandaDoc credit pack is added. "
    "PandaDoc Starter is 3 seats at $19 a month for a year, $684. "
    "PandaDoc Business is 3 seats at $49 a month for a year, $1,764. "
    "DocuSign Standard is 3 users at $25 a month, $900. "
    "Allowance for this team: 300. Envelopes over that: 0. "
    "Standard overage rate $3.60. Business Pro overage rate $5.80. "
    "DocuSign Business Pro is 3 users at $40 a month, $1,440. "
    "Jotform Sign one account is Bronze, $408. One account per user is $1,224."
)

SCRIPT = r"""
<script>
function calcEsign(input) {
  var seats = Math.max(1, Math.round(Number(input.seats) || 1));
  var docs = Math.max(0, Math.round(Number(input.docs) || 0));
  var billing = input.billing === "monthly" ? "monthly" : "annual";
  var hipaa = input.hipaa === "yes";
  var auto = Math.max(0, Math.min(100, Math.round(Number(input.auto) || 0)));
  var stdRate = Number(input.stdRate);
  if (!isFinite(stdRate) || stdRate < 0) stdRate = 0;
  var bpRate = Number(input.bpRate);
  if (!isFinite(bpRate) || bpRate < 0) bpRate = 0;
  var annual = billing === "annual";
  var autoMonth = Math.round(docs * auto / 100);
  var stdRateCents = Math.round(stdRate * 100);
  var bpRateCents = Math.round(bpRate * 100);
  var yearDocs = docs * 12;
  var allowance = annual ? 100 * seats : 10 * seats;
  var over = annual ? Math.max(0, yearDocs - 100 * seats) : Math.max(0, docs - 10 * seats) * 12;
  var pandaQuote = hipaa ? "quote (Enterprise)" : "";
  var creditUnknown = !hipaa && autoMonth > 0;
  var starterSeat = hipaa ? null : (annual ? 1900 : 3500) * seats * 12;
  var businessSeat = hipaa ? null : (annual ? 4900 : 6500) * seats * 12;
  var dsQuote = (hipaa || seats > 50) ? "quote (Enhanced)" : "";
  var standard = dsQuote ? null : (annual ? 2500 : 4500) * seats * 12 + over * stdRateCents;
  var businessPro = dsQuote ? null : (annual ? 4000 : 6500) * seats * 12 + over * bpRateCents;
  var personal = "off";
  var personalCents = null;
  if (seats === 1) {
    if (hipaa) personal = "hipaa";
    else if (docs > 5) personal = "over";
    else {
      personal = "price";
      personalCents = annual ? 12000 : 18000;
    }
  }
  var jfName = "Enterprise";
  var jfOne = null;
  var jfPer = null;
  var jfQuote = "";
  var jfLimit = 0;
  if (!hipaa && docs <= 10) {
    jfName = "Starter";
    jfLimit = 10;
    jfOne = 0;
    jfPer = 0;
  } else if (!hipaa && docs <= 100) {
    jfName = "Bronze";
    jfLimit = 100;
    jfOne = annual ? 40800 : 46800;
    jfPer = jfOne * seats;
  } else if (!hipaa && docs <= 250) {
    jfName = "Silver";
    jfLimit = 250;
    jfOne = annual ? 46800 : 58800;
    jfPer = jfOne * seats;
  } else if (docs <= 1000) {
    jfName = "Gold";
    jfLimit = 1000;
    jfOne = annual ? 118800 : 154800;
    jfPer = jfOne * seats;
  } else {
    jfName = "Enterprise";
    jfQuote = "quote (Enterprise)";
  }
  return {
    seats: seats,
    docs: docs,
    billing: billing,
    hipaa: hipaa,
    auto: auto,
    autoMonth: autoMonth,
    yearDocs: yearDocs,
    allowance: allowance,
    over: over,
    pandaQuote: pandaQuote,
    creditUnknown: creditUnknown,
    starterSeat: starterSeat,
    businessSeat: businessSeat,
    dsQuote: dsQuote,
    standard: standard,
    businessPro: businessPro,
    stdRateCents: stdRateCents,
    bpRateCents: bpRateCents,
    personal: personal,
    personalCents: personalCents,
    jfName: jfName,
    jfOne: jfOne,
    jfPer: jfPer,
    jfQuote: jfQuote,
    jfLimit: jfLimit
  };
}

function esDefaultRates(billing) {
  if (billing === "monthly") return { std: 540, bp: 780 };
  return { std: 360, bp: 580 };
}

function esMoney(cents) {
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

function esRate(cents) {
  var v = Math.abs(Math.round(cents));
  var dollars = Math.floor(v / 100);
  var rem = v % 100;
  return "$" + dollars + "." + (rem < 10 ? "0" : "") + rem;
}

function esFormula(c) {
  var parts = [];
  parts.push(c.seats + (c.seats === 1 ? " sender." : " senders."));
  parts.push(c.docs + " documents a month, " + c.yearDocs + " in the year.");
  parts.push(c.billing === "annual" ? "Annual, paid upfront." : "Month-to-month.");
  parts.push(c.hipaa ? "HIPAA is on." : "HIPAA is off.");
  if (c.autoMonth > 0) {
    parts.push("Automation share is " + c.auto + "%, " + c.autoMonth + " documents a month. The PandaDoc year total leaves out an unknown credit pack.");
  } else {
    parts.push("Automation share is " + c.auto + "%. No PandaDoc credit pack is added.");
  }
  if (c.pandaQuote) {
    parts.push("PandaDoc Starter and Business are " + c.pandaQuote + ".");
  } else {
    var stRate = c.billing === "annual" ? 19 : 35;
    var buRate = c.billing === "annual" ? 49 : 65;
    parts.push("PandaDoc Starter is " + c.seats + " seats at $" + stRate + " a month for a year, " + esMoney(c.starterSeat) + ".");
    parts.push("PandaDoc Business is " + c.seats + " seats at $" + buRate + " a month for a year, " + esMoney(c.businessSeat) + ".");
  }
  if (c.dsQuote) {
    parts.push("DocuSign Standard and Business Pro are " + c.dsQuote + ".");
  } else {
    var stdMonthly = c.billing === "annual" ? 25 : 45;
    var bpMonthly = c.billing === "annual" ? 40 : 65;
    parts.push("DocuSign Standard is " + c.seats + " users at $" + stdMonthly + " a month, " + esMoney(c.standard) + ".");
    parts.push("Allowance for this team: " + c.allowance + ". Envelopes over that: " + c.over + ".");
    parts.push("Standard overage rate " + esRate(c.stdRateCents) + ". Business Pro overage rate " + esRate(c.bpRateCents) + ".");
    parts.push("DocuSign Business Pro is " + c.seats + " users at $" + bpMonthly + " a month, " + esMoney(c.businessPro) + ".");
  }
  if (c.personal === "price") parts.push("DocuSign Personal is " + esMoney(c.personalCents) + ".");
  if (c.personal === "over") parts.push("DocuSign Personal is not offered at this volume.");
  if (c.jfQuote) parts.push("Jotform Sign is " + c.jfQuote + ".");
  else {
    parts.push("Jotform Sign one account is " + c.jfName + ", " + esMoney(c.jfOne) + ".");
    parts.push("One account per user is " + esMoney(c.jfPer) + ".");
  }
  return parts.join(" ");
}

function esPandaCell(c, seat) {
  if (c.pandaQuote) return c.pandaQuote;
  if (c.creditUnknown) return esMoney(seat) + " + unknown";
  return esMoney(seat);
}

function esKnown(cents) {
  return cents !== null && isFinite(cents);
}

function renderEsign(event) {
  var billingEl = document.getElementById("es-billing");
  var stdEl = document.getElementById("es-std-over");
  var bpEl = document.getElementById("es-bp-over");
  if (event && event.target && event.target.id === "es-billing") {
    var next = esDefaultRates(billingEl.value);
    var prev = esDefaultRates(billingEl.value === "monthly" ? "annual" : "monthly");
    if (Math.round(Number(stdEl.value) * 100) === prev.std) stdEl.value = (next.std / 100).toFixed(2);
    if (Math.round(Number(bpEl.value) * 100) === prev.bp) bpEl.value = (next.bp / 100).toFixed(2);
  }
  var c = calcEsign({
    seats: document.getElementById("es-seats").value,
    docs: document.getElementById("es-docs").value,
    billing: billingEl.value,
    hipaa: document.getElementById("es-hipaa").value,
    auto: document.getElementById("es-auto").value,
    stdRate: stdEl.value,
    bpRate: bpEl.value
  });
  document.getElementById("es-seats-val").textContent = String(c.seats);
  document.getElementById("es-docs-val").textContent = String(c.docs);
  document.getElementById("es-auto-val").textContent = c.auto + "%";
  document.getElementById("es-std-over-val").textContent = esRate(c.stdRateCents);
  document.getElementById("es-bp-over-val").textContent = esRate(c.bpRateCents);
  var rows = [];
  rows.push({ name: "PandaDoc Starter", text: esPandaCell(c, c.starterSeat), cents: c.pandaQuote || c.creditUnknown ? null : c.starterSeat });
  rows.push({ name: "PandaDoc Business", text: esPandaCell(c, c.businessSeat), cents: c.pandaQuote || c.creditUnknown ? null : c.businessSeat });
  rows.push({ name: "DocuSign Standard", text: c.dsQuote || esMoney(c.standard), cents: c.dsQuote ? null : c.standard });
  rows.push({ name: "DocuSign Business Pro", text: c.dsQuote || esMoney(c.businessPro), cents: c.dsQuote ? null : c.businessPro });
  if (c.personal === "price") rows.push({ name: "DocuSign Personal", text: esMoney(c.personalCents), cents: c.personalCents });
  if (c.personal === "over") rows.push({ name: "DocuSign Personal", text: "not offered", cents: null });
  rows.push({ name: "Jotform Sign, one account", text: c.jfQuote || esMoney(c.jfOne), cents: c.jfQuote ? null : c.jfOne });
  rows.push({ name: "Jotform Sign, one account per user", text: c.jfQuote || esMoney(c.jfPer), cents: c.jfQuote ? null : c.jfPer });
  var known = [];
  rows.forEach(function (row) {
    if (esKnown(row.cents)) known.push(row);
  });
  known.sort(function (a, b) { return a.cents - b.cents; });
  var lowest = known.length ? known[0] : null;
  var tied = [];
  if (lowest) {
    known.forEach(function (row) {
      if (row.cents === lowest.cents) tied.push(row.name);
    });
  }
  document.getElementById("shell-product").textContent = lowest ? lowest.name : "Year-1 list price";
  document.getElementById("shell-big").textContent = lowest ? esMoney(lowest.cents) : "unknown";
  document.getElementById("shell-sub").textContent = "";
  document.getElementById("shell-best").textContent = lowest ? "Lowest Year-1 cost: " + tied.join(" and ") + "." : "";
  var bars = [
    { row: "shell-row-base", amt: "shell-amt-base", title: "shell-title-base", text: rows[0].text, cents: rows[0].cents },
    { row: "shell-row-seats", amt: "shell-amt-seats", title: "shell-title-seats", text: rows[2].text, cents: rows[2].cents },
    { row: "shell-row-hidden", amt: "shell-amt-hidden", title: "shell-title-hidden", text: rows[rows.length - 2].text, cents: rows[rows.length - 2].cents }
  ];
  document.getElementById("shell-title-base").textContent = "PandaDoc Starter";
  document.getElementById("shell-title-seats").textContent = "DocuSign Standard";
  document.getElementById("shell-title-hidden").textContent = "Jotform Sign";
  var maxCents = 1;
  bars.forEach(function (bar) {
    if (esKnown(bar.cents) && bar.cents > maxCents) maxCents = bar.cents;
  });
  bars.forEach(function (bar) {
    var share = esKnown(bar.cents) ? (Math.round(bar.cents / maxCents * 1000) / 10) : 0;
    var label = esKnown(bar.cents) ? esMoney(bar.cents) : (String(bar.text).indexOf("quote") === 0 ? "quote" : "unknown");
    document.getElementById(bar.amt).textContent = label;
    document.getElementById(bar.row).style.setProperty("--wb-bar-share", share + "%");
  });
  var html = "";
  rows.forEach(function (row) {
    html += "<tr><td data-label=\"Plan\">" + row.name + "</td><td data-label=\"Year 1\">" + row.text + "</td></tr>";
  });
  document.getElementById("es-body").innerHTML = html;
  document.getElementById("shell-math").textContent = esFormula(c);
}

["es-seats", "es-docs", "es-billing", "es-hipaa", "es-auto", "es-std-over", "es-bp-over"].forEach(function (id) {
  var el = document.getElementById(id);
  el.addEventListener("input", renderEsign);
  el.addEventListener("change", renderEsign);
});
renderEsign();
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
    blob = TITLE + DESCRIPTION + LEAD + CONTROLS + REST + FORMULA_DEFAULT + SCRIPT
    for banned in ("\u2014", "Best option", "Winner", "SaaSTruth", "answer first", "test section", "placeholder"):
        if banned.lower() in blob.lower():
            raise SystemExit("banned copy: " + banned)
    workbench = render_workbench(
        CONTROLS,
        controls_title="Your sending",
        chart_title="Year-1 list price",
        cta_href="#es-costs",
        cta_label="Cost table",
        cta_vendor="saasbill",
    )
    for old, new in (
        ('class="wb-vbar-container"', 'class="wb-vbar-container wb-vbar-separate"'),
        ('id="shell-row-base" style="flex: 40 1 0px;"', 'id="shell-row-base" style="--wb-bar-share: 76%;"'),
        ('id="shell-row-seats" style="flex: 8 1 0px;"', 'id="shell-row-seats" style="--wb-bar-share: 100%;"'),
        ('id="shell-row-hidden" style="flex: 52 1 0px;"', 'id="shell-row-hidden" style="--wb-bar-share: 45.3%;"'),
        ('id="shell-product">Year-1 total<', 'id="shell-product">Jotform Sign, one account<'),
        ('id="shell-big">$0<', 'id="shell-big">$408<'),
        ('id="shell-sub">Matches advertised price ($0 hidden fees).</p>', 'id="shell-sub"></p>'),
        ('id="shell-title-base">Sticker Price<', 'id="shell-title-base">PandaDoc Starter<'),
        ('id="shell-sub-base">Advertised price<', 'id="shell-sub-base">Year 1<'),
        ('id="shell-amt-base">$0<', 'id="shell-amt-base">$684<'),
        ('id="shell-title-seats">Other sticker fees<', 'id="shell-title-seats">DocuSign Standard<'),
        ('id="shell-sub-seats">Included in the sticker<', 'id="shell-sub-seats">Year 1<'),
        ('id="shell-amt-seats">$0<', 'id="shell-amt-seats">$900<'),
        ('id="shell-title-hidden">Hidden Cost Gap<', 'id="shell-title-hidden">Jotform Sign<'),
        ('id="shell-sub-hidden">Fees above the advertised price<', 'id="shell-sub-hidden">One account<'),
        ('id="shell-amt-hidden">$0<', 'id="shell-amt-hidden">$408<'),
        ('id="shell-best"></div>', 'id="shell-best">Lowest Year-1 cost: Jotform Sign, one account.</div>'),
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
    body = (
        '<section class="hero">'
        "<h1>What does PandaDoc cost versus DocuSign and Jotform Sign in Year 1?</h1>"
        '<p class="lead">%s</p>' % LEAD
        + "</section>"
        + workbench
        + REST
        + SCRIPT
    )
    if LEAD and body.count(LEAD) != 1:
        raise SystemExit("lead repeated before render")
    render_page(
        REL,
        TITLE,
        DESCRIPTION,
        CANONICAL,
        wrap_calculator_shell(body),
        faqs=None,
        published_date="2026-11-13",
        modified_datetime="2026-11-13T00:00:00+00:00",
        show_affiliate_note=True,
    )
    copy_to_root(REL)


if __name__ == "__main__":
    build()
