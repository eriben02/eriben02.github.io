# SaaSBill design and copy

Read this before changing a page or the UI. New pages use the same shell and classes as the pages already on saasbill.io. They should not look like a separate site.

## 1. Principles

These are internal. Do not print them as visible copy. The copy lint in `data/copy_lint.json` rejects "answer first", "explanation on demand", "30-day test", "test section", and the other phrases listed there.

- The answer is the first thing on the page: the lead sentence under the `h1`. The longer explanation sits in a `<details>` block, or under "Show calculation" when the page is a calculator.
- Labels follow the math. Use "Lowest Year-1 cost:" or "Lowest cost:" / "Lower cost:". Do not use "Best option", "Best choice", or "Winner".
- An unknown price is the word "unknown". It is never `$0`.
- Every factual claim keeps a source link and the access date, in small muted type (`.src-cluster`, `.src-link`, `.src-date`).
- One footer line on pages that contain affiliate links: "Some links are affiliate links. They never change the math." It links to the methodology section. Pass `show_affiliate_note=False` to `render_page` when a page has no affiliate links, as `/ai-act/` does.
- Do not add a disclosure under each button. The exception is a partner contract that requires its own line. The Jotform Wix guide uses `.paid-partnership-note` for that: "Paid partnership with Jotform (#JotformPartner). Some links are affiliate links."
- Affiliate clicks go through `/go/` and use `rel="sponsored nofollow noopener"`.

## 2. Components to reuse

`scripts/layout.py` builds every page.

`render_page(rel_path, title, description, canonical_path, body_html, faqs=None, extra_schema=None, published_date=None, show_affiliate_note=True)` writes `public/` and the caller copies the file to the repo root. It adds the header, TechArticle JSON-LD, the related-links block, and the footer. The document `<title>`, `og:title`, and `twitter:title` are the same string. If `title` does not already contain "saasbill", the function appends ` – saasbill.io`. Keep that full string at or under 60 characters. Reference: `ai-act/index.html`.

`render_workbench(controls_html, controls_title="Estimate Your True Cost", chart_title="Your Estimated True Cost", cta_href="#comparison", cta_label="See pricing", cta_vendor="saasbill")` is the shared calculator: controls, stacked bar, result column, and the sticker / hidden-cost cards. Reference: the homepage workbench in `index.html`.

`render_related_links` adds four cards under the heading "Related calculators", plus a "Browse all" list. The homepage gets `render_site_directory` instead: every sitemap URL as a plain link, grouped by topic. Pages under `ai-act/` only link to the other AI Act guides, under "Related AI Act guides". Reference: `compare/close-vs-pipedrive-year-1-cost-calculator/index.html`, `index.html`, and `ai-act/index.html`.

| Class or element | What it is | Reference |
| --- | --- | --- |
| `.hero.editorial-hero.editorial-hero-wrap` | Page hero. The `h1` sits in this section on every page except the homepage, which uses `.editorial-hero`. | `compare/close-vs-pipedrive-year-1-cost-calculator/index.html` |
| `.lead` | The short answer under the `h1`. | `ai-act/index.html` |
| `.card` and `.card-grid` | Equal cards for the next pages or for a small set of icons. `compact-cards` is the tighter grid. | `ai-act/index.html`, `ai-act/deepfake-labelling-patterns/index.html` |
| `.summary-caveat` | Short muted note, including "Not legal advice." | `ai-act/index.html` |
| `.table-wrap.editorial-gap-table.mobile-cards` | Comparison table. Each `td` has `data-label` so it stacks on a phone. | `ai-act/article-50-deployer-checklist/index.html` |
| `.key-list` | A simple list under a heading, including the source list. | `ai-act/etsi-ts-104-275-explained/index.html` |
| `details.full-table-disclosure.below-disclosure` | Explanation on demand. Summary uses `.full-table-summary`, `.below-disclosure-title`, and `.full-table-toggle-pill`. Body is `.full-table-body`. | `compare/close-vs-pipedrive-year-1-cost-calculator/index.html` |
| `details.math-drawer` | "Show calculation". The body is `.math-drawer-body`. It opens as a popover on the result column. | Homepage workbench in `index.html` |
| `.src-cluster`, `.src-link`, `.src-date` | Discreet source link plus "Accessed …" date. | `ai-act/deepfake-labelling-patterns/index.html` |
| `.paid-partnership-note` | The one contracted partnership line. | `guides/jotform-wix-app-setup-and-pricing-guide/index.html` |
| `.footer-note` and `.footer-disclosure` | Footer date, inquiries, and the single affiliate sentence. | Any calculator page |
| `.related-calc-grid` | The related-link cards. | `ai-act/index.html` |
| `.ai-act-pre` | Scrolls the illustrative HTML snippet instead of widening the page. Do not reuse it for new copy. | `ai-act/deepfake-labelling-patterns/index.html` |

## 3. Copy rules

English, plain, and specific. No internal or process words. The banned list and the per-page whitelist live in `data/copy_lint.json`. The deploy guard runs that lint on every pull request and on main.

## 4. Checklist before opening a pull request

- The page is built with `render_page` and, when it is a calculator, `render_workbench`.
- No new CSS unless the existing classes cannot do the job. Say why in the pull request.
- No new inline `<style>` block, and no CSS class that is missing from `assets/styles.css`, unless it is already listed in `tests/test_style_reuse.py`.
- `data/copy_lint.json` passes.
- Desktop and mobile screenshots sit next to a reference page from the table above.
- `python3 -m unittest discover -s tests`, `node tests/calc_test.js`, `node tests/test_calculator_scenarios.js`, and `node scripts/test_calculators.js` pass.
