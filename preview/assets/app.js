/* QUOTE_PAY_PROFILE_START */
function quotePayProfile(id, gmvMo, txMo) {
  function payMoney(n) {
    var rounded = Math.round(n);
    var sign = rounded < 0 ? "-" : "";
    return sign + "$" + Math.abs(rounded).toLocaleString("en-US");
  }
  function disputeDrainMo(gmv, tx, feeEach) {
    return Math.round(gmv * 0.0065 * 0.8 + tx * 0.0065 * feeEach);
  }
  function gapLine(hidden, sticker) {
    var pct = sticker > 0 ? Math.round((hidden / sticker) * 100) : 0;
    return "+" + payMoney(hidden) + "/mo (+" + payMoney(hidden * 12) + "/yr, +" + pct + "% Hidden Cost Gap above the " + payMoney(sticker) + "/mo advertised sticker rate)";
  }
  var gmv = Math.max(0, Number(gmvMo) || 0);
  var tx = Math.max(0, Number(txMo) || 0);
  var intl = Math.round(gmv * 0.015 * 0.30);
  var heldReserve = Math.round(gmv * 0.25);
  var gmvK = Math.round(gmv / 1000);
  var txLabel = tx.toLocaleString("en-US");
  var assumptions = "Assumptions ($" + gmvK + "k/mo GMV, " + txLabel + " tx, 30% intl)";

  if (id === "whop-payments") {
    var b = Math.round(gmv * 0.027);
    var s = Math.round(tx * 0.30);
    var failover = Math.round(gmv * 0.008);
    var h = intl + failover;
    var sticker = b + s;
    var total = sticker + h;
    var without = total - failover;
    var line = gapLine(h, sticker);
    return {
      b: b, s: s, h: h, total: total, held: 0, sticker: sticker, without: without, failover: failover, intl: intl, unit: "/ mo", recovery: false,
      callTitleBase: "Sticker Price: Base rate",
      callSubBase: "2.7% base rate (" + payMoney(b) + "/mo)",
      callTitleSeats: "Sticker Price: Per-tx fees",
      callSubSeats: "$0.30 × " + txLabel + " tx (" + payMoney(s) + "/mo)",
      callTitleHidden: "Hidden Cost Gap",
      callSubHidden: "+1.5% Intl FX (" + payMoney(intl) + ") + optional 0.8% multi-PSP failover (" + payMoney(failover) + ") = " + payMoney(h) + "/mo",
      quote: "<strong>Estimated monthly processing fees:</strong> " + payMoney(total) + "/mo (" + payMoney(total * 12) + "/yr)<br/><strong>Potential funds temporarily held:</strong> $0/mo (multi-acquirer routing)",
      sub: assumptions + ". " + line + " " + payMoney(total) + "/mo total with multi-PSP failover, or " + payMoney(without) + "/mo without orchestration. $0 single-PSP reserve hold.",
      gapLine: line,
      tableBaseAmt: sticker,
      tableFeeSub: payMoney(b) + " base (2.7%) + " + payMoney(s) + " per-tx + " + payMoney(intl) + " intl + " + payMoney(failover) + " optional multi-PSP (" + payMoney(without) + "/mo without orchestration)",
      tableHeldPill: "$0 single-PSP hold exposure",
      tableHeldSub: "Multi-acquirer failover routing avoids single-processor freezes",
      disputeLine: "Optional 0.8% multi-PSP failover is " + payMoney(failover) + "/mo. International FX on 30% of GMV is " + payMoney(intl) + "/mo. Single-PSP reserve hold is $0.",
      disputeAmt: payMoney(h) + "/mo"
    };
  }

  if (id === "paddle-mor") {
    var pb = Math.round(gmv * 0.05);
    var ps = Math.round(tx * 0.50);
    var fx = Math.round(gmv * 0.009);
    var pdrain = disputeDrainMo(gmv, tx, 20);
    var ph = fx + pdrain;
    var psticker = pb + ps;
    var ptotal = psticker + ph;
    var pline = gapLine(ph, psticker);
    return {
      b: pb, s: ps, h: ph, total: ptotal, held: heldReserve, sticker: psticker, fx: fx, drain: pdrain, unit: "/ mo", recovery: false,
      callTitleBase: "Sticker Price: Base rate",
      callSubBase: "5.0% MoR base (" + payMoney(pb) + "/mo)",
      callTitleSeats: "Sticker Price: Per-tx fees",
      callSubSeats: "$0.50 × " + txLabel + " tx (" + payMoney(ps) + "/mo)",
      callTitleHidden: "Hidden Cost Gap",
      callSubHidden: "+FX conversion spread (" + payMoney(fx) + ") + 0.65% dispute drain (" + payMoney(pdrain) + "/mo unrecovered + $20 fees) = " + payMoney(ph) + "/mo",
      quote: "<strong>Estimated monthly processing fees:</strong> " + payMoney(ptotal) + "/mo (" + payMoney(ptotal * 12) + "/yr)<br/><strong>Potential funds temporarily held:</strong> " + payMoney(heldReserve) + "/mo (25% hold risk)",
      sub: assumptions + ". " + pline,
      gapLine: pline,
      disputeLine: "0.65% dispute rate. Unrecovered sales at a 20% manual win rate plus $20 fees = " + payMoney(pdrain) + "/mo.",
      disputeAmt: payMoney(pdrain) + "/mo",
      tableFeeSub: payMoney(psticker) + " sticker (5.0% + $0.50) + " + payMoney(ph) + " Hidden Cost Gap",
      tableHeldPill: payMoney(heldReserve) + " / mo temporarily held",
      tableHeldSub: "If 25% payout hold triggers on review (not a fee) · Non-exportable MoR card vault"
    };
  }

  if (id === "lemon-squeezy") {
    var lb = Math.round(gmv * 0.05);
    var ls = Math.round(tx * 0.50);
    var subFee = Math.round(gmv * 0.005);
    var ldrain = disputeDrainMo(gmv, tx, 15);
    var lh = subFee + intl + ldrain;
    var lsticker = lb + ls;
    var ltotal = lsticker + lh;
    var lline = gapLine(lh, lsticker);
    return {
      b: lb, s: ls, h: lh, total: ltotal, held: heldReserve, sticker: lsticker, subFee: subFee, intl: intl, drain: ldrain, unit: "/ mo", recovery: false,
      callTitleBase: "Sticker Price: Base rate",
      callSubBase: "5.0% MoR base (" + payMoney(lb) + "/mo)",
      callTitleSeats: "Sticker Price: Per-tx fees",
      callSubSeats: "$0.50 × " + txLabel + " tx (" + payMoney(ls) + "/mo)",
      callTitleHidden: "Hidden Cost Gap",
      callSubHidden: "+0.5% subscription fee (" + payMoney(subFee) + ") + 1.5% Intl (" + payMoney(intl) + ") + 0.65% dispute drain (" + payMoney(ldrain) + "/mo) = " + payMoney(lh) + "/mo",
      quote: "<strong>Estimated monthly processing fees:</strong> " + payMoney(ltotal) + "/mo (" + payMoney(ltotal * 12) + "/yr)<br/><strong>Potential funds temporarily held:</strong> " + payMoney(heldReserve) + "/mo (25% reserve)",
      sub: assumptions + ". " + lline,
      gapLine: lline,
      disputeLine: "0.65% dispute rate. Unrecovered sales at a 20% manual win rate plus $15 fees = " + payMoney(ldrain) + "/mo.",
      disputeAmt: payMoney(ldrain) + "/mo",
      tableFeeSub: payMoney(lsticker) + " sticker (5.0% + $0.50) + " + payMoney(lh) + " Hidden Cost Gap",
      tableHeldPill: payMoney(heldReserve) + " / mo temporarily held",
      tableHeldSub: "If 25% rolling reserve triggers during onboarding review (not a fee)"
    };
  }

  if (id === "chargeflow") {
    var disputed = Math.round(gmv * 12 * 0.0065);
    var recovered = Math.round(disputed * 0.65);
    var fee = Math.round(recovered * 0.25);
    var net = recovered - fee;
    var netMo = Math.round(net / 12);
    var cline = "+" + payMoney(net) + "/yr net recovered (" + payMoney(netMo) + "/mo net) on a 0.65% dispute rate";
    return {
      b: 0, s: 0, h: 0, total: 0, held: 0, sticker: 0, unit: "/ yr net", recovery: true,
      netYr: net, netMo: netMo, disputedYr: disputed, recoveredYr: recovered, feeYr: fee,
      bench: { disputed: disputed, recovered: recovered, fee: fee, net: net, netMo: netMo, yearly: gmv * 12 },
      callTitleBase: "Sticker Price: Base rate",
      callSubBase: "$0/mo base platform fee",
      callTitleSeats: "Sticker Price: Per-tx fees",
      callSubSeats: "$0 evidence prep",
      callTitleHidden: "Hidden Cost Gap",
      callSubHidden: "25% success fee (" + payMoney(fee) + "/yr) on " + payMoney(recovered) + " recovered. Net kept " + payMoney(net) + "/yr (" + payMoney(netMo) + "/mo).",
      quote: "<strong>Estimated monthly processing fees:</strong> $0/mo<br/><strong>Potential funds temporarily held:</strong> $0/mo (add-on dispute layer)",
      sub: assumptions + ". " + cline + ". Disputed sales " + payMoney(disputed) + "/yr. Gross recovered at a 65% planning win rate " + payMoney(recovered) + ". Success fee 25% " + payMoney(fee) + ". $0/mo base platform fee and $0 evidence prep.",
      gapLine: cline,
      disputeLine: "Disputed sales at 0.65% = " + payMoney(disputed) + "/yr. Gross recovered at 65% = " + payMoney(recovered) + ". Success fee 25% = " + payMoney(fee) + ". Net kept " + payMoney(net) + "/yr.",
      disputeAmt: "+" + payMoney(net) + "/yr",
      tableFeeSub: "$0/mo base · $0 evidence prep · 25% of " + payMoney(recovered) + " recovered",
      tableHeldPill: "+" + payMoney(net) + " / yr net recovered",
      tableHeldSub: "$0/mo platform fee · 65% is a planning benchmark, not a guaranteed win rate"
    };
  }

  var sb = Math.round(gmv * 0.029);
  var ss = Math.round(tx * 0.30);
  var billing = Math.round(gmv * 0.007);
  var sdrain = disputeDrainMo(gmv, tx, 15);
  var sh = billing + intl + sdrain;
  var ssticker = sb + ss;
  var stotal = ssticker + sh;
  var sline = gapLine(sh, ssticker);
  return {
    b: sb, s: ss, h: sh, total: stotal, held: heldReserve, sticker: ssticker, billing: billing, intl: intl, drain: sdrain, unit: "/ mo", recovery: false,
    callTitleBase: "Sticker Price: Base rate",
    callSubBase: "2.9% card rate (" + payMoney(sb) + "/mo)",
    callTitleSeats: "Sticker Price: Per-tx fees",
    callSubSeats: "$0.30 × " + txLabel + " tx (" + payMoney(ss) + "/mo)",
    callTitleHidden: "Hidden Cost Gap",
    callSubHidden: "+0.7% Billing (" + payMoney(billing) + ") + 1.5% Intl FX (" + payMoney(intl) + ") + 0.65% chargeback drain (" + payMoney(sdrain) + "/mo unrecovered disputes & $15 fees) = " + payMoney(sh) + "/mo",
    quote: "<strong>Estimated monthly processing fees:</strong> " + payMoney(stotal) + "/mo (" + payMoney(stotal * 12) + "/yr)<br/><strong>Potential funds temporarily held:</strong> " + payMoney(heldReserve) + "/mo (25% reserve)",
    sub: assumptions + ". " + sline,
    gapLine: sline,
    disputeLine: "0.65% dispute rate. Unrecovered sales at a 20% manual win rate plus $15 fees = " + payMoney(sdrain) + "/mo.",
    disputeAmt: payMoney(sdrain) + "/mo",
    tableFeeSub: payMoney(ssticker) + " sticker (2.9% + $0.30) + " + payMoney(sh) + " Hidden Cost Gap",
    tableHeldPill: payMoney(heldReserve) + " / mo temporarily held",
    tableHeldSub: "If 25% rolling reserve triggers (held 90–180 days, not a fee) · Portable card tokens"
  };
}
if (typeof window !== "undefined") window.quotePayProfile = quotePayProfile;
/* QUOTE_PAY_PROFILE_END */
(function () {
  document.addEventListener("toggle", function (event) {
    var drawer = event.target;
    if (!drawer || !drawer.classList || !drawer.classList.contains("math-drawer")) return;
    if (!drawer.open) return;
    document.querySelectorAll("details.math-drawer[open]").forEach(function (other) {
      if (other !== drawer) other.open = false;
    });
  }, true);

  document.addEventListener("click", function (event) {
    document.querySelectorAll("details.math-drawer[open]").forEach(function (drawer) {
      if (!drawer.contains(event.target)) drawer.open = false;
    });
  });

  document.addEventListener("keydown", function (event) {
    if (event.key !== "Escape") return;
    document.querySelectorAll("details.math-drawer[open]").forEach(function (drawer) {
      drawer.open = false;
    });
  });

  var layingOut = false;
  function normalizeLayout() {
    if (layingOut) return;
    layingOut = true;
    document.querySelectorAll(".wb-result-col").forEach(function (col) {
      var total = col.querySelector(".wb-big-total");
      var drawer = col.querySelector(".math-drawer");
      if (total && drawer && total.nextElementSibling !== drawer) total.insertAdjacentElement("afterend", drawer);
    });
    document.querySelectorAll(".summary-card").forEach(function (card) {
      var metric = card.querySelector(".summary-metric");
      var drawer = card.querySelector(".math-drawer");
      if (metric && drawer && metric.nextElementSibling !== drawer) metric.insertAdjacentElement("afterend", drawer);
    });
    layingOut = false;
  }

  window.calcChargeflowRecovery = function (gmvMonthly, disputeRate) {
    var rate = disputeRate == null ? 0.0065 : disputeRate;
    var disputed = Math.round(gmvMonthly * 12 * rate);
    var recovered = Math.round(disputed * 0.65);
    var fee = Math.round(recovered * 0.25);
    return { disputed: disputed, recovered: recovered, fee: fee, net: recovered - fee };
  };

  var CAT_CALCS = {
    payments: [
      ["./chargeback-fee-and-recovery-calculator/", "Stripe, Shopify &amp; Paddle Chargeback Cost Calculator", "Dispute fees, manual prep, and automated recovery."],
      ["./exit/stripe-shopify-paddle-frozen-funds-alternatives/", "Stripe, Shopify &amp; Paddle Frozen Funds &amp; Reserve Calculator", "25% rolling reserves, payout holds, and the chargeback rate that triggers a freeze."],
      ["./pricing/stripe-billing-0-7-percent-recurring-tax-calculator/", "Stripe Billing 0.7% Fee, Tax &amp; Chargeback Calculator", "Recurring revenue tax, Stripe Tax, and subscription chargebacks."]
    ],
    helpdesk: [
      ["./intercom-fin-cost-calculator/", "Intercom Fin AI Cost Calculator", "Year-1 price at $0.99 per resolution versus Freshdesk and Zendesk."],
      ["./zendesk-ai-cost-calculator/", "Zendesk AI Cost Calculator", "Suite seats plus the per-resolution add-on versus Freshdesk and Intercom."],
      ["./zendesk-vs-freshdesk-cost-comparison/", "Zendesk vs. Freshdesk Cost Comparison", "Year-1 pricing with AI resolutions side by side."]
    ],
    crm: [
      ["./pricing/hubspot-true-cost-and-onboarding-fees/", "HubSpot True Cost &amp; Onboarding", "What HubSpot costs in Year 1 once mandatory onboarding is included."],
      ["./compare/close-crm-vs-hubspot-sales-hub-5-to-20-reps/", "Close CRM vs. HubSpot Sales Hub", "True Year-1 cost for 5 to 20 reps, including HubSpot onboarding."],
      ["./pricing/gong-io-platform-fee-and-seat-minimum-calculator/", "Gong.io $5,000 Platform Fee &amp; Seat Calculator", "Platform fee plus per-seat licenses versus Close CRM."]
    ],
    compliance: [
      ["./compliance/hipaa-baa-and-soc2-pricing-tiers/", "HIPAA BAA &amp; SOC 2 Pricing Tiers", "Which plan signs a BAA, and what the CPA audit adds."],
      ["./compliance/google-workspace-vs-microsoft-365-hipaa-baa-tiers/", "Google Workspace vs. Microsoft 365 HIPAA BAA", "Minimum editions that sign a BAA, plus form intake rules."],
      ["./compare/typeform-vs-jotform-response-limit-and-hipaa-cost/", "Typeform vs. Jotform Response &amp; HIPAA Calculator", "Response caps and which plan signs a HIPAA BAA."]
    ],
    all: [
      ["./chargeback-fee-and-recovery-calculator/", "Stripe, Shopify &amp; Paddle Chargeback Cost Calculator", "Dispute fees, manual prep, and automated recovery."],
      ["./pricing/hubspot-true-cost-and-onboarding-fees/", "HubSpot True Cost &amp; Onboarding", "What HubSpot costs in Year 1 once mandatory onboarding is included."],
      ["./intercom-fin-cost-calculator/", "Intercom Fin AI Cost Calculator", "Year-1 price at $0.99 per resolution versus Freshdesk and Zendesk."]
    ]
  };

  var originalDirectory = null;
  function categoryKey(value) {
    var v = String(value || "").toLowerCase();
    if (v.indexOf("payment") !== -1) return "payments";
    if (v.indexOf("helpdesk") !== -1) return "helpdesk";
    if (v.indexOf("crm") !== -1) return "crm";
    if (v.indexOf("compliance") !== -1 || v.indexOf("hipaa") !== -1) return "compliance";
    return "all";
  }
  function renderActiveCatCalcs(key) {
    var mount = document.getElementById("active-cat-calcs");
    var title = document.getElementById("active-cat-calcs-title");
    if (!mount) return;
    var items = CAT_CALCS[key] || CAT_CALCS.all;
    if (title) title.textContent = "Dedicated Calculators in This Category";
    mount.innerHTML = items.map(function (item) {
      return '<div class="card" data-cat="' + key + '"><h3><a href="' + item[0] + '" data-track="internal-audit">' + item[1] + " &rarr;</a></h3><p>" + item[2] + "</p></div>";
    }).join("");
    var grid = document.querySelector("#all-calculators .card-grid");
    if (!grid) return;
    if (!originalDirectory) originalDirectory = Array.prototype.slice.call(grid.children);
    var cards = originalDirectory.slice();
    if (key !== "all") {
      cards.sort(function (a, b) {
        return (a.getAttribute("data-cat") === key ? 0 : 1) - (b.getAttribute("data-cat") === key ? 0 : 1);
      });
    }
    cards.forEach(function (card) { grid.appendChild(card); });
  }
  function syncCategorySurfaces() {
    var select = document.getElementById("cat-filter");
    var active = document.querySelector(".cat-tab.active");
    var value = (select && select.value) || (active && active.getAttribute("data-cat")) || "";
    renderActiveCatCalcs(categoryKey(value));
  }
  document.addEventListener("click", function (event) {
    if (event.target.closest && event.target.closest(".cat-tab")) setTimeout(syncCategorySurfaces, 0);
  });
  document.addEventListener("change", function (event) {
    if (event.target && event.target.id === "cat-filter") setTimeout(syncCategorySurfaces, 0);
  });

  normalizeLayout();
  syncCategorySurfaces();
  if (typeof renderDirectory === "function") renderDirectory();
  if (typeof MutationObserver === "function" && document.body) {
    var observer = new MutationObserver(function () { normalizeLayout(); });
    observer.observe(document.body, { childList: true, subtree: true });
  }
})();
