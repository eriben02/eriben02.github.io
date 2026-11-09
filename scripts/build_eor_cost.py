"""Deel vs Rippling EOR: management fee, deposit lock-up, and unknowns.

Sources checked 2026-11-08. Unknown stays the word unknown.
The deposit is working capital, not a Year-1 vendor fee.
Rippling's EOR price is not on the pricing page, so the default comparison
does not name a lowest cost.
"""
import os
import shutil

from layout import BASE_DIR, PUBLIC_DIR, render_page, render_workbench, wrap_calculator_shell

TITLE = "Deel vs Rippling EOR cost – saasbill.io"
DESCRIPTION = (
    "Deel EOR starts at $599 per employee per month. One employee is $7,188 for the year. "
    "Rippling's EOR price is unknown. Checked 8 Nov 2026."
)
REL = "compare/deel-vs-rippling-eor-hidden-fx-and-offboarding-fees/index.html"
CANONICAL = "/compare/deel-vs-rippling-eor-hidden-fx-and-offboarding-fees/"

CONTROLS = """
        <div class="wb-control-item">
          <label class="wb-control-label" for="eor-employees">EOR employees <span class="val-pill" id="eor-employees-val">1</span></label>
          <div class="wb-slider-row">
            <input type="range" id="eor-employees" min="1" max="10" step="1" value="1" aria-label="EOR employees" data-track="calculator-control" data-control="employees" />
          </div>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="eor-salary">Example monthly salary <span class="val-pill" id="eor-salary-val">$5,000</span></label>
          <div class="wb-slider-row">
            <input type="range" id="eor-salary" min="1000" max="20000" step="500" value="5000" aria-label="Example monthly salary" data-track="calculator-control" data-control="salary" />
          </div>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="eor-rippling">Rippling figure</label>
          <select id="eor-rippling" class="wb-tool-select" aria-label="Rippling figure" data-track="calculator-control" data-control="rippling">
            <option value="unknown" selected>Unknown</option>
            <option value="blog">Blog $499 assumption</option>
            <option value="entered">Use the fee in Assumptions</option>
          </select>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="eor-deposit">Deposit multiple <span class="val-pill" id="eor-deposit-val">1.0×</span></label>
          <div class="wb-slider-row">
            <input type="range" id="eor-deposit" min="10" max="15" step="1" value="10" aria-label="Deel deposit multiple" data-track="calculator-control" data-control="deposit" />
          </div>
        </div>
        <details class="full-table-disclosure" id="eor-extras">
          <summary class="full-table-summary"><span class="below-disclosure-title">Assumptions</span><span class="full-table-toggle-pill">Show</span></summary>
          <div class="full-table-body">
            <p class="wb-budget-subnote">The salary is an example, not a list price. Rippling's blog says EOR starts at $499 a month and does not say per employee. Choosing that option multiplies $499 by headcount only as your assumption. The deposit slider stops at 1.5 times. Country rules and special cases can require about two months or more, and those are not on the slider.</p>
            <div class="wb-control-item">
              <label class="wb-control-label" for="eor-employer">Employer-cost percent <span class="val-pill" id="eor-employer-val">0%</span></label>
              <div class="wb-slider-row">
                <input type="range" id="eor-employer" min="0" max="40" step="1" value="0" aria-label="Employer cost percent" data-track="calculator-control" data-control="employer" />
              </div>
              <p class="wb-budget-subnote">Your country estimate. Not a vendor fee, and not a France or Germany default.</p>
            </div>
            <div class="wb-control-item">
              <label class="wb-control-label" for="eor-allow">Fixed allowances <span class="val-pill" id="eor-allow-val">none</span></label>
              <div class="wb-slider-row">
                <input type="range" id="eor-allow" min="0" max="2000" step="50" value="0" aria-label="Monthly allowances" data-track="calculator-control" data-control="allowances" />
              </div>
            </div>
            <div class="wb-control-item">
              <label class="wb-control-label" for="eor-fx">FX assumption <span class="val-pill" id="eor-fx-val">excluded</span></label>
              <div class="wb-slider-row">
                <input type="range" id="eor-fx" min="0" max="8" step="1" value="0" aria-label="FX assumption percent" data-track="calculator-control" data-control="fx" />
              </div>
              <p class="wb-budget-subnote">Deel's numeric spread is unpublished. Zero means excluded. A percent here is your assumption on the payroll pass-through, not a Deel tariff.</p>
            </div>
            <div class="wb-control-item">
              <label class="wb-control-label" for="eor-pay">Deel payment method</label>
              <select id="eor-pay" class="wb-tool-select" aria-label="Deel payment method" data-track="calculator-control" data-control="payment">
                <option value="none" selected>Fees excluded</option>
                <option value="card-us">Card, US or EU</option>
                <option value="card-intl">Card, outside US and EU</option>
                <option value="flat5">$5 method</option>
                <option value="pad">PAD, $10 CAD</option>
                <option value="becs">BECS, $10 AUD</option>
              </select>
            </div>
            <div class="wb-control-item">
              <label class="wb-control-label" for="eor-rippling-fee">Entered Rippling fee <span class="val-pill" id="eor-rippling-fee-val">$499</span></label>
              <div class="wb-slider-row">
                <input type="range" id="eor-rippling-fee" min="100" max="2000" step="1" value="499" aria-label="Entered Rippling monthly fee" data-track="calculator-control" data-control="rippling-fee" />
              </div>
              <p class="wb-budget-subnote">Used only when the Rippling menu says to use the fee in Assumptions. Treat it as your per-employee assumption.</p>
            </div>
            <label class="wb-budget-subnote"><input type="checkbox" id="eor-platform" data-track="calculator-control" data-control="platform" /> Show a separate hypothetical line for Rippling's $8 per employee starting price</label>
            <p class="wb-budget-subnote">Not a required EOR add-on. Not inside the modeled fee. The monthly base fee on top of $8 is unknown.</p>
          </div>
        </details>
"""

REST = r"""
<section id="eor-split">
  <h2>This example, split</h2>
  <p>These are modeled known fees, not an all-in quote. Salary, employer costs, and allowances are pass-through. The deposit is cash set aside. Using it later to pay the final invoice does not create a second cost. The salary and fees on that invoice are the costs.</p>
  <div class="table-wrap editorial-gap-table mobile-cards">
    <table>
      <caption>One employee, the $5,000 example salary, and Deel's starting fee. Rippling stays unknown.</caption>
      <thead>
        <tr>
          <th>Line</th>
          <th>Deel</th>
          <th>Rippling</th>
        </tr>
      </thead>
      <tbody id="eor-split-body">
        <tr><td data-label="Line">Management fee, Year-1</td><td data-label="Deel">$7,188</td><td data-label="Rippling">unknown</td></tr>
        <tr><td data-label="Line">Deposit cash lock-up</td><td data-label="Deel">$5,599</td><td data-label="Rippling">unknown</td></tr>
        <tr><td data-label="Line">FX</td><td data-label="Deel">excluded</td><td data-label="Rippling">unknown</td></tr>
        <tr><td data-label="Line">Offboarding administration fee</td><td data-label="Deel">unknown</td><td data-label="Rippling">unknown</td></tr>
        <tr><td data-label="Line">Modeled known fees</td><td data-label="Deel">$7,188</td><td data-label="Rippling">unknown</td></tr>
      </tbody>
    </table>
  </div>
  <p id="eor-note" class="summary-caveat">Illustrative Deel management fee: $7,188 for the year. Rippling's EOR fee is unknown. This is not a quote and not a ranking. The $5,599 figure is the lower-end 1.0 times example, not a deposit quote.</p>
</section>

<section>
  <h2>Prices checked on 8 Nov 2026</h2>
  <div class="table-wrap editorial-gap-table mobile-cards">
    <table>
      <caption>Published prices and the lines that stay unknown.</caption>
      <thead>
        <tr>
          <th>Item</th>
          <th>What the page says</th>
          <th>In the Year-1 fee</th>
        </tr>
      </thead>
      <tbody>
        <tr><td data-label="Item">Deel EOR</td><td data-label="What the page says">Starting at $599 per EOR employee per month. The pricing page lists full legal employment in 130+ countries, managed payroll, tax filings, benefits administration, onboarding, and on-demand HR, legal, and tax expertise.</td><td data-label="In the Year-1 fee">12 times the starting fee, times the employee count.</td></tr>
        <tr><td data-label="Item">Deel's pricing claim</td><td data-label="What the page says">Deel says you only pay for the services you use, with no hidden fees, and that local compliance, payroll, and benefits administration are in the quoted price. Pricing is month to month. EOR cancellation follows local labor laws, including notice and severance.</td><td data-label="In the Year-1 fee">Reported next to the deposit and FX help articles. Those articles document extras the pricing FAQ does not price.</td></tr>
        <tr><td data-label="Item">Not in the $599</td><td data-label="What the page says">From Deel's own pages: employee salary, country-specific employer costs, the EOR deposit, FX when the funding currency differs from the invoice currency, and legally required notice, unused leave, and severance on the final invoice.</td><td data-label="In the Year-1 fee">Salary and employer costs stay pass-through. The deposit stays out of the fee. Exit administration has no published dollar amount, so it is unknown.</td></tr>
        <tr><td data-label="Item">Deel deposit</td><td data-label="What the page says">Charged for each EOR hire and invoiced in the EOR location currency. The published standard band is 1 to 1.5 times monthly charges, including salary, employer costs, fixed allowances, and management fees. Some countries, and cases such as removing probation, extra PTO, a longer notice period, a transfer, or a large incentive plan, can require about two months or more. Refunded after termination or resignation once invoices are settled.</td><td data-label="In the Year-1 fee">The $5,599 default is the lower-end 1.0 times example on a $5,000 salary plus the $599 fee, with employer costs and allowances left at zero. Not a deposit quote. Not an expense, even if it later pays the final invoice.</td></tr>
        <tr><td data-label="Item">Deel FX</td><td data-label="What the page says">A forward rate from banking partners. No numeric markup is published. Paying the invoice in its own currency avoids the conversion. Deel says its rates are typically more favorable than the 4% to 5% markup it attributes to many retail banks. That is Deel's comparison, not Deel's own spread.</td><td data-label="In the Year-1 fee">Excluded unless you set a percent. That percent is your assumption on the payroll pass-through.</td></tr>
        <tr><td data-label="Item">Deel payment fees</td><td data-label="What the page says">Paying an invoice in its own currency avoids Deel's FX conversion. Processing fees are separate. Cards in the US or EU: $0.30 and 2.9%. Cards elsewhere: $0.30 and 3.9%. ACH, SEPA, BACS, wire, Brex, and Coinbase: $5. Mercury and Wise: the equivalent of $5. PAD: $10 CAD. BECS: $10 AUD.</td><td data-label="In the Year-1 fee">The default leaves payment fees excluded. That is not a claim that funding is free. A CAD or AUD fee stays in that currency, and the dollar figure is then an incomplete subtotal.</td></tr>
        <tr><td data-label="Item">Deel country surcharge</td><td data-label="What the page says">No public schedule of EOR prices above $599.</td><td data-label="In the Year-1 fee">unknown</td></tr>
        <tr><td data-label="Item">Rippling EOR</td><td data-label="What the page says">The pricing page says plans start at $8 per employee per month, with a monthly base fee, and that the total depends on the products you choose. It does not publish an EOR price, deposit, FX markup, setup fee, offboarding fee, minimum term, or auto-renewal clause. One Rippling blog says EOR starts at $499 a month and does not say per employee. Another says EOR is quote-based.</td><td data-label="In the Year-1 fee">unknown until you choose an assumption. The blog figure is multiplied by headcount only if you say to treat it as per employee. The $8 line, if shown, is a separate hypothetical and is not a required EOR add-on. The base fee amount is unknown.</td></tr>
        <tr><td data-label="Item">Rippling country count</td><td data-label="What the page says">Rippling's own pages say 50+, 115+, and 185+. They do not agree, and the text does not always say the unit.</td><td data-label="In the Year-1 fee">Not used. Coverage stays unpublished as a single number.</td></tr>
        <tr><td data-label="Item">User reports</td><td data-label="What the page says">One employer described a Deel forward rate about 3% to 4% above the figure they expected, and a deposit refund that was hard to collect. Another described USD and CAD conversions that added about 2% to 5.5%. An AskDeel reply said Deel uses a forward rate and that a consistent 3% to 4% needed a closer look.</td><td data-label="In the Year-1 fee">Not a tariff. Not used in the default math.</td></tr>
      </tbody>
    </table>
  </div>
  <p class="src-cluster"><a class="src-link" href="https://www.deel.com/pricing/" target="_blank" rel="noopener">Deel pricing</a> <span class="src-date">Accessed 2026-11-08</span></p>
  <p class="src-cluster"><a class="src-link" href="https://help.letsdeel.com/hc/en-gb/articles/15574494993297-About-EOR-Deposit-Calculations" target="_blank" rel="noopener">Deel, EOR deposit calculations</a> <span class="src-date">Accessed 2026-11-08</span></p>
  <p class="src-cluster"><a class="src-link" href="https://help.letsdeel.com/hc/en-gb/articles/4407745380241-About-Exchange-Rates-and-Fees" target="_blank" rel="noopener">Deel, exchange rates and fees</a> <span class="src-date">Accessed 2026-11-08</span></p>
  <p class="src-cluster"><a class="src-link" href="https://www.rippling.com/pricing" target="_blank" rel="noopener">Rippling pricing</a> <span class="src-date">Accessed 2026-11-08</span></p>
  <p class="src-cluster"><a class="src-link" href="https://www.rippling.com/employer-of-record" target="_blank" rel="noopener">Rippling employer of record</a> <span class="src-date">Accessed 2026-11-08</span></p>
  <p class="src-cluster"><a class="src-link" href="https://www.rippling.com/blog/best-employer-of-record" target="_blank" rel="noopener">Rippling, best employer of record</a> <span class="src-date">Accessed 2026-11-08</span></p>
  <p class="src-cluster"><a class="src-link" href="https://www.rippling.com/blog/remote-competitors" target="_blank" rel="noopener">Rippling, remote competitors</a> <span class="src-date">Accessed 2026-11-08</span></p>
  <p class="src-cluster"><a class="src-link" href="https://www.reddit.com/r/Payroll/comments/1rxqkce/frustrations_with_deel/" target="_blank" rel="noopener">User report, Deel billing</a> <span class="src-date">Accessed 2026-11-08</span></p>
  <p class="src-cluster"><a class="src-link" href="https://www.reddit.com/r/Payroll/comments/1lkkzn2/currency_handling_at_deel_causing_me_headaches/" target="_blank" rel="noopener">User report, Deel currency handling</a> <span class="src-date">Accessed 2026-11-08</span></p>
</section>
<script>
function eorMoney(cents) {
  if (cents < 0) return "unknown";
  var v = Math.round(cents);
  var dollars = Math.floor(v / 100);
  var rest = v % 100;
  var text = "$" + dollars.toLocaleString("en-US");
  if (rest) text += "." + (rest < 10 ? "0" : "") + rest;
  return text;
}

function eorRipplingMonth(mode, fee) {
  if (mode === "blog") return 499;
  if (mode === "entered") return Math.max(100, Math.round(Number(fee) || 0));
  return -1;
}

function calcEor(input) {
  var employees = Math.max(1, Math.round(Number(input.employees) || 1));
  var salary = Math.max(0, Math.round(Number(input.salary) || 0));
  var pct = Math.max(0, Math.round(Number(input.employerPct) || 0));
  var allowances = Math.max(0, Math.round(Number(input.allowances) || 0));
  var tenths = Math.max(10, Math.min(15, Math.round(Number(input.depositTenths) || 10)));
  var employer = Math.round(salary * pct / 100);
  var perHead = salary + employer + allowances + 599;
  var deposit = Math.round(perHead * employees * tenths / 10);
  var deelYear = 599 * 12 * employees;
  var ripplingMonth = eorRipplingMonth(input.ripplingMode, input.ripplingFee);
  var ripplingYear = ripplingMonth < 0 ? -1 : ripplingMonth * 12 * employees;
  var passMonth = (salary + employer + allowances) * employees;
  var fxPct = Math.max(0, Math.round(Number(input.fxPct) || 0));
  var fxYear = fxPct === 0 ? 0 : Math.round(passMonth * 12 * fxPct / 100);
  var invoiceMonth = passMonth + 599 * employees;
  var pay = input.payMethod || "none";
  var payCents = 0;
  if (pay === "card-us") payCents = Math.round(invoiceMonth * 12 * 2.9) + 360;
  else if (pay === "card-intl") payCents = Math.round(invoiceMonth * 12 * 3.9) + 360;
  else if (pay === "flat5") payCents = 6000;
  else if (pay === "pad" || pay === "becs") payCents = -1;
  var payIncomplete = pay === "pad" || pay === "becs";
  var vendorCents = deelYear * 100 + fxYear * 100 + (payCents > 0 ? payCents : 0);
  var platformYear = input.platform8 ? 8 * 12 * employees : 0;
  return {
    employees: employees,
    salary: salary,
    pct: pct,
    employer: employer,
    allowances: allowances,
    tenths: tenths,
    perHead: perHead,
    deposit: deposit,
    deelYear: deelYear,
    ripplingMonth: ripplingMonth,
    ripplingYear: ripplingYear,
    fxYear: fxYear,
    fxPct: fxPct,
    payCents: payCents,
    pay: pay,
    payIncomplete: payIncomplete,
    vendorCents: vendorCents,
    platformYear: platformYear
  };
}

function eorScenario(deelYear, ripplingYear, mode) {
  var deel = eorMoney(deelYear * 100);
  if (ripplingYear < 0) {
    return "Illustrative Deel management fee: " + deel + " for the year. Rippling's EOR fee is unknown. This is not a quote and not a ranking.";
  }
  var rip = eorMoney(ripplingYear * 100);
  var unit = mode === "blog"
    ? " The blog says starts at $499 a month and does not say per employee. You chose to treat that figure as per employee."
    : " The Rippling amount is a per-employee figure you entered, not a published rate card.";
  return "Illustrative management fees only: Deel " + deel + ". Rippling " + rip + "." + unit + " Not a quote and not a ranking. Base fee, required products, FX, and exit costs stay unknown.";
}

function eorRead() {
  return {
    employees: document.getElementById("eor-employees").value,
    salary: document.getElementById("eor-salary").value,
    employerPct: document.getElementById("eor-employer").value,
    allowances: document.getElementById("eor-allow").value,
    depositTenths: document.getElementById("eor-deposit").value,
    ripplingMode: document.getElementById("eor-rippling").value,
    ripplingFee: document.getElementById("eor-rippling-fee").value,
    fxPct: document.getElementById("eor-fx").value,
    payMethod: document.getElementById("eor-pay").value,
    platform8: document.getElementById("eor-platform").checked
  };
}

function eorNone(amount) {
  if (amount < 0) return "unknown";
  if (amount === 0) return "none";
  return eorMoney(amount * 100);
}

function renderEor() {
  var c = calcEor(eorRead());
  document.getElementById("eor-employees-val").textContent = String(c.employees);
  document.getElementById("eor-salary-val").textContent = eorMoney(c.salary * 100);
  document.getElementById("eor-employer-val").textContent = String(c.pct) + "%";
  document.getElementById("eor-allow-val").textContent = c.allowances === 0 ? "none" : eorMoney(c.allowances * 100);
  document.getElementById("eor-deposit-val").textContent = (c.tenths / 10).toFixed(1) + "×";
  document.getElementById("eor-fx-val").textContent = c.fxPct === 0 ? "excluded" : String(c.fxPct) + "%";
  document.getElementById("eor-rippling-fee-val").textContent = eorMoney(Math.round(Number(document.getElementById("eor-rippling-fee").value) || 0) * 100);
  var line = eorScenario(c.deelYear, c.ripplingYear, document.getElementById("eor-rippling").value);
  document.getElementById("shell-best").textContent = line;
  document.getElementById("shell-big").textContent = eorMoney(c.vendorCents);
  var foreign = c.pay === "pad" ? "$10 CAD" : "$10 AUD";
  document.getElementById("shell-product").textContent = c.payIncomplete
    ? "USD subtotal, incomplete"
    : "Deel management fee, " + c.employees + (c.employees === 1 ? " employee" : " employees");
  var near = "Modeled known fees, not an all-in quote. ";
  if (c.pay === "none") near += "Payment fees are excluded. That does not mean funding is free. ";
  else if (c.payIncomplete) near += "The " + foreign + " payment fee is excluded and not converted, so this dollar figure is incomplete. ";
  near += "Rippling's price, FX spread, deposit, setup, and offboarding fee stay unknown unless a line below is an assumption you turned on.";
  if (c.platformYear > 0) near += " Separate hypothetical platform line: " + eorMoney(c.platformYear * 100) + " a year. Not a required EOR add-on and not in the figure above.";
  document.getElementById("shell-sub").textContent = near;
  var ripplingBar = c.ripplingYear < 0 ? -1 : c.ripplingYear * 100;
  var bars = [
    ["shell-row-base", "shell-amt-base", "shell-title-base", "shell-sub-base", "Deel fee", c.deelYear * 100, "Starting price, 12 months"],
    ["shell-row-seats", "shell-amt-seats", "shell-title-seats", "shell-sub-seats", "Deposit", c.deposit * 100, "Cash lock-up, not a fee"],
    ["shell-row-hidden", "shell-amt-hidden", "shell-title-hidden", "shell-sub-hidden", "Rippling fee", ripplingBar, "Unknown unless you enter one"]
  ];
  var maxBar = 1;
  bars.forEach(function (bar) { if (bar[5] > maxBar) maxBar = bar[5]; });
  bars.forEach(function (bar) {
    var flex = bar[5] > 0 ? Math.max(12, Math.round(bar[5] / maxBar * 100)) : 12;
    document.getElementById(bar[0]).style.flex = flex + " 1 0px";
    document.getElementById(bar[1]).textContent = eorMoney(bar[5]);
    document.getElementById(bar[2]).textContent = bar[4];
    document.getElementById(bar[3]).textContent = bar[6];
  });
  document.getElementById("shell-sticker").textContent = eorMoney(c.deelYear * 100);
  document.getElementById("shell-sticker-note").textContent = "Deel management fee";
  document.getElementById("shell-gap").textContent = eorMoney(c.deposit * 100);
  var labels = document.querySelectorAll("#shell-summary .summary-label");
  if (labels.length >= 2) {
    labels[0].textContent = "Deel Year-1 fee";
    labels[1].textContent = "Deposit lock-up";
  }
  var notes = document.querySelectorAll("#shell-summary .summary-scenario");
  var zeroBits = c.employer === 0 && c.allowances === 0
    ? " Employer costs and allowances are left at zero."
    : " Employer costs " + eorNone(c.employer) + " and allowances " + eorNone(c.allowances) + " per employee are in the example.";
  var depositNote = "Lower-end " + (c.tenths / 10).toFixed(1) + " times this example: " + eorMoney(c.salary * 100) + " salary plus the $599 fee." + zeroBits + " Not a deposit quote. Country and special cases above 1.5 times are not on the slider. Not an expense, even if it later pays the final invoice.";
  if (notes.length >= 2) notes[1].textContent = depositNote;
  var fxText = c.fxPct === 0 ? "excluded" : eorMoney(c.fxYear * 100);
  var payText = "excluded";
  if (c.pay === "pad") payText = "$10 CAD, excluded from the USD subtotal";
  else if (c.pay === "becs") payText = "$10 AUD, excluded from the USD subtotal";
  else if (c.payCents > 0) payText = eorMoney(c.payCents);
  var platformText = c.platformYear === 0 ? "off" : eorMoney(c.platformYear * 100);
  document.getElementById("shell-math").textContent = c.employees + " employees. Example salary " + eorMoney(c.salary * 100) + ". Deel management " + eorMoney(c.deelYear * 100) + ". Deposit " + eorMoney(c.deposit * 100) + ". " + depositNote + " FX " + fxText + ". Payment fee " + payText + ". Rippling management " + eorMoney(c.ripplingYear < 0 ? -1 : c.ripplingYear * 100) + ". Hypothetical $8 platform line " + platformText + ". Offboarding administration fee unknown for both. Not a quote and not a ranking.";
  function row(name, deel, rip) {
    return "<tr><td data-label=\"Line\">" + name + "</td><td data-label=\"Deel\">" + deel + "</td><td data-label=\"Rippling\">" + rip + "</td></tr>";
  }
  document.getElementById("eor-split-body").innerHTML = ""
    + row("Management fee, Year-1", eorMoney(c.deelYear * 100), eorMoney(c.ripplingYear < 0 ? -1 : c.ripplingYear * 100))
    + row("Deposit cash lock-up", eorMoney(c.deposit * 100), "unknown")
    + row("Payroll pass-through, Year-1", eorNone((c.salary + c.employer + c.allowances) * c.employees * 12), "same example, not a vendor fee")
    + row("FX on that pass-through", fxText, "unknown")
    + row("Payment fee", payText, "unknown")
    + row("Hypothetical platform line", "not a Deel line", platformText === "off" ? "not shown" : platformText + ", not in the fee")
    + row("Offboarding administration fee", "unknown", "unknown")
    + row(c.payIncomplete ? "USD subtotal, incomplete" : "Modeled known fees", eorMoney(c.vendorCents), eorMoney(c.ripplingYear < 0 ? -1 : c.ripplingYear * 100));
  document.getElementById("eor-note").textContent = line + " " + depositNote;
  if (typeof window.trackSaaSBillEvent === "function") {
    window.trackSaaSBillEvent("result_rendered", { page: "eor-cost", employees: c.employees });
  }
}
["eor-employees", "eor-salary", "eor-employer", "eor-allow", "eor-deposit", "eor-rippling", "eor-rippling-fee", "eor-fx", "eor-pay", "eor-platform"].forEach(function (id) {
  var el = document.getElementById(id);
  el.addEventListener("input", renderEor);
  el.addEventListener("change", renderEor);
});
renderEor();
</script>
"""

FAQS = [
    (
        "What does Deel's $599 include?",
        "Deel's pricing page says EOR starts at $599 per employee per month and lists legal employment, managed payroll and tax filings, benefits administration, onboarding, and HR, legal, and tax support. The same page says costs are in the quoted price. The help center still documents a deposit and a currency conversion when you pay in a different currency. Salary and statutory employer costs are not a Deel list price. A country surcharge above $599 is unknown.",
    ),
    (
        "Is the Deel deposit a fee?",
        "No. Deel invoices a deposit for each EOR hire. The published standard band is 1 to 1.5 times monthly charges. The slider stops there. Country rules and special cases can require about two months or more, and those are not modeled. The deposit is refunded after the contract ends and invoices are paid, or it can pay the final invoice. That use is not a second cost. The salary, employer costs, and fees on the invoice are the costs. A separate offboarding administration fee is not published, so that amount is unknown.",
    ),
    (
        "What does Rippling charge for EOR?",
        "Rippling's pricing page does not publish an EOR price, deposit, FX markup, setup fee, or offboarding fee. It says plans start at $8 per employee per month, plus a monthly base fee whose amount is unknown. A Rippling comparison blog says EOR starts at $499 a month, and another Rippling article says EOR is quote-based. The calculator leaves Rippling unknown until you choose one of those inputs. Country counts on Rippling's own pages conflict, so this page does not pick 50+, 115+, or 185+.",
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
        raise SystemExit("em dash in eor copy")
    workbench = render_workbench(
        CONTROLS,
        controls_title="Your EOR example",
        chart_title="Fee and deposit",
        cta_href="https://www.deel.com/pricing/",
        cta_label="Deel pricing",
        cta_vendor="deel",
    )
    needle = 'href="https://www.deel.com/pricing/" data-track="vendor-cta" data-vendor="deel" data-cta-location="workbench">Deel pricing &rarr;</a>'
    replacement = (
        'href="https://www.deel.com/pricing/" target="_blank" rel="noopener" data-track="vendor-cta" data-vendor="deel" data-cta-location="workbench">Deel pricing &rarr;</a>'
        '<a id="shell-cta-rippling" class="btn-secondary" href="https://www.rippling.com/pricing" target="_blank" rel="noopener" data-track="vendor-cta" data-vendor="rippling" data-cta-location="workbench">Rippling pricing &rarr;</a>'
    )
    if needle not in workbench:
        raise SystemExit("Deel CTA not found")
    workbench = workbench.replace(needle, replacement, 1)
    for old, new in (
        ('id="shell-product">Year-1 total<', 'id="shell-product">Deel management fee, 1 employee<'),
        ('id="shell-big">$0<', 'id="shell-big">$7,188<'),
        ('id="shell-sub">Matches advertised price ($0 hidden fees).</p>', 'id="shell-sub">Modeled known fees, not an all-in quote. Payment fees are excluded. That does not mean funding is free. Rippling\'s price, FX spread, deposit, setup, and offboarding fee stay unknown unless a line below is an assumption you turned on.</p>'),
        ('id="shell-title-base">Sticker Price<', 'id="shell-title-base">Deel fee<'),
        ('id="shell-sub-base">Advertised price<', 'id="shell-sub-base">Starting price, 12 months<'),
        ('id="shell-amt-base">$0<', 'id="shell-amt-base">$7,188<'),
        ('id="shell-title-seats">Other sticker fees<', 'id="shell-title-seats">Deposit<'),
        ('id="shell-sub-seats">Included in the sticker<', 'id="shell-sub-seats">Cash lock-up, not a fee<'),
        ('id="shell-amt-seats">$0<', 'id="shell-amt-seats">$5,599<'),
        ('id="shell-title-hidden">Hidden Cost Gap<', 'id="shell-title-hidden">Rippling fee<'),
        ('id="shell-sub-hidden">Fees above the advertised price<', 'id="shell-sub-hidden">Unknown unless you enter one<'),
        ('id="shell-amt-hidden">$0<', 'id="shell-amt-hidden">unknown<'),
        ('<div class="summary-label">Sticker Price</div>', '<div class="summary-label">Deel Year-1 fee</div>'),
        ('id="shell-sticker">$0<', 'id="shell-sticker">$7,188<'),
        ('id="shell-sticker-note">Advertised price<', 'id="shell-sticker-note">Deel management fee<'),
        ('<div class="summary-label">Hidden Cost Gap</div>', '<div class="summary-label">Deposit lock-up</div>'),
        ('id="shell-gap">$0<', 'id="shell-gap">$5,599<'),
        ('<div class="summary-scenario">Above the advertised price</div>', '<div class="summary-scenario">Not added to the Year-1 fee</div>'),
    ):
        if old not in workbench:
            raise SystemExit("missing eor fallback: " + old)
        workbench = workbench.replace(old, new, 1)
    body = (
        '<section class="hero">'
        "<h1>Deel vs. Rippling EOR cost (2026)</h1>"
        '<p class="lead">Deel\'s EOR management fee starts at $599 per employee per month, $7,188 for one employee over a year. '
        "Rippling does not publish an EOR price. These figures are a model, not a quote and not a ranking. "
        "The deposit shown is the lower-end 1.0 times example, not a guaranteed deposit.</p>"
        "</section>"
        + workbench
        + REST
    )
    if "/go/deel" in body or "/go/rippling" in body or "sponsored" in body:
        raise SystemExit("affiliate tracking on the EOR page")
    render_page(
        REL,
        TITLE,
        DESCRIPTION,
        CANONICAL,
        wrap_calculator_shell(body),
        faqs=FAQS,
        published_date="2026-11-08",
        show_affiliate_note=False,
        modified_datetime="2026-11-08T06:05:08+00:00",
    )
    copy_to_root(REL)


if __name__ == "__main__":
    build()
