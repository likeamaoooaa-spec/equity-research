-- Review and apply after confirming the actual schema.
alter table if exists public.annotations enable row level security;
alter table if exists public.replies enable row level security;

drop policy if exists "public read annotations" on public.annotations;
create policy "public read annotations"
  on public.annotations for select
  to anon, authenticated
  using (true);

drop policy if exists "public insert annotations" on public.annotations;
create policy "public insert annotations"
  on public.annotations for insert
  to anon, authenticated
  with check (
    length(coalesce(path, '')) between 1 and 500
    and length(coalesce(quote, '')) between 1 and 1000
    and length(coalesce(text, '')) between 1 and 5000
    and length(coalesce(author, '')) between 1 and 100
  );

drop policy if exists "public read replies" on public.replies;
create policy "public read replies"
  on public.replies for select
  to anon, authenticated
  using (true);

drop policy if exists "public insert replies" on public.replies;
create policy "public insert replies"
  on public.replies for insert
  to anon, authenticated
  with check (
    length(coalesce(text, '')) between 1 and 5000
    and length(coalesce(author, '')) between 1 and 100
  );
