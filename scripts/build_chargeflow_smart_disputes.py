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
    "At 10 disputes a month and a $100 amount, a 50% win rate you set puts manual "
    "response at $2,700, Chargeflow at $3,300, and Smart Disputes at $3,600. Checked 11 Nov 2026."
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
          <label class="wb-control-label" for="sd-win">Win rate you set <span class="val-pill" id="sd-win-val">50%</span></label>
          <div class="wb-slider-row">
            <input type="range" id="sd-win" min="0" max="100" step="5" value="50" aria-label="Win rate you set" data-track="calculator-control" data-control="win-rate" />
          </div>
          <p class="wb-budget-subnote">Assumption. Change it. It is not a Stripe or Chargeflow statistic.</p>
        </div>
        <p class="wb-budget-subnote">Year 1 is 12 months. The $15 dispute received fee stays on every dispute.</p>
"""

REST = r"""
<section id="sd-compare">
  <h2>Three ways to answer the same disputes</h2>
  <p id="sd-caption">10 disputes a month, $100 disputed, 50% win rate you set, for 12 months. Not a ranking.</p>
  <div class="table-wrap editorial-gap-table mobile-cards">
    <table>
      <caption>Year-1 cost of the response. The win rate is an assumption.</caption>
      <thead>
        <tr>
          <th>Path</th>
          <th>What is priced</th>
          <th>Year-1</th>
        </tr>
      </thead>
      <tbody id="sd-body">
        <tr><td data-label="Path">Manual response</td><td data-label="What is priced">$15 received on every dispute, plus $15 countered kept on losses</td><td data-label="Year-1">$2,700</td></tr>
        <tr><td data-label="Path">Stripe Smart Disputes</td><td data-label="What is priced">$15 received, plus 30% of the amount you win. No fee on a loss.</td><td data-label="Year-1">$3,600</td></tr>
        <tr><td data-label="Path">Chargeflow Automation</td><td data-label="What is priced">$15 received, plus 25% of the amount you recover. The 25% does not include the dispute fee.</td><td data-label="Year-1">$3,300</td></tr>
      </tbody>
    </table>
  </div>
  <p id="sd-note" class="summary-caveat">Neither Smart Disputes nor Chargeflow removes the $15 dispute received fee. The countered fee on a response Chargeflow files is unknown and is not added.</p>
</section>

<section>
  <h2>What is not in the Year-1 figure</h2>
  <ul class="key-list">
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
  <p class="src-cluster"><a class="src-link" href="https://www.chargeflow.io/pricing" target="_blank" rel="noopener">Chargeflow pricing</a> <span class="src-date">Accessed 2026-11-11</span></p>
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

function sdLowest(c) {
  var rows = [
    ["Manual response", c.manual],
    ["Stripe Smart Disputes", c.smart],
    ["Chargeflow Automation", c.chargeflow]
  ];
  var low = rows[0][1];
  rows.forEach(function (row) { if (row[1] < low) low = row[1]; });
  var names = rows.filter(function (row) { return row[1] === low; }).map(function (row) { return row[0]; });
  return { cents: low, names: names };
}

function renderSmartDisputes() {
  var c = calcSmartDisputes(sdRead());
  document.getElementById("sd-disputes-val").textContent = String(c.disputes);
  document.getElementById("sd-amount-val").textContent = sdMoney(c.amount * 100);
  document.getElementById("sd-win-val").textContent = c.win + "%";
  var low = sdLowest(c);
  var named = low.names.length === 1 ? low.names[0] : low.names.join(" and ");
  document.getElementById("shell-product").textContent = named + ", " + c.disputes + " disputes";
  document.getElementById("shell-big").textContent = sdMoney(low.cents);
  document.getElementById("shell-sub").textContent = "Modeled at a " + c.win + "% win rate you can change. That rate is an assumption, not a Stripe or Chargeflow figure. Neither tool removes the $15 dispute received fee.";
  var bars = [
    ["shell-amt-base", "shell-title-base", "shell-sub-base", "Manual response", c.manual, "Received fee, plus countered fee kept on losses"],
    ["shell-amt-seats", "shell-title-seats", "shell-sub-seats", "Smart Disputes", c.smart, "30% of the amount you win, plus the received fee"],
    ["shell-amt-hidden", "shell-title-hidden", "shell-sub-hidden", "Chargeflow", c.chargeflow, "25% of the amount you recover, plus the received fee"]
  ];
  bars.forEach(function (bar) {
    document.getElementById(bar[0]).textContent = sdMoney(bar[4]);
    document.getElementById(bar[1]).textContent = bar[3];
    document.getElementById(bar[2]).textContent = bar[5];
  });
  document.getElementById("shell-sticker").textContent = sdMoney(c.manual);
  document.getElementById("shell-sticker-note").textContent = c.win + "% win rate, an assumption";
  document.getElementById("shell-gap").textContent = sdMoney(c.chargeflow);
  var notes = document.querySelectorAll("#shell-summary .summary-scenario");
  if (notes.length >= 2) notes[1].textContent = "Smart Disputes is " + sdMoney(c.smart);
  var best = low.names.length === 1
    ? "Lowest modeled Year-1 cost: " + low.names[0] + ", " + sdMoney(low.cents) + ", at the " + c.win + "% win rate you set. That rate is an assumption."
    : "Same modeled Year-1 cost: " + named + ", " + sdMoney(low.cents) + ", at the " + c.win + "% win rate you set. That rate is an assumption.";
  document.getElementById("shell-best").textContent = best;
  document.getElementById("sd-caption").textContent = c.disputes + " disputes a month, " + sdMoney(c.amount * 100) + " disputed, " + c.win + "% win rate you set, for 12 months. Not a ranking.";
  document.getElementById("sd-body").innerHTML = ""
    + "<tr><td data-label=\"Path\">Manual response</td><td data-label=\"What is priced\">$15 received on every dispute, plus $15 countered kept on losses</td><td data-label=\"Year-1\">" + sdMoney(c.manual) + "</td></tr>"
    + "<tr><td data-label=\"Path\">Stripe Smart Disputes</td><td data-label=\"What is priced\">$15 received, plus 30% of the amount you win. No fee on a loss.</td><td data-label=\"Year-1\">" + sdMoney(c.smart) + "</td></tr>"
    + "<tr><td data-label=\"Path\">Chargeflow Automation</td><td data-label=\"What is priced\">$15 received, plus 25% of the amount you recover. The 25% does not include the dispute fee.</td><td data-label=\"Year-1\">" + sdMoney(c.chargeflow) + "</td></tr>";
  document.getElementById("shell-math").textContent = c.disputes + " disputes. Amount " + sdMoney(c.amount * 100) + ". Win rate " + c.win + "% (assumption). Received fees " + sdMoney(c.received) + ". Countered fees kept on losses " + sdMoney(c.countered) + ". Manual " + sdMoney(c.manual) + ". Smart Disputes fee " + sdMoney(c.smartFee) + ", total " + sdMoney(c.smart) + ". Chargeflow fee " + sdMoney(c.cfFee) + ", total " + sdMoney(c.chargeflow) + ". Appeal fees, Prevent, Alerts, and the startup discount stay unknown.";
}

["sd-disputes", "sd-amount", "sd-win"].forEach(function (id) {
  document.getElementById(id).addEventListener("input", renderSmartDisputes);
});
renderSmartDisputes();
</script>
"""

FAQS = [
    (
        "Does Chargeflow's 25% include Stripe's dispute fee?",
        "No. Chargeflow's pricing page says the 25% applies only to the recovered amount and does not include the dispute fee. This page still adds Stripe's $15 dispute received fee on every dispute. The $15 countered fee for a response Chargeflow files is not stated on the pages checked 11 Nov 2026, so it stays unknown and is not added.",
    ),
    (
        "What does Stripe Smart Disputes cost?",
        "On the US pricing page checked 11 Nov 2026, Smart Disputes is 30% of the disputed amount for each dispute you win, and there is no Smart Disputes fee on a loss. The $15 dispute received fee still applies. The product is in public preview, and eligibility for a given dispute is unknown until Stripe accepts it.",
    ),
    (
        "Is Stripe Chargeback Protection still for sale?",
        "It is not listed on the US pricing page checked 11 Nov 2026, and the old product page redirects to Radar. Terms last updated 3 June 2019 are still online. Current availability and the current price are unknown. Check the Dashboard. A 2019 launch price is not used on this page.",
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
        ('id="shell-product">Year-1 total<', 'id="shell-product">Manual response, 10 disputes<'),
        ('id="shell-big">$0<', 'id="shell-big">$2,700<'),
        ('id="shell-sub">Matches advertised price ($0 hidden fees).</p>', 'id="shell-sub">Modeled at a 50% win rate you can change. That rate is an assumption, not a Stripe or Chargeflow figure. Neither tool removes the $15 dispute received fee.</p>'),
        ('id="shell-title-base">Sticker Price<', 'id="shell-title-base">Manual response<'),
        ('id="shell-sub-base">Advertised price<', 'id="shell-sub-base">Received fee, plus countered fee kept on losses<'),
        ('id="shell-amt-base">$0<', 'id="shell-amt-base">$2,700<'),
        ('id="shell-title-seats">Other sticker fees<', 'id="shell-title-seats">Smart Disputes<'),
        ('id="shell-sub-seats">Included in the sticker<', 'id="shell-sub-seats">30% of the amount you win, plus the received fee<'),
        ('id="shell-amt-seats">$0<', 'id="shell-amt-seats">$3,600<'),
        ('id="shell-title-hidden">Hidden Cost Gap<', 'id="shell-title-hidden">Chargeflow<'),
        ('id="shell-sub-hidden">Fees above the advertised price<', 'id="shell-sub-hidden">25% of the amount you recover, plus the received fee<'),
        ('id="shell-amt-hidden">$0<', 'id="shell-amt-hidden">$3,300<'),
        ('<div class="summary-label">Sticker Price</div>', '<div class="summary-label">Manual response</div>'),
        ('id="shell-sticker">$0<', 'id="shell-sticker">$2,700<'),
        ('id="shell-sticker-note">Advertised price<', 'id="shell-sticker-note">50% win rate, an assumption<'),
        ('<div class="summary-label">Hidden Cost Gap</div>', '<div class="summary-label">Chargeflow Automation</div>'),
        ('id="shell-gap">$0<', 'id="shell-gap">$3,300<'),
        ('<div class="summary-scenario">Above the advertised price</div>', '<div class="summary-scenario">Smart Disputes is $3,600</div>'),
        ('aria-label="Sticker price and hidden cost gap"', 'aria-label="Modeled Year-1 costs"'),
        ('id="shell-best"></div>', 'id="shell-best">Lowest modeled Year-1 cost: Manual response, $2,700, at the 50% win rate you set. That rate is an assumption.</div>'),
    ):
        if old not in workbench:
            raise SystemExit("missing workbench fallback: " + old)
        workbench = workbench.replace(old, new, 1)
    body = (
        '<section class="hero">'
        "<h1>What does Chargeflow cost versus Stripe Smart Disputes in Year 1?</h1>"
        '<p class="lead">At 10 disputes a month and a $100 disputed amount, a 50% win rate you set puts a manual Stripe response at $2,700. '
        "Chargeflow Automation is $3,300. Stripe Smart Disputes is $3,600. "
        "The win rate is an assumption, not a published statistic. Change it.</p>"
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
        faqs=FAQS,
        published_date="2026-11-11",
        show_affiliate_note=False,
    )
    copy_to_root(REL)


if __name__ == "__main__":
    build()
