"""Pipedrive Year-1 calculator and Pipedrive vs HubSpot comparison."""
import json
import os
import re
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from build_pipedrive_pages import (  # noqa: E402
    DEFAULT,
    HS_REL,
    HS_SLUG,
    PD_REL,
    PD_SLUG,
    hubspot_plans,
    js_core,
    load_pricing,
    page_data,
    run_node,
)

PUBLIC = os.path.join(ROOT, "public")


def read(rel):
    with open(os.path.join(PUBLIC, rel), encoding="utf-8") as handle:
        return handle.read()


def calc(kind, **kwargs):
    data = page_data(load_pricing())
    core = js_core(data)
    payload = dict(DEFAULT)
    payload.update(kwargs)
    if "addons" in kwargs:
        addons = dict(DEFAULT["addons"])
        addons.update(kwargs["addons"])
        payload["addons"] = addons
    return run_node(core, kind, {"one": payload})["one"]["r"]


class TestPipedriveYear1Math(unittest.TestCase):
    def test_default_growth_five_seats_is_exact(self):
        result = calc("pd")
        self.assertEqual(result["current"]["plan"], "growth")
        self.assertEqual(result["current"]["total"], 5 * 39 * 12)
        self.assertFalse(result["current"]["unknown"])
        self.assertEqual(result["lowest"]["id"], "lite")
        self.assertEqual(result["lowest"]["total"], 5 * 14 * 12)

    def test_leadbooster_is_per_company_and_included_on_premium(self):
        growth = calc("pd", addons={"leadbooster": True})
        self.assertEqual(growth["current"]["total"], 5 * 39 * 12 + 32.50 * 12)
        premium = calc("pd", plan="premium", addons={"leadbooster": True})
        self.assertEqual(premium["current"]["total"], 5 * 59 * 12)
        line = [item for item in premium["current"]["lines"] if item["id"] == "leadbooster"][0]
        self.assertTrue(line["included"])
        self.assertEqual(line["amount"], 0)

    def test_unknown_addon_basis_is_a_floor_and_not_zero(self):
        result = calc("pd", addons={"campaigns": True})
        row = result["current"]
        self.assertIsNone(row["total"])
        self.assertAlmostEqual(row["floor"], 5 * 39 * 12 + 13.33 * 12, places=2)
        self.assertIsNone(result["lowest"])
        self.assertNotEqual(row["floor"], 5 * 39 * 12)
        text = json.dumps(row)
        self.assertNotIn('"amount": 0', text.split("campaigns")[1][:80])

    def test_monthly_prices_are_not_in_the_browser_data(self):
        data = page_data(load_pricing())
        for plan in data["pipedrive"]["plans"].values():
            self.assertNotIn("monthly", plan)
            self.assertIsNotNone(plan["annual"])

    def test_hubspot_default_uses_tools_json(self):
        hs = hubspot_plans()
        with open(os.path.join(ROOT, "data", "tools.json"), encoding="utf-8") as handle:
            tools = json.load(handle)
        src = next(t for t in tools if t["id"] == "hubspot-sales-pro")
        self.assertEqual(hs["professional"]["annual"], src["advertised_monthly_price_usd"])
        self.assertEqual(hs["professional"]["onboarding"], src["mandatory_onboarding_fee_usd"])
        self.assertEqual(hs["enterprise"]["annual"], src["enterprise_seat_price_usd"])
        self.assertEqual(hs["enterprise"]["onboarding"], src["enterprise_onboarding_fee_usd"])
        result = calc("hs")
        self.assertEqual(result["pipedrive"]["total"], 2340)
        self.assertEqual(result["hubspot"]["total"], 5 * 90 * 12 + 1500)
        self.assertEqual(result["lowest"], "pipedrive")
        self.assertEqual(result["difference"], 4560)

    def test_unknown_addon_does_not_name_a_lowest_vendor(self):
        result = calc("hs", addons={"web_visitors": True})
        self.assertIsNone(result["pipedrive"]["total"])
        self.assertIsNone(result["lowest"])
        self.assertGreater(result["pipedrive"]["floor"], result["pipedrive"]["seat"])

    def test_starter_can_be_the_lower_exact_total(self):
        result = calc("hs", tier="starter")
        self.assertEqual(result["hubspot"]["total"], 5 * 15 * 12)
        self.assertEqual(result["lowest"], "hubspot")


class TestPipedriveYear1Pages(unittest.TestCase):
    def test_pages_use_the_shared_shell_and_go_link(self):
        for rel in (PD_REL, HS_REL):
            html = read(rel)
            self.assertIn("editorial-hero editorial-hero-wrap", html)
            self.assertIn("editorial-workbench", html)
            self.assertIn("wb-fill-chart", html)
            self.assertIn("Your Estimated True Cost", html)
            self.assertIn(">Show calculation<", html)
            self.assertIn("Lowest Year-1 cost", html)
            self.assertIn("True Year-1 cost", html)
            self.assertNotIn("—", html)
            self.assertNotIn("&mdash;", html)
            self.assertNotIn("PLACEHOLDER", html.upper())
            tags = re.findall(r"<a\b[^>]*data-vendor=\"pipedrive-crm\"[^>]*>", html)
            self.assertTrue(tags, rel)
            for tag in tags:
                self.assertIn('href="/go/pipedrive"', tag)
                self.assertIn('rel="sponsored nofollow noopener"', tag)
                self.assertIn('data-track="vendor-cta"', tag)
            self.assertNotIn("aff.trypipedrive.com", html)

    def test_sitemap_and_llms(self):
        sitemap = read("sitemap.xml")
        self.assertIn("https://saasbill.io" + PD_SLUG, sitemap)
        self.assertIn("https://saasbill.io" + HS_SLUG, sitemap)
        llms = read("llms.txt")
        self.assertIn(PD_SLUG, llms)
        self.assertIn(HS_SLUG, llms)

    def test_default_numbers_are_prerendered(self):
        pd = read(PD_REL)
        hs = read(HS_REL)
        self.assertIn("$2,340", pd)
        self.assertIn("$840", pd)
        self.assertIn("$2,340", hs)
        self.assertIn("$6,900", hs)
        self.assertIn("Lowest Year-1 cost:</strong> Pipedrive Growth", hs)


if __name__ == "__main__":
    unittest.main()
