create table if not exists biodesign_leads (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  status text not null default 'nuevo' check (status in ('nuevo', 'contactado', 'cerrado')),
  pool_type text not null,
  size_m2 numeric,
  location text not null,
  budget_range text,
  name text not null,
  phone text not null,
  email text
);

create index if not exists biodesign_leads_created_at_idx on biodesign_leads (created_at desc);
