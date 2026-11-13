"""Chargeflow vs Stripe Smart Disputes Year-1 cost.

Checked 2026-11-11.
Stripe US pricing (https://stripe.com/us/pricing): dispute received $15.00,
dispute countered $15.00 and returned only if you win, dispute appealed $15.00
and not returned, Smart Disputes 30% of the disputed amount on a win only.
Chargeback Protection is not listed.
Chargeflow pricing (https://www.chargeflow.io/pricing): Automation is 25% of
the recovered amount and does not include the dispute fee.
No Chargeflow affiliate link.
"""
import os
import shutil

from layout import BASE_DIR, PUBLIC_DIR, render_page, render_workbench, wrap_calculator_shell

TITLE = "Chargeflow vs Stripe Smart Disputes – saasbill.io"
DESCRIPTION = (
    "Compares a manual Stripe response, Stripe Smart Disputes, and Chargeflow Automation for one year. Checked 11 Nov 2026."
)
REL = "pricing/chargeflow-vs-stripe-smart-disputes-year-1-cost/index.html"
CANONICAL = "/pricing/chargeflow-vs-stripe-smart-disputes-year-1-cost/"

CONTROLS = """
        <div class="wb-control-item">
          <label class="wb-control-label" for="sd-disputes">Monthly disputes <span class="val-pill" id="sd-disputes-val">10</span></label>
          <div class="wb-slider-row">
            <input type="range" id="sd-disputes" min="0" max="100" step="1" value="10" aria-label="Monthly disputes" data-track="calculator-control" data-control="disputes" />
          </div>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="sd-amount">Average disputed amount <span class="val-pill" id="sd-amount-val">$100</span></label>
          <div class="wb-slider-row">
            <input type="range" id="sd-amount" min="20" max="500" step="5" value="100" aria-label="Average disputed amount" data-track="calculator-control" data-control="amount" />
          </div>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="sd-win">Win rate (our planning assumption, adjust to yours) <span class="val-pill" id="sd-win-val">50%</span></label>
          <div class="wb-slider-row">
            <input type="range" id="sd-win" min="0" max="100" step="5" value="50" aria-label="Win rate" data-track="calculator-control" data-control="win-rate" />
          </div>
        </div>
        <p class="wb-budget-subnote">Year 1 is 12 months.</p>
"""

REST = r"""
<section id="sd-compare">
  <h2>Three ways to answer the same disputes</h2>
  <p id="sd-caption">12 months.</p>
  <div class="table-wrap editorial-gap-table mobile-cards">
    <table>
      <caption>Each path also pays the $15 dispute received fee.</caption>
      <thead>
        <tr>
          <th>Path</th>
          <th>What is priced</th>
          <th>Year-1</th>
        </tr>
      </thead>
      <tbody id="sd-body">
        <tr><td data-label="Path">Manual response</td><td data-label="What is priced">$15 countered fee kept on losses</td><td data-label="Year-1">$2,700</td></tr>
        <tr><td data-label="Path">Stripe Smart Disputes</td><td data-label="What is priced">30% of the amount you win. No fee on a loss.</td><td data-label="Year-1">$3,600</td></tr>
        <tr><td data-label="Path">Chargeflow Automation</td><td data-label="What is priced">25% of the amount you recover. The countered fee, if Stripe bills it when Chargeflow files the response, is unknown and is not added.</td><td data-label="Year-1">$3,300</td></tr>
      </tbody>
    </table>
  </div>
</section>

<section>
  <h2>What is not in the Year-1 figure</h2>
  <ul class="key-list">
    <li>The manual response total covers only Stripe's fees. It does not include the time your team spends preparing evidence.</li>
    <li>Smart Disputes is in public preview. Eligibility depends on the reason code, the payment method, and whether evidence is available. This total assumes the dispute is eligible. A dispute that is not eligible is unknown here.</li>
    <li>The appeal fee is $15 and is not returned even if you win. This page does not ask how many appeals you file, so appeal fees stay unknown.</li>
    <li>Chargeflow Insights is $0. Prevent is $0.10 per scanned transaction, and the first 1,000 scanned transactions are free. Alerts are $29 per deflected chargeback. A lower Alerts price above 50 a month is not published, so that discount is unknown. None of those products are in the Automation total above.</li>
    <li>Chargeflow says eligible ecommerce and SaaS startups can get up to 70% off. Who qualifies is not stated, so the discount is unknown and is not applied.</li>
    <li>Chargeflow's "4x ROI Guarantee" is marketing. It is not a measured result and it is not used here.</li>
  </ul>
</section>

<section>
  <h2>Stripe Chargeback Protection</h2>
  <p>Stripe Chargeback Protection is not listed on the US pricing page checked 11 Nov 2026. The old product page redirects to Radar, which does not mention it. Terms last updated 3 June 2019 are still online and say the fee is sent by email or shown in the Dashboard. Current availability and the current price are unknown. Check your own Dashboard. A 2019 launch price is not used here. One Stripe user wrote on 18 Oct 2025 that Stripe said the service was being discontinued and refunded the charges. That is one account, not a Stripe notice.</p>
</section>

<section>
  <h2>Sources checked 11 Nov 2026</h2>
  <p class="src-cluster"><a class="src-link" href="https://stripe.com/us/pricing" target="_blank" rel="noopener">Stripe US pricing</a> <span class="src-date">Accessed 2026-11-11</span></p>
  <p class="src-cluster"><a class="src-link" href="https://docs.stripe.com/disputes/smart-disputes" target="_blank" rel="noopener">Stripe Smart Disputes</a> <span class="src-date">Accessed 2026-11-11</span></p>
  <p class="src-cluster"><a class="src-link" href="https://www.chargeflow.io/pricing" target="_blank" rel="noopener">Chargeflow pricing</a> <span class="src-date">Accessed 2026-11-12</span></p>
  <p class="src-cluster"><a class="src-link" href="https://stripe.com/legal/chargeback-protection" target="_blank" rel="noopener">Stripe Chargeback Protection terms</a> <span class="src-date">Accessed 2026-11-11</span></p>
  <p class="src-cluster"><a class="src-link" href="https://www.reddit.com/r/stripe/comments/1m3i609/stripe_chargeback_protection/" target="_blank" rel="noopener">One Stripe user's account, 18 Oct 2025</a> <span class="src-date">Accessed 2026-11-11</span></p>
</section>
<script>
function sdMoney(cents) {
  var v = Math.round(cents);
  var sign = v < 0 ? "-" : "";
  var abs = Math.abs(v);
  var dollars = Math.floor(abs / 100);
  var rest = abs % 100;
  var text = sign + "$" + dollars.toLocaleString("en-US");
  if (rest) text += "." + (rest < 10 ? "0" : "") + rest;
  return text;
}

function calcSmartDisputes(input) {
  var disputes = Math.max(0, Math.round(Number(input.disputes) || 0));
  var amount = Math.max(0, Math.round(Number(input.amount) || 0));
  var win = Math.max(0, Math.min(100, Math.round(Number(input.win) || 0)));
  var won = disputes * win / 100;
  var lost = disputes - won;
  var received = Math.round(disputes * 1500);
  var countered = Math.round(lost * 1500);
  var wonCents = Math.round(won * amount * 100);
  var smartFee = Math.round(wonCents * 30 / 100);
  var cfFee = Math.round(wonCents * 25 / 100);
  return {
    disputes: disputes,
    amount: amount,
    win: win,
    received: received * 12,
    countered: countered * 12,
    smartFee: smartFee * 12,
    cfFee: cfFee * 12,
    manual: (received + countered) * 12,
    smart: (received + smartFee) * 12,
    chargeflow: (received + cfFee) * 12
  };
}

function sdRead() {
  return {
    disputes: document.getElementById("sd-disputes").value,
    amount: document.getElementById("sd-amount").value,
    win: document.getElementById("sd-win").value
  };
}

function renderSmartDisputes() {
  var c = calcSmartDisputes(sdRead());
  document.getElementById("sd-disputes-val").textContent = String(c.disputes);
  document.getElementById("sd-amount-val").textContent = sdMoney(c.amount * 100);
  document.getElementById("sd-win-val").textContent = c.win + "%";
  document.getElementById("shell-product").textContent = "Manual response";
  document.getElementById("shell-big").textContent = sdMoney(c.manual);
  document.getElementById("shell-sub").textContent = "";
  document.getElementById("shell-best").textContent = "";
  var bars = [
    ["shell-amt-base", "shell-title-base", "shell-sub-base", "Manual response", c.manual, "Countered fee kept on losses"],
    ["shell-amt-seats", "shell-title-seats", "shell-sub-seats", "Smart Disputes", c.smart, "30% of the amount you win"],
    ["shell-amt-hidden", "shell-title-hidden", "shell-sub-hidden", "Chargeflow", c.chargeflow, "25% of the amount you recover"]
  ];
  bars.forEach(function (bar) {
    document.getElementById(bar[0]).textContent = sdMoney(bar[4]);
    document.getElementById(bar[1]).textContent = bar[3];
    document.getElementById(bar[2]).textContent = bar[5];
  });
  document.getElementById("sd-body").innerHTML = ""
    + "<tr><td data-label=\"Path\">Manual response</td><td data-label=\"What is priced\">$15 countered fee kept on losses</td><td data-label=\"Year-1\">" + sdMoney(c.manual) + "</td></tr>"
    + "<tr><td data-label=\"Path\">Stripe Smart Disputes</td><td data-label=\"What is priced\">30% of the amount you win. No fee on a loss.</td><td data-label=\"Year-1\">" + sdMoney(c.smart) + "</td></tr>"
    + "<tr><td data-label=\"Path\">Chargeflow Automation</td><td data-label=\"What is priced\">25% of the amount you recover. The countered fee, if Stripe bills it when Chargeflow files the response, is unknown and is not added.</td><td data-label=\"Year-1\">" + sdMoney(c.chargeflow) + "</td></tr>";
  document.getElementById("shell-math").textContent = "Received fees " + sdMoney(c.received) + ". Countered fees kept on losses " + sdMoney(c.countered) + ". Manual " + sdMoney(c.manual) + ". Smart Disputes fee " + sdMoney(c.smartFee) + ". Chargeflow fee " + sdMoney(c.cfFee) + ".";
}

["sd-disputes", "sd-amount", "sd-win"].forEach(function (id) {
  document.getElementById(id).addEventListener("input", renderSmartDisputes);
});
renderSmartDisputes();
</script>
"""

FAQS = []


def copy_to_root(rel):
    src = os.path.join(PUBLIC_DIR, rel)
    dst = os.path.join(BASE_DIR, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src, dst)


def build():
    if len(TITLE) > 60:
        raise SystemExit("Title is %s chars: %s" % (len(TITLE), TITLE))
    blob = TITLE + DESCRIPTION + CONTROLS + REST
    if "\u2014" in blob or "Best option" in blob or "Winner" in blob:
        raise SystemExit("banned copy in the Chargeflow page")
    if "0.4%" in blob:
        raise SystemExit("do not print 0.4% as a Chargeback Protection price")
    workbench = render_workbench(
        CONTROLS,
        controls_title="Your disputes",
        chart_title="Modeled Year-1 cost",
        cta_href="#sd-compare",
        cta_label="See the three costs",
        cta_vendor="saasbill",
    )
    for old, new in (
        ('class="wb-vbar-container"', 'class="wb-vbar-container wb-vbar-separate"'),
        ('id="shell-product">Year-1 total<', 'id="shell-product">Manual response<'),
        ('id="shell-big">$0<', 'id="shell-big">$2,700<'),
        ('id="shell-sub">Matches advertised price ($0 hidden fees).</p>', 'id="shell-sub"></p>'),
        ('id="shell-title-base">Sticker Price<', 'id="shell-title-base">Manual response<'),
        ('id="shell-sub-base">Advertised price<', 'id="shell-sub-base">Countered fee kept on losses<'),
        ('id="shell-amt-base">$0<', 'id="shell-amt-base">$2,700<'),
        ('id="shell-title-seats">Other sticker fees<', 'id="shell-title-seats">Smart Disputes<'),
        ('id="shell-sub-seats">Included in the sticker<', 'id="shell-sub-seats">30% of the amount you win<'),
        ('id="shell-amt-seats">$0<', 'id="shell-amt-seats">$3,600<'),
        ('id="shell-title-hidden">Hidden Cost Gap<', 'id="shell-title-hidden">Chargeflow<'),
        ('id="shell-sub-hidden">Fees above the advertised price<', 'id="shell-sub-hidden">25% of the amount you recover<'),
        ('id="shell-amt-hidden">$0<', 'id="shell-amt-hidden">$3,300<'),
        ('<a id="shell-cta" class="btn-cta wb-primary-cta" href="#sd-compare">See the three costs &rarr;</a>', ''),
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
        "<h1>What does Chargeflow cost versus Stripe Smart Disputes in Year 1?</h1>"
        '<p class="lead">This page compares a manual Stripe response, Stripe Smart Disputes, and Chargeflow Automation.</p>'
        "</section>"
        + workbench
        + REST
    )
    if "/go/" in body or "sponsored" in body:
        raise SystemExit("affiliate tracking on the Chargeflow page")
    render_page(
        REL,
        TITLE,
        DESCRIPTION,
        CANONICAL,
        wrap_calculator_shell(body),
        faqs=None,
        published_date="2026-11-11",
        show_affiliate_note=False,
    )
    copy_to_root(REL)


if __name__ == "__main__":
    build()
