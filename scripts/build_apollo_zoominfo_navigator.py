"""Apollo versus ZoomInfo versus Sales Navigator, Year 1.

Apollo prices were read live on 2026-11-14 from https://www.apollo.io/pricing
and https://www.apollo.io/pricing/about-credits.

Annual, per seat per month, credits granted per seat per year:
  Free $0, 900 credits granted monthly
  Basic $49, 30,000 credits upfront
  Professional $79, 48,000 credits upfront
  Organization $119, minimum 3 seats, 72,000 credits upfront

Monthly view:
  Free $0, 75 credits per month
  Basic $65, 2,500 credits per month
  Professional $99, 4,000 credits per month
  Organization shows $149 and Annual Only, so the year uses $119

Email is 1 credit. A phone number is 8 credits. Credits do not roll over.
Advanced Dialer is $119 per team per month billed annually and is not in the total.
Apollo is the affiliate, through /go/apollo.
"""
import os
import shutil

from layout import BASE_DIR, PUBLIC_DIR, render_page, render_workbench, wrap_calculator_shell

TITLE = "Apollo vs ZoomInfo Year-1 – saasbill.io"
DESCRIPTION = (
    "Year-1 Apollo seat and credit cost beside Sales Navigator and a labeled ZoomInfo estimate. Checked 14 Nov 2026."
)
CANONICAL = "/pricing/apollo-vs-zoominfo-vs-sales-navigator-year-1-cost/"
REL = "pricing/apollo-vs-zoominfo-vs-sales-navigator-year-1-cost/index.html"
LEAD = "This page compares Apollo, ZoomInfo, and LinkedIn Sales Navigator for one year."

CONTROLS = r"""
        <div class="wb-control-item">
          <label class="wb-control-label" for="ap-seats">Seats <span class="val-pill" id="ap-seats-val">5</span></label>
          <div class="wb-slider-row">
            <input type="range" id="ap-seats" min="1" max="50" step="1" value="5" aria-label="Seats" data-track="calculator-control" data-control="seats" />
          </div>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="ap-billing">Billing</label>
          <select id="ap-billing" class="wb-tool-select" data-track="calculator-control" data-control="billing">
            <option value="annual" selected>Annual</option>
            <option value="monthly">Monthly</option>
          </select>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="ap-plan">Apollo plan</label>
          <select id="ap-plan" class="wb-tool-select" data-track="calculator-control" data-control="apollo-plan">
            <option value="free">Free</option>
            <option value="basic">Basic</option>
            <option value="professional" selected>Professional</option>
            <option value="organization">Organization</option>
            <option value="custom">Custom</option>
          </select>
          <p class="wb-budget-subnote">Annual: Free $0, Basic $49, Professional $79, Organization $119. Monthly: Free $0, Basic $65, Professional $99.</p>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="ap-emails">Emails revealed per seat per month <span class="val-pill" id="ap-emails-val">300</span></label>
          <div class="wb-slider-row">
            <input type="range" id="ap-emails" min="0" max="2000" step="10" value="300" aria-label="Emails revealed per seat per month" data-track="calculator-control" data-control="emails" />
          </div>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="ap-phones">Phone numbers revealed per seat per month <span class="val-pill" id="ap-phones-val">30</span></label>
          <div class="wb-slider-row">
            <input type="range" id="ap-phones" min="0" max="200" step="1" value="30" aria-label="Phone numbers revealed per seat per month" data-track="calculator-control" data-control="phones" />
          </div>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="ap-addon">Add-on price per credit</label>
          <input id="ap-addon" class="wb-tool-select" type="text" inputmode="decimal" aria-label="Add-on price per credit" data-track="calculator-control" data-control="addon" />
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="ap-sn">Sales Navigator plan</label>
          <select id="ap-sn" class="wb-tool-select" data-track="calculator-control" data-control="sales-navigator">
            <option value="core" selected>Core</option>
            <option value="advanced">Advanced</option>
            <option value="plus">Advanced Plus</option>
          </select>
          <p class="wb-budget-subnote">Core is $1,079.88 a year or $119.99 a month. Advanced is $1,799.88 a year or $159.99 a month. LinkedIn calls these estimates and they may exclude VAT. Advanced Plus is a quote.</p>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="ap-zi-platform">Third-party ZoomInfo platform fee per year</label>
          <input id="ap-zi-platform" class="wb-tool-select" type="number" min="0" step="1" value="14995" aria-label="Third-party ZoomInfo platform fee per year" data-track="calculator-control" data-control="zoominfo-platform" />
          <p class="wb-budget-subnote">ZoomInfo does not publish these rates. ZoomInfo&rsquo;s AI information page says figures such as $14,995 a year are out of date. Edit them to your quote.</p>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="ap-zi-seat">Third-party ZoomInfo fee per seat per year</label>
          <input id="ap-zi-seat" class="wb-tool-select" type="number" min="0" step="1" value="1500" aria-label="Third-party ZoomInfo fee per seat per year" data-track="calculator-control" data-control="zoominfo-seat" />
        </div>
"""

REST = r"""
<section>
  <h2>How the year is priced</h2>
  <p>Apollo&rsquo;s year is the seat price times billed seats times 12, plus shortfall credits times an add-on price you type. An email is 1 credit, and never more than 1 credit per contact. A phone number is 8 credits. Credits are pooled, granted at the start of the billing cycle, and they do not roll over. A monthly plan checks each month on its own. An annual plan uses the year&rsquo;s upfront pool. Annual credits per seat are 900 on Free, 30,000 on Basic, 48,000 on Professional, and 72,000 on Organization. Monthly credits per seat are 75, 2,500, 4,000, and 6,000. Every seat is on the same plan. Add-on credits renew until the slider is set back to zero. Apollo does not publish an add-on credit price, so a blank field stays unknown. An annual invoice cannot move to monthly mid-cycle. A downgrade is immediate and does not refund unused time. Cancellation takes effect at the end of the term. SSO is the Custom plan, which is a quote. The monthly pricing view shows Organization at $149 and marks it Annual Only, so this year uses the annual seat price and a 3-seat minimum. Advanced Dialer is $119 per team per month billed annually and is not in the total. This page does not price dialer minutes. Seat prices exclude tax. Basic and Professional list a 14-day trial.</p>
  <p>Sales Navigator uses the published yearly price, or 12 times the monthly price. LinkedIn sells up to five Advanced licenses online. The plan includes 50 InMail messages a month.</p>
  <p>The ZoomInfo year is the platform fee plus the per-seat fee, billed for at least 3 seats. Each export is one credit. Credits above the 5,000 third-party allowance are not priced, so they are not added. A Vendr median of $33,500 a year is a separate figure and is not this estimate. Renewal notice rules are on the <a href="../../exit/zoominfo-60-day-auto-renewal-notice-and-cancellation/">ZoomInfo renewal notice page</a>. The May 1, 2025 terms say the agreement is not cancellable.</p>
</section>
<section>
  <h2>Year-1 cost</h2>
  <div class="table-wrap editorial-gap-table mobile-cards">
    <table>
      <caption>Seat cost, credits, and the year for the inputs above.</caption>
      <thead>
        <tr>
          <th>Path</th>
          <th>Year 1</th>
          <th>Seat cost</th>
          <th>Credits</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td data-label="Path">Apollo</td>
          <td data-label="Year 1" id="ap-cell-year">$4,740</td>
          <td data-label="Seat cost" id="ap-cell-seat">$4,740</td>
          <td data-label="Credits" id="ap-cell-credits">32,400 needed, 240,000 included, shortfall 0</td>
        </tr>
        <tr>
          <td data-label="Path">Sales Navigator</td>
          <td data-label="Year 1" id="ap-cell-sn-year">$5,399.40</td>
          <td data-label="Seat cost" id="ap-cell-sn-seat">$5,399.40</td>
          <td data-label="Credits" id="ap-cell-sn-credits">No email or phone credits</td>
        </tr>
        <tr>
          <td data-label="Path">ZoomInfo estimate</td>
          <td data-label="Year 1" id="ap-cell-zi-year">$22,495</td>
          <td data-label="Seat cost" id="ap-cell-zi-seat">$7,500</td>
          <td data-label="Credits" id="ap-cell-zi-credits">19,800 export credits</td>
        </tr>
        <tr>
          <td data-label="Path">Sales Navigator plus Apollo Basic</td>
          <td data-label="Year 1" id="ap-cell-split-year">$8,339.40</td>
          <td data-label="Seat cost" id="ap-cell-split-seat">$8,339.40</td>
          <td data-label="Credits" id="ap-cell-split-credits">Basic shortfall 0</td>
        </tr>
      </tbody>
    </table>
  </div>
</section>
<section>
  <h2>User reports</h2>
  <ul class="key-list">
    <li>Anecdotal. On 5 Jan 2026 a legacy user said monthly credits dropped from 10,000 to 4,000. <span class="src-cluster"><a class="src-link" href="https://www.reddit.com/r/UseApolloIo/comments/1q4uv4q/" target="_blank" rel="noopener">r/UseApolloIo</a> <span class="src-date">Accessed 14 Nov 2026.</span></span></li>
    <li>Anecdotal. On 20 Jan 2026 a team said a plan near $500 a month lost dialer access mid-plan, and that power dialing is an add-on. <span class="src-cluster"><a class="src-link" href="https://www.reddit.com/r/UseApolloIo/comments/1qido3x/" target="_blank" rel="noopener">r/UseApolloIo</a> <span class="src-date">Accessed 14 Nov 2026.</span></span></li>
    <li>Anecdotal. On 9 Jun 2026 one SDR team said a Professional renewal moved from about $150 a user a month to above $200. <span class="src-cluster"><a class="src-link" href="https://www.reddit.com/r/EntrepreneurRideAlong/comments/1u0y9xj/" target="_blank" rel="noopener">r/EntrepreneurRideAlong</a> <span class="src-date">Accessed 14 Nov 2026.</span></span></li>
  </ul>
  <p class="summary-caveat">Checked 14 Nov 2026. <span class="src-cluster"><a class="src-link" href="https://www.apollo.io/pricing" target="_blank" rel="noopener">Apollo pricing</a> <span class="src-date">Accessed 14 Nov 2026.</span></span> <span class="src-cluster"><a class="src-link" href="https://www.apollo.io/pricing/about-credits" target="_blank" rel="noopener">Apollo credits</a> <span class="src-date">Accessed 14 Nov 2026.</span></span> <span class="src-cluster"><a class="src-link" href="https://business.linkedin.com/sales-solutions/compare-plans" target="_blank" rel="noopener">Sales Navigator plans</a> <span class="src-date">FAQ updated 27 Sep 2026. Accessed 14 Nov 2026.</span></span> <span class="src-cluster"><a class="src-link" href="https://www.zoominfo.com/pricing" target="_blank" rel="noopener">ZoomInfo pricing</a> <span class="src-date">Accessed 14 Nov 2026.</span></span> <span class="src-cluster"><a class="src-link" href="https://www.zoominfo.com/legal/ltc_05_01_2025" target="_blank" rel="noopener">ZoomInfo terms, 1 May 2025</a> <span class="src-date">Accessed 14 Nov 2026.</span></span> <span class="src-cluster"><a class="src-link" href="https://www.zoominfo.com/ai-information" target="_blank" rel="noopener">ZoomInfo AI information</a> <span class="src-date">Accessed 14 Nov 2026.</span></span> <span class="src-cluster"><a class="src-link" href="https://www.getcleed.com/blog/zoominfo-pricing" target="_blank" rel="noopener">Cleed ZoomInfo pricing</a> <span class="src-date">Accessed 14 Nov 2026.</span></span> <span class="src-cluster"><a class="src-link" href="https://www.pin.com/blog/zoominfo-pricing/" target="_blank" rel="noopener">Pin ZoomInfo pricing</a> <span class="src-date">Accessed 14 Nov 2026.</span></span></p>
</section>
"""

SCRIPT = r"""
<script>
function calcApolloYear(input) {
  input = input || {};
  var seats = Math.max(1, Math.round(Number(input.seats) || 1));
  var billing = input.billing === "monthly" ? "monthly" : "annual";
  var emails = Math.max(0, Math.round(Number(input.emails) || 0));
  var phones = Math.max(0, Math.round(Number(input.phones) || 0));
  var plan = input.plan || "professional";
  var sn = input.sn || "core";
  var addon = null;
  if (input.addon !== undefined && input.addon !== null && String(input.addon).trim() !== "") {
    var addonDollars = Number(input.addon);
    if (isFinite(addonDollars) && addonDollars >= 0) addon = Math.round(addonDollars * 100);
  }
  function dollarsOrNull(value) {
    if (value === undefined || value === null || String(value).trim() === "") return null;
    var amount = Number(value);
    if (!isFinite(amount) || amount < 0) return null;
    return Math.round(amount * 100);
  }
  var ziPlatform = dollarsOrNull(input.ziPlatform);
  var ziSeatRate = dollarsOrNull(input.ziSeat);
  var plans = {
    free: { annual: 0, monthly: 0, yearCredits: 900, monthCredits: 75, min: 1, monthlyOk: true },
    basic: { annual: 4900, monthly: 6500, yearCredits: 30000, monthCredits: 2500, min: 1, monthlyOk: true },
    professional: { annual: 7900, monthly: 9900, yearCredits: 48000, monthCredits: 4000, min: 1, monthlyOk: true },
    organization: { annual: 11900, monthly: 0, yearCredits: 72000, monthCredits: 6000, min: 3, monthlyOk: false }
  };
  function pricePlan(which) {
    var spec = plans[which];
    var emailCredits = emails * seats * 12;
    var phoneCredits = phones * seats * 8 * 12;
    var need = emailCredits + phoneCredits;
    if (!spec) {
      return {
        year: null,
        seat: null,
        included: null,
        shortfall: null,
        addonCost: null,
        billed: seats,
        need: need,
        emailCredits: emailCredits,
        phoneCredits: phoneCredits,
        forcedAnnual: false
      };
    }
    var forcedAnnual = billing === "monthly" && !spec.monthlyOk;
    var useMonthly = billing === "monthly" && spec.monthlyOk;
    var billed = Math.max(seats, spec.min);
    var rate = useMonthly ? spec.monthly : spec.annual;
    var seat = rate * 12 * billed;
    var included;
    var shortfall;
    if (useMonthly) {
      var monthNeed = emails * seats + phones * seats * 8;
      var monthShort = Math.max(0, monthNeed - spec.monthCredits * billed);
      included = spec.monthCredits * billed * 12;
      shortfall = monthShort * 12;
    } else {
      included = spec.yearCredits * billed;
      shortfall = Math.max(0, need - included);
    }
    var addonCost = shortfall === 0 ? 0 : (addon === null ? null : shortfall * addon);
    var year = addonCost === null ? null : seat + addonCost;
    return {
      year: year,
      seat: seat,
      included: included,
      shortfall: shortfall,
      addonCost: addonCost,
      billed: billed,
      need: need,
      emailCredits: emailCredits,
      phoneCredits: phoneCredits,
      forcedAnnual: forcedAnnual
    };
  }
  var main = pricePlan(plan);
  var basic = pricePlan("basic");
  var snPlans = {
    core: { annual: 107988, monthly: 11999 },
    advanced: { annual: 179988, monthly: 15999 }
  };
  var snSpec = snPlans[sn] || null;
  var snYear = null;
  var snSeat = null;
  if (snSpec) {
    var snUnit = billing === "monthly" ? snSpec.monthly * 12 : snSpec.annual;
    if (!(sn === "advanced" && seats > 5)) {
      snSeat = snUnit * seats;
      snYear = snSeat;
    }
  }
  var ziSeats = Math.max(seats, 3);
  var ziYear = null;
  var ziSeat = null;
  if (ziPlatform !== null && ziSeatRate !== null) {
    ziSeat = ziSeatRate * ziSeats;
    ziYear = ziPlatform + ziSeat;
  }
  var split = null;
  var splitSeat = null;
  if (basic.seat !== null && snSeat !== null) splitSeat = basic.seat + snSeat;
  if (basic.year !== null && snYear !== null) split = basic.year + snYear;
  return {
    apolloYear: main.year,
    apolloSeat: main.seat,
    need: main.need,
    included: main.included,
    shortfall: main.shortfall,
    addonCost: main.addonCost,
    billed: main.billed,
    emailCredits: main.emailCredits,
    phoneCredits: main.phoneCredits,
    forcedAnnual: main.forcedAnnual,
    snYear: snYear,
    snSeat: snSeat,
    ziYear: ziYear,
    ziSeat: ziSeat,
    ziSeats: ziSeats,
    exports: (emails + phones) * seats * 12,
    split: split,
    splitSeat: splitSeat,
    basicYear: basic.year,
    basicSeat: basic.seat,
    basicShortfall: basic.shortfall
  };
}

function apMoney(cents) {
  if (cents === null) return "unknown";
  var negative = cents < 0;
  var value = Math.abs(Math.round(cents));
  var dollars = Math.floor(value / 100);
  var rem = value % 100;
  var text = "$" + dollars.toLocaleString("en-US");
  if (rem) text += "." + (rem < 10 ? "0" : "") + rem;
  return negative ? "-" + text : text;
}

function apCount(value) {
  if (value === null) return "unknown";
  return Math.round(value).toLocaleString("en-US");
}

function renderApolloYear() {
  var result = calcApolloYear({
    seats: document.getElementById("ap-seats").value,
    billing: document.getElementById("ap-billing").value,
    emails: document.getElementById("ap-emails").value,
    phones: document.getElementById("ap-phones").value,
    plan: document.getElementById("ap-plan").value,
    addon: document.getElementById("ap-addon").value,
    ziPlatform: document.getElementById("ap-zi-platform").value,
    ziSeat: document.getElementById("ap-zi-seat").value,
    sn: document.getElementById("ap-sn").value
  });
  document.getElementById("ap-seats-val").textContent = document.getElementById("ap-seats").value;
  document.getElementById("ap-emails-val").textContent = Number(document.getElementById("ap-emails").value).toLocaleString("en-US");
  document.getElementById("ap-phones-val").textContent = document.getElementById("ap-phones").value;
  var names = { free: "Free", basic: "Basic", professional: "Professional", organization: "Organization", custom: "Custom" };
  document.getElementById("shell-product").textContent = "Apollo " + (names[document.getElementById("ap-plan").value] || "plan");
  document.getElementById("shell-big").textContent = apMoney(result.apolloYear);
  var amounts = [result.apolloYear, result.snYear, result.ziYear].filter(function (amount) { return amount !== null; });
  var max = amounts.length ? Math.max.apply(null, amounts) : 0;
  function setBar(rowId, amtId, cents) {
    var share = cents === null || max <= 0 ? 0 : Math.round((cents / max) * 1000) / 10;
    document.getElementById(amtId).textContent = apMoney(cents);
    document.getElementById(rowId).style.setProperty("--wb-bar-share", share + "%");
  }
  setBar("shell-row-base", "shell-amt-base", result.apolloYear);
  setBar("shell-row-seats", "shell-amt-seats", result.snYear);
  setBar("shell-row-hidden", "shell-amt-hidden", result.ziYear);
  var best = document.getElementById("shell-best");
  if (result.apolloYear === null || result.snYear === null) {
    best.textContent = "";
    best.style.display = "none";
  } else {
    var gap = result.snYear - result.apolloYear;
    best.style.display = "";
    if (gap === 0) best.textContent = "Same as Sales Navigator.";
    else if (gap > 0) best.textContent = apMoney(gap) + " less than Sales Navigator.";
    else best.textContent = apMoney(-gap) + " more than Sales Navigator.";
  }
  var math = document.getElementById("shell-math");
  math.textContent = "";
  function addLine(text) {
    var line = document.createElement("p");
    line.textContent = text;
    math.appendChild(line);
  }
  addLine("Apollo seats: " + apMoney(result.apolloSeat) + " for " + result.billed + " billed seats.");
  addLine("Credits: " + apCount(result.emailCredits) + " email credits and " + apCount(result.phoneCredits) + " phone credits. Included " + apCount(result.included) + ". Shortfall " + apCount(result.shortfall) + ". Add-on " + apMoney(result.addonCost) + ".");
  addLine("Sales Navigator: " + apMoney(result.snYear) + ".");
  addLine("ZoomInfo: platform plus " + apMoney(result.ziSeat) + " for " + result.ziSeats + " seats = " + apMoney(result.ziYear) + ". Export credits " + apCount(result.exports) + ".");
  addLine("Split: Apollo Basic " + apMoney(result.basicYear) + " plus Sales Navigator " + apMoney(result.snYear) + " = " + apMoney(result.split) + ".");
  document.getElementById("ap-cell-year").textContent = apMoney(result.apolloYear);
  document.getElementById("ap-cell-seat").textContent = apMoney(result.apolloSeat);
  document.getElementById("ap-cell-credits").textContent = apCount(result.need) + " needed, " + apCount(result.included) + " included, shortfall " + apCount(result.shortfall);
  document.getElementById("ap-cell-sn-year").textContent = apMoney(result.snYear);
  document.getElementById("ap-cell-sn-seat").textContent = apMoney(result.snSeat);
  document.getElementById("ap-cell-zi-year").textContent = apMoney(result.ziYear);
  document.getElementById("ap-cell-zi-seat").textContent = apMoney(result.ziSeat);
  document.getElementById("ap-cell-zi-credits").textContent = apCount(result.exports) + " export credits";
  document.getElementById("ap-cell-split-year").textContent = apMoney(result.split);
  document.getElementById("ap-cell-split-seat").textContent = apMoney(result.splitSeat);
  document.getElementById("ap-cell-split-credits").textContent = "Basic shortfall " + apCount(result.basicShortfall);
}

["ap-seats", "ap-billing", "ap-plan", "ap-emails", "ap-phones", "ap-addon", "ap-sn", "ap-zi-platform", "ap-zi-seat"].forEach(function (id) {
  var el = document.getElementById(id);
  el.addEventListener("input", renderApolloYear);
  el.addEventListener("change", renderApolloYear);
});
renderApolloYear();
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
    if "\u2014" in (TITLE + DESCRIPTION + LEAD + CONTROLS + REST + SCRIPT):
        raise SystemExit("em dash in page copy")
    workbench = render_workbench(
        CONTROLS,
        controls_title="Your team",
        chart_title="Year-1 cost",
        cta_href="../../go/apollo/",
        cta_label="Apollo pricing",
        cta_vendor="apollo",
    )
    replacements = (
        ('class="wb-vbar-container"', 'class="wb-vbar-container wb-vbar-separate"'),
        ('id="shell-row-base" style="flex: 40 1 0px;"', 'id="shell-row-base" style="--wb-bar-share: 21.1%;"'),
        ('id="shell-row-seats" style="flex: 8 1 0px;"', 'id="shell-row-seats" style="--wb-bar-share: 24%;"'),
        ('id="shell-row-hidden" style="flex: 52 1 0px;"', 'id="shell-row-hidden" style="--wb-bar-share: 100%;"'),
        ('id="shell-product">Year-1 total<', 'id="shell-product">Apollo Professional<'),
        ('id="shell-big">$0<', 'id="shell-big">$4,740<'),
        ('id="shell-sub">Matches advertised price ($0 hidden fees).</p>', 'id="shell-sub"></p>'),
        ('id="shell-title-base">Sticker Price<', 'id="shell-title-base">Apollo<'),
        ('id="shell-sub-base">Advertised price<', 'id="shell-sub-base">Year 1<'),
        ('id="shell-amt-base">$0<', 'id="shell-amt-base">$4,740<'),
        ('id="shell-title-seats">Other sticker fees<', 'id="shell-title-seats">Sales Navigator<'),
        ('id="shell-sub-seats">Included in the sticker<', 'id="shell-sub-seats">Year 1<'),
        ('id="shell-amt-seats">$0<', 'id="shell-amt-seats">$5,399.40<'),
        ('id="shell-title-hidden">Hidden Cost Gap<', 'id="shell-title-hidden">ZoomInfo<'),
        ('id="shell-sub-hidden">Fees above the advertised price<', 'id="shell-sub-hidden">Year 1<'),
        ('id="shell-amt-hidden">$0<', 'id="shell-amt-hidden">$22,495<'),
        ('id="shell-best"></div>', 'id="shell-best">$659.40 less than Sales Navigator.</div>'),
        (
            '<a id="shell-cta" class="btn-cta wb-primary-cta" href="../../go/apollo/" data-track="vendor-cta" data-vendor="apollo" data-cta-location="workbench">Apollo pricing &rarr;</a>',
            '<a id="shell-cta" class="btn-cta wb-primary-cta" href="../../go/apollo/" target="_blank" rel="sponsored nofollow noopener" data-track="vendor-cta" data-vendor="apollo" data-cta-location="workbench">Apollo pricing &rarr;</a>',
        ),
    )
    for old, new in replacements:
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
        "<h1>What does Apollo cost in Year 1 versus ZoomInfo and Sales Navigator?</h1>"
        '<p class="lead">%s</p>' % LEAD
        + "</section>"
        + workbench
        + REST
        + SCRIPT
    )
    render_page(
        REL,
        TITLE,
        DESCRIPTION,
        CANONICAL,
        wrap_calculator_shell(body),
        faqs=None,
        published_date="2026-11-14",
        show_affiliate_note=True,
    )
    copy_to_root(REL)


if __name__ == "__main__":
    build()
