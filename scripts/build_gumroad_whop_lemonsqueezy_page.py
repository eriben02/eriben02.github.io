"""Builds /compare/gumroad-vs-whop-vs-lemon-squeezy-take-rate-calculator/ (published 2026-10-26).
All fee figures verified 2026-10-26 against the official pages listed in SOURCES.
The Python calc() mirrors the JS calcPlatforms() 1:1 (tests/test_calculators.py checks both)."""
import json
from layout import render_page

SLUG = "/compare/gumroad-vs-whop-vs-lemon-squeezy-take-rate-calculator/"
REL = "compare/gumroad-vs-whop-vs-lemon-squeezy-take-rate-calculator/index.html"
TITLE = "Gumroad vs Whop vs Lemon Squeezy Fees (2026) – saasbill.io"
CHECKED = "Oct 26, 2026"
CHECKED_ISO = "2026-10-26"
WHOP_URL = "https://whop.com/sell?a=baggyprairieae"
GUMROAD_URL = "https://gumroad.com/pricing"
LS_URL = "https://www.lemonsqueezy.com/pricing"

# ---- Verified fee schedule (2026-10-26) ----
FEES = {
    "gumroad": {"pct": 0.10, "fixed": 0.50, "hv_pct": 0.05, "hv_threshold": 20000, "proc_pct": 0.029, "proc_fixed": 0.30, "discover_pct": 0.30},
    "ls": {"pct": 0.05, "fixed": 0.50, "intl": 0.015, "paypal": 0.015, "sub": 0.005, "dispute": 15.0, "payout_intl_pct": 0.01},
    "whop": {"pct": 0.027, "fixed": 0.30, "intl": 0.015, "fx": 0.01, "tax": 0.02, "billing": 0.005, "risk_fixed": 0.10, "dispute": 15.0, "ach_payout": 2.50, "payouts_per_month": 4},
}

DEFAULTS = dict(price=29.0, sales=200, intl=30, paypal=10, sub=False, discover=0, whop_tax="remit", whop_fx=True, whop_risk=True, dispute=0.5, payout="us")


def calc(price=29.0, sales=200, intl=30, paypal=10, sub=False, discover=0, whop_tax="remit", whop_fx=True, whop_risk=True, dispute=0.5, payout="us"):
    G = price * sales
    i, pp, disc, dr = intl / 100, paypal / 100, discover / 100, dispute / 100
    disputes = sales * dr
    g, l, w = FEES["gumroad"], FEES["ls"], FEES["whop"]
    # Gumroad: 10% + 50c (5% + 50c on direct sales after $20k paid sales in the month) + 2.9% + 30c processing; Discover 30% flat incl. processing
    direct = 1 - disc
    under = min(G, g["hv_threshold"]) * direct
    over = max(0, G - g["hv_threshold"]) * direct
    g_platform = under * g["pct"] + over * g["hv_pct"] + g["fixed"] * sales * direct
    g_proc = G * direct * g["proc_pct"] + g["proc_fixed"] * sales * direct
    g_disc = G * disc * g["discover_pct"]
    g_total = g_platform + g_proc + g_disc
    # Lemon Squeezy: 5% + 50c, +1.5% intl, +1.5% PayPal, +0.5% subscriptions, $15/dispute, 1% payout fee outside US
    l_platform = G * l["pct"] + l["fixed"] * sales
    l_extra = G * i * l["intl"] + G * pp * l["paypal"] + (G * l["sub"] if sub else 0)
    l_disp = disputes * l["dispute"]
    l_pre = l_platform + l_extra + l_disp
    l_payout = (G - l_pre) * l["payout_intl_pct"] if payout == "intl" else 0
    l_total = l_pre + l_payout
    # Whop: 2.7% + 30c, +1.5% intl cards, +1% FX, +2% tax (managed tax option), +0.5% billing (subs), $0.10 Radar+3DS, $15/dispute, $2.50 next-day ACH payout
    w_platform = G * w["pct"] + w["fixed"] * sales
    w_extra = G * i * w["intl"] + (G * i * w["fx"] if whop_fx else 0) + (w["risk_fixed"] * sales if whop_risk else 0)
    w_tax = G * w["tax"] if whop_tax != "none" else 0
    w_bill = G * w["billing"] if sub else 0
    w_disp = disputes * w["dispute"]
    w_payout = w["ach_payout"] * w["payouts_per_month"] if payout == "us" else 0
    w_total = w_platform + w_extra + w_tax + w_bill + w_disp + w_payout
    r = lambda x: round(x, 2)
    return {
        "gmv": r(G),
        "gumroad": {"platform": r(g_platform), "processing": r(g_proc), "discover": r(g_disc), "total": r(g_total), "net": r(G - g_total)},
        "ls": {"platform": r(l_platform), "surcharges": r(l_extra), "disputes": r(l_disp), "payout": r(l_payout), "total": r(l_total), "net": r(G - l_total)},
        "whop": {"platform": r(w_platform), "surcharges": r(w_extra), "tax": r(w_tax), "billing": r(w_bill), "disputes": r(w_disp), "payout": r(w_payout), "total": r(w_total), "net": r(G - w_total)},
    }


E = calc()
E_NOTAX = calc(whop_tax="none")
f = lambda n: f"{n:,.0f}"
f2 = lambda n: f"{n:,.2f}"
pct = lambda part, whole: f"{part / whole * 100:.1f}"

# Single $29 domestic card sale, for the per-sale table
def single(price):
    g = price * 0.10 + 0.50 + price * 0.029 + 0.30
    l = price * 0.05 + 0.50
    w = price * 0.027 + 0.30
    return g, l, w

S29 = single(29); S10 = single(10); S100 = single(100)

DESC = (f"Gumroad takes 10% + 50¢ plus 2.9% + 30¢ card processing; Lemon Squeezy 5% + 50¢ (+1.5% international/PayPal); Whop 2.7% + 30¢ (+2% for managed tax). "
        f"On $5,800/mo of $29 sales you net ${f(E['gumroad']['net'])} on Gumroad vs ${f(E['ls']['net'])} on Lemon Squeezy and ${f(E['whop']['net'])} on Whop. Verified {CHECKED}.")

SOURCES = [
    ("Gumroad pricing page (10% + $0.50 per direct sale; 30% via Discover; merchant of record since Jan 1, 2025)", GUMROAD_URL),
    ("Gumroad Help: Gumroad's fees (10% + $0.50 excludes credit card processing of 2.9% + $0.30 and PayPal fees; Discover 30% incl. processing; 5% + $0.50 after $20,000 paid sales in a calendar month; refunds keep processing portion)", "https://gumroad.com/help/article/66-gumroads-fees"),
    ("Gumroad Help: Getting paid ($100 minimum payout; 7-day holding period on weekly/monthly/quarterly payouts; PayPal payouts 2% fee; US instant payouts 3% up to $10K; account review 1–3 weeks)", "https://gumroad.com/help/article/13-getting-paid"),
    ("Gumroad Help: Chargebacks (creator covers refunded amount + processing fees, Gumroad returns platform fee; 25% balance reserve if chargebacks exceed 1.5% of 365-day sales volume)", "https://gumroad.com/help/article/134-how-does-gumroad-handle-chargebacks"),
    ("Lemon Squeezy pricing page (5% + 50¢ per transaction; no monthly fee; merchant of record; payouts twice a month)", LS_URL),
    ("Lemon Squeezy Docs: Fees (+1.5% international, +1.5% PayPal, +0.5% subscriptions; payouts free to US banks, 1% outside US; PayPal payouts $0.50 US / 3% capped at $30 outside US; +5% recovered carts, +3% affiliate referrals)", "https://docs.lemonsqueezy.com/help/getting-started/fees"),
    ("Lemon Squeezy Docs: Refunds and Chargebacks ($15 dispute fee deducted from next payout; may issue refunds within 60 days to prevent chargebacks)", "https://docs.lemonsqueezy.com/help/payments/refunds-chargebacks"),
    ("Lemon Squeezy blog: 2026 Update – Lemon Squeezy + Stripe Managed Payments (Jan 28, 2026; Stripe acquired Lemon Squeezy in 2024; goal is an easy migration to Stripe Managed Payments)", "https://www.lemonsqueezy.com/blog/2026-update"),
    ("Stripe Managed Payments (adds 3.5% per successful transaction on top of standard Stripe processing fees; Stripe becomes merchant of record)", "https://stripe.com/managed-payments"),
    ("Whop Docs: Fees (2.7% + $0.30 domestic cards; +1.5% international; +1% currency conversion; ACH 1.5% max $5; payouts: next-day ACH $2.50, RTP 4% + $2.50, wire $23; $15 dispute; $29 RDR alert; 3DS $0.03; Radar $0.07; orchestration 0.8%, billing 0.5%, tax 2%)", "https://docs.whop.com/fees"),
    ("Whop Docs: Taxes (direct sales: 'Whop collects and remits' covers US, EU, UK; managed options cost 2%; Discover sales handled by Whop as marketplace facilitator)", "https://docs.whop.com/payments-and-billing/fees/fees/taxes"),
    ("Whop Docs: Reserves (rolling and fixed reserves for new accounts / high dispute rates; release dates shown on Balances page)", "https://docs.whop.com/trust-and-safety/account-health/reserves"),
    ("Whop Seller Terms, last updated July 14, 2026 (reserves up to 100% of funds, held no longer than 180 days)", "https://whop.com/seller-terms/"),
    ("Whop Help: Advertising on Discover (0% commission on marketplace sales)", "https://help.whop.com/en/articles/11430710-advertising-on-whop-s-marketplace-discover"),
]
# Fix accidental path duplication in the Whop taxes URL
SOURCES = [(t, u.replace("/fees/fees/taxes", "/fees/taxes")) for t, u in SOURCES]


def rows_sources():
    return "\n".join(f'<li><a href="{u}" target="_blank" rel="noopener">{t}</a> &middot; <em>Verified source, checked {CHECKED}</em></li>' for t, u in SOURCES)


g, l, w = E["gumroad"], E["ls"], E["whop"]
G = E["gmv"]

body = f"""
<section class="hero">
  <h1>Gumroad (10% + 50¢ + processing) vs. Whop (2.7% + 30¢) vs. Lemon Squeezy (5% + 50¢): what you actually keep.</h1>
  <p class="lead">Headline rates hide the real take: Gumroad’s 10% excludes card processing, Lemon Squeezy adds 1.5% for international and PayPal buyers, and Whop’s 2.7% does not include tax handling. Enter your price and volume to see net payouts side by side.</p>
  <div class="geo-direct-answer">
    <p><strong>The short version:</strong> As of {CHECKED}, a $29 product selling 200 times a month (${f(G)} gross, 30% international buyers, 10% PayPal) nets <strong>${f(g['net'])} on Gumroad</strong> (${f(g['total'])} in fees, {pct(g['total'], G)}%: 10% + 50¢ plus 2.9% + 30¢ card processing), <strong>${f(l['net'])} on Lemon Squeezy</strong> (${f(l['total'])}, {pct(l['total'], G)}%: 5% + 50¢ plus surcharges and $15 per dispute) and <strong>${f(w['net'])} on Whop</strong> (${f(w['total'])}, {pct(w['total'], G)}%, including the optional 2% “Whop collects and remits” tax service; ${f(E_NOTAX['whop']['net'])} if you handle tax yourself). Over a year that is a <strong>${f((w['net'] - g['net']) * 12)}</strong> difference between Gumroad and Whop.</p>
  </div>
</section>

<section class="calc-box" id="calculator">
  <h2 style="margin-top:0;">Net payout calculator: Gumroad vs. Whop vs. Lemon Squeezy</h2>
  <p style="color:var(--muted); margin-bottom:16px; font-size:0.95rem;">Prefilled with a $29 digital product, 200 sales/month. Results update as you change the inputs below.</p>
  <div id="tr-summary" class="summary-strip" aria-live="polite"></div>
  <h3 style="margin:22px 0 10px; font-size:1rem;">Adjust your numbers</h3>
  <div class="calc-grid">
    <div class="control-group">
      <label for="tr-price">Price per sale (USD): <span class="val-pill" id="tr-price-val">$29</span></label>
      <input type="range" id="tr-price" min="1" max="500" step="1" value="29" data-track="calculator-control" data-control="price" />
    </div>
    <div class="control-group">
      <label for="tr-sales">Sales per month: <span class="val-pill" id="tr-sales-val">200</span></label>
      <input type="range" id="tr-sales" min="1" max="5000" step="1" value="200" data-track="calculator-control" data-control="sales" />
    </div>
    <div class="control-group">
      <label for="tr-intl">Buyers outside the US: <span class="val-pill" id="tr-intl-val">30</span>%</label>
      <input type="range" id="tr-intl" min="0" max="100" step="5" value="30" data-track="calculator-control" data-control="intl" />
    </div>
    <div class="control-group">
      <label for="tr-paypal">Buyers paying with PayPal: <span class="val-pill" id="tr-paypal-val">10</span>%</label>
      <input type="range" id="tr-paypal" min="0" max="100" step="5" value="10" data-track="calculator-control" data-control="paypal" />
    </div>
    <div class="control-group">
      <label for="tr-discover">Gumroad sales via Discover marketplace: <span class="val-pill" id="tr-discover-val">0</span>%</label>
      <input type="range" id="tr-discover" min="0" max="100" step="5" value="0" data-track="calculator-control" data-control="discover" />
    </div>
    <div class="control-group">
      <label for="tr-dispute">Dispute (chargeback) rate: <span class="val-pill" id="tr-dispute-val">0.5</span>%</label>
      <input type="range" id="tr-dispute" min="0" max="3" step="0.1" value="0.5" data-track="calculator-control" data-control="dispute" />
    </div>
    <div class="control-group">
      <label for="tr-sub">Billing type</label>
      <select id="tr-sub" data-track="calculator-control" data-control="billing">
        <option value="0" selected>One-time purchases</option>
        <option value="1">Subscriptions (+0.5% LS, +0.5% Whop Billing)</option>
      </select>
    </div>
    <div class="control-group">
      <label for="tr-tax">Whop tax handling (direct sales)</label>
      <select id="tr-tax" data-track="calculator-control" data-control="whop-tax">
        <option value="remit" selected>Whop collects &amp; remits (+2%, US/EU/UK)</option>
        <option value="collect">Whop collects, I remit (+2%)</option>
        <option value="none">I handle tax myself (+0%)</option>
      </select>
    </div>
    <div class="control-group">
      <label for="tr-fx">Whop currency conversion on international sales</label>
      <select id="tr-fx" data-track="calculator-control" data-control="whop-fx">
        <option value="1" selected>Yes (+1% on international sales)</option>
        <option value="0">No (buyers pay in USD)</option>
      </select>
    </div>
    <div class="control-group">
      <label for="tr-risk">Whop Radar + 3DS per-transaction fees</label>
      <select id="tr-risk" data-track="calculator-control" data-control="whop-risk">
        <option value="1" selected>Include ($0.07 + $0.03 per sale)</option>
        <option value="0">Exclude</option>
      </select>
    </div>
    <div class="control-group">
      <label for="tr-payout">Where you get paid</label>
      <select id="tr-payout" data-track="calculator-control" data-control="payout">
        <option value="us" selected>US bank account</option>
        <option value="intl">Bank account outside the US</option>
      </select>
    </div>
  </div>
  <div class="table-wrap mobile-cards" style="margin-top:20px;">
    <table>
      <caption>Monthly fees &amp; net payout: Gumroad vs. Lemon Squeezy vs. Whop (USD, fees verified {CHECKED})</caption>
      <thead><tr><th>Platform</th><th>Base fee / mo</th><th>Add-ons / mo</th><th>Total fees / mo</th><th>Net payout / yr</th><th>Next step</th></tr></thead>
      <tbody id="tr-tbody"></tbody>
    </table>
  </div>
  <p id="tr-note" style="font-size:0.84rem; color:var(--muted); margin-top:10px;"></p>
</section>

<section aria-labelledby="persale-heading">
  <h2 id="persale-heading">What each platform keeps from a single sale</h2>
  <p class="section-tldr">On a single $29 domestic card sale, Gumroad keeps ${f2(S29[0])}, Lemon Squeezy ${f2(S29[1])} and Whop ${f2(S29[2])} (before Whop’s optional 2% tax service). Fixed per-sale fees hurt cheap products most: on a $10 sale Gumroad takes {S10[0] / 10 * 100:.0f}%.</p>
  <div class="table-wrap mobile-cards">
    <table>
      <caption>Fee per US card sale, no add-ons (verified {CHECKED})</caption>
      <thead><tr><th>Sale price</th><th>Gumroad (10% + 50¢ + 2.9% + 30¢)</th><th>Lemon Squeezy (5% + 50¢)</th><th>Whop (2.7% + 30¢)</th></tr></thead>
      <tbody>
        <tr><td data-label="Sale price"><strong>$10</strong></td><td data-label="Gumroad (10% + 50¢ + 2.9% + 30¢)">${f2(S10[0])} ({S10[0] / 10 * 100:.1f}%)</td><td data-label="Lemon Squeezy (5% + 50¢)">${f2(S10[1])} ({S10[1] / 10 * 100:.1f}%)</td><td data-label="Whop (2.7% + 30¢)">${f2(S10[2])} ({S10[2] / 10 * 100:.1f}%)</td></tr>
        <tr><td data-label="Sale price"><strong>$29</strong></td><td data-label="Gumroad (10% + 50¢ + 2.9% + 30¢)">${f2(S29[0])} ({S29[0] / 29 * 100:.1f}%)</td><td data-label="Lemon Squeezy (5% + 50¢)">${f2(S29[1])} ({S29[1] / 29 * 100:.1f}%)</td><td data-label="Whop (2.7% + 30¢)">${f2(S29[2])} ({S29[2] / 29 * 100:.1f}%)</td></tr>
        <tr><td data-label="Sale price"><strong>$100</strong></td><td data-label="Gumroad (10% + 50¢ + 2.9% + 30¢)">${f2(S100[0])} ({S100[0]:.1f}%)</td><td data-label="Lemon Squeezy (5% + 50¢)">${f2(S100[1])} ({S100[1]:.1f}%)</td><td data-label="Whop (2.7% + 30¢)">${f2(S100[2])} ({S100[2]:.1f}%)</td></tr>
      </tbody>
    </table>
  </div>
</section>

<section aria-labelledby="terms-heading">
  <h2 id="terms-heading">Fee schedule, tax handling and payout rules compared</h2>
  <p class="section-tldr">Gumroad and Lemon Squeezy are merchants of record on every sale, so tax is included in their fee. Whop is cheaper per transaction, but on direct sales you choose between paying 2% for managed tax or handling tax yourself.</p>
  <div class="table-wrap mobile-cards">
    <table>
      <caption>Gumroad vs. Lemon Squeezy vs. Whop: verified terms ({CHECKED})</caption>
      <thead><tr><th>Item</th><th>Gumroad</th><th>Lemon Squeezy</th><th>Whop</th></tr></thead>
      <tbody>
        <tr><td data-label="Item"><strong>Headline fee</strong></td><td data-label="Gumroad">10% + $0.50 per direct sale</td><td data-label="Lemon Squeezy">5% + $0.50 per transaction</td><td data-label="Whop">2.7% + $0.30 (domestic cards)</td></tr>
        <tr><td data-label="Item"><strong>Card processing</strong></td><td data-label="Gumroad">+2.9% + $0.30 (not included in the 10%)</td><td data-label="Lemon Squeezy">Included</td><td data-label="Whop">Included</td></tr>
        <tr><td data-label="Item"><strong>International buyers</strong></td><td data-label="Gumroad">No surcharge listed</td><td data-label="Lemon Squeezy">+1.5%</td><td data-label="Whop">+1.5% international cards, +1% currency conversion</td></tr>
        <tr><td data-label="Item"><strong>PayPal</strong></td><td data-label="Gumroad">PayPal fees not included</td><td data-label="Lemon Squeezy">+1.5%</td><td data-label="Whop">Not listed on fees page</td></tr>
        <tr><td data-label="Item"><strong>Subscriptions</strong></td><td data-label="Gumroad">Same fee on every charge</td><td data-label="Lemon Squeezy">+0.5%</td><td data-label="Whop">Billing tool +0.5% when enabled</td></tr>
        <tr><td data-label="Item"><strong>Marketplace sales</strong></td><td data-label="Gumroad">30% flat (Discover, processing included)</td><td data-label="Lemon Squeezy">No marketplace</td><td data-label="Whop">0% commission (Discover)</td></tr>
        <tr><td data-label="Item"><strong>Volume discount</strong></td><td data-label="Gumroad">5% + $0.50 on direct sales after $20,000 paid sales in a calendar month</td><td data-label="Lemon Squeezy">Custom pricing on request</td><td data-label="Whop">Custom pricing on request</td></tr>
        <tr><td data-label="Item"><strong>Tax / merchant of record</strong></td><td data-label="Gumroad">Merchant of record since Jan 1, 2025 (included)</td><td data-label="Lemon Squeezy">Merchant of record (included)</td><td data-label="Whop">Discover sales handled; direct sales: +2% managed tax (remit option covers US, EU, UK) or do it yourself</td></tr>
        <tr><td data-label="Item"><strong>Dispute / chargeback</strong></td><td data-label="Gumroad">No separate fee; you lose the sale + processing, Gumroad returns its fee</td><td data-label="Lemon Squeezy">$15 per dispute</td><td data-label="Whop">$15 per dispute; $29 per early dispute alert (RDR)</td></tr>
        <tr><td data-label="Item"><strong>Payout fees</strong></td><td data-label="Gumroad">Bank: none listed; PayPal 2%; US instant 3%</td><td data-label="Lemon Squeezy">US bank free; non-US bank 1%; PayPal $0.50 US / 3% (max $30) non-US</td><td data-label="Whop">Next-day ACH $2.50; instant (RTP) 4% + $2.50; wire $23; international local banks vary</td></tr>
        <tr><td data-label="Item"><strong>Payout timing &amp; holds</strong></td><td data-label="Gumroad">$100 minimum; 7-day hold on weekly/monthly payouts; new-account review 1–3 weeks; 25% reserve if chargebacks &gt; 1.5%</td><td data-label="Lemon Squeezy">Twice-monthly payouts</td><td data-label="Whop">Funds withdrawable in 1–4 business days; reserves possible for new or high-risk accounts (up to 180 days per Seller Terms)</td></tr>
        <tr><td data-label="Item"><strong>Ownership / roadmap</strong></td><td data-label="Gumroad">Independent</td><td data-label="Lemon Squeezy">Owned by Stripe since 2024; stated goal is migration to Stripe Managed Payments (+3.5% on top of Stripe processing)</td><td data-label="Whop">Independent</td></tr>
      </tbody>
    </table>
  </div>
</section>

<section aria-labelledby="findings-heading">
  <h2 id="findings-heading">What we found in the fine print</h2>
  <ul class="key-list">
    <li><strong>Gumroad’s “10%” is really 12.9% + 80¢ on card sales.</strong> Gumroad’s own help center says the 10% + $0.50 fee “does not include” credit card processing (2.9% + $0.30) or PayPal fees.</li>
    <li><strong>Gumroad Discover costs 30%.</strong> Sales from new customers who find you through Gumroad’s marketplace pay a flat 30%, processing included. Whop charges 0% on its Discover marketplace.</li>
    <li><strong>Lemon Squeezy’s 5% + 50¢ grows with your buyer mix.</strong> International buyers add 1.5%, PayPal adds 1.5% and subscription payments add 0.5%, so a non-US PayPal subscriber costs 8.5% + 50¢.</li>
    <li><strong>Whop’s 2.7% does not include tax.</strong> For direct sales, “Whop collects and remits tax” (US, EU, UK) or “Whop collects tax, I remit” costs 2% per transaction; otherwise tax compliance stays with you.</li>
    <li><strong>Disputes:</strong> Lemon Squeezy and Whop each charge a flat $15 per dispute. Gumroad lists no dispute fee, but holds 25% of your balance if chargebacks exceed 1.5% of sales over 365 days.</li>
    <li><strong>Lemon Squeezy’s future runs through Stripe.</strong> In its January 28, 2026 update, Lemon Squeezy said its goal is to give users an easy way to migrate to Stripe Managed Payments, which adds 3.5% per transaction on top of standard Stripe processing fees.</li>
  </ul>
</section>

<section aria-labelledby="pick-heading">
  <h2 id="pick-heading">Which platform should you pick?</h2>
  <ul class="key-list">
    <li><strong>Whop</strong> has the lowest base rate (2.7% + 30¢) and charges 0% on marketplace sales, so it wins for mostly-US buyer mixes even with the 2% tax option. Watch the stack on international sales: 2.7% + 1.5% + 1% FX + 2% tax = 7.2% + 30¢, which is more than Lemon Squeezy’s 6.5% + 50¢ on non-US card sales priced above roughly $15–$29 (the break-even depends on whether Whop’s $0.10 Radar + 3DS fees apply). It fits sellers who either want Whop’s 2% managed tax option or already handle sales tax/VAT themselves. Budget for possible reserves on a new account.</li>
    <li><strong>Lemon Squeezy</strong> is a full merchant of record at 5% + 50¢ with license keys and software subscriptions built in. Weigh the Stripe Managed Payments migration path before building a new business on it.</li>
    <li><strong>Gumroad</strong> costs the most on direct sales (12.9% + 80¢ on card sales) but is the simplest way to launch with tax handled. Its fee drops to 5% + 50¢ (plus processing) on direct sales once you pass $20,000 in a month.</li>
  </ul>
</section>

<section aria-labelledby="sources-heading">
  <h2 id="sources-heading">Sources &amp; verification dates</h2>
  <ol class="key-list" style="font-size:0.9rem;">
    {rows_sources()}
  </ol>
</section>

<script>
const TR_FEES = {json.dumps(FEES)};
function calcPlatforms(o) {{
  const G = o.price * o.sales, i = o.intl / 100, pp = o.paypal / 100, disc = o.discover / 100, dr = o.dispute / 100;
  const disputes = o.sales * dr, g = TR_FEES.gumroad, l = TR_FEES.ls, w = TR_FEES.whop;
  const direct = 1 - disc;
  const under = Math.min(G, g.hv_threshold) * direct, over = Math.max(0, G - g.hv_threshold) * direct;
  const gPlatform = under * g.pct + over * g.hv_pct + g.fixed * o.sales * direct;
  const gProc = G * direct * g.proc_pct + g.proc_fixed * o.sales * direct;
  const gDisc = G * disc * g.discover_pct;
  const gTotal = gPlatform + gProc + gDisc;
  const lPlatform = G * l.pct + l.fixed * o.sales;
  const lExtra = G * i * l.intl + G * pp * l.paypal + (o.sub ? G * l.sub : 0);
  const lDisp = disputes * l.dispute;
  const lPre = lPlatform + lExtra + lDisp;
  const lPayout = o.payout === 'intl' ? (G - lPre) * l.payout_intl_pct : 0;
  const lTotal = lPre + lPayout;
  const wPlatform = G * w.pct + w.fixed * o.sales;
  const wExtra = G * i * w.intl + (o.whop_fx ? G * i * w.fx : 0) + (o.whop_risk ? w.risk_fixed * o.sales : 0);
  const wTax = o.whop_tax !== 'none' ? G * w.tax : 0;
  const wBill = o.sub ? G * w.billing : 0;
  const wDisp = disputes * w.dispute;
  const wPayout = o.payout === 'us' ? w.ach_payout * w.payouts_per_month : 0;
  const wTotal = wPlatform + wExtra + wTax + wBill + wDisp + wPayout;
  const r = x => Math.round(x * 100) / 100;
  return {{
    gmv: r(G),
    gumroad: {{platform: r(gPlatform), processing: r(gProc), discover: r(gDisc), total: r(gTotal), net: r(G - gTotal)}},
    ls: {{platform: r(lPlatform), surcharges: r(lExtra), disputes: r(lDisp), payout: r(lPayout), total: r(lTotal), net: r(G - lTotal)}},
    whop: {{platform: r(wPlatform), surcharges: r(wExtra), tax: r(wTax), billing: r(wBill), disputes: r(wDisp), payout: r(wPayout), total: r(wTotal), net: r(G - wTotal)}}
  }};
}}
const trFmt = n => '$' + Math.round(n).toLocaleString('en-US');
function trInputs() {{
  const v = id => document.getElementById(id).value;
  return {{price: +v('tr-price'), sales: +v('tr-sales'), intl: +v('tr-intl'), paypal: +v('tr-paypal'), discover: +v('tr-discover'), dispute: +v('tr-dispute'),
          sub: v('tr-sub') === '1', whop_tax: v('tr-tax'), whop_fx: v('tr-fx') === '1', whop_risk: v('tr-risk') === '1', payout: v('tr-payout')}};
}}
function updateTr() {{
  const o = trInputs();
  document.getElementById('tr-price-val').textContent = '$' + o.price;
  document.getElementById('tr-sales-val').textContent = o.sales.toLocaleString('en-US');
  document.getElementById('tr-intl-val').textContent = o.intl;
  document.getElementById('tr-paypal-val').textContent = o.paypal;
  document.getElementById('tr-discover-val').textContent = o.discover;
  document.getElementById('tr-dispute-val').textContent = o.dispute.toFixed(1);
  const R = calcPlatforms(o), G = R.gmv;
  const taxLabel = {{remit: 'Whop collects & remits tax (+2%)', collect: 'Whop collects tax, you remit (+2%)', none: 'you handle tax on Whop'}}[o.whop_tax];
  const scenarioLine = `Based on ${{o.sales.toLocaleString('en-US')}} sales/mo at $${{o.price}} (${{trFmt(G)}}/mo gross, ${{trFmt(G*12)}}/yr), ${{o.intl}}% international, ${{o.paypal}}% PayPal, ${{o.sub ? 'subscriptions' : 'one-time'}}, ${{o.dispute.toFixed(1)}}% disputes, ${{taxLabel}}`;
  const rows = [
    {{id: 'gumroad', name: 'Gumroad', sub: '10% + 50¢' + (o.discover ? ' · ' + o.discover + '% Discover at 30%' : '') + (G > 20000 ? ' · 5% + 50¢ above $20k/mo' : ''), base: R.gumroad.platform, addon: R.gumroad.processing + R.gumroad.discover,
     addonText: trFmt(R.gumroad.processing) + ' card processing' + (R.gumroad.discover ? ' + ' + trFmt(R.gumroad.discover) + ' Discover' : ''), hidden: R.gumroad.processing, hiddenText: 'card processing (2.9% + 30¢), which is not included in Gumroad’s 10% + 50¢',
     total: R.gumroad.total, net: R.gumroad.net, url: '{GUMROAD_URL}', cta: 'View Gumroad pricing →', tag: 'Direct vendor link', badge: 'badge-high'}},
    {{id: 'lemon-squeezy', name: 'Lemon Squeezy', sub: '5% + 50¢ · merchant of record', base: R.ls.platform, addon: R.ls.surcharges + R.ls.disputes + R.ls.payout,
     addonText: trFmt(R.ls.surcharges) + ' surcharges + ' + trFmt(R.ls.disputes) + ' disputes' + (R.ls.payout ? ' + ' + trFmt(R.ls.payout) + ' payout' : ''), hidden: R.ls.surcharges, hiddenText: 'international / PayPal / subscription surcharges (+1.5% / +1.5% / +0.5%)',
     total: R.ls.total, net: R.ls.net, url: '{LS_URL}', cta: 'View Lemon Squeezy pricing →', tag: 'Direct vendor link', badge: 'badge-medium'}},
    {{id: 'whop-payments', name: 'Whop', sub: '2.7% + 30¢' + (o.whop_tax !== 'none' ? ' · +2% managed tax' : ' · tax not included'), base: R.whop.platform, addon: R.whop.surcharges + R.whop.tax + R.whop.billing + R.whop.disputes + R.whop.payout,
     addonText: trFmt(R.whop.surcharges) + ' intl/FX/fraud + ' + trFmt(R.whop.tax) + ' tax + ' + trFmt(R.whop.disputes + R.whop.payout + R.whop.billing) + ' disputes/payouts' + (o.sub ? '/billing' : ''), hidden: R.whop.tax > R.whop.surcharges ? R.whop.tax : R.whop.surcharges,
     hiddenText: R.whop.tax > R.whop.surcharges ? 'the 2% managed tax option (tax is not included in 2.7% + 30¢)' : 'international card (+1.5%), currency conversion (+1%) and Radar/3DS fees',
     total: R.whop.total, net: R.whop.net, url: '{WHOP_URL}', cta: 'Start selling on Whop →', tag: 'Referral link · we may earn a commission', badge: 'badge-low'}}
  ].sort((a, b) => a.total - b.total);
  const low = rows[0], high = rows[rows.length - 1];
  const big = rows.slice().sort((a, b) => b.hidden - a.hidden)[0];
  const bigPct = big.total > 0 ? Math.round(big.hidden / big.total * 100) : 0;
  document.getElementById('tr-summary').innerHTML = `
    <div class="summary-card card-lowest">
      <div class="summary-label">Highest net payout</div>
      <div class="summary-metric" style="color:var(--emerald);">${{trFmt(low.net * 12)}} / yr &middot; ${{low.name}}</div>
      <div class="summary-scenario">${{scenarioLine}}</div>
      <div class="summary-breakdown">${{trFmt(low.total)}}/mo in fees (${{(low.total / G * 100).toFixed(1)}}% of gross) &middot; keeps ${{trFmt((low.net - high.net) * 12)}}/yr more than ${{high.name}}</div>
      <div class="summary-caveat"><strong>Hidden Cost Highlight:</strong> The biggest fee most sellers miss here is ${{big.name}}’s ${{big.hiddenText}}: ${{trFmt(big.hidden)}}/mo (${{trFmt(big.hidden * 12)}}/yr, ${{bigPct}}% of ${{big.name}}’s fees).</div>
      <div class="summary-actions">
        <div class="cta-stack">
          <a class="btn-cta" href="${{low.url}}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="${{low.id}}" data-cta-location="summary-card">${{low.cta}}</a>
        </div>
      </div>
    </div>
    <div class="summary-card card-hidden">
      <div class="summary-label">Annual fees &amp; net payout, all three</div>
      <div class="summary-metric" style="color:var(--rose);">${{high.name}}: ${{trFmt(high.total * 12)}} / yr in fees</div>
      <div class="summary-scenario">${{scenarioLine}}</div>
      <div class="summary-breakdown">${{rows.map(r => r.name + ' ' + trFmt(r.total * 12) + ' fees → ' + trFmt(r.net * 12) + ' net').join(' &middot; ')}}</div>
      <div class="summary-caveat"><strong>Before you switch:</strong> ${{o.whop_tax === 'none' ? 'Whop is shown without tax handling, so sales tax/VAT compliance stays with you.' : 'Gumroad and Lemon Squeezy include tax as merchant of record; Whop is shown with its 2% managed tax option.'}} New Whop and Gumroad accounts may see payout holds or reserves.</div>
    </div>`;
  document.getElementById('tr-tbody').innerHTML = rows.map(r => `
    <tr>
      <td data-label="Platform"><strong>${{r.name}}</strong> <span class="status-pill status-verified">Verified</span>
        <div style="font-size:0.78rem; color:var(--muted);">${{r.sub}}</div>
        <div class="source-inline">Verified source: <a href="${{r.id === 'gumroad' ? 'https://gumroad.com/help/article/66-gumroads-fees' : r.id === 'lemon-squeezy' ? 'https://docs.lemonsqueezy.com/help/getting-started/fees' : 'https://docs.whop.com/fees'}}" target="_blank" rel="noopener">Official fee docs &nearr;</a></div></td>
      <td data-label="Base fee / mo" style="font-family:var(--sans); font-variant-numeric:tabular-nums;">${{trFmt(r.base)}}</td>
      <td data-label="Add-ons / mo"><span class="badge ${{r.badge}}">${{r.addonText}}</span></td>
      <td data-label="Total fees / mo" class="price-highlight">${{trFmt(r.total)}} <span style="font-size:0.8rem; color:var(--muted);">(${{(r.total / G * 100).toFixed(1)}}%)</span></td>
      <td data-label="Net payout / yr" class="price-highlight">${{trFmt(r.net * 12)}}<div class="cell-scenario">${{scenarioLine}}</div></td>
      <td data-label="Next step"><div class="cta-stack"><a class="btn-secondary" href="${{r.url}}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="${{r.id}}" data-cta-location="table-row">${{r.cta}}</a></div></td>
    </tr>`).join('');
  let note = 'Assumptions: list prices, fees calculated on the pre-tax price (Lemon Squeezy calculates its fee on the order total including tax, so its real fee is slightly higher on taxed sales). Gumroad PayPal sales are modelled at the 2.9% + 30¢ card rate; actual PayPal fees may differ. Whop payouts assume 4 next-day ACH withdrawals/mo ($2.50 each). Lost revenue from chargebacks is the same on every platform and is not included.';
  if (o.payout === 'intl') note += ' Whop international local-bank payout fees vary by country and are not included.';
  document.getElementById('tr-note').textContent = note;
  if (typeof window.trackSaaSBillEvent === 'function') {{ window.trackSaaSBillEvent('result_rendered', {{ page: 'gumroad-whop-lemon-squeezy', price: o.price, sales: o.sales }}); }} else {{ (window.__saasbillEvents = window.__saasbillEvents || []).push({{event: 'result_rendered', page: 'gumroad-whop-lemon-squeezy', price: o.price, sales: o.sales, ts: Date.now()}}); }}
}}
['tr-price','tr-sales','tr-intl','tr-paypal','tr-discover','tr-dispute','tr-sub','tr-tax','tr-fx','tr-risk','tr-payout'].forEach(id => document.getElementById(id).addEventListener('input', updateTr));
updateTr();
</script>
"""

faqs = [
    ("How much does Gumroad take per sale in 2026?",
     f"As checked on {CHECKED}, Gumroad charges 10% + $0.50 on sales through your profile or direct links, plus credit card processing of 2.9% + $0.30, so a card sale costs 12.9% + $0.80. Sales through the Gumroad Discover marketplace cost a flat 30% including processing. Once paid sales reach $20,000 in a calendar month, new direct sales that month pay 5% + $0.50 (plus processing)."),
    ("What are Whop's fees for sellers?",
     "Whop charges 2.7% + $0.30 per successful domestic card transaction, plus 1.5% for international cards and 1% when currency conversion applies. Optional add-ons are 2% for managed tax, 0.5% for Billing and 0.8% for orchestration. Disputes cost $15 each, and a next-day ACH payout costs $2.50. Marketplace (Discover) sales carry 0% commission."),
    ("Does Lemon Squeezy really charge only 5% + 50¢?",
     "The base platform fee is 5% + 50¢, but Lemon Squeezy's docs add 1.5% for transactions outside the US, 1.5% for PayPal and 0.5% for subscription payments. Payouts to non-US bank accounts cost 1%, and each chargeback carries a $15 dispute fee."),
    ("Which is cheapest: Gumroad, Whop or Lemon Squeezy?",
     f"In our example ($29 product, 200 sales a month, 30% international, 10% PayPal), fees are ${f(g['total'])}/month on Gumroad, ${f(l['total'])} on Lemon Squeezy and ${f(w['total'])} on Whop with its 2% tax service (${f(E_NOTAX['whop']['total'])} without it). Whop is cheapest per transaction; Gumroad is the most expensive on direct sales."),
    ("Are Gumroad, Lemon Squeezy and Whop merchants of record?",
     "Gumroad has been merchant of record for all sales since January 1, 2025, and Lemon Squeezy is merchant of record for every sale; both include sales tax and VAT handling in their fee. Whop handles tax on Discover marketplace sales. For direct sales you choose 'Whop collects and remits tax' (US, EU and UK, 2%), 'Whop collects tax, I remit' (2%) or handling tax yourself."),
    ("Is Lemon Squeezy shutting down after the Stripe acquisition?",
     "No shutdown date has been announced. Stripe acquired Lemon Squeezy in 2024, and in a January 28, 2026 update Lemon Squeezy said its goal is to give users an easy way to migrate to Stripe Managed Payments, Stripe's merchant of record product, which adds 3.5% per transaction on top of standard Stripe processing fees."),
    ("How long do Gumroad and Whop hold payouts?",
     "Gumroad requires a $100 minimum balance and holds each sale at least 7 days on weekly, monthly and quarterly schedules; new accounts go through a 1–3 week review. Whop makes sale proceeds withdrawable in 1–4 business days but can place rolling or fixed reserves on new or high-risk accounts; its Seller Terms cap reserves at 180 days."),
]

extra = {"@type": "Dataset", "name": f"Gumroad, Whop & Lemon Squeezy seller fee data (verified {CHECKED_ISO})",
         "description": "Platform take rates, card processing, international/PayPal/subscription surcharges, tax handling, dispute fees, payout fees and payout holds.",
         "creator": {"@type": "Organization", "name": "SaaSBill Editorial"},
         "isBasedOn": [u for _, u in SOURCES], "license": "https://creativecommons.org/licenses/by/4.0/"}

if __name__ == "__main__":
    render_page(REL, TITLE, DESC, SLUG, body, faqs=faqs, extra_schema=extra, published_date=CHECKED_ISO)
    print(json.dumps({"example": E, "example_whop_no_tax": E_NOTAX["whop"]}, indent=1))
