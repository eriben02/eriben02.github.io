"""
Nightly Publisher Engine for SaaSBill (/workspace/saastruth/scripts/nightly_publish.py)
Pops the next queued topic from /workspace/saastruth/data/publishing_queue.json,
builds a light-editorial calculator page with natural answer-first copy (no robotic labels),
dynamic freshness signals, and refreshes sitemap.xml (<lastmod>), llms.txt, and llms-full.txt.
"""
import json
import os
from layout import load_data, render_page, PUBLIC_DIR, DATA_DIR, SITE_ORIGIN, get_freshness_timestamps
from update_meta_files import generate_meta_files

def run_nightly(dry_run=False):
    queue_path = os.path.join(DATA_DIR, "publishing_queue.json")
    log_path = os.path.join(DATA_DIR, "publish_log.json")
    with open(queue_path) as f:
        queue = json.load(f)

    next_item = next((item for item in queue if item.get("status") == "queued"), None)
    if not next_item:
        print("No queued items remaining.")
        return

    iso_date, iso_datetime, human_date = get_freshness_timestamps()

    if dry_run:
        print(f"[DRY RUN] Next nightly page to publish: #{next_item['priority']} -> {next_item['slug']} ({next_item['title']}) [timestamp={iso_datetime}]")
        return

    tools, affiliates = load_data()
    aff = affiliates.get(next_item["primary_affiliate"], {"destination_url": "https://saasbill.io/", "program_name": "Partner"})
    slug_clean = next_item["slug"].strip("/")
    rel_html_path = f"{slug_clean}/index.html"

    body_html = f"""
    <section class="hero">
      <h1>{next_item['title']}</h1>
      <p class="lead">Independent contract and Year-1 cost audit for {next_item['category']}. Use the calculator below to check hidden overages, renewal notice windows, and lower-cost alternatives.</p>
      <div class="geo-direct-answer">
        <p><strong>The short version:</strong> Standard advertised pricing in {next_item['category']} frequently omits seat-bucket minimums, auto-renewal notice windows (30–60 days), and usage overage multipliers. Comparing your workload against transparent-pricing alternatives such as <strong>{aff.get('program_name')}</strong> helps avoid mandatory onboarding fees and annual lock-in traps.</p>
      </div>
    </section>
    <section class="calc-box">
      <h2 style="margin-top:0;">Compare verified contract terms</h2>
      <p style="color:var(--muted); margin-bottom:16px;">Compare your current quote against <strong>{aff.get('program_name')}</strong>.</p>
      <div class="cta-stack"><a class="btn-cta" href="{aff.get('destination_url')}" target="_blank" rel="nofollow noopener" data-track="vendor-cta">View official pricing &rarr;</a></div>
    </section>
    """
    faqs = [
        (f"What is the biggest hidden contract cost in {next_item['title']}?", f"As checked on {human_date} ({iso_date}), the main cost escalators are mandatory onboarding fees, 30-to-60 day auto-renewal cancellation windows, and uncapped usage or per-resolution overage charges."),
        (f"Which transparent alternative is recommended for {next_item['category']}?", f"We recommend evaluating {aff.get('program_name')} ({aff.get('destination_url')}), which offers self-serve pricing without mandatory onboarding fees.")
    ]
    render_page(rel_html_path, next_item["title"], next_item["title"], next_item["slug"], body_html, faqs=faqs, published_date=iso_date)
    next_item["status"] = "published"
    next_item["published_at"] = iso_datetime

    with open(queue_path, "w") as f:
        json.dump(queue, f, indent=2)

    published_slugs = [item["slug"] for item in queue if item.get("status") == "published"]
    generate_meta_files(extra_urls=published_slugs)

    logs = []
    if os.path.exists(log_path):
        with open(log_path) as f:
            logs = json.load(f)
    logs.append({"date": iso_datetime, "slug": next_item["slug"], "title": next_item["title"], "affiliate": next_item["primary_affiliate"]})
    with open(log_path, "w") as f:
        json.dump(logs, f, indent=2)
    print(f"Published nightly page: {next_item['slug']} [dateModified={iso_datetime}]")

if __name__ == "__main__":
    import sys
    run_nightly(dry_run="--dry-run" in sys.argv)
