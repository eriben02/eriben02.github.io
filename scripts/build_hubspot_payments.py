"""HubSpot payments versus Stripe connected to HubSpot.

Checked 2026-11-12.
HubSpot payments FAQ (last updated 22 Sep 2026) and the connect-Stripe article
(last updated 28 Oct 2026). Stripe US pricing: domestic cards 2.9% + $0.30,
ACH Direct Debit 0.8% with a $5 cap, dispute received fee $15.00.
No HubSpot affiliate link.
"""
import os
import shutil

from layout import BASE_DIR, PUBLIC_DIR, render_page, render_workbench, wrap_calculator_shell

TITLE = "HubSpot Payments vs Stripe fees – saasbill.io"
DESCRIPTION = (
    "Compares HubSpot payments with Stripe connected to HubSpot. Checked 12 Nov 2026."
)
CANONICAL = "/pricing/hubspot-payments-vs-stripe-platform-fee-year-1-cost/"
REL = "pricing/hubspot-payments-vs-stripe-platform-fee-year-1-cost/index.html"

CONTROLS = r"""
        <div class="wb-control-item">
          <label class="wb-control-label" for="hp-country">Country</label>
          <select id="hp-country" class="wb-tool-select" data-track="calculator-control" data-control="country">
            <option value="us" selected>United States</option>
            <option value="uk">United Kingdom</option>
            <option value="ca">Canada</option>
            <option value="other">Other</option>
          </select>
          <p class="wb-budget-subnote">HubSpot payments is listed for businesses in the US, UK, and Canada. Another country uses a connected Stripe account.</p>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="hp-card">Monthly card volume <span class="val-pill" id="hp-card-val">$10,000</span></label>
          <div class="wb-slider-row">
            <input type="range" id="hp-card" min="0" max="200000" step="500" value="10000" aria-label="Monthly card volume" data-track="calculator-control" data-control="card-volume" />
          </div>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="hp-avg">Average transaction <span class="val-pill" id="hp-avg-val">$100</span></label>
          <div class="wb-slider-row">
            <input type="range" id="hp-avg" min="1" max="5000" step="1" value="100" aria-label="Average transaction" data-track="calculator-control" data-control="average-transaction" />
          </div>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="hp-intl">International cards <span class="val-pill" id="hp-intl-val">0%</span></label>
          <div class="wb-slider-row">
            <input type="range" id="hp-intl" min="0" max="100" step="5" value="0" aria-label="Share of card volume on international cards" data-track="calculator-control" data-control="international-share" />
          </div>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="hp-uk-intl">UK international cards</label>
          <select id="hp-uk-intl" class="wb-tool-select" data-track="calculator-control" data-control="uk-international">
            <option value="eea" selected>Non-UK EEA, +0.8%</option>
            <option value="noneea">Outside the EEA, +1.55%</option>
          </select>
          <p class="wb-budget-subnote">Used only for a UK business. The FAQ lists both adders.</p>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="hp-ach">ACH volume, as a percent of card volume <span class="val-pill" id="hp-ach-val">0%</span></label>
          <div class="wb-slider-row">
            <input type="range" id="hp-ach" min="0" max="100" step="5" value="0" aria-label="ACH volume as a percent of card volume" data-track="calculator-control" data-control="ach-share" />
          </div>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="hp-stripe-pct">Your Stripe card rate <span class="val-pill" id="hp-stripe-pct-val">2.9%</span></label>
          <div class="wb-slider-row">
            <input type="range" id="hp-stripe-pct" min="0" max="10" step="0.1" value="2.9" aria-label="Your Stripe card rate" data-track="calculator-control" data-control="stripe-rate" />
          </div>
          <p class="wb-budget-subnote">Default is Stripe's standard US domestic card rate, 2.9% + $0.30, checked 12 Nov 2026. Change it if your rate is different.</p>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="hp-stripe-fixed">Stripe fixed fee per card charge <span class="val-pill" id="hp-stripe-fixed-val">$0.30</span></label>
          <div class="wb-slider-row">
            <input type="range" id="hp-stripe-fixed" min="0" max="2" step="0.01" value="0.30" aria-label="Stripe fixed fee per card charge" data-track="calculator-control" data-control="stripe-fixed" />
          </div>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="hp-promo">First-year platform promotion</label>
          <select id="hp-promo" class="wb-tool-select" data-track="calculator-control" data-control="promotion">
            <option value="no" selected>Off</option>
            <option value="yes">On for Year 1</option>
          </select>
          <p class="wb-budget-subnote">Assumption. The 0% platform fee in Year 1 is a promotion for eligible customers. Who qualifies is not stated, so this stays off unless you turn it on. Year 2 uses 0.5% either way.</p>
        </div>
"""

REST = r"""
<section id="hp-fees">
  <h2>Year-1 and Year-2 fees</h2>
  <div class="table-wrap editorial-gap-table mobile-cards">
    <table>
      <caption>Twelve months of the fees on the volume you enter.</caption>
      <thead>
        <tr>
          <th>Path</th>
          <th>Year 1</th>
          <th>Year 2</th>
        </tr>
      </thead>
      <tbody id="hp-body">
        <tr><td data-label="Path">HubSpot payments</td><td data-label="Year 1">$4,080</td><td data-label="Year 2">$4,080</td></tr>
        <tr><td data-label="Path">Stripe connected to HubSpot</td><td data-label="Year 1">$4,740</td><td data-label="Year 2">$4,740</td></tr>
      </tbody>
    </table>
  </div>
  <p id="hp-note" class="summary-caveat">The 0.75% platform fee applies on top of Stripe's own fees. On bank debits, that 0.75% is uncapped.</p>
</section>

<section>
  <h2>What is not in these fees</h2>
  <ul class="key-list">
    <li>Currency conversion on HubSpot payments is +1% in the US and +2% in the UK and Canada. It is not in this total.</li>
    <li>Affirm and Klarna are 5.99% plus the platform fee. They are not in this total.</li>
    <li>HubSpot charges no refund fee. The original transaction fees are not returned.</li>
    <li>Taxes may apply to payment processing fees from 3 Aug 2026. Whether they apply here is unknown.</li>
    <li>A high-volume rate is possible through HubSpot's commerce team. The terms are unknown.</li>
    <li>Stripe's dispute received fee is $15. This page does not ask how many disputes you get, so dispute fees stay out of the total.</li>
    <li>Stripe lists +1.5% for international cards when currency conversion is required. It is not added unless you include it in the Stripe rate you enter.</li>
    <li>Outside the US, Stripe's own bank-debit fee was not on the US pricing page checked 12 Nov 2026, so it stays unknown and is not added.</li>
    <li>The Revenue Hub seat price is unknown and is not in this total. Invoices, payment links, and subscriptions have no monthly SaaS fee. Quotes and contracts need a Revenue Hub subscription.</li>
    <li>Payouts can be held during a document request or a risk review. A maximum monthly volume is set in underwriting.</li>
    <li>Downgrading to the free HubSpot plan ends HubSpot payments. Subscriptions keep billing for 30 days.</li>
  </ul>
</section>

<section>
  <h2>What users wrote</h2>
  <ul class="key-list">
    <li>On the HubSpot Community, a prospective customer calls the Stripe option's platform fee a dealbreaker. That is one post, not a measured result. <span class="src-cluster"><a class="src-link" href="https://community.hubspot.com/t/credit-card-payment-fees/64536/34" target="_blank" rel="noopener">HubSpot Community thread</a> <span class="src-date">Accessed 12 Nov 2026.</span></span></li>
    <li>On Reddit in October 2024, users describe the move from the older Stripe integration to the newer connection. Those are posts, not a measured result. <span class="src-cluster"><a class="src-link" href="https://www.reddit.com/r/hubspot/comments/1g8tx9x/hubspot_stripe_ends_on_november_4_what_are_you/" target="_blank" rel="noopener">Reddit thread, 21 Oct 2024</a> <span class="src-date">Accessed 12 Nov 2026.</span></span></li>
  </ul>
</section>

<p class="summary-caveat">Checked 12 Nov 2026. <span class="src-cluster"><a class="src-link" href="https://knowledge.hubspot.com/payment-processing/payments-frequently-asked-questions" target="_blank" rel="noopener">HubSpot payments FAQ</a> <span class="src-date">Last updated 22 Sep 2026. Accessed 12 Nov 2026.</span></span> <span class="src-cluster"><a class="src-link" href="https://knowledge.hubspot.com/payment-processing/connect-your-stripe-account-as-a-payment-processor-in-hubspot" target="_blank" rel="noopener">Connect a Stripe account</a> <span class="src-date">Last updated 28 Oct 2026. Accessed 12 Nov 2026.</span></span> <span class="src-cluster"><a class="src-link" href="https://www.hubspot.com/products/revenue/payments" target="_blank" rel="noopener">HubSpot payments</a> <span class="src-date">Accessed 12 Nov 2026.</span></span> <span class="src-cluster"><a class="src-link" href="https://stripe.com/us/pricing" target="_blank" rel="noopener">Stripe US pricing</a> <span class="src-date">Accessed 12 Nov 2026.</span></span></p>
"""

SCRIPT = r"""
<script>
function calcHubspotPayments(input) {
  var country = input.country || "us";
  if (country !== "uk" && country !== "ca" && country !== "other") country = "us";
  var card = Math.max(0, Math.round(Number(input.card) || 0));
  var avg = Math.max(1, Math.round(Number(input.avg) || 1));
  var intl = Math.max(0, Math.min(100, Math.round(Number(input.intl) || 0)));
  var achPct = Math.max(0, Math.min(100, Math.round(Number(input.ach) || 0)));
  var stripePct = Number(input.stripePct);
  if (!isFinite(stripePct) || stripePct < 0) stripePct = 0;
  var stripeFixed = Number(input.stripeFixed);
  if (!isFinite(stripeFixed) || stripeFixed < 0) stripeFixed = 0;
  var promo = input.promo === "yes";
  var ukIntl = input.ukIntl === "noneea" ? 0.0155 : 0.008;
  var cardCents = card * 100;
  var avgCents = avg * 100;
  var achCents = Math.round(cardCents * achPct / 100);
  var cardTx = cardCents / avgCents;
  var achTx = achCents / avgCents;
  var intlShare = intl / 100;
  var offered = country !== "other";
  function cardRate() {
    if (country === "us") return 0.029 + 0.015 * intlShare;
    if (country === "uk") return 0.017 + ukIntl * intlShare;
    if (country === "ca") return 0.029 + 0.008 * intlShare;
    return 0;
  }
  function cappedMonth(volumeCents, txCount, rate, capCents) {
    if (volumeCents <= 0 || txCount <= 0) return 0;
    var per = Math.min(Math.round(avgCents * rate), capCents);
    return Math.round(per * txCount);
  }
  function platformRate(year) {
    if (promo && year === 1) return 0;
    return 0.005;
  }
  function hubspotYear(year) {
    if (!offered) return null;
    var pRate = platformRate(year);
    var cardFee = Math.round(cardCents * cardRate()) + Math.round(cardCents * pRate);
    var achProc = cappedMonth(achCents, achTx, 0.008, 1000);
    var achPlat = cappedMonth(achCents, achTx, pRate, 1000);
    return (cardFee + achProc + achPlat) * 12;
  }
  var fixedCents = Math.round(stripeFixed * 100);
  var stripeCard = Math.round(cardCents * stripePct / 100) + Math.round(cardTx * fixedCents) + Math.round(cardCents * 0.0075);
  var stripeAchPlat = Math.round(achCents * 0.0075);
  var stripeAchOwn = country === "us" ? cappedMonth(achCents, achTx, 0.008, 500) : (achCents > 0 ? null : 0);
  var stripeMonth = stripeCard + stripeAchPlat + (stripeAchOwn === null ? 0 : stripeAchOwn);
  return {
    country: country,
    offered: offered,
    card: card,
    avg: avg,
    intl: intl,
    achPct: achPct,
    promo: promo,
    stripePct: stripePct,
    stripeFixed: stripeFixed,
    cardRate: offered ? cardRate() : null,
    hubspot1: hubspotYear(1),
    hubspot2: hubspotYear(2),
    stripe1: stripeMonth * 12,
    stripe2: stripeMonth * 12,
    stripeAchUnknown: stripeAchOwn === null,
    achProcSample: offered ? cappedMonth(achCents, achTx, 0.008, 1000) : null,
    stripeAchSample: stripeAchOwn
  };
}

function hpMoney(cents) {
  if (cents === null) return "Not offered";
  var v = Math.round(cents);
  var neg = v < 0;
  v = Math.abs(v);
  var dollars = Math.floor(v / 100);
  var rem = v % 100;
  var text = "$" + dollars.toLocaleString("en-US");
  if (rem) text += "." + (rem < 10 ? "0" : "") + rem;
  return neg ? "-" + text : text;
}

function hpRateText(rate) {
  return (Math.round(rate * 1000) / 10) + "%";
}

function hpRead() {
  return {
    country: document.getElementById("hp-country").value,
    card: document.getElementById("hp-card").value,
    avg: document.getElementById("hp-avg").value,
    intl: document.getElementById("hp-intl").value,
    ukIntl: document.getElementById("hp-uk-intl").value,
    ach: document.getElementById("hp-ach").value,
    stripePct: document.getElementById("hp-stripe-pct").value,
    stripeFixed: document.getElementById("hp-stripe-fixed").value,
    promo: document.getElementById("hp-promo").value
  };
}

function renderHubspotPayments() {
  var c = calcHubspotPayments(hpRead());
  document.getElementById("hp-card-val").textContent = hpMoney(c.card * 100);
  document.getElementById("hp-avg-val").textContent = hpMoney(c.avg * 100);
  document.getElementById("hp-intl-val").textContent = c.intl + "%";
  document.getElementById("hp-ach-val").textContent = c.achPct + "%";
  document.getElementById("hp-stripe-pct-val").textContent = (Math.round(c.stripePct * 10) / 10) + "%";
  document.getElementById("hp-stripe-fixed-val").textContent = hpMoney(Math.round(c.stripeFixed * 100));
  var hubLabel = c.offered ? "HubSpot payments" : "Stripe connected to HubSpot";
  var big = c.offered ? c.hubspot1 : c.stripe1;
  document.getElementById("shell-product").textContent = hubLabel;
  document.getElementById("shell-big").textContent = hpMoney(big);
  document.getElementById("shell-sub").textContent = "";
  document.getElementById("shell-amt-base").textContent = hpMoney(c.hubspot1);
  document.getElementById("shell-title-base").textContent = "HubSpot payments";
  document.getElementById("shell-sub-base").textContent = "Year 1";
  document.getElementById("shell-amt-seats").textContent = hpMoney(c.stripe1);
  document.getElementById("shell-title-seats").textContent = "Stripe connected";
  document.getElementById("shell-sub-seats").textContent = "Year 1";
  document.getElementById("shell-amt-hidden").textContent = hpMoney(c.hubspot2);
  document.getElementById("shell-title-hidden").textContent = "HubSpot payments";
  document.getElementById("shell-sub-hidden").textContent = "Year 2";
  var baseRow = document.getElementById("shell-row-base");
  var seatsRow = document.getElementById("shell-row-seats");
  var hiddenRow = document.getElementById("shell-row-hidden");
  var baseAmt = c.hubspot1 === null ? 0 : c.hubspot1;
  var seatsAmt = c.stripe1;
  var hiddenAmt = c.hubspot2 === null ? 0 : c.hubspot2;
  var parts = Math.max(1, baseAmt + seatsAmt + hiddenAmt);
  baseRow.style.flex = Math.max(8, Math.round(baseAmt / parts * 100)) + " 1 0px";
  seatsRow.style.flex = Math.max(8, Math.round(seatsAmt / parts * 100)) + " 1 0px";
  hiddenRow.style.flex = Math.max(8, Math.round(hiddenAmt / parts * 100)) + " 1 0px";
  var best = "";
  if (c.offered) {
    if (c.hubspot1 < c.stripe1) best = "Lower Year-1 fee: HubSpot payments, " + hpMoney(c.hubspot1) + ".";
    else if (c.stripe1 < c.hubspot1) best = "Lower Year-1 fee: Stripe connected to HubSpot, " + hpMoney(c.stripe1) + ".";
    else best = "Same Year-1 fee: " + hpMoney(c.hubspot1) + ".";
  }
  document.getElementById("shell-best").textContent = best;
  document.getElementById("hp-body").innerHTML = ""
    + "<tr><td data-label=\"Path\">HubSpot payments</td><td data-label=\"Year 1\">" + hpMoney(c.hubspot1) + "</td><td data-label=\"Year 2\">" + hpMoney(c.hubspot2) + "</td></tr>"
    + "<tr><td data-label=\"Path\">Stripe connected to HubSpot</td><td data-label=\"Year 1\">" + hpMoney(c.stripe1) + "</td><td data-label=\"Year 2\">" + hpMoney(c.stripe2) + "</td></tr>";
  var cardRate = c.cardRate === null ? "not offered" : hpRateText(c.cardRate);
  var platform1 = c.promo ? "0%" : "0.5%";
  document.getElementById("shell-math").textContent = "Card volume " + hpMoney(c.card * 100) + " a month. Average transaction " + hpMoney(c.avg * 100) + ". ACH volume " + hpMoney(Math.round(c.card * 100 * c.achPct / 100)) + ". HubSpot card rate " + cardRate + ". Year-1 platform " + platform1 + ". ACH processing on HubSpot payments is 0.8% capped at $10 a transaction, and the platform fee on that ACH is capped at $10 a transaction. Stripe card rate " + (Math.round(c.stripePct * 10) / 10) + "% plus " + hpMoney(Math.round(c.stripeFixed * 100)) + " a charge. US ACH on Stripe is 0.8% capped at $5. HubSpot payments Year 1 " + hpMoney(c.hubspot1) + ", Year 2 " + hpMoney(c.hubspot2) + ". Stripe connected Year 1 " + hpMoney(c.stripe1) + ".";
}

["hp-country", "hp-card", "hp-avg", "hp-intl", "hp-uk-intl", "hp-ach", "hp-stripe-pct", "hp-stripe-fixed", "hp-promo"].forEach(function (id) {
  var el = document.getElementById(id);
  el.addEventListener("input", renderHubspotPayments);
  el.addEventListener("change", renderHubspotPayments);
});
renderHubspotPayments();
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
    blob = TITLE + DESCRIPTION + CONTROLS + REST + SCRIPT
    for banned in ("\u2014", "Best option", "Winner", "/go/", "sponsored"):
        if banned in blob:
            raise SystemExit("banned copy: " + banned)
    workbench = render_workbench(
        CONTROLS,
        controls_title="Your payments",
        chart_title="Year-1 fees",
        cta_href="#hp-fees",
        cta_label="Fee table",
        cta_vendor="saasbill",
    )
    for old, new in (
        ('class="wb-vbar-container"', 'class="wb-vbar-container wb-vbar-separate"'),
        ('id="shell-product">Year-1 total<', 'id="shell-product">HubSpot payments<'),
        ('id="shell-big">$0<', 'id="shell-big">$4,080<'),
        ('id="shell-sub">Matches advertised price ($0 hidden fees).</p>', 'id="shell-sub"></p>'),
        ('id="shell-title-base">Sticker Price<', 'id="shell-title-base">HubSpot payments<'),
        ('id="shell-sub-base">Advertised price<', 'id="shell-sub-base">Year 1<'),
        ('id="shell-amt-base">$0<', 'id="shell-amt-base">$4,080<'),
        ('id="shell-title-seats">Other sticker fees<', 'id="shell-title-seats">Stripe connected<'),
        ('id="shell-sub-seats">Included in the sticker<', 'id="shell-sub-seats">Year 1<'),
        ('id="shell-amt-seats">$0<', 'id="shell-amt-seats">$4,740<'),
        ('id="shell-title-hidden">Hidden Cost Gap<', 'id="shell-title-hidden">HubSpot payments<'),
        ('id="shell-sub-hidden">Fees above the advertised price<', 'id="shell-sub-hidden">Year 2<'),
        ('id="shell-amt-hidden">$0<', 'id="shell-amt-hidden">$4,080<'),
        ('id="shell-best"></div>', 'id="shell-best">Lower Year-1 fee: HubSpot payments, $4,080.</div>'),
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
        "<h1>What do HubSpot Payments fees cost versus connecting Stripe?</h1>"
        '<p class="lead">This page compares HubSpot payments with Stripe connected to HubSpot.</p>'
        "</section>"
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
        published_date="2026-11-12",
        show_affiliate_note=False,
    )
    copy_to_root(REL)


if __name__ == "__main__":
    build()
