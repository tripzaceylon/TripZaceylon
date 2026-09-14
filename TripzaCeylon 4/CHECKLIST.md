# TripzaCeylon — everything you need, on one page

Two lists: **what to upload**, and **what to do**. Print this if it helps.

Detailed walkthrough with every button named: **`START-HERE.md`**.

---

## A. The files

### Upload these to GitHub — 16 files

| File | What it is |
|---|---|
| `index.html` | Home page. **Must keep this name** — it's the only filename GitHub serves at your bare web address |
| `build-your-trip.html` | Route planner + enquiry form. **The file you edit to add your keys** |
| `place.html` | Article page for every map pin (49 entries) |
| `guide.html` | Article page for the 14 footer guides |
| `offer.html` | Special offer pages |
| `admin.html` | Your private admin panel |
| `enquire.html` | Redirect, so old shared links still work |
| `privacy.html` | Privacy Policy |
| `cookies.html` | Cookie Policy |
| `terms.html` | Website Terms |
| `booking.html` | Booking & Refund Conditions |
| `logo.png` | Nav logo |
| `logo-full.png` | Footer logo |
| `favicon.png` | Browser tab icon |
| `apple-touch-icon.png` | Icon when saved to a phone home screen |
| `.nojekyll` | Empty file that stops GitHub mangling your site. Hidden — press **⌘ + Shift + .** in Finder to see it |

Optional but sensible: `.gitignore` and `supabase-setup.sql` (neither affects the
website; the SQL is useful to have version-controlled).

### Do NOT upload these

| File | Why |
|---|---|
| `LEGAL-RISKS.md` | **Records that the site was making accreditation claims that weren't true.** A public repo means publishing that admission. Keep it on your Mac. |
| `SECURITY.md` | Lists the exact security gaps that remain. That's a map for anyone wanting to poke at your site. |
| `build-legal.py` | Development tool. Harmless, but no use to a web server. |
| `START-HERE.md`, `CHECKLIST.md`, `GITHUB-SETUP.md` | Your notes. Uploading is harmless, just clutter. |

`.gitignore` already excludes the first three, so if you ever use Git properly
they stay out automatically. **Dragging files by hand ignores `.gitignore`** — so
when you drag, just don't select them.

---

## B. The accounts

Three, all free, no card:

1. **GitHub** — hosts the site · github.com/signup
2. **Web3Forms** — emails you each enquiry · web3forms.com (no account, just an email)
3. **Supabase** — stores enquiries, powers your admin login · supabase.com

---

## C. The three values you'll paste in

All three go in **`build-your-trip.html`**, in one block near the top. Search the
file for **`SETTINGS`** in capitals.

| Value | Where it comes from | Also needed in |
|---|---|---|
| `FORM_KEY` | Web3Forms emails it to you | — |
| `SB_URL` | Supabase → Project Settings → API → "Project URL" | `admin.html` |
| `SB_KEY` | Supabase → Project Settings → API → **anon public** | `admin.html` |

> **The `service_role` key is on that same Supabase page. Never use it.** It
> ignores every security rule. Only the **anon public** one belongs in your files.

All three are safe in a public file — that's by design, and `SECURITY.md`
explains why.

---

## D. The order to do things in

- [ ] **1.** Create the GitHub repo, named `tripzaceylon`, **Public**
- [ ] **2.** Drag in the 16 files — **the files, not the folder**
- [ ] **3.** Settings → Pages → Deploy from a branch → `main` / `(root)` → Save
- [ ] **4.** Wait 3 minutes → your site is live
- [ ] **5.** Settings → Pages → tick **Enforce HTTPS**
- [ ] **6.** Get a Web3Forms key, paste into `build-your-trip.html`, commit
- [ ] **7.** Test the form → check your Gmail (and the spam folder)
- [ ] **8.** Create the Supabase project, region **Singapore**
- [ ] **9.** SQL Editor → paste all of `supabase-setup.sql` → Run
- [ ] **10.** Paste `SB_URL` and `SB_KEY` into **both** `build-your-trip.html` and `admin.html`, commit both
- [ ] **11.** Supabase → Authentication → Users → Add user (tick **Auto Confirm**)
- [ ] **12.** Supabase → Authentication → Sign In / Providers → **turn OFF "Allow new users to sign up"**
- [ ] **13.** Test: submit the form, then open `admin.html` and sign in

Your site: `https://YOUR-USERNAME.github.io/tripzaceylon/`
Your admin: `https://YOUR-USERNAME.github.io/tripzaceylon/admin.html`

---

## E. Before you tell anyone about it

These are not optional-optional. They're the difference between a site that's
ready and one that isn't.

- [ ] **Register with the SLTDA.** Operating an unregistered tourist service is
      an offence in Sri Lanka. This comes before everything else — see
      `LEGAL-RISKS.md` §1.
- [ ] **Fill in the 35 yellow placeholders** across the four legal pages —
      company name, registration number, address.
- [ ] **Decide your real cancellation terms** and put them in `booking.html`.
      Every percentage in there is currently blank on purpose.
- [ ] **Have a Sri Lankan lawyer read all four legal pages** before you accept a
      single deposit.
- [ ] **Change your TikTok and Instagram passwords.** You pasted them into a chat
      during this project; treat both as compromised.

---

## F. Common problems

| Symptom | Cause | Fix |
|---|---|---|
| Site shows **404** | You dragged the folder, not the files | In the repo, if you see one folder instead of your `.html` files — delete it and re-upload the contents |
| Home page won't load at the bare address | `index.html` renamed or missing | It must be called exactly `index.html` |
| Form says **"that did not send"** | Key still a placeholder, or the file wasn't re-uploaded | Re-check the `SETTINGS` block; hard-reload with **⌘ + Shift + R** |
| Form sends but nothing in the database | `SB_URL` / `SB_KEY` not pasted, or SQL not run | Steps 9–10 |
| Admin signs in but the list is empty | Your email isn't in the `staff` table | Supabase → Table Editor → `staff` → add it |
| **"new row violates row-level security policy"** | The SQL didn't finish | Re-run all of `supabase-setup.sql` |
| Changes don't show up | Browser cache | **⌘ + Shift + R** |

Any page misbehaving: press **F12**, click **Console**, and the real error is
written there in plain words.

---

## G. What you've actually got

- 7 site pages, 4 legal pages, 1 admin panel
- An interactive map with 48 places, stays and activities, each with its own article
- 14 destination and experience guides
- A route planner that estimates distance and driving time
- An enquiry form that emails you *and* stores to a database
- An admin panel with a real login where you can read enquiries and edit your own
  site copy without touching code
- Zero JavaScript dependencies — nothing to update, nothing to rot
- About 850 KB total
