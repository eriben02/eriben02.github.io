// Pipedrive Year-1 math, shared by the Pipedrive calculator and the
// Pipedrive vs HubSpot comparison. PY_DATA is injected from
// data/crm_pricing.json plus HubSpot fields already published on this site.
// A null amount is unknown. It is never stored or displayed as $0.
// Unknown add-on price bases contribute only a floor (the published
// "from" price times 12). A lowest option is named only when one exact
// total is strictly below every other option's floor.

function pyCents(v) { return Math.round(Number(v) * 100) / 100; }

function pyAddonLine(data, id, planKey, on) {
  var a = data.pipedrive.addons[id];
  var base = { id: id, label: a.label, on: !!on, included: false, unknown: false, amount: 0, floor: 0, basis: a.per || '' };
  if (!on) return base;
  var included = (a.includedIn || []).indexOf(planKey) !== -1;
  if (included) {
    base.included = true;
    base.amount = 0;
    base.floor = 0;
    base.basis = 'included';
    return base;
  }
  if (a.per === 'company' && a.annual !== null && a.annual !== undefined) {
    var company = pyCents(a.annual * 12);
    base.amount = company;
    base.floor = company;
    base.basis = 'company';
    return base;
  }
  if (a.from !== null && a.from !== undefined) {
    base.amount = null;
    base.floor = pyCents(a.from * 12);
    base.unknown = true;
    base.basis = 'unknown';
    return base;
  }
  base.amount = null;
  base.floor = null;
  base.unknown = true;
  base.basis = 'unknown';
  return base;
}

function pyOnePlan(data, seats, planKey, selected) {
  var plan = data.pipedrive.plans[planKey];
  var rate = plan.annual;
  var seat = rate === null || rate === undefined ? null : pyCents(seats * rate * 12);
  var ids = data.pipedrive.addonOrder;
  var lines = [];
  for (var i = 0; i < ids.length; i++) lines.push(pyAddonLine(data, ids[i], planKey, !!(selected && selected[ids[i]])));
  var unknown = false;
  var unpriced = false;
  var exact = seat;
  var floor = seat;
  if (seat === null) { unknown = true; unpriced = true; }
  for (var j = 0; j < lines.length; j++) {
    var line = lines[j];
    if (!line.on) continue;
    if (line.unknown) {
      unknown = true;
      if (line.floor === null) unpriced = true;
      else if (floor !== null) floor = pyCents(floor + line.floor);
    } else if (exact !== null) {
      exact = pyCents(exact + line.amount);
      floor = pyCents(floor + line.amount);
    }
  }
  return {
    seats: seats,
    plan: planKey,
    planLabel: plan.label,
    rate: rate,
    seat: seat,
    lines: lines,
    total: (unknown || unpriced) ? null : exact,
    floor: unpriced ? null : floor,
    unknown: unknown
  };
}

function pyLowest(rows) {
  var winners = [];
  for (var i = 0; i < rows.length; i++) {
    var row = rows[i];
    if (row.total === null) continue;
    var beats = true;
    for (var j = 0; j < rows.length; j++) {
      if (i === j) continue;
      var other = rows[j].total === null ? rows[j].floor : rows[j].total;
      if (other === null || !(row.total < other)) beats = false;
    }
    if (beats) winners.push(row);
  }
  if (winners.length === 1) return { id: winners[0].id, total: winners[0].total, tie: false };
  if (winners.length > 1) return { id: null, total: winners[0].total, tie: true };
  return null;
}

function calcPipedriveYear1(input) {
  var D = PY_DATA;
  input = input || {};
  var seats = Math.round(Number(input.seats));
  if (!isFinite(seats)) seats = 5;
  seats = Math.min(50, Math.max(1, seats));
  var plan = D.pipedrive.plans[input.plan] ? input.plan : 'growth';
  var selected = input.addons || {};
  var keys = Object.keys(D.pipedrive.plans);
  var rows = [];
  for (var i = 0; i < keys.length; i++) {
    var one = pyOnePlan(D, seats, keys[i], selected);
    one.id = keys[i];
    rows.push(one);
  }
  var current = null;
  for (var k = 0; k < rows.length; k++) if (rows[k].id === plan) current = rows[k];
  return { seats: seats, plan: plan, billing: 'annual', rows: rows, current: current, lowest: pyLowest(rows) };
}

function calcHubspotYear1(input) {
  var D = PY_DATA;
  input = input || {};
  var seats = Math.round(Number(input.seats));
  if (!isFinite(seats)) seats = 5;
  seats = Math.min(50, Math.max(1, seats));
  var tier = D.hubspot.plans[input.tier] ? input.tier : 'professional';
  var p = D.hubspot.plans[tier];
  var seat = pyCents(seats * p.annual * 12);
  var onboarding = p.onboarding;
  return {
    seats: seats,
    tier: tier,
    planLabel: p.label,
    rate: p.annual,
    seat: seat,
    onboarding: onboarding,
    total: pyCents(seat + onboarding),
    floor: pyCents(seat + onboarding)
  };
}

function calcPipedriveVsHubspot(input) {
  input = input || {};
  var pd = calcPipedriveYear1(input);
  var hs = calcHubspotYear1({ seats: pd.seats, tier: input.tier });
  var current = pd.current;
  var lowest = null;
  var difference = null;
  if (current.total !== null) {
    if (current.total < hs.total) lowest = 'pipedrive';
    else if (hs.total < current.total) lowest = 'hubspot';
    else lowest = 'tie';
    difference = pyCents(Math.abs(current.total - hs.total));
  } else if (current.floor !== null && hs.total < current.floor) {
    lowest = 'hubspot';
    difference = null;
  }
  return { seats: pd.seats, billing: 'annual', pipedrive: current, plans: pd.rows, hubspot: hs, lowest: lowest, difference: difference };
}

function pyMoney(n) {
  var v = Math.round(Number(n) || 0);
  return '$' + v.toLocaleString('en-US');
}
function pyUnit(n) {
  return Number(n) % 1 === 0 ? '$' + Number(n).toLocaleString('en-US') : '$' + Number(n).toFixed(2);
}
function pyPill() {
  return ' <span class="status-pill status-unknown">unverified</span>';
}
function pyTotal(row) {
  if (!row) return '';
  if (row.total === null) {
    return row.floor === null ? 'unknown' + pyPill() : '&ge; ' + pyMoney(row.floor) + pyPill();
  }
  return pyMoney(row.total);
}
function pyAddonPhrase(line) {
  if (!line.on) return '';
  if (line.included) return line.label + ' included';
  if (line.basis === 'company') return line.label + ' ' + pyMoney(line.amount) + ' (per company)';
  if (line.unknown) return line.label + ' at least ' + (line.floor === null ? 'unknown' : pyMoney(line.floor)) + ' (price basis unpublished)';
  return line.label + ' ' + pyMoney(line.amount);
}
function pyMathRows(row) {
  var out = [];
  function add(label, formula, val) {
    out.push('<div class="calc-math-row"><span class="calc-math-label"><strong>' + label + '</strong><span class="calc-math-formula">' + formula + '</span></span><span class="calc-math-val">' + val + '</span></div>');
  }
  add('Pipedrive ' + row.planLabel + ' seats', row.rate === null ? 'unverified rate' : (row.seats + ' &times; ' + pyUnit(row.rate) + ' &times; 12'), row.seat === null ? 'unknown' + pyPill() : pyMoney(row.seat));
  var lines = row.lines || [];
  for (var i = 0; i < lines.length; i++) {
    var line = lines[i];
    if (!line.on) continue;
    if (line.included) add(line.label, 'Included in ' + row.planLabel + '. Not an extra charge.', 'Included');
    else if (line.basis === 'company') add(line.label, pyUnit(PY_DATA.pipedrive.addons[line.id].annual) + ' per company &times; 12', pyMoney(line.amount));
    else add(line.label, 'Published from-price &times; 12. Per seat or per company is not stated, so this is a floor, not a total.', line.floor === null ? 'unknown' + pyPill() : '&ge; ' + pyMoney(line.floor) + pyPill());
  }
  add('Year-1 cost', row.unknown ? 'At least the known seats plus published starting add-on prices' : 'Seats + add-ons', pyTotal(row));
  return '<div class="calc-math-list">' + out.join('') + '</div>';
}
function pyHsMath(hs) {
  return '<div class="calc-math-list">' +
    '<div class="calc-math-row"><span class="calc-math-label"><strong>' + hs.planLabel + ' seats</strong><span class="calc-math-formula">' + hs.seats + ' &times; ' + pyUnit(hs.rate) + ' &times; 12</span></span><span class="calc-math-val">' + pyMoney(hs.seat) + '</span></div>' +
    '<div class="calc-math-row"><span class="calc-math-label"><strong>Onboarding</strong><span class="calc-math-formula">One-time, Year 1</span></span><span class="calc-math-val">' + pyMoney(hs.onboarding) + '</span></div>' +
    '<div class="calc-math-row"><span class="calc-math-label"><strong>Year-1 cost</strong><span class="calc-math-formula">Seats + onboarding. Calling credits are not in this total.</span></span><span class="calc-math-val">' + pyMoney(hs.total) + '</span></div>' +
    '</div>';
}
function pyCta(location) {
  return '<a class="btn-secondary" href="/go/pipedrive" target="_blank" rel="sponsored nofollow noopener" data-track="vendor-cta" data-vendor="pipedrive-crm" data-cta-location="' + location + '">' + PY_DATA.pipedrive.ctaLabel + ' &rarr;</a>';
}
function pyHsCta(location) {
  return '<a class="btn-secondary" href="' + PY_DATA.hubspot.sourceUrl + '" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="hubspot" data-cta-location="' + location + '">View HubSpot pricing &rarr;</a>';
}
function pyOnSummary(lines) {
  var parts = [];
  for (var i = 0; i < lines.length; i++) {
    var phrase = pyAddonPhrase(lines[i]);
    if (phrase) parts.push(phrase);
  }
  return parts.length ? parts.join('; ') : 'No add-ons';
}
function pyPdCard(row, label) {
  return '<div class="summary-card result-card">' +
    '<div class="summary-label">' + label + '</div>' +
    '<div class="summary-metric">' + pyTotal(row) + (row.total === null ? '' : ' / yr') + '</div>' +
    '<details class="math-drawer"><summary>Show calculation</summary><div class="math-drawer-body">' + pyMathRows(row) + '</div></details>' +
    '<div class="summary-driver">' + row.planLabel + '</div>' +
    '<div class="summary-scenario">' + pyOnSummary(row.lines) + '</div>' +
    '<div class="summary-actions"><div class="cta-stack">' + pyCta('summary-card') + '</div></div></div>';
}
function pyLowestCard(result) {
  var metric, driver;
  if (!result.lowest) {
    metric = 'Not determined';
    driver = 'An add-on price basis is unpublished, so no plan is marked lowest';
  } else if (result.lowest.tie) {
    metric = 'Same cost';
    driver = pyMoney(result.lowest.total) + '/yr on more than one plan';
  } else {
    var row = null;
    for (var i = 0; i < result.rows.length; i++) if (result.rows[i].id === result.lowest.id) row = result.rows[i];
    metric = row.planLabel;
    driver = pyMoney(result.lowest.total) + '/yr on annual billing';
  }
  return '<div class="summary-card result-card card-lowest">' +
    '<div class="summary-label">Lowest Year-1 cost</div>' +
    '<div class="summary-metric" style="color:var(--emerald);">' + metric + '</div>' +
    '<details class="math-drawer"><summary>Show calculation</summary><div class="math-drawer-body">' + pyMathRows(result.current) + '</div></details>' +
    '<div class="summary-driver">' + driver + '</div>' +
    '<div class="summary-scenario">Prices verified ' + PY_DATA.pipedrive.verified + '</div>' +
    '<div class="summary-actions"><a class="summary-audit-link" href="#py-compare-heading" data-track="internal-audit">Compare side by side &darr;</a></div></div>';
}
function pyAddonCard(result) {
  var lines = result.current.lines;
  var extra = 0, floor = 0, unknown = false, unpriced = false, on = false;
  var body = '<div class="calc-math-list">';
  for (var i = 0; i < lines.length; i++) {
    var line = lines[i];
    if (!line.on) continue;
    on = true;
    var val;
    if (line.included) {
      val = 'Included';
      extra += 0;
      floor += 0;
    } else if (line.unknown) {
      unknown = true;
      if (line.floor === null) { unpriced = true; val = 'unknown' + pyPill(); }
      else { floor += line.floor; val = '&ge; ' + pyMoney(line.floor) + pyPill(); }
    } else {
      extra += line.amount;
      floor += line.amount;
      val = pyMoney(line.amount);
    }
    body += '<div class="calc-math-row"><span class="calc-math-label"><strong>' + line.label + '</strong><span class="calc-math-formula">' + pyAddonPhrase(line) + '</span></span><span class="calc-math-val">' + val + '</span></div>';
  }
  if (!on) body += '<div class="calc-math-row"><span class="calc-math-label"><strong>Add-ons</strong><span class="calc-math-formula">None selected</span></span><span class="calc-math-val">' + pyMoney(0) + '</span></div>';
  var row = { total: (unknown || unpriced) ? null : pyCents(extra), floor: unpriced ? null : pyCents(floor) };
  body += '<div class="calc-math-row"><span class="calc-math-label"><strong>Add-on Year-1</strong><span class="calc-math-formula">' + (unknown ? 'Floor only where the price basis is unpublished' : 'Known add-ons') + '</span></span><span class="calc-math-val">' + (on ? pyTotal(row) : pyMoney(0)) + '</span></div></div>';
  return '<div class="summary-card result-card"><div class="summary-label">Add-ons on this plan</div>' +
    '<div class="summary-metric">' + (on ? pyTotal(row) : pyMoney(0)) + (row.total === null ? '' : ' / yr') + '</div>' +
    '<details class="math-drawer"><summary>Show calculation</summary><div class="math-drawer-body">' + body + '</div></details>' +
    '<div class="summary-driver">' + pyOnSummary(lines) + '</div>' +
    '<div class="summary-scenario">Included add-ons are not an extra charge</div></div>';
}
function pyCardsHtml(result) {
  return pyLowestCard(result) + pyPdCard(result.current, 'Your plan') + pyAddonCard(result);
}
function pyTableHtml(result) {
  var rows = result.rows;
  var html = '';
  for (var i = 0; i < rows.length; i++) {
    var row = rows[i];
    var add = pyOnSummary(row.lines);
    html += '<tr><td data-label="Platform"><strong>Pipedrive</strong><br><span class="status-pill status-verified">Verified</span> &middot; <a href="' + PY_DATA.pipedrive.sourceUrl + '" target="_blank" rel="noopener" class="source-link">pipedrive.com/pricing</a><div class="cp-verified">Verified ' + PY_DATA.pipedrive.verified + '</div></td>' +
      '<td data-label="Plan chosen">' + row.planLabel + ' &middot; ' + pyUnit(row.rate) + '/seat/mo<div class="cp-verified">Annual billing</div></td>' +
      '<td data-label="Seats &amp; add-ons">' + row.seats + ' seats: ' + pyMoney(row.seat) + (add === 'No add-ons' ? '' : ' &middot; ' + add) + '</td>' +
      '<td data-label="Calling / dialer">Not in this total. Pipedrive has no built-in dialer.</td>' +
      '<td data-label="True Year-1 cost"><strong>' + pyTotal(row) + '</strong></td>' +
      '<td data-label="Action">' + pyCta('comparison-table') + '</td></tr>';
  }
  return html;
}
function pyBestLine(result) {
  if (!result.lowest) return '<strong>Lowest Year-1 cost:</strong> not determined, because an add-on price basis is unpublished.';
  if (result.lowest.tie) return '<strong>Lowest Year-1 cost:</strong> ' + pyMoney(result.lowest.total) + '/yr on more than one plan.';
  var row = null;
  for (var i = 0; i < result.rows.length; i++) if (result.rows[i].id === result.lowest.id) row = result.rows[i];
  return '<strong>Lowest Year-1 cost:</strong> Pipedrive ' + row.planLabel + ' (' + pyMoney(result.lowest.total) + '/yr).';
}
function pyScenario(result) {
  return result.seats + (result.seats === 1 ? ' seat' : ' seats') + ' &middot; annual billing &middot; ' + result.current.planLabel;
}
function pyCompareCards(r) {
  var pd = r.pipedrive, hs = r.hubspot;
  var metric, driver;
  if (r.lowest === 'pipedrive' || r.lowest === 'hubspot') {
    metric = r.lowest === 'pipedrive' ? 'Pipedrive' : 'HubSpot';
    driver = r.difference !== null ? pyMoney(r.difference) + '/yr less than ' + (r.lowest === 'pipedrive' ? 'HubSpot' : 'Pipedrive') : 'Lower even at the minimum of the unverified side';
  } else if (r.lowest === 'tie') {
    metric = 'Same cost';
    driver = pyMoney(pd.total) + '/yr on both';
  } else {
    metric = 'Not determined';
    driver = 'An add-on price basis is unpublished, so the two totals are not ranked';
  }
  var lowest = '<div class="summary-card result-card card-lowest"><div class="summary-label">Lowest Year-1 cost</div>' +
    '<div class="summary-metric" style="color:var(--emerald);">' + metric + '</div>' +
    '<details class="math-drawer"><summary>Show calculation</summary><div class="math-drawer-body">' + pyMathRows(pd) + pyHsMath(hs) + '</div></details>' +
    '<div class="summary-driver">' + driver + '</div>' +
    '<div class="summary-scenario">Pipedrive prices verified ' + PY_DATA.pipedrive.verified + '</div>' +
    '<div class="summary-actions"><a class="summary-audit-link" href="#py-compare-heading" data-track="internal-audit">Compare side by side &darr;</a></div></div>';
  var pdCard = '<div class="summary-card result-card"><div class="summary-label">Pipedrive Year-1 cost</div>' +
    '<div class="summary-metric">' + pyTotal(pd) + (pd.total === null ? '' : ' / yr') + '</div>' +
    '<details class="math-drawer"><summary>Show calculation</summary><div class="math-drawer-body">' + pyMathRows(pd) + '</div></details>' +
    '<div class="summary-driver">Pipedrive ' + pd.planLabel + '</div>' +
    '<div class="summary-scenario">' + pyOnSummary(pd.lines) + '</div>' +
    '<div class="summary-actions"><div class="cta-stack">' + pyCta('summary-card') + '</div></div></div>';
  var hsCard = '<div class="summary-card result-card"><div class="summary-label">HubSpot Year-1 cost</div>' +
    '<div class="summary-metric">' + pyMoney(hs.total) + ' / yr</div>' +
    '<details class="math-drawer"><summary>Show calculation</summary><div class="math-drawer-body">' + pyHsMath(hs) + '</div></details>' +
    '<div class="summary-driver">' + hs.planLabel + '</div>' +
    '<div class="summary-scenario">' + pyMoney(hs.seat) + ' seats + ' + pyMoney(hs.onboarding) + ' onboarding</div>' +
    '<div class="summary-actions"><div class="cta-stack">' + pyHsCta('summary-card') + '</div></div></div>';
  return lowest + pdCard + hsCard;
}
function pyCompareTable(r) {
  var pd = r.pipedrive, hs = r.hubspot;
  var add = pyOnSummary(pd.lines);
  return '<tr><td data-label="Platform"><strong>Pipedrive</strong><br><span class="status-pill status-verified">Verified</span> &middot; <a href="' + PY_DATA.pipedrive.sourceUrl + '" target="_blank" rel="noopener" class="source-link">pipedrive.com/pricing</a><div class="cp-verified">Verified ' + PY_DATA.pipedrive.verified + '</div></td>' +
    '<td data-label="Plan chosen">' + pd.planLabel + ' &middot; ' + pyUnit(pd.rate) + '/seat/mo</td>' +
    '<td data-label="Seats &amp; add-ons">' + pd.seats + ' seats: ' + pyMoney(pd.seat) + (add === 'No add-ons' ? '' : ' &middot; ' + add) + '</td>' +
    '<td data-label="Calling / dialer">Not priced. Pipedrive has no built-in dialer, and a Marketplace dialer is not added here.</td>' +
    '<td data-label="True Year-1 cost"><strong>' + pyTotal(pd) + '</strong></td>' +
    '<td data-label="Action">' + pyCta('comparison-table') + '</td></tr>' +
    '<tr><td data-label="Platform"><strong>HubSpot</strong><br><span class="status-pill status-verified">Verified</span> &middot; <a href="' + PY_DATA.hubspot.sourceUrl + '" target="_blank" rel="noopener" class="source-link">hubspot.com/pricing/sales</a><div class="cp-verified">Verified ' + PY_DATA.hubspot.verified + '</div></td>' +
    '<td data-label="Plan chosen">' + hs.planLabel + ' &middot; ' + pyUnit(hs.rate) + '/seat/mo</td>' +
    '<td data-label="Seats &amp; add-ons">' + hs.seats + ' seats: ' + pyMoney(hs.seat) + ' + ' + pyMoney(hs.onboarding) + ' onboarding</td>' +
    '<td data-label="Calling / dialer">Calling credits are not in this total.</td>' +
    '<td data-label="True Year-1 cost"><strong>' + pyMoney(hs.total) + '</strong></td>' +
    '<td data-label="Action">' + pyHsCta('comparison-table') + '</td></tr>';
}
function pyCompareBest(r) {
  if (r.lowest === null) return '<strong>Lowest Year-1 cost:</strong> not determined, because an add-on price basis is unpublished.';
  if (r.lowest === 'tie') return '<strong>Lowest Year-1 cost:</strong> ' + pyMoney(r.pipedrive.total) + '/yr on both.';
  var name = r.lowest === 'pipedrive' ? ('Pipedrive ' + r.pipedrive.planLabel) : r.hubspot.planLabel;
  var total = r.lowest === 'pipedrive' ? r.pipedrive.total : r.hubspot.total;
  var other = r.lowest === 'pipedrive' ? 'HubSpot' : 'Pipedrive';
  return '<strong>Lowest Year-1 cost:</strong> ' + name + ' (' + pyMoney(total) + '/yr)' +
    (r.difference !== null ? ' &middot; ' + pyMoney(r.difference) + '/yr less than ' + other : '') + '.';
}
function pyCompareScenario(r) {
  return r.seats + (r.seats === 1 ? ' seat' : ' seats') + ' &middot; annual billing &middot; Pipedrive ' + r.pipedrive.planLabel + ' &middot; ' + r.hubspot.planLabel;
}
