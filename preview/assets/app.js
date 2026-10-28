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
  if (typeof MutationObserver === "function" && document.body) {
    var observer = new MutationObserver(function () { normalizeLayout(); });
    observer.observe(document.body, { childList: true, subtree: true });
  }
})();
