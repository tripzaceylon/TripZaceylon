-- ============================================================================
-- TripzaCeylon — enquiries database
-- ============================================================================
-- Paste this whole file into Supabase → SQL Editor → New query → Run.
-- It is safe to run twice; everything is guarded with "if not exists".
--
-- THE SECURITY MODEL, IN ONE PARAGRAPH
-- Your website carries a public "anon" key. That key is meant to be public —
-- the protection is not the key, it is the row-level policies below. A visitor
-- can INSERT an enquiry and do nothing else: they cannot read enquiries, cannot
-- edit them, cannot delete them. Reading is allowed only for a signed-in user
-- whose email is listed in the staff table. Get these policies wrong and every
-- enquirer's name and email is readable by anyone who views your page source,
-- so do not loosen them without understanding what you are opening up.
-- ============================================================================


-- ---------------------------------------------------------------------------
-- 1. Who is allowed to read enquiries
-- ---------------------------------------------------------------------------
create table if not exists public.staff (
  email text primary key,
  added_at timestamptz not null default now()
);

-- Change this to the address you will actually sign in with.
insert into public.staff (email)
values ('tripzaceylon@gmail.com')
on conflict (email) do nothing;

alter table public.staff enable row level security;
-- Deliberately no policies on staff: nobody can read or edit it through the
-- API at all. You manage it from the Supabase dashboard, which bypasses RLS.


-- A SECURITY DEFINER function can see the staff table even though RLS hides it
-- from everyone else. Without this, the policy below would check an empty table
-- and lock you out of your own data.
create or replace function public.is_staff()
returns boolean
language sql
security definer
stable
set search_path = public
as $$
  select exists (
    select 1 from public.staff
    where lower(email) = lower(auth.jwt() ->> 'email')
  );
$$;


-- ---------------------------------------------------------------------------
-- 2. The enquiries themselves
-- ---------------------------------------------------------------------------
create table if not exists public.enquiries (
  id           bigint generated always as identity primary key,
  created_at   timestamptz not null default now(),

  name         text not null,
  email        text not null,
  package      text,
  route        text,
  travel_when  text,
  travellers   text,
  trip_length  text,
  budget       text,
  interests    text,
  notes        text,

  -- your own workflow columns
  status       text not null default 'new',
  staff_note   text,

  -- Proof of consent. Under the PDPA and the GDPR it is the business that has to
  -- be able to show consent was given, so the moment it was ticked is recorded
  -- with the enquiry rather than being assumed.
  consent_at   timestamptz,
  marketing    boolean not null default false,

  source       text default 'website'
);

-- Length limits are the cheap half of spam control: a bot cannot dump a
-- megabyte of text into your database and eat the free tier.
alter table public.enquiries drop constraint if exists enq_name_len;
alter table public.enquiries drop constraint if exists enq_email_len;
alter table public.enquiries drop constraint if exists enq_text_len;
alter table public.enquiries drop constraint if exists enq_status_ok;

alter table public.enquiries
  add constraint enq_name_len  check (char_length(name)  between 1 and 120),
  add constraint enq_email_len check (char_length(email) between 3 and 200),
  add constraint enq_text_len  check (
        char_length(coalesce(route,''))      <= 2000
    and char_length(coalesce(notes,''))      <= 4000
    and char_length(coalesce(interests,''))  <= 400),
  add constraint enq_status_ok check (status in ('new','replied','booked','closed'));

create index if not exists enquiries_created_idx on public.enquiries (created_at desc);
create index if not exists enquiries_status_idx  on public.enquiries (status);

alter table public.enquiries enable row level security;


-- ---------------------------------------------------------------------------
-- 3. The policies — this is the part that matters
-- ---------------------------------------------------------------------------
drop policy if exists "anyone may submit an enquiry" on public.enquiries;
drop policy if exists "staff may read enquiries"     on public.enquiries;
drop policy if exists "staff may update enquiries"   on public.enquiries;

-- A visitor's browser may add a row. Note this is INSERT only: there is no
-- SELECT policy for anon, so the same key cannot read anything back.
create policy "anyone may submit an enquiry"
  on public.enquiries for insert
  to anon, authenticated
  with check (
        status = 'new'                    -- can't file something as "booked"
    and source = 'website'
    and staff_note is null                -- can't write to your private column
    -- consent_at comes from the visitor's browser, so sanity-check it rather
    -- than trusting it: a timestamp far from now is either a broken clock or
    -- someone fabricating a consent record.
    and (consent_at is null
         or consent_at between now() - interval '1 hour' and now() + interval '10 minutes')
  );

create policy "staff may read enquiries"
  on public.enquiries for select
  to authenticated
  using (public.is_staff());

create policy "staff may update enquiries"
  on public.enquiries for update
  to authenticated
  using (public.is_staff())
  with check (public.is_staff());

-- No DELETE policy anywhere, on purpose. Nothing can delete an enquiry through
-- the API, including you. Removing one is a deliberate act in the dashboard.


-- ---------------------------------------------------------------------------
-- 3b. Column-level privileges — stops field tampering
-- ---------------------------------------------------------------------------
-- A policy says *which rows* you may add. It does not say *which columns* you
-- may fill. Without this, someone could POST their own created_at — dating an
-- enquiry into the future so it always sorts to the top of your inbox — or
-- write to your private staff_note column. Revoking the table-wide grant and
-- re-granting only the columns a visitor legitimately fills closes that off:
-- everything else falls back to its default.
--
-- THIS LIST MUST MATCH WHAT THE FORM ACTUALLY SENDS.
-- Postgres refuses the whole INSERT if the client names even one column the
-- role lacks privilege on, and the error is the unhelpful
--     401 — permission denied for table enquiries
-- An earlier version of this file omitted status and source while the form was
-- still sending them, which produced exactly that. The self-test at the bottom
-- now catches this class of mistake before you hit it on the live site.
--
-- status and source are safe to grant: the policy above pins them to 'new' and
-- 'website', so a visitor can name them but cannot give them any other value.
-- created_at, id and staff_note stay ungranted — that is the actual protection.
revoke insert on public.enquiries from anon;
grant insert (name, email, package, route, travel_when, travellers,
              trip_length, budget, interests, notes,
              status, source, consent_at, marketing)
  on public.enquiries to anon;


-- ---------------------------------------------------------------------------
-- 3c. Rate limiting — stops one script filling your free tier
-- ---------------------------------------------------------------------------
-- The anon key is public, so anyone can call the insert endpoint in a loop.
-- SECURITY DEFINER lets this count existing rows even though RLS hides them
-- from the anon role.
--
-- NOTE THE LIMIT IS PER EMAIL ADDRESS. Testing your own form more than ten times
-- in an hour with the same address will trip it, and the site will say "that did
-- not send" while the email still arrives. That is the trigger doing its job,
-- not a fault. Raise the number below if ten is too tight for you.
create or replace function public.enquiry_rate_limit()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
declare recent integer;
begin
  select count(*) into recent
    from public.enquiries
   where lower(email) = lower(new.email)
     and created_at > now() - interval '1 hour';
  if recent >= 10 then
    raise exception 'Rate limit: % enquiries from % in the last hour (max 10). This is the '
                    'enquiry_rate_limit trigger in supabase-setup.sql, not a permissions '
                    'problem. If you are testing your own site, wait an hour or use a '
                    'different email address.', recent, new.email;
  end if;

  select count(*) into recent
    from public.enquiries
   where created_at > now() - interval '1 minute';
  if recent >= 20 then
    raise exception 'Too many enquiries right now. Please try again in a moment.';
  end if;

  return new;
end;
$$;

drop trigger if exists enquiry_rate_limit on public.enquiries;
create trigger enquiry_rate_limit
  before insert on public.enquiries
  for each row execute function public.enquiry_rate_limit();


-- ---------------------------------------------------------------------------
-- 4. Check it worked — READ THE RESULTS TABLE AT THE BOTTOM
-- ---------------------------------------------------------------------------
-- An earlier version of this file reported its findings with "raise notice".
-- That was a mistake: the Supabase SQL Editor does not display notices
-- anywhere. They are only written to Postgres Logs, several minutes later, and
-- only if you have turned the log level up. So the self-test looked like it did
-- nothing, and you had no way to tell whether your database was working.
--
-- Everything now comes back as an ordinary results table, which the editor
-- always shows. Seven rows. Read the last one first.
--
-- This is also more than a paperwork check: step 7 briefly becomes the anon
-- role and files a real enquiry exactly as your website does, then deletes it
-- again. A grant and a policy can each look correct and still disagree with
-- each other, and only actually trying the insert catches that.

drop function if exists public.zz_tripza_setup_check();

create function public.zz_tripza_setup_check()
returns table (step text, verdict text)
language plpgsql
as $fn$
declare
  -- The columns build-your-trip.html actually POSTs. If you ever add a field to
  -- the form, add it here and to the grant in section 3b.
  form_sends text[] := array[
    'name','email','package','route','travel_when','travellers','trip_length',
    'budget','interests','notes','status','source','consent_at','marketing'];
  granted  text;
  missing  text;
  exposed  text;
  n        integer;
begin
  select string_agg(column_name, ', ' order by column_name) into granted
    from information_schema.column_privileges
   where grantee = 'anon' and table_schema = 'public'
     and table_name = 'enquiries' and privilege_type = 'INSERT';

  select string_agg(c, ', ') into missing
    from unnest(form_sends) c
   where not exists (
     select 1 from information_schema.column_privileges
      where grantee = 'anon' and table_schema = 'public'
        and table_name = 'enquiries' and privilege_type = 'INSERT'
        and column_name = c);

  select string_agg(column_name, ', ') into exposed
    from information_schema.column_privileges
   where grantee = 'anon' and table_schema = 'public'
     and table_name = 'enquiries' and privilege_type = 'INSERT'
     and column_name in ('id', 'created_at', 'staff_note');

  select count(*) into n
    from pg_policies
   where schemaname = 'public' and tablename = 'enquiries';

  step := '1. security rules on the enquiries table';
  verdict := case when n = 3
    then 'OK - 3 policies (insert, select, update), no delete policy'
    else n || ' policies found, expected 3 - re-run this whole file' end;
  return next;

  step := '2. columns a visitor may fill';
  verdict := coalesce(granted, 'NONE - section 3b did not run');
  return next;

  step := '3. columns the form sends but cannot write';
  verdict := case when missing is null
    then 'NONE - good'
    else 'MISSING: ' || missing ||
         ' -- this is what causes "401 permission denied for table enquiries"' end;
  return next;

  step := '4. private columns wrongly left open';
  verdict := case when exposed is null
    then 'NONE - good, id/created_at/staff_note are protected'
    else 'EXPOSED: ' || exposed || ' -- re-run section 3b as written' end;
  return next;

  step := '5. rate-limit trigger';
  verdict := case when exists (
      select 1 from pg_trigger
       where tgrelid = 'public.enquiries'::regclass
         and tgname = 'enquiry_rate_limit' and not tgisinternal)
    then 'OK - max 10 per email per hour, 20 site-wide per minute'
    else 'MISSING - re-run section 3c' end;
  return next;

  select count(*) into n from public.staff;
  step := '6. who may sign in to admin.html';
  verdict := case when n = 0
    then 'NOBODY - add your address to the staff table'
    else n || ' address(es): ' ||
         (select string_agg(email, ', ' order by email) from public.staff) end;
  return next;

  -- The one that actually matters.
  begin
    set local role anon;

    insert into public.enquiries
      (name, email, package, route, travel_when, travellers, trip_length,
       budget, interests, notes, status, source, consent_at, marketing)
    values
      ('SETUP SELF-TEST', 'selftest@tripzaceylon.invalid', null,
       'Colombo -> Kandy', '2027-04', '2 people', '7-10 days', 'Mid-range',
       'Wildlife', 'Written and deleted by supabase-setup.sql',
       'new', 'website', now(), false);

    reset role;
    delete from public.enquiries where email = 'selftest@tripzaceylon.invalid';

    step := '7. SELF-TEST';
    verdict := 'PASSED - your website can file an enquiry. '
            || 'The test row was deleted, so your table is still clean.';
  exception when others then
    begin reset role; exception when others then null; end;
    step := '7. SELF-TEST';
    verdict := 'FAILED - ' || sqlerrm
            || ' || The site will say "that did not send" until this is fixed. '
            || 'Read rows 3 and 4 above: they usually name the cause.';
  end;
  return next;

  return;
end;
$fn$;

-- Nobody but you should ever be able to run it, and it is dropped below anyway.
revoke all on function public.zz_tripza_setup_check() from public;

select * from public.zz_tripza_setup_check();

drop function public.zz_tripza_setup_check();
