#!/usr/bin/env python3
"""
Generates the four legal pages from one template so their chrome, styling and
"needs review" banners stay identical.

Run:  python3 build-legal.py       (from inside the site folder)

Everything wrapped in [[ ]] becomes a highlighted placeholder on the page —
those are the details only Tharu can supply, and they are deliberately loud so
nobody publishes the site with them still in.
"""
import re, pathlib

UPDATED = "12 September 2026"

CSS = """
:root{--deep:#1a2c22;--ocean:#2f4b3a;--teal:#4f7457;--leaf:#5f855f;
 --ink:#1e2a22;--muted:#5c6b60;--line:rgba(47,75,58,.16);--warn:#8a4b2f;
 --grad:linear-gradient(120deg,var(--ocean),var(--teal) 55%,var(--leaf))}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Poppins',sans-serif;color:var(--ink);background:#fcfdfa;-webkit-font-smoothing:antialiased}
a{color:var(--teal)}
.wrap{width:min(820px,92vw);margin:0 auto}
.skip{position:absolute;left:-9999px;top:0;background:#fff;color:var(--ink);padding:.7rem 1rem;z-index:200;border-radius:0 0 8px 0}
.skip:focus{left:0}
header{background:var(--deep);padding:1rem 0;position:sticky;top:0;z-index:50}
header .wrap{width:min(1180px,92vw)}
.nav{display:flex;align-items:center;gap:1rem}
.logo{display:flex;align-items:center;gap:.5rem;font-family:'Pacifico',cursive;
 font-size:1.3rem;color:#fff;text-decoration:none;padding-top:.15rem}
.logo img{height:56px;width:auto;object-fit:contain}
.back{margin-left:auto;display:inline-flex;align-items:center;gap:.5rem;color:rgba(255,255,255,.85);
 font-size:.7rem;letter-spacing:.14em;text-transform:uppercase;font-weight:500;text-decoration:none}
.back:hover{color:#fff}
main{padding:3.2rem 0 5rem}
h1{font-weight:800;text-transform:uppercase;font-size:clamp(1.8rem,4vw,2.6rem);
 line-height:1.05;letter-spacing:-.03em;margin-bottom:.6rem}
.meta{font-size:.78rem;color:var(--muted);margin-bottom:2rem}
h2{font-size:1.02rem;font-weight:700;margin:2.6rem 0 .7rem;letter-spacing:-.01em}
h3{font-size:.88rem;font-weight:600;margin:1.5rem 0 .4rem}
p,li{font-size:.93rem;font-weight:300;line-height:1.85;color:#3a473e}
p{margin-bottom:.9rem}
ul,ol{margin:0 0 1rem 1.2rem}
li{margin-bottom:.35rem}
strong,b{font-weight:600;color:var(--ink)}
table{width:100%;border-collapse:collapse;margin:1rem 0 1.4rem;font-size:.86rem}
th,td{text-align:left;padding:.6rem .7rem;border:1px solid var(--line);vertical-align:top;font-weight:300;line-height:1.6}
th{background:#f1f5ef;font-weight:600;font-size:.78rem}
.draft{background:#fdf3ec;border:1px solid #e8c9b0;border-left:4px solid var(--warn);
 border-radius:10px;padding:1.1rem 1.2rem;margin-bottom:2.2rem}
.draft p{margin:0;font-size:.86rem;color:#6f3d26}
.draft p+p{margin-top:.6rem}
.fill{background:#fff3cd;border-bottom:2px solid #d9a441;padding:0 .25rem;
 font-weight:600;color:#6b4e0e;white-space:nowrap}
.toc{background:#f4f7f2;border:1px solid var(--line);border-radius:12px;padding:1.1rem 1.3rem;margin-bottom:2.4rem}
.toc ol{margin:0 0 0 1.1rem}
.toc li{margin-bottom:.2rem;font-size:.86rem}
footer{background:#16241c;color:rgba(255,255,255,.5);font-size:.78rem;padding:2rem 0;margin-top:3rem}
footer .wrap{display:flex;gap:1.2rem;flex-wrap:wrap;justify-content:space-between;align-items:center}
footer a{color:rgba(255,255,255,.72);text-decoration:none}
footer a:hover{color:#fff;text-decoration:underline}
footer nav{display:flex;gap:1.1rem;flex-wrap:wrap}
:focus-visible{outline:3px solid var(--leaf);outline-offset:2px}
"""

FOOT = """<footer>
  <div class="wrap">
    <span>&copy; 2026 TripzaCeylon. All rights reserved.</span>
    <nav aria-label="Legal">
      <a href="privacy.html">Privacy</a>
      <a href="cookies.html">Cookies</a>
      <a href="terms.html">Terms</a>
      <a href="booking.html">Booking &amp; refunds</a>
      <a href="index.html">Home</a>
    </nav>
  </div>
</footer>"""


def page(slug, title, blurb, body, toc):
    fill = lambda s: re.sub(r'\[\[(.+?)\]\]', r'<span class="fill">\1</span>', s)
    items = "\n".join(f"      <li><a href=\"#{i}\">{n}</a></li>" for i, n in toc)
    html = f"""<!DOCTYPE html>
<!--
  ============================================================================
  TripzaCeylon — {title}
  ============================================================================
  GENERATED FILE. Edit build-legal.py and re-run it, or edit here and stop
  running the generator — but don't do both and expect them to agree.

  THIS IS A DRAFT, NOT LEGAL ADVICE. It was written to be honest and specific
  about what this site actually does, which is a better starting point than a
  generic template, but it has not been reviewed by a lawyer. Everything
  highlighted in yellow is a detail only you can supply.
  ============================================================================
-->
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — TripzaCeylon</title>
<meta name="description" content="{blurb}">
<link rel="icon" type="image/png" href="favicon.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Pacifico&family=Poppins:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<header>
  <div class="wrap nav">
    <a href="index.html" class="logo">
      <img src="logo.png" alt="" width="45" height="56"> TripzaCeylon
    </a>
    <a href="index.html" class="back">&larr; Back to site</a>
  </div>
</header>

<main id="main">
  <div class="wrap">
    <h1>{title}</h1>
    <p class="meta">Last updated {UPDATED}</p>

    <div class="draft" role="note">
      <p><strong>Draft — not yet reviewed by a lawyer.</strong> This was written
      to describe accurately what this website really does, but it is not legal
      advice and it has not been checked by anyone qualified in Sri Lankan law.</p>
      <p>Every <span class="fill">highlighted item</span> is a detail only
      TripzaCeylon can supply. Do not publish this page until they are filled in
      and a lawyer has read it.</p>
    </div>

    <nav class="toc" aria-label="On this page">
      <ol>
{items}
      </ol>
    </nav>

{fill(body)}
  </div>
</main>

{FOOT}
</body>
</html>
"""
    pathlib.Path(slug).write_text(html)
    return slug


# ═══════════════════════════════════════════════════════════════ PRIVACY ═══
privacy_toc = [("who", "Who we are"), ("what", "What we collect"),
               ("why", "Why we collect it, and our legal basis"),
               ("who-sees", "Who else sees it"), ("where", "Where it goes"),
               ("keep", "How long we keep it"), ("rights", "Your rights"),
               ("security", "Security"), ("children", "Children"),
               ("changes", "Changes"), ("contact", "Contact and complaints")]

privacy_body = """
<h2 id="who">1. Who we are</h2>
<p>TripzaCeylon is a travel planning business based in Sri Lanka. For the purposes
of data protection law we are the <strong>controller</strong> of the personal data
described here — meaning we decide what is collected and why.</p>
<table>
  <tr><th>Trading name</th><td>TripzaCeylon</td></tr>
  <tr><th>Registered company name</th><td>[[registered company name]]</td></tr>
  <tr><th>Company registration number</th><td>[[registration number]]</td></tr>
  <tr><th>Registered address</th><td>[[registered address]]</td></tr>
  <tr><th>SLTDA registration number</th><td>[[SLTDA number, or delete this row]]</td></tr>
  <tr><th>Contact</th><td><a href="mailto:TripzaCeylon@gmail.com">TripzaCeylon@gmail.com</a> &middot; 076 167 4855</td></tr>
</table>

<h2 id="what">2. What we collect</h2>
<p>Only what you type into the enquiry form. There is no account to create, no
newsletter sign-up that runs without you, and no tracking of what you browse.</p>
<ul>
  <li><strong>Your name and email address</strong> — so we can reply.</li>
  <li><strong>Your trip preferences</strong> — the package or route you chose,
    roughly when you want to travel, how many of you there are, trip length,
    budget band, and the interests you ticked.</li>
  <li><strong>Anything you write in the notes box.</strong> Please don't put
    anything sensitive there — passport numbers, card details, health or medical
    information. If we need those later we will ask for them properly and
    securely, never through this form.</li>
</ul>
<p>We do <strong>not</strong> collect payment details on this website, and we do not
ask for your date of birth, passport details or address at enquiry stage. If you
go on to book, we will tell you separately what is needed and why.</p>
<p>Our website sets <strong>no cookies</strong> and runs <strong>no analytics</strong>.
See our <a href="cookies.html">Cookie Policy</a> for the detail.</p>

<h2 id="why">3. Why we collect it, and our legal basis</h2>
<table>
  <tr><th>What for</th><th>Legal basis</th></tr>
  <tr><td>Replying to your enquiry and preparing a quote</td>
      <td>Steps taken at your request before entering a contract</td></tr>
  <tr><td>Keeping a record of enquiries so we can pick up a conversation later</td>
      <td>Our legitimate interest in running the business, balanced against your privacy</td></tr>
  <tr><td>Sending you travel offers or news, if you ask for that</td>
      <td>Your consent, which you can withdraw at any time</td></tr>
</table>
<p>We do not sell your data, we do not share it with advertisers, and we do not
use it to build a profile of you.</p>

<h2 id="who-sees">4. Who else sees it</h2>
<p>A handful of service providers process enquiry data on our behalf. We have
listed them by name because you are entitled to know who is holding your details.</p>
<table>
  <tr><th>Who</th><th>What they do</th><th>Where</th></tr>
  <tr><td>Supabase</td><td>Stores the enquiry in our database</td><td>[[your Supabase region — Singapore if you followed the setup guide]]</td></tr>
  <tr><td>Web3Forms</td><td>Delivers the enquiry to our email</td><td>Outside Sri Lanka</td></tr>
  <tr><td>Google (Gmail)</td><td>Our email inbox</td><td>Outside Sri Lanka</td></tr>
  <tr><td>GitHub Pages</td><td>Hosts this website; sees your IP address as any web server does</td><td>Outside Sri Lanka</td></tr>
  <tr><td>Google Fonts, Unsplash</td><td>Serve the fonts and photographs on these pages, so they receive your IP address</td><td>Outside Sri Lanka</td></tr>
</table>
<p>We may also share your details with the specific hotels, guides and transport
operators needed to arrange a trip you have asked us to arrange — but only those,
only what they need, and only once you are actually booking.</p>
<p>We will disclose information if the law requires it, for example a valid
request from a court or a regulator.</p>

<h2 id="where">5. Where it goes</h2>
<p>Some of the providers above store data outside Sri Lanka. Where Sri Lankan or
other applicable law requires a safeguard for that transfer, we rely on the
provider's standard contractual terms. If you would like to know more about a
particular provider, ask us.</p>

<h2 id="keep">6. How long we keep it</h2>
<ul>
  <li><strong>Enquiries that don't turn into a trip:</strong> [[choose a period — 24 months is a common answer]], then deleted.</li>
  <li><strong>Enquiries that become bookings:</strong> kept for as long as we need
    them for the trip, and afterwards for [[period — check with an accountant; Sri Lankan tax record-keeping rules will drive this]].</li>
  <li><strong>Email:</strong> our inbox holds a copy of each enquiry. We clear these on the same schedule.</li>
</ul>

<h2 id="rights">7. Your rights</h2>
<p>Sri Lanka's <strong>Personal Data Protection Act No. 9 of 2022</strong> gives
you rights over your personal data. Its obligations on businesses are being brought
into force in stages. We intend to meet them in full, and we will honour these
requests now regardless of which sections are currently in force:</p>
<ul>
  <li>ask what we hold about you, and get a copy</li>
  <li>have anything inaccurate corrected</li>
  <li>ask us to delete it</li>
  <li>object to our using it, or ask us to restrict how we use it</li>
  <li>withdraw consent for marketing at any time, without it affecting anything else</li>
</ul>
<p>If you are in the United Kingdom or the European Economic Area, the UK GDPR or
the GDPR may also apply to us because we offer services to travellers there. In
that case you have the equivalent rights under those laws, including the right to
data portability and the right to complain to your national data protection
authority.</p>
<p>To exercise any of these, email
<a href="mailto:TripzaCeylon@gmail.com">TripzaCeylon@gmail.com</a>. We will reply
within 30 days. We may ask you to confirm who you are first, so that we don't hand
your details to somebody else.</p>

<h2 id="security">8. Security</h2>
<p>Enquiries are stored in a database with access rules that allow the website to
add an enquiry but not to read any. Reading them requires a staff account with an
individual password. The site is served over HTTPS.</p>
<p>No system is perfectly secure, and we will not pretend otherwise. If a breach
ever affects your data we will tell you and the relevant authority as the law
requires.</p>

<h2 id="children">9. Children</h2>
<p>This site is meant for adults planning travel. We don't knowingly collect
personal data from children. If a trip involves children, we only need their
details from the adult booking, at booking stage — never through this form.</p>

<h2 id="changes">10. Changes</h2>
<p>If we change this policy we will update the date at the top. If the change is
significant we will say so on the home page.</p>

<h2 id="contact">11. Contact and complaints</h2>
<p>Questions or complaints about how we handle your data:
<a href="mailto:TripzaCeylon@gmail.com">TripzaCeylon@gmail.com</a>.</p>
<p>If you are not satisfied with our answer, you can complain to the Data
Protection Authority established under the Personal Data Protection Act in Sri
Lanka, or to your own national data protection authority if you are in the UK or
the EEA.</p>
"""

# ═══════════════════════════════════════════════════════════════ COOKIES ═══
cookies_toc = [("short", "The short version"), ("cookies", "Cookies we set"),
               ("storage", "Browser storage"), ("third", "Third parties your browser contacts"),
               ("consent", "Why there is no consent banner"),
               ("control", "How to control all of this")]

cookies_body = """
<h2 id="short">1. The short version</h2>
<p><strong>This website sets no cookies.</strong> There is no advertising, no
analytics, no Google Analytics, no Meta pixel, and nothing that follows you
between sites.</p>
<p>Two things are still worth being straight with you about: a small amount of
browser storage used by our staff-only admin page, and a few third-party servers
your browser contacts to fetch fonts and photographs. Both are below.</p>

<h2 id="cookies">2. Cookies we set</h2>
<p>None. If you inspect this site you will not find a cookie from us.</p>

<h2 id="storage">3. Browser storage</h2>
<p>Our staff admin page — which visitors have no reason to open and cannot use
without a password — keeps two things in your own browser:</p>
<table>
  <tr><th>What</th><th>Why</th><th>How long</th></tr>
  <tr><td>A sign-in token</td><td>So a staff member isn't asked for their password on every click</td><td>Cleared when the browser tab closes</td></tr>
</table>
<p>Neither is used for tracking and neither leaves your device except to
authenticate with our database provider.</p>

<h2 id="third">4. Third parties your browser contacts</h2>
<p>When a page loads, your browser fetches some things from other companies'
servers. Those companies necessarily see your IP address and basic request
information, in the same way any website you visit does. They are:</p>
<table>
  <tr><th>Who</th><th>What for</th><th>Sets cookies?</th></tr>
  <tr><td>GitHub Pages</td><td>Hosts and serves this site</td><td>No</td></tr>
  <tr><td>Google Fonts</td><td>The two typefaces this site uses</td><td>No, but Google receives your IP address</td></tr>
  <tr><td>Unsplash</td><td>The photographs</td><td>No, but Unsplash receives your IP address</td></tr>
  <tr><td>Web3Forms and Supabase</td><td>Contacted only at the moment you press Send on the enquiry form</td><td>No</td></tr>
</table>
<p>If you follow a link to our WhatsApp, Instagram, Facebook or TikTok, you leave
this site and that company's own policies take over. We have no control over
what they do.</p>

<h2 id="consent">5. Why there is no consent banner</h2>
<p>Consent banners exist because of rules on storing or reading information on
your device — cookies, mainly. We store nothing on your device, so there is
nothing to ask permission for, and a banner would be noise pretending to be care.</p>
<p>One honest caveat: European regulators have taken the view that loading fonts
from Google's servers transfers a visitor's IP address to a third party and needs
its own justification. We think the safer answer is not a banner but removing the
transfer — see the note in our risk register about serving the fonts and images
from our own site instead. <span class="fill">Decide whether to self-host fonts and images before launch</span>.</p>

<h2 id="control">6. How to control all of this</h2>
<p>Your browser can block third-party requests, and privacy extensions can block
them selectively. Nothing on this site will break if you do — the pages will
simply fall back to your system fonts and show empty spaces where photographs
would be.</p>
<p>Questions: <a href="mailto:TripzaCeylon@gmail.com">TripzaCeylon@gmail.com</a>.</p>
"""

# ═════════════════════════════════════════════════════════════════ TERMS ═══
terms_toc = [("about", "About these terms"), ("who", "Who we are"),
             ("use", "Using this website"), ("content", "Accuracy of what you read here"),
             ("enquiry", "Enquiries are not bookings"), ("ip", "Our content and yours"),
             ("links", "Links to other sites"), ("liability", "Our liability"),
             ("law", "Governing law"), ("contact", "Contact")]

terms_body = """
<h2 id="about">1. About these terms</h2>
<p>These terms cover your use of this website. Booking a trip is covered
separately by our <a href="booking.html">Booking &amp; Refund Conditions</a>, and
how we handle your data is in our <a href="privacy.html">Privacy Policy</a>.</p>
<p>By using this site you accept these terms. If you don't accept them, please
don't use the site.</p>

<h2 id="who">2. Who we are</h2>
<p>This site is operated by <span class="fill">registered company name</span>,
company number <span class="fill">registration number</span>, registered at
<span class="fill">registered address</span>, Sri Lanka.</p>

<h2 id="use">3. Using this website</h2>
<p>You may read these pages, plan a route and send us an enquiry. Please don't:</p>
<ul>
  <li>submit false enquiries, or somebody else's details without their permission</li>
  <li>try to break, overload or gain unauthorised access to the site or our database</li>
  <li>copy the site wholesale, or scrape it to build a competing service</li>
  <li>use it for anything unlawful</li>
</ul>

<h2 id="content">4. Accuracy of what you read here</h2>
<p>We write our own descriptions and we try hard to keep them accurate, but:</p>
<ul>
  <li><strong>Distances and driving times on the route planner are estimates.</strong>
    They are calculated from straight-line distances with an allowance for how
    Sri Lankan roads actually run. Treat them as a guide, not a timetable.</li>
  <li><strong>Opening hours, seasons, wildlife and festival dates change.</strong>
    Full-moon festivals move every year. Wildlife is wildlife: we can tell you
    where the odds are good, never that you will see an animal.</li>
  <li><strong>Photographs are illustrative.</strong> Several show the region or the
    setting rather than the exact property, activity or room, and each carries a
    caption saying what it is.</li>
  <li>Availability and prices are confirmed only in a written quote, not on these pages.</li>
</ul>

<h2 id="enquiry">5. Enquiries are not bookings</h2>
<p>Sending the enquiry form costs nothing and commits you to nothing. It is not a
booking, not an option held in your name, and not a contract. A trip exists only
once we have sent you a written confirmation and you have paid what that
confirmation asks for. See the <a href="booking.html">Booking Conditions</a>.</p>

<h2 id="ip">6. Our content and yours</h2>
<p>The text, layout, maps and design of this site belong to us. The photographs
are used under the <a href="https://unsplash.com/license" target="_blank" rel="noopener">Unsplash License</a>,
which permits commercial use; copyright stays with the photographers.</p>
<p>You keep ownership of anything you send us. By sending an enquiry you allow us
to use its contents for the purpose of answering you and arranging your trip.</p>

<h2 id="links">7. Links to other sites</h2>
<p>Where we link to another website we are not endorsing it and we are not
responsible for its content or its handling of your data.</p>

<h2 id="liability">8. Our liability</h2>
<p>We provide this website as it is. We do not promise it will always be
available or free of errors.</p>
<p>To the extent the law allows, we are not liable for loss arising from your
relying on general information published here — as opposed to a written quote or
confirmation we have given you directly. Nothing in these terms limits liability
for death or personal injury caused by our negligence, for fraud, or for anything
else that cannot lawfully be excluded under Sri Lankan law.</p>
<p><span class="fill">A lawyer should review this clause — the enforceable extent of a liability limit is exactly the kind of thing that varies by jurisdiction.</span></p>

<h2 id="law">9. Governing law</h2>
<p>These terms are governed by the laws of Sri Lanka, and the courts of Sri Lanka
have jurisdiction. If you are a consumer elsewhere, you may still have the
protection of the mandatory consumer laws of your own country.</p>

<h2 id="contact">10. Contact</h2>
<p><a href="mailto:TripzaCeylon@gmail.com">TripzaCeylon@gmail.com</a> &middot; 076 167 4855</p>
"""

# ═══════════════════════════════════════════════════════ BOOKING/REFUND ═══
booking_toc = [("status", "Status of this document"), ("quote", "Quotes and confirmation"),
               ("pay", "Payment"), ("cancel-you", "If you cancel"),
               ("cancel-us", "If we cancel or change your trip"),
               ("force", "Events outside anyone's control"),
               ("insurance", "Insurance — please read this one"),
               ("docs", "Passports, visas and health"),
               ("conduct", "Behaviour and safety"), ("complaints", "If something goes wrong"),
               ("law", "Governing law")]

booking_body = """
<div class="draft" role="note">
  <p><strong>This page is a skeleton, not a finished policy.</strong> Cancellation
  terms are commercial decisions: the numbers below are placeholders showing the
  usual <em>shape</em> of such a policy, not a recommendation. Replace every figure
  with what TripzaCeylon will actually honour, and have a lawyer check the result
  before taking a single payment.</p>
</div>

<h2 id="status">1. Status of this document</h2>
<p>These conditions apply when you book a trip with us. They sit alongside our
<a href="terms.html">Website Terms</a> and <a href="privacy.html">Privacy Policy</a>.</p>

<h2 id="quote">2. Quotes and confirmation</h2>
<ul>
  <li>A quote is valid for <span class="fill">number</span> days unless it says otherwise.</li>
  <li>A quote is not a reservation. Hotels and guides are held only once you have confirmed and paid the deposit.</li>
  <li>Your trip is confirmed when we send you a written confirmation. That
    confirmation, plus these conditions, is the contract between us.</li>
  <li>Please check every name, date and flight detail on the confirmation
    immediately. Corrections later may carry supplier charges.</li>
</ul>

<h2 id="pay">3. Payment</h2>
<ul>
  <li><strong>Deposit:</strong> <span class="fill">%</span> of the trip cost, due on confirmation.</li>
  <li><strong>Balance:</strong> due <span class="fill">number</span> days before arrival.</li>
  <li><strong>Late bookings</strong> made within <span class="fill">number</span> days of arrival are payable in full.</li>
  <li><strong>How to pay:</strong> <span class="fill">bank transfer / card / which providers</span>.</li>
  <li><strong>Currency and charges:</strong> <span class="fill">state the currency, and who bears bank charges and any currency conversion</span>.</li>
</ul>
<p>If the balance is not paid by the due date we may treat the booking as
cancelled by you, and the cancellation charges below will apply.</p>

<h2 id="cancel-you">4. If you cancel</h2>
<p>Cancellations must be in writing to
<a href="mailto:TripzaCeylon@gmail.com">TripzaCeylon@gmail.com</a> and take effect
on the day we receive them.</p>
<table>
  <tr><th>Notice before arrival</th><th>Charge</th></tr>
  <tr><td>More than <span class="fill">n</span> days</td><td><span class="fill">%</span> of trip cost</td></tr>
  <tr><td><span class="fill">n</span> to <span class="fill">n</span> days</td><td><span class="fill">%</span></td></tr>
  <tr><td><span class="fill">n</span> to <span class="fill">n</span> days</td><td><span class="fill">%</span></td></tr>
  <tr><td>Fewer than <span class="fill">n</span> days, or no-show</td><td><span class="fill">%</span></td></tr>
</table>
<p>Some elements are non-refundable from the moment they are booked — typically
domestic flights, train seats in reserved classes, permits and certain peak-season
hotel nights. We will tell you which parts of your trip those are, in writing,
before you pay.</p>

<h2 id="cancel-us">5. If we cancel or change your trip</h2>
<ul>
  <li>We occasionally have to change a hotel or reorder a route. Where we do, we
    will provide accommodation and services of an equivalent or better standard
    at no extra cost to you.</li>
  <li>If we have to make a <em>significant</em> change — a materially different
    route, a lower standard of accommodation, or a change of travel dates — you may
    accept it, accept an alternative trip we offer, or cancel and receive a full
    refund of everything you have paid us.</li>
  <li>If we cancel your trip for any reason other than your non-payment or an
    event outside our control, you get a full refund.</li>
</ul>

<h2 id="force">6. Events outside anyone's control</h2>
<p>Neither of us is liable for failing to perform because of something genuinely
outside our control: war, civil unrest, terrorism, epidemic, natural disaster,
extreme weather, strikes, airport or border closures, or government action.</p>
<p><span class="fill">Decide and state what happens to money already paid in these circumstances — refund, credit, or refund less unrecoverable supplier costs. This is the clause travellers argue about most, so be explicit.</span></p>

<h2 id="insurance">7. Insurance — please read this one</h2>
<p><strong>Travel insurance is your responsibility and we strongly recommend it.</strong>
It should cover at minimum medical treatment and repatriation, cancellation and
curtailment, and your baggage.</p>
<p>If your trip includes anything adventurous — hiking, surfing, diving,
white-water rafting, ziplining, quad biking, paragliding or skydiving — check that
your policy actually covers that activity. Many standard policies exclude them, or
require an add-on. We cannot check your policy for you and we are not liable for a
loss your insurer declines.</p>

<h2 id="docs">8. Passports, visas and health</h2>
<p>Making sure your passport, visa and vaccinations are in order is your
responsibility. Requirements depend on your nationality and change without much
notice. We are happy to point you at official sources, but we cannot be
responsible for you being refused entry.</p>

<h2 id="conduct">9. Behaviour and safety</h2>
<p>Sri Lanka has religious sites with dress and conduct rules, and national parks
with rules that exist for the animals' sake as much as yours. We ask you to follow
what your guide tells you. We may end a trip without refund if someone's behaviour
puts others at risk or is seriously disruptive.</p>
<p>We do not arrange elephant rides, elephant bathing, or any activity where an
animal is crowded or cornered for a photograph, and we will not book operators
who do.</p>

<h2 id="complaints">10. If something goes wrong</h2>
<p>Tell your guide or call us <em>while you are still in the country</em> — most
problems can be fixed on the spot, and almost none can be fixed after you have
flown home. If it isn't resolved, write to
<a href="mailto:TripzaCeylon@gmail.com">TripzaCeylon@gmail.com</a> within
<span class="fill">number</span> days of returning and we will respond within
<span class="fill">number</span> days.</p>

<h2 id="law">11. Governing law</h2>
<p>These conditions are governed by the laws of Sri Lanka. If you are a consumer
resident elsewhere, mandatory consumer protections in your own country may also
apply.</p>
"""

if __name__ == "__main__":
    made = [
        page("privacy.html", "Privacy Policy",
             "How TripzaCeylon collects, uses and protects the details you send through our enquiry form.",
             privacy_body, privacy_toc),
        page("cookies.html", "Cookie Policy",
             "This site sets no cookies and runs no analytics. Here is exactly what it does do.",
             cookies_body, cookies_toc),
        page("terms.html", "Website Terms",
             "The terms covering your use of the TripzaCeylon website.",
             terms_body, terms_toc),
        page("booking.html", "Booking & Refund Conditions",
             "How bookings, payments, changes and cancellations work with TripzaCeylon.",
             booking_body, booking_toc),
    ]
    for f in made:
        print(f"  wrote {f:16} {pathlib.Path(f).stat().st_size/1024:5.1f} KB")
