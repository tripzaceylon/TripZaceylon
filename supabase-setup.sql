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
-- may fill. Without this, someone could POST their own created_at (dating an
-- enquiry into the future so it always sorts to the top of your inbox) or set
-- status to 'booked'. Revoking the table-wide grant and re-granting only the
-- columns a visitor legitimately fills closes that off: everything else falls
-- back to its default.
revoke insert on public.enquiries from anon;
grant insert (name, email, package, route, travel_when, travellers,
              trip_length, budget, interests, notes, consent_at, marketing)
  on public.enquiries to anon;


-- ---------------------------------------------------------------------------
-- 3c. Rate limiting — stops one script filling your free tier
-- ---------------------------------------------------------------------------
-- The anon key is public, so anyone can call the insert endpoint in a loop.
-- SECURITY DEFINER lets this count existing rows even though RLS hides them
-- from the anon role.
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
  if recent >= 5 then
    raise exception 'Too many enquiries from this email address in the last hour.';
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
-- 4. Check it worked
-- ---------------------------------------------------------------------------
-- Should list exactly three policies: one insert, one select, one update.
select policyname, cmd, roles
from pg_policies
where schemaname = 'public' and tablename = 'enquiries'
order by cmd;

-- And the columns anon may actually write (should be 12, no created_at, no status).
select string_agg(column_name, ', ' order by column_name) as anon_may_insert
from information_schema.column_privileges
where grantee = 'anon' and table_name = 'enquiries' and privilege_type = 'INSERT';
