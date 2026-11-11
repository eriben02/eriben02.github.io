"""Intercom Fin to Freshdesk Year-1 migration calculator.

Sources checked 2026-11-04:
- https://www.intercom.com/pricing
- https://www.intercom.com/learning-center/intercom-pricing
- https://www.intercom.com/help/en/articles/8205718-fin-ai-agent-outcomes
- https://www.freshworks.com/freshdesk/pricing/
- https://support.freshdesk.com/support/solutions/articles/50000011515-manage-freddy-ai-add-ons
- Freshdesk monthly seat rates are a secondary source:
  https://superdupr.com/blog/freshdesk-pricing (19 Oct 2026).
- Migration quotes are third-party:
  https://www.getmacha.com/blog/best-freshdesk-migration-tools
  https://www.getmacha.com/blog/intercom-to-freshdesk-migration
- Fin on another helpdesk has a monthly minimum. Third-party pages cite 50
  outcomes. Intercom's pages checked here do not state the number, so the
  minimum stays unknown and is not applied:
  https://clankersupport.com/blog/intercom-fin-pricing
  https://aftersales.co/blog/intercom-pricing

Default example: 5 full seats, Intercom Essential annual ($29), 1,000 Fin
outcomes a month, Freshdesk Growth annual ($19), Copilot off, 10,000 records.
Intercom seats $1,740 + Fin $11,880 = $13,620.
Freddy: 12,000 sessions, 500 one-time free, 115 packs x $49 = $5,635.
Freshdesk seats $1,140 + Freddy $5,635 + migration $514 = $7,289.
Difference $6,331. Freshdesk is lower only because one Fin outcome is counted
as one Freddy email session. Those units are not the same.

No Freshworks affiliate link. The program is not approved.
"""
import math
import os
import shutil

from layout import BASE_DIR, PUBLIC_DIR, render_page, wrap_calculator_shell

TITLE = "Intercom to Freshdesk Year-1 – saasbill.io"
DESCRIPTION = (
    "Five Essential seats and 1,000 Fin outcomes a month cost $13,620 in Year 1. "
    "Freshdesk Growth plus a 10,000-record move is $7,289. Checked 4 Nov 2026."
)
H1 = "Migrate off Intercom Fin without losing ticket history"
REL = "exit/intercom-to-freshdesk-ticket-and-help-center-migration/index.html"
CANONICAL = "/exit/intercom-to-freshdesk-ticket-and-help-center-migration/"

IC_RATES = {
    "annual": {"essential": 29, "advanced": 85, "expert": 132},
    "monthly": {"essential": 39, "advanced": 99, "expert": 139},
}
FD_RATES = {
    "annual": {"growth": 19, "pro": 55, "enterprise": 89},
    "monthly": {"growth": 23, "pro": 66, "enterprise": 107},
}
UNIT_SENTENCE = (
    " This counts one Fin outcome as one Freddy email session. "
    "An outcome is charged once per conversation. "
    "A Freddy email session is a 72-hour window and is charged either way."
)


def calc(raw):
    """Year-1 cents. None means the figure is unknown and must not become 0."""
    agents = max(0, int(round(float(raw.get("agents") or 0))))
    outcomes = max(0, int(round(float(raw.get("outcomes") or 0))))
    records = max(0, int(round(float(raw.get("records") or 0))))
    billing = "monthly" if raw.get("billing") == "monthly" else "annual"
    ic_plan = raw.get("intercom") or "essential"
    fd_plan = raw.get("freshdesk") or "growth"
    copilot_on = bool(raw.get("copilot"))
    ic_rate = IC_RATES[billing].get(ic_plan)
    fd_rate = FD_RATES[billing].get(fd_plan)
    ic_seat = None if ic_rate is None else agents * ic_rate * 12 * 100
    fd_seat = None if fd_rate is None else agents * fd_rate * 12 * 100
    fin = outcomes * 99 * 12
    sessions = outcomes * 12
    free_left = 500
    if billing == "annual":
        packs = int(math.ceil(max(0, sessions - 500) / 100.0))
    else:
        packs = 0
        for _ in range(12):
            covered = min(free_left, outcomes)
            free_left -= covered
            month_bill = outcomes - covered
            packs += int(math.ceil(month_bill / 100.0))
    freddy = packs * 49 * 100
    if copilot_on and fd_plan in ("pro", "enterprise"):
        copilot = agents * 29 * 12 * 100
        copilot_state = "on"
    elif copilot_on:
        copilot = 0
        copilot_state = "not-on-growth"
    else:
        copilot = 0
        copilot_state = "off"
    if records == 0:
        migration = 0
    elif records == 1000:
        migration = 100 * 100
    elif records == 10000:
        migration = 514 * 100
    else:
        migration = None
    ic_year = None if ic_seat is None else ic_seat + fin
    fd_software = None if fd_seat is None else fd_seat + freddy + copilot
    fd_year = None if fd_software is None or migration is None else fd_software + migration
    if ic_year is None or fd_year is None:
        diff = None
        lower = None
    else:
        diff = ic_year - fd_year
        if diff > 0:
            lower = "freshdesk"
        elif diff < 0:
            lower = "intercom"
        else:
            lower = "same"
    return {
        "agents": agents,
        "outcomes": outcomes,
        "records": records,
        "billing": billing,
        "intercom": ic_plan,
        "freshdesk": fd_plan,
        "icRate": ic_rate,
        "fdRate": fd_rate,
        "sessions": sessions,
        "packs": packs,
        "icSeat": ic_seat,
        "fdSeat": fd_seat,
        "fin": fin,
        "freddy": freddy,
        "copilot": copilot,
        "copilotState": copilot_state,
        "migration": migration,
        "icYear": ic_year,
        "fdSoftware": fd_software,
        "fdYear": fd_year,
        "diff": diff,
        "lower": lower,
    }


def money(cents):
    if cents is None:
        return "unknown"
    neg = cents < 0
    value = abs(int(round(cents)))
    dollars, rem = divmod(value, 100)
    text = "${:,}".format(dollars)
    if rem:
        text += ".%02d" % rem
    return ("-" if neg else "") + text


def lower_sentence(result):
    extra = ""
    if result["copilotState"] == "not-on-growth":
        extra += " Freddy AI Copilot is not listed on Growth, so this total leaves it out."
    if result["billing"] == "monthly":
        extra += " Freshdesk monthly seat rates are a secondary source, checked 19 Oct 2026."
    if result["icYear"] is None or result["fdYear"] is None:
        return (
            "Intercom Year-1: %s. Freshdesk Year-1, including migration: %s. Difference: unknown.%s%s"
            % (money(result["icYear"]), money(result["fdYear"]), UNIT_SENTENCE, extra)
        )
    gap = money(abs(result["diff"]))
    if result["lower"] == "same":
        return "Same Year-1 cost: %s. Difference $0.%s%s" % (money(result["icYear"]), UNIT_SENTENCE, extra)
    if result["lower"] == "freshdesk":
        return (
            "Lower Year-1 cost: Freshdesk, %s. Intercom %s. Difference %s.%s%s"
            % (money(result["fdYear"]), money(result["icYear"]), gap, UNIT_SENTENCE, extra)
        )
    return (
        "Lower Year-1 cost: Intercom, %s. Freshdesk %s. Difference %s.%s%s"
        % (money(result["icYear"]), money(result["fdYear"]), gap, UNIT_SENTENCE, extra)
    )


DEFAULT = calc({
    "agents": 5,
    "outcomes": 1000,
    "records": 10000,
    "intercom": "essential",
    "freshdesk": "growth",
    "billing": "annual",
    "copilot": False,
})
DEFAULT_LINE = lower_sentence(DEFAULT)

BODY = r"""
<section class="hero">
  <h1>Migrate off Intercom Fin without losing ticket history</h1>
  <p class="lead">Intercom seats and Fin outcomes versus Freshdesk seats, Freddy sessions, and a one-time record migration quote. Those units are not the same: an outcome is charged once per conversation, and a Freddy email session is a 72-hour window charged either way.</p>
</section>

<div class="unified-inspector-tray">
<section class="calc-box editorial-workbench" aria-labelledby="im-heading">
  <h2 id="im-heading" class="sr-only-control">Intercom to Freshdesk Year-1 calculator</h2>
  <div class="workbench-grid">
    <div class="wb-col-controls">
      <div class="wb-col-title">Your move</div>
      <div class="wb-controls-stack">
        <div class="wb-control-item">
          <label class="wb-control-label" for="im-agents">Full seats <span class="val-pill" id="im-agents-val">5</span></label>
          <div class="wb-slider-row">
            <input type="range" id="im-agents" min="0" max="80" step="1" value="5" aria-label="Full seats" data-track="calculator-control" data-control="agents" />
          </div>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="im-outcomes">Fin outcomes per month <span class="val-pill" id="im-outcomes-val">1,000</span></label>
          <div class="wb-slider-row">
            <input type="range" id="im-outcomes" min="0" max="20000" step="50" value="1000" aria-label="Fin outcomes per month" data-track="calculator-control" data-control="outcomes" />
          </div>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="im-records">Records to migrate <span class="val-pill" id="im-records-val">10,000</span></label>
          <div class="wb-slider-row">
            <input type="range" id="im-records" min="0" max="50000" step="500" value="10000" aria-label="Records to migrate" data-track="calculator-control" data-control="records" />
          </div>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="im-intercom">Intercom plan</label>
          <select id="im-intercom" class="wb-tool-select" data-track="calculator-control" data-control="intercom-plan">
            <option value="essential" selected>Essential, $29 annual</option>
            <option value="advanced">Advanced, $85 annual</option>
            <option value="expert">Expert, $132 annual</option>
          </select>
        </div>
        <div class="wb-control-item">
          <label class="wb-control-label" for="im-freshdesk">Freshdesk plan</label>
          <select id="im-freshdesk" class="wb-tool-select" data-track="calculator-control" data-control="freshdesk-plan">
            <option value="growth" selected>Growth, $19 annual</option>
            <option value="pro">Pro, $55 annual</option>
            <option value="enterprise">Enterprise, $89 annual</option>
          </select>
        </div>
        <div class="wb-quiet-options">
          <div class="wb-quiet-field">
            <label for="im-billing">Billing</label>
            <select id="im-billing" data-track="calculator-control" data-control="billing">
              <option value="annual" selected>Annual</option>
              <option value="monthly">Monthly</option>
            </select>
          </div>
          <div class="wb-quiet-field">
            <label for="im-copilot">Freddy AI Copilot</label>
            <select id="im-copilot" data-track="calculator-control" data-control="copilot">
              <option value="no" selected>No</option>
              <option value="yes">Yes</option>
            </select>
          </div>
        </div>
        <p id="im-status" class="wb-budget-subnote">Billing is annual list price. Essential $19 on the Intercom pricing page is a new-customer promo and is not the baseline.</p>
      </div>
    </div>

    <div class="wb-col-chart">
      <div class="wb-col-title">Year-1 cost of staying or moving</div>
      <div id="im-vbar" class="wb-vbar-container" aria-live="polite">
        <div class="wb-vbar-row" id="im-row-ic" style="flex: 65 1 0px;">
          <div class="wb-vbar-block block-base"><span class="wb-block-amount" id="im-amt-ic">$13,620</span></div>
          <div class="wb-callout-item"><div class="wb-leader-line"></div><div class="wb-callout-text"><strong>Intercom Year-1</strong><span id="im-sub-ic">Essential, 5 full seats, Fin $11,880</span></div></div>
        </div>
        <div class="wb-vbar-row" id="im-row-fd" style="flex: 35 1 0px;">
          <div class="wb-vbar-block block-seats"><span class="wb-block-amount" id="im-amt-fd">$7,289</span></div>
          <div class="wb-callout-item"><div class="wb-leader-line"></div><div class="wb-callout-text"><strong>Freshdesk Year-1</strong><span id="im-sub-fd">Growth, Freddy $5,635, migration $514</span></div></div>
        </div>
      </div>
    </div>

    <div class="wb-result-col" id="im-result">
      <div class="wb-selected-product" id="im-product">Freshdesk Growth</div>
      <div class="wb-big-total"><span id="im-big">$7,289</span> <span class="wb-per-year">/ year</span></div>
      <details class="math-drawer" id="im-calc-details">
        <summary>Show calculation</summary>
        <div class="math-drawer-body" id="im-math">Intercom Essential, annual: 5 full seats x $29 x 12 = $1,740. Fin: 1,000 outcomes a month x 12 x $0.99 = $11,880. Intercom Year-1 $13,620. Freshdesk Growth, annual: 5 agents x $19 x 12 = $1,140. Freddy email sessions counted: 12,000. New-account allowance: 500 once. Packs billed: 115 x $49 = $5,635. Copilot off. Migration: 10,000 records, third-party basic-plan quote $514. Freshdesk Year-1 $7,289. Difference $6,331. Annual billing pools the year's sessions into one pack purchase, because the billing cycle is the year. The 500 free sessions are used once. One Fin outcome is counted as one Freddy email session.</div>
      </details>
      <p class="wb-budget-quote" id="im-quote">True Year-1 cost</p>
      <p class="wb-budget-subnote" id="im-sub">Intercom $13,620. Freshdesk $7,289. One Fin outcome is counted as one Freddy email session.</p>
      <div class="wb-best-option" id="im-best"><strong>Lower Year-1 cost:</strong> Freshdesk, $7,289. Intercom $13,620. Difference $6,331. This counts one Fin outcome as one Freddy email session. An outcome is charged once per conversation. A Freddy email session is a 72-hour window and is charged either way.</div>
      <div class="cta-stack">
        <a id="im-fd-link" class="btn-cta wb-primary-cta" href="https://www.freshworks.com/freshdesk/pricing/" target="_blank" rel="noopener" data-track="vendor-cta" data-vendor="freshdesk" data-cta-location="workbench">Freshdesk pricing</a>
      </div>
      <p class="summary-caveat">List prices: <a href="https://www.intercom.com/pricing" target="_blank" rel="noopener">Intercom pricing</a> and <a href="https://www.freshworks.com/freshdesk/pricing/" target="_blank" rel="noopener">Freshdesk pricing</a>.</p>
    </div>
  </div>
</section>
</div>

<div id="im-summary" class="summary-strip" aria-live="polite">
  <div class="summary-card result-card">
    <div class="summary-label">Intercom Year-1</div>
    <div class="summary-metric" id="im-sum-ic">$13,620</div>
    <div class="summary-scenario" id="im-sum-ic-note">Essential, 5 full seats</div>
  </div>
  <div class="summary-card result-card">
    <div class="summary-label">Freshdesk Year-1</div>
    <div class="summary-metric" id="im-sum-fd">$7,289</div>
    <div class="summary-scenario" id="im-sum-fd-note">Includes migration</div>
  </div>
  <div class="summary-card result-card">
    <div class="summary-label">Migration quote</div>
    <div class="summary-metric" id="im-sum-mig">$514</div>
    <div class="summary-scenario" id="im-sum-mig-note">10,000 records, third-party</div>
  </div>
  <div class="summary-card result-card">
    <div class="summary-label">Difference</div>
    <div class="summary-metric" id="im-sum-diff">$6,331</div>
    <div class="summary-scenario" id="im-sum-diff-note">Freshdesk lower</div>
  </div>
</div>

<p>Assumption: this page counts one Fin outcome as one Freddy email session. Intercom charges an outcome once per conversation, and only when Fin resolves it, hands off a procedure, or disqualifies the conversation. A Freshdesk email session is a 72-hour window from the first customer email, and Freshdesk charges that session whether or not Freddy resolves the issue. The counts match here only so the two Year-1 totals can sit on one page.</p>

<div class="table-wrap editorial-gap-table mobile-cards">
  <table>
    <caption>Year-1 totals in this calculator. A line marked unknown is not treated as $0.</caption>
    <thead>
      <tr>
        <th>Line</th>
        <th>Intercom</th>
        <th>Freshdesk</th>
      </tr>
    </thead>
    <tbody id="im-tbody">
      <tr><td data-label="Line">Seats</td><td data-label="Intercom">$1,740</td><td data-label="Freshdesk">$1,140</td></tr>
      <tr><td data-label="Line">Fin outcomes / Freddy sessions</td><td data-label="Intercom">$11,880</td><td data-label="Freshdesk">$5,635</td></tr>
      <tr><td data-label="Line">Copilot</td><td data-label="Intercom">Not included ($99/mo)</td><td data-label="Freshdesk">$0</td></tr>
      <tr><td data-label="Line">Migration</td><td data-label="Intercom">Not in the Intercom total</td><td data-label="Freshdesk">$514</td></tr>
      <tr><td data-label="Line">Total in this calculator</td><td data-label="Intercom">$13,620</td><td data-label="Freshdesk">$7,289</td></tr>
      <tr><td data-label="Line">Difference</td><td data-label="Intercom">Freshdesk lower by $6,331</td><td data-label="Freshdesk">Freshdesk lower by $6,331</td></tr>
      <tr><td data-label="Line">Fin qualification</td><td data-label="Intercom">unknown</td><td data-label="Freshdesk">Not in the Freshdesk total</td></tr>
      <tr><td data-label="Line">Fin on another helpdesk, monthly minimum</td><td data-label="Intercom">unknown</td><td data-label="Freshdesk">Not in this total</td></tr>
      <tr><td data-label="Line">Freddy day passes</td><td data-label="Intercom">Not in the Intercom total</td><td data-label="Freshdesk">unknown</td></tr>
      <tr><td data-label="Line">Proactive Support Plus</td><td data-label="Intercom">Not included ($99/mo)</td><td data-label="Freshdesk">Not in the Freshdesk total</td></tr>
    </tbody>
  </table>
</div>

<section>
  <h2>Prices used, and what stays unknown</h2>
  <div class="table-wrap editorial-gap-table mobile-cards">
    <table>
      <caption>Figures checked 4 Nov 2026. Monthly Freshdesk seats are a secondary source from 19 Oct 2026.</caption>
      <thead>
        <tr>
          <th>Item</th>
          <th>Published figure</th>
          <th>In this total</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td data-label="Item">Intercom Essential</td>
          <td data-label="Published figure">$29 per full seat per month on annual billing, or $39 on monthly billing. The pricing page also shows $19 for new customers.</td>
          <td data-label="In this total">$29 or $39, whichever billing you pick. The $19 promo is not the baseline.</td>
        </tr>
        <tr>
          <td data-label="Item">Intercom Advanced</td>
          <td data-label="Published figure">$85 annual, $99 monthly. Includes 20 Lite seats.</td>
          <td data-label="In this total">Full seats only. The included Lite seats are not an extra charge.</td>
        </tr>
        <tr>
          <td data-label="Item">Intercom Expert</td>
          <td data-label="Published figure">$132 annual, $139 monthly. Includes 50 Lite seats, plus SSO, HIPAA support, and SLAs.</td>
          <td data-label="In this total">Full seats only.</td>
        </tr>
        <tr>
          <td data-label="Item">Essential Lite seats</td>
          <td data-label="Published figure">Not stated on the pages checked.</td>
          <td data-label="In this total">unknown</td>
        </tr>
        <tr>
          <td data-label="Item">Fin outcome</td>
          <td data-label="Published figure">$0.99. One charge per conversation for a resolution, a procedure handoff, or a disqualification. A resolution includes an assumed resolution when the customer leaves. No charge when the customer asks for a human. Usage reminders and hard limits are available.</td>
          <td data-label="In this total">The monthly outcome count you enter, times 12, times $0.99.</td>
        </tr>
        <tr>
          <td data-label="Item">Fin qualification</td>
          <td data-label="Published figure">$9.99.</td>
          <td data-label="In this total">unknown. This page does not ask for a qualification count.</td>
        </tr>
        <tr>
          <td data-label="Item">Fin on another helpdesk</td>
          <td data-label="Published figure">$0.99 per outcome and no seats. A monthly minimum commitment applies. Third-party pages cite 50 outcomes. Intercom's pages checked here do not state the number.</td>
          <td data-label="In this total">unknown. The cited 50 is not added.</td>
        </tr>
        <tr>
          <td data-label="Item">Intercom Copilot Pro</td>
          <td data-label="Published figure">$99 per month.</td>
          <td data-label="In this total">Not included.</td>
        </tr>
        <tr>
          <td data-label="Item">Proactive Support Plus</td>
          <td data-label="Published figure">$99 per month.</td>
          <td data-label="In this total">Not included.</td>
        </tr>
        <tr>
          <td data-label="Item">Freshdesk seats, annual</td>
          <td data-label="Published figure">Growth $19, Pro $55, Enterprise $89 per agent per month.</td>
          <td data-label="In this total">The plan you select, when billing is annual.</td>
        </tr>
        <tr>
          <td data-label="Item">Freshdesk seats, monthly</td>
          <td data-label="Published figure">$23, $66, and $107. Secondary source, 19 Oct 2026. Not taken from the Freshworks pricing page.</td>
          <td data-label="In this total">Used only when billing is monthly.</td>
        </tr>
        <tr>
          <td data-label="Item">Freddy AI Agent</td>
          <td data-label="Published figure">500 sessions once per account for new customers, then $49 per 100 sessions. The 500 is not a monthly grant. Packs expire with the billing cycle. Auto-recharge exists, and the default threshold is 50 sessions.</td>
          <td data-label="In this total">The 500 is included, as a new-account move. Annual billing pools the year. Monthly billing buys a pack each month for that month's remainder.</td>
        </tr>
        <tr>
          <td data-label="Item">Freddy email session</td>
          <td data-label="Published figure">A 72-hour window from the first customer email. Charged whether or not the AI resolves the issue.</td>
          <td data-label="In this total">Counted one-for-one with the Fin outcomes you enter. That mapping is an assumption.</td>
        </tr>
        <tr>
          <td data-label="Item">Freddy chat</td>
          <td data-label="Published figure">Chat AI Agent is part of Freshdesk Omni, not Support Desk.</td>
          <td data-label="In this total">Not included. An Omni price is unknown.</td>
        </tr>
        <tr>
          <td data-label="Item">Freddy AI Copilot</td>
          <td data-label="Published figure">$29 per agent per month on Pro and Enterprise. A separate monthly-billing rate was not on the page checked. Day passes are listed at $2, $7, and $12.</td>
          <td data-label="In this total">$29 per agent when Copilot is on and the plan lists it. Growth does not list it. Day-pass dollars are unknown, because the count is not asked and the pages checked do not say which price belongs to which plan.</td>
        </tr>
        <tr>
          <td data-label="Item">Migration, 1,000 records</td>
          <td data-label="Published figure">About $100 on the Help Desk Migration basic plan. Third-party report. Quotes vary. Replies, notes, and attachments are not records.</td>
          <td data-label="In this total">$100 when the record count is 1,000.</td>
        </tr>
        <tr>
          <td data-label="Item">Migration, 10,000 records</td>
          <td data-label="Published figure">$514 on that same basic plan. Third-party report. Quotes vary.</td>
          <td data-label="In this total">$514 when the record count is 10,000.</td>
        </tr>
        <tr>
          <td data-label="Item">Migration, any other count</td>
          <td data-label="Published figure">No other quote was checked.</td>
          <td data-label="In this total">unknown. Zero records is $0, because the quote is empty. A record here is a conversation, contact, company, or article.</td>
        </tr>
      </tbody>
    </table>
  </div>
  <p class="summary-caveat">Checked 4 Nov 2026. <span class="src-cluster"><a class="src-link" href="https://www.intercom.com/pricing" target="_blank" rel="noopener">Intercom pricing</a> &middot; <a class="src-link" href="https://www.intercom.com/learning-center/intercom-pricing" target="_blank" rel="noopener">Intercom pricing guide</a> &middot; <a class="src-link" href="https://www.intercom.com/help/en/articles/8205718-fin-ai-agent-outcomes" target="_blank" rel="noopener">Fin AI Agent outcomes</a> &middot; <a class="src-link" href="https://www.freshworks.com/freshdesk/pricing/" target="_blank" rel="noopener">Freshdesk pricing</a> &middot; <a class="src-link" href="https://support.freshdesk.com/support/solutions/articles/50000011515-manage-freddy-ai-add-ons" target="_blank" rel="noopener">Freddy AI add-ons</a> <span class="src-date">Accessed 4 Nov 2026.</span></span></p>
  <p class="summary-caveat">Secondary and third-party notes. <span class="src-cluster"><a class="src-link" href="https://superdupr.com/blog/freshdesk-pricing" target="_blank" rel="noopener">Freshdesk monthly rates, superdupr.com</a> <span class="src-date">Accessed 19 Oct 2026.</span></span> <span class="src-cluster"><a class="src-link" href="https://www.getmacha.com/blog/best-freshdesk-migration-tools" target="_blank" rel="noopener">Help Desk Migration record prices</a> &middot; <a class="src-link" href="https://www.getmacha.com/blog/intercom-to-freshdesk-migration" target="_blank" rel="noopener">Intercom export limits</a> <span class="src-date">Accessed 4 Nov 2026.</span></span> <span class="src-cluster"><a class="src-link" href="https://clankersupport.com/blog/intercom-fin-pricing" target="_blank" rel="noopener">Fin minimum, third-party</a> &middot; <a class="src-link" href="https://aftersales.co/blog/intercom-pricing" target="_blank" rel="noopener">Fin minimum, second third-party page</a> <span class="src-date">Accessed 4 Nov 2026.</span></span></p>
</section>

<section>
  <h2>What moves, and what you rebuild</h2>
  <details class="full-table-disclosure below-disclosure">
    <summary class="full-table-summary">
      <span class="below-disclosure-title">Ticket history, the help center, and the pieces that stay behind</span>
      <span class="full-table-toggle-pill" aria-hidden="true">&darr;</span>
    </summary>
    <div class="full-table-body">
      <ul class="key-list">
        <li>Export Intercom history before the subscription ends. The in-product bulk export moves 200 to 300 conversations at a time. Internal notes are left out of transcript exports. A dataset export to S3 does not include transcripts, so a full history needs the Conversations API.</li>
        <li>Freshdesk's own importer takes contacts and companies from a CSV. It does not import tickets.</li>
        <li>Help Desk Migration prices per record on its basic plan. A free demo and a delta migration are available. The $100 and $514 figures are third-party reports, and quotes vary.</li>
        <li>Intercom collections and articles map to Freshdesk solution categories, folders, and articles, through a migration tool or the Freshdesk Solutions API.</li>
        <li>Automation rules, SLA policies, dashboards, and historical SLA metrics do not migrate. Rebuild them.</li>
        <li>Keeping Intercom and changing only the AI layer is a separate path. Fin on another helpdesk is $0.99 per outcome with no seats. The monthly minimum is unknown.</li>
      </ul>
    </div>
  </details>
</section>

<section>
  <h2>What teams described in June 2026</h2>
  <ul class="key-list">
    <li>Threads on r/intercom in June 2026 describe Fin bills that rose about threefold as volume rose. The same threads describe teams going through resolutions that were only article lookups before a renewal. These are reports from those threads, not a measured average. <span class="src-cluster"><a class="src-link" href="https://www.reddit.com/r/intercom/comments/1u9xxgm/has_anyone_genuinely_cut_their_fin_bill_in_half/" target="_blank" rel="noopener">Fin bill thread</a> &middot; <a class="src-link" href="https://www.reddit.com/r/intercom/comments/1trb4cg/fin_is_getting_expensive_and_i_want_to_know_what/" target="_blank" rel="noopener">Fin cost thread</a> <span class="src-date">Accessed 4 Nov 2026.</span></span></li>
    <li>Before you let the Intercom subscription lapse, export the history you still need. If the seat product is fine and only the outcome meter is the problem, Fin on the helpdesk you already use is the other path, and its monthly minimum is unknown.</li>
  </ul>
</section>
<script>
function calcIntercomFreshdesk(input) {
  var agents = Math.max(0, Math.round(Number(input.agents) || 0));
  var outcomes = Math.max(0, Math.round(Number(input.outcomes) || 0));
  var records = Math.max(0, Math.round(Number(input.records) || 0));
  var billing = input.billing === "monthly" ? "monthly" : "annual";
  var icPlan = input.intercom || "essential";
  var fdPlan = input.freshdesk || "growth";
  var copilotOn = !!input.copilot;
  var icTable = {
    annual: { essential: 29, advanced: 85, expert: 132 },
    monthly: { essential: 39, advanced: 99, expert: 139 }
  };
  var fdTable = {
    annual: { growth: 19, pro: 55, enterprise: 89 },
    monthly: { growth: 23, pro: 66, enterprise: 107 }
  };
  var icLookup = icTable[billing][icPlan];
  var fdLookup = fdTable[billing][fdPlan];
  var icKnown = typeof icLookup === "number";
  var fdKnown = typeof fdLookup === "number";
  var icRate = icKnown ? icLookup : null;
  var fdRate = fdKnown ? fdLookup : null;
  var icSeat = icKnown ? agents * icRate * 12 * 100 : null;
  var fdSeat = fdKnown ? agents * fdRate * 12 * 100 : null;
  var fin = outcomes * 99 * 12;
  var sessions = outcomes * 12;
  var packs = 0;
  var freeLeft = 500;
  if (billing === "annual") {
    packs = Math.ceil(Math.max(0, sessions - 500) / 100);
  } else {
    var month = 0;
    while (month < 12) {
      var covered = Math.min(freeLeft, outcomes);
      freeLeft -= covered;
      var monthBill = outcomes - covered;
      packs += Math.ceil(monthBill / 100);
      month += 1;
    }
  }
  var freddy = packs * 49 * 100;
  var copilotOk = fdPlan === "pro" || fdPlan === "enterprise";
  var copilot = 0;
  var copilotState = "off";
  if (copilotOn && copilotOk) {
    copilot = agents * 29 * 12 * 100;
    copilotState = "on";
  } else if (copilotOn) {
    copilotState = "not-on-growth";
  }
  var migration = null;
  if (records === 0) migration = 0;
  else if (records === 1000) migration = 10000;
  else if (records === 10000) migration = 51400;
  var icYear = icKnown ? icSeat + fin : null;
  var fdSoftware = fdKnown ? fdSeat + freddy + copilot : null;
  var fdYear = fdSoftware === null || migration === null ? null : fdSoftware + migration;
  var diff = icYear === null || fdYear === null ? null : icYear - fdYear;
  var lower = null;
  if (diff !== null) {
    if (diff > 0) lower = "freshdesk";
    else if (diff < 0) lower = "intercom";
    else lower = "same";
  }
  return {
    agents: agents,
    outcomes: outcomes,
    records: records,
    billing: billing,
    intercom: icPlan,
    freshdesk: fdPlan,
    icRate: icRate,
    fdRate: fdRate,
    sessions: sessions,
    packs: packs,
    icSeat: icSeat,
    fdSeat: fdSeat,
    fin: fin,
    freddy: freddy,
    copilot: copilot,
    copilotState: copilotState,
    migration: migration,
    icYear: icYear,
    fdSoftware: fdSoftware,
    fdYear: fdYear,
    diff: diff,
    lower: lower
  };
}

function imMoney(cents) {
  if (cents === null) return "unknown";
  var neg = cents < 0;
  var v = Math.abs(Math.round(cents));
  var dollars = Math.floor(v / 100);
  var rem = v % 100;
  var text = "$" + dollars.toLocaleString("en-US");
  if (rem) text += "." + (rem < 10 ? "0" : "") + rem;
  return neg ? "-" + text : text;
}

function imPlanName(kind, key) {
  if (kind === "intercom") {
    if (key === "advanced") return "Advanced";
    if (key === "expert") return "Expert";
    return "Essential";
  }
  if (key === "pro") return "Pro";
  if (key === "enterprise") return "Enterprise";
  return "Growth";
}

function imLowerSentence(c) {
  var unit = " This counts one Fin outcome as one Freddy email session. An outcome is charged once per conversation. A Freddy email session is a 72-hour window and is charged either way.";
  var extra = "";
  if (c.copilotState === "not-on-growth") extra += " Freddy AI Copilot is not listed on Growth, so this total leaves it out.";
  if (c.billing === "monthly") extra += " Freshdesk monthly seat rates are a secondary source, checked 19 Oct 2026.";
  if (c.icYear === null || c.fdYear === null) {
    return "Intercom Year-1: " + imMoney(c.icYear) + ". Freshdesk Year-1, including migration: " + imMoney(c.fdYear) + ". Difference: unknown." + unit + extra;
  }
  var gap = imMoney(Math.abs(c.diff));
  if (c.lower === "same") return "Same Year-1 cost: " + imMoney(c.icYear) + ". Difference $0." + unit + extra;
  if (c.lower === "freshdesk") return "Lower Year-1 cost: Freshdesk, " + imMoney(c.fdYear) + ". Intercom " + imMoney(c.icYear) + ". Difference " + gap + "." + unit + extra;
  return "Lower Year-1 cost: Intercom, " + imMoney(c.icYear) + ". Freshdesk " + imMoney(c.fdYear) + ". Difference " + gap + "." + unit + extra;
}

function imMathText(c) {
  var billName = c.billing === "monthly" ? "monthly" : "annual";
  var pool = c.billing === "monthly"
    ? "Monthly billing buys Freddy packs each month, because packs expire with the billing cycle. The 500 free sessions are used once, across the year."
    : "Annual billing pools the year's sessions into one pack purchase, because the billing cycle is the year. The 500 free sessions are used once.";
  var copilotLine = "Copilot off.";
  if (c.copilotState === "on") copilotLine = "Copilot on: " + c.agents + " agents x $29 x 12 = " + imMoney(c.copilot) + ".";
  if (c.copilotState === "not-on-growth") copilotLine = "Copilot was requested. It is not listed on Growth, so it is not in this total.";
  var icRateText = c.icRate === null ? "unknown" : imMoney(c.icRate * 100);
  var fdRateText = c.fdRate === null ? "unknown" : imMoney(c.fdRate * 100);
  var migrationText = imMoney(c.migration);
  if (c.migration !== null && c.migration > 0) migrationText = "third-party basic-plan quote " + migrationText;
  var gapText = c.diff === null ? "unknown" : imMoney(Math.abs(c.diff));
  return "Intercom " + imPlanName("intercom", c.intercom) + ", " + billName + ": " + c.agents + " full seats x " + icRateText + " x 12 = " + imMoney(c.icSeat) + ". Fin: " + c.outcomes.toLocaleString("en-US") + " outcomes a month x 12 x $0.99 = " + imMoney(c.fin) + ". Intercom Year-1 " + imMoney(c.icYear) + ". Freshdesk " + imPlanName("freshdesk", c.freshdesk) + ", " + billName + ": " + c.agents + " agents x " + fdRateText + " x 12 = " + imMoney(c.fdSeat) + ". Freddy email sessions counted: " + c.sessions.toLocaleString("en-US") + ". New-account allowance: 500 once. Packs billed: " + c.packs + " x $49 = " + imMoney(c.freddy) + ". " + copilotLine + " Migration: " + c.records.toLocaleString("en-US") + " records, " + migrationText + ". Freshdesk Year-1 " + imMoney(c.fdYear) + ". Difference " + gapText + ". " + pool + " One Fin outcome is counted as one Freddy email session.";
}

function imDiffCell(c) {
  if (c.diff === null) return "unknown";
  if (c.lower === "same") return "Same cost";
  if (c.lower === "freshdesk") return "Freshdesk lower by " + imMoney(c.diff);
  return "Intercom lower by " + imMoney(Math.abs(c.diff));
}

function imCopilotCell(c) {
  if (c.copilotState === "not-on-growth") return "Not on Growth";
  return imMoney(c.copilot);
}

function imRead() {
  return {
    agents: document.getElementById("im-agents").value,
    outcomes: document.getElementById("im-outcomes").value,
    records: document.getElementById("im-records").value,
    intercom: document.getElementById("im-intercom").value,
    freshdesk: document.getElementById("im-freshdesk").value,
    billing: document.getElementById("im-billing").value,
    copilot: document.getElementById("im-copilot").value === "yes"
  };
}

function renderIntercomFreshdesk() {
  var c = calcIntercomFreshdesk(imRead());
  document.getElementById("im-agents-val").textContent = c.agents.toLocaleString("en-US");
  document.getElementById("im-outcomes-val").textContent = c.outcomes.toLocaleString("en-US");
  document.getElementById("im-records-val").textContent = c.records.toLocaleString("en-US");
  var promo = "Essential $19 on the Intercom pricing page is a new-customer promo and is not the baseline.";
  document.getElementById("im-status").textContent = c.billing === "monthly"
    ? "Billing is monthly. Freshdesk monthly seat rates are a secondary source, checked 19 Oct 2026. " + promo
    : "Billing is annual list price. " + promo;
  var icBar = c.icYear === null ? 0 : c.icYear;
  var fdBar = c.fdYear === null ? 0 : c.fdYear;
  var barTotal = Math.max(1, icBar + fdBar);
  document.getElementById("im-row-ic").style.flex = Math.max(8, Math.round(icBar / barTotal * 100)) + " 1 0px";
  document.getElementById("im-row-fd").style.flex = Math.max(8, Math.round(fdBar / barTotal * 100)) + " 1 0px";
  document.getElementById("im-amt-ic").textContent = imMoney(c.icYear);
  document.getElementById("im-amt-fd").textContent = imMoney(c.fdYear);
  document.getElementById("im-sub-ic").textContent = imPlanName("intercom", c.intercom) + ", " + c.agents + " full seats, Fin " + imMoney(c.fin);
  document.getElementById("im-sub-fd").textContent = imPlanName("freshdesk", c.freshdesk) + ", Freddy " + imMoney(c.freddy) + ", migration " + imMoney(c.migration);
  var product = "Year-1 comparison";
  var big = "unknown";
  if (c.lower === "freshdesk") {
    product = "Freshdesk " + imPlanName("freshdesk", c.freshdesk);
    big = imMoney(c.fdYear);
  } else if (c.lower === "intercom") {
    product = "Intercom " + imPlanName("intercom", c.intercom);
    big = imMoney(c.icYear);
  } else if (c.lower === "same") {
    product = "Same Year-1 cost";
    big = imMoney(c.icYear);
  }
  document.getElementById("im-product").textContent = product;
  document.getElementById("im-big").textContent = big;
  document.getElementById("im-sub").textContent = "Intercom " + imMoney(c.icYear) + ". Freshdesk " + imMoney(c.fdYear) + ". One Fin outcome is counted as one Freddy email session.";
  var line = imLowerSentence(c);
  var best = document.getElementById("im-best");
  var lowerLabel = "Lower Year-1 cost:";
  var sameLabel = "Same Year-1 cost:";
  if (line.indexOf(lowerLabel) === 0) best.innerHTML = "<strong>" + lowerLabel + "</strong>" + line.slice(lowerLabel.length);
  else if (line.indexOf(sameLabel) === 0) best.innerHTML = "<strong>" + sameLabel + "</strong>" + line.slice(sameLabel.length);
  else best.textContent = line;
  document.getElementById("im-math").textContent = imMathText(c);
  document.getElementById("im-sum-ic").textContent = imMoney(c.icYear);
  document.getElementById("im-sum-ic-note").textContent = imPlanName("intercom", c.intercom) + ", " + c.agents + " full seats";
  document.getElementById("im-sum-fd").textContent = imMoney(c.fdYear);
  document.getElementById("im-sum-fd-note").textContent = c.fdYear === null ? "Migration quote missing" : "Includes migration";
  document.getElementById("im-sum-mig").textContent = imMoney(c.migration);
  document.getElementById("im-sum-mig-note").textContent = c.records.toLocaleString("en-US") + " records" + (c.migration === null ? ", no quote on file" : c.migration > 0 ? ", third-party" : "");
  var diffNote = "unknown";
  if (c.lower === "freshdesk") diffNote = "Freshdesk lower";
  if (c.lower === "intercom") diffNote = "Intercom lower";
  if (c.lower === "same") diffNote = "Same cost";
  document.getElementById("im-sum-diff").textContent = c.diff === null ? "unknown" : imMoney(Math.abs(c.diff));
  document.getElementById("im-sum-diff-note").textContent = diffNote;
  function row(label, ic, fd) {
    return "<tr><td data-label=\"Line\">" + label + "</td><td data-label=\"Intercom\">" + ic + "</td><td data-label=\"Freshdesk\">" + fd + "</td></tr>";
  }
  var diffCell = imDiffCell(c);
  document.getElementById("im-tbody").innerHTML = row("Seats", imMoney(c.icSeat), imMoney(c.fdSeat))
    + row("Fin outcomes / Freddy sessions", imMoney(c.fin), imMoney(c.freddy))
    + row("Copilot", "Not included ($99/mo)", imCopilotCell(c))
    + row("Migration", "Not in the Intercom total", imMoney(c.migration))
    + row("Total in this calculator", imMoney(c.icYear), imMoney(c.fdYear))
    + row("Difference", diffCell, diffCell)
    + row("Fin qualification", "unknown", "Not in the Freshdesk total")
    + row("Fin on another helpdesk, monthly minimum", "unknown", "Not in this total")
    + row("Freddy day passes", "Not in the Intercom total", "unknown")
    + row("Proactive Support Plus", "Not included ($99/mo)", "Not in the Freshdesk total");
  if (typeof window.trackSaaSBillEvent === "function") {
    window.trackSaaSBillEvent("result_rendered", { page: "intercom-freshdesk-migration", agents: c.agents, outcomes: c.outcomes, records: c.records });
  }
}
["im-agents", "im-outcomes", "im-records", "im-intercom", "im-freshdesk", "im-billing", "im-copilot"].forEach(function (id) {
  var el = document.getElementById(id);
  el.addEventListener("input", renderIntercomFreshdesk);
  el.addEventListener("change", renderIntercomFreshdesk);
});
renderIntercomFreshdesk();
</script>
"""

FAQS = [
    (
        "What does a Fin outcome cost in 2026?",
        "Intercom charges $0.99 for one outcome on a conversation. That covers a resolution, a procedure handoff, or a disqualification, and at most one charge per conversation. A resolution includes an assumed resolution when the customer leaves without asking for more help. Intercom does not charge when the customer asks for a human. Qualification is $9.99, and this calculator does not ask for that count, so qualification stays unknown. Checked 4 Nov 2026 on Intercom's pricing page and the Fin outcomes article.",
    ),
    (
        "Why is a Freddy session not the same as a Fin outcome?",
        "A Fin outcome is charged once per conversation, and only for a successful resolution, procedure handoff, or disqualification. A Freddy email session is a 72-hour window that starts at the first customer email, and Freshdesk charges the session whether or not the AI resolves the issue. This page counts one session for each outcome you enter so the Year-1 totals can be compared. That mapping is an assumption, not a vendor rule. Chat AI Agent sessions are a Freshdesk Omni feature, not Support Desk, and an Omni price is unknown here.",
    ),
    (
        "Will Freshdesk import my Intercom tickets?",
        "Freshdesk's own importer takes contacts and companies from a CSV. It does not import tickets. A third-party tool such as Help Desk Migration prices per record. Replies, notes, and attachments are not records. Reported basic-plan quotes are about $100 for 1,000 records and $514 for 10,000. Other counts are unknown here because quotes vary. Export the Intercom history before the subscription ends. The in-product bulk export moves 200 to 300 conversations at a time and leaves internal notes out of transcript exports. A dataset export to S3 does not include transcripts, so the full history needs the Conversations API.",
    ),
    (
        "What does not come across in the move?",
        "Automation rules, SLA policies, dashboards, and historical SLA metrics do not migrate. Rebuild them on Freshdesk. Intercom collections and articles map to Freshdesk solution categories, folders, and articles, through a migration tool or the Freshdesk Solutions API.",
    ),
    (
        "Can I keep Intercom and change only the AI?",
        "Yes. That path keeps the Intercom seats or drops them. Fin on another helpdesk, including Freshdesk, is $0.99 per outcome with no seats. A monthly minimum commitment applies. Third-party pages cite 50 outcomes. Intercom's own pages checked on 4 Nov 2026 do not state the number, so the minimum is unknown and is not added to these totals.",
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
    if DEFAULT["icYear"] != 1362000 or DEFAULT["fdYear"] != 728900 or DEFAULT["diff"] != 633100:
        raise SystemExit(
            "Default example drifted: %s %s %s" % (DEFAULT["icYear"], DEFAULT["fdYear"], DEFAULT["diff"])
        )
    if not DEFAULT_LINE.startswith("Lower Year-1 cost: Freshdesk, $7,289."):
        raise SystemExit(DEFAULT_LINE)
    blob = BODY + TITLE + DESCRIPTION
    for banned in ("\u2014", "&mdash;", "/go/fresh", "rel=\"sponsored\"", "SaaSTruth", "Best option", "Best choice"):
        if banned in blob:
            raise SystemExit("banned token in migration page: " + banned)
    render_page(
        REL,
        TITLE,
        DESCRIPTION,
        CANONICAL,
        wrap_calculator_shell(BODY),
        faqs=FAQS,
        published_date="2026-11-04",
        show_affiliate_note=True,
    )
    copy_to_root(REL)


if __name__ == "__main__":
    build()
