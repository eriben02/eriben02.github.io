"""SOC 2 Year-1 cost: Vanta and Drata AWS list prices, plus the CPA audit.

Sources checked 2026-11-07. Unknown stays the word unknown.
AWS Marketplace figures are list prices for the stated headcount band.
They are not negotiated medians. Comp AI has no public rate card.
"""
import os
import shutil

from layout import BASE_DIR, PUBLIC_DIR, render_page, render_workbench, wrap_calculator_shell

TITLE = "SOC 2 cost: Vanta, Drata, Comp AI – saasbill.io"
DESCRIPTION = (
    "For 1 to 20 people, Vanta Essentials is a $14,000 AWS list price and "
    "Drata Foundation is $15,000. The CPA audit is separate. Checked 7 Nov 2026."
)
REL = "compliance/vanta-vs-drata-vs-comp-ai-soc2-negotiation-benchmarks/index.html"
CANONICAL = "/compliance/vanta-vs-drata-vs-comp-ai-soc2-negotiation-benchmarks/"

CONTROLS = """
        <div class="wb-control-item">
          <label class="wb-control-label" for="soc-platform">Platform</label>
          <select id="soc-platform" class="wb-tool-select" aria-label="Platform" data-track="calculator-control" data-control="platform">
            <option value="vanta-essentials" selected>Vanta Essentials</option>
            <option value="vanta-plus">Vanta Plus</option>
            <option value="vanta-professional">Vanta Professional</option>
            <option value="vanta-quote">Vanta Enterprise</option>
            <option value="drata-foundation">Drata Foundation</option>
            <option value="drata-quote">Drata Advanced</option>
            <option value="comp-ai">Comp AI</option>
          </select>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="soc-band">Employees</label>
          <select id="soc-band" class="wb-tool-select" aria-label="Employee band" data-track="calculator-control" data-control="employees">
            <option value="1-20" selected>1 to 20</option>
            <option value="21-50">21 to 50</option>
            <option value="51">51 or more</option>
          </select>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="soc-audit">CPA auditor <span class="val-pill" id="soc-audit-val">$30,000</span></label>
          <div class="wb-slider-row">
            <input type="range" id="soc-audit" min="10000" max="50000" step="1000" value="30000" aria-label="CPA auditor fee" data-track="calculator-control" data-control="auditor" />
          </div>
          <p class="wb-budget-subnote">Vanta cites a typical SOC 2 audit fee of $10,000 to $50,000. The default is the middle of that range, not a measured median.</p>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="soc-trust">Vanta Trust Center add-on</label>
          <select id="soc-trust" class="wb-tool-select" aria-label="Trust Center add-on" data-track="calculator-control" data-control="trust">
            <option value="none" selected>None</option>
            <option value="standard">Trust Center, $6,000</option>
            <option value="advanced">Trust Center Advanced, $10,000</option>
          </select>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="soc-quest">Vanta questionnaire add-on</label>
          <select id="soc-quest" class="wb-tool-select" aria-label="Questionnaire add-on" data-track="calculator-control" data-control="questionnaires">
            <option value="none" selected>None</option>
            <option value="qa">144 a year, $10,000</option>
            <option value="advanced">288 a year, $16,000</option>
          </select>
        </div>
        <label class="wb-budget-subnote"><input type="checkbox" id="soc-ctm" data-track="calculator-control" data-control="ctm" /> Customer Trust Management, $22,250</label>
        <label class="wb-budget-subnote"><input type="checkbox" id="soc-tprm" data-track="calculator-control" data-control="tprm" /> TPRM, up to 50 vendors, $13,600</label>
        <label class="wb-budget-subnote"><input type="checkbox" id="soc-ftr" data-track="calculator-control" data-control="ftr" /> AWS FTR module, $7,500</label>
        <label class="wb-budget-subnote"><input type="checkbox" id="soc-tools" data-track="calculator-control" data-control="tools" /> Year-1 security-tools allowance, $10,000</label>
        <p class="wb-budget-subnote">Those add-on dollars are Vanta's AWS list for 1 to 20 employees. On any other platform, or on a larger Vanta band, a selected add-on makes that line unknown. The $10,000 allowance is the security-tools figure Vanta cites, counted in Year-1 only.</p>
"""

REST = r"""
<section id="soc-compare">
  <h2>Published lists plus this auditor setting</h2>
  <p>Each row is the 12-month AWS list, where one exists for this headcount, plus the auditor slider. Add-ons are not in this table. Comp AI has no public price, so its row stays unknown.</p>
  <div class="table-wrap editorial-gap-table mobile-cards">
    <table>
      <caption>Year-1 and Year-2 before add-ons. AWS list prices, not negotiated medians.</caption>
      <thead>
        <tr>
          <th>Platform</th>
          <th>12-month list</th>
          <th>Year-1</th>
          <th>Year-2</th>
        </tr>
      </thead>
      <tbody id="soc-compare-body">
        <tr><td data-label="Platform">Vanta Essentials</td><td data-label="12-month list">$14,000</td><td data-label="Year-1">$44,000</td><td data-label="Year-2">$44,000</td></tr>
        <tr><td data-label="Platform">Vanta Plus</td><td data-label="12-month list">$21,500</td><td data-label="Year-1">$51,500</td><td data-label="Year-2">$51,500</td></tr>
        <tr><td data-label="Platform">Vanta Professional</td><td data-label="12-month list">$23,000</td><td data-label="Year-1">$53,000</td><td data-label="Year-2">$53,000</td></tr>
        <tr><td data-label="Platform">Drata Foundation</td><td data-label="12-month list">$15,000</td><td data-label="Year-1">$45,000</td><td data-label="Year-2">$45,000</td></tr>
        <tr><td data-label="Platform">Vanta Enterprise</td><td data-label="12-month list">unknown</td><td data-label="Year-1">unknown</td><td data-label="Year-2">unknown</td></tr>
        <tr><td data-label="Platform">Drata Advanced or Enterprise</td><td data-label="12-month list">unknown</td><td data-label="Year-1">unknown</td><td data-label="Year-2">unknown</td></tr>
        <tr><td data-label="Platform">Comp AI</td><td data-label="12-month list">unknown</td><td data-label="Year-1">unknown</td><td data-label="Year-2">unknown</td></tr>
      </tbody>
    </table>
  </div>
  <p class="summary-caveat">Year-2 repeats the same 12-month list and the same auditor setting. Auto-renewal notice windows were not on the official pages checked on 7 Nov 2026, so that term is unknown.</p>
</section>

<section id="soc-split">
  <h2>This selection, split</h2>
  <div class="table-wrap editorial-gap-table mobile-cards">
    <table>
      <caption>Platform, add-ons, and the CPA auditor for the controls above.</caption>
      <thead>
        <tr>
          <th>Piece</th>
          <th>Year-1</th>
          <th>Year-2</th>
        </tr>
      </thead>
      <tbody id="soc-split-body">
        <tr><td data-label="Piece">Vanta Essentials</td><td data-label="Year-1">$14,000</td><td data-label="Year-2">$14,000</td></tr>
        <tr><td data-label="Piece">Add-ons</td><td data-label="Year-1">none</td><td data-label="Year-2">none</td></tr>
        <tr><td data-label="Piece">CPA auditor</td><td data-label="Year-1">$30,000</td><td data-label="Year-2">$30,000</td></tr>
        <tr><td data-label="Piece">Total</td><td data-label="Year-1">$44,000</td><td data-label="Year-2">$44,000</td></tr>
      </tbody>
    </table>
  </div>
</section>

<section>
  <h2>Prices checked on 7 Nov 2026</h2>
  <div class="table-wrap editorial-gap-table mobile-cards">
    <table>
      <caption>AWS Marketplace list prices for the stated size band. Official sites do not print these dollars.</caption>
      <thead>
        <tr>
          <th>Item</th>
          <th>Published price</th>
          <th>In the Year-1 total</th>
        </tr>
      </thead>
      <tbody>
        <tr><td data-label="Item">Vanta Essentials, Plus, Professional</td><td data-label="Published price">$14,000, $21,500, and $23,000 for 12 months, starting cost for 1 to 20 employees, on AWS Marketplace.</td><td data-label="In the Year-1 total">Used only for that band. Larger headcounts are unknown.</td></tr>
        <tr><td data-label="Item">Vanta plan names on vanta.com</td><td data-label="Published price">Essentials, Plus, Professional, and Enterprise. No dollars on the site. Essentials is one framework. Plus adds 25 questionnaires a year and Access Management. Professional adds 144 questionnaires a year, risk, and Advanced Trust Center. Enterprise is custom.</td><td data-label="In the Year-1 total">Enterprise is unknown. The questionnaire counts on the site are not the same line as the AWS add-on prices.</td></tr>
        <tr><td data-label="Item">Vanta add-ons, 1 to 20 employees</td><td data-label="Published price">Trust Center $6,000. Trust Center Advanced $10,000. Questionnaire Automation $10,000 (144 a year). Questionnaire Automation Advanced $16,000 (288 a year). Customer Trust Management $22,250. TPRM up to 50 vendors $13,600. AWS FTR module $7,500.</td><td data-label="In the Year-1 total">Added only when selected, and only on a Vanta row for 1 to 20 employees. Trust Center tiers are one choice. Questionnaire tiers are one choice.</td></tr>
        <tr><td data-label="Item">Vanta audit</td><td data-label="Published price">Not included in the subscription. Professional services and the auditor are separate. The Seamless Auditor Bundle price is unknown.</td><td data-label="In the Year-1 total">The auditor slider, not the platform line.</td></tr>
        <tr><td data-label="Item">SOC 2 audit fee</td><td data-label="Published price">Vanta's guide: typical $10,000 to $50,000. All-in first SOC 2 $10,000 to $80,000 or more. Big Four or a large enterprise: low six figures or more. Type 1 is a point in time. Type 2 covers 3 to 12 months and usually costs more.</td><td data-label="In the Year-1 total">The slider is the typical audit range only. It is not the all-in range and it does not split Type 1 from Type 2.</td></tr>
        <tr><td data-label="Item">Prep ranges Vanta cites</td><td data-label="Published price">Readiness from about $10,000. Security tools from about $10,000. Additional prep from about $10,000. These are vendor-published ranges, not SaaSBill measurements.</td><td data-label="In the Year-1 total">Off unless the security-tools allowance is checked. Readiness and additional prep stay out of the total.</td></tr>
        <tr><td data-label="Item">Drata Foundation</td><td data-label="Published price">$15,000 for 12 months on AWS Marketplace, for 1 to 50 employees. One listed dimension. Orders are non-cancellable and fees are non-refundable on that listing.</td><td data-label="In the Year-1 total">Used for 1 to 20 and for 21 to 50. At 51 or more it is unknown.</td></tr>
        <tr><td data-label="Item">Drata plans on drata.com</td><td data-label="Published price">Foundation, Advanced, and Enterprise. No dollars on the site. Foundation is up to 50 employees and one pre-mapped framework among SOC 2, ISO 27001, Cyber Essentials, HIPAA, and GDPR, plus Trust Center Standard, AI Questionnaire Assistance Standard, Risk Management, Custom Controls, Compliance as Code, and an Open API. Advanced adds any available framework and paid extras. Enterprise adds Risk Management Pro, Compliance as Code Pro, User Access Review, and Agentic TPRM Assessment.</td><td data-label="In the Year-1 total">Advanced and Enterprise list prices are unknown.</td></tr>
        <tr><td data-label="Item">Comp AI</td><td data-label="Published price">No public rate card. The quote depends on frameworks, headcount, timeline, and whether an audit, pen test, or trust center is included. Comp AI does not issue the SOC 2 report. A CPA firm does. Whether the audit is included is unknown until an order form says so.</td><td data-label="In the Year-1 total">unknown</td></tr>
        <tr><td data-label="Item">Auto-renewal notice</td><td data-label="Published price">Not stated on the official pages checked today.</td><td data-label="In the Year-1 total">unknown. Year-2 is the same list again, not a renewal quote.</td></tr>
      </tbody>
    </table>
  </div>
  <details class="full-table-disclosure below-disclosure">
    <summary class="full-table-summary"><span class="below-disclosure-title">What sits on top of the platform</span><span class="full-table-toggle-pill">Show</span></summary>
    <div class="full-table-body">
      <ul class="key-list">
        <li>The platform quote is sales-led. An AWS list price is not what every buyer pays.</li>
        <li>Extra frameworks, Trust Center, questionnaire, and TPRM modules, implementation, a pen test, and the CPA audit stack on the platform fee.</li>
        <li>Drata's AWS listing says orders are non-cancellable and fees are non-refundable.</li>
        <li>Forum threads on SOC 2 describe Vanta and Drata as expensive for small teams, and they separate the platform fee from the CPA invoice. Those threads are not prices, and this page does not quote them as dollars.</li>
      </ul>
    </div>
  </details>
  <p class="src-cluster"><a class="src-link" href="https://aws.amazon.com/marketplace/pp/prodview-5ophamrbfxt44">Vanta on AWS Marketplace</a> <span class="src-date">Accessed 2026-11-07</span></p>
  <p class="src-cluster"><a class="src-link" href="https://www.vanta.com/pricing">Vanta pricing</a> <span class="src-date">Accessed 2026-11-07</span></p>
  <p class="src-cluster"><a class="src-link" href="https://www.vanta.com/collection/soc-2/soc-2-audit-cost">Vanta, SOC 2 audit cost</a> <span class="src-date">Accessed 2026-11-07</span></p>
  <p class="src-cluster"><a class="src-link" href="https://drata.com/plans">Drata plans</a> <span class="src-date">Accessed 2026-11-07</span></p>
  <p class="src-cluster"><a class="src-link" href="https://aws.amazon.com/marketplace/pp/prodview-3xw4sjqv2pb22">Drata on AWS Marketplace</a> <span class="src-date">Accessed 2026-11-07</span></p>
  <p class="src-cluster"><a class="src-link" href="https://www.trycomp.ai/pricing" target="_blank" rel="noopener">Comp AI pricing</a> <span class="src-date">Accessed 2026-11-07</span></p>
  <p class="src-cluster"><a class="src-link" href="https://www.reddit.com/r/soc2/">r/soc2</a> <span class="src-date">Accessed 2026-11-07</span></p>
</section>
<script>
function socMoney(dollars) {
  if (dollars < 0) return "unknown";
  return "$" + Math.round(dollars).toLocaleString("en-US");
}

function socPlatformList(platform, band) {
  if (platform === "vanta-essentials") return band === "1-20" ? 14000 : -1;
  if (platform === "vanta-plus") return band === "1-20" ? 21500 : -1;
  if (platform === "vanta-professional") return band === "1-20" ? 23000 : -1;
  if (platform === "drata-foundation") return band === "51" ? -1 : 15000;
  return -1;
}

function socPlatformName(platform) {
  if (platform === "vanta-essentials") return "Vanta Essentials";
  if (platform === "vanta-plus") return "Vanta Plus";
  if (platform === "vanta-professional") return "Vanta Professional";
  if (platform === "vanta-quote") return "Vanta Enterprise";
  if (platform === "drata-foundation") return "Drata Foundation";
  if (platform === "drata-quote") return "Drata Advanced or Enterprise";
  return "Comp AI";
}

function calcSoc2(input) {
  var platform = String(input.platform || "vanta-essentials");
  var band = String(input.band || "1-20");
  var auditor = Math.round(Number(input.auditor) || 30000);
  if (auditor < 10000) auditor = 10000;
  if (auditor > 50000) auditor = 50000;
  var list = socPlatformList(platform, band);
  var vantaBand = platform.indexOf("vanta") === 0 && band === "1-20";
  var trust = input.trust === "standard" ? 6000 : (input.trust === "advanced" ? 10000 : 0);
  var quest = input.quest === "qa" ? 10000 : (input.quest === "advanced" ? 16000 : 0);
  var picked = trust + quest + (input.ctm ? 22250 : 0) + (input.tprm ? 13600 : 0) + (input.ftr ? 7500 : 0);
  var modules = picked === 0 ? 0 : (vantaBand ? picked : -1);
  var tools = input.tools ? 10000 : 0;
  var year1 = -1;
  var year2 = -1;
  if (list >= 0 && modules >= 0) {
    year2 = list + modules + auditor;
    year1 = year2 + tools;
  }
  return {
    name: socPlatformName(platform),
    platform: platform,
    band: band,
    list: list,
    auditor: auditor,
    modules: modules,
    tools: tools,
    year1: year1,
    year2: year2
  };
}

function socLowest(band, auditor) {
  var rows = [
    ["Vanta Essentials", band === "1-20" ? 14000 + auditor : -1],
    ["Vanta Plus", band === "1-20" ? 21500 + auditor : -1],
    ["Vanta Professional", band === "1-20" ? 23000 + auditor : -1],
    ["Drata Foundation", band === "51" ? -1 : 15000 + auditor]
  ];
  var known = [];
  rows.forEach(function (row) { if (row[1] >= 0) known.push(row); });
  if (!known.length) {
    return "No published platform list for this headcount. The CPA auditor setting is " + socMoney(auditor) + ". Vanta, Drata, and Comp AI stay unknown.";
  }
  var low = known[0][1];
  known.forEach(function (row) { if (row[1] < low) low = row[1]; });
  var lows = [];
  var rest = [];
  known.forEach(function (row) {
    if (row[1] === low) lows.push(row[0]);
    else rest.push(row[0] + " " + socMoney(row[1]));
  });
  var tail = rest.length ? rest.join(". ") + ". " : "";
  var extra = band === "1-20"
    ? "Before add-ons. Vanta Enterprise, Drata Advanced or Enterprise, and Comp AI are unknown."
    : "Vanta's published AWS list is for 1 to 20 employees, so it is unknown here. Drata Advanced or Enterprise, and Comp AI, are unknown.";
  return "Lowest Year-1 cost: " + lows.join(" and ") + ", " + socMoney(low) + ". " + tail + extra;
}

function socRead() {
  return {
    platform: document.getElementById("soc-platform").value,
    band: document.getElementById("soc-band").value,
    auditor: document.getElementById("soc-audit").value,
    trust: document.getElementById("soc-trust").value,
    quest: document.getElementById("soc-quest").value,
    ctm: document.getElementById("soc-ctm").checked,
    tprm: document.getElementById("soc-tprm").checked,
    ftr: document.getElementById("soc-ftr").checked,
    tools: document.getElementById("soc-tools").checked
  };
}

function socCell(amount, noneLabel) {
  if (amount < 0) return "unknown";
  if (amount === 0 && noneLabel) return "none";
  return socMoney(amount);
}

function renderSoc2() {
  var c = calcSoc2(socRead());
  document.getElementById("soc-audit-val").textContent = socMoney(c.auditor);
  var line = socLowest(c.band, c.auditor);
  var label = "Lowest Year-1 cost:";
  var best = document.getElementById("shell-best");
  if (line.indexOf(label) === 0) best.innerHTML = "<strong>" + label + "</strong>" + line.slice(label.length);
  else best.textContent = line;
  document.getElementById("shell-big").textContent = socMoney(c.year1);
  document.getElementById("shell-product").textContent = c.name + ", Year-1";
  document.getElementById("shell-sub").textContent = "Platform " + socMoney(c.list) + ". Auditor " + socMoney(c.auditor) + ". Add-ons " + socCell(c.modules, true) + (c.tools ? " plus " + socMoney(c.tools) + " in Year-1." : ".");
  var addonYear1 = c.modules < 0 ? -1 : c.modules + c.tools;
  var bars = [
    ["shell-row-base", "shell-amt-base", "shell-title-base", "shell-sub-base", "Platform", c.list, "12-month AWS list, or unknown"],
    ["shell-row-seats", "shell-amt-seats", "shell-title-seats", "shell-sub-seats", "Add-ons", addonYear1, "Modules and the Year-1 allowance"],
    ["shell-row-hidden", "shell-amt-hidden", "shell-title-hidden", "shell-sub-hidden", "CPA auditor", c.auditor, "Separate from the subscription"]
  ];
  var maxBar = 1;
  bars.forEach(function (bar) { if (bar[5] > maxBar) maxBar = bar[5]; });
  bars.forEach(function (bar) {
    var flex = bar[5] > 0 ? Math.max(12, Math.round(bar[5] / maxBar * 100)) : 12;
    document.getElementById(bar[0]).style.flex = flex + " 1 0px";
    document.getElementById(bar[1]).textContent = bar[5] === 0 ? "none" : socMoney(bar[5]);
    document.getElementById(bar[2]).textContent = bar[4];
    document.getElementById(bar[3]).textContent = bar[6];
  });
  document.getElementById("shell-sticker").textContent = socMoney(c.list);
  document.getElementById("shell-sticker-note").textContent = "12-month list";
  var above = c.year1 >= 0 && c.list >= 0 ? c.year1 - c.list : -1;
  document.getElementById("shell-gap").textContent = above < 0 ? "unknown" : (above === 0 ? "none" : "+" + socMoney(above));
  var labels = document.querySelectorAll("#shell-summary .summary-label");
  if (labels.length >= 2) {
    labels[0].textContent = "Platform";
    labels[1].textContent = "Auditor and add-ons";
  }
  var notes = document.querySelectorAll("#shell-summary .summary-scenario");
  if (notes.length >= 2) notes[1].textContent = "Year-2 is " + socMoney(c.year2);
  var addonText = c.modules < 0 ? "unknown" : socCell(c.modules + c.tools, true);
  document.getElementById("shell-math").textContent = c.name + ". Platform " + socMoney(c.list) + ". Add-ons " + (c.modules < 0 ? "unknown" : socCell(c.modules, true)) + ". Security-tools allowance " + socCell(c.tools, true) + ", Year-1 only. Auditor " + socMoney(c.auditor) + ". Year-1 " + socMoney(c.year1) + ". Year-2 " + socMoney(c.year2) + ".";
  function compareRow(name, list) {
    var total = list < 0 ? -1 : list + c.auditor;
    return "<tr><td data-label=\"Platform\">" + name + "</td><td data-label=\"12-month list\">" + socMoney(list) + "</td><td data-label=\"Year-1\">" + socMoney(total) + "</td><td data-label=\"Year-2\">" + socMoney(total) + "</td></tr>";
  }
  var vantaList = c.band === "1-20";
  var drataList = c.band !== "51";
  document.getElementById("soc-compare-body").innerHTML = ""
    + compareRow("Vanta Essentials", vantaList ? 14000 : -1)
    + compareRow("Vanta Plus", vantaList ? 21500 : -1)
    + compareRow("Vanta Professional", vantaList ? 23000 : -1)
    + compareRow("Drata Foundation", drataList ? 15000 : -1)
    + compareRow("Vanta Enterprise", -1)
    + compareRow("Drata Advanced or Enterprise", -1)
    + compareRow("Comp AI", -1);
  function splitRow(name, y1, y2) {
    return "<tr><td data-label=\"Piece\">" + name + "</td><td data-label=\"Year-1\">" + y1 + "</td><td data-label=\"Year-2\">" + y2 + "</td></tr>";
  }
  document.getElementById("soc-split-body").innerHTML = ""
    + splitRow(c.name, socMoney(c.list), socMoney(c.list))
    + splitRow("Add-ons", addonText, socCell(c.modules, true))
    + splitRow("CPA auditor", socMoney(c.auditor), socMoney(c.auditor))
    + splitRow("Total", socMoney(c.year1), socMoney(c.year2));
  if (typeof window.trackSaaSBillEvent === "function") {
    window.trackSaaSBillEvent("result_rendered", { page: "soc2-cost", platform: c.platform, band: c.band });
  }
}
["soc-platform", "soc-band", "soc-audit", "soc-trust", "soc-quest", "soc-ctm", "soc-tprm", "soc-ftr", "soc-tools"].forEach(function (id) {
  var el = document.getElementById(id);
  el.addEventListener("input", renderSoc2);
  el.addEventListener("change", renderSoc2);
});
renderSoc2();
</script>
"""

FAQS = [
    (
        "Does the Vanta subscription include the SOC 2 audit?",
        "No. Vanta says professional services and the auditor are separate from the subscription. The Seamless Auditor Bundle has no public price, so it is unknown. On AWS Marketplace, Essentials is $14,000, Plus is $21,500, and Professional is $23,000 for 12 months at 1 to 20 employees. Those are list prices. Vanta's own pricing page names Essentials, Plus, Professional, and Enterprise and does not print dollars. Enterprise is unknown.",
    ),
    (
        "What does Drata publish for SOC 2?",
        "Drata's plans page names Foundation, Advanced, and Enterprise and does not print dollars. Foundation is up to 50 employees and one pre-mapped framework. On AWS Marketplace, Foundation for 1 to 50 employees is $15,000 for 12 months. That listing says orders are non-cancellable and fees are non-refundable. Advanced and Enterprise list prices are unknown. The CPA audit is still a separate bill.",
    ),
    (
        "Does Comp AI issue the SOC 2 report?",
        "No. A CPA firm issues the report. Comp AI does not publish a rate card. The quote depends on frameworks, headcount, timeline, and whether an audit, pen test, or trust center is included. Treat an included audit as unknown until an order form says so.",
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
        raise SystemExit("em dash in soc2 copy")
    workbench = render_workbench(
        CONTROLS,
        controls_title="Your SOC 2 bill",
        chart_title="Year-1 split",
        cta_href="../../go/vanta/",
        cta_label="See Vanta pricing",
        cta_vendor="vanta",
    )
    needle = 'href="../../go/vanta/" data-track="vendor-cta" data-vendor="vanta" data-cta-location="workbench">See Vanta pricing &rarr;</a>'
    replacement = (
        'href="../../go/vanta/" target="_blank" rel="sponsored nofollow noopener" data-track="vendor-cta" data-vendor="vanta" data-cta-location="workbench">See Vanta pricing &rarr;</a>'
        '<a id="shell-cta-drata" class="btn-secondary" href="../../go/drata/" target="_blank" rel="sponsored nofollow noopener" data-track="vendor-cta" data-vendor="drata" data-cta-location="workbench">See Drata plans &rarr;</a>'
    )
    if needle not in workbench:
        raise SystemExit("Vanta CTA not found")
    workbench = workbench.replace(needle, replacement, 1)
    body = (
        '<section class="hero">'
        "<h1>Vanta, Drata, and Comp AI SOC 2 cost (2026)</h1>"
        '<p class="lead">For 1 to 20 employees, the AWS Marketplace list is $14,000 for Vanta Essentials and $15,000 for Drata Foundation, each for 12 months. '
        "The CPA audit is a separate bill, typically $10,000 to $50,000. Comp AI does not publish a price.</p>"
        "</section>"
        + workbench
        + REST
    )
    if "trycomp.ai" not in body or "/go/vanta/" not in body or "/go/drata/" not in body:
        raise SystemExit("missing CTA or Comp AI link")
    render_page(
        REL,
        TITLE,
        DESCRIPTION,
        CANONICAL,
        wrap_calculator_shell(body),
        faqs=FAQS,
        published_date="2026-11-07",
        show_affiliate_note=True,
    )
    copy_to_root(REL)


if __name__ == "__main__":
    build()
