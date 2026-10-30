"""Build the /ai-act/ test section from the 30 Oct 2026 drafts.

Facts, numbers and prices are the draft text. Each citation links to the
source and carries the access date. These pages have no affiliate links.
"""
import os
import shutil
from html import escape
from urllib.parse import quote

from layout import BASE_DIR, PUBLIC_DIR, render_page

ACCESSED = "Accessed 30 Oct 2026."

SOURCES = {
    "S1": ("https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-50", "AI Act Art. 50, Service Desk"),
    "S1b": ("https://eur-lex.europa.eu/eli/reg/2024/1689/oj", "Regulation (EU) 2024/1689, EUR-Lex"),
    "S2": ("https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/when-does-enforcement-start", "AI Act Service Desk FAQ, when enforcement starts"),
    "S3": ("https://digital-strategy.ec.europa.eu/en/policies/eu-icons-labelling-ai-generated-content", "EU icons for labelling AI-generated content"),
    "S3a": ("https://ec.europa.eu/newsroom/dae/redirection/document/129546", "EU icons SVG download"),
    "S3b": ("https://ec.europa.eu/newsroom/dae/redirection/document/129547", "EU icons PNG download"),
    "S4": ("https://ec.europa.eu/newsroom/dae/redirection/document/129555", "Code of Practice on Transparency of AI-generated Content"),
    "S4a": ("https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content", "Code of Practice policy page"),
    "S5": ("https://ai-act-service-desk.ec.europa.eu/sites/default/files/2026-07/guidelines_on_the_implementation_of_the_transparency_obligations_for_certain_ai_systems_under_article_50_of_the_ai_act_bzptwqhk0ikg1dtlddap41psfy_131215.pdf", "Commission Guidelines on Art. 50, C(2026) 5054 final"),
    "S5a": ("https://digital-strategy.ec.europa.eu/en/policies/guidelines-ai-transparency-obligations", "Art. 50 guidelines policy page"),
    "S6": ("https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-113", "AI Act Art. 113, Service Desk"),
    "S7": ("https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-111", "AI Act Art. 111, Service Desk"),
    "S8": ("https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng", "Regulation (EU) 2026/1744, EUR-Lex"),
    "S9": ("https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-99", "AI Act Art. 99, Service Desk"),
    "S10": ("https://digital-strategy.ec.europa.eu/en/news/strong-backing-code-practice-transparency-ai-generated-content", "Commission news, strong backing for the Code of Practice"),
    "E1": ("https://www.etsi.org/deliver/etsi_TS/104200_104299/104275/01.01.01_60/ts_104275v010101p.pdf", "ETSI TS 104 275 V1.1.1 PDF"),
    "E2": ("https://www.etsi.org/newsroom/press-releases/etsi-unveils-new-standard-to-reduce-production-of-harmful-deepfakes/", "ETSI press release, 29 Oct 2026"),
    "E3": ("https://portal.etsi.org/webapp/WorkProgram/Report_WorkItem.asp?WKI_ID=78186", "ETSI work programme, DTS/SAI-0031"),
    "T1": ("https://c2pa.org/", "C2PA"),
    "T2": ("https://spec.c2pa.org/specifications/specifications/2.5/index.html", "C2PA specifications, 2.5"),
    "T3": ("https://opensource.contentauthenticity.org/", "CAI open-source SDK"),
    "T4": ("https://helpx.adobe.com/creative-cloud/apps/adobe-content-authenticity/beta-overview.html", "Adobe Content Authenticity (Beta)"),
    "T5": ("https://blog.adobe.com/en/publish/2025/04/24/adobe-content-authenticity-now-public-beta-helps-creators-secure-attribution", "Adobe blog, public beta, 24 Apr 2025"),
    "T6": ("https://blog.google/innovation-and-ai/models-and-research/google-deepmind/synth-id-ai-content/", "Google blog, SynthID Detector"),
    "T7": ("https://ai.google.dev/responsible/docs/safeguards/synthid", "Google SynthID Text"),
    "T8": ("https://www.digimarc.com/solutions/provenance-authenticity", "Digimarc provenance and authenticity"),
    "T9": ("https://www.truepic.com/", "Truepic"),
    "T10": ("https://vision.truepic.dev/docs/lens-api", "Truepic Lens API"),
    "T11": ("https://www.truepic.com/pricing", "Truepic pricing"),
}


def cite(*keys):
    links = []
    for key in keys:
        url, label = SOURCES[key]
        links.append('<a class="src-link" href="%s">%s</a>' % (url, escape(label)))
    return '<span class="src-cluster">%s <span class="src-date">%s</span></span>' % (" &middot; ".join(links), ACCESSED)


def sources_section(keys):
    items = []
    for key in keys:
        url, label = SOURCES[key]
        items.append(
            '<li id="src-%s"><a href="%s">%s</a>. <span class="src-date">%s</span></li>'
            % (key, url, escape(label), ACCESSED)
        )
    return """
<section class="sources-block" aria-labelledby="sources-heading">
  <h2 id="sources-heading">Sources</h2>
  <ol class="sources-list">
    %s
  </ol>
</section>
""" % "\n    ".join(items)


def details(summary, body):
    return """<details class="explain-on-demand">
  <summary>%s</summary>
  <div class="explain-body">%s</div>
</details>""" % (summary, body)


def table(caption, headers, rows):
    head = "".join("<th>%s</th>" % escape(header) for header in headers)
    body = []
    for row in rows:
        cells = []
        for header, cell in zip(headers, row):
            cells.append('<td data-label="%s">%s</td>' % (escape(header), cell))
        body.append("<tr>%s</tr>" % "".join(cells))
    return """
<div class="table-wrap editorial-gap-table mobile-cards">
  <table>
    <caption>%s</caption>
    <thead><tr>%s</tr></thead>
    <tbody>%s</tbody>
  </table>
</div>
""" % (caption, head, "".join(body))


COMING = """
<aside class="coming-soon-box" aria-label="Free checklist">
  <p class="coming-soon-title">Free checklist (PDF) coming soon</p>
  <p>AI Act Article 50: the 2-page labelling checklist for teams that publish AI content.</p>
</aside>
"""


def hero(h1, lead):
    return """
<section class="hero editorial-hero editorial-hero-wrap">
  <h1>%s</h1>
  <p class="lead">%s</p>
</section>
""" % (h1, lead)


def page_index():
    lead = (
        "<strong>The answer first:</strong> Since <strong>2 August 2026</strong>, organisations that publish deepfakes, "
        "run emotion recognition or biometric categorisation on people, or publish unreviewed AI text on public-interest "
        "topics must disclose it, clearly and at first exposure. The EU offers free icons to do it. "
        + cite("S1", "S2", "S3")
    )
    cards = """
<div class="card-grid compact-cards">
  <div class="card">
    <h3><a href="article-50-deployer-checklist/">Article 50 deployer checklist</a></h3>
    <p>What you must disclose, the exceptions (art, law enforcement, human editorial review) and the dates.</p>
  </div>
  <div class="card">
    <h3><a href="deepfake-labelling-patterns/">Deepfake labelling patterns</a></h3>
    <p>Where to put the EU &ldquo;AI&rdquo; icon on images, video, audio and text, and the accessibility rules.</p>
  </div>
  <div class="card">
    <h3><a href="c2pa-watermarking-tools-compared/">C2PA and watermarking tools compared</a></h3>
    <p>Content Credentials, SynthID, Digimarc, Truepic and the open-source SDK: what each does; published prices only.</p>
  </div>
  <div class="card">
    <h3><a href="etsi-ts-104-275-explained/">ETSI TS 104 275 explained</a></h3>
    <p>ETSI&rsquo;s new deepfake-prevention spec for AI developers (V1.1.1, Sep 2026) in plain English.</p>
  </div>
</div>
"""
    dates = details(
        "The two dates people mix up",
        "<ul class=\"key-list\">"
        "<li><strong>2 Aug 2026.</strong> Article 50 applies and is enforceable. %s</li>"
        "<li><strong>2 Dec 2026.</strong> Only for <strong>providers</strong> of generative AI systems already on the market before 2 Aug 2026, and only for <strong>machine-readable marking</strong> (Art. 50(2)). Visible labels are not delayed. %s</li>"
        "</ul>" % (cite("S2"), cite("S2", "S7")),
    )
    why = details(
        "Why is this on a SaaS cost site?",
        "<p>Labelling is now part of what AI tools cost to run properly. This is a 30-day test section. The same rule as the calculators: the answer first, the explanation on demand, sources with dates.</p>",
    )
    checklist_preview = details(
        "What the 2-page checklist covers",
        "<p><strong>Do you need to disclose?</strong> If you publish deepfakes, run emotion recognition or biometric categorisation on people, or publish unreviewed AI text on public-interest topics, you must tell people, clearly, at first exposure, and accessibly.</p>"
        "<p><strong>Are you a deployer?</strong> Using AI in a professional capacity (business, trade, freelance, or regular economic benefit) means you continue. Purely personal, non-professional use only: deployer duties do not apply. Provider duties still do. %s</p>"
        "<ul class=\"key-list\">"
        "<li>Emotion recognition or biometric categorisation on people: inform them the system is operating (Art. 50(3)).</li>"
        "<li>Image, audio or video deepfake: disclose AI-generated or manipulated (Art. 50(4)).</li>"
        "<li>Published AI text informing the public on public-interest matters: disclose, unless human review plus editorial responsibility (Art. 50(4)).</li>"
        "</ul>"
        "<p><strong>Exceptions.</strong> Evidently artistic, satirical or fictional work: lighter, non-intrusive disclosure, still required. Authorised by law for criminal-offence detection or prosecution: no disclosure. Text only, human-reviewed, with a named person who holds editorial responsibility: no disclosure.</p>"
        "<p><strong>How to label it</strong> (EU Code of Practice, Section 2). Image: icon top-right, embedded, clear of overlays. Video: icon at the start, at regular intervals, and after every break. Audio: short spoken disclaimer at the start; reminders in long or live audio; visual icon too if a screen exists. Text: icon above the text, near the headline, or in the colophon. Art and satire: in credits, description, or next to the frame. Visible at first exposure, no hover or click needed. %s</p>"
        "<p><strong>Icon.</strong> Optional, free, no attribution. Basic &ldquo;AI&rdquo;, &ldquo;AI GENERATED&rdquo;, and &ldquo;AI MODIFIED&rdquo;, in black or white, solid or 50 %% transparent. Add a text label (&ldquo;generated&rdquo;, &ldquo;modified&rdquo;). EU testing found this improved results. %s</p>"
        "<p><strong>Accessibility.</strong> alt text or aria-label, plain language, high contrast, timed labels long enough, and a second layer that keyboard and screen-reader users can reach. %s</p>"
        "<p><strong>Evidence to keep.</strong> Who is responsible for labelling, and where the rule is written down. Real examples of labels in use. For the text exception: name, role and contact of the editorially responsible person, and how review works.</p>"
        % (cite("S5"), cite("S4"), cite("S3"), cite("S3")),
    )
    body = hero(
        "AI Act Article 50, for people who design and publish",
        lead,
    ) + """
<p class="legal-note">Not legal advice. Every claim links to an official source with the date we checked it.</p>
<h2>Start here</h2>
""" + cards + COMING + dates + why + checklist_preview + sources_section(["S1", "S2", "S3", "S4", "S5", "S7"])
    return body


def page_checklist():
    lead = (
        "<strong>The answer first:</strong> If your organisation <em>uses</em> AI (you are a &ldquo;deployer&rdquo;) and it "
        "(a) runs emotion recognition or biometric categorisation on people, (b) publishes deepfakes, or (c) publishes "
        "AI-written text meant to inform the public on matters of public interest without human editorial review, you must tell people. "
        "You must do it clearly, at the latest at first exposure, and in an accessible way. This applies from <strong>2 August 2026</strong>. "
        + cite("S1", "S2")
    )
    rows = [
        ["1", "Use an emotion recognition or biometric categorisation system on people?", "Inform the people exposed to it that the system is operating (and process personal data under the GDPR).", "Art. 50(3). " + cite("S1")],
        ["2", "Publish image, audio or video that is a deepfake made or changed with AI?", "Disclose that the content is AI-generated or manipulated.", "Art. 50(4), 1st subpara. " + cite("S1")],
        ["3", "Publish AI-generated or AI-changed text to inform the public on matters of public interest?", "Disclose that the text is AI-generated or manipulated, <strong>unless</strong> a human reviewed it and a person holds editorial responsibility.", "Art. 50(4), 2nd subpara. " + cite("S1")],
        ["4", "Show any of the above to people?", "Make the notice clear and distinguishable, <strong>at the latest at first interaction or exposure</strong>, and meet accessibility rules.", "Art. 50(5). " + cite("S1")],
        ["5", "Want a ready-made method?", "You <em>may</em> use the EU icons and the Code of Practice. Both are voluntary. The duty to disclose is not.", cite("S3", "S4")],
    ]
    checklist = table("The 5-line checklist", ["#", "Do you...", "Then you must...", "Source"], rows)
    who = details(
        "Who counts as a deployer?",
        "<p>A deployer is the organisation or person <em>using</em> an AI system under its authority. A natural person using AI for a <strong>purely personal, non-professional</strong> activity is outside the deployer duties. The Commission&rsquo;s guidelines give examples (deepfakes of your own household, students&rsquo; homework, personal social media posts). Anyone gaining an economic benefit on a regular basis, or acting in a business, trade or freelance capacity, counts as professional. %s</p>"
        "<p>The <em>provider</em> of the tool still has its own duties (for example machine-readable marking under Art. 50(2)), even when the user is a private person. %s</p>"
        % (cite("S5"), cite("S5")),
    )
    deepfake = details(
        "What is a deepfake here?",
        "<p>AI-generated or manipulated image, audio or video that resembles existing persons, objects, places, entities or events and would falsely appear to a person to be authentic or truthful. %s</p>" % cite("S3"),
    )
    public_interest = details(
        "What counts as text on matters of public interest?",
        "<p>The guidelines test three things: the text is <strong>published</strong> (open to a large, undefined audience, not a closed group or internal memo), it aims to <strong>inform the public</strong>, and it covers a <strong>matter of public interest</strong> (politics, public services, justice, public health, safety, environment, economic or scientific developments, etc.). %s</p>"
        "<p>Examples the Commission says <strong>are in scope</strong>: an AI summary of a town-council article on a newspaper site; AI-manipulated investor information in a listed company&rsquo;s report; an AI-written storm warning on a weather institute&rsquo;s social profile. Examples <strong>out of scope</strong>: AI-generated fantasy novels; ad copy and product descriptions (unless they make health, safety or sustainability claims); a chatbot news summary only the prompting user sees. %s</p>"
        % (cite("S5"), cite("S5")),
    )
    exceptions = table(
        "Exceptions (short version)",
        ["Exception", "Applies to", "What it means", "Source"],
        [
            ["<strong>Evidently artistic, creative, satirical, fictional or analogous work</strong>", "Deepfakes", "Not exempt, but a lighter duty: disclose that generated or manipulated content exists, in a way that does not hamper the display or enjoyment of the work.", "Art. 50(4). " + cite("S1", "S4")],
            ["<strong>Authorised by law to detect, prevent, investigate or prosecute criminal offences</strong>", "Deepfakes, public-interest text", "No disclosure duty.", "Art. 50(4). " + cite("S1")],
            ["<strong>Permitted by law to detect, prevent or investigate criminal offences</strong>", "Emotion recognition, biometric categorisation", "No information duty, subject to safeguards and Union law.", "Art. 50(3). " + cite("S1")],
            ["<strong>Human review or editorial control + someone holds editorial responsibility</strong>", "Public-interest text only", "No disclosure duty for that text. Does <strong>not</strong> apply to deepfakes.", "Art. 50(4). " + cite("S1")],
        ],
    )
    review = details(
        "What human review looks like in the Code of Practice",
        "<p>Signatories that rely on the editorial exception commit to a written policy that names the person with editorial responsibility (name, role, contact details) and describes the organisational measures and people who do the review before publication. They do not have to log each individual review. Media service providers already under editorial standards can use their existing procedures. %s</p>" % cite("S4"),
    )
    emotion = details(
        "A note on emotion recognition",
        "<p>Emotion recognition in the workplace and in education is prohibited under Art. 5(1)(f) (subject to the narrow exceptions in that article), so the Art. 50(3) notice is not a way to make it legal there. Outside those settings, the Commission notes emotion recognition systems are also high-risk, so Art. 50(3) applies alongside the high-risk rules. %s</p>" % cite("S5"),
    )
    dates = table(
        "Key dates",
        ["Date", "What happens", "Source"],
        [
            ["2 Aug 2026", "Article 50 transparency obligations apply and are enforceable.", cite("S2", "S6")],
            ["2 Dec 2026", "Deadline for <strong>providers</strong> of generative AI systems placed on the market <strong>before</strong> 2 Aug 2026 to meet <strong>Art. 50(2)</strong> (machine-readable marking). It does <strong>not</strong> move any deployer disclosure duty.", "Art. 111(4). " + cite("S7", "S2")],
        ],
    )
    why = details(
        "Why there is a December date",
        "<p>The Digital Omnibus on AI, Regulation (EU) 2026/1744 (published 24 July 2026), inserted Art. 111(4). Its recital 38 explains the four-month transition for providers already on the market. %s</p>" % cite("S8", "S7"),
    )
    fines = details(
        "What happens if you get it wrong",
        "<p>Breaches of Article 50 can lead to fines of up to EUR 15 000 000 or 3%% of total worldwide annual turnover, whichever is higher. Member States set the actual penalty rules and must consider the interests of SMEs. %s</p>" % cite("S9"),
    )
    body = hero("Article 50 checklist for deployers", lead) + """
<p class="legal-note">Not legal advice. This page summarises official EU sources. Check the text of the law for your own case.</p>
<h2>The 5-line checklist</h2>
""" + checklist + who + deepfake + public_interest + """
<h2>Exceptions (short version)</h2>
""" + exceptions + review + emotion + """
<h2>Key dates</h2>
""" + dates + why + fines + """
<h2>Next steps</h2>
<ul class="key-list">
  <li>See how to show the label: <a href="../deepfake-labelling-patterns/">Deepfake labelling patterns</a></li>
  <li>Machine-readable marking tools: <a href="../c2pa-watermarking-tools-compared/">C2PA and watermarking tools compared</a></li>
</ul>
""" + COMING + sources_section(["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9"])
    return body


def icon_src(filename):
    return "../../assets/eu-ai-icons/" + quote(filename)


def page_patterns():
    lead = (
        "<strong>The answer first:</strong> Put an &ldquo;AI&rdquo; mark where people see it <strong>before or as</strong> they first see the content: "
        "top-right of an image or video, at the start of a video and again after breaks, a short spoken disclaimer at the start of audio, "
        "and above or near the headline of text. The EU publishes free icons for this. Using them is optional; disclosing is not. "
        + cite("S3", "S4")
    )
    icons = """
<div class="eu-icon-row">
  <figure class="eu-icon-card">
    <img src="%s" alt="EU basic AI icon, black" width="140" height="70">
    <figcaption><strong>Basic icon.</strong> File name in the EU SVG download: LABEL_AI_black.svg. Use it when AI was involved, or you add your own text label or an interactive second layer. EU example: deepfake video with the label &ldquo;voices generated with&rdquo; followed by the icon.</figcaption>
  </figure>
  <figure class="eu-icon-card">
    <img src="%s" alt="EU fully AI-generated icon, black" width="140" height="70">
    <figcaption><strong>Fully AI-Generated.</strong> File name: LABEL_AI GENERATED_black.svg. Use it when the whole deepfake or text is AI-generated, no human-made elements or editorial control (apart from prompting). EU example: fully AI-generated videos of politicians; AI-generated news summaries.</figcaption>
  </figure>
  <figure class="eu-icon-card">
    <img src="%s" alt="EU partially AI-modified icon, black" width="140" height="70">
    <figcaption><strong>Partially AI-Modified.</strong> File name: LABEL_AI MODIFIED_black.svg. Use it when existing human-made content was partly changed with AI. EU example: a face swapped in a real photo; an empty-flat photo furnished with AI.</figcaption>
  </figure>
</div>
<p>Each icon also comes in white, and in black and white at 50%% transparency, as SVG and PNG. %s</p>
""" % (
        icon_src("LABEL_AI_black.svg"),
        icon_src("LABEL_AI GENERATED_black.svg"),
        icon_src("LABEL_AI MODIFIED_black.svg"),
        cite("S3", "S3a", "S3b"),
    )
    design = details(
        "Design rules behind the icons",
        "<ul class=\"key-list\">"
        "<li>The main element is the capitalised acronym <strong>&ldquo;AI&rdquo;</strong> in English (a national-language acronym is allowed where national language law requires it). Letters have the same height; keep proportions when resizing. %s</li>"
        "<li>You may add &ldquo;generated&rdquo; or &ldquo;modified&rdquo; next to the icon or in a second layer, and say <em>what</em> was changed (for example &ldquo;face altered&rdquo;). %s</li>"
        "<li>Size, contrast, colour and typography can vary as long as the label stays clear and recognisable. %s</li>"
        "<li>The EU says user testing showed better results across all measures when the icon was paired with a text label (for example &ldquo;modified&rdquo;). %s</li>"
        "</ul>" % (cite("S4"), cite("S4"), cite("S4"), cite("S3")),
    )
    licence = details(
        "Licence and usage terms",
        "<p>The icons are &ldquo;publicly available for everyone to use freely, without the need for attribution to the Commission or the AI Office.&rdquo; Code signatories must follow the placement specifications. Non-signatories using the icons must not present that as adherence to the Code. Using the icon does not by itself establish legal compliance. %s</p>"
        "<p>Official page: <a href=\"https://digital-strategy.ec.europa.eu/en/policies/eu-icons-labelling-ai-generated-content\">EU icons for labelling AI-generated content</a>.</p>"
        % cite("S3"),
    )
    sample = details(
        "Example HTML pattern (illustrative, not an official EU snippet)",
        "<pre class=\"ai-act-pre\"><code>%s</code></pre>"
        "<p>Position the icon top-right with clear spacing from other overlays. A CSS overlay is lost when the image is downloaded, so also bake the icon into the exported file. %s</p>"
        % (
            escape(
                '<figure class="ai-labelled">\n'
                '  <img src="campaign.jpg" alt="Product photo. Background generated with AI.">\n'
                '  <img class="ai-icon" src="/assets/eu-ai-icons/LABEL_AI MODIFIED_white.svg"\n'
                '       alt="AI-modified content" width="64">\n'
                '  <figcaption>Background modified with AI.</figcaption>\n'
                "</figure>"
            ),
            cite("S3"),
        ),
    )
    body = hero("Deepfake labelling patterns", lead) + """
<p class="legal-note">Not legal advice. The patterns below summarise Section 2 of the EU Code of Practice and the EU icons page.</p>
<h2>The official EU icons (what actually exists)</h2>
<p>The European Commission publishes <strong>three icons</strong>, each in <strong>four variants</strong> (black, white, black 50 %% transparent, white 50 %% transparent), as SVG and PNG downloads. %s</p>
""" % cite("S3") + icons + design + licence + """
<h2>Patterns by format</h2>
<h3>1. Image</h3>
<p><strong>Pattern:</strong> icon in the <strong>top-right corner</strong>, embedded in the image, clear of other overlays, readable on any background. %s</p>
<ul class="key-list">
  <li>Embed it in the file so it survives reshares and downloads. A UI overlay is acceptable only if it <em>appears to be on the content</em>. %s</li>
  <li>Prefer the labelled variant (&ldquo;AI GENERATED&rdquo; / &ldquo;AI MODIFIED&rdquo;) over the bare &ldquo;AI&rdquo;. %s</li>
</ul>
<h3>2. Video</h3>
<p><strong>Pattern:</strong> icon <strong>at the start</strong>, where possible <strong>at regular intervals</strong>, and <strong>at minimum after every interruption</strong> (for example ad breaks). %s</p>
<ul class="key-list">
  <li>If only a segment is a deepfake, the Code encourages showing the icon during that segment. %s</li>
  <li>Audio cues alone are not enough for visual deepfakes; they can only be added on top of a visual label. %s</li>
  <li>Live streams: people join late, so repeat the icon. %s</li>
</ul>
<h3>3. Audio-only</h3>
<p><strong>Pattern:</strong> a <strong>short spoken disclaimer at the beginning</strong>, in plain language (same language as the content, or English). %s</p>
<ul class="key-list">
  <li>Long-form or live audio: add reminders at regular intervals and after interruptions. %s</li>
  <li>If a screen is available (car display, phone), <strong>also</strong> show the visual icon. %s</li>
  <li>An earcon (sound logo) is allowed only with awareness measures, pending a common EU audio solution. %s</li>
</ul>
<h3>4. Published text (public-interest topics)</h3>
<p><strong>Pattern:</strong> icon <strong>above or at the top of the text</strong>, near the headline, or in the colophon at the start. You may label only the AI-generated part. %s</p>
<ul class="key-list">
  <li>Very short text (single words, brief phrases): a contextual notice in the UI is acceptable, for example an indicator next to the output. %s</li>
  <li>No label needed if a human reviewed it and someone holds editorial responsibility. %s</li>
</ul>
<h3>5. Artistic, satirical, fictional works</h3>
<p><strong>Pattern:</strong> a lighter disclosure that does not spoil the work: in credits, description, accompanying notes, or adjacent to the frame in the UI; for exhibitions, at the point of entry or on the leaflet or ticket. %s</p>
<h3>6. Internal-only content (training videos and similar)</h3>
<p><strong>Pattern:</strong> disclosure may sit in the UI or physical setting <strong>before</strong> exposure, if it is clear to the people involved. %s</p>
<h2>Accessibility checklist for the label</h2>
<ul class="key-list">
  <li>Icon is large enough to see. %s</li>
  <li>Plain-language text, no jargon or abbreviations except &ldquo;AI&rdquo;. %s</li>
  <li>alt text or aria-label saying the content is AI-generated or manipulated. %s</li>
  <li>Timed labels stay up long enough for people with cognitive or processing difficulties. %s</li>
  <li>Second layer (hover or click info) is signalled by the icon and keyboard and screen-reader navigable. %s</li>
  <li>High contrast; works for colour-vision deficiencies. %s</li>
</ul>
""" % (
        cite("S4"),
        cite("S3", "S4"),
        cite("S3"),
        cite("S4"),
        cite("S4"),
        cite("S4"),
        cite("S4"),
        cite("S4"),
        cite("S4"),
        cite("S4"),
        cite("S4"),
        cite("S4"),
        cite("S4"),
        cite("S1"),
        cite("S4"),
        cite("S4"),
        cite("S3"),
        cite("S3"),
        cite("S3"),
        cite("S3"),
        cite("S3"),
        cite("S4"),
    ) + sample + """
<h2>Common mistakes</h2>
<ul class="key-list">
  <li>Label only in the footer or &ldquo;About&rdquo; page: not at first exposure. %s</li>
  <li>Label only on hover: the Code says recognition should not require user action. %s</li>
  <li>Label only in metadata: machine-readable marks are the <strong>provider&rsquo;s</strong> Art. 50(2) duty; deployers still need a visible disclosure. %s</li>
</ul>
<p>Related: <a href="../article-50-deployer-checklist/">Article 50 deployer checklist</a> &middot; <a href="../c2pa-watermarking-tools-compared/">C2PA and watermarking tools</a></p>
""" % (cite("S1"), cite("S4"), cite("S1")) + sources_section(["S1", "S3", "S3a", "S3b", "S4"])
    return body


def page_tools():
    lead = (
        "<strong>The answer first:</strong> Under the EU Code of Practice, providers of generative AI are expected to use <strong>two layers</strong> of machine-readable marking: "
        "<strong>digitally signed metadata</strong> (what C2PA / Content Credentials does) <strong>plus an imperceptible watermark</strong> (what SynthID or Digimarc do). "
        "Free-form text cannot carry metadata, so a watermark alone is considered sufficient there. Neither layer replaces the visible label a deployer must show. "
        + cite("S4", "S1")
    )
    rows = [
        ["<strong>C2PA / Content Credentials</strong>", "Open technical standard for provenance (&ldquo;Content Credentials&rdquo;). Latest spec listed: 2.5.", "Signed metadata (plus soft-binding API for watermarks)", "Standard, format support depends on implementation", "Open standard", "n/a (standard)", cite("T1", "T2")],
        ["<strong>CAI open-source SDK</strong> (c2pa-rs, c2patool, c2pa-web, c2pa-node, Python, Swift, Android, C/C++)", "Libraries to read, validate, create and sign C2PA manifests", "Signed metadata", "Supported formats vary by library and release", "Open source", "Free to use; you need your own signing certificate", cite("T3")],
        ["<strong>Adobe Content Authenticity (Beta)</strong>", "Free web app to apply and inspect Content Credentials; Chrome extension to view them", "Metadata + invisible watermark + fingerprint (Adobe states all three)", "Apply: JPG/PNG, up to 50 files, 20 MB each", "Free (public beta)", "Free", cite("T4", "T5")],
        ["<strong>Google SynthID</strong>", "Google DeepMind imperceptible watermark + public detector", "Watermark", "Images, video, audio (detector); text via open-source SynthID Text", "SynthID Text open-sourced (Hugging Face Transformers v4.46.0+)", "Detector: unknown / not stated; SynthID Text: open source", cite("T6", "T7")],
        ["<strong>Digimarc (C2PA solution)</strong>", "Imperceptible watermark that links content to its C2PA Content Credentials, even after metadata is stripped", "Watermark linked to C2PA", "Images, video, audio", "Commercial", "Unknown (demo / contact sales)", cite("T8")],
        ["<strong>Truepic (Lens / Vision)</strong>", "Authenticated capture: photos and videos signed at capture with Truepic PKI; reports content credentials (C2PA)", "Signed metadata at capture", "Photos, video", "Commercial", "Inspection product: from $1,000/mo (Flex). This is for inspections, not AI labelling. C2PA-only pricing unknown.", cite("T9", "T10", "T11")],
    ]
    comparison = table(
        "Comparison of marking tools. Published prices only. Unknown means unknown.",
        ["Tool", "What it is", "Layer", "Media (as stated)", "Open / free?", "Published price", "Source"],
        rows,
    )
    who = details(
        "Which do I need? (provider vs deployer)",
        "<ul class=\"key-list\">"
        "<li><strong>You build or sell a generative AI system (provider):</strong> Art. 50(2) applies to you. The Code expects signed metadata <strong>and</strong> a watermark for audio, image, video and containerised text. Systems already on the market before 2 Aug 2026 have until <strong>2 Dec 2026</strong>. %s</li>"
        "<li><strong>You only use AI to make content (deployer):</strong> your legal duty is the <strong>visible</strong> disclosure under Art. 50(4). C2PA and watermarks are useful (they survive sharing and back up your label), but they are not the label. See <a href=\"../deepfake-labelling-patterns/\">labelling patterns</a>. %s</li>"
        "</ul>" % (cite("S1", "S4", "S7"), cite("S1")),
    )
    c2pa = details(
        "C2PA / Content Credentials, details",
        "<ul class=\"key-list\">"
        "<li>C2PA describes itself as &ldquo;an open technical standard for publishers, creators and consumers to establish the origin and edits of digital content. It&rsquo;s called Content Credentials.&rdquo; %s</li>"
        "<li>The spec index lists versions up to <strong>2.5</strong>, plus a Soft Binding API (the hook that lets a watermark point back to a manifest). %s</li>"
        "<li>The &ldquo;cr&rdquo; pin is a C2PA trademark used by conforming products. %s</li>"
        "<li>The C2PA is a standards body under the Linux Foundation&rsquo;s Joint Development Foundation; the CAI is an Adobe-led consortium that maintains the open-source SDK. %s</li>"
        "</ul>" % (cite("T1"), cite("T2"), cite("T3"), cite("T3")),
    )
    adobe = details(
        "Adobe Content Authenticity, details",
        "<ul class=\"key-list\">"
        "<li>Free web app at contentauthenticity.adobe.com, in public beta. %s</li>"
        "<li>Upload up to 50 JPG/PNG files at a time, max 20 MB each; credentials cannot be edited after applying. %s</li>"
        "<li>Adobe states credentials are stored in the file and in Adobe&rsquo;s public Content Credentials cloud, linked through embedded metadata, invisible watermarking and digital fingerprinting. %s</li>"
        "<li>Support for video and audio was announced as &ldquo;coming soon&rdquo; in April 2025; we did not find a confirmation of availability. <strong>Unknown.</strong> %s</li>"
        "</ul>" % (cite("T4", "T5"), cite("T4"), cite("T4"), cite("T5")),
    )
    synth = details(
        "Google SynthID, details",
        "<ul class=\"key-list\">"
        "<li>Google says SynthID has watermarked over 180 billion images and videos and 240,000 years of audio, and that the SynthID Detector became available globally in English on 7 Oct 2026 (post updated 29 Oct 2026). %s</li>"
        "<li>The detector checks images, video and audio made with AI from Google or partners named as OpenAI, NVIDIA, Kakao and Apple. %s</li>"
        "<li>SynthID Text is open source; detection is probabilistic (watermarked / not watermarked / uncertain). Thorough rewriting or translation can greatly reduce detector confidence. %s</li>"
        "<li>Pricing for the detector or for third-party image, audio or video watermarking: <strong>unknown</strong>.</li>"
        "</ul>" % (cite("T6"), cite("T6"), cite("T7")),
    )
    digimarc = details(
        "Digimarc, details",
        "<ul class=\"key-list\">"
        "<li>Digimarc says it built &ldquo;the first implementation of invisible watermarking for C2PA purposes&rdquo; and that its watermark keeps a link to Content Credentials even if media is manipulated or stripped of metadata. %s</li>"
        "<li>It positions the product for the EU AI Act among other regulations. %s</li>"
        "<li>Pricing: <strong>unknown</strong> (request a demo). %s</li>"
        "</ul>" % (cite("T8"), cite("T8"), cite("T8")),
    )
    truepic = details(
        "Truepic, details",
        "<ul class=\"key-list\">"
        "<li>Truepic&rsquo;s current site focuses on authenticated photo and video inspections (insurance, lending, warranty). %s</li>"
        "<li>Its Lens API docs describe signing captures with a key and certificate from Truepic&rsquo;s Certificate Authority and returning a JSON report of the content credentials; sample output shows C2PA manifest data. %s</li>"
        "<li>Public pricing exists for the inspection product (Flex: $1,000/month minimum; Standard shown at $1,450/month for a selected tier). %s Truepic is a capture-provenance tool, not an AI-output labelling tool.</li>"
        "</ul>" % (cite("T9"), cite("T10"), cite("T11")),
    )
    body = hero("C2PA and watermarking tools compared", lead) + """
<p class="legal-note">Not legal advice. Prices are shown only where the vendor publishes them. &ldquo;Unknown&rdquo; means we could not find it on an official page.</p>
<h2>Comparison table</h2>
""" + comparison + who + c2pa + adobe + synth + digimarc + truepic + """
<h2>What none of these do</h2>
<ul class="key-list">
  <li>They do not decide whether your content is a &ldquo;deepfake&rdquo; or &ldquo;public-interest text&rdquo;. That is a judgment under Art. 50(4). %s</li>
  <li>Watermark detection is probabilistic; metadata can be stripped. That is why the Code asks for layers. %s</li>
</ul>
<p>Related: <a href="../article-50-deployer-checklist/">Article 50 deployer checklist</a> &middot; <a href="../etsi-ts-104-275-explained/">ETSI TS 104 275 explained</a></p>
""" % (cite("S1"), cite("S4", "T7")) + sources_section(["S1", "S4", "S7", "T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10", "T11"])
    return body


def page_etsi():
    lead = (
        "<strong>The answer first:</strong> ETSI TS 104 275 is a free technical specification from ETSI&rsquo;s committee on Securing AI. "
        "It tells <strong>developers and operators of generative AI</strong> how to reduce the chance their systems produce harmful deepfakes: "
        "risk assessment before release, human oversight, labelling and filters in the UI, training, and documented evidence, with pass/fail test cases. "
        "It is <strong>not</strong> a harmonised standard under the AI Act and does not by itself prove Article 50 compliance. "
        + cite("E1", "E2", "E3")
    )
    facts = table(
        "ETSI TS 104 275 fact box",
        ["Item", "Detail"],
        [
            ["Full title", "Securing Artificial Intelligence (SAI); Application of Baseline Cyber Security Requirements for AI Models and Systems principles to Generative AI; Preventing Harm from Deepfakes. " + cite("E1")],
            ["Number / version", "ETSI TS 104 275 <strong>V1.1.1 (2026-09)</strong>. " + cite("E1")],
            ["Work item", "DTS/SAI-0031, Technical Committee SAI. " + cite("E1", "E3")],
            ["Published", "Cover date and publication milestone <strong>29 Sep 2026</strong>. " + cite("E3")],
            ["Announced", "ETSI press release dated <strong>29 Oct 2026</strong>. " + cite("E2")],
            ["Harmonised standard?", "<strong>No</strong> (ETSI work programme). " + cite("E3")],
            ["Length", "26 pages (PDF). " + cite("E1")],
            ["Price", "Free PDF download from ETSI. " + cite("E1")],
            ["Builds on", "ETSI EN 304 223 (V2.1.1), Baseline Cyber Security Requirements for AI Models and Systems. " + cite("E1")],
        ],
    )
    dates = details(
        "Why two dates?",
        "<p>The ETSI work programme lists the publication milestone and cover date as 29 Sep 2026, and the PDF metadata is dated the same day. ETSI&rsquo;s press release &ldquo;ETSI unveils new standard to reduce production of harmful deepfakes&rdquo; is dated 29 Oct 2026. If you see &ldquo;released 29 October&rdquo;, that is the announcement; the document itself is dated September 2026. %s</p>" % cite("E1", "E2", "E3"),
    )
    annex_c = details(
        "Annex C: test cases with pass/fail",
        "<p>Annex C (normative) gives a test purpose, method and pass/fail verdict per extension provision. Example: for the UI provision, a <strong>pass</strong> needs design and implementation evidence of content filters, clear AI-content labelling and user information on limits, <em>and</em> test results showing they work. For training, a <strong>pass</strong> needs GenAI security topics in training material reviewed within the last 12 months. %s</p>" % cite("E1"),
    )
    act = details(
        "How it relates to the EU AI Act",
        "<ul class=\"key-list\">"
        "<li>ETSI says the TS &ldquo;supports objectives laid out in the EU AI Act, extending security beyond systems classified as high-risk.&rdquo; %s</li>"
        "<li>The ETSI work programme marks it as <strong>not</strong> a harmonised standard. %s So it does not give a presumption of conformity.</li>"
        "<li>For Article 50 labelling and marking, the Commission&rsquo;s recognised tool is the <strong>Code of Practice on Transparency of AI-generated Content</strong>, which the Commission and AI Board assessed as adequate. %s</li>"
        "<li>The TS mentions labelling only at a high level (&ldquo;clearly labelling AI-generated content&rdquo;); it does not specify icons, placement or C2PA. For those, see the Code and the EU icons. %s</li>"
        "</ul>" % (cite("E2"), cite("E3"), cite("S4", "S10"), cite("E1", "S3")),
    )
    annex_ab = details(
        "Annexes A and B",
        "<p>Annex A (informative) gives an overview of detection and prevention of GenAI deepfakes, including reporting and removal. Annex B (informative) maps GenAI to trustworthy-AI concepts. %s</p>" % cite("E1"),
    )
    phases = table(
        "The structure: 13 principles in 5 lifecycle phases. Source: ETSI TS 104 275, clause 5 and table of contents.",
        ["Phase", "Principles", "Deepfake-specific additions (summarised)"],
        [
            ["Secure design", "1 Awareness. 2 Design for security. 3 Threats and risks. 4 Human responsibility", "Training resources on deepfake risks (5.1.1-1). <strong>UI shall encourage responsible use, for example content filters, clear labelling of AI-generated content, telling users about reliability limits</strong> (5.1.2-1). Risk assessment and mitigations before deployment (5.1.3-2). Human oversight and post-deployment monitoring (5.1.4-2)."],
            ["Secure development", "5 Assets. 6 Infrastructure. 7 Supply chain. 8 Document data, models and prompts. 9 Testing", "Informed consent and opt-in/opt-out if a system trains on users&rsquo; works (5.2.1-1). Developer confirms training data was legally accessed and/or licensed (5.2.4-1). Red-teaming suggested, for example the same prompt in several languages (note to 5.2.5)."],
            ["Secure deployment", "10 Communication with end users", "A risk communication policy, able to share information with for example a national market surveillance authority under the AI Act (5.3.1-1)."],
            ["Secure maintenance", "11 Updates. 12 Monitoring", "No new provisions; notes on informing users and human oversight."],
            ["Secure end of life", "13 Data and model disposal", "No new provisions."],
        ],
    )
    body = hero("ETSI TS 104 275 explained", lead) + """
<p class="legal-note">Not legal advice.</p>
<h2>Fact box</h2>
""" + facts + dates + """
<h2>Scope in one sentence</h2>
<p>A deepfake-focused application of EN 304 223 to generative AI, covering misinformation, disinformation, loss of confidentiality, copyright, IPR and LLM training and source material, with more prescriptive provisions where needed. %s</p>
<h2>Who it is for</h2>
<p>Mainly <strong>developers</strong> and <strong>system operators</strong> of generative AI (some provisions also name data custodians). It is not written for people who only publish AI content, though its UI provision is relevant to designers. %s</p>
<h2>The structure: 13 principles in 5 lifecycle phases</h2>
""" % (cite("E1"), cite("E1")) + phases + "<p>%s</p>" % cite("E1") + annex_c + act + annex_ab + """
<h2>What a designer can take from it</h2>
<ol class="key-list">
  <li>Labelling is a <strong>design requirement</strong>, not a legal footnote (5.1.2-1).</li>
  <li>Keep evidence: design docs and test results showing the label and filters work (Annex C).</li>
  <li>Tell users what the system can&rsquo;t do reliably (5.1.2-1).</li>
</ol>
<p>Related: <a href="../deepfake-labelling-patterns/">Labelling patterns</a> &middot; <a href="../c2pa-watermarking-tools-compared/">C2PA and watermarking tools</a></p>
""" + sources_section(["E1", "E2", "E3", "S3", "S4", "S10"])
    return body


PAGES = [
    (
        "ai-act/index.html",
        "EU AI Act Article 50: labelling AI content, explained for designers",
        "Article 50 of the EU AI Act in plain English: who must label AI content, how to show the EU icons, which marking tools exist, and what ETSI TS 104 275 adds. Sources on every claim.",
        "/ai-act/",
        page_index,
    ),
    (
        "ai-act/article-50-deployer-checklist/index.html",
        "EU AI Act Article 50 checklist for deployers (2026)",
        "What deployers must disclose under Article 50: emotion recognition, biometric categorisation, deepfakes and AI text on public-interest topics. Exceptions and dates, with sources.",
        "/ai-act/article-50-deployer-checklist/",
        page_checklist,
    ),
    (
        "ai-act/deepfake-labelling-patterns/index.html",
        "Deepfake labelling patterns with the EU AI icons (UI, video, audio, text)",
        "How to place the EU's official AI icons on images, video, audio and text under AI Act Article 50(4). Placement rules, accessibility and licence, with sources.",
        "/ai-act/deepfake-labelling-patterns/",
        page_patterns,
    ),
    (
        "ai-act/c2pa-watermarking-tools-compared/index.html",
        "C2PA, Content Credentials and AI watermarking tools compared (2026)",
        "C2PA / Content Credentials, CAI open-source SDK, Adobe Content Authenticity, Google SynthID, Digimarc and Truepic: what each does, media types, pricing as published. Unknown means unknown.",
        "/ai-act/c2pa-watermarking-tools-compared/",
        page_tools,
    ),
    (
        "ai-act/etsi-ts-104-275-explained/index.html",
        "ETSI TS 104 275 explained: preventing harm from deepfakes (V1.1.1)",
        "ETSI TS 104 275 V1.1.1 in plain English: who it is for, the 13 principles, what it adds for deepfakes, how it relates to the EU AI Act. Free PDF from ETSI.",
        "/ai-act/etsi-ts-104-275-explained/",
        page_etsi,
    ),
]


def copy_to_root(rel):
    src = os.path.join(PUBLIC_DIR, rel)
    dst = os.path.join(BASE_DIR, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src, dst)


def build():
    for rel, title, description, canonical, builder in PAGES:
        render_page(
            rel,
            title,
            description,
            canonical,
            builder(),
            published_date="2026-10-30",
            show_affiliate_note=False,
        )
        copy_to_root(rel)


if __name__ == "__main__":
    build()
