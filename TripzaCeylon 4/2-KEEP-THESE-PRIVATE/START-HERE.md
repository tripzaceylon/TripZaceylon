# Start here — the whole thing, one step at a time

Do these in order. Don't skip ahead: each stage checks that the last one worked.

Total time: about 45 minutes. Nothing here costs money and no card is needed.

There are three stages, and each one ends with something you can look at:

1. **Get the site online** → a real web address you can send people
2. **Get enquiries by email** → the form starts working
3. **Add the database and admin login** → enquiries stored properly, with an inbox

If you only have twenty minutes today, do stage 1 and stage 2. Stage 3 can wait.

---

# STAGE 1 — Put the site online

### 1. Make a GitHub account

Go to **github.com/signup**. Use any email. Pick a username — it becomes part of
your web address, so keep it tidy, e.g. `tripzaceylon`.

Verify the email they send you.

### 2. Start a new repository

Go to **github.com/new**

### 3. Fill that form in

- **Repository name:** type `tripzaceylon`
- **Public** — leave this selected. It must be public for free hosting.
- **Do not** tick "Add a README file"
- Click the green **Create repository**

### 4. Find the upload link

You'll land on a mostly empty page. Look for the line of small text that says
*"…or upload an existing file"* and click **uploading an existing file**.

### 5. Open your site folder

On your Mac, open the **TripzaCeylon** folder — the one this file is in.

### 6. Show hidden files

Press **⌘ + Shift + .** (command, shift, full stop).

A file called `.nojekyll` appears, greyed out. You need it. Leave hidden files
showing for now.

### 7. Select everything

Click once inside the folder, then press **⌘ + A**.

Everything should be highlighted, including `.nojekyll`.

### 8. Drag it across

Drag the highlighted files onto the GitHub page in your browser.

> **This is the step people get wrong.** Drag the *files*, not the folder. If you
> drag the folder itself, your site will show "404" later and you'll have to
> delete everything and start this step again.

Wait for the file names to finish listing on the page.

### 9. Commit

Scroll to the bottom, click the green **Commit changes**.

You should now see all your files listed in the repository.

### 10. Turn hosting on

Click **Settings** — it's in the row of tabs at the top of the repository, near
the right. Not your account settings; the repository's.

### 11. Find Pages

In the left sidebar, scroll down and click **Pages**.

### 12. Choose the source

Under **Build and deployment**:

- **Source:** choose **Deploy from a branch**
- **Branch:** choose **main**, and leave the folder as **/ (root)**
- Click **Save**

### 13. Wait, then look

Wait **two or three minutes**. Reload the page.

A box appears at the top: *"Your site is live at…"* with your address:

```
https://YOUR-USERNAME.github.io/tripzaceylon/
```

### ✅ Checkpoint 1

Open that address on your phone. You should see the TripzaCeylon home page,
the map, the packages — everything.

**If you see a 404:** you dragged the folder instead of the files (step 8). Go to
the repo, and if you see a single folder called `TripzaCeylon` rather than your
`.html` files, that's the problem. Delete it and redo steps 4–9.

---

# STAGE 2 — Make the form email you

Right now the enquiry form on your site looks like it works, but it doesn't send
anywhere. Fifteen minutes fixes that.

### 14. Get a form key

Go to **web3forms.com**

### 15. Ask for the key

There's a box on their home page asking for your email. Type:

```
TripzaCeylon@gmail.com
```

Click **Create Access Key**.

### 16. Get it out of your email

Open that Gmail inbox. There's a message from Web3Forms with your key. It looks
like:

```
a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

Copy it.

### 17. Open the file on GitHub

Back in your repository, click **build-your-trip.html** in the file list.

### 18. Start editing

Click the **pencil icon** (top right of the file, next to the Raw button).

### 19. Find the line

Press **⌘ + F**, type `SETTINGS`, press Enter.

It jumps to a big comment block near line 517 headed
*"SETTINGS — THE ONLY THREE LINES YOU EVER NEED TO EDIT"*. Just below it:

```js
const FORM_KEY = 'PASTE_YOUR_WEB3FORMS_ACCESS_KEY_HERE';
```

### 20. Replace it

Select just `PASTE_YOUR_WEB3FORMS_ACCESS_KEY_HERE` — the bit between the quotes,
not the quotes themselves — and paste your key over it.

It should end up looking like:

```js
const FORM_KEY = 'a1b2c3d4-e5f6-7890-abcd-ef1234567890';
```

### 21. Save

Click the green **Commit changes** button (top right), then **Commit changes**
again in the little box that pops up.

### 22. Wait, then test

Wait two minutes. Open your live site → **Build Your Own** → scroll to the form
at the bottom → fill it in with your own details → **Send my enquiry**.

### ✅ Checkpoint 2

Check `TripzaCeylon@gmail.com`. The enquiry should be there within a minute.

**Check your spam folder the first time**, and mark it *not spam* so later ones
go to the inbox.

**If the form says "that did not send":** wait another minute and try again — the
old version of the file may still be cached. Still failing? Press
**⌘ + Shift + R** on the page to force a fresh copy, then retry.

---

# STAGE 3 — The database and your admin login

Email is fine, but an enquiry then lives in one inbox and nowhere else. This
gives you a proper record and a private page to read them on.

### 23. Make a Supabase account

Go to **supabase.com**, click **Start your project**, sign in with GitHub
(easiest — you already have an account now).

### 24. Create the project

Click **New project**.

- **Name:** `tripzaceylon`
- **Database Password:** click Generate, then **copy it somewhere safe**. You
  won't need it today, but you don't want to lose it.
- **Region:** pick **Southeast Asia (Singapore)** — closest to Sri Lanka
- Click **Create new project**

It takes a minute or two to build. Wait for it.

### 25. Open the SQL editor

In the left sidebar, click **SQL Editor**, then **New query**.

### 26. Paste the setup

On your Mac, open **supabase-setup.sql** from your site folder — right-click it
→ Open With → TextEdit.

Select all (**⌘ + A**), copy (**⌘ + C**), then paste it into the big empty box in
Supabase.

### 27. Run it

Click **Run** (bottom right, or press **⌘ + Enter**).

You should see a small results table appear at the bottom listing three rows —
one `INSERT`, one `SELECT`, one `UPDATE`. That's your security rules confirming
they exist.

### 28. Get your two values

Left sidebar → **Project Settings** (the cog at the bottom) → **API**.

You need two things off this page:

- **Project URL** — looks like `https://abcdefgh.supabase.co`
- **anon public** key — a very long string starting `eyJ...`

> There is also a **service_role** key on this page. **Never copy that one.** It
> ignores every security rule. The `anon public` one is the safe one.

### 29. Put them in the first file

Repository → **build-your-trip.html** → pencil icon → **⌘ + F** →
search `SETTINGS`. The two Supabase lines are in the same block as the form key
you edited in step 20.

Replace the two placeholders so they read like:

```js
const SB_URL = 'https://abcdefgh.supabase.co';
const SB_KEY = 'eyJhbGciOi...';
```

**Commit changes.**

### 30. Put them in the second file

Same again, this time in **admin.html**. Same two lines, same two values.

**Commit changes.**

### 31. Create your login

Back in Supabase: left sidebar → **Authentication** → **Users** → **Add user** →
**Create new user**.

- **Email:** `tripzaceylon@gmail.com`
- **Password:** make a strong one and save it in your password manager
- **Tick "Auto Confirm User"** — without this you can't sign in
- Click **Create user**

### 32. Lock the door behind you

Left sidebar → **Authentication** → **Sign In / Providers** → click **Email**.

Find **Allow new users to sign up** and turn it **OFF**. Save.

Without this, a stranger could make themselves an account.

### 33. Test the whole path

On your live site, submit the enquiry form again with test details.

Then open:

```
https://YOUR-USERNAME.github.io/tripzaceylon/admin.html
```

Sign in with the email and password from step 31.

### 33b. Two security settings, thirty seconds

**GitHub → your repo → Settings → Pages:** tick **Enforce HTTPS**. Without it,
`http://` keeps working alongside `https://`.

**Supabase → Authentication → Sign In / Providers → Email:** confirm **Allow new
users to sign up** is **off** (you did this at step 32 — worth double-checking,
it's the one that matters).

### ✅ Checkpoint 3

Your test enquiry should be listed, showing the route you built, when you want
to travel, and everything else. Try the dropdown to mark it **replied** — it
saves straight to the database.

---

# You're done

You now have:

- a live website at your GitHub address
- enquiries arriving by email
- every enquiry stored in a database that can't be accidentally deleted
- a private admin page with a real login, where you can read enquiries and edit
  your packages and map entries without touching code

## Security

`SECURITY.md` walks through a 20-point launch checklist and scores this site
honestly against it — including the three gaps that remain and why. Worth ten
minutes before you go live.

If you re-run `supabase-setup.sql` at any point, use the current version: it now
includes column-level permissions and a rate limit that the first version didn't.

## If something breaks

`GITHUB-SETUP.md` in this folder has a fuller explanation of each part and a
troubleshooting table for the specific error messages.

The single most useful trick: on any page that's misbehaving, press **F12**, click
**Console**, and the actual error is written there in plain English.

## A few things to know

- **Everything in a public repository is public.** Never put a password in a file.
  The two Supabase values you pasted are the exception — they're designed to be
  public, and the database rules are what protect you.
- **While you're thinking about passwords:** change your TikTok and Instagram
  ones. You pasted them into a chat earlier, which means they should be treated
  as compromised.
- **Updating the site later:** repo → click the file → pencil → edit → Commit.
  Or use the **Edit content** tab in your admin page, which is easier for
  wording changes and can't break the layout.
