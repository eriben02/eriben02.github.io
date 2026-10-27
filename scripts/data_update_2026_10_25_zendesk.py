"""Verified data additions for the Zendesk AI outcome-pricing page (verified 2026-10-25).
Idempotent: re-running replaces entries by id."""
import json, os, sqlite3
D = "/workspace/saastruth/data"
V = "2026-10-25"
ZP = "https://www.zendesk.com/pricing/"
ZA = "https://support.zendesk.com/hc/en-us/articles/10479587390106-Managing-resolution-allowances"
ZT = "https://support.zendesk.com/hc/en-us/articles/9570369117338-About-automated-resolution-tiers"
ZC = "https://www.zendesk.com/company/agreements-and-terms/zendesk-customer-agreement/"
FP = "https://www.freshworks.com/freshdesk/pricing/"
HP = "https://www.helpscout.com/pricing/"
HA = "https://docs.helpscout.com/article/1421-about-annual-payments"

new_tools = [
 {"id":"zendesk-suite-team","name":"Zendesk Suite Team + AI Agents","vendor":"Zendesk","category":"Helpdesk & AI Support",
  "advertised_monthly_price_usd":55,"monthly_billing_price_usd":69,"seat_minimum":1,"actual_minimum_monthly_spend_usd":55,
  "mandatory_onboarding_fee_usd":0,"enterprise_onboarding_fee_usd":0,"enterprise_seat_price_usd":None,
  "ai_usage_tax_model":"5 automated resolutions/agent/month included (pricing page; help-center allowance model: $2/agent/month); then $1.50 committed or $2.00 pay-as-you-go per automated resolution. 'Allow overage' is the default setting; overage billed monthly regardless of subscription term.",
  "ai_per_resolution_usd":2.0,"billing_lock_in_type":"Annual or monthly; auto-renews for equivalent term at then-current rates unless 30 days' written notice (Zendesk Customer Agreement §7.2)",
  "cancellation_notice_days":30,"data_and_token_portability":"Not verified in this audit","hipaa_baa_minimum_tier":"Not HIPAA-enabled on Suite Team (pricing page: HIPAA enabled on Suite Professional)",
  "soc2_report_tier":"Not verified in this audit","sso_minimum_tier":"SAML/JWT SSO listed for all plans in pricing table",
  "trap_badge":"$2.00 PAYG per AI Resolution · Overage ON by Default","trap_severity":"high","verified_date":V,"affiliate_slug":"zendesk",
  "sources":[ZP,ZA,ZT,ZC]},
 {"id":"zendesk-suite-professional","name":"Zendesk Suite Professional + AI Agents","vendor":"Zendesk","category":"Helpdesk & AI Support",
  "advertised_monthly_price_usd":115,"monthly_billing_price_usd":149,"seat_minimum":1,"actual_minimum_monthly_spend_usd":115,
  "mandatory_onboarding_fee_usd":0,"enterprise_onboarding_fee_usd":0,"enterprise_seat_price_usd":None,
  "ai_usage_tax_model":"10 automated resolutions/agent/month included (pricing page; help-center allowance model: $5/agent/month, max $5,000/yr); then $1.50 committed or $2.00 pay-as-you-go. Copilot add-on $50/agent/month (annual).",
  "ai_per_resolution_usd":2.0,"billing_lock_in_type":"Annual or monthly; auto-renews for equivalent term at then-current rates unless 30 days' written notice (Zendesk Customer Agreement §7.2)",
  "cancellation_notice_days":30,"data_and_token_portability":"Not verified in this audit","hipaa_baa_minimum_tier":"Suite Professional ('HIPAA Enabled' in pricing table; BAA executed separately)",
  "soc2_report_tier":"Not verified in this audit","sso_minimum_tier":"SAML/JWT SSO listed for all plans in pricing table",
  "trap_badge":"$115 Seat + $1.50–$2.00 per Verified AI Resolution","trap_severity":"high","verified_date":V,"affiliate_slug":"zendesk",
  "sources":[ZP,ZA,ZT,ZC]},
 {"id":"help-scout-plus","name":"Help Scout Plus + AI Answers (Envoy)","vendor":"Help Scout","category":"Helpdesk & AI Support",
  "advertised_monthly_price_usd":45,"monthly_billing_price_usd":54,"seat_minimum":1,"actual_minimum_monthly_spend_usd":45,
  "mandatory_onboarding_fee_usd":0,"enterprise_onboarding_fee_usd":0,"enterprise_seat_price_usd":75,
  "ai_usage_tax_model":"$0.75 per AI resolution, billed monthly, with an optional monthly spending cap that auto-disables AI Answers; 3-month free AI trial for new accounts",
  "ai_per_resolution_usd":0.75,"billing_lock_in_type":"Monthly or annual prepay (16% discount); annual card payments auto-renew by default",
  "cancellation_notice_days":0,"data_and_token_portability":"Not verified in this audit","hipaa_baa_minimum_tier":"Pro ($75/user/mo, 10-user minimum) includes HIPAA; add-on on lower plans",
  "soc2_report_tier":"Not verified in this audit","sso_minimum_tier":"Pro includes SSO/SAML; add-on on Standard/Plus",
  "trap_badge":"Plus capped at 50 users · Pro needs 10-user minimum","trap_severity":"low","verified_date":V,"affiliate_slug":"help-scout",
  "notes":"Monthly-billing prices ($30/$54/$90) are from third-party checks (eesel.ai, resolve247.ai, Oct 2026); official page renders the annual toggle ($25/$45/$75).",
  "sources":[HP,HA]},
]
fd_update = {"advertised_monthly_price_usd":19,"monthly_billing_price_usd":23,"actual_minimum_monthly_spend_usd":19,"enterprise_seat_price_usd":89,
  "ai_usage_tax_model":"Freddy AI Agent: 500 sessions included once per account, then $49 per 100 sessions (billed per session, not per resolution); Freddy AI Copilot $29/agent/month (annual)",
  "ai_per_resolution_usd":0.49,"billing_lock_in_type":"Monthly or annual; no cancellation fees, cancellation takes effect at end of term",
  "cancellation_notice_days":0,"hipaa_baa_minimum_tier":"Not listed on Freshdesk pricing page (unverified)","sso_minimum_tier":"SAML SSO listed on all plans (Growth, Pro, Enterprise)",
  "soc2_report_tier":"Not verified in this audit","trap_badge":"Predictable Seats · $0.49/AI Session (charged even if unresolved)","verified_date":V,
  "notes":"Plans verified 2026-10-25: Growth $19 / Pro $55 / Enterprise $89 per agent/month annual; $23 / $66 / $107 monthly (from pricing-page data).","sources":[FP]}

tp = os.path.join(D,"tools.json"); tools = json.load(open(tp))
ids = {t["id"] for t in new_tools}
tools = [t for t in tools if t["id"] not in ids]
for t in tools:
    if t["id"] == "freshdesk-support": t.update(fd_update)
# insert new helpdesk tools right after freshdesk
idx = next(i for i,t in enumerate(tools) if t["id"]=="freshdesk-support")+1
tools[idx:idx] = new_tools
json.dump(tools, open(tp,"w"), indent=2, ensure_ascii=False)

ap = os.path.join(D,"affiliate_links.json"); aff = json.load(open(ap))
aff["freshworks"].update({
  "program_name":"Freshworks Affiliate Program (Freshdesk & Freshservice)","network":"PartnerStack",
  "commission":"20% of first-year subscription revenue (paid monthly up to 12 months); 25% at 50–100 and 30% at 101+ converted referrals/month (terms effective Mar 31, 2026); commissions only on initial MRR, not upgrades",
  "cookie_days":90,"conversion_window":"Referral must become paying within 3 months","signup_url":"https://market.partnerstack.com/page/freshworks4391",
  "terms_url":"https://www.freshworks.com/company/affiliate-partner/terms-and-conditions/","restrictions":"No PPC bidding on Freshworks brand keywords without permission; no coupon/spam traffic",
  "status":"not applied","verified_date":V})
aff["help-scout"] = {"program_name":"Help Scout Affiliate Program","network":"PartnerStack",
  "commission":"15% of every deal closed (1–10 referred customers in last 3 months); 20% (11+)","cookie_days":90,
  "official_program_url":"https://market.partnerstack.com/page/helpscout","signup_url":"https://market.partnerstack.com/page/helpscout",
  "restrictions":"No pay-per-click ads; no coupon/discount sites","tracking_url":"/go/help-scout","destination_url":"https://www.helpscout.com/pricing/",
  "status":"not applied","verified_date":V}
aff["zendesk"] = {"program_name":"Zendesk Marketing Affiliates","network":"PartnerStack",
  "commission":"15% rate for the first year of sales; 'Top Affiliates can earn more'; monthly payouts","cookie_days":None,
  "cookie_note":"Cookie length not published on official page (unverified)","official_program_url":"https://www.zendesk.com/programs/affiliate-program/",
  "signup_url":"https://www.zendesk.com/programs/affiliate-program/","restrictions":"Existing Zendesk partners/resellers/consultants not accepted",
  "tracking_url":"/go/zendesk","destination_url":"https://www.zendesk.com/pricing/","status":"not applied","verified_date":V,
  "editorial_note":"Optional: page is critical of Zendesk AI pricing; joining is compatible but disclose clearly."}
json.dump(aff, open(ap,"w"), indent=2, ensure_ascii=False)

# keep tools.sqlite in sync (not used by build, kept for completeness)
con = sqlite3.connect(os.path.join(D,"tools.sqlite"))
cols = [r[1] for r in con.execute("PRAGMA table_info(tools)")]
for t in tools:
    if t["id"] in ids or t["id"]=="freshdesk-support":
        vals = [t.get(c) for c in cols]
        con.execute(f"INSERT OR REPLACE INTO tools ({','.join(cols)}) VALUES ({','.join('?'*len(cols))})", vals)
con.commit(); con.close()
print("tools:",len(tools),"affiliates:",len(aff))
