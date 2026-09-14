# Putting TripzaCeylon online with GitHub Pages

Free hosting, HTTPS included, no card. Three parts: get the files online, get
enquiries emailed to you, and put them in a free database with a proper admin
login.

---

## Part A — hosting (about 10 minutes)

### 1. Make a GitHub account

<https://github.com/signup> if you don't have one. Note your username — it ends
up in your web address.

### 2. Create the repository

**New repository** (the green button, or <https://github.com/new>)

- **Name:** `tripzaceylon`
- **Public** — Pages needs this on the free plan
- Leave "Add a README" **unticked**
- **Create repository**

### 3. Upload the site

On the empty repo page, click **uploading an existing file**.

Open this folder, select **everything inside it** — all the `.html` files, all
the `.png` files, and `.nojekyll` — and drag them onto the page.

> Drag the *contents*, not the folder itself. If you drag the folder, everything
> lands one level deep and your site will 404.

`.nojekyll` may be hidden on your Mac. Press **⌘ + Shift + .** in Finder to show
hidden files, drag it, then press it again to re-hide.

Scroll down, click **Commit changes**.

### 4. Turn Pages on

**Settings** (top of the repo) → **Pages** in the left sidebar.

- **Source:** Deploy from a branch
- **Branch:** `main`, folder `/ (root)`
- **Save**

Wait two or three minutes, then reload. Your address appears at the top:

```
https://YOUR-USERNAME.github.io/tripzaceylon/
```

That's the site live. The home page loads because it's named `index.html` —
that's the one filename GitHub Pages serves at a bare URL, which is why I
renamed it from `tripzaceylon.html` and repointed every internal link.

### 5. Updating it later

Repo → the file you want to change → the pencil icon → edit → **Commit changes**.
Or **Add file → Upload files** and drop in a newer copy to overwrite.

Changes go live in a minute or two. If you don't see them, hard-reload with
**⌘ + Shift + R** — the old version is usually just cached in your browser.

### 6. Your own domain, when you want one

Buy a domain, then Settings → Pages → **Custom domain**, type it in, and add the
DNS records GitHub shows you at your registrar. Tick **Enforce HTTPS** once it
turns on. Nothing in the site files needs to change.

---

## Part B — getting the enquiries

GitHub Pages can only serve files. It cannot run any code, so the form needs an
outside service to carry the message. **Web3Forms** does this free, has no
account to create, and delivers straight to your Gmail.

### 7. Get your access key

1. Go to <https://web3forms.com>
2. Type `TripzaCeylon@gmail.com` into the box and press **Create Access Key**
3. Check that inbox — the key arrives in under a minute. It looks like
   `a1b2c3d4-e5f6-7890-abcd-ef1234567890`

### 8. Put it in the site

Open `build-your-trip.html` and find this line near the bottom:

```js
const FORM_KEY = 'PASTE_YOUR_WEB3FORMS_ACCESS_KEY_HERE';
```

Replace the placeholder with your key, keeping the quotes. Upload the file to
GitHub again.

That key is safe sitting in a public file — it can only ever deliver mail to the
address that created it, so a copy is useless to anyone else. This is the reason
Web3Forms works on a static host when the WhatsApp API can't: there is no secret
to protect.

### 9. Test it

Open your live site, go to Build Your Own, fill the form in and send. The
enquiry should land in `TripzaCeylon@gmail.com` within a minute, laid out as:

```
Name:       Jane Perera
Email:      jane@email.com
Package:    —
Route:      Colombo → Kandy → Ella  (586 km, ~10 days)
When:       2027-04
Travellers: 2 people
Length:     7–10 days
Budget:     Mid-range
Interests:  Wildlife, Beaches
Notes:      Two kids, avoid long drives
```

Check spam the first time and mark it *not spam*, so later ones go to the inbox.

---

## If the form says "that did not send"

Nothing the visitor typed is cleared, and they're offered a WhatsApp link and an
email link — so you still get the lead. Then check, in this order:

| Cause | Fix |
|---|---|
| Key still says `PASTE_...` | Step 8 — the form deliberately refuses to send until a real key is in. |
| Key pasted with a stray space or a missing quote | Re-copy it from the email. |
| The file wasn't re-uploaded after editing | Upload `build-your-trip.html` again. |
| Browser cached the old file | Hard-reload with **⌘ + Shift + R**. |
| Free monthly limit reached | Web3Forms allows 250 submissions a month free. |

Press **F12 → Console** on the live page to see the real error if it's none of
these.

---

## Getting it to WhatsApp as well, later

Once email is working, Web3Forms can also fire a **webhook** on each submission.
Point that at a Make or Zapier scenario and it can push the same enquiry into
WhatsApp. Worth doing only once enquiries are steady — email first, it works
today and costs nothing.

---

## Part C — the enquiries database (Supabase)

Email alone means an enquiry lives in one inbox and nowhere else. Supabase gives
you a real database, a proper admin login, and it's free — 500 MB of Postgres,
no card.

### 10. Create the project

<https://supabase.com> → sign up → **New project**. Choose **Singapore** or
**Mumbai** as the region; both are close to Sri Lanka. Save the database password
it generates somewhere safe — you won't need it for this, but losing it is a
nuisance.

### 11. Create the table and the security rules

**SQL Editor → New query.** Open `supabase-setup.sql` from this folder, paste the
whole thing in, press **Run**.

That creates the `enquiries` table plus three rules that are the entire security
model:

- anyone may **add** an enquiry
- only a signed-in address listed in the `staff` table may **read** one
- nothing may **delete** one, including you — removing an enquiry is a
  deliberate act in the dashboard

The query prints the three policies at the end so you can see they took.

### 12. Copy your two public values

**Project Settings → API.** Copy the **Project URL** and the **anon public** key.

Paste both into two files — `admin.html` and `build-your-trip.html` — replacing:

```js
const SB_URL = 'PASTE_YOUR_SUPABASE_PROJECT_URL_HERE';
const SB_KEY = 'PASTE_YOUR_SUPABASE_ANON_KEY_HERE';
```

Upload both files to GitHub.

**These two values are meant to be public.** The anon key can only insert an
enquiry — it cannot read, edit or delete one. That's enforced by the database,
not by hiding the key. There is also a **service_role** key on that page: that
one is a master key and must never go into any file here.

### 13. Make your admin login

**Authentication → Users → Add user.**

- Email: the address in the staff table — `tripzaceylon@gmail.com` unless you
  changed it in the SQL
- A strong password
- Tick **Auto Confirm User**

Then **Authentication → Sign In / Providers** and turn **Allow new users to sign
up** **off**. Without this a stranger could create an account for themselves.

### 14. Test the whole path

Submit the form on your live site, then open `admin.html`, sign in, and the
enquiry should be sitting there. If the form says "did not send", press
**F12 → Console** — the error from Supabase is printed there in full.

| Message | Meaning |
|---|---|
| `new row violates row-level security policy` | The SQL didn't run, or ran only partly. Re-run step 11. |
| `401` / `Invalid API key` | Wrong key pasted, or a stray space. |
| Sign-in says `Invalid login credentials` | The user doesn't exist yet — step 13. |
| Signed in but the list is empty and no error | Your email isn't in the `staff` table. Add it under **Table Editor → staff**. |

---

## The admin panel

`admin.html` is a private page for running the site. Nothing links to it, so
visitors won't find it — open it at:

```
https://YOUR-USERNAME.github.io/tripzaceylon/admin.html
```

It does two things:

**Edit content.** Loads the live home page, lets you rewrite package names,
nights, routes, descriptions, the three offers and all 48 map entries, then
hands you back an updated `index.html` to upload. It only changes the words you
actually touch — everything else is byte-for-byte identical, so it cannot break
the layout or the map.

**Read enquiries.** Sign in with your Supabase email and password and every
enquiry is listed newest first, with the route the visitor built, and a dropdown
to mark each one new / replied / booked / closed. That status writes straight
back to the database.

The login is real — the database checks it, not this page — so the file being
public on GitHub doesn't matter: without your password it shows an empty login
box. It still can't change the live site on its own; publishing is always you
uploading a file.

**Bookings and payments are the one thing this still can't cover.** Taking money
needs a server that can hold a secret key, which a static host can't. When you
get there: either move to a small server, or embed a booking product like Rezdy
or Checkfront. The database you now have will carry over either way.

---

## Notes

- **Everything in a public repo is public**, including this file. Never commit
  passwords, and change the TikTok and Instagram passwords you shared earlier if
  you haven't already.
- The form carries a hidden honeypot checkbox. Bots tick it, Web3Forms drops
  those submissions, and you never see the spam.
- The photographs still load from Unsplash's servers, so they cost you no GitHub
  storage or bandwidth. Worth self-hosting them before any serious launch, in
  case an image is ever removed.
