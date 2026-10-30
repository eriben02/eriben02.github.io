// Close vs Pipedrive Year-1 math and HTML renderers.
// Pure functions: the browser runs them on every input change, and
// scripts/build_close_vs_pipedrive.py runs them in Node to prerender the
// default scenario. CP_DATA is injected from data/crm_pricing.json.
// A null price means "unknown/unverified": the term becomes null and is
// never counted as $0. Totals with a null term are shown as ">= known part".

function calcCloseVsPipedrive(input) {
  var D = CP_DATA;
  input = input || {};
  function num(v, lo, hi) {
    var n = Math.round(Number(v));
    if (!isFinite(n)) n = lo;
    return Math.min(hi, Math.max(lo, n));
  }
  function cents(v) { return Math.round(v * 100) / 100; }
  function add(list) {
    var sum = 0;
    for (var i = 0; i < list.length; i++) {
      if (list[i] === null) return null;
      sum += list[i];
    }
    return cents(sum);
  }
  function known(list) {
    var sum = 0;
    for (var i = 0; i < list.length; i++) if (list[i] !== null) sum += list[i];
    return cents(sum);
  }
  var seats = num(input.users, 1, 50);
  var billing = input.billing === 'monthly' ? 'monthly' : 'annual';
  var calling = (input.calling === 'none' || input.calling === 'power') ? input.calling : 'click';
  var minutes = calling === 'none' ? 0 : num(input.minutes, 0, 3000);
  var email = !!input.email;
  var sequences = !!input.sequences;
  var leadcapture = !!input.leadcapture;
  var excludeDialer = !!input.excludeDialer;
  var unknown = [];
  function flag(key) { if (unknown.indexOf(key) === -1) unknown.push(key); }

  // Close: cheapest plan that covers the needs.
  var cPlan = (calling === 'power' || sequences) ? 'growth' : ((seats === 1 && !email) ? 'solo' : 'essentials');
  var cRate = D.close.plans[cPlan][billing];
  if (cRate === null) flag('close_' + billing);
  var cSeat = cRate === null ? null : cents(seats * cRate * 12);
  var cUsage = calling === 'none' ? 0 : cents(seats * minutes * 12 * D.close.callPerMin);
  var cNumbers = calling === 'none' ? 0 : cents(seats * D.numbersPerRep * D.close.numberPerMonth * 12);
  var close = {
    plan: cPlan, planLabel: D.close.plans[cPlan].label, rate: cRate,
    seat: cSeat, usage: cUsage, numbers: cNumbers,
    total: add([cSeat, cUsage, cNumbers]), floor: known([cSeat, cUsage, cNumbers])
  };

  // Pipedrive: base plan by needs, LeadBooster vs Premium, third-party dialer.
  function pdRate(plan) {
    var p = D.pipedrive.plans[plan];
    var v = p[billing];
    if (v === null) flag('pipedrive_' + billing);
    return v;
  }
  var base = (email || sequences) ? 'growth' : 'lite';
  var pPlan = base;
  var useLB = false;
  var premiumCompared = false;
  var lbMonthly = D.pipedrive.leadbooster[billing];
  if (leadcapture) {
    if (lbMonthly === null) flag('leadbooster_' + billing);
    var baseRate = pdRate(base);
    var premRate = pdRate('premium');
    if (baseRate !== null && premRate !== null && lbMonthly !== null) {
      premiumCompared = true;
      var withLB = seats * baseRate * 12 + lbMonthly * 12;
      var prem = seats * premRate * 12;
      if (prem < withLB) pPlan = 'premium'; else useLB = true;
    } else {
      useLB = true;
    }
  }
  var pRate = pdRate(pPlan);
  var pSeat = pRate === null ? null : cents(seats * pRate * 12);
  var pAddons = useLB ? (lbMonthly === null ? null : cents(lbMonthly * 12)) : 0;
  var tier = null, licenses = 0, extraNumbers = 0, dLicenses = 0, dNumbers = 0;
  if (calling !== 'none' && !excludeDialer) {
    var A = D.aircall;
    tier = calling === 'power' ? 'professional' : 'essentials';
    var acRate = A[tier][billing];
    if (acRate === null) flag('aircall_' + billing);
    licenses = Math.max(seats, A.minLicenses);
    extraNumbers = Math.max(seats * D.numbersPerRep - A.includedNumbers, 0);
    dLicenses = acRate === null ? null : cents(licenses * acRate * 12);
    dNumbers = cents(extraNumbers * A.extraNumber * 12);
  }
  var pDialer = tier === null ? 0 : (dLicenses === null ? null : cents(dLicenses + dNumbers));
  var pTerms = [pSeat, pAddons, dLicenses, dNumbers];
  var pipedrive = {
    plan: pPlan, planLabel: D.pipedrive.plans[pPlan].label, basePlan: base, rate: pRate,
    leadbooster: useLB, premiumCompared: premiumCompared,
    seat: pSeat, addons: pAddons, dialer: pDialer,
    dialerTier: tier, dialerLabel: tier ? D.aircall[tier].label : '',
    licenses: licenses, extraNumbers: extraNumbers,
    dialerLicenses: dLicenses, dialerNumbers: dNumbers,
    excludeDialer: excludeDialer && calling !== 'none',
    total: add(pTerms), floor: known(pTerms)
  };
  if (leadcapture && premiumCompared) {
    var altPlan = pPlan === 'premium' ? base : 'premium';
    var altSeat = seats * D.pipedrive.plans[altPlan][billing] * 12;
    pipedrive.altPlan = altPlan;
    pipedrive.altTotal = cents(altSeat + (altPlan === 'premium' ? 0 : lbMonthly * 12) + (pDialer || 0));
  }

  var lowest = null;
  var difference = null;
  if (close.total !== null && pipedrive.total !== null) {
    lowest = close.total < pipedrive.total ? 'close' : (pipedrive.total < close.total ? 'pipedrive' : 'tie');
    difference = cents(Math.abs(close.total - pipedrive.total));
  } else if (close.total !== null && close.total < pipedrive.floor) {
    lowest = 'close';
  } else if (pipedrive.total !== null && pipedrive.total < close.floor) {
    lowest = 'pipedrive';
  }
  return {
    seats: seats, billing: billing, calling: calling, minutes: minutes,
    email: email, sequences: sequences, leadcapture: leadcapture, excludeDialer: excludeDialer,
    close: close, pipedrive: pipedrive, unknown: unknown, lowest: lowest, difference: difference
  };
}

function cpMoney(n) {
  var v = Math.round(Number(n) || 0);
  return '$' + v.toLocaleString('en-US');
}
function cpUnit(n) {
  return Number(n) % 1 === 0 ? '$' + Number(n).toLocaleString('en-US') : '$' + Number(n).toFixed(2);
}
function cpPill(text) {
  return ' <span class="status-pill status-unknown">' + (text || 'unverified') + '</span>';
}
function cpTotal(total, floor) {
  return total === null ? '&ge; ' + cpMoney(floor) + cpPill('unverified') : cpMoney(total);
}
function cpPart(v) {
  return v === null ? 'unknown' + cpPill('unverified') : cpMoney(v);
}
function cpName(r, v) {
  if (v === 'close') return 'Close ' + r.close.planLabel;
  var p = r.pipedrive;
  var s = 'Pipedrive ' + p.planLabel;
  if (p.leadbooster) s += ' + LeadBooster';
  if (p.dialerTier) s += ' + Aircall ' + p.dialerLabel;
  return s;
}
function cpScenario(r) {
  var needs = [];
  if (r.email) needs.push('email tracking');
  if (r.sequences) needs.push('sequences');
  if (r.leadcapture) needs.push('lead capture');
  var callText = r.calling === 'none' ? 'no calling' : (r.calling === 'power' ? 'power dialer' : 'click-to-call');
  var s = r.seats + (r.seats === 1 ? ' rep' : ' reps') + ' &middot; ' + r.billing + ' billing &middot; ' +
    (needs.length ? needs.join(', ') : 'no extra needs') + ' &middot; ' + callText;
  if (r.calling !== 'none') {
    s += ' &middot; ' + r.minutes.toLocaleString('en-US') + ' billed min/rep/mo';
    if (r.minutes === CP_DATA.defaultMinutes) s += ' (example assumption)';
  }
  return s;
}
function cpLowestLine(r) {
  if (r.lowest === 'tie') return 'Same Year-1 cost on both: <strong>' + cpMoney(r.close.total) + '</strong>';
  if (r.lowest === null) return 'Lowest Year-1 cost: <strong>not determined</strong> (some prices are unverified)';
  var other = r.lowest === 'close' ? 'Pipedrive' : 'Close';
  var vendor = r.lowest === 'close' ? 'Close' : 'Pipedrive';
  if (r.difference === null) return 'Lowest Year-1 cost: <strong>' + vendor + '</strong>';
  return 'Lowest Year-1 cost: <strong>' + vendor + '</strong>, ' + cpMoney(r.difference) + '/yr less than ' + other;
}
function cpMathRows(r, which) {
  var c = r.close, p = r.pipedrive, out = [];
  function row(label, formula, val) {
    out.push('<div class="calc-math-row"><span class="calc-math-label"><strong>' + label + '</strong><span class="calc-math-formula">' + formula + '</span></span><span class="calc-math-val">' + val + '</span></div>');
  }
  if (which !== 'pipedrive') {
    row('Close ' + c.planLabel + ' seats', r.seats + ' &times; ' + (c.rate === null ? 'unknown' : cpUnit(c.rate)) + ' &times; 12', cpPart(c.seat));
    if (r.calling !== 'none') {
      row('Close call minutes', r.seats + ' &times; ' + r.minutes.toLocaleString('en-US') + ' min &times; 12 &times; ' + cpUnit(CP_DATA.close.callPerMin) + ' (approx.)', cpMoney(c.usage));
      row('Close phone numbers', r.seats + ' &times; ' + cpUnit(CP_DATA.close.numberPerMonth) + ' &times; 12 (from)', cpMoney(c.numbers));
    }
    row('Close Year-1 total', 'seats + minutes + numbers', cpTotal(c.total, c.floor));
  }
  if (which !== 'close') {
    row('Pipedrive ' + p.planLabel + ' seats', r.seats + ' &times; ' + (p.rate === null ? 'unverified' : cpUnit(p.rate)) + ' &times; 12', cpPart(p.seat));
    if (p.leadbooster) row('LeadBooster', (CP_DATA.pipedrive.leadbooster[r.billing] === null ? 'unknown' : cpUnit(CP_DATA.pipedrive.leadbooster[r.billing])) + ' per company &times; 12', cpPart(p.addons));
    if (p.dialerTier) {
      var ac = CP_DATA.aircall[p.dialerTier][r.billing];
      row('Aircall ' + p.dialerLabel + ' licenses', p.licenses + ' (min ' + CP_DATA.aircall.minLicenses + ') &times; ' + (ac === null ? 'unknown' : cpUnit(ac)) + ' &times; 12', cpPart(p.dialerLicenses));
      row('Aircall extra numbers', p.extraNumbers + ' &times; ' + cpUnit(CP_DATA.aircall.extraNumber) + ' &times; 12', cpMoney(p.dialerNumbers));
    } else if (p.excludeDialer) {
      row('Dialer', 'excluded (you already pay for one)', '$0');
    }
    row('Pipedrive Year-1 total', 'seats + add-ons + dialer', cpTotal(p.total, p.floor));
  }
  return '<div class="calc-math-list">' + out.join('') + '</div>';
}
function cpAnswerHtml(r) {
  return '<p class="cp-answer-lowest">' + cpLowestLine(r) + '</p>' +
    '<ul class="cp-answer-rows">' +
    '<li><span>' + cpName(r, 'close') + '</span><strong>' + cpTotal(r.close.total, r.close.floor) + '</strong></li>' +
    '<li><span>' + cpName(r, 'pipedrive') + '</span><strong>' + cpTotal(r.pipedrive.total, r.pipedrive.floor) + '</strong></li>' +
    '</ul>' +
    '<p class="cp-answer-scenario">' + cpScenario(r) + '</p>' +
    '<details class="math-drawer"><summary>Show calculation</summary><div class="math-drawer-body">' + cpMathRows(r, 'both') + '</div></details>';
}
function cpWhy(r, v) {
  if (v === 'close') {
    var plan = r.close.plan;
    if (plan === 'growth') return r.calling === 'power' ? 'Power dialer is Growth and up' : 'Workflows are Growth and up';
    if (plan === 'solo') return '1 user, no open tracking needed';
    return r.email ? 'Email open tracking is Essentials and up' : 'Solo is limited to 1 user';
  }
  var p = r.pipedrive;
  var why = r.sequences ? 'Sequences are Growth and up' : (r.email ? 'Email sync with tracking is Growth and up' : 'Lowest plan covers your needs');
  if (p.plan === 'premium') why = 'Premium includes LeadBooster and costs less than ' + (p.basePlan === 'growth' ? 'Growth' : 'Lite') + ' + LeadBooster here';
  else if (p.leadbooster) why += '; LeadBooster for lead capture';
  return why;
}
function cpSourceCell(url, label, verified, pill) {
  return '<a href="' + url + '" target="_blank" rel="noopener">' + label + ' &nearr;</a><div class="cp-verified">Verified ' + verified + (pill ? cpPill(pill) : '') + '</div>';
}
function cpTableHtml(r) {
  var c = r.close, p = r.pipedrive, D = CP_DATA;
  var perC = c.total === null ? '&ge; ' + cpMoney(c.floor / r.seats / 12) : cpMoney(c.total / r.seats / 12);
  var perP = p.total === null ? '&ge; ' + cpMoney(p.floor / r.seats / 12) + cpPill('unverified') : cpMoney(p.total / r.seats / 12);
  var cCall = r.calling === 'none' ? 'No calling' : 'Built in: ' + cpMoney(c.usage) + ' minutes + ' + cpMoney(c.numbers) + ' numbers';
  var pCall = r.calling === 'none' ? 'No calling' : (p.excludeDialer ? 'Dialer excluded ($0)' :
    'Aircall ' + p.dialerLabel + ': ' + cpPart(p.dialerLicenses) + ' (' + p.licenses + ' licenses) + ' + cpMoney(p.dialerNumbers) + ' (' + p.extraNumbers + ' extra numbers)');
  var pAdd = p.plan === 'premium' && r.leadcapture ? 'LeadBooster included' : (p.leadbooster ? 'LeadBooster ' + cpPart(p.addons) : '$0');
  var pRate = p.rate === null ? 'unverified' + cpPill('unverified') : cpUnit(p.rate) + '/seat/mo';
  var pPill = r.billing === 'monthly' && !D.allowSecondary ? 'monthly unverified' : '';
  return '' +
    '<tr><td data-label="Vendor"><strong>Close</strong></td>' +
    '<td data-label="Plan chosen">' + c.planLabel + ' &middot; ' + (c.rate === null ? 'unknown' : cpUnit(c.rate) + '/seat/mo') + '</td>' +
    '<td data-label="Why">' + cpWhy(r, 'close') + '</td>' +
    '<td data-label="Seats">' + r.seats + '</td>' +
    '<td data-label="Add-ons">$0</td>' +
    '<td data-label="Calling / dialer">' + cCall + '</td>' +
    '<td data-label="Year-1 total"><strong>' + cpTotal(c.total, c.floor) + '</strong></td>' +
    '<td data-label="Per rep / month">' + perC + '</td>' +
    '<td data-label="Source">' + cpSourceCell(D.close.sourceUrl, 'close.com/pricing', D.close.verified, '') + '</td>' +
    '<td data-label="Try it"><a class="btn-secondary" href="/go/close" target="_blank" rel="sponsored nofollow noopener" data-track="vendor-cta" data-vendor="close-crm" data-cta-location="comparison-table">' + D.close.ctaLabel + ' &rarr;</a></td></tr>' +
    '<tr><td data-label="Vendor"><strong>Pipedrive</strong></td>' +
    '<td data-label="Plan chosen">' + p.planLabel + ' &middot; ' + pRate + '</td>' +
    '<td data-label="Why">' + cpWhy(r, 'pipedrive') + '</td>' +
    '<td data-label="Seats">' + r.seats + '</td>' +
    '<td data-label="Add-ons">' + pAdd + '</td>' +
    '<td data-label="Calling / dialer">' + pCall + '</td>' +
    '<td data-label="Year-1 total"><strong>' + cpTotal(p.total, p.floor) + '</strong></td>' +
    '<td data-label="Per rep / month">' + perP + '</td>' +
    '<td data-label="Source">' + cpSourceCell(D.pipedrive.sourceUrl, 'pipedrive.com/pricing', D.pipedrive.verified, pPill) + '</td>' +
    '<td data-label="Try it"><a class="btn-secondary" href="/go/pipedrive" target="_blank" rel="sponsored nofollow noopener" data-track="vendor-cta" data-vendor="pipedrive-crm" data-cta-location="comparison-table">' + D.pipedrive.ctaLabel + ' &rarr;</a></td></tr>';
}
