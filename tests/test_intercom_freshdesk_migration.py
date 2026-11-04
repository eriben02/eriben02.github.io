"""Intercom to Freshdesk migration Year-1 calculator. Facts checked 2026-11-04."""
import json
import os
import re
import subprocess
import sys
import unittest

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(BASE, "scripts"))
import build_intercom_freshdesk_migration as page  # noqa: E402

REL = "exit/intercom-to-freshdesk-ticket-and-help-center-migration/index.html"
URL = "https://saasbill.io/exit/intercom-to-freshdesk-ticket-and-help-center-migration/"
DEFAULT_LINE = (
    "Lower Year-1 cost: Freshdesk, $7,289. Intercom $13,620. Difference $6,331. "
    "This counts one Fin outcome as one Freddy email session. "
    "An outcome is charged once per conversation. "
    "A Freddy email session is a 72-hour window and is charged either way."
)


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def extract_js(html):
    parts = []
    for name in (
        "calcIntercomFreshdesk",
        "imMoney",
        "imPlanName",
        "imLowerSentence",
        "imMathText",
    ):
        signature = "function " + name
        start = html.find(signature)
        brace = html.find("{", start)
        depth = 0
        end = None
        for index, char in enumerate(html[brace:], brace):
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    end = index + 1
                    break
        parts.append(html[start:end])
    return "\n".join(parts)


class TestIntercomFreshdeskMigration(unittest.TestCase):
    def page(self):
        root = read(os.path.join(BASE, REL))
        public = read(os.path.join(BASE, "public", REL))
        self.assertEqual(root, public)
        return root

    def test_default_example_and_unit_mismatch(self):
        result = page.calc({
            "agents": 5,
            "outcomes": 1000,
            "records": 10000,
            "intercom": "essential",
            "freshdesk": "growth",
            "billing": "annual",
            "copilot": False,
        })
        self.assertEqual(result["icSeat"], 174000)
        self.assertEqual(result["fin"], 1188000)
        self.assertEqual(result["icYear"], 1362000)
        self.assertEqual(result["fdSeat"], 114000)
        self.assertEqual(result["packs"], 115)
        self.assertEqual(result["freddy"], 563500)
        self.assertEqual(result["migration"], 51400)
        self.assertEqual(result["fdYear"], 728900)
        self.assertEqual(result["diff"], 633100)
        self.assertEqual(result["lower"], "freshdesk")
        self.assertEqual(page.lower_sentence(result), DEFAULT_LINE)
        html = self.page()
        self.assertIn("Lower Year-1 cost:</strong> Freshdesk, $7,289. Intercom $13,620. Difference $6,331.", html)
        self.assertIn("Those units are not the same", html)
        self.assertIn("72-hour window", html)
        # One outcome is not forced up to a 50-outcome minimum.
        small = page.calc({"agents": 1, "outcomes": 1, "records": 0, "copilot": False})
        self.assertEqual(small["fin"], 1188)
        self.assertEqual(small["packs"], 0)

    def test_unknown_migration_monthly_packs_and_copilot(self):
        unknown = page.calc({"agents": 5, "outcomes": 1000, "records": 2500, "copilot": False})
        self.assertIsNone(unknown["migration"])
        self.assertIsNone(unknown["fdYear"])
        self.assertIsNone(unknown["diff"])
        self.assertIn("Difference: unknown.", page.lower_sentence(unknown))
        self.assertNotIn("$0", page.lower_sentence(unknown).split("Difference")[1][:40])
        thousand = page.calc({"agents": 5, "outcomes": 1000, "records": 1000, "copilot": False})
        self.assertEqual(thousand["migration"], 10000)
        empty = page.calc({"agents": 5, "outcomes": 1000, "records": 0, "copilot": False})
        self.assertEqual(empty["migration"], 0)
        self.assertEqual(empty["fdYear"], 677500)
        annual = page.calc({"agents": 1, "outcomes": 50, "records": 0, "billing": "annual", "copilot": False})
        monthly = page.calc({"agents": 1, "outcomes": 50, "records": 0, "billing": "monthly", "copilot": False})
        self.assertEqual(annual["packs"], 1)
        self.assertEqual(monthly["packs"], 2)
        self.assertEqual(monthly["fdRate"], 23)
        self.assertEqual(monthly["icRate"], 39)
        growth = page.calc({"agents": 5, "outcomes": 1000, "records": 10000, "freshdesk": "growth", "copilot": True})
        self.assertEqual(growth["copilotState"], "not-on-growth")
        self.assertEqual(growth["copilot"], 0)
        self.assertEqual(growth["fdYear"], 728900)
        pro = page.calc({"agents": 5, "outcomes": 1000, "records": 10000, "freshdesk": "pro", "copilot": True})
        self.assertEqual(pro["copilot"], 174000)
        self.assertEqual(pro["fdSeat"], 330000)
        self.assertEqual(pro["fdYear"], 1118900)
        low = page.calc({"agents": 1, "outcomes": 10, "records": 10000, "copilot": False})
        self.assertEqual(low["icYear"], 46680)
        self.assertEqual(low["fdYear"], 74200)
        self.assertEqual(low["lower"], "intercom")

    def test_javascript_matches_python(self):
        html = self.page()
        script = extract_js(html) + """
        const cases = %s;
        const out = cases.map((row) => {
          const result = calcIntercomFreshdesk(row);
          return { result: result, line: imLowerSentence(result), math: imMathText(result) };
        });
        console.log(JSON.stringify(out));
        """ % json.dumps([
            {"agents": 5, "outcomes": 1000, "records": 10000, "intercom": "essential", "freshdesk": "growth", "billing": "annual", "copilot": False},
            {"agents": 5, "outcomes": 1000, "records": 2500, "intercom": "essential", "freshdesk": "growth", "billing": "annual", "copilot": False},
            {"agents": 1, "outcomes": 50, "records": 0, "intercom": "essential", "freshdesk": "growth", "billing": "monthly", "copilot": False},
            {"agents": 5, "outcomes": 1000, "records": 10000, "intercom": "expert", "freshdesk": "pro", "billing": "annual", "copilot": True},
            {"agents": 0, "outcomes": 0, "records": 0, "intercom": "essential", "freshdesk": "growth", "billing": "annual", "copilot": False},
        ])
        res = subprocess.run(["node", "-e", script], capture_output=True, text=True, check=True)
        rows = json.loads(res.stdout)
        inputs = json.loads(script.split("const cases = ", 1)[1].split(";", 1)[0])
        for raw, row in zip(inputs, rows):
            expected = page.calc(raw)
            self.assertEqual(row["result"], expected)
            self.assertEqual(row["line"], page.lower_sentence(expected))
        self.assertIn(rows[0]["math"], html)

    def test_title_sources_and_no_affiliate_link(self):
        html = self.page()
        title = re.search(r"<title>(.*?)</title>", html).group(1)
        self.assertLessEqual(len(title), 60, title)
        self.assertEqual(title, "Intercom to Freshdesk Year-1 – saasbill.io")
        self.assertEqual(title, re.search(r'property="og:title" content="(.*?)"', html).group(1))
        self.assertIn("<h1>Migrate off Intercom Fin without losing ticket history</h1>", html)
        self.assertNotIn("Best option", html)
        self.assertNotIn("Winner", html)
        self.assertNotIn("answer first", html.lower())
        self.assertNotIn("SaaSTruth", html)
        self.assertNotIn("Erik", html)
        self.assertNotIn("\u2014", html)
        self.assertNotIn("&mdash;", html)
        self.assertNotIn("/go/fresh", html)
        self.assertNotIn('rel="sponsored', html)
        self.assertNotIn("Direct vendor link", html)
        for source in (
            "https://www.intercom.com/pricing",
            "https://www.intercom.com/learning-center/intercom-pricing",
            "https://www.intercom.com/help/en/articles/8205718-fin-ai-agent-outcomes",
            "https://www.freshworks.com/freshdesk/pricing/",
            "https://support.freshdesk.com/support/solutions/articles/50000011515-manage-freddy-ai-add-ons",
            "https://superdupr.com/blog/freshdesk-pricing",
            "https://www.getmacha.com/blog/best-freshdesk-migration-tools",
            "https://www.getmacha.com/blog/intercom-to-freshdesk-migration",
            "https://clankersupport.com/blog/intercom-fin-pricing",
            "https://aftersales.co/blog/intercom-pricing",
            "https://www.reddit.com/r/intercom/comments/1u9xxgm/has_anyone_genuinely_cut_their_fin_bill_in_half/",
            "https://www.reddit.com/r/intercom/comments/1trb4cg/fin_is_getting_expensive_and_i_want_to_know_what/",
        ):
            self.assertIn(source, html)
        self.assertIn("4 Nov 2026", html)
        self.assertIn("19 Oct 2026", html)
        self.assertIn("unknown", html)
        self.assertIn("$0.99", html)
        self.assertIn("$49", html)
        self.assertEqual(html.count("Some links are affiliate links. They never change the math."), 1)
        self.assertIn("mobile-cards", html)
        self.assertNotIn("<td>", html)
        self.assertGreaterEqual(len(html.encode("utf-8")), 20 * 1024)
        self.assertIn('class="table-wrap editorial-gap-table mobile-cards"', html)
        self.assertIn("Show calculation", html)
        self.assertIn("True Year-1 cost", html)

    def test_homepage_queue_and_sitemap(self):
        home = read(os.path.join(BASE, "index.html"))
        public_home = read(os.path.join(BASE, "public", "index.html"))
        self.assertEqual(home, public_home)
        block = home[home.index('id="all-calculators"'):]
        self.assertIn("./exit/intercom-to-freshdesk-ticket-and-help-center-migration/", block)
        for name in ("sitemap.xml", "llms.txt", "llms-full.txt"):
            self.assertIn("/exit/intercom-to-freshdesk-ticket-and-help-center-migration/", read(os.path.join(BASE, name)))
            self.assertIn("/exit/intercom-to-freshdesk-ticket-and-help-center-migration/", read(os.path.join(BASE, "public", name)))
        with open(os.path.join(BASE, "data", "publishing_queue.json"), encoding="utf-8") as handle:
            queue = json.load(handle)
        item = next(row for row in queue if row["slug"] == "/exit/intercom-to-freshdesk-ticket-and-help-center-migration/")
        self.assertEqual(item["status"], "published")
        self.assertEqual(item["published_at"], "2026-11-04")
        self.assertEqual(item["url"], URL)
        self.assertEqual(item["category"], "Helpdesk & AI Support")
        self.assertIn("2026-11-04", item["verification_note"])
        self.assertIn("not approved", item["verification_note"])


if __name__ == "__main__":
    unittest.main()
