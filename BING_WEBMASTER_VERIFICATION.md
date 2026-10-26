# Bing Webmaster Tools Verification Guide for saasbill.io

Why this matters for GEO (Generative Engine Optimization):
ChatGPT Search (`OAI-SearchBot`) and Microsoft Copilot rely heavily on the **Bing Web Index** alongside direct crawling. Verifying `https://saasbill.io` in Bing Webmaster Tools and submitting `https://saasbill.io/sitemap.xml` accelerates indexing across Bing, ChatGPT Search, and Perplexity.

## Option A — 1-Click Import from Google Search Console (Fastest, 0 code changes)
1. Go to [https://www.bing.com/webmasters](https://www.bing.com/webmasters) and sign in.
2. Click **Import from Google Search Console** on the welcome screen.
3. Authorize with the Google account where `saasbill.io` is verified in GSC.
4. Bing automatically verifies ownership and imports `https://saasbill.io/sitemap.xml`.

## Option B — HTML Meta Tag in `scripts/layout.py`
1. In Bing Webmaster Tools, choose **Add a site manually** -> enter `https://saasbill.io/`.
2. Select **HTML Meta Tag** and copy the `<meta name="msvalidate.01" content="..." />` tag.
3. Open `scripts/layout.py`, replace the placeholder comment under `<meta name="viewport" ...>` with your tag, and run `python3 scripts/build.py` to propagate it to all 17 pages.

## Option C — DNS CNAME Record
Add the CNAME record provided by Bing (`<bing-hash>` -> `verify.bing.com`) in your DNS provider for `saasbill.io`.
