# Security review — the 20-item checklist, honestly scored

**Date:** 12 September 2026 · **Reviewer:** Claude (an AI assistant, not a security professional)

That checklist is written for apps with a server, user accounts, sessions and
dependencies. Your site has none of those, so **six of the twenty simply don't
apply** — and saying "done ✅" against them would be the same kind of dishonesty
as the fake reviews I removed.

Here is each one, what I actually did, and where the gaps are.

---

## Score

| | Count |
|---|---|
| Already correct before this pass | 6 |
| Fixed in this pass | 8 |
| Genuinely not applicable | 6 |
| **Known gaps that remain** | **3** (items 18, 19, 9 — all explained below) |

---

## 1. Hide API keys — ✅ correct, but counter-intuitive

Two keys sit in your page source **on purpose**:

- **Web3Forms key** — can only deliver mail to the address that created it.
- **Supabase anon key** — can only INSERT an enquiry. It cannot read, edit or
  delete one. That's enforced by the database, not by hiding the key.

The dangerous one is Supabase's **service_role** key, which ignores every rule.
I scanned every file: it is not present, and the setup guide warns against it in
three separate places.

> The rule isn't "hide all keys". It's "know which keys are safe to publish".
> Publishing an anon key is normal; publishing a service_role key is a disaster.

## 2. Purge Git secrets — ✅ done

Added `.gitignore` covering `.env`, `*.key`, `*.pem`, `service_role*` and macOS
clutter. Scanned the whole folder for JWTs, AWS keys, Meta tokens, private key
blocks and hardcoded passwords: **none found.**

Since you haven't pushed to GitHub yet, there's no history to purge — which is
the easiest time to get this right.

## 3. Use the public DB key — ✅ already correct

The site uses the anon key. The admin panel uses the same anon key plus a signed-in
user's token.

## 4. Enable row-level security — ✅ already correct

RLS is on for `enquiries` and `staff`. Three policies: anyone may insert, only
staff may select, only staff may update. **No delete policy exists at all**, so
nothing can delete an enquiry through the API.

## 5. Encrypt sensitive data — ✅ as far as it applies

HTTPS in transit; Supabase encrypts at rest. More importantly, **the site doesn't
collect sensitive data** — no passports, no card numbers, no health information.
I added a warning under the notes box telling people not to send those.
Not collecting something beats encrypting it.

## 6. Enforce server-side auth — ✅ fixed earlier in this project

The admin login is checked by Supabase's servers against the `staff` table. This
replaced my earlier position that a login was impossible on a static host — true
of a homemade one, not of a real auth provider.

## 7. Lock record access — ✅ already correct

Reading enquiries requires a signed-in user **whose email is in the staff table**.
Signing in isn't enough on its own. Public sign-ups must also be turned off
(step 32 of `START-HERE.md`).

## 8. Block field tampering — ✅ **fixed this pass**

This was a real hole. The insert policy controlled *which rows* could be added
but not *which columns* could be filled. Someone could have posted their own
`created_at`, dating an enquiry into the future so it sat permanently at the top
of your inbox — or set `status` to `booked`.

Fixed with column-level grants: the anon role may now write **only** the twelve
fields a visitor legitimately fills. Everything else falls back to its default.
Also added a sanity check so a fabricated `consent_at` far from the present is
rejected.

## 9. Secure session cookies — ⚠️ not applicable, with a caveat

No cookies anywhere. The admin token lives in `sessionStorage` and vanishes when
the tab closes.

**The honest caveat:** `sessionStorage` is readable by JavaScript, so an XSS bug
in the admin page could steal a session. The mitigation is that item 15 holds —
all enquiry data is escaped before display. An `httpOnly` cookie would be
stronger, but setting one requires a server, which you don't have.

## 10. Hash passwords — ✅ not your code's job

Supabase Auth handles hashing. Your code never sees or stores a password.

## 11. Rate limit login — ✅ **fixed this pass** (and extended)

Supabase rate-limits auth attempts itself. The gap was the **enquiry endpoint**:
the anon key is public, so anyone could script inserts in a loop and exhaust your
free tier.

Added a database trigger: **max 5 enquiries per email address per hour**, and
**max 20 across the whole site per minute**.

## 12. Add bot protection — ✅ **fixed this pass**

Two layers, no CAPTCHA:

- **Honeypot** — a hidden checkbox humans never see and bots tick.
- **Time trap (new)** — the form records when it loaded and rejects anything
  submitted in under three seconds. No human reads that form that fast.

## 13. Parameterize queries — ✅ correct, hardened

There is no SQL in your site. Supabase's PostgREST parameterises everything. The
one place a value enters a URL — the status update filter — now forces an integer
and checks the status against a fixed list before sending.

## 14. Validate all input — ✅ **fixed this pass**

Validation now exists in three places, which is the right number:

| Layer | What it does |
|---|---|
| HTML attributes | `required`, `type=email`, `maxlength` |
| JavaScript | name 2–120 chars, real email shape, notes ≤ 4000, time trap |
| **Database** | `CHECK` constraints on every length, status restricted to 4 values |

The database layer is the one that matters — the other two can be bypassed by
posting straight to the API.

## 15. Escape user content — ✅ verified line by line

I checked this first because it's the one that could have hurt you: an attacker
puts `<img onerror=...>` in the name field, you open your admin panel, their
script runs with your session.

Every attacker-controlled field goes through `esc()` before display. `status` is
pinned to four values by a database constraint; `id` is a number. **No XSS
found.**

## 16. Restrict file uploads — ⚪️ not applicable

There are no file uploads anywhere on the site. The only file picker is in the
admin content editor, and it reads a file **in your own browser** — nothing is
uploaded anywhere.

## 17. Trim API responses — ✅ **fixed this pass**

The admin panel asked for `select=*`, which returned columns it never displayed,
including your private `staff_note`. Now it names the fifteen columns it actually
shows and caps the response at 500 rows.

## 18. Add security headers — ⚠️ **partly done — a real limitation**

Added to all 11 pages via `<meta>`:

- **Content-Security-Policy** restricting images to Unsplash, fonts to Google,
  network calls to Supabase and Web3Forms, and `object-src 'none'`
- **Referrer-Policy: strict-origin-when-cross-origin**
- **upgrade-insecure-requests**

**Two honest gaps:**

1. `script-src` needs `'unsafe-inline'` because every page's JavaScript is inline
   and a static host can't issue a per-request nonce. That weakens the CSP's
   XSS protection substantially. Fixing it properly means moving all JS to
   separate `.js` files — worth doing, but a big refactor.
2. `frame-ancestors`, `X-Content-Type-Options` and `Strict-Transport-Security`
   **cannot be set from a meta tag** — they're HTTP headers only, and GitHub
   Pages doesn't let you set headers. Moving to Cloudflare Pages or Netlify later
   would let you set them properly.

## 19. Force HTTPS — ⚠️ one setting is yours to tick

`upgrade-insecure-requests` is in the CSP, and GitHub Pages serves HTTPS by
default. But **you must tick "Enforce HTTPS"** in Settings → Pages once your site
is live, or `http://` will keep working alongside it.

Proper HSTS needs a header, so see the limitation in item 18.

## 20. Scan dependencies — ✅ nothing to scan

**Your site has zero JavaScript dependencies.** No npm, no package.json, no
React, no jQuery, no CDN libraries. Every line is written for this project.

That's not laziness, it's the strongest answer to this item: no dependencies
means no supply-chain risk, no `npm audit` output to triage, and nothing that
rots while you aren't looking. The only third-party code is Google's font
stylesheet.

---

## What I would still do

1. **Tick "Enforce HTTPS"** in GitHub Pages settings the moment the site is live.
2. **Turn off public sign-ups in Supabase** (step 32) — without it, a stranger can
   create an account, though the staff-table check still stops them reading anything.
3. **Use a strong, unique password** for the admin login, in a password manager.
4. **Re-run `supabase-setup.sql`** — it now contains the column grants and the
   rate-limit trigger. It's safe to run again.
5. Consider moving inline JavaScript into `.js` files so the CSP can drop
   `'unsafe-inline'`. The biggest remaining win, and the most work.
6. Consider Cloudflare Pages instead of GitHub Pages when you want real HTTP
   headers. Same free tier, same drag-and-drop.

## What this review is not

I'm an AI assistant, not a penetration tester. I read the code and reasoned about
it; I did not attack a running system. Before you handle payments or hold
passport details, get a real security review — the threat model changes
completely at that point.
